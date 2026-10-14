                                               Counterexample Generation via Per-Theorem Symbolic Verifiers:
                                                     When Imitation Hurts and Reinforcement Repairs

                                                 Omar Farouk Zouak1 * Houssam Eddine Boukhalfa1 Soumaya Lakehal1
                                                                Shiv Katiyar2 Samia Nefti-Meziani2
                                                             1
                                                                 National School of Artificial Intelligence, Algiers, Algeria
                                                                      2
                                                                        University of Birmingham, United Kingdom


                                                              Abstract                           tion learning (SFT) often exacerbates this by induc-
                                                                                                 ing format-biases rather than true logical reasoning
                                            Large language models often solve a theorem          (Shao et al., 2025).
arXiv:2610.02444v1 [cs.CL] 1 Oct 2026




                                            forward yet fail to disprove a closely related
                                                                                                    The natural fix is to train counterexample gen-
                                            false one: a falsification gap that supervised
                                            fine-tuning does not close and can actively
                                                                                                 eration directly, but two obstacles have so far pre-
                                            worsen. We frame counterexample genera-              vented this from becoming a primary objective.
                                            tion as constrained witness emission against         First, large-scale counterexample data is scarce:
                                            a deterministic per-theorem Python verifier,         the only widely cited counterexample benchmark,
                                            and release S YM CE, a corpus of 4,707 false         COUNTERMATH, contains 1,216 problems, and
                                            undergraduate-algebra and real-analysis con-         its evaluation is mediated by an LLM judge. Sec-
                                            jectures, each paired with executable verifiers.     ond, supervised fine-tuning (SFT) on counterex-
                                            The verifier also serves as the reward func-
                                                                                                 amples appears insufficient. Counterexample-only
                                            tion, making S YM CE a training environment.
                                            Training Qwen3-4B with SFT followed by               training data contains, by construction, only false
                                            GRPO under this oracle reveals an imitation          statements, and we show below that imitation-only
                                            trap: counterexample-only SFT collapses true-        training transfers this distribution shift into the pol-
                                            theorem recognition from 0.27 to 0.00, while         icy: a model trained purely to emit counterexam-
                                            RLVR with a sparse outcome-only reward re-           ples loses the ability to recognise true statements,
                                            pairs this and exceeds the base, to 0.66. The        and confidently fabricates witnesses on theorems
                                            collapse replicates across four seeds and on
                                                                                                 that are in fact true.
                                            Gemma-3-4B. Sparse and dense rewards yield
                                            statistically indistinguishable in-domain suc-
                                                                                                    We attack both obstacles together.               We
                                            cess yet diverge by 33 points on a held-out          build S YM CE, a deterministic, large-scale
                                            calibration probe, a dissociation we trace to        counterexample environment, by hypothesis-
                                            the partial-credit term. Our 4B model outper-        dropping over 6,748 undergraduate-level
                                            forms every evaluated 7B open-weights math           theorems and generating, for each (theorem_id,
                                            specialist, remains competitive with six fron-       dropped_hypothesis) pair, an independent
                                            tier commercial APIs, and transfers under un-        Python verifier module that returns one boolean
                                            changed prompting to GSM8K, MATH-500
                                                                                                 per remaining hypothesis and one for the negated
                                            and MMLU-college-math. A human audit of
                                            177 verifier decisions finds 97.7 % accuracy.        conclusion. The pipeline retains 4,707 records.
                                            Code, data, verifier modules and annotations:        Evaluation is fully symbolic: the policy emits a
                                            https://github.com/ce-rlvr/SymCE.                    one line Python expression, and the verifier returns
                                                                                                 a boolean tuple. Because the verifier runs in tens
                                        1    Introduction                                        of milliseconds, the same substrate serves as the
                                                                                                 reward function during reinforcement learning, so
                                        Large Language Models (LLMs) excel at forward
                                                                                                 S YM CE is a training environment and not only a
                                        mathematical derivation, but struggle significantly
                                                                                                 benchmark.
                                        with inverse reasoning and generating counterex-
                                                                                                    We use this environment to train Qwen3-
                                        amples to false claims. Recent benchmarks demon-
                                                                                                 4B (Qwen Team, 2025) with SFT followed by
                                        strate that even frontier models fail at falsification
                                                                                                 GRPO under two reward shapes and to evaluate
                                        tasks they can easily forward-solve (Sinha et al.,
                                                                                                 against five 7B open-weights math specialists, six
                                        2025; Li et al., 2025). Furthermore, standard imita-
                                                                                                 commercial-API frontier models, and four external
                                            * Corresponding author: omar.zouak@ensia.edu.dz      mathematics benchmarks. In doing so, we uncover
a pathology: imitation-only training on counterex-       (around 48 %) and counterexample success (below
amples collapses the policy’s ability to recognise       9 %) for the same models. The most directly related
true theorems, and only verifier-grounded RL with        training resource is Learning to Disprove (Li et al.,
an outcome-only reward repairs it. Partial-credit        2026), which constructs roughly 575K hypothesis-
dense rewards yield equal in-domain success but          dropping mutations of Lean 4 Mathlib theorems
do not restore calibration; a dissociation that, to      and uses Lean tactic checks as the verification sig-
our knowledge, has not been previously isolated.         nal. Our dataset is smaller than Li et al.’s but uses
                                                         a Python-verifier substrate that is more faithful to
Contributions. We make four main contri-                 the algebraic and real-analytic structures evaluated,
butions. (C1) The Imitation Trap Pathol-                 runs in tens of milliseconds rather than seconds,
ogy. We isolate a calibration failure mode               and is paired with the witness-schema interface of
in counterexample-only supervised fine-tuning:           §3.2. The Alchemy line of AST-mutation work
Pass@1 on true theorems collapses from 0.27 to           (Wu et al., 2024) focuses on generating valid mu-
0.00 under the training prompt style, because the        tated true theorems for automated theorem proving
policy learns the output form of a counterexample        and is complementary rather than competing.
without the negated-conclusion constraint. The col-
lapse reproduces in all four training seeds and on a
second model family. (C2) Verifier-Grounded              Verifiable-reward reinforcement learning for
RLVR for Falsification. We demonstrate that              mathematics. RLVR with GRPO has become
Reinforcement Learning with Verifiable Rewards           the dominant post-training paradigm for forward
(RLVR), guided by a deterministic symbolic exe-          mathematical reasoning, anchored by DeepSeek-
cution interface, repairs this pathology. Further-       R1 (Guo et al., 2025) and adopted in PRIME (Cui
more, we show that the partial-credit reward term        et al., 2025) and Eurus (Yuan et al., 2024). While
that is the natural dense shaping for this task struc-   recent studies debate whether RLVR installs new
ture preserves logical calibration markedly worse        reasoning or merely elicits latent capabilities via
than an outcome-only reward, and we identify             format adaptation (Shao et al., 2025), our out-of-
the mechanism. (C3) Strong Empirical Perfor-             distribution transfer results (§6.5) suggest falsifi-
mance & Transfer. Our Qwen3-4B RLVR model                cation training installs fundamentally transferable
achieves 0.49 ± 0.02 Pass@1 on in-domain falsifi-        inverse-reasoning skills.
cation across four seeds, outperforming all eval-
uated 7B open-weights math specialists and re-           Process supervision and symbolic verifiers.
maining competitive with frontier APIs, while            Process reward models (PRMs), introduced for
demonstrating strong zero-shot transfer to standard      mathematical reasoning by Lightman et al. (2024)
forward-math tasks (MATH-500, GSM8K). (C4)               and extended by Math-Shepherd (Wang et al.,
S YM CE: A Deterministic Falsification Environ-          2023), and the FOVER pipeline (Kamoi et al.,
ment. To enable this training, we introduce and re-      2026), which mines step-level labels from Z3 and
lease a programmatically verifiable corpus of 4,707      Isabelle traces, supply dense supervision at the step
false algebraic conjectures with per-theorem exe-        level for forward proving. Our per-theorem ver-
cutable verifiers, moving beyond the noisy LLM-          ifier sits between an outcome reward model and
as-a-judge paradigm.                                     a PRM: it returns one boolean per remaining hy-
                                                         pothesis and one for the negated conclusion, which
2   Related Work
                                                         gives the reward function (Eq. 1) a structured, au-
Counterexample and falsification benchmarks.             dited signal without the human-annotation cost of
The closest comparable resource for counterexam-         a learned PRM. PRL (Yao et al., 2026) and self-
ple reasoning is COUNTERMATH (Li et al., 2025),          rewarding correction (Xiong et al., 2025) bear di-
a 1,216-problem benchmark of university-level            rectly on where such an intermediate signal sits;
counterexample-driven proofs evaluated with an           our boolean tuple differs from both in being ex-
LLM-as-judge protocol; the largest frontier model        ternally grounded and non-learned, which is what
reported in that work achieves an F1 of 60.1. RE-        lets §6.3 attribute a behavioural change to one term
FUTE (Sinha et al., 2025) measures counterexam-          of the aggregation. SymPy and Z3 (Meurer et al.,
ple success on algorithmic problems and reports a        2017; De Moura and Bjørner, 2008) provide the
sharp asymmetry between forward solution rates           underlying verification primitives.
The hallucination tax. A growing literature de-             A sandboxed subprocess imports the veri-
scribes a calibration pathology induced by standard      fier dynamically, builds the witness-evaluation
imitation-style training: TreeCut (Ouyang, 2025)         namespace, evaluates the policy’s witness ex-
demonstrates that LLMs continue to fabricate an-         pression string in that namespace, and calls
swers when problems are systematically modi-             conditions(witness), which returns a list of
fied to remove a critical constraint; SUM (Song          booleans, one per remaining hypothesis followed
et al., 2025) and related work report refusal-rate       by one for the negated conclusion. The policy and
collapses of roughly 80 % under standard rejection-      the oracle share no code paths beyond Python’s
sampling fine-tuning on unanswerable-math bench-         eval; the verifier is fixed at the start of training and
marks. Our imitation-trap finding (§6.2) is the          reused across all rollouts for that conjecture.
cleanest measurement of this pathology in the               This is a deliberate departure from prior
counterexample-generation setting we are aware           counterexample-evaluation pipelines: COUNTER-
of, and the first to localise the mechanism, via the     MATH (Li et al., 2025) relies on an LLM-as-judge
reason taxonomy of §6.3, to the partial-credit term      protocol, and Learning to Disprove (Li et al., 2026)
of the reward function.                                  relies on a Lean tactic check. A Python module
                                                         evaluated against a witness expression is interme-
3     Dataset and Verification Environment               diate: it is symbolic and decidable for the subdo-
                                                         mains we target, fast (§3.5), and reproducible.
We frame counterexample generation as a con-
strained generation task: given a false conjecture       3.2    Witness-schema interface
of the form “if H1 ∧ · · · ∧ Hk then Q”, output a wit-
ness w such that all remaining hypotheses hold and       We attach to each prompt a one-line witness
Q fails on w. Our environment is built around three      schema: a short Python-shape description of an
design choices: a per-theorem Python verifier com-       acceptable witness. Schemas are generated post-
piled once and reused across all rollouts, a struc-      hoc by reading the verifier module and its canonical
tured witness-schema interface that constrains the       witness with a second teacher model (DeepSeek)
policy’s output shape, and a conclusion-weighted         and asking for a single-sentence description of the
dense reward whose sparse counterpart we use for         expected Python object shape, with one or two
ablation.                                                concrete examples. Sample schemas are shown in
                                                         Appendix H.
3.1    Source theorems and hypothesis dropping              Schemas are merged into the user prompt. We
                                                         view this as a small but load-bearing methodolog-
We collected 6,748 unique undergraduate-level            ical contribution: a structural prior on the output
mathematical theorems spanning six subdomains            shape, generated automatically from the verifier
(Group, Ring, Field and Number Theory, Linear Al-        and a canonical witness, is what allows for the prac-
gebra and Real Analysis). Each theorem is stored         tical RLVR effectiveness without altering either the
in a structured form with explicit hypotheses and        reward function or the verifier.
conclusion fields. To construct false conjectures we
drop one hypothesis at a time, giving 18,262 candi-      3.3    Split construction
dates. Removing a hypothesis does not guarantee
the result is false or even well-posed — the hy-         We construct three splits with per-domain strati-
pothesis may be redundant or merely clarificatory        fied sampling and a fixed seed (42): the held-out
— so we apply an LLM-driven filter (Gemini 3.1           test set (n=201), the SFT split (n=1,000), and the
Pro): the teacher must classify the mutated theorem      RLVR prompt set (n=3,506). Table 1 summarises
as well-posed and non-trivial, emit a valid Python       the splits.
verifier, and propose a counterexample that evalu-
                                                         3.4    Reward function
ates to True on that verifier without execution er-
rors, with up to 5 retries under error-trace feedback.   The per-rollout reward computed by the oracle is
The teacher produces a verifier for 12,376 candi-
                                                                       shyp
dates; gating then distils these to 4,707 verifier-            r =α·        + β · q¬ + γ · 1[format ok]
backed records over 3,485 unique theorems, of                          nhyp
                                                                  −δ · 1[gave up on false]                   (1)
which 4,700 carry a witness schema (§3.2). We
report per-subdomain counts in Table 1.                           −ε · (1 − 1[parse ok]) ,
                             Pnhyp
where shyp           =         i=1 conditions[i]               Domain          Strict   SFT RLVR Test
counts     satisfied   hypotheses,     q¬      =               GroupTheory      874     366    434    74
conditions[neg_q_index] ∈ {0, 1} is the                        RingTheory       565     237    280    48
                                                               NumberTheory     392     164    195    33
negated-conclusion indicator, and the format /                 LinearAlgebra    233      98    115    20
parse flags come from the structural and witness-              FieldTheory      166      70     82    14
evaluation checks. The penalty δ applies when                  RealAnalysis     159      67     79    13
the policy emits the literal sentinel NONE. Every              Allocated       2389 1002      1185   202
training conjecture is false, so this is always a
give-up signal.                                         Table 1: Domain-stratified allocation of the strict
                                                        pool: the 2,389 records whose teacher-generated canon-
Dense       and   sparse      variants. We              ical witness passes its own verifier at generation time.
study two reward shapes.              Dense:            Rounding the split targets and one oracle-gating drop
α=0.25, β=0.65, γ=0.10, δ=0.30, ε=1.00,                 move three records from SFT and test into the RLVR
                                                        prompt set, so the final split sizes are SFT 1,000, test
range approximately [−1, +1].         Sparse:
                                                        201, and RLVR 1,188 + 2,318 = 3,506; the 2,318
α=γ=δ=0, β=ε=1, range {−1, 0, +1}. The                  loose records have a working verifier but no oracle-
same SFT checkpoint is used as the reference            confirmed canonical witness. Pipeline total: 4,707
policy for both.                                        records over 3,485 unique theorems; canonical-witness
                                                        positive-reward rate 0.98.
Conclusion-weighting bound. A structural prop-
erty of Eq. (1) under dense weights is that
any successful, formatting-compliant rollout            whether each is genuinely a valid counterexam-
(1[format ok] = 1[parse ok] = 1 and                     ple. Of the accepted, 99/101 were confirmed valid
1[gave up on false] = 0) that falls into the            (false-accept rate 2.0 %); of the rejected, 74/76
“hypothesis-only” failure mode (shyp = nhyp , q¬ =      were confirmed invalid, for 97.7 % decision accu-
0) is strictly dominated by any valid rollout that      racy. No case was traced to an incorrect verifier
successfully negates the conclusion (q¬ = 1):           module, and we found no evidence of reward hack-
                                                        ing through verifier acceptance. A single study thus
      rhyp-only = α + γ < β + γ ≤ rneg-Q .              speaks to verifier trustworthiness, hypothesis-drop
                                                        label noise, reward hacking and witness-schema
This structurally precludes the “all hypotheses sat-    quality at once. Composition and the four disputed
isfied but conclusion asserted true” failure mode       decisions are in Appendix B; the annotations are
that affects naïve formulations (Li et al., 2026).      released.
                                                           Operationally, the sandbox is fast enough to
3.5   Verifier audit and operational
                                                        support RLVR at our budget: across the held-out
      measurements
                                                        test set with each record’s canonical witness fed
The verifiers are produced by a teacher model           through the oracle, the median wall-clock per call is
(Gemini 3.1 Pro) and therefore must be audited          132 ms, p95 145 ms, and the maximum 326 ms. No
before they can support a reward signal. We audit       test record approached the eight-second sandbox
the accept/reject decision on real policy outputs       timeout.
rather than the verifier source. The generated ver-
ifiers decide conditions with heuristics and finite     Theorem-truth probe. We construct an auxil-
simplifications that are theoretically incomplete yet   iary set of 347 true theorems drawn from the same
correct on the instances that arise, so a judgement     theorem source. The model is asked to classify
on the source is slow to make and largely subjec-       whether the provided theorem is true or false.
tive; the decision is also the quantity the reward
                                                        4   Training Setup
signal actually depends on. This audit replaces a
hand-curated unit-test suite over the verifier mod-     We train Qwen3-4B (Qwen Team, 2025)
ules, which we abandoned for that reason. We            (unsloth/Qwen3-4B) using Supervised Fine-
sampled 177 model-generated witnesses from the          Tuning (SFT) followed by Group Relative Policy
held-out test split across seeds and training con-      Optimization (GRPO) (Shao et al., 2024). SFT
figurations (101 accepted by the verifier and 76        is performed over 2–3 epochs with a cosine
rejected) and had an author with graduate-level         learning rate schedule (Appendix A). For RLVR,
training in the relevant areas judge independently      we initialise from the SFT adapter and train for 4
epochs (≈ 1,752 steps) using a KL penalty of 0.02         math (n=100), AIME-2024 (n=30) (Cobbe et al.,
against the SFT reference policy. During RLVR,            2021; Hendrycks et al., 2021b,a). All four mod-
we sample G = 4 rollouts per prompt using vLLM            els use identical prompting (standard chain-of-
(Kwon et al., 2023) to maintain high-throughput           thought); our SFT and RLVR splits contain no
generation. Both training stages use LoRA (Hu             examples from these benchmarks and no training
et al., 2022) (rank 16, applied to all attention and      on their answer-extraction formats.
MLP modules) and bfloat16 precision.
   Notably, our entire pipeline is highly computa-        5.3    Decoding and metrics
tionally accessible: training executes on a single        We evaluate under two decoding regimes: greedy
NVIDIA RTX 5090 (32 GB) consumer GPU, with                (temperature 0, n=1) and sampled (temperature
SFT completing in under five minutes and each             0.7, top-p 1.0, n=8). Pass@k for k ∈ {1, 3, 5, 8}
RLVR run taking approximately nine hours. Full            is computed with the unbiased estimator of Chen
hyperparameters, optimizer configurations, and            et al. (2021); greedy Pass@1 is reported as the head-
prompt templates are detailed in Appendix A.              line number throughout. 95 % confidence intervals
                                                          are percentile bootstrap intervals over problem ids
5     Experimental Setup                                  with 10,000 resamples (the unbiased Pass@k esti-
5.1    Models                                             mator is applied per problem before resampling).
                                                          Paired deltas (model A minus model B) bootstrap
We report four model variants from this work: the         over the per-problem Pass@k differences. All
unmodified Qwen3-4B base, SFT checkpoint, and             scripts are released.
two RLVR checkpoints RLVR-dense (Eq. 1 dense
weights) and RLVR-sparse (sparse weights). For            6     Results
external context we evaluate five open-weights 7B
math-specialised models, Abel-7B-002, DeepSeek-           6.1    Counterexample generation
Math-7B-RL, Eurus-2-7B-PRIME, MAmmoTH2-                   Table 2 summarises the main result on the ref-
7B-Plus and Qwen2.5-Math-7B-Instruct (Shao                erence seed. Counterexample-only SFT lifts
et al., 2024; Yang et al., 2024; Cui et al., 2025; Yue    greedy Pass@1 modestly above the Qwen3-4B
et al., 2024), and six frontier commercial APIs from      base (0.30 → 0.35; 95 % CI on the paired delta
the DeepSeek and Gemini families. Per-model               [−0.030, +0.119]), entirely consistent with no sta-
breakdowns of the external comparators are de-            tistically significant gain at this sample size. Con-
ferred to Appendix G; in the main paper we sum-           tinuing with verifier-grounded RL, regardless of
marise them as a best-7B row and a frontier-API           reward shape, yields a substantial further gain to
range. For the cross-family replication of §6.6 we        0.50 [0.43, 0.57] (paired delta versus the base
repeat the pipeline on Gemma-3-4B.                        +0.199 [+0.13, +0.27]). Across four seeds the
                                                          RLVR variants reach 0.49 ± 0.02 (dense) and
5.2    Benchmarks                                         0.46 ± 0.03 (sparse) against an unchanged base of
Counterexample (in-domain, n=201). Our held-              0.30 (Table 5).
out test split (§3.3), stratified by domain. The strict      Three points are worth emphasising. First,
scoring criterion is q¬ =1 ∧ shyp =nhyp ; we also         our 4B RLVR model exceeds every 7B math-
report the relaxed conclusion-pass rate q¬ =1.            specialist open-weights model we evaluated (full
   Theorem-truth (n=347). The model is con-               table in Appendix G); the best 7B baseline (Eurus-
sidered correct iff it recognises the theorem as          2-7B-PRIME at 0.30) is statistically indistinguish-
true. We evaluate two prompt styles: S YM CE-             able from our untrained 4B base (paired CI
prompt (the same prompt style as training) and            [−0.075, +0.065]), which isolates the gain to the
truth-classify (an explicit true/false question).         training method rather than parameter count, and
   A response counts as correct only when the             is consistent with the forward/falsification asym-
model commits to an answer. Permissive extrac-            metry reported by Sinha et al. (2025). Second, the
tion inflates untrained baselines substantially; Ap-      gain holds in expectation under sampled decod-
pendix C reports both readings and validates the          ing: RLVR Pass@8 is 0.68, versus 0.57 for the
rule.                                                     best 7B baseline and 0.49 for the base. Third, our
   External math benchmarks.                  GSM8K       4B RLVR model falls inside the range of greedy
(n=1319), MATH-500 (n=500), MMLU-college-                 Pass@1 measured for six commercial frontier APIs
  Model                                           Pass@1 (greedy) Pass@8 (sampled) Concl.-pass Format-OK Parse-OK
  Qwen3-4B base                                       0.30 [0.24, 0.37]       0.49 [0.42, 0.56]    0.30         0.45        0.42
   + SFT                                              0.35 [0.28, 0.41]       0.64 [0.57, 0.70]    0.41         1.00        0.82
   + RLVR (dense)                                     0.50 [0.43, 0.57]       0.68 [0.61, 0.74]    0.61         0.98        0.94
   + RLVR (sparse)                                    0.50 [0.43, 0.57]       0.67 [0.61, 0.74]    0.59         0.97        0.95
  Best open-weights 7B (Eurus-2-7B-PRIME)             0.30 [0.24, 0.36]       0.57 [0.50, 0.64]    0.34         0.87        0.70
  Frontier APIs (range over 6)a                        0.42 – 0.58             up to 0.77           —            —           —

Table 2: In-domain counterexample benchmark (n=201), reference seed 42. Greedy Pass@1 is the headline metric;
95 % bootstrap CIs in brackets. Conclusion-pass is the relaxed criterion q¬ =1 of §5.2. Four-seed means for the
trained variants are in Table 5. a Range across six DeepSeek/Gemini frontier APIs. The full per-model open-weights
table is in Appendix G.


       Model               S YM CE-prompt truth-classify                   A true theorem from the theorem-truth probe. Contin-
                                                                           uous convergence theorem (Real Analysis): if a sequence
       Qwen3-4B base           0.27            0.36                        of continuous functions satisfies the required convergence
        + SFT                  0.00            0.21                        assumptions, the limit function is continuous.
        + RLVR (dense)         0.34            0.73
        + RLVR (sparse)        0.65            0.84                        SFT output. Counterexample: X = [0, 1], fn (x) = xn ,
                                                                           and                        (
                                                                                                        0 x < 1,
Table 3: Theorem-truth probe (n=347), reference seed                                          f (x) =
                                                                                                        1 x = 1.
42. Pass@1 (greedy) = fraction of true theorems cor-
rectly recognised as true, under the answer-extraction                     The theorem is true. SFT proposes the classical sequence
rules of §5.2. Four-seed means are in Table 5. The                         fn (x) = xn anyway, a construction that violates the con-
                                                                           vergence assumption it would need. RLVR-dense abstains;
base column is conservative: on 62 % of items the base
                                                                           RLVR-sparse recognises the theorem as true and emits
states no verdict at all, exhausting the token budget mid-                 NONE.
reasoning, and it asserts FALSE on only 2.6 %. SFT
reverses this, asserting FALSE for 70 % of true theorems.                 Figure 1: The imitation trap on one item. Appendix F
Four-seed spread for both columns is in Table 5.                          gives the symmetric sparse-reward failure: a false con-
                                                                          jecture the dense model disproves and the sparse model
                                                                          wrongly abstains on.
(0.42–0.58); only one of the six APIs outperforms
it. This supports the claim that a 4B model can be
made competitive with frontier APIs on this task by
training rather than by scale. RLVR also roughly                             Continuing from the same SFT adapter, verifier-
doubles the rate at which the policy negates the con-                     grounded RL with a sparse outcome-only reward
clusion (0.30 → 0.61); the 0.11 that separates this                       repairs and exceeds the base under both prompt
from Pass@1 is rollouts that negate the conclusion                        styles (0.65 and 0.84 respectively). The dense re-
but violate a remaining hypothesis.                                       ward also repairs the more demanding S YM CE-
                                                                          prompt probe, but only to just above the base (0.34
6.2   The imitation trap
                                                                          against 0.27), where sparse reaches 0.65. The dense
Table 3 presents what we view as the central sci-                         and sparse variants are statistically indistinguish-
entific finding of this work. Counterexample-only                         able on the in-distribution counterexample bench-
SFT collapses the model’s ability to recognise true                       mark of §6.1 (Table 2) but differ by 31 percentage
theorems. Under the counterexample-emit prompt                            points on this probe on the reference seed, and
format used throughout training, Pass@1 drops                             by 33 ± 8 points across four seeds. Appendix E
from 0.27 (base) to 0.00 (SFT) on all true theo-                          shows the dissociation is larger still on the subset
rems, in every seed we ran. The collapse is also                          of true theorems whose mutations were never seen
visible under an explicit true/false classification                       in training, so it is not a memorisation artefact.
prompt (0.36 → 0.21), and there it takes a partic-
ularly stark form: where the base model mostly                               This dissociation, equal in-distribution Pass@1
declines to commit, the supervised-only model ac-                         with a large out-of-distribution gap, is interpretable
tively asserts that 70 % of true theorems are false.                      as evidence that the two reward shapes induce qual-
The base model retains genuine calibration; the                           itatively different policies despite producing the
supervised-only model does not. Figure 1 shows                            same counterexample-generation performance. We
one such item.                                                            give the mechanism in §6.3.
                              Counterexample benchmark — per-sample reason distribution (greedy, n=201)                                                                      Counterexample benchmark — per-domain Pass@1 with 95% bootstrap CIs
                              1.0                                                                                                                                  1.0
                                                                                                                                                                            n=74             n=47          n=33           n=20            n=13                n=14
Fraction of greedy rollouts



                              0.8                                                                                                                                  0.8




                                                                                                                                                 Pass@1 (greedy)
                                                                                                          Success
                                                                                                          ¬Q only
                              0.6                                                                                                                                  0.6
                                                                                                          Abstain (NONE)
                                                                                                          Full hypotheses (asserts Q true)
                                                                                                          Partial hypotheses (asserts Q true)
                              0.4                                                                         Parse error                                              0.4
                                                                                                          Format error


                              0.2                                                                                                                                  0.2


                              0.0                                                                                                                                  0.0
                                    Qwen3-4B base      + SFT        + RLVR (dense)   + RLVR (sparse)                                                                     GroupTheory      RingTheory   NumberTheory   LinearAlgebra    RealAnalysis    FieldTheory

                                                                                                                                                                                       Qwen3-4B base      + SFT       + RLVR (dense)        + RLVR (sparse)


Figure 2: Per-sample outcome distribution on the coun-
terexample benchmark (greedy, n=201). The oracle                                                                                                Figure 3: Per-domain counterexample Pass@1 (greedy)
assigns each rollout exactly one outcome: success                                                                                               with 95 % bootstrap CIs. Annotations on top: number
(q¬ =1 and all hypotheses satisfied), ¬Q only (q¬ =1                                                                                            of test items per domain. The largest absolute gain
but not all hypotheses), abstain (the NONE sentinel                                                                                             is on LinearAlgebra (+0.30); the most striking result
on a false conjecture), hyp-only (all hypotheses sat-                                                                                           is on RealAnalysis, where RLVR-sparse gains +0.23
isfied but q¬ =0, so the policy asserts the false con-                                                                                          absolute despite the domain being only 6.7 % of the
jecture is true), partial, parse error and no tag. The                                                                                          RLVR training distribution.
released records carry these as the codes success,
neg_q_only, none_on_false, hyp_only, partial,
oracle_parse_error and no_tag.                                                                                                                     We conclude that when a verifier yields a struc-
                                                                                                                                                tured boolean tuple, an outcome-only aggregator
                                                                                                                                                preserves calibration better than partial credit. Re-
6.3                                   Why it happens: a reason-taxonomy                                                                         warding satisfaction of some but not all hypotheses
                                      analysis                                                                                                  actively trains over-eager counterexample emis-
We exploit the structured reward to label every test                                                                                            sion. The claim is specific to that term rather
rollout with one of seven mutually exclusive out-                                                                                               than to dense rewards in general, and our dense
comes (Figure 2). Three observations explain the                                                                                                reward is not a strawman: its conclusion weighting
imitation trap.                                                                                                                                 (β=0.65 > α=0.25) provably precludes the naive
   SFT trades format errors for logical errors.                                                                                                 hypothesis-only dominance failure (§3.4), and it
The base model rarely emits the trained format at                                                                                               was selected after exploring several dense variants.
all: 55 % of its rollouts carry no tag. SFT solves
this, but the corresponding mass does not move                                                                                                  6.4                      Cross-domain consistency
uniformly into success; instead, the hyp-only cat-                                                                                              Figure 3 stratifies the main result by domain. Both
egory, in which the policy satisfies the remaining                                                                                              RLVR variants improve on the base in every do-
hypotheses but asserts the false conclusion is true,                                                                                            main, with no sign of domain collapse or narrow
rises from 1 % to 31 %. The supervised-only model                                                                                               specialisation. The largest relative gain is on Real
learned the form of a counterexample without learn-                                                                                             Analysis (0.23 → 0.46), despite it being the small-
ing the calibration: it confidently emits objects that                                                                                          est slice of the RLVR training set at 6.7 %. This
fail the negated-conclusion check.                                                                                                              is the inverse of what an over-fitting model would
   Sparse RL re-learns abstention. The absten-                                                                                                  do, and is consistent with the policy learning a
tion rate is 0 % under SFT, 2 % under dense RL, and                                                                                             transferable skill rather than a domain-conditional
10 % under sparse RL. The sparse reward yields                                                                                                  shortcut.
equal score for emitting a wrong witness and emit-                                                                                                 Dense and sparse 95 % CIs overlap in almost
ting NONE, so any rollout the policy is uncertain                                                                                               every domain, supporting the in-distribution equiv-
about is funnelled into abstention; under the dense                                                                                             alence of §6.1 per-domain rather than as an aggre-
reward, the partial-credit term α·(shyp /nhyp ) makes                                                                                           gation artefact.
“try and partially succeed” strictly better than “ab-
stain”. This is the causal mechanism for the 31-                                                                                                6.5                      Out-of-domain transfer
percentage-point gap of Table 3.                                                                                                                Table 4 measures transfer to four standard
   Identical success rates hide diverging failure                                                                                               mathematical-reasoning benchmarks. Training im-
modes. While dense and sparse RL achieve nearly                                                                                                 proves on the base everywhere, with sparse and
identical success fractions (0.502 vs 0.497), dense                                                                                             dense comparable. All four models are evalu-
rewards push the remaining probability mass into                                                                                                ated under identical chain-of-thought prompting,
over-eager hyp-only errors, whereas sparse rewards                                                                                              and our SFT and RLVR data contain no GSM8K,
push it into abstention.                                                                                                                        MATH, MMLU or AIME examples and no train-
 Benchmark (n)      base       SFT          dense       sparse        in Appendix D. The imitation trap is not a seed
 GSM8K (1319)       0.83   0.82 ±.03     0.88 ±.02     0.88 ±.01      artefact: counterexample-only SFT scores exactly
 MATH-500 (500)     0.13   0.55 ±.01     0.65 ±.02     0.65 ±.01      0.00 on the S YM CE-prompt probe in all four Qwen
 MMLU-CM (100)      0.34   0.54 ±.03     0.70 ±.05     0.72 ±.04
 AIME-2024 (30)     0.00   0.07 ±.03     0.08 ±.03     0.08 ±.02
                                                                      seeds. The sparse-over-dense calibration gap on
                                                                      that probe is positive in every seed, at +0.33±0.08.
Table 4: Out-of-domain transfer under standard chain-                 In-domain success stays within noise between the
of-thought prompting (greedy, Pass@1), mean ± sd over                 two reward shapes, dense ahead by 0.02 on average,
all four training seeds. Identical prompt template across             consistent in sign but far inside the test-set boot-
all four models; our SFT/RLVR pipeline contains no                    strap width. And the phenomenon crosses model
examples or answer-format training from these bench-                  families: on Gemma-3-4B the collapse is more
marks.
                                                                      total still, from 0.49 to 0.01 under explicit clas-
                                                                      sification and from 0.40 to 0.00 on the S YM CE-
 Metric                 base      SFT          dense        sparse
                                                                      prompt probe, with both RLVR variants restoring
 Qwen3-4B, mean ± sd over 4 seeds                                     classification above the base. It replicates on a sec-
 S YM CE Pass@1         0.30    0.34 ±.02    0.49 ±.02    0.46 ±.03   ond Gemma seed (24): the same two probes fall
 S YM CE Pass@8         0.49    0.62 ±.02    0.66 ±.02    0.64 ±.02
 Truth S YM CE-prompt   0.27    0.00 ±.00    0.33 ±.04    0.66 ±.04
                                                                      from 0.49 to 0.00 and from 0.40 to 0.00, and dense
 Truth-classify         0.36    0.16 ±.05    0.71 ±.09    0.75 ±.13   RLVR restores classification to 0.54.
 Gemma-3-4B, seed 56                                                     On truth-classify the sparse advantage is smaller
 S YM CE Pass@1         0.21      0.22         0.39          0.34     and less consistent: sparse leads dense by 0.04 ±
 Truth-classify         0.49      0.01         0.53          0.59     0.15, positive in three seeds and negative in seed
                                                                      64. We therefore restrict the sparse-over-dense cal-
Table 5: Robustness of the headline findings. S YM CE                 ibration claim to the probe that shares the training
Pass@k is the counterexample benchmark (n=201); the
                                                                      prompt style, where it holds in every seed. Ap-
two Truth rows are the theorem-truth probe (n=347) un-
der the two prompt styles of §5.2. Qwen3-4B seeds are                 pendix F gives worked examples of both failure
42, 19, 31 and 64; the base is training-seed independent.             modes.
Bold marks the best value in a row.

                                                                      7   Discussion
ing on their answer-extraction formats, so the im-
provements are attributable to transfer rather than                   This is not generic catastrophic forgetting. A
to format adaptation in the training pipeline.                        natural reading of §6.2 is that counterexample-only
   Part of the MATH-500 jump is nonetheless for-                      SFT simply induces forgetting, and that standard
mat adaptation: the base scores 0.13 largely be-                      mitigations such as replay are the appropriate con-
cause it does not follow the answer-extraction tem-                   trol. Four properties argue otherwise. The failure
plate, which SFT installs. GSM8K isolates the rea-                    is selective: after SFT, general mathematical com-
soning gain, because there the base already formats                   petence improves substantially (MATH-500 0.13
answers correctly (0.83), yet RLVR still reaches                      → 0.55, Table 4) while true-theorem recognition
0.88 under the identical prompt while SFT alone                       falls to 0.00, which is closer to the hallucination
does not improve on the base at all (0.82 ± 0.03).                    tax (Ouyang, 2025; Song et al., 2025) than to for-
The transfer therefore arrives with the reinforce-                    getting. The repair exceeds the baseline (0.27 →
ment stage, not the imitation stage.                                  0.66), which recovering previously seen behaviour
   We interpret these results as supporting the                       does not predict. It occurs with zero true theorems
broader narrative motivated in the introduction:                      in training, purely by changing the reward’s treat-
counterexample-style supervision is a fundamental                     ment of abstention; a replay baseline would alter
component of mathematical reasoning that con-                         that distribution and dissolve the phenomenon, so
ventional pre-training under-installs, rather than a                  the controlled comparison is dense versus sparse,
narrow side-skill.                                                    which holds data and initialisation fixed and still
                                                                      differs by 33 points. Finally the mechanism is lo-
6.6   Robustness across seeds and model                               calised to a specific behavioural shift (§6.3), and
      families                                                        generic forgetting offers no account of why two re-
Table 5 repeats the pipeline with three further seeds                 ward shapes on the same checkpoint should differ
and on a second model family; per-seed values are                     at all.
Why sparse generalises better on calibration.             Analysis result (6.7 % training share, +0.23 abso-
The mechanism in §6.3 is interpretable. Under the         lute gain) and the +52 percentage-point gain on
dense reward, the partial-credit term α · (shyp /nhyp )   MATH-500 under unchanged prompting are the
guarantees a positive reward whenever the policy          strongest evidence for this reading. The literature
satisfies at least one remaining hypothesis, even         on the “hallucination tax” (Song et al., 2025) pre-
when it asserts the (false) conclusion is true. This      dicts that standard imitation-only training degrades
actively trains the policy to always emit a coun-         calibration; the present results suggest that verifier-
terexample expression: doing so on a false conjec-        grounded RL with an outcome-only reward avoids
ture yields up to α + γ = 0.35 and never less than        that pathology and installs a transferable inverse-
γ = 0.10 when the witness parses, much better             reasoning skill.
than the −0.20 of abstention. Sparse rewards re-
move this incentive: the policy is rewarded only for      8   Conclusion
correctly negating the conclusion, and abstention
                                                          We have presented S YM CE, a deterministic, large-
is no worse than a wrong witness. The behavioural
                                                          scale dataset and verification environment for coun-
consequence is the higher abstention rate on the
                                                          terexample generation on undergraduate algebra
in-distribution test set (10 % vs 2 %) and, crucially,
                                                          and real analysis, and used it to identify and ex-
the preservation of abstention as a viable action
                                                          plain an imitation trap: supervised fine-tuning on
when the policy is shown a true theorem at test
                                                          counterexample-only data collapses the policy’s
time. The dense reward does not preserve this; the
                                                          ability to recognise true theorems, and verifier-
partial-credit term is in tension with calibration.
                                                          grounded reinforcement learning with a sparse
   We conjecture this generalises to other settings
                                                          outcome-only reward repairs and exceeds the orig-
where (i) the reward signal already returns a struc-
                                                          inal calibration where a partial-credit dense re-
tured boolean tuple, and (ii) the failure mode of
                                                          ward does not. The collapse reproduces in ev-
interest is the policy answering when it should ab-
                                                          ery training seed and on a second model family.
stain, rather than failing to produce well-formed
                                                          A Qwen3-4B model trained this way exceeds ev-
output. Whether this conjecture survives at scale is
                                                          ery 7B open-weights math specialist we evaluated
left to future work.
                                                          on the in-domain benchmark, remains competitive
Deterministic verification beats LLM-as-judge             with frontier commercial APIs, and transfers un-
where the verification problem is decidable.              der unchanged prompting to GSM8K, MATH-500
The verifier substrate is reproducible, fast (median      and MMLU-college-math, evidence that counterex-
132 ms), audited end-to-end at 97.7 % decision ac-        ample reasoning is a fundamental, under-installed
curacy over 177 human-checked verifier decisions,         skill rather than a narrow specialisation. We release
and immune to judge-model drift. We would add             the dataset, the verifier modules, the human-audit
that this shifts, rather than removes, the dependence     annotations, the witness-schema generator, and the
on a language model: an LLM-as-judge protocol             full evaluation pipeline, and we view extension to
incurs stochastic error at every evaluation, whereas      topology and higher-order logic, broader mutation
construction-time LLM dependence is frozen once           strategies, larger scales and alternative RL algo-
and can be audited once, which is what §3.5 does.         rithms, and integration with a Lean back-end as the
Its scope is bounded by what is decidable in Python       natural next steps.
with SymPy/Z3; for the algebraic subdomains in
this paper this is sufficient. Where the verification     Limitations
problem is decidable a deterministic verifier is the
                                                          Scale, parameterisation and RL algorithm. Ev-
stronger choice; LLM-judging, as used by COUN-
                                                          ery trained variant here is a 4B model adapted
TERMATH (Li et al., 2025), remains necessary for
                                                          with LoRA and optimised with GRPO, so three
domains that fall outside it.
                                                          axes remain untested: substantially larger scales,
Counterexample reasoning as a fundamental ca-             full-parameter fine-tuning, and alternative RL algo-
pability. The cross-domain consistency of §6.4            rithms. Full fine-tuning with GRPO rollouts was
and the out-of-domain transfer of §6.5 together sup-      not feasible on our compute (a single RTX 5090,
port a stronger reading of the contribution: training     32 GB), so we cannot separate properties of the
on structured falsification improves general math-        environment from properties of GRPO. Two obser-
ematical reasoning, not only disproof. The Real           vations mitigate the concern that the findings are
adapter artefacts: they replicate across four seeds    eration, in which several teachers must agree on
and a second model family under the same adapter       a verifier before it enters the corpus, is a valuable
configuration, including an exact 0.00 collapse in     extension we have not implemented.
all six SFT runs, and the mechanism we identify
operates at the level of the optimisation objective    Ethics and Risk Considerations
rather than the parameterisation. The scaling ques-    The work studies counterexample generation for
tion is the most important one we leave open.          undergraduate-level algebraic and real-analysis the-
Verifier scope. Our substrate is Python with           orems, using LLM-generated Python verifiers and
SymPy and Z3. This suffices for the six subdo-         a hypothesis-dropping mutation pipeline. The arte-
mains we evaluate but not for topology, general        facts produced (S YM CE, a dataset of false math-
higher-order logic, or claims whose verification re-   ematical conjectures, per-theorem verifier mod-
duces to undecidable fragments. A Lean backend,        ules, and a small 4B model specialised for fal-
or continuous-FOL extensions for metric spaces, is     sifying such conjectures) do not present obvious
a natural follow-up.                                   dual-use risks beyond those general to research on
                                                       LLM mathematical reasoning. Per-artefact licences
Audit scope. The 177-decision study of §3.5 was        are listed in Appendix I. The dataset contains no
annotated by a single author, so we report no inter-   human-derived data, no personal information, and
annotator agreement, and 177 decisions bound the       no naturally occurring text from which PII could
pipeline’s error rate only coarsely. A larger, inde-   be derived; the trained models are released for re-
pendently annotated audit would support stronger       search use and are not deployed in any user-facing
claims about the full verifier collection.             setting; and the methodology does not enable capa-
                                                       bilities that meaningfully extend beyond existing
Mutation strategy and scope of the resource
                                                       open-source mathematical reasoning models.
claim. We mutate only by dropping a single hy-
pothesis. This was deliberate: it gives every false    Acknowledgements
conjecture a known, attributable cause of falsity,
which is what makes the per-hypothesis boolean         We gratefully acknowledge Sukai Labs and its
interface and the outcome taxonomy possible. Con-      CEO, Ahmed Sedouki, for believing in this re-
clusion mutation, multi-hypothesis dropping and        search and providing access to the NVIDIA
AST-level mutation (Wu et al., 2024) would enrich      RTX 5090 (32 GB) GPU on which all training and
the distribution but complicate attribution, and re-   evaluation runs in this paper were performed. We
main unexplored. S YM CE should accordingly be         also thank the ACL ARR reviewers and the action
read as a deterministic falsification environment      editor, whose requests for multi-seed replication, a
rather than a benchmark spanning the full space of     second model family, and a stronger verifier audit
mathematical fallacies.                                shaped the evidence reported here.

No COUNTERMATH cross-evaluation. Cross-
evaluation on COUNTERMATH (Li et al., 2025)            References
would compare our models against the published         Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
frontier on a benchmark with broader domain cov-        Henrique Ponde de Oliveira Pinto, Jared Kaplan,
erage. The authors do not release the test labels or    Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
                                                        Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
evaluation scripts, and predicted outputs must be       Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
submitted for LLM-judged scoring on their side,         Mishkin, Brooke Chan, Scott Gray, and 39 others.
which diverges from this paper’s focus on open,         2021. Evaluating large language models trained on
deterministic verification. We leave this for future    code. arXiv preprint arXiv:2107.03374.
work.                                                  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
                                                         Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
Teacher model dependence. The verifiers are              Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
generated by a single teacher model (Gemini              Nakano, Christopher Hesse, and John Schulman.
3.1 Pro) and the witness schemas by a second             2021. Training verifiers to solve math word prob-
(DeepSeek). Although the audit found no verifier-        lems. arXiv preprint arXiv:2110.14168.
logic errors, the pipeline retains a dependence on     Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang,
teacher output quality. Multi-model consensus gen-       Yuchen Zhang, Jiacheng Chen, Wendi Li, Bingxiang
  He, Yuchen Fan, Tianyu Yu, Qixin Xu, Weize Chen,         Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri
  Jiarui Yuan, Huayu Chen, Kaiyan Zhang, Xingtai             Edwards, Bowen Baker, Teddy Lee, Jan Leike, John
  Lv, Shuo Wang, Yuan Yao, Xu Han, and 6 others.             Schulman, Ilya Sutskever, and Karl Cobbe. 2024.
  2025. Process reinforcement through implicit re-           Let’s verify step by step. In International Conference
  wards. arXiv preprint arXiv:2502.01456.                    on Learning Representations.

Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:           Aaron Meurer, Christopher P. Smith, Mateusz Pa-
  An efficient smt solver. In Tools and Algorithms           procki, Ondřej Čertík, Sergey B. Kirpichev, Matthew
  for the Construction and Analysis of Systems: 14th         Rocklin, AMiT Kumar, Sergiu Ivanov, Jason K.
  International Conference, TACAS 2008, pages 337–           Moore, Sartaj Singh, Thilina Rathnayake, Sean Vig,
  340. Springer.                                             Brian E. Granger, Richard P. Muller, Francesco
                                                             Bonazzi, Harsh Gupta, Shivam Vats, Fredrik Johans-
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,           son, Fabian Pedregosa, and 8 others. 2017. Sympy:
  Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang,             symbolic computing in python. PeerJ Computer Sci-
  Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai Yu,           ence, 3:e103.
  Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhu-
  oshu Li, Ziyi Gao, Aixin Liu, and 175 others. 2025.      Jialin Ouyang. 2025. Treecut: A synthetic unanswer-
  Deepseek-r1 incentivizes reasoning in llms through          able math word problem dataset for llm hallucination
  reinforcement learning. Nature, 645(8081):633–638.          evaluation. arXiv preprint arXiv:2502.13442.
                                                           Qwen Team. 2025. Qwen3 technical report. Preprint,
Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou,
                                                            arXiv:2505.09388.
  Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
  2021a. Measuring massive multitask language under-       Rulin Shao, Shuyue Li, Rui Xin, Scott Geng, Yiping
  standing. In International Conference on Learning          Wang, Sewoong Oh, Simon Du, Nathan Lambert, Se-
  Representations.                                           won Min, Ranjay Krishna, Yulia Tsvetkov, Hannaneh
                                                             Hajishirzi, Pang Koh, and Luke Zettlemoyer. 2025.
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul           Spurious rewards: Rethinking training signals in rlvr.
  Arora, Steven Basart, Eric Tang, Dawn Song, and            Preprint, arXiv:2506.10947.
  Jacob Steinhardt. 2021b. Measuring mathematical
  problem solving with the math dataset. NeurIPS.          Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
                                                             Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan            Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.
  Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and            Deepseekmath: Pushing the limits of mathematical
  Weizhu Chen. 2022. LoRA: Low-rank adaptation of            reasoning in open language models. arXiv preprint
  large language models. In International Conference         arXiv:2402.03300.
  on Learning Representations.
                                                           Shiven Sinha, Shashwat Goel, Ponnurangam Ku-
Ryo Kamoi, Yusen Zhang, Nan Zhang, Sarkar                    maraguru, Jonas Geiping, Matthias Bethge, and
  Snigdha Sarathi Das, Ranran Haoran Zhang, Wen-             Ameya Prabhu. 2025. Can language models falsify?
  peng Yin, and Rui Zhang. 2026. Efficient prm train-        evaluating algorithmic reasoning with counterexam-
  ing data synthesis via formal verification. In Find-       ple creation. Preprint, arXiv:2502.19414.
  ings of the Association for Computational Linguistics:
  ACL 2026.                                                Linxin Song, Taiwei Shi, and Jieyu Zhao. 2025. The
                                                             hallucination tax of reinforcement finetuning. arXiv
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying                 preprint arXiv:2505.13988.
 Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gon-
 zalez, Hao Zhang, and Ion Stoica. 2023. Efficient         Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai
 memory management for large language model serv-            Dai, Yifei Li, Deli Chen, Y. Wu, and Zhifang Sui.
 ing with PagedAttention. In Proceedings of the 29th         2023. Math-shepherd: Verify and reinforce llms step-
 Symposium on Operating Systems Principles.                  by-step in mathematical reasoning. arXiv preprint
                                                             arXiv:2312.08935.
Yinghui Li, Jiayi Kuang, Haojing Huang, Zhikun Xu,         Shaonan Wu, Shuai Lu, Yeyun Gong, Nan Duan, and
  Xinnian Liang, Yi Yu, Wenlian Lu, Yangning Li, Xi-         Ping Wei. 2024. Alchemy: Amplifying theorem-
  aoyu Tan, Chao Qu, Ying Shen, Hai-Tao Zheng, and           proving capability through symbolic mutation. arXiv
  Philip S. Yu. 2025. One example shown, many con-           preprint arXiv:2410.15748.
  cepts known!: counterexample-driven conceptual rea-
  soning in mathematical llms. In Proceedings of the       Wei Xiong, Hanning Zhang, Chenlu Ye, Lichang Chen,
  42nd International Conference on Machine Learning,         Nan Jiang, and Tong Zhang. 2025. Self-rewarding
  ICML’25. JMLR.org.                                         correction for mathematical reasoning. Preprint,
                                                             arXiv:2502.19613.
Zenan Li, Zhaoyu Li, Kaiyu Yang, Xiaoxing Ma, and
  Zhendong Su. 2026. Learning to disprove: Formal          An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao,
  counterexample generation with large language mod-         Bowen Yu, Chengpeng Li, Dayiheng Liu, Jian-
  els. arXiv preprint arXiv:2603.19514.                      hong Tu, Jingren Zhou, Junyang Lin, Keming Lu,
          Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang                                                                             Supervised fine-tuning (SFT)
          Ren, and Zhenru Zhang. 2024. Qwen2.5-math tech-                                                                            Base model                          unsloth/Qwen3-4B
          nical report: Toward mathematical expert model via                                                                         Chat template                                    qwen-3
          self-improvement. arXiv preprint arXiv:2409.12122.                                                                         Max sequence length                                 2048
                                                                                                                                     Precision                                       bfloat16
Jiarui Yao, Ruida Wang, Hao Bai, and Tong Zhang.                                                                                     LoRA rank r / scale α                             16 / 16
   2026. Future-kl regularized grpo: Process-level                                                                                   LoRA dropout                                            0
   credit assignment from f -divergence regularization.                                                                              LoRA targets                            all attn. + MLP
   Preprint, arXiv:2601.10201.                                                                                                       Gradient checkpointing                            unsloth
                                                                                                                                     Per-device batch                                       16
Lifan Yuan, Ganqu Cui, Hanbin Wang, Ning Ding,                                                                                       Gradient accumulation                                   2
  Xingyao Wang, Jia Deng, Boji Shan, Huimin Chen,                                                                                    Effective batch                                        32
   Ruobing Xie, Yankai Lin, Zhenghao Liu, Bowen                                                                                      Epochs                                                  3
                                                                                                                                     Learning rate                                  2 × 10−4
   Zhou, Hao Peng, Zhiyuan Liu, and Maosong Sun.
                                                                                                                                     LR schedule / warmup                       cosine / 0.05
   2024. Advancing llm reasoning generalists with pref-                                                                              Optimiser                                       AdamW
   erence trees. Preprint, arXiv:2404.02078.                                                                                         Weight decay                                          0.0
                                                                                                                                     Max grad norm                                         1.0
Xiang Yue, Tuney Zheng, Ge Zhang, and Wenhu Chen.                                                                                    Eval-loss split fraction                             0.05
  2024. Mammoth2: Scaling instructions from the web.                                                                                 Seed                                                   42
  arXiv preprint arXiv:2405.03548.
                                                                                                                                     RLVR (GRPO from SFT adapter)

A                   Full Hyperparameters                                                                                             Algorithm                       TRL GRPOTrainer
                                                                                                                                     Rollout backend              vLLM (gpu_util = 0.5)
                                                                                                                                     Max LoRA rank                                    16
Table 6 lists the exact hyperparameters used                                                                                         G (generations / prompt)                          4
for the SFT and RLVR runs reported in                                                                                                Max prompt / completion tok.           768 / 1024
this paper.      The reference-seed runs were                                                                                        Temperature                                     1.0
                                                                                                                                     Top-p                                           1.0
launched from configs/full_run.yaml (SFT),                                                                                           Per-device batch                                  4
configs/full_run_dense_test.yaml (dense                                                                                              Gradient accumulation                             8
RLVR) and configs/full_run_sparse.yaml                                                                                               Effective batch                                  32
                                                                                                                                     Epochs                                            4
(sparse RLVR); the additional seeds are in                                                                                           Total steps                               ≈ 1,752
configs/seeds/. Each run directory also carries                                                                                      Learning rate                           5 × 10−6
the fully resolved config.json it was launched                                                                                       LR schedule / warmup                 constant / 0.1
                                                                                                                                     PPO clip ε                                      0.2
with, which is the authoritative record.                                                                                             KL coefficient βKL                            0.02
                                                                                                                                     Max grad norm                                   0.5
                           RLVR training stability — 4 epochs over 3506 prompts (G=4, T=1.0)
                      Mean reward                              KL to SFT ref                                  Policy loss
                                                                                                                                     Oracle timeout                                  8s
          0.4
                                                  2.00
                                                                                             0.08                                    Reward-pool workers                               4
          0.3
                                                  1.75
                                                                                             0.07                                    Seed                                             42
          0.2                                     1.50                                       0.06
reward




                                                                                                                                     Oracle reward weights (Eq. 1)
                                                                                      loss




          0.1                                     1.25
                                             KL




                                                                                             0.05
          0.0                                     1.00

         −0.1                                     0.75
                                                                                             0.04
                                                                                                                                     Dense (α, β, γ, δ, ε) = (0.25, 0.65, 0.10, 0.30, 1.00)
         −0.2
                                   RLVR-dense
                                   RLVR-sparse
                                                  0.50                                       0.03
                                                                                                                                     Sparse (α, β, γ, δ, ε) = (0, 1, 0, 0, 1)
                                                  0.25
                0    500    1000      1500               0   500    1000       1500                 0   500       1000      1500
                           Step                                    Step                                          Step

                                                                                                                                   Table 6: Hyperparameters used for SFT and both RLVR
Figure 4: Per-step training curves for the dense and                                                                               variants, as recorded by the reference-seed runs. The
sparse RLVR runs at the reference seed (≈ 1,752 steps                                                                              one setting that is not uniform is the SFT epoch count:
over four epochs of 3,506 prompts). Mean reward rises                                                                              seed 42 uses 3 epochs, and seeds 19, 31 and 64 use
monotonically and crosses zero by step ∼240 for both                                                                               2, after we checked that the two schedules performed
variants; KL to the SFT reference decays smoothly; loss                                                                            equivalently and preferred the shorter one. SFT wall-
is bounded and oscillatory but stable.                                                                                             clock on a single RTX 5090 32 GB is under five minutes;
                                                                                                                                   each RLVR run is approximately nine hours.
   Figure 4 shows the per-step training curves for
both RLVR runs. The reward trajectory rises from                                                                                   B    Human Audit of Verifier Decisions
approximately −0.20 at step 80 to +0.40 (dense) /
+0.30 (sparse) at convergence; the KL penalty to                                                                                   We sampled 177 model-generated witnesses from
the SFT reference declines from ∼ 2.0 to ∼ 0.5 as                                                                                  the held-out test split, drawn across four seeds and
the policy explores away from imitation; the policy                                                                                three training configurations (dense 85, sparse 61,
loss is bounded and oscillatory but does not diverge.                                                                              SFT 31) and all six subdomains, and split by the
Both runs complete the full four epochs without                                                                                    verifier’s own verdict: 101 that it accepted and 76
any restart, gradient explosion or reward collapse.                                                                                that it rejected. An author with graduate-level train-
ing in the relevant areas judged, independently of         of true or false anywhere in the completion, taking
the verifier, whether each witness is genuinely a          the last one. On completions that exhaust the gener-
valid counterexample. Table 7 reports the composi-         ation budget mid-reasoning this converts unfinished
tion.                                                      chains of thought into apparent verdicts. The effect
                                                           is confined almost entirely to the untrained base
      Domain           accepted   rejected   total         model, which reasons at length and frequently fails
      GroupTheory            31        27      58          to commit within budget; the trained models emit
      RingTheory             20        15      35
      NumberTheory           23         8      31          the required format and are barely affected.
      LinearAlgebra          11        11      22
      FieldTheory             8         8      16                                 S YM CE-prompt     truth-classify
      RealAnalysis            8         7      15
                                                            Model               strict permissive strict permissive
      Total                 101        76    177
                                                            Qwen3-4B base       0.27      0.86     0.36      0.71
                                                             + SFT              0.00      0.00     0.21      0.23
Table 7: Composition of the human audit, split by the        + RLVR (dense)     0.34      0.37     0.73      0.76
verifier’s verdict. Decision accuracy: 99/101 accepted       + RLVR (sparse)    0.65      0.69     0.84      0.84
witnesses confirmed valid, 74/76 rejected witnesses con-
firmed invalid, 173/177 = 97.7 % overall. Annotations      Table 8: Theorem-truth probe under both answer-
are released at human_eval/.                               extraction rules (reference seed 42, n=347). “Permis-
                                                           sive” reproduces what the original evaluation harness
                                                           recorded; the paper reports the strict column throughout.
The four disputed decisions. Two verifier ac-
ceptances were judged invalid: one witness sat-                Two properties of the finding are invariant to the
isfied the remaining hypotheses without actually           choice. Counterexample-only SFT scores exactly
negating the conclusion, and one supplied a mal-           0.00 on the S YM CE-prompt probe under both rules
formed field construction. Two rejections were             and in every seed, and the sparse-over-dense gap
judged wrong, and in neither case is the veri-             on that probe is 0.31 under both. What the choice
fier module at fault. In bw_seq_rn__h3 the emit-           does affect is the base model’s apparent calibration,
ted witness was valid but the witness-schema de-           and hence whether RLVR is described as exceeding
scription showed a bare Matrix where the veri-             it.
fier’s namespace requires sympy.Matrix; the fault              We validated that the strict truth-classify rule
is in the schema text, not the verifier logic. In          does not under-credit models that do answer.
word_problem_direct_product the conjecture                 Across every cell in our corpus, each response
remained true after the hypothesis drop, and the           the rule records as stating no verdict is an unfin-
model correctly emitted NONE; the verifier “re-            ished completion; no completion that terminated
jected” only because a counterexample was ex-              normally is scored as having failed to answer. The
pected where none exists. This is the single case in       accepted answer frames were derived by inspect-
177 that we attribute to hypothesis-drop label noise,      ing the completions that the narrow Answer: TRUE
and the single case attributable to schema quality.        pattern alone would have missed, and cover the
   Among the confirmed-correct rejections the an-          phrasings both model families actually produce, in-
notator noted several where the mathematics was            cluding \boxed{TRUE} and “the claim is TRUE”.
right and only the Python namespace or API us-
age was wrong, such as Matrix for sympy.Matrix;            D    Per-Seed Results
only 9 of the 76 rejections carry free-text annota-
tions, so we cannot estimate a rate.                       Table 9 gives the individual seed values behind the
                                                           means of Table 5. The base model is training-seed
C    Answer Extraction and the Scoring                     independent and is evaluated once per suite.
     Correction
                                                           E    Theorem-Truth Robustness: Seen vs
§5.2 adopts strict answer-extraction rules for the              Unseen Subsets
two calibration probes. This appendix reports both
readings so the effect is auditable.                       The 347-item theorem-truth probe partitions into
   The evaluation harness that produced our raw            true theorems whose mutated form appeared in
records used, as a last resort when no answer frame        the RLVR training corpus (extra_stratified,
was present, a parser matching any bare occurrence         n=150) and those whose mutated form did not
 Metric                Arm       42       19      31    64     A false conjecture from the counterexample
                                                                                                       √           bench-
                                                                                               √
                                                               mark. Minimal polynomial of a + b (Field Theory):
                       SFT    0.348 0.358 0.323 0.338          the original theorem requires that a, b and ab are all non-
 S YM CE Pass@1        dense 0.502 0.478 0.458 0.502           squares in the base field. The benchmark removes the
                       sparse 0.497 0.438 0.463 0.453          assumption that a is not a square.
                       SFT    0.637 0.617 0.592 0.632          RLVR-dense witness. (F, a, b) = (Q, 1, 2). Since 1 is a
 S YM CE Pass@8        dense 0.677 0.632 0.672 0.662           square in Q, the claimed  quartic is no longer the minimal
                                                                                   √
                       sparse 0.672 0.622 0.632 0.637          polynomial of 1 + 2:
                      SFT    0.000 0.000 0.000 0.000
 Truth S YM CE-prompt dense 0.343 0.294 0.308 0.386                                         x2 − 2x − 1 ̸= x4 − 6x2 + 1.
                      sparse 0.654 0.715 0.660 0.608
                                                               RLVR-dense finds this compact counterexample; RLVR-
                       SFT    0.210 0.101 0.173 0.161          sparse abstains and emits NONE.
 Truth-classify        dense 0.729 0.801 0.594 0.700
                       sparse 0.839 0.813 0.787 0.550
                                                             Figure 5: A sparse-reward failure: improved calibration
Table 9: Per-seed values. The sparse-over-dense gap          on true theorems costs false abstentions on genuinely
on the S YM CE-prompt probe is positive in every seed        false conjectures. We discuss the trade-off in §7.
(+0.31, +0.42, +0.35, +0.22); on truth-classify it is
not (+0.11, +0.01, +0.19, −0.15), which is why §6.6
restricts the claim to the S YM CE-prompt probe.             G          Per-Model Baseline Breakdowns
                                                             Table 11 reports the per-model counterexample-
(from_test_set, n=197). Because both subsets                 benchmark scores for the five 7B open-weights
are drawn from the same theorem source, compar-              math specialists summarised in the body. Table 12
ing them bounds how much of the trained models’              reports the same for the six commercial-API fron-
calibration is memorisation.                                 tier models that contribute to the “frontier API
                                                             range” band in Table 2. We additionally report the
      Model             unseen    seen           ∆           Qwen2.5-Math-1.5B base in Table 11 as a smaller
      Qwen3-4B base     0.244     0.307        +0.063        comparison point. Figure 6 shows all comparators
       + SFT            0.000     0.000         0.000        together.
       + RLVR dense     0.274     0.433        +0.159
       + RLVR sparse    0.614     0.707        +0.092                                              Counterexample benchmark — our 4B method vs open-weights 7B math specialists

                                                                   Qwen3-4B base                                                 0.30



Table 10: S YM CE-prompt Pass@1 by subset (greedy,                          + SFT

                                                                   + RLVR (dense)
                                                                                                                                        0.35

                                                                                                                                                         0.50


strict scoring, reference seed 42). ∆ = seen − unseen.             + RLVR (sparse)                                                                      0.49


                                                                  MAmmoTH2-7B+       0.00


                                                                      Abel-7B-002           0.04


                                                             DeepSeek-Math-7B-RL                       0.10


   Two readings. The base model shows a small                Qwen2.5-Math-7B-Instr                                 0.20


                                                                 Eurus-2-7B-PRIME                                               0.30                               frontier commercial APIs

positive ∆ (+0.06), which sets the scale of any                                  0.0                0.1          0.2          0.3              0.4     0.5
                                                                                                                                                                   (range 0.42–0.58, n=6)

                                                                                                                                                                    0.6              0.7
                                                                                                                       Counterexample Pass@1 (greedy, n=201)
residual difficulty difference between the subsets
rather than of memorisation, since the base saw nei-         Figure 6: Counterexample Pass@1 (greedy) for all com-
ther. The trained models show larger gaps (+0.09             parators evaluated. Our trained 4B models are in colour;
to +0.16), consistent with some memorisation of              open-weights 7B specialists are in grey; the shaded yel-
theorem identity. Crucially, the sparse-over-dense           low band shows the range across six frontier commercial
gap on the unseen subset alone is 0.614 − 0.274 =            APIs.
+0.34, larger than on the full probe, so the central
dissociation of this paper is not a memorisation
artefact.                                                    H          Witness-Schema Generator and
                                                                        Example Schemas
F    Qualitative Examples
                                                             The witness-schema stage (§3.2) is implemented
Figure 1 shows the imitation trap on a true theorem:         in tools/inject_witness_schema.py. The tool
the SFT model emits a syntactically valid, well-             iterates over verifier modules and queries a teacher
formatted counterexample expression that none the            model (DeepSeek via the OpenAI-compatible API
less fails the negated-conclusion check, which is a          client) with the verifier source code and the canoni-
hyp-only failure in the taxonomy of §6.3. Figure 5           cal witness expression, asking for a single-sentence
below shows the symmetric failure mode of the                Python-shape description of an acceptable witness,
sparse reward.                                               with a concrete example.
  Model                                   Pass@1 (greedy)            Pass@1 (sampled)            Pass@3 (sampled)            Pass@8 (sampled)
  Eurus-2-7B-PRIME                          0.299 [0.24, 0.36]          0.292 [0.24, 0.34]          0.458 [0.40, 0.52]          0.567 [0.50, 0.64]
  Qwen2.5-Math-7B-Instruct                  0.199 [0.14, 0.25]          0.063 [0.05, 0.08]          0.155 [0.12, 0.19]          0.289 [0.23, 0.35]
  DeepSeek-Math-7B-RL                       0.105 [0.06, 0.15]          0.072 [0.05, 0.09]          0.171 [0.13, 0.21]          0.308 [0.25, 0.37]
  Abel-7B-002                               0.045 [0.02, 0.07]          0.052 [0.04, 0.07]          0.124 [0.09, 0.16]          0.224 [0.17, 0.28]
  MAmmoTH2-7B-Plus                          0.000 [0.00, 0.00]          0.040 [0.03, 0.05]          0.106 [0.08, 0.14]          0.219 [0.16, 0.28]
  Qwen2.5-Math-1.5B (smaller ref.)          0.010 [0.00, 0.02]          0.017 [0.01, 0.03]          0.045 [0.03, 0.07]          0.095 [0.05, 0.13]

Table 11: Open-weights baselines on the counterexample benchmark (n=201). All numbers Pass@k with
95 % bootstrap CIs over problem ids. Sampled decoding uses n = 8, temperature 0.7. Regenerated by
build_camera_ready_tables.py.

      Model                         Pass@1 (greedy)              Pass@1 (sampled)            Pass@3 (sampled)            Pass@8 (sampled)
      Gemini-3.1-Flash-Lite           0.577 [0.51, 0.64]          0.565 [0.50, 0.63]          0.638 [0.57, 0.70]          0.687 [0.62, 0.75]
      Gemini-3.5-Flash                0.493 [0.42, 0.56]               —                           —                           —
      Gemini-3-Flash-Preview          0.468 [0.40, 0.54]          0.489 [0.44, 0.53]          0.708 [0.65, 0.76]          0.771 [0.71, 0.83]
      Gemini-3.1-Pro                  0.433 [0.36, 0.50]               —                           —                           —
      DeepSeek-Pro                    0.428 [0.36, 0.49]          0.437 [0.38, 0.49]          0.551 [0.49, 0.61]          0.622 [0.55, 0.69]
      DeepSeek-Flash                  0.423 [0.35, 0.49]          0.432 [0.38, 0.49]          0.562 [0.50, 0.62]          0.637 [0.57, 0.70]

Table 12: Frontier commercial APIs on the counterexample benchmark (n=201). Dashes indicate sampled passes
that were not run because token-budget constraints prevented an 8-sample run within the budget. Regenerated by
build_camera_ready_tables.py.


Representative schemas (one per subdomain).                                I     Artefact Licences
     GroupTheory.            “Python    tuple                             All third-party artefacts are used for non-
     (G, H) where both G and H are                                        commercial research consistent with their release
     sympy.combinatorics.PermutationGroup
     objects constructed via SymPy group                                  terms. Models: Qwen3-4B and Qwen2.5-Math
     constructors  (e.g.,  SymmetricGroup(n),                             (Apache 2.0), Gemma-3-4B (Gemma Terms of
     AlternatingGroup(n),   DihedralGroup(n),                             Use), DeepSeek-Math-7B-RL (DeepSeek Licence),
     CyclicGroup(n)).       Example syntax:
     (SymmetricGroup(3), DihedralGroup(4)).”                              Eurus-2-7B-PRIME, MAmmoTH2-7B-Plus and
                                                                          Abel-7B-002 (Apache 2.0). Libraries: vLLM, TRL,
     RingTheory.    “An RModule instance with                             PEFT/LoRA, SymPy and Z3 (Apache 2.0 or MIT).
     attributes:     ring   (CommutativeRing)                             Benchmarks: GSM8K (MIT), MATH-500 (MIT),
     and generators_count (int).     Example:
     RModule(Z, 2).”                                                      MMLU (MIT), AIME-2024 (MIT). Commercial
                                                                          APIs were accessed under their providers’ terms of
     FieldTheory. “A SymPy Domain object represent-                       service.
     ing an integral domain that is not a field. Example:                    S YM CE itself is released with the code under the
     ZZ from SymPy.”
                                                                          MIT Licence and the corpus, verifier modules and
                                                                          human-audit annotations under CC BY 4.0. The
     LinearAlgebra. “A SymPy Matrix object
     (square, non-real). Example: Matrix([[0, 1],                         corpus consists exclusively of formal mathematical
     [-1, 0]]).”                                                          statements and their hypothesis-dropped mutations;
                                                                          it contains no human-derived text, no personal in-
     RealAnalysis. “Python tuple (f, a, b, p) where                       formation, and no content from which personally
     f is a SymPy expression (or string) in terms of
     Symbol(’x’), a and b are real numbers (a < b),                       identifying information could be derived.
     p is a real number.”
                                                                           J     Eval-Suite Configuration and
     NumberTheory.          “A Python int or                                     Reproducibility
     sympy.Integer (single integer). Example: 5.”
                                                                          All evaluation in the main paper is orchestrated
   The schemas are short (10–40 tokens) and add a                         by the multi-model multi-benchmark suite runner
small overhead to the user prompt (median schema                           python -m training.eval.run_suite –config configs/
length is well below the SFT user-prompt median                            eval/full_eval.yaml, which iterates the cartesian
of 120 tokens reported in the dataset stats).                              product {model} × {benchmark} × {prompt-style}
× {greedy, sampled} and writes one JSON per
cell. Each per-cell JSON contains a summary
block (Pass@k, by-domain, and (where appli-
cable) subset metrics) and a per_record block
(one record per test problem with all sample-
level fields: completion, extracted, correct,
reason, format_ok, parse_ok, is_none, oracle
timing, etc.).
Reproducing the paper from the released arte-
facts.

  1. Every table.
     python -m paper_preparation.scripts.build_
     camera_ready_tables
     regenerates all numbers in Tables 2, 3, 4, 5, 7,
     8, 9, 10, 11 and 12 directly from the raw
     per-record evaluation outputs, applying the
     answer-extraction rules of §5.2. It is the
     single source of truth for this paper.
  2. Bootstrap CIs.
     python -m
     paper_preparation.scripts.bootstrap_cis
     regenerates bootstrap_cis.csv and
     bootstrap_deltas.csv.

  3. Reason distribution (Fig. 2).
     python -m
     paper_preparation.scripts.eval_reason_dist
     regenerates the reason-counts table.
  4. All figures.
     python -m
     paper_preparation.scripts.make_plots –all
     regenerates Figures 2, 3, 4, and 6 from the
     released CSVs.

Dataset fingerprints. Each suite run writes a
dataset_fingerprint.json file containing the
SHA-256 hash and line count of every input JSONL
used (the test set, the theorem-truth probe, and the
external-benchmark sources). These fingerprints
are sufficient to verify that all numbers in this paper
were produced from the released splits.
Seeds. Four training seeds (42, 19, 31 and 64)
were used; the split seed is fixed at 42 throughout.
The configs are sufficient to reproduce all training
runs deterministically up to GPU non-determinism
in the rollout backend (vLLM tensor-parallel sam-
pling); the reported test-set numbers are robust to
this residual non-determinism within the reported
95 % bootstrap CIs.
