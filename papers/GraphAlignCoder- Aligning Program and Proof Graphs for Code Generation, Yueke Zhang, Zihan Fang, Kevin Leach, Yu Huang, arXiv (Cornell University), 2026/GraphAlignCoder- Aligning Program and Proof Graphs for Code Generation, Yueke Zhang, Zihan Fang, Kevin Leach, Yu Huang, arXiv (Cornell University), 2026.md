                                            GraphAlignCoder: Aligning Program and Proof Graphs for Code Generation

                                                                            Yueke Zhang, Zihan Fang, Kevin Leach, Yu Huang
                                                                                                     Vanderbilt University
                                                                                                   Nashville, TN 37015 USA




                                                                      Abstract
                                           Code large language models (LLMs) can generate syntac-
                                           tically plausible programs that nevertheless violate hidden
                                           semantic constraints. Existing execution-feedback training
                                           methods identify whether a completed program fails, but pro-
                                           vide limited supervision about how a correct solution should
arXiv:2608.11394v1 [cs.SE] 11 Aug 2026




                                           be organized. We introduce GraphAlignCoder, a training
                                           framework that transfers explicit correctness structure into
                                           code generation.
                                           GraphAlignCoder constructs an implementation graph that
                                           captures control and dependence among program regions. In
                                           parallel, a constrained Lean pipeline produces proof traces,          Figure 1: Shared Algorithmic Skeleton Between Lean
                                           from which we extract a formal proof-flow graph. The model            Proof and Python Control Flow. A Lean proof plan ex-
                                           first learns executable code together with graph-derived de-
                                                                                                                 poses case splits, branch obligations, and final conclusions
                                           scriptions of why individual program regions are correct,
                                           and then consolidates this knowledge into code generation.            that align with the branch and return structure of an exe-
                                           GraphAlignCoder consistently outperforms the base model,              cutable Python program.
                                           code-only SFT, and CodeRL across all benchmarks. Com-
                                           pared with CodeRL, it increases the solved count from 38 to
                                           50 on LiveCodeBench v6 and from 16 to 23 on BigCodeBench              code can contain insecure patterns, package hallucinations,
                                           Hard, corresponding to relative gains of 31.6% and 43.8%,             and repository-level inconsistencies, suggesting that correct-
                                           while also improving BigCodeBench Full from 359 to 363                ness failures are not merely surface-level syntax errors but
                                           tasks. The ablation study further shows that verification-graph
                                           injection produces the initial reasoning gain, while verification
                                                                                                                 often reflect missing semantic structure (Kim et al. 2026;
                                           to code consolidation is essential for robust cross-benchmark         Ravichander et al. 2025; Si et al. 2026). Therefore, improv-
                                           transfer.                                                             ing code generation requires more than making models fluent
                                                                                                                 in programming syntax; it requires helping them recover the
                                                                                                                 latent structure that makes a program correct.
                                                                 Introduction                                       Formal proof provides an opportunity to fill this gap be-
                                         Large language models (LLMs) for code have rapidly moved                cause it exposes reasoning as an explicit structure rather than
                                         from research prototypes to widely used programming assis-              as an implicit byproduct of final code (de Moura et al. 2015;
                                         tants (Chen et al. 2021; Li et al. 2022; Rozière et al. 2023;           Leino 2010). Figure 1 illustrates the key observation behind
                                         Lozhkov et al. 2024; Guo et al. 2024; Hui et al. 2024). These           this work: a proof plan for even a simple property, such as
                                         advances have also changed how programming is practiced:                nonnegativity of an absolute-value computation, contains a
                                         developers increasingly rely on code models for drafting im-            case split and conclusion structure that mirrors the control-
                                         plementations, completing functions, explaining APIs, and               flow branches and return sites of the corresponding Python
                                         repairing errors (Peng et al. 2023; Jain et al. 2025).                  program. Proof assistants such as Lean decompose a theorem
                                            Despite this progress, code LLMs remain vulnerable to                into proof states, subgoals, tactic applications, case splits,
                                         hallucination. In natural language, hallucination often ap-             obligations, and lemma invocations, which can be viewed
                                         pears as fluent but unsupported content (Huang et al. 2025;             as a tactic graph describing how a solution is semantically
                                         Pearce et al. 2022). This problem is subtle in programming              organized (de Moura et al. 2015; Yang et al. 2023; Jiang
                                         because generated code may look reasonable, compile suc-                et al. 2023; Azerbayev et al. 2024). Similarly, a Python im-
                                         cessfully, and even pass a small number of examples while               plementation can be represented as a program graph, such
                                         still failing hidden tests or violating implicit correctness con-       as an abstract syntax tree, control-flow graph, or data-flow
                                         straints (Spracklen et al. 2025; Agarwal et al. 2024; Zhang             graph, where nodes and edges capture how computation pro-
                                         et al. 2025b). Prior studies have shown that AI-generated               ceeds through branches, loops, calls, state updates, and re-
turns (Aho et al. 2006; Ferrante, Ottenstein, and Warren          headers, skip the header row when collecting data, preserve
1987; Yamaguchi et al. 2014). Although Lean tactic graphs         the column–row alignment, and return a DataFrame with the
and Python control-flow graphs are written in different lan-      expected schema.
guages of reasoning, they often share a latent algorithmic           The base model generates plausible code using
structure: proof case splits correspond to program branches,      requests, BeautifulSoup, and pandas, but it as-
invariant-preservation obligations correspond to loop bodies,     sumes that the table body is explicitly wrapped in a tbody
inductive decomposition corresponds to recursion, and wit-        element. When the benchmark page does not follow this exact
ness construction corresponds to return-value assembly. This      structure, the implementation fails with ValueError("No
structural correspondence suggests that graph similarity can      table data found."). The CodeRL baseline repairs
serve as a bridge between formal reasoning and executable         part of the structure by iterating over table rows, but it ex-
program generation, providing process-level supervision that      tracts all th elements as headers while also processing rows
is richer than pass/fail execution feedback but more grounded     in a way that creates a mismatch between the number of
than free-form natural language critique.                         columns and the number of values. As a result, it still fails
   In this paper, we propose GraphAlignCoder, a train-            when constructing the DataFrame.
ing framework based on a principle: correct programs have            GraphAlignCoder succeeds because its generated pro-
structure, formal obligations make correctness structure ex-      gram follows a more obligation-preserving structure. It first
plicit, and graph alignment can transfer this structure into      checks that a table exists, then checks that rows exist, extracts
code LLM training. Our approach extracts program graphs           headers from th cells, iterates over data rows after the header
from solutions first, including control-flow, data-flow, and      row, extracts td cells consistently, and finally constructs the
region-level structures such as loops and returns. In parallel,   DataFrame using the aligned header and data lists. This ex-
we construct graphs that encode semantic obligations, tactic      ample illustrates the central motivation of our approach: the
skeletons, and subgoals. This design gives code LLMs an au-       difference between failure and success is not merely whether
ditable semantic scaffold for learning the organization of cor-   the model knows the right library calls, but whether it orga-
rect programs. The resulting framework has two parts. First,      nizes those calls according to the semantic structure of the
GraphAlignCoder constructs a filtered structural scaffold         task.
by aligning correctness obligations with concrete regions of         From the Python side, the correct solution contains a
trusted Python programs. Second, it adapts the model un-          control-flow structure with a connection guard, a table-
der code generation: the model may learn from structural          existence guard, a row-existence guard, a header-extraction
annotations during training, but the final deployed behavior      region, a data-row extraction loop, and a return-construction
remains ordinary Python generation from the task alone.           region. From the proof side, the same solution can be de-
   This paper makes the following contributions:                  scribed as a set of obligations: the page must be reach-
                                                                  able, the target table must exist, headers must define the
 • We introduce GraphAlignCoder, a framework that con-
                                                                  DataFrame schema, each data row must match the schema,
   nects executable program structure with proof-flow struc-
                                                                  and the returned object must preserve the extracted table
   ture. It aligns implementation regions and Lean proof
                                                                  content. GraphAlignCoder uses this alignment between
   transitions, injects this structure into a code model, and
                                                                  operational regions and obligations as auxiliary supervision,
   consolidates it into Python generation.
                                                                  while still using Python code as the executable target.
 • GraphAlignCoder consistently outperforms the base
   model, code-only SFT, and CodeRL across all three                                    Related Work
   benchmarks. Compared with CodeRL, it improves the
   solved count by 31.6% on LiveCodeBench v6 (50 versus           Code Language Models and Code Generation
   38) and 43.8% on BigCodeBench Hard (23 versus 16).             Large language models for code have made code genera-
 • Ablations validate the complementary roles of structural       tion a central task in software engineering research. Codex
   injection and consolidation. Structural injection increases    showed that pretrained language models can synthesize func-
   LiveCodeBench v6 from 33 to 44 solved tasks, while             tional programs from natural-language prompts (Chen et al.
   consolidation further raises it to 49 and recovers Big-        2021; Li et al. 2022). Recent open code models, including
   CodeBench Full from 339 to 352.                                Code Llama and Qwen-Coder, further improve completion,
                                                                  instruction following, and multilingual programming ability
                 Motivating Example                               through large-scale code pretraining and instruction tuning
                                                                  (Rozière et al. 2023; Hui et al. 2024). These advances are
Motivating Example                                                increasingly evaluated on benchmarks that stress different
Figure 2 shows a representative example from Big-                 forms of programming competence (Jain et al. 2025; Zhuo
CodeBench where both the base code model and the CodeRL           et al. 2025).
baseline fail, while GraphAlignCoder succeeds. The task
asks the model to scrape the first HTML table from a web          Formal Proof Guidance for Reasoning
page and convert it into a Pandas DataFrame. Although this        Formal proof assistants expose reasoning as explicit inter-
task appears to be a simple library-usage problem, it re-         mediate structure, making them a natural source of supervi-
quires the implementation to preserve several implicit obli-      sion for models that must preserve correctness constraints.
gations: fetch the page safely, locate the first table, extract   Lean represents proofs through states, subgoals, tactics, case
Figure 2: Motivating Example: Structural Failure and Graph-Aligned Correction. The task requires scraping the first HTML
table into a Pandas DataFrame. The base model fails by assuming a specific tbody structure, and CodeRL fails by mismatching
header and row flows. GraphAlignCoder succeeds by aligning the Python control-flow graph with obligation-level constraints
such as table existence, row/schema consistency, and DataFrame construction.


splits, lemma applications, and obligation discharge, which     tural view: Floyd–Hoare logic attaches assertions to pro-
provides a structured view of how a theorem is solved           gram points and uses branch conditions and loop invari-
(de Moura et al. 2015). Recent work has used this structure     ants to derive correctness obligations, while modern veri-
to train or guide theorem-proving systems: LeanDojo sup-        fiers such as Dafny automate these obligations for executable
ports retrieval-augmented theorem proving, Draft-Sketch-        programs (Floyd 1967; Hoare 1969; Leino 2010).
Prove uses informal proof sketches to guide formal proof
search, and Llemma develops language models specialized                                Methodology
for mathematical reasoning (Yang et al. 2023; Jiang et al.      GraphAlignCoder follows the four-stage pipeline in Fig-
2023; Azerbayev et al. 2024; Ospanov, Farnia, and Mohit         ure 3. Panels A and B expose complementary structures
2026). These systems show that proof artifacts can provide      from Python code. Panel C turns its correspondence into
useful process-level signals beyond final answers (Zhang        Verification-Graph Injection Training. Panel D then removes
et al. 2025a). However, theorem-proving supervision does        the auxiliary outputs and consolidates the structure into
not directly solve Python code generation. Formal proofs        Python code.
operate over explicit logical statements, while programming
benchmarks require executable implementations that satisfy      Executable Structure: Implementation Graph
tests, APIs, input formats, and hidden edge cases (Cao et al.
2025; Zhou et al. 2024).                                        For task i, let xi contain the natural-language specification,
                                                                starter code, and visible tests, and let yi be a correct Python
Program Graphs and Structural Code                              code snippet provided by the benchmark. Thus, yi defines
Representations                                                 what the model should produce, while the graph below ex-
Program graphs provide a long-standing way to represent         poses how that solution is organized. We deterministically
code beyond token sequences (Allamanis, Brockschmidt,           parse yi with Python’s AST and construct the implementa-
and Khademi 2017). Classical compiler analysis uses ab-         tion graph
stract syntax, control flow, data flow, and program depen-                     GIi = GI (yi ) = (ViI , EiI , Ri ),          (1)
dence graphs to capture how computation is organized across
branches, loops, definitions, uses, and state updates (Aho      where ViI contains function-entry and statement nodes, Ri
et al. 2006; Ferrante, Ottenstein, and Warren 1987). More       groups source spans into regions such as guards, loops, calls,
recent work extends these ideas to learning-based code anal-    recursive sites, updates, and returns, and EiI contains control-
ysis: code property graphs combine syntactic, control-flow,     flow, call, and dominance relations. The graph converts a
and data-flow information for vulnerability discovery, while    whole-program target into region-level structure. As visual-
GraphCodeBERT incorporates data-flow structure into code        ized in Figure 3A, correctness descriptions can be attached
representation learning (Yamaguchi et al. 2014; Guo et al.      to a specific boundary, update, or return rather than to the
2021). Formal verification provides a complementary struc-      program as an undifferentiated sequence.
Figure 3: Overview of GraphAlignCoder. (A) We parse a solution into an implementation graph whose regions expose
boundaries, updates, and return relations. (B) Template-constrained Lean construction turns formal hints into kernel-checked goal
transitions and a formal proof-flow graph. (C) Region–proof correspondences produce three complementary training targets—
executable code, verification roles, and region-grounded conditions—that update one shared code model. (D) Verification-to-
Code Consolidation continues from the structure-aware checkpoint using executable Python alone; auxiliary outputs are removed
before deployment.


Formal Structure: Lean Proof-Flow Graph                             Then, the tactic engine executes the skeleton as a sequence
A formal proof-flow graph contains proof states as nodes and        of state transformations,
                                                                                        0     1            L
tactic-driven goal transformations as edges. We construct it                          gij →
                                                                                          − gij →
                                                                                                − ··· →− gij .              (5)
through two constrained teacher LLM passes with GPT-5.2.            where each gijℓ
                                                                                    is the current list of unresolved goals. For ex-
The first teacher reads xi , yi , and the region inventory Ri       ample, cases creates branch-specific goals, induction
to identify boundary, invariant, progress, and return require-      creates base and step goals, rw applies a typed equality,
ments. The second maps these requirements to a formal hint          have adds a proved fact to Γij , and exact or simpa
set                                                                                                                    L
                                                                    closes a goal. Successful execution ends with gij    = ∅. The
          HiF = LLMF xi , yi , summary(GIi ), T ,
                                                   
                                                           (2)
                                                                    elaborator compiles a successful trace into a proof term, and
where the fixed library T contain theorem templates and tac-        Lean’s kernel independently checks the term.
tic skeletons. Each hint hij ∈ HiF specifies a known theorem           Rather than using the proof term as an opaque certifi-
shape, tactic plan, proof roles, and lemma families. Restrict-      cate, we extract the goal-state trajectory that produced it. Let
ing the teacher to these libraries makes it select controlled       PiLean = {PijLean }j denote the generated artifacts for task i;
formal building blocks instead of generating an unrestricted        then
Lean program.                                                         GF                                 Lean
                                                                                                              , HiF = (ViF , EiF ).
                                                                                                                   
                                                                       i = ExtractTacticGraph Pi
   Lean turns each accepted hint into the explicit process                                                                       (6)
shown in Figure 3B. First, the generator selects the theorem        The extractor connects goal states with tactic-labeled edges
schema and tactic skeleton whose declared roles match hij :         and records whether transitions perform case analysis, induc-
                     τij = SelectT (hij ).                   (3)    tion, rewriting, invariant propagation, or witness construc-
                                                                    tion. Together, the implementation and proof-flow graphs
Second, it instantiates the schema’s types, variables, hypothe-     form the scaffold
ses, and conclusion with task-specific symbols. The resulting                            Si = (GIi , GF      F
                                                                                                        i , Hi )                 (7)
Lean declaration has context Γij , proposition φij , and a tactic
block inserted after := by:                                         that preserves the provenance of both executable regions and
                                                                    formal transitions. The dashed links between Panels A and
             PijLean = Instantiate(τij , xi , hij ).         (4)    B represent shared semantic roles.
Verification-Graph Injection Training                              Verification-to-Code Consolidation
In Panel C, we show three complementary examples and               Finally, we convert the structure-aware model back to the out-
convert these scaffolds into one code model. In step C1, we        put contract required at deployment. After injection, we stop
project the graph nodes and transitions into compact roles.        requesting concept and obligation responses and continue
Let CiI and CiF denote the roles recovered from the im-            training the same checkpoint on task-to-Python examples.
plementation and proof-flow graphs, and let Ai retain their        This removes the auxiliary output channels while carrying
shared semantic support:                                           their parameter updates into the code-only phase.
                                                                      Let θ0 denote the initial trainable parameters and θ1 the
                  CiI = πI Roles(GIi ) ,
                                        
                                                         (8)       checkpoint produced by Verification-Graph Injection Train-
                    F                 F
                                                                  ing. For the consolidation set Dcon = {(xi , yi )}N      con
                                                                                                                          i=1 , where
                 Ci = πF Roles(Gi ) ,                    (9)
                                                                   yi = (yi,1 , . . . , yi,Ti ) is an executable reference implemen-
                   Ai = CiI ∩ CiF .                        (10)    tation, we initialize θ ← θ1 and optimize the code loss
                                                                                           Ncon     Ti
We retain only implementation roles supported by the source                           1 X        1 X
and use cross-graph overlap as alignment evidence. Con-               Lcon (θ) = −                     log pθ (yi,t | xi , yi,<t ) .
                                                                                     Ncon i=1 Ti t=1
trolled schemas then translate each retained role into a region-
                                                                                                                                  (20)
level condition—for example, a loop update must preserve
                                                                      where Ti is the target length and yi,<t is the target prefix.
its invariant, or a return must establish the required output
                                                                   Optimization yields θ2 , the consolidated checkpoint shown
relation:
                                                                   at the end of Panel D.
               Ci = FilterC (CiI ; Ai , GIi , yi ),        (11)       Let SI and SC be the numbers of injection and consolida-
                                                                   tion steps. The two-phase curriculum can be written as
               O
               ei = Gen(Ci , Ri ),                         (12)                      (
                                                                                       Linject (θ), 1 ≤ s ≤ SI ,
                             ei ; GI , yi ).
               Oi = FilterO (O                                          L(s)
                                   i                       (13)           curr (θ) =                                              (21)
                                                                                       Lcon (θ),    SI < s ≤ SI + SC .
We serialize these accepted sets consistently as
                                                                      Injection and consolidation therefore serve comple-
              ci = ser(Ci ),        oi = ser(Oi ).         (14)    mentary purposes. Injection makes boundaries, invariants,
                                                                   progress conditions, and return relations explicit; consolida-
   In step C2, each scaffold yields three separate prompt–         tion rewards the model for realizing the same organization in
target pairs: code generation xi → yi , concept prediction         Python. At inference, θ2 receives the ordinary programming
qiC → ci , and obligation prediction qiO → oi . The graphs         input and emits one Python solution, with no implementation
are not appended as privileged text to the Python prompt.          graph or proof-flow graph.
Instead, step C3 routes all three examples through the same
model parameters. Consequently, predicting an invariant or                                  Evaluation
boundary condition updates the same representation later           Benchmarks and Inference Protocol
used by pθ (yi | xi ).
                                                                   We evaluate on two complementary code-generation bench-
   For prompt q, response a = (a1 , . . . , aT ), and example
                                                                   marks. LiveCodeBench v6 contains 175 held-out algorithmic
weight w, prompt and padding tokens are masked and the
                                                                   programming tasks and tests generalization beyond the Live-
response-token loss is
                                                                   CodeBench v1–v4 tasks used for training. BigCodeBench
                               T                                   Complete contains 1,140 function-level tasks emphasizing
                            wX                                     API usage, dependency handling, data manipulation, and
         ℓθ (q, a; w) = −         log pθ (at | q, a<t ).   (15)
                            T t=1                                  realistic function completion; its Hard subset contains 148
                                                                   tasks with stricter functional requirements. BigCodeBench
The three objectives specialize this common loss to ex-            is used only for evaluation. The main metric is Pass@1 un-
ecutable tokens, shared verification concepts, and region-         der the single-sample greedy contract above. All compared
grounded obligations:                                              models follow the same evaluation contract: each receives the
                          X 1                                      ordinary programming-task input and produces one Python
               Lcode = −           log pθ (yi | xi ),      (16)    solution with greedy decoding. Pass@1 is the fraction of
                          i
                            |yi |                                  tasks for which the single generated program passes the offi-
                          X 1                                      cial execution suite.
           Lconcept = −            log pθ (ci | qiC ),     (17)
                          i
                            |ci |                                  Baselines and Ablations
                          X 1                                      Baselines Approach We compare GraphAlignCoder
          Lobligation = −          log pθ (oi | qiO ).     (18)
                          i
                            |o i |                                 against base-model and execution-feedback baselines. Base
                                                                   Model is the original Qwen code model. This baseline
The reported injection objective is therefore                      measures how much performance is already present in the
                                                                   pretrained code model. Code-only SFT (Supervised Fine-
         Linject = Lcode + Lconcept + Lobligation .        (19)    Tuning) is a diagnostic checkpoint trained only on Python
Table 1: Overall Pass@1 performance. Values are solved                    Table 2: Difficulty-level Pass@1 by bucket. Values are solved
counts with rates in parentheses; N is the benchmark size.                count with rate in parentheses

Bench.       N      Base        Code-only SFT   CodeRL         GAC        Diff.              N        Code-only SFT     CodeRL          GAC
LCB v6      175   15 (.086)       33 (.189)      38 (.217)    50 (.286)   LiveCodeBench v6
BCB Hard    148    9 (.061)       15 (.101)      16 (.108)    23 (.155)   Easy             43           25 (.581)       25 (.581)     32 (.744)
BCB Full   1140   209 (.183)      354 (.311)    359 (.315)   363 (.318)   Medium           52            6 (.115)        9 (.173)     10 (.192)
                                                                          Hard             80            2 (.025)        4 (.050)      8 (.100)
                                                                          BigCodeBench
                                                                          Easy           396            164 (.414)      163 (.412)    160 (.404)
implementations. CodeRL denotes the reported execution-                   Medium         638            178 (.279)      185 (.290)    189 (.296)
feedback baseline, which improves code generation using                   Hard           106             12 (.113)       11 (.104)     14 (.132)
execution outcomes. It is evaluated with the same input, de-
coding, and one-sample contract as the other models (Le
                                                                                  Table 3: Representative category-level Pass@1.
et al. 2022).
Ablation Variants Verification-graph injection is a di-                   Category               N      Code-only SFT     CodeRL         GAC
agnostic checkpoint that adds the active auxiliary concept-               LiveCodeBench v6
prediction and obligation targets to the primary executable-              Array                  10        5 (.500)        4 (.400)     7 (.700)
                                                                          DP                     35        0 (.000)        0 (.000)     1 (.029)
code target. This measures loss-level graph injection.                    Graph                  19        2 (.105)        2 (.105)     4 (.211)
Consolidation-only is initialized directly from the base                  Simulation             12        3 (.250)       4 (.333)      4 (.333)
model and trained to generate executable Python from tasks                Sorting                 5        2 (.400)        2 (.400)     1 (.200)
                                                                          String                 19        9 (.474)       10 (.526)    12 (.632)
augmented with graph-derived verification information, such
as region-level obligations.                                              BigCodeBench
                                                                          API/Lib             84           34 (.405)      33 (.393)    30 (.357)
                                                                          Crypto              47           12 (.255)      12 (.255)    15 (.319)
Category and Difficulty Annotation                                        FS/OS              186           45 (.242)      49 (.263)    57 (.306)
                                                                          Plot/Vis.          264           79 (.299)      80 (.303)    81 (.307)
We use a separate GPT-5.2 annotation pipeline only for analy-             Web/Text            88           19 (.216)      19 (.216)    26 (.295)
sis grouping. The script batches evaluation tasks, sends com-
pact task summaries to the GPT-5.2 endpoint with tempera-
ture 0, and requires output containing the task identifier, one           for code-only SFT, and 38 for CodeRL. Thus, GraphAlign-
allowed category, an estimated difficulty label, a confidence             Coder solves more than three times as many tasks as the base
score, and a short rationale. For LiveCodeBench, the allowed              model and improves the solved count over code-only SFT and
categories are algorithmic families such as array, string, dy-            CodeRL by 51.5% and 31.6%, respectively. The improve-
namic programming and others. For BigCodeBench, the al-                   ment over both the base and adapted baselines shows that the
lowed categories are function-oriented groups such as data                gain cannot be explained solely by the pretrained model’s
science, plotting/visualization, filesystem/OS, web/text pro-             existing capability or by additional code-only training.
cessing, crypto/encoding and other.                                          The improvement is similarly pronounced on Big-
                                                                          CodeBench Hard. GraphAlignCoder solves 23 tasks, com-
Training and Hardware Setting                                             pared with 9 for the base model, 15 for code-only SFT, and
All GraphAlignCoder checkpoints are initialized from                      16 for CodeRL. This corresponds to 155.6% more solved
Qwen/Qwen3.5-4B-Base and trained with LoRA                                tasks than the base model, 53.3% more than code-only
adapters. The training data follows the executable-reference              SFT, and 43.8% more than CodeRL. On BigCodeBench
policy defined in Methodology. Verification-to-Code Con-                  Full, GraphAlignCoder solves 363 tasks, exceeding the
solidation contains 514 code-only examples and runs for 65                base model’s 209 solved tasks and improving over code-only
optimization steps. All checkpoints use LoRA rank 16, and                 SFT and CodeRL, which solve 354 and 359 tasks, respec-
the final checkpoint uses adapter tensor scale 0.55. Train-               tively. GraphAlignCoder retains their general function-
ing and checkpoint construction run on a local workstation                level capability while achieving much larger gains on Live-
with 2× NVIDIA RTX A6000 GPUs. Final results are com-                     CodeBench v6 and BigCodeBench Hard.
puted from saved greedy generations with the official Live-
CodeBench and BigCodeBench evaluators.                                    RQ2: Where Does GraphAlignCoder
                                                                          Generalize? Analysis Across Difficulty Levels and
                               Results                                    Task Categories
                                                                          Table 2 shows that the LiveCodeBench improvement extends
RQ1: How does GraphAlignCoder compare with
                                                                          across all difficulty levels. On easy problems, GraphAlign-
the base model, code-only SFT, and CodeRL?                                Coder solves 32 of 43 tasks, seven more than either base-
Table 1 demonstrates that GraphAlignCoder consistently                    line. On medium problems, it achieves the best result with
achieves the best Pass@1 across all three evaluation set-                 10 solved tasks. Most notably, GraphAlignCoder solves
tings. On LiveCodeBench v6, GraphAlignCoder solves 50                     8 hard tasks, twice as many as CodeRL and four times as
tasks, compared with 15 for the base-matched model, 33                    many as code-only SFT. A similar advantage appears in
        Table 4: Deployed code-generation performance.                      which learns only from task-to-code pairs, consolidation-
                                                                            only improves LiveCodeBench v6 from 33 to 49 solved tasks
Model                                  LCB v6        BCB        BCB-H       and BigCodeBench Hard from 15 to 19, while remaining
Code-only SFT                          33 (.189)   354 (.311)   15 (.101)   nearly unchanged on BigCodeBench Full (352 versus 354).
GraphAlignCoder-Structural injection   44 (.251)   339 (.297)   17 (.115)   These results indicate that exposing the base model to
GraphAlignCoder-Consolidation-Only     49 (.280)   352 (.309)   19 (.128)   explicit correctness obligations, even when Python is the
GraphAlignCoder                        50 (.286)   363 (.318)   23 (.155)
                                                                            only training output, improves algorithmic and hard-task
                                                                            generation. Consolidation-only is nevertheless weaker than
                                                                            the complete GraphAlignCoder model, which reaches
the more demanding portions of BigCodeBench. Although                       50, 363, and 23 solved tasks on LiveCodeBench v6,
GraphAlignCoder is slightly below the baselines on easy                     BigCodeBench Full, and BigCodeBench Hard, respectively.
tasks, it obtains the best results on both medium and hard                  The full model exceeds consolidation-only by 1, 11, and
tasks, solving 189 and 14 problems, respectively. In particu-               4 tasks, showing that obligation-guided Python generation
lar, it improves over CodeRL from 11 to 14 solved tasks in the              is beneficial but cannot replace the richer representation
hard bucket, corresponding to a 27.3% relative gain. Thus,                  learned through verification-graph injection. The best
the overall improvement of GraphAlignCoder is concen-                       performance arises when auxiliary structural learning and
trated in the settings where maintaining structural consis-                 consolidation are combined.
tency is more difficult.
   The category-level results in Table 3 provide further                                          Conclusion
evidence for this interpretation. On LiveCodeBench v6,
GraphAlignCoder achieves clear improvements in array,                       This paper presented GraphAlignCoder, a training frame-
graph, and string problems. On BigCodeBench, the largest                    work that uses graph-aligned correctness obligations to im-
gains over CodeRL occur in filesystem/OS and web/text pro-                  prove code generation. The key idea is to connect the exe-
cessing, where GraphAlignCoder solves 8 and 7 additional                    cutable structure of Python programs with the correctness
tasks, respectively. It also improves in crypto/encoding and                structure. The model first learns executable code together
plotting/visualization. These categories frequently require a               with graph-derived descriptions of why program regions
sequence of dependent operations—such as preserving in-                     are correct, and then consolidates this knowledge into the
termediate state and constructing a valid return object—                    Python-only output distribution required at deployment.
that closely matches the region-level obligations used by our                  GraphAlignCoder solves 50/175 LiveCodeBench v6
method. Its strongest gains consistently appear in categories               tasks, 23/148 BigCodeBench Hard tasks, and 363/1140 Big-
where correct execution depends on organizing operations                    CodeBench Full tasks, outperforming both code-only SFT
into a coherent, constraint-preserving program.                             and CodeRL. The ablation study shows that structural injec-
                                                                            tion improves LiveCodeBench v6 from 33 to 44 solved tasks,
RQ3: Which Training Components Drive the                                    while consolidation-only provides further benefits by reach-
Performance Gains of GraphAlignCoder?                                       ing 49 LiveCodeBench and 19 BigCodeBench Hard tasks.
                                                                            However, it remains below the complete GraphAlignCoder
Effect of structural injection. Adding graph-aligned
                                                                            model across the three settings. GraphAlignCoder offers
structural supervision to code-only SFT substantially im-
                                                                            a practical way to transfer mechanically checked correct-
proves LiveCodeBench v6, increasing the solved count from
                                                                            ness structure into ordinary code generation. Future work
33 to 44 and Pass@1 from 18.9% to 25.1%. It also improves
                                                                            can extend this framework to richer obligations, additional
BigCodeBench Hard from 15 to 17 solved tasks. These gains
                                                                            programming languages, and repository-level generation.
demonstrate that verification concepts and region-grounded
obligations provide useful supervision beyond executable-
code imitation. In particular, the 11-task improvement on                                          References
LiveCodeBench indicates that structural injection helps the                 Agarwal, V.; Pei, Y.; Alamir, S.; and Liu, X. 2024. CodeMi-
model organize algorithmic solutions more effectively. Struc-               rage: Hallucinations in Code Generated by Large Language
tural injection alone, however, reduces BigCodeBench Full                   Models. arXiv preprint arXiv:2408.08333.
performance from 354 to 339 solved tasks. This result high-
lights an important role of the subsequent training stages:                 Aho, A. V.; Lam, M. S.; Sethi, R.; and Ullman, J. D. 2006.
directly introducing auxiliary structural targets improves                  Compilers: Principles, Techniques, and Tools. Addison-
structure-sensitive generation, but can temporarily shift the               Wesley, 2 edition. ISBN 978-0-321-48681-3.
model away from its original Python-only output distribu-                   Allamanis, M.; Brockschmidt, M.; and Khademi, M. 2017.
tion. Thus, structural supervision is effective, but it must be             Learning to represent programs with graphs. arXiv preprint
consolidated before the resulting checkpoint can serve as a                 arXiv:1711.00740.
broadly capable code generator.
                                                                            Azerbayev, Z.; Schoelkopf, H.; Paster, K.; Dos Santos, M.;
Effect      of    Verification-to-Code      Consolidation.                  McAleer, S. M.; Jiang, A. Q.; Deng, J.; Biderman, S.; and
Consolidation-only tests whether graph-derived obli-                        Welleck, S. 2024. Llemma: An Open Language Model for
gations can directly guide Python generation without                        Mathematics. In The Twelfth International Conference on
verification-graph injection. Compared with code-only SFT,                  Learning Representations.
Cao, J.; Lu, Y.; Li, M.; Ma, H.; Li, H.; He, M.; Wen, C.; Sun,       Informal Proofs. In The Eleventh International Conference
L.; Zhang, H.; Qin, S.; et al. 2025. From informal to formal–        on Learning Representations.
incorporating and evaluating llms on natural language re-            Kim, J.; Guo, W.; Song, D.; Berkeley, U.; and Santa Barbara,
quirements to verifiable formal proofs. In Proceedings of the        U. 2026. Sok: Attack and defense landscape of agentic ai
63rd Annual Meeting of the Association for Computational             systems. In 35nd USENIX Security Symposium (USENIX
Linguistics (Volume 1: Long Papers), 26984–27003.                    Security 26).
Chen, M.; Tworek, J.; Jun, H.; Yuan, Q.; Ponde de                    Le, H.; Wang, Y.; Gotmare, A. D.; Savarese, S.; and Hoi, S.
Oliveira Pinto, H.; Kaplan, J.; Edwards, H.; Burda, Y.;              C. H. 2022. CodeRL: Mastering Code Generation through
Joseph, N.; Brockman, G.; et al. 2021.               Evaluating      Pretrained Models and Deep Reinforcement Learning. In
Large Language Models Trained on Code. arXiv preprint                Advances in Neural Information Processing Systems, vol-
arXiv:2107.03374.                                                    ume 35, 21314–21328.
de Moura, L.; Kong, S.; Avigad, J.; van Doorn, F.; and
                                                                     Leino, K. R. M. 2010. Dafny: An Automatic Program Veri-
von Raumer, J. 2015. The Lean Theorem Prover (Sys-
                                                                     fier for Functional Correctness. In Logic for Programming,
tem Description). In Automated Deduction—CADE-25, vol-
                                                                     Artificial Intelligence, and Reasoning, volume 6355 of Lec-
ume 9195 of Lecture Notes in Computer Science, 378–388.
                                                                     ture Notes in Computer Science, 348–370. Springer.
Springer.
                                                                     Li, Y.; Choi, D.; Chung, J.; Kushman, N.; Schrittwieser, J.;
Ferrante, J.; Ottenstein, K. J.; and Warren, J. D. 1987. The
                                                                     Leblond, R.; Eccles, T.; Keeling, J.; Gimeno, F.; Dal Lago,
Program Dependence Graph and Its Use in Optimization.
                                                                     A.; et al. 2022. Competition-Level Code Generation with
ACM Transactions on Programming Languages and Systems,
                                                                     AlphaCode. Science, 378(6624): 1092–1097.
9(3): 319–349.
Floyd, R. W. 1967. Assigning Meanings to Programs. In                Lozhkov, A.; Li, R.; Ben Allal, L.; Cassano, F.; Lamy-Poirier,
Schwartz, J. T., ed., Mathematical Aspects of Computer Sci-          J.; Tazi, N.; Tang, A.; Pykhtar, D.; Liu, J.; Wei, Y.; et al. 2024.
ence, volume 19 of Proceedings of Symposia in Applied                StarCoder 2 and The Stack v2: The Next Generation. arXiv
Mathematics, 19–32. American Mathematical Society.                   preprint arXiv:2402.19173.
Guo, D.; Ren, S.; Lu, S.; Feng, Z.; Tang, D.; Liu, S.; Zhou, L.;     Ospanov, A.; Farnia, F.; and Mohit, R. 2026. Apollo: Auto-
Duan, N.; Svyatkovskiy, A.; Fu, S.; Tufano, M.; Deng, S. K.;         mated llm and lean collaboration for advanced formal rea-
Clement, C.; Drain, D.; Sundaresan, N.; Yin, J.; Jiang, D.;          soning. Advances in Neural Information Processing Systems,
and Zhou, M. 2021. GraphCodeBERT: Pre-training Code                  38: 41599–41633.
Representations with Data Flow. In The Ninth International           Pearce, H.; Ahmad, B.; Tan, B.; Dolan-Gavitt, B.; and Karri,
Conference on Learning Representations.                              R. 2022. Asleep at the Keyboard? Assessing the Security
Guo, D.; Zhu, Q.; Yang, D.; Xie, Z.; Dong, K.; Zhang, W.;            of GitHub Copilot’s Code Contributions. In 2022 IEEE
Chen, G.; Bi, X.; Wu, Y.; Li, Y. K.; Luo, F.; Xiong, Y.; and         Symposium on Security and Privacy, 754–768. IEEE.
Liang, W. 2024. DeepSeek-Coder: When the Large Language              Peng, S.; Kalliamvakou, E.; Cihon, P.; and Demirer, M. 2023.
Model Meets Programming—The Rise of Code Intelligence.               The Impact of AI on Developer Productivity: Evidence from
arXiv preprint arXiv:2401.14196.                                     GitHub Copilot. arXiv preprint arXiv:2302.06590.
Hoare, C. A. R. 1969. An Axiomatic Basis for Computer                Ravichander, A.; Ghela, S.; Wadden, D.; and Choi, Y. 2025.
Programming. Communications of the ACM, 12(10): 576–                 Halogen: Fantastic llm hallucinations and where to find them.
580, 583.                                                            In Proceedings of the 63rd Annual Meeting of the Associa-
Huang, L.; Yu, W.; Ma, W.; Zhong, W.; Feng, Z.; Wang, H.;            tion for Computational Linguistics (Volume 1: Long Papers),
Chen, Q.; Peng, W.; Feng, X.; Qin, B.; and Liu, T. 2025. A           1402–1425.
Survey on Hallucination in Large Language Models: Prin-              Rozière, B.; Gehring, J.; Gloeckle, F.; Sootla, S.; Gat, I.;
ciples, Taxonomy, Challenges, and Open Questions. ACM                Tan, X. E.; Adi, Y.; Liu, J.; Sauvestre, R.; Remez, T.; et al.
Transactions on Information Systems, 43(2): 1–55.                    2023. Code Llama: Open Foundation Models for Code. arXiv
Hui, B.; Yang, J.; Cui, Z.; Yang, J.; Liu, D.; Zhang, L.; Liu, T.;   preprint arXiv:2308.12950.
Zhang, J.; Yu, B.; Lu, K.; Dang, K.; Fan, Y.; Zhang, Y.; Yang,       Si, S.; Zhao, H.; Gao, C.; Bai, Y.; Wang, Z.; Gao, B.; Luo,
A.; Men, R.; Huang, F.; Zheng, B.; Miao, Y.; Quan, S.; Feng,         K.; Li, W.; Huang, Y.; Chen, G.; et al. 2026. Teaching
Y.; Ren, X.; Ren, X.; Zhou, J.; and Lin, J. 2024. Qwen2.5-           large language models to maintain contextual faithfulness via
Coder Technical Report. arXiv preprint arXiv:2409.12186.             synthetic tasks and reinforcement learning. In Proceedings
Jain, N.; Han, K.; Gu, A.; Li, W.-D.; Yan, F.; Zhang, T.;            of the AAAI Conference on Artificial Intelligence, volume 40,
Wang, S.; Solar-Lezama, A.; Sen, K.; and Stoica, I. 2025.            33001–33009.
LiveCodeBench: Holistic and Contamination Free Evalua-               Spracklen, J.; Wijewickrama, R.; Sakib, A. H. M. N.; Maiti,
tion of Large Language Models for Code. In The Thirteenth            A.; Viswanath, B.; and Jadliwala, M. 2025. We Have a Pack-
International Conference on Learning Representations.                age for You! A Comprehensive Analysis of Package Halluci-
Jiang, A. Q.; Welleck, S.; Zhou, J. P.; Lacroix, T.; Liu, J.;        nations by Code Generating LLMs. In 34th USENIX Secu-
Li, W.; Jamnik, M.; Lample, G.; and Wu, Y. 2023. Draft,              rity Symposium (USENIX Security 25), 3687–3706. USENIX
Sketch, and Prove: Guiding Formal Theorem Provers with               Association. ISBN 978-1-939133-52-6.
Yamaguchi, F.; Golde, N.; Arp, D.; and Rieck, K. 2014.
Modeling and Discovering Vulnerabilities with Code Prop-
erty Graphs. In 2014 IEEE Symposium on Security and
Privacy, 590–604. IEEE.
Yang, K.; Swope, A. M.; Gu, A.; Chalamala, R.; Song, P.; Yu,
S.; Godil, S.; Prenger, R. J.; and Anandkumar, A. 2023. Le-
anDojo: Theorem Proving with Retrieval-Augmented Lan-
guage Models. In Advances in Neural Information Process-
ing Systems, volume 36, 21573–21612.
Zhang, Y.; Zhang, Y.; Leach, K.; and Huang, Y. 2025a. Code-
Grad: Integrating Multi-Step Verification with Gradient-
Based LLM Refinement. arXiv:2508.10059.
Zhang, Z.; Wang, C.; Wang, Y.; Chen, J.; and Zheng, Z.
2025b. LLM Hallucinations in Practical Code Generation:
Phenomena, Mechanism, and Mitigation. Proceedings of the
ACM on Software Engineering, 2(ISSTA): 481–503.
Zhou, J.; Staats, C.; Li, W.; Szegedy, C.; Weinberger, K.;
and Wu, Y. 2024. Don’t Trust: Verify–Grounding LLM
Quantitative Reasoning with Autoformalization. In Inter-
national Conference on Learning Representations, volume
2024, 2544–2563.
Zhuo, T. Y.; Vu, M. C.; Chim, J.; Hu, H.; Yu, W.; Widyasari,
R.; Yusuf, I. N. B.; Zhan, H.; He, J.; Paul, I.; et al. 2025. Big-
CodeBench: Benchmarking Code Generation with Diverse
Function Calls and Complex Instructions. In The Thirteenth
International Conference on Learning Representations.
