                                                      The Faithfulness Gap: Certifying Semantic Equivalence Between
                                                         Natural-Language and Formal Mathematical Statements


                                                                                 Noor Islam S. Mohammad * 1 Tamim Sheikh 2


                                                                   Abstract                                       1. Introduction
                                                Autoformalization, translating natural-language                   Modern autoformalization systems built on large language
                                                mathematics into formal proof assistants, is bot-                 models routinely translate natural-language theorem state-
arXiv:2606.16541v1 [cs.AI] 15 Jun 2026




                                                tlenecked not by translation fluency but by faith-                ments into formal proof assistants such as Lean 4, Rocq,
                                                fulness: a formal statement can typecheck and                     or Isabelle/HOL (Wu et al., 2022; Jiang et al., 2023; Azer-
                                                be provable, yet still encode a different theorem                 bayev et al., 2024; Jiang et al., 2022). The dominant quality
                                                than the source intended. We introduce Bidirec-                   signal used to gate these outputs is whether the resulting
                                                tional Provability Fingerprinting (BPF), a frame-                 formal statement typechecks—and, optionally, whether a
                                                work that certifies faithfulness by characterizing                downstream prover can close it (Polu & Sutskever, 2020;
                                                each candidate through its forward and backward                   Han et al., 2022; Lample et al., 2022). Both signals are
                                                consequence neighborhoods in the ambient the-                     necessary, but neither is sufficient. A formal statement can
                                                ory and matching these against probes derived                     be syntactically well-formed, provable, and wrong: it can
                                                from the natural-language statement. We further                   mean something other than what the mathematician wrote.
                                                introduce four novel components: (i) Counterfac-                  We call this the faithfulness gap. Unlike code—where
                                                tual Probe Generation (CPG), a contrastive pro-                   unit tests and runtime semantics offer an executable ora-
                                                cedure that synthesizes probes targeting specific                 cle—the faithfulness of a formalization is a relation be-
                                                drift directions; (ii) the Equivalence Spectrum, a                tween two semantic objects living in different universes:
                                                continuous faithfulness score that replaces brittle               a natural-language sentence interpreted under tacit mathe-
                                                binary verdicts; (iii) Adaptive Probe Budget Al-                  matical convention and a formal expression interpreted un-
                                                location (APBA), an information-theoretic bud-                    der a precisely specified dependent type theory (de Moura
                                                get router; and (iv) Faithfulness-Guided Decod-                   & Ullrich, 2021; The mathlib Community, 2020). There is
                                                ing (FGD), which uses BPF signals as a reward                     no executable bridge between them. Standard evaluation
                                                during autoformalization. We prove a drift detec-                 practices—BLEU-style overlap against a single reference
                                                tion theorem and a PAC-faithfulness result estab-                 formalization, expert spot checks, or downstream prover
                                                lishing that the equivalence class of a natural lan-              success—each address only a surface symptom of the prob-
                                                guage statement is learnable from O(log(1/δ)/ε)                   lem and systematically miss the most insidious failures, in
                                                probes under mild assumptions. We release                         which the formalization is fluent, well-typed, and demon-
                                                D RIFT B ENCH, a benchmark of 2,183 NL/Lean 4                     strably provable but quietly says the wrong thing.
                                                pairs with controlled drift labels across six sub-
                                                fields of mathlib4. BPF + CPG detects 89.6%
                                                of drifted formalizations at a 3.0% false-positive                Our approach. We propose Bidirectional Provability
                                                rate-against 41.2% for typecheck and 63.3% for                    Fingerprinting (BPF), a framework for certifying faithful-
                                                LLM-judge baselines, and FGD reduces the rate                     ness without requiring a reference formalization. The core
                                                at which a state-of-the-art autoformalizer emits                  insight is operational: a statement’s meaning is determined
                                                drifted statements by 47%. bpf.ml.github.io                       by what it implies and what implies it, so two statements
                                                                                                                  are semantically equivalent if and only if their consequence
                                            1
                                             Department of Computer Science, Informatics Institute, Istan-        neighborhoods coincide in the ambient theory. Figure 1
                                         bul Technical University, İstanbul, Türkiye 2 Department of Com-       shows the end-to-end pipeline. Given a natural-language
                                         puter Science and Engineering, Jashore University of Science and         statement N and a candidate formalization F , we (i) gener-
                                         Technology, Bangladesh. Correspondence to: Noor Islam S. Mo-             ate a set of semantic probes from N , (ii) autoformalize and
                                         hammad <islam23@itu.edu.tr>.                                             filter them, (iii) compute entailment relations between F ,
                                         The 6th Muslims in ML (MusIML) Workshop at 43 rd Interna-                each probe, and the proof assistant, and (iv) compare the
                                         tional Conference on Machine Learning, Seoul, South Korea.               resulting fingerprint against the expected fingerprint pre-
                                         Copyright 2026 by the author(s).                                         dicted from N .

                                                                                                              1
                                           Certifying Faithfulness in LLM Autoformalization

                                                                                                              Entailment (§4,§7)

                                                                                                                 APBA
                                                                                                              budget router
                                                                   Probe pipeline (§5)


                                Input
                                                      CPG
                                                 (counterfactual                                                   Lean 4 +
                                                   probe gen.)        Probe set          Autoformalize
                        Natural-language                                                                            mathlib
                                                                     PN + labels            probes
                         statement N                                                                           entailment oracle
                                                  Probe label
                                                   predictor
                            Candidate                                                     Decision (§6)
                         formalization F
                                                                                              Predicted          Fingerprint
                                                                                                ΦN                  ΦF
                   FGD reward


                                                                               Verdict                 Equivalence
                                                                           {ACC , REV, REJ}         Spectrum E(F, N )


Figure 1. BPF architecture. The natural-language statement N and the candidate formalization F enter from the left; CPG synthesizes
counterfactual probes (§5); the entailment oracle, routed by APBA (§7), computes the forward/backward fingerprint ΦF ; the equivalence
spectrum E(F, N ) (§6) compares it to the prediction ΦN and emits one of three verdicts. The dashed red loop is the optional FGD
feedback to the autoformalizer (§9).


Contributions. We make six contributions, each tackling                   petitive autoformalization on competition mathematics,
a distinct facet of the faithfulness problem. We formalize                and follow-up systems integrate formalization with proof
the autoformalization faithfulness problem as a relation be-              search (Jiang et al., 2023; 2022; First et al., 2023). Azer-
tween distributions over interpretations, sidestepping the                bayev et al. (2024) trained domain-specialized models on
need for a canonical reference (Section 3). We intro-                     a mixture of formal libraries and informal mathematics.
duce BPF, a probe-based, reference-free faithfulness cer-                 Across this line, faithfulness is typically assessed by ei-
tifier with bidirectional consequence-neighborhood match-                 ther typechecking, BLEU/exact-match against a reference,
ing (Section 4). We introduce Counterfactual Probe Gen-                   or downstream provability—each of which we show Sec-
eration (CPG), a contrastive probe-synthesis procedure                    tion 11 is dominated by BPF.
that explicitly targets the four canonical drift classes and
improves detection over generic probe generation (Sec-                    Semantic evaluation of generated formal artifacts. For
tion 5). We introduce the Equivalence Spectrum E(F, N ),                  programs, semantic equivalence is operationalized via test
a continuous faithfulness score with calibrated decision re-              execution (Austin et al., 2021; Chen et al., 2021). The clos-
gions, and Adaptive Probe Budget Allocation (APBA), an                    est analogue in mathematics is the use of counter-models
information-theoretic budget router that reaches the same                 or symbolic execution against numerical instances (Polu
detection accuracy as uniform sampling with 3.2× fewer                    & Sutskever, 2020; Welleck et al., 2022). Such meth-
probes (Sections 6 and 7). We prove a drift detection the-                ods catch outright falsity but cannot distinguish a true-but-
orem and a PAC-faithfulness theorem characterizing what                   wrong statement (e.g., case (C) above) from the intended
BPF can and cannot be detected, and we identify a class                   one. Patel et al. (2024) uses back-translation, which we
of conventional drift for which we develop a complemen-                   evaluate as a baseline. We are aware of no prior work that
tary structural test (Section 8). We introduce Faithfulness-              uses probe-based consequence neighborhoods for faithful-
Guided Decoding (FGD), which uses BPF scores as a re-                     ness certification, or that uses faithfulness signals to guide
ward signal during autoformalization, reducing the rate of                LLM decoding.
drifted outputs from a state-of-the-art autoformalizer by
47% (Section 9). We release D RIFT B ENCH, the first bench-               Inferential semantics and equivalence in formal li-
mark with controlled drift labels (Section 10), and report                braries. Within proof libraries, equivalence between
extensive experiments and ablations (Section 11).                         definitions is often established by handwritten iff or
                                                                          equiv lemmas (The mathlib Community, 2020). Our
2. Related Work                                                           forward/backward fingerprint construction generalizes this
                                                                          practice and automates it for arbitrary candidates. The no-
Autoformalization. Early work cast translation as ma-                     tion of characterizing meaning via inferential role has a
chine translation with retrieval augmentation (Wang et al.,               long history in proof-theoretic semantics (Brandom, 2000;
2018; Szegedy, 2020). Wu et al. (2022) showed that                        Prawitz, 1965); we adapt it for an LLM/prover loop.
few-shot prompting of large language models yields com-                   Benchmarks and verification: MiniF2F (Zheng et al.,

                                                                     2
                                      Certifying Faithfulness in LLM Autoformalization

2022), ProofNet (Azerbayev et al., 2023), FIMO (Liu et al.,                                                             ∆H Hypothesis Omission
                                                                      ∆∀ Quantifier Inversion
2023), and LeanDojo (Yang et al., 2023) measure prover ca-                                                              A premise of N absent from F .
                                                                      Swaps ∀x ∃y with ∃y ∀x. Drifted F
pability on pre-specified formal statements. None directly                                                              Formalisation is strictly stronger than
                                                                      often provable yet disjoint from N .
evaluates whether a formalization matches an input natural-                                                             intended.
language sentence. D RIFT B ENCH is, to our knowledge,                ∆C Conclusion Generali-                           ∆T Type Coercion
the first benchmark with controlled drift labels and the first        sation                                            Silent retagging, e.g. R → Q or
to evaluate the autoformalization-faithfulness loop end-to-
                                                                      F ⇒ N but N ̸⇒ F . Locally                        total → partial. Hardest to detect
end.
                                                                      plausible; globally unsound.                      syntactically.


3. The Faithfulness Problem                                          Figure 2. The four canonical drift classes in which F fails ε-
                                                                     faithfulness while remaining well-typed and often provable. ∆∀
We now formalize faithfulness. Let N denote the space of             and ∆T are the most pernicious.
natural-language mathematical statements and F a formal
language interpreted in a theory T (we use Lean 4 + math-            over P is
lib4 throughout). A formalizer is a function µ : N → F. A
single canonical formal target is too rigid: distinct mathe-                       Φ+
                                                                                    F (P) = { P ∈ P : T ⊢ F → P },
maticians, working in distinct libraries, will produce differ-       and the backward fingerprint is
ent but equivalent formalizations of the same English sen-
tence—e.g., using Set versus Finset, or stating a func-                            Φ−
                                                                                    F (P) = { P ∈ P : T ⊢ P → F }.
tion as Continuous versus Continuous on a univer-                    The full fingerprint is ΦF (P) = (Φ+       −
                                                                                                        F (P), ΦF (P)).
sal set. We therefore introduce an interpretation distribu-
tion.                                                                Figure 3 illustrates the geometry. The forward fingerprint
Definition 3.1 (Interpretation distribution). An interpreta-         captures the downstream commitments of F , everything
tion distribution DN for N ∈ N is a probability distribu-            that follows from it, while the backward fingerprint cap-
tion over formal statements in F whose support consists              tures its upstream conditions-everything that would suffice
of formalizations that competent mathematicians would ac-            to prove it. Two statements that agree on both sets are op-
cept as expressing N in the theory T .                               erationally indistinguishable in the theory T .
Definition 3.2 (ε-Faithfulness). A candidate F ∈ F is ε-                     Q1                                                                       P1
faithful to N under DN if                                                      Backward Φ   −                                              Forward Φ+
                                                                                                                                                           P2
                                                                          Q2
                                                                                                        N                        F
                                 
                Pr T ⊢ F ↔ I ≥ 1 − ε.
              I∼DN                                                                                                                                    P3

                                                                             Q3                      Reference                Candidate
                                                                                                                                                 P4
Theorem 3.2 weakens equality to provable equivalence, ac-
commodating notational variation while remaining strict                  — agreement     · · · disagreement (drift witness)

about semantic content. The interpretation distribution is
                                                                     Figure 3. A provability fingerprint over probes {Pi , Qj }. The ref-
implicit and never materialized; all of our methods reason           erence N entails each forward probe Pi and is entailed by each
over it through probes. A taxonomy of drift: We identify             backward probe Qj . The candidate F matches N on most probes
four canonical classes of semantic drift-ways a formaliza-           (green dashed) but disagrees on P4 and Q2 (red dotted); these dis-
tion F can fail to be ε-faithful while remaining well-typed          agreements are witnesses of drift. Two statements with identical
                                                                     fingerprints over a sufficiently rich probe set are provably equiva-
and (often) provable. Figure 2 visualizes the taxonomy
                                                                     lent (Theorem 4.2).
with an instance of each class.
These four classes account for 94% human-labeled drift in-           A fingerprint is computed by issuing entailment queries to
stances in our pilot study of 400 randomly sampled out-              the proof assistant. We use a bounded tactic budget per
puts from a state-of-the-art autoformalizer (Section 10); the        query (default exact? + aesop + a small library of
remainder fall into combinations or into the undetectable-           mathlib-aware closers, capped at 30 seconds wall-clock;
drift regime described in Section 8.                                 queries that neither succeed nor refute within budget are
                                                                     recorded as ?. We discuss the impact of incomplete ora-
                                                                     cles in Section 8.
4. Bidirectional Provability Fingerprinting
4.1. Provability fingerprints                                        4.2. Why bidirectional matters
Definition 4.1 (Provability fingerprint). Let F ∈ F and let          Forward-only fingerprints fail to distinguish a strict
P ⊆ F be a set of probes. The forward fingerprint of F               strengthening of N from N itself: a strictly stronger F en-

                                                                 3
                                       Certifying Faithfulness in LLM Autoformalization

tails everything N entails. Backward-only fingerprints du-            statement N , and a drifted twin N D , obtained by mechani-
ally fail to catch strict weakenings. Bidirectional matching          cally perturbing N in a way that induces drift class D (e.g.,
is the minimum sufficient signal.                                     swapping the order of two adjacent quantifiers or dropping
Proposition 4.2. Let F be a candidate for a set, N , and              a stated hypothesis). CPG then asks an LLM to produce
let P be a probe set closed under T -equivalence. Then                probes that distinguish N from N D : probes that should be
T ⊢ F ↔ N if and only if ΦF (P) = ΦN (P) and for each                 entailed by N but are not N D , or vice versa. The LLM is
pair (P, P ′ ) ∈ P 2 with T ⊢ P → P ′ , the entailment also           conditioned on the contrast itself, which empirically yields
holds in F ’s fingerprint.                                            probes sharply targeted at the drift class in question. For-
                                                                      mally, for drift class D, the probe distribution is
A proof appears in Section A.
                                                                      QD (P ) ∝ Pr[ P entailed by N ]·Pr[ P not entailed by N D ],
4.3. Algorithm                                                        estimated through an LLM scoring step. We sample kD
Algorithm 1 gives the full BPF procedure used in our ex-              probes per class, kD determined by APBA (Section 7).
periments.
                                                                      5.2. The role of negative drifted twins
Algorithm 1 Bidirectional Provability Fingerprinting
                                                                      A critical design choice is one that N D is generated me-
  Input: NL statement N , candidate F , theory T , budget             chanically, not by an LLM. Mechanical perturbation guar-
  k, tactic, budget τ                                                 antees the drift class label is unambiguous and that N D ex-
  Output: verdict, and witness probes V                               hibits exactly the targeted failure. LLM-generated drifted
  PN ← CPG.Generate(N, k) (§5)                                        twins, in contrast, frequently produce statements that are
    F
  PN   ← Autoformalize(PN )                                           either nonsense or accidentally drifted along multiple axes
    F                                F
  PN   ← FilterTypecheck(PN            )                              simultaneously, which destroys the contrastive signal.
  V←∅
               F
  for P ∈ PN     with label ℓ(P ) routed by APBA do
                                                                      5.3. Empirical effect
     if ℓ(P ) = + then
        if TryProve(F → P, τ ) = refuted then                         Figure 4 shows the detection rate of BPF specific CPG
           V ← V ∪ {(P, +)}                                           probes versus generic probes, as a function of probe budget.
        end if                                                        CPG reaches the same detection rate as generic probes at
     else if ℓ(P ) = − then                                           less than half the budget and outperforms generic probes at
        if TryProve(F → P, τ ) = proved then                          every budget level on three of the four drift classes.
           V ← V ∪ {(P, −)}
                                                                                            1
        end if
     end if
  end for                                                                                  0.8
                                                                          Detection rate




                                      F
  E ← ComputeSpectrum(V, PN             )
                                                                                                                            BPF + CPG
  return verdict by thresholding E, V                                                      0.6
                                                                                                                            BPF-naive
                                                                                                                            LLM-judge
                                                                                           0.4                            Back-translation

5. Counterfactual Probe Generation                                                               2   4   8          16        32             64
                                                                                                         Probe budget k
A naive probe generator samples specializations, general-
izations, and edge cases of N . This is the starting point,           Figure 4. Detection rate vs. probe budget on D RIFT B ENCH. CPG
but it leaves substantial information on the table: it does           reaches BPF-naive’s k = 32 performance at k ≈ 12. Budget for
not target the drift classes the certifier is trying to detect.       non-probe methods refers to comparable wall-clock equivalents.
We introduce Counterfactual Probe Generation (CPG), a
contrastive procedure that synthesizes probes designed to
maximally discriminate between faithful and drifted candi-            6. The Equivalence Spectrum
dates.                                                                Binary faithful/drifted verdicts are brittle. A fingerprint
                                                                      with one anomalous cell out of fifty is qualitatively differ-
5.1. Probe synthesis as contrastive generation                        ent from one with twenty. We introduce a continuous score
CPG treats probe generation as a contrastive problem. For             E(F, N ) ∈ [0, 1].
each drift class D ∈ {∆∀ , ∆H , ∆C , ∆T }, we construct               Definition 6.1 (Equivalence Spectrum). Let P be a probe
a counterfactual pair consisting of the natural-language              set with predicted labels ℓ : P → {+, −, ⊥} and class

                                                                  4
                                                     Certifying Faithfulness in LLM Autoformalization

weights w : {∆∀ , ∆H , ∆C , ∆T } → R>0 . The equivalence                        split). APBA samples the next probe from the class with
spectrum score is                                                               maximum IG, breaking ties by descending class weight.
                  P
                         w(DP ) · ⊮[ cellP (F ) ̸= ℓ(P ) ]                      The procedure is greedy but has the standard sublinear re-
 E(F, N ) = 1 − P ∈P         P                             ,                    gret guarantee for monotone submodular gain.
                                P ∈P w(DP )
                                                                                Theorem 7.1 (APBA budget reduction). Let k ⋆ be the bud-
where DP the drift class is targeted by the probe P and                         get required by uniform allocation to reach the detection
cellP (F ) is the observed fingerprint cell at P .                              rate ρ on D RIFT B ENCH. Then APBA reach the same ρ
E is calibrated against expert annotations on a held-out sub-                   with budget kAPBA ≤ k ⋆ /γ, where γ is the heterogeneity ra-
set D RIFT B ENCH to yield three decision regions: E ≥ 0.93                     tio of witnessability rates across drift classes? On D RIFT-
(ACCEPT), E ∈ [0.78, 0.93) (REVIEW), and E < 0.78                               B ENCH, γ ≈ 3.2.
(REJECT). Figure 5 shows the resulting distribution on
D RIFT B ENCH.                                                                  8. Theoretical Analysis
              40                                                                We now establish the two main theoretical results: a high-
                       Faithful REJECT                       REVIEWACCEPT
                                                                                probability detection theorem for each canonical drift class
              30       Drifted
                                                                                and a PAC-style learnability result for the equivalence class
    Density




              20                                                                of N .

              10
                                                                                8.1. Drift Detection Theorem
               0
                                                                                Theorem 8.1 (Drift Detection). Fix δ ∈ (0, 1) and drift
                   0         0.25             0.5          0.78   0.93 1
                                                                                class D ∈ {∆∀ , ∆H , ∆C , ∆T }. Let N be a natural-
                                         E(F, N ) score
                                                                                language statement and F a candidate formalization ex-
Figure 5. Empirical distribution of E(F, N ) on D RIFT B ENCH,                  hibiting drift of class D relative to every I in the support
separated by ground truth label. The dashed lines mark the cali-                of DN . Suppose the probe generator samples probes from
brated ACCEPT (E ≥ 0.93) and REVIEW (0.78 ≤ E < 0.93) thresh-                   a distribution QD such that
olds.
                                                                                                                         
                                                                                         Pr P witnesses D for (N, F ) ≥ α(D),
                                                                                      P ∼QD
Beyond a more informative output, E enables three down-
stream uses that a binary verdict precludes: (i) ranking mul-                   where α(D) ∈ (0, 1] is the witnessability rate for class D.
tiple candidates from an autoformalizer; (ii) triage of RE -                    Then, with the probe budget
VIEW -region candidates to human inspection; (iii) reward
shaping as a continuous signal for FGD (Section 9).                                                          1     1
                                                                                                    k ≥         log ,
                                                                                                           α(D)    δ
7. Adaptive Probe Budget Allocation                                             BPF flags F as drifted with probability at least 1 − δ,
BPF’s dominant cost is the entailment oracle. Allocating                        provided the entailment oracle is complete on the chosen
the probe budget uniformly across drift classes is waste-                       probes.
ful when some classes are easier to witness than others, or
when initial probes have already provided strong evidence.                      The proof is a standard coverage argument and is given
We introduce Adaptive Probe Budget Allocation (APBA),                           in Section A. The witnessability rates we estimate empir-
which routes budget by expected information gain.                               ically in Section 11 are α(∆∀ ) ≈ 0.62, α(∆H ) ≈ 0.55,
                                                                                α(∆C ) ≈ 0.48, α(∆T ) ≈ 0.31, meaning a budget of
                                                                                k = 32 probes is already given δ ≤ 0.01 for the first three
7.1. Information-theoretic routing
                                                                                classes.
Let H(F ) be the entropy of the posterior over F ’s drift
status given the probes drawn so far. APBA selects the next                     8.2. PAC-Faithfulness
probe to maximize expected reduction in H(F ), estimated
under a calibrated probability model for each drift class.                      The detection theorem says we can catch any specific drift;
Concretely, for drift class D with current posterior pD , the                   the stronger question is whether we can learn the full equiv-
expected information gain from a probe targeting D is                           alence class of N . We answer affirmatively under a polyno-
                                                                              mial query bound.
         IG(D) = H(pD ) − Er∼πD H(pD | r) ,
                                                                                Theorem 8.2 (PAC-Faithfulness). Let [N ]T denote the
where r is the predicted oracle outcome and πD is the em-                       equivalence class {F ∈ F : T ⊢ F ↔ N }. Assume
pirical witnessability distribution (estimated on a held-out                    CPG probes are drawn from a distribution Q such that

                                                                            5
                                            Certifying Faithfulness in LLM Autoformalization

for every F ∈  / [N ]T reachable by an LLM autoformal-                      split of D RIFT B ENCH, FGD reduces the rate of drifted
izer, PrP ∼Q [P witnesses F ’s drift] ≥ α0 > 0. Then with                   outputs from a state-of-the-art autoformalizer from 19.4%
k ≥ (1/α0 ) log(1/δε) probes, BPF produces a hypothesis                     to 10.3%, a 47% relative reduction. The bulk of the im-
Ĥ ⊆ F such that with probability at least 1 − δ,                           provement comes from re-prompting on ∆H and ∆C can-
                                                                          didates, where the witness probe gives the model a concrete
          Pr F ∈ Ĥ ⇐⇒ F ∈ [N ]T ≥ 1 − ε,                                   instance of the failure to repair.
        F ∼Dµ

where Dµ is the autoformalizer’s output distribution.
                                                                            10. The D RIFT B ENCH Benchmark
The proof, in Section A, recasts BPF as a hypothesis class
                                                                            D RIFT B ENCH contains 2,183 natural language/Lean 4
indexed by fingerprints and applies an Occam-style bound.
                                                                            pairs with controlled drift labels, drawn from six math-
Theorem 8.2 formalizes the operational claim: with a poly-
                                                                            lib4 subfields (analysis, algebra, topology, number the-
nomial probe budget, BPF learns to recognize the equiv-
                                                                            ory, combinatorics, and category theory). Each pair
alence class of N up to error ε over the autoformalizer’s
                                                                            carries: (i) a natural-language statement, (ii) a can-
output distribution.
                                                                            didate Lean 4 formalization, (iii) a drift label in
                                                                            {faithful, ∆∀ , ∆H , ∆C , ∆T , combined}, and (iv) an expert-
8.3. Incomplete oracle and undetectable drift                               verified gold formalization. Table 1 summarizes the com-
Lean’s tactic stack is incomplete: some true entailments                    position.
will not be closed within τ seconds. Let η(τ ) be the prob-
ability that the oracle returns ? on a probe that admits a τ -              Table 1. Composition of D RIFT B ENCH by subfield and drift class.
cost proof. The detection bound degrades to 1 − δ − kη(τ );
                                                                              Subfield        Faith.    ∆∀    ∆H      ∆C     ∆T     Comb.
empirically η(30s) ≈ 0.07 on D RIFT B ENCH probes. BPF
cannot detect a class we call convention drift: F adopts a                    Analysis          198     64      71     58     33        31
                                                                              Algebra           173     51      68     49     28        27
notational convention different from N ’s, but every probe                    Topology          162     49      59     47     30        25
responds identically because the convention is invisible to                   Number Th.        144     42      55     41     22        22
provability. We give a structural test for it in Section B.                   Combinator.       138     43      51     39     24        21
                                                                              Category          117     35      44     33     19        19

9. Faithfulness-Guided Decoding                                               Total             932    284     348    267    156       145

BPF is most valuable as a post-hoc verifier, but it also pro-
                                                                            We use deterministic perturbation rules rather than sam-
vides a signal that can be plugged back into autoformal-
                                                                            pling drift from an LLM autoformalizer so that the drift la-
ization itself. We introduce Faithfulness-Guided Decoding
                                                                            bel is unambiguous. A complementary wild split contains
(FGD), a procedure that uses E as a reward during sample-
                                                                            384 pairs where the candidate was generated by an LLM
and-rerank decoding (Figure 6).
                                                                            autoformalizer and the drift label was independently anno-
                           Autoformalizer              Candidates
                                                                            tated by two experts (κ = 0.81). We report results on both
        NL N                   (LLM) w/ witness probe F1 , . . . , Fm
                              re-prompt                                     splits.


      Output F ∗
                             Rerank +                      BPF              11. Experiments
                               top-1                     E scoring
                                                                            11.1. Setup
Figure 6. Faithfulness-Guided Decoding (FGD). The autofor-
malizer samples m candidates; BPF scores each by E; the top-                Models. For the natural-language probe generator and
ranked candidate F ∗ is returned. If all candidates fall in the RE -        adversarial paraphraser, we use a strong instruction-tuned
VIEW or REJECT region, the highest-scoring witness probe is fed
                                                                            LLM and report results on Llama-34B (Azerbayev et al.,
back as an in-context repair hint (red dashed loop).
                                                                            2024) and a closed-weights frontier model; results are qual-
                                                                            itatively similar. For autoformalization of probes, we use
Algorithm. Given N , the autoformalizer samples m can-                      Llama-34B fine-tuned on mathlib4 with retrieval aug-
didate formalizations F1 , . . . , Fm . For each candidate,                 mentation. The entailment oracle is Lean 4 + mathlib4
FGD computes a low-budget E score (k = 8 probes per                         with the tactic budget described in Section 4. Baselines:
class) and reranks by score. The top-ranked candidate                       Typecheck: flag drift iff F fails to typecheck. Provabil-
is returned. Optionally, candidates with E < 0.78 trig-                     ity: flag drift iff F is unprovable within the tactic budget.
ger a re-prompt with the highest-scoring witness probe at-                  BLEU-ref: flag drift iff BLEU against the gold formaliza-
tached as an in-context hint, biasing the autoformalizer                    tion is below a threshold. Back-translation: Autoformal-
away from the detected drift class. Effect on a held-out                    ize F back to NL and compare to N (Patel et al., 2024).

                                                                        6
                                                             Certifying Faithfulness in LLM Autoformalization

LLM-judge: ask a frontier LLM to directly judge faith-                                              Table 3. Detection rate by drift class (at 3% FPR overall).
fulness from (N, F ). BPF-naive: BPF with generic (not
                                                                                                                             Method                 ∆∀         ∆H          ∆C          ∆T
counterfactual) probes.
                                                                                                                             Typecheck              0.07       0.05        0.04        0.31
                                                                                                                             Provability            0.46       0.62        0.33        0.18
11.2. Main results                                                                                                           Back-translation       0.66       0.61        0.59        0.40
                                                                                                                             LLM-judge              0.74       0.67        0.64        0.42
Table 2 summarizes performance on the controlled D RIFT-                                                                     BPF-naive              0.89       0.88        0.84        0.55
B ENCH split and Figure 7 shows ROC curves for the four                                                                      BPF + CPG              0.94       0.93        0.91        0.66
strongest methods.

Table 2. Drift detection on the controlled D RIFT B ENCH split.                                                                       Provability   Back-tr.     LLM-judge             BPF+CPG

Det@3%FPR is the detection rate at a 3% false-positive rate.
                                                                                                                              1
  Method                                     F1     Det@3%FPR            FPR          Cost
                                                                                                                            0.8




                                                                                                           Detection rate
  Typecheck only                             0.27         0.114         0.020 1×
  Provability                                0.42         0.412         0.030 18×                                           0.6
  BLEU-ref                                   0.55         0.301         0.030 1×                                            0.4
  Back-translation                           0.66         0.589         0.030 4×
  LLM-judge                                  0.71         0.633         0.030 2×                                            0.2
  BPF-naive                                  0.85         0.832         0.031 22×
  BPF + CPG                                  0.91         0.896         0.030 26×                                             0
  BPF + CPG + APBA                           0.91         0.894         0.031 8×                                                      ∆∀            ∆H                ∆C                ∆T

                                                                                                 Figure 8. Per-class detection. BPF + CPG dominates across all
                         1                                                                       four drift classes; the gap on ∆T (type coercion) is the smallest,
                                                                                                 consistent with its lower witnessability rate α(∆T ) ≈ 0.31.
                        0.8
   True-positive rate




                        0.6                                                                      close most of the residual gap.
                        0.4                                          BPF + CPG
                                                                     BPF-naive                   11.4. Probe budget scaling
                        0.2                                          LLM-judge
                                                                   Back-translation              Figure 9 shows detection rate as a function of probe bud-
                         0
                              0   5 · 10−2    0.1         0.15        0.2             0.25       get under uniform allocation versus APBA. Uniform allo-
                                             False-positive rate
                                                                                                 cation requires k ≈ 28 probes to reach 0.87 the detection
                                                                                                 rate; APBA reaches the same rate at k ≈ 9, a 3.1× reduc-
Figure 7. ROC curves on the controlled D RIFT B ENCH split.                                      tion matching the theoretical prediction of Theorem 7.1.
BPF + CPG dominates other methods uniformly across operating
points; AUC = 0.962 vs. 0.938 for BPF-naive and 0.879 for LLM-                                                               1
judge.
                                                                                                                                                                3.1×
                                                                                                     Detection rate




                                                                                                                            0.8
BPF + CPG reduces the residual error rate of the best
non-fingerprinting baseline (LLM-judge) by approximately                                                                    0.6
72%, the matched FPR. Adding APBA preserves detection                                                                                                                      APBA (adaptive)
performance while reducing wall-clock cost by 3.2×, con-                                                                    0.4
                                                                                                                                                                           Uniform allocation

firming Theorem 7.1. Table 3 and Figure 8 report per-class                                                                        2        4          8          16               32             64
breakdowns; the type-coercion class (∆T ) is the hardest for                                                                                         Probe budget k
every method but CPG closes a substantial portion of the
gap.                                                                                             Figure 9. Probe budget scaling. APBA reaches ρ = 0.87 at k ≈
                                                                                                 9; uniform allocation requires k ≈ 28, matching Theorem 7.1’s
                                                                                                 prediction of γ ≈ 3.2.
11.3. Wild split
On the 384 pair-wise split, BPF + CPG agrees with expert
                                                                                                 11.5. Ablations
annotators κ = 0.77 (cf. inter-annotator κ = 0.81), versus
κ = 0.58 for LLM-judges. A breakdown of BPF’s false                                              We ablate BPF + CPG components in Table 4 and Fig-
positives shows that 63% trace to incomplete entailment-                                         ure 10. Removing bidirectional matching (forward-only)
oracle outputs that flipped a fingerprint cell, not funda-                                       costs 11 F1 points, confirming Theorem 4.2. Removing
mental probe-generation errors—suggesting that integrat-                                         CPG (replacing it with generic probes) costs 6 points. Re-
ing stronger hammers (Czajka & Kaliszyk, 2018) would                                             moving hypothesis-drop probes costs 9 points, almost all

                                                                                             7
                                                                         Certifying Faithfulness in LLM Autoformalization

on ∆H .                                                                                                           the probe generator’s labels are correct. We treat both as
                                                                                                                  engineering boundaries: convention drift is addressed by
          Table 4. Ablations of BPF + CPG on the controlled split.
                                                                                                                  a separate structural check (Section B), and probe labels
                                  Variant                                               F1                        are calibrated against expert annotation on a held-out set.
                                                                                                                  The PAC-Faithfulness theorem (Theorem 8.2) bounds the
                                  Full BPF + CPG                                    0.91
                                    – counterfactual probes (CPG)                   0.85                          cumulative effect of probe-label noise. (i). Compute: The
                                    – bidirectional (forward only)                  0.80                          dominant cost is the entailment oracle. We see two paths to
                                    – hypothesis-drop probes                        0.82                          bringing this down: (i) caching fingerprints for canonical
                                    – boundary probes                               0.88                          statements in mathlib4 and reusing them, and (ii) replac-
                                    – adversarial probes                            0.87                          ing the per-query proof search with a learned entailment
                                    probe budget k = 8 (vs. 32)                     0.83
                                    probe budget k = 8 + APBA                       0.89                          classifier whose errors are bounded by occasional formal
                                                                                                                  verification.

   Full BPF + CPG                                                                                   0.91          APBA (Section 7) already provides a 3.2× practical speed-
    k = 8+APBA                                                                               0.89                 up. (ii). Sociotechnical risk: If BPF-certified statements
 − boundary probes                                                                      0.88                      are treated as ground truth without expert review, resid-
               − adv. probes                                                      0.87                            ual drift—especially convention drift—could contaminate
                             − CPG                                         0.85                                   libraries. BPF should be deployed as a triage tool that pri-
 − hyp-drop probes                                               0.82                                             oritizes expert review, not a replacement for it. The Equiv-
                         forward-only                    0.8                                                      alence Spectrum’s REVIEW band is explicitly designed
            k = 8 uniform                                           0.83                                          for this purpose. (iii). Cross-system generality: While
                                        0.75          0.8               0.85                 0.9           0.95   our experiments focus on Lean 4, the BPF framework is
                                                               F1 on controlled split                             system-agnostic: it requires only an entailment oracle and
Figure 10. Ablation deltas. CPG and bidirectional matching are                                                    a probe-generation procedure. Preliminary experiments on
the two largest individual contributors; APBA preserves perfor-                                                   Isabelle/HOL show comparable detection rates (F 1 = 0.88
mance even at a low budget.                                                                                       vs. 0.91 on Lean 4), suggesting fingerprints transfer across
                                                                                                                  formal systems.
11.6. FGD downstream impact
                                                                                                                  13. Conclusion
We evaluate FGD as a wrapper around a state-of-the-art
autoformalizer on the wild split, comparing drift rate with                                                       We introduced Bidirectional Provability Fingerprinting, a
and without FGD as a function of the number of candidates                                                         framework for certifying faithfulness in autoformalization
m (Figure 11). The autoformalizer’s baseline drift rate is                                                        that requires no reference formalization, along with four
19.4%. With m = 4 drift falls to 10.3%; with m = 8, to                                                            supporting innovations: counterfactual probe generation,
8.7%.                                                                                                             the equivalence spectrum, adaptive budget allocation, and
                                                                                                                  faithfulness-guided decoding. We proved a drift-detection
                            0.2                                         FGD (rerank + re-prompt)                  theorem and a PAC-faithfulness theorem characterizing
   Drifted-output rate




                                                                        Rerank only (no re-prompt)
                                                                                                                  what is and is not detectable, released D RIFT B ENCH as
                                                                         Baseline autoformalizer
                           0.15                                                                                   the first benchmark with controlled drift labels; and demon-
                                                                                                                  strated substantial gains over typecheck, BLEU, back-
                            0.1                                                                                   translation, and LLM-judge baselines. We see the faith-
                                                                                                                  fulness gap as the bottleneck for trustworthy autoformal-
                                  1     2      4                8                                     16          ization at the scale of full mathematical libraries and the
                                               Number of candidates m per statement                               techniques in this paper as a concrete step toward closing
                                                                                                                  it.
Figure 11. FGD reduces drifted-output rate from 19.4% to 10.3%
at m = 4. The re-prompt component contributes most of the im-
provement at small m; pure reranking saturates at ∼ 14%.                                                          Impact Statement
                                                                                                                  This work aims to advance machine learning by improving
12. Discussion and Limitations                                                                                    the reliability of AI-assisted formal mathematics. We do
                                                                                                                  not anticipate direct negative societal impacts. However,
What BPF does it not solve? BPF certifies that the con-                                                           as discussed in Section 12, uncritical use of a faithfulness
sequence neighborhood F matches the consequence neigh-                                                            certifier could propagate subtle errors into formal libraries
borhood predicted from N . It does not certify that N it-                                                         that may later be treated as ground truth.
self is unambiguous (convention drift; Section 8) or that

                                                                                                             8
                                      Certifying Faithfulness in LLM Autoformalization

References                                                           Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A.,
                                                                       Hayat, A., Lavril, T., Ebner, G., and Martinet, X. Hy-
Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,
                                                                       perTree proof search for neural theorem proving. In
  H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., and
                                                                       Advances in Neural Information Processing Systems
  Sutton, C. Program synthesis with large language mod-
                                                                       (NeurIPS), pp. 26337–26349, 2022.
  els. arXiv preprint arXiv:2108.07732, 2021.
                                                                     Langley, P. Crafting papers on machine learning. In Pro-
Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers,
                                                                       ceedings of the 17th International Conference on Ma-
  E. W., Radev, D., and Avigad, J. ProofNet: Autoformal-
                                                                       chine Learning (ICML), pp. 1207–1216, 2000.
  izing and formally proving undergraduate-level mathe-
  matics. In Workshop on Mathematical Reasoning and                  Liu, C., Shen, J., Xin, H., Liu, Z., Yuan, Y., Wang, H., Ju,
 AI at NeurIPS, 2023.                                                  W., He, C., Jiang, J., Li, Z., and Liang, X. FIMO: A
                                                                       challenge formal dataset for automated theorem proving.
Azerbayev, Z., Schoelkopf, H., Paster, K., Dos Santos, M.,             In arXiv preprint arXiv:2309.04295, 2023.
  McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and
  Welleck, S. Llemma: An open language model for math-               Patel, A., Reddy, S., and Bahdanau, D. New symbol gener-
  ematics. In International Conference on Learning Rep-                alization and faithfulness in autoformalization. In Work-
  resentations (ICLR), 2024.                                           shop on AI for Math at ICML, 2024.

Brandom, R. B. Articulating Reasons: An Introduction to              Polu, S. and Sutskever, I. Generative language model-
  Inferentialism. Harvard University Press, 2000.                      ing for automated theorem proving. arXiv preprint
                                                                       arXiv:2009.03393, 2020.
Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto,
  H. P., Kaplan, J., Edwards, H., Burda, Y., Joseph, N.,             Prawitz, D. Natural Deduction: A Proof-Theoretical Study.
  Brockman, G., et al. Evaluating large language models                Almqvist & Wiksell, 1965.
  trained on code. arXiv preprint arXiv:2107.03374, 2021.            Szegedy, C. A promising path towards autoformalization
Czajka, Ł. and Kaliszyk, C. Hammer for Coq: Automa-                    and general artificial intelligence. Intelligent Computer
  tion for dependent type theory. Journal of Automated                 Mathematics (CICM), pp. 3–20, 2020.
  Reasoning, 61(1):423–453, 2018.                                    The mathlib Community. The Lean mathematical library.
de Moura, L. and Ullrich, S. The Lean 4 theorem prover                 In Proceedings of the 9th ACM SIGPLAN International
  and programming language. In International Conference                Conference on Certified Programs and Proofs (CPP), pp.
  on Automated Deduction (CADE), pp. 625–635, 2021.                    367–381, 2020.
                                                                     Wang, Q., Kaliszyk, C., and Urban, J. First experiments
First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:
                                                                      with neural translation of informal to formal mathemat-
  Whole-proof generation and repair with large language
                                                                      ics. Intelligent Computer Mathematics (CICM), pp. 255–
  models. In Proceedings of the 31st ACM Joint European
                                                                      270, 2018.
  Software Engineering Conference and Symposium on the
  Foundations of Software Engineering (ESEC/FSE), pp.                Welleck, S., Liu, J., Lu, X., Hajishirzi, H., and Choi, Y.
  1229–1241, 2023.                                                    NaturalProver: Grounded mathematical proof genera-
                                                                      tion with language models. In Advances in Neural In-
Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S.
                                                                      formation Processing Systems (NeurIPS), 2022.
  Proof artifact co-training for theorem proving with lan-
  guage models. In International Conference on Learning              Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
  Representations (ICLR), 2022.                                       nik, M., and Szegedy, C. Autoformalization with large
                                                                      language models. In Advances in Neural Information
Jiang, A. Q., Li, W., Tworkowski, S., Czechowski, K.,                 Processing Systems (NeurIPS), pp. 32353–32368, 2022.
   Odrzygóźdź, T., Miłoś, P., Wu, Y., and Jamnik, M. Thor:
   Wielding hammers to integrate language models and au-             Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song, P.,
   tomated theorem provers. In Advances in Neural Infor-               Yu, S., Godil, S., Prenger, R., and Anandkumar, A. Le-
   mation Processing Systems (NeurIPS), pp. 8360–8373,                 anDojo: Theorem proving with retrieval-augmented lan-
   2022.                                                               guage models. In Advances in Neural Information Pro-
                                                                       cessing Systems (NeurIPS), 2023.
Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jam-
   nik, M., Lacroix, T., Wu, Y., and Lample, G. Draft,               Zheng, K., Han, J. M., and Polu, S. MiniF2F: A cross-
   sketch, and prove: Guiding formal theorem provers with              system benchmark for formal olympiad-level mathemat-
   informal proofs. In International Conference on Learn-              ics. In International Conference on Learning Represen-
   ing Representations (ICLR), 2023.                                   tations (ICLR), 2022.

                                                                 9
                                      Certifying Faithfulness in LLM Autoformalization

A. Proofs
A motivating example. Consider the natural-language statement: “Every continuous function on a compact set attains
its maximum.” Three Lean 4 formalizations are syntactically plausible:
 -- (A) Faithful
 theorem evt_A {K : Set R} (hK : IsCompact K)
     (hne: K.Nonempty) {f : R -> R}
     (hf: ContinuousOn f K) :
     exists x in K, forall y in K, f y <= f x


 -- (B) Hypothesis omission: missing nonempty
 theorem evt_B {K : Set R} (hK : IsCompact K)
     {f : R -> R} (hf : ContinuousOn f K) :
     exists x in K, forall y in K, f y <= f x


 -- (C) Quantifier inversion: silently true
 theorem evt_C {K : Set R} (hK : IsCompact K)
     (hne: K.Nonempty) {f : R -> R}
     (hf: ContinuousOn f K) :
     forall y in K, exists x in K, f y <= f x


All three typecheck. Only (A) is faithful: (B) is false on the empty set; (C) is trivially true (take x = y) and is unrelated to
the Extreme Value Theorem. Critically, a downstream prover that closes either (A) or (C) provides no signal distinguish-
ing them, and (C) is the type of failure most likely to occur in practice precisely because it remains provable. Current
autoformalization pipelines accept all three as valid outputs. Why this matters now: As autoformalization scales toward
populating libraries such as mathlib4 (The mathlib Community, 2020) with LLM-produced statements, faithfulness errors
propagate. A theorem with a silently weakened hypothesis becomes a usable lemma for downstream proofs that should not
exist; a quantifier-inverted statement becomes a trivial fact mistakenly cited as a deep one. Existing benchmarks-miniF2F
(Zheng et al., 2022), ProofNet (Azerbayev et al., 2023), LeanDojo (Yang et al., 2023)-all measure proving capability condi-
tional on the formal statement being correct, so the upstream error is invisible to them. Our pilot study (Section 10) found
that 19% formalizations produced by a state-of-the-art autoformalizer on graduate-level analysis exhibit at least one form
of semantic drift.

A.1. Proof of Theorem 4.2
(⇒) If T ⊢ F ↔ N , then for every P we have T ⊢ F → P iff T ⊢ N → P , so Φ+                     +
                                                                                     F (P) = ΦN (P); similarly for the
backward direction. (⇐) Suppose ΦF (P) = ΦN (P) and the additional closure condition holds, but T ⊬ F ↔ N . WLOG
T ⊬ F → N (the other case is symmetric). By the closure assumption on P under T -equivalence, N ∈ P (or some
T -equivalent of N is). Then N ∈ Φ+                      / Φ+
                                  N (P) trivially, but N ∈  F (P), contradicting fingerprint equality.              □

A.2. Proof of Theorem 8.1
For a given drift class D, let WP be the indicator that the probe P ∼ QD witnesses D for (N, F ). By assumption
E[WP ] ≥ α(D). Drawing k probes i.i.d., the probability that none witness D is at most (1 − α(D))k ≤ e−kα(D) . Setting
this to δ gives k ≥ α(D)−1 log(1/δ). If the entailment oracle is complete on each chosen probe, every witness probe will
be detected by BPF, so the failure probability is bounded by δ. If instead each probe has an independent oracle failure
probability η(τ ), by a union bound, the total failure probability is at most δ + kη(τ ).                            □

A.3. Proof of Theorem 8.2
Define a hypothesis class H = {HΦ : Φ ∈ 2P×{+,−} }, where HΦ = {F ∈ F : ΦF (P) = Φ}. Given k probes, |H| ≤ 4k
(each cell is in {0, 1}2 ). Each candidate F ∈
                                             / [N ]T that is reachable by the autoformalizer has, by assumption, probability
at least α0 of being witnessed by each probe in Q. Thus, with k ≥ (1/α0 ) log(1/δε) probes, the probability that any such
F is consistent with Ĥ is at most (1 − α0 )k ≤ δε. Applying an Occam-style bound over the hypothesis class with size 4k ,
and noting that log |H| ≤ 2k is dominated by the chosen k, gives the stated bound.                                        □

A.4. Proof of Theorem 7.1
Let α = (α(∆∀ ), . . . , α(∆T )) be the witnessability rates and w the class weights. Uniform allocation sam-
ples each class with probability 1/4; APBA samples class D in proportion to α(D)w(D). The expected num-

                                                              10
                                     Certifying Faithfulness in LLM Autoformalization
                                                                                                      P
                                   is 1/ᾱunif for uniform and 1/ᾱapba for APBA, where ᾱunif = (1/4) D α(D)
ber of probes toPwitness any drift P
and ᾱapba = ( D α(D)w(D))2 / D α(D)2 w(D)2 . The ratio is the heterogeneity factor γ, bounded below by
maxD α(D)/ minD α(D) when weights are equal. On D RIFT B ENCH, maxD α(D)/ minD α(D) ≈ 2.0, and with cali-
brated weights γ ≈ 3.2.                                                                                    □

B. Structural Test for Convention Drift
Convention drift, by definition, leaves the consequence neighborhood invariant on standard probes. We address it through
a structural test on the type signature of F , comparing it to a canonical-signature prediction derived from N . Given N , the
canonical-signature predictor returns a tuple (ΣN , KN ) where the first element ΣN is the expected type signature (with
universe levels and implicit arguments) and the second element KN is a set of structural keywords (e.g. Set, Finset,
Function, Pi) expected to appear. We then compare against the type signature of F : Compute the structural diff ∆Σ =
ΣF △ΣN . Flag convention drift if |∆Σ| exceeds a calibrated threshold but BPF returns FAITHFUL. In our experiments, this
structural test catches an additional 0.04 F1 worth of convention-drift cases on the wild split. We view it as complementary
to, not a substitute for, the main BPF procedure.

C. Case Studies
We summarize three case studies from the wild split; full Lean 4 code is in the supplementary materials. Case 1 (Banach–
Steinhaus, ∆∀ ): Natural-language statement: “Let (Ti ) be a family of bounded operators on a Banach space X such
that for every x ∈ X, supi ∥Ti x∥ < ∞. Then supi ∥Ti ∥ < ∞.” The candidate swapped the order of quantifiers in the
conclusion. BPF generated a specialization probe instantiating X = ℓ2 and a specific bounded family for which pointwise
boundedness holds, but the swapped conclusion fails; the entailment F → P is closed, flagging drift. The CPG probe
targeting ∆∀ recovered the witness with a 4-probe budget, where naive sampling was required 19. Case 2 (Continuity,
∆H ): Natural-language statement: ”A function continuous on a closed interval is uniformly continuous on that interval.”
The candidate dropped the closedness hypothesis. A hypothesis-dropping probe instantiating f (x) = 1/x on (0, 1) the
candidate refuted it. BPF flagged drift and FGD repaired the candidate on re-prompting. Case 3 (Convention drift,
undetected): Natural-language statement: ”Every group homomorphism with a trivial kernel is injective.” The candidate
formalized the group as a monoid (since group axioms beyond monoid structure are not used in the statement). BPF
returns FAITHFUL because every probe is preserved; the structural test of Section B flags the Monoid/Group mismatch.

D. Probe-Generation Prompts
We include exact prompts used for the LLM-based probe generator. Each prompt is parameterized by the natural-language
statement and constrained to emit a JSON-structured list of probe candidates with predicted labels. The full prompt suite,
along with the system prompts and few-shot exemplars, is included in the supplementary materials.

E. Hyperparameters

                       Hyperparameter                         Value
                       Probe budget k                         32 (uniform) / 10 (APBA)
                       Tactic budget τ                        30 s wall-clock
                       E accept threshold                     0.93
                       E review threshold                     0.78
                       Probe-class weights w                  equal across {∆∀ , ∆H , ∆C }, 1.5× for ∆T
                       Adversarial probes per statement       4
                       Specialization probes per statement    8
                       Hypothesis-drop probes per statement   up to 8
                       Boundary probes per statement          4
                       FGD candidates m                       4 (default) / 8 (high-budget)




                                                              11
