                                                                                                                                            PREPRINT




                                         Physics as the label for measuring and
                                         correcting materials reasoning in multimodal
                                         models
arXiv:2609.12181v1 [cs.CV] 10 Sep 2026




                                         Hasan Kurban1,             Rasul Khanbayov1           Mustafa Kurban2,
                                         1
                                             College of Science and Engineering, Hamad Bin Khalifa University, Doha, Qatar
                                         2
                                             Ankara University, Ankara, Turkey
                                             Correspondence: hkurban@hbku.edu.qa, mkurbanphys@gmail.com


                                               ABSTRACT

                                               Vision–language and language models increasingly interpret materials data, yet benchmarks report
                                               that they hallucinate invalid properties and violate physical law. Evaluation matches final answers to
                                               scarce human labels, while discovery agents verify final proposals or density functional theory (DFT)
                                               execution. Neither measures the physical consistency of a model’s reasoning chain. Materials data
                                               carries its own physics, making a large class of materials reasoning verifiable without annotation. We
                                               introduce MatPCR, a label-free benchmark whose programmatic oracles check diffraction geometry
                                               through Bragg’s law, scale bars, spectral peaks, and Materials Project-grounded checks of near-hull
                                               stability, computed band-gap class, and net magnetization. We define the Physical-Consistency Rate
                                               over image and structure inputs; introduce Constraint-Grounded Self-Verification, an agentic loop
                                               whose gain survives self-refinement and equal-compute re-prompting controls; release an open verifier
                                               useful in distribution but near chance on all six held-out constraint types; and derive an exact identity
                                               for how oracle error displaces the reported rate.

                                         KEYWORDS       materials informatics; vision–language models; scientific reasoning; label-free evaluation;
                                         density functional theory




                                         Preprint • Kurban Intelligence Lab • https://github.com/KurbanIntelligenceLab/matpcr                              1
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                         Kurban Intelligence Lab




   Key contributions. (1) We reframe materials-model evaluation from answer accuracy to
   the physical consistency of the reasoning chain, checkable without human labels for a large,
   well-defined class of physical errors, across vision–language and language inputs. (2) We
   release MatPCR: programmatic, modality-specific physical oracles including DFT-grounded
   property checks. (3) We define PCR, a metric with bootstrap confidence intervals and a paired
   significance test, and prove an exact identity for the bias an imperfect oracle induces, which
   fixes what the oracle-validity gate must establish for the reported rate to be trustworthy.
   (4) We fine-tune and release an open physical-consistency verifier, a useful in-distribution
   detector whose transfer to six held-out constraint types is at or near chance, and benchmark
   it against zero-shot LLM-judge and self-confidence baselines. (5) We propose CGSV, a label-
   free agentic self-verification loop, isolate its effect from unaided self-refinement and equal-
   compute re-prompting controls, and give a protocol to measure its effect on violations.


1 Introduction
Materials data is governed by physics that is, in large part, programmatically checkable. A micro-
graph’s scale bar fixes its spatial calibration; a powder diffraction pattern’s peak positions follow
from a crystal structure and the source through Bragg’s law; a crystal’s thermodynamic stability is
set by its energy relative to a convex hull; and a computed property has a definite sign and order of
magnitude. Vision–language models (VLMs), built on open instruction-tuned architectures[1] as
well as closed frontier systems, and language models (LLMs) are now routinely asked to reason over
such data step by step, in the free-form chain-of-thought style now standard for eliciting multi-step
reasoning from these models,[2] and a large literature evaluates them on materials tasks;[3–6]
classical computer-vision pipelines for microstructure and defect analysis predate them.[7, 8]
    The problem this creates is now well documented. Materials benchmarks report that general-
purpose models hallucinate invalid property values[3, 9] and benchmark their spatial and structural
reasoning over crystals,[10] motivating purpose-built multimodal materials models.[11] Beyond
materials, recent work shows vision–language models violate basic physical law, for example
failing conservation under transformation;[12] in response, open vision–language models now add
physics-grounded reinforcement learning and inference-time self-verification to strengthen physics-
problem reasoning.[13] Across domains, a shared response has emerged: a model’s reasoning
should be audited against laws or logic in a reference-free way, whether through conservation-
grounded metrics or deterministic formal checks.[12, 14]
    That literature, like multimodal evaluation generally, scores the final answer against human
labels. A parallel and fast-growing line builds discovery agents that couple language models with
simulation and first-principles tools to propose and screen candidates;[15–25] some verify the
physics of final proposals, for example through physics-aware rejection sampling,[26] mitigate
hallucination during DFT execution,[15] or pre-screen candidates with machine-learned inter-
atomic potentials before DFT.[27, 28] General-domain methods verify chains of thought via visual
grounding or generic programs,[29–32] but against visual evidence or generic programs rather
than domain physics, and on general benchmarks rather than materials. A third line builds verifiers
and process-reward models that score reasoning steps;[33–35] these have driven reinforcement


                                                 2
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                         Kurban Intelligence Lab



learning from verifiable rewards in mathematics and code, where correctness is programmatically
checkable,[36] but verification has remained under-specified for scientific reasoning, where an-
swers are free-form and references are scarce.[37] Across all three lines, the physical consistency
of the model’s reasoning chain on materials data is neither measured nor made reusable. Yet that
is what determines whether a model can be trusted inside an analysis or screening pipeline: a
chain that reads a 100 nm scale bar and then reports a 10 𝜇m feature, assigns a peak to a 2𝜃 the
stated phase cannot produce, or calls a structure stable that lies far above the convex hull, is wrong
on its face. Checking the chain against external physics is also less susceptible than outcome- or
judge-based verification to a plausible but physically inadmissible chain: a model’s stated reason-
ing need not faithfully reflect its computation, so an unfaithful trace can satisfy a final-answer or
judge check while resting on physics that does not hold, whereas a programmatic oracle tests the
admissibility of the stated claims directly.[38]
   We make one observation: materials data contains directly checkable physical constraints for a
large class of reasoning errors, and first-principles databases extend these constraints from geome-
try to computed materials properties. These constraints are checkable with no human annotation,
yielding a label-free signal that scales with the available public data and that applies equally to
image inputs (VLMs) and structure or text inputs (LLMs). This brings to materials the reference-
free correctness signal that has driven progress in mathematics and code, though here the oracles
are imperfect-precision necessary conditions rather than the effectively exact checkers of those
domains. We turn this into MatPCR, a benchmark and a set of oracles including DFT-grounded prop-
erty checks; the Physical-Consistency Rate (PCR); Constraint-Grounded Self-Verification (CGSV);
and an open, fine-tuned verifier released as a reusable artifact (Fig. 1).
   The distinction from each neighboring line is precise. Against materials benchmarks that score
answers or property predictions,[3, 9–11] we score the physical consistency of the reasoning chain
rather than the final answer, with a label-free oracle. Against physical-law evaluations of model
reasoning,[12, 13] we ground the check in materials characterization and first-principles DFT, span
both image and structure inputs, and release a verifier and a label-free self-verification loop rather
than only a diagnostic. Against discovery agents,[15, 26] we measure reasoning-chain consistency
and act on oracle-flagged violations, rather than screen final proposals or run DFT. Against general
verifiers and process-reward models,[33–35] including recent step-level verifiers for scientific or
structured reasoning,[39, 40] we supply a domain-specific, physics- and DFT-grounded, label-free
signal for a setting where verification was previously under-specified. Those verifiers need an
answer key, a tool call, or gold reasoning annotation; our oracle needs none of these. The two
closest contemporaneous efforts use physics as a programmatic signal for materials models but
stop short of the reasoning chain: one benchmarks vision–language models on X-ray-diffraction
peak indexing, grading the final indexed answer against structure-derived labels on the diffraction
modality alone,[41] and the other uses DFT-computed energies and band gaps as a label-free reward,
but as a binary exact-match signal on the final answer during reinforcement-learning training
rather than a chain-level consistency measure at evaluation and inference time.[42] MatPCR differs
from both in scoring the physical consistency of the intermediate chain, spanning four oracle
modalities, and closing a label-free self-verification loop with a released verifier. To our knowledge
no single prior effort combines a label-free, reasoning-chain-level, multi-oracle, materials-specific
consistency benchmark with a self-verification loop and a released verifier.


                                                  3
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                                                                      Kurban Intelligence Lab



        a) Materials data fixes quantities a reasoning chain can be checked against

               • Diffraction                              • Micrograph                                    • Spectrum                                • Convex hull
                                   claimed 33◦                                                                    real maximum
                                                                    claimed 𝑑 = 10 𝜇m
        intensity                  ×                                                                                                                                     claimed stable




                                                                                                   intensity




                                                                                                                                                energy
                                                                                                                            claimed peak

                                                             100 nm
                                                                                                                                 ×


                                   2𝜃                                                                                  wavenumber                               composition

              admissible 2𝜃 from Bragg’s law              field of view from the scale bar               a peak needs a local maximum                     stable only if 𝐸hull ≤ 𝜖




        b) Each claim is tested againstmodel
                                        its own physics
                                             reasoning chain
                                                                                                                  c)     What the oracles actually catch

                    “. . . the strongest reflection sits near 2𝜃=33◦ , the particle is about                       Diffraction, 78 human-confirmed violations
                    10 𝜇m across, and the computed gap is small, so the phase is
                                                                                                               gridline or scale misreading                                          70.5%
                    metallic.”
                                                                                                                    peak misidentification                14.1%

                     peak at 2𝜃 = 33◦            feature ≈ 10 𝜇m        phase is metallic                                             other                15.4%
                                                                                                                   Microscopy, 93 human-confirmed violations

                         no reflec-              scale bar sets a                                                       scale-bar unit error                        37.6%
                                                                         computed gap
                        tion within                2.1 𝜇m field                                                            unit conversion                     23.7%
                                                                          0.02 eV ≤ 0.05
                         0.5◦ of 33◦                  of view
                                                                                                                    scale-factor arithmetic               14.0%
                                                                                                                                      other                    24.7%
                         × violation               × violation             ✔ consistent
                                                                                                                                               0%        20%   40%      60%      80%
                                        violations returned (CGSV, diffraction and spectra only)                          share of confirmed violations
              Schematic: the chain and the numbers illustrate the                              Spectra and the DFT families are excluded: their human
              checks; they are not a model output.                                             reviews predate the final oracle definitions.



Figure 1 Physics is the label. a) Materials data fixes quantities that a stated claim must respect: which
2𝜃 can carry a reflection, through Bragg’s law and the reference pattern of the named phase; the field of
view, through the calibration a scale bar sets; whether a claimed spectral peak coincides with a genuine
local maximum of sufficient prominence; and whether a composition lies within tolerance of the computed
convex hull. Each constraint is checkable with no human annotation. b) A chain is parsed into its checkable
claims and each claim is tested against the oracle for its own constraint type, returning a per-claim verdict
rather than a single score for the answer; detected violations are returned to the model by Constraint-
Grounded Self-Verification, which is applied to the diffraction and spectra constraint types only (Methods).
The chain and the values shown are schematic and illustrate the checks; they are not a model output. c) The
violations these oracles flag are legible physical mistakes, not parsing artifacts. For the two oracle families
whose human review postdates the final oracle definitions, an open-ended categorization of every confirmed
violation gives a small taxonomy: diffraction failures are dominated by misreading the gridlines or the axis
scale, and microscopy failures by scale-bar unit and unit-conversion errors, rather than by errors in the
arithmetic that follows. Percentages are shares of the 78 and 93 confirmed violations respectively (Methods).


   This work also extends a line of research by the present authors on multimodal resources
and benchmarks for crystalline materials,[43, 44] on machine-learning property prediction for
nanomaterials,[45, 46] on benchmarking model hallucination,[47] and on physics-grounded bench-
marks for dynamic systems.[48] MatPCR is distinct from each: rather than providing a dataset,
scoring generation or property prediction, or measuring text factuality, it measures the physi-
cal consistency of the reasoning chain itself and acts on the violations it finds, with label-free,
DFT-grounded oracles.




                                                                                               4
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                           Kurban Intelligence Lab



2 Results
All quantitative results below are measured, not projected. DFT-grounded numbers (stability, metallic-
ity, and magnetism-magnitude constraints, and every column or cell marked with ∗ ) rest on Materials
Project reference values.

2.1 Oracle validity: positive control and precision audit
Every downstream number rests on the oracles firing on genuine physical violations rather than
on parsing artifacts, so we validated the oracles before running any model (Table 1). In a positive
control we injected synthetic violations into real reference data at planted rates of 10%, 30%, and
50% and measured the fraction the oracle missed. All six oracle families recovered every planted
violation at every rate (maximum false-negative rate 0.0000), evidence that the oracles are complete
on the injected violation types; under the idealization that this completeness extends to genuine
violations (an oracle recall 𝑑̂ = 1; Methods), Corollary 2 gives PCR ≤ PCR⋆ for the true consistency
rate PCR⋆ , so the measured PCR does not overstate it for these oracles. We then audited oracle
precision by human review of at least 100 real oracle-fired cases per family, drawn from Qwen2.5-
VL-7B and Gemini 2.5 Flash Lite outputs on real data (the full real/false-positive/unsure breakdown
for all six families is shown in Supplementary Fig. S1). For diffraction and microscopy the audited
precision was 77.2% (XRD, 𝑛 = 101) and 88.6% (SEM, 𝑛 = 105). The XRD false positives were
predominantly a tolerance effect, with 16 of 23 disagreed cases within 1.0◦ of a real reference
peak, just outside the 0.5◦ tolerance (Fig. 2a shows three such real cases). The Raman spectrum
oracle was subsequently revised, mid-project, from a windowed-maximum check to a genuine-
local-maximum-with-prominence check (Methods), specifically because that first precision audit
(72.8%, 𝑛 = 103) showed the prominence criterion did not fully match human judgement of a
peak on noisy, baseline-drifting spectra. Authors completed a fresh precision audit of the revised
spectrum oracle, reviewing all 𝑛 = 495 oracle-fired cases produced under the corrected oracle:
audited precision is 92.7% (457 real violations, 36 false positives, 2 unsure, excluded from the ratio).
Root-causing the 36 false positives shows this is again predominantly a tolerance effect, not a
semantic mismatch between the oracle’s criterion and human judgement: 34 of 36 (94%) have a
claimed peak within 10 cm−1 of a real, independently detected local maximum, just outside the
oracle’s 5 cm−1 tolerance window (the same root cause already identified for diffraction’s false
positives, at a different tolerance); only 2 of 36 are genuinely far from any real peak (> 30 cm−1 ).
This is a substantially cleaner result than the pre-revision oracle’s audit, where most false positives
had no real peak-like structure at the claimed position at all – direct evidence the revision (Methods)
fixed a real semantic gap, not just moved the same failure mode around (Fig. 2b shows three such
real cases). For the three DFT-grounded families (stability, metallicity and property magnitude)
Table 1 reports audited precision of 95.3%, 94.7% and 92.2% at 𝑛 = 107, 114 and 115. This precision
pass reviewed all 336 oracle-fired cases across the three DFT-grounded families (107 near-hull,
114 computed band-gap, and 115 net-magnetization cases). During the positive control we found
and fixed one real oracle bug: the magnetization check compared the computed reference to zero
with exact floating-point equality, which misfired on 82 of 3000 real materials whose computed
magnetization is near but not exactly zero, and we replaced it with an absolute-tolerance zero
check.


                                                   5
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                                                           Kurban Intelligence Lab




                                           Peak-position inconsistencies flagged by the XRD pattern oracle
 a                                                            b                                                            c




     Model's claim:                                17.5 deg       Model's claim:                               34.0 deg         Model's claim:                               30.5 deg
     Nearest Bragg peak:                          ~17.0 deg       Nearest Bragg peak:                         ~34.5 deg         Nearest Bragg peak:                         ~30.1 deg
     Claimed position (17.5°) sits just outside the 0.5°          Claimed position (34.0°) sits just outside the 0.5°           Claimed position (30.5°) sits just outside the 0.5°
     tolerance around the nearest Bragg peak (~17.0°).            tolerance around the nearest Bragg peak (~34.5°).             tolerance around the nearest Bragg peak (~30.1°).

                                   Peak-position inconsistencies flagged by the Raman spectrum oracle
a                                                             b                                                             c




     Model's claim:                             870.0 cm ¹        Model's claim:                              830.0 cm ¹        Model's claim:                             1000.0 cm ¹
     Nearest strong peak:                       ~860 cm ¹         Nearest strong peak:                        ~845 cm ¹         Nearest strong peak:                        ~993 cm ¹
     Claimed position (870 cm ¹) falls outside the 5 cm ¹         Claimed position (830 cm ¹) falls outside the 5 cm ¹          Claimed position (1000 cm ¹) falls outside the 5 cm ¹
     tolerance around the nearest strong peak (~860 cm ¹).        tolerance around the nearest strong peak (~845 cm ¹).         tolerance around the nearest strong peak (~993 cm ¹).

                                       Scale-bar inconsistencies flagged by the SEM plausibility oracle
 a                                                             b                                                            c




Model's claim:                                     100.0 µm Model's claim:                                      150.0 µm Model's claim:                                         10.0 µm
Scale bar:                                             1 µm Scale bar:                                            10 µm Scale bar:                                                1 µm
Claimed size (100 µm) exceeds the field of view               Claimed size (150 µm) exceeds the field of view              Claimed size (10 µm) exceeds the field of view
implied by the 1 µm scale bar by ~100×.                       implied by the 10 µm scale bar by ~10×.                      implied by the 1 µm scale bar by ~10×.

Figure 2 Representative inconsistencies identified by the multimodal oracles. a, X-ray diffraction
cases in which the model-reported 2𝜃 position lies outside the 0.5◦ tolerance around the nearest genuine
Bragg reflection. b, Raman spectroscopy cases in which the model-reported Raman shift exceeds the 5 cm−1
tolerance relative to the nearest genuine spectral peak. c, Microscopy cases in which the model-reported fea-
ture size is inconsistent with the physical scale indicated by the embedded scale bar, producing discrepancies
of approximately 10–100×. All examples are human-confirmed oracle activations and illustrate representa-
tive tolerance, unit-conversion, and scale-factor failure modes.




                                                                                            6
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                Kurban Intelligence Lab


Table 1 Oracle validity. The positive-control false-negative rate is the maximum across three planted
violation rates (10%, 30%, and 50%); all three rates yielded 0.0000 for every oracle family. Audited precision
is the fraction of oracle-fired cases from Qwen2.5-VL-7B and Gemini 2.5 Flash Lite outputs that human
review confirmed as genuine violations of the stated constraint rather than parsing or oracle artifacts. The
spectrum result reflects the revised local-maximum-with-prominence oracle (Methods), evaluated over all
495 oracle-fired cases; the pre-revision result (72.8%, 𝑛 = 103) is reported only for transparency. The
three Materials Project-grounded results were obtained using the final operational definitions: near-hull
classification, computed band-gap classification with an abstention band, and net-magnetization magnitude.

                        Oracle family             Data source            FN rate         Audited precision

                                                                      positive control     human audit

                        Geometric oracles (gate passed)
                        Diffraction (XRD)           opXRD                 0.0000          77.2% (𝑛=101)
                        Microscopy (SEM)            NFFA-EUROPE           0.0000          88.6% (𝑛=105)
                        Spectra (Raman)             RRUFF                 0.0000         92.7% (𝑛=495)†

                        DFT-grounded oracles
                        Stability (hull)          Materials Project       0.0000          95.3% (𝑛=107)
                        Metallicity (band gap)    Materials Project       0.0000          94.7% (𝑛=114)
                        Magnetism (magnitude)     Materials Project       0.0000          92.2% (𝑛=115)



    † Revised oracle (genuine local-maximum-with-prominence check); supersedes an earlier pre-revision figure of 72.8% (𝑛 = 103),

see Results.


2.2 Physical consistency of current models
We measure the Physical-Consistency Rate and per-constraint-type violation rates for the four
originally evaluated models, four later-generation frontier or open models, and one flagship-tier ad-
dition across diffraction, microscopy, spectra, and DFT-grounded constraints, separately for image
(VLM) and structure or text (LLM) inputs (Table 2, Fig. 3a), 𝑛 = 30 items per (model, constraint-
type) cell per seed, 𝑆 = 3 seeds pooled per cell (4,472 checkable records in total across the nine
models). These numbers supersede an earlier pass: the spectrum oracle was revised mid-project
from a windowed-maximum check to a genuine-local-maximum-with-prominence check (Meth-
ods), which lowered every model’s spectra column substantially, and the magnetism oracle was
redesigned to a per-atom-normalized magnitude check that never compares sign (Methods); both
changes are oracle corrections, not model regressions, and every number below reflects the cor-
rected oracles. Overall PCR ranges from 0.555 (Qwen3-VL-8B-Instruct) to 0.774 (GPT-5.6-Terra);
models are markedly more consistent on microscopy (0.67–1.00) than on spectra (0.07–0.83) or
diffraction (0.47–0.82), and the DFT-grounded column is more tightly clustered (0.64–0.74) than any
single geometric constraint, without one constraint type standing out as uniformly hardest once
the corrected oracles are applied. The later-released API models do not uniformly outperform their
earlier siblings: GPT-5.6-Terra improves clearly over GPT-4o overall (0.774 vs. 0.687, bootstrap
95% CIs [0.736, 0.810] vs. [0.643, 0.728], not overlapping), but Claude Opus 4.6 does not improve
over Claude Sonnet 4.5 (0.655 vs. 0.656, CIs overlapping), and the reasoning-mode Qwen3-VL-
8B-Thinking does not improve over its non-reasoning sibling (0.579 vs. 0.555, CIs overlapping).
Explicit reasoning mode alone therefore does not reliably raise PCR in this sample. The locally
run model is the weakest on microscopy (0.667, 95% CI [0.563, 0.759]); six of the other seven mod-

                                                                7
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                        Kurban Intelligence Lab


Table 2 Main evaluation: Physical-Consistency Rate by constraint type and overall, 𝑛 = 30 items per (model,
constraint-type) cell per seed, 𝑆 = 3 seeds pooled per cell (bootstrap 95% CIs omitted from this compact view;
see Supplementary Table S1 for the full per-cell confidence intervals, and the Methods for why 𝜌𝑡 = 1 − PCR
here). DFT column combines the stability, metallicity, and magnitude constraint types. The first four rows
are the originally evaluated models; the next four are the later-generation refresh (Methods, Baselines
subsection). ‡ GPT-5.6-Sol is OpenAI’s flagship tier, added to test whether it exceeds the balanced-tier GPT-
5.6-Terra above within the same generation; its All-column bootstrap 95% CI, [0.731, 0.806], overlaps Terra’s
[0.736, 0.810], so flagship does not separate from balanced despite leading on diffraction alone (Discussion).

                                             Physical-Consistency Rate (higher is more consistent)

                     Model                   Diffraction   Microscopy    Spectra   DFT∗      All∗

                     Qwen2.5-VL-7B (open)      0.500           0.667      0.148    0.685    0.565
                     Gemini 2.5 Flash Lite     0.517           1.000      0.278    0.641    0.622
                     GPT-4o                    0.625           0.954      0.068    0.717    0.687
                     Claude Sonnet 4.5         0.547           0.977      0.189    0.736    0.656

                     Claude Opus 4.6           0.578           0.954      0.244    0.714    0.655
                     GPT-5.6-Terra             0.797           0.951      0.833    0.694    0.774
                     Qwen3-VL-8B-Instruct      0.468           0.802      0.133    0.642    0.555
                     Qwen3-VL-8B-Thinking      0.578           0.885      0.092    0.639    0.579

                     GPT-5.6-Sol‡              0.820           0.915      0.764    0.715    0.770



els exceed it with non-overlapping intervals (0.885–1.000), while Qwen3-VL-8B-Instruct at 0.802
([0.709, 0.884]) does not separate from it. We do not yet know whether the gap reflects genuine
scale-bar-reading skill or a difference in how each model handles the info-bar layout variety in
the source micrographs, and do not claim more than the measured difference. The high absolute
microscopy rates should also be read against the looseness of this oracle, which flags only feature
sizes exceeding the field of view (a necessary, not sufficient, condition), so a near-ceiling rate partly
reflects an easily satisfied check.

2.3 Accuracy versus consistency
On three constraint types with a genuine, non-circular accuracy criterion distinct from the oracle’s
own tolerance (diffraction: agreement with the single nearest true peak to 0.1◦ , versus the oracle’s
looser 0.5◦ tolerance; spectra: agreement with the nearest real measured peak to 2 cm−1 , versus the
oracle’s prominence-based check; stability: agreement with the Materials Project is_stable label,
evaluated separately from the oracle’s operational 0.05 eV atom−1 near-hull threshold), we report
accuracy alongside PCR and the four-cell breakdown on the same 920 items (𝑛 = 30 per (model,
constraint-type) cell, 𝑆 = 3 seeds; recomputed directly from experiments/exp3_results.jsonl,
which supersedes an earlier 918-item run). This figure is not directly comparable to Supplementary
Table S1’s 923 checkable records for the same four models’ diffraction, spectra and stability cells:
that table reports Experiment 2’s main PCR sweep, a separately drawn sample for a different
purpose, not this accuracy-versus- consistency analysis; the two are expected to differ and are not
a reconciliation target for each other. Microscopy is excluded: its prompt elicits only a feature-size
claim, so no non-circular accuracy ground truth is available without a different prompt design.
These numbers reflect the corrected spectrum oracle (Methods) and supersede an earlier pass in


                                                           8
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                          Kurban Intelligence Lab



which the gap was reported differently. Across all 12 (model, constraint-type) cells, accuracy and
PCR disagree on a mean of 22.2% of items, confirming that PCR is not answer accuracy under
another name (Fig. 5b,c). Diffraction is dominated by items that are wrong by the tight accuracy
criterion yet still oracle-consistent (up to 36 of 62 items in one diffraction cell, gap 58.1%): models
are frequently close enough to satisfy the oracle’s looser tolerance while measurably off the exact
peak. Spectra, under the corrected oracle, is now dominated by the opposite pattern from before
the correction: most disagreement is items wrong by both criteria (WI) rather than wrong-but-
consistent (WC), so the accuracy-consistency gap for spectra is small (4.2–11.2% across models)
rather than the large WC-dominated gap the pre-correction oracle produced; the earlier framing
of spectra as the largest-gap constraint no longer holds under the corrected oracle. Stability still
shows its own distinct pattern, dominated by items that are classified differently by the Materials
Project is_stable label and the operational near-hull threshold, a direct consequence of the two
definitions of stability disagreeing on a substantial share of real materials: on a random sample
of 3,000 real Materials Project entries, the oracle’s 𝜖 = 0.05 eV atom−1 tolerance and Materials
Project’s own strict is_stable label disagree on 571 (19.0%); its gap (18.0–27.8% across models) is
now comparable to, rather than smaller than, diffraction’s. One model (Qwen2.5-VL-7B) shows a
raw stability accuracy of 81/82 (0.988) on the unstable class but 0/8 on the small stable class, the
clearest case of the base-rate confound: because the sampled materials skew toward the unstable
class, near-ceiling raw accuracy reflects the base rate rather than discriminative skill. Balanced
accuracy (the mean of per-class accuracy, correcting for this skew) is 0.494 (Qwen2.5-VL-7B), 0.681
(Gemini 2.5 Flash Lite), 0.476 (GPT-4o), and 0.971 (Claude Sonnet 4.5). Three of four models fall to at
or near chance once the class imbalance is corrected for, and only Claude Sonnet 4.5’s apparent skill
survives this correction (𝑛 = 90 per model, 5–8 stable and 82–85 unstable materials per model’s
sample).

2.4 Effect of self-verification
We measure PCR before and after CGSV on identical items and test the change with the exact
paired McNemar test, reporting fixes, regressions, and residual violations (Table 3, Fig. 3b), on
diffraction and spectra, the two constraint types where the oracle’s feedback is an actionable
physical constraint the model can re-examine without the feedback message itself revealing the
answer (a scale-bar violation message would state the conversion factor outright, and the three DFT
claim types are single-shot binary judgments with no intermediate quantity to reconsider). 𝑛 = 30
items per (model, constraint-type) cell, 𝑆 = 3 seeds, 𝐾 = 2 maximum revision rounds, 545 checkable
records in total (superseding an earlier 555-record pass under the pre-correction spectrum oracle).
CGSV never regresses a previously consistent item: the regression count 𝑏 = 0 in every one of the 8
(model, constraint-type) cells and in the pooled per-model totals. CGSV significantly raises PCR for
all four models pooled across both constraint types (Qwen2.5-VL-7B 0.338 → 0.439, 𝑝 = 3.1 × 10−5 ;
Gemini 2.5 Flash Lite 0.521 → 0.632, 𝑝 = 2.4 × 10−4 ; GPT-4o 0.434 → 0.593, 𝑝 = 7.6 × 10−6 ; Claude
Sonnet 4.5 0.373 → 0.639, 𝑝 = 4.6×10−13 ); under the corrected spectrum oracle, absolute PCR is lower
throughout (tracking the main table’s spectrum collapse) but the relative gain and its significance
are, if anything, stronger for every model than under the earlier oracle. Residual violations remain
in every cell after 𝐾 = 2 rounds (roughly 40–90% of items under the stricter corrected spectrum
oracle), so CGSV measurably improves but does not eliminate violations, a positive control on the

                                                  9
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                         Kurban Intelligence Lab



oracles, not a guarantee of full correction. Because CGSV is scored by the same oracles that supply
its feedback, a rise in PCR is consistent both with the model correcting the flagged physics and
with it retracting or hedging the flagged claim; separating these requires the number of checkable
claims each chain exposes before and after CGSV. We checked this directly: this benchmark’s
single-claim-per-item design means every one of the 545 items exposed exactly one checkable
claim in every round it reached, before and after revision (𝑘𝑖 = 1 for all 𝑖, confirmed by comparing
each item’s number of recorded claim values against its number of revision rounds; zero items
exposed fewer claims after CGSV than before). Because 𝑘𝑖 never changes, a PCR gain here cannot be
explained by the model dropping a checkable claim; it must reflect the claim’s stated value changing
to one the oracle judges consistent. This rules out retraction in the sense of claim removal. It does
not rule out retreat: a model could move to a value that is trivially admissible rather than to the
physically right one, which the oracle, being a necessary-condition check, would accept either way.
Distinguishing those two would require the post-CGSV accuracy of the revised claim. We computed
it, applying the same non-circular accuracy criteria as the accuracy-versus-consistency analysis
(0.1◦ for diffraction, 2 cm−1 for spectra) to each item’s final-round claim: post-CGSV accuracy is
29.8% on diffraction (𝑛 = 252) and 9.9% on spectra (𝑛 = 293), both far below the corresponding post-
CGSV PCR (Table 3). Most of the CGSV gain is therefore retreat, not correction: the model moves
to a value the oracle’s necessary condition accepts far more often than it moves to the value that
is actually right. CGSV demonstrably reduces oracle-detected violations; this result shows it does
not, on the evidence here, demonstrably improve the underlying physical correctness of the claim.
We separately isolate whether this gain is attributable to the oracle signal specifically, or to extra
inference-time compute alone, with three controls matched to CGSV’s items, models, and decoding
(Baselines subsection): unaided self-refinement (the model is told to double-check its answer with
no oracle feedback) shows no significant change (before 0.349, after 0.339, 𝑛 = 542, 𝑏 = 34, 𝑐 = 29,
𝑝 = 0.615); generic equal-compute re-prompting (the model is simply asked to reconsider) likewise
shows no significant change (before 0.358, after 0.342, 𝑛 = 562, 𝑏 = 24, 𝑐 = 15, 𝑝 = 0.20); both
controls, unlike CGSV itself, show nonzero regressions (𝑏 > 0). Best-of-3 independent resampling
gives a random-pick PCR of 0.363 and an oracle-oracle upper bound (best of 3) of 0.419 (𝑛 = 614).
Both fall below CGSV’s oracle-guided after-PCR for every model, though the margin over the
weakest, Qwen2.5-VL-7B at 0.439, is only 0.02, and the resampling run draws its own item sample,
so we do not test the difference. Together these controls support attributing CGSV’s gain to the
physical-consistency signal specifically, not to generic self-reflection or additional sampling at
equal compute.

2.5 Verifier for violation prediction
We fine-tune Qwen2.5-0.5B-Instruct with LoRA on oracle-derived labels alone (no human anno-
tation) to predict, from the input description and chain text alone, whether a physical violation is
present, using 2,152 real oracle-checked records spanning all six constraint types collected across
the preceding evaluations (superseding an earlier 2,416-record pass under the pre-correction spec-
trum oracle). We report precision, recall, 𝐹1 , ROC AUC, and expected calibration error (ECE) on
an 80/20 in-distribution split and separately on six held-out-constraint-type splits (train on the
other five constraint types, test on one entirely unseen one). The in-distribution split is disjoint
at the parent source (item/structure) level, not the record level: an earlier pass split at the record

                                                 10
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                Kurban Intelligence Lab


Table 3 Effect of Constraint-Grounded Self-Verification, pooled across diffraction and spectra, 𝑛 =
30 items per (model, constraint-type) cell, 𝑆 = 3 seeds, 𝐾 = 2 rounds, under the corrected spec-
trum oracle (Methods). Δ: PCR gain (after minus before); 𝑏: regressions (before-consistent, after-
inconsistent); 𝑐: fixes (before-inconsistent, after-consistent); 𝑝: exact two-sided McNemar test on
(𝑏, 𝑐); 𝑝Holm : Holm-Bonferroni-adjusted 𝑝 over this table’s 6-test family (Methods, Statistics paragraph;
experiments/exp15_multiplicity_correction.py). All four CGSV effects survive this strictest correction;
both controls remain non-significant.

                                                       PCR              Discordant

                Model                        before    after        Δ   𝑏      𝑐          𝑝           𝑝Holm

                Qwen2.5-VL-7B                 0.338   0.439     0.101   0     16      3.1 × 10−5    1.2 × 10−4
                Gemini 2.5 Flash Lite         0.521   0.632     0.111   0     13      2.4 × 10−4    7.3 × 10−4
                GPT-4o                        0.434   0.593     0.159   0     18      7.6 × 10−6    3.8 × 10−5
                Claude Sonnet 4.5             0.373   0.639     0.266   0     42      4.6 × 10−13   2.7 × 10−12

                Mechanism-isolation controls (pooled across models, both constraint types)
                Self-refinement (no oracle) 0.349 0.339 −0.010 34             29         0.615        0.615
                Generic re-prompting          0.358 0.342 −0.016 24           15          0.20        0.399



level, which let seed replicates and same-chain claims of one item land on both sides of the split
and leaked item identity into the reported in-distribution number; we rebuilt the dataset to retain
a source identifier and re-split so that no source item appears on both sides. In distribution the
verifier is a useful detector (precision 0.77, recall 0.71, 𝐹1 = 0.74, AUC = 0.850, ECE = 0.096, close
to but slightly below the pre-fix leaky estimate of AUC = 0.858, as expected once the leak is closed).
Its cross-constraint-type generalization is poor for all six constraint types under the source-disjoint
split: diffraction, microscopy, and stability are indistinguishable from chance when held out entirely
(AUC 0.50, 0.53, and 0.44, bootstrap 95% confidence intervals straddling 0.5), spectra is not separable
from chance either (AUC 0.56, CI [0.488, 0.626]); and metallicity is the single arguable exception,
with a nominal 95% interval that excludes chance (AUC 0.58, CI [0.510, 0.652]) but that no longer
does so once the interval is widened for the six held-out comparisons (Bonferroni-corrected interval
[0.487, 0.673]). We therefore treat metallicity as a nominal, uncorrected exception rather than as
evidence of transfer, and do not build any claim on it. Magnetism, previously reported (under the
leaky, pre-correction split) as generalizing as well held-out as in distribution (AUC = 0.867), does
not survive the corrected, source-disjoint split: its held-out AUC is 0.503 (95% CI [0.430, 0.576]),
squarely at chance. We independently confirmed this under both the held-out-modality and held-
out-constraint-type variants of the split (the two coincide in this benchmark, since each oracle
family is its own constraint type), which reproduced the same chance-level result rather than the
earlier exception. We therefore retract the earlier magnetism-exception claim: it was very likely
an artifact of the record-level split allowing same-source records on both sides of train/test, not a
real transferable signal. The corrected finding is that no held-out constraint type shows transfer
that survives correction for the six comparisons. We report the verifier as a useful in-distribution
tool only, and explicitly do not claim it as a general-purpose, constraint-agnostic violation detector.
A pooled AUC across all six held-out constraint types is not reported: the six held-out runs are
separately fine-tuned models (not one model sliced six ways), so their raw probability outputs
are not on a directly comparable scale, and naively concatenating them before computing one


                                                               11
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                 Kurban Intelligence Lab


Table 4 Verifier precision/recall/𝐹1 (in-distribution and held-out-constraint-type splits, both source-
disjoint) and the detector’s bootstrap 95% CI on ROC AUC, predicting a real oracle violation from held-out
verifier scores. Expected calibration error is reported in the text for the in-distribution split (ECE = 0.096).
No pooled across-constraint-type AUC is reported (see text).

                                                     Violation prediction          Detector (ROC)

                        Split                    Precision     Recall     𝐹1     AUC        95% CI

                        In distribution (80/20 split, source-disjoint)
                        All constraint types        0.768       0.706    0.735   0.850   [0.813, 0.883]

                        Held out entirely (train on the other five constraint types)
                        Diffraction (XRD)          0.600       0.030 0.057 0.497         [0.419, 0.578]
                        Microscopy (SEM)           0.239       0.905 0.378 0.527         [0.468, 0.589]
                        Spectra (Raman)              –         0.000      –      0.558   [0.488, 0.626]
                        Stability∗                 0.355       0.103 0.159 0.436         [0.370, 0.502]
                        Metallicity∗               0.486       0.158 0.238 0.582         [0.510, 0.652]
                        Magnetism∗                 0.468       0.635 0.539 0.503         [0.430, 0.576]



AUC conflates genuine signal with arbitrary cross-model scale differences; we report only the six
individually well-defined per-constraint-type numbers (Table 4, Fig. 3c).




                                                               12
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                                                        Kurban Intelligence Lab




              a) Physical consistency by model and constraint type
                                                       geometric oracles                                DFT-grounded oracles

                                           Diffraction     Microscopy           Spectra       Stability      Metallicity     Magnetism             Overall
                                               (XRD)            (SEM)           (Raman)             ∗               ∗                ∗              (all six)


                      GPT-5.6-Terra†          0.797           0.951             0.833          0.656             0.659          0.767               0.774

                           GPT-5.6-Sol‡       0.820           0.915             0.764          0.742             0.670          0.733               0.770

                                GPT-4o        0.625           0.954             0.068          0.800             0.671          0.678               0.687

                 Claude Sonnet 4.5            0.547           0.977             0.189          0.756             0.694          0.756               0.656

                 Claude Opus 4.6†             0.578           0.954             0.244          0.722             0.721          0.700               0.655

              Gemini 2.5 Flash Lite           0.517           1.000             0.278          0.730             0.702          0.494               0.622

           Qwen3-VL-8B-Thinking†              0.578           0.885             0.092          0.767             0.644          0.506               0.579

                     Qwen2.5-VL-7B            0.500           0.667             0.148          0.744             0.540          0.767               0.565

            Qwen3-VL-8B-Instruct†             0.468           0.802             0.133          0.713             0.688          0.533               0.555


                              Physical-Consistency Rate                                                          † later-generation refresh ‡ flagship addition

                                                           0.00          0.25     0.50       0.75         1.00




              b) Oracle feedback raises PCR                                       c) Violation detection versus baselines
                                                                                   In distribution

                                                                                          MatPCR verifier                                                       0.850
                     0.7
                                                                                   Zero-shot LLM judge                                                          0.447
                                                    Claude Sonnet 4.5∗∗∗
                                                                                  Model self-confidence                                                         0.315
                                                    Gemini 2.5 FL∗∗∗
                                                                                   Held out (unseen constraint type)
                     0.6
                                                    GPT-4o∗∗∗
                                                                                              Metallicity∗                                                      0.582
                                                                                         Spectra (Raman)                                                        0.558
               PCR




                     0.5                                                              Microscopy (SEM)                                                          0.527
                                                                                             Magnetism∗                                                         0.503
                                                    Qwen2.5-VL-7B∗∗∗
                                                                                         Diffraction (XRD)                                                      0.497
                     0.4
                                                                                                Stability∗                                                      0.436
                                                    self-refinement
                                                    generic re-prompt
                                                    (both n.s.)
                     0.3
                            before          after
                 ∗∗∗ Holm-adjusted 𝑝 < 10−3 ; 𝑏 = 0 in every CGSV cell                                           0.3 0.4 0.5 0.6 0.7 0.8 0.9
                                                                                                                 Detector AUC with bootstrap 95% CI
                                                                                          CI above chance          nominal CI only        not above chance



Figure 3 Physical consistency, oracle-driven correction, and violation detection. a) Physical-
Consistency Rate (PCR) for nine models across the six label-free constraint types and overall, ordered
by overall PCR; shading is linear in PCR on the scale shown. Microscopy is the easiest constraint and Raman
spectra the hardest and most model-dependent, from 0.068 (GPT-4o) to 0.833 (GPT-5.6-Terra). Within the DFT-
grounded block the three types diverge for several models, which the pooled DFT column of Table 2 conceals.
Cell 𝑛 is 44–90 records; per-cell bootstrap intervals are in Supplementary Table S1. † Later-generation refresh
models; ‡ flagship-tier addition testing GPT-5.6-Sol against the balanced-tier GPT-5.6-Terra. b) Constraint-
Grounded Self-Verification before and after on identical items (Table 3). PCR rises for all four models with
no regression in any cell, whereas the two matched controls, unaided self-refinement and equal-compute re-
prompting (grey, dashed), do not change PCR and do produce regressions, attributing the gain to the oracle
signal rather than to additional inference-time compute. c) Detector AUC with bootstrap 95% confidence
intervals (Table 4) for the released verifier, its two comparator baselines and the six held-out constraint
types, on source-disjoint splits. In distribution the verifier separates violations; the LLM judge does not, and
self-confidence falls below chance, so neither baseline substitutes for it. Held out, five of six types are not
separable from chance, and metallicity’s interval excludes chance nominally but not after correcting for the
six comparisons.



                                                                                    13
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                            Kurban Intelligence Lab



3 Discussion
Across nine models spanning two capability generations and six label-free constraint types, current
models are far from uniformly consistent (overall PCR 0.555–0.774), ruling out the scenario in which
the benchmark would be uninformative because every model already satisfies the physics we check;
spectra and diffraction, in particular, remain hard and highly model-dependent under the corrected
oracles (Methods). Capability scaling within a provider family is not automatic: the later-released
GPT-5.6-Terra improves clearly over GPT-4o (0.774 vs. 0.687, non-overlapping bootstrap CIs), but
Claude Opus 4.6 does not improve over Claude Sonnet 4.5, and an explicit reasoning mode (Qwen3-
VL-8B-Thinking) does not improve over its non-reasoning sibling, in this sample. Nor does flagship
tier improve over balanced tier within the same generation: GPT-5.6-Sol (0.770, 95% CI [0.731, 0.806])
does not separate from GPT-5.6-Terra (0.774, [0.736, 0.810]) overall, despite leading every model
on diffraction specifically (0.820); price and marketed capability tier are not, on this evidence, a
reliable proxy for physical-consistency performance any more than release date is. Because the
refresh models are one to three provider releases behind the newest available on the collection date,
and GPT-5.6-Terra is a balanced rather than a flagship tier, these comparisons bound generational
improvement in this sample rather than characterizing the current frontier. The accuracy-versus-
consistency gap (a mean 22.2% disagreement across 12 cells; the superseded spectrum oracle gave
41.8%, a figure we record here for transparency about the correction and do not report elsewhere)
shows directly that PCR is not a restatement of answer accuracy: models are frequently consistent
while measurably wrong on diffraction, and, for stability specifically, frequently correct by one
strict definition while flagged inconsistent by a looser but defensible tolerance, a real ambiguity
in what "stable" should mean for a reasoning check, not an error in either definition; separately,
one model’s near-ceiling raw stability accuracy is a base-rate artifact of the sampled materials, not
discriminative skill, once balanced accuracy is computed. CGSV is a one-directional positive control:
it never regressed a previously consistent item across 545 records, and raised PCR significantly
for all four models tested, an effect two mechanism-isolation controls (unaided self-refinement,
generic equal-compute re-prompting) do not reproduce, supporting attribution of the gain to the
oracle signal rather than to extra inference-time compute alone. The released verifier is a useful
in-distribution detector (AUC = 0.850, on a split we rebuilt to be source-disjoint after finding
the original random split leaked item identity across train and test), but its cross-constraint-type
generalization is the paper’s clearest negative result: five of the six held-out constraint types
are indistinguishable from chance, and the sixth (metallicity) separates from chance only before
correcting for the six comparisons. This corrects an earlier, substantively different finding: under
the leaky split, magnetism appeared to generalize as well held-out as in distribution (AUC = 0.867);
under the corrected, source-disjoint split, magnetism’s held-out AUC is 0.503, and we now attribute
the earlier result to the split leak rather than to a real transferable signal. We report this correction,
and the resulting conclusion that no held-out constraint type shows transfer surviving correction
for the six comparisons, rather than continue to report the retracted exception, consistent with
our stated position that a verifier trained on one constraint type’s surface patterns should not
be assumed to transfer to another without direct evidence. Comparator baselines sharpen this
picture. In distribution neither is competitive: a zero-shot LLM-as-judge reaches AUC 0.447 and
the model’s own token-level self-confidence 0.315, the latter significantly below chance, against the


                                                   14
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                          Kurban Intelligence Lab



fine-tuned verifier’s 0.850. Held out, all three are weak, but not uniformly: the LLM-judge reaches
AUC 0.735 (95% CI [0.682, 0.790]) on microscopy, above anything the fine-tuned verifier achieves
on any held-out constraint type, which suggests the fine-tuned verifier’s advantage is specific to
the distribution it was trained on rather than a general superiority over prompting. The fine-tuned
verifier’s in-distribution advantage is real, but it is not a general substitute for the oracle out of
distribution. The central limitation is intrinsic to the approach, not particular to these results: the
oracles bound a class of physically checkable errors, so PCR is a necessary-not-sufficient reliability
signal, and the released verifier predicts the oracle signal rather than replacing first-principles
ground truth. As a clearly scoped extension, the verifier could pre-filter candidate structures before
DFT in a small screening study; a first best-of-3 resampling check finds real but modest headroom
over a random pick (PCR 0.363 random-pick vs. 0.419 oracle-oracle ceiling), though we did not build
the verifier-as-selector comparison this ceiling would need to be practically useful, and report it
only as a bounded, partial result. A further implication, which we make possible but do not claim to
demonstrate here, is that a label-free, physics-grounded consistency signal can serve as a verifiable
reward for training materials-reasoning models, extending reinforcement learning from verifiable
rewards to a domain where verification has been under-specified.[37] We also ran a domain-specific
structure-aware model (MatterChat) on the DFT arms as a materials-domain evaluee (Baselines
subsection): it reaches PCR 0.783/0.795/0.850 on stability/metallicity/ magnetism on a shuffled
sample of 120 real materials. These rates sit at or above the general-purpose models’ rates on
the same three constraint types, but the sample is drawn separately from the main evaluation,
so the comparison is indicative rather than paired, and it rests on one domain model. Finally,
every DFT-grounded number in this paper (the DFT column of Table 2, the stability arm of the
accuracy-versus-consistency analysis, and the metallicity and magnetism arms of the verifier and
detector analyses) rests on Materials Project reference values and oracle tolerances.

4 Methods
4.1 Data sources
MatPCR draws only on public data for reproducibility and license clarity: experimental powder
diffraction patterns with known structures;[49] public scanning electron microscopy (SEM) images
that include scale bars;[50] open Raman spectra;[51] and public first-principles data (computed
energies, convex hulls, band gaps) from established databases.[52] No number reported in this
paper rests on a first-principles calculation run by the authors: every DFT-grounded reference
value used is Materials Project’s own standardized computational result, retrieved via the mp-api
client (Methods, DFT-grounded oracles); an authors’-own-DFT fallback for missing or questionable
Materials Project entries was implemented but never invoked over the reported sample. We also
surveyed the simulated diffraction dataset SimXRD-4M[53] as a candidate diffraction source, but
its schema (units of the tabulated lattice-distance field; the meaning of its integer label) could not
be resolved against its documentation with confidence, so it was not used in any reported result;
all diffraction numbers in this paper are from real experimental patterns only.




                                                 15
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                            Kurban Intelligence Lab



4.2 Tasks, modalities, and exposed constraints
Each item pairs an input with a question whose faithful answer requires at least one physically
checkable quantity (Fig. 5a). Inputs span image items (VLM), such as micrographs and diffraction
images, and structure or text items (LLM), such as a crystal structure with a property question.
We parse the reasoning chain for stated quantities (peak positions, scale, feature sizes, stability
claims, property values) and test each against the matching oracle. An item is checkable if its chain
exposes at least one such quantity.

4.3 Programmatic geometric oracles
For diffraction we apply Bragg’s law, 𝜆 = 2𝑑 sin 𝜃, converting any claimed 2𝜃 to a 𝑑-spacing, testing
claimed peaks against the reference pattern of the stated structure within tolerance, and rejecting
claims outside the realizable 2𝜃 window. For microscopy we recover nanometres per pixel from
the detected scale bar and reject any feature larger than the field of view. For spectra we accept
a claimed peak only if a genuine interior local maximum (higher than both adjacent flanks down
to their nearest valleys, rejecting a monotonic rise or a shoulder on a nearby peak) exists near
it with prominence exceeding a fraction of the signal’s dynamic range; this is a revision, made
mid-project after a first precision audit showed a windowed-maximum check without the interior-
local-maximum requirement was too permissive on noisy, baseline-drifting Raman spectra, so it
does not appear in numbers computed before the revision (flagged where relevant throughout).

4.4 DFT-grounded property oracles
First-principles access extends the oracle from geometry to computed physics, still without human
labels. A stability claim is checked against the energy above the convex hull computed for the stated
composition; a metallicity claim against the computed band gap; and a magnetism claim against
the computed total magnetization, normalized per atom. Reference values are Materials Project’s
own standardized computational references (database version 2026.04.13, retrieved 2026-07-16 via
the mp-api client; GGA/GGA+U relaxation under Materials Project’s published standard workflow),
described throughout as standardized computational references, not experimental ground truth.
Because DFT-computed references depend on the exchange-correlation functional (semilocal func-
tionals underestimate band gaps), each oracle is designed around that known error rather than
treating the reference as exact. Stability (operational near-hull criterion): for this benchmark, a
model’s stable/unstable claim is judged consistent according to whether the computed energy above
the convex hull satisfies 𝐸hull ≤ 𝜖, with 𝜖 = 0.05 eV atom−1 . We additionally report sensitivity at
𝜖 ∈ {0, 0.025, 0.05, 0.10} eV atom−1 ; all four thresholds gave 0% false-negative and false-positive rates
in the positive-control audit. The adopted threshold is an operational screening criterion rather
than a definition of strict thermodynamic stability: structures with 𝐸hull = 0 lie on the computed
convex hull, whereas structures with 0 < 𝐸hull ≤ 0.05 eV atom−1 are described as near-hull or poten-
tially metastable. On a random sample of 3,000 Materials Project entries, this operational threshold
and the Materials Project is_stable label disagreed for 571 structures (19.0%); in every such case,
Materials Project labelled the structure unstable whereas the operational threshold admitted it as
near-hull (the reverse did not occur in this sample). Figure 4a shows three model claims evaluated
against this operational near-hull criterion. Computed band-gap classification: a Materials Project
band gap ≤ 0.05 eV is assigned to the computed zero/near-zero-gap class, whereas a gap ≥ 0.20 eV

                                                   16
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                          Kurban Intelligence Lab



is assigned to the computed nonzero-gap class. The intervening range (0.05–0.20 eV) is treated
as an explicit abstention band and excluded from PCR rather than forced into either class. These
thresholds were fixed before the reported evaluation runs. Figure 4b shows three examples of model
classifications that are inconsistent with the corresponding Materials Project-computed band-gap
references. Magnetism (net-magnetization check): because a global reversal of all collinear spins
changes the sign of the total magnetization without changing the physical state, the oracle uses the
absolute total magnetization normalized per atom. The Materials Project reference is classified as
finite or near-zero net magnetization using a threshold of 0.05 𝜇B atom−1 , fixed before the reported
runs. Only within the finite-net-magnetization class is a claimed magnitude checked against the
reference within one order of magnitude (Fig. 4c). This oracle concerns net magnetization only;
a near-zero net value does not exclude antiferromagnetic or compensated ferrimagnetic ordering.
An earlier version used an exact-zero comparison and was then patched with a 10−6 𝜇B absolute
tolerance for numerical noise; both formulations are superseded by the per-atom classification
threshold above and no longer appear in the released code. Positive-control testing showed all
three thresholds and the stability sensitivity grid give 0% false-negative and false-positive rates on
real Materials Project structures; the metallicity abstention band correctly excluded 125 of 3,000
sampled materials in that test. These checks make plausible-but-wrong physics detectable. No step
requires a human annotation of the correct answer, which is what lets MatPCR scale and distin-
guishes it from answer-accuracy benchmarks and from proposal- or execution-level verification.

4.5 The Physical-Consistency Rate
Let items be indexed 𝑖 = 1, … , 𝑁 , let 𝑘𝑖 be the number of physically checkable constraints the chain
exposes on item 𝑖, and 𝑣𝑖 ≤ 𝑘𝑖 the number the oracles find violated. The item is consistent iff 𝑣𝑖 = 0.
Over the checkable subset  = {𝑖 ∶ 𝑘𝑖 > 0},
                                                1
                                      PCR =        ∑ 𝟏[𝑣𝑖 = 0].                                     (1)
                                               || 𝑖∈

We report per-constraint-type violation rates 𝜌𝑡 = ( ∑𝑖 𝑣𝑖,𝑡 )/( ∑𝑖 𝑘𝑖,𝑡 ) and per-modality rates with
percentile bootstrap confidence intervals. The definition admits several checkable claims per item,
but every item in this benchmark exposes exactly one claim of its own constraint type, so 𝑘𝑖 = 1
throughout and 𝜌𝑡 reduces to 1 − PCR within a constraint type; we keep the general form because
the metric is intended for chains that expose more. PCR is distinct from answer accuracy: a model
can be accurate yet inconsistent, or consistent yet wrong, and the gap is itself reported.

4.6 Constraint-Grounded Self-Verification
CGSV uses the same oracles as a corrective signal at inference time with no labels. Because a
model’s own self-verification is largely confirmatory rather than corrective,[54] CGSV supplies the
correction signal externally, from the oracle, rather than asking the model to re-examine its answer
unaided. The model extracts the governing constraints, answers, is shown any programmatic or
DFT-grounded violation, and revises, up to 𝐾 rounds or until no violation remains (Algorithm 1).
CGSV is a positive control: if the oracles capture real errors, exposing them should raise PCR,
measured by a paired test, not assumed. Writing 𝑐 for the items the oracle flags before but not
after revision and 𝑏 for those flagged after but not before, the change in the rate is exactly ΔPCR =

                                                 17
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                              Kurban Intelligence Lab




            (a) Stability oracle

                         SrMoO3                                ThPbAu2                               EuZrFeBiO6
                 real Materials Project entry            real Materials Project entry            real Materials Project entry
             model claimed    MP-computed reference   model claimed   MP-computed reference   model claimed   MP-computed reference

                                     STABLE                                   STABLE                                UNSTABLE
              UNSTABLE        ×      𝐸hull =0.0000
                                                        UNSTABLE      ×      𝐸hull =0.0000
                                                                                                STABLE        ×      𝐸hull =1.2843




                MP hull energy is exactly 0:            Same error on an unrelated               Opposite error, far larger:
             structure on the computed hull             composition: hull energy 0,               hull energy is 25× the
                     judged unstable.                   still defaulted to UNSTABLE.             tolerance, unambiguous.


            (b) Computed band-gap oracle

                     KCaTbNbO6                                 Ca(H8 O5 )2                           KMgMn16 O32
                 real Materials Project entry            real Materials Project entry            real Materials Project entry
             model claimed    MP-computed reference   model claimed   MP-computed reference   model claimed   MP-computed reference

                                    METALLIC                              NONMETALLIC                               METALLIC
             NONMETALLIC      ×     𝐸𝑔 =0.0000 eV
                                                        METALLIC      ×      𝐸𝑔 =4.4694 eV
                                                                                              NONMETALLIC     ×     𝐸𝑔 =0.0000 eV




                 Materials Project reports                  Opposite error: the                  Computed gap is exactly
                  a zero computed gap;                      MP-computed gap                    zero again; reasoning pointed
              reasoned from structure alone.                     is 4.47 eV,                        the wrong direction.
                                                       over 20× the abstention edge.


            (c) Net-magnetization oracle

                             C                                     Eu2 Sb3                              Na2 FeO3
                 real Materials Project entry            real Materials Project entry            real Materials Project entry
             model claimed    MP-computed reference   model claimed   MP-computed reference   model claimed   MP-computed reference

              MAGNETIC            NONMAGNETIC                                MAGNETIC                               MAGNETIC
               2.2 µB/atom
                              ×   0.0000 µB/atom
                                                      NONMAGNETIC     ×     2.76 µB/atom
                                                                                              NONMAGNETIC     ×    0.667 µB/atom




               Real moment is exactly zero;              Real moment is large and                Real moment is well above
                reasoning admits it never              unambiguous; reasoned Eu/Sb            threshold; own reasoning called
                  identified the formula.             moments cancel, but they do not.               this “close to zero.”


Figure 4 Representative Materials Project-grounded oracle violations. a, Stability-oracle cases com-
paring model STABLE/UNSTABLE claims with Materials Project energies above the convex hull, 𝐸hull . The
first two structures lie on the Materials Project computed convex hull, whereas EuZrFeBiO6 lies far above
the 0.05 eV atom−1 operational near-hull threshold. b, Computed band-gap cases comparing model METAL-
LIC/NONMETALLIC claims with the operational zero/near-zero-gap and nonzero-gap classes derived from
Materials Project band gaps, 𝐸𝑔 . These are computational reference classifications, not experimental trans-
port assignments. c, Net-magnetization cases comparing model MAGNETIC/NONMAGNETIC claims with
the operational near-zero and finite classes derived from Materials Project total magnetization per atom.
This panel evaluates net magnetization only and does not determine the complete magnetic ordering. All
examples are real, human-confirmed oracle activations from the DFT-grounded Half-B evaluation; values
are reported exactly as recorded.




                                                                      18
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                            Kurban Intelligence Lab



Algorithm 1 Constraint-Grounded Self-Verification
  1 Input: input 𝑥, question 𝑞, oracle set , max rounds 𝐾
  2 𝐺 ← ExtractConstraints(𝑥)
  3 𝑎 ← Answer(𝑥, 𝑞, 𝐺)
  4 for 𝑟 = 1 … 𝐾 do
  5    𝑉 ← {𝑜 ∈  ∶ 𝑜(Claims(𝑎), 𝐺) fails}
  6    if 𝑉 = ∅ then
  7        break
  8    end if
  9    𝑎 ← Revise(𝑥, 𝑞, 𝐺, 𝑎, 𝑉 )
 10 end for
 11 return 𝑎, residual violations 𝑉



(𝑐 −𝑏)/𝑛, so the discordant pair (𝑏, 𝑐) carries all of the effect and the exact McNemar test on it is the
natural paired test (Supplementary Note 1.6). The loop halts after at most 𝐾 rounds by construction.
We do not assume revisions can only remove violations; 𝑏 is measured.

4.7 Released physical-consistency verifier
Because the oracles require reference data (a structure, a scale bar, a computed value), we fine-
tune an open model to predict, from the input and chain alone, whether a physical violation is
present. Training labels come from the oracles, so the verifier is trained without human annotation.
Unlike process-reward and generative reward models trained on human preference or model-
judged correctness,[33, 34] its labels are a deterministic physics signal, which reduces the spurious
correlations that affect preference-trained reward models; where a reference exists, the oracle is
hard to game by surface-form changes. We release it as the reusable artifact of this work and report
precision, recall, 𝐹1 , ROC AUC, and calibration against held-out oracle judgments.

4.8 What oracle error does to the reported rate
An oracle that misses genuine violations or fires on clean chains moves the measured PCR away
from the rate we want to report. The result below makes that displacement exact, and is the formal
reason the oracle-validity gate is run before any model. Let  be the set of checkable items with
|| = 𝑛, where here 𝑛 denotes the number of checkable items in the set under analysis (distinct
from the per-cell item count of the evaluation tables). For 𝑖 ∈  let 𝑌𝑖 ∈ {0, 1} be the latent indicator
that the chain contains at least one genuine physical violation and 𝑌̂𝑖 ∈ {0, 1} the oracle’s decision.
The true inconsistency rate is 𝜏 = 𝑛1 ∑𝑖 𝑌𝑖 , the true rate is PCR⋆ = 1 − 𝜏, and the measured rate
is PCR = 1 − 𝑛1 ∑𝑖 𝑌̂𝑖 . Define the empirical item-level recall and false-alarm rate of the oracle,
𝑑̂ = #{𝑌̂𝑖 =1, 𝑌𝑖 =1}/#{𝑌𝑖 =1} and 𝑓̂ = #{𝑌̂𝑖 =1, 𝑌𝑖 =0}/#{𝑌𝑖 =0} (a rate multiplies a zero count to zero
when its class is empty).

                                                     ̂ − (1 − 𝜏)𝑓̂.
Proposition 1 Bias decomposition. PCR − PCR⋆ = 𝜏(1 − 𝑑)

Proof. Counting flagged items, ∑𝑖 𝑌̂𝑖 = 𝑑̂ #{𝑌𝑖 =1} + 𝑓̂ #{𝑌𝑖 =0} = 𝑛[𝜏 𝑑̂ + (1 − 𝜏)𝑓̂], so PCR =
1 − 𝜏 𝑑̂ − (1 − 𝜏)𝑓̂. Subtracting PCR⋆ = 1 − 𝜏 gives the result.

                                                  19
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                                                                                              Kurban Intelligence Lab




                                a) From public data to a released verifier, with no human annotation
                                                                                                                          Oracle-validity gate, run before any model
                                                                                                                        planted violations recovered at 10%, 30%, 50%
                                                                                                                         (FN rate 0.0000); precision audited by hand


                                                                                                                                                   validates


                                              Public data                      Items and oracles                                         Parse claims,                  PCR and 𝜌𝑡
                                                                                                             Sample chains
                                             opXRD, RRUFF,                       Bragg, scale bar,                                       apply oracles               bootstrap 95% CI
                                                                                                               9 models
                                             NFFA-EUROPE,                        peak, hull, gap,                                         consistent                 (Prop. 1 bounds
                                                                                                              𝑆 = 3 seeds
                                             Materials Project                    magnetization                                           or violation                the oracle bias)

                                                                                                                                                       oracle judgments
                                                                                                           label-free
                                                                                                           feedback
                                                                                                                                                                                         open
                                                                                                            CGSV: return the                                             Fine-tune on
                                                                                                         violation, revise (𝐾 = 2)                                       oracle labels
                                                                                                          4 models, diffraction                                           → released
                                                                                                               and spectra                                                  verifier


                                           No step requires a human annotation of the correct answer; every training and scoring label above is derived from physics.




                                b) What PCR adds to accuracy                                                             c) Where the two axes disagree
                                                                                                                                             mean 22.2%
                                                                                                                                                            (12 cells)

                                                             ✔ consistent               × inconsistent                                                               58.1% largest cell
      resolved by accuracy, needs labels




                                                                                                                            Diffraction (XRD)
                                                             right for the             right despite a
                                             correct




                                                            right reasons             physics violation
                                                                                                                                     Stability∗                          18.0–27.8%
                                                                                      dominates stability
                                                               the target
                                                                                       (gap 18.0–27.8%)                                           4.2–11.2%
                                                                                                                            Spectra (Raman)
                                                             wrong but                   wrong and
                                             incorrect




                                                             consistent                 inconsistent
                                                                                                                                                  0%           20%         40%           60%
                                                         dominates diffraction
                                                                                       dominates spectra                                    items on which accuracy and PCR disagree
                                                         (up to 58.1% of a cell)
                                                                                                                          Microscopy is excluded: its prompt elicits only a feature-size claim,
                                                                                                                          so no non-circular accuracy criterion is available.
                                                                 resolved by PCR, without labels


Figure 5 The MatPCR framework and what its metric adds to accuracy. a) Items and oracles are built
from public characterization data and Materials Project references; the oracles are validated before any model
is run, by a positive control that plants violations at three known rates and a human audit of oracle-fired
cases; reasoning chains are then parsed into claims, checked, and summarized as the Physical-Consistency
Rate with bootstrap intervals, whose displacement from the true rate Proposition 1 makes exact. The same
oracle judgments drive Constraint-Grounded Self-Verification, which returns each violation to the model
for revision, and supply the training labels for the released verifier. No step uses a human annotation of the
correct answer. b) A reasoning chain occupies one of four states. Accuracy resolves the rows and needs labels;
PCR resolves the columns and does not. The three constraint types with a non-circular accuracy criterion
each populate a different off-diagonal cell: models are frequently close enough to satisfy the diffraction
oracle while measurably off the exact peak, correct by Materials Project’s own stability label yet outside
the oracle’s looser tolerance, and wrong on both counts for spectra. c) The resulting disagreement, as the
percentage of items on which the two axes differ, across the four originally evaluated models. The mean is
22.2% over the twelve (model, constraint-type) cells, so PCR is not answer accuracy under another name;
the spread across constraint types shows that the two axes come apart for different reasons in each.




                                                                                                                 20
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                 Kurban Intelligence Lab



Corollary 2 One-sided guarantees and bias bound. If the oracle is complete (𝑑̂ = 1) then
PCR ≤ PCR⋆ , so PCR never overstates consistency; if it is sound (𝑓̂ = 0) then PCR ≥ PCR⋆ ; if both,
                                             ̂ + 𝑓̂.
PCR = PCR⋆ . In general |PCR − PCR⋆ | ≤ (1 − 𝑑)
                                                                                              ̂ −
Proof. The three cases substitute 𝑑̂ = 1 and 𝑓̂ = 0 into Proposition 1. For the bound, |𝜏(1 − 𝑑)
(1 − 𝜏)𝑓̂| ≤ 𝜏(1 − 𝑑)
                   ̂ + (1 − 𝜏)𝑓̂ ≤ (1 − 𝑑)
                                        ̂ + 𝑓̂ because 𝜏, 1 − 𝜏 ≤ 1.

Corollary 2 is the formal reason to run the positive control and precision audit first (Table 1). The
positive control estimates the oracle’s recall 𝑑̂ (planted-violation recovery). The precision audit
estimates its precision 𝜋 on fired cases, equivalently the false-discovery rate 1 − 𝜋; this is not
the false-alarm rate 𝑓̂, whose denominator is the truly-clean items, and the two coincide only
through the base rate. Under the 𝑑̂ = 1 idealization supported by the positive control, Corollary 2
gives PCR ≤ PCR⋆ , and the understatement is exactly the false-positive fraction (1 − 𝜋)(1 − PCR),
which the audited precision estimates directly; estimating 𝑓̂ itself, and hence the bias when 𝑑̂ < 1,
additionally requires sampling oracle-silent items to fix the base rate.
     Proposition 1 and Corollary 2 concern the oracle’s bias on a fixed set of items and are exact: they
involve no distributional assumption. The reported PCR is also a finite sample, so its total error as
an estimate of the rate the benchmark’s item-generating process would produce carries a second,
statistical part. We report that part empirically, as the percentile bootstrap interval on every rate,
resampling at the source level where items share a parent source (Supplementary Note 1.4). A
distribution-free alternative, obtained by adding a Hoeffding term to the bias bound above under
independent sampling, is stated in Supplementary Note 1.7; at the cell sizes used here it is looser
than the bootstrap interval, so we use it only to make the decomposition explicit and not as the
reported uncertainty.
Write 𝑌̂𝑖𝑣 ∈ {0, 1} for the learned verifier’s decision on item 𝑖, in place of the oracle’s 𝑌̂𝑖 , and
PCR𝑣 = 1 − 𝑛1 ∑𝑖 𝑌̂𝑖𝑣 for the rate it reports. Substituting the verifier for the oracle when reference
data are unavailable at inference costs at most the two decisions’ measurable disagreement rate
𝛿 = 𝑛1 #{𝑖 ∶ 𝑌̂𝑖𝑣 ≠ 𝑌̂𝑖 }: both rates are means of indicators over the same items, so |PCR𝑣 − PCR| =
                                                                                  ̂ + 𝑓̂ + 𝛿 by Corollary 2. The
| 𝑛1 ∑𝑖 (𝑌̂𝑖 − 𝑌̂𝑖𝑣 )| ≤ 𝑛1 ∑𝑖 |𝑌̂𝑖 − 𝑌̂𝑖𝑣 | = 𝛿, and hence |PCR𝑣 − PCR⋆ | ≤ (1 − 𝑑)
verifier’s precision and recall in Table 4 summarize that disagreement. Because that disagreement
is small only in distribution and large where transfer fails, the bound is tight in distribution and
loose out of it, which is exactly where reference data are absent; we therefore present it as a
guarantee for in-distribution use, not a license to replace the oracle across constraint types. Standard
background results (Bragg’s law, scale-bar calibration, convex-hull stability, the percentile bootstrap,
a concentration inequality for the empirical rate, and the exact McNemar test) are collected in
Supplementary Note 1.

4.9 Models and experimental protocol
We evaluate nine models in total across three passes. The original pass (data collected 2026-07-04
through 2026-07-11, re-run on corrected oracles 2026-07-16/17) covers one open vision–language
model, Qwen2.5-VL-7B-Instruct[55] (Hugging Face repository Qwen/Qwen2.5-VL-7B-Instruct,
run locally in bfloat16 on an NVIDIA A100 80GB via transformers), and three frontier models
accessed through the OpenRouter API: openai/gpt-4o, google/gemini-2.5-flash-lite, and
anthropic/claude-sonnet-4.5. A later-generation refresh pass (data collected 2026-07-19/20)

                                                      21
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                         Kurban Intelligence Lab



adds anthropic/claude-opus-4.6, openai/gpt-5.6-terra, qwen/qwen3-vl-8b-instruct, and a
reasoning-mode condition, qwen/qwen3-vl-8b-thinking, all four again via OpenRouter. This
refresh is one to three provider releases behind the newest models available on the collection date:
within the same families, Claude Opus 4.7, 4.8 and 5, and the flagship GPT-5.6-Sol tier, had all been
released by 2026-07-20, and GPT-5.6-Terra is the balanced rather than the flagship tier of its series.
A third pass (data collected 2026-08-06) adds openai/gpt-5.6-sol, the flagship sibling of GPT-5.6-
Terra, at the same 𝑛 = 30, 𝑆 = 3 scale, to test directly whether flagship tier exceeds balanced tier
within the same generation; it does not (Discussion). We therefore describe the second pass as a
later-generation, not a frontier, comparison, and the third as answering the flagship-tier question
the second pass’s absence of a flagship model had left open. Model strings, weights, and API
routing are pinned in the released repository; OpenRouter does not expose a per-request snapshot
date distinct from the model string for these providers, so the listed model identifiers and the
stated collection dates are the reproducibility anchor. We additionally evaluate a materials-domain
structure-aware model, MatterChat[11] (its released Mistral-7B-based checkpoint and CHGNet
structure encoder, run locally), on the DFT arms only (Baselines subsection). No LLaVA-class
model was run.
   For each model and item we sample reasoning chains at a fixed decoding configuration with
𝑆 = 3 seeds, apply the oracles, and report mean PCR with percentile bootstrap confidence intervals
(𝐵 = 10,000 resamples); CGSV uses the same decoding and 𝐾 = 2 rounds. The local model uses
greedy decoding (do_sample=False); the API models are called with no explicit temperature or top-
𝑝 override, i.e. each provider’s own default sampling settings for the given model string, which we
did not tune. We ran the most informative experiment first, the oracle-validity gate reported above
(Table 1): a positive control that injected synthetic violations into otherwise valid chains at known
rates and confirmed the oracles recover them, followed by a manual audit of oracle-fired cases that
quantified oracle precision on real chains. This established that PCR measures genuine physical
violations rather than parsing artifacts. Tolerances, prompts, and the DFT protocol were fixed
before the reported evaluation runs and are released with the code; we do not describe them as pre-
registered, because two oracles were revised mid-project after the precision audit (the spectrum and
magnetism checks, above) and every affected number was re-collected under the revised definition
rather than carried over. No time-stamped registration of the tolerances and prompts was made
(checked directly against this project’s version history), so we report the wording above rather than
an unverifiable pre-registration claim. We report 𝑆 = 3 seeds per condition, bootstrap confidence
intervals on all rates, and the exact McNemar test for paired before/after comparisons. Each seed
draws a fresh, independently sampled subset of items (verified directly: zero duplicate source files
across seeds in every (constraint-type, model) cell checked), so the 𝑆 = 3 seeds are not the same
items re-scored, and pooling records across seeds within a cell does not pool literal duplicates.
The separate concern that the six McNemar tests in Table 3 (four per-model CGSV comparisons
plus two mechanism-isolation controls) needed a multiple-comparisons correction is now resolved:
we applied Holm and Benjamini–Hochberg correction directly (Baselines subsection, Statistics
paragraph) and every CGSV effect survives.




                                                 22
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                          Kurban Intelligence Lab



4.10 Baselines, ablations, and controls
Three of the study’s controls are not consistently reported in comparable verifier and reasoning-
benchmark studies: the oracle positive control with a precision audit, bootstrap confidence intervals
with an exact paired test, and a held-out-constraint generalization split, to the best of our knowledge
as of this writing. A physical-consistency metric, a released verifier, and a self-correction loop are
nonetheless interpretable only against the further baselines and controls specified here.
Models. We added the later-generation refresh and reasoning-mode condition described above
(Claude Opus 4.6, GPT-5.6-Terra, Qwen3-VL-8B-Instruct, Qwen3-VL-8B-Thinking), and a materials-
domain evaluee. For the domain evaluee we ran MatterChat[11], a structure-aware model that
aligns a pretrained CHGNet material encoder with a Mistral-7B language model, on the three DFT
constraint types (its native input, a crystal structure) using its released checkpoint and code, on a
shuffled sample of 120 real Materials Project structures (an unshuffled first sample, drawn in raw
file order, was 3.3% magnetic versus the corrected sample’s 65%, so we discarded it and redrew with
shuffling before reporting). MatterChat reaches PCR 0.783 (stability), 0.795 (metallicity, 𝑛 = 112
checkable of 120), and 0.850 (magnetism, genuinely varying its answer across materials rather than
defaulting to one class, confirmed directly). We did not run a domain-specific model on the image
arms. Microscopy-specific vision–language models for materials do exist; we checked whether the
one cited here, MicroscopyGPT,[5] could serve as a domain evaluee on the scale-bar arm and found
its task and interface are incompatible with the question this arm poses, not merely unevaluated.
MicroscopyGPT is trained to caption simulated scanning transmission electron microscopy images
of 2D materials with a full atomic structure (lattice parameters, element identities, and atomic
coordinates), and its released interface has no scale-bar-reading or feature-size-estimation output
at all; forcing it to answer a size question it was never built to produce would not evaluate the
model, it would evaluate an ad hoc adapter we would have to invent around it. We therefore leave
the image arms without a domain-specific evaluee and report this as an honest coverage gap. On
reasoning mode: Qwen3-VL-8B-Thinking does not improve over Qwen3-VL-8B-Instruct overall
(0.579 vs. 0.555, bootstrap CIs overlapping), so explicit reasoning mode alone does not reliably raise
PCR in this sample (Results).
Verifier baselines. We compare the released verifier against a zero-shot LLM-as-judge (Gemini
2.5 Flash Lite, prompted to judge each chain for a physical-consistency violation with a stated
confidence) and the evaluated local model’s own token-level self-confidence (mean log-probability
of its stated final answer span), on the same in-distribution and six held-out-constraint-type splits,
2,152 items. Neither baseline is competitive with the fine-tuned verifier in distribution: the LLM-
judge reaches AUC = 0.447 (95% CI [0.400, 0.493], indistinguishable from or below chance) and
self-confidence AUC = 0.315 (95% CI [0.264, 0.365], significantly below chance, an anti-correlation
we discuss below), against the fine-tuned verifier’s in-distribution AUC = 0.850. Held out, all
three approaches are weak: the LLM-judge ranges AUC 0.489–0.735 across the six constraint types
(best on microscopy, worst on diffraction) and self-confidence ranges AUC 0.246–0.523, several
below chance; neither baseline recovers the fine-tuned verifier’s in-distribution advantage out of
distribution, and none of the three approaches is a reliable held-out detector. We investigated
the below-chance self-confidence result directly rather than treat it as noise: on a 40-item sample,
chains later judged physically inconsistent had a higher mean token log-probability (−2.84) than
chains judged consistent (−3.99), i.e. the evaluated model is more confident, not less, when it is

                                                 23
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                              Kurban Intelligence Lab



physically wrong, which is the source of the below-chance AUC rather than a sign error in our
scoring. We separately built reliability diagrams (binned calibration curves) and a recommended
per-split operating threshold for the released verifier: in distribution its predicted probabilities are
reasonably calibrated (seven of ten reliability bins have a gap under 0.1 between predicted and
empirical violation rate; the two largest gaps are 0.198 in the 0.1–0.2 bin and 0.228 in the 0.3–0.4 bin)
and its default 0.5 threshold is close to optimal (best 𝐹1 = 0.765 at threshold 0.25 versus 𝐹1 = 0.735
at 0.5). Held out, however, every constraint type is severely miscalibrated in the same direction: the
verifier’s low-probability bins massively underestimate the true violation rate (for example, held-
out diffraction: predicted 0.07–0.14 in its lowest bins, actual 0.47–0.49; held-out spectra: predicted
0.02–0.15, actual 0.84–0.93), so at the default 0.5 threshold the verifier essentially never fires held out
(recall as low as 0.03 for diffraction), and a much lower threshold (0.05 in five of six held-out splits)
recovers usable recall at a real precision cost (for example, held-out diffraction 𝐹1 rises from 0.057 at
threshold 0.5 to 0.628 at threshold 0.05). No off-the-shelf process-reward model (PRM) comparison
is reported: we checked directly and found no general-purpose or physics/materials-science PRM
publicly available; every widely used open PRM (for example Qwen2.5-Math-PRM-7B, PRM800K-
tuned variants, MedPRM) is trained on a specific domain’s own step-labeled data (mathematics,
medicine), so applying one to these physics reasoning chains would be an uninterpretable domain
mismatch rather than a meaningful comparator, and we report this as a genuine absence rather
than an oversight.
Self-verification controls. We isolate CGSV’s contribution with three controls, matched to CGSV’s
items, models, 𝐾 , and decoding: (i) unaided self-refinement, in which the model is told only to
double-check its answer with no oracle feedback, shows no significant change (PCR 0.349 → 0.339,
𝑛 = 542, 𝑏 = 34, 𝑐 = 29, 𝑝 = 0.615); (ii) generic equal-compute re-prompting, in which the
model is simply asked to reconsider with no critique framing, likewise shows no significant change
(0.358 → 0.342, 𝑛 = 562, 𝑏 = 24, 𝑐 = 15, 𝑝 = 0.20); both controls, unlike CGSV, show nonzero
regressions. (iii) Best-of-3 independent resampling (no multi-turn revision) gives a random-pick
PCR of 0.363 and an oracle-oracle best-of-3 ceiling of 0.419 (𝑛 = 614), both below CGSV’s after-
PCR for every model, by as little as 0.02 for the weakest model and on a separately drawn item
sample. We did not build a verifier-as-selector comparison on top of best-of-𝑁 (this would need
each candidate’s chain text persisted for verifier scoring, which the current best-of-𝑁 harness does
not retain), so the best-of-3 result establishes only that resampling alone leaves real headroom
over a random pick, not that the verifier can currently capture it; this is reported as a partial result.
Together, CGSV’s significant, zero-regression gain against two null controls supports attributing it
to the physical-consistency signal specifically, not to generic self-reflection or additional sampling
at equal compute (Results, CGSV table).
Ablations, human agreement, and error analysis. (i) Tolerance sensitivity: we re-checked already-
collected real model claims against the oracle at multiple tolerance settings without new model
calls. Diffraction’s model ranking is not robust to tolerance: at tol = 0.25◦ the local model’s
PCR exceeds the API models’ pooled PCR, but the ranking reverses by tol = 1.0◦ (pairwise rank
agreement 0.0 against the default 0.5◦ across the tolerances tested); spectrum’s ranking is fully
robust across 𝑥tol ∈ {10, 20, 30} cm−1 and prominence fraction ∈ {0.03, 0.05, 0.08} (rank agreement
1.0); stability’s ranking is robust at 2 of 3 non-default tolerances in the {0, 0.025, 0.05, 0.10} eV atom−1
sensitivity grid stated in Methods (rank agreement 0.67). We flag the diffraction result as a real


                                                    24
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                         Kurban Intelligence Lab



robustness concern for any model comparison drawn from that single column. We additionally ran
an independent prompt/format sensitivity check: for diffraction, spectra, and stability, we wrote
a second, independently worded prompt template per constraint type (not a minimal edit of the
original) and re-collected real model responses from four of the paper’s API models (Gemini 2.5
Flash Lite, GPT-4o, Claude Sonnet 4.5, GPT-5.6-Terra) under both templates, then measured the
same pairwise rank agreement metric used for the tolerance check above. Diffraction’s ranking is
again fragile under this different kind of perturbation (rank agreement 0.5, echoing its tolerance-
sensitivity fragility rather than resolving it); spectra’s ranking is fairly robust to rewording (rank
agreement 0.833); stability’s ranking is more mixed (rank agreement 0.667), though its absolute rates
stay tightly clustered under both wordings (0.667–0.933 across all four models and both templates),
so this number likely reflects several close scores changing relative order rather than a dramatic
swing in any one model’s judgment. Independent of the exact ranking, GPT-5.6-Terra is the clear
standout on spectra under both wordings (0.867/0.933) while GPT-4o is consistently the weakest
under both (0.000/0.067); notably, GPT-4o’s persistent low-checkable-rate anomaly on spectra
(Results; reproduced again here under the original wording, 𝑛 = 7/15) did not reproduce under the
paraphrase (𝑛 = 15/15), a small but concrete clue that this long-standing anomaly may be sensitive
to the exact prompt wording rather than a fixed property of the (GPT-4o, spectra) pairing. (ii)
Human agreement: each precision audit was performed by a single human annotator. Accordingly,
Table 1 reports single-annotator point estimates, and no inter-rater Cohen’s 𝜅 or per-precision
confidence interval is reported. This is a limitation of the present study. (iii) Error taxonomy:
from the diffraction and microscopy oracles’ already-human-confirmed real violations (78 and 93
cases respectively; spectra and the DFT families are excluded because their human reviews predate
the spectrum-oracle and magnetism-oracle corrections and would mismatch the corrected oracles’
current fired-case population), an open-ended per-item categorization followed by a semantic
clustering pass gives a small, legible taxonomy: diffraction failures are dominated by gridline/scale
misreading (70.5%) over peak misidentification (14.1%); microscopy failures are dominated by scale-
bar unit and unit-conversion errors (37.6% and 23.7%) over scale-factor arithmetic errors (14.0%;
Fig. 2c shows three such real cases).
    (iv) Contamination: we checked whether any model chain ever states source-specific metadata
it was never shown (institution codes, database sample IDs, present only in each dataset’s own
sidecar metadata, never in the rendered plot) – zero such cases across 2,152 checked records,
a real if narrow negative signal. We compared each dataset’s public release date against each
model’s documented training cutoff where both are known: opXRD’s Zenodo record (15298026) was
published 2025-04-28, which postdates GPT-4o’s documented cutoff (2023-10, with some sources
reporting a later 2024-06 extension), ruling out direct memorization of this specific corpus for that
model; most other model–dataset pairs cannot be so ruled out because frontier providers do not
publish per-snapshot cutoff dates. A local-model perplexity comparison (real opXRD text mean log-
probability −0.18 versus procedurally generated control text in the same surface format at −1.91)
is reported but explicitly flagged as weak and non-diagnostic: lower perplexity on real structured
data than on random control text is fully explained by real data being more predictable than
gibberish, independent of memorization. Per-family, per-modality item counts with provenance:
205 (diffraction, opXRD), 481 (microscopy, NFFA-EUROPE), 575 (spectra, RRUFF), 395 (stability),
255 (metallicity), and 241 (magnetism) real oracle-checked records make up the 2,152-record verifier


                                                 25
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                               Kurban Intelligence Lab



dataset described above; they are not the 4,472 records of the main evaluation in Supplementary
Table S1, which pools three seeds over nine models.
Statistics. The model-by-constraint-type sweep (9 × 6 × 3 = 162 cells) reports bootstrap confidence
intervals, not a family of significance tests, so a Holm/Benjamini–Hochberg correction (designed
for hypothesis tests) does not apply to those 162 cells in the same sense. The actual family
of significance tests in this paper is Table 3’s six exact McNemar tests (four per-model CGSV
comparisons plus the two mechanism-isolation controls); we corrected this family directly
(matpcr_metrics.holm_bonferroni, benjamini_hochberg, verified against a synthetic case and
applied to the real before/after records in experiments/exp15_multiplicity_correction.py). All
four CGSV effects survive the strictest (Holm) correction (adjusted 𝑝 < 10−3 for every model,
most far smaller), and both negative controls remain non-significant under either correction
(Holm-adjusted 𝑝 = 0.615 and 0.399); the qualitative finding, that CGSV works while generic
self-refinement and re-prompting do not, is robust to multiplicity correction, not an artifact of
testing six things at once. We separately checked the specific unit-of-analysis mechanism raised
above and found it does not apply as stated (seeds draw independent item subsets, verified directly).

DATA AND CODE AVAILABILITY
The benchmark is derived entirely from public datasets: experimental powder diffraction patterns,[49]
scanning electron micrographs,[50] Raman spectra,[51] and first-principles reference values.[52] The as-
sembled MatPCR items and the oracle reference values with their provenance are available at https:
//zenodo.org/records/21829644.
   All code, including the oracle implementations with unit tests, the chain-parsing code, the metric code,
the DFT protocol settings, the prompts, and the released verifier weights, is available at https://github.c
om/KurbanIntelligenceLab/matpcr.

AUTHOR CONTRIBUTIONS
H.K. and M.K. conceived the study. H.K., R.K., and M.K. designed the methodology. R.K. and H.K.
implemented the physical oracles, the metric, and the verifier. M.K. designed the density functional theory
protocol and the physics underlying the oracles and is responsible for their validation. All authors designed
the experimental protocol, interpreted the analyses, and wrote and approved the manuscript. H.K., Hasan
Kurban; R.K., Rasul Khanbayov; M.K., Mustafa Kurban.

COMPETING INTERESTS
The authors declare no competing interests. In line with the policy that large language models do not satisfy
authorship criteria, we disclose that an AI assistant was used during the preparation of this manuscript. All
content was reviewed and verified by the human authors, who take full responsibility for the work. No AI
system is an author.

FUNDING
The authors received no specific funding for this work.

ACKNOWLEDGMENTS
Computations were run across two single-GPU hosts over the course of the study: an NVIDIA P100 (16 GB)
host for early, pre-pilot exploratory work that produced no result reported here, and an NVIDIA A100 (80 GB)
host for the pilot and Experiment 1–4 onward, later joined by QCRI’s Panther cluster (A100 80 GB and H200
141 GB partitions) for the later-generation model refresh, the verifier retraining, and the DFT-grounded re-


                                                     26
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                              Kurban Intelligence Lab



runs. Exact total GPU-hours are not recoverable: most historical result logs did not record per-item timing,
and the original P100 host’s logs no longer exist, so we do not report an aggregate figure we cannot verify.
We thank the institutions maintaining the public datasets this work depends on (opXRD, NFFA-EUROPE,
RRUFF, Materials Project).


References
 [1] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction
     tuning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),
     pages 26296–26306, June 2024.
 [2] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V.
     Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In
     Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, Advances in
     Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems
     2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022. URL http://papers
     .nips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Confere
     nce.html.
 [3] Zhengzhao Lai, Youbin Zheng, Zhenyang Cai, Haonan Lyu, Jinpu Yang, Hongqing Liang, Yan Hu, and
     Benyou Wang. Can multimodal llms see materials clearly? a multimodal benchmark on materials
     characterization. arXiv preprint arXiv:2509.09307, 2025.
 [4] Prateek Verma, Minh-Hao Van, and Xintao Wu. Vision language models for scientific image analysis:
     an evaluation highlighting opportunities and challenges. npj Computational Materials, 2026.
 [5] Kamal Choudhary. Microscopygpt: generating atomic-structure captions from microscopy images of
     2d materials with vision-language transformers. The Journal of Physical Chemistry Letters, 16(27):7028,
     2025.
 [6] Zekun Li, Xianjun Yang, Kyuri Choi, Wanrong Zhu, Ryan Hsieh, HyeonJung Kim, Jin Hyuk Lim,
     Sungyoung Ji, Byungju Lee, Xifeng Yan, et al. Mmsci: A multimodal multi-discipline dataset for
     phd-level scientific comprehension. In AI for Accelerated Materials Design-Vienna 2024, 2024.
 [7] Elizabeth A Holm, Ryan Cohn, Nan Gao, Andrew R Kitahara, Thomas P Matson, Bo Lei, and Srujana Rao
     Yarasi. Overview: Computer vision and machine learning for microstructural characterization and
     analysis. Metallurgical and Materials Transactions A, 51(12):5985–5999, 2020.
 [8] Wei Li, Kevin G Field, and Dane Morgan. Automated defect analysis in electron microscopic images.
     npj Computational Materials, 4(1):36, 2018.
 [9] Andre Niyongabo Rubungo, Kangming Li, Jason Hattrick-Simpers, and Adji Bousso Dieng. Llm4mat-
     bench: benchmarking large language models for materials property prediction. Machine Learning:
     Science and Technology, 6(2):020501, 2025.
[10] Taoyuze Lv, Alexander Chen, Fengyu Xie, Chu Wu, Jeffrey Meng, Dongzhan Zhou, Yingheng Wang,
     Bram Hoex, Zhicheng Zhong, and Tong Xie. Atomworld: A benchmark for evaluating spatial reasoning
     in large language models on crystalline materials. arXiv preprint arXiv:2510.04704, 2025.
[11] Yingheng Tang, Wenbin Xu, Jie Cao, Weilu Gao, Steve Farrell, Benjamin Erichson, Michael W Mahoney,
     Andy Nonaka, and Zhi Yao. Matterchat: A multi-modal llm for material science. arXiv preprint
     arXiv:2502.13107, 2025.
[12] Dezhi Luo, Yijiang Li, Maijunxian Wang, Tianwei Zhao, Bingyang Wang, Siheng Wang, Pinyuan Feng,
     Pooyan Rahmanzadehgervi, Ziqiao Ma, and Hokin Deng. Vision language models cannot reason about
     physical transformation. arXiv preprint arXiv:2603.07109, 2026.




                                                    27
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                              Kurban Intelligence Lab



[13] Yun Luo, Futing Wang, Qianjia Cheng, Fangchen Yu, Haodi Lei, Jianhao Yan, Chenxi Li, Jiacheng Chen,
     Yufeng Zhao, Haiyuan Wan, et al. P1-vl: bridging visual perception and scientific reasoning in physics
     olympiads. arXiv preprint arXiv:2602.09443, 2026.
[14] Vikash Singh, Debargha Ganguly, Haotian Yu, Chengwei Zhou, Prerna Singh, Brandon Lee, Vipin
     Chaudhary, and Gourav Datta. Toward guarantees for clinical reasoning in vision language models
     via formal verification. arXiv preprint arXiv:2602.24111, 2026.
[15] Ziqi Wang, Hongshuo Huang, Hancheng Zhao, Changwen Xu, Shang Zhu, Jan Janssen, and Venkata-
     subramanian Viswanathan. Dreams: Density functional theory based research engine for agentic
     materials simulation. arXiv preprint arXiv:2507.14267, 2025.
[16] Ryan Nduma, Hyunsoo Park, and Aron Walsh. Crystalyse: a multi-tool agent for materials design.
     arXiv preprint arXiv:2512.00977, 2025.
[17] Lianhao Zhou, Hongyi Ling, Keqiang Yan, Kaiji Zhao, Xiaoning Qian, Raymundo Arróyave, Xiaofeng
     Qian, and Shuiwang Ji. Toward greater autonomy in materials discovery agents: Unifying planning,
     physics, and scientists. arXiv preprint arXiv:2506.05616, 2025.
[18] Alireza Ghafarollahi and Markus J Buehler. Atomagents: Alloy design and discovery through physics-
     aware multi-modal multi-agent artificial intelligence. arXiv preprint arXiv:2407.10022, 2024.
[19] Shuyi Jia, Chao Zhang, and Victor Fung. Llmatdesign: Autonomous materials discovery with large
     language models. arXiv preprint arXiv:2406.13163, 2024.
[20] Jiacheng Zhou, Bo Xiao, Qi Liu, Lifeng Liu, and Lei Zhang. Matpc: prompting large language model,
     crystal structure prediction, and first-principles for semantic-driven material design. ACS Applied
     Materials & Interfaces, 17(31):44528–44540, 2025.
[21] Yeonghun Kang and Jihan Kim. Chatmof: an artificial intelligence system for predicting and generating
     metal-organic frameworks using large language models. Nature communications, 15(1):4705, 2024.
[22] Huan Zhang, Yu Song, Ziyu Hou, Santiago Miret, and Bang Liu. Honeycomb: A flexible llm-based
     agent system for materials science. In Findings of the Association for Computational Linguistics: EMNLP
     2024, pages 3369–3382, 2024.
[23] Minh-Hao Van, Prateek Verma, Chen Zhao, and Xintao Wu. A survey of ai for materials science:
     foundation models, llm agents, datasets, and tools. ACM Computing Surveys, 58(14):1–37, 2026.
[24] Ming Du, Yanqi Luo, Srutarshi Banerjee, Michael Wojcik, Jelena Popovic, and Mathew J Cherukara.
     Eaa: Automating materials characterization with vision language model agents. arXiv preprint
     arXiv:2602.15294, 2026.
[25] Xian Wang, Qun Zeng, Dong-Hui Xu, Li Zhang, Gang Jiang, and Mingli Yang. Accelerating materials
     discovery via ai-agent integration of large language models and simulation tools. Journal of Materials
     Informatics, 6(1):N–A, 2026.
[26] Lee Hyun, Sohee Yoon, Jinwoo Park, Sue In Chae, Seongeon Park, Jooyeon Ahn, Yebin Jung, Youjung
     Chung, Hogeun Chang, Sujin Park, et al. Aligning reasoning llms for materials discovery with physics-
     aware rejection sampling. arXiv preprint arXiv:2509.00768, 2025.
[27] Nathan J Szymanski and Christopher J Bartel. Establishing baselines for generative discovery of
     inorganic crystals. Materials Horizons, 12(19):8000–8011, 2025.
[28] Bowen Deng, Peichen Zhong, KyuJung Jun, Janosh Riebesell, Kevin Han, Christopher J Bartel, and
     Gerbrand Ceder. Chgnet as a pretrained universal neural network potential for charge-informed
     atomistic modelling. Nature Machine Intelligence, 5(9):1031–1041, 2023.
[29] Shixin Yi and Lin Shang. Corgi: Verified chain-of-thought reasoning with post-hoc visual grounding.
     arXiv preprint arXiv:2508.00378, 2025.




                                                    28
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                               Kurban Intelligence Lab



[30] Linzhuang Sun, Hao Liang, Jingxuan Wei, Bihui Yu, Tianpeng Li, Fan Yang, Zenan Zhou, and Wentao
     Zhang. Mm-verify: Enhancing multimodal reasoning with chain-of-thought verification. In Proceedings
     of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
     pages 14100–14115, 2025.
[31] Chaoya Jiang, Yongrui Heng, Wei Ye, Haiyang Xu, Ming Yan, Ji Zhang, Fei Huang, and Shikun Zhang.
     Vlm-r3 : Region recognition, reasoning, and refinement for enhanced multimodal chain-of-thought.
     Advances in Neural Information Processing Systems, 38:63841–63869, 2026.
[32] Viraj Prabhu, Senthil Purushwalkam, An Yan, Caiming Xiong, and Ran Xu. Trust but verify: Program-
     matic vlm evaluation in the wild. In 2025 IEEE/CVF International Conference on Computer Vision (ICCV),
     pages 3258–3267. IEEE, 2025.
[33] Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jingren
     Zhou, and Junyang Lin. Processbench: Identifying process errors in mathematical reasoning. In
     Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
     Papers), pages 1009–1024, 2025.
[34] Shudong Liu, Hongwei Liu, Junnan Liu, Linchen Xiao, Songyang Gao, Chengqi Lyu, Yuzhe Gu, Wenwei
     Zhang, Derek F Wong, Songyang Zhang, et al. Compassverifier: A unified and robust verifier for llms
     evaluation and outcome reward. In Proceedings of the 2025 Conference on Empirical Methods in Natural
     Language Processing, pages 33454–33482, 2025.
[35] Minki Kang, Jongwon Jeong, and Jaewoong Cho. T1: Tool-integrated self-verification for test-time
     compute scaling in small language models. arXiv e-prints, pages arXiv–2504, 2025.
[36] Daya Guo et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. Nature,
     645(8081):633–638, 2025. ISSN 1476-4687. doi: 10.1038/s41586-025-09422-z. URL http://dx.doi.org
     /10.1038/s41586-025-09422-z.
[37] Zijie Chen, Zhenghao Lin, Xiao Liu, Zhenzhong Lan, Yeyun Gong, and Peng Cheng. Improving data
     and reward design for scientific reasoning in large language models, 2026. URL https://arxiv.org/
     abs/2602.08321.
[38] Jinghan Jia, Joe Benton, and Eric Easley. Faithfulness as information flow: Evaluating and training
     faithful chain-of-thought reasoning. arXiv preprint arXiv:2605.24286, 2026.
[39] Xiangyu Zhao, Henry Hengyuan Zhao, Yiheng Wang, Wanghan Xu, Yuhao Zhou, Qinglong Cao,
     Zhiwang Zhou, Lei Bai, Wenlong Zhang, and Xiao-Ming Wu. SCI-PRM: A tool aware process reward
     model for scientific reasoning verification. CoRR, abs/2606.04579, 2026. doi: 10.48550/ARXIV.2606.04
     579. URL https://doi.org/10.48550/arXiv.2606.04579.
[40] Massimiliano Pronesti, Anya Belz, and Yufang Hou. Beyond outcome verification: Verifiable process
     reward models for structured reasoning. In Maria Liakata, Viviane P. Moreira, Jiajun Zhang, and
     David Jurgens, editors, Findings of the Association for Computational Linguistics, ACL 2026, San Diego,
     California, United States, July 2-7, 2026, pages 32187–32202. Association for Computational Linguistics,
     2026. doi: 10.18653/V1/2026.FINDINGS-ACL.1611. URL https://doi.org/10.18653/v1/2026.findi
     ngs-acl.1611.
[41] Chengliang Xu, Xiaogang Li, Peiyao Xiao, Beng Wang, Hu Wei, and Bing Zhao. Crystalxrd-bench:
     Benchmarking vision-language models for xrd peak indexing across diverse crystalline materials. arXiv
     preprint arXiv:2605.29446, 2026.
[42] Sarrah R. Mikhail Leung, Taehan Kim, and Jeongbin Park. Mat-pref: Verifiable-reward training
     improves compositional reasoning in inorganic materials, 2026. URL https://arxiv.org/abs/2606.2
     1830.
[43] Can Polat, Erchin Serpedin, Mustafa Kurban, and Hasan Kurban. Crysmtm: a multiphase, temperature-



                                                    29
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                              Kurban Intelligence Lab



     resolved, multimodal dataset for crystalline materials. Machine Learning: Science and Technology, 6(3):
     030603, aug 2025. doi: 10.1088/2632-2153/adf9bc. URL https://doi.org/10.1088/2632-2153/adf9bc.
[44] Can Polat, Erchin Serpedin, Mustafa Kurban, and Hasan Kurban. How far can you grow? characterizing
     the extrapolation frontier of graph generative models for materials science. In Proceedings of the 32nd
     ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2, page 11821–11832. ACM,
     August 2026. doi: 10.1145/3770855.3818872. URL http://dx.doi.org/10.1145/3770855.3818872.
[45] Can Polat, Hasan Kurban, and Mustafa Kurban. Quantumshellnet: Ground-state eigenvalue prediction
     of materials using electronic shell structures and fermionic properties via convolutions. Computational
     Materials Science, 246:113366, 2025. ISSN 0927-0256. doi: https://doi.org/10.1016/j.commatsci.2024.113
     366. URL https://www.sciencedirect.com/science/article/pii/S0927025624005871.
[46] Can Polat, Mustafa Kurban, and Hasan Kurban. Multimodal neural network-based predictive modeling
     of nanoparticle properties from pure compounds. Machine Learning: Science and Technology, 5(4), 2024.
     ISSN 2632-2153. doi: 10.1088/2632-2153/ad9708.
[47] Samir Abdaljalil, Hasan Kurban, and Erchin Serpedin. Halluverse25: Fine-grained multilingual bench-
     mark dataset for llm hallucinations, 2025. URL https://arxiv.org/abs/2503.07833.
[48] Rasul Khanbayov, Mohamed Rayan Barhdadi, Erchin Serpedin, and Hasan Kurban. Iris: A real-world
     benchmark for inverse recovery and identification of physical dynamic systems from monocular video,
     2026. URL https://arxiv.org/abs/2603.16432.
[49] Daniel Hollarek, Henrik Schopmans, Jona Östreicher, Jonas Teufel, Bin Cao, Adie Alwen, Simon Schwei-
     dler, Mriganka Singh, Tim Kodalle, Hanlin Hu, et al. opxrd: Open experimental powder x-ray diffraction
     database. Advanced Intelligent Discovery, 2(2):e202500044, 2026.
[50] Rossella Aversa, Mohammad Modarres, Stefano Cozzini, Regina Ciancio, and Alberto Chiusole. The
     first annotated set of scanning electron microscopy images for nanoscience. Scientific Data, 5:180172,
     08 2018. doi: 10.1038/sdata.2018.172.
[51] Barbara Lafuente, R. T. Downs, H. Yang, and N. Stone. 1. The power of databases: The RRUFF project,
     pages 1–30. De Gruyter (O), Berlin, München, Boston, 2016. ISBN 9783110417104. doi: doi:10.1515/97
     83110417104-003. URL https://doi.org/10.1515/9783110417104-003.
[52] Anubhav Jain, Shyue Ping Ong, Geoffroy Hautier, Wei Chen, William Davidson Richards, Stephen
     Dacek, Shreyas Cholia, Dan Gunter, David Skinner, Gerbrand Ceder, et al. Commentary: The materials
     project: A materials genome approach to accelerating materials innovation. APL materials, 1(1), 2013.
[53] Bin Cao, Yang Liu, Zinan Zheng, Ruifeng Tan, Jia Li, and Tong-yi Zhang. Simxrd-4m: big simulated
     x-ray diffraction data and crystal symmetry classification benchmark. In International Conference on
     Learning Representations, volume 2025, pages 70721–70745, 2025.
[54] Quanyu Long, Kai Jie Jiang, Jianda Chen, Xu Guo, Leilei Gan, and Wenya Wang. Self-verification
     dilemma: Experience-driven suppression of overused checking in llm reasoning. arXiv preprint
     arXiv:2602.03485, 2026.
[55] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang,
     Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan,
     Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng,
     Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025. URL
     https://arxiv.org/abs/2502.13923.




                                                    30
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                         Kurban Intelligence Lab



Supplementary Information
This file contains Supplementary Note 1 (standard derivations underlying the oracles and estimators
used in the Article) and Supplementary Table S1 (per-cell Physical-Consistency Rate with bootstrap
confidence intervals). The novel measurement result (Proposition 1 and Corollary 1) is stated and
proved in the main Article.

Supplementary Note 1: standard derivations
The results collected here are standard and are included for completeness.

1.1 Bragg’s law and 𝑑 -spacing
For constructive interference from lattice planes of spacing 𝑑 at Bragg angle 𝜃 with a beam of
wavelength 𝜆, the path difference 2𝑑 sin 𝜃 equals an integer number of wavelengths; for first order
(𝑛 = 1), 𝜆 = 2𝑑 sin 𝜃. The measured scattering angle is 2𝜃, so a claimed peak at 2𝜃 corresponds
to 𝑑 = 𝜆/(2 sin 𝜃) with 𝜃 equal to half the measured angle. Physical realizability requires sin 𝜃 ≤
1, equivalently 𝑑 ≥ 𝜆/2, and the instrument range further restricts 2𝜃 to a finite window; the
diffraction oracle enforces both and matches claimed peaks to the reference pattern of the stated
phase within tolerance.

1.2 Scale-bar calibration
A scale bar of stated length 𝓁nm spanning 𝑝bar pixels fixes the calibration 𝑠 = 𝓁nm /𝑝bar (nanometres
per pixel). For an image whose long edge is 𝑝img pixels, the field of view is 𝑠 𝑝img nanometres,
which upper-bounds any reported feature size and defines the microscopy oracle.

1.3 Convex-hull stability
For a given composition, the energy above the convex hull 𝐸hull ≥ 0 is the formation energy
minus that of the lowest-energy combination of stable phases at the same composition. A phase
is thermodynamically stable when 𝐸hull = 0 and is treated as within tolerance when 𝐸hull ≤ 𝜖; the
DFT-grounded near-hull oracle uses the reported threshold 𝜖 = 0.05 eV atom−1 .

1.4 Percentile bootstrap confidence intervals
For a rate estimated from 𝑛 items we resample items with replacement 𝐵 times, recompute the
rate on each resample, and report the empirical 𝛼/2 and 1 − 𝛼/2 quantiles. Under independent
sampling of items the interval is consistent as 𝑛, 𝐵 → ∞. Where items share a parent source (for
example, several questions about one structure), we resample at the source level to respect that
dependence. We report the interval for all rates.

1.5 Concentration of the empirical rate
For a rate 𝑋̄ = 𝑛1 ∑𝑛𝑖=1 𝑋𝑖 that averages independent variables 𝑋𝑖 ∈ [0, 1] with mean 𝔼[𝑋̄ ] = 𝜇,
                                                         2
Hoeffding’s inequality gives Pr[ |𝑋̄ − 𝜇| > 𝑡 ] ≤ 2𝑒 −2𝑛𝑡 for every 𝑡 > 0. Applied to 𝑋𝑖 = 1 − 𝑌𝑖
this bounds the sampling error of PCR⋆ about the population physical-consistency rate about
the population physical-consistency rate; where items share a parent source, 𝑛 is the number of
independent sources, matching the source-level percentile bootstrap above.

                                                 31
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                   Kurban Intelligence Lab



1.6 Exact McNemar test
For paired before/after consistency, let 𝑏 and 𝑐 be the numbers of discordant items (consistent-then-
inconsistent, i.e. regressions, and inconsistent-then-consistent, i.e. fixes). Under the null that each
discordant item changes direction with probability 12 , 𝑐 ∼ Binomial(𝑏 + 𝑐, 12 ), and the two-sided
exact 𝑝-value is min(1, 2 ∑min(𝑏,𝑐)
                             𝑘=0
                                      𝑏+𝑐 −(𝑏+𝑐)
                                     ( 𝑘 )2      ). This is the test used for CGSV in the main Article.

1.7 Distribution-free bound on the total error of a reported rate
The main Article’s Proposition 1 and Corollary 1 are exact statements about the oracle’s bias
on a fixed set of items. If, in addition, the checkable items are drawn independently from the
benchmark’s item-generating process, with 𝜇 = 𝔼[1 − 𝑌𝑖 ] that process’s physical-consistency rate,
then splitting PCR − 𝜇 = (PCR − PCR⋆ ) + (PCR⋆ − 𝜇), bounding the first term by (1 − 𝑑)    ̂ + 𝑓̂
(Corollary 1) and the second by the concentration inequality above gives, for every 𝑡 > 0, with
                                2
probability at least 1 − 2𝑒 −2𝑛𝑡 ,

                                |PCR − 𝜇| ≤ (1 − 𝑑)     ̂ + 𝑓̂ +           𝑡       .
                                            ⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏞⏟     ⏟⏟⏟
                                                    oracle bias         sampling

Where items share a parent source the same statement holds with 𝑛 replaced by the number 𝑚 of
independent sources under balanced source sizes; unequal sizes give a size-weighted mean and
a correspondingly weaker rate. Both steps are standard, and the independence assumption is an
idealization for a convenience benchmark. At the cell sizes used in the Article the sampling term is
far looser than the percentile bootstrap interval: at 𝑛 = 90 and 95% confidence it is 𝑡 = 0.143, against
reported per-cell intervals of roughly ±0.09. The Article therefore reports bootstrap intervals as its
uncertainty and uses this bound only to show that the two sources of error are separately controlled.




                                                      32
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                           Kurban Intelligence Lab



Supplementary Figure S1
Oracle precision audit, every family, full breakdown. Referenced from the main Article’s
Results (Oracle validity subsection). Each bar is every human-reviewed oracle-fired case for that
family (Article, Table 1), split into real violations, false positives, and unsure verdicts. Precision is
high across the board (77.2–95.3%) but not uniform: diffraction’s tolerance is visibly the tightest
relative to typical model precision, while the three DFT-grounded families cluster above 92%.

                Oracle precision audit: every human-reviewed fired case, all six families

    GEOMETRIC ORACLES
            Diffraction                       77.2%                                                       n=101
                 (XRD)
            Microscopy                             88.6%                                                  n=105
                 (SEM)
               Spectra                                92.3%                                               n=495
              (Raman)
    DFT-GROUNDED ORACLES
              Stability                                95.3%                                              n=107

            Metallicity                               94.7%                                               n=114

            Magnetism                                 92.2%                                               n=115

                          0       20             40                 60              80               100
                                          Share of oracle-fired cases judged by human review
                                                                     Real violation      False positive           Unsure




                                                       33
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                         Kurban Intelligence Lab



Supplementary Table S1
Per-cell Physical-Consistency Rate with bootstrap 95% confidence intervals. Referenced
from the main evaluation table of the Article. 𝑛 is the number of checkable records in the cell
(pooled across 𝑆 = 3 seeds); CI is the percentile bootstrap 95% interval (𝐵 = 10,000 resamples)
on the cell’s own PCR. The first four models are the originally evaluated set; the next four are
the later-generation refresh; the last (GPT-5.6-Sol) is a flagship-tier addition testing whether it
exceeds the balanced-tier GPT-5.6-Terra within the same generation (Article, Table 1 note). Each
item in this benchmark exposes exactly one checkable constraint of its own constraint type, so the
per-constraint-type violation rate 𝜌𝑡 = 1 − PCR for every cell below and is not tabulated separately.




                                                34
MATPCR: PHYSICS AS THE LABEL FOR MATERIALS REASONING                                    Kurban Intelligence Lab



                    Model                   Constraint type   𝑛    PCR        95% CI
                    Qwen2.5-VL-7B           Diffraction       64   0.500   [0.375, 0.625]
                    Qwen2.5-VL-7B           Microscopy        87   0.667   [0.563, 0.759]
                    Qwen2.5-VL-7B           Spectra           88   0.148   [0.080, 0.227]
                    Qwen2.5-VL-7B           Stability∗        90   0.744   [0.656, 0.833]
                    Qwen2.5-VL-7B           Metallicity∗      87   0.540   [0.437, 0.644]
                    Qwen2.5-VL-7B           Magnetism∗        90   0.767   [0.678, 0.856]

                    Gemini 2.5 Flash Lite   Diffraction       60   0.517   [0.400, 0.650]
                    Gemini 2.5 Flash Lite   Microscopy        86   1.000   [1.000, 1.000]
                    Gemini 2.5 Flash Lite   Spectra           90   0.278   [0.189, 0.378]
                    Gemini 2.5 Flash Lite   Stability∗        89   0.730   [0.640, 0.820]
                    Gemini 2.5 Flash Lite   Metallicity∗      84   0.702   [0.607, 0.798]
                    Gemini 2.5 Flash Lite   Magnetism∗        89   0.494   [0.382, 0.596]

                    GPT-4o                  Diffraction       64   0.625   [0.500, 0.750]
                    GPT-4o                  Microscopy        87   0.954   [0.908, 0.989]
                    GPT-4o                  Spectra           44   0.068   [0.000, 0.159]
                    GPT-4o                  Stability∗        90   0.800   [0.711, 0.878]
                    GPT-4o                  Metallicity∗      85   0.671   [0.565, 0.765]
                    GPT-4o                  Magnetism∗        90   0.678   [0.578, 0.778]

                    Claude Sonnet 4.5       Diffraction       64   0.547   [0.422, 0.672]
                    Claude Sonnet 4.5       Microscopy        87   0.977   [0.943, 1.000]
                    Claude Sonnet 4.5       Spectra           90   0.189   [0.111, 0.267]
                    Claude Sonnet 4.5       Stability∗        90   0.756   [0.667, 0.844]
                    Claude Sonnet 4.5       Metallicity∗      85   0.694   [0.600, 0.788]
                    Claude Sonnet 4.5       Magnetism∗        90   0.756   [0.666, 0.844]

                    Claude Opus 4.6         Diffraction       64   0.578   [0.453, 0.703]
                    Claude Opus 4.6         Microscopy        87   0.954   [0.908, 0.989]
                    Claude Opus 4.6         Spectra           90   0.244   [0.156, 0.333]
                    Claude Opus 4.6         Stability∗        90   0.722   [0.633, 0.811]
                    Claude Opus 4.6         Metallicity∗      86   0.721   [0.628, 0.814]
                    Claude Opus 4.6         Magnetism∗        90   0.700   [0.600, 0.789]

                    GPT-5.6-Terra           Diffraction       64   0.797   [0.703, 0.891]
                    GPT-5.6-Terra           Microscopy        81   0.951   [0.901, 0.988]
                    GPT-5.6-Terra           Spectra           90   0.833   [0.756, 0.911]
                    GPT-5.6-Terra           Stability∗        90   0.656   [0.556, 0.756]
                    GPT-5.6-Terra           Metallicity∗      85   0.659   [0.553, 0.753]
                    GPT-5.6-Terra           Magnetism∗        90   0.767   [0.678, 0.844]

                    Qwen3-VL-8B-Instruct    Diffraction       62   0.468   [0.355, 0.597]
                    Qwen3-VL-8B-Instruct    Microscopy        86   0.802   [0.709, 0.884]
                    Qwen3-VL-8B-Instruct    Spectra           90   0.133   [0.067, 0.200]
                    Qwen3-VL-8B-Instruct    Stability∗        87   0.713   [0.621, 0.805]
                    Qwen3-VL-8B-Instruct    Metallicity∗      77   0.688   [0.584, 0.792]
                    Qwen3-VL-8B-Instruct    Magnetism∗        90   0.533   [0.433, 0.633]

                    Qwen3-VL-8B-Thinking Diffraction          64   0.578   [0.453, 0.703]
                    Qwen3-VL-8B-Thinking Microscopy           87   0.885   [0.816, 0.943]
                    Qwen3-VL-8B-Thinking Spectra              87   0.092   [0.034, 0.161]
                    Qwen3-VL-8B-Thinking Stability∗           90   0.767   [0.678, 0.856]
                    Qwen3-VL-8B-Thinking Metallicity∗         87   0.644   [0.540, 0.736]
                    Qwen3-VL-8B-Thinking Magnetism∗           89   0.506   [0.404, 0.607]

                    GPT-5.6-Sol             Diffraction       61   0.820   [0.721, 0.918]
                    GPT-5.6-Sol             Microscopy        82   0.915   [0.854, 0.976]
                    GPT-5.6-Sol             Spectra           89   0.764   [0.674, 0.854]
                    GPT-5.6-Sol             Stability∗        89   0.742   [0.652, 0.831]
                    GPT-5.6-Sol             Metallicity∗      88   0.670   [0.580, 0.761]
                    GPT-5.6-Sol             Magnetism∗        90   0.733   [0.644, 0.822]

                                                   35
