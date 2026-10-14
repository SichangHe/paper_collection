                                         Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis

                                         TAEWAN GOO∗ , BioNexus, Republic of Korea
                                         JUNSIK KIM∗ , Seoul National University, Republic of Korea
                                         KYULHEE HAN, BioNexus, Republic of Korea
                                         GWONYUL JO, BioNexus, Republic of Korea
                                         JONG-SOO KIM, BioNexus, Republic of Korea
                                         TAE-HYUNG KIM† , BioNexus, Republic of Korea
                                         Agentic LLM systems such as OpenScholar and PaperQA2 read the scientific literature and return cited answers, and both they and their
                                         benchmarks already check whether those citations hold, with a fixed attribution model or human graders. Neither audits the reliability
                                         of that check itself. We show it is not reliable, and that this matters. On identical agent outputs the measured unsupported-citation
                                         rate ranges from about 3% to about 18% depending only on the verifier’s strictness, and although verifiers agree on which citations are
                                         supported, they disagree on which to flag (negative-specific agreement 0.27 to 0.30), so no single flag set is trustworthy and cross-paper
                                         comparison is invalid without a named verifier and protocol.
arXiv:2607.20527v1 [cs.AI] 10 Jul 2026




                                             We present a gold-anchored evaluation protocol and a deployable guard that make this behavior measurable and bounded. The
                                         protocol validates the verifier, measures re-attribution, and calibrates a guarantee against human gold rather than another model’s
                                         verdict; the verifier is a swappable instrument chosen on cost (recall 0.94 on the supported class, held out), and re-attribution is a
                                         commodity step where a deterministic BM25 matches the best open generator. The guard adds a split-conformal layer placing a
                                         distribution-free, finite-sample bound on truly unsupported citations that slip past a chosen flagging rule, a guarantee on catch rate
                                         rather than conclusion correctness. The bound holds on held-out gold, and we identify and quantify the condition governing its
                                         transfer to deployment, calibration-negative difficulty, with a concrete recalibration recipe, left untested by prior conformal-factuality
                                         work.
                                             Validated across four open 27–35B models and three agentic pipelines on public benchmarks (SciFact, QASA, PubMedQA), with
                                         confidence intervals on every headline number, the protocol and guard ship as an open single-GPU kit.

                                         Additional Key Words and Phrases: citation faithfulness, attribution evaluation, conformal prediction, LLM-as-judge reliability,
                                         trustworthy AI


                                         1    Introduction
                                         Agentic literature-synthesis systems such as OpenScholar [4] and PaperQA2 [42] now operate in a closed loop of
                                         retrieval, reasoning, and writing, returning answers with citations to the scientific record. Such systems are part of a
                                         broader move toward agentic AI for science [13, 16, 18, 47]. For these agents the citation is the trust contract, telling the
                                         reader that a specific claim is backed by a specific source. A growing body of work checks that contract automatically
                                         and reports that AI citations are frequently unsupported [14, 48], and that even a factually correct citation may not
                                         faithfully reflect the passage the model actually used [46]. The agentic systems themselves do this too. OpenScholar
                                         scores citation support with a fixed attribution model and PaperQA2 with human graders. Yet these evaluations take
                                         the checker for granted, reporting a citation-support number without asking whether that judgment is itself reliable.
                                         ∗ Co-first authors.
                                         † Corresponding author and lead contact.


                                         Authors’ Contact Information: Taewan Goo, BioNexus, Suwon, Republic of Korea, taewan.goo@bionexus.kr; Junsik Kim, Seoul National University,
                                         Seoul, Republic of Korea; Kyulhee Han, BioNexus, Suwon, Republic of Korea; GwonYul Jo, BioNexus, Suwon, Republic of Korea; Jong-Soo Kim, BioNexus,
                                         Suwon, Republic of Korea; Tae-Hyung Kim, BioNexus, Suwon, Republic of Korea, thkim@bionexus.kr.
                                         Manuscript submitted to ACM                                                                                                                     1
2                                                                                                                  Goo et al.


    Evaluating this behavior at deployment scale is itself an intelligent-systems problem, because the judgment must then
be made by a model rather than by the human graders a one-off benchmark can afford. We begin from an uncomfortable
observation: the reported unsupported-citation rate depends on the verifier, and the verifiers do not agree. Deciding whether
a passage “supports” a claim is a judgment, and automated verifiers make it inconsistently and in disagreement with
one another. This is one instance of a fragility already documented for model graders in general [21, 28]: whenever an
evaluation hands a judgment to a model, the reported metric inherits that judge’s idiosyncrasies. Three gaps follow for
benchmarking agentic citation faithfulness. (G1) The reported unsupported-citation rate is verifier-dependent, so a
single number does not compare across studies. (G2) Verifiers agree on what is supported but disagree on what to flag,
so no single deployment flag set can be trusted. (G3) No method places a distribution-free guarantee on how many
truly unsupported citations slip through a chosen flagging rule. Our contribution is not the observation behind G1 and
G2 but its consequence for benchmarking, and a remedy: anchoring the metric on human gold to make G1 and G2
measurable, and wrapping an imperfect verifier in a conformal guarantee that closes G3.
    If deployment judgments cannot be trusted, the responsible move is to anchor evaluation on human gold labels,
where “supported” has a checkable meaning. We do this at three points: we validate the verifier against gold rather
than choosing it by reputation; we measure re-attribution accuracy against gold-labeled supporting passages rather
than against another verifier; and we calibrate a distribution-free guarantee on gold. The result is both an evaluation
protocol and a deployable guard that wraps an imperfect verifier in a finite-sample bound. Everything ships as an
open single-GPU kit. Figure 1 summarizes the design end to end. The result is a new evaluation protocol, benchmark
methodology, and reliability guard for a critical agentic behavior, faithful citation, in scientific-synthesis agents, treated
as an intelligent-systems evaluation problem in which the deployment metric is itself produced by a model. The
work spans formal analysis (a distribution-free finite-sample guarantee with a proof), evaluation methodology (the
gold-anchored protocol), and a deployable system (a single-GPU lab-audit kit).

    Contributions.

     • An agentic-evaluation finding (G1, G2). On agentic scientific synthesis we quantify how unreliable deployment
        citation-faithfulness judgments are: the same agent outputs score about 3% to about 18% unsupported across
        five gold-validated verifiers, and although the verifiers agree on which citations are supported, they disagree
        on which to flag (negative-specific agreement 0.27 to 0.30 among the three continuous-scored verifiers). That
        model graders are imperfect is known; we show it leaves no single deployment flag set trustworthy and makes
        cross-paper comparison invalid without a named verifier and protocol.
     • A gold-anchored evaluation protocol. We validate the verifier, measure re-attribution, and calibrate the
        guarantee against human gold labels rather than against another verifier’s verdict, turning an unreliable judgment
        into a checkable measurement.
     • A distribution-free guard (G3). Split-conformal calibration on gold converts an imperfect, moderate-agreement
       verifier into a finite-sample bound on unflagged-unsupported citations at a chosen tolerance; the bound holds
        empirically on held-out gold, and we show its transfer is governed by calibration-negative difficulty, so a
        deployment recalibrates on target-domain negatives rather than inheriting our threshold.
     • An open, reproducible kit. The protocol and guard run on one 80GB GPU or on CPU and are released under
        the MIT license at https://github.com/GooTec/citation-guard, so a laboratory can audit an agentic synthesis
        system on hardware it already has.

Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                                                                   3



                SUBJECT
                                 Generators                                   × 3 pipelines                                                  Cited answers
                         LM

                                 Gemma-4 ×2 ⋅ Qwen3.6 ×2             bare ⋅ OpenScholar ⋅ PaperQA2                                           {claim c, passage p} — audited

                                                                        audit the deployment outputs

                          S1 Rate                                   S2 Verifier                               S3 Calibration                     S4 Re-attribution
                Is there one trustworthy number?                Which instrument to trust?                     How to flag safely?              Find the true source cheaply?

                       Deployment outputs                           SciFact                                     QASA                                     QASA
       DATA




                                                                                                        Q&A                                     Q&A

                       generator × pipeline cites                   208 test + 802 train (human)                calibration = train / test               held-out test
       MODEL




                       5 verifiers                                  5 verifiers                                AttrScore + conformal                    BM25 vs generators
                       pooled comparison                            → AttrScore-3B                             the adopted stack                        lexical vs self-attr




                    No single number                        Comparable @ catch                                Guarantee holds                          Swappable slot
       RESULT




                    3–18% across verifiers;                      strict GPT-4o no better;                   catch-rate tracks target                   BM25 0.69 (CPU) ⋅
                     they disagree on flags                          adopt cheap local                    on held-out (contribution)                   Gemma 0.76 (GPU)

                                                                  adopt: AttrScore (S2) ⋅ BM25 / Gemma (S4) ⋅ conformal τ (S3)



                THE GUARD            − adopted stack, one GPU


                         VERIFY                                   RE-ATTRIBUTE                           FLAG                                   Audited citations
                                                                  BM25 (CPU)
                                                                                                         conformal τ                                  catch ≥ 1 − α
                         AttrScore-3B                             Gemma (GPU)                                                                         distribution-free

                               Anchor a verifier-dependent metric on human gold, then guarantee the catch-rate with conformal calibration.




Fig. 1. Study design. The agentic systems under audit (top) produce cited answers; four evaluation stages then anchor a verifier-
dependent metric on human gold and guarantee the catch rate. S1 Rate: the unsupported-citation rate has no single value across
verifiers. S2 Verifier: on SciFact gold the verifiers separate comparably at a matched catch rate, so the cheap local AttrScore-3B is
adopted on cost. S3 Calibration: split-conformal calibration on QASA gold turns the verifier score into a distribution-free catch-rate
guarantee (the contribution). S4 Re-attribution: recovering the true source is a swappable commodity slot (lexical BM25 on CPU, or
a generator on GPU). The adopted guard (verify → re-attribute → flag) runs on one GPU.


2     Related Work
2.1    Agentic AI for scientific synthesis
LLM agents increasingly conduct literature synthesis and discovery, from OpenScholar and PaperQA2 [4, 42] to
autonomous chemistry and biology agents [7, 16, 30, 43] and co-scientist systems [18]. These pipelines retrieve, reason,
and write in a loop, often with self-reflection [5, 41], meta-knowledge-guided self-correction [53], and corrective
retrieval [50]. Their scientific value rests on faithful citation, yet studies warn that agentic reasoning can also produce
confident, well-formed, but unsupported claims [33, 46].

2.2    Evaluating and benchmarking agentic systems
A large benchmarking literature evaluates agents on task success: AgentBench [29], GAIA [34], 𝜏-bench [51], Agent-
Board [31], tool use [20, 37], and software engineering [23], and surveys chart LLM and LLM-agent evaluation
broadly [8, 19]. A recent certification scheme issues assurances for LLM-based applications [6]. These measure whether
                                                                                                                                                      Manuscript submitted to ACM
4                                                                                                                 Goo et al.


an agent reaches a goal or certify high-level application properties. Our concern is orthogonal and finer-grained: not
whether the agent succeeds, but whether the evidence it cites actually supports what it writes, and crucially whether
that measurement is itself reliable. Where a certification scheme attests arbitrary application-level properties, we place
a distribution-free, finite-sample bound on one concrete, passage-level quantity, the unsupported-citation slip-through
rate, and treat the reliability of the metric as a first-class object.


2.3    LLM-as-judge reliability
Model-graded evaluation is now pervasive [24, 54], and so are its known failure modes: self-preference [36], sensitivity
to spurious features such as length [10], self-inconsistency [21], and the general difficulty of automatic attribution
evaluation [28]. Proposed mitigations include specialized judges [24], reward-model benchmarks [25], judge bench-
marks [44], and juries of diverse models [45]. We add a quantitative account of judge disagreement specifically for
citation support on agentic outputs, and, rather than seek a better judge, we anchor the metric on gold and bound the
residual error. A jury of the disagreeing verifiers does not resolve this: averaging idiosyncratic thresholds still has no
ground-truth anchor, and a majority-vote flag set inherits the same untrustworthy operating point we document; gold
anchoring supplies the reference that consensus cannot.


2.4    Citation and attribution evaluation
Attribution evaluation spans the AIS framework [39], ALCE [14], TRUE [22], AttrScore [52], RAGAS [12], CiteEval [49],
and medical citation auditing [48]. A separate line verifies whether a cited reference exists and whether its metadata
is correct, catching fabricated references [9, 26, 40]; our concern is the orthogonal one, whether a genuinely existing
passage supports the claim attached to it. AttributionBench shows this support judgment is hard even for strong
models [28], which motivates treating any single verifier’s verdict as uncertain.


2.5    Conformal and selective prediction
Conformal prediction provides distribution-free, finite-sample guarantees [3] and has been applied to language-model
factuality [35], conformal language modeling [38], and hallucination abstention [1], in the tradition of selective
prediction [11, 15]. The closest work bounds answer-level claim correctness; we instead place a distribution-free bound
on the passage-level unsupported-citation slip-through rate, a quantity specific to citation faithfulness.


3     Preliminaries and Problem Formulation
3.1    Notation and definitions
An agentic synthesis system answers a query by retrieving a set of passages 𝑃 = {𝑝 1, . . . , 𝑝𝑚 } and returning an answer
composed of cited sentences, which we decompose into claim–citation pairs (𝑐, 𝑝𝑖 ) where claim 𝑐 is a sentence and
𝑝𝑖 ∈ 𝑃 is the passage it cites. Table 1 collects the notation.

    Definition 3.1 (Verifier and support). A verifier is a function 𝑣 (𝑐, 𝑝) ∈ {0, 1} that judges whether passage 𝑝 supports
claim 𝑐, optionally exposing a continuous score 𝑠 (𝑐, 𝑝) ∈ [0, 1] that estimates the probability of support. A citation
(𝑐, 𝑝𝑖 ) is unsupported under 𝑣 if 𝑣 (𝑐, 𝑝𝑖 ) = 0. A gold label 𝑦 (𝑐, 𝑝) ∈ {0, 1} is a human annotation of support, available
only on benchmark data.

Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                     5

                                                   Table 1. Notation used throughout.


                           Symbol                   Meaning
                          𝑐                         a claim (a generated sentence)
                          𝑃 = {𝑝 1, . . . , 𝑝𝑚 }    passages retrieved for the query
                          (𝑐, 𝑝𝑖 )                  claim–citation pair; 𝑝𝑖 ∈ 𝑃 is the cited passage
                          𝑣 (𝑐, 𝑝) ∈ {0, 1}         verifier verdict (1 = supports)
                          𝑠 (𝑐, 𝑝) ∈ [0, 1]         continuous verifier score (probability of support)
                          𝑦(𝑐, 𝑝) ∈ {0, 1}          human gold support label (benchmark only)
                          𝛼                         tolerance; the target catch rate is 1 − 𝛼
                          𝜏                         flag threshold; flag the citation if 𝑠 (𝑐, 𝑝) ≤ 𝜏
                          𝑛 cal                     number of calibration (unsupported-class) scores


    Definition 3.2 (Unsupported-citation rate). The unsupported-citation rate of a system under verifier 𝑣 is the fraction of
its claim–citation pairs that are unsupported under 𝑣. As a function of both the outputs and 𝑣, it is meaningful only
together with the verifier and protocol that produced it.


3.2    Problem statement
Let a deployed agent produce claim–citation pairs whose true support status is unknown. A gold label 𝑦 (𝑐, 𝑝) ∈ {0, 1} is
a human annotation of support, available only on benchmark data. Two problems follow. (1) Measurement. The reported
unsupported rate is a function of both the outputs and the verifier; we ask how much it varies with the choice of 𝑣 and
how much verifiers agree on the per-citation verdict. (2) Guarantee. Given an imperfect verifier, we seek a flagging rule
that, for a chosen tolerance 𝛼, catches at least a 1 − 𝛼 fraction of the truly unsupported citations, with a finite-sample,
distribution-free guarantee calibrated on gold. The first problem establishes that no single verifier verdict can be trusted;
the second turns that imperfect verifier into a bounded triage.

4     Method
4.1    The verifier as a swappable measurement instrument
Any verifier is an automated judge that emits a continuous score 𝑠 (𝑐, 𝑝) separating supported from unsupported claims,
and different verifiers make different errors, so the verifier must be validated against gold before we trust anything it
reports. Because the conformal layer below is what controls the catch rate on unsupported citations, the verifier need
not be the strictest judge, only a good separator. We therefore compare gold-validated verifiers at a matched catch rate
and, finding their separation comparable, adopt the attribution-tuned 3B model AttrScore [52] on cost because it runs
locally. Its separation on gold is the signal the conformal layer turns into a guarantee (Figure 2).

4.2    Quantifying verifier disagreement
To measure how much the metric depends on the instrument, we score identical agent outputs with a panel of gold-
validated verifiers spanning the frontier, from high-recall AttrScore to a high-specificity natural-language-inference
(NLI) judge, with RAGAS [12] and a frontier judge in between. We report (i) the unsupported rate under each verifier
and (ii) class-specific pairwise agreement on a fixed sample of deployment citations. Because the supported class is
highly prevalent, we read negative-specific agreement (agreement on what to flag) rather than Cohen’s 𝜅 alone, which
the base rate depresses (the kappa paradox; Supplementary S2).
                                                                                                         Manuscript submitted to ACM
6                                                                                                                   Goo et al.


4.3    The conformal guard
The guard processes each cited sentence in three steps (Figure 1). It verifies the claim against its cited passage with the
3B verifier; if unsupported, it attempts to re-attribute the claim to another provided passage that supports it, keeping
the claim and fixing only the pointer; what cannot be repaired it flags rather than deletes. The verifier is imperfect, so a
hard threshold would have unknown error on new data. Split conformal removes that uncertainty. On a held-out gold
calibration set we choose a tolerance 𝛼 and set the flag threshold 𝜏 to the appropriate quantile of the unsupported-class
scores with a finite-sample correction:
                                                                                
                                            𝜏 = 𝑠 (𝑘 ) ,   𝑘 = (𝑛 cal + 1)(1 − 𝛼) ,                                         (1)

where 𝑠 (1) ≤ · · · ≤ 𝑠 (𝑛cal ) are the sorted scores of the calibration unsupported citations. Flagging every citation with
𝑠 (𝑐, 𝑝) ≤ 𝜏 then catches at least 1 − 𝛼 of the truly unsupported citations, in finite samples and without any assumption
on the score distribution; the only assumption is exchangeability between calibration and deployment.

    Proposition 4.1 (Finite-sample catch rate). Let the calibration unsupported-class scores 𝑠 1, . . . , 𝑠𝑛cal and a fresh
unsupported-class score 𝑠 new be exchangeable, and set 𝜏 = 𝑠 (𝑘 ) with 𝑘 = ⌈(𝑛 cal + 1)(1 − 𝛼)⌉. Then the rule “flag if 𝑠 ≤ 𝜏”
catches the new unsupported citation with probability at least 1 − 𝛼: Pr[ 𝑠 new ≤ 𝜏 ] ≥ 1 − 𝛼.

    Proof. By exchangeability the rank of 𝑠 new among the 𝑛 cal + 1 scores is uniform on {1, . . . , 𝑛 cal + 1}, so Pr[ 𝑠 new ≤
𝑠 (𝑘 ) ] ≥ 𝑘/(𝑛 cal + 1) ≥ 1 − 𝛼 by the choice of 𝑘. This is the standard split-conformal argument [3] applied to the
unsupported-class score distribution; it gives coverage ≥ 1 − 𝛼 under exchangeability and is exact for continuous,
tie-free scores. The discrete verifier score can tie; we break ties conservatively (treating 𝑠 new ≤ 𝜏 at equality), which
preserves the ≥ 1 − 𝛼 bound. This is what earns the word “guarantee” even when gold is scarce.                               □

    The bound is on the catch rate, the safety axis; we verify below that it holds empirically on held-out gold (Figure 4A).

4.4    Re-attribution
When a citation is flagged, the guard ranks the other provided passages, proposes the top-ranked one as a replacement
pointer, and re-verifies that candidate before the pointer is moved. The ranker is a swappable slot: we adopt a deterministic
lexical BM25 by default and compare it against the verifier’s own attribution score 𝑠 (𝑐, 𝑝 𝑗 ) and against the generators
asked to re-attribute their own citations. We evaluate re-attribution against gold: on data where a human-labeled
supporting passage exists, we measure how often the gold passage is ranked first or within the top 𝑘, scored against
truth rather than against the verifier that did the flagging. Because the ranker only proposes and the verifier disposes, a
lexical default is safe even though it cannot itself distinguish support from contradiction.

5     Experiments
5.1    Setup
    Agents and conditions. We audit four open instruction-tuned models in the 27–35B range, two dense and two
mixture-of-experts from the Gemma-4 and Qwen3.6 families [2, 17], run locally on a single GPU, across two published
agentic pipelines, OpenScholar and PaperQA2, against a bare no-retrieval floor. We hold the retrieved context fixed and
reproduce each system’s published prompting, so the rates reflect generation-time citation behavior rather than each
system’s own retrieval. Running every generator locally keeps the audit fully reproducible on commodity hardware. The
Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                                                               7


                                       (A) Matched catch-rate: comparable separation                              (B) Score separation on gold (n = 2750)
                                1.0                                                                         3.5                      unsupported (s ̄ = 0.20)
                                                                 catch 90%
                                                                                                                                     supported (s ̄ = 0.54)
                                                                                                            3.0
  Catch rate (on unsupported)




                                0.8
                                                                                                            2.5
                                0.6




                                                                                                  density
                                                                                                            2.0

                                0.4                                                                         1.5

                                                                                                            1.0
                                0.2                              DeBERTa-NLI (AUC 0.896)
                                                                 AttrScore-3B (AUC 0.884)                   0.5
                                                                 GPT-4o (AUC 0.873)
                                0.0                                                                         0.0
                                      0.0      0.2       0.4      0.6        0.8            1.0                   0.0       0.2       0.4        0.6            0.8   1.0
                                            Review cost (false-flag on supported)                                       Verifier score s(c, p) = P(attributable)


Fig. 2. The verifier as a swappable instrument, validated on gold. (A) Matched catch-rate frontier on SciFact: at any common catch
rate on unsupported citations the three verifiers separate comparably (AUC and review cost overlap), so a strict frontier judge buys
no advantage and the cheap local AttrScore-3B is adopted on cost. (B) The continuous score separates supported from unsupported
claims on gold (means 0.54 versus 0.20), the signal the conformal layer turns into a guarantee.


deployment citations we audit for the rate and disagreement analyses are these systems’ answers on the ScholarQABench
multi-paper tasks [4].

        Verifiers. Five gold-validated verifiers span the recall–specificity frontier: AttrScore-3B (high recall), an OpenScholar
post-hoc judge, GPT-4o, RAGAS, and a DeBERTa-NLI judge (high specificity).

        Gold data. Verifier validation uses SciFact (𝑛 = 208 human-labeled claim–passage test pairs, with a disjoint 𝑛 = 802
split used only for prompt selection). Re-attribution and conformal calibration use the full QASA test set (𝑛 = 1375), a
question-answering benchmark over research papers [27] with human-labeled supporting passages. A scope control
uses PubMedQA (𝑛 = 843).

        Metrics. We report per-class recall and specificity (not a single accuracy, which moves with class balance), Cohen’s 𝜅
with bootstrap 95% confidence intervals (CIs), unsupported-citation rates, re-attribution recall@𝑘 with binomial 95%
CIs, and conformal catch rate against the declared target.

5.2                             The verifier, a swappable instrument chosen on cost
Because the conformal layer controls the catch rate, the verifier need only separate the two classes well, so we compare
verifiers at a matched catch rate rather than at their native thresholds. On SciFact gold the continuous-scored verifiers
separate comparably (Figure 2A): their ROC-AUC values overlap (AttrScore-3B 0.88 [0.84, 0.93], DeBERTa-NLI 0.90
[0.85, 0.94], GPT-4o 0.87 [0.82, 0.92]; bootstrap 95% CIs, SciFact 𝑛 = 208), and at any common catch rate their review cost
is comparable, so a strict frontier judge such as GPT-4o buys no separation advantage over the local 3B model. Given
comparable separation, the verifier is a swappable instrument and the deciding factor is cost: we adopt AttrScore-3B
                                                                                                                                                Manuscript submitted to ACM
8                                                                                                                                   Goo et al.

Table 2. The verifier frontier on SciFact gold (𝑛 = 208): recall on the supported class (the safety axis) versus specificity. AttrScore-3B
sits at the high-recall end. The adopted verifier is re-validated on a disjoint held-out split (recall 0.94, 𝑛 = 802); full metrics, Cohen’s 𝜅
with CIs, and the prompt-selection comparison are in Supplementary S1.


                                                           Verifier                   Recall (supported)    Specificity
                                                           AttrScore-3B (adopted)            0.90              0.54
                                                           OpenScholar post-hoc              0.50              0.92
                                                           GPT-4o                            0.46              0.92
                                                           RAGAS                             0.30              0.96
                                                           DeBERTa-NLI                       0.25              0.97




                                                            Same outputs, verifier-dependent rate
                                                    20.0
                                                                       bare
                                                    17.5               OpenScholar
                                                                       PaperQA2
                        Unsupported citations (%)




                                                    15.0

                                                    12.5

                                                    10.0

                                                     7.5

                                                     5.0

                                                     2.5

                                                     0.0
                                                           AttrScore        OS-post        GPT-4o          RAGAS          DeBERTa
                                                             (.90)           (.50)          (.46)           (.30)           (.25)
                                                                          verifier (lenient → strict) ⋅ gold recall


Fig. 3. The unsupported-citation rate has no single value: on the same agent outputs it ranges threefold to sixfold across five
gold-validated verifiers ordered by recall. Most of the climb is the strict verifiers falsely rejecting genuinely supported citations.




because it runs locally on one GPU. Its native operating point is high recall on the supported class (0.90 on SciFact,
Table 2; 0.94 on a disjoint held-out split, 𝑛 = 802), which suits a guard that must not discard genuine citations, while the
per-class trade-offs of the stricter verifiers (DeBERTa recall 0.25/specificity 0.97; GPT-4o recall 0.46) explain the inflated
rates they report in Figure 3. Supplementary S1 gives the full per-verifier metrics, the matched-catch comparison, the
prompt-selection procedure, and the held-out validation.
Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                9


5.3   The unsupported rate is verifier-dependent
On the same agent outputs the measured unsupported rate rises monotonically as the verifier gets stricter, from about
3% at the bare floor under the high-recall verifier to roughly 14–18% under a strict NLI judge, with the agentic pipelines
a few points above the floor at each setting (Figure 3). Much of that climb is not extra unfaithfulness but extra false
rejection: the strict verifiers have low recall on genuinely supported claims (0.25 on gold), so their high rates partly
count supported citations. The rates are pooled over the four open models and three pipelines and stay single-digit at
the lenient end while climbing with verifier strictness, so the effect is a property of the verifier, not of any one generator.
We therefore report no single rate without naming its operating point; two unsupported rates from different papers are
not comparable unless they name the same verifier and protocol.

5.4   Verifiers disagree on what is unsupported
Disagreement runs deeper than the headline rate, and it is specifically about what to flag. On 300 cited sentences from
the deployed pipelines, three gold-validated verifiers spanning the recall–specificity range (AttrScore-3B, DeBERTa-NLI,
and the GPT-4o judge; the two binary-only judges, RAGAS and OpenScholar post-hoc, are omitted from this pairwise
analysis) agree strongly on which citations are supported (positive-specific agreement 0.90–0.96) but agree on which
to flag as unsupported only weakly (negative-specific agreement 0.27–0.30); concretely, 60 to 80% of the citations
one verifier flags, another calls supported. (Full agreement statistics, including observed agreement, Gwet’s AC1, and
Cohen’s 𝜅 with the base-rate caveat and CIs, are in Supplementary S2.) The verifiers thus encode genuinely different
flag thresholds: there is no single deployment flag set to trust. Everything load-bearing below, the verifier’s validation,
the re-attribution accuracy, and the conformal threshold, is therefore anchored on human gold rather than on a model’s
idiosyncratic cutoff.

5.5   The conformal guarantee holds in-distribution
Calibrated on QASA gold (the full test set, 1375 supported and 1375 unsupported pairs), the conformal flag rule’s
achieved catch rate tracks the declared target across the operating range on repeated held-out splits (Figure 4A), so
the distribution-free bound is empirical, not only asymptotic. This coverage is marginal over the calibration draw: an
individual split can fall below target, which is why we calibrate on as much gold as is available and recalibrate when
the target setting differs. The finite-sample correction is what earns the word “guarantee” when gold is scarce: at a
calibration size of 25 a naive empirical-quantile threshold under-covers (0.85 at a 0.90 target) while the conformal rule
holds (0.92); the gap closes by a calibration size of about 200 (Supplementary S3). At large calibration sizes the two
coincide, so the value of conformal here is distribution-free validity, not a numerical gain.

  Calibration-negative difficulty governs transfer. The bound is distribution-free only under exchangeability between
calibration and deployment negatives, and that assumption is consequential. Our calibration negatives are QASA in-
paper distractors, which are easy: the verifier scores them low (mean 𝑃 (attributable) = 0.20). Genuinely mis-cited claims
are harder, because the cited passage is on topic but does not support the specific claim; on SciFact’s human-labeled
unsupported claims the verifier scores them far higher (mean 0.50). A threshold 𝜏 calibrated on the easy distractors
to catch 90% of them therefore catches only 37% of the harder human-labeled negatives (44% and 61% at the 94% and
98% targets; Supplementary S6). The conformal machinery is not at fault: recalibrating 𝜏 on negatives drawn from the
deployment distribution restores the guarantee, at a higher review budget. The operational rule is therefore that the
calibration set must resemble the deployment negatives; the QASA coverage above is an in-distribution demonstration,
                                                                                                    Manuscript submitted to ACM
10                                                                                                                                                                     Goo et al.


                               (A) The guarantee holds                                                                   (B) Recall-cost dial (per-model band)
                                                                                                                  12
                        1.0           target (diagonal)                                                                                                          bare
                                      achieved (held-out)                                                                                                        OpenScholar
                                                                                                                  10                                             PaperQA2
                        0.9




                                                                                           Review cost (flag %)
  Achieved catch rate



                                                                                                                   8
                        0.8
                                                                                                                   6
                        0.7
                                                                                                                   4

                        0.6
                                                                                                                   2

                        0.5
                                                                                                                   0
                              0.5      0.6         0.7         0.8      0.9          1.0                                1.0      0.9       0.8      0.7          0.6       0.5
                                             Guaranteed recall 1 − α                                                                   Guaranteed recall 1 − α


Fig. 4. The conformal guarantee, calibrated on QASA gold (𝑛 = 1375). (A) The guarantee holds: the achieved catch rate tracks the
declared target 1 − 𝛼 on repeated held-out splits across the operating range (target 0.90/0.94/0.98 → achieved 0.90/0.94/0.98). (B) The
recall-cost dial, per open model: declaring a guaranteed catch rate fixes the review budget in advance. The verify → re-attribute →
flag pipeline itself is shown in Figure 1.


Table 3. Per-model review budget: flag rate (%) at a 90% guaranteed catch rate, by generator and pipeline (QASA-calibrated 𝜏). The
budget stays single-digit at the bare floor for every open model and rises with pipeline agency; no single model drives the pooled
rate. Each cell is 𝑛 = 250 deployment citations; Wilson 95% CIs span a few points (e.g. bare Gemma-4-26B 0.8% [0.2, 2.9], PaperQA2
Qwen3.6-35B 9.5% [6.5, 13.8]).


                                                            Generator         bare    OpenScholar                              PaperQA2
                                                            Gemma-4-31B       3.2                                 2.8              4.0
                                                            Gemma-4-26B       0.8                                 1.2              3.2
                                                            Qwen3.6-27B       2.0                                 6.4              7.6
                                                            Qwen3.6-35B       4.0                                 2.8              9.5
                                                            Pooled            2.5                                 3.3              6.1



and a deployment should recalibrate on target-domain negatives rather than inherit the QASA threshold. Identifying
and quantifying this calibration-negative-difficulty condition is itself part of the contribution: prior conformal-factuality
work names distribution shift as a limitation but does not characterize which shift matters, whereas we isolate one such
condition empirically and show how to restore the guarantee.
      The guarantee pays for safety in review effort, the genuine citations it also flags (Figure 4B). At a 90% guarantee,
pooled across the four open models, the flag rate at the high-recall operating point is about 3% for OpenScholar and 6%
for PaperQA2, against about 2.5% for the bare model: a few cited sentences per hundred sent for review. Table 3 breaks
the budget down by model: it stays single-digit at the bare floor for every open model and rises with pipeline agency,
with no single model driving the pooled figure.
Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                                        11


                                                Re-attribution: lexical BM25 (CPU) vs generator self-attribution (GPU)
                                          100
                                                      chance (random)
   Gold passage recovered, recall@1 (%)



                                                      BM25 — lexical, CPU (adopted)
                                                      verifier-score (AttrScore)
                                                      generator self-attribution, GPU
                                          80



                                          60



                                          40



                                          20



                                            0
                                                      random        Qwen3.6         Qwen3.6       guard        BM25     Gemma-4      Gemma-4
                                                                     27b             35b        (verifier)    (adopt)     31b          26b
                                                                                   QASA gold n = 1375 (100% coverage)


Fig. 5. Re-attribution validated against gold (QASA, 𝑛 = 1375, recall@1, 100% coverage). Recovering the supporting passage is a
swappable commodity slot: a deterministic lexical BM25 on CPU (0.69) matches the verifier score (0.58) and is reliable, while the open
generators run locally on GPU vary from 0.51 (Qwen) to 0.76 (Gemma). All crush the 3% random baseline. Wilson 95% CIs.


    Even a single-digit unsupported rate matters at synthesis scale, where one survey can carry hundreds of cited
sentences; the value is not a large defect rate but a bounded, declared review budget over many citations.

5.6                                 Re-attribution is a swappable, commodity slot
When a citation is flagged, recovering its true supporting passage among the provided candidates is an easy retrieval
task, and it is not where the contribution lies. On QASA gold (𝑛 = 1375; Table 4, Figure 5) every reasonable ranker
crushes the 3% random baseline and they form a clear order: a deterministic lexical BM25 reaches recall@1 0.69 on CPU,
the verifier’s own attribution score reaches 0.58, and the open generators asked to re-attribute their own citations range
from 0.51 (Qwen3.6) to 0.74–0.76 (Gemma-4) on GPU. The most accurate ranker is therefore a generator, not BM25
and not the verifier; but generator quality is model-dependent, and the advantage over BM25 is concentrated where it
is least needed. A lexical-overlap stratification (Supplementary S4) makes this concrete: on the half of items whose
answer shares vocabulary with the gold passage, BM25 and Gemma are tied (0.88 each); the generator’s edge appears
only on the low-overlap tail (0.31 versus 0.53 at the lowest-overlap quartile), exactly the cases that need reading for
entailment rather than matching words.
    Two properties make BM25 the sensible default for this slot despite not being the most accurate. It is deterministic and
free, with no model to host, 100% coverage, and reproducible output; and re-attribution is a retrieval step, not a support
                                                                                                                             Manuscript submitted to ACM
12                                                                                                                          Goo et al.

Table 4. Re-attribution recall@𝑘 on QASA gold (𝑛 = 1375, 100% coverage). The open generators (run locally on GPU) are most
accurate but vary by model; a deterministic lexical BM25 on CPU is close and reliable; all crush chance. Wilson CIs, the lexical-overlap
stratification, and the paired McNemar test (BM25 vs. verifier score) are in Supplementary S4.


                       Re-attribution ranker                  resource     recall@1      recall@3     recall@5
                       Gemma-4-26B (self-attribution)         GPU             0.76         0.86          0.87
                       Gemma-4-31B (self-attribution)         GPU             0.74         0.84          0.86
                       BM25 (lexical, adopted default)        CPU             0.69         0.83          0.87
                       Guard (verifier score)                 GPU             0.58         0.75          0.82
                       Qwen3.6-35B (self-attribution)         GPU             0.52         0.59          0.59
                       Qwen3.6-27B (self-attribution)         GPU             0.51         0.58          0.59
                       Random                                                              0.03




judgment, so a lexical ranker is appropriate. Crucially, a lexical ranker cannot tell support from contradiction: on SciFact
an answer and a refuting passage share almost identical vocabulary (Jaccard 0.064 versus 0.055), so BM25 would surface
a contradicting passage as readily as a supporting one, whereas the verifier separates them (mean 𝑃 (attributable) 0.83
versus 0.50; Supplementary S4). The division of labor is therefore deliberate: the re-attributor proposes a candidate by
lexical match, and the verifier then re-checks that the proposed passage actually supports the claim before the pointer is
moved. Because the slot is swappable, an operator already running a strong generator can plug it in for the low-overlap
tail; either way re-attribution is a commodity and the guard’s load-bearing value is flagging with a guarantee, not repair.
On real deployed outputs the picture is soberer still: most genuinely flagged claims are unsupported by any provided
passage, so there is no better source to move them to.


5.7   Worked examples
Two cases from the deployed outputs (Gemma-4 under PaperQA2 and OpenScholar) illustrate the guard’s two non-
trivial actions. Re-attribution. For the claim “these attacks are used to identify sensitive information leakage,” the cited
passage only states that word embeddings are trained on potentially sensitive data, so the verifier finds it unsupported;
BM25 then proposes another provided passage (“we quantitatively investigate how machine learning models leak
information. . . the membership inference attack”), the verifier confirms it supports the claim, and the guard moves the
pointer to it while keeping the sentence unchanged. Flagging. For the claim “unsupervised fine-tuning may require
further supervised or RL-based alignment for optimal performance,” the cited passage only compares fine-tuning with
retrieval-augmented generation and never makes the alignment claim; no other provided passage supports it either,
so the guard marks the citation [N UNVERIFIED] rather than deleting it, leaving the sentence for human review. Both
decisions are made by the external verifier on gold-validated scores, not by the generator that produced the citation.


5.8   Scope control
A scope control sharpens what the verifier does. Applied to PubMedQA, where the label is whether a study’s conclusion
is yes or no, the verifier shows near-zero agreement (𝜅 = 0.02, 𝑛 = 843). This is the intended result: the verifier checks
whether a passage supports a claim, not whether a conclusion is correct. The guard is a citation-faithfulness auditor for
agentic outputs, not a conclusion-correctness checker.
Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                             13


6    Discussion
The broader lesson is twofold: trust in machine-generated citations should be measured and bounded, not assumed, and
the measurement is itself a choice. The same agent outputs look several times worse under a strict verifier than a lenient
one, so a faithfulness number reported without its operating point is not a fact a reader can use. For agentic intelligent
systems this reframes evaluation: a benchmark leaderboard of citation faithfulness is meaningful only relative to a
named, gold-validated verifier and protocol, and a deployable agent needs not a better detector but a stated operating
point with a guarantee. We conjecture the same caution applies wherever a model or rubric stands in as judge of an
agent’s output, common across agentic evaluation, though our evidence here is limited to citation support.
    For a practitioner the guard changes the operating posture: rather than trust a verifier’s verdicts at face value, an
operator declares the residual risk they will tolerate and receives a written promise, conditional on the calibration
negatives resembling deployment and optimistic otherwise, on how many unsupported citations can survive review,
with the review budget that promise costs. The promise isolates a single checkable assumption, that calibration data
resemble deployed outputs; when that is in doubt, recalibrating on a small labeled sample from the target setting
restores it.


7    Limitations
The unsupported-citation rate is relative to a verifier’s operating point, so our numbers and any others in this literature
are interpretable only together with the verifier and protocol that produced them. We verify each claim against the full
cited passage with a sliding-window protocol so that support located anywhere counts; truncating the passage to a fixed
prefix, a tempting shortcut, inflates the apparent unsupported rate severalfold and must be avoided. The conformal
bound is conditional on exchangeability between calibration and deployed outputs, and this condition is consequential,
not cosmetic: our calibration negatives are easy in-paper distractors (verifier mean 𝑃 (attributable) = 0.20), whereas
genuinely mis-cited claims are harder (mean 0.50 on SciFact’s human-labeled unsupported claims), so a threshold
calibrated to catch 90% of the distractors catches only 37% of the harder human-labeled negatives (Supplementary S6).
The guaranteed catch rate must therefore be read as optimistic for real mis-citations, and a deployment must recalibrate
𝜏 on target-domain negatives, which restores the guarantee at a higher review budget; the QASA coverage we report is
an in-distribution demonstration of the method, not a transferable operating point. Our audit isolates the generation
step, holding retrieval fixed, so it does not capture errors each agent’s own retrieval would introduce. Re-attribution
helps only where an alternative supporting passage is present and is not guaranteed out of distribution, so the guard
must not be a sole gate in safety-critical settings, where expert review of flagged sentences remains required.


8    Conclusion
We treated the reliability of citation-faithfulness evaluation for agentic scientific synthesis as a first-class problem and
showed that deployment verifier judgments disagree enough that no single reported number is trustworthy. Anchoring
measurement on human gold and wrapping an imperfect verifier in a distribution-free conformal guarantee yields an
evaluation protocol and a deployable guard that hold despite that disagreement, released as an open single-GPU kit.
Two directions follow. The first is to raise the guarantee a level, from whether a passage supports a claim to whether
the full body of cited evidence adequately justifies it, accounting for contradiction and selective citation. The second is
to harden the calibration against adversarial and distribution-shifted inputs, so the bound still holds when an agent
                                                                                                  Manuscript submitted to ACM
14                                                                                                                                           Goo et al.


is optimized against the verifier [32]. A local, auditable guard of this kind is, in our view, a prerequisite for trusting
agentic systems that read and cite the scientific record.


Acknowledgments
The authors thank the maintainers of the open benchmarks and models used in this study.


References
 [1] Yasin Abbasi-Yadkori, Ilja Kuzborskij, David Stutz, et al. 2024. Mitigating LLM Hallucinations via Conformal Abstention. arXiv:2405.01563
 [2] Alibaba Qwen Team. 2026. Qwen3.6 Model Family. qwen.ai/blog.
 [3] Anastasios N. Angelopoulos and Stephen Bates. 2021. A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification.
     arXiv:2107.07511 Found. Trends Mach. Learn., 2023.
 [4] Akari Asai, Jacqueline He, Rulin Shao, et al. 2026. Synthesizing scientific literature with retrieval-augmented language models. Nature (2026).
     doi:10.1038/s41586-025-10072-4 OpenScholar; preprint arXiv:2411.14199.
 [5] Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. 2024. Self-RAG: Learning to Retrieve, Generate, and Critique through
     Self-Reflection. In Proceedings of ICLR. arXiv:2310.11511.
 [6] Nicola Bena, Marco Anisetti, Ernesto Damiani, Alex Della Bruna, Chan Yeob Yeun, and Claudio A. Ardagna. 2026. A Certification Scheme for Large
     Language Models-Based Applications. ACM Transactions on Intelligent Systems and Technology (2026). doi:10.1145/3819077
 [7] Daniil A. Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes. 2023. Autonomous chemical research with large language models. Nature 624
     (2023). doi:10.1038/s41586-023-06792-0
 [8] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, Wei Ye, Yue
     Zhang, Yi Chang, Philip S. Yu, Qiang Yang, and Xing Xie. 2024. A Survey on Evaluation of Large Language Models. ACM Transactions on Intelligent
     Systems and Technology 15, 3 (2024). doi:10.1145/3641289
 [9] Mikaël Chelli, Jules Descamps, Vincent Lavoué, et al. 2024. Hallucination Rates and Reference Accuracy of ChatGPT and Bard for Systematic
     Reviews. Journal of Medical Internet Research 26 (2024). doi:10.2196/53164
[10] Yann Dubois, Balázs Galambosi, Percy Liang, and Tatsunori B. Hashimoto. 2024. Length-Controlled AlpacaEval: A Simple Way to Debias Automatic
     Evaluators. arXiv:2404.04475 COLM 2024.
[11] Ran El-Yaniv and Yair Wiener. 2010. On the Foundations of Noise-free Selective Classification. Journal of Machine Learning Research 11 (2010).
[12] Shahul Es, Jithin James, Luis Espinosa-Anke, and Steven Schockaert. 2024. RAGAs: Automated Evaluation of Retrieval Augmented Generation. In
     Proceedings of EACL: System Demonstrations. doi:10.18653/v1/2024.eacl-demo.16
[13] Shanghua Gao, Ada Fang, Yepeng Huang, et al. 2024. Empowering biomedical discovery with AI agents. Cell 187 (2024). doi:10.1016/j.cell.2024.09.022
[14] Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. 2023. Enabling Large Language Models to Generate Text with Citations. In Proceedings of
     EMNLP. doi:10.18653/v1/2023.emnlp-main.398
[15] Yonatan Geifman and Ran El-Yaniv. 2017. Selective Classification for Deep Neural Networks. In Advances in Neural Information Processing Systems
     (NeurIPS). arXiv:1705.08500.
[16] Ali Essam Ghareeb, Benjamin Chang, Ludovico Mitchener, et al. 2026. A multi-agent system for automating scientific discovery. Nature (2026).
     doi:10.1038/s41586-026-10652-y Robin; preprint arXiv:2505.13400 (2025).
[17] Google DeepMind. 2026. Gemma 4: Frontier Multimodal Intelligence On-Device. deepmind.google/models/gemma/gemma-4.
[18] Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, et al. 2026. Accelerating scientific discovery with Co-Scientist. Nature (2026). doi:10.1038/s41586-
     026-10644-y Preprint arXiv:2502.18864 (2025).
[19] Shengyue Guan, Jindong Wang, Jiang Bian, Bin Zhu, Jian-Guang Lou, and Haoyi Xiong. 2026. Evaluating LLM-based Agents for Multi-turn
     Conversations: A Survey. ACM Transactions on Intelligent Systems and Technology 17, 4 (2026). doi:10.1145/3793671
[20] Zhicheng Guo et al. 2024. StableToolBench: Towards Stable Large-Scale Benchmarking on Tool Learning. ACL Findings (2024). arXiv:2403.07714.
[21] Rajarshi Haldar and Julia Hockenmaier. 2025. Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks. In Findings of the Association for
     Computational Linguistics: EMNLP 2025. doi:10.18653/v1/2025.findings-emnlp.1361
[22] Or Honovich, Roee Aharoni, Jonathan Herzig, et al. 2022. TRUE: Re-evaluating Factual Consistency Evaluation. In Proceedings of NAACL.
     doi:10.18653/v1/2022.naacl-main.287
[23] Carlos E. Jimenez, John Yang, Alexander Wettig, et al. 2024. SWE-Bench: Can Language Models Resolve Real-World GitHub Issues?. In Proceedings
     of ICLR.
[24] Seungone Kim, Juyoung Suk, Shayne Longpre, et al. 2024. Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language
     Models. In Proceedings of EMNLP. doi:10.18653/v1/2024.emnlp-main.248
[25] Nathan Lambert, Valentina Pyatkin, Jacob Morrison, et al. 2024. RewardBench: Evaluating Reward Models for Language Modeling. arXiv:2403.13787
     (2024).
[26] Junhyeok Lee. 2026. citecheck: An MCP Server for Automated Bibliographic Verification and Repair in Scholarly Writing. arXiv:2603.17339
Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                                                15


[27] Yoonjoo Lee, Kyungjae Lee, Sunghyun Park, Dasol Hwang, Jaehyeon Kim, Hong-in Lee, and Moontae Lee. 2023. QASA: Advanced Question
     Answering on Scientific Articles. In International Conference on Machine Learning (ICML) (PMLR, Vol. 202).
[28] Yifei Li, Xiang Yue, Zeyi Liao, and Huan Sun. 2024. AttributionBench: How Hard is Automatic Attribution Evaluation?. In Findings of the Association
     for Computational Linguistics: ACL 2024. doi:10.18653/v1/2024.findings-acl.886
[29] Xiao Liu, Hao Yu, Hanchen Zhang, et al. 2024. AgentBench: Evaluating LLMs as Agents. In Proceedings of ICLR. arXiv:2308.03688.
[30] Andres M. Bran, Sam Cox, Oliver Schilter, et al. 2024. Augmenting large language models with chemistry tools. Nature Machine Intelligence 6 (2024).
     doi:10.1038/s42256-024-00832-8
[31] Chang Ma, Junlei Zhang, et al. 2024. AgentBoard: An Analytical Evaluation Board of Multi-Turn LLM Agents. In Advances in Neural Information
     Processing Systems (NeurIPS).
[32] David Manheim and Scott Garrabrant. 2018. Categorizing Variants of Goodhart’s Law. arXiv:1803.04585
[33] Lisa Messeri and M. J. Crockett. 2024. Artificial intelligence and illusions of understanding in scientific research. Nature 627 (2024). doi:10.1038/s41586-
     024-07146-0
[34] Grégoire Mialon, Clémentine Fourrier, Craig Swift, et al. 2024. GAIA: A Benchmark for General AI Assistants. In Proceedings of ICLR. arXiv:2311.12983.
[35] Christopher Mohri and Tatsunori Hashimoto. 2024. Language Models with Conformal Factuality Guarantees. In Proceedings of ICML. arXiv:2402.10978.
[36] Arjun Panickssery, Samuel R. Bowman, and Shi Feng. 2024. LLM Evaluators Recognize and Favor Their Own Generations. In Advances in Neural
     Information Processing Systems (NeurIPS). arXiv:2404.13076.
[37] Shishir G. Patil et al. 2025. The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation. In Proceedings of ICML.
[38] Victor Quach, Adam Fisch, Tal Schuster, et al. 2024. Conformal Language Modeling. In International Conference on Learning Representations (ICLR).
     arXiv:2306.10193.
[39] Hannah Rashkin, Vitaly Nikolaev, Matthew Lamm, et al. 2023. Measuring Attribution in Natural Language Generation Models. Computational
     Linguistics 49, 4 (2023). doi:10.1162/coli_a_00486
[40] Kaize Shi, Wei Sun, Zhao Zhang, Li Sun, Nitesh V. Chawla, and Yanfang Ye. 2026. CiteAudit: You Cited It, But Did You Read It? A Benchmark for
     Verifying Scientific References in the LLM Era. arXiv:2602.23452
[41] Noah Shinn, Federico Cassano, Edward Berman, et al. 2023. Reflexion: Language Agents with Verbal Reinforcement Learning. In Advances in Neural
     Information Processing Systems (NeurIPS).
[42] Michael D. Skarlinski, Sam Cox, Jon M. Laurent, et al. 2024. Language agents achieve superhuman synthesis of scientific knowledge. arXiv:2409.13740
     PaperQA2.
[43] Kyle Swanson, Wesley Wu, Nash L. Bulaong, et al. 2025. The Virtual Lab of AI agents designs new SARS-CoV-2 nanobodies. Nature (2025).
     doi:10.1038/s41586-025-09442-9
[44] Sijun Tan et al. 2025. JudgeBench: A Benchmark for Evaluating LLM-Based Judges. In Proceedings of ICLR. arXiv:2410.12784.
[45] Pat Verga, Sebastian Hofstatter, Sophia Althammer, et al. 2024. Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse
     Models. arXiv:2404.18796 (2024).
[46] Jonas Wallat, Maria Heuss, Maarten de Rijke, and Avishek Anand. 2024. Correctness is not Faithfulness in RAG Attributions. arXiv:2412.18004
[47] Hanchen Wang, Tianfan Fu, Yuanqi Du, et al. 2023. Scientific discovery in the age of artificial intelligence. Nature 620 (2023). doi:10.1038/s41586-
     023-06221-2
[48] Kevin Wu, Eric Wu, Kevin Wei, et al. 2025. An automated framework for assessing how well LLMs cite relevant medical references. Nature
     Communications 16 (2025). doi:10.1038/s41467-025-58551-6 SourceCheckup.
[49] Yumo Xu, Peng Qi, Jifan Chen, et al. 2025. CiteEval: Principle-Driven Citation Evaluation for Source Attribution. In Proceedings of the 63rd Annual
     Meeting of the ACL. doi:10.18653/v1/2025.acl-long.1574
[50] Shi-Qi Yan, Jia-Chen Gu, Yun Zhu, and Zhen-Hua Ling. 2024. Corrective Retrieval Augmented Generation. In arXiv:2401.15884.
[51] Shunyu Yao et al. 2024. 𝜏 -bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. arXiv:2406.12045 (2024).
[52] Xiang Yue, Boshi Wang, Ziru Chen, et al. 2023. Automatic Evaluation of Attribution by Large Language Models. In Findings of the Association for
     Computational Linguistics: EMNLP 2023. doi:10.18653/v1/2023.findings-emnlp.307 AttrScore.
[53] Wei Zhang, Guojun Dai, Ding Luo, Yan Wang, and Chen Ye. 2026. From Hallucination to Certainty: Meta-Knowledge Guided Self-Correcting Large
     Language Models. ACM Transactions on Intelligent Systems and Technology (2026). doi:10.1145/3797906
[54] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, et al. 2023. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In NeurIPS Datasets and
     Benchmarks Track. arXiv:2306.05685.




                                                                                                                                Manuscript submitted to ACM
16                                                                                                                      Goo et al.


Supplementary Material
This supplement holds the detailed statistics and the reproducibility specification kept out of the main text. Section
numbers (S1–S6) are referenced from the main paper. All numbers are produced by the scripts in the released kit from
the result files under results/.

S1     Verifier validation, prompt selection, and held-out re-validation
Table S1 gives the full per-verifier metrics on the SciFact gold set (𝑛 = 208) used to draw the recall–specificity frontier
(main Figure 1, Table 1). Cohen’s 𝜅 is reported with a percentile-bootstrap 95% CI (2000 resamples).
Table S1. Per-verifier gold metrics on SciFact (𝑛 = 208). This is the development set on which the AttrScore prompt was selected;
absolute AttrScore numbers here are therefore optimistic (see Table S2).


                  Verifier                    Recall (supported)     Specificity    Cohen’s 𝜅        𝜅 95% CI
                  AttrScore-3B (adopted)             0.898              0.535          0.463      [0.332, 0.589]
                  OpenScholar post-hoc               0.496              0.916          0.339      [0.243, 0.449]
                  GPT-4o                             0.460              0.916          0.305      [0.207, 0.402]
                  RAGAS                              0.299              0.958          0.195      [0.123, 0.277]
                  DeBERTa-NLI                        0.248              0.972          0.164      [0.098, 0.236]


     Prompt selection and held-out re-validation. The AttrScore verifier prompt was chosen on the 𝑛 = 208 development set
for supported-class recall. To avoid reporting a selection-biased number, we re-validate the adopted prompt (“OURS”)
and a canonical alternative (“CANON”) on a disjoint held-out gold split (𝑛 = 802). Table S2 shows that OURS keeps the
highest recall on held-out (0.942), the safety axis, while CANON attains a higher 𝜅 (0.567) at lower recall (0.869). We
adopt the high-recall operating point deliberately: for a citation guard, discarding a genuine citation is costlier than an
extra review. Main-text numbers for the adopted verifier use the held-out values.
Table S2. AttrScore prompt selection (dev, 𝑛 = 208) versus held-out re-validation (𝑛 = 802). The dev ranking by 𝜅 does not carry to
held-out; we select on recall (the safety axis), not 𝜅.


               Split                 Prompt      Recall (supported)      Specificity   Cohen’s 𝜅        𝜅 95% CI
               dev (𝑛 = 208)         OURS               0.898               0.535         0.463       [0.332, 0.589]
               dev (𝑛 = 208)         CANON              0.664               0.690         0.328       [0.196, 0.455]
               held-out (𝑛 = 802)    OURS               0.942               0.483         0.384       [0.329, 0.435]
               held-out (𝑛 = 802)    CANON              0.869               0.722         0.567       [0.511, 0.624]


S2     Verifier agreement, full statistics
On 300 deployment citations, the supported class is highly prevalent (AttrScore 0.957, DeBERTa 0.823, GPT-4o 0.933), so
Cohen’s 𝜅 is depressed by the base-rate paradox even when observed agreement is high. We therefore report observed
agreement, Gwet’s AC1, and class-specific (positive and negative) agreement alongside 𝜅 (Table S3). All three verifiers
see the full cited passage: AttrScore and DeBERTa via 600/300 window tiling, GPT-4o via its long context (no truncation;
this fixes a prior one-sided head-slice for GPT-4o). The diagnostic that matters is negative-specific agreement, the
agreement on which citations to flag: it is only 0.27–0.30, whereas positive-specific agreement (on what is supported) is
0.90–0.96 and AC1 is 0.78–0.91.
Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                      17

Table S3. Pairwise verifier agreement on 300 deployment citations (symmetric full-passage protocol). 𝜅 and negative-specific agreement
with percentile-bootstrap 95% CIs (2000 resamples).


        Verifier pair               Obs. agree       Cohen’s 𝜅 [CI]          Gwet AC1      Pos. spec.      Neg. spec. [CI]
        AttrScore vs DeBERTa           0.840       0.218 [0.084, 0.359]        0.801         0.910       0.273 [0.129, 0.416]
        AttrScore vs GPT-4o            0.923       0.264 [0.051, 0.475]        0.914         0.959       0.303 [0.083, 0.500]
        DeBERTa vs GPT-4o              0.830       0.226 [0.091, 0.359]        0.784         0.903       0.301 [0.167, 0.427]



S3     Conformal calibration-size ablation
The main text reports marginal coverage over repeated held-out splits. Table S4 shows why the finite-sample correction
matters when gold is scarce: at a calibration size of 25, a naive empirical-quantile threshold under-covers the nominal
target, while the conformal (finite-sample corrected) rule maintains it. The gap closes by a calibration size of about 200.
Estimated over 𝐵 = 1000 random calibration/test splits (test 𝑛 = 200, seed 0); unsupported-class scores from QASA gold.

Table S4. Achieved catch rate (corrected conformal vs naive empirical-quantile threshold) by calibration size, at two targets. Naive
under-covers at small calibration sizes; the two coincide as size grows.


                                                      target 1 − 𝛼 = 0.90      target 1 − 𝛼 = 0.95
                                 Calibration size     corrected naive          corrected naive
                                 25                      0.922       0.848       0.960       0.922
                                 50                      0.900       0.881       0.961       0.941
                                 100                     0.901       0.892       0.951       0.942
                                 200                     0.901       0.896       0.951       0.946


     This coverage is marginal over the calibration draw; on an individual split it can fall below target, the standard
conformal caveat. We recommend recalibrating on a small labeled sample from the target setting when the deployment
distribution differs from the calibration distribution.

S4     Re-attribution is a swappable, commodity slot
All rankers are evaluated on the full QASA test set (𝑛 = 1375, 100% coverage), with the same gold definition, recall@𝑘,
and query, differing only in the ranker. Table S5 reports recall@𝑘 with Wilson 95% CIs. Every ranker far exceeds the 3%
random baseline. The open generators, run locally on GPU and asked to re-attribute their own citations, are the most
accurate but vary by model (0.51 to 0.76); a deterministic lexical BM25 on CPU is close and reliable (0.69); the verifier’s
own attribution score is a weaker ranker (0.58).

     Where the generator’s advantage lies (lexical-overlap stratification). BM25 ranks by word overlap, so its accuracy
should track the lexical similarity between the answer and the gold passage. We stratify the 1375 items by the maximum
token-Jaccard overlap between the answer and its gold passage and compare BM25 with the best generator, Gemma-4-
26B (Table S6). On the high-overlap half the two are tied (0.886 each); the generator’s advantage appears only on the
low-overlap half (0.64 versus 0.49) and is largest on the lowest-overlap quartile (0.53 versus 0.30), exactly the items where
support must be read for entailment rather than matched by words. The generator’s edge over BM25 is statistically
significant overall (McNemar exact two-sided 𝑝 = 1.4 × 10−9 ; 177 Gemma-only versus 80 BM25-only discordant hits at
                                                                                                          Manuscript submitted to ACM
18                                                                                                                        Goo et al.

Table S5. Re-attribution recall@𝑘 on QASA gold (𝑛 = 1375, 100% coverage); recall@1 with Wilson 95% CIs. Generators run locally on
GPU; BM25 runs on CPU. All far exceed the 3% random baseline. recall@1 carries Wilson 95% CIs; recall@3 and recall@5 CIs are
within ±0.02–0.03 of the point estimates (𝑛 = 1375).


                       Ranker                                      recall@1           recall@3     recall@5
                       Gemma-4-26B (self-attribution)         0.761 [0.737, 0.783]     0.860         0.874
                       Gemma-4-31B (self-attribution)         0.740 [0.717, 0.764]     0.844         0.856
                       BM25 (lexical, adopted default)        0.686 [0.661, 0.710]     0.834         0.875
                       Guard (verifier score)                 0.583 [0.556, 0.609]     0.755         0.820
                       Qwen3.6-35B (self-attribution)         0.516 [0.490, 0.543]     0.592         0.594
                       Qwen3.6-27B (self-attribution)         0.510 [0.483, 0.536]     0.584         0.586
                       Random                                                     0.033


𝑘 = 1), but it is concentrated on the entailment tail, so a free CPU ranker is a defensible default and a generator is a
drop-in upgrade where that tail matters.

Table S6. Lexical-overlap stratification: BM25 versus the best generator (Gemma-4-26B), recall@1 on QASA gold (𝑛 = 1375), by
answer–gold token-Jaccard overlap. They tie when words overlap; the generator’s advantage is confined to the low-overlap (entailment)
tail.


                                 Stratum                           𝑛      BM25     Gemma-4-26B
                                 High overlap (top 50%)           687     0.886         0.886
                                 Low overlap (bottom 50%)         688     0.494         0.635
                                   lowest-overlap quartile        344     0.299         0.529
                                 Overall                         1375     0.690         0.761



     A lexical ranker cannot judge support versus contradiction. Re-attribution and verification are separate components
because lexical overlap cannot distinguish a supporting passage from a contradicting one: both share the claim’s
vocabulary. On SciFact, supported and refuted claim–evidence pairs have almost identical answer–evidence Jaccard
overlap (0.064 versus 0.055), so a BM25 ranker would surface a contradicting passage as readily as a supporting one.
The attribution verifier separates them cleanly (mean 𝑃 (attributable) 0.83 on supported versus 0.50 on refuted). The
guard therefore uses BM25 only to propose a candidate and the verifier to judge whether the proposed passage actually
supports the claim before any pointer is moved.

S5     Reproducibility specification
     Generators. Four open instruction-tuned models, all run locally with vLLM on a single GPU at temperature 0
(greedy): google/gemma-4-31b-it (dense), google/gemma-4-26b-a4b-it (MoE), Qwen/Qwen3.6-27B-FP8 (dense,
Mamba-hybrid), Qwen/Qwen3.6-35B-A3B-FP8 (MoE). The exact HuggingFace snapshot revisions are pinned and
recorded in the kit (e.g. Qwen3.6-35B 95a723d0, Qwen3.6-27B e89b16eb, Gemma-4-31B 35487898). Full-passage
prompts up to the model context window, no truncation. Conditions: bare (no retrieval), OpenScholar, PaperQA2;
retrieved context held fixed, published prompts reproduced.

     Verifiers. AttrScore-3B (osunlp/attrscore-flan-t5-xl), DeBERTa-NLI (MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-
GPT-4o (openai/gpt-4o via OpenRouter, temperature 0; a non-deterministic API baseline whose raw per-citation
Manuscript submitted to ACM
Evaluating and Guarding Citation Faithfulness in Agentic Scientific Synthesis                                                19


verdicts are frozen in the kit for audit), RAGAS faithfulness, OpenScholar post-hoc. Support is judged over the full
passage via 600-char windows at stride 300 (supported if any window is attributable); claims capped at 600 characters
symmetrically.

     Gold data. SciFact (verifier validation, 𝑛 = 208 test / 𝑛 = 802 held-out), QASA (re-attribution and conformal calibration,
full test set 𝑛 = 1375, human-labeled supporting passages), PubMedQA (scope control, 𝑛 = 843), and ScholarQABench
multi-paper tasks (the deployment outputs: the four generators’ answers under each pipeline). The per-cell deployment-
citation samples (250 per model×pipeline for the conformal dial, 300 for the agreement analysis) are drawn in file
order and frozen in the kit. Dataset licenses and redistribution status of the derived score files are listed in the kit’s
DATA_LICENSES file.

     Calibration. Split-conformal with finite-sample quantile 𝑘 = ⌈(𝑛 cal + 1)(1 − 𝛼)⌉; calibration/test splits and all random
seeds are fixed (seed 0) and recorded.

     Compute. The verifier and guard run on one 80GB GPU or on CPU; the full kit reproduces in about two hours. Code,
configs, prompts, seeds, and the figure-generation script are released under the MIT license at https://github.com/
GooTec/citation-guard, tagged release v0.2.0 (commit b907985, the hash-anchored citable snapshot for this paper); a
Zenodo DOI will be minted from this tag for the camera-ready.

     What reproduces. The shipped reproduce/ kit is a cross-domain demonstration on a public BioASQ slice (𝑛 = 200),
not the headline. The main-text artifacts are regenerated by the experiment scripts from the frozen score files under
results/: the verifier frontier and matched-catch AUC (SciFact), the per-model unsupported rate (deployment outputs
× five verifiers), the conformal coverage and recall–cost dial, the coverage-transfer analysis (S6), and re-attribution
recall@𝑘 (QASA 𝑛 = 1375). Each headline number traces to a named result file; the QASA calibration entry point is
included.

S6     Calibration-negative difficulty and coverage transfer
The conformal bound is distribution-free only under exchangeability between the calibration and deployment negative
distributions. We quantify how much this matters by scoring two negative sets with the same adopted verifier (AttrScore-
3B 𝑃 (attributable), window-max): the QASA in-paper distractors used for calibration, and SciFact’s human-labeled
unsupported claim–evidence pairs, which are harder because the evidence is on topic but does not support the claim.
The distractors score low (mean 0.20, median 0.17); the human-labeled negatives score far higher (mean 0.50, median
0.53), a 0.30 gap in mean verifier score. Table S7 shows the resulting coverage transfer: a threshold 𝜏 calibrated on
the distractors for a target catch rate, applied to the harder negatives, under-covers substantially (e.g. 0.90 → 0.37),
because many harder negatives score above a 𝜏 tuned on easy ones. This is the standard exchangeability caveat made
quantitative. The split-conformal method remains valid; what it requires is a calibration set drawn from the deployment
negative distribution. Recalibrating 𝜏 on representative (harder) negatives restores the target catch rate at a higher flag
rate. We are not aware of prior conformal-factuality work that quantifies this calibration-negative-difficulty condition,
which we regard as part of the contribution.
     The Wilson 95% CIs (SciFact unsupported 𝑛 = 71) confirm the under-coverage is not a small-sample artifact. The
SciFact refuted pairs are a deliberately hard (near-upper-bound) proxy, in which the evidence is topically central but
contradicts the claim; real deployment negatives range between these and the easy distractors, so the achieved catch in
practice lies between the two columns. Restoring a 90% catch on the hard negatives requires 𝜏 = 0.83 and a ≈ 46% flag
                                                                                                     Manuscript submitted to ACM
20                                                                                                                           Goo et al.

Table S7. Coverage transfer from easy calibration negatives (QASA in-paper distractors, 𝑛 = 1375) to harder human-labeled negatives
(SciFact unsupported, 𝑛 = 71), same verifier and score. 𝜏 is calibrated on the distractors for each target catch rate; the achieved catch
on the human-labeled negatives is far below target.


            Target catch 1 − 𝛼        𝜏     catch on distractors        catch on human-labeled negatives (𝑛 = 71)
            0.90                    0.42             0.90                               0.37 [0.26, 0.48]
            0.94                    0.47             0.94                               0.44 [0.33, 0.55]
            0.98                    0.63             0.98                               0.61 [0.49, 0.71]
            Recalibrated on the harder negatives: 𝜏 = 0.83 restores catch 0.90, at a ≈ 46% deployment flag rate.


rate, i.e. the verifier’s separation, not the conformal layer, becomes the binding constraint in the hardest regime, where
stronger verifiers or human review are warranted.

     Recalibration recipe. To deploy with a meaningful guarantee: (1) label ≳ 200 flagged citations from the target system
as supported or unsupported (the S3 ablation shows the finite-sample correction has converged by ≈ 200); (2) run the
kit’s calibration entry point on these target negatives to obtain 𝜏 and its Wilson flag-rate CI; (3) deploy at that 𝜏 and
read off the review budget. The QASA-calibrated threshold should not be inherited.




Manuscript submitted to ACM
