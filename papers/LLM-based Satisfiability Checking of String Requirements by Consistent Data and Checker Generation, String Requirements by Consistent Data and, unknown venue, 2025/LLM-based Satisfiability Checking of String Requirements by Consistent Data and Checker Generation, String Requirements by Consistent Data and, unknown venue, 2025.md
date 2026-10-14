                                                        LLM-based Satisfiability Checking of
                                                    String Requirements by Consistent Data and
                                                              Checker Generation
                                              Boqi Chen*                   Aren A. Babikian*            Shuzhao Feng            Dániel Varró†         Gunter Mussbacher
                                                 ECE                   Dep’t of Computer Science             ECE                        IDA                     ECE
                                            McGill University            University of Toronto          McGill University      Linköping University       McGill University
                                            Montreal, Canada                Toronto, Canada             Montreal, Canada        Linköping, Sweden         Montreal, Canada
arXiv:2506.16639v1 [cs.SE] 19 Jun 2025




                                            Abstract—Requirements over strings, commonly represented               (e.g., through textual programs) but also for data manipulation.
                                         using natural language (NL), are particularly relevant for soft-          For instance, many systems manipulate strings in the form
                                         ware systems due to their heavy reliance on string data manip-            of an email address and a password given by the user as
                                         ulation. While individual requirements can usually be analyzed
                                         manually, verifying properties (e.g., satisfiability) over sets of        input. Additionally, strings must comply with well-formedness
                                         NL requirements is particularly challenging. Formal approaches            requirements (e.g., an email address must contain exactly one
                                         (e.g., SMT solvers) may efficiently verify such properties, but           “@” character), which are often numerous and interconnected.
                                         are known to have theoretical limitations. Additionally, the              Verifying the satisfiability of an individual requirement over
                                         translation of NL requirements into formal constraints typically          strings may be feasible via manual analysis. However, with an
                                         requires significant manual effort. Recently, large language mod-
                                         els (LLMs) have emerged as an alternative approach for formal             increasing number of requirements, common for large-scale
                                         reasoning tasks, but their effectiveness in verifying requirements        projects, verifying their satisfiability becomes a challenging
                                         over strings is less studied. In this paper, we introduce a hybrid        task, particularly considering that requirements may be con-
                                         approach that verifies the satisfiability of NL requirements over         tradictory or ambiguous. Such challenges have been studied
                                         strings by using LLMs (1) to derive a satisfiability outcome (and a       by existing work in the field of requirements engineering [1]–
                                         consistent string, if possible), and (2) to generate declarative (i.e.,
                                         SMT) and imperative (i.e., Python) checkers, used to validate the         [5]. In fact, inconsistency and ambiguity detection in (formal)
                                         correctness of (1). In our experiments, we assess the performance         requirements, even beyond strings, is an active subfield of
                                         of four LLMs. Results show that LLMs effectively translate                requirements engineering.
                                         natural language into checkers, even achieving perfect testing               Problem Statement. Existing approaches for satisfiability
                                         accuracy for Python-based checkers. These checkers substantially          checking of requirements over strings are often formal: they
                                         help LLMs in generating a consistent string and accurately
                                         identifying unsatisfiable requirements, leading to more than              rely on general-purpose SMT solvers, such as Z3 [6], or on
                                         doubled generation success rate and F1-score in certain cases             string-specific constraint solvers, such as Ostrich [7]. Such
                                         compared to baselines without generated checkers.                         approaches are sound and efficiently handle complex con-
                                            Index Terms—large language model, satisfiability checking for          straints over strings by either (1) detecting problems, i.e.,
                                         requirements, test data generation, constraint solving                    unsatisfiability, in input requirements or (2) generating con-
                                                                                                                   forming strings as proof of satisfiability, which is particularly
                                                                    I. I NTRODUCTION                               useful in the context of requirements-based testing. However,
                                            Motivation. Large-scale software systems commonly in-                  a major assumption of such approaches is to take a formal
                                         volve numerous parties, from domain experts to technical team             definition of requirements as input (e.g., using the SMT-LIB2
                                         members and end-users. For the successful development of                  syntax), which is often unavailable (and hard to create by
                                         such systems, it is necessary to ensure a smooth interaction              formal methods non-experts).
                                         between these parties, which becomes particularly challenging                Given that string requirements are mainly written in NL,
                                         when considering their varying levels of domain expertise and             NL-based approaches are better suited for their interpretation.
                                         technical knowledge. For this purpose, requirements are most              In recent years, large language models (LLMs) have emerged
                                         commonly captured using natural language (NL).                            as a promising alternative for NL interpretation in general,
                                            A particularity of software systems is their reliance on               with certain logic reasoning capabilities [8], particularly due to
                                         strings, not only for the implementation of software artifacts            their strong few-shot generalization capabilities in data-scarce
                                                                                                                   settings. However, existing research [9] has shown that the
                                           * Both authors contributed equally to the research.
                                                                                                                   effectiveness of using LLMs to verify the satisfiability of (NL)
                                           † Also affiliates with McGill University.
                                                                                                                   string requirements is below that of formal approaches. Still,
                                           Partially supported by the FRQNT-B2X project (file number: 319955),
                                         IT30340 Mitacs Accelerate, and the Wallenberg AI, Autonomous Systems      their inherent support for NL requirements, as well as their
                                         and Software Program (WASP), Sweden                                       capacity of generating realistic strings as proof of consistency,
remain significant assets vis-à-vis formal approaches.              need to manually formalize NL requirements. Additionally,
   A further drawback of LLM-based verification of require-          our comparative evaluation gives insights on the strengths and
ments satisfiability is the lack of soundness guarantees. To         weaknesses of various LLMs and checker types in providing
remedy this, existing LLM-based approaches [10]–[12] rely            correct verification outcomes for NL requirements.
on a trial-and-error method guarded by formal checks: LLM-
                                                                                            II. BACKGROUND
derived outcomes are formally checked for correctness at each
iteration and may only be returned if the check succeeds. On         A. Satisfiability checking of requirements over strings
the one hand, checking may be performed using (declarative)             This paper focuses on verifying the satisfiability of require-
SMT solvers, which have known theoretical limitations, e.g.,         ments (given as input) over strings by leveraging a consistent
supporting nested quantifiers, which do occur in problems over       string data and checker generation approach. To illustrate
strings. For instance, checking if a string is a palindrome is       this, let us consider, as an illustrating example, an extended
complex since it requires the solver to check that for each          version of the email address manipulation system introduced
character at position i of data d, there exists an identical char-   in Section I which has the following three requirements:
acter at position d.length − i. On the other hand, imperative          R1 The system shall require an email address to contain
methods such as Python programs may efficiently check that                  exactly one “@” character.
strings conform to complex requirements, with less theoretical         R2 The system shall require an email address not to end
limitations. However, they cannot be used to provide claims                 with a “.” character.
that the requirements are unsatisfiable.                               R3 The system shall require an email to contain at least one
   Contributions: We introduce a hybrid generative approach                 “.” character after the “@” character.
to verify the satisfiability of NL requirements over strings. Our       We illustrate the versatility of requirements satisfiability
approach uses LLMs (1) to derive a satisfiability outcome,           verification by considering the above system in a requirements-
and (2) to generate checkers used to ensure the correctness of       based testing context. Given requirements R1, R2, and R3, a
the satisfiability outcome derived in (1). Our approach gen-         test engineer first selects a set of test cases, represented as
erates two types of checkers: declarative checkers (i.e., SMT        conditions over the set of requirements. They then associate
specifications to verify unsatisfiability of requirement sets) and   an expected system behavior to each test case (e.g., the system
imperative checkers (i.e., Python programs, which can more           stores the email address if and only if the given input satisfies
generally check data when a requirement is satisfiable). The         all system requirements). An example containing five such test
specific contributions of the paper are as follows:                  cases is shown in Table I.
  • We propose a novel approach that takes as input a
                                                                     TABLE I: Test cases, their satisfiability, and corresponding test
    collection of NL requirements over strings and either
                                                                     data
    (1) detects unsatisfiable requirements or (2) generates a
    conforming string (instance) as a proof of satisfiability.                               Expected
                                                                            Test case                     Satisfiability     Test data
                                                                                             Behavior
    (Section III)                                                       R1 ∧ R2 ∧ R3        Store email       Yes           “ab@cd.com”
  • We integrate a divide-and-conquer approach for efficient           ¬R1 ∧ R2 ∧ R3        Show error        Yes          “ab@@cd.com”
    handling of complex collections of string requirements.            R1 ∧ ¬R2 ∧ R3        Show error        Yes             “ab@cd.”
                                                                       R1 ∧ R2 ∧ ¬R3        Show error        Yes           “ab@cdcom”
    As a novel intermediate step, our approach derives                 R1 ∧ ¬R2 ∧ ¬R3       Show error        No                 -
    checkers for verifying the satisfiability of individual NL
    requirements and leverages a formal solver within a                 Upon test case selection, as a first step, the engineer
    feedback loop to improve accuracy. (Section IV)                  must check whether the test case is satisfiable, which is
  • Our approach relies on checkers to examine the cor-
                                                                     a challenging task to perform manually, even for domain
    rectness of LLM-derived satisfiability outcomes. In the          experts. For instance, it is difficult to determine manually that
    case where no correct outcome is derived, our approach           a R1 ∧ ¬R2 ∧ ¬R3 test case is unsatisfiable, considering
    degrades gracefully by returning the closest-to-sound            that if an email containing exactly one “@” character (R1)
    outcome derived within the allocated budget. (Section V)         does not contain any “.” characters after the “@” (¬R3),
  • We conduct experiments with four popular LLMs, (i.e.,
                                                                     then it cannot end with a “.” (¬R2). While SMT solvers may
    GPT-4o [13], GPT-4o-mini [13], Llama3.1-8b [14], and             efficiently detect such an unsatisfiable case if the requirements
    DeepSeek-V3 [15]). We investigate 340 NL requirement             are formalized, a key advantage of our approach is to derive
    sets conforming to 12 categories of textual variables            SAT/UNSAT outcomes directly from NL requirements.
    drawn from common programming exercises in technical                Once the satisfiability is determined, for each satisfiable test,
    interviews. (Section VI)                                         the engineer must derive textual test data (i.e., a string) that
   Added Value: In contrast to approaches focused solely on          would trigger the expected behavior in the underlying system.
data generation, our approach provides accurate outcomes for         Deriving such data manually and ensuring its compliance with
both satisfiable and unsatisfiable (string) requirement sets. As     the test case specification is a daunting task, particularly with
a key improvement, this paper generates verification outcomes        an increasing number of requirements. Our approach generates
by taking as input only the NL requirements, i.e., without the       conformant test data automatically for each satisfiable test
case as a side-effect of the satisfiability verification, where                NL                  LLM            Verification
the generated test data is the proof of satisfiability.                    Requirements           Checker          Outcome
                                                                                                 generator         Checkers
B. Constraint satisfaction problems over strings
                                                                            Feedback
   Constraints over strings are common in the context of                          Verfication Outcome
commercial software applications, e.g., through password and                                                        Checker-
                                                                                                 UNKNOWN             based
email restrictions. They are also addressed significantly in                            SAT
                                                                             UNSAT                ~UNSAT             verifier
scientific research, through automated, string-specific formal
                                                                                        + data     ~SAT               LLM
reasoning techniques [7], [16]–[19] designed to solve collec-
tions of complex constraints. These approaches are evaluated
                                                                                       Fig. 1: Approach overview
over large benchmarks [20] and in the context of solver
competitions [21], where string constraints are represented
formally (e.g., in the SMT-LIB2 [22] format). In this context,      not-necessarily-sound approach (e.g., LLMs), as detailed in
the solvers are evaluated according to their achieved runtime       Section V. It then checks (validates) the correctness of the
and success rate.                                                   intermediate verification outcome wrt. the requirements. The
   While the constraint satisfaction problems contained in          checker generator component is described in Section IV.
these benchmarks are valuable from a logical perspective,              NL requirements and the generated checkers are then given
their relevance for real-world application domains such as          as input to the checker-based verifier, detailed in Section V,
requirements engineering has been less studied. Additionally,       which outputs a verification outcome for the conjunction of
solvers take as input a formal representation of the problem,       input NL requirements. When the requirements are determined
which is often unavailable upfront for most software systems.       to be satisfiable, the verifier returns SAT, as well as string data
C. Large language models (LLMs)                                     as a proof of satisfiability. When unsatisfiable NL requirements
                                                                    are detected, the verifier returns UNSAT and may pinpoint the
   LLMs are powerful transformer neural networks [23] trained       problematic subset of the NL requirements through a feedback
on vast amounts of data for handling various tasks involving        loop. Similar to existing heuristic-based search approaches
natural language. Recent research highlights LLMs’ emerg-           [29], a budget is imposed on the feedback loop to limit the
ing reasoning capabilities, achieving notable performance on        number of retries. If the verifier runs out of budget, it returns
many logic reasoning benchmarks [8]. This positions them            an UNKNOWN outcome. As a key particularity, our approach
as promising alternatives to traditional constraint solvers for     degrades gracefully when no sound SAT or UNSAT outcome
addressing constraint-solving problems involving text values.       may be provided: in this case, our approach returns the closest-
   Recent research has also focused improving LLM perfor-           to-sound outcome derived within the allocated budget.
mance by optimizing the input NL prompt, known as prompt
engineering [24]. Techniques such as leveraging emotional                              IV. C HECKER G ENERATOR
stimuli [25] and zero-shot chain-of-thought reasoning [26]             Figure 2 shows a detailed workflow of our proposed divide-
have been shown to be effective across various LLMs.                and-conquer Checker generator that takes as input a set of
   While LLMs typically produce natural language output,            NL requirements and derives a checker for each requirement
recent advancements such as Open AI’s structured outputs [27]       within that set.
and LangChain’s output parsers [28] have enabled them to               Types of checkers. In this paper, we consider two types of
produce structured output. In this paper, we rely on LangChain      checkers, namely declarative checkers based on SMT solvers
to instruct the LLM to present final answers in various             and imperative checkers based on Python scripts. On one hand,
structured formats depending on the components.                     a declarative checker is the formalization of the input NL
                                                                    requirement set into an SMT-solver-friendly (static) specifica-
                 III. A PPROACH OVERVIEW                            tion. This specification is fed to an SMT solver, which can
   An overview of our proposed satisfiability verification ap-      verify its satisfiability. Declarative checkers may also be used
proach for NL requirement is shown in Figure 1, where               to check the consistency of a generated string by integrating
the blue and orange boxes represent input, intermediate, and        the string value as a constraint within the checker specification.
output artifacts, while the red boxes represent processes. Our      On the other hand, an imperative checker consists of, for each
approach takes as input a conjunction of NL requirements such       requirement, a function where the requirement is formalised
as the ones introduced in Section II-A. Our approach outputs        using standard software language constructs. The function
a Verification Outcome vi ∈ {UNSAT, SAT, UNKNOWN} as-               takes as input a string and returns a boolean value indicating
sessing the satisfiability of the input requirements conjunction.   whether the string satisfies the requirement formalization.
   As a first step, our approach generates a Verification Out-         Requirements splitting. As an initial step, the checker
come Checker (checker) for each input NL requirement. A             generator splits the NL requirements into a set of requirement
checker is a process that takes as input (1) the NL require-        batches which will be converted into checkers as a contiguous
ments and (2) an intermediate UNSAT or SAT verification             unit. Splitting may be done arbitrarily, and will result in a
outcome for the requirements derived by an intermediate,            batching that lies between the following extremes (which we
assess in our evaluation): (1) complete split, which yields         this may be assessed via formal equivalence checks comparing
batches containing a single requirement, and (2) no split,          them to ground truth implementations, if available. When an
which considers the entire requirement set as a single batch.       individual NL requirement is satisfiable, semantic correctness,
   Such an input batching approach is widely used to enhance        for both declarative and imperative checkers, may be approx-
efficiency across various domains, including neural network         imated through testing, as proposed by existing research [31].
training and testing [30], as it often helps reduce neural          In this setting, valid- and invalid-labeled data is fed into the
network’s memory usage and/or training time. For our checker        checker and the derived checker outcome is compared to the
generation, batching reduces the number of LLM calls re-            ground-truth labeling.
quired to generate all checkers and may provide context when
requirements are inter-related. However, for this paper, we             V. C HECKER - BASED NL R EQUIREMENTS V ERIFIER
hypothesize that complete splitting reduces the complexity of          Figure 4 shows a detailed workflow of our proposed
checker generation despite an increased number of LLM calls.        checker-based NL requirements verifier component, which
We will demonstrate this in Section VI.                             takes as input the original NL requirements and the verification
   Requirements-to-checker conversion. Each batch of NL             outcome checkers derived in accordance to Figure 2 and
requirements is then converted into a corresponding batch of        returns a verification outcome for the input requirements. As
checkers using an LLM.                                              an initial step, we leverage an LLM to derive an LLM-derived
   For generating imperative Python checkers, we employ             verification outcome (LVO) for the input NL requirements. For
zero-shot prompting, where the prompt consists of a Python          this purpose, we adopt zero-shot prompting by describing the
function signature and a docstring comment containing the           requirement verification in the prompt. We then ask the LLM
NL requirement. This approach specifies the intended function       to output string data that satisfies all the NL requirements if
behavior, similar to how the HumanEval dataset prompts              it is possible to do so. Otherwise, we ask the LLM to output
LLMs in their code generation benchmark [31].                       UNSAT. We follow the similar prompting best practices as
   For generating declarative SMT checkers, we provide one          described earlier in Section IV. Figure 3 shows an excerpt of
example in the prompt consisting of a batch of NL require-          the prompt template used for generating LVOs with feedback.
ments along with an example pair of NL requirements and                Correctness evaluation. Once the LVO is derived, we
their corresponding SMT checker expression in string format,        evaluate its correctness by leveraging the checkers given as
and it focuses on deriving exactly one SMT expression string        input. When the LLM claims that the input requirements are
as checker for each requirement within the batch. This example      unsatisfiable, our approach relies on declarative checkers (e.g.,
guides the LLM on the expected output format, increasing            based on SMT solving) to assess its correctness. When the
the likelihood that the generated result adheres to the desired     LLM provides a proof-of-consistency string as output, both
format.                                                             declarative and imperative (e.g., a Python script) checkers
   To enhance the LLM’s performance, we also incorporate            may be leveraged for correctness evaluation. This separation is
several best practices into the prompt design, namely role          due to the theoretical limits of imperative checkers: they rely
description, chain-of-thought prompting [32], and emotional         on queries and operations over data to provide a correctness
stimuli [25].                                                       outcome, which is not possible if no data is provided by the
   Checker soundness evaluation. Once a batch of checkers           LLM (as in the UNSAT case).
is derived, it is subjected to a syntactic soundness evaluation,       If the checker confirms the correctness of the LVO, the latter
which may be augmented with semantic soundness. Note that           (i.e., either UNSAT or SAT+data) is returned by the process.
for a given batch of checkers, the soundness of each individual     Otherwise, the checker may return an incorrect or an unknown
checker is evaluated separately. If all checkers within the batch   outcome. An incorrect outcome triggers a feedback loop,
are deemed to be sound, the batch is ready to be merged with        where the quality of the current LVO is assessed respective
other batches and returned as a contiguous set. Otherwise, if       to the configured level of feedback information (e.g., the
there exist unsound checkers in a batch, feedback information       specific requirements that were violated), then the LVO and
is gathered from the soundness evaluation (e.g., which specific     its feedback is saved for future use. The quality of an LVO
checkers are unsound), then fed back into the LLM-based             is determined as a side-effect of its correctness evaluation. In
requirement-to-checker converter. Once all batches of checkers      the case where the LVO is SAT+data and the checker returns
are evaluated to be sound, they are merged into a complete set      UNSAT, we associate the quality of the LVO to the ratio of
of verification outcome checkers to be returned.                    input requirements that the data satisfies. If the LVO is UNSAT
   Since checkers are formal textual artifacts, their soundness     and the checker returns SAT, then the quality of the UNSAT
is two-fold: syntactic and semantic. On one hand, checkers          LVO is set to a fixed value. Note that the SMT checker may
must conform to the syntactic rules of the corresponding            also produce data for the input requirements. We do not wish to
formal language, e.g., Python syntax for imperative checkers.       return the checker-generated data directly since data generated
This may be evaluated efficiently by language-specific parsers.     by SMT checkers often lacks realism, and the LLM-generated
   On the other hand, ensuring semantic soundness of checkers       checkers themselves may also be incorrect.
(i.e., whether the checker indeed checks the correct property)         Declarative checkers may also return an unknown correct-
is complex and formalism-dependent. For declarative checkers,       ness outcome due to limitations of the checker (e.g., the SMT
                                                                                         LLM
                      NL                      Split               Batches of           Convert to      Batches of       Evaluate checker      Verification
                  Requirements            requirements            NL Req.s             checkers        Checkers           soundness        Outcome Checkers


                                                                                                                    Soundness Outcome
                                                                                          Gather feedback                                      Merge
                                                                                                                    Unsound     Sound
                                                                                            information                                       batches

                   Fig. 2: Overview of our divide-and-conquer approach for generating verification outcome checkers


  You are a test engineer working on creating test data for a new feature. You are given                                      VI. E VALUATION
  a variable “{name}” with some associated constraints.
  Your target is to find a string value for “{name}” that satisfies ALL of the following               We systematically evaluate our proposed LLM-based ap-
  constraints: {constraints}
                                                                                                    proach for requirement satisfiability verification. The pro-
  If the word “{name}” is meaningful, the value should be as realistic as possible.
  Before proposing a candidate value, analyze whether the constraints are logically
                                                                                                    posed framework consists of two main components: the
  consistent. If any constraints conflict, explain which ones and conclude that no                  checker generator and the checker-based verifier. To assess
  value can satisfy all constraints (output “UNSAT”).
  Below are previously generated values for “{name}” provided as counter examples in
                                                                                                    the performance of each component individually, RQ1 evalu-
  the following format:“<value>”. Note that these values do not satisfy all constraints:            ates the checker generator using different LLMs, while RQ2
  {update feedback}                                                                                 measures the LLM verifier’s theoretical performance in an
  Your output should follow the format below. If no value can satisfy all constraints,
  assign the value ”UNSAT”:                                                                         experimental setting where ground-truth checkers are avail-
  {output format}                                                                                   able. However, these two research questions focus on isolated
  Please follow these steps:                                                                        components rather than the overall system. Therefore, RQ3
                                                                  Role description
  1. Summarize Counter Example Violations: …
  2. Analyze the Constraints: …
                                                                  Template variables                then evaluates how well the approach performs in an end-to-
                                                                  Feedback information
  3. Determine Feasibility: …                                     Chain-of-thought instruction
                                                                                                    end, realistic deployment setting (i.e., without ground truth
                                                                                                    checkers), where LLMs are used to (1) generate the checkers,
Fig. 3: LVO generation with feedback prompt template excerpt                                        and to (2) use them to produce LVOs based solely on NL input.
                                                                                                    Specifically, we address the following research questions:
                                                                                                    RQ1 What is the soundness of declarative and imperative
                                                                                                          checkers generated by LLMs?
process). Thus, the feedback loop is not initiated. Instead, the
                                                                                                    RQ2 How do the feedback mechanism and checker type
best saved LVO is determined, as detailed below, and returned.
                                                                                                          impact the quality of LVOs from the LLMs?
   Budget check. Once the current LVO is saved, we check                                            RQ3 What is the end-to-end performance of the framework
the remaining budget (e.g., runtime, number of LLM calls,                                                 when LLMs generate both checkers and LVOs?
or number of tokens). If a budget remains, we continue the
feedback loop by optionally incorporating saved LVOs and/or                                         A. Evaluation setup
their feedback into the update feedback field of the subsequent                                           a) LLMs: We compare four popular LLMs that differ
LVO generation prompt. Section VI discusses the different                                           in size and accessibility. GPT-4o-mini and GPT-4o [13] are
levels of feedback information we used in our experiment.                                           powerful LLMs recently developed by OpenAI. Compared to
   If, at the current stage, no budget remains, we determine the                                    their predecessors, they demonstrate superior performance as
best LVO among all saved LVOs (i.e., the closest-to-sound)                                          well as improved speed and cost-efficiency across a range of
and return an UNKNOWN verification outcome. In practice,                                            language understanding and reasoning benchmarks. Addition-
users may proceed with such fallback output even when full                                          ally, these models exhibit strong code-generation capabilities
correctness was not established. This behavior is particularly                                      and have been integrated into various software development
useful in scenarios such as interactive workflows, where quick                                      tools, including GitHub Copilot [33].
iterations may be prioritized over absolute certainty.                                                 Despite their impressive capabilities, GPTs are closed-
                                                                                                    source and accessible only through APIs, which may raise
   We determine the best saved LVO as follows: (1) If there                                         concerns regarding data security and privacy. To address these
are more saved UNSAT LVOs than there are saved SAT+data                                             potential issues, we include two open-source LLMs in our
LVOs, then the best saved LVO (the most likely NL re-                                               evaluation. DeepSeek V3 [15], a mixture-of-experts LLM,
quirements verification outcome) is UNSAT (∼UNSAT). (2)                                             achieves performance comparable to GPT-4o while substan-
Otherwise, the best saved LVO is the SAT+data outcome with                                          tially reducing training costs. Llama3.1 8b [14] is a smaller-
the highest ratio of input NL requirements satisfied. In this                                       scale model offering a balanced trade-off between performance
case, the NL requirements’ LVO is most likely SAT (∼SAT).                                           and computational efficiency. It has been shown to achieve
   Failure mode. A critical failure mode occurs when both                                           performance comparable to larger-scale LLMs in various tasks
the LLM output and its checker are flawed but agree, leading                                        [14] while remaining deployable on consumer-grade GPUs.
to incorrect results. While feedback helps, it cannot fully                                               b) Checkers: In this experiment, we explore two types
eliminate the risk. Future work should explore safeguards like                                      of checkers for string data validation and propose a hybrid
redundant or cross-validated checkers.                                                              approach that leverages the strengths of both.
                 Verification
              Outcome Checkers                    LLM Verif.          Declarative            Correctness Outcome         - Return -
                                    LLM         Outcome (LVO)        Eval. correctness                                  Current LVO
                                                   UNSAT                                            Correct
                  NL               Derive                                                                                 UNSAT
              Requirements       verification                         Decl. | Imper.
                                                  SAT + data                                  Incorrect   Unknown       SAT + data
                                  outcome                             Eval. correctness


                                                 Budget                                   Assess LVO
                                    Gather                       Check                                                 - Return -
                                                Remains?                      Save          quality
                                   feedback                    remaining                                            Best Saved LVO
                                                  Yes                         LVO
                                 information                     budget                                               UNKNOWN
                                                                                              Find best saved       ~UNSAT ~SAT
                                                  No
                                                                                                    LVO

                         Fig. 4: Overview of our checker-based NL requirements verification approach


   (Declarative) SMT solvers are often used for handling                         c) Dataset: To evaluate the LVO quality of our require-
constraint satisfaction problems involving strings. They can               ments verification approach, we use requirements over twelve
verify whether a given string complies with a set of formal                categories of string variables drawn from common program-
constraints and detect the unsatisfiability of these constraints.          ming exercises in technical interviews, namely Email, Name,
In this study, we adapt the CVC5 solver to validate strings                Password, Url, Date, IBAN number, ISBN number, Arithmetic
against formal constraints. Nevertheless, our approach is in-              expression, Palindrome, Parentheses sequence, DNA sequence,
dependent of the solver used, allowing other SMT solvers for               and File path. While these are common programming exer-
strings, such as Z3 and Z3str, to be used as well. However, the            cises, prior studies have shown that they remain challenging
declarative nature of SMT solvers makes them challenging for               for LLMs [9]. Notably, the requirements in our case stud-
handling complex constraints involving strings. Our prelimi-               ies correspond to production rules derived from regular and
nary experiments indicate that these solvers frequently time               context-free grammars, which require computational models
out on recursive constraints (e.g., placement of parentheses in            up to pushdown automata for resolution.
mathematical formulas) while exhibiting inherent limitations                  From these requirements, we derive a total of 340 NL re-
with universal quantifiers [34].                                           quirement sets (which include both satisfiable and unsatisfiable
   (Imperative) These limitations can effectively be mitigated             cases) by considering all possible combinations of the require-
by imperatively checking strings against constraints. In our               ments and their negations using equivalence partitioning [35].
experiments, we select Python as the language for imple-                   To ensure conditions are precise, we manually formalize these
menting imperative checkers, primarily due to the exceptional              requirements.
code-generation capabilities of most LLMs using Python.                       As an example, let us consider the following requirement
Nevertheless, imperative checkers have an intrinsic limita-                from the ISBN number category ” “The system shall require
tion: they can only confirm that a specific string conforms                an ISBN number to contain exactly 10 characters, excluding
to requirements while they are unable to determine if the                  hyphens”, which is itself satisfiable. When fed into the GPT-4o
requirements themselves are unsatisfiable.                                 LLM for verification, the ”1-234-56789-X“ string is returned
   For our experiment, we ask an LLM to generate declarative               as a proof of satisfiability. Satisfiability is also confirmed by
checkers as an SMT string expression, which we use with                    the CVC5 SMT solver, which yields ”0000000000“ (a much
Python’s Z3 API to verify against our LVOs. The imperative                 less realistic value).
checkers are generated as Python function implementations,                    To assess the quality of verification outputs, we first derive
which can be parsed natively to Python executables. An                     a ground truth satisfiability label for each requirement set
example of checker generation is shown in Figure 5.                        by manually translating the requirements to formal logical
                                                                           constraints (using the SMT-LIB2 syntax) and feeding them to
  Natural language requirement.                                            the CVC5 solver (with 5-second timeout). Among the 340
  The system shall require an email address to contain                     requirement sets within the dataset, 230 returned SAT, 54
  exactly one “@” character.                                               returned UNSAT, and 56 returned UNKNOWN (which, upon
  Declarative checker.                                                     manual inspection, yielded 53 SAT cases and 3 UNSAT cases).
  (and (str.contains s “@”) (not (str.in.re s (re.++ (re.*                 Therefore, in our final labeling, we have 283 SAT cases and
  re.allchar) (str.to.re “@”) (re.* re.allchar) (str.to.re “@”)            57 UNSAT cases.
  (re.* re.allchar)))))                                                          d) Implementation details: To minimize variations
  Imperative checker.                                                      caused by LLM generation, we set the temperature to 0 for
  def this constraint(s: str) -> bool:                                     open-source models and to 0.01 for GPT models. When con-
      return s.count(“@”) == 1                                             trolled variation is needed, such as retrying without feedback,
                                                                           we use a low temperature of 0.1. We set the maximum retry
Fig. 5: An example requirement and its according checkers.                 budget to 2 LLM calls for the check generator and to 5 for the
checker-based verifier. For evaluation purposes, we map the           TABLE II: Accuracy of Python checker generation (in %)
most likely UNSAT (∼UNSAT) and SAT (∼SAT) outcomes                                LLM          Approach         Syntax Acc     Testing Acc
directly to UNSAT and SAT, respectively. The anonymized                                         BATCH              100             100
                                                                            Llama3.1-8b
                                                                                                 IND               100              98
artifact accompanying this paper is available online [36].                  GPT-4o-mini
                                                                                                 BATCH             100             100
                                                                              GPT-4o
                                                                                                  IND              100             100
B. RQ1: Checker generation                                                  DeepSeek-V3

      a) Setup: Here, we investigate the soundness of LLMs to
generate declarative (SMT) and imperative (Python) checkers                                                                       Syntax Acc
                                                                            0.8                                                   Testing Acc
from NL requirements under different settings. For both types                                                                     Formal Acc
of checkers, we provide feedback on their syntactic soundness               0.6
by the corresponding parser during checker generation.
                                                                            0.4
    Compared approaches. We compare two batching methods
for each requirement set, in accordance with Section IV: (1)                0.2
the BATCH method yields two batches: one for all positive
                                                                            0.0    BATCH IND      BATCH   IND    BATCH   IND   BATCH   IND
requirements, one for all negated requirements; (2) The IND
method creates one independent batch for each requirement.                         GPT-4o Mini     GPT-4o       DeekSeek V3 Llama3.1 8b
    Metrics. We evaluate the quality of n generated checkers            Fig. 6: Accuracy of generated SMT constraints (in %)
from both syntactic and semantic perspectives.
    For syntactic soundness, we rely on Python and SMT
parsers to verify the syntactic correctness of generated check-      checker v, let vgt denote the ground truth checker corre-
ers. Formally, let V be the set of generated checkers and            sponding to v, and let E(v, s) represent the execution output
P : V → {0, 1} represent a parser function that returns 1 if         of checker v on sample s. Testing accuracy is defined as:
the checker is syntactically valid and 0 otherwise. We define        |{v|v∈V∧∀s∈Sv :E(v,s)=E(vgt ,s)}|
                                                                                     n                 .
syntax accuracy as the ratio of syntacticallyPvalid checkers            Testing accuracy provides an over-approximation of check-
                                                      P(v)
to the total number of checkers generated: v∈Vn            . Such    ers’ semantic correctness, as it relies on a non-exhaustive set
a metric is adequate to evaluate the usability of generated          of test samples. For SMT checkers, however, it is possible
checkers (compared to, e.g., a finer-grain syntax accuracy           to formally prove semantic correctness by verifying their
metric that counts the syntax errors) since checkers must be         equivalence with the ground truth checkers.
syntactically error-free to be applicable in our use case.                 b) Results: Table II and Figure 6 present the soundness
    We also define the proportion of SMT checkers whose              of Python and SMT checkers generated by LLMs, respec-
equivalence with ground truth checkers has been formally             tively. For Python, all tested LLMs exhibit exceptional capa-
proven as formal accuracy. Formally, for a set of checkers           bility, achieving perfect syntax accuracy across both BATCH
                                          |{v|v∈V∧v≡vgt }|
V, the formal accuracy is defined as             n          . This   and IND. Moreover, three of the evaluated models (DeepSeek-
equivalence check is converted into an SMT formulation and           V3, GPT-4o, and GPT-4o-mini) maintain perfect testing
subsequently verified using the CVC5 solver. Checkers are            accuracy (100%), with only Llama3.1-8b slightly lower at
considered formally correct only if equivalence is explicitly        approximately 98% in the IND setting. These results strongly
proven; all solver results that yield timeout or unknown out-        suggest that Python is a highly suitable language for checker
comes are disregarded. Formal accuracy is the most precise           generation using LLMs, leveraging their strengths in Python
metric for evaluating correctness; however, it can only be           code generation tasks. Indeed, prior research has already
computed using declarative checkers, as it requires the CVC5         demonstrated LLMs’ capability on challenging code genera-
solver to formally verify the equivalence of two SMT expres-         tion benchmarks such as HumanEval [15]; generating Python-
sions. To the best of our knowledge, no existing method allows       based checkers for string validation is then a comparatively
for the formal equivalence checking of Python functions.             less challenging task. However, it is important to note that
    To evaluate semantic soundness across both declarative           Python checkers are not capable of validating unsatisfiability.
and imperative checkers, we adopt a testing-based approach.             LLMs’ capability is particularly important when generating
Specifically, for each requirement, we manually construct five       SMT checkers. As shown in Figure 6, smaller-scale LLMs
string samples that satisfy the requirement and five that violate    (GPT-4o-mini and Llama3.1-8b) achieve notably lower qual-
it, resulting in a total of 10 testing samples per requirement.      ity compared to larger models (GPT-4o and DeepSeek-V3).
These samples are then validated using the generated checkers        Specifically, outputs from Llama3.1-8b exhibit significantly
and compared against the ground truth labels. A checker is           lower quality, achieving less than 20% syntax and testing
considered semantically correct if it produces identical outputs     accuracy in IND. This clearly suggests that Llama3.1-8b’s
to the ground truth checker for all associated samples. We           smaller scale limits its ability to effectively generate SMT
refer to the proportion of checkers meeting this criterion           checkers. Conversely, DeepSeek-V3 and GPT-4o achieve sub-
as testing accuracy. Formally, let Sv be the set of sam-             stantially higher accuracy, both with over 85% syntax accuracy
ple string data associated with the original requirement of          and over 75% testing accuracy in IND. Interestingly, formal
accuracy is closely aligned with testing accuracy, suggesting        For each checker type, we examine three distinct feedback
that most of the checkers passing the sample-based tests can be   mechanisms: (1) V (validation), which follows a trial-and-
formally proven correct. When comparing syntax correctness        error approach, where checkers provide no explicit feedback
to semantic correctness, the ratio between syntax accuracy        but ask the LLM to retry upon incorrect outcomes; (2)
and semantic accuracy exceeds 65% in all evaluated cases          VF (validation with feedback), which explicitly incorporates
and surpasses 70% in six out of eight cases. This observation     incorrect LVOs from previous loop(s) as counterexamples
suggests that while syntax accuracy is already relatively high,   within the generation prompt; and (3) VFE (validation with
further enhancing syntax correctness could still positively       feedback and explanation), which further enriches feedback
influence semantic soundness.                                     by specifying which of the natural language requirements did
   Comparing BATCH and IND generation approaches shows            each counterexample fail, using validation results from each
that treating each requirement independently generally bene-      requirement’s corresponding checker.
fits the LLMs, with IND consistently outperforming BATCH             Metrics. We assess LVOs from different approaches based
across all tested LLMs. The accuracy gain from indepen-           on the generation quality of the test data for SAT outcome and
dent handling is particularly pronounced for smaller LLMs.        the quality of UNSAT decisions.
For instance, GPT-4o-mini shows an over 10% increase in              The Generation Success Rate (GSR) measures the percent-
accuracy when using IND, compared to only around 3%               age of requirement sets successfully verified by generating
improvement for GPT-4o. This indicates that larger LLMs           appropriate test data. Formally, let D be the dataset of re-
can effectively handle multiple requirements simultaneously,      quirements, Dsat ⊆ D represent the subset of satisfiable
making the simplified IND scenario less beneficial to them.       requirements, vgt   d
                                                                                          denote the ground truth checker associated
                                                                  with each set of requirements d ∈ D, and sd represent the
  Answer to RQ1. Three LLMs achieve perfect accuracy              string generated by an approach for a requirement set d.
  (100% testing accuracy) in generating Python check-             Furthermore, let E(v, s) ∈ B indicate the validation result
  ers, with Llama3.1-8b achieving near-perfect accuracy           of checker v on output s. The GSR is defined as: GSR =
  (≥98%) across both BATCH and IND settings. For SMT              |{d|d∈Dsat ,E(vgtd
                                                                                     ,sd )}|
  checkers, LLM size significantly influences the sound-                   |Dsat |           .
  ness, as larger LLMs (over 75% in testing accuracy                 To evaluate the effectiveness of each approach in detecting
  for DeekSeek-V3) consistently outperform smaller ones           unsatisfiable requirement sets, we compute standard precision
  (less than 20% in testing accuracy for Llama3.1-8b).            (P), recall (R), and F1-score metrics using the unsatisfiable
  Moreover, treating each requirement independently (IND)         subset of the dataset, Dunsat . Let Sunsat denote the set of
  consistently helps improve both syntactic and semantic          outputs identified as unsatisfiable by an approach. These met-
  soundness compared with batched input (BATCH).                  rics are defined as: P = |Dunsat     ∩Sunsat |
                                                                                                    |Sunsat |    , R = |Dunsat ∩Sunsat |
                                                                                                                          |Dunsat |      ,
                                                                               2×P ×R
                                                                  and F 1 = P +R .
C. RQ2: Checker-based verification                                      b) String generation results: The measurement results
      a) Setup: Existing studies suggest that applying an ex-     for requirements verification across different checkers, feed-
plicit validation stage for LLM generation may significantly      back methods, and LLMs are presented in Table III. Un-
improve the LLM’s performance in various tasks [9]–[12].          derlined numbers indicate the best quality achieved by each
Building upon this insight, this research question further        checker by integrating with a specific LLM, while bold
explores how different feedback mechanisms and checkers           numbers highlight the top-performing results for each LLM.
influence the quality of LVO produced by LLMs in the context      Results from the baseline (direct) approach reveal a significant
of requirement verification. Specifically, this RQ focuses on     difference in GSR depending on the scale of the LLM.
the theoretical performance of checker-based verification when    Evidently, LLMs’ capacity is directly correlated with output
a ground truth checker is present. In RQ3, the best theoret-      quality, as GPT-4o achieves the highest direct GSR at 78.45%,
ical settings are then evaluated in the end-to-end setting to     whereas smaller-scale LLMs, such as Llama3.1-8b, notably
understand the overall effectiveness in a realistic use case.     lag at 25.80%. Nevertheless, even the highest GSR from
   Compared approaches. We compare the direct LLM gen-            direct remains relatively low, highlighting the importance of
eration approach with various checkers and feedback methods.      additional validation techniques to enhance output quality.
The direct approach validates the satisfiability of constraints      Introducing checkers (+V) consistently enhances GSR
with a single call to the LLM. In this approach, the NL           across all evaluated LLMs compared to the direct approach.
requirements are fed into the LLM, and the derived LVO is         Notably, the GSR for GPT-4o increases from 78.45% to
returned directly (with neither a checker-based evaluation nor    91.87% when using the Python checker. Smaller models
a feedback loop). In this case, a checker-based evaluation is     exhibit even greater relative improvement; for example, the
irrelevant since the derived feedback cannot be leveraged.        GSR of Llama3.1-8b more than doubles from 25.80% to
   For feedback approaches, we assess both imperative check-      55.48% with validation by SMT checkers. These results show
ers in Python and declarative checkers using SMT. Moreover,       the effectiveness of checkers in enhancing the capability of
we propose a Hybrid approach, which uses Python to validate       smaller LLMs to produce valid string outputs.
generated strings and SMT to verify unsatisfiability decisions.      Interestingly, incorporating feedback with counterexamples
TABLE III: Quality of LVOs from compared approaches on NL requirements verification with ground truth checkers (in %)
                                GPT-4o-mini                        GPT-4o                       DeekSeek-V3                     Llama3.1-8b
   checker   Methods   GSR       P       R      F1     GSR       P       R       F1     GSR       P      R      F1     GSR       P       R      F1
              Direct   66.43   58.33   61.40   59.83   78.45   90.32   49.12    63.64   72.08   63.27  54.39   58.49   25.80   35.29   33.33   34.29
               +V      73.50   47.37   63.16   54.14   91.87   87.50   49.12    62.92   89.75   70.45  54.39   61.39   38.16   36.00   31.58   33.64
   Python      +VF     71.38   50.77   57.89   54.10   90.81   96.67   52.63    68.16   82.33   66.00  57.89   61.68   38.87   34.15   26.32   29.72
              +VFE     74.56   52.31   59.65   55.74   91.52   90.62   50.88    65.17   84.81   62.00  54.39   57.94   45.94   46.67   36.84   41.18
               +V      74.20   60.56   75.44   67.19   86.93   69.05   50.88    58.59   86.93   70.00  61.40   65.42   55.48   70.91   68.42   69.64
    SMT        +VF     75.97   65.82   91.23   76.47   87.28   82.26   89.47    85.71   84.10   80.60  94.74   87.10   48.76   71.43 98.25     82.72
              +VFE     74.56   69.33   91.23   78.79   89.75   81.54   92.98    86.89   89.75   79.41  94.74   86.40   46.64   68.42   91.23   78.20
               +V      77.39   63.08   71.93   67.21   92.23   93.55   50.88    65.91   91.87   85.37  61.40   71.43   53.36   77.50   56.14   65.11
   Hybrid      +VF     78.09   72.00   94.74   81.82   90.11   96.15   87.72    91.74   90.81   87.10  94.74   90.76   51.94   80.95   91.23   85.78
              +VFE     77.74   74.29   92.98   82.59   92.23   96.36   92.98    94.64   91.87   89.83  96.49   93.04   57.24   80.60   94.74   87.10



(+VF) does not consistently enhance GSR and, in some                           enhances the output quality, yielding gains in 10 out of
instances, slightly decreases it. For example, using the SMT                   12 scenarios compared to validation alone. Supplementing
checker, the GSR notably drops from 55.48% to 48.76%. This                     these counterexamples with explanations (+VFE) results in the
reduction could be attributed to confusion caused by coun-                     highest overall LVO quality, further improving the F1-score in
terexamples lacking explanations, making it difficult for LLMs                 8 out of 12 scenarios compared to +VF cases.
to identify why specific inputs fail validation. This hypothesis
is reinforced by the improvements when explanatory feedback                      Answer to RQ2. Incorporating feedback from ground
(+VFE) is introduced, resulting in enhanced GSR in 7 out of                      truth checkers substantially improves LVO quality from
the 12 tested scenarios compared to both +V and +VF.                             LLMs in terms of both GSR and verification F1-scores.
   When comparing the effectiveness of different checkers,                       Specifically, the Hybrid checker, combined with coun-
Python generally yields improvements similar to those of                         terexamples and explanations (+VFE), achieves the best
SMT for smaller LLMs (GPT-4o-mini and Llama3.1-8b).                              results, providing the highest GSR (57.24% to 92.23%)
We hypothesize that smaller LLMs struggle with more com-                         in three out of four LLMs and the best verification F1-
plex requirements where Python checkers could be more                            scores (82.59% to 93.04%) across all evaluated LLMs.
beneficial. Indeed, Python consistently outperforms SMT for
larger models, particularly GPT-4o, achieving the highest GSR
                                                                               D. RQ3: End-to-end evaluation
of 91.87%, compared to 89.75% with SMT. Furthermore,
combining Python and SMT into a Hybrid checker results in                            a) Setup: In this research question, we integrate the pre-
even better LVO quality, providing the highest GSR of 92.23%                   viously evaluated checker generator from RQ1 and checker-
across all LLMs and feedback configurations evaluated.                         based verifiers from RQ2 to comprehensively assess the
      c) Requirement verification results: When evaluating the                 overall system.
effectiveness of the approaches in verifying the satisfiability                   Compared approaches. We evaluate the combined system
of requirement sets, the Python checker alone does not con-                    of the best configurations identified in previous research
sistently improve the generation F1-score, as it cannot vali-                  questions for the checker generator and the checker-based
date the unsatisfiability (UNSAT) decisions made by LLMs.                      verifier. Specifically, for the checker generator, we select
Conversely, the SMT checker can effectively verify these                       the checkers generated by IND across all evaluated LLMs.
UNSAT decisions, yielding significant improvements over the                    For the checker-based verifier, we adopt the Hybrid+VFE
direct approach. Notably, incorporating explanatory feedback                   configuration, which integrates the advantages of both declar-
(+VFE) enhances precision for three out of four LLMs and                       ative and imperative validation methods and provides the
improves recall and F1-scores across all evaluated models.                     most detailed feedback. We assess the effectiveness of these
Moreover, the Hybrid checker uses Python’s better capability                   combined configurations across all LLMs, comparing their
to detect invalid string outputs, further improving output                     output quality against the baseline results obtained without
quality and achieving higher F1-scores compared to the SMT                     any checker or feedback loop (Direct, as presented in RQ2).
checker alone in the +VFE scenario. This improvement is                           Metrics. We evaluate the LVO quality from the integrated
more notable for smaller LLMs; for example, the F1-score of                    system using the same metrics as defined in RQ2: GSR, P, R,
Llama3.1-8b increases substantially from 34.29% to 87.10%                      and F1. Since RQ2 configurations use ground truth checkers,
using the Hybrid+VFE approach.                                                 their corresponding metric values represent an upper bound on
   When comparing feedback methods, providing more infor-                      achievable LVO quality for the complete system. Therefore,
mative feedback consistently helps LLMs identify inconsisten-                  in this RQ, we report the ratio of the measured metrics to
cies within sets of requirements. Introducing validation alone                 these upper-bound values for each metric. Specifically, given
(+V) already enhances the F1-score in identifying unsatisfiable                a measured metric value m and its corresponding upper-bound
requirement sets, improving it in 8 out of 12 cases. However,                  value m̂ (obtained using ground truth checkers), we calculate
                                                                                                   m
because this method does not offer explicit feedback, quality                  and plot the ratio m̂  to illustrate how closely each evaluated
gains remain limited. Adding counterexamples (+VF) further                     configuration approaches the upper-bound metric values.
          GPT-4o-mini            Llama3.1-8b    GPT-4o                        DeepSeek-V3                      Llama3.1-8b
                 GRS             GPT-4o-mini       GRS                              GRS                                GRS
           1.0                   GPT-4o      1.0                              1.0                              1.0
                                 DeepSeek-V3                                                                     0.8
             0.8                 No checkers    0.8                             0.8
                                                                                                                     0.6
                 0.6                            0.6                                 0.6
                                                                                                                       0.4
P                   0.4        R P                0.4            R P                   0.4        R P                      0.2       R




                   F1                            F1                                   F1                               F1
Fig. 7: Metric ratio of different LLM-based verifiers using LLM-generated checkers compared with the ground truth checkers;
each figure represents a different LLM-based verifier; each line represents a checker generation method; the filled color shows
the best checker generation method for each verifier


     b) Results: Figure 7 presents radar plots illustrating the      to scenarios without checkers. This finding suggests that our
metric ratio of the system across various LLM combinations           feedback system generally shows robustness against variations
compared against the baseline approach without validation            in the quality of generated checkers.
(Direct from RQ2). Specifically, the center of each radar plot
corresponds to a metric ratio of 0.4 for GPT-4o-mini, GPT-             Answer to RQ3. Combining an LLM-based checker gen-
4o, and DeepSeek-V3, whereas the center represents a ratio             erator with a checker-based verifier significantly improves
of 0.2 for Llama3.1-8b.                                                output quality compared to direct generation without
   The quality of LVOs generated using the feedback ap-                checkers, achieving over 95% GSR ratio in three verifiers
proaches significantly outperforms the configuration without           and over 60% F1-score ratio in all verifiers. Enhancing
checkers (Direct) across almost all metrics and configura-             the quality of individual components, such as using
tions. The only exceptions occur when checkers generated               higher-quality checkers and more capable verifier LLMs,
by Llama3.1-8b are used with either the GPT-4o-mini or                 directly translates into improved overall performance in
Llama3.1-8b verifiers, likely due to the limited quality of            the final LVO. This finding highlights the modularization
these generated checkers combined with the lower capability            of the system for achieving better overall outcomes.
of these smaller LLMs. Across all configurations, the GSR
consistently exceeds the baseline without checkers and ap-
                                                                     E. Threats to Validity
proaches the ground-truth checker, particularly when using
checkers generated by DeepSeek-V3 combined with verifiers               Internal Validity: The authors manually convert each re-
such as GPT-4o and DeepSeek-V3, achieving ratios over                quirement set into checkers and testing samples, which could
95%. However, verification F1-score remains considerably             introduce biases or inaccuracies. To mitigate potential issues
below their upper bounds, with the best case achieving around        arising from manual effort, we cross-check the created checks
88% when combining the GPT-4o-mini verifier with checkers            and samples to make sure they are consistent with each
generated by DeepSeek-V3. This performance gap likely                other. Moreover, the dataset is imbalanced and contains more
results from the substantially lower quality of generated SMT        SAT cases than UNSAT cases. To mitigate bias caused by
checkers compared to Python checkers, highlighting the need          this imbalance, we evaluate different metrics separately for
for further improvements in SMT checker generation methods.          each category. Additionally, we control for variations in LLM
   When comparing output quality across different checkers,          outputs by setting temperature parameters to zero for open-
higher checker quality consistently correlates with improved         source models (e.g., Llama3.1-8b and DeepSeek-V3) and
overall output quality. Specifically, verifiers using the highest-   to a minimal value (0.01) for GPT-based models, except in
quality checkers generated by GPT-4o and DeepSeek-V3                 cases where controlled variation is necessary (such as the +V
generally achieve the best results. Notably, DeepSeek-V3-            scenario), in which case a temperature value of 0.1 is used.
generated checkers yield the highest GSR for three out of               External Validity: The collected requirements in the dataset
four verifiers, and GPT-4o-generated checkers produce the            may be impacted by selection bias. Therefore, our findings
best F1-scores in three out of four verifiers. Interestingly, even   may differ when generalized to other contexts. Specifically, the
though checkers generated by Llama3.1-8b have significantly          original requirements may be present in the training data of
lower SMT checker quality compared with other LLMs (see              LLMs, as they are derived from common programming exer-
RQ1), they still enhance LVO quality across all metrics for          cises. However, the dataset includes all possible combinations
the GPT-4o and DeepSeek-V3 verifiers, and improve GSR,               of these requirements and their negations. Such unusual cases
P, and F1 metrics for the GPT-4o-mini verifier compared              are less likely to occur in the training dataset. Future studies
are necessary to evaluate whether our approach generalizes            different LLMs and specialized prompting techniques tailored
well to more complex, industry-scale requirements.                    for each subtask.
   Construct validity: We evaluate the quality of generated              Iterative LLM-based approaches have been effectively
checkers based on semantic and syntactic correctness, consis-         adapted to software engineering tasks such as code generation
tent with general practice in code generation [37]. We assess         [52], [56], test generation [57], and software modeling [58].
the quality of LVOs on standard success rate for generation,          In requirement engineering, specifically, iterative methods
and precision/recall/F1-score for classification.                     have integrated retrieval-augmented generation for enhanced
                                                                      requirement traceability and compliance checking [59].
                     VII. R ELATED W ORK                                 In this paper, we propose an iterative approach using LLMs
                                                                      for requirement satisfiability verification. Our approach can
LLM for requirements engineering. LLMs are becoming                   also be seen as a multi-agent system, wherein one agent
increasingly popular in various stages of requirements engi-          (checker generator) generates verification checkers to validate
neering, including elicitation, modeling, and verification [38].      the verification outputs produced by another agent (checker-
   Ronanki et al. [39] explore the strengths and limitations of       based verifier).
LLMs in the elicitation process. Görer and Aydemir [40] pro-
pose an LLM-assisted approach that yields interview questions                                  VIII. C ONCLUSION
for identifying new requirements. In requirement modeling,
                                                                         In this paper, we propose an approach that leverages LLMs,
existing work has studied LLM’s ability in generating domain
                                                                      SMT solvers (i.e., CVC5), and imperative programming (i.e.,
models [41], [42] and goal models [43], [44]. LLMs have
                                                                      Python) for the verification of NL requirements for satisfia-
also been effectively used for helping identify ambiguities or
                                                                      bility through consistent string and checker generation. Our
inconsistent sets of requirements [1], [2].
                                                                      approach takes as input a collection of NL requirements over
   In this paper, we leverage LLMs for verification of NL
                                                                      strings and either (1) detects unsatisfiable requirements or
requirements for satisfiability. As a key side effect, when
                                                                      (2) generates a conforming string instance as a proof of
requirement sets are satisfiable, our approach generates a con-
                                                                      satisfiability. We experimentally show that checker generation
formant and realistic string instance as a proof of satisfiability,
                                                                      is improved by assessing each requirement individually, while
which is relevant as input data for requirements-based testing.
                                                                      requirements verification benefits from integrating declarative
LLM for test data generation. Due to their impressive NL              and imperative checkers with detailed feedback. These findings
generation capability, LLMs have been increasingly applied            allow us to achieve near-ground-truth performance without
to test data generation tasks (e.g., for testing graphical user       manual intervention, e.g., NL requirement formalization.
interfaces [45], fuzz testing [46], validating SMT solvers [47])         As future work, we plan to extend our satisfiability ver-
from (satisfiable) requirements given as input. However, less         ification approach for string requirements to more complex
focus has been placed on (1) satisfiability of requirements and       textual formalisms, such as domain-specific textual languages.
on (2) assessing requirements over strings.                           While this work focuses on string requirements, the underlying
   Existing research [48] takes as input user-written constraints     idea of combining checker generation with data generation is
for string variables and generates corresponding test cases.          expected to generalize to a broader range of requirement types,
In contrast, our approach verifies the input requirements             provided that a corresponding formal specification language
for satisfiability and outputs consistent test data when the          and constraint satisfiability solving approach are available. For
requirements are satisfiable. Similarly, Babikian et al. [9]          instance, our approach may be applicable to the satisfiability
propose a textual test data generation approach from input            verification of NL requirements on the safety of autonomous
NL requirements over strings. However, their approach relies          vehicles, where such requirements are represented as numeric
on manual formalization of NL requirements to ensure output           conditions over the position and assigned path of each vehicle
correctness, which is a significant drawback compared to our          in a traffic scenario [60]. We plan to explore this extension in
proposed approach.                                                    future work. Further improvements in SMT checker genera-
   Iterative generation with LLMs. Recent advances in                 tion could be explored by incorporating semantic soundness
LLMs have demonstrated impressive performance in various              feedback during the generation process. Additionally, we plan
tasks. However, complex reasoning problems still pose signif-         to improve the feedback loop proposed in Figure 4 by inte-
icant challenges, motivating approaches that decompose com-           grating stochastic mutations over a collection of simultaneous
plex tasks into iterative sub-tasks [49]. The Tree-of-Thought         LVOs, in analogy to a genetic algorithm.
framework [49], [50] enables LLMs to approach decision-
making incrementally, with the ability to trace back and                                           R EFERENCES
revise decisions if necessary. Building upon this, the Graph-
                                                                       [1] N. Feng, L. Marsso, S. G. Yaman, I. Standen, Y. Baatartogtokh,
of-Thought framework [51] allows LLMs to organize their                    R. Ayad, V. O. De Mello, B. Townsend, H. Bartels, A. Cavalcanti
reasoning in a graph structure, enabling the parallel execution            et al., “Normative requirements operationalization with large language
of multiple subtasks. More recently, multi-agent collaboration,            models,” in RE 2024. IEEE, 2024, pp. 129–141.
                                                                       [2] A. Fantechi, S. Gnesi, L. Passaro, and L. Semini, “Inconsistency
employing multiple LLMs for distinct subtasks, has gained                  detection in natural language requirements using ChatGPT: a preliminary
popularity [52]–[55]. Such methods leverage the strengths of               evaluation,” in RE 2023. IEEE, 2023, pp. 335–340.
 [3] M. B. Hosseini, J. Heaps, R. Slavin, J. Niu, and T. Breaux, “Ambiguity         [26] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, “Large
     and Generality in Natural Language Privacy Policies,” in 2021 IEEE                  language models are zero-shot reasoners,” NeurIPS 2022, pp. 22 199–
     29th International Requirements Engineering Conference (RE), 2021,                  22 213, 2022.
     pp. 70–81.                                                                     [27] OpenAI, accessed: 2025-03-10. [Online]. Available: https://openai.com/
 [4] D. Giannakopoulou, T. Pressburger, A. Mavridou, and J. Schumann,                    index/introducing-structured-outputs-in-the-api
     “Generation of Formal Requirements from Structured Natural Lan-                [28] H. Chase and contributors, “LangChain,” 2022. [Online]. Available:
     guage,” in Requirements Engineering: Foundation for Software Quality,               https://github.com/langchain-ai/langchain
     N. Madhavji, L. Pasquale, A. Ferrari, and S. Gnesi, Eds. Springer              [29] P. Dinges and G. A. Agha, “Solving complex path conditions through
     International Publishing, 2020, pp. 19–35.                                          heuristic search on induced polytopes,” in Proceedings of the 22nd
 [5] D. M. Berry and E. Kamsties, “Ambiguity in Requirements Specifica-                  ACM SIGSOFT International Symposium on Foundations of Software
     tion,” in Perspectives on Software Requirements. Springer US, 2004,                 Engineering, (FSE-22), Hong Kong, China, November 16 - 22, 2014.
     pp. 7–44.                                                                           ACM, 2014, pp. 425–436.
 [6] L. De Moura and N. Bjørner, “Z3: An efficient SMT solver,” in TACAS            [30] I. Kandel and M. Castelli, “The effect of batch size on the generalizabil-
     2008. Springer, 2008, pp. 337–340.                                                  ity of the convolutional neural networks on a histopathology dataset,”
 [7] T. Chen, M. Hague, A. W. Lin, P. Rümmer, and Z. Wu, “Decision                      ICT Express, vol. 6, no. 4, pp. 312–315, 2020. [Online]. Available:
     procedures for path feasibility of string-manipulating programs with                https://www.sciencedirect.com/science/article/pii/S2405959519303455
     complex operations,” OSTRICH String Constraint Solver and Results,             [31] M. Chen, J. Tworek, H. Jun, Q. Yuan et al., “Evaluating large language
     vol. 3, no. POPL, pp. 49:1–49:30, Jan. 2019.                                        models trained on code,” arXiv preprint arXiv:2107.03374, 2021.
 [8] J. Huang and K. C.-C. Chang, “Towards reasoning in large language              [32] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
     models: A survey,” in ACL 2023. ACL, 2023, pp. 1049–1065.                           D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large
 [9] A. A. Babikian, B. Chen, and G. Mussbacher, “Exploring                              language models,” Advances in neural information processing systems,
     large language models for requirements on string values,”                           vol. 35, pp. 24 824–24 837, 2022.
     in Proceedings of the 2nd IEEE/ACM Workshop on Multi-                          [33] “Github copilot,” https://github.com/features/copilot, accessed: 2025-03-
     disciplinary, Open, and RElevant Requirements Engineering,                          10.
     2025. [Online]. Available: https://mo2re.github.io/assets/preprints/           [34] “Cvc5/src/theory/incomplete id.h at main · cvc5/cvc5,” https://github.
     BCM-LLMsForStringRequirments-MO2RE25.pdf                                            com/cvc5/cvc5/blob/main/src/theory/incomplete id.h.
[10] Y. Li, J. Parsert, and E. Polgreen, “Guiding enumerative program               [35] I. Burnstein, Practical software testing: a process-oriented approach.
     synthesis with large language models,” in International Conference on               Springer Science & Business Media, 2006.
     Computer Aided Verification. Springer, 2024, pp. 280–301.
                                                                                    [36] B. Chen, A. A. Babikian, S. Feng, D. Varró, and G. Mussbacher,
[11] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof
                                                                                         “Constrainsolver artifacts,” Jun. 2025. [Online]. Available: https:
     generation and repair with large language models,” in Proceedings of
                                                                                         //doi.org/10.5281/zenodo.15679384
     the 31st ACM Joint European Software Engineering Conference and
                                                                                    [37] L. Chen, Q. Guo, H. Jia, Z. Zeng, X. Wang, Y. Xu, J. Wu, Y. Wang,
     Symposium on the Foundations of Software Engineering, 2023, pp.
                                                                                         Q. Gao, J. Wang et al., “A survey on evaluating large language models
     1229–1241.
                                                                                         in code generation tasks,” arXiv preprint arXiv:2408.16498, 2024.
[12] J. H. Kirchner, Y. Chen, H. Edwards, J. Leike, N. McAleese, and
     Y. Burda, “Prover-verifier games improve legibility of llm outputs,”           [38] C. Arora, J. Grundy, and M. Abdelrazek, “Advancing requirements
     arXiv preprint arXiv:2407.13692, 2024.                                              engineering through generative AI: Assessing the role of LLMs,” in
[13] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark,                Generative AI for Effective Software Development. Springer, 2024, pp.
     A. Ostrow, A. Welihinda, A. Hayes, A. Radford et al., “Gpt-4o system                129–148.
     card,” arXiv preprint arXiv:2410.21276, 2024.                                  [39] K. Ronanki, C. Berger, and J. Horkoff, “Investigating ChatGPT’s poten-
[14] A. Grattafiori, A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle,             tial to assist in requirements elicitation processes,” in 2023 49th Euromi-
     A. Letman, A. Mathur, A. Schelten, A. Vaughan et al., “The llama 3                  cro Conference on Software Engineering and Advanced Applications
     herd of models,” arXiv preprint arXiv:2407.21783, 2024.                             (SEAA). IEEE, 2023, pp. 354–361.
[15] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng,              [40] B. Görer and F. B. Aydemir, “Generating requirements elicitation
     C. Zhang, C. Ruan et al., “Deepseek-v3 technical report,” arXiv preprint            interview scripts with large language models,” in RE 2023 Workshops
     arXiv:2412.19437, 2024.                                                             (REW). IEEE, 2023, pp. 44–51.
[16] Y.-F. Chen, D. Chocholatý, V. Havlena, L. Holı́k, O. Lengál, and J. Sı́č,   [41] K. Chen, Y. Yang, B. Chen, J. A. H. López, G. Mussbacher, and
     “Solving string constraints with lengths by stabilization,” Proceedings             D. Varró, “Automated domain modeling with large language models: A
     of ACM Programming Languages, vol. 7, no. OOPSLA2, Oct. 2023.                       comparative study,” in 2023 ACM/IEEE 26th International Conference
[17] K. Lotz, A. Goel, B. Dutertre, B. Kiesl-Reiter, S. Kong, R. Majumdar,               on Model Driven Engineering Languages and Systems (MODELS).
     and D. Nowotka, “Solving String Constraints Using SAT,” in CAV 2023.                IEEE, 2023, pp. 162–172.
     Springer, 2023, pp. 187–208.                                                   [42] J. Cámara, J. Troya, L. Burgueño, and A. Vallecillo, “On the assessment
[18] H. Wu, Y.-F. Chen, Z. Wu, B. Xia, and N. Zhan, “A decision procedure                of generative ai in modeling tasks: an experience report with chatgpt and
     for string constraints with string/integer conversion and flat regular              uml,” Software and Systems Modeling, vol. 22, no. 3, pp. 781–793, 2023.
     constraints,” Acta Informatica, vol. 61, no. 1, pp. 23–52, Mar. 2024.          [43] B. Chen, K. Chen, S. Hassani, Y. Yang, D. Amyot, L. Lessard,
[19] S. Krings, J. Schmidt, P. Skowronek, J. Dunkelau, and D. Ehmke,                     G. Mussbacher, M. Sabetzadeh, and D. Varró, “On the use of GPT-4 for
     “Towards Constraint Logic Programming over Strings for Test Data                    creating goal models: An exploratory study,” in RE 2023 Workshops.
     Generation,” in Declarative Programming and Knowledge Management.                   IEEE, 2023, pp. 262–271.
     Springer, 2020, pp. 139–159.                                                   [44] S. de Kinderen and K. Winter, “Towards taming large language models
[20] “SMT-LIB The Satisfiability Modulo Theories Library,” https://smt-                  with prompt templates for legal GRL modeling,” in BPMDS 2024.
     lib.org/benchmarks.shtml.                                                           Springer, 2024, pp. 213–228.
[21] “SMT-COMP 2024,” https://smt-comp.github.io/2024/.                             [45] Z. Liu, C. Chen, J. Wang, X. Che, Y. Huang, J. Hu, and Q. Wang, “Fill
[22] C. Barrett, P. Fontaine, and C. Tinelli, “The SMT-LIB standard: Version             in the blank: Context-aware automated text input generation for mobile
     2.6,” Department of Computer Science, The University of Iowa, Tech.                 GUI testing,” in ICSE 2023. IEEE, 2023, pp. 1355–1367.
     Rep., 2017.                                                                    [46] C. S. Xia, M. Paltenghi, J. Le Tian, M. Pradel, and L. Zhang, “Fuzz4all:
[23] A. Vaswani, N. M. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N.                 Universal fuzzing with large language models,” in ICSE 2024, 2024, pp.
     Gomez, L. Kaiser, and I. Polosukhin, “Attention is all you need,” in                1–13.
     NIPS, 2017.                                                                    [47] M. Sun, Y. Yang, Y. Wang, M. Wen, H. Jia, and Y. Zhou, “SMT solver
[24] P. Sahoo, A. K. Singh, S. Saha, V. Jain, S. Mondal, and A. Chadha,                  validation empowered by large pre-trained language models,” in ASE
     “A systematic survey of prompt engineering in large language models:                2023. IEEE, 2023, pp. 1288–1300.
     Techniques and applications,” arXiv preprint arXiv:2402.07927, 2024.           [48] Z. Liu, C. Chen, J. Wang, M. Chen, B. Wu, Z. Tian, Y. Huang, J. Hu,
[25] C. Li, J. Wang, Y. Zhang, K. Zhu, W. Hou, J. Lian, F. Luo, Q. Yang,                 and Q. Wang, “Testing the limits: Unusual text inputs generation for
     and X. Xie, “Large language models understand and can be enhanced                   mobile app crash detection with large language model,” in ICSE 2024,
     by emotional stimuli,” arXiv preprint arXiv:2307.11760, 2023.                       2024, pp. 1–12.
[49] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and
     K. Narasimhan, “Tree of thoughts: Deliberate problem solving with large
     language models,” Advances in neural information processing systems,
     vol. 36, pp. 11 809–11 822, 2023.
[50] J. Long, “Large language model guided tree-of-thought,” arXiv preprint
     arXiv:2305.08291, 2023.
[51] M. Besta, N. Blach, A. Kubicek, R. Gerstenberger, M. Podstawski,
     L. Gianinazzi, J. Gajda, T. Lehmann, H. Niewiadomski, P. Nyczyk
     et al., “Graph of thoughts: Solving elaborate problems with large
     language models,” in Proceedings of the AAAI Conference on Artificial
     Intelligence, vol. 38, no. 16, 2024, pp. 17 682–17 690.
[52] S. Hong, X. Zheng, J. Chen, Y. Cheng, J. Wang, C. Zhang, Z. Wang,
     S. K. S. Yau, Z. Lin, L. Zhou et al., “Metagpt: Meta programming for
     multi-agent collaborative framework,” arXiv preprint arXiv:2308.00352,
     vol. 3, no. 4, p. 6, 2023.
[53] J. Li, Q. Zhang, Y. Yu, Q. Fu, and D. Ye, “More agents is all you need,”
     arXiv preprint arXiv:2402.05120, 2024.
[54] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,
     S. Zhang, J. Liu et al., “Autogen: Enabling next-gen LLM applications
     via multi-agent conversation,” arXiv preprint arXiv:2308.08155, 2023.
[55] D. Gao, Z. Li, X. Pan, W. Kuang, Z. Ma, B. Qian, F. Wei, W. Zhang,
     Y. Xie, D. Chen et al., “Agentscope: A flexible yet robust multi-agent
     platform,” arXiv preprint arXiv:2402.14034, 2024.
[56] J. He, C. Treude, and D. Lo, “Llm-based multi-agent systems for
     software engineering: Literature review, vision and the road ahead,”
     ACM Transactions on Software Engineering and Methodology, 2024.
[57] N. Alshahwan, J. Chheda, A. Finogenova, B. Gokkaya, M. Harman,
     I. Harper, A. Marginean, S. Sengupta, and E. Wang, “Automated unit
     test improvement using large language models at Meta,” in Companion
     Proceedings of the 32nd ACM International Conference on the Founda-
     tions of Software Engineering, 2024, pp. 185–196.
[58] Y. Yang, B. Chen, K. Chen, G. Mussbacher, and D. Varro, “Multi-step
     iterative automated domain modeling with large language models,” in
     ACM/IEEE 27th International Conference on Model Driven Engineering
     Languages and Systems: Companion Proceedings (MODELS), 2024, pp.
     587–595.
[59] A. Masoudifard, M. M. Sorond, M. Madadi, M. Sabokrou, and
     E. Habibi, “Leveraging graph-rag and prompt engineering to enhance
     llm-based automated requirement traceability and compliance checks,”
     arXiv preprint arXiv:2412.08593, 2024.
[60] A. A. Babikian, O. Semeráth, and D. Varró, “Concretization of Abstract
     Traffic Scene Specifications Using Metaheuristic Search,” IEEE Trans-
     actions on Software Engineering, vol. 50, no. 1, pp. 48–68, 2024.
