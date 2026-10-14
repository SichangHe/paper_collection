                                         Formalize Once, Edit the Rest: Efficient Lean-Based Answer Selection for
                                                                    Math Reasoning

                                                                               Ji Feng and Zhouxing Shi
                                                                            University of California, Riverside
                                                                          {jfeng080, zhouxing.shi}@ucr.edu



                                                              Abstract                          and selecting among them is an instance of test-
                                                                                                time scaling and has driven much of the recent
                                             With large language models (LLMs) increas-
arXiv:2606.15972v1 [cs.CL] 14 Jun 2026




                                                                                                progress on mathematical reasoning (Snell et al.,
                                             ingly applied to mathematical reasoning, for-      2025; Brown et al., 2024).
                                             mal proof assistants such as Lean can be lever-
                                                                                                   A central challenge, however, lies in the selec-
                                             aged to verify reasoning outputs with machine-
                                             checkable rigor, enabling use cases such as        tion step—choosing the correct answer without
                                             answer selection in test-time scaling with K       access to a ground-truth label. The dominant ap-
                                             sampled candidate answers. However, employ-        proaches are majority voting (Wang et al., 2023)
                                             ing Lean requires that LLM outputs, originally     and best-of-N selection with learned reward mod-
                                             in natural language, first be formalized. Exist-   els (Cobbe et al., 2021; Lightman et al., 2024),
                                             ing Lean-based answer-selection work uses an       the former relying on consensus within the candi-
                                             autoformalization model to generate a formal
                                                                                                date set and the latter on a scalar score. However,
                                             statement in Lean for each candidate answer
                                             independently, incurring a significant computa-
                                                                                                majority voting is a heuristic and fails when the cor-
                                             tional cost. We propose BASE, a base-and-edit      rect answer is in the minority; reward models are
                                             pipeline that formalizes a single base candi-      typically black boxes. More fundamentally, both
                                             date per problem and derives the remaining         provide no formal guarantee of correctness.
                                             K−1 statements by editing the answer expres-          To address this, a recent line of work leverages
                                             sion in place. To facilitate this, we train a      a formal verifier (Zhou et al., 2024; Yao et al.,
                                             rewriter model L EAN S CRIBE to localize the       2025). For each candidate answer, the problem
                                             answer in the base formalization and generate
                                                                                                and the answer are jointly formalized by an LLM
                                             a reusable edit function for the other K − 1
                                             candidates. BASE simultaneously improves           known as an autoformalizer (Wang et al., 2025)
                                             selection accuracy and reduces formalization       into a Lean 4 (Moura and Ullrich, 2021) theorem
                                             cost—a Pareto improvement that holds on all        statement asserting that the candidate is the correct
                                             12 (dataset, solver) configurations across four    answer to the problem; a prover then attempts to
                                             benchmarks and three solvers, cutting auto-        prove this statement (Ren et al., 2025; Lin et al.,
                                             formalizer calls by about 5× at K=8, with          2025b; Liu et al., 2026), with the proof verified
                                             the reduction expected to become larger as K
                                                                                                by the Lean 4 compiler. The highest-ranked prov-
                                             grows. Code is available at https://github.
                                             com/ucr-rai/base-and-edit.
                                                                                                able candidate is then selected. This paradigm is
                                                                                                grounded in formal mathematics, as a statement
                                         1   Introduction                                       with a verified proof is guaranteed to be correct.
                                                                                                   This reliability, however, introduces a significant
                                         As large language models (LLMs) tackle increas-        computational cost — to verify K candidates for
                                         ingly hard mathematical reasoning tasks, they can      a single problem, the autoformalization model is
                                         often generate distinct reasoning paths for a given    invoked K times, once per candidate. We observe,
                                         problem. In particular, for computational prob-        however, that the K statements for one problem are
                                         lems that require a concrete answer, as opposed        nearly identical: they typically share the same prob-
                                         to theorem-proving tasks for which only a proof        lem structure and differ only in the answer slots. A
                                         is required, such reasoning paths often arrive at      correct formalization of any one candidate already
                                         different answers, which raises a fundamental ques-    captures this shared structure; thus the remaining
                                         tion: how to verify which answer is correct? The       K−1 statements can in principle be obtained by
                                         paradigm of sampling a large number of answers         reusing one formalization and editing the answer
Figure 1: The BASE pipeline. An upstream solver emits K ranked candidate answers; BASE autoformalizes them in
rank order until one type-checks, giving the base statement Fb (a failure triggers “try next answer”). A two-tier
cascade—R1 direct substitution and R2 L EAN S CRIBE—edits Fb into the remaining K−1 statements, and the
highest-ranked type-checking candidate is selected.


expression in place. Realizing this efficiency gain,      step is the technical core, handled by a two-tier
however, is nontrivial, as candidate answers of-          cascade: a rule-based substitution for answers that
ten do not appear verbatim in the Lean statement          appear verbatim in the base statement, and L EAN -
but are instead encoded in syntactically diverse          S CRIBE, a learned rewriter we train, for the syntac-
forms. Therefore, reuse often requires localizing         tically diverse forms that rules cannot reach. BASE
and rewriting the answer-bearing expression rather        then returns the highest-ranked type-checked candi-
than a simple string substitution alone.                  date, without invoking the autoformalizer for all K
   In this work, we exploit the shared structure          candidates. In this work, BASE focuses on efficient
across a problem’s candidate statements for effi-         statement formalization and treats proof generation
cient formalization, taking a step toward scalable        as orthogonal, leaving its efficiency to future work;
Lean-based verification for computational prob-           nevertheless, statement-level type-checking already
lems. Specifically, we propose BASE (Base-And-            serves as an effective selection signal (Section 3.4).
Substitute-Edit; base-and-edit for short), an answer-        Figure 1 gives an overview and our contributions
selection pipeline that reuses a type-checked base        are summarized below:
formalization, i.e., a Lean statement accepted by         1. Pipeline. We propose BASE, an answer-
the compiler as well-formed. In this pipeline, an up-         selection pipeline that efficiently formalizes K
stream solver first produces a list of K candidate an-        candidates by formalizing a single base can-
swers ranked by its own confidence—highest first.             didate and deriving the remaining K−1 state-
Rather than formalizing all K candidate statements            ments with localized answer edits, thereby re-
independently, BASE formalizes them in rank order             ducing the autoformalizer cost from Θ(K) to
until one type-checks, and this type-checked base            Θ(1). To our knowledge, this is the first work
statement is then reused across the remaining candi-          to amortize formalization through a shared base.
dates, deriving the remaining statements by editing           BASE also serves as an efficient drop-in re-
only the answer expression in place. This editing             placement for the per-candidate formalization
   stage in existing formal-selection pipelines (Sec-   2025; Wang et al., 2025; Gao et al., 2025; Chan
   tion 5.5).                                           et al., 2025; Guo et al., 2025b) and proofs (Cabral
2. Model. We introduce L EAN S CRIBE, a learned         et al., 2025; Jana et al., 2025), each targeting a
   rewriter model trained to localize and re-express    single statement or proof at a time. Automated
   answers across diverse formal encodings. It is       theorem provers generate or search for machine-
   lightweight and invoked only once per problem,       checkable proofs of given formal statements. Mod-
   generating a reusable edit function applied to all   ern approaches are commonly LLM-based, in-
   K−1 candidates.                                      cluding next-tactic prediction (Polu and Sutskever,
3. Experiments. Across four benchmarks and              2020; Lample et al., 2022; Yang et al., 2023) and
   three solvers, BASE improves selection accu-         whole-proof generation (Ren et al., 2025; Xin et al.,
   racy on all twelve (dataset, solver) configura-      2025a; Lin et al., 2025a; Xin et al., 2025b). In this
   tions (up to +23 percentage points) while reduc-     work, we focus on the efficient autoformalization
   ing formalization cost by roughly 5×—a Pareto        of statements across multiple candidates, and our
   improvement over independent formalization.          pipeline builds on existing autoformalization and
                                                        prover models as underlying components.
2   Related Work
                                                        3     Method
Answer selection for math reasoning. Step-by-
                                                        We design a pipeline for efficient Lean-based an-
step reasoning (Wei et al., 2022) with many sam-
                                                        swer selection. Given an informal mathematics
pled candidates is often adopted for math reason-
                                                        problem x, we first elicit a ranked list of K dis-
ing (Lewkowycz et al., 2022; Azerbayev et al.,
                                                        tinct candidate answers S(x) = (a1 , . . . , aK ) from
2024). Without gold labels, candidates are usu-
                                                        an upstream LLM solver S in a single generation
ally selected by majority voting (Wang et al., 2023)
                                                        call. We then formalize each problem-answer pair
or a learned reward model—outcome- (Cobbe
                                                        (x, ai ) as a Lean 4 theorem statement, type-check
et al., 2021), process- (Uesato et al., 2022; Light-
                                                        the statements, and return the highest-ranked candi-
man et al., 2024; Wang et al., 2024), or genera-
                                                        date whose verification passes (falling back to the
tive (Zhang et al., 2024)—with related work on
                                                        top candidate if none does) (Section 3.4).
test-time compute allocation (Snell et al., 2025).
                                                           A naive instantiation of this pipeline requires a
These signals are statistical rather than formal, of-
                                                        separate autoformalizer call for each of the K can-
fering no guarantee of correctness.
                                                        didates, which we call independent formalization.
Formal verification for mathematical reasoning.         In contrast, with our proposed BASE (Section 3.2),
A growing line of work incorporates a proof as-         we derive the remaining K−1 formal statements
sistant for mathematical reasoning. FANS (Yao           from a single successfully formalized and type-
et al., 2025) formalizes each candidate answer into     checked base statement, via a two-tier cascade of a
a Lean 4 theorem and selects among verified ones;       rule-based rewriter and L EAN S CRIBE—a learned
S AFE (Liu et al., 2025) applies Lean 4 verification    answer rewriter we train (Section 3.3).
to verify reasoning steps. Others integrate Lean
                                                        3.1   Candidate Generation
into the reasoning loop (Ospanov et al., 2025b) or
repair proofs from compiler feedback (Ospanov           The upstream solver S produces a ranked list
et al., 2025a). However, these approaches formal-       of K distinct candidate answers, ordered by the
ize each statement independently, so the autofor-       solver’s own confidence: higher-ranked candidates
malization cost scales linearly with the number of      are those the solver believes more likely to be cor-
statements (Yao et al., 2025; Ospanov et al., 2025b;    rect. We obtain this list from a single generation
Lu et al., 2026), and the shared structure across       call for simplicity. The selection method described
them is left unexploited.                               below, however, is agnostic to how the candidates
                                                        are produced and may be applied to candidates in-
Autoformalization and theorem proving. Auto-            dependently sampled through different reasoning
formalization aims to translate natural-language        paths. We denote the solver’s output as
mathematics into formal languages such as
                                                                     S(x) = (a1 , a2 , . . . , aK ),
Lean (Moura and Ullrich, 2021). Existing work
trains specialized models and builds pipelines for      where a1 ≺ a2 ≺ · · · ≺ aK reflects the solver’s
autoformalizing individual statements (Lu et al.,       preference: a1 is the most likely candidate, aK the
least. We use this ordering both during formaliza-          Algorithm 1 BASE substitution cascade
tion and as a tiebreaker during selection.                  Require: base statement Fb , base answer ab , candidate ai
                                                             1: P ← G ATE(Fb , ab )       ▷ valid substitution sites for ab
3.2   Formalization: Independent and                            ▷ R1: direct localization
      Base-and-Edit                                          2: if |P| ≥ 1 then
                                                             3:     if |P| = 1 then
To verify a candidate answer ai with Lean, we                4:         p ← unique element of P
                                                             5:     else
translate the problem and that specific answer into          6:         p ← D ISAMBIG(Fb , P)
a formal theorem statement Fi using an answer-               7:     return S UBSTITUTE(Fb , p, ai )
conditioned autoformalizer F:                                   ▷ R2: predict local block s and fill function f
                                                             8: (s, f ) ← L EAN S CRIBE(x, Fb , ab )
          Fi = F(x, ai ),     i = 1, . . . , K.              9: if G ATE(Fb , s) is a singleton then
                                                            10:     return S UBSTITUTE(Fb , s, f (ai ))
Each statement Fi asserts that ai is the correct an-        11: return ⊥                           ▷ no substitution for ai
swer to x. We describe two strategies for gen-
erating these statements: a costly baseline (inde-
pendent formalization) and our proposed efficient           ab by exact string matching within the gated region
approach (base-and-edit).                                   of Fb , where the gate is a filter that restricts matches
                                                            to the theorem statement body and excludes other
Independent formalization (baseline). In this               parts such as comments and headers (Appendix B).
brute-force approach, F is invoked indepen-                 A unique match gives the substitution site directly;
dently for each candidate, incurring K autofor-             when ab matches at several positions, a small dis-
malizer calls per problem. This matches the per-            ambiguation model conditioned on the statement
candidate strategy of prior formal answer-selection         (Appendix C) selects the occurrence that serves as
pipelines (Yao et al., 2025) and serves as our effi-        the answer slot. R1 is cheap and exact, but it fails
ciency reference point.                                     whenever the autoformalizer does not encode the
                                                            answer as a verbatim copy of ab . For these cases
Base-and-edit (BASE). In contrast, we propose
                                                            the second tier (R2) invokes L EAN S CRIBE, the
BASE, which replaces these K independent formal-
                                                            answer rewriter we train (Section 3.3). For each
izations with one formalization plus K−1 local
                                                            candidate, the cascade applies R1 when direct lo-
edits. It proceeds in two steps: base discovery and
                                                            calization and insertion are feasible, and otherwise
a substitution cascade.
                                                            falls back to R2 (Algorithm 1).
   Base discovery. We iterate candidates in rank
order; for each ai , we compute Fi = F(x, ai ) and          3.3    L EAN S CRIBE: Learned Semantic
check whether Fi type-checks in Lean. Let                          Localization and Rewriting Model
           b = min{ i : Fi type-checks }.            (1)    The forms that defeat R1 span a broad range. For
                                                            example, a tuple “(3, 5)” may be formalized as two
When such a b exists, Fb becomes the base formal-           bindings (a = 3, b = 5) or as a single Prod value
ization and ab the base answer. Base discovery              ((3, 5) : N × N), so often no verbatim “(3, 5)”
requires at most b autoformalizer calls, and since          substring exists to be replaced. Similarly, inter-
recent autoformalizers (Wang et al., 2025) achieve          vals, sets, and symbolic forms require structural
a high compilation rate, b is typically small and                                             produce—“[0, 2)”
                                                            rewrites that no string match can √
thus the base discovery effectively costs only Θ(1)         becomes Set.Ico 0 2 and “3 13” becomes 3
autoformalizer calls in practice. If no candidate           * Real.sqrt 13. In each case, the surrounding
type-checks, we fall back to the top-ranked candi-          theorem structure binds the answer. Locating and
date a1 , which is rare (1.5% of problems overall;          rewriting it thus requires modeling how the auto-
Appendix F) and identical for both strategies.              formalizer encoded the answer in context, which
   Substitution cascade. Given (Fb , ab ), the cas-         is a semantic-parsing problem rather than a string-
cade evaluates each remaining candidate ai (i ̸= b)         matching one.
by constructing Fb→i , a modified statement that               To this end, we propose L EAN S CRIBE, a special-
reuses Fb ’s structure with only the answer expres-         ized fine-tuned LLM. Given (x, Fb , ab ), it (i) pre-
sion replaced by ai . The cascade applies two tiers         dicts a contiguous, answer-dependent local block
of increasing flexibility. The first tier (R1) is a rule-   s within Fb (localization) and (ii) generates a
based direct localization: it locates the base answer       lightweight Python function f mapping any infor-
    L EAN S CRIBE input                                                      S CRIBE model is trained by SFT at each iteration
 Problem x. “Find the distance between (2, −6) and (−4, 3).”                 as the dataset grows.
 Base answer ab . 3\sqrt{13}
 Base formalization Fb .
                                                                             3.4    Verification and Selection
        theorem ex :
          Real.sqrt ((2+4)ˆ2 + (-6-3)ˆ2)                                     Each formal statement Fi , encoding a particular
            = 3 * Real.sqrt 13 := by sorry
                                                                             candidate answer ai , is verified at two levels. The
    L EAN S CRIBE output                                                     statement level involves a Lean type-check: ci = 1
 Local block s. "3 * Real.sqrt 13"                                           iff the Lean 4 compiler accepts Fi as a well-formed
 Fill function g.                                                            proposition asserting ai as the answer. The proof
        def fill_answer(a: str) -> str:                                      level is stricter: a prover attempts a proof for the
          m = re.match(r’(\d+)\sqrt{(\d+)}’, a)
          return f"{m[1]} * Real.sqrt {m[2]}"
                                                                             given type-checked statement, and the Lean kernel
                                                                             then verifies the proof, giving pi = 1 iff the proof
 Inference. For each remaining candidate ai (e.g. 2\sqrt{13}), the cascade
 replaces this block in Fb with fill_answer(ai ); L EAN S CRIBE runs         passes Lean verification.
 once per problem, and the synthesized function runs once per remaining
 candidate.
                                                                                In this work, we focus on efficient statement for-
                                                                             malization. Proof-level verification, while more
Figure 2: L EAN S CRIBE prediction on a MATH-500                             rigorous, remains too limited in coverage to serve
distance problem. The model identifies the answer-                           as a practical selection signal: although cur-
dependent local block in Fb and generates a Python                           rent provers achieve strong performance at large
function that converts any informal answer of the same
                                                                             pass@K (Ren et al., 2025; Lin et al., 2025a; Liu
shape into the corresponding Lean expression.
                                                                             et al., 2026), their pass@1 success rates remain low
                                                                             (Section 5.4), making proof-level selection imprac-
                                                                             tical at the single-attempt budget we target. We
mal answer to the Lean expression that replaces s                            therefore base selection on the statement-level sig-
(transformation). Editing only this block preserves                          nal ci and leave efficient proof generation to future
the verified base structure, and the reusability of f                        work. A statement-level type-check certifies well-
allows the cost of a single model call to be amor-                           formedness of Fi rather than mathematical truth
tized across all K−1 candidates: we run f on each                            of ai , so selecting by ci is a practical choice that
ai (i ̸= b) to obtain Fi = f (ai ), effectively replac-                      does not yet provide a correctness guarantee for the
ing the answer expression of ab with that of ai                              selected answer, a gap we expect stronger and more
while leaving the rest of Fb intact. Figure 2 shows                          efficient provers to close in future work. Neverthe-
a concrete example.                                                          less, since the autoformalizer encodes the answer
   To train L EAN S CRIBE, we construct a training                           into a typed expression, a structurally inconsistent
dataset via a Lean-filtered expert iteration, inspired                       answer is more likely to yield an ill-typed state-
by prior work training reasoning models or the-                              ment, and combined with the solver’s ranking this
orem provers (Zelikman et al., 2022; Lin et al.,                             proves an effective selection signal in practice (Sec-
2025a): we iteratively collect model predictions,                            tions 5.3, 5.4). We study proof-level verification
retain only those whose outputs pass the Lean type-                          separately in Section 5.4.
check, and incorporate the accepted predictions                                 Given the signals {c1 , . . . , cK } and the solver’s
into the training dataset for supervised fine-tuning                         rank order a1 ≺ · · · ≺ aK (Section 3.1), we return
(SFT). We first build a seed dataset from N UMI -                            the highest-ranked type-checking candidate:
NA M ATH (Li et al., 2024): for each problem we
autoformalize the gold answer with F to obtain a                                    â = aj ∗ ,    j ∗ = min{ j : cj = 1 },      (2)
base statement, predict local blocks and fill func-
                                                                             falling back to a1 if none type-checks. This de-
tions using the base model, and keep only those
                                                                             sign combines the formal type-check signal with
whose reconstructed statements pass a Lean type-
                                                                             the solver’s ranking as a tiebreaker, requiring no
check. The seed dataset is used for the first itera-
                                                                             separate reward model.
tion of training. For subsequent iterations, using
the current L EAN S CRIBE checkpoint, we gener-                              4     Experimental Settings
ate block/function predictions on a broader set of
problems, particularly previously failed examples,                           4.1    Datasets
and expand the training dataset with the additional                          We evaluate on four mathematics benchmarks re-
type-checked predictions. A new, stronger L EAN -                            quiring concrete answers, spanning high-school
olympiad to Putnam-level difficulty: MATH-              cal for both methods), and Acc | GT@K is ACC
500 (Lightman et al., 2024; Hendrycks et al.,           on that subset, isolating verifier quality; thereby,
2021), comprising the standard 500-problem sub-         Acc = GT@K · Acc | GT@K. For verifier diag-
set of MATH; OlympiadBench (He et al., 2024),           nostics, GT-pass is the fraction whose gold state-
566 English single-answer olympiad problems;            ment type-checks and P-cand the average fraction
AMC-AIMO (AI-MO, 2024), 83 AMC12 prob-                  of candidate statements that type-check (ablation
lems (2022–2023) from the AIMO validation set;          only). For computational costs, we report autofor-
and AIME 2024 (AI-MO, 2024), the 30 problems            malizer calls per problem.
from the 2024 AIME. Answer types range from in-
tegers and rationals to algebraic expressions, inter-   5     Main Results
vals, sets, and natural-language descriptors; subset
                                                        5.1    Accuracy
selection and answer normalization are detailed in
Appendix A.                                             Table 1 reports our main result: BASE’s end-to-
                                                        end accuracy (ACC) and gold-pass rate (GT-pass)
4.2   Models and Implementation                         across four datasets and three upstream solvers,
To assess generality across solver families, we         against the independent formalization baseline.
use three upstream solvers for generating candi-        The pattern is consistent across solvers and datasets.
dates: Gemini 3 Pro, Qwen3-8B (Yang et al.,             BASE exceeds independent formalization on ACC
2025), and DeepSeek-R1-0528-Qwen3-8B (Guo               in all twelve (dataset, solver) cells, with gains from
et al., 2025a) (R1-Qwen3-8B in tables), all at K=8.     +0.7 to +23.3 points. It also raises GT-pass in all
For verification, the autoformalizer F is Kimina-       twelve cells (up to +33.3 points, remaining high
Autoformalizer-7B (Wang et al., 2025); type-            across all cells, 96–100%): the gold candidate’s
checking uses the Lean 4 compiler (Moura and            statement almost always survives under BASE, so
Ullrich, 2021), and the proof step uses DeepSeek-       sharing a verified base makes the gold formaliza-
Prover-V2-7B (Ren et al., 2025) with a single           tion markedly more robust.
greedy attempt per type-checked statement. For the      5.2    Cost
learned rewriter L EAN S CRIBE (Section 3.3), it is
based on Qwen3-8B (Yang et al., 2025) fine-tuned        Table 2 gives the per-problem formalization cost.
via LoRA on the expert-iterated training dataset        The autoformalizer dominates pipeline cost and is
with details in Appendix C. All inference runs on a     where the two pipelines differ in scaling: the base-
single RTX PRO 6000 GPU with vLLM and greedy            line issues one call per candidate (Θ(K)), while
decoding, and Lean 4 (Moura and Ullrich, 2021)          BASE issues one base call plus at most one substitu-
verification uses Mathlib 4 (mathlib Community,         tion call, giving Θ(1) cost determined by the base
2020) with a 60s per-statement timeout.                 rank b (≈1.5). The substitution call invokes L EAN -
                                                        S CRIBE once per problem to predict a reusable
4.3   Baseline and Metrics                              edit function (Section 3.3); this single prediction is
                                                        applied to all K−1 candidates and is far cheaper
Baseline. We compare primarily against indepen-
                                                        than the K−1 autoformalizer calls it replaces, so
dent formalization (Section 3.2): the same pipeline
                                                        it does not affect the Θ(1) scaling. At K=8 this is
but with K independent autoformalizer calls, in-
                                                        b/K=0.19× of independent formalization—a 4.7–
stead of one base call plus K−1 local edits. We
                                                        6.5× reduction (mean 5.4×)—and the gap widens
use identical verifier components, prompts, and se-
                                                        with K. Together with the accuracy result of Sec-
lection rule for both methods, so any difference is
                                                        tion 5.1, BASE is strictly cheaper while never less
attributable to the formalization strategy.
                                                        accurate across all twelve configurations, achieving
Metrics. All main results use the statement-level       a Pareto improvement.
signal (type-check); the proof level is studied sep-
arately (Section 5.4), and “verification” means         5.3    Ablations
the statement level unless noted. Acc is the frac-      Table 3 isolates the contribution of L EAN S CRIBE,
tion of problems whose selected answer equals           the learned answer rewriter (R2). The ablation
the gold answer. GT@K is the fraction whose             study is performed on MATH-500 (Gemini K=8),
gold answer appears in the ranked list (determined      measured by the per-candidate Lean pass rate (P-
solely by the upstream solver and thus identi-          cand)—the fraction of all candidate statements that
                                                                  ACC (%)                 GT-pass (%)
                 Dataset             Solver              Indep.     BASE (ours)      Indep.   BASE (ours)
                                     Gemini 3 Pro        70.2           79.4+9.2      87.3         98.7+11.4
                 MATH-500            Qwen3-8B            45.7           51.2+5.5      88.2         96.3+8.1
                                     R1-Qwen3-8B         58.7           67.5+8.8      85.4         98.8+13.4
                                     Gemini 3 Pro        41.7           53.4+11.7     77.6         99.0+21.4
                 OlympiadBench       Qwen3-8B            31.6           39.7+8.1      80.4         98.1+17.7
                                     R1-Qwen3-8B         42.8           53.2+10.4     79.4         100.0+20.6
                                     Gemini 3 Pro        73.5           86.7+13.2     82.9         100.0+17.1
                 AMC-AIMO            Qwen3-8B            37.8           46.8+9.0      72.9         97.9+25.0
                                     R1-Qwen3-8B         67.5           85.0+17.5     81.2         100.0+18.8
                                     Gemini 3 Pro        40.0           63.3+23.3     66.7         100.0+33.3
                 AIME 2024           Qwen3-8B            20.0           20.7+0.7      85.7         100.0+14.3
                                     R1-Qwen3-8B         44.8           60.7+15.9     73.7         100.0+26.3

Table 1: Main results across four datasets and three upstream solvers (K=8). Indep.=independent formalization.


 Dataset         Gemini 3 Pro Qwen3-8B R1-Qwen3-8B                 Dataset          Gemini 3 Pro    Qwen3-8B     R1-Qwen3-8B
 MATH-500            1.23          1.29          1.23              MATH-500           31.4+3.9        25.9+3.2     28.4+3.2
 AMC-AIMO            1.49          1.65          1.43              AMC-AIMO           13.3+3.5         8.9+1.3     16.2+5.0
 AIME 2024           1.67          1.50          1.70              AIME 2024          6.7+3.4          6.9+3.5     3.6−7.1
 OlympiadBench       1.65          1.57          1.45              OlympiadBench      11.9+2.8        11.2+2.5     11.8+3.3

Table 2: Per-problem formalization cost of BASE (av-              Table 4: Proof-level accuracy (%) for BASE, compared
erage number of base-discovery calls). In contrast, the           against the independent formalization baseline with
independent formalization baseline requires K=8 auto-             gains denoted in the subscripts. We use K=8 for candi-
formalizer calls per problem.                                     dates and DeepSeek-Prover-V2 for the prover.


     Dataset           Indep.     BASE    −R2    ∆R2
                                                                  5.4     Proof-level analysis
     MATH-500              87.5   87.9    67.9   +20.0
     AMC-AIMO              76.6   93.9    85.6   +8.3             We also run the full pipeline that further consists of
     AIME 2024             76.1   82.6    60.1   +22.5
     OlympiadBench         76.8   86.4    67.7   +18.7
                                                                  proving the formal statements with a prover, and
                                                                  we first use D EEP S EEK -P ROVER -V2 (Ren et al.,
Table 3: Component ablation (P-cand %, Gemini, K =                2025). This studies whether the statement-level
8). “Indep.” is the baseline; BASE uses both R1 and R2;
                                                                  gains carry through to a prover that must close
“−R2” disables R2, leaving R1 only; “∆R2 ” indicates
the contribution of R2 on top of using R1 only.                   each theorem. Prior work on provers typically re-
                                                                  ports pass@k with a large k, sampling many proof
                                                                  attempts per theorem. In our setting, however, each
verify. Removing R2 leaves only the rule-based                    of the K candidate answers needs its own proof, so
localization tier (R1). L EAN S CRIBE accounts for                a large k for sampling proofs would multiply the
8 to 22 points of per-candidate coverage (∆R2 ).                  prover cost by a factor of K and is impractical. We
Rule-only localization (R1) handles answers ap-                   therefore use a single pass@1 proof attempt per
pearing as verbatim substrings of the base, but                   candidate.
L EAN S CRIBE recovers many candidates that en-                      Table 4 shows the results. We notice that the
code answers differently; the two tiers are thus                  proof-level accuracies are low (4–31%) compared
complementary, with R1 covering easy verbatim                     to results in Table 1, which is because of the
edits and R2 the harder cases.                                    limited capability of the prover under the single-
   L EAN S CRIBE also generalizes out of distribu-                attempt budget. Nevertheless, we still compare
tion: although fine-tuned only on NuminaMath                      BASE against independent formalization in each
(Section 4.2), it attains high GT-pass on every                   setting, which is the focus of this work. BASE im-
benchmark (Table 1, 96–100%), indicating that its                 proves proof-level accuracy on 11 out of 12 cells
localization-and-rewriting behavior transfers rather              (sign test p=0.006), the lone exception being the
than memorizing NuminaMath patterns, with resid-                  smallest cell (AIME-2024, R1-Qwen3-8B, n=28).
ual failures concentrated on very long answer ex-                 This echoes prior findings that the quality of the
pressions and unusual geometric constructions.                    formal statement shapes how a downstream prover
 Dataset      Prover    Complete (%)    GT-complete (%)    Solver         Method GT@K Acc | GT@K Acc
              DSP-V2       7.3+0.8          31.4+2.3                      Indep.   80.4       87.3       70.2
 MATH-500                                                  Gemini 3 Pro
              Kimina         6.5             29.1                         BASE     80.6       98.5       79.4
              DSP-V2       8.1+3.9          14.5+6.1
 AMC-AIMO                                                                 Indep.   60.9       75.0       45.7
              Kimina         4.2              8.4          Qwen3-8B
                                                                          BASE     60.7       84.3       51.2
Table 5: Prover swap on BASE-formalized candi-                            Indep.   69.0       85.1       58.7
dates. Complete/GT-complete: candidate-level and gold-     R1-Qwen3-8B
                                                                          BASE     68.8       98.2       67.5
answer proof-completion rates.
                                                               Table 7: Factorization on MATH-500 (%).

  Dataset        Calls (Indep.→BASE)          Acc
  MATH-500        4000 → 689 (5.8× ↓)    88.2 → 88.6      use candidate answers from Qwen2.5-Math-7B-
  AMC-AIMO         664 → 116 (5.7× ↓)    62.7 → 61.4      Instruct, following FANS, and sample K=8 can-
  AIME 2024         240 → 53 (4.5× ↓)    13.3 → 13.3
                                                          didates. Keeping other components fixed, we re-
Table 6: Dropping BASE into a FANS-style majority-        place only the formalization stage: FANS originally
voting pipeline (Qwen2.5-Math-7B-Instruct, K=8) by        uses independent formalization; in contrast, we de-
replacing only the formalization stage. Calls: autofor-   rive one Lean-verified base statement and edit it
malizer calls per dataset; Acc: selection accuracy (%).
                                                          for the rest. In this way, we isolate the impact of
                                                          our improved autoformalization, and compare the
fares (Jiang et al., 2023; Wu et al., 2022). The per-     number of autoformalizer calls and final selection
candidate false-positive rate—an incorrect answer         accuracy under an otherwise identical downstream
receiving a complete proof—is a low ∼7% on aver-          pipeline. Table 6 shows the results, with experi-
age (1–14% across cells), arising when the autofor-       mental details in Appendix D. Our BASE cuts aut-
malizer renders an incorrect answer as a statement        oformalizer calls by 4.5–5.8× while maintaining
that type-checks and admits a proof. Given such           accuracy. This demonstrates that BASE is a flexi-
false positives, we combine the formal signal with        ble and efficient module that can be integrated into
the solver’s ranking rather than relying on a single      other pipelines, such as FANS, that make contribu-
proof.                                                    tions orthogonal to efficient autoformalization for
                                                          Lean-based answer-selection.
Swapping the prover. BASE feeds type-checked
candidates to an off-the-shelf prover, so the prover      6   Mechanism and Analysis
should be interchangeable. Replacing D EEP S EEK -        Factorizing the gain. End-to-end accuracy fac-
P ROVER -V2 with K IMINA -P ROVER -P REVIEW-              torizes cleanly into
D ISTILL -7B (Wang et al., 2025) (Table 5), the two
are close on MATH-500 but D EEP S EEK -P ROVER -                    Acc = GT@K · Acc | GT@K,               (3)
V2 is about twice as strong on AMC-AIMO. The
advantage is dataset-dependent, and base-and-edit         where the first factor depends mostly on the up-
is agnostic to the prover used.                           stream solver (both methods score the same can-
                                                          didate list) and the second is the verifier’s con-
5.5   Drop-in for an Existing Pipeline                    version rate on solver-correct problems, so any
                                                          sizable difference in Acc comes from the verifier.
Our BASE pipeline described in Section 3 is stream-
                                                          Table 7 confirms this on MATH-500: GT@K is
lined to focus on the formalization stage and en-
                                                          essentially identical across methods, while BASE’s
able efficient formalization for K candidates. In
                                                          Acc | GT@K is uniformly higher across all three
practice, Lean-based answer selection can be more
                                                          solvers. The gain is thus a verifier effect: BASE
sophisticated and can contain proving statements
                                                          does not change which answers the solver proposes,
in addition to formalization. Our efficient base-
                                                          but raises the rate at which a solver-correct answer
and-edit formalization in BASE can be seamlessly
                                                          is retained.
integrated into other Lean-based answer-selection
pipelines. We demonstrate this with FANS (Yao             Where the gain comes from: the shared veri-
et al., 2025), which generates proofs for state-          fied base. To trace the gain to the shared ver-
ments, checks consistency between natural lan-            ified base, we compare three strategies on the
guage and formal language with a QwQ-32B judge,           same candidate lists (Table 8). Both variants that
and enhances the selection by majority vote. We           reuse a single verified base—BASE, which reuses
 Setting                GT-pass P-cand Acc Acc | GT@K Limitations
 Indep. baseline         81.9   81.2   39.3     66.7
 First verified base     98.2   91.7   47.1     79.5     This work focuses on the efficiency of statement
 Random verified base    95.4   91.2   45.6     77.0     autoformalization for K candidate answers, and we
Table 8: Ablating the shared verified base (%) on        use statement-level type-checking as the selection
a matched set of OlympiadBench, AMC-AIMO, and            signal due to the limitation of provers. Future work
AIME 2024.                                               is needed to address the efficiency of provers when
                                                         handling K relevant theorem statements for the
                                                         candidate answers, and enable an efficient answer-
the first type-checking candidate, and a control         selection with both statement autoformalization
that reuses a random one—outperform indepen-             and theorem proving. In our method, base-and-edit
dent formalization, and crucially first ≈ random:        assumes the K candidate answers share problem-
the benefit comes from structural reuse, not from        side structure so that a single base formalization
cherry-picking a good formalization. This traces         can be reused; this holds for the tasks we study but
to one mechanism—sharing a single verified scaf-         may not transfer to settings where each candidate
fold rather than formalizing independently. Sta-         requires a structurally different statement. Lastly,
tistically, sharing cuts per-candidate formalization     since we find that prover can appear to complete
noise (6.3× lower pairwise variance, though only         proofs for some of the incorrect answers, the faith-
part of the story: r=0.22 with per-problem gains);       fulness of autoformalization remains a challenge
mechanistically, every candidate inherits the base’s     for future work.
verified structure rather than risking its own auto-
formalizer failure. Either way, sharing raises the       Ethics Statement
type-check rate by +9.9 points (Appendix G).
                                                         This work studies answer selection for mathemat-
                                                         ical reasoning using public benchmarks (MATH-
7   Conclusion                                           500, OlympiadBench, AMC-AIMO, AIME 2024)
                                                         and models; it involves no human subjects, no pri-
We present BASE, a base-and-edit approach to for-
                                                         vate or personally identifiable data, and no sensitive
mal answer selection that formalizes a single ver-
                                                         content. L EAN S CRIBE is fine-tuned on the openly
ified base per problem and derives the remaining
                                                         available NuminaMath dataset. The primary in-
candidates by editing only the answer block. Re-
                                                         tended use is reducing the inference cost of formal
placing K independent autoformalizer calls with
                                                         answer verification while improving the reliability,
one base call plus localized edits cuts formalization
                                                         which lowers the energy and compute footprint of
cost from Θ(K) to Θ(1) while improving selection
                                                         test-time scaling rather than increasing it. As we
accuracy—a Pareto improvement on all twelve con-
                                                         emphasize in Section 5.4, a single Lean proof is not
figurations. Our analysis traces the gain to the veri-
                                                         a standalone correctness guarantee; practitioners
fier and the use of shared base formalization. We
                                                         should not treat the formal signal as infallible certi-
believe this work will enable more practical answer-
                                                         fication, particularly in high-stakes settings, since
selection and verification for natural-language rea-
                                                         residual errors can arise from mis-formalization.
soning with Lean.
                                                         We see no foreseeable risk of harm specific to this
                                                         work beyond those general to mathematical reason-
Acknowledgement                                          ing systems.

This work is supported in part by an NVIDIA Aca-
demic Grant Program award.                               References
  This work used the Delta system at the National
                                                         AI-MO. 2024. AIMO validation datasets (AMC,
Center for Supercomputing Applications [award              AIME). https://huggingface.co/AI-MO.
OAC 2005572] through allocation CIS250704 from
the Advanced Cyberinfrastructure Coordination            Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster,
Ecosystem: Services & Support (ACCESS) pro-                Marco Dos Santos, Stephen Marcus McAleer, Al-
                                                           bert Q. Jiang, Jia Deng, Stella Biderman, and Sean
gram, which is supported by National Science               Welleck. 2024. Llemma: An open language model
Foundation grants #2138259, #2138286, #2138307,            for mathematics. In The Twelfth International Con-
#2137603, and #2138296.                                    ference on Learning Representations.
Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald     Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,
  Clark, Quoc V Le, Christopher Ré, and Azalia Mirho-      Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja
  seini. 2024. Large language monkeys: Scaling infer-      Jamnik, Guillaume Lample, and Yuhuai Wu. 2023.
  ence compute with repeated sampling. arXiv preprint      Draft, sketch, and prove: Guiding formal theorem
  arXiv:2407.21787.                                        provers with informal proofs. In The Eleventh Inter-
                                                           national Conference on Learning Representations.
Rafael Cabral, Tuan Manh Do, Xuejun Yu, Wai Ming
  Tai, Zijin Feng, and Xin Shen. 2025. Proofflow: A      Guillaume Lample, Timothee Lacroix, Marie-Anne
  dependency graph approach to faithful proof autofor-     Lachaux, Aurelien Rodriguez, Amaury Hayat,
  malization. arXiv preprint arXiv:2510.15981.             Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.
                                                           2022. Hypertree proof search for neural theorem
Willy Chan, Michael Souliman, Jakob Nordhagen,             proving. Advances in neural information processing
  Brando Miranda, and Sanmi Koyejo. 2025. Lean-            systems, 35:26337–26349.
  ing on quality: How high-quality data beats diverse
  multilingual data in autoformalization.                Aitor Lewkowycz, Anders Johan Andreassen,
                                                           David Dohan, Ethan Dyer, Henryk Michalewski,
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,            Vinay Venkatesh Ramasesh, Ambrose Slone, Cem
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias           Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu,
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro          Behnam Neyshabur, Guy Gur-Ari, and Vedant Misra.
  Nakano, and 1 others. 2021. Training verifiers           2022. Solving quantitative reasoning problems with
  to solve math word problems. arXiv preprint              language models. In Advances in Neural Information
  arXiv:2110.14168.                                        Processing Systems.

Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao,        Jia Li, Edward Beeching, Lewis Tunstall, Ben Lip-
  Zihan Qin, Tianyi Xu, and Bin Dong. 2025. Her-            kin, Roman Soletskyi, Shengyi Huang, Kashif Rasul,
  ald: A natural language annotated lean 4 dataset. In      Longhui Yu, Albert Q Jiang, Ziju Shen, and 1 oth-
  The Thirteenth International Conference on Learning       ers. 2024. Numinamath: The largest public dataset
  Representations.                                          in ai4maths with 860k pairs of competition math
                                                            problems and solutions. Hugging Face repository,
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,          13(9):9.
  Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang,
  Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai Yu,       Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
  Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhu-          son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  oshu Li, Ziyi Gao, Aixin Liu, and 175 others. 2025a.     John Schulman, Ilya Sutskever, and Karl Cobbe.
  Deepseek-r1 incentivizes reasoning in llms through       2024. Let’s verify step by step. In The Twelfth Inter-
  reinforcement learning. Nature, 645(8081).               national Conference on Learning Representations.
                                                         Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
Qi Guo, Jianing Wang, Jianfei Zhang, Deyang Kong,          Hongzhou Lin, Kaiyu Yang, Jia LI, Mengzhou Xia,
  Xiangzhou Huang, Xiangyu Xi, Wei Wang, Jingang           Danqi Chen, Sanjeev Arora, and Chi Jin. 2025a.
  Wang, Xunliang Cai, Shikun Zhang, and 1 others.          Goedel-prover: A frontier model for open-source
  2025b. Autoformalizer with tool feedback. arXiv          automated theorem proving. In Second Conference
  preprint arXiv:2510.06857.                               on Language Modeling.
Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding            Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-
  Hu, Zhen Thai, Junhao Shen, Jinyi Hu, Xu Han,            Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
  Yujie Huang, Yuxiang Zhang, and 1 others. 2024.          Jiawei Ge, Jingruo Sun, and 1 others. 2025b. Goedel-
  Olympiadbench: A challenging benchmark for pro-          prover-v2: Scaling formal theorem proving with
  moting agi with olympiad-level bilingual multimodal      scaffolded data synthesis and self-correction. arXiv
  scientific problems. In Proceedings of the 62nd An-      preprint arXiv:2508.03613.
  nual Meeting of the Association for Computational
  Linguistics (Volume 1: Long Papers), pages 3828–       Chengwu Liu, Ye Yuan, Yichun Yin, Yan Xu, Xin Xu,
  3850.                                                    Zaoyu Chen, Yasheng Wang, Lifeng Shang, Qun Liu,
                                                           and Ming Zhang. 2025. Safe: Enhancing mathemati-
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul         cal reasoning in large language models via retrospec-
  Arora, Steven Basart, Eric Tang, Dawn Song, and          tive step-aware formal verification. In Proceedings
  Jacob Steinhardt. 2021. Measuring mathematical           of the 63rd Annual Meeting of the Association for
  problem solving with the MATH dataset. In Thirty-        Computational Linguistics (Volume 1: Long Papers),
  fifth Conference on Neural Information Processing        pages 12171–12186.
  Systems Datasets and Benchmarks Track (Round 2).
                                                         Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos,
Prithwish Jana, Kaan Kale, Ahmet Ege Tanriverdi,           Weikun He, Jiawei Liu, Ran Wang, Yunzhou Xie,
   Cruise Song, Sriram Vishwanath, and Vijay Ganesh.       Junqiao Zhao, Qiufeng Wang, and 1 others. 2026.
   2025. Proofbridge: Auto-formalization of natural        Numina-lean-agent: An open and general agentic
   language proofs in lean via joint embeddings. arXiv     reasoning system for formal mathematics. arXiv
   preprint arXiv:2510.15681.                              preprint arXiv:2601.14027.
Haijian Lu, Wei Wang, and Jing Liu. 2026. For-            Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai
  malevolve: Neuro-symbolic evolutionary search             Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
  for diverse and prover-effective autoformalization.       2024. Math-shepherd: Verify and reinforce LLMs
  Preprint, arXiv:2603.19828.                               step-by-step without human annotations. In Proceed-
                                                            ings of the 62nd Annual Meeting of the Association
Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang,       for Computational Linguistics (Volume 1: Long Pa-
   Jing Xiong, Liu Chengwu, Jianhao Shen, Hui Jin,          pers), pages 9426–9439, Bangkok, Thailand. Associ-
   Jipeng Zhang, Haiming Wang, Zhicheng Yang, Jing          ation for Computational Linguistics.
   Tang, and Zhijiang Guo. 2025. Process-driven auto-
   formalization in lean 4.                               Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le,
                                                            Ed H. Chi, Sharan Narang, Aakanksha Chowdhery,
The mathlib Community. 2020. The lean mathematical          and Denny Zhou. 2023. Self-consistency improves
  library. In Proceedings of the 9th ACM SIGPLAN            chain of thought reasoning in language models. In
  International Conference on Certified Programs and        The Eleventh International Conference on Learning
  Proofs, page 367–381. ACM.                                Representations.
Leonardo de Moura and Sebastian Ullrich. 2021. The        Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  lean 4 theorem prover and programming language. In         Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
  International Conference on Automated Deduction,           and 1 others. 2022. Chain-of-thought prompting elic-
  pages 625–635. Springer.                                   its reasoning in large language models. Advances
                                                             in neural information processing systems, 35:24824–
Azim Ospanov, Farzan Farnia, and Roozbeh Youse-
                                                             24837.
  fzadeh. 2025a. APOLLO: Automated LLM and lean
  collaboration for advanced formal reasoning. In The     Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li,
  Thirty-ninth Annual Conference on Neural Informa-         Markus Norman Rabe, Charles E Staats, Mateja Jam-
  tion Processing Systems.                                  nik, and Christian Szegedy. 2022. Autoformalization
Azim Ospanov, Zijin Feng, Jiacheng Sun, Haoli Bai,          with large language models. In Advances in Neural
  Xin Shen, and Farzan Farnia. 2025b. Hermes: To-           Information Processing Systems.
  wards efficient and verifiable mathematical reasoning
                                                          Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao,
  in llms. Preprint, arXiv:2511.18760.
                                                            Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,
Stanislas Polu and Ilya Sutskever. 2020. Generative         Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang,
   language modeling for automated theorem proving.         Qihao Zhu, Dejian Yang, Zhibin Gou, Z.F. Wu, Fuli
  Preprint, arXiv:2009.03393.                               Luo, and Chong Ruan. 2025a. Deepseek-prover-
                                                            v1.5: Harnessing proof assistant feedback for rein-
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,         forcement learning and monte-carlo tree search. In
   Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,         The Thirteenth International Conference on Learning
   Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-       Representations.
   rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,
   Daya Guo, and Chong Ruan. 2025. Deepseek-prover-       Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang
   v2: Advancing formal mathematical reasoning via          Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Ming
   reinforcement learning for subgoal decomposition.        Ding. 2025b. BFS-prover: Scalable best-first tree
   Preprint, arXiv:2504.21801.                              search for LLM-based automatic theorem proving.
                                                            In Proceedings of the 63rd Annual Meeting of the
Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Avi-      Association for Computational Linguistics (Volume 1:
  ral Kumar. 2025. Scaling LLM test-time compute            Long Papers), pages 32588–32599, Vienna, Austria.
  optimally can be more effective than scaling param-       Association for Computational Linguistics.
  eters for reasoning. In The Thirteenth International
  Conference on Learning Representations.                 An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
                                                            Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-          Chengen Huang, Chenxu Lv, Chujie Zheng, Day-
  cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,       iheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao
  Geoffrey Irving, and Irina Higgins. 2022. Solv-           Ge, Haoran Wei, Huan Lin, Jialong Tang, and 41
  ing math word problems with process-and outcome-          others. 2025. Qwen3 technical report. Preprint,
  based feedback. arXiv preprint arXiv:2211.14275.          arXiv:2505.09388.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas             Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chala-
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,          mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jian-             Prenger, and Animashree Anandkumar. 2023. Le-
  qiao Lu, Hugues de Saxcé, Bolton Bailey, Chen-            andojo: Theorem proving with retrieval-augmented
  dong Song, Chenjun Xiao, Dehao Zhang, Ebony               language models. Advances in Neural Information
  Zhang, Frederick Pu, Han Zhu, and 21 others. 2025.        Processing Systems, 36:21573–21612.
  Kimina-prover preview: Towards large formal rea-
  soning models with reinforcement learning. Preprint,    Jiarui Yao, Ruida Wang, and Tong Zhang. 2025. FANS:
  arXiv:2504.11354.                                          Formal answer selection for LLM natural language
  math reasoning using lean4. In Proceedings of the
  2025 Conference on Empirical Methods in Natural
  Language Processing, pages 3181–3200, Suzhou,
  China. Association for Computational Linguistics.
Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Good-
   man. 2022. Star: Bootstrapping reasoning with rea-
   soning. Advances in Neural Information Processing
  Systems, 35:15476–15488.
Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran
  Kazemi, Aviral Kumar, and Rishabh Agarwal. 2024.
  Generative verifiers: Reward modeling as next-token
  prediction. In The 4th Workshop on Mathematical
  Reasoning and AI at NeurIPS’24.
Jin Zhou, Charles Staats, Wenda Li, Christian Szegedy,
   Kilian Weinberger, and Yuhuai Wu. 2024. Don’t
   trust: Verify–grounding llm quantitative reasoning
   with autoformalization. In International Conference
   on Learning Representations, volume 2024, pages
   2544–2563.
A    Dataset Details                                        fill_answer(answer: str) -> str that,
                                                            given any informal answer string, returns the
MATH-500 is the 500-problem evaluation sub-
                                                            Lean expression replacing that block.
set (Lightman et al., 2024) of MATH (Hendrycks
et al., 2021). OlympiadBench (He et al., 2024):         The local block is required to occur exactly once
we use the English mathematics open-ended sub-          in Fb outside comments and inside the theorem
set, restricted to single-answer problems with          body; otherwise the example is discarded during
Numerical or Expression answer types, yielding          inference.
566 problems; proof-only problems are excluded          Lean-filtered expert iteration. The corpus is
as they fall outside the answer-construction setting    built in stages, each Lean-filtered. Phase 1
(Section 1). AMC-AIMO is the AIMO validation            (225 examples) consists of verified seed rewrites
AMC set (AI-MO, 2024): 83 AMC12 problems                mined directly from N UMINA M ATH formaliza-
from 2022–2023, extracted from the AoPS wiki            tions. Phase 2 (699 examples after strict fil-
and normalized to integer-answer form. AIME             tering) is generated by an intermediate L EAN -
2024 is the 30-problem AIME subset of the AIMO          S CRIBE checkpoint under rejection sampling: the
validation set (AI-MO, 2024).                           checkpoint produces several block/function pre-
B   Substitution Gate                                   dictions per problem, and we keep only those
                                                        whose reconstructed statements pass an indepen-
The substitution gate referenced in Section 3.2         dent Lean type-check. We additionally mine
filters candidate positions through two structural      hard cases—problems where direct localization
checks:                                                 fails—with earlier checkpoints, again retaining
1. Comment-aware filter. Exclude positions in-          only Lean-passing rewrites (3,262 examples after
   side Lean block comments (/- . . . -/) and           de-duplication against Phases 1–2). Merging these
   line comments (– . . . ).                            gives 4,186 examples (3,768 train / 418 test). The
                                                        final L EAN S CRIBE is a Qwen3-8B model LoRA-
2. Theorem-body filter.             Restrict posi-      fine-tuned on this aggregated corpus, with rank 32,
   tions to the local block between the                 α=64, and dropout 0.05 on all attention and MLP
   theorem/lemma/example keyword and the                projections, for 3 epochs at learning rate 1×10−4
   := by proof marker, excluding imports, helper        in bfloat16. The R1 disambiguation step (choos-
   definitions, and content after the proof.            ing among multiple occurrences of the answer
A position survives the gate iff it passes both fil-    string) uses the same base model without the LoRA
ters. The gate is deterministic and stateless. We       adapter, prompted to return the index of the answer
additionally short-circuit the base candidate ab in     slot; only L EAN S CRIBE (R2) uses the fine-tuned
the cascade: since the base statement Fb type-          adapter.
checks by construction, we mark ab as verified
without re-running the substitution, avoiding spuri-
                                                        D     Drop-in Pipeline Setup
ous failures from non-round-tripping edits. A per-      The drop-in experiment (Section 5.5) embeds base-
candidate fallback further routes individual unsafe     and-edit into a FANS-style pipeline (Yao et al.,
candidates (e.g., natural-language labels) to L EAN -   2025). This setting differs from our main rank-
S CRIBE even when R1 would otherwise apply; we          based pipeline in three ways: a single solver,
ablate this in Section 5.3.                             Qwen2.5-Math-7B-Instruct, produces the K=8
                                                        candidate answers; an NL–FL consistency judge
C    L EAN S CRIBE SFT Details                          (QwQ-32B) filters formalizations; and the final se-
Each L EAN S CRIBE training example consists of:        lector aggregates surviving candidates by majority
                                                        vote rather than by generator rank.
• Input. An informal problem x, a Lean statement
                                                           The full pipeline is proof-level. Candidate an-
  Fb that the autoformalizer produced for some
                                                        swers are converted into formal statements using
  verified base answer ab , and the natural-language
                                                        either independent Kimina formalization or BASE.
  original answer string.
                                                        D EEP S EEK -P ROVER -V2 then generates proofs for
• Output.     A JSON object specifying (i)              the resulting statements; QwQ-32B checks natural-
  the predicted local block inside Fb that en-          language–formal consistency; the Lean server ver-
  codes the answer, and (ii) a Python function          ifies the generated proofs; and majority vote is
applied over candidates that pass both the proof          G    Variance Reduction Detail
and consistency filters. Thus, in this section, “ver-
                                                          The base-ablation of Section 6 (Table 8) excludes
ified candidates” refers to candidates whose gen-
                                                          MATH-500: substituting alternative answers into
erated proofs are accepted by Lean and whose for-
                                                          its bases produces statements whose Lean elabo-
mal statements pass the NL–FL consistency judge,
                                                          ration is prohibitively slow, hitting the type-check
not merely statements that type-check before proof
                                                          timeout on nearly every candidate, so the matched-
search.
                                                          set comparison there is run on OlympiadBench,
   We hold the answer generator, prover, NL–FL
                                                          AMC-AIMO, and AIME 2024. This exclusion af-
judge, Lean proof verifier, majority-vote selector,
                                                          fects only the three-way base-ablation; the main
and candidate inputs fixed, and swap only the for-
                                                          results (Table 1) and the factorization (Table 7)
malization stage. Independent formalization is the
                                                          do include MATH-500 and show the same qual-
FANS default, while BASE preserves the K candi-
                                                          itative pattern there—BASE raises Acc | GT@K
date slots and fills them with base-and-edit formal
                                                          while leaving GT@K nearly unchanged—so we
statements. Therefore, the differences in autofor-
                                                          do not expect the shared-base effect to be specific
malizer calls and final accuracy in Table 6 are at-
                                                          to the smaller datasets, though we cannot run the
tributable to the formalization strategy.
                                                          matched random-base control on MATH-500 itself.
                                                             Formalizing once rather than K times reduces
E    Proof-Complete Criterion
                                                          the variance among a problem’s K candidate state-
In the prover-swap ablation (Section 5.4) we report       ments. Measuring pairwise character n-gram dis-
the proof-complete rate—the fraction of statements        tance between the K statements of each problem,
for which the prover returns a proof that Lean ac-        BASE is 6.3× more consistent than independent
cepts with no remaining sorry placeholder—rather          formalization, stable across both solvers and all
than the raw pass rate. D EEP S EEK -P ROVER -V2          datasets. At the per-problem level, the magnitude
sometimes returns proofs that compile but leave a         of variance reduction predicts the type-check gain
sorry, which would admit a goal without proving           (Pearson r=0.22, p<10−3 , n=2015), and the gain
it; on MATH-500 its raw pass rate is 15.1% but            concentrates on problems the baseline struggles to
its proof-complete rate is 7.3%. K IMINA -P ROVER         formalize. Importantly, the variance signal predicts
does not emit such proofs, so the two rates coin-         the type-check gain but not the downstream prove-
cide for it. We use proof-complete throughout for         completion gain (|r|<0.05): variance reduction
a consistent comparison across provers.                   acts at the formalization stage, raising how many
                                                          candidates—and how many correct candidates—
F   Fall-back Rate                                        type-check and reach the prover, rather than chang-
                                                          ing what the prover can close.
On a small fraction of problems no candidate’s
autoformalization type-checks in Lean, so neither         H    Qualitative Formulation Examples
independent formalization nor BASE has a verified
statement to select from; for these we fall back          The examples below are drawn from MATH-500
to the top-ranked candidate a1 (Section 3.2). Ta-         (Gemini 3 Pro, K=8). Each shows a single prob-
ble 9 reports the per-dataset fall-back rate on the       lem with its verified base statement Fb , and then a
Gemini 3 Pro line.                                        second candidate answer ai formalized two ways:
                                                          by BASE (editing only the answer block of Fb )
      Dataset              n   Fall-backs   Rate          and by independent formalization (a fresh auto-
      MATH-500           500           6    1.2%          formalizer call). In every case the BASE edit
      OlympiadBench      566          12    2.1%          type-checks (✓) while the independent statement
      AIME 2024           30           0    0.0%          does not (×). The independent call, re-deriving
      AMC-AIMO            83           0    0.0%
                                                          the whole statement from scratch, drifts in ways
      Total            1179           18    1.5%
                                                          that break the Lean check—dropping the theo-
Table 9: Per-dataset fall-back rates (Gemini K=8): the    rem header, re-encoding the goal, or changing the
fraction of problems where no candidate formalization     domain—whereas BASE preserves the well-typed
type-checks. The rate is identical for the baseline and   structure of the shared base and rewrites only the
BASE, so it does not affect their comparison.             answer term. (import Mathlib headers are elided
                                                          for space.)
Example 1: tuple answer split across a conjunc-             Independent Fi (×):
tion. Problem. Find (p, q, r) such that x3 − 3x2 +          theorem (f : R → R) (h : . . . ) (h’ :
                                                            f 1 = 1) :
4x − 1 divides x9 + px6 + qx3 + r. Base answer                {n : Z | f n = n} = {-1, 1} := by sorry
ab = (6, 31, −1); candidate ai = (−6, −31, 1).
                                                       BASE’s base encodes the fixed-point set over R
     Fb (✓):
     open Polynomial                                   with an integrality constraint. The independent call
     theorem thm {p q r : R}                           re-types the set over Z and applies f : R → R
       (h : (Xˆ3 - 3*Xˆ2 + 4*X - C 1 : R[X])
         | (Xˆ9 + C p*Xˆ6 + C q*Xˆ3 + C r)) :
                                                       to an integer index, which is ill-typed; it does not
       p = 6 ∧ q = 31 ∧ r = -1 := by sorry             type-check.
     Base Fb→i (✓): same body,
       p = -6 ∧ q = -31 ∧ r = 1 := by sorry
                                                       Summary. Across these cases the same answer is
     Independent Fi (×):
                                                       well-typed under BASE but not under independent
     theorem (p q r : R)                               formalization—not because the answer is intrinsi-
       (h : ∀ (z : C), zˆ3 - 3*zˆ2 + 4*z - 1           cally hard to formalize, but because re-formalizing
     = 0
         → zˆ9 + p*zˆ6 + q*zˆ3 + r = 0) :              from scratch introduces structural and typing vari-
       p = -6 ∧ q = -31 ∧ r = 1 := by sorry            ance that the shared verified base eliminates. This
                                                       is the per-example face of the variance reduction
BASE edits the three scalar slots of the verified      quantified in Appendix G.
divisibility statement. The independent call instead
re-encodes divisibility as a quantifier over complex
roots and omits the theorem name, and does not
type-check.
Example 2: set-valued answer. Problem. Find
all real x with (x − 3)3 + (x − 7)3 = (2x − 10)3 .
Base answer ab = {3, 5, 7}; candidate ai =
{−3, 7}.
     Fb (✓):
     theorem thm :
       {x | (x-3)ˆ3 + (x-7)ˆ3 = (2*x-10)ˆ3}
         = {3, 5, 7} := by sorry
     Base Fb→i (✓): same body, = {-3, 7}
     Independent Fi (×):
     theorem (x : R) :
       (x-3)ˆ3 + (x-7)ˆ3 = (2*x-10)ˆ3
         ↔ x = -3 ∨ x = 7 := by sorry

BASE keeps the set-equality form and edits the
solution set. The independent call rewrites the
same answer as a biconditional over a free variable
(and drops the header), changing the proposition’s
shape; it does not type-check.
Example 3: domain divergence (Z vs. R). Prob-
lem. For f : R → R with f (x) + f (y) =
f (x+y) − xy − 1 and f (1) = 1, find the integer
fixed points. Base answer ab = {−2, 1}; candi-
date ai = {−1, 1}.
    Fb (✓):
    theorem thm {f : R → R}
       (h : ∀ x y, f x + f y = f (x+y) - x*y
    - 1)
       (h’ : f 1 = 1) :
       {n | ∃ m : Z, n = m ∧ f n = n} = {-2,
    1}
       := by sorry
     Base Fb→i (✓): same body, = {-1, 1}
