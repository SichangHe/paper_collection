                                            P OSTCOND B ENCH: Benchmarking Correctness and Completeness in
                                                            Formal Postcondition Inference

                                                                         Gehao Zhang and Juan Zhai
                                                               Manning College of Information and Computer Sciences
                                                                       University of Massachusetts Amherst
                                                                               Amherst, MA, USA
                                                                      {gehaozhang,juanzhai}@umass.edu


                                                              Abstract                          As a result, a long line of work has studied the
                                            Formal postconditions precisely characterize        automatic generation of specifications from source
arXiv:2605.03356v1 [cs.SE] 5 May 2026




                                            program behavior and support debugging, test-       code and natural-language (NL) artifacts, aiming to
                                            ing, and verification, but writing them requires    reduce the cost and expertise required for writing
                                            substantial expertise and effort. This has moti-    specifications (Goffi et al., 2016; Blasi et al., 2018;
                                            vated recent work on automatically generating       Zhai et al., 2020; Zhang et al., 2020; Xie et al.,
                                            postconditions from code and natural-language       2022; Pandita et al., 2012).
                                            artifacts using large language models (LLMs).          Large language models (LLMs) have signifi-
                                            However, evaluation remains a key bottleneck.
                                                                                                cantly improved generative capabilities for soft-
                                            Existing benchmarks primarily emphasize cor-
                                            rectness under limited evaluation settings, often   ware engineering tasks, including code generation
                                            relying on surface-form matching or manual as-      and testing (Chen et al., 2021; Islam et al., 2024;
                                            sessment on small or synthetic datasets.            Xue et al., 2024). Several studies have shown that
                                            We introduce P OSTCOND B ENCH, a multilin-          LLMs can also generate method-level postcondi-
                                            gual benchmark for evaluating method-level          tions directly from code or NL descriptions (Xie
                                            postcondition generation from real-world soft-      et al., 2025; Endres et al., 2024; Ma et al., 2025).
                                            ware. P OSTCOND B ENCH comprises 420                However, how to reliably evaluate generated post-
                                            Python and Java tasks drawn from 121 open-          conditions remains an open challenge.
                                            source projects, each paired with a high-quality       Most existing automatic evaluations focus on
                                            ground-truth postcondition set constructed with
                                                                                                correctness. Under sufficient test inputs, a postcon-
                                            expert involvement. To enable automatic evalu-
                                            ation, P OSTCOND B ENCH provides a runnable         dition is deemed correct if it is never violated when
                                            execution environment and operationalizes           executed against a correct implementation (Zhai
                                            completeness via defect discrimination: a post-     et al., 2020; Endres et al., 2024). Correctness alone
                                            condition set is more complete if it is violated    is insufficient as a correct postcondition set can
                                            by more defective implementations while re-         still overlook important behavioral aspects of the
                                            maining satisfied on correct executions. Using      method, i.e., they can be incomplete.
                                            P OSTCOND B ENCH, we formulate three gener-
                                                                                                   Evaluating completeness is fundamentally dif-
                                            ation settings and evaluate five SOTA LLMs.
                                            Our results reveal a substantial gap between        ficult because there is no single canonical spec-
                                            correctness and completeness, and show that         ification. The same behavioral property can of-
                                            repository-level dependencies and method com-       ten be expressed by many syntactically different
                                            plexity exacerbate this gap.                        but semantically equivalent postconditions (Endres
                                                                                                et al., 2024; Xie et al., 2025). This diversity makes
                                        1   Introduction
                                                                                                matching against a fixed ground truth, e.g., via
                                        A formal specification expresses the properties         string or AST similarity, brittle and prone to penal-
                                        that a program is expected to satisfy (Lamsweerde,      izing semantically correct specifications. Conse-
                                        2000). By precisely characterizing program behav-       quently, prior work has largely relied on manual
                                        ior, specifications play a central role in debugging,   assessment for evaluating completeness (Xie et al.,
                                        testing, and verification. Despite their importance,    2025; Zhai et al., 2020; Ma et al., 2025) (exam-
                                        formal specifications are scarce in real-world soft-    ples in Figure 11). Existing attempts at automatic
                                        ware, as writing them is time-consuming, error-         completeness evaluation remain limited. For in-
                                        prone, and requires substantial expertise (Lam-         stance, Endres et al. (2024) propose a completeness
                                        sweerde, 2000; Snook, 2001; Henkel et al., 2008).       metric, but evaluate it only on HumanEval+ (Liu
et al., 2023), a small dataset of standalone tiny             dency analysis and method size (MLOC).
Python programs. To date, there is no benchmark
that simultaneously provides (i) multilingual, real-        • An automatic evaluation platform that sup-
project-derived tasks, (ii) high-quality ground-truth         ports both correctness and completeness,
postconditions, and (iii) automatic support for cor-          with completeness measured via defect-
rectness and completeness evaluation.                         discriminative power.
   We present P OSTCOND B ENCH, a multilingual
                                                            • Extensive evaluation of five SOTA LLMs on
benchmark for evaluating the correctness and
                                                              three generation tasks reveals a substantial gap
completeness of method-level postconditions, a
                                                              between correctness and completeness, and
widely used form of formal specification that con-
                                                              shows that repository-level dependencies and
strains program states after method execution (Lam-
                                                              method complexity further widen this gap.
sweerde, 2000). P OSTCOND B ENCH comprises 420
postcondition generation tasks in Python and Java,      2    Background and Related Work
drawn from 121 diverse and popular open-source
projects. Each task is paired with a comprehen-         Prior work on specification generation includes
sive, high-quality postcondition set constructed        static analysis, dynamic analysis, and data-driven
via a semi-automated pipeline with domain-expert        approaches. Static techniques infer specifications
involvement. Moreover, P OSTCOND B ENCH pro-            from program structure, often providing soundness
vides a runnable execution environment with abun-       guarantees but struggling with scalability and pre-
dant context and tests, together with code-coverage     cision (Chen et al., 2016; Shoham et al., 2007;
analysis to ensure sufficiently exercised executions.   Flanagan and Leino, 2001). Dynamic approaches
   Crucially, P OSTCOND B ENCH operationalizes          learn likely specifications from execution traces,
completeness via defect discrimination: a post-         but their effectiveness depends heavily on test cov-
condition set is more complete if it distinguishes      erage (Ernst et al., 2001; Nimmer and Ernst, 2002).
more defective implementations from the reference       Repository-mining methods exploit recurring pat-
set while remaining satisfied on correct executions.    terns across large codebases, yet are sensitive to
This formulation enables automatic computation          repository quality and consistency (Ramanathan
without relying on brittle equivalence checking         et al., 2007; Nguyen et al., 2014).
against a single canonical specification.                  Recently, LLMs have been applied to generate
   Using P OSTCOND B ENCH, we formulate three           formal specifications from NL and/or code (Kreber
postcondition generation tasks and evaluate five        and Hahn, 2021; Cosler et al., 2023; Endres et al.,
state-of-the-art (SOTA) LLMs. Our results show          2024; Xie et al., 2025). While much of this work
that completeness remains challenging even for          focuses on temporal properties such as linear tem-
strong models (e.g., at most 17% in Python and          poral logic (LTL), recent studies demonstrate the
43% in Java for GPT-5), and that there is a substan-    promise of LLMs for generating method-level post-
tial gap between being correct and being complete.      conditions. However, evaluations are conducted on
We further analyze common causes of incorrect           small, standalone programs, limiting their ability
postconditions and the behavioral aspects most fre-     to reflect real-world software complexity.
quently overlooked by incomplete ones, highlight-          Evaluating generated specifications remains dif-
ing concrete directions for future research.            ficult because there is no single canonical “correct
   Our main contributions are:                          and complete” specification: multiple formulations
                                                        may be semantically valid yet differ substantially
   • P OSTCOND B ENCH, a multilingual bench-            in behavioral coverage (Endres et al., 2024; Xie
     mark of 420 Python/Java method-level post-         et al., 2025). As a result, prior work frequently
     condition generation tasks from 121 real-          relies on manual evaluation or restricts attention to
     world repositories, with high-quality ground-      tasks with well-defined ground truths (Zhai et al.,
     truth postconditions. Unlike prior bench-          2020; Kreber and Hahn, 2021).
     marks based on standalone programs, P OST-            Automatic evaluation of completeness has re-
     COND B ENCH captures repository-level con-         ceived limited attention. Endres et al. (2024) ex-
     text, including inter-method dependencies and      plore completeness checking for postconditions,
     non-trivial method complexity. We quanti-          but is limited to a small, Python-only dataset of
     tatively characterize these factors via depen-     standalone programs. Existing benchmarks rarely
capture repository-level code, cross-language di-         This dataset is designed for flexibility and
versity, or the gap between test-based correctness     broad applicability, with a primary focus on spec-
and true behavioral completeness.                      ification generation. For generation from NL,
   In contrast, P OSTCOND B ENCH provides a multi-     we use xgenFromNL = (sig, nl, T , M, P); for in-
lingual, repository-level benchmark with automat-      ference from implementations, xgenFromCode =
ically evaluable ground-truth postconditions. By       (sig, impl, T , M, P). Beyond specification tasks,
combining test-based validation with mutant-based      the dataset also enables applications such as code
completeness checking, it enables systematic mea-      generation using xcode = (sig, nl, impl, T , P),
surement of both correctness and completeness in       which supports workflows that require grounding
realistic software settings.                           code synthesis in developer intent.

3     Methodology                                      3.2     Dataset Construction Pipeline
                                                       We construct P OSTCOND B ENCH through a multi-
3.1    Benchmark Overview
                                                       step pipeline, illustrated in Figure 2.
Our benchmark targets formal postcondition infer-
ence, evaluating whether approaches can generate       3.2.1    Target Method Selection
precise and comprehensive postconditions from NL       We select candidate target methods from open-
descriptions and/or code implementations. We con-      source repositories, requiring runnable environ-
struct a multilingual, repository-level dataset with   ments and methods with adequate documentation,
automated evaluation capabilities. Formally, each      non-trivial complexity, and high test coverage.
P OSTCOND B ENCH instance is a tuple that captures
a method, its documentation, implementation, and       Repository Selection. We mine popular and di-
evaluation artifacts: x = ⟨sig, nl, impl, T , M, P⟩    verse GitHub repositories: for Python/Java, we
where sig is the method signature; nl, the NL de-      retrieve repos that (1) use a top-200 frequent tag,
scription; impl, the code implementation; T , a set    (2) are ≤ 20 MB, and (3) have a permissive license,
of test cases for correctness evaluation; M, a set     then keep the top 5,000 most-starred per language.
of implementation mutants for completeness evalu-      These sets cover all top-200 tags, ensuring broad
ation; and P, a set of ground-truth postconditions.    topical diversity.
Figure 1 shows a representative instance example
                                                       Automated Environment Setup. To enable test-
from joowani/binarytree (Joowani, 2022).
                                                       ing and coverage, each repository must run lo-
   Our postconditions are written in widely adopted    cally with tests passing and provide a cover-
formats, Java Modeling Language (JML (Leav-            age report (e.g., JaCoCo (jacoco, 2025), pytest-
ens et al., 2008)) for Java and icontract (Parquery,   cov (pytest-dev, 2025)). To scale the otherwise
2025) for Python. Unlike Endres et al. (2024),         labor-intensive setup (e.g., Pan et al. (2025) reports
which uses native assertion statements as postcon-     over 200 hours spent on setup), we adopt an LLM-
ditions, and Xie et al. (2025), which uses a custom-   driven loop: starting from a clean machine with
defined format, the postcondition languages/frame-     dependency managers (e.g., Poetry (python-poetry,
works used here are mature and more expressive.        2026), Maven (Miller et al., 2010)), our module
   Our postconditions capture intra- and inter-        checks requirements and, upon failure, queries an
class dependencies, and preserve pre-state             LLM (gpt-o4-mini) to propose edits to core con-
information. For example, the postcondition            fig files (e.g., pyproject.toml, pom.xml), applies
Arrays.deepEquals(\old(this.items()),                  them, and iterates for a bounded number of rounds.
\result.items()) uses \old(this.items())               Out of 10,000 repositories, 941 are successfully
to preserve the value of this.items() prior to         set up (9.4%), slightly better than SWE-agent (Hu
method execution. Further, JML provides full           et al., 2025; Yang et al., 2024).
support for logical connectives (implication,
equivalence, and inequivalence; written as ⇒, ⇔,       Method Parsing and Filtering. We parse meth-
and ̸⇔) While existing research highlights that        ods from the AST (Latif et al., 2023), align cov-
these logical connectives improve writing and          erage reports to obtain per-method line coverage,
understanding (Brown, 2024; Baron et al., 2024),       and retain methods that satisfy: ❶ Comment Qual-
Endres et al. (2024) and Xie et al. (2025) do not      ity: a comment with >15 English words (and we
provide sufficient support for them.                   manually remove obvious mismatches); ❷ Code
        01    def get_parent(root: Optional[Node], child: Optional[Node]) -> Optional[Node]:
                                                                                                            ...
                                         (a) Method signature                                          41
                                                                                                       42
                                                                                                            -
                                                                                                            +
                                                                                                                  if child is None:
                                                                                                                  if child is not None: # buggy
                                                                                                       43            return None...
        11         """Search the binary tree and return the parent of given child...

                                     (b) Natural language comment                                                       (e) Mutants used for completeness evaluation
        21         if child is None:                                                              51    @icontract.ensure(
        22             return None...                                                             52        lambda result:
        23         stack: List[Optional[Node]] = [root]                                           53            result is None or isinstance(result, Node))
        24         while stack:...                                                                54    @icontract.ensure(
                                                                                                  55        lambda result, child:
                                      (c) Method implementation                                   56
                                                                                                  57
                                                                                                                not child is None or result is None)
                                                                                                        @icontract.ensure(
                                                                                                  58        lambda result, root, child:
             31   def test_get_parent_utility_function() -> None:                                 69            result is (None if root is None or child is None
             32       root = Node(0)...                                                           70                else next((node for node in root.levelorder
             33       assert get_parent(root, root.left.left) == root.left...                     71                    if node.left is child or node.right is child), None,)))

                             (d) Test cases used for correctness evaluation                                                     (f) Ground-truth postconditions

Figure 1: An example instance from P OSTCOND B ENCH, illustrating the components of a benchmark instance. The
instance corresponds to the target method get_parent.

        Method Selection                          Mutant Generation                             Postcond. Validation                                 PostCondBench
                    Repository                     Operator-/LLM-                                            Correctness Check                               Target Method
                                                   based Mutation Mutants
                   Comment Quality
                                                                                                            Completeness Check                                    Signature
                   Code Complexity
                   Code Coverage                                                                                   (Only if Correct)                              NL Comment
                                                                                                                                                                  Implementation
                  Method
                                                  Postcond. Generation                                                                                            Mutants
                      Signature
                                                                                                                                                                  Ground Truth
                      NL Comment                                                                                  No                         Yes                  Postcond.
                                                                                                                           Postcond. Set
                      Implementation
                                                                                                                            Complete?
                      Test Cases                                                                                                                             Postcond. Eval.
                      Code Context                     LLM-based              Candidate        Target Expert                                                 Pipeline
                                                       Generator              Postcond.         Refinement


                                                   Figure 2: Overall workflow of P OSTCOND B ENCH.


Complexity: at least 15 lines of code or cyclomatic                                               we use an LLM-based mutation strategy. We parse
complexity (McCabe, 1976) ≥ 3; ❸ Code Cover-                                                      the AST to locate lines that define conditions in
age: ≥ 90% line coverage. We exclude methods                                                      if, while, and do statements, loop headers in
that throw exceptions under normal execution. This                                                for statements, and method calls. We replace
yields 1,030 Python and 1,476 Java methods.                                                       each target line with a placeholder and prompt
                                                                                                  gpt-4o-mini to generate an alternative line that
3.2.2   Mutant Generation                                                                         introduces a defect.
We generate mutants for each selected method fol-                                                    We discard mutants that still pass all tests and
lowing mutation-testing principles, which intro-                                                  remove those that throw exceptions under normal
duce small, controlled perturbations that approx-                                                 execution, to ensure postconditions are exercised.
imate realistic bugs. This supports completeness                                                  We retain only methods with at least five valid mu-
evaluation: a complete postcondition set should                                                   tants. This process yields 999 Python methods
be violated when the method runs on a defective                                                   and 1,431 Java methods, with an average of 24.8
implementation. We use operator-based mutation                                                    mutants per method.
and LLM-based mutation, and keep only defective
mutants that fail the original test suite.                                                        3.2.3            Postcondition Generation

Operator-based Mutation. We apply a single,                                                       We use an LLM to draft postcondition sets for each
localized syntactic transformation to the original                                                method, reducing manual effort in ground truth con-
method body (e.g., replacing a return value with                                                  struction. The model is given (i) the target method,
None, modifying conditional operators, or remov-                                                  (ii) repository code, and (iii) a list of mutants, and
ing void method calls). For Python, we reuse mu-                                                  is asked to propose postconditions that hold for the
tation operators from Mutmut (Hovmöller, 2016).                                                   original code but fail for defective mutants.
For Java, we reproduce the default mutation opera-                                                   We use gpt-5-mini with reasoning enabled.
tors from PIT (Coles et al., 2016).                                                               The prompt includes the method and, for each mu-
                                                                                                  tant, a line-by-line diff. We provide repository con-
LLM-based Mutation. Operator-based mutation                                                       text by uploading a zip archive and using OpenAI’s
is efficient but limited in diversity and coupling                                                code interpreter tool (OpenAI, 2023) to access rel-
strength (Wang et al., 2024). To complement it,                                                   evant files.
3.2.4 Postcondition Validation                              and stable evaluation on completeness (see Ap-
We validate each postcondition set along two axes:          pendix F).
correctness on the original implementation and              3.2.5 Expert Refinement and Finalization
completeness against buggy mutants. A set is cor-
                                                            If the LLM-generated postcondition set is not bug-
rect if the original method satisfies it across the
                                                            complete, two domain experts refine it by inspect-
provided tests; it is complete if it also distinguishes
                                                            ing the method, repository context, and mutants,
every generated mutant.
                                                            and re-running validation until bug-completeness is
Correctness. A postcondition set is correct if a            reached; disagreements are resolved by consensus.
correct implementation satisfies it for all (legal) in-     Each expert has over five years of programming
puts. We treat the developer test suite as the input        experience and more than one year of experience
distribution and require high test quality (line cov-       with formal specifications. If the generated set is
erage ≥ 90%). For a target method m and a post-             already bug-complete, we adopt it as the ground
condition set p, we instrument m with p and run             truth. We exclude methods (or specific mutants)
the test suite, obtaining eval(m, p) ∈ {−1, 0, 1}:          that require unsupported specification constructs
eval(m, p) == 1 iff all tests pass and all postcondi-       or remain unkillable under the available tests. All
tions hold; eval(m, p) == 0 iff any postcondition           removals are reported in the Appendix H. Most of
is violated; and eval(m, p) == −1 iff the run fails         these exclusions arise from representational limits
due to other exceptions. We define correctness as           of the underlying specification frameworks.

  corr(m, p) == T rue ⇐⇒ eval(m, p) == 1                    Benchmark Finalization. From 999 Python and
                                                            1,431 Java methods with sufficient mutants, we
 Our evaluation of correctness relies on test suites        select a diverse subset via farthest-first traver-
for the execution distribution. To reduce noise from        sal (Rosenkrantz et al., 1977) within each language,
weak or sparse test suites, we filter tasks by test         using cosine distance over CodeBERT (Feng
coverage and retain only methods with high line             et al., 2020) embeddings of method headers. We
coverage. Although high code coverage does not              then interleave automated generation with ex-
necessarily imply high test quality (e.g., assertions       pert refinement and filtering, yielding P OSTCOND -
may be weak and corner cases may remain under-              B ENCH with 210 methods per language, each with
tested), which can lead to optimistic estimates in          a bug-complete postcondition set.
dynamic evaluation, we expect this criterion to pref-          As shown in Table 1, methods in P OSTCOND -
erentially select tasks with relatively stronger test       B ENCH exhibit non-trivial size and complexity,
suites in practice. The final benchmark achieves an         with rich test coverage and multiple ground-truth
average line coverage of 99%.                               postconditions per method, reflecting realistic
                                                            repository-level scenarios.
Completeness. Correctness alone can be vacu-
ous; a postcondition set may pass tests yet fail to         Table 1: Statistics of P OSTCOND B ENCH for Python and
capture essential behavior. We assess complete-             Java. All metrics are reported as method-level averages,
ness via mutation testing. For each method m, we            except for the number of methods and repositories.
generate a mutant set {b1 , . . . , bq } (Section 3.2.2).
                                                                         Statistic          Python     Java
For a correct postcondition set p, we say p kills
mutant bh if eval(bh , p) == 0. A postcondition set                      Methods             210        210
                                                                       Repositories           61         60
is bug-complete if it is correct and kills all mutants:           Comment Word Length        44.6       46.9
                                                                        Test Cases           27.4       40.0
         comp(m, p) == T rue ⇐⇒                                       Line Coverage         98.8%      99.3%
                     " q                   #                          Lines of Code          30.4       30.6
                                                                  Cyclomatic Complexity       5.0        5.2
                      ^
   eval(m, p) == 1 ∧     eval(bh , p) == 0                               # Mutant            26.6       21.9
                           h=1                                       # Postcondition          3.6        5.5

   This mutation-based completeness is an opera-
tional proxy for behavioral coverage rather than
                                                            4   Experimental Setup
a definitive measure of semantic completeness.
Our mutation approach supports sufficient mutant            For each target method and each LLM, we eval-
quality and diversity, leading to a comprehensive           uate postcondition generation under three input
settings. Under each setting, we independently                                           Method-level correctness completeness gap
                                                                                       1.0
sample 5 candidate postcondition sets. Each candi-




                                                           Gap (Corr_rate Comp_rate)
date is evaluated for test-based correctness and bug-                                  0.8
completeness. Unless otherwise stated, we report
single-sample (@1) results in the main paper and                                       0.6
defer multi-sample (@k) results to the appendix.
                                                                                       0.4
Input Settings. We evaluate postcondition gen-
                                                                                       0.2
eration under three input settings: ❶ Code-
only (C2P), which provides only the method im-                                         0.0
plementation; ❷ NL-only (N2P), which provides                                                C2P (Code-only) N2P (NL-only) F2P (NL + Code)
                                                                                                            Input Setting
only NL comments; and ❸ Code+NL (F2P), which
provides both. These settings allow us to study         Figure 3: Distribution of method-level correct-
how different input modalities affect correctness,      ness–completeness gaps under different input settings.
completeness, and their discrepancy.                    For each method m, the gap is computed as ∆(m) =
                                                        corr_rate(m) − comp_rate(m), where corr_rate and
Models. We evaluate 5 SOTA LLMs, cover-                 comp_rate denote the fraction of generated postcondi-
ing proprietary and open-weight families: GPT-          tion sets that are test-correct and complete, respectively.
5 (OpenAI, 2025), Claude-4.5 (Sonnet) (Anthropic,       Each violin aggregates gap values across methods for
2025), LLaMA-4 (Maverick) (AI, 2025), Qwen3-            which at least one test-correct postcondition is gener-
32B (Yang et al., 2025), and Gemma-3-27B (Mes-          ated; methods with Corr@k = 0 are excluded. Horizon-
                                                        tal lines indicate the 25th, 50th, and 75th percentiles,
nard et al., 2024). Details are in Appendix D.1.
                                                        while dots denote the mean.
Evaluation Metrics. We report Corr@k and
Comp@k, which assess that when we generate k
postcondition sets for a method independently, the      Comp@1/Corr@1. Across models, ∆@1 is
expectation that at least one generation result is      large (0.063–0.423) and ρ@1 is below 0.5 for most
correct/complete; full details are in Appendix D.3.     models, indicating fewer than half of test-correct
                                                        outputs are complete. Notably, higher Corr@1 can
Evaluation Protocol. For each model, input set-         coincide with a larger gap (e.g., Claude-4.5).
ting, and method, we evaluate generated postcon-           Increasing the sample budget (i.e., increasing k
ditions using the metrics above. We report model-       in Corr/Comp@k metrics) improves both correct-
level aggregates (e.g., Corr@1, Comp@1) in tables       ness and completeness, but does not remove the
and method-level gap distributions in violin plots.     gap between them. For Corr@k/Comp@k, GPT-5
                                                        improves from 0.483/0.255 at @1 to 0.802/0.446 at
5     Results                                           @5, while Claude-4.5 improves from 0.629/0.207
We now present experimental results on P OST-           at @1 to 0.822/0.292 at @5. Additional sampling
COND B ENCH , covering overall performance, the         increases the chance of obtaining a usable specifica-
relationship between correctness and completeness,      tion. However, completeness still lags substantially
the effect of different input modalities, and fine-     behind correctness.
grained analyses of model failures.                        Figure 3 analyzes method-level gaps, computed
                                                        as ∆(m) = corr_rate(m) − comp_rate(m) over
5.1    How Large Is the Gap Between                     multiple generations. We focus on methods with
       Correctness and Completeness?                    Corr@k > 0 (excluding Corr@k = 0) to isolate
We evaluate LLM-generated postcondition sets un-        incompleteness after correctness is achieved. The
der both single-sample and multi-sample settings.       distribution is broad and right-skewed: the median
Table 2 reports Corr@k and Comp@k, aggregated           gap is consistently positive (∼0.2) and the upper
across languages and input settings. Across all k,      quartile reaches roughly 0.6 to 0.8, showing the gap
Claude-4.5 achieves the highest correctness, while      is widespread rather than driven by a few outliers.
GPT-5 achieves the strongest completeness.                 Input modality affects the severity of the gap but
  To quantify this discrepancy, we measure the          not its existence. All settings exhibit sizable gaps;
absolute gap ∆@1 = Corr@1 − Comp@1                      even F2P has median ∼0.2 with a non-trivial tail
and the conditional completeness rate ρ@1 =             above 0.5. The gap is most pronounced under N2P,
Table 2: Postcondition generation performance of LLMs. We report Corr@k, Comp@k, ∆@k, and Comp/Corr
for k ∈ {1, 3, 5}, where Corr@k indicates the expectation that at least one of the k generated postcondition sets is
test-correct and Comp@k indicates for at least one is complete. Results are aggregated across input settings and
programming languages.

                                 @1                               @3                                @5
 Model                                    Comp/                            Comp/                             Comp/
                 Corr    Comp         ∆           Corr    Comp         ∆            Corr    Comp         ∆
                                           Corr                             Corr                              Corr
 GPT-5           0.483   0.255    0.227   0.529   0.714   0.386    0.329   0.540    0.802   0.446    0.356   0.556
 Claude-4.5      0.629   0.207    0.423   0.329   0.777   0.268    0.509   0.345    0.822   0.292    0.530   0.355
 LLaMA-4         0.214   0.094    0.120   0.441   0.336   0.128    0.209   0.379    0.395   0.144    0.251   0.365
 Qwen3-32B       0.118   0.055    0.063   0.466   0.189   0.080    0.109   0.423    0.229   0.093    0.136   0.406
 Gemma-3-27B     0.110   0.044    0.066   0.401   0.171   0.058    0.113   0.339    0.204   0.064    0.140   0.315



with the largest median and widest spread (many             insufficient understanding of the boundary between
methods above 0.6, extremes near 1.0). C2P and              pre-state and post-state.
F2P are more concentrated; F2P slightly reduces                To test whether this failure mode is actionable,
the upper tail compared to C2P, but the two remain          we add a brief grammar-guidance block to the F2P
close overall, suggesting code provides most of the         prompt, summarized from the official icontract and
constraining signal for completeness.                       JML documentation, including an explanation of
                                                            the specification language / API in use, with brief
  Correctness does not reliably imply com-                  examples. We test GPT-5 and Claude-4.5. Table 11
  pleteness: large, systematic correctness–                 shows that both correctness and completeness im-
  completeness gaps persist across methods, in-             prove noticeably (e.g., 0.629 → 0.814 for Claude-
  put settings, and sample budgets. NL-derived              4.5 Corr@1, and 0.207 → 0.283 for Comp@1).
  postconditions exhibit greater variance and               However, the gap between correctness and com-
  heavier upper tails                                       pleteness remains large. Our claim still holds: even
                                                            after these improvements, completeness remains
                                                            challenging even for state-of-the-art models, and a
5.2   What Are the Major Failure Modes of
                                                            large correctness–completeness gap is retained.
      Incorrect Postconditions?
To understand why LLMs produce invalid spec-                Semantic Overreach (34%). This error arises
ifications, we analyze failure modes of incorrect           when LLMs enforce behaviors unsupported by the
postconditions. We sample 50 incorrect postcondi-           implementation or documentation. For example,
tion sets from GPT-5 and Claude-4.5; for each set,          Figure 9 (Appendix) shows cases where LLMs for-
we select one postcondition that triggers the failure       malize non-existent semantics.
and manually label its primary cause.                       Other Low-frequency Issues (12%). The re-
                                                            maining cases include basic syntactic mistakes
Specification Language / API Misuse (54%).
                                                            such as mismatched brackets (6%) and null
Most failures stem from incorrect contract syntax
                                                            dereferences (6%), where postconditions access
or framework APIs (54%), leading to compilation/-
                                                            None/null values without proper guards.
type errors or runtime contract violations.
   Note that many of these misuses are not superfi-
                                                              Incorrect postconditions are primarily caused
cial syntax mistakes. More than half of Java mis-
                                                              by specification-language misuse (54%), indi-
takes in this category are misusing post-state vari-
                                                              cating that improved model awareness of con-
ables in \old(·). In JML, the \old(·) is used for
                                                              tract syntax and APIs could eliminate a large
snapshotting the value of the inputted expression
                                                              fraction of failures.
at the pre-state. Expression that input to \old(·)
should only rely on variables that existed in the
pre-state. However, as an example in Figure 4,              5.3    Which Behaviors Are Missed by Correct
the generated postcondition uses entry in \old(·),                 but Incomplete Postconditions?
while entry is a temporary variable that is created         We study postcondition sets that are test-correct
when calling the allMatch(·) API in the post-state.         on the reference implementation but fail to kill at
Rather than merely a syntax error, this highlights an       least one mutant, revealing missing behavioral con-
01 //@ ensures !model.containsKey("g") || model.get("g").entrySet()       11 //@ ensures !model.containsKey("g") || model.get("g").entrySet()
       .stream().allMatch(entry -> entry.getValue() ==                           .stream().allMatch(entry -> entry.getValue() ==
       \old(model.get("g").get(entry.getKey())));                                \old(Map.copyOf(model)).get("g").get(entry.getKey()));

                       (a) Incorrect postcondition                                           (b) Correct postcondition

Figure 4: An example of incorrect postconditions caused by LLMs’ misuse of specification languages or APIs, with
corrected versions shown on the right. Highlighted regions indicate key corrections.


straints. We focus on GPT-5 and Claude-4.5, and                          Table 3: Postcondition generation performance on non-
manually inspect 50 randomly sampled (postcondi-                         standalone (Dep.) and standalone (Solo.) methods. Dep.
                                                                         requires repository-specific dependencies, while Solo.
tion set, unkilled mutant) pairs.
                                                                         is runnable with only built-ins. Bold indicates the higher
                                                                         score within each comparison.
Under-specified Return Value Behavior (78%).
Most incompleteness arises from weak constraints                                Language        Group       Corr@1         Comp@1
on return values: postconditions often validate only                                              Dep.        0.181          0.035
                                                                                  Python
special cases, types, or coarse ranges, leaving core                                              Solo.       0.239          0.090
computation insufficiently specified. Consequently,                                               Dep.        0.410          0.188
                                                                                   Java
output-perturbing or logic-bypassing mutants go                                                   Solo.       0.488          0.316
undetected (Figure 8 in Appendix). Across the
sampled cases, missed return-value behaviors span
multiple return types: scalar or primitive-like val-                       Most incompleteness stems from weak con-
ues (34%), built-in collections of scalars (26%),                          straints on return values, often involving sim-
repository-defined types (14%), and third-party li-                        ple scalar outputs. This suggests that system-
brary types (4%). Notably, over one third of missed                        atic strengthening of return-value specifica-
cases involve simple scalar returns, indicating that                       tions, rather than handling complex structures,
incompleteness often stems from weak semantic                              could substantially improve completeness.
constraints rather than from output complexity.
                                                                         5.4    How Do Method Characteristics Affect
                                      def __init__(self, *, points):            Postcondition Quality?
 01     def __init__(self, *, points,... self._points = points
 02 -     super().__init__(points=points)
 03 +     super().__init__(points=None)...                               We analyze two method-level factors that affect
 11 @icontract.snapshot(lambda points: points, name="points")...
 12 @icontract.ensure(lambda OLD, self: self._points is OLD.points)
                                                                         postcondition generation: dependency complexity
 21 @icontract.ensure(lambda self, colors: self.colors is colors)        (standalone vs. non-standalone) and method length.
 22 @icontract.ensure(lambda self, n_x, ...
                                         No validation on self._points

                                                                         Dependency Complexity. Following prior
Figure 5: Example of a correct but incomplete post-                      work (Yu et al., 2024), we label a method as
condition set. Top: Target method with mutant                            standalone if it runs with only built-in types and
changes (“+”/“–”). Middle: Complete postconditions.
                                                                         standard libraries; otherwise it is non-standalone.
Bottom: Test-correct but incomplete postconditions.
                                                                         As shown in Table 3, when averaging across
                                                                         models and input settings, standalone methods
                                                                         consistently achieve higher scores. The stratified
Unconstrained Object State (16%). Incom-                                 results (Table 10 in Appendix) show this trend is
pleteness also stems from missing constraints                            robust: across 60 paired comparisons (2 metrics ×
on object state. As shown in Figure 5, while                             2 languages × 5 models × 3 settings), standalone
other fields are validated, the initialization of                        wins in 51 cases (85%). The gap is larger for
self._points remains unconstrained, allowing a                           completeness: average Comp@1 rises from 0.035
state-altering mutant to pass undetected.                                to 0.090 in Python (2.6×) and from 0.188 to
                                                                         0.316 in Java (1.7×), suggesting that external
Lack of Defensive Guards (6%). Some post-                                dependencies make it harder to produce sufficiently
conditions lack basic robustness, raising runtime                        constraining postconditions.
exceptions (e.g., dereferencing None) under mutant-
induced states rather than failing as specifications.                    Method Length. We bucket methods by lines
Adding simple defensive guards before attribute                          of code (LoC): [0, 20), [20, 40), and [40, ∞). As
access would correctly reject these mutants.                             shown in Figure 6, performance generally de-
                    GPT-5                 LLaMA-4               Gemma-3-27B                Mutant budget ablation. For each method, we
                    Claude-4.5            Qwen3-32B
                                                                                           randomly sample subsets containing 10%, 20%,
                    C2P                       N2P                       F2P
         0.6                                                                               . . . , 100% of the full mutant set and compute
Corr@1



         0.4                                                                               Comp@1. We observe a clear saturation pattern
         0.2                                                                               once ≥80% of mutants are included. For GPT-
                                                                                           5, mean Comp@1 decreases only slightly from
         0.4                                                                               0.2616 (80%) to 0.2585 (90%) and 0.2551 (100%),
Comp@1




         0.3
                                                                                           with absolute differences of ≈0.003. Claude-4.5
         0.2
         0.1                                                                               shows the same pattern (0.2120 → 0.2091 →
         0.0                                                                               0.2068) (see Table 8).
           [0,20)   [20,40)   [40, ) [0,20)   [20,40)   [40, ) [0,20)   [20,40)   [40, )
                    #LoC                      #LoC                      #LoC

 Figure 6: Corr@1 (top) and Comp@1 (bottom) across                                             Comp@1 meaningfully reflects mutation de-
 target methods grouped by lines of code (LoC).                                                sign, remaining stable under substantial pertur-
                                                                                               bations of operator sets and mutation budget.
                                                                                               This indicates that the benchmark is neither
 creases with LoC, and the drop is much steeper                                                dominated by a specific mutation family nor
 for completeness. For example, under C2P with                                                 overly sensitive to particular operator choices.
 Claude-4.5, Comp@1 falls from 0.388 to 0.206
 and 0.076 from short to medium and long meth-
 ods. Aggregated over models, languages, and input                                         6     Conclusion
 settings, the overall average score decreases from
 0.296 to 0.205 and then to 0.149 as LoC increases,                                        We presented P OSTCOND B ENCH, a multilingual
 confirming that longer methods pose a substantially                                       benchmark for evaluating method-level postcon-
 harder generation problem.                                                                ditions in real-world software.       P OSTCOND -
                                                                                           B ENCH provides high-quality ground-truth post-
     Method characteristics strongly affect postcon-                                       conditions and a runnable platform that evaluates
     dition generation: standalone methods are eas-                                        correctness with tests and completeness via de-
     ier than dependency-heavy ones, and longer                                            fect discrimination. Evaluating five SOTA LLMs
     methods degrade performance monotonically,                                            across three generation tasks reveals a persistent
     with completeness being especially sensitive.                                         gap between correctness and completeness. By
                                                                                           enabling reliable completeness evaluation, P OST-
                                                                                           COND B ENCH aims to support future work on gener-
 5.5           How Stable Is Completeness Under
                                                                                           ating more behaviorally complete postconditions.
               Mutant-Set Changes?
We provide ablations to analyze how mutation de-
sign affects completeness (details in Appendix F).
                                                                                           Limitations

 Operator-level ablation. Each language in-                                                We exclude methods (or specific mutants) that re-
 cludes 11 operator-based mutation types. We                                               quire unsupported specification constructs or re-
 remove each operator individually and compute                                             main unkillable under the available tests. It is
 Comp@1 (averaged across models). In Python,                                               possible that this exclusion introduces bias in the
 dropping any single operator changes Comp@1                                               P OSTCOND B ENCH evaluation of the affected be-
 by at most 0.004; in Java, most operators shift                                           haviors, such as iterator or concurrency behaviors.
 Comp@1 by ≤0.001 (see Table 9).                                                           However, filtering affects a minority of the sampled
                                                                                           methods. Most of these exclusions arise from rep-
 Mutation-strength ablation. We further vary                                               resentational limits of the underlying specification
 mutation “strength” by (i) randomly removing 5 of                                         frameworks (Appendix H). The exceptional be-
 the 11 operators and (ii) randomly removing 50%                                           haviors are also not in P OSTCOND B ENCH’s scope
 of LLM-based mutants (50 trials each). Across all                                         since we focus on normal postconditions (in con-
 models, the mean Comp@1 changes by less than                                              trast to exceptional postconditions). Besides, we
 4% relative to the full-mutant baseline, with stan-                                       restrict on methods with high code coverage due to
 dard deviation ≤0.004 in all settings (see Table 8).                                      the execution-based nature of our metrics.
Ethical Considerations                                     negations: Its complicated. In Proceedings of the
                                                           28th International Conference on Evaluation and As-
Data sources and licensing. Our benchmark is               sessment in Software Engineering, pages 303–312.
constructed from publicly available open-source
                                                         Arianna Blasi, Alberto Goffi, Konstantin Kuznetsov,
repositories. We only include projects with permis-        Alessandra Gorla, Michael D Ernst, Mauro Pezzè,
sive licenses and preserve attribution to the original     and Sergio Delgado Castellanos. 2018. Translating
authors and repositories. Any release of the bench-        code comments to procedure specifications. In Pro-
mark and derived artifacts should comply with the          ceedings of the 27th ACM SIGSOFT International
                                                           Symposium on Software Testing and Analysis, pages
licenses of the included projects.
                                                           242–253, Amsterdam, Netherlands. ACM.
Privacy and sensitive information. The bench-            Walter E. Brown. 2024. Implication for c++. WG21 Pa-
mark is derived from public code and related arti-         per P2971R2 P2971R2, ISO/IEC JTC1/SC22/WG21.
facts (e.g., tests and comments). The dataset un-
derwent end-to-end inspection during curation and        Junjie Chen, Yanwei Bai, Dan Hao, Lingming Zhang,
                                                           Lu Zhang, Bing Xie, and Hong Mei. 2016. Support-
validation. Across these inspections, we did not           ing oracle construction via static analysis. 2016 31st
observe privacy-related or sensitive information in        IEEE/ACM International Conference on Automated
the data intended for release.                             Software Engineering (ASE), pages 178–189.

Human involvement. Some parts of dataset cre-            Mark Chen, Jerry Tworek, Heewoo Jun, Qiming
ation and validation involve domain-expert partic-        Yuan, Henrique Ponde, Jared Kaplan, Harrison Ed-
                                                          wards, Yura Burda, Nicholas Joseph, Greg Brockman,
ipation (e.g., refining or verifying postconditions       Alex Ray, Raul Puri, Gretchen Krueger, Michael
and resolving ambiguities). The experts are invited;      Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin,
no public recruitment. Domain experts provide as-         Brooke Chan, Scott Gray, and 34 others. 2021. Eval-
sistance on a voluntary basis. While administrative       uating large language models trained on code. ArXiv,
                                                          abs/2107.03374.
contact information may be required to coordinate
participation, we did not collect such information       Henry Coles, Thomas Laurent, Christopher Henard,
as part of the dataset itself, did not use it beyond       Mike Papadakis, and Anthony Ventresque. 2016. Pit:
study administration, and it is not included in any        a practical mutation testing tool for java. In Proceed-
                                                           ings of the 25th international symposium on software
released artifacts.                                        testing and analysis, pages 449–452.
Acknowledgments                                          Matthias Cosler, Christopher Hahn, Daniel Men-
                                                          doza, Frederik Schmitt, and Caroline Trippel. 2023.
This paper uses AI writing assistance purely with         nl2spec: Interactively translating unstructured natu-
the language of the paper, which covers models            ral language to temporal logics with large language
used for paraphrasing or polishing the author’s           models. In International Conference on Computer
                                                          Aided Verification, pages 383–396. Springer.
original content, rather than for suggesting new
content.                                                 Madeline Endres, Sarah Fakhoury, Saikat Chakraborty,
                                                          and Shuvendu K Lahiri. 2024. Can large language
Data Availability                                         models transform natural language intent into formal
                                                          method postconditions? Proceedings of the ACM on
To follow the Open Science Policy and support             Software Engineering, 1(FSE):1889–1912.
reproducibility, we have released code about our
                                                         Michael D Ernst, Jake Cockrell, William G Griswold,
implementations and evaluations. All source code           and David Notkin. 2001. Dynamically discovering
and data used in our work can be found at https://         likely program invariants to support program evolu-
github.com/zhang-ge-hao/postcond-bench.                    tion. IEEE Transactions on Software Engineering,
                                                           27(2):99–123.

                                                         Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xi-
References                                                 aocheng Feng, Ming Gong, Linjun Shou, Bing Qin,
Meta AI. 2025. Gpt-4o mini: advancing cost-efficient       Ting Liu, Daxin Jiang, and 1 others. 2020. Codebert:
 intelligence. Meta.                                       A pre-trained model for programming and natural
                                                           languages. In Findings of the Association for Com-
Anthropic. 2025. Introducing claude sonnet 4.5. An-        putational Linguistics: EMNLP 2020, pages 1536–
  thropic.                                                 1547.

Aviad Baron, Ilai Granot, Ron Yosef, and Dror Feitel-    Cormac Flanagan and K. Rustan M. Leino. 2001. Hou-
  son. 2024. Understanding logical expressions with        dini, an annotation assistant for esc/java. In FME.
Alberto Goffi, Alessandra Gorla, Michael D Ernst, and     René Just, Darioush Jalali, Laura Inozemtseva,
  Mauro Pezzè. 2016. Automatic generation of oracles        Michael D Ernst, Reid Holmes, and Gordon Fraser.
  for exceptional behaviors. In Proceedings of the 25th     2014b. Are mutants a valid substitute for real faults
  International Symposium on Software Testing and           in software testing? In Proceedings of the 22nd ACM
  Analysis, pages 213–224. ACM.                             SIGSOFT international symposium on foundations
                                                            of software engineering, pages 654–665.
Johannes Henkel, Christoph Reichenbach, and Amer
  Diwan. 2008. Developing and debugging algebraic         Keon. 2025. algorithms: Minimal examples of data
  specifications for java classes. ACM Transactions on      structures and algorithms in python and other lan-
  Software Engineering and Methodology (TOSEM),             guages. https://github.com/keon/algorithms.
  17(3):1–37.                                               GitHub repository, accessed 2026-01-06.
                                                          Jens U Kreber and Christopher Hahn. 2021. Generating
Anders    Hovmöller.     2016.          Mutmut:              symbolic reasoning problems with transformer gans.
  a     python     mutation     testing  system.             arXiv preprint arXiv:2110.10054.
  https://kodare.net/2016/12/01/
  mutmut-a-python-mutation-testing-system.                Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
  html. Blog post on En kodare.                            Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gon-
                                                           zalez, Hao Zhang, and Ion Stoica. 2023. Efficient
Ruida Hu, Chao Peng, Junjielong Xu, Cuiyun Gao, and        memory management for large language model serv-
  1 others. 2025. Repo2run: Automated building ex-         ing with pagedattention. In Proceedings of the 29th
  ecutable environment for code repository at scale.       symposium on operating systems principles, pages
  In The Thirty-ninth Annual Conference on Neural          611–626.
  Information Processing Systems.
                                                          Axel van Lamsweerde. 2000. Formal specification: a
Md Ashraful Islam, Mohammed Eunus Ali, and                  roadmap. In Proceedings of the Conference on the
 Md Rizwan Parvez. 2024. Mapcoder: Multi-agent              Future of Software Engineering, pages 147–159.
 code generation for competitive problem solving. In
 Annual Meeting of the Association of Computational       Afshan Latif, Farooque Azam, Muhammad Waseem
 Linguistics 2024, pages 4912–4944. Association for         Anwar, and Amina Zafar. 2023. Comparison of lead-
 Computational Linguistics (ACL).                           ing language parsers–antlr, javacc, sablecc, tree-sitter,
                                                            yacc, bison. In 2023 13th International Conference
jacoco. 2025. JaCoCo: Java code coverage library.           on Software Technology and Engineering (ICSTE),
   https://github.com/jacoco/jacoco. GitHub                 pages 7–13. IEEE.
   repository.                                            Gary T Leavens, Erik Poll, Curtis Clifton, Yoonsik
                                                            Cheon, Clyde Ruby, David Cok, Peter Müller, Joseph
Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia          Kiniry, Patrice Chalin, Daniel M Zimmerman, and 1
  Yan, Tianjun Zhang, Sida Wang, Armando Solar-             others. 2008. Jml reference manual.
  Lezama, Koushik Sen, and Ion Stoica. 2024. Live-
  codebench: Holistic and contamination free eval-        Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Ling-
  uation of large language models for code. arXiv            ming Zhang. 2023. Is your code generated by chatgpt
  preprint arXiv:2403.07974.                                 really correct? rigorous evaluation of large language
                                                             models for code generation. Advances in Neural
jhy. 2025. jsoup: the java html parser, built for html       Information Processing Systems, 36:21558–21572.
   editing, cleaning, scraping, and xss safety. https:
   //github.com/jhy/jsoup/. GitHub repository, ac-        Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei
   cessed 2026-01-06.                                       Bu. 2025. Specgen: Automated generation of formal
                                                            program specifications via large language models. In
Carlos E Jimenez, John Yang, Alexander Wettig,              2025 IEEE/ACM 47th International Conference on
  Shunyu Yao, Kexin Pei, Ofir Press, and Karthik            Software Engineering (ICSE), pages 16–28. IEEE.
  Narasimhan. 2024. Swe-bench: Can language mod-
  els resolve real-world github issues? In 12th Inter-    Thomas J McCabe. 1976. A complexity measure. IEEE
  national Conference on Learning Representations,          Transactions on software Engineering, (4):308–320.
  ICLR 2024.                                              Gemma Team Thomas Mesnard, Cassidy Hardin,
                                                            Robert Dadashi, Surya Bhupatiraju, Shreya Pathak,
Joowani. 2022. binarytree: A python library for study-      L. Sifre, Morgane Riviere, Mihir Kale, J Christo-
  ing binary trees. https://github.com/joowani/             pher Love, Pouya Dehghani Tafti, L’eonard Hussenot,
  binarytree. GitHub repository, accessed 2026-01-          Aakanksha Chowdhery, Adam Roberts, Aditya
  06.                                                       Barua, Alex Botev, Alex Castro-Ros, Ambrose Slone,
                                                            Am’elie H’eliou, Andrea Tacchetti, and 88 others.
René Just, Darioush Jalali, and Michael D Ernst. 2014a.     2024. Gemma: Open models based on gemini re-
  Defects4j: A database of existing faults to enable        search and technology. ArXiv, abs/2403.08295.
  controlled testing studies for java programs. In Pro-
  ceedings of the 2014 international symposium on         Frederic P Miller, Agnes F Vandome, and John McBrew-
  software testing and analysis, pages 437–440.              ster. 2010. Apache Maven. Alpha Press.
Hoan Anh Nguyen, Robert Dyer, Tien N Nguyen, and           Bo Wang, Mingda Chen, Youfang Lin, Mike Papadakis,
  Hridesh Rajan. 2014. Mining preconditions of apis          and Jie M Zhang. 2024. An exploratory study on
  in large-scale code corpus. In Proceedings of the          using large language models for mutation testing.
  22nd ACM SIGSOFT International Symposium on                CoRR.
  Foundations of Software Engineering, pages 166–177.
  ACM.                                                     Danning Xie, Yitong Li, Mijung Kim, Hung Viet Pham,
                                                             Lin Tan, Xiangyu Zhang, and Michael W Godfrey.
Jeremy W Nimmer and Michael D Ernst. 2002. Au-               2022. Docter: documentation-guided fuzzing for
   tomatic generation of program specifications. ACM         testing deep learning api functions. In Proceedings
   SIGSOFT Software Engineering Notes, 27(4):229–            of the 31st ACM SIGSOFT International Symposium
   239.                                                      on Software Testing and Analysis, pages 176–188.

OpenAI. 2023.        Code interpreter. https:              Danning Xie, Byoungwoo Yoo, Nan Jiang, Mijung Kim,
  //platform.openai.com/docs/guides/                         Lin Tan, Xiangyu Zhang, and Judy S Lee. 2025.
  tools-code-interpreter. OpenAI API Docu-                   How effective are large language models in generat-
  mentation. Accessed: 2026-01-06.                           ing software specifications? In 2025 IEEE Interna-
                                                             tional Conference on Software Analysis, Evolution
OpenAI. 2025. Gpt-5 is here. OpenAI.                         and Reengineering (SANER), pages 1–12. IEEE.

Jiayi Pan, Xingyao Wang, Graham Neubig, Navdeep            Zhiyi Xue, Liangguo Li, Senyue Tian, Xiaohong Chen,
   Jaitly, Heng Ji, Alane Suhr, and Yizhe Zhang. 2025.       Pingping Li, Liangyu Chen, Tingting Jiang, and
   Training software engineering agents and verifiers        Min Zhang. 2024. Llm4fin: Fully automating llm-
   with SWE-gym. In Forty-second International Con-          powered test case generation for fintech software
   ference on Machine Learning.                              acceptance testing. In Proceedings of the 33rd ACM
                                                             SIGSOFT International Symposium on Software Test-
Rahul Pandita, Xusheng Xiao, Hao Zhong, Tao Xie,             ing and Analysis, pages 1643–1655.
  Stephen Oney, and Amit Paradkar. 2012. Inferring
  method specifications from natural language API de-      An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  scriptions. In Proceedings of the 34th International       Binyuan Hui, Bo Zheng, Bowen Yu, Chang
  Conference on Software Engineering, pages 815–825.         Gao, Chengen Huang, Chenxu Lv, and 1 others.
  IEEE Press.                                                2025. Qwen3 technical report. arXiv preprint
                                                             arXiv:2505.09388.
Parquery. 2025. icontract. GitHub repository.
                                                           John Yang, Carlos E Jimenez, Alexander Wettig, Kilian
Parquery AG. 2019.     icontract documentation:              Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir
  Async.   https://icontract.readthedocs.io/                 Press. 2024. Swe-agent: Agent-computer interfaces
  en/latest/async.html. Accessed: 2026-01-05.                enable automated software engineering. Advances in
                                                             Neural Information Processing Systems, 37:50528–
pytest-dev. 2025.  pytest-cov: Coverage plugin               50652.
  for pytest. https://github.com/pytest-dev/
                                                           Hao Yu, Bo Shen, Dezhi Ran, Jiaxin Zhang, Qi Zhang,
  pytest-cov. GitHub repository.
                                                             Yuchi Ma, Guangtai Liang, Ying Li, Qianxiang Wang,
python-poetry. 2026. Poetry: Python packaging                and Tao Xie. 2024. Codereval: A benchmark of prag-
  and dependency management made easy. https:                matic code generation with generative pre-trained
  //github.com/python-poetry/poetry. GitHub                  models. In Proceedings of the 46th IEEE/ACM Inter-
  repository.                                                national Conference on Software Engineering, pages
                                                             1–12.
Murali Krishna Ramanathan, Ananth Grama, and               Juan Zhai, Yu Shi, Minxue Pan, Guian Zhou, Yongxi-
 Suresh Jagannathan. 2007. Static specification in-          ang Liu, Chunrong Fang, Shiqing Ma, Lin Tan, and
 ference using predicate mining. In ACM SIGPLAN              Xiangyu Zhang. 2020. C2s: translating natural lan-
 Notices, pages 123–134. ACM.                                guage comments to formal program specifications.
                                                             In Proceedings of the 28th ACM Joint Meeting on
Daniel J Rosenkrantz, Richard E Stearns, and Philip M
                                                             European Software Engineering Conference and Sym-
  Lewis, II. 1977. An analysis of several heuristics for
                                                             posium on the Foundations of Software Engineering,
  the traveling salesman problem. SIAM journal on
                                                             pages 25–37.
  computing, 6(3):563–581.
                                                           Shiyu Zhang, Juan Zhai, Bu Lei, Wang Linzhang, and
Sharon Shoham, Eran Yahav, Stephen J. Fink, and              Xuandong Li. 2020. Automated geration of ltl speci-
  Marco Pistoia. 2007. Static specification mining us-       fications for smart home iot using natural language.
  ing automata-based abstractions. IEEE Transactions         In 2020 Design, Automation & Test in Europe Con-
  on Software Engineering, 34:651–666.                       ference & Exhibition (DATE). IEEE.
Colin Frank Snook. 2001. Exploring the barriers to
  formal specification. Ph.D. thesis, University of
  Southampton.
A     Discussion                                        2025), Claude-4.5 (Sonnet) (Anthropic, 2025),
                                                        LLaMA-4 (Maverick) (AI, 2025), Qwen3-32B
Insufficiency for Real Bugs. We use mutants
                                                        (Yang et al., 2025), Gemma-3-27B (Mesnard et al.,
rather than real bugs made in development to as-
                                                        2024). For GPT-5, we use the OpenAI batch
sess the completeness. The reason is that mutation
                                                        API. For Claude-4.5 and LLaMA-4, we use the
lets us generate many defective variants for the
                                                        batch inference pipeline in Amazon Bedrock. For
same method. For real bugs (Just et al., 2014a;
                                                        Qwen and Gemma models, we locally deploy Vllm
Jimenez et al., 2024), each fixed version is typi-
                                                        (Kwon et al., 2023) services for experiments. We
cally paired with a very limited number (usually
                                                        apply the reasoning mode for GPT-5 and Claude
only one) of corresponding buggy versions, which
                                                        4.5, setting reasoning.effort = "medium" for
makes it insufficient to assess how completely a
                                                        GPT-5 and thinking.budget_tokens = 2048 for
specification constrains the method’s behavior.
                                                        Claude 4.5. Besides the reasoning effort configura-
   Moreover, prior work shows that mutants can
                                                        tions, we follow each provider’s default configura-
effectively couple with real faults (Just et al.,
                                                        tions and use consistent prompts across models for
2014b). Therefore, although P OSTCOND B ENCH is
                                                        fair comparison.
designed to evaluate the quality of formal postcon-
ditions, the reported mutant discrimination can be       01 # Code Context
a prerequisite capability for downstream uses such       02 {code_context}
                                                         03 # Target Method
as verification and debugging.                           04 {target_method}
                                                         05 # Guideline
                                                         06 Above is the {Python|Java} code context and
B     Future Work                                           target method. You should generate {icontract|JML}
                                                            format postconditions ...
Live Benchmark against Data Leakage. “Live”
benchmarks are continuously updated with newer          Figure 7: Prompt template. The placeholders are shown
data, reducing the risk of data leakage (Jain et al.,   in green.
2024). They are often designed to support efficient
updates. For P OSTCOND B ENCH, most stages of
                                                        D.2   Prompt Construction
the construction pipeline are automated, and the
benchmark can be re-run on newly released reposi-       P OSTCOND B ENCH supports runnable reposito-
tories with limited manual effort; the expert effort    ries and automatic evaluation; we therefore for-
for maintaining a refreshed version is expected to      mulate postcondition generation as prompting an
be less than 50 hours per year. It is practical to      LLM with a target method plus its surround-
maintain a periodically refreshed benchmark.            ing context. All settings share the prompt tem-
                                                        plate in Figure 7, which contains two main
C     Comparison with Existing Work                     fields: {code_context} (in-file context) and
                                                        {target_method} (the method to validate).
Table 4 positions P OSTCOND B ENCH relative to
                                                           We instantiate three input settings:
prior work on postcondition generation. While
existing studies primarily propose generation ap-          • F2P. We provide the method signature, the
proaches and evaluate them under task-specific               NL method-level comment, and the full im-
datasets or execution settings, they do not release a        plementation in {target_method} (cf. Fig-
reusable benchmark with curated ground truths or             ure 1). We fill {code_context} with the
an explicit evaluation methodology for complete-             method-located file content to provide in-file
ness. P OSTCOND B ENCH fills this gap by provid-             context.
ing a benchmark that jointly supports multilingual,
repository-level programs, advanced postcondition          • C2P. We provide the method signature and
syntax, and automatic evaluation of both correct-            implementation in {target_method}, remov-
ness and completeness.                                       ing any code comments inside the implemen-
                                                             tation. We also remove all code comments
D     Experimental Setup                                     from {code_context}.
D.1    Models                                              • N2P. We provide the method signature
We chose five state-of-the-art large language mod-           and its NL method-level comment in
els (LLMs) for experiments: GPT-5 (OpenAI,                   {target_method}. In {code_context}, we
               Table 4: Comparison of evaluation features in Python/Java postcondition generation.

Work                         C2S (Zhai      Endres et al.   Endres et al.   SpecGen (Ma      Xie et al.   Ours
                            et al., 2020)   (2024) (Hu-       (2024)         et al., 2025)    (2025)
                                            manEval+)       (Defects4J)
Multi-Language                   ✗               ✗                 ✗              ✗             ✗          ✓
Repository-level                 ✓               ✗                 ✓              ✗             ✓          ✓
Ground Truths Included           ✗               ✗                 ✗              ✓             ✓          ✓
Advanced Spec. Syntax            ✓               ✗                 ✗              ✓             ✗          ✓
Auto. Completeness Eval.         ✗               ✓                 ✗              ✗             ✗          ✓
 Endres et al. (2024) report postcondition generation results under two benchmarks: HumanEval+ (Liu et al., 2023) and
Defects4J (Just et al., 2014a).


       keep the method-located file but remove               • Correctness–completeness gap. To quantify the
       method bodies, so the model can leverage dec-         discrepancy between correctness and completeness,
       larations and surrounding structure without           we define two complementary measures. The abso-
       seeing implementations.                               lute gap is defined as

These settings isolate the effects of code, com-                          ∆@k = Corr@k − Comp@k,                 (1)
ments, and their combination on correctness and
bug-completeness.                                            which captures the extent to which test-based cor-
                                                             rectness overestimates completeness. We also re-
D.3     Evaluation Metrics                                   port the conditional completeness rate,

We evaluate generated postconditions along two                                           Comp@k
                                                                               ρ@k =            ,                (2)
dimensions: correctness and completeness. Com-                                           Corr@k
pleteness is evaluated only for test-correct post-
condition sets; candidates that fail correctness are         measuring the fraction of test-correct postcondi-
treated as incomplete.                                       tions that are also complete. Unless otherwise spec-
                                                             ified, gap analyses in the main paper focus on @1,
Correctness. A generated postcondition set is                while multi-sample results are reported in the ap-
considered correct if, when instrumented into the            pendix.
original method, all postconditions in the set pass
all provided test cases. Test-based correctness re-
                                                             E     Correctness–Completeness Gap: Case
flects whether the generated specification is consis-              study
tent with observed program behaviors.                        Figure 8 gives concrete examples. For distance
                                                             (left), the correct-but-incomplete set mainly checks
Completeness. A generated postcondition set is               boundary/special cases (e.g., x==y) and the return
considered complete if it not only passes all test           type, yet fails to kill a mutant that initializes sum
cases, but also rejects all automatically generated          to one when x != y; the complete set additionally
mutants of the target method. Since mutants in-              checks the expected value (line 003), which rules
troduce buggy behaviors that should be ruled out             out the mutant. The Java example (right) shows
by a correct specification, completeness measures            a similar pattern: the correct-but-incomplete set
whether a postcondition set sufficiently constrains          includes a redundant constraint, while the complete
the method’s behavior. Completeness is evaluated             set adds a stricter condition beyond the special case.
only for test-correct postcondition sets; candidates
that fail correctness are treated as incomplete.             F     Ablation on Mutation Schemes
• @k aggregation. Let k denote the number of inde-
pendently generated postcondition sets for a given           F.1       False Discovery Rate Across Mutation
method. Corr@k indicates whether at least one of                       Schemes
the k generated postcondition sets is test-correct.          We ablate our two mutation schemes—rule-based
Comp@k indicates whether at least one of the k               and LLM-based—to assess their complementarity.
generated postcondition sets is both test-correct            Table 6 reports the false discovery rate (FDR) for
and complete.                                                each scheme. Concretely, for a given scheme S, we
Table 5: Postcondition generation evaluation results from Large Language Models. The bold font emphasizes the
highest-performing LLM for each metric within each language.

                                   C2P (Code-only)                             N2P (NL-only)                                F2P (NL + Code)

                         Corr       Comp                   Comp/      Corr     Comp                    Comp/      Corr        Comp                  Comp/
           Metric                              ∆@1                                         ∆@1                                           ∆@1
                         @1          @1                    Corr       @1        @1                     Corr       @1           @1                   Corr

         GPT-5           0.493      0.290      0.203       0.588      0.434    0.177       0.257       0.408      0.520       0.298      0.222      0.573
     Claude-4.5          0.645      0.234      0.411       0.362      0.593    0.150       0.443       0.253      0.650       0.237      0.413      0.364
     LLaMA-4             0.224      0.105      0.119       0.469      0.180    0.062       0.118       0.344      0.239       0.116      0.122      0.487
    Qwen3-32B            0.141      0.062      0.079       0.441      0.092    0.043       0.049       0.469      0.120       0.060      0.061      0.494
  Gemma-3-27B            0.117      0.054      0.063       0.459      0.097    0.026       0.071       0.266      0.117       0.053      0.064      0.453


 01 def distance(x,y):                                                        21   /** Returns true if any of the Element's child nodes should indent...
 02     """...calculates the (eulidean) distance between vector x and y...    22   static boolean hasChildBlocks(Element el) {
 03     result = ()                                                           23       Element child = el.firstElementChild();
 04 -   sum = 0                                                               24   -   for (int i = 0; i < maxScan && child != null; i++) {
 05 +   sum = 1                                                               25   +   for (int i = 0; i >= maxScan && child != null; i++) {
 06     for i in range(len(x)):                                               26           if (child.isBlock() || !child.tag.isKnownTag()) return true;
 07         result += (x[i] -y[i],)                                           27           child = child.nextElementSibling();
 08     for component in result:                                              28       }
 09         sum += component**2                                               29       return false;
 10     return math.sqrt(sum)                                                 30   }
 41   @icontract.ensure(lambda result: isinstance(result, float))
 42   @icontract.ensure(lambda result: result >= 0.0)
 43   @icontract.ensure(lambda x, y, result:                                  51 //@ ensures \result <==> el.children().stream().limit(maxScan).anyMatch(
 44       math.isclose(result, math.sqrt(                                            child -> child.isBlock() || !child.tag.isKnownTag());
 45           sum((x[i] - y[i]) ** 2 for i in range(len(x)))),                52 //@ ensures \result ==> el.firstElementChild() != null;
 46           rel_tol=1e-12, abs_tol=0.0))
 47   @icontract.ensure(lambda x, y, result: (x == y) == (result == 0.0))
 61 @icontract.ensure(lambda result: result >= 0)
                                                                              71 //@ ensures el.firstElementChild() == null ==> \result == false;
 62 @icontract.ensure(lambda result, x, y: (result == 0) == (x == y))
                                                                              72 //@ ensures \result == true ==> el.firstElementChild() != null;
 63 @icontract.ensure(lambda result: isinstance(result, float))



Figure 8: Left: A Python instance from keon/algorithms (Keon, 2025). Right: A Java instance from jhy/jsoup
(jhy, 2025). Top: Target methods. For each method, the “+” and “-” leading lines represent the differences from the
original code to an example mutant. Middle: Complete postcondition sets (both are GPT-5 generated from the F2P
task). Bottom: Correct but incomplete postcondition sets (Claude-4.5 generated from the F2P task). The green box
enclosed the key postcondition that make the set more complete.


first evaluate completeness using only mutants gen-                            F.2       Complementarity Under Scheme
erated by S and collect postcondition sets that are                                      Exclusion
classified as complete under this restricted mutant
                                                                               We further recompute Comp@1 after excluding ei-
set. We then re-evaluate these same postcondition
                                                                               ther all LLM-based mutants or all operator-based
sets on mutants from the other scheme S̄ and com-
                                                                               mutants. Table 7 shows that scores increase af-
pute the fraction that fail to kill all S̄-mutants; this
                                                                               ter removing either mutation family, indicating
fraction is the FDR. A higher FDR indicates that a
                                                                               that each family exposes defects the other does
single scheme is insufficient in isolation, and that
                                                                               not cover well. For example, when LLM-based
the other scheme contributes additional mutants
                                                                               mutants are excluded, Claude-4.5 increases from
that expose incompleteness.
                                                                               0.2068 to 0.2944; when operator-based mutants
                                                                               are excluded, LLaMA-4 increases from 0.0944 to
   As shown in Table 6, both schemes exhibit non-                              0.1281. This provides a direct complement to the
trivial FDRs, suggesting meaningful complemen-                                 FDR analysis above: high completeness requires
tarity. For example, the Avg row shows an FDR                                  handling both mutation families well.
of 0.206 for LLM-based mutation on Python–F2P,
and an FDR of 0.203 for rule-based mutation on                                 F.3       Mutant-Budget Stability
Java–N2P. In other words, if we rely on only one                               We also vary the overall mutant budget by ran-
mutation scheme, a noticeable fraction of postcon-                             domly sampling a fixed fraction of the full mutant
dition sets deemed “complete” would still be in-                               set for each method. As shown in Table 8, com-
complete and would be revealed by mutants from                                 pleteness approaches saturation as the budget in-
the other scheme.                                                              creases. Between 80%, 90%, and 100% of mutants,
                                                                               the mean Comp@1 changes only slightly for all
 Overall, rule- and LLM-based mutation comple-                                 five models, and the standard deviations are small
ment each other for completeness evaluation.                                   once the budget reaches 80% or above. This sug-
Table 6: Mutation FDR (False Discovery Rate) (↓) of different mutation schemes. I.e., if we only use one scheme
to identify the complete postconditions, the ratio of the discovered “complete” postcondition that cannot kill all
mutants from another scheme.

                                       Python                                                Java
                       F2P        C2P        N2P        F2P        C2P        N2P
                   #Rule #LLM #Rule #LLM #Rule #LLM #Rule #LLM #Rule #LLM #Rule #LLM
        GPT-5      0.155   0.154    0.127   0.188    0.132   0.169     0.146   0.049     0.111    0.051    0.183   0.036
    Claude-4.5     0.164   0.201    0.153   0.205    0.209   0.152     0.220   0.064     0.210    0.049    0.250   0.061
    LLaMA-4        0.186   0.174    0.103   0.158    0.143   0.167     0.148   0.050     0.187    0.126    0.203   0.150
   Qwen3-32B       0.400   0.000    0.000   0.000      -       -       0.181   0.144     0.227    0.077    0.108   0.042
 Gemma-3-27B       0.667   0.500    0.833   0.000      -       -       0.252   0.097     0.215    0.167    0.270   0.062
             Avg   0.314   0.206    0.243   0.110    0.161   0.162     0.189   0.081     0.190    0.094    0.203   0.070

Table 7: Comp@1 after excluding one mutation family from completeness evaluation. Higher values after exclusion
indicate that the removed mutation family exposes defects not covered well by the retained family.

 Condition                 GPT-5            Claude-4.5           LLaMA-4               Qwen3-32B          Gemma-3-27B
 w/ all mutants            0.2551               0.2068               0.0944              0.0551              0.0441
 wo/ LLM-based             0.3094               0.2944               0.1046              0.0606              0.0481
 wo/ operator-based        0.2773               0.2289               0.1281              0.0690              0.0622



gests that completeness is not dominated by a small          66% of the final benchmark ground-truths are LLM-
number of unusually influential mutants.                     generated. In this section, we discuss whether the
                                                             LLM-generated ground truths will introduce bias
F.4   Operator-Level Ablation                                in the benchmark evaluation.
To test whether the metric is overly sensitive to               Importantly, P OSTCOND B ENCH does not use
a particular rule-based operator, we remove each             ground-truth postconditions during evaluation.
operator in turn and average the resulting Comp@1            Corr@1 and Comp@1 are computed solely via test
across models. Table 9 shows that most removals              execution and mutant discrimination, independent
have only minor effects. In Python, dropping                 of any reference specification. Therefore, adopt-
any single operator changes Comp@1 by at most                ing LLM-generated outputs as ground truth does
0.0038; in Java, the largest change is 0.0063 after          not affect how models are scored. During dataset
removing null_returns. This supports that com-               construction, LLM was used only to reduce man-
pleteness is not driven by one critical operator.            ual effort by proposing candidate ground-truths.
                                                             Target methods are filtered solely when human ex-
F.5   Mutation-Strength Ablation                             perts judge that writing a complete postcondition
                                                             set is infeasible under the current framework (Ap-
Finally, we test robustness under large random per-          pendix H). LLM assists in identifying solvable
turbations of the mutant set. We either remove 5 of          cases but does not influence evaluation criteria or
the 11 rule-based operators at random or remove              introduce model-specific bias.
50% of LLM-based mutants, and then recompute
Comp@1 over 50 trials. As shown in Table 8, the              H       Expert Refinement Statistics/Analysis
mean changes are small and the standard deviations
remain low for all models. These results indicate            As Section 3.2.5 mentioned, during domain expert
that the completeness metric is stable under sub-            refinement, some methods/mutants are found in-
stantial changes in both mutant composition and              appropriate for inclusion in the benchmark. We
mutant strength.                                             analyze and attribute them in this section.
                                                                Overall, filtering affects a minority of the sam-
G     Discussion on Bias from                                pled methods rather than most of them. Among 297
      LLM-Generated Ground Truths                            sampled Python methods, 87 are filtered (29.3%);
                                                             among 234 sampled Java methods, 24 are filtered
As described in Section 3.2.3, we introduce an               (10.3%). Most filtered methods arise from lim-
LLM (GPT-5-mini) for ground truth generation.                itations of the current specification frameworks
Table 8: Comp@1 under two forms of large mutant-set perturbation. Except for the baseline column, each cell
reports the mean and the standard deviation over 50 trials.

                                                Ex. 5                Ex. 50%                       Mutant-Budget Fractions
       Model                  Baseline        Operators            LLM Mutants         0.1          0.2     0.8       0.9                    1.0
                                                 0.265                0.265           0.331        0.307         0.262        0.259        0.255
       GPT-5                    0.255
                                                (0.004)              (0.002)         (0.007)      (0.006)       (0.003)      (0.003)      (0.000)
                                                 0.215                0.216           0.298        0.261         0.212        0.209        0.207
       Claude-4.5               0.207
                                                (0.003)              (0.002)         (0.010)      (0.008)       (0.003)      (0.002)      (0.000)
                                                 0.098                0.098           0.129        0.116         0.097        0.096        0.094
       LLaMA-4                  0.094
                                                (0.002)              (0.001)         (0.006)      (0.004)       (0.002)      (0.002)      (0.000)
                                                 0.056                0.057           0.074        0.068         0.056        0.056        0.055
       Qwen3-32B                0.055
                                                (0.001)              (0.001)         (0.003)      (0.003)       (0.001)      (0.001)      (0.000)
                                                 0.046                0.045           0.059        0.053         0.045        0.045        0.044
       Gemma-3-27B              0.044
                                                (0.001)              (0.001)         (0.004)      (0.003)       (0.001)      (0.001)      (0.000)

 01 @icontract.ensure(lambda result: not result.startswith('_'))               11 //@ ensures \result >= 0;
                                                                               31 /** This method is used to get a long with the specified size...
 21 def normalize_key(data: str) -> str:
                                                                               32   * Be careful with java long bit sign.
 22     """This is a lossy algorithm. Repeating and trailing underscores are        * This method doesn't handle signed values.<br>...
                                                                               33
        removed...           Does not mention starting.                        34 public long getNextLong(final int pLength) {...

                          (a) icontract example                                                            (b) JML example

Figure 9: Two examples of incorrect postconditions generated due to LLMs’ hallucination on semantics. The
left side is the generated postconditions from the N2P task and the target method from kellyjonbrazil/jc.
The documentation states that repeating and trailing underscores are removed, but makes no claim about leading
underscores. The generated postcondition nevertheless enforces the absence of leading underscores, introducing an
unsupported constraint. The right side target method is from devnied/Bit-lib4j. The postcondition is generated
from the F2P task. The method reads a long value of a given bit length. Although the comment notes that signed
values are “not handled” this implies no special treatment of the sign bit rather than non-negativity. The generated
postcondition incorrectly enforces \result >= 0, thereby ruling out valid behaviors. Both postconditions are
generated by Claude-4.5.


rather than the complexity of the methods: 45 of                               inappropriate for inclusion. The reasons for which
the 87 filtered Python methods and 13 of the 24                                they are filtered are analyzed in the following sec-
filtered Java methods fall into framework-limited                              tion.
categories, such as iterator-related or concurrency-                              These 75 methods have 2957 mutants. Among
related. For the remaining filtered cases, domain                              them, 43 mutants were identified as inappropriate
experts determined that writing a complete postcon-                            for inclusion and were filtered. 10 methods filtered
dition set would still be non-trivial even for humans                          the mutants. The reasons for their filtration are
under the current evaluation setup.                                            analyzed in the following section.
                                                                                  Overall, we have 135 + 75 = 210 Python methods
H.1      Python Language                                                       in our benchmark.
297 Python methods sampled by farthest-first
                                                                               H.1.1 Method-level Filtering Analysis
traversal. We ensure that the sampled methods
                                                                               After manual checking, 87 methods are filtered.
have at least five mutants.
                                                                               Under the current formal specification framework,
   Among them, 135 target methods have complete
                                                                               writing complete postcondition expressions for
postconditions generated by GPT-5-mini. These
                                                                               them is non-trivial even for human engineers. We
methods have 2670 mutants, all of which are killed
                                                                               analyze the reason for filtering.
by auto-generated postconditions.
   We manually checked the remaining 162 Python                                Iterator related (18). By limitation of the API,
methods and attempted to write complete postcon-                               Iterator/Generator objects can only be iterated over
ditions for them.                                                              once. Validating them by postcondition expres-
   Of the 162 Python methods, 75 have manually                                 sions has side effects. Therefore, methods have key
written postconditions that are identified as com-                             variables that in Iterator/Generator types, and the
plete. The remaining 87 methods are identified as                              key feature relies on accessing elements from the
                             GPT-5           Claude-4.5            LLaMA-4              Qwen3-32B             Gemma-3-27B
                Python C2P           Python N2P           Python F2P                Java C2P            Java N2P                Java F2P
         0.8
         0.6
Corr@1



         0.4
         0.2
         0.0
         0.6
Comp@1




         0.4
         0.2
         0.0
           [0,20) [20,40) [40, ) [0,20) [20,40) [40, ) [0,20) [20,40) [40, ) [0,20) [20,40) [40, ) [0,20) [20,40) [40, ) [0,20) [20,40) [40, )
                   #LoC                 #LoC                  #LoC                   #LoC                 #LoC                   #LoC
               Figure 10: Corr@1 (top) and Comp@1 (bottom) across target methods grouped by lines of code (LoC).


Table 9: Operator-level ablation for rule-based mutation,                           @icontract.ensure(lambda result:

averaged across models.                                                       (a)       all(result[i] <= result[i + 1]
                                                                                            for i in range(len(result) - 1)))


                                Python                                        (b) @icontract.ensure(lambda result:
                                                                                      all(a <= b for a, b in zip(result, result[1:])))
   Excluded operator                                  Comp@1
                                                                              (c) @icontract.ensure(lambda result:
                                                                                      result == sorted(result))
   No exclusion (baseline)                                0.0516
   asymmetric_str_method_swap                             0.0516
   augassign_to_assign                                    0.0516
                                                                              (d) @icontract.ensure(lambda result:
                                                                                      all(a <= b for a, b in itertools.pairwise(result)))
   numeric_increments                                     0.0516
   symmetric_str_method_swap                              0.0516              (e) @icontract.ensure(lambda result:
                                                                                      list(itertools.accumulate(result, max)) == result)
   unary_op_removal                                       0.0516
   boolean_constant_flip                                  0.0519                            def sort(arr: List[int]) -> List[int]:
   arg_removal                                            0.0521                                ...
   string_perturbation                                    0.0523
   keyword_rewrite                                        0.0525            Figure 11: An example for sorting algorithm validation.
   operator_replacement                                   0.0531
                                                                            (a) to (e) are postconditions written in icontract, which
   assignment_nullification                               0.0554
                                                                            are semantically equivalent but syntactically different.
                                 Java
   Excluded operator                                  Comp@1
   No exclusion (baseline)                                0.2106            Timeout (17). The postcondition running also
   conditionals_boundary                                  0.2106
   false_returns                                          0.2106            requires time. For these cases, complete vali-
   invert_negatives                                       0.2106            dations lead to timeouts. Figure 14 shows the
   true_returns                                           0.2107            load_inventory method from the project hynek/-
   increments                                             0.2108
   math                                                   0.2109            doc2dash. Note that the return value is directly re-
   primitive_returns                                      0.2110            lated to the content in the objects.inv file. There-
   negate_conditionals                                    0.2110            fore, a complete validation requires accessing the
   empty_returns                                          0.2111
   void_method_call                                       0.2152            file content, leading to timeouts.
   null_returns                                           0.2169
                                                                            Concurrency related (13). Some methods’ key
                                                                            feature is related to obtaining results through con-
iterator objects that have been filtered. Figure 13                         currency mechanisms (starting sub-processes, sub-
shows the prefix_lines method from project                                  threads, etc.), which are identified as inappro-
miyuchina/mistletoe.                                                        priate for inclusion. Figure 15 shows method
   Validating these methods requires access to the                          execute_code in vndee/llm-sandbox. In this case,
actual string elements. However, both the input                             the results depend on running the inputted code in-
parameters and return value have Iterator objects.                          side the session, which launches a sandbox using
Accessing elements in @icontract.snapshot or                                Docker, Kubernetes, Podman, etc. This leads to
@icontract.ensure decorators leads to side-                                 a non-trivial validation, since it would require an-
effects. The current icontract does not provide an                          alyzing the code’s semantics or launching a new
effective path to deal with these cases.                                    sandbox within the postcondition.
Table 10: Postcondition generation performance on non-standalone (Dep.) and standalone (Solo.) methods. Dep.
requires repository-specific dependencies, while Solo. is runnable with only built-ins. Bold indicates the higher
score within each comparison.

                       Language                 Python                                                             Java
                                     Corr@1              Comp@1                                         Corr@1             Comp@1
                 Model / Setting
                                   Dep.   Solo.         Dep. Solo.                                    Dep.   Solo.        Dep. Solo.
                            C2P    0.315     0.419      0.135                     0.210               0.614    0.768   0.385     0.600
                   GPT-5    N2P    0.211     0.365      0.038                     0.126               0.591    0.708   0.245     0.503
                            F2P    0.335     0.419      0.139                     0.245               0.662    0.768   0.393     0.578
                            C2P    0.470     0.600      0.070                     0.216               0.782    0.784   0.332     0.459
              Claude-4.5    N2P    0.441     0.597      0.018                     0.152               0.699    0.703   0.216     0.368
                            F2P    0.484     0.603      0.072                     0.223               0.775    0.805   0.335     0.459
                            C2P    0.120     0.158      0.024                     0.052               0.301    0.395   0.160     0.265
               LLaMA-4      N2P    0.092     0.142      0.004                     0.039               0.232    0.351   0.083     0.232
                            F2P    0.143     0.190      0.023                     0.081               0.302    0.405   0.173     0.281
                            C2P    0.012     0.023      0.001                     0.010               0.250    0.351   0.116     0.146
              Qwen3-32B     N2P    0.009     0.006      0.000                     0.000               0.149    0.303   0.055     0.232
                            F2P    0.015     0.006      0.003                     0.003               0.215    0.292   0.108     0.157
                            C2P    0.016     0.006      0.001                     0.000               0.209    0.276   0.090     0.184
           Gemma-3-27B      N2P    0.035     0.032      0.000                     0.000               0.170    0.108   0.046     0.076
                            F2P    0.019     0.019      0.003                     0.000               0.197    0.297   0.083     0.200
                   Avg             0.181     0.239      0.035                     0.090               0.410    0.488   0.188     0.316


Table 11: Effect of adding grammar guidance on the                                            Method-level correctness completeness gap
F2P task for two strong models.                                                             1.0
                                                                Gap (Corr_rate Comp_rate)




                 w/ guidance  w/o guidance
 Model
              Corr@1 Comp@1 Corr@1 Comp@1                                                   0.8
 GPT-5         0.767       0.400     0.520      0.298
 Claude-4.5    0.814       0.283     0.629      0.207                                       0.6

                                                                                            0.4

   Moreover, this category also includes sev-                                               0.2
eral coroutine-using methods. Figure 16 shows
get_task in a2aproject/a2a-python. Since the                                                0.0
return value directly relies on the results from
                                                                                                  C2P (Code-only) N2P (NL-only) F2P (NL + Code)
self.task_store.get. If get is a sync method,                                                                    Input Setting
we can call it and validate on its return value in-
side the postcondition. However, since get is an                Figure 12: Distribution of method-level correct-
async method and Python does not support async                  ness–completeness gaps under different input settings,
lambda. With icontract, defining async conditions               without methods with Corr@k = 0 excluded. The gaps
(and snapshots) is indeed tedious (Parquery AG,                 are relatively smaller than Figure 3 due to generally low
                                                                Corr_rates (e.g., Corr@1 = 0.224 in Table 5 for LLaMA-
2019).
                                                                4 under C2P setting)


Language entities related (8). Some methods
return a function object, edit a class object, etc. Val-         Ordinary (9). Some methods’ key features (log-
idation on these language entities is generally non-             ging, printing to stdout, sending email, etc.) are not
trivial. Figure 17 shows while_until_true in                     related to changes in the accessible code context
pypyr/pypyr, which returns a function object.                    status and cannot be caught by the specification
Moreover, Figure 18 shows make_sync in run-                      framework. Figure 19 shows rich_format_error
llama/llama_deploy, which edits and returns a class              in fastapi/typer. This method’s key feature is to
object.                                                          print error logs under different conditions. Buggy
mutants that disturb log printing can be caught by        These test cases would simply fail due to as-
the test suite since the test cases use mock util to   sertion error (exit_code is not 0), and the error
validate logging outputs. However, this method is      message will not specify whether the error is from
not feasible to validate with only the formal speci-   icontract violation error. For this case, since
fication framework.                                    only a few mutants (seven of 34) are affected by
                                                       this issue, we keep the method but filter out affected
Specified       error       process       (5). For
                                                       mutants.
Python, we need the program output
icontract.errors.ViolationError in stderr to           Equivalent but not the same results (two mu-
know that the postcondition can kill the mutant.       tants; one method involved). Sometimes, the
However, in some cases, errors do not output an        algorithm has multiple possible results, the test
error log. Figure 20 shows the test case format for    cases are over-validated, and fail on mutants
_make_command_help in langchain-ai/langchain-          that are actually equivalent to the correct code.
mcp-adapters. These test cases would simply fail       We filter out these mutants since we only keep
due to assertion error (exit_code is not 0), and       buggy mutants. Figure 24 shows the original
the error message will not specify whether the         method k_closest(points, k, origin) from
error is from icontract violation error.               keon/algorithms, the equivalent mutant, and the
                                                       over-constrained test case.
Others (17). Not included above, and non-trivial
                                                          While the mutant’s return value [(-2, -2),
for human engineers to write complete postcondi-
                                                       (-1, 0), (1, 1), (1, 0)] is equivalent to
tions. These methods are generally lengthy or exist
                                                       the expected result, the test case failed.
within complex code contexts, increasing the costs
                                                          Therefore, we filter out mutants under this cate-
of understanding. The human engineer failed to
                                                       gory since we only keep buggy mutants.
write complete postconditions for these. Figure 21
shows method merge in pypyr/pypyr. This 81-line        Timeout (three mutants; two methods involved).
method is complicated, and recursion is used. The      The postcondition running also requires time.
human engineer failed to write complete postcon-       Post-conditions that are complete enough to kill
ditions for it.                                        these mutants lead to a timeout. Figure 25
                                                       shows the partition_by_spaces method in the
H.1.2 Mutant-level Filtering Analysis                  frostming/marko project together with the down-
Of the 210 Python methods in the benchmark, 10         stream call path that amplifies the failure into a
have mutants filtered after manual checking. 43        timeout.
mutants are filtered. Note that we ensure the main        However, one mutant replaces the break in
feature of the methods can still be validated after    partition_by_spaces with return, directly re-
some of the mutants are filtered for these methods.    turning nothing. That will cause an error in
Ordinary (29 mutants; five methods involved).          break_paragraph. Further, it leads to more
The feature that mutant disturbs (logging, process     loop running in the parse method, and finally
sleeping length, etc.) is not related to accessible    causes a timeout. Since only one mutant trig-
code context status change and cannot be caught        gers this timeout issue, and the main feature
by the specification framework. Figure 22 shows        of partition_by_spaces is still validatable, we
getprops in google/mobly.                              keep this target method and filter out this mutant.
   The main feature of this method is validat-         H.2   Java Language
able. However, a few mutants disturb the line of
                                                       We sampled 234 Java methods by farthest-first
time.sleep, e.g., replacing it by time.sleep(0).
                                                       traversal. We ensure that the sampled methods
We filter out these mutants for a similar reason to
                                                       have at least five mutants.
the way we filter “ordinary” category methods.
                                                          Among them, 141 target methods have complete
Specified error process (nine mutants; two             postconditions generated by GPT-5-mini. These
methods involved). These mutants triggered er-         methods have 2,530 mutants, all of which are killed
rors that do not output error types. Figure 23         by auto-generated postconditions.
shows the triggered test case format for two mu-          We manually checked the remaining 93 Java
tants on method _parse_ignore_file in project          methods, trying to write complete postconditions
coderamp-labs/gitingest.                               for them.
    From the 93 Java methods, 69 methods have             The java.awt.Graphics2D object is cre-
manually-written postconditions that are identified    ated from java.awt.image.BufferedImage
as complete. The remaining 24 methods are iden-        by BufferedImage::createGraphics() API.
tified as inappropriate for inclusion. The reasons     However, due to the privacy limitation, the
that they are filtered are analyzed in the following   buffered image cannot be accessed by the
section.                                               created Graphics2D object.         This method
    These 69 methods have 2,075 mutants. Among         drawRectanglesOfDifferences draws rect-
them, two mutants were identified as inappropri-       angles onto a BufferedImage object using a
ate to be included and filtered. One method has        Graphics2D object graphics, while the modified
mutants being filtered. The reasons that they are      buffered image cannot be accessed for validation.
filtered are analyzed in the following section.
                                                       Random related (3). Some methods rely on ran-
    Overall, we have 141 + 69 = 210 Java methods
                                                       dom algorithms. For defects within these methods,
in our benchmark.
                                                       test cases can be called multiple times, and bugs
H.2.1   Method-level Filtering Analysis                can be distinguished by observing the statistics,
After manual checking, 24 methods are filtered.        while a postcondition that runs each time after the
Under the current formal specification framework,      method calls cannot catch the bugs. Figure 29a
writing complete postcondition expressions for         shows changeMess in TheAlgorithms/Java.
them is non-trivial even for human engineers. We          ber is a field. This method randomly gets a pseu-
analyze the reason for filtering.                      dorandom x between 0 and 1 and modifies message
                                                       when x < ber. Figure 29b shows one representa-
Timeout (5). The postcondition running also re-        tive test case that covers this method. After 1,000
quires time. For these cases, complete validations     calls of changeMess, it is nearly certain that the
lead to timeouts. Figure 26 shows the compare          wrongMess field is larger than zero. However, the
method from red6/pdfcompare.                           postcondition validation is called each time after
   This method applies a PDF loading and compar-       the method runs. It is possible that after a method
ison. Therefore, validating this method generally      call, the wrongMess is still zero. Therefore, it is
requires accessing two PDF files, leading to time-     non-trivial to validate wrongMess due to this ran-
outs.                                                  domness.

Iterator related (4). By limitation of the API,        Ordinary (2). Some methods’ key feature is not
Iterator/Generator objects can only be iterated over   related to accessible code context status change and
once. Validating them by postcondition expres-         cannot be caught by the specification framework.
sions has side effects. Therefore, methods have        Figure 30 shows execute in antkorwin/xsync.
key variables that in Iterator/Generator types, and       As the key feature of this execute method, we
the key feature relies on accessing elements from      need to validate whether the runnable has been
the iterator objects that have been filtered. Fig-     run, which is non-trivial to validate since the im-
ure 27 shows the iterator method from project          plementation of runnable can be various.
decorators-squad/eo-yaml.
   Validating the return value of this method re-      Others (6). Not included above, and non-trivial
quires access to the actual string elements of the     for human engineers to write complete postcondi-
return value. However, the return value has Itera-     tions. These methods are generally long or within
tor objects. Accessing elements in postconditions      complex code contexts, increasing the understand-
leads to side-effects.                                 ing costs. Figure 31 shows douglasPeucker in
                                                       dyn4j/dyn4j.
Inaccessible code context (4). In Java, only              This 85-line method is complicated, and recur-
public cross-class fields/methods can be accessed.     sion is used. The human engineer failed to write
This category refers to the case where the tar-        complete postconditions for it.
get method modifies some write-only code con-
text. The postcondition cannot perform vali-           H.2.2   Mutant-level Filtering Analysis
dation due to inaccessible code contexts. Fig-         Of the 210 Java methods in the benchmark, one
ure 28 shows drawRectanglesOfDifferences in            has mutants filtered after manual checking. Two
romankh3/image-comparison.                             mutants are filtered. Note that we ensure the main
feature of the methods can still be validated after
part of the mutants are filtered for these three meth-
ods.
   All mutants are filtered due to nameless imple-
mentation, which happens in method accumulate
from dyn4j/dyn4j: Figure 32a shows the target
method, and Figure 32b shows a representative
isComplete implementation from the test suite.
   This method has two mutants that replace
if (force.isComplete(elapsedTime)) and if
(torque.isComplete(elapsedTime)) with if
(elapsedTime > 0). If isComplete has no side-
effect, we can call it in the postconditions and
validate that after the method calls, no element
in list this.forces and this.torques satisfies
isComplete.
   However, in particular, isComplete can be vari-
ous, defined by inner classes, and has side effects.
For example, Figure 32b shows the Force class
implementation used in the test case applyTimed.
   For the Torque class, the situation is similar.
   Therefore, killing the mutant that disturbs the
isComplete-related feature is non-trivial. It cannot
be called directly. Without calling it, validating is
also non-trivial due to the various implementations
with inner classes involved.
@classmethod
def prefix_lines(
    cls,
    lines: Iterable[str],
    first_line_prefix: str,
    following_line_prefix: str = None,
) -> Iterable[str]:
    ...
    for line in lines:
        ...
        yield prefixed if not prefixed.isspace() else ""



 Figure 13: Python iterator-related filtered method example: prefix_lines from miyuchina/mistletoe.



def load_inventory(source: Path) -> Mapping[str, Mapping[str, InventoryEntry]]:
    ...
    with (source / "objects.inv").open("rb") as fp:
        ...



  Figure 14: Python timeout-related filtered method example: load_inventory from hynek/doc2dash.



def execute_code(
    code: str,
    language: str = "python",
    libraries: list[str] | None = None,
    timeout: int = 30,
) -> list[ImageContent | TextContent]:
    ...
    try:
        ...
        with session_cls(
            ...
        ) as session:
            result = session.run(
                code=code,
                libraries=libraries or [],
                timeout=timeout,
            )
    ...
    else:
        return results



Figure 15: Python concurrency-related filtered method example: execute_code from vndee/llm-sandbox.



async def get_task(self) -> Task | None:
    ...
    self._current_task = await self.task_store.get(
        self.task_id, self._call_context
    )
    ...
    return self._current_task



  Figure 16: Python coroutine-related filtered method example: get_task from a2aproject/a2a-python.
    def while_until_true(interval, max_attempts):
        def decorator(f):
            ...

        return decorator



      Figure 17: Python language-entity filtered method example: while_until_true from pypyr/pypyr.


    def make_sync(_class: type[T]) -> Any:
        """Wraps the methods of the given model class so that they can be called without
        ,→ `await`."""


        class ModelWrapper(_class): # type: ignore
            _instance_is_sync: bool = True
        ...
        return ModelWrapper



     Figure 18: Python language-entity filtered method example: make_sync from run-llama/llama_deploy.


    def rich_format_error(self: click.ClickException) -> None:
        ...
        if ctx is not None:
            console.print(ctx.get_usage())

        if ctx is not None and ctx.command.get_help_option(ctx) is not None:
            console.print(
                ...
            )

        console.print(
            ...
        )



    Figure 19: Python ordinary-category filtered method example: rich_format_error from fastapi/typer.


    def test_help_create():
        result = runner.invoke(app, ["create", "--help"])
        assert result.exit_code == 0
        ...



Figure 20: Python specified-error-process example: test case covering _make_command_help from langchain-
ai/langchain-mcp-adapters.


    def merge(self, add_me):
        """Merge add_me into context and applies interpolation.
        ... (27 lines of comments)
        """
        def merge_recurse(current, add_me):
            ... (47 lines)
        ... (2 lines)
        merge_recurse(self, add_me)



                 Figure 21: Python other filtered method example: merge from pypyr/pypyr.
    def getprops(self, prop_names):
        ...
        if attempt < attempts - 1:
            time.sleep(DEFAULT_GETPROPS_RETRY_SLEEP_SEC)
        return results



               Figure 22: Python mutant-level ordinary example: getprops from google/mobly.




    result = _invoke_isolated_cli_runner(["./", "--output", "-", "--exclude-pattern", "tests/"])
    ...
    assert result.exit_code == 0



Figure 23: Python mutant-level specified-error-process example: triggered test case for _parse_ignore_file from
coderamp-labs/gitingest.




    def k_closest(points, k, origin=(0, 0)):
        ...
        heapify(heap)
        ...
        for point in points[k:]:
            ...
        return [point for nd, point in heap]


                                               (a) Original method.


    def k_closest(points, k, origin=(0, 0)):
        ...
        heap.sort()
        ...
        for point in points[k:]:
            ...
        return [point for nd, point in heap]


                                              (b) Equivalent mutant.


    self.assertEqual(
        [(-2, -2), (1, 1), (1, 0), (-1, 0)], k_closest(...)
    )


                                          (c) Over-constrained test case.

Figure 24: Python mutant-level equivalent-result example: original method, equivalent mutant, and test case for
k_closest from keon/algorithms.
    def partition_by_spaces(text, spaces) -> tuple[str, str, str]:
        ...
        for i, c in enumerate(text):
            ...
            elif start >= 0:
                end = i
                break
        ...


                                              (a) Target method.


    def parse(...) -> list[str] | SetextHeading:
        ...
        while ...:
            if cls.break_paragraph(source):
                break
            ...

    def break_paragraph(...) -> bool:
        try:
            str1, str2, str3 = parse_leading(...)
            if ...:
                return True
            return False
        finally:
            ...


                                      (b) Simplified downstream call path.

Figure 25: Python mutant-level timeout example: partition_by_spaces from frostming/marko and a simplified
downstream call path.



    public T compare() throws IOException, RenderingException {
        ...
        try (PDDocument expectedDocument = Loader.loadPDF(...)) {
            try (PDDocument actualDocument = Loader.loadPDF(...)) {
                compare(expectedDocument, actualDocument);
            }
        }
        ...
        return compareResult;
    }



          Figure 26: Java timeout-related filtered method example: compare from red6/pdfcompare.



    public Iterator<YamlLine> iterator() {
        Iterator<YamlLine> iterator = this.yamlLines.iterator();
        if (iterator.hasNext()) {
            final List<YamlLine> docsStart = ...
            ...
            iterator = docsStart.iterator();
        }
        return iterator;
    }



      Figure 27: Java iterator-related filtered method example: iterator from decorators-squad/eo-yaml.
    private void drawRectanglesOfDifferences(List<Rectangle> rectangles, Graphics2D graphics) {
        List<Rectangle> rectanglesForDraw;
        ...
        draw(graphics, rectanglesForDraw);
        if (fillDifferenceRectangles) {
            fillRectangles(graphics, ...);
        }
    }



Figure 28: Java inaccessible-code-context filtered method example: drawRectanglesOfDifferences from
romankh3/image-comparison.




    public void changeMess() {
        for (int y : message) {
            double x = randomGenerator.nextDouble();
            ...
            if (x < ber) {
                messageChanged = true;
                ...
                message.set(...);
            }
        }
        if (messageChanged) {
            wrongMess++;
        }
    }


                                            (a) Target method.


    @Test
    void testIntermediateBER() {
        CRCAlgorithm c = new CRCAlgorithm("1101", 4, 0.5);
        c.generateRandomMess();
        for (int i = 0; i < 1000; i++) {
            ...
            c.changeMess();
            ...
        }
        assertTrue(c.getWrongMess() > 0);
        ...
    }


                                        (b) Representative test case.

     Figure 29: Java random-related filtered method examples for changeMess from TheAlgorithms/Java.
public void execute(KeyT firstKey, KeyT secondKey, Runnable runnable) {
    ...
    if (...) {
        synchronized (firstMutex) {
            synchronized (secondMutex) {
                runnable.run();
            }
        }
    } else {
        synchronized (globalLock) {
            synchronized (firstMutex) {
                synchronized (secondMutex) {
                    runnable.run();
                }
            }
        }
    }
}



     Figure 30: Java ordinary-category filtered method example: execute from antkorwin/xsync.




/**
 * Recursively ... (8 lines of comments)
 */
private final List<Vector2> douglasPeucker(...) {
    ... (22 lines)
    if (...) {
        // sub-divide and run the algo on each half
        List<Vector2> aReduced = this.douglasPeucker(...);
        List<Vector2> bReduced = this.douglasPeucker(...);
        ... (4 lines)
    } else {
        ... (41 lines)
    }

    return result;
}



         Figure 31: Java other filtered method example: douglasPeucker from dyn4j/dyn4j.
protected void accumulate(double elapsedTime) {
    ...
    if (...) {
        Iterator<Force> it = this.forces.iterator();
        while(it.hasNext()) {
            Force force = it.next();
            ...
            if (force.isComplete(elapsedTime)) {
                it.remove();
            }
        }
    }
    ...
    if (...) {
        Iterator<Torque> it = this.torques.iterator();
        while(it.hasNext()) {
            Torque torque = it.next();
            ...
            if (torque.isComplete(elapsedTime)) {
                it.remove();
            }
        }
    }
}


                                         (a) Target method.


@Test
public void applyTimed() {
    ...
    Force f = new Force(1, 0) {
        private double time = 0;
        public boolean isComplete(double elapsedTime) {
            time += elapsedTime;
            if (time >= 2.0 / 60.0) {
                return true;
            }
            return false;
        }
    };
    ...
}


                               (b) Representative test implementation.

         Figure 32: Java mutant-level nameless-implementation examples from dyn4j/dyn4j.
                                                                                         F2P Method-level correctness completeness gap
                                                                           1.0

                                               Gap (Corr_rate Comp_rate)   0.8

                                                                           0.6

                                                                           0.4

                                                                           0.2

                                                                           0.0
                                                                                 gpt-5     claude-sonnet-4-5 llama-4-maverick   Qwen3-32B    gemma-3-27b
                                                                                                                 Model

Figure 33: Distribution of method-level correctness–completeness gaps with F2P setting under different models. For
each method m, the gap is computed as ∆(m) = corr_rate(m) − comp_rate(m), where corr_rate and comp_rate
denote the fraction of generated postcondition sets that are test-correct and complete, respectively. Each violin
aggregates gap values across methods for which at least one test-correct postcondition is generated; methods with
Corr@k = 0 are excluded.




                                                                                 Method-level correctness completeness gap
                                                                                  Python                                                    Java
                                       1.0
           Gap (Corr_rate Comp_rate)




                                       0.8

                                       0.6

                                       0.4

                                       0.2

                                       0.0
                                          C2P (Code-only) N2P (NL-only) F2P (NL + Code)                               C2P (Code-only) N2P (NL-only) F2P (NL + Code)

Figure 34: Distribution of method-level correctness–completeness gaps under different input settings and program-
ming languages. For each method m, the gap is computed as ∆(m) = corr_rate(m) − comp_rate(m), where
corr_rate and comp_rate denote the fraction of generated postcondition sets that are test-correct and complete,
respectively. Each violin aggregates gap values across methods for which at least one test-correct postcondition is
generated; methods with Corr@k = 0 are excluded.
