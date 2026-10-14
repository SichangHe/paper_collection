                                                                Putnam 2025 Problems in Rocq
                                                                using Opus 4.6 and Rocq-MCP


                                                              Guillaume Baudart                             Marc Lelarge
                                                     IRIF, Université Paris Cité, Inria, CNRS         DI ENS, PSL University, Inria
arXiv:2603.20405v2 [cs.LG] 21 May 2026




                                                          Tristan Stérin                            Jules Viennot
                                                           PRGM DEV                     IRIF, Université Paris Cité, Inria, CNRS



                                                                                       Abstract

                                                     We report on an experiment in which Claude Opus 4.6, equipped with a suite of
                                                     Model Context Protocol (MCP) tools for the Rocq proof assistant, autonomously
                                                     proved 10 of 12 problems from the 2025 Putnam Mathematical Competition. The
                                                     MCP tools, designed with Claude by analyzing logs from a prior experiment on
                                                     miniF2F-Rocq, encode a compile-first, interactive-fallback strategy. Running on
                                                     an isolated VM with no internet access, the agent deployed 141 subagents over
                                                     17.7 hours of active compute (51.6h wall-clock), consuming approximately 1.9
                                                     billion tokens. All proofs are publicly available.1


                                         1       Introduction

                                         The Putnam Mathematical Competition is one of the most prestigious undergraduate mathematics
                                         contests in North America. Until recently, LLM-based theorem proving relied primarily on models
                                         specialized for a single proof assistant. DeepMind’s AlphaProof [AlphaProof and AlphaGeometry
                                         teams, DeepMind, 2024] pioneered this formal approach, reaching silver-medal level at the 2024 IMO
                                         using reinforcement learning in Lean. Since then, specialized provers, e.g., DeepSeek-Prover [Xin
                                         et al., 2024; Ren et al., 2025], Kimina-Prover [Wang et al., 2025], Goedel-Prover [Lin et al., 2025],
                                         SeedProver [Chen et al., 2025], and Aristotle [Achim et al., 2025], have pushed performance further,
                                         with Aristotle achieving gold-medal level at the 2025 IMO. All these systems target Lean and rely on
                                         fine-tuning or reinforcement learning. A striking recent shift is the emergence of agentic approaches
                                         built on general-purpose frontier models: Numina-Lean-Agent [Project Numina, 2025] solved all 12
                                         Putnam 2025 problems in Lean by pairing Claude with an MCP-based tool server. This pivot from
                                         specialized models to tool-augmented frontier agents has an important consequence for proof-assistant
                                         diversity. Unlike fine-tuned provers that are heavily trained on Lean code, general-purpose frontier
                                         models have no strong bias toward any single proof language, and their mathematical reasoning is
                                         largely decoupled from the target formalism. The gap between proof assistants therefore narrows
                                         considerably. Our experiment tests this hypothesis on Rocq (formerly Coq), a proof assistant that has
                                         received far less attention from the LLM community than Lean.
                                         We present a case study in which Claude Opus 4.6 [Anthropic, 2025a], orchestrated by Claude
                                         Code [Anthropic, 2025b], formally verified Putnam 2025 problems in Rocq using rocq-mcp [team],
                                         a set of eight MCP tools [Anthropic, 2024] developed with Claude using feedback from a prior
                                         experiment on the miniF2F-Rocq dataset [Viennot et al., 2025]. The Putnam statements were
                                         autoformalized from Numina’s [Project Numina, 2025] and Axiom’s [Axiom Math, 2025] Lean
                                         versions, combined with natural-language statements from the Putnam archive [Kedlaya].
                                             1
                                                 https://github.com/LLM4Rocq/Putnam2025-Rocq


                                         Preprint.
Contamination risk. The experiment ran on an isolated VM with web search disabled. Although
Lean solutions exist on GitHub, they were released in December 2025, after the model’s training
cutoff of May 2025.

Outline. In Section 2, we describe the design of rocq-mcp tools, motivated by empirical analysis of
miniF2F logs. In Section 3, we report quantitative results on Putnam 2025: 10/12 solved, with per-
problem breakdowns. In Section 4, we use Claude to perform an in-depth analysis of the experiment
logs, covering tool use, multi-agent orchestration, scaling, and failure modes.


2     Background and Experimental Setup

2.1   The rocq-mcp Toolchain

The rocq-mcp server [team] exposes eight MCP tools organized in two tiers.
Compilation tools (require only coqc):

       • rocq_compile: Full-file compilation with structured error reporting, including source-line
         annotations and caret underlines for error positions. This is the primary verification method:
         81% of miniF2F proofs succeeded via direct compilation alone.
       • rocq_verify: Since LLM-generated code cannot be trusted, the proof is wrapped inside a
         Rocq module, isolating it from the rest of the file. The tool then attempts to prove the original
         theorem statement by applying the theorem proved inside the module. This sandboxing
         prevents the LLM from silently redefining the problem statement or using Admitted. A
         whitelist of standard axioms filters out proofs that rely on custom axioms.
       • rocq_auto_solve: Attempts standard automation tactics (auto, lia, lra, ring, field,
         etc.) as a quick check before manual construction.

Interactive tools (require pet from coq-lsp [Contributors, a]):

       • rocq_query: Run Search, Check, Print, or About commands for library exploration.
       • rocq_step / rocq_step_multi: Execute tactics interactively; step_multi tests up to 20
         tactics in parallel without advancing the session.
       • rocq_toc / rocq_notations: File structure and notation resolution queries.

These tools encode a compile-first, interactive-fallback strategy identified through miniF2F log
analysis: the agent writes a complete proof file, compiles it, iterates on errors, and only falls back to
interactive stepping for debugging specific subgoals.

2.2   Tool Design from miniF2F Analysis

Prior to the Putnam experiment, we ran Claude Opus 4.6 on the miniF2F-Rocq benchmark [Viennot
et al., 2025] (244 test theorems) with only the Rocq compiler as a tool. Of the 244 theorems, 198
(81%) were correctly proved: the agent wrote a complete proof file that compiled and passed manual
verification. The remaining 46 failures fell into categories that each motivated a specific tool:

       • Invalid proofs (20/46): 14 proofs used Admitted and 6 exploited type redefinition to bypass
         the theorem statement. These compiled without errors but were mathematically invalid,
         motivating a sandboxing mechanism and an axiom whitelist in rocq_verify.
       • Incomplete proofs (15/46): Proofs with open subgoals that the agent could not detect from
         compiler output alone, motivating the interactive rocq_step tool for goal inspection.
       • Other failures (11/46): Timeouts, type errors, and import issues. Across all failures, the
         agent struggled to locate errors from raw coqc output, often compiling entire .v files just to
         run Search commands, motivating rocq_query. Scope ambiguity (e.g., + in nat_scope
         vs Z_scope) caused silent type errors, motivating rocq_notations.


                                                    2
Table 1: Per-problem results. Lines = lines of Rocq code. Time = wall-clock from experiment start to
successful compilation. ✓ = exploited a loophole in the A3 formalization (later fixed by the agent).
Bold None = fully constructive (zero axioms).

                Problem    Status   Lines       Time    Axioms      Domain
                A1           ✓        305       51m     classical   Number theory
                A2           ✓        308    1h 33m       Reals     Real analysis
                A3           ✓        110    1h 07m       None      Combinatorics
                A4           ✓        531    4h 58m       Reals     Linear algebra
                A5           ✗       2294         –         –       Enum. combinatorics
                A6           ✓        897   19h 56m       None      Number theory
                B1           ✓        570    1h 48m       Reals     Geometry
                B2           ✓        513    5h 13m       Reals     Real analysis
                B3           ✓        439   15h 21m       None      Number theory
                B4           ✓        414    3h 46m       None      Combinatorics
                B5           ✓       1455   46h 01m       None      Number theory
                B6           ✗       1160         –         –       Analysis



2.3   Experimental Protocol

The Putnam 2025 problems were autoformalized from Numina’s [Project Numina, 2025] and Ax-
iom’s [Axiom Math, 2025] Lean versions, combined with natural-language statements from the
Putnam archive [Kedlaya]. Each problem is a standalone .v file containing definitions and a Theorem
putnam_2025_XX : ... Admitted. stub.
The experiment ran on a Docker container with Rocq 9.0, the rocq-mcp server, and large math libaries
(Coquelicot [Contributors, b], math-comp [Contributors, c], and math-comp-analysis [MathComp
Analysis Contributors]) installed. Web search was disabled. The user prompt was:

         Launch an agent team with an expert mathematician, an expert computer scientist,
         an expert in formal verification (Coq/Rocq), and a devil’s advocate. Your goal is to
         solve the 12 theorems in this directory.

Claude Code (orchestrating Claude Opus 4.6) ran autonomously for approximately 3 days, with
human intervention limited to resuming sessions after container crashes and rate-limit pauses.

3     Results
The agent solved 10 of 12 problems, producing a total of 5,542 lines of verified Rocq code (Table 1).
However, the A3 proof exploited a loophole in the problem formalization rather than proving the
intended mathematical statement; it was later fixed by the agent in a separate session (see Section 5).
Five proofs are fully constructive (A3, A6, B3, B4, B5): they use no axioms. The remaining solved
proofs use standard mathematical axioms (classical logic, Dedekind Reals).

4     Analysis
4.1   How effective are the MCP tools?

Across the experiment, the agent made 12,427 tool calls. The MCP tools accounted for approximately
30% of all calls, with rocq_compile being the dominant verification method (Table 2).
Compile-first confirmed. Every successful proof was ultimately verified via rocq_compile or
direct coqc invocation. The compile-iterate loop (write proof → compile → fix errors → repeat) was
the universal workflow. Across all problems, compile success rates ranged from 46% (A1) to 58%
(A3), with a median of ∼50%, meaning roughly half of compilation attempts produced errors that the
agent then fixed.
rocq_auto_solve is insufficient for Putnam. Standard automation never solved a Putnam problem:
these require non-trivial mathematical insight, not tactic search. However, rocq_auto_solve


                                                  3
                                           12                                                                                  12 total


              Cumulative problems solved
                                                                                                                     B5
                                           10                                 A6
                                                                    B3
                                            8             B2
                                            6            A4
                                                       B4
                                            4    B1
                                                 A2
                                            2   A3                                           Active
                                                A1                                           Inactive (rate limit / sleep)
                      0
                       8:00    0:00    6:00    2:00    8:00    0:00    6:00    2:00     8:00
               a r 09 1 ar 10 0 ar 10 0 ar 10 1 ar 10 1 ar 11 0 ar 11 0 ar 11 1 ar 11 1
             M           M       M       M       M       M       M       M       M
                                                                              Time (UTC)
Figure 1: Cumulative problems solved over wall-clock time. Solid green segments indicate active
compute; dashed red segments indicate inactivity (API rate limits or user absence). Shaded regions
mark the 7 detected gaps (>30 min). The first 4 problems were solved within 2 hours; B5 was not
solved until 46 hours into the experiment.



                             12
Cumulative problems solved




                                                                                                                                    B5
                             10                                                                                           A6
                                                                                                                B3
                                    8                                                                   B2
                                                                                                  A4
                                    6                                               B4
                                    4
                                                                               B1
                                                               A3        A2
                                    2             A1
                                    0
                                                108                                                            109
                                                                    Cumulative tokens (log scale)
Figure 2: Cumulative problems solved vs. cumulative tokens consumed (log scale). The first 5
problems required ∼100M tokens; the last 5 required ∼10× more, illustrating sharp diminishing
returns on harder problems.



remains useful for simpler problems because it provides a fast, zero-cost baseline before engaging
the LLM: it solves 53/244 (22%) of miniF2F-Rocq test problems.
All proofs were double-checked with rocq_verify. All 10 solved proofs pass verification with
only standard axioms (classical logic, Dedekind Reals, functional extensionality). However, the
module sandbox caused false negatives on two problems (A3, B1) where custom inductive types
could not unify across the module boundary. A two-phase strategy was later added to rocq-mcp [team]
to handle this case.


                                                                                         4
                                      Table 2: MCP tool usage.

                           Tool                    Calls     Role
                           rocq_compile          ∼3,100      Compilation
                           rocq_verify            ∼120       Axiom checking
                           rocq_auto_solve         ∼20       Quick automation
                           rocq_query              ∼80       Library search
                           rocq_step              ∼450       Interactive debug


            Table 3: Subagent roles. Roles are inferred from each agent’s initial prompt.

                           Role               Agents       Tokens   Tool calls
                           Lemma Prover           55        738M        4,845
                           Bug Fixer              36        538M        3,409
                           General                21        253M        1,588
                           Verifier               15         65M          639
                           Proof Completer        13        185M        1,257
                           Compiler                1          1M           14
                           Total                 141       1,780M      11,752



Interactive tools see targeted use. rocq_step was used almost exclusively on the three hardest
problems (A5, B5, B6), where the agent needed to understand specific proof states. For the other
nine problems, compile-first sufficed.

4.2   How does the multi-agent architecture perform?

The orchestrator launched 4 parallel teams of 3 problems each, then spawned a total of 141 subagents
over the experiment. The architecture was strictly two-level: one orchestrator managing worker
subagents (no sub-subagent spawning observed).
Initial burst. The parallel dispatch was highly effective: 4 problems solved in 1.8h, 7 in 5.2h
(Figure 1).
Specialized follow-up. After the initial teams completed, the orchestrator spawned targeted agents
classified by role (Table 3). Lemma Provers (55 agents, 738M tokens) dominated, reflecting the
proof-by-subgoal strategy: once an overall structure was established, the hard work was proving
specific lemmas. Bug Fixers (36 agents) handled compile-error repair, while Proof Completers (13
agents) filled in incomplete proof skeletons. Verifiers (15 agents) were used to check axiom-freeness
and eliminate unnecessary Admitted stubs.
Diminishing returns on hard problems. B5 received 82+ subagents and B6 received 91, yet many
agents attempted the same core mathematical difficulty without fundamentally new approaches. An
early-termination strategy that detects when multiple agents fail at the same bottleneck could save
substantial resources.
Mathematical hints matter. Each subagent received multi-paragraph mathematical proof strategies
in its prompt. These hints (e.g., the two-region strategy for A2’s upper bound, the equilateral triangle
construction for B1) were critical for directing the search. Notably, these hints were generated by the
orchestrator LLM itself, not by a human.

4.3   How do costs scale with problem difficulty?

The experiment consumed approximately 1.9 billion tokens at an estimated API cost of $1,760
(Table 4).
Output tokens dominate cost. Despite being only 0.9% of token volume, output tokens account
for 23.1% of cost at $25/M, reflecting hundreds of lines of proof code and extended mathematical
reasoning per problem. Cache reads account for the largest share of cost (51.4%) despite their low
per-token price ($0.50/M), simply due to volume: 95.4% of all tokens are cache reads.


                                                   5
                                A2    A6         B4
                                A3    B1         B5
                                A4    B2         B6
                                A5    B3
Tool calls (log scale)


                         102




                         101
                                           106                                 107               108
                                                          Total tokens (log scale)
Figure 3: Subagent efficiency. Each bubble represents one subagent (141 total, filtered to those with
>10 tool calls). Position: tokens consumed vs. tool calls (both log scale). Size: duration. Color:
problem assignment.

                                                      Table 4: Token economics.
                                       Category           Tokens          %     Cost    % Cost
                                       Input               <1M          0.0%      $1      0.1%
                                       Output               16M         0.9%    $406     23.1%
                                       Cache creation       72M         3.8%    $448     25.5%
                                       Cache read        1,809M        95.4%    $905     51.4%
                                       Total             1,897M        100%    $1,760    100%



Sharp diminishing returns. The first 5 problems consumed a small fraction of total tokens; the
remaining 5 consumed the vast majority (Figure 2). Table 5 details the budget distribution across
difficulty groups.
Active time vs. wall-clock. Only 17.7h of the 51.6h wall-clock was active compute. The remaining
33.8h consisted of 7 inactivity gaps caused by API rate limits and user absence.


5                        Discussion

The compile-first paradigm. On the Putnam 2025 problems considered here, the compile-first
strategy was sufficient: the compiler provides precise error messages, and the agent can write and
revise complete proof files in a single pass. Interactive stepping was only useful for debugging
specific subgoals, not for proof discovery. This aligns with our miniF2F findings: 81% of proofs
succeeded without any interactive tools. Whether this holds for more complex formalization tasks
involving large libraries remains an open question.
Cost efficiency. Prompt caching reduced costs by 5.6×. The sharp scaling wall, where unsolved
problems consume disproportionate resources, suggests that better difficulty estimation and early
termination could significantly improve cost efficiency.
Formalization quality matters: the A3 case. Problem A3 is a combinatorial game: two players
alternate moves and the player with no legal move loses. The initial autoformalization modeled


                                                                   6
Table 5: Scaling behavior by problem difficulty. The unsolved problems consumed the most resources.

                  Group                      Problems    Active time   Est. tokens
                  Easy (A1, A2, A3, B4)              4         < 2h        ∼100M
                  Medium (A4, B1, B2, B3)            4          ∼5h        ∼400M
                  Hard (A6, B5)                      2         ∼11h        ∼600M
                  Unsolved (A5, B6)                  2            –        ∼800M



strategies as partial functions (option state). This encoding had a loophole: the strategy “never
move” is vacuously compatible with any game, so the agent proved Bob wins with a mathematically
trivial argument in 1 h 07 m. When asked to close this loophole, the agent spent ∼9 h attempting to
prove the strengthened statement before concluding the encoding was fundamentally flawed. We
then pointed the agent to an alternative formalization from AxiomProver [Axiom Math, 2025], where
the current player must exhibit a valid move, which closes the loophole by construction. The agent
translated the formalization from Lean to Rocq and found a correct, fully constructive proof in ∼1 h.
This episode illustrates both a strength and a risk of the agentic approach: agents can detect and
exploit formalization gaps, but closing them may require human guidance on the problem encoding.

6   Conclusion
Claude Opus 4.6, equipped with empirically designed MCP tools and a compile-first multi-agent
workflow, solved 10 of 12 Putnam 2025 problems in Rocq. This result, achieved with a proof assistant
that has received far less LLM attention than Lean, suggests that tool-augmented frontier agents
can operate effectively across proof systems without language-specific training. The A3 episode
highlights that formalization quality is a first-class concern in agentic proving: agents can exploit
gaps in problem encodings, and closing those gaps sometimes requires human guidance. All proofs
and the rocq-mcp toolchain are publicly available [team, 2026; team].

References
Tudor Achim, Alex Best, Kevin Der, Mathïs Fédérico, Sergei Gukov, Daniel Halpern-Leister, Kirsten
  Henningsgard, Yury Kudryashov, Alexander Meiburg, Martin Michelsen, Riley Patterson, Eric
  Rodriguez, Laura Scharff, Vikram Shanker, Vladmir Sicca, Hari Sowrirajan, Aidan Swope, Matyas
  Tamas, Vlad Tenev, Jonathan Thomm, Harold Williams, and Lawrence Wu. Aristotle: IMO-level
  automated theorem proving. arXiv preprint arXiv:2510.01346, 2025.

AlphaProof and AlphaGeometry teams, DeepMind. AI achieves silver-medal standard solving In-
  ternational Mathematical Olympiad problems. https://deepmind.google/discover/blog/
  ai-solves-imo-problems-at-silver-medal-level/, 2024.

Anthropic. Model context protocol. https://modelcontextprotocol.io/, 2024.

Anthropic. Claude Opus 4.6.          https://docs.anthropic.com/en/docs/about-claude/
  models, 2025a.

Anthropic. Claude code: Anthropic’s agentic coding tool. https://docs.anthropic.com/en/
  docs/claude-code, 2025b.

Axiom Math. AxiomProver at Putnam 2025. https://github.com/AxiomMath/Putnam2025,
  2025.

Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
  Xing Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun,
  Jiahui Wang, Siran Wang, Zhihong Wang, Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu,
  Yihang Xia, Huajian Xin, Fan Yang, Huaiyuan Ying, Hongyi Yuan, Zheng Yuan, Tianyang Zhan,
  Chi Zhang, Yue Zhang, Ge Zhang, Tianyun Zhao, Jianqiu Zhao, Yichi Zhou, and Thomas Hanwen
  Zhu. Seed-prover: Deep and broad reasoning for automated theorem proving. arXiv preprint
  arXiv:2507.23726, 2025.


                                                 7
Coq-LSP Contributors. coq-lsp: Language server protocol for rocq. https://github.com/
  ejgallego/coq-lsp, a.
Coquelicot Contributors. Coquelicot: A user-friendly library of real analysis for Coq. https:
  //gitlab.inria.fr/coquelicot/coquelicot, b.
MathComp Contributors.       Mathematical components.        https://github.com/math-comp/
 math-comp, c.
Kiran S. Kedlaya. The William Lowell Putnam mathematical competition archive. https://
  kskedlaya.org/putnam-archive/.
Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
  Xia, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover: A frontier model for open-source
  automated theorem proving, 2025.
MathComp Analysis Contributors. Mathematical components analysis. https://github.com/
 math-comp/analysis.
Project Numina.  Numina putnam 2025 lean formalization.                   https://github.com/
  project-numina/Numina-Putnam2025, 2025.
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
   Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu,
  Wenjun Gao, Daya Guo, and Chong Ruan. DeepSeek-Prover-V2: Advancing formal mathematical
   reasoning via reinforcement learning for subgoal decomposition. arXiv preprint arXiv:2504.21801,
   2025.
LLM4Rocq team. rocq-mcp: MCP server for Rocq proof development. https://github.com/
  LLM4Rocq/rocq-mcp.
LLM4Rocq team. Putnam 2025 formal proofs in Rocq. https://github.com/LLM4Rocq/
  Putnam2025-Rocq, 2026.
Jules Viennot, Guillaume Baudart, Emilio Jesús Gallego Arias, and Marc Lelarge. MiniF2F in Rocq:
  Automatic translation between proof assistants. arXiv preprint arXiv:2503.04763, 2025.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
  Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey,
  Chendong Song, Chenjun Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei Liu,
  Jonas Bayer, Julien Michel, Longhui Yu, Léo Dreyfus-Schmidt, Lewis Tunstall, Luigi Pagani,
  Moreira Machado, Pauline Bourigault, Ran Wang, Stanislas Polu, Thibaut Barroyer, Wen-Ding Li,
 Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu, Zihan Wang, Zhilin Yang, Zhengying Liu,
  and Jia Li. Kimina-Prover Preview: Towards large formal reasoning models with reinforcement
  learning. arXiv preprint arXiv:2504.11354, 2025.
Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
  and Xiaodan Liang. DeepSeek-Prover: Advancing theorem proving in LLMs through large-scale
  synthetic data. In NeurIPS 2024 Workshop on Mathematical Reasoning, 2024.




                                                8
