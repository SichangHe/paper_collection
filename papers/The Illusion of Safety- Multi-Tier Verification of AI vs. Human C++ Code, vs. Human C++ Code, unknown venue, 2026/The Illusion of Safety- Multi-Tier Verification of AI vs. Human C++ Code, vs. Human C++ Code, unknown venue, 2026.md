                                        The Illusion of Safety: Multi-Tier Verification of AI
                                                       vs. Human C++ Code
                                                                    Saif Mahmud∗ , Fadul Sikder∗ , Yuede Ji∗ , Haotian Zhang† , and Yu Lei∗
                                                       ∗ Computer Science and Engineering, The University of Texas at Arlington, Arlington, Texas, USA

                                                                          Email: {sxm8931, fxs5359}@mavs.uta.edu, {yuede.ji, ylei}@uta.edu
                                                      † Computer Science and Engineering, New Jersey Institute of Technology, Newark, New Jersey, USA

                                                                                                  Email: haotian.zhang@njit.edu


                                           Abstract—As large language models (LLMs) are increasingly                  as their primary (or exclusive) verification method [3], [5],
                                        deployed for systems programming, their ability to generate                   [7]. For C++ in particular, static-only evaluation provides an
                                        secure C++ code, where a single memory-safety failure creates                 incomplete and potentially misleading security assessment.
                                        an exploitable vulnerability, remains a critical concern. Yet
                                        most security evaluations of AI-generated code rely on static                 Static tools (cppcheck, clang-tidy) report comparable warn-
                                        analysis alone, which flags warnings without confirming run-                  ing rates for AI-generated and human-written code, superfi-
                                        time violations or reasoning about untested paths. This study                 cially suggesting the two are equally safe. However, static
                                        investigates whether AI-generated C++ is measurably less safe
arXiv:2607.00107v3 [cs.SE] 2 Aug 2026




                                                                                                                      analysis cannot confirm that warnings correspond to true
                                        than human-written code, and whether common verification tools                runtime violations, nor can it reason about untested code
                                        agree on the risk. We introduce V UL B ENCH -CPP, a benchmark
                                        of 8,918 C++ programs from three open-weight LLMs (Gemma 3                    paths. This methodological limitation obscures a significant
                                        27B IT, LLaMA 3.3 70B Instruct, Qwen 2.5 Coder 32B Instruct)                  vulnerability gap: AI-generated C++ code triggers confirmed
                                        and human authors across 851 competitive-programming tasks.                   runtime memory-safety violations at several times the rate of
                                        Each program is annotated by four verification tiers: functional              human-written code, a gap invisible to static analysis alone.
                                        testing, static analysis (cppcheck, clang-tidy), dynamic analysis             Relying exclusively on static checks allows undetected runtime
                                        (ASan/UBSan), and bounded model checking (ESBMC). Account-
                                        ing for the correlation among solutions to a shared task, we find             vulnerabilities to enter production. This risk is compounded
                                        that AI-generated code is roughly twice as likely as human code               in CI/CD pipelines where static-only checks gate code accep-
                                        to trigger a confirmed runtime violation, even after controlling              tance, providing an incomplete measure of code safety.
                                        for code length and test pass-rate. Under static analysis the                 The limitations of any single verification tier. The root
                                        two look equally safe, but this is misleading: the apparent                   cause of this hidden vulnerability gap is methodological: static
                                        similarity reflects code length rather than real safety, and the
                                        tiers detect largely different classes of violation, demonstrating            analysis, dynamic verification (ASan/UBSan), and formal ver-
                                        that no single tier is sufficient. These vulnerability patterns               ification (bounded model checking) operate on fundamentally
                                        remain consistent across independent generations. We release the              different principles and detect non-overlapping vulnerability
                                        benchmark, harness, and annotated results1 .                                  classes. Static tools examine source patterns without execu-
                                                                                                                      tion; dynamic analysis confirms violations only on executed
                                                                 I. I NTRODUCTION                                     code paths; formal verification exhaustively explores all execu-
                                        Problem and importance. Large language models (LLMs)                          tion paths within a bounded loop depth, including code paths
                                        are increasingly used to generate source code in professional                 never exercised by tests. Consequently, no single verification
                                        software development [1]. GitHub reports that AI-assisted                     tier is sufficient. Our study quantifies this gap: cross-tool
                                        coding now contributes to a substantial and growing fraction of               agreement between dynamic and formal verification is near-
                                        code in active repositories [2], [3], and enterprise adoption is              zero (Jaccard ≈ 0.05); of the 661 violations formally proven
                                        accelerating across systems programming, embedded develop-                    by ESBMC, 598 occur on untested paths that sanitizers never
                                        ment, and high-performance computing, domains where C++                       detect, while sanitizers discover 576 runtime bugs the model
                                        dominates. For memory-unsafe languages like C++, which                        checker does not flag. To address the vulnerability gap revealed
                                        provides no runtime exceptions or memory safety guarantees,                   by dynamic and formal verification, practitioners require a
                                        the stakes are particularly high: a single buffer overflow or                 systematic methodology that combines all four tiers: functional
                                        use-after-free vulnerability translates to an exploitable security            correctness testing, static analysis, dynamic analysis, and
                                        breach or silent data corruption [4]. A critical question re-                 formal verification.
                                        mains: how secure is AI-generated C++ code, and are existing                  Approach and benchmark construction. To validate this
                                        verification practices sufficient to catch its flaws?                         hypothesis and measure cross-tool coverage empirically, we
                                        The limitations of static-only evaluation. Prior evaluations                  introduce V UL B ENCH -CPP, a benchmark of 8,918 C++
                                        of AI-generated code security have employed static analysis                   programs: 7,223 generated by three state-of-the-art LLMs
                                                                                                                      (Gemma 3 27B IT, LLaMA 3.3 70B Instruct, Qwen 2.5 Coder
                                          1 Replication package: https://anonymous.4open.science/r/bsa-aigcvul-257B   32B Instruct) and 1,695 human-written solutions across 851
                                                            TABLE I
  C OMPARISON WITH CLOSELY RELATED WORK ON AI- GENERATED CODE SECURITY EVALUATION . V UL B ENCH -CPP IS THE FIRST C++ BENCHMARK
              WITH HUMAN REFERENCE SOLUTIONS AND FOUR - TIER VERIFICATION ENABLING DIRECT AI VS . HUMAN COMPARISON .


                        Study                  Language    Static     Dynamic      Formal     Multi-tier          Human ref.
                        Pearce et al. [3]       Python/C     ✓          –              –          –                       –
                        Khoury et al. [5]        C/C++       ✓          –              –          –                       –
                        Siddiq & Santos [6]      Python      ✓          –              –          –                       –
                        Dai et al. [7]           Python      ✓          –              –          –                       –
                        FormAI [8]                 C         ✓          ✓              –          ✓                       –
                        FormAI-v2 [9]              C         ✓          ✓              ✓          ✓                       –
                        SeCodePLT [10]            Multi      ✓          ✓              –          ✓                       –
                        VulBench-CPP (ours)       C++        ✓          ✓              ✓          ✓                       ✓



competitive programming tasks. Each program is annotated                     includes multi-tool annotations spanning four verifica-
with outputs from four verification tiers: (1) functional cor-               tion tiers (functional correctness testing, static analysis,
rectness testing via test suite execution, (2) static analysis (cp-          dynamic analysis, and formal verification), evaluation
pcheck, clang-tidy), (3) dynamic analysis (ASan/UBSan), and                  scripts, and all raw analysis outputs. As summarized
(4) bounded model checking (ESBMC [11]). By measuring                        in Table I, V UL B ENCH -CPP is the first benchmark to
cross-tool agreement via Jaccard similarity, we precisely quan-              combine an uncontaminated human reference baseline
tify which vulnerability classes are exclusive to each tier and              with four-tier verification for C++, addressing the critical
whether deploying additional tools provides complementary or                 evidence gaps left by prior static-only or Python-centric
merely redundant coverage.                                                   datasets.
Key results. Under dynamic analysis, AI-generated code                   Figure 1 illustrates the four-tier verification pipeline. The
triggers confirmed runtime violations at 3.6× the raw rate             remainder of this paper is organized as follows: Section 2
of human code (9.3% vs. 2.6%). Because the solutions to a              surveys related work; Section 3 defines our research questions;
shared task are correlated, we estimate the gap with a clustered       Section 4 describes the benchmark; Section 5 details the
mixed-effects logistic model: AI authorship roughly doubles            methodology; Section 6 presents results; Section 7 discusses
the odds of a runtime violation (adjusted OR = 2.15, 95% CI            implications; Sections 8 and 9 cover threats and conclusions.
1.52–3.03, p < 0.001), even after controlling for code length                           II. R ESEARCH Q UESTIONS
and test pass-rate. Static analysis shows no such gap; once
code length is controlled the AI effect reverses, confirming its         This study empirically characterizes the security of AI-
warning counts are not a reliable security signal. The dynamic         generated C++ code compared to human-written code using
gap is stable across independent LLM generations (within-              a multi-tier verification framework, organized around three
model variance ≤1.8 pp), confirming these are systematic               complementary research questions.
model properties rather than sampling artifacts. Finally, the
tiers detect largely disjoint violation classes: of 661 formally
proven violations, 598 are not triggered by sanitizers, and
                                                                             Code-contest                         851 coding                         Openrouter
of 639 sanitizer-triggered programs, 576 are not flagged by                  dataset shards                      instructions                        API call to
                                                                                                                   (Prompt)                         three models
ESBMC, so no single tier is sufficient.
   In this work, we make two primary contributions:
                                                                                                      Human Solutions                       Generated programs
                                                                              Tests Suites             2 solution sets:                      3 generations per
  1) Empirical findings. We demonstrate through a four-                                                   total 1695                         model: total 7223

     tier verification methodology that cross-tool agreement
     is remarkably low (Jaccard ≈ 0.05 between dynamic
     and formal tiers), with each tier detecting hundreds
     of unique vulnerabilities invisible to the others. AI-                                       Run static
                                                                             Run testsuites                                 Run dynamic              Run Model
                                                                                                   analyzer
     generated code triggers runtime violations at 3.6× the                     on the
                                                                                                 (Cppcheck /
                                                                                                                              analysis                Checker
                                                                               programs                                    (ASan / UBSan)             (ESBMC)
                                                                                                  Clang-tidy)
     rate of human-written code (z = 9.28, p < 0.001), and
     ESBMC formally proves 661 violations including bugs
     on untested code paths.                                                 Test Pass Rate
                                                                                                CWE / compiler             Runtime error
                                                                                                                                                   Counterexample
                                                                                                  warnings                    report
  2) Benchmark. We introduce V UL B ENCH -CPP, a curated
     benchmark of 8,918 C++ programs (7,223 generated
     by Gemma 3 27B IT, LLaMA 3.3 70B Instruct, and
                                                                       Fig. 1. Four-tier verification pipeline: 851 CodeContests problems yield 8,918
     Qwen 2.5 Coder 32B Instruct, plus 1,695 human-written             C++ programs evaluated through functional correctness testing, static analysis
     solutions) across 851 competitive programming tasks               (cppcheck, clang-tidy), dynamic analysis (ASan/UBSan), and bounded model
     from the CodeContests dataset [12]. The benchmark                 checking (ESBMC).
                                                              TABLE II
 M ULTI - TIER VERIFICATION SUMMARY ACROSS ALL MODELS AND TIERS . S ANITIZER RATE IS COMPUTED OVER COMPILED PROGRAMS . ESBMC RATE IS
                              COMPUTED OVER ANALYZABLE PROGRAMS ( EXCLUDING PARSE ERROR, TIMEOUT).


                          Model        N    Cppcheck CWE         Clang-tidy     Sanitizer            ESBMC FAILED
                          Gemma     2,238      1,021 (45.6%)    620 (27.7%)    173 (8.6%)    234 (25.9% of analyzable)
                          LLaMA     2,496        840 (33.7%)    838 (33.6%)    217 (9.6%)    271 (36.7% of analyzable)
                          Qwen      2,489        908 (36.5%)    740 (29.7%)    224 (9.8%)    135 (29.5% of analyzable)
                          Human     1,695       765 (45.1%)    1,004 (59.2%)    43 (2.6%)     21 (18.8% of analyzable)



RQ1 AI vs. human comparison. How do the vulnerability                                              TABLE III
    rates of AI-generated code compare to human-written                        B ENCHMARK COMPOSITION : INSTRUCTIONS AND TEST CASE
                                                                                                 AVAILABILITY.
    solutions under multi-tier verification?
    Rationale: Human-written solutions under identical task                                 Category                     Count
                                                                                            Total instructions             851
    conditions provide the only meaningful security baseline                                Instructions with tests        560
    at scale. Comparing AI and human code across all four                                   Instructions without tests     291
    verification tiers reveals whether their comparable static-
    warning rates reflect genuinely similar safety or merely
    mask a deeper gap, and whether AI adoption introduces               collected after the release of large code models (e.g., GitHub
    qualitatively new risks. This is the core empirical question        repositories containing Copilot-assisted code, modern Stack
    that motivates the benchmark.                                       Overflow contributions) are likely contaminated by LLM-
RQ2 Generation stability. Are vulnerability patterns repro-             generated or LLM-inspired code. CodeContests’ pre-2021
    ducible across independent generations of the same                  human submissions represent genuine human programming
    model?                                                              under competitive pressure, with vulnerabilities arising from
    Rationale: LLM code generation is inherently non-                   human reasoning and implementation choices alone. This
    deterministic. Validating that vulnerability rates remain           purity enables a meaningful, historically grounded security
    stable across independent generations (e.g., Gemma                  baseline rather than a potentially degraded baseline reflecting
    gen 1, gen 2, gen 3) proves that observed differences               a mixture of human and algorithmic code.
    in RQ1 are systematic model properties, not sampling                   For each instruction, we generate three independent C++
    artifacts. Stability is essential for practitioners to trust that   programs from each of three LLMs (Gemma 3 27B IT [13],
    RQ1 findings generalize to future model outputs.                    LLaMA 3.3 70B Instruct [14], and Qwen 2.5 Coder 32B In-
RQ3 Unique vulnerability classes per tier. What vulnerabil-             struct [15]) under zero-shot prompting. We include up to two
    ity classes does each analysis tier detect, and how do these        accepted human-written solutions per problem (1,695 total
    class distributions differ between AI and human code?               across 851 problems) as a reference baseline. This cap is
                                                                        methodologically principled: (1) it maintains statistical balance
    Rationale: Understanding the vulnerability class profiles
                                                                        (9 AI samples per problem versus 2 human samples), prevent-
    per tier explains the mechanisms driving the RQ1 gap.
                                                                        ing human code from dominating per-problem comparison;
    For instance, formal verification may reveal vulnerabili-
                                                                        (2) it ensures computational feasibility, as formal verification
    ties on untested paths that are more prevalent in AI code,
                                                                        (ESBMC with 60-second timeout per program) is expensive,
    while sanitizers may catch runtime violations at systemat-
                                                                        and including all available human solutions would expand the
    ically different rates for AI versus human solutions. This
                                                                        benchmark to 10,000+ programs; (3) it avoids sampling bias
    explains the mechanisms underlying the RQ1 findings.
                                                                        from problems with heterogeneous numbers of accepted solu-
            III. T HE V UL B ENCH -CPP B ENCHMARK                       tions. The baseline enables direct vulnerability rate comparison
 A. Dataset Composition                                                 under identical conditions to answer RQ1: whether comparable
                                                                        static-warning rates mask a genuine security gap. The bench-
    The benchmark is built from the CodeContests [12] dataset,          mark comprises 7,223 AI-generated and 1,695 human-written
 which contains competitive programming problems with pub-              programs (8,918 total).
 licly available test cases and human-written C++ solutions. We
 select 851 coding instructions for which at least one human-           B. Evaluation Harness
 written C++ solution exists. Among these, 560 have at least
 one public test case, while 291 have none (Table III).                   The benchmark includes a complete, automated evaluation
    Justification for CodeContests baseline. The CodeContests           pipeline:
 dataset, originally released in 2021 and sourced from compet-             • Extraction: scripts to extract C++ code from LLM API
 itive programming contests predating the GPT era, provides                  responses
 an uncontaminated human baseline. This temporal separation                • Functional testing: parallel compilation and test execu-
 is critical for RQ1 (AI vs. human comparison): solutions                    tion against CodeContests test suites
  • Static analysis: cppcheck (v2.19.0) and clang-tidy (v21)       D. Tier 1: Static Analysis
    with standardized configurations                                  We apply cppcheck [17] (v2.19.0) with warnings, style,
  • Dynamic analysis: ASan/UBSan instrumented compila-             performance, and portability checks enabled, targeting C++17
    tion and execution                                             with a 30-second timeout. MITRE Common Weakness Enu-
  • Formal verification: ESBMC (v8.0.0) bounded model              meration (CWE) [18] annotations are used to categorize
    checking                                                       findings. We additionally utilize clang-tidy [19] (v21), an
  • Aggregation: scripts to merge all tool outputs into a uni-     extensible AST-based linter built on the LLVM compiler in-
    fied master CSV with per-program, cross-tool annotations       frastructure, with the clang-analyzer-*, bugprone-*,
                                                                   performance-*, and modernize-* check families.
C. Annotated Results
   All analysis outputs are included: per-program verdicts         E. Tier 2: Dynamic Analysis
from each tool, CWE annotations, cross-tool agreement labels,        Each program is compiled with AddressSanitizer
and summary statistics. The master analysis CSV contains           (ASan) [20] and UndefinedBehaviorSanitizer (UBSan) [21]
8,918 rows with columns for each tool’s findings, enabling         using g++ 13.3.0 on Ubuntu 24.04.3 LTS:
researchers to immediately perform cross-tool comparisons                                     Listing 1
without re-running analyses.                                             C OMPILATION WITH SANITIZERS FOR DYNAMIC ANALYSIS .

                                                                   g++ -std=c++17 -O1 \
D. Intended Use                                                        -fsanitize=address,undefined \
   V UL B ENCH -CPP supports two primary use cases: (1) eval-          -fno-omit-frame-pointer \
uating new LLMs by running them on the 851 tasks and ana-              "$src" -o "$bin"
lyzing outputs through the existing pipeline, and (2) evaluating      Sanitizer-instrumented binaries are executed against the
new analysis tools by applying them to the existing 8,918          same test inputs. A program is classified as sanitizer-triggered
programs and comparing findings against the annotated results.     if any ASan or UBSan error is reported.
                    IV. M ETHODOLOGY                               F. Tier 3: Formal Verification (ESBMC)
A. Models and Access                                                  We apply ESBMC v8.0.0 [11], a bounded model checker
                                                                   that translates C/C++ programs into SMT formulas and ex-
   All models were accessed through the OpenRouter API [16],
                                                                   haustively checks safety properties for all inputs up to a
which provides unified access to multiple open and hosted
                                                                   bounded loop depth. ESBMC is configured as follows:
large language models. The final experiments were conducted
using Gemma 3 27B IT [13], LLaMA 3.3 70B Instruct [14],                                     Listing 2
                                                                            ESBMC INVOCATION FOR FORMAL VERIFICATION .
and Qwen 2.5 Coder 32B Instruct [15]. All models were
evaluated under identical prompting, decoding, and analysis        esbmc "$src" \
settings.                                                              --compact-trace \
                                                                       --no-unwinding-assertions \
B. Code Generation                                                     --no-div-by-zero-check \
                                                                       --overflow-check \
  For all models, we use a fixed zero-shot prompt:                     --unwind 10 \
      You are a competitive programming                                --timeout 60
      assistant. Write a complete, efficient
      C++ program using standard input/output                         For each program, ESBMC produces one of four ver-
      to solve this problem. Please do not                         dicts: SUCCESS (no violation found within the bound),
      include explanation. Only code:                              FAILED (violation proven with a concrete counterexample),
      {description}                                                PARSE_ERROR (C++ frontend cannot parse the program),
  No security-specific guidance is provided. We use Open-          or TIMEOUT (analysis exceeds 60 seconds). ESBMC checks
Router’s default decoding parameters (temperature = 1.0, top-      array bounds (CWE-119), null pointer dereference (CWE-
p = 1.0) and generate three independent solutions per model        476), arithmetic overflow (CWE-190, unsigned), memory
per problem. Responses are filtered to extract fenced C++          leaks (CWE-401), double free (CWE-415), and use-after-free
code blocks; fewer than 2% of LLaMA and Qwen responses             (CWE-416). Division-by-zero checking is explicitly disabled
required exclusion, while Gemma’s exclusion rate was approx-       (--no-div-by-zero-check) to reduce false positives
imately 12%.                                                       from unconstrained input variables; signed integer overflow is
                                                                   not caught by --overflow-check and requires UBSan’s
C. Functional Correctness Testing                                  runtime detection.
   Each solution is compiled with g++ (C++17, -O2) and                Table IV summarizes ESBMC coverage. The 56.5% parse
executed against public test cases with a fixed timeout. We        error rate reflects ESBMC’s C++ frontend limitations with
record compilation success, test pass counts, and timeout          STL containers, templates, and standard library functions.
occurrences uniformly for AI-generated and human solutions.        Among the 24.8% of programs that ESBMC can fully analyze,
Interactive problems are excluded.                                 29.9% contain formally proven violations.
                        TABLE IV                                  deliberately coarse because detailed CWE-level agreement
   ESBMC VERDICT DISTRIBUTION ACROSS ALL 8,918 PROGRAMS .         is confounded by (i) tool-specific property definitions (e.g.,
                                                                  whether signed overflow is checked by default), (ii) frontend
               Verdict           Count      Fraction
                                                                  limitations (ESBMC parse errors prevent CWE classification
               PARSE ERROR       5,039        56.5%               for 56.5% of programs), and (iii) scope differences (ESBMC
               TIMEOUT           1,621        18.2%
               SUCCESS           1,551        17.4%               analyzes all paths up to loop bound 10; sanitizers trigger
               FAILED              661         7.4%               only on executed paths). Program-level Jaccard agreement
               ERROR                46         0.5%               is therefore the appropriate first-order metric for answering
               Total             8,918                            whether tools cover overlapping regions of the behavior space.
                                                                  I. Evaluation Summary
G. Compilation and Coverage                                          The four-tier pipeline produces per-program verdicts from
   Table V reports compilation success rates. LLMs achieve        five tools. All outputs are merged into a cross-reference table.
90–92% compilation success; human solutions compile at            The cross-tool analysis subset (4,295 programs, Table II) is
98.2%. The lower AI rate reflects missing headers, mismatched     defined as programs from the 819 coding problems for which
function signatures, and incomplete code in a minority of         both (a) ESBMC produced any verdict (all 8,918 programs
responses (Gemma’s higher exclusion rate during generation,       receive an ESBMC verdict) and (b) sanitizer analysis was
≈12%, contributed to its lower compilation rate). Sanitizer       executed, which requires that the program compiled under
analysis is applied to all programs regardless of standard com-   sanitizer flags and had at least one public test case to run.
pilation success; a program classified as sanitizer-triggered     The 291 instructions without any public test case contribute
must both compile under sanitizer flags and produce a san-        programs to the benchmark but are excluded from cross-tool
itizer error during test execution. ESBMC is applied to all       agreement analyses because the sanitizer cannot be triggered
8,918 programs regardless of compilation status, producing        without a test input; ESBMC results for these programs are
PARSE ERROR for programs whose C++ features it cannot             reported separately in Table IV.
model.                                                                                     V. R ESULTS
                           TABLE V                                A. RQ1: AI vs. Human Comparison
   C OMPILATION SUCCESS RATES AND ANALYSIS SCOPE PER MODEL .
                                                                     1) Dynamic Analysis: AI-generated code triggers sanitizers
              Model      Total   Compiled       Rate
                                                                  at 3.6× the rate of human-written code (9.3% vs. 2.6% of com-
                                                                  piled programs). A two-proportion z-test confirms statistical
              Gemma      2,238      2,018      90.2%
              LLaMA      2,496      2,272      91.0%              significance (z = 9.28, p < 0.001). Restricting to programs
              Qwen       2,489      2,290      92.0%              with at least one executed test yields higher rates: 15.5% (AI)
              Human      1,695      1,665      98.2%              vs. 4.3% (human).
              Total      8,918      8,245      92.5%                 2) Formal Verification: Among ESBMC-analyzable pro-
                                                                  grams, AI-generated code shows higher violation rates than
                                                                  human code: Gemma 25.9%, LLaMA 36.7%, and Qwen
H. Vulnerability Classification and Cross-Tool Aggregation        29.5% versus 18.8% for human solutions (Table II).
   Each analysis tool produces findings, which we aggregate          3) Static Analysis: Static analysis presents a contrasting
and normalize at the program level for cross-tool compari-        picture. Cppcheck flags 33–46% of AI-generated programs,
son. Sanitizer-triggered programs are those that (1) compile      comparable to 45% for human code. Clang-tidy reports di-
under sanitizer flags and (2) trigger a runtime error during      agnostics for 27.7–33.6% of AI-generated programs versus
test execution; these are automatically classified into CWE       59.2% of human code; the higher human rate reflects greater
categories: AddressSanitizer reports array out-of-bounds ac-      use of complex language features. This apparent similarity
cesses, use-after-free, and double-free as CWE-119 (buffer        under static analysis is misleading and does not extend to
overflow), CWE-416 (use-after-free), and CWE-415 (double          confirmed runtime or formally proven violations.
free), respectively; UndefinedBehaviorSanitizer reports arith-       4) Correctness vs. Security: Programs that pass all func-
metic overflow, shift errors, and null pointer dereferences as    tional tests still contain vulnerabilities. Among AI-generated
CWE-190 (signed integer overflow), CWE-1025 (comparison           programs that pass all tests, 1.8% trigger sanitizer violations;
using wrong types), and CWE-476 (null pointer dereference),       for human solutions, this rate is 3.6%. This demonstrates
respectively. CWE assignments for static and formal verifi-       that functional correctness does not imply security, test-suite
cation tools are obtained from tool-native annotations. For       validation alone is insufficient.
cross-tool agreement analysis, we compute Jaccard similar-           5) Mixed-Effects Regression: The comparisons above treat
                   |A∩B|
ity J(A, B) = |A∪B|       at the program level: A is the set      programs as independent, but the nine AI programs and up to
of programs flagged by one tool (e.g., sanitizer-triggered),      two human solutions for a given task are correlated through
B is the set flagged by another (e.g., ESBMC FAILED).             shared problem difficulty. To account for this clustering and
This program-level binary aggregation (flagged or not) is         to adjust for potential confounders, we fit a mixed-effects
                               TABLE VI                                     RQ1 Finding
   M IXED - EFFECTS LOGISTIC REGRESSION OF EACH TIER ’ S VIOLATION
 INDICATOR ON S O U R C E (AI VS . HUMAN REFERENCE ), WITH A RANDOM         AI-generated code is significantly more vulnerable
INTERCEPT FOR PROBLEM . O DDS RATIOS > 1 INDICATE HIGHER ODDS OF
                 A VIOLATION FOR AI- GENERATED CODE .                       than human-written code under dynamic verification:
                                                                            the 3.6× sanitizer-rate gap holds in a mixed-effects
  Tier (outcome)               n    AI OR       95% CI           p          logistic regression that adjusts for clustering and cor-
  Dynamic (sanitizer)      4,961      2.15     1.52–3.03     < 0.001        rectness (adjusted OR = 2.15, p < 0.001). Formal ver-
  Static (cppcheck)†       4,961      0.68     0.57–0.81     < 0.001        ification shows the same direction descriptively (25.9–
  Formal (ESBMC)‡          1,680      1.83     0.94–3.56      0.076         36.7% vs. 18.8%) but is underpowered for adjusted
   † adjusted for program length (LOC). ‡ unadjusted; conclusive human      inference. Static analysis not only fails to reveal this
                     n = 96, hence not significant.                         gap but reverses once code length is controlled, con-
                                                                            firming its warning counts are not a reliable security
                                                                            signal.

                                                                         B. RQ2: Generation Stability
                                                                            LLM code generation is non-deterministic, producing differ-
                                                                         ent programs across independent invocations. To validate that
                                                                         RQ1 findings represent systematic model properties rather than
                                                                         sampling artifacts, we analyze vulnerability pattern stability
                                                                         across three independent generations per model.
logistic regression (a generalized linear mixed model with                  1) Sanitizer Trigger Rate Stability: Across independent
logit link) for each verification tier: the outcome is a binary          generations, sanitizer trigger rates remain stable within each
violation indicator, the primary fixed effect is source (AI              model: Gemma ranges from 8.2% to 8.8% (pp-range ≤0.6),
vs. human, human as reference), and a random intercept                   LLaMA ranges from 9.0% to 10.3% (pp-range ≤1.3), Qwen
for problem absorbs between-task heterogeneity. Candidate                ranges from 9.5% to 10.0% (pp-range ≤0.5). The human
covariates, test pass rate, standardized program length (LOC),           baseline is consistent at 2.6% across solutions. Within-model
and number of test cases, were reduced by backward elimina-              variance across generations (≤1.8 pp for sanitizers) is substan-
tion (likelihood-ratio test, α = 0.05; source and the random             tially smaller than the AI-vs-human gap (3.6×), confirming
intercept retained by design). All estimates were robust to a            that vulnerability patterns are reproducible properties of the
population-averaged GEE logistic model with exchangeable                 models, not sampling artifacts.
within-problem correlation, fit as a sensitivity check. Table VI            2) Formal Verification Stability: ESBMC violation rates
reports the adjusted odds ratios.                                        similarly demonstrate low generation-to-generation variance.
                                                                         This consistency indicates that the RQ1 gap (AI 25.9–36.7%
                                                                         vs. human 18.8

   Under dynamic analysis, AI authorship independently pre-                 RQ2 Finding
dicts a sanitizer violation (OR = 2.15, 95% CI 1.52–3.03,
p < 0.001) after adjusting for clustering and correctness;                  Vulnerability patterns are reproducible across indepen-
a higher pass rate is strongly protective (OR ≈ 0.23). The                  dent generations: within-model variance in sanitizer
dynamic-tier gap is therefore not an artifact of AI programs                trigger rates (≤1.8 pp) is much smaller than the AI-
failing more tests, and it survives the more rigorous treatment             vs-human gap (3.6×). This validates that RQ1 findings
that a simple two-proportion test cannot provide. Under static              reflect systematic model properties, enabling confident
analysis the effect reverses once program length is controlled:             deployment recommendations.
conditional on LOC, itself a dominant predictor (OR ≈ 6.7),
AI programs have lower odds of a cppcheck flag (OR = 0.68,               C. RQ3: Unique Vulnerability Classes per Tier
95% CI 0.57–0.81, p < 0.001), confirming that the higher raw                Each analysis tier detects distinct vulnerability classes,
static-warning counts for AI code are largely a code-length              reflecting the fundamentally different mechanisms through
effect rather than a security signal. For formal verification,           which they operate. Figure 2 illustrates the sanitizer trigger
ESBMC returns a conclusive verdict (SUCCESS or FAILED)                   rates by model, confirming that AI-generated code produces
for only 96 human programs (13 FAILED); this conclusive                  runtime violations at 3.4–3.8× the rate of human-written code
human sample is too small to support an adjusted mixed                   across all three models.
model, and an unadjusted clustered estimate is not statistically            1) ESBMC-Exclusive Findings: Of 661 formally proven
significant (OR = 1.83, 95% CI 0.94–3.56, p = 0.076). We                 violations, 598 are not detected by sanitizers. ESBMC’s viola-
therefore treat the formal-tier comparison as descriptive, and           tion CWE distribution is dominated by array bounds violations
caution that the high ESBMC parse-error rate on competitive-             (CWE-119, 102 instances) and null pointer dereference (CWE-
programming C++ (Section VII) limits its generalizability.               476, 88 instances), with additional findings in invalid pointer
                                                                               Runtime Error Detection Rate by Model (ASan/UBSan)                              relevant categories (CWE-119: bounds violations, CWE-252:
                                       0.12
                                                                                                                                                               unchecked return values), qualitatively different patterns indi-
                                                                                          9.6%                       9.8%
                                                                                                                  (224/2290)
                                       0.10                                            (217/2272)                                                              cating static analysis masks the true vulnerability gap.
Sanitizer Trigger Rate (of compiled)




                                                          8.6%
                                                       (173/2018)
                                       0.08
                                                                                                                                                                  4) Illustrative Examples: To concretize the complementary
                                                                                                                                                               nature of each tier, we present three representative examples.
                                       0.06                                                                                                                    Example 1: Formal verification catches what static and
                                       0.04                                                                                                                    dynamic analysis miss. Listing 3 shows a Gemma-generated
                                                                                                                                               2.6%
                                                                                                                                             (43/1665)         solution for the “Bear and Raspberry” problem. Both cppcheck
                                       0.02
                                                                                                                                                               and clang-tidy report no warnings, and no available test case
                                       0.00
                                                        Gemma                           Llama                       Qwen                      Human
                                                                                                                                                               triggers a sanitizer violation. ESBMC, however, produces a
                                                                                                                                                               counterexample at n = INT_MIN: the loop bound expres-
Fig. 2. Runtime error detection rates (ASan/UBSan) by model as a fraction                                                                                      sion n - 1 on line 5 is signed-integer subtraction overflow,
of compiled programs. All AI models exceed the human baseline by a factor                                                                                      undefined behavior in C++. ESBMC’s --overflow-check
of 3.4–3.8×.
                                                                                                                                                               flags this as arithmetic overflow on sub (CWE-
                                                                                         Runtime Vulnerability Distribution by CWE Type (ASan/UBSan)
                                                                                                                                                               190). No public test case provides n = INT_MIN, which
              CWE-761 (Free of Pointer not at Start of Buffer)
                                                                                                                                                    Model      is why neither sanitizers nor the test suite expose it. The
                                                                                                                                                     Gemma
                                                                                                                                                     Llama
                                                                                                                                                     Qwen
                                                                                                                                                               hardcoded branches later in the program (omitted here) access
                                                        CWE-416 (Use After Free)                                                                     Human     x[0]–x[5] but are guarded by short-circuited n == k
                                                 CWE-121 (Stack Buffer Overflow)                                                                               checks and are not the violation point.
                                                        CWE-369 (Divide By Zero)                                                                                                            Listing 3
                                                                                                                                                               ESBMC- EXCLUSIVE : SIGNED - INT OVERFLOW ON N - 1 (CWE-190) AT
                                              CWE-476 (NULL Pointer Dereference)                                                                                N = INT_MIN; CPPCHECK / CLANG - TIDY: NO WARNINGS ; SANITIZER :
                                                                                                                                                                        NOT TRIGGERED ON AVAILABLE TESTS (G EMMA ).
                                                   CWE-125 (Out-of-bounds Read)


                                                 CWE-122 (Heap Buffer Overflow)
                                                                                                                                                               1      int n, c;
                                                                                                                                                               2      cin >> n >> c; // n is unvalidated int from
                                                      CWE-190 (Integer Overflow)                                                                                           input
                                                                                   0      50        100       150         200       250       300        350   3      vector<int> x(n);
                                                                                                              Number of Programs                               4      for (int i = 0; i < n; ++i) cin >> x[i];
                                                                                                                                                               5      for (int d = 0; d < n - 1; ++d) {
Fig. 3. Runtime vulnerability distribution by CWE type (ASan/UBSan).                                                                                                      CWE-190:n-1 overflows when
Signed integer overflow (CWE-190) and heap/stack buffer overflows (CWE-                                                                                                   n=INT_MIN
122/121) dominate AI-generated code; human code shows markedly lower                                                                                            6       long long profit = x[d] - x[d+1] - c;
counts across all categories, particularly CWE-190 and CWE-122.                                                                                                 7       max_profit = max(max_profit, profit);
                                                                                                                                                                8     }
                                                                                                                                                                9     ...
use (CWE-825). These violations are proven for inputs that                                                                                                     10     ...
the test suite does not exercise, ESBMC explores all possible                                                                                                  11     if (n==6 && ...) { cout << ... << x[5]; }
inputs up to its loop bound, uncovering edge-case bugs that
remain latent during test-driven execution.                                                                                                                    Example 2: Sanitizers catch what formal verification de-
   2) Sanitizer-Exclusive Findings: Of 639 sanitizer-triggered                                                                                                 clares safe. Listing 4 shows a Gemma-generated solution for
programs, 576 are not flagged by ESBMC. The dominant                                                                                                           the “Blocked Points” problem. ESBMC successfully analyzes
violation type is signed integer overflow (CWE-190), detected                                                                                                  this program and returns SUCCESS, no violations found.
by UBSan, followed by heap-buffer-overflow (CWE-122) and                                                                                                       Cppcheck and clang-tidy report no warnings. However, UBSan
stack-buffer-overflow (CWE-121) detected by ASan. Many of                                                                                                      detects signed integer overflow (CWE-190) on 30 of 50 test
these programs could not be parsed by ESBMC’s C++ frontend                                                                                                     cases: when n is large, the expression 4 * n * (n + 1)
(56.5% parse error rate), while others involve runtime-specific                                                                                                overflows a 32-bit int. Although --overflow-check is
behavior (heap layout, large-input overflow) that exceeds the                                                                                                  enabled, ESBMC checks unsigned arithmetic overflow; signed
model checker’s analysis bound or property set. Figure 3                                                                                                       integer overflow in C++ is undefined behavior detectable only
shows the full CWE breakdown across models.                                                                                                                    at runtime by UBSan, not by the model checker’s property set.
   3) Static-Only Findings: Cppcheck and clang-tidy flag 33–                                                                                                                                    Listing 4
59% of programs, but their findings are predominantly style                                                                                                         S ANITIZER - EXCLUSIVE : ESBMC RETURNS SUCCESS, BUT UBS AN
                                                                                                                                                                             DETECTS SIGNED INTEGER OVERFLOW (G EMMA ).
warnings (CWE-398: code quality, CWE-563: unused vari-
ables) rather than confirmed security violations. The high                                                                                                     1      int n;
flagging rate creates a misleading appearance of compara-                                                                                                      2      cin >> n;
ble vulnerability levels between AI and human code. Static                                                                                                     3      if (n == 0) cout << 0 << endl;
                                                                                                                                                               4      else if (n == 1) cout << 4 << endl;
analysis findings show that AI models share nearly identi-                                                                                                     5      else if (n == 2) cout << 8 << endl;
cal distributions dominated by code-quality CWEs (CWE-                                                                                                         6      else if (n == 3) cout << 16 << endl;
398/563/570/571), while human code exhibits more security-                                                                                                     7      else cout << 4 * n * (n + 1) << endl;
 8       // n is int: when n > ˜23170,                               A. Practical Implications
 9       // 4*n*(n+1) overflows 32-bit int
10       // UBSan: signed integer overflow
                                                                        Static-only gates mask AI vulnerabilities. Static analysis
                                                                     flags 33–46% of AI code at rates comparable to human code
                                                                     (45%), while runtime violations occur at 3.6× the rate (9.3%
Example 3: Both tiers detect the same program, different
                                                                     vs 2.6%). Static-only gates often fail to detect runtime issues,
violation classes. Listing 5 shows a Gemma-generated solu-
                                                                     allowing vulnerabilities to persist in CI pipelines and skewing
tion for the “String Multiplication” problem. ESBMC proves
                                                                     safety assessments.
a null-pointer dereference (CWE-476), while ASan confirms
                                                                        Multi-tier strategy. Organizations should (1) include run-
a stack-buffer-overflow (CWE-121) on 4 of 5 test cases. Both
                                                                     time instrumentation (ASan/UBSan) in CI (catches 8.6–9.8%
tools identify the same underlying bug (out-of-bounds string
                                                                     of programs static analysis misses); (2) apply bounded model
access) but classify it under different CWE categories.
                                                                     checking selectively to safety-critical code (detects 661 viola-
                              Listing 5                              tions on untested paths at 60s per file); (3) treat passing tests as
     B OTH TIERS DETECT: ESBMC PROVES CWE-476, AS AN CONFIRMS
        CWE-121 ON THE SAME OUT- OF - BOUNDS ACCESS (G EMMA ).       necessary but insufficient (1.8% of test-passing AI programs
                                                                     trigger violations).
1     for (int j = 0; j < pi.length(); ++j) {                           Benchmark as infrastructure. V UL B ENCH -CPP enables
2       temp += pi;
3       // j iterates over pi.length(),
                                                                     evaluation of new models and tools on the same 8,918 anno-
4       // product may be shorter than pi:                           tated programs, supporting reproducible security assessment.
5       // so, product[j] is out of bounds
6       temp += product[j]; // OOB access
                                                                                      VII. T HREATS TO VALIDITY
7     }                                                                 Analysis Accuracy. Static analysis tools may report false
                                                                     positives. Dynamic analysis (ASan/UBSan) provides con-
                                                                     firmed runtime evidence with near-zero false positive rate, but
      RQ3 Finding
                                                                     only covers executed code paths. ESBMC provides proven
      Each tier detects distinct vulnerability classes across        violations with concrete counterexamples but is limited by
      both AI and human code: formal verification proves             loop bounds (unwind 10) and C++ frontend coverage. We
      edge-case violations on untested paths (598 ESBMC-             mitigate these by combining tiers and focusing on comparative
      exclusive), sanitizers confirm runtime undefined be-           trends under fixed configurations.
      havior (576 sanitizer-exclusive), and static analysis             ESBMC Coverage and Configuration Sensitivity. The
      predominantly reports style warnings. While AI and             56.5% parse error rate means formal verification covers only
      human code both exhibit the full spectrum of violation         a subset of programs. The baseline unwind bound (10) and
      classes, their distributions differ systematically per tier,   timeout (60s) mean that violations requiring deeper loop
      explaining the RQ1 gap and demonstrating why no                exploration may not be found. Signed integer overflow (CWE-
      single tier suffices.                                          190) is not captured by --overflow-check (which checks
                                                                     unsigned overflow); it is detected at runtime by UBSan instead.
                                                                     All reported ESBMC FAILED verdicts are proven within the
                          VI. D ISCUSSION                            stated bounds and are therefore valid; they represent a lower
   No single tier suffices. The four verification tiers detect       bound on actual formal violations. A supplementary run with
substantially different violations: formal verification reports      unwind=20 and timeout=120s yields 832 FAILED verdicts at
598 violations that sanitizers do not (typically edge cases          16.8% coverage, confirming that the bound and timeout are
on unexecuted paths), while sanitizers confirm 576 runtime           the primary sensitivity axes.
violations that ESBMC does not report. Critically, 83 sanitizer-        Test Coverage and No-Test Tasks. Sanitizer results depend
confirmed violations occur in programs where ESBMC com-              entirely on test inputs. The 291 instructions without public test
pletes and returns SUCCESS. Static analysis flags both AI            cases contribute 8,918 × (291/851) ≈ 3,058 programs that
and human code at comparable rates but is dominated by low-          cannot be evaluated by the dynamic tier (these programs are
severity warnings and does not separate the two populations.         analyzed by ESBMC and static tools only). Cross-tool anal-
Practitioners relying on static analysis alone risk a false sense    yses are restricted to the 4,295 programs from test-available
of security [22].                                                    problems; dynamic rates for the no-test subset are not reported
   Security debt and verification capacity. The low overlap          and may differ.
between tiers indicates that any single technique leaves blind          AI vs. Human Confounding. Problem difficulty, test-
spots. Confirmed/proven violations constitute “security debt         coverage depth, and code length are potential confounders
principal,” while high-volume static warnings create triage          of the AI-vs-human comparison. Rather than relying on the
overhead that allows defects to survive [23]. The 3.6× higher        aggregate two-proportion test alone, we model these explicitly
sanitizer rate in AI code suggests faster debt accumulation          with the mixed-effects logistic regression reported in Sec-
unless verification capacity (e.g., sanitizer-backed CI) scales      tion V-A5: a random intercept for problem absorbs task-level
with AI adoption. Full analysis of ESBMC configuration               difficulty, and backward elimination retains the covariates that
sensitivity is reported in the replication package.                  matter per tier (correctness for the dynamic tier, LOC for
the static tier). The dynamic-tier AI effect is robust to this       code has grown rapidly. Subsequent studies confirmed the con-
adjustment (OR = 2.15, p < 0.001), whereas the static-tier           cern across settings: ChatGPT-generated C/C++ is frequently
effect is explained by code length, so the headline gap is           insecure on first attempt, with iterative refinement helping only
not an artifact of these confounders. The principal remaining        marginally [5]; prompt-to-CWE benchmarks [24] and Codex
limitation is the formal tier, where ESBMC yields a conclusive       code-smell analyses [6] surfaced recurring weakness patterns;
verdict for too few human programs (96) to support adjusted          and controlled user studies found that developers using AI
inference; we report it descriptively.                               assistants introduce more vulnerabilities, even when security-
   Tool Bias. Our findings are conditioned on specific tool          aware [25], [26]. Closest to our framing, Asare et al. [27]
versions (cppcheck 2.19.0, clang-tidy v21, ESBMC v8.0.0,             report that Copilot’s vulnerability rates are broadly comparable
g++ 13.3.0) and configurations. Different versions or rule sets      to human programmers’, a baseline we extend to three open-
may surface different issues. Clang-tidy was run without a           weight LLMs and four verification tiers. More recently, Dai et
compile_commands.json; missing build flags may affect                al. [7] showed that a single static analyzer gives an incomplete
the accuracy of inter-procedural checks (e.g., bugprone-*)           security assessment even for Python, which we confirm and
but are unlikely to affect the relative AI-vs-human compari-         amplify for C++; SafeGenBench [28] targets vulnerability
son since both groups were processed identically. Alternative        detection rather than multi-tier verification, and Fang et al. [29]
formal verification frontends (e.g., CBMC, VeriFast) were not        find LLMs themselves detect vulnerabilities unreliably.
evaluated; reducing the 56.5% ESBMC parse error rate with               Gap 1: Static-only evaluation of memory-unsafe lan-
a different C++ frontend is left as future work.                     guages. Across these studies, reliance on static analysis or
   Jaccard on ESBMC-Analyzable Subset. The reported                  manual review leaves a blind spot for C++, where buffer over-
Jaccard ≈0.05 between dynamic and formal tiers is computed           flows, use-after-free, and undefined behavior are undetectable
across all 8,918 programs. Restricting to the 2,212 programs         without runtime execution or formal reasoning; static tools can
where ESBMC completed (SUCCESS or FAILED) changes                    then report comparable warning rates while a large confirmed
the denominator but not the 63 jointly-detected programs; the        runtime gap goes unseen. We address this by combining four
full cross-tabulation restricted to this subset is provided in the   tiers and measuring how much their findings overlap rather
replication package and yields a Jaccard of approximately 0.05       than reporting them in isolation.
on the analyzable subset, consistent with the global figure.
                                                                     B. Datasets and Benchmarks for Code Security
   Malformed LLM Output Exclusion. Gemma 3 27B IT
produced malformed outputs for approximately 12% of tasks,              Tihanyi et al. [8] released FormAI, 112,000 AI-generated C
which were excluded from analysis. A sensitivity check re-           programs labeled by static and dynamic analysis and the clos-
taining these programs as “compilation failures” does not            est prior work to ours; FormAI-v2 [9] added newer LLMs [30],
materially change sanitizer or ESBMC rates for the remaining         [31] and ESBMC. Both, however, target C rather than C++, use
programs, since malformed outputs trivially fail all verification    CWE-specific prompts that constrain the vulnerability space,
tiers and their exclusion removes noise rather than signal.          and do not quantify cross-tool agreement. Other benchmarks
   Test Strength and Sanitizer Coverage. Sanitizer trigger           emphasize functional correctness or synthesis rather than secu-
rates depend on test input quality. We did not stratify results      rity, including HumanEval [32], APPS [33], and MBPP [34],
by the number of test cases or the presence of large-input/stress    while SeCodePLT [10] reverse-engineers task descriptions and
tests. Tasks with richer test suites may exhibit higher sanitizer    thereby introduces an intent gap. We adopt CodeContests [12]
rates; this stratification is available in the replication package   as our task source because its competitive-programming prob-
for the 560 tasks with public test cases.                            lems, with test suites and human solutions, elicit vulnerabilities
   Task Domain. Programs are drawn from competitive pro-             that emerge organically rather than through security-targeted
gramming tasks and reflect short, algorithmic code. Vulnera-         prompts.
bility patterns may not generalize to production codebases.             Gap 2: C++ security beyond prompts. V UL B ENCH -CPP
   Prompting Scope. We use a single zero-shot prompt at tem-         is the first C++ security benchmark to combine naturally
perature = 1.0. Different prompting strategies or temperature        occurring tasks rather than CWE-targeted prompts, annotations
settings may alter vulnerability characteristics.                    from five tools across four tiers, and pre-GPT human reference
   Longitudinal Survival. We do not measure longitudinal             solutions for comparison under identical conditions.
survival of security violations in real repositories; instead, we
                                                                     C. Bounded Model Checking for C/C++
relate our findings to survivability results reported in prior
survival-analysis work on AI code.                                      Bounded model checking (BMC) [35] translates a program
                                                                     and its properties into a satisfiability problem, checking all
                    VIII. R ELATED W ORK                             execution paths up to a given loop depth. ESBMC [11]
                                                                     is a state-of-the-art bounded model checker for C/C++ that
A. Security of AI-Generated Code                                     encodes programs as SMT formulas and uses satisfiability
   Since Pearce et al. [3] first evaluated GitHub Copilot at scale   solvers [36] to find property violations with concrete coun-
and reported that roughly 40% of generated programs con-             terexamples. ESBMC has been successfully applied to in-
tained vulnerabilities, security assessment of LLM-generated         dustrial verification [37] and has won multiple categories in
the annual SV-COMP software verification competition [38].          GPT era CodeContests dataset, using the same four-tier veri-
CBMC [39] provides similar capabilities and is widely used          fication pipeline for both. See Table I (presented in Section I
in the verification community.                                      with the contributions) for comparison with closely related
   Tihanyi et al. [8], [9] applied ESBMC to their FormAI            work.
datasets of C programs, representing the first application of
formal verification to AI-generated code security. However,                              IX. C ONCLUSION
they report ESBMC results alongside other tools without
                                                                       This paper set out to test whether AI-generated C++ is
analyzing cross-tool agreement. We extend formal verification
                                                                    measurably less safe than human-written code, and whether
to C++ and, critically, treat cross-tool agreement as a primary
                                                                    the tools practitioners rely on agree on that risk. To answer
research question, quantifying the extent to which dynamic
                                                                    both questions on common ground, we built V UL B ENCH -
analysis and formal verification produce complementary rather
                                                                    CPP, a benchmark of 8,918 C++ programs from three open-
than redundant findings. A key insight motivating our design
                                                                    weight LLMs and human authors across 851 competitive-
is that BMC and sanitizers operate on fundamentally different
                                                                    programming tasks, each annotated under a four-tier verifi-
principles: BMC exhaustively explores all inputs up to a loop
                                                                    cation framework spanning functional testing, static analysis,
bound (detecting bugs with no test input), while sanitizers
                                                                    dynamic analysis, and bounded model checking.
confirm violations only on executed paths (requiring test
                                                                       The three findings reinforce one another into a single, and
coverage). Their near-zero Jaccard agreement in our study is
                                                                    somewhat uncomfortable, conclusion. AI-generated code is not
therefore not a calibration failure but a structural property of
                                                                    merely more vulnerable than human code but reliably so, and
how these tools cover the vulnerability space.
                                                                    in a way that the most commonly used verification tier cannot
D. Non-Determinism and Generation Stability                         see. Dynamic verification exposes runtime violations at 3.6×
                                                                    the human rate (9.3% vs. 2.6%), and formal verification places
   LLM code generation is inherently non-deterministic: the
                                                                    AI violation rates at 25.9–36.7% against 18.8% for human
same prompt can produce structurally different programs
                                                                    solutions, a gap that persists across independent generations,
across independent invocations. Ouyang et al. [40] conducted
                                                                    with within-model variance (≤1.8 pp) far smaller than the
the first systematic study of this phenomenon, finding sig-
                                                                    gap itself. That reproducibility matters: it means the security
nificant variability in ChatGPT’s code generation across re-
                                                                    deficit is a systematic property of these models rather than an
peated queries, including variation in correctness, style, and
                                                                    artifact of any single sample, and can therefore be expected
complexity. Wu and Fard [41] evaluated the communication
                                                                    of future outputs. Yet static analysis alone reports the two as
competence of code generation, finding that models often
                                                                    equally safe. This is the central hazard our multi-tier design
produce inconsistent outputs. Donato et al. [42] studied how
                                                                    surfaces: the tiers agree almost nowhere (cross-tier Jaccard ≈
configuration parameters (temperature, top-p) impact genera-
                                                                    0.05), each catching a different class of violation, 598 edge-
tion quality and consistency.
                                                                    case violations on untested paths from formal verification, 576
   This non-determinism raises a question that prior security
                                                                    runtime violations that formal tools declare safe from sanitiz-
studies have not addressed: are vulnerability patterns repro-
                                                                    ers, and predominantly style warnings from static analysis. A
ducible properties of a model, or artifacts of individual sam-
                                                                    practitioner screening AI-generated C++ with static analysis
ples? If vulnerability rates vary substantially across samples, a
                                                                    alone would conclude, wrongly, that it carries no more risk
benchmark drawn from a single generation may misrepresent
                                                                    than human code.
the model’s typical security behavior. We address this directly
                                                                       We release the benchmark, evaluation harness, and anno-
by generating three independent solutions per model per task
                                                                    tated results so that future models and tools can be assessed
and measuring stability via both aggregate trigger rates and
                                                                    on the same annotated corpus, and so that the multi-tier
pairwise CWE type distributions across generations (RQ3).
                                                                    gap we report can be independently scrutinized. Our find-
E. Positioning and Research Gaps                                    ings are scoped to short, algorithmic C++ under zero-shot
                                                                    generation; extending the study to larger and more realistic
   Summary of Gaps. Prior evaluations of AI code security
                                                                    codebases, to additional LLMs and programming languages,
have two systematic limitations: (1) Gap 1: Language and
                                                                    and to alternative C++ model-checking frontends that reduce
analysis scope. Most studies focus on Python or C with static
                                                                    the current 56.5% ESBMC parse-error rate remains important
analysis alone, leaving C++ and runtime verification under-
                                                                    future work.
explored despite C++’s pervasive use in systems software
where memory safety failures are critical. (2) Gap 2: In-
                                                                                          X. C ONCLUSION
adequate human baselines. Even recent multi-tool studies
(FormAI-v2) [9] do not provide human-written reference so-             This paper evaluated the security of AI-generated C++
lutions collected before the GPT era, making it difficult to        code compared to human-written solutions using a multi-
isolate AI-specific vulnerabilities from general code quality       tier verification framework. By analyzing 8,918 programs in
variation.                                                          the V UL B ENCH -CPP benchmark, we found that AI-generated
   VulBench-CPP addresses both gaps by evaluating AI-               code consistently contains more runtime vulnerabilities than
generated C++ against human-written solutions from the pre-         human code.
   Importantly, static analysis alone does not reveal this differ-          [5] R. Khoury, A. R. Avila, J. Brunelle, and B. M. Camara, “How secure is
ence. Static tools reported comparable warning rates for both                   code generated by ChatGPT?” in 2023 IEEE International Conference
                                                                                on Systems, Man, and Cybernetics (SMC). IEEE, 2023, pp. 2445–2450.
groups, primarily flagging style and code quality issues. Iden-             [6] M. L. Siddiq and J. C. S. Santos, “An empirical study of code smells
tifying the actual vulnerability gap required dynamic analysis                  in transformer-based code generation techniques,” in Proceedings of the
and bounded model checking, which detected entirely different                   22nd IEEE International Working Conference on Source Code Analysis
                                                                                and Manipulation (SCAM ’22). IEEE, 2022, pp. 71–82.
classes of memory-safety errors, including runtime overflows                [7] S.-C. Dai, J. Xu, and G. Tao, “Rethinking the evaluation of secure code
and edge-case bugs on untested paths. Furthermore, these                        generation,” in Proceedings of the 48th International Conference on
vulnerability rates remained stable across independent model                    Software Engineering (ICSE ’26). Rio de Janeiro, Brazil: ACM/IEEE,
                                                                                2026.
generations, indicating they are consistent model behaviors                 [8] N. Tihanyi, T. Bisztray, R. Jain, M. A. Ferrag, L. C. Cordeiro, and
rather than isolated sampling errors.                                           V. Mavroeidis, “The formai dataset: Generative ai in software security
   Organizations using AI to generate C++ should not rely                       through the lens of formal verification,” in Proceedings of the 19th
                                                                                International Conference on Predictive Models and Data Analytics in
solely on static analysis for security screening. Our results                   Software Engineering, ser. PROMISE 2023. New York, NY, USA:
suggest that combining runtime sanitizers and formal verifica-                  Association for Computing Machinery, 2023, p. 33–43. [Online].
tion is necessary to adequately detect these vulnerabilities. We                Available: https://doi.org/10.1145/3617555.3617874
                                                                            [9] N. Tihanyi, T. Bisztray, M. A. Ferrag, R. Jain, and L. C. Cordeiro, “How
release V UL B ENCH -CPP and all evaluation scripts to support                  secure is ai-generated code: a large-scale comparison of large language
further research. Future work will expand this evaluation to                    models,” Empirical Software Engineering, vol. 30, no. 2, p. 47, 2025.
larger codebases and explore alternative formal verification               [10] Y. Nie, Z. Wang, Y. Yang, R. Jiang, Y. Tang, X. Davies, Y. Gal, B. Li,
                                                                                W. Guo, and D. Song, “Secodeplt: A unified benchmark for evaluating
frontends to handle a wider range of C++ features.                              the security risks and capabilities of code genai,” in Advances in Neural
                                                                                Information Processing Systems, vol. 38, 2025.
                             A PPENDIX                                     [11] M. R. Gadelha, F. R. Monteiro, J. Morse, L. C. Cordeiro, B. Fischer, and
                                                                                D. A. Nicole, “ESBMC 5.0: An industrial-strength C model checker,”
   This appendix summarizes additional analysis reported in                     in Proceedings of the 33rd ACM/IEEE International Conference on
the replication package at https://anonymous.4open.science/r/                   Automated Software Engineering (ASE). ACM, 2018, pp. 888–891.
bsa-aigcvul-257B.                                                          [12] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
                                                                                T. Eccles, J. Keeling, F. Gimeno, A. Dal Lago et al., “Competition-
A. A. Per-Model CWE Distributions                                               level code generation with alphacode,” Science, vol. 378, no. 6624, pp.
                                                                                1092–1097, 2022.
   All three AI models exhibit nearly identical cppcheck CWE               [13] Gemma Team, Google DeepMind, “Gemma 3 technical report,” 2025.
distributions dominated by code-quality warnings (CWE-398,                      [Online]. Available: https://arxiv.org/abs/2503.19786
                                                                           [14] Llama Team, AI@Meta, “The llama 3 herd of models,” arXiv preprint
CWE-563), while human code shows higher security-relevant                       arXiv:2407.21783, 2024.
categories (CWE-119, CWE-252). Full per-model breakdowns                   [15] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang,
are in the replication package.                                                 B. Yu, K. Dang et al., “Qwen2. 5-coder technical report,” arXiv preprint
                                                                                arXiv:2409.12186, 2024.
                                                                           [16] OpenRouter, “Openrouter: A unified interface for llms,” 2024. [Online].
B. D. Benchmark Composition                                                     Available: https://openrouter.ai/
   The 851 tasks span 36 problem categories: Implementation,               [17] D. Marjamäki, “Cppcheck: A tool for static C/C++ code analysis,” http:
                                                                                //cppcheck.sourceforge.net, 2007, accessed: December 15, 2025.
Greedy, and Math account for 48.9%, while Data Structures                  [18] The MITRE Corporation, “Common weakness enumeration,” 2024,
and Graphs add 19.3%. Complete category distribution is in                      accessed: February 2026. [Online]. Available: https://cwe.mitre.org/
the replication package.                                                   [19] C. Lattner and V. Adve, “LLVM: A compilation framework for lifelong
                                                                                program analysis & transformation,” in Proceedings of the International
                          AI D ISCLOSURE                                        Symposium on Code Generation and Optimization (CGO).                IEEE
                                                                                Computer Society, 2004, pp. 75–86.
   GitHub Copilot was used for code completion during                      [20] K. Serebryany, D. Bruening, A. Potapenko, and D. Vyukov, “Address-
                                                                                Sanitizer: A fast address sanity checker,” in 2012 USENIX Annual
pipeline development. Claude (Anthropic) was used to assist                     Technical Conference (USENIX ATC), 2012, pp. 309–318.
with drafting and editing portions of the manuscript text. All             [21] E. Stepanov and K. Serebryany, “MemorySanitizer: Fast detector of
generated content was reviewed, verified, and revised by the                    uninitialized memory use in C++,” in 2015 IEEE/ACM International
                                                                                Symposium on Code Generation and Optimization (CGO). IEEE, 2015,
authors. The experimental design, analysis, interpretation of                   pp. 46–55.
results, and scientific conclusions are entirely the authors’ own          [22] A. Bessey, K. Block, B. Chelf, A. Chou, B. Fulton, S. Hallem, C. Henri-
work.                                                                           Gros, A. Kamsky, S. McPeak, and D. Engler, “A few billion lines
                                                                                of code later: Using static analysis to find bugs in the real world,”
                           R EFERENCES                                          Communications of the ACM, vol. 53, no. 2, pp. 66–75, 2010.
                                                                           [23] Z. Li, P. Avgeriou, and P. Liang, “A systematic mapping study on
 [1] J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim, “A survey on large         technical debt and its management,” Journal of systems and software,
     language models for code generation,” ACM Transactions on Software         vol. 101, pp. 193–220, 2015.
     Engineering and Methodology, vol. 35, no. 2, pp. 1–72, 2026.          [24] C. Tony, M. Mutas, M. A. Ferrag, and L. C. Cordeiro, “LLMSecEval:
 [2] GitHub, “Octoverse: The state of open source and ai,” GitHub, Tech.        A dataset of natural language prompts for security evaluations,” in
     Rep., 2024. [Online]. Available: https://octoverse.github.com/             Proceedings of the 20th International Conference on Mining Software
 [3] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri, “Asleep        Repositories (MSR ’23), Data Showcase Track. IEEE, 2023.
     at the keyboard? Assessing the security of GitHub Copilot’s code      [25] N. Perry, M. Srivastava, D. Kumar, and D. Boneh, “Do users write
     contributions,” vol. 68, no. 2. ACM New York, NY, USA, 2025, pp.           more insecure code with AI assistants?” in Proceedings of the 2023
     96–105.                                                                    ACM SIGSAC Conference on Computer and Communications Security
 [4] L. Szekeres, M. Payer, T. Wei, and D. Song, “SoK: Eternal war in           (CCS ’23). ACM, 2023, pp. 2785–2799.
     memory,” in 2013 IEEE Symposium on Security and Privacy (S&P).        [26] G. Sandoval, H. Pearce, T. Nys, R. Karri, S. Garg, and B. Dolan-Gavitt,
     IEEE, 2013, pp. 48–62.                                                     “Lost at C: A user study on the security implications of large language
     model code assistants,” in 32nd USENIX Security Symposium (USENIX
     Security ’23). USENIX Association, 2023, pp. 2205–2222.
[27] O. Asare, M. Nagappan, and N. Asokan, “Is github’s copilot as bad
     as humans at introducing vulnerabilities in code?” Empirical Software
     Engineering, vol. 28, no. 6, p. 129, 2023.
[28] X. Li, J. Ding, C. Peng, B. Zhao, X. Gao, H. Gao, and X. Gu, “Safe-
     genbench: A benchmark framework for security vulnerability detection
     in llm-generated code,” arXiv preprint arXiv:2506.05692, 2025.
[29] C. Fang, N. Miao, S. Srivastav, J. Liu, R. Zhang, R. Fang, R. Tsang,
     N. Nazari, H. Wang, H. Homayoun et al., “Large language models
     for code analysis: Do {LLMs} really do their job?” in 33rd USENIX
     Security Symposium (USENIX Security 24), 2024, pp. 829–846.
[30] OpenAI, “GPT-4 technical report,” arXiv preprint arXiv:2303.08774,
     2023.
[31] B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi,
     J. Liu, R. Sauvestre, T. Remez et al., “Code llama: Open foundation
     models for code,” arXiv preprint arXiv:2308.12950, 2023.
[32] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan,
     H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
     language models trained on code,” arXiv preprint arXiv:2107.03374,
     2021.
[33] D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo,
     C. Burns, S. Puranik, H. He, D. Song et al., “Measuring coding challenge
     competence with apps,” arXiv preprint arXiv:2105.09938, 2021.
[34] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,
     E. Jiang, C. Cai, M. Terry, Q. Le et al., “Program synthesis with large
     language models,” arXiv preprint arXiv:2108.07732, 2021.
[35] A. Biere, A. Cimatti, E. Clarke, and Y. Zhu, “Symbolic model checking
     without bdds,” in International conference on tools and algorithms for
     the construction and analysis of systems. Springer, 1999, pp. 193–207.
[36] L. De Moura and N. Bjørner, “Z3: An efficient smt solver,” in Inter-
     national conference on Tools and Algorithms for the Construction and
     Analysis of Systems. Springer, 2008, pp. 337–340.
[37] M. R. Gadelha, F. Monteiro, L. Cordeiro, and D. Nicole, “Esbmc
     v6. 0: Verifying c programs using k-induction and invariant inference:
     (competition contribution),” in International Conference on Tools and
     Algorithms for the Construction and Analysis of Systems. Springer,
     2019, pp. 209–213.
[38] D. Beyer, “State of the art in software verification and witness validation:
     Sv-comp 2024,” in International Conference on Tools and Algorithms
     for the Construction and Analysis of Systems. Springer, 2024, pp.
     299–329.
[39] D. Kroening and M. Tautschnig, “CBMC–C bounded model checker:
     (competition contribution),” in International Conference on Tools and
     Algorithms for the Construction and Analysis of Systems. Springer,
     2014, pp. 389–391.
[40] S. Ouyang, J. M. Zhang, M. Harman, and M. Wang, “An empirical
     study of the non-determinism of chatgpt in code generation,” ACM
     Transactions on Software Engineering and Methodology, vol. 34, no. 2,
     pp. 1–28, 2025.
[41] J. J. Wu and F. H. Fard, “HumanEvalComm: Benchmarking the com-
     munication competence of code generation for LLMs and LLM agent,”
     ACM Transactions on Software Engineering and Methodology, vol. 34,
     no. 7, pp. 1–42, 2025.
[42] B. Donato, L. Mariani, D. Micucci, and O. Riganelli, “Studying how
     configurations impact code generation in llms: The case of chatgpt,”
     arXiv preprint arXiv:2502.17450, 2025.
