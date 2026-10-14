                                                            Do AI models help produce verified bug fixes?
                                                 Li Huang, Ilgiz Mustaﬁn, Marco Piccioni, Alessandro Schena, Reto Weber, Bertrand Meyer
                                                                                              <ﬁrst.last@constructor.org>
                                                                                           Constructor Institute of Technology
                                                                                               Schaﬀhausen, Switzerland
                                        ABSTRACT                                                                1 INTRODUCTION
                                        Among areas of software engineering where AI techniques — par-          As the AI wave — particularly the LLM wave — upends ever more
                                        ticularly, Large Language Models — seem poised to yield dramatic        areas of industry and knowledge, software engineering is on the
                                        improvements, an attractive candidate is Automatic Program Re-          front line. Predictions that AI techniques will replace programmers
                                        pair (APR), the production of satisfactory corrections to software      run wild. While opinions diﬀer on whether it will truly be a re-
                                        bugs. Does this expectation materialize in practice? How do we          placement or just a complement, some of the transfer has already
arXiv:2507.15822v2 [cs.SE] 4 Aug 2025




                                        ﬁnd out, making sure that proposed corrections actually work? If        happened; as one example, the Microsoft CEO publicly stated that
                                        programmers have access to LLMs, how do they actually use them          as of April 2025 30% of the company’s code is “written by AI” [24].
                                        to complement their own skills?                                             A widely popular practice among developers is “vibe coding”,
                                           To answer these questions, we took advantage of the availabil-       which uses AI to assist programming, often producing large chunks
                                        ity of a program-proving environment, which formally determines         of the code. Software engineering is, however, more than coding.
                                        the correctness of proposed ﬁxes, to conduct a study of program         What about vibe designing, vibe specifying, vibe testing, vibe pro-
                                        debugging with two randomly assigned groups of programmers,             gram proving or — the focus of this article — vibe debugging?
                                        one with access to LLMs and the other without, both validating              Seeking help on the veriﬁcation side, including debugging, is a
                                        their answers through the proof tools. The methodology relied           natural move. In software engineering as in other disciplines, the
                                        on a division into general research questions (Goals in the Goal-       succession of reactions when one starts using LLM is often a see-
                                        Query-Metric approach), speciﬁc elements admitting speciﬁc an-          saw: alternated "Wow, see what it just did!" and "Wow, see how wrong
                                        swers (Queries), and measurements supporting these answers (Met-        it is — hallucinating again!" reactions. LLMs have been shown to
                                        rics). While applied so far to a limited sample size, the results are   produce fundamentally wrong solutions with airs of absolute as-
                                        a ﬁrst step towards delineating a proper role for AI and LLMs in        surance [21]. Hence the idea of complementing the impressive but
                                        providing guaranteed-correct ﬁxes to program bugs.                      occasionally wayward creativity of LLMs with the boring but re-
                                           These results caused surprise as compared to what one might          assuring rigor of formal veriﬁcation techniques supported by me-
                                        expect from the use of AI for debugging and APR. The contribu-          chanical proof tools. That is what the study reported in this article
                                        tions also include: a detailed methodology for experiments in the       does. We presented a group of programmers with:
                                        use of LLMs for debugging, which other projects can reuse; a ﬁne-       • A set of buggy programs.
                                        grain analysis of programmer behavior, made possible by the use         • A request to ﬁnd and correct the bugs.
                                        of full-session recording; a deﬁnition of patterns of use of LLMs,      • Access to a set of state-of-the-art LLMs — or, for the control
                                        with 7 distinct categories; and validated advice for getting the best      group, no such help.
                                        of LLMs for debugging and Automatic Program Repair.                     • A formal veriﬁcation environment (a mathematics-based pro-
                                                                                                                   gram prover) to validate the ﬁxes.
                                        CCS CONCEPTS                                                            We not only collected the results but video-taped the entire session
                                        • Software and its engineering → Formal software veriﬁca-               to try to gain detailed insights on whether LLMs help towards ﬁnd-
                                        tion; Software testing and debugging; Empirical software val-           ing bug ﬁxes, and, if they do, how programmers take advantage of
                                        idation; Error handling and recovery.                                   them. These are our two basic research questions, further detailed
                                                                                                                in section 3.
                                                                                                                    This study is a contribution to Automatic Program Repair (APR),
                                        KEYWORDS                                                                a thriving ﬁeld of research in the past two decades [22, 23]. A burn-
                                        Automatic Program Repair, Debugging, Integrated Development             ing question in that ﬁeld is the extent to which it can use AI for
                                        Environments, Software tools, Program transformation, Bug seed-         proposing corrections (“ﬁxes”) to buggy programs. We provide ele-
                                        ing, Software quality.                                                  ments of answer with a special feature: we take advantage of tech-
                                                                                                                nology that can formally verify proposed ﬁxes. In much APR work,
                                                                                                                the ﬁnal step of the APR process, checking that the proposed ﬁxes
                                                                                                                do indeed work and remove the bug, relies on testing. It is the
                                                                                                                weakest link in the traditional APR chain since it assumes that: (1)
                                                                                                                programmers produce a set of test cases, a tedious task; (2) these
                                                                                                                test cases are diﬀerent from those that led to identiﬁcation of the
                                                                                                                bug (otherwise, they risk overﬁtting: ﬁxing the program’s behavior
                                        Note: This article was entirely written by the authors. No part of it   only for the identiﬁed cases, without correcting the actual fault);
                                        was generated by an LLM or other automatic tool.                        (3) the test cases, even without blatant overﬁtting, are signiﬁcant.
XXX Conference, MMYYYY, ADDRESS                                           Li Huang, Ilgiz Mustafin, Marco Piccioni, Alessandro Schena, Reto Weber, Bertrand Meyer


A test is only the program’s result on one set of inputs, not a speciﬁ-        mostly at the stage of prototypes although some elements have
cation. In contrast, the present work validates ﬁxes through an au-            found their way into IDEs (development environments used by pro-
tomatic program prover. The downside is that programmers must                  grammers). The widely accepted typical APR cycle [16] includes
have written a precise speciﬁcation in the form of contracts [20],             four phases: fault localization, ﬁx generation, ﬁx validation (includ-
but then the proof is an actual mathematical guarantee of correct-             ing for correctness) and ﬁx selection (when several ﬁxes are being
ness. So the present work is not just evaluating the use of AI for             proposed).
generating bug ﬁxes, but its use for generating veriﬁed bug ﬁxes.                 Some ﬁx generation techniques are very sophisticated, but it
   The analysis applies to the research questions the GQM method               is a normal reaction for a researcher in the ﬁeld to compare the
of empirical software engineering, Goal-Question-Metric [5].                   results of the latest heuristics with what an LLM such as ChatGPT
   Section 2 deﬁnes basic APR terminologies. Section 3 presents                would produce, based on modern AI approaches (machine learning
the research questions (the goals) as well as the queries and metrics.         and generative techniques). The ﬁrst results are often impressive,
Section 4 presents related work. Section 5 introduces the tools used           suggesting that these approaches can be eﬀective at ﬁx suggestion.
for the study, and Section 6 the setup (participants, tasks, mode of           Beyond such an individual experiences, there has not been (to our
recording). Section 7 discusses limitations and threats to validity.           knowledge) any systematic evaluation of how good LLMs are at
Section 8 presents the measured results, complemented in section               generating valid and correct ﬁxes or — more realistically, since in
9 by more qualitative observations resulting from observing pro-               the current state of technology we cannot rule out the presence of
grammers’ behaviors: practices that hamper fruitful usage of LLMs              a human in the loop — at helping programmers obtain such ﬁxes.
(“antipatterns”, 9.1), LLM user “personalities” (9.2, advice for LLM           This question is the focus of the study.
usage (9.3.). Section 10 is the conclusion.                                       More speciﬁcally, we set out to obtain elements of answer the
2   TERMINOLOGY                                                                following two research questions, which for mnemonics we call W
                                                                               for “whether” and H for “How” (instead of the usual RQ1 and RQ2):
A malfunction in a program is called a failure. The underlying deﬁ-
ciency is a fault, also informally called a bug. (One fault can result          • W: In turning a buggy program into a correct one, is it fruitful
in several diﬀerent failures in various executions of the program.)               to use an LLM? (“Whether”.)
A proposed remedy to the fault, hoped to remove the fault, is a                 • H: If programmers do use an LLM for debugging, what is an
correction, also called a ﬁx, a repair or a patch.                                eﬀective process? (“How”.)
   A ﬁx is valid if it leads to a valid program (syntactically and
type-wise correct, in other words able to be compiled and run) and                The How question, H, assumes by default a positive answer to
removes the failure or failures that were observed. A valid ﬁx is cor-         the Whether question, W, although even in the case of a negative
rect if it actually removes the fault. The diﬀerence between “valid”           answer, suggesting that LLMs do not help, it is still interesting to
                                                                               elicit the “how” so as to understand where and why the LLMs fail
and “correct” is related to the problem of overﬁtting: if a number of
failures were identiﬁed, a valid ﬁx might remove these speciﬁc fail-           the programmer.
ures but still not address the underlying problem. (As an extreme                 The study and its analysis follow the GQM method, Goal-Query-
                                                                               Metric [7], of performing software engineering studies. In this ap-
but worthless solution, the ﬁx might just add a conditional instruc-
tion that produces the expected results in the identiﬁed cases, and            proach, we pursue some goals, deﬁned as an eﬀort to obtain an-
for all others proceeds as before.)                                            swers to speciﬁed questions; here the research questions W and
                                                                               H are the goals. For that purpose, one should deﬁne queries: spe-
   Most APR approaches are test-based: not only are failures iden-
tiﬁed as a result of test runs not producing the expected eﬀect, but           ciﬁc, well-deﬁned and concrete questions (often although not al-
the checking of a valid ﬁx for correctness also uses a set of test             ways Boolean), whose answers help address the underlying goals.
                                                                               To answer the queries, one deﬁnes metrics: criteria that can be as-
cases (a diﬀerent one, to avoid overﬁtting). This notion of correct-
ness is not absolute. For a ﬁrmer assessment of correctness, one               sessed by conducting a study, with a numerical value.
needs a proof-based approach, assuming the presence of a for-                     We deﬁned the following queries and the corresponding metrics
                                                                               as follows. “Q” is for queries, “M” for metrics.
mal speciﬁcation of each program element’s function, and a tool
to validate an implementation against it. In the tool stack described             For goal W: In turning a buggy program into a correct one, is it
in section 5 programs are written in Eiﬀel and include a speciﬁca-             fruitful to use an LLM?
tion in the form of “contracts”, and the AutoProof program prover               • QW-1 Can programmers solve more debugging tasks with/with-
can check an implementation — in particular, an implementation                    out LLM?
incorporating a ﬁx — against the contracts, through mathematical                    MW-1.a How many of the tasks are solved with LLM?
techniques and tools. (That notion of correctness is still not total:               MW-1.b How many of the tasks are solved without LLM?
it only expresses that the program is correct with respect to the               • QW-2 For tasks that programmers can solve with/without LLM,
given contracts, ignoring any other aspects; and it is dependent on               which takes longer?
the correctness of the proof tools themselves. But it is rigorously                 MW-2.a How long does each task solved with LLM take?
deﬁned and much more credible than a test-based view.)                              MW-2.b How long does each task solved without LLM take?
                                                                                • QW-3 For tasks that programmers cannot solve with/without
3   RESEARCH QUESTIONS                                                            LLM, which takes longer?
Automatic Program Repair (APR) has been around in the past decade                   MW-3.a How long does each task unsolved with LLM take?
and a half, resulting in a wide array of techniques and tools, still                MW-3.b How long does each task unsolved without LLM take?
Do AI models help produce verified bug fixes?                                                                                 XXX Conference, MMYYYY, ADDRESS


• QW-4 Do submissions contain more incorrect features with/with-                              MH-6.b Do experienced programmers use LLM output more/-
  out LLM?                                                                                    less often?
     MW-4.a How many tasks are incorrectly solved with LLM?
     MW-4.b How many tasks are incorrectly solved without LLM?
                                                                                         As a matter of methodology, the research questions as presented
• QW-5 Do LLMs help experienced programmers more/less than
                                                                                         above (goals, queries and metrics) were deﬁned as we were set-
  novice ones?
                                                                                         ting up the experiments, but before running them, and we did not
     MW-5.a How many problems do experienced programmers
                                                                                         modify them in any way afterwards, to avoid any a-posteriori con-
     solve with/without LLM?
                                                                                         ﬁrmation bias (sometimes known as HARKing, for Hypothezing
     MW-5.b How many problems do programmers with static ver-
                                                                                         After the Results are Known [15]).
     iﬁcation experience solve with/without LLM?
     MW-5.c How many problems do programmers with program-
     ming language experience solve with/without LLM?
• QW-6 Do LLMs help active programmers more/less than occa-                              4 RELATED WORK
  sional ones?                                                                           State-of-the-art large language models including ChatGPT, Claude,
     MW-6.a How many problems do active programmers solve                                Gemini, Mistral and DeepSeek have demonstrated signiﬁcant po-
     with/without LLM?                                                                   tential in supporting a variety of programming tasks, such as code
     MW-6.b How many problems do programmers with active                                 generation [3] and automatic program repair [35, 36]. Recent stud-
     static veriﬁcation practice solve with/without LLM?                                 ies have further investigated their applications to a more advanced
     MW-6.c How many problems do active programmers in the                               goal — achieving formally veriﬁed programs. Such eﬀorts include
     given programming language solve with/without LLM?                                  using LLMs to generate program speciﬁcations [18] and synthe-
  For goal H: If programmers do use an LLM for debugging, what is                        size code that conforms to speciﬁed requirements [6, 29, 30]. In the
an eﬀective process?                                                                     context of ﬁxing formally veriﬁed programs, Tihanyi et al. [31] es-
                                                                                         tablished a workﬂow similar to the present study, combining LLMs
• QH-1 What are the categories of the prompts used by the pro-                           with a formal veriﬁcation tool: they ﬁrst used Bounded Model Check-
  grammers?                                                                              ing (BMC) to detect vulnerabilities and produces counterexamples;
    MH-1.a In using LLMs for debugging, what are the categories                          they fed the outputs from BMC to the LLM for generating ﬁxes; the
    of prompts (determined empirically from the evidence and                             ﬁxes are then validated by BMC to conﬁrm their correctness.
    from previous published work)?                                                          As LLMs become increasingly integrated into everyday software
    MH-1.b For each task, how many categories of prompts do                              development workﬂows, providing an accurate estimation on their
    programmers use?                                                                     eﬀectiveness across diverse programming tasks becomes crucial. A
• QH-2 What are the components of the prompts for solved/un-                             user study [8] performed in the context of practical software devel-
  solved submission?                                                                     opment evaluated the impact of generative AI on developers’ pro-
    MH-2.a How many prompts contain natural language?                                    ductivity involving around 5,000 developers at Microsoft, Accen-
    MH-2.b How many prompts contain code?                                                ture and a Fortune 100 company. Their results show a 26% increase
    MH-2.c How many prompts contain tool output?                                         in completed tasks among developers using AI tools, with less ex-
    MH-2.d Is the task solved?                                                           perienced developers showing higher adoption rates and greater
• QH-3 How important is the phrasing of prompts in solving a                             productivity gains. Similarly, [13] studied a team of eight devel-
  bug?                                                                                   opers working on diverse projects over a period of twelve weeks.
    MH-3.a For each category of prompts, how many prompts                                The study suggested a positive value of Copilot (a code generation
    lead to a solved task?                                                               tool powered by the Codex model) in terms of monetization — the
    MH-3.b How many prompt categories lead to a solved task?                             company is willing to maintain the tool or pay to continue using it.
• QH-4 How do programmers interact with LLMs?                                            These studies demonstrate the potential of LLMs to improve soft-
    MH-4.a How many prompts do programmers send before solv-                             ware development eﬃciency in practice.
    ing a task?                                                                             Several human studies have explored the usability of Copilot in
    MH-4.b How many prompts do programmers send for unsolved                             programming education. Prather et al. [25] observed introductory-
    tasks?                                                                               level students using Copilot for a CS1 assignment. While most stu-
• QH-5 How do programmers use the outputs from LLMs?                                     dents felt Copilot helped them write code faster, they expressed
    MH-5.a How many times do programmers copy-paste a ﬁx                                 concerns about not fully understanding the generated code and be-
    produced by LLMs?                                                                    coming overly dependent on the tool. Similarly, Mailach et al. [19]
    MH-5.b How many times do programmers accept LLMs’ out-                               studied CS2 students using a chatbot to solve programming tasks
    put as the ﬁnal version?                                                             and found that those using the chatbot achieved 21% higher scores
• QH-6 What is the eﬀect of programmers’ experience1 on LLM                              on implementation tasks. [27] assessed ChatGPT-3.5 for solving
  use?                                                                                   programming tasks by novice programmers in higher education,
    MH-6.a Do experienced programmers use more/fewer prompts?                            ﬁnding that while students widely adopt GenAI, their engagement
                                                                                         varies from passive acceptance of solutions to critical use. [14] stud-
1 A more general version of this question would include age in addition to experience.   ied 33 learners aged 10–17 and identiﬁed common usage patterns
After giving it some consideraton we decided that it was nor essential to this study.    of AI code generators. Unlike the present study, which considers a
XXX Conference, MMYYYY, ADDRESS                                         Li Huang, Ilgiz Mustafin, Marco Piccioni, Alessandro Schena, Reto Weber, Bertrand Meyer


variety range of participant experience levels, those studies speciﬁ-
cally explore the experience of interacting with Copilot among pro-
gramming novices. In a setting similar to the present study, Wang
et al. [34] examined how users employ LLMs to solve simple cod-
ing problems and ﬁx real-world bugs in small-scale open-source
projects. Across these studies, interaction patterns reveal both the
perceived usefulness of LLMs and recurring issues such as halluci-
nations, overconﬁdence, and overreliance. Notably, none of these
user studies involve formal veriﬁcation; they assess the correctness
of generated code only through manual inspection or program ex-
ecution.
   Shein [28] asked three groups of MIT students to produce a pro-
gram in a language they did not know, FORTRAN, respectively
with two diﬀerent search engines and without any (but access to
search), a setting not unlike the present study’s. LLM-equipped stu-
dents performed much faster on program production, but the no-
LLM group beat them handily when it came to explaining it some                                   Figure 1: An AutoProof session
time later. Some results of the present study go in the same direc-
tion of suggesting that “LLMs favor the diligent” (section 10).
   Other research has focused on Copilot’s impact on task perfor-            • The Boogie prover [4, 17], itself relying on an SMT (Satisﬁability
mance and developer behavior. Vaithilingam et al. [33] found that               Modulo Theory) solver, currently Z3 [9].
participants using Copilot were less successful in accurately com-           For each task in the experiment (see next section), the user is pre-
pleting tasks compared to those relying on IntelliSense in VS Code,          sented with a pre-ﬁlled program, which is valid Eiﬀel but buggy:
though they appreciated Copilot’s ability to generate useful start-          clicking Verify will result in successful compilation but failed ver-
ing code — even when it sometimes led to “debugging rabbit holes.”           iﬁcation, with appropriate diagnostic such as a postcondition not
Barke et al. [3] identiﬁed two modes of interaction with Copilot:            being veriﬁed. The user can then correct the program and try again
acceleration mode, where developers use it to complete code they             (or give up).
already plan to write, and exploration mode, where they rely on                 Although testing tools such as AutoTest [2] are otherwise avail-
Copilot for unfamiliar tasks. However, over-reliance and the need            able in the EiﬀelStudio environment, no testing tool is included
to choose from multiple suggestions were found to cause cognitive            in the tool stack for the present work. The veriﬁcation performed
overload and hinder task completion. Although certain interaction            in this work is entirely static: no code is ever executed, no test
patterns observed are similar, this present study distinguishes it-          cases are ever needed. “Verifying” a class or one of its features
self by examining the usability of LLMs for a signiﬁcantly more              (routines, methods) means submitting them to a proof attempt based
advanced goal — ﬁxing formally veriﬁed software.                             on principles of Hoare logic as implemented by the AutoProof-
                                                                             Boogie-Z3 combination.
                                                                                This approach is made possible by the presence in the Eiﬀel code
5   TOOL STACK
                                                                             of built-in speciﬁcations known as contracts [20]. In the trivial spec-
The experiments are performed online, using a Web browser [11];              iﬁcation of Fig. 1, the contract includes a precondition (to deposit a
participants do not need to download any other software. The code            value into a bank account, that value must be positive) and a post-
for the examples is in Eiﬀel. All software processing is performed           condition (as a result of the deposit operation, the balance will have
by the AutoProof program veriﬁcation system for Eiﬀel (originally            been increased by that value). Contracts also include class invari-
presented in [32]). Participants access AutoProof through an instal-         ants, expressing consistency properties of all instances (objects) of
lation at our institution [1] (URL anonymized in this reference). In         a certain type (class). A program — possibly resulting from an at-
the Web-based version of AutoProof, the user enters a program                tempt at correcting a buggy ﬁrst version, as in the present set of
text; for each of the tasks, the program is pre-ﬁlled with a buggy           experiments — passes veriﬁcation if all creation procedures (con-
version. The user can then click the Verify button of the interface,         structors) of a class ensure its class invariant, and every exported
causing compilation and formal veriﬁcation. In the example below,            feature, executed with its precondition and class invariant satis-
from the AutoProof tutorial (not a task used in the present study),          ﬁed, terminates with its postcondition satisﬁed and the invariant
clicking Verify has resulted in three features being correctly ver-          satisﬁed again. (This characterization of Hoare-style semantics for
iﬁed (green) and two not, as the prover cannot prove that the re-            object-oriented programs summarizes the principal ideas; see for
spective feature ensures a clause of its postcondition and preserves         example the speciﬁcation of AutoProof [32] for the precise rules.)
a clause of the class invariant.
AutoProof relies on:                                                          6 STUDY SETUP
• The EiﬀelStudio compiler for Eiﬀel. Clicking Verify will ﬁrst cause        All participants in the study were volunteers, responding to calls
  a compilation. If the compilation produces an error, AutoProof             for participation sent to students and researchers in our institu-
  reports it (and does not attempt any veriﬁcation). If the compi-           tion, the Eiﬀel User Group, LinkedIn, and personal contacts. The
  lation succeeds, AutoProof proceeds with veriﬁcation.                      requirement was simply to have some programming experience, at
Do AI models help produce verified bug fixes?                                                                    XXX Conference, MMYYYY, ADDRESS


least basic knowledge of Eiﬀel (so as not to be derailed by language        • Stop after two hours at most.
comprehension issues) and to be willing to devote two hours to the          Examination of the results indicates that the instructions were clear
program debugging session, the exact time being chosen by each              and that the participants complied, although one (in the non-AI
participant freely, over a 5-day period (which included a week-end          group) forgot to share the screen, but still delivered the corrected
for convenience).                                                           programs. Participants were oﬀered no incentive to perform in any
    The invitation, in its entirety, stated: “Dear Colleague, to help       particular way (in particular, student participants’ performance had
with research on program veriﬁcation at” [name of our organization          no inﬂuence on their grade in any course); the only motivation, ex-
and research group], we are inviting to take part in a test next week.      pressed in the invitation email reproduced above, was to “help re-
It takes place in a 2-hour slot that you can pick, within those days (in-   search on program veriﬁcation”. Examination of the results suggests
cluding the week-end) to match your schedule. The task is to consider       that all participants took the tasks seriously and did their best to
a few buggy Eiﬀel programs and to attempt to correct the bugs. If you       perform at their best.
are willing to participate, please conﬁrm by email to [email address           The results available to the researchers, on which this article is
of the contact].” There was no other element; in particular there           based, include for each participant: the ﬁlled questionnaire; the so-
was no mention of artiﬁcial intelligence, LLMs etc. — only “pro-            lutions (corrected programs); the full video (usually two hours) of
gram veriﬁcation”. Assignment to a group mentioned "Group 1" or             the session (except for one participant as mentioned. The beneﬁt
"Group 2", with no reference to AI or no-AI. The same discipline            of the videos is that they allow us to follow the participants’ suc-
of not revealing the aims of the study, intended to avoid any bias,         cessive attempts and ideas, successful or not. The downside is that
was observed in subsequent interactions with participants prior to          this analysis is labor-intensive, since altogether it required watch-
their sessions; for example the email with a link to instructions           ing a total of some 50 hours of recording. Although aided by some
was simply titled “Program debugging study”.                                custom-produced scripts (allowing an analyst to observe speciﬁc
    Participants were divided into two groups. Given the relatively         events that occur at a speciﬁc time), the process is manual.
small size, we did not try to balance them explicitly by participant           The questionnaire [26] is short and intended to help analyze
characteristics but made a random assignment. The instruction               the results along diﬀerent categories. The questions addressed: age
sheet diﬀered between the groups: one prescribed the use of AI              (which would have been relevant with a more complete version of
tools, the other proscribed the use of any tools. The instruction           query QH6, but is ignored in the present work in favor of expe-
sheet templates, with identifying URLs removed, are available as            rience); number of hours spent weekly on, respectively, program-
part of the supplementary material of this article [12].                    ming (in general), Eiﬀel programming and LLM usage (ChatGPT,
    Each instruction sheet was actually generated diﬀerently for            Gemini etc.); duration in years of, respectively, programming expe-
each participant (of either group) since it included a link to a video      rience, Eiﬀel programming experience and static analysis experi-
session (MS Teams or Zoom) unique to the participant. The instruc-          ence; number of hours spent weekly on Eiﬀel programming; high-
tion sheet speciﬁes the following steps (elements in italics are from       est educational degree. The questions were single-choice, from a
the instructions, others are comments for this article):                    set of predeﬁned possibilities; their goal was mainly to allow the
                                                                            researchers to get an idea of the level of experience of the partic-
• Fill a short preliminary questionnaire. The text of the question-         ipants, typically grouped into two categories (experienced/novice
  naire remains available [26].                                             in Eiﬀel etc.) for the results of section 8.
• Connect to a video session at [URL of the participant’s unique               While the participants’ identity is known to the researchers,
  Teams or Zoom session]. Make sure to enable screen sharing (for           their anonymity is guaranteed for anyone else (including between
  our detailed analysis).                                                   the participants themselves) and the researchers are pledged not
• In your personal page, you will ﬁnd a list of links to speciﬁc tasks.     to reveal any information beyond what is contained in this article.
  Each task is a link to an AutoProof session, pre-ﬁlled with pro-          Both the article and its supporting material have been cleaned of
  gram text (as in Fig. 1).                                                 any element that could in any way serve to disclose such informa-
• For each task, click Verify. Since the program is buggy, veriﬁca-         tion.
  tion will fail with error messages.                                          29 people volunteered, which we split into a group of 15 (non-
• (For each task) attempt to correct the bug, and for each correction       AI) and one of 14 (AI). 25 of the volunteers actually performed the
  attempt click Verify to check the correctness of your proposed solu-      experiment. By a stroke of back luck the four no-shows were all
  tion. Here the instruction sheet, for both groups, included: You          from the same group (the AI group), causing a small imbalance.
  are allowed access to the AutoProof tool tutorial (including exam-        In all we have 10 exploitable AI-assisted results and 15 non-AI-
  ples of ﬁxes) at [URL of the tutorial at our institution.] No search      assisted (including the one without video).
  engines or any other docs or websites are allowed (with or without
  AI). But then they diﬀered:                                               7 THREATS TO VALIDITY
  – For group 1 (AI): “You are allowed interaction with the default         The preceding description of the setup sets the limits of what one
     model (GPT-4o mini) at https://duck.ai.”                               can expect from the results. The main limitation is the relatively
  – For group 2 (no-AI): You are not allowed interaction with any           small number of participants, although it is comparable to the size
     LLM (Large Language Model) or any other AI tool.                       in previous studies of similar topics (such as [3]). This article con-
• After each task, send your solution (working or not) to [email ad-        sequently refrains from any detailed statistical analysis (which the
  dress] using the “Share Code URL” button on the AutoProof page            numbers do not justify) and from drawing sweeping general con-
  and send the generated link.                                              clusions.
XXX Conference, MMYYYY, ADDRESS                                           Li Huang, Ilgiz Mustafin, Marco Piccioni, Alessandro Schena, Reto Weber, Bertrand Meyer


   There was no particular a priori thesis among the researchers.              charts below, slightly diﬀerent from the order in which they were
The motivation for the study was the observation, in some of the               presented to participants, is the increasing order of their diﬃculty
authors’ prior work on Automatic Program Repair, involving so-                 (based on our assessment, conﬁrmed by observation of the partic-
phisticated techniques of repair suggestion, that sometimes “just              ipants’ performance). Each corresponds to one of the problems in
asking ChatGPT” would yield what seemed like similar answers.                  [10]:
We wanted to explore whether that impression was borne out by
the facts. We can ﬁnd solace (and disappointment) in either the re-
sult that LLMs do very well or that they do not. We just wanted to              • Task 1. MAPLE_RECURSIVE_ABSOLUTE : The class deﬁnes an abs func-
ﬁnd out.                                                                          tion intended to return the absolute value of an integerx . The
   As noted in the previous section, all participants took the tasks              function incorrectly returns x instead of −x , failing to handle
seriously and did their best. One feature of the experiment that                  negative inputs properly.
may raise questions is that participants are known to researchers               • Task 2. FIND_IN_SORTED : The class implements a recursive binary
since they share their screens during the session. It is possible that            search to locate an integer in a sorted array, returning its index
some participants in the AI-assisted group wanted to show (for                    or 0 if not found. Injected bug: an incorrect conditional that pre-
reputation’s sake) that they could solve the problems without AI                  vents the function from correctly identifying found elements.
help. We have, however, no evidence that such a phenomenon took                 • Task 3. CALCULATOR: The class deﬁnes a calculate function that
place at all. Being able to observer the participants’ actual program-            performs basic arithmetic operations (+, -, *, /, %%) on two inte-
ming attempts in the recorded (through screen-sharing) sessions,                  gers based on the given operator, returning -1 for unsupported
while a tedious eﬀort for the researchers, yielded invaluable infor-              operations. Injected bug: in the implementation of the subtrac-
mation which would not have been available had we attempted full                  tion case, the code incorrectly performs addition instead of sub-
anonymity (without any guarantee of achieving it).                                traction.
   All participants in the LLM group used only one LLM, GPT-4o                  • Task 4. LINKED_STACK_MAKE_COMBINED : The class represents a linked
mini from Open AI, through the duck.ai interface. The study does                  stack structure with state-tracking booleans (before, after) and
not provide insights into how participants would have fared with                  pointers to elements, and includes a creation procedure to ini-
another LLM. We simply note that ChatGPT, of which GPT-4o is                      tialize the stack. Bug: the creation procedure incorrectly sets
part, is the dominant LLM oﬀering and often serves as the refer-                  before := True without properly initializing other attributes (e.g.,
ence in this ﬁeld.                                                                first_element and last_element ).
                                                                                • Task 5. TIME : The class models a 24-hour clock with operations
8   ANALYSIS OF THE STUDY’S OUTCOME                                               to set and retrieve time components, decrement time, run count-
This section examines the questions and metrics introduced in sec-                down timers, compute time diﬀerences, while maintaining strict
tion 3 as ways to address the research questions W and H. The met-                invariants on valid time values. Injected bug: the precondition
rics should be interpreted with caution given the small size of the               of the routine set_hour incorrectly allows hour to take the value
samples, but we believe that they do identify relevant trends. (The               24, violating the class invariant on the bounds on hour (0≤ hour
next two sections provide more observations.) The results are ex-                 and hour <24).
amined in the order of the research questions and the correspond-               • Task 6. QS_QUEUE: the class implements a ﬁxed-size queue (max
ing queries and metrics introduced in section 3. We provide the raw               size 100) with operations for inserting, deleting, searching, and
results when relevant, followed by our observations, particularly                 checking elements, while maintaining front and rear indices and
emphasizing outcomes that may go against expectations.                            tracking overﬂow/underﬂow exceptions. Bug: in the search rou-
   To enable more signiﬁcant visual inferences from the results                   tine, the loop incorrectly decrements index (index := index − 1)
comparing participants’ performance on various tasks, such as QW-                 instead of incrementing it, causing an inﬁnite loop or incorrect
2, QW-3 etc., the charts show these tasks in order, from left to right,           behavior when the key is not found.
of increasing diﬃculty (as assessed by us from observing the par-               • Task 7. PRIME_CHECK : the class provides a routine is_prime that
ticipants’ performance).                                                          checks if a given integer a is prime by testing divisibility from
   The diagrams use: blue for the group that used AI and orange for               2 up to a // 2. Bug: incorrect exit condition — when a \\ i = 0
the group that did not; ‘•’ for the average; and ‘×’ for the median; ⊤            (a divisor is found), Result is set to False but the loop does not
and ⊥ for the 80th and 20th percentile respectively. If a data point              break.
does not exist it is omitted in the diagram; for example there is no            • Task 8. ARRAY_FORCE_TO_EMPTY : the class implements an indexable
blue mark (in the diagram for QW-2 below) for Task 9 since no one                 container with arbitrary bounds and contiguous memory stor-
using AI solved it successfully.                                                  age, including a buggy routine intended to insert an element
   There are 9 tasks altogether, each consisting of an Eiﬀel class                into an empty array at index i: when the array is resized, the
with a buggy feature (method, routine). The source code, as well                  last element uninitialized (wrong default handling).
as the corrections for the bugs, are available at [10]. The tasks are           • Task 9. FIND_FIRST_IN_SORTED class deﬁnes a routine that attempts
of varying complexity and diﬃculty levels; they are drawn from                    to ﬁnd the ﬁrst occurrence of key in a sorted array using a bi-
several sources including common examples from formal veriﬁ-                      nary search strategy but contains logic errors: when the 𝑘𝑒𝑦 is
cation tutorials, bug databases, and examples from EiﬀelBase li-                  less than the middle element, it fails to shrink the search interval
braries that at some point of their existence contained actual bugs,              properly, potentially causing an inﬁnite loop or incorrect result.
corrected since. The order in which the tasks appear in the result
Do AI models help produce verified bug fixes?                                                                                                                                                                                                                                                                     XXX Conference, MMYYYY, ADDRESS


8.1                                  Goal W: In turning a buggy program into a                                                                     a number of “hallucination loops”, where the LLM was giving
                                     correct one, is it fruitful to use an LLM?                                                                    wrong advice and the participant got hooked with no prospect
                                                                                                                                                   of success. Section 9.1 discusses this phenomenon further.
• QW-1 Can programmers solve more debugging tasks with/with-
                                                                                                                                                                                                                                                                 Time used for unsuccessful fix
  out LLM?
    MW-1.a How many tasks are solved with LLM?                                                                                                                                        60

    MW-1.b How many of the tasks are solved without LLM?                                                                                                                              50




                                                                                                                                                    Time used (minutes)
                             7                                                                                                                                                        40
    Number of solved tasks




                             6                                                                                                                                                        30


                                                                                                                                                                                      20
                             5

                                                                                                                                                                                      10
                             4

                                                                                                                                                                                                  0
                             3
                                                                                                                                                                                                          k   1       k   2       k                          3         k   4       k                 5                k   6       k   7       k   8       k   9
                                                                                                                                                                                                      Tas         Tas         Tas                                  Tas         Tas                                Tas         Tas         Tas         Tas
  Observations: The result is a rough measure; subsequent charts
  provide more detailed views, reﬁned along various criteria. This                                                                               • QW-4 Do submissions contain more incorrect features with/with-
  one provides, however, the ﬁrst surprise: we would, perhaps naïvely,                                                                             out LLM?
  expected the AI group to fare better overall. Here all indications                                                                                 MW-4.a How many tasks are incorrectly solved with LLM?
  — minima, maxima, medians — are in the reverse order. A sim-                                                                                       MW-4.b How many tasks are incorrectly solved without LLM?
  plistic deduction from looking at just that ﬁgure would be “LLM                                                                                    MW-4.c How many tasks are correctly solved with LLM?
  help for debugging hurts rather than helps”. The results are too                                                                                   MW-4.d How many tasks are correctly solved without LLM?
  coarse-grained to allow such a conclusion but they point the                                                                                                                                                                                               2.0
                                                                                                                                                                                   7
  study in an interesting direction.



                                                                                                                                                                                                                                 Number of incorrect tasks
                                                                                                                                                    Number of solved tasks



                                                                                                                                                                                                                                                             1.5
  Variation is wider in the non-AI group, presumably (a conjecture                                                                                                                 6
  to be assessed better in results appearing below) because of the
                                                                                                                                                                                                                                                             1.0
  varying level of expertise.                                                                                                                                                      5

• QW-2 For tasks that programmers can solve with/without LLM,                                                                                                                                                                                                0.5
                                                                                                                                                                                   4
  which takes longer?
     MW-2.a How long does each task solved with LLM take?                                                                                                                          3
                                                                                                                                                                                                                                                             0.0

     MW-2.b How long does each task solved without LLM take?
                                                                         Time used for successful fix
                                                                                                                                                   Observations: The data is not great advertisement for AI support
                             35
                                                                                                                                                   for debugging. Non-AI-assisted programmers solve more tasks
                                                                                                                                                   correctly and fewer tasks incorrectly!
                             30
                                                                                                                                                 • QW-5 Do LLMs help experienced programmers more/less than
                             25                                                                                                                    novice ones?
    Time used (minutes)




                             20
                                                                                                                                                     MW-5.a How many problems do experienced programmers
                                                                                                                                                     solve with/without LLM?
                             15
                                                                                                                                                     MW-5.b How many problems do programmers with static ver-
                             10                                                                                                                      iﬁcation experience solve with/without LLM?
                                                                                                                                                     MW-5.c How many problems do programmers with program-
                                 5
                                                                                                                                                     ming language experience solve with/without LLM?
                                 0                                                                                                                                                                        Experience in programming                                                                                       Experience in Eiffel
                                         k   1       k   2       k   3       k   4       k   5       k   6       k   7       k   8       k   9
                                     Tas         Tas         Tas         Tas         Tas         Tas         Tas         Tas         Tas                                                              8                                                                                                       9


  Observations: The information on time spent is not very conclu-                                                                                                                                     7
                                                                                                                                                                                                                                                                                                              8
                                                                                                                                                                             Number of solved tasks




                                                                                                                                                                                                                                                                                     Number of solved tasks




  sive but suggests that LLM help is somewhat eﬀective for the                                                                                                                                                                                                                                                7
                                                                                                                                                                                                      6
  easier tasks. For the harder tasks, LLMs helps for Task 8, but
                                                                                                                                                                                                                                                                                                              6
  then no LLM-helped participants ﬁnished Task 9, the hardest.                                                                                                                                        5
• QW-3 For tasks that programmers cannot solve with/without                                                                                                                                                                                                                                                   5

  LLM, which takes longer?                                                                                                                                                                            4
                                                                                                                                                                                                                                                                                                              4
     MW-3.a How long does each task unsolved with LLM take?
                                                                                                                                                                                                      3                                                                                                       3
     MW-3.b How long does each task unsolved without LLM take?
                                                                                                                                                                                                          nced rienced rienced rienced                                                                            nced rienced rienced rienced
  Observations (the chart appears at the top of the next column):                                                                                          E                 xp e
                                                                                                                                                                                  rie                         e       e
                                                                                                                                                                                                           Exp on-Exp on-Exp
                                                                                                                                                                                                                              e
                                                                                                                                                                                                                                                                                 E   xp e
                                                                                                                                                                                                                                                                                          rie                         e       e
                                                                                                                                                                                                                                                                                                                   Exp on-Exp on-Exp
                                                                                                                                                                                                                                                                                                                                      e
                                                                                                                                                                                                              N       N                                                                                               N       N
  Here a worrying phenomenon seems to aﬀect hopes of using
  LLMs for correcting programs: spending far too much time in a                                                                                    There were too few people experienced in static veriﬁcation to
  useless direction. In observing participant sessions, we noticed                                                                                 draw a meaningful diagram for the associated measures.
XXX Conference, MMYYYY, ADDRESS                                       Li Huang, Ilgiz Mustafin, Marco Piccioni, Alessandro Schena, Reto Weber, Bertrand Meyer


  Observations: As noted above, the questionnaire assessed expe-                 MH-2.a How many prompts contain natural language? (An-
  rience in several ranges (0-2, 3-5, 6-10, over 10 years), which                swer: 97.7%.)
  we reduced to two in each case (5 years or more being consid-                  MH-2.b How many prompts contain code? (Answer: 48.3%.)
  ered “experienced”). For overall experience in programming, the                MH-2.c How many prompts contain tool output? (Answer:
  LLM-help advantage is blatant for novices (right two segments                  43.7%.)
  of the left box); for experienced programmers, the situation is             Observations: The total is more than 100% since a prompt can
  reversed, with non-LLM having a smaller but still clear advan-              contain elements of several kinds. Natural language is essen-
  tage. For experience in the programming language, the picture               tially always present. Code is present half of the time; so is the
  is less clear; given the wide spectrum of non-LLM results it is             output of AutoProof or EiﬀelStudio, which suggests that pro-
  diﬃcult to draw a ﬁrm conclusion, but it does seem that pro-                grammers like to feed some of the messages they get in order
  grammers with a strong experience in Eiﬀel (leftmost segment                to get feedback and explanations from the LLM.
  in the right box) can beneﬁt most from LLM use. We may conjec-            • QH-3 How important is the phrasing of prompts in solving a
  ture that, knowing the language very well — in addition to their            bug?
  general knowledge of programming, which is implied by their                    For each category of prompts, how many prompts lead to a
  speciﬁc experience in the language — they have a long practice                 solved task?
  of sifting through code in that language and correcting bugs, en-              MH-3.b How many prompt categories lead to a solved task?
  abling them to use an LLM suggestion much more eﬀectively                   Observations: There was too little data to answer this query mean-
  than a beginner through their ability to sort the weed from the             ingfully.
  chaﬀ (the good from the bad and ugly) by developing a strong              • QH-4 How do programmers interact with LLMs?
  hallucination-spotting and hallucination-avoiding instinct.                    How many prompts do programmers send before solving a
• QW-6 Do LLMs help active programmers more/less than occa-                      task? (Answer: 2.8 prompts on average.)
  sional ones?                                                                   How many prompts do programmers send for unsolved tasks?
     MW-6.a How many problems do active programmers solve                        (Answer: 3.6 prompts on average).
     with/without LLM?                                                        Observations: These ﬁgures suggest that the interaction with the
     MW-6.b How many problems do programmers with active                      LLM is meaningful and potentially useful. They also indicate
     static veriﬁcation practice solve with/without LLM?                      that LLMs are not genius debuggers: even for solving a task,
     MW-6.c How many problems do active programmers in the                    you need almost three steps on average; and before you realize
     given programming language solve with/without LLM?                       that the LLM does not help you have interacted between 3 and
  There were too few people that practiced Eiﬀel or static veriﬁca-           4 times.
  tion regularly to draw meaningful charts.                                 • QH-5 How do programmers use the outputs from LLMs?
                                                                                 How many times do programmers copy-paste a ﬁx produced
                                                                                 by LLMs?
8.2   Goal H: If programmers do use an LLM for                                   MH-5.b How many times do programmers accept LLMs’ out-
      debugging, what is an eﬀective process?                                    put as the ﬁnal version?
• QH-1 What are the categories of the prompts used by the pro-                Observations: We do not have the exact numbers for the given
  grammers? (clariﬁcation, expansion of previous, skepticism of               questions but we do have interesting information from watching
  previous answer, other categories use in the related works)                 the recorded sessions. Half of the participants did not copy-paste
    MH-1.a In using LLMs for debugging, what are the categories               at all from LLM answers. Those who did copy-paste did so less
    of prompts (determined empirically from the evidence and                  than once per task (except one person who copy and pasted 18
    from previous published work)?                                            times). Only once was the copy-pasted result part of the ﬁnal
    We identiﬁed the following categories, given here with their              version. We may safely deduce that in this experiment partici-
    percentage of use in the observed results (from watching the              pants do not slavishly use the LLM to give them a solution, but
    recorded screen-shared sessions):                                         as guidance; they still exercise their own judgment.
    ∗ Request for context clariﬁcation: 19.5%.                              • QH-6 What is the eﬀect of programmers’ experience on LLM
    ∗ Persona (a frequent recommendation in texts about “prompt               use?
       engineering”: tell the LLM that you are asking a question in              MH-6.a Do experienced programmers use more/fewer prompts?
       a certain role (as in “assume that I am a novice Eiﬀel pro-               (Answer: experienced programmers use 4.9 prompts on aver-
       grammer. How would I...”): 2.3%.                                          age, median 4; non-experienced programmers use 25 on aver-
    ∗ Other categories cited in the literature: not present in the               age, median 23.)
       experiment’s record.                                                      MH-6.b Do experienced programmers use LLM output more/-
    MH-1.b For each task, how many categories of prompts do                      less often? (Answer: experienced programmers use on aver-
    programmers use? Note: There is too little data. Categories                  age 0.9 times the output, median 0; non-experienced program-
    were not used.                                                               mers use 10.0 times the output, median 7.)
  Observations: The overall conclusion here is that programmers
  practice no prompt engineering beyond requesting clariﬁcations.          Observations: These results conﬁrm that experienced programmers,
• QH-2 What are the components of the prompts for solved/un-               when they use the LLM, get much faster to the point, presum-
  solved submission?                                                       ably because they understand the underlying programming issues
Do AI models help produce verified bug fixes?                                                                            XXX Conference, MMYYYY, ADDRESS


much better and can identify useful advice quickly, removing irrel-       • The prejudiced: Frames prompt around a prior hypothesis, such
evant or incorrect elements.                                                 as“it is the contract that is buggy”, steering the AI tool oﬀ-course.
                                                                          • The searcher: Uses LLM like a reference, encyclopedia or search
9     QUALITATIVE OBSERVATIONS                                               engine. Asks, for example, for explanations or reminders on lan-
                                                                             guage mechanisms, such as “What does [the keyword] detach-
Analysis of participants’ behavior, in addition to their actual code
                                                                             able mean in Eiﬀel?”)2 .The searcher remains in control and is-
outputs, yielded insights not captured by the mostly quantitative
                                                                             sues no queries requesting ﬁxes.
results of the preceding section. This further analysis is made possi-
                                                                          • The copy-paster: Queries the AI tool for ﬁxes in the form of
ble by examination of the 24 individual recordings of participants’
                                                                             code. Pastes responses back with little interpretation or adapta-
shared-screen sessions.
                                                                             tion. Prone to “hallucination loops” when veriﬁcation fails.
                                                                          • The follower: Accepts the AI tool’s suggestions and tries them
9.1     Antipatterns of LLM usage                                            out one-by-one. Unlike the copy-paster, works from these sug-
A real risk observed in a number of sessions is the hallucination            gestions rather than taking them unquestioningly.
loop. The AI tool makes an incorrect guess about how to correct           • The collaborator: Uses the AI tool as a form of pair debugger.
a bug; the programmer tries it, the result does not verify, the pro-         Supplies code and/or tool output, interprets LLM suggestions
grammer tries to ﬁx it, and gets into a fruitless try-verify-fail loop.      and decides to apply them or not. Adapts the generated code
The problem is that a ﬁx might look plausible but, in the current            from LLM; progressively enrich prompts. Our observations con-
state of generative AI, have no conceptual basis. A typical scenario         sistently indicate that this personality pattern is the most suc-
occurs for the most challenging tasks (8 and 9) of the present study,        cessful. It serves as the basis for our proposed ideal strategy (9.3
for which the LLM was unable to produce a correctly ﬁx. Veriﬁca-             below).
tion of its proposed code failed; usually, the participant still failed   It might intuitively seem that individuals will oscillate between
to understand the cause after several iterations.                         these attitudes, but that does not occur in our observations (with
   Another aberrant behavior, where using the LLM actually harms          one exception seen next: turning into a quitter). Throughout the
the programmer, is a variant of the hallucination loop, the noisy         experiments, each individual stuck to one of the patterns.
solution. The code proposed by the LLM actually contains the so-              Collaborators had the highest observed success rate (9̃1%), espe-
lution, but also includes, along with the correct elements, irrele-       cially when the veriﬁer failed to prove the proposed ﬁx and pro-
vant ones which prevent or delay the programmer from obtaining            vided a counterexamples from failed outputs, enabling them to ap-
a correct ﬁx. Copy-pasting the solution will not work. An exam-           ply selective edits rather than pasting wholesale. Copy-paster be-
ple of such behavior occurred in Task 9: the participant provided         havior was common (38%) but low-yield (only 3̃3% helpful) and as-
the buggy code to the LLM, which reported multiple issues (some           sociated with cascading compilation failures when the LLM rewrote
of them are irrelevant or spurious) and suggested several possible        large code blocks. Followers and Prejudiced had near-zero direct
ﬁxes; the participant tried out these suggestions one by one but,         success and had a high chance of turning into quitters, typically
before reaching the correct one, became frustrated and gave up.           after two negative high-eﬀort LLM sessions.
   More generally, the LLM often exhibits the neutrality ﬂaw: it
presents various solutions, some potentially useful, others worth-        9.3 Advice for LLM usage
less or harmful, without indicating their respective likelihood of be-    In addition to categories of LLM usage for debugging and repair,
ing helpful. In addition to pointing to an area of clearly needed im-     the extensive observation of participants’ tackling of the problems,
provement for LLMs, this phenomenon suggests that programmers             their attempts, their successes and their failures yields the follow-
using them should not just treat all their suggestions as equally         ing suggestions for a winning strategy of taking advantage of AI
valid but make a systematic eﬀort to rank them (see 9.3 below).           for these tasks.
   Watching the videos uncovers yet another antipattern: timid-              Smell a rat: Detect strong user framing (as in “the bug must be
ity. Some programmers, seeing that an LLM-generated ﬁx is not             in the contract”), appealing in their simplicity but useless, and look
working after a copyppaste, tried their luck by submitting to the         at alternative hypotheses. In particular, be on the lookout for in-
veriﬁer small variations of the AI solution without following a rig-      correct early hypotheses from the LLM, into which the Prejudiced
orously logical process. Poorly thought-out use of AI tools may           personality would jump head-on. They are the primary causes of
lead to this unproductive behavior.                                       frustration in LLM usage, observed again and again in our experi-
                                                                          ments.
9.2     Patterns of AI usage, and their eﬀectiveness                         Remove noise: Make your way through multi-issue early an-
Our observation of how participants interact with LLMs yield the          swers in which the correct ﬁx is present, but buried deep. The LLM
following categorization of programmer personalities. Our data            does not separate the essential from the auxiliary; you should.
shows that all categories arise in practice (a larger study would            Signal highlighting: When you see suggestions, rank them (to
make it possible to determine reliable percentages of their occur-        ﬁght the “neutrality” antipattern from 9.1). Visually highlight one-
rence). They are the following in — roughly — order of increasing         line high-conﬁdence ﬁxes so that they are not buried.
use of the AI tool (and increasing sophistication of that use).           2 In the void-safety mechanism of Eiﬀel, which guarantees the absence of null-pointer
                                                                          responsibility as part of the type system, a type is by default “attached”, guaranteeing
• The independent: Does not use AI support even when avail-               that its values will never be null (void); in the other case, that of a variable can have
  able.                                                                   a null value and hence must be protected, the type must be marked detachable.
XXX Conference, MMYYYY, ADDRESS                                           Li Huang, Ilgiz Mustafin, Marco Piccioni, Alessandro Schena, Reto Weber, Bertrand Meyer


   Too good to be true: Avoid the temptation to copy-paste the                  • The use of a program prover for conducting software engineer-
full solution (as the copy-paster would do), since it is likely to lead           ing studies, in the present case the assessment of Automatic Pro-
to high failure rate, often beginning with a compilation failure (the             gram Repair strategies, to provide an incontrovertible answer as
LLM is not an expert in the programming language).                                to the correctness or incorrectness of the results — as opposed
   From the present work also emerges a proposed best overall                     to the dominant use of tests (or, sometimes, manual inspection),
strategy, based on the collaborator personality pattern. where at                 from which any correctness conclusion is inevitably shaky.
each step you:                                                                  • The methodology. The GQM-based set of goals, resulting queries
                                                                                  and supporting metrics, devised before the experiment, proved
• Provide both the candidate code and the veriﬁer’s output.                       adequate for it without change, and capture, we believe, what
• Ask not just for a proposed solution but for the “diﬀ” (list of                 should be studied when assessing the value of AI support for
  individual diﬀerences) with the previous version.                               debugging and automatic program repair.
• Review the proposed ﬁx. (This rule is a general one: only make                • The use of full-session screen-sharing recordings. An argu-
  sure you understand a proposal before submitting it.)                           ment against this approach is the waiving of programmer anonymity
                                                                                  vis-à-vis the researchers (although anonymity is preserved for
Throughout this process, the programmer should constantly be on
                                                                                  the world at large in the results of this study). In addition, the
the alert for the risk of taking the wrong road (by following mis-
                                                                                  approach is labor-intensive, since someone must examine the
placed LLM advice). The old advice, “if you ﬁnd yourself in a hole,
                                                                                  videos3 ; with 25 participants it implied scrutinizing 50 hours,
stop digging”, applies. One should know when to stop ﬁddling with
                                                                                  and the approach may be hard to sustain for a study that would
an unveriﬁed answer in the hope that one more twist will make it
                                                                                  include a few hundred programmers. But for the present study
verify. Sometimes the best strategy is to start afresh, with a mix of
                                                                                  the ability to observe how programmers work, step by step, proved
LLM advice and personal thinking.
                                                                                  immensely valuable and yielded insights — on the use of prompts
                                                                                  and the use of copy-paste — that we would never have obtained
10     CONCLUSIONS                                                                by just looking at raw code produced by the programmers.
Section 7 stated the limitations of this study, particularly regard-            • The identiﬁcation of personalities of LLM usage and their pat-
ing sample size. Counterbalancing them is a degree of certainty                   terns (section 9.2).
not found in many Automatic Program Repair studies which rely                   • The identiﬁcation of the risk of hallucination loops through
on tests: here, through the use of a mathematically-based and tool-               which, particularly for non-experts, LLMs can take a program-
supported environment for proving program correctness, we can                     mer completely oﬀ-course and cause more harm than good.
determine unambiguously that a proposed ﬁx is correct (in the spe-              • The painful realization that the enthusing ﬁrst impression that
ciﬁc sense of satisfying the stated speciﬁcation, and within the lim-             an LLM can produce when one ﬁrst tries to apply it to program
itation of proof tools) or not.                                                   repair can be followed by disillusion, as the proposed ﬁxes may
                                                                                  have only the appearance of correctness.
10.1     Lessons on the use of LLMs for debugging                               • A delineation of the cases in which LLM can (nevertheless) help.
                                                                                • For these cases, validated advice on how to gain these beneﬁts,
One can derive a few lessons from the experiment. One stands                      including an eﬀective overall strategy
out clearly: whatever their merits for debugging, LLMs (at least
to judge by GPT-4o mini’s performance) are not a silver bullet. In             The overall lesson is that just as luck favors the prepared, AI helps
fact programmers not using the LLM perform better or as well                   the diligent. Hoping that feeding a buggy program into an LLM
on most counts. Two exceptions are, at opposite ends: complete                 will yield a correctly repaired version seems, in the current state of
novices, who can beneﬁt from the LLM to identify and correct sim-              generative AI, unfounded. As also evidenced by Shein’s MIT study
ple bugs; and programmers who are experts in the language, who                 of program construction [28], there is no substitute for thinking; at
would probably have found the corrections by themselves but can                every step you must remain on top of the process and understand
use the LLM to zoom in faster on the solution, saving some time.               what is being presented to you.
   The study also uncovers a major issue with LLM-based debug-                    If that is the case, software developers can take advantage of
ging: the hallucination loop (section 9.1). Hallucination for LLMs             LLM debugging help to move more quickly through the issues, sep-
is well-known, but in program debugging we encounter a particu-                arating the essential from the auxiliary, and develop an eﬀective
larly disruptive form: a suggestion that has all the looks of reason-          AI-aided process of program repair.
ableness, but misleads the programmer into a fruitless direction.              Acknowledgements. We are grateful to the following colleagues for
Often, expert programmers can smell a rat and ignore hallucinat-               their help: Eric Bezault, Joel Gamonez, Alejandro García, Karsten
ing answers, but novices are at a serious risk of failure.                     Heusser, Jimmy Jack Johnson, Adam Kasprzak, Viktoriya Kananchuk,
                                                                               Alik Khilazhev, Alexander Kogtenkov, Éric Lubat, Vivien Moreau,
                                                                               Anders Persson, João M. Rocha, Vladimir Shcherba, Kseniya Sidorova,
10.2     Contributions                                                         Catalin Toma. We are also indebted to Joaquim Soares and Ivan
We believe the present study, taking account of the numerical lim-             Turlakov of Constructor Institute of Technology for essential help
itations of the experiment, provides an important perspective and              in setting up the debugging sessions and making the results avail-
some clear results which we hope will inform and help others who               able. After the publication of a ﬁrst version of this article on arXiv,
may wish to pursue studies with a larger programmer sample en-
abling statistical inferences. The contributions include:                       3 It is not clear whether today’s AI tools can help in this analysis.
Do AI models help produce verified bug fixes?                                                                                       XXX Conference, MMYYYY, ADDRESS


a fruitful discussion took place on LinkedIn (https://bit.ly/4m30G5F);                [30] Teuber, S., Beckert, B.: Next steps in llm-supported java veriﬁcation. arXiv
we are grateful in particular to Hillel Wayne for pointing out an in-                      preprint arXiv:2502.01573 (2025)
                                                                                      [31] Tihanyi, N., Jain, R., Charalambous, Y., Ferrag, M.A., Sun, Y., Cordeiro, L.C.: A
consistency, now corrected, in the terminology.                                            new era in software security: Towards self-healing software via large language
                                                                                           models and formal veriﬁcation. arXiv preprint arXiv:2305.14752 (2023)
                                                                                      [32] Tschannen, J., Furia, C.A., Nordio, M., Polikarpova, N.: AutoProof: Auto-active
                                                                                           Functional Veriﬁcation of Object-Oriented Programs. In: International Confer-
REFERENCES                                                                                 ence on Tools and Algorithms for the Construction and Analysis of Systems
 [1] Web-based AutoProof installation, Anonymized                                          (TACAS). pp. 566–580. Springer (2015)
 [2] AutoTest, https://www.eiﬀel.org/doc/eiﬀelstudio/Using_AutoTest                   [33] Vaithilingam, P., Zhang, T., Glassman, E.L.: Expectation vs. experience: Evaluat-
 [3] Barke, S., James, M.B., Polikarpova, N.: Grounded copilot: How programmers            ing the usability of code generation tools powered by large language models. In:
     interact with code-generating models. Proceedings of the ACM on Programming           CHI conf. on human factors in computing systems (ext. abst.). pp. 1–7 (2022)
     Languages 7(OOPSLA1), 85–111 (2023)                                              [34] Wang, W., Ning, H., Qian, S., Zhang, G., Wang, Y.: Characterizing developers’
 [4] Barnett, M., Chang, B.Y.E., DeLine, R., Jacobs, B., Leino, K.R.M.: Boogie: A Mod-     behaviors in llm-supported software development. In: 2024 IEEE 48th Annual
     ular Reusable Veriﬁer for Object-Oriented Programs. In: Int. Symposium on For-        Computers, Software, and Applications Conference (COMPSAC). pp. 1168–1177.
     mal Methods for Components and Objects. pp. 364–387. Springer (2005)                  IEEE (2024)
 [5] Basili, V.R., Caldiera, G., Rombach, H.D.: The goal question metric approach. In:[35] Wei, Y., Xia, C.S., Zhang, L.: Copiloting the copilots: Fusing large language mod-
     Marciniak, J.J. (ed.) Encyclopedia of Software Engineering, vol. 1, pp. 528–532.      els with completion engines for automated program repair. In: Proceedings of
     Wiley (1994)                                                                          the 31st ACM Joint European Software Engineering Conference and Symposium
 [6] Brandfonbrener, D., Henniger, S., Raja, S., Prasad, T., Loughridge, C., Cassano,      on the Foundations of Software Engineering. pp. 172–184 (2023)
                                                                                      [36] Xia, C.S., Zhang, L.: Automated program repair via conversation: Fixing 162 out
     F., Hu, S.R., Yang, J., Byrd, W.E., Zinkov, R., et al.: Vermcts: Synthesizing multi-
     step programs using a veriﬁer, a large language model, and tree search. arXiv         of 337 bugs for $0.42 each using chatgpt. In: Proceedings of the 33rd ACM SIG-
     preprint arXiv:2402.08147 (2024)                                                      SOFT International Symposium on Software Testing and Analysis. pp. 819–831
 [7] Caldiera, V.R.B.G., Rombach, H.D.: Goal question metric paradigm. Encyclopedia        (2024)
     of software engineering 1(528-532), 6 (1994)
 [8] Cui, Z.K., Demirer, M., Jaﬀe, S., Musolﬀ, L., Peng, S., Salz, T.: The eﬀects of genera-
     tive ai on high skilled work: Evidence from three ﬁeld experiments with software
     developers. Available at SSRN 4945566 (2024)
 [9] De Moura, L., Bjørner, N.: Z3: An Eﬃcient SMT Solver. In: International Con-
     ference on Tools and Algorithms for the Construction and Analysis of Systems
     (TACAS). pp. 337–340. Springer (2008)
[10] Doe, J.: Experiment bugs (07 2025), https://anonymous.4open.science/r/experiment_bugs-4385
[11] Doe, J.: Experiment bugs (07 2025), https://anonymous.4open.science/r/CodeForge-9ED8
[12] Doe,           J.:        Experiment               instructions         (07         2025),
     https://anonymous.4open.science/r/experiment_instructions-087E/
[13] Gonçalves, C.A., Gonçalves, C.T.: Assessment on the eﬀectiveness of github copi-
     lot as a code assistance tool: an empirical study. In: EPIA Conference on Artiﬁcial
     Intelligence. pp. 27–38. Springer (2024)
[14] Kazemitabaar, M., Hou, X., Henley, A., Ericson, B.J., Weintrop, D., Grossman,
     T.: How novices use llm-based code generators to solve cs1 coding tasks in a
     self-paced learning environment. In: Proceedings of the 23rd Koli calling inter-
     national conference on computing education research. pp. 1–12 (2023)
[15] Kerr, N.L.: Harking: Hypothesizing after the results are known. Personality and
     Social Psychology Review 2(3), 196–217 (1998)
[16] Le Goues, C., Nguyen, T., Forrest, S., Weimer, W.: Genprog: A generic method for
     automatic software repair. Trans. on Software Engineering 38(1), 54–72 (2011)
[17] Leino,      K.R.M.,      Rümmer,         P.:     The       Boogie     2      Type     Sys-
     tem:        Design         and         Veriﬁcation           Condition         Generation,
     https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.146.4277
[18] Liu, Y., Xue, Y., Wu, D., Sun, Y., Li, Y., Shi, M., Liu, Y.: Propertygpt: Llm-driven for-
     mal veriﬁcation of smart contracts through retrieval-augmented property gen-
     eration. arXiv preprint arXiv:2405.02580 (2024)
[19] Mailach, A., Gorgosch, D., Siegmund, N., Siegmund, J.: “ok pal, we have to code
     that now”: interaction patterns of programming beginners with a conversational
     chatbot. Empirical Software Engineering 30(1), 34 (2025)
[20] Meyer, B.: Applying “Design by Contract”. Computer 25(10), 40–51 (1992)
[21] Meyer, B.: Ai does not help programmers. Blog article at Communications of the
     ACM (June 2023)
[22] Monperrus, M.: Automatic software repair: A bibliography. ACM Computing
     Surveys (CSUR) 51(1), 1–24 (2018)
[23] Monperrus, M.: The living review on automated program repair. Ph.D. thesis,
     HAL Archives Ouvertes (2018)
[24] Nadella,        S.:     Microsoft         ceo        says      up     to       30%      of
     the       company’s         code         was          written      by       ai     (2025),
     https://techcrunch.com/2025/04/29/microsoft-ceo-says-up-to-30-of-the-companys-code-was-written-by-ai/
[25] Prather, J., Reeves, B.N., Denny, P., Becker, B.A., Leinonen, J., Luxton-Reilly, A.,
     Powell, G., Finnie-Ansley, J., Santos, E.A.: “it’s weird that it knows what i want”:
     Usability and interactions with copilot for novice programmers. ACM transac-
     tions on computer-human interaction 31(1), 1–31 (2023)
[26] LLM Debugging Study Questionnaire, https://forms.gle/1kﬁPynkUdsvLfh6A
[27] Scholl, A., Kiesler, N.: How novice programmers use and experience chatgpt
     when solving programming exercises in an introductory course. In: 2024 IEEE
     Frontiers in Education Conference (FIE). pp. 1–9. IEEE (2024)
[28] Shein,     E.:      The    impact       of      ai     on     computer     science     ed-
     ucation.        Communications             of       the       ACM        (July      2024),
     https://cacm.acm.org/news/the-impact-of-ai-on-computer-science-education/
[29] Sun, C., Sheng, Y., Padon, O., Barrett, C.: Clover: Closed-loop veriﬁable code
     generation. In: Int. Symposium on AI Veriﬁcation. pp. 134–155. Springer (2024)
