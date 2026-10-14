                                                Enhancing Program Repair with Specification
                                                Guidance and Intermediate Behavioral Signals
                                                            Minh Le-Anh*                            Cuong Chi Le*                            Tien N. Nguyen
                                                    FPT Software AI Center                   University of Texas at Dallas            University of Texas at Dallas
                                                 Hanoi Univ. of Science and Tech.                    Texas, USA                                Texas, USA
                                                        Hanoi, Vietnam                          cuong.le@utdallas.edu                  tien.n.nguyen@utdallas.edu
                                                        minhla4@fpt.com



                                           Abstract—Automated Program Repair (APR) has recently              broadly grouped into the following categories. First, one-
                                        benefited from large language models (LLMs). However, most           shot prompting with validation workflows can help LLMs
arXiv:2604.11770v2 [cs.SE] 5 Jul 2026




                                        LLM-based APR approaches still rely primarily on coarse-             outperform traditional APR systems [14], [15], [16]. This line
                                        grained, end-to-end signals from test-suite outcomes or speci-
                                        fication checks on the candidate fix to guide repair, providing      of approaches relies mainly on the APR capability of LLMs.
                                        limited insight into where a program’s internal logic deviates       Second, recent approaches further enhance repair through
                                        from its intended behavior. In contrast, human debugging             context retrieval augmentation (e.g., RAP-Gen [17]). Third,
                                        often relies on intermediate reasoning about program states          iterative repair strategies formulate APR as an iterative process
                                        through localized correctness conditions or assertions. Inspired     that selectively refines promising candidate trajectories with
                                        by this observation, we propose SpecTune, a specification-guided
                                        debugging framework that incorporates intermediate behavioral        different types of feedback (e.g., ChatRepair [15], REx [18]).
                                        reasoning into APR. SpecTune decomposes the repair task into         Fourth, advanced approaches enhance repair through multi-
                                        suspicious regions connected by execution checkpoints and derives    agent frameworks (e.g., AutoCodeRover [19], RepairAgent [20],
                                        localized postconditions representing expected program behaviors     AgentCoder [21]) that iteratively localize faults and refine
                                        at those points. By executing the buggy program and evaluating       patches using external tools (e.g., compilation and testing).
                                        these postconditions, SpecTune produces micro-level debugging
                                        signals that indicate mismatches between observed and intended          Despite these advances, existing APR approaches still
                                        behaviors, enabling more precise fault localization and targeted     rely primarily on macro-level debugging signals: they eval-
                                        patch generation. To address the potential unreliability of          uate candidate repairs based on final outcomes, such as
                                        LLM-generated postconditions, we introduce two complementary         test-suite pass/fail results [18]. Other approaches ex-
                                        signals: a specification validation signal α, which estimates the    plore specification signals in different forms. For example,
                                        consistency of generated postconditions using partial passing test
                                        cases, and a discriminative signal β, which detects violations of    SpecRover [22] uses natural-language specifications to guide
                                        validated postconditions during execution. With these signals,       and vet patches in AutoCodeRover [19] agentic APR frame-
                                        SpecTune safely leverages automatically generated specifications     work, while nl2postcond [23] studies the generation of formal
                                        for APR. Experimental results show that SpecTune improves fault      postconditions from natural-language intent. However, these
                                        localization and APR effectiveness than the baselines.               signals are typically method-level or candidate-level, rather than
                                                                 I. I NTRODUCTION                            checkpoint-level behavioral signals inside the buggy execution.
                                                                                                                While effective, such signals are coarse-grained. A failing
                                           Automated Program Repair (APR) has evolved through
                                                                                                             test or a failing check with a specification indicates that the can-
                                        several methodological paradigms. Early work largely followed
                                                                                                             didate’s output/logic is incorrect, but it often provides limited
                                        the generate-and-validate paradigm, where candidate patches
                                                                                                             fine-grained information about where the program’s internal
                                        are enumerated and validated against a test suite serving as the
                                                                                                             state first deviates from the intended behavior. Consequently,
                                        oracle. Search-based approaches [1], [2] explored syntactic edits
                                                                                                             the APR process frequently degenerates into a large search
                                        via evolutionary mutation, while template-driven and learning-
                                                                                                             over candidate edits guided only by coarse-grained signals.
                                        guided systems [3], [4] constrained or ranked candidate patches
                                                                                                                This reliance on macro signals does not reflect how de-
                                        using repair templates and properties of human-written fixes.
                                                                                                             velopers debug programs. Human debugging often proceeds
                                        Subsequently, semantic and pattern-based approaches [5], [6],
                                                                                                             by decomposing the computation into smaller parts and
                                        [7], [8], [9] improved repair by leveraging symbolic execution,
                                                                                                             reasoning about intermediate program states at checkpoints.
                                        constraint solving, execution traces, and recurring fix patterns.
                                                                                                             Developers form hypotheses about what the program should
                                        Later, deep learning approaches [10], [11], [12], [13] reframed
                                                                                                             satisfy at certain checkpoints and validate these hypotheses
                                        repair as translation from buggy to fixed code, learning repair
                                                                                                             through intermediate checks. When the observed behavior
                                        patterns directly from bug-fixing datasets.
                                                                                                             violates such expectations, the developer can narrow the fault
                                           The advances of large language models (LLMs) has trans-
                                                                                                             scope and modify the responsible code region. In essence,
                                        formed APR. Modern LLM-based APR approaches can be
                                                                                                             human debugging is often guided by intermediate behavioral
                                          * Equal Contribution                                               specifications rather than only by end-to-end pass/fail outcome.
This suggests a new direction for APR: leveraging intermediate
specifications as structured debugging signals.
   We propose SpecTune, a specification-guided debugging
framework for APR that incorporates intermediate behavioral
reasoning into the APR process. In a single-pass setting, it
aims to make an LLM more effective than the same LLM used
alone. In an iterative repair setting, the goal is to improve
an iterative refinement framework (without SpecTune), by
providing intermediate behavioral guidance. We also aim for
it to improve a file-level, agentic APR framework. These
comparisons isolate whether SpecTune adds value to the
same repair model or iterative framework. We do not target
repo-level, multi-agent APR systems, since they introduce
                                                                  Fig. 1: A developer derives debugging‘ signals from program semantics. Step
additional confounding factors, including context retrieval, tool 1: Read the problem description to understand the intended behavior. Step 2:
use, planning, test generation, build setup, and patch ranking, Inspect relevant code regions and reason about expected variable relationships
making it difficult to attribute improvements to SpecTune.        and formulate hypotheses as postconditions. Step 4: Evaluate the postconditions
                                                                  in execution to reveal mismatches between actual and intended behavior.
   Given a buggy program and its problem description, the
target LLM is prompted to decompose the repair task into sus-
picious regions separated by intermediate checkpoints. For each                                II. M OTIVATION
checkpoint, it is prompted to derive a localized postcondition
that captures the expected program behavior at that point. The       Fig. 1 illustrates an example. Firstly, the intended program
buggy program is then executed via the given test cases and       behavior     is given in the problem description (4 1). Given the
these postconditions are evaluated against the observed program   buggy    code    in the bottom left corner of Figure 1, a developer
states. When a specification is violated, the resulting mismatch  will  identify     one or more critical code regions and reason
indicates that the program logic near that checkpoint may be      about    the   expected    relations between intermediate variables
faulty. These mismatch signals provide structured guidance for    during    execution     (4   2, 4 3). For example, in Fig. 1, once
fault localization (FL) and targeted fix generation.              the  developer      understands     that the task is to reconstruct the
   The first key challenge is that these LLM-generated post-      array   original      from   the  XOR      array derived and count the
conditions are not always reliable. In our work, we in-           number      of  ‘1’s,  they  inspect    the  current code. In particular,
tentionally keep the generation strategy simple and focus         Region     1  corresponds     to the  reconstruction      step that attempts
on controlling specification quality after generation. Second,    to  recover    the  original     array   from   the  derived    array, while
poorly placed checkpoints are usually not useful for repair as    Region    2   performs   the  counting    step that  computes     the number
they produce postconditions that are either inconsistent with     of  ‘1’s  in  the  reconstructed    array.   Instead   of  attempting   repair
passing executions or not discriminative on failing executions.   the  entire   buggy   program    at once,   (s)he  typically   validates each
Thus, our tool validates and filters generated specifications     code    region.    For  example,     (s)he  could    form   a  hypothesis    at
before using them via two complementary signals. The first        the  end   of   Region   1  (j4).    From    the  perspective    of  a model,
is a specification validation signal α, which addresses the a formulation of such hypothesis could be expressed as an
potential unreliability of LLM-generated postconditions. The executable postcondition that captures the expected program
α signal is computed using partial passing test cases obtained state after Region 1 (j5). In our example, the postcondition
from executing the original program and estimates whether is whether the reconstructed array original satisfies the XOR
a generated postcondition is consistent with the intended relationship with the derived array:
behavior supported by available evidence. The second is a ∀i ∈ [0, n − 1], derived[i] = original[i] ⊕ original[(i + 1) mod n]
micro-level discriminative signal β, which estimates how often
a postcondition remains satisfied on failing executions; lower However, when implementing the reconstruction logic, the
β indicates a stronger ability to expose behavioral mismatches. original array is initialized with zeros. During the iterative
This paper makes the following contributions:                     reconstruction process, the elements of the original array
   (1) SpecTune, a specification-guided APR framework that are expected to be computed sequentially, where each newly
decomposes APR into checkpoint-based reasoning steps and reconstructed value depends on previously computed elements.
leverages intermediate postconditions to guide repair.            In particular, when reconstructing the array, the value of
   (2) We introduce checkpoint-level postcondition violations original[i+1] should be derived from the already computed
as micro-level debugging signals for guiding LLM-based APR. element original[i]. However, the buggy code in Figure 1
   (3) We design a dual-signal filtering algorithm that uses α instead uses original[i+1] when updating original[i],
to remove unreliable postconditions and β to remove weak or which introduces a forward dependency on a value that has
non-discriminative postconditions.                                not yet been correctly derived. This leads to the bug.
   (4) Empirical evaluation, showing that SpecTune can enhance       The actual/observed behavior of the buggy program is
APR performance over the state-of-the-art approaches.             given through the passing/failing test cases, while the intended
behavior is formulated as a postcondition at each checkpoint. This acts as a validation to quantify the correctness of ge-
The mismatch between the two behaviors at a checkpoint nerated postconditions based on their consistency with the
indicates that the logic leading to that checkpoint might be program behavior during the executions of passing test cases.
faulty. Overall, decomposing a buggy program into suspicious         For each generated postcondition p, we also design a
functional regions and validating each region with dedicated discriminative signal β, a type of micro-level signal that
postconditions can help a human or an LLM significantly assesses the quality of the generated postcondition p on its
narrow the search space for bug localization and repair. By ability to distinguish incorrect behavior (in failing test cases)
focusing on localized behavioral constraints, developers can from the intended behavior (via p). The postconditions with
reason about the correctness of individual regions. Importantly, high discriminative signals β are treated as potential indicators
from the mismatch, the developer could fix the buggy code.        of faulty logic and used as contextual guidance for the LLM in
                                                                  APR. In Fig. 1, the mismatch between the observed program
                         III. K EY I DEAS                         state at the end of Region 1 under failing test executions and the
                                                                  inferred postcondition 1 (right-hand side) constitutes a micro-
[Key Idea 1] Specification-guided debugging. In practice,
                                                                  level debugging signal. That is, β assesses the discriminative
developers typically decompose the overall problem and buggy
                                                                  characteristic (also referred to as completeness) of a generated
code into multiple smaller regions, progressively narrowing
                                                                  postcondition. It also helps remove the ‘weak’ postcondition
down the search space to localize and fix bugs. Each region
                                                                  (e.g., ‘true == true’) that cannot detect a bug.
is then validated using local unit checks, such as assertions
or intermediate correctness conditions. When a violation is                           IV. S PEC T UNE A PPROACH
observed, developers fix the corresponding code region to
restore the expected behavior.                                    A. Problem Formulation
   ,→ Inspired by this debugging strategy, we propose SpecTune,      We formulate the specification-driven APR problem as fol-
a specification-guided debugging framework that decomposes lows. Given a buggy program C, a description, and a test suite
the repair problem into a sequence of suspicious regions sep- T = {t1 , t2 , . . . , tn }, where each test case ti = (xi , yi ) consists
arated by intermediate checkpoints. For a checkpoint, it of an input xi and its expected output yi produced by the
derives a postcondition that aligns with the intended program canonical program C ∗ . By executing the buggy program C on
behavior mentioned in the problem description. By executing each test case in T , we partition the test suite into two subsets:
the program and evaluating these specifications, it aims to the passing test cases P = { ti ∈ T | C(xi ) = yi } and the
identify mismatches between the observed program behavior failing ones F = { tj ∈ T | C(xj ) ̸= yj }. Our objective is to
and the intended specifications. These mismatch signals provide generate a set of postconditions S that are both consistent with
structured guidance for localizing faults and generating fixes. and complete with respect to the intended program behavior I,
[Key Idea 2]. Micro Debugging Signals. Existing APR which is specified in the description. Ideally, we aim to find an
                                                                                             ∗
approaches primarily rely on coarse-grained debugging signals, optimal condition set S that maximizes completeness while
i.e., assess the repair candidates as a whole via test cases [15] satisfying a sufficiently high consistency requirement:
or checking them with natural-language specifications [22]. In
                                                                  S ∗ = arg maxS Completeness(S, I) s.t. Consistency(S, I) ≥ θ
contrast, the intrinsic logic of a program is typically validated
through finer-grained checks, such as intermediate assertions where Consistency(S, I) measures how well the postconditions
or localized correctness conditions. These micro-level tests S align with the intended behavior I, and Completeness(S, I)
verify whether individual functions or intermediate states of measures S’s discriminative ability to expose deviated behav-
the program satisfy specific logical properties.                  iors in incorrect mutated executions, rather than being trivial.
   ,→ To derive intermediate specifications, we leverage large       Directly measuring Consistency and Completeness is infea-
language models (LLMs) to infer postconditions at selected sible in practice, since both depend on the correct program C ∗
execution checkpoints. Given the problem description and the and its intermediate execution states, which are unavailable in
surrounding program context, an LLM generates the checkpoints APR. Thus, we introduce α-β algorithm that assesses the
and postconditions that capture the expected properties and quality of generated postconditions using only observable
relationships among the relevant variables. These postconditions executions of the buggy program. Specifically, the α signal
describe the intended program state after the execution to the leverages the passing test cases P to estimate whether a
corresponding code region. Prior work [23] has demonstrated generated postcondition is consistent with the intended behavior,
that LLMs can effectively synthesize postconditions and while the β signal leverages failing executions to estimate
assertions from textual descriptions or source code, making whether the postcondition is sufficiently discriminative.
them suitable for generating intermediate behavioral constraints.    Since SpecTune operates over a finite set (S’) of LLM-
[Key Idea 3] Specification Validation. Directly relying on these     generated candidate postconditions, it does not solve a global
specifications from LLMs may lead to incorrect localization          optimization problem. Instead, it realizes the objective through
due to their hallucinations/imprecision. To address this, we         threshold-based selection over (S’). The threshold on α serves
introduce a correctness validation signal α, computed from           as a reliability filter, removing postconditions that are not
the partial passing test cases gathered through running the code.    supported by passing executions. The threshold on β acts as
                                                                                                        Spec Selection

                  Problem
                 Description
                                                                                 Initial Specs S'                         Filtered Specs Ŝ
                                                 Spec Generation
                                                                                  #LINE 8:                                  #LINE 8:
                                                                                  assert ...                                assert ...
                                   Desired Program                                assert ...
                                                                                                         Consistency        assert ...

                                      Semantics                                   #LINE 12:                Signal α         #LINE 12:
                                                                                  assert ...                                assert ...
                                   In-scope program                               assert ...
                                                                                  assert ...
                                                                                                                            assert ...
                                                                                                                            assert ...
                                       variables           Spec Model                                                                        Repair Model
                                                                                  #LINE 19:                                 #LINE 19:
                                                                                  assert ...                                assert ...

                                                                                                        Discriminative
                                                                                                           Signal β

                Buggy Program
                                                          if ∀s∈S', Trivial(s)
                                                                                                          Passing
                                                                                                           Traces

                                                  Execute Tests                                           Failing
                                                                                                          Traces


Fig. 2: SpecTune framework starts with a buggy program, a test suite, and its problem description, from which candidate specifications are generated based
on program semantics and in-scope variables. These specifications are then validated using passing and failing test executions to compute the consistency (α)
and discriminative (β) signals, respectively. After filtering, the refined specification set Ŝ is used to guide the repair model in generating corrected programs.



a discriminative filter, removing postconditions that are too                                   {p1 , p2 , . . . , pm } and F = {f1 , f2 , . . . , fl } denote the sets
weak, incomplete, or uninformative for debugging.                                               of passing and failing test cases, respectively. Let Q =
   The refined specification set Ŝ is then used to guide the LLM.                              {q1 , q2 , . . . , qn } denote the set of checkpoints within the buggy
Let Mϕ denote a LLM parameterized by ϕ. The repair process                                      program proposed by LLMs. For each checkpoint qj , we
can be formulated as generating a candidate fixed program Ĉ                                    have an initial set of candidate LLM-generated postconditions
from the conditional distribution: Ĉ ∼ Mϕ (· | C, Ŝ), where Ŝ                                Sj′ = {sj1 , sj2 , . . . , sjk }. From these, we compute two signals
provides structured behavioral guidance that steers the model                                   α and β to assess the quality of candidate conditions:
toward repairs consistent with the intended program semantics.                                     Consistency Signal (α). For each candidate specification
                                                                                                sjk associated with checkpoint qj , we approximate its con-
B. SpecTune Workflow
                                                                                                sistency with the intended program behavior using the α
   SpecTune’s workflow is illustrated in Fig. 2. SpecTune                                       signal computed over the passing test cases. The consistency
takes as input a buggy program C, its functional description D,                                 signal α of a postcondition sjk is defined as the probability
a test suite T , together with the consistency and discriminative                               that the specification holds when a passing test reaches the
thresholds θ and γ. The output is the corrected program.                                        corresponding checkpoint:
   1) Checkpoints and Postcondition Generation: SpecTune
first prompts an LLM to construct candidate postconditions at                            |{ pi ∈ P | pi reaches qj ∧ xij |= sjk }|
                                                                               α(sjk ) =                                               (1)
multiple LLM-generated checkpoints. We leverage the capabil-                                    |{ pi ∈ P | pi reaches qj }|
ity of Code LLMs to analyze and reason over program logic to where xij denotes the program state observed when executing
identify a set of intermediate checkpoints Q = {q1 , q2 , . . . , qn } test case pi at checkpoint qj . Based on this signal, we filter out
within the buggy program. These checkpoints correspond to specifications with low α values, as they are likely inconsistent
critical execution points where the internal program state can with the intended program behavior. Specifically, we apply a
reveal potential logical inconsistencies. For each checkpoint qj , threshold θ ∈ [0, 1] and retain only the specifications whose
a set of candidate postconditions S ′ (qj ) = {sj0 , sj1 , . . . , sjk } consistency signals satisfy α(sjk ) ≥ θ.
is associated, where each specification is expected to hold im-            Discriminative Signal (β). Evaluating consistency alone is
mediately after execution reaches that checkpoint. To facilitate insufficient, as some LLM-generated postconditions may be
checkpoint and postcondition generation, we provide the LLM trivially satisfied and fail to capture erroneous behaviors due
with contextual information, including a failing input-output to a poorly placed checkpoint. Thus, we introduce the signal β
test case of the buggy program. Conditioned on this information, to assess whether a postcondition sjk can effectively identify
we obtain a set of candidate postconditions
                                        S for each checkpoint, incorrect executions using failing test cases:
forming the initial specifications S ′ = qj ∈Q S ′ (qj ). SpecTune
                                                                                         |{ fi ∈ F | fi reaches qj ∧ yij |= sjk }|
executes the code on both passing and failing tests and collects               β(sjk ) =                                               (2)
traces and program states at each checkpoint.                                                   |{ fi ∈ F | fi reaches qj }|
   2) Specification Validation: Although LLMs show promis- A higher β indicates that the postcondition is frequently
ing capability in proposing candidate specifications [23], it satisfied during the executions of failing test cases. This may
remains necessary to verify whether these generated post- arise either because the postcondition is incomplete and fails to
conditions are consistent with the intended behavior and capture the erroneous behavior, or because the failing execution
sufficiently informative for debugging. Concretely, let P = does not reach the program state where the logical mismatch
manifests. In contrast, postconditions with lower β signals if the current program is buggy to repairing the buggy program.
exhibit stronger discriminative capability, as they are more All baselines are attached to multiple repair backbones/settings,
likely to be violated by failing executions and give more allowing us to evaluate them under one-turn, iterative, and
informative signals for exposing incorrect program behaviors. agentic file-level repair frameworks/settings.
To remove incomplete or uninformative postconditions for APR,        Backbone Frameworks. We evaluate each repair signal under
we filter candidates using a threshold γ ∈ [0, 1] and retain only three backbone frameworks/settings. The first is the one-turn
those whose discriminative signals satisfy β(sjk ) < γ.           setting, where each method takes the buggy program and is al-
   3) Specification Selection: Overall, the postconditions lowed to produce one fixed program without iterative feedback.
satisfying both the consistency (αjk ≥ θ) and discriminative The second setting is ChatRepair [15], an iterative repair
(βjk < γ) criteria are added to the refined specification set framework that uses test outcomes from previous attempts as
Ŝ, while the others are discarded, ensuring that the resulting conversational feedback to improve later patches. The third
postconditions are both consistent with correct executions and setting is AgentCoder [21], an agentic repair framework in
capable of exposing erroneous behaviors.                          which multiple roles cooperate to generate and refine patches.
                                                                  Since ChatRepair uses a test-driven feedback as an APR signal,
         Ŝ = { sjk ∈ S ′ | α(sjk ) ≥ θ ∧ β(sjk ) < γ }       (3) we use it as a baseline and denote it by Tester.
Finally, the LLM repair model is prompted to generate a              Model Backbones. We use GPT-4o-mini and Qwen3-235B-
candidate fixed program Ĉ conditioned on the buggy program       A22B-Instruct-2507    for cost efficiency. We apply nucleus
C and the validated specification set Ŝ.                         sampling   and generate 5 candidate fixes per buggy problem.
                                                                     Datasets. Since SpecTune does not target repository-level
                  V. E MPIRICAL E VALUATION                       APR, we use file-level repair benchmarks. However, existing
   For evaluation, we seek to answer the following questions: file-level APR benchmarks may be exposed to modern LLMs,
   RQ1. [Program Repair Performance] What is SpecTune’s raising contamination concerns. We therefore collect recent
program repair performance across different settings?             problems from CodeForces (https://codeforces.com/), a compet-
   RQ2. [Fault Localization Capability] How does SpecTune itive programming platform with continuously updated tasks
compare with existing baselines in fault localization?            and executable tests, to build a newer and less likely con-
   RQ3. [Effectiveness of α-β Algorithm]. How effective is taminated file-level benchmark. Each repair instance consists
our algorithm in keeping the high-quality postconditions?         of a problem statement, a human-submitted buggy solution,
   RQ4. [Ablation Study] What is the individual contribution and the corresponding hidden-quality test suite. Each problem
of each signal in SpecTune?                                       is attached with a test suite ranging from 50 test cases to
   RQ5. [Sensitivity Analysis] How sensitive is the perfor- more than 200 test cases. We chose the buggy code with the
mance of SpecTune to the choices of the α and β thresholds? cyclomatic complexity of 8 or more and has at least 15 LOCs.
   Our evaluation is designed to isolate the contribution Finally, we obtained 180 buggy solutions across 90 problems.
of SpecTune under its intended scope. Since SpecTune pro-
vides intermediate behavioral guidance rather than a full                 VI. P ROGRAM R EPAIR P ERFORMANCE (RQ1)
repo-level repair workflow, we attach it to the same repair          1) Settings: Each buggy program is subjected to 5 indepen-
frameworks used by the state-of-the-art baselines. This allows dent repair attempts. In the one-turn setting, each attempt gen-
us to compare SpecTune with other specification feedback erates 5 candidate patches, from which the highest-performing
signals/baselines in one-turn LLM repair, iterative refinement one is selected as the final output. For iterative refinement
repair, and file-level agentic repair frameworks/settings while setting, we set the default maximum number of refinement
keeping the framework/setting fixed. We do not compare with iterations to 20 for each attempt. With SpecTune integrated
full repo-level multi-agent APR systems as end-to-end baselines, into them, the number of specification regeneration attempts is
since their performance depends on additional components such limited to 5 when trivial specifications are encountered.
as repository search, tool use, build setup, and patch ranking,      2) Metrics: We evaluate performance using Pass@k. This
making it difficult to attribute gains specifically to SpecTune. metric measures whether at least one of the top-k generated,
   Baselines. We compare SpecTune with two specification- fixed programs successfully passes the entire test suite.
guided APR baselines, SpecRover [22] and HoarePrompt [24].           3) Empirical Results: As seen in Table I, in the one-turn
SpecRover infers natural-language intent specifications to guide setting, SpecTune consistently improves over SpecRover and
patch generation and vet candidate patches in a repository-level HoarePrompt, improving Pass@1 5.0% and 7.1%, respectively
agent. Since SpecRover is designed for repo-level repair in with GPT-4o-mini and 25.0% and 1.2%, respectively with
AutoCodeRover, we adapt it to a file-level variant, by disabling Qwen3-235B. Moreover, when integrated into iterative refine-
its codebase search and navigation components, as SpecTune ment framework, SpecTune continues to deliver consistent
does not target repo-level bug fixing. HoarePrompt checks the improvements over Tester, SpecRover, and HoarePrompt 4.7%,
correctness of a program by prompting an LLM to reason about 3.2%, and 12.0%, respectively with GPT-4o-mini. With the
whether it satisfies natural-language Hoare-style specifications. integration to the AgentCoder agentic APR framework,
We adapt it to program repair by keeping its specification-based SpecTune improves over Tester, SpecRover, and HoarePrompt
reasoning procedure and changing the final query from checking 1.9%, 10.0%, and 22.5%, respectively with Qwen3-235B.
TABLE I: Program-repair performance across backbone frameworks, backbone models, and specification-guided repair methods. APR = Average Pass Rate. IT
= input tokens, OT = output tokens, and TT = total tokens.

   Backbone        Model                             Method                      Functional Repair Metrics                 Tokens (Millions)
                                                                           Pass@1      Pass@3      Pass@5      APR        IT       OT       TT
                                                     SpecRover              42.33       48.05        49.44     67.52     4.01     0.91      4.92
                   GPT-4o-mini                       HoarePrompt            40.22       52.78        57.78     64.52     1.04     0.52      1.56
                                                     SpecTune (Ours)        47.34       56.17        60.56     70.41     3.11     1.30      4.41
   One-turn
                                                     SpecRover              48.78       67.84        72.78     57.71     4.07     0.96      5.13
                   Qwen3-235B-A22B Instruct          HoarePrompt            72.56       82.61        87.78     79.59     1.12     0.68      1.80
                                                     SpecTune (Ours)        73.78       83.23        85.56     83.05     3.26     1.52      4.78
                                                     Tester                 50.33       50.84        51.11     82.99     12.89     5.51    17.40
                                                     SpecRover              51.78       52.50        52.78     82.21     21.76     6.43    28.19
                   GPT-4o-mini
                                                     HoarePrompt            43.01       43.45        43.89     79.01      8.57     6.12    14.69
                                                     SpecTune (Ours)        55.00       55.95        56.67     84.97     19.80    5.81     25.61
   ChatRepair
                                                     Tester                 86.89       87.84        88.84     96.01     10.57    13.42    24.09
                                                     SpecRover              81.67       83.78        84.45     93.12     22.84     7.41    30.25
                   Qwen3-235B-A22B Instruct
                                                     HoarePrompt            88.34       88.67        88.89     96.08      9.25     6.94    16.19
                                                     SpecTune (Ours)        91.56       91.67        91.67     97.59     21.02    5.61     26.63
                                                     Tester                 42.89       46.44        47.78     67.30     33.12    2.07     35.19
                                                     SpecRover              42.56       46.89        47.78     68.25     12.47    2.95     15.42
                   GPT-4o-mini
                                                     HoarePrompt            41.22       45.94        47.78     65.65     12.52    2.83     15.35
                                                     SpecTune (Ours)        45.56       49.01        50.00     67.98     17.16    3.98     21.14
   AgentCoder
                                                     Tester                 62.56       74.22        76.67     78.18     35.67    2.96     38.64
                                                     SpecRover              48.67       64.56        75.56     54.41     11.95    3.63     15.58
                   Qwen3-235B-A22B Instruct
                                                     HoarePrompt            42.00       69.56        80.00     43.56      9.51    5.93     15.44
                                                     SpecTune (Ours)        64.45       77.00        81.12     78.77     13.10    3.83     16.93



   4) Qualitative analysis: We found that our (α,β) algorithm               in ChatRepair and 21.14M/16.93M total tokens in AgentCoder
selects high-quality condition signals, helping code repair, better         under GPT-4o-mini/Qwen3-235B, respectively.
than natural-language specifications. Let us illustrate in Figs 3-             Overall, SpecTune introduces token usage comparable to
4. The executable condition at line 11 from SpecTune was                    existing specification-guided repair methods, while achieving
selected by our algorithm as α=1.0 (correctness) and β=0                    better functional quality across backbone frameworks.
(completeness), leading to SpecTune detecting the bug in that
branch. In contrast, HoarePrompt simply produced "This is                      VII. FAULT L OCALIZATION (FL) C APABILITY (RQ2)
printed: SEGMENT", which was not useful here. By using                         One of the key design goals of SpecTune (Key Idea 1) is to
feedback about trivial or unreliable specifications from previous           provide specification-guided signals that improve the reasoning
refinement turns, with the results of passing and failing tests, the        capability of LLMs, enabling them to more effectively narrow
model can generate better specifications in later turns. Moreover,          the search space and identify error-prone code regions, leading
the condition from SpecTune at line 7 has 30 passing tests, all             to better locating faulty lines. Thus, we compare the localization
30 satisfied, while none of the failing test cases went through.            performance of SpecRover and HoarePrompt using each of
That could signal the model that the error might be elsewhere.              the two backbone LLMs with that of SpecTune with the same
                                                                            model under one-turn setting. That also helps to explain the
   5) Token Usage Efficiency: We measure token usage by                     high APR performance of SpecTune as seen in RQ1.
the number of input tokens, output tokens, and total tokens                    1) Settings: Since the dataset does not include explicit
consumed when integrating specification-guided repair into                  ground-truth buggy locations, we evaluate fault localization
existing repair frameworks. Table I reports input tokens (IT),              using an LLM-as-a-judge paradigm. For each bug instance,
output tokens (OT), and total tokens (TT) in millions. Since                each approach under evaluation predicts suspicious line(s).
refinement-based and agentic frameworks involve iterative                   These predictions are then provided to a judge LLM, which
feedback and multiple repair attempts, their token usage is                 performs a pairwise comparison and returns a binary preference
naturally higher than the one-turn setting. In the one-turn                 indicating which prediction better captures the faulty line(s). For
setting, SpecTune uses 4.41M total tokens with GPT-4o-mini                  the judge model, to improve evaluation robustness and reduce
and 4.78M total tokens with Qwen3-235B. These numbers                       model-specific bias, we use GPT-5.2 and GPT-5.4, leveraging
are comparable to SpecRover, which uses 4.92M and 5.13M                     their strong reasoning capabilities across diverse code-related
total tokens, while being higher than HoarePrompt, which                    tasks. To further ensure the reliability of the evaluation, we
uses 1.56M and 1.80M total tokens. For iterative and agentic                retain only the subset of instances where all judge models are
frameworks, SpecTune also maintains competitive token usage                 able to produce a correct repair, indicating their capability to
compared with the baselines, using 25.61M/26.63M total tokens               accurately reason about the underlying bug. In addition, we also
1  # SpecTune                                                                               1  # HOAREPROMPT
2  a,b,c,d=map(int,input().split())                                                         2  # State of the program right berfore the function call:
 3 o=max(a,b,c,d)                                                                                   stdin contains one input: four space-separated
 4 # assert o == max(a, b, c, d), ensuring the maximum is                                           positive integers, each not exceeding 100, ...
        correctly identified                                                                 3 a, b, c, d = map(int, input().split())
 5 # assert o >= a and o >= b and o >= c and o >= d                                          4 o = max(a,b,c,d)
 6 if (a>=b and a>=c and a<b+c) or (a>=b and a>=d and a<b+d)                                 5 if (a >=b and a >= c and a <b+c or a>=b and a>=d and
        or (a>=d and a>=c and a<c+d) or (b>=a and b>=c and                                          a<b+d or a>=d and a>=c and a<c+d or b>=a and b>=c and
        b<a+c) or (b>=a and b>=d and b<a+d) or (b>=c and                                            b<a+c or b>=a and b>=d and b<a+d or b>=c and b>=d and
        b>=d and b<c+d) or (c>=a and c>=d and c<a+d) or                                             b<c+d or c>=a and c>=d and c<a+d or c>=a and c>=b and
        (c>=a and c>=b and c<a+b) or (c>=b and c>=d and                                             c<a+b or c>=b and c>=d and c<b+d or d>=a and d>=b and
        c<b+d) or (d>=a and d>=b and d<a+b) or (d>=a and                                            d<a+b or d>=a and d>=c and d<a+c or d>=c and d >= b
        d>=c and d<a+c) or (d>=c and d>=b and d<c+b):                                               and d<c+b):
 7    # assert any( p + q > r for (p,q,r) in [ sorted(t) for                                 6    print(’TRIANGLE’)
           t in [(a,b,c), (a,b,d), (a,c,d), (b,c,d)] ] )                                     7    #This is printed: TRIANGLE
 8    print(’TRIANGLE’)                                                                      8 elif (2*o <a+b+c+d) :
 9 elif 2*o<a+b+c+d:                                                                         9      print(’SEGMENT’)
10    # assert not any( p + q > r for (p,q,r) in [ sorted(t)                                10      #This is printed: SEGMENT
           for t in [(a,b,c), (a,b,d), (a,c,d), (b,c,d)] ] )                                11 else :
11    # assert any( p + q == r for (p,q,r) in [ sorted(t)                                   12      print(’IMPOSSIBLE’)
           for t in [(a,b,c), (a,b,d), (a,c,d), (b,c,d)] ] )                                13      #This is printed: IMPOSSIBLE
12    print(’SEGMENT’)                                                                      14      #State: a, b, c, d are positive integers not
13 else:                                                                                                 exceeding 100, representing the lengths of four
14    # assert not any( p + q > r for (p,q,r) in [ sorted(t)                                             sticks, and o is the maximum value among a, b,
           for t in [(a,b,c), (a,b,d), (a,c,d), (b,c,d)] ] )                                             c, and d. It is guaranteed that no triplet of
15    # assert not any( p + q == r for (p,q,r) in [                                                      sticks can form a triangle, meaning for every
           sorted(t) for t in [(a,b,c), (a,b,d), (a,c,d),                                                triplet where one stick is the longest,...
           (b,c,d)] ] )                                                                     15 # Overall this is what the function does: The function
16    print(’IMPOSSIBLE’)                                                                           reads four space-separated positive integers ...
                                             ‘                                                                                       ‘
    Fig. 3: Output from SpecTune: the condition at line 11 was selected by                      Fig. 4: Output from HoarePrompt [24]: The bug at line 9 with that branch
    α-β algorithm: α=1.0 (18 satisfies, 18 reaches, 67 passing tests), β=0.0 (0                 was not detected by HoarePrompt as its generated condition at line 11: "This
    satisfies, 7 reaches, 16 failing tests). It helps detect the (line 9) in that branch.       is printed: SEGMENT", which is not executable by test cases.



manually inspect a sampled subset of the localization results for          When using GPT-5.2 as the judge, SpecTune first shows
human evaluation. To assess the consistency between human substantial improvements over the naive baseline, winning in
judgments and LLM-based judgments, we report their inter- 107 cases (89.91%) under GPT-4o-mini and 114 cases (95.79%)
                                                                o −pe
rater agreement using Cohen’s κ (for two raters): κ = p1−p         e
                                                                      , under Qwen3-235B. Compared with stronger natural-language
where po denotes the observed agreement between the two specification baselines, SpecTune achieves 58 cases (48.73%)
raters, and pe denotes the expected agreement by chance.                and 59 cases (49.58%) where its predictions are preferred over
   2) LLM-judge Metrics: Let D denote the set of bug instances SpecRover and HoarePrompt, respectively, under GPT-4o-mini.
where both a baseline (SpecRover or HoarePrompt) and A similar trend is observed for Qwen3-235B, where SpecTune
SpecTune produce valid localization predictions. For each is preferred in 47 cases (39.50%) and 48 cases (40.34%) over
instance i ∈ D, let si and ni denote the sets of predicted SpecRover and HoarePrompt, respectively.
faulty lines from SpecTune and the base LLM. We employ                     When using GPT-5.4 as the judge, SpecTune remains
an LLM-based judge function Judge(si , ni ), which takes                consistently  preferred over the baselines. Against the naive
two sets of predicted lines as input and returns a binary               baseline, SpecTune    wins in 102 cases (85.72%) under GPT-
outcome: 0 if si is preferred over ni , and 1 otherwise.                4o-mini  and  113  cases (94.95%) under Qwen3-235B. Under
We define the following metrics: WinRate(SpecTune) =                    GPT-4o-mini,    SpecTune    further wins over SpecRover and
|{i∈D|Judge(si ,ni )=0}|
                         , WinRate(Base)=    |{i∈D|Judge(si ,ni )=1}|
                                                                      , HoarePrompt    in 57  cases  (47.90%) and 52 cases (43.71%),
          |D|                                         |D|
                                                                        respectively. Under  Qwen3-235B,    SpecTune is preferred in 39
DrawRate = |{i∈D|s    |D|
                         i =ni }|
                                  , where WinRate(SpecTune) mea- cases (32.78%) and 38 cases (31.93%) over SpecRover and
sures the proportion of instances where the judge prefers HoarePrompt, respectively. Under GPT-5.4 as the judge, the
the result from SpecTune, while WinRate(Base) captures the results remain consistent. That is, SpecTune yields a higher
opposite cases. DrawRate corresponds to instances where both proportion of preferred outcomes than the baselines, regardless
methods predict identical sets of buggy lines.                          of the underlying model or judge.
   3) Empirical Results: We conduct the experiment on 119                  4) Qualitative Analysis: SpecTune provides a fine-grained
tasks on our dataset for GPT-4o-mini and Qwen3-235B, where view of where the buggy program begins to diverge from
violated specifications are successfully generated by the base- the intended behavior. The signal comes from two sources:
lines under the condition α ≥ 0.9 and β < 1. Table II presents whether an execution reaches a checkpoint, and whether the
the overall impact of the generated postconditions on fault corresponding postcondition is satisfied when it is reached.
localization. Overall, SpecTune consistently outperforms the If passing and failing executions share earlier checkpoints
baselines across all settings, demonstrating that the generated but the failing execution first violates a later postcondition,
postconditions, guided by the estimated α and β signals, are the suspicious region can be narrowed to the code segment
effective in improving localization quality.                            leading to that checkpoint. If a failing execution fails to reach
TABLE II: Pairwise fault-localization comparison between SpecTune and
natural-language specification baselines.

Judge     Comparison                    SpecTune Baseline Draws
                         GPT-4o-mini
GPT-5.2   SpecTune vs Naive          89.91          4.21      5.88
GPT-5.2   SpecTune vs HoarePrompt    49.58          29.42     21.00
GPT-5.2   SpecTune vs SpecRover      48.73          31.09     20.18
GPT-5.4   SpecTune vs Naive          85.72          8.40      5.88
GPT-5.4   SpecTune vs HoarePrompt    43.71          35.29     21.00
GPT-5.4   SpecTune vs SpecRover      47.90          31.92     20.18
                  Qwen3-235B-A22B Instruct                                                                                         ‘
GPT-5.2   SpecTune vs Naive        95.79            3.36      0.85      Fig. 5: Distribution of ∆α = α − α∗ across all postconditions from GPT-4o-
GPT-5.2   SpecTune vs HoarePrompt  40.34            17.65     42.01     mini (yellow) and Qwen3-235B (blue).
GPT-5.2   SpecTune vs SpecRover    39.50            22.69     37.81
GPT-5.4   SpecTune vs Naive        94.95            4.20      0.85
GPT-5.4   SpecTune vs HoarePrompt  31.93            26.06     42.01
GPT-5.4   SpecTune vs SpecRover    32.78            29.41     37.81     algorithm removes inconsistent or uninformative postconditions,
                                                                        retaining the high-quality specifications for APR.
                                    ‘
                                                                        A. Reliability of the α Consistency Estimate
TABLE III: Agreement between human annotators and LLM judges measured
by Cohen’s κ.                                                              1) Settings: SpecTune generates checkpoint-level postcondi-
        Metric      Human vs GPT-5.2      Human vs GPT-5.4              tions from the buggy code and the problem description. These
        Cohen’s κ        0.629***              0.731***                 postconditions are intended to represent hypotheses about the
        *** p < 0.001                                                   expected program state, analogous to how a developer reasons
                                                                        about intermediate behavior during debugging. To evaluate
                                                                        whether our estimated consistency signal α is reliable, we need
a checkpoint that is normally reached by passing executions,            access to the corresponding fixed program and a mapping from
the signal suggests that the bug may occur elsewhere in the             checkpoints in the buggy program to locations in the fixed
control flow. In Fig. 3, the assertion on line 7 has 30 passing         program. Because our main dataset does not provide human-
tests going through; all 30 were satisfied, yet no failing test         written fixes, we use HumanEvalFix [25], which contains
cases reached it. This helps the model look elsewhere. In our           168 coding problems and provides buggy/fixed program pairs.
experiments, these dynamic checkpoint-level signals help the            However, HumanEvalFix contains only 7.25 test cases per
model reason more precisely about program states.                       problem on average, which is insufficient for reliably estimating
   5) Human Evaluation: To further assess the reliability of            postcondition consistency. Therefore, we use GPT-4.1-mini to
LLM-as-a-judge, we conduct a human study on a randomly                  generate additional inputs aimed at increasing branch coverage.
sampled subset of 30 bug instances. For each instance, human            We execute these inputs on the canonical solution to obtain
are asked to compare the localization outputs produced by the           additional test cases and merge them with the original tests.
baselines and SpecTune, and determine which prediction better           Overall, each task has 102.38 test cases on average.
captures the faulty region. To quantify the agreement between              2) Procedure: Given a buggy program C, we run SpecTune
human judgments and LLM-based decisions, we compute                     to generate postconditions at multiple checkpoints and compute
Cohen’s κ between human annotations and each LLM judge.                 their estimated consistency signal α using only executions of
As seen in Table III, Cohen’s κ indicates substantial agreement         the buggy program, as done in the normal SpecTune workflow.
between humans and GPT-5.2 (κ=0.629) and GPT-5.4 (κ=                    We then map each checkpoint to its respective location in
0.731). This further confirms that the judgments produced by            the fixed program C∗ and execute C∗ on the tests. Based on
the LLM are largely consistent with human assessments.                  whether the same postconditions hold at the mapped check-
   6) Conclusion: These suggest that using specification-               points in C∗, we compute a reference consistency signal α∗ .
guided signals in SpecTune effectively helps narrow down                   By comparing α with α∗ , we evaluate how well the consis-
the search space for fault localization. This also reinforces the       tency signal estimated from the buggy program approximates
findings of RQ1 (Section VI) and Key Idea 1 (Section III).              the reference consistency measured on the fixed program. This
                                                                        experiment focuses only on the reliability of the α estimate; the
    VIII. E FFECTIVENESS OF (α-β) A LGORITHM (RQ3)                      effectiveness of the full α-β algorithm in retaining high-quality
                                                                        postconditions is evaluated in Section VIII-B.
   α-β algorithm aims to retain high-quality LLM-generated                 3) Empirical Results: Fig. 6 presents the distribution of
conditions. This RQ evaluates it from two perspectives. First,          ∆α = α−α∗ across all generated postconditions for both back-
we assess whether the estimated consistency signal α, computed          bone models. In our evaluation, we consider a postcondition
from executions of the buggy program, reliably approximates             to be highly consistent with the reference signal if |∆α| < 0.1,
the consistency of the same postconditions on the fixed program.        meaning the estimated consistency signal deviates from the true
Second, we analyze how effectively the full α-β filtering               reference by less than 0.1. The plot reveals that the distribution
                                                                                                                          ‘
                                                                                    TABLE IV: Distribution of generated specification quality by GPT-4o-mini
                                                                                    across different threshold values θ and γ. Percentages indicate the proportion
                                                                                    of specifications in each region.

                                                                                         θ      γ    Non-Consist. (%) Trivial (%) Acceptable (%)
                                                                                       0.90 0.90            45.99                34.66           19.36
                                                                                       0.90 1.00            45.99                33.55           20.47
                                                                                       1.00 0.90            48.61                33.23           18.16
                                                                                       1.00 1.00            48.61                36.84           12.76

                                                                                         TABLE V: Effect of α and β signals on SpecTune performance.
                                                                     ‘              Setting                            Pass@1 Pass@3 Pass@5 APR
Fig. 6: Distribution of generated condition quality by GPT-4o-mini, estimated
using the α consistency signal (x-axis) and the β discriminative signal (y-axis).   Full SpecTune                        47.34       56.17      60.56     70.41
                                                                                    w/o Consistency Signal α             44.89       53.17      55.56     69.72
                                                                                    w/o Discriminative Signal β          45.67       53.78      57.23     69.57
                                                                                    w/o α and β signals                  44.11       52.34      55.56     69.49
is sharply concentrated around zero for both models: over
78.6% of postconditions generated by GPT-4o-mini and over
81.2% of those generated by Qwen3-235B are classified as
highly consistent. Furthermore, both models yield near-zero            Analysis: The results have two implications. First, we do not
mean and median errors: GPT-4o-mini achieves a mean ∆α              need many correct specifications for APR. While the overall
of 0.004 with a median of 0.000, while Qwen3-235B obtains           yield of acceptable specifications is low, this does not hinder the
a mean of -0.02 and a median of 0.000.                              effectiveness of SpecTune as one high-quality that can detect
                                                                    the fault is needed. From a human debugging perspective, a
   4) Analysis: These results show that α is a reliable estimator
                                                                    programmer does not attempt to generate as many specifications
of postcondition consistency. Despite relying only on executions
                                                                    as possible; instead, they brainstorm only a small subset of
of the buggy program, α closely approximates the reference
                                                                    specifications that capture the most suspicious or informative
consistency measured on the fixed code. This confirms Key
                                                                    program states at relevant checkpoints. This targeted reasoning
Idea 3: α provides a dependable validation signal for assessing
                                                                    is sufficient to localize and fix a bug. Second, the results also
and filtering LLM-generated postconditions.
                                                                    confirm our Key Ideas 2 and 3 on the need for a filtering
B. Distribution of Postcondition Quality                            mechanism to prevent low-quality specifications from being
                                                                    used in code repair. Our (α-β) algorithm ensures that only
   This section analyzes the quality distribution of the post-
                                                                    consistent and discriminative specifications are retained for
conditions generated by the LLM at multiple checkpoints.
                                                                    repair. As shown in the ablation study (Table V), removing the
Having established in Section VIII-A that the estimated signal
                                                                    (α-β) algorithm significantly degrades performance, as a large
α reliably approximates the consistency quality of generated
                                                                    number of inconsistent or trivial specifications are introduced
postconditions, we now apply SpecTune to the buggy programs
                                                                    into the repair process, misleading the fault localization and
in our dataset and compute the α and β values of the
                                                                    reducing the overall bug-fixing effectiveness.
generated checkpoint-level postconditions. We then categorize
each postcondition into one of three regions: the non-consistent
                                                                                      IX. A BLATION S TUDY (RQ4)
region if α(s) < θ; the trivial region if α(s) ≥ θ and
β(s) ≥ γ; and the acceptable region if α(s) ≥ θ and β(s) < γ.          This section examines the contribution of each signal α and
Each region reflects a different level of specification quality β. Specifically, we analyze how removing the consistency signal
with respect to consistency and the ability to detect incorrect α and the discriminative signal β affects its APR effectiveness.
behavior. This experiment is designed to characterize how often        1) Setting: We conduct an ablation study of under the one-
LLM-generated postconditions are usable for repair, and to turn setting when SpecTune integrated with the base LLMs
quantify the extent to which inconsistent or trivial specifications from RQ1 (Section VI) by systematically removing each
must be filtered out before they are used as debugging signals. component: (1) removing the consistency signal α (i.e., keeping
   Fig. 6 shows the distribution of generated specification all specifications that satisfy β<1 regardless of their consistency
quality by GPT-4o-mini, using θ = γ = 0.80. The trivial region with passing executions), (2) removing the discriminative
has the highest density at 36.09% and the non-consistent signal β (i.e., retaining all specifications that satisfy α ≥ 0.9
region accounts for 44.63%, indicating that the model often regardless of their ability to detect faulty behaviors), and (3)
generates specifications with little practical value. The plot removing both signals (i.e., using all generated specifications
also shows that specifications are highly concentrated around without any filtering). As both underlying models exhibit
(α, β) = (0, 0), corresponding to inconsistent cases, and (1, 1), consistent trends across all three RQs above, for brevity, we
corresponding to trivial ones. Only 19.28% of specifications evaluate each ablated variant on GPT-4o-mini only.
fall into the acceptable region. We present the density of each        2) Empirical Results: Table V shows that removing either
region across multiple threshold values in Table IV.                signal degrades performance across all metrics. Removing α
            TABLE VI: Sensitivity analysis on quality thresholds.
                                                                          reduce its impact, we use the same backbones and controlled
    α≥θ         β<γ        Pass@1      Pass@3       Pass@5          APR   settings when comparing baseline and augmented variants.
                  0.9       46.44        56.12       60.00      71.49
                                                                             External Validity. Results may not generalize to other
      0.9        0.95       45.78        56.12       57.78      69.69     languages, large systems, or domain bugs.
                  1.0       47.34        56.17       60.56      70.41        Construct Validity. Test-suite pass rates may not fully capture
                  0.9       44.67        54.16       57.89      68.35     correctness due to its incompleteness.
     0.95        0.95       45.44        51.56       55.00      69.28
                  1.0       45.78        54.45       58.66      70.08                         XII. R ELATED W ORK
                  0.9       45.00        53.89       58.89      68.61  In addition to classic APR [1], [26], [27], [28], [5], [29], [30],
      1.0        0.95       45.67        53.55       56.12          [9] and deep learning APR methods [11], [31], [32], [33], [34],
                                                                70.82
                  1.0       45.22        53.89       57.21          [35] (Section I), we focus on LLM-based APR approaches.
                                                                69.82
                                                                       Single-pass, non-iterative LLM-based APR. Recent ad-
                                                                    vances in LLMs have transformed APR by enabling powerful
alone drops Pass@1 by 2.45%, this suggests that without con- zero-shot and few-shot patch generation. Prior studies [16],
sistency filtering, inconsistent postconditions are passed to the [14] show that large pretrained models can generate plausible
repair process, misleading the Repair Model toward incorrect fixes when prompted with buggy code and context. A LPHA R E -
reasoning about the desired program behavior. Otherwise, PAIR [36] leverages large pretrained code models to generate
removing β alone results in a less drop (1.67%) in Pass@1, patches with infilling-style prediction, while R EPILOT [37]
showing that keeping high-quality specification is crucial. This integrates LLM-based code completion with patch validation.
suggests that introducing trivial postconditions into the repair       LLM-based APR with iterative refinement. C HAT R E -
process reduces the LLM’s ability to reason about the root PAIR [15] leverages conversational feedback to iteratively
cause of the bug. Finally, we removed both signals, meaning improve patches based on test results, while REx [18] for-
that all postconditions generated by the LLM are passed directly mulates repair as a budgeted search problem over candidate
into the repair process. The results show that this leads to the trajectories. Retrieval-augmented approaches such as RAP-
largest degradation, with a 3.23% drop in Pass@1.                   Gen [17] incorporate similar bug-fix exemplars into the prompt.
                                                                       Our experimental results show that SpecTune is able to
               X. S ENSITIVITY A NALYSIS (RQ5)                      improve the APR performance of the underlying LLMs in a
    This section aims to investigate the sensitivity of SpecTune single-pass and iterative repair settings.
to its key hyperparameters: the consistency signal α and the           Agentic APR frameworks. Multi-agent frameworks, e.g., AU -
discriminative signal β, with respect to its performance.           TO C ODE ROVER [19] and R EPAIR AGENT [20] treat APR as an
    1) Setting: To ensure both consistency with correct ex- autonomous workflow, where LLMs iteratively localize faults,
ecutions and correctness in identifying faults, we consider analyze context, and invoke tools such as compilation and
threshold ranges for the consistency and discriminative signals testing. We did not compare or add SpecTune to repository-
as θ, γ ∈ {0.9, 0.95, 1.0}, where specifications are retained if level, multi-agent APR systems, since they introduce extra
α ≥ θ and β < γ. Similar to RQ4 (Section IX), we perform confounding factors, including context retrieval, tool use,
this experiment using the SpecTune configuration integrated planning, test generation, build setup, and patch ranking,
with backbone LLMs, as established in RQ1 (Section VI) and making it difficult to attribute improvements to SpecTune.
report only the results for Qwen3-235B only.                           Specification generation and test synthesis. Learning tech-
    2) Empirical Results: Table VI presents the sensitivity of niques have been explored for generating program specifications
SpecTune to the thresholds θ and γ. Overall, SpecTune demon- and test artifacts, including postcondition inference [23],
strates robust and consistent performance across all evaluated [38], test oracle synthesis [39], [40], [41], test coverage
hyperparameter combinations, with all variants consistently improvement [42], [43], [44], and unit test generation [45],
outperforming configurations without specification filtering. In [46]. EvoSpex [47] infers input–output relations, while others
our study, the configuration (θ, γ) = (0.9, 1.0) yields the best generate property-based tests [48] or candidate properties [49].
overall results. From these observations, we notice that for           Machine learning has also been applied to infer specifi-
a fixed θ, increasing γ toward 1.0 - which means we only cations, such as program invariants [50], [51], [52], [53].
filter out postconditions that are completely trivial with β=1, SpecRover [22] is an intent/specification-inference approach
consistently yields equal or better performance. This indicates for improving the agentic APR framework AutoCodeRover.
that specifications with discriminative signal β ∈ [0.9, 1.0) still It iteratively infers natural-language specifications to guide
carry useful fault-localizing and APR information.                  patching, vet patches, and provide confidence/evidence. We
                                                                    have shown SpecTune performs better than SpecRover and
                  XI. T HREATS TO VALIDITY                          HoarePrompt. NL2Postcond [23] leverages LLMs to infer
    Internal Validity. SpecTune depends on LLM-generated postconditions from textual descriptions of code. We do not
postconditions, whose quality may suffer from hallucinations. compare with NL2Postcond because it targets a different setting.
We mitigate this threat through our (α-β) mechanism. Another It generates method-level postconditions either from natural-
threat is the nondeterminism of LLM-based generation; to language intent alone or from a correct/reference program. In
contrast, SpecTune takes a buggy program and its natural-                       [13] ——, “Dear: a novel deep learning-based approach for automated
language description as input and generates checkpoint-level                         program repair,” in Proceedings of the 44th International Conference on
                                                                                     Software Engineering, ser. ICSE ’22. New York, NY, USA: Association
postconditions at intermediate locations. Thus, NL2Postcond                          for Computing Machinery, 2022, p. 511–523. [Online]. Available:
does not directly match our input or repair-guidance setting.                        https://doi.org/10.1145/3510003.3510177
                                                                                [14] C. S. Xia, Y. Wei, and L. Zhang, “Automated program repair
                         XIII. C ONCLUSION                                           in the era of large pre-trained language models,” in Proceedings
                                                                                     of the 45th International Conference on Software Engineering, ser.
   This paper introduces SpecTune, a specification-guided                            ICSE ’23. IEEE Press, 2023, p. 1482–1494. [Online]. Available:
framework for improving code LLMs in APR. By leveraging                              https://doi.org/10.1109/ICSE48619.2023.00129
intermediate specifications and execution signals, SpecTune                     [15] C. S. Xia and L. Zhang, “Automated program repair via conversation:
                                                                                     Fixing 162 out of 337 bugs for $0.42 each using chatgpt,” in
improves single-pass repair and can enhance existing iterative                       Proceedings of the 33rd ACM SIGSOFT International Symposium on
APR frameworks. Our results show consistent repair gains,                            Software Testing and Analysis, ser. ISSTA 2024. New York, NY, USA:
improved fault localization, and more meaningful behavioral                          Association for Computing Machinery, 2024, p. 819–831. [Online].
                                                                                     Available: https://doi.org/10.1145/3650212.3680323
guidance, suggesting that specification-guided reasoning is a                   [16] Z. Fan, X. Gao, M. Mirchev, A. Roychoudhury, and S. H. Tan,
promising direction for reliable LLM-based APR.                                      “Automated repair of programs from large language models,” in
   Data Availability. All data and code are available at [54].                       Proceedings of the 45th International Conference on Software
                                                                                     Engineering, ser. ICSE ’23. IEEE Press, 2023, p. 1469–1481. [Online].
                                                                                     Available: https://doi.org/10.1109/ICSE48619.2023.00128
                             R EFERENCES                                        [17] W. Wang, Y. Wang, S. Joty, and S. C. Hoi, “Rap-gen: Retrieval-
 [1] W. Weimer, T. Nguyen, C. Le Goues, and S. Forrest, “Automatically find-         augmented patch generation with codet5 for automatic program
     ing patches using genetic programming,” in 2009 IEEE 31st International         repair,” in Proceedings of the 31st ACM Joint European Software
     Conference on Software Engineering, 2009, pp. 364–374.                          Engineering Conference and Symposium on the Foundations of Software
 [2] C. Le Goues, T. Nguyen, S. Forrest, and W. Weimer, “Genprog: A                  Engineering, ser. ESEC/FSE 2023. New York, NY, USA: Association
     generic method for automatic software repair,” IEEE Transactions on             for Computing Machinery, 2023, p. 146–158. [Online]. Available:
     Software Engineering, vol. 38, no. 1, pp. 54–72, Jan 2012.                      https://doi.org/10.1145/3611643.3616256
 [3] F. Long and M. Rinard, “Staged program repair with condition synthesis,”   [18] H. Tang, K. Hu, J. P. Zhou, S. C. Zhong, W.-L. Zheng, X. Si,
     in Proceedings of the 2015 10th Joint Meeting on Foundations of                 and K. Ellis, “Code repair with LLMs gives an exploration-
     Software Engineering, ser. ESEC/FSE 2015. New York, NY, USA:                    exploitation tradeoff,” in The Thirty-eighth Annual Conference on
     Association for Computing Machinery, 2015, p. 166–178. [Online].                Neural Information Processing Systems, 2024. [Online]. Available:
     Available: https://doi.org/10.1145/2786805.2786811                              https://openreview.net/forum?id=o863gX6DxA
 [4] ——, “Automatic patch generation by learning correct code,” SIGPLAN         [19] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury, “Autocoderover:
     Not., vol. 51, no. 1, p. 298–312, Jan. 2016. [Online]. Available:               Autonomous program improvement,” in Proceedings of the 33rd
     https://doi.org/10.1145/2914770.2837617                                         ACM SIGSOFT International Symposium on Software Testing and
 [5] H. D. T. Nguyen, D. Qi, A. Roychoudhury, and S. Chandra, “Semfix:               Analysis, ser. ISSTA 2024. New York, NY, USA: Association
     Program repair via semantic analysis,” in 2013 35th International               for Computing Machinery, 2024, p. 1592–1604. [Online]. Available:
     Conference on Software Engineering (ICSE), 2013, pp. 772–781.                   https://doi.org/10.1145/3650212.3680384
 [6] J. Xuan, M. Martinez, F. DeMarco, M. Clement, S. L. Marcote,               [20] I. Bouzenia, P. Devanbu, and M. Pradel, “Repairagent: An autonomous,
     T. Durieux, D. Le Berre, and M. Monperrus, “Nopol: Automatic                    llm-based agent for program repair,” in Proceedings of the
     repair of conditional statement bugs in java programs,” IEEE Trans.             IEEE/ACM 47th International Conference on Software Engineering,
     Softw. Eng., vol. 43, no. 1, p. 34–55, Jan. 2017. [Online]. Available:          ser. ICSE ’25. IEEE Press, 2025, p. 2188–2200. [Online]. Available:
     https://doi.org/10.1109/TSE.2016.2560811                                        https://doi.org/10.1109/ICSE55347.2025.00157
 [7] S. Mechtaev, J. Yi, and A. Roychoudhury, “Angelix: scalable multiline      [21] D. Huang, J. M. Zhang, M. Luck, Q. Bu, Y. Qing, and H. Cui,
     program patch synthesis via symbolic analysis,” in Proceedings of the           “Agentcoder: Multi-agent-based code generation with iterative testing and
     38th International Conference on Software Engineering, ser. ICSE ’16.           optimisation,” 2024. [Online]. Available: https://arxiv.org/abs/2312.13010
     New York, NY, USA: Association for Computing Machinery, 2016, p.           [22] H. Ruan, Y. Zhang, and A. Roychoudhury, “Specrover: Code
     691–701. [Online]. Available: https://doi.org/10.1145/2884781.2884807           intent extraction via llms,” in Proceedings of the IEEE/ACM
 [8] D. Kim, J. Nam, J. Song, and S. Kim, “Automatic patch generation learned        47th International Conference on Software Engineering, ser.
     from human-written patches,” in 2013 35th International Conference on           ICSE ’25. IEEE Press, 2025, p. 963–974. [Online]. Available:
     Software Engineering (ICSE), 2013, pp. 802–811.                                 https://doi.org/10.1109/ICSE55347.2025.00080
 [9] A. Koyuncu, K. Liu, T. F. Bissyandé, D. Kim, J. Klein, M. Monperrus,       [23] M. Endres, S. Fakhoury, S. Chakraborty, and S. K. Lahiri, “Can large
     and Y. Le Traon, “Fixminer: Mining relevant fix patterns for automated          language models transform natural language intent into formal method
     program repair,” Empirical Softw. Engg., vol. 25, no. 3, p. 1980–2024,          postconditions?” Proc. ACM Softw. Eng., vol. 1, no. FSE, Jul. 2024.
     May 2020. [Online]. Available: https://doi.org/10.1007/s10664-019-              [Online]. Available: https://doi.org/10.1145/3660791
     09780-z                                                                    [24] D. S. Bouras, Y. Dai, T. Wang, Y. Xiong, and S. Mechtaev, “HoarePrompt:
[10] Z. Chen, S. Kommrusch, M. Tufano, L.-N. Pouchet, D. Poshyvanyk, and             Structural reasoning about program correctness in natural language,” in
     M. Monperrus, “ SequenceR: Sequence-to-Sequence Learning for End-               Proceedings of the 48th IEEE/ACM International Conference on Software
     to-End Program Repair ,” IEEE Transactions on Software Engineering,             Engineering, ser. ICSE 2026, 2026.
     vol. 47, no. 09, pp. 1943–1959, Sep. 2021. [Online]. Available:            [25] N. Muennighoff, Q. Liu, A. Zebaze, Q. Zheng, B. Hui, T. Y. Zhuo,
     https://doi.ieeecomputersociety.org/10.1109/TSE.2019.2940179                    S. Singh, X. Tang, L. von Werra, and S. Longpre, “Octopack:
[11] T. Lutellier, H. V. Pham, L. Pang, Y. Li, M. Wei, and L. Tan, “Coconut:         Instruction tuning code large language models,” 2024. [Online].
     combining context-aware neural translation models using ensemble for            Available: https://arxiv.org/abs/2308.07124
     program repair,” in Proceedings of the 29th ACM SIGSOFT International      [26] A. Ghanbari, S. Benton, and L. Zhang, “Practical program repair
     Symposium on Software Testing and Analysis, ser. ISSTA 2020. New                via bytecode mutation,” in Proceedings of the 28th ACM SIGSOFT
     York, NY, USA: Association for Computing Machinery, 2020, p.                    International Symposium on Software Testing and Analysis, ser. ISSTA
     101–114. [Online]. Available: https://doi.org/10.1145/3395363.3397369           2019. New York, NY, USA: Association for Computing Machinery, 2019,
[12] Y. Li, S. Wang, and T. N. Nguyen, “Dlfix: context-based code                    p. 19–30. [Online]. Available: https://doi.org/10.1145/3293882.3330559
     transformation learning for automated program repair,” in Proceedings      [27] K. Liu, A. Koyuncu, D. Kim, and T. F. Bissyandé, “Tbar: revisiting
     of the ACM/IEEE 42nd International Conference on Software                       template-based automated program repair,” in Proceedings of the
     Engineering, ser. ICSE ’20. New York, NY, USA: Association                      28th ACM SIGSOFT International Symposium on Software Testing
     for Computing Machinery, 2020, p. 602–614. [Online]. Available:                 and Analysis, ser. ISSTA 2019. New York, NY, USA: Association
     https://doi.org/10.1145/3377811.3380345                                         for Computing Machinery, 2019, p. 31–42. [Online]. Available:
                                                                                     https://doi.org/10.1145/3293882.3330577
[28] K. Liu, A. Koyuncu, D. Kim, and T. F. Bissyandè, “Avatar: Fixing                Computing Machinery, 2022, p. 2130–2141. [Online]. Available:
     semantic bugs with fix patterns of static analysis violations,” in 2019         https://doi.org/10.1145/3510003.3510141
     IEEE 26th International Conference on Software Analysis, Evolution and     [40] A. Mastropaolo, N. Cooper, D. N. Palacio, S. Scalabrino, D. Poshyvanyk,
     Reengineering (SANER), 2019, pp. 1–12.                                          R. Oliveto, and G. Bavota, “Using transfer learning for code-related
[29] J. Hua, M. Zhang, K. Wang, and S. Khurshid, “Sketchfix: a tool for              tasks,” IEEE Transactions on Software Engineering, vol. 49, no. 4, pp.
     automated program repair approach using lazy candidate generation,”             1580–1598, 2023.
     in Proceedings of the 2018 26th ACM Joint Meeting on European              [41] M. Tufano, D. Drain, A. Svyatkovskiy, and N. Sundaresan, “Generating
     Software Engineering Conference and Symposium on the Foundations of             accurate assert statements for unit test cases using pretrained
     Software Engineering, ser. ESEC/FSE 2018. New York, NY, USA:                    transformers,” in Proceedings of the 3rd ACM/IEEE International
     Association for Computing Machinery, 2018, p. 888–891. [Online].                Conference on Automation of Software Test, ser. AST ’22. New York,
     Available: https://doi.org/10.1145/3236024.3264600                              NY, USA: Association for Computing Machinery, 2022, p. 54–64.
[30] L. Chen, Y. Pei, and C. A. Furia, “ Contract-Based                              [Online]. Available: https://doi.org/10.1145/3524481.3527220
     Program Repair Without The Contracts: An Extended Study                    [42] C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen, “Codamosa: Escaping
     ,” IEEE Transactions on Software Engineering, vol. 47,                          coverage plateaus in test generation with pre-trained large language
     no. 12, pp. 2841–2857, Dec. 2021. [Online]. Available:                          models,” in Proceedings of the 45th International Conference on
     https://doi.ieeecomputersociety.org/10.1109/TSE.2020.2970009                    Software Engineering, ser. ICSE ’23. IEEE Press, 2023, p. 919–931.
[31] N. Jiang, T. Lutellier, and L. Tan, “Cure: Code-aware neural machine            [Online]. Available: https://doi.org/10.1109/ICSE48619.2023.00085
     translation for automatic program repair,” in 2021 IEEE/ACM 43rd           [43] J. Altmayer Pizzorno and E. D. Berger, “Coverup: Effective high
     International Conference on Software Engineering (ICSE), 2021, pp.              coverage test generation for python,” Proc. ACM Softw. Eng., vol. 2, no.
     1161–1173.                                                                      FSE, Jun. 2025. [Online]. Available: https://doi.org/10.1145/3729398
[32] Q. Zhu, Z. Sun, Y.-a. Xiao, W. Zhang, K. Yuan, Y. Xiong, and               [44] C. C. Le, C. D. Van, T. D. Vu, M. V. T. Pham, H. N. Phan,
     L. Zhang, “A syntax-guided edit decoder for neural program repair,”             H. N. Phan, and T. N. Nguyen, “TestWeaver: Execution-aware,
     in Proceedings of the 29th ACM Joint Meeting on European Software               feedback-driven regression testing generation with large language
     Engineering Conference and Symposium on the Foundations of Software             models,” in Proceedings of the 48th IEEE/ACM International Conference
     Engineering, ser. ESEC/FSE 2021. New York, NY, USA: Association                 on Software Engineering (ICSE ’26), Rio de Janeiro, Brazil, Apr. 2026,
     for Computing Machinery, 2021, p. 341–353. [Online]. Available:                 to appear. [Online]. Available: https://arxiv.org/abs/2508.01255
     https://doi.org/10.1145/3468264.3468544                                    [45] S. K. Lahiri, S. Fakhoury, A. Naik, G. Sakkas, S. Chakraborty,
[33] H. Ye, M. Martinez, X. Luo, T. Zhang, and M. Monperrus, “Selfapr:               M. Musuvathi, P. Choudhury, C. von Veh, J. P. Inala, C. Wang, and J. Gao,
     Self-supervised program repair with test execution diagnostics,” in             “Interactive code generation via test-driven user-intent formalization,”
     Proceedings of the 37th IEEE/ACM International Conference on                    2023. [Online]. Available: https://arxiv.org/abs/2208.05950
     Automated Software Engineering, ser. ASE ’22. New York, NY,                [46] M. Tufano, D. Drain, A. Svyatkovskiy, S. K. Deng, and N. Sundaresan,
     USA: Association for Computing Machinery, 2023. [Online]. Available:            “Unit test case generation with transformers and focal context,” 2021.
     https://doi.org/10.1145/3551349.3556926                                         [Online]. Available: https://arxiv.org/abs/2009.05617
[34] Q. Zhu, Z. Sun, W. Zhang, Y. Xiong, and L. Zhang, “Tare:                   [47] F. Molina, P. Ponzio, N. Aguirre, and M. Frias, “Evospex: An
     Type-aware neural program repair,” in Proceedings of the 45th                   evolutionary algorithm for learning postconditions,” in Proceedings
     International Conference on Software Engineering, ser. ICSE                     of the 43rd International Conference on Software Engineering, ser.
     ’23.     IEEE Press, 2023, p. 1443–1445. [Online]. Available:                   ICSE ’21. IEEE Press, 2021, p. 1223–1235. [Online]. Available:
     https://doi.org/10.1109/ICSE48619.2023.00126                                    https://doi.org/10.1109/ICSE43902.2021.00112
[35] N. Jiang, T. Lutellier, Y. Lou, L. Tan, D. Goldwasser, and X. Zhang,       [48] V. Vikram, C. Lemieux, J. Sunshine, and R. Padhye, “Can large
     “Knod: Domain knowledge distilled tree decoder for automated program            language models write good property-based tests?” 2024. [Online].
     repair,” in 2023 IEEE/ACM 45th International Conference on Software             Available: https://arxiv.org/abs/2307.04346
     Engineering (ICSE), 2023, pp. 1251–1263.                                   [49] D. Key, W. Li, and K. Ellis, “I speak, you verify: Toward trustworthy
[36] C. S. Xia and L. Zhang, “Less training, more repairing please:                  neural program synthesis,” CoRR, vol. abs/2210.00848, 2022. [Online].
     revisiting automated program repair via zero-shot learning,” in                 Available: https://doi.org/10.48550/arXiv.2210.00848
     Proceedings of the 30th ACM Joint European Software Engineering            [50] P. Garg, D. Neider, P. Madhusudan, and D. Roth, “Learning invariants
     Conference and Symposium on the Foundations of Software Engineering,            using decision trees and implication counterexamples,” in Proceedings
     ser. ESEC/FSE 2022. New York, NY, USA: Association for                          of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles
     Computing Machinery, 2022, p. 959–971. [Online]. Available:                     of Programming Languages, ser. POPL ’16. New York, NY, USA:
     https://doi.org/10.1145/3540250.3549101                                         Association for Computing Machinery, 2016, p. 499–512. [Online].
[37] Y. Wei, C. S. Xia, and L. Zhang, “Copiloting the copilots: Fusing               Available: https://doi.org/10.1145/2837614.2837664
     large language models with completion engines for automated program        [51] L. Laich, P. Bielik, and M. Vechev, “Guiding program
     repair,” in Proceedings of the 31st ACM Joint European Software                 synthesis by learning to generate examples,” in International
     Engineering Conference and Symposium on the Foundations of Software             Conference on Learning Representations, 2020. [Online]. Available:
     Engineering, ser. ESEC/FSE 2023. New York, NY, USA: Association                 https://openreview.net/forum?id=BJl07ySKvS
     for Computing Machinery, 2023, p. 172–184. [Online]. Available:            [52] J. Yao, G. Ryan, J. Wong, S. Jana, and R. Gu, “Learning nonlinear
     https://doi.org/10.1145/3611643.3616271                                         loop invariants with gated continuous logic networks,” in Proceedings
[38] C. C. Le, M. V. Pham, T. D. Vu, V. D. Cuong, P. N. Huy, P. N.                   of the 41st ACM SIGPLAN Conference on Programming Language
     Hoang, and T. N. Nguyen, “SpecMind: Cognitively inspired, interactive           Design and Implementation, ser. PLDI 2020. New York, NY, USA:
     multi-turn framework for postcondition inference,” in Proceedings of the        Association for Computing Machinery, 2020, p. 106–120. [Online].
     64th Annual Meeting of the Association for Computational Linguistics            Available: https://doi.org/10.1145/3385412.3385986
     (Volume 1: Long Papers), M. Liakata, V. P. Moreira, J. Zhang, and          [53] K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can large
     D. Jurgens, Eds. San Diego, California, United States: Association              language models reason about program invariants?” in Proceedings
     for Computational Linguistics, Jul. 2026, pp. 36 409–36 424. [Online].          of the 40th International Conference on Machine Learning, ser.
     Available: https://aclanthology.org/2026.acl-long.1687/                         Proceedings of Machine Learning Research, A. Krause, E. Brunskill,
[39] E. Dinella, G. Ryan, T. Mytkowicz, and S. K. Lahiri, “Toga:                     K. Cho, B. Engelhardt, S. Sabato, and J. Scarlett, Eds., vol. 202.
     a neural method for test oracle generation,” in Proceedings                     PMLR, 23–29 Jul 2023, pp. 27 496–27 520. [Online]. Available:
     of the 44th International Conference on Software Engineering,                   https://proceedings.mlr.press/v202/pei23a.html
     ser. ICSE ’22.          New York, NY, USA: Association for                 [54] [Online]. Available: https://spectune.site
