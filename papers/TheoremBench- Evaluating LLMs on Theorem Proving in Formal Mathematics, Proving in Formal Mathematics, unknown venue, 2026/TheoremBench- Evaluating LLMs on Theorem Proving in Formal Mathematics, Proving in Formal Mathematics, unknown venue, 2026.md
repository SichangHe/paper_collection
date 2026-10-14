                                            TheoremBench: Evaluating LLMs on Theorem
                                                  Proving in Formal Mathematics

                                         QuocViet Pham1,2[0009−0005−5880−9608] , Elvir Karimov1,4[0009−0002−3198−6186] ,
                                                    Andrey Galichin1,3,4[0009−0002−5918−1435] , and Ivan
                                                              Oseledets1,3[0000−0003−2071−2163]
                                                          1
                                                           Skolkovo Institute of Science and Technology
                                                                         2
                                                                           HSE University
arXiv:2606.09450v1 [cs.AI] 8 Jun 2026




                                                           3
                                                             Artificial Intelligence Research Institute
                                                                            4
                                                                               Sberbank
                                            {QuocViet.Pham, elvir.karimov}@skoltech.ru, a.v.galichin@mtuci.ru,
                                                                  ivan.oseledets@gmail.com



                                              Abstract. LLMs have recently achieved strong results on formal proving
                                              benchmarks. However, existing evaluations remain heavily concentrated
                                              on competition-style problems and often fail to capture how models be-
                                              have on longer, more dependency-rich mathematical developments. We
                                              introduce TheoremBench, a Lean4 benchmark designed to evaluate
                                              theorem provers beyond contest settings. The benchmark is built from
                                              nearly one hundred classical theorems and is released in two comple-
                                              mentary forms: a plain main version containing one target theorem per
                                              instance, and a premised version that expands each theorem into a struc-
                                              tured family of related proving tasks consisting of the main theorem
                                              together with automatically extracted supporting subtheorems. This de-
                                              sign enables evaluation of not only whether the final theorem was proved
                                              from scratch, but also of partial progress through the internal proof
                                              structure of a theorem. Our experiments show that explicit premises
                                              substantially improve performance for Lean4-capable prover models. To
                                              provide a comprehensive evaluation, we introduce theorem-level coverage
                                              and token-efficiency metrics that expose qualitative differences in proof
                                              behavior. The results show that current provers remain strongly biased
                                              toward easy subtheorems and often solve theorems through long and
                                              inefficient tactic traces rather than compact proof plans. TheoremBench
                                              therefore provides a more fine-grained view of formal reasoning ability and
                                              highlights the importance of structural benchmark design for evaluating
                                              Lean4 theorem provers.

                                              Keywords: Formal Math · Lean4 · LLMs · benchmark


                                        1    Introduction
                                           Formal proof assistants such as Lean4 encode mathematical statements and
                                        proofs so that every inference is checked by a trusted kernel [22]. With libraries
                                        such as mathlib [7], they support large-scale, reusable formal mathematics. This
2         Q. Pham et al.

makes Lean theorem proving a useful testbed for LLM reasoning: unlike natural-
language answers, generated proofs are accepted or rejected by a verifier.
    LLM-based provers have advanced rapidly on competition-style benchmarks.
Kimina-Prover [30], DeepSeek-Prover-V2k [26], Goedel-Prover [18], and related
ATP-augmented systems combine language modeling, search, reinforcement learn-
ing, and verifier feedback. Yet Lean proving remains difficult: a model must
generate valid code, instantiate implicit arguments, select mathlib lemmas, re-
spect namespaces and notation, and satisfy the type checker.
    Benchmarks such as MiniF2F [43], PutnamBench [29], ProverBench [26], Com-
biBench [20], and FormalMATH [42] have driven progress, but mainly evaluate
standalone contest-style statements. Real Lean developments are more structured:
final theorems depend on intermediate lemmas, local definitions, typeclass as-
sumptions, namespaces, and prior results. Thus, final-statement evaluation often
hides whether a model can use or reconstruct the surrounding proof structure.
    We introduce TheoremBench, a Lean4 benchmark for this intermediate regime.
It is based on classical mathematical theorems inspired by Wiedijk’s list of
100 theorems [33] and has two forms. The plain-main dataset presents each
target theorem as a standalone final statement. The premised dataset expands
each theorem into related Lean instances: the main theorem and automatically
extracted subtheorems, with relevant prior results exposed as explicit premise
binders. This supports evaluation of both final success and partial progress
through the proof structure.
    A final theorem statement often lacks the context needed to recover supporting
lemmas, while accumulating lemmas into long prompts scales poorly. Theorem-
Bench instead embeds selected dependencies directly into theorem declarations as
explicit assumptions, producing self-contained Lean snippets. This transformation
must preserve imports, namespaces, implicit binders, typeclass inference, notation,
and local context, yielding a controlled and diagnostic evaluation setting.
    Our experiments show that explicit premises reduce difficulty only for models
able to exploit them. DeepSeek-Prover-V2-7B and Goedel-Prover-V2-8B benefit
strongly, Kimina-Prover-Distill-8B improves modestly, and Goedel-Prover-SFT
shows almost no gain. The premised structure also enables theorem-level analysis:
we measure how many supporting subtheorems are proved and how close a model
comes to completing a full theorem group.
    Our contributions are:

    – We introduce TheoremBench, a Lean4 benchmark for mid-level classical
      theorems beyond competition-style datasets.
    – We propose a premised representation that converts relevant prior Lean results
      into explicit premise binders, producing self-contained dependency-aware
      proving instances.
    – We add theorem-level coverage and token-efficiency metrics, showing differ-
      ences in premise use, proof-structure coverage, and proof compactness beyond
      pass@k.
                              TheoremBench: LLMs in Formal Mathematics           3




Fig. 1: Performance comparison of Lean4-capable theorem provers in the plain
main and premised settings, indicating their theorem fully-proved ability. Premises
help substantially for DeepSeek and Goedel-Prover-V2-8B, modestly for Kimina,
and nothing for non-reasoning model Goedel-Prover-SFT.


2   Related Work

Autoformalization and proof assistants. Autoformalization maps informal math-
ematical statements and proofs to verifier-checkable formal code. Early LLM-
based work showed that informal competition problems can be translated into
formal statements and used to improve proving performance [34], while ProofNet
connected informal and formal undergraduate mathematics through aligned
statements and proofs [2]. Surveys cover the broader development of autoformal-
ization, neural theorem proving, premise selection, proof-step generation, search,
synthetic data, and evaluation protocols [32,16]. A central difficulty is the gap
between informal notation and formal syntax: Lean, Isabelle, and Coq require
exact binders, types, references, and proof terms [22,24,5]. Lean4 is especially
relevant because it combines a proof assistant with a programming language
and is supported by mathlib [1,7], but this also exposes models to namespaces,
typeclass inference, scoped notation, and evolving APIs [31,41].

LLM-based formal theorem proving. Neural theorem proving predates current
LLM provers: GamePad studied Coq proof-state learning [11], TacticToe learned
tactic search in HOL4 [9], HOList and DeepHOL framed higher-order theorem
proving as reinforcement learning [4], and CoqGym provided a large Coq dataset
with AST-based tactic generation [38]. LLM provers extend this line by generating
4      Q. Pham et al.




Fig. 2: Performance of models on the premised benchmark. DeepSeek-Prover-V2-
7B consistently achieves the highest success rate, followed by Goedel-Prover-V2-
8B, Kimina-Prover-Distill-8B, and Goedel-Prover-SFT


candidate proofs checked by the proof assistant. GPT-f demonstrated accepted
formal proof generation [25]; LeanDojo made Lean interaction and retrieval-
augmented proving reproducible, emphasizing premise selection as a mathlib-
scale bottleneck [39]. ReProver [39], REAL-Prover [27], BFS-Prover [37], and
HUNYUANPROVER [15] combine retrieval, search, synthetic data, and verifier
feedback. Other systems target premise selection, search, repair, or decomposition:
Thor [12], Magnushammer [21], Draft, Sketch, and Prove [13], HyperTree Proof
Search [14], Baldur [8], and COPRA [28]. Lean-specific scaling efforts include
Llemma [3], TheoremLlama [31], Lean Workbook [41], and LeanNavigator [40].

Benchmarks. Formal-proving benchmarks have evolved from large proof-assistant
environments to competition and curriculum-style datasets. HOList and CoqGym
provide large-scale testbeds for HOL Light and Coq [4,38]; LeanDojo provides a
Lean interaction framework with premise annotations and generalization splits
[39]. MiniF2F targets olympiad-style problems [43], PutnamBench raises the level
to undergraduate competition mathematics [29], ProofNet and FIMO connect
informal and formal undergraduate or IMO-style reasoning [2,19], CombiBench
stresses combinatorics [20], FormalMATH expands Lean4 evaluation to thousands
of problems [42], and ProverBench evaluates modern Lean provers in the DeepSeek-
Prover-V2 setting [26]. Most of these datasets evaluate standalone theorem
statements. TheoremBench instead evaluates classical Lean developments through
                                TheoremBench: LLMs in Formal Mathematics         5

an explicit premised structure, making supporting subtheorems visible benchmark
instances rather than hidden context.


               Dataset         Samples            Difficulty        Success
        miniF2F [43]         244         Highschool, AIME            90.4%
        PutnamBench [29]     658         Undergraduate               13.07%
        ProverBench [26]     325         AIME                        59.1%
        ProofNet [2]         186         Undergraduate               37.1%
        CombiBench [20]      100         Undergraduate               12%
        FormalMATH-Lite [42] 425         Highschool, Undergraduate 54.11%
        FormalMATH-All [42] 5560         Highschool, Undergraduate -
        TheoremBench (Ours) 1142         Undergraduate, Postgraduate 54.91%

Table 1: Current popular benchmarks and reported success of strong prover
models.




Evaluation metrics and efficiency. LLM-based formal proving is usually evaluated
by pass@k: a theorem is solved if one of the first k generated attempts is accepted
by the verifier. This follows code-generation evaluation [6] and is standard in
MiniF2F [43], LeanDojo [39], DeepSeek-Prover [26], Kimina-Prover [30], Goedel-
Prover [17], and FormalMATH [42]. Since pass@k ignores efficiency, search-based
provers also report explored states, verifier calls, CPU time, and depth, as in
HyperTree Proof Search [14], DeepSeek-Prover-V1.5 [36], BFS-Prover [37], and
APOLLO [23]. Proof quality adds another axis: Baldur and COPRA study repair
and interactive/backtracking behavior [8,28], InternLM2.5-StepProver reports
proof length and CPU usage [35], and ProofOptimizer trains models to shorten
Lean proofs [10]. TheoremBench follows this diagnostic direction by retaining
pass@k while adding theorem-level coverage, fully proved parent counts, and
token-efficiency.

3      TheoremBench Dataset Construction
    TheoremBench is a Lean4 benchmark for evaluating theorem provers on
classical mathematical theorems beyond competition-style tasks. The benchmark
is constructed from Lean4 formalizations of classical results inspired by Freek
Wiedijk’s list of 100 theorems [33]. Unlike benchmarks centered on compact
olympiad-style statements, these formalizations usually appear inside larger Lean
developments and depend on imported theories, local definitions, namespaces,
typeclass assumptions, and intermediate lemmas.

3.1     Construction Pipeline
      For each source file, we construct the dataset as follows:
6      Q. Pham et al.




Fig. 3: TheoremBench construction pipeline. Lean4 source files are parsed into
theorem groups, enriched with required formal context, transformed into plain-
main and premised instances, and verified by Lean4 before inclusion in the
benchmark.


1. We collect raw Lean4 theorem developments from classical formalizations
   inspired by Wiedijk’s list of 100 theorems [33]. Each source file corresponds
   to one parent theorem and contains the final theorem together with its
   surrounding Lean development.
2. For each parent theorem, we parse the Lean file into a theorem group. The final
   declaration is treated as the main theorem, and the required Lean context is
   reconstructed so that the extracted instance can compile independently. Each
   parent theorem also provides supporting theorem and lemma declarations,
   which we extract as subtheorems and use to build the premised dataset.
3. For every theorem or subtheorem, earlier results used in its proof are con-
   verted into explicit premise binders. We then emit a self-contained Lean4
   snippet, verify it with Lean4, keep only compilable instances, and store each
   instance with its theorem-level ID, Lean declaration name, extracted premises,
   environment context, and ground-truth proof.

    This procedure produces two aligned dataset views. The plain-main version
contains one standalone final theorem per parent theorem. The premised version
expands the same parent theorem into a group of related proving tasks, consisting
of the main theorem and its extracted supporting subtheorems. Figure 3 illustrates
the full construction pipeline.
                               TheoremBench: LLMs in Formal Mathematics             7




      Fig. 4: Distribution of TheoremBench instances by mathematical field.


3.2    Dataset Statistics
     TheoremBench covers a broad range of undergraduate and postgraduate math-
ematics, including algebra, number theory, real and complex analysis, geometry,
topology, set theory, logic, combinatorics, probability, and abstract algebra. The
difficulty of instances also varies substantially: some require short local reasoning,
while others depend on many auxiliary lemmas, definitions, tactics, and explicit
binders from mathlib or from earlier results in the same source file.
     We estimate difficulty using both LLM-based classification and Lean4-level
structural features, including proof length, referenced declarations, tactic usage,
and the number of mathematical fields involved. Figure 4 summarizes the field
distribution of the benchmark.


4     Experiments and Discussion
4.1    Evaluation metrics
    We evaluate model performance using both standard instance-level metrics
and additional theorem-level metrics that are specific to the premised structure
of TheoremBench.

Pass@k. For a theorem instance, let r1 , . . . , rk denote the first k generated proof
attempts, and let si ∈ {0, 1} indicate whether attempt i is accepted by Lean4.
We define                                              !
                                             k
                           Pass@k = 1
                                           _
                                                 si = 1 .                          (1)
                                           i=1
8       Q. Pham et al.

At the dataset level, pass@k is the mean of this indicator over all theorem
instances. We report pass@k for powers of two up to kmax = 64, which reveals
both final success and sample-efficiency scaling.

Fully proved parent theorem. In the premised dataset, a parent theorem is
considered fully proved if and only if the model proves the main theorem together
with all of its associated subtheorems. This metric is substantially stricter than
instance-level pass@k, because a parent theorem is counted as solved only when
the entire proof structure has been completed.

Theorem-level coverage. For each parent theorem T , let m(T ) be the total
number of subtheorems in its theorem group and let p(T ) be the number proved
successfully by the model. We define theorem-level coverage by

                                           p(T )
                               Cov(T ) =         × 100.                               (2)
                                           m(T )

This allows us to study partial progress even when the full theorem group is not
solved. In addition to average coverage, we report a survival-style curve showing
the fraction of parent theorems whose coverage is at least a chosen threshold.

Average subtheorems proved per theorem. To provide a direct interpretation of
model progress within a decomposed theorem, we also compute the average
number of proved subtheorems per parent theorem:

                                            1 X
                               AvgSub =         p(T ),                                (3)
                                            N
                                                T

where N is the number of parent theorems. This metric answers the practical
question: if a theorem is decomposed into intermediate obligations, how many of
them will the model solve on average?

Token-efficiency. For every solved subtheorem instance, we compare the token
length of successful generated proofs against the token length of the ground-
truth Lean proof. Let ℓgt (T ) denote the token count of the reference proof, and
let ℓgen,1 (T ), . . . , ℓgen,m (T ) denote the lengths of all successful generated proofs
among the sampled attempts. We define
                              1
                                Pm
                             m     j=1 ℓgen,j (T )                minj ℓgen,j (T )
            Eavg (T ) =                            , Emin (T ) =                   .   (4)
                                    ℓgt (T )                          ℓgt (T )

Before tokenization, we remove non-Lean explanatory prose and comments from
generated outputs, so the metric reflects proof text rather than natural-language
reasoning. Values above 1 indicate that the model tends to produce longer proofs
than the reference proof, while values near or below 1 indicate more compact
outputs.
                             TheoremBench: LLMs in Formal Mathematics           9

Plain-main versus premised comparison. Since the plain-main and premised
datasets represent the same underlying theorem families at different structural
levels, we also compare pass@64 across the two settings on the theorem units that
are shared between them. This comparison measures whether explicit premises
help models solve the final theorem more effectively.

4.2   Evaluating Formal Theorem Provers
    We evaluate four Lean4-capable provers on two aligned versions of Theorem-
Bench: DeepSeek-Prover-V2-7B[26], Goedel-Prover-V2-8B[18], Kimina-Prover-
Distill-8B[30], and the non-reasoning Goedel-Prover-SFT model[17] as baseline.
    The plain-main benchmark contains one standalone target theorem per parent
theorem. The premised benchmark expands the same parent theorem into a group
of related instances, including the main theorem and automatically extracted
supporting subtheorems. All instances in a group share the same theorem-level
ID, while each retains its own Lean4 declaration name.
    This setup lets us compare final-statement proving with structured proof
completion. It tests whether explicit premises reduce difficulty and whether
models can complete a theorem’s internal proof structure rather than only
isolated statements.
    All instances are verified with Lean4 using an automated pipeline that records
compilation outcomes, resource usage, and structural statistics. We also keep
ground-truth proofs for token-level comparison with generated proofs. Each
theorem or subtheorem is sampled up to kmax = 64 times, and every candidate
proof is checked by Lean4. We report both standard instance-level metrics and
theorem-level metrics specific to the premised benchmark.

4.3   Main empirical results
Subtheorem-level proving performance. Figure 2 shows the pass@k curves on
the premised benchmark. All models improve monotonically as the generation
budget increases, but the ranking remains stable throughout the entire range.
DeepSeek-Prover-V2-7B is the strongest model at every value of k, reaching
approximately 0.46 pass@64. Goedel-Prover-V2-8B is the second strongest at
roughly 0.33, followed by Kimina-Prover-Distill-8B at roughly 0.22, while Goedel-
Prover-SFT remains substantially lower at about 0.11. Since the same ranking is
already visible at k = 1 and k = 2, the gap cannot be explained purely by larger
sampling budgets; it reflects a real difference in first-attempt and low-budget
proving quality.

Impact of explicit premises. Figure 1 compares plain-main and premised theorem
proving at pass@64 on the theorem units shared between both dataset versions.
The results show that explicit premises reduce benchmark difficulty substantially,
but the gain depends strongly on the model. DeepSeek-Prover-V2-7B benefits
the most, improving from 0.053 on plain-main theorems to 0.263 on premised
theorems. Goedel-Prover-V2-8B also improves substantially, from 0.053 to 0.123.
10     Q. Pham et al.

Kimina-Prover-Distill-8B improves only modestly, from 0.053 to 0.070. In contrast,
Goedel-Prover-SFT shows essentially no difference, remaining at 0.035 in both
conditions. These results indicate that explicit premises are useful only when the
prover is able to exploit the additional structure effectively.

Theorem-level completion behavior. Instance-level pass@k alone does not show
how close a model comes to finishing a full parent theorem. Figure 5 therefore
reports theorem-level coverage in survival form: for each threshold on the x-axis,
the y-value gives the fraction of parent theorems for which the model proves
at least that percentage of subtheorems. This view is more informative for the
premised dataset because it measures partial completion of a theorem’s internal
proof structure. DeepSeek-Prover-V2-7B has the strongest curve over most of the
range, which means it is the most likely model to cover a large fraction of the
subtheorems belonging to a given theorem. Goedel-Prover-V2-8B is competitive
at very low thresholds, indicating that it often makes some initial progress, but it
falls below DeepSeek at medium and high thresholds, suggesting lower probability
of approaching full completion. Kimina-Prover-Distill-8B remains behind these
two stronger models, while Goedel-Prover-SFT is weakest throughout most of
the range. Thus, DeepSeek is not only the strongest at individual subtheorem
solving, but also the most reliable at advancing substantially through an entire
theorem group.




Fig. 5: Theorem-level coverage survival curve on the premised benchmark. For
each threshold x, the y-value gives the fraction of parent theorems for which
the model proves at least x% of subtheorems. Higher curves indicate a greater
probability of approaching theorem completion.
                               TheoremBench: LLMs in Formal Mathematics           11

Token-efficiency and proof verbosity. To compare generated proofs with reference
proofs, we compute the token-efficiency ratio
                      average successful generated proof tokens for T
            E(T ) =                                                   .
                             ground-truth proof tokens for T
Before tokenization, we remove non-Lean explanatory prose and comments, so
the metric reflects proof text rather than natural-language reasoning. Figure 6
shows that successful generated proofs are usually longer than the corresponding
reference proofs. Goedel-Prover-V2-8B is the most verbose model, with median
token-efficiency around 16, followed by DeepSeek-Prover-V2-7B at around 7.8.
Kimina-Prover-Distill-8B is more compact, with median around 3.6. Goedel-
Prover-SFT has the lowest median, about 1.44, but this reflects a much smaller
and more selective solved subset rather than uniformly better proof compactness.




Fig. 6: Overall token-efficiency distribution on solved premised instances. Values
above 1 indicate that the model’s successful proofs are longer than the corre-
sponding reference proofs.



Discussion. Taken together, the results give a consistent picture of current Lean4
theorem-proving behavior. First, DeepSeek-Prover-V2-7B is the strongest overall
model on TheoremBench under the premised setting, both in subtheorem pass@k
and in theorem-level completion. Second, the premised representation is genuinely
helpful, but only models that can use explicit auxiliary structure effectively obtain
substantial gains from it. Third, performance is strongly biased toward easy
12      Q. Pham et al.

subtheorems and toward a subset of mathematical fields, which shows that broad
formal mathematical competence is still far from achieved. Finally, even when
models succeed, their proofs are usually much longer than the corresponding
ground-truth proofs, suggesting that correctness is often reached through verbose
tactic exploration rather than compact proof planning. TheoremBench therefore
exposes not only whether a theorem prover succeeds, but also how it succeeds,
how far it progresses within a structured proof, and how efficiently it uses the
formal context it is given.


5    Limitations
    TheoremBench has several limitations. First, it is built from existing Lean4
formalizations of classical theorems, so its coverage depends on what has already
been formalized and can be extracted into compilable snippets. Second, the
premised transformation relies on syntactic dependency analysis and Lean-level
verification; although every retained instance compiles, premise extraction may
not always recover the mathematically minimal dependency set. Third, our
experiments cover four Lean4-capable prover models under a fixed sampling
budget and low model-size, leaving broader model families, search strategies, and
retrieval-augmented settings for future work.


6    Conclusion
    We introduced TheoremBench, a Lean4 benchmark for evaluating theorem
provers on classical mathematical theorems beyond compact competition-style
tasks. The benchmark provides two aligned settings: a plain-main version that
tests final-statement proving, and a premised version that exposes supporting
subtheorems and prior results as explicit premises. This structure enables more
diagnostic evaluation, measuring not only whether a model proves a final theorem,
but also how much of the underlying proof structure it can recover.
    Our experiments show that explicit premises substantially help models able
to exploit formal context, especially DeepSeek-Prover-V2-7B and Goedel-Prover-
V2-8B, while weaker or non-reasoning models benefit little. The theorem-level
coverage and token-efficiency analyses further show that current provers remain
biased toward easy subtheorems and often produce verbose proofs. These results
suggest that future Lean4 theorem provers should be evaluated not only by
pass@k, but also by their ability to use structured premises, complete proof
chains, and generate compact formal proofs.


References
 1. Avigad, J., De Moura, L., Kong, S.: Theorem proving in lean (2021)
 2. Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E.W., Radev, D., Avigad, J.:
    Proofnet: Autoformalizing and formally proving undergraduate-level mathematics
    (2023), https://arxiv.org/abs/2302.12433
                                 TheoremBench: LLMs in Formal Mathematics               13

 3. Azerbayev, Z., Schoelkopf, H., Paster, K., Dos Santos, M., McAleer, S., Jiang,
    A.Q., Deng, J., Biderman, S., Welleck, S.: Llemma: An open language model for
    mathematics (2023), https://arxiv.org/abs/2310.10631
 4. Bansal, K., Loos, S.M., Rabe, M.N., Szegedy, C., Wilcox, S.: Holist: An environment
    for machine learning of higher-order theorem proving (2019), https://arxiv.org/
    abs/1904.03241
 5. Barras, B., Boutin, S., Cornes, C., Courant, J., Filliâtre, J.C., Giménez, E., Herbelin,
    H., Huet, G., Muñoz, C., Murthy, C., Parent, C., Paulin-Mohring, C., Saïbi, A.,
    Werner, B.: The Coq Proof Assistant Reference Manual : Version 6.1. Research Re-
    port RT-0203, INRIA (May 1997), https://inria.hal.science/inria-00069968,
    projet COQ
 6. Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H.P., Kaplan, J.,
    Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger, G.,
    Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S., Ryder, N., Pavlov,
    M., Power, A., Kaiser, L., Bavarian, M., Winter, C., Tillet, P., Such, F.P., Cummings,
    D., Plappert, M., Chantzis, F., Barnes, E., Herbert-Voss, A., Guss, W.H., Nichol,
    A., Paino, A., Tezak, N., Tang, J., Babuschkin, I., Balaji, S., Jain, S., Saunders,
    W., Hesse, C., Carr, A.N., Leike, J., Achiam, J., Misra, V., Morikawa, E., Radford,
    A., Knight, M., Brundage, M., Murati, M., Mayer, K., Welinder, P., McGrew, B.,
    Amodei, D., McCandlish, S., Sutskever, I., Zaremba, W.: Evaluating large language
    models trained on code (2021), https://arxiv.org/abs/2107.03374
 7. mathlib Community, T.: The lean mathematical library. In: Proceedings of the
    9th ACM SIGPLAN International Conference on Certified Programs and Proofs.
    p. 367–381. CPP 2020, Association for Computing Machinery, New York, NY,
    USA (2020). https://doi.org/10.1145/3372885.3373824, https://doi.org/10.
    1145/3372885.3373824
 8. First, E., Rabe, M.N., Ringer, T., Brun, Y.: Baldur: Whole-proof generation and
    repair with large language models (2023), https://arxiv.org/abs/2303.04910
 9. Gauthier, T., Kaliszyk, C., Urban, J.: Learning to reason with hol4 tactics (2018),
    https://arxiv.org/abs/1804.00595
10. Gu, A., Piotrowski, B., Gloeckle, F., Yang, K., Markosyan, A.H.: Proofoptimizer:
    Training language models to simplify proofs without human demonstrations (2025),
    https://arxiv.org/abs/2510.15700
11. Huang, D., Dhariwal, P., Song, D., Sutskever, I.: Gamepad: A learning environment
    for theorem proving (2018), https://arxiv.org/abs/1806.00608
12. Jiang, A.Q., Li, W., Tworkowski, S., Czechowski, K., Odrzygozdz, T., Milos, P.,
    Wu, Y., Jamnik, M.: Thor: Wielding hammers to integrate language models and
    automated theorem provers (2022), https://arxiv.org/abs/2205.10893
13. Jiang, A.Q., Welleck, S., Zhou, J.P., Lacroix, T., Liu, J., Li, W., Jamnik, M., Lample,
    G., Wu, Y.: Draft, sketch, and prove: Guiding formal theorem provers with informal
    proofs. In: The Eleventh International Conference on Learning Representations
    (2023), https://openreview.net/forum?id=SMa9EAovKMC
14. Lample, G., Lachaux, M.A., Lavril, T., Martinet, X., Hayat, A., Ebner, G., Ro-
    driguez, A., Lacroix, T.: Hypertree proof search for neural theorem proving (2022),
    https://arxiv.org/abs/2205.11491
15. Li, Y., Du, D., Song, L., Li, C., Wang, W., Yang, T., Mi, H.: Hunyuanprover: A
    scalable data synthesis framework and guided tree search for automated theorem
    proving (2025), https://arxiv.org/abs/2412.20735
16. Li, Z., Sun, J., Murphy, L., Su, Q., Li, Z., Zhang, X., Yang, K., Si, X.: A survey on
    deep learning for theorem proving (2024), https://arxiv.org/abs/2404.09939
14      Q. Pham et al.

17. Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li, J., Xia, M., Chen, D.,
    Arora, S., Jin, C.: Goedel-prover: A frontier model for open-source automated
    theorem proving (2025), https://arxiv.org/abs/2502.07640
18. Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.H., Zhao, H., Jiang, L., Geng, Y., Ge,
    J., Sun, J., Wu, J., Gesi, J., Lu, X., Acuna, D., Yang, K., Lin, H., Choi, Y., Chen, D.,
    Arora, S., Jin, C.: Goedel-prover-v2: Scaling formal theorem proving with scaffolded
    data synthesis and self-correction (2025), https://arxiv.org/abs/2508.03613
19. Liu, C., Shen, J., Xin, H., Liu, Z., Yuan, Y., Wang, H., Ju, W., Zheng, C., Yin,
    Y., Li, L., Zhang, M., Liu, Q.: Fimo: A challenge formal dataset for automated
    theorem proving (2023)
20. Liu, J., Lin, X., Bayer, J., Dillies, Y., Jiang, W., Liang, X., Soletskyi, R., Wang,
    H., Xie, Y., Xiong, B., Yang, Z., Zhang, J., Zhi, L., Li, J., Liu, Z.: Combibench:
    Benchmarking llm capability for combinatorial mathematics (2025), https://arxiv.
    org/abs/2505.03171
21. Mikula, M., Tworkowski, S., Antoniak, S., Piotrowski, B., Jiang, A.Q., Zhou, J.P.,
    Szegedy, C., Kucinski, L., Milos, P., Wu, Y.: Magnushammer: A transformer-based
    approach to premise selection (2023), https://arxiv.org/abs/2303.04488
22. Moura, L.d., Ullrich, S.: The lean 4 theorem prover and programming language. In:
    Automated Deduction – CADE 28: 28th International Conference on Automated De-
    duction, Virtual Event, July 12–15, 2021, Proceedings. p. 625–635. Springer-Verlag,
    Berlin, Heidelberg (2021). https://doi.org/10.1007/978-3-030-79876-5_37,
    https://doi.org/10.1007/978-3-030-79876-5_37
23. Ospanov, A., Yousefzadeh, R.: Apollo: Automated llm and lean collaboration for
    advanced formal reasoning (2025), https://arxiv.org/abs/2505.05758
24. Paulson, L.: Isabelle: A Generic Theorem Prover. Lecture Notes in Computer
    Science, Springer (1994), https://books.google.ru/books?id=RxlhqG0-cGwC
25. Polu, S., Sutskever, I.: Generative language modeling for automated theorem proving
    (2020), https://arxiv.org/abs/2009.03393
26. Ren, Z.Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W., Zhang, L., Fu, Z., Zhu,
    Q., Yang, D., Wu, Z.F., Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D., Ruan,
    C.: Deepseek-prover-v2: Advancing formal mathematical reasoning via reinforcement
    learning for subgoal decomposition (2025), https://arxiv.org/abs/2504.21801
27. Shen, Z., Huang, N., Yang, F., Wang, Y., Gao, G., Xu, T., Jiang, J., He, W., Yang,
    P., Sun, M., Ju, H., Wu, P., Dai, B., Dong, B.: Real-prover: Retrieval augmented lean
    prover for mathematical reasoning (2025), https://arxiv.org/abs/2505.20613
28. Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., Chaudhuri, S.: An in-context learning
    agent for formal theorem-proving (2023), https://arxiv.org/abs/2310.04353
29. Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jennings, M., Thakur, A.,
    Chaudhuri, S.: Putnambench: Evaluating neural theorem-provers on the putnam
    mathematical competition (2024), https://arxiv.org/abs/2407.11214
30. Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos, M.D., Sung, F., Vinyes,
    M., Ying, Z., Zhu, Z., Lu, J., Saxcé, H.d., Bailey, B., Song, C., Xiao, C., Zhang, D.,
    Zhang, E., Pu, F., Zhu, H., Liu, J., Bayer, J., Michel, J., Yu, L., Dreyfus-Schmidt,
    L., Tunstall, L., Pagani, L., Machado, M., Bourigault, P., Wang, R., Polu, S.,
    Barroyer, T., Li, W.D., Niu, Y., Fleureau, Y., Hu, Y., Yu, Z., Wang, Z., Yang, Z.,
    Liu, Z., Li, J.: Kimina-prover preview: Towards large formal reasoning models with
    reinforcement learning (2025), http://arxiv.org/abs/2504.11354
31. Wang, R., Zhang, J., Jia, Y., Pan, R., Diao, S., Pi, R., Zhang, T.: Theoremllama:
    Transforming general-purpose llms into lean4 experts (2024), https://arxiv.org/
    abs/2407.03203
                               TheoremBench: LLMs in Formal Mathematics             15

32. Weng, K., Du, L., Li, S., Lu, W., Sun, H., Liu, H., Zhang, T.: Autoformalization in
    the era of large language models: A survey (2025), https://arxiv.org/abs/2505.
    23486
33. Wiedijk, F.: 100 theorems in lean, https://leanprover-community.github.io/
    100.html
34. Wu, Y., Jiang, A.Q., Li, W., Rabe, M.N., Staats, C., Jamnik, M., Szegedy, C.:
    Autoformalization with large language models (2022), https://arxiv.org/abs/
    2205.12615
35. Wu, Z., Huang, S., Zhou, Z., Ying, H., Wang, J., Lin, D., Chen, K.: Internlm2.5-
    stepprover: Advancing automated theorem proving via expert iteration on large-scale
    lean problems (2024), https://arxiv.org/abs/2410.15700
36. Xin, H., Ren, Z.Z., Song, J., Shao, Z., Zhao, W., Wang, H., Liu, B., Zhang, L.,
    Lu, X., Du, Q., Gao, W., Zhang, H., Zhu, Q., Yang, D., Wu, Z.F., Luo, F., Ruan,
    C.: Deepseek-prover-v1.5: Harnessing proof assistant feedback for reinforcement
    learning and monte-carlo tree search (2024), https://arxiv.org/abs/2408.08152
37. Xin, R., Xi, C., Yang, J., Chen, F., Wu, H., Xiao, X., Sun, Y., Zheng, S., Shen, K.:
    Bfs-prover: Scalable best-first tree search for llm-based automatic theorem proving
    (2025), https://arxiv.org/abs/2502.03438
38. Yang, K., Deng, J.: Learning to prove theorems via interacting with proof assistants
    (2019), https://arxiv.org/abs/1905.09381
39. Yang, K., Swope, A.M., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger,
    R., Anandkumar, A.: Leandojo: Theorem proving with retrieval-augmented language
    models (2023), https://arxiv.org/abs/2306.15626
40. Yin, D., Gao, J.: Generating millions of lean theorems with proofs by exploring
    state transition graphs (2025), https://arxiv.org/abs/2503.04772
41. Ying, H., Wu, Z., Geng, Y., Yuan, Z., Lin, D., Chen, K.: Lean workbook: A large-
    scale lean problem set formalized from natural language math problems (2025),
    https://arxiv.org/abs/2406.03847
42. Yu, Z., Peng, R., Ding, K., Li, Y., Peng, Z., Liu, M., Zhang, Y., Yuan, Z., Xin,
    H., Huang, W., Wen, Y., Zhang, G., Liu, W.: Formalmath: Benchmarking formal
    mathematical reasoning of large language models (2025), https://arxiv.org/abs/
    2505.02735
43. Zheng, K., Han, J.M., Polu, S.: Minif2f: a cross-system benchmark for formal
    olympiad-level mathematics (2022), https://arxiv.org/abs/2109.00110
16     Q. Pham et al.

A     Appendix
A.1   Dataset Distribution
    In total, TheoremBench contains 1,142 Lean4 proving instances across the
processed theorem groups. Table 2 summarizes the size of the extracted proof
structures. Most theorem groups contain fewer than 20 supporting subtheorems,
while a small number of long Lean developments contribute much larger groups.


      Subtheorems per theorem Theorem groups Premised instances
                  1−5                       39                  117
                 6 − 10                     9                    81
                 11 − 20                    19                  319
                 21 − 50                    14                  460
                  > 50                      2                   165
                  Total                     83                 1142
Table 2: Distribution of supporting subtheorems per parent theorem in the
retained premised dataset. A theorem group contains the main theorem and its
extracted supporting subtheorems




A.2   Additional Results
Field and difficulty coverage. Figure 7 shows model coverage over mathematical
fields and difficulty buckets. The field-level radar confirms that the benchmark
spans a broad range of topics, but model performance is highly non-uniform
across them. The strongest coverage is concentrated in algebra, analysis, number
theory, and logic/set-theoretic material, while probability, measure theory, and
several smaller fields remain much harder for all models. DeepSeek-Prover-V2-7B
and Goedel-Prover-V2-8B have the broadest field coverage, although DeepSeek
reaches the largest solved counts in the main categories. The complexity radar
reveals an equally strong skew with respect to theorem difficulty. All models solve
many more easy subtheorems than medium or hard ones. Even the strongest
systems degrade sharply as the difficulty bucket increases. This confirms that
current theorem provers remain much better at discharging short local obligations
than at sustaining long and dependency-heavy proof chains.

Additional Token-Efficiency Analysis. Figure 8 conditions token-efficiency on
theorem difficulty. For DeepSeek-Prover-V2-7B, the median token-efficiency drops
from about 9.0 on easy instances to about 3.2 on medium instances and about
1.05 on hard instances. Kimina-Prover-Distill-8B shows a similar trend, decreasing
from about 3.8 on easy instances to about 2.8 on medium instances and about 1.5
on hard instances. This suggests that, among the harder instances these models
                             TheoremBench: LLMs in Formal Mathematics          17




Fig. 7: Coverage by mathematical field and complexity bucket on the premised
benchmark. Counts are shown at vertices, while radius indicates percentage of
proved instances. Performance is strongest on easy instances and concentrated in
a subset of mathematical domains.


solve, generated proof lengths are closer to the references. Goedel-Prover-V2-8B
remains comparatively verbose even on harder buckets, while Goedel-Prover-SFT
has very small medians on medium and hard instances because it solves only a
few selected examples. Table 3 reports the aggregate token-efficiency statistics
used in the main text.




Fig. 8: Token-efficiency conditioned on theorem difficulty. The strongest solved
instances for several models become relatively more compact on harder buckets,
but sample counts are much smaller there.



Generated versus reference proof lengths. Figure 9 plots the token length of
ground-truth proofs against the average length of successful generated proofs. The
18        Q. Pham et al.


     Model                      Solved instances Median Eavg Mean Eavg Median Emin
     DeepSeek-Prover-V2-7B           529           7.78       20.72       4.69
     Goedel-Prover-SFT               127           1.44       9.65        0.20
     Goedel-Prover-V2-8B             381          16.00       42.49       8.51
     Kimina-Prover-Distill-8B        254           3.57       5.94        2.00
Table 3: Token-efficiency summary on solved premised instances. Smaller values
indicate more compact generated proofs relative to the reference Lean proofs,
but values must be interpreted jointly with solved-instance counts.




diagonal represents parity with the reference proof. Most DeepSeek and Goedel-
Prover-V2-8B points lie well above the diagonal, indicating that these models
often solve the theorem with substantially longer tactic traces than the human-
written Lean proof. Kimina-Prover-Distill-8B lies closer to the diagonal on average,
indicating more compact successful proofs. Goedel-Prover-SFT often lies closer to
or even below the diagonal, but again only on a relatively small solved subset. The
scatter therefore reinforces an important qualitative conclusion: current theorem
provers are not simply memorizing or reproducing the reference proofs. Rather,
they often reach correctness through much longer, more repetitive, and less
economical proof scripts. The low token-efficiency of Goedel-Prover-SFT should
be interpreted cautiously: it solves far fewer instances, so its compactness reflects
a highly selective solved subset rather than uniformly better proof planning.




Fig. 9: Ground-truth proof length versus average successful generated proof length.
Most successful generations lie above the diagonal, showing that current provers
typically produce longer proofs than the human-written references.
                             TheoremBench: LLMs in Formal Mathematics         19

Pass@64 summary. Table 4 summarizes the final pass@64 values used in the
main comparison plots.


         Model                      Premised pass@64 Plain-main pass@64
         DeepSeek-Prover-V2-7B           0.460             0.053
         Goedel-Prover-SFT               0.109             0.035
         Goedel-Prover-V2-8B             0.334             0.053
         Kimina-Prover-Distill-8B        0.223             0.053
Table 4: Final pass@64 results on the two benchmark settings. The premised
benchmark substantially improves performance for DeepSeek and Goedel-Prover-
V2-8B, while gains are smaller for Kimina and negligible for Goedel-Prover-SFT.




A.3   Premises structure
   Figure 10 illustrates how a supporting lemma is exposed as an explicit premise
binder in the generated theorem statement.
20       Q. Pham et al.




     Premises structure to original theorem statement


     Original Lean4 Statement


      import Mathlib.Algebra.Order.Archimedean.Basic
      ...

      theorem card_eq_index_normalizer [Fact p.Prime] [Finite (Sylow p
      ,→  G)] (P : Sylow p G) :
          Nat.card (Sylow p G) = P.normalizer.index := by
          ...

      theorem card_dvd_index [Fact p.Prime] [Finite (Sylow p G)] (P :
      ,→  Sylow p G) :
          Nat.card (Sylow p G) | P.index := by sorry


     Premised Lean4 Statement


      import Mathlib.Algebra.Order.Archimedean.Basic
      ...

      theorem card_dvd_index_premised {card_eq_index_normalizer :
       ([Fact p.Prime] → [Finite (Sylow p G)] → (P : Sylow p G) →
       Nat.card (Sylow p G) = P.normalizer.index} [Fact p.Prime]
      [Finite (Sylow p G)] (P : Sylow p G) :
          Nat.card (Sylow p G) | P.index := by sorry




Fig. 10: Example of transformation from original to premised structure. The
highlighted binder exposes a previously proved supporting lemma as an explicit
premise.
