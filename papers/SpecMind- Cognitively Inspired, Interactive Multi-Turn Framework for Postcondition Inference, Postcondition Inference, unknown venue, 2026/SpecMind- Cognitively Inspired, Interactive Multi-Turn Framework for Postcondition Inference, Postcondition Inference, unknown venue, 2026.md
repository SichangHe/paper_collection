                                         S PEC M IND: Cognitively Inspired, Interactive Multi-Turn Framework for
                                                                  Postcondition Inference
                                                       Cuong Chi Le1 , Minh V.T. Pham2 , Tung Duy Vu3 , Cuong Duc Van2 ,
                                                              Huy N. Phan2 , Hoang N. Phan4 , Tien N. Nguyen1
                                                             1
                                                                 The University of Texas at Dallas, 2 FPT Software AI Center,
                                                                    3
                                                                      VinUniversity, 4 Nanyang Technological University
                                                                            Contacts: {cuong.le, tien.n.nguyen}@utdallas.edu


                                                                 Abstract                                Third, EvoSpex (Molina et al., 2021) uses
                                                                                                      execution-guided evolutionary search to evolve
                                             Specifications are vital for ensuring program
arXiv:2602.20610v3 [cs.SE] 28 Jun 2026




                                             correctness, yet writing them manually re-               postcondition candidates, yet its handcrafted opera-
                                             mains challenging and time-intensive. Recent             tors only weakly exploit program semantics, lead-
                                             large language model (LLM)-based methods                 ing to incomplete or brittle postconditions. Fourth,
                                             have shown successes in generating specifi-              nl2postcond (Endres et al., 2024) leverages LLMs
                                             cations such as postconditions, but existing             to translate code and informal documentation into
                                             single-pass prompting often yields inaccurate            postconditions. The limitation of simple prompting
                                             results. In this paper, we present S PEC M IND,          in nl2postcond lies in their reliance on single-pass
                                             a novel framework for postcondition genera-
                                                                                                      generation: nl2postcond expects the LLM to gen-
                                             tion that treats LLMs as interactive and ex-
                                             ploratory reasoners rather than one-shot gen-            erate a correct and complete postcondition in a
                                             erators. S PEC M IND employs feedback-driven             single prompt. Such prompting results in incorrect
                                             multi-turn prompting approaches, enabling the            postconditions that are syntactically plausible but
                                             model to iteratively refine candidate postcondi-         semantically inaccurate, failing correctness tests
                                             tions by incorporating implicit and explicit cor-        or lacking discriminative power for bug detection.
                                             rectness feedback, while autonomously decid-             (Related work details are given in Appendix A.2).
                                             ing when to stop. This process fosters deeper
                                                                                                         In our work, S PEC M IND, we aim to enhance
                                             code comprehension and improves alignment
                                             with true program behavior via exploratory at-           the LLM’s capability in generating postconditions
                                             tempts. Our empirical evaluation shows that              from given source code. A more robust alternative
                                             S PEC M IND significantly outperforms state-of-          is retry-based prompting (Greedy Multi-turn or
                                             the-art approaches in both accuracy and com-             Greedy for short), where the LLM is iteratively
                                             pleteness of generated postconditions.                   asked to regenerate postconditions until one passes
                                                                                                      a soundness check and exceeds a certain threshold
                                         1   Introduction
                                                                                                      of completeness. While this approach introduces
                                         Program specifications (pre-/postconditions) are             feedback into the loop, it remains reactive and ex-
                                         central to checking that program behavior matches            ternally controlled – the LLM is not actively in-
                                         intent, but writing them manually is tedious. Prior          volved in the reasoning process but simply retries in
                                         work on automated inference broadly falls into four          response to failure signals. Thus, we also propose
                                         categories. First, program-analysis methods infer            Exploratory Multi-Turn (Exploratory for short),
                                         invariants dynamically from executions (Beschast-            offering a more cognitively aligned framework in
                                         nikh et al., 2011; Ernst et al., 1999)—and thus are          which the LLM is treated not just as a code-to-
                                         coverage-limited—or statically from code, often              code generator, but as an interactive reasoner.
                                         at the cost of conservative, false-positive–prone re-        We prompt the LLM to autonomously perform the
                                         sults (Ramanathan et al., 2007; Wei et al., 2011).           exploration, internalize the reasoning process to de-
                                         Second, data-mining approaches extract common                rive the postcondition, and decide by itself when to
                                         API-usage patterns (e.g., call pairs/sequences and           stop the process. We prompt the model to perform
                                         automata) from large codebases (Wasylkowski                  one or multiple turns for exploration, i.e., submit-
                                         et al., 2007; Thummalapenta and Xie, 2009; Pradel            ting postconditions to obtain the intermediate feed-
                                         and Gross, 2009; Wasylkowski and Zeller, 2009;               back on soundness and completeness, before decid-
                                         Zhong et al., 2009a), but typically do not infer se-         ing to submit the final postcondition. This method
                                         mantic specifications such as pre-/postconditions.           engages the model in an iterative self-refinement
                                         Task #69 from EvalPlus                                                                       Single-pass (nl2postcond)
            def search(lst):                                                                                       assert return_value == -1
                                                                                                        Solution
                '''You are given a non-empty list of positive integers. Return the greatest                               or (return_value > 0 and return_value in lst)
            integer that is greater than zero, and has a frequency greater than or equal to
            the value of the integer itself. The frequency of an integer is the number of
            times it appears in the list. If no such a value exist, return -1.'''                                                        Exploratory Multi-Turn
                count = dict()                                                                           Turn 1:     assert return_value == -1
                for num in lst:                                                                          Explore            or (return_value > 0 and return_value in lst)
                    if num not in count:
                                                                                                                                         Observation: Assertions are correct.
                         count[num] = 0
                    count[num] += 1                                                                      Turn 2:     assert return_value == -1
                ans = -1                                                                                 Explore            or lst.count(return_value) >= return_value
                for num, cnt in count.items():                                                                                           Observation: Assertions are correct.
                    if cnt >= num:                                                                                   assert return_value == -1
                         ans = max(ans, num)
                                                                                                         Turn 3:
                                                                                                                            or all(lst.count(x) < x or x <= return_value
                return ans                                                                               Explore
                                                                                                                                 for x in set(lst) if x > 0)
                                                                                                                                         Observation: Assertions are correct.
                                             Greedy Multi-Turn                                           Turn 4:
                                                                                                                     assert return_value == -1
                                                                                                                            or all(x < return_value or lst.count(x) < x
            Turn 1: assert return_value == -1                                                            Explore
                                                                                                                                 for x in set(lst))
           Solution        or (return_value > 0 and return_value in lst)
                                                                                                          Observation: Assertions are incorrect. The postcondition failed on correct function implementation.
                  Observation: Assertions are correct, but they can not catch a buggy implementation.
                                                                                                                    The assertion failed, which means our current postconditions might
            Turn 2: count = Counter(lst)                                                                 Turn 5:
                                                                                                                    not be sufficient or accurate. Let’s revisit and refine them... We
           Solution assert return_value == -1 or count[return_value] >= return_value                      Think
                                                                                                                    can use a different approach to check this. Let’s iterate over...
                  Observation: Assertions are correct, but they can not catch a buggy implementation.               assert (lst.count(return_value) >= return_value
                   count = Counter(lst)                                                                  Turn 5:      and return_value == max(x for x in set(lst) if lst.count(x) >= x
            Turn 3:                                                                                                     and x > 0) or (return_value == -1 and not any(lst.count(x) >= x
                    assert return_value == -1 or all(return_value >= x                                   Explore
           Solution                                                                                                     and x > 0 for x in set(lst))))
                             and count[x] >= x for x in set(lst) if count[x] >= x)
                  Observation: Assertions are correct, but they can not catch a buggy implementation.                                    Observation: Assertions are correct.
                    count = Counter(lst)                                                                            assert (lst.count(return_value) >= return_value
            Turn 4:
                    assert return_value == -1 or all(return_value >= x                                   Turn 6:      and return_value == max(x for x in set(lst) if lst.count(x) >= x
           Solution        for x, freq in count.items() if freq >= x)                                   Solution        and x > 0) or (return_value == -1 and not any(lst.count(x) >= x
                  Observation: Assertions are correct, but they can not catch a buggy implementation.                   and x > 0 for x in set(lst))))
                                                        ...

Figure 1: Example of task #69 from EvalPlus with postconditions from Single-pass (nl2postcond (Endres et al.,
2024)), Greedy Multi-turn, and Exploratory Multi-turn. Blue blocks show model reasoning (omitted for all but
turn 5 of Exploratory Multi-turn for space reason), red, orange, and gray blocks show submission and exploration
attempts, and feedback. ✓: correct and complete postcondition, ×: otherwise.


process where it internalizes the feedback, reflects                                                       proving over the baseline nl2postcond by 26.1% in
on prior attempts with the observations on the re-                                                         correctness and 2.48X in completeness. The aver-
sults of the intermediate turns, and gradually con-                                                        age increase in completeness after one submission
verges toward a more accurate and comprehensive                                                            attempt of Exploratory Multi-Turn is 1.67X higher
postcondition. This feedback to LLMs can be im-                                                            than that of Greedy. The postconditions from S PEC -
plicit (e.g., soundness and/or completeness signals)                                                       M IND can detect 1.42X-2.14X more bugs than
or explicit (e.g., un-caught mutants). Greedy is a                                                         nl2postcond in FixEval with less costs. Our data
special case of Exploratory Multi-turn where no                                                            and code can be found at (Spe, 2026).
intermediate turn of exploration is allowed and the
model submits the final result after each attempt.                                                         2         Illustration
While Greedy is an iterative algorithm enhanced                                                           The function search in Fig. 1 takes a non-empty list
with history, Exploratory Multi-turn is an algorith-                                                      of positive integers as input and returns the great-
mically defined, iterative, exploratory reasoning                                                         est integer in the list whose frequency is greater
framework with 1) explicit exploration-submission                                                         than or equal to its value; if no such integer exists,
decoupling, 2) structured history-aware reasoning,                                                        it returns −1. In the ground truth, the complete
3) best-so-far tracking, and 4) autonomous stopping                                                       specification for this function must contain all of
(Section 2). Those characteristics give Exploratory                                                       the following sub-conditions:
Multi-turn the following key benefits:                                                                       (1) the return value is either −1 or a positive
   Deeper Code Comprehension: By interacting                                                              integer from the input list;
with feedback and refining its outputs over multiple                                                         (2) if the return value is positive, its frequency
turns, the model is encouraged to form a more                                                             must be greater than or equal to its value;
semantically grounded understanding of the code                                                              (3) if the return value is positive, it must be the
logic, rather than relying on superficial patterns.                                                       greatest integer satisfying the frequency condition;
   Autonomous Reasoning: In the autonomous ex-                                                               (4) if the return value is −1, no integer in the list
ploration, the model determines when to stop,                                                             satisfies the frequency condition.
which introduces a degree of self-awareness and                                                              We applied the state-of-the-art, LLM-based,
decision-making on the sufficiency of its answer.                                                         postcondition generation tool, nl2postcond (Endres
   We evaluated our model on EvalPlus (Endres                                                             et al., 2024) on the code of the search function.
et al., 2024) and FixEval (Anjum Haque et al.,                                                            nl2postcond leverages a single-pass prompting strat-
2023). Exploratory Multi-turn achieves 99.4% cor-                                                         egy to request the LLM used in this example,
rectness and 89.6% completeness, relatively im-                                                           Llama 4 Scout, to generate the postcondition.
   A candidate postcondition can be evaluated us-         == -1 or ..., a pattern that can be trivially satisfied
ing two metrics: correctness and completeness (En-        by faulty code returning -1 in all cases.
dres et al., 2024). Correctness refers to if the post-       Exploratory Multi-turn. In real-world learning,
condition passes all test cases in the given test set.    students rarely solve complex problems correctly
A postcondition is correct if it holds true for all       in a single attempt. Effective learners instead ask
test cases that the original function passes (no con-     clarifying questions, explore partial solutions, and
tradiction to the behavior in test cases). However,       test their understanding before committing to a fi-
correctness alone is not sufficient as a trivial post-    nal answer. This differs from blindly retrying after
condition like "True" is always correct but useless       a “try again” signal, and from single-pass solving
in bug detection. Completeness, referring to dis-         without refinement. Inspired by this, we propose
criminative power, measures how informative the           Exploratory Multi-turn for postcondition genera-
postcondition is. It reflects the postcondition’s abil-   tion, where the LLM acts not as a code-to-code gen-
ity to detect incorrect versions of the function (e.g.,   erator but as an active reasoner. It autonomously
mutated code). This is done by checking if the            explores intermediate reasoning paths, probes par-
postcondition can "catch" mutants (i.e., detecting        tial answers, internalizes feedback, and decides
bugs), i.e., the modified versions that behave differ-    when it has enough evidence to produce the result.
ently. Formally, completeness is the percentage of           In the example, similar to Greedy Multi-turn,
mutants that can be distinguished (i.e., rejected) by     the first three attempts correctly generated condi-
the postcondition when used with the test suite.          tions (1)–(3). In the 4th attempt, a minor change
   From our experiment on the above example, we           triggered an AssertionError. Unlike Greedy, which
made the following observations:                          often stagnates on the same incomplete assertion,
   1. The state-of-the-art LLM-based, single-pass         Exploratory Multi-Turn broke from its prior pattern
approach, nl2postcond (Endres et al., 2024), gen-         and shifted direction in the fifth attempt. The model
erated the postconditions ensuring that the return        explicitly noted: “The assertion failed, which
value is either -1 or a positive integer from the input   means our current postconditions might not be suffi-
list, thereby satisfying the condition (1). However,      cient or accurate. Let’s revisit and refine them... We
none of the conditions (2)–(4) was generated.             can use a different approach... Let’s iterate over...”.
   2. Feedback-driven Multi-Turn Approaches.              This shift produced a postcondition that covered
Prior work suggests that the feedback helps LLMs          condition (4) and discarded the overly permissive
ground their generations more effectively (Gehring        pattern assert return_value == -1 or .... It finally
et al., 2025). Building on this, we integrated            generated the correct and complete postcondition,
feedback into the process by explicitly indicating        suggesting that Exploratory Multi-Turn helps es-
which generated constraints were incorrect or non-        cape local optima and improves completeness.
discriminative. Thus, we propose the following               Specifically, our key design ideas are as follows:
two feedback-driven Multi-Turn approaches:                   1. Exploration-submission decoupling: we ex-
   Greedy Multi-Turn. The first one is a feedback-        plicitly decouple exploration (hypothesis probing
guided, test-driven iterative prompting for refine-       via <assert>) from commitment (<solution>). Only
ment. We employed a simple feedback mechanism             submission attempts update the best-so-far candi-
in which the LLM repeatedly attempted to produce          date, while exploratory turns gather semantic evi-
a correct postcondition until all test cases passed       dence. This separation transforms the process from
and a desired completeness is reached, using feed-        feedback-guided heuristic search into structured
back from previous failed attempts. This feedback         exploring with hypothesis probing.
includes either binary pass/fail signals or syntax           2. Best-so-far tracking: S PEC M IND uses a
errors. The iterative process enabled the model to        completeness threshold, best-so-far tracking, and a
progressively cover the condition (1) in the first        model-controlled stop decision that can terminate
attempt, the condition (2) in the second, and the         when the threshold is met, returns diminish, or the
condition (3) in the third, eventually combining          attempt budget is reached. This ensures the final
them into a single assertion by the fourth attempt.       output is the strongest candidate observed (best-so-
Within the 12-attempt limit, the model focused pre-       far), rather than simply the last attempt.
dominantly on these three conditions, but failed to          3. History-aware reasoning: In iterative prompt-
generate the condition (4). The generated asser-          ing, each attempt is often independent or loosely
tions consistently began with assert return_value         conditioned on prior error messages. To support
                                                                Require: Function code f , test suite T , completeness threshold τ
exploration, S PEC M IND maintains a structured his-            Ensure: Final postcondition ϕfinal
tory buffer that is embedded into the prompt. This               1: H ← [ ]                                       ▷ History buffer
enables explicit reflection on prior mistakes and be-            2: ϕbest ← ∅, sbest ← 0.0
                                                                 3: while True do
havioral gaps during historical exploration, rather              4:     prompt ← constructPrompt(f, H)
than relying solely on the immediate feedback.                   5:     (ϕ, type) ← LLM.generate(prompt)                         ▷
                                                                    type ∈ {explore, submit}
   4. Autonomous stopping mechanism: S PEC -                     6:     Append (ϕ, type) to H              ▷ Update history buffer
M IND allows the model to determine termination                  7:     if type = submit then                     ▷ score ∈ [0, 1]
                                                                 8:         (f eedback, score) ← evaluateFeedback(ϕ, T )
via LLM, based on improvement trajectory and                     9:         annotateLast(H, f eedback, score)         ▷ Feedback
completeness threshold. This introduces a self-                 10:          if score > sbest then
regulated search dynamic absent in retry-based it-              11:              ϕbest ← ϕ, sbest ← score ▷ Update best solution
                                                                    only on submission attempts
erative prompting paradigms.                                    12:     if LLM.decidesToStop(H, sbest ) then
                                                                13:          return ϕbest     ▷ When the termination condition is
3    Problem Formulation                                            met; return best-so-far

Given a function f :I → O, where I and O are the                Figure 2: Feedback-Driven Exploratory Multi-Turn Algo-
                                                                rithm with Completeness Threshold
input and output domains, the goal is to synthesize
a postcondition ϕ : I × O → {true, false} that
characterizes the correct behavior of f .                           Threshold τ ∈ [0, 1]: A predefined target com-
   The postcondition ϕ is a logical predicate that              pleteness level. The loop continues until the model
must hold for any input-output pair (i, o) where                achieves this threshold or chooses to stop early.
o = f (i). Formally: ∀i ∈ I, ϕ(i, f (i)) = true.
                                                                    Best-so-far Tracking: The algorithm keeps track
In practice, ϕ is often expressed as an assertion or
                                                                of the best postcondition submitted by the model
a condition over program variables after execution.
                                                                so far (based on the highest completeness score)
The goal is to infer such a ϕ automatically, using
                                                                and returns it if the loop ends prematurely.
the following inputs: a function’s source code, a
finite test suite T = {(i1 , o1 ), . . . , (in , on )}, and a       LLM.decidesToStop. At each attempt, the model
set of mutants M of the original f . Two evaluation             may choose to submit a postcondition once it is
criteria for a synthesized postcondition ϕ include              confident after a process of exploration and refine-
   Correctness (Corr.): The postcondition must                  ment or reaches a maximum number of attempts.
hold on all known correct executions captured in                The submitted postcondition is then evaluated and,
the test suite: ∀(ij , oj ) ∈ T , ϕ(ij , oj ) = true.           if it improves upon the Best-so-far Tracking and
The postcondition must reject incorrect variants.               satisfies the completeness threshold, the algorithm
   Completeness (Comp.): Given a set of program                 triggers LLM.decidesToStop to terminate and return
mutants M = {f1′ , f2′ , . . . , fm
                                  ′ }, the completeness         the best postcondition generated so far.
of a postcondition measures the proportion of mu-                   Details. Fig. 2 outlines Exploratory Multi-turn
tants for which the postcondition fails:
                                                                for a given function. We treat inference as an
              |{fk′ ∈ M | ∃i ∈ I, ϕ(i, fk′ (i)) = false}|       iterative process guided by structured feedback:
 Comp(ϕ) =
                                |M|
                                                                S PEC M IND lets the LLM refine candidates until
   Correctness ensures consistency with the given               the completeness criterion is met or the submis-
code, while completeness reflects the specifica-                sion budget is exhausted. We maintain a history
tion’s robustness in identifying deviations/defects.            buffer H that stores all attempted postconditions
Objective of Postcondition Inference/Genera-                    (exploratory and submitted) with metadata (line 1),
tion. Given a function f , a test suite T , and a               and a best-so-far record (ϕbest , sbest ) tracking the
set of mutants M, the objective of S PEC M IND is               strongest submitted candidate (line 2).
to synthesize a postcondition ϕ that:                               Each iteration synthesizes a prompt from the
   1. Achieves full correctness over T ;                        function code f and prior feedback in H (line 4),
   2. Maximizes completeness over M;                            encouraging the model to reflect on earlier mistakes.
                                                                It then produces either an exploratory refinement or
4    Exploratory Multi-turn Algorithm
                                                                a submission. Submitted candidates are evaluated
Algorithm supporting information. Complete-                     by a feedback engine that returns qualitative out-
ness Score s ∈ [0, 1]: Each feedback evaluation re-             comes (e.g., pass/fail) and a normalized complete-
turns a quantitative measure of completeness (e.g.,             ness score s ∈ [0, 1] (line 6). We log the submis-
how much of the expected behavior is covered).                  sion, feedback, and score in H (line 9), and update
 Prompt Template
                                                                               PromptTemplate is a function that formats code, prior
 Objective: Verify correctness of a Python function using its natural lan-
 guage description and implementation. Your goal is to write symbolic          generations, and critiques into an LLM-readable
 postconditions — Python assert statements that validate specific behavioral   input. A prompt template is shown in Fig. 3.
 properties of the function’s return value.
 Turn Structure: Each turn must begin with a <think> block containing             Our evolving structure allows the LLM to inter-
 reasoning about purpose, constraints, and edge cases. After this reasoning,
 choose exactly one of the following actions:                                  nalize past mistakes and progressively refine its
    •    <assert> – Propose a single candidate assertion for testing.          output. Unlike static prompt, our dynamic history-
     → Triggers an <observation> with feedback.                                aware formulation fosters deeper reasoning and re-
  • <solution> – Provide the final refined postcondition.
                                                                               moves the need to reset the context between turns.
 You will now be given the function {function_name}:
                                                                                  Feedback Mechanism. Our feedback mecha-
 {function_signature}
     {function_docstring}                                                      nism serves two goals: 1) guiding the LLM’s refine-
     {function_implementation}
                                                                               ment with actionable signals, and 2) providing a
 Let’s begin                                                                   quantitative estimate of each candidate’s semantic
    Turn 1: (ϕ1 , feedback1 )
                                                                               completeness. Each LLM-generated postcondition
    <think> ... </think> <assert> ϕ1 </assert> <observation> feedback1
    </observation>                                                             ϕt is evaluated against the code’s observed behav-
 ...                                                                           ior, typically using a test suite and a set of mutants.
    Turn t−1: (ϕt−1 , feedbackt−1 )                                               The feedback feedbackt includes: (a) a correct-
    <think> ... </think> <assert> ϕt−1 </assert> <observation> feedbackt−1
    </observation>                                                             ness indicator–whether ϕt holds on all tests; and
                                                                               (b) a completeness score–the fraction of mutants
Figure 3: Template prompt for Greedy and Exploratory.                          “caught” by ϕt (i.e., faulty variants that violate the
    The highlighted <assert> action is specific to Exploratory Multiturn.      postcondition). If the completeness threshold is not
                                                                               reached within the attempt budget, we also return
(ϕbest , sbest ) if s > sbest (lines 10–11). Termina-                          the remaining uncaught mutants as additional feed-
tion is controlled by LLM.decidesToStop (line 12),                             back. We append the prompt–feedback pair to the
which stops when a candidate reaches threshold τ ,                             history Ht to steer subsequent generations toward
returns diminish, or the maximum attempts µ is                                 remaining behavioral gaps. If available, we can use
reached; the algorithm returns ϕbest (line 13).                                symbolic execution or verification backends; oth-
   Overall, we use the LLM as an interactive rea-                              erwise, correctness is checked empirically on tests
soner that incorporates feedback and self-regulates                            and completeness is measured via mutant catching.
the search, reducing hallucination and overgeneral-                            Grounding prompts in correctness and complete-
ization. Greedy Multi-turn (not shown) repeatedly                              ness yields an informative refinement loop.
prompts the LLM to resubmit until all tests pass or
                                                                               6   Empirical Evaluation
until τ or the attempt budget is reached.
                                                                               We aim to answer the following questions:
5        Prompt Design and Feedback
                                                                                  RQ1. [Effectiveness–Efficiency]. How effective
   Prompt Design. We adopt a modular and evolv-                                and efficient is our tool in postcondition inference?
ing prompt template that reflects the model’s cur-                                RQ2. [Reasoning]. How does S PEC M IND with
rent understanding, errors in prior attempts, and                              Exploratory Multi-turn perform reasoning?
the functional structure of the code under analysis.                              RQ3. [Stratifying Results]. How does S PEC -
The base prompt includes the full code of the tar-                             M IND with feedback perform on hard cases?
get function and, optionally, a high-level natural                                RQ4. [Cost Efficiency]. How efficient is S PEC -
language description (if available). Moreover, each                            M IND in token costs and actual costs?
subsequent prompt incorporates an interaction his-                                RQ5. [Bug Detection]. How effective is S PEC -
tory consisting of prior postconditions, associated                            M IND in bug detection?
feedback, and explicit instructions for refinement.                            Benchmarks. We selected EvalPlus as our dataset
Formally, let the function be denoted f , and let the                          as it was used in nl2postcond (Endres et al., 2024).
interaction history up to turn t be represented as:                            It has 164 Python problems, each with a function
        Ht = [(ϕ1 , feedback1 ), (ϕ2 , feedback2 ), . . . ,                    stub, textual description, reference implementation,
                                                                               and validation tests (Liu et al., 2023). EvalPlus
                    (ϕt−1 , feedbackt−1 )]
                                                                               updates the HumanEval benchmark (Chen et al.,
The prompt at turn t, denoted Promptt , is synthe-                             2021), containing the same problems but with more
sized as: Promptt = PromptTemplate(f, Ht ) where                               extensive test suites (≈ 775 test cases per problem).
Table 1: Postcondition Generation Effectiveness with Llama 4 (RQ1). τ : completeness threshold, µ: max turns; R.
Sampl.: run nl2postcond µ independent times, Subs: avg submissions, Corr: correctness, Comp.: Completeness.
Method                     Config.      Attempts      Avg Subs      Corr. Comp. Method                    Config.   Attempts       Avg Subs    Corr. Comp.
                                        min-max       min-max                                                       min-max        min-max
                                                                                R.Sampl. w. nl2postcond             6.4 (1 - 8)    6.4 (1 - 8) 84.9% 48.4%
nl2postcond                                                                                             τ = 70
                          Single-pass      1.0           1.0        73.3% 36.0% Greedy                              3.8 (1 - 8)    3.8 (1 - 8) 96.9% 78.6%
 (Baseline)                                                                                             µ=8
                                                                                Exploratory                         5.7 (2 - 8)    1.2 (1 - 4) 93.1% 83.7%
R.Sampl. w. nl2postcond                 3.0 (1 - 4) 3.0 (1 - 4)     79.2% 41.2% R.Sampl. w. nl2postcond τ = 70      9.0 (1 - 12)   9.0 (1 - 12) 84.9% 51.9%
                           τ = 50
Greedy                                  2.3 (1 - 4) 2.3 (1 - 4)     93.7% 69.2% Greedy                  µ = 12
                                                                                                                    5.3 (1 - 12)   5.3 (1 - 12) 100.0% 78.4%
                           µ=4
Exploratory                             3.8 (3 - 4) 1.0 (1 - 2)     84.3% 70.6% Exploratory                         6.5 (3 - 12)   1.4 (1 - 6) 97.5% 85.9%
R.Sampl. w. nl2postcond                 5.1 (1 - 8) 5.1 (1 - 8) 84.9% 47.9%     R.Sampl. w. nl2postcond         3.7 (1 - 4)   3.7 (1 - 4)     79.2%   41.5%
                           τ = 50                                                                       τ = 90
Greedy                                  2.9 (1 - 8) 2.9 (1 - 8) 96.9% 70.7%     Greedy                          3.2 (1 - 4)   3.2 (1 - 4)     96.9%   76.4%
                           µ=8                                                                          µ=4
Exploratory                             5.7 (3 - 8) 1.2 (1 - 3) 93.1% 81.5%     Exploratory                     3.8 (3 - 4)   1.1 (1 - 2)     84.3%   71.6%
R.Sampl. w. nl2postcond                 6.9 (1 - 12) 6.9 (1 - 12) 84.9% 50.9%   R.Sampl. w. nl2postcond         7.1 (1 - 8)   7.1 (1 - 8)     84.9%   48.9%
                           τ = 50                                                                       τ = 90
Greedy                                  3.3 (1 - 12) 3.3 (1 - 12) 100.0% 75.0%  Greedy                          5.1 (1 - 8)   5.1 (1 - 8)     99.4%   81.1%
                           µ = 12                                                                       µ=8
Exploratory                             6.5 (3 - 12) 1.3 (1 - 5) 98.1% 86.4%    Exploratory                     6.2 (3 - 8)   1.4 (1 - 4)     94.3%   83.2%
R.Sampl. w. nl2postcond                 3.5 (1 - 4)   3.5 (1 - 4)   79.2% 41.3% R.Sampl. w. nl2postcond τ = 90 10.3 (1 - 12) 10.3 (1 - 12)    84.9%   52.6%
                           τ = 70
Greedy                                  2.6 (1 - 4)   2.6 (1 - 4)   95.6% 68.6% Greedy                  µ = 12
                                                                                                                6.2 (1 - 12) 6.2 (1 - 12)     98.7%   85.8%
                           µ=4                                                                                                                99.4%   89.6%
Exploratory                             3.8 (3 - 4)   1.0 (1 - 2)   84.3% 70.4% Exploratory                     7.2 (3 - 12) 1.7 (1 - 6)




Baselines. We chose as baseline the state-of-the-                                  erage and submits the resulting postcondition from
art nl2postcond, with access to the reference imple-                               1.0 to 1.7 times. As seen, on average, S PEC M IND
mentation. nl2postcond was shown to outperform                                     uses a small number of attempts and does not need
prior approaches such as TOGA (Dinella et al.,                                     to use up the attempt budget. However, the highest
2022) and Daikon (Ernst et al., 1999). We used                                     numbers of attempts reach the maximum budget.
Llama 4 Scout as the underlying LLMs for the                                       That means that it needs to use all the budget of
tools in all experiments.                                                          attempts in hard cases (see RQ3). The results run
Evaluation Metrics. We use two key metrics:                                        on GLM 4.7 is shown in Appendix A.1.
1) Correctness refers to whether the postcondi-
                                                                                    6.1.1     Correctness
tion passes all test cases in the given test suite;
2) Completeness is the percentage of mutants dis-                                  We first study the effect of the attempt budget µ.
tinguishable (i.e., rejected) by the postcondition                                 With µ=4, both Exploratory and Greedy Multi-turn
given the test suite. We used the same mutant set                                  outperform nl2postcond. Under the most relaxed
from nl2postcond for a fair comparison.                                            setting (τ =50, µ=4), Greedy reaches 93.7% cor-
   To calculate the efficiency over submission at-                                 rectness in 2.3 attempts on average, a 20-point
tempts, we P define the efficiency score in a setting                              gain over nl2postcond (73.3%). Exploratory also
as E = N1 N
                      completeness scorei                                          improves over nl2postcond, but achieves 84.3% due
               i=1 number of submission turnsi , where N
is the number of functions in the dataset. The ef-                                 to limited exploratory turns. Exploratory benefits
ficiency score E measures the average increase of                                  more from larger µ: the average number of func-
completeness after one submission attempt.                                         tions with correct postconditions rises from 139.0
                                                                                   (µ = 4) to 153.7 (µ=8) and 161.3 (µ=12). Greedy
6.1    Effectiveness and Efficiency (RQ1)
                                                                                   improves less with µ. On average, increasing µ by
As seen in Table 1, with Exploratory achieving                                     4 yields a 6.8% correctness gain for Exploratory
peak performance at τ =90, µ=12 (99.4% correct-                                    versus 2.1% for Greedy, as Exploratory can probe
ness, 89.6% completeness) while requiring an av-                                   more candidates before submission (Section 6.2).
erage of 7.2 attempts and 1.7 submissions per task.                                   For comparison, we also evaluate Random Sam-
nl2postcond achieves 73.3% correctness and 36.0%                                   pling with nl2postcond, i.e., querying the LLM in-
completeness using a single attempt.                                               dependently µ times with early stopping when τ
   Across most settings, for both Greedy and Ex-                                   is met. Random Sampling achieves 79.2% cor-
ploratory Multi-turn, despite allowing a higher                                    rectness at (τ =50, µ=4) and peaks at 84.9% under
maximum number of attempts, the average number                                     the strictest setting (τ =90, µ=12). Under the same
of attempts range between 2.3-7.2, with the correct-                               setting, Greedy and Exploratory reach 98.7% and
ness increasing from 84.3% to 99.4% and complete-                                  99.4% correctness, using 6.2 and 7.2 attempts on
ness increasing from 69.2% to 89.6%. The higher                                    average, compared to 10.3 for Random Sampling.
maximum number of attempts allowed, the higher
correctness and completeness for Greedy and Ex-                                     6.1.2     Completeness
ploratory Multi-turn. For Exploratory Multi-turn,                                   Exploratory Multi-turn outperforms Greedy in all
among 3.8-7.2 attempts, it explores 3.5 times on av-                                settings except τ =90, µ=4. The smallest complete-
                                                            To categorize reasoning behaviors, we first
                                                         use an LLM to cluster reasoning texts in five
                                                         batches (200–226 each), producing distinct, non-
                                                         overlapping categories. We then manually consol-
                                                         idate and refine these into seven observable cat-
                                                         egories. Finally, we use an LLM to classify all
                                                         reasoning texts into the seven categories for consis-
                                                         tent labeling, and manually validate the results by
  Figure 4: Efficiency for configurations with µ=12.
                                                         inspecting a random 10% sample per category.
                                                            Table 2 presents the categories of S PEC M IND’s
ness gap is at τ =50, µ=4 (70.6% vs. 69.2%), and         reasoning along with their descriptions, frequen-
the largest at τ =50, µ=12 (86.4% vs. 75.0%). Our        cies, and representative examples. The most fre-
tool’s lowest completeness is 68.6% at τ =70, µ=4,       quent behavior is Refine Assertions, appearing in
far above single-pass nl2postcond (36.0%), high-         419 reasonings, where the model improves existing
lighting the benefit of multi-turn refinement for        assertions to make them more concise and com-
more discriminative specifications. Random Sam-          prehensive. Typical phrases include: “To refine
pling improves with more attempts (e.g., at τ =90,       our postconditions...”, “A more accurate property
41.5% with µ=4 to 52.6% with µ=12) but remains           might be...”, or “The current postcondition does
well below S PEC M IND’s worst case (68.6%). We          not accurately reflect...”. The second most frequent
also analyze completeness scores across submis-          category is Verify Function Behavior, with 270
sion attempts. See Appendix A.3 for details.             reasonings. In this category, the model proposes
                                                         assertions to verify functional properties.
6.1.3    Efficiency
                                                            Reasoning Patterns. Fig. 5 shows the occur-
Fig. 4 shows that Exploratory Multi-turn is more
                                                         rences of 7 categories across attempts for all sam-
submission-efficient than Greedy, peaking at 80.0%
                                                         ples, excluding unsolvable cases. Return Value
vs. 47.7%. That is, the average completeness gain
                                                         Type and Range and Verify Function Behavior con-
per submission is 1.67× higher for Exploratory.
                                                         centrate in the first attempt (49 and 94 instances).
Raising the completeness threshold increases final
                                                         Check Base Cases and Check Edge Cases also ap-
completeness but reduces efficiency: from τ =50
                                                         pear early, peaking at the 2nd (8) and 3rd (17) at-
to τ =90, efficiency drops by 5.7% for Exploratory
                                                         tempts, indicating that the model initially explores
and 14.5% for Greedy, suggesting that more dis-
                                                         return values and base/edge cases. Submit Final So-
criminative postconditions require more explorato-
                                                         lution occurs from attempts 3–12 and peaks around
ries. Compared to Random Sampling, Exploratory
                                                         attempts 5–6, consistent with Exploratory requir-
is more efficient (80.0% vs. 26.3%) and degrades
                                                         ing about 5–6 attempts per case. Refine Assertions
less as τ increases. As τ rises from 50-70-90, Ex-
                                                         is frequent between attempts 2–6, peaking at at-
ploratory achieves 3.04×, 4.17×, and 5.59× the
                                                         tempts 3–4 (74 and 68), suggesting the model re-
efficiency of Random Sampling. See a case study
                                                         fines before submitting. Postcondition Combina-
comparing two approaches in Appendix A.4.
                                                         tion emerges at attempt 3 and peaks at attempt 5
6.2     S PEC M IND’s Reasoning at Each Attempt          (14), indicating it combines exploratory results be-
                                                         fore submitting. See Appendix A.5 for an example.
This experiment analyzes S PEC M IND’s reasoning
behavior across attempts, focusing on Exploratory
                                                         6.3   Stratifying Results on Hard Cases (RQ3)
Multi-turn because each attempt may depend on
prior exploratory or submission turns (Greedy            We analyze the hardest cases: the model exhausts
Multi-turn contains only submission turns). We use       the attempt budget without reaching the complete-
τ =70 since τ =50 often stops too early and τ =90        ness threshold, under the strict setting τ =90, µ=12.
frequently exhausts the budget without meeting the       This yields 23 hard cases out of 159: one with no
threshold. We set µ=12 to observe behavior over          correct postcondition and 22 with completeness
more attempts. We analyze all natural-language           < 90 (average 56.2%). In the standard setting, we
reasoning texts produced per attempt (enclosed by        provide only binary feedback: whether a postcon-
<think>. . . </think>), totaling 1,026 instances; each   dition passes all tests (correctness) and whether it
case has 6.5 reasoning instances on average.             catches all mutants (completeness). For these hard
Table 2: Exploratory Multi-turn’s reasoning behavior categories with descriptions, frequencies, examples (RQ2).
   Reasoning Category          Description                               Freq Example
   Return Value Type & Range Checking the type and range of the return      77   "The assertion I proposed checks if . . . To further
                             value.                                              strengthen the assertion, I can check if the return
                                                                                 value is a list of strings. . . "
   Check Base Cases            Checking the base cases of a function.       32   "Let’s check if the function returns the correct val-
                                                                                 ues for the base cases. For n = 0, the return value
                                                                                 should be 0. . . "
   Check Edge Cases          Adding postconditions checking edge 63              "Let’s consider the case where the input number is
                             cases: empty inputs or boundary values.             an integer. The decimal part should be exactly 0. . . "
   Postcondition Combination Combining multiple postconditions into 59           "Both properties seem to be correct. . . Let’s com-
                             one.                                                bine these insights into a single assertion. . . "
   Refine Assertions         Refining assertions to make them more 419           "The combined assertion seems correct and compre-
                             concise, meaningful, or comprehensive.              hensive. However, let’s make it more concise and
                                                                                 readable. . . "
   Verify Function Behavior    Adding assertions to verify correctness of 270    "The first assertion checks. . . Next, we want to
                               calculations.                                     check that the return value, when added to apples
                                                                                 and blues, equals the total number of fruits. . . "
   Submit Final Solution       Submitting assertions as the final solution 129   "The assertion is now concise and readable. It cor-
                               without further refining.                         rectly checks. . . , let’s consider submitting it..."




  (a) Ret. Val. Type/Range       (b) Check Base Cases            (c) Check Edge Cases                     (d) Postcond. Comb.




      (e) Refine Assertions                  (f) Verify Function Behavior                            (g) Submit A Solution
        Figure 5: Frequency distribution analysis from seven reasoning categories across attempts (RQ2)


cases, we add richer feedback by returning a                  Random Sampling uses an average of 302 to-
randomly-selected uncaught mutant and asking the              kens per instance (min=19 and max=1,666 tokens),
model for refinement. We then extend the budget               which is much lower than the usages of Multi-turn
by 4 attempts (µ=16) to measure the impact.                   approaches. Greedy uses an average of 5,752 to-
   With enhanced feedback, correct postconditions             kens per instance (ranging from 266 to 25,909),
increase to 22/23 and average completeness rises              while Exploratory uses an average of 8,299 tokens
to 85.1%; the model reaches the threshold in                  per instance (ranging 1,313–29,956).
14/22 correct cases. Applying binary feedback first              The higher token usage per instance for our tool
(τ =90, µ=12) and using enhanced feedback only                stems from two factors: (1) inclusion of Chain-of-
for the remaining hard cases with 4 extra attempts            Thought tokens (nl2postcond does not have CoT)
improves performance to 99.7% correctness and                 and (2) inclusion of the history buffer (Equation 1).
92.0% completeness (vs. 99.4% and 89.6% with bi-              However, the actual costs remain modest: 0.18
nary feedback only). If we use enhanced feedback              cent and 0.25 cent per instance for Greedy and
from the start with τ =90, µ=12, the model pro-               Exploratory, respectively (τ =90, µ=12).
duces correct postconditions for 21/23 hard cases;               This high token usage is a tradeoff for more
among 22 correct cases, 9 reach the completeness              bug detection. Fig. 6 displays the trends for Ran-
target, with overall average completeness 90.6%.              dom Sampling, Greedy, and Exploratory when
                                                              the completeness threshold increases (µ=50,70,90).
6.4   LLM Token Usage & Cost Analysis (RQ4)
                                                              When µ increases, each approach uses more to-
Under the strictest configuration (completeness               kens due to more attempts. However, across thresh-
threshold τ =90, maximum number of turns µ=12),               olds, both Greedy and Exploratory catch more mu-
                                                                Table 3: Bug Detection Performance.
                                                                        µ=3               µ=5            µ = 10
                                                         Approach
                                                                              % dist.         % dist.         % dist.
                                                                    % Corr.           % Corr.         % Corr.
                                                                               bugs            bugs            bugs
                                                        R.Sampl. w/
                                                                    66.41     16.15   76.82   22.40   86.20    27.86
                                                        nl2postcond
                                                        Greedy      59.38     24.74   67.71   30.73   87.24    38.02
                                                        Exploratory 79.69     34.64   90.10   36.98   95.57    39.58



                                                        rationale is as follows. Using the associated test
                                                        suite for a problem in the dataset to ensure cor-
Figure 6: Token Usages & Numbers of Caught Mutants      rectness, as we run a model on the correct version,
                                                        the resulting postcondition ϕ acts as an oracle of
                                                        intended behavior of the code. When we apply
tants/bugs than Random Sampling. Greedy caught
                                                        that oracle to the executions of the buggy solution,
24.7 mutants with 3,065.9 tokens per instance (≈
                                                        any deviation from the intended relation between
0.0029 cent/bug) and 27.8 mutants with 5,752 to-
                                                        inputs and outputs will violate the postcondition ϕ
kens per instance (≈ 0.0047 cent/bug). Exploratory
                                                        (i.e., there exists an input i such that postcondition
achieved the highest bug detection performance,
                                                        ϕ(i,buggy_function(i))=false). This is the same
reaching 29.2 mutants with 6110.5 tokens per in-
                                                        completeness definition: postconditions “reject” a
stance (≈ 0.0046 cent/bug) and peaking at 30.9
                                                        faulty variant (mutant); here, the buggy version
with 8,299 tokens per instances (≈ 0.0058 cen-
                                                        plays the role of a single mutant. Thus, the gener-
t/bug). Random Sampling caught 17.6 mutants
                                                        ated postcondition can be used in detecting future
with 298 tokens. Using more tokens (3,182 tokens)
                                                        bugs in regression testing. We used the same crite-
with maximum allowed attempts µ=170, its num-
                                                        ria in nl2postcond for a bug-discriminating postcon-
ber of detected bugs reaches to 23.3 (1.4 bugs less
                                                        dition. We consider a generated postcondition to be
compared to 24.7 bugs by Greedy with 3k tokens),
                                                        bug-discriminating if it satisfies the following: (1)
with 0.0082 cent/bug (2.83X cost more). Random
                                                        The postcondition passes all the trigger and regres-
Sampling has higher cost as it generates more out-
                                                        sion tests, on the correct version of a function. (2)
put tokens (which cost more), whereas our tool
                                                        The postcondition fails a trigger test or a regression
requires more input tokens but produces fewer out-
                                                        test on the buggy version (Endres et al., 2024).
puts. In brief, with lower attempts, Exploratory
                                                        Experimental Results. As seen in Table 3, both
incurs lower costs with more detected bugs.
                                                        Greedy and Exploratory approaches are able to
6.5   Usefulness in Bug Detection (RQ5)                 distinguish more buggy versions than the baseline
                                                        nl2postcond being run µ times independently (for a
Experimental Methodology. We adapted an eval-
uation approach used in nl2postcond (Endres et al.,     fair comparison). When µ=3 submission attempts,
2024) and TOGA (Dinella et al., 2022). The evalu-       the baseline distinguished 16.15% of the buggy ver-
ation idea is that it aims to evaluate if a model can   sions from the correct ones, with passing 66.41%
generate postconditions that distinguish between        of test cases. In contrast, Greedy distinguishes
correct and buggy code regarding regression and         relatively 53.19% more buggy versions with pass-
triggering test cases in regression testing. We used    ing 59.38% of test cases. Importantly, Exploratory
FixEval (Anjum Haque et al., 2023), a benchmark         catches 2X more buggy versions than the baseline
comprising buggy and correct submission code to         with 34.64% of passing test cases.
competitive programming problems. From the full            As we increased the number of submission at-
test set of 243k Python buggy-correct pairs, we         tempts to µ=5, all approaches performed better
filtered out runtime errors and kept 157,355 pairs.     in terms of both correctness and number of distin-
We then randomly selected 384 bugs, ensuring 95%        guishable bugs. As µ=10, Exploratory performs the
statistical significance. We evaluated the effective-   best as it distinguished 39.58% of the buggy ver-
ness of postconditions that a user could have used      sions, i.e., better than both the baseline and Greedy.
to catch a bug as the postconditions fail on the           An example of the bugs detected by the postcon-
buggy version, and succeed on the correct one. The      ditions from S PEC M IND is shown in Section A.6.
Limitations & Threats to Validity                          for Programming Problems . In 2023 IEEE/ACM In-
                                                           ternational Workshop on Automated Program Repair
Our evaluation is conducted on EvalPlus (Endres            (APR), pages 11–18, Los Alamitos, CA, USA. IEEE
et al., 2024), which may not reflect the full diver-       Computer Society.
sity of real-world codebases. While EvalPlus is          Ivan Beschastnikh, Yuriy Brun, Sigurd Schneider,
a large public benchmark with postcondition an-             Michael Sloan, and Michael D. Ernst. 2011. Lever-
notations and enables a fair comparison against             aging existing instrumentation to automatically infer
nl2postcond on its original setting, it primarily con-      invariant-constrained models. In Proceedings of the
                                                           19th Symposium on Foundations of Software Engi-
sists of Python tasks of moderate complexity. Thus,         neering, ESEC/FSE ’11, pages 267–277. ACM.
generalization to larger systems, other program-
ming languages, or other forms of specifications         Arianna Blasi, Alberto Goffi, Konstantin Kuznetsov,
                                                           Alessandra Gorla, Michael D. Ernst, Mauro Pezzè,
is not guaranteed. In addition, we evaluate mainly         and Sergio Delgado Castellanos. 2018. Translating
GPT-family models; performance may differ for              code comments to procedure specifications. In Pro-
other model families or future versions.                   ceedings of the 27th ACM SIGSOFT International
   Our results may also be influenced by the pre-          Symposium on Software Testing and Analysis, ISSTA
                                                           2018, page 242–253, New York, NY, USA. Associa-
training knowledge of LLMs. Although we cannot             tion for Computing Machinery.
fully rule out exposure to similar code during pre-
training, our evaluation centers on generating new       Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
                                                          Henrique Ponde De Oliveira Pinto, Jared Kaplan,
postconditions and validating them via execution,
                                                          Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
which is unlikely to be explained by memorization.        Brockman, and 1 others. 2021. Evaluating large
   We operationalize postcondition quality using          language models trained on code. arXiv preprint
two proxies: correctness (passing the test suite) and     arXiv:2107.03374.
completeness (rejecting mutants). Both inherit limi-     Patrick M. Cousot, Radhia Cousot, Francesco Logozzo,
tations from their backends: correctness is bounded        and Michael Barnett. 2012. An abstract interpre-
by test coverage, and completeness depends on the          tation framework for refactoring with application to
quality and representativeness of the mutant set. If       extract methods with contracts. In Proceedings of the
                                                           ACM International Conference on Object Oriented
the tests or mutants fail to capture realistic behav-      Programming Systems Languages and Applications,
iors or defects, our metrics may overestimate true         OOPSLA ’12, page 213–232, New York, NY, USA.
specification quality or bug-detection usefulness.         Association for Computing Machinery.
   Finally, our conclusions depend on experimental       Elizabeth Dinella, Gabriel Ryan, Todd Mytkowicz, and
choices such as the attempt budget µ and com-               Shuvendu K. Lahiri. 2022. Toga: a neural method
pleteness threshold τ . While we evaluate across            for test oracle generation. In Proceedings of the 44th
multiple configurations to reduce sensitivity to any        International Conference on Software Engineering,
                                                            ICSE ’22, page 2130–2141, New York, NY, USA.
single setting, other datasets, feedback designs, or        Association for Computing Machinery.
hyperparameter choices could change the observed
trade-offs between effectiveness and efficiency.         Madeline Endres, Sarah Fakhoury, Saikat Chakraborty,
                                                          and Shuvendu K. Lahiri. 2024. Can large language
                                                          models transform natural language intent into formal
                                                          method postconditions? Proc. ACM Softw. Eng.,
References                                                1(FSE).
2026.   Specmind code.        https://github.com/        Dawson Engler, David Yu Chen, Seth Hallem, Andy
  thaiminhpv/SpecMind.                                     Chou, and Benjamin Chelf. 2001. Bugs as deviant
                                                           behavior: A general approach to inferring errors
Juan Altmayer Pizzorno and Emery D. Berger. 2025.          in systems code. In Proceedings of the Eighteenth
  Coverup: Effective high coverage test generation for     ACM Symposium on Operating Systems Principles,
  python. Proc. ACM Softw. Eng., 2(FSE).                   SOSP’01, pages 57–72. ACM.
Glenn Ammons, Rastislav Bodík, and James R. Larus.       Michael D. Ernst, Jake Cockrell, William G. Griswold,
  2002. Mining specifications. In Proceedings of the       and David Notkin. 1999. Dynamically discovering
  29th ACM SIGPLAN SIGACT Symposium on Princi-             likely program invariants to support program evolu-
  ples of Programming Languages, POPL ’02, pages           tion. In Proceedings of the 21st International Con-
  4–16. ACM.                                               ference on Software Engineering, ICSE’99, pages
                                                           213–224. ACM.
Md Mahim Anjum Haque, Wasi Uddin Ahmad, Is-
 mini Lourentzou, and Chris Brown. 2023. FixE-           Pranav Garg, Daniel Neider, P. Madhusudan, and Dan
 val: Execution-based Evaluation of Program Fixes          Roth. 2016. Learning invariants using decision trees
  and implication counterexamples. In Proceedings           Benjamin Livshits and Thomas Zimmermann. 2005.
  of the 43rd Annual ACM SIGPLAN-SIGACT Sym-                  Dynamine: finding common error patterns by min-
  posium on Principles of Programming Languages,              ing software revision histories. In Proceedings of
  POPL ’16, page 499–512, New York, NY, USA. As-              the 10th European Software Engineering Conference
  sociation for Computing Machinery.                          Held Jointly with 13th ACM SIGSOFT International
                                                              Symposium on Foundations of Software Engineering,
Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard               ESEC/FSE-13, page 296–305, New York, NY, USA.
  Mella, Taco Cohen, and Gabriel Synnaeve. 2025.              Association for Computing Machinery.
  RLEF: Grounding code LLMs in execution feedback
  with reinforcement learning. In Forty-second Inter-       Antonio Mastropaolo, Nathan Cooper, David Nader
  national Conference on Machine Learning.                    Palacio, Simone Scalabrino, Denys Poshyvanyk,
                                                              Rocco Oliveto, and Gabriele Bavota. 2023. Using
Ted Kremenek, Paul Twohey, Godmar Back, Andrew                transfer learning for code-related tasks. IEEE Trans-
  Ng, and Dawson Engler. 2006. From uncertainty to            actions on Software Engineering, 49(4):1580–1598.
  belief: inferring the specification within. In Proceed-
  ings of the 7th Symposium on Operating Systems De-        Facundo Molina, Pablo Ponzio, Nazareno Aguirre, and
  sign and Implementation, OSDI ’06, page 161–176,            Marcelo Frias. 2021. Evospex: An evolutionary al-
  USA. USENIX Association.                                    gorithm for learning postconditions. In Proceedings
                                                              of the 43rd International Conference on Software En-
Shuvendu K. Lahiri, Sarah Fakhoury, Aaditya Naik,             gineering, ICSE ’21, page 1223–1235. IEEE Press.
  Georgios Sakkas, Saikat Chakraborty, Madanlal
  Musuvathi, Piali Choudhury, Curtis von Veh, Jee-          Tung Thanh Nguyen, Hoan Anh Nguyen, Nam H. Pham,
  vana Priya Inala, Chenglong Wang, and Jianfeng Gao.         Jafar M. Al-Kofahi, and Tien N. Nguyen. 2009.
  2023. Interactive code generation via test-driven user-     Graph-based mining of multiple object usage pat-
  intent formalization. Preprint, arXiv:2208.05950.           terns. In Proceedings of the Symposium on Founda-
                                                              tions of Software Engineering, ESEC/FSE ’09, pages
Larissa Laich, Pavol Bielik, and Martin Vechev. 2020.         383–392. ACM.
  Guiding program synthesis by learning to generate
  examples. In International Conference on Learning         Rahul Pandita, Xusheng Xiao, Hao Zhong, Tao Xie,
  Representations.                                            Stephen Oney, and Amit Paradkar. 2012. Inferring
                                                              method specifications from natural language api de-
Cuong Chi Le, Cuong Duc Van, Tung Duy Vu, Minh                scriptions. In Proceedings of the 34th International
  V. T. Pham, Hoang Nhat Phan, Huy N. Phan, and               Conference on Software Engineering, ICSE ’12, page
  Tien N. Nguyen. 2026. TestWeaver: Execution-                815–825. IEEE Press.
  aware, feedback-driven regression testing generation
  with large language models. In Proceedings of the         Kexin Pei, David Bieber, Kensen Shi, Charles Sutton,
  48th IEEE/ACM International Conference on Soft-             and Pengcheng Yin. 2023. Can large language mod-
  ware Engineering (ICSE ’26), Rio de Janeiro, Brazil.        els reason about program invariants? In Proceedings
  To appear.                                                  of the 40th International Conference on Machine
                                                              Learning, volume 202 of Proceedings of Machine
Caroline Lemieux, Jeevana Priya Inala, Shuvendu K.            Learning Research, pages 27496–27520. PMLR.
  Lahiri, and Siddhartha Sen. 2023. Codamosa: Es-
  caping coverage plateaus in test generation with pre-     Michael Pradel and Thomas R. Gross. 2009. Auto-
  trained large language models. In Proceedings of the        matic generation of object usage specifications from
  45th International Conference on Software Engineer-         large method traces. In Proceedings of the 2009
  ing, ICSE ’23, page 919–931. IEEE Press.                    IEEE/ACM International Conference on Automated
                                                              Software Engineering, ASE ’09, pages 371–382.
Wen-Ding Li, Darren Yan Key, and Kevin Ellis. 2025.           IEEE Computer Society.
 Toward trustworthy neural program synthesis. In
 ICLR 2025 Third Workshop on Deep Learning for              Murali Krishna Ramanathan, Ananth Grama, and
 Code.                                                       Suresh Jagannathan. 2007. Static specification in-
                                                             ference using predicate mining. In Proceedings of
Zhenmin Li and Yuanyuan Zhou. 2005. Pr-miner: Au-            the 2007 ACM SIGPLAN Conference on Program-
  tomatically extracting implicit programming rules          ming Language Design and Implementation, PLDI
  and detecting violations in large software code. In        ’07, pages 123–134. ACM.
  Proceedings of the 13th Symposium on Foundations
  of Software Engineering, ESEC/FSE-13, pages 306–          Sharon Shoham, Eran Yahav, Stephen Fink, and Marco
  315. ACM.                                                   Pistoia. 2007. Static specification mining using
                                                              automata-based abstractions. In Proceedings of the
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Ling-         2007 International Symposium on Software Testing
   ming Zhang. 2023. Is your code generated by chat-          and Analysis, ISSTA ’07, page 174–184, New York,
   GPT really correct? rigorous evaluation of large lan-      NY, USA. Association for Computing Machinery.
   guage models for code generation. In Thirty-seventh
   Conference on Neural Information Processing Sys-         Lin Tan, Ding Yuan, Gopal Krishna, and Yuanyuan
   tems.                                                      Zhou. 2007. /*icomment: bugs or bad comments?*/.
  In Proceedings of Twenty-First ACM SIGOPS Sym-           Jianan Yao, Gabriel Ryan, Justin Wong, Suman Jana,
  posium on Operating Systems Principles, SOSP ’07,           and Ronghui Gu. 2020. Learning nonlinear loop in-
  page 145–158, New York, NY, USA. Association for            variants with gated continuous logic networks. In
  Computing Machinery.                                        Proceedings of the 41st ACM SIGPLAN Conference
                                                              on Programming Language Design and Implemen-
Lin Tan, Yuanyuan Zhou, and Yoann Padioleau. 2011.            tation, PLDI 2020, page 106–120, New York, NY,
  acomment: mining annotations from comments and              USA. Association for Computing Machinery.
  code to detect interrupt related concurrency bugs. In
  Proceedings of the 33rd International Conference         Hao Zhong, Tao Xie, Lu Zhang, Jian Pei, and Hong
  on Software Engineering, ICSE ’11, page 11–20,             Mei. 2009a. Mapo: Mining and recommending api
  New York, NY, USA. Association for Computing               usage patterns. In Proceedings of the 23rd European
  Machinery.                                                 Conference on ECOOP 2009 — Object-Oriented Pro-
Shin Hwei Tan, Darko Marinov, Lin Tan, and Gary T.           gramming, pages 318–343. Springer-Verlag.
  Leavens. 2012. @tcomment: Testing javadoc com-
                                                           Hao Zhong, Lu Zhang, Tao Xie, and Hong Mei. 2009b.
  ments to detect comment-code inconsistencies. In
                                                             Inferring resource specifications from natural lan-
  Proceedings of the 2012 IEEE Fifth International
                                                             guage api documentation. In Proceedings of the 24th
  Conference on Software Testing, Verification and Val-
                                                             IEEE/ACM International Conference on Automated
  idation, ICST ’12, page 260–269, USA. IEEE Com-
                                                             Software Engineering, ASE ’09, page 307–318, USA.
  puter Society.
                                                             IEEE Computer Society.
Suresh Thummalapenta and Tao Xie. 2009. Alattin:
  Mining alternative patterns for detecting neglected      Yu Zhou, Ruihang Gu, Taolue Chen, Zhiqiu Huang,
  conditions. In Proceedings of the 2009 IEEE/ACM            Sebastiano Panichella, and Harald Gall. 2017. Ana-
  International Conference on Automated Software En-         lyzing apis documentation and code to detect direc-
  gineering, ASE ’09, pages 283–294. IEEE Computer           tive defects. In 2017 IEEE/ACM 39th International
  Society.                                                   Conference on Software Engineering (ICSE), pages
                                                             27–37.
Michele Tufano, Dawn Drain, Alexey Svyatkovskiy,
  Shao Kun Deng, and Neel Sundaresan. 2021. Unit
  test case generation with transformers and focal con-
                                                           A     Appendix
  text. Preprint, arXiv:2009.05617.
                                                           A.1    Results of S PEC M IND with GLM-4.7
Michele Tufano, Dawn Drain, Alexey Svyatkovskiy,           Table 4 shows the results as we used GLM-4.7 as
  and Neel Sundaresan. 2022. Generating accurate
  assert statements for unit test cases using pretrained   the underlying model. As seen, Exploratory also
  transformers. In Proceedings of the 3rd ACM/IEEE         achieves peak performance at τ =90, µ=12 (99.37%
  International Conference on Automation of Software       correctness, 87.57% completeness) with the same
 Test, AST ’22, page 54–64, New York, NY, USA.             trend as the results using Llama Scout in Table 1.
  Association for Computing Machinery.
Vasudev Vikram, Caroline Lemieux, Joshua Sunshine,         A.2    Related Work
  and Rohan Padhye. 2024. Can large language mod-
  els write good property-based tests?    Preprint,
                                                           Researchers have proposed automated approaches
  arXiv:2307.04346.                                        that fall into three categories: program analysis-
                                                           based, data mining-based, and large language
Andrzej Wasylkowski and Andreas Zeller. 2009. Min-
  ing temporal specifications from object usage. In Pro-
                                                           model (LLM)-based.
  ceedings of the 2009 IEEE/ACM International Con-            Program analysis-based methods use dynamic
  ference on Automated Software Engineering, ASE           or static techniques. Dynamic approaches (Am-
  ’09, pages 295–306. IEEE Computer Society.               mons et al., 2002; Beschastnikh et al., 2011; Ernst
Andrzej Wasylkowski, Andreas Zeller, and Christian         et al., 1999) infer properties by monitoring execu-
  Lindig. 2007. Detecting object usage anomalies. In       tions but depend heavily on test coverage. Static
  Proceedings of the Symposium on Foundations of           analyses (Shoham et al., 2007; Engler et al., 2001;
  Software Engineering, ESEC-FSE ’07, pages 35–44.
  ACM.
                                                           Kremenek et al., 2006; Ramanathan et al., 2007;
                                                           Wei et al., 2011) and abstract interpretation (Cousot
Yi Wei, Carlo A. Furia, Nikolay Kazmin, and Bertrand       et al., 2012) avoid this dependency but often pro-
   Meyer. 2011. Inferring better contracts. In Proceed-
   ings of the 33rd International Conference on Soft-
                                                           duce conservative or imprecise specifications due
   ware Engineering, ICSE ’11, pages 191–200. ACM.         to high false-positive rates. Several approaches at-
                                                           tempted to generate specification by analyzing API
Chadd C. Williams and Jeffrey K. Hollingsworth. 2005.
  Automatic mining of source code repositories to im-
                                                           documentation or code comments (Pandita et al.,
  prove bug finding techniques. IEEE Trans. Softw.         2012; Tan et al., 2007, 2011, 2012; Blasi et al.,
  Eng., 31(6):466–480.                                     2018; Zhong et al., 2009b; Zhou et al., 2017).
Table 4: Postcondition Generation Effectiveness with GLM-4.7 (RQ1). τ : completeness threshold, µ: max turns; R.
Sampl.: run nl2postcond µ independent times, Subs: avg submissions, Corr: correctness, Comp.: Completeness.
Method                     Config.      Attempts   Avg Subs    Corr.   Comp. Method                  Config.   Attempts    Avg Subs    Corr.   Comp.
                                        min-max    min-max                                                     min-max     min-max
                                                                                R.Sampl. w. nl2postcond        6.4 (1 - 8)  6.4 (1 - 8) 77.97% 31.24%
nl2postcond                                                                                             τ = 70
                          Single-pass      1.0        1.0     46.0%      12.4% Greedy                          3.8 (1 - 8)  3.8 (1 - 8) 91.82% 70.55%
 (Baseline)                                                                                             µ=8
                                                                                Exploratory                    5.7 (2 - 8)  1.2 (1 - 4) 98.11% 85.46%
R.Sampl. w. nl2postcond                 3.0 (1 - 4) 3.0 (1 - 4) 69.8% 25.13% R.Sampl. w. nl2postcond τ = 70 9.0 (1 - 12) 9.0 (1 - 12) 80.62% 40.59%
                           τ = 50
Greedy                                  2.3 (1 - 4) 2.3 (1 - 4) 84.74% 65.14% Greedy                    µ = 12
                                                                                                               5.3 (1 - 12) 5.3 (1 - 12) 93.26% 74.51%
                           µ=4
Exploratory                             3.8 (3 - 4) 1.0 (1 - 2) 92.2% 81.68% Exploratory                       6.5 (3 - 12) 1.4 (1 - 6) 99.12% 84.31%
R.Sampl. w. nl2postcond                 5.1 (1 - 8) 5.1 (1 - 8) 77.97% 31.24% R.Sampl. w. nl2postcond          3.7 (1 - 4)  3.7 (1 - 4) 69.84% 25.13%
                           τ = 50                                                                       τ = 90
Greedy                                  2.9 (1 - 8) 2.9 (1 - 8) 88.05% 66.48% Greedy                           3.2 (1 - 4)  3.2 (1 - 4) 86.79% 67.65%
                           µ=8                                                                          µ=4
Exploratory                             5.7 (3 - 8) 1.2 (1 - 3) 97.48% 85.3% Exploratory                       3.8 (3 - 4)  1.1 (1 - 2) 93.08% 80.79%
R.Sampl. w. nl2postcond                 6.9 (1 - 12) 6.9 (1 - 12) 80.62% 40.59% R.Sampl. w. nl2postcond        7.1 (1 - 8)  7.1 (1 - 8) 77.97% 31.24%
                           τ = 50                                                                       τ = 90
Greedy                                  3.3 (1 - 12) 3.3 (1 - 12) 90.21% 69.94% Greedy                         5.1 (1 - 8)  5.1 (1 - 8) 86.16% 69.68%
                           µ = 12                                                                       µ=8
Exploratory                             6.5 (3 - 12) 1.3 (1 - 5) 98.43% 83.21% Exploratory                     6.2 (3 - 8)  1.4 (1 - 4) 98.74% 84.93%
R.Sampl. w. nl2postcond                 3.5 (1 - 4) 3.5 (1 - 4) 69.84% 25.13% R.Sampl. w. nl2postcond τ = 90 10.3 (1 - 12) 10.3 (1 - 12) 80.62% 40.59%
                           τ = 70
Greedy                                  2.6 (1 - 4) 2.6 (1 - 4) 86.16% 67.34% Greedy                    µ = 12
                                                                                                               6.2 (1 - 12) 6.2 (1 - 12) 87.42% 69.41%
                           µ=4                                                                                 7.2 (3 - 12) 1.7 (1 - 6) 99.37% 87.57%
Exploratory                             3.8 (3 - 4) 1.0 (1 - 2) 97.48% 82.75% Exploratory



   Data mining-based approaches extract common
API usage patterns from large codebases (Li and
Zhou, 2005; Livshits and Zimmermann, 2005;
Zhong et al., 2009a). They identify call pairs,
sequences, and finite-state models (Wasylkowski
et al., 2007; Williams and Hollingsworth, 2005;
Thummalapenta and Xie, 2009; Nguyen et al.,
2009; Pradel and Gross, 2009; Wasylkowski and
Zeller, 2009). While useful for API usages, they                              Figure 7: Trend of completeness score from our seleted
rarely infer semantic specifications such as pre/-                            cases in EvalPlus, using Exploratory Multi-turn with
postconditions (Ramanathan et al., 2007).                                     configuration τ =90 and µ=12
   In general, ML approaches for specification
generation have advanced in multiple directions,                              while Speculyzer(Li et al., 2025) enumerates likely
including postcondition inference (Endres et al.,                             properties and candidate inputs with LLMs, but
2024), synthesizing test oracles (Dinella et al.,                             uses them primarily as heuristics to guide code gen-
2022; Mastropaolo et al., 2023; Tufano et al., 2022),                         eration rather than to ensure correctness or com-
improving test coverage (Lemieux et al., 2023; Alt-                           pleteness of specifications. Beyond input–output
mayer Pizzorno and Berger, 2025; Le et al., 2026),                            properties, machine learning has also been applied
and generating unit tests (Lahiri et al., 2023; Tu-                           to infer intermediate specifications, such as pro-
fano et al., 2021). These techniques rely on dif-                             gram invariants (Garg et al., 2016; Laich et al.,
ferent types of inputs. AthenaTest (Tufano et al.,                            2020; Yao et al., 2020; Pei et al., 2023).
2021) generates both the input and the oracle of a
unit test directly from the implementation of the                             A.3      Behavioral Patterns in Completeness
focal method, while TOGA generates only the or-                                        Across Submissions
acle (Dinella et al., 2022). TiCoder (Lahiri et al.,                          To analyze the change in completeness score across
2023) leverages LLMs to produce both inputs and                               submission attempts, we consider the strictest set-
outputs based on a natural language description of                            ting with completeness threshold τ = 90 and max-
user intent.                                                                  imum number of turns µ = 12. We plot the com-
   While these methods target the production of                               pleteness score over submission attempts for eight
concrete test cases (and sometimes oracles), our                              selected solvable cases (i.e., cases where the final
work instead focuses on generating postcondi-                                 solution is correct and satisfies the completeness
tions. Similarly, EvoSpex (Molina et al., 2021)                               target) in Fig. 7. These cases are representative of
applies evolutionary learning to infer functional in-                         typical behaviors observed in our dataset and are
put–output relationships. More recent efforts have                            selected here for illustration.
explored property-based specifications. Vikram                                   The selected tasks require between two and four
et al. (Vikram et al., 2024) propose leveraging                               submission attempts. All eight cases show an in-
LLMs to generate property-based tests (PBTs),                                 crease in completeness from the first submission to
Table 5: Exploratory Multi-turn’s trajectory for function #159 in EvalPlus dataset. It requires implementing the
function eat, which calculates the total number of carrots eaten and the number of carrots remaining, given number
(carrots already eaten), need (carrots that need to be eaten), and remaining (carrots in stock).
      Att.   Category                   Reasoning (ret=return_value, rem=remaining, num=number.)
       1     Verify Func. Behavior The function ‘eat‘ calculates... The function returns... Key constraints and edge cases:... To verify the
                                   correctness of the function, we need to write symbolic postconditions that check these properties.
                                   » assert isinstance(ret, list) && len(ret) == 2 && isinstance(ret[0], int) &&
                                   isinstance(ret[1], int)
       2     Check Edge Cases      The first assertion checks... However, we need to add more assertions to cover other properties of the function.
                                   Let’s consider the case when ‘need‘ is less than or equal to ‘remaining‘... We should also consider the case
                                   when ‘need‘ is greater than ‘remaining‘...
                                   » assert need <= rem || (need > rem && ret[1] == 0)
       3     Refine Assertions     The second assertion checks if... should also check if the total number of carrots eaten is correct in both...
                                   » assert (need <= rem && ret[0] == num + need) || (need > rem && ret[0] == num + rem)
       4     Postcondition Combin- ... let’s try to combine them into a single assertion...
             ing
                                   » assert (need <= rem && ret[1] == rem - need) || (need > rem && ret[1] == 0)
                                   » assert (need <= rem && ret[0] == num + need) || (need > rem && ret[0] == num + rem)
       5     Refine Assertions     ... let’s refine our assertions to make them more concise and meaningful...
                                   » assert (need <= rem && ret[0] == num + need && ret[1] == rem - need) || (need > rem &&
                                   ret[0] == num + rem && ret[1] == 0)
       6     Submit Final Solution We have several assertions that check different properties of the function... Let’s try to finalize our solution by
                                   submitting a single assertion that combines all the checks...
                                   » assert (need <= rem && ret == [num + need, rem - need]) || (need > rem && ret == [num
                                   + rem, 0])




the final submission that reaches the completeness                               sertion, while Greedy directly submits the second,
threshold. Across all 164 tasks, we observe that                                 more complex constraint.
23 cases show no change in completeness between
consecutive submissions (e.g., case #90 and case                                    In the second attempt, Exploratory explores the
#161), indicating early convergence. In contrast,                                second property and explicitly notes its potential
18 cases temporarily drop to zero completeness                                   relevance. Greedy, however, reverts to the first
due to the submission of an incorrect postcondition                              property and briefly mentions the case n ≤ 2 in its
before recovering in later attempts (e.g., case #10,                             reasoning but dismisses it as irrelevant, despite its
not shown). The earliest correct submission occurs                               semantic importance.
at attempt 3 in 11 cases (e.g., case #112), suggest-                               In the third attempt, Exploratory combines
ing that Exploratory Multi-turn often identifies a                               the two properties and explicitly incorporates
correct core postcondition early and incrementally                               the n ≤ 2 case. In contrast, Greedy submits
improves its discriminative power.                                               assertions targeting specific input values (e.g.,
A.4   A Case Study of Exploratory vs. Greedy                                     n = 2, n = 3). Notably, its reasoning states
      Multi-turn                                                                 get_max_triples(n)=0, while the submitted assertion

To illustrate the behavioral differences between                                 enforces get_max_triples(n)=1; this mismatch hap-
Greedy and Exploratory Multi-turn, Fig. 8 presents                               pens to pass tests but reflects unstable reasoning.
a detailed analysis of case #147 from EvalPlus                                      In the final attempt, Exploratory refines its ear-
under τ = 50 and µ = 4. The task defines the                                     lier reasoning by adding the missing n ≤ 2
function get_max_triples(n), which computes the                                  sub-condition and submits a complete postcondi-
number of valid triples in an array a of length n,                               tion. Greedy instead submits a new constraint,
where a[i] = i × i − i + 1, such that the sum of                                 return_value <= n**3 // 6, which is weaker than a
the triples is divisible by 3. If n ≤ 2, the function                            stricter constraint it had already produced earlier,
returns False.                                                                   resulting in a correct yet incomplete specification.
   Exploratory Multi-turn submits its final solution
at attempt #4, whereas Greedy Multi-turn submits a                                  Overall, Exploratory Multi-turn produces a cor-
candidate postcondition at every attempt by design,                              rect and complete postcondition using a single sub-
with its best-performing one appearing in attempt                                mission and three exploratory steps. It systemati-
#1. In the first attempt, both approaches identify                               cally explores sub-conditions and composes them
two key properties: (1) the return value should be a                             into a final specification. In contrast, Greedy Multi-
non-negative integer, and (2) it should be bounded                               turn identifies a partially correct condition early but
by the total number of possible triples. Exploratory                             fails to refine it into a comprehensive postcondition
probes the first property through an exploratory as-                             within the same budget.
                          Exploratory Multi-Turn                                                              Greedy Multi-Turn
             The function get_max_triples(n) calculates... The return                 The function get_max_triples(n) calculates the number of
             value represents the count of valid triples, so it should                triples (a[i], a[j], a[k]) in an array a of length n,
  Think      be a non-negative integer... should also be an integer        Think      where a[i] = i * i - i + 1... The return value of the
             that does not exceed the total number of possible triples                function represents a count of triples and must be a non-
             in an array of length n...                                               negative integer. We also note that...
 Explore     assert isinstance(return_value, int) and return_value >= 0   Solution    assert return_value <= n * (n - 1) * (n - 2) // 6
                          Observation: Assertions are correct.                     Observation: Assertions are correct, but they can not catch a buggy implementation.
             Given that the array a is generated based on... since it's               We also note that for n <= 2, the function returns False,
             counting valid triples, the value should be less than or                 which is not a valid count of triples... we will focus on
  Think                                                                    Think
             equal to the total possible combinations of triples in the               the case where n > 2...
             array, which is...
 Explore     assert return_value <= n * (n - 1) * (n - 2) // 6            Solution    assert isinstance(return_value, int) and return_value >= 0
                          Observation: Assertions are correct.                     Observation: Assertions are correct, but they can not catch a buggy implementation.
             ...for n <= 2, the function returns False, which seems to                Considering the function's behavior for different values
  Think      be an edge case handling... but expressing this directly                 of n... the return value should be equal to 0 when n = 3
                                                                           Think
             in a postcondition without replicating the function...                   or n = 4 if the implementation is correct for small
             assert isinstance(return_value, int) and return_value >= 0               inputs...
 Explore
             and return_value <= n * (n - 1) * (n - 2) // 6               Solution    assert get_max_triples(3) == 0 or get_max_triples(4) == 1
                          Observation: Assertions are correct.                     Observation: Assertions are correct, but they can not catch a buggy implementation.
             The function get_max_triples(n) has a specific behavior                  ...that the return value grows in a reasonable way as n
  Think      for n <= 2... A comprehensive postcondition should check                 increases. Specifically, we can check that the return
             for these cases explicitly.                                   Think
                                                                                      value is less than or equal to n^3 / 6, which is a rough
             assert (n <= 2 and return_value is False) or (n > 2 and                  upper bound on the number of triples.
             isinstance(return_value, int) and return_value >= 0 and      Solution    assert return_value <= n**3 // 6
 Solution    return_value <= n * (n - 1) * (n - 2) // 6)
                                                                                   Observation: Assertions are correct, but they can not catch a buggy implementation.




Figure 8: A comparison between Exploratory Multi-turn and Greedy Multi-turn for case #147 from EvalPlus: the
figure illustrates S PEC M IND’s outputs (τ =50 and µ=4), model’s reasoning are given in the blue blocks, submission
attempts are given in the red blocks, and exploration attempts are enclosed in the orange blocks. The feedback is
shown in the gray boxes. ✓: correct and complete postcondition, ×: otherwise.


A.5         An Example Trajectory of Reasoning                            in the submission of a complete postcondition.
            Categories
                                                                          A.6          An Example of Bugs Detected by
Table 5 presents a representative reasoning trajec-                                    Conditions generated by S PEC M IND
tory produced by Exploratory Multi-turn for case
#159 from the EvalPlus dataset. This task requires                        Let us use an example of the correct code (not
implementing the function eat, which computes                             shown), aiming to solve the task: given a starting
the total number of carrots eaten and the number                          point and a mapping of each point to the next, find
of carrots remaining, given number (already eaten                         the position reached after K steps.
carrots), need (carrots to be eaten), and remaining                          1. When running the baseline nl2postcond in
(carrots in stock).                                                       Random Sampling µ independent times, the LLM
   The trajectory begins with Verify Function Be-                         does not learn from its past experience, leading
havior, where the model describes the function’s                          to repeated mistakes. For example, the postcondi-
overall behavior and proposes assertions checking                         tions produced at the attempts #2 and #5 are the
basic structural properties of the return value. It                       same even though the one at attempt #2 is incorrect.
transitions to Check Edge Cases, explicitly reason-                       This approach exhausted all 10 attempts without
ing about conditional scenarios such as whether                           catching the bug.
need exceeds remaining. The model enters Refine                              2. For Greedy approach, the LLM demonstrated
Assertions, improving earlier checks by strengthen-                       the ability to learn from past mistakes. For example,
ing semantic constraints on the return values.                            in attempt #2, it proposed to check if the output is
   The reasoning then moves to Postcondition Com-                         a positive number:
bination, where previously explored assertions are                             assert isinstance(return_values[0], int) and
consolidated. This is followed by another Refine                          return_values[0] > 0
Assertions step, reflecting iterative improvement to-                        Getting the correctness feedback, it simplified
ward a more concise and comprehensive specifica-                          the condition to only check if the output is an
tion. Finally, the trajectory concludes with Submit                       integer: assert isinstance(return_values[0], int).
Final Solution, where the model submits a single                          However, none of the 10 retries can catch the bug.
assertion that captures all explored conditions.                             3. Exploratory Multi-turn started with a simple
   Overall, this illustrates a systematic progression                     postcondition checking if the output is an integer.
through reasoning categories, starting from high-                         After getting the feedback on its incorrect condi-
level function understanding, moving to edge case                         tion, it expanded the condition to a correct one
analysis and iterative refinement, and culminating                        to check that the output string can be converted to
an integer.
  We also observed that Exploratory was able to
refine the postcondition. For example, at attempt
#3, it checks that the output index is within the
bounds of the sequence:
  N, K = map(int, lines[0].split()); sequence =
list(map(int, lines[1].split()));
  assert 1 <= int(return_values[0]) <= N
   After getting the positive feedback, it contin-
ued to refine the post condition to a stricter one
and eventually submitted the correct one at the at-
tempt #5. Its reasoning texts are as follows: "The
current postcondition checks if the output index is
within the bounds ... However, to make the post-
condition more specific and meaningful, I will con-
sider...Given that the sequence represents a linked
list with possible cycles, the output value should be
an element in the sequence." The final condition
caught the buggy version as the output is not an
element of the sequence.
  N, K = map(int, lines[0].split()); sequence =
list(map(int, lines[1].split()))
  assert int(return_values[0]) in sequence

A.7   Usage of LLM Assistance
We used large language models (LLMs) to aid in
polishing the writing and improving clarity. All
research ideas, experiments, and conclusions are
the work of the authors.
