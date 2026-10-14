                                                      Programmers Are Poor and Overconfident Judges of
                                                                LLM-Generated Assertions
                                                                 Zhanna Kaufman                                                                Yuriy Brun
                                                           zhannakaufma@umass.edu                                                        brun@cs.umass.edu
                                                       University of Massachusetts Amherst                                       University of Massachusetts Amherst
                                                                Amherst, MA, USA                                                          Amherst, MA, USA

                                                                   Adithya Murali                                                          Madeline Endres
                                                            adithyamurali@cs.wisc.edu                                                    mendres@umass.edu
                                                         University of Wisconsin–Madison                                         University of Massachusetts Amherst
                                                                 Madison, WI, USA                                                         Amherst, MA, USA
                                        Abstract                                                                       this burden, researchers have proposed shifting developer review
                                        Code comprehension and code review are already critically im-                  toward smaller reliability-oriented artifacts such as tests [17, 41],
                                        portant software engineering tasks, and the rising use of AI code              specifications [40, 81], or assertions [16]. For example, Endres et al.
                                        generation tools is only increasing that importance. Generative AI             propose using LLMs to generate executable assertions that allow
                                        has the possibility of supporting these activities, for example by             developers to review intended program behavior rather than the
                                        augmenting code with assertions and natural-language explana-                  full implementation, reducing the amount of code that must be
arXiv:2607.08885v1 [cs.SE] 9 Jul 2026




                                        tions describing code behavior. However, little is known about how             inspected while enabling run-time validation of generated code.
                                        effective such support may be. We conduct a controlled experiment              Similarly, Lahiri envisions a future in which LLMs help formalize
                                        with 86 Python programmers and a follow-up think-aloud study to                user intent through behavioral artifacts such as tests, assertions,
                                        examine developers’ ability to assess the correctness and complete-            and formal specifications [40]. By formalizing intended program
                                        ness of generated assertions of varying quality, and to investigate            behavior, such artifacts have the potential to help developers de-
                                        how natural-language explanations influence these assessments.                 termine if generated code captures their intent and, in some cases,
                                        While programmers can somewhat accurately judge correct asser-                 validate that intent at run time.
                                        tions (74% accuracy), they perform poorly when shown incorrect                     A key assumption underlying these approaches is that develop-
                                        assertions (49% accuracy), despite reporting similar levels of confi-          ers can accurately evaluate machine-generated reliability artifacts.
                                        dence in both judgments. This difference in judgment accuracy is               Yet this assumption remains largely unexamined. While a growing
                                        statistically significant (𝑝 < 0.001): the odds of a developer accu-           body of work studies developers’ interactions and understanding of
                                        rately judging a correct assertion was nearly three times higher than          LLM-generated code (see Hou et al. [28], Table 10), comparatively
                                        the odds of accurately judging an incorrect assertion (OR = 2.94).             little empirical evidence exists regarding how effectively developers
                                        Surprisingly, natural-language explanations of assertions provided             evaluate generated specifications, tests, or assertions. This uncer-
                                        no overall benefit. Furthermore, low-quality explanations could                tainty extends to one of the most common mechanisms used to
                                        impair specification assessment accuracy (𝑝 = 0.037, 𝑂𝑅 = 0.58)                support comprehension of such artifacts: natural-language expla-
                                        while simultaneously increasing developer confidence (𝑝 = 0.005,               nations [31, 48]. Modern LLMs routinely generate comments and
                                        3.99/5 vs. 4.25/5). Our findings suggest that, contrary to common              explanations alongside code and specifications. However, like the
                                        assumptions, AI assistance may not improve the reliability of code             code itself, such explanations may be incorrect, incomplete, vague,
                                        comprehension and review. More broadly, our findings highlight                 or irrelevant [11, 36]. Consequently, it is unknown whether natural-
                                        the importance of helping developers evaluate machine-generated                language explanations improve programmer judgment or instead
                                        reliability artifacts, in addition to generating them.                         introduce additional sources of error.
                                                                                                                           In this paper, we investigate two questions: (1) How effective are
                                                                                                                       programmers at judging the correctness and completeness of LLM-
                                        1   Introduction                                                               generated assertions about code? and (2) How does the presence
                                        Generative AI tools have transformed software engineering, and are             and quality of natural-language comments affect these judgments?
                                        now a routine part of virtually every aspect of development includ-                We focus on postcondition assertions for several reasons. First,
                                        ing code generation [63], architectural design [34], debugging [63],           postconditions possess well-defined formal semantics, allowing us
                                        and verification [20]. This makes code comprehension and code                  to rigorously characterize metrics such as correctness and com-
                                        review, already important parts of the software engineering life-              pleteness. Second, LLMs are fairly proficient (but not yet perfect) at
                                        cycle, even more important, as humans are asked to be part of the              generating valid assertions from documentation and have been ex-
                                        loop, reviewing, adapting, and adopting automatically generated                plicitly proposed as part of a human-in-the-loop software reliability
                                        code [55, 78]. However, reviewing code is difficult, time-consuming,           workflow [16]. This allows us to study a close-to-ideal setting, in
                                        and cognitively demanding [5, 6]. Programmers often struggle to                which LLMs are generally capable of generating useful assertions,
                                        understand non-self-authored code [74], including LLM-generated                but are not sufficiently reliable to eliminate the need for careful
                                        code [69], as such code may be incorrect or misaligned with user in-           human review. Finally, postconditions can express rich behavioral
                                        tent [17, 77], which can be difficult to fix in practice [80]. To reduce
                                                                                                                   1
properties while remaining compact enough to support controlled                We conclude by discussing implications for AI-assisted software
experimental evaluation.                                                    reliability, suggesting that future tools should move beyond gen-
   We conduct a controlled experiment with 86 Python program-               erating reliability artifacts to helping developers verify that they
mers spanning a range of professions and experiences. We construct          faithfully capture intended program behavior.
a corpus of Python functions paired with LLM-generated postcondi-
tion assertions and natural-language comments, extending datasets           2   Motivating Example
used in prior work on assertion generation [10, 16, 45]. Participants       Consider Juan, a developer who is asked to write and test the func-
were shown a function and postcondition, then asked to assess               tion has_close_elements(numbers: List[float], threshold:
whether the postcondition correctly captured the function’s be-             float) (this example comes from the HumanEval [10] dataset).
havior and how completely it did so. To evaluate how explanation            Juan is given a natural-language docstring description of the de-
quality affects developers’ reasoning about generated reliability           sired functionality:
artifacts, we included four types of comments that described the
assertions: correct, incorrect, under-specified, and over-specified.    1   " Check if in given list of numbers , are any two numbers
                                                                             closer to each other than given threshold . "
We complemented the controlled experiment with a think-aloud
study with 10 developers. This qualitative analysis allows us to               Juan decides to use an LLM to generate and test the code. In
characterize how developers reason about generated assertions and           generating unit tests, the biggest challenge lies in generating asser-
explanations.                                                               tions to act as oracles [50]. Luckily, LLMs may be able to help. For
   Our findings reveal a substantial asymmetry in developer reason-         example, ChatAssert [27] generates test oracles using code sum-
ing. Participants were much better at identifying correct assertions        maries and examples, and then uses static and dynamic analyses
than identifying incorrect ones (74% vs. 49% accuracy, 𝑝 < 0.001,           to repair incorrect assertions. But LLMs sometimes oversimplify
𝑂𝑅 = 2.94), despite reporting similarly high confidence in both             specifications, and at other times fabricate them entirely [43]. Thus,
cases (approximately 4/5 for both, 𝑝 > 0.1). Surprisingly, natural-         to effectively use LLMs to generate tests, Juan needs to review and
language explanations led to no improvement in judgment accuracy            assess the correctness of the generated oracle assertions.
(𝑝 > 0.05), and low-quality explanations could even reduce accuracy            They ask an LLM to generate a test oracle for this docstring in
(𝑝 = 0.037, 𝑂𝑅 = 0.58) while simultaneously increasing confidence           the form of an assert with function input numbers and function
compared to no comment at all (𝑝 = 0.005, 4.25/5 vs. 3.99/5).               return ret. The model returns:
   Simultaneously, developers’ assessments of assertion complete-
                                                                        1   assert not ret or any ( abs (j - i ) < threshold
ness correlated with an independent mutation-based measure of           2     for i in numbers for j in numbers if i != j )
how many bugs it could detect (Spearman’s 𝜌 = 0.18, 𝑝 < 0.001),
and participants rated correct assertions as significantly more com-           This postcondition asserts that if the function returns True, then
plete than incorrect ones (𝑝 < 0.001). Together, this suggests that         some pair of non-equivalent elements in the input list must have
developers can distinguish stronger specifications from weaker ones         an absolute difference less than the given threshold. This statement
even when they struggle to identify logical errors. Providing insight       may seem satisfactory at first glance, but contains two errors. The
into these findings, our think-aloud study suggests that developers         first is an issue of completeness: it does not perform any checks
frequently rely on direct comparisons between assertion clauses             in cases where ret is False. The second is an issue of correctness:
and documentation, helping explain why some incorrect assertions            the if i != j check excludes all elements with equivalent values,
are difficult to detect. We make the following contributions:               rather than equivalent indices.
                                                                               Comprehending assert statements can be difficult in practice. If
                                                                            Juan misses the completeness error, they fail to test half of their
• A controlled experiment with 86 Python programmers investi-               intended functionality. If Juan misses the correctness error, they
  gating how developers evaluate LLM-generated postconditions,              will end up developing a function that is entirely mismatched with
  a representative class of machine-generated specifications used           their intended functionality. A natural question thus arises: if Juan
  in AI-assisted software reliability workflows.                            prompts the LLM to also generate a comment explaining the test
• Evidence that developers are much better at recognizing correct           oracle, can the resulting natural language translation of the test
  assertions than incorrect ones (74% vs. 49% accuracy, 𝑝 < 0.001,          oracle help them catch such errors? Furthermore, if the LLM’s
  𝑂𝑅 = 2.94), despite reporting similarly high confidence in both           comment is misaligned with the logic of the oracle (i.e., of poor
  cases (approximately 4/5, 𝑝 > 0.1).                                       quality), how will this misalignment affect Juan’s understanding of
• An investigation of natural-language explanations, showing that           the test?
  they provide no overall improvement in developers’ ability to                Unfortunately, a dearth of research exists into developer under-
  evaluate assertions, while low-quality explanations can reduce            standing of LLM-generated test oracles, whether LLM-generated
  accuracy (𝑝 = 0.037, 𝑂𝑅 = 0.58) compared to high-quality ones,            comments can aid this understanding, and whether misaligned
  and simultaneously increase developer confidence (𝑝 = 0.005)              comments can hurt this understanding. This work aims to bridge
  compared to no comment at all.                                            this gap by investigating 1) how reliably developers can identify
• A think-aloud study with 10 developers identifying five recur-            postcondition correctness, 2) whether LLM-generated comments
  ring reasoning strategies for evaluating generated assertions and         can aid in this task, and 3) whether the quality of these comments
  providing qualitative insight into why some classes of incorrect          matters. We augment this investigation with a qualitative analysis
  assertions may be systematically overlooked.                              of developer reasoning during postcondition comprehension tasks.
                                                                        2
3     Experimental Methodology                                                (2) Incorrect: There is at least one input/output pair that aligns with
To understand how programming logic, natural language, and hu-                    requirements in the function docstring where the postcondition
man reasoning interact, we conducted two user studies:                            raises an error.

(1) Controlled Experiment: A large-scale experiment with 86 partic-             Figure 1 has an example stimulus, including the target function
    ipants. Participants assessed if a series of logical postconditions       and associated postcondition conditions.
    accurately captured the a function’s behavior. We varied stimuli          Comment Conditions: For each postcondition–function pair, our
    in a controlled manner to understand the impact of assertion              corpus contained five stimuli: one for each comment condition.
    correctness or the quality of an accompanying natural-language            In our definitions, the ‘failure’ of an postcondition indicates that
    comment on human judgment.                                                the Python assert statement will raise an error. ‘passing’ indicates
(2) Qualitative Think-Aloud: For a nuanced understanding of de-               that the Python assert statement will not error. When we refer to
    veloper reasoning, we conducted a think-aloud with 10 partic-             the ‘failure’ or ‘passing’ of a comment, we are referring to a direct
    ipants. Participants interacted with a series of postconditions           translation of the comment into a Python assert statement.
    and functions while verbalizing their reasoning.
                                                                              (1) Exact: Comment is equivalent to the postcondition; For all func-
   These studies combine the strengths of controlled analysis with                tion input/output pairs, there are no cases where the comment
insight into participant reasoning, enabling a deeper understanding               passes and the postcondition fails, or vice versa. We consider
of how programmers interpret specifications.                                      exact comments to be high-quality comments.
                                                                              (2) Over-specified: Comment is stricter than the postcondition;
                                                                                  There exists a function input/output where the comment fails
3.1    Study 1: Controlled Experiment
                                                                                  and the postcondition passes, but not vice versa.
To study how assertion correctness and the presence or quality of an          (3) Under-specified: Comment is less strict than the postcondition;
associated natural-language comment influence human judgement,                    There is a function input/output where the comment passes
we conducted a controlled experiment with 86 participants. Partic-                and the postcondition fails, but not vice versa.
ipants reviewed a series of stimuli, each consisting of a function            (4) Incorrect: There exist function input/output pairs where the
and associated docstring, postcondition assertion, and (optionally)               comment fails and the postcondition assertion passes, and there
a natural-language comment describing the assertion. Participants                 exist function input/output pairs where the comment passes
assessed whether the postcondition accurately described the func-                 and the postcondition assertion fails.
tion’s behavior, assuming the provided implementation was correct.            (5) No Comment: No natural-language comment was included in the
Participants also rated the completeness of the postcondition—that                stimulus. The stimulus consisted entirely of the target function
is, how fully they felt it captured the function’s behavior. For both             and candidate postcondition.
correctness and completeness judgments, participants reported
confidence using a 0–5 Likert-style scale.                                       Figure 2 shows an example of an exact, over-specified, under-
    Our experimental design was guided by two considerations:                 specified, and incorrect comment for the correct postcondition from
(1) balancing experimental power against participant attention, and           Figure 1.
(2) isolating the effects of postcondition correctness and comment
quality. Each participant completed 10 stimuli. We chose 10 after             3.1.2 Stimulus Corpus Construction. We now describe how we
a small pilot study where we varied the number and found that                 constructed a corpus instantiating the experimental conditions de-
participants began to lose attention after 10. The study was hosted           scribed in Section 3.1.1. Each stimulus consisted of a function, a
on Qualtrics, took 45–60 minutes, and contained 3 attention-checks.           postcondition assertion, and (optionally) a natural-language com-
Stimuli were balanced within and across participants with respect             ment describing the postcondition.
to two postcondition correctness conditions (correct and incorrect)              For functions, we used a subset of the HumanEval [10] dataset
and five comment conditions (exact, over-specified, underspecfied,            developed by OpenAI for evaluating code generation models. We
incorrect, and no-comment). We discuss these conditions below.                selected this dataset because it was previously used in prior work
                                                                              on LLM-generated postconditions by Endres et al. [16]. In addition,
3.1.1 Experimental Conditions. To isolate the effects of program-             HumanEval functions are sufficiently complex to permit non-trivial
ming logic and natural-language explanations, we systematically               postconditions while remaining simple enough for inclusion in an
varied two aspects of each stimulus: (1) postcondition correct-               online survey without overloading participants.
ness and (2) the presence and quality of an accompanying natural-                In their previous work, Endres et al. used GPT-3.5-turbo and GPT-
language comment. This led to ten variants of every function (2               4 to generate postcondition/comment pairs for the 164 HumanEval
correctness × 5 comment conditions).                                          functions and evaluated the resulting postconditions for correctness
Correctness Conditions: For each function, our corpus included two            and completeness [16]. From this dataset, we filtered for functions
postconditions, one correct with respect to the function, and one             that had at least one correct and one incorrect postcondition. We
incorrect:                                                                    required that the incorrect postcondition be logically incorrect,
                                                                              rather than syntactically. We further filtered out cases where either
(1) Correct: For all function input/output pairs that align with the          postcondition was logically trivial, prohibitively long, or referenced
    requirements in the function docstring, there are no cases where          out-of-context functions. We identified 29 functions that fit our
    the postcondition raises an error.                                        requirements.
                                                                          3
                   (a) HumanEval function 58                           (b) Correct postcondition: ensures that all returned elements appear in both
1   def common ( l1 : list , l2 : list ) :
                                                                       input lists and that the return value is sorted and contains only unique elements.
2     """ Return sorted unique common elements for                 1   assert all ( i in l1 and i in l2 for i in ret )
        two lists .                                                2     and ret == sorted ( set ( ret ) )
3     common ([1 ,4 ,34 ,653 ,2 ,5] , [5 ,7 ,1 ,5 ,653 ,121]) ->
         [1 , 5, 653]
4     common ([5 ,3 ,2 ,8] , [3 ,2]) -> [2 ,3] " " "                   (c) Incorrect postcondition: appears plausible, but fails for some correct return
5     shared = set ()                                                  values. When l1 = [1,1,2], l2 = [1,4], and return_val = [1], it evaluates to
6     for e1 in l1 :
7       for e2 in l2 :                                                 [1] == [1,1] as duplicate elements from l1 are preserved.
8          if e1 == e2 : shared . add ( e1 )                       1   assert ret == sorted ([ value for value in l1
9     return sorted ( list ( shared ) )                            2     if value in l2 and ret . count ( value ) == 1])


                     Figure 1. Example stimuli shown to participants, including the target function and associated postcondition conditions.

                                                                       (a) Exact comment
1   # Ensures that all elements in the return value are present in both lists l1 and l2 , and that the return value is a
      sorted list of unique elements .

                                (b) Over-specified comment: adds a constraint that does not exist in the postcondition.
1   # Confirm that the return value is a unique set of elements found in both l1 and l2 , sorted in ascending order , that
      appear in both lists exactly once .

                                    (c) Under-specified comment: omits a constraint that exists in the postcondition.
1   # Return value contains elements that are present in both lists l1 and l2 , and the return value is sorted .

                                (d) Incorrect comment: both adds and omits constraints compared to the postcondition.
1   # Verify that the return value contains all elements that are common between the two input lists .


                   Figure 2. Example comments corresponding to the correct postcondition in Figure 1 under each comment-quality condition.


       All postconditions in the Endres et al. dataset included an as-              our survey questions for 5 curated functions. We curated these
    sociated LLM-generated comment. Some postconditions already                     questions by ordering our HumanEval functions by the difference
    had multiple associated comments spanning several quality cate-                 between the percentage of participants who accurately identified
    gories because the original dataset contained repeated postcondi-               the correct postcondition as correct, and the percentage of par-
    tions paired with different comments. When one or more comment-                 ticipants who accurately identified the incorrect postcondition as
    quality categories (exact, over-specified, under-specified, and in-             incorrect. We chose the 3 functions with the highest differences be-
    correct) were missing for a postcondition, the first author used                tween these values, and the 2 functions with the lowest differences
    GPT-3.5-turbo to generate additional candidate comments. These                  between these values. We counterbalanced function order, as well
    candidates were manually reviewed and annotated to produce one                  as whether follow-up participants were given correct or incorrect
    example of each comment-quality condition for every postcondi-                  postconditions across questions, such that each participant saw 3
    tion.                                                                           incorrect postconditions and 2 correct postconditions. All stimuli
       Three authors independently reviewed all postconditions and                  included exact comments.
    comments for quality and correctness consistency before inclusion
    in our experimental corpus. At this stage, we removed three addi-               4    Research Questions and Analysis Approach
    tional functions from the corpus due to implementation ambiguity                We organize our investigation and analysis of programming logic,
    in the original HumanEval dataset.                                              natural language comments, and human comprehension around
       The final corpus contained 26 functions. Each function was                   four research questions. As described in Section 3, we approach
    paired with one correct and one incorrect postcondition, and each               our investigation from the perspective of a programmer assessing
    postcondition was paired with all five comment conditions, yielding             postconditions in Python.
    a total of 260 experimental stimuli.
                                                                                    RQ1—Postcondition Correctness: How does the logical correct-
                                                                                    ness of an LLM-generated postcondition assertion impact program-
    3.2    Study 2: Qualitative Think-Aloud                                         mers’ ability to determine whether the assertion correctly describes
    While our controlled experiment quantified programmer perfor-                   the behavior of a Python function?
    mance, it did not explain why participants succeeded or failed. To              RQ2—Natural-Language Comments: How does the presence and
    better understand how programmers approach and analyzed post-                   quality of LLM-generated comments affect programmers’ ability to
    conditions, we also conducted a series of think-aloud sessions where            identify whether a postcondition correctly describes the behavior
    participants described their thought process when responding to                 of a Python function?
                                                                                4
RQ3—Assertion Characteristics: What features of assertions (e.g.,            fixed and random effects, rather than requiring separate post hoc
complexity or completeness) correlate with programmer perfor-                comparisons. Additional analyses, including the feature analyses
mance when evaluating postconditions?                                        for RQ3, were exploratory and are labeled as such in our results.
RQ4—Developer Reasoning: How do programmers reason about                     Following recommendations for exploratory analyses [58], we do
postconditions and accompanying natural-language comments?                   not apply multiple comparison corrections to reduce the likelihood
Are particular reasoning strategies associated with successful com-          of false negatives.
prehension?                                                                     We used RStudio [56] for our analysis. R packages included
                                                                             lme4, lmerTest, stats, car, and psych. We include all analysis
    Although our controlled experiment was originally designed to            scripts and report the results of all conducted statistical tests in our
investigate the effects of natural-language comments (RQ2), early            replication package [1].
analysis revealed a substantially larger-than-anticipated difference
between programmers’ ability to recognize correct and incorrect
                                                                             4.2    Qualitative Methods and Final Codebook
postconditions. This unexpected finding motivated additional analy-
ses examining the role of postcondition correctness (RQ1), postcon-          We address RQ4 through a qualitative think-aloud study designed to
dition characteristics associated with performance (RQ3), and our            better understand how programmers reason about logical assertions
qualitative follow-up study of the reasoning strategies underlying           and accompanying natural-language comments (Section 3.2). Par-
these differences (RQ4).                                                     ticipants verbalized their reasoning while completing five assertion-
    To support the original experimental goal, we pre-registered our         evaluation tasks. To analyze the think-aloud transcripts, we con-
hypotheses relating to RQ2 on the Open Science Framework [21].               ducted a directed content analysis [29] using a hybrid deductive–
In particular, we hypothesized that natural-language comments                inductive approach. Two authors collaboratively developed and
would improve participants’ ability to evaluate assertion correct-           refined a codebook capturing: (1) how participants constructed a
ness, but that these effects would depend on comment quality. All            mental model of the function and postcondition, and (2) the strate-
pre-registered hypotheses, study materials, analysis scripts, and            gies participants used to determine postcondition correctness.
replication artifacts are included in our replication package [1, 37].          Our mental-model coding scheme was informed by prior work on
While RQ1, RQ3, and RQ4 were motivated by observations made                  code comprehension [13, 19]. Specifically, we categorized participant–
during the early stages of analysis (and are thus more exploratory),         stimulus pairs as using a top-down, bottom-up, or as-needed com-
all analyses were conducted using the same controlled experimental           prehension processes:
design and statistical methodology (see Sections 3 and 4.1).                 Top-Down: Formed expectations from the docstring or comment,
                                                                             then verified them by reading the code.
4.1    Quantitative and Statistical Methods                                  Bottom-Up: Inferred behavior from the code, then verified it using
We address RQ1–RQ3 through quantitative analysis of our con-                 the docstring or comment.
trolled experiment with 86 programmers. Across these analyses,               As-Needed: Alternated between the code and the docstring or com-
our primary dependent variables are participant accuracy (whether            ment as needed to resolve questions.
the participant correctly assessed the postcondition), response time,           Correctness strategies were identified inductively as they emerged
and self-reported confidence.                                                during analysis, and are one of our contributions in RQ4. To im-
   Unless otherwise stated, we use mixed-effects models through-             prove reliability, two authors jointly coded the transcript of one
out our analyses. We use generalized linear mixed-effects models             participant, and refined code definitions by resolving coding dis-
for binary outcomes (e.g., participant accuracy) and linear mixed-           agreements. The first author then applied the finalized codebook
effects models for continuous outcomes (e.g., response time and              to the remaining transcripts.
confidence). Because response times were right-skewed, we log-
transformed them prior to analysis following established recom-              5     Participants and Recruitment
mended best practice [12, 72].                                               For both studies, we recruited via computing-specific email lists
   All models include participant- and stimulus-level random effects         and Slack channels at three large public universities. We also used
to account for repeated measures, participant ability, and variation         snowball sampling seeded by software company contacts. Partic-
in stimulus difficulty. Fixed effects were selected according to the         ipants had to (1) be at least 18, (2) able to read and understand
research question. For example, when evaluating the effects of com-          Python code, and (3) correctly answer all 3 study attention checks.
ment quality, we include postcondition correctness as a covariate            Participants received a $12 gift card.
to account for its potential influence on performance. We used
odds ratios for generalized linear model effect sizes, and estimated         Controlled Experiment Participants. We collected 106 survey submis-
marginal means for linear models. When comparing binary vari-                sions, of which 86 met our inclusion criteria and were retained for
ables, we additionally report 𝜒 2 tests and Fisher’s exact tests where       analysis. We excluded participants who failed one or more attention
appropriate.                                                                 checks. To remove implausibly rushed responses, we also excluded
   We used a significance threshold of 𝑝 < 0.05. We do not apply             stimulus-level data completed in under 20 seconds (18/737 total
a global correction for multiple comparisons because the primary             stimuli); the mean time spent on a non-attention-check question
analyses for RQ1 and the pre-registered analyses for RQ2 each                was 133.5 seconds.
centered on only three mixed-effects models: one each for accuracy,             Participants ranged in age between 18 and 42, with a mean age
response time, and confidence. Such models jointly estimate all              of 27.1. 66.3% of participants were professional developers. Most
                                                                         5
       ID   Age   Prof.   Years   LLM Use     Writes    Assertion                                               Confidence Distribution by Participant and Postcondition Correctness
                  Dev.    Exp.                Python      Exp.                                                           Postcondition: Correct                               Postcondition: Correct
                                                                                                                       Participant: Correct (73.9%)                        Participant: Incorrect (26.1%)
        1   31     Yes    10–15   Sometimes    Daily      Some                                             60
        2   26     No     10–15     Never      Rarely   Very little                                                                           48.3
                                                                                                                                                                                                            43.2
        3   25     Yes    5–10      Daily      Daily    Moderate                                           40                                          36.4
                                                                                                                                                                                                     29.5




                                                                             Percentage of Responses (%)
        4   27     Yes    10–15     Rarely     Daily    Moderate
        5   32     No     5–10      Often      Often      Some                                             20                                                                                 13.7
        6   26     No     5–10    Sometimes    Often      Some                                                                        9.7                                               8.4
                                                                                                                 0.4     1.5    3.7                                  2.1        3.2
        7   21     Yes     1–5    Sometimes    Often    Very little                                         0
        8   32     Yes     >15      Rarely     Often      A lot                                                          Postcondition: Incorrect                            Postcondition: Incorrect
        9   32     Yes    10–15     Daily      Rarely     Some                                                         Participant: Correct (49.0%)                        Participant: Incorrect (51.0%)
       10   29     Yes    5–10      Daily      Daily    Moderate                                           60
                                                                                                                                                       43.1                                          42.0   40.9
                                                                                                           40                                 37.4
              Figure 3. Think-aloud participant overview.
                                                                                                           20                         12.1                                                    11.6
                                                                                                                 1.7     1.1    4.6                                  1.7        1.7     2.2
                                                                                                            0
                                                                                                                  0       1     2      3        4      5       0     1                  2      3      4      5
participants reported between one and ten years of programming ex-                                                                              Participant Confidence
perience, moderate or greater Python proficiency, frequent Python                                                                            Postcondition Correct         No     Yes
use, and at least some prior experience writing logical assertions
and using LLMs.
                                                                             Figure 4. Confidence distributions of participants in four cases. Case 1 (top
Think-Aloud Participants. To better understand the reasoning pro-            left): Participant succeeds in identifying a correct postcondition. Case 2 (top
cesses underlying our quantitative findings, we recruited 10 addi-           right): Participant fails in identifying a correct postcondition. Case 3 (bottom
tional participants for the think-aloud study. Figure 3 shows par-           left): Participant succeeds in identifying an incorrect postcondition. Case 4
ticipant demographics and programming experience. Participants               (bottom right): Participant fails in identifying an incorrect postcondition.
ranged in age from 21 to 32 years. Seven participants were pro-
fessional programmers and three were university students. Nine
participants had more than five years of programming experience,                Participants frequently used negative examples when they per-
although only one reported significant experience writing logical            ceived a postcondition to be incorrect (18/29 cases), typically to
assertions.                                                                  confirm an initial judgment formed through clause comparison,
                                                                             logic walk-throughs, or intuition (14/18).
6     Results                                                                   We also examined the impact of assertion correctness on re-
                                                                             sponse time. When the postcondition was correct, participants took
We now present our experimental results, organized around our
                                                                             about the same amount of time to respond whether they answered
four research questions (see Section 4).
                                                                             correctly or not (103.4 vs. 108.4 average seconds). In contrast, suc-
                                                                             cessfully identifying an incorrect postcondition required substan-
6.1    RQ1: The Impact of Assertion Correctness                              tially more time (123.0 s) than incorrectly accepting it as correct
Programmers were substantially better at recognizing correct post-           (97.1 s). This difference was significant; a mixed-effects model with
conditions than identifying incorrect ones. Participants correctly           participant accuracy and postcondition correctness as predictors
identified 73.9% of correct postconditions as correct, but only 49.0%        shows a significant effect of participant accuracy on response time
of incorrect postconditions as incorrect. This difference was signifi-       (𝑝 = 0.014), driven by the interaction effect between participant
cant (𝑝 < 0.001, 𝑂𝑅 = 2.94), indicating that the odds of correctly           accuracy and postcondition correctness (𝑝 = 0.002). This suggests
recognizing a correct postcondition were nearly three times higher           that detecting specification errors requires effort, and incorrectly
than those of correctly identifying an incorrect one. As a qualitative       accepting plausible assertions often occurs quickly.
example, our stimulus example in Figure 1 is the function where
                                                                                                      RQ1: Summary—Impact of Assertion Correctness: Pro-
we saw the largest difference in participant accuracy between the
                                                                                                      grammers were much better at recognizing correct assertions
correct and incorrect postcondition (92% vs. 10%, respectively).
                                                                                                      than identifying incorrect ones. Detecting incorrect assertions
    We hypothesize two potential reasons for this discrepancy. First,
                                                                                                      also required significantly more time, yet participants remained
developers may have an acceptance bias toward AI-generated spec-
                                                                                                      similarly confident regardless of whether their judgments were
ifications; prior work has shown that people are likely to accept
                                                                                                      correct.
code suggestions even when they are incorrect [15]. Second, it
may be more cognitively demanding to identify that a logical state-
ment is incorrect than it is to confirm that the statement is correct.       6.2                                 RQ2: Comment Presence and Quality
We return to this second possibility in RQ3 (Section 6.3) and RQ4            We now investigate how natural-language comments impact pro-
(Section 6.4).                                                               grammer assessments of postcondition correctness. Surprisingly,
    Interestingly, neither postcondition correctness nor participant         we find that (1) comments generally do not improve programer
correctness significantly affected self-reported confidence (𝑝 > 0.1).       accuracy, and (2) low-quality comments can reduce performance
Confidence was uniformly high in all cases (3.98–4.14, 0–5 Likert).          and increase confidence.
Figure 4 summarizes confidence distributions by postcondition and              We fit a mixed effects model predicting participant accuracy from
participant correctness.                                                     comment condition while controlling for postcondition correctness.
                                                                         6
Contrary to our pre-registered hypothesis (see Section 4), the pres-        means = = 2.66 vs. 2.35). Together, these findings suggest that partic-
ence of a comment (even if that comment was of high-quality) did            ipants could distinguish stronger specifications from weaker ones
not significantly improve participant accuracy compared to pro-             even when they failed to identify logical errors.
viding no comment at all (𝑝 > 0.1). Furthermore, these effects did          Complexity: Correct postconditions exhibited significantly lower
not differ between correct and incorrect postconditions. These find-        cyclomatic complexity than incorrect postconditions (𝑝 < 0.001;
ings suggest that simply providing an explanation is insufficient;          emmeans = 4.28 vs. 4.85), a pattern that we find is also true across
explanation quality can matter more than explanation presence.              the larger postcondition corpus from prior work [16] from which
    Although comments provided no overall benefit, comment qual-            we filter for our experimental stimuli. However, mediation analy-
ity did matter. When comparing between different comment qual-              sis found that cyclomatic complexity did not explain the effect of
ities in the case that a comment exists, participants were signif-          postcondition correctness on participant accuracy (𝑝 = 0.50), and
icantly less accurate when comments were under-specified than               neither Halstead difficulty nor cognitive complexity differed signifi-
when comments exactly matched the postcondition (𝑝 = 0.037,                 cantly between correct and incorrect postconditions (𝑝 > 0.1). Thus,
𝑂𝑅 = 0.58). Anecdotally, participants were also slightly less ac-           although incorrect assertions tend to be somewhat more complex,
curate with under-specified comments than with no comment at                complexity alone does not explain developers’ difficulty detecting
all(54.3% vs. 62.7%), suggesting that incomplete explanations may           them.
actively interfere with reasoning rather than simply failing to help.       Assertion Construction Patterns: Using the postcondition taxon-
    This decrease in performance was accompanied by increased               omy proposed by Endres et al. [16], we explored whether particular
confidence. Participants reported significantly higher confidence           assertion construction patterns were associated with participant
when evaluating under-specified comments than when evaluating               performance.
stimuli without comments (𝑝 = 0.005; emmeans = 4.25/5 vs. 3.99/5).             Assertions containing type checks (𝜒 2 = 7.99, 𝑝 = 0.005, 𝑂𝑅 =
We found no significant relationship between participant confi-             2.10) or arithmetic equalities (𝜒 2 = 9.64, 𝑝 = 0.002, 𝑂𝑅 = 2.07) were
dence and judgment correctness. Thus, under-specified comments              more likely to be judged correctly, whereas implications (𝜒 2 = 3.84,
may have increased perceived understanding without improving                𝑝 = 0.05, 𝑂𝑅 = 0.69) and element-property assertions (𝜒 2 = 3.26,
actual comprehension.                                                       𝑝 = 0.07, 𝑂𝑅 = 0.66) were associated with decreased performance.
    Comment condition also affected response time (𝑝 = 0.022). Par-         We return to these observations in RQ4 (Section 6.4), where our
ticipants took the longest time to respond when looking at exact            qualitative analysis suggests these construction patterns differ in
comments, and the shortest time to respond when there was no                the extent to which they support direct clause comparison.
comment at all (emmeans = 94.3, 114.5, 105.3, 109.6, 111.8 for no
comment, exact comment, incorrect comment, over-specified com-              6.3.1 Demographics. Finally, we found no evidence that developer
ment, and under-specified comment, respectively). Participants may          experience, Python expertise, assertion-writing experience, or LLM
have spent additional time comparing the comment with the post-             usage predicted participant accuracy. This may indicate that pro-
condition, although this additional effort did not improve judgment         grammers of all experience levels could benefit from assistance
accuracy.                                                                   with parsing postconditions.
  RQ2: Summary—Impact of Comments: Contrary to our                            RQ3: Summary—Assertion Construction Patterns: Partici-
  pre-registered hypotheses, natural-language comments did not                pants could recognize differences in completeness between post-
  improve programmers’ ability to evaluate postconditions. Fur-               conditions. Although incorrect assertions tended to be slightly
  thermore, under-specified comments reduced accuracy relative                more complex, complexity did not explain the performance
  to exact comments, while increasing developer confidence com-               difference observed in RQ1. Some logical structures are easier
  pared to no comment at all.                                                 for developers to evaluate than others.

                                                                            6.4    RQ4: Understanding Developer Reasoning
                                                                            To provide insight into developer reasoning, we conduct a quali-
                                                                            tative think-aloud, where we investigate (1) how participants un-
6.3    RQ3: Assertion Characteristics and                                   derstand functions and associated postcondition assertions, and
       Performance                                                          (2) how do participants reason about postcondition correctness.
Because the large asymmetry observed in RQ1 was unexpected, we              We collected think-aloud transcripts for 50 function–postcondition
conducted several exploratory analyses to better understand what            pairs (10 participants, 5 stimuli each). Figure 5 describes these stim-
characteristics of postcondition assertions were associated with            uli, which were selected to cover a range of reasoning difficulties
participant performance.                                                    (as determined by participant performance in our large quantitative
Completeness: For correct postconditions, we compared partic-               evaluation).
ipant completeness ratings against the independently computed               Comprehension: Building a mental model: As described in
mutation-based bug-completeness scores from Endres et al. [16].             Section 4.2, we code each interaction for its predominant compre-
Participants’ completeness ratings showed a significant positive cor-       hension process (top-down, bottom-up, or as-needed).
relation with bug-completeness (Spearman’s 𝜌 = 0.18, 𝑝 < 0.001).               For the majority of responses (31/50), participants used a top-
Participants also rated correct postconditions as significantly more        down approach, first reading the English language docstring or
complete than incorrect ones (Wilcoxon rank-sum test, 𝑝 < 0.001;            comment, and then confirming their understanding by parsing the
                                                                        7
                                      % Identified                                                    Original Postcondition - Correct
           Function               Incorrect     Correct    Diff
                                                                                           Clause
           common                    10.0         92.3      82.3                          Compare
                                                                                                                                              Perceived
           match_parens              82.4         18.2      64.2                                                                               Correct
           has_close_elements        17.6         76.9      59.3                           Logic
           any_int                   75.0         82.4       7.4                           Walk

           choose_num                 0.6        0.611       1.1
                                                                                        Pos Example

                                                                                        Neg Example                                           Perceived
Figure 5. Functions curated for our qualitative follow-up study. These func-
                                                                                                                                              Incorrect
tions make up the top three and the bottom two of our stimuli, ordered                    Intuition
by the difference between the percentage of participants who accurately
identified the correct postcondition as correct and those who accurately
identified the incorrect postcondition as incorrect.                                                  Original Postcondition - Incorrect


                                                                                           Clause                                             Perceived
code. In 7 responses, participants went bottom-up, first reading the                      Compare                                              Correct

code and then confirming with comments. In 10 responses, partic-
ipants showcased an as-needed approach, bouncing between the                               Logic
documentation and the code. In 2 responses, the participants did not                       Walk

provide enough spoken information for us to make a determination.                       Pos Example                                           Perceived
                                                                                                                                              Incorrect
Reasoning Strategies: We identified five strategies used by par-                        Neg Example
ticipants to determine postcondition correctness:
                                                                                          Intuition
(1) Clause Comparison: The participant compared logical clauses
    between the function and the postcondition, and determined
    whether they matched. “Now, looking at this assertion, it’s en-
                                                                                   Figure 6. Two Sankey diagrams showing the portion of responses from
    tirely missing the integer criterion.” (P4)                                    the think-aloud survey where participants employed each strategy when
(2) Logic Walk-through: The participant traced the flow of data                    they perceived a postcondition to be incorrect, and when they perceived a
    through the postcondition to determine whether it matched an                   postcondition to be correct. The diagrams are separated by the ground-truth
    expected data flow with respect to the function. “This is just                 correctness of the original postconditions.
    saying, return whatever the maximum value is in that valid range
    if X is less than or equal to Y . . . otherwise negative 1. It seems
    correct.” (P3)                                                                     We found that in most cases where a postcondition was per-
(3) Positive Examples: The participant walked through a specific                   ceived to be incorrect (18/29), participants used negative examples.
    example of an input-output pair for the function that passed the               This was often to confirm a perception formed by clause compar-
    postcondition. “Empty list, that would be fine. [The postcondition]            isons, logic walk-through, or intuition (14/18). For example, one
    would be vacuously satisfied if the return value is just one thing.”           participant viewing the choose_num function intuited that “the as-
    (P4)                                                                           sert doesn’t look right”, then followed a negative example to “think
(4) Negative Examples: The participant walked through a specific                   through the whole thing” (P9). Occasionally, participants would at-
    example of an input-output pair for the function that failed the               tempt to confirm or break their correctness perception by trying
    postcondition. “If X and Y were 3 and 3, then the return value [of             to find a counterexample. For instance, one participant stated that
    the function] would be negative 1, but ... this assertion would fail.”         the correct postcondition for function match_parens “seems right”
    (P10)                                                                          (P10), then went on to look for counterexamples with “let me think
(5) Intuition: The participant did not systematically determine post-              if I can break this” (P10).
    condition correctness, but rather intuited that the postcondition                  Easier postconditions tended to afford clause comparison. In
    seemed correct or incorrect. “I’m not totally certain, maybe I’m               four of the five postconditions with at least 75% accuracy in the
    missing some subtle detail, but it sounds correct. It seems like it’s          original study (Figure 5), every think-aloud participant used clause
    capturing the correct behavior... I can’t think of how I’m not right.”         comparison at least once. The any_int function had the highest
    (P3)                                                                           average response accuracy across ground-truth correct and incor-
   Participants often used multiple strategies to assess the same                  rect postconditions. For this function, both postconditions afforded
stimulus. Figure 6 displays two Sankey diagrams summarizing strat-                 direct clause comparison. For example, when viewing the incorrect
egy use across our five think-aloud functions (Figure 5), split by                 postcondition, P1 noted that “we are missing the requirement that
when the participant perceived a postcondition to be correct and                   they are all integers”. When viewing the correct postcondition, P6
when they perceived it to be incorrect. The top diagram summa-                     noted that “it seems like this assertion checks all three conditions
rizes responses for ground-truth correct postconditions, while the                 here”.
bottom diagram summarizes responses for ground-truth incorrect                         We observed no clear relationship between the number of strate-
postconditions.                                                                    gies used and response correctness, nor with stimulus. However,
                                                                               8
we did observe individual differences in reasoning styles: some con-          complexity to flag potentially incorrect postconditions or inform
sistently used only one or two strategies, whereas others regularly           recommendations to developers.
applied three or more. For instance, P2 used only 1 strategy in 4 out
of 5 of their responses, while participant 8 used 4 or more strategies        8     Related Work
in 4 out of 5 of their responses. Additionally, certain participants
                                                                              While recent work has made substantial progress in generating
seemed to prefer certain strategies. For instance, P3 always began
                                                                              specifications, assertions, and natural-language explanations, com-
with a logic walk-through, P6 leaned on clause comparisons, and               paratively little is known about if developers can reliably evaluate
P8 consistently used examples.                                                these generated reliability artifacts. Our work helps fill this gap
   Only 12/50 responses involved the use of intuition, with just 3            by systematically investigating the human ability to assess machine-
responses consisting entirely of intuition. However, when intuition           generated assertions and the effect of accompanying natural-language
was used, participants were wrong more often than they were right,            explanations on that ability.
with 7/12 incorrect responses. These made up the majority of the
11 incorrect responses.
                                                                              8.1    Natural Language Support for AI-Generated
    RQ4: Summary—Developer Reasoning: Participants primar-                           Software
    ily used top-down comprehension, relying on clause compari-
                                                                              Collaboration between developers and LLMs is now standard in de-
    son, logic walk-throughs, positive and negative examples, and
                                                                              velopment workflows [63]. Although LLMs perform well on many
    intuition to assess function–postcondition alignment. Partici-
                                                                              benchmarks, they remain susceptible to vulnerabilities [25], hal-
    pants more accurately classified postconditions that afforded
                                                                              lucinated APIs [35, 60], and misinterpretation of natural-language
    clause comparison than those that did not. Negative examples
                                                                              instructions [68]. Generated code may be fundamentally misaligned
    were primarily used to confirm suspected incorrectness after
                                                                              with developer intent, and that misalignment can be hard to de-
    other reasoning strategies.
                                                                              tect [69]. Humans also cede agency to artificial intelligence in a
                                                                              way they do not cede it to humans [9], and readily accept incorrect
7     Discussion and Implications                                             code [15].
Our findings have several implications for tool design.                          Natural-language comments are the standard mechanism for im-
Developers tend to trust ML output even when it is wrong.                     proving code comprehension [32] and can increase developer adop-
Humans are significantly worse at recognizing when postconditions             tion of LLM-generated code [42]. Early work generated comments
are incorrect than when they are correct; that is, they are far more          using static-analysis heuristics and templates [2, 14, 26, 47, 62].
likely to return false positives than false negatives. Furthermore,           More recent work formulates comment generation as machine
they trust with high confidence in both cases (see Figure 4). This            translation from code to natural language [3, 4, 18, 22, 30, 32, 33,
aligns with previous findings regarding code repair suggestions [15],         39, 46, 53, 54, 61, 70, 71]. These approaches are typically evaluated
and indicates that development assistance tools should facilitate             using automatic metrics such as BLEU [52], or ROUGE [44], al-
developer comprehension of suggested test oracles.                            though such metrics do not necessarily correlate with developer
                                                                              understand, and humans may prefer human-written summaries to
Comments are insufficient to explain postconditions to devel-
                                                                              machine-written ones [64].
opers. Comments are a standard way to increase code comprehen-
                                                                                 As a result, several works evaluate generated comments through
sion [32] and facilitate LLM-based development [42]. However, our
                                                                              human studies of how the comments impact comprehension. Prior
findings in Section 6.2 indicate that comprehension of postcondi-
                                                                              work has measured comprehension using short-answer questions [24,
tions specifically may not increase significantly with comments, and
                                                                              64], multiple-choice questions [73], cloze tests [8], and code writ-
that comments that are insufficiently specified may even harm com-
                                                                              ing/debugging tasks [24]. ComCat shows that expertise-guided
prehension. Future work should investigate alternative approaches
                                                                              context improves both generated comments and developer under-
to aligning human mental models to logical postcondition state-
                                                                              standing [24]. B"orstler et al. find that comments conveying infor-
ments.
                                                                              mation beyond direct code translation, such as purpose, improve
Developers have an intuitive understanding of completeness.                   readability but not necessarily comprehension [8]. Steidl et al. pro-
Humans can correctly gauge relative postcondition completeness,               pose and validate a model that evaluates comment quality based
and can intuit that correct postconditions are more complete than             on coherence, usefulness, completeness, and consistency [65]. Fi-
incorrect postconditions (Section 6.3). This could indicate that intu-        nally, Wu et al. show that annotations containing formally verified
ited bug-completeness can potentially help ground mental models               assertions can themselves improve program understanding [73].
of postcondition correctness, and should be investigated in future               In our work, we are interested in programmers’ ability to cor-
work.                                                                         rectly assess logical assertions. Rather than evaluating generated
Incorrect postconditions tend towards higher cyclomatic                       comments through programmer comprehension tasks, we inves-
complexity than correct postconditions. While we did not                      tigate how comment quality affects programmers’ judgement of
find that this mediated our observed difference between partic-               generated assertions. Because assertions have precise formal se-
ipant tendency to identify correct and incorrect postconditions               mantics, we can systematically characterize comment–assertion
(Section 6.3), this is a noteworthy difference observed not only in           alignment as exact, over-specified, under-specified, or incorrect, en-
our filtered dataset but over the entire unfiltered dataset from previ-       abling controlled study of how different forms of comment quality
ous work [16]. Future work should investigate the use of cyclomatic           influence programmer judgment.
                                                                          9
8.2    Aligning Natural Language Intent with Code                             other demographics will exhibit different understanding patterns
A common approach to ensuring alignment between developer                     of LLM-generated comments or assertions.
intent and generated code is to formalize human-written natural-              The generation model. We used GPT-3.5-turbo to generate asser-
language specifications. Lahiri argues that future AI-assisted soft-          tion comments, and the postcondition assertions we used were also
ware development should increasingly rely on behavioral artifacts             generated by this model during previous work [16]. More recent
such as tests, assertions, and formal specifications to capture devel-        models have since been released, with updated code generation
oper intent [40]. Helping realize this vision, Prasad et al. propose          capabilities. However, as our work targets human understanding
a cognitively grounded framework that helps developers verify                 rather than model capability, we posit that our results will general-
AI-generated code by reasoning over machine-generated formal                  ize to more recent models.
artifacts [57]. Together, these works motivate specification-centric,         The survey dataset. All of our survey questions, including LLM-
human-in-the-loop development workflows. However, compara-                    generated comments and postconditions, were built with the Hu-
tively little is known about how effectively developers can evaluate          manEval dataset [10]. We chose this dataset as it was written specif-
the generated specifications they are asked to review.                        ically to act as a benchmark for LLM-driven code generation. How-
    A large body of work has focused on generating formal speci-              ever, this dataset includes only single-function Python code blocks
fications from natural-language documentation. ALICS [51] and                 with functionality that can be mostly summarized in a single asser-
Doc2Spec [76] infer formal language specifications from API docu-             tion statement. We cannot be certain that our results generalize to
mentation. Toradocu [23], JDoctor [7], and C2S [75] use comments              multi-function code or to multiple assertions, though we posit that
to generate oracles as precondition or postcondition assertions.              more complex code will exacerbate the concerns we have surfaced.
Swami generates executable tests from structured natural-language
specifications [50]. More recent work leverages LLMs, using con-              10     Conclusion
text gathered from existing code [49], documentation [27, 43], or
GitHub issues [59] to generate specifications.                                We perform a systematic evaluation of humans’ ability to com-
    In practice, natural-language documentation or developer intent           prehend LLM-generated logical Python postcondition statements,
can be misaligned with implementation. Thus, other approaches                 and the effect of associated natural-language comments of varying
attempt to catch or correct such misalignment. iComment extracts              quality on this comprehension. We further perform an exploratory
implicit program rules from comments and analyzes them for im-                analysis of postcondition characteristics that affect human compre-
plementation inconsistencies [66]. @TComment generates tests                  hension. Our work contributes to the under-studied area of human
for Javadoc properties to find discrepancies between comments                 understanding of LLM-generated logical specifications.
and code [67]. JavadocMiner uses heuristic-based metrics to assess
inline documentation quality and code-alignment [38]. Zhou et                 Data Availability
al. extract logical directives from API documents and use a con-              Our stimuli, pre-registration, data, analysis scripts, and results are
straint solver to detect defects [79]. Specine repairs misalignment           available at a repository on the Open Science Framework (osf.io) [1].
between LLM-generated specifications and intent [68]. Endres et al.
propose empirically and qualitatively validated metrics to measure            Acknowledgments
alignment between natural-language generated postconditions and               This work is supported by the National Science Foundation under
intent [16]. Finally, TiCoder partially formalizes intent by interac-         grant no. CCF-2210243.
tively guiding developers via test generation [17].
    Accross this literature, evaluation of alignment between natu-            References
ral language and formal specifications is largely automatic. While             [1] 2026. Replication Package for The impact of comments on the correct under-
recent work has proposed systems that support developers in re-                    standing of logical code statements. https://osf.io/q6d2m/overview?view_only=
viewing generated specifications and formal artifacts [57], there is               442a1b8d82554de0baa4b4083987a6b6.
                                                                               [2] Nahla J. Abid, Natalia Dragan, Michael L. Collard, and Jonathan I. Maletic. 2015.
limited empirical understanding of how accurately programmers                      Using stereotypes in the automatic generation of natural language summaries
can assess specification correctness or how they reason about these                for C++ methods. In 2015 IEEE International Conference on Software Maintenance
                                                                                   and Evolution (ICSME). 561–565. doi:10.1109/ICSM.2015.7332514
artifacts. In our study, we provide participants with both human-              [3] Wasi Uddin Ahmad, Saikat Chakraborty, Baishakhi Ray, and Kai-Wei Chang.
written intent in the form of function docstrings, and machine-                    2021. Unified Pre-training for Program Understanding and Generation.
generated assertion statements. By measuring both participant                      arXiv:2103.06333 [cs.CL] https://arxiv.org/abs/2103.06333
                                                                               [4] Miltiadis Allamanis, Hao Peng, and Charles Sutton. 2016. A Convolutional Atten-
accuracy at identifying assertion correctness and perceptions of                   tion Network for Extreme Summarization of Source Code. In International Con-
completeness, we provide empirical evidence about the human ver-                   ference on Machine Learning (Proceedings of Machine Learning Research, Vol. 48),
ification capability underlying specification-driven development.                  Maria Florina Balcan and Kilian Q. Weinberger (Eds.). PMLR, New York, New
                                                                                   York, USA, 2091–2100. https://proceedings.mlr.press/v48/allamanis16.html
                                                                               [5] Alberto Bacchelli and Christian Bird. 2013. Expectations, outcomes, and chal-
                                                                                   lenges of modern code review. In 2013 35th international conference on software
9     Limitations and Threats to Validity                                          engineering (ICSE). IEEE, 712–721.
                                                                               [6] Tobias Baum, Kurt Schneider, and Alberto Bacchelli. 2019. Associating working
                                                                                   memory capacity and code change ordering with code review performance.
The population. Our participants were recruited exclusively from                   Empirical Software Engineering 24, 4 (2019), 1762–1798.
a population of university students and software company employ-               [7] Arianna Blasi, Alberto Goffi, Konstantin Kuznetsov, Alessandra Gorla, Michael D.
                                                                                   Ernst, Mauro Pezzè, and Sergio Delgado Castellanos. 2018. Translating code
ees in the United States. As such, we were only able to capture                    comments to procedure specifications (ISSTA 2018). Association for Computing
participant behavior in this demographic, and it is possible that                  Machinery, New York, NY, USA, 242–253. doi:10.1145/3213846.3213872
                                                                         10
 [8] Jürgen Börstler and Barbara Paech. 2016. The Role of Method Chains and Com-                     Intelligence 56, 6 (2026), 200. doi:10.1007/s10489-026-07230-0
     ments in Software Readability and Comprehension—An Experiment. IEEE Trans-                 [26] Sonia Haiduc, Jairo Aponte, and Andrian Marcus. 2010. Supporting program
     actions on Software Engineering 42, 9 (2016), 886–898. doi:10.1109/TSE.2016.                    comprehension with source code summarization. In 32nd International Con-
     2527791                                                                                         ference on Software Engineering - Volume 2 (Cape Town, South Africa) (ICSE
 [9] Cindy Candrian and Anne Scherer. 2022. Rise of the machines: Delegating                         ’10). Association for Computing Machinery, New York, NY, USA, 223–226.
     decisions to autonomous AI. Computers in Human Behavior 134 (2022), 107308.                     doi:10.1145/1810295.1810335
     doi:10.1016/j.chb.2022.107308                                                              [27] Ishrak Hayet, Adam Scott, and Marcelo d’Amorim. 2025. ChatAssert: LLM-Based
[10] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de                             Test Oracle Generation With External Tools Assistance. IEEE Trans. Softw. Eng.
     Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg                  51, 1 (Jan. 2025), 305–319. doi:10.1109/TSE.2024.3519159
     Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf,             [28] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li, Xiapu Luo,
     Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail                     David Lo, John Grundy, and Haoyu Wang. 2024. Large language models for
     Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter,                        software engineering: A systematic literature review. ACM Transactions on
     Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fo-                    Software Engineering and Methodology 33, 8 (2024), 1–79.
     tios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex             [29] Hsiu-Fang Hsieh and Sarah E Shannon. 2005. Three approaches to qualitative
     Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shan-              content analysis. Qualitative health research 15, 9 (2005), 1277–1288.
     tanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh            [30] Xing Hu, Ge Li, Xin Xia, David Lo, and Zhi Jin. 2018. Deep code comment
     Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles                        generation. In Proceedings of the 26th Conference on Program Comprehension
     Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei,                   (Gothenburg, Sweden) (ICPC ’18). Association for Computing Machinery, New
     Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. Evaluating Large                    York, NY, USA, 200–210. doi:10.1145/3196321.3196334
     Language Models Trained on Code. (2021). arXiv:2107.03374 [cs.LG]                          [31] Xing Hu, Xin Xia, David Lo, Zhiyuan Wan, Qiuyuan Chen, and Thomas Zimmer-
[11] Umut Cihan, Vahid Haratian, Arda İçöz, Mert Kaan Gül, Ömercan Devran,                           mann. 2022. Practitioners’ expectations on automated code comment generation.
     Emircan Furkan Bayendur, Baykal Mehmet Uçar, and Eray Tüzün. 2025. Auto-                        In Proceedings of the 44th International Conference on Software Engineering (Pitts-
     mated Code Review in Practice. In International Conference on Software Engi-                    burgh, Pennsylvania) (ICSE ’22). Association for Computing Machinery, New
     neering: Software Engineering in Practice (ICSE-SEIP). 425–436. doi:10.1109/ICSE-               York, NY, USA, 1693–1705. doi:10.1145/3510003.3510152
     SEIP66354.2025.00043                                                                       [32] Yuan Huang, Shaohao Huang, Huanchao Chen, Xiangping Chen, Zibin Zheng,
[12] Douglas Curran-Everett. 2018. Explorations in statistics: the log trans-                        Xiapu Luo, Nan Jia, Xinyu Hu, and Xiaocong Zhou. 2020. Towards automati-
     formation.       Advances in Physiology Education 42, 2 (2018), 343–347.                        cally generating block comments for code snippets. Information and Software
     arXiv:https://doi.org/10.1152/advan.00018.2018 doi:10.1152/advan.00018.2018                     Technology 127 (2020), 106373. doi:10.1016/j.infsof.2020.106373
     PMID: 29761718.                                                                            [33] Srinivasan Iyer, Ioannis Konstas, Alvin Cheung, and Luke Zettlemoyer. 2016.
[13] A Dunsmore, M Roper, and M Wood. 2000. The role of comprehension in software                    Summarizing Source Code using a Neural Attention Model. In Proceedings of the
     inspection. Journal of Systems and Software 52, 2 (2000), 121–129. doi:10.1016/                 54th Annual Meeting of the Association for Computational Linguistics (Volume 1:
     S0164-1212(99)00138-7                                                                           Long Papers), Katrin Erk and Noah A. Smith (Eds.). Association for Computational
[14] Brian P. Eddy, Jeffrey A. Robinson, Nicholas A. Kraft, and Jeffrey C. Carver. 2013.             Linguistics, Berlin, Germany, 2073–2083. doi:10.18653/v1/P16-1195
     Evaluating source code summarization techniques: Replication and expansion.                [34] Jasmin Jahić and Ashkan Sami. 2024. State of Practice: LLMs in Software En-
     In International Conference on Program Comprehension. 13–22. doi:10.1109/ICPC.                  gineering and Software Architecture. In International Conference on Software
     2013.6613829                                                                                    Architecture (ICSA). 311–318. doi:10.1109/ICSA-C63560.2024.00059
[15] Hadeel Eladawy, Claire Le Goues, and Yuriy Brun. 2024. Automated Program                   [35] Erik Jones, Hamid Palangi, Clarisse Simões Ribeiro, Varun Chandrasekaran,
     Repair, What Is It Good For? Not Absolutely Nothing!. In International Confer-                  Subhabrata Mukherjee, Arindam Mitra, Ahmed Hassan Awadallah, and Ece
     ence on Software Engineering (14–20). Lisbon, Portugal, 1017–1029. doi:10.1145/                 Kamar. 2024. Teaching Language Models to Hallucinate Less with Synthetic
     3597503.3639095                                                                                 Tasks. In The Twelfth International Conference on Learning Representations. https:
[16] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K. Lahiri.                    //openreview.net/forum?id=xpw7V0P136
     2024. Can Large Language Models Transform Natural Language Intent into                     [36] Sungmin Kang, Louis Milliken, and Shin Yoo. 2024. Identifying Inaccu-
     Formal Method Postconditions? PACMSE 1, FSE (2024), 84:1–84:24. doi:10.1145/                    rate Descriptions in LLM-generated Code Comments via Test Execution.
     3660791                                                                                         arXiv:2406.14836 [cs.SE] https://arxiv.org/abs/2406.14836
[17] Sarah Fakhoury, Aaditya Naik, Georgios Sakkas, Saikat Chakraborty, and Shu-                [37] Zhanna Kaufman, Yuriy Brun, Adithya Murali, and Madeline Endres. 2025. The
     vendu K. Lahiri. 2024. LLM-Based Test-Driven Interactive Code Generation: User                  impact of comments on the correct understanding of logical code statements.
     Study and Empirical Evaluation. IEEE Transactions on Software Engineering 50, 9                 osf.io/5f73u
     (Sept. 2024), 2254–2268. doi:10.1109/tse.2024.3428972                                      [38] Ninus Khamis, René Witte, and Juergen Rilling. 2010. Automatic Quality As-
[18] Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xiaocheng Feng, Ming Gong,                        sessment of Source Code Comments: The JavadocMiner. In Natural Language
     Linjun Shou, Bing Qin, Ting Liu, Daxin Jiang, and Ming Zhou. 2020. CodeBERT:                    Processing and Information Systems, Christina J. Hopfe, Yacine Rezgui, Elisabeth
     A Pre-Trained Model for Programming and Natural Languages. In Findings of the                   Métais, Alun Preece, and Haijiang Li (Eds.). Springer Berlin Heidelberg, Berlin,
     Association for Computational Linguistics: EMNLP 2020, Trevor Cohn, Yulan He,                   Heidelberg, 68–79.
     and Yang Liu (Eds.). Association for Computational Linguistics, Online, 1536–              [39] Junaed Younus Khan and Gias Uddin. 2023. Automatic Code Documentation
     1547. doi:10.18653/v1/2020.findings-emnlp.139                                                   Generation Using GPT-3. In International Conference on Automated Software En-
[19] Kathrin Figl, Maria Kirchner, Sebastian Baltes, and Michael Felderer. 2025. The                 gineering (Rochester, MI, USA) (ASE ’22). Association for Computing Machinery,
     Influence of Code Comments on the Perceived Helpfulness of Stack Overflow                       New York, NY, USA, Article 174, 6 pages. doi:10.1145/3551349.3559548
     Posts. 30, 6 (2025). doi:10.1007/s10664-025-10727-w                                        [40] Shuvendu K Lahiri. 2026. Intent formalization: A grand challenge for reliable
[20] Emily First, Markus Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-                    coding in the age of AI agents. arXiv preprint arXiv:2603.17150 (2026).
     Proof Generation and Repair with Large Language Models. In ACM Joint European              [41] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K Lahiri, and Siddhartha Sen.
     Software Engineering Conference and Symposium on the Foundations of Software                    2023. Codamosa: Escaping coverage plateaus in test generation with pre-trained
     Engineering (ESEC/FSE) (6–8). San Francisco, CA, USA, 1229–1241. doi:10.1145/                   large language models. In International Conference on Software Engineering (ICSE).
     3611643.3616243                                                                                 IEEE, 919–931.
[21] Erin Foster and Ariel Deardorff. 2017. Open Science Framework (OSF). Journal               [42] Changwen Li, Christoph Treude, and Ofir Turel. 2026. Do comments and expertise
     of the Medical Library Association 105 (04 2017). doi:10.5195/JMLA.2017.88                      still matter? An experiment on programmers’ adoption of AI-generated JavaScript
[22] Shuzheng Gao, Cuiyun Gao, Yulan He, Jichuan Zeng, Lunyiu Nie, Xin Xia, and                      code. Journal of Systems and Software 231 (2026), 112634. doi:10.1016/j.jss.2025.
     Michael Lyu. 2023. Code Structure–Guided Transformer for Source Code Summa-                     112634
     rization. ACM Trans. Softw. Eng. Methodol. 32, 1, Article 23 (Feb. 2023), 32 pages.        [43] Hui Li, Zhen Dong, Siao Wang, Hui Zhang, Liwei Shen, Xin Peng, and Dongdong
     doi:10.1145/3522674                                                                             She. 2025. Extracting Formal Specifications From Documents Using LLMS for
[23] Alberto Goffi, Alessandra Gorla, Michael D. Ernst, and Mauro Pezzè. 2016. Auto-                 Test Automation. In International Conference on Program Comprehension (ICPC).
     matic generation of oracles for exceptional behaviors. In International Sympo-                  1–12. doi:10.1109/ICPC66645.2025.00039
     sium on Software Testing and Analysis (ISSTA). Saarbrücken, Genmany, 213–224.              [44] Chin-Yew Lin. 2004. ROUGE: A Package for Automatic Evaluation of Summaries.
     doi:10.1145/2931037.2931061                                                                     In Annual Meeting of the Association for Computational Linguistics. https://api.
[24] Skyler Grandel, Scott Thomas Andersen, Yu Huang, and Kevin Leach. 2026.                         semanticscholar.org/CorpusID:964287
     ComCat: Expertise-Guided Context Generation to Enhance Code Comprehension.                 [45] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. Is
     35, 3, Article 82 (Feb. 2026), 30 pages. doi:10.1145/3742475                                    Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large
[25] Burak Gülmez. 2026. Code generation with large language models: a survey                        Language Models for Code Generation. In Thirty-seventh Conference on Neural
     from neural program synthesis to autonomous software development. Applied                       Information Processing Systems. https://openreview.net/forum?id=1qvx610Cu7

                                                                                           11
[46] Shangqing Liu, Yu Chen, Xiaofei Xie, Jingkai Siow, and Yang Liu. 2021.                     [65] Daniela Steidl, Benjamin Hummel, and Elmar Jürgens. 2013. Quality analysis
     Retrieval-Augmented Generation for Code Summarization via Hybrid GNN.                           of source code comments. International Conference on Program Comprehension
     arXiv:2006.05405 [cs.LG] https://arxiv.org/abs/2006.05405                                       (ICPC) (2013), 83–92. https://api.semanticscholar.org/CorpusID:16657129
[47] Paul W. McBurney and Collin McMillan. 2014. Automatic documentation genera-                [66] Lin Tan, Ding Yuan, Gopal Krishna, and Yuanyuan Zhou. 2007. /*icomment:
     tion via source code summarization of method context. In Proceedings of the 22nd                bugs or bad comments?*/. SIGOPS Oper. Syst. Rev. 41, 6 (Oct. 2007), 145–158.
     International Conference on Program Comprehension (Hyderabad, India) (ICPC                      doi:10.1145/1323293.1294276
     2014). ACM, New York, NY, USA, 279–290. doi:10.1145/2597008.2597149                        [67] Shin Hwei Tan, Darko Marinov, Lin Tan, and Gary T. Leavens. 2012. @tComment:
[48] Vishal Misra, Jakku Sai Krupa Reddy, and Sridhar Chimalakonda. 2020. Is there                   Testing Javadoc Comments to Detect Comment-Code Inconsistencies. In 2012
     a correlation between code comments and issues? an exploratory study. In Pro-                   IEEE Fifth International Conference on Software Testing, Verification and Validation.
     ceedings of the 35th Annual ACM Symposium on Applied Computing (Brno, Czech                     260–269. doi:10.1109/ICST.2012.106
     Republic) (SAC ’20). Association for Computing Machinery, New York, NY, USA,               [68] Zhao Tian and Junjie Chen. 2025. Aligning Requirement for Large Language
     110–117. doi:10.1145/3341105.3374009                                                            Model’s Code Generation. arXiv:2509.01313 [cs.SE] https://arxiv.org/abs/2509.
[49] Davide Molinelli, Luca Di Grazia, Alberto Martin-Lopez, Michael D. Ernst, and                   01313
     Mauro Pezzè. 2025. Do LLMs Generate Useful Test Oracles? An Empirical Study                [69] Priyan Vaithilingam, Tianyi Zhang, and Elena L. Glassman. 2022. Expectation
     with an Unbiased Dataset. In International Conference on Automated Software                     vs. Experience: Evaluating the Usability of Code Generation Tools Powered by
     Engineering (ASE). 278–290. doi:10.1109/ASE63991.2025.00031                                     Large Language Models. In Extended Abstracts of the 2022 CHI Conference on
[50] Manish Motwani and Yuriy Brun. 2019. Automatically Generating Precise Oracles                   Human Factors in Computing Systems (New Orleans, LA, USA) (CHI EA ’22).
     from Structured Natural Language Specifications. In International Conference on                 Association for Computing Machinery, New York, NY, USA, Article 332, 7 pages.
     Software Engineering (29–31). Montreal, QC, Canada, 188–199. doi:10.1109/ICSE.                  doi:10.1145/3491101.3519665
     2019.00035                                                                                 [70] Yao Wan, Zhou Zhao, Min Yang, Guandong Xu, Haochao Ying, Jian Wu, and
[51] Rahul Pandita, Xusheng Xiao, Hao Zhong, Tao Xie, Stephen Oney, and Amit                         Philip S. Yu. 2018. Improving automatic source code summarization via deep
     Paradkar. 2012. Inferring method specifications from natural language API                       reinforcement learning. In International Conference on Automated Software Engi-
     descriptions. In 2012 34th International Conference on Software Engineering (ICSE).             neering (Montpellier, France) (ASE ’18). Association for Computing Machinery,
     815–825. doi:10.1109/ICSE.2012.6227137                                                          New York, NY, USA, 397–407. doi:10.1145/3238147.3238206
[52] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002. BLEU: a                 [71] Yue Wang, Weishi Wang, Shafiq Joty, and Steven C.H. Hoi. 2021. CodeT5:
     method for automatic evaluation of machine translation. In Proceedings of the 40th              Identifier-aware Unified Pre-trained Encoder-Decoder Models for Code Under-
     Annual Meeting on Association for Computational Linguistics (Philadelphia, Penn-                standing and Generation. In Conference on Empirical Methods in Natural Language
     sylvania) (ACL ’02). Association for Computational Linguistics, USA, 311–318.                   Processing, Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and Scott Wen-
     doi:10.3115/1073083.1073135                                                                     tau Yih (Eds.). Association for Computational Linguistics, Online and Punta Cana,
[53] Md Rizwan Parvez, Wasi Ahmad, Saikat Chakraborty, Baishakhi Ray, and Kai-                       Dominican Republic, 8696–8708. doi:10.18653/v1/2021.emnlp-main.685
     Wei Chang. 2021. Retrieval Augmented Code Generation and Summarization.                    [72] Robert M West. 2022.             Best practice in statistics: The use of log
     In Findings of the Association for Computational Linguistics: EMNLP 2021, Marie-                transformation.      Annals of Clinical Biochemistry 59, 3 (2022), 162–165.
     Francine Moens, Xuanjing Huang, Lucia Specia, and Scott Wen-tau Yih (Eds.).                     arXiv:https://doi.org/10.1177/00045632211050531 doi:10.1177/00045632211050531
     Association for Computational Linguistics, Punta Cana, Dominican Republic,                      PMID: 34666549.
     2719–2734. doi:10.18653/v1/2021.findings-emnlp.232                                         [73] Haoze Wu, Rocky Klopfenstein, Keith Farkas, and Nina Narodytska. 2026. Viverra:
[54] Long Phan, Hieu Tran, Daniel Le, Hieu Nguyen, James Annibal, Alec Peltekian,                    Text-to-Code with Guarantees. arXiv:2605.14972 [cs.SE] https://arxiv.org/abs/
     and Yanfang Ye. 2021. CoTexT: Multi-task Learning with Code-Text Trans-                         2605.14972
     former. In Proceedings of the 1st Workshop on Natural Language Processing for              [74] Xin Xia, Lingfeng Bao, David Lo, Zhenchang Xing, Ahmed E. Hassan, and Shan-
     Programming (NLP4Prog 2021), Royi Lachmy, Ziyu Yao, Greg Durrett, Milos                         ping Li. 2018. Measuring Program Comprehension: A Large-Scale Field Study
     Gligoric, Junyi Jessy Li, Ray Mooney, Graham Neubig, Yu Su, Huan Sun, and                       with Professionals. IEEE Transactions on Software Engineering 44, 10 (2018),
     Reut Tsarfaty (Eds.). Association for Computational Linguistics, Online, 40–47.                 951–976. doi:10.1109/TSE.2017.2734091
     doi:10.18653/v1/2021.nlp4prog-1.5                                                          [75] Juan Zhai, Yu Shi, Minxue Pan, Guian Zhou, Yongxiang Liu, Chunrong Fang,
[55] Veronica Pimenova, Sarah Fakhoury, Christian Bird, Margaret-Anne Storey, and                    Shiqing Ma, Lin Tan, and Xiangyu Zhang. 2020. C2S: translating natural language
     Madeline Endres. 2025. Good vibrations? A qualitative study of co-creation,                     comments to formal program specifications (ESEC/FSE 2020). Association for
     communication, flow, and trust in vibe coding. arXiv preprint arXiv:2509.12491                  Computing Machinery, New York, NY, USA, 25–37. doi:10.1145/3368089.3409716
     (2025).                                                                                    [76] Hao Zhong, Lu Zhang, Tao Xie, and Hong Mei. 2009. Inferring Resource Specifi-
[56] Posit team. 2025. RStudio: Integrated Development Environment for R. Posit                      cations from Natural Language API Documentation. In International Conference
     Software, PBC, Boston, MA. http://www.posit.co/                                                 on Automated Software Engineering. 307–318. doi:10.1109/ASE.2009.94
[57] Siddhartha Prasad, Skyler Austen, Kathi Fisler, and Shriram Krishnamurthi. 2026.           [77] Li Zhong and Zilong Wang. 2024. Can LLM replace stack overflow? a
     Meaningful Human-in-the-Loop Checking of GenAI Synthesis for Restricted                         study on robustness and reliability of large language model code generation
     Languages. In 40th European Conference on Object-Oriented Programming (ECOOP                    (AAAI’24/IAAI’24/EAAI’24). AAAI Press, Article 2437, 9 pages. doi:10.1609/aaai.
     2026), Vol. 372. 22:1–22:31. doi:10.4230/LIPIcs.ECOOP.2026.22                                   v38i19.30185
[58] Kenneth J Rothman. 1990. No adjustments are needed for multiple comparisons.               [78] Suzhen Zhong, Shayan Noei, Ying Zou, and Bram Adams. 2026. Human–AI
     Epidemiology 1, 1 (1990), 43–46.                                                                Synergy in Agentic Code Review. arXiv preprint arXiv:2603.15911 (2026).
[59] Haifeng Ruan, Yuntong Zhang, and Abhik Roychoudhury. 2025. SpecRover: Code                 [79] Yu Zhou, Ruihang Gu, Taolue Chen, Zhiqiu Huang, Sebastiano Panichella, and
     Intent Extraction via LLMs. In International Conference on Software Engineering                 Harald Gall. 2017. Analyzing APIs Documentation and Code to Detect Directive
     (Ottawa, Ontario, Canada) (ICSE ’25). IEEE Press, 963–974. doi:10.1109/ICSE55347.               Defects. In International Conference on Software Engineering. 27–37. doi:10.1109/
     2025.00080                                                                                      ICSE.2017.11
[60] Advait Sarkar, Xiaotong, Xu, Neil Toronto, Ian Drosos, and Christian Poelitz. 2024.        [80] Yangtian Zi, Luisa Li, Arjun Guha, Carolyn Anderson, and Molly Q Feldman. 2025.
     When Copilot Becomes Autopilot: Generative AI’s Critical Risk to Knowledge                      “I Would Have Written My Code Differently’: Beginners Struggle to Understand
     Work and a Critical Solution. arXiv:2412.15030 [cs.HC] https://arxiv.org/abs/                   LLM-Generated Code. In International Conference on the Foundations of Software
     2412.15030                                                                                      Engineering (Clarion Hotel Trondheim, Trondheim, Norway) (FSE Companion
[61] Rishab Sharma, Fuxiang Chen, and Fatemeh Fard. 2022. LAMNER: code comment                       ’25). Association for Computing Machinery, New York, NY, USA, 1479–1488.
     generation using character language model and named entity recognition. In                      doi:10.1145/3696630.3731663
     International Conference on Program Comprehension (Virtual Event) (ICPC ’22).              [81] Christo Zietsman. 2026. The Specification as Quality Gate: Three Hypotheses on
     ACM, New York, NY, USA, 48–59. doi:10.1145/3524610.3527924                                      AI-Assisted Code Review. arXiv preprint arXiv:2603.25773 (2026).
[62] Giriprasad Sridhara, Emily Hill, Divya Muppaneni, Lori Pollock, and K. Vijay-
     Shanker. 2010. Towards automatically generating summary comments for
     Java methods. In International Conference on Automated Software Engineering
     (Antwerp, Belgium) (ASE ’10). ACM, New York, NY, USA, 43–52. doi:10.1145/
     1858996.1859006
[63] Stack Overflow. 2025. 2025 Stack Overflow Developer Survey. https://survey.
     stackoverflow.co/2025 Accessed June 2026.
[64] Sean Stapleton, Yashmeet Gambhir, Alexander LeClair, Zachary Eberhart, Westley
     Weimer, Kevin Leach, and Yu Huang. 2020. A Human Study of Comprehension
     and Code Summarization. In Proceedings of the 28th International Conference on
     Program Comprehension (Seoul, Republic of Korea) (ICPC ’20). Association for
     Computing Machinery, New York, NY, USA, 2–13. doi:10.1145/3387904.3389258
                                                                                           12
