                                           Understanding Tool-Augmented Agents for Lean Formalization: A Factorial
                                                                         Analysis


                                                                      Ke Zhang 1 Patricio Gallardo 1 Maziar Raissi 1 Sudhir Murthy 1


                                                                     Abstract                               datasets (Gao et al., 2025; Wang et al., 2025). Although
                                                                                                            these methods can generate plausible code, they face sev-
                                              Automatic translation of natural language math-
                                                                                                            eral fundamental obstacles. Training data for graduate-level
arXiv:2604.16538v1 [cs.SE] 16 Apr 2026




                                              ematics into faithful Lean 4 code is hindered by
                                                                                                            mathematics is sparse, causing models to hallucinate nonex-
                                              the fundamental dissonance between informal set-
                                                                                                            istent theorems and symbols. Even when the mathematics is
                                              theoretic intuition and strict formal type theory.
                                                                                                            correct, a deep mismatch remains between the set-theoretic
                                              This gap often causes LLMs to hallucinate non-
                                                                                                            language of textbooks and Lean’s dependent type theory,
                                              existent library definitions, resulting in code that
                                                                                                            making direct translation unreliable. Moreover, syntactic
                                              fails to compile or lacks semantic fidelity. In
                                                                                                            validity does not ensure semantic fidelity: Lean code may
                                              this work, we investigate the effectiveness of tool-
                                                                                                            compile yet express a vacuous or incorrect statement. These
                                              augmented agents for this task through a system-
                                                                                                            issues are further compounded by the fact that Mathlib 4 is
                                              atic factorial analysis of three distinct tool cate-
                                                                                                            a fast-evolving, community-maintained library, so models
                                              gories: Fine-tuned Model Querying (accessing
                                                                                                            trained on static snapshots frequently generate code that
                                              expert drafts), Knowledge Search (retrieving sym-
                                                                                                            targets deprecated or nonexistent definitions in the current
                                              bol definitions), and Compiler Feedback (verify-
                                                                                                            environment.
                                              ing code via a Lean REPL). We first benchmark
                                              the agent against one-shot baselines, demonstrat-             To address these limitations, we introduce an agentic frame-
                                              ing large gains in both compilation success and               work that replaces static generation with iterative refinement.
                                              semantic equivalence. We then use the factorial               A generalist LLM orchestrator interacts with three tool cate-
                                              decomposition to quantify the impact of each cat-             gories—symbol retrieval, expert drafting, and Lean REPL
                                              egory, isolating the marginal contribution of each            feedback—forming a closed loop of draft, verify, and re-
                                              tool type to overall performance.                             pair that corrects both syntactic and semantic errors. Rather
                                                                                                            than treating this toolset as a black box, we apply a full
                                                                                                            factorial design on a new benchmark of 400 graduate-level
                                         1. Introduction                                                    theorems to quantify the causal contribution and interaction
                                                                                                            of each component. This allows us to identify which tools
                                         Large language models (LLMs) have demonstrated remark-             create new capability regimes and which merely stabilize or
                                         able capability in producing complex mathematical argu-            accelerate convergence toward faithful formalizations.
                                         ments (Castelvecchi, 2025), yet their probabilistic nature
                                         fundamentally conflicts with the absolute certainty required       Finally, to support reproducibility, we will open-source our
                                         by formal mathematics. Proof assistants such as Lean               entire research framework, including the full benchmark,
                                         4 (de Moura & Ullrich, 2021) resolve this conflict by me-          agent implementation, evaluation scripts, and agent tool
                                         chanically verifying logical correctness, but they introduce       calling logs upon acceptance.
                                         a significant barrier: the ”formalization bottleneck.” Most
                                         modern undergraduate and graduate-level theorems exist             2. Problem Setting
                                         only in natural language and have not yet been translated
                                         into the strict syntax required by proof assistants (Lean          We address the task of formalization: automatically trans-
                                         Prover Community).                                                 lating natural-language mathematical statements into valid
                                                                                                            Lean 4 theorem declarations. This task serves as the critical
                                         Current attempts to automate translation into Lean 4 rely          first step in verifying mathematics, bridging the gap between
                                         primarily on one-shot prompting or fine-tuning on static           informal human intent and machine-checkable syntax.
                                           1
                                             University of California, Riverside. Correspondence to:
                                         Maziar Raissi <maziar.raissi@ucr.edu>.

                                         Preprint. April 21, 2026.

                                                                                                        1
                                       Tool-Augmented Agents for Lean Formalization

           Table 1. Benchmark Dataset Composition.

Domain              Source Material                       N
Real Analysis       Basic Analysis (Lebl) (Lebl, 2025a)   100
Complex Analysis    Cultivating Complex Analysis          100
                    (Lebl) (Lebl, 2025b)
Topology            Notes on Topology                     100
                    (McKay) (McKay, 2025)
Algebra             Abstract Algebra (Doty) (Doty,        100
                    2025)
Total                                                     400



2.1. Task Definition
Formally, let X be the space of informal mathematical state-
ments and Y be the space of valid Lean 4 source code.
Given an input x ∈ X , the system must generate a formal
statement y ∈ Y that satisfies three criteria: it must pos-
sess syntactic validity (compile in Lean 4 with Mathlib),
maintain statement-centricity (omitting proofs via := by
sorry), and ensure semantic faithfulness (logical equiva-
lence to x).                                                         Figure 1. Agent Orchestration Logic. The architecture consists
                                                                     of a central LLM orchestrator (left) and a Lean 4 execution envi-
2.2. Dataset Construction                                            ronment (right).

To benchmark this task, we curated a dataset of 400
graduate-level theorems derived from open-source LaTeX               the evaluation with statement-level meaning.
lecture notes and textbooks. We selected sources that pro-
vide natural language statements without accompanying                Success Metric: We define a generated translation y for an
formal code, ensuring the task represents a genuine transla-         input statement x as Faithful if and only if:
tion effort rather than retrieval.                                   Compiles(y) = True        AND     EquivalentScore(x, y) ≥ 9
As detailed in Table 1, we balanced the dataset across four
major mathematical domains—Real Analysis, Complex                    3. Methodology
Analysis, Topology, and Algebra—selecting 100 diverse
                                                                     The agent architecture, illustrated in Figure 1, is structured
examples from each to ensure broad coverage of mathemati-
                                                                     as a for-loop. The core component is a central LLM orches-
cal terminology and structures.
                                                                     trator (GPT 5.2) that interacts with the Lean 4 environment
                                                                     via a defined API. Unlike static prompting, this architecture
2.3. Evaluation Protocol                                             allows the model to maintain a persistent state, observing
To evaluate the quality of the generated formalizations, we          the consequences of its actions—such as compiler errors
adopt a rigorous two-stage protocol. First, we apply a Com-          or retrieval results—before deciding on the next step. This
piler Verification filter; any code that fails to compile is         design effectively decouples the LLM reasoning from the
immediately assigned a score of 0. Second, for compiling             Lean Compiler verification.
code, we employ an LLM-as-a-Judge (GPT-5.2 Medium
Thinking mode) to assess semantic equivalence. The eval-             3.1. Tool Definitions
uator compares the generated Lean statement against the
                                                                     We equip the agent with tools designed to bridge the gap
original natural language input and assigns a faithfulness
                                                                     between informal mathematical reasoning and formal Lean
score on a scale of 0–10. Because all reported results de-
                                                                     4 syntax:
pend on this judge, we explicitly validate its reliability via
cross-judge agreement with an independent model in (Sec-
                                                                        • Mathlib Retrieval:         Retrieval tools such as
tion 4.5).
                                                                          lean inspect name allow the agent to ask
The judge prompt and rubric (Appendix B) were reviewed                    Lean “what is this symbol?”, returning its real type
and adjusted by a Lean 4–experienced researcher to align                  and definition directly from Mathlib.

                                                                 2
                                        Tool-Augmented Agents for Lean Formalization

   • Expert Drafting: The lean4 translator tool re-                  3.3. Execution Loop
     quests a translation from the fine-tuned model Herald,
                                                                     Finally, we formalize the interaction between these compo-
     providing a specialized starting point.
                                                                     nents as a discrete control loop, shown in Algorithm 1. At
                                                                     each step t, the agent receives the current message history
   • Compiler Feedback: The lean repl runner tool                    (including the modular prompt and any tool outputs) and
     exposes the Lean 4 compiler interface. This provides            produces either a tool call or a final response. This process
     precise error messages, enabling the agent to iteratively       repeats until the Lean compiler reports success or the step
     diagnose and correct syntax or validity issues.                 budget Tmax is exhausted.

Detailed specifications of the tool definitions and signatures       Algorithm 1 Agentic Controller for Lean Formalization
are provided in Appendix A.                                           1: Input: Statement x, Context p, ToolSet T
                                                                      2: H ← [SystemPrompt, UserMsg(x, p, τ )]
3.2. Prompt Composition                                               3: for t = 1 to Tmax do
                                                                      4:     M sg ← LLM(H)
To ensure rigorous evaluation, we employ a modular prompt-            5:     H.append(M sg)
ing architecture. The system context is dynamically assem-            6:     if M sg calls T OOL(name, args) then
bled from three independent components, ensuring that the             7:         Result ← ExecuteTool(name, args)
core task definition remains constant while we vary the               8:         H.append(ToolOutput, Result)
available tools:                                                      9:     else if M sg declares S UCCESS then
                                                                     10:         return S UCCESS        ▷ Compilation Verified
   • Role Definition: Instructs the agent to act strictly as         11:     end if
     a translator, not a prover. The objective is to produce         12: end for
     a type-correct theorem statement ending in := by                13: return FAILURE
     sorry, ignoring proof generation.

                                                                     4. Performance Evaluation
   • General Guidelines: Enforces validity standards, such
     as requiring import Mathlib and strictly prohibit-              To quantify the ”agentic premium” of our framework, we
     ing the invention of new definitions or axioms to pre-          benchmark the full agent against two static baselines: One-
     vent ”hallucinated” success.                                    Shot Base (standard GPT-5.2 and Gemini-2.5-Pro prompt-
                                                                     ing without tools) and a One-Shot Fine-Tuned model (Her-
   • Tool Specifications: Contains the functional defini-            ald), which represents the limit of parametric knowledge
     tions for the active toolset. We alter the configuration        without execution feedback.
     by simply including or excluding tools from this block,
     without modifying the instructions above.                       4.1. Performance Analysis
                                                                     Figure 2 presents performance on the 400-theorem bench-
A common failure mode in agent evaluation is mixing up               mark. One-shot generation without tools proves inade-
tool effects with prompt tweaks. If we rewrote the instruc-          quate: Herald and GPT-5.2 achieve compilation rates of
tions for each tool configuration, any performance difference        only 26.0% and 26.2%, respectively. Faithfulness is even
could come from better prompt wording rather than the tools          lower, ranging from 10.8% (Herald) to 28.0% (Gemini-2.5-
themselves.                                                          Pro). In contrast, the full tool-augmented agent framework
                                                                     (Tmax = 24) boosts compilation to 89.5% and faithfulness
To rule this out, we keep the role definition and general            to 60.5%, confirming the value of iterative refinement.
guidelines exactly the same in every experiment. The only
thing that changes across configurations is the tool interface
                                                                     4.2. Efficiency Analysis
block (which tools are declared and how they are described).
This makes the factorial ablation in Section 5 cleaner: dif-         Beyond raw accuracy, and to provide insight into the bal-
ferences in performance can be attributed to the presence or         ance between cost and performance, we analyze the compu-
absence of components such as compiler feedback or expert            tational budget required to achieve these results. Figure 3
drafting, rather than to changes in the core instructions.           plots the cumulative success rate against the step budget (T ),
                                                                     illustrating the trade-off between performance and cost.
The full prompt templates, including the shared base prompt
and all configuration-specific tool-availability blocks, are         The plot reveals two distinct phases in the agent’s behav-
provided in Appendix A.                                              ior. We observe rapid convergence up to T = 8, where

                                                                 3
                                                                                         Tool-Augmented Agents for Lean Formalization

                                  100                                                                                                                           Domain-level computational overhead (config=111)
                                                                                                                                        10       Mean steps                                         9.83                      9.84
                                             Compiles (Syntax Correct)                              89.5%                                        Median steps            9.20
                                             Faithful (Correct)
                                  80                                                                                                     8                                                                                              7.50
                                                                                                                                                  6.88
                                                                                                                                                                                                              6.50
                                                                                                                                         6                                          6.00
                                                                                                            60.5%




                                                                                                                                Steps
               Success Rate (%)




                                  60                                                                                                                        5.00

                                                                                                                                         4

                                  40                                                                                                     2
                                                                                 31.0%
                                          26.0%               26.2%                      28.0%
                                                                         19.8%                                                           0                                      y
                                                                                                                                                      sis                     g                     Algebra                   nalysis
                                  20                                                                                                          x Analy                   Topolo                                       Real A
                                                  10.8%                                                                                 Comple
                                                                                                                                                                                           Domain

                                      0                                                                                          Figure 4. Domain-level difficulty (config=111). Mean and median
                                            Herald               GPT-5.2         Gemini 2.5 Pro         Agent
                                                                                                  (Full Framework)               agent steps by domain.

  Figure 2. Main Results. The full framework (all tools enabled;
  Tmax = 24) achieves substantially higher compilation and faith-                                                                4.4. Model Generalizability
  fulness than one-shot baselines on N = 400 theorems.
                                                                                                                                 To verify that the framework’s gains are not specific
                                                                                                                                 to the GPT-5.2 orchestrator, we evaluate two additional
                                          Efficiency Analysis: Success Rate vs. Step Budget                                      orchestrators—Claude Sonnet 4.5 and Gemini-2.5-Pro—on
                                                                                                                                 the full benchmark under the 111 configuration. All three
                            60
                                                                                                                                 converge to 60–65% consensus faithful despite different one-
Faithful Success Rate (%)




                            50                                                                                                   shot baselines (19–28%), confirming that the dominance of
                                                                                                                                 compiler feedback is structural rather than model-specific.
                            40                                                                                                   Full results are in Appendix C.5.
                            30
                                                                                                                                 4.5. Robustness and Metric Validation
                            20
                                                                                                                                 To validate our LLM-based semantic evaluation, we cross-
                            10                                                              Agent (Cumulative)                   check the primary judge (GPT-5.2) against another judge
                                                                                            GPT-5.2 Baseline (20.3%)             (Gemini-2.5-Pro). The two judges exhibit a consistent con-
                            0
                                  2          5                   10                 15                20               24
                                                                      Step Budget (T)                                            tainment relationship, indicating a structured difference in
                                                                                                                                 strictness rather than random disagreement.
  Figure 3. Formalization Efficiency. Cumulative faithfulness rate
  as a function of the inference step budget (T ).
                                                                                                                                 Judge Containment. Table 2 reports, for each system,
                                                                                                                                 the number of translations judged Faithful by each judge.
                                                                                                                                 Across all systems, Gemini-2.5-pro consistently accepts
    nearly half the benchmark is resolved. While returns dimin-                                                                  more outputs than GPT-5.2, while the consensus is a subset
    ish thereafter, significant gains persist until T = 14. We                                                                   of both. This yields a near-perfect containment pattern
    therefore identify T ≈ 14 as the practical saturation point,
                                                                                                                                                         PassConsensus ⊆ PassGPT ⊆ PassGemini :
    capturing the bulk of solvable problems before computa-
    tional costs outweigh improvements.                                                                                          across all ten configurations, at most 6 out of 400 transla-
                                                                                                                                 tions are labeled Faithful by GPT-5.2 but not by Gemini,
    4.3. Domain-Specific Analysis                                                                                                indicating that Gemini-2.5-Pro is systematically more per-
                                                                                                                                 missive, while GPT-5.2 provides a more conservative se-
    Figure 4 reports domain-level computational overhead under
                                                                                                                                 mantic filter. The inclusion relation for the consensus-rate
    full agent framework, measured by mean and median agent
                                                                                                                                 definition is shown in Figure 5.
    steps (N=100 per domain). Complex Analysis requires the
    fewest iterations (6.88 mean steps; median 5.0), indicating
    the lowest computational overhead among the four domains.                                                                    Conservatism of the Primary Metric. We quantify agree-
    Real Analysis is the most expensive (9.84 mean steps; me-                                                                    ment using the consensus rate, defined as the fraction of
    dian 7.5), with Algebra close behind (9.83 mean; median                                                                      GPT-5.2-labeled Faithful translations that are also labeled
    6.5). Topology exhibits intermediate overhead (9.20 mean;                                                                    Faithful by Gemini:
    median 6.0). Appendix C.1 and Appendix C.2 provides the                                                                                                                                    #PassConsensus
    corresponding per-domain summary tables.                                                                                                                ConsensusRate :=                                  .
                                                                                                                                                                                                #PassGPT

                                                                                                                            4
                                            Tool-Augmented Agents for Lean Formalization

Table 2. Comparison of LLM judges and their consensus. En-
tries count translations that compile and are judged Faithful by                                140
                                                                                                      GPT Gemini Disagreement by Domain
each judge; Consensus counts those labeled Faithful by both.                                                                      125
                                                                                                120




                                                                          Total Disagreements
     System             Gemini     GPT-5.2       Consensus                                      100
                                                                                                         82
     One-shot baselines                                                                          80
     Herald              52            43            43                                                               61                       58
     GPT-5.2             90            81            79                                          60
     Sonnet 4.5         145           116           114
     Gemini-2.5-Pro     122           112           112                                          40
     Tool-augmented agents (GPT-5.2 orchestrator)                                                20
     Config 100         112         98            98                                              0
                                                                                                       Algebr
                                                                                                              a                  is        is       y
                                                                                                                          AnalyRseal Analys Topolog
     Config 001         160        134           132
     Config 101         174        146           144                                                               p l ex
     Config 110         282        241           235                                                           Com
     Config 111         291        248           242
     Config 010         304        250           245                   Figure 6. GPT–Gemini disagreement by mathematical domain.
     Config 011         291        251           248                   Total number of GPT–Gemini disagreements aggregated across all
                                                                       ten experimental systems.
     Tool-augmented agents (alt. orchestrators, config 111)
     Sonnet 4.5         315          271           262
     Gemini-2.5-Pro     307          263           262


                                                                       sis (61), and Topology (58). This structured concentration
                                                                       suggests that judge disagreements are systematically asso-
                                                                       ciated with particular mathematical domains. This pattern
                                                                       aligns with our domain difficulty results: under the full
                                                                       agent setting (config=111), Real Analysis exhibits the low-
                                                                       est Faithful rate among the four domains (Appendix C, Ta-
                                                                       ble 6), suggesting that harder domains leave more borderline
                                                                       cases for judges to interpret.



      Figure 5. Inclusion relation for faithfulness labels.
                                                                       Human Expert Validation. To directly validate the LLM-
                                                                       as-Judge metric, a Lean 4 expert independently reviewed
Across all baselines and tool-augmented agents, the consen-            138 translations that the consensus metric classified as Faith-
sus rate exceeds 97% in every case, with an overall average            ful, scoring each on the same 0–10 rubric. Of 138 scored
of 98.7%. For example, on the full system (111), GPT-                  translations, 83.3% (115/138) received exactly matching
5.2 labeled 248 translations as Faithful, of which Gemini              scores between the human and LLM judges. A further
also labeled 242 as Faithful (97.6%). Together with the                14.5% (20/138) disagreed by ±1 within the faithful range
containment pattern above, this supports using the strict              (scores of 9 vs. 10), leaving only 3 out of 138 (2.2%) where
GPT∩Gemini consensus as the primary faithfulness metric                the human score crossed below the faithful threshold (≥9)—
throughout the paper (Section 2), providing a conservative             all cases where the LLM overestimated (LLM scored 10,
lower bound on semantic faithfulness.                                  human scored 5–7). This yields 97.8% binary agreement
                                                                       on the faithful/unfaithful classification, confirming that the
Where do judges disagree? Figure 6 breaks down GPT–                    automated metric is well-calibrated with a slight positive
Gemini disagreements by mathematical domain, aggregated                bias.
across all ten experimental systems (three one-shot baselines
                                                                       We note two limitations of this audit: (1) it covers only
and seven tool-augmented agents). Each domain contains
                                                                       outputs classified as faithful (score ≥9), so it measures pre-
100 problems evaluated under 10 systems, so each bar sum-
                                                                       cision but not recall; and (2) the expert was not blinded to
marizes 1,000 judged translations.
                                                                       the LLM scores. However, the expert did not uniformly con-
Although overall agreement is high (Section 4.5), the re-              firm the LLM labels—in 3 of 138 cases, substantially lower
maining disagreements are not uniformly distributed across             scores were assigned—suggesting independent judgment
domains. Real Analysis accounts for the largest number of              rather than mechanical agreement. A broader audit covering
conflicts (125), followed by Algebra (82), Complex Analy-              the full score distribution is left to future work.

                                                                   5
                                        Tool-Augmented Agents for Lean Formalization

Table 3. Factorial analysis results. Performance across all 23       Table 4. Factorial main effects on Faithful accuracy. Each effect
configurations (N = 400), grouped by the presence of the REPL        is computed by Eq. 1. 95% confidence intervals are obtained via
feedback tool (F). We use 0 to denote that tool is turned off.       bootstrap resampling (B = 10,000).

     Config        Performance                 Gain                    Factor             X=1       X=0       Effect       95% CI
 T     F S     Comp. (%) Faith. (%)     ∆Faith. (pts) vs . 000
                                                                       Feedback (F)        60.6      28.3      +32.3     [28.7, 35.9]
 Regime 1: F = 0 (Agent with no REPL)                                  Search (S)          47.9      41.1      +6.8       [3.6, 10.0]
 0     0   0      26.25       19.75              –                     Translation (T)     44.9      44.0      +0.9      [−2.1, 4.0]
 1     0   0      30.25       24.50            +4.75
 0     0   1      45.50       33.00            +13.25
 1     0   1      50.00       36.00            +16.25
                                                                     Main-Effect Definition. Let Y (T, F, S) denote the Faith-
 Regime 2: F = 1 (Agent with REPL)                                   ful accuracy for configuration (T, F, S) in Table 3. For any
 1     1   0      93.50       58.75            +39.00                factor X ∈ {T, F, S}, its factorial main effect is
 1     1   1      89.50       60.50            +40.75
 0     1   0      91.50       61.25            +41.50
 0     1   1      87.25       62.00            +42.25                        Effect(X) = E[ Y | X=1 ] − E[ Y | X=0 ],             (1)

                                                                     where the expectation averages uniformly over all settings
5. Factorial Analysis                                                of the other two factors. Table 4 reports the resulting main
                                                                     effects.
While the superior performance of the agent is evident, the
“black box” nature of the full system obscures which com-               • Feedback is the capability bottleneck (+32.3 pts):
ponents drive this success. To disentangle these factors, we              Enabling the REPL transforms the agent from a low-
conduct a systematic factorial analysis to quantify why the               success regime (19.75–36.00%) into a high-success
agent succeeds.                                                           regime (58.75–62.00%). This shows that iterative
                                                                          compiler-guided repair is the dominant mechanism
5.1. Experimental Design: Factorial Ablation                              enabling faithful Lean formalization. Notably, the mag-
To systematically isolate the contribution of each compo-                 nitude of this effect varies by domain, with Complex
nent, we decompose the agent arsenal into three tool factors:             Analysis benefiting most (+53 pts) and Algebra/Topol-
                                                                          ogy least (+20 pts); see Appendix C.3 for details.
     • T (Translation expert). Access to the fine-tuned Her-            • Search is a stabilizer (+6.8 pts): Symbol-level re-
       ald (7B) model for translation.                                    trieval via #check/#print provides a consistent
                                                                          boost by reducing hallucinations and improving name
     • F (Feedback). Access to the Lean compiler feedback                 resolution, even though it does not create a new per-
       loop (REPL) for error correction and compile status.               formance regime on its own. Domain-level analysis
                                                                          (Appendix C.4) shows that Search yields +12.4 pts
     • S (Search). Symbol-retrieval tools (retrieval/web                  when full REPL is absent, but near-zero gain (+1.2 pts)
       search) for resolving unknown definitions.                         when Feedback is enabled—consistent with the neg-
                                                                          ative F ×S interaction (Section 5.3), as full compiler
We adopt a full 23 factorial design to evaluate interaction               diagnostics subsume symbol-level queries.
effects. We explicitly map the empty-set configuration (∅) to
the One-Shot Baseline established in Section 4, as an agen-             • Drafting is largely substitutable (+0.9 pts): The
tic loop with zero tools conceptually reduces to standard                 specialized Herald model yields only a small average
autoregressive generation. The remaining seven configura-                 improvement. Because the orchestrator (GPT-5.2) is
tions are evaluated by selectively toggling tool definitions              already strong, external drafting becomes redundant
in the system prompt.                                                     once feedback and search are available, and in some
                                                                          cases slightly interferes with the repair loop.
5.2. Results and Interpretation
                                                                     5.3. Interaction Effects: Capability vs. Efficiency
Table 3 reports performance across all configurations,
grouped by the presence of Compiler Feedback (F). To quan-           Main effects summarize average marginal gains, but they
tify the contribution of each factor, we compute standard            can hide strong regime dependence. To expose when tools
factorial main and interaction effects, defined as differences       improve final faithfulness versus primarily efficiency, we
in mean response between the high and low levels of a factor         compute simple effects conditioned on the presence of com-
(averaged over the other factors).                                   piler feedback F .

                                                                 6
                                        Tool-Augmented Agents for Lean Formalization

When does Search improve final faithfulness? Define                   Table 5. Tool Usage Counts (Total). Cumulative tool invoca-
                                                                      tions across the subset with complete tool-call logs (N = 384;
the Search simple effect at fixed feedback level F =f as              all accuracy results use N = 400). We report REPL calls
                                                                      (lean4 repl runner) and aggregate symbol-retrieval tools
  ∆S (F =f ) = E[Y | S=1, F =f ] − E[Y | S=0, F =f ],                 into Stotal = search online + lean inspect name +
                                                                      lean resolve name.
where the expectation averages uniformly over T . From
Table 3, Search yields a large gain without REPL feedback,              (T, F, S)   Trans.   REPL      Stotal   Notes
∆S (F =0) = +12.4 points, but only a marginal gain with
                                                                         (0,1,0)         0     1496       0     Feedback-only
REPL feedback, ∆S (F =1) = +1.2 points. Thus, Search                     (0,1,1)         0     1050    1726     +Search (REPL↓)
meaningfully improves faithfulness in the low-capability
regime (F = 0), but in the high-capability regime (F = 1)                (1,1,0)       257     1374       0     Feedback + Expert
                                                                         (1,1,1)       112     1008    1913     +Search (REPL↓)
it mainly shifts how the agent acquires information—from
repeated compile–repair iterations toward earlier, targeted
symbol queries—consistent with the reduced REPL-call
counts in Table 5.                                                    enables strong cross-domain transfer, which—when com-
                                                                      bined with compiler feedback and retrieval—allows the
When does drafting hurt? Similarly, define the Transla-               generalist model to adapt to Lean syntax and semantics
tor simple effect                                                     through iterative correction, reducing the marginal value of
                                                                      a domain-specialized draft.
 ∆T (F =f ) = E[Y | T =1, F =f ] − E[Y | T =0, F =f ],
                                                                      The value of verification beyond retrieval. Search pro-
averaging over S. Drafting helps when feedback is absent
                                                                      vides symbol-level semantic primitives (existence checks,
(∆T (F =0) = +3.9 points) but hurts when feedback is
                                                                      types, and definitions via #check/#print), but it does
present (∆T (F =1) = −2.0 points). This “drafting penalty”
                                                                      not provide whole-statement verification or full elaboration
suggests that, once compiler-guided repair is available, spe-
                                                                      diagnostics. In contrast, Feedback adds (i) a global compi-
cialist drafts may become redundant or introduce anchoring
                                                                      lation/elaboration signal and (ii) actionable error messages
effects that impede convergence to the most faithful formu-
                                                                      that enable iterative repair, which appear to be the dominant
lation.
                                                                      drivers of faithful formalization.
Substitution captured by interactions. The regime de-
                                                                      5.4. Behavioral Analysis: REPL Efficiency
pendence above appears as negative interaction terms under
the standard difference-in-differences definition (averag-            While the factorial analysis in Section 5.2 identifies which
ing over the remaining factor): F ×S = −11.1 points and               tools determine final Faithful accuracy, tool invocation logs
F ×T = −5.9 points, while S×T ≈ 0. In our implementa-                 provide complementary insight into how efficiently the agent
tion, both F (whole-program compilation) and S (targeted              reaches that accuracy. In particular, the number of calls
symbol queries) are backed by the same installed Lean/-               to the Lean REPL (lean4 repl runner) serves as a
Mathlib snapshot; in particular, S is realized via Lean-level         proxy for the amount of trial-and-error required to obtain
checks such as #check/#print rather than an indepen-                  compilable and faithful Lean code.
dent external knowledge source. Under this setup, the nega-
                                                                      As shown in Table 5, using the convention (T, F, S), adding
tive interactions are consistent with overlapping functional-
                                                                      Search reduces REPL usage in both T = 0 and T = 1
ity between whole-program diagnostics and symbol-level
                                                                      settings when feedback is enabled. For T = 0, REPL
lookup: when REPL feedback is enabled, enabling Search
                                                                      calls drop from 1,496 in (010) to 1,050 in (011), a 29.8%
is associated with only small changes in final faithfulness,
                                                                      reduction. For T = 1, REPL calls drop from 1,374 in
while shifting some information gathering from compiler-
                                                                      (110) to 1,008 in (111), a 26.6% reduction. Meanwhile,
error-driven trial-and-error toward earlier identifier and type
                                                                      Search usage increases substantially (from 0 to 1,726 or
resolution. A domain-level breakdown of this effect is pro-
                                                                      1,913), indicating that the agent shifts effort from expensive
vided in Appendix C.4.
                                                                      compile-and-repair iterations toward cheaper symbol-level
                                                                      validation.
Scale and Transfer Effects. A plausible explanation for
the limited marginal value of the Expert Drafter (T ) is the          One plausible mechanism is that, before Search is avail-
disparity in model capacity and pretraining diversity. While          able, the agent may rely on REPL feedback not only for
the Herald translator is fine-tuned on Lean data, the orches-         “compile/no-compile” verification but also largely to infer
trator (GPT-5.2) is trained at much larger scale on a broad           missing identifiers, expected variables, and type constraints
mixture of programming languages, mathematics, and nat-               from Lean’s error messages; introducing Search could re-
ural language. This large-scale, multi-domain pretraining             duce this reliance by providing symbol-level information

                                                                  7
                                         Tool-Augmented Agents for Lean Formalization

earlier.                                                               Compute Cost. Agentic formalization is significantly
                                                                       more expensive than one-shot generation. Although symbol
Finally, we note that the extensive interaction logs gener-
                                                                       search tools reduce the number of compiled iterations, the
ated by our agent constitute a valuable dataset of successful
                                                                       inference cost of the full REPL loop remains a barrier to
and failed formalization trajectories. These traces map the
                                                                       real-time interactive assistance.
trial-and-error process of resolving compiler errors, making
them an ideal corpus for future research into Reinforcement
Learning (RL) for formalization. By training on these repair           7. Conclusion
loops, future models might internalize the feedback dynam-
                                                                       We presented a systematic study of tool-augmented agents
ics, learning to predict successful repairs without incurring
                                                                       for translating natural-language mathematics into Lean 4.
the high inference cost of the live REPL.
                                                                       By combining a generalist LLM with retrieval, expert draft-
                                                                       ing, and compiler feedback, the agent raises faithfulness
6. Limitations                                                         from 28.0% to 60.5% over the strongest one-shot baseline
                                                                       on a new 400-theorem benchmark.
Our study has several important limitations that contextual-
ize the interpretation of the results.                                 Beyond raw performance, our factorial analysis reveals a
                                                                       clear structural picture. Compiler feedback is the domi-
                                                                       nant capability driver, enabling a transition from unreliable
Statement Fidelity vs. Provability. Our task is translating            drafts to consistently faithful formalizations. Symbol-level
natural language into valid Lean 4 statement declarations              search improves efficiency and stability by reducing hallu-
(ending in := by sorry). We enforce syntactic validity                 cinations and lowering the number of expensive compile–
and semantic faithfulness but do not verify provability. In a          repair cycles, while expert drafting provides only marginal
small pilot on 12 benchmark problems, Aristotle achieved               gains once feedback and search are available. These results
11/12 faithful translations by consensus, while our agent              demonstrate that execution and retrieval, rather than para-
achieved 8/12 on the same subset using general-purpose                 metric specialization alone, are the critical ingredients for
LLMs. A systematic comparison with Lean-specialized                    scalable mathematical formalization.
models remains future work.
                                                                       Together, these findings suggest a general design principle
                                                                       for formal reasoning agents: high-precision execution en-
Dependence on the Lean Environment. In our cur-                        vironments should serve as the primary scaffold for LLM
rent implementation, all formal feedback ultimately flows              reasoning, with retrieval used to stabilize and accelerate con-
through the Lean 4 environment, either directly via REPL               vergence. Our results suggest a broader lesson: for rapidly
compilation or indirectly through symbol-level queries                 evolving formal libraries, one-off fine-tuning on a static cor-
backed by the installed Mathlib snapshot. As a result, our             pus may be brittle, and sustained progress likely depends
factorial analysis primarily reflects differences in interaction       more on verification-coupled iteration (and continual re-
modality (whole-program compilation vs. targeted symbol                fresh) than on a fixed offline drafter alone. We believe this
lookup) rather than access to fundamentally independent                paradigm will be central to future systems that aim to bridge
sources of mathematical truth.                                         informal mathematical knowledge and machine-verifiable
                                                                       proof.
A natural extension is to build a static, agent-facing Mathlib
dataset (e.g., indexed statements, docstrings, and symbol
metadata) that supports offline lookup and reduces reliance            Impact Statement
on the live REPL during search. However, this direction in-
                                                                       This work advances methods for translating informal math-
troduces its own limitation: Mathlib evolves rapidly, so any
                                                                       ematics into formal proof assistant statements. Potential
fixed dataset can become stale, potentially yielding outdated
                                                                       impacts include improving reliability and accessibility of
names, moved theorems, or changed type signatures unless
                                                                       formal verification tools. Risks include overreliance on auto-
it is versioned and regularly refreshed.
                                                                       mated formalization and evaluation bias; we advocate trans-
                                                                       parent reporting of tool configurations and failure modes.
Restricted Mathematical Coverage. Our benchmark
covers four major domains (Real Analysis, Complex Analy-               References
sis, Topology, Algebra). We caution that these results may
                                                                       Castelvecchi, D. AI models solve maths problems at level
not generalize to combinatorial or discrete domains (e.g.,
                                                                         of top students. Nature, 644:7, 2025.
Graph Theory, Number Theory), where formalization re-
lies less on structural type definitions and more on intricate
logical predicates.                                                    de Moura, L. and Ullrich, S. The Lean 4 theorem prover

                                                                   8
                                      Tool-Augmented Agents for Lean Formalization

  and programming language (system description). In
  Automated Deduction – CADE 28, volume 12699 of
  LNCS, pp. 625–635. Springer, 2021. doi: 10.1007/
  978-3-030-79876-5 37.
Doty, S. R. Lecture notes on abstract algebra. https://
  github.com/srdoty/AbstractAlgebraBook,
  2025. GitHub repository; accessed 2025-09-04.

Gao, G., Wang, Y., Jiang, J., Gao, Q., Qin, Z., Xu, T., and
  Dong, B. Herald: A natural language annotated lean 4
  dataset. In The Thirteenth International Conference on
  Learning Representations, 2025.

Lean Prover Community.          Missing under-
  graduate mathematics in Mathlib.     https:
  //leanprover-community.github.io/
  undergrad_todo.html. Accessed: September 4,
  2025.
Lebl, J. Basic analysis: Introduction to real analy-
  sis. https://github.com/jirilebl/ra, 2025a.
  GitHub repository; accessed 2025-09-04.
Lebl, J. Guide to cultivating complex analysis: Working the
  complex field. https://github.com/jirilebl/
  ca, 2025b. GitHub repository; accessed 2025-09-04.

McKay, B. Topology lecture notes. https://github.
 com/Ben-McKay/topology-lecture-notes,
 2025. GitHub repository; accessed 2025-09-04.
Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,
 M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.
 Kimina-prover preview: Towards large formal reason-
 ing models with reinforcement learning. arXiv preprint
 arXiv:2504.11354, 2025.




                                                              9
                                        Tool-Augmented Agents for Lean Formalization

A. Agent Implementation Details
A.1. Prompt Assembly
The system prompt is constructed from three modular components: (i) a task definition establishing the core translation
objective, (ii) a general usage guide containing fixed best practices for Lean 4 code generation, and (iii) a capability block
that is dynamically populated based on the factorial configuration (T, F, S). This structure holds the agent’s semantic goal
and coding standards (i and ii) fixed, while selectively enabling or disabling external tools (iii) to isolate the causal effect of
each capability. We assemble (i) and (ii) into a Shared Base Prompt, shown below, while the capability block definitions
are provided in Appendix A.3.

A.2. Shared Base Prompt

    Base System Prompt

   You are an expert Lean4 translation agent.
   Your task is to translate a natural-language mathematical statement into faithful Lean4 syntax (NOT a proof). The
   final result must: - import Mathlib at the very top - compile in Mathlib - be semantically faithful to the original
   statement - end with ‘:= by sorry‘
   You are NOT proving anything. You are only producing a correctly typed, correct-meaning Lean statement.
   GENERAL INSTRUCTIONS FOR CODE GENERATION
   • The Lean file MUST start with: import Mathlib
   • The Lean file MUST contain exactly ONE final translated statement representing the original natural-language
   meaning.
   • The final statement MUST end with: := by sorry
   • Do NOT write any proof code before ‘:= by sorry‘ (no ‘by‘, ‘simp‘, ‘have‘, ‘calc‘, etc. anywhere before the final
   ‘:= by sorry‘).
   • Do NOT invent new definitions, axioms, constants, or placeholder structures.
   • Prefer robust formulations: use quantifiers, membership, and ↔ characterizations rather than fragile definitional
   equalities.
   • Only finish when the last written version: (1) compiles in Mathlib (if lean4 repl runner is available) (2) is
   semantically faithful to the original statement
   When both are satisfied, return: ”status”: ”success”


A.3. Tool-Availability Blocks
Each factorial configuration (T, F, S) determines which tools are exposed to the agent. We implement this by a modular
prompt template in which the AVAILABLE TOOLS block is constructed by including the corresponding tool-specification
entries and omitting inactive ones. We show the complete tool block for the fully enabled configuration (1, 1, 1) below;
other configurations are obtained by deleting the entries for tools that are disabled.

    Tool Block (T=1, F=1, S=1)

    AVAILABLE TOOLS
    lean4 translator(statement)
      Draft a Lean 4 statement using the fine-tuned Herald translator (you may edit or ignore).
    lean write file(code)
      Write the full Lean file to the workspace (imports + exactly one final statement).
    lean4 repl runner()
      Compile the current Lean file and return compiler feedback.
    lean inspect name(name, imports?, include print?)
      Query Mathlib about an identifier via #check/#print.
    lean resolve name(token, namespace hints?, imports?, top k?)
      Suggest likely Mathlib identifiers for an unknown or ambiguous token.


                                                                10
                                    Tool-Augmented Agents for Lean Formalization


   search online(query)
     Run a web search and return results for the query.


A.4. Tool Interfaces
   Agent Tool API

       Tool                     Arguments                         Functionality
       lean inspect name        name,            imports?, Checks whether a Mathlib symbol exists and re-
                                include print?             turns its type (#check) and optionally its definition
                                                           (#print).
       lean resolve name        token, namespace hints?, Performs fuzzy symbol resolution to map informal
                                imports?, top k?           or incorrect names to valid Mathlib identifiers.
       lean4 repl runner        Lean 4 code to be          Compiles the current Lean file and returns compiler
                                executed                   diagnostics (errors, warnings, and success flags).
       lean4 translator         statement                  Invokes the fine-tuned Herald translator to generate
                                                           a draft Lean formalization of the natural-language
                                                           input.
       search online            query                      Performs external web search to retrieve mathemati-
                                                           cal or documentation context not present in Mathlib.



A.5. Example Execution Trace

   Example Execution Trace (agent tool calls)

   Step       Tool                   Arguments (agent side)
   1          lean write file        path="jirilebl ca ca 17658.lean";   content = import Mathlib
                                     ... theorem jirilebl ca ca 17658 ... := by sorry
   2          lean4 repl runner      path="jirilebl ca ca 17658.lean"
   3          lean inspect name      name="Polynomial.IsConstant"
   4          lean inspect name      name="Polynomial.eval"
   5          lean inspect name      name="Polynomial.isConstant"
   6          lean inspect name      name="Polynomial.natDegree"
   7          lean write file        path="jirilebl ca ca 17658.lean";  content = patched theorem
                                     uses p.natDegree ̸= 0 and Polynomial.eval
   8          lean4 repl runner      path="jirilebl ca ca 17658.lean"



B. LLM-as-a-Judge Prompt and Rubric
We evaluate semantic faithfulness using an LLM-as-a-judge that receives: (i) the natural-language statement, (ii) the
generated Lean 4 code, and (iii) a boolean compile pass. The judge outputs a JSON object with fields faithful and
grade (0–10). If compile pass=false, we require faithful=false and restrict the grade to 0–3. The translation
is considered as faithful if and only if the code compiles and the score is >= 9.

   Judge system prompt (verbatim)

   You are an expert in Lean 4, Mathlib, and mathematics. You are judging
    ,→ TRANSLATION-ONLY.



                                                          11
                      Tool-Augmented Agents for Lean Formalization


Input: (1) a natural-language statement, (2) a Lean 4 code snippet, (3)
 ,→ compile_pass boolean.
Your job: decide whether the Lean code, AS A STATEMENT, matches the meaning
 ,→ of the natural-language statement.

Key policy (NOT PICKY):
- If compile_pass = False: the translation is NOT faithful. grade must be
 ,→ 0..3. faithful=false.
- If compile_pass = True: ignore the proof/body entirely (including `by
 ,→ sorry`). Proof completeness is NOT part of the evaluation.
- A translation is faithful if the Lean statement expresses the same
 ,→ mathematical claim as the NL statement.

Auxiliary definitions policy (lenient but not allowing cheating):
- Auxiliary defs/lemmas are allowed if they are reasonable
 ,→ encodings/abbreviations and do not change the meaning.
- However, if the code introduces a clearly vacuous placeholder for a
 ,→ nontrivial concept (e.g. `def X := True`, `:= none`, `:= 0` for
 ,→ something meant to be meaningful), and that placeholder is essential to
 ,→ making the final theorem appear to match, then the translation is NOT
 ,→ faithful.

How to judge meaning (focus):
- Compare the MAIN theorem/definition statement(s) to the NL statement.
- Check quantifiers (forall/exists), logical structure (->/<->/and/or), and
 ,→ key hypotheses.
- Check main objects/domains: Nat/Int/Real, rings/groups, ZMod n, matrices,
 ,→ etc.
- Small implementation details are OK if the meaning is preserved.

Scoring guide (integer 0..10):
- 0: unrelated.
- 1-3: compile_pass is False OR statement is clearly wrong.
- 4-6: compiles, but meaning is materially different / missing key
 ,→ hypotheses / wrong domain;
       might be "in the ballpark".

- 7-8: compiles, mostly matches, but has a noticeable mismatch (e.g.
 ,→ strengthened/weakened in an important way).
- 9: compiles, very close; only tiny mismatch.
- 10: compiles and meaning matches.

Output contract (STRICT):
Return a single JSON object with exactly these fields:
{
  "faithful": true or false,
  "grade": 0..10,
  "thought": "### BEGIN THOUGHT\n<short explanation focusing on
   ,→ statement-level comparison>\n### END THOUGHT"
}
Return ONLY valid JSON. No extra keys. No markdown outside JSON.




                                          12
                                                Tool-Augmented Agents for Lean Formalization

C. Additional Domain Results
C.1. Domain Metrics under Full Configuration

   Domain metrics under config 111


              Table 6. Domain metrics under config=111. Conditional faithfulness is computed as Faithful/Compile.

            Domain                       Compile Faithful Faithful—Compile Steps (mean) Steps (median)
            Complex Analysis                   0.95           0.82                           0.86                 6.88            5
            Real Analysis                      0.89           0.49                           0.55                 9.84          7.5
            Algebra                            0.87           0.56                           0.64                 9.83          6.5
            Topology                           0.87           0.61                           0.70                 9.20            6


C.2. Judge Scores by Domain

   Average judge scores by domain across configurations


   Table 7. Average faithfulness scores by domain and configuration. Columns correspond to tool configurations in (T, F, S) bit
   order.

                                   Domain                      001      010     011      100         101   110      111
                                   Algebra                    5.60     7.14     7.23    4.46        5.85   7.20    7.22
                                   Complex Analysis           4.72     9.27     8.91    4.20        4.94   8.94    8.98
                                   Real Analysis              4.62     7.38     7.34    3.59        4.75   7.33    7.31
                                   Topology                   5.39     7.10     7.03    4.47        6.14   7.05    7.25

   Interpretation. Score trends are consistent with the domain difficulty ranking in Section 4.3: Complex Analysis attains the
   highest scores under tool-enabled settings, while Real Analysis remains lowest.


C.3. Domain-Level Feedback Effects

                                                                pivot_domain_faithful
                                                                                                                          0.8
                                   Algebra     0.41    0.56      0.58     0.28         0.43         0.57   0.56
                                                                                                                          0.7


                           Complex Analysis    0.28    0.84      0.80     0.25         0.31         0.79   0.82           0.6
                  domain




                                                                                                                          0.5

                              Real Analysis    0.27    0.54      0.56     0.16         0.26         0.51   0.49           0.4

                                                                                                                          0.3
                                  Topology     0.38    0.56      0.57     0.29         0.46         0.54   0.61
                                                                                                                          0.2
                                               001     010       011          100      101          110     111

                                              Figure 7. Faithful rate by domain and configuration.


                                                                          13
                                          Tool-Augmented Agents for Lean Formalization

   Domain-wise effect of Compiler Feedback (F)


                                    Domain                    F=0 (avg)        F=1 (avg)         ∆F
                                    Complex Analysis                0.28             0.81      +0.53
                                    Real Analysis                   0.23             0.53      +0.30
                                    Algebra                         0.37             0.57      +0.20
                                    Topology                        0.38             0.57      +0.19

   Interpretation. Complex Analysis benefits most from compiler feedback (+53 pts), likely due to mature Mathlib coverage.
   Algebra and Topology show smaller gains ( +20 pts), suggesting either limited library support or intrinsic formalization difficulty.




C.4. Domain-Level Effects of Search (S)

   Simple effect of Search conditioned on Feedback

   The Search tool (S) provides symbol-level queries via #check/#print, accessing a subset of REPL functionality without
   full compilation diagnostics. As noted in Section 5.3, both tools are backed by the same Lean/Mathlib snapshot, leading to the
   negative interaction F ×S = −11.6 pts.

                                                                   F=0                F=1
                                       Domain                   S=0 S=1            S=0    S=1
                                       Algebra                  0.28    0.42     0.565       0.57
                                       Complex Analysis         0.25    0.30     0.815       0.81
                                       Real Analysis            0.16    0.27     0.525      0.525
                                       Topology                 0.29    0.42      0.55       0.59
                                       Avg ∆S                    +10.8 pts          +1.0 pts

   Interpretation. When full REPL is unavailable (F=0), symbol queries provide substantial gains (+10.8 pts average). Once full
   REPL is enabled (F=1), the marginal benefit of Search drops to near zero (+1.0 pts), confirming that whole-program diagnostics
   subsume symbol-level information. This domain-level breakdown corroborates the negative F ×S interaction reported in
   Section 5.3.




C.5. Multi-Model Orchestrator Comparison
To assess whether the framework’s gains are specific to the GPT-5.2 orchestrator or reflect structural properties of tool-
augmented formalization, we evaluate two additional orchestrator models—Claude Sonnet 4.5 and Gemini-2.5-Pro—on the
full 400-theorem benchmark under the 111 (all tools) configuration.

                                                                   14
                                                      Tool-Augmented Agents for Lean Formalization


                                                         Compiles (Syntax Correct)
                                                100      Faithful (Correct)        93.0%
                                                      89.5%
                                                                                                   80.5%
                                                80

                                                                                           65.5%           65.5%


                             Success Rate (%)
                                                               60.5%
                                                60



                                                40



                                                20



                                                 0
                                                         GPT-5.2                    Sonnet 4.5     Gemini 2.5 Pro

Figure 8. Multi-model agent comparison (config 111). All three orchestrators converge to 60–65% consensus faithful despite different
one-shot baselines (19–28%).


As shown in Figure 8, all three models show large uplift from the tool-augmented framework (+148 to +163 faithful
translations) and converge to 60–65% consensus faithful despite markedly different one-shot baselines (19–28%). This
convergence confirms that the findings of the factorial analysis—particularly the dominance of compiler feedback—are
structural rather than model-specific.




                                                                                    15
