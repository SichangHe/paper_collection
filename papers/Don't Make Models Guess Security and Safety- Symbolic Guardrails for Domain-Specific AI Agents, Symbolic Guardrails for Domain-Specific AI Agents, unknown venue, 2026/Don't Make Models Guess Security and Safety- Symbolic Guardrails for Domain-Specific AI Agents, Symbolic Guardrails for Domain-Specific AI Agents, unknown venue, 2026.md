                                          Don’t Make Models Guess Security and Safety:
                                        Symbolic Guardrails for Domain-Specific AI Agents
                                                     Yining Hong*, Yining She, Eunsuk Kang, Christopher S. Timperley and Christian Kästner
                                                                                            Carnegie Mellon University
                                                                                            *yhong3@andrew.cmu.edu


                                           Abstract—There is increasing interest in integrating AI agents        Study 1: Security and safety requirements in AI agent benchmarks
                                        that invoke tools into domain-specific commercial software, where
                                        unintended tool calls can cause serious security and safety                                                          Policy: “As an airline agent,
                                                                                                                                                             you help users book, modify,
                                                                                                                                                                                                       Not verifiable
                                                                                                                                                                                                       (implicit/          85%
                                        incidents. This has drawn growing research attention, and many                                                       or cancel flight reservations.            goals only)
                                                                                                                                                             - You should not give
                                        agent security and safety benchmarks have emerged. They                                                              subjective comments                       Verifiable
                                                                                                                                                                                                                           9%
arXiv:2604.15579v2 [cs.SE] 5 Jul 2026




                                                                                                                                                             - Only assist users with their
                                        implicitly shape how the community approaches security and                systematic             AI agent            own reservations
                                                                                                                                                                                                       (in principle)
                                                                                                                   lit. review        security/safety        - No operation is allowed
                                        safety. Yet existing work exhibits a blind spot: it emphasizes                                 benchmarks            before user is authenticated
                                                                                                                                                                                              security/safety policy
                                        training-based methods and neural guardrails, which reduce                                                           - …”
                                                                                                                                                                                              (set of requirements)
                                        the likelihood of insecure or unsafe actions but cannot guar-            Key finding: Security / safety policies in 85% of agent benchmarks not verifiable
                                        antee their prevention. It generally overlooks opportunities for
                                        deductive, symbolic guardrails grounded in standard software            Study 2: Symbolic enforceability of security and safety requirements
                                        engineering practices, which can provide guarantees for some
                                        security and safety requirements. Our study has three parts: (1)                                  Requirement: “You should not give                 Not Enforceable
                                                                                                                                                                                                                           26%
                                                                                                                                          subjective comments.”                           by symbolic guardrails
                                        a systematic review of 80 agent security and safety benchmarks
                                        finding that that 85% of benchmarks do not state verifiable                                       Requirement: “Only assist users
                                                                                                                                                                                            Enforceable
                                                                                                                                                                                          by API validation
                                                                                                                                          with their own reservations”
                                        requirements (61% provide none, and 24% give only high-                 security/safety                                                     assert(user==ticket.user)
                                                                                                                 requirements                                                                                              74%
                                        level goals); (2) an applicability analysis of which security                from                 Requirement: “No operation is
                                                                                                                                                                                             Enforceable
                                                                                                                   τ2-bench                                                                by temporal logic
                                        and safety requirements symbolic guardrails can and cannot               CAR-bench
                                                                                                                                          allowed before user is authentic.”
                                                                                                                                                                                     ¬toolCall W authenticate
                                        enforce on τ 2 -Bench, CAR-bench, and MedAgentBench, finding            MedAgentBench                                                                       …
                                        that 74% of requirements are symbolically enforceable and               Key finding: 74% requirements symbolically enforceable, most w/ simple methods
                                        95% of these need only simple, low-cost checks; and (3) an
                                        empirical evaluation of symbolic guardrails on the same three                        Study 3: Effect of symbolic guardrails on AI agents
                                        benchmarks, finding that symbolic guardrails improve security
                                        and safety without sacrificing utility, and often improve it. Our                                   Security/safety violation rate
                                                                                                                                            (tasks violating enf. requirement)
                                                                                                                                                                                       20-78% → 0%
                                                                                                                                                                                      without / with symb. guardrails
                                        work draws attention to the potential for symbolic guardrails
                                                                                                                  benchmark
                                        for AI agents, suggesting them as an overlooked but practical              execution                Utility                                                         in τ2-bench,
                                                                                                                                                                                       36% → 48% similar for others
                                                                                                                                            (tasks successfully completed)
                                        path toward deploying domain-specific AI agents in risk-averse           with and without
                                                                                                                symbolic guardrails
                                                                                                                                                                                      without / with symb. guardrails

                                        commercial software. We release all codes and artifacts at                  Key finding: Agent without symbolic guardrails often violate enforceable
                                        https://github.com/hyn0027/agent-symbolic-guardrails.                    security/safety requirements; symbolic guardrails improve, not undermine utility
                                           Index Terms—AI Agents, Software Security, Agent Safety,
                                        Agent Security, Symbolic Guardrails                                                  Fig. 1: Overview of the three-part study.

                                                              I. I NTRODUCTION
                                           AI agent security and safety have become an active re-              However, current benchmarks do not capture the needs of
                                        search area [1], [2]. This paper argues that current agent          risk-averse commercial applications. AI agents are increas-
                                        security and safety benchmarks exhibit a large blind spot:          ingly deployed not just as personal assistants but to automate
                                        they emphasize alignment (training the LLM to internalize           business functions at scale, such as customer support [5],
                                        human preferences) and neural guardrails (auxiliary LLMs that       healthcare [6], and software development [7], yet many orga-
                                        screen agent traces), so that agents meet vague common-sense        nizations are wary of risks. Individual users may accept some
                                        security and safety expectations. However, these benchmarks         personal risk when adopting assistants such as OpenClaw [8],
                                        overlook effective and widely applicable symbolic guardrails        but when agents act on behalf of a company, a single inci-
                                        grounded in standard software engineering practices, such as        dent can have serious consequences, such as compromising
                                        precondition checks on tool calls, schema enforcement, and          customer accounts [9] or authorizing transactions that violate
                                        least-privilege design. Benchmarks do not merely measure            company policies [10]; such risks fall centrally on the system
                                        progress; they direct it [3], [4]. By enumerating what counts as    operator. Agents are more secure and safer when stronger
                                        success and failure, benchmarks implicitly define the problem       LLMs and neural guardrails are used: in our study, upgrading
                                        the community optimizes for. The security and safety require-       the LLM from GPT-4o to GPT-5 cuts the rate of runs violating
                                        ments that benchmarks encode thus serve as the operational          security and safety requirements in τ 2 -Bench [11] from 52%
                                        definition of a secure or safe agent, and the defenses that the     to 20%. Yet it is unclear how continued progress of this kind
                                        community builds are the ones these benchmarks reward.              can instill enough confidence to deploy a commercial system
when a single incident, such as a leaked patient database or       cess [24], [25]. Our experiments show the opposite. Symbolic
an irreversible transaction, can cause severe damage [12]. The     guardrails eliminate a large class of violations of enforceable
relevant question in such risk-averse settings is therefore not    requirements (which occur in 20% to 78% of tasks when the
how an agent usually behaves, but whether certain actions can      requirements are given only in the prompt and judgment is
be ruled out, even under an adversary; this is a guarantee that    left to the model), while maintaining or improving the task
neural defenses, inductive by definition, cannot provide.          completion rate. One explanation is that symbolically blocked
   In this work, we examine whether current benchmarks, as a       actions give the agent clear feedback to reflect and retry with
proxy for the community’s attention, support building agents       a safe alternative, rather than finishing with the wrong result.
for high-assurance settings. As in Fig. 1, we conducted a             Overall, we contribute the first systematic characteriza-
three-part study: a systematic literature review of 80 agent       tion of whether and how agent benchmarks specify verifi-
security and safety benchmarks (Sec. III), an applicability        able security and safety requirements, a mapping from these
analysis of which requirements are (not) symbolically en-          requirements to the symbolic mechanisms that can enforce
forceable across three benchmarks (Sec. IV), and an empirical      them, and evidence that such enforcement does not degrade
evaluation of how symbolic guardrails affect agent security,       agent utility. These results suggest that symbolic guardrails
safety, and utility (Sec. V). We reached three major findings:     are an overlooked but practical path toward deploying domain-
   First, 85% of security and safety benchmarks do not             specific agents in risk-averse commercial applications.
state verifiable requirements. Of the 80 identified bench-
                                                                             II. BACKGROUND AND R ELATED W ORK
marks, 61% provide no security or safety requirements on
agent behaviors, expecting agents to follow unstated common-       A. Security and Safety Requirements
sense norms; another 24% provide only high-level goals with           The terms security and safety are often used loosely across
operative terms undefined, such as “If user requests anything      fields, by both practitioners and researchers. This looseness
unsafe, do not fulfill” [13] with unsafe unexplained. Engineers    is central to our study: we examine what security and safety
cannot assure what they cannot specify, so most benchmarks         expectations are encoded in current agent benchmarks, and the
offer limited insight for high-assurance settings. Notably,        imprecision of these terms is itself part of our findings.
the few benchmarks with verifiable requirements all target            At a high level, security and safety requirements both aim to
domain-specific agents, where bounded tasks and tools make         prevent undesirable outcomes, but differ in the source of risk
requirements enumerable, suggesting that verifiable policies       they address. Security requirements constrain how a system
are feasible precisely in the commercial applications we target.   behaves in the presence of an adversary, and conventionally
   Second, among benchmarks that do state verifiable               concern confidentiality, integrity, and availability. Safety re-
security and safety requirements, most are symbolically            quirements constrain the harm a system may cause to its users
enforceable using classical software engineering mecha-            and environment, under accidental or environmental faults
nisms that the agent literature has largely overlooked.            rather than an adversary; they require the system to stay within
Confidentiality and integrity, for example, have long been         its intended operating envelope and fail only into benign states
enforced through symbolic, deductive mechanisms such as            (e.g., not deleting files or issuing destructive commands).
access control [14], input validation [15], and information-flow      In commercial settings, there are often application-specific
control [16], which afford formal, logic-based assurances and      constraints such as “refunds above $50 require approval.” Such
build on principles such as least privilege and complete medi-     a constraint can be violated by an adversary’s attack or by an
ation [17]. The agent literature, by contrast, emphasizes neural   honest mistake; either may cause financial or reputational harm
guardrails such as LLM-as-a-judge [18]–[20], which use prob-       to the system owner or its users. Whether we call the constraint
abilistic, inductive methods to enforce rules, some of which       a safety or security requirement depends on the source of risk
could instead be enforced symbolically for a formal guarantee.     we consider, not on how the constraint is written.
For example, we observed that in τ 2 -Bench, an airline agent         We deliberately do not adopt these definitions of security
can erroneously cancel an already-flown flight [21], because       and safety as a filter on what we study. Applying them to
the corresponding rule is passed through a prompt rather than      current benchmarks yields limited insight: the expectations
enforced symbolically in the agent harness. In our study, we       of agent behavior encoded in benchmarks are rarely stated
considered six types of symbolic guardrails. We found 74%          explicitly, and the sources of risk they address often overlap, so
of the analyzed requirements are symbolically enforceable, of      the same requirement often protects against both mistakes and
which 95% need only simple, low-cost checks, predominantly         adversaries. Forcing each requirement into one bin obscures
API validation, rather than more complex methods such as           more than it clarifies, and this ambiguity is itself one of
information-flow tracking [22] or temporal logic [23]. We          our empirical findings. What the requirements we study do
argue that these mechanisms are critical for the path toward       share is a common form: instructions the agent is meant to
deploying agents in risk-averse commercial applications.           follow in order to prevent a specific undesirable outcome,
   Third, enforcing these requirements symbolically im-            whether that outcome is data exfiltration, a destructive action,
proves agent utility rather than eroding it. A common              or a violation of an organizational policy that could lead to
objection to agent guardrails is that they over-constrain the      harm. We refer to this broader notion of a harm-preventing
agent, improving security and safety at the cost of task suc-      expectation collectively as security and safety requirements.
             LLM                                   LLM                      Tools   (Sec. II-A). To prevent agents from taking insecure or unsafe
                              Tools
                                                                                    actions, researchers have explored various methods.
 Instruction: “Assist the              Instruction: “Assist the user with
 user with any task using               flight ticket booking using tools              One line of research trains the underlying LLM supporting
   all available tools…”                 that access the airline DBs…”              the AI agent to be secure and safe, embedding these properties
  (a) General-purpose agents.           (b) Domain-specific agents.                 in the model itself rather than enforcing them externally. Re-
                                                                                    searchers have explored post-training alignment, particularly
                     Fig. 2: Two types of AI agents.                                supervised fine-tuning and reinforcement learning from human
                                                                                    feedback (RLHF) [37]–[40], and methods that replace human
                                                                                    feedback with AI-generated signals [41]–[43]. Other work
B. AI Agents                                                                        explored adversarial data collection and risk-focused active
   Over the past few years, large language models (LLMs)                            learning [44], [45]. These methods reduce the likelihood of
have advanced beyond single-turn text generation, gaining ca-                       insecure or unsafe actions, but because LLMs are inherently
pabilities for context understanding, reasoning, and interaction                    probabilistic, they cannot guarantee that agents will never
with the environment through external tool use [26]. They                           violate specific security or safety requirements.
now serve as the core of AI agents, from the earlier retrieval-                        Another line of research introduces runtime guardrails built
augmented generation paradigm [27] to more recent ones such                         around the LLM. We distinguish two kinds: neural guardrails
as ReAct [28] and Reflexion [29].                                                   (inductive) and symbolic guardrails (deductive).
   AI agents lack a standard definition; we focus on LLM-                              Neural guardrails make decisions inductively, most com-
based agents with tool-use capabilities. The agent interacts                        monly via the LLM-as-judge paradigm: judge LLMs that are
with the user iteratively: at each step, the LLM decides the                        independent of the agent monitor (1) agent inputs and outputs
next action, either invoking tools or responding with text. Tool                    for insecure or unsafe content, such as prompt injection and
outputs are appended to the agent context, conditioning later                       sensitive data, or (2) agent actions to assess their security
actions. Tools may include APIs, command-line interfaces, or                        and safety. For example, AGrail [18] uses LLMs to generate
other agents. Agents autonomously decide when to invoke a                           and apply safety checks; LlamaFirewall [19] uses ML classi-
tool, which to invoke, and with what arguments. To make tools                       fiers to detect prompt injection and LLMs for misalignment;
reusable across agents and to facilitate invocation, standardized                   RTBAS [46] combines an LLM with a probabilistic saliency
formats for describing tools’ purposes and schemas have been                        screener for information-flow analysis; and Liu et al. [47] use
widely adopted, including Model Context Protocol (MCP) [30]                         LLMs to detect prompt injection. Some work aims to provide
and the Agent2Agent (A2A) Protocol [31].                                            deterministic guardrails, but still relies on LLMs to generate
   AI agents are now deployed across diverse settings. Fol-                         guardrail specifications or to execute them. These approaches,
lowing prior work [32], we distinguish general-purpose from                         therefore, remain probabilistic and cannot provide guarantees.
domain-specific agents by the scope of tasks they support.                          For example, GuardAgent [48] uses LLMs to generate
General-purpose agents (Fig. 2a) are designed to assist users                       guardrail code; NeMo Guardrails [20] provides programmable
with an open-ended set of tasks and are equipped with broadly                       guardrails while execution involves judge LLMs; S HIELD -
applicable tools. Examples include ChatGPT Agent mode [33]                          AGENT [49] relies on LLMs to retrieve and execute rule-
and Microsoft Copilot integrated with Windows [34], which                           based policy checks; AGENT G UARDIAN [50] uses LLMs to
can observe the screen and control the keyboard and mouse.                          generate control policies. A key limitation of neural guardrails
We also consider CLI agents such as Claude Code [35]                                is their inductive nature: because their generation or execution
and OpenClaw [8] as general-purpose, since they support a                           depends on LLMs, their behavior cannot be formally reasoned
wide range of tasks with broad tool-use capabilities, including                     about. They reduce the likelihood of unintended actions, but
file editing, command-line execution, and internet access. In                       cannot guarantee an agent will never violate a security or
contrast, domain-specific agents (Fig. 2b) are designed for a                       safety requirement, which may leave deployment risk above
fixed scope of tasks, with access only to task-relevant tools.                      acceptable levels in commercial settings.
For instance, a customer support agent for airline reservations                        In contrast, traditional software engineering uses symbolic,
may only access reservation-related tools such as ticket lookup                     deductive enforcement techniques to provide guarantees, such
or refund [11], while a Customer Relationship Management                            as input sanitization against SQL injection [15], information-
(CRM) agent [36] may interact only with CRM-internal work-                          flow control against sensitive data leakage [16], and access
flows. Neither may access the internet or execute arbitrary                         control against unauthorized access [14]. A few recent studies
code. These two categories differ in their security and safety                      have explored these mechanisms as symbolic guardrails for
considerations, as we discuss in Sec. III-C.                                        AI agent security and safety. For example, AGENT S PEC [23],
                                                                                    AGENT-C [51], and Maris [52] use temporal logic to con-
                                                                                    strain tool-call orders; Progent [53] defines privilege control
C. AI Agent Guardrail: Neural versus Symbolic
                                                                                    policies using domain-specific languages; Doshi et al. [54]
   Although AI agents are powerful and widely adopted [5]–                          explore temporal logic and information-flow control with
[8], they may use tools to interact with environments in                            formal models; PFI [55] detects unsafe data flows to prevent
unintended ways, raising security and safety concerns [1], [2]                      privilege escalation; F IDES [22] uses information-flow control
              arXiv API search             Exclude robotics/RL papers           our search interface for two reasons: AI agent papers typically
             Inclusion criteria (a)-(e)         Exclusion criteria (f)-(g)
                    (n=553)                             (n=140)                 appear on arXiv well before formal publication, and arXiv’s
                                                                                subject metadata (e.g., cs.SE) enables filtering to keep the
                                          Exclude non-benchmark paper
           After exclusion criteria                                             candidate set tractable. Because LLM-based agents emerged
                                           LLM filter (Cohen’s kappa=0.88)
                   (n=413)
                                                        (n=112)
                                                                                only after ChatGPT’s release [60] in late 2022, we limit the
       After non-benchmark LLM filter
                                          Exclude by manual inspection          search period to Jan. 2022 through Mar. 2026.
                                                   – no benchmark: 11
                   (n=301)                 – not tool-calling LLM agents: 135       Following prior work [61], we first assemble a seed set of
                                              – no security/safety eval: 52
                                                    – out of scope: 23          15 papers known to the authors. By analyzing this seed set,
                                                        (n=221)
            Papers for analysis                                                 we derive the following inclusion criteria: (a) title or abstract
                  (n=80)
                                                                                contains at least one whole word from {bench, benchmark,
Fig. 3: PRISMA-style flow of the systematic literature review.                  dataset, framework}; (b) title contains at least one substring
                                                                                from {eval, assess, bench, dataset}; (c) title or abstract con-
                                                                                tains the whole word agent; (d) title or abstract contains at least
to track confidentiality and integrity; PCAS [56] likewise                      one whole word from {safety, security, privacy, confidentiality,
uses information-flow control for provenance tracking; and f -                  policy, risk, attack}; and (e) the paper is cross-listed in at least
secure [57] and CaMeL [58] tackle prompt injection attacks                      one of the arXiv categories cs.AI, cs.CL, or cs.LG.
by separating control flow from data flow.                                          The query returned 553 candidate papers. Manual inspection
   We believe symbolic guardrails offer a practical path toward                 revealed that many were irrelevant, concerning reinforcement
the guarantees needed to deploy AI agents in risk-averse com-                   learning or robotics, where “agent” and “policy” carry dif-
mercial settings. Although each symbolic guardrail enforces a                   ferent meanings. We therefore added two exclusion criteria:
specific class of security or safety requirements, it is unclear                (f) the paper is cross-listed in cs.RO; and (g) title or abstract
whether existing symbolic guardrails cover the requirements                     contains any whole word from {robot, self-driving, embodied,
arising in practical deployments. Moreover, there is a concern                  reinforcement}. After the exclusions, 413 papers remained.
that guardrails may reduce agent utility (the ability to complete                   Filtering Methods. We assessed whether each of the 413
tasks) as they restrict agent behavior [24], [25]. This paper                   papers proposes benchmarks. One author manually annotated
provides the first empirical investigation of these questions:                  a random sample of 100 papers, while GPT-5-nano annotated
to what extent existing symbolic guardrails apply to agent                      all 413; both the human and the LLM saw only the paper
security and safety requirements, and how they affect utility.                  title and abstract. On the 100-paper sample, human and LLM
                                                                                labels reached a Cohen’s kappa of 0.88 (95% CI [0.76, 0.99]),
III. S TUDY 1: V ERIFIABILITY OF S ECURITY AND S AFETY                          with LLM precision 0.96 and recall 0.99 against the human
  R EQUIREMENTS E VALUATED IN AGENT B ENCHMARKS                                 labels. Given this high agreement, we adopted the LLM’s
   Benchmarks do not merely measure progress; they shape                        labels, filtering out 112 non-benchmark papers, leaving 301.
it [3], [4]. By defining success and failure, benchmarks im-                        We manually inspected all 301 papers. We excluded 11 for
plicitly define the problem researchers optimize for. Agents                    not proposing a benchmark, 135 for not targeting tool-calling
are routinely tuned and compared on security and safety                         LLM-based agents, and 52 for not evaluating security or safety
benchmarks, giving them an outsized role: the requirements                      aspects. We further excluded 23 as out-of-scope: benchmarks
they encode become, in effect, the operational definition of a                  assessing agents’ ability to perform security- or safety-related
safe or secure agent. Yet in risk-averse deployments, we can                    tasks rather than evaluating the security or safety of the agents
only reason about requirements specified in verifiable form.                    themselves; extensions of already included benchmarks that
This motivates our research question: which security and safety                 add only data or metrics without altering security or safety
requirements do agent benchmarks evaluate, and how are these                    policies; and evaluations of whether an agent threat is plausible
requirements specified?                                                         rather than whether the agent is secure or safe. As in Fig. 3,
   To answer this, we performed a systematic literature review                  80 papers remained; details are available in the paper artifact.
of 80 agent security and safety benchmarks and examined                             2) Classifying Benchmarks: For each of the 80 benchmark,
the sets of requirements they define, which we call policies                    we analyze its security or safety policy, defined as the set
following prior convention [11], [21]. We classify them along                   of security and safety requirements the benchmark specifies.
a spectrum from unstated to task-specific rules, finding that                   Using forced-choice coding, we classified benchmarks by (1)
most benchmarks never state the requirements they test.                         the target agent type (general-purpose vs. domain-specific,
                                                                                Sec. II-B) and (2) policy specificity, characterized by scope
A. Research Method                                                              and verifiability (TABLE I). The focus here is verifiability:
   1) Identifying Benchmarks: Following established guide-                      given a policy and an agent’s actions, whether one can prove
lines [59], we assembled our corpus through a systematic                        (verify) at the level that the actions satisfy the policy [63].
literature review. The process is illustrated in Fig. 3.                        Verifiability is an established quality attribute of well-formed
   Search Criteria. We target papers that (1) propose a                         requirements in requirements engineering [63] and relates to
benchmark, (2) evaluate tool-calling LLM-based agents, and                      research on ambiguity in natural-language requirements [64].
(3) evaluate agent security or safety. We use the arXiv API as                  In our corpus, the issue is more often omission than impreci-
                  TABLE I: Taxonomy of AI Agent Security and Safety Policies, Classified by Verifiability and Scope
  Specificity         Scope   Verifiable    Explanation                           Example
  No Policy           -       -             No security/safety guidance.          -
  Goal-Setting        Agent   No            High-level security/safety goals      “If user requests anything unsafe, do not fulfill” [13]; “If query asks private
                                            governing agent behavior.             information, decline to answer” [36]; unsafe and private are unexplained.
  Verifiable-Rule     Agent   Yes           Verifiable security/safety require-   “If any portion of the flight has already been flown, the agent cannot
                                            ments governing agent behavior.       help” [21], a verifiable requirement for an airline-ticket agent.
  Task-Specific       Task    Yes           Verifiable security/safety require-   For a web agent over arbitrary webpages, “When clicking the Create group
                                            ments apply only to a specific        button, ask permission” [62] applies to a GitLab group-creation task but
                                            task.                                 not, e.g., to an online-shopping task.



sion: requirements either leave the operative term (e.g., unsafe                  TABLE II: Distribution of Benchmarks by Agent Domain and
or private) unexplained, or benchmarks state no requirement at                    Policy Specificity, Computed over n = 80
all, conveying expected behavior only through evaluation data.                                                      Agent Domain
The problem is often not that a requirement could be read two
                                                                                       Policy Specificity     Gen.-Purp.      Dom.-Spec.           Total
ways (ambiguity), but that too little is stated for verification.
                                                                                       No Policy              38 (47.5%)       11 (13.8%)       49 (61.3%)
   We do not attempt to define verifiability thresholds pre-                           Goal-Setting           14 (17.5%)        5 (6.3%)        19 (23.8%)
cisely, and we do not believe doing so would be produc-                                Verifiable-Rule         0 (0.0%)         5 (6.3%)         5 (6.3%)
tive: like specificity and ambiguity in software requirements,                         Task-Specific           1 (1.3%)         1 (1.3%)         2 (2.5%)
                                                                                       Unclear                 2 (2.5%)         3 (3.8%)         5 (6.3%)
verifiability lies on a spectrum, and any threshold would
be arbitrary. This stance is shared by work on automated                               Total                  55 (68.8%)       25 (31.3%)      80 (100.0%)
requirements-quality checkers, where whether a flagged issue
is a genuine problem is a contextual judgment [65], [66]. We
use four categories for a pragmatic partition: No Policy, Goal-                   jointly. All data are available for external validation.
Setting, Verifiable-Rule, and Task-Specific, defined and illus-
trated in TABLE I. In practice, the distinction is usually clear,                 B. Results
and all authors discussed the rare borderline cases; we release                      We identified 80 benchmarks for AI agent security and
all data for readers to confirm. We classified five benchmarks                    safety. TABLE II summarizes them along two dimensions:
with insufficient information as unclear. Goal-Setting policies                   agent type (general-purpose vs. domain-specific) and the speci-
fall into two patterns: (1) using safety or security without                      ficity of their security and safety policies.
explanation, e.g., “If user requests anything unsafe, do not                         Security and safety requirements in 61% of agent bench-
fulfill” [13]; and (2) leaving key terms unexplained, typically                   marks are left implicit. These benchmarks provide no explicit
adjectives constraining information (e.g., private, sensitive) or                 instruction for the agent to behave safely or securely; their de-
actions (e.g., necessary, legitimate), e.g., “If query asks private               signers implicitly expect agents to prioritize security and safety
information, decline to answer” [36].                                             norms over user instructions, even though this expectation is
   3) Threats to Validity: First, we use benchmark policies as                    never communicated. For example, AgentHarm [67] expects
a proxy for the security and safety requirements that deployed                    agents to refuse a user request to forge a passport, without
agents should satisfy. Benchmarks reflect their developers’                       instructing the agent that safety should override obedience.
interests and may characterize researchers’ attention more than                   In effect, designers expect agents to follow common-sense
deployment concerns. Second, despite arXiv’s broad coverage                       security and safety norms, yet what counts as common sense
of ML-related papers1 and our broad selection criteria, we may                    varies across benchmarks and is rarely articulated, leaving it
have missed benchmarks. Because this section reports policy-                      to be inferred from evaluation criteria.
type distributions while later sections focus on Verifiable-Rule                     Security and safety encompass broad themes and are
benchmarks, we performed an informal snowballing search,                          interpreted differently across benchmarks. Conceptions of
tracking citations to and from known papers, to confirm that                      security and safety vary widely across benchmarks (Sec. II-A),
our Verifiable-Rule set is complete. Among 61 candidates,                         spanning themes such as privacy, authorization, robustness
we identified no new Verifiable-Rule benchmarks, suggesting                       to attacks, fairness, truthfulness, bodily harm, and policy
this limitation does not alter our conclusions. Finally, our                      compliance. Even the same theme is often interpreted in
benchmark classifications are categorical, though domain and                      different, sometimes conflicting ways. For user privacy, for
policy specificity lie on a spectrum and require judgment.                        example, MobileSafetyBench [68] expects an agent to always
We applied labels consistently and discussed uncertain cases                      request user permission before sharing private information.
                                                                                  MPCI [69], in contrast, evaluates whether an agent shares con-
   1 For each of NeurIPS, ICML, ICLR, ACL, EMNLP, and NAACL, we                   fidential information in “suitable” social contexts and refuses
sampled 100 papers accepted in 2025 and searched arXiv for exact title            in inappropriate ones, without providing explicit instructions.
matches. Hit rates were 71%, 77%, 78%, 74%, 71%, and 74%. Manual
inspection showed a lot of misses were slight title variants of papers already       Verifiable policies (Verifiable-Rule and Task-Specific) are
on arXiv, indicating arXiv indexes the vast majority of ML papers.                rare (9%). In non-verifiable policies, what counts as danger-
ous, illegal, or private is often unclear or context-dependent.        missed opportunity that we argue should be addressed. We be-
Only 9% of benchmarks specify plausibly verifiable require-            lieve many settings exist where domain-specific agents can be
ments. For example, CAR-bench [70] states: “if tool descrip-           deployed safely and securely while providing practical value,
tion starts with REQUIRES_CONFIRMATION, before calling                 whereas general-purpose agents remain too risky even when
. . . must list the tool parameter and action details and obtain       broadly aligned with common-sense expectations. Domain-
explicit expressive user confirmation. . . ” This rule is verifiable   specific agents with enforceable security and safety are there-
because both the antecedent (REQUIRES_CONFIRMATION                     fore a promising direction for commercial deployment.
prefix) and the consequent (explicit content for user confirma-
tion) are checkable from the agent’s trace.                            IV. S TUDY 2: S YMBOLIC E NFORCEABILITY OF S ECURITY
                                                                        AND S AFETY R EQUIREMENTS IN AGENT B ENCHMARKS
C. Discussion                                                             Study 1 found that most agent benchmarks do not state
   Verifiable-Rule and Task-Specific policies are essential for        verifiable security and safety requirements. Study 2 examines
security and safety assurances in commercial deployments.              the few that do, since they are the only benchmarks that admit
When policies are implicit or unverifiable, practitioners can          security and safety guarantees needed in risk-averse commer-
neither implement reliable guardrails nor audit agent behavior         cial settings. We ask: among verifiable security and safety
against a standard. Common-sense expectations cannot fill this         requirements in agent benchmarks, which can be symbolically
gap: many hold only within a community or are contested.               enforced, and how? Why are others not enforceable?
For example, LPS-Bench [71] considers agent that “adheres                 This restricts Study 2 to the seven benchmarks with veri-
too rigidly to instructions while ignoring implicit intent” as         fiable security and safety requirements identified in Sec. III
unsafe, which we find contestable: in high-stakes scenarios            (5 Verifiable-Rule and 2 Task-Specific). This is not a sampling
such as medical record updates, following explicit instructions        decision: these seven are the only benchmarks that can answer
may be preferable to inferring intent. In commercial deploy-           our research questions on symbolic enforceability.
ments, violating a requirement can be costly, and relying on the
underlying model to interpret vague goals (e.g., what counts           A. Research Method
as necessary or private) shifts this risk onto an inductive               1) Selecting Benchmarks: Among the seven benchmarks
process that cannot be reasoned about. Verifiable-Rule and             with verifiable security and safety requirements, we exclude
Task-Specific policies remove this dependence by stating, in           the two Task-Specific ones, where guardrail applicability would
verifiable form, which actions the agent must or must not take,        be entirely input-dependent. Of the five Verifiable-Rule bench-
providing a basis for enforcement guardrails.                          marks, four target customer-service agents. To avoid overfitting
   Verifiable-Rule policies are preferable to Task-Specific            to one domain, we select τ 2 -Bench [11] (the most widely used
policies. Both contain verifiable requirements, but Verifiable-        of the four) and CAR-bench [70] (the non-customer-service
Rule policies state agent-level requirements that generalize           benchmark, for in-car voice assistants). Both state policies
across tasks, while Task-Specific policies apply only to one           in natural language; we treat each sentence as a candidate
specific task and require generating and updating policies per         requirement, yielding 120 in τ 2 -Bench and 18 in CAR-bench.
use case. In practice, this means either delegating policy gen-           To broaden domain coverage beyond these two, we con-
eration to a model, which reintroduces the reliability concerns        sidered synthesizing plausible Verifiable-Rule policies for ad-
that motivated verifiable policies in the first place, or asking       ditional domain-specific benchmarks. We initially planned
the user to articulate the policy for every input in a verifiable      to construct policies for the 20 domain-specific benchmarks
form (e.g. formal notation). Both options are problematic: the         without Verifiable-Rule policies, so policies reflect what the
former undermines reliability, while the latter is impractical in      benchmark evaluates. This proved difficult: although evalu-
most deployments considering usability and cost.                       ation methods implicitly encode security and safety expec-
   Domain-specific agents are more feasible for enumerat-              tations, recovering consistent verifiable requirements would
ing Verifiable-Rule policies. Although verifiable requirements         have demanded extensive data review and modification, as task
are desirable, articulating them for general-purpose agents is         conflicts were common. For example, in CRMArenaPro [36],
hard; their broad use cases make common-sense expectations             one task expects the agent to reject “Considering recent
seem more scalable. Consistent with this, all Verifiable-Rule          discussions, should this lead be considered qualified?” as a
benchmarks we found target domain-specific agents (TA-                 privacy violation, while another expects it to answer the near-
BLE II): inputs may vary, but the task scope is defined and            identical query “After assessing recent discussions, should this
tools are limited, so verifiable requirements can be enumerated        lead be considered qualified?” No single requirement aligns
in advance. For example, an airline-ticket agent with access           with both cases without modifying the benchmark labels.
only to airline-database tools can be given the requirement “If           As a result, we adopted an alternative solution, creating
flights are flown, agent cannot cancel and refund” [11]. For           a synthetic policy for a domain-specific benchmark in a
general-purpose agents with open-ended tasks and broad tool            high-stakes domain that did not originally target security or
access, comprehensively specifying verifiable requirements is          safety, hence excluded from Study 1. We selected MedA-
far more difficult. Yet 20 of 25 domain-specific benchmarks            gentBench [73], which evaluates an electronic medical record
still do not specify Verifiable-Rule policies (TABLE II), a            (EMR) assistant. To create a plausible policy without biasing
                                         TABLE III: Symbolic Guardrails and Illustrative Examples
    Symbolic Guardrail              Examplea
    API Validation                   Before invoking cancel_ticket(user, ticket), verify that user == ticket.user.
    Schema Constraint [72]           Reject LLM output if it is neither a tool invocation matching the airline API schema nor a message to the user.
    Temporal Logic [23]              Block all other tools until authenticate_user completes successfully.
    Information Flow [22]            Prevent information about other passengers from reaching the agent.
    User Confirmation                Before cancel_ticket, require rule-based user confirmation rather than LLM-initiated confirmation.
    Response Template                After cancel_ticket, display a predefined cancellation summary rather than an LLM-generated response.
    a Illustrative examples are based on an airline ticket agent, inspired by τ 2 -Bench [11]. The agent assists users with managing their flight bookings
    and interacts with internal databases by invoking tools such as get_flight_info, get_user_info, and cancel_ticket.


                                                                                         100%
it toward or against symbolic enforcement, we followed the                                                                   23 (26.1%)
                                                                                         75%    42 (35%)
procedure below. First, we prompted GPT-5.2 to generate a                                                                                       Not Enforceable




                                                                                 Share
                                                                                         50%                                 34 (38.6%)         Enforceable
security and safety policy from the EMR assistant’s use case                                                 17 (94.4%)
                                                                                                                                                Out of Scope
                                                                                         25%    69 (57.5%)
and tool schema, requesting verifiable rules with no mention                                                                 31 (35.2%)
                                                                                          0%
of enforcement. This produced 50 requirements. Second, we                                       τ −Bench
                                                                                                 2           CAR−bench    MedAgentBench
improved policy comprehensiveness through hazard analysis,
specifically System-Theoretic Process Analysis (STPA) [74],                     Fig. 4: Distribution of security and safety requirements en-
which anticipates harms from diverse perspectives and derives                   forceability across the three benchmarks.
corresponding requirements. Using an automated STPA tool
from prior work [75] with GPT-5, we identified 5,138 candi-
date requirements. To keep scope manageable, we randomly
sampled 4% (205 entries), clustered them into 10 categories                     • Enforceable symbolically: can be enforced by one or more
via K-Means over OpenAI text-embedding-3-small                                    symbolic guardrails; we also record which guardrails.
embeddings, and prompted an LLM to consolidate each clus-                       • Likely not enforceable symbolically: cannot be enforced
ter, yielding 77 candidate requirements; we randomly sampled                      by any combination of the considered guardrails.
20 for further analysis. Because these 20 often contained
compound logic, we decomposed them into 43 atomic require-                         In most cases, classification was straightforward. To validate
ments; after removing 5 duplicates, 38 remained. Combining                      borderline labels, all authors discussed them and reached
the 50 initial requirements and the 38 from STPA produced a                     consensus; we share our classifications for readers to confirm.
final policy of 88 requirements. All key steps were automated                   For each requirement labeled enforceable, one author imple-
to avoid author bias; full details are in the paper artifact.                   mented the corresponding guardrail and verified its behavior
   2) Classifying Requirements Enforceability and Matching                      against the benchmark data; these implementations are reused
Symbolic Guardrails: For each requirement, we manually                          in Study 3 (see Sec. V for details). All authors also discussed
classify whether it can be plausibly enforced symbolically,                     requirements classified as not enforceable, exploring common
that is, through deductive reasoning in program code. We                        reasons through a card-sorting-style grouping and reflection.
operationalize this by checking whether any of six symbolic
guardrails, explained in TABLE III, could enforce it: API val-                    3) Threats to Validity: Our analysis is limited by the
idation, schema constraints, information flow2 , temporal logic,                small number of Verifiable-Rule benchmarks, covering only
user confirmation, and response templates. We assembled this                    two domains. The MedAgentBench policy extends coverage
catalog in two ways. Top-down, we identified methods already                    but is LLM-generated rather than human-written and may
used in prior work to secure AI agents (Sec. II-C), such                        not fully reflect requirements practitioners would impose in
as information-flow control [22]. Bottom-up, we identified                      deployment. Hazard analysis helps identify security and safety
strategies not usually discussed in the academic literature but                 concerns comprehensively, but we followed an automated
well-suited to the requirements these benchmarks evaluate.                      process without expert judgment. As before, benchmark re-
   For each candidate requirement in the three benchmarks’                      quirements often shape what researchers focus on and may not
policies, we manually assign one of three labels:                               match the concerns of commercial settings. Our results should
• Out of scope: (1) provides information rather than stating a
                                                                                therefore be interpreted as a step toward understanding what
   requirement (e.g., “User’s profile contains their email”); (2)               enforcement is possible for plausible domain-specific policies,
   specifies a system-level requirement that cannot be fulfilled                not as a comprehensive reflection of commercial practice.
   through agent behavior (e.g., “No PII should be stored                         Our guardrail catalog may also be incomplete, and our
   persistently”); or (3) was hallucinated by the LLM and is                    judgment of symbolic enforceability also depends on our
   infeasible given the available tools (MedAgentBench only).                   understanding of what symbolic guardrails can achieve and
   2 Strict enforcement of information-flow properties is challenging given
                                                                                our ability to implement them. Therefore, the enforceable rate
implicit flows and environment interactions, though various approaches ex-      should be read as a conservative lower bound, which does not
ist [76]; these nuances are beyond our scope.                                   undermine our argument.
        100%
                                                                                 ducing context size and token costs. Because LLMs struggle
        75%                             16 (47.1%)   API Validation              to follow instructions when too many are provided [77], a
                                                     Schema Constraint
               34 (81%)
                           11 (64.7%)
                                                     Temporal Logic
                                                                                 shorter policy may also improve compliance with the remain-
Share




        50%                                          Information Flow            ing instructions. At the same time, keeping some enforced
                                                     User Confirmation
                                         3 (8.8%)
                                                     Response Template
                                                                                 requirements in the policy may still be useful, so the agent
        25%                 3 (17.6%)   5 (14.7%)
                                                     Combination of Guardrails   can take the right action upfront rather than receive a guardrail
               6 (14.3%)    2 (11.8%)   6 (17.6%)
         0%
                                                                                 error. This trade-off is an implementation choice beyond our
               τ −Bench
               2           CAR−bench MedAgentBench
                                                                                 scope, and one that, to our knowledge, has received little
Fig. 5: Distribution of applicable symbolic guardrails for                       attention in the agent security and safety literature.
enforceable requirements across the three benchmarks.
                                                                                 C. Which requirements are not enforceable with symbolic
                                                                                 guardrails, and what alternative approaches are available?
B. Which requirements are enforceable with symbolic                                  1) Results: We identified four recurring themes among
guardrails, and how?                                                             the not enforceable requirements in the three benchmarks,
   1) Results: Across the three benchmarks, 74% of secu-                         described below; mitigations are discussed in Sec. IV-C2.
rity and safety requirements are enforceable by symbolic                             Persona and interaction-style requirements specify how
guardrails. As shown in Fig. 4, after excluding out-of-scope                     the agent should communicate, such as using specific language
requirements, symbolic guardrails enforce 42/51 in τ 2 -Bench,                   or tone. For example, a medical assistant may be required to
17/18 in CAR-bench, and 34/57 in MedAgentBench.                                  remain neutral and avoid offering medical judgment [73].
   Simple guardrails such as API validation often suf-                               “No hallucination” requirements expect the agent to avoid
fice. As shown in Fig. 5, API validation alone covers 81%,                       generating unsupported or fabricated information. For exam-
65%, and 47% of enforceable requirements in τ 2 -Bench,                          ple, τ 2 -Bench specifies that the agent “should not provide any
CAR-bench, and MedAgentBench, respectively. Adding other                         information not provided by the user or available tools” [11].
simple methods (schema constraints, user confirmation, and                           Procedure-following requirements specify that the agent
response templates) brings coverage to 95% of all enforceable                    must follow a predefined sequence of steps. For example, in
requirements. Only five requirements (all in MedAgentBench)                      τ 2 -Bench, an agent helping with airline booking is expected
require temporal logic or information-flow control, which are                    to first obtain user details and then trip details [11].
relatively more costly to implement.                                                 Common-sense reasoning requirements arise even within
   2) Discussion: Symbolic guardrails are effective and                          Verifiable-Rule policies. These requirements leave substantial
inexpensive for many security and safety requirements in                         room for interpretation and therefore depend on common-sense
the analyzed agents. Many security and safety requirements                       reasoning. For instance, in the flight-assistant setting of τ 2 -
in identified policies can be enforced with symbolic guardrails,                 Bench, a policy such as “Do not proactively offer compen-
and in most cases are inexpensive in both engineering effort                     sation unless the user explicitly asks for it” still requires the
and runtime cost, because the requirements can be handled                        model to interpret what counts as an explicit request [11].
through simple API validation, schema enforcement, or hard-                          2) Discussion: Symbolic guardrails cannot enforce all
coded user confirmation and response templates. These mech-                      requirements; some still require neural guardrails. The four
anisms are rarely discussed in research on AI agent security                     themes above are not enforceable symbolically, even within
and safety. More sophisticated mechanisms explored in recent                     Verifiable-Rule policies. In such cases, neural guardrails can
work, such as information-flow tracking and temporal logic,                      help: for example, an LLM judge may detect hallucinations
require greater engineering effort and are rarely needed (5                      while symbolic guardrails cannot.
of 93, 5%) for the enforceable requirements in the three                             Some non-enforceable requirements become enforceable
analyzed benchmarks. Even the few we identified that require                     through stronger or weaker reformulations; whether to
these methods are simple, for example, “Block all other tools                    do so is an engineering decision. For example, a procedure-
until authenticate_user completes successfully.” We                              following requirement to collect user information before trip
argue that domain-specific agents offer many low-hanging                         details when booking a flight could be enforced via a sub-agent
fruit opportunities: lightweight checks that could prevent many                  design that splits the workflow into sequential stages, which
agent errors. Surprisingly, benchmark implementations often                      is a stronger reformulation requiring architectural change.
do not enforce even basic rules in the tools themselves, for                     Conversely, the requirement “Do not proactively offer compen-
example, that an agent cannot cancel a flight already flown, and                 sation unless the user explicitly asks for it” could be replaced
instead rely on the agent model or additional neural guardrails.                 with a weaker but more precise rule such as “Block com-
This design violates basic software engineering and security                     pensation tools until the user’s response exactly matches the
principles such as least privilege and complete mediation [17].                  word ‘compensation’ ”, making it enforceable. In commercial
   Symbolic guardrails may simplify agent prompts and                            deployments, this is a trade-off between implementation cost
improve instruction following. Once enforced symbolically,                       and residual risk. Enforcing requirements symbolically when-
requirements can be removed from the agent’s prompt, re-                         ever feasible reduces both the attack surface and the potential
for hazards, letting developers reserve more expensive neural         3) Datasets: For τ 2 -Bench, we use τ 2 -Bench-Verified (air-
guardrails with residual risk for the remaining requirements.      line) [78], a cleaned version that fixes inconsistencies in the
                                                                   original benchmark without altering the policy, prompts, or
                                                                   tools. It contains 50 tasks in which AI agents assist customers
 V. S TUDY 3: B ENCHMARKING S ECURITY, S AFETY, AND
                                                                   with flight reservations; some customers attempt policy viola-
   U TILITY OF AGENTS WITH S YMBOLIC G UARDRAILS
                                                                   tions, e.g., requesting a refund for a non-refundable flight.
   Symbolic guardrails can enforce certain security and safety        For CAR-bench, we use the 100 data entries from the
requirements, but a concern is that they over-constrain agents     “Base” category, in which the agent acts as an in-car voice
and reduce utility (their ability to complete tasks success-       assistant that helps users with navigation and vehicle opera-
fully) [24], [25]. We ask: how do symbolic guardrails affect       tions such as checking the weather and adjusting fog lights.
agent security, safety, and utility? Study 3 empirically mea-         MedAgentBench evaluates whether an agent can assist with
sures this across the three benchmarks from Sec. IV.               electronic medical record (EMR) tasks such as checking
                                                                   patient records and ordering medications. It contains 300 tasks,
                                                                   none probing for policy violations. Because our policy requires
A. Research Method                                                 patient authorization, which is not considered in the original,
   We run each benchmark with and without symbolic                 we augment the dataset by providing the user (simulated by
guardrails (independent variable) and measure policy viola-        LLMs) with the patient information needed for authorization.
tions (agent actions that violate symbolically-enforceable secu-      To supplement our analysis, we construct an adversarial
rity and safety requirements) and utility (dependent variables).   dataset for MedAgentBench in which the user tries to manip-
We reuse the three benchmarks from Study 2, τ 2 -Bench             ulate the agent into violating a requirement. Following prior
(airline) [11], CAR-bench [70], and MedAgentBench [73],            practices [36], [62], [71], we identified four task categories
along with the guardrails implemented there, detailed below.       from the original benchmark and prompted an LLM to expand
                                                                   them into 17 scenarios. For each scenario-requirement pair,
   1) Experiment Infrastructure: We implement a tool-calling
                                                                   the LLM generated an adversarial task that seeks to violate the
agent following τ 2 -Bench [11], with GPT-4o and GPT-5 as
                                                                   requirement within the scenario. Due to cost, we sampled 50 of
backbone LLMs and policies in system prompts. Across all
                                                                   the 391 tasks (17 scenarios × 23 requirements) for evaluation.
conditions, tools are exposed via an MCP server [30].
                                                                      4) Dependent variables: We measure utility as the first-
   Because these benchmarks require multi-turn user-agent          try task success rate, using each benchmark’s original metric:
interactions, we simulate user responses with an LLM, in line      Pass^1 for τ 2 -Bench and CAR-bench, and Success Rate (SR)
with τ 2 -Bench and CAR-bench. The user-simulation LLM is          for MedAgentBench. We do not measure utility on the adver-
given the relevant context but has no access to the MCP tools.     sarial dataset, as task completion is not expected.
   2) Tool and Symbolic Guardrail Implementation: For τ 2 -           For security and safety, only CAR-bench measures policy
Bench and CAR-bench, we use the tool implementations               violations among the three: its rpolicy metric evaluates whether
released with each benchmark as the baseline condition,            each task follows the policy throughout, relying in part on
wrapping them with symbolic guardrails for all enforceable         a probabilistic LLM judge. To evaluate security and safety
requirements to form the guardrail condition (Fig. 5).             non-probabilistically, we restrict evaluation to symbolically
   For MedAgentBench, we implement three tool conditions:          enforceable requirements, the only ones that can be validated
(1) the raw condition uses an MCP server exposing generic          accurately and are addressed in this work. By construction, our
GET and POST tools, mirroring the original benchmark design        symbolic guardrails prevent violations by rejecting all non-
in which the agent constructs HTTP requests autonomously;          compliant tool calls; we therefore measure policy violations
(2) the baseline condition uses an MCP server with eight           only under raw and baseline, where guardrails are absent.
tools, one per HTTP endpoint in the original benchmark; and           To detect requirement violations, we also apply the symbolic
(3) the guardrail condition wraps the eight-tool baseline with     guardrails in the raw and baseline conditions, but only to
symbolic guardrails for 23 enforceable requirements, drawn         record triggers rather than reject tool calls. We then count
from the 34 classified as enforceable in Study 2. Of the           the tasks that trigger at least one violation in each benchmark.
remaining 11, one was already implemented in the benchmark;           A complication arises when a guardrail adds extra tool
the other ten require substantial medical domain knowledge an      parameters (Sec. V-A2), affecting 6 of 16 tools in τ 2 -Bench
expert could enumerate but was not available to us, such as        and 6 of 8 in MedAgentBench. Because modifying tool
appropriate dosage units for different medications.                signatures could alter agent behavior, we adopt a replay-based
   Across all three benchmarks, baseline and guardrail share       evaluation procedure to avoid biasing the agent: when the
tool schemas, but guardrail adds enforcement parameters            agent calls a baseline tool that would require extra arguments
in 6 of 16 τ 2 -Bench tools and 6 of 8 MedAgentBench               under the guardrail condition for policy violation checks, we
tools. For example, τ 2 -Bench’s cancel_ticket takes only          pause execution, roll back to the state before the baseline
ticket_id in baseline and adds user_id in guardrail to             tool-call decision, and re-prompt the model with the extended
verify ownership via user_id == ticket.user. CAR-                  guardrail signature. If the replayed call uses the same tool
bench needs no additional parameters.                              name and original arguments and supplies the required extra
argument, we use it to assess policy violations. After this             TABLE IV: Experiment Results on Three Benchmarks
assessment, we resume execution from the rollback point                                                 (a) τ 2 -Bench
with the original baseline call, so that the evaluation does
not alter the agent’s behavior. This yields the information                                                 Security & Safety                     Utility
needed for policy-violation checks, such as the user ID for            Model        Condition      Unsafe↓        Unknown          Safe↑      Pass^1↑
cancel_ticket, without altering the reasoning induced                  GPT-4o       baseline        52.0%           0.0%           48.0%           0.36
by the baseline tool schema. If the agent cannot supply the                         guardrail        0.0%            0.0%          100.0%          0.48
                                                                       GPT-5        baseline        20.0%           10.0%          70.0%           0.68
additional argument during replay, we classify the execution                        guardrail        0.0%            0.0%          100.0%          0.70
as unsafe, since the context is insufficient for a security or
safety check. If it instead selects a different tool or changes                                 (b) CAR-bench (GPT-5)
the original arguments, we retry up to five times; if the call
                                                                                                    Security & Safety                  Utility
still cannot be reproduced, we label the outcome as unknown.
   Since CAR-bench requires no additional parameters under                   Condition      Unsafe↓         Safe↑        rpolicy ↑     Pass^1↑
guardrail condition, no tool calls receive an unknown outcome,               baseline           21.0%      79.0%            0.83           0.59
                                                                             guardrail           0.0%      100.0%           0.97           0.72
so we do not report its unknown rate for policy violation.
   For all dependent variables, we assess the significance of                              (c) MedAgentBench (GPT-5)
differences across conditions using the paired McNemar test.
   5) Threats to Validity: Our evaluation covers only policy                                                  Security & Safety                    Utility
violations that are reliably detectable via symbolic guardrails          Data         Condition         Unsafe↓     Unknown          Safe↑           SR↑
and excludes those that are not. As is common in agent                  Original        raw              39.0%        9.7%            51.3%          0.64
benchmarks, executions are expensive even at benchmark sizes                          baseline           23.0%        0.3%            76.7%          0.59
of 50 to 300 tasks, with a single benchmark run costing                               guardrail          0.0%         0.0%           100.0%          0.67
                                                                      Adversarial       raw              78.0%        4.0%            18.0%            –
approximately USD 80. This constrains the experimental con-                           baseline           62.0%        4.0%            34.0%            –
ditions (e.g., model choices) and repetitions we can evaluate,                        guardrail          0.0%         0.0%           100.0%            –
so our findings reveal general trends, and the statistical tests
may detect only large effects. Further work is needed to
assess generalization beyond the three benchmarks. Finally, all
experimental conditions include the full policy in the system
prompt, even though many policy sentences are technically            frequently violate security and safety requirements stated
redundant under the guardrail condition; future work could           explicitly in the system prompt. Stronger models make fewer
examine the trade-offs of removing this redundancy.                  mistakes, and future models with larger context windows and
B. Results                                                           better instruction following may reduce these errors further,
   AI agents without guardrails violate requirements that            but easily preventable failures still create unnecessary risk.
symbolic guardrails can enforce. As shown in TABLE IV,               Dedicated neural guardrails can likely reduce many of these
policy violations are common across all settings without             errors, but add non-trivial runtime cost and still leave residual
symbolic guardrails: 20% to 78% of task executions violate           risk. In adversarial settings, for example, prompt injection that
symbolically enforceable requirements. Violations are more           causes a model to offer compensation improperly or prescribe
frequent on adversarial tasks (TABLE IVc) and for weaker             the wrong medication, deploying such agents may become too
models (compare GPT-4o and GPT-5 in TABLE IVa), but                  risky to be feasible. Although not all desirable security and
occur under every condition without guardrails. Under the            safety properties can be enforced symbolically, practitioners
guardrail condition, such violations are prevented by construc-      in high-assurance commercial settings should assess whether
tion, and the difference is statistically significant (p < 0.01 in   the most important requirements can be specified and enforced
all cases). AR-bench’s rpolicy metric (TABLE IVb), evaluated         this way, then use neural guardrails for the remaining critical
in part by an LLM judge, shows the same pattern (p < 0.01).          requirements as part of a deliberate risk assessment.
   Symbolic guardrails do not sacrifice agent utility. As
shown in TABLE IV, utility increases under the guardrail                Security, safety, and utility are not necessarily a trade-
condition across all datasets, though several improvements           off. Intuitively, guardrails seem to constrain agent flexibility,
are not statistically significant (p = 0.18 for GPT-4o and           but our results suggest they actually help the model explore
p = 1.00 for GPT-5 on τ 2 -Bench; p < 0.01 on CAR-                   safe solutions more effectively. By inspecting the agent-
bench; p = 0.27 vs. raw and p < 0.01 vs. baseline on                 interaction traces, we provide a possible explanation: when
MedAgentBench). Overall, the results suggest that symbolic           a symbolic guardrail blocks an unsafe action, it prevents
enforcement is unlikely to harm utility and may improve it.          the agent from terminating incorrectly and returns an error
                                                                     message explaining why the action failed, why it was insecure
C. Discussion                                                        or unsafe, and which requirement it violated. The agent can
  Relying on models alone to enforce security and safety             then use this feedback to adjust, retry with a safer alternative,
requirements is risky. Even without adversarial users, agents        and often complete the task successfully.
                     VI. C ONCLUSION                                                           R EFERENCES
   We argue that symbolic guardrails are an overlooked but         [1] X. Ma, Y. Gao, Y. Wang, R. Wang, X. Wang, Y. Sun et al., “Safety
highly practical mechanism for AI agent security and safety,           at scale: A comprehensive survey of large model and agent safety,”
                                                                       Foundations and Trends in Privacy and Security, vol. 8, no. 3-4, pp.
especially in domain-specific, risk-averse commercial settings.        1–240, 2026.
Most existing benchmarks do not specify verifiable security        [2] Z. Deng, Y. Guo, C. Han, W. Ma, J. Xiong, S. Wen, and Y. Xiang, “Ai
or safety requirements; when they do, many can be enforced             agents under threat: A survey of key security challenges and future
symbolically through simple methods. These guardrails elim-            pathways,” ACM Comput. Surv., vol. 57, no. 7, Feb. 2025. [Online].
                                                                       Available: https://doi.org/10.1145/3716628
inate a large class of security and safety violations without      [3] M. Dehghani, Y. Tay, A. A. Gritsenko, Z. Zhao, N. Houlsby, F. Diaz,
reducing agent utility. Symbolic guardrails are not a complete         D. Metzler, and O. Vinyals, “The benchmark lottery,” 2021. [Online].
solution, as some requirements still depend on model-based             Available: https://arxiv.org/abs/2107.07002
                                                                   [4] I. D. Raji, E. Denton, E. M. Bender, A. Hanna, and A. Paullada, “AI
judgment and neural guardrails, but using inductive methods            and the everything in the whole wide world benchmark,” in Thirty-
for requirements that could instead be enforced symbolically           fifth Conference on Neural Information Processing Systems Datasets
introduces avoidable risk for limited benefit. We argue that           and Benchmarks Track (Round 2), 2021.
                                                                   [5] Sierra, “Meet your agent,” https://sierra.ai/product/meet-your-agent,
broader use of symbolic guardrails is a promising path toward          2026, accessed: 2026-03-12.
deploying domain-specific AI agents in high-stakes settings        [6] Hippocratic AI, “Hippocratic ai: Home,” https://hippocraticai.com/,
with stronger security and safety guarantees.                          2026.
                                                                   [7] Anysphere, Inc., “Cursor: The ai code editor,” https://cursor.com, 2026.
                    ACKNOWLEDGMENT                                 [8] OpenClaw, “Openclaw — personal ai assistant,” https://openclaw.ai/,
                                                                       2026, accessed: 2026-03-12.
   This work was supported in part by the National Science         [9] M. Isaac and E. Tan. (2026) In a.i. blunder, more than 34,000 instagram
Foundation (award 2206859) and an unrestricted gift from               accounts were attacked. [Online]. Available: https://www.nytimes.com/
                                                                       2026/06/09/technology/instagram-hack-ai-bug.html
Google’s GARA. We would also like to thank Chenyang Yang,         [10] L. Cecco. (2024) Air canada ordered to pay customer who was
the SSSG attendees, and the S3C2 Quarterly Meeting attendees           misled by airline’s chatbot. The Guardian. [Online]. Available: https:
for their valuable feedback on this work.                              //www.theguardian.com/world/2024/feb/16/air-canada-chatbot-lawsuit
                                                                  [11] V. Barres, H. Dong, S. Ray, X. Si, and K. Narasimhan, “τ 2 -bench:
                                                                       Evaluating conversational agents in a dual-control environment,” 2025.
                                                                       [Online]. Available: https://arxiv.org/abs/2506.07982
                                                                  [12] G. Stoneburner, A. Goguen, and A. Feringa, “Risk management
                                                                       guide for information technology systems,” 2002-07-01 00:07:00 2002.
                                                                       [Online]. Available: https://tsapps.nist.gov/publication/get_pdf.cfm?pu
                                                                       b_id=151254
                                                                  [13] K. Zhou, S. Jangam, A. Nagarajan, T. Polu, S. Oruganti, C. Liu, C.-C.
                                                                       Kuo, Y. Zheng, S. Narayanaraju, and X. E. Wang, “Safepro: Evaluating
                                                                       the safety of professional-level ai agents,” 2026. [Online]. Available:
                                                                       https://arxiv.org/abs/2601.06663
                                                                  [14] R. Sandhu, D. Ferraiolo, and R. Kuhn, “The nist model for role-based
                                                                       access control: towards a unified standard,” in ACM workshop on Role-
                                                                       based access control, vol. 10, no. 344287.344301, 2000.
                                                                  [15] W. G. J. Halfond, J. Viegas, and A. Orso, “A classification of sql
                                                                       injection attacks and countermeasures,” in International Symposium
                                                                       on Signals, Systems, and Electronics, 2006. [Online]. Available:
                                                                       https://api.semanticscholar.org/CorpusID:5969227
                                                                  [16] D. E. Denning, “A lattice model of secure information flow,” Commun.
                                                                       ACM, vol. 19, no. 5, p. 236–243, May 1976. [Online]. Available:
                                                                       https://doi.org/10.1145/360051.360056
                                                                  [17] J. Viega and G. R. McGraw, Building secure software: how to avoid
                                                                       security problems the right way. Pearson Education, 2001.
                                                                  [18] W. Luo, S. Dai, X. Liu, S. Banerjee, H. Sun, M. Chen, and C. Xiao,
                                                                       “AGrail: A lifelong agent guardrail with effective and adaptive safety
                                                                       detection,” in Proceedings of the 63rd Annual Meeting of the Associa-
                                                                       tion for Computational Linguistics (Volume 1: Long Papers), W. Che,
                                                                       J. Nabende, E. Shutova, and M. T. Pilehvar, Eds. Vienna, Austria:
                                                                       Association for Computational Linguistics, Jul. 2025, pp. 8104–8139.
                                                                  [19] S. Chennabasappa, C. Nikolaidis, D. Song, D. Molnar, S. Ding,
                                                                       S. Wan, S. Whitman, L. Deason, N. Doucette, A. Montilla, A. Gampa,
                                                                       B. de Paola, D. Gabi, J. Crnkovich, J.-C. Testud, K. He, R. Chaturvedi,
                                                                       W. Zhou, and J. Saxe, “Llamafirewall: An open source guardrail
                                                                       system for building secure ai agents,” 2025. [Online]. Available:
                                                                       https://arxiv.org/abs/2505.03574
                                                                  [20] T. Rebedea, R. Dinu, M. N. Sreedhar, C. Parisien, and J. Cohen, “NeMo
                                                                       guardrails: A toolkit for controllable and safe LLM applications with
                                                                       programmable rails,” in Proceedings of the 2023 Conference on Empir-
                                                                       ical Methods in Natural Language Processing: System Demonstrations,
                                                                       Y. Feng and E. Lefever, Eds. Singapore: Association for Computational
                                                                       Linguistics, Dec. 2023, pp. 431–445.
                                                                  [21] S. Yao, N. Shinn, P. Razavi, and K. Narasimhan, “τ -bench: A
                                                                       benchmark for tool-agent-user interaction in real-world domains,” 2024.
                                                                       [Online]. Available: https://arxiv.org/abs/2406.12045
[22] M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem,               Elias, R. Green, S. Mokrá, N. Fernando, B. Wu, R. Foley, S. Young,
     S. Tople, L. Wutschitz, and S. Zanella-Béguelin, “Securing ai                     I. Gabriel, W. Isaac, J. Mellor, D. Hassabis, K. Kavukcuoglu,
     agents with information-flow control,” 2025. [Online]. Available:                 L. A. Hendricks, and G. Irving, “Improving alignment of dialogue
     https://arxiv.org/abs/2505.23643                                                  agents via targeted human judgements,” 2022. [Online]. Available:
[23] H. Wang, C. M. Poskitt, and J. Sun, “Agentspec: Customizable runtime              https://arxiv.org/abs/2209.14375
     enforcement for safe and reliable llm agents,” 2025. [Online]. Available:    [41] Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones et al.,
     https://arxiv.org/abs/2503.18666                                                  “Constitutional ai: Harmlessness from ai feedback,” 2022. [Online].
[24] Y. Tan, Y. Jiang, Y. Li, J. Liu, X. Bu, W. Su, X. Yue, X. Zhu,                    Available: https://arxiv.org/abs/2212.08073
     and B. Zheng, “Equilibrate rlhf: Towards balancing helpfulness-              [42] H. Lee, S. Phatale, H. Mansoor, T. Mesnard, J. Ferret, K. Lu, C. Bishop,
     safety trade-off in large language models,” 2025. [Online]. Available:            E. Hall, V. Carbune, A. Rastogi, and S. Prakash, “Rlaif vs. rlhf: scaling
     https://arxiv.org/abs/2502.11555                                                  reinforcement learning from human feedback with ai feedback,” in
[25] Y. Dong, R. Mu, Y. Zhang, S. Sun, T. Zhang, C. Wu, G. Jin, Y. Qi,                 Proceedings of the 41st International Conference on Machine Learning,
     J. Hu, J. Meng et al., “Safeguarding large language models: A survey,”            ser. ICML’24. JMLR.org, 2024.
     Artificial intelligence review, vol. 58, no. 12, p. 382, 2025.               [43] W. Yuan, R. Y. Pang, K. Cho, X. Li, S. Sukhbaatar, J. Xu, and
[26] T. Schick, J. Dwivedi-Yu, R. Dessi, R. Raileanu, M. Lomeli, E. Hambro,            J. Weston, “Self-rewarding language models,” in Proceedings of the
     L. Zettlemoyer, N. Cancedda, and T. Scialom, “Toolformer: Language                41st International Conference on Machine Learning, ser. ICML’24.
     models can teach themselves to use tools,” in Advances in Neural                  JMLR.org, 2024.
     Information Processing Systems, A. Oh, T. Naumann, A. Globerson,             [44] E. Perez, S. Huang, F. Song, T. Cai, R. Ring, J. Aslanides, A. Glaese,
     K. Saenko, M. Hardt, and S. Levine, Eds., vol. 36. Curran Associates,             N. McAleese, and G. Irving, “Red teaming language models with
     Inc., 2023, pp. 68 539–68 551.                                                    language models,” in Proceedings of the 2022 Conference on Empirical
[27] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal et al.,         Methods in Natural Language Processing, Y. Goldberg, Z. Kozareva,
     “Retrieval-augmented generation for knowledge-intensive nlp tasks,”               and Y. Zhang, Eds. Abu Dhabi, United Arab Emirates: Association for
     Advances in neural information processing systems, vol. 33, pp. 9459–             Computational Linguistics, Dec. 2022, pp. 3419–3448.
     9474, 2020.                                                                  [45] D. Ganguli, L. Lovitt, J. Kernion, A. Askell, Y. Bai, S. Kadavath
[28] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. R. Narasimhan, and Y. Cao,          et al., “Red teaming language models to reduce harms: Methods,
     “React: Synergizing reasoning and acting in language models,” in The              scaling behaviors, and lessons learned,” 2022. [Online]. Available:
     Eleventh International Conference on Learning Representations, 2023.              https://arxiv.org/abs/2209.07858
[29] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao,                [46] P. Y. Zhong, S. Chen, R. Wang, M. McCall, B. L. Titzer,
     “Reflexion: language agents with verbal reinforcement learning,” in Ad-           H. Miller, and P. B. Gibbons, “Rtbas: Defending llm agents against
     vances in Neural Information Processing Systems, A. Oh, T. Naumann,               prompt injection and privacy leakage,” 2025. [Online]. Available:
     A. Globerson, K. Saenko, M. Hardt, and S. Levine, Eds., vol. 36. Curran           https://arxiv.org/abs/2502.08966
     Associates, Inc., 2023, pp. 8634–8652.                                       [47] Y. Liu, Y. Jia, R. Geng, J. Jia, and N. Z. Gong, “Formalizing and
[30] Anthropic. (2024) Model context protocol. [Online]. Available:                    benchmarking prompt injection attacks and defenses,” in 33rd USENIX
     https://github.com/modelcontextprotocol                                           Security Symposium (USENIX Security 24). Philadelphia, PA: USENIX
[31] R. Surapaneni, M. Jha, M. Vakoc, and T. Segal. (2025, Apr)                        Association, Aug. 2024, pp. 1831–1847. [Online]. Available: https:
     Announcing the agent2agent protocol (a2a). [Online]. Available: https://          //www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei
     developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/        [48] Z. Xiang, L. Zheng, Y. Li, J. Hong, Q. Li, H. Xie, J. Zhang, Z. Xiong,
[32] J. Lei, V. Gumma, R. Bhardwaj, S. M. Lim, C. Li, A. Zadeh,                        C. Xie, C. Yang, D. Song, and B. Li, “Guardagent: Safeguard llm
     and S. Poria, “Offtopiceval: When large language models enter                     agents by a guard agent via knowledge-enabled reasoning,” 2025.
     the wrong chat, almost always!” 2026. [Online]. Available: https:                 [Online]. Available: https://arxiv.org/abs/2406.09187
     //arxiv.org/abs/2509.26495                                                   [49] Z. Chen, M. Kang, and B. Li, “ShieldAgent: Shielding agents via verifi-
[33] OpenAI. (2025) Chatgpt agent. [Online]. Available: https://chatgpt.co             able safety policy reasoning,” in Proceedings of the 42nd International
     m/features/agent                                                                  Conference on Machine Learning, ser. Proceedings of Machine Learning
[34] Microsoft. (2023) Getting started with copilot on windows. [Online].              Research, A. Singh, M. Fazel, D. Hsu, S. Lacoste-Julien, F. Berkenkamp,
     Available: https://support.microsoft.com/en-us/topic/getting-started-wit          T. Maharaj, K. Wagstaff, and J. Zhu, Eds., vol. 267. PMLR, 13–19 Jul
     h-copilot-on-windows-1159c61f-86c3-4755-bf83-7fbff7e0982d                         2025, pp. 8313–8344.
[35] Anthropic. (2026) Claude code overview. Accessed: 2026-03-25.                [50] N. Abaev, D. Klimov, G. Levinov, D. Mimran, Y. Elovici,
     [Online]. Available: https://docs.anthropic.com/en/docs/claude-code/ov            and A. Shabtai, “Agentguardian: Learning access control policies
     erview                                                                            to govern ai agent behavior,” 2026. [Online]. Available: https:
[36] K.-H. Huang, A. Prabhakar, O. Thorat, D. Agarwal, P. K. Choubey,                  //arxiv.org/abs/2601.10440
     Y. Mao, S. Savarese, C. Xiong, and C.-S. Wu, “CRMArena-pro:                  [51] A. Kamath, S. Zhang, C. Xu, S. Ugare, G. Singh, and S. Misailovic,
     Holistic assessment of LLM agents across diverse business scenarios               “Enforcing temporal constraints for llm agents,” 2025. [Online].
     and interactions,” Transactions on Machine Learning Research, 2026.               Available: https://arxiv.org/abs/2512.23738
     [Online]. Available: https://openreview.net/forum?id=EPlpe3Fx1x              [52] J. Cui, Z. Li, L. Xing, and X. Liao, “Maris: A formally verifiable
[37] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin,                privacy policy enforcement paradigm for multi-agent collaboration
     C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton,                   systems,” 2026. [Online]. Available: https://arxiv.org/abs/2505.04799
     F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. F. Christiano,   [53] T. Shi, J. He, Z. Wang, H. Li, L. Wu, W. Guo, and D. Song,
     J. Leike, and R. Lowe, “Training language models to follow instructions           “Progent: Programmable privilege control for llm agents,” 2025.
     with human feedback,” in Advances in Neural Information Processing                [Online]. Available: https://arxiv.org/abs/2504.11703
     Systems, S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and         [54] A. Doshi, Y. Hong, C. Xu, E. Kang, A. Kapravelos, and C. Kästner,
     A. Oh, Eds., vol. 35. Curran Associates, Inc., 2022, pp. 27 730–27 744.           “Towards verifiably safe tool use for llm agents,” 2026. [Online].
[38] Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma                     Available: https://arxiv.org/abs/2601.08012
     et al., “Training a helpful and harmless assistant with reinforcement        [55] J. Kim, W. Choi, and B. Lee, “Prompt flow integrity to prevent
     learning from human feedback,” 2022. [Online]. Available: https:                  privilege escalation in llm agents,” 2025. [Online]. Available:
     //arxiv.org/abs/2204.05862                                                        https://arxiv.org/abs/2503.15547
[39] N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss,                 [56] N. Palumbo, S. Choudhary, J. Choi, P. Chalasani, and S. Jha, “Policy
     A. Radford, D. Amodei, and P. F. Christiano, “Learning to summarize               compiler for secure agentic systems,” 2026. [Online]. Available:
     with human feedback,” in Advances in Neural Information Processing                https://arxiv.org/abs/2602.16708
     Systems, H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin,       [57] F. Wu, E. Cecchetti, and C. Xiao, “System-level defense against indirect
     Eds., vol. 33. Curran Associates, Inc., 2020, pp. 3008–3021.                      prompt injection attacks: An information flow control perspective,”
[40] A. Glaese, N. McAleese, M. Tr˛ebacz, J. Aslanides, V. Firoiu,                     2024. [Online]. Available: https://arxiv.org/abs/2409.19091
     T. Ewalds, M. Rauh, L. Weidinger, M. Chadwick, P. Thacker,                   [58] E. Debenedetti, I. Shumailov, T. Fan, J. Hayes, N. Carlini, D. Fabian,
     L. Campbell-Gillingham, J. Uesato, P.-S. Huang, R. Comanescu,                     C. Kern, C. Shi, A. Terzis, and F. Tramèr, “Defeating prompt injections
     F. Yang, A. See, S. Dathathri, R. Greig, C. Chen, D. Fritz, J. S.                 by design,” 2025. [Online]. Available: https://arxiv.org/abs/2503.18813
[59] B. Kitchenham and S. Charters, “Guidelines for performing systematic
     literature reviews in software engineering,” Keele University and Uni-
     versity of Durham, Tech. Rep., 2007.
[60] OpenAI, “Chatgpt,” https://chatgpt.com/, 2026, large language model
     accessed March 20, 2026.
[61] K. R. Felizardo, E. Mendes, M. Kalinowski, É. F. Souza, and N. L.
     Vijaykumar, “Using forward snowballing to update systematic reviews
     in software engineering,” in Proceedings of the 10th ACM/IEEE Interna-
     tional Symposium on Empirical Software Engineering and Measurement,
     2016, pp. 1–6.
[62] I. Levy, B. wiesel, S. Marreed, A. Oved, A. Yaeli, and S. Shlomov, “ST-
     webagentbench: A benchmark for evaluating safety and trustworthiness
     in web agents,” in The Fourteenth International Conference on Learning
     Representations, 2026. [Online]. Available: https://openreview.net/for
     um?id=MuCDzH0ctf
[63] ISO/IEC/IEEE International Standard – Systems and software engineer-
     ing – Life cycle processes – Requirements engineering, ISO/IEC/IEEE
     Std. ISO/IEC/IEEE 29 148:2018, Nov. 2018.
[64] D. M. Berry, E. Kamsties, and M. M. Krieger, “From Contract
     Drafting to Software Specification: Linguistic Sources of Ambiguity,”
     University of Waterloo, Tech. Rep., Nov. 2003. [Online]. Available:
     https://cs.uwaterloo.ca/~dberry/handbook/ambiguityHandbook.pdf
[65] H. Femmer, D. Méndez Fernández, S. Wagner, and S. Eder, “Rapid
     quality assurance with requirements smells,” Journal of Systems and
     Software, vol. 123, pp. 190–213, 2017.
[66] H. Femmer and A. Vogelsang, “Requirements quality is quality in use,”
     IEEE Software, vol. 36, no. 3, pp. 83–91, 2019.
[67] M. Andriushchenko, A. Souly, M. Dziemian, D. Duenas, M. Lin,
     J. Wang, D. Hendrycks, A. Zou, J. Z. Kolter, M. Fredrikson,
     Y. Gal, and X. Davies, “Agentharm: A benchmark for measuring
     harmfulness of LLM agents,” in The Thirteenth International
     Conference on Learning Representations, 2025. [Online]. Available:
     https://openreview.net/forum?id=AC5n7xHuR1
[68] J. Lee, D. Hahm, J. S. Choi, W. B. Knox, and K. Lee,
     “Mobilesafetybench: Evaluating safety of autonomous agents in mobile
     device control,” Proceedings of the AAAI Conference on Artificial
     Intelligence, vol. 40, no. 44, pp. 37 565–37 573, Mar. 2026. [Online].
     Available: https://ojs.aaai.org/index.php/AAAI/article/view/41090
[69] S. Wang and H. Zhang, “Mpci-bench: A benchmark for multimodal
     pairwise contextual integrity evaluation of language model agents,”
     2026. [Online]. Available: https://arxiv.org/abs/2601.08235
[70] J. Kirmayr, L. Stappen, and E. André, “Car-bench: Evaluating
     the consistency and limit-awareness of llm agents under real-world
     uncertainty,” 2026. [Online]. Available: https://arxiv.org/abs/2601.22027
[71] T. Chen, C. Hu, G. Gao, D. Liu, X. Hu, and W. Wang, “Lps-bench:
     Benchmarking safety awareness of computer-use agents in long-horizon
     planning under benign and adversarial scenarios,” 2026. [Online].
     Available: https://arxiv.org/abs/2602.03255
[72] T. Scholak, N. Schucher, and D. Bahdanau, “PICARD: Parsing in-
     crementally for constrained auto-regressive decoding from language
     models,” in Proceedings of the 2021 Conference on Empirical Methods
     in Natural Language Processing, M.-F. Moens, X. Huang, L. Specia,
     and S. W.-t. Yih, Eds. Online and Punta Cana, Dominican Republic:
     Association for Computational Linguistics, Nov. 2021, pp. 9895–9901.
[73] Y. Jiang, K. C. Black, G. Geng, D. Park, J. Zou, A. Y. Ng, and J. H.
     Chen, “Medagentbench: a virtual ehr environment to benchmark medical
     llm agents,” Nejm Ai, vol. 2, no. 9, p. AIdbp2500144, 2025.
[74] N. G. Leveson, Engineering a Safer World: Systems Thinking Applied
     to Safety. The MIT Press, 01 2012.
[75] Y. Hong, C. S. Timperley, and C. Kästner, “From hazard identification
     to controller design: Proactive and llm-supported safety engineering for
     ml-powered systems,” in 2025 IEEE/ACM 4th International Conference
     on AI Engineering – Software Engineering for AI (CAIN), 2025, pp.
     113–118.
[76] A. Sabelfeld and A. C. Myers, “Language-based information-flow secu-
     rity,” IEEE Journal on selected areas in communications, vol. 21, no. 1,
     pp. 5–19, 2003.
[77] C. Yang, Y. Shi, Q. Ma, M. X. Liu, C. Kästner, and T. Wu, “What
     prompts don’t say: Understanding and managing underspecification in
     llm prompts,” 2025. [Online]. Available: https://arxiv.org/abs/2505.133
     60
[78] A. Cuadron, P. Yu, Y. Liu, and A. Gupta, “Saber: Small actions, big
     errors - safeguarding mutating steps in llm agents,” 2025. [Online].
     Available: https://arxiv.org/abs/2512.07850
