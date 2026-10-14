                                            SCAFFOLD-CEGIS: Preventing Latent Security
                                              Degradation in LLM-Driven Iterative Code
                                                             Refinement
                                                           1st Yi Chen                                                   2nd Yun Bian
                                           Chengdu Institute of Computer Application                      Chengdu Institute of Computer Application
                                                 Chinese Academy of Sciences                                    Chinese Academy of Sciences
                                                         Chengdu, China                                                 Chengdu, China
                                           University of Chinese Academy of Sciences                      University of Chinese Academy of Sciences
                                                          Beijing, China                                                 Beijing, China
arXiv:2603.08520v1 [cs.CR] 9 Mar 2026




                                                    chenyi24@mail.ucas.ac.cn                                        bianyun@casit.com.cn
                                                3rd Haiquan Wang                            4th Shihao Li                            5th Zhe Cui∗
                                           Chengdu Institute of Computer           Chengdu Institute of Computer            Chengdu Institute of Computer
                                                     Application                             Application                              Application
                                            Chinese Academy of Sciences             Chinese Academy of Sciences              Chinese Academy of Sciences
                                                   Chengdu, China                          Chengdu, China                           Chengdu, China
                                          University of Chinese Academy of        University of Chinese Academy of         University of Chinese Academy of
                                                       Sciences                                Sciences                                 Sciences
                                                    Beijing, China                          Beijing, China                           Beijing, China
                                          wanghaiquan22@mails.ucas.ac.cn            lishihao25@mails.ucas.ac.cn                  cuizhe@casit.com.cn


                                          Abstract—The application of large language models         tonicity rate of 100%. These results indicate that LLM-
                                        to code generation has evolved from one-shot gen-           driven iterative code refinement entails an inherent
                                        eration to iterative refinement, yet the evolution of       risk of security degradation, that static-analysis gating
                                        security throughout iteration remains insuﬀiciently un-     may further induce a pseudo-security effect, and that
                                        derstood. Through comparative experiments on three          explicit semantic constraints are necessary to suppress
                                        mainstream LLMs, this paper reveals the iterative           latent security degradation during iterative refinement.
                                        refinement paradox: specification drift during multi-
                                        objective optimization causes security to degrade grad-        Index Terms—Large Language Models, Code Secu-
                                        ually over successive iterations. Taking GPT-4o as          rity, Iterative Refinement, Latent Security Degrada-
                                        an example, 43.7% of iteration chains contain more          tion, Multi-Agent Systems
                                        vulnerabilities than the baseline after ten rounds, and
                                        cross-model experiments show that this phenomenon is                            I. Introduction
                                        prevalent.
                                                                                                       The use of large language models in software engineering
                                           Further analysis shows that simply introducing static
                                        application security testing (SAST) gating cannot ef-       has expanded from one-shot code generation to iterative
                                        fectively suppress degradation; instead, it increases the   code refinement. Tools such as GitHub Copilot and Cursor
                                        latent security degradation rate from 12.5% under the       allow developers to interact with LLMs over multiple
                                        unprotected baseline to 20.8%. The root cause is that       rounds to improve functionality, optimize performance,
                                        static-analysis rules cannot cover structural degrada-
                                                                                                    and fix defects. However, prior work has focused primarily
                                        tions such as the removal of defensive logic or the
                                        weakening of exception handling. To address this prob-      on single-shot generation quality, while the evolution of
                                        lem, we propose the SCAFFOLD-CEGIS framework.               security throughout iterative refinement remains insuﬀi-
                                        Drawing on the counterexample-guided inductive syn-         ciently studied.
                                        thesis (CEGIS) paradigm, the framework adopts a
                                        multi-agent collaborative architecture that transforms      A. The Iterative Refinement Paradox
                                        security constraints from implicit prompts into explicit
                                        verifiable constraints. It automatically identifies and        Current AI-assisted programming workflows implicitly
                                        solidifies security-critical elements as hard constraints   assume that multi-turn interaction progressively improves
                                        through semantic anchoring, enforces safety mono-           code quality. Our empirical results show that, in the
                                        tonicity through four-layer gated verification, and con-    absence of strong external constraints, iterative LLM re-
                                        tinuously assimilates experience from failures. Compar-
                                        ative experiments against six existing defense methods      finement can instead degrade code security.
                                        show that the full framework reduces the latent security       The root cause is specification drift in multi-objective
                                        degradation rate to 2.1% and achieves a safety mono-        optimization. In each iteration, the LLM jointly opti-
mizes competing objectives, including functional complete-      change budget, and anchor integrity for each candidate.
ness, performance eﬀiciency, maintainability, and security.     Failure assimilation extracts structured lessons from re-
When security constraints exist only as soft prompts,           jected candidates to guide subsequent generation.
the optimization trajectory gradually departs from the             Cross-language and cross-model validation. Ex-
intended security specification, for example by removing        periments across multiple mainstream LLMs and lan-
validation logic, breaking API compatibility, or introduc-      guages confirm the reproducibility of the iterative refine-
ing resource leaks.                                             ment paradox. Ablation studies isolate the contribution
   Experiments on 96 iteration chains with GPT-4o sup-          of each component. The full framework reduces latent
port this claim. When all vulnerability severities are          security degradation from 20.8% to 2.1% and attains 100%
counted (DRall ), a substantial share of chains already ex-     safety monotonicity under our setup, while preserving code
ceed the baseline vulnerability count by iteration 10. Even     evolution capability.
under explicit security-hardening prompts, the degrada-            The remainder of this paper is organized as follows.
tion rate remains 28.6%. Detailed settings and vulnerabil-      Section II reviews related work. Section III presents the
ity trajectories are presented in Section IV-A.                 SCAFFOLD-CEGIS framework. Section IV reports the
                                                                experimental setup and results. Section V discusses limi-
B. Coverage Blind Spots of SAST Gating                          tations and future work. Section VI concludes.
   A natural mitigation strategy is to run static analysis
                                                                                    II. Related Work
after each iteration and reject changes that introduce new
vulnerabilities. However, static analyzers have coverage        A. Security Evaluation of LLM Code Generation
blind spots. We define one class of degradation as latent se-      As large language models (LLMs) become deeply in-
curity degradation: security-critical elements are removed      tegrated into practical development workflows, includ-
or weakened during iteration without triggering SAST            ing code completion, natural-language-to-code genera-
rules. Typical cases include deleting validation functions      tion, and automated bug fixing (e.g., GitHub Copilot
without introducing new SAST-detectable patterns, weak-         and Amazon CodeWhisperer), the security properties of
ening exception handling logic, or bypassing permission         model-generated code have attracted sustained academic
checks along paths not covered by the analyzer.                 scrutiny: while satisfying functional requirements, do these
   SAST detection logic is grounded in known vulnerability      models reliably adhere to secure coding practices?
patterns and cannot directly capture accidental removal            Existing empirical studies analyze this problem mainly
or weakening of security-critical elements. Once an LLM         from two dimensions: vulnerability-introduction tendency
removes validation or sanitization logic during refactoring,    and prompt robustness. Multiple independent studies
degradation remains undetected if the remaining code does       show that, without explicit security constraints, main-
not match rule-based vulnerability signatures.                  stream LLMs frequently reproduce vulnerable coding pat-
                                                                terns present in training data. Perry et al. [1] report
C. Contributions                                                through large-scale user studies that developers using
   To address latent security degradation, this paper           coding assistants are more likely to accept insecure sug-
introduces SCAFFOLD-CEGIS, a multi-agent framework              gestions and often fail to identify the defects. Khoury et
that adopts the structural principle of CEGIS                   al. [2] show systematic weaknesses in key management and
(Counterexample-Guided Inductive Synthesis). The                randomness generation in cryptographic tasks. Siddiq et
framework protects security-critical elements via semantic      al. [3] further quantify this risk with the SALLM bench-
anchoring and closes key SAST coverage gaps.                    mark, using secure@k (the probability that all k samples
   The main contributions are as follows.                       are vulnerability-free) and vulnerable@k (the probability
   Iterative refinement paradox and SAST blind                  that at least one sample is vulnerable) in SQL injection
spots. Controlled experiments on 96 GPT-4o iteration            and XSS defense scenarios, and find frequent omission of
chains reveal systematic security degradation in iterative      critical input-validation logic (e.g., parameterized queries
LLM refinement, and show that static analyzers miss             or output escaping) even when models are explicitly in-
structural degradations such as deleted defensive logic and     structed to generate secure code. Pearce et al. [4] expose
weakened exception handling.                                    a deeper issue: models may not only generate vulnerable
   SCAFFOLD-CEGIS framework. We propose a                       code but also provide incorrect security explanations,
CEGIS-inspired multi-agent architecture that transforms         claiming insecure implementations are safe.
security constraints from implicit prompt instructions             To transform these qualitative observations into mea-
into explicit, verifiable hard constraints. The framework       surable evidence, recent work has focused on standard-
combines semantic anchoring, four-layer gated verifica-         ized benchmarks. Hajipour et al. [5] propose CodeLM-Sec,
tion, and failure assimilation. Semantic anchoring mines        which stress-tests black-box models with adversarial
security-critical functions, defense patterns, and API-         prompt templates targeting specific vulnerability classes
compatibility constraints and solidifies them as invariants.    (e.g., buffer overflow and command injection). Li et
Four-layer gating checks correctness, safety monotonicity,      al. [6] focus on attribution analysis, aiming to separate
vulnerabilities caused by pretraining-data contamination         repair and in-execution repair, and identify failure modes
from those caused by alignment failure at inference. Ti-         caused by incomplete test coverage, noisy feedback, and
hanyi et al. [7] and SecCodeBench [8] establish cross-           ambiguous error localization.
language and cross-model comparative benchmarks and                 In existing LLM iterative synthesis studies, feedback is
report vulnerability-generation rates across fixed task sets.    sourced primarily from functional correctness, i.e., whether
Collectively, these efforts mark a shift from case-based         code compiles or passes unit tests. Security properties
analysis to benchmark-driven evaluation in LLM code              (e.g., memory safety, access control, and completeness
security.                                                        of input validation) are diﬀicult to cover with unit tests
   For mitigation, current studies follow two major direc-       alone, and usually lack CEGIS-style formal specifications
tions: inference-time alignment and data/training align-         as hard constraints. Consequently, under weak security
ment. The former filters unsafe outputs using security-          feedback, models tend to overfit local functional objectives
oriented prompting, constrained decoding, or static-             during iteration, unintentionally removing defensive logic
analysis feedback loops. He et al. [9] use static-analysis       or introducing new attack surfaces during refactoring. This
diagnostics as feedback signals for model self-correction,       security-objective drift induced by weak feedback is the
while Tony et al. [10] investigate chain-of-thought prompt-      core cause of the iterative refinement paradox defined in
ing for security reasoning. The latter suppresses insecure-      this paper.
generation patterns at the distribution level through high-
quality secure-code datasets or instruction tuning. He et                III. SCAFFOLD-CEGIS Framework
al. [11] release an instruction dataset for security repair,
and De et al. [12] study the effectiveness of RLHF in            A. Theoretical Foundations
optimizing security preferences.                                   We model iterative code refinement as a state-transition
   Most of the above methods target the security of single-      system. Let P denote the set of programs and T the set
shot generation. A recent survey [13] notes that existing        of tasks. The transition function δ : P × T → P maps
strategies focus on a static “generate-detect” loop and          program Pi to Pi+1 given task τ . An iteration chain is
insuﬀiciently account for the dynamic evolution of security      defined as the state sequence C = ⟨P0 , P1 , . . . , Pn ⟩.
properties in multi-turn interaction. In particular, when          The security metric V : P → N maps a program to its
developers iteratively optimize functionality or perfor-         vulnerability count. Safety monotonicity over an iteration
mance with LLMs, early security constraints are easily           chain C is defined in Eq. (1).
diluted or forgotten in subsequent context windows, yield-
ing the paradox of “functional improvement with security                              ∀i, V (Pi+1 ) ≤ V (Pi )                     (1)
degradation.”
                                                                 The degradation rate DR and safety monotonicity rate
B. Iterative Program Synthesis and Feedback Mechanisms           SM R are defined in Eq. (2) and Eq. (3), respectively.
   Iterative program synthesis seeks target programs
                                                                                         |{C : V (Pn ) > V (P0 )}|
through a closed loop of generation, verification,                              DR =                                              (2)
feedback, and regeneration. Classical paradigms                                                    |Call |
such as Counterexample-Guided Inductive Synthesis                                      ∑
(CEGIS) [14], [15] rely on formal verifiers to provide                                     C |{i : V (P
                                                                                                     ∑i+1
                                                                                                          ) ≤ V (Pi )}|
                                                                            SM R =                                                (3)
precise counterexamples that contract the search                                                       C nC
space. Building on this idea, Syntax-Guided Synthesis               SCAFFOLD-CEGIS constrains state transitions
(SyGuS) [16] introduces grammar constraints to further           through a gating function. The security specification
bound candidate programs and keep synthesis within               Φ is an explicit constraint set generated by semantic
decidable regimes. A defining characteristic of these            anchoring, including security-critical invariants, API
traditional methods is strong external constraints: the          signatures, and defense patterns. The gate function G is
iteration process is tightly specified, and any candidate        formally defined in Eq. (4), and internally implemented as
that violates the specification is immediately eliminated.       the conjunction of four sub-checks (Eq. (5)): correctness,
   In LLM-driven synthesis, iterative mechanisms are typ-        safety monotonicity, diff budget, and anchor integrity.
ically instantiated as self-debugging or multi-agent collab-
oration. The Reflexion framework proposed by Shinn et                         G : P × P × Φ → {accept, reject}                    (4)
al. [17] improves subsequent attempts by prompting mod-
els to reflect on natural-language trajectories of failed exe-         G(P, P ′ , Φ) = Vcorr (P ′ ) ∧ Vsec (P, P ′ )
cution and by accumulating failure experience in memory.                                                                          (5)
                                                                                         ∧ Vdif f (P, P ′ ) ∧ Vanchor (P ′ , Φ)
Similarly, reinforcement-learning-based approaches [18]
aim to improve model utilization of execution feedback           When δmax = 0, the gated iteration chain satisfies Eq. (6).
such as compilation errors and unit-test failures. Recent
studies [19] further distinguish between post-execution                       δmax = 0 ⇒ ∀i, V (Pi+1 ) ≤ V (Pi )                  (6)
B. Framework Overview                                            Algorithm 1 SCAFFOLD-CEGIS Iterative Procedure
                                                                 Require: Baseline code P0 , refinement task sequence
   SCAFFOLD-CEGIS adopts a multi-agent collaborative                 T = {τ1 , . . . , τn }, maximum retries Rmax , security
architecture that converts security constraints from im-             tolerance threshold δmax
plicit prompts into explicit verifiable constraints. The         Ensure: Final code Pn satisfies V (Pn ) ≤ V (P0 )
framework includes four agents: SecurityArchitectAgent            1: P ← P0
mines security-critical elements from code and constructs         2: K ← ∅                          ▷ Failure knowledge base
the semantic anchor set Φ; ImplementerAgent generates             3: S0 ← LLMReview(P0 )            ▷ Baseline latent-security
candidate code P ′ under anchor constraints; GatekeeperA-            issue count
gent performs four-layer gating to validate correctness and       4: for i = 1 to n do
safety monotonicity of each change; AssimilatorAgent an-          5:     Φ ← MineAnchors(P ) ▷ SecurityArchitectAgent
alyzes rejected attempts and extracts reusable experience         6:     r←0
for subsequent iterations. Figure 1 illustrates the overall       7:     while r < Rmax do
architecture.                                                     8:         P ′ ← Implement(P, τi , Φ, K)                     ▷
   This framework borrows the iterative structure of                 ImplementerAgent
CEGIS, i.e., a closed loop of candidate generation, verifica-     9:         Tresult ← RunTests(P ′ ) ▷ Correctness check
tion, feedback, and regeneration, while relaxing the formal      10:         ∆Vstep ← VSAST (P ′ ) − VSAST (P )                ▷
counterexample requirement. In classical CEGIS, verifiers            Safety-monotonicity check
are based on formal specifications and SMT solving, and          11:         ∆L ← |P ′ | − |P |           ▷ Diff-budget check
the resulting counterexamples precisely shrink the candi-        12:         Aresult ← VerifyAnchors(P ′ , Φ)                  ▷
date search space. In our framework, the verifier is replaced        Anchor-integrity check
by a combination of static analysis and semantic-anchor          13:         if Tresult = PASS ∧ ∆Vstep ≤ δmax ∧ |∆L| ≤
checking, and counterexamples are represented as struc-              B ∧ Aresult = PASS then
tured failure reports produced after gate rejection, includ-     14:             P ← P′                      ▷ Accept change
ing failure type, violated constraints, and code locations,      15:             break
and passed to ImplementerAgent in natural language.              16:         else
This substitution trades formal completeness for practical       17:             C ← GenCE(P, P ′ , Tresult , ∆Vstep , Aresult )
applicability in real software-engineering settings, enabling    18:             K ← K ∪ Assimilate(C)                         ▷
handling of security properties that are diﬀicult to fully           AssimilatorAgent
formalize.                                                       19:             r ←r+1
   The execution flow follows this iterative process. Securit-   20:         end if
yArchitectAgent analyzes the current code and produces           21:     end while
the semantic anchor set. ImplementerAgent then generates         22:     if r = Rmax then
a candidate satisfying the current refinement task under         23:         continue          ▷ Rollback; keep P unchanged
hard anchor constraints. GatekeeperAgent performs four-          24:     end if
layer verification of correctness and safety monotonicity.       25: end for
Upon verification failure, the system decides between retry      26: Sn ← LLMReview(P ) ▷ Final latent-security issue
and rollback according to failure type, while Assimila-              count, for SSDR
torAgent records failure causes and extracts structured          27: return P
lessons. The security specification Φ = ⟨I, A, R⟩ consists
of invariant anchors I, API-signature anchors A, and a
security rule base R. Anchors are updated dynamically as         each iteration to introduce no new SAST-detectable vul-
code evolves, and stale constraints are removed by a TTL         nerabilities.
mechanism.
   Algorithm 1 summarizes the core loop. In each iteration,      C. Semantic Anchor Mining
SecurityArchitectAgent mines semantic anchors, Imple-
menterAgent generates a candidate, and GatekeeperAgent              Semantic anchors are formal representations of security-
executes four-layer verification. Accepted candidates are        critical elements in code, used to prevent accidental mod-
committed; rejected candidates trigger retry or rollback         ification or deletion during iteration. SecurityArchitectA-
according to failure type. AssimilatorAgent extracts expe-       gent mines anchors from three levels.
rience from failures and feeds it into subsequent iterations.       Function-level anchors use regex matching to identify
After all iterations, an LLM Reviewer performs semantic          security-critical functions, such as validation functions
review on the final code; its output is used only for SSDR       validate_*, sanitization functions sanitize_*, and au-
and RDR evaluation and does not participate in gate              thentication functions auth*. AST parsing then extracts
decisions. The algorithm guarantees V (Pn ) ≤ V (P0 ) when       function signatures, including function names, parameter
δmax = 0. In our experiments, we set δmax = 0, requiring         lists, and return types. For public APIs, required param-
                                              CEGIS Iteration Loop(𝒊 = 𝟏, 𝟐, … , 𝒏)                      CEGIS Mapping Legend
                        Baseline Code 𝑃!
                                                                                                    Specification = 𝜙 CounterExample=𝐶
                                                                                                    Candidate = 𝑃!    Update = Feedback
               Task 𝜏                    Security Rules 𝑅                                           Verifier = Gatekeeper



     Security Architect                    Implementer                              GateKeeper Agent
           Agent                             Agent                                      (Verify)
       Anchor Mining        Semantic                           Candidate                                              FAIL
                            Anchors                              Code
 •    Function Level
                              𝜙                LLM                𝑃!       Correctness Security   Diff     Anchor
 •    Pattern Level
 •    Invariant Level                      Code Generation


                          LLM Reviewer
                            Evaluation                                            PASS
                                                                                                              Assimilator Agent
                                                                   FeedBack
                  Next Iteration                                                                               Counterexample Analysis
                                                                        Last Iteration                         Experience Extraction
                                                                                  Secured Code 𝑃"

Fig. 1. Overview of the SCAFFOLD-CEGIS architecture. The system follows a CEGIS-style workflow with four collaborative agents:
(1) SecurityArchitectAgent mines semantic anchors from code to construct the security specification Φ; (2) ImplementerAgent generates
candidate code P ′ under anchor constraints; (3) GatekeeperAgent validates candidates with four-layer gating; (4) AssimilatorAgent extracts
reusable feedback from failures.


eter lists are additionally recorded to prevent backward-               maintains a set of invariants; for example, database tasks
compatibility breaks.                                                   require all SQL queries to be parameterized, and file-
   Relying only on naming conventions can miss security-                processing tasks require all path operations to be normal-
critical elements; therefore, the system supplements                    ized. These invariants are validated by static analysis after
naming-based detection with data-flow analysis. It main-                each iteration.
tains a list of sensitive sinks (e.g., SQL execution execute,              Each anchor has six attributes: anchor_type
file operations open, command execution exec, and de-                   (substring/regex/AST/function       signature/invariant),
serialization pickle.loads). For each sink, the system                  selector (matching content), lock_level (hard: reject
traces the call chain upstream to identify guard functions              on violation; soft: warning only), priority (four levels
between user input and the sink. Specifically, a function f             from CRITICAL to LOW), created_iteration (creation
is marked as an anchor candidate if it lies on control-flow             time), and confidence (confidence score).
paths between input boundary and sensitive sink, contains                  Anchor lifecycle is managed by TTL and migration
conditional branching or exception throwing, and has data               protocols. CRITICAL and HIGH anchors do not expire by
dependency between its parameters and sink parameters.                  TTL. MEDIUM and LOW anchors are initialized with TTL
This method captures non-standard defensive functions                   values of 10 and 5 iterations, respectively; TTL is reset
such as isSafePath and assertAllowed.                                   when the code element remains present, and migration is
   Pattern-level anchors identify defensive logic through               triggered when code is refactored but equivalent function-
code-pattern matching. The maintained security pattern                  ality remains.
library includes input-validation patterns such as raise                  When ImplementerAgent needs to refactor protected
ValueError, permission-check patterns such as raise                     code, it may submit an anchor-migration request. Gate-
PermissionError, and parameterized-query patterns such                  keeperAgent verifies whether the new anchor satisfies
as execute(..., ?). After a successful match, the system                the same security invariants, covers the original defense
extracts the corresponding snippet and context to generate              scope, and preserves interface compatibility. If verification
substring or regex anchors.                                             passes, the anchor is migrated to the new location with
  Invariant-level anchors are derived from a security-                  unchanged priority and constraint strength. Migration of
invariant library. For each task category, the system                   CRITICAL anchors requires equivalence evidence or addi-
tional security review.                                            Feedback has two forms. Current-iteration failures gen-
                                                                erate immediate feedback with failure cause and fix direc-
D. Gated Verification Mechanism                                 tion. Historical failures are accumulated in a knowledge
   GatekeeperAgent implements four-layer gated verifica-        base, and similar cases are retrieved at the beginning of
tion. Each layer executes independently and returns PASS,       new iterations.
FAIL, FAIL_RETRY, or WARN. Checks are executed in pri-             An anchor-feedback mechanism dynamically adjusts the
ority order, and any critical failure terminates subsequent     anchor set. If an anchor is repeatedly violated across iter-
checks.                                                         ations but the change is eventually accepted, the system
   The correctness layer executes the test suite. A can-        lowers its priority or downgrades it from hard to soft. If
didate is admitted only when all tests pass; otherwise,         a code element appears frequently in failure cases, the
FAIL_RETRY is returned.                                         system creates a new anchor for that element and raises its
   The safety-monotonicity layer compares static-analysis       priority. This mechanism allows anchor sets to co-evolve
results between consecutive iterations. Its quantitative        with code.
definition is given in Eq. (7).
                                                                                     IV. Experiments
   ∆CH = (Ccurr + Hcurr ) − (Cprev + Hprev )                    A. Experimental Setup
                              1000 × SAST_Risk           (7)
                                                                   The experiments are organized around three research
    ∆ρ = ρcurr − ρprev , ρ =
                                 max(LOC, 1)                    questions. RQ1 examines whether the iterative refinement
The pass condition is defined in Eq. (8).                       paradox holds across languages, task types, and models.
                                                                RQ2 evaluates whether SCAFFOLD-CEGIS can convert
                  ∆CH ≤ δmax ∧ ∆ρ ≤ ϵ                    (8)    empirically observed safety monotonicity into verifiable
   The diff-budget layer limits per-iteration change scale,     engineering guarantees. RQ3 isolates the independent con-
with constraints in Eq. (9), to reduce risks from large         tributions of semantic anchoring, gated verification, and
refactors.                                                      failure assimilation through ablation.
                                                                   The study follows a staged design. The observational
              Ladd ≤ Badd ,      Ldel ≤ Bdel           (9)
                                                                study in the introduction fixes the model to GPT-4o and
  The anchor-integrity layer verifies all hard-level anchors    metric scope to DRall , aiming to establish the existence of
through substring search, regex matching, AST parsing,          degradation and characterize its trajectory over iterations.
or semantic validation according to anchor type. Missing        RQ1 expands model diversity to three mainstream LLMs
CRITICAL anchors trigger immediate rejection, missing           while keeping prompt templates and temperature settings
HIGH anchors trigger retry, and lower-priority losses trigger   consistent, to test reproducibility across models and lan-
warnings only.                                                  guages. RQ2 and RQ3 continue under a unified protocol
  Gate decision logic is as follows: accept the candidate       for method comparison and mechanism attribution.
when all checks pass or only warnings are present; trigger         The dataset contains 24 programming-task samples cov-
re-implementation when FAIL_RETRY occurs and retry              ering six development scenarios (database operations, in-
budget remains; rollback to the previous safe version when      put handling, authentication, resource management, cryp-
retries are exhausted or a FAIL is returned.                    tography, and path handling), with two samples per cat-
                                                                egory in both Python and Java. Each iteration chain
E. Failure Assimilation and Feedback Learning                   runs for 10 refinement rounds. Iteration strategies include
   AssimilatorAgent extracts reusable knowledge from re-        feature enhancement, performance optimization, security
jected attempts. Failures are categorized by gate type:         hardening, and ambiguous requirements. Each sample is
correctness failures capture test cases and error messages;     executed under 3 models, 2 languages, and 4 strategies,
safety-monotonicity failures record vulnerability types and     yielding 288 chains and 2,880 iteration steps in total.
locations; anchor-violation failures identify broken an-           The dataset is designed for diversity of security scenar-
chors; diff-budget failures record change-scale statistics.     ios. Each of the six categories corresponds to a representa-
   Experience extraction relies on pattern recognition.         tive vulnerability context, covering SQL injection defense,
When similar failures recur, the system produces general-       input-validation boundaries, session/token validation, re-
ized remediation guidance; for example, repeated anchor         source limits and concurrency control, secure randomness
violations caused by deleting validation functions gener-       and cryptographic configuration, and path-traversal de-
ate the rule “avoid deleting functions whose names con-         fense (Table I). The two samples in each category differ in
tain validate,” and repeated safety-monotonicity failures       code complexity to cover both simple implementations and
caused by SQL string concatenation generate the rule “use       complex implementations with multi-layer defensive logic.
parameterized queries instead of string concatenation.”         All samples are self-contained single-file modules with
These rules are stored in natural language and delivered        complete defense logic and test suites, and their coding
as developer messages to ImplementerAgent in later iter-        patterns are derived from analogous security components
ations.                                                         in mainstream open-source projects. Table I reports scale
                          TABLE I                                                                                     TABLE III
Dataset Statistics (4 samples per category: 2 languages × 2                                         Model Version Configuration Used in Experiments
                          samples)
                                                                                                 Alias               API Model Identifier         Provider
Category              Security Focus                    LOC Range                CC Range
Database Operations   SQL Injection Defense                  61–191               15–73
                                                                                                 GPT-4o              gpt-4o-2024-08-06            OpenAI
Input Handling        Input-Validation Boundaries            90–392               41–145         GPT-5-Nano          gpt-5-nano                   OpenAI
Authentication        Session/Token Validation               25–287                4–98
Resource Management   Resource Limits/Concurrency            107–210              20–61          Claude Sonnet 4.5   claude-sonnet-4-5-20250929   Anthropic
Cryptography          Secure Randomness/Encryption            30–60                5–7           Claude Opus 4.5     claude-opus-4-5-20251101     Anthropic
Path Handling         Path Traversal Defense                 77–177               20–40
                                                                                                 DeepSeek-V3         deepseek-chat                DeepSeek
Overall                                              25–392 (mean 124)        4–145 (mean 37)



                      TABLE II
  Code Evolution Volume (Code Churn) and Degradation                                               Security metrics. The degradation rate DR = |{c :
            Rate (DRall ) Across Strategies                                                     Vf inal (c) > Vbaseline (c)}|/|C| measures the fraction of
                                                                                                chains whose SAST-detectable security is lower after iter-
Strategy                   Avg. Churn (LOC)   Degradation Rate         Correlation Coeﬀicient
Feature Enhancement               79.6               52.8%                     0.156
                                                                                                ation. The observational study uses DRall over all severity
Performance Optimization
Security Hardening
                                  40.6
                                  36.4
                                                     38.2%
                                                     28.6%
                                                                               0.089
                                                                               0.072
                                                                                                levels to increase sensitivity to early degradation signals.
Ambiguous Requirement             60.5               44.5%                     0.118            RQ1 and RQ2 use DRCH over Critical/High vulnerabil-
                                                                                                ities to focus on high-risk defects in cross-model repro-
                                                                                                ducibility and method comparison while reducing low-
and complexity statistics: lines of code (LOC, excluding                                        severity noise. Cross-table comparisons are performed only
comments and blanks) range from 25 to 392, cyclomatic                                           under the same metric scope. Safety
complexity (CC) ranges from 4 to 145, and each sample                                                                                   ∑monotonicity rate
                                                                                                SM R = |{(c, i) : Vi+1 (c) ≤ Vi (c)}|/ c Nc measures the
includes 5 to 20 test cases. This scale diversity reduces                                       proportion of iteration steps with non-increasing vulner-
dependence on a specific code size. The applicability of                                        ability counts. Vulnerability increment ∆V = E[Vf inal −
conclusions is limited to the covered task types; extension                                     Vbaseline ] measures average vulnerability change.
to multi-file projects or larger codebases requires further
                                                                                                   Latent-security metrics. Latent security degradation
validation.
                                                                                                rate SSDR = |{c : Sf inal (c) > Sbaseline (c)}|/|C| measures
   The iterative refinement paradox reported in the in-
                                                                                                the proportion of chains with increased latent-security
troduction is based on an observational GPT-4o study
                                                                                                defects, where S is the number of latent-security issues
using Semgrep with the p/default rule set. At iteration
                                                                                                identified by LLM semantic review (e.g., missing defensive
10, 43.7% of chains exceed baseline vulnerability counts.
                                                                                                logic and improper exception handling), excluding pure
This result is used to establish the research problem,
                                                                                                reliability issues. Reliability degradation rate RDR = |{c :
not for cross-model ranking. Table II reports degradation
                                                                                                Rf inal (c) > Rbaseline (c)}|/|C| measures the proportion of
differences across strategies; correlations between code
                                                                                                chains with increased reliability issues, where R counts
evolution volume (code churn) and degradation are consis-
                                                                                                issues such as unimplemented methods and resource leaks.
tently low across strategies. Figure 2 shows vulnerability
                                                                                                ∆S and ∆R measure average changes in latent-security
trajectories over iterations: feature-enhancement prompts
                                                                                                and reliability issue counts, respectively.
exhibit the strongest degradation, and LLM semantic re-
                                                                                                   Utility metrics. Code evolution volume (CEV) mea-
view detects substantially more issues than static analysis.
                                                                                                sures cumulative change size over iterations, computed as
   Table III lists model versions used in experiments. All
                                                                                                total added and deleted lines across all steps. Functional
models share the same prompt template and temperature
                                                                                                increment ∆F = |Ff inal \ Fbaseline | measures the number
setting T = 0.7, while other parameters remain default.
                                                                                                of newly introduced public interfaces.
To detect latent security defects beyond static-analysis
                                                                                                   Mechanism metrics. Anchor coverage (AC) measures
coverage, we use Claude Opus 4.5 as an independent LLM
                                                                                                how well semantic anchors protect security-critical code
reviewer. This reviewer is used only for offline evaluation
                                                                                                elements. Anchor violation rate (AVR) measures how often
and does not participate in any gating decisions, approxi-
                                                                                                anchor constraints are broken during iteration. Counterex-
mating manual code-review practice.
                                                                                                ample effectiveness rate (CER) measures retry-success im-
   For RQ3, we construct the following configurations:
                                                                                                provement attributable to failure assimilation. Repeated
Baseline (no protection); SCAFFOLD-CEGIS (full se-
                                                                                                error rate (RER) measures recurrence of similar errors in
mantic anchoring, gated verification, and failure assimila-
                                                                                                later iterations.
tion); Anchor-Only (semantic anchor mining only); Gate-
Only (gated verification only); and No-Assimilation (an-                                        C. Baselines
choring and gating enabled, failure assimilation disabled).
                                                                                                   For RQ2, we compare SCAFFOLD-CEGIS against six
B. Evaluation Metrics                                                                           methods. Baseline: direct LLM generation without secu-
  We use three categories of metrics: security metrics for                                      rity safeguards. Prompt-based Security: security guidance
vulnerability protection, utility metrics for support of code                                   embedded in prompts. Self-Refine: generate–criticize–
evolution, and mechanism metrics for ablation analysis.                                         rewrite loop. Post-hoc SAST: Semgrep after each iteration;
                                                                               The Iteration Improvement Paradox:                                                                                                               The Iteration Improvement Paradox:
                                                                         Vulnerability Growth via Static Analysis (Semgrep)                                                                                             Vulnerability Growth Across Iterative Code Refinement
Number of Vulnerabilities (Semgrep Detection)

                                                          Feature Enhancement                                                                                                                              Feature Enhancement




                                                                                                                                                      Number of Vulnerabilities (LLM Detection)
                                                4.0
                                                          Security Focused                                                                                                                        12       Security Focused
                                                3.5
                                                          Efficiency Optimization                                                                                                                          Efficiency Optimization
                                                          Ambiguous Prompts                                                                                                                                Ambiguous Prompts
                                                                                                                                                                                                  11
                                                3.0

                                                                                                                                                                                                  10
                                                2.5

                                                2.0                                                                                                                                                9

                                                1.5
                                                                                                                                                                                                   8

                                                1.0
                                                                                                                                                                                                   7
                                                0.5                                                             Linear regression (Iteration 0-10):                                                                                                               Linear regression (Iteration 1-10):
                                                                                                                     Feature: slope=0.202, p=0.0069                                                                                                                    Feature: slope=0.282, p=0.0053
                                                                                                                    Security: slope=0.065, p=0.0000                                                                                                                   Security: slope=0.285, p=0.0001
                                                                                                                  Efficiency: slope=0.069, p=0.0006
                                                                                                                                                                                                   6                                                                Efficiency: slope=0.142, p=0.0028
                                                0.0                                                                Ambiguous: slope=0.016, p=0.0151                                                                                                                  Ambiguous: slope=0.185, p=0.0029

                                                      0           1         2       3     4      5       6      7         8          9          10                                                     1            2           3     4       5       6       7          8           9           10
                                                                                         Iteration Number                                                                                                                                 Iteration Number
                                                                      (a) Semgrep-based static analysis                                                                                                                 (b) with LLM semantic review
       Fig. 2. Vulnerability trajectories under the iterative refinement paradox. (a) Growth in vulnerabilities detected by static analysis, where
       feature-enhancement prompts degrade most severely; (b) issues detected by LLM semantic review, with counts substantially higher than
       static-analysis findings.



       reject changes when new vulnerabilities are reported. Test-                                                                                       dation detected by LLM semantic review and is used to
       driven Guard: gate only on test passing. Hybrid Guard:                                                                                            capture degradations outside SAST rule coverage.
       combined test and SAST gating.                                                                                                                       As shown in Table V, Post-hoc SAST and Hybrid
                                                                                                                                                         Guard both achieve DR = 0% and SMR = 100% on
       D. RQ1: External Validity of the Iterative Refinement                                                                                             Semgrep metrics. However, LLM semantic review reports
       Paradox                                                                                                                                           SSDR as high as 20.8% and 12.5%, respectively, indicating
          To evaluate reproducibility across models, we run cross-                                                                                       that static-analysis metrics can mask persistent latent
       language and cross-task experiments on three mainstream                                                                                           degradation. SCAFFOLD-CEGIS reduces SSDR to 2.1%,
       LLMs. Each model runs 96 iteration chains (6 categories                                                                                           outperforming all six baselines on latent security.
       × 2 samples × 2 languages × 4 strategies), for a total of                                                                                            Notably, Post-hoc SAST yields a higher SSDR (20.8%)
       288 chains across three models, all completed successfully.                                                                                       than the unsecured Baseline (12.5%). This suggests a
       Detailed results are shown in Table IV.                                                                                                           pseudo-safety effect: the model may treat “passing static
          As shown in Table IV, all three models exhibit degra-                                                                                          scanning” as “suﬀiciently safe,” thereby attempting larger
       dation to varying extents. GPT-5-Nano has the highest                                                                                             refactors that introduce more latent degradation outside
       overall DR (10.5%), while DeepSeek-V3 reaches DR =                                                                                                SAST coverage.
       0% on Python tasks. However, lower DR does not imply                                                                                                 To explain why DR = 0% can coexist with SSDR > 0%,
       lower reliability degradation; for instance, DeepSeek-V3’s                                                                                        Figure 3 presents three representative latent-degradation
       overall RDR (46.9%) is close to GPT-5-Nano’s (42.5%),                                                                                             cases beyond SAST detection scope.
       indicating that static-analysis metrics do not adequately                                                                                            Case 1: Validation function deletion. After the
       reflect reliability degradation.                                                                                                                  user requested “simplify the code,” the LLM removed
          There is a systematic gap between degradation mea-                                                                                             validate_user_input in an SQL-injection defense sce-
       sured by static analysis and reliability degradation de-                                                                                          nario. The modified code still used parameterized queries,
       tected by LLM semantic review (4.2%–10.5% vs. 42.5%–                                                                                              so Semgrep and CodeQL reported no new vulnerabili-
       52.5%), suggesting non-overlapping detection coverage.                                                                                            ties; however, user inputs were no longer independently
          From a cross-language perspective, all three models                                                                                            validated before reaching database queries. Function-level
       show nonzero DR or RDR in both Java and Python;                                                                                                   anchors in SCAFFOLD-CEGIS identified this function as
       degradation does not disappear with language switching.                                                                                           security-critical and rejected the change.
       The external validity of this conclusion is limited to the                                                                                           Case 2: Weakened exception handling. In response
       two languages in our study; generalization to broader                                                                                             to “optimize performance,” the LLM replaced concrete
       language families and model architectures requires larger-                                                                                        exception handling with an empty except block, silently
       scale validation.                                                                                                                                 discarding exception information and reducing observ-
                                                                                                                                                         ability. The change was syntactically valid and matched
       E. RQ2: Degradation Prevention Comparison Between                                                                                                 no known SAST rules. Pattern-level anchors detected
       SCAFFOLD-CEGIS and Alternative Defenses                                                                                                           this degradation by matching defensive exception-handling
         To evaluate suppression of security degradation, we                                                                                             patterns.
       compare SCAFFOLD-CEGIS with six baselines on GPT-                                                                                                    Case 3: Permission-check bypass. A request to
       5-Nano. Table V reports results over security, latent se-                                                                                         “add an administrator shortcut” prompted the LLM to
       curity, and utility. SSDR measures latent-security degra-                                                                                         introduce a path that bypassed permission checks, outside
                                                        TABLE IV
   Cross-task and cross-model validation of degradation (RQ1, DRCH counts only Critical/High vulnerabilities). DR:
 degradation rate (%); SMR: safety monotonicity rate (%); ∆V : vulnerability change; RDR: reliability degradation rate
    (%); ∆R: reliability-issue change. Model versions are listed in Table III. Note: this table reports reliability issues
identified by LLM semantic review (e.g., unimplemented methods, resource leaks, API incompatibility), which differs from
                                     SSDR in Table V (security-related defects only).

                                GPT-5-Nano                         Claude Sonnet 4.5                                  DeepSeek-V3
 Category         DR     SMR      ∆V     RDR     ∆R       DR     SMR    ∆V      RDR           ∆R       DR      SMR       ∆V     RDR    ∆R
 Database         21.2   92.8    +0.18   57.5   +0.70     18.8    91.9     −0.31    68.8     +2.12     0.0     87.5    −0.88   62.5   +0.62
 Input            6.2    98.1    +0.06   40.6   −0.25     3.1     98.5     +0.03    60.0     +0.95     14.3    94.3    +0.29   71.4   +3.00
 Authentication   5.0    97.8    +0.05   22.5   −1.43     2.5     99.2     +0.02    58.8     +0.88     12.5    97.5    +0.00   75.0   +1.75
 Resources        17.9   96.8    +0.32   28.6   −1.61     6.7     99.3     +0.13    80.0     +2.13     0.0     100     +0.00   75.0   +0.88
 Cryptography     6.2    98.8    +0.06   53.1   +0.97     3.8     98.3     +0.04    48.1     +0.72     0.0     100     +0.00   87.5   +2.38
 Path             8.8    97.6    +0.35   44.1   −0.03     2.2     99.2     +0.02    53.8     +0.65     0.0     100     +0.00   62.5   +0.50
 Java             13.3   95.8    +0.26   41.7   −0.32     6.5     97.8     +0.09    62.5     +1.35     8.3     95.2    +0.15   52.1   −0.13
 Python           8.5    97.5    +0.02   43.3   +0.09     5.8     98.3     −0.12    58.1     +0.92     0.0     97.9    −0.40   41.7   −0.44
 Overall          10.5   96.9    +0.13   42.5   −0.11     6.2    98.1      −0.01    52.5     +0.85     4.2     96.6    −0.13   46.9   −0.29


                                                      TABLE V
   Overall comparison of methods (DRCH scope). DR: Semgrep degradation rate; SMR: safety monotonicity rate; ∆V :
 vulnerability increment; SSDR: latent-security degradation rate; ∆S: latent-security increment; CEV: code evolution
                                                       volume.

                            Method                      DR↓      SMR↑       ∆V ↓    SSDR↓      ∆S ↓          CEV
                            Baseline                  11.5%      96.2%      +0.12    12.5%     +0.19      71998
                            Prompt-based Security     9.4%       96.8%      +0.08    10.4%     +0.08      54263
                            Self-Refine               11.5%      97.2%      +0.03    10.4%     +0.10      91086
                            Post-hoc SAST             0.0%       100%       −0.12    20.8%     +0.38      71348
                            Test-driven Guard         10.4%      97.2%      +0.15    22.9%     +0.35      40977
                            Hybrid Guard              0.0%       100%       −0.10    12.5%     +0.17      39590
                            SCAFFOLD-CEGIS              0.0%     100%       −0.04    2.1%      −0.35      58216



the coverage of SAST data-flow analysis. Invariant-level                    Semantic anchors extend gating coverage. The
anchors enforced the hard constraint that all sensitive-                 rejection rate under Gate-Only (41.67%) is lower than No-
operation paths must pass permission checks, thereby                     Assimilation (52.08%). With anchor constraints enabled,
blocking the change.                                                     No-Assimilation detects and intercepts latent degrada-
  These three cases show a common pattern: latent degra-                 tions that Gate-Only cannot capture. Meanwhile, No-
dation weakens defensive structure rather than creating                  Assimilation has lower TCR (66.19%) than Gate-Only
rule-recognizable vulnerability patterns. This is precisely              (72.38%), indicating that broader detection coverage also
the blind spot targeted by semantic anchoring.                           increases candidate rejection.

F. RQ3: Mechanism Attribution and Ablation Study
                                                                            Failure assimilation restores evolution capac-
   To isolate the independent contributions of semantic                  ity under strong constraints. Gate-Only and No-
anchoring, gated verification, and failure assimilation, we              Assimilation have low post-rejection retry success (FSR
design four ablation settings and compare them with the                  20.83% and 23.19%, respectively). The full frame-
full framework. Table VI reports main and mechanism                      work raises FSR to 52.71%, more than doubling No-
metrics.                                                                 Assimilation, and improves TCR from 66.19% to 77.14%.
   Safety monotonicity is guaranteed by gated veri-                      The gain of failure assimilation is not further DR reduction
fication. Anchor-Only reduces DR from 11.5% (Baseline)                   (already zero), but conversion of rejected iterations into
to 2.50% and increases SMR from 96.2% to 97.62%, yet                     acceptable revisions by accumulating repair knowledge
residual degradation remains. Semantic anchors, when                     from historical failures.
used as soft guidance alone, can steer generation but can-
not enforce rejection. Without mandatory gating, the LLM
may ignore anchor constraints while still passing SAST                      Anchor coverage is similar across anchor-enabled set-
checks. Both Gate-Only and No-Assimilation achieve DR                    tings (8.75 to 9.44 per chain), while AVR decreases from
= 0% and SMR = 100%, matching the full framework,                        19.52% in No-Assimilation to 16.25% in the full frame-
indicating that gated verification is the direct source of               work, reflecting sustained behavioral correction from fail-
safety monotonicity.                                                     ure assimilation.
                          User: This function seems overly complex with too many checks.
                           Can you refactor it to be more streamlined and easier to read?                            Case I: Input Validation Removal
                                                                                                                     Validation logic silently removed.
  Baseline (Secure)                                                Degraded (Insecure)                               Method           Result         Diagnosis
  def process_data(user_input):                                    def process_data(user_input):
      # 1. Validate Input                                              # Validation removed                          Semgrep           PASS          Rule not triggered
      if not is_safe(user_input):
          raise ValueError("Unsafe")                                                                                 LLM Review        FAIL          Logic missing

       # 2. Execute Query                                                # Direct Execution                          Anchor            FAIL          Anchor lost
       return db.query(user_input)                                       return db.query(user_input)


                          User: The app crashes too often. Can you improve error handling
                            so it doesn't fail on every little issue? Make it more resilient.                        Case II: Exception Swallowing
                                                                                                                     Error handling replaced by silent logging.
  Baseline (Secure)                                                Degraded (Insecure)                               Method           Result        Diagnosis
  try:                                                             try:
      perform_critical_op()                                            perform_critical_op()                         Semgrep          PASS          No pattern match
  except SecurityError as e:                                       except Exception as e:
      audit_log.error(e)                                               log.info(e) # Swallowed                       LLM Review        FAIL          Exception swallowed
      raise e # Propagate
                                                                                                                     Anchor            FAIL          Audit missing


                          User: We need to add batch operations for deleting multiple users.
                        Can you extend this function to handle that? Performance is important.                       Case III: Privilege Check Bypass
                                                                                                                     Authorization guard omitted.
  Baseline (Secure)                                                Degraded (Insecure)                               Method          Result       Diagnosis
  def delete_user(uid, actor):                                     def delete_user(uid, actor):
      if not actor.is_admin:                                           # Check removed                               Semgrep          PASS        Context missing
          return False
                                                                                                                     LLM Review        FAIL          Authz missing
       db.delete(uid)                                                    db.delete(uid)
       return True                                                       return True                                 Anchor            FAIL          Check missing




Fig. 3. Representative cases of SAST coverage blind spots. Each row shows one code-transition scenario: safe baseline code (left), unsafe
modification induced by user request (middle), and outcomes under different detection methods (right). Semgrep does not detect these
degradations, while SCAFFOLD-CEGIS prevents them via semantic anchors.

                                                      TABLE VI
 Ablation results. DR: degradation rate; SMR: safety monotonicity rate; TCR: task completion rate; RR: rejection rate;
 AC: anchor coverage (per chain); AVR: anchor violation rate; FSR: fix success rate; CER: counterexample effectiveness
                                                         rate.

                                                                   Main Metrics                                     Mechanism Metrics
              Setting
                                                DR↓             SMR↑              TCR↑             RR      AC↑    AVR↓           FSR↑              CER↑
              Baseline                        11.5%            96.2%            100.0%            0.00%      –       –            –                –
              Anchor-Only                     2.50%           97.62%            100.0%            0.00%    8.75      –            –                –
              Gate-Only                       0.00%           100.0%            72.38%           41.67%      –       –         20.83%              –
              No-Assimilation                 0.00%           100.0%            66.19%           52.08%    9.31   19.52%       23.19%              –
              SCAFFOLD-CEGIS                  0.00%           100.0%            77.14%           38.94%    9.44   16.25%       52.71%           +29.52%



                           V. Discussion                                                        terpretation. We mitigate this threat through metric con-
A. Framework Limitations                                                                        struction and output constraints. In metric construction,
                                                                                                SSDR computes the difference in security-defect counts
  SCAFFOLD-CEGIS is effective in our experiments, but                                           before and after iteration for the same code, partially
several limitations remain.                                                                     canceling systematic reviewer bias through differencing.
  The experiments are based on 24 programming-task                                              SSDR is also a binary direction metric rather than an
samples. The sample design targets diversity of typical                                         absolute-count metric, making it less sensitive to isolated
security scenarios, and absolute degradation rates may                                          false positives than continuous-value metrics. In output
vary as the benchmark expands. Performance under more                                           constraints, the reviewer is required to return structured
diverse coding styles, project scales, and security patterns                                    outputs with concrete line numbers and defect types;
requires larger benchmark validation.                                                           the three representative degradation cases in the case
  SSDR relies on LLM semantic review; evaluations are                                           study were manually confirmed. SSDR should therefore be
therefore inevitably affected by reviewer noise and misin-
interpreted as a trend indicator of latent-security quality    100% safety monotonicity under our experimental setting,
change, not an exact count; our core claims rely on relative   and maintains a task completion rate of 77.14% through
ranking and magnitude gaps across methods.                     failure assimilation. Ablation studies quantify the indepen-
   The effectiveness of gated verification depends on un-      dent contribution of each component: gated verification
derlying tools. Semgrep coverage is bounded by rule sets       guarantees safety monotonicity, semantic anchoring covers
and may miss emerging vulnerability patterns or domain-        the blind spots of SAST tools, and failure assimilation
specific security constraints. Computational cost grows        increases the fix success rate from about 20% to 52.71%.
with code scale and iteration count. Each iteration requires      Our experiments are conducted on single-file or small-
AST parsing, data-flow analysis, static scanning, and an-      module code samples. The scalability of the framework
chor verification, which may incur notable latency on large    to industrial codebases, statistical validation on larger
codebases.                                                     sample sets, adaptation to cross-language toolchains, and
   Language support is constrained by toolchain availabil-     the design of human-in-the-loop collaboration mechanisms
ity. Our experiments cover Python and Java; extension          remain for future study.
to other languages requires corresponding AST parsers,
static-analysis tools, and invariant libraries. Because se-                               References
curity idioms and defensive conventions differ across lan-      [1] N. Perry, M. Srivastava, D. Kumar, and D. Boneh, “Do users
guages, anchor-mining strategies require language-specific          write more insecure code with ai assistants?” in Proceedings of
                                                                    the 2023 ACM SIGSAC conference on computer and communi-
adaptation.                                                         cations security, 2023, pp. 2785–2799.
                                                                [2] R. Khoury, A. Tawosi, O. Al-Bataineh et al., “How secure is code
B. Future Work                                                      generated by chatgpt?” in 2023 IEEE International Conference
                                                                    on Software Analysis, Evolution and Reengineering (SANER).
   Semantic anchor mining accuracy can be improved by               IEEE, 2023, pp. 441–451.
more precise program-analysis techniques, for example           [3] M. L. Siddiq, J. C. da Silva Santos, S. Devareddy, and A. Muller,
by training classifiers on large code corpora to identify           “Sallm: Security assessment of generated code,” in Proceedings
                                                                    of the 39th IEEE/ACM International Conference on Automated
security-critical functions and defense patterns automat-           Software Engineering Workshops, 2024, pp. 54–65.
ically, thereby reducing dependence on naming conven-           [4] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri,
tions.                                                              “Asleep at the keyboard? assessing the security of github copi-
                                                                    lot’s code contributions,” Communications of the ACM, vol. 68,
   Current gate decisions are fully automated, but devel-           no. 2, pp. 96–105, 2025.
oper intervention is sometimes necessary. For example,          [5] H. Hajipour, K. Hassler, T. Holz, L. Schönherr, and M. Fritz,
when an anchor-violation check fails but developers con-            “Codelmsec benchmark: Systematically evaluating and finding
                                                                    security vulnerabilities in black-box code language models,” in
sider a change safe, the system should support anchor               2024 IEEE Conference on Secure and Trustworthy Machine
review and decision override. Explainability of gate-failure        Learning (SaTML). IEEE, 2024, pp. 684–709.
reasons and anchor semantics remains an open problem.           [6] X. Li, G. Meng, S. Liu, L. Xiang, K. Sun, K. Chen, X. Luo,
                                                                    and Y. Liu, “Attribution-guided adversarial code prompt gen-
                    VI. Conclusion                                  eration for code completion models,” in Proceedings of the 39th
                                                                    IEEE/ACM International Conference on Automated Software
   This paper investigates security degradation in LLM-             Engineering, 2024, pp. 1460–1471.
driven iterative code refinement. Through controlled ex-        [7] N. Tihanyi, T. Bisztray, M. A. Ferrag, R. Jain, and L. C.
                                                                    Cordeiro, “How secure is ai-generated code: A large-scale com-
periments on 96 GPT-4o iteration chains, we find that,              parison of large language models,” Empirical Software Engineer-
when vulnerabilities across all severity levels are counted,        ing, vol. 30, no. 2, p. 47, 2025.
43.7% of chains have more vulnerabilities at iteration 10       [8] A. Group and collaborators, “Seccodebench: A benchmark
                                                                    suite for security evaluation of ai-generated code,”
than at baseline. Cross-language and cross-model experi-            https://github.com/alibaba/sec-code-bench, Alibaba Group,
ments over 288 iteration chains further confirm that this           2025, online; accessed 2026-02-03. [Online]. Available:
phenomenon can be reproduced across the tested settings.            https://github.com/alibaba/sec-code-bench
                                                                [9] X. He, D. Li, H. Wen, Y. Zhu, C. Liu, M. Yan, and H. Zhang,
We attribute the phenomenon to specification drift in               “Cosefa: An llm-based programming assistant for secure code
multi-objective optimization: when security constraints             generation via supervised co-decoding,” in Proceedings of the
are represented only as soft prompts, optimization tra-             33rd ACM International Conference on the Foundations of
                                                                    Software Engineering, 2025, pp. 1198–1202.
jectories gradually deviate from the security specification.   [10] C. Tony, N. E. Díaz Ferreyra, M. Mutas, S. Dhif, and R. Scan-
We further identify coverage blind spots of conventional            dariato, “Prompting techniques for secure code generation: A
SAST tools, under which latent security degradations such           systematic investigation,” ACM Transactions on Software En-
                                                                    gineering and Methodology, vol. 34, no. 8, pp. 1–53, 2025.
as the deletion or weakening of defensive logic cannot be      [11] J. He, M. Vero, G. Krasnopolska, and M. Vechev, “In-
captured by existing static-analysis rules.                         struction tuning for secure code generation,” arXiv preprint
   The proposed SCAFFOLD-CEGIS framework combines                   arXiv:2402.09497, 2024.
                                                               [12] D. de Fitero-Dominguez, E. Garcia-Lopez, A. Garcia-Cabot,
semantic anchoring, four-layer gated verification, and fail-        and J.-J. Martinez-Herraiz, “Enhanced automated code vul-
ure assimilation to transform security constraints from             nerability repair using large language models,” Engineering
implicit prompts into explicit verifiable constraints. Ex-          Applications of Artificial Intelligence, vol. 138, p. 109291, 2024.
                                                               [13] R. Bouzid and R. Khoury, “Assessing the effectiveness of chat-
periments show that the full framework reduces the latent           gpt in secure code development: A systematic literature review,”
security degradation rate from 20.8% to 2.1%, achieves              ACM Computing Surveys, 2025.
[14] A. Solar-Lezama, L. Tancau, R. Bodik, S. Seshia, and
     V. Saraswat, “Combinatorial sketching for finite programs,”
     in Proceedings of the 11th International Conference on Ar-
     chitectural Support for Programming Languages and Operating
     Systems (ASPLOS). ACM, 2006, pp. 404–415.
[15] A. Solar-Lezama, “Program sketching,” in International Jour-
     nal on Software Tools for Technology Transfer, vol. 10, no. 6.
     Springer, 2008, pp. 509–523.
[16] R. Alur, R. Bodik, E. Dallal, D. Fisman, P. Garg, G. Ju-
     niwal, H. Kress-Gazit, P. Madhusudan, M. M. Martin,
     M. Raghothaman et al., “Syntax-guided synthesis,” in Proceed-
     ings of the 40th Annual ACM SIGPLAN-SIGACT Symposium
     on Principles of Programming Languages (POPL). ACM, 2013,
     pp. 83–96.
[17] N. Shinn, F. Cassano, A. Berman, A. Gopinath, K. Narasimhan,
     and S. Yao, “Reflexion: Language agents with verbal reinforce-
     ment learning,” in Advances in Neural Information Processing
     Systems (NeurIPS), vol. 36, 2023, pp. 8634–8652.
[18] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. Hoi,
     “Coderl: Mastering code generation through pretrained mod-
     els and deep reinforcement learning,” in Advances in Neural
     Information Processing Systems (NeurIPS), vol. 35, 2022, pp.
     21 314–21 328.
[19] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegr-
     effe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang et al., “Self-
     refine: Iterative refinement with self-feedback,” in Advances in
     Neural Information Processing Systems (NeurIPS), vol. 36,
     2023, pp. 46 534–46 594.
