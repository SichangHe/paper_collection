                                                                                                                                                                       1




                                         AssumptionMiner: Extracting, Tracing, and Revising
                                           Implicit Assumptions in LLM Code Generation
                                                                                                  Jie JW Wu



                                            Abstract—Large language models (LLMs) generate                 into everyday practice [5], [6]. Yet real-world prompts are
                                         code from natural-language prompts, but real prompts              rarely complete specifications: they leave open questions
                                         are rarely complete specifications. When a prompt                 about input formats, boundary conditions, error-handling
                                         leaves input formats, error handling, or design decisions
                                         unstated, the model fills the gaps with implicit assump-          policies, domain constraints, and intended semantics [7],
                                         tions: choices absent from the prompt that nonetheless            [8].
                                         shape the code’s behavior, and often its correctness.                 This gap is structural, not incidental. Traditional soft-
                                         Because these assumptions are invisible, generated code           ware engineering moves from requirements to design to
                                         can pass its tests while violating the developer’s intent.        implementation through successive refinements, and each
                                            We present AssumptionMiner, a framework that
                                         makes such assumptions a first-class output of code               translation step is an opportunity to surface and resolve
                                         generation. Instead of producing code alone, Assump-              ambiguity. LLM-based code generation collapses these
                                         tionMiner also emits an explicit assumption layer: a              steps: natural language is converted directly into executable
                                         structured record of every inferred constraint and                code in a single opaque step. As Mary Shaw observes, “vibe
arXiv:2607.22898v1 [cs.SE] 24 Jul 2026




                                         design decision. Developers inspect, confirm, or revise           coding ignores the shifts from the language of the world
                                         assumptions through an interactive interface, and an
                                         AST-based dependency graph lets the system regenerate             to the language of the machine” [9]: the disambiguation
                                         only the code a revised assumption governs.                       work that those shifts used to force into the open does not
                                            We also contribute a benchmark of 180 ambiguous                disappear. The model performs it silently. When an LLM
                                         programming tasks with 676 annotated assumptions,                 fills a specification gap, it commits to implicit assumptions:
                                         including a human-verified curated subset for code-
                                                                                                           specific design choices that were never stated in the prompt
                                         localization evaluation. We evaluate extraction, code lo-
                                         calization, and revision support. With open-source mod-           and are never reported to the developer.
                                         els, a confidence-weighted ensemble attains F1 = 0.816 for            These implicit assumptions are a pervasive source of
                                         extraction, improving on the strongest offline baseline           misalignment. The generated code may pass unit tests
                                         by 3.6×. Under a stricter decision-level metric that also         while violating project conventions, security policies, or the
                                         requires each extracted description to name the same
                                                                                                           developer’s actual intent, a class of defect we term working-
                                         design decision as the reference, the best open-source
                                         configuration reaches only F1 = 0.66, far above the near-         but-wrong. In our benchmark of 180 LLM-generated code
                                         zero non-LLM baselines but low in absolute terms, indi-           artifacts, every task contained at least two latent implicit
                                         cating that decision-level assumption extraction remains          assumptions (mean: 3.8 per task, range: 2–5) identifiable
                                         far from solved. On the human-verified localization set,          only through inspection, motivating the need for automated
                                         AST-guided localization produces tighter code regions
                                                                                                           extraction.
                                         than keyword and whole-file baselines. When developers
                                         revise an assumption, targeted regeneration changes less              The core difficulty is that existing tools give developers
                                         code than non-targeted alternatives, although it also             no visibility into what the LLM assumed. Prompt engineer-
                                         exposes a need for stronger handling of cascading edits.          ing guides [10] advise more detailed prompts but cannot
                                         Together, these results show how making assumptions               enumerate what was left out. Stoica et al. observe that
                                         explicit can support more inspectable and controllable
                                                                                                           when a request is ambiguous, an LLM-based agent has
                                         LLM-based code generation. The benchmark, code, and
                                         replication package are available at https://doi.org/10           two simple ways to disambiguate: it can ask the user for
                                         .5281/zenodo.21535058.                                            clarification, or it can state the assumptions underlying
                                           Index Terms—Assumption mining, LLM code gen-                    its answer so that the user sees how to improve the
                                         eration, implicit assumptions, implicit requirements,             prompt [11]. The first strategy has grown into an active
                                         code adaptability, AST dependency graph, incremental              line of clarification-question research: ClarifyGPT detects
                                         code regeneration, requirements engineering, program              ambiguous requirements via code-consistency checks and
                                         analysis, software engineering benchmark                          asks targeted questions [12]; SpecValidator instead de-
                                                                                                           tects defective task descriptions (lexical vagueness, under-
                                                             I. Introduction
                                                                                                           specification, and malformed formatting) with a lightweight

                                         M       ODERN software development increasingly relies
                                                 on large language models (LLMs) to accelerate
                                         code generation [1], [2], [3], [4]. Developers write natural-
                                                                                                           fine-tuned classifier [13]; HumanEvalComm benchmarks
                                                                                                           whether code LLMs ask clarifying questions at all when
                                                                                                           requirements are inconsistent, ambiguous, or incomplete,
                                         language prompts and receive executable code within sec-          finding that they usually generate code instead [14], and
                                         onds, a workflow that has moved from research prototypes          such defective descriptions measurably degrade code-model
                                          Jie JW Wu is with Michigan Technological University, Houghton,   accuracy [15]; ClarifyCoder fine-tunes models to prefer
                                         MI, USA. E-mail: jie.jw.wu@mtu.edu. ORCID: 0000-0002-7895-2023.   asking over answering [16]; TiCoder interactively formalizes
                                                                                                                                      2



              Without AssumptionMiner                                                  With AssumptionMiner
             def authenticate(user, pwd):                             def authenticate(...):
                                                                                               [T2] A2: token = plain UUID
                   h = md5(pwd.encode())                  T6                 h = md5(pwd)
                                                                                               [T6] A1: MD5 → bcrypt (edited)
                 if h != user.hash: raise                                 if h != ...: ...
                  tok = str(uuid.uuid4())                 T2                tok = uuid4()      [T3] A3: retry limit = 3
                                                               AM
                   if fail_cnt > 3: raise                 T3               if cnt > 3: ...     [T4] A4: in-memory only
                    _sessions[uid] = tok                  T4              sessions[u] = tok         [T5] A5: O(n) linear scan
                 for _ in range(100): ...                 T5              for _ in ...: ...
                   return {"token": tok}                                     return tok
       5 implicit assumptions (colored), committed                                   Developer edits A1 (MD5 → bcrypt);
     silently, invisible to developer until code review                             AM regenerates only the affected region


Fig. 1. Implicit assumptions in LLM code generation, before and after AssumptionMiner. Left: An ambiguous prompt yields code with
five undisclosed assumptions (colored, tagged with taxonomy categories) about password storage (A1), session format (A2), failure policy
(A3), persistence (A4), and performance (A5), invisible until code review. Right: AssumptionMiner augments the same generation step to
jointly produce code and an explicit assumption layer (A1–A5). The developer confirms four assumptions and flips A1 (MD5 → bcrypt);
AssumptionMiner incrementally regenerates only the affected code region.



user intent by generating tests for the user to confirm [17];       LLM reasoning explicit and inspectable.
and self-planning approaches decompose prompts before (C3) Assumption–code dependency mechanism
generation [18]. These systems reduce ambiguity up-front,          (§III-D, §III-E): a two-pass AST-guided dependency
but their questions are hypothetical (what might matter)            graph (keyword-overlap candidate identification fol-
rather than diagnostic (what the model actually decided),           lowed by minimal-subtree AST narrowing), linking
their answers are not linked to specific code regions, and a        each assumption to the code regions it governs,
later change of decision still requires a full reprompt. The        enabling traceable and controllable incremental code
second strategy, making the model’s assumptions them-               updates when assumptions are flipped or revised.
selves explicit, has remained largely unexplored for code (C4) Interactive interface and software artifact (§IV,
generation, even though it imposes no up-front interaction          Appendix E): a developer-facing review interface and
cost on the developer. Self-repair methods [19], [20] iterate       an open-source implementation of the full pipeline.
on test failures but cannot repair silent assumptions that (C5) Benchmark and empirical evaluation (§V, §VI):
produce passing-but-wrong code.                                     180 programming tasks under ambiguous prompts,
   In this research, we operationalize the second strategy:         with 676 annotated assumptions (including a 30-task
we present AssumptionMiner, a framework that makes                  curated subset of novel tasks with 109 human-verified
implicit assumptions a first-class output of LLM code gen-          assumptions), evaluated across extraction quality,
eration. Rather than extracting assumptions after the fact,         dependency accuracy, and code adaptability.
AssumptionMiner augments the generation step itself: Paper organization. §II defines implicit assumptions and
the backbone LLM jointly produces executable code and motivates the problem with a running example. §III de-
an explicit assumption layer: a structured, formalized list scribes the AssumptionMiner architecture. §IV presents
of every inferred constraint and design decision embedded the developer interface. §V introduces the benchmark. §VI
in the generated code. Where clarification-question systems reports experimental results and discussion. §VII surveys
require the developer (or model) to know in advance what related work. §VIII discusses threats to validity. §IX con-
to ask, AssumptionMiner diagnoses which decisions the cludes. Appendices provide the full extraction prompt (§A),
LLM already made, surfacing them as revisable records complete per-category P/R/F1 tables (§B), benchmark
grounded in the actual generated code. Developers inspect, construction details (§C), the ensemble algorithm (§D),
confirm, or modify individual assumptions through an software-artifact details (§E), and reproducibility notes
interactive interface (§IV). When an assumption is flipped (§F). Our replication package (the benchmark, source code,
or revised, AssumptionMiner incrementally regenerates all evaluation scripts, and raw results) is publicly available
only the code regions governed by that assumption while at https://doi.org/10.5281/zenodo.21535058.
preserving all unaffected components.
Contributions. We make the following contributions in                     II. Motivation & Background
this research:                                                A. Formal Definition
(C1) Assumption taxonomy (§II-C): a six-category                Let p be a natural-language prompt (potentially ambigu-
       taxonomy of implicit assumptions in LLM-generated ous or underspecified) and c = G(p) be the code produced
       code, covering input validation, data format, error by an LLM G. We define an implicit assumption as follows.
       policy, persistence, performance, and security.
(C2) Implicit-assumption generation framework                  Definition 1 (Implicit Assumption). A implicit
      (§III): a novel approach that integrates assumption      assumption   a of (p, c) is a proposition that:
       surfacing directly into LLM-based code synthesis,        (i) is not stated in p (arising from ambiguity or
       producing code and a formalized assumption layer in           underspecification),
       a single augmented generation step, making implicit
                                                                                                                             3



  (ii) is instantiated in c (i.e., c behaves as if a holds),            B2 Uniqueness (T3): Exactly one valid pair is assumed.
       and                                                                  The first match is returned without checking for
 (iii) has at least one alternative instantiation that sat-                 additional solutions.
       isfies p but would produce a meaningfully different              B3 No-solution policy (T3): An empty list [] is re-
       c.a                                                                  turned when no pair sums to the target, not None,
     aWe operationalize “meaningfully different” as producing dis-          not a raised ValueError.
  tinct observable behavior on at least one input not excluded by p.    B4 Space–time trade-off (T5): An O(n)-space hash
  For example, using MD5 vs. bcrypt for password hashing yields             map is chosen over an O(n2 ) brute-force scan or an
  different outputs for any password string, satisfying this condition.
                                                                            O(n log n) sort-and-scan approach.
The set of implicit assumptions of (p, c) is denoted A(p, c).             Unlike the authentication example, these assumptions
In AssumptionMiner, A(p, c) is produced during genera- arise in seven lines of purely algorithmic code with no
tion as a formalized assumption layer co-output alongside external dependencies, confirming that implicit assump-
c. Each assumption ai ∈ A(p, c) is characterized by: tions are not confined to system-design tasks: they emerge
(i) its category κ(ai ) (see §II-C), (ii) a natural-language whenever a prompt leaves behavioral or design questions
description d(ai ), (iii) the code regions R(ai ) ⊆ c it governs, open, regardless of code complexity.
and (iv) a set of alternatives Alt(ai ) representing choices
the LLM could have made differently.
                                                                        C. Assumption Taxonomy
B. Running Example                                              We developed the taxonomy through an iterative, author-
  We use the following prompt as a running example           led open-coding process over 30 LLM-generated code
throughout the paper:                                        samples from the curated subset of the benchmark, as-
                                                             sisted by LLM-proposed candidate labels [21]. In each
  “Implement a user authentication system that checks        iteration, candidate assumptions and category labels were
  credentials and returns a session token.”                  first proposed automatically (GPT-4o), then reviewed,
                                                             corrected, and grouped into emergent themes by the author.
   A typical LLM-generated implementation embeds at
                                                             Category boundaries were refined between iterations. The
least five implicit assumptions, which AssumptionMiner
                                                             most contested boundary during this process was T1/T3:
labels A1 –A5 :
                                                             a guard clause is T1 (Input Validation) when it enforces a
A1 Password storage (T6): Passwords are hashed with caller precondition, but T3 (Error Policy) when the design
     MD5 (weak, SHA-256 or bcrypt preferred).                question is how the function signals failure, a distinction
A2 Session format (T2): Tokens are plain UUID v4 that matters for code reuse across call sites. The process
     strings, with no signing or expiry logic.               converged after three iterations. The same six categories
A3 Failure policy (T3): After three failed attempts a covered the tasks in the full benchmark without requiring
     bare exception is raised, with no structured error or additional categories. This supports their adequacy for the
     HTTP status code.                                       present dataset. It does not establish that the taxonomy is
A4 Persistence (T4): Sessions are held in an in-memory complete for other languages, repositories, or development
     Python dict, with no database or file persistence.      settings. To assess whether the six categories can be applied
A5 Performance (T5): A fixed-iteration loop performs reliably, two developers independently categorized all 111
     an O(n) linear scan, with no indexing or configurable assumptions of the curated subset and then reconciled
     work factor.                                            their disagreements to consensus (rater background and
   These five assumptions are silently embedded in fewer protocol in Appendix C). Agreement before reconciliation
than a dozen lines of generated code (see Figure 1). Without was strong (Cohen’s κ = 0.85, 88.3% raw agreement),
a tool like AssumptionMiner, the developer would need indicating that the taxonomy can be applied consistently
to audit the generated code manually to discover them. by a second developer rather than being idiosyncratic to
(Category labels T1–T6 refer to the assumption taxonomy its author (details in §VIII).
introduced in §II-C.)                                             a) Category characterization.: T1 (Input Valida-
     a) Second Example: An Algorithmic Function.: To tion) is the most frequent category (86% of tasks) and
demonstrate that implicit assumptions pervade even short captures assumptions about what the caller guarantees:
algorithmic code, consider a prompt typical of competitive that a list argument is non-empty, that a string is valid
programming or coding interviews:                            UTF-8, or that an integer falls within a documented range:
  “Given a list of integers and a target value, find two     silent preconditions whose violation causes runtime errors
  numbers that add up to the target.”                        rather than wrong results. T2 (Data Format) is nearly
                                                             as common (75% of tasks) because most functions must
   A hash-map solution generated by GPT-4o in seven lines decide how to represent their output (as an index or a
embeds four implicit assumptions invisible in the prompt: value, as a dict or a dataclass, as None or an empty list
B1 Return type (T2): The function returns a pair of on failure) without any prompt guidance. T3 (Error
     indices (e.g., [1, 3]), not the values themselves, a Policy) covers the choice of how failures are communicated:
     choice the prompt does not specify.                     raised exceptions vs. sentinel returns vs. silent defaults.
                                                                                                                                        4



                           TABLE I
 Taxonomy of implicit assumptions in LLM-generated code.                            p         C1       p      C2    (p, c)     C3
  The last column is the percentage of the 180 tasks that              Developer            Prompt         Code Gen        Assumption
  contain at least one instance of the category. Because a                                 Ingestion        (LLM)           Extractor
task usually spans several categories, this column does not
sum to 100% and is distinct from the per-assumption shares in                                                                   A
                           Table II.

ID   Category           Description                      % of tasks                         a′i

T1   Input Validation   Input format, encoding,                86%
                        boundary checks, type
                        coercion
                                                                                            C5      R(·)     C4        A   Assumption
T2   Data Format        Return type, output struc-             75%                      Incremental      Dependency          Records
                        ture, serialization, nullabil-                                  Regenerator       Mapper
                        ity
T3   Error Policy       Exception types, return sen-           81%                 c′
                        tinels, error propagation
T4   Persistence        Storage backend, schema,                4%
                        consistency guarantees                        Fig. 2. AssumptionMiner system architecture. Boxes denote com-
T5   Performance        Algorithm        complexity,           76%    ponents. Arrows denote data flow. The dashed region marks the
                        caching, data structure                       developer interaction loop.
                        choices
T6   Security           Auth, cryptography, rate                3%
                        limiting, access control                      C2: Code Generator. Issues p to the backbone LLM
                                                                        and produces the initial code artifact c. Any instruction-
                                                                        tuned LLM (GPT-4o, Qwen2.5-Coder-7B, or similar)
A function returning False on bad input versus raising                  may serve as the backbone.
ValueError are semantically equivalent in isolation but               C3: Assumption Extractor. Given (p, c), applies a
diverge sharply under a caller that inspects the return                 structured extraction prompt (§III-B) to enumerate
type. T4 (Persistence) applies when a function writes                   A(p, c) as a list of AssumptionRecord objects (§III-C).
or reads state: the choice between an in-memory dict and              C4: Dependency Mapper. Links each assumption to
a database, or between append and overwrite, is invisible               the code regions it governs via a lightweight AST-level
in the function signature but consequential for any multi-              analysis (§III-D).
session caller. T5 (Performance) reflects algorithm or                C5: Incremental Regenerator. When the developer re-
data-structure trade-offs (hash map vs. sort-and-scan, eager            vises an assumption ai , regenerates only the code regions
vs. lazy evaluation) that determine asymptotic complexity               R(ai ) while preserving all other regions (§III-E).
without appearing in the function signature. T6 (Security)              Algorithm 1 summarizes the end-to-end procedure.
is the least frequent (3%) but highest-stakes category: a             Components C3–C5 correspond to its three phases. The
password stored as an MD5 hash passes all functional tests            remainder of this section details each in turn.
yet violates every modern security policy.
     b) Distribution pattern.: Input validation, error policy,
performance, and data format each appear in roughly B. Assumption Extraction
three-quarters or more of tasks, because most non-trivial         The core of AssumptionMiner is a two-phase extrac-
functions must decide how to treat their inputs, signal tion prompt (listing 1). Phase 1 asks the LLM to reason
failure, structure output, and trade off performance. T4 about what choices were made in c that go beyond what p
(Persistence, 4%) and T6 (Security, 3%) are rare because requires, a chain-of-thought [22] reasoning step. Phase 2
persistence- and security-sensitive tasks are underrepre- asks the model to format its discoveries into the structured
sented in general coding prompts. Their low frequency AssumptionRecord schema, enabling downstream program-
should not be interpreted as low importance: a single matic processing. The full prompt text is given in section A.
T6 assumption (e.g., weak cryptography) can invalidate
an entire system. This skew motivates our per-category C. AssumptionRecord Schema
breakdown in Table IV: aggregate F1 alone would mask
                                                                  Each extracted assumption is stored as an Assump-
systematic failures on low-frequency but critical categories.
                                                               tionRecord (listing 2). The schema is designed for both
                                                               human readability and programmatic processing by C4
       III. The AssumptionMiner Framework                      (dependency mapping) and C5 (incremental regeneration).
A. Architecture Overview
   AssumptionMiner consists of five loosely-coupled com- D. Assumption-Code Dependency Mapping
ponents connected by a structured data model (Figure 2).          To support targeted incremental regeneration, Assump-
C1: Prompt Ingestion. Receives           the     developer’s tionMiner must link each assumption to the code regions
   natural-language prompt p, optionally enriched with it governs. This is non-trivial: a single assumption (e.g.,
   project-level context (language, framework, coding style password hashing algorithm) may manifest across multiple
   guide).                                                     non-contiguous lines and functions.
                                                                                                                                   5



Algorithm 1 AssumptionMiner: assumption extraction, SYSTEM : You are an expert software engineer
dependency mapping, and incremental regeneration.               auditing LLM - generated
Require: prompt p, generated code c; category-to-node- code for implicit design decisions .
    type map M; narrowing threshold θ; context width USER :
    k                                                      ### Original Prompt
Ensure: assumption records A with linked code regions; { PROMPT }
    revised code on edit                                   ### Generated Code
 1: {Phase 1: Assumption extraction (§III-B)}             { CODE }
 2: r ← Llm(ExtractPrompt(p, c)) {single two-phase
                                                           ### Task
    prompt, temperature 0}                                 1. REASON : List every design decision in the code
 3: A ← ParseRecords(r) {each a: description, category            that is NOT
    ∈ T1–T6, severity, alternatives}                           required by the prompt . For each , name a
                                                                      realistic alternative .
 4: {Phase 2: Dependency mapping (§III-D)}                 2. FORMAT : Return a JSON array of
 5: (T , N ) ← TreeSitterParse(c) {N [t]: AST nodes of          A s s u m p t i o n R ec o r d objects .
    type t}                                                    Schema : { schema }
                                                               Return ONLY valid JSON after the tag [ RECORDS
 6: for all a ∈ A do                                                  ].
 7:   K ← Keywords(a); R ← ∅
 8:   for all node type t ∈ M[a.category] and node n ∈ [ RECORDS ]
      N [t] do                                            Listing 1. Assumption extraction prompt template (abbreviated).
 9:      if some κ ∈ K occurs in Text(n) then             {PROMPT} and {CODE} are replaced at runtime.
10:         if Span(n) ≤ θ then
11:            (s, e) ← (n.start, n.end)
12:         else
13:            (s, e) ← NarrowToKeywordLines(n, K) {
              {fall back to full span if no keyword line}    " id ":                     " string " ,               // e . g . " A1 "
                                                             " category ":               " T1 | T2 | T3 | T4 | T5 | T6 " ,
14:         end if                                           " description ": " string " ,                        // natural -
15:         R ← R ∪ {CodeRef(s, e, t)}                              language statement
16:      end if                                              " rationale ":              " string " ,             // why LLM made
                                                                    this choice
17:   end for                                                " alternatives ": [" string "] ,                     // >= 1
18:   a.code_refs ← R                                               alternatives
19: end for                                                  " code_refs ": [{                                    // dependency
                                                                    info ( C4 populates )
20: {Phase 3: Incremental regeneration when the user            " file ":                  " string " ,
    revises a ∈ A to a new description d′ (§III-E)}             " start_line ": " int " ,
21: for all ρ ∈ SortByStartDesc(a.code_refs) do                 " end_line ":              " int " ,
                                                                " ast_node ":              " string "             // optional AST
22:   x ← ContextWindow(c, ρ, k) {±k lines around                       node type
      region ρ}                                              }] ,
23:   y ← Llm(RegenPrompt(a.description, d′ , x))            " confidence ": " float " ,                          // [0 , 1]
                                                                    extraction confidence
24:   c ← Splice(c, ρ, ExtractCode(y), k) {reverse or-       " severity ":             " low | medium | high " // LLM -
      der keeps line offsets valid}                                 assigned ; human may override
25: end for                                               }
26: return A and, on revision, the updated code c         Listing 2. AssumptionRecord JSON schema.



   We construct an Assumption-Code Dependency Graph
G = (Va ∪ Vc , E) (Figure 3), where Va is the set of assump-
tions, Vc is the set of AST nodes in c, and (ai , nj ) ∈ E              any keyword from the assumption’s description or
if assumption ai governs node nj . Edge weights reflect                 alternatives appears as a substring in the node’s
confidence.                                                             identifier tokens. Optionally, an LLM call can replace
                                                                        keyword scoring with semantic region descriptions
   Edge construction proceeds in two passes:
                                                                        (use_llm=True). We evaluate this variant in §VI-D:
 1) Keyword-overlap pass. We extract content                            a strong open-source mapper improves accuracy over
    words from the assumption’s description and                         the heuristic at additional inference cost.
    alternatives fields and tokenize the code identifiers.           2) AST refinement pass. We parse c with the
    AST nodes of the category-appropriate types                         tree-sitter library and perform a bottom-up traver-
    (e.g.,   T3:     except_clause,     with_statement,                 sal from each candidate leaf node, stopping at the
    call; T5: assignment, for_statement; T6:                            deepest ancestor that encloses all candidate nodes for
    import_statement, call) are matched against                         that assumption. This yields the minimal enclosing
    node identifier text. A candidate is retained when                  sub-tree.
                                                                                                                                                    6



                                                                                              TABLE II
  Assumptions                         AST Nodes                     Benchmark composition. The 180 tasks split into the 30-task
                                                                      curated subset, which carries human-verified code-region
                      0.92                                           references (used for RQ2), and the 150-task extended tier
                                                                        drawn from HumanEval/MBPP. All headline results
   T6     A1                       def hash_password()
                                                                             (Tables III and IV, RQ3) use all 180 tasks.

                                                                    Metric                      Curated subset    Extended tier             All (180)
                       0.88                                         Tasks                                    30               150                  180
   T2     A2                          token = uuid4()               Total assumptions
                                                                    Mean assumptions / task
                                                                                                            109
                                                                                                            3.6
                                                                                                                              567
                                                                                                                              3.8
                                                                                                                                                   676
                                                                                                                                                   3.8
                                                                    Mean lines of code / task              11.0              10.6                 10.7
                                                                    Category breakdown: count and % of each tier’s assumptions (columns sum to 100%)
                       0.85                                         T1 Input Validation
                                                                    T2 Data Format
                                                                                                       20 (18%)
                                                                                                       31 (28%)
                                                                                                                        183 (32%)
                                                                                                                        112 (20%)
                                                                                                                                             203 (30%)
                                                                                                                                             143 (21%)
   T3     A3                            return False                T3 Error Policy                    24 (22%)         142 (25%)            166 (25%)
                                                                    T4 Persistence                       8 (7%)             0 (0%)              8 (1%)
                        0.71                                        T5 Performance                     21 (19%)         130 (23%)            151 (22%)
                                                                    T6 Security                          5 (5%)             0 (0%)              5 (1%)
                       0.79
   T4     A4                           sessions = {}
                                                                              V. The AssumptionMiner Benchmark

   T5     A5                        def authenticate()                 To enable systematic, reproducible evaluation of assump-
                       0.83                                         tion mining methods, we construct the AssumptionMiner
                                                                    benchmark (Table II).
Fig. 3. Assumption-code dependency graph for the running example.      Task collection. The benchmark consists of 180
Left: assumption nodes A1 –A5 (colored by category). Right: AST
nodes in the generated code. Edge weight = dependency confi-
                                                                    programming tasks under ambiguous or underspecified
dence. The graph is many-to-many: A2 governs two nodes, and         prompts. Thirty tasks are novel, spanning diverse do-
authenticate() is governed by both A2 and A5 .                      mains (data structures, algorithms, file I/O, networking,
                                                                    system utilities), stress-testing the underrepresented T4–
                                                                    Persistence and T6–Security categories, and selected to
E. Incremental Regeneration
                                                                    be out-of-distribution with respect to HumanEval [1] and
  When a developer revises assumption ai to a new                   MBPP [2], which supply the remaining 150 tasks.
value a′i , AssumptionMiner identifies R(ai ) = {n ∈                   Annotation. All 180 tasks use GPT-4o [24] to ex-
Vc : (ai , n) ∈ E} and constructs a targeted regeneration           tract the reference assumption list with the same struc-
prompt containing only the affected sub-tree, the revised           tured prompt as the extractor (§III-B), followed by
assumption, and the surrounding context (at most k lines            programmatic validation (schema conformance, category-
above/below each region, k = 5 in our experiments). The             vocabulary checks, and deduplication). The 30 novel tasks
remainder of c is left unchanged. This approach is analogous        form the curated subset: their prompts were designed
to in-place surgical editing [23], but guided by explicit           specifically for this benchmark, and they additionally carry
assumption metadata rather than test-failure signals.               code-region references (line ranges) used for RQ2. Since
                                                                    the reference annotations are LLM-derived, two developers,
              IV. Interactive Interface
                                                                    each with at least five years of professional software-
  The AssumptionMiner interface (Figure 4) is a web-                development experience in industry, independently verified
based IDE panel implemented in React that augments a                the curated subset (111 assumptions), spending roughly
standard code editor. Developers interact through three             four hours each, and reconciled to consensus: they agreed
primary actions:                                                    that 110 of 111 are valid implicit assumptions (99.1% raw
Inspect. Each AssumptionRecord is a severity-colored                agreement, κ = 0.66) and agreed on category at κ = 0.85
  card (red/amber/green). Hovering highlights its code              (§VIII, Appendix C). Adjudication then removed two
  region in the editor.                                             invalid entries and corrected eight category labels, yielding
Edit. Developers modify the description or pick an alter-           the 109 human-verified assumptions used throughout the
  native. Changes are staged, not yet applied.                      paper. Because GPT-4o produced the reference annotations,
Regenerate. Pressing Regenerate triggers C5 for all                 results for the GPT-4o backbone carry a self-consistency
  staged edits, topologically ordered over the dependency           risk, marked † in Table III. The open-source backbones
  graph.                                                            (Qwen32B, DeepSeek) share no weights or provider with
  Implementation. AssumptionMiner is implemented                    the annotation model, though their scores still measure
as an open-source Python package (assumption_miner),                agreement with the reference. All tasks share the six-
one module per component (C1–C5), with the interface                category schema (Table I).
served as a web application and a unit-test suite of 119 tests.        Benchmark statistics are summarized in Table II. Full
Appendix E details the module layout, experiment entry              benchmark construction details, including prompt selection
points, and extensibility. The package and all experiment           criteria and the annotation resolution process, are provided
scripts are part of the released artifact.                          in section C.
                                                                                                                                           7




                                                  AssumptionMiner: Interactive Interface
                                                                                          Assumption Records
                    Prompt
    “Implement user authentication: check                   A1: Security (high)
    credentials, hash password, return                T6
                                                            Password hashed with MD5. Weak by current standards; bcrypt
    session token.”                                         or argon2id strongly recommended.
                                                             Accept          Edit          Reject


               Generated Code
    def authenticate(user, pwd):                      T4    A4: Persistence (medium)
      h = md5(pwd.encode())
                                                            Sessions stored in in-memory dict; lost on restart. Edited: switched
                                                            to Redis (TTL = 1 h).
      if h != user.hash: raise
      _sessions[uid] = tok                                  Regenerating affected region. . .
      if fail_cnt > 3: raise
      return {"token": str(tok)}
                                                      T3    A3: Error Policy (low)
                                                            Three consecutive failures raise an exception; no back-off or
                                                            account lockout defined.
                                                             Accept          Edit          Reject

     Accept All               |   Regenerate Selected (1)                                                                1 of 3 reviewed

Fig. 4. AssumptionMiner interactive interface. (1) Highlighted code regions correspond to extracted assumptions. (2) The assumption panel
lets developers inspect and edit each assumption record. (3) The revision panel applies changes through incremental regeneration.



   In the curated subset, 67% of code-region references are                (§VI-B, scripts/run_rq1_semantic.py). We deliberately
single-line (mean span: 2.0 lines), suggesting assumptions                 avoid an LLM judge, which would reintroduce the very
typically manifest at specific statements. This motivates                  LLM-grades-LLM circularity we control for elsewhere. For
our IoU threshold of 0.5 for RQ2. All T4 (Persistence) and                 RQ2 dependency links, we use line-level IoU: IoU(R̂, R∗ ) =
T6 (Security) assumptions in the benchmark occur in the                    |R̂ ∩ R∗ | / |R̂ ∪ R∗ |; a link is correct when IoU ≥ 0.5. This
curated subset: the 150 HumanEval/MBPP tasks of the                        threshold is motivated by the reference annotation spans,
extended tier contain none, so the novel tasks provide the                 which are predominantly 1–3 lines. IoU≥0.5 requires the
benchmark’s only coverage of these two rare but high-stakes                predicted region to overlap with at least half the annotated
categories. (Note the two frequency views: Table I reports                 span.
the share of tasks containing ≥ 1 instance of a category
over all 180 tasks, whereas the breakdown above reports                                             VI. Evaluation
each category’s share of the assumptions in each tier.)
   Metrics. We define three extraction metrics over A(p, c)                    We evaluate AssumptionMiner through three research
and a reference set A∗ (p, c):                                              questions. RQ1 assesses whether the system recovers im-
                                                                            plicit decisions from generated code. RQ2 assesses whether
AR (Assumption Recall): |A ∩ A∗ | / |A∗ |
                                                                            it localizes those decisions to the relevant implementation
AP (Assumption Precision): |A ∩ A∗ | / |A|
                                                                            region, and RQ3 assesses whether those links support more
AF1 (Assumption F1 ): Harmonic mean of AR and AP
                                                                            focused revisions. This sequence separates the three claims
   Matching. We report extraction quality under two                         required by the approach: identifying a decision, tracing it
matching rules of increasing strictness. Category-level                     to code, and using the trace during change.
(lenient) matching counts a predicted assumption as correct
when its category equals that of an unused reference
assumption for the same task, with multiplicity (if the                     A. Experimental Setup
extractor proposes two T3 assumptions and the reference                       Backbone LLMs. We evaluate AssumptionMiner
contains one, only one is a true positive). It answers “did                 with four backbone LLMs: GPT-4o [24] (OpenAI API,
the extractor notice a decision of this kind?” and is the                   model alias gpt-4o), Qwen2.5-Coder-32B-Instruct (here-
basis of AR, AP, and AF1 . Being category-only, it is                       after Qwen32B), DeepSeek-Coder-V2-Lite-Instruct (here-
deliberately lenient and comparable to how prior work                       after DeepSeek), and Qwen2.5-Coder-7B-Instruct (here-
scores taxonomy coverage. Decision-level (strict) matching                  after Qwen-7B). The latter three are served locally via
additionally requires the predicted description to refer                    vLLM [25] on a single NVIDIA RTX PRO 6000 Blackwell
to the same decision as the reference: a match holds                        workstation GPU (96 GB of VRAM). All are evaluated on
only when categories agree and the description similarity                   the full n = 180 benchmark tasks. We additionally report
sim(d(a), d(a∗ )) ≥ τ . It answers the harder question “did                 a Conf-Weighted (CW) ensemble combining Qwen2.5-
the extractor identify the actual decision?” We compute sim                 Coder-32B (high-recall backbone) and DeepSeek-Coder-V2-
as the cosine similarity of sentence embeddings (a determin-                Lite (high-precision backbone), averaging per-assumption
istic, reproducible measure) and calibrate τ against human                  confidence scores and thresholding at 0.5. Results for all
same-decision judgments on a sample of matched pairs                        backbones are reported in Table III.
                                                                                                                                                 8



  Baselines.                                                                            TABLE III
                                                               RQ1 assumption-extraction quality on the full benchmark
   • Comment Extraction (CE): Extracts design decisions
                                                              (n = 180, 676 assumptions). Best per column in bold. † GPT-4o
     from code comments and docstrings only, and requires        is both annotator and evaluator here (it produced all
     no LLM call.                                               reference annotations), so its scores may be inflated by
                                                                 self-consistency. The open-source backbones are fully
   • Knowledge-Based Pattern Extraction (KBE): Mines
                                                              cross-model. CW = Conf-Weighted cross-model ensemble. The
     Python AST structure and code idioms (return sen-                   strict AF1 column is explained in §VI-B.
     tinels, exception breadth, hash-map use) against a
                                                              Method                                          AR       AP      AF1     AF1 (strict)
     hand-built rule base to infer implicit design choices,
                                                              Offline baselines (no LLM, n = 180)
     and runs entirely offline without an LLM.                Comment Extraction (CE)                       0.176    0.312    0.225          0.079
                                                              Pattern Extraction (KBE)                      0.044    0.476    0.081          0.019
  We also considered three additional chain-of-               AssumptionMiner (ours, n = 180)
thought/prompting baselines during development:               AssumptionMiner (GPT-4o)†
                                                              AssumptionMiner (Qwen2.5-Coder-32B)
                                                                                                            0.905
                                                                                                             0.753
                                                                                                                      0.864
                                                                                                                      0.797
                                                                                                                              0.884
                                                                                                                               0.774
                                                                                                                                             0.806
                                                                                                                                              0.654
Direct Generation (DG), which asks the LLM to list            AssumptionMiner (DeepSeek-Coder-V2-Lite)       0.732   0.814     0.771          0.565
                                                              AssumptionMiner (Qwen2.5-Coder-7B)             0.468    0.810    0.593          0.463
assumptions without the structured two-phase prompt;          Ensemble (ours, n = 180, cross-model)
Clarifying Questions (CQ), which prompts the LLM              AssumptionMiner Ens. (Qwen32B+DeepSeek, CW)   0.823    0.810    0.816          0.662

to generate questions it would ask before coding; and         Bootstrap 95% CI over per-task F1 (10,000 resamples of the 180
                                                              tasks): GPT-4o† [0.866, 0.910], Qwen32B [0.745, 0.794], DeepSeek
Chain-of-Thought (CoT) prompting [22], which elicits          [0.737, 0.785], Qwen-7B [0.553, 0.608].
reasoning before extraction. In preliminary experiments
on the 30 curated-subset tasks, DG reached F1 = 0.41 (vs.
0.59 for the two-phase prompt), CQ reached F1 = 0.37 (it   model, as the primary cross-model evidence, and report
generates hypothetical questions rather than identifying   the GPT-4o result separately (marked †).
actual code choices), and CoT reached F1 = 0.56. None         Table III presents the aggregate comparison. It estab-
exceeded the structured two-phase prompt in either         lishes the overall extraction result before Table IV examines
precision or recall. We therefore use the structured promptwhere the methods succeed or fail across assumption
as the single AssumptionMiner extraction method and        categories.
report only CE and KBE as offline baselines in the main       The aggregate values do not reveal whether performance
tables.                                                    is concentrated in common, easy-to-observe decisions. We
  Dependency baselines (RQ2):                              therefore break F1 down by taxonomy category in Table IV.
   • Keyword Heuristic (KH): Token-overlap between as-     The complete precision and recall values are deferred to
     sumption description and code tokens, with no AST     Appendix B.
     information.                                             Findings (n = 180). The offline baselines provide
   • Full-File Dependency (FF): Trivially assigns every
                                                           little coverage because the decisions of interest are seldom
     assumption to the entire file (upper bound on recall, written in comments or directly encoded by a fixed pattern.
     lower bound on precision).                            CE reaches F1 = 0.225, largely through documented return
  Regeneration baselines (RQ3):                            formats (T2), whereas KBE reaches F1 = 0.081 because
   • Full Regeneration (FR): Re-generates the entire func- its recall is only 0.044.
     tion from scratch with the revised assumption in the     The strongest open-source result is the CW ensemble
     prompt.                                               (F1 = 0.816). Qwen32B and DeepSeek are nearly tied
   • In-Place LLM Edit (IPE): Passes the full code +       overall (F1 = 0.774 and 0.771), but make complementary
     revision instruction to the LLM and asks it to apply  errors: Qwen32B recovers more assumptions and DeepSeek
     the change [23].                                      is slightly more precise. Their overlapping bootstrap in-
   • Manual Reprompt (MR): Developer manually rewrites     tervals (Table III) indicate that this small difference is
     the prompt. LLM generates fresh code.                 not meaningful. GPT-4o obtains the highest score, but we
                                                           treat it as secondary evidence because it also produced the
B. RQ1: Extraction Quality                                 reference annotations.
   RQ1 asks whether AssumptionMiner can recover the           The per-category F1 results (Table IV) identify an
implicit assumptions that a developer would otherwise important boundary of the benchmark. Data-format and
need to infer through code review. We evaluate extraction performance decisions are comparatively easy to recover,
against the benchmark reference annotations on all 180 whereas the rare persistence and security decisions are
tasks. We first compare methods using category-level harder. All T4 and T6 instances occur in the curated
precision, recall, and F1 . This measures whether a method tasks, showing why conventional HumanEval/MBPP-style
identifies a decision of the appropriate kind. We then prompts are insufficient for assessing these categories.
examine performance by category and report a stricter         Lenient vs. strict matching. The scores above
decision-level match to distinguish category coverage from use lenient category-level matching. Under the strict
description fidelity. Because GPT-4o created the initial decision-level metric, which additionally requires the
reference annotations, we treat the open-source backbones predicted description to refer to the same decision as
(Qwen32B, DeepSeek, Qwen-7B, and their CW ensemble), the reference (§VI-A), scores fall substantially. We mea-
which share no weights or provider with the annotation sure description similarity by sentence-embedding cosine
                                                                                                                                                9



                                                      TABLE IV
RQ1 per-category AF1 (n = 180). Best cross-model F1 per category in bold (GPT-4o† produced the reference annotations).
                 CE F1 = 0.363 on T2 (return-type docstrings) but near-zero on all other categories.


Method                                                     T1          T2           T3            T4             T5            T6            All
Comment Extraction (CE)                                  0.171      0.363        0.058          0.000        0.116         0.000            0.225
AssumptionMiner (GPT-4o)†                                0.905      0.882        0.869          0.615        0.902         0.500            0.884
AssumptionMiner (Qwen2.5-Coder-32B)                      0.709      0.795       0.771          0.667        0.851          0.500            0.774
AssumptionMiner (DeepSeek-Coder-V2-Lite)                0.799       0.796        0.725          0.588        0.781        0.533             0.771


(all-MiniLM-L6-v2) and calibrate the match threshold             specific. Our primary analysis uses the 109 human-verified
against human judgment: an author labeled 30 candidate           code-region references in the curated subset. We also
(predicted, reference) pairs sampled across the similarity       report a secondary analysis on all 676 references. Its
range as same-decision or not (three boundary cases              additional 567 references are auto-labeled, so those results
adjudicated jointly), and τ = 0.56 best separates the labels     measure agreement with the generated reference rather
(24/30 = 80% agreement, any τ between 0.55 and 0.58              than accuracy against ground truth. We report both
performs identically). At τ = 0.56, the strict decision-level    threshold accuracy (IoU≥ 0.5) and mean IoU to distinguish
scores are GPT-4o† F1 = 0.806 (P = 0.788, R = 0.825),            selecting the right area from selecting a tight span.
Qwen2.5-Coder-32B F1 = 0.654, DeepSeek-Coder-V2-Lite
F1 = 0.565, and Qwen2.5-Coder-7B F1 = 0.463 (the                                          TABLE V
                                                                   RQ2: Dependency accuracy (Acc. = IoU≥0.5; IoU = mean;
strict column of Table III), each well below its lenient         Exact = exact-match rate; Calls = LLM calls per assumption).
counterpart, and consistent with the purely lexical lower        nC = 109 curated-subset references (primary); nF = 676 full
bound (F1 ≈ 0.60 for Qwen2.5-Coder-32B), which penalizes             set (adds 567 auto-labeled references; secondary).
                                                                 AM-LLM = AssumptionMiner with use_llm=True and the given
paraphrases that the embedding metric credits. The CW             mapper model (§VI-D). Both mappers are evaluated on the
ensemble attains the highest strict AF1 of any cross-model             curated and full sets. Best per column in bold.
configuration (F1 = 0.662), mirroring its lenient lead and
                                                                                                   Curated (nC )            Full (nF )
confirming that merging a high-recall and a high-precision
                                                                 Method                          Acc     IoU     Exact     Acc      IoU      Calls
backbone helps under the stricter criterion as well. The
                                                                 Keyword Heuristic (KH)         0.606    0.545    0.431    0.284    0.288       0
offline baselines, by contrast, collapse to near-zero (CE        Full-File (FF)                 0.064    0.196    0.018    0.368    0.397       0
                                                                 AssumptionMiner (heuristic)    0.569    0.581   0.505     0.376    0.376       0
F1 = 0.079, KBE F1 = 0.019): the few assumptions                 AM-LLM (GPT-4o)                0.560    0.596    0.431    0.475   0.480        1
they surface almost never name the same decision as the          AM-LLM (Qwen2.5-Coder-32B)    0.642    0.653    0.505    0.479     0.464       1

reference. To score the baselines and the ensemble strictly
(neither emits per-assumption descriptions natively), we   Findings. The curated subset is the primary result
reconstruct one description per prediction from its ex-  because its references were human-verified. On this set,
tracted span (scripts/build_strict_inputs.py), which     AssumptionMiner and keyword matching have similar
reproduces each method’s lenient prediction count exactlythreshold accuracy (56.9% and 60.6%), but AST narrowing
(CE 381, KBE 63, and ensemble 689 predictions, the last  yields the tightest regions (mean IoU 0.581, versus 0.545
giving lenient F1 = 0.816). The gap is not a weakness of for keyword matching). The whole-file baseline performs
AssumptionMiner’s framework but a property of the        poorly because these references usually identify a small
benchmark: identifying which implicit decision was made, part of the implementation. Table VI ablates the mapper’s
                                                         category-to-node-type map (§III-D): Full is the shipped
not merely that a decision of some category exists, remains
                                                         map, and Original is the map before development-time
difficult for current models, so the benchmark is far from
                                                         tuning added the T3 call, T3 with_statement, and
saturated and retains headroom to measure future progress.
RQ1 answer. Open-source models recover implicit as-      T5 import_from_statement types (its “expansions”), to-
sumptions substantially better than the offline comment- gether worth +2.7pp. Removing the base T5 assignment
and pattern-based baselines. The cross-model CW ensemble type, present in both maps, costs the same 2.7pp on its own.
reaches F1 = 0.816, compared with 0.225 for the strongestAssignments (e.g., cache = {}) are where data-structure
offline baseline. Exact decision matching remains more   choices surface, so they are important for localizing perfor-
                                                         mance decisions.
difficult than category-level matching, especially for the
rare security and persistence categories.                  The full-set result should be interpreted differently. It
                                                         includes 567 auto-labeled references for very short functions,
                                                         where marking the entire function is often sufficient. In that
C. RQ2: Dependency Accuracy                              setting AssumptionMiner improves on keyword matching
  RQ2 asks whether the dependency mapper identifies but is close to the whole-file baseline. We therefore use the
the code region that implements a recovered assumption. curated-subset result to support claims about localization
This question matters because localized regeneration is precision and report the full set as a secondary robustness
meaningful only when the selected region is sufficiently check.
                                                                                                                         10



                        TABLE VI                              call per assumption. Both LLM mappers lead on the
RQ2 ablation: dependency mapper accuracy when removing        secondary full set (Table V, nF columns): Qwen32B reaches
 one node type at a time from the full configuration (30
         curated-subset tasks, 109 assumptions).              47.9% accuracy (IoU 0.464) and GPT-4o 47.5% (IoU 0.480),
                                                              versus 37.6% for the heuristic and 36.8% for whole-file
Configuration                             Acc. ∆ Acc. localization. Whereas the heuristic barely separates from
                                                              whole-file localization on these short auto-labeled functions,
Full (all expansions)                    0.569           n/a both LLM mappers keep a clear margin, so on the full set
   −T3 call                              0.560      −0.9pp the mapper choice matters less than whether an LLM
   −T3 with_statement                    0.560      −0.9pp mapper is used at all. We keep the AST heuristic as
   −T5 import_from_statement             0.569         0.0pp AssumptionMiner’s default for its zero inference cost
   −T5 assignment                        0.541      −2.7pp and competitive accuracy, and expose the LLM-guided
Original (no expansions)                 0.541      −2.7pp mapper via the use_llm flag for accuracy-critical settings.
                                                              (An earlier version of this comparison, which scored noisy
                                                              predicted extractor descriptions against the pre-correction
   We also asked whether the dependency map’s accuracy
                                                              references, favored the heuristic, 45.5% vs. 30.9–31.8%.
carries through to code adaptability: whether tasks with
                                                              That reference set has since been superseded by the human-
more accurate maps also receive smaller edits in RQ3.
                                                              verified consensus, so we report the numbers above as
On the human-verified references this correlation is weak:
                                                              primary.)
splitting the 30 tasks by AssumptionMiner link accuracy
(IoU≥0.5) into high (n = 23) and low (n = 7) groups, E. RQ3: Code Adaptability
mean edit distance rises only from 0.258 to 0.281 (1.09×),
and In-Place LLM Edit shows a similar spread (0.264              RQ3 asks whether assumption-guided regeneration re-
vs. 0.323). We therefore do not claim a strong mapping-       duces   the scope of a code change when a developer revises
accuracy-to-edit-size effect. The value of the dependency     one  decision. We use the full 180-task benchmark with GPT-
map is in enabling targeted regeneration at all (RQ3), not    4o  and  repeat the AssumptionMiner configuration on the
in a monotonic accuracy-edit relationship. §VI-D shows an     30  novel  tasks with Qwen32B. Assumptions are extracted
LLM-guided mapper with a strong open-source mapper            with   C3  (§III-B).  No manual dependency annotation is
can improve over this heuristic on the curated subset (the    required   because  syntactic  validity and edit distance are
AM-LLM rows of Table V), at the cost of one additional        measured    on  the regenerated   output.
                                                                 Assumption modification procedure. For each task
inference call per assumption.
                                                              we select the highest-severity AssumptionRecord and
RQ2 answer. On human-verified references, AST narrow-
                                                              rewrite its description to the first entry in its alternatives
ing produces tighter localizations than keyword matching,
                                                              field, producing a (code, original-assumption, revised-
although their threshold accuracies are similar. An optional
                                                              assumption) triple. The revised record is passed to the
LLM-guided mapper improves accuracy to 64.2% at the
                                                              regenerator (§III-E) together with the affected code sub-
cost of an additional inference call. Whole-file localization
                                                              tree and k = 5 context lines. Only the regions governed
is competitive only on the secondary set of very short,
                                                              by the selected assumption are updated. This operational-
auto-labeled functions.
                                                              ization ensures the revision is semantically meaningful (a
                                                              real alternative that the LLM could have chosen) and
D. Mapper Ablation: Use-LLM vs. Heuristic                     reproducible (deterministic given the AssumptionRecord).
   We ablate whether replacing keyword-overlap scoring           Worked example. For the authentication task of the
with an LLM-guided localization step (use_llm=True, running example, the selected record is A1 (T6): “Passwords
§III-D) improves dependency accuracy. We evaluate five are hashed with MD5, a cryptographically broken algorithm”,
mapper configurations on the 109 human-verified assump- whose first alternative is “bcrypt.” The regenerator receives
tions of the curated subset, scored against the consensus the revised record, the dependency-mapped sub-tree (the
reference regions: AssumptionMiner (heuristic), AM- hash_password function body), and five context lines. It
LLM (Qwen32B), AM-LLM (GPT-4o), KH, and FF. All rewrites the hashing call and its salt handling, leaving
five appear in the nC columns of Table V, together with session, persistence, and rate-limiting code untouched. On
each variant’s per-assumption inference cost.                 this task the regenerated code differs from the original
   Findings. The LLM-guided mapper with a Qwen2.5- by a normalized edit distance of 0.40, versus 0.85 for Full
Coder-32B backbone achieves 64.2% accuracy (IoU 0.653), Regeneration and 0.82 for Manual Reprompt, which rewrite
the best of all mapper variants in Table V, exceeding the the entire function.
AssumptionMiner heuristic (56.9%, IoU 0.581) by 7.3 pp.          Metrics.
With a GPT-4o mapper, the LLM-guided variant scores              • Syntactic Validity Rate (SVR): fraction of tasks where
56.0% (IoU 0.596), on par with the heuristic (within 1 pp           the revised code compiles (py_compile). This is a
on accuracy). The result is therefore mapper-dependent: a           necessary but not sufficient condition for functional
strong open-source code model improves localization over            correctness. It does not verify that the revision im-
keyword-narrowing plus AST filtering, while GPT-4o does             plements the intended behavior, and full unit-test
not, and either LLM variant incurs one additional inference         evaluation is future work (§VIII).
                                                                                                                                             11



                          TABLE VII                                            (1) False negative       (2) False positive
   RQ3: Code adaptability when one assumption is revised                       T4: Persistence          T6: Security (hallucinated)
(n = 180, GPT-4o, full benchmark). SVR = syntactic validity                    users = {}               return token
   rate (py_compile); Edit Dist. = normalized Levenshtein                      Missed: “no I/O; in-memory
                                                                                                        Hallucinated: “tokens expire af-
(lower = more targeted). AssumptionMiner achieves lowest                       only.”                   ter 1h.”
             edit distance in all configurations.                              (3) Wrong category       (4) Imprecise dependency
                                                                               T5 labeled T3            T3: full method returned
Method                                       SVR      Edit Dist.   Lat. (s)    d = {}; d[k] = v         def validate(x):       ...entire
Manual Reprompt                               1.000        0.574       1.79    Hash-map choice mis-classified
                                                                                                        body...
Full Regeneration                             1.000        0.549       1.61    as error policy.         GT:      only    if x is None:
In-Place LLM Edit                             1.000        0.306       1.46                             return False.
AssumptionMiner (Incremental)                 0.833       0.244        2.40    (5) Failed regeneration  (6) Cascading edit
Cross-model: AssumptionMiner (Qwen2.5-Coder-32B, n = 30 novel tasks)           Wrong region modified    Revising A1 invalidates A3
AssumptionMiner (Qwen2.5-Coder-32B, local)  0.833        0.242         3.58    def parse() ← edited     bcrypt.hash(pw)
                                                                               Should have modified def T3 “return False” region no
                                                                               encode().                longer valid.
   • Edit Distance: character-level Levenshtein distance                      Fig. 5. Representative error cases across six failure modes.
     between original and revised code, normalized by the
     length of the longer string (lower = more targeted).
   • Latency: wall-clock time for the regeneration step in         (1) False negatives are the most frequent extraction
     seconds.                                                   failure for the open-source backbones, though GPT-4o
   Findings. AssumptionMiner makes the smallest edits inverts the balance (Table VIII). The extractor misses
in both configurations (0.244 on the full benchmark and assumptions that have no identifier-level cue: a T4 assump-
0.242 with Qwen32B on the novel tasks). Its advantage is tion encoded as users = {} is invisible to any approach
substantial over full regeneration and manual reprompting, that relies on function names or import statements. T1
and smaller but still present relative to in-place editing. The (Input Validation) is a leading source across backbones
bootstrap intervals for the full benchmark do not overlap because its realizations are often single-line guard checks
with those of any baseline.                                     with no domain-specific vocabulary.
   This benefit has a clear trade-off: the targeted pipeline       (2) False positives arise when the extractor proposes
achieves 83.3% syntactic validity, whereas all non-targeted     an  assumption the code does not implement. They concen-
baselines compile in every case. The error analysis at-         trate  in T3 (Table VIII), partly reflecting wrong-category
tributes most failures to cascading edits, in which a revision  predictions   (mode 3 below), which lenient matching counts
invalidates another linked region. Thus, the result supports    twice:   as a  false positive in the predicted category and
targeted regeneration as a way to limit change scope, not       a  false  negative   in the reference category. A rarer but
as a substitute for validation of the revised program.          distinctive  pattern    is T6 hallucination: the extractor infers
RQ3 answer. Assumption-guided regeneration reduces              expiry   logic or HTTPS      enforcement from context, but the
the size of a revision, with the lowest edit distance in both   code   contains   neither,   reflecting  a tendency in LLMs to
configurations. It currently trades that precision for lower    over-specify   security   concerns  when  prompted to audit code.
syntactic validity (83.3% versus 100% for the non-targeted      Requiring    textual   evidence   in the code before proposing a
baselines), so conflict detection and functional testing are    T6  assumption    is a  straightforward   prompt-level mitigation.
necessary next steps.                                              (3) Wrong-category errors occur most often at the
                                                                T1/T3 boundary (guard clauses), the T2/T4 boundary
                                                                (return type vs. storage), and the T3/T6 boundary (error
F. Error Analysis
                                                                handling vs. security policy). These are the same category
   Figure 5 illustrates six representative failure modes: boundaries that human annotators debated most during
three in extraction (1–3) and three in localization and taxonomy development (§II-C). Category errors propagate
regeneration (4–6). For the extraction modes, Table VIII to downstream dependency mapping, since AST node-type
summarizes each backbone’s error profile, derived from filters are category-specific.
the saved RQ1 predictions (per-category false-negative and         (4) Imprecise dependency errors occur when the
false-positive counts follow from per-category precision and dependency mapper identifies the correct function but
recall over the 676 reference assumptions). Modes (4)–(6) returns its entire body rather than the specific statement.
draw on the RQ2 and RQ3 runs (Tables V and VII). The This is common for T3 assumptions whose realization spans
cases in Figure 5 are illustrative.                             multiple return statements or except clauses scattered
                                                                through a function. The AST refinement pass computes a
                          TABLE VIII                            minimal enclosing sub-tree, which in these multi-site cases
  Extraction error profile per backbone, derived from the
 saved RQ1 predictions (n = 180, 676 reference assumptions).    spans the entire function body by construction. A future fix
                                                                is to report a union of minimal sub-trees rather than a single
Backbone                FN     FP    Top FN cat.    Top FP cat. enclosing sub-tree when candidates are non-contiguous.
GPT-4o †                  64    96    T2 (36%)       T3 (34%)      (5) Failed regeneration occurs when the regenerator
Qwen2.5-Coder-32B        167   130    T1 (49%)       T3 (54%)   modifies the wrong code region. Root cause: the depen-
DeepSeek-Coder-V2-Lite   181   113    T3 (32%)       T2 (27%)
                                                                dency map for one assumption partially overlaps with a
                                                                                                                          12



different function. For example, a T5 assumption about with Qwen32B on local vLLM (Table VII), and extraction
algorithm choice may be associated with def encode() via adds one comparable LLM call. That overhead is modest
the keyword hash, but the mapper returns def parse() against the several seconds generation already takes in
because it contains more matching tokens. Disambiguation a typical IDE, and the resulting records double as auto-
between candidate regions would require either stronger generated design documentation. AssumptionMiner can
assumption descriptions or a secondary prompt to the LLM be dropped into existing workflows as a post-generation
asking which function best matches.                            hook in any IDE extension that wraps an LLM code
   (6) Cascading edits are the dominant cause of the assistant. Teams adopting it at scale would accumulate a
17pp syntactic-validity gap between AssumptionMiner queryable corpus of assumption records, enabling cross-
and full-regeneration baselines. When revising assumption project comparison of how different backbones handle
A1 (e.g., switching from MD5 to bcrypt), the regenerator recurring ambiguity patterns such as error-propagation
correctly updates the hashing region, but the T3 assump- policy (T3) or authentication mechanism (T6).
tion A3 (“return False on bad password”) was linked to the        This paper is a first investigation: it establishes assump-
old hashing pipeline. After the bcrypt transition, A3 ’s code tion mining as a problem, contributes a benchmark and
region no longer exists in the same form. Regenerating taxonomy, and provides an initial empirical evaluation. Two
A1 without updating A3 ’s region leaves the function in an deeper questions stay open. First, why does an LLM make
internally inconsistent state. A conflict-detection pass that a particular assumption (a mechanistic-interpretability
re-validates all dependency links after each regeneration question)? Second, can extraction achieve provably reliable
step, and flags invalidated regions for secondary review, coverage rather than the empirical coverage RQ1 measures?
would address this without requiring full regeneration.        Both need interpretability tooling beyond our current
                                                               scope. The self-consistency concern of using LLMs to both
G. Discussion                                                  generate and extract assumptions is addressed here through
   The four backbones trade precision against recall in a cross-model validation (§VI-B) and, going forward, through
consistent way. Qwen2.5-Coder-32B is recall-biased and the human-verification protocol released with the artifact
DeepSeek-Coder-V2-Lite is precision-biased, which is pre- (§VIII).
cisely why combining them in the CW ensemble yields
the best fully cross-model result (F1 = 0.816). For code                         VII. Related Work
review, recall is usually the more valuable bias: a missed
                                                               A. LLM Code Generation, Repair, and Ambiguity
assumption is costlier than a spurious one a developer
can quickly reject. The trade-off tightens at lower capacity      Large language models achieve strong results on program-
(Qwen2.5-Coder-7B stays precise but has by far the lowest ming benchmarks such as HumanEval [1], MBPP [2], and
recall), suggesting that smaller models prefer safe, high- SWE-bench [4]. Self-repair approaches [19], [20] improve
confidence extractions and that added capacity mainly correctness by iterating on test failures. Self-planning
buys recall. It nonetheless remains a usable no-API-cost methods [18], [26] decompose prompts before generation.
option, comfortably ahead of both offline baselines.           Conversational tools [23] use test-driven dialogue to refine
   The AssumptionRecord schema (listing 2) is, structurally, incorrect code. User studies [6], [5] show that developers
an automated and fine-grained analogue of an Architectural frequently struggle to identify why generated code is
Decision Record. We develop this connection, and its wrong, a gap that AssumptionMiner directly addresses
implications for architecture knowledge management, in by surfacing implicit design decisions as editable, traceable
§VII. A natural extension is to promote Assumption- records.
Miner-generated records to first-class ADR artifacts stored       Automated Program Repair (APR) [27], [28], [29] gener-
alongside the code, giving a live decision log that grows ates patches for observable failures (test errors, crashes).
with the codebase.                                             AssumptionMiner’s incremental regenerator (C5) shares
   RQ3 exposes a genuine tension between how surgical the patch-isolation structure, but its trigger is funda-
AssumptionMiner is and how reliably its output compiles. mentally different: APR is fault-driven, whereas C5 is
It makes the smallest edits of any method but reaches only assumption-driven, targeting working-but-wrong code that
83% syntactic validity, whereas In-Place LLM Edit (IPE) produces no test failures yet violates developer intent, a
compiles in every case at a larger edit distance. What regime APR cannot address.
sets AssumptionMiner apart is traceability: each edit is          Requirements engineering research addresses natural-
tied to a specific AssumptionRecord, so a developer can language ambiguity detection [8], [30], [31] in human-
audit which decision drove which change, and independent written specifications, and a parallel line studies ambiguity
revisions can be applied in parallel, neither of which a free- in the prompts given to code models: ambiguous, contradic-
form IPE edit supports. The validity gap stems mainly from tory, or incomplete task descriptions measurably degrade
cascading edits (error mode 6, Figure 5), where revising generated-code correctness [15], and lightweight classifiers
Ai invalidates Aj ’s region. We intend to close it with a can flag such defective descriptions before generation [13].
conflict-detection pass.                                       These approaches all analyze the input specification. As-
   In deployment the regeneration step is cheap: across our sumptionMiner instead extends ambiguity handling to
RQ3 runs it averaged 2.4 s per task with GPT-4o and 3.6 s the LLM’s output, where the artifact under analysis is
                                                                                                                         13



executable code and the goal is not only detection but also      too numerous for manual ADR authoring in practice.
structured, targeted revision.                                   The resulting corpus could retroactively seed architectural
                                                                 documentation tools [40], bridging micro-level assumption
B. Interactive Code Generation and Prompt Engineering tracking and macro-level architecture knowledge manage-
                                                                 ment.
   Several systems augment LLM code generation with                 Previous work on automated design-rationale extrac-
interactive clarification steps. Clarify [18] generates clarify- tion [27] targets source code history and commit messages.
ing questions before producing code, reducing assumption- AssumptionMiner targets the generation-time decision
driven errors in some settings. TiCoder [17] formalizes surface, which is both earlier in the lifecycle and richer in
user intent interactively by generating candidate tests the implicit signals.
developer confirms or rejects, pruning the space of programs
consistent with the prompt. However, these systems require                      VIII. Threats to Validity
developers to answer questions up-front and do not link             We assess threats following Wohlin et al. [41].
answers to specific code regions, meaning later revision            Internal validity. The primary internal threat is that
requires a full reprompt rather than a targeted update. the benchmark reference annotations are LLM-derived:
Prompt engineering surveys [10] document patterns for GPT-4o proposed all assumptions and code-region ref-
eliciting more precise behavior from LLMs, but operate erences, and the taxonomy was developed by a single
entirely at the prompt level and cannot recover implicit researcher with LLM assistance. Hallucinated or mis-
decisions already made by the model. AssumptionMiner categorized reference entries would distort the reported
is complementary to both: it operates post-generation, precision and recall. To bound this threat, two developers
diagnosing what the LLM already decided rather than independently reviewed all 111 assumptions of the curated
shaping what it will decide, and enables revision without subset, judging for each (a) whether it is a valid implicit
a full reprompt.                                                 assumption under Definition 1, (b) its taxonomy category,
                                                                 and (c) whether its code-region reference is correct (rater
C. Program Analysis and Traceability                             background, effort, and completed sheets in Appendix C
   Traceability techniques [32], [33] link requirement arti- and the artifact). Because one of the two annotators is
facts to code via information retrieval or machine learning, an author, the agreement statistics measure consistency
and static analysis tools [34], [35] construct data-flow and between the author and a second, independent developer
control-flow dependency graphs. Neither class of technique rather than between two fully external raters. The second
connects dependency edges to the natural-language in- developer’s independent agreement nonetheless indicates
tent that produced the code. AssumptionMiner bridges the labels are not idiosyncratic to the author. Agreement
this gap with assumption-to-code dependency graphs for was high on the two judgments that do not depend on line
LLM-generated artifacts, enabling developer auditing and numbers: validity reached 99.1% raw agreement (κ = 0.66,
automated change propagation.                                    and both raters independently rejected only a single
   Specification mining [36] and contract inference extract candidate that restates an explicit prompt requirement),
program invariants post-hoc from executions or static and category reached 88.3% raw agreement (κ = 0.85,
analysis. LLM-augmented testing tools (CodaMosa [37], “almost perfect” [42]). The κ for validity is lower than
Fuzz4All [38]) leverage language models for coverage-driven its raw agreement because κ is deflated when one class
exploration and oracle generation, but all operate after dominates (nearly all candidates are valid). We therefore
code exists and cannot attribute discovered properties to report both. The code-region review corroborated the
specific prompt ambiguities. AssumptionMiner is com- AST-based reference correction of Appendix C: one rater
plementary: its assumption layer could seed downstream independently flagged the majority of the automatically
invariant checkers, while its primary role is interactive corrected references as originally wrong, and after correc-
disambiguation at generation time.                               tion the other rater accepted them. These results support
                                                                 the reliability of the curated-subset reference. Residual
                                                                 risk concerns the 150-task extended tier, which is not
D. Design Rationale and Decision Documentation                   human-verified and is used for RQ1 and the secondary RQ2
   Architectural Decision Records (ADRs) [39], [40] capture analysis. Extraction runs at temperature 0 to minimize non-
the rationale, alternatives, and consequences of design determinism. Each reported number comes from a single
decisions as lightweight prose documents. The Assump- scored run per task and configuration, with raw outputs
tionRecord schema in AssumptionMiner is directly preserved in the artifact.
inspired by this tradition: both treat design decisions as          LLM backbone bias. Because GPT-4o produced the ref-
first-class, addressable artifacts with explicit alternatives. erence annotations, evaluating AssumptionMiner (GPT-
The key distinction is automation and granularity: ADRs 4o) on this benchmark risks circular self-consistency rather
are authored manually by architects for major architec- than true generalization, which we flag with † throughout
tural choices, whereas AssumptionMiner generates fine- (Tables III and IV). We treat the fully cross-model results
grained assumption records automatically during code as our primary validity claims: Qwen2.5-Coder-32B (F1 =
synthesis, capturing routine, ephemeral decisions that are 0.774) and DeepSeek-Coder-V2-Lite (F1 = 0.771), neither
                                                                                                                            14



of which was involved in benchmark construction, though             We presented AssumptionMiner, a framework that
their scores still measure agreement with the reference. The     mines implicit assumptions from LLM-generated code,
human verification above further reduces the concern that        surfaces them as structured AssumptionRecord objects
the reference itself is an artifact of the annotating model.     linked to their governing code regions, and propagates
   Benchmark contamination. HumanEval [1] and                    developer-specified revisions through targeted incremental
MBPP [2] tasks (the 150-task extended tier) are part of          regeneration. Offline baselines that rely on surface syntax
GPT-4o’s training data. The model may therefore generate         obtain low scores (F1 = 0.225 and below), suggesting that
predictable, stereotyped solutions whose assumptions are         such cues alone are insufficient for this task. Using only
easier to extract, potentially inflating extraction accuracy     open-source models, AssumptionMiner’s cross-model
relative to novel tasks. The 30 tasks of the curated subset      ensemble reaches F1 = 0.816, a 3.6× improvement over the
are novel and designed to be out-of-distribution, further        strongest offline baseline, and the best result we obtained
reinforcing the primacy of cross-model results on that           without a proprietary API. Under a stricter decision-level
subset.                                                          metric that also requires the extracted description to match
   External validity. The benchmark is Python-only and           the reference decision, however, the same ensemble reaches
may not generalize to statically typed languages (e.g., Rust,    only F1 = 0.66 (and the best individual open-source model
Java) where some assumptions are enforced by the type            0.65), far above the near-zero non-LLM baselines but low in
system. Industrial-scale codebases with multi-file context       absolute terms. Reliably identifying which implicit decision
may expose additional assumption categories not covered          a model made is thus far from solved, and we hope the
by our six-category taxonomy, and team conventions or            benchmark and this second, stricter metric draw future
organizational style guides may create assumption patterns       work to the problem. Its dependency mapper localizes
not present in HumanEval/MBPP tasks.                             assumptions to the lines that implement them more
   Construct validity. The headline AR/AP/AF1 use                tightly than either baseline, although on binary accuracy
category-level matching, which measures coverage of deci-        it is competitive with, rather than clearly better than, a
sion kinds rather than description fidelity: two assumptions     keyword heuristic (an optional LLM-guided variant does
in the same category but with different descriptions both        better, at extra inference cost). When a developer revises
count as correct. This leniency inflates absolute scores         an assumption, the incremental regenerator changes 1.3–
symmetrically across methods, so relative comparisons            2.4× less code than non-targeted alternatives, but at a cost
remain meaningful but the absolute lenient F1 should not         in syntactic validity. The error analysis identifies cascading
be read as decision-level accuracy. To bound the effect we       edits as a common failure mode. Conflict detection is a
also report the strict decision-level metric (§VI-A, §VI-B),     promising, but untested, mitigation.
which requires the predicted description to match the               The broader implication is that implicit assumptions
reference decision. It is substantially lower, quantifying the   in AI-generated code are not merely a quality concern
gap rather than leaving it unmeasured. We use embedding          but a traceability concern: without explicit records of why
cosine (deterministic) rather than an LLM judge for              code looks the way it does, developers cannot confidently
this metric to avoid compounding the LLM-grades-LLM              revise AI-generated artifacts. Within the scope of this study,
circularity discussed above. RQ3’s syntactic validity rate       AssumptionMiner shows that assumption records can
is necessary but not sufficient for functional correctness.      be generated at interactive-scale cost and used to support
Unit-test evaluation is left to future work.                     auditable code updates. Whether this workflow improves
   Conclusion validity. We use a two-tier evaluation             developer decision making in practice remains an important
design. RQ1 and RQ3 are evaluated on the full benchmark          question for future user studies.
(n = 180). RQ2’s primary analysis uses the curated                  Future work includes extending human verification to the
subset (n = 30 tasks, 109 assumptions), where code-region        150-task extended tier and beyond, extending Assumption-
references exist, with a secondary full-set analysis. For        Miner to multi-file repositories, incorporating project-level
n = 180 comparisons we report bootstrap 95% confidence           style guides as assumption priors, a conflict-detection pass
intervals (§VI-B, §VI-E) and Cliff’s δ effect sizes (§VI-E).     for cascading edits, description-level quality metrics, unit-
At n = 30 we omit significance testing and report point          test-based evaluation of regenerated code, and integration
estimates only. The consistent direction of effects across       with test generation and static analysis tools. We release the
four independent backbones further supports conclusion           benchmark and the AssumptionMiner implementation
robustness.                                                      (see Data Availability).

                     IX. Conclusion
                                                                                     Acknowledgment
   LLM code generation silently embeds implicit assump-
tions (a mean of 3.8 per task in our benchmark) that                The author thanks Mike Papadakis (University of Lux-
developers have no systematic way to inspect or revise.          embourg) for helpful discussions.
These decisions are one source of working-but-wrong code:           We acknowledge the use of OpenAI Codex and An-
code that passes available tests yet violates developer          thropic’s Claude [43] for assistance in polishing the writing
intent.                                                          of this paper.
                                                                                                                                               15



                      Data Availability                                  [19] T. X. Olausson, J. P. Inala, C. Wang, J. Gao, and A. Solar-
                                                                              Lezama, “Is self-repair a silver bullet for code generation?” in
  The AssumptionMiner benchmark (180 tasks / 676                              Proc. ICLR, 2024.
assumptions, 30 curated-subset tasks for RQ2), the As-                   [20] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegr-
                                                                              effe et al., “Self-refine: Iterative refinement with self-feedback,”
sumptionMiner source code, all evaluation scripts, raw                        in Proc. NeurIPS, 2023.
results for RQ1–RQ3, and the human-verification pro-                     [21] A. Strauss and J. Corbin, Basics of Qualitative Research:
tocol and annotation sheets, with instructions to repro-                      Techniques and Procedures for Developing Grounded Theory,
                                                                              2nd ed. Sage Publications, 1998.
duce all tables and figures, are archived on Zenodo at                   [22] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia,
https://doi.org/10.5281/zenodo.21535058 (DOI:                                 E. H. Chi, Q. V. Le, and D. Zhou, “Chain-of-thought prompting
10.5281/zenodo.21535058).                                                     elicits reasoning in large language models,” in Proc. NeurIPS,
                                                                              2022.
                                                                         [23] C. S. Xia and L. Zhang, “Conversational automated program
                                                                              repair,” arXiv preprint arXiv:2301.13246, 2023.
                          References                                     [24] OpenAI, “GPT-4o system card,” 2024. [Online]. Available:
                                                                              https://arxiv.org/abs/2410.21276
 [1] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto,
                                                                         [25] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E.
     J. Kaplan, H. Edwards et al., “Evaluating large language models
                                                                              Gonzalez, H. Zhang, and I. Stoica, “Efficient memory manage-
     trained on code,” arXiv preprint arXiv:2107.03374, 2021.
                                                                              ment for large language model serving with PagedAttention,” in
 [2] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski,
                                                                              Proc. ACM SOSP, 2023.
     D. Dohan et al., “Program synthesis with large language models,”
                                                                         [26] Y. Dong, X. Jiang, Z. Jin, and G. Li, “Self-collaboration code
     arXiv preprint arXiv:2108.07732, 2021.
                                                                              generation via ChatGPT,” ACM Transactions on Software
 [3] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser,
                                                                              Engineering and Methodology, vol. 33, no. 7, pp. 1–38, 2024.
     R. Leblond et al., “Competition-level code generation with
                                                                         [27] K. Liu, A. Koyuncu, D. Kim, and T. F. Bissyandé, “AVATAR:
     AlphaCode,” Science, vol. 378, pp. 1092–1097, 2022.
                                                                              Fixing semantic bugs with fix patterns of static analysis viola-
 [4] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press,             tions,” in Proc. SANER, 2019.
     and K. Narasimhan, “SWE-bench: Can language models resolve          [28] Z. Chen, S. Kommrusch, M. Tufano, L.-N. Pouchet, D. Poshy-
     real-world GitHub issues?” in Proc. ICLR, 2024.                          vanyk, and M. Monperrus, “SequenceR: Sequence-to-sequence
 [5] A. Ziegler, E. Kalliamvakou, X. A. Li, A. Rice, D. Rifkin,               learning for end-to-end program repair,” IEEE Transactions on
     S. Simister, G. Sittampalam, and E. Aftandilian, “Productivity           Software Engineering, vol. 47, no. 9, pp. 1943–1959, 2021.
     assessment of neural code completion,” in Proc. MAPS, 2022.         [29] H. Ye, M. Martinez, and M. Monperrus, “Neural program repair
 [6] P. Vaithilingam, T. Zhang, and E. L. Glassman, “Expectation              with execution-based backpropagation,” in Proc. ICSE, 2022.
     vs. experience: Evaluating the usability of code generation tools   [30] N. Kiyavitskaya, N. Zeni, L. Mich, and D. M. Berry, “Require-
     powered by large language models,” in Proc. CHI EA, 2022.                ments for tools for ambiguity identification and measurement in
 [7] K. Wiegers and J. Beatty, Software Requirements, 3rd ed.                 natural language requirements specifications,” in Requirements
     Microsoft Press, 2013.                                                   Engineering, 2008.
 [8] A. Ferrari and A. Esuli, “An NLP approach for cross-domain          [31] S. Ezzini, S. Abualhaija, C. Arora, M. Sabetzadeh, and L. C.
     ambiguity detection in requirements engineering,” Automated              Briand, “Using domain-specific corpora for improved handling of
     Software Engineering, vol. 26, pp. 559–598, 2019.                        ambiguity in requirements,” in Proc. ICSE, 2021, pp. 1485–1497.
 [9] M. Shaw, “Correctness, confidence, and context: Framing             [32] J. Lin, Y. Liu, Q. Zeng, M. Jiang, and J. Cleland-Huang,
     software assurance in the AI age,” 2026. [Online]. Available:            “Traceability transformed: Generating more accurate links with
     https://arxiv.org/abs/2607.04667                                         pre-trained BERT models,” in Proc. ICSE, 2021, pp. 324–335.
[10] J. White, Q. Fu, S. Hays, M. Sandborn, C. Olea, H. Gilbert          [33] C. McMillan, M. Grechanik, D. Poshyvanyk, C. Fu, and Q. Xie,
     et al., “A prompt pattern catalog to enhance prompt engineering          “Portfolio: Finding relevant functions and their usages,” in Proc.
     with ChatGPT,” arXiv preprint arXiv:2302.11382, 2023.                    ICSE, 2011, pp. 111–120.
[11] I. Stoica, M. Zaharia, J. Gonzalez, K. Goldberg, K. Sen,            [34] B. Livshits, M. Sridharan, Y. Smaragdakis, O. Lhoták, J. N.
     H. Zhang, A. Angelopoulos, S. G. Patil, L. Chen, W.-L. Chiang,           Amaral, B.-Y. E. Chang et al., “In defense of soundiness: A
     and J. Q. Davis, “Specifications: The missing link to making the         manifesto,” Communications of the ACM, vol. 58, no. 2, pp.
     development of LLM systems an engineering discipline,” 2024.             44–46, 2015.
     [Online]. Available: https://arxiv.org/abs/2412.05299               [35] D. Guo, S. Ren, S. Lu, Z. Feng, D. Tang, S. Liu et al.,
[12] F. Mu, L. Shi, S. Wang, Z. Yu, B. Zhang, C. Wang, S. Liu, and            “GraphCodeBERT: Pre-training code representations with data
     Q. Wang, “ClarifyGPT: A framework for enhancing LLM-based                flow,” in Proc. ICLR, 2021.
     code generation via requirements clarification,” Proceedings of     [36] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco,
     the ACM on Software Engineering, vol. 1, no. FSE, 2024.                  M. S. Tschantz, and C. Xiao, “The Daikon system for dynamic de-
[13] A. Akli, M. Papadakis, M. Cordy, and Y. Le Traon, “Defective             tection of likely invariants,” Science of Computer Programming,
     task descriptions in LLM-based code generation: Detection and            vol. 69, no. 1–3, pp. 35–45, 2007.
     analysis,” arXiv:2604.24703, 2026.                                  [37] C. Lemieux, J. P. Inala, S. K. Lahiri, and K. Sen, “CodaMosa:
[14] J. J. W. Wu and F. H. Fard, “HumanEvalComm: Benchmarking                 Escaping coverage plateaus in test generation with pre-trained
     the communication competence of code generation for LLMs and             large language models,” in Proc. ICSE, 2023.
     LLM agent,” ACM Transactions on Software Engineering and            [38] C. S. Xia, M. Paltenghi, J. L. Tian, M. Pradel, and L. Zhang,
     Methodology, 2025.                                                       “Fuzz4All: Universal fuzzing with large language models,” in
[15] M. Larbi, A. Akli, M. Papadakis, R. Bouyousfi, M. Cordy,                 Proc. ICSE, 2024.
     F. Sarro, and Y. Le Traon, “When prompts go wrong: Eval-            [39] A. Jansen and J. Bosch, “Software architecture as a set of
     uating code model robustness to ambiguous, contradictory, and            architectural design decisions,” in Proc. Working IEEE/IFIP
     incomplete task descriptions,” arXiv:2507.20439, 2025.                   Conference on Software Architecture (WICSA), 2005, pp. 109–
[16] J. J. W. Wu et al., “ClarifyCoder: Clarification-aware fine-             120.
     tuning for programmatic problem solving,” 2025, tODO:               [40] R. Capilla, A. Jansen, A. Tang, P. Avgeriou, and M. A. Babar, “10
     complete author list from arXiv:2504.16331. [Online]. Available:         years of software architecture knowledge management: Practice
     https://arxiv.org/abs/2504.16331                                         and future,” Journal of Systems and Software, vol. 116, pp. 191–
[17] S. K. Lahiri, A. Naik, G. Sakkas, P. Choudhury, C. von Veh,              205, 2016.
     M. Musuvathi, J. P. Inala, C. Wang, and J. Gao, “Interac-           [41] C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell, and
     tive code generation via test-driven user-intent formalization,”         A. Wesslén, Experimentation in Software Engineering. Springer,
     arXiv:2208.05950, 2022.                                                  2012.
[18] X. Jiang, Y. Dong, L. Wang, Q. Shang, and G. Li, “Self-planning     [42] J. R. Landis and G. G. Koch, “The measurement of observer
     code generation with large language models,” arXiv preprint              agreement for categorical data,” Biometrics, vol. 33, no. 1, pp.
     arXiv:2303.06689, 2023.                                                  159–174, 1977.
                                                                                                                              16



[43] Anthropic, “Claude [large language model],” 2025. [Online].                     Appendix C
     Available: https://www.anthropic.com/claude                            Benchmark Construction Details
                                                                   A. Novel Task Design
                   Appendix A
         Full Extraction Prompt Template                              The 30 novel tasks of the curated subset were de-
  The full system and user prompt used by C3 (Assumption           signed to: (a) cover domains underrepresented in standard
Extractor) in all experiments is:                                  benchmarks (authentication, serialization, file I/O, network
                                                                   I/O, concurrency); (b) stress-test T4 (Persistence) and
SYSTEM :                                                           T6 (Security) categories by requiring tasks where storage
You are an expert software engineer auditing LLM -
    generated                                                      backend and security policy choices are meaningful; (c) be
code for implicit design decisions ( implicit                      short enough that GPT-4o could solve them in under 30
    assumptions ) .                                                lines of Python, avoiding multi-file complexity; and (d) be
USER :                                                             genuinely ambiguous: each task deliberately omits at least
### Original Prompt                                                two meaningful design choices.
{ prompt }

### Generated Code
‘‘‘ python                                                         B. Reference Annotation Pipeline
{ code }                                                               For every task, GPT-4o [24] extracted an Assumption-
‘‘‘
                                                                    Record list using the standard prompt (section A) at tem-
### Task                                                            perature 0. Records were then validated programmatically
1. REASON : List every design decision embedded in                  (schema conformance, category vocabulary, deduplication
        the code
     that is NOT explicitly required by the prompt .                by category and description similarity). For the curated
              For each ,                                            subset, code-region references (line ranges) were produced
     name at least one realistic alternative .                      by the same pipeline from the code_refs field. Because
2. FORMAT : Return a JSON array of                                  these line numbers are LLM-counted rather than parser-
      A s s u m p t i o n R e co r d objects                        derived, they are susceptible to indexing errors: a tree-
     matching this schema :                                         sitter consistency scan (each reference’s declared AST-
{ schema }
                                                                    node type checked against the node actually present at
Taxonomy categories :                                               the stored lines) found 15 of the 111 curated references
   T1 -- Input format / validation                                  off by one to two lines, consistent with sporadic 0-indexed
   T2 -- Return type / output structure
   T3 -- Edge - case / error - handling policy                      counting by the annotating model. These were corrected
   T4 -- Persistence / storage backend                              by snapping each reference to its declared node, with every
   T5 -- Algorithm / performance trade - off                        correction manually adjudicated against the assumption
   T6 -- Security / au thentica tion policy
                                                                    description (scripts/fix_coderef_offsets.py in the
Return ONLY valid JSON after the tag [ RECORDS ].                   artifact documents all 15). All RQ2 results in this paper
Do not include any other text after [ RECORDS ].                    are scored against the corrected references.
[ RECORDS ]                                                            Human verification. Two developers then independently
Listing 3. Full extraction prompt. {prompt}, {code}, and {schema}
                                                                    reviewed   all 111 curated-subset assumptions using the
are substituted at runtime.                                         released  protocol, recording for each a validity judgment,
   The schema object inserted at {schema} is:                       a taxonomy category, and whether the (corrected) code-
{
                                                                    region reference is correct. Both have at least five years of
   " id ":                       " string ( e . g . ’A1 ’) " ,      professional software-development experience in industry.
   " category ":                 " T1 | T2 | T3 | T4 | T5 | T6 " ,  One is an author of this paper and the other is an indepen-
   " description ": " natural - language statement of
          the assumption " ,
                                                                    dent developer not otherwise involved in the project. Each
   " rationale ":                " why the LLM made this choice " , rater spent roughly four hours on this independent pass,
   " alternatives ": [" list of >=1 realistic                       after which the two met for an approximately one-hour
          alternatives "] ,
   " confidence ":               " float in [0 ,1]" ,
                                                                    joint session to resolve every disagreement to consensus.
   " severity ":                 " low | medium | high "            Inter-rater agreement (before reconciliation) was 99.1%
}                                                                   (κ = 0.66) on validity and 88.3% (κ = 0.85) on category.
                                                                    On the code-region judgment the raters agreed on 89.6% of
   The code_refs field (used by C4) is not included in the
                                                                    comparable references. The region review also served as an
extraction prompt. C4 populates it separately after the
                                                                    independent audit of the AST correction above: one rater,
extraction call returns.
                                                                    working from the pre-correction line numbers, flagged the
                                                                    majority of the 15 corrected references as originally wrong,
                                   Appendix B                       while the other, working from the corrected numbers,
   Full Per-Category Precision, Recall, and F1                      accepted them, an independent confirmation of the fix.
   Table IX extends Table IV with per-category AR and Disagreements were resolved by discussion to form the
AP values for the cross-model backbones.                            final reference: two assumptions were removed as invalid,
                                                                                                                                                                              17



                                                         TABLE IX
Full per-category precision (AP), recall (AR), and F1 (AF1 ) for all AssumptionMiner backbones on the benchmark (n = 180,
                           676 assumptions). † self-evaluation risk for GPT-4o on 150/180 tasks.

                                          T1                      T2                       T3                      T4                      T5                      T6
Method                   All F1      P       R      F1       P       R      F1       P        R      F1       P       R      F1       P       R      F1       P         R     F1
GPT-4o†                  0.884    0.876   0.936   0.905   0.930   0.839   0.882   0.823    0.922   0.869   0.800   0.500   0.615   0.866   0.940   0.902   0.429   0.600    0.500
Qwen2.5-Coder-32B        0.774    0.865   0.601   0.709   0.934   0.692   0.795   0.679    0.892   0.771   0.600   0.750   0.667   0.834   0.868   0.851   0.429   0.600    0.500
DeepSeek-Coder-V2-Lite   0.771    0.876   0.734   0.799   0.788   0.804   0.796   0.818    0.651   0.725   0.556   0.625   0.588   0.808   0.755   0.781   0.400   0.800    0.533
Qwen2.5-Coder-7B         0.593    0.923   0.414   0.571   0.738   0.867   0.797   0.904    0.283   0.431   0.375   0.375   0.375   0.824   0.371   0.511   0.667   0.400    0.500




eight category labels were corrected, and twelve code-                                       Because both backbones vote on each category and
region spans were reconciled (several additional off-by-                                  only the single highest-confidence instance per qualifying
one references the automated scan had missed), yielding                                   category is kept, CW trades a small amount of recall for
a human-verified curated subset of 109 assumptions. All                                   precision relative to a plain union. On the benchmark
curated-subset (RQ2) and open-source RQ1 results in this                                  the three strategies score: Union (keep all records from
paper are scored against this reconciled reference. Re-                                   either backbone) P = 0.755, R = 0.857, F1 = 0.803;
scoring changed the full-benchmark numbers by at most                                     Intersection (keep only categories produced by both
0.006, confirming the LLM-derived reference was already                                   backbones) P = 0.887, R = 0.624, F1 = 0.733; CW
reliable. The rating sheets, the agreement script, the                                    P = 0.810, R = 0.823, F1 = 0.816. CW outperforms both
adjudication decisions, and the resulting consensus.jsonl                                 by combining the backbones’ confidence signals rather than
are included in the artifact.                                                             applying a binary gate.

                                                                                                                 Appendix E
C. Extended-Tier Tasks                                                                                  Software Artifact Details
  The 150 tasks drawn from HumanEval and MBPP use                                            AssumptionMiner is implemented as an open-source
the same pipeline. These annotations are used only for                                    Python package (assumption_miner) released alongside
RQ1 extraction evaluation and the RQ2 full-set secondary                                  this paper. This section describes the software architecture,
analysis (Table V, auto-labeled columns). RQ2’s primary                                   interfaces, and replication support.
analysis uses only the curated subset. The extended tier is
not human-verified. This is noted as a residual threat in             A. Architecture and Components
§VIII.
                                                                         The package maps directly to the five components
                                                                      described in section III-A, one module per component:
                                  Appendix D                             C1 (Prompt Ingestion), ingestion.py. A
            Conf-Weighted Ensemble Algorithm                          CodeSample data class with three constructors:
   Algorithm 4 gives the pseudocode for the Conf-Weighted from_strings (prompt and code as plain strings),
(CW) ensemble used to combine the high-recall back- from_json_file (iterates benchmark JSON files such as
bone (Qwen2.5-Coder-32B) and high-precision backbone data/benchmark.json), and from_code_file (prompt
(DeepSeek-Coder-V2-Lite).                                             plus a path to a source file).
                                                                         C2       (Code        Generator),        generator.py.
                                                                      generate_code() dispatches to interchangeable backends
def e n s e m b l e _ c o n f _ w e i g h t e d ( preds_a , preds_b ,
                                                  threshold =0.5) :   selected by the ASSUMPTION_MINER_BACKEND environment
        " " " Include ␣ a ␣ category ␣ if ␣ the ␣ mean                variable: openai (OpenAI API, configurable model)
␣ ␣ ␣ ␣ confidence ␣ across ␣ all ␣ instances ␣ from                  or local (an OpenAI-compatible vLLM endpoint for
␣ ␣ ␣ ␣ either ␣ backbone ␣ >= ␣ threshold ; ␣ keep ␣ the
␣ ␣ ␣ ␣ highest - confidence ␣ instance . " " "                       open-source models).
        by_cat = defaultdict ( list )                                    C3 (Assumption Extractor), extractor.py.
        for p in preds_a + preds_b :                                  extract_assumptions() issues the structured two-part
               by_cat [ p [ " category " ]]. append ( p )
                                                                      prompt (Appendix A) and parses the [RECORDS] JSON
        result = []                                                   block into AssumptionRecord objects (schema.py, which
        for cat , items in sorted ( by_cat . items () ) :             also defines the CodeRef type for dependency links).
               mean_conf = ( sum ( x [ " confidence " ]
                                      for x in items )                   C4 (Dependency Mapper), dependency.py.
                                      / len ( items ) )               map_dependencies() implements the two-pass strategy:
               if mean_conf >= threshold :                            keyword-overlap candidate selection followed by AST
                    best = max ( items ,
                            key = lambda x : x [ " confidence " ])    narrowing that snaps candidate lines to the smallest
                    result . append ( best )                          enclosing category-appropriate node. The LLM-guided
        return result                                                 variant evaluated in §VI-D is available via a use_llm flag.
Listing 4.       Conf-Weighted (CW) ensemble (as implemented The AST heuristic is the default for its zero inference cost,
in scripts/run_rq1_ensemble.py). preds_a and preds_b are with the LLM-guided mapper available for accuracy-critical
AssumptionRecord lists from the two backbones for one task.
                                                                      settings.
                                                                                                                                        18




Fig. 6. The AssumptionMiner web interface on the running authentication example (screenshots of the released interface/ application).
Top: after Analyze, the backbone-generated code (left) is shown beside its five extracted assumption records (right), each labeled with its
taxonomy category (T2–T6) and an LLM-assigned severity. Hovering a card highlights the code lines it governs. Bottom: mid-review, the
developer has accepted A2, rejected A5, and opened A1 for editing (MD5 → bcrypt). Pressing Regenerate invokes the incremental regenerator
(C5) on only that assumption’s code region. The footer tracks review progress.
                                                                                                                                           19



  C5 (Incremental Regenerator), regenerator.py.                E. Quality and Testing
regenerate() accepts a revised AssumptionRecord and
                                                                  The package ships with a unit-test suite of 119 tests
the original code, constructs a region-targeted prompt from
                                                               across eight modules (assumption_miner/tests/), all
the dependency map (k = 5 context lines), and splices the
                                                               passing at release, covering schema serialization round-trips,
regenerated region back into the surrounding code.
                                                               dependency-mapper AST logic, extractor output parsing,
  The offline baselines of Table III (CE, KBE) and the
                                                               ingestion, the offline baselines, and the RQ evaluation
prompting baselines (DG, CQ, CoT) are implemented in
                                                               helpers. All results in section VI were generated from the
baselines.py, so every number in section VI is repro-
                                                               released code with no post-hoc modifications.
ducible from the same package.

                                                                                        Appendix F
B. Scripts and Entry Points
                                                                                   Reproducibility Notes
   All experiment scripts are under scripts/:
   • run_rq1.py: extraction evaluation on a benchmark
                                                              A. Environment
     file.                                                      All local-model experiments were conducted on a ma-
   • run_rq1_offline.py: CE/KBE offline baselines.            chine with an NVIDIA RTX PRO 6000 Blackwell Max-
   • run_rq1_ensemble.py: Union/Intersection/CW en- Q Workstation Edition GPU (96 GB VRAM), serving
     sembles combining two extractor outputs.                 models through vLLM’s OpenAI-compatible server. The
   • run_rq1_semantic.py: strict decision-level AF1 via       package requires Python ≥3.10 with tree-sitter ≥0.22
     sentence-embedding similarity at threshold τ .           and tree-sitter-python ≥0.22 (exact dependency pins
   • build_strict_inputs.py:           reconstructs     per- are recorded in pyproject.toml in the artifact). Cloud
     prediction descriptions for the CE/KBE baselines and API calls used the OpenAI API with model alias gpt-4o.
     the CW ensemble so they can be scored under the
     strict metric.
   • run_rq2.py,                     run_rq2_ablation.py, B. Running the Experiments
     run_rq2_usellm.py: dependency accuracy, node-              From the repository root:
     type ablation, and the heuristic-vs.-LLM mapper
                                                              # Install d e p e n d e n c i e s
     comparison.                                              pip install -e " .[ dev ] "
   • run_rq3.py: code adaptability evaluation.

   Each script accepts –benchmark, –out, –backend, and #python  RQ1 - GPT -4 o ( cloud )
                                                                      scripts / run_rq1 . py \
–limit flags documented in –help output. A –dry-run             -- backend openai -- model gpt -4 o \
flag substitutes the offline KBE extractor for all LLM calls,   -- benchmark data / benchmark . json \
                                                                -- out data / results / rq1_gpt4o . json \
enabling smoke-testing without API credentials or GPU           -- delay 0.5
access.
                                                               # RQ1 - Qwen2 .5 - Coder -32 B ( local vLLM )
                                                               bash scripts / s t a r t _ v l l m _ s e r v e r . sh # t e r m i n a l 1
C. Interactive Interface                                       python scripts / run_rq1 . py \
                                                                 -- backend local \
   The interactive interface (§IV) is a single-page web          -- benchmark data / benchmark . json \
application served by interface/server.py, exposing              -- out data / results / rq1_qwen32b . json \
                                                                 -- delay 0.1 # t e r m i n a l 2
three REST endpoints: /api/analyze (prompt → code
+ assumption records), /api/regenerate (code + revised         # RQ1 e n s e m b l e ( no GPU if using cloud b a c k b o n e s )
assumption → updated code), and /api/status. It runs           python scripts / r u n _ r q 1 _ e n s e m b l e . py \
                                                                 -- benchmark data / benchmark . json \
against either backend (OpenAI or local vLLM) using the          -- out data / results / rq1_ensemble . json
same environment-variable configuration as the package.
Figure 6 shows the running interface on the paper’s            # RQ2 mapper a b l a t i o n
                                                               python scripts / run_rq2_ usellm . py \
authentication example: the generated code appears on the        -- backend openai -- model gpt -4 o \
left, and each extracted assumption becomes a category-          -- benchmark data / benchmark . json \
tagged, severity-scored card on the right that the developer     -- out data / results / r q 2 _ u s e _ l l m _ g p t 4 o . json
can accept, edit, or reject before regenerating.               # RQ3 code a d a p t a b i l i t y
                                                               python scripts / run_rq3 . py \
                                                                 -- backend openai -- model gpt -4 o \
D. Extensibility                                                 -- benchmark data / bench mark_min i . json \
                                                                 -- out data / results / rq3_gpt4o . json
   New backbone LLMs are added as a dispatch case
in generator.py/extractor.py (any OpenAI-compatible A dry-run mode (no API calls) is available for smoke
endpoint works out of the box via the local backend). testing:
New assumption categories require extending the taxonomy python scripts / run_rq1 . py -- dry - run \
vocabulary in the extraction prompt and the category-to-   -- benchmark data / bench mark_min i . json -- limit 3
node-type map in dependency.py.
                                                                       20



C. Randomness
  LLM outputs are non-deterministic in general. We mini-
mize this at the source. Assumption extraction (C3) runs
at temperature=0. Code generation (C2) and regeneration
(C5) run at temperature=0.2 (RQ3 baselines likewise at
0.2). Each reported metric comes from a single scored
run per task and configuration. Raw model outputs for
every run are preserved in the artifact, and the bootstrap
confidence intervals in §VI-B and §VI-E quantify across-
task variability.



                     Jie “JW” Wu is an Assistant Professor in
                     the Department of Computer Science at Michi-
                     gan Technological University, USA, starting
                     Fall 2025. He was a Postdoctoral Fellow at
                     the University of British Columbia Okanagan,
                     Canada, from 2024 to 2025. He worked as a full-
                     time software developer for eight years at Snap
                     Inc. and Microsoft in USA. His recent research
                     centers on intent-aware software engineering,
                     developing AI-assisted techniques that infer,
                     communicate, and preserve developer intent to
enable the development of high-quality software.
