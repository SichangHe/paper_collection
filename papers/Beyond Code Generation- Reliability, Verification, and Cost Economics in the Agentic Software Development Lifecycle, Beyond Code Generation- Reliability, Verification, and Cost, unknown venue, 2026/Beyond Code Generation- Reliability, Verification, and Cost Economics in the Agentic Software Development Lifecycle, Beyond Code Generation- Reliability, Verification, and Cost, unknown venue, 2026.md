                                        Happy Bhati                                                                     Reliability and Cost in the Agentic SDLC



                                        Beyond Code Generation: Reliability, Verification, and Cost
                                        Economics in the Agentic Software Development Lifecycle
                                           A Systems Synthesis of Industrial Evidence and a Research Agenda for Agentic Engineering

                                                                                              Happy Bhati
                                                                                         bhati.h@northeastern.edu

                                                                                               September 2026

                                                                                                  Abstract
                                                 AI coding systems are moving from autocomplete and chat toward agents that can inspect repositories, edit
                                             multiple files, run tools, write tests, open pull requests, and work for long periods with limited supervision. That
arXiv:2609.04681v1 [cs.SE] 4 Sep 2026




                                             capability changes the bottleneck in software delivery. Recent field experiments show large gains in coding activity,
                                             but newer evidence also shows that those gains attenuate sharply between writing code and shipping reliable
                                             software. Review, integration, testing, security, deployment, and production operations remain constraining
                                             stages; in several studies, the quality of the surrounding harness and verification process matters as much as raw
                                             model capability. At the same time, the economics are changing from predictable per-seat licenses toward variable
                                             token, tool, sandbox, CI, and rework costs.
                                                 This paper synthesizes peer-reviewed software-engineering research, university studies, benchmark audits,
                                             production reports from major technology companies, developer telemetry, and cost-management evidence released
                                             primarily from 2024 through September 2026. It does not report new model experiments. Numerical findings
                                             remain attributed to their original studies. The synthesis develops four engineering concepts: the Agentic SDLC
                                             Throughput Paradox, which describes why code-generation gains can outrun release gains; Production-Qualified
                                             Change (PQC), a unit of output that counts a change only after reliability gates are satisfied; the Verification Tax,
                                             which makes downstream review and assurance costs explicit; and an Agentic SDLC Control Plane that allocates
                                             autonomy subject to cost, reliability, and human-attention budgets. The paper then maps an evidence-based
                                             horizon from today’s supervised coding agents to future policy-bounded software factories. The resulting research
                                             agenda argues that the useful question is no longer how much code an agent can generate, but how much
                                             production-qualified value an engineering system can deliver per dollar, per reviewer-hour, and per unit of
                                             operational risk.

                                        Keywords: agentic software engineering, software development lifecycle, coding agents, code review, software
                                        testing, reliability, AI cost, FinOps, developer productivity, AI observability, software supply chain, autonomous
                                        agents.


                                        1 Introduction

                                        Software engineering is entering an odd phase: producing a plausible patch is getting cheaper at the same time that
                                        proving the patch deserves to ship is becoming more important. Coding agents can now search a repository, modify
                                        code, run commands, and iterate on failures. This is a genuine capability change, not merely a faster autocomplete.
                                        My earlier work described this transition as an emerging Agentic Software Development Lifecycle (A-SDLC) and
                                        focused on architecture, delegated execution, and changes in engineering work [1]. The present paper starts one step
                                        later. It asks what happens when organizations try to operate that lifecycle at scale.
                                        The answer emerging from recent evidence is not simply “developers become faster.” In three randomized field
                                        experiments spanning 4,867 developers, AI assistance increased completed tasks by 26.08% in the pooled estimate
                                        [3]. That is strong causal evidence that assistance can improve output in some professional settings. Yet a 2026
                                        study of more than 100,000 GitHub developers found a much larger cumulative increase in coding activity from
                                        autonomous agents - 180% at the commit level - that fell to 50% at the project level and 30% at actual releases
                                        [4]. The authors describe a weak-link production structure: writing code accelerates faster than the human and
                                        organizational stages needed to turn changes into shipped software.
                                        That gap is visible from several directions. Google reports millions of code-review comments annually and about
                                        60 minutes of active author shepherding time between sending a change for review and submitting it [6]. Google’s
                                        2025 DORA study, based on nearly 5,000 technology professionals, associated higher AI adoption with higher
                                        delivery throughput but still found a negative relationship with delivery stability [5]. Stanford’s SWE-chat dataset


                                                                                                      1
Happy Bhati                                                                 Reliability and Cost in the Agentic SDLC


of 6,000 real coding-agent sessions found that only 44% of agent-produced code survived into user commits, while
users corrected, interrupted, or otherwise pushed back on agent outputs in 44% of turns; agent-written code also
showed more security vulnerabilities than human-written code in that dataset [8]. Long-horizon evaluations reveal a
different failure shape: SWE-Marathon rollouts averaged 27.2 million tokens, yet the initial study found no tested
configuration above 30% pass@1 and observed reward-hacking behavior in 13.8% of rollouts [9].
These are not contradictory results. They describe different layers of the same system. AI can increase local coding
productivity while the global delivery system remains constrained by verification, coordination, human judgment,
and operational risk. In an agentic workflow, those constraints are not side issues. They become part of the runtime.
Cost follows the same pattern. The direct model bill is easy to see. The rest is distributed across context construction,
repeated attempts, tool calls, sandboxes, CI minutes, security scans, reviewer attention, rework, incidents, and the
infrastructure required to observe all of it. Northeastern researchers show that token use can vary substantially across
programming languages even after controlling for problem difficulty, in part because agents produce non-compiling
attempts, revise already-passing solutions, and distrust provided tests [11]. The FinOps Foundation reports that 98%
of surveyed practitioners now manage AI spend, up from 31% two years earlier, and identifies AI cost management
as the top skillset to develop [12]. Gartner goes further and forecasts that AI coding cost could exceed the average
developer salary by 2028 under growing token consumption and consumption-based pricing [13]. That forecast
should not be treated as a measured inevitability, but it is a useful signal that engineering leaders are moving from
adoption questions to unit-economics questions.
This paper connects those threads. It treats an AI coding agent as one component in a production system, not as
the unit of evaluation. The goal is to identify the control problem organizations now face: how much autonomy
should a task receive, which model and harness should execute it, how much verification is required, when should a
human intervene, and when does another agent attempt stop being worth its cost?
The synthesis is organized around four concepts:
1. Agentic SDLC Throughput Paradox. Upstream change generation can accelerate much faster than
   downstream validation and release, so local productivity growth does not translate linearly into shipped value.
2. Production-Qualified Change (PQC). A pull request, commit, or generated patch is not finished output. A
   change becomes useful production output only after it crosses the relevant review, test, security, deployment, and
   operational gates.
3. Verification Tax. Agentic generation creates a variable assurance workload. Its cost includes CI, reviewer time,
   security analysis, rework, and escaped failures, not only tokens.
4. Agentic SDLC Control Plane. A policy and telemetry layer should allocate models, context, parallelism,
   retries, tests, and human review according to task risk, reliability evidence, budget, and organizational capacity.
The purpose is not to claim that any one company has already implemented this complete control plane. The
purpose is to turn a scattered set of research results into a systems model that can be tested.


2 Scope, Evidence Selection, and Claim Boundary

The review emphasizes work from 2024 through September 3, 2026, with earlier benchmark papers included where
they establish an important baseline. Sources were selected for direct relevance to at least one of six questions: (1)
coding-agent capability, (2) developer productivity and work allocation, (3) code review and testing, (4) reliability
and security, (5) coordination and long-horizon execution, or (6) cost and resource governance.
The source set intentionally mixes research types because production software engineering is not well described by
benchmark papers alone. A randomized field experiment answers a different question from a public leaderboard;
an industrial deployment report answers a different question from a controlled academic study; a market forecast
is weaker evidence than either, but can still describe what organizations are budgeting for. Table 1 keeps those
categories visible.




                                                           2
Happy Bhati                                                                 Reliability and Cost in the Agentic SDLC


Table 1: Evidence hierarchy used in this synthesis. Tiers describe evidence type, not a universal ranking of research
quality.


 Tier    Evidence type           Representative sources                      How claims are used
 A       Peer-reviewed      /    Management Science developer RCTs;          Strong basis for findings in the studied set-
         major     conference    Google ICSE code-review work; Meta FSE      ting; not generalized beyond the design.
         research                TestGen-LLM; Microsoft ASE developer-
                                 agent study
 B       Academic preprints /    Stanford SWE-chat and CooperBench;          Frontier evidence; useful for identifying
         university research     SWE-Marathon; MIT/NBER shipping             emerging failure modes and hypotheses.
                                 study; Northeastern token-cost study
 C       Benchmark / evalua-     SWE-bench, SWE-Lancer, benchmark au-        Used to measure specific capabilities; bench-
         tion research           dits, long-horizon benchmarks               mark limitations are treated as part of the
                                                                             result.
 D       Documented indus-       Google DORA; GitHub security validation     Evidence of practice or observed telemetry,
         trial telemetry /       and ROI dashboard; company telemetry        with vendor/self-report boundary stated.
         deployment              and engineering reports
 E       Cost / market / work-   FinOps Foundation; Gartner forecasts        Used for adoption and planning signals; fore-
         force reports                                                       casts are explicitly not treated as measured
                                                                             outcomes.
 F       This paper’s synthe-    PQC, Verification Tax, Autonomy Budget,     Proposed engineering constructs to be vali-
         sis                     Control Plane, horizon map                  dated, not empirical results.




A second boundary is important because this paper builds on my prior A-SDLC paper [1]. The earlier paper
mapped the architectural transition from assistant to agent. This paper does not repeat that architecture as a new
contribution. It narrows the question to reliability, verification capacity, delivery economics, and the operating model
required when agentic work becomes routine. One additional self-citation is used for AI observability, where prior
work proposed tracing model cost and quality together [2]. The aim is continuity, not citation inflation.
No benchmark score, productivity gain, code-review statistic, security result, market number, or company deployment
outcome in this paper is an original measurement. Those results remain with the cited authors and organizations.


3 From Coding Capability to Production Capability

3.1 Benchmarks established the capability leap

SWE-bench moved coding evaluation from small algorithmic problems toward real GitHub issues and repository
states [14]. SWE-agent showed that the agent-computer interface around a model materially affects performance,
making tools and interaction design part of the system rather than neutral plumbing [15]. OpenAI’s SWE-Lancer
added an economic dimension by collecting more than 1,400 real freelance software-engineering tasks representing
roughly US$1 million in historical payouts [16]. These benchmarks made agent progress legible and pushed models
toward repository-scale work.
The benchmarks also exposed a problem that becomes more important as scores rise: automated tests are not a
perfect proxy for software correctness. OpenAI’s 2026 audit of SWE-bench Verified reported that, among 138 tasks
that one frontier model did not consistently solve, 59.4% had material issues in test design or problem description.
The same analysis identified contamination risk from public tasks and solutions [17]. A separate position paper
argues that coding benchmarks conflate the model, harness, context, execution environment, and feedback signals
into a single score, making it difficult to know what actually improved [18].
For production engineering this matters because a high benchmark score is evidence about one slice of the delivery
path. It is not a release-readiness certificate. A benchmark usually starts with a well-formed task and ends when a
hidden test suite passes. A company starts earlier - with incomplete requirements and organizational context - and
ends later, after security review, deployment, monitoring, user behavior, and maintenance.


                                                           3
Happy Bhati                                                                     Reliability and Cost in the Agentic SDLC


3.2 Software engineering is broader than patch generation

Gu et al., with authors from MIT, UC Berkeley, Stanford, and Cornell, argue that current AI-for-software-engineering
work over-concentrates on code generation relative to the breadth of real engineering activity: testing, debugging,
review, refactoring, performance, security, migration, communication, and large-scale change management all matter
[19]. Microsoft Research reaches a similar conclusion from direct observation. In a 2025 ASE study of 19 developers
resolving 33 real repository issues with an interactive agent, roughly half the issues were successfully resolved;
incremental collaboration outperformed one-shot use, and developers still struggled with trust, debugging, and
testing [20].
The practical implication is that “agent capability” should be decomposed. A useful organization-level question is
not whether an agent can write a patch, but whether the entire human-agent system can consistently move a change
from intent to production without creating more validation work than it removes.


4 The Agentic SDLC Throughput Paradox

The clearest recent evidence for a bottleneck migration comes from Demirer, Musolff, and Yang [4]. Using data
from more than 100,000 GitHub developers combined with AI usage telemetry, they estimate progressively larger
cumulative effects on commits as tools move from autocomplete to interactive and autonomous agents: 40%, 140%,
and 180%, respectively. But at the autonomous-agent stage, the effect is only 50% for the number of projects and
30% for releases.
Figure 1 visualizes that attenuation. The numbers are from Demirer et al.; the “throughput paradox” label is the
synthesis used in this paper.

          Cumulative effect after autonomous-agent adoption

                                                      Commits +180%

                              Projects +50%

                      Releases +30%
                                                                                     estimated cumulative change
          The production hierarchy absorbs a large share of upstream coding
          acceleration. Review, integration, testing, release, and downstream
          demand remain complementary inputs.

Figure 1: The Agentic SDLC Throughput Paradox. Effect sizes are reported by Demirer et al. [4]; this paper’s
interpretation is that the bottleneck migrates downstream as code generation accelerates.


This interpretation is consistent with other evidence. DORA’s 2025 study finds that AI adoption is associated with
higher delivery throughput but a negative relationship with delivery stability [5]. That does not mean AI necessarily
causes instability; DORA is observational and organization-level. It does mean that increasing throughput does not
remove the need for strong testing, version control, feedback loops, and loosely coupled architecture. DORA’s own
framing is useful: AI acts as a mirror and multiplier of the surrounding delivery system.
METR’s early-2025 randomized trial provides a deliberately different view. Sixteen experienced open-source
developers completed 246 tasks in mature repositories they knew well. Developers expected AI to make them faster,
yet the study measured a 19% slowdown in that setting [21]. The result should not be generalized to every developer
or to later tools. Its value is methodological: perceived acceleration can differ from measured end-to-end task time,
particularly when domain knowledge is high and quality standards are strict.
Taken together, these studies suggest a distinction that engineering metrics often blur:

     Generation throughput is the rate at which candidate change is produced. Delivery throughput is the rate
     at which trustworthy change reaches users. Agentic software engineering raises the first rate faster than
     it automatically raises the second.


                                                            4
Happy Bhati                                                                Reliability and Cost in the Agentic SDLC


That distinction becomes the organizing principle for review, testing, reliability, and cost.


5 Code Review Becomes a Capacity Problem

Code review traditionally serves several purposes at once: defect detection, design alignment, security, knowledge
transfer, ownership, maintainability, and organizational accountability. An agent can assist with portions of those
tasks, but increasing the number and size of proposed changes can also create a review queue.
Google’s code-review work provides a useful scale reference. At Google, authors receive millions of reviewer comments
per year, and the average change requires about 60 minutes of active shepherding time between sending for review
and submitting [6]. The team’s ML system can propose edits that resolve reviewer comments, reducing some of that
iteration. Google’s AutoCommenter similarly uses large language models to learn and enforce coding best practices
and was deployed to tens of thousands of developers [7]. These systems show that review itself is automatable in
pieces.
But review automation introduces a recursive assurance problem: if one model generates the change and another
model approves it, what independent evidence remains? The problem is not solved by insisting that a human read
every line either; that simply caps agentic throughput at human review capacity. The more scalable direction is to
separate kinds of evidence.
A high-risk change may require independent static analysis, generated and human-authored tests, dependency/security
checks, ownership review, and a canary. A low-risk documentation change may need far less. In other words, review
should become risk-adaptive rather than uniformly manual or uniformly automated.
Real-world agent use reinforces the point. SWE-chat finds a bimodal pattern: in 41% of sessions agents authored
virtually all committed code, while in 23% humans authored all of it. Only 44% of agent-produced code survived
into commits, and users pushed back in 44% of turns [8]. A plausible interpretation is that interaction and filtering
remain part of the work. Counting generated lines or agent-authored diffs therefore overstates realized engineering
output.


6 Testing: More Generated Tests Are Not Automatically More Assurance

Testing is often proposed as the natural counterweight to AI-generated code: let the agent write code, then let it
write tests. The research is more nuanced.
Meta’s TestGen-LLM provides one of the strongest industrial examples because generated tests are filtered through
objective checks before being recommended. In an Instagram evaluation, 75% of generated test cases built correctly,
57% passed reliably, and 25% increased coverage. Across Meta test-a-thons, the system improved 11.5% of classes
to which it was applied, and engineers accepted 73% of its recommendations for production deployment [22]. The
design lesson is more important than any single percentage: generation was paired with a verification harness that
rejected unhelpful output.
Microsoft Research has similarly explored reinforcement learning from automatic feedback for higher-quality unit-test
generation, motivated partly by the observation that generated tests can contain test smells and weak assertions
[23]. In 2026, Chen et al. studied tests written by software-engineering agents on SWE-bench trajectories and found
that resolved and unresolved tasks showed similar test-writing frequency; many generated tests behaved more like
observational probes than assertion-rich regression tests. Prompting agents to write more or fewer tests did not
significantly change final outcomes in their experiment [24].
The engineering conclusion is not “agents should not write tests.” It is that test volume is a poor assurance metric.
A test is useful when it adds independent discriminatory power against plausible faults. In agentic pipelines, the
verifier itself must be treated as a first-class artifact.
This is also why benchmark audits matter. If hidden tests are too narrow, too wide, or contaminated, an agent can
be judged incorrectly even when the patch is functionally sound [17]. In long-horizon settings, the failure can go the
other way: an agent can find a shortcut through the verifier rather than solve the intended engineering problem.
SWE-Marathon’s 13.8% reward-hacking observation is a direct example [9].




                                                          5
Happy Bhati                                                                   Reliability and Cost in the Agentic SDLC


7 Reliability Is a Chain of Gates, Not a Model Score

A production change accumulates evidence as it moves through the lifecycle. Figure 2 presents a reliability-gate
ladder. This is a synthesis framework, not an industry standard. Its main purpose is to show why passing a repository
benchmark covers only part of production assurance.




                Candidate correctness

                  Requirement           Patch             Build /            Unit /          Integration /
                      fit            correctness        type checks       property tests     contract tests

               Production qualification

                   Security /         Review /            Deploy /         Production        Maintenance /
               dependency policy      ownership            canary         SLO / rollback      regression




Figure 2: Reliability Gate Ladder. Different organizations will use different gates, but the key distinction is between
producing a plausible change and accumulating enough independent evidence to operate it safely.


The gate view aligns with recent system-level reliability work. Jarmak’s 2026 monograph argues that coding agents
are evaluated as models but deployed as systems; reliability depends on the harness, execution state, retrieval,
memory, permissions, review interfaces, and resource allocation [25]. The benchmark-misalignment argument by
Gorinova et al. makes the same point from evaluation: a score can move because the model improved or because the
harness changed [18].
GitHub’s 2026 expansion of automatic security validation to third-party coding agents offers a concrete production
pattern. Agent-generated changes can be checked with CodeQL, dependency advisories, and secret scanning before
the pull request is finalized. GitHub reports that the analogous Copilot cloud-agent validation had already prevented
hundreds of potential security leaks and vulnerabilities since its 2025 release [26]. This is a vendor-reported operational
result, but it illustrates the architecture: autonomy is paired with mandatory machine-verifiable gates.


7.1 Coordination is a separate reliability dimension

As organizations move from one agent to several specialized agents, correctness is no longer only about individual
competence. CooperBench, from Stanford and SAP Labs, contains more than 600 collaborative coding tasks. Agents
were on average about 30% less successful when cooperating than when performing both tasks alone, with failures
linked to poor communication, commitment deviations, and incorrect models of partner behavior [10].
That finding matters for proposals that assume a reviewer agent, test agent, security agent, and implementation
agent will naturally form a reliable team. Specialized agents may still need explicit contracts: ownership boundaries,
structured messages, shared state, conflict resolution, and a coordinator capable of determining which evidence is
authoritative. Agent count is not equivalent to engineering capacity.




                                                            6
Happy Bhati                                                                       Reliability and Cost in the Agentic SDLC


8 Production-Qualified Change: A Better Unit of Output

Traditional developer metrics become fragile in an agentic environment. Lines of code are easy to inflate. Commits
can be split or merged. Pull-request count can rise because an agent produces many small changes. Even “tasks
completed” depends on who defines completion.
A more useful unit is a Production-Qualified Change (PQC). A candidate change i receives PQC credit only if
it satisfies the organization’s relevant qualification vector:
                                                      Y
                                            PQCi =           1{g(i) = pass},                                           (1)
                                                      g∈Gi


where Gi is the set of required gates for that change class. A low-risk documentation edit may have a small Gi ; a
database migration, authentication change, or payment path may have a much larger one. The concept intentionally
allows risk-adaptive policy.
The corresponding throughput is:

                                                                      i∈T PQCi
                                                                   P
                                        PQC-Throughput(T ) =                        .                                  (2)
                                                                       |T |time

PQC is not intended to replace DORA metrics or engineering judgment. It is a bridge between agent telemetry and
delivery outcomes. It makes one assumption explicit: output should be counted after the reliability system has done
its work, not when generation ends.
For organizations that want quality-weighted output, the binary indicator can be extended with severity, customer
value, or risk weights, but that extension should be approached carefully. A single opaque “developer score” would
recreate the metric problems this framework is trying to avoid.


9 The Economics of Agentic Software Delivery

9.1 Token price is only the visible part of cost

A common budget model for AI coding begins with seats or tokens. That is increasingly incomplete. An agentic task
can incur costs from model inference, long repository context, retrieval, tool execution, sandbox compute, repeated
builds, test environments, dependency downloads, parallel attempts, code-review attention, security scans, rework,
and production failures.
A simple Total Cost to Deliver (TTD) model is:

          CTTD = Cmodel + Ccontext + Ctools + Csandbox + CCI + Creview + Csecurity + Crework + Cincident .             (3)

Equation 3 is a cost taxonomy, not a claim that every organization can perfectly allocate every term to an individual
pull request. Its value is to prevent optimization of the easiest visible number while downstream cost grows unnoticed.

               Direct AI cost           Execution cost            Verification cost             Failure cost
              model + context       tools + sandbox + CI         review + security           rework + incident


                   A cheaper model can increase total cost if it needs more retries, generates weaker
                     patches, consumes more CI, or creates more reviewer rework. A more expen-
                     sive model can also be wasteful if it is used on low-risk, easily verified tasks.

Figure 3: Total Cost to Deliver. The diagram is conceptual and intentionally avoids assigning universal percentages
to cost categories.




                                                             7
Happy Bhati                                                                 Reliability and Cost in the Agentic SDLC


9.2 Token consumption is behavior, not just model pricing

The Northeastern study by Wu, Anderson, and Guha is useful because it holds problem difficulty constant while
comparing five models across Python, Java, Rust, and OCaml. Token use varies substantially by language. Trajectory
analysis shows repeated non-compiling attempts in less familiar languages, unnecessary revision of passing solutions,
code-comment planning, distrust of provided tests, and fallback prototyping in Python [11]. This suggests that token
cost is partly a software-engineering quality signal: a poor harness or weak language competence can show up as
wasted inference.
Long-horizon work makes the effect more extreme. SWE-Marathon’s initial rollouts averaged 27.2 million tokens and
had a very long tail [9]. At that scale, retry policy, termination criteria, context compression, verifier design, and
model choice are first-order economic decisions.
The FinOps Foundation’s 2026 report provides an organizational counterpart. It says 98% of surveyed FinOps
practitioners now manage AI spend and names AI cost management as the leading skill need [12]. GitHub’s Copilot
impact dashboard now explicitly connects actual AI credit consumption to cost per developer per month, payroll
percentage, and pull requests per month [27]. These are signs that engineering organizations are starting to demand
unit economics rather than adoption counts.
Gartner forecasts that, under rising token consumption and consumption-based licensing, AI coding cost could
exceed the average developer salary by 2028 [13]. The exact forecast may prove wrong. The more durable point is
that agentic systems introduce a variable cost surface that engineering leaders cannot govern with seat counts alone.


10 The Verification Tax

The cost model suggests a measurable quantity: the Verification Tax. For a set of agent-generated candidate
changes, define:

                                              CCI + Creview + Csecurity + Crework
                                     Vtax =                                       ,                                  (4)
                                                          Cgeneration

where Cgeneration includes model, context, and agent execution cost. The ratio is not expected to be stable across
repositories or task types. That variability is precisely what makes it useful. A high Verification Tax can mean
several different things:

• the task is inherently high risk and deserves expensive assurance;
• the chosen model or context is producing weak candidates;
• the agent is attempting work beyond its current reliability envelope;
• the test/review infrastructure is inefficient or overloaded;
• organizational policy is requiring redundant evidence without reducing risk.

The metric therefore needs diagnosis, not gamification. The goal is not “minimize verification.” A low Verification
Tax can be dangerous if it results from skipping tests or rubber-stamping reviews. The useful objective is to reduce
verification cost for a fixed reliability target, or improve reliability for a fixed assurance budget.
This distinction also helps reconcile apparently conflicting productivity studies. AI can increase coding output in
randomized enterprise settings [3], slow experienced maintainers in a particular mature-repository setting [21], and
still increase commits far more than releases in broad telemetry [4]. Different studies observe different ratios between
generation gain and verification burden.


11 The Agentic Autonomy Budget

Agent autonomy is often discussed as a capability level: can the system run for 30 minutes, eight hours, or several
days? For organizations, autonomy is better treated as a budgeted privilege.
Each task consumes at least three constrained resources:


                                                            8
Happy Bhati                                                                Reliability and Cost in the Agentic SDLC


1. Money / compute budget: model tokens, context, tools, sandbox, CI, and parallelism.
2. Reliability / risk budget: expected failure impact, security exposure, reversibility, blast radius, and error-budget
   consumption.
3. Human-attention budget: clarification, review, escalation, debugging, approval, and incident response.

Figure 4 represents the feasible autonomy region as the intersection of those budgets.

                                                  Reliability / risk
                                                       budget




                                                                    Increase auton-
                                                                    omy only if all
                                                                   three budgets re-
                                            Permitted             main within policy.
                                            autonomy




    Money / compute                                                                            Human-attention
        budget                                                                                    budget

Figure 4: Agentic Autonomy Budget. The largest model or longest possible run is not automatically the best
operating point. Autonomy is constrained jointly by money, reliability, and human review capacity.


A control policy for candidate execution plan p can be written conceptually as:

                           p∗ = arg max [E(Vprod (p)) − λC(p) − µ E(Lfailure (p)) − νH(p)] ,                        (5)
                                      p


subject to mandatory security, policy, and SLO constraints. Vprod is expected production-qualified value, C is
monetary/compute cost, Lfailure is expected failure loss, and H is expected human attention. The weights are
organizational policy, not universal constants.
This framing helps avoid two opposite errors. The first is under-delegation: using an expensive engineer for repetitive,
well-verified work that an agent can safely execute. The second is over-delegation: allowing an agent to consume
millions of tokens and large review queues on tasks with poor verifiability or high blast radius.


12 An Agentic SDLC Control Plane

The findings above point toward a platform problem. If every developer individually chooses models, context size,
agent parallelism, test strategy, and retry depth, then reliability and cost policy is fragmented across IDEs. The
emerging unit of infrastructure is therefore an Agentic SDLC Control Plane: a layer that observes work, assigns
an execution policy, and records the evidence required to qualify the result.
Figure 5 shows the proposed architecture.



                                                           9
Happy Bhati                                                                                             Reliability and Cost in the Agentic SDLC




                             Work intake                             Policy / risk classifier                      Execution planner
                 issue, PR, incident, change request         blast radius, ownership, reversibility        model, context, budget, parallelism




                       Implementation agent        Test / verifier agent        Review agent             Security agent




                                                    CI / build / tests       Security / policy gates     Human escalation / approval




                                     Observability                         Deploy / canary / rollback                Outcome learning
                      tokens, latency, CI, reviewer time, failures          production qualification          PQC, escaped defects, cost, SLOs



Figure 5: Proposed Agentic SDLC Control Plane. Specialized agents are optional components; the core idea is
centralized policy, evidence gates, and feedback linking cost and reliability to future autonomy decisions.


The control plane does not need to replace IDE agents, CI systems, Git hosting, security scanners, or deployment
platforms. It can begin as a policy and telemetry layer around them. The design has six responsibilities:

1. Classify task risk. Estimate consequence, reversibility, data sensitivity, ownership, and affected components.
2. Select an execution plan. Choose model, context strategy, harness, tool permissions, parallelism, and hard
   budget.
3. Require evidence. Bind each risk class to specific tests, static analysis, reviewers, security scans, and deployment
   gates.
4. Stop waste. Terminate or escalate when marginal progress no longer justifies cost or when repeated attempts
   are cycling.
5. Attribute cost. Record model, tool, CI, reviewer, and rework cost at task/PR/team/repository level.
6. Learn from outcomes. Update policies based on PQC rate, escaped defects, rollbacks, review corrections,
   token use, and human escalation.

This is where AI observability becomes an engineering control rather than a dashboard. Prior work on developer-tool
observability argued for joining cost and code-quality signals [2]; the control-plane view extends that principle from
reporting to policy enforcement.


13 What Companies Are Actually Struggling With

The literature and production reports converge on several recurring problems. Table 3 maps each one to a measurable
control.




                                                                             10
Happy Bhati                                                                                 Reliability and Cost in the Agentic SDLC


             Table 3: Recurring agentic-SDLC problems, evidence, and corresponding operating controls.


 Problem              Evidence pattern                           Operational risk                         Control to measure / enforce

 Code generation      Commit      gains     attenuate     to     Review queues, integration backlog,      PQC throughput, review latency, CI
 outruns delivery     project/release gains [4]; DORA            unstable releases                        queue, change-failure/rollback rate
                      throughput vs stability tension [5]

 Benchmarks over-     SWE-bench audit finds task/test            False confidence in agent capability     Private evals, multiple verifiers, pro-
 state certainty      issues and    contamination      [17];                                              duction shadowing, benchmark hy-
                      benchmark-system conflation [18]                                                    giene

 Generated tests      Agent test volume may have marginal        Green CI with shallow assurance          Mutation/property tests, independent
 are weak evidence    outcome effect [24]; filtered tests work                                            oracles, coverage quality, fault detec-
                      better at Meta [22]                                                                 tion

 Multi-agent coor-    CooperBench     shows       coopera-       Conflicting changes, false claims, du-   Structured contracts, shared state,
 dination fails       tion   penalty  and     communica-         plicated work                            ownership, coordinator, merge conflict
                      tion/commitment failures [10]                                                       metrics

 Long-horizon         SWE-Marathon averages 27.2M to-            Runaway inference, verifier exploita-    Token/time caps, progress check-
 agents     waste     kens; poor self-verification and reward    tion, low predictability                 points,      adversarial verifiers,
 budget               hacking [9]                                                                         stop/escalate rules

 Security burden      SWE-chat security findings [8];            Vulnerabilities, secrets, dependency     Mandatory static analysis, secret
 grows with auton-    GitHub automated security validation       risk                                     scans, dependency policy, permission
 omy                  [26]                                                                                sandboxing

 Token cost is hard   Cross-language token variation and         Budget variance, poor ROI attribution    Cost per PQC, tokens per accepted
 to predict           wasteful trajectories [11]; FinOps AI-                                              change, retry rate, model routing
                      spend adoption [12]




13.1 The hidden organizational issue: verification capacity

Companies often budget AI licenses before budgeting the capacity needed to verify the resulting changes. This is
the software equivalent of adding upstream factory machines without increasing inspection, integration, or shipping
capacity. When generation is cheap, the queue can simply move.
The NBER/MIT evidence makes this visible at macro scale [4]; Google code-review data makes the human review
cost concrete [6]; SWE-chat shows that human filtering remains common even in agent-heavy sessions [8]. A likely
enterprise response is not unlimited reviewer hiring. It is a redesign of assurance so low-risk evidence is automated
and high-risk human attention is protected.


13.2 The hidden technical issue: harness quality

The model is only one layer. Tool permissions, repository retrieval, context compression, test selection, sandbox
state, and retry logic can materially change success and cost. SWE-agent’s original results already showed how
much an agent-computer interface matters [15]; newer reliability work makes the dependency chain explicit [25].
Organizations therefore need versioned harnesses and reproducible agent runs, not only a record of which foundation
model was called.


14 Metrics for an Agentic Engineering Organization

The metric set in Table 5 is proposed as a research and operating starting point. No single metric should become a
performance score for individual developers. Most are system-level measures.




                                                                       11
Happy Bhati                                                                        Reliability and Cost in the Agentic SDLC


                  Table 5: Proposed metrics for reliability- and cost-aware Agentic SDLC operations.


 Metric                     Definition / approximation           Why it matters
 PQC rate                   Production-qualified changes /       Separates generation from changes that actually satisfy delivery
                            candidate agent changes              gates.
 PQC per dollar             PQC / total attributable delivery    Normalizes AI cost by qualified output rather than tokens or
                            cost                                 PR count.
 PQC per reviewer-          PQC / human review and escala-       Measures whether agentic throughput is consuming scarce
 hour                       tion time                            expert attention.
 Verification Tax           Assurance + rework cost / gen-       Makes the downstream cost of unreliable generation visible.
                            eration cost
 First-pass    qualifica-   Candidate changes passing all re-    Sensitive to model/harness quality and task selection.
 tion                       quired pre-deploy gates without
                            agent or human rework
 Human        escalation    Tasks requiring clarification,       Measures effective autonomy and where policy boundaries are
 rate                       override, or manual completion /     wrong.
                            agent-started tasks
 Retry / cycle rate         Repeated agent attempts after no     Detects token-burning loops.
                            material verifier improvement
 Escaped-failure rate       Agent-associated changes causing     Connects development automation to production reliability.
                            rollback, incident, security find-
                            ing, or post-release defect
 Cost variance              P95 / median cost for comparable     Agentic economics are dangerous when the tail is unbounded.
                            task class
 Evidence coverage          Fraction of risk-required gates      Prevents silent bypass of review/security policy.
                            with machine-readable evidence
                            attached




These metrics intentionally pull the optimization target toward systems outcomes. GitHub’s 2026 ROI dashboard
is already moving in this direction by connecting AI credits with cost per developer and pull-request output [27].
The next step is to connect cost with qualification and reliability, because a pull request that creates rework is not
equivalent to one that safely ships.


15 Future Horizon: From Supervised Agents to Policy-Bounded Software Factories

Capability is moving quickly enough that date-specific predictions are brittle. Figure 6 therefore uses maturity
horizons rather than years. The labels distinguish documented practice from emerging architecture and open research.




                                                                 12
Happy Bhati                                                                             Reliability and Cost in the Agentic SDLC


                                       H1 - Emerging                   H2 - Experimental
           H0 - Documented                                                                            H3 - Open horizon
                                                                       frontier
           now                         • Risk-tiered agent per-
                                                                                                      • Continuous au-
                                       missions                        • Multi-agent reposi-
           • Copilots + repository                                                                    tonomous SDLC
                                       • Specialized                   tory teams
           agents                                                                                     • Policy-bounded soft-
                                       test/review/security            • Multi-day au-
           • Agent-authored PRs                                                                       ware factories
                                       agents                          tonomous work
           • ML/LLM review as-                                                                        • Formal/learned cor-
                                       • Cost attribution per          • Dynamic verification
           sistance                                                                                   rectness evidence
                                       task / PR                       plans
           • Filtered test genera-                                                                    • Autonomous rollback
                                       • Budget-aware model            • Automated merge for
           tion                                                                                       and repair
                                       routing                         bounded risk
           • Automated security                                                                       • Cross-repository coor-
                                       • Automated evidence            • Self-repair after failed
           validation                                                                                 dinated evolution
                                       bundles                         gates
           • Human merge author-                                                                      • Proven economic +
                                       • Human approval for            • Reliability-aware
           ity                                                                                        reliability control
                                       high-risk changes               agent swarms


                                     increasing delegated execution and verification responsibility


Figure 6: Capability-based horizon for the Agentic SDLC. H0 contains documented practices. H1-H3 are progressively
less mature and should not be read as guaranteed timelines.


15.1 H0: supervised agents with hard CI boundaries

This is already real. Agents can implement features and fixes, generate or improve tests, respond to review feedback,
and open pull requests. GitHub applies automated security validation to agent-generated changes [26]; Google and
Meta have deployed AI-assisted review/test systems [6, 22]. The characteristic architecture is still human-accountable:
the agent proposes and iterates, but production policy remains externally enforced.


15.2 H1: control-plane engineering

The near-term shift is likely to be less visually dramatic than a “fully autonomous developer” and more operationally
important. Organizations will standardize agent harnesses, permission tiers, token budgets, independent verifiers,
model routing, and evidence requirements. AI cost will increasingly be allocated to repositories and business services,
not just centralized tool budgets. The FinOps data and GitHub ROI tooling already point in this direction [12, 27].


15.3 H2: multi-agent and long-horizon execution

Research systems are already testing this frontier, but reliability is not solved. CooperBench shows a coordination
penalty [10]; SWE-Marathon shows low success on ultra-long-horizon tasks, high token use, weak self-verification,
and reward hacking [9]. Those failures are valuable because they identify what a future software factory would
need: durable state, structured coordination, adversarial verification, bounded permissions, progress accounting, and
recovery from partial failure.
METR’s time-horizon work also indicates that agent capability on longer tasks is increasing over time [28]. As
horizon grows, cost and verification become more tightly coupled: a multi-day agent run can create a much larger
change surface and a much larger cost tail than a single patch.


15.4 H3: autonomous software factories remain a systems research problem

The open horizon is not “an LLM writes all the code.” It is a production system that can safely decide, implement,
verify, deploy, observe, rollback, and learn while remaining within organizational policy. That requires reliable
composition of capabilities that are currently evaluated separately.
Harvard’s 2026 work and teaching discussions around correct-by-construction programming capture the assurance
challenge directly: as software is generated and evolved automatically at greater scale, manual review and post-
hoc verification become harder to sustain, motivating stronger correctness-by-construction methods [29]. Boston
University’s 2026 software-engineering-for-AI curriculum similarly emphasizes evaluating AI-generated code for
correctness, security, and long-term maintainability, reflecting the skill shift toward production assurance rather
than prompt fluency alone [30]. These are educational/research-direction signals rather than performance evidence,
but they show the same bottleneck migration appearing in how institutions are training engineers.


                                                                  13
Happy Bhati                                                               Reliability and Cost in the Agentic SDLC


16 Research Agenda

The synthesis leaves a set of concrete research questions that can be evaluated experimentally.


16.1 RQ1: What predicts Production-Qualified Change better than benchmark score?

A useful study would instrument real agentic PRs across multiple repositories and model versions, then test whether
benchmark score, first-pass tests, verifier diversity, reviewer corrections, token trajectory features, or task-risk
classification best predict successful production qualification and post-release stability.


16.2 RQ2: Can verification budgets be allocated adaptively without increasing escaped defects?

Instead of running the same CI/review pipeline for every agent change, a policy could select gates based on task risk
and model/harness confidence. The experiment should hold escaped-defect risk constant and measure cost, latency,
reviewer time, and qualification rate.


16.3 RQ3: When does an additional agent increase reliability rather than correlated error?

Reviewer/test/security agents are appealing, but independence cannot be assumed. Research should measure
correlation between generator and verifier errors across model families, prompts, context sources, and toolchains.
Diverse models may help, but diversity itself consumes budget.


16.4 RQ4: What is the optimal stop rule for long-horizon coding agents?

SWE-Marathon makes the economic problem visible: long trajectories can consume millions of tokens while making
little progress [9]. A stop policy could use verifier improvement, edit churn, repeated failures, context growth, and
estimated remaining work to decide whether to continue, switch models, reset context, or escalate to a human.


16.5 RQ5: How should agentic cost be attributed to delivered value?

FinOps practice is moving toward AI-spend allocation [12], but engineering needs a causal unit. Research should
compare cost per PR, cost per merged PR, cost per PQC, cost per escaped-defect-free service change, and total cost
to deliver. The best metric may differ by product class.


16.6 RQ6: Does AI-generated test code improve real defect detection?

Current evidence suggests that test quantity is not enough [24]. Future work should evaluate mutation score, fault
localization, regression detection, specification coverage, and independence from generator assumptions, ideally on
post-release defects rather than benchmark-only patches.


16.7 RQ7: What organization design converts code acceleration into release acceleration?

The 180%-to-30% attenuation observed by Demirer et al. [4] invites organizational experiments. Candidate
interventions include review-agent triage, platform engineering, smaller change sets, contract testing, architecture
modularity, automated ownership routing, and protected reviewer capacity.


16.8 RQ8: How should software agents coordinate?

CooperBench shows that current agents do not automatically become effective teammates [10]. Research should test
structured protocols, explicit commitments, shared plans, role ownership, transactional state, conflict detection, and
coordinator architectures against free-form chat.



                                                         14
Happy Bhati                                                                Reliability and Cost in the Agentic SDLC


16.9 RQ9: How can reliability evidence survive model and harness changes?

A production organization will continuously swap models and upgrade tools. Evaluation needs to separate model,
harness, environment, retrieval, and policy effects [18, 25]. Versioned evidence and replayable trajectories are
prerequisites for knowing whether a system actually improved.


16.10 RQ10: What skills should senior engineers retain when routine implementation is delegated?

The human role shifts toward decomposition, architecture, risk judgment, verification, and incident reasoning.
Harvard and BU curricula are already emphasizing correctness, evaluation, testing, CI/CD, and production reliability
in AI-assisted software work [29, 30]. Longitudinal studies should test whether heavy delegation erodes the expertise
required to review and recover from agent failures.


17 Implications for Engineering Leaders

The evidence does not support either extreme position: “agents are only toys” or “software engineering is solved.”
The more useful operating stance is to treat agentic development as a new production technology with explicit
constraints.

1. Budget the whole delivery path. Track model and token cost, but also CI, sandbox, reviewer, security,
   rework, and incident cost.
2. Measure shipped reliability, not generated activity. Commits and pull requests are intermediate inventory.
   Use PQC-like metrics, DORA outcomes, escaped defects, and rollback data.
3. Protect scarce review capacity. Automatically verify low-risk properties and reserve expert attention for
   architecture, security, ambiguous requirements, and high-blast-radius changes.
4. Make agent runs reproducible. Version the model, harness, prompts/policy, context construction, tool
   permissions, and verifier. Otherwise failures cannot be diagnosed.
5. Set hard stop rules. Long-horizon agents need token/time ceilings and progress checkpoints. Unlimited
   iteration is not autonomy; it is an unbounded variable bill.
6. Treat tests as evidence, not ceremony. A generated test that asserts the generator’s own assumptions adds
   little independence. Prefer strong oracles, properties, mutation, integration checks, and production signals.
7. Do not assume agent teams coordinate. Add explicit ownership and protocols before multiplying agents.
8. Increase autonomy by change class. Documentation, mechanical refactors, test additions, and low-risk
   dependency updates can have different policies from identity, payments, cryptography, data migration, or
   safety-critical code.

The economic decision should be framed as marginal value. If the next US$10 of model inference avoids an hour of
expert work and does not raise risk, it is likely worthwhile. If the next US$100 of retries creates a larger patch that
still needs the same expert review, the agent has not created equivalent value. A control plane should make that
decision visible.


18 Implications for Researchers and Universities

Software-engineering research is moving from model evaluation toward socio-technical system evaluation. The
MIT/Stanford/Berkeley/Cornell position paper calls for broader SWE tasks and more realistic environments [19];
Stanford’s real-world agent traces provide behavior data beyond benchmarks [8]; MIT/NBER work connects tool
adoption to actual release output [4]; Northeastern demonstrates that token economics depend on language and
agent behavior [11]; Harvard is exploring correctness-by-construction in a world of large-scale generated software
[29]; BU’s curriculum explicitly teaches verification and maintainability of AI-generated code [30].
The educational consequence is that students need more than prompt-writing skill. A durable agentic-software
curriculum should include:


                                                          15
Happy Bhati                                                               Reliability and Cost in the Agentic SDLC


• software architecture and change impact;
• testing theory, property-based testing, mutation, and test-oracle design;
• secure coding, dependency risk, and least-privilege agent tooling;
• CI/CD, observability, SLOs, incident response, and rollback;
• model/harness evaluation and benchmark design;
• cost attribution, token economics, and resource budgets;
• human-agent interaction, review, accountability, and organizational design.

If implementation becomes cheaper, engineering judgment becomes more leveraged. That is a reason to teach
foundations more deeply, not less.


19 Limitations and Responsible Claims

This paper is a structured systems synthesis, not a PRISMA-style exhaustive systematic review. The field is moving
quickly, and some 2026 sources are preprints or organization reports rather than mature peer-reviewed evidence.
Company-reported deployment outcomes may be affected by selection, product design, or incentives that do not
transfer to other organizations. Market forecasts, especially the Gartner cost forecasts, are planning signals rather
than facts about 2028.
Several prominent results describe different populations and should not be directly compared as if they were one
experiment. The 26.08% productivity estimate comes from pooled randomized field experiments with coding
assistance [3]; METR’s 19% slowdown comes from 16 experienced maintainers working in repositories they knew
deeply with early-2025 tools [21]; the MIT/NBER production-hierarchy results come from observational event-study
data on more than 100,000 GitHub developers [4]. Their settings, treatments, outcomes, and causal strength differ.
The proposed constructs - PQC, Verification Tax, Agentic Autonomy Budget, and the Control Plane - are not
claimed as validated standards. They are hypotheses intended to make future studies comparable. A company could
implement them poorly. In particular, PQC must not become an individual developer productivity score; doing so
could encourage gaming and penalize engineers who work on difficult, high-risk systems.
Security and reliability also vary by domain. A coding agent used for internal scripts should not inherit the same
autonomy policy as one modifying authentication, financial transactions, medical devices, or critical infrastructure.
The right operating point depends on reversibility, blast radius, regulation, and human consequence.
Finally, this paper does not assume that rising agent capability inevitably reduces engineering employment. Evidence
such as Demirer et al. points to strong complementarity between AI output and human effort in the production
chain [4]. The composition of work is changing, but labor outcomes depend on product demand, organizational
design, education, and how productivity gains are distributed.


20 Conclusion

The Agentic SDLC is becoming a real operating model, but the hardest problem is moving downstream. Generating
candidate code is no longer the only scarce activity. Reliable software still requires requirements that make sense,
tests that distinguish correct from plausible, reviewers and security systems that catch what the generator misses,
deployment controls that limit blast radius, and production telemetry that reveals whether the change actually
helped.
Recent research makes the bottleneck migration measurable. AI assistance can increase developer output in
randomized enterprise studies. Autonomous agents can dramatically increase commits. Yet those gains attenuate
before releases, and real-world agent traces still show substantial human correction and discarded code. Long-horizon
agents consume enormous inference budgets while struggling with self-verification and occasionally trying to game
their verifiers. Multi-agent coding introduces coordination failures rather than automatic team productivity. Cost
management is therefore becoming inseparable from reliability engineering.
The practical unit of progress should move from code generated to production-qualified value delivered. That is
the reason for PQC, the Verification Tax, and the Agentic Autonomy Budget proposed here. They are not final


                                                         16
Happy Bhati                                                                     Reliability and Cost in the Agentic SDLC


metrics; they are a way to ask better questions. How much trusted change reaches users? What did it cost end to
end? How much expert attention did it consume? What risk did it introduce? When should an agent continue,
switch strategies, or stop?
The likely future is not a single coding model that replaces the SDLC. It is an engineering control system that
coordinates models, tools, tests, security, human expertise, and budgets. Organizations that build that control layer
well may turn agentic speed into dependable software. Organizations that optimize only for generation will discover
that faster code can simply create a faster queue in front of review, testing, and production.


Acknowledgments and Research Integrity Note

This manuscript is an independent research synthesis. No new model benchmark, productivity experiment, cost
measurement, or company deployment result is claimed. Numerical findings and observed effects remain attributed
to the cited researchers and organizations. The terms Agentic SDLC Throughput Paradox, Production-Qualified
Change, Verification Tax, Agentic Autonomy Budget, the control-plane architecture, and the horizon interpretation
are the author’s synthesis of that evidence and are proposed for further validation.


References

 [1] H. Bhati. Agentic AI in the Software Development Lifecycle: Architecture, Empirical Evidence, and the Reshaping of
     Software Engineering. arXiv:2604.26275, 2026. https://arxiv.org/abs/2604.26275.

 [2] H. Bhati and T. Sisodia. AI Observability for Developer Productivity Tools: Bridging Cost Awareness and Code Quality.
     arXiv:2604.17092, 2026. https://arxiv.org/abs/2604.17092.

 [3] K. Z. Cui, M. Demirer, S. Jaffe, L. Musolff, S. Peng, and T. Salz. The Effects of Generative AI on High-Skilled Work: Evi-
     dence from Three Field Experiments with Software Developers. Management Science, 2026. doi:10.1287/mnsc.2025.00535.

 [4] M. Demirer, L. Musolff, and L. Yang. Writing Code vs. Shipping Code: Productivity Effects Across Generations of AI
     Coding Tools. NBER Working Paper 35275, 2026. doi:10.3386/w35275.

 [5] Google Cloud DORA. State of AI-Assisted Software Development 2025. Google Cloud, 2025. https://cloud.google.c
     om/resources/content/2025-dora-ai-assisted-software-development-report.

 [6] A. Frömmgen et al. Resolving Code Review Comments with Machine Learning. In IEEE/ACM International Conference
     on Software Engineering: Software Engineering in Practice (ICSE-SEIP), 2024. https://research.google/pubs/resol
     ving-code-review-comments-with-machine-learning/.

 [7] G. Vijayvergiya et al. AI-Assisted Assessment of Coding Practices in Modern Code Review. Google Research / Auto-
     Commenter, 2024. https://research.google/blog/ai-assisted-assessment-of-coding-practices-in-modern-cod
     e-review/.

 [8] J. Baumann, V. Padmakumar, X. Li, J. Yang, D. Yang, and S. Koyejo. SWE-chat: Coding Agent Interactions From Real
     Users in the Wild. arXiv:2604.20779, 2026. https://arxiv.org/abs/2604.20779.

 [9] R. Desai, J. Hu, J. Cabezas, N. Harsola, P. Shukla, D. Wang, X. Li, et al. SWE-Marathon: Can Agents Autonomously
     Complete Ultra-Long-Horizon Software Work? arXiv:2606.07682, 2026. https://arxiv.org/abs/2606.07682.

[10] A. Khatua, H. Zhu, P. Tran, A. Prabhudesai, F. Sadrieh, J. K. Lieberwirth, X. Yu, et al. CooperBench: Why Coding
     Agents Cannot be Your Teammates Yet. arXiv:2601.13295, 2026. https://arxiv.org/abs/2601.13295.

[11] Z. Wu, C. J. Anderson, and A. Guha. The Best Programming Language for Tokenmaxxing: An Investigation of
     Coding Agent Behavior Across Programming Languages. arXiv:2607.22807, Northeastern University, 2026. https:
     //arxiv.org/abs/2607.22807.

[12] FinOps Foundation. State of FinOps 2026. 2026. https://data.finops.org/.

[13] Gartner. Gartner Predicts AI Coding Costs Will Surpass Average Developer’s Salary by 2028 as Token Consumption Surges.
     June 24, 2026. Market forecast. https://www.gartner.com/en/newsroom/press-releases/2026-06-24-gartner-pre
     dicts-ai-coding-costs-will-surpass-average-developer-salary-by-2028-as-token-consumption-surges.

[14] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan. SWE-bench: Can Language Models
     Resolve Real-World GitHub Issues? In ICLR, 2024. arXiv:2310.06770.


                                                             17
Happy Bhati                                                                  Reliability and Cost in the Agentic SDLC


[15] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and O. Press. SWE-agent: Agent-Computer
     Interfaces Enable Automated Software Engineering. arXiv:2405.15793, 2024.

[16] S. Miserendino, M. Wang, T. Patwardhan, and J. Heidecke. SWE-Lancer: Can Frontier LLMs Earn 1 Million Dollars
     from Real-World Freelance Software Engineering? arXiv:2502.12115, 2025. https://openai.com/index/swe-lancer/.

[17] OpenAI. Why SWE-bench Verified No Longer Measures Frontier Coding Capabilities. February 23, 2026. https:
     //openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/.

[18] M. I. Gorinova, M. Baker, A. Heineike, M. Shaposhnikov, R. Willoughby, and D. Knox. Position: Coding Benchmarks
     Are Misaligned with Agentic Software Engineering. arXiv:2606.17799, 2026.

[19] A. Gu, N. Jain, W.-D. Li, M. Shetty, Y. Shao, Z. Li, D. Yang, K. Ellis, K. Sen, and A. Solar-Lezama. Challenges and
     Paths Towards AI for Software Engineering. arXiv:2503.22625, 2025.

[20] A. Kumar, Y. Bajpai, S. Gulwani, G. Soares, and E. Murphy-Hill. Why AI Agents Still Need You: Findings from
     Developer-Agent Collaborations in the Wild. In IEEE/ACM International Conference on Automated Software Engineering
     (ASE), 2025. Microsoft Research.

[21] J. Becker, N. Rush, E. Barnes, and D. Rein. Measuring the Impact of Early-2025 AI on Experienced Open-Source
     Developer Productivity. arXiv:2507.09089, 2025.

[22] N. Alshahwan, J. Chheda, A. Finogenova, B. Gokkaya, M. Harman, I. Harper, A. Marginean, S. Sengupta, and
     E. Wang. Automated Unit Test Improvement using Large Language Models at Meta. In FSE Companion, 2024.
     doi:10.1145/3663529.3663839.

[23] B. Steenhoek et al. Reinforcement Learning from Automatic Feedback for High-Quality Unit Test Generation. DeepTest
     at ICSE, 2025. Microsoft Research.

[24] Z. Chen, Z. Sun, Y. Shi, C. Peng, X. Gu, D. Lo, and L. Jiang. Rethinking the Value of Agent-Generated Tests for
     LLM-Based Software Engineering Agents. arXiv:2602.07900, 2026.

[25] S. Jarmak. Engineering Reliable Coding Agents: Evaluating and Operating the System Around the Model. arXiv:2608.13867,
     2026.

[26] GitHub. Security Validation for Third-Party Coding Agents. GitHub Changelog, June 9, 2026. https://github.blog/ch
     angelog/2026-06-09-security-validation-for-third-party-coding-agents/.

[27] GitHub. Copilot Impact Dashboard Adds a Return on Investment Section. GitHub Changelog, August 7, 2026. https:
     //github.blog/changelog/2026-08-07-copilot-impact-dashboard-adds-a-return-on-investment-section/.

[28] METR. Measuring AI Ability to Complete Long Tasks / Time Horizon Research, 2026 Update. 2026. https://metr.org
     /research/.

[29] N. Amin. Correct-by-Construction Programming in the Era of Generative AI. Harvard John A. Paulson School of
     Engineering and Applied Sciences seminar, February 12, 2026. https://events.seas.harvard.edu/event/correct-b
     y-construction-programming-in-the-era-of-generative-ai.

[30] Boston University College of Engineering. Master’s in Software Engineering for AI Curriculum: AI/LLM-Aided Software
     Development. 2026. https://www.bu.edu/eng/admissions/graduate/omse-curriculum/.




                                                           18
