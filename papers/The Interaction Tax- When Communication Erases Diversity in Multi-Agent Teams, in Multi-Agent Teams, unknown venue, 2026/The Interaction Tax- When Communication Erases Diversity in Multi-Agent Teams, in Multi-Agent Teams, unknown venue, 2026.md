                                                         The Interaction Tax: When Communication Erases Diversity
                                                                            in Multi-Agent Teams


                                                                             Summer Eunhyung Ann Haokun Liu Chenhao Tan


                                                                    Abstract                                useful for optimization tasks, where the goal is to find one
                                                                                                            strong solution from many possible candidates. A diverse
                                                Does multi-agent LLM interaction help or hurt?
arXiv:2608.23541v1 [cs.MA] 24 Aug 2026




                                                                                                            team can cover more of the solution space, but only if those
                                                Some work reports gains from debate (Du et al.,             differences survive later interaction.
                                                2024), critique loops (Chen et al., 2025), and
                                                mixture-of-agents synthesis (Wang et al., 2025),            Recent work gives mixed evidence about whether interac-
                                                while other work finds that interaction adds cost           tion helps. Debate, critique loops, and mixture-of-agents
                                                without improving quality under equal budgets               systems report gains from agents reading, reviewing, or syn-
                                                (Tran & Kiela, 2026; Xu et al., 2026; Jarrett et al.,       thesizing each other’s outputs (Du et al., 2024; Chen et al.,
                                                2025), or that independent sampling already cap-            2025; Wang et al., 2025). Other work finds that multi-agent
                                                tures multi-agent gains (Li et al., 2024). We ar-           systems can add cost without improving quality under equal
                                                gue this contradiction reflects a missing distinc-          budgets (Tran & Kiela, 2026; Xu et al., 2026; Jarrett et al.,
                                                tion, because not all multi-agent communication             2025), or that independent sampling already captures much
                                                is equal. Different model families find structurally        of the benefit of using multiple agents (Li et al., 2024). One
                                                different solutions, but when agents read each              reason these results can coexist is that some systems let
                                                other’s complete outputs, their proposals converge          agents read complete solutions before they answer again,
                                                within one round, erasing the diversity that moti-          while others keep solutions independent until selection or
                                                vates using multiple models. We call this the in-           synthesis.
                                                teraction tax. We test 11 verifier-scored optimiza-         We study this on 11 verifier-scored optimization tasks. Each
                                                tion tasks under matched budgets and find that              agent outputs a candidate solution, and a deterministic ver-
                                                full-solution interaction is a weak default. Inde-          ifier returns a scalar score. Claude, GPT-4o, and Gemini
                                                pendent proposal generation avoids this collapse.           each achieve the best score on at least one task, while each
                                                Full-solution interaction mainly makes agents stay          same-model team scores zero on at least one task. A diverse
                                                close to the first solution they see instead of try-        set of models can therefore find solutions that a same-model
                                                ing different approaches, and critique helps only           team may miss.
                                                if the violated rule is easy for the LLM to find and
                                                fix. These results suggest that multi-agent per-            We then test what happens when agents exchange full can-
                                                formance depends less on the number of agents               didate solutions. When agents read each other’s complete
                                                than on the information they exchange, and in-              outputs, their later solutions become more similar after one
                                                teraction helps only when agents share the right            round, as shown in Figure 1. This can help same-model
                                                information at the right time.                              teams, where agents start from similar solutions, but it often
                                                                                                            hurts diverse-model teams, where the useful difference is
                                                                                                            erased. We call this loss the interaction tax.
                                                                                                            The tax does not mean that all communication is harmful.
                                         1. Introduction                                                    MoA (Wang et al., 2025) avoids the collapse because agents
                                         Multi-agent LLM systems are often used because differ-             produce candidate solutions independently before synthesis.
                                         ent models may find different solutions. This is especially        Critique can also help when it shows a fault that the model
                                                                                                            can find and repair, as in Knapsack, but is less reliable when
                                            1
                                             Department of Computer Science, University of Chicago,         the fault is harder to locate, as in 3AP-Free.
                                         Chicago, IL, USA. Correspondence to: Summer Eunhyung Ann
                                         <summereunann@uchicago.edu>.                                       Our main contribution is to show that full-solution interac-
                                                                                                            tion is a weak default. Idit can erase useful model diversity,
                                         Proceedings of the 43 rd International Conference on Machine       while independent generation and repair-focused critique
                                         Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026
                                                                                                            avoid this failure in different ways.
                                         by the author(s).

                                                                                                        1
                       The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams




       (a) Independent proposals            (b) Full-solution exchange drives convergence          (c) Selection preserves diversity
Figure 1. The interaction tax on optimization tasks. Different model families (Claude, GPT-4o, Gemini) find structurally different
solutions. When agents exchange full candidate solutions, their proposals converge and diversity is lost. When agents generate
independently and the best is selected, diversity is preserved.


2. Related Work                                                          3. Methods
Single vs. multi-agent comparisons. Multi-agent debate                   Setup. Each task is scored by a deterministic evaluator.
improves factuality (Du et al., 2024), MAgICoRe raises                   Each configuration is a workflow run under identical re-
math accuracy through solver-reviewer-refiner loops (Chen                source budgets (details in supplementary). Agents see a
et al., 2025), and MoA synthesis dioutperforms individual                visible dev evaluator during search. Protocols use this score
models on language benchmarks (Wang et al., 2025). On                    for refinement, selection, critique, and aggregation. After
the other side, Tran and Kiela (Tran & Kiela, 2026), Xu et               the run, the dev-selected artifact is evaluated once by a hid-
al. (Xu et al., 2026), Li et al. (Li et al., 2024), and Jarrett et       den evaluator. Hidden evaluators are stricter, more complete,
al. (Jarrett et al., 2025) each demonstrate multi-agent losses           or robustness-shifted checks designed to test whether a so-
under various conditions, but all use same-model teams or                lution found using the visible scorer still holds up offline.
do not control for model diversity. Our work isolates model              We use hidden scores for MEG comparisons and visible
diversity as a variable and tests when interaction preserves             feasibility for the two hard-validity analyses. Visible and
or erases the solution diversity that diverse models provide.            hidden rankings diverge on three of the tasks analyzed with
                                                                         hidden scores.
Evolutionary approaches. FunSearch (Romera-Paredes
et al., 2024), Evolution through Large Models (Lehman                    We test ten configurations from a larger protocol pool (see
et al., 2023), and AlphaEvolve (Georgiev et al., 2025) em-               supplementary) built from Claude Sonnet 4 (Anthropic,
bed LLMs inside evolutionary loops for mathematical dis-                 2025), GPT-4o (OpenAI, 2024), and Gemini 2.5 Flash
covery. These approaches preserve population diversity                   (Google DeepMind, 2025). Four are single-agent base-
through selection pressure rather than through agent interac-            lines (Single-Shot, Best-of-N sampling, Self-Refine, and
tion, sidestepping the convergence mechanism we study.                   Verifier-Guided Search). The remaining configurations are
                                                                         multi-agent workflows spanning sequential revision (Chain),
Ensemble diversity theory. The ensemble diversity de-
                                                                         solver-reviewer-refiner critique (MAgICoRe (Chen et al.,
composition (Krogh & Vedelsby, 1994; Hansen & Sala-
                                                                         2025)), critique exchange (Debate (Du et al., 2024)), plan-
mon, 1990; Lakshminarayanan et al., 2017) shows that en-
                                                                         and-execute (HPE (Wang et al., 2023)), and independent-
semble error equals mean member error minus a diversity
                                                                         proposer synthesis (MoA (Wang et al., 2025)). MoA is the
term. When members communicate and converge, diver-
                                                                         only configuration where proposers never read each other’s
sity shrinks toward zero. The interaction tax is a structural
                                                                         outputs. The benchmark contains 11 verifier-scored opti-
instance of this effect.
                                                                         mization tasks, with four adapted from the AlphaEvolve
                                                                         suite (Georgiev et al., 2025) (full configuration and task de-
                                                                         tails in supplementary). All tasks share the same interface,
                                                                         where agents output JSON candidate solutions and determin-
                                                                         istic verifiers return scalar scores. Tasks differ in feedback

                                                                     2
                        The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

                 (a) No configuration reliably beats single-agent baseline

         MoA
                                                                                                                           (b) Interaction erases diversity
                                                                        CI includes 0




                                                                                                                            x
   Self-Refine




                                                                                                                           y=
                                                                                                                     0.2                                    interaction
                                                                                                                                                            helps both
    Best-of-N




                                                                                        MIG, diverse-model agents
  Cross-Chain                                                                                                        0.1

  Homo-Chain                                                                                                                                            MoA
                                                                                                                     0.0                                    Chain
   MAgICoRe
                                                                                                                                                           MAgICoRe
                                                                                                                                            Debate
          VGS                                                                                                       −0.1
        Debate                                                                                                                    HPE
                                                                                                                                   interaction           diversity tax zone
   Single-Shot
                                                                                                                    −0.2          always hurts

                                                    MoA (diverse)
                                                    Multi-agent w/ interaction
                                                                                                                           −0.2      −0.1         0.0          0.1            0.2
          HPE                                       Single-agent controls                                                           MIG, same-model agents

             −0.30 −0.25 −0.20 −0.15 −0.10 −0.05            0.00      0.05
                           Aggregate MEG (95% CI, 9 tasks)

Figure 2. (a) Aggregate MEG for all ten configurations (95% CI, 9 tasks). MoA is the only configuration whose confidence interval
includes zero. (b) MIG quadrant scatter (x-axis = same-model MIG, y-axis = diverse-model MIG). MAgICoRe, Chain, and Debate
occupy the interaction tax zone (bottom-right quadrant), where full-solution interaction helps same-model agents but hurts once models
are diverse. MoA escapes to the top-right because its proposers never see each other’s outputs.


structure. On graded-feedback tasks (e.g., MaxCut, Cir-                      erage translates into a measurable performance advantage,
cle Packing), almost every well-formed answer receives a                     we run a controlled factorial experiment.
meaningful score. On hard-validity tasks (e.g., Knapsack,
3AP-Free), a structural rule must be satisfied before the                    Table 1. Best-of-N Q-scores per model on six tasks where scores
score is meaningful, and a small edit can violate the rule and               diverge. Bold = best model. Each model family wins on different
collapse the score. Raw scores are normalized to Q ∈ [0, 1].                 tasks.
The main benchmark uses five seeds per cell, and the 2×2                         Task                                      Claude      GPT-4o        Gemini          Winner
factorial uses ten seeds on three tasks with sufficient score
                                                                                 Circle Packing                            1.000          0.519          0.745       Claude
variance (task subsets noted per figure).
                                                                                 TSP-50                                    0.141             —           0.115       Claude
Metrics. Positive MEG means the configuration outper-                            Erdős                                     0.131        0.710           0.142       GPT-4o
                                                                                 TSP-100                                    0.013        0.021           0.010       GPT-4o
formed every single-agent baseline. Positive MIG means
                                                                                 DiffBases                                  0.209         0.264         0.610        Gemini
interaction improved over independent generation. The                            Flat Poly                                  0.000         0.007         0.143        Gemini
diverse parallel baseline is inherently stronger because it
benefits from coverage, so negative diverse MIG is a conser-
vative finding (formal definitions in supplementary).                        A controlled check on the diversity advantage. A 2×2 fac-
                                                                             torial crosses model diversity (same vs. diverse proposers)
                                                                             with synthesis (MoA synthesis vs. best-score selection) on
4. Results                                                                   three tasks with sufficient Q-score variance (N =120, task-
Diversity creates coverage. Every same-model team has                        stratified bootstrap). The diversity coefficient is +0.188
at least one task with Q=0 (Table 1), so no single model                     (CI [+0.073, +0.299], p<0.001, factorial table in supple-
covers all tasks. A diverse team (Claude + GPT-4o + Gem-                     mentary). The synthesis coefficient is near zero. Leave-
ini) never scores zero on any task, even though its aggregate                one-out analysis (supplementary) shows the finding is task-
Q is comparable to the best same-model team (capability                      dependent (see Limitations).
confound check in supplementary). To test whether this cov-                  The interaction tax. Same-model interaction can refine
                                                                             proposals. Chain, MAgICoRe, and Debate all produce posi-

                                                                         3
                        The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

tive same-model MIG (Table 2). With diverse models, all               guidance rather than a concrete repair (per-run breakdown
three turn negative (Chain −0.024, MAgICoRe −0.035, De-               in supplementary).
bate −0.078), with bootstrap P (same>div) ≥ 88%. For
MAgICoRe and Debate, only the models change across con-
ditions, so the loss is consistent with the diversity erased by       Table 3. Explicit feasibility rates on Knapsack and 3AP-Free
full-solution interaction. MoA’s MIG remains positive from            (n=10 per cell). On Knapsack (fault easy to locate), diverse
same-model to diverse (+0.012 → +0.016), which sug-                   models help. On 3AP-Free (fault hard to locate), diverse models
                                                                      hurt.
gests the damage comes from the full-solution interaction
step. No configuration achieves positive aggregate MEG                 Task             Config        Same     Diverse    Direction
(Figure 2).
                                                                                        MAgICoRe       1/10       2/10    ≈
                                                                       Knapsack-50
                                                                                        Debate         2/10      10/10    Div. helps
Table 2.     Mean MIG per configuration family (8 tasks).                               MAgICoRe       6/10       3/10    Div. hurts
P (same>div): bootstrap probability that same-model MIG ex-            3AP-Free-100
                                                                                        Debate         6/10       0/10    Div. hurts
ceeds diverse MIG.

        Configuration     Same MIG    Div MIG       P
        Chain               +0.051     −0.024     97%
        MAgICoRe            +0.044     −0.035     99%                 5. Discussion and Conclusion
        Debate              +0.012     −0.078     88%
        HPE                 −0.163     −0.145     38%                 Our experiments show that full-solution interaction can de-
        MoA                 +0.012     +0.016     42%                 stroy the diversity it is meant to exploit. When agents read
                                                                      each other’s complete outputs, solutions converge within
                                                                      a single round of full-solution interaction. MoA, where
How convergence happens. This loss is immediate because
                                                                      proposers never see each other’s outputs, is the only config-
diversity collapses within a single round of full-solution in-
                                                                      uration whose diverse MIG remains positive.
teraction. On Erdős, diverse Debate achieves a strong inter-
mediate score at round 2 but regresses at round 3 once agents         These results suggest that multi-agent performance depends
read each other’s full solutions (round-by-round scores in            less on the number of agents than on the information they ex-
supplementary). Across protocols, mean pairwise distance              change and when it is exposed. Full candidate solutions cre-
between agents’ solution representations falls from 0.315             ate strong convergence. Lower-bandwidth signals, such as
before interaction to 0.229 after. The damage happens at              scores, method descriptions, or failure causes, may preserve
the moment of full output exchange, not gradually over mul-           independent exploration while still supporting coordination.
tiple rounds. The collapse happens because synthesis does             Evolutionary approaches like FunSearch (Romera-Paredes
not recombine proposals. On five of seven tasks, synthesis            et al., 2024) and AlphaEvolve (Georgiev et al., 2025) already
copies the best proposer’s output ≥80% of the time rather             do this in effect, preserving population diversity through
than combining parts from each (classification table in sup-          selection pressure rather than through agent interaction. Cri-
plementary). On Erdős, GPT-4o outputs the identical trivial          tique is most useful when it identifies a concrete repair, as
constant on 100% of seeds (Q=0.710), so any interaction               in Knapsack, and can be harmful when the relevant error is
or synthesis step converges to that single point regardless of        difficult for the LLM to locate reliably, as in 3AP-Free.
what Claude or Gemini proposed.
                                                                      Limitations and future work. The coverage finding is task-
Critique helps only when the fault is easy to locate. In              dependent (removing Erdős drops the diversity coefficient to
our experiments, the interaction tax reverses only when the           +0.014 with CI crossing zero). The main benchmark uses
shared information points to a concrete, repairable fault.            only five seeds per condition, and the diversity factorial uses
In Knapsack-50, a failed solution usually violates a capac-           ten seeds on only three tasks. The explicit feasibility analy-
ity constraint, and the critic can propose a direct repair by         sis rests on two hard-validity tasks, Knapsack and 3AP-Free,
removing or swapping overweight items. Diverse Debate                 although other tasks such as TSP also have hard structural
achieves 10/10 feasibility versus 2/10 for same-model De-             constraints. All tasks are verifier-scored optimization prob-
bate (Table 3). In contrast, 3AP-Free-100 also has an exact           lems, so the interaction tax may not transfer unchanged to
verifier, but locating the violated rule requires finding an          open-ended writing, planning, or dialogue settings. Our
arithmetic-progression triple among many combinations.                experiments identify full-solution interaction as a weak de-
Diverse Debate drops to 0/10 versus 6/10 for same-model.              fault, but they do not directly test which lower-bandwidth
The same qualitative contrast appears under MAgICoRe,                 information channel is best. A natural next step is a sharing
though the Knapsack effect is weaker. On graded-feedback              ablation over scores, method descriptions, failure causes,
tasks, the first critique round degrades solutions 57% of the         verified summaries, and late crossover. Code and data are
time (17/30 runs), consistent with critique offering general          available in the supplementary material.

                                                                  4
                     The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

References                                                          Tran, D. and Kiela, D. Single-agent LLMs outperform
                                                                      multi-agent systems on multi-hop reasoning under equal
Anthropic. The claude model card, 2025. URL
                                                                      thinking token budgets, 2026. arXiv:2604.02460.
  https://docs.anthropic.com/en/docs/
  about-claude/models.                                              Wang, J. et al. Mixture-of-agents enhances large lan-
                                                                     guage model capabilities. In ICLR Spotlight, 2025.
Bianchi, F., Kwon, M., and Zou, J. EinsteinArena: Har-               arXiv:2406.04692.
  nessing the collective intelligence of agents in the wild
  to advance science. https://www.together.ai/                      Wang, L. et al. Plan-and-solve prompting: Improving zero-
  blog/einsteinarena, 2025. Together AI.                             shot chain-of-thought reasoning by large language mod-
                                                                     els. In ACL, 2023. arXiv:2305.04091.
Chen, J. C.-Y. et al. MAgICoRe: Multi-agent, iterative,
  coarse-to-fine refinement for reasoning. In EMNLP, 2025.          Xu, J. et al. Rethinking the value of multi-agent workflow:
  arXiv:2409.12147.                                                  A strong single agent baseline, 2026. arXiv:2601.12307.

Du, Y. et al. Improving factuality and reasoning in lan-
  guage models through multiagent debate. In ICML, 2024.
  arXiv:2305.14325.

Georgiev, B., Gómez-Serrano, J., Tao, T., and Wagner, A. Z.
  Mathematical exploration and discovery at scale, 2025.
  arXiv:2511.02864.

Google DeepMind. Gemini 2.5: Our most intelligent AI
  model, 2025. URL https://deepmind.google/
  technologies/gemini/.

Hansen, L. K. and Salamon, P. Neural network ensembles.
  IEEE Transactions on Pattern Analysis and Machine In-
  telligence, 12(10):993–1001, 1990.

Jarrett, D. et al. Multi-agent teams hold experts back, 2025.
   arXiv:2602.01011.

Krogh, A. and Vedelsby, J. Neural network ensembles, cross
  validation, and active learning. In Advances in Neural
  Information Processing Systems, volume 7, 1994.

Lakshminarayanan, B., Pritzel, A., and Blundell, C. Simple
  and scalable predictive uncertainty estimation using deep
  ensembles. In Advances in Neural Information Process-
  ing Systems, volume 30, 2017.

Lehman, J. et al. Evolution through large models, 2023.
  arXiv:2206.08896.

Li, J. et al.   More agents is all you need, 2024.
  arXiv:2402.05120.

OpenAI. GPT-4o system card, 2024. arXiv:2410.21276.

Romera-Paredes, B. et al. Mathematical discoveries from
  program search with large language models. Nature, 625:
  468–475, 2024.

Sung, J. JSAgent: An ai agent for mathematical dis-
  covery on EinsteinArena. https://github.com/
  jmsung/einstein, 2026.

                                                                5
                      The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

Supplementary Material
                                                                      # Verify saved scores (~3 min, no API key)
This appendix provides workflow details, reproducibility              npx tsx tools/evaluate.ts \
                                                                        --results results/full-v2 \
notes, and extended tables and figures for the main paper.              --task bench-difference-bases \
                                                                        --verifier both

                                                                      # Paper tables from cached results
A. Workflow Recipe                                                    python analysis/analyze_bench.py
                                                                      # -> results/analysis/meg_full.tsv
The paper’s practical claim is a reusable workflow for AI-
                                                                      # Re-run one cell (needs OPENROUTER_API_KEY)
assisted math/CS/ML optimization.                                     npx tsx src/runner/run-offline.ts \
                                                                        --task bench-difference-bases \
                                                                        --protocol moa --seeds 1,2,3
  1. Choose 2–3 diverse model families.
  2. Generate candidate solutions independently with no               The verification step prints a table of recorded vs. recom-
     cross-agent visibility.                                          puted scores; all rows should match exactly. Re-running
                                                                      one task with three seeds takes approximately 5 minutes
  3. Rank candidates with a visible deterministic checker             and costs under $1 via OpenRouter. Results are written
     or development evaluator.                                        to results/offline/. The full 11-task, 10-protocol
                                                                      benchmark with 10 seeds takes roughly 4 hours. The artifact
  4. If the task exposes local, checkable violations, allow           README contains the complete reproduction guide.
     critique-and-revise passes. Otherwise skip interaction
     and select among the independent candidates.
                                                                      D. Minimal End-to-End Example
  5. Verify the chosen artifact with a stricter held-out evalu-
     ator or deterministic check.                                     Below is a lightly condensed but faithful excerpt from a
                                                                      single MoA run on Molecule QED (seed 1, higher is better).
                                                                      Three proposers generate independently; the synthesizer
The reported gains motivating this rule are performance
                                                                      sees all three outputs and their dev scores.
and correctness gains, not a claim of universal time savings.
Backbone diversity contributes +0.188 in the 2×2 factorial            Proposer 1 (Claude, devScore = 0.828)
(though this is driven by the Erdős task; see Section L),              {"smiles":       "COc1ccc(Cc2cnc(N)nc2N)cc1"}
while critique raises feasibility from 0% to 47–73% only on
                                                                      Proposer 2 (GPT-4o, devScore = 0.685)
verifiable constraint tasks.
                                                                        {"smiles":       "O=C(C)Oc1ccccc1C(=O)NCc2ccccc2"}
                                                                      Proposer 3 (Gemini, devScore = 0.547)
B. Reproducibility and Verification                                     {"smiles":       "CC(=O)NCCC(=O)O"}
The artifact includes exact prompt templates for all configu-
rations, pinned model identifiers, task instances, determin-          Synthesizer (Claude). Receives all three proposals with
istic visible and hidden evaluators, saved JSON run traces            scores. Verbatim reasoning:
with raw model outputs, and scripts that reproduce every ta-
ble and figure from cached results. This makes the workflow               “Agent                   1’s               molecule
inspectable without re-running API calls and re-runnable                  COc1ccc(Cc2cnc(N)nc2N)cc1 contains:                 a
                                                                          methoxybenzene ring (drug-like aromatic system),
within a few hours with ordinary API access. Correctness                  a pyrimidine ring with amino groups (common in
is checked in three layers. Visible evaluators guide search.              pharmaceuticals), connected by a simple methylene
Hidden evaluators score the final artifact once. The anal-                bridge. . . Agent 2’s molecule has lower QED likely
ysis scripts recompute the reported statistics from saved                 due to suboptimal LogP or molecular weight, while
raw outputs. This separation matters because visible and                  Agent 3’s simple amino acid derivative lacks the
                                                                          structural complexity needed for high QED. Since
hidden rankings diverge on three of nine optimization tasks.              Agent 1 already achieved an excellent QED score of
Throughout this appendix, raw task scores follow each task’s              0.8279 with a synthetically accessible molecule that
native direction. Normalized Q is always higher-is-better.                balances all drug-likeness parameters optimally, this
                                                                          represents the superior solution.”
C. Quickstart Reproduction
                                                                      Final          output:              {"smiles":
The artifact runs on Node.js ≥ 20 and Python ≥ 3.10. No               "COc1ccc(Cc2cnc(N)nc2N)cc1"}             (devS-
GPU is required.                                                      core = 0.828, hiddenScore = 0.738).
# Install                                                             The synthesizer correctly identified the best proposal using
npm install && pip install -r requirements.txt
                                                                      the interpretable molecular structure and large score gap

                                                                  6
                                 The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

(0.83 ≫ 0.55). On tasks where one backbone produces a                                             I. Critique Regression Rates
fixed high-scoring constant (e.g., Erdős), synthesis always                                      Table 7. First-round critique regression rate (MAgICoRe, Gemini
converges to that constant, erasing the diversity of the other                                    backbone, n=15 per task). Constraint = Knapsack-50, 3AP-Free-
proposals (see the Erdős transcript in Section V below).                                         100. Optimization = Erdős, Flat Polynomials.

                                                                                                  Task type                  Regress 0→1          Any regress    n
E. Artifact Contents
                                                                                                  Constraint (2 tasks)          0/30 (0%)         5/30 (17%)     30
The      repository     at     https://github.com/                                                Optimization (2 tasks)       17/30 (57%)       25/30 (83%)     30
SummerAnn/interaction-tax contains: (i) all
                                                                                                  Table 8. Feasibility success rates on two constraint tasks (Gemini
11 task instances with embedded dev and hidden evaluators;
                                                                                                  backbone, n=15 each). Fisher exact p compares MAgICoRe to
(ii) verbatim prompt templates for all 10 configurations                                          Best-of-N .
(src/config/prompts.ts); (iii) pinned model
identifiers (src/config/models.ts); (iv) 1,556                                                    Task               BoN      Self-Ref     MAgICoRe        p
saved JSON run traces with raw model outputs, dev
                                                                                                  Knapsack-50         0%             13%           47%     0.003
scores, and hidden scores; (v) Python analysis scripts that                                       3AP-Free-100        0%              7%           73%     <0.001
reproduce every table and figure; and (vi) the offline runner
for re-executing any cell from scratch via OpenRouter.
                                                                                                  J. MIG per Configuration Family
F. Full Per-Task MEG                                                                              Table 9.     Mean MIG per configuration family (8 tasks).
                                                                                                  P (same>div): bootstrap probability that same-model MIG ex-
Table 4. Per-task MEG for all ten configurations. MaxCut and                                      ceeds diverse MIG.
LJ-n=41 omitted (all configurations score zero on both tasks).
Task          MoA       SR     BoN     XCh     HCh    MAgI     VGS     Deb      SS     HPE        Configuration          Same MIG               Div MIG          P
Circle Pack   −0.24   −0.03    0.00   −0.03    0.00    0.00    0.00   −0.52    0.00   −1.00
DiffBases
Flat Poly
              +0.09
              +0.01
                      −0.11
                      −0.06
                               0.00
                              −0.08
                                      −0.11
                                      −0.08
                                              −0.20
                                              −0.08
                                                      −0.15
                                                      −0.08
                                                              −0.13
                                                               0.00
                                                                      +0.11
                                                                      −0.04
                                                                              −0.20
                                                                              −0.08
                                                                                      −0.20
                                                                                      −0.08
                                                                                                  Chain                      +0.051              −0.024         97%
TSP-100
Erdős
              −0.02
              +0.02
                      −0.02
                       0.00
                              −0.01
                              −0.37
                                      −0.01
                                      −0.13
                                              −0.02
                                              −0.05
                                                      −0.01
                                                      −0.15
                                                               0.00
                                                              −0.48
                                                                      −0.02
                                                                      −0.33
                                                                              −0.01
                                                                              −0.48
                                                                                      −0.02
                                                                                      −0.48
                                                                                                  MAgICoRe                   +0.044              −0.035         99%
MolQED
TSP-50
              −0.01
              −0.05
                      −0.05
                      −0.08
                               0.00
                               0.00
                                      −0.10
                                      −0.02
                                              −0.12
                                              −0.04
                                                      −0.14
                                                      −0.05
                                                              −0.04
                                                               0.00
                                                                      +0.02
                                                                      −0.02
                                                                              −0.11
                                                                              −0.09
                                                                                      −0.24
                                                                                      −0.02
                                                                                                  Debate                     +0.012              −0.078         88%
                                                                                                  HPE                        −0.163              −0.145         38%
G. Per-Backbone Coverage                                                                          MoA                        +0.012              +0.016         42%
Table 5. Per-backbone Best-of-N Q-scores on six tasks where
backbone scores clearly diverge. Bold = best backbone. On Erdős,                                 K. 2×2 Factorial Estimates
GPT-4o’s Q=0.710 reflects a trivial constant (Section Y); Gemini
                                                                                                  Table 10. 2×2 factorial estimates (N =120, 10,000 task-stratified
averages Q=0.142 (4/5 seeds score Q=0, one seed matches GPT-
                                                                                                  bootstrap). Diversity is the only factor whose CI excludes zero.
4o).
                                                                                                  Term                               Estimate    95% CI
Task                          Claude          GPT-4o          Gemini           Winner
                                                                                                  Intercept (same + selection)        +0.182     [+0.123, +0.246]
Circle Packing                1.000             0.519           0.745          Claude             Diversity                           +0.188     [+0.073, +0.299]
TSP-50                        0.141                —            0.115          Claude             Synthesis                           −0.010     [−0.111, +0.094]
Erdős                         0.131           0.710            0.142          GPT-4o             Diversity × Synthesis               +0.046     [−0.132, +0.226]
TSP-100                        0.013           0.021            0.010          GPT-4o
DiffBases                      0.209            0.264          0.610           Gemini
Flat Poly                      0.000            0.007          0.143           Gemini             L. Leave-One-Out Sensitivity
                                                                                                  Table 11. Leave-one-out sensitivity of the diversity main effect.
                                                                                                  Only removing Erdős drops the coefficient to near zero.
H. Capability Confound Check
Table 6. MoA-no-synthesis aggregate Q-scores across nine op-                                      Task withheld              β̂div               95% CI    p
timization tasks (n=10 per condition). The diverse team and                                       None (N =120)         +0.188        [+0.073, +0.299]     <0.001
GPT-4o×3 have similar point estimates, but each same-model                                        Erdős (n=80)         +0.014        [−0.109, +0.139]     0.84
team catastrophically fails on at least one task (Q=0.000), while
                                                                                                  DiffBases (n=80)      +0.265        [+0.142, +0.381]     <0.001
the diverse team never does.
                                                                                                  MolQED (n=80)         +0.286        [+0.125, +0.442]     <0.001
Configuration                                          Aggregate Q            Min task Q
Diverse (Claude + GPT-4o + Gemini)                              0.349         >0                  M. Convergence Mechanism
GPT-4o×3                                                        0.215         0.000
Gemini×3                                                        0.250         0.000               Step-level trajectories reveal when diversity dies. On Erdős,
                                                                                                  diverse Debate achieves a strong intermediate score at

                                                                                              7
                                                                                                                                              The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

round 2, when agents exchange only critiques, but collapses                                                                                                                                                                                                                                                                                     P. Per-Task MIG Breakdown
at round 3 once agents read each other’s full solutions. The                                                                                                                                                                                                                                                                                    Table 14. MIG per task for five configuration families (eight op-
damage occurs at the moment of full output exchange, not                                                                                                                                                                                                                                                                                        timization tasks). Bold marks Erdős sign flips. On tasks with no
gradually.                                                                                                                                                                                                                                                                                                                                      Q-score variance (MaxCut, LJ-n41), MIG is zero for all configura-
                                                        (a) Difference Bases      visible scores by interaction step                                                 (b) Erd s Overlap    visible scores by interaction step                                                             (c) Erd s   diversity exists before interaction
                                                                                                                                                                                                                                                                                                                                                tions.
                                                                                             Debate diverse                                                   20.0                                     Debate diverse (5 seeds)                                                0.50
Visible score (dev; lower is better, log scale)




                                                                                             Homo-chain (Gemini)                                                                                       Cross-chain (5 seeds)




                                                                                                                                                                                                                                   Best visible score (dev; lower is better)
                                                                                             Cross-chain (diverse)                                            17.5
                                                                                                                       Visible score (dev; lower is better)                                                                                                                                                                                     Family               Cfg           MCut           CPack           DBases             FPoly           TSP1         LJ41        Erdős         MolQ
                                                  104
                                                                                                                                                                                                                                                                               0.45
                                                                                                                                                              15.0

                                                  103
                                                                                                                                                              12.5                                                                                                             0.40                                                             MAgICoRe             homo             0.00            0.00          +0.05              0.00          0.00         0.00       +0.33          −0.03
                                                                                                                                                              10.0
                                                                                                                                                                                                                                                                               0.35
                                                                                                                                                                                                                                                                                                                                                MAgICoRe             mixed            0.00            0.00          −0.07              0.00         −0.01         0.00       −0.28          +0.09
                                                                                                                                                               7.5
                                                  102
                                                                                                                                                               5.0
                                                                                                                                                                                                                                                                               0.30
                                                                                                                                                                                                                                                                                                                                                Debate               homo             0.00        −0.52             +0.31           +0.04           −0.01         0.00       +0.14          +0.13
                                                  101                                                                                                          2.5                                                                                                                                                                              Debate               mixed            0.00        −0.60             −0.14           +0.02            0.00         0.00       +0.14          −0.04
                                                                                                                                                               0.0                                                                                                             0.25
                                                         Step 1          Step 2             Step 3
                                                                               Interaction step
                                                                                                                                                                     Step 1                   Step 2
                                                                                                                                                                                         Interaction step
                                                                                                                                                                                                                          Step 3                                                      MoA-nosynth
                                                                                                                                                                                                                                                                                       (diverse)
                                                                                                                                                                                                                                                                                                       BoN
                                                                                                                                                                                                                                                                                                     (Claude)
                                                                                                                                                                                                                                                                                                                     BoN
                                                                                                                                                                                                                                                                                                                   (Gemini)
                                                                                                                                                                                                                                                                                                                                   BoN
                                                                                                                                                                                                                                                                                                                                 (GPT-4o)
                                                                                                                                                                                                                                                                                                                                                Chain                homo             0.00         0.00              0.00            0.00           −0.01         0.00       +0.43          −0.01
                                                                                                                                                                                                                                                                                                                                                XChain               mixed            0.00        −0.03             −0.06           −0.03           +0.01         0.00       −0.08          +0.01
Figure 3. Per-round visible-score trajectories on two optimization                                                                                                                                                                                                                                                                              MoA                  homo             0.00        −0.08             +0.07            0.00           −0.01         0.00       +0.07          +0.04
                                                                                                                                                                                                                                                                                                                                                MoA                  mixed            0.00        −0.24             +0.15           +0.06           −0.01         0.00       +0.07          +0.10
tasks. (a) DiffBases: sequential interaction often improves at
step 2 but loses that advantage by the final step. (b) Erdős: diverse
interaction improves at round 2 then regresses at round 3 after                                                                                                                                                                                                                                                                                 Q. Agent Configurations
agents exchange full outputs. (c) Erdős: diverse MoA-nosynth
achieves broader coverage than same-backbone Best-of-N .                                                                                                                                                                                                                                                                                        Table 15. Agent configurations. All operate under the same budget
                                                                                                                                                                                                                                                                                                                                                vector (T =200K, W =600s, C=30s, K=25). HPE = Hierarchi-
                                                                                                                                                                                                                                                                                                                                                cal Planner-Executor. Two MoA ablations (same-model proposers,
N. Diversity Collapse                                                                                                                                                                                                                                                                                                                           no synthesis) are used in the 2×2 analysis.
                                                                                                                                                                                                                                                                                                                                                Configuration      Role      Mechanism                                                                             Ref.
Table 12. Mean pairwise solution distance. After synthesis, diverse                                                                                                                                                                                                                                                                             Single-Shot        Control   One model, one attempt, no iteration.                                                 —
MoA distance (0.315) falls to 0.229.                                                                                                                                                                                                                                                                                                            Best-of-N (N =8)
                                                                                                                                                                                                                                                                                                                                                Self-Refine
                                                                                                                                                                                                                                                                                                                                                                   Control
                                                                                                                                                                                                                                                                                                                                                                   Control
                                                                                                                                                                                                                                                                                                                                                                             8 independent samples, return visible-best.
                                                                                                                                                                                                                                                                                                                                                                             Same model generates, critiques, revises for 3 rounds.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   —
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Madaan et al., 2023
                                                                                                                                                                                                                                                                                                                                                VGS                Control   Evolutionary loop (pop. 4, gen. 5, elite 2) with visible scores as fitness.           Romera-Paredes et al., 2024
                                                                                                                                                                                                                                                                                                                                                Homo-Chain         Multi     4 same-model agents in sequence, each revises prior output. Visible-best returned.    This work
                                                                                                                                                                                                                                                                                                                                                Cross-Chain        Multi     3-agent chain (Claude → GPT-4o → Gemini). Visible-best returned.                      This work
Configuration                                                                                                                                                                                                   Avg pairwise distance                                                                                                           MAgICoRe
                                                                                                                                                                                                                                                                                                                                                Debate
                                                                                                                                                                                                                                                                                                                                                                   Multi
                                                                                                                                                                                                                                                                                                                                                                   Multi
                                                                                                                                                                                                                                                                                                                                                                             Solver → reviewer → refiner, 2 rounds.
                                                                                                                                                                                                                                                                                                                                                                             2 agents propose, exchange critiques (2 rounds), synthesizer merges.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Chen et al., 2025
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Du et al., 2024
                                                                                                                                                                                                                                                                                                                                                HPE                Multi     Planner decomposes, executors solve subproblems, integrator assembles.                Wang et al., 2023; Hong et al., 2023
                                                                                                                                                                                                                                                                                                                                                MoA                Multi     3 proposers generate independently, 1 synthesizer combines.                           Wang et al., 2025
MoA (no synthesis)                                                                                                                                                                                                                                                                                                   0.315
Best-of-N (same model)                                                                                                                                                                                                                                                                                               0.312
                                                                                                                                                                                                                                                                                                                                                All proposer calls use temperature 0.7; critique and synthe-
Debate                                                                                                                                                                                                                                                                                                               0.309
                                                                                                                                                                                                                                                                                                                                                sis calls use 0.3–0.5, consistent across backbones.
MoA (diverse + synthesis)                                                                                                                                                                                                                                                                                            0.229
                                                                                                                                                                                                                                                                                                                                                R. Synthesis Decision Quality
O. Visible–Hidden Rank Agreement
                                                                                                                                                                                                                                                                                                                                                Table 16. Synthesis output classified relative to the best-scoring
Table 13. Spearman rank correlation between visible and hidden                                                                                                                                                                                                                                                                                  proposer. On five of seven tasks synthesis copies the best proposal
configuration rankings per task (n=10 configurations). Three                                                                                                                                                                                                                                                                                    ≥80% of the time. On Difference Bases it degrades 50% of the
tasks show ρ < 1.                                                                                                                                                                                                                                                                                                                               time.

Task                                                                                                                                                                     ρ                 Top-3 overlap                                                                                             Top-1 inv?                                 Task                                                    Improved                                Copied                     Degraded
MaxCut                                                                                                                 0.891                                                               2/3                                                                                                                   Yes                            Circle Packing                                                          60%                          40%                                  0%
Circle Packing                                                                                                         1.000                                                               3/3                                                                                                                   No                             Molecule QED                                                            20%                          80%                                  0%
DiffBases                                                                                                              0.806                                                               2/3                                                                                                                   No                             Erdős                                                                  10%                          80%                                 10%
Flat Poly                                                                                                              1.000                                                               3/3                                                                                                                   No                             Flat Polynomials                                                         0%                         100%                                  0%
TSP-100                                                                                                                1.000                                                               3/3                                                                                                                   No                             TSP-100                                                                  0%                         100%                                  0%
LJ-n=41                                                                                                                1.000                                                               3/3                                                                                                                   No                             TSP-50                                                                   0%                          90%                                 10%
Erdős                                                                                                                 1.000                                                               3/3                                                                                                                   No                             Difference Bases                                                         7%                          43%                                 50%
MolQED                                                                                                                 0.952                                                               3/3                                                                                                                   No
TSP-50                                                                                                                 1.000                                                               3/3                                                                                                                   No




                                                                                                                                                                                                                                                                                                                                            8
                               The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

S. Within-Backbone Comparisons (n=15)
                                                                                          Output format: a single Python code block.
Table 17. Within-backbone comparisons (Gemini, n=15 per con-
dition). Positive d = iterative configuration is worse.
                                                                                          Reviewer prompt (used in MAgICoRe, Debate).
Task               Config            Iter          BoN             d      p               System: You are a mathematical reviewer.
                                                                                          Analyze the proposed solution for correctness.
Flat Poly          MAgI-G           2.087      1.899        +1.25         0.002           List specific errors, constraint violations,
Flat Poly          SR-G             2.020      1.899        +1.02         0.009           or improvements.

TSP-100            MAgI-G          53,351     50,786        +1.42         0.001           User: Task: [OBJECTIVE]
TSP-100            SR-G            53,239     50,786        +1.46         0.001           Proposed solution (scored [VISIBLE_SCORE]):
                                                                                          [SOLUTION_CODE]
TSP-50             MAgI-G          24,167     23,103        +1.23         0.002
MolQED             MAgI-G           0.863      0.859        +0.05         0.93            Provide a numbered list of issues and concrete
                                                                                          suggestions for improvement.


T. Task Descriptions                                                                      The proposer prompt is identical across configurations; only
                                                                                          the orchestration (whether agents see prior outputs) differs.
Table 18. Benchmark tasks. Four optimization tasks are adapted
from AlphaEvolve (Georgiev et al., 2025) with smaller parame-                             The reviewer prompt is used only in critique-based config-
terizations. Two constraint tasks test interaction under checkable                        urations. All prompts, including the synthesizer prompt
violations.                                                                               for MoA and the planner/executor prompts for HPE, are
                                                                                          included verbatim in the artifact.
Task                 Domain           Type           Objective
Circle Packing       Geometry         Optimization   Maximize radius of n non-
                                                     overlapping circles in a unit        V. Example Multi-Agent Exchange
                                                     square
Difference Bases     Combinatorics    Optimization   Find a set whose pairwise dif-
                                                     ferences cover all residues
                                                                                          Below is a condensed transcript from a Cross-Chain run on
                                                     mod n                                Erdős (seed 1). On Erdős, lower raw scores are better; after
Erdős Overlap       Analysis         Optimization   Minimize
                                                            R                             Q-normalization, higher Q is always better.
                                                     maxt |f (x)f (x+t)| dx
                                                     over translates
Flat Polynomials     Algebra          Optimization   Minimize ∥p∥∞ for a poly-
                                                                                          Example 1. Sequential interaction converges to a degen-
                                                     nomial with ±1 coefficients          erate constant (Cross-Chain, Erdős, seed 1).
TSP-50 / TSP-100     Routing          Optimization   Minimize tour length for 50
                                                     or 100 cities                        Step 1 (Claude, dev score = 0.500). Claude reasons about
MaxCut               Graph theory     Optimization   Maximize cut value in a fixed
                                                     graph
                                                                                          minimizing overlap with translates and produces a struc-
LJ-n=41              Chemistry        Optimization   Minimize Lennard-Jones po-           tured sparse function using binary patterns.
                                                     tential for 41 atoms
Molecule QED         Drug design      Optimization   Maximize quantitative esti-          Step 2 (GPT-4o, dev score = 0.250). GPT-4o sees Claude’s
                                                     mate of drug-likeness (QED
                                                     score)
                                                                                          solution but outputs a trivial constant f = 0.5. GPT-4o
Knapsack-50          Combinatorics    Constraint     Maximize value subject to            defaults to near-constant functions on this task regardless of
                                                     weight capacity constraint           input context (Q=0.710, best single backbone on Erdős).
3AP-Free-100         Combinatorics    Constraint     Find the largest 3-AP-free
                                                     subset of {1, . . . , 100}
                                                                                          Step 3 (Gemini, dev score = 0.694). Gemini produces a
                                                                                          structured binary pattern but scores worse than GPT-4o. The
MaxCut and LJ-n=41 are omitted from most analyses be-                                     chain’s visible-best selection picks GPT-4o’s output (0.250,
cause all configurations score Q=0 on both tasks under the                                lowest hence best).
given budget, providing no inter-configuration signal.
                                                                                          GPT-4o’s trivial constant is genuinely the best-scoring so-
                                                                                          lution (Q=0.710), but it contributes zero strategy diversity
U. Representative Prompt Templates                                                        because every GPT-4o seed produces the identical output
Full prompt templates for all ten configurations are available                            (Table 21). When a chain includes GPT-4o on Erdős, the
in the release artifact. Below we show the structure of two                               non-trivial solutions from Claude and Gemini are discarded
representative prompts.                                                                   in favor of a degenerate constant. Under independent gener-
                                                                                          ation (MoA-nosynth), the same three models produce raw
Proposer prompt (used in MoA, Best-of-N , Single-Shot).                                   scores of 2.47 (Q=0), 0.34 (Q=0.710), and 0.50 (Q=0);
System: You are a mathematical optimization
                                                                                          the best (0.34, Q=0.710) is selected, outperforming any
agent. Your goal is to [OBJECTIVE]. Return                                                single-backbone run.
ONLY executable Python code that prints the
solution as a JSON object.

User: [Full task description with parameters,
constraints, input data, and evaluation
function specification.]


                                                                                      9
                          The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

W. Per-Task 2×2 Cell Means                                                           Y. Model Strategy Classification
Table 19. Mean Q-scores for each arm of the 2×2 diversity ×                          Table 21. Strategy frequency per backbone on Erdős and DiffBases,
synthesis factorial, broken down by task (n=10 per cell). The                        classified from rawOutput keywords across all single-shot seeds.
diversity contrast shows that Erdős drives the aggregate diversity                  Categories are non-exclusive keyword tags. GPT-4o outputs a
coefficient, DiffBases contributes moderately, and MolQED con-                       trivial constant (≈0.005) on 100% of Erdős runs. Gemini also
tributes near zero. The synthesis contrast is near zero on all three                 produces near-trivial constants (all zeros, raw score ≈0.503). Only
tasks.                                                                               Claude generates structurally varied, non-trivial solutions. On
                                                                                     DiffBases, GPT-4o uses triangular numbers on every run.
Task        Same+Sel   Same+Syn   Div+Sel   Div+Syn   Div contr.   Syn contr.
DiffBases      0.202      0.071     0.237     0.287     +0.126       −0.041
Erdős         0.031      0.071     0.568     0.497     +0.482       −0.016
                                                                                     Task        Strategy type             Claude    GPT-4o     Gemini
MolQED         0.314      0.377     0.307     0.437     +0.026       +0.097
                                                                                                 Trivial constant             0/10        5/5       5/5
                                                                                                 Binary/block pattern         4/10        0/5       0/5
                                                                                     Erdős
The per-task breakdown is essential context for the leave-                                       Smooth/cosine-based          2/10        0/5       0/5
one-out result (Section L). Erdős contributes +0.482 to                                         Mathematical reasoning       6/10        0/5       0/5
the diversity contrast, which is 2.5× larger than DiffBases                                      Sidon sets (B2 sets)         4/10        0/5       1/5
(+0.126) and 19× larger than MolQED (+0.026). Remov-                                             Triangular numbers           1/10        5/5       1/5
                                                                                     DiffBases
                                                                                                 Arithmetic progression       1/10        0/5       2/5
ing Erdős therefore drops the aggregate coefficient from
                                                                                                 Greedy/algorithmic           2/10        0/5       0/5
+0.188 to +0.014. The synthesis contrast is near zero or
slightly negative on all three tasks, confirming the null syn-
thesis finding is not an artifact of task selection.                                 On Erdős, GPT-4o and Gemini each produce a single stereo-
                                                                                     typed output across all seeds, contributing zero strategy vari-
                                                                                     ance to any diverse ensemble. A “three-backbone” team ef-
X. Cross-Synthesizer Replication                                                     fectively has one contributor. On DiffBases, GPT-4o is sim-
Table 20. Diversity coefficient under three synthesizer backbones.                   ilarly fixed (triangular numbers on 100% of runs), though
The coefficient remains positive and significant for all three syn-                  Gemini and Claude each use multiple strategies. The ef-
thesizers. The synthesis coefficient remains near zero regardless
                                                                                     fective diversity of an ensemble depends on whether each
of which model synthesizes.
                                                                                     backbone explores different regions of the solution space,
                                                                                     not merely on the number of distinct model families.
Synthesizer                        β̂div     95% CI
                                                                                     This has a direct consequence for the MIG results. When
Claude Sonnet 4              +0.234          [+0.106, +0.355]                        a diverse Debate or Cross-Chain team includes GPT-4o
GPT-4o                       +0.176          [+0.049, +0.303]                        on Erdős, one agent always proposes the same trivial con-
Gemini 2.5 Flash             +0.170          [+0.044, +0.298]                        stant (Q=0.710). Although this constant scores highest,
                                                                                     it contributes zero strategy variance, so the nominal three-
The diversity coefficient is stable across synthesizer choices.                      backbone team has effectively one non-trivial contributor.
All three synthesizer backbones produce a positive, signifi-                         The interaction step risks discarding Claude’s or Gemini’s
cant diversity coefficient. This rules out the possibility that                      structurally different solutions in favor of this single fixed
the null synthesis effect (Table 10) is an artifact of a partic-                     output, producing the regression visible in the per-task MIG
ular synthesizer being too weak or too strong to combine                             breakdown (Section P).
diverse proposals.




                                                                                10
                         The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

Z. Within-Model vs. Between-Model Variance                                 Table 24. MAgICoRe vs. Best-of-N on two optimization tasks,
                                                                           two backbones (n=15 each). The loss replicates on both tested
Table 22. Variance decomposition of single-shot Q-scores across            backbones, with large effect sizes.
                                                              2
three backbones (n=5 seeds each). Between-model variance (σB    )
measures how different the model means are. Within-model vari-             Task        Backbone     MAgICoRe      Best-of-N          d        p
        2
ance (σW   ) measures per-seed noise. A B/W ratio above 1 indi-
cates that models are more different from each other than from             Flat Poly   Gemini            2.087        1.899    +1.25      0.002
themselves, the prerequisite for backbone diversity to help. Two           Flat Poly   GPT-4o            2.951        2.251    +1.30      0.001
tasks clearly meet this criterion (B/W ≥ 2) and two are marginal           TSP-100     Gemini           53,351       50,786    +1.42      0.001
(B/W ≈ 1.2–1.3). LJ-n=41 and TSP-50 are omitted (LJ be-                    TSP-100     GPT-4o           53,529       50,128    +2.64     <0.001
cause all models score Q=0, TSP-50 for incomplete backbone
coverage).
                                                                           AC. Constraint Feasibility Gradient
                      2            2
Task                 σW           σB    B/W      Diversity useful?
                                                                           Within the Gemini backbone (n=15 each), constraint fea-
Circle Packing     0.017       0.253      15.2   Yes
MolQED             0.015       0.030       2.0   Yes                       sibility generally increases with configuration sophistica-
Flat Poly          0.054       0.070       1.3   Marginal                  tion. Critique-based configurations outperform evolutionary
Erdős             0.050       0.061       1.2   Marginal                  search on both tasks. Single-Shot outperforms Best-of-N on
TSP-100            0.020       0.010       0.5   No                        Knapsack (7% vs. 0%), breaking a strict monotonic gradient
MaxCut            0.0001     0.00002       0.3   No                        at the sampling end.
DiffBases          0.095       0.016       0.2   No                        Table 25. Constraint feasibility rates by configuration type (Gemini
                                                                           backbone, n=15). Critique outperforms evolution on both tasks.
Diversity adds information primarily on tasks where models
make structurally different errors (B/W ≥ 2). On tasks                     Task                   S-Shot     BoN        VGS      MAgICoRe
where within-model noise dominates (B/W < 1), adding a                     Knapsack-50               7%       0%        27%               47%
different backbone contributes no more than resampling the                 3AP-Free-100              0%       0%        13%               73%
same one. This is consistent with the interaction tax theory.
The tax only appears where there is genuine diversity to de-
stroy. Note that B/W measures separation of model means,                   AD. Constraint MIG: Same-Model vs. Diverse
while the 2×2 diversity contrast measures the gap between                      Backbones
the best draw from a diverse team and the best draw from
a same-model team. On DiffBases (B/W =0.2, diversity                       The interaction tax reverses on constraints with trivially
contrast +0.126), within-model noise is high, but Gemini’s                 checkable violations but persists when verification requires
mean (Q=0.610) far exceeds Claude’s (Q=0.209), so a di-                    reasoning. On Knapsack-50, where a weight violation is an
verse team’s best draw is still better even though individual              arithmetic check, diverse Debate achieves 10/10 feasibility
seeds are noisy.                                                           versus 2/10 for same-model. On 3AP-Free-100, where veri-
                                                                           fying a three-term arithmetic progression requires reasoning,
                                                                           diverse Debate drops to 0/10 versus 6/10 for same-model.
AA. Inter-Model Error Correlation                                          The pattern replicates across MAgICoRe.
Table 23. Spearman rank correlations of per-seed hidden scores be-
tween model pairs on four tasks with nonzero cross-model Q-score           Table 26. Constraint feasibility rates by backbone condition (n=10
variance. Low or negative ρ indicates uncorrelated errors (diver-          per cell). On Knapsack (trivially checkable), diverse backbones
sity helps). Positive ρ indicates correlated errors (diversity adds        help. On 3AP-Free (reasoning-required), diverse backbones hurt.
less). Gemini is constant on Erdős (all seeds produce Q=0.000),
precluding correlation.                                                    Task              Configuration       Same    Diverse     Direction
                                                                                             MAgICoRe            1/10       2/10     ≈
Task        Cl–GPT ρ     Cl–Gem ρ      GPT–Gem ρ    Error indep.           Knapsack-50
                                                                                             Debate              2/10      10/10     Div. helps
Erdős           +0.18    — (const)     — (const)   Yes                                      MAgICoRe            6/10         3/10   Div. hurts
DiffBases        +0.05       +0.12         +0.17    Yes                    3AP-Free-100
                                                                                             Debate              6/10         0/10   Div. hurts
MolQED           −0.45       −0.20         −0.33    Yes (anti-corr)
TSP-100          +0.38       +0.50         +0.41    No (correlated)

                                                                           AE. Formal Metric Definitions
AB. Cross-Backbone Replication
                                                                           Raw scores are normalized to Q(s) = (s − b)/(r − b),
The optimization loss pattern replicates on both tested back-              clipped to [0, 1], where b is the trivial baseline and r the best
bones (Gemini and GPT-4o).                                                 known result.




                                                                      11
                              The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

Marginal Epistemic Gain (MEG) measures whether a con-                                  AH. MAgICoRe Step-by-Step Trajectories
figuration beats the best single-agent baseline:                                       Table 29. Mean devScore at each MAgICoRe step (step 0 = initial
                                                                                       attempt, step 1 = after first critique, step 2 = after second critique),
         MEG(p, t) = Qhidden (p, t) − max Qhidden (c, t),                              averaged over n=15 seeds. Direction arrows indicate whether
                                               c∈C
                                                                                       lower (↓) or higher (↑) is better. ∗ Only 2/15 Erdős seeds reach
                                                                                       step 2.
where C = {Self-Refine, Best-of-N, VGS}.
                                                                                       Task        Dir   Step 0   Step 1   Step 2   Trend           Note
Marginal Interaction Gain (MIG) measures whether interac-
                                                                                       TSP-100     ↓     54,054   53,686   53,638   Slight impr.    Still below BoN
tion helps relative to the same agents running independently:                          Flat Poly   ↓      2.290    2.297    2.345   Degrading       Values, not struct.
                                                                                       Mol. QED    ↑      0.731   0.830     0.785   Peak revert     Step 1 lost
  MIG(p, t) = Qhidden (p, t) − Qhidden (parallel(A), t).                               Erdős      ↓      0.699    0.504      —∗    Conv. trivial   12/15 → 0.250



The 2×2 factorial uses N =120 runs total (ten per arm on                               On optimization tasks, critique frequently degrades solu-
each of the three tasks: Erdős, DiffBases, and MolQED).                               tions. Molecule QED peaks at step 1 (+13.5%) but reverts
                                                                                       at step 2. On Erdős, 12 of 15 seeds converge to the triv-
                                                                                       ial constant function at raw score 0.250 (Q=0.710). The
AF. Step-Level Solution Distance                                                       critic steers Gemini toward the simplest possible answer,
Table 27. Pairwise solution distance between consecutive steps                         which scores highest but is structurally degenerate. Flat
within each run, averaged over seeds. On Debate diverse, distance                      Poly shows no structural change across steps. These trajec-
drops sharply after agents exchange outputs (round 2→3), con-                          tories are the per-run manifestation of the 0/30 vs. 17/30
firming diversity collapse in real time. Metrics: Jaccard distance
for DiffBases (discrete sets), cosine distance for Erdős (continuous                  first-round regression rate in Section I.
arrays), Levenshtein distance for MolQED (SMILES strings).

Task          Configuration       Step 1→2     Step 2→3        Pattern
                                                                                       AI. Proposer Score Spread
              Debate (same)           0.950          0.891     Slight conv.            Table 30. Mean pairwise score spread among MoA proposers
DiffBases     Debate (diverse)        0.956         0.479      Collapse r3             within each run, measuring how different the proposals are before
              MAgICoRe (div.)         0.953          0.815     Convergence             synthesis. Diverse proposers produce 2.2× more score spread
              Debate (same)           0.500             —      Single change
                                                                                       than same-model proposers on Erdős. On DiffBases, within-model
Erdős        Cross-Chain             0.128          0.199     Low throughout          variance dominates, so backbone diversity adds less spread.
              MAgICoRe (div.)         0.448          0.293     Shrinking
              Debate (same)           0.571          0.412     Converging              Task              Diverse spread             Same spread              Ratio
MolQED
              Debate (diverse)        0.669         0.378      Fast conv.
                                                                                       Erdős                         0.448                   0.207          2.2×
                                                                                       MolQED                         0.222                   0.152          1.5×
AG. Per-Round Debate Scores                                                            DiffBases                       1500                    3045          0.5×
Table 28. Per-round visible scores for same-model and diverse
Debate on two tasks (lower is better for both, bold = best round).
Same-model Debate improves monotonically. Diverse Debate                               Diversity is real at proposal time. On Erdős, diverse propos-
reverses direction at round 3 after agents have exchanged their full                   als are 2.2× more spread out than same-model proposals,
outputs.                                                                               confirming that different backbones explore different re-
                                                                                       gions of the solution space. On DiffBases, within-model
Configuration          Task           Round 1        Round 2        Round 3            noise dominates (0.5×), consistent with the B/W ratio of
Debate (same)          DiffBases              436            132             66        0.2 in Section Z. Synthesis erases this diversity (Section N).
Debate (diverse)       DiffBases              889             72            274
Debate (same)          Erdős             4.61               1.24        0.62          AJ. Relation to Open-Ended Agent Systems
Debate (diverse)       Erdős             1.28               0.30        0.38
                                                                                       Open-ended platforms such as EinsteinArena (Bianchi et al.,
On both tasks, diverse Debate peaks at round 2 (when agents                            2025) show that multi-agent systems can produce real scien-
have exchanged critiques but not full solutions) and then                              tific results. These systems operate in a richer regime than
regresses at round 3 after full output exchange. Same-model                            our controlled benchmark, with many attempts over long
Debate improves monotonically because there is no struc-                               horizons, public verifiers, leaderboards, discussion, partial
tural diversity to destroy.                                                            results, and accumulated findings. Public descriptions of
                                                                                       EinsteinArena and agents such as JSAgent (Sung, 2026)
                                                                                       emphasize selective information channels, including scores,
                                                                                       notes, failure causes, and reusable findings, rather than only
                                                                                       short-horizon peer-to-peer exchange of complete candidate
                                                                                       solutions. Our controlled experiments suggest a possible

                                                                                  12
                       The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

mechanism consistent with such architectures. Selective                 diversity by always converging to that output. This is con-
information may let agents compound useful knowledge                    sistent with the null synthesis coefficient (Table 10). Across
without forcing every solver to condition on a complete peer            tasks, synthesis neither reliably helps nor reliably hurts.
solution early in generation.
                                                                        Example 4. Homogenization improves score (Debate di-
                                                                        verse, DiffBases, seed 1). Round 1 (devScore = 597). The
AK. Additional Transcript Examples                                      model reasons creatively about fractal-like structures for a
                                                                        difference basis set. Round 2 (devScore = 157). After see-
Examples 2–5 complement Example 1 in Section V. To-
                                                                        ing the first model’s approach, the agent shifts to a standard
gether they illustrate synthesis failure, synthesis success,
                                                                        triangular-number construction. Hidden score is 70.2. This
homogenization-as-improvement, and preserved diversity.
                                                                        is a positive example of interaction. The solution improved
Example 2. Synthesis selects a degenerate solution (MoA,                by replacing a creative but poorly executed approach with a
Erdős, seed 1). Three proposers generate independently                 conventional mathematical construction. But the improve-
(lower scores are better on Erdős). Claude produces a struc-           ment came from homogenization. The solution got better
tured binary-pattern function (devScore = 0.490, Q=0).                  by becoming less creative. This is exactly the mechanism
GPT-4o outputs a trivial uniform array of constant 0.005 val-           the diversity coefficient captures at aggregate. Interaction
ues (devScore = 0.250, Q=0.710). The synthesizer selects                rewards convergence toward standard approaches.
GPT-4o’s output, constructing a mathematical justification:
                                                                        Example 5. Independent generation preserves diversity
                                                                        (MoA-nosynth, Erdős, seed 1). Three proposers gener-
     “Agent 2 uses a uniform distribution with constant value
                                                                        ate independently (lower is better). Claude scores 2.47
     0.005 across all points. This achieves exactly the theo-
     retical lower bound of 1/4 for uniform distributions. . .          (structured sparse function). GPT-4o scores 0.34 (compact
     The uniform approach is mathematically optimal. . .                near-constant solution). Gemini scores 0.50 (different inter-
     Agent 2’s solution is superior as it achieves the lower            polation). The configuration picks the best (GPT-4o’s 0.34),
     bound with perfect consistency.”                                   which is better than any Claude-only attempt on the same
                                                                        seed (best of three is 0.392). The diverse ensemble finds a
The synthesizer correctly picked the higher-scoring proposal            solution Claude does not naturally produce. The gain is real,
(Q=0.710 vs. Q=0), though the mathematical reasoning it                 but only because the agents generated without seeing each
gives is wrong. The problem is the loss of strategy diversity.          other.
GPT-4o produces this identical trivial constant on every
seed (Table 21), so synthesis always converges to the same              AL. Protocol Implementation Details
degenerate output regardless of what Claude or Gemini
propose. Diversity existed at proposal time but was erased              All ten configurations share the budget vector
at synthesis.                                                           (T =200K tokens, W =600s, C=30s, K=25) and the
                                                                        same task prompt. The selection rule is: the artifact
Example 3. Synthesis selects the right proposal (MoA,
                                                                        with the best dev score under the task’s score direc-
MolQED, seed 1). Three proposers produce structurally
                                                                        tion is submitted for hidden evaluation. Below we
distinct molecules (higher scores are better on MolQED).
                                                                        summarize implementation details from the release
Claude produces a methoxybenzene-pyrimidine scaffold
                                                                        artifact.  Full source code is available at https:
(devScore = 0.828). GPT-4o produces an aspirin deriva-
                                                                        //github.com/SummerAnn/interaction-tax.
tive (devScore = 0.685). Gemini produces a small acetyl
amino acid (devScore = 0.547). The synthesizer identi-                  Backbone models.        All models are ac-
fies Claude’s molecule as containing “a methoxybenzene                  cessed via OpenRouter:     Claude Sonnet 4
ring (drug-like aromatic system) and a pyrimidine ring with             (anthropic/claude-sonnet-4),            GPT-
amino groups (common in pharmaceuticals)” and correctly                 4o    (openai/gpt-4o),   Gemini   2.5   Flash
selects it. Here the quality gap is large (0.83 ≫ 0.55) and             (google/gemini-2.5-flash).     Model IDs are
the solution format is chemically interpretable. Synthesis              pinned in the codebase.
works when the best proposal’s advantage is obvious.
                                                                        Best-of-N . Eight independent calls at temperatures
Pattern. On Erdős, the synthesizer correctly selects the               0.60, 0.65, . . . , 0.95. Temperature variation introduces sam-
highest-scoring proposal, but that proposal is a structurally           ple diversity without changing the prompt.
degenerate constant that GPT-4o produces on every seed.
                                                                        VGS. FunSearch-style evolutionary loop. Initial population
On MolQED, the synthesizer also selects the best proposal,
                                                                        of four at varied temperature. Five generations, top-two
but here all three proposals are structurally distinct. The dif-
                                                                        elites retained, two new candidates per generation via mu-
ference is whether diversity survives. When one backbone
dominates on score with a fixed output, synthesis erases

                                                                   13
                     The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

tation call. Early termination if no improvement for two
                                                                      Synthesize the best solution. Output ONLY JSON.
consecutive generations.
MAgICoRe roles. Solver generates (SINGLE_SHOT                         Debate synthesizer prompt.
prompt). Reviewer critiques without producing code (“What
                                                                      System: You are a neutral Synthesizer. Two agents
are the weaknesses? Be concrete and technical.”). Refiner             debated this problem. Combine the best ideas from
receives critique and produces improved solution. Two                 both into an optimal solution. Return ONLY valid
                                                                      JSON.
rounds.
                                                                      User: # Problem
Debate. Debater A uses exploratory strategy (temperature              [PROBLEM]
0.9): “Take an EXPLORATORY approach — try unconven-
                                                                      # Schema
tional strategies.” Debater B uses rigorous strategy (tem-            [SCHEMA]
perature 0.5): “Take a RIGOROUS approach — use well-
                                                                      # Debater A (score: [SCORE_A])
established methods.” Two critique rounds, then a neutral             [POSITION_A]
synthesizer merges.
                                                                      # Debater B (score: [SCORE_B])
                                                                      [POSITION_B]
MoA. Three proposers generate independently with no
shared context. Aggregator receives all three proposals with          Synthesize the best solution. Output ONLY JSON.
dev scores and produces synthesized output. The aggregator
prompt includes: “Multiple agents independently solved                MAgICoRe reviewer prompt.
this problem. Synthesize their best ideas into a superior
                                                                      System: You are a REVIEWER. Analyze the solution
solution.”                                                            below and provide specific, actionable critique.
                                                                      What are the weaknesses? What strategies could
HPE. A planner decomposes the problem into sub-foci                   improve the score? Be concrete and technical.
for parallel executors. Each executor works only on its               User: # Problem
assigned focus and produces a partial contribution (free-             [PROBLEM]
form text, not a complete solution). An integrator assembles          # Current Solution (score: [SCORE], goal: [DIR])
the contributions into one schema-valid solution. Multiple            [SOLUTION]
rounds give the planner score feedback.                               Provide your critique.
Retry behavior. All protocols share a common retry mech-
anism. If the LLM produces malformed JSON or a verifier-              HPE planner prompt.
rejected solution, the error message is appended to the next          System: You are a PLANNER. Decompose this problem
call. Generation steps allow up to 5 retries; refinement steps        into focused sub-tasks for [N] executor agents
                                                                      working in parallel. Each executor works ONLY on
allow up to 2 to conserve budget. A cell that exhausts retries        its assigned sub-focus, then a separate integrator
at the first generation step is excluded from analysis.               will combine the contributions into one final
                                                                      solution.
Budget enforcement. A shared BudgetEnforcer tracks cu-
                                                                      Return ONLY valid JSON:
mulative token usage, wall clock time, and evaluator call             {"strategy": "one-sentence plan",
count. Any call exceeding a cap is silently dropped and the            "subtasks": [{"id": 1, "focus": "..."},
                                                                                    {"id": 2, "focus": "..."}, ...]}
protocol terminates early.
                                                                      Make the foci genuinely complementary -- they should
                                                                      NOT all attempt the whole problem.
AM. Extended Prompt Templates
                                                                      All ten protocol prompt sets (including VGS mutation, Self-
Section U shows two representative prompts. Here we in-               Refine iteration, Homo-Chain refinement, Cross-Chain re-
clude additional templates verbatim from the release artifact.        finement, HPE executor, and HPE integrator) are committed
MoA aggregator prompt.                                                verbatim in the artifact at src/config/prompts.ts.

System: You are an Aggregator. Multiple agents
independently solved this problem. Synthesize their
best ideas into a superior solution. Return ONLY
valid JSON.

User: # Problem
[PROBLEM]

# Schema
[SCHEMA]

# Agent Solutions
[CANDIDATES with dev scores]



                                                                 14
