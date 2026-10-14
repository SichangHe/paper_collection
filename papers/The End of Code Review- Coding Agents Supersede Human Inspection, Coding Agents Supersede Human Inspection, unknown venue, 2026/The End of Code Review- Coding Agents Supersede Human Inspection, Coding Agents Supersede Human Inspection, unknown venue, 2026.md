                                                          The End of Code Review:
                                                  Coding Agents Supersede Human Inspection
                                                                                                Martin Monperrus
                                                                                        KTH Royal Institute of Technology
                                                                                             Stockholm, Sweden
                                                                                              monperrus@kth.se


                                            Abstract—Code review has been the primary quality gate in        that agents can produce inline defect comments at quality
                                         software development since Fagan formalised code inspection in      comparable to trained human reviewers [11], [12].
                                         1976. For five decades, having a human examine and comment            In this paper, we make a strong claim: coding agents
arXiv:2606.13175v1 [cs.SE] 11 Jun 2026




                                         on a colleague’s changes before merge has been a cornerstone
                                         practice at organisations of every size. Coding agents are large    have reached a capability threshold at which human code
                                         language model (LLM)-based autonomous systems capable of            review is redundant and should be replaced by agent-driven
                                         reading, writing, testing, and repairing software. We argue         verification. We do not present a new empirical study; instead,
                                         that coding agents have crossed a threshold of capability at        we synthesise existing capability evidence, and enumerate
                                         which traditional human code review is no longer a necessary        the implications for software engineering practice, tooling,
                                         component of a software quality pipeline. Our argument rests on
                                         two claims: every stated goal of code review can be served by       and research. Specifically, we argue that agents can satisfy
                                         agents at lower cost and higher throughput; the naive integration   the established goals of review, that the intermediate model
                                         in which agents write code and humans remain the mandatory          in which agents write code but humans remain mandatory
                                         reviewers is a dead end because it neither provides meaningful      reviewers is unstable, and that the economics of mandatory
                                         assurance nor scales with AI-assisted throughput.                   human inspection have already turned negative for routine
                                                                                                             changes.
                                                               I. I NTRODUCTION                                To sum up, our contributions are:
                                                                                                                • The demonstration that every stated goal of code
                                            Code review is the dominant human quality gate in modern
                                                                                                                   review—defect detection, style enforcement, knowledge
                                         software development. Since Bacchelli and Bird surveyed its
                                                                                                                   transfer, and team awareness—can be met by coding
                                         practice at Microsoft [1] and Sadowski et al. documented
                                                                                                                   agents at lower cost and higher throughput than human
                                         it at Google [2], the field has understood code review as
                                                                                                                   reviewers.
                                         serving four overlapping goals: finding defects before they
                                                                                                                • The argument that combining AI code generation with
                                         reach production, enforcing style and conventions, transfer-
                                                                                                                   mandatory human review is not a stable endpoint: it
                                         ring knowledge between team members, and building shared
                                                                                                                   creates the appearance of assurance while turning review
                                         awareness of the evolving codebase. No serious software team
                                                                                                                   capacity into the next delivery bottleneck.
                                         omits it.
                                                                                                                • The cost-benefit analysis showing that mandatory human
                                            Yet code review carries substantial costs that are often               inspection has already flipped; agent reviews are instan-
                                         underappreciated. Developers at large organisations spend                 taneous, consistent, and auditable, while the marginal
                                         between ten and fifteen percent of their working hours reading            defect-detection value of human review shrinks as agent
                                         and commenting on others’ code [2]. The review latency                    capabilities grow.
                                         between submitting a pull request and receiving actionable
                                         feedback routinely stretches over twenty-four hours and can                              II. BACKGROUND
                                         extend to days, imposing a structural drag on continuous-
                                         delivery [3]. Beyond time, review generates social friction:        A. Code Review: History and Practice
                                         tone escalations, seniority bias, and the well-documented             Code review as a formal engineering discipline originates
                                         tendency for first-time contributors to abandon projects after      with Fagan’s 1976 paper on code inspections at IBM [13].
                                         critical feedback [4], [5].                                         Fagan proposed a structured, multi-stage process: planning,
                                            Into this landscape, coding agents have arrived. LLM-based       overview, preparation, inspection, rework, and follow-up. The
                                         systems such as Claude Code, Codex, and GitHub Copilot              process was presented as expensive, requiring up to three
                                         can now read and modify files, execute test suites, interpret       percent of total project effort.
                                         compiler output, and iteratively repair failures without human        The empirical record on the effectiveness of modern code
                                         direction [6]–[9]. On SWE-bench (a benchmark of real, un-           review is more nuanced than the practice’s universal adoption
                                         modified GitHub issues drawn from popular Python libraries),        might suggest. Bacchelli and Bird found that defect detection,
                                         state-of-the-art agents resolve more than eighty percent of         while a primary motivation, is not what reviewers most reliably
                                         tasks end-to-end [10]. Work on LLM-based code review shows          deliver: style corrections, minor improvements, and questions
           Goal 1                                                                                                                Implication 1
                                               Claim 1
    Bug & defect detection
                                        All review goals met by                                                             Merge workflow redesign
                                         agents at lower cost                                                                to agent-in-loop gates
           Goal 2
       Security analysis                                                                                                         Implication 2
                                               Claim 2                                                                         Team roles shift to
                                                                                  CONCLUSION                                 specifier & orchestrator
           Goal 3                     Human review of agent code
                                           is the bottleneck                 Agent review supersedes
         Code quality
                                                                           mandatory human code review                           Implication 3
                                                                                                                           Open-source & onboarding
           Goal 4                              Claim 3                                                                     feedback loop compression
      Knowledge transfer
                                        Cost-benefit balance of
                                       human review has flipped                                                                  Implication 4
           Goal 5                                                                                                             CI/CD, IDE & platform
     Standards compliance                                                                                                    tooling for agent review




Fig. 1. Argument map of the paper. Review goals support three claims that lead to the conclusion, which entails four implications for practice and tooling.



about intent dominate the comment corpus [1]. Czerwonka                          To our knowledge, this paper is the first to argue for the
et al. reached the pointed conclusion that code reviews at                     complete displacement of mandatory human code review by
Microsoft “do not find bugs” in the sense of catching deep,                    coding agents, and to discuss the resulting implications for
logic-level defects; their primary value lies in knowledge                     workflow, tooling and research.
transfer and maintainability improvement [14]. Knowledge
                                                                               C. Coding Agents
transfer and socialisation emerge consistently across studies
as valued outcomes of the review interaction [1], [4].                            A coding agent is a system in which a large language
                                                                               model (LLM) is embedded in an agentic loop: the model
B. Automated Code Review
                                                                               can invoke tools for reading and writing files, executing shell
   Efforts to automate code review predate large language                      commands, running tests, querying documentation, and then
models. Early approaches relied on pattern matching, rule-                     iterate until a goal is achieved or a stopping condition is met.
based checkers, and machine-learning classifiers trained on                    The LLM provides language understanding, code synthesis,
review-comment corpora to predict whether a change would                       and contextual reasoning; the tool loop provides grounding in
attract a comment and what that comment would say. These                       the actual state of the software artefact and its execution.
systems automated individual review activities in isolation:                      Representative agents include OpenAI Codex [18], an inter-
comment prediction, priority ranking of changed files, detec-                  active assistant built on top of the GPT line of models; Claude
tion of specific defect classes.                                               Code [19], an agentic coding assistant that operates directly
   The LLM era opened new possibilities. CodeReviewer [11]                     in the developer’s terminal; SWE-agent [6], which introduces
pre-trains a model on a large corpus of pull-request diffs                     an agent-computer interface optimised for repository-scale
and associated review comments, achieving competitive per-                     software engineering tasks; Devin [7], a commercial system
formance on comment generation, code-refinement predic-                        that autonomously navigates codebases and deploys fixes; and
tion, and severity classification. LLaMA-Reviewer [15] ap-                     GitHub Copilot [9], which integrates agent capabilities directly
plies parameter-efficient fine-tuning to adapt a general-purpose               into the pull-request workflow.
LLM for the review-comment generation task, demonstrating
that strong review performance is achievable with fine-tuning.                              III. E VIDENCE OF AGENT C APABILITY
Tufano et al. [16] build an end-to-end pipeline from diff                        To support the claim that coding agents can displace hu-
to refined patch, showing that a model can both generate                       man code review, we survey evidence of agent capability
a review comment and produce the corrected code, elimi-                        across three dimensions: benchmark performance on software-
nating one round-trip in the review-revise cycle. Pornprasit                   engineering tasks, review-specific capabilities, and developer
and Tantithamthavorn evaluate these and related systems in                     productivity with deployed tools.
industrial settings and find meaningful coverage across defect
types [12]. Tang et al. introduce CodeAgent [17], a multi-agent                A. Benchmark Performance
system in which specialised communicative agents collaborate                      The most direct evidence for agent capability comes from
to perform code review, pushing the automation boundary from                   SWE-bench, a benchmark that evaluates whether a system
single-model comment generation toward coordinated agent                       can resolve real, unmodified issues drawn from popular open-
workflows. What these systems share is a focus on automating                   source Python projects [10]. Unlike synthetic coding chal-
activities within a review workflow that remains human-                        lenges, SWE-bench tasks require understanding issue descrip-
governed; they improve the efficiency of specific steps without                tions, navigating multi-file repositories, modifying the correct
questioning whether the overall review gate is necessary.                      files, and producing patches that pass the project’s existing test
suite. Early results were sobering: GPT-4 with retrieval-based           Defect detection. Human reviewers are effective at identify-
context selection resolved approximately 1.7 % of tasks. SWE-         ing surface-level issues but unreliable at catching deep logical
agent, by introducing an agent-computer interface that struc-         bugs [14]. Agents powered by large language models, by
tures the model’s interaction with the file system and shell,         contrast, can perform exhaustive dataflow reasoning, cross-
raised this figure to approximately 12.5 % [6]. By late 2024,         reference the full test suite, and apply learned patterns
the best-performing systems on SWE-bench Verified—a cu-               from millions of open-source repositories. Recent work
rated subset with verified ground-truth resolutions—exceeded          shows that LLM-based review systems produce actionable
50 %. By late 2025, top agents on the public leaderboard              defect reports comparable in quality to those of trained human
resolved more than 70 % of tasks [20]. The improvement                reviewers, while operating on every commit without fatigue or
trajectory, from under two percent to over seventy percent            time-zone constraints [11], [12].
in roughly two years, is without precedent in the history of             Style and standards enforcement. Linters, formatters, and
automated software engineering tools.                                 type checkers have long handled syntactic and stylistic con-
   Related evidence comes from adjacent tasks. For example,           cerns automatically. Agents extend this capacity to semantic
Xia et al. demonstrate that LLM-based repair approaches               style: naming consistency, idiomatic API usage, and docu-
substantially outperform earlier generate-and-validate systems        mentation conventions can all be enforced through LLM-
like GenProg [21], [22], fixing a far larger proportion of            based rewriting, eliminating an entire category of reviewer
benchmark bugs without requiring manually specified test              comment.
cases or fix templates. At the competitive programming level,            Security. Security review is precisely the domain where
AlphaCode ranked within the top 54 % of human participants            human attention is most overloaded and most consequential.
on Codeforces contests [23]. This establishes that LLMs can           Pearce et al. demonstrate that GitHub Copilot introduces com-
reason about non-trivial algorithmic problems.                        mon weakness enumeration (CWE) violations at non-trivial
                                                                      rates [24], yet the same generation capability, when redirected
B. Review-Specific Capabilities
                                                                      toward detection, allows agents to enumerate vulnerability
   Beyond general software engineering, several strands of            classes far more systematically than a developer performing
work speak specifically to the capabilities that code review re-      an ad-hoc review [25]. AI-based security scanners already
quires. Pornprasit and Tantithamthavorn evaluate LLM-based            outperform many manual reviewers on standard vulnera-
automated review in industrial settings and find that agents          bility benchmarks [26].
detect the same categories of defect that human reviewers                Knowledge transfer. Agents can actively generate on-
target: correctness errors, security weaknesses, performance          demand explanations, architectural summaries, and up-
inefficiencies, and style violations [12]. Li et al. demonstrate      dated documentation at merge time, which is a more re-
that CodeReviewer produces actionable inline comments at              liable and scalable mechanism for propagating knowledge
quality that is at least comparable to those of trained human         than the incidental commentary of a busy colleague.
reviewers on a significant fraction of the evaluation set [11].
   Agents bring capabilities that human reviewers structurally
                                                                      B. Claim 2: The naive integration—AI coding with human
cannot match. A human reviewer reads a diff; an agent can
                                                                      review—is a dead end.
simultaneously hold the full file, the complete test suite,
the git history of every touched function, and the project’s             The first response of most organisations to the rise of AI
documentation in context. A human reviewer can identify a             coding tools is as follows: an agent writes the code, a human
problem and describe it in a comment; an agent can identify           reviews it. This arrangement feels conservative and safe. We
the problem, generate a fix, apply it, run the tests, and close the   argue that it fails on two independent grounds.
review loop without any human scheduling. A human reviewer               Human review provides no genuine assurance. The tra-
has a calendar, a timezone, and finite attention; an agent            ditional rationale for code review rests on a tacit assumption:
operates continuously, applying the same scrutiny at 3 am             human developers write code, and human reviewers provide
on a Sunday as during a Monday morning sprint. These are              an independent check. When an agent generates the code, this
structural advantages that compound as the scale and velocity         assumption collapses. A large language model can produce
of software development increase.                                     hundreds of lines of plausible, internally consistent code
                                                                      that contains subtle semantic errors—errors that are invisible
     IV. T HE E ND OF C ODE R EVIEW: T HE A RGUMENT
                                                                      without running the full test suite or performing the kind
A. Claim 1: Every goal of code review can be served by agents         of exhaustive dataflow analysis that only an agent can do
at lower cost and higher throughput.                                  systematically. Human reviewers, reading a diff on a screen,
  Bacchelli and Bird identify four primary goals of code              are poorly positioned to catch the errors that AI-generated
review: defect detection, style and standards enforcement,            code may contain. In practice, reviews of agent-generated code
knowledge transfer, and team awareness [1]. We argue that             become rubber-stamps: the human approves because the code
contemporary coding agents satisfy each goal at least as              looks correct, because the tests pass, and because the cognitive
well as human reviewers, and in several dimensions markedly           cost of genuine scrutiny is prohibitive [14]. The assurance that
better.                                                               review is supposed to provide is illusory.
   Human review does not scale. AI coding tools increase de-       where a named human must bear legal accountability. For
veloper throughput. A developer assisted by an agent produces      the vast majority of commits (incremental features, bug fixes,
more commits, more pull requests, and more lines of changed        dependency updates, refactors) agent sign-off is sufficient, and
code per day than an unassisted developer [27]. Human review       requiring more is waste.
capacity does not scale and the result is a bottleneck that           Team structure and roles. As agent review matures, the
grows proportionally with the productivity gain that AI coding     role of the professional code reviewer will diminish in its
delivers. Organisations that deploy AI coding tools while          current form. The time developers spend in synchronous re-
retaining human-gated review will find that the review queue       view meetings and asynchronous comment threads will shrink.
becomes the binding constraint on their delivery pipeline. The     This does not mean that developer expertise becomes less
faster the agents write, the longer the queue grows, and the       important; it means that expertise is redirected. Developers
more review degrades into a formality performed under time         increasingly become specifiers and orchestrators: they ar-
pressure. Retaining human review in this context does not          ticulate requirements precisely enough for agents to act on
preserve quality; it discards both the productivity benefit of     them, evaluate agent-produced artefacts at a higher level of
AI coding and the quality benefit of genuine review.               abstraction, and intervene when agent reasoning is uncertain
   The logically consistent step is to close the loop: an in-      or the stakes are high. The craft shifts from line-by-line
dependent agent reviews agent-generated code, with humans          inspection to system-level judgment. This is a change that
intervening only when agents flag uncertainty or a change          many developers will welcome, since surveys consistently
crosses an explicit risk threshold.                                show that reviewing code is among the least enjoyable parts
                                                                   of the job [2].
C. Claim 3: The cost-benefit calculation has flipped.
                                                                      Onboarding and knowledge transfer. One of the most-
   Code review imposes measurable costs: developers at large       cited benefits of code review is its role in propagating knowl-
organisations spend 10–15 % of their working hours reviewing       edge among team members [1]. Agents can generate on-
code [2], and review latency introduces delays into continuous-    demand, context-keyed explanations at merge time that are
delivery pipelines [3], [28]. These costs were historically        richer than what a busy senior engineer provides in a rushed
justified by the defects that review caught. The justification     comment. The genuine risk is a reduction in the informal,
weakens as agent coverage grows.                                   bidirectional conversations through which tacit knowledge and
   Consider the marginal value of a human review comment.          team culture propagate; organisations will need complemen-
As agents scan every file, every test, and every commit with       tary mechanisms such as pair programming and structured
increasing recall, the set of defects that escape agent review     mentorship to preserve this cohesion.
but would be caught by a human reviewer shrinks. At the same          Open-source dynamics. In open-source projects, main-
time, the cost of human review in time, in latency, in social      tainer bandwidth is a structural bottleneck: contributions wait
friction [4], [5], remains constant. The crossover point, at       weeks for review and projects are abandoned not because
which the marginal benefit of human review no longer               patches stop arriving but because maintainers run out of review
justifies its marginal cost, has already been reached. Agent       capacity. Agent review directly addresses this bottleneck,
reviews are instantaneous, deterministic, and auditable: they      compressing feedback loops and lowering the barrier for first-
produce structured reports, not informal threaded comments,        time contributors.
and they can be re-run at any point in the pipeline. The com-
petitive advantage of continuous delivery [28] makes review        B. Implications for Tooling
latency an increasingly unacceptable tax on software teams,           CI/CD integration. Agent review is a natural extension of
and agents eliminate it entirely.                                  the continuous integration pipeline. Just as build systems and
                                                                   test runners execute automatically on every push, a review
                      V. I MPLICATIONS
                                                                   agent can be triggered at the same point, on every commit to
A. Implications for Software Engineering Practices                 a feature branch, or as a mandatory gate before merge. This
   Merge workflow redesign. The most immediate implica-            reframes review from an asynchronous social activity into a
tion of agent-based review is the restructuring of the pull-       first-class engineering check, analogous to compilation: it runs,
request workflow. In the current model, a developer opens a        it reports, and it either passes or blocks [28]. Agents produce
pull request and waits, sometimes for days, for a colleague        structured reports (JSON, SARIF) that CI dashboards, security
to find time to review it. We propose replacing this gating        platforms, and analytics systems can consume without human
step with an agent-in-the-loop verification pipeline that runs     mediation. Review history becomes an engineering artefact,
automatically on every candidate merge. Merge gates shift          versioned and queryable, rather than a thread of informal
from a human approval checkbox to a structured agent sign-         comments that ages poorly.
off: test coverage thresholds, security scan results, style com-      IDE and editor integration. The latency reduction that
pliance reports, and reasoning traces are all produced without     agents enable is not confined to the merge pipeline. An
human scheduling. Human approval is not eliminated; it is          agent embedded in a developer’s editor can review changes
reserved for the decisions that genuinely require it: high-risk    before they are committed: as the developer writes, the agent
changes, novel architecture choices, and regulated code paths      reads context, identifies issues, and surfaces them inline. This
collapses the feedback loop from hours or days to seconds. The     C. Counter-argument: Adversarial inputs and prompt injec-
interaction model also changes: rather than reading a list of      tion.
review comments and deciding whether to accept or dismiss              A sophisticated adversary who can submit a pull request
each one, the developer converses with the agent in natural        may also craft code that, when read by a reviewing agent,
language, asking for explanations, requesting alternative im-      manipulates the agent’s reasoning through embedded natural-
plementations, or negotiating tradeoffs. This is closer to pair    language instructions. A maliciously crafted comment, iden-
programming than to traditional review, and it operates without    tifier, or string literal could instruct the agent to overlook a
the social overhead that makes synchronous pairing difficult       vulnerability or to approve a change it should block. This
to sustain at scale.                                               is an active area of security research with no fully solved
   Version control platforms. For agent review to function         defences [32], and it represents a qualitatively new attack
as a first-class activity, platforms such as GitHub and GitLab     surface that does not exist for human reviewers. Organisations
must extend their identity and permission models to support        deploying agent review must treat agent reviewer prompt
agent actors. An agent reviewer needs a cryptographically          injection as a first-class threat model.
signed identity, the ability to push records in the platform’s
audit log, and the capacity to approve, request changes, or        D. Counter-argument: Architectural coherence requires hu-
block merge in the same way a human reviewer can [9].              man judgment.
The pull-request user interface must evolve accordingly: agent-
                                                                      At the architectural level, reviewers assess whether a change
generated summaries, confidence scores, categorised findings,
                                                                   is consistent with the system’s long-term design: whether a
and inline fix suggestions should be presented as structured
                                                                   new abstraction duplicates an existing one, whether a local
UI components, not as synthetic comment threads that mimic
                                                                   trade-off accumulates strategic technical debt, or whether an
human behaviour. Review history in this model becomes
                                                                   interface decision prevents future extension. These judgements
machine-readable by design: downstream analytics can operate
                                                                   depend on a mental model of the system’s architecture that AI
directly on agent review records (defect trend dashboards,
                                                                   may not yet hold with sufficient fidelity [1].
security posture tracking, codebase health scoring) .
                                                                      This concern misidentifies the scope of what pull-request re-
                                                                   view actually delivers. Architectural coherence is best enforced
                      VI. D ISCUSSION                              through design documents, architecture decision records, and
                                                                   dedicated architecture reviews, not through per-commit diff
A. Counter-argument: Hallucination and false negatives.            inspection. Conflating the two overstates what human PR
   LLMs can miss defects that fall outside their training          review reliably provides, since empirical studies show that
distribution [25]. A human reviewer who is unsure about a          reviewers overwhelmingly focus on surface defects and style
change will typically say so; an LLM may silently produce an       rather than strategic architectural validity [1], [14].
approval. The primary mitigation is ensemble review: running
multiple independent agents, potentially based on different        E. Counter-argument: Ethical accountability requires human
models and prompting strategies, and requiring consensus           judgment.
before sign-off. A second mitigation is calibrated uncertainty        At the ethical level, code changes can carry consequences
reporting: reviewer agents should be trained and evaluated to      for user privacy, algorithmic fairness, and environmental foot-
abstain (“I don’t know”) and emit confidence estimates that        print that require values-based judgement rather than cor-
track empirical correctness, rather than always issuing a binary   rectness verification. Agents are calibrated to optimise for
approval [29].                                                     technical quality metrics; they are not reliably equipped to
                                                                   detect that a telemetry change violates a user’s reasonable
                                                                   privacy expectation or that a ranking modification amplifies
B. Counter-argument: Security vulnerabilities in agent-
                                                                   demographic bias [4]. Legal and organisational accountability
generated code.
                                                                   frameworks assume a named human decision-maker: an auto-
   Pearce et al. demonstrate that GitHub Copilot introduces        mated approval leaves an accountability gap when a change
common weakness enumeration (CWE) violations at non-               causes harm.
trivial rates across a range of security-relevant coding sce-         Agents already flag security-sensitive patterns (PII logging,
narios [24]. When the same model family that generates             insecure randomness, over-privileged API calls) and their
code is also responsible for reviewing it, there is a risk that    coverage of compliance properties is growing [24], [25]. More
generative and review blind spots are correlated: the agent        fundamentally, mandatory PR review is not the appropriate lo-
may fail to flag the very pattern of vulnerability that its        cus for ethical scrutiny of software: this responsibility belongs
generation tendency produces. The mitigation is to use cyber-      in requirements engineering and post-deployment monitoring.
specialized frontier reviewers for security sign-off: recent       Agent review can be governed by the same institutional
benchmark-oriented reports show that the latest models can         mechanisms as other automated quality gates, with human
outperform traditional static analyzers and strong baselines on    escalation reserved for changes that agents flag as uncertain
vulnerability-identification tasks [30], [31].                     or high-risk.
                         VII. C ONCLUSION                                      [11] Z. Li, S. Lu, D. Guo, N. Duan, S. Jannu, G. Jenks, D. Majumder,
                                                                                    J. Green, N. Sundaresan, M. Fu et al., “CodeReviewer: Pre-training
   Code review has served software engineering for five                             for automating code review activities,” in Proceedings of the 30th ACM
decades. From Fagan’s formal inspections [13] to the pull-                          Joint European Software Engineering Conference and Symposium on
request model that now governs millions of daily commits [1],                       the Foundations of Software Engineering (ESEC/FSE). ACM, 2022,
                                                                                    pp. 1536–1546.
having humans read each other’s code before merge has been                     [12] C. Pornprasit and C. Tantithamthavorn, “Automated code review in prac-
treated as a mandatory engineering virtue. We have argued                           tice,” in Proceedings of the 38th IEEE/ACM International Conference
that this assumption no longer holds.                                               on Automated Software Engineering (ASE). IEEE, 2023, pp. 394–405.
                                                                               [13] M. E. Fagan, “Design and code inspections to reduce errors in program
   Coding agents have reached a capability level at which every                     development,” IBM Systems Journal, vol. 15, no. 3, pp. 182–211, 1976.
stated goal of code review can be met automatically, faster,                   [14] J. Czerwonka, M. Greiler, and J. Tilford, “Code reviews do not find
and at a scale that human review cannot match. The transition                       bugs: How the current code review best practice slows us down,” pp.
                                                                                    27–28, 2015.
is already underway for routine changes in industry. Agents                    [15] J. Lu, L. Yu, X. Li, L. Yang, and C. Zuo, “Llama-reviewer: Advancing
review dependency bumps, refactors, and test additions today,                       code review automation with large language models through parameter-
with humans providing oversight only at the margins. The                            efficient fine-tuning,” in Proceedings of the 34th IEEE International
                                                                                    Symposium on Software Reliability Engineering (ISSRE). IEEE, 2023,
open question is not whether this shift will occur, but how                         pp. 647–658.
quickly it will extend from routine changes to the full breadth                [16] R. Tufano, S. Masiero, A. Mastropaolo, L. Pascarella, D. Poshyvanyk,
of software development, and how the profession will manage                         and G. Bavota, “Using pre-trained models to boost code review automa-
                                                                                    tion.” ACM, 2022, pp. 1–12.
that extension.                                                                [17] X. Tang, K. Kim, Y. Song, C. Lothritz, B. Li, S. Ezzini, H. Tian, J. Klein,
   Code review will not disappear overnight. Its role will                          and T. F. Bissyande, “CodeAgent: Autonomous communicative agents
refocus to a layer of high-stakes human oversight: architecture                     for code review,” arXiv preprint arXiv:2402.02172, 2024.
                                                                               [18] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan,
decisions with long-lived consequences, security-critical paths                     H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
in regulated systems, and changes whose correctness depends                         language models trained on code,” arXiv preprint arXiv:2107.03374,
on requirements that no agent has been given access to. For                         2021.
                                                                               [19] Anthropic, “The Claude 3 model family: Opus, Sonnet, Haiku,” An-
everything else, the case for mandatory human review has                            thropic Technical Report, 2024.
already weakened to the point where it is difficult to defend                  [20] S. bench Team, “SWE-bench leaderboard,” https://www.swebench.com,
on technical grounds.                                                               2025.
                                                                               [21] C. Le Goues, T. Nguyen, S. Forrest, and W. Weimer, “A systematic
   The end of code review, as we once thought the absolute                          study of automated program repair: Fixing 55 out of 105 bugs for $8
best practice of modern software engineering, is the beginning                      each,” pp. 3–13, 2012.
of a more productive way to build software.                                    [22] C. S. Xia, Y. Wei, and L. Zhang, “Automated program repair in the era
                                                                                    of large pre-trained language models,” pp. 1482–1494, 2023.
                             R EFERENCES                                       [23] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
                                                                                    T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago et al., “Competition-
 [1] A. Bacchelli and C. Bird, “Expectations, outcomes, and challenges              level code generation with AlphaCode,” Science, vol. 378, no. 6624, pp.
     of modern code review,” in Proceedings of the 35th International               1092–1097, 2022.
     Conference on Software Engineering (ICSE). IEEE, 2013, pp. 712–           [24] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri, “Asleep
     721.                                                                           at the keyboard? assessing the security of GitHub Copilot’s code
 [2] C. Sadowski, E. Söderberg, L. Church, M. Sipko, and A. Bacchelli,              contributions,” in Proceedings of the 43rd IEEE Symposium on Security
     “Modern code review: a case study at Google,” in Proceedings of                and Privacy (SP). IEEE, 2022, pp. 754–768.
     the 40th International Conference on Software Engineering: Software       [25] R. Khoury, A. R. Avci, J. Brunelle, and B. Marc Camara, “How secure
     Engineering in Practice (ICSE-SEIP). ACM, 2018, pp. 181–190.                   is code generated by ChatGPT?” 2023.
 [3] M. Hilton, T. Tunnell, K. Huang, D. Marinov, and D. Dig, “Usage,          [26] J. W. Lin, E. K. Jones, D. J. Jasper, E. J.-s. Ho, A. Wu, A. T. Yang,
     costs, and benefits of continuous integration in open-source projects,”        N. Perry, A. Zou, M. Fredrikson, J. Z. Kolter et al., “Comparing ai
     in Proceedings of the 31st IEEE/ACM International Conference on                agents to cybersecurity professionals in real-world penetration testing,”
     Automated Software Engineering (ASE). ACM, 2016, pp. 426–437.                  arXiv preprint arXiv:2512.09882, 2025.
 [4] A. Bosu, M. Greiler, and C. Bird, “Process aspects and social dynamics    [27] S. Peng, E. Kalliamvakou, P. Cihon, and M. Demirer, “The impact of
     of contemporary code review,” in IEEE Transactions on Software                 AI on developer productivity: Evidence from GitHub Copilot,” arXiv
     Engineering, vol. 43, no. 1. IEEE, 2016, pp. 56–75.                            preprint arXiv:2302.06590, 2023.
 [5] A. Murgia, P. Tourani, B. Adams, and M. Ortu, “Do developers feel         [28] M. Shahin, M. A. Babar, and L. Zhu, “Continuous integration, delivery
     emotions? an exploratory analysis of emotions in software artifacts,”          and deployment: A systematic review on approaches, tools, challenges
     in Proceedings of the 11th Working Conference on Mining Software               and practices,” IEEE Access, vol. 5, pp. 3909–3943, 2017.
     Repositories (MSR). ACM, 2014, pp. 262–271.                               [29] S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez,
 [6] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan,           N. Schiefer, Z. Dodds, N. DasSarma, E. Tran-Johnson, S. Johnston,
     and O. Press, “SWE-agent: Agent-computer interfaces enable automated           S. El-Showk, A. Jones, N. Elhage, T. Hume, A. Chen, Y. Bai, S. Bow-
     software engineering,” arXiv preprint arXiv:2405.15793, 2024.                  man, S. Fort, D. Ganguli, D. Hernandez, J. Jacobson, J. Kernion,
 [7] Cognition AI, “Introducing Devin, the first AI software engineer,” Cog-        S. Kravec, L. Lovitt, K. Ndousse, C. Olsson, S. Ringer, D. Amodei,
     nition AI Blog, 2024, https://www.cognition.ai/blog/introducing-devin.         T. B. Brown, J. Clark, N. Joseph, B. Mann, S. McCandlish, C. Olah,
 [8] X. Wang, B. Chen, Y. Yuan, Y. Zhang, B. Li, C. Qian et al., “OpenDevin:        and J. Kaplan, “Language models (mostly) know what they know,” arXiv
     An open platform for AI software developers as generalist agents,” in          preprint arXiv:2207.05221, 2022.
     arXiv preprint arXiv:2407.16741, 2024.                                    [30] A. Yildiz, S. G. Teo, Y. Lou, Y. Feng, C. Wang, and D. M. Divakaran,
 [9] GitHub, “GitHub Copilot Workspace: Welcome to the Copilot-                     “Benchmarking llms and llm-based agents in practical vulnerability
     native developer environment,” GitHub Blog, 2024, https://github.blog/         detection for code repositories,” arXiv preprint arXiv:2503.03586, 2025.
     2024-04-29-github-copilot-workspace/.                                     [31] Berkeley Risk and Decisions Initiative, “Frontier ai’s impact on the
[10] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and               cybersecurity landscape (paper summary and blog),” https://rdi.berkeley.
     K. Narasimhan, “SWE-bench: Can language models resolve real-GitHub             edu/frontier-ai-impact-on-cybersecurity/, 2025.
     issues?” arXiv preprint arXiv:2310.06770, 2023.                           [32] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz,
                                                                                    “Not what you’ve signed up for: Compromising real-world LLM-
                                                                                    integrated applications with indirect prompt injection,” arXiv preprint
                                                                                    arXiv:2302.12173, 2023.
