                                             CodeSpec: Dual Executable Specifications for Agentic Long-Horizon Feature
                                                                          Development
                                                              Peiding Wang1 , Li Zhang1 , Fang Liu1∗ , Taichuan Li1 , Yinghao Zhu2
                                                                       1
                                                                         State Key Laboratory of Complex & Critical Software Environment,
                                                                     School of Computer Science and Engineering, Beihang University, China
                                                                      2
                                                                        School of Computing and Data Science, The University of Hong Kong
                                                                                 {wangpeiding, fangliu}@buaa.edu.cn


                                                                    Abstract                                                    Feature Instruction + Existing Repository
                                                                                                           Task Statement                                                                                   •     APIs
                                                                                                           • Implement MLflow Distributed Tracing System                                                    •     Files
                                           LLM-based code agents have advanced repository-level soft-      Core Functionalities                                                                             •     Modules
                                           ware development through iterative interaction with code-       • Create and manage distributed tracing ......                                                   •     Constraints
                                                                                                                                                                                             MLFlow
                                                                                                           • Support both live and immutable span ......                                    Repository      •     Dependencies
                                           bases and tools. However, feature development requires in-
                                           tegrating new behaviors into existing architectures through
                                           coherent cross-component functional chains. Existing agents     Repository-Constrained Design                                          Long-Horizon Constraint Drift
                                           typically derive such chains through free-form reasoning,        # base_mlflow.py                      # span.py
                                                                                                                                                                                   Turn 1       Turn 50         Turn 150    Turn 300
arXiv:2607.26777v1 [cs.SE] 29 Jul 2026




                                           often producing unreliable feature designs with incomplete       Class BaseMlflow
                                                                                                                                      import
                                                                                                                                                  create_mlflow_span()
                                                                                                            SpanProcessor()                                     dispatch         Processor → invoke → Factory
                                           functional chains. Moreover, textual designs are difficult to                             invoke ?
                                                                                                                                                  LiveSpan/Span/...                                                               ?
                                                                                                                                   propagate ?
                                           verify and enforce, making it challenging to maintain de-        # provider.py      # trace_data.py           # trace_manager.py

                                           sign–implementation consistency throughout long-horizon                                                                               Factory → dispatch → Span types
                                                                                                                               TraceData
                                                                                                                                                                                                                                  ?
                                           development. We propose CodeSpec, a dual executable spec-                                                serialize
                                           ification method for repository-level feature development. It    # fluent.py       # constant.py
                                                                                                                                                # utils.py
                                                                                                                                                                # otel.py        TraceData → serialize → OTLP
                                                                                                                                                                OTLP
                                           builds reliable functional chains from evidence pairing sub-
                                                                                                                                                                                Functional-chain constraints gradually fade
                                           requirement semantics with repository architectures, then
                                           compiles them into complementary architecture and behavior
                                           specifications that check chain completeness and correctness                     Locally Plausible Code, Incomplete Feature Realization
                                           while preserving design–implementation consistency over                      Required Factory Call                                              Generated Local Call
                                                                                                           class BaseMlflowSpanProcessor(...):                                class BaseMlflowSpanProcessor(...):
                                           long interactions. On FeatureBench, which targets feature de-   def on_start(self, span, parent_context):                          def on_start(self, span, parent_context):
                                                                                                               mlflow_span = create_mlflow_span(                                  mlflow_span = LiveSpan(
                                           velopment in existing repositories, CodeSpec achieves 70.7%,            span, trace_id, span_type                                          span, trace_id, span_type
                                                                                                               )                                                                  )           bypasses the required factory relation
                                           55.0%, and 49.9% pass rates under DeepSeek-V4-Pro, outper-
                                           forming representative baselines such as Claude Code. Results
                                           on the repository generation benchmark NL2Repo-Bench fur-       Figure 1: Feature development requires agents to de-
                                           ther demonstrate its generalizability. The code and data are    rive repository-consistent functional chains and preserve
                                           available at https://github.com/zhu-zhu-ding/CodeSpec.          them throughout implementation. Missing a critical ar-
                                                                                                           chitectural relation, such as invoking factory method cre-
                                                                                                           ate_mlflow_span(), may break the end-to-end feature behav-
                                                                Introduction                               ior.
                                         With the rapid advancement of large language models, auto-        nizes these entities and interactions into a coherent functional
                                         mated software development has evolved from standalone            chain from feature entry points to observable behaviors.
                                         function generation (Chen 2021; Austin et al. 2021) to               The repository-level nature of feature development makes
                                         repository-level tasks (Li et al. 2024; Jimenez et al. 2024).     LLM-based coding agents a promising paradigm. Repre-
                                         Feature development is particularly important because real-       sentative agents, including Claude Code (Anthropic 2026),
                                         world software systems are continuously extended to satisfy       Codex (OpenAI 2025), SWE-agent (Yang et al. 2024), and
                                         evolving requirements (Du et al. 2025; Li et al. 2025; Zhou       OpenHands (Wang et al. 2025c), rely on the agent’s reasoning
                                         et al. 2026). Unlike standalone generation, implementing a        capabilities to implicitly plan development through natural-
                                         new feature requires integrating new behaviors into an exist-     language interactions while iteratively generating and repair-
                                         ing architecture. Agents must determine not only which code       ing code. Other approaches introduce explicit design pro-
                                         entities should be created or modified, but also how these        cesses: MetaGPT (Hong et al. 2024) and ChatDev (Qian
                                         entities should interact across components. Feature develop-      et al. 2024) produce natural-language artifacts describing
                                         ment therefore commonly requires the design stage that orga-      module responsibilities and collaboration workflows, while
                                                                                                           RTADev (Liu et al. 2025) performs architecture planning be-
                                            ∗
                                              Corresponding author.                                        fore implementation. However, both free-form implicit plan-
                                         Copyright © 2027, Association for the Advancement of Artificial   ning and explicit textual design provide limited support for
                                         Intelligence (www.aaai.org). All rights reserved.                 deriving reliable repository-grounded functional chains and
enforcing them throughout long-horizon development.                   of each functional chain, jointly verifying whether the
   As illustrated in Figure 1, existing agents face two closely       chain is complete and behaves correctly while maintain-
related challenges:                                                   ing design–implementation consistency throughout long-
  • Unreliable functional-chain design. Existing agents typ-          horizon development.
    ically design features through free-form reasoning, which       • We conduct extensive experiments on FeatureBench and
    can deviate from repository architecture constraints and          NL2Repo with different backbone models, demonstrating
    overlook the call and dependency relations among code             the effectiveness, robustness, generalizability, and favor-
    entities. Consequently, they may derive functional chains         able quality–cost trade-off of CodeSpec for long-horizon
    that are incomplete or inconsistent with the repository.          feature development.
  • Weak long-horizon enforcement. Functional designs
    are typically represented as free-form textual plans, which                          Related Work
    are difficult to verify and enforce during iterative explo-    Repository-level Feature Development Benchmarks
    ration, editing, and repair. As a result, the implementation
    may gradually diverge from the intended functional chain,      Code generation research has evolved from standalone func-
    leading to inconsistencies between design and realization.     tion synthesis (Chen 2021; Austin et al. 2021) to repository-
                                                                   level software development, where models need to under-
   To address these challenges, we propose CodeSpec, a dual        stand project context and generate patches in real codebases.
executable specification method for agentic long-horizon           Benchmarks such as DevEval (Li et al. 2024) and SWE-
feature development. It constructs repository-grounded             bench (Jimenez et al. 2024) evaluate such repository-level ca-
functional-chains for feature sub-requirements and compiles        pabilities through realistic software engineering tasks. More
each chain into complementary architecture and behavior ex-        recent feature-level benchmarks, including FEA-Bench (Li
ecutable specifications. CodeSpec consists of two key com-         et al. 2025), and FeatureBench (Zhou et al. 2026), further
ponents:                                                           focus on practical feature development, where a high-level
1) Evidence-Grounded Functional Chain derives traceable            instruction may require coordinated changes and generation
feature realization paths by identifying relevant functional       across multiple functions, files, classes, and interfaces. These
units and connecting them with paired requirement seman-           tasks usually involve a full development process of design,
tics and repository as evidence, such as design patterns, call     implementation, testing, execution, and repair, making one-
relations, and dependencies. This reduces free-form archi-         shot generation insufficient and motivating coding agents
tectural reasoning and grounds each transition in the existing     that interact with repositories and development environments
repository to improve the design reliability.                      over multiple steps.
2) Dual Executable Specification Compilation converts
each functional chain into two executable forms: an ar-            LLM-based Coding Agents
chitecture specification that represents its architecture re-      LLM-based coding agents have become a popular paradigm
alization and a behavior specification that represents its ex-     for repository-level software development (Wang et al. 2026,
pected execution. They complementarily verify whether the          2025b,a). Unlike one-shot generation methods, they can au-
chain is complete and whether it behaves correctly, thereby        tonomously invoke tools, inspect files, text plan, edit pro-
preserving design–implementation consistency throughout            grams, and iteratively repair failures. Representative coding
long-horizon development.                                          agents and assistants include Claude Code (Anthropic 2026),
   Experiments on FeatureBench (Zhou et al. 2026) show             Codex (OpenAI 2025), SWE-agent (Yang et al. 2024), and
that CodeSpec achieves 70.7%, 55.0%, and 49.9% %Passed             OpenHands (Wang et al. 2025c). In addition, development-
on the Lite, Fast, and Full splits, consistently outperform-       oriented agent frameworks such as MetaGPT (Hong et al.
ing coding-agent and architecture-planning baselines under         2024), ChatDev (Qian et al. 2024) and RTADev (Liu et al.
the same DeepSeek-V4-Pro backbone. Results with GPT-               2025) organize software development into structured stages
5.4-mini and NL2Repo-Bench (Ding et al. 2026) which                and use textual architecture designs to coordinate soft-
evaluates greenfield repository development from natural-          ware development. Despite their progress, existing agents
language requirements further demonstrate robustness across        still mainly maintain design information as free-form tex-
models and generalization to greenfield repository genera-         tual plans, which makes it difficult to explicitly preserve
tion. Ablation and further analyses confirm the effectiveness      functional chains and architecture constraints during long-
of evidence-grounded functional chains and the complemen-          horizon feature development.
tary executable specifications, particularly on complex and
long-horizon tasks, with moderate additional cost.                                           Method
   Our main contributions are summarized as follows:
  • We propose evidence-grounded functional-chain reason-
                                                                   Task Definition
    ing that pairs task semantics with repository architecture     In this section, we define the feature development task.
    evidence at each transition, enabling agents to derive reli-   Given a natural-language feature instruction I and an existing
    able cross-component realization paths from feature entry      repository R, an LLM-based coding agent generates a patch
    points to observable behaviors.                                P to get the updated repository R′ which preserving existing
  • We introduce dual executable specifications that repre-        functionality and satisfying the instruction I:
    sent the architecture realization and expected execution                   P = LLM(I, R),           R′ = R ⊕ P.            (1)
  1 Functional Chain Construction                                                            2 Dual Executable Specification Compilation

            Evidence-Grounded Functional Chain                                                         Executable Architecture Specification                                 Executable Behavior Specification
                                                                                               1 def spec_subfunction_i(repo):                                      1 def test_subfunction_chain_i():
                                                                                               2     # requirement: <required feature behavior i>                   2     # requirement: <required feature behavior i>
        Requirements                                                  Repository               3     # chain: u1 -> u2 -> ... -> uk                                 3     # chain: u1 -> u2 -> ... -> uk
                               Paired Evidence                                                 4     # evidence: desgin patterns, call relations, ...               4     # evidence: desgin patterns, call relations, ...
         Semantics                                                    Architecture             5     # data flow: invoke, dispatch,propagate, ...                   5     # behaviors: b1, b2, b3, ..., bn
                                                                                               6                                                                    6
                                                                                               7     check_unit(repo, "<u1>", "<u2>")                               7     check_output("<π1>", "<boutput1>")
                                                                                               8     check_relation("<u1>", "<u2>", "< ρ1>")                        8     check_boundary("<π1>", "<bboundary1>")
            Design Patterns           Call Relations            ...
                                                                                               9     check_data_flow("<u1>", "<u2>", "<d1>")                        9     check_state("<π1>", "<bstate1>")
        <u1>                  <u2>                     <u3>                 <uk>              10     ...                                                Behavior   10     ...
                   < ρ1>                 < ρ2>                 < ρk-1>                        11     check_unit(repo, "<uk-1>", "<uk>")                 Analysis   11     check_output("<πn>", "<boutputn>")
       Processor            Factory                SpanType                 ...
                                                                                              12     check_relation("<uk-1>", "<uk>", "<ρk-1>")                    12     check_boundary("<πn>", "<bboundaryn>")
                   <e1>                  <e2>                  <ek-1>                         13     check_data_flow("<uk-1>", "<uk>", "<dk>")                     13     check_state("<πn>", "<bstaten>")

        invoke              dispatch               propagate             data flow            14                                                                   14
                                                                                              15     return feedback(info)                                         15     return feedback(info)
         <d1>                 <d2>                     <d3>               <dk>



       Inputs                              Repository Grounding                              3 Specification Guided Code Generation
                                                                                                                                                                   all checks pass

                                     Requirements                       Code Units
        Feature                                                                                                      Execute Specifications                                                                     Verified
                                      Create span...             span.py          types.py
      Instruction                                                                                                                                                      Arch Feedback                             Patch
                                                                                                                      Architecture            Path
                                       Propagate...                                                                                         Integrity                 Chain Violation
                                                                 trace.py          io.py                                Checks
                                                                                              Edit Patch                                                            Behavior Feedback            Revise
                                      Export OTLP...                                                                    Behavior          Runtime
                                                                                                                         Checks          Correctness                 Behavior Failure
                                                                  util.py         base.py
       Existing                              ...
                                                                                                                      long-horizon constraint preservation
      Repository


                                                                                  Figure 2: The overview of CodeSpec.


Overview                                                                                                         These units provide candidate building blocks, but select-
As shown in Figure 2, CodeSpec constructs reliable func-                                                      ing relevant units alone does not yield a valid feature design;
tional chains using evidence that pairs sub-requirement se-                                                   the key is determining how they should be connected to real-
mantics with the corresponding repository architecture. It                                                    ize each obligation. CodeSpec therefore prompts the LLM to
then compiles each chain into dual executable specifica-                                                      perform evidence-driven chain reasoning by pairing require-
tions: an architecture specification representing its struc-                                                  ment evidence, which explains why a transition is needed
tural realization and a behavior specification representing                                                   from requirements, with repository evidence, which shows
its expected execution. These specifications complementar-                                                    how it is supported by existing design patterns, call relations,
ily verify whether the chain is complete and behaves cor-                                                     or repository architectures. The resulting functional chain is
rectly, thereby maintaining design–implementation consis-                                                     an ordered sequence in which each adjacent pair of units uki
tency throughout long-horizon feature development.                                                            and uk+1
                                                                                                                    i    is linked according to its supporting evidence eki :
                                                                                                                                     ci = {u1i , e1i , u2i , . . . , uki , eki , uk+1
                                                                                                                                                                                  i   }.                                     (4)
Evidence-Grounded Functional Chain
                                                                                                              Here, uki denotes a functional unit involved in realizing re-
A feature is realized through coordinated interactions among                                                  quirements ri , and eki denotes the evidence supporting the
multiple repository components rather than isolated code                                                      transition from uki to uk+1
                                                                                                                                        i  . Each evidence eki pairs re-
modifications. However, feature instructions usually describe                                                 quirement semantics with repository evidence, ensuring that
desired behaviors without specifying which components                                                         adjacent units are connected through traceable, repository-
should participate or how they should interact. To bridge this                                                supported reasoning rather than free code relations.
gap, CodeSpec constructs an evidence-grounded functional
chain for each sub-function by pairing requirement seman-                                                     Dual Executable Specification Compilation
tics with repository architecture evidence at every reasoning
                                                                                                              The constructed functional chains explicitly describe how in-
step.
                                                                                                              dividual feature requirement should be realized across repos-
    Given a feature instruction I, the agent first decomposes                                                 itory components. However, retaining these chains as tex-
it into a set of sub-requirements:                                                                            tual design artifacts is unsuitable for long-horizon develop-
                                                                                                              ment, because agents may gradually overlook pre-designed
                    LLM(I) = {r1 , r2 , . . . , rm }.                                        (2)              key information during long-term interactions. Therefore,
   Each requirement ri represents a specific behavior that                                                    we compile each functional chain into two complementary
the feature should achieve. For each requirement, the agent                                                   executable specifications: the architecture specification that
identifies candidate implementation units that need to be                                                     verifies path integrity and the behavior specification that ver-
modified or introduced:                                                                                       ifies runtime correctness along the path.
                                                                                                              Executable Architecture Specification Given a sub-
                           Uri = {u1 , u2 , . . . , un }.                                    (3)              requirement ri and its functional chain ci , CodeSpec instan-
tiates an executable architecture specification sarch
                                                 i    using the         which may cover a functional unit, a transition, or a sub-
template τarch shown in Figure 2:                                       path. The checks examine observable outcomes, including
                                                                        returned values and external effects, boundary and excep-
              sarch
               i    = LLMarch (R, ri , ci ; τarch ).              (5)   tional conditions, and state transitions at multiple positions
                                                                        along the functional chain. Thus, the behavior specification
   Inspired by architecture conformance checking and pro-
                                                                        examines multiple intermediate and final behaviors rather
gram analysis (Pruijt et al. 2017; Murphy, Notkin, and Sul-
                                                                        than only the final output.
livan 2001; Kildall 1973), we operationalize path integrity
using three representative dimensions: functional units, ar-               During implementation, violated expectations are reported
chitectural relations, and data flows. The template maps the            as localized behavior violations. In this way, executable be-
units, relations, and data flows in ci into three types of checks:      havior specifications complement architecture specifications
                                                                        by preserving runtime correctness along each functional
                                                                        chain.
            n               oki
  sarch
   i    =    CheckUnit(uji )
                                  j=1                                   Specification Guided Code Generation
             n                               oki −1                     For all sub-requirements, the generated architecture and be-
            ∪ CheckRelation(uji , uj+1
                                   i   , ρj
                                          i )                     (6)
                                                                        havior specifications are aggregated as:
                                                    j=1
             n                                      oki −1
            ∪ CheckDataFlow(uji , uj+1
                                   i   , dji )                .                              m
                                                                                             [                         m
                                                                                                                       [
                                                        j=1                       S arch =         sarch
                                                                                                    i    ,   S beh =         sbeh
                                                                                                                              i .   (9)
                                                                                             i=1                       i=1
   Here, ρji and dji are jointly inferred from the requirement
                                                                           The agent implements the feature under the joint con-
and repository evidence in eji , representing the intended ar-          straints of S arch and S beh . Architecture feedback identifies
chitectural relation and data-flow operation between uji and            missing units, broken relations, or interrupted data flows,
uj+1
 i   , respectively. CheckUnit verifies that each required              while behavior feedback reports incorrect runtime behaviors
unit exists, CheckRelation checks whether adjacent units                along the functional chains. The agent incorporates both sig-
preserve the intended relation ρji , and CheckDataFlow ver-             nals into subsequent edits until all specifications pass or the
ifies the required data state dji between them.                         interaction budget K is exhausted.
   During implementation, the specification is executed
against the updated repository. Missing units, broken re-               Algorithm 1: Specification Guided Code Generation
lations, or interrupted data flows are reported as localized                Input: Instruction I, repository R, specifications S arch
architecture violations. In this way, executable architecture               and S beh , budget K
specifications preserve the path integrity of each functional               Output: Patch P
chain.                                                                   1: P, Farch , Fbeh ← ∅
Executable Behavior Specification Given the sub-                         2: k ← 0
requirement ri , its functional chain ci , and the corresponding         3: while k < K do
architecture specification sarch
                             i    , CodeSpec jointly analyzes            4:     ∆P ← LLMcode (I, R, S arch , S beh , P, Farch , Fbeh )
the intended path structure and architectural constraints to             5:     P ← P ⊕ ∆P
identify behavior-observation subpaths, and instantiates an              6:     R′ ← R ⊕ P
executable behavior specification using the template τbeh                7:     Farch ← ExecArch(R′ , S arch )
shown in Figure 2:                                                       8:     Fbeh ← ExecBeh(R′ , S beh )
                                                                         9:     if Pass(Farch ) ∧ Pass(Fbeh ) then
             sbeh = LLMbeh (ri , ci , sarch ; τbeh ).             (7)   10:         break
              i                        i
                                                                        11:     end if
   Inspired by established property-based, category-                    12:     k ← InteractCount()
partition, and model-based testing techniques (Claessen and             13: end while
Hughes 2000; Ostrand and Balcer 1988; Chow 1978), we                    14: return P
operationalize behavioral obligations using three represen-
tative dimensions: observable outputs, boundary conditions,
and state transitions. The template derives three types of                 Here, ExecArch verifies the integrity of the functional
behavioral checks at multiple observation scopes along the              chains, whereas ExecBeh verifies their runtime behaviors.
functional chain:                                                       Their complementary feedback jointly preserves path in-
                                                                        tegrity and behavioral correctness throughout long-horizon
         sbeh
          i   = {CheckOutput(πiq , boutput
                                    i,q    ),                           implementation.

                   CheckBoundary(πiq , bboundary
                                        i,q      ),               (8)                    Experimental Setups
                   CheckState(πiq , bstate ni
                                     i,q )}q=1 .                        Research Questions
  Here, ni denotes the number of behavioral observation                 We evaluate CodeSpec through the following research ques-
scopes derived for ci , and πiq ⊆ ci denotes the q-th scope,            tions:
                                     Lite                                    Fast                                   Full
 Agent Scaffold
                   %Passed       #Resolved   Avg. Cost ($)    %Passed    #Resolved   Avg. Cost ($)   %Passed    #Resolved   Avg. Cost ($)
 OpenHands         60.0±5.7         6            0.15         41.4±3.6      10           0.13        37.1±2.7      18           0.11
 Claude Code       59.8±5.4         6            0.11         47.0±3.8      14           0.12        41.1±2.8      23           0.10
 Mini-SWE-Agent    62.6±6.0         7            0.09         49.6±4.0      24           0.09        43.4±2.8      25           0.09
 RTADev            65.3±5.6         6            0.17         49.7±3.8      15           0.16        46.1±2.8      26           0.15
 CodeSpec          70.7±5.1         9            0.18         55.0±3.8      17           0.19        49.9±2.8      28           0.16

Table 1: Comparison under the DeepSeek-V4-Pro (max thinking) backbone model on FeatureBench. The Lite, Fast, and Full
splits contain 30, 100, and 200 tasks, respectively. Bold numbers indicate the best performance.


  Agent Scaffold     %Passed        #Resolved    Avg. Cost ($)             • OpenHands (Wang et al. 2025c), a general-purpose agent
                                                                             supporting repository exploration, code editing, execu-
  Mini-SWE-Agent      47.5±6.0          2               0.7                  tion, and iterative repair.
  OpenHands           48.1±5.9          3               1.2
  RTADev              45.9±5.7          3               1.3
                                                                           • Mini-SWE-Agent (Yang et al. 2024), a lightweight agent
                                                                             based on a minimal repository interaction and repair loop.
  Codex               51.7±6.2          4               0.7
  CodeSpec            54.7±5.8          5               1.3                • Claude Code (Anthropic 2026), a widely adopted in-
                                                                             dustrial coding agent for autonomous repository editing,
Table 2: Comparison of different coding agents with the                      execution, and debugging.
same GPT-5.4-mini backbone (medium thinking) on the Fea-                   • Codex (OpenAI 2025), an OpenAI coding agent support-
tureBench Lite split.                                                        ing repository-level reasoning, tool use, code modifica-
                                                                             tion, and iterative refinement.
                                                                           • RTADev (Liu et al. 2025), an architecture-first agent that
 • RQ1: Overall Performance. How does CodeSpec com-                          uses textual architecture designs to guide development;
   pare with existing coding agents on repository-level fea-
   ture development tasks?                                                  For controlled comparison, all methods (except for Codex)
                                                                         use DeepSeek-V4-Pro as the backbone model. We addition-
 • RQ2: Ablation Study. How does each component con-                     ally evaluate GPT-5.4-mini to examine model-level gener-
   tribute to the CodeSpec’s performance?                                alization. All methods share the same repository environ-
 • RQ3: Executable vs. Textual Specifications. Do exe-                   ments, evaluation scripts, and interaction budgets. We boot-
   cutable specifications preserve design constraints more               strap task-level results 10,000 times and report the resulting
   effectively than textual specifications?                              mean and standard deviation.
 • RQ4: Greenfield Repository Development Generaliza-
   tion. Can CodeSpec generalize from repository evolution                                 Experimental Results
   to greenfield repository generation?                                  RQ1: Overall Performance
                                                                         As shown in Table 1, CodeSpec consistently achieves the best
Benchmarks and Metrics                                                   performance across all FeatureBench splits under the same
We evaluate CodeSpec on FeatureBench (Zhou et al. 2026),                 DeepSeek-V4-Pro backbone. On the Lite split, CodeSpec
a repository-level feature development benchmark requir-                 reaches 70.7% %Passed and resolves 9 tasks, outperforming
ing coordinated modifications across mutli-interfaces. Each              the strongest baseline RTADev by 5.4 percentage points in
problem averages 4.8k words and requires about 800 lines                 %Passed and 3 resolved tasks. Similar improvements are ob-
of valid code, compared with 0.2k words and about 32 lines               served on the Fast and Full splits, where CodeSpec improves
in SWE-Bench(Jimenez et al. 2024). It contains three splits:             %Passed over RTADev by 5.3 and 3.8 percentage points, re-
Lite (30), Fast (100), and Full (200).                                   spectively, while achieving the highest number of resolved
   Following FeatureBench, we report %Passed, the aver-                  tasks. Compared with general-purpose coding agents such as
age proportion of fail-to-pass tests passed across tasks, and            OpenHands and Mini-SWE-Agent, CodeSpec obtains larger
Resolved #, the number of tasks for which all required tests             gains across all splits. Unlike textual plans, which remain pas-
pass. The former measures partial implementation progress,               sive context and can be overlooked during extended interac-
while the latter measures complete task resolution. We also              tions, executable specifications continuously expose whether
reporte the average cost metric for each task: Avg.Cost ($).             the intended functional chains remain complete and correct.
                                                                         Their lightweight feedback also helps agents localize vio-
                                                                         lations without repeatedly reconsidering the entire design.
Baselines and Implementation Details
                                                                         These results demonstrate that explicitly modeling functional
We compare CodeSpec with five representative coding-agent                chains and enforcing them through executable specifications
scaffolds:                                                               effectively improves repository-level feature development.
 Variant                            %Passed    #Resolved   Avg. Cost ($)                            CodeSpec (Text)          CodeSpec      RTADev
                                                                                             100%
 Specification Ablations
   w/o All Specification            62.6±6.0      7            0.09                          80%           77.2 74.1
                                                                                                                                               71.8 68.9




                                                                            Mean pass rate
   w/o Behavior Specification       64.0±5.2      6            0.13                                 69.5
   w/o Architecture Specification   66.6±5.7      7            0.16                          60%
 Evidence-Grounded Functional Chain Ablations                                                                                           43.8
   w/o Evidence                  64.8±5.7         6            0.16                          40%                                                           36.3 38.3
 CodeSpec                           70.7±5.1      9            0.18
                                                                                             20%                                                                         17.2

Table 3: Ablation study on the FeatureBench Lite split. All                                   0%
variants use DeepSeek-V4-Pro as the base model.                                                     <= 3,000 words                 3,000-5,000 words       > 5,000 words
                                                                                                                      Task description length (words)
   The additional architecture design and specification execu-             (a) Pass-rate comparison across different instruction-length groups.
tion introduce moderate overhead. Compared with RTADev,                                             CodeSpec (Text)          CodeSpec      RTADev
                                                                                             100%
CodeSpec increases the average cost by only $0.01–$0.03
per task, while consistently improving feature completion                                    80%                                               78.8 78.6




                                                                            Mean pass rate
performance across different task scales. The additional inter-                                            69.0
                                                                                                    64.8              65.2                                        65.2
actions mainly come from executing functional-chain speci-                                   60%                                        55.2
                                                                                                                                                           51.2          50.1
fications and leveraging their violation feedback for iterative
refinement, which provides more precise guidance during im-                                  40%
plementation. To further examine robustness across different
backbone models, we additionally compare agent scaffolds                                     20%
using GPT-5.4-mini on the Lite split (Table 2). CodeSpec
maintains the best performance, achieving 54.7% %Passed                                       0%
                                                                                                     <= 120 turns                       120-200 turns       > 200 turns
and resolving 5 tasks under the same backbone, even surpass-                                                                 Agent interaction turns
ing Codex, a dedicated coding agent developed by OpenAI
for GPT series LLMs. These results suggest that the effec-                 (b) Pass-rate comparison across different agent interaction-length
tiveness of CodeSpec is robust across different backbone                   groups.
models rather than relying on a specific LLM.
                                                                           Figure 3: Pass-rate comparison among textual specifications,
                                                                           executable specifications, and RTADev across tasks grouped
RQ2: Ablation Study                                                        by instruction length and agent interaction turns.

Table 3 reports the contribution of executable specifications              RQ3: Executable vs. Textual Specifications
and evidence-guided functional-chain construction. Remov-
ing all specifications decreases %Passed from 70.7% to                     We further investigate whether executable specifications
62.6% and reduces the number of resolved tasks from 9 to 7,                preserve design constraints more effectively than textual
confirming that persistent executable constraints are impor-               specifications. CodeSpec (Text) retains the same evidence-
tant for long-horizon feature implementation. The two spec-                grounded functional-chain construction as CodeSpec, but
ification types provide complementary benefits. Removing                   represents the resulting design as textual information rather
the behavior specification causes a substantial drop to 64.0%              than executable specifications. We compare it with Code-
Passed and 6 resolved tasks, indicating that architecture con-             Spec and RTADev, another code agent based on textual de-
nectivity alone cannot ensure correct outputs, boundary han-               sign planning. We compared the three methods described
dling, or state transitions. Removing the architecture specifi-            above on the FeatureBench Lite split.
cation reduces %Passed to 66.6% and resolves 7 tasks, show-                   As shown in Figure 3, the three methods perform rel-
ing that behavior checks alone may still permit incomplete                 atively similarly on simpler tasks with instructions below
or unintended realization paths. Their combination therefore               3,000 words or interactions under 120 turns. The gaps widen
improves both path integrity and runtime correctness.                      as task complexity increases: CodeSpec achieves 71.8% on
   Evidence-guided functional-chain is also critical. Without              instructions of 3,000–5,000 words, compared with 43.8%
explicit evidence grounding, %Passed falls from 70.7% to                   for CodeSpec (Text), and reaches 65.2% beyond 200 turns,
64.8%, while the number of resolved tasks decreases from 9                 outperforming the two textual approaches by 14.0 and 15.1
to 6. This suggests that requirement semantics and repository              points. Although textual plans also provide useful design in-
evidence help identify more reliable functional units and rela-            formation, placing all details in the context increases input
tions, thereby reducing unsupported architectural reasoning.               size and the risk of overlooking requirements and design
Although the complete method incurs the highest average                    constraints. In contrast, CodeSpec provides lightweight ex-
cost at $0.18 per task, the increase is modest relative to the             ecutable feedback throughout interaction, offering more re-
consistent gains in both partial progress and complete task                liable guidance for requirement-intensive and long-horizon
resolution.                                                                tasks.
                                          Easy      Medium         Hard                                     Overall
                    Agent Scaffold
                                        %Passed    %Passed        %Passed       %Passed               #Resolved             Avg.Cost ($)
                    OpenHands           48.6±6.5    26.2±4.4       9.4±2.2       26.4±2.9                    2                    0.10
                    Claude Code         62.0±5.6    45.7±4.6      19.3±3.7       41.6±3.2                    5                    0.11
                    Mini-SWE-Agent      58.0±6.3    35.0±4.2      18.7±4.2       35.5±3.1                    4                    0.08
                    RTADev              61.3±6.3    47.4±4.7      16.3±4.8       41.3±3.5                    7                    0.14
                    CodeSpec            70.0±5.6    51.7±4.3      20.4±4.7       46.6±3.3                    8                    0.17

Table 4: Comparison on NL2Repo using DeepSeek-V4-Pro (max thinking). Easy, Medium, and Hard correspond to repositories
with <1.5K, 1.5K–4K, and >4K lines of code (LOC). Bold indicates the best result.


RQ4: Greenfield Repository Development                                                                       Implementation Comparison
Generalization                                                               RTADev && CodeSpec (Text)                                                              Pass Rate: 56.7%

To assess generalization beyond repository evolution, we                     Processor
                                                                                       × create_mlflow_span() ×             LiveSpan / Span /      ✓
                                                                                                                                                        TraceData
                                                                                                                                                                       ×         OTLP
                                                                                                                               NoOpSpan
evaluate CodeSpec on NL2Repo-Bench (Ding et al. 2026),                        missing cross-module import        wrong dispatch                              serialization incomplete

which contains 104 greenfield tasks that require generating                  def create_mlflow_span():
                                                                             #...
                                                                                                                                                   Broken Relations
                                                                                                                                                   × Processor → Factory:
a Python repository from a requirements document and an                      if isinstance(otel_span, OTelReadableSpan):
                                                                                                                                                    invoke broken by missing import
                                                                                  if otel_span.is_recording():
                                                                                                                                                   × Factory → Span Types:
empty workspace. CodeSpec first creates a repository skele-                           return LiveSpan(otel_span, trace_id, span_type or
                                                                                                                                                   wrong dispatch
                                                                             SpanType.UNKNOWN)
                                                                                  else:                                                            × TraceData → OTLP:
ton and functional units, after which the evolving codebase                           return Span(otel_span)                                       serialization incomplete

provides repository evidence for functional-chain construc-
tion and specification compilation.                                          CodeSpec                                                                               Pass Rate: 100%
   As shown in Table 4, CodeSpec achieves 70.0%, 51.7%,                            ✓                                  ✓      LiveSpan / Span /     ✓                  ✓
                                                                             Processor        create_mlflow_span()                                      TraceData                OTLP
                                                                                                                                NoOpSpan
and 20.4% %Passed on the Easy, Medium, and Hard splits,
                                                                             def create_mlflow_span():
outperforming the strongest baselines by 8.0, 4.3, and 1.1 per-              #...                                                                Executable Checks
                                                                             if not otel_span or isinstance(otel_span,                           ✓ check_runtime_imports()
centage points, respectively. It also obtains the best overall               NonRecordingSpan):                                                   cross-module import
                                                                                  return NoOpSpan()                                              ✓ check_create_mlflow_span_runtime()
%Passed (46.6%) and #Resolved (8), demonstrating its gen-                    if isinstance(otel_span, OTelSpan):                                  NoOpSpan · LiveSpan · Span dispatch
                                                                                  return LiveSpan(otel_span, trace_id, span_type)                ✓ TraceData → OTLP serialization
eralizability to greenfield development. The larger gains on                 if isinstance(otel_span, OTelReadableSpan):                         ✓ ......
                                                                                  return Span(otel_span)
Easy and Medium tasks suggest that CodeSpec effectively
organizes requirements into coherent implementations for
repositories within approximately 4K lines of code, while the          Figure 4: Case study of MLflow distributed tracing in Fea-
smaller gain on Hard tasks reflects the remaining difficulty           turebench by using DeepSeek-V4-Pro.
of coordinating larger requirements for current agents. Al-
though its additional specification and feedback steps slightly        lows the agent to localize and repair structural or behavioral
increase the average cost to 0.17, the performance gains in-           violations during implementation. The case therefore shows
dicate a favorable quality–cost trade-off.                             that executable specifications go beyond textual design de-
                                                                       scriptions by continuously enforcing the functional chain
                        Discussion                                     and maintaining design–implementation consistency across
                                                                       long-horizon development.
Case Study
Figure 4 presents a representative MLflow feature-                                                               Conclusion
development task in Featurebench that requires the agent to
                                                                       We propose CodeSpec, a dual-specification approach for
preserve a complete span lifecycle across multiple modules.
                                                                       agentic long-horizon feature development. It constructs
The RTADev and CodeSpec (Text) identify the major enti-
                                                                       evidence-grounded functional chains from feature require-
ties, but fail to preserve several cross-module relations dur-
                                                                       ments and repository evidence, and compiles each chain into
ing implementation. In particular, it dispatches spans based
                                                                       complementary executable architecture and behavior specifi-
on is_recording() rather than the required OTel span
                                                                       cations. Architecture specifications preserve the integrity of
type, misses a required import between modules, and leaves
                                                                       feature realization paths, while behavior specifications verify
the OTLP conversion path incomplete. Although many indi-
                                                                       runtime correctness along those paths. Together, they provide
vidual interfaces are implemented, these broken connections
                                                                       fine-grained and persistent feedback throughout implemen-
lead to an incomplete feature and a pass rate of 56.7%.
                                                                       tation. Experiments on FeatureBench show that CodeSpec
   In contrast, CodeSpec compiles the functional chain into            consistently outperforms representative coding agents, par-
complementary executable architecture and behavior spec-               ticularly on complex and long-horizon tasks. Moreover, re-
ifications. Architecture feedback reveals whether the chain            sults on NL2Repo-Bench further demonstrate its generaliz-
remains complete and connected, while behavior feedback                ability across repository-level development settings.
identifies whether the connected path realizes the intended
behavior correctly. This lightweight, targeted feedback al-
                        References                                mark for evaluating repository-level code generation for fea-
Anthropic. 2026.          Claude Code: An Agentic Cod-            ture implementation. In Proceedings of the 63rd Annual
ing Tool. https://docs.anthropic.com/en/docs/claude-code/         Meeting of the Association for Computational Linguistics
overview. Accessed: 2026-07-11.                                   (Volume 1: Long Papers), 17160–17176.
Austin, J.; Odena, A.; Nye, M.; Bosma, M.; Michalewski,           Liu, J.; Wang, G.; Yang, R.; Zeng, J.; Zhao, M.; and Cai, Y.
H.; Dohan, D.; Jiang, E.; Cai, C.; Terry, M.; Le, Q.; et al.      2025. RTADev: Intention Aligned Multi-Agent Framework
2021. Program synthesis with large language models. arXiv         for Software Development. In Che, W.; Nabende, J.; Shutova,
preprint arXiv:2108.07732.                                        E.; and Pilehvar, M. T., eds., Findings of the Association for
                                                                  Computational Linguistics: ACL 2025, 1548–1581. Vienna,
Chen, M. 2021. Evaluating large language models trained           Austria: Association for Computational Linguistics. ISBN
on code. arXiv preprint arXiv:2107.03374.                         979-8-89176-256-5.
Chow, T. S. 1978. Testing software design modeled by finite-      Murphy, G. C.; Notkin, D.; and Sullivan, K. J. 2001. Software
state machines. IEEE transactions on software engineering,        reflexion models: Bridging the gap between design and im-
(3): 178–187.                                                     plementation. IEEE Transactions on Software Engineering,
Claessen, K.; and Hughes, J. 2000. QuickCheck: a                  27(4): 364–380.
lightweight tool for random testing of Haskell programs. In       OpenAI. 2025. Introducing Codex. https://openai.com/
Proceedings of the fifth ACM SIGPLAN international con-           index/introducing-codex/. Accessed: 2026-07-11.
ference on Functional programming, 268–279.
                                                                  Ostrand, T. J.; and Balcer, M. J. 1988. The category-partition
Ding, J.; Long, S.; Pu, C.; Zhou, H.; Gao, H.; Gao, X.; He,       method for specifying and generating functional tests. Com-
C.; Hou, Y.; Hu, F.; Li, Z.; Shi, W.; Wang, Z.; Zan, D.; Zhang,   munications of the ACM, 31(6): 676–686.
C.; Zhang, X.; Chen, Q.; Cheng, X.; Deng, B.; Gu, Q.; Hua,
                                                                  Pruijt, L.; Köppe, C.; van der Werf, J. M.; and Brinkkem-
K.; Lin, J.; Liu, P.; Li, M.; Pan, X.; Peng, Z.; Qin, Y.; Shan,
                                                                  per, S. 2017. The accuracy of dependency analysis in static
Y.; Tan, Z.; Xie, W.; Wang, Z.; Yuan, Y.; Zhang, J.; Zhao, E.;
                                                                  architecture compliance checking. Software: practice and
Zhao, Y.; Zhu, H.; Zhu, L.; Zou, C.; Ding, M.; Jiao, J.; Liu,
                                                                  Experience, 47(2): 273–309.
J.; Liu, M.; Liu, Q.; Tao, C.; Yang, J.; Yang, T.; Zhang, Z.;
Chen, X.; Huang, W.; and Zhang, G. 2026. NL2Repo-Bench:           Qian, C.; Liu, W.; Liu, H.; Chen, N.; Dang, Y.; Li, J.; Yang,
Towards Long-Horizon Repository Generation Evaluation of          C.; Chen, W.; Su, Y.; Cong, X.; et al. 2024. Chatdev: Com-
Coding Agents. arXiv:2512.12730.                                  municative agents for software development. In Proceedings
                                                                  of the 62nd annual meeting of the association for computa-
Du, Y.; Cai, Y.; Zhou, Y.; Wang, C.; Qian, Y.; Pang, X.; Liu,
                                                                  tional linguistics (volume 1: Long papers), 15174–15186.
Q.; Hu, Y.; and Chen, S. 2025. Swe-dev: Evaluating and
training autonomous feature-driven software development.          Wang, P.; Zhang, L.; Liu, F.; Shi, L.; Li, M.; Shen, B.; and Fu,
arXiv preprint arXiv:2505.16975.                                  A. 2025a. CodeIF-Bench: Evaluating Instruction-Following
                                                                  Capabilities of Large Language Models in Interactive Code
Hong, S.; Zhuge, M.; Chen, J.; Zheng, X.; Cheng, Y.; Wang,        Generation. arXiv:2503.22688.
J.; Zhang, C.; Yau, S.; Lin, Z.; Zhou, L.; et al. 2024.
MetaGPT: Meta programming for a multi-agent collabora-            Wang, P.; Zhang, L.; Liu, F.; Tao, C.; and Zhu, Y. 2026. Code-
tive framework. In International Conference on Learning           MEM: AST-Guided Adaptive Memory for Repository-Level
Representations, volume 2024, 23247–23275.                        Iterative Code Generation. arXiv preprint arXiv:2601.02868.
Jimenez, C. E.; Yang, J.; Wettig, A.; Yao, S.; Pei, K.;           Wang, P.; Zhang, L.; Liu, F.; Zhu, Y.; Xu, W.; Shi, L.; Lian,
Press, O.; and Narasimhan, K. 2024. Swe-bench: Can lan-           X.; Li, M.; Shen, B.; and Fu, A. 2025b. EfficientEdit: Accel-
guage models resolve real-world github issues? In Inter-          erating Code Editing via Edit-Oriented Speculative Decod-
national Conference on Learning Representations, volume           ing. arXiv:2506.02780.
2024, 54107–54157.                                                Wang, X.; Li, B.; Song, Y.; Xu, F. F.; Tang, X.; Zhuge, M.;
Kildall, G. A. 1973. A unified approach to global program         Pan, J.; Song, Y.; Li, B.; Singh, J.; et al. 2025c. Openhands:
optimization. In Proceedings of the 1st annual ACM SIGACT-        An open platform for ai software developers as generalist
SIGPLAN symposium on Principles of programming lan-               agents. In International Conference on Learning Represen-
guages, 194–206.                                                  tations, volume 2025, 65882–65919.
                                                                  Yang, J.; Jimenez, C.; Wettig, A.; Lieret, K.; Yao, S.;
Li, J.; Li, G.; Zhao, Y.; Li, Y.; Liu, H.; Zhu, H.; Wang, L.;
                                                                  Narasimhan, K.; and Press, O. 2024. Swe-agent: Agent-
Liu, K.; Fang, Z.; Wang, L.; Ding, J.; Zhang, X.; Zhu, Y.;
                                                                  computer interfaces enable automated software engineer-
Dong, Y.; Jin, Z.; Li, B.; Huang, F.; Li, Y.; Gu, B.; and Yang,
                                                                  ing. Advances in Neural Information Processing Systems,
M. 2024. DevEval: A Manually-Annotated Code Generation
                                                                  37: 50528–50652.
Benchmark Aligned with Real-World Code Repositories. In
Ku, L.-W.; Martins, A.; and Srikumar, V., eds., Findings of       Zhou, Q.; Zhang, J.; Wang, H.; Hao, R.; Wang, J.; Han, M.;
the Association for Computational Linguistics: ACL 2024,          Yang, Y.; Wu, S.; Pan, F.; Fan, L.; et al. 2026. Featurebench:
3603–3614. Bangkok, Thailand: Association for Computa-            Benchmarking agentic coding for complex feature develop-
tional Linguistics.                                               ment. arXiv preprint arXiv:2602.10975.
Li, W.; Zhang, X.; Guo, Z.; Mao, S.; Luo, W.; Peng, G.;
Huang, Y.; Wang, H.; and Li, S. 2025. Fea-bench: A bench-
