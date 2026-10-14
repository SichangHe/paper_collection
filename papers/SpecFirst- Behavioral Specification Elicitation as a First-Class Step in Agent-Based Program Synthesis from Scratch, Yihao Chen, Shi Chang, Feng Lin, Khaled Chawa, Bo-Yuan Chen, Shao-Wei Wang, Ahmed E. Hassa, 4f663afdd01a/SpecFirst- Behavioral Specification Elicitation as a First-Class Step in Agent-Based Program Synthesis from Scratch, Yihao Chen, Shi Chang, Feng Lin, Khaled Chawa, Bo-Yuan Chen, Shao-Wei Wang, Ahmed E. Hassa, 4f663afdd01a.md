                                          SpecFirst: Behavioral Specification Elicitation as a
                                          First-Class Step in Agent-Based Program Synthesis
                                                              from Scratch
                                            Yihao Chen2 , Shi Chang1 , Khaled Chawa4 , Feng Lin1 , Boyuan Chen1 , Shaowei Wang3 , Ahmed E. Hassan2
                                                                                                     1 Huawei Canada

                                                                                   {shi.chang, feng.lin, boyuan.chen}@huawei.com
                                                                                                   2 Queen’s University

                                                                                    yihao.chen@queensu.ca, ahmed@cs.queensu.ca
                                                                                                3 University of Manitoba

                                                                                             shaowei.wang@umanitoba.ca
                                                                                                 4 Concordia University

                                                                                           khaled.chawa@mail.concordia.ca



                                            Abstract—LLM-based agents excel at software engineering             architecture and programming language) and reconstruct the
arXiv:2607.27167v1 [cs.SE] 29 Jul 2026




                                         tasks where an existing codebase provides context, but con-            full behavioral envelope of a target program from limited
                                         structing a program from scratch remains fundamentally harder.         information alone. P ROGRAM B ENCH [5] makes this concrete:
                                         Recent benchmarks such as ProgramBench quantify this gap:
                                         given only natural-language documentation and an execute-only          given only natural-language documentation and an execute-
                                         binary as a behavioral oracle, even frontier models solve fewer        only binary as a behavioral oracle, an agent must produce
                                         than 1% of instances. Existing frameworks conflate documenta-          a faithful re-implementation from scratch. Even the strongest
                                         tion reading, behavioral exploration, and code synthesis into a        frontier models (e.g., GPT-5.5) can only fully resolve fewer
                                         single pass, causing agents to probe insufficiently, lose behavioral   than 1% of instances, confirming that from-scratch program
                                         intent as context drifts, and propagate early misinterpretations
                                         into the final implementation. Inspired by classical requirements      construction remains an open challenge.
                                         engineering, we argue that behavioral specification elicitation           Existing agent frameworks such as SWE-agent [2] and
                                         should be a first-class phase that precedes implementation. We         OpenHands [6] approach this task by providing the agent with
                                         present S PEC F IRST, a two-stage framework that forces the            natural-language documentation as the primary specification
                                         specification elicitation before code synthesis. A dedicated spec      and an execute-only binary as a behavioral oracle [5]. While
                                         agent first probes the binary and combines observations with doc-
                                         umentation into a structured specification. Next, a code synthesis     this setup permits behavioral discovery through probing, these
                                         agent then uses this specification to drive implementation. This       frameworks mix specification elicitation and code synthesis
                                         decomposition resolves documentation ambiguities before coding         into a single undifferentiated loop—the agent switches freely
                                         begins and provides a stable behavioral reference throughout           between planning, reading documentation, probing the binary,
                                         synthesis. We evaluate S PEC F IRST on all 200 ProgramBench            and writing code within the same turn budget, with no mecha-
                                         instances across four models spanning two families and an order
                                         of magnitude of capability. S PEC F IRST consistently outperforms      nism forcing comprehensive elicitation before implementation
                                         the single-loop baseline, improving test pass rates by 6.9%–           begins. This entanglement leads to three systematic limita-
                                         21.3% and binary exploration coverage by 9.4%–18.5%, all               tions.
                                         statistically significant. Behavioral analysis on code synthesis        1 Ineffective exploratory probing. Without a dedicated
                                         further shows that a prior specification enables earlier and more      phase for behavioral discovery, the agent rarely probes the
                                         sustained code construction. Our results demonstrate that an
                                         explicit requirements-engineering phase is an effective paradigm       binary thoroughly enough to construct a complete behavioral
                                         for from-scratch program construction.                                 model before committing to implementation. Edge cases, error
                                            Index Terms—Large language Models, Code Agent, long-                paths, and flag interactions that are absent from the documen-
                                         horizon tasks, ProgramBench, Specification Elicitation, Spec           tation but present in the binary are frequently missed, because
                                         Agent.                                                                 the agent shifts to coding before its exploration is complete.
                                                                                                                 2 Specification loss over long horizon. Without explicit
                                                                I. I NTRODUCTION                                upfront elicitation, behavioral intent must be maintained im-
                                           LLM-based agents have demonstrated strong performance                plicitly across turns and is susceptible to drift as context
                                         on software engineering tasks such as bug fixing [1], feature          grows [7], [8]. Compression mechanisms such as reasoning
                                         implementation [2], and code completion [3], [4]. Those tasks          token stripping (i.e., removing the reasoning content between
                                         share a common structure: an existing codebase anchors the             agent turns) and context summarization exacerbate this by
                                         agent’s work. Building a program entirely from scratch is              selectively discarding tokens that encode the original speci-
                                         fundamentally harder: the agent must decide everything (e.g.,          fication [9], [10], so later-turn outputs increasingly reflect a
degraded approximation of the target behavior.                         2) Empirical evaluation. We evaluate on all 200 Pro-
 3 Error Propagation without anchoring. Without an                        gramBench instances across four models, demonstrating
elicited specification as a stable reference, errors introduced           consistent improvements in test pass rate (6.9%–21.3%)
early in the run accumulate and propagate across subsequent               and binary exploration coverage (9.4%–18.5%), all sta-
turns without correction. When the agent misinterprets the                tistically significant.
documentation or makes an incorrect behavioral assumption,             3) Behavioral analysis. We show that having a prior spec-
it continues building on that assumption turn after turn—each             ification changes how the code synthesis agent spends
dependent decision compounding the original error with no                 its turn budget: it starts writing code earlier and sustains
artifact to anchor against.                                               implementation longer, rather than alternating between
   In traditional software engineering, these limitations are             probing and coding throughout the run.
addressed by treating specification elicitation as a first-class       The remainder of this paper is organized as follows. Sec-
phase that precedes implementation [11], [12]: requirements         tion II presents the background and limitations of existing
engineers exercise prototypes and construct scenarios to sur-       approaches. Section III introduces the details of S PEC F IRST.
face behavioral detail that written artifacts never capture,        Section IV presents experimental settings. Section V presents
before a single line of code is written [13], [14]. We argue        the evaluation and results. Section VI surveys the related work
the same decomposition should apply to agentic program              and discusses the differences between our work and previous
construction. Spec-driven frameworks such as OpenSpec [15]          studies. Section VII discusses failure cases, formats, costs, and
and spec-kit [16] adopt a similar philosophy, but rely solely       threats to validity. Section VIII concludes our study.
on prompting human stakeholders for specification input, and
do not support automated behavioral elicitation through binary                  II. BACKGROUND AND M OTIVATION
probing.
   We present S PEC F IRST, a two-stage pipeline that explicitly    A. Problem Formulation
separates behavioral specification elicitation from code synthe-       Let P denote a target program that is a deterministic
sis. In the first stage, a dedicated spec agent receives the doc-   command-line program. The agent L observes P through
umentation and execute-only binary and focuses exclusively          two artifacts: (i) documentation D (e.g., a readme file) that
on understanding the target program’s behavior through sys-         describes P in natural language, and (ii) an execute-only
tematic black-box probing, producing a structured behavioral        binary B that instantiates P’s observable behavior but whose
specification artifact (i.e., SPEC.md). In the second stage,        source code and internal structure are inaccessible. The agent
an existing code synthesis agent receives the documentation,        L task is to produce an implementation Î containing source
the binary, and SPEC.md, and focuses exclusively on im-             code and necessary files to build an executable file, that
plementation, now equipped with a behavioral model that             reconstructs the behavior of P. The implementation Î may
goes beyond what the documentation alone provides. This             be written in any programming language and architecture
decomposition directly addresses each limitation above: the         chosen by the agent. Next, it builds a candidate executable
spec agent explores freely without competing with coding,           B̂ from Î, and evaluates B̂ against a given hidden test suite
documentation ambiguities are resolved through probing be-          T = {ti }Ni=1 , where each test ti = ai , si , B(ai , si ) consists
fore implementation begins, and the behavioral gap between          of a command-line argument string ai ∈ Σ∗ , a standard-
documentation and binary is explicitly addressed rather than        input stream si ∈ Σ∗ , and the ground-truth output B(ai , si )
left to chance.                                                     produced by B on that input. The objective is to produce Î
   We evaluate S PEC F IRST on the full 200-instance P RO -         that maximizes test pass rate:
GRAM B ENCH suite [5] across four models spanning two
                                                                                               N
families and an order of magnitude of capability (Qwen3.5-                                  1 X h                             i
                                                                      TestRate(Î, T ) =          1 B̂(ai , si ) = B(ai , si ) ,   (1)
397B-A17B, Qwen3.6-35B-A3B, GPT-5.5-high, and GPT-5.4-                                      N i=1
mini). Across all settings, S PEC F IRST consistently outper-
forms the baseline (i.e., mini-SWE-agent), with test pass rate         which measures the fraction of test cases where B̂ repro-
improvement of 6.9%–21.3% and binary exploration coverage           duces the observable behavior of P exactly. A submission
gains of 9.4%–18.5%, all statistically significant. Behavioral      achieves PassRate = 1.0 if and only if B̂ is behaviorally
analysis further confirms that the decomposition restructures       equivalent to B on T . Figure 1 (blue box) presents the general
how the code synthesis agent allocates its budget: with a prior     pipeline of existing code synthesis agents [2], [5], [6]. The
specification, the agent commits to writing code earlier and        agent operates in an iterative probe-then-build loop: it invokes
produces larger, more complete implementations.                     B on selected inputs and reads D to build an understanding of
   This paper makes the following contributions:                    the program’s behavior, then progressively writes, tests, and
   1) S PEC F IRST framework. We propose the first agen-            refines source code until it judges the implementation suffi-
       tic pipeline that explicitly decouples behavioral spec-      ciently complete. The final output is a repository containing
       ification elicitation from code synthesis for from-          source code and a build file (e.g., compile.sh), which the
       scratch program construction, directly instantiating the     evaluation harness compiles into a candidate executable B̂ and
       requirements-engineering phase.                              scores against hidden tests.
                                                                     information was observed once and never re-referenced: the
           Listing 1: gomplate README file (D).                      final submission’s function map registers 17 namespaces and
gomplate is a template renderer that supports multiple               silently omits all six, causing 126 test cases to fail before a
datasources (JSON, YAML, HTTP endpoints, environment
variables, and more).                                                single line of code is written for them.
###Usage examples:
                                                                     Error propagation without anchoring. Without a persis-
                                                                     tent specification, a single early misinterpretation can silently
Basic usage with environment variables: echo ’Hello, {{ .Env         corrupt every subsequent implementation decision. In the
.USER }}’ | gomplate
                                                                     gomplate instance under Qwen3.6-35B-A3B, the agent
Inline template evaluation: gomplate -i ’the answer is: {{           correctly reads the typed signature Seq(start, end,
mul 6 7 }}’
                                                                     step int64) []int64 from documentation at turns 4–
Using a datasource file: gomplate -d config=./config.yaml -i         5. Yet when Seq is first implemented at turn 57, it emits
 ’the value we want is: {{ (ds "config").foo.bar.baz }}’
                                                                     a degraded form—func Seq(args ...interface)
See the official documentation for full details and examples         []interface— discarding both typed arguments and re-
: https://docs.gomplate.ca
                                                                     turn value. Over the next 140 turns the math namespace
License: see the LICENSE file in this repository.                    is refactored five times, each time re-emitting the wrong
                                                                     signature without ever consulting the original documentation.
B. Limitations of Existing Code Synthesis Agent                      The incorrect signature ships in the final submission, causing
   In practice, D provides only a surface-level description          25 of 43 Seq-related tests to fail with type errors.
of P—primary features, typical usage, and representative                These limitations motivate S PEC F IRST’s core design: a
examples—while remaining ambiguous or silent on edge                 dedicated spec agent that systematically explores the specifi-
cases, output formats, and error behavior [17], [18]. Figure 1       cation before implementation begins, externalizing its findings
shows the README for gomplate1 , a command-line tem-                 into a persistent specification file (Spec.md) that eliminates
plate renderer in P ROGRAM B ENCH. The README describes              the coverage gap from ineffective probing, prevents early
the tool’s purpose and lists common flags, but gomplate              misinterpretations from propagating uncorrected, and ensures
extends Go’s text/template engine with a large library of            that Behavioral knowledge discovered during exploration is
built-in functions spanning namespaces such as coll, math,           never lost across turns.
net, crypto, and strings. No README can enumerate
                                                                                    III. A PPROACH OF S PEC F IRST
the precise semantics, argument types, error conditions, and
output formats of every function; faithful re-implementation             Our approach directly addresses all three limitations through
therefore requires extensive behavioral exploration of the bi-       a dedicated specification elicitation phase prior to implementa-
nary. We use this instance to illustrate the limitations of the      tion. We implement an autonomous spec agent that probes B
existing single-loop framework.                                      systematically through black-box interaction, uncovering be-
Ineffective exploratory probing. Without a dedicated explo-          haviors that documentation D leaves implicit or omits entirely
ration phase, the baseline agent interleaves probing with cod-       — directly countering 1 by ensuring exploration is complete
ing, allocating only a fraction of its turns to behavioral discov-   before coding begins. The elicited specification is persisted
ery before committing to an implementation. For gomplate,            as an explicit artifact S (i.e., SPEC.md in our case), which
this is particularly damaging: the agent must understand not         serves as a stable behavioral contract that anchors all subse-
only the top-level CLI interface but also the semantics of           quent implementation decisions, resolving 2 by providing an
functions across ten namespaces, each with its own argument          anchor that prevents early errors from compounding. Critically,
conventions and edge-case behavior. In practice, we observe          because S is stored externally rather than maintained implicitly
that the general code synthesis agent (i.e., mini-SWE-agent          in the model’s context, it remains intact regardless of context
using Qwen3.6-35B-A3B) confines its probing to the functions         growth or compression, mitigating 3 . The overall framework
explicitly mentioned in the README—primarily the env                 of S PEC F IRST is presented in Figure 1. The code synthesis
and data namespaces—while leaving the behavior of coll,              agent can be any existing agent (e.g., OpenHands [6] or SWE-
math, net, and random largely unverified.                            agent [2]). If the agent encounters an ambiguity or gap in S
Specification loss over long horizon. Even when the collected        during implementation, it may still probe binary B to resolve
specification is read correctly, its content can be lost across a    it. We elaborate on the design and operation of the spec agent
long run if nothing anchors it. In gomplate, the general             in the following sections.
code synthesis agent (i.e., mini-SWE-agent using GPT-5.5-            A. Eliciting Behavior Specification through Probing of the
high) collected the full namespace index at turn 4, receiving        Executable File
function signatures for every namespace including aws, gcp,
sockaddr, semver, sprig, and cidr. Yet across the                       At each turn, the spec agent selects a probe, i.e., an
remaining 25 turns, none of these six namespace names                invocation of B with arguments, flags, or stdin chosen from
appears again in the agent’s reasoning or tool calls. The            what it has inferred so far, and observes the run time results
                                                                     from triple channels (stdout, stderr, exit). Free-form
  1 https://github.com/hairyhenderson/gomplate                       bash was chosen over a structured probe API because it mirrors
            Input                                                                             Write, test,
                                   Output, behavior                                         complete code               Repository
                                                          Code Synthesis Agent
                                      Probe               Task: Write code to re-      Implementation
       Documentation                                      implement the program
                                                                                                                    Source    Build file
                                    Invoke binary,
                                       read doc                                                 Output
     Executable binary
                                  Inv                                                                         General Code Synthesis
                                      ok
                                    rea e bina
                                       dd      r
                                          oc y,
                     Pro                                                                 Specification
          Ou                 be              Spec Agent
            tpu                                                                      [Sec1]: Overview
               t, b
                   eh                                                                ...
                      av                     Task: elicit the specification
                         ior
                                             of the program                          [Sec n]: Edge cases
                                                                                                               Specification Elicitation

Fig. 1: Framework of S PEC F IRST. On top of the default code synthesis pipeline in the blue box, S PEC F IRST introducesspec
agent to elicit the specification before implementation in the green box.
how a human engineer would interact with an unfamiliar tool,                  which would trivialize re-implementation; (b) binary intro-
and because it allows the agent to chain commands (e.g.,                      spection uses disassemblers, tracers, or decompilers to bypass
constructing input files, running the binary, and inspecting                  black-box interaction entirely. Neither shortcut represents the
its output in one step). For interactive or TUI programs, pre-                specification-elicitation behavior we aim to study, and both
installed tmux/libtmux provides a virtual terminal through                    would confound the results.
which the agent can send keystrokes and capture screen state.                    Therefore, to address this, when designing prompts, we
   The spec agent conducts an iterative probing loop in which                 explicitly prohibit LLM from doing both classes of actions.
each observation of binary B informs the next probe. Starting                 All interactions with B must go through its normal user
from the behavioral skeleton provided by D, the agent progres-                interface (CLI flags, stdin/stdout). An automated judge in-
sively deepens its exploration of P by targeting the classes of               spects the agent’s command history for prohibited patterns
behavior that documentation characteristically under-specifies.               (repository clones, registry installs, source tarball downloads,
Analyzing of the D reveals four recurring probing patterns that               and disassembler calls); any detected violation disqualifies
go beyond what D already provides:                                            the run and records a score of zero. Wrapping or shimming
   • Boundary probing: testing inputs at the limits of accepted               the provided binary is similarly prohibited and detected. This
     ranges (e.g., empty input, maximum-length strings, spe-                  enforcement ensures that all behavioral knowledge encoded in
     cial characters) to determine exact boundary semantics                   the generated spec file derives from black-box observation,
     that documentation leaves implicit.                                      making the specification-elicitation loop the sole source of
   • Error-path elicitation: systematically triggering error                  information beyond D.
     conditions (malformed input, missing required arguments,
     conflicting flags) to record the precise stderr message
                                                                              C. Specification Deliverable and Format
     and exit code each condition produces.
   • Combinatorial flag testing: exercising flags in combi-                       Even a thorough elicitation loop is only useful if its findings
     nation to surface interaction effects absent from per-flag               are communicated in a form the downstream exec agent can act
     documentation.                                                           on. The format of specification is a non-trivial design variable.
   • Output-format refinement: presenting adjacent inputs                     A free-form transcript of raw observations is hard to act on,
     and comparing their outputs to resolve ambiguities in                    while an over-prescribed template may suppress behavioral
     field ordering, delimiter choice, and whitespace handling                detail that does not fit its categories. We adopt the sections
     that prose descriptions inevitably leave underspecified.                 format: a light scaffold of six named headings: Overview;
                                                                              Flags; Input & stdin; Output format; Error patterns; Edge
B. Constraints and Shortcut Prevention                                        cases. They are chosen as the minimal structure that covers the
  We observe that LLM agents can shortcut the intended task                   behavioral dimensions a re-implementer needs. The headings
in ways that inflate apparent performance without genuine                     prescribe what to document, not how to discover or phrase
behavioral understanding. Two shortcuts are particularly dan-                 it, ensuring the isolation between specification elicitation and
gerous in this setting: (a) source recovery locates the original              code synthesis. More comparison of different formats (i.e.,
source code via package registries, GitHub, or web search,                    freeform and OpenSpec [15]) can be found in Section VII-B.
D. Termination                                                        •  RQ4: How does S PEC F IRST affect the behavior of the
  There is no semantic oracle for specification completeness:            code synthesis agent?
no external judge can assess whether SPEC.md captures all              In RQ1, we evaluate the effectiveness of S PEC F IRST in
of P’s observable behavior. An agent that terminates too            synthesizing programs from scratch and compare it with
early produces an incomplete spec; one that never terminates        selected baseline. In RQ2, we evaluate the effectiveness of
produces no spec at all. A run terminates under one of three        S PEC F IRST across instances with different difficulty levels.
conditions, applied in priority order.                              In RQ3, we evaluate the specification exploration ability of
  • Self-declared completion (primary): if the spec agent           S PEC F IRST and compare it with the baseline. In RQ4, we
     judges the specification complete, it finalizes the process.   investigate how the spec agent affects the behavior of the code
     Completeness is the agent’s own judgment, which is itself      synthesis agent by comparing pipeline configurations with and
     a research variable we measure.                                without spec elicitation.
  • Step limit: if 1,000 agent–environment turns is reached,
                                                                    B. Benchmark
     it terminated. The generous step limit (1,000 turns) is
     set to permit high-coverage exploration; in practice, most        We evaluate on the full P ROGRAM B ENCH suite [5], which
     runs self-terminate well before this cap, confirming that      comprises 200 command-line program instances drawn from
     the limit is a safety net rather than a binding constraint.    real-world open-source tools, covering widely used software
  • Wall-clock limit: We use 6 hours as a final safeguard.
                                                                    and complex applications, such as FFmpeg, SQLite, and
     The spec agent is terminated after running 6 hours.            the PHP interpreter. Those 200 task instances in Program-
                                                                    Bench are built from repositories written primarily in com-
  Finally, a deliverable gate enforces artifact presence. If the
                                                                    piled languages: Rust (107), Go (46 repositories), C/C++
specification file is absent at submission, the run is rejected
                                                                    (45 repositories), 1 (Java), and 1 (Haskell). Each instance
and the agent is asked to write it (capped at 8 rejections, after
                                                                    provides a natural-language documentation (a README and
which the run is recorded as a failure).
                                                                    man page) describing the program, and an execute-only binary
E. Principles of Agent Design                                       that serves as the behavioral oracle during spec elicitation and
   We introduce the principles of the agent design involved         implementation. Each instance is labelled by difficulty—easy
in S PEC F IRST in this section. General agent architecture.        (28), medium (143), and hard (29)—and annotated with the
All our agents follow the ReAct agent design by following           implementation language of the reference binary. To evaluate
previous work [19], [20]. Except for that, we force all agents      the correctness and coverage of the implemented program, the
to emit reasoning output after each tool calling, including ob-     benchmark contains 248,853 test functions across its 200 tasks,
servation, considering alternative actions, and reasoning about     averaging a median of 770 tests per task. These suites achieve
next actions. This reasoning output forces explicit processing      an average of 79.7% line coverage, and are hidden from the
rather than blind tool call chaining and creates interpretable      code synthesis agent.
reasoning traces for debugging. Context Management. We              C. Evaluation Metric
compress information passing through the two stages (i.e.,
spec agent and code synthesis agent), to prevent information        Average test pass rate as the primary metric. For each instance
overload. More specifically, we condition the code synthe-          p, let kp denote the number of hidden test cases passed by the
sis agent with the structured behavioral specification artifact     candidate executable and np the total number of test cases for
(i.e., SPEC.md), while discarding verbose reasoning and tool        that instance. The instance-level pass rate is rp = kp /np , and
calling outputs from the spec agent. This preserves essential       the benchmark-level score is the mean over all instances:
findings while removing redundant content that causes atten-                                      1 X kp
                                                                                           r̄ =             .                     (2)
tion dilution when context windows become too large. We                                          |P|     np
                                                                                                        p∈P
summarize the context information between stages rather than
complete conversation histories [2], [19].                          This metric awards partial credit for implementations that
                                                                    reproduce a subset of the target’s behavior, making it sensitive
                 IV. E XPERIMENTAL D ESIGN                          to incremental improvements that a binary resolved/unresolved
   In this section, we present our research questions (RQs),        rate would mask. Note that even the strongest baseline, GPT-
studied dataset, retrievers, used prompt templates, implemen-       5.5-high without spec elicitation, fully resolves only 1 of 200
tation details, and our approach to RQs.                            instances (resolved rate 0.5%) [5], yet achieves a non-trivial r̄
                                                                    reflecting partial behavioral coverage across many instances.
A. Research Question                                                Average test pass rate therefore provides a meaningful signal
  We aim to answer the following research question:                 for comparing pipeline configurations in a regime where full
  • RQ1: What is the effectiveness of S PEC F IRST ?                resolution is rare.
  • RQ2: How effective is S PEC F IRST across task diffi-           Probing Coverage. To quantitatively evaluate the specification
    culty levels?                                                   exploration ability of our approach against the baseline, we
  • RQ3: Does the Spec Agent improve behavioral explo-              introduce probing coverage as the primary metric. Given a
    ration coverage?                                                target binary executable B, let C = {c1 , c2 , . . . , cN } denote the
          TABLE I: Models used in the evaluation.                   TABLE II: Comparison of S PEC F IRST and Direct-Synthesis
 Model                       Family       Type      Reasoning
                                                                    on average test pass rate (%). W/L/T counts the number of
 Qwen3.5-397B-A17B [21]   Open-weights    MoE       On (default)    instances where S PEC F IRST outperforms, underperforms, and
 Qwen3.6-35B-A3B [21]     Open-weights    MoE       On (default)    ties Direct-Synthesis, respectively. We present the improve-
 GPT-5.5-high [22]         Proprietary   Unknown    High effort
 GPT-5.4-mini [23]         Proprietary   Unknown   Medium effort    ment of S PEC F IRST over Direct-Synthesis in ().
                                                                     Model            Direct-Synthesis      S PEC F IRST    W/L/T
set of all N executable lines of code in B. During the probing       Qwen3.5-397B         33.66%         40.84% (+21.3%)   130/58/12
phase, the agent interacts with B by issuing a sequence of           Qwen3.6-35B          27.51%         31.40% (+14.1%)   121/67/12
probes; for each probe, we instrument B to record the set of         GPT-5.5-high         59.02%         65.14% (+10.4%)   150/38/12
                                                                     GPT-5.4-mini         39.09%          41.78% (+6.9%)   119/69/12
lines executed. We use a language-specific instrumentation tool
for each language. For instance, we use go build -cover             a single OpenAI-API-compatible routing proxy LiteLLM [24],
for Go binaries, gcc --coverage for C/C++ binaries, and             with a fresh context per pipeline phase to prevent information
cargo llvm-cov for Rust binaries to capture line-level              leakage between the spec and exec runtimes. All experiments
execution traces for every probe issued during the session.         were conducted using model APIs accessed via a stable API
Upon completion of the probing phase, we aggregate the              provider.
unique recorded lines across all probes to obtain the covered
set Cprobed ⊆ C. Probing coverage is then defined as:                                         V. R ESULTS
                                                                    A. RQ1 - Effectiveness of S PEC F IRST
                              |Cprobed |
                Coverage =               × 100%               (3)      1) Approach: We compare S PEC F IRST against Direct-
                                |C|
                                                                    Synthesis across all four models, with all other experimen-
A higher probing coverage indicates that the agent has exer-        tal conditions held constant. For each model, we run both
cised a larger portion of the program’s behavior during specifi-    configurations on the full 200-instance suite and compute
cation, reflecting a more thorough and complete understanding       the per-instance pass rate rp for each instance. To assess
of the binary’s functionality.                                      whether the improvement in average pass rate is statistically
D. Models                                                           significant, we apply a paired two-sided Wilcoxon signed-rank
   We evaluate four models spanning two families and an             test (α = 0.05). We report win/loss/tie counts to characterise
order of magnitude of capability, selected to disentangle the       the direction and prevalence of the effect across instances.
effect of model scale from the effect of model family. Table I      To further understand whether S PEC F IRST improves not just
summarizes their key properties. All four models are evaluated      the average performance, but the proportion of high-quality
with reasoning enabled, reflecting the multi-step inference the     implementations, we report the fraction of instances achieving
task demands. The Qwen models expose no effort-level control        a pass rate above a threshold t (i.e., 50% - 95%) for both
and are evaluated with thinking on by default. We do not            S PEC F IRST and Direct-Synthesis.
tune any other decoding parameters and use provider defaults           2) Results: S PEC F IRST consistently improves the aver-
throughout, to avoid conflating model capability with hyper-        age test pass rate across all four models, with relative gains
parameter optimization.                                             ranging from 6.9% to 21.3%, up to 65.14% with GPT-5.5-
                                                                    high. Table II shows that S PEC F IRST consistently improves
E. Baselines                                                        the average test pass rate across all four models, with relative
   Direct-Synthesis: The baseline is the original P ROGRAM -        gains ranging from 6.9% (GPT-5.4-mini) to 21.3% (Qwen3.5-
B ENCH pipeline [5], in which the code synthesis agent re-          397B-A17B). All improvements are statistically significant
ceives (D, B) and proceeds directly to implementation without       (p < 0.01), confirming that the gains are not attributable
any preceding specification elicitation phase. This baseline es-    to random variation. The win/loss/tie counts reinforce this
tablishes the performance ceiling of the standard approach and      conclusion: across all models, S PEC F IRST outperforms the
measures the net gain attributable to the entire specification      baseline at least on more than 59% of instances, with the
elicitation.                                                        strongest model (GPT-5.5-high) winning on 75% (150/200)
   Note that we use the same scaffold (i.e., official mini-swe-     instances. Taken together, these results confirm that explicitly
agent) as the code synthesis agent for both Direct-Synthesis        eliciting a behavioral specification before implementation is
and S PEC F IRST. In other words, the only difference between       a robust and model-agnostic intervention that materially im-
Direct-Synthesis and S PEC F IRST is that we introduce spec         proves program re-implementation fidelity.
agent in S PEC F IRST, and other settings are kept the same.           S PEC F IRST does not merely lift average pass rates; it
                                                                    significantly expands the upper tail of the score distribution
F. Implementation details                                           by driving a higher proportion of programs to near-
   Each run executes in an isolated, no-network Docker con-         perfection (i.e., the programs that pass almost all tests).
tainer from the task image by ProgramBench. The same model          Table III presents the proportion of programs, where the test
is used for both specification elicitation and code synthesis       pass rate is larger than a threshold (50% to 95%). For instance,
phases. Our local modifications to each are released as patches     at the most stringent thresholds, S PEC F IRST triples the rate of
against those exact commits. All models are accessed through        near-perfect solutions from 5.5% to 16.5% (for t ≥ 90%) and
                                                                   problems. Crucially, the largest absolute improvements often
Listing 2: Selected entries from SPEC.md elicited by S PEC A-      manifest where the baseline struggles the most. For instance,
GENT for the gomplate instance.                                    on Hard instances, the frontier model GPT-5.5-high experi-
## Function Set
                                                                   ences its most pronounced surge, improving the average test
The executable provides gomplate namespaces and aliases in         pass rate from 30.8% to 40.0%, which represents a remarkable
addition to Go template built-ins. Important observed              29.9% improvement. This pattern indicates that a rigorous, de-
functions and aliases include:
                                                                   coupled specification phase serves as a vital cognitive scaffold,
- Data: datasource/ds, include, datasourceExists,                  allowing models to systematically decompose intricate logic
datasourceReachable...
- Collections: coll.Dict/dict, coll.Slice, coll.GoSlice...         that would otherwise cause a direct code-generation attempt
## Flags
                                                                   to fail.
$ ./executable --help
Process text files with Go templates                               C. RQ3 - Effectiveness of Spec Agent
Usage:
  gomplate [flags]
Flags:
                                                                      1) Approach: The spec agent is dedicated to probing the
  -d, --datasource datasource      datasource in alias=URL         binary and eliciting a behavioral specification before imple-
form.    Specify multiple times to add multiple sources.
  ...
                                                                   mentation begins. To assess whether it actually improves
                                                                   exploratory coverage, we measure probing coverage of S PEC -
## Edge Cases and Compatibility Notes
  --in plus --file or --input-dir: invalid (exclusive-input
                                                                   F IRST and compare it against Direct-Synthesis, which per-
conflict).                                                         forms no dedicated elicitation phase.
  --file plus --input-dir: likewise invalid.
  ...                                                                 2) Results: S PEC F IRST consistently elicits broader
                                                                   behavioral coverage than Direct-Synthesis significantly,
                                                                   achieving 9.4%–18.5% improvement. The gain originates
more than quadruples it from 1.5% to 6.5% (for t ≥ 95%). We
                                                                   from the spec agent rather than from the code synthesis
observe a consistently similar trend across the other evaluated
                                                                   agent. Table V reports probing coverage across all four
models.
                                                                   models. S PEC F IRST achieves 58.3%–60.3% total coverage,
TABLE III: Proportion of programs that have a test pass rate       an improvement of 9.4%–18.5% over Direct-Synthesis on
larger than a threshold t using GPT-5.5-high, with the 95%         every model. All improvements are statistically significant
confidence interval in [].                                         (p < 0.05). Its spec agent covers more behaviors than the
      ≥ t(%)         Baseline              S PEC F IRST
                                                                   baseline in 63.5%–77.2% of instances.
      ≥ 50     69.0% [62.3%, 75.0%]   74.0% [67.5%, 79.6%]            Decomposing S PEC F IRST by component reveals that the
      ≥ 70     42.5% [35.9%, 49.4%]   55.5% [48.6%, 62.2%]         spec agent alone (54.9%–58.3%) consistently exceeds the code
      ≥ 90       5.5% [3.1%, 9.6%]    16.5% [12.0%, 22.3%]
      ≥ 95       1.5% [0.5%, 4.3%]     6.5% [3.8%, 10.8%]          synthesis agent (31.2%–51.3%) on all models, and the union
                                                                   adds only marginally over the spec agent. This confirms that
   Listing 2 shows an example specification elicited for the       the coverage gain is driven by the dedicated elicitation phase,
gomplate instance. For example, S PEC F IRST records a thor-       not by incidental exploration during code synthesis.
ough SPEC.md containing all function sets and edge cases.
An exec agent that reads it before writing code can implement      D. RQ4 - Impact of Spec Agent on Code Synthesis Agent’s
each of these behaviors correctly on the first attempt rather      behavior
than guessing, which directly reduces the behavioral residual
between B̂ and B and explains the consistent pass rate lift           1) Approach: To understand how the elicited specification
across all four models.                                            shapes the code synthesis agent’s behavior during the run,
                                                                   we record the codebase size (lines of code) at every agent–
B. RQ2 - Effectiveness across different difficulty levels          environment turn for both S PEC F IRST and Direct-Synthesis,
   1) Approach: To assess the robustness of S PEC F IRST, we       and normalise each turn index to [0, 1] by dividing by the run’s
analyze its performance across different task-difficulty tiers:    total number of turns.
Easy (n = 28), Medium (n = 143), and Hard (n = 29), with              2) Results: Providing a persistent behavioral specifi-
the difficulty tags provided in the benchmark.                     cation before implementation shifts the code synthesis
   2) Result: S PEC F IRST consistently outperforms Direct-        agent from a probe-then-build pattern to an earlier, more
Synthesis across all difficulty levels and all evaluated           sustained building phase. Figure 2 tracks the growth of the
models. For instance, GPT-5.5-high experiences its most            reconstructed codebase as the code synthesis agent progresses
pronounced surge, improving the average test pass rate             through its turns. S PEC F IRST starts implementation earlier
from 30.8% to 40.0%, which represents a remarkable                 than baseline. In the baseline, the early portion of the run
29.9%. Rather than being restricted to a specific tier of tasks    is dominated by exploratory probing. For instance, Figure 3
or a particular model architecture, the S PEC F IRST shows a       compares the probing phase and implementation phase of
universal improvement. More importantly, the performance           S PEC F IRST and the baseline on four instances. On age, for
gains are not confined to trivial or moderately difficult tasks.   example, the baseline spends most turns inspecting behavior
S PEC F IRST delivers substantial improvements on the hardest      before attempting to dump the entire 841-line implementation
 TABLE IV: Comparison of the average test pass rates between Direct-Synthesis and S PEC F IRST across task difficulty levels.
 Cells show the pass rate change as Direct-Synthesis → S PEC F IRST (relative improvement).
                                    Model                    Easy (n = 28)             Medium (n = 143)              Hard (n = 29)
                                    Qwen3.5-397B        42.9% → 52.9% (+23.3%)     34.6% → 42.1% (+21.7%)       20.0% → 23.0% (+15.0%)
                                    Qwen3.6-35B         37.8% → 42.2% (+11.6%)     28.1% → 32.1% (+14.2%)       14.5% → 17.6% (+21.4%)
                                    GPT-5.5-high        73.7% → 78.9% (+7.1%)       61.9% → 67.5% (+9.0%)       30.8% → 40.0% (+29.9%)
                                    GPT-5.4-mini        49.7% → 57.4% (+15.5%)      40.7% → 42.8% (+5.2%)        21.0% → 21.9% (+4.3%)


                                                              Direct-Synthesis               Ours (Code Synthesis)
                             Qwen3.5-397B                        GPT-5.4-mini                        GPT-5.5-high                   Qwen3.6-35B
codebase size (LOC)




                                                     1000
                      2000                                                                   750                          2000
                                                                                             500
                      1000                              500
                                                                                                                          1000
                                                                                             250
                         0                                 0                                   0                              0
                         0.0        0.5           1.0      0.0           0.5           1.0     0.0        0.5          1.0    0.0         0.5         1.0
                               run progress                       run progress                        run progress                   run progress
 Fig. 2: Median reconstructed codebase size (lines of code) as a function of normalised run progress (0 = start, 1 = termination),
 with shaded interquartile range (IQR) across instances. The y-axis is capped at the 95th percentile of final codebase sizes to
 suppress outliers. A curve that rises earlier indicates the agent commits to writing code sooner in its budget; a higher terminal
 value indicates a larger final codebase.
 TABLE V: Probing coverage of S PEC F IRST versus Direct- they have understood enough, not because they exhausted
 Synthesis. For S PEC F IRST, coverage is reported separately for their budget. In other words, simply allocating more compute
 the spec agent, the code synthesis agent, and their union. Win would not help. S PEC F IRST addresses this by equipping the
 denotes the proportion of instances where S PEC F IRST’s union code synthesis agent with a persistent specification established
 coverage exceeds Direct-Synthesis.                                  through the dedicated spec agent prior to implementation,
       Model                          S PEC F IRST          Direct-Synthesis     Win     enabling higher coverage of the specification, as demonstrated
                                Spec / Synthesis / Union                                 in RQ3.
       Qwen3.5-397B               58.0%/51.0%/59.8%              51.9%         77.2%
       Qwen3.6-35B                54.9%/51.3%/58.3%              49.2%         71.2%        Introducing the spec agent leads to larger codebases
       GPT-5.5-high               58.3%/31.2%/60.3%              55.1%         66.2%     and higher pass rates across all models. The final codebase
       GPT-5.4-mini               56.5%/41.7%/58.6%              52.1%         63.5%     produced under S PEC F IRST is 7–29% larger across models
                                                                                         (shaded IQR), consistent with agents writing more complete
 in a single action, inevitably failing due to an exhausted de-                          implementations rather than terminating early under behavioral
 bugging budget. The baseline typically exhausts 11 to 20 turns                          uncertainty. This aligns with RQ3, where we demonstrate
 probing the binary’s behavior. In contrast, S PEC F IRST directly                       that a higher probing coverage from the spec agent yields
 resolves this bottleneck by externalizing exploration into a                            a more complete specification, which in turn drives broader
 persistent SPEC.md during the dedicated spec phase. Instead                             implementation coverage.
 of wasting implementation turns on trial-and-error probing,                                Together, these results show that specification elicitation
 the code synthesis agent spends just 2 to 9 turns establishing                          does not merely provide additional context—it fundamentally
 context before immediately shifting to implementation.                                  restructures how the exec agent allocates its effort, shifting the
    Direct-Synthesis agents stop early, not because they run                             run profile from a probe-then-build pattern toward an earlier,
 out of budget, but because they run out of behavioral un-                               more sustained building phase.
 derstanding. One possible attribute of the weaker performance                                                  VI. R ELATED W ORK
 of Direct-Synthesis to insufficient turn budget: if probing
 consumes too many turns, the agent has little budget left for                           A. LLM-based Code Generation and Program Synthesis
 implementation. To rule out this explanation, we examine the                               The application of large language models to code synthesis
 number of turns consumed by Direct-Synthesis. The results                               has progressed from template-filling approaches [25] through
 are striking: zero instances reach the 1,000-turn step limit,                           neural program induction [26] to contemporary autoregressive
 and all instances terminate early by agent choice, consuming                            models trained on hundreds of billions of tokens of source
 a median of only 22–177 turns (2–18% of the available                                   code [3], [27]–[30]. These models achieve impressive perfor-
 budget). The bottleneck is therefore not turn budget but the                            mance on function-level benchmarks such as HumanEval [3]
 quality of behavioral understanding the agent constructs before                         and MBPP [31], where a docstring and a handful of unit-
 it stops: agents terminate voluntarily because they believe                             test examples provide a highly constrained, unambiguous
                                                                 probe impl edits   properties from execution traces, but require either source
 codesnap                                                         13 7        2
                                                                   3 12 5           instrumentation or passive observation of existing traces rather
 gomplate                                                         16 15 6
                                                                   9 17 10          than active, agent-directed probing. LLM-based decompila-
     hush                                                         11 15 8           tion [43] recovers source from binaries at the instruction level
                                                                   2    8     3
      age                                                         20 11 2           and requires disassembly access that our setting explicitly
                                                                   2 25 9
                                                                                    prohibits. Program translation approaches [44] operate source-
            0.0     0.2       0.4       0.6      0.8       1.0

                              turn fractionOurs (Code Synthesis)
                  Direct-Synthesis                                                  to-source and assume a complete, readable specification is
       probe phase (no source written yet)               source-write event         already available. S PEC F IRST occupies a distinct position:
       implementation phase (compile / test / submit)                               it actively probes a black-box binary under maximal access
                                                                                    restrictions and produces a natural-language behavioral spec-
Fig. 3: Comparison of the code synthesis phase between                              ification consumable directly by a downstream LLM code
S PEC F IRST and baseline from four GPT-5.5 cases. Hatched                          synthesis agent.
areas represent the exploration calls, and solid areas denote
the implementation calls. Vertical ticks indicate source-write                                            VII. D ISCUSSION
turns.
                                                                                    A. Failure case analysis
specification. Scaling the same paradigm to repository-level or
                                                                                       To understand the failure case and identify their root causes,
whole-program tasks reveals a pronounced degradation. SWE-
                                                                                    we randomly sample 50 test failure cases across four models
bench [2] demonstrates that resolving real GitHub issues,
                                                                                    and manually label each by examining three artifacts jointly:
which requires understanding repository context far harder
                                                                                    (i) the failing-test message (what behavior the test exercises
than synthesizing isolated functions. Agentic frameworks [2],
                                                                                    and what concrete output, exit code, or error string it expects),
[19], [32], [33] couple LLMs with tool-use loops (shell, file
                                                                                    (ii) the Spec.md (whether and how precisely the behavior
editors, web search) to extend their reach, yet they still rely
                                                                                    is described), and (iii) the relevant source snippet (whether
on a task description written by a human that is treated as a
                                                                                    the implementation contains the corresponding code path and
fixed, complete specification. P ROGRAM B ENCH [5] introduces
                                                                                    whether it matches Spec.md). We observed the following five
a harder variant: the reference behavior is embodied in a black-
                                                                                    types of failures:
box binary, not a text description, forcing the agent to discover
the specification rather than consume it. Our work is the first                     F1: Spec Omission (10%). Spec.md never documents the
to explicitly design the discovery step as a first-class, reusable                  features that the test exercises (e.g., the CLI flag, subcommand,
pipeline component when building programs from scratch.                             error path, or output channel). It means that the spec agent
                                                                                    failed to discover and collect the behavior from the binary.
B. Requirements Elicitation in Software Engineering                                 F2: Wrong Spec Description (4%). Spec.md describes the
   Requirements engineering (RE) is among the most studied                          behavior incorrectly (e.g., attributing a message to stderr
disciplines in SE [11]–[13], with a recurring finding that                          when the test asserts stdout). The implementation was faith-
written artifacts systematically omit behavioral detail, contain                    ful to Spec.md, but Spec.md itself contradicted the binary’s
ambiguities, and conflict with one another [17], [18], making                       actual behavior.
elicitation through interaction the standard remedy [14], [34].                     F3: Inaccurate Spec Description (26%). Spec.md documents
NLP and LLM techniques have been applied to automate parts                          the feature under test, but the description is insufficiently
of this process, including ambiguity detection [18], traceability                   precise, forcing the implementation agent to guess. For ex-
recovery [35], and requirements inconsistency detection [36],                       ample, Spec.md may document that invalid input produces an
but these approaches treat requirements as textual artifacts to                     error without specifying the exit code or output channel; the
be processed rather than behaviors to be discovered through                         implementation chooses rc=1 with a stderr message, while
interaction. S PEC AGENT takes the complementary view, in-                          the test expects rc=2 with a stdout message.
stantiating an LLM as an active elicitor that probes a running                      F4: Execution Fault (52%). Spec.md describes the behavior
system rather than analyzing static documents—closest in                            correctly and completely, yet the implementation diverges.
spirit to behavior-driven development [37], [38], but producing                     Common shapes include a subcommand recognized in help
a requirements artifact rather than a test suite.                                   text but rejected by the dispatcher, a flag was parsed but
                                                                                    its effect never applied, or an error format that contradicts
C. Black-box Program Analysis and Specification Extraction                          Spec.md’s documented convention. This is the dominant fail-
   The closest prior work to S PEC F IRST’s elicitation loop is                     ure mode, indicating that even a correct Spec.md does not
the line of research on protocol reverse engineering, which                         guarantee a correct implementation for complex behavioral
probes network binaries to extract message formats and state                        constraints.
machines [39], [40]. These approaches share our black-box                           F5: Environment-dependent Error (8%). Failures are
observation model but produce machine-readable protocol                             environment-dependent (e.g., NS server strings embedded in
grammars for security analysis rather than natural-language                         error messages, missing test-wrapper paths, or subprocess
behavioral specifications for code generation. Specification                        timeouts from absent toolchains). These reflect benchmark
mining [41] and dynamic invariant detection [42] infer formal                       infrastructure noise rather than agent deficiencies.
Implications. Although S PEC F IRST prove the use of spec             TABLE VII: Mean per-instance cost (USD) for Direct-
agent is a promising direction for building a program from            Synthesis and S PEC F IRST. For S PEC F IRST, cost is broken
scratch. Our failure analysis suggests the following research         down into the spec agent, code synthesis agent, and their total;
direction. The dominant failure mode (F4, 52%) indicates that         percentages indicate overhead relative to Direct-Synthesis.
closing the remaining gap requires stronger execution-stage            Model          Direct-Synthesis    S PEC F IRST (Spec/Synthesis/Total)
reasoning (e.g., better instruction following, self-consistency        Qwen3.5-397B        $2.56         $0.95 / $2.84 (+11%) / $3.79 (+48%)
                                                                       Qwen3.6-35B         $2.03         $0.50 / $2.68 (+32%) / $3.17 (+56%)
checking against Spec.md, and test-driven repair loops), rather        GPT-5.4-mini        $0.35         $0.25 / $0.29 (-17%) / $0.53 (+51%)
than improvements to spec elicitation alone. F1, F2, and               GPT-5.5-high        $2.54         $3.16 / $2.69 (+6%) / $5.85 (+130%)
F3 (40% combined) suggest that elicitation coverage and
behavioral fidelity remains an open problem; future work could        more feature-complete implementations, modestly increasing
further explore targeted probing strategies that systematically       its own cost as well (+6%–+32% for most models). The
exercise under-documented surfaces such as error paths, flag          exception is GPT-5.4-mini, where synthesis cost decreases by
interactions, and output routing.                                     17%, suggesting that a clearer upfront specification reduces
                                                                      exploratory overhead during coding. The largest overhead
B. Does the specification’s format matter?                            occurs with GPT-5.5-high (+130%), driven primarily by the
   To understand the impact of specification format, we com-          cost of the spec agent itself rather than by synthesis. Overall,
pared the following formats, differing only in the deliverable-       the cost increase is a direct reflection of S PEC F IRST doing
instruction paragraph of the task prompt; all other prompt text,      more useful work—broader behavioral exploration and more
probing rules, and limits are identical across conditions. Note       complete implementation—rather than redundant computation.
that all the results reported in RQs are based on Sections.
Sections. The format we used is introduced in Section VII-B,
where the agent is asked to write SPEC.md as structured               D. Threats to Validity
Markdown under named headings.
Freeform. The agent chooses its own structure and coverage            Internal Validity The S PEC F IRST uses two agents instead of
criteria. This condition isolates whether imposed structure           one, meaning it spends more budget than the baseline (without
helps or hurts downstream exec quality.                               spec agent). The risk is that the improvement is not actually
OpenSpec. The agent writes SPEC.md in the Open-                       from the value of having a specification, but simply because
Spec format [15], structuring the document as a ##                    the model got a larger compute budget. To alleviate this threat,
Purpose section followed by ### Requirement: blocks,                  as shown in RQ4, 100% of the runs ended early by choice.
each annotated with RFC 2119 keywords (MUST/SHALL,                    Therefore, giving the baseline models more compute wouldn’t
SHOULD , MAY ), and concrete #### Scenario: examples                  have naturally increased their test pass rate.
in GIVEN/WHEN/THEN form. This condition tests whether                 External Validity Our evaluation covers deterministic
a more formal, requirements-engineering vocabulary improves           command-line programs in P ROGRAM B ENCH; results may
the precision of the elicited specification.                          not generalize to programs with non-deterministic behavior,
   We compare the average test pass rate of S PEC F IRST using        graphical interfaces, or complex inter-process communication.
the above different format with GPT-5.4-mini on randomly              We evaluate four models on a single scaffold (SWE-agent);
sampled 50 instances2 . Table VI compares the effectiveness           while consistent gains across two model families suggest
of different formats. As shown, every specification format            robustness, results may differ for other models and scaffolds.
improves on the baseline, while Sections improves the most            Although S PEC F IRST requires an executable binary for spec
and outperforms other formats.                                        elicitation, the binary serves as a proxy for any executable
                                                                      oracle that exposes a probe-and-observe interface, such as a
         TABLE VI: Specification Format Comparison                    running REST API, a containerized service, a compiled SDK,
                 Format                 Pass Rate (%)                 or a remote CLI are all equivalent from the spec agent’s per-
                 Baseline (No Spec)         55.9%                     spective. The key prerequisite is not a binary specifically but
                 Freeform                   60.7%                     any queryable reference or human, a condition met by most
                 OpenSpec                   61.7%
                 Sections                   62.6%                     software maintenance, migration, and integration scenarios.
                                                                      Construct Validity The study’s main evaluation metric (a
C. Cost of S PEC F IRST                                               0–100% scale average test pass rate) combines two different
  Table VII reports the mean per-instance cost for Direct-            things: whether the agent can actually build a working pro-
Synthesis and S PEC F IRST. The total cost of S PEC F IRST is         gram, and whether that program behaves correctly. There was
higher by 48%–130% across models, which is expected: the              a risk that failures such as compilation failures (like a missing
spec agent constitutes an additional inference phase ($0.25–          compile.sh) would unfairly tank the average scores. However,
$3.16 per instance), and the more complete specification              these total technical failures were extremely rare (at most 3
produced leads the code synthesis agent to generate larger,           out of 200 runs). This means when an agent scored a 0%, it
                                                                      was not because it could not build a working program; it was
  2 We choose to use GPT-5.4-mini and a subset due to budget limit.   because the program’s actual behavior was completely wrong.
                     VIII. C ONCLUSION                                                            R EFERENCES
   We presented S PEC F IRST, a two-stage agentic frame-            [1] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and
work that explicitly decouples behavioral specification elic-           K. Narasimhan, “Swe-bench: Can language models resolve real-world
                                                                        github issues?” in International Conference on Learning Representa-
itation from code synthesis for from-scratch program re-                tions, vol. 2024, 2024, pp. 54 107–54 157.
implementation. By dedicating a separate spec agent to sys-         [2] J. Yang, C. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan, and
tematically probe the binary and produce a structured speci-            O. Press, “Swe-agent: Agent-computer interfaces enable automated soft-
                                                                        ware engineering,” Advances in Neural Information Processing Systems,
fication prior to implementation, S PEC F IRST addresses three          vol. 37, pp. 50 528–50 652, 2024.
fundamental limitations of single-loop baselines: insufficient      [3] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan,
behavioral exploration, specification loss over multi-turns, and        H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
uncorrected error propagation. Experiments on all 200 P RO -            language models trained on code,” arXiv preprint arXiv:2107.03374,
                                                                        2021.
GRAM B ENCH instances across four frontier models demon-            [4] GitHub, “GitHub Copilot: Your AI Pair Programmer,” https://github.
strate consistent improvements in test pass rates (6.9%–21.3%)          com/features/copilot, 2021.
and binary exploration coverage (9.4%–18.5%). Our results           [5] J. Yang, K. Lieret, J. Ma, P. Thakkar, D. Pedchenko, S. Sootla,
                                                                        E. McMilin, P. Yin, R. Hou, G. Synnaeve et al., “Programbench:
suggest that treating requirements elicitation as a first-class         Can language models rebuild programs from scratch?” arXiv preprint
phase is a promising paradigm for advancing LLM agents on               arXiv:2605.03546, 2026.
complex, from-scratch software construction tasks.                  [6] X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan,
                                                                        Y. Song, B. Li, J. Singh et al., “Openhands: An open platform for ai
                                                                        software developers as generalist agents,” in International Conference
                                                                        on Learning Representations, vol. 2025, 2025, pp. 65 882–65 919.
                                                                    [7] V. Dongre, R. A. Rossi, V. D. Lai, D. S. Yoon, D. Hakkani-Tür, and
                                                                        T. Bui, “Drift no more? context equilibria in multi-turn llm interactions,”
                                                                        arXiv preprint arXiv:2510.07777, 2025.
                                                                    [8] P. Laban, H. Hayashi, Y. Zhou, and J. Neville, “Llms get lost in multi-
                                                                        turn conversation,” arXiv preprint arXiv:2505.06120, 2025.
                                                                    [9] A. B. Labate, V. M. de Sousa, S. R. Fiorini, L. G. Azevedo, R. M.
                                                                        Thiago, and V. T. da Silva, “Solving context window overflow in ai
                                                                        agents,” arXiv preprint arXiv:2511.22729, 2025.
                                                                   [10] Y. Ma and J.-H. Liu, “Quantifying laziness, decoding suboptimality,
                                                                        and context degradation in large language models,” arXiv preprint
                                                                        arXiv:2512.20662, 2025.
                                                                   [11] B. Nuseibeh and S. Easterbrook, “Requirements engineering: a
                                                                        roadmap,” in Proceedings of the Conference on the Future of Software
                                                                        Engineering, 2000, pp. 35–46.
                                                                   [12] I. Sommerville, Software engineering, 9/E. Pearson Education India,
                                                                        2011.
                                                                   [13] K. Wiegers and J. Beatty, Software requirements. Pearson Education,
                                                                        2013.
                                                                   [14] D. Zowghi and C. Coulin, “Requirements elicitation: A survey of tech-
                                                                        niques, approaches, and tools,” in Engineering and managing software
                                                                        requirements. Springer, 2005, pp. 19–46.
                                                                   [15] Fission AI, “Openspec: A lightweight spec-driven framework for ai-
                                                                        assisted development,” 2026, accessed: 2026-06-10. [Online]. Available:
                                                                        https://openspec.dev
                                                                   [16] GitHub, “Github spec kit: Toolkit to help you get started with spec-
                                                                        driven development,” 2026, accessed: 2026-06-29. [Online]. Available:
                                                                        https://github.github.com/spec-kit/
                                                                   [17] D. M. Berry, E. Kamsties, and M. M. Krieger, “From contract drafting
                                                                        to software specification: Linguistic sources of ambiguity,” 2003.
                                                                   [18] A. Ferrari, G. Lipari, S. Gnesi, and G. O. Spagnolo, “Pragmatic
                                                                        ambiguity detection in natural language requirements,” in 2014 IEEE
                                                                        1st International Workshop on Artificial Intelligence for Requirements
                                                                        Engineering (AIRE). IEEE, 2014, pp. 1–8.
                                                                   [19] X. Yang, J. Zhou, M. Pacheco, W. Zhu, P. He, S. Wang, K. Liu,
                                                                        and R. Pan, “Lingxi: Repository-level issue resolution framework
                                                                        enhanced by procedural knowledge guided scaling,” arXiv preprint
                                                                        arXiv:2510.11838, 2025.
                                                                   [20] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao,
                                                                        “React: Synergizing reasoning and acting in language models,” arXiv
                                                                        preprint arXiv:2210.03629, 2022.
                                                                   [21] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao,
                                                                        C. Huang, C. Lv et al., “Qwen3 technical report,” arXiv preprint
                                                                        arXiv:2505.09388, 2025.
                                                                   [22] OpenAI. (2026, 4) Introducing gpt-5.5. [Online]. Available: https:
                                                                        //openai.com/index/introducing-gpt-5-5/
                                                                   [23] ——. (2026, 3) Introducing gpt-5.4 mini and nano. [Online]. Available:
                                                                        https://openai.com/index/introducing-gpt-5-4-mini-and-nano/
                                                                   [24] BerriAI, “Litellm: Call 100+ llms using the openai input/output format,”
                                                                        https://github.com/BerriAI/litellm, Aug. 2023. [Online]. Available:
                                                                        https://github.com/BerriAI/litellm
[25] S. Gulwani, O. Polozov, and R. Singh, “Program synthesis,” Foundations         [35] J. H. Hayes, A. Dekhtyar, and S. K. Sundaram, “Advancing candidate
     and Trends in Programming Languages, vol. 4, no. 1-2, pp. 1–119, 2017.              link generation for requirements tracing: The study of methods,” IEEE
[26] J. Devlin, J. Uesato, S. Bhupatiraju, R. Singh, A.-r. Mohamed, and                  Transactions on Software Engineering, vol. 32, no. 1, pp. 4–19, 2006.
     P. Kohli, “Robustfill: Neural program learning under noisy i/o,” in            [36] S. Bashir, A. Ferrari, A. Khan, P. E. Strandberg, Z. Haider, M. Saa-
     International conference on machine learning. PMLR, 2017, pp. 990–                  datmand, and M. Bohlin, “Requirements ambiguity detection and ex-
     998.                                                                                planation with llms: An industrial study,” in 2025 IEEE International
[27] E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou, S. Savarese,              Conference on Software Maintenance and Evolution (ICSME). IEEE,
     and C. Xiong, “Codegen: An open large language model for code with                  2025, pp. 620–631.
     multi-turn program synthesis,” arXiv preprint arXiv:2203.13474, 2022.          [37] J. F. Smart and J. Molak, BDD in Action: Behavior-driven development
[28] B. Roziere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi,          for the whole software lifecycle. Simon and Schuster, 2023.
     J. Liu, R. Sauvestre, T. Remez et al., “Code llama: Open foundation            [38] K. Karhu, T. Repo, O. Taipale, and K. Smolander, “Empirical observa-
     models for code,” arXiv preprint arXiv:2308.12950, 2023.                            tions on software testing automation,” in 2009 International Conference
[29] D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen,                        on Software Testing Verification and Validation. IEEE, 2009, pp. 201–
     X. Bi, Y. Wu, Y. Li et al., “Deepseek-coder: when the large language                209.
     model meets programming–the rise of code intelligence,” arXiv preprint         [39] J. Caballero, H. Yin, Z. Liang, and D. Song, “Polyglot: Automatic
     arXiv:2401.14196, 2024.                                                             extraction of protocol message format using dynamic binary analysis,”
[30] R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou,                     in Proceedings of the 14th ACM conference on Computer and commu-
     M. Marone, C. Akiki, J. Li, J. Chim et al., “Starcoder: may the source              nications security, 2007, pp. 317–329.
     be with you!” arXiv preprint arXiv:2305.06161, 2023.                           [40] P. M. Comparetti, G. Wondracek, C. Kruegel, and E. Kirda, “Prospex:
[31] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,                    Protocol specification extraction,” in 2009 30th IEEE Symposium on
     E. Jiang, C. Cai, M. Terry, Q. Le et al., “Program synthesis with large             Security and Privacy. IEEE, 2009, pp. 110–125.
     language models,” arXiv preprint arXiv:2108.07732, 2021.                       [41] G. Ammons, R. Bodı́k, and J. R. Larus, “Mining specifications,” ACM
[32] X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan,                       Sigplan Notices, vol. 37, no. 1, pp. 4–16, 2002.
     Y. Song, B. Li, J. Singh et al., “Openhands: An open platform for ai           [42] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco, M. S.
     software developers as generalist agents,” in International Conference              Tschantz, and C. Xiao, “The daikon system for dynamic detection of
     on Learning Representations, vol. 2025, 2025, pp. 65 882–65 919.                    likely invariants,” Science of computer programming, vol. 69, no. 1-3,
[33] P. Gao, Z. Tian, X. Meng, X. Wang, R. Hu, Y. Xiao, Y. Liu, Z. Zhang,                pp. 35–45, 2007.
     J. Chen, C. Gao et al., “Trae agent: An llm-based agent for software           [43] H. Tan, Q. Luo, J. Li, and Y. Zhang, “Llm4decompile: Decompiling
     engineering with test-time scaling,” arXiv preprint arXiv:2507.23370,               binary code with large language models,” in Proceedings of the 2024
     2025.                                                                               Conference on Empirical Methods in Natural Language Processing,
[34] E. D. Canedo, A. T. S. Calazans, G. R. S. Silva, P. H. T. Costa, R. P.              2024, pp. 3473–3487.
     de Mesquita, and E. T. S. Masson, “Creativity and design thinking as           [44] B. Roziere, M.-A. Lachaux, L. Chanussot, and G. Lample, “Unsu-
     facilitators in requirements elicitation,” International Journal of Software        pervised translation of programming languages,” Advances in neural
     Engineering and Knowledge Engineering, vol. 32, no. 10, pp. 1527–                   information processing systems, vol. 33, pp. 20 601–20 611, 2020.
     1558, 2022.
