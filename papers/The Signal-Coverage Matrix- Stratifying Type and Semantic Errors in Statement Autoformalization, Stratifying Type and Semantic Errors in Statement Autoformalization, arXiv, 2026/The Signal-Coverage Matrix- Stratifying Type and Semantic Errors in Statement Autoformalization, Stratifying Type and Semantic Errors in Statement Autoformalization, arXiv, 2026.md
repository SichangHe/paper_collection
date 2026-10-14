                                                                    The Signal-Coverage Matrix:
                                                Stratifying Type and Semantic Errors in Statement Autoformalization


                                                                              Chengxiao Dai 1 Zhaokun Yan 2 Zhanhui Lin 1


                                                                  Abstract                                     benchmarks (Azerbayev et al., 2023; Poiroux et al., 2024)
                                                                                                               has climbed from ∼53% (GPT-4o (OpenAI, 2024)) to ∼76%
                                              Headline type-correctness (TC%) of LLM auto-
                                                                                                               (DeepSeek V4-Pro (DeepSeek-AI, 2026)) in two years,
arXiv:2606.28013v1 [cs.CL] 26 Jun 2026




                                              formalization has climbed from ∼53% to ∼76%
                                                                                                               driven by methods that refine against the Lean elaborator.
                                              in two years, yet this scalar conceals which er-
                                                                                                               Because TC% does not certify denotational correctness,
                                              rors each method resolves. We propose a signal-
                                                                                                               semantic-faithfulness (SF%) estimators are reported along-
                                              coverage matrix that crosses the Lean elabora-
                                                                                                               side it: back-translation (Zhou et al., 2024) and generalized
                                              tor (pass/fail) with a semantic-equivalence judg-
                                                                                                               tree edit distance (GTED, Liu et al., 2025b).
                                              ment (equivalent/not), sorting every output into
                                              one of four cells: true success (TS), type-only                  Headline metrics conceal mechanism. A +15 pp TC% gain
                                              (TO), semantic-only (SO), or both fail (BF). On                  hides which error stratum is repaired and which is not, and
                                              ProofNet# and MiniF2F-test with DeepSeek V4-                     the choice of SF% judge can shift the reported value by
                                              Pro across Vanilla, Lean-Retry, Sample-Filter, and               ≥ 25 pp on elab-feedback methods (§5.5). No published
                                              Stratified Autoformalization (SAF): (1) the +34                  account decomposes TC% gains by stratum and method.
                                              to +36 TS gain across the three elab-feedback                    We provide such an account.
                                              methods is ∼64% type-stratum recovery, with SO
                                                                                                               Existing methods cluster along three axes. Single-oracle re-
                                              flat on net (87.5% of original semantic errors res-
                                                                                                               finement against the elaborator (Wu et al., 2022; Poiroux
                                              cued, 8 newly created). (2) The TO→TS rate is
                                                                                                               et al., 2024; Guo et al., 2025; Lu et al., 2024) consults
                                              23/61 for each method (Wilson 95% CI [26.6%,
                                                                                                               only the elaborator (or a close proxy) during refinement,
                                              50.3%]), and this stratum-level recovery rate pre-
                                                                                                               and the class has plateaued at ∼75% TC% on ProofNet#
                                              dicts ∆TS on held-out methods to within 2/186
                                                                                                               regardless of topology. Semantic-faithfulness judging
                                              and renders ∆T C linear in the Vanilla elab-fail
                                                                                                               comprises LLM back-translation (Zhou et al., 2024) and
                                              rate across six (model, dataset) cells (R2 =0.96).
                                                                                                               symbolic GTED via the Lean LSP (Liu et al., 2025b), used
                                              (3) The two judges disagree by 26 to 37 pp on
                                                                                                               as standalone SF% estimators but never calibrated against
                                              elab-feedback outputs (vs. 7 pp on Vanilla), with
                                                                                                               each other at scale. Typed structured intermediate rep-
                                              30 to 56% of symbolic-judge false negatives trace-
                                                                                                               resentations were introduced for Isabelle by Draft, Sketch,
                                              able to elaborator-forced rewrites. The persis-
                                                                                                               and Prove (Jiang et al., 2023), whose sketch is a textual
                                              tent residual reduces to two gold-formalization
                                                                                                               proof skeleton rather than a typed structural object. The
                                              errors. TC% gains should be credited by which
                                                                                                               broader formal-math LM literature on premise selection,
                                              cell moved, not by the scalar alone.
                                                                                                               proof generation, and math pretraining (Polu & Sutskever,
                                                                                                               2020; Yang et al., 2023; Azerbayev et al., 2024; Lin et al.,
                                                                                                               2025) addresses different stages of the pipeline and is com-
                                         1. Introduction                                                       plementary.
                                         Statement-level autoformalization maps a natural-language             We instantiate a 2×2 signal-coverage matrix (elaborator
                                         theorem to a Lean 4 signature with a sorry-placeholder                pass/fail × judge equivalent/not) on DeepSeek V4-Pro ×
                                         body. Headline type-correctness (TC%) on ProofNet-class               ProofNet# (186 problems) under a dual-judge protocol that
                                             1                                                                 pairs Claude Opus 4.7 (Anthropic, 2026) with GTED at
                                               School of Computer Science, University of Sydney, Syd-
                                         ney, Australia 2 China Academy of Information and Communi-            τ =0.5, tracking per-problem transitions from Vanilla into
                                         cations Technology, China. Correspondence to: Chengxiao Dai           Lean-Retry, Sample-Filter, and Stratified Autoformalization
                                         <cdai0023@uni.sydney.edu.au>.                                         (SAF).
                                         The 3 rd AI for Math Workshop at the 43rd International Confer-       This paper makes three contributions:
                                         ence on Machine Learning (ICML), Seoul, South Korea, 2026.
                                         Copyright 2026 by the author(s).                                      (1) A diagnostic framework and the predictive regularity

                                                                                                           1
                                 The Signal-Coverage Matrix for Statement Autoformalization

it yields. A 2×2 signal-coverage matrix and a 4×4 tran-               diagonal cells are exactly the per-instance disagreements
sition matrix decompose any TC% gain into type-stratum                between elaborator and judge, and their size, sources, and
recovery, semantic-stratum turnover, and a durable resid-             dynamics across methods are this paper’s core empirical
ual. Under this lens, three algorithmically distinct methods          object. Writing |c| for the count in cell c,
each recover 23/61 of Vanilla TO (Wilson 95% CI [26.6%,
                                                                         T C% = |TS|+|SO|   , SF % = |TS|
                                                                                                                      P
50.3%]), and ∆T C is linear in the Vanilla elab-fail rate at                          n                    n ,     n = c |c|. (1)
R2 =0.96 across six (model, dataset) cells (§2, §5.2, §5.4).
(2) A calibrated dual-judge protocol. Opus paired with                       (Generated Lean signature)     Signal-coverage matrix
GTED at τ =0.5 achieves 94.4% to 95.0% precision across                               Candidate                      Judge:         Judge:
                                                                                   formalization 𝝈
                                                                                                 ෝ                 equivalent   not equivalent
benchmarks, and a four-class taxonomy attributes 30 to
56% of GTED false negatives to elaborator-forced structural
                                                                                                                     TRUE
                                                                                                          Elab:                  SEM ONLY
rewriting (§5.5).                                                                                         pass     SUCCESS
                                                                                                                                   (SO)
                                                                                               Pass                   (TS)
                                                                                 Lean
(3) SAF as a causal-attribution probe. Stratified Auto-                       Elaborator
                                                                                               Fail
formalization (SAF) refines a typed JSON IR against the
elaborator and emits Lean by a deterministic translator. Its
                                                                                                          Elab:   TYPE ONLY      BOTH FAIL
determinism makes the candidate’s surface form a function                    Semantic       Equivalent     fail      (TO)          (BF)
of the IR alone, attributing the +37 pp Opus-vs-GTED gap                    Equivalence
                                                                              Judges           Not
to elaborator-driven surface geometry rather than LLM sam-                                  equivalent
pling noise (§5.5). SAF ties Lean-Retry and Sample-Filter                     𝑐𝑜𝑚𝑝𝑎𝑟𝑒 𝜎ො against gold             TC% = (TS + SO) / n
on aggregate metrics. Its role here is diagnostic rather than                    formalization 𝜎 *                   SF% = TS / n
state-of-the-art optimization.
                                                                      Figure 1. Signal-coverage matrix: elaborator (pass/fail) × judge
                                                                      (equivalent/not) gives the 2×2 cell decomposition and TC%/SF%.
2. The Signal-Coverage Matrix
Under statement-level scope (NL statement S →                         3. Stratified Autoformalization
Lean 4 signature σ with := by sorry), an out-
put that fails its specification falls into exactly one               Because refinement signals are stratum-specialized (§2),
of two strata.         A type-stratum failure means σ                 SAF factors autoformalization through a typed intermediate
does not type-check (Unknown identifier, failed                       representation (IR). The LLM emits an IR, a determinis-
to synthesize, application type mismatch,                             tic ∼30-line translator produces Lean from it, and on elab
. . . ), so the math may be understood but the Lean surface           failure the IR is refined rather than Lean source. This deter-
form is invalid. A semantic-stratum failure means σ type-             minism is central: every refined SAF output is a function
checks but denotes a different proposition from S, for in-            of the IR alone. On the aggregate metrics, SAF ties Lean-
stance hardcoding ZMod 2 when S refers to “any field of               Retry and Sample-Filter on both TC and Opus-judged SF
size 2”, using Summable f when S asserts the sequence                 (§5). Its role in this paper is the causal-attribution probe of
has a limit, reversing an inequality, or dropping a hypothesis.       §5.5, where the +37 pp Opus-vs-GTED gap is attributed
(A third, implementation stratum for proof-level autoformal-          to elaborator-driven surface geometry rather than to LLM
ization is out of scope.)                                             sampling noise.

The two refinement signals used in practice are stratum-              The refinement loop (Algorithm 1) alternates IR generation
specialized. The Lean elaborator is complete on the type              by the LLM with elaborator checking until the candidate
stratum, since every failure raises an error, and silent on           type-checks. The total LLM budget is K+1 (one extraction
the semantic stratum, since a semantically wrong but type-            plus K refinements), and we use K=3 in all experiments.
correct σ elaborates without complaint. Semantic judges,              A SAF IR is a JSON object with five fields:
namely back-translation (Zhou et al., 2024) and GTED
                                                                       {
(Liu et al., 2025b), cover the semantic stratum but forgive                "imports":    ["Mathlib"],
the type stratum, since a non-compiling fragment back-                     "opens":      ["Polynomial", "Real"],
translates to noisy NL.                                                    "objects":    [
                                                                              {"name":"G","type":"Type*", "binding":
Crossing elaboration (pass / fail) with the semantic judgment                     "implicit"},
(equivalent / not-equivalent) partitions n outputs into four                  {"name":"", "type":"Group G","binding"
cells (Figure 1): true success (TS), type-only failure (TO),                      :"instance"},
semantic-only failure (SO), and both fail (BF). These labels                  {"name":"a","type":"G",      "binding"
                                                                                  :"explicit"}
denote failure modes, not correctness modes. The two off-                  ],

                                                                  2
                                The Signal-Coverage Matrix for Statement Autoformalization

     "hypotheses":[{"id":"h", "expression":"a                        cross-dataset runs serving as mechanism-direction checks
         *b = b*a"}],                                                at coarser (GTED-only) judge resolution.
     "conclusion": "<Lean 4 expression>"
 }
                                                                     Methods. Four methods, three at the same ∼4-LLM-call
                                                                     budget. Vanilla: one-shot. Lean-Retry (Guo et al., 2025-
Algorithm 1 SAF refinement loop                                      style): emit Lean signature, refine by feeding elaborator er-
Require: NL statement S, retry budget K                              rors back to the LLM, K=3 retries. Sample-Filter (Poiroux
Ensure: type-checked Lean signature, or ⊥                            et al., 2024-style): sample N =4 candidates, retain elab-pass
 1: ir ← LLM.extract IR(S)                                           candidates, pick first. SAF (this paper, §3): typed JSON
 2: for k = 0 to K do                                                IR refined against the elaborator, translated to Lean by a
 3:    σ ← ir to lean(ir)                                            deterministic ∼30-line procedure, K=3.
 4:    (ok, errors) ← LeanElaborator.check(σ)
 5:    if ok then                                                    Judges. A dual-judge protocol pairs Claude Opus 4.7 (An-
 6:       return σ                                                   thropic, disjoint from all four subject families) as the gold
 7:    end if                                                        cross-judge with GTED (Liu et al., 2025b) as the scalable
 8:    ir ← LLM.refine IR(S, ir, errors)                             symbolic proxy. Opus compares candidate Lean against
 9: end for                                                          gold Lean for semantic equivalence under a STRICT prompt
10: return ⊥                                                         when the candidate elaborates and an EQUIV-IF-FIXED
                                                                     prompt when it does not, yielding 744 verdicts on DeepSeek
The imports and opens fields carry the Mathlib en-                   V4-Pro × ProofNet# × {Vanilla, Lean-Retry, SAF, Sample-
vironment, objects declares typed binders with their                 Filter}, 244 on DeepSeek V4-Pro × MiniF2F × Vanilla,
binding mode, hypotheses lists named premises, and                   and 988 in total. GTED computes generalized tree edit dis-
conclusion holds the goal as a Lean 4 expression. The                tance on the LSP-extracted typed operator tree, returns a
ir to lean translator is a ∼30-line template substitution            similarity in [0, 1], is thresholded at τ =0.5, and runs on all
that maps each field to its Lean counterpart: imports                19 (model, dataset, method) combinations.
to import lines, opens to open lines, each objects
entry to a typed binder ((x : T) / {x : T} / [T]                     Infrastructure. Lean 4.19.0 via lean interact, pre-
per binding), hypotheses to hypothesis binders, and                  built Mathlib, ATLAS-based (Liu et al., 2025a) GTED
conclusion to the theorem body ending in := by                       LSP backend, elab timeout 60s, and JSONL resume on
sorry. The translator is purely template-based (no LLM,              all pipelines.
no fuzzy matching, no error recovery), and malformed IR
fails fast.                                                          5. Experimental Results and Analysis

4. Experimental Setup                                                5.1. Per-method cell decomposition
                                                                     For each of the 186 ProofNet# test problems run on
Datasets. ProofNet# (Poiroux et al., 2024) is the type-
                                                                     DeepSeek V4-Pro under each of the four methods, we record
complex benchmark: 186 undergraduate-textbook problems
                                                                     the elaborator label (pass / fail) and the Opus label (equiv-
(Rudin, Munkres, Dummit-Foote, Artin, Axler, Herstein,
                                                                     alent / not-equivalent), assigning each output to one of the
Pugh, Putnam, Ireland-Rosen, Shakarchi) exercising Math-
                                                                     four cells defined in §2. Table 1 reports the four-method ma-
lib typeclass machinery (Group, MeasurableSpace,
                                                                     trix, Figure 2 visualizes Vanilla’s cell counts, and Figure 3
ContinuousMap, Sylow, . . . ). MiniF2F-test (Zheng
                                                                     shows the cross-method TC / SF comparison (computed per
et al., 2022) is the type-simple benchmark: 244 olympiad
                                                                     Equation (1)). We use DeepSeek V4-Pro × ProofNet# as
problems admitting largely primitive-type formalizations.
                                                                     the running example because it is the only (model, dataset)
The two bracket the type-system complexity axis.
                                                                     cell with full four-method Opus dual-judging. Appendix E
                                                                     extends the same ∆TC / ∆SF comparison to the other five
Subject models. DeepSeek V4-Pro (49B active / 1.6T to-
                                                                     cells under GTED. The cell-level view is what lets us sep-
tal MoE parameters) is the primary subject, with the full bat-
                                                                     arate elaborator-side recovery (TO→TS) from semantic
tery on ProofNet# and three methods on MiniF2F. Qwen3.5-
                                                                     recovery (SO→TS) rather than read both off a single aggre-
Plus (Qwen Team, 2026) (480B-class) and MiMo-v2.5-
                                                                     gate rate.
Pro (Xiaomi MiMo Team, 2026) (Xiaomi, thinking traces
disabled) serve as cross-family direction checks. All de-            Vanilla decomposes as 95 / 16 / 61 / 14. Of the 91 failures,
coding is at temperature=0.0 except where N =4 sam-                  the elaborator catches 75 (TO + BF) and Opus catches
pling is the method itself. Gold-judge analysis is anchored          30 (SO + BF), with overlap of 14. The 77 / 186 outputs
on DeepSeek V4-Pro × ProofNet# , with cross-model and                off-diagonal (41.4%, SO + TO) are the per-instance dis-

                                                                 3
                                           The Signal-Coverage Matrix for Statement Autoformalization


                 signals agree        signals disagree                                                                                        TC %      Opus SF %


                                                                                                                 80                      75.8           76.3           75.3
                 TRUE SUCCESS               SEMANTIC-ONLY                                                                                       70.4           70.4           69.4




                                                                                        V4-Pro × ProofNet# (%)
                     95                           16
   Elab: pass                                                  111 (59.7%)                                            59.7
                                                                                                                 60
                                                                                                                             51.1
                     51.1%                         8.6%

                                                                                                                 40

                  TYPE-ONLY                    BOTH-FAIL

                                                                                                                 20
    Elab: fail
                     61                           14           75 (40.3%)


                     32.8%                         7.5%
                                                                                                                  0
                                                                                                                       Vanilla           Lean-Retry    Sample-Filter       SAF
                 BT: equivalent              BT: not equiv.
                  156 (83.9%)                    30 (16.1%)                            Figure 3. TC% and Opus-judged SF% across four methods on
                                                                                       DeepSeek V4-Pro × ProofNet# . The three elab-feedback methods
                                                                                       (Lean-Retry, Sample-Filter, SAF) cluster within ∼ 1 pp on both
Figure 2. Vanilla signal-coverage matrix (DeepSeek V4-Pro ×
                                                                                       axes.
ProofNet# ). Rose-outlined off-diagonal cells mark elaborator/O-
pus disagreements.
                                                                                       that land in Lean-Retry cell c′ , the net TS gain is given by

Table 1. Signal-coverage matrix on DeepSeek V4-Pro ×                                                             ∆|TS| = |TO→TS| + |SO→TS| + |BF→TS|
ProofNet# (n=186), four methods. Cells are defined in Figure 1,
                                                                                                                         | {z } | {z } | {z }
                                                                                                                                    23                 14              2
labels denote failure modes.                                                                                                                                                         (2)
                                                                                                                             − |TS→¬TS| = +36,
                                                                                                                               | {z }
Method             TS        SO           TO             BF   TC%       SF%                                                               3

Vanilla            95            16         61           14   59.7          51.1       attributing 23/36 ≈ 64% to type-stratum recovery and
Lean-Retry        131            10         41            4   75.8          70.4       14/36 ≈ 39% to semantic flip on the rescued side. Per-
Sample-Filter     131            11         37            7   76.3          70.4       cell individual rescue rates are: 96.8% of Vanilla TS stay
SAF               129            11         39            7   75.3          69.4
                                                                                       TS, 87.5% (14 / 16) of Vanilla SO problems are individu-
                                                                                       ally rescued, and only 37.7% (23 / 61) of Vanilla TO are
                                                                                       recovered, with the remainder stuck.

agreements between the two signals. The largest single                                 5.3. Semantic turnover and the gold-error floor
recovery target for any elab-only feedback method is the 61
TO cases: semantically correct outputs that the elaborator                             The aggregate SO count drops only from 16 to 10 under
nonetheless rejects on surface form.                                                   Lean-Retry, but this stability masks substantial per-problem
                                                                                       turnover. 14 of 16 Vanilla SO are individually rescued
The three elab-feedback methods add 34 to 36 problems
                                                                                       (87.5%), while Lean-Retry simultaneously creates 8 new
to TS, shrink TO by 20 to 24, shrink BF by 7 to 10, and
                                                                                       SO (4 from BF, 3 from TS regression, 1 from TO), for
shrink SO by only 5–6 from its baseline of 16, despite their
                                                                                       a net change of −6: aggregate stability hides a near-total
algorithmic differences (feedback vs. sampling, raw Lean
                                                                                       replacement of the underlying error population.
vs. typed IR). A bootstrap 95% CI (B=10,000, Table 9)
shows ∆TS and ∆TO significant for all three methods (CI                                Of the 2 Vanilla SO problems that remain SO under
does not cross 0), while ∆SO is not significant for any.                               Lean-Retry, both are gold-formalization bugs, verified
                                                                                       by Opus reasoning across all four methods. The first,
5.2. Per-problem transitions: TS gains come mostly                                     Ireland-Rosen|exercise 1 30, asks “Prove that
     from TO-rescue                                                                    1/2 + 1/3 + · · · + 1/n is not an integer.” Gold’s sum-
                                                                                              1
                                                                                       mand n+2   does not depend on the summation index, so the
Aggregate ∆s answer which cells moved on net. To resolve                               gold sum evaluates to n/(n + 2), a different proposition
which problems moved, we join each problem’s Vanilla                                   from the harmonic tail. The candidate faithfully formalizes
cell to its Lean-Retry cell, giving the 4×4 transition matrix                          the harmonic tail, and Opus correctly judges candidate ̸=
in Figure 4 and the per-cell decomposition of ∆|TS| in                                 gold under all four methods (Theorem 1).
Equation (2).
                                                                                       Example 1 (Buggy gold formalization, n=1).
Writing |c→c′ | for the number of problems in Vanilla cell c

                                                                                   4
                                                        The Signal-Coverage Matrix for Statement Autoformalization

                                              Lean-Retry cell
                                                                                        Table 2. Per-stratum recovery rates on DeepSeek V4-Pro ×
                            rescued (39)   new SO (8)
                                                                                        ProofNet# , dual-judged. ρc→TS (m) is the share of Vanilla cell c
                                TS            SO          TO     BF
                                                                                        that lands in TS under method m.

                       TS      92              3           .      .    95
                                                                                        Method                 TO→TS SO→TS BF→TS TS retain
                                                                                        Lean-Retry               37.7%      87.5%      14.3%      96.8%
                                                                                        SAF                      37.7%      75.0%      42.9%      92.6%
                       SO      14              2           .      .    16               Sample-Filter            37.7%      68.8%      28.6%      97.9%
        Vanilla cell




                                                                                        mean (cross-method)      37.7%      77.1%      28.6%      95.8%
                                                                                        half-spread                0 pp     9.4 pp    14.3 pp     2.6 pp
                       TO      23              1          35      2    61




                       BF       2              4          6       2    14
                                                                                        5.4. A predictive regularity: stratum-rates are
                                                                                             method-invariant
                                131           10          41      4    n = 186
                                                                                        The aggregate gains of §5.1 and the transition matrix of
                                                                                        §5.2 naturally raise the question: do the three elab-feedback
Figure 4. Per-problem Vanilla → Lean-Retry transition matrix.
Green column: rescue into TS. Orange column: newly created SO.
                                                                                        methods recover the same problems at the same rate, or do
Dotted diagonal: stay-put. Shade encodes count.                                         they merely converge in aggregate? For each Vanilla cell
                                                                                        c ∈ {TS, SO, TO, BF} and each elab-feedback method m,
                                                                                        define the recovery rate

 -- Gold: summand ‘(1 : Rat) / (n+2)‘ is                                                                  |{p : Vanilla(p) = c ∧ m(p) = TS}|
     constant in i,                                                                       ρc→TS (m) =                                          .
                                                                                                                  |{p : Vanilla(p) = c}|
 -- so the sum equals n/(n+2), not the                                                                                                         (3)
     harmonic tail.
 theorem exercise_1_30 {n : Nat} :                                                      Table 2 reports the four rates for each of the three elab-
   Not (Exists fun a : Int ⇒                                                            feedback methods.
     (Finset.sum (Finset.univ : Finset
         (Fin n))                                                                       All three elab-feedback methods recover exactly 23 of the
       fun _ ⇒ (1 : Rat) / (n+2)) = a)                                                  61 Vanilla TO problems, despite differing in algorithm (se-
                                                                                        quential elaborator feedback, deterministic IR refinement,
                                                                                        parallel N =4 sampling), in LLM call topology, and in can-
                                                                                        didate generation entropy. The point estimate has a wide
 -- Candidate (elab pass; Opus ̸= gold                                                  Wilson 95% CI of [26.6%, 50.3%] at n=61, so we do not
     under all 4 methods):                                                              claim the true rate is precisely 37.7%. What we claim, and
 -- faithful formalization of the harmonic                                              what the predictive regularity of Table 3 rests on, is that the
     tail.
 theorem exercise_1_30 {n : Nat} (hn : 2 ≤                                              three methods recover statistically indistinguishable popula-
      n) :                                                                              tions on the type stratum: per-method CIs overlap entirely,
   Not (Exists fun a : Int ⇒                                                            and a Fisher exact test of pairwise homogeneity returns
     (Finset.sum (Finset.Icc 2 n)                                                       p=1.00 for all three pairs. Appendix A gives Wilson CIs for
       fun k ⇒ (1 : Rat) / k) = a)                                                      every cell of Table 2 and discusses the limits of the n=186
                                                                                        sample. The semantic recovery rate is high and tighter than
                                                                                        the BF rate (the latter is small-n noise, 14 BF problems
                                                                                        total). The retention rate on TS is uniformly ≥ 92.6%, so
The companion case Dummit-Foote|exercise 7 2 2
                                                                                        net regression is small.
has gold LHS p | 0, trivially true in any commutative ring,
so the biconditional collapses to a one-sided statement                                 Taking any single elab-feedback method’s rates and apply-
(Appendix F, Case D). Both cases are documented with                                    ing them as a mass-balance rule to the Vanilla cell distri-
Opus traces and suggested corrections in the supplementary                              bution (|TS|, |SO|, |TO|, |BF|) = (95, 16, 61, 14) yields
note.                                                                                   a testable prediction for the other methods. With Lean-
                                                                                                        ˆ = 0.377·61 + 0.875·16 + 0.143·14 −
                                                                                        Retry’s rates, ∆TS
Across all four methods, only 1 of 186 problems is durably
                                                                                        (1 − 0.968)·95 = +36.0. Table 3 compares predicted to
SO (Ireland-Rosen|exercise 1 30). Under Lean-
                                                                                        observed: the calibration on Lean-Retry predicts the other
Retry the count rises to 2, both gold bugs. Excluding the
                                                                                        two methods’ ∆TS to within 2 of 186 problems, an order of
gold bugs, zero of 186 problems are durably semantic-only
                                                                                        magnitude better than the bootstrap noise band of any cell.
across the three elab-feedback methods, so the SO plateau
approximates the gold-error floor of the benchmark.                                     Extending across the six (model, dataset) cells of the cross-

                                                                                    5
                                    The Signal-Coverage Matrix for Statement Autoformalization

Table 3. Predicted vs. observed ∆TS on DeepSeek V4-Pro ×                    Table 5. Opus vs. GTED SF% on DeepSeek V4-Pro × ProofNet#
ProofNet# , using stratum-rates calibrated from Lean-Retry.                 outputs.

 Method            Predicted ∆TS      Observed ∆TS         Residual         Method           TC%         Opus SF%     GTED SF%         Gap
 Lean-Retry                 +36.0                 +36          0.0          Vanilla           59.7           51.1          44.1        +7.0
 SAF                        +36.0                 +34         −2.0          Lean-Retry        75.8           70.4          44.1       +26.3
 Sample-Filter              +36.0                 +36          0.0          SAF               75.3           69.4          32.3       +37.1
                                                                            Sample-Filter     76.3           70.4          43.5       +26.9
Table 4. Cross-cell fit of Equation (4) on six (model, dataset) cells
under Lean-Retry. Rows are grouped by benchmark.                            Table 6. GTED τ calibration against Opus. P = P (Opus equiv |
                                                                            GTED ≥ τ ), R is recall on the Opus-equiv elab-pass set. Rec-
Model                 Vfail % ∆T C obs. ∆T C pred. residual                 ommended row τ =0.5 in blue underline. Per-method ProofNet#
                 ProofNet# (type-complex, n=186)                            precision in Table 10.
DeepSeek V4-Pro         40.3        +16.1         +16.0       +0.1
                                                                                      MiniF2F, Vanilla        ProofNet# , 4-method pool
Qwen3.5-Plus            28.5        +12.9         +12.1       +0.8
MiMo-v2.5-Pro           32.3        +12.4         +13.4       −1.0           τ         P             R          P                 R
                  MiniF2F (type-simple, n=244)                              0.3      88.5%       62.0%        93.1%            75.1%
DeepSeek V4-Pro         12.7        + 6.1          + 7.0      −0.9          0.5      94.4%       45.5%        95.0%            51.0%
Qwen3.5-Plus             6.1        + 4.5          + 4.9      −0.4          0.7      97.8%       23.5%        98.1%            21.2%
MiMo-v2.5-Pro           13.5        + 8.6          + 7.3      +1.3


model panel, where the test is necessarily at the TC level                  bers (Table 5). SAF’s deterministic IR translator isolates the
(Opus dual-judging is anchored on the V4-Pro × ProofNet#                    cause.
cell), the recovery rate of Vanilla elab-fails under Lean-                  On Vanilla the two judges agree to within +7 pp. On
Retry fits a single linear regression in the Vanilla elab-fail              the three elab-feedback methods they disagree by +26
rate Vfail :                                                                to +37 pp, with Opus reading SF as rising and GTED
                                                                            reading it as flat or falling. The mechanism: GTED pe-
    ∆T
    \  C = 0.325 · Vfail + 2.88             (R2 = 0.957),        (4)
                                                                            nalizes surface-form normalizations (alternative opens,
with per-cell residuals in [−1.0, +1.3] pp (Table 4). The                   IsCompact univ↔CompactSpace, Fin n → R vs.
recovery rate of elab-fails (∆T C/Vfail ) is 41.2% on                       ∀i : N, Icc 0 1 restatements) that elab-feedback adopts to
ProofNet# (range [38.3, 45.3]) and 61.8% on MiniF2F                         satisfy the elaborator, while Opus recognizes these as seman-
(range [48.4, 73.3]): the same elab-signal recovers a strictly              tically equivalent. Theorem 2 is a representative instance on
higher share of failures on type-simple benchmarks because                  Munkres|exercise 29 4: gold and candidate denote
type-simple failures concentrate in the easy surface-form                   the same Π type, but GTED returns similarity 0.143 because
band that K=3 refinement resolves.                                          the extracted operator trees place an arrow node where the
                                                                            other places a ∀ binder.
Two consequences for method comparison follow. First, a
new method’s aggregate ∆T C is partially determined by its                  Example 2 (Surface-form gap, n=1).
target’s Vanilla cell distribution, not only by the method’s
algorithmic innovations: a method evaluated only on a type-                  -- Gold
complex benchmark will look weaker than the same method                      theorem exercise_29_4 :
on MiniF2F, by a benchmark-modulation factor predicted                         Not (LocallyCompactSpace
from Vfail alone. Second, the type-stratum recovery rate of                          (Nat → Set.Icc (0 : Real) 1))
23/61 is what current elab-feedback methods deliver, and
closing the gap to the elab-only ceiling (|TS|+|TO|)/n =                     -- Vanilla candidate (elab pass; Opus
83.9% would require recovering hard TO cases that survive                        equiv; GTED sim 0.143)
                                                                             theorem exercise_29_4 :
K=3 refinement, a population on which no current method
                                                                               Not (LocallyCompactSpace
makes progress (§6). The within-2/186 agreement is partly                            (forall i : Nat, Set.Icc (0 :
self-consistency, since the three methods already converge                               Real) 1))
in aggregate (Table 1).
                                                                            The gap is largest for SAF (+37 pp): with surface form fixed
5.5. Opus vs. GTED: the surface-form rewriting gap
                                                                            by the deterministic translator, divergence is the IR’s choice,
On the same 186 DeepSeek V4-Pro × ProofNet# outputs,                        not LLM sampling noise. Additional cases (TO→TS recov-
Claude Opus 4.7 and GTED τ =0.5 give different SF% num-                     eries, gold bugs) are catalogued in Appendix F.

                                                                        6
                                The Signal-Coverage Matrix for Statement Autoformalization

Table 7. Taxonomy of Opus-vs-GTED disagreements on DeepSeek          because SAF’s deterministic ir to lean translator does
V4-Pro × ProofNet# . Counts: problems with Opus equiv ∧
GTED < 0.5 ∧ elab-pass. Percentages: share of each method’s
                                                                     not freely restructure binders) but +20 in Z, reflecting the
false-negative pool.                                                 multi-category rewrites the IR-mediated path tends to pro-
                                                                     duce. The disagreement gap is therefore not random surface
 Method           N (%)     I (%)     S (%)     Z (%) Total          variance but a measurement of elaborator-driven structural
 Vanilla        4 (10.5) 6 (15.8) 14 (36.8) 14 (36.8)    38          rewriting, which is precisely the mechanism that recovers
 Lean-Retry    11 (17.7) 9 (14.5) 30 (48.4) 12 (19.4)    62          TO into TS (§5.2).
 SAF           11 (14.5) 8 (10.5) 23 (30.3) 34 (44.7)    76
 Sample-Filter 3 ( 4.8) 6 ( 9.7) 35 (56.5) 18 (29.0)     62          5.6. Cross-dataset: SO rate stable, TO rate scales with
                                                                          type-complexity
Table 6 confirms that τ =0.5 maintains 95.0% pooled preci-           DeepSeek V4-Pro × MiniF2F-test × Vanilla (244 problems,
sion on ProofNet# and ≥ 93% on every method individually             Opus-judged) decomposes as TS=163, SO=24, TO=51,
(per-method breakdown in Table 10). The threshold is sta-            BF=6. The SO rate is 9.8%, essentially unchanged from
ble across distributions, so the gap is a structural property        8.6% on type-complex ProofNet# . The TO rate, by con-
of elab-feedback’s surface rewriting rather than of judge            trast, drops from 32.8% to 20.9%. Dataset type-complexity
calibration.                                                         loads the type stratum and not the semantic stratum, pro-
                                                                     viding supporting evidence at Vanilla-only resolution for
The Opus-equiv but GTED-non-equiv set (n=38 on Vanilla,
                                                                     the mechanism of §5.2. Full MiniF2F dual-judge analysis
n ∈ [62, 76] on the three elab-feedback methods) is what
                                                                     across the four methods is future work.
drives the gap. We classify each case by the type of rewrite
that distinguishes the candidate from gold (rules and per-
                                                                     5.7. Cross-model: TC gain robust to subject model
method audit in Appendix D):
                                                                     Figure 5 reports TC% for three subject models on both
   • Notational (N). Surface rewrites that preserve def-             datasets. Lean-Retry ≥ Vanilla in 6/6 cells (mean ∆TC =
     initional shape: A->B vs. forall        : A, B,                 +10.1 pp). SAF ≥ Vanilla in 5/6, the one exception (Qwen
     Realˆn vs. Fin n -> Real, coercion (ZMod                        × ProofNet# , −12.9 pp) being a high IR-extraction failure
     2 for the unique field of order 2), alternative                 rate on Qwen3.5-Plus, reported without ad-hoc patching.
     open/namespace prefixes, or cosmetic renaming.                  Under GTED-only judging, ∆TC > ∆SF holds in 6/6 cells
   • Idiomatic (I). Definitional aliases or Mathlib for-             for Lean-Retry (mean +10.1 vs. +1.3 pp, Table 11).
     mulation swaps: IsConj vs. exists g, b =
     g*a*g−1 , Summable vs. Tendsto of partial sums,                 5.8. K-saturation: refinement saturates fast and three
     CompactSpace vs. IsCompact Set.univ, or                              methods converge
     LinearEquiv-via-Nonempty typeclass framing.                     Figure 6 plots SAF’s K-saturation on DeepSeek V4-Pro ×
   • Structural (S). Binder, quantifier, or typeclass restruc-       ProofNet# . TC% rises 50.5 → 72.0 → 74.7 → 75.3%
     turing that changes the post-elaboration term: let              across K=0, 1, 2, 3.       Refinement saturates at K=1
     vs. explicit hypothesis, instance binder vs. hypothe-           (+21.5 pp), with K=2, 3 contributing +3.3 pp combined.
     sis binder, [Field] vs. (h : Field), quanti-                    All three methods land within 1.0 pp at saturation (SAF
     fier moved inside or outside an existential, Iff direc-         75.3, Lean-Retry 75.8, Sample-Filter 76.3), so different
     tion swap, biconditional introduced or collapsed, or            topologies reach the same ceiling. Per-iteration faithful-
     subtype vs. predicate-restricted set.                           ness remains high: k ∗ =0: 89/94 (94.7%), k ∗ =1: 34/40
   • Residual (Z). Cases that mix multiple categories or             (85.0%), k ∗ =2: 5/5 (100%), and k ∗ =3: 1/1 (100%). Of the
     resist single-category classification.                          46 problems that never pass, 39 (84.8%) are Opus equiv-if-
                                                                     fixed (i.e., TO). The 16 durably TO across all four methods
Table 7 reads as follows. On Vanilla, 38 of 95 elab-pass             share a common failure mode: plausible but invalid Mathlib
outputs (40%) are surface-form rewrites Opus accepts but             API names that elab errors cannot prescribe (Appendix F,
GTED does not, distributed across all four categories. Under         Case E).
each elab-feedback method the false-negative count grows
by 24 to 38 problems. For Lean-Retry and Sample-Filter               6. Discussion and Limitations
the growth concentrates in category S (16 of 24 and 21 of
24 added cases, respectively): the elaborator pressures the          The (TC ̸= SF) gap itself is not new, but the per-stratum
LLM to restructure binders, typeclass formulations, and              quantification is. On type-complex benchmarks TC%
quantifier orderings until the output type-checks. SAF’s             alone is misleading: the recommended reporting unit is
growth is more diffuse: only 9 added in S (the smallest,             TC%, dual-judge SF%, and the per-cell decomposition

                                                                 7
                                                                               The Signal-Coverage Matrix for Statement Autoformalization

                                                                                                             Vanilla             Lean-Retry            SAF


                                                                                                                                              98.4
                                        100                                              93.4   95.5                                  93.9
                                                                                                                                                     96.3                                95.1   95.5
                                                                                  87.3                                                                                            86.5
                                                                                                                   84.4
                                                                                                                                                                    80.1
                                                               75.8    75.3                                                                                                75.3
                                         75                                                                71.5
                                                                                                                                                             67.7
                                 TC %




                                                       59.7                                                               58.6

                                         50


                                         25


                                          0
                                                      DeepSeek V4-Pro            DeepSeek V4-Pro            Qwen3.5-Plus               Qwen3.5-Plus          MiMo-v2.5-Pro        MiMo-v2.5-Pro
                                                         ProofNet#                   MiniF2F                 ProofNet#                   MiniF2F              ProofNet#              MiniF2F
                                                          (n=186)                    (n=244)                  (n=186)                    (n=244)                (n=186)              (n=244)


                                                                              Figure 5. Cross-model TC% on 3 models × 2 datasets × 3 methods.


                                  90                                                                                             newly created errors per method). Future signals must cor-
                                              Sample-Filter 76.3
                                                                                                                                 relate with semantic correctness rather than only distinguish
                                  85
                                                                                                                                 elab-pass from elab-fail.
 SAF TC % on ProofNet# (n=186)




                                              Lean-Retry 75.8
                                  80
                                                                                         74.7                                    SAF’s deterministic IR translation serves as a causal-
                                  75                                  72.0                                                       attribution probe for the surface-form rewriting mechanism
                                                                                                            75.3
                                  70                                                               +0.6                          (§5.5) and the per-stratum predictive regularity (§5.4). Two
                                                                               +2.7
                                                                                                                                 ProofNet# gold formalizations contain gold-formalization
                                  65
                                                                                                                                 errors             (Ireland-Rosen|exercise 1 30,
                                  60                                                                                             Dummit-Foote|exercise 7 2 2) and are docu-
                                                       +21.5                                                                     mented with suggested corrections in the supplementary
                                  55          50.5
                                                                                                                                 note. Benchmarks aiming to measure SO below 1% will
                                  50                                                              SAF (this paper)               need gold audits, not larger LLMs alone.
                                  45
                                                0                      1                  2                   3                  Our semantic labels rely on Claude Opus 4.7 as a strong
                                                                   Refinement budget K                                           cross-judge rather than expert Lean validators (≥ 94%
                                                                                                                                 pooled precision in §5.5). A small expert audit and a
Figure 6. SAF K-saturation on DeepSeek V4-Pro × ProofNet# .                                                                      canonicalization-aware symbolic metric (e.g. operator-tree
Dashed bands: Lean-Retry and Sample-Filter saturation levels.                                                                    matching after whnf reduction) would absorb most of the
                                                                                                                                 N/I taxonomy categories without an LLM judge. Both are
                                                                                                                                 natural follow-ups.
(TS/SO/TO/BF). Two elab-feedback methods compared
under a single symbolic judge can differ by ≥ 25 pp purely                                                                       7. Conclusion
from structural rewriting, so independent-LLM verification
is required for any SF% claim.                                                                                                   We decompose TC% gains via a 2×2 signal-coverage ma-
                                                                                                                                 trix and a 4×4 per-problem transition matrix. On DeepSeek
Why three methods converge. The collapse to within                                                                               V4-Pro × ProofNet# , three elab-feedback methods de-
∼1 pp TC% at saturation (§5.8), the identical 37.7%                                                                              liver +34 to +36 TS via ∼64% type-stratum recovery
TO→TS rate (§5.4), and the shared structural-rewriting                                                                           (Equation (2)), with SO net-flat but 87.5% per-problem
signature in the Opus/GTED gap (§5.5) are three views of                                                                         turnover. The TO→TS rate is 23/61 for each method
the same claim: at K≤3 the elab signal is largely exhausted                                                                      (Wilson 95% CI [26.6%, 50.3%]), cross-method calibra-
by the fixed ∼4-call budget, so all three refinement topolo-                                                                     tion predicts ∆TS to within 2/186, and ∆T C fits a linear
gies converge to the same family of type-checking surface                                                                        regression in the Vanilla elab-fail rate at R2 =0.96 across
forms. The remaining axis of progress is the signal itself,                                                                      six (model, dataset) cells. A dual-judge protocol (Opus and
not the topology on top of it.                                                                                                   GTED at 95% pooled precision) shows that single-judge
                                                                                                                                 SF% under-credits elab-feedback methods by ≥ 25 pp via
Per-output semantic faithfulness is unreliable under elab-                                                                       elaborator-forced structural rewrites.
feedback because of turnover (87.5% rescue offset by 8

                                                                                                                           8
                                 The Signal-Coverage Matrix for Statement Autoformalization

References                                                             Polu, S. and Sutskever, I. Generative language model-
                                                                         ing for automated theorem proving. arXiv preprint
Anthropic. The Claude 4 model family. https://www.
                                                                         arXiv:2009.03393, 2020.
  anthropic.com/claude, 2026. Model card.
                                                                       Qwen Team. Qwen3.5 technical report. https://
Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,            qwenlm.github.io, 2026. Technical report.
  Radev, D., and Avigad, J. Proofnet: Autoformalizing and
  formally proving undergraduate-level mathematics. arXiv              Wu, Y., Jiang, A. Q., Li, W., Rabe, M., Staats, C., Jam-
  preprint arXiv:2302.12433, 2023.                                      nik, M., and Szegedy, C. Autoformalization with large
                                                                        language models. Advances in Neural Information Pro-
Azerbayev, Z., Schoelkopf, H., Paster, K., Dos Santos, M.,              cessing Systems, 35:32353–32368, 2022.
  McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and
 Welleck, S. Llemma: An open language model for math-                  Xiaomi MiMo Team.        MiMo-V2.5-Pro: Reasoning
  ematics. In International Conference on Learning Repre-                model technical report. https://github.com/
  sentations, 2024.                                                      XiaomiMiMo, 2026. Technical report.

DeepSeek-AI. DeepSeek-V4 technical report. https://                    Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu,
  huggingface.co/deepseek-ai, 2026. Technical                            S., Godil, S., Prenger, R., and Anandkumar, A. Lean-
  report.                                                                Dojo: Theorem proving with retrieval-augmented lan-
                                                                         guage models. In Advances in Neural Information Pro-
Guo, Q., Wang, J., Zhang, J., Kong, D., Huang, X., Xi,                   cessing Systems, 2023.
 X., Wang, W., Wang, J., Cai, X., Zhang, S., and Ye,
 W. Autoformalizer with tool feedback. arXiv preprint                  Zheng, K., Han, J. M., and Polu, S. MiniF2F: a cross-system
  arXiv:2510.06857, 2025.                                                benchmark for formal olympiad-level mathematics. In
                                                                         International Conference on Learning Representations,
Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jamnik,         2022. doi: 10.48550/arXiv.2109.00110. URL https:
   M., Lacroix, T., Wu, Y., and Lample, G. Draft, sketch,                //arxiv.org/abs/2109.00110.
   and prove: Guiding formal theorem provers with infor-
                                                                       Zhou, J. P., Staats, C., Li, W., Szegedy, C., Weinberger,
   mal proofs. In International Conference on Learning
                                                                         K. Q., and Wu, Y. Don’t trust: Verify – grounding llm
   Representations, 2023.
                                                                         quantitative reasoning with autoformalization. In Inter-
Lin, H., Sun, Z., Welleck, S., and Yang, Y. Lean-STaR:                   national Conference on Learning Representations, 2024.
  Learning to interleave thinking and proving. In Interna-
  tional Conference on Learning Representations, 2025.

Liu, X., Bao, K., Zhang, J., Liu, Y., Chen, Y., Liu, Y.,
  Jiao, Y., and Luo, T. ATLAS: Autoformalizing theo-
  rems through lifting, augmentation, and synthesis of data.
  arXiv preprint arXiv:2502.05567, 2025a.

Liu, Y., Zhu, T., Liu, X., Chen, Y., Liu, Z., Guo, Q., Zhang,
  J., Bao, K., and Luo, T. Generalized tree edit distance
  (GTED): A faithful evaluation metric for statement auto-
  formalization. In ICML 2025 Workshop on AI for Math
  (AI4Math), 2025b. arXiv:2507.07399.

Lu, J., Wan, Y., Liu, Z., Huang, Y., Xiong, J., Liu, C., Shen,
  J., Jin, H., Zhang, J., Wang, H., Yang, Z., Tang, J., and
  Guo, Z. Process-driven autoformalization in lean 4. arXiv
  preprint arXiv:2406.01940, 2024.

OpenAI. Hello GPT-4o. https://openai.com/
  index/hello-gpt-4o/, 2024.

Poiroux, A., Weiss, G., Kunčak, V., and Bosselut, A. Im-
  proving autoformalization using type checking. arXiv
  preprint arXiv:2406.07222, 2024.

                                                                   9
                               The Signal-Coverage Matrix for Statement Autoformalization

A. Wilson 95% CI on per-stratum recovery rates
Table 8 gives Wilson 95% CIs for every entry of Table 2. Pairwise Fisher exact tests for homogeneity of the TO→TS rate
return p=1.0 for all three pairs (the observed counts are identical, 23/61 for each method). The semantic and BF recovery
rates have overlapping CIs across methods, consistent with a shared underlying rate plus small-sample noise. The wide BF
CI (±∼20 pp) reflects n=14 rather than instability of the recovery mechanism.

                                      Table 8. Wilson 95% CI for each entry of Table 2.

                 Method         TO→TS               SO→TS              BF→TS              TS retain
                 Lean-Retry    37.7% [26.6, 50.3] 87.5% [64.0, 96.5] 14.3% [ 4.0, 39.9] 96.8% [91.1, 98.9]
                 SAF           37.7% [26.6, 50.3] 75.0% [50.5, 89.8] 42.9% [21.4, 67.4] 92.6% [85.6, 96.4]
                 Sample-Filter 37.7% [26.6, 50.3] 68.8% [44.4, 85.8] 28.6% [11.7, 54.6] 97.9% [92.6, 99.4]



B. Bootstrap 95% CI on stratum-shift ∆s
Resampling is at the problem level rather than the cell level because the four cell counts on a given problem are coupled
(each problem contributes to exactly one cell per method), and intervals are the percentile method on B=10,000 resamples
(seed 20260512) on DeepSeek V4-Pro × ProofNet# (n=186). The interval containment pattern is uniform across the three
elab-feedback methods: ∆TS and ∆TO are bounded away from 0 for all three, ∆SO CIs all straddle 0, and ∆BF reaches
significance only on Lean-Retry, which gives the precise numerical backing for the qualitative claim of §5.1.

                 Table 9. Bootstrap 95% CI on ∆ vs. Vanilla (B=10,000). ∆BF significant only for Lean-Retry.

                      Method                    ∆TS              ∆SO             ∆TO             ∆BF
                      Lean-Retry    +36 [+25, +48] −6 [−15, +3] −20 [−31, −10] −10 [−17, −3]
                      SAF           +34 [+22, +47] −5 [−14, +4] −22 [−33, −11]   −7 [−15, 0]
                      Sample-Filter +36 [+25, +47] −5 [−14, +3] −24 [−35, −13]   −7 [−14, 0]



C. GTED τ calibration: per-method precision
Table 6 of §5.5 reports the 4-method pooled precision at τ =0.5 (95.0% on ProofNet# ). The breakdown below shows that
no single method drags the pool: per-method precision stays at ≥ 93.4% at τ =0.5 and rises monotonically with τ , so the
chosen threshold is robust to which method’s elab-pass outputs are pooled into the calibration set.

          Table 10. GTED precision at three thresholds, per-method on DeepSeek V4-Pro × ProofNet# elab-pass subset.

                                      τ     Vanilla Lean-Retry     SAF Sample-Filter
                                      0.3   87.4%       95.2% 95.7%              93.5%
                                      0.5   93.4%       97.2% 94.6%              94.5%
                                      0.7   96.3%      100.0% 100.0%             96.8%



D. Disagreement taxonomy: rules and audit
Table 7 of §5.5 reports a four-class classification of every Opus-equiv but GTED < 0.5 output on DeepSeek V4-Pro ×
ProofNet# , across four methods. Classes are defined as follows:

N (Notational). The rewrite preserves the operator-tree shape modulo Lean’s surface notation: A -> B ↔ forall :
    A, B, Realˆn ↔ Fin n -> Real, alternative open/namespace prefixes, coercion (ZMod 2 as representative for
    “any field of order 2”), Function.Injective ↔ Injective, and cosmetic variable renaming. GTED penalises
    these because its operator tree is extracted pre-reduction.
I (Idiomatic). The rewrite swaps one Mathlib idiom for a definitionally equivalent or near-equivalent one: IsConj
     ↔ exists g, b = g*a*g−1 , Summable ↔ Tendsto of partial sums, CompactSpace ↔ IsCompact

                                                             10
                                The Signal-Coverage Matrix for Statement Autoformalization

     Set.univ, LocallyCompactSpace ↔ Nonempty-wrapped LinearEquiv, generateFrom = sInf ↔
     generateFrom (sInter ...), etc.
S (Structural). The rewrite changes term structure: binder ordering, hypothesis hoisting (let-binding vs. explicit
     hypothesis vs. premise), typeclass formulation ([Field K] vs. (h : Field K), [Fact p.Prime] vs.
     Nat.Primes, [GCDMonoid R] vs. explicit gcd predicate), quantifier reordering across an existential or universal,
     Iff direction swap or biconditional collapse, implication-vs-biconditional substitution, subtype-vs-predicate-restricted-
     set, and hypothesis omission of vacuously-true premises (e.g. 0 < n when n=0 admits no counterexample).
Z (Residual). Cases mixing multiple categories (e.g. both a notational and a structural rewrite) or specific to NL ambiguity
    that do not cleanly map to one class.

Classification rules are encoded as a regex cascade evaluated in the order I → N → S → Z, and the first match wins. Rules
are tuned on the Opus rationale text, then frozen before the per-method counts were tabulated. The full classifier ships
with the supplementary script analysis/disagreement taxonomy.py, which also dumps the per-case rationale
string and assigned label for every entry in Table 7. Limitations of the classifier: (i) the Z bucket absorbs cases that mix
two structural levels or that the rationale describes ambiguously, and (ii) borderline I vs. N decisions (e.g. deriv[n] vs.
iteratedDeriv n) are made by the first matching rule rather than by adjudication. The dominant-class claim of §5.5
(that S grows under elab-feedback) is robust to these noise sources because S’s share rises by 12 to 20 pp between Vanilla
and the elab-feedback methods, well outside any plausible reassignment of the Z residual.

E. Cross-method TC/SF dissociation under GTED (6 (model, dataset) combos)
This table reports the GTED-judged ∆ vs. Vanilla on the five (model, dataset) cells outside the Opus-judged DeepSeek
V4-Pro × ProofNet# baseline of §5.1. The dissociation pattern reappears: ∆TC% is positive in 11 of 12 (method,
model, dataset) rows (up to +16.1 pp), while ∆SF% stays within ±5 pp in 11 of 12 rows and is non-positive in 6 of 12:
elab-feedback moves the elab axis without moving the semantic axis on every cell tested.

        Table 11. ∆ vs. Vanilla under GTED τ =0.5 across the six (model, dataset) cells. Left: ProofNet# . Right: MiniF2F.

           (a) ProofNet# (type-complex, n=186)                                    (b) MiniF2F (type-simple, n=244)

      Model              Method       ∆TC% ∆SF%                           Model               Method        ∆TC% ∆SF%
      DeepSeek V4-Pro    Lean-Retry    +16.1      0.0                     DeepSeek V4-Pro     Lean-Retry      +6.1     +0.8
      DeepSeek V4-Pro    SAF           +15.6    −11.8                     DeepSeek V4-Pro     SAF             +8.2      0.0
      Qwen3.5-Plus       Lean-Retry    +12.9     +4.3                     Qwen3.5-Plus        Lean-Retry      +4.5     +0.8
      Qwen3.5-Plus       SAF           −12.9     −5.4                     Qwen3.5-Plus        SAF             +2.4     +4.9
      MiMo-v2.5-Pro      Lean-Retry    +12.4     +1.6                     MiMo-v2.5-Pro       Lean-Retry      +8.6     +0.4
      MiMo-v2.5-Pro      SAF            +7.5     −5.4                     MiMo-v2.5-Pro       SAF             +9.0     −3.7



F. Case studies
Each case below shows the natural-language statement, the gold formalization, and one or more candidate outputs. Gold
and candidates are reproduced in Lean 4 syntax with implicit elaboration arguments preserved. Outcome tags use the cell
labels of §5.1. The five cases together cover the four mechanisms identified in the body: Case A is a TO→TS recovery
(§5.2), Case B a canonical GTED false negative driven by surface-form rewriting (§5.5), Cases C and D the two distinct
gold-formalization bug shapes that pin the durable SO floor (§5.3), and Case E a representative TO that survives K=3
refinement across all four methods (§5.8).

Case A: TYPE ONLY → TRUE SUCCESS under Lean-Retry (Dummit-Foote|exercise 11 1 13). NL.
“As vector spaces over Q, Rn ∼
                             = R, for all n ∈ Z+ .”
 -- Gold (Mathlib idiom)
 theorem exercise_11_1_13 {n : Nat} (hn : 0 < n) :
   Nonempty (LinearEquiv (RingHom.id Rat)
                         (Fin n → Real) Real)


                                                               11
                               The Signal-Coverage Matrix for Statement Autoformalization

 -- Vanilla (elab fail): ‘Realˆn‘ does not resolve to a type
 -- in this position (no ‘HPow Type Nat Type‘ instance)
 theorem exercise_11_1_13 {n : Nat} (hn : 0 < n) :
   Nonempty (LinearEquiv (RingHom.id Rat)
                         (Realˆn) Real)

 -- Lean-Retry K=1 (elab pass; matches gold idiom)
 theorem exercise_11_1_13 {n : Nat} (hn : 0 < n) :
   Nonempty (LinearEquiv (RingHom.id Rat)
                         (Fin n → Real) Real)

Opus judges equiv to gold under both STRICT and EQUIV-IF-FIXED prompts. One of 23 TO→TS recoveries.

Case B: GTED false negative on a surface-form rewrite (Munkres|exercise 29 4). NL. “Show that [0, 1]ω is not
locally compact in the uniform topology.”
 -- Gold
 theorem exercise_29_4 :
   Not (LocallyCompactSpace (Nat → Set.Icc (0 : Real) 1))

 -- Vanilla (elab pass; Opus equiv; GTED sim = 0.143)
 theorem exercise_29_4 :
   Not (LocallyCompactSpace
         (forall i : Nat, Set.Icc (0 : Real) 1))

The two function types are the same Π type with different surface notations (A -> B is itself notation for forall      :
A, B). The elaborator treats them identically. The typed operator tree GTED extracts from each is structurally divergent
(arrow node vs. ∀ binder), giving the 0.143 similarity. Canonical shape of the +26 to +37 pp Opus-vs-GTED gap on
elab-feedback outputs (§5.5).

Case C: Durable SEM ONLY from a buggy gold formalization (Ireland-Rosen|exercise 1 30). NL. “Prove
that 1/2 + 1/3 + · · · + 1/n is not an integer.”
 -- Gold: summand ‘(1 : Rat) / (n+2)‘ is constant in i,
 -- so the sum equals n/(n+2), not the harmonic tail.
 theorem exercise_1_30 {n : Nat} :
   Not (Exists fun a : Int ⇒
     (Finset.sum (Finset.univ : Finset (Fin n))
       fun _ ⇒ (1 : Rat) / (n+2)) = a)

 -- Candidate (elab pass; Opus ̸= gold under all 4 methods):
 -- faithfully formalizes the harmonic tail.
 theorem exercise_1_30 {n : Nat} (hn : 2 ≤ n) :
   Not (Exists fun a : Int ⇒
     (Finset.sum (Finset.Icc 2 n)
       fun k ⇒ (1 : Rat) / k) = a)

The gold theorem and the natural-language statement are different propositions: the gold sum is a rational n/(n + 2) rather
than the harmonic tail. The only problem durably SO across all four methods on DeepSeek V4-Pro × ProofNet# .

Case D: Durable SEM ONLY from a vacuous gold biconditional (Dummit-Foote|exercise 7 2 2). NL. “Let
p(x) = an xn + · · · + a0 ∈ R[x]. Prove that p(x) is a zero divisor in R[x] iff there is a nonzero b ∈ R with b · p(x) = 0.”
 -- Gold: LHS ‘Dvd.dvd p 0‘ is trivially true (p * 0 = 0),
 -- so the biconditional collapses to a one-sided Exists.
 theorem exercise_7_2_2 {R : Type*} [Ring R]
     (p : Polynomial R) :
   Iff (Dvd.dvd p 0)
       (Exists fun b : R ⇒ b ̸= 0 /\ b * p = 0)


                                                            12
                              The Signal-Coverage Matrix for Statement Autoformalization

-- Candidate (elab pass under Lean-Retry / Sample-Filter;
-- Opus ̸= gold): captures zero-divisor non-trivially.
theorem exercise_7_2_2 {R : Type*} [CommRing R]
    (p : Polynomial R) :
  Iff (Exists fun q : Polynomial R ⇒ q ̸= 0 /\ p * q = 0)
      (Exists fun b : R          ⇒ b ̸= 0 /\ b * p = 0)

Gold’s LHS is vacuous over any commutative ring, collapsing the biconditional to its right-hand side. Durably SO under
Lean-Retry and Sample-Filter. Under SAF the IR refinement loop fails to elaborate at all (BF). Both gold-formalization
bugs are documented with Opus reasoning traces in the supplementary note accompanying this submission.

Case E: Durable TO across all four methods (Dummit-Foote|exercise 3 4 5b). NL. “Prove that quotient
groups of a solvable group are solvable.”
-- Gold (Mathlib idiom): the class name is ‘IsSolvable‘.
theorem exercise_3_4_5b {G : Type*} [Group G] [IsSolvable G]
    (H : Subgroup G) [Normal H] :
  IsSolvable (G / H)

-- Vanilla (elab fail; Opus equiv-if-fixed):
-- uses ‘Solvable‘, but the Mathlib class is ‘IsSolvable‘.
theorem solvable_quotient {G : Type*} [Group G] [Solvable G]
    (H : Subgroup G) [H.Normal] :
  Solvable (G / H)

-- Lean-Retry K=3 (still elab fail; Opus equiv-if-fixed):
-- the elaborator reports ‘unknown identifier Solvable‘ but does
-- not surface the correct Mathlib name. The LLM only adjusts
-- binder syntax (‘[H.Normal]‘ → ‘[h : H.Normal]‘).
theorem solvable_quotient {G : Type*} [Group G] [Solvable G]
    (H : Subgroup G) [h : H.Normal] :
  Solvable (G / H)

Opus judges both candidates equiv-if-fixed: the mathematical content matches gold, only the Mathlib API name is wrong.
SAF and Sample-Filter likewise fail to elaborate at K=3 on this problem. One of 16 problems that remain TO across
all four methods on DeepSeek V4-Pro × ProofNet# : a canonical instance of the elab signal naming a symptom without
surfacing the cure.




                                                         13
