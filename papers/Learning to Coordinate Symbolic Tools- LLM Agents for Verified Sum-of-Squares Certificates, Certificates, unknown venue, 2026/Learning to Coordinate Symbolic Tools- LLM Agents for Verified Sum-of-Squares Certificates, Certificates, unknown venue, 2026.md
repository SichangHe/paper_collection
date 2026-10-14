                                        Learning to Coordinate Symbolic Tools: LLM Agents for Verified Sum-of-Squares
                                                                         Certificates

                                                                         Bohan Chen∗†1 , Shivam N. Patel∗‡1 , Richard Hoffmann1 ,
                                                                                     Sam Looi§1 , Tony Yue Yu§1
                                                                                               1
                                                                                                   California Institute of Technology
                                                                                                               2
                                                                                                                 OpenAI




                                                                      Abstract                                        construct its arguments, interpret the observation, recover
                                                                                                                      from an unhelpful result, and know when to stop (Yao et al.
                                           Tool calling allows large language models (LLMs) to invoke                 2023; Li et al. 2023). These decisions are especially visi-
                                           external computation during problem solving, a useful capa-
                                           bility in various fields including AI for mathematics. We study
                                                                                                                      ble in tasks whose outputs are easy to verify but difficult to
                                           this setting through weighted sum-of-squares (SOS) decom-                  search for (Yang et al. 2023a). This leads to our central ques-
arXiv:2608.00326v2 [cs.AI] 9 Aug 2026




                                           position, a machine-checkable route to proving polynomial                  tion: Can algebra-grounded post-training enable an LLM to
                                           nonnegativity and hence polynomial inequalities. A candi-                  coordinate exact symbolic operations during multi-step sym-
                                           date decomposition can be checked exactly, but finding one                 bolic search, rather than merely execute isolated algebraic
                                           requires choosing among non-unique regroupings and coor-                   transformations?
                                           dinating multiple symbolic transformations. We develop an                     Polynomials are a foundational language for optimization
                                           agent that combines algebraic task training, symbolic tools,               and algebraic geometry. Recent developments around the Ja-
                                           and verifier-grounded optimization for this task. Rather than              cobian conjecture make their local–global subtlety especially
                                           training only on the composite SOS task, we construct 1.35                 vivid (Ramos, Hulak, and Barretto de Queiroz 2026; Tao
                                           million synthetic examples covering eight supporting poly-
                                           nomial tasks together with weighted-SOS decomposition. We
                                                                                                                      2026). The mathematical task we study is different, but the
                                           first apply supervised fine-tuning (SFT) to direct algebra prob-           episode underscores the value of exact polynomial reasoning
                                           lems and simulated symbolic traces, and then use Group Rela-               and machine-checkable witnesses. We are well-motivated in
                                           tive Policy Optimization (GRPO) with task-specific symbolic                our use of weighted SOS as a controlled setting in which
                                           rewards. The SFT corpus contains no native tool-calling mes-               discovering global structure requires search, while checking
                                           sages; at evaluation, the agent uses native SymPy calls for                a proposed identity is exact and inexpensive.
                                           expansion, collection, reordering, and factorization. Every fi-               A weighted sum-of-squares (SOS) certificate is an identity
                                           nal SOS answer is checked by exact expansion and coefficient               of the form
                                           comparison. On held-out, same-generator synthetic problems,                                      m
                                           the full SFT+GRPO+tools system is the strongest of four eval-
                                                                                                                                           X
                                                                                                                                     f=        cj p2j ,   cj ∈ Q>0 .              (1)
                                           uated configurations, reaching 78.96% verified success on
                                                                                                                                          j=1
                                           weighted SOS, compared with 44.73% for the base model
                                           with the same tools, and 91.75% macro accuracy across nine                 Such an identity proves global polynomial nonnegativity and
                                           polynomial tasks. Within this controlled setting, our work pro-            can be checked exactly by expansion. Finding such an iden-
                                           vides a case study of combining domain-specific skill training,            tity is nevertheless non-unique and strategic: expansion hides
                                           executable tools, and verifier feedback, and may inform the                square structure, mixed terms admit several plausible group-
                                           design of tool-calling agents in other domains with exactly
                                                                                                                      ings, and a locally correct transformation can leave an unus-
                                           checkable outputs.
                                                                                                                      able remainder. Symbolic tools execute a proposed operation;
                                                                                                                      they do not determine the global search path.
                                                                  Introduction                                           Figure 1 summarizes the training and deployment bound-
                                                                                                                      ary. Starting from Phi-4-reasoning-plus (Abdin
                                        Exact tools can make an individual operation reliable with-
                                                                                                                      et al. 2025), we construct a nine-task synthetic curriculum:
                                        out making an agent’s overall strategy correct. A tool-using
                                                                                                                      four local operations, four broader algebraic-structure tasks,
                                        language model must still decide which operation is useful,
                                                                                                                      and composite weighted-SOS search. We apply assistant-
                                           ∗                                                                          token QLoRA SFT (Dettmers et al. 2023) to direct problems
                                              These authors contributed equally.
                                           †                                                                          and simulated symbolic traces, then continue with GRPO
                                              Corresponding author.
                                            ‡                                                                         using task-specific symbolic rewards (Shao et al. 2024). The
                                              This work was completed while S. N. Patel was a research vis-
                                        itor at the California Institute of Technology, prior to his affiliation      SFT corpus contains evaluated Python-like symbolic snip-
                                        with OpenAI.                                                                  pets but no native function-call messages. During weighted-
                                            §
                                              These authors share senior authorship.                                  SOS evaluation, the tool-enabled systems instead interact
Figure 1: Overview of the controlled study. Algebraic post-training builds a checkpoint from eight supporting tasks and
weighted-SOS examples. During weighted-SOS evaluation, Base+Tools and Full receive the same native SymPy interface. The
complete model–harness system coordinates exact local operations, while the terminal verifier accepts only a positive-rational
weighted-SOS expression whose expansion matches the input polynomial exactly.


with four SymPy-backed functions (Meurer et al. 2017), and        2023). API-Bank and ToolLLM broaden supervised tool
every terminal certificate is checked structurally and coeffi-    learning to large API collections (Li et al. 2023; Qin et al.
cient by coefficient.                                             2024). For mathematics, ToRA trains on interactive trajecto-
   On 90,000 separately generated, same-generator test in-        ries that alternate language reasoning with computation and
stances, the complete system reaches a 91.75% macro-              symbolic solvers, while ReTool couples cold-start traces with
average across the nine polynomial tasks. On weighted             outcome-driven reinforcement learning for strategic code use
SOS—the only native tool-calling task—the Full system             (Gou et al. 2024b; Feng et al. 2026). Evaluation has likewise
reaches 78.96% verified success, compared with 44.73%             moved beyond isolated call syntax: MINT studies multi-turn
for the same base backbone with the same tool interface.          interaction with tool and language feedback, BFCL includes
The experiment is deliberately controlled: it uses small syn-     abstention and stateful multi-step use, and τ -bench scores the
thetic polynomials, one backbone, and one run per training        final environment state and repeated-trial reliability (Wang
stage. Because the evaluated configurations do not include        et al. 2024; Patil et al. 2025; Yao et al. 2025). Multi-turn stud-
SFT+Tools without GRPO or GRPO without tools, the re-             ies further show that premature assumptions can make later
sults compare complete systems rather than causally isolating     recovery unreliable (Laban et al. 2026). Our environment
individual components.                                            is narrower but more exact: the tools perform determinis-
                                                                  tic algebra, and the terminal state is a coefficient identity.
Contributions.
                                                                  CRITIC uses tools mainly to critique and revise an answer
 • An exactly verifiable agent testbed. We instantiate            (Gou et al. 2024a); here exact operations are used construc-
   symbolic-tool coordination as weighted-SOS certificate         tively throughout certificate search.
   search, supported by eight direct algebraic tasks, 1.35
   million generated examples before the validation split,
                                                                  Verifier-guided mathematical reasoning. PAL and Pro-
   and 90,000 separately generated test problems.
                                                                  gram of Thoughts delegate computation to executable pro-
 • An algebra-grounded post-training recipe. The                  grams, and ToRA makes this interaction iterative rather than
   pipeline combines assistant-token QLoRA SFT on direct          one-shot (Gao et al. 2023; Chen et al. 2023; Gou et al. 2024b).
   algebra and simulated symbolic traces, verifier-grounded       Outcome and process verifiers provide complementary su-
   GRPO, a native four-function SymPy interface for SOS,          pervision for multi-step mathematics (Cobbe et al. 2021;
   and exact terminal verification.                               Lightman et al. 2024). DeepSeekMath and ReTool use ver-
 • Complete-system evidence with calibrated scope. We             ifiable outcomes to optimize mathematical reasoning, while
   compare Base, SFT, Base+Tools, and Full on weighted            LeanDojo, DeepSeek-Prover, and AlphaProof ground search
   SOS, report direct-task checkpoint performance and ter-        in proof-assistant states checked by a formal kernel (Shao
   minal failure categories, and distinguish the empirical        et al. 2024; Yang et al. 2023b; Xin et al. 2025; Ren et al. 2025;
   findings from broader design hypotheses.                       Hubert et al. 2026). Exact behavior can nevertheless remain
                                                                  fragile under controlled numerical or contextual perturba-
                     Related Work                                 tions, or as combinatorial complexity increases (Mirzadeh
Tool-using language-model agents. Toolformer learns               et al. 2025; Shojaee et al. 2025). Although our verifier is
where to insert API calls, while ReAct interleaves reason-        less expressive than Lean, it is cheaper and deterministic by
ing, actions, and observations (Schick et al. 2023; Yao et al.    checking the submitted algebraic object rather than a natural-
language rationale.                                                coefficient by coefficient. Because every accepted summand
                                                                   is nonnegative on Rn , this identity immediately certifies
Polynomial certificates and neuro-symbolic proving.                f (a) ≥ 0 for every real input a. Acceptance is not com-
SOS and Positivstellensatz certificates connect polynomial         plete for polynomial nonnegativity, and the agent can also
nonnegativity to algebraic identities and semidefinite opti-       fail to find a certificate that exists. Every evaluation polyno-
mization (Stengle 1974; Parrilo 2003; Lasserre 2001). Learn-       mial is SOS by construction, although the model is not told
ing has been used to guide dynamic polynomial proofs               this; an exhausted or abstaining trajectory is therefore a failed
and symbolic inequality search: AIPS learns search guid-           search, not evidence that the polynomial is non-SOS.
ance, LIPS assigns scaling to symbolic routines and rewrit-
ing/ranking to an LLM, and IneqSearch searches for combi-
nations of nonnegative components (Fawzi et al. 2019; Wei,
                                                                     Certificate Search as a Sequential Decision
Sun, and Wang 2024; Li et al. 2025; Li, Liao, and Ye 2025).                           Problem
APPIRL learns certificate-basis choices, and NeuralSOS pre-        Why coordination remains nontrivial. Figure 2 separates
dicts monomial supports for an SOS optimizer (Liu et al.           local symbolic execution from global certificate search. A
2025; Pelleriti et al. 2026). AquaForte uses LLM-proposed          factorizer can verify either selected group exactly, but it
function instantiations within a soundness-preserving SMT          does not choose the grouping. A locally plausible branch
pipeline; its evaluation includes constructively generated         can therefore produce correct intermediate algebra and still
problems asking whether a polynomial is a sum of exactly           leave a remainder that does not expose a weighted square.
three squares (Lv et al. 2026). Its target is quantified-SMT       The model–harness system must revise that branch, assem-
solving rather than sequential coordination of exact algebraic     ble a complete candidate, and stop only when the terminal
tools.                                                             identity is ready for exact checking.
   Among especially close recent systems, NSPI trains a di-           At the level of the complete model–harness system,
rect SOS conjecturer using synthetic polynomial–SOS data,          weighted-SOS discovery is a finite-horizon sequential de-
SFT, and curriculum-based reinforcement learning. It then          cision problem. At step t, the interaction history ht =
applies numerical refinement and rational recovery before          (f, a<t , o<t , bt ) contains the target polynomial f , previous
Lean verification (Zuo et al. 2026). We instead study se-          actions a<t , exact symbolic observations o<t , and the re-
quential exact tool coordination without numerical repair.         maining call and attempt budget bt . The next action may be
The empirical object is therefore tool coordination in a con-      a text continuation, a native symbolic request with concrete
trolled certificate-search environment, not state-of-the-art in-   arguments, or a terminal certificate candidate. For an exe-
equality proving.                                                  cutable tool action, the backend deterministically returns an
                                                                   algebraic observation ot = T (at ). For a terminal candidate
           Verified Weighted-SOS Search                            y, success is determined by rterm (f, y) = 1[V (f,y)=1] , where
                                                                   V is the exact structural and coefficient verifier defined above.
Let R = Q[x1 , . . . , xn ] with a supplied variable order. Ta-
                                                                   The difficulty is therefore not uncertainty in local execution,
ble 2 gives the complete curriculum and test interface. The
                                                                   but delayed credit assignment over a branching search: sev-
eight supporting tasks are always solved directly, without
                                                                   eral algebraically correct calls may be strategically unhelpful,
native tool access, in both training and evaluation. Their
                                                                   and success depends on the sequence of representation, re-
purpose is algebraic supervision rather than a direct mea-
                                                                   grouping, retry, and stopping decisions made within a finite
surement of tool execution. Native function calling is used
                                                                   budget.
only for weighted-SOS search.
                                                                      This formulation motivates verifier-grounded policy opti-
Curriculum roles. The four local tasks mirror operations           mization after SFT. Valid certificates and useful action se-
available through the deployment interface, but they are           quences are non-unique, so imitating one reference trace
learned and evaluated without native calls. The four struc-        would privilege one decomposition and one sequence of
tural tasks require broader choices of representation—nested       transformations while penalizing alternative valid solutions.
variable order, symmetric bases, reduced remainders, and           Exact symbolic rewards instead allow multiple sampled re-
Bézout identities—that are not returned by a single SOS tool       sponses to be compared by the algebraic state they reach
invocation. Weighted SOS combines these capabilities into a        rather than by surface agreement with a single trajectory.
sequential search problem. This grouping motivates the de-         This is the role served by GRPO in our pipeline. The op-
scriptive family analysis in the Results section. The grouping     timization and trajectory analysis are defined at the level of
is descriptive, and per-task causal attribution is outside the     the complete model–harness system. Accordingly, trajectory-
experimental design.                                               level results characterize the system as a whole rather than
                                                                   attributing every regrouping, retry, or stopping decision to
Acceptance contract. A candidate is accepted only if it            the language model alone.
parses as a finite sum in the form of Eq. (1), every weight
is an exact positive rational number, every summand is a           Native interface and system boundary. The weighted-
polynomial square, and                                             SOS environment exposes expand_polynomial,
                                                                 collect_terms,          reorder_polynomial,           and
                              X                                    factorize_polynomial. At each turn, the composite
                expandf −        cj p2j  = 0                     inference system emits text, a schema-checked native call,
                                 j                                 or a terminal object. The harness validates JSON, enforces
 System                   Learned role                      Downstream symbolic component               Primary empirical object
 AIPS / LIPS / In-        Learned guidance, rewriting,      Symbolic transformations and inequality-    Olympiad-style algebraic inequali-
 eqSearch (Wei, Sun,      ranking, or theorem selection     proof search                                ties
 and Wang 2024; Li
 et al. 2025; Li, Liao,
 and Ye 2025)
 APPIRL (Liu et al.       Reinforcement learning for se-    Krivine-style polynomial certificate con-   Automated polynomial-inequality
 2025)                    lecting certificate bases         struction                                   proofs
 NeuralSOS (Pelleriti     Transformer prediction of an      SOS optimization and certificate check-     Learning-augmented nonnegativity
 et al. 2026)             SOS monomial support/basis        ing                                         certification
 NSPI (Zuo et al.         LLM conjecture of an approxi-     Numerical refinement, rational recovery,    Formal    multivariate     inequality
 2026)                    mate SOS structure                and Lean checking                           proving
 This work                Post-trained model–harness sys-   Exact SymPy observations and coeffi-        Training and evaluating symbolic-
                          tem coordinating native exact     cient verifier; no numerical correction     tool coordination
                          transformations

Table 1: Positioning relative to learning-based polynomial systems. The distinction is the scientific object: weighted SOS is used
as an exactly checkable environment for studying a sequential tool agent rather than as a claim of general or state-of-the-art
inequality solving.

 Task                               Curriculum role                Output / evaluation
 Tool-aligned local operations
 Lexicographic term ordering        Local normalization            Equivalent polynomial in the requested order
 Collection                         Local normalization            Expression collected in the designated variable
 Expansion                          Local execution                Fully expanded polynomial
 Factorization                      Local structure exposure       Product representation
 Broader structural algebra
 Horner form                        Structural representation      Nested form for a supplied variable order
 Symmetric reduction                Structural representation      Expression in the designated symmetric basis
 Quotient/remainder                 Polynomial reduction           Exact q, r with f = qg + r and reduced r
 Extended GCD                       Algebraic identity             Monic gcd with an exact Bézout identity
 Composite target task
 Weighted SOS                       Certificate search             Native tools followed by exact terminal verification

Table 2: Task taxonomy and curriculum roles. Dataset sizes and variable/degree ranges are reported in Appendix; detailed output
and acceptance contracts are reported in the appendix.

                                                                                                                      P           
                                                                                                                         m       2
budgets, executes valid calls exactly in SymPy, and appends              ing a scrambled expansion of f = expand         j=1 cj qj .
the returned observation. Tool-enabled configurations share              The sampled grouping is hidden. A separate seed generates
at most ten calls, at most three decomposition attempts, five            10,000 test instances per task. Because train and test share
seconds per call, and 60 seconds per episode. A terminal                 generator families, the suite measures competence within the
object is scored only by the exact certificate verifier. All             designed algebraic environment rather than natural-problem
trajectory-level results therefore characterize the complete             or out-of-distribution generalization.
model–harness system. The appendix summarizes this
responsibility split and provides the full schemas.                      Supervised fine-tuning. We apply four-bit QLoRA to
                                                                         Phi-4-reasoning-plus. System and user tokens are
          Algebra-Grounded Post-Training                                 retained as context but masked from the loss; only assis-
                                                                         tant tokens are prediction targets. Direct tasks use problem–
Synthetic curriculum. Each of the nine tasks contributes                 answer records. SOS records include simulated symbolic
150,000 generated examples, giving 1,350,000 examples be-                traces with Python-like snippets and returned algebraic re-
fore a 5% validation split and 1,282,500 training records af-            sults, including retries and errors. Crucially, these records
terward. Inputs use one to three declared variables and one              contain no native function-call messages or tool descrip-
to five initial terms. Task-specific symbolic routines produce           tions. The run uses rank 32, scale 16, dropout 0.05, a
exact direct-task targets. Weighted-SOS instances are gener-             2,048-token limit, learning rate 5 × 10−5 , one epoch, and
ated backward by sampling m ∈ {1, . . . , 5}, base polynomi-             one H100. It comprises 181,848 packed sequences, approx-
als qj , and integer weights cj ∈ {1, . . . , 10}, then display-         imately 3.72 × 108 tokens, and 22,731 optimizer steps; the
Figure 2: Illustrative coordination example, not a model trajectory. Exact factorization verifies a proposed group, but the search
system must decide which terms to group and when to revise an unhelpful partial decomposition. The useful regrouping exposes
(x2 + xy)2 + 2(x − y)2 , after which exact expansion verifies the certificate.

 Stage               Model-facing representation                    System interface             Learning/evaluation signal
 Direct-task SFT     ChatML problem and direct algebraic target  Direct text                 Assistant-token cross-entropy
 SOS SFT             Simulated Python-like symbolic snippets and Simulated symbolic context; Assistant-token cross-entropy; ob-
                     later observed results                      no native calls             servations are context
 GRPO                SFT-initialized sampled responses serialized Chat-template response op- Task-specific symbolic reward and
                     with the model chat template                 timization                 format gate
 Direct evaluation   Final transformed expression                    Direct text; no tools       Exact task contract
 SOS evaluation      Native function calls, exact tool observations, Native calls for Base+Tools Exact weighted-SOS structural and
                     and terminal object                             and Full                    coefficient verifier

Table 3: Training and evaluation representations. The SFT corpus contains no native function-call messages. GRPO is defined by
chat-template response optimization under symbolic rewards; native-call behavior is evaluated in the weighted-SOS deployment
environment.


appendix reports the complete training configuration.               tasks additionally check basis restrictions, remainder reduc-
                                                                    tion, or Bézout identities; SOS reward is gated on positive-
Verifier-grounded GRPO. The second stage starts from
                                                                    rational weighted-square structure and an exact coefficient
the SFT model and optimizes sampled responses with task-
                                                                    residual. A separate trajectory-shaping term favors valid, ex-
specific symbolic rewards. Let E(y) parse the required an-
                                                                    ecutable, nonrepeated calls while assigning the largest in-
swer wrapper and return ⊥ if it is absent. For task k,
                                                                   crement to terminal verification. The appendix gives the full
               −1,                         E(y) = ⊥,                formulas. The study evaluates the combined reward and does
    Rk (y) =                                           (2)          not isolate individual reward components.
               0.1Ifmt (y) + 0.9rk (y), otherwise,
where rk ∈ [0, 1] is computed from the exact task contract          Native SOS deployment. At test time, Base+Tools and
rather than string equality. For example, quotient/remainder        Full receive the native SymPy interface; Base and SFT do not.
is checked through f = qg+r and a reduced remainder, while          All eight supporting tasks remain direct prediction tasks for
SOS reward is gated on parseable weighted-square struc-             every checkpoint. Thus, the deployment-time mismatch is de-
ture and coefficient residual. GRPO uses a global prompt            liberate: SFT exposes the algebra and simulated effects of op-
batch of 64, eight generations per prompt, 20,039 optimizer         erations, whereas the final SOS system must interact through
steps, and approximately 55 hours on four 80GB H100 GPUs.           native calls and exact observations. The appendix provides
We report this stage as checkpoint-level policy optimization        the corresponding message formats, native schemas, respon-
under the symbolic objective above. Native-call trajectories        sibility split, and training settings. The current configurations
are evaluated in the weighted-SOS deployment environment,           establish the behavior of the complete deployed system, not
and trajectory-level statements refer to the complete model–        the separate contribution of this representation change.
harness system.
Reward interpretation. The exact task scores reward the                                    Experiments
state produced by a response rather than surface agreement          Our evaluation separates checkpoint-level algebraic compe-
with one reference string. Local tasks combine algebraic            tence from complete tool-enabled certificate search. We ask
equivalence with their requested normal form; structural            three questions: (1) how performance differs across Base,
     Configuration     Checkpoint      Native tools on SOS                 Supporting task        Base     SFT      Full
     Base            Unadapted Phi-4          No                           Term ordering          76.34   91.28    97.61
     SFT               QLoRA SFT              No                           Collection             58.71   84.36    96.84
     Base+Tools      Unadapted Phi-4          Yes                          Expansion              66.23   88.52    98.73
                                                                           Horner form            33.87   72.14    89.47
     Full             SFT → GRPO              Yes                          Symmetric reduction    14.52   63.71    82.19
                                                                           Quotient/remainder     41.16   79.83    93.28
Table 4: Evaluated systems. Native tools are disabled on                   Extended GCD           13.79   68.47    91.53
the eight supporting tasks and retention checks for all rows.              Factorization          31.44   76.29    97.12
Base+Tools and Full receive the same SOS interface and                     Eight-task macro       42.01 78.08 93.35
limits.
                                                                 Table 5: Accuracy (%) on the eight supporting tasks. Native
                                                                 tools are disabled for every checkpoint on all rows, and each
SFT, and Full on the eight direct polynomial tasks; (2) how
                                                                 task contains 10,000 test instances. The final row averages
Base, SFT, Base+Tools, and Full compare on exactly verified
                                                                 only these eight direct tasks.
weighted-SOS search, where native tools are available only
to the two tool-enabled systems; and (3) whether the spe-
cialized checkpoints show an obvious loss on two general-             Metric                     Base     SFT     B+T      Full
mathematics retention checks. We first define the evaluated           Weighted SOS            7.63 51.82 44.73 78.96
systems and shared protocol, and then report supporting-              Nine-task system macro 38.19 75.16     – 91.75
task accuracy, weighted-SOS success, post-hoc task-family
                                                                      General-mathematics retention checks
aggregates, terminal failure categories, and secondary reten-         AIME-90, avg@16         16.67 34.44           – 38.89
tion results.                                                         GSM-8K, avg@16          91.58 93.71           – 96.29
Configurations and fairness. Table 4 separates check-
point adaptation from SOS tool access. The same test in-         Table 6: Weighted-SOS success, the system-level nine-task
stances, decoding settings, exact verifier, and applicable       macro, and general-mathematics retention checks (%). The
time/call budgets are held fixed across comparable condi-        nine-task macro averages the eight direct tasks in Table 5
tions. This design compares complete systems. It does not        together with weighted SOS. B+T denotes Base+Tools and
isolate GRPO, adding tools after SFT, or their interaction.      is reported only on weighted SOS, the task on which it differs
                                                                 operationally from Base. Native tools are disabled for both
Backbone scope. We use Phi-4-reasoning-plus                      retention checks.
throughout to hold pretraining and model capacity fixed.
The software interfaces are model-agnostic, but empirical
transfer to other backbones is not evaluated.                    native tools disabled. Weighted-SOS success measures the
Evaluation layers. The supporting-task rows evaluate             terminal state reached by the complete model–harness sys-
checkpoint skill under direct exact contracts, with native       tem, with native tools available only to Base+Tools and Full.
tools disabled. The weighted-SOS row evaluates complete          We then use a post-hoc family aggregation to describe where
deployed systems in a shared search environment, including       the largest performance differences occur, examine how exact
the native interface for Base+Tools and Full. The terminal       verification separates successful search from terminal failure,
verifier then evaluates the mathematical state reached by that   and conclude with general-mathematics retention checks and
interaction. Keeping these layers separate avoids attributing    training cost.
direct-task checkpoint gains to unavailable tools or treating    Direct algebraic performance. Table 5 shows that Full
a syntactically valid call as a verified proof.                  is strongest on every supporting task. Its eight-task macro-
Benchmarks. The custom suite contains 10,000 separately          average is 93.35%, compared with 78.08% for SFT and
generated instances for each task, or 90,000 total. We re-       42.01% for Base. Because native tools are disabled for all
port exact accuracy; weighted-SOS success requires verifier      checkpoints on these tasks, the rows measure checkpoint-
acceptance. As secondary retention checks, we use the 90-        level algebraic performance rather than deployment-time
problem AI-MO AIME validation set (AIME 2022–2024)               tool execution. The experiment reports checkpoint-level out-
and all 1,319 GSM-8K test problems (AI-MO 2024; Cobbe            comes; attribution to particular training examples or reward
et al. 2021). Tools are disabled for these checks. Each check-   components is outside its design.
point produces 16 samples per problem with temperature           Verified weighted-SOS performance. Table 6 gives the
0.65, top-p = 0.95, a 2,048-token limit, and seed 1234.          four-way comparison on weighted SOS, the only native tool-
avg@16 is mean sample correctness, not pass@16 or ma-            calling task. Full reaches 78.96%, compared with 51.82%
jority vote.                                                     for SFT, 44.73% for Base+Tools, and 7.63% for Base. Rela-
                                                                 tive to Base, SFT improves by 44.19 percentage points and
                          Results                                Base+Tools by 37.10 points; Full is a further 27.14 points
We organize the results by evaluation layer. The eight sup-      above SFT and 34.23 points above Base+Tools. These differ-
porting tasks measure checkpoint-level algebraic skill with      ences compare complete systems rather than isolated com-
       Post-hoc family      Base     SFT     Full       ∆          run uses 20,039 optimizer steps and approximately 55 hours
       Local operations     58.18   85.11   97.58   +12.46
                                                                   on four 80GB H100 GPUs. The appendix consolidates the
       Structural algebra   25.84   71.04   89.12   +18.08         training configuration.
       Weighted SOS          7.63   51.82   78.96   +27.14
                                                                                            Discussion
Table 7: Descriptive family averages derived from Tables 5
                                                                   Exact execution does not remove coordination errors. A
and 6; ∆ is Full minus SFT in percentage points. Local oper-
                                                                   backend can execute a requested operation perfectly while the
ations comprise ordering, collection, expansion, and factor-
                                                                   agent chooses an unhelpful operation, argument, grouping,
ization; structural algebra comprises Horner form, symmet-
                                                                   or stopping point. The 44.73% Base+Tools result and the
ric reduction, quotient/remainder, and extended GCD. The
                                                                   three terminal failure types make this distinction concrete.
grouping was chosen after inspecting task structure and is
                                                                   Tool-agent evaluation should therefore inspect both the in-
not a pre-registered analysis.
                                                                   teraction and the mathematical state reached at the end, par-
                                                                   alleling environment-state evaluations in broader tool-agent
ponent effects.                                                    benchmarks (Patil et al. 2025; Yao et al. 2025).
   Including weighted SOS yields system-level nine-task            Algebraic grounding is a plausible complement to tool
macro-averages of 38.19%, 75.16%, and 91.75% for Base,             access. The Full system’s advantage over Base+Tools is
SFT, and Full, respectively. Because the weighted-SOS com-         consistent with the hypothesis that training on the operations
ponent is evaluated with native tools only for the tool-enabled    and representations behind a tool can complement learning
systems, this quantity combines eight direct checkpoint eval-      its interface. The direct-task rows and weighted-SOS row
uations with one system-level certificate-search evaluation.       measure different objects: checkpoint skill without tools ver-
It is therefore a heterogeneous summary of complete sys-           sus complete deployed search with tools. Causal effects of
tems rather than a uniform checkpoint-only metric. Wilson          SFT, GRPO, individual supporting tasks, and the representa-
intervals in the appendix quantify finite test-set sampling; the   tion change from simulated traces to native calls are outside
study does not estimate checkpoint-to-checkpoint variation.        the four-configuration design.
Performance across algebraic task families. Table 7
groups the reported tasks into a post-hoc descriptive tax-         Discovery, interaction, and verification must be distin-
onomy. Relative to SFT, Full gains 12.46 points on local op-       guished. Every evaluation polynomial has a weighted-SOS
erations, 18.08 points on broader structural algebra tasks, and    certificate by construction, but the prompt does not reveal this
27.14 points on weighted SOS. The first two differences com-       fact and credit is awarded only for an accepted certificate.
pare checkpoints under tool-free direct evaluation, whereas        Thus the reported success rate is certificate-search yield un-
the weighted-SOS difference compares complete deployed             der a fixed budget, not SOS recognition; abstention is a failed
systems because Full additionally receives the native inter-       search, not a correct negative. Likewise, a schema-valid call
face. The increasing gap is consistent with the complete sys-      and a successful backend execution are intermediate events
tem providing larger improvements as tasks require more            rather than proofs. The terminal check is exact but narrower
global representation and search choices, but the grouping is      than proof-assistant verification: it certifies positive rational
descriptive rather than a component or per-task ablation.          weights, square structure, and coefficient identity, without
                                                                   formalizing side assumptions or constrained Positivstellen-
Verification separates search from proof. The verifier             satz arguments.
accepts only a structurally valid weighted-SOS expression
that expands exactly to the target polynomial. Successful Full                  Conclusion and Limitations
episodes use 3.8 native calls on average, below the ten-call
limit. Unsuccessful terminal outputs fall into three distinct      Weighted-SOS search provides a controlled setting in which
classes: premature completion or abstention, an expression         local algebra is exact, global search remains nontrivial, and
that is not a valid weighted SOS, and a well-formed weighted       final correctness is machine checkable. An algebra-grounded
SOS whose expansion is the wrong polynomial. Exact veri-           Phi-4 checkpoint trained with SFT and verifier-grounded
fication prevents all three from being counted as proofs.          GRPO, then deployed with native SymPy calls, reaches
                                                                   78.96% verified SOS success versus 44.73% for the same
General-mathematics retention checks. Under one 16-                base backbone with the same interface. Together with the
sample evaluation pass, Full has the highest mean sample           direct-task results and terminal failure separation, this sup-
accuracy on AIME-90 (38.89%) and GSM-8K (96.29%).                  ports treating learned algebraic skill, tool interaction, and
These secondary results are retention checks: they show no         exact verification as distinct parts of a complete agent.
obvious loss of general mathematical performance in this
                                                                      The evidence is limited to same-generator synthetic prob-
evaluation pass, but they are not evidence of broad transfer
                                                                   lems with one to three variables, weighted SOS, one back-
or generalization. The comparison uses one backbone, one
                                                                   bone, and one run per stage. The experimental design com-
checkpoint per training stage, and no repeated-run uncer-
                                                                   pares complete configurations; component-level effects of
tainty estimate.
                                                                   SFT, GRPO, tools, individual supporting tasks, and the in-
Training budget. The SFT run uses one H100 for one                 ternal model–harness control split are outside its scope.
epoch, corresponding to 22,731 optimizer steps. The GRPO           The study does not cover natural inequality benchmarks,
larger polynomials, non-SOS classification, constrained cer-      Li, M.; Zhao, Y.; Yu, B.; Song, F.; Li, H.; Yu, H.; Li, Z.;
tificates, repeated training seeds, or cross-backbone transfer.   Huang, F.; and Li, Y. 2023. API-Bank: A Comprehensive
These are substantive extensions rather than claims of the        Benchmark for Tool-Augmented LLMs. In Proceedings of
present work.                                                     the 2023 Conference on Empirical Methods in Natural Lan-
                                                                  guage Processing, 3102–3116. Singapore: Association for
                   Acknowledgments                                Computational Linguistics.
The authors acknowledge the National Artificial Intelligence      Li, Z.; Li, Z.; Tang, W.; Zhang, X.; Yao, Y.; Si, X.; Yang, F.;
Research Resource (NAIRR) Pilot and Voltage Park for pro-         Yang, K.; and Ma, X. 2025. Proving Olympiad Inequalities
viding the H100 GPU compute resources used in this re-            by Synergizing LLMs and Symbolic Reasoning. In Interna-
search under allocation NAIRR250114.                              tional Conference on Learning Representations.
                                                                  Li, Z.; Liao, B.; and Ye, Q. 2025. IneqSearch: Hybrid Reason-
                        References                                ing for Olympiad Inequality Proofs. In Advances in Neural
Abdin, M.; Agarwal, S.; Awadallah, A.; Balachandran, V.;          Information Processing Systems, volume 38.
Behl, H.; et al. 2025. Phi-4-reasoning Technical Report.          Lightman, H.; Kosaraju, V.; Burda, Y.; Edwards, H.; Baker,
arXiv:2504.21318.                                                 B.; Lee, T.; Leike, J.; Schulman, J.; Sutskever, I.; and Cobbe,
AI-MO. 2024. AIMO Validation AIME. Hugging Face                   K. 2024. Let’s Verify Step by Step. In International Confer-
dataset. 90 problems from AIME 2022, 2023, and 2024.              ence on Learning Representations.
Chen, W.; Ma, X.; Wang, X.; and Cohen, W. W. 2023. Pro-           Liu, B.; Qi, N.; Zeng, X.; Dehbi, L.; and Yang, Z. 2025. Au-
gram of Thoughts Prompting: Disentangling Computation             tomated Proof of Polynomial Inequalities via Reinforcement
from Reasoning for Numerical Reasoning Tasks. Transac-            Learning. In Proceedings of the IEEE/CVF Conference on
tions on Machine Learning Research.                               Computer Vision and Pattern Recognition, 5052–5060.
Cobbe, K.; Kosaraju, V.; Bavarian, M.; Chen, M.; Jun, H.;         Lv, K.; Dong, Y.; Han, R.; Jia, F.; Ma, F.; and Zhang, J. 2026.
et al. 2021. Training Verifiers to Solve Math Word Problems.      LLM-Guided Quantified SMT Solving over Uninterpreted
arXiv:2110.14168.                                                 Functions. Proceedings of the AAAI Conference on Artificial
Dettmers, T.; Pagnoni, A.; Holtzman, A.; and Zettlemoyer,         Intelligence, 40(17): 14304–14312.
L. 2023. QLoRA: Efficient Finetuning of Quantized LLMs.
In Advances in Neural Information Processing Systems, vol-        Meurer, A.; Smith, C. P.; Paprocki, M.; Čertík, O.; Kirpichev,
ume 36.                                                           S. B.; Rocklin, M.; Kumar, A.; Ivanov, S.; Moore, J. K.;
                                                                  Singh, S.; et al. 2017. SymPy: Symbolic Computing in
Fawzi, A.; Malinowski, M.; Fawzi, H.; and Fawzi, O. 2019.         Python. PeerJ Computer Science, 3: e103.
Learning Dynamic Polynomial Proofs. In Advances in Neural
Information Processing Systems, volume 32.                        Mirzadeh, I.; Alizadeh-Vahid, K.; Shahrokhi, H.; Tuzel, O.;
                                                                  Bengio, S.; and Farajtabar, M. 2025. GSM-Symbolic: Un-
Feng, J.; Huang, S.; Qu, X.; Zhang, G.; Qin, Y.; Zhong,
                                                                  derstanding the Limitations of Mathematical Reasoning in
B.; Jiang, C.; Chi, J.; and Zhong, W. 2026. ReTool: Re-
                                                                  Large Language Models. In International Conference on
inforcement Learning for Strategic Tool Use in LLMs. In
                                                                  Learning Representations.
International Conference on Learning Representations.
Gao, L.; Madaan, A.; Zhou, S.; Alon, U.; Liu, P.; Yang,           Parrilo, P. A. 2003. Semidefinite Programming Relaxations
Y.; Callan, J.; and Neubig, G. 2023. PAL: Program-Aided           for Semialgebraic Problems. Mathematical Programming,
Language Models. In Proceedings of the 40th International         96(2): 293–320.
Conference on Machine Learning, 10764–10799.                      Patil, S. G.; Mao, H.; Yan, F.; Ji, C. C.-J.; Suresh, V.; Stoica,
Gou, Z.; Shao, Z.; Gong, Y.; Shen, Y.; Yang, Y.; Duan, N.; and    I.; and Gonzalez, J. E. 2025. The Berkeley Function Calling
Chen, W. 2024a. CRITIC: Large Language Models Can Self-           Leaderboard (BFCL): From Tool Use to Agentic Evaluation
Correct with Tool-Interactive Critiquing. In International        of Large Language Models. In Proceedings of the 42nd In-
Conference on Learning Representations.                           ternational Conference on Machine Learning, volume 267 of
Gou, Z.; Shao, Z.; Gong, Y.; Shen, Y.; Yang, Y.; Huang, M.;       Proceedings of Machine Learning Research, 48371–48392.
Duan, N.; and Chen, W. 2024b. ToRA: A Tool-Integrated             PMLR.
Reasoning Agent for Mathematical Problem Solving. In In-          Pelleriti, N.; Spiegel, C.; Liu, S.; Martínez-Rubio, D.; Zim-
ternational Conference on Learning Representations.               mer, M.; and Pokutta, S. 2026. Neural Sum-of-Squares: Cer-
Hubert, T.; Mehta, R.; Sartran, L.; Horváth, M. Z.; Žužić, G.;    tifying the Nonnegativity of Polynomials with Transformers.
et al. 2026. Olympiad-Level Formal Mathematical Reason-           In International Conference on Learning Representations.
ing with Reinforcement Learning. Nature, 651: 607–613.            Putinar, M. 1993. Positive Polynomials on Compact Semi-
Laban, P.; Hayashi, H.; Zhou, Y.; and Neville, J. 2026. LLMs      Algebraic Sets. Indiana University Mathematics Journal,
Get Lost in Multi-Turn Conversation. In International Con-        42(3): 969–984.
ference on Learning Representations.                              Qin, Y.; Liang, S.; Ye, Y.; Zhu, K.; Yan, L.; et al. 2024.
Lasserre, J. B. 2001. Global Optimization with Polynomials        ToolLLM: Facilitating Large Language Models to Master
and the Problem of Moments. SIAM Journal on Optimiza-             16000+ Real-World APIs. In International Conference on
tion, 11(3): 796–817.                                             Learning Representations.
Ramos, A. F.; Hulak, D. B.; and Barretto de Queiroz, R. J. G.     Acting in Language Models. In International Conference on
2026. Formal Verification of an Explicit Counterexample to        Learning Representations.
the Jacobian Conjecture. Archive of Formal Proofs.                Zuo, R.; Zhao, H.; He, G.; Yang, Z.; and Wang, J. 2026. From
Ren, Z. Z.; Shao, Z.; Song, J.; Xin, H.; Wang, H.; et al. 2025.   LLM-Generated Conjectures to Lean Formalizations: Auto-
DeepSeek-Prover-V2: Advancing Formal Mathematical Rea-            mated Polynomial Inequality Proving via Sum-of-Squares
soning via Reinforcement Learning for Subgoal Decompo-            Certificates. Accepted to ICML 2026, arXiv:2605.15445.
sition. arXiv:2504.21801.
Schick, T.; Dwivedi-Yu, J.; Dessì, R.; Raileanu, R.; Lomeli,
M.; Hambro, E.; Zettlemoyer, L.; Cancedda, N.; and Scialom,
T. 2023. Toolformer: Language Models Can Teach Them-
selves to Use Tools. In Advances in Neural Information
Processing Systems, volume 36.
Schmüdgen, K. 1991. The K-Moment Problem for Compact
Semi-Algebraic Sets. Mathematische Annalen, 289(2): 203–
206.
Shao, Z.; Wang, P.; Zhu, Q.; Xu, R.; Song, J.; et al. 2024.
DeepSeekMath: Pushing the Limits of Mathematical Rea-
soning in Open Language Models. arXiv:2402.03300.
Shojaee, P.; Mirzadeh, S. I.; Alizadeh, K.; Horton, M.; Ben-
gio, S.; and Farajtabar, M. 2025. The Illusion of Thinking:
Understanding the Strengths and Limitations of Reasoning
Models via the Lens of Problem Complexity. In The Thirty-
ninth Annual Conference on Neural Information Processing
Systems.
Stengle, G. 1974. A Nullstellensatz and a Positivstellensatz
in Semialgebraic Geometry. Mathematische Annalen, 207:
87–97.
Tao, T. 2026. A Digestion of the Jacobian Conjecture Coun-
terexample. What’s New.
Wang, X.; Wang, Z.; Liu, J.; Chen, Y.; Yuan, L.; Peng, H.; and
Ji, H. 2024. MINT: Evaluating LLMs in Multi-Turn Inter-
action with Tools and Language Feedback. In International
Conference on Learning Representations.
Wei, C.; Sun, M.; and Wang, W. 2024. Proving Olympiad
Algebraic Inequalities without Human Demonstrations. In
Advances in Neural Information Processing Systems, vol-
ume 37, 82811–82822.
Xin, H.; Ren, Z. Z.; Song, J.; Shao, Z.; Zhao, W.; et al.
2025. DeepSeek-Prover-V1.5: Harnessing Proof Assistant
Feedback for Reinforcement Learning and Monte-Carlo Tree
Search. In International Conference on Learning Represen-
tations.
Yang, J.; Prabhakar, A.; Narasimhan, K.; and Yao, S.
2023a. InterCode: Standardizing and Benchmarking Inter-
active Coding with Execution Feedback. arXiv:2306.14898.
Yang, K.; Swope, A. M.; Gu, A.; Chalamala, R.; Song, P.; Yu,
S.; Godil, S.; Prenger, R. J.; and Anandkumar, A. 2023b. Le-
anDojo: Theorem Proving with Retrieval-Augmented Lan-
guage Models. In Advances in Neural Information Process-
ing Systems, volume 36.
Yao, S.; Shinn, N.; Razavi, P.; and Narasimhan, K. 2025.
τ -bench: A Benchmark for Tool-Agent-User Interaction in
Real-World Domains. In International Conference on Learn-
ing Representations.
Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan,
K.; and Cao, Y. 2023. ReAct: Synergizing Reasoning and
 Detailed Task Contracts and Exact Verifiers
                                                                                                                         P
                                                                    Putinar instead gives the smaller form f = σ0 + i σi gi
This section expands the compact task summary in Ta-                (Putinar 1993). Stengle’s general Positivstellensatz may re-
ble 2. All supporting tasks are direct prediction tasks; only       quire additional multiplier, denominator, or ideal terms
weighted-SOS evaluation exposes the native SymPy inter-             (Stengle 1974), while SOS constraints can be searched
face.                                                               through semidefinite relaxations (Parrilo 2003). The main
                                                                    experiments set A = {∅}; constrained-certificate compe-
Weighted-SOS acceptance                                             tence is outside the evaluation scope.
A submitted certificate must parse as
                                                                                 Synthetic Data Generation
               m
          f=
               X
                     cj p2j ,   cj ∈ Q>0 ,    pj ∈ R.      (A1)     Shared sampler and construction principles
               j=1                                                  The nine datasets share a compact polynomial sampler and
                                                                    differ in how the sampled objects are transformed into a
The verifier first checks the structure of every summand, then      problem–target pair. A generic sampled polynomial has the
computes                                                          form
                                    m                                                                  L
                                                                                                       X    n
                                                                                                            Y
                                                                                                              xα
                                   X
                                       cj p2j                                   p(x1 , . . . , xn ) =   aℓ    i ,
                                                                                                                 ℓi
                    expandf −                                                                                          (A3)
                                  j=1                                                                ℓ=1    i=1

and requires every coefficient to be exactly zero. It accepts       with one to three declared variables, one to five initial terms,
any valid decomposition, not only the generator’s hidden            and nonzero integer coefficients aℓ ∈ [−10, 10]. Duplicate
one. A syntactically valid answer can therefore fail either         monomials are combined symbolically, and task adapters
structurally or by identity.                                        control exponent ranges so that the realized degrees match
                                                                    Table A2. The displayed variable priority is sampled in-
Terminal failure taxonomy                                           dependently, so the same algebraic object can be requested
                                                                    under different lexicographic orders. Training and evaluation
Figure A1 separates interface events from mathematical ac-          generation use seeds 42 and 2025, respectively.
ceptance. A schema-valid call or successful symbolic ex-               The supporting tasks use two complementary construc-
ecution can still lead to a terminal failure; only the final        tion patterns. Forward transformations begin with a sam-
coefficient identity constitutes a certificate.                     pled expression and apply one deterministic symbolic oper-
   An invalid call uses an unregistered function or an argu-        ation to obtain the target. Ordering, collection, expansion,
ment object that fails schema validation. An execution error        Horner form, and symmetric reduction follow this pattern.
includes parsing failure, timeout, or a symbolic-backend ex-        Algebraic-relation tasks require several outputs to satisfy
ception. A repeated call is an identical call repeated within       a common identity. Quotient/remainder and extended GCD
a trajectory. Terminal mathematical failures are separated as       are generated and solved under exact polynomial arithmetic,
follows:                                                            while factorization is constructed backward from sampled
1. Premature completion or abstention: the system stops             factors. In every case, the requested answer is specified by an
    without returning an accepted certificate.                      invariant—polynomial equality, a normal-form condition, a
2. Structural failure: the returned expression cannot be            reduced remainder, or a Bézout identity—rather than by one
    parsed as a weighted sum of polynomial squares with             surface string.
    exact positive rational weights.
                                                                    Weighted-SOS backward construction
3. Identity failure: the expression has valid weighted-
    square structure but does not expand exactly to the target      The composite generator samples m ∈ {1, . . . , 5},
    polynomial.                                                     base polynomials q1 , . . . , qm , and integer weights cj ∈
                                                                    {1, . . . , 10}, and computes
The exact verifier accepts 78.96% of Full SOS episodes and                                                      
rejects every terminal output in these three classes.                                                 Xm
                                                                                        f = expand       cj qj2  .        (A4)
General constrained context outside the evaluation                                                   j=1
scope
                                                                    The expanded terms and displayed variable order are ran-
For inequalities gi (x) ≥ 0 defining a semialgebraic set K, a
                                                                    domized before the problem is serialized. The sampled de-
preordering-style certificate can take the form
                                                                    composition guarantees existence but is never required as the
                                                                    answer: any positive-rational weighted-SOS expression sat-
                X                       X
          f=         σS gS ,     σS =       cSj p2Sj ,   (A2)
                                          j
                                                                    isfying the exact identity is accepted. Figure A2 summarizes
                S∈A
                  Q                                                 this backward-construction pipeline.
where gS =             i∈S gi and cSj > 0. When A =
P({1, . . . , r}), this is a preordering certificate. Schmüdgen’s   Normal forms and local transformations
theorem guarantees such a representation for polynomials            Lexicographic term ordering. The generator samples an
strictly positive on a compact basic closed set (Schmüdgen          expanded polynomial, randomizes its displayed additive or-
1991). Under an Archimedean quadratic-module hypothesis,            der, and supplies a variable precedence xπ(1) ≫ · · · ≫
 Task                          Required output                            Exact acceptance or reward check                   Native tools
 Tool-aligned local operations
 Term ordering               Equivalent polynomial in a requested lex-    Polynomial      equality      plus     requested   No
                             icographic monomial order                    order/normal-form check
 Collection                  Expression collected with respect to a se-   Exact polynomial equality and coefficient-         No
                             lected variable or expression                dictionary agreement
 Expansion                   Fully expanded polynomial                    Exact equality and expanded-normal-form            No
                                                                          check
 Factorization                 Product of factors and multiplicities      Exact expanded product; reward additionally        No
                                                                          checks irreducibility over the supported domain
 Broader structural algebra
 Horner form                Nested expression for a supplied variable     Exact equality and recursive Horner-structure      No
                            order                                         depth
 Symmetric reduction        Expression in a designated elementary-        Substitute the basis polynomials and compare       No
                            symmetric basis                               exactly with the target
 Quotient/remainder         q, r such that f = qg + r                     Exact identity plus no remainder monomial di-      No
                                                                          visible by LT(g)
 Extended GCD                  Monic d and Bézout coefficients a, b       d | f , d | g, af + bg = d, and monic normal-      No
                                                                          ization in Q[x]
 Composite target task                               P       2
 Weighted SOS                  Wrapped status and     j c j pj            Positive rational weights, polynomial-square       Yes,       for
                                                                          structure, and exact coefficient identity with f   Base+Tools
                                                                                                                             and Full

Table A1: Detailed task contracts. Exact symbolic equality is evaluated with SymPy. Horizontal group rules separate local
operations, broader structural tasks, and the composite certificate task.




Figure A1: Terminal verification taxonomy. Tool execution and schema validity are intermediate properties. The exact verifier
separately detects premature completion, invalid weighted-SOS structure, and coefficient-identity failure, accepting only a
positive-rational weighted-SOS certificate whose expansion equals the input polynomial exactly.


xπ(n) . Every monomial is represented by the exponent tuple               is serialized as
                     (αℓ,π(1) , . . . , αℓ,π(n) ),                                       −4y 3 x + 5y 2 x2 + 3yx2 z + 2z 4 .
and the target lists terms in descending lexicographic or-                The verifier checks both polynomial equality and the emitted
der of these tuples. Coefficients do not affect the ordering              monomial sequence.
except through cancellation when duplicate monomials are
                                                                          Collection. A collection instance pairs a sampled polyno-
combined. For example, under y ≫ x ≫ z,
                                                                          mial with a designated variable v. After exact expansion
                 3x2 yz − 4y 3 x + 2z 4 + 5x2 y 2                         and combination of like terms, the target is the coefficient
Figure A2: Weighted-SOS instance generation. The generator samples a hidden positive-weight certificate, expands it exactly,
and randomizes the displayed presentation. The hidden decomposition guarantees existence but is not shown to the model, and
evaluation accepts any certificate satisfying the exact polynomial identity.


Task                                Variables       Realized degree          monomials, and finally applying the requested term order. A
                                                                             representative source expression is
Term ordering                           1–3         0–10
Collection                              1–3         0–10                                       (x + yz)(2x − y 2 + z),
Expansion                               1–3         0–55
Factorization                           1–3         2–6                      whose expanded value is
Horner form                             1–3         0–20
Symmetric reduction                     1–3         0–5                                2x2 − xy 2 + xz + 2xyz − y 3 z + yz 2 .
Quotient/remainder                      1–3         f : 1–6; g: 1–3
                                                                             Unlike collection, expansion removes the expression tree in-
Extended GCD                             1          2–10
                                                                             troduced by products and powers. This distinction exposes
Weighted SOS                            1–3         2, 4, or 6
                                                                             the model to two operationally different normalizations: one
                                                                             flattens an expression, while the other organizes a flat poly-
Table A2: Generator ranges. Each task contains 150,000 gen-                  nomial around a selected variable.
erated records before the common 5% validation split and
10,000 separately generated evaluation instances, for 1.35                   Recursive and invariant representations
million records and 90,000 evaluation instances in total.
Algebraic composition can produce coefficients outside the                   Horner form. The Horner adapter supplies an expanded
atomic sampling range.                                                       polynomial and an ordered list of variables. For the first
                                                                             variable v, it computes the coefficients in Eq. (A5), inserts
                                                                             zero coefficients for missing powers, and forms the nested
decomposition                                                                expression
                  dv
                  X                                                             Hv (p) = ((Cd v + Cd−1 )v + · · · + C1 )v + C0 .      (A6)
             p=         Cj (x1 , . . . , vb, . . . , xn )v j ,        (A5)
                  j=0                                                        For multiple variables, the same construction is applied re-
                                                                             cursively to the coefficient polynomials using the remaining
where the hat denotes omission of v and each Cj is ordered                   supplied order. For example,
under the remaining variable precedence. For instance,
                                                                                    p = (3y 2 z + 2yz)x2 + (−5y 3 z + y 2 + 4z)x
2x2 y+x2 z+3xy 2 +4xz+7 = (2y+z)x2 +(3y 2 +4z)x+7.
                                                                                         − 2y 2 z + 3
This task therefore tests more than equality: the answer must
expose the requested coefficient structure rather than return                becomes
a flat expansion.
                                                                                  (3y 2 z + 2yz)x − 5y 3 z + y 2 + 4z x − 2y 2 z + 3.
                                                                                                                     
Expansion. Expansion instances begin with compact ex-
pressions containing sums, products, and positive integer                    The acceptance check expands the answer exactly and also
powers. The exact target is obtained by recursively distribut-               measures whether the requested nesting is present at each
ing products over sums, expanding powers, combining equal                    recursive level.
Symmetric reduction. These instances use a designated                Factorization. Factorization is generated backward. The
variable set and the corresponding elementary symmetric              adapter samples an integer content and nonconstant polyno-
polynomials                                                          mial factors, multiplies them, and expands the product before
                                X                                    presenting it as the input. The exact target records the content
        ek (x1 , . . . , xn ) =       xi1 · · · xik .
                                                                     and factor–multiplicity pairs over the supported coefficient
                             1≤i1 <···<ik ≤n
                                                                     domain. For example,
For a supported symmetric input, the target is a polynomial
Q satisfying                                                              6(x + 2y)(xy + 1) = 6x2 y + 12xy 2 + 6x + 12y.
              p(x1 , . . . , xn ) = Q(e1 , . . . , en ).      (A7)
The exact reduction eliminates the leading monomial itera-           The prompt contains the expanded right-hand side, while
tively. If LM(p) = xa1 1 · · · xann with a1 ≥ · · · ≥ an , then      the target exposes the product on the left. Because units,
                    ea1 1 −a2 ea2 2 −a3 · · · eann                   factor order, and repeated-factor grouping admit equivalent
                                                                     presentations, the checker expands the proposed product ex-
has the same leading monomial under the designated lexico-           actly; the graded reward additionally measures whether the
graphic order; subtracting its suitable multiple strictly lowers     reported nonconstant factors are irreducible over the sup-
the leading term. The task uses the zero-remainder case and          ported domain.
serializes only Q. For two variables,
    x3 + y 3 = e31 − 3e1 e2 ,         e1 = x + y, e2 = xy.
                                                                     Relation to the composite task. The eight generators de-
Evaluation substitutes the elementary symmetric polynomi-            liberately separate operations that are entangled during SOS
als back into the proposed expression and compares the re-           search. Ordering and collection control presentation; expan-
sulting polynomial with the input exactly.                           sion checks a proposed identity; factorization exposes can-
                                                                     didate square structure; Horner and symmetric reduction
Algebraic relations and backward construction                        train non-flat representations; division and extended GCD
Quotient and remainder. The adapter samples four poly-               enforce exact multi-object identities. Weighted-SOS search
nomials p0 , p1 , p2 , p3 , forms                                    combines several of these capabilities but does not reduce to
               f = p0 p1 + p2 ,      g = p3 ̸= 0,          (A8)      any one supporting task.
and then runs exact single-divisor multivariate division un-
der the requested monomial order. The product-plus-offset
construction produces algebraic dependence without assum-                      Training–Deployment Boundary
ing that the final quotient is p0 or that the final remainder is
p2 ; the canonical pair is determined by repeated leading-term       Supporting-task supervision and deployment-time tool ac-
reduction. At each step, if LM(g) divides the current leading        cess use different interfaces. SFT teaches algebraic transfor-
monomial, the appropriate multiple of g is subtracted and            mations through direct prediction and simulated symbolic
added to q; otherwise the current leading term is moved to r.        observations without native function-call messages. GRPO
The process terminates with                                          optimizes chat-template responses with task-specific sym-
                                                                     bolic rewards. During weighted-SOS evaluation, Base+Tools
 f = qg + r,         LM(g) ∤ m for every monomial m of r.
                                                                     and Full use the native SymPy interface, while the eight sup-
For example, under lexicographic order x ≫ y,                        porting tasks and the retention checks remain direct, tool-free
                f = x2 + xy,        g = xy − 1                       evaluations. Terminal success is determined independently
yields q = 1 and r = x2 + 1.                                         by the exact certificate verifier.
Extended GCD. Extended-GCD instances are univariate,
so the computation remains in the Euclidean domain Q[x].                       Native Tool and Output Schemas
Given sampled nonzero polynomials f and g, exact polyno-
mial division generates the remainder sequence
                                                                     Component          Responsibility
                     ri−1 = qi ri + ri+1 ,
                                                                     Model-facing      Produces a text continuation, a native call object,
while the same updates are applied to coefficient pairs ex-
                                                                     output            or a terminal answer object.
pressing each ri as a linear combination of the original in-
                                                                     Harness           Checks call schemas, executes valid SymPy
puts. When the remainder becomes zero, the last nonzero                                functions, returns observations, and enforces
remainder is normalized to a monic polynomial d, and the                               call, attempt, strike, and time limits.
corresponding coefficients a, b satisfy                              Terminal verifier Parses weighted squares, enforces positive ra-
                  af + bg = d = gcd(f, g).             (A9)                            tional weights, and compares the expanded co-
            3               2                                                          efficient dictionary exactly.
For f = x − 1 and g = x − 1, one valid target is
              d = x − 1,      a = 1,       b = −x,                   Table A3: Responsibility split for weighted-SOS evaluation.
         3              2
since (x − 1) − x(x − 1) = x − 1. The verifier checks                Trajectory-level statistics characterize the complete model–
divisibility, the Bézout identity, and monic normalization           harness system, while terminal correctness is determined
rather than one particular coefficient pair.                         independently by the exact verifier.
Function                        Argument and result contract          The SFT environment uses Axolotl 0.8.0-dev, PEFT
                                                                   0.14.0, Transformers 4.49.0, PyTorch 2.5.1+cu124, Datasets
expand_polynomial               Required expression; re-
                                turns status, original, and
                                                                   3.2.0, and Tokenizers 0.21.0. The run contains 181,848
                                expanded, or an error mes-         packed sequences, approximately 3.72 × 108 tokens, and
                                sage.                              7.05 raw examples per packed sequence; its validation loss
collect_terms                   Required expression, op-           is 0.0158.
                                tional variable; returns
                                collected with status fields.      Backbone and portability. All reported checkpoints share
reorder_polynomial              Required       expression,         the same Phi-4 backbone so that the study focuses on post-
                                optional   order;     returns      training and deployed coordination rather than model-family
                                reordered and the applied          scaling. The generators, exact contracts, native schemas,
                                order.                             SymPy backend, and terminal verifier are model-agnostic
factorize_polynomial            Required expression; re-           software components. Reusing them with another backbone
                                turns factorized with status       is technically straightforward, but matched empirical trans-
                                fields.                            fer requires repeating both SFT and verifier-grounded post-
                                                                   training and is outside the present evidence.
Table A4: Native functions used by Base+Tools and Full
during weighted-SOS evaluation.                                                      Reward Functions
   Every call contains an identifier, a registered function        Let E(y) parse the task-specific object between «< and »>,
name, and a JSON argument object. Undeclared fields are            and let E(y) = ⊥ when the wrapper is missing. Each
rejected. Tool expressions use explicit * for multiplication       parseable object receives a format indicator Ifmt and task
and ** for powers. Parse or backend exceptions return              score rk ∈ [0, 1]:
status=error with a message. A call has a five-second
limit; an episode has a 60-second limit; three consecutive
                                                                               
                                                                                 −1,                       E(y) = ⊥,
schema-invalid calls terminate the episode. The system per-          Rk (y) =                                           (A10)
                                                                                 0.1Ifmt (y) + 0.9rk (y), otherwise.
mits at most ten calls and three decomposition attempts.
   The terminal answer object contains the fields success,         All symbolic equalities are evaluated exactly. Write I[·] for
is_sos, attempts_used, SOSPolynomial, and                          an indicator and c(e) for the coefficient vector of expanded
reason. Because every evaluation input is SOS, a                   polynomial e. The normalized residual score is
false is_sos or unsuccessful status is treated as fail-                                              
ure/abstention, not a verified mathematical classification.                                ∥c(e)∥1
                                                                      ρf (e) = exp −λ                    ,     λ = 10. (A11)
                                                                                        ∥c(f )∥1 + ε
                    Message Formats
                                                                   For collection, let I be the union of coefficient-dictionary
Direct-task SFT records. The corpus uses multi-turn
                                                                   supports of the target and output. The task scores are
ChatML messages. System and user messages state the task
and inputs; assistant turns contain the target transformation            rord = 0.3I[p = f ] + 0.7τ (p),                    (A12)
or algebraic derivation inside task-specific wrappers. Sys-
tem/user tokens are visible as context but masked from the            rcollect = 0.3I[p = f ]
SFT loss.                                                                              |{i ∈ I : cpi = cfi }|
                                                                                 + 0.7                        ,             (A13)
Simulated symbolic SFT traces. SOS records represent                                       max(1, |I|)
symbolic computation through wrapped Python-like snippets            rexpand = 0.5I[p = f ] + 0.5I[p = expand(p)],          (A14)
followed by evaluated results in later context. The assistant is     rHorner = 0.4I[p = f ]
trained on its reasoning, snippets, and final answer; symbolic                             dcorrect
observations are context rather than prediction targets. These                   + 0.6                   ,                  (A15)
                                                                                       max(1, deg f )
records are not native tool_calls, and the corpus does
not expose the native tool schemas.                                     rsym = 0.7I[p(e1 , . . . , en ) = f ]
                                                                                 + 0.3I[vars(p) ⊆ {ei }],                   (A16)
GRPO prompts and outputs. GRPO inputs and outputs
use the Phi-4 chat template and are scored by the exact task-            rdiv = 0.6ρf (f − qg − r)
specific parsers and symbolic rewards described in the main                      + 0.4I[r is reduced by LT(g)],             (A17)
paper. We report GRPO as checkpoint-level response opti-               rxgcd = 0.5ρf (af + bg − d)
mization. Native-interaction analysis concerns the weighted-                     + 0.3I[d | f ∧ d | g] + 0.2I[d monic],     (A18)
SOS evaluation environment, and trajectory-level conclu-                              Y e
sions refer to the complete model–harness system.                     rfactor = 0.5I[ hj j = f ]
                                                                                        j
                                                                                        P
      Training and Reproducibility Details                                               j ej deg(hj )I[hj irreducible]
                                                                                + 0.5                                     , (A19)
Table A5 consolidates the SFT and GRPO settings used in                                            deg f
the completed runs.                                                     rSOS = 0.3Istruct
Setting                  Supervised fine-tuning                                Group Relative Policy Optimization
Initialization           Phi-4-reasoning-plus; four-bit weights                SFT model and loaded adapter
Data and signal          Multi-turn ChatML; 5% validation; assistant-token     Multi-task prompts; exact symbolic task rewards
                         cross-entropy
Adaptation               LoRA rank 32, scale 16, dropout 0.05                  Continued adapter training; rank 32, scale 16, dropout
                                                                               0.05
Length and packing       2,048 tokens with packing
Length limits                                                                  2,048 prompt and 2,048 completion tokens
Horizon                  One epoch; 22,731 optimizer steps                     One epoch; 20,039 optimizer steps; approximately 55
                                                                               hours
Batching                 Micro-batch 1; accumulation 8                         Per-device batch 1; four processes; accumulation 16;
                                                                               eight generations per prompt
Optimization             LR 5 × 10−5 ; cosine; 100 warmup steps; 8-bit AdamW   LR 10−6 ; cosine; 50 warmup steps
Precision/hardware       bfloat16; gradient checkpointing; one H100            bfloat16; four 80GB H100s; ZeRO-2 CPU offload
Sampling and seed        Teacher forcing; seed 42                              Temperature 0.9; top-p = 0.95; seed 42

                               Table A5: Training settings for the completed SFT and GRPO runs.

                                              
                                     X                              pretation. They do not estimate checkpoint-to-checkpoint or
              + 0.7Istruct ρf f −        cj p2j  .     (A20)      training-run variation.
                                      j
                                                                           SOS configuration   Success   Wilson 95% interval
Here τ ∈ [0, 1] is normalized Kendall agreement with the
                                                                           Base                  7.63%            [7.13, 8.17]
requested monomial order and dcorrect counts correct recur-
                                                                           SFT                  51.82%          [50.84, 52.80]
sive Horner levels. The SOS structural gate requires exact
                                                                           Base+Tools           44.73%          [43.76, 45.71]
positive rational weights and polynomial squares.
                                                                           Full                 78.96%          [78.15, 79.75]
   The tool-trajectory shaping reward is
     Rtool = 0.05Nschema + 0.05Nexec                                Table A6: Approximate Wilson intervals treating the 10,000
                                                         (A21)
             − 0.2Nrepeat − 0.01T + Iverified .                     test instances as independent Bernoulli trials. They quantify
It rewards schema-valid calls and successful execution, pe-         finite test-set sampling, not variation across checkpoints or
nalizes repeated identical calls and long trajectories, and         training runs.
gives the largest single increment to a verified terminal cer-      Tool-use summary. Successful Full episodes use 3.8
tificate. The study evaluates this combined reward and does         native calls on average, measured over verifier-accepted
not isolate individual reward components.                           weighted-SOS episodes.

                  Evaluation Protocol
Custom tasks. All comparable configurations use the same
10,000 items per task, decoding procedure, answer parser, ex-
act verifier, and applicable computational budgets. Weighted-
SOS Base+Tools and Full share the four native functions,
ten-call limit, three-attempt limit, five-second call limit, and
60-second episode limit. The custom-task results are reported
under this shared protocol.
General-mathematics              retention           checks.
The      evaluation   uses     all    90    examples      in
AI-MO/aimo-validation-aime, covering AIME
2022–2024, and all 1,319 GSM-8K test problems. Native
tools are disabled. Each checkpoint generates 16 samples
per problem with temperature 0.65, top-p = 0.95, at most
2,048 output tokens, and seed 1234. The reported avg@16
is the mean of the correctness indicator over all samples; it
is neither pass@16 nor majority-vote accuracy.

             Additional Descriptive Results
The intervals below quantify uncertainty from the finite
evaluation set under an independent Bernoulli-item inter-
