                                         Agentic AI in the Software Development Lifecycle                                                                  Page 1




                                                  Agentic AI in the Software Development Lifecycle:
                                              Architecture, Empirical Evidence, and the Reshaping of Software Engineering

                                                                                     Happy Bhati
                                                                   Northeastern University · Boston, Massachusetts, USA
                                                                               bhati.h@northeastern.edu

                                             Abstract. The arrival of large language models (LLMs) capable of multi-step reasoning, tool use, and
                                             long-horizon planning has produced a qualitative shift in software engineering. Where earlier code-completion
                                             tools such as GitHub Copilot operated at the granularity of a line or function, modern agentic systems—
                                             Claude Code, OpenAI Codex CLI, Google Jules, Devin, OpenHands, SWE-agent, MetaGPT, ChatDev, and
arXiv:2604.26275v1 [cs.SE] 29 Apr 2026




                                             DeepMind’s AlphaEvolve—operate at the granularity of a repository, a feature, or an algorithm. We synthesize
                                             work from Anthropic, OpenAI, Google DeepMind, Microsoft Research, Princeton, Stanford, and the broader
                                             academic community to characterize this transition. We propose a six-layer reference architecture for agentic
                                             software engineering systems, contrast a traditional Software Development Lifecycle (SDLC) with an emerging
                                             Agentic SDLC (A-SDLC), and consolidate empirical evidence on performance (a rise from 1.96% to 78.4% on
                                             SWE-bench Verified between October 2023 and April 2026), productivity (13.6%–55.8% time savings across
                                             controlled studies), and labor-market impact (49% of jobs sampled by Anthropic in 2026 saw AI used for at
                                             least a quarter of their tasks). We argue that the central object of inquiry has shifted from code generation to
                                             delegated execution under human supervision, and we identify five open problems—evaluation, governance,
                                             technical debt, skill redistribution, and the economics of attention—that will determine whether the agentic
                                             transition is net-positive for the discipline. This paper is intended as both a synthesis for practitioners and a
                                             research agenda for the field.
                                             Keywords: agentic AI, large language models, software engineering, SDLC, autonomous agents, SWE-bench,
                                             developer productivity, multi-agent systems, human–AI collaboration


                                         1   Introduction                                              is now produced by Claude Code [7]. On Princeton’s
                                                                                                       SWE-bench Verified benchmark— designed to test
                                         The release of GitHub Copilot in 2021 marked the
                                                                                                       resolution of real GitHub issues drawn from popular
                                         first mainstream encounter most software engineers
                                                                                                       open-source repositories—state-of-the-art systems
                                         had with a generative-AI tool integrated into their
                                                                                                       have moved from 1.96% in October 2023 to roughly
                                         daily workflow [31]. Copilot, like its successors Tab-
                                                                                                       78% by spring 2026 [9, 16, 24].
                                         nine, Codeium, and Amazon CodeWhisperer, oper-
                                         ated as an in-editor completion system: the developer            This shift is not merely quantitative. It changes
                                         wrote, the model suggested, the developer accepted            what software engineers do during a working day,
                                         or rejected. The cognitive contract was clear—the             what artifacts the SDLC produces, and which skills
                                         human remained the engineer; the model was an                 command a wage premium. It also raises governance
                                         autocomplete with judgment.                                   questions—about determinism, auditability, security,
                                                                                                       and intellectual property—that the discipline has
                                            Five years later, that contract has been substan-
                                                                                                       not yet fully metabolized.
                                         tially renegotiated. Anthropic’s Claude Code, Ope-
                                         nAI’s Codex CLI, Google’s Jules, Cognition’s Devin,
                                         and the open-source OpenHands and SWE-agent
                                         projects do not complete code so much as perform              Contributions. This paper makes four contribu-
                                         engineering work: they read a repository, formulate           tions. First, in §2 we synthesize the principal lines
                                         a plan across multiple files, execute shell commands,         of work on agentic coding from major industrial labs
                                         run tests, observe failures, revise their approach, and       and academic groups. Second, in §3 we propose a
                                         deliver a committed change [2, 7, 35, 38]. Anthropic          six-layer reference architecture that organizes the
                                         reports that the majority of code written internally          design space of agentic software engineering systems.
                                                                                                       Third, in §4 we contrast the traditional SDLC with

                                                                                        Preprint. Under review.
Agentic AI in the Software Development Lifecycle                                                          Page 2


an Agentic SDLC (A-SDLC). Fourth, in §5 and §6            OpenAI. OpenAI’s contribution has been bracket-
we consolidate empirical evidence on performance          shaped. In 2021, the original Codex paper intro-
and labor-market effects, and in §7 identify five open    duced HumanEval [15]. In 2024, OpenAI collabo-
problems that constitute the field’s near-term re-        rated with the SWE-bench authors to release SWE-
search agenda.                                            bench Verified, a 489-task subset filtered for solvabil-
                                                          ity and clarity [16]. By 2026, GPT-5.4-Codex powers
2     Background and Related Work                         a Codex CLI that competes directly with Claude
                                                          Code, achieving high scores on Terminal-Bench 2.0
2.1    From Code Completion to Agency
                                                          and SWE-bench Pro [29].
The earliest LLM-based coding tools were trained
on large corpora of public source code and evalu-
ated on benchmarks like HumanEval and MBPP,               Google DeepMind. DeepMind’s AlphaEvolve
both of which test the ability to synthesize a single     [22, 28], unveiled in May 2025, represents a different
function from a docstring [11, 15]. These bench-          conception of agentic coding. Rather than resolving
marks saturated quickly: by 2024, frontier models         GitHub issues, AlphaEvolve uses an evolutionary
exceeded 90% pass@1 on HumanEval. The satura-             loop—an ensemble of Gemini Flash and Pro models
tion of single-function evaluation prompted Jimenez       proposes program variants, an automated evaluator
et al. at Princeton to introduce SWE-bench in Oc-         scores them, and the best survive into the next gen-
tober 2023 [24], a benchmark of 2,294 GitHub is-          eration. AlphaEvolve has discovered a new 4 × 4
sues drawn from twelve mature Python repositories.        complex matrix multiplication algorithm using 48
SWE-bench requires a system to navigate a real            scalar multiplications (improving on Strassen’s 1969
codebase, locate the relevant files, write a patch that   result), advanced 20% of fifty open mathematical
resolves the issue, and pass the project’s hidden test    problems, recovered 0.7% of compute across Google’s
suite. The original report found that no system,          data centers, and produced a 23% speedup of the
retrieval-augmented or otherwise, could resolve more      FlashAttention kernel that trains Gemini itself [28].
than ∼2% of issues.
   The performance ceiling broke not because models       Cognition / Devin. Cognition’s Devin, demon-
became larger, but because the scaffolding around         strated in March 2024, was the first commercial
them changed. SWE-agent [38], introduced by the           product to popularize the framing of “AI software
same Princeton group at NeurIPS 2024, demon-              engineer” [18]. Devin runs in a sandboxed cloud
strated that a custom agent–computer interface            VM with a browser, terminal, and editor, and is dis-
(ACI)—structured commands for navigating, editing,        patched tasks via Slack, Jira, or its web UI. Although
and testing—lifted resolution rates to 12.5% even         Devin’s headline SWE-bench numbers have been
with the same underlying model. This insight, that        overtaken by frontier-model agents, the product es-
interface design for the agent matters as much as         tablished the pattern that competitors—commercial
model capability, has organized the field since.          and open-source alike—now follow.

2.2    Industrial Frontier Systems
                                                          Microsoft / GitHub. Microsoft Research con-
Anthropic. Anthropic released Claude Code as
                                                          ducted some of the earliest rigorous productivity
a research preview alongside Claude 3.7 Sonnet in
                                                          studies on Copilot [19, 31]. In a controlled experi-
early 2025 [2, 3]. Claude Code operates at project
                                                          ment, developers using Copilot completed an HTTP
granularity: it reads the full codebase, plans changes
                                                          server task 55.8% faster than the control group [31];
across files, executes shell commands, runs tests,
                                                          a follow-up analysis of 934,533 Copilot users found
and iterates. Anthropic reports that Claude Opus
                                                          a ∼30% suggestion acceptance rate and projected
4.7 leads on SWE-bench Verified at 78.4% [9]. The
                                                          $1.5T in cumulative GDP impact by 2030 [19]. Mi-
product positions itself as a delegation interface—
                                                          crosoft’s Azure-based agentic SDLC reference ar-
engineers define goals and review results rather than
                                                          chitecture [30] formalizes specialized phase-agents
guiding each step.
                                                          coordinated by a core orchestrator.

                                             Preprint. Under review.
Agentic AI in the Software Development Lifecycle                                                                                                                 Page 3


    SWE-bench Verified (%)                                                                                        self-hosted deployments.
                                                                                                          78.4%
                              80                    Agentic systems
                                               Non-agentic (RAG)
                              60                                                                                  L1: Reasoning, Memory, Self-Reflection. The
                                                                                                                  cognitive scaffolding: chain-of-thought and ReAct-
                              40
                                                                                                                  style planning [37, 40], short- and long-term mem-
                              20
                                                                                                          ∼20%
                                                                                                                  ory mechanisms (including “memory files” produced
                               0
                                                                                                                  natively by Claude Opus 4 [3]), and self-critique
                                       23           24        ’24        5           25        25         6
                                  t’           d’           te        r’2       d’          te’       r’2         loops. Self-reflection largely accounts for the gap
                               Oc           Mi           La         Ea       Mi           La        Ap

                                                                    Timeline                                      between zero-shot model accuracy and agentic reso-
                                                                                                                  lution rates.
Figure 1. Issue-resolution rate on SWE-bench Verified,
October 2023 to April 2026. Agentic systems (solid)
compounded rapid gains; non-agentic RAG-based LLMs                                                                L2: Agent–Computer Interface (ACI). The
(dashed) plateaued near 20%. Data compiled from [7, 9,                                                            ACI [38] translates between an LLM’s text-token
16, 24, 29, 38].                                                                                                  output and concrete operations on a real computer.
                                                                                                                  The Princeton group’s core finding is that ACI design
                                                                                                                  quality is, empirically, as important as model size.
2.3                           Academic and Open-Source Work
The academic literature on agentic software engi-
                                                                                                                  L3: Tools and Environment. Filesystem and
neering has expanded rapidly. MetaGPT [23] and
                                                                                                                  editor operations, shell and process management,
ChatDev [33] both encode software development as
                                                                                                                  web browsing, test runners and compilers, and inte-
a multi-agent process: MetaGPT instantiates Prod-
                                                                                                                  gration with version control and CI/CD.
uct Manager, Architect, Engineer, and QA roles
operating under standardized operating procedures,
while ChatDev models a virtual software company                                                                   L4: Orchestration. Two dominant patterns coex-
in which agents communicate through a chat-chain.                                                                 ist. Single-agent loops (SWE-agent [38], Claude
AgileCoder [27] extends these ideas with sprints and                                                              Code [7]) maintain one cognitive locus. Multi-
a dynamic code-dependency graph. OpenHands (for-                                                                  agent systems—MetaGPT, ChatDev, AgileCoder,
merly OpenDevin) [35] is the leading open-source                                                                  AgentMesh [23, 25, 27, 33]— decompose work across
generalist platform, providing a Docker-sandboxed                                                                 role-specialized agents.
execution environment and supporting multiple LLM
backends. AutoCodeRover [41] and HyperAgent [32]
                                                                                                                  L5: Governance and Safety. Permission bound-
specialize in repository-level program repair. Re-
                                                                                                                  aries, sandboxing, audit logs, and policies for sensi-
cent surveys [26, 34, 36] organize this work along
                                                                                                                  tive operations. We argue in §7 that L5 is currently
axes of planning, memory, tool augmentation, and
                                                                                                                  the least mature layer and is rapidly becoming the
self-reflection.
                                                                                                                  bottleneck on enterprise deployment.
3                            A Reference Architecture for Agentic
                                                                                                                  4   From SDLC to Agentic SDLC
                             Software Engineering
                                                                                                                  The classical SDLC—whether waterfall, iterative,
Across heterogeneous systems we observe a recurring
                                                                                                                  or Agile—presupposes that behavior is fully speci-
stratification, summarized in Figure 3. We organize
                                                                                                                  fied at build time and validated before release [20].
it as six layers (L0–L5):
                                                                                                                  Agentic systems violate this assumption in two ways.
                                                                                                                  First, the systems themselves are stochastic: prompt
L0: Foundation Model. The base LLM pro-                                                                           drift, context truncation, and model updates produce
vides the system’s reasoning and code-generation                                                                  non-deterministic behavior under nominally identical
capacity. Claude Opus 4.7, GPT-5.4, and Gemini                                                                    inputs. Second, the development process becomes
3.1 Pro currently anchor the frontier; open-weights                                                               stochastic too: an agent may take a different path
models (Llama, DeepSeek, Qwen-Coder) populate                                                                     through the same task on different runs.

                                                                                                    Preprint. Under review.
Agentic AI in the Software Development Lifecycle                                                                                            Page 4


 (a) Traditional SDLC                           Human
                                               (b)    Supervisor
                                                   Agentic SDLC
                                                                                        Phase     Traditional SDLC       Agentic SDLC
        Requirements             HumanReq Agent                   Code Agent
                                                                                        Require- Analyst writes specs; Intent specification;
                    Design       Human             Orchestrator                         ments     stakeholder review     agent drafts spec
                                                      Agent
                                                                                        Design    Architect produces di- Agents propose & cri-
    Implementation               HumanDesign Agt                  Test Agent
                                                                                                  agrams, ADRs           tique; human selects
                                                                                        Implement.Engineers write code Coding agents exe-
                    Testing      Human                                                            file by file           cute plan; human re-
                                                    Deploy Agt                                                           views
              Deployment                                                                Testing   QA writes/runs tests Testing agents gener-
                                                                                                                         ate suites; sandbox
            Maintenance
                                                                                        Deploy    Manual or pipeline CI agent gates; hu-
                                                                                                  promotion              man approves prod
Figure 2. Traditional SDLC (a) vs. Agentic SDLC (b).                                    Maintain. On-call, tickets, hot- Monitor agents triage;
In the A-SDLC, an orchestrator coordinates specialized                                            fixes                  repair agents patch
sub-agents while the human supervises at intent, review,                                KPI       Cycle time, defect Accept rate, escala-
                                                                                                  rate                   tion quality
and approval gates.
                                                                                  Table 1. Phase-by-phase comparison of traditional and
                                                                                  Agentic SDLC.
                                                                     Feedback ↓




                                L5: Governance & Safety
                                                                                  5     Empirical Evidence
     Dependency ↑




                                   L4: Orchestration

                                                                                  5.1     Capability
                                L3: Tools & Environment

                                                                                  Figure 1 plots SWE-bench Verified resolution rates
                              L2: Agent–Computer Interface
                                                                                  for the dominant agentic system at each timepoint
                                L1: Reasoning & Memory                            between October 2023 and April 2026. The trajec-
                                 L0: Foundation Model
                                                                                  tory is approximately logistic: from 1.96% (RAG
                                                                                  baseline [24]) to 12.5% (SWE-agent [38]) to 33.2%
Figure 3. Six-layer reference architecture. Dependency                            (Anthropic’s first scaffold around Sonnet 3.5 [1]) to
runs upward; feedback flows downward (dashed red).                                49% (Claude 3.5 Sonnet new [3]) to 62.3% (Claude
                                                                                  3.7 Sonnet + Claude Code [7]) to 72.7% (Claude
                                                                                  Sonnet 4 [3]) to 78.4% (Claude Opus 4.7 [9]). Fron-
                                                                                  tier non-agentic systems have plateaued near 20%,
                                                                                  confirming that the gain is dominated by scaffolding
  We follow recent industry frameworks [17, 20, 30]                               rather than raw model capability.
in distinguishing an Agentic SDLC (A-SDLC) from                                      Figure 5 places major systems on a two-
the augmented SDLC merely accelerated by AI assis-                                dimensional capability–autonomy plane. The frontier
tants. Figure 2 illustrates the contrast, and Table 1                             is currently anchored by frontier-lab agentic stacks:
maps the phase-by-phase translation.                                              Claude Code, GPT-5.4 + Codex CLI, and Gemini
  Three structural differences are worth emphasizing.                             3.1 Pro + Jules. AlphaEvolve sits off the SWE-bench
First, the unit of work shrinks: instead of estimating                            frontier because it targets algorithmic discovery [28].
two-week sprints, teams scope work in tasks that an
agent can complete in minutes to hours, with human                                5.2     Productivity
review at the boundary. Second, the developer’s role                              Productivity evidence falls into three tiers. Con-
shifts from producing to orchestrating, reviewing, and                            trolled experiments have reported the largest effects:
directing— closer to the role of a senior engineer or                             Peng et al. [31] found a 55.8% completion-time reduc-
tech-lead than to that of an individual contributor [7].                          tion on a JavaScript HTTP-server task; Brandebuse-
Third, behavioral metrics—agent acceptance rate,                                  meyer et al. [13] found that moderate Copilot use
escalation quality, supervision burden—displace, but                              improved efficiency, while excessive use eroded the
do not entirely replace, process metrics like cycle                               benefit. Field experiments: Cui et al. [19] observed
time and defect rate [17, 20].                                                    12.92%–21.83% more pull requests per week at Mi-

                                                                   Preprint. Under review.
Agentic AI in the Software Development Lifecycle                                                                                                                            Page 5


  Reported Gain (%)                                                                                                        Frontier lab
                                                                                                                                                                           Claude Code
                                                                                                              80                                          Codex CLI
                      60      55.8                                                                                                                                 Jules




                                                                                            Capability (%)
                                                                                                                          Autonomy-first
                      50                                                                                                   Open-source
                                                                                                              60
                      40                                                                                                 Editor-integrated
                                                                                                                            Copilot
                      30                                                                                                                               OpenHands
                                               21.8                                                           40
                      20                                                      13.6
                                                                 8.7
                      10
                                                                                                              20                             SWE-agent
                       0                                                                                                                                                      Devin
                           Pen
                               g              S)               cc)           eb.
                                          e (M             e (A         rand
                                     Dohmk            Dohmk            B
                                                                                                              0   lete             st             d
                                                                                                             Comp            Sugge           Guide    Semi-
                                                                                                                                                           auto      Auto


Figure 4. Productivity gains across four studies of AI-                                                                                   Autonomy Level
assisted coding [10, 13, 19, 31]. Controlled experiments
report the largest effects.                                                             Figure 5. The capability–autonomy frontier, 2021–2026.
                                                                                        Frontier-lab stacks (blue) define the upper-right envelope;
                                                                                        open-source systems (green) trade capability for accessi-
                                                                                        bility; Devin (red) prioritizes autonomy. Dashed curve:
crosoft and 7.51%–8.69% at Accenture. Longitudinal                                      approximate frontier.
team studies found that team performance and per-
ceived efficiency rise even when commit metrics stay                                                         Program Flagship                  Emphasis              SWE-
flat [10].                                                                                                                                                           b
   These numbers should be read alongside two cau-                                                           Anthropic Claude Code Delegation; memory; ∼78%
tionary findings. First, recent work argues that AI-                                                                   (Opus 4.7)   safety
                                                                                                             OpenAI Codex       CLI General agentic ca- ∼73%
assisted code can increase long-term technical debt                                                                    (GPT-5.4)    pability
[12]. Second, productivity gains are unevenly dis-                                                           DeepMind AlphaEvolve Evolutionary discov- ∼70%
tributed: experienced Claude users are substantially                                                                   + Jules      ery
                                                                                                             MS/GitHubCopilot,      Enterprise breadth ∼50%
more successful than newcomers [10], suggesting a                                                                      Azure
learning curve that compounds the existing skill dis-                                                        Cognition Devin        Sandboxed AI SWE ∼14%
tribution.                                                                                                   Princeton SWE-         Benchmarks & ACI 12.5%
                                                                                                                       agent/bench
                                                                                                             Academia MetaGPT,      Multi-agent SOPs n/a
5.3                   Adoption and Labor-Market Signals                                                                ChatDev
Anthropic’s quarterly Economic Index reports [4, 5,
10] are the most systematic public source of usage                                      Table 2. Frontier agentic-coding programs, c. April 2026.
data. As of February 2026, computer and mathe-                                          SWE-bench Verified figures are approximate [3, 7, 9, 29,
                                                                                        38].
matical tasks account for ∼35% of Claude.ai conver-
sations and nearly half of API traffic. 49% of jobs in
Anthropic’s sample saw Claude used for at least a
                                                                                        6                    Comparative Analysis of Frontier Pro-
quarter of their tasks (up from 36% in January 2025).
                                                                                                             grams
However, when usage is weighted by an effective cov-
erage measure, software developers are relatively less                                  We summarize the strategic posture of each major
affected than naïve task-coverage would suggest—a                                       program in Table 2. Three patterns are notable.
counterintuitive finding driven by the difficulty of                                    Anthropic has placed primary emphasis on the del-
the tasks developers actually delegate.                                                 egation use case—long-horizon agentic coding with
   Anthropic’s labor-market analysis [8] finds no clear                                 explicit human approval gates. OpenAI has con-
unemployment signal in high-exposure occupations                                        verged on a similar product surface (Codex CLI)
as of early 2026, but does find that hiring of workers                                  and competes closely on benchmarks [29]. Google
aged 22–25 into the most exposed roles has slowed                                       DeepMind has pursued a distinctive evolutionary
by ∼14% relative to a counterfactual. Among 81,000                                      path with AlphaEvolve [28]. Microsoft / GitHub
respondents to a separate survey [6], roughly one-                                      occupies the broadest user base. Princeton/Stanford
fifth of workers in AI-exposed jobs voiced concern                                      open-source work on SWE-agent and SWE-bench
about economic displacement; software engineers                                         underpins the evaluation infrastructure [16, 24, 38].
were among the most concerned.                                                            Despite differing strategies, convergence is visible.

                                                                           Preprint. Under review.
Agentic AI in the Software Development Lifecycle                                                           Page 6


All major programs now expose: (i) a CLI- or IDE-          7.4    Skill Redistribution
resident agent with shell, file, and test-runner access;   Anthropic’s data [10] suggests an emerging two-track
(ii) human-in-the-loop approval at high-impact ac-         market: experienced engineers capture compound-
tions; (iii) some form of long-term memory; (iv)           ing gains; newcomers use agents to do the work
parallel/multi-agent execution for non-trivial tasks;      and underperform. Educational research that ex-
and (v) a strong story about safety and audit.             plicitly trains orchestration skills—decomposition,
                                                           prompting, review, and judgment about when not to
7     Open Problems and Research Agenda
                                                           delegate—will be needed to keep the pipeline open.
We close by identifying five open problems we believe
will dominate the next two-to-three years of work.         7.5    The Economics of Attention
                                                           If an agent can produce ten plausible patches per
7.1    Evaluation beyond SWE-bench                         hour, the rate-limiting resource is human review.
SWE-bench has been an indispensable forcing func-          Research on tooling for high-throughput review—
tion, but it has limitations: it is dominated by           automated diff summarization, behavioral test gen-
Python, focuses on bug-fixing, and provides ground-        eration, principled sampling of agent traces—is a
truth tests that real-world tasks lack [39, 42]. SWE-      natural successor research program to the agent pro-
bench Multimodal [39], SWE-bench Pro, Terminal-            grams of 2023–2026.
Bench, and SWE-Compass [21, 29, 39] are extending
coverage to JavaScript, multi-language, multimodal,        8     Conclusion
and production-aligned tasks. Research is needed           Software engineering is in the middle of a disconti-
on benchmarks that capture long-horizon delegation,        nuity. In 2021, the question was whether language
collaboration with human reviewers, faithfulness to        models could plausibly autocomplete a function; by
stated intent, and the absence of “reward hacking”         2026, frontier agentic systems resolve roughly four
behaviors [3].                                             out of five real GitHub issues drawn from mature
7.2    Governance, Safety, and Audit                       repositories, and a non-trivial fraction of the code at
                                                           major AI labs is written by such systems [7].
The 2025 AI Agent Index [14] documents a prolifera-
                                                              Our reading is cautiously optimistic. Agentic sys-
tion of deployed agentic systems alongside a marked
                                                           tems are real productivity tools, not toys; the em-
deficit in governance documentation. The ADLC
                                                           pirical evidence on time saved and tasks delegated
framework [17, 20] proposes human–agent responsi-
                                                           is substantial, if uneven. But the frame of code
bility mapping—an explicit allocation of authority
                                                           generation is the wrong frame. The right frame is
levels and approval gates—as a non-optional design
                                                           delegated execution under human supervision—and
step. Operationalizing this idea in a way auditors
                                                           the long-run winners will be those who invest earliest
can verify is an open problem.
                                                           in the process, governance, and skills that delegation
7.3    The Technical-Debt Hypothesis                       requires. The research agenda we have sketched is,
                                                           in the end, a research agenda for keeping humans
Bauer et al. [12] argue that AI-assisted programming       firmly in the loop while letting the machines do the
may decrease productivity for experienced develop-         typing.
ers by inflating maintenance burden. Agents are
biased toward producing more code (because pro-            Acknowledgments
duction is cheap) and toward local fixes (because
global redesign is expensive in tokens). Long-term         We thank the open-source maintainers of SWE-
studies of repository health under sustained agent         bench, SWE-agent, and OpenHands, and the pub-
contribution are urgently needed.                          lic documentation teams at Anthropic, OpenAI,
                                                           Google DeepMind, Microsoft Research, and Cog-
                                                           nition, whose published reports made this synthesis
                                                           possible.



                                              Preprint. Under review.
Agentic AI in the Software Development Lifecycle                                                       Page 7


References                                                [13] Charlotte Brandebusemeyer, Tobias Schimmer,
                                                               and Bert Arnrich. Developers’ experience with
 [1] Anthropic. SWE-Bench performance with
                                                               generative AI: First insights from an empirical
     Claude 3.5 Sonnet. https://www.anthropic.
                                                               mixed-methods field study. In ICSE SEIP 2026;
     com/research/swe-bench-sonnet, 2024.
                                                               arXiv:2512.19926, 2026.
 [2] Anthropic. Introducing Claude 3.7 Sonnet and
                                                          [14] S. Casper et al. The 2025 AI Agent Index:
     Claude Code. https://www.anthropic.com/
                                                               Documenting technical and safety features of
     news/claude-3-7-sonnet, 2025.
                                                               deployed agentic AI systems. arXiv:2602.17753,
 [3] Anthropic. Introducing Claude 4 (Opus 4                   2026.
     and Sonnet 4). https://www.anthropic.com/            [15] Mark Chen et al. Evaluating large language
     news/claude-4, 2025.                                      models trained on code. arXiv:2107.03374,
                                                               2021.
 [4] Anthropic. Anthropic Economic Index: Insights
     from Claude conversations (january 2025 base-        [16] Neil Chowdhury, James Aung, Chan Jun Shern,
     line), 2025.                                              Oliver Jaffe, Dane Sherburn, Giulio Starace,
                                                               Evan Mays, Rachel Dias, Marwan Aljubeh, Mia
 [5] Anthropic. New building blocks for under-
                                                               Glaese, and Carlos E. Jimenez. Introducing
     standing AI use. https://www.anthropic.
                                                               SWE-bench Verified. Technical report, OpenAI,
     com/research/economic-index-primitives,
                                                               2024.
     2025.
                                                          [17] Codebridge. Agentic AI software development
 [6] Anthropic. What 81,000 people told us about
                                                               lifecycle: Secure ADLC playbook. Codebridge
     the economics of AI. https://www.anthropic.
                                                               Tech, 2026.
     com/research/81k-economics, 2026.
                                                          [18] Cognition Labs. Introducing Devin, the first
 [7] Anthropic. Claude Code: Anthropic’s agentic               AI software engineer. https://cognition.ai/
     coding system. https://www.anthropic.com/                 blog/introducing-devin, 2024.
     product/claude-code, 2026.
                                                          [19] Thomas Dohmke, Marco Iansiti, and Greg
 [8] Anthropic.    Labor market impacts of                     Richards. Sea change in software development:
     AI: A new measure and early evidence.                     Economic and productivity analysis of the AI-
     https://www.anthropic.com/research/                       powered developer lifecycle. arXiv:2306.15033,
     labor-market-impacts, 2026.                               2023.
 [9] Anthropic. Claude Opus 4.7 model card and            [20] EPAM. Agentic development lifecycle (ADLC):
     system report. https://www.anthropic.com,                 A new model for AI systems beyond SDLC.
     2026.                                                     https://www.epam.com/insights, 2026.
[10] Anthropic. Anthropic Economic Index re-              [21] X. Gao et al. SWE-Bench-CL: Continual learn-
     port: Learning curves (february 2026 data).               ing for coding agents. arXiv:2507.00014, 2025.
     https://www.anthropic.com/research/
     economic-index-march-2026-report, 2026.              [22] Google DeepMind. AlphaEvolve: A Gemini-
                                                               powered coding agent for designing advanced
[11] Jacob Austin et al. Program synthesis with                algorithms. https://deepmind.google/blog,
     large language models. arXiv:2108.07732, 2021.            2025.

[12] S. Bauer et al. AI-assisted programming de-          [23] Sirui Hong et al. MetaGPT: Meta programming
     creases the productivity of experienced develop-          for a multi-agent collaborative framework. In
     ers by increasing the technical debt and main-            International Conference on Learning Represen-
     tenance burden. arXiv:2510.10165, 2025.                   tations (ICLR), 2024.

                                             Preprint. Under review.
Agentic AI in the Software Development Lifecycle                                                         Page 8


[24] Carlos E. Jimenez, John Yang, Alexander Wet-         [33] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen,
     tig, Shunyu Yao, Kexin Pei, Ofir Press, and               Yufan Dang, Jiahao Li, Cheng Yang, Weize
     Karthik Narasimhan. SWE-bench: Can lan-                   Chen, Yusheng Su, Xin Cong, Juyuan Xu, Da-
     guage models resolve real-world GitHub issues?            hai Li, Zhiyuan Liu, and Maosong Sun. Chat-
     In International Conference on Learning Repre-            Dev: Communicative agents for software devel-
     sentations (ICLR), 2024.                                  opment. arXiv:2307.07924, 2024.

[25] Sourena Khanzadeh.      AgentMesh: A co-             [34] R. Sapkota et al. Agentic AI: A comprehensive
     operative multi-agent generative AI frame-                survey of architectures, applications, and future
     work for software development automation.                 directions. arXiv:2510.25445, 2025.
     arXiv:2507.19902, 2025.
                                                          [35] Xingyao Wang et al. OpenHands: An open
[26] Y. Liu et al. A comprehensive survey on                   platform for AI software developers as generalist
     benchmarks and solutions in software engi-                agents. In International Conference on Learning
     neering of LLM-empowered agentic systems.                 Representations (ICLR), 2025.
     arXiv:2510.09721, 2025.                              [36] Yanlin Wang et al. Agents in software engineer-
                                                               ing: Survey, landscape, and vision. Automated
[27] Minh-Hoang Nguyen et al.      AgileCoder:
                                                               Software Engineering, 32(2):1–36, 2025.
     Dynamic collaborative agents for software
     development based on agile methodology.              [37] Jason Wei et al. Chain-of-thought prompting
     arXiv:2406.11912, 2024.                                   elicits reasoning in large language models. In
                                                               Advances in Neural Information Processing Sys-
[28] Alexander Novikov, Ngân Vũ, Marvin Eisen-                tems (NeurIPS), 2022.
     berger, Emilien Dupont, Po-Sen Huang,
     Adam Zsolt Wagner, Sergey Shirobokov,                [38] John Yang, Carlos E. Jimenez, Alexander
     Borislav Kozlovskii, Francisco J. R. Ruiz, Ab-            Wettig, Kilian Lieret, Shunyu Yao, Karthik
     bas Mehrabian, M. Pawan Kumar, Abigail                    Narasimhan, and Ofir Press. SWE-agent:
     See, Swarat Chaudhuri, George Holland, Alex               Agent–computer interfaces enable automated
     Davies, Sebastian Nowozin, Pushmeet Kohli,                software engineering. In Advances in Neural In-
     and Matej Balog. AlphaEvolve: A coding                    formation Processing Systems (NeurIPS), 2024.
     agent for scientific and algorithmic discovery.
                                                          [39] John Yang et al. SWE-bench Multimodal: Do
     arXiv:2506.13131, 2025.
                                                               AI systems generalize to visual software do-
[29] OpenAI. GPT-5.4-Codex and Codex CLI                       mains? arXiv:2410.03859, 2024.
     0.120: Technical overview. https://openai.           [40] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du,
     com/index/codex-cli, 2026.                                Izhak Shafran, Karthik Narasimhan, and Yuan
                                                               Cao. ReAct: Synergizing reasoning and acting
[30] Shashikanta Parida. Modernizing the SDLC
                                                               in language models. In International Conference
     process with agentic AI. Microsoft Data Science
                                                               on Learning Representations (ICLR), 2023.
     Blog, 2025.
                                                          [41] Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and
[31] Sida Peng, Eirini Kalliamvakou, Peter Cihon,              Abhik Roychoudhury. AutoCodeRover: Au-
     and Mert Demirer. The impact of AI on de-                 tonomous program improvement. In ISSTA
     veloper productivity: Evidence from GitHub                2024, 2024.
     Copilot. Microsoft Research Technical Report;
     arXiv:2302.06590, 2023.                              [42] Y. Zhao et al. SWE-Compass: Towards unified
                                                               evaluation of agentic coding abilities for large
[32] Huy Nhat Phan et al. HyperAgent: Generalist               language models. arXiv:2511.05459, 2025.
     software engineering agents to solve coding tasks
     at scale. arXiv:2409.16299, 2024.

                                             Preprint. Under review.
