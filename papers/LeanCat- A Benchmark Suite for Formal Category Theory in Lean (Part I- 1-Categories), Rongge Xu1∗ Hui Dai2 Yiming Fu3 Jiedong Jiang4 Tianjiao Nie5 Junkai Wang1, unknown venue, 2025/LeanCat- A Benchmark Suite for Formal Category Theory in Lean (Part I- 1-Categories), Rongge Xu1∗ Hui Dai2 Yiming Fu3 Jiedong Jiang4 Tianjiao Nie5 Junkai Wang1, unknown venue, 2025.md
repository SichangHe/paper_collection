                                         L EAN C AT: A B ENCHMARK S UITE FOR F ORMAL C ATE -
                                         GORY T HEORY IN L EAN (PART I: 1-C ATEGORIES )

                                          Rongge Xu1∗ Hui Dai2 Yiming Fu3 Jiedong Jiang4 Tianjiao Nie5 Junkai Wang1
                                          Holiverse Yang6 Zhi-Hao Zhang7
                                          1
                                            Yau Mathematical Sciences Center, Tsinghua University 2 Iluvatar CoreX 3 Department
                                          of Mathematics, Southern University of Science and Technology 4 Westlake Institute for
                                          Advanced Study, Westlake University 5 Qiuzhen College, Tsinghua University
                                          6
                                            Department of Physics, The Chinese University of Hong Kong 7 Yanqi Lake Beijing Institute
                                          of Mathematical Sciences and Applications (BIMSA)
arXiv:2512.24796v2 [cs.LO] 25 Feb 2026




                                                                                       A BSTRACT
                                                    While large language models (LLMs) have demonstrated impressive capabilities in
                                                    formal theorem proving, current benchmarks fail to adequately measure library-
                                                    grounded abstraction—the ability to reason with high-level interfaces and reusable
                                                    structures central to modern mathematics and software engineering. We introduce
                                                    LeanCat, a challenging benchmark comprising 100 fully formalized category-
                                                    theory tasks in Lean. Unlike algebra or arithmetic, category theory serves as a
                                                    rigorous stress test for structural, interface-level reasoning. Our evaluation reveals
                                                    a severe abstraction gap: the best state-of-the-art model solves only 12.0% of
                                                    tasks at pass@4, with performance collapsing from 55.0% on Easy tasks to 0.0%
                                                    on High-difficulty tasks, highlighting a failure in compositional generalization.
                                                    To overcome this, we evaluate LeanBridge, a retrieval-augmented agent that
                                                    employs a retrieve–generate–verify loop. LeanBridge achieves a peak success rate
                                                    of 24.0%—doubling the performance of the best static baseline. These results
                                                    empirically demonstrate that iterative refinement and dynamic library retrieval are
                                                    not merely optimizations but strict necessities for neuro-symbolic reasoning in
                                                    abstract domains. LeanCat offers a compact, reusable testbed for tracking progress
                                                    toward reliable, research-level formalization.


                                         1       I NTRODUCTION
                                         Recent advances in large language models (LLMs) and agentic training have revived the prospect
                                         of end-to-end formal theorem proving. On the formal side, systems such as OpenAI’s early Lean-
                                         based prover (Polu et al., 2022) and DeepMind’s AlphaProof (Hubert et al., 2025) demonstrate that
                                         reinforcement learning with formal verification feedback can produce non-trivial Lean proofs. More
                                         recently, specialized provers such as DeepSeek-Prover-V2 (Ren et al., 2025) and Seed-Prover 1.5
                                         (Chen et al., 2025) show that large-scale agentic RL and test-time scaling can push formal success rates
                                         on established benchmarks substantially higher. These results suggest that formal proof generation is
                                         no longer limited to toy domains, and that tight tool feedback loops (retrieve–generate–verify) can be
                                         a decisive ingredient.
                                         Despite steady progress in neural theorem proving, current formal benchmarks still do not adequately
                                         exercise library-grounded, abstraction-heavy reasoning. Widely used datasets such as miniF2F
                                         (Zheng et al., 2022) and FIMO Liu et al. (2023) largely draw from olympiad-style problems, while
                                         university-level suites like ProofNet Azerbayev et al. (2022) and PutnamBench Tsoukalas et al.
                                         (2024) focus on undergraduate competition or textbook material. These benchmarks are valuable, but
                                         they often reward short clever tricks or computation rather than sustained work inside rich abstract
                                         frameworks. By contrast, modern research mathematics is written at high generality, organized
                                         around reusable interfaces, and deeply intertwined with large libraries of definitions and lemmas—so
                                         success hinges less on a single key insight and more on navigating abstraction, managing definitions,
                                         and coherently composing library knowledge over long horizons.
                                             ∗
                                                 Email: rongge@tsinghua.edu.cn


                                                                                              1
                                                                    Other Baselines
                                   70                               Other LeanBridge
                                                                    Best Baseline (Claude-Opus-4.5)
                                                                    Best LeanBridge (GPT-5.2)
                                   60                               Abstraction Gap Closed


                                   50



                Success Rate (%)
                                   40

                                   30                25.0%

                                   20

                                   10
                                                                                            2.5%
                                                                                       0.0%
                                    0                2.5%
                                        Easy        Medium                                  High
                                               Problem Difficulty

Figure 1: Closing the Abstraction Gap. Performance comparison of standard baselines (dashed
lines) vs. our agentic approach, LeanBridge (solid lines), across difficulty levels. Bold lines highlight
the best-performing models (Claude-Opus-4.5 for pass@4 baseline, GPT-5.2 for LeanBridge with
NL+Statement input), while faint lines represent other models. Note the sharp performance collapse
of baselines on Medium/High tasks (the “abstraction gap”), which LeanBridge effectively bridges,
achieving the first successful proofs on High-difficulty problems.



Category theory provides a natural stress-test for this capability: as the interface language of mod-
ern mathematics—categories, functors, natural transformations, adjunctions, limits/colimits, mon-
ads—formal proofs typically rely on diagrammatic and universal-property reasoning, i.e., construct-
ing morphisms with the right naturality/uniqueness guarantees and showing commutativity across
families of structures. Yet existing formal benchmarks rarely target this abstraction layer directly. To
bridge this gap, we introduce LeanCat1 , a benchmark of 100 category-theory problems formalized
in Lean 4 (with Mathlib), designed to test whether automated provers can operate inside a mature
library and compose high-level abstractions rather than solve isolated puzzles. LeanCat complements
algebra-focused benchmarks such as the FATE series Jiang et al. (2025) by shifting the frontier from
abstract algebra to category theory.
Our baseline evaluation reveals a stark abstraction gap: across five strong models, the best achieves
only 8.25% at pass@1 and 12% at pass@4. More critically, we observe a collapse in compositional
generalization: performance drops from 55.0% on Easy tasks to 0.0% on High-difficulty tasks
(Figure 1), validating that current LLMs struggle to manage long-horizon abstraction dependencies.
To address this challenge, we go beyond static evaluation and introduce LeanBridge, a retrieval-
augmented agent designed to close the abstraction gap. LeanBridge implements a dynamic retrieve–
generate–verify loop that actively queries the library for definitions and lemmas. Our experiments
show that LeanBridge achieves a success rate of 24.0%. As shown in Figure 1, our agentic approach
(solid lines) effectively mitigates the performance collapse observed in baselines, securing the first
successful proofs on High-difficulty tasks. These results empirically demonstrate that iterative
refinement and library retrieval are not merely optimizations, but strict necessities for neuro-symbolic
reasoning in abstract domains.
To our knowledge, LeanCat is the first installment of a benchmark series dedicated to category theory.
Beyond merely ranking models, we view this direction as pivotal for both human mathematics—by
mapping which parts of abstract reasoning remain elusive to formalization—and AI—by forcing
progress on abstraction-aware planning, definition retrieval, and robust compilation-driven refinement.
Our key contributions are summarized as follows:


   1
       The benchmark code and data are available at https://github.com/sciencraft/LeanCat.


                                                    2
       • LeanCat benchmark (1-Categories). We present LeanCat, a suite of 100 category-theory
         problems formalized in Lean 4. The tasks span eight topic clusters, curated to cover reusable
         abstract interfaces and structural reasoning rather than contest-style tricks.
       • Difficulty annotation pipeline. We propose a hybrid grading process combining model-
         based estimates and expert judgment. Each problem receives weighted ratings from both
         advanced LLMs and human formalizers to assign reliable Easy/Medium/High labels.
       • Baseline evaluation. We benchmark state-of-the-art generalist models (e.g., GPT-5.2,
         Claude-Opus-4.5) alongside specialized neural provers (e.g., DeepSeek-Prover-V2). Our
         extensive evaluation reveals a severe abstraction gap: while generalist models struggle
         with long-horizon coherence, specialized provers fail to generalize beyond their training
         curriculum, achieving near-zero success on Medium/High tasks even with high sampling
         budgets.
       • Search-augmented proving via LeanBridge. To address the abstraction gap, we propose
         and evaluate LeanBridge, an agentic workflow integrating LeanExplore (Asher, 2025). We
         demonstrate that this retrieval-augmented approach doubles the pass rate of static baselines,
         validating the necessity of dynamic tool use in higher mathematics.

2     L EAN C AT B ENCHMARK D ESIGN
2.1   B ENCHMARK S TRUCTURE AND C ONTENT

Data Source The problems in our benchmark are organized into two main parts: Abstract and
Concrete:

       • Abstract part: Problems are primarily drawn from standard, widely used textbooks in
         category theory, especially Category Theory in Context (Riehl, 2017) and Categories for
         the Working Mathematician (Mac Lane, 1998), together with a small number of problems
         adapted from unpublished lecture notes (Kong; Zheng).
       • Concrete part: Problems are curated mainly from Abstract and Concrete Categories
         (Adámek et al., 1990), which provides a systematic source of exercises on concretizability,
         injectivity, and related themes.
       • Others: Beyond these core sources, we also include selected problems inspired by research
         papers and advanced community-driven references (Chen, 2021; Adámek et al., 2021).

Each LeanCat problem is self-contained at the statement level: the formal statement of the theorem
is provided (often with informal description provided in the corresponding Markdown file), and all
necessary definitions exist in Lean’s environment (either already in Mathlib (mathlib Community,
2020) or introduced as part of the problem setup). Where possible, we drew on known theorems from
category theory literature, many tasks were crafted or adapted specifically to probe corner cases and
interface interactions that an AI prover might struggle with. In several High-difficulty cases, relevant
lemmas were not readily available, forcing human formalizers to devise intermediate results. This
aspect of LeanCat, that it sometimes goes beyond the library, makes it a particularly stringent test for
automated provers, which cannot rely solely on rote application of existing library facts.
LeanCat comprises 100 theorem statements in category theory, each fully formalized in Lean 4 (i.e.
each problem is given as a Lean theorem declaration, with required definitions and context available).
The problems are organized into eight topical clusters reflecting key areas of category theory, ranging
from Basic Category Properties to advanced structures like Abelian Categories and Monads.
Figure 2 illustrates the distribution of problems across these topics and their difficulty levels. The
benchmark covers both standard textbook results (e.g., adjunctions, limits) and frontier formalization
tasks (e.g., cocompletions, which require new definitions). We provide a detailed breakdown of each
topical cluster and the specific mathematical competencies they test in Appendix A.

2.2   C URATION W ORKFLOW

LeanCat is curated through a three-stage workflow that combines expert selection, LLM-assisted
drafting, and rigorous human verification:


                                                   3
Figure 2: Sunburst diagram showing the distribution of our LeanCat problem sets by topic and
difficulty. The inner ring groups problems into thematic sections (Basic, Adjunction, Reflective,
Concrete, Limit, Cocompletion, Abelian, Monad), while the outer ring lists individual problems,
labelled by difficulty: E = Easy, M = Medium, H = High.



      1. Collection. Three category-theory experts curate candidate problems from established
         sources (as described above), aiming to cover both core interfaces (e.g., adjunctions, limits/-
         colimits, monads) and representative proof patterns (diagram chasing, universal properties,
         naturality).

      2. Formalization. For each selected problem, we first use several LLMs to draft Lean 4
         statements. The same three category-theory experts then review these drafts and retain only
         semantically correct formal statements. For problems where none of the models produced
         a correct statement, we organized a three-day workshop at Westlake University, bringing
         together Lean experts to author the missing statements and (when feasible) corresponding
         proofs.

      3. Review. Finally, two independent reviewers with strong mathematical backgrounds and
         Lean expertise perform a full consistency pass, checking compilation, fixing definitional
         mismatches, and ensuring the formal statement matches the intended mathematical meaning.


Statement-level tasks. LeanCat is a statement-level benchmark: each item consists of a single
standalone theorem to prove (see Figure 3 in Appendix A for a concrete example), rather than a
scaffolded sequence of intermediate lemmas that gradually builds toward a final goal. This design
aims to evaluate general library-grounded proving capabilities—retrieval, definition management,
and abstraction navigation—instead of rewarding problem-specific hint engineering.


Scope and difficulty. Overall, LeanCat is broad in its topical coverage across category theory, and
deep in the sense that even short-looking theorems can require layered abstractions and careful use of
reusable interfaces, mirroring how mathematicians work inside large formal libraries.


Formalization standards. All benchmark files follow strict, uniform conventions: (i) each Lean
file is strictly self-contained, relying solely on Mathlib and explicitly including any definitions or
lemmas required by the theorem statement; (ii) the natural-language problem description is stored
in a companion Markdown file (supporting LATEX), designed to be injected into the Lean code as a
comment during the evaluation phase.


                                                   4
2.3   D IFFICULTY A NNOTATION P IPELINE

Rather than relying purely on the problem author’s intuition, we implemented a systematic
LLM+human rating pipeline to grade problem difficulty on a 10-point scale, then binned the scores
into the three categories: Easy, Medium, and High. This approach aimed to capture both human
expertise and automated solver perspectives, similar in spirit to FATE’s curation process (which
combined expert judgment with model feedback for difficulty ranking).
Our pipeline proceeded as follows:

       • LLM Difficulty Scoring. We employ a data-driven approach where each problem is
         evaluated using the LeanBridge sequential refinement protocol (as detailed in Section
         3.1) across all five baseline models. We assign 2 points for a full proof and 0.5 points
         for a correct statement (credited only if the proof fails). The difficulty is calculated as:
         Diff = max(0, 10 − 2Nproof − 0.5Nstmt ), where Nproof is the number of models producing
         a verified proof, and Nstmt is the number of models generating a correct formal statement
         but failing the proof (ensuring disjoint counts). This scales from 0 (all solved) to 10 (none
         solved).
       • Human Difficulty Scoring. In parallel, two human mathematicians (with Lean expertise
         and category theory background) independently rated each problem on the same 1-10
         difficulty scale. They factored in things like the length of the proof, intricacy of arguments,
         and whether any non-obvious lemmas are required. The human scores tended to correlate
         with intuition: e.g. a trivial diagram chase might be 2/10, whereas a complex construction
         spanning several definitions could be 9/10.
       • Aggregation. We combined the scores giving 50% weight to human ratings and 50% to
         LLM ratings. Finally, we mapped the numeric scores to difficulty categories by selecting
         thresholds specifically to enforce a distribution of 20 Easy, 40 Medium, and 40 High tasks.
         This resulted in cut-offs of scores ≤ 5.54 for Easy and ≥ 7.8 for High. We intentionally
         adopted this skewed distribution (heavier on Medium/High tasks) to prevent premature
         saturation by current models—which already solve > 50% of Easy tasks—and to provide
         sufficient headroom for tracking future progress in closing the abstraction gap. The complete
         scoring data for all 100 problems is provided in Appendix Figure 5.

This data-driven approach provides a more objective difficulty metric than human intuition alone.
Our experimental results (Section 4) validate this ranking: the best-performing model solved most
tasks classified as Easy, while problems with scores ≥ 9 remained unsolved across all baselines.
This distribution confirms that our difficulty labels effectively proxy the "formalization hardness" for
current neuro-symbolic systems.

3     E XPERIMENTS AND R ESULTS
3.1   E XPERIMENTAL S ETUP

We employ two distinct inference strategies to evaluate performance on LeanCat: parallel sampling
for standard baselines, and sequential refinement for the LeanBridge agent.

Standard Baselines: Parallel Sampling (Pass@k). We benchmark a suite of state-of-the-art
models, including GPT-5.2 (OpenAI, 2025), Gemini-3-Pro (Gemini Team, Google, 2025), Claude-
Opus-4.5 (Anthropic, 2025), DeepSeek-V3.2-Thinking (Liu et al., 2025), and Kimi-K2 Team et al.
(2025), under a purely formal setup.

       • Input: Each problem is presented in a uniform format containing the Lean statement
         (theorem name, hypotheses, and conclusion) and necessary imports. The model sees the
         formal goal exactly as a human user would. Crucially, no natural language hints or
         decomposed lemmas are provided; the model must derive the proof solely from the formal
         statement and standard library knowledge.
       • Prompting: We prompt models to generate a Lean proof script directly, adopting the prompt
         template from FATE-Eval (Jiang et al., 2025) for consistency.


                                                   5
Algorithm 1 LeanBridge Inference Loop (Dynamic Retrieval)
  Input: Natural Language Statement SN L , Formal Statement SLean (Optional)
  Output: Proof Script π or Failure
  // Phase 1: Context Initialization & Mandatory Retrieval
  C ← {SN L , SLean }
  Dinit ← Retrieve(Query = SN L ) {Initial broad search}
  C ← C ∪ {Dinit }
  // Phase 2: Refinement Loop
  for t = 1 to Tmax do
     Actiont ← LLM.Generate(C)
     if t > 1 and Actiont is SearchRequest(Keywords) then
        // Agent decides to refine knowledge
        Dnew ← Retrieve(Keywords)
        C ← C ∪ {Actiont , Dnew }
     else if Actiont is ProofCandidate(π) then
        // Agent attempts a proof
        Success, M sg ← LeanCompiler.Verify(π)
        if Success then
           return π
        else
           // Feedback loop: Error message drives next step
           C ← C ∪ {π, M sg}
        end if
     end if
  end for
  return Failure


      • Protocol: We use the pass@k metric (Chen et al., 2021). For each problem, we sample
        k independent proof attempts. The problem is considered solved if any of the k attempts
        compiles and verifies. We report pass@1 (single-try reliability) and pass@4 (sampling
        diversity).

To determine if the abstraction gap is merely a result of using general-purpose models, we extended
our pass@k evaluation to specialized neural provers explicitly trained for formal mathematics:
DeepSeek-Prover-V2-671B(Ren et al., 2025), Goedel-Prover-v2-32B(Lin et al., 2025), StepFun-
Prover-32B(Shang et al., 2025), and Kimina-72B(Wang et al., 2025). Given their specialized nature,
we relaxed the evaluation strictness, allowing for a significantly higher sampling budget of pass@32
(compared to pass@4 for generalist models).

LeanBridge: Sequential Refinement. To address the library-grounded and abstraction-heavy
nature of LeanCat, we also evaluate LeanBridge, a retrieval-augmented agent. Unlike the static
baselines, LeanBridge actively leverages Mathlib via LeanExplore (Asher, 2025)—which utilizes
a hybrid ranking strategy combining semantic embeddings, BM25+, and PageRank—through a
retrieve–generate–verify loop (Algorithm 1).

      • Input: We test two settings: (1) NL-to-Proof : The model receives only the natural-language
        problem description; and (2) NL+Statement-to-Proof : The model receives both the natural
        language description and the formal statement.
      • Protocol: Unlike the independent sampling used for baselines, LeanBridge operates in
        a sequential loop. The system initiates a search using the natural-language statement,
        generates a proof, and validates it. If verification fails, the system analyzes the error,
        potentially performs a targeted retrieval, and revises the proof. We allow a maximum of
        4 iterations per problem. A problem is considered solved if the system produces a valid,
        verified proof at any point within these 4 iterations.


Verification and Constraints.    All proof attempts are verified against Lean 4 (Mathlib v4.19.0).


                                                 6
Table 1: Baseline Performance. Success rates of static models evaluated via Pass@1 and Pass@4
metrics. Pass@1 scores are estimated using the unbiased estimator from Chen (2021).

      Model                   Easy              Medium             High             Overall
      Claude-Opus-4.5 40.00% / 55.00% 0.63% / 2.50% 0.00% / 0.00%               8.25% / 12.00%
      GPT-5.2         27.50% / 35.00% 0.00% / 0.00% 0.00% / 0.00%               5.50% / 7.00%
      Gemini-3-Pro    13.75% / 30.00% 1.25% / 5.00% 0.00% / 0.00%                3.25% / 8.00%
      DeepSeek-V3.2   20.00% / 40.00% 0.00% / 0.00% 0.00% / 0.00%                4.00% / 8.00%
      Kimi-K2         10.00% / 20.00% 0.00% / 0.00% 0.00% / 0.00%               2.00% / 4.00%

Table 2: LeanBridge Performance. Success rates of the agentic workflow (max 4 iterations).
Columns distinguish between NL-only and NL+Statement input settings.

        Model                   Easy            Medium             High           Overall
        Claude-Opus-4.5 70.0% / 70.0%         5.0% / 17.5%     0.0% / 0.0% 16.0% / 21.0%
        GPT-5.2         60.0% / 65.0%         5.0% / 25.0%     0.0% / 2.5% 14.0% / 24.0%
        Gemini-3-Pro    45.0% / 60.0%        12.5% / 17.5%     0.0% / 2.5% 14.0% / 20.0%
        DeepSeek-V3.2   55.0% / 40.0%         0.0% / 7.5%      0.0% / 0.0% 11.0% / 11.0%
        Kimi-K2         30.0% / 55.0%         2.5% / 7.5%      0.0% / 0.0% 7.0% / 14.0%


       • Success Criteria: A proof is considered valid if the Lean kernel accepts it without errors
         and strictly contains no sorry, admit, or additional axiom declarations.
       • Resource Limits: Each attempt is subject to a generic output budget of 50,000 tokens and a
         verification time limit of 5 minutes. Attempts exceeding these limits are marked as failures.
       • Human Review (NL-to-Proof Only): In the NL-to-Proof setting, a model may generate a
         valid proof for an incorrect formalization. To guard against such superficial “green” proofs,
         all successful candidates in this mode undergo human expert review to ensure semantic
         alignment with the original natural-language problem.


4     R ESULTS AND A NALYSIS

We evaluate five state-of-the-art models on LeanCat. We first present the quantitative performance of
standard baselines, followed by the results of our retrieval-augmented agent, LeanBridge. Finally, we
provide a qualitative analysis of common failure modes.

4.1    Q UANTITATIVE P ERFORMANCE

Standard Baselines (Pass@k). Table 1 summarizes the success rates of API-based models in the
purely formal setting. As shown, the overall success rate is low across the board. The best-performing
model, Claude-Opus-4.5, solves only 8.25% of problems on the first attempt (Pass@1) and improves
to 12.00% with four attempts (Pass@4). Other top-tier models like GPT-5.2 and DeepSeek-V3.2
follow, achieving Pass@4 scores of 7.00% and 8.00%, respectively. Across all baseline experiments,
only 14 distinct problems were solved by at least one model, highlighting the rigorous difficulty of
LeanCat compared to earlier benchmarks.

LeanBridge Performance. Table 2 details the performance of our agentic approach. By comparing
static baselines, the NL-only agent, and the NL+Statement agent, we isolate two key drivers of
success:

       • The Agentic Advantage (Static vs. Agent). First, the retrieval loop alone provides
         a massive boost. Even without the formal statement (NL-only), LeanBridge (GPT-5.2)
         achieves an overall success rate of 14.0%, doubling its static Pass@4 baseline of 7.0%. This
         confirms that dynamic library interaction effectively bridges basic knowledge gaps.


                                                  7
Table 3: Specialized Provers (Pass@32). Performance of domain-specific models. Despite a higher
sampling budget, they fail to generalize to Medium/High tasks.

                      Model                             Easy Med. High Avg.
                      DeepSeek-Prover-V2-671B           45.0%   0.0%   0.0%   9.0%
                      Goedel-Prover-V2-32B              20.0%   2.5%   0.0%   5.0%
                      StepFun-Prover-32B                20.0%   2.5%   0.0%   5.0%
                      Kimina-72B                        10.0%   0.0%   0.0%   2.0%


       • Impact of Formal Grounding (NL-only vs. NL+Statement). Second, comparing the
         two agent settings reveals that grounding the agent in the formal statement is decisive for
         handling abstraction. While the two settings perform similarly on Easy tasks (60.0% vs.
         65.0%), the gap widens drastically on Medium tasks (5.0% vs. 25.0%). Crucially, only the
         NL+Statement setting unlocks High-difficulty problems (2.5%), a frontier that remained
         completely inaccessible (0%) to both static baselines and ungrounded agents. This finding
         indicates that precise formal definitions act as essential anchors for long-horizon planning
         in abstract domains. (See Appendix Figure 7 for a detailed visual comparison across all
         models.)

Comparison with Specialized Provers.           Table 3 presents the results. Three key observations
emerge:

       • The Abstraction Gap Persists. Even with a 8× higher sampling budget, specialized provers
         exhibit the same collapse in performance as generalist models. DeepSeek-Prover-V2, the
         strongest in this category, achieves a respectable 45.0% on Easy tasks but plummets to 0.0%
         on both Medium and High tasks.
       • Curriculum Overfitting. The disparity between Easy and Medium/High tasks is even more
         pronounced in specialized provers than in generalist LLMs. For instance, Goedel-Prover
         achieves 20% on Easy tasks but fails almost completely on Medium tasks (2.5%). This
         suggests that these models may have overfitted to the “olympiad-style” or “undergraduate
         calculation” distribution prevalent in their training data (e.g., miniF2F), failing to generalize
         to the structural reasoning required for category theory.
       • Inefficiency of Blind Scaling. Comparing Table 2 and Table 3, we see that a generalist agent
         (LeanBridge with GPT-5.2), using a maximum of only 4 iterations, surpasses specialized
         provers at pass@32 on overall metrics, and significantly outperforms them on harder tasks.
         This indicates that agentic workflow and library grounding offer superior scaling potential
         regarding reasoning depth for abstract mathematics compared to simply scaling up sampling
         on model weights trained for lower-level proofs.

4.2   P ERFORMANCE A NALYSIS

Difficulty Gap. As visualized in Figure 1, there is a divergent trend between static baselines and
our agentic framework. For standard models, we observe a sharp performance degradation consistent
with our difficulty annotations. For instance, Claude-Opus-4.5 achieves 55.00% Pass@4 on Easy
problems but drops to 2.5% on Medium and 0% on High. In contrast, LeanBridge (solid lines in
Figure 1) mitigates this collapse, maintaining a smoother degradation curve and securing the only
successes on High-difficulty tasks. Notably, even the “Easy” subset—which requires nontrivial
abstraction and library navigation—is far from solved. This suggests that the baseline complexity of
LeanCat is already beyond the reliable capability of current models, which struggle once problems
move beyond simple exercises.

Efficacy of Retries (Pass@1 vs. Pass@4). Moving from Pass@1 to Pass@4 yields modest absolute
gains. For top models like Claude-Opus-4.5 / GPT-5.2, the improvement is marginal (+3.75% /
+1.5%). This saturation indicates that simple test-time scaling (more samples) is insufficient for
structural reasoning; the models fail not because of random noise, but due to fundamental deficits in


                                                    8
Table 4: Ablation Study (Gemini-3-Pro). Comparisons of Baseline vs. LeanBridge variants. Full
(w/ Search) achieves the best performance on harder tasks.

                                        Baselines               LeanBridge
                      Diff.
                                   Pass@1      Pass@4      No Search      Search
                      Easy          13.75%     30.00%        45.00%       60.00%
                      Medium         1.25%      5.00%         7.50%       17.50%
                      High           0.00%      0.00%         0.00%        2.50%
                      Avg.          3.25%       8.00%        12.00%       20.00%


knowledge and planning. This observation motivates the necessity of the active retrieval mechanism
in LeanBridge.

4.3   Q UALITATIVE A NALYSIS AND FAILURE M ODES

To understand the root causes of failure, we manually inspected failed attempts (specifically from the
Medium and High categories). For a deep dive into specific examples, we refer readers to Appendix E,
which present step-by-step trajectories of a representative success (Problem 59) and a complex failure
(Problem 63). Based on this inspection, we identify five dominant failure modes:

      1. Math failure. The proof uses an incorrect mathematical strategy (e.g. vacuity for an
         existential goal, constant diagrams for genuine colimits), so no Lean patch can make it true.
         Example: in Prob. 68 it picks an empty category PEmpty and tries to finish by simp, but
         the existential statement then reduces to ⊥.
      2. Lean grammar failure. The mathematical idea may be fine, but the Lean script is syn-
         tactically/elaborationally invalid (bad braces, wrong binder order, illegal notation, private
         constructors), so the verifier fails before reaching the proof content. Example: in Prob. 73
         it triggers parser/elaboration errors (e.g. “unexpected token have; expected }”) while
         attempting to build lifted-limit data.
      3. Hallucination failure. The model invokes nonexistent lemmas/constants or misuses projec-
         tions (e.g. T.foo as a field when it is not), often due to name guessing or version/import mis-
         match. Example: in Prob. 3 it repeatedly uses nonexistent API such as hFull.preimage
         / Functor.image_preimage to lift maps from Full, yielding “unknown constant”
         errors.
      4. Lazy failure. The model avoids developing required intermediate definitions/lemmas
         not in mathlib and instead tries infer_instance, guessed theorem names, comments,
         or placeholders, so the missing bridge is never constructed. Example: in Prob. 75 it
         attempts by classical infer_instance to prove IsFiltered (Rec C), and
         when that fails it outputs only commentary rather than proving the needed lemma.
      5. Hack failure. The model makes the goal trivially provable by altering the formal mean-
         ing of the statement (e.g. redefining/shadowing key notions) rather than proving the in-
         tended theorem. Example: in Prob. 17 it defines a local Retract that merely stores
         IsInjectiveObj Y and a piObj that ignores its input, so the theorem reduces to a
         tautology and compiles without proving the real claim.

Pure syntax-level errors (e.g., indentation or parenthesis mismatch) are present but significantly less
frequent than the semantic and strategic failures described above.

4.4   A BLATION S TUDY: T HE I MPACT OF R ETRIEVAL

To disentangle the contributions of the iterative agentic loop versus the dynamic library retrieval,
we conducted an ablation study using Gemini-3-Pro. We evaluated a “No-Search” variant of Lean-
Bridge, which retains the verify–refine loop but is restricted to its internal parametric knowledge (i.e.,
forbidden from issuing search queries).
Table 4 presents the results. We observe a clear hierarchy of capability:


                                                    9
       • Loop vs. Sampling: LeanBridge (w/o Search) achieves 12.0%, significantly outperforming
         the static Pass@4 baseline (8.0%). This indicates that the ability to interpret compiler error
         messages and self-correct provides a tangible gain over blind resampling, particularly on
         Easy tasks (30.0% → 45.0%).
       • The Necessity of Retrieval: However, the “No-Search” agent hits a ceiling on harder
         problems, solving only 7.5% of Medium tasks and failing completely on High tasks (0%).
         Enabling retrieval (Full LeanBridge) unlocks a further ∼ 2× performance jump on Medium
         tasks (17.5%) and enables the only successes on High tasks. This confirms that while
         the agentic loop handles logical bugs, dynamic retrieval is indispensable for bridging the
         knowledge gap in abstract formalization.
LeanBridge substantially strengthens an LLM’s practical proving ability, and retrieval is a key driver
of that improvement. With retrieval enabled, the system more reliably escapes “local patching”
plateaus by pulling in the right library knowledge at the right time, translating into markedly better
performance on harder problems.

5    D ISCUSSION AND F UTURE W ORK
Key Challenges in Abstract Formalization. Our results highlight four persistent bottlenecks that
distinguish LeanCat from earlier benchmarks: (i) Library Awareness: The primary hurdle is not
logical reasoning per se, but locating and instantiating the correct abstract interfaces from Mathlib.
(ii) Abstraction Control: Models struggle to maintain the “categorical imperative,” often drifting into
counter-productive element-wise reasoning that disconnects from the intended library lemmas. (iii)
Long-horizon Coherence: Maintaining a consistent proof plan across dependent steps remains difficult
without external guidance or backtracking. (iv) The Limits of Specialization: Our evaluation confirms
that domain-specific fine-tuning is insufficient for LeanCat. Even with extensive sampling (pass@32),
specialized provers (e.g., DeepSeek-Prover, Goedel) fail on Medium/High tasks. This suggests
that abstract formalization requires the broad “mathematical world knowledge” and compositional
reasoning found in large-scale generalist models, rather than merely local tactic prediction.
The LeanCat Roadmap: Towards Higher Algebra. We envision LeanCat not merely as a static
dataset, but as the first installment of a broader series targeting high-abstraction mathematics. Future
iterations will expand beyond 1-category theory to cover monoidal categories and higher-categorical
structures (e.g., 2-categories). This evolution aims to create a virtuous cycle:
                                 Benchmark             AI Solutions

                                New Frontier       Merged to Mathlib

Broader Impact. For AI research, LeanCat provides a concrete testbed for improving retrieval-
augmented generation (RAG) and abstraction-aware planning. For the mathematics community,
these checkpoints help identify missing lemmas and interface gaps in the library, prioritizing human
engineering efforts.

ACKNOWLEDGMENTS
The Lean workshop at Westlake University was supported by the National Natural Science Foundation
of China (NSFC), Grant No. 12574176. We thank Prof. Jian Li for supporting the organization of the
workshop. We are also grateful to Jiatong Yang and Hongwei Wang for their valuable assistance with
formalization during the workshop. We specifically thank Zhimin Cao for conducting the evaluation
of specialized provers. We thank Xingyu Ren for inspiring this benchmark. We thank Prof. Lifan
Guan, Huayi Chen, Bin Dong and Hao Zheng for helpful comments. We also thank Jiadong Adam
Guo, Jinyuan Zhang, and Xiaodong Hu for providing API access for our large language model
experiments.

R EFERENCES
Jiří Adámek, Horst Herrlich, and George Strecker. Abstract and concrete categories. Wiley-
    Interscience, 1990.


                                                  10
Jiří Adámek, Liang-Ting Chen, Stefan Milius, and Henning Urbat. Reiterman’s theorem on finite
    algebras for a monad. ACM Transactions on Computational Logic (TOCL), 22(4):1–48, 2021.
Anthropic. System card: Claude opus 4.5. Anthropic, November 2025. URL https://www.
  anthropic.com/claude-opus-4-5-system-card. Released November 24, 2025.
 Accessed on February 27, 2026.
Justin Asher. LeanExplore: A search engine for Lean 4 declarations, 2025. URL https://arxi
  v.org/abs/2506.11085.
Zhangir Azerbayev, Bartosz Piotrowski, and Jeremy Avigad. ProofNet: A benchmark for autofor-
  malizing and formally proving undergraduate-level mathematics problems. In Second MATH-AI
  Workshop, 2022.
Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing
   Jin, Chenggang Li, Wenlei Shi, et al. Seed-prover 1.5: Mastering undergraduate-level theorem
   proving via learning from experience. arXiv preprint arXiv:2512.17260, 2025.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code. arXiv preprint arXiv:2107.03374, 2021.
Ruiyuan Chen. On sifted colimits in the presence of pullbacks. arXiv preprint arXiv:2109.12708,
  2021.
Gemini Team, Google. Gemini 3 pro model card. November 2025. URL https://storage.go
  ogleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.
  pdf.
Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth, Goran Žužić, Eric Wieser, Aja
  Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Masoom, et al. Olympiad-level formal
  mathematical reasoning with reinforcement learning. Nature, pp. 1–3, 2025.
Jiedong Jiang, Wanyi He, Yuefeng Wang, Guoxiong Gao, Yongle Hu, Jingting Wang, Nailing Guan,
   Peihao Wu, Chunbo Dai, Liang Xiao, et al. Fate: A formal benchmark series for frontier algebra
   of multiple difficulty levels. arXiv preprint arXiv:2511.02872, 2025.
Liang Kong. Category theory. Unpublic.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
  Jiawei Ge, Jingruo Sun, et al. Goedel-prover-v2: Scaling formal theorem proving with scaffolded
  data synthesis and self-correction. arXiv preprint arXiv:2508.03613, 2025.
Aixin Liu, Aoxue Mei, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu, Bowei
  Zhang, Chaofan Lin, Chen Dong, et al. Deepseek-v3. 2: Pushing the frontier of open large language
  models. arXiv preprint arXiv:2512.02556, 2025.
Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju,
  Chuanyang Zheng, Yichun Yin, Lin Li, et al. FIMO: A challenge formal dataset for automated
  theorem proving. arXiv preprint arXiv:2309.04295, 2023.
Saunders Mac Lane. Categories for the working mathematician, volume 5. Springer Science &
  Business Media, 1998.
The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs, 2020.
OpenAI. Update to gpt-5 system card: Gpt-5.2. OpenAI, December 2025. URL https://open
  ai.com/index/gpt-5-system-card-update-gpt-5-2/. Released December 11,
  2025. Accessed on February 27, 2026.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
  Sutskever. Formal mathematics statement curriculum learning. arXiv preprint arXiv:2202.01344,
  2022.


                                                11
ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
  Zhe Fu, Qihao Zhu, Dejian Yang, et al. DeepSeek-Prover-V2: Advancing formal mathematical
  reasoning via reinforcement learning for subgoal decomposition. arXiv preprint arXiv:2504.21801,
  2025.
Emily Riehl. Category theory in context. Courier Dover Publications, 2017.
Shijie Shang, Ruosi Wan, Yue Peng, Yutong Wu, Xiong hui Chen, Jie Yan, and Xiangyu Zhang.
  Stepfun-prover preview: Let’s think and verify step by step, 2025. URL https://arxiv.or
  g/abs/2507.20199.
Kimi Team, Yifan Bai, Yiping Bao, Guanduo Chen, Jiahao Chen, Ningxin Chen, Ruijue Chen, Yanru
  Chen, Yuankun Chen, Yutian Chen, et al. Kimi k2: Open agentic intelligence. arXiv preprint
  arXiv:2507.20534, 2025.
George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings, Ami-
  tayush Thakur, and Swarat Chaudhuri. PutnamBench: Evaluating neural theorem-provers on the
  putnam mathematical competition. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet,
  J. Tomczak, and C. Zhang (eds.), Advances in Neural Information Processing Systems, volume 37,
  pp. 11545–11569. Curran Associates, Inc., 2024. URL https://proceedings.neurip
  s.cc/paper_files/paper/2024/file/1582eaf9e0cf349e1e5a6ee453100aa
  1-Paper-Datasets_and_Benchmarks_Track.pdf.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, et al. Kimina-prover preview: Towards large formal
  reasoning models with reinforcement learning. arXiv preprint arXiv:2504.11354, 2025.
Hao Zheng. Category note. Unpublic.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: A cross-system benchmark
  for formal olympiad-level mathematics. In The Tenth International Conference on Learning
 Representations, 2022.




                                               12
A     D ETAILED B ENCHMARK B REAKDOWN
In this section, we provide a detailed description of the eight topical clusters comprising LeanCat,
complementing the overview in Section 2.

       • Basic Category Properties (Problems 1-18): Fundamental results about categories and
         morphisms. These include properties of monomorphisms and epimorphisms, initial/terminal
         objects, factorization of idempotents, and examples of categorical constructions.
       • Adjunctions (Problems 19-29): Constructions and criteria involving adjoint functors, a
         central concept in category theory. Problems include proving that familiar functors have left
         or right adjoints, as well as general adjointness criteria like the comma category condition
         (Problem 19) and some concrete examples (Problem 28). These tasks test a prover’s ability to
         manipulate universal properties and to move between element-wise (“pointwise”) reasoning
         and diagrammatic reasoning.
       • Reflective and Coreflective Subcategories (Problems 30-33): Abstract properties and con-
         crete examples of a special kind of subcategories (e.g. classifying the reflective subcategories
         of Set and T opCH ).
       • Concrete Categories (Problems 34-41): Categories with a faithful forgetful functor to Set
         and related notions. These tasks are largely concrete and overlap substantially with other
         areas of mathematics, such as topology, order theory, and set theory. They are designed to
         test a model’s ability to connect abstract concepts with concrete examples.
       • Limits and Colimits (Problems 42-73): This is the largest cluster, covering a range of
         results about limits, colimits, and related categorical constructs. Many of these statements
         are at the frontier of what Lean’s Mathlib currently contains, indeed some (like Problem 46
         or 67) required developing new formal definitions. This cluster stresses a prover’s ability to
         chain together multiple categorical facts.
       • Cocompletions (Problems 74-78): This part is based on recent work on cocompletions. It
         requires the LLM to introduce new definitions and then prove the key theorems built on
         those definitions that are not currently available in Mathlib.
       • Abelian Categories (Problems 79-90): Tasks concerning abelian categories and homologi-
         cal algebra concepts. Abelian categories are highly structured categories (every morphism
         has a kernel and cokernel, etc.) and generalize the category of modules or abelian groups.
         These statements mirror standard results in homological algebra, but formalizing them in
         Lean requires care with categorical abstractions (e.g. kernel objects, exact sequences) that
         are more complex than their set-based counterparts. Solving them may require the prover to
         introduce creative auxiliary lemmas about kernels, images, or exactness - a tall order for
         automated tools.
       • Monads (Problems 91-100): The final cluster centers on monads and their associated
         constructions (Kleisli and Eilenberg-Moore categories). Monads are a high-level concept
         that encapsulates a form of “computation” or structure; proving properties about them in
         Lean often demands a two-level reasoning (reasoning about the monad’s algebraic laws
         and about category-theoretic conditions like preservation of coequalizers). This cluster
         provides a valuable test of an AI’s ability to work with highly abstract algebraic structure in
         a category-theoretic setting.

A.1   S AMPLE P ROBLEM I NSTANCE

To illustrate the data format of LeanCat, we present two sample entries, each problem consists of a
natural language description (stored in a companion Markdown file) and a self-contained Lean 4 file
with the formal declaration.

B     D IFFICULTY S CORING DATA
We provide the full raw data used for difficulty scoring:



                                                  13
    Natural Language Statement (.md)
     Definition: A functor F : C → D is said to lift limits if for every diagram D : I → C and
    every limit L of F ◦ D, there exists a limit L′ ∈ D such that F (L′ ) ∼= L.
    Theorem: There is a functor that lifts limits but is not faithful.

    Formal Statement (.lean)
      import Mathlib

      open CategoryTheory Limits

      namespace CAT_statement_S_0059

      universe w' w'₁ w w₁ v₁ v₂ v₃ u₁ u₂ u₃

      variable {C : Type u₁} [Category.{v₁} C]
      variable {D : Type u₂} [Category.{v₂} D]
      variable {J : Type w} [Category.{w'} J] {K : J ⥤ C}

      structure LiftableCone₂ (K : J ⥤ C) (F : C ⥤ D) (c : Cone (K ⋙ F)) where

      liftedCone : Cone K

      validLift : F.mapCone liftedCone ≅ c
      isLimit : IsLimit liftedCone

      class LiftsLimit (K : J ⥤ C) (F : C ⥤ D) where

      lifts : ∀ c, IsLimit c → LiftableCone₂ K F c

      theorem exists_functor_lifts_limit_and_not_faithful :
          ∃ (C : Type (u₁+1)) (_ : Category.{u₁} C) (D : Type u₂) (_ : Category.{u₂} D) (F : C ⥤
           ,→ D), (∀ (J : Type u₁) (_ : Category.{w'} J) (K : J ⥤ C), Nonempty (LiftsLimit K F)) ∧
          ¬ F.Faithful := by
      sorry

      end CAT_statement_S_0059




Figure 3: A Sample LeanCat Task (Problem 59). The task is to prove the existence of a functor
that lifts limits but is not faithful.


    Natural Language Statement (.md)
    Definition: Let C be a locally small category. An object c ∈ C is called compact if
    homC (c, −) preserves filtered colimits.
    Theorem: In the category Grp of groups, an object is compact if and only if it is a finitely
    presented group. Every group is a filtered colimit of finitely presented groups.

    Formal Statement (.lean)
      import Mathlib

      open CategoryTheory

      namespace CAT_statement_S_0063

      universe u

      def IsFinitelyPresentedGrp (X : Type u) [Group X] : Prop :=
          ∃ (α : Type u) (rels : Set (FreeGroup α)), Finite α ∧ rels.Finite ∧ Nonempty (X ≃*
           ,→ PresentedGroup rels)

      theorem isCompactObject_Grp_iff_finite_presented (X : Type u) [Group X] :
          CategoryTheory.IsFinitelyPresentable (Grp.of X) ↔ IsFinitelyPresentedGrp X := by
        sorry


      theorem group_realized_as_direct_limit_of_finitely_presented_groups (X : Type u) [Group X] :
          ∃ (J : Type u) (inst₁ : CategoryTheory.SmallCategory J) (inst₂ :
           ,→ CategoryTheory.IsFiltered J) (F : CategoryTheory.Functor J Grp), ∀ (j : J),
           ,→ IsFinitelyPresentedGrp (F.obj j) ∧ Nonempty (X ≃* Grp.FilteredColimits.colimit F) :=
           ,→ by
          sorry

      end CAT_statement_S_0063




Figure 4: A Sample LeanCat Task (Problem 63). The task is to prove the compact object in Grp is
exactly the finitely presented groups.



                                                             14
                Sections    Order          Statement                       Proof                        Difficulty

                                               Claud                     Claud
                                    Chat Gemi        Deep Kimi Chat Gemi       Deep Kimi
                                                 e                         e
                Models              GPT    ni
                                               Opus
                                                     seek k2   GPT   ni
                                                                         Opus
                                                                               seek k2     LLM Human1 Human2 Average Class
                                     5.2 3 pro       V3.2 0905 5.2 3 pro       V3.2 0905
                                                4.5                       4.5

                Weight              0.4   0.4   0.4   0.4   0.4   2   2      2     2   2   0.5   0.25      0.25
                              1                                                            1.6    3         6        3.05    Easy
                              2                                                             4     3         3        3.5     Easy
                              3                                                            9.6    2         3        6.05   Medium
                              4                                                            7.6    4         3        5.55   Medium
                              5                                                            3.6    5         3        3.8     Easy
                              6                                                            9.6    3         6        7.05   Medium
                              7                                                            9.2    5         3        6.6    Medium
                              8                                                            10     5         6        7.75   Medium
                              9                                                            8.4    7         6        7.45   Medium
                 Basic
                             10                                                            9.6    7         3        7.3    Medium
                             11                                                            10     7         9         9      High
                             12                                                            10     7         9         9      High
                             13                                                            10     8         9        9.25    High
                             14                                                            10     8         9        9.25    High
                             15                                                            10     8         9        9.25    High
                             16                                                            10     8         6        8.5     High
                             17                                                            10     9         9        9.5     High
                             18                                                            10     9         9        9.5     High
                             19                                                            5.2    5         3        4.6     Easy
                             20                                                            6.8    4         3        5.15    Easy
                             21                                                             8     6         3        6.25   Medium
                             22                                                            8.4    6         3        6.45   Medium
                             23                                                            9.6    6         3        7.05   Medium
               Adjunction    24                                                            7.6    3         3        5.3     Easy
                             25                                                            7.2    5         6        6.35   Medium
                             26                                                             8     7         6        7.25   Medium
                             27                                                             8     8         6        7.5    Medium
                             28                                                             8     8         3        6.75   Medium
                             29                                                            10     7         3        7.5    Medium
                             30                                                            10     7         6        8.25    High
                             31                                                            9.6    8         6        8.3     High
               Reflective
                             32                                                            9.6    9         6        8.55    High
                             33                                                            9.6    9         6        8.55    High
                             34                                                            9.2    8         3        7.35   Medium
                             35                                                            8.8    8         9        8.65    High
                             36                                                            8.4    9         6        7.95    High
                             37                                                            10     9         6        8.75    High
                Concrete
                             38                                                            9.6    9         9        9.3     High
                             39                                                            9.6    9         9        9.3     High
                             40                                                            10     9         6        8.75    High
                             41                                                            10     9         9        9.5     High
                             42                                                             2     5         3         3      Easy
                             43                                                            4.8    4         3        4.15    Easy
                             44                                                            1.6    4         9        4.05    Easy
                             45                                                            1.6    6         6        3.8     Easy
                             46                                                            7.2    3         3        5.1     Easy
                             47                                                             8     2         3        5.25    Easy
                             48                                                            4.8    6         6        5.4     Easy
                             49                                                            7.6    3         3        5.3     Easy
                             50                                                            9.2    3         6        6.85   Medium
                             51                                                            8.4    4         6        6.7    Medium
                             52                                                            9.6    5         3        6.8    Medium
                             53                                                            5.6    7         6        6.05   Medium
                             54                                                            8.4    6         6        7.2    Medium




Figure 5: Snapshot of the difficulty annotation data. Green: Correct Lean proof. Blue: Correct formal
statement. Olive: Statement correct but language mismatch. Grey: Syntax/Type error (incomplete
Lean script). Yellow: Mathematically correct but informal Lean code.




                                                                      15
                             55                              9.2   6   3   6.85   Medium
                             56                              9.6   6   6   7.8     High
                             57                              8.8   6   6   7.4    Medium
                 Limit
                             58                              10    6   6    8      High
                             59                              10    6   9   8.75    High
                             60                              9.6   7   9   8.8     High
                             61                              10    7   6   8.25    High
                             62                              9.6   7   9   8.8     High
                             63                              10    7   9    9      High
                             64                              10    7   9    9      High
                             65                              9.2   9   9   9.1     High
                             66                              9.2   9   9   9.1     High
                             67                              10    8   3   7.75   Medium
                             68                              9.2   8   9   8.85    High
                             69                              9.6   8   6   8.3     High
                             70                              9.6   8   6   8.3     High
                             71                              10    8   3   7.75   Medium
                             72                              9.6   9   9   9.3     High
                             73                              9.6   7   3   7.3    Medium
                             74                              9.6   7   9   8.8     High
                             75                              10    7   9    9      High
              Cocompletion   76                              10    8   9   9.25    High
                             77                              10    9   9   9.5     High
                             78                              10    9   9   9.5     High
                             79                              1.6   2   3   2.05    Easy
                             80                              0     5   3    2      Easy
                             81                              6.4   3   3   4.7     Easy
                             82                              3.6   3   3   3.3     Easy
                             83                              8.8   2   3   5.65   Medium
                             84                              10    2   3   6.25   Medium
                Abelian
                             85                              8.8   6   3   6.65   Medium
                             86                              9.2   5   3   6.6    Medium
                             87                              9.6   7   6   8.05    High
                             88                              9.2   7   3   7.1    Medium
                             89                              8     7   3   6.5    Medium
                             90                              10    8   3   7.75   Medium
                             91                              1.6   5   3   2.8     Easy
                             92                              7.6   4   6   6.3    Medium
                             93                              6.8   5   9   6.9    Medium
                             94                              3.6   7   6   5.05    Easy
                             95                              7.2   7   9   7.6    Medium
                Monad
                             96                              10    5   3    7     Medium
                             97                              7.2   6   6   6.6    Medium
                             98                              9.6   5   6   7.55   Medium
                             99                              8     4   3   5.75   Medium
                             100                             9.6   9   9   9.3     High




Figure 6: Snapshot of the difficulty annotation data (continued). Green: Correct Lean proof. Blue:
Correct formal statement. Olive: Statement correct but language mismatch. Grey: Syntax/Type error
(incomplete Lean script). Yellow: Mathematically correct but informal Lean code.




                                               16
  C                            V ISUALIZATION OF M ODEL P ERFORMANCE

 We provide a detailed visualization of the impact of formal statement guidance across all models:

                                                                                                                                    NL-only               NL+Statement
                                                 Easy                                                                 Medium                                                            High                                                       Overall
                   80                                                                                                                                     5
                   70     70%70%
                                                                                      25                        25%                                                                                                25                        24%
                                           65%
                                    60%                60%                                                                                                4                                                                      21%
                   60                                                                                                                                                                                                                                     20%
Success Rate (%)




                                                             55%                55%   20                                                                                                                           20
                   50                            45%
                                                                                                    17%                      17%
                                                                                                                                                          3                                                               16%
                                                                   40%                15                                                                                         2%          2%                    15                  14%          14%                         14%
                   40                                                                                                  12%
                                                                                                                                                                                                                                                                11%11%
                   30                                                    30%                                                                              2                                                        10
                                                                                      10
                                                                                                                                        7%          7%                                                                                                                    7%
                   20
                                                                                       5      5%          5%                                              1                                                         5
                   10                                                                                                                         2%
                                                                                                                                   0%                            0% 0%     0%           0%        0% 0%    0% 0%
                    0                                                                  0                                                                  0                                                         0
                            de      -5.2        ini    eek               Kim
                                                                            i                  de        -5.2        ini    eek              Kim
                                                                                                                                                i                 de      -5.2           ini    eek       Kim
                                                                                                                                                                                                             i              de        -5.2        ini    eek             Kim
                                                                                                                                                                                                                                                                            i
                        Clau     GPT         Gem DeepS                                     Clau       GPT         Gem DeepS                                   Clau     GPT            Gem DeepS                         Clau       GPT         Gem DeepS



  Figure 7: Impact of Formal Statement Guidance across All Models (Ablation Study). Comparison
  of LeanBridge performance with NL-only (grey) vs. NL+Statement (blue) inputs. Providing formal
  statements consistently improves success rates on Medium tasks for nearly all models. Notably, it
  enables GPT-5.2 and Gemini-3-Pro to solve High difficulty problems (the 2.5% breakthrough), which
  are otherwise unsolvable.



  D                            P ROMPTS AND E XPERIMENTAL S ETUP

  D.1                            S YSTEM P ROMPTS

 We use the following system prompt for the baseline models (pass@k):
                               """
                               You are an expert in Lean 4 and Mathematics. Please finish the
                               following proof in Lean4 code.
                               Do not change the original statement. Copy the final statement to
                               prove exactly.
                               Please include the complete header (including imports and
                               namespaces) so that your code can
                               pass the Lean4 compiler. Please solve the statement step by step
                               and provide your complete
                               Lean4 code between ```lean4 and ``` after careful reasoning.
                               The statement for you to complete is:

                                 ```lean4
                                     {formal_statement}
                                 ```
                                 """

                                                                         Listing 1: Prompt template for pass@k proof generation


  D.2                            L EAN B RIDGE P ROMPTS

  For the LeanBridge agent, we use a distinct prompt structure to facilitate the retrieve-generate-verify
  loop:
                               """You are an expert in Lean 4 and Mathematics. Please finish the
                               following proof in Lean4 code.

                               if provided a formal statement, do not change the original formal
                               statement. Copy the final statement to prove exactly. Please
                               include the complete header (including imports and namespaces) so
                               that your code can pass the Lean4 compiler.



                                                                                                                                                     17
Please solve the statement step by step and provide your complete
Lean4 code between ```lean4 and ``` after careful reasoning.

The statement for you to complete is:
Natural language statement:
{nl_statement}

Lean 4 formal statement:
{formal_statement}

Reference Knowledge (Search Results from Mathlib):
{search_contents}

"""

          Listing 2: Prompt template for LeanBridge proof generation




"""The previous Lean 4 proof attempt contains errors. Your goal is
to fix them according to the compiler's error message.

Input:
Lean 4 code:
{original_proof}

Error messages:
{error_messages}

Instructions:
1. First, analyze the error message carefully in a "## Error
Analysis" section. Identify specifically why the verification
failed (e.g., missing import, wrong tactic, type mismatch, or a
missing lemma).
2. Based on your analysis, decide whether you need to search
Mathlib for external knowledge (definitions, theorems, or syntax)
or if you can fix it immediately.

Condition A: If you need external information
Output the search query wrapped in the tag below. Make your query
specific (e.g., a math statement, a definition name, or a type
signature).
Format:
## Error Analysis
(Your analysis of the error and what you need to find)
[SEARCH: your_search_query]

Condition B: If you can fix it immediately
Output the analysis and the fully refined code.
Format:
## Error Analysis
(Your analysis of the error and the fix plan)

## Refined Code
```lean
-- The complete, corrected Lean 4 code
```
"""

            Listing 3: Prompt template for LeanBridge refinement




                                     18
                 Table 5: Detailed experimental configuration and hyperparameters.

          Component              Parameter       Value / Description
          LLM Generation         Temperature     1.0 (Encouraging diversity)
                                 Max Tokens      50, 000 (Generalist models)
                                                 Model-specific max (Specialized provers)
          Verification           Lean Version    v4.19.0
                                 Timeout         300 seconds per attempt
          LeanBridge             Loop Limit      Max 4 refinement iterations
                                 Retrieval       Top-3 results per search query


D.3    H YPERPARAMETERS

E     C ASE S TUDY

This section presents a detailed case study of a specific problem, including the original problem
statement, the generated Lean 4 code, and the evaluation of the generated code.

E.1   S UCCESS C ASE

As depicted in Appendix Figure 3, Problem 59 is a representative success case: it is the only High-
difficulty problem solved in our setting, achieved only by GPT-5.2 and Gemini-3-Pro with LeanBridge.
We study the GPT-5.2 attempt. This run fails in early attempts but verifies successfully on the final
refinement (the proving trajectory showed in Figure 8).

1. Strategy used (and mathematical correctness).         The final successful witness takes
 C := Type u1 ,          D := a terminal category on PUnit,         F : C → D the constant functor.
This strategy is mathematically appropriate: limit-lifting becomes easy because C has all limits
and D has trivial cone structure, while non-faithfulness is immediate because F collapses distinct
morphisms to the unique morphism in D.

2. Why it fails initially, and how LLM fixes it. The first attempt tries to exploit “vacuity” by
taking an empty codomain (e.g. PEmpty) and concludes lifting should be trivial. This fails due
to (i) universe/typeclass issues when synthesizing the required Category instances and (ii) ill-
typed constructions (e.g. attempting to inhabit PEmpty). In subsequent iterations, the run pivots to
the clean terminal-codomain construction above, but still encounters Lean-engineering obstacles:
universe mismatches when using Bool : Type 0 as an object of Type u_1, and brittle pattern
matching tactics (e.g. casesm*). The final repair commits to the clean construction and patches
these issues by using ULift Bool : Type u_1 (with explicit ULift.up) and replacing
brittle matches with simple cases.

3. Why the fix works. Limit lifting succeeds because Type u_1 already provides canonical
limit data limit.cone K and limit.isLimit K, which can be used verbatim as the lift. The
required cone isomorphism is trivial in a terminal category: all cone legs are definitional equal
to the unique morphism, so the isomorphism can be constructed by extensionality with reflexive
components. Non-faithfulness is witnessed concretely by two distinct endomorphisms on ULift
Bool (identity vs. boolean negation), which both map to the unique morphism in D; this contradicts
Functor.map_injective by evaluating at ULift.up true.
In summary, the run succeeds because it converges to a canonical, Lean-friendly counterexample: a
constant functor from a complete category (Type) to a terminal category. This choice simultaneously
trivializes the lifting obligation (via existing limit infrastructure in Type) and makes non-faithfulness
explicit (via collapsing distinct functions), while the final patches resolve the remaining universe and
pattern-matching pitfalls.


                                                   19
      Problem 59 Proving Trajectory
       -- Attempt 1: Failed (Universe & Logic Error)
       theorem exists_functor_lifts_limit_and_not_faithful : ... := by
         classical
         -- [Error] Trying to use PEmpty causes instance synthesis failures
         -- and logical contradictions when C is inhabited.
         refine PUnit, (by infer_instance : Category.{u} PUnit), PEmpty, (by infer_instance :
          ,→   Category.{u} PEmpty), ?_, ?_, ?_
             exact (Functor.empty _)
             intro J _ K
             refine ?_   -- [Error] Proof stalls here; cannot inhabit the goal.
             intro c hc
             exfalso
             cases c.pt.elim -- [Error] Ill-typed destruction.
             ...




       -- Attempt 2: Failed (Type Mismatch & Universe Levels)
         ...
         let C' : Type (u + 1) := Type u
         let D' : Type u := OneObjTriv
         -- ... (Functor definition omitted, correctness verified) ...

         -- [Error Section: Non-faithfulness proof]
           intro hfaith
           let X : C' := ULift Bool
           let f : X ⟶ X := fun x => x
           -- [Error] Type mismatch: `!x.down` returns Bool, but expected ULift Bool.
           -- The model forgot the explicit `ULift.up` wrapper.
           let g : X ⟶ X := fun x => !x.down

           have hmap : F'.map f = F'.map g := rfl
           have hinj : f = g := (Functor.map_injective F') hmap
           -- [Error] The simplification proof fails due to the malformed `g`.
           have : (true : ULift Bool) = !true := by ...




       -- Final Version: Success
       theorem exists_functor_lifts_limit_and_not_faithful : ... := by
         classical
         -- 1. Setup Canonical Counterexample
         let C' : Type (u₁ + 1) := Type u₁
         let D' : Type u₂ := OneObjTriv
         let F' : C' ⥤ D' :=
           { obj := fun _ => PUnit.unit
             map := fun {_ _} _ => PUnit.unit }
         refine ⟨C', (by infer_instance : Category.{u₁} C'),
           D', (by infer_instance : Category.{u₂} D'), F', ?_, ?_⟩

         -- 2. Prove LiftsLimit (Trivial in Terminal Category)
         · intro J _ K
            refine ⟨{ lifts := ?_ }⟩
            intro c hc
            refine
              { liftedCone := limit.cone K
                validLift := by
                  -- Key fix: Explicitly constructing the Iso
                  refine Cones.ext (Iso.refl _) ?_
                  intro j; rfl
                isLimit := limit.isLimit K }

         -- 3. Prove Not Faithful (Witnessed by Bool)
         · intro hfaith
            let X : Type u₁ := ULift Bool
            let f : X ⟶ X := fun x => x
            -- Key fix: Correctly wrapping the boolean negation with ULift.up
            let g : X ⟶ X := fun x => ULift.up (!x.down)

           have hinj : f = g := (Functor.map_injective F') rfl
           -- Explicit contradiction proof
           have hpoint : f (ULift.up true) = g (ULift.up true) := by
             simpa using congrArg (fun h : X → X => h (ULift.up true)) hinj

           have : (true : Bool) = false := by
             have : (ULift.down (f (ULift.up true))) = ULift.down (g (ULift.up true)) := by
               exact congrArg ULift.down hpoint
             simpa [f, g] using this
           simpa using this




Figure 8: Case Study (Success): Iterative Refinement on Problem 59. The proving trajectory by
LeanBridge (GPT-5.2), showing the progression from initial attempts to a successful formal proof.



E.2    FAILURE C ASE

We also study the GPT-5.2 with LeanBridge. As depicted in Appendix Figure 4, Problem 63
is a representative failure case (the proving trajectory showed in Figure 9): combining both a
mathematical-strategy error and a “lazy” failure mode.


                                                                 20
     Problem 63 Proving Trajectory
      -- Attempt 1: Trivial Diagram (Failed)
      theorem group_realized_as_direct_limit_of_finitely_presented_groups (X : Type u) [Group X] :
        ... := by
        classical
        -- [Strategy Error] Trying to use PUnit (a single point) as the index category.
        -- This implies X itself is finitely presented, which is false.
        refine ⟨PUnit, inferInstance, inferInstance, (Functor.const _ (Grp.of X)), ?_⟩
        intro j
        refine ⟨?_, ?_⟩
          -- [Hopeful Thinking] Hoping `aesop` can prove X is finitely presented.
          simpa using (by classical; aesop)
          -- [Hopeful Thinking] Hoping `aesop` can prove colimit isomorphism trivially.
          simpa using (by classical; aesop)




      -- Attempt 2 & 3: Giving Up (Explicit Acknowledgment)
      theorem group_realized_as_direct_limit_of_finitely_presented_groups ... := by
        -- [Agent Comment] "Requires the result that every group is a filtered
        -- colimit of finitely presented groups, and must align with the custom predicate.
        -- Current search results do not provide relevant lemmas."
        -- "Cannot construct existence proof under current constraints."
        fail




      -- Attempt 4: Lazy/Hallucinated Contradiction (Failed)
      theorem group_realized_as_direct_limit_of_finitely_presented_groups ... := by
        classical
        -- [Failure] No progress possible without additional lemmas.
        -- Reverts to the invalid PUnit construction.
        refine PUnit, inferInstance, inferInstance, (Functor.const (C := PUnit) (Grp.of X)), ?_
        intro j
        refine ?_, ?_
          -- [Lazy Mode] Tries to claim a contradiction (False.elim)
          -- where none exists. This is a common LLM failure mode when stuck.
          exact False.elim (by trivial)
          exact False.elim (by trivial)




Figure 9: Case Study (Failure): Iterative Refinement on Problem 63. The proving trajectory by
LeanBridge (GPT-5.2).


The task is to formalize in Lean + mathlib the claim that in Grp, categorical finite presentability
matches finite group presentation (generators/relations), and that every group is a filtered colimit of
finitely presented groups. In the file, “finitely presented as a group” is encoded by a custom predicate
IsFinitelyPresentedGrp X := ∃(α, rels), Finite α ∧
                            rels.Finite ∧ Nonempty(X ≃∗ PresentedGroup rels)
and the goals are (i) an equivalence
    IsFinitelyPresentable (Grp.of X) ↔ IsFinitelyPresentedGrp X,
and (ii) a filtered diagram F landing in groups satisfying IsFinitelyPresentedGrp whose
colimit is isomorphic to X.

1. Strategy used (and mathematical correctness). The LLM aims to reuse existing mathlib results:
reduce the statement to mathlib’s notion IsFinitelyPresentable in Grp, then connect that
to the concrete PresentedGroup-based predicate, and finally invoke a filtered-colimit theorem
in Grp. This high-level plan matches the correct mathematical strategy: one normally proves the
equivalence via standard theorems (Baer/Freyd-style characterizations in algebraic categories) and
then uses the classical fact that any group is a filtered colimit of finitely presented groups. However,
when it cannot find the required bridge theorems, the LLM falls back to an invalid shortcut: it tries to
realize the filtered colimit using a trivial/constant diagram (e.g. indexed by PUnit), which would
effectively force IsFinitelyPresentedGrp X for arbitrary X, a statement that is false in
general.

2. Why it fails, and how the LLM tries to fix it. In the first attempt the LLM tries to close the
equivalence using a guessed lemma name like Grp.isFinitelyPresentable_iff, but Lean
reports it as an unknown constant (the lemma does not exist under that name). For the colimit part it
attempts to define a constant functor into a filtered index category and then discharge the remaining
obligations with automation (e.g. aesop), but the hard goals remain: one must actually prove


                                                              21
IsFinitelyPresentedGrp (F.obj j) for each index j and produce Nonempty (X ≃∗
colimit F). After this failure the LLM “fixes” by switching placeholders: it inserts fail in
place of the missing mathematics (which Lean rejects), then replaces fail by simp (which makes
no progress on genuinely nontrivial goals), and finally tries contradiction-style discharge, attempting
to reduce obligations to False and solve them via assumption or rcases. These last steps fail
because no contradiction is derivable from the given hypotheses, and because some tactic steps are
applied to ill-typed or non-inductive targets, indicating the repair loop has drifted away from the
correct categorical structure.

3. Why the fixes do not work. The fixes fail for structural reasons rather than minor syntax. First,
the proof fundamentally needs nontrivial “bridge” theorems (or a substantial new development)
connecting mathlib’s categorical finite presentability in Grp with the specific user-defined predicate
IsFinitelyPresentedGrp based on PresentedGroup. The LLM never finds or constructs
this bridge; instead it guesses lemma names. Second, the constant-diagram shortcut cannot satisfy
the statement “every group is a filtered colimit of finitely presented groups,” since it would imply
every group is itself finitely presented. Third, swapping in fail, simp, or attempting to conjure
False does not create the missing mathematical content; Lean correctly rejects these as non-proofs.
In summary, the run fails because the LLM does not supply the missing mathematical in-
frastructure required by the formal statement: (i) a correct, explicit connection between
IsFinitelyPresentable in Grp and the concrete PresentedGroup-based predicate, and
(ii) a correct nontrivial filtered diagram witnessing X as a filtered colimit of finitely presented groups.
When those are not available, the LLM falls back to lemma-name guessing and tactic placeholders,
which do not typecheck or do not solve the goals, so verification never succeeds.

F    DATASHEET FOR DATASETS
       • Motivation: To benchmark library-level abstraction reasoning in LLMs.
       • Composition: 100 pairs of Natural Language and Lean 4 statement code.
       • Collection Process: Expert curation from textbooks, unpublished lecture note and research
         papers.
       • Maintenance: Hosted on GitHub under MIT.




                                                   22
