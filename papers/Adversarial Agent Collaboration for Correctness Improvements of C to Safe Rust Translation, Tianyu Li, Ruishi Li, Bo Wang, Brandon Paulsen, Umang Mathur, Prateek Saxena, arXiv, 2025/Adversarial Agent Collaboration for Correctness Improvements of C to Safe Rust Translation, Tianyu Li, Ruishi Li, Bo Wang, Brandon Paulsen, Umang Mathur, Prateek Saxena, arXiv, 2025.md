                                              Adversarial Agent Collaboration for Correctness
                                                Improvements of C to Safe Rust Translation


                                                                            Tianyu Li1     Ruishi Li1    Bo Wang1
                                                                 Brandon Paulsen2        Umang Mathur1         Prateek Saxena1
                                                     1                                                    2
                                                         National University of Singapore, Singapore          Amazon Web Services, USA
arXiv:2510.03879v3 [cs.SE] 17 May 2026




                                                                      {tianyuli, liruishi, bo_wang}@u.nus.edu
                                                                                bpaulse@amazon.com
                                                                        {umathur, prateeks}@comp.nus.edu.sg



                                                                                          Abstract
                                                     Translating C to memory-safe languages, like Rust, prevents critical memory safety
                                                     vulnerabilities that are prevalent in legacy C software. Even with recent LLM-
                                                     based and tool-augmented translators, the resulting Rust code frequently diverges
                                                     from the C source on inputs absent from the test suite used during translation;
                                                     this correctness gap on unseen inputs remains a dominant obstacle to reliable,
                                                     automatic C-to-Rust translation. In this work, we present ACToR (Adversarial C
                                                     To Rust), a simple LLM-agent loop that closes this gap by adversarially searching
                                                     for inputs on which the translation diverges from the C source, and using them
                                                     to drive subsequent refinements. Inspired by GANs, ACToR pits a translator
                                                     agent against a discriminator agent that collaborate to iteratively refine the Rust
                                                     translation. On each iteration, the translator agent synthesizes and refines a Rust
                                                     translation to pass an existing suite of tests, and then the discriminator agent finds
                                                     new failing tests by constructing and refining a differential fuzzer over the C and
                                                     Rust binaries. Across 63 real-world command-line C utilities, with an average size
                                                     of 473 lines of code and the longest reaching thousands of lines in size, ACToR
                                                     achieves over 90% test pass rate with zero human intervention. The improvement
                                                     holds across seven agent–LLM configurations on our micro-benchmark, indicating
                                                     that the loop is largely independent of the choice of underlying translator and LLM.
                                                     Compared to a non-adversarial, coverage-driven test-generation baseline, ACToR
                                                     improves correctness by up to 36.7%. When applied on top of one recent translator,
                                                     C2SaferRust, ACToR further improves the validation pass rate by 16.6%.


                                         1    Introduction
                                         Memory safety vulnerabilities in C/C++ code constitute a large fraction of security vulnerabilities each
                                         year. Microsoft reported 70% of their CVEs are due to memory safety issues [43, 44]. In response,
                                         there has been an increasing demand to translate memory-unsafe legacy code to modern memory-safe
                                         languages like Rust from industry and governments [8], thereby ensuring full memory safety by
                                         design. Unfortunately, given the scale of legacy code that permeates our software systems today,
                                         manual translation of (millions of lines of) existing C code is a formidable and practically infeasible
                                         task. A reasonable translation from C to Rust must use safe and idiomatic Rust programming
                                         abstractions, which are checked mostly at compile time and avoid runtime performance overhead,
                                         unlike memory safety checking directly in C [46, 45, 50, 53].
                                         Existing approaches fall into two categories. Rule-based translators (e.g., c2rust [29] and corrode [54])
                                         produce largely unsafe Rust; converting this unsafe output into safe, idiomatic Rust remains a major
                                         open challenge, with substantial follow-up work on type inference [14, 65, 62, 25], idiom-specific
                                         Preprint.
                                          C Program

       Translator                         Rust Translation                 Discriminator
           Agent                                                           Agent
                                          Test Cases
                                                                           Read
                                                                           Read & Update


Figure 1: High-level overview of ACToR. The Translator and the Discriminator agents update the
translation and the tests in turn to iteratively improve the correctness of the translated program.
refactoring [23, 22, 24], and syntactic rewriting [36]. However, these techniques typically address
only parts of the conversion, and producing fully safe Rust output often still requires manual effort.
LLM-based approaches—including both single-shot translation and agentic setups that iterate on
compiler errors and test failures during translation—produce safer, more idiomatic Rust, but they
share a fundamental correctness gap: the translated code often diverges from the C source on inputs
not exercised by the tests available during translation [34, 1], and several systems report needing
manual intervention or specialized analyses [55, 4, 48, 67, 16].
This is fundamentally a generalization problem: with only a limited test set available during transla-
tion, the translator cannot easily tell whether its output matches the C source’s behavior on unseen
inputs. Augmenting the agent with standard line-coverage tools [18] does not close the gap, as we
show in our evaluation: such tests, while achieving high line coverage, are limited in revealing the
semantic divergences that drive translation toward correctness. Closing this gap requires techniques
that adaptively target divergences between the candidate Rust translation and the C reference program.
In this work, we introduce an adversarial loop that wraps a translator agent and overcomes the
limited generalization observed in non-adversarial agent frameworks. Inspired by the generator–
discriminator paradigm of GANs [19], we employ two collaborating agents: a translator, which
proposes candidate Rust translations, and a discriminator, which actively searches for evidence
(in the form of counterexamples) that the translation diverges from the C source. Whenever the
discriminator identifies such adversarial inputs, these are fed back to the translator, which uses
them to refine subsequent translations. Over iterations, the translator’s output not only passes the
original tests but also withstands the discriminator’s adversarial probing. We refer to this adversarial
translator–discriminator loop as ACToR, for Adversarial C To Rust, as demonstrated in Figure 1.
We evaluate ACToR on two sets of benchmarks: A micro-benchmark set of 6 C programs considered
in recent work, and a macro-benchmark set of 57 C programs from BSDCoreUtils. These 63 real-
world C programs average 473 lines of code, longest in the thousands, totaling around 30k. ACToR
automatically produces Rust translations for all benchmarks that pass more than 90% of tests on
average with zero human intervention during translation. The improvement holds across seven
agent–LLM configurations on our micro-benchmark, indicating that the loop is largely independent
of the underlying translator and LLM. Applied on top of C2SaferRust’s translations on 7 standalone
programs from its benchmark, ACToR raises pass rate by approximately 16.6% (from 76.3% to
92.9%), showing ACToR can complement existing translators to improve correctness.
In addition, we show that ACToR’s adversarial design choice improves pass rates by up to 36.7%
compared with a non-adversarial, coverage-driven test-generation baseline. Against a strong baseline
(Claude Opus 4.6 with no adversarial loop), ACToR with a weaker LLM (Claude-Sonnet-4.5) reaches
98.2% pass rate on the micro-benchmark vs. the strong baseline’s 94.7%, and on the macro-benchmark
wins on 32/57 programs (vs. 3/57; 22 non-discriminating ties). This suggests the adversarial loop can
compensate for differences in underlying LLM capability. The adversarial loop is also not tied to
proprietary models: applied with the open-weights GLM 4.7 (via Mini-SWE-Agent), ACToR reaches
95.3% pass rate on the micro-benchmark, comparable to the strong baseline’s 94.7%. Our code,
benchmarks, and resulting translations are provided as supplementary material and will be released
publicly upon publication.




                                                   2
2     Related Work
Automated translation of C to Rust is a relatively recent approach towards achieving full memory
safety [13]. The desired goal of such translation is to generate safe1 Rust code corresponding to C
code, i.e., Rust code that uses only idiomatic Rust primitives that the compiler can statically verify or
trust to be memory safe. While several prior works have made progress along distinct objectives (e.g.,
type inference, scalability via decomposition), achieving full correctness of the translated Rust code
remains a major challenge [34].

2.1    C to Rust Translation

Existing works on C-to-Rust translation can primarily be categorized as rule-based or LLM-based
techniques. Rule-based techniques such as c2rust [29] and corrode [54] opt for mechanical, line by
line, rewriting of the C code, often resorting to raw pointers and unsafe Rust. Later efforts explored
ways to infer Rust types from C code, either by compiler feedback [14, 25], SMT solving [65],
data-flow graphs [62], or syntactic rewriting [36], and specialized analyses targeted idioms like
tagged unions [23], output parameters [22], and file APIs [24]. Beyond general C, Low* compilation
to Rust [17] demonstrates scalable translation in restricted settings, though such techniques remain
infeasible for general-purpose C due to expressiveness and unmodeled APIs.
LLM-based approaches use an LLM to propose a translation [32]. Recent work augments models
with different kinds of tools. These include test generation tools [15, 63], dynamic pointer analy-
ses [55], or multi-modal prompting [47]. Function-level decomposition has been explored to improve
scalability [57, 4, 51], while agentic workflows combine LLMs with static analysis [67, 16]. Neural
methods yield more idiomatic code, yet often fall short of preserving exact input/output behavior.
Moreover, behavior often diverges from the C source on inputs outside the test suite used during
translation. Studies echo these concerns: decomposition introduces inconsistencies [34], and LLMs
remain prone to subtle errors [1].
Existing C-to-Rust systems make distinct design tradeoffs. Some prioritize scalability through
decomposition or static analysis [48, 4]; others target fully safe Rust output but do not aim for
compilable end-to-end translations [25]; yet others trade automation for correctness via dynamic
profiling and human-in-the-loop refinement [55]. Table 1 positions these systems along several
dimensions. To our knowledge, ACToR is the only system in this space that targets both fully
safe Rust and correctness on inputs unseen during translation without human intervention. The
adversarial loop is also complementary to these systems: any of the LLM-based translators in the
table can in principle serve as the underlying translator that ACToR’s discriminator augments.

Table 1: ACToR positioned against representative LLM-based prior C-to-Rust systems. “Translator”
distinguishes single-shot LLM calls (LLM) from interactive coding agents (Agent). “Correctness”
indicates whether reported pass rates are measured on tests held back from the translator (hidden
tests) or shared with it (given tests). “–” marks dimensions that do not apply or are not reported.
 System                   Analysis      Translator   No Human       Safe Rust        Correctness          Eval Size
 ACToR (this paper)           –           Agent           ✓           ✓         Hidden tests, ∼95%       ∼30k LoC
 Tymcrat [25]            Lightweight      LLM             ✓           ✓            – (signatures)       ∼800k LoC
 C2SaferRust [48]           Static        LLM             ✓            –        Given tests, partial    ∼270k LoC
 Syzygy [55]              Dynamic         LLM             –           ✓         Given tests, partial      ∼3k LoC
 EvoC2Rust [59]          Lightweight      Agent           –          Mostly     Given tests, partial      ∼8k LoC
 SmartC2Rust [57]             –           LLM             ✓          Mostly       Given tests, full      ∼40k LoC
 IRENE [38]                 Static        LLM             ✓          Mostly     Given tests, partial        Small



2.2    Collaborative LLMs & Agents

Many works propose multi-LLM and multi-agent systems, where the LLMs or agents collaborate to
produce a final answer. Many works on code generation propose specific roles, such as coder, tester,
or analyst, which collaborate to write code [41, 6, 11, 27, 52, 30]. Collaborative approaches have been
used outside of code generation as well. Many works propose self-reflection techniques [56, 39, 9],
    1 The use of unsafe keyword in Rust allows mixing unchecked and possibly memory unsafe code in otherwise safe Rust




                                                          3
sometimes aided by tools [1, 21, 10], where the LLM first proposes an answer, then reflects on its
answer to improve accuracy. Similar works propose multi-agent debate architectures [5, 12, 35, 26,
60, 37] where multiple answers are proposed, then the LLM(s) debate the correct answer. Several
works propose frameworks for agent collaboration [26, 60, 37].
The key difference between ours and prior work is in the high-level principle: To reliably improve
the translated code, we leverage the C program as the oracle in the construction of a discriminator,
which automatically identifies correctness gaps and provide iterative feedback to the translator.

3     ACToR Design
Given a C program and a seed test set, ACToR produces a safe Rust translation that generalizes
beyond the seeds. This section formalizes the translation problem, identifies the generalization gap,
and introduces the adversarial loop that narrows it.

3.1   Problem Formulation

Given a source C program c, an ideal translation is a safe Rust program rs whose external behavior
— standard output, error messages, file modifications, and so on — agrees with c on every input in
the safe universe U , defined as the set of inputs that do not trigger memory-unsafety in c. Formally,
we want rs to satisfy the Boolean requirement IsEq(c, rs), where IsEq is an oracle reporting
equivalence over all of U . For inputs outside U , memory-safe handling is guaranteed by the safe Rust
compiler itself.
However, existing LLM-based translators do not yet produce such an ideal translation. A standard
setup provides translator F with the C program c and a small seed test set T0 , returning a Rust
program rs = F (c, T0 ) that passes those tests. This ensures only the pointwise check IsEq∗ (c, rs, t)
on t ∈ T0 , where IsEq∗ runs both programs on input t and reports whether they match. On
unseen t ∈ U \ T0 , IsEq∗ (c, rs, t) may fail, so rs does not satisfy IsEq(c, rs) over all of U — a
generalization gap that we observe empirically (Sec. 4).
Our aim in this paper is to develop a methodology M that wraps the translator F to narrow this gap.
Given rs = F (c, T0 ), M produces an improved translation rs′ = M (F, c, T0 ) that agrees with c on
more unseen inputs than rs.

3.2   Adversarial Translation Loop

We instantiate this methodology as an adversarial translation loop between two LLM agents, inspired
by GANs: a translator agent that produces a Rust translation, and a discriminator agent that searches
for inputs on which the C and Rust programs disagree. The two agents work in turn, iteratively im-
proving the translation, with the discriminator pushing the translator to fix newly exposed mismatches.
The full pseudocode is given as Algorithm 1 in Appendix A.
Given the C program c, the seed test set T0 , a translator agent F , and a discriminator agent D, ACToR
produces an improved Rust translation rs′ :
                                      rs′ = ACToR(F, D, c, T0 ).
D, the discriminator agent, surfaces mismatches via static inspection, manual testing, and a customiz-
able differential fuzzer that the agent adjusts to fit each program’s input space and efficiently explore
inputs. Fuzzer construction is enabled by default; we ablate the no-fuzzer variant (ACToR-NoFuzz)
in Sec. 4.2. The translator F is intentionally abstract: here we instantiate it as an LLM coding agent.
ACToR can also post-process an existing Rust translation (e.g., output of C2SaferRust).
ACToR maintains an append-only test set T , initialized to the seed set T0 . Initialization. The
translator produces an initial safe Rust translation rs′ that passes all of T0 before the adversarial loop
begins. Discriminator step. Reading c and the current rs′ , the discriminator emits a batch of tests on
which their outputs disagree; each test is required to be well-formed and to execute successfully on c
before being appended to T . Translator step. The translator updates rs′ to pass the enlarged T while
using only safe Rust; if it cannot fully pass after a fixed number of retries, the loop continues with
the latest rs′ retained, even when some tests in T remain failing. After at most M AX I TER iterations,
ACToR returns the final rs′ and the accumulated test set T .


                                                    4
ACToR ensures the loop executes as expected through validation of F and D, and file sandboxing.
The translator’s output rs′ is validated to contain no unsafe constructs and to pass all tests in the
current T ; on failure, the translator restarts within a retry limit. The discriminator’s tests are validated
to be well-formed, execute successfully on c, and disclose mismatches before being appended to T .
Each agent additionally runs in a sandboxed workspace where its writes are effectively restricted to
the files it controls (translator: Rust source; discriminator: tests), with c and build scripts read-only to
both. Implementation details of the validator and sandbox are deferred to Appendix B.

4     Evaluation
Ideally, a successful C-to-Rust translation preserves the C program’s behavior on inputs unseen
during translation, and produces fully safe Rust. We evaluate ACToR on the following criteria:

      1. Correctness on unseen inputs. Do ACToR’s translations preserve the C program’s behavior
         on inputs not seen during translation? Are the translations fully safe Rust?
      2. Mechanism applicability. Does the same adversarial loop transfer across different translator
         agents, LLMs, and program sizes?
      3. Ablation. How does the adversarial loop compare against alternative translators and alterna-
         tive test-generation strategies? How sensitive are results to configuration choices?

4.1   Experiment Settings


                                      Table 2: Benchmark Statistics
                (a) Micro Benchmark                            (b) Macro Benchmark by Category
        Program      LOC      Funcs    Cov.              Category             LOC      Funcs     Count
        printf        371        11    95%               Text Processing     13269       355        21
        expr          452        17    92%               File Dir. Mgmt.      6683       151        15
        fmt           416        12    91%               Scripting Utils      4204       118         8
        test          528        17    78%               Sys. Info Status     2908        70        10
        join          475        10    90%               Env. Proc. Ctrl.      204         8         3
        csplit        303         7    88%               Total               27268       702        57
        Total        2545        74    89%

Benchmarks. Our evaluation uses two sets of benchmarks: a micro-benchmark set and a macro-
benchmark set. The micro-benchmark comes from a prior user study on C to Rust translation, which
contains 6 standalone C programs, with an average of 424 lines of code each [34]. We extend the
validation suite to at least 60 test cases per program (89% average line coverage), which are used to
evaluate the correctness of translations. We use this small-scale benchmark to demonstrate ACToR’s
ability to adapt to different LLMs and coding agent frameworks, and to perform an ablation study.
Our main macro-benchmark is a set of 57 real-world system utility programs (e.g., ls, cp, xargs)
obtained from a software project named BSDCoreUtils [40]. It has an average of 478 lines of
code each. More details about how we filter the benchmark are reported in Appendix D. We use
this benchmark to demonstrate ACToR’s correctness improvement on real-world programs, and
to compare its adversarial loop against alternative translators and the coverage-driven baseline.
Given the large number of programs, manually crafting a comprehensive set of test cases for each
macro-benchmark is infeasible, and existing test suites for similarly-named GNU utilities are not
directly applicable due to documented BSD/GNU behavioral differences. Moreover, automated test
generation techniques can produce test sets that unfairly advantage a specific translation approach.
Instead, we perform a relative evaluation between ACToR and baselines, as described below in the
Evaluation Metrics section.
To minimize measurement noise and make our experiments automatable, our evaluation focuses on
single-threaded C programs that have deterministic behaviors across different executions, which
is currently an assumption of our testing framework that both the translator and the discriminator
depends on. Table 2 summarizes the statistics of two benchmarks, where we categorize the 57


                                                     5
programs into five categories: process execution control, file/directory management, shell scripting
commands, system information access, and textual content processing.
Test Format and Testing Setup. As the adversarial procedure progresses, newly generated test
inputs are continuously added to the test set. To efficiently manage and execute these tests, we enforce
a fixed test format and design a unified test runner that works for all benchmark programs. Each test
case is specified in a JSON format that defines the program input and the execution configurations.
The configuration includes commands for test setup and cleanup, instructions for redirecting result
files to standard output for comparison, and regular-expression rules to normalize outputs and filter
out trivial differences (e.g., path names). The test runner automatically executes the given set of tests
for each program, runs both the C and Rust implementations with identical inputs, compares their
outputs, and produces coverage reports, according to the provided command-line arguments.
Agent Frameworks and Models. We use Claude Code [2] with Claude Sonnet 4.5 [3] as the main
agent framework and LLM for our experiments. To test if our approach generalizes to other agent
frameworks and LLMs, we also performed experiments using Mini-SWE-Agent [58], a popular open-
source agent framework, with Claude 4.5 Sonnet, Claude 4 Sonnet, GPT 5 mini [49], Gemini-3.1-
Pro [20], and one open source model, GLM-4.7 [64], as the LLMs. We use ‘ClaudeCode+Sonnet4.5’,
‘ClaudeCode+Sonnet4‘, ‘SWE+Sonnet4.5’, ‘SWE+Sonnet4’, ‘SWE+GPT5mini’, ‘SWE+GLM4.7‘,
‘SWE+Gemini3.1-Pro‘ to represent them in later sections, respectively. The detailed version of the
agent and model is reported in Appendix C.
Comparison Baselines. We compare ACToR against four baselines: (1) Naive baseline: a single
translator agent identical to ACToR’s, instructed to pass initially provided tests (seed tests in ACToR)
without iterating to add tests or refine the code. (2) Strong baseline: a single agent without iteration,
but backed by a much stronger closed-source LLM (Claude Opus 4.6). (3) Coverage baseline: a
two-agent setup similar to ACToR, but the discriminator agent is only instructed to find additional
tests that increase the line coverage of the C program, so the new tests do not specifically try to reveal
inequivalent behavior. (4) ACToR-NoFuzz: ACToR but without fuzzer construction. Comparison
against (1), (3), and (4) isolates the gain from, respectively, ACToR’s iterative loop, its adversarial
test-generation strategy, and its agent-driven differential fuzzer; comparison against (2) calibrates
these gains against a stronger underlying LLM. We also check whether ACToR can improve the
correctness of Rust translations produced by C2SaferRust, one of the recent works whose translations
are public, compilable, and executable [48].
Evaluation Metrics. Our primary evaluation metric to evaluate the correctness of an individual
translation is pass rate, which is the percentage of tests that pass for a given set of tests. On our micro-
benchmark, we report the pass rate on manually written validation tests when we evaluate different
configurations of ACToR only (e.g., different LLM–agent settings or experiment hyperparameters).
When we compare ACToR against other translation methods, we compute pass rates using a set of
tests produced by a competing method, and refer to this metric as relative pass rate. This reduces
bias from a method overfitting to its own tests (in practice, a method usually passes almost all of its
own tests) and provides a stronger signal for cross-method comparison. We use relative pass rate for
(i) ablation studies that compare ACToR against alternative designs on the micro-benchmark, and
(ii) the final experiment on the macro-benchmark, which lacks manually written tests and therefore
relies solely on test suites generated by the methods. The test sets used to compute relative pass rate
achieve an average of 92.6% line coverage on the micro benchmark and 90.1% line coverage on the
macro benchmark, by unioning test cases across translation methods. This indicates they are a useful
signal for overall correctness as well.
Qualitative Requirements. ACToR aims to translate C code into fully safe Rust. Across both bench-
marks, we enforced the absence of any unsafe blocks at every iteration. After all the experiments
finished, we manually reviewed the final translations output by ACToR, confirming they are indeed
safe and contain no malicious constructs intended to bypass the checking.
Experimental Configuration. We fixed a configuration to compare different agent settings and
translation methods on the micro-benchmark. By default, ACToR and all baselines start with 15
manually crafted, diverse seed tests based on the C code for each program2 . For the coverage
baseline, ACToR-NoFuzz, and ACToR, we run 10 iterations of the adversarial loop. On each
iteration, we generate 3 new tests, resulting in a total of 45 tests per program in the end. We fix these
   2 The seed tests carry intended test format that both translator and discriminator of ACToR use. It also avoids a cold-start

that produces translations in poor quality at the first few iterations for ACToR as well as all other systems we compare to.


                                                              6
parameters because exploring different configurations for all agent–model settings and translation
methods would be prohibitively costly. We conduct an ablation experiment to study the influence of
different experiment configurations on the final correctness and cost of ACToR, and apply the default
configuration to translate the macro-benchmark. See the Appendix E for the prompt templates.

4.2   Evaluation Result on Micro Benchmark




Figure 2: Overall pass rate (on hidden tests) on the micro benchmark across 7 agent–LLM configura-
tions, comparing ACToR (green, iter 10) with the naive baseline (cyan, initial translation) and the
strong baseline (Claude Opus 4.6, no iteration).

Correctness & Adaptability. We compare ACToR against the naive baseline (per agent–LLM
configuration) and the strong baseline (Claude Opus 4.6). The aggregate results are shown in
Figure 2; per-program results are provided in Appendix F. All translations from ACToR and the
baselines are free of unsafe blocks. ACToR consistently improves the translation correctness on
all 7 agent-model settings. With Claude Code and Claude-Sonnet-4.5, the validation pass rate rises
from an average of 89.2% (naive baseline) to 98.2% after 10 iterations. With Mini-SWE-Agent,
completing 10 iterations improves correctness by 4.7% to 8.8% across the five LLMs. Against the
strong baseline (94.7%), ACToR with Claude-Sonnet-4.5 (98.2%) is higher despite a less capable
LLM. This suggests that the iterative refinement provides value beyond what is gained from using a
stronger underlying model alone. The consistent gains across all seven configurations further indicate
the loop transfers across underlying translators. We use Claude Code + Sonnet-4.5 as the default
configuration for the following experiments. With this configuration, it takes 411 million tokens to
finish 6 programs, which costs $201 USD in total. The average time cost for ACToR to finish one
program is approximately 2.45 hours3 .
Ablation Study on Design. We conduct an ablation to know how the adversarial design in
ACToR drives correctness gains on the micro-benchmark. We compare three variants of ACToR—
coverage-baseline (replacing the adversarial discriminator with non-adversarial test generation),
ACToR-NoFuzz (without the fuzzing script), and the full ACToR—to isolate the contributions of
the adversarial discriminator and the use of the fuzzing script. The cross-testing results (shown on
the left of Figure 3) report the relative pass rate of each method (row) on the tests generated by the
other methods (column). While all methods pass most of their own tests, the adversarial variants
generalize much better across tests. On coverage-guided tests, ACToR-NoFuzz and the full ACToR
achieve 90% and 94% pass rates, respectively, whereas the coverage-guided baseline achieves less
than 40% on tests from either adversarial variant. This indicates that adversarially generated tests are
more effective at exposing semantic mismatches than coverage-guided sampling. The full ACToR
further improves over ACToR-NoFuzz in cross-testing (71%→73%), suggesting that the customized
fuzzer helps the discriminator find more challenging bugs. To better understand cost-effectiveness,
we also run an equal-cost experiment in which we extend the coverage baseline to 25 iterations,
roughly matching the cost of running ACToR for 10 iterations. However, even under equal budget,
the coverage baseline’s pass rate (75/177 = 42.4%) remains far below that of ACToR (425/447 =
95.1%). More details about this ablation study and equal-cost experiment are reported in Appendix G.
Ablation Study on Configurations. We also study how different configurations affect ACToR on
the micro-benchmark. We examine three factors: seed tests, number of iterations, and number of
   3 The token consumption is computed by summing up the input, output, and cached tokens reported in the API response

messages. When computing the time cost, we first compute the average time cost per iteration, then times it by 10 as an
approximation of the total runtime for translating one program.


                                                          7
Figure 3: (Left) The relative comparison among 3 translation methods on Claude Code with Sonnet-
4.5. Entry (row, column) is the relative pass rate of the row’s translation on the column method’s tests.
(Right) The validation pass rate of ACToR on different configurations. Pass rate versus the number
of new test cases added per iteration (Top). Pass rate versus the number of iterations (Bottom).




Figure 4: On the macro benchmarks, the relative pass rate when cross-comparing ACToR and
coverage baseline (Cov-Base) on Claude Code with Claude-Sonnet-4.5 at iteration 10. For each
program, the left bar shows evaluating the translation from ACToR on tests generated in coverage-
baseline; the right bar is evaluating the translation from coverage-baseline on ACToR’s tests. The
length of each program in LoC is presented next to the program name.
tests generated by the discriminator agent per iteration. Details are in Appendix H. Figure 3 (right)
shows the results. The results show that the default configuration, which uses 15 initial seed tests, 10
iterations, and 3 new tests per iteration, achieves a favorable balance between performance and cost.
Increasing tests per iteration yields diminishing returns: 3 tests instead of 1 improves pass rate from
94.7% to 98.2% with a 16% cost increase, while 5 tests adds only 1.4% at an additional 29% cost.
Most gains occur within the first 10 iterations; extending to 20 iterations adds only 1.4% at 2.1× cost.
Finally, using 15 seed tests instead of a single seed test improves pass rate from 94.9% to 98.2% with
only a 6% cost increase, suggesting that richer initial coverage is beneficial.
Stability of Results. To assess the stability of ACToR ’s translation results, we run ACToR three
times using the default settings (i.e., 15 initial tests, 10 iterations, and 3 tests per iteration). We record
the pass rate of each trial on the validation set. For each program, we compute the sample standard
deviation of the three pass rates and then average these standard deviations across all programs. On
average, the three runs achieve a pass rate of 97.0%, with a deviation of 1.9%.


 On the micro-benchmark, ACToR substantially and stably improves translation correctness over
 the non-adversarial baselines. The adversarial discriminator is crucial to improving correctness,
 and the fuzzer construction further strengthens the discovery of mismatches.




                                                      8
4.3    Evaluation on Macro Benchmark

We compare ACToR against two baselines on the macro benchmark: the coverage baseline (using
relative pass rate) and the strong baseline (Claude Opus 4.6, evaluated on the coverage baseline’s
tests for a fair comparison with ACToR). We use the Claude Code agent and Claude-Sonnet-4.5 for
this experiment4 . All ACToR translations are free of unsafe blocks.
Figure 4 shows the cross-comparison at iteration 10. The left bar for each program is the relative
pass rate of testing ACToR’s translation on the test cases from the coverage baseline. The right bar
shows the reverse: relative pass rate of the coverage baseline against ACToR’s test cases. ACToR
outperforms the coverage baseline on 54/57 programs. ACToR gets 100% relative pass rate on 34
programs when running on the tests from the coverage baseline, while the coverage baseline can only
get full pass on 3 programs. On average, ACToR achieves 95.1% relative pass rate, 36.7% higher
than the coverage baseline’s 58.4%. The cross-comparison confirms that adversarial agentic design
in ACToR plays a significant role in improving the translation correctness. As an absolute measure,
by taking the union of the test cases from both ACToR and the coverage baseline, we get a test set of
an average 90.1% coverage. ACToR achieves a 95.9% pass rate on it. This shows ACToR’s utility on
real-world projects. The total financial costs to translate 57 programs using the coverage baseline
and ACToR are $808 USD and $1634 USD, respectively. On average, ACToR consumes 57 million
tokens per program, with more than 97% of them being cache-read tokens. The average time cost for
ACToR to finish one program is about 2.5 hours.
Against the strong baseline (Claude Opus 4.6), we compare ACToR and the strong baseline on the
coverage-baseline tests (neither method sees them during translation). Across the 57 programs,
ACToR wins 32, the strong baseline wins 3, and the two tie on 22 programs where the tests cannot
distinguish them. On the 35 discriminating programs, ACToR wins 32 (91%), confirming the micro-
benchmark pattern at scale: the gain from ACToR’s adversarial loop is not closed by simply switching
to a stronger underlying LLM.
Augmenting C2SaferRust. We also test ACToR as a correctness-improvement layer on top of
C2SaferRust [48], one recent C-to-Rust translator. From C2SaferRust’s benchmark, we filter
out libraries that are not independently testable, leaving 7 standalone executable programs within
ACToR’s scope, and seed ACToR with C2SaferRust’s translation as the initial Rust input. Because
C2SaferRust’s output contains unsafe blocks, we relax ACToR’s strict safe-Rust requirement for
this experiment: the translator agent may keep existing unsafe code but is instructed not to introduce
additional unsafe lines. On a held-out validation test suite, applying ACToR raises pass rate by
approximately 16.6% (from 76.3% to 92.9%) over C2SaferRust’s translations alone, showing that
ACToR can complement existing translation techniques to further improve correctness (Sec. 3.2).

 ACToR improves correctness on the BSDCoreUtil benchmark: it outperforms the coverage-driven
 baseline on 54/57 programs (95.1% vs. 58.4% relative pass rate) and the strong baseline (Claude
 Opus 4.6) on 32/57 programs with 22 non-discriminating ties. As a layer on top of C2SaferRust,
 ACToR helped raise the pass rate on hidden tests from 76.3% to 92.9%.


4.4    Limitations

ACToR currently targets standalone command-line programs and does not directly support library
translation, due to the lack of a precise equivalence notion when program behaviors are language-
specific—known to be hard to automatically determine [28], especially when library interfaces and
types differ across languages. Existing work targeting C-to-Rust library translation often addresses
this with manually vetted test drivers, one written for each language to drive the library’s interface
(e.g., CRUST-Bench [31]); integrating such test-driver synthesis with our discriminator’s adversarial
fuzzing is left to future work. Our macro evaluation uses closed-source models. However, the micro-
evaluation has shown that the adversarial loop generalizes across multiple agent–LLM configurations
with consistent gains, suggesting the same pattern would hold across other model families.


   4We run macro evaluation on both Claude-Sonnet-4 and Claude-Sonnet-4.5. Due to space limitations, we put the result of

Claude-Sonnet-4 in Appendix I for reference. The results are consistent between two trials.


                                                             9
5   Conclusion
We present ACToR, an agent-based automatic translation approach that aims for functionally correct
C to Rust translations. Our method introduces a collaborative pipeline in which two agents iteratively
refine the translations. At each iteration, the discriminator agents detect the semantic mismatches
between the source code and the translated program, and report them as failing test cases. The
translator agents then improve the translation to pass the current test set. Our experiments demonstrate
the power of ACToR’s adversarial agentic setup to produce translations with high correctness,
surpassing the quality of translation as compared to non-adversarial setups. A noteworthy advantage
of ACToR is that its adversarial loop is largely independent of the underlying translator and LLM.
ACToR also composes with existing translators: applied on top of C2SaferRust’s outputs, it further
improves the pass rate on hidden tests.

References
 [1] Lost in Translation: A Study of Bugs Introduced by Large Language Models while Translating
     Code, January 2024. URL http://arxiv.org/abs/2308.03109. arXiv:2308.03109 [cs].
 [2] Anthropic. Claude code. Website, 2025.                 URL https://claude.com/product/
     claude-code. Accessed: 2025-09-24.
 [3] Anthropic. Claude sonnet 4.5. Website, 2025. URL https://www.anthropic.com/claude/
     sonnet. Accessed: 2025-11-20.
 [4] Xuemeng Cai, Jiakun Liu, Xiping Huang, Yijun Yu, Haitao Wu, Chunmiao Li, Bo Wang, Imam
     Nur Bani Yusuf, and Lingxiao Jiang. Rustmap: Towards project-scale c-to-rust migration via
     program analysis and llm. arXiv preprint arXiv:2503.17741, 2025.
 [5] Chi-Min Chan, Weize Chen, Yusheng Su, Jianxuan Yu, Wei Xue, Shanghang Zhang, Jie
     Fu, and Zhiyuan Liu. Chateval: Towards better LLM-based evaluators through multi-agent
     debate. In The Twelfth International Conference on Learning Representations, 2024. URL
     https://openreview.net/forum?id=FQepisCUWu.
 [6] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu
     Chen. Codet: Code generation with generated tests. In The Eleventh International Conference
     on Learning Representations, 2023.
 [7] Chuyang Chen, Brendan Dolan-Gavitt, and Zhiqiang Lin. ELFUZZ: efficient input generation
     via LLM-driven synthesis over fuzzer space. USENIX Association, USA, 2025. ISBN 978-1-
     939133-52-6.
 [8] DARPA. Tractor: Translating all c to rust. DARPA website, 2025. URL https://www.darpa.
     mil/research/programs/translating-all-c-to-rust. Accessed: 2025-09-23.
 [9] Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Celikyilmaz,
     and Jason Weston. Chain-of-verification reduces hallucination in large language models. arXiv
     preprint arXiv:2309.11495, 2023.
[10] Guanting Dong, Keming Lu, Chengpeng Li, Tingyu Xia, Bowen Yu, Chang Zhou, and Jingren
     Zhou. Self-play with execution feedback: Improving instruction-following capabilities of large
     language models. In The Thirteenth International Conference on Learning Representations,
     2025.
[11] Yihong Dong, Xue Jiang, Zhi Jin, and Ge Li. Self-collaboration code generation via chatgpt.
     ACM Transactions on Software Engineering and Methodology, 33(7):1–38, 2024.
[12] Yilun Du, Shuang Li, Antonio Torralba, Joshua B Tenenbaum, and Igor Mordatch. Improv-
     ing factuality and reasoning in language models through multiagent debate. In Forty-first
     International Conference on Machine Learning, 2023.
[13] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. Translating c to safer
     rust. Proc. ACM Program. Lang., 5(OOPSLA), October 2021. doi: 10.1145/3485498. URL
     https://doi.org/10.1145/3485498.
[14] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf.
     Aliasing limits on translating c to safe rust. Proceedings of the ACM on Programming Languages,
     7(OOPSLA1):551–579, 2023.


                                                  10
[15] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, Joey Dodds,
     and Daniel Kroening. Towards translating real-world code with llms: A study of translating to
     rust. arXiv preprint arXiv:2405.11514, 2024.
[16] Muhammad Farrukh, Smeet Shah, Baris Coskun, and Michalis Polychronakis. Safetrans:
     Llm-assisted transpilation from c to rust. arXiv preprint arXiv:2505.10708, 2025.
[17] Aymeric Fromherz and Jonathan Protzenko. Compiling c to safe rust, formalized, 2024. URL
     https://arxiv.org/abs/2412.15042.
[18] GNU. gcov. Website, 2025. URL https://man7.org/linux/man-pages/man1/
     gcov-tool.1.html. Accessed: 2025-09-24.
[19] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil
     Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial networks. Commun.
     ACM, 63(11):139–144, October 2020. ISSN 0001-0782. doi: 10.1145/3422622. URL https:
     //doi-org.libproxy1.nus.edu.sg/10.1145/3422622.
[20] Google. Gemini 3.1 pro. Website, 2025. URL https://docs.cloud.google.com/
     vertex-ai/generative-ai/docs/models/gemini/3-1-pro. Accessed: 2026-05-06.
[21] Zhibin Gou, Zhihong Shao, Yeyun Gong, Yujiu Yang, Nan Duan, Weizhu Chen, et al. Critic:
     Large language models can self-correct with tool-interactive critiquing. In The Twelfth Interna-
     tional Conference on Learning Representations, 2024.
[22] Jaemin Hong and Sukyoung Ryu. Don’t write, but return: Replacing output parameters with
     algebraic data types in c-to-rust translation. Proc. ACM Program. Lang., 8(PLDI), June 2024.
     doi: 10.1145/3656406. URL https://doi.org/10.1145/3656406.
[23] Jaemin Hong and Sukyoung Ryu. To tag, or not to tag: Translating c’s unions to rust’s
     tagged unions. In Proceedings of the 39th IEEE/ACM International Conference on Automated
     Software Engineering, ASE ’24, page 40–52, New York, NY, USA, 2024. Association for
     Computing Machinery. ISBN 9798400712487. doi: 10.1145/3691620.3694985. URL https:
     //doi.org/10.1145/3691620.3694985.
[24] Jaemin Hong and Sukyoung Ryu. Forcrat: Automatic i/o api translation from c to rust via origin
     and capability analysis, 2025. URL https://arxiv.org/abs/2506.01427.
[25] Jaemin Hong and Sukyoung Ryu. Type-migrating c-to-rust translation using a large language
     model. Empirical Software Engineering, 30(1):3, 2025.
[26] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao
     Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng
     Xiao, Chenglin Wu, and Jürgen Schmidhuber. MetaGPT: Meta programming for a multi-agent
     collaborative framework. In The Twelfth International Conference on Learning Representations,
     2024. URL https://openreview.net/forum?id=VtmBAGCN7o.
[27] Dong Huang, Jie M Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming Cui.
     Agentcoder: Multi-agent-based code generation with iterative testing and optimisation. arXiv
     preprint arXiv:2312.13010, 2023.
[28] Ali Reza Ibrahimzada, Brandon Paulsen, Reyhaneh Jabbarvand, Joey Dodds, and Daniel
     Kroening. Matchfixagent: Language-agnostic autonomous repository-level code translation
     validation and repair. arXiv preprint arXiv:2509.16187, 2025.
[29] Immunant. c2rust: Migrate C code to Rust. https://github.com/immunant/c2rust.
     Accessed: July 4, 2023.
[30] Md. Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. MapCoder: Multi-
     agent code generation for competitive problem solving. In Lun-Wei Ku, Andre Martins,
     and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for
     Computational Linguistics (Volume 1: Long Papers), pages 4912–4944, Bangkok, Thailand,
     August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.269.
     URL https://aclanthology.org/2024.acl-long.269/.
[31] Anirudh Khatry, Robert Zhang, Jia Pan, Ziteng Wang, Qiaochu Chen, Greg Durrett, and Isil
     Dillig. Crust-bench: A comprehensive benchmark for c-to-safe-rust transpilation, 2025. URL
     https://arxiv.org/abs/2504.15254.
[32] Marie-Anne Lachaux, Baptiste Roziere, Lowik Chanussot, and Guillaume Lample. Unsuper-
     vised translation of programming languages. arXiv preprint arXiv:2006.03511, 2020.


                                                11
[33] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K. Lahiri, and Siddhartha Sen. Codamosa:
     Escaping coverage plateaus in test generation with pre-trained large language models. In
     Proceedings of the 45th International Conference on Software Engineering, ICSE ’23, page
     919–931. IEEE Press, 2023. ISBN 9781665457019. doi: 10.1109/ICSE48619.2023.00085.
     URL https://doi.org/10.1109/ICSE48619.2023.00085.
[34] Ruishi Li, Bo Wang, Tianyu Li, Prateek Saxena, and Ashish Kundu. Translating c to rust:
     Lessons from a user study. arXiv preprint arXiv:2411.14174, 2024. Benchmark available at
     https://github.com/Zero0one1/c2rs-userstudy-benchmark.
[35] Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang, Yan Wang, Rui Wang, Yujiu Yang, Shuming
     Shi, and Zhaopeng Tu. Encouraging divergent thinking in large language models through multi-
     agent debate. arXiv preprint arXiv:2305.19118, 2023.
[36] Michael Ling, Yijun Yu, Haitao Wu, Yuan Wang, James R Cordy, and Ahmed E Hassan. In
     rust we trust: a transpiler from unsafe c to safer rust. In Proceedings of the ACM/IEEE 44th
     International Conference on Software Engineering: Companion Proceedings, pages 354–355,
     2022.
[37] Zijun Liu, Yanzhe Zhang, Peng Li, Yang Liu, and Diyi Yang. A dynamic llm-powered agent
     network for task-oriented agent collaboration. In First Conference on Language Modeling,
     2024.
[38] Feng Luo, Kexing Ji, Cuiyun Gao, Shuzheng Gao, Jia Feng, Kui Liu, Xin Xia, and Michael R
     Lyu. Integrating rules and semantics for llm-based c-to-rust translation. In 2025 IEEE Interna-
     tional Conference on Software Maintenance and Evolution (ICSME), pages 685–696. IEEE,
     2025.
[39] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri
     Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement
     with self-feedback. Advances in Neural Information Processing Systems, 36:46534–46594,
     2023.
[40] Diego Magdaleno. Bsd coreutils is a port of many utilities from bsd to linux and macos. URL
     https://github.com/DiegoMagdaleno/BSDCoreUtils. Accessed: April, 2024.
[41] Nat McAleese, Rai Michael Pokorny, Juan Felipe Ceron Uribe, Evgenia Nitishinskaya, Maja
     Trebacz, and Jan Leike. Llm critics help catch llm bugs. arXiv preprint arXiv:2407.00215,
     2024.
[42] Ruijie Meng, Martin Mirchev, Marcel Böhme, and Abhik Roychoudhury. Large language
     model guided protocol fuzzing. In 31st Annual Network and Distributed System Secu-
     rity Symposium, NDSS 2024, San Diego, California, USA, February 26 - March 1, 2024.
     The Internet Society, 2024. URL https://www.ndss-symposium.org/ndss-paper/
     large-language-model-guided-protocol-fuzzing/.
[43] Microsoft. A proactive approach to more secure code. https://msrc.microsoft.
     com/blog/2019/07/a-proactive-approach-to-more-secure-code/, 2019. Accessed:
     2025-09-18.
[44] Microsoft. We need a safer systems programming language. https://msrc.microsoft.com/
     blog/2019/07/we-need-a-safer-systems-programming-language/, 2019. Accessed:
     2025-09-18.
[45] Santosh Nagarakatte, Jianzhou Zhao, Milo M.K. Martin, and Steve Zdancewic. Softbound:
     highly compatible and complete spatial memory safety for c. SIGPLAN Not., 44(6):245–258,
     June 2009. ISSN 0362-1340. doi: 10.1145/1543135.1542504. URL https://doi.org/10.
     1145/1543135.1542504.
[46] Santosh Nagarakatte, Jianzhou Zhao, Milo M.K. Martin, and Steve Zdancewic. Cets: compiler
     enforced temporal safety for c. SIGPLAN Not., 45(8):31–40, June 2010. ISSN 0362-1340. doi:
     10.1145/1837855.1806657. URL https://doi.org/10.1145/1837855.1806657.
[47] Vikram Nitin, Rahul Krishna, and Baishakhi Ray. Spectra: Enhancing the code translation ability
     of language models by generating multi-modal specifications. arXiv preprint arXiv:2405.18574,
     2024.
[48] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. C2saferrust: Transform-
     ing c projects into safer rust with neurosymbolic techniques. arXiv preprint arXiv:2501.14257,
     2025.


                                                12
[49] OpenAI. Gpt-5 mini — openai documentation. OpenAI Platform, 2025. URL https://
     platform.openai.com/docs/models/gpt-5-mini. Accessed: 2025-09-24.
[50] Benjamin Orthen, Oliver Braunsdorf, Philipp Zieris, and Julian Horsch. Softbound+cets
     revisited: More than a decade later. In Proceedings of the 17th European Workshop on
     Systems Security, EuroSec ’24, page 22–28, New York, NY, USA, 2024. Association for
     Computing Machinery. ISBN 9798400705427. doi: 10.1145/3642974.3652285. URL https:
     //doi.org/10.1145/3642974.3652285.
[51] Guangsheng Ou, Mingwei Liu, Yuxuan Chen, Xueying Du, Shengbo Wang, Zekai Zhang, Xin
     Peng, and Zibin Zheng. Enhancing llm-based code translation in repository context via triple
     knowledge-augmented. arXiv preprint arXiv:2503.18305, 2025.
[52] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize
     Chen, Yusheng Su, Xin Cong, et al. Chatdev: Communicative agents for software development.
     In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics
     (Volume 1: Long Papers), pages 15174–15186, 2024.
[53] Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitriy Vyukov.
     {AddressSanitizer}: A fast address sanity checker. In 2012 USENIX annual technical conference
     (USENIX ATC 12), pages 309–318, 2012.
[54] Jamey Sharp. Corrode: Automatic semantics-preserving translation from C to Rust. https:
     //github.com/jameysharp/corrode. Accessed: September 20, 2025.
[55] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A. Seshia, and Koushik Sen. Syzygy:
     Dual code-test c to (safe) rust translation using llms and dynamic analysis, 2024. URL https:
     //arxiv.org/abs/2412.14234.
[56] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
     Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information
     Processing Systems, 36:8634–8652, 2023.
[57] Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa. Smartc2rust: Iterative, feedback-
     driven c-to-rust translation via large language models for safety and equivalence. arXiv preprint
     arXiv:2409.10506, 2024.
[58] SWE-agent. mini-swe-agent: The 100-line ai agent for github issues and command line.
     https://github.com/SWE-agent/mini-swe-agent, 2025. Accessed: 2025-09-24.
[59] Chaofan Wang, Tingrui Yu, Beijun Shen, Jie Wang, Dong Chen, Wenrui Zhang, Yuling Shi,
     Chen Xie, and Xiaodong Gu. Evoc2rust: A skeleton-guided framework for project-level
     c-to-rust translation. arXiv preprint arXiv:2508.04295, 2025.
[60] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun
     Zhang, Shaokun Zhang, Jiale Liu, et al. Autogen: Enabling next-gen llm applications via
     multi-agent conversations. In First Conference on Language Modeling, 2024.
[61] Chunqiu Steven Xia, Matteo Paltenghi, Jia Le Tian, Michael Pradel, and Lingming Zhang.
     Fuzz4all: Universal fuzzing with large language models. In Proceedings of the IEEE/ACM 46th
     International Conference on Software Engineering, ICSE ’24, page 1–13. ACM, April 2024.
     doi: 10.1145/3597503.3639121. URL http://dx.doi.org/10.1145/3597503.3639121.
[62] Qingxiao Xu and Jeff Huang. Optimizing type migration for llm-based c-to-rust translation: A
     data flow graph approach. In Proceedings of the 14th ACM SIGPLAN International Workshop
     on the State Of the Art in Program Analysis, SOAP ’25, page 8–14, New York, NY, USA, 2025.
     Association for Computing Machinery. ISBN 9798400719226. doi: 10.1145/3735544.3735582.
     URL https://doi.org/10.1145/3735544.3735582.
[63] Aidan Z. H. Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel Kroening.
     VERT: Verified Equivalent Rust Transpilation with Large Language Models as Few-Shot
     Learners, May 2024. URL http://arxiv.org/abs/2404.18852.
[64] Z.ai. Glm-4.7: Advancing the coding capability. Website, 2025. URL https://z.ai/blog/
     glm-4.7. Accessed: 2026-05-06.
[65] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. Ownership guided c to rust
     translation. In Computer Aided Verification: 35th International Conference, CAV 2023, Paris,
     France, July 17–22, 2023, Proceedings, Part III, page 459–482, Berlin, Heidelberg, 2023.


                                                 13
     Springer-Verlag. ISBN 978-3-031-37708-2. doi: 10.1007/978-3-031-37709-9_22. URL
     https://doi-org.libproxy1.nus.edu.sg/10.1007/978-3-031-37709-9_22.
[66] Hongxiang Zhang, Yuyang Rong, Yifeng He, and Hao Chen. Llamafuzz: Large language model
     enhanced greybox fuzzing, 2025. URL https://arxiv.org/abs/2406.07714.
[67] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill Levchenko, and Varun
     Chandrasekaran. Llm-driven multi-step translation from c to rust using static analysis. arXiv
     preprint arXiv:2503.12511, 2025.


A    Adversarial Translation Loop: Detailed Algorithm
ACToR takes as input the C code c, the universe U , the seed test set T0 , together with hyperparameters
such as the number of iterations the translator and discriminator interact (MaxIter) before ACToR
outputs the final translated program. ACToR then conducts iterative translation on the source C code
and outputs both the Rust translation rs∗ and the final test set T ∗ . The T RANSLATOR subroutine
in Algorithm 1 is intentionally abstract: in our default instantiation it is an LLM coding agent. To
complement an existing C-to-Rust translator, the loop can also be seeded with that translator’s output
(e.g., C2SaferRust), with ACToR then post-processing the output across iterations.
During iterative improvement, ACToR maintains an append-only test set T . In the beginning, the
translator agent generates the initial safe translation and ensures it passes all the seed tests (lines
1-3) before the adversarial iterative loop (involving the discriminator) begins. Next, in each iteration
that follows, the discriminator agent reads the C code c and the current Rust code rs, and generates
test cases on which C and Rust outputs disagree (lines 7-11). To efficiently surface such inputs, the
discriminator constructs and refines a differential fuzzer besides static inspection and manual testing.
The discriminator is structured so that (1) all the test cases abide by the correct format and execute
successfully on the source C program (SANITYOK at line 9); and that (2) some test cases witness a
mismatch between outputs of the C and the Rust code that the translator has created so far (line 10).
We ensure this by providing a prompt to the discriminator to continue retrying until the generated test
cases meet the above two requirements. Once successful, the newly generated test cases (Batch)
are added to the full test set. The translator agent then takes the updated test cases as guidance to
improve the translation. It is set up with prompts that repeatedly ask it to pass all the test cases in the
current test set and only use fully safe Rust (lines 13-16). If the translator runs out of retries but still
cannot fully pass the test set T , the loop continues with the latest rs retained, even when some tests
in T remain failing. After a fixed maximum number of iterations, ACToR stops the loop and outputs
the final translation and the test set generated.

B    ACToR Implementation
The ACToR translation pipeline consists of three components: a task manager, a translator agent,
and a discriminator agent. The task manager prepares a sandboxed working directory containing all
necessary input files for the target project, coordinates agent execution, and snapshots the workspace
after each iteration. Both agents operate exclusively within this sandbox. To enforce isolation, each
agent is restricted to modifying only the files under its control: the translator agent may modify only
the translated Rust source file, while the discriminator agent may modify only the test case files. All
other files, including the original C source code, documentation, and build scripts, are read-only for
both agents. This constraint is enforced indirectly: after each iteration, all files outside the allowed
edit list are reverted to their state from the previous iteration. The agents do not communicate via
explicit message passing; instead, they collaborate implicitly through the shared filesystem state in
the sandbox. This design simplifies coordination and allows agents to be easily replaced without
affecting other components. The task manager alternates execution of the two agents in an adversarial
loop. At iteration 0, the translator agent produces an initial Rust translation. Subsequently, the
discriminator and translator alternate as [discrimination → translation]iter1 → [discrimination →
translation]iter2 → . . . This process continues for a fixed, configurable number of iterations.
During the translation phase, the translator agent may execute all existing test cases, analyze any
observed mismatches by inspecting both the C source and the Rust translation, then repair the
translated code. The agent must ensure that the updated Rust program passes all tests before


                                                    14
Algorithm 1 ACToR: Adversarial C to Rust Translation
Input: C program c, seed test set T0 , test input universe U (implicit)
 Params: MaxIter (of outer loop), TestBatchSize, RetryLimit (of inner loops)
Output: Final translation rs∗ and final test set T ∗
  1: while N OT PASSES S UITE(c, rs, T0 ) do                         ▷ initial translation on seed tests
  2:     rs ← T RANSLATOR(c, ∅, T0 )
  3: end while
  4: assert I S S AFE (rs); T ← T0
  5: for k = 1 to MaxIter do
  6:     retry ← 0
  7:     repeat
  8:         Batch ← D ISCRIMINATOR(c, rs, n=TestBatchSize);
  9:         IsV alid ← ∀t ∈ Batch : VALID T EST F ORMAT(t) ∧ S ANITYO K(t, c)
10:          IsDisc ← ∃t ∈ Batch : ¬IsEq∗ (c, rs, t); retry ← retry + 1
11:      until (|Batch| = TestBatchSize ∧ IsV alid ∧ IsDisc) ∨ retry ≥ RetryLimit
12:      T ← T ∪ Batch; retry ← 0
13:      while N OT PASSES S UITE(c, rs, T ) ∧ retry ≤ RetryLimit do
14:          rs ← T RANSLATOR(c, rs, T ); retry ← retry + 1
15:      end while
16:      assert I S S AFE(rs)
17: end for
18: return rs as rs∗ , T as T ∗

completing the task. Upon submission, an independent validator function will be invoked to verify
that (i) the Rust code compiles successfully, (ii) the translation contains no unsafe constructs, and
(iii) all tests pass. If any of these conditions are violated, the translator agent is restarted to repeat the
task. The prompts used for the translator agent are provided in Appendix E.
During the discrimination phase, the discriminator agent analyzes the C program and its Rust
translation to identify potential behavioral discrepancies. It then refines the fuzzer to explore a large
input space. After confirming mismatches, the agent selects the top-k distinguishing inputs and
formats them as new test cases. A validator checks that exactly k new tests are added and that the
Rust translation exhibits mismatches with the C program on these inputs. To filter out discrepancies
caused by non-determinism unrelated to translation correctness, the checker also compiles the C
source under two different compilation configurations (e.g., distinct optimization levels) and verifies
that both binaries produce identical outputs on each test input. The discriminator agent retries until
all checks pass or a retry limit is reached. The prompts used for the discriminator agent are also
provided in Appendix E.
Each agent runs in a sandboxed workspace where the modification is restricted to the files it controls
(translator: Rust source; discriminator: tests), with C code and the build scripts read-only to both.
This is enforced indirectly: after each iteration, any file outside the agent’s allowed edit set is reverted
to its prior content.
ACToR system is designed to be lightweight: the worker manager is implemented in around 1.8k lines
of Python code, while each agent is implemented with less than 500 lines including the prompts.

C    Agent and Model Details
We use Claude Code version 2.0.42 in all experiments. The model versions are claude-sonnet-
4-5-20250929, claude-sonnet-4-20250514, gpt-5-mini-2025-08-07, gemini-3.1-pro-preview, and
glm-4.7.

D    Benchmark Filtering
The full set of BSDCoreUtils contains 69 programs, but we filter out 12 of them from our main results
due to three reasons: (1) some utilities are trivial (e.g., true , yes ) (2) certain utilities require special
environments (e.g., stty ) or privileges (e.g., sudo ) not available in our experimental sandbox; and (3)
certain utilities perform destructive operations (e.g., rmdir ) that may break the testing harness.


                                                     15
    (ACToR/ Coverage Baseline) Translator Agent Prompt


    Task Description :
    ‘‘‘
    You are an expert in C and Rust .
    Your task is to translate the C ‘< project_name > ‘ project to safe Rust implementations .

    <... Project Setup >

    ## Workflow
    1. Read the C code and the test script to understand the functionalities .
    2. Initialize a new Cargo project in the ‘ ts / ‘ folder .
    3. Translate the C code to Rust code and compile it into binary .
    4. Run ‘./ testcmp . sh ‘ to compare the output of the translated Rust code with the original C
         program . You should run ‘./ testcmp . sh -- help ‘ to understand how to use the test script .
    5. Clean the working directory by removing temporary files and backup files .

    # # constraints
    - The translated Rust code MUST compile and MUST be 100% safe .
    - The translated Rust code MUST pass all the unit tests .
    ‘‘‘




                              Figure 5: The task prompt for the translator agent.




    (Coverage Baseline) Test Generator Agent Prompt — Adding Tests


    Task Description :
    ‘‘‘
    You are an expert in C and Rust .
    Your task is to add additional test cases to for the C program to improve the coverage .

    <... Project Setup >

    ##   Workflow
    1.   Read the C code to understand the functionalities .
    2.   Focus first on ** core functionalities ** , then explore ** edge cases **.
    3.   Run ‘ make clean && make all && ./ testcmp . sh coverage ‘ to compile the C code and get the
           current coverage .
    4.   Read the coverage report and the record of added test cases in ‘ t est _ca ses _re co rd . md ‘ to find
           potential missed cases .
    5.   Design **3** new test cases that are different from existing test cases .
    6.   Run ‘./ testcmp . sh coverage ‘ to get the new coverage . Ensure that the new coverage is higher
           than the previous one .
    7.   Clean the working directory by removing temporary files and scripts , temporary test cases , and
            backup files .

    <... Test formatting requirements >

    # # Constraints
    1. There should be exactly 3 new test cases added to the JSONL file . You should run ‘./ testcmp . sh
          ‘ and the number of test cases will be shown . There should be ‘< current_test_cases_number > +
            3 ‘ test cases in total .
    2. The 3 test cases should be different from each other . You should check this by reading the
          content of the test cases .
    3. The added tests must be valid for the C code . You should run ‘ make clean && make all ‘ and then
            run ‘./ testcmp . sh compare ./ xxx . out ( compiled from C code ) ‘. It must show ‘ All tests passed
          ! ‘.
    ‘‘‘




             Figure 6: The task prompt for the test generator agent of the coversge baseline.
E        Prompt Template


For Mini-SWE-Agent, we keep the system prompt that describes the agent workflow unchanged
as the original one during all the experiments. For Claude Code, we begin directly with the task
described in the user message, without any additional text preceding it. The task prompt structure for
the translator agent is shown in Figure 5. This prompt is shared among all translation methods during
evaluation. The prompt structure for the test-generation agent used in the coverage baseline is shown
in Figure 6. The prompt structure for the discriminator agent for ACToR is shown in Figure 7. The
fuzzing mode is controlled by the ‘allow_fuzz‘ section in the prompt.


                                                            16
    (ACToR) Discriminator Agent Prompt — Adding Tests


    Task Description :
    ‘‘‘
    You are an expert in C and Rust .
    Your task is to add additional test cases to discover semantic mismatches between the C code and
         the translated Rust code .

    <... Project Setup >

    ## Workflow
    1. Analyze the C code and the translated Rust code to detect ** semantic mismatches **.
    2. Focus first on ** core functionalities ** , then explore ** edge cases **.
    3. Read the current test script and the record of added test cases in ‘ t est _ca se s_r eco rd . md ‘ to
         find potential missed cases .
    4. Collect the best **3** new input cases that expose mismatches between C code and Rust
         translation . Add the 3 new test cases to the test cases file .
    5. Run the new tests to compare the output of the translated Rust code with the original C
         program to confirm the mismatches .
    6. Clean the working directory by removing temporary files and scripts , temporary test cases , and
          backup files .

    <... Test formatting requirements >
    IF { $allow_fuzz }
    <... Details on the usage of the fuzzer script >
    ENDIF

    # # Constraints
    1. There should be exactly 3 new test cases added to the JSONL file . You should run ‘./ testcmp . sh
          ‘ and the number of test cases will be shown . There should be ‘< current_test_cases_number > +
            3 ‘ test cases in total .
    2. The 3 test cases should be different from each other . You should check this by reading the
          content of the test cases .
    3. The added tests must be valid for the C code . You should run ‘ make clean && make all ‘ and then
            run ‘./ testcmp . sh compare ./ xxx . out ( compiled from C code ) ‘. It must show ‘ All tests passed
          ! ‘.
    4. The added tests should reflect the differences between the C code and the Rust code . You
          should run ‘./ testcmp . sh compare ./ ts / target / release / xxx ( compiled from Rust code ) ‘. The Rust
            code should fail on all 3 new test cases .
    ‘‘‘




                     Figure 7: The task prompt for the discriminator agent of ACToR.



    Post-processing Prompt — Eliminating Unsafe Blocks


    Task Description :
    ‘‘‘
    You are an expert in C and Rust .
    Your task is to translate the C ‘< project_name > ‘ project to safe Rust implementations .

    <... Project Setup >

    ##  Workflow
    1.  Read the C code and the test script to understand the functionalities .
    2.  Initialize a new Cargo project in the ‘ ts / ‘ folder .
    3.  Translate the C code to Rust code and compile it into binary .
    4.  Run ‘./ testcmp . sh ‘ to compare the output of the translated Rust code with the original C
          program . You should run ‘./ testcmp . sh -- help ‘ to understand how to use the test script .
    5. Clean the working directory by removing temporary files and backup files .
    ‘‘‘

    The translation contains unsafe keywords .
    Please fix it to ensure no unsafe code is used .
    Also , keep it passing all the tests .




                           Figure 8: The task prompt for eliminating unsafe blocks.
F        Per-program Results for Correctness & Adaptability.


The per-program results of the Correctness & Adaptability experiments are shown in Figure 9. When
applying SWE + GLM-4.7 to the translation loop, we were unable to complete 10 iterations for the
program ‘join‘ within 48 hours due to limited model-serving capacity. We therefore report results
from the maximum completed iteration on this program. Completing the full 10 iterations may yield
larger correctness improvements.


                                                          17
Figure 9: Validation pass rate achieved by ACToR on micro benchmark across different settings
compared with naive baseline and strong baseline, on 7 different agent-model settings.
G    Ablation Study on Design


We conduct an ablation to know how the adversarial design in ACToR drives correctness gains on
the micro-benchmark. We analyze the improvement offered by two design choices: (a) having an
adversarial discriminator in the workflow to guide the translator, and (b) forcing the discriminator
agent to use the fuzzing script we provided. We compare three variants of ACToR: coverage-baseline,
ACToR-NoFuzz, and the full ACToR (with fuzzing). The results summed across programs at the
final iteration are reported on the left of Figure 3. Entry (row, column) shows the relative pass rate
of the row method on the column method’s tests. All three methods largely pass their own tests as
expected. On coverage-baseline’s tests, ACToR-NoFuzz and the full ACToR reach 90% and 94%
passing rates, respectively; in the reverse direction, coverage-baseline achieves less than 40% passing
rate on tests from either ACToR variant. This indicates that adversarial discriminators produce tests
that more effectively expose semantic mismatches and result in more correct translations. Between
ACToR variants, the full ACToR attains 73% vs. 71% when cross-tested against ACToR-NoFuzz.
This suggests that the discriminating agent uses the customized fuzzer to surface more challenging
bugs in the translated code. We also measure the final test coverage of each method on the C code.
The result is shown at the bottom left of Figure 3. The coverage baseline works as expected and
achieves the highest line coverage on the C code than two other ACToR variants. However, it is
worse in correctness. This further supports the conclusion that adversarial translation is more efficient
in improving correctness compared with purely sampling new test cases based on coverage. Finally,
we compare the financial costs of completing all six programs: the coverage baseline costs $95 USD,
while ACToR-NoFuzz and the full ACToR cost $240 USD and $211 USD, respectively. To better
understand cost-effectiveness, we run an equal-cost experiment in which we extend the coverage
baseline to 25 iterations, costing $220 USD, roughly matching the cost of running ACToR for 10
iterations ($211 USD). We cross-compare their resulting translations using relative pass rate. The
two methods complete different numbers of iterations, resulting in different numbers of test cases.
However, even under equal budget, the coverage baseline does not achieve comparable correctness.
Its relative pass rate (75/177 = 42.4%) remains far below that of ACToR (425/447 = 95.1%). In terms
of failure counts, ACToR fails only 22 out of 447 tests from the coverage baseline, while the coverage
baseline fails 102 out of 177 from ACToR. This demonstrates that the adversarial setting delivers
substantially higher correctness per dollar spent.


                                                   18
H    Ablation Study on Configurations
We conduct a second ablation study on the micro-benchmark to identify an effective experimental
configuration. We examine three factors: seed test cases, number of iterations, and number of test
cases generated by the discriminator agent per iteration. Recall that the default configuration of
ACToR uses 15 initial seed tests, runs for 10 iterations, and adds 3 new tests per iteration. To assess
the effect of the number of tests added per iteration, we run two variants of ACToR that follow the
default setting except that they add 1 and 5 test(s) per iteration, respectively, instead of 3. To analyze
the relation between correctness and the number of iterations, we run ACToR for 20 iterations with
other parameters set as default. We collect the initial translation (0th iteration) and the translated
code at the end of 5th , 10th , 15th , and 20th iterations. We compute their pass rates on the validation
test set. The results summed across programs are shown on the right of Figure 3. Compared with
adding 1 test per iteration, adding 3 new tests costs 16% more USD to translate all programs, and
improves the final pass rate from 94.7% to 98.2%. Adding 5 new tests per iteration further increases
the money cost by 29% compared with adding 3 tests per iteration, but only improves the pass rate by
1.4%. When comparing across different iteration numbers, the validation pass rate is improved by 9%
after the first 10 iterations. Further extending to 20 iterations yields only a 1.4% improvement, at the
expense of 2.1× the total financial cost. At last, we analyze the influence of initial test cases. We run
ACToR starting with only a single seed test, while keeping all other parameters as default values. A
single seed test is sufficient to demonstrate the expected test case format and prevent trivial failures
due to formatting mismatches, but it provides less initial coverage than the default setting of 15 seed
tests. Using the default configuration (15 initial tests) increases cost by 6% relative to the single-seed
setup, and improves the final pass rate from 94.9% to 98.2%. To balance performance and cost, we
adopt the configuration of 15 seed tests, 10 iterations, and 3 new tests per iteration when translating
the macro-benchmark.

I   Macro Experiments with Claude Code and Claude-Sonnet-4
We also run ACToR with Claude-Sonnet-4 to translate the macro-benchmark. In this trial, we use an
older implementation of ACToR that discourages the use of unsafe, but does not enforce full safe Rust
in the middle of the translation loop. Instead, full safe Rust is enforced at the end of the translation
as a post-processing step, performed via a single agent call that eliminates all unsafe blocks while
preserving the functionality of the translated Rust code. The prompt for this post-processing step is
shown in Figure 8. We emphasize that the latest implementation of ACToR used in the main paper
(with Claude-Sonnet-4.5) does not include this post-processing step: full safety is instead enforced at
every iteration of the translation loop, as described in Sec. 3.2. All other experimental settings in this
trial are identical to those described in the main text. The results are presented in Figure 10. With
Claude-Sonnet-4, ACToR outperforms the coverage baseline on 55/57 programs in terms of relative
pass rate. ACToR achieves full pass on 26 programs using the tests from the coverage baseline.
Across all 57 programs, ACToR attains an average relative pass rate of 93.9%, which is 18.9% higher
than the 75.0% pass rate of the coverage baseline. ACToR achieves a 95.3% pass rate on the union
of the test cases from both ACToR and the coverage baseline. This result aligns with the findings
on Claude-Sonnet-4.5, demonstrating that ACToR’s performance is stable and generalizes across
different model configurations.

J   Mismatch Detection through Agent-driven Differential Fuzzing
The discrimination procedure aims to detect semantic mismatches between the C code and its
Rust translation, thereby guiding the translator agent to improve translation quality. To effectively
uncover functional discrepancies across the two implementations, we incorporate two key design
choices. First, as mentioned in Section 3.2, we employ an LLM agent as the mismatch detector
across C code and Rust code. Second, rather than relying solely on static source-code inspection
or manual testing, we prompt the discriminator to construct and refine a fuzzer with customized
input generators that differentially exercise both implementations across a diverse input space.
Recent work on LLM-assisted software testing and fuzzing has shown that LLMs can leverage
their understanding of program semantics and specifications to generate focused and structured
input cases [61, 66, 42, 33, 7]. Consistent with these findings, our manual inspection (presented
in Appendix K) shows that the LLM agent frequently updates the fuzzer to improve mismatch


                                                   19
Figure 10: The relative pass rate when cross-comparing ACToR and coverage baseline (Cov-Base) on
Claude Code with Claude-Sonnet-4 at iteration 10. For each program, the left bar shows evaluating
the translation from ACToR on tests generated in coverage-baseline; the right bar is evaluating the
translation from coverage-baseline on ACToR’s tests. The length of each program in LoC is presented
next to the program name.




Figure 11: One example fuzzer updating during a discrimination procedure. The discriminator agent
keeps updating the fuzzer to find mismatches.
detection during the discrimination procedure. Figure 11 presents one representative update that
happened in the fold program. The discriminator begins by running the existing fuzzer inherited
from the previous iteration. After determining that this fuzzer fails to uncover new mismatches, the
discriminator controls the fuzzer to probe previously unexplored regions. The updated fuzzer initially
still reports no discrepancies. Through another refinement of the fuzzer, the discriminator eventually
identifies four distinct behaviour mismatches. These observations suggest that the discriminator needs
to continuously and adaptively manipulate the fuzzer to detect mismatches during the adversarial
translation process. Furthermore, as demonstrated in the ablation study in Section 4.2, incorporating
fuzzer construction in the discrimination procedure improves overall performance by 2% while
reducing total LLM query costs by approximately 12%, compared to prompting the discriminator to
identify mismatches through manual testing alone. This shows that the tailored fuzzer improves the
LLM agent’s cost efficiency at detecting mismatches.

K    Case Study on the Agentic Discriminator
To better understand the role played by the LLM agent in the discrimination procedure, we conduct
a case study by analyzing detailed interactions between the agent and the constructed fuzzer using
agent execution logs. We first examine how frequently the LLM agent interacts with the fuzzer,


                                                 20
measured by the number of edits on the fuzzer. Specifically, we identify such interactions using the
edit/write tool calls recorded in the logs. On the 6 programs in the micro benchmark, the agent
edits the fuzzer script 126 times over 10 iterations, averaging approximately 21 edits per program.
On the macro benchmark consisting of 57 programs, the fuzzer is updated 312 times in total across
10 iterations, with an average of 5.5 edits per program. We then conduct a manual inspection of the
interaction patterns between the discriminator agent and the fuzzer. We sample 10 programs (3 from
the micro benchmark, 7 from the macro benchmark) and analyze the discriminator agent logs for all
10 iterations. There are 127 fuzzer edits in total during the adversarial translation process for these 10
programs. Based on the underlying motivations, we categorize the fuzzer updates into three groups:
(1) Redirection. After inspecting the code or examining existing test cases, the agent determines that
the current fuzzer is no longer effective at uncovering new mismatches. It then updates the fuzzer to
target different regions of the input space that may expose additional discrepancies. There are 94
cases in this category. (2) Targeted Refinement. After confirming a semantic mismatch during broad
exploration, the discriminator further refines the fuzzer to target the identified pattern and its logically
related inputs. 22 case belongs to this category. (3) Unrelated Update. The remaining 11 edits are
cases where the discriminator agent fixes bugs in the fuzzer, separates one update into multiple edits,
etc., that are not related to mismatch detection. Based on these inspections, the fuzzer needs to be
constantly updated to discover new discrepancies during the adversarial translation process. A fixed
fuzzer with a fixed set of seed tests may not be sufficient to find new mismatches.




                                                    21
