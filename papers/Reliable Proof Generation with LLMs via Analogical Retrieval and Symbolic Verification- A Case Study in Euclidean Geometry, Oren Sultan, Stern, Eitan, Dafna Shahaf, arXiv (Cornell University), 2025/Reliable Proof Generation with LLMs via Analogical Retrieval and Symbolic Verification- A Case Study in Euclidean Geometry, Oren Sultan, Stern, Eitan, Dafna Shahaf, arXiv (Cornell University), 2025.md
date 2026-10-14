                                               Reliable Proof Generation with LLMs via Analogical Retrieval and
                                                  Symbolic Verification: A Case Study in Euclidean Geometry

                                                                      Oren Sultan, Eitan Stern, Dafna Shahaf
                                                                        The Hebrew University of Jerusalem
                                                               {oren.sultan,eitan.stern,dshahaf}@cs.huji.ac.il



                                                                Abstract                            Mathematical proofs demand rigorous logical de-
                                                                                                 duction, symbolic manipulation, and an understand-
arXiv:2505.14479v11 [cs.AI] 31 Aug 2026




                                              Large language models (LLMs) struggle with
                                                                                                 ing of abstract concepts that go beyond statistical
                                              formal domains that require rigorous logical de-
                                              duction and symbolic reasoning, such as math-
                                                                                                 correlations in language. The requirement for ab-
                                              ematical proof generation. We propose a neuro-     solute truth and the absence of ambiguity in math-
                                              symbolic approach centered on the hypothesis       ematical reasoning present a significant challenge
                                              that structurally analogous problems often ad-     for models trained to generate plausible text rather
                                              mit similar proofs. As a proof-of-concept, we      than formally valid inferences (Singh et al., 2024;
                                              focus on SAT-level geometry problems. Our          Pan et al., 2025). In addition, the often lengthy
                                              approach is two-fold: (1) We retrieve analo-       nature of proofs necessitates a level of sustained
                                              gous problems and use their proofs to guide
                                                                                                 logical coherence and hierarchical reasoning that
                                              the LLM, and (2) a formal verifier evaluates
                                              the generated proofs and provides feedback,        is hard for current LLMs. Recent work has shown
                                              helping the model fix incorrect proofs.            that altering even superficial aspects of mathemat-
                                                                                                 ical problems results in significant performance
                                              Our complete pipeline substantially improves
                                              proof accuracy across model families, achiev-      drops (Mirzadeh et al., 2024), suggesting that their
                                              ing 68%-96% accuracy compared with 10%-            success often hinges on pattern matching rather
                                              44% for LLM-only baselines that use neither        than genuine mathematical reasoning.
                                              analogy retrieval nor verifier feedback. When         The lengthy nature of proofs also implies that the
                                              comparing against models with the same veri-       space of possible proofs can get prohibitively large,
                                              fier feedback and inference budget, analogical     and general-purpose LLMs often struggle to search
                                              guidance improves accuracy from 88% to 96%
                                                                                                 through it. We address this challenge through anal-
                                              for GPT-5, 78% to 86% for Claude Sonnet 4.6,
                                              72% to 86% for Gemini-Flash-2.5, and 52% to
                                                                                                 ogy; our central hypothesis is that structurally anal-
                                              80% for OpenAI o1. More broadly, shifting to       ogous geometry problems admit similar proofs.
                                              LLMs that generate provably correct conclu-           In this work, we introduce a neuro-symbolic ap-
                                              sions has the potential to dramatically improve    proach that combines the generative strengths of
                                              their reliability, accuracy and consistency, un-   LLMs with two complementary structured compo-
                                              locking complex tasks and critical real-world      nents: (1) analogical guidance and (2) symbolic
                                              applications that require trustworthiness.         verification. See Figure 1 for an illustration.
                                                                                                    The first component retrieves analogous prob-
                                          1   Introduction
                                                                                                 lems and their proofs to guide the model. This is
                                          LLMs have considerable potential for mathemat-         inspired by cognitive science, where analogy is rec-
                                          ical proof generation (Tafjord et al., 2020; Ya-       ognized as fundamental to human problem-solving
                                          sunaga et al., 2023; Trinh et al., 2024; Ren et al.,   and generalization (Gentner, 1983; Holyoak and
                                          2025). Unlike symbolic theorem provers, LLMs           Thagard, 1996), as well as recent work showing
                                          can directly process natural-language problem de-      that prompting LLMs to generate analogous prob-
                                          scriptions, draw on broad mathematical knowledge       lems and solutions can improve performance on
                                          acquired during pretraining, and flexibly explore      math problems (Yasunaga et al., 2023).
                                          possible proof strategies. However, despite sub-          Since the target proof is unavailable at inference
                                          stantial progress in LLM capabilities, their gener-    time, we construct abstract symbolic representa-
                                          ated proofs remain unreliable without verification     tions of problem statements and learn to predict
                                          (Cobbe et al., 2021; Lightman et al., 2024).           proof similarity from these features. Retrieved
                                                                                            (2)       Veriﬁer

                                                       (1)                                                Feedback

                               Abstracted           Find Analogies
           Target                                                                                    LLM Proof
                                 Target              (problems +
          Problem                                                                                    Generation
                                Problem                proofs)



                                                                 Analogy:
                               Abstracted                                                            Geometry
         FormalGeo             Problems +                                                            Theorem
                                                                 alternate_interior_angle(2,AE,DC)   Dictionary
                                 Proofs
                                                                 angle_sum(1,EDC)


Figure 1: Our neuro-symbolic approach. Given a target problem from the FormalGeo-7k dataset, we first convert
it into an abstract form by replacing entity names (e.g., lines, angles) and specific numeric values with placeholders
( §3.1). We then retrieve structurally similar problems from the abstracted dataset by computing Jaccard similarity
over key formal components: construction (entities and geometric relations), conditions (e.g., angle equalities,
segment lengths), and goal (the conclusion to be proven). This is based on the observation that structurally similar
problems often share proof patterns ( §3.2). The retrieved problems, along with their corresponding formal proofs,
are presented to an LLM as in-context examples, together with the available theorems from the Geometry Theorem
Dictionary, to guide proof generation for the target problem ( §3.3). Finally, a symbolic verifier iteratively checks
the generated proof and provides feedback until a correct proof is produced or a retry limit is reached ( §3.4).


proofs of analogous problems then provide use-                    feedback. In contrast to other works, we evaluate
ful starting points for proof generation and help                 the entire proof, not just the final numeric answer.
identify the most relevant theorems to present to                 (3) Our method substantially improves proof ac-
the model, substantially reducing costs.                          curacy across all models while reducing computa-
   To complement this, our second component em-                   tional cost through focused context construction.
ploys a symbolic verifier that checks the generated               Our complete pipeline achieves 68%-96% accu-
proofs and provides structured feedback. This feed-               racy, compared with 10%-44% for LLM-only base-
back drives an iterative loop, enabling the model to              lines. Under matched inference budgets with veri-
revise its output until a valid proof is obtained.                fier feedback, analogical guidance improves accu-
   As a proof of concept, we focus on Euclidean                   racy from 88% to 96% for GPT-5, 78% to 86% for
geometry – a symbolic, verifiable domain rich                     Claude Sonnet 4.6, 72% to 86% for Gemini-Flash-
in structural analogies. Our goal is to evaluate                  2.5, and 52% to 80% for o1. At the same time, it
whether our symbolic augmentations improve the                    substantially reduces the theorem dictionary size
proof-generation capabilities of general-purpose                  (e.g., from 18K to 2.5K tokens on average for o1).
LLMs. Thus, while we use geometry as our testbed,                 (4) We release data and code at: https://github.
our focus is not on competing with specialized                    com/orensul/LLMs_proof_generation.
state-of-the-art geometry solvers, but rather on
quantifying the gains enabled by our method.                      2    Problem Formulation
   Enabling LLMs to generate formally verifiable
proofs can improve their reliability,1 in applications            We demonstrate our ideas in the domain of Eu-
across math, science and education (Welleck et al.,               clidean geometry. Our input is a geometry prob-
2022; Gupta et al., 2025; Kumar et al., 2023).                    lem, described in both natural language and via
   Our main contributions are: (1) We propose                     a formal representation. The description includes
a neuro-symbolic system that aids LLMs in proof                   the geometric entities involved (e.g., lines, angles),
generation by providing analogical guidance and                   their relationships (e.g., perpendicular, collinear),
verification feedback. (2) We design a symbolic                   and measurements or algebraic expressions over
verifier tailored to geometry proofs with expressive              them. We also receive a goal, some quantity to be
   1
    Throughout this paper, we use reliable to refer to the        determined (e.g., the length of a line). In addition,
generation of proofs formally verified by a symbolic verifier.    the model has access to a dictionary of theorems
                              Problem:                                Theorem Dictionary (GDL):
       Description: “∠ABC=40°, CD||AB,
          BC is perpendicular to AC.
          Find the measure of ∠ECD”                               parallel_property_alternate_interior_angle(AB,CD):
                                                                  {
       Construction:
                                                                     1: {
       Shape(CA,AB,BC), Shape(EC,CD) …
                                                                      premises:
       Construction (extended):
                                                                  ParallelBetweenLine(AB,CD)&Line(AD),
       Shape(AB,BC,CA), Shape(BC,CA,AB) …
                                                                      conclusions: Equal(MeasureOfAngle(BAD), …)
       Conditions:
                                                                        },
       Equal(MeasureOfAngle(ABC),40),
                                                                     2: { ... },
       ParallelBetweenLine(CD,AB) …
                                                                     …
       Goal:
                                                                  },
       Value(MeasureOfAngle(ECD))
                                                                  angle_addition(ABC, CBD): {
       Answer: 50                                                     1: { …},
       Proof:                                                       …
       1) parallel_property_alternate_interior_angle(1,CD,AB)     },
       2) angle_addition(1,ECD,DCB)                               …
       3) adjacent_complementary_angle(1,ECB,BCA)


Figure 2: An example problem from FormalGeo-7k. Left: Problem inputs, including a natural-language description
and formal representations: construction (entities and relations), extended construction (inferred via extension rules),
conditions, and goal. The input also includes a numeric answer (or expression) and a formal proof, with each step
invoking a theorem from the dictionary. Right: The Theorem Dictionary, with theorem IDs, arguments, premises,
and conclusions. The dataset also includes diagrams (which we do not use), shown here for illustration.


that may be used in the proof.                                  identify such problems, the pipeline first ab-
   The output is a formal proof that derives the goal           stracts the target problem and all problems in
from the given conditions and theorems, along with              the dataset. We chose a very simple abstrac-
the final, numeric answer. The proof consists of                tion schema: entity names are replaced with
steps, each applying a specific theorem from the                “<word>” and numbers with “<num>”. For exam-
dictionary. See Figure 2 for an example.                        ple, “Equal(MeasureOfAngle(ABC),40)” becomes
                                                                “Equal(MeasureOfAngle(<word>), <num>)”. This
3     Approach                                                  process is applied to the formal representations of
Our goal is to develop a system that assists LLMs               construction, conditions, and goal. More nuanced
in proof generation. As a proof of concept, we                  abstraction schemas (e.g., preserving shared sym-
focus on geometry problems from the FormalGeo-                  bols between words) are left for future work.
7k dataset (Zhang et al., 2023), containing 6,981
                                                                3.2   Analogous Problems Retrieval
SAT-level Euclidean geometry problems.
   Our approach is two-fold (see Figure 1). Given               Our goal in this section is to retrieve problems
a target problem, we first build on the insight that            whose (known) proof is similar to the (unknown)
structurally similar problems often admit similar               target proof. We conjecture that providing the
proofs. We abstract all problems in the dataset                 model with these proof examples in context will
(§3.1), retrieve analogous problems (similar to the             improve its ability to generate a correct proof.
target on an abstract level, §3.2), and use the top-               Our underlying working hypothesis is that simi-
ranked analogies and their corresponding proofs                 lar problems often yield similar proofs. More con-
as few-shot examples (§3.3). Next, we employ a                  cretely, we posit we can identify problems with
symbolic verifier that iteratively provides feedback            potentially useful proofs by finding analogous prob-
on the validity of the generated proofs (§3.4).                 lems (i.e., problems which are structurally similar
                                                                to the target problem). To do this, we train a re-
3.1    Problem Abstraction                                      gressor to predict proof similarity between two
Analogous problems share a similar underlying                   problems, based on their structural similarity.
structure, but could differ on surface-level de-                Dataset and Training. For each pair of abstracted
tails such as entity names or measurements. To                  problems, we compute the Jaccard similarity over
 k            Analogy               Random               nary, which defines geometry theorems in terms
       Coverage ↑ Theorems ↓ Coverage ↑ Theorems ↓       of formal premises and conclusions (see Figure 2).
 20      88%         11.06       62%         32.92       The LLM’s task is to generate a correct proof, us-
 50      93%         18.57       79%         49.87       ing only the theorems from the dictionary. See
 100     96%         26.66       88%         66.98       Appendix B for the prompt.
 150     98%         31.96       92%         82.82          One challenge we encountered is that the full
                                                         theorem dictionary contains 196 theorems (234 in-
Table 1: Average number of problems whose entire         cluding variations), resulting in a large token count
proof was covered by the union of theorems from their    and, consequently, high costs. This also limits
top-k analogies vs. random problems, over 100 random     scalability, as adding more theorems would further
target problems (20 per level, 1–5). Analogies consis-   increase the input size.
tently achieve higher coverage despite fewer theorems.
                                                            To address this problem, we propose a more effi-
                                                         cient approach. We have just shown that analogous
the multi-sets of construction and condition rep-        problems tend to have similar proofs; thus, we test
resentations. We define goal similarity as 1 if the      whether we could similarly narrow down the dic-
goals match exactly and 0 otherwise. These three         tionary to include only theorems used in analogous
features form the input to our model. Abstract           proofs. This reduction not only reduces costs, but
proof similarity, computed again via Jaccard simi-       also narrows the search space, helping the model
larity, serves as the label.                             focus on more relevant theorems.
   The dataset contains ∼ 24.4M problem pairs (all          To evaluate the effectiveness of this approach,
combinations of 6,981 problems). Proof similarity        we measure the extent to which the narrowed-down
scores are binned into five intervals of width 0.2.      dictionary still captures all the theorems needed for
As the distribution is highly imbalanced, with 88%       the proof of the target problem. We sample 100
of pairs in the first bin (0-0.2), we down-sample        problems (20 from each level 1-5) and evaluate how
all bins to the size of the smallest (131K, 0.8-1),      many of their target proofs are completely covered
yielding a balanced dataset of 655K pairs. We split      using theorems from their top-k similar problems
the data into 90% training and 10% evaluation.           (retrieved with the regressor of Section 3.2), and
                                                         compare to a random set of k problems.
   We train a simple three-layer neural network
                                                            Note that even if a proof of a problem includes a
using mean squared error (MSE) loss and the Adam
                                                         theorem not present in its analogous set, it might
optimizer, with a learning rate of 0.001, batch size
                                                         still be possible to construct a valid proof using only
of 32, and 10 epochs. See Appendix A for details.
                                                         the covered theorems. Therefore, our coverage
Evaluation. Note that for our use case, we are
                                                         metric is a conservative estimate of effectiveness.
only interested in whether we can predict very
                                                            See Table 1 for results. Theorems from analo-
high proof similarity. We select all pairs with pre-
                                                         gous problems consistently outperform the baseline
dicted similarity above 0.95 and measure the frac-
                                                         of theorems from random k problems, providing
tion whose ground-truth proof similarity is in the
                                                         higher coverage despite lower number of theorems.
top two bins. While only 1.28% of pairs exceed
                                                         A larger k increases coverage but also expands the
this threshold, 71% of our predictions do.
                                                         input; we find that k = 100 offers a good trade-off,
   We are encouraged by the results, which confirm
                                                         achieving coverage of 96% with only 26.66 theo-
that our regressor can identify proofs similar to
                                                         rems on average, that is 13.6% of the full dictionary.
the (unknown) target proof, based on the target
                                                         Exploring other values of k is left for future work.
problem’s description alone.
                                                         3.4   Verifier Iterative Feedback
3.3    LLM Proof Generation
                                                         We next endow the LLM with an external verifier
We use a few-shot prompt (in-context learning)           that can guide it through a feedback loop. This is in-
that begins with the target problem, including its       spired by similar efforts showing that code-writing
textual description, construction, conditions and        LLMs can improve with iterative corrections (Peng
goal. This is followed by the top analogous prob-        et al., 2025; Palavalli and Santolucito, 2024). Af-
lems selected using the regressor from Section 3.2,      ter each attempt to produce a proof, the verifier
along with their full proofs and numeric answers.        provides natural-language feedback, specifying the
Additionally, the LLM is given a theorem dictio-         first error found in the proof. The LLM incorpo-
rates it into its context for the next iteration. The    A Note on Baselines for Comparison. Our goal is
loop continues until the proof is verified or the max-   to measure how symbolic augmentation improves
imum number of retries is reached (see Section 4).       formal proof generation in existing LLMs, rather
   The verifier is a symbolic reasoning system ca-       than compete with specialized geometry solvers.
pable of performing both formal logic checks and         Similarly, we evaluate whether analogy retrieval
algebraic reasoning. Internally, it encodes proof        improves proof generation, rather than optimize
steps and geometric constraints as logical formu-        the retrieval method itself. We evaluate retrieval in
las and algebraic expressions, and evaluates them        three ways: intrinsic retriever evaluation via proof-
using satisfiability modulo theories (SMT).              similarity prediction (§3.2); intrinsic comparison
   Importantly, the verifier does not know the so-       to random retrieval via theorem coverage (Table 1);
lution. Instead, it assesses whether the numerical       and extrinsic comparison to random retrieval via
answer is entailed by the constraints imposed by         downstream proof accuracy under matched infer-
the proof. If the proof is valid and the answer can      ence budgets (Table 2). Comparisons with addi-
indeed be inferred from it, the proof is accepted.       tional retrieval methods are left to future work.
Error tiers. To analyze where the LLM struggles,            We now share details on our experimental setup.
we define three verifier-identified error tiers:         Input problems. We randomly sample 10 prob-
  1. Theorem call syntax violation: Syntax errors.       lems for each difficulty level from 1 to 5 from the
      Common issues include undefined theorems           FormalGeo-7K dataset, resulting in a total of 50
      or incorrect argument signatures.                  problems. Levels correspond to the number of steps
  2. Premise violation: Theorem calls that rely on       in the ground-truth proof.
      premises that have not been derived from the       Base models. We evaluate reasoning-capable mod-
      problem description or preceding proof steps.      els from multiple families using recommended
      Feedback identifies the missing premise and        configurations. We evaluate OpenAI’s o1 (Jaech
      lists all premises derived so far.                 et al., 2024), GPT-5 (OpenAI, 2025), Gemini-2.5-
  3. Goal not reached: The proof contains no er-         Flash (Comanici et al., 2025) and Claude Sonnet
      rors but does not reach the goal. Feedback         4.6 (Anthropic, 2026). Throughout the paper, base-
      indicates that either (1) the proof is undercon-   line refers to the non-augmented variant of each
      strained and multiple solutions exist, or (2)      of these models (i.e., without our neuro-symbolic
      that the (unique) solution derived by the veri-    method), rather than to any specific model.
      fier differs from the LLM’s answer.                   We use OpenAI o1 with the default settings;
See Appendix C for examples of error messages            GPT-5 with medium reasoning; Gemini-2.5-Flash
from the different tiers.                                with t=0.7; and Claude Sonnet 4.6 with t=1.0. Full
Implementation details. To identify tier-1 errors,       configuration details are provided in our codebase.
we extended the implementation of Zhang et al.              We additionally evaluated non-reasoning mod-
(2023). To identify tier-2 and tier-3 errors we use      els, including GPT-4 and GPT-4o (Achiam et al.,
the Z3 Theorem Prover (De Moura and Bjørner,             2023; Hurst et al., 2024), and found that they fre-
2008), a state-of-the-art SMT solver, that encodes       quently generate proofs with numerous syntax er-
algebraic constraints derived from geometric prop-       rors. Smaller open-weight models such as Qwen-3-
erties and verifies their logical consistency.           8B and Qwen-3-14B (Yang et al., 2025) similarly
   We also augment Z3 with symbolic workarounds          struggle to adhere to the required output format.
for trigonometric functions it does not natively sup-    Few-shot variants. For each base model, we eval-
port. See Appendix C for more details.                   uate two variants: an analogy-based variant using
                                                         our method, and a baseline variant without it.
4   Experimental Setup                                       • Analogy-based: We provide k similar (analo-
                                                               gous) problems and their proofs as few-shot
We evaluate the performance of our method on the               examples, along with an abridged theorem
FormalGeo-7K dataset. Our main research ques-                  dictionary which includes only theorems from
tions are as follows:                                          the proofs of similar problems (Section 3.3).
RQ1: Does our method lead to a higher rate of                • Base model (non-analogy): We provide k
correct proofs generated by the LLM?                           random problems and their proofs as few-shot
RQ2 (Ablation): What is the individual contribu-               examples, along with the complete dictionary.
tion of different components in our method?              A note about k. In our preliminary exploration, no
model was able to correctly follow the proof format     5     Results
with zero-shot prompts (unsurprisingly). We have
found that k = 5 works well in practice; testing the    Table 2 shows the results for the different settings.
effect of k in more depth is left for future work.
                                                        5.1 RQ1: Performance gains of our approach.
Feedback iterations and multiple runs. For each
base model and variant (analogy-based and non-          We first compare our full pipeline, ours3,5 , against
analogy), we evaluate several inference settings        the minimal base1,1 baseline. Our method substan-
involving verifier-guided feedback and repeated         tially improves accuracy across all models: from
runs. As outlined in Section 3.4, we integrate the      10% to 80% for o1, 22% to 86% for Gemini, 28%
LLM into a feedback loop guided by a verifier,          to 86% for Claude, and 44% to 96% for GPT-5.
allowing the LLM up to five iterations (retries fol-       To isolate the contribution of analogical guid-
lowing feedback) per run. In addition, since LLMs       ance, we compare base3,5 and ours3,5 , which use
sometimes fail to progress toward the correct so-       the same inference budget and verifier feedback
lution (even with feedback), we allow restarting        and differ only in analogical guidance. Accuracy
from scratch up to three times per problem. Within      still improves across all models: from 52% to 80%
each run, the conversation is append-only: failed       for o1, 72% to 86% for Gemini, 78% to 86% for
attempts and verifier feedback are retained, and        Claude, and 88% to 96% for GPT-5.
each retry conditions on the full interaction history      Finally, we evaluate our method with a single run
within that run. The n runs are independent, each       (ours1,5 ), isolating the benefit from multiple runs.
starting from a fresh context.                          Even without multiple runs, accuracy reaches 68%
   Overall, we evaluate four base models, each un-      for o1, 74% for Gemini, 78% for Claude, and 96%
der two prompting variants and three inference set-     for GPT-5, compared with 10%, 22%, 28%, and
tings: single-pass, verifier-guided feedback itera-     44% for base1,1 , respectively. Overall, these results
tions, and multiple independent runs with feedback      show substantial gains from our approach across
iterations. In total, this yields 24 configurations.    models and inference settings. See Appendix D for
                                                        detailed results and significance tests.
   We denote the different configurations by basei,j
or oursi,j , where i is the number of runs and j the
                                                        5.2    RQ2: Ablations.
number of verifier-guided retries.
                                                        We assess each of our method’s components: anal-
Metric. We report the fraction of problems for
                                                        ogy retrieval, the verifier, and multiple runs.
which the model produces a correct proof, for the
following settings:                                     Analogy retrieval. To isolate the effect of anal-
                                                        ogy retrieval, we compare our method to the base
   • First run, no retries (%): The model pro-          model under three settings: (1) single run no re-
     duces a correct proof on its first attempt.        tries, (2) single run with verifier-based retries, and
   • First run, with retries (%): Any of m retries      (3) multiple runs with verifier-based retries. In set-
     (following feedback) in the first run succeeds.    ting (1), our method substantially improves over
   • Multiple runs, with retries (%): Any at-           the baseline: o1 increases from 10% to 48% accu-
     tempt across n independent runs (each with         racy, Gemini from 22% to 48%, Claude from 28%
     up to m retries) succeeds.                         to 60%, and GPT-5 from 44% to 64% ( base1,1
   More runs and retries increase costs; we found       and ours1,1 ). In setting (2), our method again im-
m = 5, n = 3 to provide a good tradeoff between         proves the baseline: o1 increases from 38% to 68%,
performance and budget, and analyze their effect in     Gemini from 58% to 74%, Claude from 58% to
the next section. Based on logged API calls, token      78%, and GPT-5 from 80% to 96% (base1, 5 and
usage, and current pricing, evaluating 50 problems      ours1, 5). In setting (3), our method continues to
costs approximately $100 (o1), $3 (GPT-5), $1           outperform the baseline: o1 improves from 52%
(Gemini-2.5-Flash), and $10 (Claude Sonnet 4.6).        to 80% accuracy, Gemini from 72% to 86%, and
The baseline is approximately 3× more expensive,        Claude from 78% to 86%, while GPT-5 from 88%
since it prompts with the full ∼18K-token theorem       to 96% (base3, 5 and ours3, 5). Overall, analogy
dictionary rather than our ∼2.5K-token analogy-         retrieval consistently improves performance across
derived dictionary, resulting in substantially larger   all settings. See Appendix E for a detailed analysis,
prompts and typically more verifier-guided retries.     and statistical significance tests.
                          First run, no retries            First run, w/ retries    Multiple runs, w/ retries
 Model                  base1,1 ours1,1        ∆      base1,5 ours1,5          ∆    base3,5 ours3,5        ∆
 o1                       10%       48%      +38%          38%     68%      +30%      52%      80%       +28%
 GPT-5                    44%       64%      +20%          80%     96%      +16%      88%      96%       +8%
 Gemini-Flash-2.5         22%       48%      +26%          58%     74%      +16%      72%      86%       +14%
 Claude Sonnet-4.6        28%       60%      +32%          58%     78%      +20%      78%      86%       +8%

Table 2: Proof accuracy (%) of the base model and our analogy-based method across settings. basei,j denotes the
base model with up to i runs and j retries, while oursi,j denotes our method. ∆ indicates absolute improvement
(percentage points). Our method consistently improves proof accuracy across all models and settings.


   The comparison above varies both example se-              5.3   Analysis.
lection (retrieved vs. random) and theorem dictio-
                                                             We provide additional analysis of our results,
nary (analogy-derived vs. full). To isolate their con-
                                                             demonstrated on the o1 model; similar trends are
tributions, we evaluate three intermediate configu-
                                                             observed for the other models.
rations (Table 3): (i) retrieved + full dictionary, (ii)
                                                             Effect of m and n parameters. Figure 3 shows
random + narrowed dictionary, and (iii) retrieved +
                                                             the average number of retries (top) and runs (bot-
random size-matched dictionary.
                                                             tom) per problem by difficulty level. Dashed line
                                                             represents maximum allowed, but the method stops
   Our full method performs best across all infer-
                                                             early if it reaches a valid proof. Our method con-
ence budgets; (i) and (iii) outperform (ii), demon-
                                                             sistently requires fewer retries and runs than the
strating the benefit of analogy retrieval, while our
                                                             base model across all levels. On average, it uses
gains over (i) and (iii) demonstrate the additional
                                                             4.6 retries and 1.58 runs per problem, compared to
benefit of analogy-derived theorem selection.
                                                             8.92 retries and 2.12 runs for the base model.
Verifier feedback. We evaluate the impact of                 Proof accuracy given correct numerical answers.
verifier-guided retries. As shown in Table 2, allow-         To isolate proof-generation failures from answer-
ing retries consistently improves performance. For           generation failures, we evaluate whether models
our analogy-based method, retries improve accu-              can produce a correct proof given that they found
racy from 48% to 68% for o1, from 48% to 74% for             the correct numerical answer.
Gemini, from 60% to 78% for Claude, and from                    We report numerical accuracy as pass@k, where
64% to 96% for GPT-5 ( ours1, 1 and ours1, 5).               k indexes sequential, verifier-guided attempts, up
The effect is even more pronounced for the base              to the complete inference budget B=15 (3 runs
model, where verifier feedback increases accuracy            × 5 verifier-guided retries per run). For o1 with
from 10% to 38% for o1, from 22% to 58% for                  our analogy-based method, pass@1 = 90% (45/50),
Gemini, from 28% to 58% for Claude, and from                 pass@5 = 98%, and pass@B = 100%. Our method
44% to 80% for GPT-5 (base1, 1 and base1, 5).                achieves 100% numerical pass@15, i.e., the correct
                                                             numerical answer appears in at least one attempt for
Multiple runs. While RQ1 compared our full                   all 50 problems, and generates correct proofs for 40
pipeline to the baseline, we now isolate the effect of       of them (80%). In contrast, the base model achieves
multiple runs per method. Specifically, we compare           90% numerical pass@15 (45/50 problems), but
ours3,5 vs. ours1,5 for our approach, and base3,5            only 26 correct proofs (57.7%, vs. 52% overall).
vs. base1,5 for the base model. We find that addi-              Interestingly, the base model often finds the cor-
tional runs consistently improve performance for             rect numeric answer but fails to produce a valid
both variants, yielding gains of 8%-12% for our              proof. We conjecture that the model has a par-
method and 8%-20% for the base model (except                 tial understanding of the proof, yet struggles to
GPT-5 under our method, which saturates at 96%).             express it precisely. By retrieving proofs from anal-
                                                             ogous problems, our method helps bridge this gap,
  To conclude, our method outperforms the                    improving both proof validity and overall answer
baseline across all settings, for every model, with          accuracy (100% vs. 90% numerical pass@15).
each component contributing to performance.                  Stability of results. Our main evaluation uses 50
                                                          Gemini-2.5-Flash              Claude Sonnet 4.6
                                                      1   1 run     3 runs           1   1 run     3 runs
 Setting    Examples Dictionary                      run + retries + retries        run + retries + retries
 Ours     Analogies      Analogy-derived       48%            74%         86%       60%      78%        86%
 (i)      Analogies      Full                  30%            68%         78%       42%      62%        78%
 (ii)     Random         Random-derived        24%            54%         72%       28%      60%        72%
 (iii)    Analogies      Random (size-matched) 32%            60%         78%       36%      66%        74%
 Baseline Random         Full                  22%            58%         72%       28%      58%        78%

Table 3: Controlled ablation of analogy retrieval and theorem-dictionary construction on 50 problems using Gemini-
2.5-Flash and Claude Sonnet 4.6. Our full method performs best across all inference settings.




Figure 3: Average number of retries (top) and runs        Figure 4: Error distribution by tier for our method vs.
(bottom) per problem by difficulty level. The dashed      (o1) base model. Our method reduces errors across all
line represents maximum allowed. Our analogy-based        tiers, with tier-1 errors being most frequent in both.
method consistently outperforms the base model (o1),
with fewer retries and runs across all levels.
                                                          2 errors, involving theorem calls with violated
                                                          premises, are the least common. This trend also
problems (10 per difficulty level, 1-5). To assess        holds for the base model. Tier-1 errors are frequent
stability, we sample 10 additional problems per           but easily corrected with verifier feedback, whereas
level and rerun our method, observing only 3%             Tier-2 errors reflect deeper geometric reasoning
average per-level variation. The baseline is simi-        failures that often persist across retries. Thus, veri-
larly stable: Gemini-2.5-Flash changes from 72%           fication removes superficial errors, leaving reason-
to 74% (6% per-level variation) and Claude Sonnet         ing failures as the main performance bottleneck.
4.6 from 78% to 80% (4%). These results confirm
                                                          6    Related Work
the robustness of our evaluation sample.
Error analysis. As detailed in Section 3.4, we            Neural Models for Proof Generation. Prior work
categorize verifier errors into three tiers. Figure 4     has used LLMs to generate logical and mathemati-
shows their distribution across difficulty levels. Our    cal proofs (Tafjord et al., 2020; Kazemi et al., 2022;
method yields fewer errors than the base model            Yue et al., 2023). More recently, LLM-based sys-
across all tiers and levels. Tier-1 syntax errors         tems have achieved impressive results in formal the-
are the most prevalent, followed by Tier-3 errors,        orem proving, including medal-level performance
where the proof fails to establish the goal. Tier-        on International Mathematical Olympiad problems
(Ren et al., 2025; Hubert et al., 2026; Chervonyi         erate unlabeled numerical variants of math word
et al., 2025; Tsoukalas et al., 2026; Achim et al.,       problems as in-context examples, whereas we focus
2025). These systems, including DeepSeek-Prover-          on formal proof generation, where such numerical
V2, AlphaProof, AlphaGeometry 2, AlphaProof               variations offer little benefit.
Nexus, and Aristotle, typically rely on specialized
training or large-scale proof search. In contrast, we     7    Conclusions and Future Work
study how structured guidance and symbolic feed-          We introduced a neuro-symbolic approach for
back can improve the proof-generation capabilities        proof generation, coupling LLMs with retrieval
of general-purpose, off-the-shelf LLMs, without           of analogous proofs and symbolic verification. The
additional training.                                      analogies help guide the LLM, and the verifier pro-
   Most closely related is Rango (Thompson et al.,        vides feedback on the generated proofs.
2024), which adaptively retrieves proofs and lem-            We evaluate our approach in Euclidean geometry.
mas from the evolving Coq proof state for next-           Experiments on the FormalGeo-7k dataset show
tactic prediction. In contrast, we retrieve struc-        substantial improvements in proof correctness over
turally analogous problems from problem state-            the base model across four leading LLMs from
ments alone, once before generation, and use their        three families, with each component contributing
complete proofs to guide whole-proof generation           to the gains. It also reduces cost by narrowing the
and select a compact set of relevant theorems, re-        theorem dictionary via analogous proofs. These
ducing context and search space.                          results demonstrate the potential of neuro-symbolic
Neuro-symbolic Methods. Neuro-symbolic ap-                methods for mathematical reasoning.
proaches combine LLMs with symbolic tools. This              In the future, we plan to extend our approach be-
strategy has been shown to be effective for some          yond geometry to other areas, where automated
structured tasks (Szeider, 2024; Régin et al., 2024;      proof verification could help validate complex
Mittal et al., 2024; Wu and Mitra, 2024). Auto-           derivations and ensure the consistency of mod-
formalization methods (Song et al., 2024; Alhessi         els. We also see an interesting use case in educa-
et al., 2025) such as LINC (Olausson et al., 2023)        tion, where analogical retrieval can surface similar
translate natural language into first-order logic us-     solved problems to guide students, and a symbolic
ing an LLM, followed by a symbolic theorem                verifier can offer targeted hints and feedback.
prover. These works focus on logical reasoning               We also aim to explore more expressive forms of
and are not well suited for mathematical or alge-         formal verification, such as model checking with
braic aspects of proofs. One work in the domain           temporal logics (LTL and CTL), enabling reason-
of geometry is AlphaGeometry (Trinh et al., 2024),        ing about dynamic systems that evolve over time,
which combines symbolic deduction with a lan-             as well as more sophisticated mechanisms for anal-
guage model trained on 100M synthetic geometry            ogy retrieval and structural similarity.
examples to generate machine-verifiable proofs. In           We hope this work inspires future research on
contrast, our method does not require training.           neuro-symbolic systems that combine the flexibil-
Analogical Reasoning. LLMs have been studied              ity of LLMs with the precision of formal reasoning,
for analogical reasoning in diverse domains, includ-      as a step toward more reliable AI systems for do-
ing word analogies, narratives and processes, and         mains where correctness is crucial.
visual scenarios. see Sultan et al. (2024) for a sur-
vey. Jobanputra and Demberg (2024) show that re-          Limitations
trieving structural analogies improves LLM-based
data-to-text generation. In mathematics, Yasunaga         General Limitations.
et al. (2023) propose analogical prompting, where             • Generalization beyond geometry. Our ex-
the model generates its own analogous problems                  periments focus on Euclidean geometry, and
and solutions. In contrast, we retrieve structurally            results may differ in other formal domains,
similar problems with verified proofs, avoiding po-             which may involve different proof structures,
tentially incorrect model-generated solutions.                  theorem types, or symbolic representations.
   Zhou et al. (2025) fine-tune models to transfer              While our pipeline is designed to be adaptable
solutions between structurally similar problems,                to any domain that supports SMT-based verifi-
whereas our method requires no training and oper-               cation, further evaluation is needed to confirm
ates entirely at inference time. Lee et al. (2025) gen-         its effectiveness beyond geometry.
Analogy Retrieval Limitations.                         Ethical Considerations
  • Abstraction schema for analogy retrieval.          Dataset. To protect privacy and ensure proper
    We use a simple abstraction method that re-        anonymization, we removed the names of individ-
    places entity names and numbers with place-        ual annotators from the subset of problems used in
    holders. While effective in many cases, this       our experiments and shared on GitHub.
    schema may miss deeper structural nuances or       Use of AI Assistants. We used Claude Sonnet
    semantic relationships, leading to suboptimal      4.6 for coding assistance and GPT-5 for language
    or misleading analogies.                           editing and rephrasing. All AI-generated outputs
Verifier Limitations.                                  were reviewed and edited by the authors to ensure
  • No support for inverse trigonometric. A            alignment with our design goals and original intent.
    key limitation of our verification system is       Acknowledgements We thank the members of
    that the Z3 theorem prover does not support        HyadataLab and NLP-HUJI for their valuable feed-
    inverse trigonometric functions. While we im-      back, as well as the anonymous reviewers for their
    plemented workarounds for direct functions         constructive comments. This work was supported
    such as sine and cosine, the system cannot         by the European Research Council (ERC) under
    verify cases requiring inverse operations (e.g.,   the European Union’s Horizon 2020 research and
    computing θ from cos(θ) = 0.5). This lim-          innovation programme (grant no. 852686, SIAM).
    its our ability to validate proofs where angle
    measures must be derived from trigonomet-
    ric values. Future work could address this         References
    by integrating custom decision procedures for
                                                       Josh Achiam, Steven Adler, Sandhini Agarwal, Lama
    inverse trigonometric reasoning.                     Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
LLM Limitations.                                         Diogo Almeida, Janko Altenschmidt, Sam Altman,
                                                         Shyamal Anadkat, et al. 2023. Gpt-4 technical report.
  • No access to diagrams. Our LLM uses only             arXiv preprint arXiv:2303.08774.
    formal and textual descriptions, without vi-
                                                       Tudor Achim, Alex Best, Alberto Bietti, Kevin Der,
    sual inputs. Although our dataset includes           Mathïs Fédérico, Sergei Gukov, Daniel Halpern-
    rich symbolic annotations, covering geomet-          Leistner, Kirsten Henningsgard, Yury Kudryashov,
    ric entities, relationships, constructions, and      Alexander Meiburg, et al. 2025. Aristotle: Imo-
    extended conditions, some errors arise due           level automated theorem proving. arXiv preprint
                                                         arXiv:2510.01346.
    to the system’s lack of access to visual dia-
    grams. For instance, when reasoning about          Yousef Alhessi, Sólrún Halla Einarsdóttir, George
    arcs, the model may incorrectly infer that           Granberry, Emily First, Moa Johansson, Sorin
    BOD + BOA = AOD instead of the cor-                  Lerner, and Nicholas Smallbone. 2025. Lemmanaid:
                                                         Neuro-symbolic lemma conjecturing. arXiv preprint
    rect relation BOD = BOA + AOD. Such                  arXiv:2504.04942.
    mistakes are less frequent in reasoning about
    line, where properties like collinearity are ex-   Anthropic. 2026. Claude sonnet 4.6.
    plicitly annotated. In some cases, ambiguity
                                                       Yuri Chervonyi, Trieu H Trinh, Miroslav Olšák, Xi-
    in notation further complicates interpretation;      aomeng Yang, Hoang H Nguyen, Marcelo Menegali,
    for example, the angle name ̸ DOB could              Junehyuk Jung, Junsu Kim, Vikas Verma, Quoc V Le,
    refer to the angle itself or its complement, de-     et al. 2025. Gold-medalist performance in solving
    pending on context.                                  olympiad geometry with alphageometry2. Journal of
                                                         Machine Learning Research, 26(241):1–39.
    On the other hand, we note that a recent work
    (Zhang et al., 2024) has shown that multi-         Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
    modal LLMs often struggle with the visual            Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
                                                         Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
    aspects of math problems, often performing           Nakano, et al. 2021. Training verifiers to solve
    better without the images.                           math word problems, 2021. URL https://arxiv.
                                                         org/abs/2110.14168, 9.
  • LLMs are sensitive to prompt phrasing.
    LLMs are sometimes sensitive to small              Gheorghe Comanici, Eric Bieber, Mike Schaekermann,
    changes to the prompts.                              Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Mar-
                                                         cel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al.
  2025. Gemini 2.5: Pushing the frontier with ad-         Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
  vanced reasoning, multimodality, long context, and        son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  next generation agentic capabilities. arXiv preprint      John Schulman, Ilya Sutskever, and Karl Cobbe.
  arXiv:2507.06261.                                         2024. Let’s verify step by step. In International
                                                            Conference on Learning Representations, volume
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:            2024, pages 39578–39601.
  An efficient smt solver. In International conference
  on Tools and Algorithms for the Construction and        Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi,
  Analysis of Systems, pages 337–340. Springer.             Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar.
                                                            2024. Gsm-symbolic: Understanding the limitations
Dedre Gentner. 1983. Structure-mapping: A theoretical       of mathematical reasoning in large language models.
  framework for analogy. Cognitive science, 7(2):155–       arXiv preprint arXiv:2410.05229.
  170.
                                                          Chinmay Mittal, Krishna Kartik, Parag Singla, et al.
                                                            2024. Puzzlebench: Can llms solve challenging
Adit Gupta, Jennifer Reddig, Tommaso Calo, Daniel           first-order combinatorial reasoning problems. arXiv
  Weitekamp, and Christopher J MacLellan. 2025.             preprint arXiv:2402.02611.
  Beyond final answers: Evaluating large lan-
  guage models for math tutoring. arXiv preprint          Theo X Olausson, Alex Gu, Benjamin Lipkin, Cede-
  arXiv:2503.16460.                                         gao E Zhang, Armando Solar-Lezama, Joshua B
                                                            Tenenbaum, and Roger Levy. 2023. Linc: A neu-
Keith J Holyoak and Paul Thagard. 1996. Mental leaps:       rosymbolic approach for logical reasoning by com-
  Analogy in creative thought. MIT press.                   bining language models with first-order logic provers.
                                                            arXiv preprint arXiv:2310.15164.
Thomas Hubert, Rishi Mehta, Laurent Sartran, Mik-
  lós Z Horváth, Goran Žužić, Eric Wieser, Aja Huang,    OpenAI. 2025. Gpt-5.
  Julian Schrittwieser, Yannick Schroecker, Hussain
  Masoom, et al. 2026. Olympiad-level formal mathe-       Mayur Amarnath Palavalli and Mark Santolucito. 2024.
  matical reasoning with reinforcement learning. Na-       Using a feedback loop for llm-based infrastructure as
  ture, 651(8106):607–613.                                 code generation. arXiv preprint arXiv:2411.19043.

                                                          Zhuoshi Pan, Yu Li, Honglin Lin, Qizhi Pei, Zinan Tang,
Aaron Hurst, Adam Lerer, Adam P Goucher, Adam               Wei Wu, Chenlin Ming, H Vicky Zhao, Conghui
  Perelman, Aditya Ramesh, Aidan Clark, AJ Os-              He, and Lijun Wu. 2025. Lemma: Learning from
  trow, Akila Welihinda, Alan Hayes, Alec Radford,          errors for mathematical advancement in llms. arXiv
  et al. 2024. Gpt-4o system card. arXiv preprint           preprint arXiv:2503.17439.
  arXiv:2410.21276.
                                                          Yun Peng, Akhilesh Deepak Gotmare, Michael R Lyu,
Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richard-          Caiming Xiong, Silvio Savarese, and Doyen Sa-
  son, Ahmed El-Kishky, Aiden Low, Alec Helyar,             hoo. 2025. Perfcodegen: Improving performance
  Aleksander Madry, Alex Beutel, Alex Carney, et al.        of llm generated code with execution feedback. In
  2024. Openai o1 system card. arXiv preprint               2025 IEEE/ACM Second International Conference
  arXiv:2412.16720.                                         on AI Foundation Models and Software Engineering
                                                            (Forge), pages 1–13. IEEE.
Mayank Jobanputra and Vera Demberg. 2024. Team-
 saarlst at the gem’24 data-to-text task: Revisiting      Florian Régin, Elisabetta De Maria, and Alexandre Bon-
 symbolic retrieval in the llm-age. In Proceedings of        larron. 2024. Combining constraint programming
 the 17th International Natural Language Generation          reasoning with large language model predictions.
 Conference: Generation Challenges, pages 92–99.             arXiv preprint arXiv:2407.13490.

Mehran Kazemi, Najoung Kim, Deepti Bhatia, Xin Xu,        ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
 and Deepak Ramachandran. 2022. Lambada: Back-              Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe
 ward chaining for automated reasoning in natural           Fu, Qihao Zhu, Dejian Yang, et al. 2025. Deepseek-
 language. arXiv preprint arXiv:2212.13894.                 prover-v2: Advancing formal mathematical reason-
                                                            ing via reinforcement learning for subgoal decompo-
                                                            sition. arXiv preprint arXiv:2504.21801.
Harsh Kumar, David M Rothschild, Daniel G Goldstein,
  and Jake M Hofman. 2023. Math education with            Joykirat Singh, Akshay Nambi, and Vibhav Vineet.
  large language models: Peril or promise? Available        2024. Exposing the achilles’ heel: Evaluating llms
  at SSRN 4641653.                                          ability to handle mistakes in mathematical reasoning.
                                                            arXiv preprint arXiv:2406.10834.
Jaeseong Lee, Wei Yang, Gopal Gupta, and Shiyi Wei.
   2025. Automatic mathematic in-context example          Peiyang Song, Kaiyu Yang, and Anima Anandkumar.
   generation for llm using multi-modal consistency. In     2024. Towards large language models as copi-
  Proceedings of the 31st International Conference on       lots for theorem proving in lean. arXiv preprint
  Computational Linguistics, pages 8908–8924.               arXiv:2404.12534.
Oren Sultan, Yonatan Bitton, Ron Yosef, and Dafna Sha-    Xiaokai Zhang, Na Zhu, Yiming He, Jia Zou, Qike
  haf. 2024. Parallelparc: A scalable pipeline for gen-     Huang, Xiaoxiao Jin, Yanjun Guo, Chenyang Mao,
  erating natural-language analogies. arXiv preprint        Yang Li, Zhe Zhu, et al. 2023. Formalgeo: An exten-
  arXiv:2403.01139.                                         sible formalized framework for olympiad geometric
                                                            problem solving. arXiv preprint arXiv:2310.18021.
Stefan Szeider. 2024. Mcp-solver: Integrating language
   models with constraint programming systems. arXiv      Ben Zhou, Sarthak Jain, Yi Zhang, Qiang Ning, Shuai
   preprint arXiv:2501.00539.                               Wang, Yassine Benajiba, and Dan Roth. 2025. Self-
                                                            supervised analogical learning using language mod-
Oyvind Tafjord, Bhavana Dalvi Mishra, and Peter             els. arXiv preprint arXiv:2502.00996.
  Clark. 2020. Proofwriter: Generating implications,
  proofs, and abductive statements over natural lan-
  guage. arXiv preprint arXiv:2012.13048.                 A    Analogous Problems Retrieval
Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin        We trained a neural network to predict proof sim-
  Fisher, Alex Sanchez-Stern, Yuriy Brun, João F          ilarity between two problems, using the Jaccard
  Ferreira, Sorin Lerner, and Emily First. 2024.
  Rango: Adaptive retrieval-augmented proving for         similarity of their proofs as the target. The model
  automated software verification. arXiv preprint         inputs a 3D feature vector capturing structural and
  arXiv:2412.14063.                                       semantic similarities: (1) Jaccard over abstract con-
                                                          structions, (2) Jaccard over abstract conditions, and
Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He,
   and Thang Luong. 2024. Solving olympiad ge-            (3) goal similarity – computed from abstracted
   ometry without human demonstrations. Nature,           problem representations. The model has three
   625(7995):476–482.                                     fully connected layers: 3→128 (ReLU), 128→64
                                                          (ReLU), and 64→1 (linear). It was trained for 10
George Tsoukalas, Anton Kovsharov, Sergey Shi-
  robokov, Anja Surina, Moritz Firsching, Gergely Bér-    epochs with batch size 32 using MSE loss and the
  czi, Francisco JR Ruiz, Arun Suggala, Adam Zsolt        Adam optimizer (learning rate 0.001).
  Wagner, Eric Wieser, et al. 2026. Advancing math-
  ematics research with ai-driven formal proof search.    B   LLM Proof Generation
  arXiv preprint arXiv:2605.22763.
                                                          See Figure 5 for the system prompt provided to
Sean Welleck, Jiacheng Liu, Ximing Lu, Hannaneh           the LLMs, and Figure 6 for few-shot examples of
  Hajishirzi, and Yejin Choi. 2022. Naturalprover:
  Grounded mathematical proof generation with lan-        analogous problems and their solutions (including
  guage models. Advances in Neural Information Pro-       proof, and answer).
  cessing Systems, 35:4913–4927.
                                                          C    Verifier Implementation Details
Erik Wu and Sayan Mitra. 2024. Can llms plan paths
  with extra hints from solvers?    arXiv preprint        Geometric reasoning module. We represent
  arXiv:2410.05045.                                       each problem state using a structured system of
An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,          Python classes that encodes geometric facts, such
  Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,             as point orderings, segment lengths, and angle rela-
  Chengen Huang, Chenxu Lv, et al. 2025. Qwen3            tionships. To enhance robustness and flexibility, we
  technical report. arXiv preprint arXiv:2505.09388.      apply normalization procedures that map geometric
Michihiro Yasunaga, Xinyun Chen, Yujia Li, Panupong       objects to canonical, direction-agnostic forms. For
  Pasupat, Jure Leskovec, Percy Liang, Ed H Chi, and      example, treating ̸ ABC and ̸ CBA as equivalent.
  Denny Zhou. 2023. Large language models as ana-
  logical reasoners. arXiv preprint arXiv:2310.01714.     Algebraic constraint solver. We use the Z3 The-
                                                          orem Prover, a state-of-the-art SMT solver, to rep-
Xiang Yue, Xingwei Qu, Ge Zhang, Yao Fu, Wen-             resent and enforce algebraic constraints implied by
  hao Huang, Huan Sun, Yu Su, and Wenhu Chen.
  2023. Mammoth: Building math generalist models          geometric statements. When a proof step estab-
  through hybrid instruction tuning. arXiv preprint       lishes a fact like collinearity of points A, B, C, and
  arXiv:2309.05653.                                       D, the system automatically generates angle equal-
                                                          ity constraints (e.g., ̸ XAB = ̸ XAC = ̸ XAD
Renrui Zhang, Dongzhi Jiang, Yichi Zhang, Haokun
  Lin, Ziyu Guo, Pengshuo Qiu, Aojun Zhou, Pan Lu,        for any reference point X).
  Kai-Wei Chang, Yu Qiao, et al. 2024. Mathverse:
  Does your multi-modal llm truly see the diagrams in
                                                          Handling of Trigonometric Expressions. Z3
  visual math problems? In European Conference on         does not natively support trigonometric functions.
  Computer Vision, pages 169–186. Springer.               To work around this limitation, we:
    • Introduce symbolic variables for trigonomet-       model (non-analogy), under the same three settings:
      ric expressions (e.g., cos_ABC).                   (1) first run, no retries, (2) first run, with retries
                                                         (verifier), (3) multiple runs, with retries (verifier).
    • Add angles referenced by trigonometric terms
                                                             In setting (1) our method achieved an overall
      to the system’s internal constraint graph.
                                                         accuracy of 48%, substantially outperforming the
    • Evaluate goals involving trigonometric expres-     baseline’s 10% (blue circle vs. red hollow circle),
      sions either by matching against known values      p =3.81e-06 in the McNemar test at the 0.05 level.
      or by reasoning symbolically if exact evalua-      In setting (2), our method achieved 68% overall
      tion is not possible.                              accuracy, while the base model reaches 38% (blue
                                                         square vs. red hollow square), p =6.10e-05 in the
Verifier Examples Figure 7 presents a represen-
                                                         McNemar test at the 0.05 level. In setting (3) we
tative example of error outputted by the verifier,
                                                         observe a 80% overall accuracy for our method vs.
from each error tier.
                                                         52% for the base model (blue triangle vs. red hol-
D    RQ1: Performance Gains                              low triangle). This improvement is also statistically
                                                         significant, with p =1.22e-04 in the McNemar test
We provide additional details on the results and sta-    at the 0.05 level. That is, analogy retrieval boosts
tistical analyses, focusing on the o1 model; similar     model performance across all settings.
trends are observed across other models.                 Disentangling analogy retrieval and theorem
   Figure 8 shows the results on o1 model for the        dictionary construction. The comparison above
different settings. We start by comparing our full       jointly varies two factors: whether examples are re-
pipeline (blue triangle: analogy + verifier, multiple    trieved analogies or random problems, and whether
runs with retries), to the most basic baseline (red      the theorem dictionary is analogy-derived or full.
hollow circle: non-analogy, no verifier, first run, no   To isolate each factor’s individual contribution, we
retries). Our full pipeline consistently outperforms     evaluate three additional configurations on Gemini-
the baseline at every level, achieving an average        Flash-2.5 and Claude Sonnet-4.6, using the same
aggregated accuracy of 80%. In contrast, the base        50 evaluation problems and inference protocol (Ta-
model achieves an average of only 10% (with 0%           ble 3): (i) retrieved analogies with the full theorem
accuracy on levels 3 and above). This difference         dictionary, isolating the effect of analogy retrieval
is statistically significant with p =5.82e-11 in the     alone; (ii) random examples with a theorem dictio-
McNemar test at the 0.05 level (our method solved        nary narrowed from those random examples, iso-
all problems the base model did, plus 35 others).        lating the effect of dictionary narrowing without
   To isolate the contribution of multiple runs, we      analogy retrieval; and (iii) retrieved analogies with
also evaluated our model after a single run (blue        a random, size-matched theorem dictionary, iso-
square). This setting also substantially outper-         lating the effect of the analogy-derived theorem
formed the base-model baseline, achieving an over-       selection specifically.
all accuracy of 68%, with p =3.73e-09 in the Mc-             Our complete method consistently achieves the
Nemar test at the 0.05 level. Thus, we conclude that     best performance across all evaluation settings, and
our method significantly boosts the base model’s         is the top-performing configuration for both models
success rate in generating correct proofs, even with-    under a single attempt, verifier-guided retries, and
out multiple runs. See Figures 10, 9, and 11 for the     the full inference budget.
corresponding results on Gemini-Flash-2.5, Claude            The intermediate ablations further validate the
Sonnet-4.6, and GPT-5, respectively.                     contribution of analogy retrieval. Both setting (i)
                                                         (retrieved analogies + full dictionary) and setting
E    RQ2: Ablations
                                                         (iii) (retrieved analogies + random size-matched
We provide additional details on the results and sta-    dictionary) consistently outperform setting (ii)
tistical analyses, focusing on the o1 model; similar     (random examples + narrowed dictionary), show-
trends are observed across other models.                 ing that retrieving analogous proofs provides use-
   We now assess the contribution of the different       ful guidance even before considering theorem-
components of our pipeline: The analogy retrieval,       dictionary construction. Compared with the base-
the verifier, and the multiple runs.                     line, settings (i) and (iii) improve performance in
Analogy retrieval. To measure the effect of anal-        nearly all evaluation settings, with the largest gains
ogy retrieval, we compare our method to the base         on the first attempt (e.g., +8 and +10 points for
Gemini, +14 and +8 points for Claude).                   difference across levels is 3%. We conclude our
   Finally, comparing our method with settings (i)       results are stable.
and (iii) isolates the contribution of the analogy-         We additionally repeat this stability check for the
derived theorem dictionary. Replacing the analogy-       baseline (non-analogy) variant, on Gemini-Flash-
derived dictionary with either the full theorem dic-     2.5 and Claude Sonnet-4.6, given its substantially
tionary (setting (i)) or a random size-matched dic-      higher inference cost relative to our method (the
tionary (setting (iii)) consistently reduces accuracy,   baseline prompts with the full theorem dictionary
demonstrating that the improvement comes from            rather than our analogy-derived, narrowed one).
selecting theorems that are specifically relevant to     Baseline accuracy is similarly stable when increas-
the retrieved analogies, rather than simply reducing     ing the evaluation set from 50 to 100 problems: for
prompt size. This is consistent with Table 1, where      Gemini-Flash-2.5, overall accuracy increases only
the analogy-derived theorem dictionary retains the       from 72% to 74%, with an average per-level varia-
complete target-proof theorem set for more prob-         tion of 6%; for Claude Sonnet-4.6, overall accuracy
lems than a random-example-derived dictionary of         increases only from 78% to 80%, with an average
comparable size, while reducing the prompt from          per-level variation of 4%. These results confirm
approximately 18K to 2.5K tokens on average.             that our conclusions are robust to the evaluation
Verifier feedback. We now measure the impact             sample size for both the proposed method and the
of retries following feedback. As shown in Fig-          baseline.
ure 8, allowing retries consistently improves results
across all difficulty levels. For our analogy-based
method, retries (blue square) yields an average gain
of additional 20% over no retries (blue circle), with
gains ranging from 10% to 30% at different levels.
The improvement is even more pronounced for the
base model (red hollow square vs. red hollow cir-
cle), where verifier feedback results in an average
gain of 28%, ranging from 10% to 40% per level.
Multiple runs. In RQ1, we evaluated the effect
of multiple runs when comparing our full method
to the base model. We now analyze the impact of
multiple runs for the same method (blue triangle
vs. square, red hollow triangle vs. square). We
find that additional runs improve performance for
both our method and the base model. Notably,
for our method multiple runs help more on harder
problems (gains of 20-30% for levels 4-5), where
the potential for improvement is greater.
   To conclude, our method outperforms the base-
line across all settings, with each component con-
tributing to performance. Although the verifier
alone does enhance the base model’s results, anal-
ogy retrieval supplies stronger initial proof candi-
dates for the verifier to correct.

F   Stability of Results
Figure 12 shows the performance of our method on
both the original 50 samples and the extended set
of 100 samples, broken down by level. As shown,
performance remains unchanged in levels 2, 3, and
5, while levels 1 show 5% difference, and level
4 4 show a 10% difference. Overall, the average
You are a mathematician expert in solving geometry problems.
Your task is to solve Problem B by constructing the correct sequence of theorems (THEOREM_SEQUENCE) to form its proof.

Inputs:
You are given:
Problem B, which you need to solve.
Five analogous problems (A1, A2, A3, A4, A5) that have similar proof structures. These are provided to help guide your
approach to solving Problem B.
Geometry Theorem Dictionary (GDL): A dictionary containing various geometry theorems, each with its premise and
conclusion. All theorems in the THEOREM_SEQUENCE must be selected from this dictionary.
GDL_DICTIONARY:
{GDL}
For each problem, you are provided the following data:
DESCRIPTION: A textual description of the problem.
CONSTRUCTION_CDL: The problem’s construction in Condition Declaration Language (CDL).
TEXT_CDL: The text of the problem in CDL.
GOAL_CDL: The goal of the problem in CDL.
CONSTRUCTION_CDL_EXTENDED: An extended version of CONSTRUCTION_CDL.
SYMBOLS_AND_VALUES: Symbols with corresponding values, in the format (predicate;symbol;value).
EQUATIONS: Equations related to solving the problem, in the format (equation).
GOAL_SYMBOL: The symbol you are trying to solve for, in the format (symbol).
ANSWER: The calculated final answer, in the format (answer).
THEOREM_SEQUENCE: The sequence of theorems used in the proof, formatted as:
step_id <step_id>; <theorem>; <premise>; <conclusion>
step_id <step_id>; <theorem>; <premise>; <conclusion>

Your Task:
You need to solve Problem B by constructing the correct THEOREM_SEQUENCE, which should consist of theorems from the
GDL. Ensure that each selected theorem logically follows the previous one and contributes to the goal of solving Problem B.

Output Format:
Your response must contain the following:
EQUATIONS: <equation> <equation> ...
GOAL_SYMBOL: <symbol>
ANSWER: <answer>
THEOREM_SEQUENCE:
<step_id>; <theorem>; <premise>; <conclusion>
<step_id>; <theorem>; <premise>; <conclusion>

Important Notes for the THEOREM_SEQUENCE:
Do not include the words "theorem", "premise", or "conclusion". Your sequence should only contain the step ID, theorem name,
premise, and conclusion.
Use the exact theorem names and formats provided in the GDL.
Start with step_id = 1 and increment sequentially.
When referring to angles, use three letters (e.g., ABC for the angle at B). Be mindful of the order, as ABC is different from
ACB. For polygons, list all distinct points in clockwise or counterclockwise order. For example, a polygon with points FGE can
also be referred to as GEF or EFG.

Example of Correct THEOREM_SEQUENCE Format:
1; angle_addition(1,BFE,EFG);
Angle(BFE)&Angle(EFG)&Angle(BFG);
["Equal(MeasureOfAngle(BFG),Add(MeasureOfAngle(BFE),MeasureOfAngle(EFG)))"]
2; triangle_property_angle_sum(1,DFC); Polygon(DFC);
["Equal(Add(MeasureOfAngle(DFC),MeasureOfAngle(FCD),MeasureOfAngle(CDF)),180)"]

Reminder:
Ensure that the theorems you select come from the GDL, follow the correct format, and use the proper arguments (e.g., angle
order and polygon points). Also, pay attention to the specific variation of the theorem (e.g., 1 for the first variation, 2 for the
second, etc.).

Figure 5: System prompt given to the o1 LLM for generating a geometry proof for a target problem B. The model
is provided with all details about the task, as well as a Geometry Theorem Dictionary (GDL) and five analogous
problems (A1–A5), which are supplied as few-shot examples (see Figure 6).
Inputs for Problem A1:
DESCRIPTION:
As shown in the diagram, Div(LengthOfLine(AD)=LengthOfLine(DF)), Div(LengthOfLine(DF)=LengthOfLine(FB)), AG=15,
DE is parallel to BC, DE is parallel to FG, FG || BC. Find the length of line CE.

CONSTRUCTION_CDL:
Shape(AD,DE,EA), ...
Collinear(ADFB), ...

TEXT_CDL:
Equal(Div(LengthOfLine(AD),LengthOfLine(DF)),3/2), ...
ParallelBetweenLine(DE,BC), ...

GOAL_CDL:
Value(LengthOfLine(CE))

CONSTRUCTION_CDL_EXTENDED:
Shape(DE,EA,AD), ...
Collinear(BFDA), ...
Point(A), ...
Line(AB), ...
Angle(ADF), ...
Polygon(ADE), ...
ParallelBetweenLine(CB,ED), ...

SYMBOLS_AND_VALUES:
LengthOfLine(AG);ll_ag;15, ...

Outputs for Problem A1:
EQUATIONS:
ll_ad/ll_df - 3/2, ...

GOAL_SYMBOL:
ll_ce

ANSWER:
9

THEOREM_SEQUENCE:
...


Inputs for Problem A2:
...

Inputs for Problem A3:
...

Inputs for Problem A4:
...

Inputs for Problem A5:
...

Outputs for Problem B:

Figure 6: Few-shot prompt shown to the o1 LLM, consisting of five analogous problems (A1–A5) along with their
inputs and solutions – including the final answer and theorem sequence used in the proof. Note: “...” indicates
omitted content for brevity.
Tier 1 (Syntax Violation)

Theorem: parallel_property_ipsilateral_internal_angle(1,GA,HD)
You output the following premises: ParallelBetweenLine(GA,HD)&Line(AD)
But the correct premises: ParallelBetweenLine(GA,HD)&Line(GH)

Tier 2 (Premise Violation)

- Error: You tried to use theorem: right_triangle_judgment_angle(1,BCD);
Polygon(BCD)&Equal(MeasureOfAngle(BCD),90);[’RightTriangle(BCD)’]

Missing premise: Angle measure 90° for triangle BCD is not established in the
premise.
Details: Premise provided: Polygon(BCD)&Equal(MeasureOfAngle(BCD),90)
- Available premises:
Perpendicular Lines: AD, BD
Collinear Points: ADC
Polygons: ABC, ABD, ACB, ADB, BCD, BDC
- Theorems related to the goal:
Step 1 - right_triangle_judgment_angle(1, BCD): RightTriangle(BCD)
- Solver constraints directly related to this goal:
|AB| = y
Please fix the proof.


Tier 3 (Goal Not Reached)

- Goal: measure of angle ADB
- Model answer: 55.0
- Error: Your proof doesn’t uniquely determine the value. You need to use additional
theorems to constrain the value.
- Available premises:
Collinear Points: AOB, BCD
Cocircular Points: A on circle O, AB on circle O, ABC on circle O, AC on circle O,
B on circle O, BC on circle O, C on circle O
Circles: O center: O
Circle Diameters: AB diameter of O
Tangent Lines: DA tangent to O
Polygons: ABD, ADB, ADCO, BCO, BOC, COAD, DCOA, OADC
- Theorems related to the goal: None found that constrain this goal
- Solver constraints directly related to this goal: ̸ ADB ≤ 180,         ̸ ADB > 0,
̸ ADC = ̸ ADB



Figure 7: Examples of verifier errors across three tiers. Tier 1: syntax violations in theorem calls. Tier 2: missing
or undefined premises. Tier 3: under-constrained reasoning that fails to derive the goal.
Figure 8: % correct proofs per level of difficulty (50        Figure 10: % correct proofs per level of difficulty (50
samples, 10 per level). Our analogy-based method out-         samples, 10 per level). Our analogy-based method
performs the o1 base model (non-analogy) in all settings.     outperforms the Gemini-Flash-2.5 base model (non-
Analogy retrieval, verifier feedback, and multiple runs       analogy) in all settings. Analogy retrieval, verifier feed-
each significantly contributes to performance. Our full       back, and multiple runs each significantly contributes
pipeline (blue triangle) outperforms the baseline in ev-      to performance. Our full pipeline (blue triangle) outper-
ery level, reaching an average aggregated accuracy of         forms the baseline in every level, reaching an average
80%. Even without multiple runs (blue square), perfor-        aggregated accuracy of 86%. Even without multiple
mance remains strong at 68%, far exceeding the 10% of         runs (blue square), performance remains strong at 74%,
the base model baseline (red hollow circle).                  far exceeding the 22% of the base model baseline (red
                                                              hollow circle).




Figure 9: % correct proofs per level of difficulty (50 sam-
ples, 10 per level). Our analogy-based method outper-         Figure 11: % correct proofs per level of difficulty (50
forms the Claude Sonnet-4.6 base model (non-analogy)          samples, 10 per level). Our analogy-based method out-
in all settings. Analogy retrieval, verifier feedback, and    performs the GPT-5 base model (non-analogy) in all set-
multiple runs each significantly contributes to perfor-       tings. Analogy retrieval, verifier feedback, and multiple
mance. Our full pipeline (blue triangle) outperforms          runs each significantly contributes to performance. Our
the baseline in every level, reaching an average aggre-       full pipeline (blue triangle) outperforms the baseline in
gated accuracy of 86%. Even without multiple runs             every level, reaching an average aggregated accuracy of
(blue square), performance remains strong at 78%, far         96%. Even without multiple runs (blue square), perfor-
exceeding the 28% of the base model baseline (red hol-        mance remains stable at 96%, far exceeding the 44% of
low circle).                                                  the base model baseline (red hollow circle).
Figure 12: Accuracy remains stable when increasing the sample size from 50 to 100 (10 additional problems per
level), with an average variation of only 3% per level. Per-level differences range from 0% (levels 2, 3, and 5) to 5%
(level 1), and 10% (level 4). We conclude our results are stable.
