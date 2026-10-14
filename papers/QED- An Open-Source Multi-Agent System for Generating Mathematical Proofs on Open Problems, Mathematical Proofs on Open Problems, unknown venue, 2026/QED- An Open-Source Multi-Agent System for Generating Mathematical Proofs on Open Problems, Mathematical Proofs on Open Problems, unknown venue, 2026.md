                                                          QED: An Open-Source Multi-Agent System for Generating
                                                                 Mathematical Proofs on Open Problems


                                                                          Chenyang An 1 Qihao Ye 1 Minghao Pan 2 Jiayun Zhang 3


                                                                    Abstract                                        solutions to Erdős problems (Alexeev et al., 2026b;c) and
                                              We present QED, an open-source multi-agent sys-                       OpenAI’s recent announcement that an internal reason-
                                              tem that turns human-provided research questions                      ing model produced a counterexample to a longstanding
arXiv:2604.24021v4 [cs.AI] 26 Jun 2026




                                              into complete mathematical proofs without fur-                        conjecture in the planar unit-distance problem (OpenAI,
                                              ther human guidance. Its pipeline is designed to                      2026). Google DeepMind’s AI Co-Mathematician further
                                              overcome common failures of single-query proof                        explores human-in-the-loop mathematical research through
                                              generation by separating planning, proving, and                       a Gemini-based, stateful multi-agent workbench (Zheng
                                              verification: a decomposition agent structures the                    et al., 2026). These developments mark a shift from bench-
                                              proof search, prover agents generate candidate                        mark problem solving toward AI-assisted mathematical re-
                                              arguments, and verifier agents check correctness.                     search. However, most high-profile demonstrations still rely
                                              In collaboration with domain experts, we evalu-                       on closed systems, models that are not publicly released, or
                                              ated QED on 18 research-level projects of vary-                       human-directed workflows. This motivates QED, an open-
                                              ing difficulty. QED produced five original works                      source, fully automatic multi-agent proof system evaluated
                                              across algebraic geometry, fluid PDEs, probabil-                      on expert-proposed research problems.
                                              ity, and inverse problems. Expert assessments re-                     Through experiments with frontier coding agents (Claude
                                              gard these works as solid specialized research con-                   Code, Codex, and Gemini CLI) on research-level proof
                                              tributions, with three comparable in difficulty and                   tasks, we observe that naive deployment (single-turn prompt-
                                              scope to work commonly published in established                       ing, unchecked outputs, no structured verification) leads
                                              specialist mathematics venues. QED is released at                     to identifiable failure modes (Section 3). We characterize
                                              https://github.com/proofQED/QED.                                      seven such failure modes and demonstrate that each can be
                                                                                                                    mitigated through a targeted architectural intervention. Each
                                                                                                                    architectural design choice in QED is directly motivated by
                                         1. Introduction                                                            an observed failure mode:
                                         Large language models (LLMs) have demonstrated strong
                                         and rapidly improving performance on mathematical reason-                  1. Context contamination: Prover and verifier share con-
                                         ing, progressing from grade-school word problems (Cobbe                       text, producing circular reasoning → separated prover
                                         et al., 2021) and competition mathematics (Hendrycks et al.,                  and verifier agents.
                                         2021; Trinh et al., 2024; Guo et al., 2025) toward research-
                                                                                                                    2. Citation hallucination: Models fabricate or misstate
                                         level use. Recent reports include individual mathematicians
                                                                                                                       referenced theorems → structured citation verification
                                         using LLM chatbots to obtain core ideas for ongoing re-
                                                                                                                       with exact-statement matching.
                                         search (Gowers, 2026; Alexeev et al., 2026a), as well as
                                         large-scale systems such as Aletheia (Feng et al., 2026),                  3. Misallocation of proof effort: Models skip the hardest
                                         which have contributed to mathematical discovery with vary-                   parts of proofs while continuing to work on easy steps
                                         ing degrees of human guidance. Fully automatic proof gen-                     → mandatory <key-original-step> tagging with
                                         eration from only a human-provided problem statement                          verifier enforcement.
                                         remains rarer. Notable examples include Aletheia’s au-
                                         tonomous results, including (Feng, 2026), OpenAI’s short                   4. Unstable proof plans: Models abandon strategies mid-
                                            1                                                                          proof on hard problems → decomposition mode separat-
                                              University of California, San Diego, La Jolla, USA 2 California
                                         Institute of Technology, Pasadena, USA 3 Amazon Web Services
                                                                                                                       ing proof planning from proof execution.
                                         (work done outside of Amazon). Correspondence to: Chenyang
                                         An <c5an@ucsd.edu>.                                                        5. Unfocused verification: Models dilute attention across
                                                                                                                       heterogeneous checks → two-stage verification (struc-
                                         Preprint. June 30, 2026.                                                      tural then detailed).

                                                                                                                1
             QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

6. Problem modification: Models alter the problem state-               ity, algebraic geometry, fluid PDEs, and inverse problems,
   ment to reduce difficulty → problem-statement integrity             with all resulting proofs verified and validated by the rel-
   checking (word-by-word comparison).                                 evant experts. Expert assessments further indicate that
                                                                       three of these results are comparable in difficulty and
7. Single-model bottleneck: Relying on one model makes
                                                                       scope to work published in established specialist math-
   the system vulnerable to that model’s blind spots →
                                                                       ematics journals. We also report selected unsuccessful
   multi-model parallel proving and brainstorm mode.
                                                                       cases, providing direct evidence of both the capabilities
                                                                       and current limitations of LLMs when embedded in a
Through our collaboration with seven domain experts, we                well-designed multi-agent pipeline for open mathematical
asked experts to propose research projects for which, to the           research problems.
best of their knowledge, no proof or complete solution was
known, and whose successful resolution would constitute a
publishable contribution. We collected 18 research projects          2. Related Work
and tested QED on them. QED successfully produced origi-             LLM mathematical reasoning. The rapid improvement
nal, nontrivial, and complete solutions to 5 research projects       of LLMs on open-source mathematical benchmarks, from
in algebraic geometry, fluid PDE, probability, and inverse           GSM8K (Cobbe et al., 2021) and MATH (Hendrycks et al.,
problems. QED was operated fully automatically, and no ex-           2021) to competition-level problems (Trinh et al., 2024), has
pert guidance was provided during the runs. Each proof was           made those benchmarks unable to measure SOTA models’
independently verified by the contributing domain experts,           reasoning capabilities. Chain-of-thought prompting (Wei
who confirmed the results to be original (not previously             et al., 2023), self-consistency (Wang et al., 2023), training
known) and nontrivial (requiring genuine mathematical in-            models on better data (An et al., 2024; 2025a), and reinforce-
sight). Moreover, the observed false positive rate of the QED        ment learning from human feedback or reward models (Guo
verifier with Codex GPT-5.5 in our experiment was 0 out              et al., 2025; An et al., 2025b) have all contributed to this
of 17. In particular, across 214 proof candidates produced           progress. However, benchmark performance does not di-
by the QED prover using Codex GPT-5.5 and evaluated by               rectly imply the ability to produce original research-level
the QED verifier under the same configuration, 17 candi-             proofs, as benchmarks consist of problems with known solu-
dates were accepted by the verifier. Every verifier-accepted         tions. To address the saturation of open benchmarks, more
candidate was subsequently accepted by the corresponding             recent efforts have introduced harder, often closed-source
domain expert, yielding an observed false-positive rate of 0         evaluations such as Frontier Math and the Humanity’s Last
in this setting.                                                     Exam benchmark, which aim to probe the limits of current
Links to the problem statements, proofs, and expert com-             models on substantially more challenging and less mem-
mentary for the five research projects that QED successfully         orized problems (Phan et al., 2025; Glazer et al., 2025).
solved can be found in the appendix A.                               However, these benchmarks are not publicly available, lim-
                                                                     iting reproducibility and systematic analysis.
Note that we do not report full details of all the unsuccess-
ful cases for QED because some of the research problems
remain active, with human mathematicians still working on            Agent architectures for coding and scientific discovery.
them. Many of the unsuccessful cases are longstanding open           Recent multi-agent LLM systems increasingly move beyond
problems that are widely regarded as genuinely difficult, and        simple chat-based collaboration toward structured agent ar-
we share some of them in the appendix B.                             chitectures for complex technical and scientific workflows.
                                                                     In software engineering, systems such as MAAD (Li et al.,
In summary, our contributions are as follows:                        2025) and ALMAS (Tawosi et al., 2025) decompose de-
                                                                     velopment into specialized roles and stages, coordinating
• We give an empirical characterization of seven failure             agents for architecture design, implementation, validation,
  modes of frontier LLMs on research-level proof tasks               and integration. In scientific discovery, systems such as
  (Section 3).                                                       MatSciAgent (Chaudhari et al., 2026), Robin (Ghareeb
                                                                     et al., 2025), DORA AI Scientist (Naumov et al., 2025), and
• We design and release QED, an open-source multi-agent
                                                                     MACC (Oyama et al., 2026) organize agents around domain-
  proof system that fully automates the theorem-proving
                                                                     specific scientific workflows, including hypothesis gener-
  process given human-provided problem statements, with
                                                                     ation, literature analysis, experiment design, tool use, and
  each architectural decision driven by a specific failure
                                                                     report generation. More broadly, CORAL (Qu et al., 2026)
  mode (Section 4).
                                                                     studies autonomous multi-agent evolution for open-ended
• Through collaborations with domain experts, we show                discovery, emphasizing sustained search and knowledge ac-
  that QED independently produced original, nontrivial               cumulation across interacting agents (Qu et al., 2026). QED
  proofs for five open research projects across probabil-            differs from these systems in its specific focus on research-

                                                                 2
             QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

level mathematical proof, its failure-mode-driven design,            the development of QED.
and its multi-stage verification pipeline tailored to math-
ematical reasoning. In particular, QED explicitly targets            3.1. Failure Mode 1: Context Contamination
challenges that are largely absent or less central in prior
agent systems: rigorous citation grounding, preservation of          When a single LLM session serves as both prover and ver-
problem-statement integrity, and formal consistency across           ifier, the verification step is contaminated by the prover’s
a subgoal tree. Rather than relying only on role specializa-         reasoning context. The model “remembers” its own proof
tion, conversational refinement, or experimental feedback,           strategy and is predisposed to accept its own arguments,
QED introduces structured verification stages that enforce           even when they contain errors. This produces a false sense
correctness at each level of the proof hierarchy, aligning the       of correctness: the model generates a flawed proof, then ver-
agent architecture with the logical and compositional nature         ifies it as correct because both steps share the same internal
of mathematical proof.                                               state.
                                                                     In our earliest attempts, we used the same LLM model to
AI and open problems. Recent work has explored                       both generate and verify proofs, although in separate calls.
whether AI systems can contribute to open mathemati-                 This avoided literal context leakage, but still suffered from
cal questions. FunSearch (Romera-Paredes et al., 2024)               same-model self-verification bias: the verifier shared the
used LLMs to discover new constructions in extremal com-             prover’s reasoning tendencies and often failed to identify
binatorics. Aletheia (Feng et al., 2026) demonstrated a              subtle flaws in proofs generated by that same model. This
closed-source agent that made research progress on open              led to more frequent false positives and motivated our later
problems across multiple mathematical domains. OpenAI                design with a more independent verification stage.
has also reported progress on Erdős-style open problems:
two manuscripts present eight short proofs across combi-             3.2. Failure Mode 2: Citation Hallucination
natorics, number theory, and probability, with the authors
                                                                     LLMs routinely fabricate mathematical citations. They in-
attributing the proofs to internal OpenAI models and de-
                                                                     vent theorem numbers, attribute results to wrong sources,
scribing the human role as digesting and polishing the write-
                                                                     fabricate URLs, or cite statements that do not appear in the
ups (Alexeev et al., 2026b;c). Its recent planar unit-distance
                                                                     referenced source. This is particularly dangerous in proof
result similarly reports a counterexample to a longstanding
                                                                     generation because a proof that relies on a hallucinated
conjecture produced by an internal reasoning model (Ope-
                                                                     lemma may appear logically sound while being built on a
nAI, 2026). Google DeepMind’s AI Co-Mathematician
                                                                     nonexistent foundation.
is a limited-release Gemini-based workbench in which a
project coordinator agent manages a stateful mathematical            In our experiments, citation hallucination was not a rare
workspace and delegates tasks across parallel workstreams            edge case. When no dedicated citation verifier was used, we
and specialized agents; the system is designed to support            observed that a high percentage of the citations produced
open-ended research workflows such as ideation, literature           by strong models such as Claude 4.6 Opus and GPT-5.5 in
search, computational exploration, theorem proving, and              research-level proofs contained some form of hallucination
theory building, and reports early tests in which it helped          or grounding error. These errors included fabricated theo-
researchers solve open problems, identify new directions,            rem statements, incorrect attributions, nonexistent URLs,
and uncover overlooked references (Zheng et al., 2026).              and citations to sources that did not actually contain the
However, these results are either produced by closed-source          claimed statement. This made citation verification essential:
agent or have faced scrutiny: some attributed solutions to           without it, a proof could appear mathematically coherent
open problems (e.g., those associated with Erdős) were ar-          while relying on unsupported or nonexistent lemmas.
gued to be rediscoveries, and construction-focused results
do not constitute proofs in the traditional sense. QED con-          3.3. Failure Mode 3: Misallocation of Proof Effort
tributes to narrowing this gap as an open-source system
producing natural-language proofs for genuinely open re-             In our experiments, we found that LLMs tend to evade
search problems, verified as original by domain experts.             the core mathematical difficulties: while they often recog-
                                                                     nize what needs to be proven, they rely on vague language
                                                                     to bypass the rigorous execution required for genuine in-
3. Why LLMs Fail at Real Proofs                                      sight, resorting to phrases like “clearly, X holds” or “it is
Before introducing the architecture of QED, we charac-               straightforward to verify” when the claim is neither clear nor
terize the failure modes that motivated its design. These            straightforward. Meanwhile, they overinvest attention in el-
observations emerge from experimentation with frontier               ementary components, providing excessive detail to reprove
coding agents (Claude Code, Codex and Gemini CLI) on                 well-established lemmas or justify routine steps; by exhaust-
research-level mathematical problems, prior to and during            ing their focus on these trivialities, they leave the primary,

                                                                 3
              QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

novel complexities of the problem largely underexplored.              4. QED System Design
                                                                      QED is a multi-stage, multi-agent pipeline for mathematical
3.4. Failure Mode 4: Unstable Proof Plans
                                                                      proof generation. Its architecture is directly motivated by the
In our experiments, we found that LLMs typically form a               failure modes identified in Section 3: each design decision
proof plan before executing it, but they give up on plans             addresses a specific observed weakness. Figure 1 provides
too easily. When a model encounters a difficult step during           an overview. We describe QED’s two proof modes (simple
execution, it tends to abandon the current plan and switch to         and decomposition), its verification pipeline, and its multi-
an entirely different strategy rather than pushing through the        model capabilities.
difficulty. Over multiple iterations, this produces a random
walk through proof space rather than systematic progress:             4.1. Simple Mode
the model cycles through superficially different plans with-
out ever committing to one long enough to resolve its hard            QED simple mode (as shown in Fig 1) implements a three-
steps. The model fails to distinguish between “this approach          stage pipeline, where Stage 0 performs literature survey
has a fixable error in execution” and “this approach is fun-          and Stage 2 summarizes the entire proof effort. Stage 1
damentally flawed and needs a new plan.”                              is essentially an iterative search–verify loop, suitable for
                                                                      problems that can be solved through progressive refinement.
3.5. Failure Mode 5: Unfocused Verification
                                                                      Per-round flow in stage 1 In each round r                   =
When a single verification agent is tasked with checking              1, . . . , Rmax , the system does the following steps:
everything—problem-statement integrity, citations, logical
structure, and step-by-step correctness—it tends to dilute its        1. Proof search: One or more proof agents write a complete
attention across all aspects and miss critical issues. This has          proof, informed by the literature survey. For rounds
been identified repeatedly in our experiments.                           r > 1, the prover receives the previous round’s proof and
                                                                         its verification results, so it can learn from past failures
3.6. Failure Mode 6: Problem Modification                                and attempt different strategies.

We also observed a form of reward hacking in proof gen-               2. Verification: Each proof is independently checked by
eration: models sometimes subtly changed the problem                     structural verification (Phases 1–5: problem-statement
being solved while still producing a plausible proof. For                integrity, completeness, citations, subgoal tree structure,
example, the model might change a quantifier, strengthen                 and any human-specified rules) followed by detailed ver-
an assumption, weaken the conclusion, restrict the domain,               ification (Phase 6: step-by-step logical and mathematical
or prove only a special case while presenting it as the origi-           checking).
nal theorem. This is dangerous because the resulting proof            3. Selection: When multiple proofs are generated, a selec-
may be mathematically correct, but for the wrong prob-                   tor agent evaluates all proof–verification pairs and selects
lem. In this sense, the model optimizes for the verifier’s               the best candidate.
proxy objective—producing something that looks like a
                                                                      4. Verdict: A verdict agent reads the selected proof and its
valid proof—rather than satisfying the true objective of
                                                                         verification reports and decides D ONE (proof accepted)
proving the exact user-specified statement. This is closely
                                                                         or C ONTINUE (next round). Note that the verdict agent
related to reward hacking or specification gaming, where
                                                                         does not read the proof or generate any new verification
a model exploits imperfections in the evaluation criterion
                                                                         reports.
to achieve a high score without accomplishing the intended
task (Bondarenko et al., 2025; Wang et al., 2026).                    Addressing Failure Mode 1 (context contamination).
                                                                      The proof agent and verification agents are separate model
3.7. Failure Mode 7: Single-Model Bottleneck                          invocations with no shared context. The verifier sees only
Different LLMs have different mathematical strengths and              the proof document and the original problem—not the
blind spots. A problem that one model cannot solve may                prover’s reasoning process or intermediate attempts.
be accessible to another. Relying on a single model means
the system inherits all of that model’s weaknesses, with no           Addressing Failure Mode 7 (single-model bottleneck).
mechanism for complementary coverage.                                 When multi-model mode is enabled, multiple coding agents
                                                                      (e.g., Claude Code, Codex, Gemini CLI) generate proofs
                                                                      in parallel. Each proof is then independently verified by
                                                                      one or more verification agents, which may themselves
                                                                      use different models. A selector agent evaluates all proof–
                                                                      verification pairs and selects the best candidate. An optional

                                                                  4
               QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

                                                                                            Stage 1: Proof Loop



                     Stage 0                           Prover 1                                                                                        Stage 2


                                                                                                                                             D ONE
           Problem             Lit. Survey             Prover 2                   SV              DV              Selector         Verdict           Summary
                                                             ..
                                                              .
                                                       Prover n

                                                                                         C ONTINUE
                                      SV = Structural Verifier, DV = Detailed Verifier


Figure 1. QED system architecture. Stage 0 surveys the literature. Stage 1 iterates a proof loop: multiple models generate proofs in
parallel; the structural verifier (SV) and detailed verifier (DV) each independently produce n × m verification reports (m per proof),
where n is the number of provers and m is the number of verification agents for each proof. At present, both n and m are at most
three, corresponding to Claude Code, Codex, and Gemini CLI. A selector reads all verification results and picks the best proof with
its verification result; and a verdict agent makes the final accept/continue decision based on the verification result of the selected proof.
Stage 2 summarizes the entire proof effort. The prover can also access the internet when additional literature review is required.


brainstorm step allows multiple models to propose proof                                        a different corrective action:
strategies before the main search begins.
                                                                                                  Decision                   Diagnosis               Action
4.2. Decomposition Mode                                                                           R EVISE P ROOF             Execution errors,       Re-prove with
                                                                                                                             plan is sound           same plan
For harder problems, QED offers a decomposition mode                                              R EVISE P LAN              Structural gaps         Modify plan,
that separates proof planning from proof execution, directly                                                                 in the plan             then re-prove
addressing Failure Mode 4 (unstable proof plans).                                                 R EWRITE                   Fundamental             New decomposition
                                                                                                                             approach is flawed      from scratch
Agents. Decomposition mode employs six specialized                                             Table 1. Three-level retry hierarchy in decomposition mode.
agents:                                                                                        The regulator distinguishes execution errors from plan-level and
                                                                                               strategy-level failures. The decomposer-regulator design addresses
                                                                                               Failure Mode 4.
1. Decomposer: Creates a structured proof plan—a di-
   rected acyclic graph (DAG) of intermediate mathemat-
   ical claims with explicit dependencies. It has access to                                    Each level has a configurable limit (e.g., 3 proof attempts
   previous plans and regulator output that identifies the fail-                               per plan revision, 2 plan revisions per decomposition, 3 total
   ure reasons for the previous plans, allowing it to avoid                                    decompositions), preventing infinite loops while allowing
   repeating them or to revise them.                                                           systematic exploration.
2. Single prover: Writes a complete proof following the
   decomposer’s plan. When the regulator decides R E -                                         Proof plan structure. The decomposer outputs a YAML-
   VISE P ROOF, the prover receives the previous proof and                                     formatted plan where each step is a precise quantitative
   its verification feedback to guide revision.                                                mathematical statement (not a vague description like “show
                                                                                               the function grows slowly”). Each step specifies its depen-
3. Structural verifier: Phases 1–5 are the same as in the
                                                                                               dencies, difficulty level, and whether it is a key step—the
   simple mode, except for an added criterion that checks
                                                                                               most novel and difficult part of the proof. The plan also
   whether the proof produced by the prover follows the
                                                                                               includes cited sources and a mandatory self-critique section.
   decomposition plan.
4. Detailed verifier: Phase 6 (same as the verification step                                   4.3. Verification Pipeline
   in simple mode).
                                                                                               QED’s verification pipeline consists of six phases, split into
5. Regulator: Analyzes verification failures and decides                                       two stages. This two-stage design addresses Failure Mode 5
   the next action.                                                                            (unfocused verification) by allowing each stage to focus on
6. Verdict: Final accept/reject decision, same as the verdict                                  a specific class of checks.
   agent in the simple mode.
                                                                                               Stage A: Structural Verification (Phases 1–5). Struc-
Three-level retry hierarchy. The regulator’s key innova-                                       tural verification checks the proof’s foundations before in-
tion is distinguishing three types of failure, each triggering                                 vesting in expensive step-by-step analysis:

                                                                                           5
                QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

                            Decomposer                                   Stage B: Detailed Verification (Phase 6). Phase 6 runs
                                    plan (YAML)
                                                                         only if Phases 1–5 pass. It performs step-by-step logical
                                                                         and mathematical checking:
                            Single Prover

                                    proof.md                             • For each assertion: state the claim, quote the justification,
                          Structural Verifier                              list dependencies, check logical validity, verify computa-
                             (Phases 1–5)
                                                                           tions, and assign a verdict (Pass/Fail/Uncertain).

                          Detailed Verifier                              • Cross-reference with citation verdicts from Phase 3.
                             (Phase 6)
                                                                         • Verify all subgoal resolutions point to specific, real parts
                                    feedback
                                                                           of the proof.
                              Regulator                     DONE
                                                                         • Analyze <key-original-step> tags (addresses
     R EWRITE                                                              Failure Mode 3): check that every tagged step is gen-
                R EVISE                           R EVISE                  uinely nontrivial and maximally detailed, and that every
                  P LAN       Decision            P ROOF
                                                                           nontrivial step is properly tagged.

Figure 2. Decomposition mode flow. The regulator analyzes                4.4. Prover Output Format Enforcement
verification failures and selects one of three corrective actions:
R EVISE P ROOF revises the proof without changing the plan,              In both simple mode and decomposition mode, QED im-
R EVISE P LAN modifies the existing decomposition plan, and              poses a structured output format on the prover to address
R EWRITE works on a new decomposition entirely. The decom-               multiple failure modes simultaneously. To address Failure
poser has access to previous plans to avoid repetition or make           Mode 2 (citation hallucination), the prover must use a stan-
revisions.
                                                                         dardized citation format: every cited result must include
                                                                         the exact theorem statement, the source (with title, authors,
                                                                         and location), and a verification that all conditions of the
• Phase 1: Problem-statement integrity (addresses Fail-
                                                                         cited result are satisfied in the current context. To address
  ure Mode 6). The verifier reads the original problem ver-
                                                                         Failure Mode 3, QED requires the prover to wrap every non-
  batim and compares it word-by-word against the claim the
                                                                         trivial original step with <key-original-step> tags.
  proof actually proves. Any discrepancy—changed quan-
                                                                         Content inside these tags must be “maximally detailed”—
  tifiers, strengthened hypotheses, weakened conclusions,
                                                                         every sub-step, every bound, every case made explicit. The
  restricted domains, swapped conclusions and hypotheses—
                                                                         verifier then checks:
  is an automatic failure.

• Phase 2: Completeness and originality. Checks that                     • Every nontrivial proof has at least one key-original-step.
  all parts of the problem are addressed and that the proof              • Tagged content contains no vague language (“clearly,”
  contains genuine argument (not just a literature survey or               “obviously,” “straightforward”).
  proof sketch).
                                                                         • Untagged nontrivial steps are flagged as potential hidden
• Phase 3: Citation verification (addresses Failure Mode                   weaknesses.
  2). For every citation the verifier independently checks:              • Routine steps inflated with key-original tags are flagged.
  (a) the source URL resolves, (b) title and authors match,
  (c) the exact statement exists at the specified location,              This creates a forcing function: the prover must identify the
  (d) the cited statement matches the source verbatim, and               hardest parts of the proof and provide complete detail for
  (e) the proof correctly applies the cited result with all              exactly those parts.
  conditions satisfied.

• Phase 4: Subgoal tree validation. The proof must de-                   4.5. Optional Human-in-the-Loop Steering
  clare its logical architecture as a tree of subgoals rooted at         While QED runs fully automatically by default, it supports
  the main claim. The verifier checks well-formedness (no                optional human steering between rounds. Domain experts
  orphans, no cycles), validity of each reduction, and com-              can provide:
  pleteness (every subgoal resolved, every cited theorem’s
  conditions accounted for as explicit subgoals).                        • Global proof hints: Persistent guidance across all rounds
                                                                           (e.g., “try Fourier-analytic methods”).
• Phase 5: Human-specified rules. If domain experts have
  provided additional verification criteria, these are checked           • Additional verification rules: Extra criteria the verifier
  as hard requirements.                                                    should enforce.

                                                                     6
             QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

These are read from designated files before each new round           also do not include full ablation studies over all projects
begins. In our evaluation on open research problems (Sec-            due to two considerations. First, no benchmark exists for
tion 5), this feature was not used—all results were obtained         open research problems. By definition, these problems lack
without expert guidance.                                             known solutions against which to measure performance.
                                                                     Second, verifying the correctness and originality of a proof
4.6. Standalone Proof Verifier                                       requires substantial effort from domain experts. Running
                                                                     QED with each component disabled would multiply the
In addition to the full proof-generation pipeline, QED pro-          number of proofs requiring expert review, imposing an im-
vides a standalone proof verifier that takes any problem–            practical burden on the mathematicians who volunteered
proof pair and produces a structured verification report. This       their time. Instead, Section 6 reports targeted diagnostic ab-
tool is designed for users who already have a proof (whether         lations on the two probability cases where repeated system
human-written or AI-generated) and want to check its cor-            variants could be compared without requiring broad expert
rectness without running the full proof-search loop.                 re-review. In practice, for each non-probability problem,
The standalone verifier uses a difficulty-adaptive architec-         we asked the corresponding expert to assess the correctness
ture with up to three agents:                                        of QED’s proof at most once; if the proof was found to be
                                                                     incorrect, we did not repeatedly revise and resubmit proofs
1. Difficulty judge. A judge agent classifies the problem            for the same problem, in order to respect the experts’ limited
   as Easy or Hard. For easy problems, the judge performs            availability and avoid overburdening them.
   a complete streamlined verification in a single pass and
   the pipeline terminates. For hard problems, the judge             5.1. Experiment Setup
   defers to two specialized verification agents.                    Research Projects. 18 research projects were contributed
2. Structural verifier (hard only). Checks problem-proof             by 7 (groups of) experts. Each project may contain 1 or
   alignment, completeness and originality, and the proof’s          more open problems.
   logical architecture.
                                                                     • Projects 1–10: Contributed by a domain expert in prob-
3. Detailed verifier (hard only, after structural pass). Per-          ability. Some of the problems in the projects arose from
   forms step-by-step logical verification, mathematical cor-          domain expert’s active research, and some of them are
   rectness checks, rigor analysis, and coverage checks.               well-known, genuinely difficult open problems in the area.
   Skipped if structural verification fails.
                                                                     • Projects 11–12: Contributed by a domain expert in op-
4.7. Automatic Resume                                                  erator algebra. Both of them are well-known, genuinely
                                                                       difficult open problems in the area.
QED supports automatic resume from any point in the
pipeline. If the process exits for any reason—model API              • Projects 13–14: Contributed by a domain expert in alge-
failures, network interruptions, machine restarts, or resource         braic geometry. All problems in the projects arose from
limits—QED detects the exact stage of progress by scan-                domain expert’s active research.
ning the output directory structure and resumes from where           • Projects 15–17: Contributed by a domain expert in fluid
it left off. This applies to both simple and decomposition             PDE. All problems in the projects arose from domain
modes: in simple mode, QED can resume at any sub-stage                 expert’s active research.
within any round; in decomposition mode, it restores the
full attempt–revision–proof hierarchy and continues from             • Project 18: Contributed by a group of domain experts
the last incomplete step. This is essential for research-level         in inverse problems, concerning Carleman weight func-
proof tasks, which may run for extended periods across                 tions for PDEs. The statement and the proof are withheld
many rounds.                                                           currently.

                                                                     The 5 research projects that QED successfully solved inde-
5. Experiments
                                                                     pendently are documented in Appendices A.1–A.5. They
We evaluate QED on 18 open research projects contributed             correspond respectively to Project 6 (probability), Project 8
by domain experts, with no proof known for any of the                (probability), Project 13 (algebraic geometry), Project 15
problems in those projects. Our evaluation takes the form            (fluid PDE), and Project 18 (inverse problems). Selected
of case studies rather than benchmark experiments. We                unsuccessful projects are presented in Appendix B.
do not report full details of all the unsuccessful cases for
QED because some of the research problems remain ac-                 Configuration and Costs. The model configurations dif-
tive, with human mathematicians still working on them. We            fered by projects:

                                                                 7
               QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

• A.1 Decomposition mode. All agents use Codex with                 Verifier Reliability In the QED pipeline, each proof can-
  GPT-5.5-pro, thinking level xhigh. This case costs around         didate generated by the QED prover is checked by the QED
  1000 US dollars.                                                  verifier. We analyze the subset of QED runs in which the
                                                                    verifier used the Codex GPT-5.5 configuration. This sub-
• A.2–A.3 Decomposition mode. All agents use Codex                  set contains 214 proof candidates spanning all 18 research
  with GPT-5.5, thinking level xhigh. A.2 costs around 200          projects considered in this work.
  US dollars. A.3 costs around 100 US dollars.
                                                                    Among these 214 proof candidates verified by the QED ver-
• A.4 There are three open research problems in this case.          ifier with Codex GPT-5.5, 17 were accepted by the verifier.
  The first problem is completed with simple mode, with all         Each of these 17 verifier-accepted proofs was subsequently
  agents using Codex with GPT-5.4, thinking level xhigh.            reviewed and accepted by the corresponding domain expert.
  The second and third problems are completed with decom-           Thus, within the proof candidates checked under this verifier
  position mode, with all agents using Codex with GPT-5.5,          configuration, we observed no false positives: there was no
  thinking level xhigh. This case costs around 600 US dol-          case in which the verifier accepted a proof candidate that
  lars.                                                             was later rejected by expert review.

• A.5 Simple mode. Literature survey, proof search, all
  verifications and verdict use Anthropic Claude Opus 4.6,
                                                                    6. Discussion
  brainstorm is not enabled. This case costs around 50 US           Beyond benchmarks. These results demonstrate a ca-
  dollars.                                                          pability qualitatively different from the benchmark perfor-
                                                                    mance discussed in Section 2. Solving a competition prob-
We report the retry details, including the number of plan           lem with a known solution is fundamentally different from
rewrites, plan revisions, and proof revisions, in Appendix C.       producing an original proof for a problem whose answer is
                                                                    not known in advance, which is why the evaluation in Sec-
                                                                    tion 5 is organized as expert-assessed research case studies
Independence. The system received only the problem                  rather than as benchmark scoring.
statements and configuration parameters; no domain-
specific guidance or expert feedback was provided.
                                                                    Originality. A central concern about AI-generated mathe-
5.2. Results                                                        matics is whether the resulting proofs are genuinely original.
                                                                    We argue that the proofs produced by QED for the five
Expert Assessment of Significance To assess the math-               research projects above satisfy this criterion. The prob-
ematical significance of the results produced by QED, we            lems addressed by QED were open research questions with
asked the collaborating domain experts to evaluate the com-         no known solutions, as described in Section 5; they were
pleted solutions in the context of their respective fields.         newly proposed by domain experts in the course of their
The experts confirmed that the resulting proofs are correct,        own recent research. QED produced all proofs without
original, and nontrivial. They further characterized the sig-       domain-expert guidance during the proof-generation pro-
nificance of the individual contributions as follows: A.1 was       cess, consistent with the independence protocol in Section 5
described as comparable to work published in the Electronic         and the unused human-steering option in Section 4.5. For
Journal of Probability or the Proceedings of the American           Appendices A.1–A.5, the corresponding experts character-
Mathematical Society; A.2 was characterized as PhD-level            ized QED’s contributions as original.
work with nontrivial technical depth; the proof in A.3 was
described as original, nontrivial, elementary, elegant, and
                                                                    Targeted ablation studies. Full ablations are impracti-
“moderately difficult”; A.4 was described as comparable to
                                                                    cal for the reasons described in Section 5: each candidate
work published in venues such as the Journal of Differen-
                                                                    research proof requires time-intensive expert review. We
tial Equations or SIAM Journal on Mathematical Analysis;
                                                                    therefore performed targeted qualitative ablations on the
and A.5 was characterized as comparable to work published
                                                                    two probability cases in Appendices A.1 and A.2. These
in journals such as the Journal of Mathematical Analysis
                                                                    two cases were selected because both were solved success-
and Applications. These assessments suggest that QED is
                                                                    fully by QED and expose the failure modes that motivated
not merely generating formal exercises or routine deriva-
                                                                    the system design in Sections 3 and 4. As a single-query
tions, but is capable of producing solutions in diverse math
                                                                    baseline, we submitted each problem to GPT-5.5 Pro in
domains, whose mathematical content reaches the level of
                                                                    five independent attempts. None of the ten attempts pro-
publishable research contributions.
                                                                    duced a complete proof; all omitted essential steps. We then
See appendix A for the statements, proof links, and full            inspected variants in which specific QED constraints were
expert comments.                                                    removed. The goal of these ablations is not to estimate a suc-

                                                                8
             QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

cess rate, but to test whether individual system components           rather than statistically powered. Nevertheless, they show
prevent the concrete failure modes identified in Sections 3.2         that the tested components address distinct, directly ob-
to 3.4.                                                               served failure modes from Section 3: citation grounding,
                                                                      verification of external dependencies, allocation of effort to
• Standardized citation format. Without the format re-                key original steps, and stability of the proof plan.
  quired in Section 4.4, the prover cited results without
  stating them precisely. In some attempts, it misstated a            7. Conclusion
  cited theorem, making the claimed application invalid.
  In others, the application was correct but insufficiently           We presented QED, an open-source multi-agent system that
  explained, falling short of mathematical writing standards          fully automates theorem proving given human-provided
  and making the argument difficult for human experts to              questions. Through collaborations with domain experts,
  verify. This supports the claim from Sections 3.2 and 4.4           QED produced original and nontrivial proofs for five re-
  that citation structure is not merely cosmetic: it forces           search projects across probability, algebraic geometry, fluid
  cited results to be explicit enough for both verifier check-        PDEs, and inverse problems, with three of them comparable
  ing and expert review.                                              in difficulty and scope to work commonly published in es-
                                                                      tablished specialist mathematics venues. In each successful
• Citation verification (Phase 3). Without independent
                                                                      case, the system received only the problem statement and
  citation verification, one attempt used a theorem found
                                                                      configuration parameters, ran without human guidance dur-
  only in unpublished research notes. As a result, a key step
                                                                      ing proof generation, and produced outputs subsequently
  in the proof relied on a less trustworthy source that readers
                                                                      validated by the relevant experts. These results provide evi-
  could not independently verify. This supports the role of
                                                                      dence that QED has a meaningful success rate for producing
  Phase 3 in Section 4.3 and directly addresses the citation
                                                                      original and nontrivial proofs in mathematical research.
  hallucination failure mode in Section 3.2: the verifier must
  check not only whether a statement is mathematically
  plausible, but whether the cited source is public, precise,         Acknowledgments
  and usable in the proof.
                                                                      We thank Xiaoqian Xu (Assistant Professor of Mathemat-
• <key-original-step> tags. Both probability ques-                    ics at Duke Kunshan University and Zu Chongzhi Cen-
  tions require matching lower and upper bounds. With-                ter for Mathematics and Computational Sciences) for con-
  out mandatory tagging, the prover developed the eas-                tributing Projects 15–17 and providing expert verification
  ier lower bound but left the harder upper bound as a                and commentary. We thank Yilong Zhang (Limited Term
  sketch. This illustrates the misallocation of proof effort          Assistant Professor in the Department of Mathematics at
  described in Section 3.3. It also supports the purpose              the University of Georgia) for contributing Projects 13–14
  of <key-original-step> tags in Section 4.4 and                      and providing expert verification and commentary. We
  their verification role in Section 4.3: they force the prover       thank Qiao Zhuang (Assistant Professor in the Department
  and verifier to identify the mathematically novel step and          of Mathematics and Statistics at University of Missouri–
  demand maximal detail precisely there.                              Kansas City), Zhongqiang Zhang (Associate Professor in
• Decomposition mode. Neither question was solved com-                the Department of Mathematical Sciences at Worcester Poly-
  pletely in simple mode, whose iterative search–verify loop          technic Institute), and Yu Wang (Assistant Professor in the
  is described in Section 4.1. Across repeated attempts, the          School of Mathematics at Southwest Jiaotong University)
  prover frequently changed its overall proof strategy, in-           for contributing Project 18 and providing expert verifica-
  dicating that the proof plan was unstable in the sense of           tion and commentary. We thank Kewei Xu (Kai Toyosawa,
  Section 3.4. As a result, no single approach was devel-             Postdoctoral Researcher in the Department of Mathematics,
  oped in sufficient depth. The manuscripts produced in               University of Münster) for contributing Projects 11–12 and
  simple mode were at most 10 pages long. By contrast, de-            providing expert verification. We thank Sam Buss (Profes-
  composition mode produced the expert-accepted proofs in             sor at University of California, San Diego) for his continued
  Appendices A.1 and A.2, which were 20 and 15 pages, re-             support and insightful discussions.
  spectively. Although length alone does not measure proof
  quality, the qualitative difference was that decomposition          References
  mode preserved a stable plan long enough to resolve the
                                                                      Alexeev, B., Barreto, K., Li, Y., Lichtman, J. D., Price,
  difficult upper-bound arguments. This supports the claim
                                                                        L., Shah, J. I., Tang, Q., and Tao, T. Primitive sets
  in Section 4.2 and Table 1 that separating planning from
                                                                        and von mangoldt chains: Erdős problem #1196 and
  execution helps address unstable proof plans.
                                                                        beyond, 2026a. URL https://arxiv.org/abs/
                                                                        2605.00301.
These ablations are limited to two cases and are diagnostic

                                                                  9
             QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

Alexeev, B., Putterman, M., Sawhney, M., Sellke, M., and            Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
  Valiant, G. Short proofs in combinatorics and number                Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
  theory, 2026b. URL https://arxiv.org/abs/                           R., Hesse, C., and Schulman, J. Training verifiers to solve
  2603.29961.                                                         math word problems, 2021. URL https://arxiv.
                                                                      org/abs/2110.14168.
Alexeev, B., Putterman, M., Sawhney, M., Sellke, M., and
  Valiant, G. Short proofs in combinatorics, probability            Feng, T. Eigenweights for arithmetic hirzebruch propor-
  and number theory ii, 2026c. URL https://arxiv.                     tionality, 2026. URL https://arxiv.org/abs/
  org/abs/2604.06609.                                                 2601.23245.

An, C. and Pan, M. Return probability for the switch–walk–          Feng, T., Trinh, T. H., Bingham, G., Hwang, D., Chervonyi,
  switch lamplighter walk on a regular tree, 2026. URL                Y., Jung, J., Lee, J., Pagano, C., hyun Kim, S., Pasqualotto,
  https://arxiv.org/abs/2605.21744.                                   F., Gukov, S., Lee, J. N., Kim, J., Hou, K., Ghiasi, G.,
                                                                      Tay, Y., Li, Y., Kuang, C., Liu, Y., Lin, H., Liu, E. Z.,
An, C. and Xu, X. Lower bounds for advection-diffusion                Nayakanti, N., Yang, X., Cheng, H.-T., Hassabis, D.,
  equations: An exploration with ai-generated proofs, 2026.           Kavukcuoglu, K., Le, Q. V., and Luong, T. Towards
  URL https://arxiv.org/abs/2605.20623.                               autonomous mathematics research, 2026. URL https:
                                                                      //arxiv.org/abs/2602.10177.
An, C., Chen, Z., Ye, Q., First, E., Peng, L., Zhang, J.,
                                                                    Ghareeb, A. E., Chang, B., Mitchener, L., Yiu, A.,
 Wang, Z., Lerner, S., and Shang, J. Learn from fail-
                                                                      Szostkiewicz, C. J., Laurent, J. M., Razzak, M. T., White,
  ure: Fine-tuning LLMs with trial-and-error data for in-
                                                                     A. D., Hinks, M. M., and Rodriques, S. G. Robin: A multi-
  tuitionistic propositional logic proving. In Ku, L.-W.,
                                                                      agent system for automating scientific discovery, 2025.
  Martins, A., and Srikumar, V. (eds.), Proceedings of
                                                                      URL https://arxiv.org/abs/2505.13400.
  the 62nd Annual Meeting of the Association for Com-
  putational Linguistics (Volume 1: Long Papers), pp.               Glazer, E., Erdil, E., Besiroglu, T., Chicharro, D., Chen,
 776–790, Bangkok, Thailand, August 2024. Association                 E., Gunning, A., Olsson, C. F., Denain, J.-S., Ho, A.,
  for Computational Linguistics. doi: 10.18653/v1/2024.               de Oliveira Santos, E., Järviniemi, O., Barnett, M., San-
  acl-long.45. URL https://aclanthology.org/                          dler, R., Vrzala, M., Sevilla, J., Ren, Q., Pratt, E., Levine,
  2024.acl-long.45.                                                   L., Barkley, G., Stewart, N., Grechuk, B., Grechuk, T.,
                                                                      Enugandla, S. V., and Wildon, M. Frontiermath: A bench-
An, C., Imani, S., Yao, F., Dong, C., Abbasi, A., Shrivas-            mark for evaluating advanced mathematical reasoning in
  tava, H., Buss, S., Shang, J., Mahalingam, G., Sharma,              ai, 2025. URL https://arxiv.org/abs/2411.
  P., and Diesendruck, M. Next-token prediction task as-              04872.
  sumes optimal data ordering for llm training in proof gen-
  eration, 2025a. URL https://arxiv.org/abs/                        Gowers, T.  A recent experience with chatgpt 5.5
  2411.00863.                                                         pro. Gowers’s Weblog, May 2026. URL https:
                                                                     //gowers.wordpress.com/2026/05/08/
An, C., Qin, Z., Kong, S., and Flamant, C. DeRL:                      a-recent-experience-with-chatgpt-5-5-pro/.
  Diverse-exploration reinforcement learning for large               Accessed May 21, 2026.
  language models improves mathematical reasoning,
  2025b. URL https://openreview.net/forum?                          Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q.,
  id=ZIYYeTkZQ4.                                                     Xu, R., Zhang, R., Ma, S., Bi, X., Zhang, X., Yu, X., Wu,
                                                                     Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A.,
Arapura, D., Greer, F., and Zhang, Y. Failure of the invariant       Xue, B., Wang, B., Wu, B., Feng, B., Lu, C., Zhao, C.,
  cycle theorem over 𭟋, 2026. URL https://arxiv.                      Deng, C., Ruan, C., Dai, D., Chen, D., Ji, D., Li, E., Lin,
  org/abs/2602.07302.                                                 F., Dai, F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H.,
                                                                     Xu, H., Ding, H., Gao, H., Qu, H., Li, H., Guo, J., Li,
Bondarenko, A., Volk, D., Volkov, D., and Ladish, J.                 J., Chen, J., Yuan, J., Tu, J., Qiu, J., Li, J., Cai, J. L., Ni,
  Demonstrating specification gaming in reasoning mod-               J., Liang, J., Chen, J., Dong, K., Hu, K., You, K., Gao,
  els, 2025. URL https://arxiv.org/abs/2502.                          K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L.,
  13295.                                                              Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang,
                                                                      M., Zhang, M., Tang, M., Zhou, M., Li, M., Wang, M.,
Chaudhari, A., Ock, J., and Barati Farimani, A. Modular               Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q., Chen,
  large language model agents for multi-task computational            Q., Du, Q., Ge, R., Zhang, R., Pan, R., Wang, R., Chen,
  materials science. Communications Materials, 2026.                  R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen, S., Ye,

                                                               10
             QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

  S., Wang, S., Yu, S., Zhou, S., Pan, S., Li, S. S., Zhou, S.,          Coral: Towards autonomous multi-agent evolution for
  Wu, S., Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Liu,            open-ended discovery, 2026. URL https://arxiv.
  W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao, W. L.,                org/abs/2604.01658.
  An, W., Liu, X., Wang, X., Chen, X., Nie, X., Cheng, X.,
  Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su, X., Lin, X.,        Romera-Paredes, B., Barekatain, M., Novikov, A., Balog,
  Li, X. Q., Jin, X., Shen, X., Chen, X., Sun, X., Wang, X.,             M., Kumar, M. P., Dupont, E., Ruiz, F. J., Ellenberg, J. S.,
  Song, X., Zhou, X., Wang, X., Shan, X., Li, Y. K., Wang,               Wang, P., Fawzi, O., et al. Mathematical discoveries from
  Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li, Y., Zhao, Y., Sun,           program search with large language models. Nature, 625
  Y., Wang, Y., Yu, Y., Zhang, Y., Shi, Y., Xiong, Y., He, Y.,           (7995):468–475, 2024.
  Piao, Y., Wang, Y., Tan, Y., Ma, Y., Liu, Y., Guo, Y., Ou,           Tawosi, V., Ramani, K., Alamir, S., and Liu, X. Almas: an
  Y., Wang, Y., Gong, Y., Zou, Y., He, Y., Xiong, Y., Luo,               autonomous llm-based multi-agent software engineering
  Y., You, Y., Liu, Y., Zhou, Y., Zhu, Y. X., Huang, Y., Li,             framework, 2025. URL https://arxiv.org/abs/
  Y., Zheng, Y., Zhu, Y., Ma, Y., Tang, Y., Zha, Y., Yan, Y.,            2510.03463.
  Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang,
  Z., Hao, Z., Ma, Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu,          Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T. Solv-
  Z., Li, Z., Xie, Z., Song, Z., Pan, Z., Huang, Z., Xu,                 ing olympiad geometry without human demonstrations.
  Z., Zhang, Z., and Zhang, Z. Deepseek-R1 incentivizes                  Nature, 625(7995):476–482, 2024.
  reasoning in llms through reinforcement learning. Nature,
  645(8081):633–638, Sept 2025. ISSN 1476-4687. doi:                   Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang,
  10.1038/s41586-025-09422-z. URL http://dx.doi.                        S., Chowdhery, A., and Zhou, D. Self-consistency im-
  org/10.1038/s41586-025-09422-z.                                       proves chain of thought reasoning in language mod-
                                                                        els, 2023. URL https://arxiv.org/abs/2203.
Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,              11171.
  S., Tang, E., Song, D., and Steinhardt, J. Measuring math-
  ematical problem solving with the math dataset, 2021.                Wang, X., Tian, M., Zeng, Y., Huang, Z., Yuan, J., Chen,
  URL https://arxiv.org/abs/2103.03874.                                 B., Xu, J., Zhou, M., Liu, W., Wu, M., Guo, Z., Qian,
                                                                        Q., Wang, Y., Zhang, F., Yin, R., Dou, S., Lv, C., Chen,
Li, R., Zhang, Y., Zhou, X., Liang, P., Sun, W., Xuan, J., Jin,         T., Song, K., Tan, X., Gui, T., Zheng, X., and Huang, X.
   Z., and Liu, Y. Maad: Automate software architecture                 Reward hacking in the era of large models: Mechanisms,
   design through knowledge-driven multi-agent collabora-               emergent misalignment, challenges, 2026. URL https:
   tion, 2025. URL https://arxiv.org/abs/2507.                          //arxiv.org/abs/2604.13602.
   21382.
                                                                       Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter,
Naumov, V., Zagirova, D., Lin, S., Xie, Y., Gou, W., Urban,             B., Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-
  A., Tikhonova, N., Alawi, K., Durymanov, M., Galkin, F.,              thought prompting elicits reasoning in large language
  et al. Dora ai scientist: Multi-agent virtual research team           models, 2023. URL https://arxiv.org/abs/
  for scientific exploration discovery and automated report             2201.11903.
  generation. bioRxiv, 2025.
                                                                       Zheng, D., von Glehn, I., Zwols, Y., Beloshapka, I., Buesing,
OpenAI.   Planar point sets with many unit dis-
                                                                         L., Roy, D. M., Wattenberg, M., Georgiev, B., Schmidt,
  tances.   OpenAI technical proof manuscript,
                                                                         T., Cowie, A., et al. Ai co-mathematician: Acceler-
  2026. URL https://cdn.openai.com/pdf/
                                                                         ating mathematicians with agentic ai. arXiv preprint
 74c24085-19b0-4534-9c90-465b8e29ad73/
                                                                         arXiv:2605.06651, 2026.
  unit-distance-proof.pdf. Accessed May 21,
  2026.
Oyama, S., Sakurai, Y., and Kashima, H. Macc: Multi-agent              A. Successful Projects
  collaborative competition for scientific exploration, 2026.
  URL https://arxiv.org/abs/2603.03780.                                Table 2 collects the public proof records, expert comments,
                                                                       and withheld items for the five successful projects.
Phan, L., Gatti, A., Han, Z., Li, N., Hu, J., Zhang, H., Zhang,
  C. B. C., Shaaban, M., Ling, J., Shi, S., et al. Humanity’s          A.1. Project 6 — Return Probability Asymptotics for
  last exam. arXiv preprint arXiv:2501.14249, 2025.                         the Lamplighter Walk on Z2 ≀ Td
Qu, A., Zheng, H., Zhou, Z., Yan, Y., Tang, Y., Ong, S. Y.,            Problem Statement. Let d ≥ 3 and let Td denote the
  Hong, F., Zhou, K., Jiang, C., Kong, M., Zhu, J., Jiang,             infinite d-regular tree. Consider the switch–walk–switch
 X., Li, S., Wu, C., Low, B. K. H., Zhao, J., and Liang, P. P.         lamplighter random walk on the wreath product Z2 ≀ Td , and

                                                                  11
               QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

                                      Table 2. Appendix proof index for successful QED projects.

Description       Domain                  Record
Appendix A.1      Probability             Proof in (An & Pan, 2026); expert comments: https://github.com/proofQED/QED/blob/
                                          main/proved_statements/prob-May-15-2026/README.md
Appendix A.2      Probability             Proof and expert comments in https://github.com/proofQED/QED/blob/main/proved_
                                          statements/prob-May-15-2026
Appendix A.3      Algebraic geometry      Proof and expert comments in https://github.com/proofQED/QED/blob/main/proved_
                                          statements/algebraicgeometry-May-17-2026/problem-1-correct-proof.md
Appendix A.4      Fluid PDE               Proof in (An & Xu, 2026); expert comments: https://github.com/proofQED/QED/blob/main/
                                          proved_statements/analysis-May-19-2026/README.md
Appendix A.5      Inverse problems        Withheld until related work is archived.



let p2n (e, e) denote the return probability of this walk to the        Workflow. The domain expert provided the problem state-
identity after 2n steps. Set                                            ment to QED with no further mathematical input. QED was
                                √                                       run in decomposition mode and produced the correct proof
                               2 d−1                                    through multiple rounds of refinement, including substantial
                       ρd =             .
                                   d                                    changes of proof plan by the decomposition agent. The
Then the following sharp asymptotic holds:                              resulting proof was then verified by the expert.
                                                            
                                                       n
p2n (e, e) = ρd2n exp − π 2 (log(d − 1))2 + o(1)
                                                 
                                                               . Expert Comment This is a technically nontrivial Ph.D.-
                                                     log2 n
                                                                 level problem in probability theory. The question again is in
Workflow. The domain expert provided the problem state-          the style of precise probabilistic calculations and estimates.
ment to QED with no further mathematical input. QED was
run in decomposition mode and produced the correct proof         A.3. Project 13 — Local Invariant Cycle Theorem over
through multiple rounds of refinement, including substantial          the Integers in Degree One
changes of proof plan by the decomposition agent. The            Problem Statement. Let X → B be a one-parameter
resulting proof was then verified by the expert.                 family of complex projective varieties over a small disk
                                                                        B, and assume that the central fiber is a simple normal
Expert Comment This result is a solid specialized contri-               crossing divisor. Let Xt denote a smooth nearby fiber, and
bution in probability theory. Its proof has real mathematical           let T denote the monodromy operator acting on H 1 (Xt , Z).
content as it cleverly combines probabilistic constructions             Then the restriction map
with spectral analysis. Its significance appears comparable
to work suitable for venues such as the Electronic Journal of
                                                                                       H 1 (X, Z) −→ H 1 (Xt , Z)T
Probability or Proceedings of the American Mathematical
Society. The question is in the style of precise probabilistic
calculations and estimates.                                             to the monodromy-invariant submodule is surjective. The
                                                                        classical (rational) invariant cycle theorem of Clemens–
A.2. Project 8 — Total Variation Asymptotics for the                    Schmid (1970s) establishes the analogous statement after
     Switch–Walk–Switch Walk on Z2 ≀ Z                                  tensoring with Q; the integral version was open. In February
                                                                        2026, Arapura–Greer–Zhang showed that the integral state-
Problem Statement. Consider the discrete-time switch–                   ment fails for H 2 . The result above establishes the integral
walk–switch random walk on the wreath product Z2 ≀ Z, and               statement for H 1 .
for a starting point x ∈ Z2 ≀ Z let Ptx denote the law of this
walk at time t. Fix
                                                                        Workflow. At the time QED was given this problem, the
          x = (0, 0)            and     y = (0, 2).                     human author had already discovered a proof but had not
                                                                        yet released it publicly. The domain expert provided the
Then the total variation distance between the two laws satis-           problem statement to QED with no further mathematical
fies the sharp asymptotic                                               input. The resulting proof was independently verified by
                   Ptx − Pty TV ≍ t−1/2 ,                               the expert and was found to be mathematically different
                                                                        from the human author’s proof. The human author subse-
where ≍ denotes equality up to positive multiplicative con-             quently posted their own proof to arXiv, which is included
stants independent of t.                                                in (Arapura et al., 2026).

                                                                   12
             QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

Expert Comment The method in the AI’s proof that in-                   Result 3 (Fast time-periodic flows; exponential L2 lower
terprets the coboundary map H 1 (X ∗ ) → H 2 (X, X ∗ ) as              bound). Let u ∈ L∞           1,∞
                                                                                              t Wx,y be divergence-free and L-
the residue map is original. This actually holds in higher             periodic in time, and let ρ solve
degrees by working with Griffiths’ residue, but in degree
one this interpretation is the classical residue and is partic-                    ∂t ρ + u(At, x, y) · ∇ρ = ν ∆ρ.
ularly useful for the integral local invariant cycle theorem,
since one has the key lemma which is essential in the proof.           Then there exist an explicit threshold A0 > 0, exponent
The proof is elementary and elegant: the first lemma is                cA > 0, and constant C > 0, all expressed in terms of ρ0 ,
essentially residue theory in complex analysis, and the sec-           u, L, and ν, such that for every A > A0 ,
ond is essentially reduced to Picard–Lefschetz theory for
                                                                                   ∥ρ(t)∥L2 ≥ C e−cA t         (t ≥ 0).
curves. It provides a different point of view on the integral
version of the invariant cycle theorem in degree one. The
                                                                       In particular, for time-independent flows and time-periodic
expert classified problem difficulty as follows: easy means
                                                                       flows of sufficiently high frequency, superexponential L2
that the expected results can be achieved by standard meth-
                                                                       decay is impossible.
ods; moderately difficult means that the expected results are
plausible, but the methods are not known in advance; and
                                                                       Workflow. The domain expert formulated the problem
difficult refers to solving open problems that have remained
                                                                       statements but did not intervene in the construction of the
unresolved for years, or finding unexpected examples or
                                                                       arguments; no PDE-specific guidance was given during
counterexamples. Under this expert classification, this prob-
                                                                       the proof-generation process. QED produced the complete
lem is considered moderately difficult.
                                                                       chain of reasoning, from the reduction of each problem to its
                                                                       step-by-step estimates, and verified the logical consistency
A.4. Project 15 — Explicit Lower Bounds for
                                                                       of the derivations. The expert confirmed that the QED
     Advection–Diffusion Equations
                                                                       outputs are correct.
Problem Statement. Consider the advection–diffusion
equation                                                               A.5. Project 18 — Carleman Estimate Weight Functions
              ∂t ρ + u · ∇ρ = ν ∆ρ
                                                                       Problem statement. Construct a smooth space–time
on the two-dimensional torus T2 with mean-zero smooth                  weight function ψ(x, t) (with auxiliary parameters) for the
initial data ρ0 ̸≡ 0 and divergence-free velocity field u.             wave operator on a half-infinite domain such that it satisfies
The paper establishes explicit, constructive lower bounds on           strict pseudoconvexity-type inequalities, positivity condi-
suitable norms of the solution in three settings.                      tions, and sufficient growth at infinity to establish a valid
                                                                       Carleman estimate. Note: the full problem statement and
Result 1 (Inviscid shear; polynomial Ḣ −1 lower bound).
                                                                       proof are withheld until the corresponding mathematics
Let θ solve the transport equation
                                                                       paper is posted on arXiv.
        ∂t θ + U (y, t) ∂x θ = 0,         θ(0) = θ0 ,
with U ∈    L∞  1,1
                                 ∈ C ∞ (T2 ) mean-zero.                Result. Using Claude Opus 4.6 for both proof generation
             t Wy (T) and θ0
Then there exists a constant c∗ > 0, depending only on                 and verification, QED (with simple mode) produced a can-
θ0 and U , such that                                                   didate weight function and a complete proof in Round 1.
                          c∗                                           The proof was produced without any domain-expert guid-
         ∥θ(t)∥Ḣ −1 ≥            for all t ≥ 0.                       ance except for the correction to the statement of problem 5
                        1 + t2
                                                                       prompted by the AI’s solution to the originally stated prob-
                                                                       lem. Subsequent expert review determined that this solution
Result 2 (Diffusive shear; exponential L2 lower bound and
                                                                       corresponded to a degenerate case, revealing that the orig-
uniform mixing scale). Let ρ solve
                                                                       inal constraints were too weak (a formulation issue rather
               ∂t ρ + U (t, y) ∂x ρ = ν ∆ρ,                            than a QED failure). After strengthening the constraints,
                                                                       the experts instructed QED to continue from its previous
with U ∈ L∞    t,y (T) and ν > 0. Then there are explicit
                                                                       candidate. QED then returned a refined weight function
constants c2 , c∗ > 0, computable from ρ0 , U , and ν, such
                                                                       together with complete proofs satisfying all strengthened
that
                                                                       conditions. No human intervention was required beyond
         ∥ρ(t)∥L2 ≥ ∥ρ0 ∥L2 e−c2 t      (t ≥ 0),
                                                                       refinement of the problem specification.
and, in the small-diffusivity regime 0 < ν ≪ 1, the mixing
scale is uniformly bounded below:                                      Expert assessment. One of the most promising applica-
            ∥ρ(t)∥Ḣ −1                                                tions of QED to the theory of Carleman estimates is the
                        ≥ c∗        for all t ≥ 0.                     automated search for admissible Carleman weights. The
             ∥ρ(t)∥L2

                                                                  13
              QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

success of a Carleman estimate hinges on finding a weight                are as below, which can all be found in (arXiv:1401.4197,
function finely adapted to the operator, the geometry, the               pp. 3–4).
boundary structure, and the relevant pseudoconvexity condi-              Definition B.1 (FIID). Let L be Lebesgue measure on [0, 1].
tions. Traditionally, this has been a highly problem-specific,           We equip the domain space [0, 1]V with the product measure
experience-driven process, involving substantial trial and               LV . The elements ω ∈ [0, 1]V of the domain space are
error and lengthy inequality verification. A specialized                 sometimes called labels.
QED-style system could transform this step into a modu-
lar, parallelizable, and rigorously verifiable search proce-             A measurable map ϕ : [0, 1]V → S V is called an Aut(Td )-
dure: candidate weights are generated, tested against the                factor if it is Aut(Td )-equivariant: for all γ ∈ Aut(Td ),
                                                                                ϕ(γω) = γ ϕ(ω) for LV -a.e. ω ∈ [0, 1]V .
                                                                                                   
required structural conditions, iteratively refined, and ul-
timately checked with full rigor. Such a tool would be
                                                                         Since the domain space is equipped with a product measure,
valuable not only for accelerating well-established construc-
                                                                         or i.i.d., such a ϕ is called a factor of i.i.d., or FIID for short.
tions, but also for exploring problems where the correct
                                                                         The push-forward measure ϕ∗ LV on S V is also called an
ansatz has yet to emerge.
                                                                         FIID.
Experts believe that QED’s contribution to this work is                  Definition B.2 (Finite Dependence). An Aut(Td )-invariant
comparable to that of research published in journals such as             probability measure µ on S V is m-dependent if
the Journal of Mathematical Analysis and Applications.                   σ(K1 ), . . . , σ(Kp ) are independent whenever the sets
                                                                         K1 , . . . , Kp ⊆ V are pairwise separated by graph distance
B. Unsuccessful Cases                                                    strictly greater than m. We say that µ is finitely dependent
                                                                         if it is m-dependent for some m < ∞.
The following problems were attempted by QED but were
not solved within the system’s preset budget. Table 3 gives              B.3. Project 7
a compact index, followed by the full problem statements
retained for future evaluation.                                          Problem statement. For each n, let (Xi )0≤i≤n be the
                                                                         simple nearest-neighbor random walk on Zk conditional on
B.1. Project 2                                                           X0 = 0 and no self-intersections up to time n — that is, a
                                                                         self-avoiding walk. Let dk (n) := E(∥Xn ∥), the expected
Problem statement. Let d ≥ 3. Let Td be the d-regular                    Euclidean distance of Xn from the origin. Is it true that
tree. There is a unique Aut(Td )-invariant probability mea-              d3 (n) ≫ n1/2 ?
sure µ on the set of proper d-colorings of E(Td ), the set of
edges of Td .                                                            B.4. Project 10
This measure is easy to construct. Let o be a fixed root.                Problem statement. Let T4 = (V, E) be the infinite 4-
Among the edges in Td adjacent to o, choose the colors of                regular tree. Let (σ0 (v))v∈V be i.i.d. with
the edges uniformly at random such that they are distinct.
Then, working outwards independently, where every time                     Pp (σ0 (v) = +1) = p,           Pp (σ0 (v) = −1) = 1 − p.
there is a choice of d − 1 distinct colors for d − 1 edges               Run continuous-time zero-temperature Glauber dynamics:
to guarantee that the coloring is proper, choose the colors              each vertex has an independent rate-one Poisson clock, and
uniformly at random across the edges.                                    when the clock at v rings, σ(v) is updated to agree with the
Prove that µ is a factor of i.i.d. Relevant definitions and              majority of its four neighbors; in case of a tie, the new spin
properties can be found in Russell Lyons’s Factors of IID                is chosen uniformly from {−1, +1}. Let Pp denote the law
on Trees.                                                                of the dynamics.
                                                                         Define
B.2. Project 3                                                                            n
                                                                           pc (T4 ) := inf p ∈ [0, 1] :
Problem statement. Let Td be the d-regular tree for                                                                    o
d ≥ 3, with vertex set V = V (Td ). We consider pro-                               Pp lim σt (v) = +1 for every v ∈ V = 1 .
                                                                                         t→∞
cesses that are invariant under the full automorphism group
Aut(Td ). Let S be a finite state space (such as {0, 1}). For            Prove Morris’ conjecture for T4 : for zero-temperature
K ⊆ V , write σ(K) for the σ-field on S V generated by the               Glauber dynamics on the 4-regular tree,
coordinate projections πx for x ∈ K.                                                                      1
                                                                                                pc (T4 ) = .
Prove that if µ is an Aut(Td )-invariant, finitely dependent                                              2
probability measure on S V (for d ≥ 3), then µ is a factor of            Equivalently, for every p > 1/2, the process fixates to +1
i.i.d. The definitions of factor of i.i.d. and finitely dependent        at every vertex almost surely.

                                                                    14
               QED: An Open-Source Multi-Agent System for Generating Mathematical Proofs on Open Problems

                                  Table 3. Index of unsuccessful QED cases disclosed in the appendix.

Description        Area                   Problem summary
Appendix B.1       Probability            Show that the invariant random proper edge-coloring measure on the d-regular tree is a factor
                                          of i.i.d.
Appendix B.2       Probability            Show that every finitely dependent Aut(Td )-invariant process on a finite state space is a factor
                                          of i.i.d.
Appendix B.3       Probability            Determine whether the three-dimensional self-avoiding walk has expected displacement larger
                                          than diffusive order, d3 (n) ≫ n1/2 .
Appendix B.4       Probability            Prove Morris’ conjecture pc (T4 ) = 1/2 for zero-temperature Glauber dynamics on the 4-
                                          regular tree.
Appendix B.5       Operator algebra       Determine whether coarse embeddability is a W ∗ -invariant for countable discrete groups.



B.5. Project 11
Problem statement. Is coarsely embeddability a W∗ -
invariant? That is, if Γ, Λ are countable discrete groups
and the group von Neumann algebras LΓ ≃ LΛ are iso-
morphic, then Γ being coarsely embeddable into Hilbert
spaces implies Λ is coarsely embeddable into Hilbert spaces
as well.
                                                                       Table 4. Per-attempt breakdown of proof generation runs in de-
                                                                       composition mode. Attempt = number of new plans generated.
C. Retry Information                                                   Revisions = same plan, number of times it is revised and the proof
                                                                       regenerated to completion. Proof number = same plan, number
In this section, A.1–A.5 refer to the 5 successful QED                 of times the proof is modified. Some successful appendix entries
projects. The notation “P” refers to an internal problem               contain multiple internal problem statements, and not every inter-
                                                                       nal problem statement necessarily appears in the final proof.
statement within one of those appendices, not to the original
research-project IDs from Section 5. For example, “A.4, P3”              Run identifier     Attempt      Revisions      Proof number
is the third internal problem statement within A.4, whereas
Project 15 is the original research project corresponding to             A.1                    2             1                2
A.4.                                                                     A.2                    1             2                5
 Table 5. Simple/legacy-mode QED runs without decomposi-                 A.3                    1             1                1
 tion, counted by verification rounds.
                                                                         A.4, P3                1             1                2
              Run identifier     Verification rounds                     A.4, P4                1             1                2
              A.4, P1                    4                               A.4, P5                1             1                3
              A.4, P2                    4
              A.5                        1                               A.4, P6                1             1                2
                                                                         A.4, P7                1             1                1
                                                                         A.4, P8                1             3                5
                                                                         A.4, P9                1             1                3
                                                                         A.4, P10               1             1                1
                                                                         A.4, P11               2             2                6
                                                                         A.4, P12               2             3                3




                                                                  15
