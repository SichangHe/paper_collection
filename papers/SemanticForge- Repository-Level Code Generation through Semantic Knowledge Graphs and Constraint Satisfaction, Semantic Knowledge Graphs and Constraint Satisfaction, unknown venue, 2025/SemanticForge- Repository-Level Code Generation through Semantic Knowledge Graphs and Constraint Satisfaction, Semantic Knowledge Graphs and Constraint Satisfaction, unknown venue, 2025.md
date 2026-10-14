                                                SemanticForge: Repository-Level Code Generation through
                                                 Semantic Knowledge Graphs and Constraint Satisfaction
                                                                                Wuyang Zhang1∗ , Chenkai Zhang1 , Zhen Luo2 , Jianming Ma2 ,
                                                                                   Wangming Yuan3 , Chuqiao Gu4 and Chengwei Feng5
                                                   1
                                                       Department of Elec.&Comp. Science, University of Massachusetts Amherst, Amherst, Massachusetts, United States
                                                                2
                                                                    Department of Computer Sys. Engineering, Northeastern University, Boston, Massachusetts, United States
                                                                         3
                                                                             Department of Computer Science, George Mason University, Fairfax, Virginia, United States
                                                           4
                                                               Department of Info. Networking Institude, Carnegie Mellon University, Pittsburgh, Pennsylvania, United States
                                                       5
                                                           Department of Computer & Mathematical Sciences, Auckland University of Technology, Auckland, New Zealand
arXiv:2511.07584v1 [cs.SE] 10 Nov 2025




                                                                                                     *Corresponding author: doggo@ieee.org




                                                                                  Abstract                                  straint Satisfaction, Repository Analysis, Large Language
                                                                                                                            Models, Software Engineering
                                                 Large language models (LLMs) have transformed soft-
                                             ware development by enabling automated code genera-
                                             tion, yet they frequently suffer from systematic errors that
                                             limit practical deployment. We identify two critical fail-
                                                                                                                            1   Introduction
                                             ure modes: logical hallucination (incorrect control/data-
                                                                                              Recent advances in large language models (LLMs) have ush-
                                             flow reasoning) and schematic hallucination (type mis-
                                                                                              ered in a new era of AI-assisted software development. Tools
                                             matches, signature violations, and architectural inconsis-
                                                                                              such as GitHub Copilot, Code-Llama, and ChatGPT now draft
                                             tencies). These errors stem from the absence of explicit,
                                                                                              entire functions or files with a single prompt, reportedly accel-
                                             queryable representations of repository-wide semantics.
                                                 This paper presents S EMANTIC F ORGE, which in-
                                                                                              erating developer productivity [7, 25, 3]. Despite this progress,
                                             troduces four fundamental algorithmic advances for
                                                                                              LLM-generated programs remain brittle in practice: generated
                                             semantically-aware code generation: (1) a novel auto-
                                                                                              code often fails to compile, or worse, compiles but embeds
                                             matic reconciliation algorithm for dual static-dynamic
                                                                                              subtle semantic errors.
                                             knowledge graphs, unifying compile-time and runtime
                                                                                                 A careful inspection reveals two dominant failure modes.
                                             program semantics; (2) a neural approach that learns to
                                                                                              First, logical hallucination arises when the model misreasons
                                             generate structured graph queries from natural language,
                                                                                              about control or data flow—mistakes in reasoning such as iter-
                                             achieving 73% precision versus 51% for traditional re-
                                                                                              ating over an incorrect collection, omitting necessary state mu-
                                             trieval; (3) a novel beam search algorithm with integrated
                                                                                              tations, or producing code that violates expected runtime be-
                                             SMT solving, enabling real-time constraint verification
                                                                                              havior. This class of errors concerns semantic execution logic
                                             during generation rather than post-hoc validation; and
                                             (4) an incremental maintenance algorithm that updates
                                                                                              rather than syntax. Second, schematic hallucination mani-
                                             knowledge graphs in O(|∆R| · log n) time while main-
                                                                                              fests as structural inconsistencies, including type mismatches,
                                             taining semantic equivalence.                    incorrect argument ordering, missing parameters, or calls to
                                                 Our evaluation on R EPO KG-50 (4,250 repository-level
                                                                                              nonexistent functions. These errors arise from violating inter-
                                             tasks across 50 Python projects) demonstrates that these
                                                                                              face or schema constraints of the repository or external APIs.
                                             algorithmic innovations yield substantial improvements:
                                                                                              While logical and schematic hallucinations can co-occur, they
                                             49.8% Pass@1 (15.6% absolute improvement over base
                                                                                              differ fundamentally in their root causes and required reme-
                                             Code-Llama-34B), 49.8% reduction in schematic hallu-
                                                                                              dies. Empirical studies report that even state-of-the-art mod-
                                             cination through SMT-guided generation, and 34.7% re-
                                                                                              els exhibit these errors in 20%–40% of generation attempts
                                             duction in logical hallucination via dual graph analysis.
                                                                                              [22, 27, 28].
                                             The system maintains sub-3s latency through incremental
                                                                                                 Why do these hallucinations persist? Current generation
                                             algorithms while providing formal correctness guarantees
                                             absent in existing approaches.                   pipelines typically combine a parametric LM with retrieval-
                                                 Beyond empirical gains, S EMANTIC F ORGE establishes
                                                                                              augmented prompts. Retrieval surfaces the top-k textual snip-
                                             theoretical foundations for constraint-aware code genera-
                                                                                              pets using lexical or embedding similarity [4, 34]. While re-
                                             tion and demonstrates that explicit semantic modeling can
                                                                                              trieval provides local context, it ignores repository-wide se-
                                             dramatically improve automated programming tools with-
                                                                                              mantics such as transitive call chains, shared global state,
                                             out sacrificing efficiency.
                                                                                              or runtime object types. Likewise, encoder models that in-
                                         Index Terms— Code Generation, Knowledge Graphs, Con- gest static abstract syntax trees (ASTs) or control-flow graphs


                                                                                                                        1
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


(CFGs) focus on intra-function structure and do not persist • We release R EPO KG-50, a curated corpus with aligned
their analysis as a reusable knowledge base [9, 10]. Fi-             {static, dynamic} graphs and oracle implementations, fos-
nally, repair-oriented approaches execute candidates against         tering further research.
unit tests to filter or refine code [13], but they require an or-
acle test suite and do not prevent the model from hallucinating
in the first place.                                               Paper organization. Section 2 reviews related work. Sec-
                                                                  tion 3 formalizes the problem and hallucination taxonomy.
                                                                  Section 4 provides methodology overview. Sections 5–8 detail
This work. We argue that high-quality generation demands our four-stage architecture. Section 9 describes experimental
an explicit, queryable representation of whole-repository se- setup, Section 10 presents results, Section 11 discusses limita-
mantics. To that end, we introduce S EMANTIC F ORGE, which tions, and Section 12 concludes with future directions.
advances beyond system integration through four fundamental
algorithmic innovations:

1. Dual static-dynamic knowledge graphs: Unlike prior                 2     Related Work
   work that uses either static analysis [16] or dynamic traces
   [30] in isolation, we introduce a novel algorithm to auto-         Our work builds on substantial progress in neural code gener-
   matically reconcile static and dynamic program informa-            ation while addressing fundamental limitations in repository-
   tion into a unified graph representation. Our reconciliation       scale synthesis. We organize related work into three key areas
   algorithm provably converges to the ground-truth program           that inform S EMANTIC F ORGE’s design.
   dependence graph as test coverage increases (Theorem 4).

2. Neural query language generation: While existing sys-              2.1    Neural Code Generation
   tems use fixed retrieval strategies (keyword matching or
                                                                      Transformer-based language models have revolutionized auto-
   embedding similarity), we present a learned approach to
                                                                      mated code synthesis. Early work with GPT-based models [3]
   generate structured graph queries from natural language.
                                                                      demonstrated strong performance on isolated function gener-
   Our REINFORCE-based algorithm with graph-aware re-
                                                                      ation tasks, leading to practical systems like GitHub Copilot
   wards achieves 73% precision in context selection versus
                                                                      [7] and specialized models like CodeLlama [18]. These ap-
   51% for traditional retrieval.
                                                                      proaches excel at pattern completion and syntactic correctness
3. SMT-integrated beam search: Prior constraint-aware sys-            but struggle with repository-wide semantic consistency.
   tems [20] verify code after generation. We introduce a                Recent advances have focused on incorporating structural
   novel algorithm that integrates an SMT solver directly into        information into generation models. GraphCodeBERT [9] and
   beam search, enabling real-time constraint verification dur-       UniXcoder [10] encode data flow graphs and AST structures,
   ing generation. This eliminates 89% of schematic errors            improving understanding of local code relationships. How-
   (type mismatches, signature violations, and visibility er-         ever, these models still operate at the function or file level with-
   rors) with only 8.3% latency overhead through our incre-           out persistent semantic representations of entire repositories.
   mental solving strategy.

4. Incremental maintenance with optimality guarantees:                2.2    Repository-Level Code Understanding
   Existing knowledge graph systems require full recompu-
   tation on code changes. We present an incremental up-              Traditional code generation models struggle with repository-
   date algorithm with formal optimality guarantees, achiev-          scale tasks that require understanding cross-file dependencies
   ing O(|∆R|·log n) complexity while maintaining semantic            and architectural constraints [6, 35]. Recent work has begun
   equivalence to full reconstruction (Theorem 3).                    addressing these challenges through three primary paradigms:
                                                                      retrieval-augmented generation, agent-based iterative refine-
                                                                      ment, and planning-based decomposition.
Contributions.    Concretely, this paper makes the following
contributions:
                                                              Retrieval-Augmented Approaches. RAG methods like
• We present the first end-to-end framework that unifies CodeRetriever [14] and RepoCoder [35] use embedding sim-
  repository-level KG construction, neural query planning, ilarity to identify relevant code snippets for generation con-
  and constraint-aware decoding for code generation.          text. Advanced systems like RAG-Code [26] employ dense
• We introduce a dual static–dynamic graph representation embeddings with sophisticated reranking mechanisms. While
  and show that it reduces logical hallucination by 31% on effective for local dependencies, these approaches fundamen-
  a benchmark of 50 Python repositories.                      tally rely on surface-level similarity and miss transitive rela-
                                                              tionships, type constraints, and architectural patterns that span
• We propose a schematic-constraint decoding algorithm that multiple modules. Our knowledge graph approach provides
  eliminates 52% of signature/type errors while adding negli- explicit semantic relationships that pure retrieval cannot cap-
  gible decoding overhead.                                    ture.

                                                                  2
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


Agent-Based Iterative Systems. Recent systems like SWE-                2.5    Positioning of SemanticForge
agent [34] and CodeAgent [29] employ autonomous agents
                                                                       S EMANTIC F ORGE advances the state-of-the-art through four
that iteratively refine solutions through environmental feed-
                                                                       key innovations that address fundamental limitations across all
back, test execution, and error correction. These approaches
                                                                       existing paradigms. Table 1 provides quantitative comparisons
can handle complex multi-step tasks and adapt to unexpected
                                                                       demonstrating these advantages.
challenges through exploration. However, they suffer from
                                                                          Explicit Semantic Representation: Unlike RAG meth-
high computational costs (often requiring 10-50 iterations per
                                                                       ods that rely on implicit embeddings or agent-based systems
task), unpredictable latency, and lack of semantic guarantees.
                                                                       that learn through trial-and-error, we construct comprehensive
In contrast, S EMANTIC F ORGE’s constraint-aware generation
                                                                       knowledge graphs that explicitly capture repository-wide se-
often produces correct solutions in a single pass while provid-
                                                                       mantics. This enables reasoning about transitive dependen-
ing formal correctness guarantees.
                                                                       cies, type propagation, and architectural constraints that are
                                                                       invisible to surface-level similarity matching or iterative explo-
                                                                       ration. Our approach reduces logical hallucination by 31.8%
Planning-Based Decomposition. Planning systems like                    compared to RAG-Code (from 36.2% to 23.1%).
CodePlan [24] decompose complex repository tasks into se-                 Single-Pass Constraint-Guided Generation:                While
quences of localized edits, enabling systematic handling of            agent-based systems require multiple expensive iterations
multi-file modifications. While these approaches provide bet-          and planning approaches often violate constraints across edit
ter task organization than monolithic generation, they typically       boundaries, our SMT-guided beam search integrates constraint
lack the semantic consistency guarantees needed to prevent             satisfaction directly into generation. As shown in Table 1,
constraint violations across edit boundaries. Our neural query         S EMANTIC F ORGE achieves 2.4s average latency (single pass)
planner provides similar decomposition benefits but operates           compared to CodePlan’s 5.7s. Agent-based systems like SWE-
at the semantic level, ensuring global consistency through con-        agent typically require 10-50 iterations [34], suggesting sig-
straint satisfaction.                                                  nificantly higher latency. Our constraint enforcement reduces
                                                                       schematic hallucination by 52.2% compared to the best base-
                                                                       line.
2.3   Constraint-Aware Code Generation                                    Learned Context Selection: Traditional retrieval uses fixed
                                                                       similarity metrics, while agents explore contexts randomly.
Recent work has begun exploring constraint satisfaction in             Our neural query planner learns to identify task-relevant se-
neural code generation. TypeT5 [31] incorporates type in-              mantic relationships, achieving 73% precision in context se-
formation during fine-tuning to improve type correctness.              lection (Section 10) compared to 51% for keyword-based re-
CODEGEN-MONO [21] specializes models for specific pro-                 trieval. This targeted selection contributes to our 2.4× faster
gramming languages to reduce basic syntactic errors.                   generation compared to planning-based approaches.
   More closely related to our approach, LEVER [20] employs               Dual Static-Dynamic Analysis: Previous approaches focus
static analysis to verify generated code against basic type con-       primarily on static program structure or rely on runtime feed-
straints. However, these approaches apply constraints as post-         back loops. Our framework uniquely combines static analysis
processing filters rather than integrating verification into the       with dynamic execution traces in a unified representation, pro-
generation process itself. Our SMT-guided beam search pro-             viding more complete semantic understanding than either ap-
vides stronger guarantees by ensuring constraint satisfaction          proach alone. Dynamic augmentation alone contributes 7.3%
throughout decoding.                                                   improvement in Pass@1 and 12.4% reduction in logical hallu-
                                                                       cination (Section 10.2).
                                                                          Comparative Advantages: Based on our empirical evalu-
                                                                       ation:
2.4   Knowledge Graphs for Code Understand-
      ing                                                                 • vs. Agent-based systems: Deterministic single-pass gen-
                                                                            eration (2.4s) vs. iterative refinement (10-50 iterations
Knowledge graphs have shown promise for representing pro-                   reported for SWE-agent [34]), formal constraint guaran-
gram semantics. CodeKG [16] constructs knowledge graphs                     tees eliminating 89% of type errors, significantly reduced
from documentation and API references for improved code                     computational cost
search, while ProgramKG [30] builds graphs from execution
                                                                          • vs. Planning approaches: 2.4× faster generation (2.4s
traces for debugging applications.
                                                                            vs. 5.7s for CodePlan), 52.2% fewer schematic errors
   Our work differs significantly by constructing comprehen-                through integrated constraint checking, global semantic
sive repository-scale knowledge graphs that integrate both                  consistency through knowledge graphs
static analysis and dynamic execution information. Unlike
previous approaches that focus on specific applications, S E -            • vs. RAG methods: 24.2% higher Pass@1 (49.8% vs.
MANTIC F ORGE uses knowledge graphs as the central repre-                   40.1%), 52.3% reduction in schematic hallucination, ex-
sentation for guiding neural code generation through explicit               plicit architectural understanding through graph represen-
semantic reasoning.                                                         tation


                                                                   3
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


Table 1: Quantitative comparison of S EMANTIC F ORGE against contemporary repository-level approaches from our experimen-
tal evaluation.

                               System                   Pass@1          Latency       SHR        LHR
                                                          (%)            (sec)         (%)        (%)
                               RAG-Code                   40.1              2.9       30.8        36.2
                               CodePlan                   42.3              5.7       31.5        33.8
                               S EMANTIC F ORGE           49.8              2.4       14.7        23.1
                               Improvement vs. best     +17.7%          -17.2%       -52.2%     -31.8%


Computational Cost Analysis. Our detailed overhead anal-              codebases while respecting semantic constraints and architec-
ysis (Section 10.8) reveals that S EMANTIC F ORGE’s 47.1%             tural invariants [6, 35]. Unlike isolated code generation, this
overhead over base Code-Llama is offset by the elimination of         problem requires understanding transitive dependencies, type
iterative refinement. For a typical task, agent-based systems         propagation, and global consistency constraints that span mul-
consume 10-50× more computational resources due to re-                tiple files and modules.
peated generation attempts. With measured energy consump-
tion of 187J per task, S EMANTIC F ORGE achieves 23% net              Formal Problem Statement. Given a repository R =
energy savings when accounting for reduced debugging itera-           {f1 , f2 , . . . , fn } consisting of source files, a natural language
tions from higher Pass@1 rates. The system scales efficiently         instruction u, and an optional test suite T , the goal is to syn-
to repositories up to 500K lines of code with sub-linear query        thesize a code patch ∆R such that the updated repository
complexity (O(n0.73 )), making it practical for real-world de-        R′ = R ∪ ∆R satisfies:
ployment.
                                                                        1. Functional Correctness: ∀t ∈ T : execute(t, R′ ) =
                                                                           PASS
Comparison Limitations. We acknowledge that direct
comparisons with agent-based systems are challenging due to             2. Semantic Consistency: compile(R′ ) = SUCCESS ∧
different evaluation setups and the lack of standardized bench-            typecheck(R′ ) = SUCCESS
marks. While we compare against systems evaluated on our
benchmark, agent-based approaches like SWE-agent were not               3. Behavioral Intent: satisfies(R′ , u) = TRUE
included in our experimental evaluation due to different task           4. Architectural Compliance:               ∀c     ∈      Carch     :
formulations and evaluation metrics. Agent-based approaches                violates(R′ , c) = FALSE
may excel at exploratory tasks requiring extensive trial-and-
error, while S EMANTIC F ORGE is optimized for well-defined              where Carch represents the set of architectural constraints de-
repository integration tasks. Future work should establish uni-       rived from the repository’s design patterns and conventions.
fied benchmarks enabling more precise quantitative compar-
isons across different paradigms.                                     3.2     Hallucination Taxonomy
   These contributions enable S EMANTIC F ORGE to achieve
substantial improvements in repository-level code generation          We formally categorize the systematic errors exhibited by cur-
while maintaining practical scalability and deterministic per-        rent LLM-based code generation systems into two primary
formance for real-world deployment.                                   classes, each requiring distinct mitigation strategies.

                                                                      Logical Hallucination.        We define logical hallucination as
3     Problem Definition and Formaliza- errors in program semantics that lead to functionally incorrect
                                        code despite syntactic validity. Formally, a generated code se-
      tion                              quence y exhibits logical hallucination if:
This section formalizes the repository-level code generation
problem and provides precise definitions of the hallucination               compile(y) = SUCCESS                                         (1)
phenomena that motivate our approach. We establish the math-                             ∧ ∃t ∈ T : execute(t, y) ̸= expected(t)
ematical framework that underpins our solution and analyze
the computational complexity of the problem space.                      Common manifestations include:
                                                                         • Control Flow Errors: Incorrect loop bounds, missing
3.1    Repository-Level Code Generation                                    conditionals, wrong branching logic
We define repository-level code generation as the task of syn-           • Data Flow Errors: Operating on wrong variables, incor-
thesizing code patches that integrate seamlessly with existing             rect data transformations, missing state updates


                                                                  4
                                      Journal of Emerging Applied Artificial Intelligence (JEAAI)


       • API Misuse: Calling methods in wrong order, ignoring12 @app.route(’/login’, methods=[’POST’])
         return values, improper error handling              13 def login():

                                                                   14           username = request.json.get(’username’)
       Example: Consider implementing a cache eviction policy: 15               password = request.json.get(’password’)
                                                                   16           if authenticate_user(username, password):
 1 # Instruction: "Remove oldest entries when
                                                 17                                 return {"status": "success"}
       cache is full"
                                                 18                             return {"status": "failed"}
 2 # Incorrect (Logical Hallucination):

 3 def evict_if_full(self):

 4     if len(self.cache) >= self.max_size:
 5         # Wrong: removes newest instead of       3.3 Complexity Analysis
               oldest
 6         self.cache.pop(list(self.cache.keys()
                                                    We analyze the computational complexity of repository-level
               )[-1])                               code generation to establish theoretical bounds and justify our
 7
                                                                          architectural choices.
 8 # Correct:
 9 def evict_if_full(self):                                               Context Selection Complexity. For a repository with n
10     if len(self.cache) >= self.max_size:                               code entities and m dependency relationships, the naive ap-
11         oldest_key = next(iter(self.cache))                            proach of considering all possible context subsets has com-
12         self.cache.pop(oldest_key)                                     plexity O(2n ). Our neural query planner reduces this to
                                                                          O(n log n) through learned heuristics and graph-based prun-
                                                                          ing.
     Schematic Hallucination. We define schematic hallucina-
     tion as violations of type systems, function signatures, or struc-
                                                                        Constraint Verification Complexity. Given k constraints
     tural constraints that prevent code from compiling or integrat-
                                                                        extracted from the knowledge graph, naive constraint check-
     ing correctly. Formally:
                                                                        ing requires O(k · |y|) time for a generated sequence y. Our
                                                                        incremental SMT-based approach achieves O(k + |y|) through
         schematic hallucination(y, G) = |{c ∈ C(G) :                   state caching and incremental solving.
                                        violates(y, c)}| > 0    (2)
                                                                    Graph Maintenance Complexity. For a code change ∆R
        where C(G) is the set of constraints extracted from reposi- affecting |∆R| entities in a repository of size n, full re-
     tory knowledge graph G.                                        analysis requires O(n2 ) time due to cross-reference resolu-
        Categories include:                                         tion. Our incremental maintenance achieves O(|∆R| · d ·
                                                                    log n) through dependency tracking and selective recomputa-
        • Type Mismatches: Passing wrong types to functions, in- tion, where d is the maximum dependency depth.
          compatible return types
       • Signature Violations: Wrong parameter counts, missing            3.4    Problem Hardness and Approximation
         required arguments
                                                                 We establish the theoretical hardness of optimal repository-
        • Scope Violations: Accessing private members, using un- level code generation and justify our approximation strategies.
          defined variables                                         Theorem 1 (Problem Hardness). The optimal repository-
                                                                 level code generation problem, defined as finding the
        • Import Errors: Missing imports, circular dependencies  minimum-cost code patch satisfying all constraints, is NP-
                                                                 hard. We define the cost function as:
       Example: Consider adding authentication to an API end-
     point:                                                                 Cost(∆R) = α · d (∆R)                            (3)
                                                                                                           e
 1 # Instruction: "Add authentication check to                                                     + β · pc (∆R) + γ · da (∆R)
       login endpoint"
 2 # Incorrect (Schematic Hallucination):                                 where de is the patch edit distance (number of lines changed),
 3 @app.route(’/login’, methods=[’POST’])                                 pc is the constraint violation penalty, da is the architectural
 4 def login():
                                                                          deviation score, and α, β, γ are weighting coefficients.
 5     # Wrong: authenticate_user takes (                                    Proof Sketch: We reduce from the Boolean Satisfiabil-
           username, password)
                                                                          ity Problem (SAT). Given a SAT instance with variables
 6     # but only username is provided
                                                                          x1 , . . . , xn and clauses c1 , . . . , cm , we construct a repository
 7     if authenticate_user(request.json.get(’
           username’)):                                                   where each variable corresponds to a code entity and each
 8         return {"status": "success"}                                   clause corresponds to a constraint. Finding a satisfying as-
 9     return {"status": "failed"}                                        signment is equivalent to finding a valid code patch.
10                                                                           This hardness result motivates our use of approximation al-
11   # Correct:                                                           gorithms and heuristic search strategies. Our neural query


                                                                      5
                                   Journal of Emerging Applied Artificial Intelligence (JEAAI)


planner provides a polynomial-time approximation, while the four requirements established in Section 3: functional correct-
SMT-based decoder ensures constraint satisfaction within the ness, semantic consistency, behavioral intent, and architectural
feasible search space.                                       compliance.
                                                                Figure 1 illustrates the complete S EMANTIC F ORGE
Approximation Quality. We define the approximation ratio pipeline, showing how each stage addresses specific aspects
of our approach as:                                          of the repository-level code generation problem:

                           E[Cost(∆RSF )]
                     ρ=                                       (4)
                                                             Stage I: Repository Knowledge Graph Construction
                           E[Cost(∆R∗ )]
                                                             (section 5). We construct a heterogeneous knowledge
where ∆RSF is the solution produced by S EMANTIC F ORGE graph G = ⟨V, E⟩ that explicitly encodes repository
and ∆R∗ is the optimal solution.                             semantics through static analysis and dynamic trace col-
   Empirical analysis on our benchmark suite shows ρ ≤ 1.3 lection. Each node v ∈ V represents a code entity
for most repository types, indicating that our solutions are with type τ (v) ∈ {FUNC, CLASS, VAR, FILE, TEST, API},
within 30% of optimal on average.                            while edges e = (vi , ρ, vj ) ∈ E capture relationships ρ ∈
                                                             {CALLS, DEFINES, IMPORTS, MUTATES, RETURNS, INSTANCE O F}.
3.5     Solution Requirements
                                                             Stage II: Neural Query Planner (section 6). A neural net-
Based on the problem analysis, we identify four key require-
                                                             work πϕ transforms natural language instructions into graph
ments that any effective solution must address:
                                                             queries that extract task-relevant context. Given instruction u,
                                                             the planner generates query q = πϕ (u) which retrieves sub-
 1. Semantic Awareness: The system must understand
                                                             graph Gu = Exec(q, G). The planner is trained via REIN-
    repository-wide semantics, not just local patterns
                                                             FORCE [32] to maximize downstream code generation qual-
 2. Constraint Enforcement: Hard constraints must be sat- ity:
    isfied, not merely approximated                                             J (ϕ) = E(u,y) [R(y, Gu )]                (5)
    3. Scalability: The approach must handle repositories with where R measures functional correctness and constraint satis-
       millions of lines of code                               faction.
  4. Adaptability: The system must evolve with the reposi-
     tory to maintain accuracy                                 Stage III: Schematic-Constraint Decoder (section 7). We
                                                               formulate code generation as constrained optimization, en-
   These requirements directly motivate the four-stage ar- suring generated code satisfies semantic constraints extracted
chitecture of S EMANTIC F ORGE, where each component ad- from Gu :
dresses specific aspects of the problem complexity while main-
taining overall system coherence.                                            ŷ = arg max log Pθ (y | u, Gu )         (6)
                                                                                                  y

                                                                                               s.t.   C(y, Gu ) = ∅
4      Methodology
                                                                         where C returns violated constraints. We solve this through
Our aim is to inject explicit, executable semantics into the             SMT-guided beam search [5] that prunes constraint-violating
code generation loop. By executable semantics, we mean a                 paths during generation.
repository-wide, queryable representation that links code en-
tities to their runtime behaviors and enforceable constraints,
                                                                         Stage IV: Continual Maintenance Agent (section 8). An
allowing code generation to be guided by verifiable seman-
                                                                         autonomous agent monitors repository changes and incremen-
tics rather than pattern matching. S EMANTIC F ORGE there-
                                                                         tally updates the knowledge graph to maintain semantic fi-
fore proceeds in two macro stages—graph construction and
                                                                         delity. The agent achieves O(|∆R| · d · log n) update com-
graph-aware generation—underpinned by continual mainte-
                                                                         plexity through dependency tracking and selective recomputa-
nance. This section provides a comprehensive overview of our
                                                                         tion, where |∆R| is the number of modified entities, d is the
four-stage architecture and establishes the mathematical foun-
                                                                         maximum dependency depth, and n is the repository size.
dations for each component.

4.1     Framework Overview                                               4.2   Key Innovations Beyond Integration
Given a repository snapshot R = {f1 , . . . , f|R| } consisting of       While S EMANTIC F ORGE integrates multiple techniques, each
source files and accompanying tests, and a natural language              component introduces fundamental algorithmic innovations
instruction u, our objective is to synthesize a code patch ∆R            that advance the state-of-the-art independently. Table 2 sum-
such that the updated repository R′ = R ∪ ∆R satisfies the               marizes these contributions.

                                                                     6
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)




Figure 1: Complete architecture of the S EMANTIC F ORGE system. The pipeline consists of four integrated stages: (I) Reposi-
tory Knowledge Graph Construction combining static analysis and dynamic traces, (II) Neural Query Planner that transforms
instructions into graph queries, (III) Schematic-Constraint Decoder ensuring semantic correctness, and (IV) Continual Main-
tenance Agent for incremental updates. Each stage addresses specific aspects of the repository-level code generation problem
while maintaining overall system coherence.

Table 2: Novel contributions of each S EMANTIC F ORGE component compared to prior work. Each row highlights a specific
algorithmic or theoretical advance beyond system integration.

   Component                    Prior Art Limitation              Our Novel Contribution                Key Innovation
   Knowledge Graph              Static    analysis only           Dual static-dynamic graph             Unified      representa-
                                (CodeKG) or dynamic               with automatic reconciliation         tion capturing both
                                only (ProgramKG)                  algorithm                             compile-time and run-
                                                                                                        time semantics
   Query Planner                Fixed retrieval strategies        Learned query language gen-           First neural planner for
                                (BM25, dense embeddings)          eration via REINFORCE with            structured code queries
                                                                  graph-aware rewards
   Constraint Decoder           Post-hoc    verification          SMT-integrated beam search            Real-time semantic ver-
                                (LEVER) or syntax-only            with incremental constraint           ification during genera-
                                constraints                       solving                               tion
   Maintenance                  Full recomputation or man-        Provably optimal incremental          Theoretical guarantee of
                                ual updates                       algorithm with O(|∆R|) com-           consistency with mini-
                                                                  plexity                               mal computation


4.3   Design Rationale                                                to identify relevant context that spans multiple modules while
                                                                      avoiding information overload.
Our architecture addresses the fundamental limitations of cur-
rent code generation systems through four key design princi-
ples:
                                                                      Constraint-Aware Generation. We embed formal verifica-
Explicit Semantic Representation. Rather than relying on              tion directly into the generation process, ensuring that out-
implicit pattern matching, we construct an explicit knowledge         put satisfies semantic constraints before emission. This elimi-
graph that captures repository semantics. This enables rea-           nates schematic hallucination at the source rather than requir-
soning about transitive dependencies, type propagation, and           ing post-hoc correction.
architectural constraints that are invisible to embedding-based
approaches.
                                                                  Continual Adaptation. Our maintenance agent ensures the
Learned Context Selection. Instead of using fixed retrieval system evolves with the repository, maintaining accuracy as
strategies, we learn a neural query planner that adapts to repos- code changes over time. This addresses the temporal mismatch
itory structure and task requirements. This allows the system between training data and deployment environments.


                                                                  7
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


4.4   Mathematical Foundations                                       5     Repository Knowledge Graph Con-
We establish the mathematical framework that underlies each                struction
system component:
                                                                     Accurate code generation requires comprehensive understand-
Knowledge Graph Formalization. The repository knowl-                 ing of repository semantics—not just what the code says (static
edge graph G approximates the ground-truth program depen-            structure), but also what it does (runtime behavior). Tradi-
dence graph G ∗ by minimizing structural Hamming distance:           tional knowledge graph approaches rely exclusively on either
                                                                     static analysis [16] or dynamic execution traces [30], each cap-
                   dSH (G, G ∗ ) = |V△V ∗ |                (7)       turing only partial semantics. Static analysis provides com-
                                                                     plete coverage but cannot resolve polymorphic behavior or
                                + |E△E ∗ |
                                                                     runtime type information. Dynamic analysis captures concrete
                                                                     execution patterns but depends on test coverage and may miss
where △ denotes symmetric difference. Our dual static-
                                                                     unexecuted paths.
dynamic extraction strategy provides complementary approxi-
                                                                        This section presents the first algorithm to automatically
mations that converge to G ∗ as test coverage increases.
                                                                     reconcile static analysis and dynamic execution traces into
                                                                     a unified knowledge graph. Our dual representation cap-
Query Planning Optimization. The planner parameters ϕ                tures both compile-time structure and runtime behavior, re-
are optimized to maximize expected code generation reward:           ducing logical hallucination by 31% compared to static-only
                                                                     approaches. The key innovation lies in an automatic recon-
                ϕ∗ = arg max E(u,y)∼D                      (8)       ciliation algorithm that merges complementary information
                            ϕ
                                                                     sources while maintaining consistency guarantees.
                     [R (y, Exec(πϕ (u), G))]

We use REINFORCE [32] with synthetic data warm-start and 5.1 Problem Formulation
contrastive learning on static-dynamic graph pairs.         We formalize the knowledge graph construction problem as
                                                            approximating the ground-truth program dependence graph G ∗
Constraint Satisfaction. Our decoder enforces constraints by minimizing:
C extracted from the knowledge graph. Constraints are en-
coded as SMT formulas [5] that can be checked incrementally              dSH (G, G ∗ ) = |V△V ∗ | + |E△E ∗ |        (9)
during beam search. The constraint set includes:
                                                            where G = ⟨V, E⟩ is our constructed graph and △ denotes
  • Type constraints: type(e) ⊆ expected type(e)            symmetric difference.

  • Signature constraints: arity(f ) = |args(f )|
                                                                     5.2   Unified Graph Schema
  • Visibility constraints: accessible(v, scope)                 Our schema captures program semantics through typed nodes
                                                                 v ∈ V with τ (v) ∈ {FUNC, CLASS, VAR, FILE, TEST, API}
   • Architectural constraints: satisfies(pattern, design rule)  and labeled edges e = (vi , ρ, vj ) ∈ E where ρ ∈
                                                                 {CALLS, DEFINES, IMPORTS, MUTATES, RETURNS, INSTANCE O F}.
  This mathematical framework provides theoretical ground-
                                                                 Nodes carry semantic attributes including type signatures,
ing for our empirical results and enables principled analysis of
                                                                 scope constraints, and docstring embeddings that enable
system behavior across different repository types and scales.
                                                                 constraint extraction during generation.

Comparison with Traditional Approaches. To illustrate
                                                                     5.3   Dual Analysis Algorithm and Performance
our innovation, consider a task requiring modification of a
data processing pipeline. A traditional RAG approach might           Our three-phase reconciliation algorithm—(1) static extrac-
retrieve a localized code snippet containing the target func-        tion via whole-program analysis, (2) dynamic augmentation
tion but miss cross-file dependencies or hidden imports, caus-       through test instrumentation, and (3) intelligent merging that
ing the generated patch to fail compilation. In contrast,            refines polymorphic targets—provably converges to ground
our knowledge graph approach resolves the full dependency            truth G ∗ as test coverage increases. Table 3 summarizes the
structure—including transitive imports, type constraints from        algorithm’s complexity, empirical performance, and impact on
parent classes, and API contracts from external libraries—           generation quality.
and enforces these constraints during generation, ensuring the          The dual approach adds 4.5s extraction overhead (55% in-
patch integrates correctly without manual debugging. This            crease) but captures 31% more edges—primarily runtime call
fundamental difference between surface-level retrieval and se-       targets and polymorphic type instantiations invisible to static
mantic understanding drives our significant performance im-          analysis. This richer semantic representation directly trans-
provements.                                                          lates to generation improvements: 7.3% higher Pass@1, 34%


                                                                 8
                                Journal of Emerging Applied Artificial Intelligence (JEAAI)




                 Figure 2: Dual static-dynamic knowledge graph construction with automatic reconciliation.


Table 3: Knowledge graph construction: complexity analysis Implementation details. Our construction pipeline lever-
and empirical validation on 50 repositories.               ages pylance for Python static analysis and custom instru-
                                                           mentation for trace collection. Graph storage, distributed pro-
 Metric                         Static Only  Dual (Ours)   cessing strategies, caching optimizations, and Neo4j integra-
                          Complexity                       tion details are provided in the supplementary material. These
 Time                            O(n log n)   O(n log n)   implementation choices achieve the performance characteris-
 Space                           O(n + m)     O(n + m)     tics shown in Table 3 but are orthogonal to our core algorith-
 Incremental update              O(k log n)   O(k log n)   mic contribution.
                  Construction Performance
 Extraction time (100K LOC)         8.2s          12.7s
 Graph size (avg nodes)           15.3K           15.8K              6    Neural Query Planner
 Graph size (avg edges)           48.2K       63.1K (+31%)
                  Generation Quality Impact                          Determining which subset of a repository knowledge graph
 Pass@1 improvement              baseline         +7.3%              is relevant to a specific coding task represents a fundamen-
 Type error reduction            baseline         -34%               tal challenge in repository-level code generation. Tradi-
 Dependency coverage               1.0×            2.3×              tional retrieval methods use fixed strategies—keyword match-
                                                                     ing (BM25) or embedding similarity—that rely on surface-
                                                                     level lexical overlap. These approaches systematically miss
                                                                     transitive dependencies, type constraints, and architectural pat-
                                                                     terns that span multiple modules but lack textual similarity to
fewer type errors, and 2.3× better transitive dependency cov-
                                                                     the query.
erage (Section 10.2).
                                                                        This section introduces the first learned approach to gen-
   Convergence guarantee: As test coverage c → 100%, our             erate structured graph queries from natural language instruc-
dual graph G → G ∗ (proof in supplementary material). The            tions. Rather than retrieving based on predetermined similarity
key insight is that dynamic information monotonically refines        metrics, our REINFORCE-based algorithm learns repository-
static analysis without introducing inconsistencies—each exe-        specific query patterns that capture semantic relationships es-
cution trace adds edges and constraints that either confirm or       sential for code generation. Our neural query planner achieves
specialize static predictions.                                       73% precision in context selection compared to 51% for tra-


                                                                 9
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)




               Figure 3: Neural query planner transforming instructions to graph queries via learned generation.


ditional retrieval, directly contributing to improved generation     2: Initialize beam B ← {¡start¿}
quality.                                                             3: while not all beams complete do
                                                                     4:     Expand beams with valid tokens per grammar
6.1   Problem Formulation                                            5:     Prune to top-k by likelihood
                                                                     6: end while
We formulate context selection as learning a mapping πϕ :            7: return highest scoring complete query
U → Q from natural language instructions to graph queries.   Stage 3: Query Optimization. Apply predicate pushdown
Unlike CoCoMIC [6] which uses syntactic matching, we opti- and traversal elimination for efficiency.
mize:
          ϕ∗ = arg max E(u,y)∼D [P(y|Gu , u)]        (10)
                        ϕ
                                                                    6.3   REINFORCE Training with Graph-Aware
where Gu = Exec(πϕ (u), G) is the retrieved subgraph.                     Rewards
                                                              Training the query planner requires learning without direct
6.2   Query Generation Algorithm                              query supervision—we observe only task descriptions and
Our key innovation is learning to generate structured queries ground-truth code, not optimal queries. We employ REIN-
rather than using fixed retrieval. The algorithm has three FORCE [32] with carefully designed variance reduction:
stages:
   Stage 1: Instruction Encoding. We encode natural lan-       J (ϕ) = Eq∼πϕ (·|u) [(R(y, Gu ) − bψ (u)) · log πϕ (q|u)] (11)
guage u using Flan-T5 augmented with repository embeddings
capturing codebase-specific patterns.                         Baseline Network Architecture. The baseline bψ (u) is a
   Stage 2: Constrained Query Decoding. We generate separate critic network that estimates expected reward without
query sequences respecting our graph query grammar:           executing queries. It shares the same Flan-T5 encoder as the
  1: Input: Encoded instruction h, Graph schema S             policy πϕ but uses a distinct prediction head: a 2-layer MLP


                                                               10
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


with 512 hidden units that outputs scalar reward estimates. reduces total training time by 52% and improves final perfor-
This architecture enables the baseline to leverage instruction mance by 4.1%.
semantics while training separately from the policy.
                                                                    6.4   Learned Query Expansion
Joint Training Procedure. We train policy and baseline
jointly through alternating optimization:                           Unlike fixed expansion rules, we learn repository-specific pat-
                                                                    terns for query augmentation. Given seed nodes from the ini-
  1: for each training batch of (u, y) pairs do
                                                                    tial query, we apply learned motif-based expansion:
  2:     Sample query q ∼ πϕ (·|u), execute to get Gu
         Generate code, compute reward R(y, Gu )
                                                                                                 [
  3:
                                                                                   Guexp = Gu ∪       match(m, Gu )            (13)
  4:     Update baseline: ψ ← ψ − β∇ψ ∥bψ (u) − R(y, Gu )∥2                                     m∈M
  5:     Compute advantage: A = R(y, Gu ) − bψ (u)
  6:     Normalize: Â = (A − µbatch )/σbatch                       where M are learned co-modification patterns (e.g., model →
  7:     Update policy: ϕ ← ϕ + αÂ∇ϕ log πϕ (q|u)                  serializer → test).
  8: end for                                                           This captures implicit dependencies: modifying a data
                                                                    model automatically retrieves related serializers and end-
                                                                    points.
Variance Reduction Techniques. Beyond baseline subtrac-
tion, we employ four complementary strategies:
   1. Advantage Normalization: Batch-wise normalization 6.5 Empirical Results
of advantages (line 5 above) stabilizes gradients across diverse Our neural query planner significantly outperforms fixed re-
tasks with varying reward scales.                                trieval strategies:
   2. Gradient Clipping: We clip policy gradients to [−1, 1]
per parameter, preventing destabilization from rare high-            • Precision: 73% vs. 51% for BM25 retrieval
reward samples.
                                                                     • Coverage: Captures 2.3× more transitive dependencies
   3. Entropy Regularization: Adding λH[πϕ (·|u)] to the
objective (λ = 0.01) encourages exploration and prevents pre-        • Efficiency: Sub-linear O(n1/k · m) query complexity
mature convergence to suboptimal queries.
   4. Reward Scaling: Our multi-objective reward combines           Ablation studies (Section 10.2) show that learned query
weighted components:                                             planning   contributes 6.2% to overall Pass@1 improvement.

  R(y, Gu ) = w1 · Rtest (y) + w2 · Rtype (y) − w3 · |Gu | (12)     6.6   Theoretical Guarantees
where Rtest measures functional correctness (0-1), Rtype mea- Theorem 4 (Convergence). With probability ≥ 1 − δ, after T
sures type violations (0-1), and |Gu | penalizes over-retrieval. iterations:
Weights (w1 = 1.0, w2 = 0.3, w3 = 0.001) are tuned on vali-                                       r            !
dation data.                                                                                        log(|H|/δ)
                                                                          J (ϕT ) ≥ max J (ϕ) − O                   (14)
                                                                                    ϕ∈H                  T
Training Stability and Hyperparameters. We use Adam
                                                                       Theorem 5 (Query Complexity). Our hierarchical execu-
optimizer with learning rate α = 5 × 10−5 for the policy and
                                                                    tion achieves O(n1/k ·m) time vs. O(n·m) for naive traversal.
β = 1 × 10−4 for the baseline. Batch size is 32, and we apply
                                                                       These guarantees ensure practical convergence (typically
exponential reward discounting with γ = 0.95 to favor imme-
                                                                    10K steps) and sub-second query execution even for million-
diate correctness over long-term metrics. Training converges
                                                                    node graphs.
within 10K steps on typical repositories.
   Empirically, the baseline network reduces gradient variance
by 67% compared to a constant baseline (measured via gra-           7     Schematic-Constraint Decoder
dient norm variance across training batches). Advantage nor-
malization further reduces variance by 43%. Gradient clip-          Language models generate code token-by-token based on
ping prevents occasional spikes from difficult tasks. Com-          learned statistical patterns, with no inherent mechanism to
bined, these techniques enable stable training: gradient norms      ensure the output satisfies the formal requirements of pro-
decrease monotonically after 2K steps, and validation perfor-       gramming languages or repository-specific constraints. This
mance plateaus around 8K steps with final policy achieving          fundamental mismatch between unconstrained text generation
73% context precision.                                              and structured code synthesis leads to schematic hallucina-
                                                                    tion—code that appears plausible but violates type systems,
Cold Start Strategy. To address initial exploration chal-           function signatures, or architectural invariants.
lenges, we warm-start training with 10K synthetic instruction-         Existing approaches to this problem apply constraints as
query pairs generated through dependency analysis. Each             post-generation filters [20, 23, 31]. While this can detect er-
repository function’s static dependencies provide ground-truth      rors, it wastes computation generating invalid code and pro-
queries for hypothetical modification tasks. This initialization    vides no guidance to the model during generation. This section


                                                               11
                                Journal of Emerging Applied Artificial Intelligence (JEAAI)




                       Figure 4: SMT-integrated beam search pruning invalid paths during generation.


presents the first beam search algorithm with integrated SMT 7.3 Novel SMT-Integrated Beam Search Algo-
solving for real-time constraint verification during decoding.        rithm
By pruning constraint-violating paths as they emerge, our ap-
proach eliminates 89% of type errors with only 6% latency Our key innovation integrates Z3 SMT solver [5] directly into
overhead, transforming constraint satisfaction from post-hoc beam search:
validation to integrated generation control.                    1: Input: Context Gu , Instruction u, Beam width k
                                                                2: Initialize beams B ← {(ϵ, SAT)} // empty sequence, SAT
                                                                   state
7.1 Problem Formulation                                         3: while not all beams complete do
                                                                4:     for each beam (y, s) ∈ B do
We formulate constrained generation as optimization with se-    5:          T ← LM.next tokens(y, u, Gu ) // top tokens
mantic constraints:                                             6:          for each token t ∈ T do
                                                                7:              s′ ← s ∪ constraints(y · t, Gu )
                ŷ = arg max log Pθ (y | u, Gu )          (15)  8:              if SMT.check(s′ ) = SAT then
                          y∈Y
                                                                9:                  Add (y · t, s′ ) to candidates
                  subject to C(y, Gu ) = ∅                (16)
                                                               10:              end if
                                                               11:          end for
where C(y, Gu ) returns constraint violations. Unlike Al- 12:          end for
phaCode [15] which struggles with semantic errors post- 13:            B ← top-k candidates by score
generation, we enforce constraints during generation.          14: end while
                                                                 Incremental solving reuses learned clauses, achieving near-
7.2 Constraint Types and SMT Encoding                          constant  constraint checking time.

We extract four constraint classes from Gu and encode them as   7.4   Optimization Strategies
SMT formulas:
                                                                We achieve 6% overhead through three key optimizations:
 1. Type constraints: type(e) ⊆ expected type(e)                   1. Incremental Solving: Reuse solver state across beams
                                                                sharing prefixes via trie-based caching.
                                                                   2. Constraint Preprocessing: Eliminate always-satisfied
 2. Signature constraints: arity(f ) = |args(f )|
                                                                constraints and partition independent constraint sets.
                                                                   3. Batch Verification: Check multiple token proposals in
 3. Visibility constraints: accessible(v, scope)
                                                                single solver calls using assumption literals.
                                                                   These optimizations reduce average constraint checking
 4. Architectural constraints: satisfies(pattern, rule)         from 23ms to 1.4ms per token.

   Each constraint type maps to specific SMT theories: types
                                                                  7.5 Empirical Validation
use algebraic datatypes, signatures use uninterpreted func-
tions, visibility uses graph reachability, and architectural pat- Our SMT-integrated decoder dramatically reduces schematic
terns use custom predicates.                                      hallucination:


                                                            12
                                   Journal of Emerging Applied Artificial Intelligence (JEAAI)


    • Error Reduction: 89% of type errors eliminated vs. un- graphs. Our approach achieves O(|∆R| · d · log n) complex-
      constrained generation                                 ity while maintaining provable semantic equivalence to full
                                                             reconstruction, enabling real-time adaptation as repositories
    • Performance: 6% latency overhead (2.4s → 2.54s aver- evolve. The key innovation lies in combining impact analy-
      age)                                                   sis with lazy cross-reference resolution to update only affected
                                                             graph regions while maintaining global consistency.
    • Coverage: Handles 94% of repository constraints with-
      out timeout
                                                                      8.1   Problem Formulation
  Ablation studies (Section 10.2) show constraint enforce- Let R denote a repository at time t = 0, and let ∆R rep-
                                                                       0                                                 i
ment is critical: removing it increases schematic hallucination resent the set of code modifications (additions, deletions, up-
by 112% (relative).                                             dates)Pat time step i. The repository at time t is thus Rt =
                                                                         t
                                                                R0 + i=1 ∆Ri . Our goal is to maintain an up-to-date knowl-
7.6 Theoretical Guarantees                                      edge graph Gt that accurately represents the semantic structure
                                                                of Rt .
Theorem 6 (Optimality). If valid completion y ∗ exists within      Formally, let FE denote the semantic extraction function
top-k at each prefix, our algorithm finds it.                   that constructs a knowledge graph from source code (as de-
  Theorem 7 (Complexity). Time complexity is O(n·k ·|Σ|· fined in Section 5). The maintenance problem requires ensur-
C) where C ≈ O(1) due to incremental solving.                   ing:
  The key insight: constraint monotonicity enables early                                            t
                                                                                                            !
                                                                                                   X
pruning without sacrificing optimality.                                           Gt = FE R0 +         ∆Ri                 (17)
                                                                                                         i=1

                                                                         The naive solution—recomputing FE (Rt ) after each
7.7    Summary
                                                                      change—has complexity O(n log n) where n is the repository
Our SMT-integrated beam search represents a paradigm shift            size. Our key insight is the locality of change principle: most
from post-hoc validation to real-time constraint enforcement.         code modifications affect only a small, localized portion of
By pruning invalid paths during generation, we eliminate the          the semantic graph. By identifying and updating only these
vast majority of schematic errors while maintaining interactive       affected regions, we achieve complexity O(|∆R| · d · log n)
performance. This approach is general: the same framework             where |∆R| is the change size and d is the maximum depen-
handles type constraints, API contracts, and architectural rules      dency depth.
across different programming languages and paradigms.
                                                                      8.2   Impact Analysis Algorithm
8     Continual Knowledge Graph Main- To achieve incremental updates, we must precisely identify
                                      which parts of the knowledge graph are affected by code
      tenance                         changes. Our novel two-phase impact analysis computes the
                                                                      minimal set of nodes requiring updates:
Modern software repositories undergo continuous evolution,                Phase 1: Direct Impact Analysis. We first identify nodes
with developers committing changes multiple times daily.              directly corresponding to modified code entities. Let V denote
While time series forecasting techniques have shown promise           the set of all nodes in the current graph. The direct impact set
in predicting software evolution patterns [17], for a code gen-       is:
eration system to remain effective, its underlying knowledge                         Id = {v ∈ V : modified(code(v))}            (18)
graph must reflect these changes immediately—stale seman-
tic information leads to incorrect code generation. However,          where code(v) maps a graph node to its source code represen-
reconstructing the entire graph after each change is computa-         tation. Crucially, we employ semantic differencing on abstract
tionally prohibitive for large repositories, where full extraction    syntax trees (ASTs) rather than textual comparison, eliminat-
can take minutes for codebases with millions of lines.                ing false positives from superficial changes like whitespace or
   Existing approaches to this problem fall short in criti-           comments.
cal ways. IDE language servers (e.g., pylance [19]) use                  Phase 2: Transitive Impact Analysis. Code changes often
timestamp-based invalidation that often misses semantic de-           have ripple effects—modifying a function signature affects all
pendencies. Build systems like Bazel [8] track file-level de-         its callers. We compute the transitive closure of dependencies:
pendencies but lack the semantic granularity needed for code             It = Id ∪ {v ∈ V : ∃ path p from u ∈ Id to v in G}      (19)
generation. Database view maintenance algorithms [11] pro-
vide theoretical foundations but assume simpler data models              Our key optimization bounds this closure by dependency
than heterogeneous code graphs containing typed nodes, se-            type: type changes propagate transitively, but implementation
mantic edges, and constraint relationships.                           changes often have local impact. This selective propagation
   This section presents the first incremental maintenance al-        reduces |It | by 73% on average compared to naive transitive
gorithm with formal optimality guarantees for code knowledge          closure.

                                                                 13
                                   Journal of Emerging Applied Artificial Intelligence (JEAAI)


8.3     Novel Incremental Update Algorithm                             Table 4: Detailed incremental update performance on
                                                                       R EPO KG-50 repositories
Our incremental update algorithm operates in three carefully
orchestrated phases that maintain graph consistency while               Metric                 Change Size (files)      vs Baseline
minimizing computational overhead:                                                              1-5 5-20       20+      Full Naive
 1: Input: Current graph Gt , Code changes ∆R                           Latency (s)
 2: Output: Updated graph Gt+1                                          SemanticForge          0.18    0.52    1.73    -96%     -71%
 3:                                                                     Full Rebuild           12.4    12.7    13.8       —        —
 4: // Phase 1: Surgical Invalidation                                   Naive Incremental      1.89    6.78    28.9       —        —
 5: Compute impact sets Id , It using impact analysis                   Timestamp Cache        0.71    2.68    12.2       —        —
 6: Gpartial ← Gt \ {v, e : v ∈ It or e incident to It }
 7:                                                                     Memory (MB)
 8: // Phase 2: Focused Re-extraction                                   SemanticForge           58     126      178    -97%     -93%
 9: G∆ ← FE ({f ∈ ∆R : f contains v ∈ Id })                             Full Rebuild          2400    2400     2400       —        —
10:                                                                     Naive Incremental      420     980     1680       —        —
11: // Phase 3: Intelligent Reconciliation                              Speedup Factor
12: Gt+1 ← merge(Gpartial , G∆ ) with:                                  vs Full Rebuild         69x     24x      8x       —        —
13:   - Preserve existing node IDs for unchanged entities               vs Naive                11x     13x     17x       —        —
14:   - Resolve type conflicts using most specific type                 vs Timestamp           3.9x    5.2x    7.0x       —        —
15:   - Mark cross-file references for lazy resolution
16:
17: return Gt+1                                                        8.4.2   Quantitative Performance Results
   The key innovation is our lazy cross-reference resolution.
                                                                       Figure 5 presents comprehensive performance analysis across
Consider a scenario where function authenticate() is
                                                                       four dimensions. The results validate our theoretical com-
modified: traditional approaches would immediately update
                                                                       plexity bounds while demonstrating practical viability for real-
all 500+ call sites across the repository. Instead, we mark these
                                                                       world deployment.
references as ”pending” and resolve them only when the code
                                                                          Update Latency Analysis. As shown in Figure 5(a), our
generator actually queries those specific call sites. This defers
                                                                       algorithm achieves sub-second updates for typical commits
O(n) work to O(1) amortized cost, reducing update latency
                                                                       (5-20 files), completing in 0.18-0.52 seconds versus 12.4-12.7
by 84% in practice while maintaining correctness through our
                                                                       seconds for full reconstruction—a 96% reduction. The empir-
eventual consistency guarantee.
                                                                       ical scaling closely matches our theoretical O(|∆R| · d · log n)
                                                                       bound, with measured exponent 1.42 (R2 = 0.97).
                                                                          Component-Level Performance. Figure 5(b) reveals that
8.4     Empirical Validation                                           re-extraction dominates update cost (38% of total time), fol-
                                                                       lowed by graph invalidation (24%) and impact analysis (17%).
We conducted comprehensive performance evaluation of our               Critically, lazy resolution adds minimal overhead (3%), vali-
incremental maintenance algorithm on the 50 repositories in            dating our deferred computation strategy.
R EPO KG-50 and five popular open-source Python projects,                 Memory Efficiency. Our working set scales linearly with
comparing against full reconstruction and two baselines: naive         change size at approximately 8-12MB per modified file for
incremental updates (without lazy resolution) and timestamp-           typical commits (10-15 files), using only 126MB compared
based caching (common in IDE language servers).                        to 2.4GB for full reconstruction—a 95% reduction. This dra-
                                                                       matic memory efficiency enables concurrent maintenance of
                                                                       multiple repositories on standard developer hardware without
8.4.1   Experimental Setup and Methodology                             dedicated infrastructure.

Test Corpus.         We collected 5,000 real commits from
                                                                       8.4.3   Real-World Repository Case Studies
R EPO KG-50 repositories, categorized by change size: small
(1-5 files), typical (5-20 files), and large (20+ files). Addition-    To validate generalization beyond R EPO KG-50, we evaluated
ally, we analyzed 1,000 commits from Django, Scikit-learn,             our algorithm on five widely-used Python projects with diverse
Pandas, Flask, and Requests to validate generalization.                characteristics:
   Measurement Protocol. All timing measurements repre-                  The consistent 45-71x speedup across diverse repositories
sent wall-clock time averaged over 100 runs per commit size            confirms that our algorithm’s benefits generalize beyond the
category. We measure five phases: impact analysis, graph in-           evaluation benchmark. Notably, larger repositories (Django,
validation, re-extraction, reconciliation, and lazy resolution.        Pandas) show higher speedup factors due to our sub-linear
Memory usage is measured via psutil at 10ms intervals,                 scaling properties.
reporting peak working set size.                                         Long-term Accuracy. Crucially, ablation studies (Sec-


                                                                  14
                                                                        Journal of Emerging Applied Artificial Intelligence (JEAAI)


                                                                   Incremental Knowledge Graph Maintenance Performance on REPOKG-50
                                                                  (a) Incremental Update Performance                                                           (b) Component-wise Latency Breakdown
                                                                                                                                                    350
                                                      102         SemanticForge (Lazy)                                                                           5 files
                                                                  Full Reconstruction                                                                            20 files


                       Update Latency (seconds)
                                                                                                                                                    300
                                                                  Naive Incremental                                                                              50 files




                                                                                                                              Time (milliseconds)
                                                                                           90% reduction
                                                                  Timestamp Cache                                                                   250
                                                      101         Typical commits
                                                                                                                                                    200
                                                                                                                                                    150
                                                      100
                                                                                                                                                    100
                                                                                         0.52s
                                                                                                                                                     50
                                                  10 1
                                                                                                                                                      0
                                                            100                101                  102                                                       Impact      Graph Re-extractionReconciliation Lazy
                                                                           Number of Modified Files                                                           Analysis Invalidation                        Resolution
                                                                                                                                                                                Update Phase
                                                                        (c) Memory Usage Scaling                                                                (d) Real-world Repository Performance
                                                      104
                                                                  SemanticForge (Incremental, 10-15 files)                         Pandas                                                          Incremental
                                                                                                                                                                                                            71x
                                                                                                                                                                                                                Update
                                                                  Full Reconstruction                                              (380K)                                                          Full Reconstruction
                             Peak Memory Usage (MB)




                                                                  Naive Incremental (10-15 files)
                                                                                                                                          Flask                     47x
                                                      103                                                                                 (35K)
                                                                                                           98% reduction     Requests                             45x
                                                                                                                                (25K)
                                                      102                                                                  Scikit-learn                                                 57x
                                                                                                                                (240K)
                                                                                                                                   Django                                                                          66x
                                                                                                                                   (475K)
                                                      101
                                                            0        100        200        300        400           500                                   0          10          20           30          40             50
                                                                           Repository Size (KLOC)                                                                           Update Time (seconds)
             Experiments on REPOKG-50 benchmark. Measurements averaged over 100 commits per repository. Hardware: Intel Xeon Gold 6248R (3.0GHz), 64GB RAM. Typical commit: 10-15 modified files.


Figure 5: Incremental knowledge graph maintenance performance on R EPO KG-50. (a) Update latency scales with change size,
achieving 90% reduction versus full reconstruction for typical commits. (b) Component-wise breakdown reveals re-extraction
as the dominant cost. (c) Memory usage remains proportional to change size, enabling workstation deployment. (d) Real-world
repositories show consistent 66x average speedup.


Table 5: Performance on real-world repositories (10-15 file Table 6: Impact of algorithmic optimizations on update latency
commits)
                                                             Configuration                 Latency     vs Full     Impact
     Repository       Size Incr. Full Speedup                                                  (ms)    System
                  (KLOC)       (s)    (s)
                                                             Full System                        520         —           —
     Django           475 0.68 45.2              66x         w/o Lazy Resolution              2,847    +448%       Critical
     Scikit-learn     240 0.42 23.8              57x         w/o Selective Propagation        1,423    +174%          High
     Pandas           380 0.54 38.6              71x         w/o Semantic Diff                  892      +72% Medium
     Flask              35 0.15      7.1         47x         w/o Index Caching                  687      +32%         Low
     Requests           25 0.12      5.4         45x
                                                             Naive Implementation             6,780 +1204%              —
     Average            — 0.38 24.0              63x

                                                                  Selective Propagation. Our type-aware propagation strat-
tion 10.2) reveal that without continual maintenance, code egy reduces unnecessary graph traversals by 73%, contributing
generation accuracy degrades by 4.1% after 30 days and 12.7% 174% performance improvement over naive transitive closure.
after 100 commits. This degradation stems from outdated type
information and missed API changes, validating that real-time 8.4.5 Scalability Validation
maintenance is essential, not optional.
                                                                We stress-tested our algorithm on synthetic repositories up to
                                                                5M LOC to validate scalability claims:
8.4.4 Optimization Impact Analysis
                                                                  The sub-linear growth rates (1.19x-1.28x) for 50x reposi-
To understand the contribution of each algorithmic optimiza- tory size increase confirm our theoretical O(|∆R| · d · log n)
tion, we conducted controlled ablation experiments disabling complexity, with the logarithmic factor dominating at scale.
individual components:
   Lazy Resolution Impact. Disabling lazy cross-reference 8.5 Theoretical Guarantees
resolution increases latency by 448%, confirming it as our
most critical optimization. For a function with 100 call sites, Our maintenance algorithm provides two critical theoretical
lazy resolution defers 98% of updates until actually queried.   guarantees that distinguish it from heuristic approaches:


                                                                                                                           15
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


        Table 7: Scalability to large-scale repositories                This continual adaptation capability transforms S EMAN -
                                                                      TIC F ORGE from a static analysis tool into a living system
      Repo Size        Update Time (s)            Memory              that evolves with the codebase, ensuring sustained accuracy
       (KLOC)       Small Medium Large              (MB)              throughout the software development lifecycle.
             100     0.15        0.48     1.52             126
             500     0.19        0.58     1.94             245
           1,000     0.23        0.68     2.31             387        9    Experimental Setup
           5,000     0.34        0.92     3.47             892
                                                                  This section describes our comprehensive experimental
    Growth Rate     1.27x       1.19x    1.28x        1.87x       methodology designed to evaluate S EMANTIC F ORGE across
                                                                  multiple dimensions: functional correctness, hallucination re-
                                                                  duction, computational efficiency, and scalability. We estab-
   Theorem 8 (Semantic Equivalence). For any sequence lish rigorous evaluation protocols that address the unique chal-
of repository modifications ∆R1 , . . . , ∆Rt , the incrementally lenges of repository-level code generation assessment.
maintained graph Gtinc is semantically equivalent to the graph
Gtfull obtained by full reconstruction.
   Proof sketch: The key insight is that our semantic extraction 9.1 Dataset Construction
function FE exhibits the monotonicity property: the graph rep- We introduce R EPO KG-50, a curated benchmark specifically
resentation of code entity e depends only on e and its depen- designed for repository-level code generation evaluation. The
dencies, not on the extraction order. Since our algorithm up- dataset addresses critical limitations of existing benchmarks
dates exactly the impact set It containing all affected entities, that focus on isolated function synthesis rather than repository-
and lazy resolution ensures eventual consistency for cross- scale integration challenges.
references, the final graph state is identical regardless of up-
date path. □
   Theorem 9 (Complexity Bound). For a repository with n Repository Selection Criteria. We select 50 high-quality
entities, modifications affecting |∆R| entities, and maximum Python repositories from GitHub based on the following cri-
dependency depth d, our incremental algorithm has time com- teria: (1) Repository size between 10K-500K lines of code to
plexity O(|∆R| · d · log n) compared to O(n · log n) for full ensure meaningful complexity while maintaining experimen-
reconstruction.                                                   tal tractability; (2) Comprehensive test suites with ¿80% cov-
   Proof sketch: Impact analysis visits at most |∆R| · d nodes erage to enable reliable dynamic analysis; (3) Active devel-
via dependency traversal. Each node operation (removal, opment with ¿100 commits in the past year to ensure modern
insertion, lookup) costs O(log n) using our graph indices. coding practices; (4) Diverse domains including web frame-
Lazy resolution amortizes cross-reference updates across fu- works, data processing, machine learning, and system utilities;
ture queries. Since typical commits have |∆R| ≪ n and d is (5) Clear architectural patterns and documentation to facilitate
bounded by architectural depth, we achieve sub-linear scaling. ground truth validation.
□
                                                                  Task Generation Methodology. For each repository, we
                                                                  generate coding tasks through three complementary ap-
8.6 Discussion and Implications
                                                                  proaches:
The continual maintenance component represents a paradigm            Historical Analysis: We analyze commit histories to iden-
shift in how knowledge-based code generation systems han- tify real development tasks that required multi-file modifica-
dle repository evolution. Prior systems either ignore changes tions. We extract the commit message as the natural language
(leading to stale information) or require manual re-indexing. instruction and the diff as the ground truth implementation.
Our approach provides three key advantages:                       This yields 1,247 authentic tasks with natural complexity dis-
   Real-time Responsiveness. Sub-second update latency en- tribution.
ables integration with development workflows where code              Synthetic Task Generation: We develop an automated task
changes continuously. Developers see generated code that re- generator that creates instructions requiring specific types of
flects their latest modifications without manual intervention.    repository knowledge. Tasks include: API extension (adding
   Theoretical Soundness. Unlike heuristic caching strate- new endpoints with proper authentication), refactoring (ex-
gies, our semantic equivalence guarantee ensures that incre- tracting common functionality), bug fixing (correcting logic
mental updates never compromise correctness. This is critical errors while maintaining interface compatibility), and feature
for production systems where incorrect code generation has integration (adding functionality that spans multiple modules).
high costs.                                                       This produces 2,156 controlled tasks with known difficulty
   Practical Scalability. The sub-linear complexity bound characteristics.
makes our approach viable for industrial-scale repositories.         Developer-Authored Tasks: We engage 12 experienced de-
Google’s monorepo or Microsoft’s Windows codebase can be velopers to manually create challenging tasks that represent
maintained incrementally despite their massive size.              realistic development scenarios. Each developer contributes

                                                                 16
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


25-30 tasks per repository subset, resulting in 847 high-quality the full dataset release at approximately 15GB (compressed),
tasks with detailed solution explanations.                       including all graphs and annotations.

Ground Truth Construction. Each task includes: (1) Nat-             9.2   Evaluation Metrics
ural language instruction following template guidelines to en-
                                                                    We establish a multi-dimensional evaluation framework that
sure clarity and consistency; (2) Complete reference imple-
                                                                    captures both functional correctness and the specific halluci-
mentation verified through automated testing and manual re-
                                                                    nation phenomena targeted by our approach.
view; (3) Semantic annotations identifying required repository
knowledge (which functions must be understood, which con-
straints must be satisfied); (4) Difficulty ratings based on re-    Functional Correctness Metrics.
quired context size and constraint complexity; (5) Expected           • Pass@k: Fraction of tasks where at least one of the top-
hallucination types based on common failure patterns.                   k generated solutions passes all test cases. We report
                                                                        Pass@1, Pass@5, and Pass@10 to capture both precision
Dataset Statistics and Composition. R EPO KG-50 con-                    and recall characteristics.
tains 4,250 total tasks across 50 repositories representing 1.2M      • Test Pass Rate: Average percentage of test cases passed
lines of code. Tasks span multiple difficulty levels: 35% be-           across all generated solutions, providing a more nuanced
ginner (single-file modifications), 45% intermediate (multi-file        view of partial correctness.
with local dependencies), 20% advanced (complex architec-
tural changes). The dataset includes comprehensive metadata           • Compilation Success Rate: Percentage of generated so-
enabling fine-grained analysis of system performance across             lutions that compile without errors, indicating basic syn-
different task characteristics.                                         tactic correctness.
                                                                   • Integration Success Rate: Percentage of solutions that
Repository Licensing and Selection. All 50 repositories are          successfully integrate with the existing codebase without
selected from GitHub under permissive open-source licenses:          breaking existing functionality.
32 MIT-licensed, 12 Apache 2.0, 4 BSD-3-Clause, and 2 GPL-
3.0. We verify license compatibility for academic research use Hallucination-Specific Metrics.
and ensure no proprietary code is included. Repository selec-
tion prioritizes well-maintained projects with active commu-       • Logical Hallucination Rate (LHR): Percentage of gen-
nities (average 2,847 stars, 412 forks) to ensure code quality       erated solutions that compile but fail functional tests
and realistic development patterns. The full list of reposito-       due to incorrect program logic. Computed as: LHR =
                                                                     # compilable but failing solutions
ries with their licenses, domains, and statistics is provided in              # total solutions
supplementary material Table A1.                                   • Schematic Hallucination Rate (SHR): Percentage of
                                                                     solutions that violate type, signature, or architectural
Data Splits and Validation Protocol. We partition the                constraints. Measured through static analysis: SHR =
4,250 tasks into training (60%, 2,550 tasks), validation (20%,       # solutions with constraint violations
                                                                                # total solutions
850 tasks), and test (20%, 850 tasks) sets. The split is strati-
fied by repository and difficulty level to ensure balanced rep-    • Constraint Violation Frequency: Detailed breakdown
resentation. For cross-repository generalization experiments,        of specific constraint types violated (type mismatches,
we use leave-one-cluster-out validation where entire reposi-         signature errors, visibility violations, architectural incon-
tory clusters are held out. Training data is used exclusively        sistencies).
for query planner training via REINFORCE; the Code-Llama-          • Hallucination Severity: Classification of errors by re-
34B base model is used frozen without fine-tuning. Validation        quired effort to fix (trivial: 1-line fix, moderate: 2-10
data guides hyperparameter selection and early stopping. All         lines, severe: > 10 lines or architectural changes).
reported results are on the test set, which is never accessed
during development.                                              Context Selection Precision Metrics.
                                                                      • Context Precision: Percentage of retrieved context ele-
Public Availability and Reproducibility. We commit to re-
                                                                        ments that are actually used in the correct solution. Com-
leasing R EPO KG-50 publicly upon paper acceptance under a
                                                                        puted by comparing retrieved subgraph nodes against a
CC BY 4.0 license. The release includes: (1) all 4,250 task
                                                                        manually-annotated gold standard of required dependen-
descriptions and reference implementations, (2) pre-computed
                                                                        cies for each task.
static and dynamic knowledge graphs for all 50 repositories,
(3) evaluation scripts and metrics computation code, (4) de-          • Context Recall: Percentage of required dependencies
tailed repository metadata and statistics, and (5) baseline im-         that are successfully retrieved. Gold standard established
plementation code for fair comparison. Data and code will               through manual analysis of 500 randomly sampled tasks
be hosted at https://github.com/semanticforge/                          by three expert annotators (inter-rater agreement κ =
repokg50 with comprehensive documentation. We estimate                  0.81).


                                                               17
                                Journal of Emerging Applied Artificial Intelligence (JEAAI)


  • Context F1 Score: Harmonic mean of precision and re- Repository-Aware Systems.
    call for balanced evaluation of context selection quality.
                                                               • RepoCoder: We reimplement using GraphCodeBERT
                                                                 encoder with graph attention networks (3 layers, 8 heads)
Code Quality Metrics.
                                                                 for repository understanding. Generation uses the same
  • Maintainability Index: Composite metric based on cy-         Code-Llama-34B backbone for fair comparison. Graph
    clomatic complexity, lines of code, and Halstead metrics.    construction uses AST-based data flow analysis. Training
                                                                 uses cross-entropy loss for 20K steps.
  • Style Consistency: Adherence to repository-specific
    coding conventions measured through automated linters.     • CodePlan: Planning decomposition uses GPT-3.5 for
                                                                 task breakdown (max 5 subtasks), followed by Code-
  • API Usage Appropriateness: Correctness of library and        Llama-34B for implementation. We optimize decompo-
    framework usage patterns based on repository-specific        sition prompts and provide access to the same repository
    guidelines.                                                  metadata. Average 3-5 generation passes per task.

  • Documentation Quality: Presence and quality of gener-            • RAG-Code: Dense retrieval using CodeBERT embed-
    ated comments and docstrings.                                      dings with FAISS indexing. Cross-encoder reranking
                                                                       (top-50 → top-10). Context window: 6144 tokens. Gen-
Efficiency Metrics.                                                    eration uses Code-Llama-34B with identical settings to
                                                                       our decoder (excluding constraint checking).
  • Generation Latency: End-to-end time from instruction
    to generated code, broken down by pipeline stage.    Graph-Based Approaches.
  • Context Retrieval Time: Time required for query plan-            • GraphCodeBERT: 125M parameter model with data
    ning and subgraph extraction.                                      flow graph pre-training. Fine-tuned on our training data
                                                                       for 15 epochs. Uses graph-guided attention but no persis-
  • Constraint Solving Overhead: Additional time intro-
                                                                       tent graph storage.
    duced by SMT-based constraint checking.
                                                                     • UniXcoder: 125M parameter multi-modal model encod-
  • Memory Usage: Peak memory consumption during gen-
                                                                       ing code, AST, and comments. Fine-tuned with con-
    eration, including knowledge graph storage.
                                                                       trastive learning on code-documentation pairs from our
                                                                       repositories.
9.3   Baseline Systems
                                                                     • CodeT5+: 220M parameter encoder-decoder with struc-
We compare S EMANTIC F ORGE against state-of-the-art                   tural understanding. Fine-tuned on our dataset using
repository-level code generation systems and relevant                  teacher forcing for 20 epochs. Uses beam search (k=5)
baselines across different paradigms.                                  without constraint checking.

Neural Baselines.                                                 Baseline Fairness and Comparison Methodology. To en-
                                                                  sure rigorous comparison, we implement extensive baseline
  • Code-Llama-34B: Base language model with BM25-                optimization and standardization protocols:
    based retrieval for repository context. We retrieve top-         Computational Budget Equalization: All systems receive
    10 most similar functions/classes using TF-IDF scoring,       identical computational budgets. For Code-Llama baselines,
    providing up to 4096 tokens of context. Generation uses       we allocate the same 2.5s average time budget as S EMANTIC -
    greedy decoding (temperature=0.2, top-p=0.95). Runs on        F ORGE by optimizing retrieval speed. For planning-based sys-
    same A100 GPU with identical batch size for fair com-         tems, we cap iterations at 5 to maintain practical latency (¡10s).
    parison.                                                      GPU memory is standardized at 40GB for all neural systems.
  • StarCoder-15B: Code-specialized model with Code-              We measure wall-clock time including all preprocessing but
    BERT embeddings for dense retrieval. Top-15 retrieved         excluding one-time setup (model loading, graph construction).
    snippets with cross-encoder reranking. Uses nucleus              Context Provision Parity: Critical for fair comparison, all
    sampling (p=0.95) with temperature=0.8. Requires 15GB         systems receive access to repository information:
    GPU memory.                                                      • RAG baselines: Full repository code indexed with both
  • GPT-4-Code: Accessed via API with repository context               BM25 and dense embeddings
    provided through carefully engineered prompts (up to             • Planning systems: Access to file structure, import graphs,
    8192 tokens). We implement few-shot prompting (3 ex-               and function signatures
    amples) and iterative refinement disabled to match single-
    pass comparison. API calls use temperature=0.1 for con-          • Graph-based models: AST and data flow information ex-
    sistency.                                                          tracted via same tools

                                                             18
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


Context window limits match natural capacities: 4096 tokens        Training Configuration. Query planner training uses RE-
for Code-Llama, 8192 for GPT-4, 2048 for smaller models.           INFORCE with Adam optimizer (learning rate α = 5 × 10−5
   Hyperparameter Optimization: All baselines undergo              for policy, β = 1×10−4 for baseline critic), batch size 32, and
systematic hyperparameter tuning on a held-out validation set      exponential reward discounting (γ = 0.95). The baseline is a
(10% of data, stratified by repository). We perform grid search    2-layer MLP with 512 hidden units trained jointly via MSE
over key parameters: retrieval k (5-20), generation temperature    loss. We employ advantage normalization, gradient clipping
(0.1-1.0), beam width (1-10), and model-specific settings. We      ([−1, 1]), and entropy regularization (λ = 0.01) for variance
report best configuration found within 50 trials per system.       reduction. Synthetic data warm-start involves 10,000 gener-
   Implementation Rigor: We reimplement baselines from             ated instruction-query pairs per repository. Training converges
published descriptions when code is unavailable, validated         within 10K steps on typical repositories.
against reported metrics where possible:
                                                               Hardware and Infrastructure. All experiments run on
   • RepoCoder:      Our implementation achieves 38.9%
                                                               identical hardware: NVIDIA A100 GPUs (40GB) for neu-
     Pass@1 vs. 37.2% reported in the original paper
                                                               ral components, 8-core Intel Xeon Gold 6248R processors
   • CodePlan: Our optimization yields 42.3% vs. 39.1% in (3.0GHz) with 64GB DDR4 RAM for graph operations.
     original publication                                      Knowledge graph extraction processes repositories in 5-15
                                                               seconds. Query response times remain < 10ms for reposi-
   • RAG-Code: 40.1% in our setup vs. 38.7% reported           tories up to 500K LOC through optimized Neo4j indexing.
This demonstrates our implementations match or exceed pub-
lished performance, ensuring fair comparison.                  Constraint Solver Configuration. We use Z3 version
   Statistical Protocol for Comparison: All pairwise com- 4.12.2 with incremental solving enabled. Constraint encod-
parisons use paired t-tests (same tasks for all systems) with ing uses: first-order logic for type relationships, uninterpreted
Bonferroni correction for 9 comparisons (α = 0.05/9 ≈ functions for API contracts, and custom theories for architec-
0.0056). We report both p-values and effect sizes (Cohen’s tural patterns. Solver timeout is 100ms per beam step. In-
d). Confidence intervals are computed via stratified bootstrap cremental state caching and batch verification reduce average
(1000 resamples, preserving repository distribution).          checking time to 1.4ms per token.

Ablation Variants.    To isolate the contribution of each sys- Timing Measurement Protocol. All latency measurements
tem component:                                                 represent wall-clock time averaged over 100 runs per task, ex-
                                                               cluding compilation and environment setup. We measure five
  • S EMANTIC F ORGE-Static: Using only static analysis granular stages: (1) instruction encoding (0.12s), (2) graph
    without dynamic traces, but maintaining all other opti- query generation and execution (0.31s), (3) context prepara-
    mizations.                                                 tion (0.19s), (4) code generation with LM (1.70s), and (5)
  • S EMANTIC F ORGE-NoCons: Removing constraint en- SMT constraint checking (0.23s). Total average: 2.55s, re-
    forcement from the decoder while preserving knowledge ported as 2.5s. We exclude outliers beyond 2 standard devia-
    graph infrastructure.                                      tions (3.2% of samples). Statistical variance is reported using
                                                               95% bootstrap confidence intervals over 1000 resamples.
  • S EMANTIC F ORGE-NoPlanner: Using BM25-based re-
    trieval optimized with repository-specific term weighting Memory Profiling Methodology. Peak memory consump-
    instead of neural query planning.                          tion is measured using NVIDIA nvidia-smi for GPU mem-
  • S EMANTIC F ORGE-NoMaint: Without continual main- ory and psutil for system RAM, sampled at 100ms intervals
    tenance, using stale graphs from repository snapshots 30 throughout generation. We report maximum observed val-
    days prior.                                                ues across all tasks. Memory measurements include: model
                                                               weights (11.2GB), knowledge graph cache (1.8GB), interme-
  • S EMANTIC F ORGE-Oracle: Upper bound experiment diate activations (0.7GB), and SMT solver state (0.5GB).
    using manually curated context to isolate generation vs.
    planning contributions.                                    Reproducibility and Variance Control. To ensure repro-
                                                               ducible results, we control multiple sources of variance:
9.4   Implementation Details                                         • Random seeds: Fixed seeds for all stochastic compo-
Model Configuration. We instantiate S EMANTIC F ORGE                   nents (42 for model initialization, 123 for data splitting,
with Flan-T5-Large (770M parameters) for query planning                456 for sampling)
and Code-Llama-34B for code generation. The planner uses             • System state: All experiments run on dedicated nodes
512-dimensional hidden states with 8 attention heads. The de-          with no competing processes
coder employs beam search with width k=5 and incorporates
our SMT-based constraint checking at each step. Both models          • Software versions: PyTorch 2.0.1, CUDA 11.8, Python
use bfloat16 precision for efficiency.                                 3.10.6, Z3 4.12.2, Neo4j 5.9.0


                                                              19
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


   • Deterministic operations: CUDA deterministic mode Repository Clustering and Stratification. We cluster our
     enabled, cuDNN benchmarking disabled                       50 repositories into 5 groups based on architectural character-
                                                                istics: (1) Web frameworks with MVC patterns, (2) Data pro-
   • Multiple runs: Each configuration tested 3 times with cessing pipelines with functional patterns, (3) Object-oriented
     different initialization; we report mean across runs with libraries with inheritance hierarchies, (4) Scientific computing
     standard error < 2% for all metrics                        with numerical patterns, and (5) System utilities with proce-
                                                                dural patterns. This clustering enables analysis of how archi-
   These controls enable other researchers to reproduce our re- tectural diversity affects system performance.
sults within 5% variance, validated through independent re-
production by two co-authors on separate infrastructure.        Cross-Repository Training and Testing. We implement
                                                                a leave-one-cluster-out evaluation protocol where the query
                                                                planner is trained on repositories from 4 clusters and tested
9.5 Human Evaluation Protocol                                   on the held-out cluster. This evaluates whether semantic pat-
                                                                terns learned from one architectural style generalize to differ-
To complement automated metrics, we conduct comprehen-
                                                                ent coding paradigms. We repeat this process for all 5 clusters
sive human evaluation focusing on aspects difficult to capture
                                                                to obtain robust generalization estimates.
through automated assessment.

                                                                    Knowledge Transfer Analysis. We measure how effec-
Evaluator Selection and Training. We recruit 18 profes-             tively knowledge graphs from source repositories can boot-
sional software developers with 3+ years of experience in           strap performance on target repositories with different charac-
Python development. Evaluators undergo training on our as-          teristics. This includes: (1) semantic pattern overlap analysis
sessment criteria and complete practice evaluations to ensure       using graph isomorphism metrics, (2) constraint transferability
consistency. Inter-rater agreement is measured using Fleiss’        assessment across different architectural styles, and (3) adap-
kappa, achieving κ = 0.73 indicating substantial agreement.         tation time measurement for new repository integration.

                                                               Domain Adaptation Protocols. For each target repository,
Evaluation Dimensions.
                                                               we evaluate: (1) zero-shot performance using knowledge
                                                               graphs from other domains, (2) few-shot adaptation with 10-50
  • Code Quality: Overall assessment of generated code
                                                               target domain examples, and (3) full adaptation with complete
    quality on a 5-point Likert scale considering readability,
                                                               target repository analysis. This protocol reveals the minimum
    maintainability, and adherence to best practices.
                                                               adaptation requirements for practical deployment.
  • Integration Appropriateness: How well the generated
    code fits with existing repository architecture and con- 9.7 Theoretical Validation Experiments
    ventions.                                                To validate the theoretical claims in our paper, we conduct spe-
                                                             cific experiments targeting each theorem:
  • Error Analysis: Detailed categorization of errors with
    difficulty estimates for manual correction.              Theorem 3 Validation (Incremental Update Equivalence).
                                                             We verify semantic equivalence between incremental updates
  • Preference Ranking: Comparative evaluation where and full reconstruction by comparing knowledge graphs built
    evaluators rank solutions from different systems for the both ways on 100 repository snapshots with varying change
    same task.                                               sizes (10-500 modified files). Graph isomorphism testing con-
                                                             firms identical structure in 100% of cases, validating the se-
Evaluation Procedure. Each evaluator assesses solutions mantic equivalence claim.
for 25 randomly sampled tasks across different difficulty lev-
els. Solutions are presented in randomized order with system        Theorem 4 Validation (Convergence with Coverage). We
identities masked. Evaluators have access to the full repository    measure knowledge graph accuracy as test coverage increases
context and task description. The evaluation interface provides     from 20% to 90% across 10 representative repositories. Re-
guided prompts to ensure comprehensive assessment.                  sults show monotonic improvement in graph completeness
                                                                    (measured by edge recall against manually-annotated ground
                                                                    truth), with 95% accuracy at 80% coverage, supporting the
9.6   Cross-Repository Generalization Analysis                      convergence claim.

To assess the generalizability of S EMANTIC F ORGE across di-
                                                               9.8 Statistical Analysis
verse codebases, we conduct comprehensive cross-repository
evaluation that goes beyond standard within-repository valida- We employ rigorous statistical methods to ensure the reliabil-
tion.                                                          ity and significance of our experimental results across both

                                                               20
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


within-repository and cross-repository settings.                     S EMANTIC F ORGE achieves substantial improvements
                                                                   across all metrics: 7.5% absolute improvement in Pass@1
Significance Testing. We use paired t-tests for comparing          over the strongest baseline (CodePlan), 49.8% reduction in
system performance on the same task set, with Bonferroni cor-      schematic hallucination rate compared to GPT-4-Code, and
rection for multiple comparisons. Effect sizes are reported us-    34.7% reduction in logical hallucination rate. These im-
ing Cohen’s d to assess practical significance. Bootstrap confi-   provements demonstrate the effectiveness of our knowledge
dence intervals (95%) provide robust uncertainty estimates for     graph-guided approach for repository-level code generation.
all reported metrics. For cross-repository analysis, we employ
mixed-effects models to account for repository-level cluster- Baseline Comparison Details. To contextualize these re-
ing.                                                             sults, we note the specific baseline configurations that pro-
                                                                 duced the reported numbers. Code-Llama-34B with BM25
                                                                 retrieval (top-10 functions, 4096 token context) represents a
Cross-Validation Protocols. We employ three complemen-
                                                                 strong RAG baseline; our 15.6% improvement over it vali-
tary validation strategies: (1) 5-fold cross-validation at the
                                                                 dates the value of semantic graphs versus keyword matching.
repository level to ensure results generalize across different
                                                                 CodePlan’s 42.3% result comes from optimized 3-5 iteration
codebases within the same architectural family, (2) leave-one-
                                                                 planning with GPT-3.5 decomposition; our single-pass 49.8%
cluster-out validation to assess cross-architectural generaliza-
                                                                 demonstrates that constraint-aware generation eliminates the
tion, and (3) temporal validation using repository snapshots
                                                                 need for iterative refinement. GPT-4-Code’s 41.7% with 8192-
from different time periods to evaluate robustness to codebase
                                                                 token context and few-shot prompting shows that even larger
evolution.
                                                                 context windows cannot substitute for explicit semantic struc-
                                                                 ture. These comparisons isolate S EMANTIC F ORGE’s algorith-
Generalization Metrics. We introduce several metrics to mic contributions from implementation advantages.
quantify cross-repository generalization: (1) Architectural
Transfer Coefficient measuring performance retention across Statistical Significance and Comparison Methodology.
different design patterns, (2) Semantic Overlap Index quan- All performance improvements are statistically significant
tifying knowledge graph similarity between repositories, and (p < 0.001) using paired t-tests with Bonferroni correction
(3) Adaptation Efficiency measuring the rate of performance for 9 pairwise comparisons (α = 0.0056). We employ paired
improvement during domain adaptation.                            tests because all systems evaluate on identical task instances,
                                                                   increasing statistical power. Effect sizes (Cohen’s d) range
Fairness Considerations. We analyze system performance             from 0.82 to 1.47, indicating large practical significance be-
across different repository characteristics (size, domain, com-    yond mere statistical significance. Bootstrap confidence inter-
plexity, programming paradigm) to identify potential biases.       vals (95%, 1000 resamples with stratification by repository)
Statistical parity metrics ensure that performance differences     confirm robustness across different repository samples.
are not systematically related to repository metadata rather          We validate that performance differences are not artifacts
than actual task difficulty. We also assess whether certain ar-    of our specific infrastructure by running a subset of exper-
chitectural patterns or coding styles receive disproportionate     iments (500 tasks) on alternative hardware (NVIDIA V100,
benefit from our approach.                                         AMD EPYC processors). Results show < 3% variance in
   This comprehensive experimental framework enables thor-         relative performance rankings, confirming that S EMANTIC -
ough evaluation of S EMANTIC F ORGE while establishing re-         F ORGE’s advantages generalize across hardware platforms.
producible benchmarks for future research in repository-level
code generation.                                                   10.2    Component Ablation Analysis
                                                                   We conduct a systematic component ablation study to isolate
10     Results and Analysis                                        the contribution of each S EMANTIC F ORGE component and
                                                                   validate our architectural design decisions. This analysis is
This section presents comprehensive experimental re-               crucial for understanding which innovations provide the most
sults demonstrating S EMANTIC F ORGE’s effectiveness in            significant benefits and guides future development priorities.
repository-level code generation. Our evaluation reveals           As shown in Figure 6, each component contributes meaning-
significant improvements in functional correctness, dramatic       fully to overall system performance with minimal computa-
reductions in both logical and schematic hallucination, and        tional overhead. The dramatic impact of constraint enforce-
practical scalability for real-world deployment.                   ment on schematic hallucination rates and the dual analysis
                                                                   benefits for logical hallucination demonstrate the effectiveness
                                                                   of our integrated approach.
10.1    Overall Performance Results
Table 8 summarizes the performance of S EMANTIC F ORGE Dual Static-Dynamic Analysis Impact. The comparison
compared to state-of-the-art baselines across our core metrics between S EMANTIC F ORGE and S EMANTIC F ORGE-Static re-
on the R EPO KG-50 benchmark.                                  veals that dynamic trace augmentation provides substantial

                                                              21
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


Table 8: Overall performance comparison on R EPO KG-50. Best results in bold, second-best underlined. Statistical significance
(p < 0.05) marked with *.

                                   Functional Correctness              Hallucination Rates               Efficiency
        System
                                Pass@1 Pass@5 Pass@10                  LHR ↓       SHR ↓         Latency (s) Memory (GB)
        Code-Llama-34B           34.2%       52.8%       61.4%          42.1%       38.7%           2.3             12.4
        StarCoder-15B            29.8%       48.2%       55.9%          45.3%       41.2%           1.8              8.2
        GPT-4-Code               41.7%       63.2%       71.8%          35.4%       29.3%           4.1               -
        RepoCoder                38.9%       58.4%       67.1%          38.7%       32.1%           3.2             15.8
        CodePlan                 42.3%       61.9%       70.4%          33.8%       31.5%           5.7             18.3
        RAG-Code                 40.1%       59.7%       68.3%          36.2%       30.8%           2.9             14.1
        GraphCodeBERT            35.7%       54.3%       63.2%          40.3%       35.9%           2.1             11.7
        UniXcoder                37.4%       56.8%       65.5%          38.9%       33.4%           2.4             13.2
        CodeT5+                  39.2%       58.1%       66.7%          37.1%       32.7%           2.6             14.5
        S EMANTIC F ORGE        49.8%*      71.4%*      79.3%*         23.1%*       14.7%*          2.4             13.9

Table 9: Detailed component ablation results with statistical significance testing. All differences vs. full S EMANTIC F ORGE are
statistically significant (p < 0.001).

 Configuration                           Pass@1             Pass@5                Pass@10                 LHR               SHR
 S EMANTIC F ORGE (Full)                 49.8%               71.4%                 79.3%               23.1%               14.7%
 S EMANTIC F ORGE-Static             42.5% (-7.3%)       64.1% (-7.3%)          71.8% (-7.5%)     35.5% (+12.4%)       16.2% (+1.5%)
 S EMANTIC F ORGE-NoCons             40.9% (-8.9%)       62.3% (-9.1%)          70.1% (-9.2%)     25.8% (+2.7%)       31.2% (+16.5%)
 S EMANTIC F ORGE-NoPlanner          43.6% (-6.2%)       65.7% (-5.7%)          73.9% (-5.4%)     28.4% (+5.3%)        18.9% (+4.2%)
 S EMANTIC F ORGE-NoMaint            45.7% (-4.1%)       67.8% (-3.6%)          75.6% (-3.7%)     24.7% (+1.6%)        16.1% (+1.4%)
 Static + NoCons                    35.2% (-14.6%)      56.8% (-14.6%)          64.3% (-15.0%)    38.9% (+15.8%)      34.7% (+20.0%)
 Base Code-Llama                    34.2% (-15.6%)      52.8% (-18.6%)          61.4% (-17.9%)    42.1% (+19.0%)      38.7% (+24.0%)


benefits: 7.3% improvement in Pass@1 and 12.4% reduction              guided decoder eliminates 89% of these errors while adding
in logical hallucination rate. This validates our hypothesis that     only 0.2s average latency (8.3% overhead). This cost-benefit
runtime information captures semantic relationships invisible         analysis strongly justifies the architectural complexity of con-
to static analysis alone. The effect is particularly pronounced       straint integration.
for repositories with polymorphic code patterns where static
analysis cannot resolve call targets.
                                                                 Neural Query Planning Contribution. Replacing learned
   Deep Analysis: Dynamic traces provide the most benefit
                                                                 query planning with traditional BM25-based retrieval
for data processing repositories (9.2% improvement) where
                                                                 (S EMANTIC F ORGE-NoPlanner) reduces Pass@1 by 6.2% and
method dispatch is often data-dependent, and least benefit for
                                                                 increases both hallucination types. Statistical analysis reveals
system utilities (4.1% improvement) where control flow is typ-
                                                                 that the neural planner achieves 73% precision in selecting
ically explicit. This pattern supports our theoretical framework
                                                                 relevant context compared to 51% for keyword-based retrieval
that dynamic analysis helps most when static analysis is fun-
                                                                 (p < 0.001, χ2 test).
damentally limited.
                                                                    Context Quality Analysis: The neural planner identifies
                                                                 2.3× more transitive dependencies and 1.8× more architec-
Constraint Enforcement Critical Value. Removing SMT-
                                                                 tural constraints per query compared to traditional retrieval.
guided constraint checking (S EMANTIC F ORGE-NoCons)
                                                                 This improved context quality directly translates to better gen-
causes the most dramatic performance degradation: 8.9%
                                                                 eration outcomes, particularly for tasks requiring understand-
reduction in Pass@1 and a catastrophic 16.5% increase in
                                                                 ing of cross-module relationships.
schematic hallucination rate. This represents a 112% relative
increase in constraint violations, demonstrating that constraint
enforcement is not merely helpful but essential for reliable Continual Maintenance System Impact. Testing with stale
code generation.                                                 knowledge graphs (S EMANTIC F ORGE-NoMaint) on reposito-
  Error Analysis: Without constraint enforcement, 47% of ries modified within the past 30 days shows 4.1% degradation
generated solutions contain type mismatches, 23% have sig- in Pass@1. While seemingly modest, this effect compounds
nature violations, and 18% have visibility errors. The SMT- over time: repositories with > 100 commits since graph con-


                                                                 22
                                                                      Journal of Emerging Applied Artificial Intelligence (JEAAI)


                                      (a) Pass@1 Performance Across Configurations                                                                 (b) Schematic Hallucination Rates by Component
                                 60       Constraint enforcement                                                                            45
                                                                                                                                                                                                                       *
                                                                                                                                                                                                                     38.7%




                                                                                                         Schematic Hallucination Rate (%)
                                               most critical
                                      49.8%                                                                                                 40
                                 50                                           *
                                                                            45.7%                                                                                                        increase      *
                                                                                                                                                                                       112% relative 34.7%
                                                *
                                              42.5%      *           *
                                                                   43.6%                                                                    35                            *
                                                                                                                                                                        31.2%
                                                       40.9%
                                 40                                                     *
                                                                                      35.2%      *
                                                                                               34.2%                                        30
Pass@1 (%)




                                                                                                                                            25
                                 30                                                                                                                                                  *
                                                                                                                                                                                   18.9%
                                                                                                                                            20
                                                                                                                                                    14.7%        *
                                                                                                                                                               16.2%                             *
                                                                                                                                                                                               16.1%
                                 20                                                                                                         15
                                                                                                                                            10
                                 10
                                                                                                                                            5
                                 0                                                                                                          0
                           (Fuorge




                                                                                                                                      (Fuorge
                                    c

                                                      ns


                                                                 er


                                                                           int


                                                                                               s




                                                                                                                                                                                             int


                                                                                                                                                                                                          s
                                                                                           am e




                                                                                                                                               c

                                                                                                                                                                       ns


                                                                                                                                                                                  er




                                                                                                                                                                                                                    am e
                                                                                    on




                                                                                                                                                                                                          on
                                 ati




                                                                                                                                            ati
                                                                                        -Ll as




                                                                                                                                                                                                                 -Ll as
                                                               nn




                                                                                                                                                                                nn
                                ll)




                                                                                                                                           ll)
                                                                                             a




                                                                                                                                                                                                                      a
                                                      Co




                                                                                                                                                                       Co
                                                                        Ma




                                                                                                                                                                                            Ma
                                                                                      de B




                                                                                                                                                                                                               de B
                                                                                  oC




                                                                                                                                                                                                        oC
                             -St




                                                                                                                                        -St
                             cF




                                                                                                                                        cF
                                                             Pla




                                                                                                                                                                             Pla
                                                 -No




                                                                                                                                                                  -No
                                                                      -No




                                                                                                                                                                                       -No
                                                                                 +N




                                                                                                                                                                                                    +N
                         SF




                                                                                                                                    SF
                         nti




                                                                                                                                    nti
                                                           -No




                                                                                                                                                                            -No
                                                SF




                                                                                                                                                                 SF
                                                                     SF




                                                                                                                                                                                      SF
           ma




                                                                                                                     ma
                                                                             tic




                                                                                                                                                                                                 tic
                                                       SF




                                                                                                                                                                        SF
                                                                                         Co




                                                                                                                                                                                                               Co
                                      (c) Logical Hallucination Rates by Component                                                                            (d) Generation Latency Breakdown
                                                                            Sta




                                                                                                                                                                                              Sta
Se




                                                                                                         Se
                                 50                                                                                                   3.0
                                                                                                 *
                                                                                               42.1%                                                 2.5s
Logical Hallucination Rate (%)




                                                                                                                                                                                                 2.4s
                                                                                        *
                                                                                      38.9%                                           2.5                               2.3s         2.2s
                                 40             *
                                              35.5%

                                                                                                        Latency (seconds)
                                                                                                                                                               1.8s                                        1.7s       1.7s
                                                                     *
                                                                   28.4%                                                              2.0
                                 30                      *
                                                       25.8%                  *
                                                                            24.7%
                                      23.1%                                                                                           1.5
                                 20
                                                                                                                                      1.0

                                 10
                                                                                                                                      0.5

                                 0                                                                                                    0.0
                           (Fuorge




                                                                                                                                      (Fuorge
                                     c

                                                      ns


                                                                 r


                                                                            t

                                                                                    ns

                                                                                              am e




                                                                                                                                                c

                                                                                                                                                                       ns


                                                                                                                                                                                  r


                                                                                                                                                                                              t

                                                                                                                                                                                                         ns

                                                                                                                                                                                                                    am e
                                                                           in




                                                                                                                                                                                               in
                                                                 ne




                                                                                                                                                                                  ne
                                 ati




                                                                                                                                            ati
                                                                                           -Ll as




                                                                                                                                                                                                                 -Ll as
                                ll)




                                                                                                                                           ll)
                                                                                                a




                                                                                                                                                                                                                      a
                                                      Co




                                                                                     o




                                                                                                                                                                       Co




                                                                                                                                                                                                           o
                                                                        Ma




                                                                                                                                                                                            Ma
                                                                 n




                                                                                                                                                                                 n
                                                                                         de B




                                                                                                                                                                                                               de B
                                                                                  oC




                                                                                                                                                                                                        oC
                             -St




                                                                                                                                        -St
                             cF




                                                                                                                                        cF
                                                             Pla




                                                                                                                                                                             Pla
                                                 -No




                                                                                                                                                                  -No
                                                                      -No




                                                                                                                                                                                       -No
                                                                                 +N




                                                                                                                                                                                                    +N
                         SF




                                                                                                                                    SF
                         nti




                                                                                                                                    nti
                                                           -No




                                                                                                                                                                            -No
                                                SF




                                                                                                                                                                 SF
                                                                     SF




                                                                                                                                                                                      SF
           ma




                                                                                                                     ma
                                                                             tic




                                                                                                                                                                                                 tic
                                                       SF




                                                                                                                                                                        SF
                                                                                         Co




                                                                                                                                                                                                               Co
                                                                            Sta




                                                                                                                                                                                              Sta
Se




                                                                                                         Se




                                                           SemanticForge (Full)           Component Ablations                                          Baseline Systems                p<0.001

     Figure 6: Component ablation results for S EMANTIC F ORGE. (a) Pass@1 performance across seven configurations with 95%
     confidence intervals. (b) Schematic hallucination rates (SHR) by configuration. (c) Logical hallucination rates (LHR) by
     configuration. (d) Generation latency in seconds. Configurations include the full system, four single-component ablations
     (SF-Static, SF-NoCons, SF-NoPlanner, SF-NoMaint), one combined ablation (Static+NoCons), and baseline Code-Llama.
     Statistical significance markers (∗) indicate p < 0.001 compared to the full system.


     struction show 12.7% degradation, highlighting the critical im-                                                                             error rate
     portance of continual adaptation.
                                                                                                                                       • Neural planning: +0.3s query time → +6.2% Pass@1
     Component Interaction Effects. The combined component            • Maintenance system: +0.1s incremental updates → sus-
     ablation (S EMANTIC F ORGE without both static-dynamic dual         tained performance
     analysis and constraint enforcement) shows super-additive
     degradation (14.6% vs. 7.3% + 8.9% = 16.2%), indicating pos-
     itive interaction between components. Dynamic traces inform Key Findings Summary. Our component ablation analy-
     constraint extraction, while constraint enforcement validates sis reveals critical insights: (1) Dynamic analysis contributes
     the semantic relationships captured in dynamic analysis.      +7.3% Pass@1 improvement by capturing runtime seman-
                                                                   tics invisible to static analysis, (2) Constraint enforcement re-
                                                                   duces error rates by 16.5% absolute (112% relative reduction
     Computational Cost-Benefit Analysis. Each component’s in schematic hallucinations), (3) Neural planning adds +6.2%
     computational overhead is justified by performance gains:     Pass@1 through improved context selection, and (4) Each
         • Dynamic analysis: +0.8s construction time → +7.3% component demonstrates statistical significance (p < 0.001)
           Pass@1                                                  with large effect sizes. This component ablation analysis con-
                                                                   clusively demonstrates that each S EMANTIC F ORGE compo-
         • Constraint enforcement: +0.2s generation time → -16.5% nent provides substantial, statistically significant benefits that


                                                                                                       23
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


Table 10: Detailed hallucination breakdown by category. Val-                                   Scalability Analysis Across Repository Sizes
ues show error rates with reduction percentages vs. GPT-4 in
parentheses.                                                                               (a) Generation Quality                                         (b) Query Performance
                                                                                     54                                                         0.5
                                                                                                                                                              Actual




                                                                                                                           Query Latency (s)
                                                                                     52                                                         0.4           O(n^0.73) fit
    Error Category          GPT-4     S EMANTIC F ORGE




                                                                 Pass@1 (%)
                                                                                     50                                                         0.3
                   Schematic Hallucination
                                                                                                                                                0.2
    Type Mismatches        15.2%       6.8% (↓55.3%)                                 48
    Signature Violations    8.7%       3.2% (↓63.2%)                                                                                            0.1
                                                                                     46
    Visibility Errors       3.4%       1.1% (↓67.6%)                                                                                            0.0 10K50K100K 200K
                                                                                          10K50K100K 200K    350K   500K                                                       350K   500K
    Import Issues           2.0%       0.3% (↓85.0%)                                         Repository Size (LOC)                                         Repository Size (LOC)
                                                                                          (c) Memory Consumption                                           (d) KG Construction
                  Logical Hallucination                                              17




                                                                                                                             Construction Time (s)
                                                                                                Actual                                               50       Actual




                                                                 Memory Usage (GB)
    Control Flow Errors 12.8%        8.4% (↓34.4%)                                   16         Linear fit                                                    O(n log n) fit
                                                                                                                                                     40
    Data Flow Errors      14.1%      9.7% (↓31.2%)                                   15
    API Misuse             6.3%      3.1% (↓50.8%)                                   14                                                              30
    State Management       2.2%      1.9% (↓13.6%)                                   13                                                              20
                                                                                     12                                                              10
                                                                                     11 10K50K100K 200K      350K   500K                             0 10K50K100K 200K         350K   500K
justify the architectural complexity. The results validate our                               Repository Size (LOC)
                                                                                                        Repository Size (LOC)
design decisions and provide clear guidance for practition-
ers considering which components to implement in resource- Figure 7: Scalability analysis showing system performance
constrained environments.                                       across repository sizes. (a) Generation quality (Pass@1) re-
                                                                mains stable across scales. (b) Query latency grows sub-
                                                                linearly with repository size. (c) Memory usage scales ap-
10.3 Hallucination Analysis                                     proximately linearly. (d) Knowledge graph construction time
                                                                shows expected O(n log n) complexity.
We provide detailed analysis of the hallucination phenomena
that S EMANTIC F ORGE addresses, demonstrating significant
improvements in code reliability.
                                                                Computational Efficiency. Query latency grows sub-
                                                                linearly with repository size (R2 = 0.89 for O(n0.73 ) fit), con-
Schematic Hallucination Elimination. Our constraint- firming the effectiveness of our indexing and caching strate-
based decoder achieves remarkable reductions in schematic gies. Memory usage scales approximately linearly (R2 =
errors: 85% reduction in import issues, 67.6% reduction in 0.94), remaining practical even for large repositories.
visibility errors, and 63.2% reduction in signature violations.
These improvements directly translate to higher compilation
success rates and reduced developer debugging effort.           Graph Construction Overhead. Initial knowledge graph
                                                                construction shows expected O(n log n) complexity, taking 5-
                                                                47 seconds for repositories in our size range. Incremental up-
Logical Hallucination Mitigation. While more challenging dates maintain sub-second response times, enabling real-time
to eliminate completely, our dual static-dynamic knowledge development workflows.
graph reduces logical errors significantly: 50.8% reduction in
API misuse and 34.4% reduction in control flow errors. The
dynamic traces provide crucial runtime semantics that help 10.5 Cross-Repository Generalization Results
models understand correct usage patterns.
                                                                Our cross-repository evaluation reveals strong generalization
                                                                capabilities while identifying important adaptation require-
10.4 Scalability Analysis                                       ments for diverse architectural patterns.
We evaluate S EMANTIC F ORGE’s performance across reposi-
tories of varying sizes to demonstrate practical scalability for
                                                                 Architectural Transfer Analysis. The average Architec-
real-world deployment.
                                                                 tural Transfer Coefficient of 0.91 indicates strong cross-
                                                                 repository generalization, with only 4.3% average perfor-
Performance Stability. Pass@1 performance remains sta- mance degradation when applying models trained on differ-
ble (48.2%-51.4%) across repository sizes from 10K to 500K ent architectural patterns. System utilities show the strongest
lines of code, demonstrating that our approach scales without transfer (0.95), likely due to their procedural patterns appear-
quality degradation. Slight improvements for larger reposito- ing across many repository types. Web frameworks and sci-
ries may reflect richer knowledge graphs providing better con- entific computing show slightly lower transfer, reflecting their
text.                                                            more specialized architectural constraints.


                                                               24
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


Table 11: Cross-repository generalization results using leave-one-cluster-out validation. Performance degradation compared to
within-cluster training.

                Target Cluster           Within-Cluster      Cross-Cluster       Degradation      Transfer Coeff.
                Web Frameworks              52.8±2.3%          47.1±2.8%             5.7%               0.89
                Data Processing             48.1±2.2%          44.3±2.6%             3.8%               0.92
                Object-Oriented Libs        50.4±2.1%          46.2±2.5%             4.2%               0.92
                Scientific Computing        47.9±2.5%          42.8±3.1%             5.1%               0.89
                System Utilities            51.7±2.4%          48.9±2.7%             2.8%               0.95
                Average                     50.2±1.1%          45.9±1.3%             4.3%               0.91

Table 12: Performance breakdown by repository domain with architectural pattern analysis. Pass@1 results with 95% confi-
dence intervals.

             Domain                     GPT-4        S EMANTIC F ORGE         Improvement       Pattern Complexity
             Web Frameworks           43.2±2.1%          52.8±2.3%                +9.6%                 High
             Data Processing          39.8±2.4%          48.1±2.2%                +8.3%                Medium
             Object-Oriented Libs     41.5±2.0%          50.4±2.1%                +8.9%                 High
             System Utilities         42.1±2.6%          51.7±2.4%                +9.6%                Medium
             Scientific Computing     40.3±2.3%          47.9±2.5%                +7.6%                 Low


Knowledge Graph Semantic Overlap. Analysis of seman-                frameworks suffer primarily from signature violations (47%
tic overlap between repository clusters reveals interesting pat-    of errors), scientific computing from type mismatches (52%
terns. The average Semantic Overlap Index ranges from 0.34          of errors), and system utilities from visibility violations (38%
(scientific computing vs. web frameworks) to 0.67 (object-          of errors). S EMANTIC F ORGE’s constraint-aware generation
oriented libraries vs. system utilities). Higher semantic over-     adapts effectively to these domain-specific error patterns.
lap correlates strongly with better cross-repository perfor-
mance (r=0.84, p < 0.01), validating our knowledge graph
representation approach.                                            10.7    Human Evaluation Results
                                                                    Professional developer evaluation provides crucial insights
Domain Adaptation Efficiency. Few-shot adaptation with              into code quality aspects difficult to capture through automated
just 25-50 target domain examples recovers 89% of full-             metrics.
adaptation performance on average, demonstrating practical
deployment feasibility. Zero-shot performance maintains 91%
of within-cluster performance, indicating that our semantic         Overall Quality Assessment. Human evaluators rated S E -
representations capture fundamental programming patterns            MANTIC F ORGE solutions significantly higher (4.2/5.0) than
that generalize across architectural styles.                        baseline systems (GPT-4: 3.6/5.0, CodePlan: 3.4/5.0) on over-
                                                                    all code quality (p < 0.001, t-test). Evaluators particularly
10.6    Domain-Specific Performance                                 praised integration appropriateness and adherence to reposi-
                                                                    tory conventions.
Analysis across different repository domains reveals consistent
improvements while highlighting domain-specific challenges
and architectural pattern dependencies.                         Error Correction Effort. When solutions contained errors,
                                                                S EMANTIC F ORGE errors required significantly less correction
                                                                effort: 68% were classified as trivial fixes versus 41% for
Pattern Complexity Correlation. Domains with higher
                                                                GPT-4-Code. This reflects our constraint enforcement pre-
architectural pattern complexity (web frameworks, object-
                                                                venting complex schematic errors that require architectural un-
oriented libraries) show larger improvements, validating our
                                                                derstanding to fix.
hypothesis that explicit semantic representation provides
greater benefits for structurally complex codebases. The cor-
relation between pattern complexity and improvement magni- Preference Rankings. In head-to-head comparisons, evalu-
tude is r=0.78 (p < 0.05).                                      ators preferred S EMANTIC F ORGE solutions in 73% of cases,
                                                             with particular advantages cited for: ”better integration with
Constraint Type Distribution. Analysis of constraint vio- existing code” (89% of evaluators), ”fewer obvious bugs”
lation patterns reveals domain-specific characteristics: web (82%), and ”more appropriate API usage” (77%).


                                                               25
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


Table 13: Detailed computational overhead breakdown by system component with variance. Times represent mean ± 95% CI
over 4,250 tasks. Overhead percentages calculated relative to base Code-Llama-34B generation.

                Component                      Time (s)      Memory (GB)        Overhead (%)         Scaling
                Base Code-Llama               1.70 ± 0.12        11.2 ± 0.3             -             O(n)
                Knowledge Graph Query         0.31 ± 0.08         1.8 ± 0.2          18.2%          O(log n)
                Context Preparation           0.19 ± 0.04         0.3 ± 0.1          11.2%            O(k)
                SMT Constraint Checking       0.23 ± 0.06         0.7 ± 0.1          13.5%        O(c + —y—)
                Maintenance Updates           0.07 ± 0.02         0.2 ± 0.1           4.1%         O(∆ log n)
                Total S EMANTIC F ORGE        2.50 ± 0.18        14.2 ± 0.5         47.1%                -


10.8    Detailed Computational Overhead Analy- Scaling Characteristics and Performance Modeling.
        sis                                    Knowledge Graph Query Performance: Query latency
                                                                follows O(log n) complexity due to optimized indexing
We conduct comprehensive analysis of computational costs to strategies. For repositories from 10K to 500K LOC, query
demonstrate the practical viability of our approach and guide time scales from 0.15s to 0.42s, representing decreasing
deployment decisions across different resource constraints.     relative overhead (15% to 12%) as repository size increases.
                                                                This counter-intuitive improvement reflects the fact that larger
Measurement Methodology. All timing measurements fol- repositories contain more diverse context, improving cache hit
low rigorous protocols to ensure reproducibility and ac- rates and amortizing index construction costs.
curacy.     We measure wall-clock time using Python’s              Constraint Verification Scaling: SMT solver performance
time.perf counter() with nanosecond precision, av- exhibits O(c + —y—) complexity where c is the number
eraged over 100 runs per task on warmed-up systems of active constraints and —y— is the generated sequence
(5 warm-up runs discarded).         Each component is pro- length. Our incremental solving strategy maintains near-
filed independently using context managers that isolate its constant overhead regardless of repository size. For typical
specific contribution. Memory consumption is measured generation tasks (50-200 tokens), constraint checking time re-
via nvidia-smi for GPU memory (100ms sampling) mains 0.18-0.28s across all repository sizes tested.
and psutil.Process().memory info() for system                      Memory Usage Optimization: Memory scaling analysis
RAM, reporting peak values. We exclude model loading time reveals three distinct scaling regimes:
(one-time cost) but include all query processing, graph opera-
tions, and generation steps. Variance is reported as 95% confi-    • Small repositories (< 50K LOC): 12.4-13.1GB total,
dence intervals via bootstrap resampling (1000 samples).              dominated by model weights

Component-Level Performance Analysis. Our 47.1% to-                  • Medium repositories (50K-200K LOC): 13.1-14.8GB to-
tal overhead is dominated by knowledge graph infrastructure            tal, linear knowledge graph growth
(18.2%) and constraint verification (13.5%). Critically, both
components exhibit sub-linear scaling properties that improve        • Large repositories (> 200K LOC): 14.8-16.2GB total,
relative performance as repository size increases. The mainte-         sublinear growth due to graph compression
nance system adds minimal overhead (4.1%) while providing
essential adaptation capabilities.
                                                                   Hardware Resource Utilization. We profile hardware uti-
Cross-System Latency Comparison Methodology. To en-                lization using NVIDIA Nsight Systems for GPU metrics and
sure fair latency comparisons in Table 8, we implement con-        Linux perf for CPU analysis, sampling at 10ms intervals
sistent measurement protocols across all baselines. For RAG-       across 500 representative tasks. Results reveal efficient re-
based systems (Code-Llama, StarCoder, RAG-Code), we mea-           source usage: 89% average GPU compute utilization during
sure total time including retrieval, encoding, and generation.     code generation (1.70s), 12% during knowledge graph queries
For CodePlan, we measure end-to-end time including task de-        (CPU-bound, 0.31s), and 67% during constraint verification
composition (GPT-3.5 call) and all subtask generations. For        (mixed workload, 0.23s). CPU utilization peaks at 78% dur-
GPT-4-Code, we measure API call latency including network          ing graph query execution (parallel traversal) and averages
overhead and server-side processing. All measurements ex-          34% during SMT solving (single-threaded bottleneck). Mem-
clude one-time costs (model loading, index construction) but       ory bandwidth utilization averages 62% during generation and
include per-request processing. Each system is run 100 times       23% during graph operations, indicating room for further op-
per task with median reported to avoid network variance for        timization. These profiles inform deployment: GPU-heavy
API-based systems. The confidence intervals in Table 8 reflect     workloads benefit from model parallelism, while graph-heavy
variation across tasks, not measurement noise.                     workloads scale with CPU cores.


                                                              26
                                 Journal of Emerging Applied Artificial Intelligence (JEAAI)


Optimization Impact Analysis. We measure the effective-            This comprehensive computational analysis demonstrates
ness of our optimization strategies through controlled ablation that S EMANTIC F ORGE’s benefits justify its overhead across
where each optimization is disabled independently and perfor- realistic deployment scenarios, with particularly strong value
mance re-measured:                                              propositions for team and enterprise environments.

   • Query result caching: 34% latency reduction (0.47s →
     0.31s), 73% cache hit rate measured across 1000-task se- 10.9 Error Analysis and Failure Cases
     quences simulating developer sessions                     We analyze remaining failure cases to understand system lim-
                                                               itations and guide future improvements.
   • Incremental SMT solving: 67% constraint verification
     speedup (0.69s → 0.23s) vs. naive per-beam full solv-
     ing, measured on 500 constraint-heavy tasks               Persistent Logical Errors. Complex algorithmic tasks re-
                                                               quiring multi-step reasoning still challenge the system, par-
   • Graph compression: 43% memory reduction (2.5GB → ticularly when the correct approach differs significantly from
     1.4GB graph storage) with < 2% query performance training data patterns. Dynamic traces help but cannot fully
     degradation (0.30s → 0.31s), validated on 200K+ LOC compensate for insufficient algorithmic understanding.
     repositories
                                                               Novel API Usage. When repositories use recently-
   • Predictive prefetching: 28% perceived latency reduc- introduced APIs not represented in training data, both retrieval
     tion during interactive sessions, measured via user study and generation quality decline. The maintenance system
     (n=12 developers, 50 tasks each)                          partially addresses this through incremental updates, but
                                                               fundamental model limitations remain.
Real-World Deployment Scenarios. We model computa-
tional requirements for three deployment scenarios:            Cross-Language Dependencies. Repositories with mixed-
   Individual Developer Setup: Single NVIDIA RTX 4090 language components (Python calling C extensions, JavaScript
(24GB) can handle repositories up to 200K LOC with 2.1s frontends) present challenges for our primarily Python-
average latency. Memory-optimized configurations support up focused analysis. Future work should extend knowledge graph
to 350K LOC with 3.2s latency using model quantization and construction to multi-language scenarios.
graph streaming.
   Team Development Server: Server-grade hardware (4×
                                                               Complex Refactoring Tasks. Large-scale refactoring re-
A100, 256GB RAM) supports concurrent access for 8-12 de-
                                                               quiring simultaneous changes across many files sometimes ex-
velopers with < 3s response times. Load balancing across
                                                               ceeds the context window limits and constraint complexity
GPUs enables 45-60 requests/minute sustained throughput.
                                                               thresholds. Hierarchical approaches may address these limi-
   Enterprise Cloud Deployment: Distributed deployment tations.
across 16 A100 nodes supports 200+ concurrent developers
                                                                  These comprehensive results demonstrate S EMANTIC -
with auto-scaling based on demand patterns. Average response
                                                               F ORGE’s significant advances in repository-level code gener-
time < 2.5s at 95th percentile during peak usage periods.
                                                               ation while identifying important directions for continued re-
                                                               search and development.
Energy Efficiency Analysis. S EMANTIC F ORGE consumes
187J per generation task (vs. 142J for base Code-Llama), rep-
resenting 32% energy overhead. However, the 15.6% improve- 11 Discussion and Limitations
ment in Pass@1 over base Code-Llama reduces debugging it-
erations, resulting in net 23% energy savings per successful This section provides critical analysis of S EMANTIC F ORGE’s
implementation when accounting for developer iteration pat- contributions, examines the broader implications of our ap-
terns.                                                         proach, and honestly assesses the limitations that constrain its
                                                               applicability. We discuss the generalizability of our findings
                                                               and identify important directions for future research.
Cost-Benefit Optimization. ROI analysis reveals break-
even points for different deployment scenarios:
                                                                   11.1   Key Contributions and Impact
  • Individual developers: Positive ROI after 120 hours of
    usage (typical: 2-3 months)                           S EMANTIC F ORGE represents a fundamental shift from
                                                          pattern-matching-based code generation to semantically-
  • Small teams (5-10 developers): Positive ROI after 60 aware synthesis. Our results demonstrate that explicit repos-
    hours of collective usage (typical: 3-4 weeks)        itory knowledge graphs, when combined with learned query
                                                          planning and constraint-aware decoding, can significantly re-
  • Enterprise teams (50+ developers): Positive ROI after duce the hallucination phenomena that limit current LLM-
    200 hours of collective usage (typical: 1-2 weeks)    based development tools.


                                                              27
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


Theoretical Contributions. We formalize the repository-              management for C++, checked exceptions for Java), and (3)
level code generation problem and provide the first compre-          Integrate with language-specific testing frameworks for dy-
hensive taxonomy of hallucination types in code generation.          namic analysis. The MultiPL-E framework [2] provides valu-
Our mathematical framework establishes theoretical founda-           able translation infrastructure that could bootstrap our cross-
tions for knowledge graph-guided generation while proving            language knowledge graph construction.
complexity bounds for each system component. The constraint             Dynamically-Typed Languages (JavaScript, Ruby,
satisfaction formulation enables principled analysis of genera-      PHP): These present greater challenges due to limited static
tion correctness.                                                    type information. Our preliminary analysis suggests perfor-
                                                                     mance degradation of 15-25% compared to Python results.
Systems Contributions. The integration of SMT solvers                However, several mitigation strategies show promise: (1)
into neural beam search represents a novel architectural ap-         TypeScript adoption patterns provide type hints for JavaScript,
proach that guarantees constraint satisfaction without sacrific-     (2) Runtime type inference through execution profiling, and
ing generation quality. Our incremental maintenance system           (3) Gradual typing systems (Flow for JavaScript, Sorbet for
demonstrates how knowledge graphs can remain synchronized            Ruby) enable hybrid static-dynamic analysis. CodeSearch-
with evolving codebases at practical computational costs. The        Net’s multi-language dataset [12] covering six languages
dual static-dynamic representation provides a new paradigm           could serve as a foundation for training multi-language query
for capturing repository semantics.                                  planners.
                                                                        Functional Languages (Haskell, OCaml, Scala): The
Empirical Impact. The 49.8% reduction in schematic hal-              strong type systems and immutability constraints in functional
lucination and 34.7% reduction in logical hallucination trans-       languages align well with our constraint satisfaction approach.
late to substantial developer productivity gains. Eliminating        Type-level programming features require extended constraint
type errors, signature mismatches, and import issues reduces         languages but may enable even stronger semantic guarantees.
debugging effort and increases confidence in generated code.         Pattern matching and algebraic data types provide rich struc-
The 15.6% improvement in functional correctness over base            tural information for knowledge graph construction.
Code-Llama enables more ambitious automated development                 Cross-Language Integration: Modern repositories in-
tasks.                                                               creasingly involve multiple languages. We identify three in-
                                                                     tegration patterns: (1) Foreign Function Interfaces (FFI) re-
                                                                     quiring cross-language type mapping, (2) Service boundaries
11.2    Generalizability Analysis
                                                                     with API contracts, and (3) Build system dependencies. A
While our evaluation focuses on Python repositories, the un-         unified knowledge graph representation could capture these
derlying principles of S EMANTIC F ORGE extend to other pro-         relationships, enabling repository-level reasoning across lan-
gramming paradigms and development contexts, though with             guage boundaries. Recent work on multi-lingual evaluation
varying degrees of adaptation required.                              [1] demonstrates the feasibility of unified semantic represen-
                                                                     tations across language barriers, suggesting our knowledge
Multi-Language Extension Roadmap. Our analysis re-                   graph approach could extend naturally to polyglot codebases.
veals a clear path for extending S EMANTIC F ORGE to addi-
tional programming languages, with different languages pre-          Domain Adaptability. The architectural patterns captured
senting distinct opportunities and challenges. Recent multi-         in our knowledge graphs reflect common software engineer-
language code generation efforts [33, 12, 1, 2] provide impor-       ing practices that span domains. Web development, data pro-
tant foundations for this extension:                                 cessing, and system programming all benefit from understand-
   Statically-Typed Languages (Java, C++, TypeScript):               ing dependency relationships and API constraints. However,
These languages offer significant advantages for S EMANTIC -         highly specialized domains require targeted extensions:
F ORGE deployment. Explicit type information enables more               Embedded Systems: Require resource constraints (mem-
precise constraint extraction, reducing the 14.7% schematic          ory, power, real-time), hardware abstraction layer modeling,
hallucination rate we observe in Python to an estimated 8-           and interrupt-driven control flow patterns.
12%. PolyCoder’s evaluation [33] across 12 programming
                                                                        Financial Systems: Need precision arithmetic constraints,
languages shows that static typing improves model accuracy
                                                                     regulatory compliance patterns, and audit trail requirements.
by 8-15%, supporting our hypothesis. The rich type systems
                                                                        Scientific Computing: Benefit from numerical stability
provide stronger semantic foundations for knowledge graph
                                                                     constraints, performance modeling, and domain-specific li-
construction. However, complex generics systems (C++ tem-
                                                                     braries (NumPy, BLAS) integration.
plates, Java wildcards) require sophisticated constraint model-
ing to capture type relationships accurately.
   Implementation Strategy: We propose a three-phase roll-           Scale Considerations. Our scalability analysis demon-
out building on multi-language parsing infrastructure: (1) Ex-       strates effectiveness up to 500K lines of code, covering most
tend static analysis using language-specific parsers (Tree-sitter    organizational repositories. However, massive monorepos (>
for C++, JavaParser for Java, TypeScript Compiler API), (2)          10M LOC) require architectural innovations: (1) Hierarchical
Adapt constraint types to language-specific features (memory         knowledge graphs with module-level abstractions, (2) Feder-


                                                                28
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


ated query planning across repository boundaries, and (3) Dis-       11.4    Computational and Practical Limitations
tributed constraint solving for large-scale generation tasks.
                                                                     Real-world deployment of S EMANTIC F ORGE faces several
                                                                     practical constraints that affect its adoption and effectiveness.
Development Workflow Integration. S EMANTIC F ORGE
assumes development environments with comprehensive test             Infrastructure Requirements. The system requires sub-
suites and stable APIs. Organizations with poor testing prac-        stantial computational resources: 40GB GPU memory for gen-
tices or rapidly changing architectures may see reduced ben-         eration, significant CPU resources for graph construction, and
efits from dynamic analysis and constraint enforcement. We           storage for knowledge graphs. These requirements may limit
propose adaptation strategies: (1) Property-based testing inte-      adoption in resource-constrained environments or small devel-
gration for coverage improvement, (2) API stability analysis         opment teams.
for architecture change detection, and (3) Gradual adoption
paths for legacy codebases.                                        Setup and Maintenance Overhead. Initial repository anal-
                                                                   ysis requires 5-47 seconds depending on size, creating friction
                                                                   for new project adoption. The knowledge graph maintenance
11.3 Fundamental Limitations                                       system, while incremental, adds complexity to development
Despite significant advances, S EMANTIC F ORGE faces several workflows. Organizations must weigh these costs against pro-
fundamental limitations that constrain its applicability and ef- ductivity benefits.
fectiveness.
                                                                   SMT Solver Limitations. Our constraint enforcement relies
                                                                   on SMT solver capabilities, which can be overwhelmed by
Algorithmic Reasoning Limitations. While our system ex- complex constraint sets or exhibit unpredictable performance
cels at structural integration and constraint satisfaction, it in- on certain problem types. The 100ms timeout prevents block-
herits the algorithmic reasoning limitations of underlying lan- ing but may allow constraint violations in edge cases.
guage models. Complex logical problems requiring multi-
step reasoning, mathematical derivations, or novel algorithmic
                                                                   Test Suite Dependencies. Dynamic analysis effectiveness
insights remain challenging. The knowledge graph provides
                                                                   correlates strongly with test suite quality and coverage. Repos-
context but cannot substitute for deep algorithmic understand-
                                                                   itories with poor testing practices receive limited benefits from
ing.
                                                                   our dual static-dynamic approach. This creates a barrier for
   Example: When asked to implement a novel graph algo- adoption in organizations with immature testing cultures.
rithm, S EMANTIC F ORGE can correctly identify relevant data
structures and API patterns but may struggle with the core al-
gorithmic logic if it differs significantly from training exam- 11.5 Ethical and Safety Considerations
ples.                                                              The deployment of advanced code generation systems raises
                                                               important ethical considerations that must be addressed re-
Creative Design Limitations. Repository knowledge sponsibly.
graphs capture existing patterns but may constrain creative
architectural decisions. The system tends to perpetuate Code Quality and Reliability. While S EMANTIC F ORGE
established patterns rather than proposing innovative designs. significantly reduces hallucination rates, it cannot eliminate all
This conservatism improves integration consistency but may errors. Developers must maintain critical evaluation of gen-
limit architectural evolution.                                 erated code, particularly for security-sensitive applications.
                                                               Over-reliance on automated generation could lead to decreased
                                                               code review rigor.
Training Data Dependencies. Like all learning-based sys-
tems, S EMANTIC F ORGE is limited by its training data. Repos-
                                                               Intellectual Property Concerns. Knowledge graphs con-
itories using cutting-edge frameworks, novel programming
                                                               structed from proprietary codebases may inadvertently expose
patterns, or domain-specific APIs may receive suboptimal sup-
                                                               internal architectural patterns or business logic. Organizations
port. While the maintenance system addresses this partially,
                                                               must carefully consider the privacy implications of compre-
fundamental knowledge gaps require model retraining.
                                                               hensive code analysis and ensure appropriate access controls.

Context Window Constraints. Despite efficient query                  Developer Skill Evolution. Highly effective code genera-
planning, very large development tasks may exceed practi-            tion tools may impact developer skill development, particu-
cal context limits. Complex refactoring operations affecting         larly for junior programmers who rely heavily on automated
dozens of files simultaneously challenge both the planning           assistance. Balancing productivity gains with skill develop-
system and the generation model. Hierarchical approaches             ment remains an important challenge for the software engi-
may address this but remain unexplored.                              neering community.


                                                                29
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


Bias Amplification. Repository knowledge graphs neces-               knowledge graphs for polyglot repositories represent a partic-
sarily reflect the patterns and conventions of their source code-    ularly compelling direction, enabling unified reasoning about
bases. If these repositories contain biased or suboptimal pat-       system-wide architectural constraints. The multi-lingual eval-
terns, S EMANTIC F ORGE may perpetuate and amplify these             uation framework of Athiwaratkun et al. [1] suggests that
issues. Regular audit and pattern analysis can help identify         semantic representations can transfer across language bound-
problematic trends.                                                  aries with modest adaptation.

11.6    Comparison with Contemporary Ap- Security-Aware Code Generation. Integrating security
        proaches                         vulnerability patterns and compliance rules into constraint lan-
                                                              guages represents a critical next step. Future work could de-
Recent advances in repository-level code generation provide
                                                              velop domain-specific constraint types for vulnerability pre-
important context for evaluating S EMANTIC F ORGE’s contri-
                                                              vention, regulatory compliance, and industry-specific security
butions.
                                                              standards. This direction promises significant practical impact
                                                              given the growing importance of secure-by-construction soft-
Agent-Based Systems. Contemporary systems like SWE- ware development.
agent and CodeAgent employ iterative refinement through en-
vironmental feedback. While these approaches can handle
complex multi-step tasks, they suffer from higher latency and Performance-Optimized Generation. Incorporating com-
computational costs. S EMANTIC F ORGE’s constraint-aware putational complexity analysis and performance characteris-
generation often produces correct solutions in a single pass, tics into knowledge graphs could enable generation systems
offering better efficiency for well-defined tasks.            that consider algorithmic efficiency, memory usage patterns,
                                                              and distributed system implications. This extension would ad-
Planning-Based Approaches. Systems like CodePlan de- dress the growing need for performance-aware automated de-
compose complex tasks into sequences of simpler operations. velopment tools in resource-constrained environments.
This approach complements S EMANTIC F ORGE’s capabilities
and could potentially be integrated with our knowledge graph Collaborative Development Integration. Extending S E -
representation. However, planning-based systems typically MANTIC F ORGE to multi-developer environments presents in-
lack the constraint enforcement that prevents schematic hal- teresting challenges in conflict prediction, team expertise mod-
lucination.                                                     eling, and collaborative context selection. Knowledge graphs
                                                                could capture team dynamics and expertise distribution, en-
Retrieval-Augmented Methods. Advanced RAG systems abling more effective task allocation and code review assis-
continue to improve context selection for code generation. tance.
However, these approaches remain fundamentally limited by
their inability to reason about global consistency and archi- Architectural Evolution Assistance. Beyond code genera-
tectural constraints. S EMANTIC F ORGE’s explicit knowledge tion, knowledge graphs could support proactive architecture
representation provides capabilities that pure retrieval cannot improvement through code smell detection, design pattern rec-
match.                                                          ommendations, and architectural debt assessment. This direc-
                                                                     tion aligns with the broader trend toward AI-assisted software
11.7    Future Research Directions                                   architecture and design.
Our work opens several promising avenues for future research
in repository-level code generation and automated software Educational Applications. The explicit constraint represen-
development. These directions build naturally on our findings tation in S EMANTIC F ORGE suggests natural applications in
while addressing broader challenges in the field.                   computer science education, including pedagogical constraint
                                                                    languages that enforce learning objectives and automated as-
Multi-Language Extension. The most immediate exten- sessment of software engineering practices. This could de-
sion involves adapting S EMANTIC F ORGE to additional mocratize access to high-quality programming education and
programming languages.         Recent multi-language bench- mentorship.
marks—PolyCoder’s 12-language evaluation [33], Code-
SearchNet’s 6-language corpus [12], and MultiPL-E’s poly- 11.8 Implications for Software Engineering
glot test suite [2]—provide crucial infrastructure for this effort.
Statically-typed languages like Java and TypeScript present S EMANTIC F ORGE represents a step toward more sophisti-
opportunities for enhanced constraint extraction through ex- cated automated development tools that understand and re-
plicit type information, potentially reducing schematic hal- spect software engineering principles. The explicit represen-
lucination rates below our current 14.7%. Dynamic lan- tation of architectural knowledge enables systems that gener-
guages pose different challenges, requiring sophisticated run- ate code consistent with established patterns while maintaining
time analysis and gradual typing integration. Cross-language flexibility for innovation.


                                                                30
                                Journal of Emerging Applied Artificial Intelligence (JEAAI)


   However, the most significant impact may be in democratiz-     eliminates schematic hallucination at the source rather than re-
ing access to complex software development capabilities. By       quiring post-hoc correction.
encoding expert knowledge about API usage, architectural pat-
terns, and constraint satisfaction, S EMANTIC F ORGE enables      Comprehensive Empirical Evaluation. Our evaluation on
less experienced developers to produce higher-quality code        R EPO KG-50 establishes new benchmarks for repository-
that integrates properly with sophisticated codebases.            level code generation assessment. The 49.8% reduction in
   The constraint satisfaction approach also suggests new         schematic hallucination, 34.7% reduction in logical halluci-
paradigms for software development where architectural rules      nation, and 15.6% improvement in functional correctness over
and patterns are explicitly encoded and automatically en-         base Code-Llama demonstrate the practical impact of our ap-
forced. This could lead to more consistent codebases, reduced     proach.
maintenance overhead, and improved software quality across
the industry.
   Ultimately, S EMANTIC F ORGE demonstrates that the com-        12.2    Broader Impact
bination of symbolic reasoning and neural generation can ad-      S EMANTIC F ORGE represents a paradigm shift from pattern-
dress fundamental limitations of purely learning-based ap-        matching-based code generation to semantically-aware syn-
proaches, pointing toward a future where automated develop-       thesis. This advance has implications beyond immediate pro-
ment tools are both more capable and more reliable.               ductivity gains:


12     Conclusion                                               Developer Productivity. By dramatically reducing debug-
                                                                ging overhead and increasing confidence in generated code,
This paper introduces S EMANTIC F ORGE, a novel approach S EMANTIC F ORGE enables developers to tackle more ambi-
to repository-level code generation that addresses the fun- tious automated development tasks. The elimination of triv-
damental limitations of current LLM-based systems through ial errors allows focus on higher-level design and algorithmic
explicit semantic representation and constraint-aware genera- challenges.
tion. Our comprehensive evaluation demonstrates significant
advances in both functional correctness and hallucination re- Code Quality and Maintainability. Constraint-aware gen-
duction, while establishing new theoretical foundations for un- eration ensures that automated code follows established archi-
derstanding and solving the repository-level code generation tectural patterns and respects design principles. This leads
problem.                                                        to more consistent codebases with reduced maintenance over-
                                                                head and improved long-term sustainability.
12.1    Summary of Contributions
                                                               Democratization of Complex Development. By encoding
We make four primary contributions that advance the state-of- expert knowledge about API usage, architectural patterns, and
the-art in automated code generation:                          constraint satisfaction, S EMANTIC F ORGE enables less experi-
                                                               enced developers to work effectively with sophisticated code-
Problem Formalization and Hallucination Taxonomy. bases. This could help address skill gaps in software engineer-
We provide the first formal treatment of repository-level code ing.
generation, establishing mathematical foundations and com-
plexity analysis. Our comprehensive taxonomy of logical and Foundation for Advanced Tools. The explicit semantic
schematic hallucination provides a principled framework for representation and constraint satisfaction framework provide
understanding and addressing systematic failures in current foundations for even more sophisticated development assis-
code generation systems.                                       tance, including architectural evolution, security-aware gen-
                                                                eration, and collaborative development support.
Knowledge Graph-Guided Architecture. The four-stage
S EMANTIC F ORGE pipeline demonstrates how explicit seman-
                                                                12.3 Technical Significance
tic representation can enable more sophisticated code gen-
eration. Our dual static-dynamic knowledge graphs capture The technical innovations in S EMANTIC F ORGE establish im-
repository semantics that are invisible to purely pattern-based portant precedents for the integration of symbolic reasoning
approaches, while neural query planning enables efficient con- and neural generation:
text selection at scale.
                                                                  Hybrid Symbolic-Neural Approaches. Our SMT-guided
Constraint-Aware Generation Algorithm. The integration            beam search demonstrates how formal verification can be
of SMT solving into neural beam search represents a funda-        seamlessly integrated into neural generation without pro-
mental architectural innovation that guarantees semantic cor-     hibitive computational overhead. This opens new possibilities
rectness without sacrificing generation quality. This approach    for constraint-aware AI systems across domains.

                                                             31
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


Scalable Knowledge Representation. The incremental                  Constraint Integration in Generation. The effectiveness
maintenance of repository knowledge graphs at O(|∆R|)               of SMT-guided decoding indicates that constraint satisfaction
complexity shows how explicit semantic representations can          should be a primary consideration in generation system design.
remain practical even for large-scale systems. This scalability     Future work should explore how different constraint types and
is crucial for real-world deployment.                               solving approaches affect generation quality and efficiency.

                                                                    Continual Learning for Code Systems. The success of
Learned Context Selection. Neural query planning pro-
                                                                    our maintenance agent highlights the importance of contin-
vides a general framework for learning to select relevant con-
                                                                    ual adaptation in software-related AI systems. As codebases
text from large structured knowledge bases. This approach
                                                                    evolve rapidly, static models quickly become obsolete without
could generalize to other domains requiring selective informa-
                                                                    mechanisms for incremental learning.
tion retrieval.

                                                                    Multi-Modal Code Understanding. Repository-level code
12.4    Limitations and Future Directions                           generation requires understanding text, code structure, execu-
                                                                    tion traces, and architectural patterns. This multi-modal chal-
While S EMANTIC F ORGE achieves significant advances, im-           lenge suggests directions for more comprehensive code under-
portant limitations remain:                                         standing systems.


Algorithmic Reasoning. Complex logical problems requir- 12.6 Practical Deployment Considerations
ing multi-step reasoning or novel algorithmic insights continue
                                                                For practitioners considering deployment of S EMANTIC -
to challenge the system. Future work should investigate inte-
                                                                F ORGE or similar systems, our experience highlights several
gration of symbolic reasoning systems and algorithmic knowl-
                                                                important factors:
edge bases.

                                                                    Test Suite Quality. The effectiveness of dynamic analysis
Multi-Language Support. Our current focus on Python                 correlates strongly with test coverage and quality. Organiza-
limits applicability to mixed-language environments common          tions should invest in comprehensive testing infrastructure to
in enterprise development. The concrete roadmap in Sec-             maximize benefits from advanced code generation tools.
tion 11.7 outlines specific milestones for Java, TypeScript, and
cross-language integration.                                    Incremental Adoption. S EMANTIC F ORGE’s modular ar-
                                                               chitecture enables incremental deployment, allowing organi-
                                                               zations to adopt components gradually. Starting with knowl-
Creative Design Tasks. The system’s emphasis on consis-
                                                               edge graph construction and query planning provides immedi-
tency and constraint satisfaction may limit creative archi-
                                                               ate benefits with lower risk.
tectural exploration. Balancing reliability with innovation
through configurable constraint relaxation represents an im-
portant research direction.                                    Developer Training. Successful deployment requires train-
                                                               ing developers to effectively collaborate with AI-assisted gen-
                                                               eration tools. Understanding system capabilities and limita-
Resource Requirements. The computational and infras- tions is crucial for productive use.
tructure requirements for S EMANTIC F ORGE may limit adop-
tion in resource-constrained environments. Our detailed cost- Infrastructure Planning. The computational requirements
benefit analysis in Section 10.8 provides guidance for deploy- for S EMANTIC F ORGE necessitate careful infrastructure plan-
ment optimization strategies.                                  ning. Organizations should evaluate resource needs against
                                                                    expected productivity gains.
12.5    Research Implications
                                                                    12.7    Long-Term Vision
S EMANTIC F ORGE’s success suggests several important direc-
tions for future research in automated software development:        S EMANTIC F ORGE represents progress toward a long-term vi-
                                                                    sion of AI-assisted software development where automated
                                                                    tools understand and respect the principles of software engi-
Explicit vs. Implicit Knowledge. Our results demonstrate            neering. In this future, developers work collaboratively with
clear advantages for explicit semantic representation over          AI systems that understand architectural patterns, maintain
purely implicit approaches. This finding has implications for       consistency across large codebases, and generate code that is
AI system design beyond code generation, suggesting when            not only functional but maintainable and well-integrated.
symbolic knowledge should complement learned representa-               This vision requires continued research across multiple di-
tions.                                                              mensions: better algorithmic reasoning, more sophisticated


                                                               32
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


constraint systems, improved human-AI collaboration inter-              and Abhinav Jangda. Multipl-e: A scalable and poly-
faces, and deeper understanding of software engineering prin-           glot approach to benchmarking neural code genera-
ciples. S EMANTIC F ORGE provides a foundation for this re-             tion. IEEE Transactions on Software Engineering,
search by demonstrating that explicit semantic representation           49(7):3675–3691, 2023. arXiv:2208.08227.
and constraint-aware generation can address fundamental lim-
itations of current approaches.                                     [3] Mark Chen, Jerry Tworek, Christopher Jun, Qiming
   The ultimate goal is not to replace human developers but             Zhai, et al. Evaluating large language models trained on
to amplify their capabilities, enabling them to focus on cre-           code. In Proceedings of the 38th International Confer-
ative design, architectural innovation, and complex problem-            ence on Machine Learning, 2021. arXiv:2107.03374.
solving while automated systems handle routine implementa-
                                                                    [4] Yicheng Chen, Shiqi Wang, Song Feng, et al. Teaching
tion tasks with reliability and consistency. S EMANTIC F ORGE
                                                                        large language models to self-improve at code generation
takes an important step toward this collaborative future.
                                                                        via retrieval augmented refinement. In arXiv preprint
                                                                        arXiv:2310.01234, 2023.
12.8    Closing Remarks
                                                                    [5] Leonardo de Moura and Nikolaj Bjørner. Z3: An ef-
Repository-level code generation represents one of the most             ficient smt solver. In Tools and Algorithms for the
challenging problems in automated software development, re-             Construction and Analysis of Systems, volume 4963 of
quiring systems that understand not just local code patterns            Lecture Notes in Computer Science, pages 337–340.
but global architectural principles and semantic constraints.           Springer, 2008.
S EMANTIC F ORGE demonstrates that this challenge can be
addressed through careful integration of symbolic reasoning         [6] Yangruibo Ding, Zijian Wang, Wasi Ahmad, Murali Kr-
and neural generation, explicit knowledge representation, and           ishna Ramanathan, Ramesh Nallapati, Parminder Bhatia,
constraint-aware synthesis.                                             Dan Roth, and Bing Xiang. Cocomic: Code comple-
   Our results show significant advances in both functional cor-        tion by jointly modeling in-file and cross-file context. In
rectness and hallucination reduction, while our open-source             Proceedings of the 2024 Joint International Conference
release of R EPO KG-50 provides a foundation for continued              on Computational Linguistics, Language Resources and
research in this critical area. The techniques and insights             Evaluation (LREC-COLING 2024), pages 3456–3468,
from S EMANTIC F ORGE have broader applicability to other               2024. arXiv:2212.10007.
domains requiring constraint-aware generation and semantic
consistency.                                                        [7] GitHub.    Github copilot:    Your ai pair pro-
   As AI-assisted development tools become increasingly so-             grammer.   https://github.com/features/
phisticated, the principles demonstrated in S EMANTIC F ORGE            copilot, 2021. Accessed: 2025-07-14.
–explicit knowledge representation, learned context selection,
                                                                    [8] Google Inc. Bazel: A fast, scalable, multi-language build
constraint-aware generation, and continual adaptation—will
                                                                        system.
become essential components of reliable and effective auto-
                                                                        urlhttps://bazel.build/, 2015. Open-sourced March 2015.
mated development systems. We look forward to continued
                                                                        Accessed: 2025-07-22.
research building on these foundations to realize the full po-
tential of AI-assisted software engineering.                        [9] Daya Guo, Shuo Ren, Suyuan Lu, Song Feng, Duyu
                                                                        Tang, Shuai Zhang, Zhi Liu, Daya Tang, and Zhi Jin.
                                                                        Graphcodebert: Pre-training code representations with
References                                                              data flow. In Proceedings of the 30th International Joint
                                                                        Conference on Artificial Intelligence, 2021.
 [1] Ben Athiwaratkun, Sanjay Krishna Gouda, Zijian Wang,
     Xiaopeng Li, Yuchen Tian, Ming Tan, Wasi Uddin [10] Daya Guo, Shuning Zhao, Duyu Tang, et al. Unixcoder:
     Ahmad, Shiqi Wang, Qing Sun, Mingyue Shang, Su-         Unified cross-modal pre-training for code understand-
     jan Kumar Gonugondla, Hantian Ding, Varun Kumar,        ing and generation. In Proceedings of the 60th Annual
     Nathan Fulton, Arash Farahani, Siddhartha Jain, Robert  Meeting of the Association for Computational Linguis-
     Giaquinto, Haifeng Qian, Murali Krishna Ramanathan,     tics, 2022.
     Ramesh Nallapati, Baishakhi Ray, Parminder Bhatia,
     Sudipta Sengupta, Dan Roth, and Bing Xiang. Multi- [11] Ashish Gupta and Inderpal Singh Mumick. Maintenance
     lingual evaluation of code generation models. In Pro-   of materialized views: Problems, techniques, and appli-
     ceedings of the 40th International Conference on Ma-    cations. IEEE Data Engineering Bulletin, 18(2):3–18,
     chine Learning (ICML), 2023. arXiv:2210.14868.          June 1995. Special Issue on Materialized Views and Data
                                                             Warehousing.
 [2] Federico Cassano, John Gouwar, Daniel Nguyen, Syd-
     ney Nguyen, Luna Phipps-Costin, Donald Pinckney, [12] Hamel Husain, Ho-Hsiang Wu, Tiferet Gazit, Miltiadis
     Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson,        Allamanis, and Marc Brockschmidt. Codesearchnet
     Molly Q. Feldman, Arjun Guha, Michael Greenberg,        challenge: Evaluating the state of semantic code search.

                                                               33
                                Journal of Emerging Applied Artificial Intelligence (JEAAI)


     In arXiv preprint arXiv:1909.09436, 2019. Multi- [22] Hammond Pearce, Baleegh Ahmad, Benjamin Tan,
     language dataset covering Python, Java, JavaScript, PHP,       Brendan Dolan-Gavitt, and Ramesh Karri. Asleep at the
     Ruby, and Go.                                                  keyboard? assessing the security of github copilot’s code
                                                                    contributions. In Proceedings of the 2022 IEEE Sym-
[13] Quoc Le, Mark Chen, et al. Coderl: Program syn-                posium on Security and Privacy, pages 754–768, 2022.
     thesis with reinforcement learning. In arXiv preprint          arXiv:2108.09293.
     arXiv:2211.00067, 2022.
                                                               [23] Gabriel Poesia, Oleksandr Polozov, Vu Le, Ashish Ti-
[14] Xiaonan Li, Yeyun Gong, Yelong Shen, Xipeng Qiu,               wari, Gustavo Soares, Christopher Meek, and Sumit Gul-
     Hang Zhang, Bolun Yao, Weizhen Qi, Daxin Jiang,                wani. Synchromesh: Reliable code generation from pre-
     Weizhu Chen, and Nan Duan. Coderetriever: A large              trained language models. In Proceedings of the 10th
     scale contrastive pre-training method for code search. In      International Conference on Learning Representations
     Proceedings of the 2022 Conference on Empirical Meth-          (ICLR), 2022. arXiv:2201.11227.
     ods in Natural Language Processing (EMNLP), pages
     2898–2910, 2022.                                          [24] Ramya Ramakrishnan, Aws Albarghouthi, Somesh
                                                                    Jha, and Thomas Reps.          Codeplan: Repository-
[15] Yujia Li, David Choi, Junyoung Chung, Nate Kushman,            level coding using llms and planning. arXiv preprint
     Julian Schrittwieser, Rémi Leblond, Tom Eccles, James         arXiv:2309.12499, 2023.
     Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hu-
     bert, Peter Choy, Cyprien de Masson d’Autume, Igor [25] Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten
     Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes                Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu
     Welbl, Sven Gowal, Alexey Cherepanov, James Molloy,            Liu, Tal Remez, Jérémy Rapin, et al. Code llama:
     Daniel J. Mankowitz, Esme Sutherland Robson, Push-             Open foundation models for code. arXiv preprint
     meet Kohli, Nando de Freitas, Koray Kavukcuoglu, and           arXiv:2308.12950, 2023. Accessed: 2025-07-22.
     Oriol Vinyals. Competition-level code generation with [26] Divyansh Shrivastava, Hugo Larochelle, and Daniel Tar-
     alphacode. Science, 378(6624):1092–1097, 2022.                 low. Rag-code: Retrieval augmented generation for code
[16] Jiawei Liu, Lin Chen, and Hongyu Zhang. Codekg:        synthesis. In Proceedings of the 2023 Conference on Em-
     Building knowledge graphs from code documentation      pirical Methods in Natural Language Processing, pages
     and api references. In Proceedings of the 29th IEEE    2234–2245, 2023.
     International Conference on Program Comprehension [27] Chunqiu Song, Mingyang Zhou, et al. An empirical
     (ICPC), pages 321–331, 2021.                           study of code generation errors made by large language
[17] Ming Luo. Machine learning for time series analysis    models. In Workshop on Machine Learning for Program-
     and forecasting. Master’s thesis, Northeastern Univer- ming (ML4P), 2023.
     sity, Boston, Massachusetts, May 2023.                    [28] Shashank Srikant, Benjamin O’Brien, Sebastian Tschi-
[18] Meta AI.        Code llama: Open foundation mod-               atschek, Eugene Bagdasaryan, Rishabh Rozen, Vikash
     els for code.       https://ai.meta.com/blog/                  Krishnamurthy, et al. Generating secure code with lan-
     code-llama-large-language-model/, 2023.                        guage models. In arXiv preprint arXiv:2306.23034,
     Accessed: 2025-07-14.                                          2023.
                                                               [29] Mingxi Tang et al. Codeagent: Autonomous program-
[19] Microsoft Corporation. Pylance: Fast, feature-rich
                                                                    ming with conversational software agents. In arXiv
     language support for python in visual studio code.
                                                                    preprint arXiv:2312.13010, 2023.
     urlhttps://devblogs.microsoft.com/python/announcing-
     pylance-fast-feature-rich-language-support-for-python-    [30] Hao Wang, Chen Li, Qian Zhang, and Yang Liu. Pro-
     in-visual-studio-code/, 2020. Accessed: 2025-07-22.            gramkg: Constructing knowledge graphs from program
                                                                    execution traces for debugging applications. In Proceed-
[20] Ansong Ni, Srini Iyer, Dragomir Radev, Ves Stoyanov,
                                                                    ings of the 45th International Conference on Software
     Wen-tau Yih, Sida I. Wang, and Xi Victoria Lin. Lever:
                                                                    Engineering (ICSE), pages 1832–1843, 2023.
     Learning to verify language-to-code generation with ex-
     ecution. In Proceedings of the 40th International Confer- [31] Yue Wang, Hung Le, Akhilesh Gotmare, Nghi Bui, Jun-
     ence on Machine Learning (ICML), pages 26106–26128,            nan Li, and Steven Hoi. Codet5+: Open code large lan-
     2023.                                                          guage models for code understanding and generation. In
                                                                    Proceedings of the 2023 Conference on Empirical Meth-
[21] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu,
                                                                    ods in Natural Language Processing (EMNLP), pages
     Huan Wang, Yingbo Zhou, Silvio Savarese, and Caim-
                                                                    1069–1088, 2023.
     ing Xiong. Codegen: An open large language model for
     code with multi-turn program synthesis. In Proceedings [32] Ronald J. Williams. Simple statistical gradient-following
     of the 11th International Conference on Learning Repre-        algorithms for connectionist reinforcement learning. Ma-
     sentations (ICLR), 2023. arXiv:2203.13474.                     chine Learning, 8(3-4):229–256, 1992.

                                                             34
                                  Journal of Emerging Applied Artificial Intelligence (JEAAI)


[33] Frank F. Xu, Uri Alon, Graham Neubig, and Vincent J.
     Hellendoorn. A systematic evaluation of large language
     models of code. In Proceedings of the 6th ACM SIG-
     PLAN International Symposium on Machine Program-
     ming (MAPS), pages 1–10, 2022. arXiv:2202.13169.

[34] John Yang, Carlos E. Jimenez, Alexander Wettig, Kil-
     ian Lieret, Shunyu Yao, Karthik R. Narasimhan, and Ofir
     Press. Swe-agent: Agent-computer interfaces enable au-
     tomated software engineering. In Proceedings of the 38th
     Conference on Neural Information Processing Systems
     (NeurIPS), 2024. arXiv:2405.15793.
[35] Fengji Zhang, Bei Chen, Yue Zhang, Jacky Keung,
     Jin Liu, Daoguang Zan, Yi Mao, Jian-Guang Lou, and
     Weizhu Chen. Repocoder: Repository-level code com-
     pletion through iterative retrieval and generation. In Pro-
     ceedings of the 2023 Conference on Empirical Methods
     in Natural Language Processing (EMNLP), pages 2471–
     2484, 2023.




                                                               35
