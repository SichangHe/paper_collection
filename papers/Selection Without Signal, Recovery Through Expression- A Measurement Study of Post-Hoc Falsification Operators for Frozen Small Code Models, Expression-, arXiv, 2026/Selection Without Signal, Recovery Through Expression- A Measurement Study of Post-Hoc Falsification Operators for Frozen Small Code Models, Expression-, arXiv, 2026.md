                                                   Selection Without Signal, Recovery Through
                                                                                     Expression:
                                                A Measurement Study of Post-Hoc Falsification
                                                                                      Operators
arXiv:2606.16999v1 [cs.SE] 15 Jun 2026




                                                                 for Frozen Small Code Models
                                                                                        Mehmet İşcan∗
                                                                   PythaLab, Yıldız Technical University, Istanbul, Turkey




                                                                                           Abstract

                                               Frozen small code models—at most about 1.5 billion parameters and run locally without
                                               fine-tuning—are attractive for offline and privacy-constrained use, but they often emit plausible-
                                               but-wrong programs. A natural remedy is a post-hoc operator that selects, verifies, repairs, or
                                               otherwise re-processes the model’s own samples without retraining it; in its most principled form
                                               the operator is Popperian, attacking each candidate with a severe test and keeping what survives.
                                               This paper measures whether such operators help. Under a single deterministic execution oracle
                                               and a leakage-free, matched-compute protocol, twenty-six semantic post-hoc operators—spanning
                                               selection, verification, repair, elimination, portfolios, sound vetoes, and generation conditioning—
                                               are evaluated against a Best-of-N (BoN) baseline; on the model cells and benchmarks tested,
                                               none improves held-out accuracy over BoN. The negative is mechanistic rather than a tuning
                                               failure, and three measured forces account for it: a coverage wall (the weak model’s hard-task
                                               failures are systematic, and deeper sampling does not rescue them), a capability scissors (a
                                               competent generator leaves almost no discriminable error among the candidates that pass the
                                               visible tests), and a near-empty consensus trap (the visible-passing-but-hidden-wrong majority
                                               a leakage-free selector needs almost never co-occurs with a correct alternative in the pool). A
                                               distribution-free do-no-harm bound cannot guarantee a population harm rate of ≤ α even at
                                               zero observed harm unless n ≥ 45. Two operators help on a different axis, outside the semantic
                                               output space. An expression-layer recovery (M1)—the only accuracy gain in this study—returns
                                               correct programs the standard extractor discards through robust extraction and public-test
                                               signature alignment; it does no harm (b10 =0), is leakage-free, and lifts DeepSeek-Coder-1.3B
                                               by +12 tasks on HumanEval+ (p=2.4 × 10−4 ). An adaptive consensus early-stop (ACE) is a
                                               calibrated compute-saving control, not a new adaptive-compute method: ≈ 19% saving at a
                                               zero-harm operating point (Hoeffding–Bentkus bound, not corrected for τ selection), with larger
                                               savings forgoing it. The M1 gain and the selection negative both replicate on HumanEval+
                                         ∗
                                             Corresponding author. PythaLab, Yıldız Technical University, Istanbul, Turkey. Email: miscan@yildiz.edu.tr.


                                                                                                1
      and MBPP+ across three model cells (ACE is reported on the local benchmark only), with M1
      stronger for the weaker model. The practical lesson is specific: for a frozen small code model,
      fix the harness (extraction, serving, and the compute schedule) and measure coverage before
      attributing failures to semantic post-hoc reasoning over the existing samples.

Keywords: frozen small code models; post-hoc operators; Popperian falsification; Best-of-N
sampling; do-no-harm certificate; expression-layer recovery; test-time compute allocation; code-
generation evaluation.


1    Introduction
Small language models are an increasingly practical target for local code generation. Models in
the 0.5–1.5 B parameter range run without quantization on a single consumer GPU, respond in
seconds, and never leave the machine, which makes them attractive for offline assistants, classroom
tooling, and privacy-constrained deployments. Their competence is measured by the pass@k protocol
introduced with Codex and HumanEval (M. Chen et al., 2021) and extended by MBPP (Austin et al.,
2021), and code-specialized small models such as DeepSeek-Coder (Guo et al., 2024) and Qwen2.5-
Coder (Hui et al., 2024) now bring real synthesis to this range. Their weakness is equally well
known: without large-scale fine-tuning they fail on edge cases, misread underspecified prompts, and
emit plausible-looking but subtly wrong programs. Best-of-N (BoN) sampling—draw k candidates,
return the first that passes the visible tests—raises pass rates but saturates quickly.
    A tempting response is to wrap the frozen model in a smarter post-hoc operator: a procedure
that re-processes the model’s own samples, without changing a single weight, to recover a correct
answer. Four families have been tried, and each has a documented failure mode at small scale.
Selection picks a better sample after generation: self-consistency marginalizes over reasoning paths
(X. Wang et al., 2023), and its code analogue is execution agreement—MBR-Exec ranks by the
mutual agreement of execution behaviour (Shi, Fried, Ghazvininejad, Zettlemoyer, & Wang, 2022),
CodeT scores candidates against model-generated tests (B. Chen et al., 2023), and Coder-Reviewer
reranks by a generation-likelihood criterion (T. Zhang et al., 2023). Verification tries to predict
correctness directly: tool-interactive critique (Gou et al., 2024) and process reward models (Lightman
et al., 2024) add an external check, yet large language model (LLM) verification of code against
a specification is systematically unreliable (Jin & Chen, 2025), and the binding bottleneck is
fault-revealing test generation, not synthesis (Bansal et al., 2026). Repair rewrites a failed attempt:
Self-Debug (X. Chen, Lin, Schärli, & Zhou, 2024), Self-Refine (Madaan et al., 2023), and Reflexion
(Shinn et al., 2023) feed execution traces or self-critique back into a revision—but intrinsic self-
correction does not reliably improve outputs without an external signal (J. Huang et al., 2024;
Valmeekam, Marquez, & Kambhampati, 2023), can degrade them (Q. Zhang et al., 2025), and
the self-generated-test variant inherits a documented oracle bias (X. Chen et al., 2025). Test-time
compute allocation spends the budget adaptively: it can beat flat Best-of-N on capable models
(Snell, Lee, Xu, & Kumar, 2025), but on code the online difficulty-adaptive variant can drop below


                                                    2
best-of-k (Damani, Shenfeld, Peng, Bobu, & Andreas, 2025).
   The most principled versions of these operators are Popperian: rather than confirm a candidate,
they attack it with the most severe test they can construct and keep what survives (Popper, 1959,
1963). Severity has a precise error-statistical meaning—a claim is corroborated only to the extent
that it has passed a test it would probably have failed were it false (Mayo, 2025; Mayo & Spanos,
2006)—and in software engineering the same intuition appears as falsification-driven verification
(Groce, Ahmed, Jensen, & McKenney, 2015). The closest agentic operationalization, POPPER,
validates a fixed natural-language hypothesis by sequential severe tests under strict Type-I control
(K. Huang et al., 2025); the closest engineering competitor wraps each model call in a verified
contract (Banerjee et al., 2026); and the REFUTE benchmark asks directly whether models can
create counterexamples to incorrect solutions, finding that even strong reasoning agents succeed
on < 9% of cases (Sinha et al., 2025). The appeal of the program is real: it is cheap (no training),
grounded (execution is a trustworthy oracle), and it rests on a well-established epistemology in
which knowledge grows by refutation rather than accumulation.
   This paper reports what happened when that program was applied, repeatedly and adversarially,
to a frozen small code model, and gives a calibrated account of why it did not improve it, together
with the two places it did. It is the companion to an earlier study (İşcan, 2026) that asked whether
attaching Popperian vocabulary to a coding agent’s prompt improves its code, and found that the
gains came from scaffold structure, not from the Popperian content: naming severe tests did not
help beyond a labels-only control. That paper’s explicit next step was to “turn the method on a
sharper target”—a skill built around executable falsification, “generating, running, and selecting
against real counterexamples rather than rubric impressions.” The present work is that successor:
it replaces the LLM-judge with a deterministic execution oracle and asks the sharper question
directly—does any executable post-hoc falsification operator make a frozen small model write more
correct code? Because code benchmarks can leak into pre-training (Matton et al., 2024), any
self-authored benchmark is treated as suspect, and replication is run on the augmented HumanEval+
and MBPP+ suites, whose hidden tests expose plausible-but-wrong programs the original suites
miss (J. Liu, Xia, Wang, & Zhang, 2023; X. Liu et al., 2025).
   Across twenty-six distinct operators spanning the standard families—selection, verification,
repair, counterexample search, version-space elimination, portfolios, sound vetoes, and generation
conditioning—none improves held-out accuracy over BoN at matched compute. What makes the
result worth reporting is that the negative is mechanistic and measured. Three forces, each quantified
on cached candidate pools, jointly explain every null:
• Coverage wall. The weak model’s hard-task failures are systematic, not stochastic: deeper
   sampling does not rescue them. At k=16 on a held-out hard set, 16/30 tasks still produce no
   hidden-correct candidate at all—reproducing a published online-code negative for difficulty-
   adaptive allocation (Damani et al., 2025).

• Capability scissors. A competent generator leaves almost no discriminable error among the
   candidates that already pass the visible tests; whatever gain is available lands in pass@1/coverage,

                                                  3
   not in the operator. The gap sharpens with a stronger model and with explicit reasoning.

• Near-empty consensus trap. The exact regime a leakage-free selector needs—a visible-passing
   majority that is hidden-wrong while a correct alternative sits in the pool—almost never co-occurs.
   On two purpose-built, sound-veto-capable trap benchmarks the model emitted the triggering bug
   on 0/10 and 2/16 tasks, never as the consensus majority; and ≈ 83% of the model’s real bugs
   are invisible to any sound metamorphic relation.
These mechanisms have a sharp statistical corollary that is made explicit and proved: a distribution-
free finite-sample do-no-harm certificate cannot bound a population harm rate at ≤ α even at zero
observed harm unless the sample is at least n ≥ ⌈log δ/ log(1 − α)⌉, which is 45 at α=0.05, δ=0.10
(Proposition 1). Every “provable do-no-harm” claim made on a ≤ 32-task set in this program
is therefore under-powered by construction—an observation that disciplines the present positive
results.
   Two operators do beat BoN, and the reason is that they do not operate over the model’s semantic
output space, where the three mechanisms take effect.
• Expression-layer recovery (M1). A large fraction of a weak model’s apparent failures are
   correct programs the standard extractor discards—a wrong function name (def Add where the
   test calls add), prose-wrapped code, a malformed fence, multiple definitions. A robust multi-
   strategy extractor plus signature alignment (rename the single defined function to the public-test
   name) recovers this code. Applied only when the standard pipeline finds no visible-passer—so
   it displaces no standard public-passing success—M1 does no harm (b10 =0 on every cell) and
   is leakage-free (the name comes from the public tests, never the reference), at zero additional
   generation. It is the only deployed accuracy gain in the program.

• Compute reduction: adaptive consensus early-stop (ACE). BoN commits on the first
   visible-passer, so the rest of the budget is wasted; an adaptive early-stop recovers that compute.
   ACE is reported with deliberate calibration: the zero-harm operating point (b10 =0, with a
   Hoeffding–Bentkus Learn-then-Test calculation (Angelopoulos, Bates, Candès, Jordan, & Lei,
   2021)) saves only ≈ 19% of samples on the competent cell; the larger ≈ 64% saving sits at an
   aggressive stop that incurs measurable regressions (b10 =2) and does not reach the bound. The
   compute win is real but modest, and it collapses on the weak model for the same coverage-wall
   reason.
   A measurement paper built on a self-authored benchmark faces an obvious objection: the
instrument may be the result. The M1 accuracy gain and the selection negative are therefore
replicated on two standard external benchmarks (HumanEval+ and MBPP+) across three model
cells (J. Liu et al., 2023); ACE is reported on the local benchmark only. M1 transfers more strongly
than on the self-authored benchmark (DeepSeek-Coder-1.3B: 29 → 41, +12 tasks, p=2.4 × 10−4 on
HumanEval+; 128 → 161, +33, p=1.2 × 10−10 on MBPP+; b10 =0 throughout; on the instruction-
tuned Qwen cells (1.5B/0.5B) the gain is small and ns, +1 to +4), and the “no leakage-free selector
beats BoN” negative replicates on every cell: the selector-agnostic headroom is 0 (the consensus

                                                 4
trap is empty), or where it is positive (6–17 across the five remaining cells) no realizable leakage-free
selector captures it (net ≤ +3, never significant).
    The contributions separate three axes and are the following.
1. A matched-compute, leakage-free measurement study of twenty-six semantic output-space
    operators (Definition 1) for frozen small code models under a single execution oracle, with a
    do-no-harm bar (b10 , McNemar) fixed in advance. The headline is a mechanistic negative for
    semantic post-hoc accuracy: none beats BoN at matched compute on the tested cells (Results
    and Discussion).

2. Three measured mechanisms—coverage wall, capability scissors, near-empty consensus trap—
    that jointly explain the negative, with a proven finite-sample power corollary that bounds what
    any do-no-harm certificate can claim (Proposition 1 and Lemma 1, measured in the Discussion).

3. An expression-layer recovery (M1), on a different axis from the twenty-six: a harness/extraction
    fix that recovers correct-but-mis-expressed code and is the only deployed accuracy gain in this
    study (do-no-harm, leakage-free; in the Results). It is not a semantic operator.

4. A calibrated compute-saving control (ACE), not a new adaptive-compute method: early
    stopping at no measured accuracy cost, with a Hoeffding–Bentkus bound at the selected operating
    point (the zero-harm saving stated honestly against the aggressive saving; in the Results). It
    saves compute, not accuracy.

5. An external replication on HumanEval+ and MBPP+ of the M1 accuracy gain and the
    selection negative across three model cells, closing the self-authored-benchmark gap (in the
    Results).
    The remainder of this paper is organized as follows. Section 2 presents the post-hoc operator
framework (the leakage-free, matched-compute evaluation protocol and its formal do-no-harm test),
together with the twenty-six benchmark methods under study and the two surviving operators.
Section 3 reports the measurement study: the experimental setup, the accuracy survey against BoN,
the two survivors, and the external replication on HumanEval+ and MBPP+. Section 4 weighs
the result against prior post-hoc and falsification-based methods and locates the three measured
mechanisms that account for it. Section 5 concludes.
    All of this is read narrowly, and nulls and negatives are reported as first-class results. The
intended takeaway is a design rule, not a no-go theorem: for a frozen small code model the dominant
addressable loss is in the harness (extraction, serving, compute schedule), not in clever post-hoc
reasoning over the model’s semantics, and accuracy claims for such operators should be interpreted
in light of the coverage wall.


2    Method
A post-hoc operator sits between a frozen generator and deployment, the setup shown in Figure 1.
The generator draws several candidate programs for a task; the operator inspects that pool together

                                                   5
                                                   Frozen generator M
                                                   (≤ 1.5B, 6 GB GPU)
                                                                                                 k = 8 samples
                                                                                                    T = 0.8
                                                                                                  shared seeds

                                                  Shared candidate pool
                                                 P = (c1 , . . . , ck ), k = 8

                                     same pool                               π, Tpub only



                      Best-of-N baseline                                         Post-hoc operator A
                 first public-passer under Tpub                                   cA = A(π, Tpub , P )
                                                                                  b
                             b
                             cBoN                                          select / verify / repair / veto


                                     Leakage-free / matched compute: A reads only
                             bcBoN    (π, Tpub , P ); no Thid , reference, or extra calls b
                                                                                          cA



                                                 Hidden execution oracle
                                          run Thid on both deployed outputs




                                    Paired do-no-harm test vs. BoN
                     b10 = #{BoN = 1, A = 0} harm, b01 = #{A = 1, BoN = 0} gain
                                      exact McNemar; pre-registered bar b10 = 0




Figure 1: The post-hoc operator setup. A frozen generator M draws a shared candidate pool P = (c1 , . . . , ck );
a leakage-free, matched-compute post-hoc operator A reads only the prompt and public tests Tpub —never the
hidden tests Thid or a reference solution—and returns one program ĉ to deploy. Every operator is judged
against the Best-of-N (BoN) baseline by the do-no-harm test fixed in advance (b10 harm / b01 gain, exact
McNemar, bar b10 =0).


with only the information available at deploy time—the prompt and the visible tests, never the
hidden tests or a reference solution—and returns one program to run. It changes no weights and, in
the matched-compute regime enforced here, draws no extra samples beyond the baseline’s budget.
The paper’s question is whether any such operator—however it selects, verifies, repairs, eliminates,
or conditions generation—returns a hidden-correct program more often than the trivial first-passer
baseline. The question is fixed precisely—the pool, the operator, and the do-no-harm test—and
every method under test is then catalogued, each with its rule and equation (§2.1).
Formal setup. A task is a triple t = (π, Tpub , Thid ) of a prompt π, a set of public (visible)
tests Tpub , and a set of hidden tests Thid , each test an (input, expected-output) pair run in a
network-isolated subprocess; the pass predicate is pass(c, S) = 1[ c satisfies every test in S ], so a
program c public-passes when pass(c, Tpub )=1 and is counted correct when pass(c, Thid )=1 (on the
external suites Tpub is the EvalPlus base suite and Thid the augmented plus suite (J. Liu et al.,

                                                              6
2023; X. Liu et al., 2025)). For budget k and temperature T the frozen generator M produces a
                                                                                                      
pool P = (c1 , . . . , ck ) with ci ∼ M (π; T ) and per-sample seed seedi = int SHA256(id_i)[:8], 16 , so
the pool is reproducible and shared byte-for-byte across all operators compared on it. A post-hoc
operator is a map A : (π, Tpub , P ) 7→ ĉ returning one program ĉ to deploy (an element of P , or a
program rewritten from P ); it is leakage-free when it is a function of (π, Tpub , P ) alone, never reading
Thid or a reference solution, and matched-compute when it issues the same number of generator calls
as the baseline (a repair or extra draw is charged against the baseline budget, so all comparisons
here are matched-compute by construction). The baseline is Best-of-N (BoN), which returns the
first public-passer in pool order, ĉ = ci⋆ with i⋆ = min{i : pass(ci , Tpub )=1} (a deployed fallback
if none passes), and is itself leakage-free. Each operator is judged against BoN on n tasks by the
paired off-diagonal counts (Fagerland, Lydersen, & Laake, 2013)

      b10 = #{t : BoN passes, A fails} (harm),          b01 = #{t : A passes, BoN fails} (gain),

with net gain b01 − b10 . The do-no-harm bar, fixed before the deciding runs, is b10 =0; a gain (a
directional hypothesis) is judged by the exact one-sided McNemar (binomial) test, which at b10 =0
gives p = 2−b01 and so reaches p < 0.05 at b01 ≥ 5, with a stricter net-≥ 6 floor (the two-sided
exact threshold) declared in advance. A comparison without a hypothesized direction (for instance,
a leakage-free selector against BoN) instead uses the two-sided exact test. Matched compute is
essential here, since an unmatched “gain” is just one more sample.
The do-no-harm bar drives every claim, so its statistical reach must be fixed up front. At b10 =0 the
bar is an observation, not yet a population guarantee; the next proposition bounds when it can
become one.
Proposition 1 (Finite-sample floor for distribution-free do-no-harm). Let harm be Bernoulli with
unknown rate r and suppose 0 harm events are observed in n i.i.d. trials. The exact one-sided
upper confidence bound at level δ is r ≤ 1 − δ 1/n , so certifying r ≤ α needs 1 − δ 1/n ≤ α, i.e.
n ≥ ⌈log δ/ log(1 − α)⌉. At α=0.05, δ=0.10 this is n ≥ 45.
Proof. P(0 harm in n) = (1 − r)n ; the 1 − δ upper bound is the largest r with (1 − r)n ≥ δ, i.e.
r = 1 − δ 1/n . Setting this ≤ α and solving gives the bound, and ⌈log 0.10/ log 0.95⌉ = 45. □
Corollary 1. Any zero-harm result on a ≤ 32-task benchmark (e.g. the sound-veto capstone and
metamorphic selection on Substrate-W) is under-powered: even at b10 =0 a distribution-free Hoeffding–
Bentkus certificate cannot issue. Only n ≥ 45 results (the ACE compute do-no-harm bound in the
Results; HumanEval+ at n=164) can carry one, so every ≤ 32-task do-no-harm claim is treated as
suggestive, not proven—a discipline applied to the present positives as much as to the operators that
are rejected.

2.1    Benchmark methods
Every method under test is catalogued here. The twenty-six operators appear in pipeline order—a
refute-first spine (#0), then selection (#1–5), verification (#6–8), repair (#9–14), elimination/veto

                                                    7
Table 1: Method-wide notation and fixed constants. Every value appears in the text and is transcribed here
for reference; externally fixed choices carry their source.

    Symbol / setting     Meaning                                            Value / source
    k                    pool size (samples per task)                       8
    T                    sampling temperature                               0.8
    |Π|                  probe-bank size (deterministic inputs)             ≤ 24
    dim ϕ                code-embedding dimension                           1536
    α                    target harm rate (do-no-harm)                      0.05
    δ                    certificate confidence level                       0.10
    nmin                 finite-sample floor, Proposition 1                 45
    τ                    ACE commit threshold (reported operating point)    4
    αlin                 LinUCB exploration coefficient                     1
    wavelet              basis / level / pad length                         db4 / 4 / 64
    PLURAL               programme temperatures                             {0.6, 0.6, 1.0, 0.2, 0.6}
    certificate          Learn-then-Test bound, Eq. (1)                     Angelopoulos et al. (2021)
    suites               augmented external benchmarks                      J. Liu et al. (2023)


(#15–17), generation conditioning (#18–23), and compute allocation (#24–25)—followed by the two
survivors; each entry gives the rule or score, its equation, and the claim it makes against BoN, and
verdicts with headline numbers are in the Results and Appendix A. Several methods share one leakage-
free execution latent: a deterministic probe bank Π(t) of at most 24 inputs (public-test arguments
plus type-aware mutations) on which each candidate c is executed in the sandbox to a fingerprint
vector fp(c) over Π, each coordinate one of {repr[:200], ERR:⟨type⟩, NOFUNC, NOCODE, TIMEOUT}, at
no generator cost. Two notions of agreement recur and must not be conflated: the per-probe plurality
(the most common fingerprint) and the strict majority (a value with count ≥ 2 and more than half
the clean candidates). Three operators issue a finite-sample certificate from the Hoeffding–Bentkus
(HB) Learn-then-Test bound (Angelopoulos et al., 2021),
                                   n                                                   o
                  HBp (r̂; n) = min 1, e−n KL(min(r̂,α) ∥ α) , e · BinomCDF(⌈nr̂⌉; n, α) ,               (1)

where r̂ is the observed harm rate; the certificate issues iff HBp ≤ δ, which by Proposition 1 needs
n ≥ 45 at (α, δ)=(0.05, 0.10). The three spectral probes share one feature map ϕW , defined with its
method below. The method-wide notation and the fixed constants are collected in Table 1.
   The survey is organized around one distinction, fixed here and used throughout.

Definition 1 (Semantic output-space operator). An operator is semantic output-space if it selects,
verifies, repairs, eliminates, or conditions generation based on candidate code meaning, execution
behavior, repair traces, or learned correctness features. The twenty-six operators surveyed below
(#0–#25) are all of this kind. The two survivors act outside this space and are analyzed separately:
expression-layer extraction (M1) acts on how the code is written, and compute scheduling (ACE)
acts on the sampling budget.

   Selection operators share one governing theory, which is stated first.



                                                     8
Definition 2 (Consensus trap). A task is in the consensus trap for pool P if (a) the public-passing
majority of P is hidden-wrong and (b) some candidate in P is hidden-correct.

Lemma 1 (Consensus-trap headroom under a majority-symmetry assumption). Let S be a leakage-
free selector (a function of (π, Tpub , P ) alone) that returns a public-passer, and assume the majority-
symmetry regime in which, on tasks whose public-passing majority is hidden-correct, deviating from
that majority does not raise expected accuracy (off-trap deviation is, in expectation, weakly harmful).
Under this assumption S can net-gain over BoN only on consensus-trap tasks (Definition 2): on a
non-trap task it cannot turn a BoN failure into a success without, on the matched population of
non-trap tasks, turning some BoN success into a failure. The expected net gain is then bounded by
the trap’s probability mass, E[b01 − b10 ] ≤ P[ task ∈ trap ].

Proof sketch. If no candidate is hidden-correct (Definition 2(b) fails) the task is unsolvable by any
selection rule. If the public-passing majority is hidden-correct (Definition 2(a) fails), the symmetry
assumption makes any deviation from the majority weakly harmful in expectation, while a rule
that never deviates is BoN-consensus and gains nothing. So the only tasks on which a leakage-free
selector can net gain are trap tasks. □
This is a diagnostic lemma, not a general impossibility theorem: it holds under the stated majority-
symmetry assumption and decomposes where a leakage-free selector’s headroom can lie, rather
than proving that every such selector must fail off-trap. The assumption is plausible for execution-
clustered pools: when the public-passing majority is hidden-correct it is the modal-correct cluster, so
deviating from it selects a minority cluster that is correct strictly less often in expectation. Its force
in this study is empirical—the consensus-trap mass is measured to be near zero (in the Discussion),
so the right-hand bound is near zero on the cells tested.

• Refute-first pipeline (REFv3, #0). The baseline spine: draw the pool, re-prompt the model
   to refute its own candidate against Tpub and revise, then deploy the first public-passer; a family
   router sends counterexample and abstention tasks to the search and abstention arms and the
   remainder to refute→revise. Procedural (no closed-form score). Claim: executable self-refutation
   lifts the pass rate over plain BoN.

• Execution-consensus (MBR-Exec, #1) (Shi et al., 2022). Among public-passers, take the
   per-probe plurality fingerprint majj and select the candidate of greatest agreement with it,

                                                                 P   h             i
                                                            1
                        ı̂ = arg max agreei ,     agreei = |Π|   j 1 fpi (j) = majj .
                                  i

   This is the minimum-Bayes-risk-over-execution instance: a plurality vote over deterministic
   execution fingerprints, not over model-generated tests. Claim: E[b01 − b10 ] > 0, which by
   Lemma 1 requires the trap to carry positive mass.

• Embedding-medoid (CEMS, #2). Embed each public-passer’s code to xi ∈ R1536 and return



                                                     9
  the medoid—the candidate of least total cosine distance to the rest:

                                      P
                       ı̂ = arg min       j̸=i dcos (xi , xj ),   dcos (u, v) = 1 − ∥u∥u·v∥v∥ .
                                 i

  Claim: the central candidate is hidden-correct more often than BoN’s first passer.

• Behavioural-trace rerank (BTR, #3). The execution twin of CEMS: replace the embedding
                                                                                             P
  by the fingerprint and minimise total Hamming distance, ı̂ = arg mini                           j̸=i hij   with hij =
  P
     k 1[fpi (k) ̸= fpj (k)]; a severity-weighted variant weights probe j by 1 − (plurality countj /n) so
  that discriminating probes count more. Claim: behavioural centrality beats first-passer selection.

• Verisimilitude (VRS, #4) (Niiniluoto, 2014). Rank by a Popperian truthlikeness over probes.
  With CtT and CtF the content of the severe probes a candidate survives and fails and the count
  proxy Ct(S) = |S|/(|S| + 1),

                                                     CtT − CtF
                                      Vs(c) =                  ∈ [−1, 1],
                                                     CtT + CtF

  with Vs=0 for a tautology and Vs=−1 when a clean-consensus probe makes the candidate crash;
  select arg maxc Vs(c). Claim: higher truthlikeness tracks hidden correctness.

• Metamorphic selection (MR, #5). On Substrate-W, refute any candidate that cleanly violates
  a declared sound relation from the library {determinism f (x)=f (x), idempotence f (f (x))=f (x),
  sortedness, length, multiset preservation, membership out ⊆ in, permutation- and inverse-
  consistency g(f (x))=x}; a crash or timeout counts as a non-violation, so the filter never refutes
  a correct program. A construction gate enforces soundness (a known-bad must fail Thid and
  violate a relation; a known-good must satisfy all). Claim: sound metamorphic agreement isolates
  the hidden-correct candidate.

• Where selection trusts the pool’s own agreement, verification instead learns or measures a
  correctness signal directly. Learned verifier (LCV, #6). A logistic regressor of hidden
  correctness on the 1536-d code embedding ϕ, g(ϕ) = σ(w⊤ ϕ + b), fit with balanced classes
  under strict per-task GroupKFold (no task in both train and test); deploy arg maxi g(ϕi ) among
  public-passers. Claim: the area under the ROC curve satisfies AUC(g) > 12 leakage-free, usefully
  enough to rerank.

• Fingerprint verifier (XFV, #7). The same logistic g on an 8-dimensional execution feature ϕ =
  (severity-weighted and plain consensus agreement, error fraction, timeout/no-function fraction,
  Hamming distance to the behavioural medoid, behavioural diversity, and the mean severity on
  agreeing and on disagreeing probes), standardised on train folds. Claim: execution features
  separate hidden-correct above chance, tested against a label-permutation null.

• Latent abstention (LEA, #8). Force k candidates under a no-refusal prompt, embed them, and
  abstain when the mean pairwise cosine dispersion d¯ of the pool exceeds a train-fitted threshold

                                                          10
                   P      ¯
  τ ⋆ = arg maxτ      i 1[(di > τ ) = ai ] (ai the abstain target), otherwise answer with the medoid.
  Claim: dispersion gates ambiguous tasks without discarding solvable ones.

• When no candidate is right, repair tries to make one. Self-debug (M2, #9) (X. Chen et
  al., 2024). One repair round, c′ = M (repair(t, c, e)), the prompt branched by severity—a
  close candidate (public-passes, hidden-fails) is asked to fix only the edge case, a far candidate
  (public-fails) to fix the basic failure—given the executed error e. Procedural. Claim (matched
  compute): the repaired candidate beats a fresh draw.

• Bandit repair router (BRR, #10). A LinUCB contextual bandit selects one of four repair
  arms {regenerate, error-trace, edge-case, refute-revise}. Keeping per-arm Aa (init the identity I)
  and ba (init 0) with θa = A−1
                             a ba , it pulls and updates
                                              q
                    ⋆
                   a = arg max    θa⊤ x + α       x⊤ A−1
                                                      a x,   Aa⋆ += xx⊤ ,       ba⋆ += r x,
                              a

  where the context x is a fixed Gaussian random projection of the normalised embedding of
  [prompt + failing code + error] with a public-pass flag and a constant bias term appended,
  the reward is r = 1[repair hidden-passes], α=1, evaluated by counterfactual replay. Claim: the
  learned router beats the best fixed arm.

• Counterexample-guided repair (CEGIS-R, #11). Build an ensemble pseudo-oracle from the
  public-passers; a probe j is a counterexample when the target crashes while a clean plurality
  agrees, or disagrees with a confident plurality:
                                                                                            plurality countj
   CEj ⇐⇒ ¬ clean(cj ) ∧ clean(majj ) ∨ cj ̸= majj ∧ conf j ≥ 0.6 ,               conf j =        #voters      .

  Here clean(·) marks a non-error fingerprint and majj the per-probe plurality of the shared
  latent above. Inject “f (x)=A, want B” and regenerate (up to two rounds). Claim: a concrete
  counterexample repairs better than a generic re-ask.

• Severity-conditioned regeneration (SERA, #12). Regenerate conditioned on a severe found
  counterexample and compare against a generic re-ask and a confirmation placebo through the
  per-task contrast
                           τ = pass(c | severe CE) − pass(c | generic re-ask) ,

  the load-bearing test being pass(severe) > pass(placebo). Claim: severity itself, not merely a
  concrete anchor, drives the gain.

• Prompt-normalisation (M3, #13). Inject the public-test signature and its input/output
  examples into the prompt and draw one sample. Procedural (no score). Claim: matching the
  weak model’s expected format lifts the single-sample pass rate.

• Thinking-iteration (TIRF, #14). Compare a visible-thinking mode to NoThink-BoN at equal


                                                      11
  compute: with the measured latency ratio R a thinking depth n is matched to NoThink depth
  ⌊nR⌋, and each arm’s pass@k uses the exact finite-pool hypergeometric
                                                          !      !!
                                          a     d . n
                                pass@k =     1−                       ,
                                         a+b    k   k

  with a/b the hidden-winning/-failing public-passers, d the non-passers, and pool size n=8 here.
  Claim: thinking beats NoThink at equal compute.

• Elimination keeps only what survives refutation. Version-space elimination (PAVER, #15).
  Treat the public-passers as a hypothesis space and delete the refuted ones: refuted(c) =
  mr(c) ∨ crash(c) (sound policy) or additionally ∨ diff(c), disagreement with the strict majority
  (full policy); deploy the first survivor, else BoN. Soundness is measured by the false-refutation
  rate FRR (the fraction of hidden-correct candidates it eliminates), and probe severity by the
                        P nv
  per-probe entropy −    v N log2 N . Claim: elimination raises accuracy do-no-harm.
                                  nv


• Programme portfolio (PLURAL, #16) (Lakatos, 1968). Run five generation programmes
  {BoN, schema, diversity, simple, repair} at fixed temperatures {0.6, 0.6, 1.0, 0.2, 0.6} and deploy
  by a fixed tiebreak order. Procedural. Claim: the portfolio beats single-programme BoN—tested
  decisively against BoN’s own pass@20 coverage.

• Conformal sound veto (SCRC, #17) (Angelopoulos et al., 2021). Keep the largest fingerprint
  cluster as an anchor and override it only if the anchor cleanly violates a sound metamorphic
  relation and a clean alternative cluster exists; certify the harm rate against full consensus by
  the shared HBp bound of Eq. (1) on the loss Li = 1[anchor correct ∧ vetoed ∧ ¬ SCRC correct].
  Claim: a sound veto raises accuracy with b10 =0 and a finite-sample certificate.

• Conditioning acts earlier, shaping the pool the operators see. Schema hint (PRAXIS, #18).
  Prepend a family-matched algorithmic-schema hint to the prompt, with a wrong-family hint as
  the placebo and decoding fixed so that only the hint varies. Procedural. Claim: the matched
  hint beats both vanilla and the mismatched placebo (∆ ≥ 0.03, b10 ≤ 1).

• Verified-exemplar (MNEMON, #19). Prepend a verified (public-passing) same-family ex-
  emplar solution to the prompt—an unrelated-family exemplar is the placebo and a no-code
  preamble the scaffold—and deploy by public-probe consensus. Procedural. Claim: relevance
  beats scaffold: the matched exemplar must beat both vanilla and the placebo.

• Decoding-diversity union (POLYGEN, #20). Generate under diverse decoding profiles
  (min-p, typical-p, hot-broad) and select by the modal public-probe cluster, ĉ = the first member
  of arg maxcluster |cluster|, falling back to BoN when the diverse pool yields no public-passer.
  Claim: diversity widens coverage the selector can convert, as plan-level search does for capable
  models (E. Wang et al., 2025).



                                                12
• Wavelet probe (WAVE-RL-F, #21). Ask whether a multi-scale wavelet basis of a candidate’s
  code signal predicts hidden correctness beyond the embedding. From the level-4 db4 transform
  {A, D1 , . . . , D4 } = wavedec(s) (signal padded to length 64), with detail-band energies EDj =
                                                    P                                        P
  ⟨Dj , Dj ⟩, relative detail energies πj = EDj /        j EDj , and wavelet entropy H = −   j πj log πj ,
  the feature map collects
                                                                                 
                      ϕW (s) = log(1+EDj ), log(1+EA ), πj , H, band sums ,

  the approximation A entering only as the separate log-energy log(1+EA ). GO iff the grouped-
  CV AUC(emb+ϕW ) − AUC(emb) ≥ 0.03 at p < 0.05 among public-passers. Claim: ϕW adds
  discriminative signal.

• Frequency probe (FREQ-RL, #22). The same ϕW gate over richer machine-space channels—
  token type, operator family, AST node type, keyword rhythm, and character class—each an
  integer-coded sequence transformed by the wavelet basis. Claim: richer spectral channels add
  signal beyond the embedding.

• Exec-behaviour differential (FREQ-RL v2, #23). On auto-generated inputs build each
  candidate’s self-behaviour channels (crash, exception, output length and change, type) and its
  deviation from a leave-one-out consensus and a known-good reference; test whether deviation
  predicts hidden failure y = 1 − pass(c, Thid ) above chance and whether it survives at deployment.
  Claim: behavioural deviation both detects and repairs hidden failure leakage-free.

• Compute allocation changes not the pick but where the sampling budget is spent. Adaptive
  allocation (SCARF, #24). At a fixed total budget b·M , greedily give the next sample to the
  task of maximal marginal pass-gain (priority a difficulty signal ϕ̂, an oracle, or uniform), with
                                                                              P
  per-task success the exact finite-pool hypergeometric and the invariant       i ni = b·M enforced on
  every replay. Claim: difficulty-aware reallocation beats flat BoN at equal compute.

• Easy→hard reallocation (ACE+, #25). Lock the consensus-decided easy tasks at the ACE
               P
  stop, free   i (kbase − ni ) samples, and reinvest them on unresolved tasks up to k=16 by difficulty
  1 − m1 /|prefix| (leftover returned to the locked tasks), at matched total compute; this reproduces
  the online-allocation negative (Damani et al., 2025). Claim: reallocation lifts accuracy at
  matched compute.

• Expression-layer recovery (M1, survivor; Algorithm 1). On tasks with no standard public-
  passer, robustly re-extract a single function from the candidate and rename it to the public-test
  name (the most-called bare identifier in the asserts) by a bare-identifier substitution that leaves
  attribute access intact, then deploy if it now public-passes. It fires only off the standard
  pipeline, so it cannot displace a standard public-passer (b10 =0); the name comes from public
  tests (leakage-free); zero extra generation. Result: the program’s only deployed accuracy win (in
  the Results).


                                                    13
Algorithm 1 M1 expression-layer recovery (do-no-harm, leakage-free).
Require: task t, public tests Tpub , candidate pool P = {c1 , . . . , ck }, standard extractor Estd
 1: ai ← Estd (ci ) for all i                                                      ▷ standard extraction
 2: if some ai passes Tpub then return BoN first public-passer over a1 , . . . , ak ▷ standard handles
    it: never altered
 3: end if
 4: name ← most-called bare identifier in Tpub      ▷ signature from public tests only (leakage-free)
 5: for i = 1 . . . k do
 6:     bi ← RobustExtract(ci )                             ▷ any def, prose-stripped, fence-tolerant
 7:     if bi defines exactly one function f ̸= name then bi ← Rename(bi , f → name) ▷ signature
    alignment
 8:     end if
 9:     if bi passes Tpub then return bi                                                     ▷ recovered
10:     end if
11: end for
12: return BoN fallback           ▷ unchanged; b10 =0 since this branch only runs when no ai passed

Algorithm 2 ACE adaptive consensus early-stop (compute reduction).
Require: task t, sampler M , public tests Tpub , budget k, commit threshold τ , execution fingerprint
    fp(·)
 1: for n = 1 . . . k do
 2:      draw and grade cn ← M (t); let Qn be the public-passers among c1 , . . . , cn ▷ one sample per
    step
 3:      cluster Qn by execution fingerprint fp; let m1 ≥ m2 be the two largest cluster sizes
 4:      if Qn ̸= ∅ and m1 − m2 > k − n or m1 ≥ τ ∧ m1 > m2 then
 5:          return embedding medoid of the modal cluster, with compute = n ▷ lock-stop / τ -stop
 6:      end if
 7: end for
 8: return full-budget consensus pick: modal-cluster medoid over all k public-passers (BoN first-
    passer if none), compute = k
    Reported operating point: the smallest τ at which the early-stop incurs no measured harm
    (b10 =0) relative to the full-budget consensus pick (here τ =4), read with the Hoeffding–Bentkus
    Learn-then-Test calculation of Eq. (1) at n ≥ 45.


• Adaptive consensus early-stop (ACE, survivor; Algorithm 2). Cluster the public-passers
   by execution fingerprint with modal cluster sizes m1 ≥ m2 and stop at the first depth n that is
   decided—lock-stop m1 − m2 > k − n, or τ -stop m1 ≥ τ ∧ m1 > m2 —returning the modal cluster’s
   embedding medoid; bound the harm rate against full consensus by HBp ≤ δ (Eq. (1)) at n ≥ 45.
   The compute saving is 1 − n̄/k. Result: a modest compute reduction with a Hoeffding–Bentkus
   bound at the selected operating point (in the Results).

   The two surviving operators are specified in full as Algorithms 1 and 2; both fire only off the
standard pipeline, so each is do-no-harm by construction, and their measured effects are reported in
the Results.



                                                  14
Table 2: Benchmarks and test data used in the measurement study. Counts are the retained task sizes; for
MBPP+ a determinism gate drops 8/378 tasks (3 order-nondeterministic, 5 non-serializable), leaving 370.
The augmented hidden tests of HumanEval+ and MBPP+ expose plausible-but-wrong programs the original
suites miss (J. Liu et al., 2023; X. Liu et al., 2025); the model cards are Guo et al. (2024); Hui et al. (2024).

 Benchmark                   Role                                          Hidden-test source           Tasks
 FALSIFY-BENCH-local         self-authored, 7 families                     sandboxed canonical exec     52–80
 Substrate-W                 engineered sound-veto-capable                 sandboxed canonical exec       32
 HumanEval+                  external, augmented (J. Liu et al., 2023)     EvalPlus plus                 164
 MBPP+                       external, augmented (J. Liu et al., 2023)     EvalPlus plus                 370


3    Results
All inference runs locally through the Ollama API, and no external call is made during evaluation.
The model cells are Qwen2.5-Coder-1.5B and -0.5B (Hui et al., 2024) and DeepSeek-Coder-1.3B (Guo
et al., 2024), with Qwen3-0.6B/1.7B (thinking and non-thinking) on selected probes, each served on a
single 6 GB consumer GPU. Pools are generated once at k=8, T =0.8, and every operator is analysed
post-hoc over the same cached pools, so cross-operator comparisons share generation noise exactly.
Four benchmarks are used (Table 2): FALSIFY-BENCH-local (52–80 tasks over 7 families: simple
functions, adversarial debugging, root-cause-vs-symptom repair, ad-hoc rescue, ambiguous-spec
abstention, faulty-oracle doubt, counterexample generation); Substrate-W (32 tasks, engineered so a
sound metamorphic relation could select correctly); and the external HumanEval+ (164 tasks) and
MBPP+ (370 retained, after a determinism gate drops 8/378 tasks with order-nondeterministic or
non-serializable canonical outputs) (J. Liu et al., 2023). Ground truth is established by sandboxed
execution of the canonical solutions; the EvalPlus adapter was independently falsified on six checks
on both external suites, including the decisive one that a public-passing-but-wrong candidate is
caught by Thid on every sampled task (fraction 1.000: 25/25 on HumanEval+, 6/6 on MBPP+).
Each operator was specified in advance with a falsifiable claim, a placebo or fair baseline where
one exists, and a decisive confound check before its deciding run, following the design principles for
falsifiable, replicable empirical work (Vranješ et al., 2024); the protocol is summarized in Figure 2.
    No operator over the model’s semantic output space beats Best-of-N (BoN) for accuracy. Table 3
summarizes the verdicts: every operator over that space, spanning selection, verification, repair,
elimination, portfolio, sound veto, and generation conditioning, is null, negative, or falsified against
BoN at matched compute. Two patterns recur. First, operators that looked positive on a first pass
did not survive a single confound check: the research-programme portfolio’s +0.19 over BoN-20
disappeared once BoN’s own pass@20 coverage was computed (0.906, essentially the oracle 0.938)—
the “gain” was BoN’s broken first-passer selection, not the portfolio. Version-space elimination’s +2
tasks came with a false-refutation rate of 0.28 (it eliminated 47/170 hidden-correct visible-passers,
near a coin flip), and it cleared the do-no-harm bar only through a fallback, not through sound
discrimination. Second, the one leakage-free signal that genuinely breached the discrimination
wall—an execution-behavior differential on auto-generated probe inputs, reaching an area under the



                                                       15
                                 One generated cache is reused for every comparison;
                               generation noise is shared byte-for-byte across methods.



                     Generate once                  sample cache
                                                                         Cached shared pools
                    k = 8, T = 0.8                                        Pt = (ct,1 , . . . , ct,k )
                    shared SHA256 seeds                                      one pool per task

                                                                                          same Pt
                           same Pt
                                                                       Operator suite #0–#25
                                                                       post-hoc over the same pool
                    Best-of-N baseline                                   no extra generator calls
                       first Tpub -passer                                 Aj (π, Tpub , Pt ) only
                      from the same Pt                              • pre-registered falsifiable claim
                            b
                            cBoN                                    • placebo / fair baseline
                                                                    • decisive confound check
                                                                       fixed before the deciding run




                                    Do-no-harm scoring against BoN
                 hidden-test outcomes are compared by exact paired McNemar discordances
             b10 = #{t : BoN = 1, Aj = 0} harm, b01 = #{t : Aj = 1, BoN = 0} gain
                       pre-registered bar b10 = 0; effect floor b01 − b10 ≥ 6

                                                            aggregate over tasks



                                   Benchmarks × model cells
                         Benchmarks                           Model cells
               FALSIFY-BENCH-local; Substrate-W;      Qwen2.5-Coder-1.5B / 0.5B;
                HumanEval+ (164); MBPP+ (370)             DeepSeek-Coder-1.3B



Figure 2: The measurement protocol. Each task’s candidate pool is generated once (k=8, T =0.8, shared
SHA256 seeds) and cached; every operator is then run post-hoc over the same pool under a falsifiable claim
fixed in advance, a placebo or fair baseline, and a decisive confound check fixed before the deciding run, and
is scored against Best-of-N (BoN) by the exact paired McNemar discordances (b10 harm, b01 gain, bar b10 =0,
net ≥ 6) over the four benchmarks and the model cells.


curve (AUC) of 0.798 for predicting hidden failure—still deployed at ∆=0 (b10 =0): the candidates
it would re-rank already agree with the consensus BoN commits to, so the signal has nothing to act
on. Detecting a bug and being able to do something about it without leakage are different problems,
and only the first is solvable here.
   A representative within-family detail: of 12 hidden-failing candidates on the purpose-built
metamorphic benchmark, only 2 violate any sound metamorphic relation—so on this benchmark
≈ 83% (10/12) of the model’s hidden failures are metamorphic-invisible, and a sound selector (one
that never refutes a correct program) has almost nothing to fire on. Semantic-preserving mutation
exposes such inconsistencies as an auditing signal (Chou, Lwin, & Soremekun, 2026), but not, here,
as a sound selector. This is not a property of these particular relations; it is the empirical shape of

                                                         16
Table 3: Verdicts for the twenty-six post-hoc operators against Best-of-N at matched compute (frozen
small code models). “Do-no-harm” is b10 =0; “significant” is net ≥ 6 at b10 =0. No operator over the model’s
semantics clears both bars; the two survivors act on the expression and compute axes. Full per-operator
numbers and falsification logs are in the released manifests.

      Family                  Representative operators                  #ops    Verdict
      Selection               execution-consensus (MBR-Exec),             5     null (ties BoN)
                              embedding-medoid, behavioural rerank,
                              verisimilitude, metamorphic selection
      Verification            learned P(hid | pub), fingerprint           3     null / below chance /
                              verifier, latent abstention                       net-negative gate
      Repair                  self-debug, bandit router,                  6     null / negative
                              counterexample-guided,                            (compute-confounded
                              severity-conditioned, prompt-norm,                or placebo-tie)
                              thinking-iteration
      Elimination /           version-space elimination, programme        3     falsified (selection
      portfolio / veto        portfolio, conformal sound veto                   artifact / FRR= 0.28)
                                                                                / ∆=0
      Generation              schema hint, verified-exemplar,             6     null / generic-scaffold
      conditioning            decoding-diversity, frequency/wavelet             / NO-GO at feature
                              probe                                             gate
      Compute allocation      adaptive allocation (SCARF),                2     null (∆ ≈ 0;
                              easy→hard reallocation (ACE+)                     reproduces Damani et
                                                                                al. 2025)
      Refute-first pipeline   test-aware refute→revise prompt             1     weak (mostly
                                                                                chain-of-thought,
                                                                                CoT; p=0.23)
     Expression               robust extraction + signature               1     positive
     (survivor)               alignment (M1)
     Compute                  adaptive consensus early-stop (ACE)         1     modest; HB bound
     (survivor)


where a competent small model’s errors live, and the mechanisms that account for it are taken up
in the Discussion.
    Two operators nonetheless beat BoN, and on a different axis than the twenty-six: an expression-
layer recovery (M1), which acts on how the model’s code is written, and a modest compute reduction
(ACE) with a Hoeffding–Bentkus bound at the selected operating point, which acts on the sampling
schedule.
    The first survivor, M1, addresses a loss the capability scissors leaves untouched: that scissors
says there is no discriminable signal among the model’s plausible candidates, whereas M1 attacks a
different loss entirely, namely candidates the model got right but expressed in a form the standard
extractor discards. On DeepSeek-Coder-1.3B, of the candidates the standard Markdown extractor
failed to parse, a large majority contained a valid def; many used a wrong function name (def Add
where the public test calls add) or wrapped the code in prose. None of this is a reasoning failure—it
is an expression/harness failure.
    M1 is a robust multi-strategy extractor followed by signature alignment: parse the required


                                                    17
Table 4: M1 expression-layer recovery vs. the standard extraction pipeline. b10 =0 on every cell by
construction (M1 fires only when the standard pipeline finds no visible-passer). FALSIFY-BENCH-local:
n=52; HumanEval+: n=164; MBPP+: n=370. p is the one-sided exact McNemar (binomial) probability.
The gain is large and significant only on the base, low-coverage DeepSeek cell and small but do-no-harm on
the instruction-tuned Qwen cells (both 1.5B and 0.5B) on both external benchmarks—an expression-failure
pattern that tracks the model, not the benchmark.

    Benchmark                 Cell                        std   M1    b10   b01   net         p
    FALSIFY-BENCH-local       DeepSeek-Coder-1.3B         25     30    0     5    +5          0.031
    FALSIFY-BENCH-local       Qwen2.5-Coder-1.5B          38     45    0     7    +7         0.0078
    HumanEval+                DeepSeek-Coder-1.3B          29   41     0    12    +12    2.4 × 10−4
    HumanEval+                Qwen2.5-Coder-1.5B          126   128    0     2    +2       0.25 (ns)
    HumanEval+                Qwen2.5-Coder-0.5B          114   115    0     1    +1        0.5 (ns)
    MBPP+                     DeepSeek-Coder-1.3B         128   161    0    33    +33    1.2 × 10−10
    MBPP+                     Qwen2.5-Coder-1.5B          259   263    0     4    +4     0.0625 (ns)
    MBPP+                     Qwen2.5-Coder-0.5B          199   202    0     3    +3      0.125 (ns)


function name from the public tests (the most-called bare identifier in the assertions, never the
reference solution), locate the single defined function in the candidate, and rename it to match. It is
applied under a strict rule—recover only on tasks where the standard pipeline finds no visible-passer—
so a task the standard pipeline already handles is never altered. Because a deployed program is
expected to pass the visible tests, a task on which the standard pipeline yields no public-passer
carries no deployable baseline success for M1 to displace, and M1 in turn returns only a recovered
public-passer; it therefore cannot convert a standard success into a failure, and b10 =0 is observed
on every cell (Table 4). It is leakage-free (the name derives from public tests; an earlier dependency
on the reference solution was caught by a falsification probe and removed) and adds zero generation
(Algorithm 1).
   Table 4 reports the result. On the self-authored benchmark M1 gains +5 (DeepSeek) and +7
(Qwen) tasks, b10 =0, p ≤ 0.031. The effect is larger on the external benchmarks for the weak
model: on HumanEval+, DeepSeek-Coder-1.3B recovers 13 visible-passers the standard extractor
dropped, 12 of them hidden-correct, lifting 29 → 41 (+12, p=2.4 × 10−4 ); on MBPP+ it recovers 43
dropped visible-passers, 33 of them hidden-correct, lifting 128 → 161 (+33, p=1.2 × 10−10 ). The
instruction-tuned Qwen cells (both 1.5B and 0.5B) gain little and ns (+1 to +4); these instruction-
tuned cells carry far fewer expression failures to recover (the 1.5B already public-passes 138/164
HumanEval+ tasks). An independent falsification harness re-derived all four checks from scratch
on every cell (every gained task had no standard visible-passer; re-extraction passes both public
and hidden; the recovered body appears verbatim in the model’s raw output; the aligned name is
invariant to poisoning the hidden tests and the reference): 4/4 HOLD on all three model cells.
   The honest scope: M1 recovers the model’s own code; it does not synthesize new logic, and
on the weak cell it is bounded by the coverage wall (only 32/164 HumanEval+ tasks yield any
visible-passer at all). But within that scope it is a real, leakage-free, do-no-harm, externally-valid
accuracy win—and the only one observed in this program. Its lesson generalizes beyond this paper:
for a weak frozen model a measurable share of “failure” is expression, not logic—a surface-form


                                                   18
                                                     ACE saving vs. do-no-harm (n=80)
                                                                                compute saving (%)   2.0
                                        60                                      harm b10 (tasks)
                                        50                            do-no-harm (HB bound)
                                                                                                     1.5

                   compute saving (%)
                                                                      19.1% saving




                                                                                                       harm b10 (tasks)
                                                                      b10=0, HB p=0.0165
                                        40
                                        30                                                           1.0
                                        20
                                                                                                     0.5
                                        10
                                        0                                                            0.0
                                             1   2        3     4         5    6        7      8
                                                                    tau

Figure 3: ACE trades compute saving against do-no-harm. As the commit threshold τ falls, the compute
saving rises but so does the harm count b10 (tasks the full-budget consensus pick gets right and the early-stop
gets wrong). The zero-observed-harm operating point (b10 =0, Hoeffding–Bentkus bound p=0.0165, not
corrected for τ selection) is τ =4 at ≈ 19% saving; the ≈ 64% saving at τ =1 comes with b10 =2 and does not
reach the bound. Regenerated from the released manifest by figures/make_figures.py.


dependence of the kind that moves measured performance independently of model competence
(Sclar, Choi, Tsvetkov, & Suhr, 2024)—so the extraction harness should be fixed before the model is
blamed.
    The second survivor, ACE, is a modest compute reduction carrying a finite-sample do-no-
harm bound. A naive Best-of-N draws all k samples and returns the first visible-passer, so the
samples after that passer are wasted. ACE (adaptive consensus early-stop) stops sampling once a
commit threshold τ on agreeing visible-passers is reached, recovering that wasted compute; its harm
rate against the full-budget consensus pick is bounded with Hoeffding–Bentkus Learn-then-Test
(Angelopoulos et al., 2021) (α=0.05, δ=0.10; by Proposition 1 the bound can issue only at n ≥ 45).
    ACE is reported with deliberate calibration, because the headline is a trade-off, not a single
number (Figure 3, Algorithm 2). Table 5 gives the τ -sweep on the competent cell.
    There is a genuine tension between saving and do-no-harm, and the harm is measured against
the full-budget consensus pick—the modal-cluster medoid taken over all k public-passers, whose
pass rate (0.6125) is within one task of BoN’s (0.625; ∆=0.0125)—so that b10 counts tasks where
spending the full budget would have been correct and the early stop is not. (Against a first-passer
deployment of BoN the lock-stop variant shows b10 =3, which is why the do-no-harm reference is the
full-budget consensus pick rather than the first-passer.) The aggressive stop (τ =1) saves 63.9% of
samples but incurs b10 =2 (two such tasks) and does not reach the bound; the first operating point
that is empirically do-no-harm (b10 =0) is τ =4, which saves 19.1% at Hoeffding–Bentkus p=0.0165.
This minimal harm-free τ is read off the evaluation set itself, with no separate calibration split
and no correction for scanning the τ -grid, so the Hoeffding–Bentkus value is a bound at this single
operating point rather than a τ -selection–corrected guarantee. A selection-corrected certificate


                                                                     19
Table 5: ACE on Qwen2.5-Coder-1.5B × FALSIFY-BENCH-local (n=80; BoN pass@=0.625 and the
full-budget consensus pick pass@=0.6125 on this cell). b10 is the harm against the full-budget consensus pick
(tasks it gets right and the early stop does not); at τ =4 the early stop equals the full-budget consensus pick
(0.6125, b10 =b01 =0). The saving/do-no-harm trade-off is explicit: the b10 =0 operating point is τ =4 at 19.1%,
not the 63.9% of τ =1. An earlier note that bundled “64% saving, b10 =0, certified” conflated two τ rows; the
manifest-exact values are below.

      τ    ACE pass     b10   mean compute (/8)          saving      note
      1       0.625      2             2.89             63.9%        aggressive; exceeds bound (p=0.53)
      2       0.625      1             4.25             46.9%
      3      0.6125      1             5.46             31.7%
      4      0.6125      0            6.48              19.1%        HB bound p=0.0165
     5–8     ≈ 0.62      0           7.1–8.0         11.6% → 0%      within bound, smaller


would require a held-out calibration split or a multiple-τ Learn-then-Test correction, neither of
which is claimed here. The honest claim is therefore: ACE recovers ≈ 19% of a full-budget run’s
compute at no measured accuracy cost, with a finite-sample do-no-harm bound at this operating
point; the larger 60%-class savings exist but forgo it. The baseline is treated deliberately, because
it bounds the claim: the ≈ 19% is measured against drawing every one of the k samples, and a
deployment that itself stops at the first public-passer already recovers most of that compute—against
such a sequential-stop deployment the saving falls toward zero. ACE’s contribution is therefore the
finite-sample do-no-harm bound on early stopping, not a large saving over a sequential deployment.
    The same shape holds on the second competent cell (Qwen2.5-Coder-0.5B, n=50): the do-no-
harm (b10 =0) point is τ =5 at 2.25% saving (HB p=0.077), while the τ =1 stop saves 61.5% at b10 =2.
On the 32-task Substrate-W cell no finite-sample bound can issue (n < 45, Corollary 1); and on
DeepSeek-Coder-1.3B the saving collapses to ∼ 7–12%, the first visible-passer arriving late under
the coverage wall. Two honest framings follow. First, ACE is a compute win, not an accuracy win:
at k=8 execution-consensus ties BoN (0.6125 vs 0.625, ∆=0.0125), confirming the accuracy survey
above. Second, the saving is real but modest, and it is reported as such—an instance of the same
calibration applied to the operators that are rejected.
    The accuracy-facing dual of ACE fails as predicted, and is reported here for completeness: it is
not a third survivor but a predicted null. Reinvesting ACE’s freed compute as deeper sampling on
hard tasks (the easy→hard move) is null at matched compute: ∆= + 0.0038 (≈ 0.3 of 80 tasks), the
difficulty signal is inert (its allocation equals a uniform placebo and the oracle to the digit), and
the gain is not coverage-backed. This is the coverage wall again, and it reproduces the published
online-code negative (Damani et al., 2025).
    A measurement program built on a self-authored benchmark is only as trustworthy as the
claim that the instrument is not the result. The M1 accuracy gain and the selection negative were
therefore re-run on two standard external benchmarks—HumanEval+ (164 tasks) and MBPP+
(370 tasks), each on three model cells (DeepSeek-Coder-1.3B, Qwen2.5-Coder-1.5B, and the smaller
Qwen2.5-Coder-0.5B) (J. Liu et al., 2023)—using the same k=8 pools and the same leakage-free,
post-hoc protocol (Figure 4). The MBPP+ ground-truth oracle is built by executing the canonical


                                                      20
                                                M1 recovery -- HumanEval+                                                                Selection headroom -- HumanEval+
                             160                                           standard extractor                                160   DeepSeek-1.3B
                                                                           M1 recovery                                             Qwen2.5-1.5B
                             140                              +2                                                             140   Qwen2.5-0.5B                             hr=7
tasks passing hidden tests




                                                                                                tasks passing hidden tests
                                                                                     +1                                                                                            hr=6
                             120                                                                                             120
                             100                                                                                             100
                              80                                                                                              80
                              60                                                                                              60
                                          +12
                              40                                                                                              40                                    hr=0
                              20                                                                                              20
                               0                                                                                               0
                                   DeepSeek-1.3B     Qwen2.5-1.5B         Qwen2.5-0.5B                                               BoN            consensus             oracle
                                                   M1 recovery -- MBPP+                                                                     Selection headroom -- MBPP+
                             350                                           standard extractor                                350                                           DeepSeek-1.3B
                                                                           M1 recovery                                                                                     Qwen2.5-1.5B
                                                                                                                                                                           Qwen2.5-0.5B
                             300                                                                                             300
tasks passing hidden tests




                                                                                                tasks passing hidden tests
                                                                                                                                                                           hr=16
                                                              +4
                             250                                                                                             250                                                   hr=17
                                                                                     +3
                             200                                                                                             200
                                          +33
                             150                                                                                             150                                    hr=11

                             100                                                                                             100
                              50                                                                                             50
                               0                                                                                              0
                                   DeepSeek-1.3B     Qwen2.5-1.5B         Qwen2.5-0.5B                                               BoN            consensus             oracle

Figure 4: External replication on both benchmarks and all three model cells (top: HumanEval+, n=164;
bottom: MBPP+, n=370). Left column: M1 expression-layer recovery (standard extractor vs. M1) lifts
the base, low-coverage DeepSeek cell substantially (+12 on HumanEval+, +33 on MBPP+; b10 =0) and the
instruction-tuned Qwen cells (1.5B/0.5B) only slightly (+1 to +4; they already public-pass most tasks). Right
column: the selector-agnostic ceiling (BoN / consensus / oracle): where the oracle−BoN headroom is positive
(6–17) the realizable consensus selector still captures at most +3, never significant (p ≥ 0.25). Regenerated
from the released manifests by figures/make_figures.py.


solutions under a determinism gate that drops the 8/378 tasks whose canonical oracle is order-
nondeterministic (3) or non-serializable (5, e.g. a returned re.Match), so exact-match grading
is sound on every retained task; the adapter is independently falsified 6/6 on both benchmarks,
including the decisive discrimination-gap-transfers check (fraction 1.000).
                             M1 transfers, more strongly than locally, on both external benchmarks. Table 4 gives it: DeepSeek-
Coder-1.3B gains +12 on HumanEval+ (p=2.4 × 10−4 ) and +33 on MBPP+ (p=1.2 × 10−10 ), both
at b10 =0; the do-no-harm and leakage-free properties survive an independent 4/4 falsification on
every cell. The same pattern holds across both benchmarks and all three cells: the gain is large
and significant on the base, low-coverage DeepSeek model and small but still do-no-harm on the
instruction-tuned Qwen cells (+1 to +4, all ns), which already public-pass most tasks and so have
few expression failures left to recover. The expression-layer loss is therefore a property of the weak
model’s output, not of the benchmark’s formatting, and the recovered gain grows with the number


                                                                                                21
Table 6: Selection vs. BoN on the external benchmarks (k=8). headroom = oracle − BoN is the selector-
agnostic ceiling. Every cell has headroom 0 (empty consensus trap) or, where headroom exists (6–17), a
realizable consensus selector that captures at most net +3 of it and is never significant (p ≥ 0.25). Here the
BoN-vs-consensus p is the two-sided exact McNemar (binomial) probability, used because no gain direction is
hypothesized for selection; this contrasts with the one-sided gain test of Table 4.

 Benchmark        Cell                     BoN    consensus    oracle   headroom    McNemar (two-sided)
 HumanEval+       DeepSeek-Coder-1.3B       29        29         29        0        b10 =0, b01 =0
 HumanEval+       Qwen2.5-Coder-1.5B       126       127        133        7        b10 =1, b01 =2 (p=1.0)
 HumanEval+       Qwen2.5-Coder-0.5B       114       116        120        6        b10 =0, b01 =2 (p=0.5)
 MBPP+            DeepSeek-Coder-1.3B      128       129        139        11       b10 =0, b01 =1 (p=1.0)
 MBPP+            Qwen2.5-Coder-1.5B       259       260        275        16       b10 =1, b01 =2 (p=1.0)
 MBPP+            Qwen2.5-Coder-0.5B       199       202        216        17       b10 =0, b01 =3 (p=0.25)


of tasks where the model emits correct-but-mis-expressed code.
    The selection negative replicates exactly. Table 6 reports the selector-agnostic ceiling headroom =
oracle − BoN—the most a perfect selector among visible-passers could gain. On the weak cell,
headroom is 0: whenever BoN’s first visible-passer is hidden-wrong, no visible-passer is hidden-
correct, so the consensus trap (Definition 2) is empty and Lemma 1 gives a bound of 0. Where
headroom is positive it is never leakage-free-addressable: a realizable consensus selector captures at
most net +3 and is never significant (p ≥ 0.25) on every such cell—HumanEval+ Qwen-1.5B/0.5B
(headroom 7/6), MBPP+ DeepSeek (headroom 11), and MBPP+ Qwen-1.5B/0.5B (headroom
16/17). “No leakage-free selector beats BoN” thus holds on both external benchmarks and on all
six cells (three models × two benchmarks), even where a sizeable oracle headroom exists—the gap
is real but not leakage-free-addressable, a qualified strengthening of the local negative.
    Together, the external replication closes the gap that would otherwise sink the study: the accuracy
win (M1) and the central negative (selection cannot beat BoN) both hold off the self-authored
benchmark.


4    Discussion
In this study, twenty-six Popperian post-hoc operators are evaluated over a frozen small code model’s
own candidate pool, each judged against a matched-compute, leakage-free Best-of-N (BoN) baseline
by the do-no-harm (DNH) test of the formal setup (b10 harm, b01 gain, bar b10 =0). The negative,
the two survivors, and the prior methods are weighed in turn, and the mechanisms that produce
them are stated with their measurements.
    It is not shown that falsification is useless, nor that post-hoc operators never help; what is
shown is narrower and measurable: for a frozen small code model, on the benchmarks tested,
no operator over the model’s semantic output space converts to a held-out accuracy gain over
matched-compute Best-of-N (BoN), and the reason is structural—coverage wall, capability scissors,
and a near-empty consensus trap—not a tuning artifact. The same three mechanisms predict where
the result would change: a weaker visible-test filter (so that visible-passing, hidden-wrong majorities


                                                     22
become common) would refill the consensus trap, and a genuinely coverage-increasing intervention
(a stronger generator, or retrieval that adds new correct candidates rather than re-ranking existing
ones) would move the wall. Operators that re-rank what is already there cannot.
    The observed negative is unlikely to be explained by a single tuning failure, because the same
pattern appears across operator families and confound checks. Three forces, each measured on the
cached pools, account for it, and together they bound what any do-no-harm certificate can promise.
The first force is a coverage wall. The weak model’s hard-task failures are systematic. Generating
deeper pools (k=16) for 30 held-out hard tasks, 16/30 still produce no hidden-correct candidate
even at k=16; 11/30 were already covered at k=8 (so the loss was selection, not coverage); and only
3/30 gain a hidden-correct candidate, of which just 1 gains a visible-passing one that a leakage-free
selector could grab. Coverage—the fraction of tasks solved by any sample, the binding axis for
repeated sampling (Brown et al., 2024)—does not grow here, directly reproducing the published
finding that online difficulty-adaptive allocation on code can fall below best-of-k (Damani et al.,
2025): there is often nothing in the budget to reallocate to.
    The second force is a capability scissors. Conditioned on passing Tpub , the residual hidden-
correctness signal is at chance. On 255 visible-passing candidates from Qwen2.5-Coder-1.5B a
wavelet/embedding probe scores AUC 0.479 for hidden correctness (∆AUC vs. embedding −0.004,
p=0.60), even though the same features predict public-pass (well-formedness) at AUC 0.985. The
discriminative signal a competent generator leaves among its plausible candidates is negligible—an
instance of the generation–verification gap that scales with pre-training compute, and so is small
for a weak model (Song et al., 2025); what gain exists has already been captured by pass@1 and
by BoN’s visible-test filter. The gap sharpens with capability: enabling reasoning on a stronger
model raises pass@1 but lowers the falsification signal (split-discriminating tasks drop from 5 to
1). Reaching for a second or larger model as the judge does not escape this, since more accurate
models carry more correlated errors (Kim, Garg, Peng, & Garg, 2025). “The model can’t think” was
a pass@1 limit, not a falsification bottleneck. The scissors has two limbs: a competent generator
(Qwen) leaves no discriminable error among its plausible candidates, while an incompetent one
(DeepSeek, with selector-agnostic headroom 0 on HumanEval+) leaves no recoverable headroom at
all. The thin discriminable middle is the only place a selector could act, and a frozen small model
rarely sits in it.
    The third force is the near-empty consensus trap. By Lemma 1 a leakage-free selector can
net-gain only on consensus-trap tasks (Definition 2)—those whose public-passing majority is hidden-
wrong while a correct candidate still survives in the pool. This regime has independently been named
the consensus trap and shown to require generator–verifier weight co-evolution to escape (Pan et al.,
2026); under frozen weights its frequency is instead measured here, and it essentially never occurs.
On two benchmarks engineered to admit a sound veto (10 and 16 tasks, Qwen2.5-Coder-1.5B) the
model emitted the triggering bug on only 0/10 and 2/16 tasks and never as the consensus majority,
so a conformal sound veto correctly never fired (∆=0, false-refute rate 0). A consensus-majority trap
occurred in 0 of these 26 engineered opportunities (an exact one-sided 95% upper bound of ≈ 11%


                                                 23
on its rate), so by Lemma 1 any leakage-free selector’s expected gain is bounded at essentially zero
on the regime tested. This is the mechanistic core: the measured regime leaves little leakage-free
selector headroom—the regime in which these operators could help is not observed to occur on the
cells tested.
   Finally, the certificates are power-limited. The trap’s near-emptiness pushes every honest method
toward a do-no-harm claim (b10 =0), and Proposition 1 fixes what that can buy: on the ≤ 32-task
benchmarks where several operators were decided, no distribution-free certificate issues even at
zero observed harm (Corollary 1). A formal certificate is issued only at n ≥ 45, and every smaller
do-no-harm result is read as suggestive—a bound that disciplines the present positives as much as
the operators that are rejected.
   Popper’s lesson here is not that refutation fails but that refutation needs something refutable. A
severe test is only informative when a wrong-but-plausible hypothesis is on the table; the capability
scissors says a competent generator rarely puts one there, and the near-empty trap says the case
where it does and a correct alternative coexists is vanishingly rare. The REFUTE benchmark’s
finding that strong agents create valid counterexamples for < 9% of incorrect solutions (Sinha et
al., 2025) is the same wall seen from the generation side. The companion study found that naming
severe tests adds nothing beyond scaffold (İşcan, 2026); this study finds that executing them as a
post-hoc operator adds nothing to accuracy either—and locates the reason in the data rather than
the rhetoric.
   Table 7 places the program against the closest prior methods, and two distinctions are load-
bearing. First, almost no prior selection or repair method states a matched-compute, leakage-free
do-no-harm guarantee: they report mean pass-rate gains, often on larger models and against
baselines that draw fewer samples—exactly the “a gain is one more sample” confound that the
matched-compute do-no-harm test rules out—and the regime their selection signal needs, the
consensus trap, is measured to be near-empty for a frozen small model (Lemma 1). Second, the
falsification-based competitors operate on a different object: POPPER (K. Huang et al., 2025)
validates a fixed natural-language hypothesis under strict Type-I control, SEVerA (Banerjee et al.,
2026) wraps each model call in a verified contract, and REFUTE (Sinha et al., 2025) measures
whether a model can generate a counterexample, whereas falsification is tested here as a post-hoc
operator over a frozen model’s own code, and why it does not convert to accuracy is measured.
Where prior methods have the edge is external validity and scale—they are demonstrated on stronger
models, where coverage is not the binding wall; the distinctive contribution here is the opposite end,
a calibrated account of the small-frozen regime with the only deployed accuracy win on it.
   The two survivors point the practitioner somewhere specific. The largest cheap win was not a
clever selector but a better extractor: M1’s expression-layer recovery delivered the program’s only
accuracy gain, on both benchmarks, at zero extra compute, by fixing the harness rather than the
model. The second win was a compute schedule (ACE), modest and with a Hoeffding–Bentkus
bound at the selected operating point. The unifying rule: spend effort on the harness (extraction,
serving, compute budget), measure coverage (pass@k) before crediting any selector, and treat


                                                 24
Table 7: This work among the closest post-hoc and falsification-based methods. “DNH/cert.” marks whether
the method states a matched-compute, leakage-free do-no-harm guarantee and a finite-sample certificate.
Prior selection and repair methods report mean gains, typically on larger models and against unmatched
baselines; the falsification competitors act on a different object than a frozen model’s own code samples.

  Method                          Acts on            DNH/cert.    Outcome and relation to this work
  Execution selection             samples, by        no / no      gains on capable models; null here, since
  (B. Chen et al., 2023; Shi et   execution                       the signal is in Thid and the consensus trap
  al., 2022)                      agreement                       is near-empty (Lemma 1)
  Self-repair (X. Chen et al.,    a failed attempt   no / no      helps strong models; compute-confounded
  2024; Shinn et al., 2023)                                       with no matched-compute gain at ≤ 1.5 B
                                                                  (J. Huang et al., 2024)
  Online allocation (Damani       sampling budget    no / no      can fall below best-of-k on code; reproduced
  et al., 2025)                                                   here
  POPPER (K. Huang et al.,        a fixed NL         Type-I / –   severe tests with error control; validates a
  2025)                           hypothesis                      hypothesis, not code synthesis
  SEVerA (Banerjee et al.,        each model call    contract /   verification, not falsification; a
  2026)                                              –            complementary guarantee
  REFUTE (Sinha et al.,           counterexample     –/–          strong agents succeed on < 9%; the same
  2025)                           generation                      wall from the generation side
  This work (M1, ACE)             a frozen model’s   yes /        only deployed accuracy win on frozen small
                                  own samples        bound        models (+12/+33, b10 =0) and a
                                                                  do-no-harm ≈ 19% compute saving
                                                                  (n ≥ 45); bounded to the small-frozen
                                                                  regime



post-hoc accuracy claims with the coverage wall in mind. This is a modest conclusion, but it is the
one the measurements support.
   In preparing this paper, a number-reconciliation pass caught an internal overclaim: an earlier
results note bundled ACE’s aggressive τ =1 saving (≈ 64%) with the τ =4 do-no-harm property
(b10 =0, Hoeffding–Bentkus (HB) p=0.0165) as if they held at one operating point. The manifest-
exact trade-off is in Table 5: the zero-harm saving is ≈ 19%. The corrected numbers are reported
here and the source notes have been fixed. This is flagged deliberately, in the spirit of the program:
a falsification discipline that does not audit its own positives is only half a discipline.
   Several boundaries of the claim deserve naming, each with its direction of risk. On scale and
models, the external replication spans two benchmarks (HumanEval+ and MBPP+), each on three
model cells (DeepSeek-Coder-1.3B and Qwen2.5-Coder-1.5B/0.5B), so the model axis covers the
0.5–1.5B range across two families; a genuinely third architecture family would strengthen it further,
but the obvious local candidate, CodeGemma-2B, is base (non-instruction-tuned) and does not
follow the instruction protocol (it emits a bare code fence and no solution), so it was not added,
to avoid confounding the comparison. A third external benchmark also remains worthwhile: a
standalone LiveCodeBench functional floor probe shows its easy functional subset is tractable for
these models (Qwen-1.5B solves 37.5% pass@1 on the public tests), so it is not vacuous, but a faithful
integration is deferred because LiveCodeBench ships no canonical solution and uses a class-method,
compressed-private-test contract that would require invasive changes to the validated grader. The
MBPP+ retained set excludes 8/378 tasks whose canonical oracle is order-nondeterministic (3) or



                                                      25
non-serializable (5), so its absolute counts are over 370 tasks, not the nominal 378, and several
per-operator verdicts rest on ≤ 32–80-task benchmarks where, by Proposition 1, a do-no-harm
certificate cannot issue; these are marked as suggestive throughout.
    On benchmark fidelity, MBPP+ passes the adapter’s name-gate, and the determinism gate drops
the order-nondeterministic set-derived tasks rather than deferring them; only 3/164 HumanEval+
tasks use floating-point tolerance, and the hidden-test input cap is a runtime bound, not a correctness
one (the discrimination-gap check still hit fraction 1.000 at the cap). On operator coverage, twenty-
six operators is a survey, not a census; in particular, logit-/entropy-based uncertainty channels and
a training-based generator change (LoRA / soft-prompt) were not exhaustively tested, though the
generation-conditioning nulls (schema, exemplar, thinking) and the coverage wall make a large win
there unlikely. The evaluation is oracle-only: all scoring is by hidden unit tests, and no claim is
made about code quality, abstention usefulness, or solutions that pass by hard-coding beyond what
the augmented tests catch. Finally, Ollama outputs are seed-stamped but not byte-identical across
hardware/driver/version, so aggregate rates are robust, but individual task-level discordances in a
McNemar table could shift by one or two on a different machine.


5    Conclusion
This study set out to make a frozen small code model write more correct code by wrapping it in a
Popperian post-hoc operator; the search was deliberately broad—twenty-six operators, claims fixed
in advance, adversarial confound checks, matched compute. For accuracy, none of the operators that
act on the model’s semantics beats Best-of-N (BoN), and the reason is measurable: the weak model’s
hard failures are systematic (the coverage wall), a competent generator leaves no discriminable error
among its plausible candidates (the capability scissors), and the regime a leakage-free selector needs
is essentially empty (the near-empty consensus trap), which in turn caps what any small-sample
do-no-harm certificate can promise.
    Two operators do win, and on a different axis: an expression-layer recovery (M1) that gives the
program its only deployed accuracy gain by fixing the extractor rather than the model—do-no-harm,
leakage-free, and stronger on standard external benchmarks (+12 tasks p=2.4×10−4 on HumanEval+
and +33 p=1.2 × 10−10 on MBPP+, DeepSeek-Coder-1.3B)—and a modest compute reduction
(ACE) with a Hoeffding–Bentkus bound at the selected operating point. The M1 accuracy gain
and the central selection negative both replicate on HumanEval+ and MBPP+ across three model
cells, closing the self-authored-benchmark gap. The practical message is plain and useful to anyone
deploying these models locally: fix the harness before the model, and interpret post-hoc accuracy
claims in light of the coverage wall.
    These conclusions are bounded, and the boundaries point to the work that remains. The
mechanisms themselves predict where the negative would change: a genuinely coverage-increasing
intervention—a stronger generator, or retrieval that adds new correct candidates rather than re-
ranking the existing pool—would move the coverage wall, and a weaker visible-test filter would refill


                                                  26
the consensus trap, so both deserve a direct test. On the measurement side, a third architecture family,
a third external benchmark that ships canonical solutions, uncertainty channels (logit/entropy), and
a training-based generator change (low-rank adaptation, LoRA, or soft-prompt) would extend the
survey beyond the twenty-six post-hoc operators examined here. Each targets a named limitation
of the present study rather than a new claim about it.
    The calibrated takeaway, then, is not a universal impossibility result. For frozen small code
models in the tested regime, the dominant addressable losses were not semantic post-hoc reasoning
over existing samples, but expression recovery and compute scheduling; accuracy gains from semantic
operators would likely require changing the generator, expanding candidate coverage, or adding
genuinely new information rather than re-processing the pool already in hand.


Generative-AI Use Disclosure
This study evaluates AI code generators (the frozen small models under test). The study’s design,
hypotheses, pre-registration, literature review, statistical analysis, and claim calibration are the
author’s own work. A generative-AI assistant was used only to improve the readability of the
manuscript prose (copy-editing and phrasing); it did not design the experiments, produce or select
the results, choose the citations, or set any conclusion. No AI system is listed as an author.


Funding
This work was supported by the Scientific and Technological Research Council of Türkiye (TÜBİTAK)
under the 1001 programme, project no. 225M316, “A Tilt-Trirotor Vertical Take-Off and Landing
Controller Enabling Task-Oriented Transfer and Rapid Adaptation: Hardware-in-the-Loop and Real
Validation of a Meta-Learning–Based Reinforcement Learning Architecture.” The meta-learning
code developed in that project was integrated into the test harness together with the frozen language
models studied here, and was used during the agent-design phase to optimize the algorithms designed
by the author.


Conflict of Interest
The author declares no conflict of interest.


A     The operator ledger
Table 8 lists every post-hoc operator in the program with its verdict and headline number against
Best-of-N at matched compute. Legend: POS positive; WEAK signal, not significant; NULL ≈
BoN; NEG worse than BoN; FALS looked positive, broke under a confound check. Numbers are from
the released per-operator manifests; cells are Qwen2.5-Coder-1.5B/0.5B and DeepSeek-Coder-1.3B
unless noted.

                                                  27
Table 8: The post-hoc operators for frozen small code models, by family. Rows #0–#25 are the twenty-six
operators of the accuracy survey (all null, negative, falsified, or weak); S1–S2 are the two survivors (M1,
ACE), counted apart because they win on the expression and compute axes the twenty-six do not address.

    #     Operator                       Family            Verdict   Headline result vs. BoN
    0     Refute-first pipeline          prompt            WEAK      60/80 vs 55/80, +6.2pp, McNemar p=0.23
          (REFv3)                                                    (mostly CoT edge; Popperian increment
                                                                     +1.2pp)
    1     Execution-consensus            selection         NULL      ties BoN (k=8); HumanEval+ qwen 127 vs
          (MBR-Exec)                                                 126, p=1.0
    2     Embedding-medoid               selection         NULL      40/50 vs 39/50, p=1.00
          (CEMS)
    3     Behavioural-trace rerank       selection         NULL      40/50, ceiling-bound
          (BTR)
    4     Verisimilitude rank (VRS)      selection         NULL      39/50, ceiling-bound
    5     Metamorphic selection          selection         NULL      +0 both cells; ∼83% of bugs MR-invisible
          (MR)
    6     Learned verifier (LCV)         verification      NULL      ROC-AUC 0.444 (below chance)
    7     Fingerprint verifier (XFV)     verification      WEAK      AUC 0.60, permutation p=0.114 (ns)
    8     Latent abstention (LEA)        verification      NEG       AUC 0.738 but 24% false-abstain →
                                                                     net-negative
    9     Self-debug (M2)                repair            NULL      compute-confounded; b10 =13 vs matched
                                                                     BoN@8
    10    Bandit repair router (BRR)     repair            NULL      LinUCB 0.379 < best fixed arm 0.482
    11    Counterexample-guided          repair            NEG       14/20 < REFv3 16/20; matched-compute
          repair (CEGIS-R)                                           retracted
    12    Severity-conditioned regen     repair             NEG      severe 0.675 = placebo 0.675 (∆=0)
          (SERA)
    13    Prompt-normalization           repair            WEAK      +3 at 1-sample, ≪ BoN@8
          (M3)
    14    Thinking-iteration (TIRF)      repair             NEG      ∆=−0.015 (qwen3-0.6b) / −0.31 (1.7b),
                                                                     b10 =2
    15    Version-space elimination      elim./veto        FALS      ∆=+0.0625 but p=0.5, FRR 0.28, deepseek
          (PAVER)                                                    ∆=0
    16    Programme portfolio            portfolio         FALS      +0.19 = selection artifact (BoN pass@20 cov
          (PLURAL)                                                   0.906 ≈ oracle)
    17    Conformal sound veto           veto              NULL      ∆=0 on 3 substrates; veto never fires
          (SCRC)
    18    Schema hint (PRAXIS)           conditioning      NEG       matched 0.781 < vanilla 0.844 (∆=−0.0625)
    19    Verified-exemplar              conditioning      FALS      real +5 but generic scaffold (verified ≈
          (MNEMON)                                                   unverified ≈ placebo)
    20    Decoding-diversity union       conditioning      NULL      coverage +2/50 but deployed ∆=0 (p=1.0)
          (POLYGEN)
    21    Wavelet probe                  conditioning      NULL      hidden-AUC 0.479, ∆AUC −0.004 (p=0.60)
          (WAVE-RL-F)
    22    Frequency probe                conditioning      NULL      hidden-AUC 0.354 < chance (gate STOP)
          (FREQ-RL)
    23    Exec-behavior differential     conditioning      NULL†     breaches wall (AUC 0.798) but deployed
          (FREQ-RL v2)                                               ∆=0
    24    Adaptive allocation            compute           NULL      = compute-saving restated; falsification not
          (SCARF)                                                    load-bearing
    25    Easy→hard reallocation         compute           NULL      ∆=+0.0038, signal inert (reproduces
          (ACE+)                                                     Damani et al. 2025)
    Survivors (orthogonal axes):
    S1   Expression recovery             expression         POS      HumanEval+ deepseek +12 (p=2.4×10−4 ,
        (M1)                                                         b10 =0)
    S2   Consensus early-stop            compute           POS‡      do-no-harm ≈ 19% saving (HB bound, τ on
        (ACE)                                             28         eval set; p=0.0165, n=80)
†
 The execution-behavior differential is the one leakage-free signal that detects hidden failure above chance, but it has
nothing to act on at deploy time (the consensus pick already agrees), so it converts to ∆=0. ‡ ACE is a compute win,
                     not an accuracy win, and the do-no-harm saving is modest (in the Results).
B     A note on finite-sample power
Proposition 1 gives the distribution-free floor: at α=0.05, δ=0.10, no zero-harm do-no-harm certificate
can issue below n=45. The per-operator benchmarks span n=10 (per family) to n=80 (FALSIFY-
BENCH-local) to n=164 (HumanEval+). Two consequences follow and are applied throughout.
First, every operator evaluated only on a ≤ 32-task set (the sound-veto capstone and metamorphic
selection on Substrate-W) is reported as suggestive: even at zero observed harm the certificate
does not issue, so a “provable do-no-harm” phrasing there would over-claim. Second, a gain at
b10 =0 is judged by the exact one-sided McNemar/binomial, which reaches p < 0.05 at b01 ≥ 5;
the pre-declared effect floor of a net ≥ 6 (the two-sided exact threshold) is stricter still. The only
operators that clear one-sided significance are M1’s accuracy wins (FALSIFY-BENCH-local qwen
b01 =7; HumanEval+ deepseek b01 =12; MBPP+ deepseek b01 =33); FALSIFY-BENCH-local deepseek
(b01 =5, p=0.031) clears one-sided significance but not the conservative net-≥ 6 floor, and no semantic
operator reaches even b01 =5. No accuracy claim is therefore made for any semantic operator, and
report all such results as null/negative with their exact discordant counts rather than as ceiling-
limited non-detections. The two positives survive a family-wise correction across the full operator
set: M1’s external accuracy wins clear a Bonferroni bar over all twenty-six operators (HumanEval+
deepseek p=2.4 × 10−4 and MBPP+ deepseek p=1.2 × 10−10 , both far below 0.05/26 ≈ 0.0019),
and no semantic operator approaches significance even uncorrected. ACE’s compute result is a
single-operating-point Hoeffding–Bentkus bound (Angelopoulos et al., 2021), read at the τ selected
on the evaluation set with no separate τ -grid multiplicity correction (see the Results).


References
Angelopoulos, A. N., Bates, S., Candès, E. J., Jordan, M. I., & Lei, L. (2021). Learn then test:
     Calibrating predictive algorithms to achieve risk control. arXiv preprint arXiv:2110.01052.
      Retrieved from https://arxiv.org/abs/2110.01052
Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry,
      M., Le, Q., & Sutton, C. (2021). Program synthesis with large language models. arXiv preprint
      arXiv:2108.07732. Retrieved from https://arxiv.org/abs/2108.07732
Banerjee, D., Xu, C., Ie, E., Zhang, M., Peng, D., Lin, C.-C., & Singh, G. (2026). SEVerA:
     Verified synthesis of self-evolving agents. arXiv preprint arXiv:2603.25111. Retrieved from
      https://arxiv.org/abs/2603.25111
Bansal, S., Jiao, F., Zhou, Y., Xu, A., Joty, S., & Yavuz, S. (2026). VIBEPASS: Can vibe
      coders really pass the vibe check? arXiv preprint arXiv:2603.15921. Retrieved from https://
      arxiv.org/abs/2603.15921
Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V., Ré, C., & Mirhoseini, A. (2024).
      Large language monkeys: Scaling inference compute with repeated sampling. arXiv preprint
      arXiv:2407.21787. Retrieved from https://arxiv.org/abs/2407.21787



                                                  29
Chen, B., Zhang, F., Nguyen, A., Zan, D., Lin, Z., Lou, J.-G., & Chen, W. (2023). CodeT: Code
     generation with generated tests. In International conference on learning representations (iclr).
     Retrieved from https://arxiv.org/abs/2207.10397 (arXiv:2207.10397)
Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H. P., Kaplan, J., Edwards, H., Burda,
     Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger, G., Petrov, M., Khlaaf, H., Sastry,
     G., Mishkin, P., Chan, B., Gray, S., Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavarian,
     M., Winter, C., Tillet, P., Such, F. P., Cummings, D., Plappert, M., Chantzis, F., Barnes,
     E., Herbert-Voss, A., Guss, W. H., Nichol, A., Paino, A., Tezak, N., Tang, J., Babuschkin, I.,
     Balaji, S., Jain, S., Saunders, W., Hesse, C., Carr, A. N., Leike, J., Achiam, J., Misra, V.,
     Morikawa, E., Radford, A., Knight, M., Brundage, M., Murati, M., Mayer, K., Welinder, P.,
     McGrew, B., Amodei, D., McCandlish, S., Sutskever, I., & Zaremba, W. (2021). Evaluating
     large language models trained on code. arXiv preprint arXiv:2107.03374. Retrieved from
     https://arxiv.org/abs/2107.03374
Chen, X., Lin, M., Schärli, N., & Zhou, D. (2024). Teaching large language models to self-debug.
     In International conference on learning representations (iclr). Retrieved from https://
     arxiv.org/abs/2304.05128 (arXiv:2304.05128)
Chen, X., Tao, Z., Zhang, K., Zhou, C., Zhang, X., Gu, W., He, Y., Zhang, M., Cai, X., Zhao,
     H., & Jin, Z. (2025). Revisit self-debugging with self-generated tests for code generation.
     In Proceedings of the 63rd annual meeting of the association for computational linguistics
     (volume 1: Long papers) (pp. 18003–18023). Retrieved from https://doi.org/10.18653/v1/
     2025.acl-long.881 (arXiv:2501.12793)
Chou, C. J., Lwin, K. T., & Soremekun, E. (2026). MUCOCO: Automated consistency testing
     of code LLMs. arXiv preprint arXiv:2604.19086. Retrieved from https://arxiv.org/abs/
     2604.19086
Damani, M., Shenfeld, I., Peng, A., Bobu, A., & Andreas, J. (2025). Learning how hard to think:
     Input-adaptive allocation of LM computation. In International conference on learning repre-
     sentations (iclr). Retrieved from https://arxiv.org/abs/2410.04707 (arXiv:2410.04707)
Fagerland, M. W., Lydersen, S., & Laake, P. (2013). The McNemar test for binary matched-pairs
     data: Mid-p and asymptotic are better than exact conditional. BMC Medical Research
     Methodology, 13 (1), 91. Retrieved from https://doi.org/10.1186/1471-2288-13-91
Gou, Z., Shao, Z., Gong, Y., Shen, Y., Yang, Y., Duan, N., & Chen, W. (2024). CRITIC: Large
     language models can self-correct with tool-interactive critiquing. In International conference
     on learning representations (iclr). Retrieved from https://arxiv.org/abs/2305.11738
     (arXiv:2305.11738)
Groce, A., Ahmed, I., Jensen, C., & McKenney, P. E. (2015). How verified is my code? Falsification-
     driven verification. In Proceedings of the 2015 30th ieee/acm international conference on
     automated software engineering (ase) (pp. 737–748). Retrieved from https://doi.org/
     10.1109/ASE.2015.40
Guo, D., Zhu, Q., Yang, D., Xie, Z., Dong, K., Zhang, W., Chen, G., Bi, X., Wu, Y., Li, Y., Luo,


                                                30
     F., Xiong, Y., & Liang, W. (2024). DeepSeek-Coder: When the large language model meets
     programming – the rise of code intelligence. arXiv preprint arXiv:2401.14196. Retrieved from
     https://arxiv.org/abs/2401.14196
Huang, J., Chen, X., Mishra, S., Zheng, H. S., Yu, A. W., Song, X., & Zhou, D. (2024). Large language
     models cannot self-correct reasoning yet. In International conference on learning representations
     (iclr). Retrieved from https://arxiv.org/abs/2310.01798 (arXiv:2310.01798)
Huang, K., Jin, Y., Li, R., Li, M. Y., Candès, E., & Leskovec, J. (2025). Automated hypothesis
     validation with agentic sequential falsifications. In Proceedings of the 42nd international
     conference on machine learning (icml). Retrieved from https://arxiv.org/abs/2502.09858
     (POPPER; arXiv:2502.09858)
Hui, B., Yang, J., Cui, Z., Yang, J., Liu, D., Zhang, L., Liu, T., Zhang, J., Yu, B., Lu, K., Dang, K.,
     Fan, Y., Zhang, Y., Yang, A., Men, R., Huang, F., Zheng, B., Miao, Y., Quan, S., Feng, Y.,
     Ren, X., Ren, X., Zhou, J., & Lin, J. (2024). Qwen2.5-Coder technical report. arXiv preprint
     arXiv:2409.12186. Retrieved from https://arxiv.org/abs/2409.12186
İşcan, M. (2026). Scaffold, not vocabulary? A controlled, two-tier, pre-registered study of a popperian
     code-generation skill. arXiv preprint arXiv:2606.06454. Retrieved from https://arxiv.org/
     abs/2606.06454 (Companion preprint; PythaLab, Yıldız Technical University)
Jin, H., & Chen, H. (2025). Uncovering systematic failures of LLMs in verifying code against
     natural language specifications. In 2025 40th ieee/acm international conference on automated
     software engineering (ase) (pp. 3819–3823). Retrieved from https://doi.org/10.1109/
     ASE63991.2025.00323 (NIER track; arXiv:2508.12358)
Kim, E., Garg, A., Peng, K., & Garg, N. (2025). Correlated errors in large language models. In
     Proceedings of the 42nd international conference on machine learning (icml). Retrieved from
     https://arxiv.org/abs/2506.07962 (arXiv:2506.07962)
Lakatos, I. (1968). Criticism and the methodology of scientific research programmes. Proceed-
     ings of the Aristotelian Society, 69 , 149–186. Retrieved from https://doi.org/10.1093/
     aristotelian/69.1.149 (New Series; paper read at the Aristotelian Society, 28 October
     1968)
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker, B., Lee, T., Leike, J., Schulman, J.,
     Sutskever, I., & Cobbe, K. (2024). Let’s verify step by step. In International conference
     on learning representations (iclr). Retrieved from https://arxiv.org/abs/2305.20050
     (arXiv:2305.20050)
Liu, J., Xia, C. S., Wang, Y., & Zhang, L. (2023). Is your code generated by ChatGPT
     really correct?    Rigorous evaluation of large language models for code generation.           In
     Advances in neural information processing systems (neurips) (Vol. 36, pp. 21558–21572).
     Retrieved      from    https://proceedings.neurips.cc/paper_files/paper/2023/hash/
     43e9d647ccd3e4b7b5baab53f0368686-Abstract-Conference.html (arXiv:2305.01210)
Liu, X., Sun, X., Bo, L., Hu, Y., Liu, X., & Ye, Z. (2025). Evaluating the test adequacy of
     benchmarks for LLMs on code generation. Journal of Software: Evolution and Process, 37 (7),


                                                  31
     e70034. Retrieved from https://doi.org/10.1002/smr.70034
Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N.,
     Prabhumoye, S., Yang, Y., Gupta, S., Majumder, B. P., Hermann, K., Welleck, S., Yaz-
     danbakhsh, A., & Clark, P. (2023). Self-Refine: Iterative refinement with self-feedback.
     In Advances in neural information processing systems (neurips) (Vol. 36). Retrieved from
     https://arxiv.org/abs/2303.17651 (arXiv:2303.17651)
Matton, A., Sherborne, T., Aumiller, D., Tommasone, E., Alizadeh, M., He, J., Ma, R., Voisin,
     M., Gilsenan-McMahon, E., & Gallé, M. (2024). On leakage of code generation evaluation
     datasets. In Findings of the association for computational linguistics: Emnlp 2024 (pp.
     13215–13223). Retrieved from https://doi.org/10.18653/v1/2024.findings-emnlp.772
     (arXiv:2407.07565)
Mayo, D. G. (2025). Severe testing: Error statistics versus Bayes factor tests. The British Journal
     for the Philosophy of Science. Retrieved from https://doi.org/10.1086/736950 (Advance
     online publication; article 736950)
Mayo, D. G., & Spanos, A. (2006). Severe testing as a basic concept in a Neyman–Pearson philosophy
     of induction. The British Journal for the Philosophy of Science, 57 (2), 323–357. Retrieved
     from https://doi.org/10.1093/bjps/axl003
Niiniluoto, I. (2014). Scientific progress as increasing verisimilitude. Studies in History and
     Philosophy of Science Part A, 46 , 73–77. Retrieved from https://doi.org/10.1016/j
     .shpsa.2014.02.002
Pan, T., Yan, Y., Wang, Z., Zhang, R., Hou, G., Zhang, W., Lu, W., Xiao, J., & Shen, Y. (2026).
     CoVerRL: Breaking the consensus trap in label-free reasoning via generator–verifier co-evolution.
     arXiv preprint arXiv:2603.17775. Retrieved from https://arxiv.org/abs/2603.17775
Popper, K. R. (1959). The logic of scientific discovery. London: Hutchinson. (English translation
     of Logik der Forschung (1934))
Popper, K. R. (1963). Conjectures and refutations: The growth of scientific knowledge. London:
     Routledge and Kegan Paul.
Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2024). Quantifying language models’ sensitivity
     to spurious features in prompt design or: How I learned to start worrying about prompt
     formatting. In International conference on learning representations (iclr). Retrieved from
     https://arxiv.org/abs/2310.11324 (arXiv:2310.11324)
Shi, F., Fried, D., Ghazvininejad, M., Zettlemoyer, L., & Wang, S. I. (2022). Natural language to
     code translation with execution. In Proceedings of the 2022 conference on empirical methods
     in natural language processing (emnlp). Retrieved from https://doi.org/10.18653/v1/
     2022.emnlp-main.231 (MBR-Exec; arXiv:2204.11454)
Shinn,   N.,   Cassano,   F.,   Berman,    E.,   Gopinath,   A.,   Narasimhan,     K., & Yao,       S.
     (2023).     Reflexion:      Language agents with verbal reinforcement learning.               In
     Advances in neural information processing systems (neurips)                 (Vol.   36).     Re-
     trieved      from        https://proceedings.neurips.cc/paper_files/paper/2023/hash/


                                                 32
     1b44b878bb782e6954cd888628510e90-Abstract-Conference.html (arXiv:2303.11366)
Sinha, S., Goel, S., Kumaraguru, P., Geiping, J., Bethge, M., & Prabhu, A. (2025). Can language
     models falsify? evaluating algorithmic reasoning with counterexample creation. In Con-
     ference on language modeling (colm). Retrieved from https://arxiv.org/abs/2502.19414
     (arXiv:2502.19414)
Snell, C., Lee, J., Xu, K., & Kumar, A. (2025). Scaling LLM test-time compute optimally can be more
     effective than scaling model parameters. In International conference on learning representations
     (iclr). Retrieved from https://arxiv.org/abs/2408.03314 (arXiv:2408.03314)
Song, Y., Zhang, H., Eisenach, C., Kakade, S., Foster, D., & Ghai, U. (2025). Mind the gap:
     Examining the self-improvement capabilities of large language models. In International
     conference on learning representations (iclr). Retrieved from https://arxiv.org/abs/2412
     .02674 (arXiv:2412.02674)
Valmeekam, K., Marquez, M., & Kambhampati, S. (2023). Can large language models really improve
     by self-critiquing their own plans? arXiv preprint arXiv:2310.08118; NeurIPS 2023 FMDM
     Workshop. Retrieved from https://arxiv.org/abs/2310.08118
Vranješ, D., Ehrhardt, J., Heesch, R., Moddemann, L., Steude, H. S., & Niggemann, O. (2024).
     Design principles for falsifiable, replicable and reproducible empirical machine learning research.
     In 35th international conference on principles of diagnosis and resilient systems (dx 2024)
     (Vol. 125, pp. 7:1–7:13). Schloss Dagstuhl – Leibniz-Zentrum für Informatik. Retrieved from
     https://doi.org/10.4230/OASIcs.DX.2024.7 (arXiv:2405.18077)
Wang, E., Cassano, F., Wu, C., Bai, Y., Song, W., Nath, V., Han, Z., Hendryx, S., Yue, S., &
     Zhang, H. (2025). Planning in natural language improves LLM search for code generation.
     In International conference on learning representations (iclr). Retrieved from https://
     arxiv.org/abs/2409.03733 (arXiv:2409.03733)
Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi, E. H., Narang, S., Chowdhery, A., & Zhou,
     D. (2023). Self-consistency improves chain of thought reasoning in language models. In
     International conference on learning representations (iclr). Retrieved from https://arxiv
     .org/abs/2203.11171 (arXiv:2203.11171)
Zhang, Q., Wang, D., Qian, H., Li, Y., Zhang, T., Huang, M., Xu, K., Li, H., Liu, Y., & Qiu, H.
     (2025). Understanding the dark side of LLMs’ intrinsic self-correction. In Proceedings of the
     63rd annual meeting of the association for computational linguistics (volume 1: Long papers)
     (pp. 27066–27101). Retrieved from https://doi.org/10.18653/v1/2025.acl-long.1314
     (arXiv:2412.14959)
Zhang, T., Yu, T., Hashimoto, T. B., Lewis, M., tau Yih, W., Fried, D., & Wang, S. I. (2023).
     Coder reviewer reranking for code generation. In Proceedings of the 40th international
     conference on machine learning (icml) (Vol. 202, pp. 41832–41846). Retrieved from https://
     proceedings.mlr.press/v202/zhang23av.html (arXiv:2211.16490)




                                                  33
