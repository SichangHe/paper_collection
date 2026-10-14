                                                               Can ChatGPT Pass a Theory of Computing Course?
                                                       Matei A. Golesteanu∗                                             Garrett B. Vowinkel                             Ryan E. Dougherty
                                                 matei.golesteanu@westpoint.edu                                 garrett.vowinkel@westpoint.edu                     ryan.dougherty@westpoint.edu
                                                 United States Military Academy                                 United States Military Academy                     United States Military Academy
                                                   West Point, New York, USA                                      West Point, New York, USA                          West Point, New York, USA
                                         ABSTRACT                                                                                           This paper attempts to answer this question for a Theory of
                                         Large Language Models (LLMs) have had considerable difficulty                                   Computing (ToC) course, which is a required course for nearly all
                                         when prompted with mathematical questions, especially those                                     undergraduate CS curricula. It is a traditionally difficult course as it
                                         within theory of computing (ToC) courses. In this paper, we detail                              nearly always requires students’ be able to write precise proofs and
                                         two experiments regarding our own ToC course and the ChatGPT                                    create mathematical constructions. We tested the ChatGPT LLM1
arXiv:2407.07757v1 [cs.CY] 10 Jul 2024




                                         LLM. For the first, we evaluated ChatGPT’s ability to pass our own                              within the ToC course at our institution in two different experi-
                                         ToC course’s exams. For the second, we created a database of sample                             ments. First, we tested its ability to pass our course’s exams by
                                         ToC questions and responses to accommodate other ToC offerings’                                 grading its responses as though it were an actual student. Second,
                                         choices for topics and structure. We scored each of ChatGPT’s out-                              we created a large database of representative questions other offer-
                                         puts on these questions. Overall, we determined that ChatGPTcan                                 ings of ToC may ask, and determine ChatGPT’s ability to answer
                                         pass our ToC course, and is adequate at understanding common                                    those questions.
                                         formal definitions and answering “simple”-style questions, e.g.,                                   Our methods attempt to model what a student would do if they
                                         true/false and multiple choice. However, ChatGPT often makes non-                               were in a ToC course and used ChatGPT. The goals of this work are
                                         sensical claims in open-ended responses, such as proofs.                                        to (1) inform educators on ChatGPT’s ability to pass a ToC course,
                                                                                                                                         (2) also inform eductors what they can do to limit students’ ability
                                         CCS CONCEPTS                                                                                    to use ChatGPT without their learning ToC concepts, and (3) if
                                                                                                                                         desired, determine where ChatGPT struggles to help inform future
                                         • Theory of computation → Formal languages and automata
                                                                                                                                         ToC course designs on how to make LLM tools be more effective in
                                         theory; • Social and professional topics → Computing educa-
                                                                                                                                         the classroom. The remainder of this paper is organized as follows.
                                         tion; • Mathematics of computing → Discrete mathematics.
                                                                                                                                              • Section 2 contains related work to ours.
                                         KEYWORDS                                                                                             • Section 3 contains our method, which involves these two
                                                                                                                                                experiments.
                                         theoretical computer science, computer science education, large
                                                                                                                                              • Section 4 contains our results to our two experiments.
                                         language model, formal languages, automata theory, chatgpt
                                                                                                                                              • Section 5 discusses our results that will inform ToC educators
                                         ACM Reference Format:                                                                                  of what aspects of ToC ChatGPT struggled with the most.
                                         Matei A. Golesteanu, Garrett B. Vowinkel, and Ryan E. Dougherty. 2018.                               • Section 6 contains our threats to validity.
                                         Can ChatGPT Pass a Theory of Computing Course?. In Proceedings of Make
                                                                                                                                              • Section 7 contains our recommendations to educators and
                                         sure to enter the correct conference title from your rights confirmation emai
                                         (Conference acronym ’XX). ACM, New York, NY, USA, 6 pages. https://doi.
                                                                                                                                                future work.
                                         org/XXXXXXX.XXXXXXX                                                                                  • Section 8 concludes the paper.

                                         1     INTRODUCTION                                                                              2     BACKGROUND RESEARCH
                                         Large Language Models (LLMs) have had a serious impact on stu-                                  As far as we are aware, there has not been any prior research with
                                         dent academic integrity, including Computer Science. Many LLMs                                  ChatGPT’s ability to pass a ToC course. However, there has been
                                         train based upon publicly available data, which is proportional to                              several works regarding other common CS courses. Sharpe et al.
                                         the popularity of students taking courses in certain topics. In terms                           [6] recently determined that ChatGPT can easily pass a CS1 course.
                                         of CS, the most popular topic is introductory programming. How-                                 Banerjee et al. [1] discussed “different opportunities with use cases
                                         ever, for less popular topics, do LLMs perform as well, especially in                           of ChatGPT in augmenting the learning experience.” The paper
                                         technical topics that require precise arguments and are rigorous?                               proposes several methods in order to integrate the use of AI’s into
                                                                                                                                         the classroom, such as having students explain an answer given
                                         ∗ The first two authors contributed equally to this research.
                                                                                                                                         by ChatGPT, or explain the logic used by ChatGPT. Echeverría et al.
                                                                                                                                         [5] conducted an analysis of ChatGPT’s performance in computer
                                         Permission to make digital or hard copies of all or part of this work for personal or
                                         classroom use is granted without fee provided that copies are not made or distributed
                                                                                                                                         engineering exams, and found that ChatGPT can effectively pass that
                                         for profit or commercial advantage and that copies bear this notice and the full citation       class even though it contained many different types of questions.
                                         on the first page. Copyrights for components of this work owned by others than the                  Although not directly a CS topic, a closely related work to ours
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission   is that of Frieder et al. [3], about ChatGPT’s ability to answer dis-
                                         and/or a fee. Request permissions from permissions@acm.org.                                     crete math questions; this course is very often a pre-requisite for
                                         Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                         ToC. They determined that ChatGPT can reasonably well solve
                                         © 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN 978-1-4503-XXXX-X/18/06
                                         https://doi.org/XXXXXXX.XXXXXXX                                                                 1 http://chatgpt.com/
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                         Golesteanu, Vowinkel, and Dougherty


Table 1: Acronyms and shortened phrases used throughout                      The paper writing assessment is an extension based on the work
our ToC course and this paper.                                            of Dougherty [2], involving writing a research paper in small groups
                                                                          across the semester using knowledge gained in our ToC course.
         Acronym        Meaning                                           The formal group presentation is based on the fifth section of our
         CFG            Context-Free Grammar                              ToC course, namely NP-Completeness. Students had to give a full
         Count          Countability                                      proof based on a given proof from the Garey and Johnson textbook
         CNF            Chomsky Normal Form                               [4], which omits some details. Finally, the midterms and final are
         Dec.           Decidable                                         standard in-class exams.
         DFA            Deterministic Finite Automaton                       In Dougherty’s method (and ours), the paper topics are different
         DPDA           Deterministic Pushdown Automaton                  for each group; the same is true of the formal group presentation.
         Induct         Structural Induction                              Therefore, we determine whether ChatGPT can adequately pass the
         NFA            Nondeterministic Finite Automaton                 three exams. The results we find would be applicable to many other
         NP             Nondeterministic Polynomial Time                  institutions and course contexts because many ToC courses have
         PDA            Pushdown Automaton                                a very heavy weight to exams; further, these exams test students’
         PL             Pumping Lemma                                     baseline understanding of the material.
         Rec.           Recognizable                                         The first midterm exam only covered Section 1 (regular lan-
         Regex          Regular Expression                                guages), the second exam only covered Section 2 (context-free
         Rice           Rice’s Theorem                                    languages), and the final exam covered all 5 sections. As for individ-
         TM             Turing Machine                                    ual topics, Midterm 1 contained questions about induction, DFAs,
         Undec.         Undecidable                                       NFAs, NFA to DFA conversion, the Pumping Lemma for Regular
                                                                          Languages, and regular expressions. Midterm 2 contained questions
                                                                          about Context-Free Grammars, Pushdown Automata, conversions
undergraduate-level problems, but not graduate-level ones. Rele-
                                                                          between these two models, the Pumping Lemma for Context-Free
vant to our work, they used ChatGPT version 4, as it is more accurate
                                                                          Languages, and Deterministic Pushdown Automata. And finally,
than previous versions of ChatGPT; we will be using this version.
                                                                          the Final Exam contained questions including topics from Midterms
   Research was also done into using “prompt engineering” in or-
                                                                          1 and 2, and Turing Machines, Countability, Decidability, Undecid-
der to tailor ChatGPT’s responses to make them more accurate.
                                                                          ability, and NP-Completeness.
Velásquez-Henao et al. [8] describe “a methodology for optimiz-
ing interactions with Artificial Intelligence language models”. They
found that by using specific, creatively framed questions for ChatGPT,    3.2     Experiment 2: Question Database
they could effectively “elicit precise, accurate, and contextually
                                                                          We do note that ToC course contexts do vary in terms of topics
appropriate responses.” We adopt a similar approach of prompt
                                                                          tested, even within the five sections mentioned above. For exam-
engineering to improve ChatGPT’s responses.
                                                                          ple, some ToC courses may teach the Pumping Lemma for Regu-
3     COURSE CONTEXT AND METHOD                                           lar Languages, and some may instead choose the Myhill-Nerode
                                                                          equivalence relation. Further, the three exams may not be as com-
Our institution is a small liberal-arts college (SLAC) located in the     prehensive for detailing specifically in which concepts ChatGPT
northeastern United States, with between 30 and 50 CS students            performs well as they are a limited-time environment. Therefore,
graduating every year. Our ToC course consists of five main sec-          in addition to the results we find for our own specific ToC course,
tions: (1) regular languages, (2) context-free languages, (3) Turing      we also compiled many different ToC questions to cover a larger
Machines and Decidability, (4) Undecidability, and (5) NP-Completeness.   spectrum of what other ToC offerings may have.
The formal pre-requisites are discrete mathematics and data struc-           We focus on the first four sections of our ToC as these sections on
tures, a CS2 course; an informal pre-requisite is programming lan-        a macro level are very widespread across ToC course offerings. Here,
guages as it helps with some formal notation. There are no formal         we created 450 questions about basic topics in ToC, evenly divided
post-requisites, but students very often take a year-long capstone        among (1), (2), and (3) + (4). These questions were evenly divided
course and an Operating Systems course in the next semester.              amongst True/False, Multiple Choice, and Proof question types. The
   For both experiments and the results we give below, there are          design of these questions is suitable for an undergraduate-level ToC
many acronyms and phrases that we use for terms in our ToC course,        course; some are based on definitions of formal objects, some on
which are very standard. For simplicity, Table 1 has a mapping from       simple properties of the given language or model, asking ChatGPT
acronym or shortened phrase to its meaning; for a refresher on the        to provide examples of a language/model, etc. Here is a sample of
formal definitions of these terms, see Sipser [7].                        our generated questions:
3.1     Experiment 1: ChatGPT in our ToC Course                                 • "Is the complement of a regular language also a regular lan-
Student assessment for our course was divided up as follows:                      guage? Justify your answer."
    • Paper Writing: 450 points                                                 • "True or false: No arbitrarily long language can ever be reg-
    • Two Midterm Exams: 200 points total                                         ular."
    • Formal Group Presentation: 100 points                                     • "Prove that the language 𝐿2 = {0𝑎 1𝑏 : 𝑎 > 𝑏} is not regular
    • Final Exam: 250 points                                                      using the pumping lemma."
Can ChatGPT Pass a Theory of Computing Course?                                                 Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


      • "What is the formal definition of a Deterministic Finite Au-                 Table 2: Overall results for Experiment 1.
        tomata?"
      • "Give an example of a language that a DFA cannot model?"                                                   Initial    After Retry
      • "True or false: There exists an NFA such that it cannot be                 Midterm 1 (Section 1)           80.5%      93.0%
        converted to a DFA."                                                       Midterm 2 (Section 2)           87.5%      92.0%
      • "Give a recursive definition for the following set: the set 𝑋              Final Exam (Sections 1–5)       81.0%      88.6%
        of all strings in {0, 1}★ containing 00."                                  Average                         82.33%     90.33%
      • "True or False: the transition function of a pushdown au-
        tomata is the same as that of an NFA."
      • "True or false: the pumping lemma for context free languages       is the most accurate currently available model and we could upload
        can be used to shown that a language is context free.”             a document directly. Many of the questions require mathematical
      • "What is the formal definition of a context free grammar?”         notation; see the sample questions above for examples. However,
    We then fed all of the questions into ChatGPT using a set precur-      an easily readable notation is not directly compatible with ASCII
sor message before every prompt: “I will ask you a question to test        characters normally typed in on a keyboard. For Experiment 1, as
your academic theoretical computer science knowledge, answer to            we are using ChatGPT 4, we directly uploaded the exams as Word
the best of you abilities. Here it is:”. After receiving and recording     documents to ChatGPT to avoid this issue; for realism purposes,
the responses, we assigned them a grade from 0–4 based on a rubric.        these exams were identical to those given to the ToC students at
It is important to note that we did not grade simply the response in       our institution. For Experiment 2, we formatted the questions as
the case of True/False or Multiple Choice questions, but also the          close as possible to the formal notation with ASCII characters; no
reasoning and correctness behind the responses. Therefore, it is           question in this data set required a diagram for the prompt. For
possible that it chose the correct option, but did not earn a 4/4 due      example, consider the third example question above about showing
to the reasoning/correctness. The rubric is as follows:                    that 𝐿2 = {0𝑎 1𝑏 : 𝑎 > 𝑏} is not regular; what we instead used for
                                                                           this prompt was L2 = {0^a 1^b : a > b}. In both experiments,
      • 4: Totally correct and complete solution, covering all aspects
                                                                           only a few times did ChatGPT not understand the initial prompt, and
        of the question, and answered with enough depth to warrant
                                                                           every issue was corrected with a clarifying prompt. One example
        full points on an undergraduate-level ToC exam.
                                                                           is in Experiment 1 when ChatGPT interpreted 𝜎 𝑖 for 𝜎𝑖 .
      • 3: Mostly correct and mostly complete solution. This covers
        answers that are mostly correct, but have minor mistakes;
        these can include not fully answering minor parts of the ques-
                                                                           4   RESULTS
        tion, slight missteps in a proof, or otherwise making some         Table 2 contains our overall results for Experiment 1. For each of the
        small error which does not detract from the overall answer,        three exams, it contains the scores for both the verbatim questions in
        but would also not earn full points on an undergraduate-level      the exam and revised answers after trying again when given a hint
        ToC exam.                                                          as to why the answer it gave is wrong. Overall, ChatGPT performed
      • 2: This grade will be given to responses that have a some-         well on all three exams, earning over 80% in all experiments, and up
        what correct answer but include a major flaw. This could           to 93% after re-tries with helpful hints. The weighted average was
        include proofs that arrive to a correct conclusion or mostly       equivalent at our institution to a B- as the initial letter grade, and
        adhere to a correct logical flow, but make some large in-          an A- after re-tries. Each of the exams contains “main” questions
        correct assumption or step which detracts from the overall         and “bonus” questions; the listed scores in our results include these
        value.                                                             bonus questions for accuracy.
      • 1: This grade is the equivalent of a 3 but on the opposite side,      Table 3 contains our overall results for Experiment 2. It shows
        being a mostly incorrect or incomplete solution. The grade         the average best score for each topic tested. Here, “Average Max”
        covers responses which have some semblance of truth and            refers to the mean of all of the scores, where the score for each
        correctness, but still make a large error in either proof or       question is the best attempt on that particular question. Overall,
        justification.                                                     ChatGPT earned an 85% for Experiment 2; this is 91.5% on true/false
      • 0: Completely wrong answer. This grade will be given to a          questions, 87.3% on multiple choice questions, and 78.8% on proof-
        response if it is absolutely incorrect and does not even begin     type questions.
        to contain some truthful aspect or a path towards the correct
        answer.                                                            5 DISCUSSION
   ChatGPT was then given the opportunity to try again if it did not       5.1 Experiment 1 Discussion
score a 4/4. Basic feedback given to ChatGPT in the following form:        For brevity we will not include a discussion of each question indi-
“You got a x/4, improve the answer.”, with x being the appropriate         vidually, but rather include any discussion that will be of use for
rubric score. A maximum of three attempts were given for each              educators and/or gave surprising results.
question. The feedback is purposefully consistent and vague.                  ChatGPT could read state diagram pictures correctly, but this
                                                                           heavily depended on the picture’s format. For example, in the in-
3.3     Experimental Setup                                                 duction question for Midterm 1, students needed to observe a state
In both experiments, none of the questions used deception to induce        diagram of a DFA given as a JPG picture included in the exam Word
ChatGPT to produce false answers. We used ChatGPT version 4 as it          document; here, ChatGPT read that picture correctly. However, in
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                               Golesteanu, Vowinkel, and Dougherty


Table 3: Results for Experiment 2; we show the average maximum score obtained for each of the 450 questions we asked ChatGPT
including re-tries, as well as the average across question types and categories. Indicated cells show when the average grade is
below failing at our institution. For the meaning of each of the acronyms and short phrases, see Table 1.

                          Section 1                                     Section 2                      Section 3                Section 4
           Induct     DFA NFA PL               Regex      CFG    PDA     CNF DPDA       PL    TMs     Count Dec., Rec.       Undec. Rice         Avg.
 T/F       3.7        4.0   3.4     3.8        3.4        4.0    3.8     3.6     3.7   3.6    3.6     3.6      3.4           3.7       3.6       3.66
 MC        3.8        4.0   3.3     3.1        3.4        3.2    3.9     3.5     3.5   3.7    3.3     3.6      3.0           3.3       3.7       3.49
 Proof     3.2        3.7   3.0     3.4        2.4        2.5    2.5     3.6     3.4   3.4    2.4     3.5      3.4           3.4       3.4       3.15
 Avg.      3.57       3.90 3.23 3.43           3.07       3.23   3.40    3.57 3.53     3.57   3.10    3.57     3.27          3.47      3.57


the same exam’s third question, about a standard NFA to DFA con-                within a fixed number of steps. Much of ChatGPT’s reasoning here
version, the state diagram was directly drawn in Word using its                 involved loosely arguing why there was no such algorithm because
built-in shapes, and not as a JPG image. As a result, ChatGPT was un-           one needed to consider “all inputs”, even though there was a bound
able to correctly read the picture even after a re-try, although some           on how many tape cells can be visited (thus not all inputs even need
of the transitions and state names were correct; see Figure 1 for the           to be considered). In a majority of cases, however, ChatGPT either
initial table. In this case, we resorted to directly giving ChatGPT the         corrected or partially addressed its answers here after a re-try.
transition table, after which it performed the conversion correctly.               ChatGPT sometimes treated parts of problems as “black boxes”
For all other questions that used Word’s built-in equation editor,              even if they are referential to other parts. For example, the Final
ChatGPT read the equation perfectly.                                            Exam had a Rice’s theorem application question, where students
   ChatGPT’s approach for “wrong” answers was often very incre-                 needed to determine if that theorem applies. In this case, it does
mental, and never attempted to diagnose any core issue with its                 not because the input to the problem is a Turing Machine, and
initial reasoning. For example, Midterm 1’s second question in-                 the language involved the TM accepting two different strings; a
volved creating a small DFA for a given language. ChatGPT’s initial             given one, and the machine’s own description. This second string
solution with 4 states was incorrect, but was fixed after a re-try.             forces Rice’s theorem to not apply as it breaks one of the theorem’s
The interesting part here is that ChatGPT’s correct DFA still had 4             conditions. Like nearly all of our ToC students, ChatGPT treated the
states, whereas the “model” solution only needed 3; here, the 4th               TM’s own description as any other ordinary string not dependent
state was unreachable and so was “useless.”                                     on the input, and concluded the theorem could be applied.
   In general, as expected, ChatGPT performed well at questions                    There were a handful of cases where ChatGPT completely “un-
that are nearly identical to those that are posted online for which it          derstood” the prompt (i.e., the question was reproduced perfectly),
could train on, and very poorly on questions that are not. ChatGPT              and the exercise was standard, but nevertheless ChatGPT made
frequently ran into trouble even in the first case because small                a simple mistake. For example, the first question of Midterm 2
deviations in question phrasing can yield large changes in the                  involved creation of a CFG that involves breaking the problem
answer as the underlying meaning could change. For example,                     down into usage of three key components: closure under union,
consider the question: “True or False: the complement of the lan-               such as 𝐿1 ∪ 𝐿2 where both languages are context-free; nesting,
guage {𝑎𝑛 𝑏𝑛 𝑐 𝑛 : 𝑛 ≥ 0} is context-free.” The answer is true and              such as {𝑎𝑛 𝑏𝑚 𝑐𝑚 𝑑 𝑛 : 𝑛, 𝑚 ≥ 0}; and multiple parts, such as
is a standard exercise to prove it (as is similar to a true/false with          {𝑎𝑛 𝑏𝑛 𝑐𝑚 𝑑𝑚 : 𝑛, 𝑚 ≥ 0}. ChatGPT treated the “multiple part” as-
explanation question in Midterm 2); however, if the ending was                  pect of the question as a “nesting” one, although after a re-try it
changed to “deterministic context-free”, then the answer is false for           corrected the mistake.
a completely different reason.
   Often the culprit for poorly performed questions is the notion               5.2    Experiment 2 Discussion
of “universality,” in treating every case. For example, the Pumping
                                                                                Again for brevity, we will not discuss every question, but rather
Lemma question in both Midterms involved showing a given lan-
                                                                                highlights. ChatGPT had the highest average with DFA-related ques-
guage is either not regular or not context-free; to adequately do
                                                                                tions, and the lowest average with Regex-related questions. This
so, all possible cases of decomposing a string needed to be consid-
                                                                                could be due to the type of question in each category. The ques-
ered. In neither case did ChatGPT handle all such cases. Whenever a
                                                                                tions for DFA’s ended up being largely definitions, with a few being
question is “existential” in that one needs to perform an algorithm
                                                                                practice problems, as it is the first topic within Section 1 of our ToC
on a given DFA, or give an example CFG, then ChatGPT performs
                                                                                course, and its definition is more involved than the Regex defini-
much better. ChatGPT performed better still when questions were
                                                                                tion. Consequently, the problems for Regex were largely practice
phrased in a direct format without any ambiguity in the truth of
                                                                                problems that required a larger amount of creativity and critical
the answer, e.g., “Prove that 𝐿 is regular” vs. “True or False: 𝐿 is
                                                                                thinking, and not just surface-level application of the definitions of
regular.”
                                                                                topics.
   ChatGPT’s reasoning for proof-type problems is very rarely for-
                                                                                   There were rare cases where the explanation and reasoning
mal. An example is on the Final Exam where a short answer question
                                                                                were very close to being fully correct, but some small error lead to
involved determining if there is an algorithm for solving a given
                                                                                ChatGPT’s final answer being wrong; this was implied in our discus-
problem, such as checking if a Turing Machine halts on all inputs
                                                                                sion about Experiment 1. These cases occurred especially with the
Can ChatGPT Pass a Theory of Computing Course?                                               Conference acronym ’XX, June 03–05, 2018, Woodstock, NY




      (a) Original NFA for Midterm 1’s third question.                              (b) Initial Table from ChatGPT.

                       Figure 1: Example of ChatGPT’s issue with reading state diagrams directly made in Word.


proof questions, as there are many more opportunities within proof       the proof questions, and the prompt gives appropriate context to
steps to be wrong, particularly with induction, Pumping Lemma,           how ChatGPT should phrase its solutions to the questions.
and Undecidable reduction proofs.
    ChatGPT is often very malleable in its responses, which would        6   THREATS TO VALIDITY
make specific feedback prone to being interpreted as a hint, leading
                                                                         The largest possible threat to the validity of the results is the ac-
to ChatGPT changing its answer to fit what the feedback is saying.
                                                                         curacy of assigning scores based on the rubric, which was done
By being vague we attempt to ensure that the knowledge being
                                                                         by only the first and second authors. We mitigated this threat by
tested reflects only what ChatGPT currently possesses.
                                                                         having the third author independently verify the scores’ accuracy,
    ChatGPT sometimes altered its response with a worse score than
                                                                         as he has taught the course 8 times.
its initial guess by adding useless information to the question’s in-
                                                                            Another threat comes from a potential low quality of the tested
tent. For example, one question asked to determine if a given CFG
                                                                         questions. In order to mitigate this threat, we ensured that the
is ambiguous, which involved showing two leftmost derivations of
                                                                         questions came only from existing ToC resources, such as the course
the same string. ChatGPT understood this, but produced two deriva-
                                                                         textbook, class notes, pre-class readings, and former exams; the
tions of two different strings that were very similar to each other,
                                                                         latter three came from our institution.
but not the same. In the re-try, ChatGPT gave the same output along
with a derivation of another string that was completely unrelated
to what the question was asking.                                         7   RECOMMENDATIONS AND FUTURE WORK
                                                                         First we give our recommendations for educators who want to
                                                                         either alter their ToC course to accommodate potential use of LLMs
5.3    Effects of Prompt Engineering
                                                                         like ChatGPT by students, or to incorporate assessments utilizing
To understand prompt engineering’s influence, we determine its ef-       LLMs. Since we have shown that ChatGPT can effectively pass a
fects on the 30 NFA questions; Table 3 shows that the average score      ToC course, we recommend keeping assessments that are closed-
on these questions was 3.23. Using the same rubric as Experiment         resources, such as in-person exams, as the majority of the course
2, we tested the same questions with the following initial prompt:       grade. As our results show, an experienced ToC educator can still
       I want you to respond like you are the preeminent                 largely and safely use questions that have not been asked before that
       computer science professor in the world. You will give            still test the same fundamental concepts and theorems. However,
       intuitive and complete responses to my questions. You             an essential part of a successful ToC course is for students to think
       will be given a series of questions designed to test your         critically about claims, and to verify them. In spirit of this, we
       ability to answer such questions. You will respond                recommend to include an assignment that involves asking an LLM
       methodically and give your complete reasoning for                 to prove a claim from a previous assessment, and then have students
       every question. I will give you feedback with a score             point out every error within the LLM’s output.
       out of 4, and you will improve your answer using my                  As ChatGPT was rarely formal, we recommend requiring stu-
       feedback as a guide for how much your answer was                  dents to provide as-formal-as-reasonable proofs of their claims,
       incorrect.                                                        especially for reductions such as undecidable proofs. Although not
                                                                         necessarily new advice, we highly recommend educators inspect
   We found that the average score on these questions rose to            students’ homework submissions for key, specific details in their
3.53. On average, the true/false questions had an increase to 3.6        proofs. ChatGPT often includes all of the “boilerplate” correctly in
(vs. 3.4), the multiple-choice questions increased to 3.9 (vs. 3.3),     each proof type, but excludes important details, such as how a re-
and the proof questions increased to 3.1 (vs. 3.0). It is clear the      duction from one language to another exactly works. Further, we
prompt engineering had a much larger effect on the multiple-choice       recommend educators to require students create non-trivial state
questions. We believe this is the case because there are more options    diagrams as ChatGPT is unable to make them unless they are very
available vs. the true/false questions, but are not unconstrained like   small, and even these are directly written in ASCII.
Conference acronym ’XX, June 03–05, 2018, Woodstock, NY                                                                               Golesteanu, Vowinkel, and Dougherty


   Now we describe future work. Certainly a future work item                            [6] James S Sharpe, Ryan E Dougherty, and Sarah J Smith. 2024. Can ChatGPT Pass
would be to use the same method to other LLMs; we predict similar                           a CS1 Python Course? Journal of Computing Sciences in Colleges 39, 8 (2024),
                                                                                            128–142.
behavior in that proof-type questions will be done poorly, whereas                      [7] Michael Sipser. 2013. Introduction to the Theory of Computation (3 ed.). Course
algorithmic-type questions will be done well. Of course, the topics                         Technology, Boston, MA.
                                                                                        [8] Juan David Velásquez-Henao, Carlos Jaime Franco-Cardona, and Lorena Cadavid-
we chose are only a small subset of topics within ToC; one could                            Higuita. 2023. Prompt Engineering: a methodology for optimizing i nteractions
in principle test ChatGPT against topics such as computational                              with AI-Language Models in the field of engineering. (Nov. 2023). https://doi.org/
complexity theory.                                                                          10.15446/dyna.v90n230.111700
   In the advent of LLMs, it is ever more important to verify po-
                                                                                        Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009
tential proofs of claims, especially mathematical ones. For future
work, one type of question would be to determine if a given proof
is correct, and if not determine where the fundamental issue(s)
is/are; this was one of our Final Exam questions. For this question,
ChatGPT identified the correct proof step that caused the problem,
but had incorrect reasoning as to why it was wrong.
   One potentially great project is to build a LLM specifically for
ToC content, especially with explaining concepts, definitions, and
breaking down assigned problems at an undergraduate level with-
out giving away answers. From experience, students have most
issues with starting proofs and often forget pre-requisite content,
namely discrete math. Even though textbooks do provide such
needed content, such as Chapter 0 of Sipser [7], our students histor-
ically do not read such resources. Further, we would recommend
adding functionality to such an LLM that can walk through some
algorithmic process, such as NFA to DFA conversion. Such a project
would require a very large data set of accurate ToC content for
training, but we are not aware of such a resource if it exists.

8    CONCLUSION
In this paper we determined whether or not ChatGPT can pass a ToC
course. We accomplished this through two experiments: one based
on our course’s exams, and another based on a large set of questions
we developed. Overall, our experiments show that ChatGPT can
“pass” the course with between a B- and a B average letter grade.
ChatGPT does suffer from being largely unable to prove claims on
which it has not been trained, but can solve very standard exercises.

ACKNOWLEDGMENTS
The opinions in the work are solely of the authors, and do not
necessarily reflect those of the U.S. Army, U.S. Army Research Labs,
the U.S. Military Academy, or the Department of Defense.

REFERENCES
[1] Paramarshi Banerjee, Anurag Srivastava, Donald Adjeroh, Ramana Reddy, and
    Nima Karimian. 2023. Understanding ChatGPT: Impact analysis and path forward
    for teaching Computer science and engineering. (April 2023). https://doi.org/10.
    36227/techrxiv.22639705.v1
[2] Ryan E. Dougherty. 2024. Experiences Using Research Processes in an Under-
    graduate Theory of Computing Course. In Proceedings of the 55th ACM Technical
    Symposium on Computer Science Education V. 1 (Portland, OR, USA) (SIGCSE
    2024). Association for Computing Machinery, New York, NY, USA, 310–316.
    https://doi.org/10.1145/3626252.3630849
[3] Simon Frieder, Luca Pinchetti, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas
    Lukasiewicz, Philipp Petersen, and Julius Berner. 2024. Mathematical capabilities
    of chatgpt. Advances in Neural Information Processing Systems 36 (2024).
[4] Michael R. Garey and David S. Johnson. 1979. Computers and Intractability. Free-
    man and Company.
[5] Roberto Rodriguez-Echeverría, Juan D. Gutiérrez, José M. Conejero, and Álvaro E.
    Prieto. 2024. Analysis of ChatGPT Performance in Computer Engineering Exams.
    IEEE Revista Iberoamericana de Tecnologias del Aprendizaje (2024), 1–1. https:
    //doi.org/10.1109/RITA.2024.3381842
