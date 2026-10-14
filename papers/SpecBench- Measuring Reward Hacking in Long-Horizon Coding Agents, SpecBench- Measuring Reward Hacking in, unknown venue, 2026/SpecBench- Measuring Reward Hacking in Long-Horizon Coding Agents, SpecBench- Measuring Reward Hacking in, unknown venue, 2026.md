                                                                                                                                           2026-09-10




                                        SpecBench: Measuring Reward Hacking in
                                        Long-Horizon Coding Agents
                                        Bingchen Zhao1 , Dhruv Srikanth1 , Yuxiang Wu1 and Zhengyao Jiang1
                                        1 Weco AI



                                        As long-horizon coding agents produce more code than any developer can review, oversight collapses
                                        onto a single surface: the automated test suite. Reward hacking naturally arises in this setup, as
                                        the agent optimizes for passing tests while deviating from the user’s true goal. We study this reward
                                        hacking phenomenon by decompose software engineering tasks into three parts: (i) a natural language
arXiv:2605.21384v2 [cs.SE] 9 Sep 2026




                                        description of the specification (ii) visible validation tests that exercise specified features in isolation,
                                        and (iii) held-out tests that compose those same features to simulate real-world usage. Based on the
                                        specification and the visible validation test suites, a genuine agent would be able to generate a solution
                                        that can also pass all of the held-out tests. Therefore we use the gap in pass rates on these two suites to
                                        quantify reward hacking. Based on this methodology, we introduce SpecBench, a benchmark comprising
                                        30 systems-level programming tasks ranging from short horizon tasks like building a JSON parser to
                                        ultra long horizon tasks like building an entire OS kernel from scratch. Large-scale experiments reveal a
                                        consistent pattern: while every frontier agent saturates the visible suite, reward hacking persists, with
                                        smaller models exhibiting larger gaps on holdout suites. The gap also scales sharply with task length:
                                        it grows by 28 percentage points for every tenfold increase in code size. Failures range from subtle
                                        feature isolation to deliberate exploits, including a 2,900-line hash-table "compiler" that memorizes
                                        test inputs. SpecBench offers a principled testbed for measuring whether coding agents build genuine
                                        working systems or merely game the test suites developers hand them.


                                        1. Introduction
                                        Software engineering is undergoing a fundamental paradigm shift. Developers are increasingly
                                        delegating the end-to-end implementation of complex systems to autonomous agents that iteratively
                                        write, test, and refine code with limited human intervention (Anthropic, 2026; OpenAI, 2025a). As
                                        tasks scale to longer horizons, the volume of code produced starts exceeding what any developer
                                        can meaningfully review. Oversight therefore collapses onto a single surface: the automated test
                                        suite. Developers use it as a proxy for whether the specification is met, and the agent treats it
                                        as its optimization target. Optimizing against this proxy creates a vulnerability long studied in
                                        reinforcement learning but under-explored in autonomous coding: reward hacking (Krakovna et al.,
                                        2020; Skalse et al., 2022). When the only feedback signal is whether tests pass, an agent can take the
                                        path of least resistance and produce code that passes those tests without satisfying the developer’s
                                        true intent.
                                            Reward hacking has been documented in qualitative case studies (Wang et al., 2026), but the
                                        field lacks a quantitative way to measure it in agentic coding. We introduce SpecBench, a benchmark
                                        of 30 systems-level coding tasks ranging from JSON parsers to operating system kernels. Each task is
                                        evaluated by two test suites (Figure 1). The validation suite, visible to the agent to iterate on, test
                                        each specified individual feature. The held-out suite, hidden from the agent, composes those same
                                        features to simulate end-to-end usage scenarios. For example, in a SQL database task, the validation
                                        tests cover SELECT, JOIN, and GROUP BY individually, while the held-out tests are queries that can
                                        combine all three. We define the reward hacking gap as the difference between an agent’s validation


                                        Correspondence: research@weco.ai
                                        © 2026 Weco AI. All rights reserved
                          SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents




  Spec + Starter Code ➔ Coding Agent                        SPEC: Build a working HTTP server
  (write → test → refine × N)                               SUPPORT: Routing, Headers, Chunked Transfer


              Validation Tests                                              Held-out Tests

                        Parse           Error                Route + Headers    Chunked +       Route + Error
    GET /route                                                   + UTF-8     Content-Length        Handling
                       Headers         Handling


             Content          Chunked                                  All Combined Composition
           Negotiation        Transfer                            (Routing, Headers, Chunked, Error)

                      =   100%                                                        =   25%
       Coding agent passes individual tests                   But fails miserably on real world usage cases.


                                       Reward Hacking Gap


Figure 1 | High-level overview of the SpecBench evaluation framework. Coding agents iteratively develop
software based on high-level specifications and are optimized against visible validation tests (𝑠val ) that verify
individual features. The generated code is subsequently evaluated on held-out tests (𝑠test ) that require complex,
cross-feature real-world use cases. The Reward Hacking Gap (Δ) is calculated as the difference between these
two scores (Δ = 𝑠val − 𝑠test ) to quantify how much the agent gamed the proxy metric. The gap should be 0 if the
system genuinely passes all validation tests.
and held-out pass rates. A positive gap means the agent has scored on the visible proxy without
genuinely satisfying the specification.
    Using SpecBench, we conduct a large-scale empirical study across models, coding harnesses
(Codex, Claude Code, OpenCode) (Anomaly, 2026; Anthropic, 2026; OpenAI, 2025a), and search
strategies (AIDE, Linear, Autoresearch) (Huntley, 2025; Jiang et al., 2025; Karpathy, 2026). We
found every model can saturate the visible test suite on every task. Yet beneath this uniform pass rate,
reward hacking scales along two axes. First, the gap between validation and holdout test pass rate
grows with task complexity (Figure 2). Second, weaker models (measured by MMLU) exhibit larger
gaps than stronger ones (Figure 4). Both findings carry the same practical warning: as teams scale to
longer tasks or swap to smaller models, the agent’s green test report increasingly hides decreasing
compliance. Beyond the quantitative findings, we also document the hacking strategies themselves,
ranging from feature isolation, where agents implement individual features that fail to share state
across components, to deliberate exploits, where agents memorize the validation tests in lookup
tables to bypass real implementation entirely.
    In summary, (i) our work bridges a critical gap in the evaluation of coding agents by formally
defining and measuring reward hacking in long horizon agentic coding. (ii) We provide the community
with a principled framework and a comprehensive testbed that exposes the hidden vulnerabilities of
test-driven development at scale. (iii) By demonstrating how pervasive these structural exploits are
across different models, search strategies, and codebase sizes, we highlight an urgent need to rethink
how we guide and evaluate AI systems. Ultimately, these insights emphasize that securing the next
generation of coding agents requires prioritizing genuine architectural integrity over the illusion of
gamified, hollow artifacts especially in long-horizon tasks.




                                                                                                                2
                                                 SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents




                          100     Mean: +23pp per 10× LOC, R²=0.24                                                                                                               os kernel
                                  P90: +28pp per 10× LOC, R²=0.25

                           80
Reward Hacking Gap (pp)




                                  Codex
                           60     Claude Code
                                  OpenCode
                                  AIDE
                           40     Linear
                                  Autoresearch                                                                                coreutils
                                                                                                                                    sql database


                           20                                                                                                                         c compiler
                                                                                                           css
                                                                                                           http2layout
                                                                                               spreadsheet engine      engine
                                                                                                                  protocol
                                                                       http server
                                                                       regex engine                                          database engine
                                                                                                                                                             javascript engine
                                                      package resolverlox             markdown     renderer
                                   json parser                        sedvm
                                                                      tinygrad
                                                                                              git impl
                                                                          interpreter filesystem     wasm
                                                                                              deflateray
                                                                                                             tcp
                                                                                                           shell
                                                                                                         tracer   stack
                                                                                                            interpreter gnu
                                                                                                                 interpreter
                                                                                                             crypto
                                                                                                       compression
                                                                                                             riscv
                                                                                                                                gollumgameboy
                                                                                                                             make
                                                                                                                        nes emulator
                                                                                                                     primitives
                                                                                                                    emulator
                                                                                                                                       compileremulator
                                                                                                                                                     elf linker
                            0
                            103                                                            104                                                                            105
                                                                  Reference Implementation Size (LOC)
    Figure 2 | Reward Hacking Gap vs. Reference Implementation Size. Each dot is one experiment run.
    This plot demonstrates that the upper bound (90th-percentile) of the reward hacking gap scales predictably,
    increasing by 27 percentage points for every tenfold increase in lines of code.

    2. Benchmark Design
    Setup. Each SpecBench task provides a natural-language specification 𝑆, starter code with stub
    implementations, and a validation test suite 𝑇val that serves as the agent’s optimization target. An
    agent 𝐴 receives 𝑆 and 𝑇val , then iteratively generates code, runs 𝑇val , and refines it over a budget of 𝑁
    steps, producing a candidate implementation 𝑐. A separate held-out test suite 𝑇test , never shown to
    the agent, is used solely for evaluation. Note that the specification 𝑆 defines all requirements for the
    target generated system and specifies that the system will be used in end-to-end complex feature
    interaction scenarios that the held-out test suite 𝑇test is evaluating.
    Measuring Reward Hacking. Let 𝑠val ( 𝑐) and 𝑠test ( 𝑐) ∈ [0, 1] denote the pass rates of 𝑐 on the validation
    and held-out test suites, respectively. We define the reward hacking gap as

                                                                        Δ ( 𝑐) = 𝑠val ( 𝑐) − 𝑠test ( 𝑐) .                                                                              (1)

    When Δ > 0, the agent has optimized the proxy (validation test pass rate) beyond its true specification
    compliance: it passes feature-level tests but fails when those features must compose. Δ = 0 indicates
    no hacking is happening. This directly instantiates the reward hacking framework from (Skalse et al.,
    2022), where optimizing a proxy reward 𝑅ˆ diverges from the true objective 𝑅∗ ; here 𝑅ˆ = 𝑠val and
    𝑅∗ = 𝑠test .
                                                                                               Table 1 | SpecBench summary statistics by task horizon.
    Test Design. The key to making Δ a faithful
    measure of reward hacking is the relationship                                                 Horizon                      Tasks       Avg LOC         Avg |𝑇val |     Avg |𝑇test |
    between 𝑇val and 𝑇test . The validation suite con-                                            Short (<10K)                    9           5.1K             53                102
                                                                                                  Medium (10–25K)                13          13.8K             66                 80
    tains tests for each individual features of the                                               Long (>25K)                     8          45.6K             54                99
    task, for example, a SQL database’s validation                                                All                            30          19.5K             59                93

                                                                                                                                                                                          3
                           SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents


Table 2 | Comparison of SpecBench with existing coding benchmarks. SpecBench is the first benchmark
that explicitly measures reward hacking through a two-way test decomposition. LOC refers to the reference
implementation size.

                                                                                                    Reward Hacking
 Benchmark                                   Tasks    LOC Range       Language       From Scratch
                                                                                                     Measurement
 HumanEval (Chen et al., 2021)                164        5–50           Python            !               #
 MBPP (Austin et al., 2021)                   974        5–30           Python            !               #
 ClassEval (Du et al., 2023)                  100      50–200           Python            !               #
 SWE-bench Verified (Jimenez et al., 2023)    500    N/A (patches)      Python            #               #
 SWE-bench Pro (Deng et al., 2025)            723    N/A (patches)      Python            #               #
 LiveCodeBench (Jain et al., 2024)           400+      10–100           Python            !               #
 DevBench (Golnari et al., 2026)               22      1K–10K           Python            !               #
 KernelBench (Ouyang et al., 2025)            250      50–500           CUDA              !               #
 SpecBench (ours)                             30      1.5K–110K      C/Python/Go          !               !

tests verify SELECT, JOIN, GROUP BY, and HAVING individually. The held-out suite composes these
features within each test, for example, a single query that joins two tables, groups by a joined column,
and filters with HAVING on an aggregate. Crucially, 𝑇test introduces no requirements beyond what
𝑆 and 𝑇val already specify. Every composition tested is mandated by the specification. A genuinely
compliant implementation should pass both suites without modification. Therefore Δ > 0 reflects the
agent gaming the proxy.
Task Suite. SpecBench comprises 30 systems-level programming tasks spanning a wide range of
complexity: from short-horizon tasks such as building a JSON parser (∼1,500 LOC reference) to
ultra-long-horizon tasks such as implementing an OS kernel from scratch (∼110,000 LOC reference).
Each task ships with a reference implementation that passes all tests 𝑇val and 𝑇test , ensuring the test
suite is satisfiable. Table 2 shows a comparison of SpecBench with prior benchmarks on coding agents.
Among these benchmarks, SpecBench is the only one benchmark that enables the measurement of
reward hacking. Please note that our validation tests 𝑇val and held-out tests 𝑇test are not to be confused
with the train/validation split in benchmark like SWE-Bench Pro (Deng et al., 2025) where the train
and validation splits are on different tasks. While on SpecBench, 𝑇val and 𝑇test are test suites designed
for the same task. Table 1 shows the summary statistics of SpecBench.

3. Experiments
We evaluate coding agents on SpecBench using a two-level architecture for the agent 𝐴: an inner agent
that writes and edits code, wrapped by an outer search loop that decides which candidates 𝑐 to refine.
This separation lets us independently vary the coding model and the search strategy. Other than
experiments in this section, we demonstrate one additional case studies on SpecBench in Appendix C.
Inner Agents. We evaluate three agents: Codex (OpenAI, 2025a), Claude Code (Anthropic, 2026),
and OpenCode (Anomaly, 2026). These are frontier-class coding agents with tool use, file editing, and
terminal access. To broaden model coverage, we evaluate OpenCode, an open-source coding CLI, with
five open-weight and API models: DeepSeek-V3.2 (DeepSeek-AI, 2025), DeepSeek-V4-Pro (DeepSeek-
AI, 2026), Qwen3-Coder (Cao et al., 2026), Kimi-K2.5 (Kimi Team, 2026), Kimi-K2.6 (Moonshot AI,
2026), and Minimax-M2.7 (MiniMax AI, 2026).
Search Strategies. Each coding agent is paired with a search strategy that control how the outer loop
explores the solution space. Generally, the process for coding agents to generate a solution to a test
suite can be described in a tree structure where each node is a full codebase built by an inner agent.
And each node can branch out child node that expands on the codebase built in its parent node to try
to pass more validation tests. At the beginning, the root node of this search tree is the starter code


                                                                                                                     4
                              SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



                                             Search Strategies
             AIDE Search                                   Linear                                 Autoresearch
                starter                                    starter                                   starter


                                                            step 1                                   step 1
    draft1       draft2      draft3
                                                            step 2                                   step 2
     debug      improve
                             best so far
                                                            step 3                                   step 3      new best

     step6    step5       step4
                                                                                                     step N
                                                            step N     solution
   • Selects best-scoring node at each
             step to expand.                     • Single chain, no branching.          • Single chain, always keeps best
                                                                                             candidate found so far.
  • Branches: draft, debug, or improve.      • Each step refines the previous one.
                                                  • Last node is the solution.         • Best public score across all wins.
      • Multiple branches explored.


Figure 3 | Search strategies used as the outer loop for coding agent. We model each generated codebase
as a node in a search tree. AIDE (Jiang et al., 2025) expands the highest-scoring candidate and explores
multiple branches via draft, debug, and improve operations; Linear (Huntley, 2025) performs sequential
refinement along a single chain and returns the final node; Autoresearch (Karpathy, 2026) also follows a
single refinement chain but retains the best candidate encountered according to public validation score.

(stub) we give to the coding agent and with each iteration of prompting the coding agent generates a
new node. Under this search tree formulation, we test three search strategies, including AIDE (Jiang
et al., 2025), Linear (Huntley, 2025), and Autoresearch (Karpathy, 2026). AIDE (Jiang et al.,
2025) is an advanced search algorithm often used for optimizing code solutions (OpenAI, 2025b). It
uses tree search with draft, debug, and improve branching. At each step, it selects the most promising
node in the search tree and generates a child via one of three operations. Note that in AIDE the
agents only have context of the path from the root node to the best so far node without context to
any of the sibling nodes. Linear (Huntley, 2025) is proposed as a simple solution to enable coding
agents to work on long horizon tasks. It performs sequential refinement without branching: each step
improves the single candidate solution from its parent. Autoresearch (Karpathy, 2026) extends
the Linear strategy by always keeping track of the single best candidate solution so far. Figure 3
demonstrates the difference of these three search strategies.


3.1. Task Horizon and Reward Hacking

We first examine how the length of the implementation horizon, measured by the reference imple-
mentation size in lines of code (LOC), relates to the severity of reward hacking. Figure 2 plots the
reward hacking gap Δ against reference LOC for every run in our dataset. We found that both the
average reward hacking gap Δ as well as the 90th-percentile reward hacking gap scales predictably
with the task size. For example, the 90th-percentile gap grows by approximately 27 percentage points
for every tenfold increase in LOC (𝑅2 = 0.21). Among tasks under 10K LOC, the worst-case gap is
21pp. Among tasks over 25K LOC, it reaches 100pp.
    This scaling trend suggests that reward hacking in long-horizon code generation is driven less
by isolated implementation difficulty and more by the growth of the compositional surface area.
As implementations needed for a system become larger, the number of internal interfaces, shared
invariants, and cross-feature execution paths grows much faster than the number of feature-level
validation tests. An agent can therefore obtain a high validation score by implementing locally correct
handlers or feature-specific shortcuts, while still failing to build the global architecture needed for
those features to interact. The relatively modest 𝑅2 indicates that LOC is only a coarse proxy for

                                                                                                                              5
                                                                             SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents


                                         Reward Hacking Gap                                                                                  Validation Score                                                                           Held-out Score
                                                                                                                                           Minimax-M2.7 Kimi-K2.6
                                                                                                                                       Qwen3-Coder
                                                                                                                                                                             DeepSeek-V4-Pro
                                                                                                                                                                                  Claude Opus 4.6
                           22                                          DeepSeek-V3.2                                       100                                                                                        100
                                     Qwen3-Coder                                                                                                    Kimi-K2.5     GPT-5.2-Codex
Mean Reward Hacking Gap (pp)



                                                                                                                               95                                   DeepSeek-V3.2                                         95
                           20                                                                                                                                                                                                                       Kimi-K2.6




                                                                                                   Mean Validation Score (%)




                                                                                                                                                                                                Mean Held-out Score (%)
                                                                                                                                                                                                                                                                                Claude Opus 4.6
                                                                                                                                                                                                                                                                           DeepSeek-V4-Pro
                           18                                                                                                  90                                                                                         90                                    GPT-5.2-Codex
                                          Minimax-M2.7

                           16                                                                                                  85                                                                                         85                   Kimi-K2.5
                                                                                                                                                                                                                                      Minimax-M2.7

                           14                                                                                                  80                                                                                         80      Qwen3-Coder
                                                   Kimi-K2.5
                           12                                                                                                  75                                                                                         75
                                                                                                                                                                      Model Size                                                                                  DeepSeek-V3.2
                           10                                                    DeepSeek-V4-Pro
                                                                                                                               70                                          ~200B                                          70
                                                                                                                                                                           ~500B
                                                                     GPT-5.2-Codex Claude Opus 4.6                             65                                          ~1000B                                         65
                               8
                                                         Kimi-K2.6
                                                                                                                                                                           Unknown
                               80   82      84       86         88          90         92                                      6080   82      84       86       88        90       92                                     6080   82     84       86        88          90         92
                                           MMLU Score (%)                                                                                    MMLU Score (%)                                                                             MMLU Score (%)
       Figure 4 | Model capability reduces reward hacking but does not eliminate it. (Left) The reward hacking
      gap decreases with model capability, measured by MMLU score. (Center) All models achieve near-identical
      validation scores, regardless of MMLU score. (Right) Held-out scores diverge sharply, with less capable models
      scoring significantly lower. These results show less capable models tend to reward hack more, while SpecBench
      exposes differences that are hidden by validation scores alone.

       horizon, some small tasks still expose difficult semantic interactions, while some larger tasks have
       modular structures that are easier to decompose. Nevertheless, the sharp increase in the reward
       hacking gap Δ shows that long-horizon tasks create more opportunities for severe reward hacking,
       turning reward hacking from an occasional edge case into a structural failure mode.


       3.2. Model Capability and Reward Hacking

      We next study how reward hacking relates with model capability. Figure 4 compares each model’s
      mean reward hacking gap against its general capability, using MMLU score as a coarse proxy. We
      observe a clear negative trend: stronger models tend to exhibit smaller reward hacking gaps. However,
      capability alone does not eliminate the problem. Even the strongest models retain a non-zero gap,
      indicating that reward hacking is not merely a failure mode of weak models.
           The middle and right panels clarify the source of this trend. Across models, validation scores are
       nearly saturated: both stronger and weaker models can optimize the public tests to a high level. The
       difference only becomes apparent on the held-out tests, where weaker models achieve substantially
       lower scores. This suggests that the validation suites alone are insufficient to distinguish genuine
       implementation quality once agents have enough capability to fit feature-level checks. Instead, the
       held-out suites reveal whether the model has built the underlying system architecture needed for
       real-world use cases to pass correctly. These results support two conclusions. First, increasing model
       capability improves true specification compliance: stronger models are better at inferring the intended
       abstractions behind the tests 𝑇val and specification 𝑆 and are less likely to rely on brittle, feature-specific
       implementations. Second, better models do not remove the incentive mismatch introduced by test-
       driven optimization. Since the validation suite observes only a finite set of feature-level behaviors, an
       implementation can score highly while still missing the shared invariants and cross-feature interactions
       required by real-world use cases. SpecBench exposes this discrepancy by evaluating use cases that
       are already implied by the specification, rather than introducing new requirements. The resulting gap
       therefore measures how much visible test performance can overestimate genuine implementation
       quality.




                                                                                                                                                                                                                                                                                             6
                            SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



3.3. Agent and Search Mode Comparison

We next compare how the choice of coding agent and outer loop search strategy affects reward hacking.
Figure 5 reports validation and held-out pass rates for each agent and search strategy combination.
Each bar in Figure 5 shows the validation score, and the stacked solid part of the bar is the held-out
suite test score, therefore the hatched areas demonstrates the reward hacking gap Δ. Across most
settings, the validation scores are close to saturation, showing that agents can reliably optimize the
visible validation tests. However, the hatched areas of the bars differ substantially, meaning that
similar validation scores can correspond to very different levels of true specification compliance.
    The results show that reward hacking is       100
not tied to a single agent or search strategy.                                                                 =34pp =32pp
                                                   80 =43pp =48pp =43pp =39pp
Claude Code achieves near-identical valida-                                                       =48pp




                                                            Pass Rate (%)
                                                                                         =64pp          =60pp
tion scores under AIDE, Autoresearch, and          60
Linear, but the held-out score remains much
lower, producing gaps of roughly 43-48pp.          40

Codex shows a stronger interaction with search     20      Codex
mode: AIDE gives the highest held-out score                Claude Code           Held-out Score (solid)
                                                           OpenCode              Hacking Gap (hatched)
among the Codex runs, while Autoresearch            0                          r
                                                            E           c h  a   AIDE           ch ar AIDE            ch ar
                                                        AID        esear Line              esear Line            esear Line
produces the largest gap, suggesting that re-                 Autor                   Autor                 Autor
taining the best validation score candidate can Figure 5 | Agent and search comparison on
amplify proxy over-optimization when the val- SpecBench. Bars show held-out score (solid) plus re-
idation score is poorly aligned with composi- ward hacking gap (hatched). Validation scores are
                                                near-saturated, while held-out scores vary substantially
tional correctness. OpenCode exhibits the op- across agents and search strategies.
posite pattern: AIDE has the largest gap, while
Autoresearch and Linear recover higher held-out scores.
    These results suggest that search strategy changes how reward hacking manifests, but does
not remove the underlying incentive mismatch. Tree search can help when exploration discovers
genuinely better architectures, but it can also select brittle candidates if they score well on validation
tests. Similarly, best-so-far selection can preserve useful improvements, but it can also lock onto a
proxy-optimized implementation. Overall, Figure 5 reinforces the central claim of SpecBench: public
validation performance alone is not a reliable indicator of genuine implementation quality. Even when
validation scores are nearly indistinguishable, held-out tests reveal large differences in whether the
generated systems actually satisfy the intended specification.


3.4. Does More Search Amplify Hacking?

A natural question is whether reward hacking is simply an artifact of insufficient search. If agents
initially produce brittle implementations but later refine them into coherent systems, then increasing
the search budget should reduce the reward hacking gap. Figure 6 tests this hypothesis by tracking
the reward hacking gap at each search step. We report both the interquartile mean (IQM), which
captures the typical behavior while reducing sensitivity to outliers (Agarwal et al., 2021), and the
90th percentile (P90), which captures the upper tail of severe reward hacking.
    The results show that additional search does not reliably remove reward hacking. Across agents,
the IQM gap remains non-zero throughout the search process. OpenCode exhibits the largest central
gap for most of the run, while Codex and Claude Code start with smaller gaps but show clear
increases after later search steps. The P90 curves show an even stronger effect: severe reward hacking
cases persist across the entire search trajectory and often become larger as search proceeds. Thus,
even when additional steps improve some implementations, they do not eliminate the tail of strongly


                                                                                                                         7
                                            SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents


                                                                       By Agent
                              30                                                                             70
IQM Reward Hacking Gap (pp)




                                                                               P90 Reward Hacking Gap (pp)
                              25                                                                             60
                              20                                                                             50
                                                                                                             40
                              15
                                                                                                             30
                              10                                                                             20
                                                                Codex                                                                     Codex
                               5                                Claude Code                                  10                           Claude Code
                                                                OpenCode                                                                  OpenCode
                               0                                                                              0
                                                                By Search Strategy
                              30                                                                             70
                                                                AIDE                                                                      AIDE
IQM Reward Hacking Gap (pp)




                                                                               P90 Reward Hacking Gap (pp)
                              25                                Linear                                       60                           Linear
                                                                Autoresearch                                 50                           Autoresearch
                              20
                                                                                                             40
                              15
                                                                                                             30
                              10                                                                             20
                               5                                                                             10
                               00   10   20          30       40           50                                 00   10   20          30   40          50
                                           Search Step                                                                    Search Step
     Figure 6 | Reward hacking dynamics over search steps. We report the IQM and 90th-percentile (P90) reward
     hacking gap at each search step, grouped by coding agent and search strategy. The gap does not vanish with
     additional search; in several settings, especially in the P90 domain, longer search increases the severity of
     reward hacking.
     reward hacked solutions. The search-strategy view clarifies why this happens. AIDE and Linear
     both show increases in the IQM gap after longer search, and their P90 gaps remain high. This suggests
     that iterative refinement can improve validation performance by adding feature-specific fixes without
     necessarily improving the shared abstractions required for held-out tests. Autoresearch shows
     a flatter IQM curve, indicating that retaining the best-so-far candidate can sometimes avoid large
     central increases in the gap. However, the gap still remains above zero, so best-so-far selection
     does not solve the underlying proxy mismatch. Overall, Figure 6 suggests that reward hacking is
     not merely an early-search failure that disappears with more compute. Longer search gives agents
     more opportunities to improve genuine implementations, but it also gives them more opportunities
     to discover reward hacking candidates that score well on validation tests. The effect is therefore
     conditional on the alignment between the validation suite and real world use: when validation tests
     reward local feature completion more than real world use cases, additional search can preserve or
     amplify the reward hacking gap rather than closing it.


     3.5. Increasing Coverage of Validation Sets.

    A common practice in software engineering for improving code quality is to write more comprehensive
    tests. Given the reward hacking behavior observed in the preceding experiments, a natural question
    is whether giving the agent access to richer validation tests would reduce the gap. If the visible suite
    includes tests for feature compositions, the agent receives direct optimization signal for cross-feature
    interactions and may be steered toward implementations that handle them correctly and do not
    reward hack. We test this by progressively increasing the compositional complexity of the visible test
    suite while keeping the held-out evaluation fixed.
         We compare three validation regimes. In the single-feature regime, the agent sees only the
     default validation tests, each exercising one spec feature in isolation; this is the baseline used in
     all other experiments. In the + composition regime, we augment the visible suite with tests that
     exercise multi-feature interactions, so the agent now receives optimization signal for both individual

                                                                                                                                                         8
                          SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



features and their compositions. In the full coverage regime, we go further and add composition
tests at a similar level of difficulty as the held-out suite, so the agent optimizes against tests that are
comparable in compositional complexity to those used for held-out evaluation. Across all three regimes,
the held-out evaluation is unchanged: we always measure the gap using the same held-out suite.
As shown in Figure 7, increasing validation cov-
                                                                               +27




                                                         Reward Hacking Gap (pp)
erage produces mixed results. The gap neither
                                                                       7                     Single-feature tests
consistently shrinks nor grows, and the effect            40               26                + Composition tests
varies widely across tasks. At one extreme,                                                  Full coverage
                                                          30
sql_database sees its gap drop from 35pp                                                   +13
to 9pp when composition tests are added, as               20
the richer signal guides the agent toward fixing                                                              6
cross-feature interactions it previously had no           10
incentive to address. At the other extreme, the            0
                                                                   ils   se    er       er ne       ne     ne
                                                                eut ataba ompil _serv _engi _engi _engi
gap on c_compiler increases by 25pp, as the
                                                             o r
                                                            c l_d
agent struggles to satisfy a larger set of tests
                                                                 sq      c_c http ayout regex script
                                                                                     _l       jav
                                                                                                  a
                                                                                 css
that impose conflicting demands on tightly cou-
pled code. On several other tasks the gap barely
                                                       Figure 7 | Reward hacking gap under three levels of
moves regardless of how many tests are made validation test coverage.
visible, suggesting that the compositions are
genuinely difficult to implement rather than merely lacking optimization signal. These findings
suggest that reward hacking cannot be eliminated by improving the test suite alone: richer tests
help when the agent already has the capability but lacks the signal, yet they can backfire when the
underlying compositions are genuinely difficult to get right.


3.6. Reward Hacking Case Studies

SpecBench reveals a spectrum of reward hacking behaviors, from explicit proxy exploits to more subtle
system-level failures. We manually inspect representative generated programs to understand what
kinds of implementation failures give rise to the reward hacking gap. Figure 8 shows two examples,
and Figure 9 summarizes the distribution of the corresponding qualitative categories across agents
and model groups.
Severe: lookup-table memorization. On the C compiler task, Codex discovered a strategy that
entirely bypasses implementation. Instead of building a lexer, parser, and code generator, the agent
pre-computed expected outputs for the public test programs by running them through the system
GCC, then stored the results in a 2,900-line hash table mapping input source hashes to expected
output bytes. The generated “compiler” simply hashes the input, looks up the result, and emits
assembly that writes the pre-computed output. This achieves 97% on validation tests and 0% on
held-out tests, yielding a 97pp reward hacking gap. The behavior is especially revealing because
the exploit was selected during search: an earlier node in the same AIDE run produced a genuine
7,900-line compiler that achieved 53% validation score and 43% held-out score. AIDE nevertheless
selected the lookup-table artifact because it scores higher on the visible validation objective. This
case demonstrates that search over validation score can actively steer the agent away from a more
genuine implementation when the proxy is misaligned with the true objective.
Moderate: feature isolation. The most common failure mode is less explicit but more pervasive. On
the SQL database task, agents often implement SELECT, JOIN, GROUP BY, and HAVING as separate
handlers. Each handler passes the validation tests for its corresponding feature. However, the imple-
mentation lacks a shared representation for column resolution, aliases, joined-table schemas, and
aggregate state. When a held-out test composes these features in a single query, the handlers fail to


                                                                                                               9
                                SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents




  CASE 1: Severe — Lookup Table Hack                                    CASE 2: Moderate — Feature Isolation
  Task: C Compiler (959 public tests)                                   Task: SQL Database (15 public tests)

  What the agent SHOULD build:                                          What the agent ACTUALLY built:
                 source.c → Lexer → Parser                              select_handler:                  join_handler:
                                                                        parse columns, find table        merge 2 tables, new cols
                → AST → CodeGen → output.s
                   → Assembler → binary                                 groupby_handler:                 having_handler:
                                                                        aggregate by col name            filter on aggregate val

  What the agent ACTUALLY built:                                        • No shared column resolver      • Each handler has own scope

                                                                        Result: Public tests pass (SELECT, JOIN, GROUP BY, HAVING)
                  source.c → FNV-64 Hash
                → Lookup expected_outputs[]                             Private test (FAILS):
                 → Emit pre-stored answer                               SELECT d.name, COUNT(*) FROM employees e
                                                                        JOIN departments d ON e.dept_id = d.id
     2,900 lines of hash table. Pre-computed using system GCC.          GROUP BY d.name HAVING COUNT(*) > 5
                                                                        FAIL: GROUP BY can't see join aliases — no shared state
  DELIBERATE exploit                                                    UNINTENTIONAL — built 4 isolated handler modules


      Public          Private                Gap: 97pp                      Public             Private                   Gap: 65pp
     97%               0%             Inputs never seen by agent          100%                 35%                   Compositional failure




Figure 8 | Representative reward hacking behaviors. We show two examples of generated systems that
pass validation tests while failing held-out compositional tests. In the C compiler task, the agent bypasses
compilation by hashing public-test inputs and returning pre-computed outputs. In the SQL database task,
the agent implements isolated handlers for individual SQL features, but fails when private tests require these
features to share state across a composed query.

                     Genuine             Feature Isolation             Edge Case Gaps                    Deliberate Exploit
                                                                 19%                                                      15%
  40%          35%              43%        32%                         36%                41%            33%                                 36%

        24%                            23%                       43%                              24%                        47%

     Codex                      Claude Code                      OpenCode                Strong Models                     Weak Models
                                                                                         (SWE 80%)                         (SWE < 80%)
Figure 9 | Distribution of qualitative outcome categories. We classify generated systems into genuine
solutions, feature-isolation failures, edge-case gaps, and deliberate exploits. The pie charts show the fraction
of each category across coding agents and across stronger versus weaker models, using SWE-Bench score to
separate the two capability groups.

pass the necessary state across feature boundaries. For example, a query that joins employees with
departments, groups by a joined column, and filters with HAVING fails because the GROUP BY logic
cannot resolve columns introduced by the join. This implementation achieves 100% validation perfor-
mance but only 35% held-out performance, producing a 65pp gap. Unlike lookup-table memorization,
this is not the agent deliberately reward hacking. It emerges naturally from optimizing individual
feature-level checks: the generated system contains locally plausible components, but never builds
the global abstractions required for end-to-end correctness.
Qualitative distribution of failures. Figure 9 shows that deliberate exploits are rare, while com-
positional failures account for a much larger fraction of reward hacking behavior. Across agents, a
substantial portion of generated systems fall into either feature isolation or edge-case gaps, meaning
that the system appears correct under feature-level validation but fails under broader usage. This pat-
tern is especially pronounced for weaker models: compared with stronger models, they produce fewer
genuine solutions and more feature-isolation failures. This is consistent with the results in Section 3.2
where weaker models obtain validation scores comparable to stronger models but substantially lower
held-out scores. Together, these case studies clarify what the reward hacking gap measures. A high


                                                                                                                                               10
                       SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



gap can come from an explicit exploit, such as memorizing public tests, but it more often reflects a
structural mismatch between local test passing and global system correctness. SpecBench exposes
both kinds of failures because held-out tests do not introduce new requirements; they require only
that the specified features compose into a real working system.


4. Related Work
Reward Hacking and Specification Gaming. Reward hacking, optimizing a proxy while degrading
the true objective, was formalized by (Skalse et al., 2022), who proved almost no proxy is unhackable.
Krakovna et al. (2020) catalogued gaming instances across RL and program synthesis. Pan et al.
(2022) and Gao et al. (2022) quantified reward overoptimization in RLHF. Manheim and Garrabrant
(2018) connected these to Goodhart’s Law. In coding agents, Baker et al. (2025) showed RL-trained
models exploit test harnesses with cross-domain transfer. Denison et al. (2024) showed gaming
escalates from simple to severe forms. Greenblatt et al. (2024) found low-stakes hacking generalizes
to novel settings. Our work, SpecBench takes a step forward and studys reward hacking in the context
of long-horizon system-level software engineering tasks.
Reward Hacking Benchmarks. EVILGENIE (Gabor et al., 2025) modifies LiveCodeBench (Jain et al.,
2024) to enable test manipulation, finding LLM judges outperform held-out tests for detecting reward
hacking. Countdown-Code (Khalifa et al., 2026) shows 1% cheating in supervised fine-tuning primes
catastrophic hacking during RLVR. TRACE (Deshpande et al., 2026) introduces 517 trajectories across
54 hack categories; GPT-5.2 detects only 63%. Terminal Wrench (Bercovich et al., 2026) catalogs 331
hackable tasks with 3,632 exploit trajectories. RHB (Thaman, 2026) finds RL post-training increases
exploit rates from 0.6% to 13.9%. SpecBench differs: we evaluate systems-level software (1.5K–110K
LOC) where hacking arises from architectural failures (feature isolation), not test manipulation.
This fits with the current trends in the community of deploying coding agents real world production
environments.
Coding Benchmarks. HumanEval (Chen et al., 2021) and MBPP (Austin et al., 2021) evaluate isolated
functions. SWE-bench (Deng et al., 2025; Jimenez et al., 2023) assumes pre-existing architecture.
ClassEval (Du et al., 2023) found models struggle with intra-class dependencies. DevBench (Li et al.,
2025), CrossCodeBench (Niu et al., 2023), LiveCodeBench (Jain et al., 2024), KernelBench (Ouyang
et al., 2025), and NL2Repo (Ding et al., 2025) each advance scope but none separate proxy from true
objective. SpecBench differs from all the above in three ways: (1) tasks require building complete
systems from scratch (1.5K–110K LOC), not patching existing repos; (2) we explicitly separate
the proxy metric (validation tests) from the true objective (held-out tests), enabling quantitative
measurement of reward hacking; and (3) our tasks span orders of magnitude in complexity, from
JSON parsers to OS kernels, covering the full spectrum of long-horizon development.
LLM-Based Coding Agents. Modern coding agents combine frontier LLMs with tool use, terminal
access, and file editing in iterative agentic loops. Proprietary scaffolds include Codex CLI (OpenAI,
2025a), which wraps OpenAI models with full-auto execution; Claude Code (Anthropic, 2026),
which provides Anthropic models with persistent workspace state; and Gemini CLI (Google, 2025),
which integrates Google models with shell access. Open-source alternatives like OpenCode (Anomaly,
2026) and Aider (Gauthier, 2024) democratize access to agentic coding with support for multiple
model backends. The search strategy wrapping these agents is as important as the model itself.
AIDE (Jiang et al., 2025) introduced tree search for code generation, using draft-debug-improve
branching to explore the solution space. Ralph-loop (Huntley, 2025) uses linear sequential refinement.
Autoresearch (Karpathy, 2026) extends linear search by maintaining the best candidate across steps.
Our experiments compare all three strategies and find that the search algorithm has a smaller effect


                                                                                                   11
                           SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



on reward hacking than the underlying model capability.


5. Conclusions
We introduced SpecBench, a benchmark for measuring reward hacking in long-horizon coding agents
by separating visible validation tests from held-out tests. Across 30 systems-level programming
tasks, our results show that high validation scores can substantially overestimate true specification
compliance, especially as task horizons grow longer. This reflects Goodhart’s law (Goodhart, 1975;
Strathern, 1997) in the setting of autonomous software development: once test pass rate becomes the
optimization target, it can cease to be a reliable measure of whether the generated system actually
satisfies the intended specification. SpecBench exposes this gap quantitatively and qualitatively,
showing both deliberate proxy exploits and more common failures of feature composition. These
findings suggest that future evaluations of coding agents must move beyond surface-level test passing
and measure whether generated systems preserve the shared abstractions, invariants, and end-to-end
behavior required for real software correctness.


References
R. Agarwal, M. Schwarzer, P. S. Castro, A. Courville, and M. G. Bellemare. Deep reinforcement learning at the
   edge of the statistical precipice. Advances in Neural Information Processing Systems, 2021. 7

Anomaly. OpenCode: The open source coding agent. https://github.com/anomalyco/opencode, 2026.
  Version v1.14.39; MIT License; accessed: 2026-05-05. 2, 4, 11

Anthropic. Claude Code: Anthropic’s agentic coding system. https://www.anthropic.com/product/
  claude-code, 2026. Accessed: 2026-05-05. 1, 2, 4, 11
J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, et al.
   Program synthesis with large language models. arXiv preprint arXiv:2108.07732, 2021. 4, 11

B. Baker, J. Huizinga, L. Gao, Z. Dou, M. Y. Guan, A. Madry, W. Zaremba, J. Pachocki, and D. Farhi. Monitoring
   reasoning models for misbehavior and the risks of promoting obfuscation. arXiv preprint arXiv:2503.11926,
   2025. 11

I. Bercovich, I. Segal, K. Zhang, S. Saxena, A. Raghunathan, and Z. Zhong. Terminal wrench: A dataset of 331
   reward-hackable environments and 3,632 exploit trajectories. arXiv preprint arXiv:2604.17596, 2026. 11

R. Cao, M. Chen, J. Chen, Z. Cui, Y. Feng, B. Hui, Y. Jing, K. Li, M. Li, J. Lin, Z. Ma, K. Shum, X. Wang, J. Wei,
  J. Yang, J. Zhang, L. Zhang, Z. Zhang, W. Zhao, and F. Zhou. Qwen3-coder-next technical report. arXiv
   preprint arXiv:2603.00729, 2026. URL https://arxiv.org/abs/2603.00729. 4

N.       Carlini.         Building    a    C     compiler    with     a           team         of   parallel   claudes.
     https://www.anthropic.com/engineering/building-c-compiler, 2026. 15

M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph,
  G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray,
  N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert,
  F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin,
  S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford,
  M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever,
  and W. Zaremba. Evaluating large language models trained on code. arXiv 2107.03374, 2021. 4, 11

DeepSeek-AI. Deepseek-v3.2: Pushing the frontier of open large language models, 2025. URL https:
  //arxiv.org/abs/2512.02556. 4


                                                                                                                    12
                          SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



DeepSeek-AI. Deepseek-v4: Towards highly efficient million-token context intelligence, 2026. URL https:
  //huggingface.co/deepseek-ai/DeepSeek-V4-Pro. Model card for DeepSeek-V4-Pro; accessed:
  2026-05-05. 4

X. Deng, J. Da, E. Pan, Y. Y. He, C. Ide, K. Garg, N. Lauffer, A. Park, N. Pasari, C. Rane, et al. Swe-bench pro:
   Can ai agents solve long-horizon software engineering tasks? arXiv preprint arXiv:2509.16941, 2025. 4, 11

C. Denison, M. MacDiarmid, F. Barez, D. Duvenaud, S. Kravec, S. Marks, N. Schiefer, R. Soklaski, A. Tamkin,
  J. Kaplan, et al. Sycophancy to subterfuge: Investigating reward-tampering in large language models. arXiv
   preprint arXiv:2406.10162, 2024. 11

D. Deshpande, A. Kannappan, and R. Qian. Benchmarking reward hack detection in code environments via
  contrastive analysis. arXiv preprint arXiv:2601.20103, 2026. 11

J. Ding, S. Long, C. Pu, H. Zhou, H. Gao, X. Gao, C. He, Y. Hou, F. Hu, Z. Li, et al. Nl2repo-bench: Towards
   long-horizon repository generation evaluation of coding agents. arXiv preprint arXiv:2512.12730, 2025. 11

X. Du, M. Liu, K. Wang, H. Wang, J. Liu, Y. Chen, J. Feng, C. Sha, X. Peng, and Y. Lou. Classeval: A manually-
   crafted benchmark for evaluating llms on class-level code generation, 2023. 4, 11

J. Gabor, J. Lynch, and J. Rosenfeld. Evilgenie: A reward hacking benchmark. arXiv preprint arXiv:2511.21654,
   2025. 11

L. Gao, J. Schulman, and J. Hilton. Scaling laws for reward model overoptimization. arxiv e-prints. arXiv
   preprint arXiv:2210.10760, 2022. 11

P. Gauthier. Aider: Ai pair programming in your terminal. https://aider.chat, 2024. 11

P. A. Golnari, A. Kumarappan, W. Wen, X. Liu, G. Ryan, Y. Sun, S. Fu, and E. Nallipogu. Devbench: A realistic,
   developer-informed benchmark for code generation models. arXiv preprint arXiv:2601.11895, 2026. 4

C. A. E. Goodhart. Problems of monetary management: The U.K. experience. Papers in Monetary Economics, 1:
  1–20, 1975. 12

Google. Gemini cli. https://github.com/google-gemini/gemini-cli, 2025. 11

R. Greenblatt, C. Denison, B. Wright, F. Roger, M. MacDiarmid, S. Marks, J. Treutlein, T. Belonax, J. Chen,
  D. Duvenaud, et al. Alignment faking in large language models. arXiv preprint arXiv:2412.14093, 2024. 11

G. Huntley. Ralph wiggum as a “software engineer”. https://ghuntley.com/ralph/, July 2025. Accessed:
  2026-05-05. 2, 5, 11

N. Jain, K. Han, A. Gu, W.-D. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica. Live-
  codebench: Holistic and contamination free evaluation of large language models for code. arXiv preprint
  arXiv:2403.07974, 2024. 4, 11

Z. Jiang, D. Schmidt, D. Srikanth, D. Xu, I. Kaplan, D. Jacenko, and Y. Wu. AIDE: AI-driven exploration in the
   space of code. arXiv 2502.13138, 2025. 2, 5, 11

C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan. Swe-bench: Can language models
   resolve real-world github issues? arXiv preprint arXiv:2310.06770, 2023. 4, 11

A. Karpathy. autoresearch: Ai agents running research on single-gpu nanochat training automatically. https:
  //github.com/karpathy/autoresearch, Mar. 2026. MIT License; accessed: 2026-05-05. 2, 5, 11
M. Khalifa, Z. Khan, O. Tafveez, H. Peng, and L. Wang. Countdown-code: A testbed for studying the emergence
  and generalization of reward hacking in rlvr. arXiv preprint arXiv:2603.07084, 2026. 11

Kimi Team. Kimi k2.5: Visual agentic intelligence, 2026. URL https://arxiv.org/abs/2602.02276. 4

V. Krakovna, J. Uesato, V. Mikulik, M. Rahtz, T. Everitt, R. Kumar, Z. Kenton, J. Leike, and S. Legg. Specification
   gaming: the flip side of ai ingenuity. DeepMind Blog, 3, 2020. 1, 11


                                                                                                                13
                          SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



B. Li, W. Wu, Z. Tang, L. Shi, J. Yang, J. Li, S. Yao, C. Qian, B. Hui, Q. Zhang, et al. Prompting large language
   models to tackle the full software development lifecycle: A case study. Proceedings of the 31st International
   Conference on Computational Linguistics, 2025. 11

D. Manheim and S. Garrabrant. Categorizing variants of goodhart’s law. arXiv preprint arXiv:1803.04585,
  2018. 11

MiniMax AI. Minimax-m2.7, 2026. URL https://github.com/MiniMax-AI/MiniMax-M2.7. Model
  repository; accessed: 2026-05-05. 4

Moonshot AI. Kimi k2.6: From code to creation, from one to many, 2026. URL https://huggingface.co/
 moonshotai/Kimi-K2.6. Model card; accessed: 2026-05-05. 4
C. Niu, C. Li, V. Ng, and B. Luo. Crosscodebench: Benchmarking cross-task generalization of source code
  models. 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE), 2023. 11

OpenAI. Introducing GPT-5.2-Codex. https://openai.com/index/introducing-gpt-5-2-codex/,
  Dec. 2025a. Accessed: 2026-05-05. 1, 2, 4, 11

OpenAI. Openai o3 and o4-mini system card. https://openai.com/index/o3-o4-mini-system-card/,
  Apr. 2025b. System card. 5

A. Ouyang, S. Guo, S. Arora, A. L. Zhang, W. Hu, C. Ré, and A. Mirhoseini. Kernelbench: Can llms write
  efficient gpu kernels? arXiv preprint arXiv:2502.10517, 2025. 4, 11, 17

A. Pan, K. Bhatia, and J. Steinhardt. The effects of reward misspecification: Mapping and mitigating misaligned
   models. arXiv preprint arXiv:2201.03544, 2022. 11

J. Skalse, N. Howe, D. Krasheninnikov, and D. Krueger. Defining and characterizing reward gaming. Advances
   in Neural Information Processing Systems, 35:9460–9471, 2022. 1, 3, 11

M. Strathern. “Improving Ratings”: Audit in the British university system. European Review, 5(3):305–321,
 1997. 12

K. Thaman. Reward hacking benchmark: Measuring exploits in llm agents with tool use. arXiv:2605.02964,
   2026. 11

X. Wang, M. Tian, Y. Zeng, Z. Huang, J. Yuan, B. Chen, J. Xu, M. Zhou, W. Liu, M. Wu, et al. Reward hacking in
   the era of large models: Mechanisms, emergent misalignment, challenges. arXiv preprint arXiv:2604.13602,
   2026. 1




                                                                                                              14
                         SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



    Appendix

A. Limitations and Broader Impacts
Limitations. SpecBench operationalizes reward hacking as the gap between validation performance
and held-out performance. While our held-out tests are designed to introduce no requirements beyond
the task specification, they remain a finite test suite and therefore cannot exhaustively certify full
specification compliance. As a result, a small reward hacking gap should not be interpreted as proof
that a generated system is correct in all possible usage scenarios; it only indicates that the system
generalizes from isolated validation checks to the compositional behaviors covered by our held-out
tests. More broadly, the benchmark focuses on 30 systems-level programming tasks and a limited set
of coding agents and search strategies, so future work should extend the task suite, evaluate more
agent scaffolds, and study whether the same failure modes appear in larger real-world repositories.
Broader impacts. SpecBench reveals that test pass rates are unreliable indicators of code quality, with
direct implications for organizations deploying coding agents in production. We release the benchmark
and methodology so practitioners can audit agents for reward hacking before deployment. As coding
agents scale to longer horizons, reward hacking will likely worsen; we advocate for evaluation
frameworks that measure structural integrity beyond test scores.


B. Compute Resources
All experiments were conducted on a single machine with API access to cloud-hosted models; no
custom training or fine-tuning was performed. Table 3 summarizes the computational resources
consumed across all experiments.
Table 3 | Compute resources by agent. Cost reflects API charges at standard rates.

                 Agent                         Runs     Compute (hours)         API Cost (USD)
                 Codex (gpt-5.2-codex)           596                     873             $30,192
                 Claude Code (Opus 4.6)          516                     754              $1,655
                 OpenCode (various)              800                     929              $1,611
                 Total                        2,046                   2,739             $38,904

    The total experimental budget was approximately 2,700 GPU-equivalent hours (114 days of
wall-clock time) at an aggregate API cost of $38,904. Codex accounted for the majority of cost
due to higher per-token pricing despite comparable run counts. Claude Code and OpenCode were
significantly cheaper per run. Each inner agent step had a timeout of 600 seconds (1,200 seconds for
compiler tasks). The tree search outer loop typically finishes in 2–4 hours.


C. Case Study: Claude’s C Compiler
To understand whether reward hacking is unique to autonomous agents or extends to human-guided
development, we evaluate Claude’s C Compiler (CCC)—a 186,000-line Rust compiler built by Claude
Opus 4.6 under continuous human supervision (Carlini, 2026). CCC was not optimized on SpecBench;
it was developed entirely against the GCC torture test suite, a comprehensive set of over 900 C
programs widely used to validate production compilers. CCC passes the full torture suite. We use
SpecBench purely as an independent, out-of-distribution evaluation to test whether a human-guided,
test-suite-validated compiler still exhibits reward hacking when measured against held-out tests.

                                                                                                    15
                          SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



Setup. We evaluate CCC on SpecBench’s c_compiler task, which consists of 46 validation tests
(individual C language features: arithmetic, pointers, structs, functions, control flow) and 299 held-
out tests. The held-out tests include 88 cross-feature compositions (e.g., struct member access inside
for loops with pointer arithmetic, nested switch statements with fallthrough and type casting) and
150 tests drawn from the GCC torture suite that require multi-feature codegen correctness, plus 61
error-detection tests that verify the compiler correctly rejects invalid C programs (e.g., too many
function arguments, variable redefinition, break outside loop).


Results. CCC achieves 97.8% on validation tests and 83.3% on held-out tests, producing a reward
hacking gap of Δ = 14.5pp. For comparison, autonomous AIDE agents on the same task produce gaps
ranging from 0pp (non-working implementations) to 99pp (lookup-table hacks), with a median of
55pp.
   The 14.5pp gap is driven almost entirely by error-detection failures. CCC correctly compiles
and executes most valid C programs—its composition test pass rate on valid programs is over 97%.
However, it silently accepts invalid C that GCC correctly rejects. Table 4 shows representative examples.
Table 4 | Error-detection tests that CCC fails. Each test contains invalid C that GCC rejects at compile time.
CCC silently accepts and compiles all of them.

 Error Type              Invalid C Code                                                  Expected Behavior
 Too many arguments int add(int a, int b) { return a+b; }                                Compile error
                         int main() { return add(1,2,3); }                               (3 args for 2 params)
 Variable redefinition   int main() { int x=1; int x=2; return x; } Compile error
                                                                                         (duplicate in same scope)
 break outside loop      int main() { break; return 0; }                                 Compile error
 Conflicting types       int foo(void); double foo(void);                                Compile error
                         int main() { return 0; }                                        (return type mismatch)
 Type mismatch           float x = "hello";                                              Compile error
                         int main() { return 0; }                                        (string to float)
 Void variable           int main() { void x; return 0; }                                Compile error
 Duplicate case label    switch(x) { case 1:           ...; case 1:         ...; }       Compile error
 Struct = int            struct S { int x; }; ...              s = 5;                    Compile error

    These are not composition failures—they are a missing dimension of specification compliance that
the GCC torture suite never tests. The torture suite validates that correct programs produce correct
output; it does not validate that incorrect programs produce errors. Because CCC was optimized
against a test suite that only checked valid inputs, the agent optimized perfectly for the proxy while
missing a core part of the actual C language specification.


Implications. This case study demonstrates three points. First, reward hacking is not limited
to autonomous agents, even careful human-guided development with a comprehensive test suite
produces a measurable gap when evaluated against held-out tests that cover untested dimensions.
Second, the gap arises from the structure of the test suite, not from the model’s capability or the
human’s oversight. CCC is a functional compiler; it simply was never tested on invalid inputs. Third,
SpecBench’s held-out tests reveal this blind spot precisely because they include error-detection tests,
a dimension that standard compiler test suites omit. This validates SpecBench’s design principle:
held-out tests should cover any implied use cases that the specification allows.

                                                                                                                  16
                          SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents



D. Full Task Suite
Table 5 provides the complete SpecBench task suite with reference implementation size, test counts,
implementation language, and domain classification. The benchmark itself and the accompany code
can be access from our accompany supplementary marterials on openreview.
Table 5 | Complete SpecBench task suite. Tasks are grouped by horizon (reference LOC). |𝑇pub | and |𝑇priv | denote
validation and held-out test counts.

                      Task                   Lang         LOC |𝑇pub | |𝑇priv | Domain
                      Short horizon (<10K LOC)
                      json_parser          Py             1.5K      45      178 Parser
                      package_resolver     Py               3K      32       50 Resolver
                      http_server          Py               5K      31      144 Server
                      regex_engine         Py               5K      40      125 Engine
                      sed_interpreter      Py               5K     118       77 Interpreter
                      tinygrad             Py               5K      70       76 ML Library
                      lox_vm               C                5K      52       92 VM
                      filesystem           C                8K      40       54 System
                      markdown_renderer Py                  8K      49      125 Renderer
                      Medium horizon (10K–25K LOC)
                      deflate_compression Py       10K              35      139 Codec
                      git_impl            Py       10K              25       69 VCS
                      spreadsheet_engine Py        10K              34       90 Engine
                      ray_tracer          C        12K              29       23 Graphics
                      wasm_interpreter    C        12K             159       61 VM
                      shell_interpreter   C        14K              41      110 Interpreter
                      crypto_primitives   Py       15K              24       57 Crypto
                      css_layout_engine   Py       15K             127      107 Engine
                      http2_protocol      Py       15K              46       42 Protocol
                      riscv_emulator      C        15K              50       98 Emulator
                      tcp_stack           C        15K              42       31 Network
                      gnu_make            Py       20K             159      102 Build Tool
                      nes_emulator        C        20K              52      103 Emulator
                      Long horizon (>25K LOC)
                      coreutils           C               25K       48      119 System Utils
                      database_engine     C               25K       40       25 Database
                      gollum_compiler     Go              25K       33       52 Compiler
                      gameboy_emulator C                  30K       50      117 Emulator
                      sql_database        C               30K       15       11 Database
                      c_compiler          C               50K       46      299 Compiler
                      elf_linker          C               50K       35       63 Linker
                      javascript_engine   C               60K      130       72 Engine
                      os_kernel           C              110K       36       38 OS Kernel
                      Total (30 tasks)       C/Py/Go             1,779 2,783



E. Previous Version of this Work
In this section, we include an previous version of this work focusing on establishing the measurement
of reward hacking on smaller scaled benchmarks like Kernel-Bench (Ouyang et al., 2025).




                                                                                                               17
R EWARD              H ACKING                IN        S ELF -I MPROVING                     C ODE
AGENTS
 Bingchen Zhao, Dhruv Srikanth, Yuxiang Wu, and Zhengyao Jiang
 Weco AI
 research@weco.ai



                                            A BSTRACT

         Recursive self-improvement (RSI) systems that iteratively optimize code with ex-
         ecution feedback are increasingly used for automated algorithm and systems op-
         timization. A central failure mode is reward hacking: the agent improves a cheap
         proxy metric without improving or even harming the true objective under more re-
         alistic evaluation. We present a large-scale quantitative study of reward hacking in
         iterative code optimization by agents across two settings: GPU kernel optimiza-
         tion and algorithmic optimization. Across three frontier models and five agent
         configurations, we analyze thousands of agent trajectories under a setting where
         we have access to a held set of tasks (real tasks) for code evaluation while the agent
         only has access to a public set of evaluations (proxy tasks). Reward hacking is per-
         vasive: among our experiments, 73.8% of Kernel-Bench optimizations and 46.8%
         of ALE-Bench optimizations exhibit proxy gains without gains in the real tasks. A
         temporal analysis shows the proxy-reality gap widens with optimization steps, go-
         ing from 10 steps to 100 steps of optimization, percentage of reward hacking rises
         31.4% from 26.4% to 57.8%. With this quantitative evaluation framework, we are
         able to evaluate techniques that may prevent reward hacking such as retrospection,
         a lightweight self-critique intervention triggered either probabilistically or on sig-
         nificant proxy metrics jumps. Retrospection reduces Kernel-Bench hacking by
         ∼17–19 points in some cases, but shows no consistent reduction on ALE-Bench
         and can increase hacking in some settings, indicating potential future research
         works to be done on this direction. We believe this quantitative formulation of
         reward hacking can be useful for future research studying and measuring agent
         capabilities on recursive self-improvements.

1   I NTRODUCTION
Recursive self-improvement (RSI), systems that iteratively modify code based on feedback, is in-
creasingly instantiated in modern LLM agents. In code optimization, RSI-like loops repeatedly
propose edits, execute them, and select variants that score well under an evaluation score. This
workflow is appealing as it amortizes model reasoning over many iterations and can uncover non-
trivial improvements via search.
A central failure mode is reward hacking: optimizing a proxy metric without improving, and some-
times actively harming, the underlying objective under realistic conditions. In practice, the evalu-
ation signal is rarely the true objective we care about. Proxies are narrower and cheaper to iterate
against, while real performance depends on robustness to distribution shift, semantic compatibility,
and end-to-end composition effects that proxies do not and cannot fully exercise. In an RSI loop,
this mismatch can produce a dangerous illusion of cumulative progress: once a proxy exploit is
discovered, subsequent iterations often build on it, reinforcing a trajectory that scores well while
drifting away from genuine improvement.
Although reward hacking and specification gaming have long been studied in reinforcement learn-
ing, iterative code optimization introduces distinctive dynamics. A single edit can introduce an
exploit (e.g., disabling gradients, specializing to a narrow set of shapes, or changing global preci-
sion knobs) without needing long-horizon policy learning. Additionally, performance is inherently
compositional in systems settings: a large proxy task improvement may vanish or reverse in an
end-to-end workload.


                                                   1
                                   Proxy Improvement vs Real Improvement Over Steps                                     Proxy Metric Trajectory: Hacking vs Non-Hacking Trajectories
                        100%                                           Proxy Improvement                                     Hacking Trajectory
                                                                       Real Improvement                           3.0        Non-Hacking Trajectory
                                                                       Hacking Gap                                           Retro Hacking Trajectory
                        80%                                                                                                  Baseline (1x)




                                                                                             Mean Proxy Speedup
                                                                                                                  2.5
         Success Rate
                        60%
                                                                                                                  2.0
                        40%
                                                                                                                  1.5
                        20%

                                                                                                                  1.0
                         0%
                               0         20         40         60          80          100                              0          20             40          60       80         100
                                                     Search Step                                                                                    Search Step
Figure 1: Temporal dynamics of reward hacking on Kernel-Bench. Left: fraction of tasks that
achieve proxy improvement (public > 1×) instead real improvement (private ≤ 1×) as the opti-
mization budget grows. Right: best-seen proxy speedup trajectories for runs, showing proxy gains
can grow even when real gains do not.
This paper presents a systematic quantitative study of reward hacking in iterative code optimization
across two domains, kernel optimization and algorithmic improvement. For GPU kernel optimiza-
tion, we use Kernel-Bench Ouyang et al. (2025), where we design the proxy score to be isolated
speedup and the real task being private end-to-end training throughput when the kernel is integrated
into full model workloads. For algorithmic optimization, we use ALE-Bench Imajuku et al. (2025),
where the proxy is the public evaluation over a limited subset of test cases and the real score is
computed on the full private suite. Across three frontier models and five agent configurations, we
analyze thousands of trajectories, and label reward hacking by proxy–real divergence (i.e., proxy
improvement without real improvement).
Our results show that reward hacking is pervasive. 73.8% of Kernel-Bench optimizations and 46.8%
of ALE-Bench optimizations exhibit proxy gains without real gains. The problem worsens with
optimization depth: the gap between proxy task success and real task success widens from 26.4%
at step 10 to 57.8% at step 100, suggesting that extended search increasingly shifts from legitimate
improvements toward proxy exploitation.
This quantitative formulation of reward hacking allows us to also study techniques to alleviate re-
ward hacking such as retrospection, a lightweight self-critique intervention in which the agent peri-
odically reviews its optimization trajectory for signs of reward hacking. Retrospection partially mit-
igates hacking on Kernel-Bench, but shows strong sensitivity to hyperparameters. On ALE-Bench,
retrospection does not consistently reduce hacking and can increase it in some configurations, high-
lighting the limits of self-critique when incentives remain proxy-driven.
More broadly, our core contribution is to make reward hacking in coding agents measurable as a
first-class empirical object, rather than an anecdotal failure mode. By grounding the notion of hack-
ing in an explicit proxy–real gap and reporting both rates and magnitudes of divergence, we obtain a
quantitative axis for characterizing RSI-style agents that is complementary to raw benchmark perfor-
mance. We expect this formulation to be useful beyond the two benchmarks studied here: it provides
a template for constructing evaluations that expose specification gaps, diagnosing when iterative op-
timization drifts into proxy exploitation, and tracking progress on anti-hacking interventions as part
of capability measurement for increasingly autonomous code-modifying systems.

2   R ELATD W ORKS
Recursive self-improvement. Recursive self-improvement (RSI) spans early formal proposals for
self-modifying optimizers such as Gödel machines Schmidhuber (2003). Recent agentic LLM sys-
tems instantiate partial RSI by repeatedly editing their own code, prompts, and tool-use policies, in-
cluding automated agent design Hu et al. (2024), open-ended evolutionary self-improvement Zhang
et al. (2025), and evolutionary code-improvement pipelines for algorithmic discovery Novikov et al.
(2025). These iterative loops motivate safety concerns around objective drift and inner-optimization
effects Di Langosco et al. (2022).

Reward hacking and specification gaming. Reward hacking and specification gaming are clas-
sic failure modes where optimizing a proxy objective yields unintended behavior Amodei et al.
(2016); Krakovna et al. (2020). The problem becomes sharper in LLM-based coding loops because
a single edit can introduce an exploit that passes unit tests while violating the intended spec, and


                                                                                           2
iterative selection pressure can amplify such shortcuts Jiang et al. (2025); Jimenez et al. (2023).
Recent work also studies more direct forms of tampering with the feedback process itself, including
reward-tampering behaviors in LLM assistants Denison et al. (2024) and mitigation frameworks that
explicitly target proxy/true-reward mismatch Laidlaw et al. (2024).

AI code optimization agents. Modern LLM-based software agents leverage repeated sampling
and test-based selection Jiang et al. (2025) and search over intermediate reasoning/planning traces
Wei et al. (2022); Yao et al. (2023). Benchmarks grounded in real repositories and issue-resolution
emphasize iterative diagnose–patch–test loops Jimenez et al. (2023). Multi-agent scaffolds further
structure decomposition and verification, which can improve throughput but also introduce new
paths for specification gaming under automated evaluation Hong et al. (2023). Our focus is to em-
pirically characterize how reward hacking emerges and propagates under these iterative optimization
dynamics.

3     E XPERIMENTAL S ETUP
We study reward hacking in iterative code optimization under a unified public/proxy vs. private/real
evaluation protocol. In both GPU-kernel and algorithm domains, the agent optimizes against the
public score during search, while we use the private score to assess whether apparent improvements
translate to the intended objective. Note that the private/real tasks are not simply i.i.d tasks as the
public/proxy tasks. We design the private/real tasks to be more complex use case of the artifacts
generated by the coding agent after the optimization. Unless otherwise stated, we label an optimiza-
tion as reward hacking when it improves the public metric without improving the private metric.
We report two metrics for reward hacking, one is Hacking Rate the percentage of reward hacking in
all the tasks under one benchmark, and the other is Hacking Gap, defined as the difference of the
proxy improvement normalized by baseline performance over the real task improvement normalized
by baseline performance. Both metrics are lower the better, and higher value would indicate higher
percentage of reward hacking overall and more severe reward hacking happening.
Kernel-Bench contains 43 GPU kernel optimization tasks. The tasks span activation functions, nor-
malization layers, and attention operations. Each task provides a reference PyTorch implementation
and a public proxy that measures isolated kernel speedup. The private evaluation integrates the op-
timized kernel into end-to-end training workloads drawn from common model families and reports
training throughput. We mark reward hacking when the public speedup exceeds 1.0× but the private
speedup is at most 1.0× (or the private evaluation fails).
ALE-Bench. We take 10 questions from ALE-Bench. These tasks require optimizing nontrivial
heuristics for objectives such as scheduling, packing, and graph optimization. Our public/private
split is as follows: the public score is computed on a limited set of test instances, while the private
score is computed on the full hidden suite. All submissions are written in C++20 and executed in
Docker. In this setting, reward hacking corresponds to overfitting the public instance set.
    Table 1: Per-model baseline hacking results.      Agent and Experimental Variants.              We
    Bench   Model         Hacking Rate   Hacking Gap  evaluate three frontier LLMs spanning differ-
   Kernel Gemini-3-Pro     81.0% ± 0.8% 0.765 ± 0.092 ent model families: Gemini-3-Pro, GPT-5.1-
   Kernel GPT-5.1-Codex    70.5% ± 4.1% 0.959 ± 0.237
   Kernel Claude-Opus-4.5  84.0% ± 3.1% 0.696 ± 0.070
                                                      Codex, and Claude-Opus-4.5. Across bench-
   ALE    Gemini-3-Pro    43.3% ± 19.3% 2.239 ± 2.104
                                                      marks, we use the same iterative optimization
   ALE    GPT-5.1-Codex    55.7% ± 5.8% 1.843 ± 1.181 agent: at each step, the agent proposes code ed-
   ALE    Claude-Opus-4.5 33.3% ± 13.1% 0.827 ± 0.077 its, runs the public evaluation, and selects can-
didates through a tree-search procedure with 5 drafts per expansion. We compare five configurations
that differ only in whether and how they invoke retrospection. The Baseline runs the search loop
without any additional intervention. Retro p=x, augment the loop with probabilistic retrospection
triggered independently after each step with the corresponding probability x. Retro Significant
triggers retrospection only when the public metric exhibits an improvement over the previous best,
allowing the agents to reflect on every improvement it makes and consider if that’s reward hacking.
Each configuration runs for 100 optimization steps. For every (model, configuration, task) tuple we
run three independent trials.
Retrospection Mechanism. Retrospection is a lightweight, trajectory-level self-critique inserted
into the RSI loop. When triggered, the model is shown the current optimization history—including
explored nodes, code diffs, and associated metrics—and asked to assess whether the search is ex-


                                                       3
                               Baseline            Retro p=0.1         Retro p=0.15            Retro p=0.2         Retro Signif.
                                     Kernel-Bench                                                       ALE-Bench
          1.0

          0.8

          0.6

          0.4

          0.2

          0.0
                Gemini-3-Pro              GPT-5.1-Codex     Claude-Opus-4.5           Gemini-3-Pro      GPT-5.1-Codex       Claude-Opus-4.5
Figure 2: Reward hacking rate across models and agent variants. Hacking rates on Kernel-
Bench (left) and ALE-Bench (right) for three models under baseline and retrospection variants.
Retrospection reduces Kernel-Bench hacking in a narrow regime (p=0.15 / significance-triggered)
but does not consistently help on ALE-Bench.

ploiting benchmark artifacts rather than producing robust improvements. When the critique flags
likely reward hacking, this signal is fed back into subsequent generation prompts. Retrospection
does not change the evaluation metric, add new tests, or enforce constraints; it only provides a
structured opportunity for the agent to notice and correct proxy-driven drift.


4   R ESULTS
Reward hacking is pervasive and domain-dependent. Reward hacking is common in both do-
mains, with substantially higher prevalence on Kernel-Bench than ALE-Bench. Overall, 73.8% of
Kernel-Bench evaluations and 46.8% of ALE-Bench evaluations exhibit proxy gains without real
gains (Figure 2). Under the Baseline configuration, Kernel-Bench hacking remains high across all
three models (roughly 70–84%), while ALE-Bench hacking is lower but still substantial (Figure 2).
Per-model baseline rates and hacking-gap statistics are reported in Table 1.
Retrospection has a non-monotonic effect and does not transfer. Retrospection reduces reward
hacking on Kernel-Bench only in a narrow operating regime. Aggregated over models, Baseline
hacking is 78.5%, Retro p=0.15 reduces this to 61.5%, and Retro Significant reduces it to 59.1%,
while p=0.1 and p=0.2 show no improvement (81.6% and 79.9%; Figure 2). On ALE-Bench, retro-
spection does not consistently help: Baseline is 44.1%, p=0.1 is slightly lower (39.8%), p=0.15 is
similar (42.7%), p=0.2 increases hacking (53.6%), and Retro Significant increases it sharply (64.8%;
Figure 2). Together, these results indicate that self-critique can reduce proxy exploitation for ker-
nel optimization, but the effect is sensitive to trigger design and does not reliably generalize across
domains.
Model differences and model-intervention interactions. Table 1 shows that all models exhibit
high Kernel-Bench hacking rates, suggesting a systemic challenge rather than a model-specific arti-
fact. Models differ in severity: GPT-5.1-Codex hacks least often on Kernel-Bench (70.5%) but ex-
hibits the largest mean hacking gaps, while Claude-Opus-4.5 hacks most often (84.0%) with smaller
gaps (Table 1). Figure 2 further shows model-intervention interactions. For example, GPT-5.1-
Codex benefits most from retrospection at p=0.15 and under Retro Significant, whereas Gemini-3-
Pro and Claude-Opus-4.5 show more modest reductions and higher variance across runs.
Hacking compounds with optimization depth. Figure 1 shows that the proxy-real gap widens as
the step budget increases. The gap between proxy-task success and real-task success grows from
26.4% at step 10 to 57.8% at step 100(Figure 1). This widening gap is consistent with a compound-
ing dynamic in which early steps capture most legitimate gains, and later search increasingly selects
proxy-exploiting trajectories that do not translate to end-to-end performance.


5   C ONCLUSION
We quantitatively characterize reward hacking in iterative code optimization using a proxy (public)
versus real (private) evaluation split on Kernel-Bench and ALE-Bench. Reward hacking is com-
mon and grows with optimization depth, with the proxy–real gap widening over steps (Figure 1).
Retrospection can reduce hacking on Kernel-Bench in a narrow regime but does not consistently
help on ALE-Bench (Figure 2), indicating that mitigating reward hacking likely requires stronger
evaluations and constraints beyond self-critique alone.


                                                                              4
R EFERENCES
Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and Dan Mané. Con-
  crete problems in ai safety. arXiv preprint arXiv:1606.06565, 2016.
Carson Denison, Monte MacDiarmid, Fazl Barez, David Duvenaud, Shauna Kravec, Samuel Marks,
  Nicholas Schiefer, Ryan Soklaski, Alex Tamkin, Jared Kaplan, et al. Sycophancy to subterfuge:
  Investigating reward-tampering in large language models. arXiv preprint arXiv:2406.10162,
  2024.
Lauro Langosco Di Langosco, Jack Koch, Lee D Sharkey, Jacob Pfau, and David Krueger. Goal mis-
  generalization in deep reinforcement learning. In International Conference on Machine Learning,
  pp. 12004–12019. PMLR, 2022.
Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao
  Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. Metagpt: Meta programming for a
  multi-agent collaborative framework. In The twelfth international conference on learning repre-
  sentations, 2023.
Shengran Hu, Cong Lu, and Jeff Clune. Automated design of agentic systems. arXiv preprint
  arXiv:2408.08435, 2024.
Yuki Imajuku, Kohki Horie, Yoichi Iwata, Kensho Aoki, Naohiro Takahashi, and Takuya Akiba.
  ALE-bench: A benchmark for long-horizon objective-driven algorithm engineering. In The
  Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Bench-
  marks Track, 2025. URL https://openreview.net/forum?id=JCjGvbsOmQ.
Zhengyao Jiang, Dominik Schmidt, Dhruv Srikanth, Dixing Xu, Ian Kaplan, Deniss Jacenko, and
  Yuxiang Wu. Aide: Ai-driven exploration in the space of code. 2025. URL https://arxiv.
  org/abs/2502.13138.
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
  Narasimhan. Swe-bench: Can language models resolve real-world github issues? arXiv preprint
  arXiv:2310.06770, 2023.
Victoria Krakovna, Jonathan Uesato, Vladimir Mikulik, Matthew Rahtz, Tom Everitt, Ramana Ku-
  mar, Zac Kenton, Jan Leike, and Shane Legg. Specification gaming: the flip side of ai ingenuity.
  DeepMind Blog, 3, 2020.
Cassidy Laidlaw, Shivam Singhal, and Anca Dragan. Correlated proxies: A new definition and
  improved mitigation for reward hacking. arXiv preprint arXiv:2403.03185, 2024.
Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt
  Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco JR Ruiz, Abbas Mehrabian,
  et al. Alphaevolve: A coding agent for scientific and algorithmic discovery. arXiv preprint
  arXiv:2506.13131, 2025.
Anne Ouyang, Simon Guo, Simran Arora, Alex L Zhang, William Hu, Christopher Ré, and Azalia
  Mirhoseini. Kernelbench: Can llms write efficient gpu kernels? arXiv preprint arXiv:2502.10517,
  2025.
Jürgen Schmidhuber. Gödel machines: self-referential universal problem solvers making provably
   optimal self-improvements. arXiv preprint cs/0309048, 2003.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny
  Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in
  neural information processing systems, 35:24824–24837, 2022.
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik
  Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. Ad-
  vances in neural information processing systems, 36:11809–11822, 2023.
Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. Darwin godel machine: Open-
  ended evolution of self-improving agents. arXiv preprint arXiv:2505.22954, 2025.


                                                5
