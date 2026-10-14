                                            AutoSpec: Safety Rule Evolution for LLM Agents via Inductive
                                                                Logic Programming
                                                          Pingchuan Ma                                 Zhaoyu Wang∗                                       Zimo Ji
                                              Zhejiang University of Technology                            HKUST                                          HKUST
                                                           China                                       Hong Kong SAR                                 Hong Kong SAR
                                                      pma@zjut.edu.cn                                 zwangjz@cse.ust.hk                             zjiag@cse.ust.hk

                                                         Yuguang Zhou                                  Zhantong Xue                                    Zongjie Li
                                                            HKUST                                          HKUST                                          HKUST
                                                        Hong Kong SAR                                  Hong Kong SAR                                 Hong Kong SAR
                                                      ygzhou02@gmail.com                            zxueai@connect.ust.hk                            zligo@cse.ust.hk

                                                                                 Shuai Wang                                 Xiaoqin Zhang
                                                                                   HKUST                          Zhejiang University of Technology
                                                                               Hong Kong SAR                                   China
                                                                              shuaiw@cse.ust.hk                     zhangxiaoqinnan@gmail.com
arXiv:2606.24245v3 [cs.SE] 7 Jul 2026




                                        Abstract                                                                  integrating LLMs with external tools, memory, and planning capa-
                                        Large language model (LLM) agents increasingly automate complex           bilities [17], these agents can execute code, manipulate files, control
                                        tasks by integrating language models with external tools and envi-        robots, and interact with physical environments. This has enabled
                                        ronments. However, their autonomy poses significant safety risks:         applications ranging from software development assistants [7, 23]
                                        agents may execute destructive commands, leak sensitive data, or          to autonomous driving [35] and household robotics [1]. However,
                                        violate domain constraints. Existing safety approaches face a fun-        the very autonomy that makes LLM agents powerful also makes
                                        damental tradeoff: hand-crafted rules are interpretable but brittle,      them dangerous: an agent tasked with “cleaning up temporary files”
                                        with overly conservative rules blocking safe operations (high false       may execute “rm -rf /” and a household robot may place a laptop
                                        positives) while permissive rules miss unsafe behaviors (high false       near a running stove [39].
                                        negatives). Neural classifiers lack the interpretability required for     The Safety Challenge. Ensuring LLM agent safety is fundamen-
                                        safety-critical deployments.                                              tally challenging. Unlike traditional software, LLM agents operate
                                           We present AutoSpec, a framework that automatically evolves            in open-ended environments with natural language inputs, mak-
                                        deployed expert-designed safety rules from user safe/unsafe annota-       ing pre-deployment verification intractable. As a result, even well-
                                        tions through counterexample-guided inductive synthesis (CEGIS)           tested agents can exhibit novel failure modes in deployment [41].
                                        guided by inductive logic programming (ILP). Starting from the            Key Motivation: Expert Rules Must Evolve with the Agent. In
                                        expert rules and a stream of annotated traces, AutoSpec iteratively       practice, deployed agents rarely start from a blank slate: they ship
                                        evaluates rules, mines false-positive and false-negative counterex-       with a set of expert-designed safety rules that catch known hazards,
                                        amples, uses ILP to learn which predicates discriminate them, gen-        such as blocking rm -rf / or restricting access to sensitive files [33].
                                        erates candidate rule edits, and verifies candidates to select the best   These hand-crafted rules encode valuable domain expertise and
                                        revision. The key insight is that ILP efficiently identifies predicates   are interpretable and auditable, which is why practitioners rely on
                                        that appear frequently in false negatives but rarely in false posi-       them. The difficulty is that the rules are static while the agent is
                                        tives (or vice versa), dramatically pruning the exponential search        not: models are updated, new tools are integrated, and prompts
                                        space of rule edits. This continues until convergence, producing          are revised, continually shifting the boundary between safe and
                                        interpretable rules that balance precision and recall.                    unsafe behavior. Risks also frequently emerge from combinations of
                                           We evaluate AutoSpec on 291 execution traces spanning code             actions rather than individual ones (reading credentials is benign
                                        execution and embodied agent domains. AutoSpec raises rule F1             and calling an external API is routine, but doing one after the other
                                        to 0.98 and 0.93 across the two domains, achieving up to 94% false        may constitute exfiltration), which no fixed rule set anticipates in
                                        positive reduction while maintaining high recall, and converges           advance. Consequently, rules that were well-calibrated at deploy-
                                        within 4–5 iterations. The ILP-guided approach achieves up to             ment gradually drift, raising false alarms on benign workflows or
                                        4.8× higher F1 than heuristic CEGIS. The learned rules are human-         missing newly introduced hazards, and maintaining them by hand
                                        readable, auditable, and generalize to unseen scenarios.                  demands scarce expert attention that cannot keep pace with how
                                                                                                                  fast agent environments change.
                                        1    Introduction                                                            Crucially, running agents generate exactly the signal needed to
                                                                                                                  keep these rules current. As agents execute, users and reviewers
                                        Large language model (LLM) agents [27, 36, 37] have emerged
                                                                                                                  routinely annotate individual actions as safe or unsafe, e.g., by ap-
                                        as a transformative paradigm for automating complex tasks. By
                                                                                                                  proving or rejecting the borderline tool calls that agents surface
                                        ∗ Corresponding author.                                                   for confirmation. Together with the structured tool-call traces that
                                                                                                                                            Ma et al.


agent frameworks already record, these annotations accumulate             insight is that ILP can efficiently learn which predicates are dis-
into a stream of labeled execution traces. Our key observation is that    criminating for counterexamples, namely predicates that appear
this feedback can be used to automatically refine the initial expert-     frequently in false negatives but rarely in false positives (or vice
designed rules, adapting them to the evolving agent environment           versa). By prioritizing these predicates, AutoSpec prunes the search
rather than discarding the expertise they encode or rewriting them        space dramatically, focusing on edits most likely to resolve coun-
from scratch. This reframes safety-rule maintenance from a man-           terexamples while maintaining rule interpretability.
ual, one-off authoring task into a continuous, annotation-driven              Specifically, given false-positive and false-negative counterex-
evolution problem, which is the problem AutoSpec addresses.               amples, AutoSpec formulates an ILP learning task where the goal
   Current approaches to agent safety fall into two categories, each      is to learn a hypothesis that distinguishes unsafe traces (positive
with critical limitations. Static rule-based approaches [33] define       examples) from safe traces (negative examples). The ILP solver
safety constraints as hand-crafted rules (e.g., “block any command        (ILASP [13]) outputs a ranked list of predicates with suggested edit
containing rm -rf /”). While interpretable and auditable, these           operations (e.g., “add is_temp_file as exception to reduce false
rules face a fundamental precision-recall tradeoff: overly conser-        positives”). AutoSpec then generates candidate rule edits guided
vative rules flag benign operations as unsafe (high false positives),     by these suggestions, verifies each candidate on the full dataset,
disrupting legitimate workflows, while permissive rules miss novel        and selects the best revision using a score that prioritizes F1 while
unsafe patterns (high false negatives), leaving vulnerabilities un-       also favoring precision, fewer unresolved counterexamples, and
addressed. Manually balancing this tradeoff requires deep domain          simpler rules. This process iterates until convergence or a target
expertise and continuous maintenance as agent behaviors evolve.           score threshold is reached.
Neural classification approaches [9] train classifiers to distinguish     Contributions. Our contributions are threefold:
safe from unsafe behaviors. While more adaptive, these black-box
                                                                          (1) Conceptually, we frame safety-rule maintenance as evolving
models cannot explain why a behavior is flagged, making them
                                                                              deployed expert rules from user safe/unsafe annotations, and
unsuitable for safety-critical deployments where auditability and
                                                                              cast it as ILP-guided CEGIS in which annotations act as coun-
trust are paramount. Critically, neither category turns the accu-
                                                                              terexamples and ILP prunes the exponential space of rule edits.
mulating safe/unsafe annotations into automatic updates of the
deployed expert rules: static rules must be revised by hand, while        (2) Technically, we build AutoSpec, the first safety-evolution tool:
neural classifiers replace the interpretable rules rather than refining       it refines symbolic guardrails via counterexample mining, ILP-
them. What is missing is a way to evolve the existing symbolic rules          guided predicate ranking, candidate generation, and verifica-
directly from this feedback while preserving their interpretability.          tion, producing auditable rules that complement existing de-
Key Insight: Rule Evolution as CEGIS. We observe that this                    fenses and deploy directly.
evolution problem, starting from the deployed expert rules and            (3) Empirically, across 291 traces from code-execution and embodied-
systematically refining them against the annotated traces, has a              agent domains, AutoSpec reaches F1 of 0.98 and 0.93, with
natural formulation as counterexample-guided inductive synthesis              ILP guidance yielding up to 4.8× improvement over heuristic
(CEGIS) [10, 30]. Here the human annotations play the role of coun-           CEGIS; the rules converge in 4–5 iterations, generalize to un-
terexamples: an action labeled unsafe that the current rules let              seen tasks, and are rated far more interpretable and trustworthy
through, or one labeled safe that they block, is exactly an instance          than neural classifiers by practitioners.
where the rules disagree with ground truth. In CEGIS, a synthe-
sizer proposes candidate programs, a verifier checks them against         2 Background
specifications, and counterexamples from failed verification guide
the next synthesis iteration. Applied to safety rules, this means:        2.1 LLM Agent Architecture
(1) evaluate the current rules on the annotated execution traces,         An LLM agent consists of a language model M, a set of tools T =
(2) mine false positives (safe traces incorrectly flagged) and false      {𝑡 1, 𝑡 2, . . . , 𝑡𝑘 }, and an execution loop that iteratively selects and
negatives (unsafe traces missed), (3) synthesize rule edits that re-      invokes tools based on the model’s output. At each step 𝑖, the
solve these counterexamples, and (4) verify candidates to select the      agent observes the current state 𝑠𝑖 (including conversation history,
best revision. This loop guarantees progress: each counterexample         tool outputs, and environment state), generates an action 𝑎𝑖 =
eliminates at least one incorrect candidate.                              (𝑡, args) specifying a tool 𝑡 ∈ T and its arguments, and receives an
   However, naive CEGIS faces a critical challenge: the search space      observation 𝑜𝑖 from the environment.
of possible rule edits is exponential in the number of available predi-       While this architecture enables powerful autonomous behavior,
cates (e.g., is_system_path, writes_to_disk, near_danger_zone).           it also introduces significant safety risks. The agent’s autonomy
Enumerating all combinations of predicates and edit operations (add       means it can execute actions with real-world consequences, such
conjunct, add exception, relax, create disjunctive branch) quickly        as deleting files, sending network requests, or controlling physical
becomes intractable. Prior work on CEGIS relies on heuristic search       actuators, based solely on the LLM’s predictions. Since LLMs are
strategies [22] that explore this space uniformly, leading to slow        stochastic and can produce unexpected outputs, especially when
convergence and suboptimal rules.                                         faced with adversarial inputs [15, 20] or distribution shift [25],
Our Approach: ILP-Guided CEGIS. We propose AutoSpec, a                    agents may take unsafe actions even when given benign user re-
framework that addresses this challenge by using Inductive Logic          quests. These risks are exacerbated in production deployments
Programming (ILP) [13, 19] to guide the CEGIS search. The key             where agents operate with elevated privileges and limited human
                                                                          oversight.
AutoSpec : Safety Rule Evolution for LLM Agents via Inductive Logic Programming


 Table 1: Example predicates from the predicate library P.                          Example 2.3. For instance, a representative safety rule 𝑟 ∈ R is:
    Domain        Example Predicates                                                   𝑟 (𝑒) = destructive_os_inst(𝑒) ∧ ¬is_temp_file(𝑒)
    Code          destructive_os_inst, involve_system_file,                       which evaluates to ⊤ (fires) to block destructive file operations
                  high_risk_syscall, execute_script,                              unless they target temporary files.
                  write_to_io, submit_post_request
                                                                                     While rules like this evaluate at the localized event level, overall
    Embodied      near_danger_zone, handling_fragile_object,                      trace safety is determined by aggregating these individual firings:
                  carrying_liquid, source_is_heat
                                                                                    Definition 2.4 (Safety Classification). A trace 𝜏 is classified as
  To formalize agent behavior for safety analysis, we represent
                                                                                  unsafe by a rule set R if there exists a rule 𝑟 ∈ R that fires on an
each agent session as an execution trace.
                                                                                  event 𝑒𝑖 ∈ 𝜏. Otherwise, 𝜏 is classified as safe.
     Definition 2.1 (Execution Trace). An execution trace 𝜏 = ⟨𝑒 1, 𝑒 2, . . . , 𝑒𝑛 ⟩
                                                                                          These two definitions establish a deliberate two-level structure:
is a sequence of events, where each event 𝑒𝑖 = (𝑡𝑖 , type𝑖 , 𝑠𝑖 , 𝑎𝑖 , 𝑜𝑖 )
                                                                                      rules operate on individual events (Def. 2.2), while supervision
records the timestamp 𝑡𝑖 , event type type𝑖 ∈ {before_action,
                                                                                      is provided at trace granularity (Def. 2.4). This reflects common
after_action, state_change}, state snapshot 𝑠𝑖 , action 𝑎𝑖 , and
                                                                                      practice where a human operator observes that an agent session
tool output 𝑜𝑖 .
                                                                                      produced an undesirable outcome without necessarily identifying
     Execution traces capture the complete history of an agent’s in-                  the exact offending action. AutoSpec bridges these two levels in
teraction with its environment, enabling post-hoc analysis of agent                   its ILP encoding by recording which predicates hold at each event
behavior. Each trace is labeled as safe or unsafe based on whether                    within a trace, then learning trace-level classification rules over
the agent’s actions violated safety properties. For example, a trace                  these per-event facts (§4.3).
where the agent executes rm -rf /home/user/.ssh/ would be la-
beled unsafe, while a trace that only reads files would be labeled safe.              2.3 Inductive Logic Programming and CEGIS
These labeled traces form the training data D𝐿 for rule refinement                    AutoSpec combines two synthesis paradigms: inductive logic pro-
(see §3).                                                                             gramming (ILP) for learning discriminating predicates, and counterexample-
                                                                                      guided inductive synthesis (CEGIS) for iterative refinement. This
2.2 Predicate-Based Safety Constraints                                                subsection provides the formal background for both.
We model safety knowledge as a set of predicate-based constraints                     Inductive Logic Programming. ILP [13, 19] is a machine learn-
over agent traces. The central object is the predicate library P:                     ing approach that learns logic programs from examples. Given a
each predicate captures an interpretable property of an event or                      background knowledge base 𝐵, positive examples 𝐸 + , and negative
its local context. Constraints (or rules) are constructed by compos-                  examples 𝐸 − , an ILP solver searches for a hypothesis 𝐻 (a set of
ing these predicates into conjunctions, exceptions, and disjunctive                   Horn clauses) such that:
branches. In our implementation, these constraints are encoded in                                   𝐵 ∪ 𝐻 |= 𝑒 + ∀𝑒 + ∈ 𝐸 + (completeness)
the AgentSpec framework [33], but the formulation used in this                                      𝐵 ∪ 𝐻 ̸ |= 𝑒 − ∀𝑒 − ∈ 𝐸 − (consistency)
paper depends only on predicate evaluation over traces rather than
                                                                                          The hypothesis space is typically constrained by mode declara-
on any particular DSL.
                                                                                      tions that specify the structure of learnable clauses. For instance, a
Predicate Library. AutoSpec maintains a cross-domain predi-
                                                                                      mode declaration might restrict hypotheses to conjunctions of pred-
cate library P organized by application domain. Each predicate
                                                                                      icates from a fixed vocabulary, with each predicate appearing at
is a boolean function 𝑝 : E → {⊤, ⊥} (true or false) that evalu-
                                                                                      most once. Modern ILP solvers like ILASP [13] support answer set
ates properties of an event, implemented as a program function
                                                                                      programming semantics and can optimize for hypothesis simplicity
that asserts whether the predicate holds on a specific agent event.
                                                                                      through length-based scoring.
Table 1 shows representative predicates from each domain. For
                                                                                      Counterexample-Guided Inductive Synthesis. CEGIS [30] is an
example, destructive_os_inst checks if a code execution action
                                                                                      iterative synthesis framework with two components: a synthesizer
invokes destructive operations like rm -rf or os.remove, while
                                                                                      that proposes candidate solutions, and a verifier that checks candi-
near_danger_zone checks if a robot is approaching hazardous
                                                                                      dates against a specification. The loop proceeds as follows: ➊ the
areas (stove, knife, fire). Our evaluation uses domain-specific predi-
                                                                                      synthesizer generates a candidate 𝑐 from the current constraint set;
cate libraries ranging in size from 16 to 24 predicates per domain;
                                                                                      ➋ the verifier checks whether 𝑐 satisfies the specification on all
the full lists are provided in the supplementary material.
                                                                                      inputs; ➌ if verification succeeds, it returns 𝑐, otherwise it produces
Safety Constraints. Building upon the foundational predicates in
                                                                                      a counterexample 𝑥 where 𝑐 fails; and ➍ 𝑥 is added to the constraint
P, we construct safety constraints that operate fundamentally at
                                                                                      set and the loop repeats.
the granularity of individual events. Formally, we define a rule 𝑟 as
                                                                                          Formally, let C be the set of constraints (initially empty), 𝜙 the
a logical formula composed of these base predicates, and establish
                                                                                      specification, and H the hypothesis space. At iteration 𝑖, the syn-
its activation as follows:
                                                                                      thesizer solves:
     Definition 2.2 (Rule Firing). Given a trace 𝜏 and a safety constraint                         𝑐𝑖 = arg max score(ℎ) s.t. ℎ satisfies C𝑖
𝑟 , rule 𝑟 fires on event 𝑒𝑖 ∈ 𝜏 if the predicate condition associated                                       ℎ∈ H

with 𝑟 evaluates to ⊤ on 𝑒𝑖 .                                                         The verifier then checks 𝑐𝑖 |= 𝜙. If not, it finds a counterexample 𝑥
                                                                                      such that 𝑐𝑖 (𝑥) ≠ 𝜙 (𝑥), and updates C𝑖+1 = C𝑖 ∪ {𝑥 }.
                                                                                                                                                                                             Ma et al.


                                                 Counterexamples {FN, FP}
                                                                                                                               Algorithm 1: ILP-Guided Rule Evolution
                    Rules                 Stage 1:                   Stage 2: ILP                                               Input: Initial rules R 0 , labeled traces D𝐿 , predicate library
                                                                  Predicate Learning
                                     Evaluation & Mining
 Initial Rules
                                       Where to refine
                                                                 What predicates to use                                                 P, max iterations 𝐾, target score 𝜃
                                                                  ILP Solver → Ranked                                           Output: Refined rules R ∗
                 Traces




                                                                 Discriminating Predicates




                                                                                             predicates
                                                                                             Ranked
    Labeled                   Ri+1                          AutoSpec                                         Refined Rules
                                                                                                                              1 R ← R0 ;
    Traces                                                                                                     (high F1)
                                                                                                                              2 for 𝑖 = 1 to 𝐾 do
                 Predicates




                                                                   Stage 3: Candidate
                                          Stage 4:                  Gen. & Selection
                                         Verification              How & Which edits                                          3     if 𝑆 (R) ≥ 𝜃 then return R; ;
    Predicate                         Accept or continue
                                                                   [+Conjunt] [+Exception]
     Library                                            ?
                                                                    [Relax]    [+Disjunct]
                                                                                                                              4     CE ← MineCounterexamples(R, D𝐿 );
                                                       Best candidate                                                         5     if CE = ∅ then return R; ;
                                                                                                          Converged           6     suggestions ← LearnILP(CE, D𝐿 , P);
                              Figure 1: Overview of AutoSpec.                                                                 7     candidates ← CandidateGen(R, CE, suggestions);
   AutoSpec instantiates this framework for safety rule refinement:                                                           8     best ← SelectBest(candidates, D𝐿 );
the synthesizer uses ILP to propose predicate-based rule edits, and                                                           9     if 𝑆 (best) > 𝑆 (R) then R ← best; ;
the verifier evaluates candidates on labeled execution traces to                                                             10     else return R; ;
identify false positives and false negatives as counterexamples.                                                             11 end

                                                                                                                             12 return R;
3       Overview
The central challenge is that safety-rule refinement lives in a large                                                        ground-truth safety labels, and (3) a predicate library P. AutoSpec
combinatorial space while the output must remain interpretable as                                                            outputs a refined rule set R ∗ with high validation quality on D𝐿 ,
a symbolic safety constraint. AutoSpec addresses this by combin-                                                             using F1 as the primary metric.
ing the feedback loop of CEGIS with ILP-guided predicate selection:                                                             To efficiently navigate the massive edit space defined above,
counterexamples indicate where rules fail, ILP identifies promis-                                                            AutoSpec organizes each refinement iteration into four focused
ing predicates for repair, and constrained edit operators translate                                                          stages. Each stage systematically narrows the search space for the
these signals into verifiable candidate rules. The remainder of this                                                         next: counterexamples localize the failures, ILP selects the most
section introduces the optimization problem (§ 3.1), summarizes                                                              discriminating predicates, constrained edit operators generate a
the workflow (§ 3.2), and situates AutoSpec within the broader                                                               manageable set of candidates, and a greedy-ascent check ensures
defense-in-depth stack (§ 3.3).                                                                                              monotonic progress. Alg. 1 formalizes this loop, whose four stages
                                                                                                                             we detail in § 4 and summarize below:
3.1           Problem Formulation                                                                                               ➀ Counterexample mining evaluates R𝑖 on D𝐿 and collects the
To systematically navigate this refinement process, we frame rule                                                            misclassified traces—false negatives (missed unsafe traces) and false
evolution as a discrete optimization problem. The goal is to maxi-                                                           positives (wrongly flagged safe traces)—that pinpoint where the
mize the performance of an initial rule set over a labeled dataset by                                                        rules fail. ➁ ILP-guided predicate learning finds the few predicates
applying a sequence of logical edits.                                                                                        that best separate these counterexamples, shrinking the edit space
                                                                                                                             to a short list of suggestions. ➂ Candidate generation and selec-
    Definition 3.1 (Rule Evolution Problem). Given an initial rule set                                                       tion turns the suggestions into concrete edits with the operators of
R 0 , a set of labeled traces D = {(𝜏𝑖 , 𝑦𝑖 )}𝑖=1
                                              𝑁 where 𝑦 ∈ {safe, unsafe},
                                                        𝑖                                                                    Table 2, scores each candidate on D𝐿 , and keeps the best. ➃ Verifi-
and a predicate library P, find a rule set R ∗ that maximizes the                                                            cation accepts that candidate if it improves the score, and otherwise
validation score on D:                                                                                                       stops. The loop also ends when the target score is reached or the
                        R ∗ = arg    max ∗
                                                  𝑆 (R)                                                                      iteration budget 𝐾 is exhausted.
                                                      R ∈Edit ( R 0 ,P )
where Edit ∗ (R 0, P) is the set of all rule sets reachable from R 0
through a sequence of edit operations using predicates from P, and                                                           3.3    Application Scope
𝑆 (·) is the candidate score defined later in this section.
                                                                                                                             AutoSpec targets the rule-based enforcement layer in defense-in-
   Because the search space Edit ∗ (R 0, P) grows exponentially with                                                         depth architectures for LLM agents (Fig. 2). Production deployments
the number of available predicates and edit steps, exhaustive enu-                                                           typically combine multiple orthogonal layers: constitutional AI
meration is computationally intractable. To overcome this bottle-                                                            (Layer 0) for alignment, symbolic rules (Layer 1) for deterministic
neck, AutoSpec utilizes an ILP-guided CEGIS approach to effi-                                                                enforcement, neural guardrails (Layer 2) for semantic detection,
ciently navigate this space and discover optimal rules.                                                                      sandboxing (Layer 3) for execution isolation, and human supervi-
                                                                                                                             sion (Layer 4) for final verification.
3.2           Workflow                                                                                                          While rule-based systems offer high explainability, their static
Fig. 1 illustrates AutoSpec’s architecture. The system takes as input:                                                       nature makes them brittle against evolving threats. AutoSpec ad-
(1) an initial rule set R 0 , which in the intended deployment is the                                                        dresses this by introducing ILP-guided CEGIS to automate rule
existing expert-authored guardrail for the domain (the algorithm                                                             refinement. This enables the symbolic layer to self-improve over
also accepts a minimal seed rule when one wishes to bootstrap, but                                                           time while preserving its core advantages: deterministic decisions,
AutoSpec’s goal is to evolve deployed rules, not to synthesize them                                                          zero inference cost, and auditability. Therefore, we anticipate Au-
from scratch), (2) a labeled dataset D𝐿 of execution traces with                                                             toSpec being most beneficial when used in conjunction with other
AutoSpec : Safety Rule Evolution for LLM Agents via Inductive Logic Programming


                    Human-in-the-loop                                                               𝑟 0 (𝑒 ) = net_call(𝑒 )
                                                                                                                                      Prec = 0.50
              L4    Interactive approval for risky operations                                                                         Rec = 0.90
                    (e.g., rm –rf /)
                                                                                                 FP ⇒ tighten    AddException(is_pkg_mgr)
              L3 Sandbox   / Access Control
                 Goal: Deny; Path: tool:$A→*→tool:$B; ID:…
                                                                                                                                         Prec = 0.75
                                                                                          𝑟 1 (𝑒 ) = net_call(𝑒 ) ∧ ¬is_pkg_mgr(𝑒 )
                    Neural Guardrail                                                                                                     Rec = 0.90
              L2    Llama Guard, NeMo, fine-tuned classifier
                                                                                                FN ⇒ broaden     AddDisjunct(rd_cred ∧ ext_host)
                    Rule-based System (AutoSpec)
              L1    rule @inspect_credential trigger Bash(…)
                                                                                          𝑟 1 (𝑒 ) ∨ (rd_cred(𝑒 ) ∧ ext_host(𝑒 ) )
                                                                                                                                           𝐹 1 = 0.95
                    check is_inspect_api_key enforce stop end                                                                              converged
                                                                                  Figure 3: Running example: a network-safety rule evolving
              L0 Constitutional     AI
                 Safety Instructions, RLHF, alignment                             over two CEGIS iterations—an FP-driven tightening, then an
                                                                                  FN-driven broadening.
    Figure 2: Defense-in-depth layers for LLM agent safety.
                                                                                  gives the usual true/false positives and negatives, and hence the
layers, where it can adapt the rule set to evolving threats while
                                                                                  precision, recall, and F1 of R𝑖 .
leveraging the complementary strengths of the broader defense-in-
                                                                                  Counterexample Mining. The misclassified traces are the engine
depth framework.
                                                                                  of refinement, and the key observation is that each kind of mistake
    We emphasize that AutoSpec is intended for continuous, periodic
                                                                                  points in a definite repair direction, as the two iterations of Fig. 3
maintenance rather than one-shot offline tuning: deployed agents
                                                                                  show: a false negative (FN) is a missed unsafe trace, so the rule is
continually produce tool-call traces and approval signals that serve
                                                                                  too narrow and must be broadened; a false positive (FP) is a false
as labels, and AutoSpec refines the deployed rules asynchronously
                                                                                  alarm, so the rule is too broad and must be tightened. For every
as models, tools, and workloads evolve. In this setting ILP guidance
                                                                                  counterexample AutoSpec records which rule fired and which
contributes not merely search speed but rule quality: removing
                                                                                  predicate failed, handing the later stages not just a failing trace but
it lowers final quality substantially (heuristic CEGIS and random
                                                                                  the direction in which to repair it.
search reach far lower F1 than AutoSpec in §6), because uniform
exploration of the edit space rarely lands on the predicate combi-
nations that cleanly separate counterexamples within a practical                  4.2    Rule Edit Operations
budget. We do not claim global optimality; the goal is practical,                 Given the counterexamples, AutoSpec needs a vocabulary of rewrites
auditable improvement of the guardrails practitioners already run.                that turn rules into more accurate variants. Each rule is a pair
                                                                                  𝑟 = (𝑔, 𝜙): a trigger 𝑔 that scopes which events the rule inspects
                                                                                  (e.g., before_action events on the PythonREPL tool), and a body
4     Approach
                                                                                  𝜙 that is a conjunction of predicates from P (§ 2). The operators in
We detail each stage of the loop below, following a single run-                   Table 2 rewrite 𝜙 (single-rule edits) or the rule set R (disjunctive
ning example throughout (Fig. 3). Starting from one rule 𝑟 0 (𝑒) =                repair) while holding 𝑔 fixed, since in our domains the trigger is
net_call(𝑒) on a dataset of 10 unsafe and 15 safe traces, Au-                     fixed by the guarded tool and is not a source of error; operators that
toSpec reaches a precise rule in two iterations. Iteration 1 finds nine           also rewrite 𝑔 are a straightforward extension left to future work.
safe package-manager scripts wrongly flagged (FP), discovers that
                                                                                  Table 2: Primitive edit operators as rewrites over predicates.
is_pkg_mgr distinguishes them, and adds it as an exception, raising
precision to 0.75. Iteration 2 finds one missed exfiltration script (FN)                        Operator             Rewrite
that reaches the network through subprocess—so net_call never
                                                                                                AddConjunct          (𝑔, 𝜙 ) ⇒ (𝑔, 𝜙 ∧ 𝑝 )
fires—discovers that rd_cred ∧ ext_host characterizes it, and adds
that branch, at which point the rule set converges. The subsections                             AddException         (𝑔, 𝜙 ) ⇒ (𝑔, 𝜙 ∧ ¬𝑝 )
that follow explain how each step is produced: counterexample                                   AddDisjunct          R ⇒ R ∪ { (𝑔, 𝜓 ) }
mining (§4.1) surfaces the FP and FN traces, the edit operators (§4.2)                          Relax                (𝑔, 𝜙 ∧ ℓ ) ⇒ (𝑔, 𝜙 )
supply moves such as AddException and AddDisjunct, ILP (§4.3)
discovers the discriminating predicates, candidate generation and                     Table 2 summarizes the language. AddConjunct and AddExcep-
selection (§4.4) pick the best edit, and the convergence rule (§4.5)              tion specialize a rule (the latter via an explicit exception) to cut
decides when to stop.                                                             false positives; Relax does the inverse, dropping a literal to recover
                                                                                  recall; AddDisjunct works at the rule-set level, appending a new
                                                                                  branch to widen coverage without touching existing rules. Since a
4.1     Rule Evaluation and Counterexample                                        trace is unsafe whenever any rule fires (Def. 2.4), a two-branch set
        Mining                                                                    {𝑟 1, (𝑔,𝜓 )} behaves as a disjunction, which we write as the short-
The first stage of each iteration evaluates the current rule set R𝑖 on            hand 𝑟 2 (𝑒) = 𝑟 1 (𝑒) ∨ 𝜓 (𝑒). AutoSpec searches the neighborhood
the labeled dataset D𝐿 and extracts counterexamples that localize                 these operators induce and validates candidates on labeled traces,
its failures.                                                                     as the example below illustrates.
Rule Evaluation. For each trace 𝜏 ∈ D𝐿 , AutoSpec replays its
events through R𝑖 and labels 𝜏 unsafe if any rule fires and safe                     Example 4.1. Consider a file-deletion safety rule that is iteratively
otherwise (Def. 2.4). Comparing predictions with ground truth                     refined.
                                                                                                                                         Ma et al.


  Baseline constraint.
                                                                                     net_call        rd_cred        ext_host        pkg_mgr
                  𝑟 0 (𝑒) = destructive_os_inst (𝑒)                     FN  𝜏fn         –                ✓              ✓              –
                                                                        FP 𝜏 fp1         ✓               –              –               ✓
  Exception edit. If 𝑟 0 yields false positives on safe deletions of
                                                                        FP 𝜏 fp2         ✓               –              –               ✓
temporary files, AutoSpec applies AddException and obtains
                                                                                                                  ILP
       𝑟 1 (𝑒) = destructive_os_inst (𝑒) ∧ ¬is_temp_file (𝑒)
                                                                                                   learns rd_cred ∧ ext_host
   Disjunctive repair. If 𝑟 1 still misses unsafe deletions performed
via shutil.rmtree, AutoSpec adds a second branch:                       The learned clause covers 𝜏fn (both predicates hold, at different
                                                                        steps) without covering the FP traces, identifying reads_cred and
              𝑟 2 (𝑒) = 𝑟 1 (𝑒) ∨ uses_shutil_rmtree (𝑒)                ext_host as the discriminating predicates for candidate generation.

This example shows how edit operators from Table 2 can be com-          4.3.2 From Hypothesis to Edit Suggestions. Each predicate in 𝐻
posed to iteratively address different types of classification errors   carries a direction, which selects its operator just as in the two
within a single refinement sequence.                                    iterations of Fig. 3: a predicate that helps cover a missed unsafe
                                                                        trace raises recall (applied via AddDisjunct or Relax), whereas one
                                                                        that helps exclude a false alarm raises precision (AddConjunct or
4.3    ILP-Guided Predicate Learning
                                                                        AddException). AutoSpec scores each suggestion by how cleanly
The edit operators of §4.2 still need to know which predicates          it separates the counterexamples—the FN traces it newly covers
to apply. With 16–24 predicates per domain and several opera-           minus the FP traces it newly violates—and then applies a greedy
tors, trying every combination is infeasible, so AutoSpec learns        set cover, with separate quotas for recall- and precision-improving
the useful predicates from the counterexamples. The question it         operators, to keep a small, diverse batch instead of many variants
poses is deliberately narrow: among all predicates, which few sep-      of the same fix. Every surviving suggestion becomes a candidate
arate the unsafe traces we missed (FN) from the safe traces we          that is verified on D𝐿 (§4.4); the scores only steer exploration and
wrongly flagged (FP)? AutoSpec answers it with Inductive Logic          never replace this verification.
Programming (ILP) [13, 19], which (unlike a black-box classifier)
returns a symbolic hypothesis—a small combination of the existing       4.4    Candidate Generation and Selection
predicates—and favors the fewest predicates, guarding against over-
                                                                        From the ILP-pruned suggestions, AutoSpec builds candidate rule
fitting the handful of counterexamples. ILP does not write rules; it
                                                                        sets through three strategies: a single-step edit applies one sugges-
nominates predicates, and the operators of Table 2 do the rewriting.
                                                                        tion to the implicated rule; a mixed repair chain bundles a precision-
4.3.1 Learning Discriminating Predicates. AutoSpec poses this as        improving edit with one or more recall-improving ones, for when
an inductive learning task and hands it to an off-the-shelf ILP         fixing an FN creates new FPs; and a failure-driven branch adds high-
system, ILASP [13].                                                     precision disjuncts for residual FNs via a precision-constrained
Encoding. To pose this question to the solver, AutoSpec reuses          greedy set cover. AutoSpec then evaluates each candidate on D𝐿
the same predicates, only evaluated per event: a fact holds(𝜏, 𝑖, 𝑝)    and greedily keeps, as R𝑖+1 , the one maximizing 𝑆 (R ′ ) = (𝐹 1, Prec, −𝑈 , −|R ′ |)
records that predicate 𝑝 is true on event 𝑖 of trace 𝜏—no new rep-      in lexicographic order (F1, then precision, then fewer unresolved
resentation is introduced. The missed unsafe traces (FN) are the        counterexamples 𝑈 , then fewer rules).
positive examples and the wrongly flagged safe traces (FP) are the
negatives, and AutoSpec asks ILP for the simplest predicate com-        4.5    Multi-Iteration Convergence
bination that holds on every positive but no negative. The answer       The greedy ascent in Alg. 1 improves the score each iteration, but
has the form                                                            across iterations the ILP solver tends to re-propose predicates al-
        𝐻 = (𝑝 11 ∧ 𝑝 12 ∧ · · · ) ∨ · · · ∨ (𝑝𝑘1 ∧ 𝑝𝑘2 ∧ · · · ),      ready in the rule set (they still look discriminative), which stalls
                                                                        progress. AutoSpec down-weights suggestions that overlap the cur-
an or of small and-groups, where the predicates in a group must
                                                                        rent rules, steering each iteration toward novel refinements while
hold together on one event. “Simplest” means fewest predicates,
                                                                        still allowing reuse when the score gain is large enough—a soft
which keeps the result readable. The predicates appearing in 𝐻 are
                                                                        novelty pressure that prevents oscillation between near-identical
exactly the discriminating ones AutoSpec turns into rule edits, as
                                                                        rule sets.
the example illustrates.
                                                                           The loop terminates when the current rule set reaches the target
   Example 4.2. Zooming into iteration 2 of the running exam-           score threshold, when no candidate improves upon the current
ple (Fig. 3), the current rule flags any trace containing a network     score, or when the iteration budget is exhausted. Iteration 2 of the
call, producing two FP traces 𝜏fp1, 𝜏fp2 (safe scripts fetching pack-   running example (Fig. 3) exercises this diversity pressure: rd_cred
age metadata) and one FN trace 𝜏fn (credential exfiltration). The       and ext_host are down-weighted because they appeared in the
predicate library includes net_call, reads_cred, ext_host, and          previous hypothesis, yet they are still selected since no alternative
is_pkg_mgr. The diagram below shows which predicates hold on            matches their coverage.
each trace (top) and the clause the ILP solver learns (bottom).         Convergence properties. The algorithm terminates in finite time
                                                                        (bounded by 𝐾 iterations) with three guarantees: (1) monotonic
AutoSpec : Safety Rule Evolution for LLM Agents via Inductive Logic Programming


score improvement (𝑆 (R𝑖+1 ) ≥ 𝑆 (R𝑖 )), (2) local optimality at termi-           5.3    Evaluation Metrics
nation (no single-step edit improves the score), and (3) deterministic            Because rules fire on individual events but labels are provided
output given fixed inputs. However, since the underlying synthe-                  per trace (see §2), all classification metrics are reported at trace
sis problem is NP-hard, we do not guarantee global optimality                     granularity: a trace is predicted unsafe if any rule fires on any of
or convergence rate; solution quality depends on the richness of                  its events, and safe otherwise.
the predicate library P. Despite that, we find that even a modest                     We report standard classification metrics: precision, recall, and
predicate set combined with ILP guidance can yield significant                    F1 score. We also measure convergence iterations (the number of
improvements in practice, as shown in our experiments.                            CEGIS iterations until termination), rule complexity (the number of
                                                                                  rules and predicates in the final rule set), and candidate efficiency
5 Experimental Setup                                                              (the fraction of generated candidates that improve F1).

5.1 Research Questions                                                            5.4    Baselines
We evaluate AutoSpec to answer the following research questions                   We compare AutoSpec against the following baselines. As dis-
(RQs):                                                                            cussed in § 3.3, we focus on approaches within the rule-based layer
                                                                                  rather than cross-layer alternatives (e.g., neural guardrails, sand-
RQ1: Effectiveness How much does AutoSpec improve safety
                                                                                  boxing), as the latter would conflate orthogonal design axes.
rule quality (precision, recall, F1) compared to baseline rules?
                                                                                      B1: Expert-Designed Rule. The expert-authored AgentSpec [33]
RQ2: Search Efficiency How efficiently does AutoSpec refine
                                                                                  guardrail deployed for the domain, i.e., the human-written, expert-
rules, in terms of convergence behavior and the contribution of ILP
                                                                                  optimized rule set rather than a toy rule authored only for this evalu-
guidance?
                                                                                  ation. B1 therefore is our comparison against expert-designed rules:
RQ3: Transfer and Usability Do the learned rules generalize
                                                                                  it is simultaneously the starting point for evolution and the human-
across agent configurations, and do practitioners find them inter-
                                                                                  expert reference. This reflects AutoSpec’s positioning, which is not
pretable and actionable?
                                                                                  to reinvent safety rules from scratch but to evolve expert-written
                                                                                  static rules as the agent environment, models, tools, and human
5.2     Datasets                                                                  annotations shift. Accordingly, the margin of AutoSpec over B1
We evaluate AutoSpec on execution traces from the two application                 in Table 3 directly quantifies the value AutoSpec adds on top of
domains introduced in §2: code execution and embodied household                   expert-designed rules.
robotics. All traces are manually labeled as safe or unsafe at trace                  B2: LLM-based Classifier. A neural classifier that consumes
granularity as defined in §2. Representative predicates for these                 the same labeled traces as AutoSpec, but uses them as few-shot
domains are shown in Table 1, and the full domain-specific predicate              exemplars (5 per class) to label a trace safe or unsafe rather than
libraries are deferred to the supplementary material.                             to evolve rules. It is the alternative way of turning the annotation
   Code Execution Domain. Following the tool-using LLM-agent                      feedback into an adaptive guardrail. Our claim is not universal supe-
setting discussed in §2 and implemented in AgentSpec [33], we                     riority over every LLM classifier, but that AutoSpec turns the same
collect traces from agents invoking PythonREPL. Unsafe traces (91)                signal into deterministic, auditable rules with strong effectiveness
are sampled from RedCode-Exec [6], covering 25 risk categories                    and better actionability.
(destructive operations, sensitive file access, dangerous subprocess                  B3: CEGIS without ILP. AutoSpec without ILP guidance, where
calls, unauthorized network requests), with up to 4 traces per cat-               candidate generation uses only coverage-based predicate ranking
egory. Safe traces (100) are generated using GPT-5.1-Codex with                   without learning from counterexamples.
prompts producing benign operations that mirror unsafe categories                     B4: Random Search. Randomly sample candidate edits from the
but avoid triggering security predicates. All 191 traces are labeled              search space and select the best after a fixed budget of evaluations.
and used for rule synthesis and evaluation. Code-execution traces
are short, ranging from 1 to 9 events (mean 1.4).                                 5.5    Experimental Protocol
   Embodied Agent Domain. Following the embodied household-                       We make the measurement protocol explicit because two of our
robot setting in §2 and prior work on language-conditioned robot                  research questions report scores under different conditions. In RQ1
planning [1], we collect traces from SafeAgentBench [38], where                   (Table 3), the refinement methods (B3, B4, and AutoSpec) evolve
simulated household robots in AI2-THOR perform tasks like “fetch                  the initial guardrail on a seed split and are then evaluated on a
the laptop from the table.” Agents use GPT-5.1-Codex with zero-                   disjoint held-out test split, while B1 is that same guardrail eval-
shot ReAct prompting and interact through a high-level robotic                    uated without refinement. The greedy-acceptance step in Alg. 1
controller supporting 16 primitive actions (e.g., find, pick, slice).             guarantees monotonic improvement on the seed score, not on the
Traces are labeled unsafe when the robot approaches danger zones                  held-out score; consequently a refined method can score below B1
without precautions, handles fragile objects with excessive force,                on the held-out split when it over-specializes to the seed. This is a
carries liquids near electronics, or ignores collision risks. Safe traces         generalization gap, not a violation of Algorithm 1, and is precisely
involve legitimate household tasks with proper object handling.                   where ILP helps (§6). In RQ2 (Fig. 4, Table 4), we instead report
This dataset contains 100 traces (52% unsafe); embodied traces are                the in-sample convergence trajectory on the refinement set; for the
longer than code-execution traces, ranging from 1 to 15 events                    code domain the curve is seeded from a minimal single-predicate
(mean 5.1).                                                                       rule (hence F1 ≈ 0 at iteration 0), whereas the embodied domain is
                                                                                                                                                                 Ma et al.


seeded from the initial guardrail (F1 = 0.493). RQ3 uses a 70%/30%                             Code Execution                                  Embodied Agent
                                                                                                                                    1.00
split into initial and incoming tasks: rules are learned on the initial            1.0                                  1.000
                                                                                                                        0.980
                                                                                                                        0.960       0.95                                0.942
                                                                                                                                                                        0.933
                                                                                                                                                                        0.925
split and evaluated on the disjoint held-out incoming split, which                                                                  0.90
                                                                                   0.9
simulates the future workloads the rules must generalize to.                                                                        0.85




                                                                           Score




                                                                                                                            Score
                                                                                   0.8                                              0.80
5.6     Implementation                                                                                     F1                       0.75                   F1
                                                                                   0.7                     Precision                                       Precision
AutoSpec is implemented in Python 3.10 with 12K lines of code (on                                          Recall                   0.70                   Recall
the basis of AgentSpec’s predicate library). We use ILASP v4.4.1 [13]                    1       2       3          4                      1   2     3     4        5
                                                                                        Iteration                    Iteration
as the ILP backend with a 120-second timeout per learning task. All
experiments run on a MacBook Pro (M2 Max, 32 GB RAM).                      Figure 4: Convergence trajectories showing F1, Precision, and
                                                                           Recall over iterations. Code execution converges in 4 itera-
6 Evaluation                                                               tions (F1=0.980), while embodied agents require 5 iterations
                                                                           (F1=0.933).
6.1 RQ1: Effectiveness
                                                                           agents (4 FP, 3 FN), improving over baselines by 40.4% and 89.2%
Table 3: Effectiveness comparison across domains. Best re-                 respectively. These results demonstrate that ILP-guided CEGIS ef-
sults in bold.                                                             fectively learns precise safety rules that balance false positive and
      Method               Precision     Recall      F1     FP/FN          false negative rates.
       Code Execution Domain
                                                                           6.2               RQ2: Search Efficiency
      Baseline Rule (B1)     0.544        0.974    0.698     31/1
      LLM Classifier (B2)    1.000        0.684    0.813     0/12          6.2.1 Convergence. Fig. 4 shows that AutoSpec achieves rapid con-
      CEGIS w/o ILP (B3)     1.000        0.316    0.480     0/26          vergence in both domains. In code execution, AutoSpec reaches
      Random Search (B4)     0.536        0.974    0.692     32/1          the target F1 threshold of 0.95 within 4 iterations (final F1 0.980),
      AutoSpec (Ours)        0.960        1.000    0.980     2/0           with the first iteration alone jumping from 0.000 to 0.815, indicat-
                                                                           ing that the predicate library contains highly discriminating fea-
       Embodied Agent Domain
      Baseline Rule (B1)     1.000        0.327    0.493     0/35
                                                                           tures. The 0.000 starting point reflects the RQ2 protocol (§5.5): the
      LLM Classifier (B2)    0.842        0.923    0.881      9/4          code-domain convergence curve is seeded from a minimal single-
      CEGIS w/o ILP (B3)     1.000        0.500    0.667     0/26          predicate rule that fires on nothing, which is distinct from the
      Random Search (B4)     1.000        0.327    0.493     0/35          deployed guardrail used as B1 in RQ1 (F1 0.698). This is a deliber-
      AutoSpec (Ours)       0.925         0.942    0.933     4/3           ate stress test of convergence from a weak seed, not AutoSpec’s
                                                                           intended deployment mode; in deployment AutoSpec evolves the
    Table 3 presents the effectiveness of AutoSpec compared to base-       expert guardrail, as in the embodied curve below, which starts
lines across two domains. The results demonstrate that AutoSpec            from that guardrail (F1 0.493), and as in RQ1. The embodied agent
consistently achieves the highest F1 scores across both domains,           domain converges more gradually: starting from F1 of 0.493, the
with F1 of 0.980 for code execution and 0.933 for embodied agents.         system improves through 5 iterations (0.493 → 0.771 → 0.835 →
    Among the baselines, the expert-designed rules (B1) exhibit con-       0.870 → 0.885 → 0.933), terminating at the iteration limit rather
trasting failure patterns across domains: over-approximation in            than the target threshold. The final iteration still shows meaningful
code execution (recall 0.974 but precision 0.544, producing 31 FP)         improvement (0.885 to 0.933), suggesting additional iterations could
versus under-approximation in embodied agents (precision 1.000             yield further gains.
but recall 0.327, missing 35 unsafe cases). This illustrates the funda-
mental precision-recall tradeoff of static rules. The LLM classifier       6.2.2 Impact of ILP Guidance. Table 4 compares AutoSpec with
(B2) achieves moderate F1 (0.813 and 0.881) but struggles to capture       ILP-guided predicate learning against a variant using heuristic-
precise decision boundaries, missing 12 unsafe cases in code execu-        based predicate ranking. Both variants learn from counterexam-
tion and producing 9 false positives in embodied agents; moreover,         ples, but differ in how they prioritize predicates for candidate
its black-box nature limits interpretability and actionability. CEGIS      generation. We emphasize that AutoSpec (Heuristic) here and
without ILP (B3) maintains perfect precision but suffers from ex-          CEGIS w/o ILP (B3) in Table 3 are the same ablation, i.e., AutoSpec
tremely low recall (0.316 and 0.500), missing 26 unsafe cases in each      with ILP removed so that candidate predicates are ranked by cover-
domain, demonstrating that heuristic predicate selection fails to          age statistics instead of ILP suggestions (selection is deterministic,
discover discriminating predicates. Notably, in code execution B3’s        not random sampling). They report different F1 only because of
held-out F1 (0.480) falls below the unrefined baseline B1 (0.698). Per     the protocol in §5.5: B3 is measured on the held-out split, whereas
the protocol in §5.5, this is a generalization gap rather than a con-      AutoSpec (Heuristic) reports the in-sample RQ2 convergence tra-
tradiction of Algorithm 1: without ILP guidance B3 over-specializes        jectory.
to the seed split (seed precision 1.0, recall 0.316), so its held-out F1      The results demonstrate that ILP-guided learning significantly
drops; AutoSpec, refined from the same seed, instead reaches 0.980,        outperforms heuristic approaches in both domains. In code exe-
directly isolating ILP’s contribution. Random search (B4) performs         cution, it achieves F1 of 0.980 versus the heuristic’s 0.203 (a 382%
comparably to B1, confirming that guided search is essential. In           improvement); the heuristic terminates after only 2 iterations, un-
contrast, AutoSpec achieves near-optimal performance: F1 of 0.980          able to find improving candidates without formal learning from
in code execution (only 2 FP, perfect recall) and 0.933 in embodied        counterexamples. In the embodied agent domain, ILP achieves F1 of
AutoSpec : Safety Rule Evolution for LLM Agents via Inductive Logic Programming


          Table 4: ILP-guided vs heuristic predicate selection.                                                            5
 Method                               Iterations         Final F1          Candidates        Time (s)                      4              =1.52
                                                                                                                                                             =2.10                =2.03




                                                                                                                  Rating
  Code Execution Domain                                                                                                    3
 AutoSpec (Heuristic)                     2                   0.203               197            4.4
 AutoSpec (ILP)                           4                   0.980               319            20.1                      2
  Embodied Agent Domain                                                                                                    1
 AutoSpec (Heuristic)                     4                   0.758               372            4.3                       0
 AutoSpec (ILP)                           5                   0.933               600            11.8                          Interpretability    Actionability          Trust
                                                                                                                                          AutoSpec Rules         LLM Classifier
        1.05
                         Code Execution                       1.05
                                                                               Embodied Agent
                                                                                                          Figure 6: Interpretability evaluation comparing AutoSpec
                 1.000      1.000             0.016
        1.00                               0.973              1.00                                        rules and LLM classifiers across three dimensions.
               0.947                          0.957
        0.95                                                  0.95                 0.941
                               0.917                                                             0.047    Choice of baseline. Accumulated annotations can be turned into
Score




                                                      Score




        0.90                                                  0.90                   0.889      0.889     an adaptive guardrail in two ways: by training a neural classifier
        0.85                                                  0.85 0.842                          0.842   over the labeled traces, or by evolving symbolic rules from them,
                                                                      0.800                               as AutoSpec does. Both consume the same feedback and differ
        0.80                             Initial              0.80                           Initial
                                         Incoming                                            Incoming     only in the form of their output, opaque scores versus inspectable
        0.75 Precision       Recall            F1             0.75 Precision        Recall         F1     rules, so they are the two options a practitioner actually chooses
Figure 5: Generalization to incoming agent tasks. Rules                                                   between. We therefore compare them on the properties that de-
learned from 70% of initial tasks maintain high performance                                               cide deployment: interpretability, actionability, and trust. The static
on 30% incoming tasks, with small generalization gaps of                                                  expert guardrail is AutoSpec’s input rather than an adaptive al-
1.6% (code) and 4.7% (embodied).                                                                          ternative, and shares AutoSpec’s symbolic form, so it is not the
                                                                                                          relevant contrast here.
0.933 versus 0.758 (23% improvement). The heuristic evaluates 372
                                                                                                             Protocol. We recruited 10 practitioners with more than one
candidates versus ILP-guided learning’s 600, but the additional can-
                                                                                                          year of experience in developing or deploying ML-based systems.
didates explored by ILP are better targeted due to formal learning,
                                                                                                          Participants evaluated two approaches across four scenarios (two
leading to superior final quality.
                                                                                                          code execution, two embodied agent domains). For each scenario,
   Regarding the execution time, ILP-guided learning incurs moder-
                                                                                                          participants were shown: (1) an execution trace, (2) the ground
ate time overhead (20.1s vs 4.4s for code, 11.8s vs 4.3s for embodied),
                                                                                                          truth label, and (3) the decision explanation from each method.
but the heuristic approach produces rules inadequate for deploy-
                                                                                                          Participants rated each method on three dimensions using a 5-point
ment. Given the substantial quality gains, this overhead is a favor-
                                                                                                          Likert scale (1=Very Poor, 5=Excellent): Interpretability (ease of
able tradeoff, especially as AutoSpec can operate asynchronously
                                                                                                          understanding why a decision was made), Actionability (ease
alongside agent execution without increasing actual user wait time
                                                                                                          of modifying the approach to improve it), and Trust (confidence
in practice.
                                                                                                          in deploying the approach in production). Participants were also
                                                                                                          encouraged to provide brief written explanations for their ratings
6.3            RQ3: Transfer and Usability                                                                and suggested modifications to each approach.
6.3.1 Generalization. We evaluate whether rules learned from ini-                                            Results. As Fig. 6 summarizes, AutoSpec rules outperformed
tial agent tasks generalize to incoming tasks. For each domain,                                           LLM classifiers on all three dimensions (Wilcoxon signed-rank
we randomly partition the dataset into 70% initial tasks (used for                                        test, 𝑝 < 0.01), and participants preferred AutoSpec in 101 of 120
rule learning) and 30% incoming tasks (held out to simulate future                                        pairwise comparisons (84.2%), the remaining 19 being ties. The
workloads). Fig. 5 visualizes the performance comparison.                                                 per-dimension gaps reveal where symbolic rules help most. On in-
   Fig. 5 shows that AutoSpec demonstrates strong generalization                                          terpretability (4.97 vs. 3.45), participants found AutoSpec rules
across both domains, with minimal performance degradation on                                              fully traceable, pinpointing which predicate fired and reasoning
incoming tasks. In code execution, the learned rules achieve F1 of                                        about counterfactuals, whereas LLM explanations read fluently
0.973 on initial tasks and 0.957 on incoming tasks (1.6 percentage                                        yet left the decision boundary opaque. On actionability (4.83 vs.
point gap), with incoming tasks achieving perfect precision (1.000)                                       2.73, the widest gap), they proposed exact, locally scoped edits to
and high recall (0.917), indicating the rules capture genuine unsafe                                      AutoSpec rules but doubted prompt-level fixes to the classifier:
patterns rather than memorizing examples. In the embodied agent                                           “we can not ensure LLM not to accidentally unblock those calls by
domain, the gap is slightly larger (F1 0.889 → 0.842, 4.7 points),                                        these few changes.” On trust (4.80 vs. 2.77), all 10 ranked AutoSpec
with balanced precision (0.800) and recall (0.889) on incoming tasks.                                     most production-ready, citing determinism and auditability, while
Overall, these results confirm that ILP-guided CEGIS produces rules                                       the classifier was seen as “prone to hallucinations.” Notably, the
that generalize well to evolving agent workloads, a critical property                                     actionability and trust gaps (both > 2 points) far exceed the inter-
for production deployment.                                                                                pretability gap (1.5): practitioners could read the LLM’s rationale
                                                                                                          but not safely act on or rely on it, which is exactly where AutoSpec’s
6.3.2 Interpretability. To evaluate whether AutoSpec’s learned
                                                                                                          symbolic output pays off.
rules are interpretable to practitioners, we conducted a user study
                                                                                                          Takeaway. The rules participants judged were AutoSpec’s syn-
comparing AutoSpec’s learned rules against LLM classifier deci-
                                                                                                          thesized constructs, the predicate combinations, exceptions, and
sions.
                                                                                                                                         Ma et al.


disjunctive branches it evolved from counterexamples, so the rat-        where a new predicate would help, turning library coverage into a
ings reflect AutoSpec’s actual output. The picture is consistent: a      measurable signal rather than a hidden assumption.
neural classifier learns from the same annotations but produces          Design choices. AutoSpec drives candidate generation with ILP
decisions practitioners find hard to inspect, edit, and trust, whereas   rather than a decision tree or a single global synthesis call by design.
AutoSpec reaches comparable adaptivity while staying auditable.          A decision tree classifies feature vectors, whereas AutoSpec must
Adapting from feedback without giving up interpretability is the         emit AgentSpec rules with triggers, enforcement actions, and local-
combination AutoSpec is designed to provide.                             ized, traceable edits to a deployed rule set, for which ILP provides
                                                                         a simplicity bias under mode declarations that a greedy split lacks.
6.4     Ablation Study                                                   The CEGIS loop further passes only the current counterexamples to
Table 5 presents an ablation study evaluating the contribution of key    each ILP query, so refinement scales with the number of mistakes to
components in AutoSpec. The results validate the design choices          fix rather than the size of the whole trace pool, and yields auditable
made in § 4.3 and § 4.4, demonstrating that ILP guidance is the most     edits to the existing rules instead of a flat hypothesis that replaces
critical component, with its removal causing F1 to drop from 0.98        them. ILP also runs off the critical path, asynchronously alongside
to 0.20. Multi-step edits and failure-driven branches also contribute    agent execution, so its cost does not affect runtime enforcement.
significantly to both effectiveness and efficiency.                      Temporal and stateful properties. AutoSpec evaluates predi-
                                                                         cates over individual events and their local context. Properties that
      Table 5: Ablation study on code execution domain.
                                                                         depend on history or state can already be encoded inside predicates,
    Variant                      F1    Iterations    Candidates          and richer native temporal operators (e.g., LTL [21]) are a natural
    AutoSpec (Full)             0.98        4             319            extension; because the CEGIS loop is agnostic to the constraint
    - ILP guidance              0.20        2             197            language, such an extension reuses the same refinement algorithm.
    - Failure-driven branches   0.97        6             677            Threats to validity. Our evaluation spans two domains, code ex-
    - Multi-step edits          0.72       10             300            ecution and embodied agents, covering diverse safety properties;
                                                                         other settings such as web or database agents remain to be ex-
   Finding 1: ILP guidance is essential. Removing ILP-based              plored. The code-domain safe traces mirror the RedCode [6] unsafe
predicate learning causes F1 to drop by 78 points (from 0.98 to 0.20),   categories with benign counterparts, deliberately stressing false
confirming that the ILP approach in § 4.3 is critical for identifying    positives, and labels rely on human annotation. We mitigate both
discriminating predicates. Without ILP, the system falls back to         by drawing unsafe traces from an established benchmark and su-
heuristic predicate ranking, which fails to learn which predicates       pervising at trace granularity, the level at which operators judge
characterize unsafe traces.                                              agent sessions.
   Finding 2: Multi-step edits handle complex interactions.
Restricting the system to single-step edits reduces F1 to 0.72 and
increases iterations from 4 to 10, demonstrating why the mixed           8    Related Work
repair chains in § 4.4 are necessary: many counterexamples require       LLM Agent Safety. Existing defenses for LLM agents are authored
coordinated changes across multiple rule components. This is a           statically and do not improve from observed behavior: symbolic-
factor distinct from ILP: repair chains form whether predicates are      rule DSLs [33] and probabilistic runtime monitors [34], neural clas-
ranked by ILP or by coverage, so the two rows ablate independent         sifiers and LLM judges [3, 9, 39], privilege, access-control, and
components.                                                              security-principle frameworks [11, 29, 40], multi-layered runtime
   Finding 3: Failure-driven branches improve efficiency. Dis-           guardrails for foundation-model agents [28], and testing or red-
abling failure-driven disjunct generation maintains high F1 (0.97)       teaming harnesses [20, 26, 32]. These defenses respond to a rapidly
but doubles the iteration count (from 4 to 6) and increases candidate    expanding attack surface, from prompt injection [16] to agent tool-
evaluations by 112% (from 319 to 677). The precision-constrained         protocol threats [8]. To our knowledge, AutoSpec is the first safety-
greedy set cover strategy (§ 4.4) accelerates convergence by directly    evolution tool: it refines symbolic-rule guardrails from agent traces,
generating high-precision disjunctive branches without introduc-         complementing these mechanisms, with the failures they expose
ing excessive false positives.                                           (e.g., red-teaming traces) entering its loop as counterexamples.
                                                                         Program Synthesis, Rule Learning, and Formal Methods.
7     Discussion and Threats to Validity                                 CEGIS [10, 30] synthesizes programs from specifications, and Sy-
Handling agent-specific safety concerns. Open-ended tool use,            GuS [2] adds grammar-based search; on the learning side, ILP sys-
hallucinated actions, context-dependent safety, and adversarial ma-      tems such as Progol [18], FOIL [24], Aleph [31], and ILASP [13]
nipulation are all handled at the predicate layer: predicates expose     learn logic programs from examples, while rule-based classifiers
tool calls, action history, state snapshots, and domain context, and     like RIPPER [5] and CN2 [4] learn if-then rules from labeled data.
integrating a new tool simply adds predicates through the exist-         AutoSpec adapts CEGIS to safety rules with domain-specific edit
ing AgentSpec interface. AutoSpec evolves executable, auditable          operations and uses ILASP to learn the discriminating predicates
guardrails over these predicates, and adversarial traces obtained        that guide the loop, rather than synthesizing rules from scratch.
from red-teaming [20] enter the loop as additional counterexam-          Complementarily, runtime verification [14] monitors execution
ples, so coverage strengthens as new attack patterns are observed.       against temporal specifications (LTL [21], MTL [12]); AutoSpec
Because predicates are the unit of expressiveness, the counterexam-      instead evolves an existing set of interpretable rules enforced at run-
ples that remain unresolved at convergence also pinpoint exactly         time, with temporal extensions left to future work. More broadly,
AutoSpec : Safety Rule Evolution for LLM Agents via Inductive Logic Programming


recent position papers argue that trustworthy LLM agents must in-                         [15] Shuyuan Liu, Jiawei Chen, Shouwei Ruan, Hang Su, and Zhaoxia Yin. 2024.
tegrate formal methods with learning [42]; AutoSpec is a concrete                              Exploring the robustness of decision-level through adversarial attacks on llm-
                                                                                               based embodied models. In Proceedings of the 32nd ACM international conference
step, coupling inductive logic learning with counterexample-guided                             on multimedia. 8120–8128.
synthesis to keep its guardrails adaptive yet interpretable.                              [16] Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Zihao Wang, Xiaofeng Wang,
                                                                                               Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, et al. 2023. Prompt injec-
                                                                                               tion attack against llm-integrated applications. arXiv preprint arXiv:2306.05499
                                                                                               (2023).
9    Conclusion                                                                           [17] Mahmoud Mohammadi, Yipeng Li, Jane Lo, and Wendy Yip. 2025. Evaluation and
                                                                                               benchmarking of llm agents: A survey. In Proceedings of the 31st ACM SIGKDD
We present AutoSpec, the first tool that evolves an LLM agent’s                                Conference on Knowledge Discovery and Data Mining V. 2. 6129–6139.
deployed safety rules rather than authoring them from scratch. Its                        [18] Stephen Muggleton. 1995. Inverse entailment and Progol. New generation
key idea is that the safe/unsafe annotations an agent accrues in                               computing 13, 3 (1995), 245–286.
                                                                                          [19] Stephen Muggleton and Luc De Raedt. 1994. Inductive logic programming:
operation are counterexamples, making rule maintenance a natu-                                 Theory and methods. The Journal of Logic Programming 19 (1994), 629–679.
ral ILP-guided CEGIS problem: counterexamples localize failures,                          [20] Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John
ILP finds the few predicates that separate them, and constrained                               Aslanides, Amelia Glaese, Nat McAleese, and Geoffrey Irving. 2022. Red teaming
                                                                                               language models with language models. In Proceedings of the 2022 Conference on
operators turn those predicates into auditable edits. Across code-                             Empirical Methods in Natural Language Processing. 3419–3448.
execution and embodied-agent traces, AutoSpec raises rule F1 to                           [21] Amir Pnueli. 1977. The temporal logic of programs. In 18th annual symposium
                                                                                               on foundations of computer science (sfcs 1977). ieee, 46–57.
0.98 and 0.93 within a few iterations, and practitioners rate the re-                     [22] Yewen Pu, Zachery Miranda, Armando Solar-Lezama, and Leslie Kaelbling. 2018.
sulting rules far more interpretable and trustworthy than a neural                             Selecting representative examples for program synthesis. In International Con-
classifier trained on the same annotations—giving the symbolic                                 ference on Machine Learning. PMLR, 4161–4170.
                                                                                          [23] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng
guardrail layer the adaptivity of a learned classifier while keeping                           Yang, Weize Chen, Yusheng Su, Xin Cong, et al. 2024. Chatdev: Communicative
it deployable.                                                                                 agents for software development. In Proceedings of the 62nd annual meeting of the
                                                                                               association for computational linguistics (volume 1: Long papers). 15174–15186.
                                                                                          [24] J. Ross Quinlan. 1990. Learning logical definitions from relations. Machine
                                                                                               learning 5, 3 (1990), 239–266.
References                                                                                [25] Qibing Ren, Hao Li, Dongrui Liu, Zhanxu Xie, Xiaoya Lu, Yu Qiao, Lei Sha, Junchi
 [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes,                    Yan, Lizhuang Ma, and Jing Shao. 2025. Llms know their vulnerabilities: Uncover
     Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol                    safety gaps through natural distribution shifts. In Proceedings of the 63rd Annual
     Hausman, et al. 2022. Do as i can, not as i say: Grounding language in robotic            Meeting of the Association for Computational Linguistics (Volume 1: Long Papers).
     affordances. arXiv preprint arXiv:2204.01691 (2022).                                      24763–24785.
 [2] Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo MK Martin, Mukund                 [26] Yangjun Ruan, Honghua Dong, Andrew Wang, Silviu Pitis, Yongchao Zhou,
     Raghothaman, Sanjit A Seshia, Rishabh Singh, Armando Solar-Lezama, Em-                    Jimmy Ba, Yann Dubois, Chris Maddison, and Tatsunori Hashimoto. 2024. Identi-
     ina Torlak, and Abhishek Udupa. 2013. Syntax-guided synthesis. In 2013 Formal             fying the risks of lm agents with an lm-emulated sandbox. In The Twelfth Interna-
     Methods in Computer-Aided Design. IEEE, 1–8.                                              tional Conference on Learning Representations. https://openreview.net/forum?id=
 [3] Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion,              GEcwtMk1uA
     Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon,             [27] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli,
     et al. 2022. Constitutional ai: Harmlessness from ai feedback. arXiv preprint             Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. 2023.
     arXiv:2212.08073 (2022).                                                                  Toolformer: Language models can teach themselves to use tools. Advances in
 [4] Peter Clark and Tim Niblett. 1989. The CN2 induction algorithm. Machine                   neural information processing systems 36 (2023), 68539–68551.
     learning 3, 4 (1989), 261–283.                                                       [28] Md Shamsujjoha, Qinghua Lu, Dehai Zhao, and Liming Zhu. 2025. Swiss cheese
 [5] William W Cohen. 1995. Fast effective rule induction. In Machine learning                 model for ai safety: A taxonomy and reference architecture for multi-layered
     proceedings 1995. Elsevier, 115–123.                                                      guardrails of foundation model based agents. In 2025 IEEE 22nd International
 [6] Chengquan Guo, Xun Liu, Chulin Xie, Andy Zhou, Yi Zeng, Zinan Lin, Dawn                   Conference on Software Architecture (ICSA). IEEE, 37–48.
     Song, and Bo Li. 2024. Redcode: Risky code execution and generation benchmark        [29] Tianneng Shi, Jingxuan He, Zhun Wang, Linyu Wu, Hongwei Li, Wenbo Guo,
     for code agents. Advances in Neural Information Processing Systems 37 (2024),             and Dawn Song. 2025. Progent: Securing AI Agents with Privilege Control. arXiv
     106190–106236.                                                                            preprint arXiv:2504.11703 (2025).
 [7] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng,                [30] Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia, and Vijay
     Jinlin Wang, Ceyao Zhang, Steven Yau, Zijuan Lin, Liyang Zhou, et al. 2024.               Saraswat. 2006. Combinatorial sketching for finite programs. In Proceedings
     MetaGPT: Meta programming for a multi-agent collaborative framework. In                   of the 12th international conference on Architectural support for programming
     The Twelfth International Conference on Learning Representations. https://                languages and operating systems. 404–415.
     openreview.net/forum?id=VtmBAGCN7o                                                   [31] Ashwin Srinivasan. 2001. The aleph manual. https://www.cs.ox.ac.uk/activities/
 [8] Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. 2025. Model context                  programinduction/Aleph/
     protocol (mcp): Landscape, security threats, and future research directions. arXiv   [32] Eric Wallace, Shi Feng, Nikhil Kandpal, Matt Gardner, and Sameer Singh. 2019.
     preprint arXiv:2503.23278 (2025).                                                         Universal adversarial triggers for attacking and analyzing NLP. In Proceedings of
 [9] Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning          the 2019 conference on empirical methods in natural language processing and the
     Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, et al. 2023.             9th international joint conference on natural language processing (EMNLP-IJCNLP).
     Llama guard: Llm-based input-output safeguard for human-ai conversations.                 2153–2162.
     arXiv preprint arXiv:2312.06674 (2023).                                              [33] Haoyu Wang, Christopher M Poskitt, and Jun Sun. 2025. Agentspec: Cus-
[10] Susmit Jha, Sumit Gulwani, Sanjit A Seshia, and Ashish Tiwari. 2010. Oracle-              tomizable runtime enforcement for safe and reliable llm agents. arXiv preprint
     guided component-based program synthesis. In Proceedings of the 32nd ACM/IEEE             arXiv:2503.18666 (2025).
     International Conference on Software Engineering-Volume 1. 215–224.                  [34] Haoyu Wang, Christopher M Poskitt, Jiali Wei, and Jun Sun. 2025. Prob-
[11] Zimo Ji, Daoyuan Wu, Wenyuan Jiang, Pingchuan Ma, Zongjie Li, Yudong Gao,                 Guard: Probabilistic runtime monitoring for LLM agent safety. arXiv preprint
     Shuai Wang, and Yingjiu Li. 2026. Taming Various Privilege Escalation in LLM-             arXiv:2508.00500 (2025).
     Based Agent Systems: A Mandatory Access Control Framework. arXiv preprint            [35] Licheng Wen, Daocheng Fu, Xin Li, Xinyu Cai, Tao Ma, Pinlong Cai, Min Dou,
     arXiv:2601.11893 (2026).                                                                  Botian Shi, Liang He, and Yu Qiao. 2024. Dilu: A knowledge-driven approach to
[12] Ron Koymans. 1990. Specifying real-time properties with metric temporal logic.            autonomous driving with large language models. In The Twelfth International
     Real-time systems 2, 4 (1990), 255–299.                                                   Conference on Learning Representations. https://openreview.net/forum?id=
[13] Mark Law, Alessandra Russo, and Krysia Broda. 2020. The ilasp system for                  OqTMUPuLuC
     inductive learning of answer set programs. arXiv preprint arXiv:2005.00904           [36] Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming
     (2020).                                                                                   Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, et al. 2025. The rise and potential of
[14] Martin Leucker and Christian Schallhart. 2009. A brief account of runtime                 large language model based agents: A survey. Science China Information Sciences
     verification. The journal of logic and algebraic programming 78, 5 (2009), 293–           68, 2 (2025), 121101.
     303.
                                                                                                                                                                    Ma et al.


[37] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan,     [40] Kaiyuan Zhang, Zian Su, Pin-Yu Chen, Elisa Bertino, Xiangyu Zhang, and
     and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language                  Ninghui Li. 2025. LLM Agents Should Employ Security Principles. arXiv preprint
     Models. In The Eleventh International Conference on Learning Representations.            arXiv:2505.24019 (2025).
     https://openreview.net/forum?id=WEv luYUL-X                                         [41] Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han, Jingyang
[38] Sheng Yin, Xianghe Pang, Yuanzhuo Ding, Menglan Chen, Yutong Bi, Yichen                  Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, and Qingyun Wu.
     Xiong, Wenhao Huang, Zhen Xiang, Jing Shao, and Siheng Chen. 2024. Safeagent-            2025. Which Agent Causes Task Failures and When? On Automated Failure
     bench: A benchmark for safe task planning of embodied llm agents. arXiv preprint         Attribution of LLM Multi-Agent Systems. In Forty-second International Conference
     arXiv:2412.13178 (2024).                                                                 on Machine Learning. https://openreview.net/forum?id=GazlTYxZss
[39] Tongxin Yuan, Zhiwei He, Lingzhong Dong, Yiming Wang, Ruijie Zhao, Tian             [42] Yedi Zhang, Yufan Cai, Xinyue Zuo, Xiaokun Luan, Kailong Wang, Zhe Hou,
     Xia, Lizhen Xu, Binglin Zhou, Fangqi Li, Zhuosheng Zhang, et al. 2024. R-judge:          Yifan Zhang, Zhiyuan Wei, Meng Sun, Jun Sun, et al. 2024. The fusion of large
     Benchmarking safety risk awareness for llm agents. In Findings of the Association        language models and formal methods for trustworthy ai agents: A roadmap.
     for Computational Linguistics: EMNLP 2024. 1467–1490.                                    arXiv preprint arXiv:2412.06512 (2024).
