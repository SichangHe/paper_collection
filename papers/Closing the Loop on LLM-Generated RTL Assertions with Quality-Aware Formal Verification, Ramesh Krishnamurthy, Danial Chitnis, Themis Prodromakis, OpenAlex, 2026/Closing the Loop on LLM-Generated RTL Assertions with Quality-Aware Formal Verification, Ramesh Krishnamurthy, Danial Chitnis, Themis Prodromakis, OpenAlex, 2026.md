                                              Closing the Loop on LLM-Generated RTL
                                           Assertions with Quality-Aware Formal Verification
                                                                        Ramesh Krishnamurthy, Danial Chitnis, Themis Prodromakis
                                                                 School of Engineering, The University of Edinburgh, Edinburgh, United Kingdom
                                                                                              rkrishn3@ed.ac.uk


                                            Abstract—Large language model (LLM) based assertion gen-           not necessarily coincide with the cycle at which the assertion
                                         eration is making formal verification more accessible for Register    actually fails.
                                         Transfer Level (RTL) designs, but three practical issues remain.
                                                                                                                  Recent related work covers important parts of this picture,
                                         Generated properties can pass for the wrong reason, proof cost
                                                                                                               but not the whole loop. Assertion-generation systems such as
arXiv:2606.21451v1 [cs.AR] 19 Jun 2026




                                         can vary widely from one design to another, and failing traces are
                                         hard to interpret. This paper presents a lightweight, open-source     AssertLLM, Spec2Assertion, AssertionForge, and DeepAssert
                                         framework that addresses these issues in one loop. Our method         improve how properties are synthesized from text, structure,
                                         combines mutation-guided refinement to reject weak assertions,        or module context [2], [3], [9], [10]. Recent work has also
                                         including vacuous ones and those that fail to distinguish faulty
                                                                                                               coupled LLM-generated properties with mutation testing to
                                         behavior, a solver-selection stage that chooses among candidate
                                         Satisfiability Modulo Theories (SMT) backends using RTL struc-        assess invariant quality [11]. In our flow, mutation serves a
                                         ture, and causal narrative synthesis to explain why a proof failed.   different role: mutant outcomes trigger verification harness
                                         Across diverse RTL designs, the framework improves confidence         refinement and help decide whether the harness is strong
                                         in generated assertions, reduces runtime variability over fixed-      enough to proceed. This distinction is deliberate. Assessing
                                         solver choices, and produces failure explanations that remain
                                                                                                               invariant quality is useful as a diagnostic, but our goal is
                                         grounded in the counterexample trace. The results suggest that
                                         quality-aware closure, rather than assertion generation alone, is     closure: when mutants survive, the framework uses that evi-
                                         the missing step for practical LLM-assisted formal verification.      dence to strengthen the harness or to recognize that a survivor
                                            Index Terms—Formal Verification, LLM, Verification Automa-         remains unobservable within the explored proof window. The
                                         tion                                                                  two strategies are therefore complementary: quality assessment
                                                                                                               can score a generated property set, whereas mutation-guided
                                                                I. I NTRODUCTION                               refinement uses the same mutation evidence as a control
                                            Formal verification (FV) offers a rigorous alternative to          signal for refinement. Agentic workflow systems such as
                                         simulation for proving hardware correctness, but its deploy-          Saarthi show how LLM agents can orchestrate formal tasks
                                         ment remains constrained by the effort needed to write high-          [12], but the quality-control layer, i.e., checking assertion
                                         quality assertions and configure proof backends effectively.          meaningfulness, selecting a backend, and explaining failures
                                         Recent LLM-based frameworks have reduced the front-end                from trace evidence, remains the gap addressed here.
                                         burden of assertion generation, including systems that translate         This paper presents a quality-aware framework for LLM-
                                         specifications into assertions and systems that use both the          generated RTL assertions. The framework combines: (i)
                                         design specification and the RTL code as input [1]–[3]. More          Mutation-Guided Refinement (MGR) to reject weak assertions,
                                         broadly, recent surveys and agentic workflows show growing            including vacuous ones and those that fail to distinguish faulty
                                         interest in LLM-assisted hardware design and verification, but        behavior, (ii) an architecture-aware solver selector that uses
                                         they also highlight the need for stronger quality control and         RTL structure before the design is translated into solver-
                                         evaluation tied to actual proof results from formal tools [4],        specific forms, and (iii) Causal Narrative Synthesis (CNS)
                                         [5]. Generation alone, however, is not enough. A generated            to summarize failing traces in human-readable form. The
                                         assertion may pass vacuously, run slowly when paired with an          contribution is a compact loop that improves confidence in
                                         unsuitable solver backend, or fail with a trace that is hard to       generated assertions, stabilizes runtime, and makes failures
                                         understand.                                                           easier to debug in an open-source flow built on Yosys-based
                                            We target these three bottlenecks directly. First, vacuity         tooling [13].1
                                         remains a known threat in formal verification because prop-
                                         erties can hold for trivial reasons rather than because the                                   II. F RAMEWORK
                                         intended behavior was actually exercised [6]. Second, backend
                                         selection remains highly instance-dependent; prior work on              Figure 1 summarizes the proposed flow. Given an RTL
                                         SMT formulas and word-level netlists shows that structural            design and a natural-language specification, an LLM first pro-
                                         features can strongly affect solver performance [7], [8]. Third,      duces an initial verification harness. In this paper, a verification
                                         raw counterexample traces remain difficult to interpret, espe-        harness means the formal assertions, assumptions, and any
                                         cially for users who are new to FV, because long traces often
                                         contain many signal changes and the first divergence does               1 Code and benchmark artifacts are available at github.com/EEdigits.
helper logic used to verify the RTL design; we refer to it here-    longer produces a meaningful hardware variant), or T IME -
after simply as the harness. The framework then profiles RTL        OUT /I NCONCLUSIVE. These per-mutant outcomes and aggre-
structure once, selects a solver backend, and emits the proof       gate audit results form the audit evidence returned to the
configuration used in subsequent audit runs. MGR injects            refinement stage. Surviving mutants are fed back to the LLM
synthetic RTL faults and checks whether the current assertions      to strengthen the next harness round. I NVALID mutants are
detect them under that fixed configuration. Surviving mutants       excluded from the denominator of ρeff because they do not
trigger harness refinement. Once the assertion set kills the        exercise the harness.
relevant mutants at an acceptable rate, the final proof outcome
                                                                    B. Architecture-Aware Solver Selection
is recorded; if the proof fails, the resulting counterexample
is translated into a short root-cause narrative. The front-end         To reduce runtime unpredictability, we profile each design
harness stage is included for completeness, but the technical       before translation into solver-specific forms. We compute a
contributions begin after that point: MGR, solver selection,        lightweight structural score:
and CNS. In the present experiments, the initial harness is                                                    DR
                                                                                     χ = (DA × W ) + DM +         ,           (2)
generated with RTL context because the study starts from                                                       IC
existing public RTL designs and treats harness generation as        where W is dominant datapath width, DA is arithmetic
a bootstrap step rather than a contribution under evaluation.       density, DM is mux density, DR is total memory size in bits,
Most of the quality-control loop is tool-driven: the mutation       and IC is index complexity. The terms are normalized to a
audit and kill-rate computation in MGR, together with RTL           common reference scale and combined as a weighted sum for
profiling and solver selection, are deterministic stages, while     the final solver decision, preventing the memory term from
LLM calls are used only for harness construction/refinement         dominating on small designs. Intuitively, high DM indicates
and for natural-language failure summaries.                         control-steering logic, high DA × W indicates wide datapaths,
                                                                    and high DR /IC indicates memory-sensitive behavior. Unlike
A. Mutation-Guided Refinement
                                                                    prior selectors that operate on SMT formulas or lowered Btor2
   The goal of MGR is to test the test [14]. Starting from          tasks [7], [8], our selector works directly on RTL structure.
the original RTL D and the current assertion set A, the             This lets the flow choose a backend before building the full
framework injects faults into D and checks whether A still          proof instance, using signals that hardware engineers can
passes. Any passing mutant reveals a weakness in the harness;       understand and sanity-check.
the survived mutant is then fed back to the LLM for the
next refinement round. Vacuity is one failure mode of weak          C. Causal Narrative Synthesis
assertions, but MGR addresses a broader problem: whether               When verification fails, the framework extracts the failing
the current harness is sufficiently discriminative under injected   property, a compact slice of the trace, and the most relevant
faulty behaviors. Satisfiability checks may be used to detect       signal transitions, then prompts the LLM to produce a concise
strict vacuity, while MGR strengthens properties that still pass    explanation of the trigger condition and violated expectation.
but fail to distinguish relevant mutants.                           Counterexample explanation is not a new problem in formal
   Unlike prior mutation-based quality checks for generated         verification; prior work has studied causality-based methods
properties [10], [11], MGR uses mutant outcomes to decide           for highlighting why a trace violates a specification [15],
whether the harness should be accepted, refined again, or inter-    and industrial studies show that explanation quality directly
preted (cautiously) when a surviving mutant does not produce        affects whether engineers can make effective use of formal
an observable failure within the explored proof window. For         verification results [16]. Our focus here is different: CNS is
a mutant set M , we define the effective kill rate as:              evaluated as a faithfulness problem rather than a fluency prob-
                                                                    lem, so the explanation should point to the right cycle, the right
                              #Killed
                 ρeff =                     .                (1)    signals, and the right failure mechanism without introducing
                          #Total − #Invalid
                                                                    claims that are not supported by the trace. This makes CNS
In the current workflow, we set the refinement trigger to           a measurable debugging aid rather than a presentation-only
T = 85%: if the effective kill rate falls below this value,         add-on. In the current workflow, the model is guided by the
another refinement round is started. This threshold is a practi-    failing step and trace-based failure cues so that the explanation
cal floor rather than a final quality target; in our experiments,   remains tied to the actual counterexample.
robust harnesses typically converged to 90–100% effective kill
                                                                                  III. E XPERIMENTAL E VALUATION
on non-invalid mutants. If the effective kill rate remains low,
surviving mutants are fed back to the LLM for strengthening,        A. Setup
turning formal verification into an adversarial refinement loop        The framework is implemented on top of a white-box
rather than a one-shot generation task.                             Yosys/SymbiYosys flow [13]. An orchestration layer extracts
      MGR workflow: Each mutant is verified independently           structural metrics, selects a solver, and emits the SymbiYosys
under the same harness and proof configuration. Results             configuration automatically. In our current artifact, initial
are classified as K ILLED (assertions detect the mutant),           harness generation uses GPT 5.4 and CNS uses Claude Son-
S URVIVED (missed by the harness), I NVALID (the edit no            net 4.6 (Anthropic). Each MGR campaign uses 20 mutants per
                                                                                                  RTL source


                                                                                   II
                                               structural metrics             SMT Solver
                                                                               Selection
                                                                               (run once)
                                                                                                                                                                                                        Verification    CEX
                                properties
                                                                                                                                                                                                         Harness RTL    Trace

                                                                                     solver cfg


                                                           verification
                                         I                  harness                                                   III                                                                                      IV
                                                                                SMT                                                                   Kill rate     Yes          Proof      fail
   Spec.         RTL                  Initial                                                                  Mutation-Guided                                                                           Causal Narrative
                                                                               Backend                                                                 ≥T ?                     result?
                                     Harness                                                                     Refinement                                                                                Synthesis

                                                                                                                                                                                     pass


                                                                                                                                                                                 RTL                          Failure
                                                                                                                                                                                Verified                      Report
                                                                                                                                                No
                                             survived mutants + audit evidence


Fig. 1. The proposed quality-aware verification loop. The initial harness stage is shown only as a bootstrap. Solver selection is computed once from RTL
structure and reused during mutation-guided refinement. The paper’s technical contributions begin with solver selection and continue through mutation-guided
refinement and concise failure narratives.

                            TABLE I                                                                                                                     TABLE II
           B ENCHMARK CLASSES AND VERIFICATION DEPTHS .                                                                                  B EST MGR ROUND PER DESIGN (‘R’ = ROUND ).

                   Class          Design                                  k                                    Design                          Best    Eff. Kill      Observation
                   Protocol       I2C Master     80                                                            UART RX                         R1       90.0%         delay-only survivors
                   Protocol       UART (Full)   120                                                            UART Full                       R1       90.0%         delay-only survivors
                   Memory         Sync. FIFO     15                                                            UP8                             R1       100.0%        instruction-level checks
                   Memory         SDRAM Ctrl    500                                                            SHA3                            R1       100.0%        fully specified datapath behavior
                   Data           FFT 256        80                                                            SDRAM                           R4       36.8%         no new kills after timing edits
                   Data           SHA3           80                                                            VGA                             R2       90.0%         one-round refinement gain
                   Peripheral     VGA LCD       80                                                             FFT                             R2        93.8%        one residual inactive-branch edit
                   Control        uP8 (ADD/ISA) 45
                                                                                                                                                                          100
                                                                                                                                         100
round. We evaluate MGR on seven RTL designs: UART RX,                                                                                                                                              90

UART Full, UP8, SHA3, SDRAM, VGA, and FFT. Fig. 2                                                                                        80
                                                                                                                                                                          90
                                                                                                                         Kill Rate (%)




shows three supplementary learning curves: UART TX, I2C,                                                                                              70
and VGA. For solver selection, we use Yices, Bitwuzla, Z3,                                                                               60

and CVC5 as representative SMT backends [17]–[20]. We                                                                                    40                               35

profile each design and report average step latency (ASL),                                                                                            25                                       UART TX

                                                                                                                                         20                                                    I2C
                                Ttotal                                                                                                                10
                                                                                                                                                                                               VGA
                            ASL =      ,                   (3)
                                  k                                                                                                       0
                                                                                                                                                       1                  2                        3
where Ttotal is wall-clock proof runtime and k is the bounded                                                                                                     Refinement Round
depth [21]. Table I lists the benchmark classes and chosen
depths.                                                                                                        Fig. 2. Illustrative MGR refinement trajectories for UART TX, I2C, and
                                                                                                               VGA; Table II gives the cross-design summary.
B. Mutation-Guided Refinement Results
                                                                                                               preprocessor branches, and timing-setting edits whose effect
   Table II summarizes the best achieved MGR round across                                                      does not appear within the number of cycles explored by the
seven completed campaigns. The overall pattern is strong and                                                   proof. This distinction matters because a low plateau is not
consistent: six designs finish between 90% and 100% effective                                                  automatically evidence of a weak harness. In practice, MGR is
kill rate. UP8 and SHA3 reach 100% in their first round.                                                       most useful when it shows which survivors come from weak
UART RX, UART Full, and VGA stop at 90%, and FFT                                                               assertions and which come from mutations that the formal
reaches 93.8%. SDRAM is the only clear outlier. Its final score                                                setup cannot observe.
remains lower because some mutations change timing-related
internal behavior, but within the bounded number of cycles                                                     C. Solver Selection Results
(explored by the proof) they do not produce any observable                                                        Table III reports solver performance across the current
failure, so the mutant survives even though the harness may                                                    benchmark suite. The pattern is consistent with the proposed
not actually be weak. In other words, additional refinement                                                    selector: control-heavy designs with small widths, such as
stopped yielding new kills. We refer to that point as a plateau.                                               I2C, VGA, and uP8, favor Yices, while the wide datapath
   Across the suite, the most important cross-design pattern is                                                benchmark SHA3 favors Bitwuzla. The table also shows why
the emergence of source-level edits that change the RTL text                                                   backend choice cannot be treated as a default setting. Cases
but not what the formal tool can observe. We refer to these                                                    like FFT256, SHA3, and VGA, timeout under Z3 despite
as true equivalents. Three categories recur repeatedly: delay                                                  completing on other backends. The selector is therefore not
annotations that disappear in RTL-level checking, inactive                                                     chasing only small runtime gains; it is avoiding bad choices
                         TABLE III                                                            TABLE V
N ORMALIZED SOLVER PERFORMANCE (ASL IN S / STEP ); T/O = TIMEOUT.              CNS FAITHFULNESS ACROSS PROMPT SETTINGS .

        Benchmark      Bitwuzla CVC5          Z3      Yices          Metric                 R1 baseline    R2 refined    R2 + hints
        I2C Master         0.125       5.913 0.713 0.038             Correct cycle              4/8            6/6           8/8
        UART (Full)        0.008        T/O  0.017 0.008             Correct signal             8/8            6/6           8/8
        Sync. FIFO         2.733        T/O 27.733 6.800             Correct mechanism          5/8            6/6           8/8
        SDRAM Ctrl         0.026        T/O  0.290 0.024             Unsupported claims          0              0             0
        FFT 256            1.338      15.975 T/O 0.613               Overall faithful           3/8           ≥6/8           8/8
        SHA3               0.250       9.413  T/O 0.500
        VGA LCD            0.388       8.725  T/O 0.150             when the trace supports a more specific class. The refined
        uP8 (ADD)          3.556      44.000 0.156 0.044            prompt addresses both issues by stating the assertion-failure
        uP8 (ISA)          0.667        T/O 18.756 0.556
                                                                    step explicitly and by giving clearer descriptions for each
                            TABLE IV                                failure class. All six cases evaluated without case-specific hints
  S OLVER - SELECTION BASELINE SUMMARY ON THE CURRENT SUITE .       are then faithful. The remaining two require extra hints, so
     Policy                  Mean ASL       Relative to Yices       the conservative claim is that refined CNS reaches at least
                                                                    75% faithfulness with the shared prompt, rising to 100% with
     Always Bitwuzla               1.010           1.04×
     Always Yices                  0.970           1.00×            additional hints. Across all settings, signal identification is
     Rule-based selector           0.491           0.51×            correct and no unsupported signal names are introduced. After
     Oracle best                   0.491           0.51×            refinement, CNS explanations remain short while preserving
                                                                    the key debug facts: responsible signal, failure type, and why
that turn a solvable proof into a timeout. The memory-heavy         the assertion fires.
uP8(ISA) case provides a useful calibration point: although its
structure suggests an array-friendly backend (like Z3), Yices                   IV. D ISCUSSION AND C ONCLUSION
still wins at the tested proof bound. This shows that memory           The results suggest that the central problem in LLM-
density alone is not enough to choose the solver, and that the      assisted FV is not property generation alone, but quality-
selector must capture such hardware-specific tradeoffs.             aware closure. MGR is the strongest component: it directly
   To make the selector easier to interpret, Table IV compares      addresses false confidence from weak properties, and six of
our rule-based policy against fixed-solver baselines. “Always       seven designs reach 90–100% effective kill rate. The SDRAM
Yices” and “Always Bitwuzla” mean that the same solver is           plateau illustrates an important structural limit: some timing-
used for every benchmark. “Oracle” is the unattainable upper        oriented mutations do not produce an observable failure within
bound that always picks the fastest solver after seeing the         feasible proof depths, so they cannot be killed regardless
result. On the current benchmark suite, the rule-based selector     of harness quality. Recognizing that limit is itself a useful
matches the oracle solver choice on every benchmark and             outcome of MGR. The solver selector provides a lightweight
reduces mean ASL by roughly 49% compared with always                hardware-level rule for choosing the proof backend. CNS
using Yices.                                                        demonstrates that a zero-shot LLM reliably identifies the
                                                                    correct signals without hallucination, and a targeted two-part
D. Causal Narrative Results
                                                                    prompt refinement lifts overall faithfulness from 37% to at
   We evaluated CNS on eight failed counterexamples drawn           least 75%. Coverage remains an important metric in AI-for-
from four designs (FFT, VGA, UART RX, and SHA3). For                FV research, but this paper focuses on a narrower and more
each case, the ground truth consists of the manually estab-         defensible notion of quality: adversarial coverage through
lished failing cycle, key signals, and failure mechanism. This      MGR, runtime stability through solver selection, and trace
ground truth was written before any CNS run and then verified       faithfulness through CNS. Taken together, the results support a
in a second blind evaluation pass. Table V compares three set-      simple message: LLM-generated assertions become materially
tings: R1 baseline is the original zero-shot prompt, R2 refined     more trustworthy when they are mutation-tested, structurally
is the shared improved prompt evaluated on six cases without        profiled, and paired with an open verification stack. Future
case-specific hints, and R2 + hints adds such hints for the         work will add explicit coverage-closure metrics, compare the
two hardest cases. The four binary scoring criteria answer the      structural score (χ) against additional solver-selection base-
four basic debug questions: when (correct failing cycle), where     lines, and extend the CNS evaluation to counterexamples from
(correct key signal), what kind (correct mechanism class), and      live regressions rather than mutation-triggered failures alone.
honest (zero unsupported signal claims). A response is faithful
only when all four hold.                                                                  ACKNOWLEDGMENT
   Even in the baseline, CNS identifies the correct signals in        The authors acknowledge UK Research and Innovation
all eight cases and never invents signal names. Its errors are      (UKRI) via its Engineering and Physical Sciences Research
mainly about when and how: in longer traces, the baseline           Council (EPSRC) funding for the AI Hub for Productive Re-
sometimes reports the first cycle where signals begin to            search and Innovation in Electronics (APRIL), grant number
diverge rather than the step at which the assertion fails, and      EP/Y029763/1.Also, EDINA and ISG@University of Edin-
it sometimes assigns a broad label such as “timing error”           burgh for AI services.
                               R EFERENCES                                                2023, Proceedings, Part II, ser. Lecture Notes in Computer Science,
                                                                                          C. Enea and A. Lal, Eds., vol. 13965. Springer, 2023, pp. 3–17.
 [1] M. Li, W. Fang, Q. Zhang, and Z. Xie, “Specllm: Exploring                       [19] L. de Moura and N. Bjørner, “Z3: An efficient SMT solver,” in Tools
     generation and review of VLSI design specification with large language               and Algorithms for the Construction and Analysis of Systems, TACAS
     model,” CoRR, vol. abs/2401.13266, 2024. [Online]. Available:                        2008, ser. Lecture Notes in Computer Science, C. R. Ramakrishnan and
     https://doi.org/10.48550/arXiv.2401.13266                                            J. Rehof, Eds., vol. 4963. Springer, 2008, pp. 337–340.
 [2] Z. Yan, W. Fang, M. Li, M. Li, S. Liu, Z. Xie, and H. Zhang,                    [20] H. Barbosa, C. W. Barrett, M. Brain, G. Kremer, H. Lachnitt, M. Mann,
     “Assertllm: Generating hardware verification assertions from design                  A. Mohamed, M. Mohamed, A. Niemetz, A. Nötzli, A. Ozdemir,
     specifications via multi-llms,” in Proceedings of the 30th Asia and South            M. Preiner, A. Reynolds, Y. Sheng, C. Tinelli, and Y. Zohar, “cvc5: A
     Pacific Design Automation Conference, ASPDAC 2025, Tokyo, Japan,                     versatile and industrial-strength SMT solver,” in Tools and Algorithms
     January 20-23, 2025, Y. Nakamura and Y. Wang, Eds. ACM, 2025, pp.                    for the Construction and Analysis of Systems - 28th International Con-
     614–621. [Online]. Available: https://doi.org/10.1145/3658617.3697756                ference, TACAS 2022, Held as Part of ETAPS 2022, Munich, Germany,
 [3] Y. Bai, G. B. Hamad, S. Suhaib, and H. Ren, “Assertionforge:                         April 2–7, 2022, Proceedings, Part I, ser. Lecture Notes in Computer
     Enhancing formal verification assertion generation with structured                   Science, D. Fisman and G. Roşu, Eds., vol. 13243. Springer, 2022, pp.
     representation of specifications and RTL,” CoRR, vol. abs/2503.19174,                415–442.
     2025. [Online]. Available: https://doi.org/10.48550/arXiv.2503.19174            [21] A. Biere, A. Cimatti, E. M. Clarke, and Y. Zhu, “Symbolic model
                                                                                          checking without BDDs,” in Tools and Algorithms for the Construction
 [4] M. Abdollahi, M. Dargahi, M. Rashidian, M. Shalan, and R. Karri,
                                                                                          and Analysis of Systems (TACAS), ser. Lecture Notes in Computer
     “Hardware design and verification with large language models: A
                                                                                          Science, vol. 1579. Springer, 1999, pp. 193–207.
     literature survey, challenges, and open issues,” Electronics, vol. 14, no. 2,
     p. 265, 2025.
 [5] D. N. Gadde, K. K. Radhakrishna, V. N. Viswambharan, A. Kumar,
     D. Lettnin, W. Kunz, and S. Simon, “Hey AI, generate me a hardware
     code! agentic AI-based hardware design & verification,” in Proceedings
     of the 38th SBC/SBMicro/IEEE Symposium on Integrated Circuits and
     Systems Design (SBCCI), 2025.
 [6] I. Beer, S. Ben-David, C. Eisner, and Y. Rodeh, “Efficient detection
     of vacuity in temporal model checking,” in Proceedings of the 12th
     International Conference on Computer Aided Verification (CAV), ser.
     LNCS, vol. 1855. Springer, 2001.
 [7] J. Scott, A. Niemetz, M. Preiner, S. Nejati, and V. Ganesh, “Machsmt:
     A machine learning-based algorithm selector for SMT solvers,” in Tools
     and Algorithms for the Construction and Analysis of Systems, ser.
     Lecture Notes in Computer Science, J. F. Groote and K. G. Larsen,
     Eds., vol. 12652. Springer, 2021, pp. 303–325.
 [8] Z. Lu, P. Chien, N. Lee, A. Gurfinkel, and V. Ganesh, “Btor2-select:
     Machine learning based algorithm selection for hardware model check-
     ing,” in Computer Aided Verification, ser. Lecture Notes in Computer
     Science, vol. 15931. Springer, 2025.
 [9] F. Wu, E. Pan, R. Kande, M. Quinn, A. Tyagi, D. K. Houngninou,
     J. Rajendran, and J. Hu, “Spec2assertion: Automatic pre-RTL asser-
     tion generation by LLMs with progressive regularization,” CoRR, vol.
     abs/2505.07995, 2025.
[10] Y. Wang, J. Zhou, H. Lyu, Z. Chao, T. Wang, and H. Li, “Deepassert:
     An LLM-aided verification framework with fine-grained assertion gen-
     eration for modules with extracted module specifications,” CoRR, vol.
     abs/2509.14668, 2025.
[11] M. Hassan, S. Ahmadi-Pour, K. Qayyum, C. K. Jha, and R. Drechsler,
     “LLM-guided formal verification coupled with mutation testing,” in
     Proceedings of the Design, Automation and Test in Europe Conference
     (DATE), 2024, pp. 1–2.
[12] A. Kumar, D. N. Gadde, K. K. Radhakrishna, and D. Lettnin, “Saarthi:
     The first AI formal verification engineer,” CoRR, vol. abs/2409.06766,
     2024.
[13] C. Wolf, J. Glaser, and J. Kepler, “Yosys-a free verilog synthesis suite,”
     in Proceedings of the 21st Austrian Workshop on Microelectronics
     (Austrochip), vol. 97, 2013, pp. 1–6.
[14] Y. Jia and M. Harman, “An analysis and survey of the development of
     mutation testing,” IEEE Transactions on Software Engineering, vol. 37,
     no. 5, pp. 649–678, 2011.
[15] I. Beer, S. Ben-David, H. Chockler, A. Orni, and R. Trefler, “Explaining
     counterexamples using causality,” in Computer Aided Verification, ser.
     Lecture Notes in Computer Science, vol. 6174. Springer, 2010, pp.
     94–108.
[16] A. P. Kaleeswaran, A. Nordmann, T. Vogel, and L. Grunske, “A user
     study for evaluation of formal verification results and their explanation
     at bosch,” Empirical Software Engineering, vol. 28, no. 125, 2023.
[17] B. Dutertre, “Yices 2.2,” in Computer Aided Verification - 26th Inter-
     national Conference, CAV 2014, Held as Part of the Vienna Summer of
     Logic, VSL 2014, Vienna, Austria, July 18–22, 2014. Proceedings, ser.
     Lecture Notes in Computer Science, A. Biere and R. Bloem, Eds., vol.
     8559. Springer, 2014, pp. 737–744.
[18] A. Niemetz and M. Preiner, “Bitwuzla,” in Computer Aided Verification
     - 35th International Conference, CAV 2023, Paris, France, July 17–22,
