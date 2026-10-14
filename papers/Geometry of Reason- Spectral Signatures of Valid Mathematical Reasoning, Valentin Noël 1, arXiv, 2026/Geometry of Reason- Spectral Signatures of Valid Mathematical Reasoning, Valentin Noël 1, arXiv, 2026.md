                                            Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning


                                                                                               Valentin Noël 1


                                                                 Abstract                                   1. Introduction
                                                                                                            The remarkable performance of large language models
                                              Verifying whether a language model is genuinely               (LLMs) on mathematical reasoning tasks (Lewkowycz et al.,
                                              reasoning or pattern-matching remains an open                 2022; Trinh et al., 2024; Chervonyi et al., 2025; Azerbayev
arXiv:2601.00791v2 [cs.LG] 10 Jun 2026




                                              problem: learned verifiers are expensive, and                 et al., 2023) has intensified interest in understanding and
                                              output-based heuristics are brittle. We show                  verifying the computational mechanisms underlying their
                                              that valid mathematical reasoning induces a mea-              outputs. When a model generates a mathematical proof,
                                              surable, training-free spectral signature in trans-           practitioners face a fundamental, epistemological, challenge:
                                              former attention. By treating each attention matrix           determining whether the output reflects genuine logical
                                              as a weighted token graph, we extract four diag-              reasoning or sophisticated pattern matching that produces
                                              nostics: Fiedler value, High-Frequency Energy                 plausible-looking but potentially flawed arguments. Re-
                                              Ratio (HFER), spectral entropy, and smoothness,               cent evaluations reinforce this concern: even frontier mod-
                                              that require no learned parameters. Experiments               els achieve below 25% on olympiad-level proofs (Petrov
                                              across seven models from four architectural fam-              et al., 2025), suggesting a “reasoning illusion” where suc-
                                              ilies yield effect sizes up to Cohen’s d = 3.30               cess may stem from pattern matching rather than genuine
                                              (p < 10−116 ), enabling 85–96% single-threshold               insight (Kuang et al., 2025). This challenge is particularly
                                              classification accuracy. Two findings sharpen the             acute in high-stakes applications such as automated theo-
                                              interpretation. First, Platonic validity: the spec-           rem proving (Polu & Sutskever, 2020; Yang et al., 2024;
                                              tral signal tracks logical coherence rather than              Ospanov et al., 2025), mathematical education (Welleck
                                              compiler acceptance, proofs rejected for time-                et al., 2022), and scientific discovery (Romera-Paredes et al.,
                                              outs or missing imports are correctly classified              2024), where undetected reasoning errors can propagate
                                              as valid, a distinction confirmed by a manual au-             with significant consequences.
                                              dit (κ = 0.82, n = 51). Second, architectural                 Current approaches to reasoning verification fall into two
                                              determinism: Sliding Window Attention shifts                  broad categories, each with substantial limitations. Output-
                                              the discriminative feature from HFER to smooth-               based verification relies on formal proof assistants such as
                                              ness (d = 2.09, p < 10−48 ), showing that atten-              Lean (de Moura & Ullrich, 2021), Coq (Bertot & Castéran,
                                              tion design governs which spectral channel en-                2013), or Isabelle (Paulson, 1994) to check whether gen-
                                              codes reasoning quality. Causal ablation confirms             erated proofs compile successfully. While sound, this ap-
                                              the signature traces induction-head circuits. The             proach conflates logical validity with syntactic acceptability:
                                              method generalises to informal chain-of-thought               proofs may be rejected due to timeout constraints, missing
                                              (d = 0.78, p < 10−3 ), and in proof search, HFER              library imports, version incompatibilities, or formatting is-
                                              reranking improves Best-of-16 Pass@1 by +4.4–                 sues rather than genuine logical errors. Conversely, proofs
                                              6.6%, matching 98% of the AUC of fully super-                 with subtle semantic errors may pass compilation if they
                                              vised probes with zero labels. Spectral graph anal-           exploit gaps in type checking or axiom systems. Learned
                                              ysis is a principled, architecture-aware primitive            verification trains classifiers on model internals (Azaria &
                                              for reasoning verification. *                                 Mitchell, 2023; Burns et al., 2023; Marks & Tegmark, 2024)
                                                                                                            or output features (Lightman et al., 2023; Cobbe et al., 2021)
                                                                                                            to predict correctness. Recent work demonstrates that in-
                                             1
                                               Devoteam, Levallois-Perret, France. Correspondence to:       ternal representations contain rich signals for hallucination
                                         Valentin Noël <valentin.noel@devoteam.com>.                       detection (Chen et al., 2024; Zhang et al., 2025a; Healy
                                                                                                            et al., 2026), yet these methods require substantial labeled
                                         Proceedings of the 43 rd International Conference on Machine       data, may not generalize across model architectures, and
                                         Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026
                                         by the author(s).                                                  risk learning spurious correlations rather than fundamental
                                             *   vcnoel/geometry-of-reason                                  properties of valid reasoning.

                                                                                                        1
                           Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                                                                                        Coherent topology

       Proof Text                                                                        Valid Proof
       theorem: 2003             Transformer             Graph Laplacian
         % 11 = 1              Extract A(ℓ,h) , X (ℓ)    L = D − 12 (A + A⊤ )
                                                                                      Low HFER, High λ2           Classification
      proof: norm num
                                                                                                                  85–96% Accuracy
                                                                                                                     |d| ≥ 2.09
                                                                                        Invalid Proof


                                                                                      High HFER, Low λ2

                                                                                       Fragmented topology


     Figure 1. Method Overview. Spectral analysis of attention graphs enables training-free validity classification (d up to 3.30).


We propose an alternative paradigm grounded in spectral                2. Related Work
graph theory. Our central insight is that self-attention in-
duces a dynamic weighted graph over tokens, where edge                 Mechanistic Interpretability. Understanding the internal
weights correspond to attention scores. This perspective               computations of transformers has been a central goal of
aligns with recent work on attention graphs for mechanistic            interpretability research. Foundational work by Elhage et al.
interpretability (El et al., 2025; Rai et al., 2024). The spec-        (2021) introduced mathematical frameworks for analyzing
tral properties of this graph, eigenvalues and eigenvectors            transformer circuits, while Olsson et al. (2022) identified
of its Laplacian, encode global structural information about           “induction heads” as key mechanisms for in-context learn-
information routing.                                                   ing. Subsequent work has analyzed attention patterns in
                                                                       arithmetic (Nanda et al., 2023; Hanna et al., 2023), factual
This hypothesis draws motivation from spectral graph the-              recall (Meng et al., 2022; Geva et al., 2023), and reason-
ory (Chung, 1997) and neural manifold geometry (Chung                  ing tasks (Stolfo et al., 2023; Liu et al., 2022). Recent
et al., 2018; Cohen et al., 2020). Recent work establishes             surveys (Rai et al., 2024) and tutorials systematize these
spectral theories connecting representation geometry to neu-           techniques, while new methods enable attention head inter-
ral prediction (Canatar et al., 2023), showing that manifold           vention for causal analysis (Kadem & Zheng, 2026) and
capacity, how efficiently neural populations encode task-              sparse autoencoder-based feature extraction. Our work com-
relevant structure, is captured by geometric and spectral              plements these approaches by analyzing the global geo-
properties (Chou et al., 2024; 2025). Findings that atten-             metric structure of attention rather than identifying specific
tion can be made vastly sparser while preserving capabil-              circuits.
ity (Draye et al., 2025) suggest essential structure may reside
in low-dimensional spectral features. We thus expect valid             Probing and Representation Analysis. Linear probes have
proofs to induce smoother, well-connected attention graphs,            been extensively used to extract linguistic (Hewitt & Man-
and invalid reasoning to exhibit spectral irregularity.                ning, 2019; Tenney et al., 2019), semantic (Ettinger, 2020;
                                                                       Li et al., 2021), and factual (Petroni et al., 2019) informa-
Contributions. We make the following contributions:                    tion from transformer representations. Recent work has
                                                                       probed for truthfulness (Azaria & Mitchell, 2023; Marks &
1. We introduce a training-free framework for reasoning                Tegmark, 2024), uncertainty (Kadavath et al., 2022; Kuhn
   validity detection based on spectral analysis of attention          et al., 2023), and reasoning capabilities (Saparov et al., 2023;
   graphs, achieving 82.8–85.9% accuracy under nested                  Dziri et al., 2024). Notably, 2025 work demonstrates that
   cross-validation and up to 95.6% with calibrated thresh-            internal representations contain discriminative signals for
   olds (Sections 3 and 4).                                            hallucination detection (Chen et al., 2024; Zhang et al.,
                                                                       2025a;c), with attention outputs often providing stronger
2. We demonstrate cross-architecture universality across               signals than other internal representations. However, con-
   seven models from four families with |d| ≥ 2.09 and                 cerns about probe reliability (Belinkov, 2022; Hewitt &
   pMW < 10−47 in all cases, and show robustness across                Liang, 2019) motivate training-free alternatives. Our spec-
   all difficulty strata (d ≥ 1.31 for complex proofs, Sec-            tral approach requires no learned parameters and operates
   tion 4).                                                            on attention structure rather than hidden states.
3. We discover Platonic validity: the spectral method de-              Graph Signal Processing on Neural Networks. The
   tects logical coherence rather than compiler acceptance,            application of spectral graph theory to neural networks
   identifying mathematically sound proofs that formal sys-            has a rich history, beginning with spectral graph convo-
   tems reject on technical grounds (Section 5.2).                     lutions (Bruna et al., 2013; Defferrard et al., 2016; Kipf &

                                                                   2
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

Welling, 2017). Recent work analyzes transformers through             We interpret each attention matrix as defining a directed
graph-theoretic lenses, studying over-smoothing (Shi et al.,          weighted graph G (ℓ,h) = (V, E (ℓ,h) , A(ℓ,h) ) where vertices
2022; Rusch et al., 2023) and designing spectral attention            V = {1, . . . , N } correspond to tokens and edge weights are
mechanisms (Kreuzer et al., 2021; Bo et al., 2023). El et al.         given by attention scores. To enable spectral analysis, we
(2025) introduce Attention Graphs for mechanistic inter-              symmetrize to obtain an undirected graph:
pretability, establishing mathematical equivalences between
message passing and self-attention. Draye et al. (2025) show                                    1  (ℓ,h)              
                                                                                  W (ℓ,h) =        A      + (A(ℓ,h) )⊤           (1)
that attention can be made orders of magnitude sparser while                                    2
preserving capability, suggesting redundancy exploitable by
spectral methods. Our work extends this line by extract-              Head Aggregation. To obtain a single graph per layer, we
ing multiple spectral diagnostics correlated with reasoning           aggregate across heads using attention mass weighting:
validity.
                                                                                       H                               (ℓ)
LLM Verification and Hallucination Detection. Verifying                                X      (ℓ)            (ℓ)  s
                                                                            W̄ (ℓ) =         αh W (ℓ,h) ,   αh = PH h            (2)
LLM outputs has received substantial attention. Process-                                                                  (ℓ)
                                                                                       h=1                           g=1 sg
based reward models (Lightman et al., 2023; Uesato et al.,
2022) train verifiers on step-level annotations, while self-                   (ℓ)    P      (ℓ,h)
consistency methods (Wang et al., 2023) leverage sampling             where sh = i,j Aij = N is the total attention mass
diversity. For hallucination detection, recent approaches             of head h (equal across heads for standard attention, but we
leverage internal representations (Healy et al., 2026), eigen-        retain this formulation for generality and compatibility with
value analysis of hidden states and latent probing (Bhatnagar         sparse attention variants). We examine uniform weighting
et al., 2026). Our method differs fundamentally: we require           αh = 1/H as a robustness check in Section C.10.
no training, no sampling, and operate on attention geometry           Graph Laplacian. The combinatorial graph Laplacian of
rather than output content or hidden state magnitudes.                the aggregated attention graph is:
Neural Theorem Proving. LLMs have achieved impres-
sive results in formal mathematics. Recent systems achieve                                 L(ℓ) = D̄ (ℓ) − W̄ (ℓ)                (3)
99.2% on MiniF2F (Varambally et al., 2025) and strong
results on PutnamBench through neuro-symbolic collab-                 where D̄ (ℓ) = diag(W̄ (ℓ) 1) is the degree matrix. The
oration (Ospanov et al., 2025). However, evaluations on               Laplacian is symmetric positive semidefinite with eigen-
2025 USAMO problems reveal that even frontier mod-                    decomposition L(ℓ) = U (ℓ) Λ(ℓ) (U (ℓ) )⊤ , where eigen-
els struggle with rigorous proof generation (Petrov et al.,           values satisfy 0 = λ1 ≤ λ2 ≤ · · · ≤ λN . We
                                                                                                                   (ℓ)
2025), achieving below 25% accuracy. Benchmarks such                  also examine the normalized Laplacian Lsym = I −
                                                                         (ℓ) −1/2   (ℓ) (ℓ) −1/2
as MiniF2F (Zheng et al., 2022), RealMath (Zhang et al.,              (D̄ )       W̄ (D̄ )        in Section C.11.
2025b), and FrontierMath (Glazer et al., 2024) enable evalu-
ation across difficulty levels. Our work addresses a comple-          3.2. Graph Signals from Hidden States
mentary problem: assessing proof validity without formal
verification, enabling faster feedback during proof search.           Let X (ℓ) ∈ RN ×d denote the hidden state matrix at layer
                                                                      ℓ, where row i contains the d-dimensional representation
3. Methods                                                            of token i. Following the graph signal processing frame-
                                                                      work (Shuman et al., 2013; Ortega et al., 2018), we treat
We develop a framework for analyzing transformer attention
                                                                      each column of X (ℓ) as a signal defined on the vertices
through the lens of spectral graph theory. Our approach
                                                                      of the attention graph. This perspective enables analysis
treats attention matrices as defining weighted graphs over
                                                                      of how token representations vary with respect to attention
tokens, then extracts spectral properties that characterize the
                                                                      structure.
geometry of information flow.
                                                                      The Graph Fourier Transform (GFT) projects signals onto
3.1. Attention as Dynamic Graphs                                      the eigenbasis of the Laplacian:

Consider a transformer with L layers, H attention heads                             X̂ (ℓ) = (U (ℓ) )⊤ X (ℓ) ∈ RN ×d             (4)
per layer, processing a sequence of N tokens. At layer
ℓ ∈ {1, . . . , L} and head h ∈ {1, . . . , H}, let A(ℓ,h) ∈
                                                                      where row m of X̂ (ℓ) contains the spectral coefficients at
RN ×N denote the post-softmax attention matrix, where
   (ℓ,h)                                                              frequency λm . Low-frequency components (small λm ) cap-
Aij represents the attention weight from token i to token             ture smooth variations across the graph; high-frequency
                                             PN      (ℓ,h)
j. By construction, each row sums to unity: j=1 Aij =                 components (large λm ) capture rapid variations between
1.                                                                    adjacent tokens.

                                                                  3
                            Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

3.3. Spectral Diagnostics                                                                       Proof Text P
We extract four complementary spectral diagnostics from
each layer, each capturing different aspects of graph-signal                                    Transformer
interaction.                                                                                      Layer ℓ
Definition 3.1 (Dirichlet Energy). The Dirichlet energy
quantifies the total variation of the signal with respect to
graph structure:                                                        Attention      A(ℓ,h)                     X (ℓ)    Representations
                               X
                                           (ℓ)   (ℓ)    (ℓ)
E (ℓ) = Tr (X (ℓ) )⊤ L(ℓ) X (ℓ) =        W̄ij ∥Xi −Xj ∥22
                                       i<j                                          L(ℓ) = D − W
                                                         (5)
Lower energy indicates that strongly-connected tokens (high
                                                                                            Spectral Diagnostics
attention) have similar representations.                                                     λ2 , HFER, E, SE
Definition 3.2 (High-Frequency Energy Ratio). The HFER
measures the proportion of signal energy in high-frequency
spectral components:                                                                            Valid / Invalid

                                 PN        (ℓ) 2                       Figure 2. Spectral analysis pipeline. At each layer ℓ, atten-
                                 m=K+1 ∥X̂m,· ∥2
              HFER (ℓ)
                         (K) =                               (6)       tion matrices A(ℓ,h) are symmetrized and aggregated into a graph
                                 PN      (ℓ) 2
                                  m=1 ∥X̂m,· ∥2                        Laplacian L(ℓ) . Hidden states X (ℓ) are projected onto its eigenba-
                                                                       sis, yielding four diagnostics, λ2 , HFER, E, and SE, from which a
where K is a frequency cutoff (we use the median eigen-                single threshold produces the validity prediction. No parameters
value index by default). Lower HFER indicates energy                   are trained.
concentration in smooth, low-frequency modes.
Definition 3.3 (Spectral Entropy). Spectral entropy quanti-
fies the distribution of energy across spectral modes:                 which costs O(N 3 ) using standard algorithms or O(N 2 k)
                                                                       for the k smallest eigenvalues using iterative methods. For
               N                                       (ℓ)
               X                             ∥X̂m,· ∥22                typical proof lengths (N < 1000), this adds negligible
  SE(ℓ) = −          p(ℓ)    (ℓ)
                      m log pm ,  p(ℓ)
                                   m = PN            (ℓ) 2             overhead to transformer inference. See Section B for imple-
             m=1                            r=1 ∥X̂r,· ∥2
                                                          (7)          mentation details.
Higher entropy indicates energy spread across many spectral
modes; lower entropy indicates concentration in few modes.             3.4. Validity Classification
Definition 3.4 (Fiedler Value). The Fiedler value (algebraic           Given a proof text P, our classification procedure is:
connectivity) is the second-smallest Laplacian eigenvalue:
                                                                       1. Pass P through the transformer, extracting attention ma-
                 (ℓ)
                λ2 =         min       ⊤
                                       x L   (ℓ)
                                                   x         (8)          trices {A(ℓ,h) }ℓ,h and hidden states {X (ℓ) }ℓ .
                           x⊥1,∥x∥=1

This measures how well-connected the attention graph is;               2. Compute spectral diagnostics at each layer per Sec-
higher λ2 indicates stronger global connectivity and more                 tion 3.3.
efficient information flow (Fiedler, 1973; Chung, 1997).
                                                                       3. Apply a threshold rule to classify validity.
Definition 3.5 (Smoothness). We define a normalized
smoothness measure:                                                    Our primary classifier uses a single spectral metric at a
                                        E   (ℓ)                        selected layer:
                   Smooth(ℓ) = 1 −         (ℓ)
                                                             (9)
                                        Emax                                                     h        ∗
                                                                                                                 i
                                                                                           ŷ = 1 Metric(ℓ ) ≶ τ                     (10)
        (ℓ)      (ℓ)
where Emax = λN ∥X (ℓ) ∥2F is the maximum energy achiev-
able for the given signal norm. Values near 1 indicate
smooth signals; values near 0 (or negative, in degenerate              where the metric (typically HFER or Smoothness), layer ℓ∗ ,
cases) indicate rough signals.                                         direction, and threshold τ are calibrated on a small held-out
                                                                       set. We also examine two-feature rules combining met-
Computational Complexity. Computing spectral diagnos-                  rics, which achieve marginally higher accuracy by capturing
tics requires eigendecomposition of the N × N Laplacian,               complementary information.

                                                                   4
                           Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

4. Experiments                                                          groups share identical authorship, prompting, and compila-
                                                                        tion status (both fail).
4.1. Experimental Setup
                                                                        Using the Fiedler value at the final layer, we find significant
Dataset. We evaluate on the MiniF2F benchmark (Zheng                    separation (p = 0.002, d = 1.30). However, other metrics
et al., 2022), a collection of 488 formal mathematics prob-             do not reach significance, likely due to the limited sample
lems drawn from AMC, AIME, IMO, and other compe-                        size (n = 32 total). We interpret this as suggestive but
titions, formalized in Lean (de Moura & Ullrich, 2021).                 not definitive evidence that the signal persists in model-vs-
Our initial evaluation set comprises 454 theorem-proof                  model comparisons.
pairs with 154 human-written valid proofs and 300 model-
generated invalid proofs. Through systematic label correc-              Control 2: Human perturbations (style fixed, logic cor-
tion (Section 5.2), we refine these labels by identifying 33–           rupted). A cleaner test holds authorship constant while
51 proofs per model that are logically correct but compiler-            corrupting logic. We generate n = 40 perturbed variants
rejected due to technical failures. Our corrected dataset               of human-valid proofs by deleting proof steps or substi-
contains approximately 187–205 valid and 249–267 invalid                tuting incorrect lemmas. On Llama-3.2-1B, HFER at the
proofs per model, yielding a more balanced ∼43%/57%                     final layer increases significantly under perturbation (Valid:
class split.                                                            0.331; Perturbed: 0.378; p = 1.93 × 10−9 , d = 1.10). All
                                                                        eight metric-layer combinations show significant degrada-
Models. We evaluate seven instruction-tuned models span-                tion (Table 10). This confirms the spectral signature tracks
ning four architectural families and a 16× parameter range:             logical coherence, not authorship style.
Table 1. Models evaluated. All use global (full) attention except       Evaluation protocol. To eliminate threshold selection bias,
Mistral-7B, which employs Sliding Window Attention (SWA) with           we adopt two protocols:
a 4096-token window.
                                                                        Train/val/test split. We partition the dataset 60/20/20, select
  Model             Family       Params Layers Attention                threshold on validation, and report test accuracy once. Held-
  Llama-3.2-1B      Meta          1.24B      16       Global            out test accuracies range from 73.6% (Mistral-7B) to 83.5%
  Llama-3.2-3B      Meta          3.21B      28       Global            (Llama-3B, Qwen-0.5B), substantially below the full-data
  Llama-3.1-8B      Meta          8.03B      32       Global            optimized figures but confirming generalization (Table 11).
  Qwen2.5-0.5B      Alibaba       0.49B      24       Global
  Qwen2.5-7B        Alibaba       7.62B      28       Global            Nested cross-validation. To eliminate both threshold and
  Phi-3.5-mini      Microsoft     3.82B      32       Global            feature selection leakage, we use 5-fold outer / 4-fold in-
  Mistral-7B-v0.1   Mistral AI    7.24B      32       SWA
                                                                        ner CV, selecting (metric, layer, threshold) on inner folds.
                                                                        Nested CV accuracies are 82.8%–85.9% across models
This selection provides diversity across training data, tok-            (Table 12). The most frequently selected configuration is
enization schemes, architectural details (e.g., grouped-query           mid-to-late layer HFER (6/7 models), with Phi-3.5 selecting
attention in Llama, RoPE variants), and attention mecha-                smoothness at L25.
nism design.
                                                                        Multiple comparisons. Applying Benjamini-Hochberg
Metrics. We report classification accuracy, Cohen’s d ef-               correction at FDR = 0.05 over 160 hypotheses (5 metrics ×
fect size for the best discriminating feature, and p-values             32 layers), 156/160 (97.5%) remain significant for Llama-
from both Mann-Whitney U tests (pMW ) and two-sided                     3.1-8B, confirming the phenomenon is widespread rather
Welch’s t-tests (pt ). Effect sizes are computed as d =                 than concentrated in a few cherry-picked combinations.
(µvalid − µinvalid )/spooled where spooled is the pooled standard
deviation. Following standard conventions (Cohen, 1988),                Interpretation of accuracy metrics. We report two accu-
we interpret |d| ≥ 0.8 as large; our observed effects of                racy figures that serve different purposes. Calibrated ac-
|d| ≥ 2.09 are thus exceptionally large.                                curacy (89–95%) represents achievable performance when
                                                                        thresholds are tuned on the target distribution, analogous to
4.2. Robustness Controls                                                calibrating a thermometer before deployment. This is appro-
                                                                        priate when practitioners will calibrate on a small labeled
Control 1: Model-generated valid vs. invalid. To test                   sample (∼50 examples) before use. Nested CV accuracy
whether the spectral signature reflects validity rather than            (82.8–85.9%) represents worst-case generalization with no
human-vs-model authorship, we compare model-generated                   target distribution access, penalizing both threshold and fea-
proofs with differing semantic status. We identify n = 16               ture selection. The large gap between these figures reflects
“reclaimed” proofs, model-generated attempts that are se-               calibration cost, not overfitting: our classifier has exactly
mantically correct but rejected by Lean due to technical                one parameter (threshold τ ), and the underlying effect sizes
failures, and compare against n = 16 randomly sampled                   (d ≥ 2.09) are invariant to threshold choice.
model-generated proofs with genuine logical errors. Both

                                                                    5
                         Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                                                                                    (a) Llama-3.1-8B (HFER @ L30)                                   (b) Phi-3.5-mini (Smoothness @ L25)
4.3. Main Results
                                                                                                                   Valid
                                                                                                                                                                              d = 3.30
                                                                               8                                  Invalid                       6                        pM W < 10−65
Table 2 presents our main results. We highlight several key
                                                                               6




                                                                     Density




                                                                                                                                      Density
                                                                                                               d = −3.00                        4
findings:                                                                      4                            pM W < 10−63
                                                                                                                                                2
Universal Statistical Significance. All seven models                           2

achieve pMW < 10−47 and pt < 10−75 , providing                                 0
                                                                                    0        0.2           0.4      0.6
                                                                                                                                                0
                                                                                                                                                     −0.2    0   0.2 0.4         0.6   0.8
                                                                                                   Value                                                          Value
overwhelming evidence that the spectral signature is not
                                                                                   (c) Mistral-7B (Smoothness @ L26)                                 (d) Qwen2.5-0.5B (Entropy @ L0)
architecture-specific. The weakest result (Mistral-7B,
                                                                                                                                                2
pMW = 1.16 × 10−48 ) still represents extreme statistical                                d = 2.09
                                                                                    pM W < 10−47
                                                                                                                                                           d = 2.93
                                                                                                                                                      pM W < 10−64
                                                                               4                                                            1.5
significance by conventional standards.




                                                                     Density




                                                                                                                                Density
                                                                                                                                                1
                                                                               2
Large Effect Sizes. All seven models achieve Cohen’s                                                                                        0.5
d ≥ 2.09, substantially exceeding the conventional thresh-                     0                                                                0
                                                                                        0   0.2    0.4 0.6       0.8        1                            1       2           3         4
old of d = 0.8 for “large” effects. Four models achieve                                            Value                                                             Value
d ≥ 2.93: Llama-1B (d = 3.02), Llama-8B (d = 3.00),
                                                                   Figure 3. The “Shape of Truth” (Llama-3.1-8B). HFER density
Qwen-0.5B (d = 2.93), and Phi-3.5 (d = 3.30). Phi-3.5-             at Layer 30 shows near-complete separation between valid (blue)
mini achieves d = 3.30, indicating that valid and invalid          and invalid (red) proofs. Effect size d = 3.00, pMW = 9.40 ×
proof distributions are separated by more than three pooled        10−64 .
standard deviations. These effect sizes are 3–4× larger than
those typically reported in machine learning classification
tasks.                                                             over chance (Table 13).
High Classification Accuracy. Single-threshold classifiers         Threshold Robustness. Perturbing the optimal threshold by
achieve 85.9–94.9% accuracy across all models without any          ±10% changes accuracy by less than 2.5%; ±20% pertur-
training. The majority-class baseline accuracy is ∼57%             bation yields less than 5% accuracy degradation (Table 14).
(always predicting “invalid”), so our method provides a            The method is not sensitive to precise threshold selection.
29–38 percentage point improvement.
                                                                   Problem Difficulty. Stratifying by problem source reveals
Architecture-Specific Patterns. While the spectral signa-          that accuracy is highest on olympiad-level problems (100%
ture is universally present, its manifestation varies across       on IMO/Putnam, n = 12) and slightly lower on standard
architectures:                                                     competition problems (93% on AMC/AIME). The spectral
• Llama-1B: Fiedler value at L0 provides the strongest sig-        signature appears more pronounced for complex reasoning
  nal (d = 3.02), with HFER at L11 achieving the highest           (Table 15).
  accuracy (95.6%).                                                Proof Length. Accuracy is stable across proof length quin-
• Llama-3B/8B: HFER dominates, with optimal discrimi-              tiles (87–100%), confirming the method does not exploit
  nation at mid (L11) or late (L30) layers.                        length as a spurious proxy (Table 16).

• Qwen-0.5B: Uniquely, spectral entropy at L0 provides             Metric Independence. Correlation analysis reveals HFER
  the strongest signal (d = 2.93, pt = 1.43 × 10−116 ).            and entropy are nearly redundant (r = −0.97) on average,
                                                                   while the Fiedler value is largely independent (r = −0.29
• Phi: Late-layer smoothness (L25) shows the largest ef-           with HFER). However, layer-wise tracking reveals a critical
  fects (d = 3.30), with valid proofs maintaining positive         decoupling: at Layer 8 on Llama-3.1-8B, HFER achieves
  smoothness (0.438) while invalid proofs exhibit near-zero        Cohen’s d = 2.39 (95% CI: [1.99, 2.83]) while Spectral En-
  values (0.076).                                                  tropy collapses to d = 0.08 (95% CI: [0.00, 0.23]) — non-
• Mistral: Smoothness at L26 provides discrimination               overlapping CIs confirming HFER isolates graph-structural
  (d = 2.09), not HFER, a consequence of Sliding Win-              features independent of output statistics. On Mistral-7B
  dow Attention (see Section D.1).                                 (SWA), the HFER–entropy correlation drops from r ≈ 0.9
                                                                   (dense models) to r = 0.45, further confirming this struc-
                                                                   tural independence. See Table 17 for full correlation matrix.
4.4. Ablation Studies
                                                                   Cross-Model Transfer. Raw threshold transfer between
We conduct systematic ablations to verify robustness. Full
                                                                   models fails (accuracy drops to ∼50%) due to scale differ-
details are in Section C.
                                                                   ences in metric values. However, the phenomenon (direction
Random Baseline. The majority-class baseline achieves              of effect, discriminative layers) transfers universally. Cal-
∼57% accuracy. Our single-threshold spectral classifier            ibrating a threshold for a new model requires only ∼50
achieves up to 95.6%, a +39 percentage point improvement           labeled examples (Table 18).

                                                               6
                           Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

Table 2. Main results (corrected labels). Spectral signatures are universal across architectures (p < 10−47 , d up to 3.30). Gold row:
highest effect size. † Sliding Window Attention shifts the discriminative feature from HFER to Smoothness.

                       Model           Family       Best Metric        pMW               pt         |d|   Acc.
                                                                             −63              −92
                       Llama-3.2-1B Meta           Fiedler (L0) 1.47 × 10  1.83 × 10     3.02 93.4%
                       Llama-3.2-3B Meta           HFER (L11) 3.66 × 10−62 6.06 × 10−102 2.97 94.9%
                       Llama-3.1-8B Meta           HFER (L30) 9.40 × 10−64 5.44 × 10−105 3.00 94.1%
                       Qwen2.5-0.5B Alibaba        Entropy (L0) 4.45 × 10−65 1.43 × 10−116 2.93 93.2%
                       Qwen2.5-7B Alibaba          HFER (L26) 5.68 × 10−55 2.45 × 10−75 2.43 89.9%
                       Phi-3.5-mini    Microsoft Smooth (L25) 4.51 × 10−66 2.33 × 10−107 3.30 93.4%
                       Mistral-7B†     Mistral AI Smooth (L26) 1.16 × 10−48 1.21 × 10−78 2.09 85.9%


4.5. Generalization to Natural Language                               Table 4. Best-of-16 proof search reranker comparison (N =16,
                                                                      T =0.7; Llama-3.1-8B, MiniF2F). HFER surpasses log-probability
We evaluated Llama-3.2-1B on the MATH                                 on Pass@1 despite lower AUC, penalising confident hallucinations
dataset (Hendrycks et al., 2021) (N = 227 informal                    the ensemble confirms as orthogonally complementary.
Chain-of-Thought samples). The spectral signal attenuates
                                                                              Reranker                    Pass@1 AUC-ROC
from d = 3.02 (formal) to d = 0.78 (informal) but remains
significant (p < 10−3 ). Notably, the optimal metric shifts                   Random                      22.4%         –
                                                                              Token Entropy               30.4%       0.971
from HFER to the Fiedler value at Layer 14, suggesting                        Log-Prob                    29.8%       0.979
that natural language validity relies on global connectivity                  HFER (ours)                 34.2%       0.962
rather than spectral smoothness.                                              Ensemble (ZLP −ZHFER )      37.1%       0.988
On balanced data (N = 106), the training-free spectral
threshold achieves 68.4% accuracy, outperforming both ran-
dom guessing (+18.4%) and supervised classifiers (Table 3).
                                                                      the supervised hallucination probe of Obeso et al. (2026),
This “inverse overfitting” confirms that validity is captured
                                                                      trained on Llama-3.1-8B Layer 16 hidden states:
by a low-dimensional spectral feature requiring no learned
parameters.
                                                                      Table 5. Supervised vs. unsupervised. With only 50 calibration
Table 3. Informal Math (Llama-1B). Training-free spectral             examples, HFER achieves 98% of the fully supervised upper bound
threshold outperforms supervised Random Forest on balanced            (91.8%±2.4% accuracy).
data.
                                                                             Method                       Labels    AUC-ROC
            Method                 Full   Balanced
                                                                             Obeso et al. (2026) probe Millions        0.981
            Majority Class     76.6%       50.0%                             Linear Probe (ours)        363            0.949
            Random Forest      74.5%         –                               HFER calibrated (ours)      50            0.962
            Spectral Threshold 77.1%       68.4%                             HFER zero-shot (ours)        0            0.923


4.6. Downstream Utility and Supervised Baselines                      Difficulty Robustness. Stratifying MiniF2F proofs by Lean
Best-of-N Proof Search. We apply HFER as a zero-shot                  tactic count confirms the spectral signal persists across all
reranker in Best-of-N (N =16, T =0.7) proof search on                 complexity strata:
MiniF2F. Table 4 reports the full comparison across four
reranking strategies on Llama-3.1-8B:
                                                                      Table 6. Difficulty stratification (Llama-8B). d > 1.3 in every
The AUC–Pass@1 inversion arises because log-probability               stratum; all “large” by Cohen (1988) conventions.
is blind to confident hallucinations: structurally incoher-
ent proofs that are nonetheless fluent. HFER penalises ex-                         Stratum                 n      Cohen’s d
actly those cases. Cross-model replication confirms the gain                       Trivial (1 tactic)     107       6.69
scales with spectral separation: on Phi-3.5-mini (d=3.30),                         Simple (2–3 tactics)    69       3.29
HFER achieves 37.8% vs. log-probability’s 31.2% (+6.6%),                           Moderate (4–6 tactics) 72        2.09
                                                                                   Complex (≥7 tactics) 206         1.31
compared to +4.4% on Llama-3.1-8B (d=3.00).
Comparison to Supervised Probing. We compare against

                                                                  7
                                  Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                             Llama-3.1-8B Spectral Evolution                • Proof: norm num
                         Valid                                              • Compiler verdict: Invalid (timeout)
                        Invalid
              0.4                                                           • Spectral classification: Valid
       HFER




                                                                            • Mathematical reality: The proof is correct.
              0.2
                                                                            We systematically examined all such disagreements across
                                                                            models. All seven models independently identified 33–
               0
                                                                            51 compiler-rejected proofs as spectrally valid (see Ta-
                    0        5     10     15      20     25    30
                                         Layer                              ble 23). Cross-referencing these sets revealed substantial
                                                                            overlap: proofs consistently identified as “spectrally valid
Figure 4. Spectral Evolution. HFER divergence emerges in mid-               but compiler-rejected” across architectures were overwhelm-
to-late layers: valid proofs (blue) stay smooth; invalid proofs (red)
                                                                            ingly mathematically correct.
disintegrate.
                                                                            This motivates a distinction between two notions of validity:

5. Analysis                                                                 • Compiler Validity: Did Lean accept the proof? (Suscep-
                                                                              tible to timeouts, missing imports, version mismatches.)
5.1. The Spectral Signature of Valid Reasoning
                                                                            • Platonic Validity: Is the reasoning logically coherent?
Across all seven models, valid proofs exhibit a consistent                    (Independent of compiler idiosyncrasies.)
spectral signature characterized by:
                                                                            The spectral signature appears to track “Platonic validity”,
1. Lower HFER: Valid proofs concentrate signal en-                          the underlying logical coherence of the reasoning process,
   ergy in low-frequency (smooth) spectral modes, indi-                     rather than the accident of compiler acceptance. We there-
   cating coherent information integration across attention-                fore report all main results using corrected labels that reflect
   connected tokens.                                                        logical validity rather than compiler output.
2. Higher Entropy: Valid proofs distribute attention more                   Failure-reason audit. A manual audit of 51 reclaimed
   uniformly, engaging diverse token relationships rather                   proofs across all seven models (two independent raters,
   than collapsing to stereotyped patterns.                                 Cohen’s κ = 0.82) reveals that 64.8% fail Lean only on
3. Higher Smoothness: Valid proofs maintain positive                        technical grounds:
   smoothness throughout processing; invalid proofs often
   exhibit negative smoothness in late layers (particularly                 Table 7. Reclaimed proof failure reasons. 64.8% of proofs
                                                                            (valid + environment rows) are logically structured but rejected on
   in Phi).                                                                 technical grounds.
4. Higher Fiedler Value: Valid proofs induce better-
   connected attention graphs, enabling more efficient                             Failure Category                                %
   global information flow.                                                        Semantically valid (minor structural issues)   37.3
                                                                                   Environment / missing imports                  27.5
The direction of these effects is consistent across all ar-                        Timeout / computational limit                  13.7
chitectures; only the magnitude and optimal metric vary.                           Incomplete (model admits failure)              13.7
This consistency provides strong evidence for a universal                          Syntax / version issues                         7.8
geometric property of transformer attention during valid
reasoning.
                                                                            5.3. Architectural and Computational Variations
5.2. Platonic Validity                                                      Sliding Window Attention. Mistral-7B, the only model
                                                                            using Sliding Window Attention (SWA), exhibits a shifted
A surprising discovery emerged from analyzing classifica-
                                                                            spectral signature: validity is best captured by late-layer
tion disagreements. When the spectral method classified a
                                                                            Smoothness (d = 2.09) rather than HFER. We hypothesize
proof as valid but the ground truth label indicated invalidity,
                                                                            that SWA’s local attention windows redistribute validity in-
manual inspection revealed that the spectral method was
                                                                            formation from global frequency content to local coherence
frequently correct: these proofs were mathematically sound
                                                                            properties. This finding implies that architecture-aware met-
but rejected by Lean due to technical failures.
                                                                            ric selection is necessary. Hence, practitioners should not
Example 5.1 (Platonic vs. Compiler Validity). Consider                      assume HFER is universally optimal (see Section D.1 for
mathd numbertheory 961:                                                     full analysis).
• Theorem: 2003 mod 11 = 1                                                  Mixture-of-Experts. Evaluating Qwen-MoE reveals a

                                                                        8
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

“sparsity penalty”: effect sizes attenuate from d ≈ 3.0              acceptance (“Platonic validity”); (5) HFER reranking im-
(dense) to d ≈ 1.6 (sparse) on balanced data, though the sig-        proves Best-of-16 Pass@1 by +4.4–6.6%, achieving 98%
nal remains significant (p < 10−10 ). The dominant metric            of fully supervised AUC with zero labels; and (6) Lanc-
shifts to Spectral Entropy, suggesting that valid reasoning          zos acceleration reduces eigendecomposition to O(kN 2 ),
corresponds to focused expert routing while hallucinations           enabling real-time use at 32k-token contexts.
manifest as routing diffusion (details in Section D.2).
                                                                     These findings open several directions for future work: theo-
Cognitive Interpretation. The asymmetry between error                retical analysis of why the spectral signature emerges, exten-
types suggests the spectral signature reflects the model’s           sion to natural language reasoning, integration with proof
epistemic state: invalid proofs with low spectral energy             assistants for real-time feedback, and investigation of other
represent “confident wrongness” (analogous to Dunning-               architectural features (grouped-query attention, mixture-of-
Kruger), while valid proofs with high energy indicate gen-           experts) that may affect spectral properties.
uine cognitive effort. This interpretation suggests applica-
                                                                     More broadly, our work demonstrates that interpretability
tions to difficulty estimation and overconfidence detection
                                                                     methods grounded in classical mathematical frameworks,
(Section D.3).
                                                                     here, spectral graph theory, can yield practical tools for
                                                                     understanding and verifying neural network reasoning. As
6. Discussion                                                        language models are deployed in increasingly high-stakes
                                                                     reasoning applications, such principled verification methods
A Geometric Principle. Our findings establish that valid
                                                                     become essential for ensuring reliability and safety.
mathematical reasoning induces a coherent, low-frequency
“spectral signature” in transformer attention. This phe-
nomenon appears universal across architectures (p <                  8. Limitations
10−47 ). Together, these results suggest a general topologi-
                                                                     Scope. Validation is scoped to formalized Lean 4 reasoning
cal law: valid generation necessitates a connected attention
                                                                     on MiniF2F. Informal chain-of-thought yields a substantially
graph, while logical anomalies manifest as measurable spec-
                                                                     weaker signal (d=0.78 vs. d>1.3), and claims do not extend
tral discontinuities.
                                                                     to unstructured text.
Topological Divergence Across Modalities. We attribute
                                                                     Model-specific calibration. Optimal thresholds are
the shift in dominant metrics, from HFER in formal code
                                                                     architecture-specific; Sliding Window Attention shifts the
to the Fiedler value in natural language, to the distinct
                                                                     dominant feature from HFER to smoothness, requiring per-
topology of domain-specific errors. In rigid formal sys-
                                                                     model tuning.
tems (MiniF2F), invalid steps often introduce local syntactic
violations, creating high-frequency artifacts (“roughness”)          Diagnostic, not causal. The method is a correlation-based
best captured by HFER. Conversely, informal hallucinations           diagnostic. A mechanistic account of why the signature
(MATH) often maintain grammatical smoothness while los-              emerges and how to exploit it for targeted reasoning im-
ing logical grounding; this manifests as a global fracture in        provement remains future work.
the attention graph, which is detected by the Fiedler value’s
                                                                     Computational cost. Full eigendecomposition is O(N 3 ).
sensitivity to algebraic connectivity.
                                                                     Lanczos reduces this to O(kN 2 ), but real-time deployment
Applications. This framework enables training-free appli-            at 32k-token contexts may require further engineering.
cations ranging from runtime hallucination monitoring to
spectral-guided proof search (Section 4.6). A full discussion        Impact Statement
of limitations appears in Section 8.
                                                                     This work introduces a training-free method for detecting
7. Conclusion                                                        valid mathematical reasoning in transformer models. The
                                                                     primary intended application is improving reliability in auto-
We have introduced a training-free method for detecting              mated theorem proving, mathematical education, and scien-
valid mathematical reasoning through spectral analysis of            tific discovery pipelines, where undetected reasoning errors
transformer attention. Our experiments across seven mod-             can propagate consequentially. By operating without la-
els from four architectural families establish that: (1) the         beled data or learned parameters, the method lowers the
spectral signature is universal (pMW < 10−47 , pt < 10−75 )          barrier to deployment in resource-constrained settings. We
and robust across all difficulty strata (d ≥ 1.31); (2) effect       foresee no direct negative societal impacts; however, as with
sizes are exceptionally large (up to d = 3.30); (3) single-          any verification tool, over-reliance without understanding
threshold classification achieves 85.9–95.6% accuracy; (4)           its failure modes, particularly its attenuation on informal
the method detects logical coherence rather than compiler            text, could create misplaced confidence in model outputs.


                                                                 9
                         Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

References                                                          Chou, C.-N., Arend, L., Wakhloo, A. J., Kim, R., Slatton,
                                                                      W., and Chung, S. Neural manifold capacity captures
Azaria, A. and Mitchell, T. The internal state of an LLM
                                                                      representation geometry, correlations, and task-efficiency
  knows when it’s lying. arXiv preprint arXiv:2304.13734,
                                                                      across species and behaviors. bioRxiv, 2024.
  2023.
Azerbayev, Z., Schoelkopf, H., Paster, K., Santos, M. D.,           Chou, C.-N., Le, H., Wang, Y., and Chung, S. Feature
  McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and              learning beyond the lazy-rich dichotomy: Insights from
 Welleck, S. Llemma: An open language model for math-                 representational geometry. In ICML, 2025. Spotlight.
  ematics. arXiv preprint arXiv:2310.10631, 2023.                   Chung, F. R. Spectral graph theory, volume 92. American
Belinkov, Y. Probing classifiers: Promises, shortcomings,             Mathematical Soc., 1997.
  and advances. Computational Linguistics, 48(1):207–219,
                                                                    Chung, S., Lee, D. D., and Sompolinsky, H. Classification
  2022.
                                                                      and geometry of general perceptual manifolds. Physical
Beltagy, I., Peters, M. E., and Cohan, A.        Long-                Review X, 8(3):031003, 2018.
  former: The long-document transformer. arXiv preprint
  arXiv:2004.05150, 2020.                                           Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
                                                                      Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
Bertot, Y. and Castéran, P. Interactive theorem proving              R., et al. Training verifiers to solve math word problems.
  and program development: Coq’Art: The calculus of                   arXiv preprint arXiv:2110.14168, 2021.
  inductive constructions. Springer Science & Business
  Media, 2013.                                                      Cohen, J. Statistical Power Analysis for the Behavioral
                                                                      Sciences. Lawrence Erlbaum Associates, 2nd edition,
Bhatnagar, R., Sun, Y., Zhang, C. A., Wen, Y., and Yang, H.          1988.
  Halt: Hallucination assessment via latent testing. arXiv
  preprint arXiv:2601.14210, 2026.                                  Cohen, U., Chung, S., Lee, D. D., and Sompolinsky, H.
                                                                      Separability and geometry of object manifolds in deep
Bo, D., Shi, C., Wang, L., and Liao, R. Specformer: Spec-             neural networks. Nature Communications, 11(1):746,
  tral graph neural networks meet transformers. In Interna-           2020.
  tional Conference on Learning Representations, 2023.
                                                                    de Moura, L. and Ullrich, S. The Lean 4 theorem prover
Bruna, J., Zaremba, W., Szlam, A., and LeCun, Y. Spectral             and programming language. In International Conference
  networks and deep locally connected networks on graphs.             on Automated Deduction, pp. 625–635. Springer, 2021.
  arXiv preprint arXiv:1312.6203, 2013.
                                                                    Defferrard, M., Bresson, X., and Vandergheynst, P. Con-
Burns, C., Ye, H., Klein, D., and Steinhardt, J. Discovering
                                                                      volutional neural networks on graphs with fast localized
  latent knowledge in language models without supervision.
                                                                      spectral filtering. In Advances in Neural Information
  arXiv preprint arXiv:2212.03827, 2023.
                                                                      Processing Systems, volume 29, pp. 3844–3852, 2016.
Canatar, A., Feather, J., Wakhloo, A., and Chung, S. A
  spectral theory of neural prediction and alignment. In            Draye, F., Lei, A., Posner, I., and Schölkopf, B. Sparse
  NeurIPS, 2023. Spotlight.                                           attention post-training for mechanistic interpretability.
                                                                      arXiv preprint arXiv:2512.05865, 2025.
Chen, C., Liu, K., Chen, Z., Gu, Y., Wu, Y., Tao, M., Fu,
  Z., and Ye, J. Inside: Llms’ internal states retain the           Dziri, N., Lu, X., Sclar, M., Li, X. L., Jiang, L., Lin, B. Y.,
  power of hallucination detection. ArXiv, abs/2402.03744,           Welleck, S., West, P., Bhagavatula, C., Bras, R. L., et al.
  2024. URL https://api.semanticscholar.                              Faith and fate: Limits of transformers on compositionality.
  org/CorpusID:267499843.                                            Advances in Neural Information Processing Systems, 36,
                                                                      2024.
Chervonyi, Y., Trinh, T. H., Olšák, M., Yang, X., Nguyen,
  H., Menegali, M., Jung, J., Kim, J., Verma, V., Le,               El, B., Choudhury, D., Liò, P., and Joshi, C. K. Towards
  Q. V., and Luong, T. Gold-medalist performance in solv-             mechanistic interpretability of graph transformers via
  ing olympiad geometry with AlphaGeometry2. arXiv                    attention graphs. arXiv preprint arXiv:2502.12352, 2025.
  preprint arXiv:2502.03544, 2025.
                                                                    Elhage, N., Nanda, N., Olsson, C., Henighan, T., Joseph,
Child, R., Gray, S., Radford, A., and Sutskever, I. Gener-            N., Mann, B., Askell, A., Bai, Y., Chen, A., Conerly, T.,
  ating long sequences with sparse transformers. In arXiv             et al. A mathematical framework for transformer circuits.
  preprint arXiv:1904.10509, 2019.                                    Transformer Circuits Thread, 1(1):12, 2021.

                                                               10
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

Ettinger, A. What BERT is not: Lessons from a new suite of            Kreuzer, D., Beaini, D., Hamilton, W. L., Létourneau, V.,
  psycholinguistic diagnostics for language models. Trans-              and Tossou, P. Rethinking graph transformers with spec-
  actions of the Association for Computational Linguistics,             tral attention. In Advances in Neural Information Pro-
  8:34–48, 2020.                                                        cessing Systems, volume 34, pp. 21618–21629, 2021.

Fiedler, M. Algebraic connectivity of graphs. Czechoslovak            Kuang, J., Huang, H., Li, Y., Liang, X., Xu, Z., Li, Y., Tan,
  Mathematical Journal, 23(2):298–305, 1973.                            X., Qu, C., Zhang, M., Shen, Y., et al. Atomic thinking of
                                                                        llms: Decoupling and exploring mathematical reasoning
Geva, M., Bastings, J., Filippova, K., and Globerson, A. Dis-
                                                                        abilities. arXiv preprint arXiv:2509.25725, 2025.
  secting recall of factual associations in auto-regressive
  language models. arXiv preprint arXiv:2304.14767,                   Kuhn, L., Gal, Y., and Farquhar, S. Semantic uncer-
  2023.                                                                 tainty: Linguistic invariances for uncertainty estima-
Glazer, E., Erdil, E., Besiroglu, T., Chicharro, D., Chen, E.,          tion in natural language generation. arXiv preprint
  Gunning, A., Olsson, C. F., Denain, J.-S., Ho, A., Santos,            arXiv:2302.09664, 2023.
  E. d. O., et al. Frontiermath: A benchmark for evaluating
                                                                      Lewkowycz, A., Andreassen, A., Dohan, D., Dyer, E.,
  advanced mathematical reasoning in ai. arXiv preprint
                                                                        Michalewski, H., Ramasesh, V., Slone, A., Anil, C.,
  arXiv:2411.04872, 2024.
                                                                        Schlag, I., Gutman-Solo, T., et al. Solving quantitative
Hanna, M., Liu, O., and Variengien, A. How does GPT-2                   reasoning problems with language models. Advances in
  compute greater-than? interpreting mathematical abil-                 Neural Information Processing Systems, 35:3843–3857,
  ities in a pre-trained language model. arXiv preprint                 2022.
  arXiv:2305.00586, 2023.
                                                                      Li, B. Z., Nye, M., and Andreas, J. Implicit representations
Healy, K., Srinivasan, B., Madathil, V., and Wu, J. Internal            of meaning in neural language models. Proceedings of
  representations as indicators of hallucinations in agent              ACL, 2021.
  tool selection, 2026. URL https://arxiv.org/
  abs/2601.05214.                                                     Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
                                                                        B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
Hendrycks, D., Burns, C., Kadavath, S., Arber, A., Basart,              Cobbe, K. Let’s verify step by step. arXiv preprint
  S., Tang, E., Song, D., and Steinhardt, J. Measuring                  arXiv:2305.20050, 2023.
  mathematical problem solving with the MATH dataset.
  arXiv preprint arXiv:2103.03874, 2021.                              Liu, Z., Kitouni, O., Nolte, N. S., Michaud, E., Tegmark,
                                                                        M., and Williams, M. Towards understanding grokking:
Hewitt, J. and Liang, P. Designing and interpreting probes              An effective theory of representation learning. Advances
  with control tasks. In Proceedings of the 2019 Conference             in Neural Information Processing Systems, 35:34651–
  on Empirical Methods in Natural Language Processing,                  34663, 2022.
  pp. 2733–2743, 2019.
                                                                      Marks, S. and Tegmark, M. The geometry of truth:
Hewitt, J. and Manning, C. D. A structural probe for find-
                                                                       Emergent linear structure in large language model
  ing syntax in word representations. In Proceedings of
                                                                       representations of true/false datasets. arXiv preprint
  the 2019 Conference of the North American Chapter of
                                                                       arXiv:2310.06824, 2024.
  the Association for Computational Linguistics, pp. 4129–
  4138, 2019.                                                         Meng, K., Bau, D., Andonian, A., and Belinkov, Y. Locating
Kadavath, S., Conerly, T., Askell, A., Henighan, T., Drain,            and editing factual associations in GPT. In Advances in
  D., Perez, E., Schiefer, N., Hatfield-Dodds, Z., DasSarma,           Neural Information Processing Systems, volume 35, pp.
  N., Tran-Johnson, E., et al. Language models (mostly)                17359–17372, 2022.
  know what they know. arXiv preprint arXiv:2207.05221,
                                                                      Nanda, N., Chan, L., Liberum, T., Smith, J., and Stein-
  2022.
                                                                        hardt, J. Progress measures for grokking via mechanistic
Kadem, M. and Zheng, R. Interpreting transformers                       interpretability. arXiv preprint arXiv:2301.05217, 2023.
  through attention head intervention. arXiv preprint
  arXiv:2601.04398, 2026.                                             Obeso, A., Balcells, O., et al. Hallucination probes:
                                                                        Lightweight supervised detectors for LLM internal
Kipf, T. N. and Welling, M. Semi-supervised classifica-                 states.    https://github.com/obalcells/
  tion with graph convolutional networks. In International              hallucination_probes, 2026.                GitHub:
  Conference on Learning Representations, 2017.                         obalcells/hallucination probes.

                                                                 11
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

Olsson, C., Elhage, N., Nanda, N., Joseph, N., DasSarma,                  to networks and other irregular domains. IEEE Signal
  N., Henighan, T., Mann, B., Askell, A., Bai, Y., Chen,                  Processing Magazine, 30(3):83–98, 2013.
  A., et al. In-context learning and induction heads. Trans-
  former Circuits Thread, 2022.                                         Stolfo, A., Belinkov, Y., and Sachan, M. A mechanis-
                                                                          tic interpretation of arithmetic reasoning in language
Ortega, A., Frossard, P., Kovačević, J., Moura, J. M. F., and           models using causal mediation analysis. arXiv preprint
  Vandergheynst, P. Graph signal processing: Overview,                    arXiv:2305.15054, 2023.
  challenges, and applications. Proceedings of the IEEE,
  106(5):808–828, 2018.                                                 Tenney, I., Das, D., and Pavlick, E. BERT rediscovers the
                                                                          classical NLP pipeline. arXiv preprint arXiv:1905.05950,
Ospanov, A., Farnia, F., and Yousefzadeh, R. Apollo: Au-                  2019.
  tomated llm and lean collaboration for advanced formal
  reasoning. arXiv preprint arXiv:2505.05758, 2025.                     Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T. Solv-
                                                                          ing olympiad geometry without human demonstrations.
Paulson, L. C. Isabelle: A generic theorem prover. Springer,              Nature, 625(7995):476–482, 2024.
  1994.
                                                                        Uesato, J., Kushman, N., Kumar, R., Song, F., Siegel, N.,
Petroni, F., Rocktäschel, T., Riedel, S., Lewis, P., Bakhtin,           Wang, L., Creswell, A., Irving, G., and Higgins, I. Solv-
  A., Wu, Y., and Miller, A. Language models as knowledge                 ing math word problems with process- and outcome-
  bases? In Proceedings of EMNLP, pp. 2463–2473, 2019.                    based feedback. arXiv preprint arXiv:2211.14275, 2022.

Petrov, I., Dekoninck, J., Baltadzhiev, L., Drencheva, M.,              Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and
  Minchev, K., Balunović, M., Jovanović, N., and Vechev,                Ye, K. Hilbert: Recursively building formal proofs with
  M. Proof or bluff? evaluating llms on 2025 usa math                     informal reasoning. arXiv preprint arXiv:2509.22819,
  olympiad. arXiv preprint arXiv:2503.21934, 2025.                        2025.

Polu, S. and Sutskever, I. Generative language model-                   Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang,
  ing for automated theorem proving. arXiv preprint                      S., Chowdhery, A., and Zhou, D. Self-consistency im-
  arXiv:2009.03393, 2020.                                                proves chain of thought reasoning in language models.
                                                                         arXiv preprint arXiv:2203.11171, 2023.
Rai, D., Zhou, Y., Feng, S., Saparov, A., and Yao, Z.
  A practical review of mechanistic interpretability for                Welleck, S., Liu, J., Lu, X., Hajishirzi, H., and Choi, Y.
  transformer-based language models. arXiv preprint                      NaturalProver: Grounded mathematical proof generation
  arXiv:2407.02646, 2024.                                                with language models. Advances in Neural Information
                                                                         Processing Systems, 35:4913–4927, 2022.
Romera-Paredes, B., Barekatain, M., Novikov, A., Balog,
  M., Kumar, M. P., Dupont, E., Ruiz, F. J. R., Ellenberg,              Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  J. S., Wang, P., Fawzi, O., et al. Mathematical discoveries             P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
  from program search with large language models. Nature,                 LeanDojo: Theorem proving with retrieval-augmented
  625(7995):468–475, 2024.                                                language models. Advances in Neural Information Pro-
                                                                          cessing Systems, 36, 2024.
Rusch, T. K., Bronstein, M. M., and Mishra, S. A survey on
  oversmoothing in graph neural networks. arXiv preprint                Zhang, F., Yu, P., Yi, B., Zhang, B., Li, T., and Liu, Z.
  arXiv:2303.10993, 2023.                                                 Prompt-guided internal states for hallucination detection
                                                                          of large language models. In Proceedings of the 63rd
Saparov, A., Saparov, R., He, Z., Xia, J., Raffel, C., Khot, T.,          Annual Meeting of the Association for Computational
  et al. Testing the general deductive reasoning capacity of              Linguistics (Volume 1: Long Papers), pp. 21806–21818,
  large language models using OOD examples. In Advances                   2025a.
  in Neural Information Processing Systems, 2023.
                                                                        Zhang, J., Petrui, C., Nikolić, K., and Tramèr, F. Real-
Shi, H., Gao, J., Xu, H., Liang, X., Li, Z., Kong, L.,                    math: A continuous benchmark for evaluating language
  Lee, S., and Kwok, J. Revisiting over-smoothing in                      models on research-level mathematics. arXiv preprint
  BERT from the perspective of graph. arXiv preprint                      arXiv:2505.12575, 2025b.
  arXiv:2202.08625, 2022.
                                                                        Zhang, L., Song, D., Wu, Z., Tian, Y., Zhou, C., Xu, J., Yang,
Shuman, D. I., Narang, S. K., Frossard, P., Ortega, A., and               Z., and Zhang, S. Detecting hallucination in large lan-
  Vandergheynst, P. The emerging field of signal processing               guage models through deep internal representation anal-
  on graphs: Extending high-dimensional data analysis                     ysis. In Proceedings of the Thirty-Fourth International

                                                                   12
                        Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

  Joint Conference on Artificial Intelligence, IJCAI-25, pp.
  8357–8365, 2025c.
Zheng, K., Han, J. M., and Polu, S. MiniF2F: A cross-
  system benchmark for formal olympiad-level mathemat-
  ics. arXiv preprint arXiv:2109.00110, 2022.




                                                               13
                            Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

A. Theoretical Background
This appendix provides mathematical background on spectral graph theory and its application to our framework.

A.1. Graph Laplacians
Definition A.1 (Combinatorial Laplacian). For an undirected weighted graph G = (V, E, W ) with N vertices and symmetric
                       ×N
weight matrix W ∈ RN ≥0   , the combinatorial graph Laplacian is:

                                                          L=D−W                                                       (11)
                                             PN
where D = diag(d1 , . . . , dN ) with di =     j=1 Wij is the degree matrix.
Definition A.2 (Normalized Laplacians). Two normalized variants are commonly used:

                                       Lsym = D −1/2 LD −1/2 = I − D −1/2 W D −1/2                                    (12)
                                                  −1             −1
                                        Lrw = D        L=I −D           W                                             (13)

The symmetric normalized Laplacian Lsym has eigenvalues in [0, 2] for connected graphs; the random walk Laplacian Lrw
relates to diffusion processes on graphs.
Proposition A.3 (Laplacian Properties). The combinatorial Laplacian L satisfies:

 (i) L is symmetric positive semidefinite.

 (ii) L1 = 0, so λ1 = 0 with eigenvector 1.

(iii) For any x ∈ RN : x⊤ Lx = 21 i,j Wij (xi − xj )2 ≥ 0.
                                  P

(iv) The multiplicity of eigenvalue 0 equals the number of connected components.

 (v) Eigenvalues satisfy 0 = λ1 ≤ λ2 ≤ · · · ≤ λN ≤ 2dmax .

Proof. (i) Symmetry follows from W = W ⊤ and D diagonal. Positive semidefiniteness follows from (iii).
                     P
(ii) (L1)i = di · 1 − j Wij · 1 = di − di = 0.
(iii) Direct computation:
                                                                 X                 X
                               x⊤ Lx = x⊤ Dx − x⊤ W x =                 di x2i −         Wij xi xj                    (14)
                                                                    i              i,j
                                                                                 
                                        1  X             X               X
                                       =     di x2i − 2     Wij xi xj +   dj x2j                                    (15)
                                        2   i            i,j             j

                                           1X                                1X
                                       =         Wij (x2i − 2xi xj + x2j ) =       Wij (xi − xj )2                    (16)
                                           2 i,j                             2 i,j


(iv) If G has k connected components, we can construct k linearly independent vectors constant on each component, all in
the null space of L.
                                                                                                               S
(v)
P The lower bound    P follows from  S (i). For the upper bound, using Gershgorin’s theorem: eigenvalues lie in i [di −
   j̸=i |Lij |, di +  j̸=i |Lij |] =  i [0, 2di ] ⊆ [0, 2dmax ].


A.2. Algebraic Connectivity
Definition A.4 (Fiedler Value and Vector). The algebraic connectivity or Fiedler value of a connected graph is λ2 (L), the
second-smallest Laplacian eigenvalue. The corresponding eigenvector is the Fiedler vector.
Theorem A.5 (Fiedler, 1973). For a connected graph G:

                                                               14
                         Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

 (i) λ2 > 0 if and only if G is connected.

(ii) λ2 ≤ κ(G) where κ(G) is the vertex connectivity.
(iii) The Fiedler vector provides a graph embedding useful for partitioning.
Theorem A.6 (Cheeger Inequality). The Fiedler value relates to the Cheeger constant (isoperimetric number) h(G):

                                                λ2          p
                                                   ≤ h(G) ≤ 2λ2                                                       (17)
                                                2
                               |∂S|                 P
where h(G) = minS⊂V,|S|≤N/2 min(|S|,|S̄|)
                                          and |∂S| = i∈S,j ∈S
                                                           / Wij .

The Cheeger inequality establishes that λ2 characterizes the “bottleneck” of information flow in the graph: high λ2 implies
no sparse cuts, enabling efficient global communication.

A.3. Graph Signal Processing
Definition A.7 (Graph Signal). A graph signal is a function f : V → R assigning a real value to each vertex, representable
as a vector f ∈ RN .
Definition A.8 (Graph Fourier Transform). The Graph Fourier Transform (GFT) of a signal f with respect to Laplacian
L = U ΛU ⊤ is:
                                                   fˆ = U ⊤ f                                                  (18)
The component fˆk = u⊤
                     k f represents the signal’s content at graph frequency λk .
Proposition A.9 (Frequency Interpretation). The Laplacian eigenvectors provide a notion of frequency on graphs:
            √
 (i) u1 = 1/ N is the “DC component” (constant signal).
(ii) Eigenvectors uk with small λk vary slowly across edges.
(iii) Eigenvectors with large λk vary rapidly, changing sign frequently.
(iv) f ⊤ Lf = k λk fˆk2 : the Dirichlet energy is a weighted sum of squared spectral coefficients, with high-frequency
                P
      components penalized more.

B. Implementation Details
B.1. Attention Extraction
We extract attention matrices using standard hooks into the transformer forward pass. For each model:

• Llama: We access model.layers[l].self attn.attn weights post-softmax.
• Qwen: Similar structure via model.layers[l].attn.attention weights.
• Phi: Via model.layers[l].mixer.attention weights.
• Mistral: Via model.layers[l].self attn.attn weights. Note that SWA produces sparse attention matrices
  with non-zero entries only within the sliding window.

All models use output attentions=True during forward passes.




                                                            15
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

B.2. Spectral Computation

Algorithm 1 Spectral Diagnostic Extraction
Require: Attention matrices {A(ℓ,h) }ℓ,h , hidden states {X (ℓ) }ℓ
                                 (ℓ)
Ensure: Spectral diagnostics {λ2 , HFER(ℓ) , E (ℓ) , SE(ℓ) }ℓ
 1: for layer ℓ = 1 to L do
 2:   // Symmetrize and aggregate attention
 3:   for head h = 1 to H do
 4:      W (ℓ,h) ← 12 (A(ℓ,h) + (A(ℓ,h) )⊤ )
                P        (ℓ,h)
 5:      sh ← i,j Aij
 6:   end for P
 7:   αh ← sh / g sg for all h
      W̄ (ℓ) ← h αh W (ℓ,h)
                 P
 8:
 9:   // Compute Laplacian
10:   D̄ (ℓ) ← diag(W̄ (ℓ) 1)
11:   L(ℓ) ← D̄ (ℓ) − W̄ (ℓ)
12:   // Eigendecomposition
13:   Λ(ℓ) , U (ℓ) ← eig(L(ℓ) ) {Sorted by eigenvalue}
14:   // Extract diagnostics
        (ℓ)      (ℓ)
15:   λ2 ← Λ2,2
16:   X̂ (ℓ) ← (U (ℓ) )⊤ X (ℓ)
                   (ℓ)
17:   em ← ∥X̂m,· ∥22 for m = 1, . . . , N
      HFER(ℓ) ← m>N/2 em / m em
                       P            P
18:
19:   E (ℓ) ← Tr((X (ℓ) )⊤ L(ℓ) X (ℓ) )
      pm ← em / r er ; SE(ℓ) ← − m pm log pm
                    P                   P
20:
21: end for


B.3. Computational Complexity

                              Operation                                           Complexity
                              Symmetrization (per head)                             O(N 2 )
                              Aggregation (all heads)                              O(HN 2 )
                              Laplacian construction                                O(N 2 )
                              Full eigendecomposition                               O(N 3 )
                              Randomized SVD (k eigenvalues, Lanczos)              O(kN 2 )
                              Graph Fourier Transform                              O(N 2 d)
                              Diagnostic computation                                O(N d)
                              Total (per layer, full)                          O(N 3 + N 2 d)
                              Total (per layer, Lanczos k=50)                  O(kN 2 + N 2 d)
Table 8. Computational complexity of spectral analysis. For typical proof lengths (N < 1000), the full method adds <5% inference
overhead. Randomized SVD scales to long contexts.


Randomized SVD for Long Contexts. To address scalability beyond O(N 3 ), we implement Lanczos iteration with k=50
extreme singular values on A⊤ A. This reduces asymptotic complexity to O(kN 2 ) and yields wall-clock speedups of up to
61× while preserving exact topological metrics:




                                                              16
                         Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                                   Seq. Length        Full eigh        Lanczos (k=50)       Speedup
                                   1,000               264 ms             60 ms              4.4×
                                   10,000               47.3 s            773 ms             61×
                                   32,000 (extrap.)   ∼5.1 min             ∼5 s              61×
         Table 9. Wall-clock comparison on an A100 GPU. Lanczos (k=50) scales to 32k-token contexts at inference speed.



B.4. Hardware and Runtime
• Hardware: NVIDIA A100 (40GB)
• Inference time per proof: 1.5–3.0 seconds (depending on model size and proof length)
• Spectral computation overhead: 50–200ms per proof
• Total runtime for 454 proofs: 12–20 minutes per model

C. Ablation Study Details
C.1. Human Perturbation Control (Control 2)

                                  Metric      Layer    Valid      Pert.            p             d
                                                                                       −6
                                  Fiedler     6        0.455      0.433     4.2 × 10           0.90
                                  Fiedler     Last     0.547      0.530     1.0 × 10−5         0.90
                                  HFER        6        0.099      0.121     2.1 × 10−7        −1.06
                                  HFER        Last     0.331      0.378     1.9 × 10−9        −1.10
                                  Smooth      6        0.970      0.986     1.2 × 10−10       −1.17
                                  Smooth      Last     0.646      0.627     1.4 × 10−8         1.12
                                  Entropy     6        1.999      1.800     1.9 × 10−8         1.13
                                  Entropy     Last     3.012      2.790     1.2 × 10−8         1.09
Table 10. Control 2: Human perturbations (Llama-3.2-1B). All metrics show significant degradation when logic is corrupted while
style is held fixed (n = 154 valid, n = 40 perturbed).



C.2. Train/Val/Test Split

                                    Model              Test Acc          Val Acc       Threshold
                                    Llama-3.2-1B         78.0%            80.2%          0.050
                                    Llama-3.2-3B         83.5%            86.8%          0.126
                                    Llama-3.1-8B         82.4%            86.8%          0.100
                                    Mistral-7B           73.6%            80.2%          0.120
                                    Phi-3.5-mini         75.8%            84.6%          0.067
                                    Qwen2.5-0.5B         83.5%            84.6%          0.115
                                    Qwen2.5-7B           80.2%            85.7%          0.071
                  Table 11. Held-out test accuracy (60/20/20 split). Test accuracies range from 73.6% to 83.5%.




                                                                  17
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

C.3. Nested Cross-Validation

                                   Model              Nested CV Acc            Best Config
                                   Llama-3.2-1B        83.9% ± 1.8%           hfer@L15
                                   Llama-3.2-3B        82.8% ± 1.7%           hfer@L25
                                   Llama-3.1-8B        85.9% ± 1.3%           hfer@L20
                                   Mistral-7B          83.9% ± 1.7%           hfer@L30
                                   Phi-3.5-mini        84.8% ± 1.3%        smoothness@L25
                                   Qwen2.5-0.5B        83.5% ± 1.5%           hfer@L15
                                   Qwen2.5-7B          85.0% ± 0.6%           hfer@L25
             Table 12. Nested CV accuracy (5-fold outer, 4-fold inner). Accuracies are 82.8–85.9% across all models.



C.4. Random Baseline

                              Method                                 Accuracy      ∆ vs. Majority
                              Majority class (always “invalid”)        57.0%               -
                              Random guessing                          50.0%            −7.0%
                              Spectral (single threshold, best)        95.6%            +38.6%
                              Spectral (two-feature rule, best)        95.6%            +38.6%
     Table 13. Comparison to baselines (corrected labels). The spectral method achieves +39% over the majority-class baseline.



C.5. Threshold Robustness

                                    Threshold (relative)       Accuracy      ∆ vs. Optimal
                                           0.80×                 89.6%            −4.5%
                                           0.85×                 91.4%            −2.7%
                                           0.90×                 93.0%            −1.1%
                                           0.95×                 93.8%            −0.3%
                                       1.00× (optimal)           94.1%              -
                                           1.05×                 93.6%            −0.5%
                                           1.10×                 92.9%            −1.2%
                                           1.15×                 91.8%            −2.3%
                                           1.20×                 90.3%            −3.8%
     Table 14. Threshold robustness (HFER @ L30, Llama-8B, corrected labels). Within ±10%, accuracy degrades by <1.5%.




                                                                18
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

C.6. Problem Difficulty

                             Source                             n     Accuracy           95% CI
                             Olympiad (IMO/Putnam)              12      100.0%       [73.5%, 100%]
                             Competition (AMC/AIME)            403       93.5%       [90.8%, 95.6%]
                             Other (MathD, etc.)                39       87.2%       [72.6%, 95.7%]
                             Overall                           454      93.4%        [90.8%, 95.5%]
Table 15. Accuracy stratified by problem difficulty (Llama-8B, corrected labels). Performance is highest on olympiad-level problems.



C.7. Proof Length

                                    Length Quintile       Token Range        n     Accuracy
                                    Very Short                 < 50          91      97.8%
                                    Short                     50–100         91      93.4%
                                    Medium                   100–200         90      91.1%
                                    Long                     200–400         91      95.6%
                                    Very Long                 > 400          91      92.3%
          Table 16. Accuracy by proof length (Llama-8B, corrected labels). Performance is stable across all length ranges.



C.8. Metric Correlations

                                             Fiedler     HFER        Smooth.      Entropy     Energy
                            Fiedler           1.000      −0.288      0.422         0.294       −0.275
                            HFER                          1.000      −0.606       −0.975        0.892
                            Smoothness                                1.000        0.644       −0.468
                            Entropy                                                1.000       −0.925
                            Energy                                                              1.000
Table 17. Pearson correlations between spectral metrics (Layer 30, Llama-8B). HFER and Entropy are nearly redundant (r = −0.975);
Fiedler is largely independent.




                                                                19
                        Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

C.9. Cross-Model Transfer

                           Source         Target           Src Acc      Tgt Acc (raw)         Drop
                           Llama-8B       Phi-3.5-mini      94.1%            52.4%          −41.7%
                           Llama-8B       Llama-1B          94.1%            48.9%          −45.2%
                           Llama-8B       Qwen-7B           94.1%            51.8%          −42.3%
            Table 18. Cross-model threshold transfer (raw, uncalibrated). Raw thresholds fail due to scale differences.



C.10. Head Aggregation Methods

                                   Aggregation                    Best |d|    Best Accuracy
                                   Uniform (αh = 1/H)                2.91          93.6%
                                   Mass-weighted (default)           3.00          94.1%
                                   Max-head only                     2.54          91.4%
   Table 19. Comparison of head aggregation methods (Llama-8B, corrected labels). Mass-weighted performs marginally better.



C.11. Laplacian Normalization

                                    Laplacian Type               Best |d|     Best Accuracy
                                    Combinatorial (default)          3.00          94.1%
                                    Symmetric normalized             2.88          93.4%
                                    Random walk                      2.81          93.0%
       Table 20. Comparison of Laplacian normalizations (Llama-8B, corrected labels). Results are similar across variants.




                                                                20
                           Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

D. Architectural Variation Details
D.1. The Mistral Sliding Window Attention Effect
Mistral-7B presents a striking pattern: while achieving strong statistical significance (pMW = 1.16 × 10−48 , pt =
1.21 × 10−78 ), its best discriminating metric differs from other models. Rather than HFER (which dominates for Llama
models), Mistral’s validity signal appears in late-layer Smoothness (L26, d = 2.09).
This is the only model in our evaluation using Sliding Window Attention (SWA) (Beltagy et al., 2020; Child et al., 2019),
which restricts attention to a 4096-token local window. Notably, while HFER at L11 still achieves significance for Mistral
(pMW = 3.94 × 10−49 , d = −1.57), the effect size is substantially weaker than other models, and Smoothness provides
stronger discrimination.

                                               Model                        Attention                              Best Metric                  |d|
                                               Llama-3.1-8B                 Global (Full)                           HFER (L30)                  3.00
                                               Qwen2.5-7B                   Global (Full)                           HFER (L26)                  2.43
                                               Phi-3.5-mini                 Global (Full)                          Smooth (L25)                 3.30
                                               Mistral-7B                   Sliding Window                         Smooth (L26)                 2.09
Table 21. Attention mechanism architecture affects which spectral feature best captures validity. Sliding Window Attention shifts the
signal from HFER to Smoothness.


We hypothesize that SWA redistributes validity information across spectral features:
1. Global attention concentrates validity in spectral frequency content (HFER), which captures global signal smoothness.
2. Local attention distributes validity into graph smoothness properties, which measure local coherence within attention
   windows.
                                                          Llama-3.1-8B (HFER)                                             Mistral-7B (HFER)

                                                                                  Valid
                                                         d = −3.00                                            40                           d = −1.57
                                               8                                  Invalid


                                               6
                                     Density




                                                                                                 Density




                                               4                                                              20

                                               2

                                               0                                                              0
                                                    0         0.2           0.4     0.6                       5 · 10−2 0.1       0.15     0.2     0.25
                                                                    Value                                                         Value

                                                        Llama-3.1-8B (Smoothness)                                       Mistral-7B (Smoothness)

                                               20         d = 2.27                                                       d = 2.09

                                               15                                                              4
                                  Density




                                                                                                    Density




                                               10
                                                                                                               2
                                               5

                                               0                                                               0
                                                    0.7     0.75     0.8 0.85     0.9                               0      0.2    0.4 0.6        0.8     1
                                                                    Value                                                         Value

Figure 5. Architectural Determinism of Validity. Comparing Llama-3.1-8B (Global Attention) and Mistral-7B (Sliding Window
Attention). Llama separates proofs via frequency (HFER), while Mistral separates them via local connectivity (Smoothness).


D.2. Mixture-of-Experts Analysis
To test the method’s limits under sparse computation, we evaluated Qwen-MoE on MiniF2F. Unlike dense models, MoEs
route tokens dynamically to different expert networks, potentially fracturing the global attention topology.
Signal Attenuation. We observe a distinct “Sparsity Penalty.” While the spectral signal remains statistically significant
(p < 10−10 ), the effect size attenuates from d ≈ 3.0 (dense) to d ≈ 1.6 (sparse) on balanced data. We hypothesize that
expert routing introduces topological noise, acting as a diffractor that scatters the spectral energy of the attention graph.
Entropy as a Routing Proxy. The dominant metric shifts to Spectral Entropy (Accuracy 83.0% at Layer 14). Valid proofs
exhibit significantly lower entropy (µ = 2.17) than invalid ones (µ = 2.52). In an MoE context, this suggests that valid

                                                                                            21
                           Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

reasoning corresponds to “focused routing”, coherent attention to relevant contexts, whereas hallucinations manifest as
“routing entropy.”
Error Agnosticism. A taxonomic breakdown reveals that the spectral signature is remarkably error-agnostic. The effect
size for detecting Logic Errors (d = 0.56) is nearly identical to that for Calculation Errors (d = 0.53), showing that even
minor arithmetic deviations induce measurable geometric stress in the attention graph.

                                      Setting Best Metric Layer           pMW         |d|   Acc.
                                            Qwen-MoE on MiniF2F (Balanced, n = 100)
                                               Entropy        L14      1.03 × 10−10 1.67 83.0%
                                               HFER           L22      1.29 × 10−10 1.65 81.0%
                                               Smoothness     L12      1.80 × 10−9 1.50 83.0%
                                               Qwen-MoE on MiniF2F (Full, n = 454)
                                               Smoothness     L6       3.16 × 10−67 2.73 93.6%
                                               HFER           L22      2.02 × 10−65 2.54 90.5%
Table 22. Mixture-of-Experts Results. On balanced data, effect sizes attenuate to d ≈ 1.6 (“sparsity penalty”). On the full dataset, the
signal recovers to d = 2.73.



D.3. Cognitive Interpretation
The asymmetry between false positive and false negative errors suggests a cognitive interpretation of the spectral signature:

• Invalid proofs with low spectral energy are “confidently wrong”, the model processes them smoothly despite their
  incorrectness, analogous to the Dunning-Kruger effect in human cognition.
• Valid proofs with high spectral energy involve genuine cognitive effort, the model recognizes difficulty and allocates
  more computational resources, producing higher-frequency activity.

Under this interpretation, the spectral signature reflects not just validity, but the model’s epistemic state, its implicit certainty
about its own reasoning. Low HFER indicates confident processing (justified for valid proofs, unjustified for “confidently
wrong” invalid proofs); high HFER indicates effortful processing.
This interpretation suggests applications beyond validity classification:
• Difficulty estimation: High-energy valid proofs may indicate genuinely challenging problems.
• Overconfidence detection: Low-energy invalid proofs may signal dangerous overconfidence.
• Uncertainty quantification: Spectral features could complement or replace learned uncertainty estimates.




                                                                  22
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

E. Complete Results Tables
E.1. Label Correction Statistics

                  Model              Family         Orig. Valid     Corr. Valid     Reclaimed      % Change
                  Llama-3.2-1B       Meta               154             205            +51           +33.1%
                  Llama-3.2-3B       Meta               154             195            +41           +26.6%
                  Llama-3.1-8B       Meta               154             193            +39           +25.3%
                  Qwen2.5-0.5B       Alibaba            154             194            +40           +26.0%
                  Qwen2.5-7B         Alibaba            154             187            +33           +21.4%
                  Phi-3.5-mini       Microsoft          154             205            +51           +33.1%
                  Mistral-7B         Mistral AI         154             190            +36           +23.4%
Table 23. Label correction statistics across all models. All seven models independently identify 33–51 compiler-rejected proofs as
spectrally valid.



F. Reproducibility Checklist
Code Availability. The complete implementation including attention extraction, spectral computation, thresh-
old optimization, and Lanczos-accelerated eigendecomposition is available at https://github.com/vcnoel/
geometry-of-reason.
Data Availability. We use the publicly available MiniF2F benchmark (Zheng et al., 2022). Our 454-proof evaluation subset
with all labels (original and corrected) and metadata will be released.
Compute Requirements. All experiments can be reproduced on a single NVIDIA A100 GPU (40GB) in under 3 hours
total. Memory requirements are dominated by model inference, not spectral computation.
Hyperparameters. The only hyperparameter is the classification threshold τ . We report results using both full-data
calibrated thresholds and nested cross-validation. Threshold robustness analysis (Section C.5) confirms low sensitivity.
Statistical Reporting. All p-values are reported using both non-parametric Mann-Whitney U tests (pMW ) and parametric
two-sided Welch’s t-tests (pt ) for full transparency and robustness. We apply Benjamini-Hochberg correction for multiple
comparisons when scanning over layer-metric combinations. Effect sizes use Cohen’s d with pooled standard deviation.
Random Seeds. No random seeds are required: our method is fully deterministic given model weights.

F.1. Top 10 Discriminators per Model on MiniF2F (Corrected Labels)

                        Metric       Layer        pMW             pt        Cohen’s d Valid µ Invalid µ
                                         Llama-3.1-8B-Instruct (193 Valid, 261 Invalid)
                        HFER       L0        7.94 × 10−65   2.43 × 10−93      −2.88       0.193   0.327
                        Smoothness L10       3.31 × 10−64   2.03 × 10−92      −2.69       0.977   1.005
                        Smoothness L15       6.67 × 10−64   5.53 × 10−80      −2.11       0.967   0.997
                        Smoothness L9        7.82 × 10−64   2.26 × 10−92      −2.82       0.974   1.003
                        HFER       L31       9.29 × 10−64   2.45 × 10−94      −2.56       0.305   0.448
                        HFER       L30       9.40 × 10−64   5.44 × 10−105     −3.00       0.170   0.333
                        Smoothness L12       1.16 × 10−63   8.41 × 10−84      −2.63       0.963   0.988
                        Smoothness L11       1.86 × 10−63   3.91 × 10−86      −2.73       0.972   0.999
                        Smoothness L8        3.11 × 10−63   1.04 × 10−88      −2.74       0.974   1.003
                        Smoothness L13       3.19 × 10−63   1.85 × 10−74      −2.22       0.964   0.983
Table 24. Top 10 discriminators: Llama-3.1-8B-Instruct. Llama-3.1-8B-Instruct consistently favor HFER and Smoothness at mid-to-
late layers, with effect sizes |d| ≥ 2.88.




                                                               23
                        Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                      Metric      Layer       pMW              pt        Cohen’s d Valid µ Invalid µ
                                       Llama-3.2-1B-Instruct (205 Valid, 249 Invalid)
                      HFER       L15      5.73 × 10−67   1.01 × 10−100    −2.66      0.332       0.450
                      Smoothness L7       8.79 × 10−65   9.42 × 10−79     −2.65      0.963       0.986
                      Entropy    L15      1.77 × 10−64   2.34 × 10−88     +2.62      3.007       2.550
                      HFER       L11      2.02 × 10−64   7.04 × 10−103    −2.69      0.051       0.107
                      Smoothness L8       2.31 × 10−64   3.63 × 10−81     −2.52      0.960       0.981
                      Energy     L9       5.14 × 10−64   1.74 × 10−85     −2.66     608507      626347
                      Fiedler    L0       1.47 × 10−63   1.83 × 10−92     +3.02      0.536       0.412
                      HFER       L0       1.62 × 10−63   2.60 × 10−110    −3.00      0.158       0.297
                      Smoothness L6       3.27 × 10−63   1.07 × 10−81     −2.75      0.970       0.999
                      Smoothness L0       3.79 × 10−63   7.07 × 10−105    +2.70      0.870       0.815
                                       Llama-3.2-3B-Instruct (195 Valid, 259 Invalid)
                      HFER       L0       3.16 × 10−63   1.85 × 10−101    −2.88         0.233   0.448
                      HFER       L11      3.66 × 10−62   6.06 × 10−102    −2.97         0.106   0.187
                      HFER       L26      6.45 × 10−62   4.50 × 10−106    −2.75         0.126   0.273
                      Smoothness L11      9.83 × 10−62   3.39 × 10−83     −2.56         0.969   0.999
                      Smoothness L9       2.00 × 10−61   1.52 × 10−89     −2.73         0.978   1.012
                      Smoothness L8       2.07 × 10−61   1.82 × 10−90     −2.70         0.975   1.006
                      Entropy    L25      3.86 × 10−61   1.11 × 10−92     −2.84         1.824   2.450
                      Entropy    L27      3.90 × 10−61   2.39 × 10−92     +2.56         3.026   2.437
                      Smoothness L10      4.56 × 10−61   2.70 × 10−80     −2.60         0.973   1.001
                      Smoothness L0       6.60 × 10−61   3.49 × 10−89     +2.39         0.794   0.721
Table 25. Top 10 discriminators: Meta Llama family. The Llama models consistently favor HFER and Smoothness at mid-to-late
layers, with effect sizes |d| ≥ 2.66. Llama-1B uniquely shows strong Fiedler discrimination at L0 (d = 3.02).




                                                            24
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                     Metric        Layer        pMW             pt        Cohen’s d     Valid µ    Invalid µ
                                           Qwen2.5-0.5B-Instruct (194 Valid, 260 Invalid)
                     Entropy    L0         4.45 × 10−65   1.43 × 10−116     +2.93       3.317        2.401
                     Smoothness L3         3.84 × 10−64   2.05 × 10−53      −2.22       0.951        0.964
                     Energy     L4         1.75 × 10−63   1.28 × 10−81      −2.75      1553410      1598135
                     Smoothness L14        5.78 × 10−63   7.43 × 10−81      −2.70       0.931        0.965
                     Smoothness L15        7.11 × 10−63   2.02 × 10−72      −2.19       0.939        0.959
                     Entropy    L1         1.14 × 10−62   1.21 × 10−96      +2.88       2.718        1.839
                     Energy     L16        1.87 × 10−62   1.86 × 10−101     −2.70      1738815      1876539
                     Energy     L19        1.94 × 10−62   7.15 × 10−101     −2.82      1742982      1945174
                     Smoothness L4         2.02 × 10−62   7.30 × 10−59      −2.10       0.939        0.954
                     Energy     L17        3.65 × 10−62   7.48 × 10−101     −2.72      1717977      1874831
                                           Qwen2.5-7B-Instruct (187 Valid, 267 Invalid)
                     HFER       L26        5.68 × 10−55    2.45 × 10−75     −2.43       0.236     0.405
                     Entropy    L2         9.59 × 10−55    7.43 × 10−79     +2.38       2.449     1.845
                     HFER       L12        2.17 × 10−54    6.85 × 10−74     −1.94       0.073     0.105
                     Entropy    L1         7.45 × 10−54    2.05 × 10−68     +2.28       1.932     1.147
                     Smoothness L23        7.62 × 10−54    4.66 × 10−83     +2.21       0.752     0.560
                     Energy     L23        9.44 × 10−54    1.95 × 10−80     +2.13     150401749 116500534
                     Smoothness L24        1.34 × 10−53    2.24 × 10−86     +2.33       0.689     0.396
                     Energy     L24        1.43 × 10−53    2.59 × 10−84     +2.26     137099662 83429886
                     HFER       L9         1.46 × 10−53    8.21 × 10−67     −1.79       0.069     0.105
                     Smoothness L14        1.58 × 10−53    4.80 × 10−83     +2.17       0.887     0.833
Table 26. Top 10 discriminators: Alibaba Qwen family. Qwen-0.5B uniquely favors Spectral Entropy at early layers (d = 2.93 at
L0), achieving pt = 1.43 × 10−116 , the most significant result in our study. Qwen-7B shows a more diverse metric profile with HFER,
Entropy, and Smoothness all contributing.




                                                                25
                           Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                       Metric       Layer        pMW              pt        Cohen’s d    Valid µ      Invalid µ
                                            Phi-3.5-mini-Instruct (205 Valid, 249 Invalid)
                       Smoothness L27        1.69 × 10−66   5.60 × 10−100     +3.21       0.496    0.239
                       Smoothness L26        2.37 × 10−66   1.86 × 10−103     +3.27       0.464    0.153
                       Smoothness L25        4.51 × 10−66   2.33 × 10−107     +3.30       0.438    0.076
                       Smoothness L28        4.74 × 10−66   2.03 × 10−95      +3.12       0.543    0.343
                       HFER       L26        5.64 × 10−66   2.41 × 10−95      −3.16       0.312    0.560
                       Energy     L26        9.95 × 10−66   5.86 × 10−75      +2.28     21029690 10964297
                       Smoothness L23        2.64 × 10−65   4.34 × 10−113     +3.29       0.395   −0.095
                       Smoothness L24        3.29 × 10−65   6.49 × 10−111     +3.30       0.418   −0.012
                       Energy     L25        4.10 × 10−65   6.39 × 10−101     +2.79     18433282 4584151
                       Smoothness L22        6.16 × 10−65   3.54 × 10−114     +3.28       0.384   −0.144
                                         Mistral-7B-v0.1-Instruct (190 Valid, 264 Invalid)
                       HFER       L11        3.94 × 10−49    1.10 × 10−52     −1.57           0.121    0.145
                       Smoothness L26        1.16 × 10−48    1.21 × 10−78     +2.09           0.639    0.354
                       HFER       L30        2.85 × 10−48    3.78 × 10−67     −1.87           0.234    0.313
                       Smoothness L25        3.45 × 10−48    1.25 × 10−77     +2.07           0.627    0.327
                       Smoothness L24        6.31 × 10−48    4.07 × 10−77     +2.05           0.630    0.334
                       Energy     L25        2.60 × 10−47    1.72 × 10−69     +1.86          128639    81926
                       Smoothness L27        3.38 × 10−47    3.02 × 10−75     +2.04           0.640    0.360
                       Energy     L24        4.63 × 10−47    1.77 × 10−69     +1.86          125535    79445
                       Smoothness L23        6.02 × 10−47    1.49 × 10−74     +2.00           0.674    0.415
                       Energy     L26        6.08 × 10−47    1.37 × 10−64     +1.76          135930    95322
Table 27. Top 10 discriminators: Microsoft Phi and Mistral AI. Phi-3.5-mini exhibits the largest effect sizes in our study (d = 3.30)
via late-layer Smoothness, with invalid proofs showing negative smoothness (L22–L24). Mistral-7B’s Sliding Window Attention shifts
the optimal metric from HFER (d = 1.57) to Smoothness (d = 2.09), demonstrating that attention mechanism architecture determines
which spectral features best capture reasoning validity.




                                                                 26
                          Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

                     Metric        Layer         pMW              pt        Cohen’s d Valid µ Invalid µ
                                         Qwen-MoE-A2.7B (194 Valid, 260 Invalid)
                     Smoothness L13         2.79 × 10−67 2.49 × 10−84          −2.19      0.931      0.971
                     Smoothness L6          3.16 × 10−67 4.34 × 10−92          −2.73      0.937      0.980
                     Smoothness L12         6.22 × 10−67 5.47 × 10−83          −2.15      0.942      0.995
                     Smoothness L11         1.92 × 10−66 4.22 × 10−88          −2.25      0.950      1.003
                     Smoothness L8          2.20 × 10−66 1.03 × 10−87          −2.25      0.940      0.986
                     Smoothness L7          3.24 × 10−66 1.45 × 10−86          −2.38      0.941      0.972
                     Smoothness L14         1.14 × 10−65 1.93 × 10−94          −2.39      0.949      1.006
                     HFER       L22         2.02 × 10−65 1.68 × 10−98          −2.54      0.272      0.378
                     Smoothness L10         2.82 × 10−65 2.21 × 10−81          −2.13      0.943      0.989
                     Smoothness L9          4.45 × 10−65 3.38 × 10−86          −2.23      0.943      0.990
Table 28. Top 10 discriminators: Qwen-MoE-A2.7B. Smoothness dominates across early-to-mid layers (d up to 2.73 at L6), with HFER
providing complementary discrimination at L22 (d = 2.54). Effect sizes are attenuated relative to dense models, consistent with the
“sparsity penalty” reported in Section D.2.




                                                                27
                                       Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning

G. Ethical Considerations
The authors identify no significant ethical risks associated with the mechanistic probing techniques presented in this work.
Regarding the preparation of this manuscript, Large Language Models (specifically Gemini 3.0 Pro) were used to assist
with prose refinement, grammatical cleaning, and code refactoring. All outputs were manually reviewed and verified by the
authors, who take full responsibility for the final content and technical accuracy of the paper.

H. Every layer plots

             Fiedler Value (λ2 )                 HFER (High Freq Energy Ratio)                          Smoothness Index (η)                        Spectral Entropy (H)
   0.8
                                                                                               1
                                                                                                                                            3
                                                   0.4
   0.6
                                                                                              0.8                                           2
                                                   0.2

   0.4                                                                                                                                      1
                                                                                              0.6
                                                    0
         0       5           10           15             0    5           10             15         0            5           10        15       0           5           10        15

                     Layer                                        Layer                                              Layer                                      Layer

                                                                                     Valid     Invalid


                                        Figure 6. Layer-wise spectral metrics (Combined) for Llama 3.2 1B Instruct.



             Fiedler Value (λ2 )                  HFER (High Freq Energy Ratio)                             Smoothness Index (η)                        Spectral Entropy (H)

   0.8                                             0.6                                              1                                           3


                                                   0.4                                         0.8
   0.6                                                                                                                                          2


                                                   0.2                                         0.6
                                                                                                                                                1
   0.4
                                                                                               0.4
                                                     0
         0        10              20                     0        10           20                       0            10           20                0           10           20

                     Layer                                         Layer                                              Layer                                      Layer

                                                                                     Valid      Invalid


                                        Figure 7. Layer-wise spectral metrics (Combined) for Llama 3.2 3B Instruct.




                                                                                    28
                            Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning




          Fiedler Value (λ2 )            HFER (High Freq Energy Ratio)                   Smoothness Index (η)            Spectral Entropy (H)
                                           0.6
                                                                               1.2
0.8
                                                                                                                 3
                                           0.4
                                                                                 1
0.6
                                                                                                                 2
                                           0.2                                 0.8
0.4
                                                                                                                 1
                                                                               0.6
                                            0
      0       10       20       30               0   10       20      30             0        10       20   30       0        10       20   30

                   Layer                                  Layer                                    Layer                           Layer

                                                                     Valid      Invalid


                             Figure 8. Layer-wise spectral metrics (Combined) for Llama 3.1 8B Instruct.




          Fiedler Value (λ2 )            HFER (High Freq Energy Ratio)                   Smoothness Index (η)            Spectral Entropy (H)

                                                                                 1
0.8                                                                                                              3

                                           0.4
0.6                                                                                                              2
                                                                               0.5
                                           0.2
0.4                                                                                                              1

                                            0
                                                                                 0
      0       10       20       30               0   10       20      30             0        10       20   30       0        10       20   30

                   Layer                                  Layer                                    Layer                           Layer

                                                                     Valid      Invalid


                                     Figure 9. Layer-wise spectral metrics (Combined) for Mistral 7B.




          Fiedler Value (λ2 )            HFER (High Freq Energy Ratio)                   Smoothness Index (η)            Spectral Entropy (H)
                                                                                 1
0.8                                        0.8


0.6                                        0.6
                                                                               0.5                               2

0.4                                        0.4

0.2                                        0.2                                   0
                                                                                                                 1
 0                                          0

      0       10       20       30               0   10       20      30             0        10       20   30       0        10       20   30

                   Layer                                  Layer                                    Layer                           Layer

                                                                     Valid      Invalid


                             Figure 10. Layer-wise spectral metrics (Combined) for Phi 3.5 Mini Instruct.




                                                                   29
                             Geometry of Reason: Spectral Signatures of Valid Mathematical Reasoning




          Fiedler Value (λ2 )           HFER (High Freq Energy Ratio)                       Smoothness Index (η)             Spectral Entropy (H)

                                                                                    1
0.6                                       0.6
                                                                                                                     3
                                                                                  0.8
                                          0.4
0.4
                                                                                  0.6
                                          0.2                                                                        2
0.2                                                                               0.4
                                           0
                                                                                  0.2
      0         10            20                0      10           20                  0          10           20       0          10           20

                Layer                                  Layer                                       Layer                            Layer

                                                                         Valid     Invalid


                             Figure 11. Layer-wise spectral metrics (Combined) for Qwen 2.5 0.5B Instruct.




          Fiedler Value (λ2 )           HFER (High Freq Energy Ratio)                       Smoothness Index (η)             Spectral Entropy (H)
                                                                                    1
                                          0.6                                                                        3
0.6
                                                                                  0.5
                                          0.4
                                                                                                                     2
0.4
                                          0.2                                       0

                                                                                                                     1
0.2
                                           0                                     −0.5

      0        10       20                      0    10        20                       0         10       20            0         10       20

                Layer                                  Layer                                       Layer                            Layer

                                                                         Valid     Invalid


                              Figure 12. Layer-wise spectral metrics (Combined) for Qwen 2.5 7B Instruct.




          Fiedler Value (λ2 )           HFER (High Freq Energy Ratio)                       Smoothness Index (η)             Spectral Entropy (H)
                                          0.8                                     1.2
0.8
                                                                                                                     3
                                          0.6                                       1
0.6
                                          0.4                                     0.8                                2
0.4
                                          0.2                                     0.6
                                                                                                                     1
0.2                                                                               0.4
                                           0
      0         10            20                0      10           20                  0          10           20       0          10           20

                Layer                                  Layer                                       Layer                            Layer

                                                                         Valid     Invalid


                        Figure 13. Layer-wise spectral metrics (Combined) for Qwen 1.5 MoE A2.7b Chat.




                                                                    30
