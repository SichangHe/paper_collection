                                                                    Reasoning without Gold Standards:
                                                                A Proxy-Judge Theory of Autoformalization
                                                                  Lei Xu1,2 Xin Quan1 André Freitas1,3,4
                                                                      1
                                                                        Idiap Research Institute, Switzerland
                                                        2
                                                          École Polytechnique Fédérale de Lausanne (EPFL), Switzerland
                                                 3
                                                   Department of Computer Science, University of Manchester, United Kingdom
                                                4
                                                  CRUK National Biomarker Centre, University of Manchester, United Kingdom
                                                          {lei.xu, xin.quan, andre.freitas}@idiap.ch

                                                              Abstract                               vides a reference output, and predictions are judged
                                                                                                     by comparison to it. For highly specialized do-
                                            Complex reasoning tasks increasingly require
                                                                                                     mains such as mathematics and formal logic, this
arXiv:2606.09449v1 [cs.CL] 8 Jun 2026




                                            systems to produce outputs whose correctness
                                            cannot be judged by exact match against a                assumption breaks once complexity scales, since
                                            single reference. Autoformalization (AF) is              constructing a reference may itself require solv-
                                            a representative example; it asks a model to             ing the task: choosing a representation, recover-
                                            translate informal mathematical or logical rea-          ing implicit assumptions, resolving notation and
                                            soning into a formally checkable object, yet             background facts, and certifying coherence inside
                                            expert-validated formalizations do not scale             a larger theory (Wu et al., 2022; Jiang et al., 2023;
                                            beyond toy cases and a single informal argu-
                                                                                                     Azerbayev et al., 2023). Beyond toy cases, gold-
                                            ment can admit many valid formal renderings.
                                            Progress therefore depends on whether partial,
                                                                                                     standard annotation is therefore not only expensive
                                            structured proxies can substitute for exact ref-         but can also become fundamentally non-scalable.
                                            erences.                                                    The difficulty is compounded by non-uniqueness.
                                            We introduce a reference-free proxy-judge                A single informal argument can admit many valid
                                            framework for AF that replaces gold-standard             renderings, differing in definitions, encodings,
                                            matching with a vector of per-axis property              lemma decompositions, proof strategies, or library
                                            checks. The framework organizes the proxy                alignments (Zhang et al., 2025). Any one gold stan-
                                            along three structural scopes that cover global          dard captures only one point in this equivalence
                                            properties of the elicited object, per-module            class, so exact-match evaluation can penalize cor-
                                            properties internal to its sub-components, and           rect alternatives while collapsing distinct kinds of
                                            cross-domain properties that re-align it to the
                                                                                                     errors into a single score.
                                            informal source, and aggregates each axis into
                                            a verdict vector. The vector drives a reflective            This creates a scalability dilemma: the tasks
                                            refinement loop in which a violated coordinate           most worth evaluating are also those for which ex-
                                            routes the controller to a matching repair target,       haustive expert annotation is least feasible. Evalua-
                                            so each iteration changes only what is judged            tion must therefore move from reference reproduc-
                                            wrong.                                                   tion to structured evidence of correctness. Instead
                                            Under bounded judge noise, the expected in-              of asking whether a candidate matches a canonical
                                            trinsic gap contracts geometrically to a noise-          solution, we ask whether it satisfies localized, task-
                                            dependent plateau. Across seven formalization            internal constraints that provide proxy evidence of
                                            backbones on miniF2F, ProofNet, e-SNLI, and              correctness without requiring a complete expert
                                            ProntoQA, refinement consistently lifts Pass
                                                                                                     reference for every instance.
                                            Rate over the single-shot ICL baseline, and the
                                            per-axis proxy outperforms a matched scalar                 Autoformalization (AF) is a representative case
                                            proxy on benchmarks where the baseline has               in which this dilemma is especially sharp. AF asks
                                            room to improve. Structured proxy judgments              a model to translate an informal mathematical or
                                            therefore provide both a practical refinement            logical argument into a formally checkable object
                                            signal and a theoretical handle on convergence           (Wu et al., 2022; Jiang et al., 2023; Azerbayev et al.,
                                            when exact references are unavailable.                   2023). A proof assistant can reject malformed syn-
                                                                                                     tax, inconsistent types, broken bindings, and failed
                                        1   Introduction
                                                                                                     elaborations (Polu and Sutskever, 2020; Yang et al.,
                                        Reasoning benchmarks often assume that correct-              2023); however, the kernel alone cannot decide
                                        ness can be specified in advance: an expert pro-             whether the formal artifact preserves the intended

                                                                                                 1
                                                                          +monotonic improvement: 𝜃𝑖

                     Autoformalization Π𝜃𝑖 (𝑛𝑙𝑖 , Γ)
                                                                          +coverage: {𝑛𝑙, 𝑁𝐿}                               judges can stand in for human evaluation in formal
                                                                             Reflective refinement
Informal (NL)                                                                   Refine 𝜃𝑖+1 , 𝜋𝑡𝑖
                                                                                                                            mathematical reasoning (Zhang et al., 2025; Zheng
     {𝑛𝑙𝑖 }
                Outline   Definition     Library     Formal                                                                 et al., 2023), and that step-level verifiers outper-
                 𝜋𝑜𝑢𝑡       𝜋𝑑𝑒𝑓           𝜋𝑙𝑖𝑏       𝜋𝑓𝑚𝑙
                                                                                  Localize 𝑡𝑖                               form outcome-only scalars for learned reasoning
    𝒦ℬ                             𝑃෡𝑖                                                                                      signals (Lightman et al., 2024; Uesato et al., 2022).
                                                                 iteration 𝑖
                                                                                                                            Both observations fit a reflective refinement loop
                                                               + Syntactically correct
                                                   Epistemic
                                                    Judges       + Binding integrity                   Formal: {𝑃෡𝑖 }       that proposes a candidate, measures its properties,
                                                       Ξ
                                                                         …
                                                                                                                            localizes a violation, and repairs it (see Figure 1);
Figure 1: Reflective Refinement Loop. At each iteration                                                                     we analyze the convergence properties of this loop
the system proposes a candidate formalization, scores it                                                                    when the judges themselves are imperfect.
on a fixed set of property axes, finds the worst-scoring                                                                       In summary, the contributions are organized as
axis, and applies a repair targeted to that axis.                                                                           follows.
                                                                                                                             1. Framework. We design a reference-free frame-
                                                                                                                                work for autoformalization that decomposes
meaning of the informal source (Zhang et al., 2025).
                                                                                                                                evaluation into audit-unit axes spanning three
At the same time, obtaining expert-written formal-
                                                                                                                                structural scopes—global, per-module, and
izations at scale is prohibitive, and treating one
                                                                                                                                cross-domain to the informal source—and
formalization as the unique reference is conceptu-
                                                                                                                                closes the loop with a prover-grounded re-
ally wrong because many correct formal renderings
                                                                                                                                turn policy, casting refinement as constraint-
may exist.
                                                                                                                                directed optimization in which each violation
   The key observation of this paper is that AF is                                                                              maps to an identifiable repair target (Section 3).
globally hard to annotate but locally amenable to
systematic assessment once the linguistic and rea-                                                                          2. Convergence analysis. Under a drift assump-
soning properties have been made explicit. The                                                                                 tion that we adopt as a primitive of the analysis
signal that drives evaluation already exists inside                                                                            (Assumption 2, with microscopic motivation in
the formal system itself. Once an argument is ren-                                                                             Section B), we give a drift-Lyapunov argument
dered as explicit statements, inferential links, and                                                                           showing the expected intrinsic gap contracts
grounding into a shared context, correctness de-                                                                               geometrically to an O(η) plateau (Theorem 1);
composes into finitely many locally checkable con-                                                                             the bound targets the asymptotic gap height,
straints whose violations admit bounded, targeted                                                                              while concurrent work on LLM-verifier loops
repair. AF is therefore hard to verify globally but                                                                            (Dantas et al., 2025) bounds expected iteration
easy to verify locally once it is made explicit, and                                                                           count.
this asymmetry is what we exploit.                                                                                          3. Empirical result. We evaluate seven formaliza-
   Building on this observation, we introduce a                                                                                tion backbones on four datasets, and our refine-
reference-free proxy-judge framework for AF. The                                                                               ment loop consistently outperforms the single-
framework decomposes evaluation into audit-unit                                                                                shot ICL baseline; on the frontier backbones,
axes organized by three structural scopes: global                                                                              average gains reach 19% on ProofNet and 16%
properties of the elicited object, per-module prop-                                                                            on e-SNLI. Within the loop, pass rate further
erties internal to its sub-components, and cross-                                                                              rises by 8.2–8.4% on ProofNet and 17–18%
domain properties that align it back to the infor-                                                                             on e-SNLI when we replace a single end-to-
mal source and the per-instance fact context. The                                                                              end judge with a per-axis proxy. The granular-
resulting verdict vector drives a reflective refine-                                                                           ity gain captures a sizeable share of the loop’s
ment loop in which each detected violation routes                                                                              overall gain over the ICL baseline on these two
the controller toward a localized repair, turning re-                                                                          benchmarks (15–21% on ProofNet, 2–25% on
finement into constraint-directed repair rather than                                                                           e-SNLI), which indicates that structured per-
undifferentiated retry.                                                                                                        axis feedback, rather than raw refinement com-
   From this local-verifiability gap, we decompose                                                                             pute, is the main source of the empirical advan-
AF evaluation into a finite vector of intrinsic prop-                                                                          tage (Section 5.6).
erties drawn from the language and inference sys-
                                                                                                                            2   Related Work
tem itself, and estimate that vector with a family
of specialized judges acting on small, controlled                                                                           Autoformalization and neural theorem proving.
contexts. Recent work shows that calibrated LLM                                                                             LLM-guided autoformalization (Wu et al., 2022;

                                                                                                                        2
Jiang et al., 2023; Azerbayev et al., 2023) and neu-         at hand, such as “a violin is an instrument”. We
ral proof search (Polu and Sutskever, 2020; Zheng            write Pbi for the iteration-i candidate and Pb⋆ for a
et al., 2022; Yang et al., 2023) use proof assis-            correct elicited target, both living in the ambient
tants as a binary success signal. Reference-free             space E; Γ remains fixed across iterations.
iterative refinement was recently formalized for                Because the same nl admits many valid formal-
full-theorem AF with four scalar acceptance crite-           izations, exact-match scoring against any single
ria (Zhang et al., 2026), and explanation-style AF           reference Pb⋆ unfairly punishes alternatives. We
gains were reported on Isabelle natural-language             instead evaluate Pb along a finite vector of prop-
inference (Quan et al., 2025). These frameworks              erty probes computable on the explicit side. Some
leave open how to exploit partial, local structure           probes are kernel-side and deterministic, while oth-
when proof completion is unavailable or the judge            ers cross back to the informal source. None con-
is noisy. We instead target proxy signals induced            sults a reference formalization, so the family by-
by explicit inference constraints and decompose              passes gold-standard scarcity at the global level.
evaluation into a property-vector that a per-axis            Section 3.1 formalizes the probes as judges, and
controller can act on.                                       Section 3.2 closes the loop into a reflective refine-
                                                             ment cycle (Figure 1).
Inference-time refinement and judge calibration.
Self-Refine and Reflexion use verbal feedback with-          3.1   Judges and Local Properties
out weight updates (Madaan et al., 2023; Shinn
et al., 2023); Tree-of-Thought (Yao et al., 2023)            A finite family of m judges Ξ = {ξ1 , . . . , ξm },
and self-consistency (Wang et al., 2023) aggregate           each a computable functional ξk : E → [0, 1], eval-
or score candidate traces. Step-level process super-         uates properties of Pb and its bindings; in this paper
vision (Uesato et al., 2022; Lightman et al., 2024)          we use m = 8, with one judge per audit axis, parti-
and calibrated LLM-as-judge (Zheng et al., 2023;             tioned by the three structural scopes introduced in
Ouyang et al., 2022; Bai et al., 2022) push eval-            Section 1.
uation below the outcome level. These methods                   Global scope (judge consumes the whole elicited
motivate local evaluation, but they report no finite         object Pb; kernel-decided):
property vector whose per-axis errors govern re-
                                                              • ξglb (Pb): the prover completes the full elabo-
finement, and no convergence statement under im-
perfect judges. Our framework supplies both ingre-              ration and inference pass on Pb without crash,
dients: a structured per-axis verdict ξ(Pb) ∈ [0, 1]m           timeout, or non-termination.
organized by global, per-module, and cross-domain             • ξdoc (Pb): Pb is a structurally valid source arti-
scopes, whose violated coordinate routes the con-               fact under the prover’s document conventions
troller to the corresponding repair target, and a               (declaration order, scope brackets, presence of
drift-Lyapunov analysis that exposes the asymp-                 required resources).
totic noise floor. Concurrent work on LLM-verifier
loops (Dantas et al., 2025) bounds expected itera-             Per-module scope (judge consumes a single mod-
tion count rather than asymptotic gap height.                ule M ∈ Pb; kernel-decided):

3   Proposed Framework                                        • ξsyn (M ): every statement inside module M is
                                                                accepted by the parser and rule schemas.
We now formalize the framework introduced in
Section 1 as a staged operator Π together with a              • ξtyp (M ): the types and schemas declared in-
judge family Ξ acting on a structured elicited object           side M are mutually consistent across its state-
(see Figure 2). Concretely, Π takes the informal                ments.
input nl together with a per-instance fact context
                                                              • ξbnd (M ): the inferential links inside M wire
Γ, and produces
                                                                its local premises and conclusions through
      Pb = Π(nl, Γ) = {M1 , M2 , . . . , MK },    (1)           structurally complete steps and preserve vari-
                                                                able bindings.
where each module M holds a coherent set of ex-
plicit statements pbj together with their declarations         Cross-domain scope (judge additionally consults
and the references they make into Γ. The context Γ           the informal source nl and per-instance context Γ;
collects per-instance facts surfaced for the example         externally judged):

                                                         3
                                                                             Reasoning Kernel:                                     ෠
                                                                                                                             𝜉𝑔𝑙𝑏 (𝑃)
                                                                             parse -> elaborate -> typecheck -> proof

                                     𝚪                       …                                                           ෡
                                                                                                                         𝑷
 Context:
 …                                                           axiomatization where
    A violin is an instrument.             𝜉𝑔𝑛𝑑 (𝑀1 , 𝑛𝑙, 𝛤)   explanation_1: "∀x. Violin x ⟶ Instrument x”             𝑴𝟏
 …                                                                                                                                       ෠
                                                                                                                                   𝜉𝑑𝑜𝑐 (𝑃)
                                                             theorem hypothesis:
                                     𝒏𝒍      𝜉𝑠𝑝 (𝑀2 , 𝑛𝑙)
 Premise:                                                     assumes asm: “Woman x ∧ Violin y ∧ Statue z ∧
 A woman is playing the violin in front                       Playing x y ∧ InFrontOf x z”                                         𝜉𝑠𝑦𝑛 (𝑀2 )
                                             𝜉𝑏𝑛𝑑 (𝑀2 )
 of a statue.                                                 shows “∃x y e. Woman x ∧ Instrument y ∧ Playing x y”                 𝜉𝑡𝑦𝑝 (𝑀2 )
 Hypothesis:                                                  using assms explanation_1 by blast
                                                      ෠
                                            𝜉𝑐𝑜𝑣 (𝑛𝑙, 𝑃)
 A woman is playing an instrument.                           end                                                        𝑴𝟐

                                          + explicit reasoning steps
              Implicit                + grounded facts/defs/rules
                                                                                      Explicit

Figure 2: Implicit-to-Explicit Transition. Correctness is checked at three scopes: the whole object, each module,
and the alignment back to the informal source nl and context Γ. Each scope has its own judge.


 • ξgnd (M, nl, Γ): every predicate, constant, or                      Prover-grounded return policy. Because the
   symbol used inside M traces back to an entity                       LLM-evaluated axes ξsp , ξcov may report false vio-
   introduced by nl or by Γ.                                           lations, a repair guided by them can break a kernel-
                                                                       verifiable axis without the judge noticing. We there-
 • ξsp (M, nl): each explicit statement inside M
                                                                       fore return the latest iterate that the prover accepts,
   aligns with some implicit claim in nl, with the
                                                                       and roll back whenever the prover moves from ac-
   alignment constructed by the judge.
                                                                       cept to reject between consecutive iterations.
 • ξcov (nl, Pb): the key claim units of nl are rep-
   resented explicitly somewhere in Pb.                                4     Proxy Theory Grounded in Explicit
                                                                             Language and Inference
Each violation points to an identifiable repair tar-
get.                                                                   The reflective loop of Section 3 converges at a rate
                                                                       determined by judge noise and a contraction pa-
3.2   Reflective Refinement Loop                                       rameter.

A controller aggregates these localized signals,                       4.1    Intrinsic Properties and the Proxy Score
picks which subcomponent to repair next, and re-
peats the cycle until an acceptance threshold is met.                  To measure intrinsic progress without a reference
We index the AF process by i with parameters θi                        formalization, we attach to the elicited object Pb ∈
that collect prompts, transformations, or policy pa-                   E a latent quality vector q : E → [0, 1]m whose
rameters. At each iteration:                                           components measure the satisfaction of m intrin-
                                                                       sic properties. Each component qk (Pb) records the
1. Propose. Produce Pbi via Πθi (nl, Γ).                               fraction of audit units of property k that pass on Pb,
                                                                       in a strict modular sense in which a single internal
2. Measure. Evaluate the judge vector ξ(Pbi ) =                        violation fails its host module.
   (ξ1 (Pbi ), . . . , ξm (Pbi )).                                        Each component ξk (Pb) ∈ [0, 1] aggregates the
                                                                       binary judge verdicts on the audit units of property
3. Localize. Select a target subcomponent ti re-
                                                                       k, with the audit-unit definition and aggregation
   sponsible for the strongest violation.
                                                                       formula detailed in Section A.
4. Repair. Update θi+1 ← Refine(θi , ti , ξ(Pbi )).                       We adopt q(Pb⋆ ) = 1 as the marker of in-
                                                                       trinsic correctness. Fixing weights w ∈ Rm        ≥0
The loop is constraint-directed, with update axes                      with ∥w∥1 = 1, the intrinsic progress measure
drawn from the finite constraint families that Sec-                    is µ⋆ (Pb) = ⟨w, q(Pb)⟩ with observable counterpart
tion 4 formalizes; Figure 1 summarizes the result-                     b(Pb) = ⟨w, ξ(Pb)⟩.
                                                                       µ
ing pipeline.

                                                                   4
                                                           Table 1: Backbones and Judge Model. Seven
  Assumption 1 (Audit sufficiency of the prop-
                                                           formalization backbones and one fixed judge. Llama
  erty vector). q(Pb) = 1 implies Pb passes                and DeepSeek identifiers are abbreviated (e.g.
  every prover-decidable check and aligns with             Llama-3.3-70B); other names match the released
  the informal source nl on every cross-domain             identifiers.
  axis within the judge family Ξ of Section 3.1.
                                                              Model             Family     Tier (Architecture)
   Theorem 1 is a score-level result and uses only             Formalization Backbones
this audit-level sufficiency.                                 GPT-5.4          GPT         Frontier (Proprietary)
                                                              DeepSeek-V4      DeepSeek    Frontier MoE
                                                              DeepSeek-V3.1 DeepSeek       Frontier MoE
4.2   Refinement and the Drift Assumption                     Llama-4-17B      Llama       Mid-Tier MoE
A refinement step takes the current object and the            Llama-3.3-70B Llama          Compact Dense
                                                              Llama-3.1-8B     Llama       Compact Dense
judge readings and returns the next iterate, Pbi+1 =          Qwen-3.5-9B      Qwen        Compact Dense
Refine(Pbi , ξ(Pbi )); Refine folds the Localize and           Judge Model
Repair sub-steps of Section 3.2 (target selection             GPT-5.4-mini      GPT        Mid-Tier (Proprietary)
on ξ, parameter update to θi+1 , and reproposal
through Πθi+1 ), and the analysis below uses only
its input/output signature.
                                                             tion 2, the expected intrinsic gap satisfies
   Following the drift-Lyapunov tradition for
stochastic optimization with bounded noise (Bot-                            E[gi+1 ] ≤ (1 − λ) E[gi ] + b η,
tou et al., 2018), we adopt an expected-contraction-
with-residual form on the gap dynamics.                               lim sup E[gi ] ≤ bλη ,
                                                                       i→∞
                                                                lim inf E[µ⋆ (Pbi )] ≥ 1 − bλη ,
  Assumption 2 (Bounded regress with con-                        i→∞
  tractive drift). There exist constants λ ∈                                                       (3)
  (0, 1] and b ≥ 0, independent of i and of                  and the plateau approaches 1 when η → 0.
  η, such that
          h          i                                        Each round shrinks the expected gap by a fac-
        E gi+1 | Pbi ≤ (1 − λ) gi + b η,                   tor 1 − λ until further contraction is balanced by
                                          (2)
                    gi := 1 − µ⋆ (Pbi ),                   the noise residual bη/λ, so the plateau height is
                                                           proportional to η (proof in Section E). Reducing η
  for all i, where η is the per-audit-unit judge           therefore tightens the plateau directly, and repeated
  misclassification rate of Assumption 4.                  judging provides such a reduction.

   The factor 1 − λ contracts the remaining gap
                                                             Lemma 1 (Majority vote reduces effective
by a fixed fraction each round, and the additive
                                                             uncertainty). Under Assumption 4, write ηeff
b η absorbs the residual judge noise and imperfect-
                                                             for the per-audit-unit misclassification rate
localization terms. The microscopic motivation
                                                             of the majority vote over T independent calls
in Section B suggests that the underlying per-step
                                                             on the same audit unit. Then
repair probability scales as ρ ≥ ρ0 − cη, so the
                                                                                             2 
contraction rate λ implicitly degrades as η grows.                    ηeff ≤ exp −2T 12 − η .          (4)
We treat λ and b as constants in the analysis and
interpret the plateau bound bη/λ as valid in the
regime η ≪ ρ0 /c.                                             Substituting Equation (4) into the plateau bound
                                                           yields
4.3   Plateau Convergence and Correctness
Iterating the drift inequality across i produces a                                                  ηeff
                                                                      1 − lim inf E[µ⋆ (Pbi )] ≲         .          (5)
closed-form bound on the intrinsic gap gi := 1 −                             i→∞                     λ
µ⋆ (Pbi ).

  Theorem 1 (Geometric convergence to a                    In the zero-noise limit, E[µ⋆ (Pbi )] → 1 certifies
  noise-dependent plateau). Under Assump-                  that the refinement converges to objects that pass
                                                           every audit-sufficient probe of Assumption 1.

                                                       5
Table 2: Per-Backbone Pass Rate (%): Baseline / Ours. Results are shown in Mean ± std across seeds. ↑: ours
exceeds baseline. Bold marks the higher mean in each cell. Cross-backbone µ⋆ aggregate is in Section F.

            Backbone                miniF2F ↑          ProofNet ↑             e-SNLI ↑             ProntoQA ↑
            GPT-5.4       91.4±1.1 / 97.7±0.2↑ 68.1±3.9 / 88.5±2.0↑ 98.0±1.0 / 99.7±0.6↑ 100.0±0.0 / 100.0±0.0
            DeepSeek-V4 83.6±0.4 / 91.5±0.2↑ 49.8±2.7 / 70.5±3.3↑ 78.3±1.1 / 100.0±0.0↑ 100.0±0.0 / 100.0±0.0
            DeepSeek-V3.1 79.9±2.1 / 88.5±2.6↑ 53.9±0.9 / 69.2±1.4↑ 75.3±2.5 / 100.0±0.0↑ 100.0±0.0 / 100.0±0.0
            Llama-4-17B      70.9±1.6 / 84.3±1.7↑ 39.9±2.2 / 59.5±4.6↑    69.0±1.0 / 99.0±1.0↑ 96.3±0.3 / 100.0±0.0↑
            Llama-3.3-70B    67.6±1.4 / 73.4±2.2↑ 8.1±1.6 / 10.4±2.2↑     62.7±4.0 / 83.0±3.6↑ 89.2±1.3 / 98.3±1.1↑
            Llama-3.1-8B     57.0±2.4 / 61.6±3.4↑ 12.1±1.4 / 14.0±2.9↑    72.7±2.1 / 83.7±3.5↑ 97.0±1.0 / 99.2±1.0↑
            Qwen-3.5-9B      82.4±2.3 / 91.4±1.4↑ 57.1±4.0 / 65.6±1.3↑    77.3±5.7 / 79.7±2.3↑ 97.3±0.8 / 98.7±0.3↑


Table 3: Judge-Capacity Ablation. Per-benchmark                     and per-dataset sampling protocols are in Sec-
rows. Results are shown in Mean ± std across seeds;                 tion G.
µ⋆ ± is cross-fixture std. Bold: column maximum.
                                                                    Formalization and judge backbones. Seven for-
Data       Judge             µ⋆0 ↑       µ⋆∞ ↑    Pass Rate ↑       malization backbones span four families and three
           Llama-3.3-70B 0.90±0.10 0.91±0.13        65.9±5.3        scale tiers: a frontier API tier (GPT-5.4, DeepSeek-
ProofNet   GPT-5.4       0.86±0.13 0.88±0.16        66.5±2.0
           GPT-5.4-mini 0.90±0.10 0.92±0.13         69.2±1.4
                                                                    V4, DeepSeek-V3.1), a mid-tier MoE point (Llama-
                                                                    4-17B), and three compact-dense open-weight mod-
         Llama-3.3-70B 0.93±0.07 0.98±0.06          100.0±0.0
ProntoQA GPT-5.4       0.93±0.07 0.99±0.04          100.0±0.0       els (Llama-3.3-70B, Llama-3.1-8B, Qwen-3.5-9B);
         GPT-5.4-mini 1.00±0.03 1.00±0.00           100.0±0.0       see Table 1 for full upstream identifiers. The judge
                                                                    is fixed to GPT-5.4-mini in all experiments except
Table 4: Locality Ablation. Judge sees only the lo-                 the judge-capacity ablation of Section 5.4, with
cal module (local) vs. the whole candidate (global,                 low-temperature decoding (≤ 0.2) and the same
LJ =LAF ). Results are shown in Mean ± std across                   per-axis prompt across all experiments.
seeds; µ⋆ ± is cross-fixture std. Bold: column maxi-
mum.                                                                Metrics. We report three metrics in each results
                                                                    table. µ⋆0 and µ⋆∞ are the audit-unit pass rate at
Data       Judge Scope      µ⋆0 ↑      µ⋆∞ ↑     Pass Rate ↑
                                                                    the initial and final iterates Pb0 and Pb∞ . Pass Rate
           Global        0.90±0.10 0.92±0.12      65.9±0.6          is the fraction of instances for which the prover
ProofNet
           Local         0.91±0.10 0.92±0.12      66.1±3.1
                                                                    accepts Pb∞ . Every setting is run with three ran-
           Global        0.99±0.02 1.00±0.00      100.0±0.0         dom seeds; table captions specify which standard
ProntoQA
           Local         0.99±0.03 1.00±0.02      100.0±0.0
                                                                    deviation is reported in each column.

                                                                    Baseline. Following prior autoformalization
5     Empirical Evaluation                                          work (Wu et al., 2022; Jiang et al., 2023; Zhang
5.1    Experimental Setup                                           et al., 2026; Quan et al., 2025), we use a single in-
                                                                    context learning prompt with three demonstrations
Benchmarks and provers. We evaluate on                              per setting (Section H) as the baseline, keeping the
two formal-proof benchmarks, miniF2F (Zheng                         backbone, prompt, and judge model identical to
et al., 2022) and ProofNet (Azerbayev et al.,                       those used by the refinement loop. This matched-
2023), and two natural-language-IR benchmarks,                      setup comparison is preferred over cross-paper ab-
e-SNLI (Camburu et al., 2018) with a typed neo-                     solute pass rates, which are not directly comparable
Davidsonian IR and ProntoQA (Saparov and He,                        when each system targets a different proof assistant
2023) with FOL. miniF2F and ProofNet are formal-                    on non-overlapping splits.
ized in Lean 4 (de Moura and Ullrich, 2021), whose
kernel-level elaboration decides the kernel-verified                5.2   Main Results
coordinates of q (ξglb , ξdoc , ξsyn , ξtyp , ξbnd ). e-            Per-backbone Pass Rate across the seven formal-
SNLI and ProntoQA are formalized in Is-                             ization backbones and four datasets is shown in
abelle/HOL (Nipkow et al., 2002), whose higher-                     Table 2. We can see that:
order logic kernel together with the bidirectional
ATP oracle certifies the cross-domain coordinates                   Our refinement framework improves Pass Rate
(ξgnd , ξsp , ξcov ) on the IR side. Sample sizes, splits,          across the seven backbones and four datasets.

                                                                6
                                                                    0.65                                                                                                                1.02
            0.8                                                                                                              1.0
                                                                    0.60                                                                                                                1.00
            0.7                                                                                                              0.9
Pass Rate




                                                        Pass Rate




                                                                                                                 Pass Rate




                                                                                                                                                                            Pass Rate
                                                                    0.55
                                                                                                                             0.8                                                        0.98
            0.6                                                     0.50
                                                                                                                             0.7                                                        0.96
            0.5                                proxy                0.45                               proxy                                                     proxy                                                 proxy
                                               oracle                                                  oracle                0.6                                 oracle                                                oracle
                                                                    0.40                                                                                                                0.94
                   1 2 3 4 5 6 7 8 9 10                                    1 2 3 4 5 6 7 8 9 10                                     1        2               3          4                      1   2      3        4        5
                               iteration                                               iteration                                                 iteration                                             iteration

              (a) DS-V3.1 / miniF2F                                  (b) DS-V3.1 / ProofNet                                        (c) DS-V3.1 / e-SNLI                                 (d) DS-V3.1 / ProntoQA
            0.85                                                                                                             0.75
                                                                    0.60
            0.80                                                                                                             0.70                                                       0.94
                                                                    0.55                                                                                                                0.92
Pass Rate




                                                        Pass Rate




                                                                                                                 Pass Rate




                                                                                                                                                                            Pass Rate
            0.75                                                                                                             0.65
                                                                    0.50                                                     0.60                                                       0.90
            0.70
                                                                    0.45                                                     0.55                                                       0.88
            0.65                               proxy                                                   proxy                                                     proxy                                                 proxy
                                               oracle                                                  oracle                0.50                                oracle                 0.86                           oracle
            0.60                                                    0.40
                   1   2   3       4       5   6    7                      1   2   3    4    5     6   7     8                      1 2 3 4 5 6 7 8 9 10                                       1 2 3 4 5 6 7 8 9 10
                               iteration                                               iteration                                                 iteration                                             iteration

             (e) Qwen-9B / miniF2F                                   (f) Qwen-9B / ProofNet                                    (g) Qwen-9B / e-SNLI                                     (h) Qwen-9B / ProntoQA

Figure 3: Refinement Trajectories. Each panel shows the proxy µ  b (solid) and the external oracle pass rate (dashed)
per iteration, on DeepSeek-V3.1 (top) and Qwen-3.5-9B (bottom); the band is the mean ± std across three seeds.
The y-axis range differs per panel, so values are not comparable across panels.

Table 5: Per-Axis vs. Scalar Verdict. Pass Rate (%). Rows above and below the midrule differ only in the verdict
format: per-axis vector (decomposed) or single end-to-end score (scalar). Results are shown in Mean ± std across
seeds. Bold: column maximum.

                                    Method                                     Judge                   miniF2F ↑ ProofNet ↑ e-SNLI ↑ ProntoQA ↑
                                                                               GPT-5.4                     84.7±0.2                     58.8±2.4             81.0±2.7           100.0±0.0
                                    Scalar
                                                                               GPT-5.4-mini                86.9±0.4                     58.4±1.1             82.0±1.0           100.0±0.0
                                                                               GPT-5.4                     86.1±1.6                     67.0±1.1          98.0±1.0              100.0±0.0
                                    Decomposed (Ours)
                                                                               GPT-5.4-mini                88.5±0.7                     66.8±1.7         100.0±0.0              100.0±0.0



Across the seven backbones and four datasets, our                                                                       family the benchmark belongs to.
refinement framework exceeds the single-shot ICL
baseline on most settings. The frontier three back-                                                                     Refinement helps every backbone, but abso-
bones gain +19% on ProofNet and +16% on e-                                                                              lute Pass Rates scale with backbone capac-
SNLI on average. These gains are an order of                                                                            ity. The frontier three backbones reach 69–89%
magnitude above the per-row seed std we observe                                                                         on ProofNet, ≥ 99.7% on e-SNLI, 100% on
in Table 2, so the improvement is not a within-seed                                                                     ProntoQA, and 88–98% on miniF2F, whereas the
fluctuation but a stable shift of the candidate that                                                                    two compact-dense Llamas remain at ≤ 14% on
the proposer alone cannot deliver.                                                                                      ProofNet even after refinement. The same compact-
                                                                                                                        dense backbones nonetheless gain +5–6% on
Refinement gain is inversely correlated with                                                                            miniF2F, +2–9% on ProntoQA, and +11–20% on
baseline Pass Rate, irrespective of whether the                                                                         e-SNLI. Backbone capacity therefore bounds the
benchmark is math or explanation. ProofNet                                                                              absolute Pass Rate, but the gain from refinement
(frontier baseline 50–68%) gains 15–21%; e-SNLI                                                                         does not vanish at smaller scales.
(baseline 75–98%) gains 2–25%; miniF2F (base-
                                                                                                                        5.3              Judge Calibration
line 80–91%) gains only 6–9%; ProntoQA stays
at the dataset ceiling. The largest gains land on                                                                      Because autoformalization lacks a scalable gold-
the two lowest-baseline benchmarks, one math                                                                           standard corpus at the sizes used here, reference-
(ProofNet) and one explanation (e-SNLI); the math                                                                      free evaluation through LLM-judge proxies is the
benchmark with the higher baseline (miniF2F)                                                                           established practice in the closest concurrent work
yields less than half the gain of ProofNet. The size                                                                   (Zhang et al., 2025, 2026; Quan et al., 2025). To
of the refinement gain therefore tracks how much                                                                       check how well our proxy reflects the true correct-
headroom the baseline leaves rather than which                                                                         ness signal, we construct an approximate stand-

                                                                                                                 7
in for the gold label, which we call the oracle,            the three judges span only 3.3% (Llama-3.3-70B
and compare its per-iteration pass rate against the         65.9 ± 5.3%, GPT-5.4-mini 69.2 ± 1.4%, GPT-
proxy score µ b on two representative backbones             5.4 66.5 ± 2.0%). The cross-dataset spread on the
(DeepSeek-V3.1, Qwen-3.5-9B). The oracle is cho-            same DeepSeek-V3.1 backbone is ≈ 19–31%, an
sen per benchmark to match what each prover can             order of magnitude larger, so a mid-sized judge
decide: on the Lean math benchmarks (miniF2F,               already exhausts the available signal under audit-
ProofNet) it is a GPT-5.4 judge that compares the           unit feedback.
candidate against the gold Lean reference, and on
the Isabelle natural-language benchmarks (e-SNLI,           5.5    Effect of Judge Context Size
ProntoQA) it queries the candidate’s axiomatiza-
                                                            We contrast the default per-axis judge (which
tion with the ATP in both directions and checks the
                                                            sees only the local audit unit) against a context-
verdict against the dataset label. We can see from
                                                            expanded variant that receives the entire elicited
Figure 3 that:
                                                            object Pb as LJ =LAF , as shown in Table 4. We can
The proxy trajectory follows the same per-                  see that:
iteration shape as the external oracle, even
though they measure quality on different scales.            Letting the judge see the entire formal candidate
On every panel of Figure 3, the proxy µ    b and the        does not help compared to letting it see only the
oracle pass rate trace qualitatively the same per-          local module being scored. ProntoQA reaches
iteration curve. Both rise sharply over the first few       100% under both views, and on ProofNet the two
iterations and flatten by iteration 3–5, reproducing        are statistically tied (65.9 ± 0.6% global vs. 66.1 ±
the geometric approach to a plateau predicted by            3.1% local). The local module already supplies
Theorem 1, with the aggregate proxy plateau at              what a global view would add.
0.89–0.99 across math and explanation (Table 6).
The two curves nonetheless differ in absolute level         5.6    Decomposed versus Scalar Feedback
because the proxy and the oracle score quality on
                                                            Holding the loop fixed, we vary only the verdict
incompatible scales, so the y-axis offset between
                                                            format—per-axis audit-unit vector (ours) versus a
the solid and dashed curves reflects this scale mis-
                                                            single end-to-end scalar with a natural-language
match rather than the noise floor η.
                                                            rationale—and cross it with judge capacity (GPT-
Where the proxy and oracle curves disagree, the             5.4 vs. GPT-5.4-mini) on the four datasets.
proxy gives credit for repairs the oracle does
not. On Qwen-3.5-9B’s ProntoQA panel the or-                A per-axis verdict outperforms a single end-
acle stays flat while the proxy continues to climb.         to-end score wherever the baseline Pass Rate
The proxy credits any per-axis repair its judge ac-         is below saturation, and matches it where the
cepts, including surface-level fixes that tighten the       baseline already saturates. On the two datasets
axiomatization, whereas the oracle only changes             where the baseline is below saturation the per-axis
when the ATP’s verdict flips on the dataset label.          proxy beats the scalar proxy on both judge tiers (Ta-
Seed-band and judge-noise diagnostics are reported          ble 5): ProofNet sees an 8.2–8.4% gap and e-SNLI
in Section I.                                               sees a 17–18% gap. ProntoQA reaches 100% under
                                                            both, and miniF2F (baseline ≥ 84%) shows only
5.4   Judge Capacity                                        a 1.4–1.6% gap within seed variance. The split
Fixing DeepSeek-V3.1 as the formalizer, we run              tracks headroom rather than benchmark family.
the loop under three judge models that span a wide
capacity range: the open-weight Llama-3.3-70B,              6     Conclusion
the mid-sized GPT-5.4-mini default, and the fron-
tier GPT-5.4, as shown in Table 3. The same                 We recast autoformalization evaluation as
DeepSeek-V3.1 formalizer carries through Sec-               constraint-directed optimization over a per-axis
tions 5.5 and 5.6. We can see that:                         vector of verifiable property checks. Across
                                                            seven backbones and four datasets the resulting
Swapping the judge for a stronger or weaker                 refinement loop consistently improves Pass Rate,
model changes the final Pass Rate by much less              and ablations identify the per-axis proxy as the
than swapping the dataset does. On ProofNet,                source of this advantage.

                                                        8
Limitations                                                 Yuntao Bai, Saurav Kadavath, Sandipan Kundu,
                                                              Amanda Askell, Jackson Kernion, Andy Jones, Anna
Our notion of correctness is audit-sufficient rather          Chen, Anna Goldie, Azalia Mirhoseini, Cameron
than fully semantic. The calibration in Section 5.3           McKinnon, Carol Chen, Catherine Olsson, Christo-
                                                              pher Olah, Danny Hernandez, Dawn Drain, Deep
nonetheless shows that the audit-unit score µ  b and          Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez,
an independently constructed external oracle move             and 32 others. 2022. Constitutional ai: Harmlessness
together in per-iteration shape on every panel, so            from ai feedback. arXiv preprint arXiv:2212.08073.
audit-sufficient acceptance and semantic correct-
                                                            Léon Bottou, Frank E. Curtis, and Jorge Nocedal. 2018.
ness are empirically correlated even though they              Optimization methods for large-scale machine learn-
are not formally identified. Formalizing this corre-          ing. SIAM Review, 60(2):223–311.
lation through paired-target oracles, on benchmarks
where such oracles can be sourced at scale, is left         Oana-Maria Camburu, Tim Rocktäschel, Thomas
                                                              Lukasiewicz, and Phil Blunsom. 2018. e-SNLI: Natu-
to future work.                                               ral language inference with natural language explana-
   Second, the empirical advantage of per-axis de-            tions. In Advances in Neural Information Processing
composition is currently dataset-conditional. We              Systems, volume 31.
see clear effects on Lean ProofNet and Isabelle             Pierre Dantas, Lucas Cordeiro, Youcheng Sun, and
e-SNLI, where the baseline Pass Rate is below sat-            Waldir Junior. 2025. The 4/δ bound: Designing pre-
uration and the kernel admits multiple violation               dictable LLM-verifier systems for formal method
modes, but the gap collapses on Lean miniF2F and               guarantee. arXiv preprint arXiv:2512.02080.
Isabelle ProntoQA where the baseline already satu-          Leonardo de Moura and Sebastian Ullrich. 2021. The
rates. Whether the audit-unit construction general-           Lean 4 theorem prover and programming language.
izes as a dataset-agnostic refinement signal will re-         In Automated Deduction – CADE 28, pages 625–635,
quire evaluation on benchmarks with broader topic             Cham. Springer International Publishing.
coverage and iter-0 pools that are below saturation,        Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda
particularly outside the four-dataset slice we used           Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix,
here.                                                         Yuhuai Wu, and Guillaume Lample. 2023. Draft,
   Third, the framework as presented is purely an             sketch, and prove: Guiding formal theorem provers
                                                              with informal proofs. In International Conference on
inference-time refinement procedure. The per-axis             Learning Representations (ICLR).
verdict vector is in principle a richer training sig-
nal than a scalar reward, and integrating it into           Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri
                                                              Edwards, Bowen Baker, Teddy Lee, Jan Leike, John
reinforcement-learning fine-tuning of either the pro-
                                                              Schulman, Ilya Sutskever, and Karl Cobbe. 2024.
poser or the judge, so as to close the loop between           Let’s verify step by step. In International Conference
calibration and policy improvement, is a natural              on Learning Representations (ICLR).
next step that we have not pursued in this work. Be-
                                                            Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
yond autoformalization, we expect the same audit-            Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
unit decomposition to apply wherever correctness             Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
can be approximated by a calibrated family of prop-          Shashank Gupta, Bodhisattwa Prasad Majumder,
erty checks, including program synthesis and multi-          Katherine Hermann, Sean Welleck, Amir Yazdan-
                                                             bakhsh, and Peter Clark. 2023. Self-refine: Iterative
hop natural-language reasoning.
                                                             refinement with self-feedback. In Advances in Neu-
                                                             ral Information Processing Systems.
Acknowledgments
                                                            Tobias Nipkow, Lawrence C. Paulson, and Markus
This work was partially funded by the Swiss Na-               Wenzel. 2002. Isabelle/HOL: A Proof Assistant for
tional Science Foundation (SNSF) projects RATIO-              Higher-Order Logic, volume 2283 of Lecture Notes
                                                              in Computer Science. Springer.
NAL and M-RATIONAL.
                                                            Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Car-
                                                              roll L. Wainwright, Pamela Mishkin, Chong Zhang,
References                                                    Sandhini Agarwal, Katarina Slama, Alex Ray, John
                                                              Schulman, Jacob Hilton, Fraser Kelton, Luke Miller,
Zhangir Azerbayev, Bartosz Piotrowski, Hailey                 Maddie Simens, Amanda Askell, Peter Welinder,
  Schoelkopf, Edward W. Ayers, Dragomir Radev, and            Paul Christiano, Jan Leike, and Ryan Lowe. 2022.
  Jeremy Avigad. 2023. Proofnet: Autoformalizing              Training language models to follow instructions with
  and formally proving undergraduate-level mathemat-          human feedback. In Advances in Neural Information
  ics. arXiv preprint arXiv:2302.12433.                       Processing Systems.


                                                        9
Stanislas Polu and Ilya Sutskever. 2020. Generative            Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
   language modeling for automated theorem proving.              2022. MiniF2F: A cross-system benchmark for for-
   arXiv preprint arXiv:2009.03393.                              mal olympiad-level mathematics. In International
                                                                 Conference on Learning Representations (ICLR).
Xin Quan, Marco Valentino, Louise A. Dennis, and
  André Freitas. 2025. Faithful and robust LLM-                Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  driven theorem proving for NLI explanations. arXiv             Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  preprint arXiv:2505.24264.                                     Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
                                                                 Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
Abulhair Saparov and He He. 2023. Language models                LLM-as-a-judge with MT-Bench and chatbot arena.
  are greedy reasoners: A systematic formal analysis             In Advances in Neural Information Processing Sys-
  of chain-of-thought. In International Conference on            tems (Datasets and Benchmarks Track).
  Learning Representations (ICLR).
                                                               A     Auxiliary Bounds
Noah Shinn, Federico Cassano, Edward Berman, Ash-
  win Gopinath, Karthik Narasimhan, and Shunyu Yao.            A.1     Audit-Unit Framework
  2023. Reflexion: Language agents with verbal rein-
  forcement learning. In Advances in Neural Informa-           Each elicited object Pb = {M1 , . . . , MK } ∈ E
  tion Processing Systems.                                     decomposes into K ≥ 1 modules. The audit-unit
                                                               definition for each property follows the scope at
Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-
  cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,
                                                               which the property is defined in Section 3.1.
  Geoffrey Irving, and Irina Higgins. 2022. Solving               For the four module-scoped properties k ∈
  math word problems with process- and outcome-                {syn, typ, bnd, gnd}, the audit units are the mod-
  based feedback. arXiv preprint arXiv:2211.14275.             ules; a single judge call on module M returns a
Marco Valentino, Ian Pratt-Hartmann, and André Fre-            binary value ξk (M ) ∈ {0, 1}, with latent coun-
 itas. 2021. Do natural language explanations repre-           terpart qk (M ) ∈ {0, 1} understood as the strict
 sent valid logical arguments? verifying entailment in         conjunction of the underlying per-statement, per-
 explainable NLI gold standards. In Proceedings of
                                                               binding, or per-symbol checks, where a single in-
 the 14th International Conference on Computational
 Semantics (IWCS), pages 76–86.                                ternal violation suffices to set qk (M ) = 0. For the
                                                               two whole-object axes k ∈ {glb, doc}, the audit
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,              units are Pb itself (a single unit per instance), with
  Ed H. Chi, Sharan Narang, Aakanksha Chowdhery,
  and Denny Zhou. 2023. Self-consistency improves              ξk (Pb), qk (Pb) ∈ {0, 1}.
  chain of thought reasoning in language models. In In-           For statement-scoped semantic preservation k =
  ternational Conference on Learning Representations           sp, the audit units are the explicit statements pbj ∈
  (ICLR).
                                                               Pb taken across modules. For coverage k = cov,
Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N.                the audit units are the source claim units c ∈ C(nl),
  Rabe, Charles Staats, Mateja Jamnik, and Christian           with ξcov (c), qcov (c) ∈ {0, 1} defined on whether
  Szegedy. 2022. Autoformalization with large lan-
                                                               c is represented somewhere in the current Pb. This
  guage models. In Advances in Neural Information
  Processing Systems.                                          batch-AND framing is the strict modular evalua-
                                                               tion semantics already implied by Section 3.1; the
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chala-
                                                               per-item view is conceptual, and both the judge
  mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  Prenger, and Anima Anandkumar. 2023. LeanDojo:               interface and the noise model live at the audit-unit
  Theorem proving with retrieval-augmented language            level corresponding to each axis’s scope.
  models. In Advances in Neural Information Process-              We write u for a generic audit unit and Nk (Pb)
  ing Systems (Datasets and Benchmarks Track).                 for its count, with Nk (Pb) = K for the four module-
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,              scoped axes,  P Nk (P ) = 1 for k ∈ {glb, doc},
                                                                                      b
  Thomas L. Griffiths, Yuan Cao, and Karthik                   Nsp (P ) = M |M | for statement-scoped seman-
                                                                      b
  Narasimhan. 2023. Tree of thoughts: Deliberate
                                                               tic preservation, and Ncov (Pb) = |C(nl)| ≥ 1 for
  problem solving with large language models. In Ad-
  vances in Neural Information Processing Systems.             coverage. Inactive coordinates are dropped, and w
                                                               is renormalized over the active set. The property-
Lan Zhang, Marco Valentino, and André Freitas. 2025.
                                                               level aggregates of Section 4.1 are sample means
  Beyond gold standards: Epistemic ensemble of LLM
  judges for formal mathematical reasoning. arXiv              over audit units:
                                                                                              X
  preprint arXiv:2506.10903.                                                  ξk (Pb) = 1         ξk (u),
                                                                                       Nk (Pb)
Lan Zhang, Marco Valentino, and André Freitas. 2026.                                             u
                                                                                                 X
  Monotonic reference-free refinement for autoformal-                                    1
                                                                           qk (Pb) =                 qk (u).
  ization. arXiv preprint arXiv:2601.23166.                                            Nk (Pb)
                                                                                                 u


                                                          10
The observable ξk (Pb) ∈ [0, 1] is the empirically             check). Let vj (Pb) ∈ {0, 1} indicate whether con-
computed proxy, while qk (Pb) ∈ [0, 1] is the ideal-           straint j is satisfied; these are exactly the per-item
ized aggregate of conceptual per-unit ground-truth             predicates that the batch-AND framing of Sec-
labels qk (u) that the proxy approximates. The per-            tion 4.1 aggregates internally to a module verdict,
audit-unit binary judge model of Assumption 4                  and we use them here to expose the microscopic
(Section C) propagates through this aggregation                dynamics that motivate Assumption 2. Setting
to a one-step concentration bound between the ob-
servable proxy µ b and the latent µ⋆ .                                                         n(Pb)
                                                                                               X
                                                                             ⋆           1
Lemma 2 (Proxy accuracy bound, one-step). Un-                               µ (Pb) =                   vj (Pb)
                                                                                       n(Pb)
                                                                                               j=1
der Assumption 4 with per-audit-unit misclassifica-
tion rate η, write Nmin (Pb) = mink: wk >0 Nk (Pb)
                                                               is the unweighted constraint-fraction view that co-
for the smallest audit-unit count on Pb across active          incides with the audit-unit aggregate of Section 4.1
axes. For any Pb ∈ E and any δ ∈ (0, 1),                       when modules are sized proportionally to their in-
                                                               ternal constraint counts.
                              s              !
                                 log(2m/δ)
 P |bµ(Pb) − µ⋆ (Pb)| > η +                    ≤ δ.
                                 2 Nmin (Pb)                      The microscopic analysis attaches to each re-
                                                               finement step a model of how many constraints it
   A proof is given in Section E. The bound has                repairs versus newly violates.
two levers. Amplification through repeated judging
(Lemma 1) shrinks η, and larger audit-unit counts              Assumption 3 (Local repair efficacy and bounded
shrink the finite-sample term. The whole-object                regress). Fix iteration i and let Ui be the number
axes (ξglb , ξdoc ) contribute a single unit and there-        of unsatisfied constraints in Pbi . Conditional on
fore depend purely on the η lever; on these axes,              Ui > 0, there exist ρ ∈ (0, 1] and κ ≥ 0 such that
                                                               one refinement step: (i) repairs at least one truly
p m=8 and δ=0.05, the finite-sample term
with
   log(2m/δ)/2 ≈ 1.7 exceeds 1 and the bound                   violated constraint with probability at least ρ; (ii)
is vacuous, so concentration must come from ma-                introduces at most κ newly violated constraints in
jority voting rather than from accumulating audit              expectation.
units. The module-scoped, statement-scoped, and                   If judges and localization are imperfect, ρ de-
source-claim-unit-scoped
                 P           axes additionally benefit         creases as the per-audit-unit misclassification rate
from larger K, M |M |, or |C(nl)|. For instances               η of Assumption 4 increases. A typical minimal
with few modules the concentration term remains                relationship is ρ ≥ ρ0 − cη for some baseline ρ0
a non-trivial fraction of the bound, and we treat it           and constant c > 0 (problem- and implementation-
accordingly in Section 6.                                      dependent).
B    Microscopic Motivation for the Drift                      Lemma 3 (Gap recursion from local repair). Under
     Assumption                                                Assumption 3, for Ui > 0,

Assumption 2 is motivated by a “finite constraints                        E[Ui+1 | Pbi ] ≤ Ui − ρ + κ.
+ local repair” view intrinsic to explicit languages;
this appendix proves the additive form of the re-              If the constraint count is preserved across the
cursion rigorously and then identifies the modeling            step, n(Pbi+1 ) = n(Pbi ), then with µ⋆ (Pbi ) =
step that converts it to the multiplicative form of            1 − Ui /n(Pbi ) this is equivalent to
Assumption 2. The appendix does not derive As-
sumption 2: the additive and multiplicative forms               E[1 − µ⋆ (Pbi+1 ) | Pbi ] ≤ (1 − µ⋆ (Pbi )) − ρ−κ
                                                                                                                b .
                                                                                                                 n(Pi )
are mathematically distinct, and the conversion is
a modeling assumption adopted as a primitive of                   Lemma 3 gives monotone improvement when-
the analysis, not a logical consequence of the mi-             ever ρ > κ. The contractive form of Assump-
croscopic recursion.                                           tion 2 follows once diminishing returns are ac-
Definition 1 (Finite constraint set per instance).             knowledged. As fewer violations remain, repairs
For each Pb ∈ E, let K(Pb) = {1, . . . , n(Pb)} in-            target subtler issues and effective progress shrinks
dex the locally checkable constraints induced by               proportionally to the residual gap, yielding a con-
the prover on that instance (each statement’s well-            traction factor 1 − λ plus a noise-dependent resid-
formedness, each binding site, each inference-step             ual. The transition from the additive recursion of

                                                          11
Lemma 3 to the multiplicative form of Assump-                D     Operationalization Details
tion 2 is itself a modeling step rather than a for-
mal derivation; we treat Assumption 2 as a primi-            D.1    Operational Objects
tive of the analysis and rely on the empirical fit of        Fix a target dataset such as Lean, Coq, Isabelle,
gi+1 = agi + c + ϵi in Section D to validate it. A           or a typed logical intermediate representation with
proof of Lemma 3 is given in Section E.                      a kernel checker, and fix a per-instance fact con-
                                                             text Γ. Each iteration produces an elicited object
C    Amplification by Repeated Judging                       Pbi ∈ E (Section 3), partitioned into K modules
                                                             M1 , M2 , . . . , MK . In practice, each module stores
                                                             explicit statements and inference links as proof
If a judge is noisy, we can reduce uncertainty by
                                                             steps or step-typed edges, declarations elicited
repeating local judgments and aggregating.
                                                             from nl as IR terms, and resolved symbol iden-
Assumption 4 (Binary per-audit-unit judge with               tifiers referenced against Γ. Optional alignment
primitive error rate). For each property k, each             metadata ties spans or claim units back to nl. The
elicited object Pb ∈ E, and each audit unit u of             object Pbi is the optimization variable, and refine-
property k on Pb as defined in Section A.1 (Pb itself        ment changes it through localized edits.
for k ∈ {glb, doc}, a module M ∈ Pb for k ∈
{syn, typ, bnd, gnd}, an explicit statement pbj ∈            Intrinsic property vector in practice. The full
                                                             instantiation of q in this paper uses the audit-unit
Pb for k = sp, or a source claim unit c ∈ C(nl) for
                                                             axes of Section 3.1, organized by the prover stage
k = cov), the latent value qk (u) ∈ {0, 1} admits
                      (t)                                    at which each is decided. The global axis ξglb is
a judge estimate ξk (u) ∈ {0, 1} on the t-th call,           read off the prover’s end-to-end acceptance ver-
t ∈ {1, 2, . . .}, with                                      dict on Pb. The document axis ξdoc is read off the
                                                             prover’s parse-only verdict on Pb as a source arti-
            (t)
          P ξk (u) ̸= qk (u) ≤ η < 12 .                      fact, before elaboration. Sentence-level ξsyn and
                            
                                                             ξtyp aggregate the parser and type-checker verdicts
                                                             across statements; inter-sentence ξbnd aggregates
Calls are taken to be mutually independent both
                                                             the binding-resolution verdicts across statements
across repetitions t and across audit units of the
                                                             within each module. The cross-domain axes are
same property. We take η as a primitive per-audit-
                                                             LLM-judged with decomposed criteria: ξgnd ag-
unit misclassification rate. The strict inequality
                                                             gregates per-symbol grounding verdicts against nl
η < 1/2 asks only that the judge be informative
                                                             and Γ, ξsp aggregates per-statement faithfulness
on average, the necessary condition for majority-
                                                             verdicts, and ξcov aggregates per-source-claim-unit
vote amplification (Lemma 1) to apply, and is com-
                                                             completeness verdicts. Each coordinate lies in
fortably satisfied by kernel-verified judges (where
                                                             [0, 1], yielding q(Pb) ∈ [0, 1]m with m = 8 in this
η ≈ 0) and by well-calibrated LLM judges on fo-
                                                             paper (the kernel-decided and cross-domain axes
cused per-property checks.
                                                             enumerated in Section 3.1).
   The independence assumption is the strongest
                                                             D.2    Judge Calibration Protocol
part of Assumption 4 in our implementation: re-
peated LLM judge calls use the same model and                The misclassification rate η is empirically grounded
prompt with low-temperature decoding, so the calls           by treating intrinsic checks q as measurement
share correlated errors. The exponential bound of            ground truth wherever possible. Collect a cali-
Lemma 1 should therefore be read as an upper                 bration set of audit units sampled from AF tra-
bound under the idealised independent-call regime,           jectories along the scope at which each axis is
and the achievable suppression in practice is closer         defined in Section A.1: whole elicited objects Pb
to ηeff ∝ η under high correlation. Our experi-              for k ∈ {glb, doc}, modules drawn from defini-
ments do not exploit the exponential rate as a quan-         tion blocks, binding sites, and reference sites for
titative prediction; we report only the qualitative          k ∈ {syn, typ, bnd, gnd}, individual explicit state-
direction that increasing T is expected to be non-           ments pbj for k = sp, and source claim units in nl
worsening for the plateau under the independent-             for k = cov.
call regime, and we do not claim empirical verifi-              For each audit unit u and property k, compute
cation on the saturated benchmarks studied here.             the ground-truth value qk (u) through the kernel, the

                                                        12
released gold formalization, or a small reviewer-             E   Proofs
facing annotation subset (depending on benchmark
                                                              Proof of Theorem 1. Taking expectations on both
family; see Section 5.3), and the judge value ξk (u)
                                                              sides of Assumption 2 gives
through the corresponding judge. Estimate per-
property error rates:                                                   E[gi+1 ] ≤ (1 − λ) E[gi ] + b η.

              η̂k = P[ξk (u) ̸= qk (u)].                      Unrolling the recursion,
                                                                                                   i−1
Define the global η̂ as maxk η̂k , the conservative
                                                                                                   X
                                                                  E[gi ] ≤ (1 − λ)i E[g0 ] + b η       (1 − λ)k
aggregator that matches the per-audit-unit bound                                                   k=0
of Assumption 4; the w-weighted mean of η̂k is a                                            b η 1−(1−λ)i
                                                                                                           
strictly smaller quantity that we record only as a di-                  = (1 − λ)i E[g0 ] +       λ            .
agnostic of average judge reliability. If judge calls
are stochastic, repeat them T times on the same au-           Since λ ∈ (0, 1], (1 − λ)i → 0 as i →
dit unit and aggregate by majority vote. Increasing           ∞, hence lim supi E[gi ] ≤ bη/λ. Equivalently,
T pushes the per-audit-unit misclassification rate            lim inf i E[µ⋆ (Pbi )] ≥ 1 − bη/λ. When η = 0, the
down exponentially via Lemma 1 and the plateau                plateau distance vanishes.
closer to 1, consistent with the amplification lever          Proof of Lemma 3. Let Ri be the number of con-
of the proxy-convergence law (Section 4).                     straints repaired at cycle i and Ri′ the number of
                                                              newly violated constraints introduced. Conditional
D.3   Refinement Operators and Bounded                        on Ui > 0, Assumption 3(i) gives E[Ri | Pbi ] ≥ ρ,
      Regress                                                 and Assumption 3(ii) gives E[Ri′ | Pbi ] ≤ κ. The
Define a finite set of repair operators A that act            update is Ui+1 = Ui − Ri + Ri′ , so E[Ui+1 | Pbi ] ≤
on a localized target t, as listed in Section 5. The          Ui − ρ + κ. Dividing by n(Pbi ) gives the stated
set covers binding, definition, step, and coverage            recursion on 1 − µ⋆ .
repairs. Each operator must act on a small context,
                                                              Proof of Lemma 1. Fix k, Pb, and an audit unit u
and its effect on q must be verifiable. For each
                                                              of property k on Pb as defined in Section A.1. Un-
iteration record
                                                              der Assumption 4, the T independent judge calls
                                                                 (t)
           ∆qi = q(Pbi+1 ) − q(Pbi ),                         {ξk (u)}Tt=1 have error indicators with mean at
                                                              most η < 1/2. The majority vote errs only if
           ∆µ⋆i = µ⋆ (Pbi+1 ) − µ⋆ (Pbi ).                    strictly more than T /2 of the calls err; by Hoeffd-
                                                              ing’s inequality,
Bounded regress is empirically supported if nega-                       " T                               #
tive jumps are rare and shallow, or are compensated                        X       (t)
                                                                         1                              1
by subsequent iterations.                                              P T      1[ξk (u) ̸= qk (u)] > 2
                                                                           t=1
                                                                           ≤ exp − 2T ( 12 − η)2 .
                                                                                                
D.4   Estimating Drift Parameters
The theorem-level recursion E[1 − µ⋆i+1 ] ≤ (1 −              Proof of Lemma 2. Fix Pb, and let Nk (Pb) denote
λ)(1 − µ⋆i ) + bη can be fit empirically without over-        the audit-unit count for property k as defined in
fitting. Let gi = 1 − µ⋆i and fit gi+1 = a gi + c + ϵi        Section A.1: Nk (Pb) = 1 for k ∈ {glb, doc},
with a ≈ 1 − λ and c ≈ bη. Estimate confidence                Nk (Pb) = PK for k ∈ {syn, typ, bnd, gnd},
intervals by bootstrapping over instances. The pre-           Nsp (Pb) = M |M |, and Ncov (Pb) = |C(nl)|. By
dicted plateau is g∞ ≈ c/(1 − a), equivalently                Assumption 4 the judge values ξk (u) ∈ {0, 1} over
µ⋆∞ ≈ 1 − c/(1 − a). To validate the η-dependence             the audit units of property k are mutually indepen-
rather than merely fit a curve, vary η experimen-             dent, so ξk (Pb) − qk (Pb) is the centered average
tally. The interventions can change the judge con-            of Nk (Pb) independent indicators in [−1, 1], each
text window size, change T , inject controlled noise          with E|ξk (u) − qk (u)| ≤ η. Hoeffding’s inequality
into judge outputs, or swap judge models. If c                on the bounded summands ξk (u) ∈ [0, 1] around
scales linearly with measured η while a is stable             their means gives, for any t > 0,
or degrades predictably, this supports the plateau
                                                              P |ξk (Pb) − Eξk (Pb)| > t ≤ 2 exp(−2Nk (Pb) t2 ),
                                                                                        
theory.

                                                         13
and the bias bound |Eξk (Pb) − qk (Pb)| ≤ η yields            H    Direct Few-Shot Baseline
|ξk (Pb) − qk (Pb)| ≤ η + t on the same high-                      Configuration
probability event. A union bound over k ∈
{1, . . . , m} gives                                          The baseline used in Section 5.2 runs the same
                                                              seven backbones at temperature 0.2 producing one
                                       
       P max |ξk (Pb) − qk (Pb)| > η + t                      sample per instance, with no resampling or majority
          k                                                   voting; the instance set per benchmark matches the
           ≤ 2m exp − 2 Nmin (Pb) t2 ,
                                         
                                                              main evaluation. The few-shot pools contain three
                                                              demonstrations per (dataset, benchmark) setting,
whereqNmin (Pb) = mink: wk >0 Nk (Pb). Choosing               matched to the target distribution.
                                                                 For miniF2F and ProofNet the three Lean 4
t = log(2m/δ)/(2Nmin (Pb)) makes the right-
                                                              demonstrations are drawn from the validation split
hand side equal to δ. Since w ∈ Rm         ≥0 with            (disjoint from the test split used for evaluation):
                       ⋆
                                P
∥w∥1 = 1, |b
           µ(P ) − µ (P )| ≤ k wk |ξk − qk | ≤
               b         b
                                                              the miniF2F pool covers a no-hypothesis numer-
maxk |ξk − qk |, and the stated bound follows.                ical identity, an N-typed divisibility goal with a
                                                              single hypothesis, and a real-typed proportion goal;
F   Theory-Aligned Aggregates                                 the ProofNet pool covers a negation-of-existence
                                                              statement, a goal with an instance-binder hypothe-
Table 6 reports the cross-backbone aggregate of the           sis, and a polynomial-irreducibility statement that
multi-seed trajectory evaluation along the proxy-             exercises typeclass binders.
side columns µ⋆0 , µ⋆∞ , and pass rate, complement-
                                                                 For e-SNLI and ProntoQA no published David-
ing the per-backbone pass-rate breakdown in Ta-
                                                              sonian or FOL Isabelle pool is available. We dis-
ble 2 in the main body.
                                                              close the data-provenance asymmetry explicitly:
                                                              each three-shot pool is drawn from clean iter-1 gen-
G    Dataset Details                                          erations in our own loop runs, with instances held
                                                              out from the test split used for evaluation; selection
Table 7 summarizes sample sizes, splits, and judge-
                                                              criteria are kernel acceptance, zero failed proxy di-
stressed coordinates per benchmark. For the two
                                                              mensions, and stylistic regularity. Concretely, the
formal-proof benchmarks (miniF2F, ProofNet) we
                                                              e-SNLI pool covers an event-typed entailment, an
use the standard test splits in their entirety. The
                                                              entity-typed entailment with a single attribute, and
four-dataset axiomatization stresses different sub-
                                                              a multi-attribute entailment; the ProntoQA pool
sets of the per-axis q vector: on Lean both ground-
                                                              covers two True-label rule chains and one False-
ing ξgnd (for symbol-resolution against mathlib)
                                                              label chain so that the literal-hypothesis shows
and statement-level semantic preservation ξsp are
                                                              clause is illustrated for both polarities.
judge-estimated; on ProofNet coverage ξcov addi-
tionally enters because the library-alignment re-                This setup favors the baseline relative to a hypo-
quirement leaves residual claim units that the can-           thetical pool drawn from unfiltered LLM outputs
didate may not represent. On Isabelle both ξsp                and therefore makes the baseline a tighter (rather
and ξcov are judge-estimated because the natural-             than looser) point of comparison; on datasets
language source admits multiple valid Davidsonian             where iter-1 generation quality is itself a confound
or FOL renderings.                                            (miniF2F, ProofNet), we use the disjoint valida-
                                                              tion pools above. The single-shot output is scored
   For e-SNLI we follow the sampling strategy of
                                                              through the same evaluation pipeline as the loop
Valentino et al. (2021), which selects instances to
                                                              (kernel prover plus per-axis proxy ξ); the external
maximize representativeness and mutual exclusiv-
                                                              oracle of Section 5.3 is not run on baseline outputs.
ity across syntactic and semantic features; our sub-
set draws 100 entailment-labeled items for which
the bidirectional ATP oracle has a well-defined               I   Extended Judge-Calibration Analysis
positive ground truth. For ProntoQA we draw a
200-sample subset from the official dev split with            This appendix collects analysis material moved out
approximately balanced True- and False-label rule             of Section 5.3 for space. The oracle referenced
chains (103/97). All splits are disjoint from the few-        throughout is the approximate stand-in for the gold
shot demonstration pools described in Section H.              label introduced in Section 5.3.

                                                         14
Table 6: End-to-End Trajectories: Cross-Backbone Aggregate. Each row pools instances from all seven
backbones and both methods (single-shot baseline and our refinement framework). µ⋆0 and µ⋆∞ are the initial and
final audit-unit scores; Pass Rate (%) is the prover’s acceptance on Pb∞ .

              Domain         Prover       Benchmark                 µ⋆0         µ⋆∞       Pass Rate (%)
              Explanation    Isabelle     e-SNLI                  0.95±0.09   0.96±0.09       81.6
              Explanation    Isabelle     ProntoQA (2799/2800)    0.99±0.05   0.99±0.03       98.1
              Math           Lean         miniF2F                 0.94±0.10   0.95±0.11       78.8
              Math           Lean         ProofNet                0.89±0.12   0.89±0.14       47.6


Table 7: Benchmark Details. n is the evaluation sample         by-instance across driver seeds. On miniF2F that
size; “judge-stress” indicates which q coordinates are         variability is largest (σ ≈ 5.6%); on ProofNet
LLM-estimated on this dataset.
                                                               (3.7%), e-SNLI (2.0%), and ProntoQA (1.8%) the
  Benchmark Prover n        Split Judge-Stressed Axes
                                                               dataset’s tighter acceptance template narrows the
                                                               dispersion.
  miniF2F     Lean 4 244 Test     ξgnd , ξsp
  ProofNet    Lean 4 182 Test     ξgnd , ξsp , ξcov            Proxy and oracle move in opposite directions on
  e-SNLI      Isabelle 100 Test   ξsp , ξcov
  ProntoQA    Isabelle 200 Dev    ξsp , ξcov                   saturating Isabelle ProntoQA. The DeepSeek-
                                                               V3.1 ProntoQA panel is the only setting where the
                                                               proxy rises monotonically while the oracle declines:
The oracles are themselves proxies, not                        between iter 1 and iter 2 the proxy gains 1.4% and
ground truth. On math (miniF2F, ProofNet)                      the oracle pass rate drops by 2.4% across all three
a ref-anchored GPT-5.4 judge produces a bi-                    seeds, so the divergence is not a cohort-aggregation
nary ours_correct verdict from the natural-                    artifact. Iter-1 candidates already satisfy the ker-
language statement, gold reference, and candidate;             nel and most per-axis judges at µ    b ≈ 0.97, and
on explanation (e-SNLI, ProntoQA), a bidirectional             the loop’s residual repair signal targets SP and
ATP probes the hypothesis and its negation against             COV verdicts on a small remainder. The bidirec-
the candidate’s formal context, and the pair is                tional ATP probe is more sensitive to axiomati-
mapped through the dataset label. Neither the math             zation soundness than to any single hypothesis’s
oracle nor the explanation oracle is reference-grade.          derivability, and tightening the axiomatization in
The math oracle compares two LLMs at different                 service of SP/COV can eliminate the incidental
capacity tiers, and the explanation oracle can be              derivability paths the iter-1 over-permissive axiom-
satisfied incidentally by an over-permissive axioma-           atization relied on, dropping a handful of fixtures
tization. We therefore decline to identify the oracle          from yes to partial. The other three panels
distance with η and report no point estimate of λ   b          show no such divergence because their iter-1 proxy
or ηbeff .                                                     is well below ceiling.

Oracle and proxy bands measure different noise                 Cross-seed oracle voting reduces single-sample
sources. The seed-bands on the DeepSeek-V3.1                   LLM-judge noise in the calibration setup. The
row carry different widths for the two curves. The             math oracle (temperature-0 ref-anchored GPT-5.4)
proxy curve reports the driver-visible composite               is deterministic at the call level but its tristate
(kernel-decided dimensions and the LLM-judged                  output, {yes, no, partial}, is per-instance and
SP/COV verdicts) and is the signal the loop early-             can collapse to a different bucket on small per-
stops on; per-instance verdicts feed back into re-             turbations of the candidate. On DeepSeek-V3.1
finement so the cohort mean converges narrowly                 ProofNet the per-instance terminal verdict differs
across seeds (σ ≤ 3.0% on every dataset, peaking               across three driver seeds for 11.5% of instances
on ProofNet and tightening to 1.2% on ProntoQA).               even after restricting to non-abstention seeds (35%
The oracle curve reports a separate per-instance               of seed-instance pairs land on partial and
whole-object verdict from a deterministic external             are treated as abstentions). A majority rule
scorer queried independently of refinement; with               (yes/no/partial→+1/−1/0; sign of the sum)
no aggregation across axes and no driver coupling,             keeps the cohort pass rate within ±1.2% of any
the cohort-mean seed-band is a direct projection of            seed ([80.9, 82.1]% across four views) and cuts ab-
how much the final formalization varies instance-              stentions from 51–61 per cohort to 48.


                                                          15
