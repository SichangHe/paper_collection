                                              Agentic Agile-V: From Vibe Coding to Verified
                                                 Engineering in Software and Hardware
                                                              Development
                                                                                                   Christopher Koch
                                                                                                Independent Researcher


                                            Abstract—Agentic AI coding systems can inspect repositories,          Yet the evidence base also challenges the strongest hype.
                                         plan implementation steps, edit files, call tools, run tests, and     A randomized controlled trial with 96 full-time Google en-
                                         submit pull requests. These capabilities make software and            gineers reported an estimated 21 percent reduction in time
arXiv:2605.20456v1 [cs.SE] 19 May 2026




                                         hardware development faster in some settings, but current
                                         evidence does not support the simple claim that autonomous            on a complex enterprise task with AI assistance [4]. In con-
                                         code generation automatically improves engineering outcomes.          trast, a METR randomized trial with experienced open-source
                                         Controlled studies report productivity gains in some enterprise       developers found that AI tools increased task completion
                                         tasks, slowdowns in mature open-source work, moderate but             time by 19 percent in mature repositories, despite developer
                                         heterogeneous meta-analytic effects, and persistent failures in       expectations of speedup [5]. A 2026 meta-analysis found a
                                         repository setup, dependency handling, permission gating, and
                                         hardware verification. This paper argues that the central problem     statistically significant but moderate productivity effect, with
                                         is no longer prompt engineering; it is engineering process            substantial heterogeneity and smaller effects in open-source
                                         control. It synthesizes evidence from agentic software engineer-      and enterprise contexts [6]. Repository-level configuration files
                                         ing, GitHub-scale adoption studies, repository-level agent con-       can reduce runtime and token use in some settings [12], but
                                         figuration, productivity trials, issue-resolution benchmarks, and     other evaluations find that context files can reduce task success
                                         hardware/RTL verification research. It proposes Agentic Agile-V,
                                         a process framework that uses Agile-V as the lifecycle backbone       and increase cost when they add unnecessary or mismatched
                                         and a task-level SCOPE-V loop - Specify, Constrain, Orchestrate,      requirements [13]. Hardware evidence is even more caution-
                                         Prove, Evolve, and Verify - to convert conversational intent into     ary: RealBench reports low pass rates on real-world Verilog
                                         structured engineering artifacts and acceptance evidence. The         generation, including 0 percent pass@1 on system-level tasks
                                         paper contributes: (i) a taxonomy of minimum input artifacts          for evaluated models [27], and FIXME argues that functional
                                         for agentic software, firmware, and hardware work; (ii) a
                                         conversation-to-contract gate that separates exploratory dialogue     verification remains underexplored despite rapid progress in
                                         from implementation; (iii) risk-adaptive feature, bug-fix, testing,   LLM-aided design [28].
                                         and hardware workflows; and (iv) an evidence-bundle acceptance           These findings point to a process gap. Agentic AI can
                                         model for agent-generated artifacts. The paper concludes that         generate plausible engineering artifacts faster than humans can
                                         agentic AI does not eliminate engineering discipline; it increases
                                                                                                               inspect them. Therefore, the bottleneck shifts from code syn-
                                         the value of requirements, constraints, traceability, independent
                                         verification, and human approval.                                     thesis to specification quality, execution context, verification,
                                            Index Terms—Agentic AI, software engineering, Agile-V, AI-         traceability, and controlled iteration. The right question is not
                                         assisted development, coding agents, hardware development,            merely “How do we prompt better?” but “Which process turns
                                         firmware, verification, testing, requirements engineering, V-         natural-language intent into verifiable engineering output?”
                                         model, software process.
                                                                                                                  This paper proposes Agentic Agile-V, a process framework
                                                                                                               for agentic software, firmware, and hardware development. It
                                                                I. I NTRODUCTION
                                                                                                               integrates Agile-V, a compliance-ready approach that com-
                                           Agentic AI changes the form of engineering work. Modern             bines Agile iteration with V-model verification and audit
                                         coding agents can do more than complete a line of code: they          artifact generation [1], with a task-level SCOPE-V execution
                                         can read repositories, plan work, invoke terminals, modify            loop. The central principle is:
                                         multiple files, run tests, prepare pull requests, and respond to           Conversation is useful for discovering intent; struc-
                                         review feedback. The ecosystem now includes asynchronous                   tured artifacts are required for implementation; evi-
                                         coding agents, repository-level instruction files, agent SDKs,             dence is required for acceptance.
                                         multi-agent workspaces, and model-agnostic routing. Large-
                                         scale evidence shows that this is already an operational phe-           The contributions are fourfold:
                                         nomenon rather than a speculative one: the AIDev dataset              1) A synthesis of evidence from agentic coding research,
                                         reports 932,791 agent-authored pull requests across 116,211              GitHub adoption studies, repository-configuration work,
                                         repositories and 72,189 developers [8]. Surveys on LLM-                  productivity studies, issue-resolution benchmarks, and
                                         based agents for software engineering identify applications              hardware verification benchmarks.
                                         across requirements, implementation, testing, maintenance,            2) A conversation-to-contract model that separates exploratory
                                         and human-agent collaboration [2], [3].                                  dialogue from structured execution.
3) The Agentic Agile-V process model, combining Agile-V            but also substantial human revision, especially for bug fixes,
   lifecycle structure with the SCOPE-V task loop.                 documentation, and project-specific standards [10].
4) Practical workflows and risk-adaptive evidence gates for           Configuration artifacts are emerging as the process layer
   feature work, bug fixing, test generation, firmware, and        around agents. A study of 2,926 GitHub repositories found
   hardware/RTL development.                                       eight configuration mechanisms across tools such as Claude
                                                                   Code, GitHub Copilot, Cursor, Gemini, and Codex, with
          II. BACKGROUND AND E VIDENCE BASE                        context files dominating and AGENTS.md emerging as an in-
A. From Assistants to Agents                                       teroperable standard [11]. One study found that AGENTS.md
                                                                   was associated with lower runtime and lower output-token
   LLM-based software agents extend standalone language
                                                                   consumption [12]. Another found that context files can re-
models with perception, planning, memory, tool use, execution
                                                                   duce task success and increase inference cost when they
environments, and human interaction [2]. Code-generation
                                                                   impose unnecessary requirements [13]. A factorial study of
agents differ from earlier code generators because they can de-
                                                                   configuration-file structure found limited evidence that size,
compose tasks, navigate repositories, execute tests, debug fail-
                                                                   position, architecture, or local contradiction variables alone
ures, and integrate changes across the software development
                                                                   create reliable adherence effects [14].
lifecycle [3]. OpenHands, for example, emphasizes sandboxed
                                                                      These mixed results motivate a minimal-context princi-
execution, lifecycle control, model-agnostic routing, custom
                                                                   ple: repository instructions should be short, current, non-
tools, memory management, and workspace/API integrations
                                                                   contradictory, and tied to executable feedback.
[21]. GitHub has also moved toward agentic workflows in
which tasks can be delegated to agents that clone repositories,
work in virtual environments, document their decisions, run        D. Repository Execution Remains Hard
tests, and propose pull requests for human review [22], [23].         Real-world repository tasks remain challenging. Git-
   This transition changes the engineering problem. The unit       TaskBench found that even the best evaluated system, Open-
of interaction is no longer just a prompt and an answer. It is     Hands plus Claude 3.7, solved 48.15 percent of tasks, with
a socio-technical loop consisting of requirements, repository      many failures caused by environment setup and dependency
context, tools, permissions, tests, build environments, review     resolution [15]. RepoMaster improves repository exploration
practices, and release gates.                                      by constructing graphs and pruning context, showing that
                                                                   repository understanding and context selection are central bot-
B. Productivity Is Context-Dependent
                                                                   tlenecks [16]. SWE-Skills-Bench found that procedural skill
   The current productivity literature supports a balanced         packages usually provide limited marginal benefit unless they
claim. AI assistance can help, especially in well-scoped or rou-   match the domain and project context [17]. SWE-rebench V2
tine tasks, but it can also create overhead through prompting,     further demonstrates the importance of reproducible execution
waiting, review, and correction. The Google RCT provides ev-       environments and reliable test suites at scale [18].
idence for acceleration in an enterprise setting [4]; the METR        The lesson is that code context alone is insufficient. Agents
RCT shows slowdown in familiar mature open-source work             need execution context: build commands, dependency setup,
[5]; and a meta-analysis reports a moderate average effect with    test commands, environment variables, toolchain information,
strong context dependence [6]. A systematic literature review      simulator access, and clear acceptance criteria.
also warns that developer productivity is multi-dimensional
and cannot be reduced to output volume or task time alone [7].
                                                                   E. Hardware and Firmware Raise the Bar
Maintenance-burden research further suggests that AI-assisted
output may shift review and rework load toward experienced            Hardware, firmware, and embedded development have
developers [32].                                                   stricter failure modes. Incorrect pin mappings, register values,
   The implication is not that agentic AI fails. It is that AI-    timing assumptions, bus behavior, reset handling, or memory
assisted engineering is a process-sensitive intervention. Task     layout can produce failures that are costly or unsafe. Real-
type, codebase complexity, developer expertise, test coverage,     Bench explicitly addresses the gap between simple Verilog
dependency setup, and verification cost can determine whether      benchmarks and real-world IP-level workflows; its low pass
agents help or hurt.                                               rates show that current LLMs are not reliable system-level
                                                                   hardware generators [27]. FIXME focuses on design verifi-
C. GitHub Evidence and Repository Configuration                    cation and uses silicon-proven designs to evaluate functional
   GitHub evidence shows rapid adoption. AIDev provides            verification capabilities [28]. Surveys of LLMs for electronic
a large corpus of agent-authored pull requests [8]. A task-        design automation and hardware/software co-design highlight
stratified analysis of 7,156 pull requests found that task type    both opportunities and reliability limitations [29]–[31].
strongly influences acceptance rates: documentation changes           For these domains, compilation is not proof. Simulation,
were accepted more often than new features, and no single          formal checking, hardware-in-the-loop tests, timing analysis,
agent performed best across all categories [9]. An empirical       and traceability from requirement to verification evidence are
study of Claude Code pull requests found high acceptance,          essential.
     III. M ETHOD : B OUNDED E VIDENCE S YNTHESIS                                          Agentic Agile-V
   This paper uses a bounded evidence synthesis rather than                         Intent → Brief → Constraints
a quantitative meta-analysis. The evidence base is heteroge-                                      ↓
neous: randomized trials, GitHub-scale datasets, repository-                      Agentic execution via SCOPE-V
configuration studies, tool papers, issue-resolution surveys,                                     ↓
hardware benchmarks, and process frameworks measure dif-                     Tests, checks, simulation, review evidence
ferent outcomes. Pooling them into a single effect size would                                     ↓
obscure rather than clarify the process problem.                               Human approval and baseline update
   Sources were selected from four streams:                               Conversation discovers intent. Structured artifacts
                                                                             control implementation. Evidence controls
1) agentic software engineering surveys and tool papers;                                     acceptance.
2) empirical studies of developer productivity, agent-authored
   pull requests, and issue resolution;                                           Fig. 1. High-level Agentic Agile-V model.
3) repository-configuration and execution-environment stud-
   ies;
4) hardware, firmware, and design-verification benchmarks.          C. The Missing Bridge

   A source was included if it addressed at least one of the fol-      Current tools provide execution surfaces, sandboxing, repos-
lowing: agentic code generation, issue resolution, repository-      itory instructions, test execution, and pull-request workflows.
aware execution, productivity, configuration artifacts, permis-     Existing engineering processes provide requirements disci-
sion or tool gating, hardware generation, hardware verification,    pline, verification logic, review, and release gates. The missing
lifecycle traceability, or verification evidence. Industry and      bridge is a lightweight framework that tells teams what input
platform sources were used only when they documented                to provide to agents, how to structure agent execution, when to
observable tool behavior or adoption trends; peer-reviewed          test, and which evidence is required before accepting generated
and preprint research was used for empirical and conceptual         artifacts.
claims.
                                                                             V. T HE AGENTIC AGILE -V F RAMEWORK

                 IV. P ROBLEM S TATEMENT                            A. Overview
                                                                       Agentic Agile-V has two layers. The macro layer is Agile-
A. The Limits of Conversational Development
                                                                    V: an iterative lifecycle in which each increment remains
   Conversational development is useful, but insufficient as        traceable to requirements, design, implementation, verification,
an implementation substrate. It helps teams discover require-       approval, and audit evidence. The micro layer is SCOPE-V,
ments, surface ambiguity, compare architectures, and identify       the task-level loop used to run individual agentic tasks.
risks. But long chat histories are not reliable engineering            This design avoids a false choice between agility and
contracts:                                                          verification. Agile iteration provides speed; V-model reasoning
• they contain superseded assumptions;                              provides traceability; agentic execution provides implementa-
• constraints are often implicit;                                   tion capacity; verification gates decide acceptance.
• acceptance criteria are rarely executable;
                                                                    B. The SCOPE-V Micro-Cycle
• agents may overfit to recent turns;
• reviewers cannot easily audit which instruction governed a           Each agentic task passes through six steps:
  change.                                                              Specify. Convert intent into a task brief with objective,
                                                                    scope, non-goals, affected modules, dependencies, acceptance
   Therefore, agentic work needs a conversation-to-contract
                                                                    criteria, and required evidence.
gate: after discovery, the relevant intent must be converted
into a reviewed execution brief.                                       Constrain. Define boundaries: no public API change unless
                                                                    approved, no unrelated files, no new dependencies without
                                                                    justification, no broad refactor during a bug fix, explicit review
B. Verification Debt
                                                                    for security-sensitive code, and mandatory preservation of
   Agentic AI can increase the volume of code, tests, doc-          hardware timing and safety constraints.
umentation, and patches. If output volume grows faster than            Orchestrate. Define how the agent should work: inspect
verification capacity, teams accumulate verification debt: weak     first, summarize current design, propose a plan, implement
tests, hidden regressions, broad patches, unvalidated dependen-     small slices, run local checks, and produce a diff summary
cies, undocumented behavior, and increased reviewer burden.         with residual risks.
The METR trial and maintenance-burden findings indicate that           Prove. Require evidence: unit tests, integration tests, re-
review and cleanup can erase perceived speedups [5], [32]. In       gression tests, static analysis, type checks, linting, security
hardware and embedded work, verification debt can become            scans, simulation, formal checks, hardware-in-the-loop results,
operational or physical risk.                                       or review checklists depending on risk.
   Evolve. Feed validated learning back into repository instruc-   4) Require a plan before edits.
tions, templates, tests, and engineering baselines. Remove stale   5) Implement the smallest useful slice.
or harmful instructions.                                           6) Add or update tests alongside implementation.
   Verify. Treat verification as recurring rather than final:      7) Run targeted and regression checks.
before implementation, during patching, before merge, after        8) Produce a diff summary, evidence bundle, and residual-risk
deployment, and after field feedback.                                 note.
                                                                   9) Require human review for architecture, security, maintain-
C. Agile-V as Lifecycle Backbone
                                                                      ability, and edge cases.
  Agile-V was proposed to address a weakness of machine-
speed AI-assisted engineering: lack of built-in task-level         B. Bug Fixing
verification and regulatory traceability [1]. Its case study
demonstrates feasibility in a hardware-in-the-loop setting with        Bug fixing is causal diagnosis, not feature generation. The
independent test generation and audit artifacts. This paper        agent should not patch immediately. A recommended process
generalizes the idea to agentic software, firmware, and hard-      is:
ware development by specifying inputs, task workflows, and         1) Capture observed and expected behavior.
acceptance gates.                                                  2) Provide reproduction steps, logs, environment, and version.
  The design principle is:                                         3) Ask the agent for hypotheses and missing evidence.
      Agile-V controls the lifecycle; SCOPE-V controls             4) Localize likely files and call paths.
      the agentic task.                                            5) Create a failing regression test where possible.
                                                                   6) Apply the minimal patch.
          VI. M INIMUM I NPUT A RTIFACT M ODEL
                                                                   7) Run regression and nearby tests.
   Table I defines a minimum input package. The goal is not to     8) Explain why the fix works and what it does not address.
overload agents with context, but to provide enough structured
                                                                      Issue-resolution surveys emphasize that realistic mainte-
information to avoid guessing.
                                                                   nance requires long-horizon reasoning, iterative exploration,
  VII. C ONVERSATIONAL D ISCOVERY VS . S TRUCTURED                 and feedback-driven decision-making beyond single-shot gen-
                    E XECUTION                                     eration [19], [20].
A. When Conversation Helps
                                                                   C. Testing and Review
   Conversation is appropriate for early uncertainty: clarifying
requirements, brainstorming architecture, identifying missing          Testing must be inside the agent loop, not after it:
constraints, comparing test strategies, asking what could fail,    • Before implementation: identify expected tests, edge cases,
and exploring alternative designs. In this phase the agent acts      and failure modes.
as a thinking partner. The desired output is not code first; it    • During implementation: run targeted tests after small
is a better problem statement.                                       changes.
B. When Structure Is Mandatory                                     • Before merge: require CI, static analysis, type checks,
                                                                     security checks, and review.
   Before implementation, the conversation must become a
                                                                   • After merge: monitor logs, defects, performance, and user
structured brief. This is mandatory when a task affects public
                                                                     feedback.
APIs, safety, security, performance, hardware behavior, regu-
lated workflows, customer-facing behavior, shared libraries, or       Permission and action gating are part of the testing prob-
persistent data.                                                   lem. A stress-test of Claude Code’s auto mode found that
   The operational rule is:                                        permission-gate assumptions may fail under ambiguous state-
     Do not let an agent implement from a long chat. Let           changing scenarios, especially when equivalent effects can be
     it implement from a reviewed brief.                           achieved through file edits instead of shell commands [26].
   This rule is consistent with mixed evidence on context files.   This supports explicit risk classification and human approval
Relevant instructions can improve efficiency [12]; unnecessary     for state-changing or high-blast-radius actions.
or mismatched instructions can harm success [13]. The correct
goal is not maximum context, but decision-relevant context.        D. Hardware, Firmware, and Embedded Development

                  VIII. TASK W ORKFLOWS                               Hardware-facing work requires stricter input and stricter
                                                                   evidence. The agent input package should include board/chip
A. Feature Development                                             revision, datasheet excerpts, registers, pinout, clocks, proto-
  Feature work expands product intent into behavior. A rec-        cols, memory map, toolchain, simulator, formal checker, test
ommended process is:                                               equipment, and rollback plan. Implementation should not be
1) Write a feature brief: goal, non-goals, acceptance criteria.    accepted without simulation, static checks, formal proper-
2) Identify affected modules, APIs, data structures, and tests.    ties where applicable, and hardware-in-the-loop evidence for
3) Ask the agent to inspect and summarize current design.          production-risk changes.
                                                                  TABLE I
                           M INIMUM INPUT ARTIFACTS FOR AGENTIC SOFTWARE , FIRMWARE , AND HARDWARE DEVELOPMENT.

    Artifact                   Software Example                                            Firmware/Hardware Example
    Intent and scope           User story, target behavior, non-goals, affected APIs       Function of module, hardware mode, peripheral role,
                                                                                           integration boundary
    Acceptance criteria        Expected inputs/outputs, UI behavior, error cases,          Timing budget, protocol compliance, register behav-
                               performance target                                          ior, waveform or HIL expectation
    Architecture context       Modules, interfaces, dependencies, data model, ser-         Board revision, MCU/FPGA/SoC, memory map,
                               vice boundaries                                             clocks, buses, pinout, RTOS assumptions
    Constraints                No API breakage, no new dependency, style and               Voltage/power limits, timing constraints, interrupt
                               security rules                                              rules, safety states, reset behavior
    Execution context          Build commands, dependency setup, test commands,            Toolchain, simulator, synthesis tool, formal checker,
                               environment variables                                       test equipment, firmware flashing path
    Evidence requirement       Unit/integration tests, lint, type checks, security scan,   Simulation logs, formal properties, HIL logs, timing
                               reviewer checklist                                          analysis, regression matrix
    Risk class                 Prototype, production, regulated, security-sensitive        Lab prototype, field firmware, safety-related, manu-
                                                                                           facturing release


                                                                   TABLE II
                                      R ISK - ADAPTIVE ACCEPTANCE GATES FOR AGENT- GENERATED ARTIFACTS .

    Risk Level             Typical Tasks                            Required Evidence                        Human Gate
    R0: exploratory        Throwaway prototype, internal            Smoke test or manual run; no pro-        Optional review
                           demo, draft script                       duction credentials
    R1: routine            Documentation, small refactor, non-      Targeted tests, lint/type checks, diff   Normal code review
                           critical UI polish                       summary
    R2: production         Feature change, bug fix, public API,     Regression tests, CI, static/security    Mandatory reviewer approval
                           database migration                       checks, rollback plan
    R3: high assurance     Security,     payments,    medical,      Traceable requirements, indepen-         Explicit sign-off and release gate
                           firmware, hardware, safety-related       dent tests, simulation/formal/HIL as
                           behavior                                 applicable, audit artifact



           IX. R ISK -A DAPTIVE ACCEPTANCE G ATES                                                     X. D ISCUSSION
                                                                            A. Implications for Teams
  Not all tasks require the same rigor. Table II defines four
acceptance levels.                                                            Teams adopting agentic development should avoid both
  The acceptance rule is:                                                   overconfidence and rejection. The practical steps are:
       Agent output is not accepted because it is plausible;                1) Maintain minimal repository instructions such as
       it is accepted because it satisfies evidence appropri-                  AGENTS.md, but keep them short, current, and testable.
       ate to its risk level.                                               2) Use task templates for features, bugs, tests, and hardware
                                                                               work.
                                                                            3) Require agents to inspect, summarize, and plan before
A. Evidence Bundle                                                             editing.
                                                                            4) Require tests or equivalent evidence before acceptance.
  For R2 and R3 tasks, the paper recommends a minimum
                                                                            5) Separate implementation and verification agents where risk
evidence bundle:
                                                                               is high.
• task brief and requirement identifiers;                                   6) Track review load, defect escape, rework, and lead time
• agent plan and affected files;                                               rather than only code volume.
• executed commands and test results;
• diff summary and known residual risks;                                    B. Implications for Tool Builders
• trace from acceptance criteria to tests;
                                                                               Tool builders should optimize not only for code generation
• reviewer decision and follow-up actions;
                                                                            but for evidence generation. Useful tool capabilities include
• rollback or recovery path for production changes.
                                                                            structured brief editors, dependency setup capture, test dis-
   For hardware or firmware, the evidence bundle should                     covery, traceability, risk classification, permission gates, sand-
include simulation logs, formal check results where applicable,             boxed execution, review summaries, and exportable evidence
HIL records, toolchain version, board revision, and timing or               bundles. The direction of the ecosystem, including Open-
protocol evidence.                                                          Hands, GitHub agent workflows, Antigravity-style artifacts,
and agent standards, is toward orchestration and observability                                XIII. C ONCLUSION
rather than simple autocomplete [21], [23]–[25].
                                                                        Agentic AI is changing software and hardware development,
C. Implications for Hardware and Embedded Engineering                but it does not make engineering process obsolete. The evi-
   For embedded and hardware teams, the process should be            dence rejects both extremes: agentic coding is not merely a
even stricter. Agents can assist with drivers, register defini-      toy, but neither is it a universal productivity multiplier. Its
tions, test harnesses, assertions, and documentation, but they       value depends on context, constraints, execution environments,
must not bypass timing, protocol, safety, or HIL gates. Hard-        verification gates, and human oversight.
ware benchmarks suggest that realistic system-level generation          This paper proposed Agentic Agile-V, combining Agile-V
and verification remain difficult [27], [28], [31].                  lifecycle discipline with the SCOPE-V task loop. The central
D. Threats to Validity                                               message is that conversation is good for discovering intent,
                                                                     but structured artifacts are required for implementation. Code,
   This paper is a synthesis and process proposal, not a new
                                                                     tests, documentation, firmware, and hardware designs should
benchmark. The field is moving quickly, and point estimates
                                                                     be accepted only when they produce evidence appropriate to
from 2024 to 2026 may change as models and tools evolve.
                                                                     their risk level. The future of agentic engineering is not vibe
Productivity studies vary by task type, developer experience,
                                                                     coding at scale. It is verified engineering with agents inside
codebase maturity, tool generation, and organizational culture.
                                                                     the loop.
Hardware benchmarks differ in design complexity and veri-
fication rigor. The framework should therefore be validated
                                                                                                  R EFERENCES
empirically in future studies across multiple teams, reposito-
ries, tools, and hardware domains.                                    [1] C. Koch and J. A. Wellbrock, “Agile V: A Compliance-Ready Frame-
                                                                          work for AI-Augmented Engineering – From Concept to Audit-Ready
                 XI. P RACTICAL T EMPLATES                                Delivery,” arXiv:2602.20684, 2026. [Online]. Available: https://arxiv.
A. Feature Brief Template                                                 org/abs/2602.20684
                                                                      [2] J. Liu et al., “Large Language Model-Based Agents for Software
   A feature brief should include: objective, user-visible behav-         Engineering: A Survey,” arXiv:2409.02977, 2024. [Online]. Available:
ior, non-goals, affected modules, interface contracts, migration          https://arxiv.org/abs/2409.02977
                                                                      [3] Y. Dong et al., “A Survey on Code Generation with LLM-based Agents,”
needs, compatibility constraints, security considerations, ac-            arXiv:2508.00083, 2025. [Online]. Available: https://arxiv.org/abs/2508.
ceptance criteria, tests to add or update, and rollback path.             00083
                                                                      [4] E. Paradis et al., “How much does AI impact development speed? An
B. Bug Brief Template                                                     enterprise-based randomized controlled trial,” arXiv:2410.12944, 2024.
  A bug brief should include: observed behavior, expected                 [Online]. Available: https://arxiv.org/abs/2410.12944
                                                                      [5] J. Becker, N. Rush, E. Barnes, and D. Rein, “Measuring the Impact of
behavior, reproduction steps, input data, logs/traces, environ-           Early-2025 AI on Experienced Open-Source Developer Productivity,”
ment, affected version, suspected area, failing test if available,        arXiv:2507.09089, 2025. [Online]. Available: https://arxiv.org/abs/2507.
constraints on fix scope, and regression-test requirement.                09089
                                                                      [6] S. Maier, M. Gunzenhaeuser, J. Schweisthal, M. Schneider, and S.
C. Hardware/Firmware Brief Template                                       Feuerriegel, “A meta-analysis of the effect of generative AI on produc-
                                                                          tivity and learning in programming,” arXiv:2605.04779, 2026. [Online].
   A hardware or firmware brief should include: board re-                 Available: https://arxiv.org/abs/2605.04779
vision, chip or FPGA variant, datasheet excerpts, register            [7] A. Mohamed, M. Assi, and M. Guizani, “The Impact of LLM-Assistants
map, pinout, clock tree, bus/protocol rules, memory map,                  on Software Developer Productivity: A Systematic Literature Review,”
                                                                          arXiv:2507.03156, 2025. [Online]. Available: https://arxiv.org/abs/2507.
RTOS/bare-metal assumptions, timing and power constraints,                03156
safety states, toolchain, simulator, HIL setup, and acceptance        [8] H. Li, H. Zhang, and A. E. Hassan, “AIDev: Studying AI Coding Agents
evidence.                                                                 on GitHub,” arXiv:2602.09185, 2026. [Online]. Available: https://arxiv.
                                                                          org/abs/2602.09185
                 XII. R ESEARCH AGENDA                                [9] G. Pinna, J. Gong, D. Williams, and F. Sarro, “Comparing AI Cod-
                                                                          ing Agents: A Task-Stratified Analysis of Pull Request Acceptance,”
  Future work should evaluate Agentic Agile-V empirically.                arXiv:2602.08915, 2026. [Online]. Available: https://arxiv.org/abs/2602.
Key questions include:                                                    08915
                                                                     [10] M. Watanabe, H. Li, Y. Kashiwa, B. Reid, H. Iida, and A. E. Hassan,
1) Do structured execution briefs improve agent success com-              “On the Use of Agentic Coding: An Empirical Study of Pull Requests
   pared with conversational prompts?                                     on GitHub,” arXiv:2509.14745, 2025. [Online]. Available: https://arxiv.
2) What is the minimum useful content of repository instruc-              org/abs/2509.14745
   tions?                                                            [11] M. Galster, S. Mohsenimofidi, J. L. Lulla, M. A. Abubakar, C. Treude,
                                                                          and S. Baltes, “Configuring Agentic AI Coding Tools: An Exploratory
3) Does independent agentic test generation reduce defect                 Study,” arXiv:2602.14690, 2026. [Online]. Available: https://arxiv.org/
   escape?                                                                abs/2602.14690
4) Which task classes benefit from Agile-V/SCOPE-V and               [12] J. L. Lulla, S. Mohsenimofidi, M. Galster, J. M. Zhang, S. Baltes, and
                                                                          C. Treude, “On the Impact of AGENTS.md Files on the Efficiency of
   which are slowed by overhead?                                          AI Coding Agents,” arXiv:2601.20404, 2026. [Online]. Available: https:
5) Can evidence bundles reduce verification debt without                  //arxiv.org/abs/2601.20404
   eliminating productivity gains?                                   [13] T. Gloaguen, N. Muendler, M. Mueller, V. Raychev, and M. Vechev,
                                                                          “Evaluating AGENTS.md: Are Repository-Level Context Files Helpful
6) How should hardware and firmware evidence quality be                   for Coding Agents?” arXiv:2602.11988, 2026. [Online]. Available: https:
   measured?                                                              //arxiv.org/abs/2602.11988
[14] D. McMillan, “Instruction Adherence in Coding Agent Configu-
     ration Files: A Factorial Study of Four File-Structure Variables,”
     arXiv:2605.10039, 2026. [Online]. Available: https://arxiv.org/abs/2605.
     10039
[15] Z. Ni et al., “GitTaskBench: A Benchmark for Code Agents
     Solving Real-World Tasks Through Code Repository Leveraging,”
     arXiv:2508.18993, 2025. [Online]. Available: https://arxiv.org/abs/2508.
     18993
[16] H. Wang et al., “RepoMaster: Autonomous Exploration and Un-
     derstanding of GitHub Repositories for Complex Task Solving,”
     arXiv:2505.21577, 2025. [Online]. Available: https://arxiv.org/abs/2505.
     21577
[17] T. Han et al., “SWE-Skills-Bench: Do Agent Skills Actually Help in
     Real-World Software Engineering?” arXiv:2603.15401, 2026. [Online].
     Available: https://arxiv.org/abs/2603.15401
[18] I. Badertdinov, M. Nekrashevich, A. Shevtsov, and A. Golubev, “SWE-
     rebench V2: Language-Agnostic SWE Task Collection at Scale,”
     arXiv:2602.23866, 2026. [Online]. Available: https://arxiv.org/abs/2602.
     23866
[19] Z. Jiang, D. Lo, and Z. Liu, “Agentic Software Issue Resolution with
     Large Language Models: A Survey,” arXiv:2512.22256, 2025. [Online].
     Available: https://arxiv.org/abs/2512.22256
[20] C. Li et al., “Advances and Frontiers of LLM-based Issue Resolution
     in Software Engineering: A Comprehensive Survey,” arXiv:2601.11655,
     2026. [Online]. Available: https://arxiv.org/abs/2601.11655
[21] X. Wang et al., “The OpenHands Software Agent SDK: A Composable
     and Extensible Foundation for Production Agents,” arXiv:2511.03690,
     2025. [Online]. Available: https://arxiv.org/abs/2511.03690
[22] T. Warren, “GitHub’s new AI coding agent can fix bugs for you,”
     The Verge, 2025. [Online]. Available: https://www.theverge.com/news/
     669339/github-ai-coding-agent-fix-bugs
[23] T. Warren, “GitHub is launching a hub for multiple AI coding agents,”
     The Verge, 2025. [Online]. Available: https://www.theverge.com/news/
     808032/github-ai-agent-hq-coding-openai-anthropic
[24] D. Preston, “Google Antigravity is an agent-first coding tool built for
     Gemini 3,” The Verge, 2025. [Online]. Available: https://www.theverge.
     com/news/822833/google-antigravity-ide-coding-agent-gemini-3-pro
[25] S. Levy, “OpenAI, Anthropic, and Block Are Team-
     ing     Up       to    Make    AI     Agents    Play    Nice,”    Wired,
     2025.          [Online].    Available:      https://www.wired.com/story/
     openai-anthropic-and-block-are-teaming-up-on-ai-agent-standards
[26] Z. Ji, Z. Li, W. Jiang, Y. Gao, and S. Wang, “Measuring the Permis-
     sion Gate: A Stress-Test Evaluation of Claude Code’s Auto Mode,”
     arXiv:2604.04978, 2026. [Online]. Available: https://arxiv.org/abs/2604.
     04978
[27] P. Jin et al., “RealBench: Benchmarking Verilog Generation Models with
     Real-World IP Designs,” arXiv:2507.16200, 2025. [Online]. Available:
     https://arxiv.org/abs/2507.16200
[28] G.-W. Wan et al., “FIXME: Towards End-to-End Benchmarking of
     LLM-Aided Design Verification,” arXiv:2507.04276, 2025. [Online].
     Available: https://arxiv.org/abs/2507.04276
[29] J. Pan, G. Zhou, C.-C. Chang, I. Jacobson, J. Hu, and Y. Chen, “A
     Survey of Research in Large Language Models for Electronic Design
     Automation,” arXiv:2501.09655, 2025. [Online]. Available: https://arxiv.
     org/abs/2501.09655
[30] C. Guo et al., “A Survey: Collaborative Hardware and Software De-
     sign in the Era of Large Language Models,” arXiv:2410.07265, 2024.
     [Online]. Available: https://arxiv.org/abs/2410.07265
[31] Q. Xu, L. Stok, R. Drechsler, X. Wang, G. L. Zhang, and I. L. Markov,
     “Revolution or Hype? Seeking the Limits of Large Models in Hardware
     Design,” arXiv:2509.04905, 2025. [Online]. Available: https://arxiv.org/
     abs/2509.04905
[32] F. Xu, P. K. Medappa, M. M. Tunc, M. Vroegindeweij, and J.
     C. Fransoo, “AI-assisted Programming May Decrease the Productiv-
     ity of Experienced Developers by Increasing Maintenance Burden,”
     arXiv:2510.10165, 2025. [Online]. Available: https://arxiv.org/abs/2510.
     10165
[33] M. Alenezi, “Rethinking Software Engineering for Agentic AI Systems,”
     arXiv:2604.10599, 2026. [Online]. Available: https://arxiv.org/abs/2604.
     10599
