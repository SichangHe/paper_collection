                                                                    Lost at C: A User Study on the Security Implications
                                                                         of Large Language Model Code Assistants

                                             Gustavo Sandoval∗, Hammond Pearce∗, Teo Nys, Ramesh Karri, Siddharth Garg, Brendan Dolan-Gavitt
                                                                                   New York University
arXiv:2208.09727v4 [cs.CR] 27 Feb 2023




                                                                     Abstract                                      AI (LLM)                    Code
                                         Large Language Models (LLMs) such as OpenAI Codex are
                                                                                                                                                        ?
                                                                                                                                Reads
                                         increasingly being used as AI-based coding assistants. Un-
                                         derstanding the impact of these tools on developers’ code is                             User
                                         paramount, especially as recent work showed that LLMs may
                                         suggest cybersecurity vulnerabilities. We conduct a security-             Suggests                  Writes         Security
                                         driven user study (N=58) to assess code written by student                                                          Tests
                                         programmers when assisted by LLMs. Given the potential
                                         severity of low-level bugs as well as their relative frequency     Figure 1: What is the security impact of LLM assistance?
                                         in real-world projects, we tasked participants with implement-
                                         ing a singly-linked ‘shopping list’ structure in C. Our results
                                                                                                           with LLM based code assistants. While programmers prone
                                         indicate that the security impact in this setting (low-level C
                                                                                                           to automation bias might naively accept buggy completions,
                                         with pointer and array manipulations) is small: AI-assisted
                                                                                                           other developers might produce overall less buggy code by
                                         users produce critical security bugs at a rate no greater than
                                                                                                           only accepting safe suggestions and using time saved to fix
                                         10% more than the control, indicating the use of LLMs does
                                                                                                           other bugs.
                                         not introduce new security risks.
                                                                                                              This leads us to the key question motivating this work:
                                                                                                           Do developers with access to an LLM-based code comple-
                                         1     Introduction                                                tion assistants produce less secure code than the code pro-
                                                                                                           duced by programmers without this access (Fig. 1)? An
                                         Large Language Models (LLMs) are deep neural networks             affirmative answer to this question could be a significant
                                         trained on massive text corpora [1, 2] to learn the underly-      showstopper for LLM based code assistants. To answer this
                                         ing distribution of natural language or structured text. When     question, we perform the first security-motivated randomized
                                         trained on code, LLMs can be used for code completion, bug        trial comparing programmers with and without access to a
                                         fixing, and summarization [3–5], useful features for devel-       Codex-based code completion assistant powered by OpenAI’s
                                         opers. Recent offerings are thus commercializing LLMs for         code-cushman-001 LLM.
                                         code, including GitHub Copilot, which after its public release
                                                                                                              Our user study in Section 3 had 58 computer science un-
                                         in June 2022 added 400,000 new users in just two months [6].
                                                                                                           dergraduate and graduate students with programming back-
                                            However, recent work has shown that LLM completions
                                                                                                           grounds split randomly into ‘control’ (no Codex LLM access)
                                         may contain critical security vulnerabilities [7, 8]. This sug-
                                                                                                           and ‘assisted’ (with Codex LLM access) groups. Given the
                                         gests that despite gain in developer productivity, LLM based
                                                                                                           relative frequency of memory-based errors in low-level lan-
                                         code assistants should be used with caution (or not at all) due
                                                                                                           guages such as C and C++ (≈70 % of CWEs assigned by Mi-
                                         to security concerns. This prior work has evaluated the secu-
                                                                                                           crosoft each year [9]), as well as their relative severity (classes
                                         rity of LLM code assuming that its entirely generated by the
                                                                                                           of memory related bugs take many of MITRE’s ‘Top 25 Com-
                                         LLM (we will call this the autopilot mode). In practice, code
                                                                                                           mon Weakness Enumeration (CWE) Most Dangerous Soft-
                                         completion LLMs assist developers with suggestions that they
                                                                                                           ware Weaknesses’ list, including positions #1 and #5 [10]),
                                         can accept, edit or reject—a real-world security evaluation
                                                                                                           we design a study where the participants were (t)asked to com-
                                         must account for the role of developers and how they interact
                                                                                                           plete a set of 12 functions that perform basic operations on a
                                             ∗ Equal Contribution                                          linked list representing a “shopping list” in C. To understand
the programming patterns in both groups, we created a cloud-      this result was not statistically significant—possibly because
based integrated development environment (IDE) that links to      some participants did not complete the tasks in the allotted
a Codex LLM in the back-end to behave like GitHub Copilot.        time, or due to the small sample size. They found Copilot
The IDE logs user inputs and interactions with Codex LLM          generates code a lot quicker than typing or finding it from
at a fine-grain. Using data from the user study, we investigate   other sources. However, they also theorize that it is often
the impact of LLMs across three research questions:               buggy and so time saved writing code may then need to be
                                                                  spent in debugging Copilot generated code.
RQ1: Confirm motivation for this research: Does an AI code           Imai [21] tasked a group of developers (N=21) to imple-
 assistant help novice users write better functional code?        ment code for a ‘minesweeper’ game. The study participants
RQ2: Given functional benefits, does the code that users          were randomly asked to use (1) GitHub Copilot as a code
 write with AI assistance have acceptable incidence rate of       assistant, (2) a human pair programmer as the ‘driver’ control-
 security bugs vis-a-vis code written without assistance?         ling the computer and writing the code, and (3) a human pair
RQ3: How do AI assisted users interact with ply vulnerable        programmer as the ‘navigator’ assisting ‘driver’, and reading
 code suggestions—i.e., where do bugs originate in an LLM-        the code the ‘driver’ is writing and examining it for issues.
 assisted system?                                                 The study concluded that Copilot tended to result in more
                                                                  lines of code than with the human-based pair-programming
   Our analysis, presented in Section 4, addresses these ques-    in the same amount of time. However, the quality of code pro-
tions both quantitatively and qualitatively. We examined com-     duced by Copilot was lower. Pair-programming with Copilot
pleted code for functionality and security, using manual and      does not match the profile of human pair-programming. The
automated methods. We sought to examine the code for bugs         study did not examine whether or not Copilot improves over
from the Common Weakness Enumeration (CWE) [11] tax-              a developer without a pair programmer.
onomy. We find that in our setting (a low-level linked list in       A study by Ziegler et al. [22] from GitHub examines user
C implemented by computer science students), the security         perspectives on productivity during usage of GitHub Copilot.
impacts are minimal. We confirm existing findings on the          Here, a large number of users running the GitHub Copilot
productivity benefits of AI-assistance (RQ1), while finding       technical preview were invited to complete a survey on their
that the AI-assisted group produced security-critical bugs at a   perspectives, and a subset of these responded (N=2,047). Here,
rate no greater than 10 % higher than the control group (non-     84% (1,724-out of-2,047 completions) self-scored a SPACE-
assisted) (RQ2). When investigating the origin of bugs within     type survey with a positive perspective aggregate. They felt
the assisted users (RQ3), 63 % of the bugs originate in code      Copilot had a more beneficial effect on their productivity than
written by humans and 36 % of the bugs were present in taken      a negative one. Using internal metrics collected by the tool,
suggestions. In the interests of open science we provide all      GitHub authors determined that the number of suggestions
data open source in [12].                                         accepted by the users was the greatest indicator of the positive
                                                                  perspective. The more suggestions a developer accepts, the
                                                                  more likely they feel the tool makes them productive. Github
2     Background and related work                                 Copilot user’s acceptance rate of suggestions is 6.6% per hour.
                                                                     A Google study by Tabachnyk et al. [23] used a large num-
2.1    AI code assistants target productivity                     ber of developers (N>10,000). They found that since the de-
Academic and commercial AI code assistant tools are prolifer-     ployment of a proprietary LLM, the fraction of all code added
ating. Examples include OpenAI’s Codex [3, 5], AI21’s Jurra-      by the LLM has increased to 2.6%, and developers have re-
sic J1 [13, 14], Salesforce CodeGen [15] and CodeBERT [16].       duced their coding iteration duration by 6 % and reduced their
These LLMs can write functionally correct code, with studies      number of context switches by 7 %, i.e. the LLM has had a
showing capabilities in solving introductory programming          measurable (and positive) impact on developer productivity.
tasks [17, 18] and algorithmic challenges [19]).
   Recent user studies examine the effects of code LLMs           2.2    Prompts to suggestions: How LLMs code
on developer productivity. Vaithilingam et al. [20] measured
productivity from a group of developers (N=24) completing         LLMs such as the GPT-type transformers which underpin
code tasks in Python. Each developer used GitHub Copilot to       Codex [3] function by building probabilistic sequences of to-
complete one task and the default non-AI based IntelliSense       kens based on the frequency of observed tokens in the training
assistant to complete a different task and discussed which they   data [2]. In other words, they act as an ‘autocomplete’ tool.
preferred on three tasks of increasing difficulty. The exact      Given some input sequence, they will find the most probable
task/assistant choice were randomized across participants.        next token(s) in the output sequence. For instance, if an LLM
Overall, the participants preferred using Copilot as it helped    is given “int main(int argc, char *” as the ‘prompt’,
them get started quicker. Analysis showed that the average        it would likely return “argv” as the ‘suggested’ next token,
task completion time when using Copilot was shorter although      as this is a very common sequence in C programs.
   In an LLM, ‘tokens’ refer to common sets of individual              Additional security concerns come from code beyond just
characters. These are used via ‘byte pair encoding’ [24] to         their execution. The primary issue concerns code plagia-
allow the LLMs to ingest more text into their fixed-size input      rism [17]. Commercial organizations and academic institu-
windows. This allows the LLM to process more information.           tions are worried that employees and students may misrepre-
Codex builds on the same tokenizer as GPT-3, extending it           sent AI code LLM outputs as their own. Although outside the
to include tokens for runs of whitespace. This makes it work        scope of this work, code licensing issues [28–30] where the
better for code indentation [3]. The average token for Codex        LLM may be trained over open-source licenses which impose
is about four characters.                                           requirements on their derivations. As the legal status of code
   LLMs are not restricted to predicting just one token at a        produced by LLMs is an open question, this could expose end-
time, however. They are autoregressive, feeding predictions         users to legal issues. Corporations may disallow employees
back in on themselves and performing searches across chains         from using public LLMs. On the other hand, in the university
of tokens (e.g. beam search is used in GPT-3 [1]). In the code-     setting, it may be the case that using an AI assistant could
writing LLMs, this allows for them to write large quantities        be academic dishonesty, especially if used in an examination
of code ‘at once’. For example, given the right input prompt        setting (e.g. a solitary assignment). One example highlighting
containing a well-defined function signature, an LLM may            this was presented in [31], where students equipped with a
produce an entire function body.                                    code-writing GPT-J LLM passed introductory programming
                                                                    assignments without triggering suspicion from MOSS [32],
                                                                    a commonly-used anti-plagiarism software. In addition to
2.3    Security concerns of LLM-generated code                      the plagiarism-detection issue, they conclude that the LLMs
Unfortunately, the somewhat naïve mechanisms that underpin          will not be stumped with novel questions—GPT-J could solve
LLM suggestion generation discussed in the previous sub-            problems outside the training set. When considering prose,
section have been shown to problematic outcomes from a              rather than code, these issues have also been observed. Wahle
security standpoint, for two primary reasons: (1) LLMs may          et al. [33] suggest using LLMs trained to detect plagiarism,
be trained over potentially insecure or buggy code (and will        and demonstrate that this technique can have greater success
then reproduce those insecurities/bugs), and (2) Code which         than typical tools such as TurnItIn. However, this has not yet
may be secure in isolation may be insecure depending on the         been demonstrated for code.
sequence it is executed in relation to other pieces of code.
   For an example of (1), consider the use of the ‘MD5’ hash        2.4    Evaluating code security
algorithm once widely used to protect secure information such
as passwords. MD5 has been cryptographically broken, and            There are several techniques to determine the security of
so should no longer be used. However, code examples with            a piece of code. Identified bugs can be classified into the
MD5 remain on open source repositories. Therefore LLMs              aforemntioned CWE taxonomy [11].
learn to (incorrectly) suggest MD5 for hashing passwords.              Static Analysis tools detect security-related bugs attempts
For (2), consider storing text in a buffer. This can occur safely   statically at compile-time. Source code is parsed and an-
using functions such as snprintf. However, if that buffer           alyzed for buggy design patterns. Common techniques in-
was just free-d, then the same line of code calling snprintf        clude access-control analysis, information-flow analysis, and
would result in a use-after-free vulnerability.                     checks for application-programming-interface (API) con-
   The issue of GitHub Copilot’s code suggestions contain-          formance [34]. Common static analysis tools are listed by
ing security vulnerabilities was first studied by Pearce et         OWASP [35], and include GitHub CodeQL [25].
al. [8]. They found that as measured by the GitHub Cod-                Run-time analysis can also occur by using tools
eQL [25] static analysis tool, 40 % of the suggestions in           such as debuggers and sanitizers like ‘Address Sanitizer’
relevant contexts contain security-related bugs (i.e. from          (ASAN) [36] and ‘Undefined Behavior Sanitizer’ (UBSAN)
MITRE’s Common Weakness Enumeration (CWE) taxon-                    [37]. These can identify bugs and instrument the underlying
omy [11]). Likewise, Siddiq et al. [7] showed that for the Hu-      code at compile time to help identify the root cause, providing
manEval dataset (which examine functional capabilities and          detailed information about the locations and causes of any
not security) GitHub Copilot emits certain CWEs in around           errors. Unlike static analysis, sanitizers require a proof-of-
2 % of cases as measured by Bandit analysis tool [26].              concept ‘crashing’ inputs which trigger bugs. These can be
   That said, LLMs may also generate secure code as a re-           found by ‘fuzzers’.
placement for insecure code [27] (i.e. may be used for bug             Fuzzers run the program on concrete, randomly generated
patches). Although this was only shown to reliably work for         inputs in an attempt to uncover bugs and vulnerabilities. Bugs
small synthetic examples rather than for case studies taken         found with fuzzing are generally guaranteed to be true pos-
from real-world vulnerabilities, where the results were incon-      itives, and the proof-of-concept input that demonstrates the
clusive, this indicates that the issue of insecure code sugges-     bug can be helpful to developers in fixes. Since the release of
tions by LLMs remains unresolved.                                   “American fuzzy lop” [38] in 2013, fuzzing has received sig-
nificant attention. Google’s oss-fuzz [39] provides continuous        tions and how to accept or reject them (‘assisted’ group), or
fuzzing for over 650 open source projects. Standards bodies           that they would not get suggestions ( ‘control’ group). They
such as NIST recommend fuzzing for secure development                 were told that when they thought they were done, they should
practices [40]. Major academic security conferences typically         upload the program and complete an exit questionnaire for
feature a dozen or more papers on fuzzing each year. While a          demographic information. We analyzed the completed code
full treatment is beyond the scope of this paper, we direct the       for functional and security correctness. This is discussed in
reader to the survey by Manes et al. [41].                            Section 4. Our institutional review board approved this study.
   Manual analysis: Despite the pressing need for automated
tooling, manual analysis for security bugs continues to be
utilized at all stages of software design [42]. Manual code           3.2    Participant recruitment
review is often essential to identify certain classes of bugs [43].
For example, in the study analysing Copilot’s outputs [8],            We recruit CS (or related discipline) students for our user
despite their use of GitHub CodeQL in identifying many                study. Prior work has noted that CS students can be reason-
CWE instances, other CWEs are checked manually.                       able proxies for developers in the context of software engi-
   In this study, we primarily use manual analysis jointly with       neering user studies. Tahaei et al. [44] found that “recruiting
static and run-time analysis as discussed in Section 4.3.             CS students from our University’s mailing list resulted in the
                                                                      highest data quality in terms of programming skills (highest),
                                                                      costs (lowest), number of duplicates (low), and passing at-
3     Design of the security-focused user study                       tention check questions (high) compared to the other tested
                                                                      crowdsourcing platforms.” Further, Ko et al. [45] note that
3.1    Overview                                                       university students can be appropriate participants when their
We seek to determine the impact of LLM assistance on the              knowledge and skills fit the one for the target audience. Fi-
security qualities of the code written by programmers, com-           nally, Salman et al. [46] found that students and professionals
paring against baseline code written by programmers without           do similarly on various code quality metrics. Intuitively, this
assistance. Here, completions suggested by an LLM may be              makes sense: university level coding students will likely soon
accepted by the users and inserted into their source code file.       join industry as professional software developers.
Suggestions may also be accepted and subsequently edited.                We selected participants with a range of experience from
   Similar to the previous two user studies using LLMs                three sources: (1) an undergraduate junior “operating sys-
[20, 21], we examined undergraduate and postgraduate stu-             tems” software class, (2) a senior- and MS-level “Application
dents from two software development courses at an R1 re-              Security” software class, and (3) an informal student “soft-
search university. We recruited participants by advertising on        ware chat group” which operates over Discord app. During
related social media. We tasked the participants with a pro-          recruitment, we outlined the goals of this study to measure the
gramming assignment. Since real-world programming tends               impact of the LLM on code writing, and informed participants
to be project-based (i.e. over a collection of related func-          of a US$50 compensation. For more details on the recruitment
tions) rather than a collection of disparate tasks, we modeled        process and ethical considerations, see the Appendix.
the assignment in this manner. This is similar to Imai’s [21]            In total, 105 participants signed up for this study, and were
‘minesweeeper’ assignment. We prompted participants to                randomly divided into the ‘assisted’ group (to be prompted
complete a “shopping list” program implementation in C.               with code generated by the AI code assistant), and the ‘con-
This was chosen as a majority of bugs are memory-based                trol’ group (to not). The participants used their own computer
issues in low-level languages such as C/C++ [9]. Participants         and resources, and were informed that they could use the In-
had to complete 12 functions related to this list (1 provided by      ternet to help in the general case, but they should not ask their
us and 11 to complete). By providing a well-defined API (the          peers or others for code writing assistance. As noted in [45],
list of functions), the program can be thought of as 12 sepa-         more structured studies in lab environments provide greater
rate programming tasks which may be analyzed separately.              control at the expense of realism, and the choice between
To minimize the risk of users running out of time, users were         the two is subjective. Both types have been used in software-
given two weeks to complete the assignment.                           engineering literature. Here, we opted for a more realistic
   To understand the effects of the LLM suggestions, we ran-          setup at the expense of structure; as [45] notes, “if a tool is
domly split the cohort into two groups. The ‘control’ group           entirely new, it may be more valuable to observe a tool being
were not given suggestions (the LLM was inactive). The ‘as-           used in more realistic conditions with fewer controls.” We
sisted’ group were given code suggestions by the LLM. All             expect the motivation levels between treatment and control
groups were given identical video instructions to sign in to          to be similarly distributed because participants are randomly
an online web portal where they complete the assignment               assigned to these groups. Not all participants ended up engag-
in a controlled development environment, with an additional           ing with the assignment: in total, 58 users completed code for
segment that either explains that they would get LLM sugges-          analysis. We present demographics of these in Section 4.1.
3.3    Programming assignment                                             * Core documents:
                                                                          README.md - contains study instructions
Summary: The students were tasked with completing a pro-                  Makefile - script for compiling code/running tests
gramming assignment that consisted of a shopping list imple-              list.h - documentation and list API
mented using a singly linked list data structure1 . The complete          list.c - file for participants to complete
assignment was provided all-at-once with all 11 functions si-             * Supplementary documents:
multaneously (task was to complete the C file to the specified            main.c - instantiates a basic list application
API). Participants could implement functions in any order and             runtests.c - the basic unit test suite
update previous answers. The students were provided with                  example_load_file.txt - for testing
documentation in the form of header files and a README,
as well as an instructional video. Other supporting documents                        Figure 2: Provided study documents / files
included a Makefile as well as 12 basic functional tests such       1   / / Node o f t h e s i n g l y l i n k e d l i s t
that the students could automatically test their code.              2   t y p e d e f s t r u c t _node {
                                                                    3           c h a r * item_name ;
   Open source: We open source the assignment in [12].              4           float price ;
   Justification for the C Language: This study focuses on          5           int quantity ;
                                                                    6           s t r u c t _node * n e x t ;
the security implications of using LLM code assistants by           7   } node ;
programmers. Given the frequency of memory-related bugs
                                                                                                   (a) Node definition (in list.h)
in C [9] such as null pointer references, and array and buffer
overflows, we chose the C programming language for the              1   # include     < s t d i o . h>
                                                                    2   # include     < s t d l i b . h>
study; these bugs are both consequential (frequently lead-          3   # include     < g e t o p t . h>
ing to exploitable code and severe errors) and relatively easy      4   # include     < s t r i n g . h>
                                                                    5   # include     " l i s t . h"
for developers to inadvertently express via vulnerable de-          6
sign patterns. Further, unlike modern languages such as Go          7   # d e f i n e MAX_ITEM_PRINT_LEN 100
                                                                    8
or Rust, the default compilation toolchains for C does not          9   / / Note : A l l l i s t _ f u n c t i o n s s h o u l d r e t u r n a s t a t u s c o d e
adequately check for these issues. Finally, all recruited par-     10   / / EXIT_FAILURE o r EXIT_SUCCESS t o i n d i c a t e s u c c e s s .
ticipants should have experience programming in C due to                            (b) #includes and implementation hints (in list.c)
syllabus requirements—i.e., this assignment should not be
their first exposure to C.                                                                       Figure 3: Preliminary codes
   Instructions: Video and text instructions walked the
students through signing in to the development environ-                    Basic functions: The ‘basic’ API functions are presented
ment, compiling, and their code. We gave the students a                 in Fig. 4. Here, ‘basic’ refers not to the difficulty of the under-
folder that contained the files listed in Fig. 2. These con-            lying code, but of the fundamental code required in any linked
tained documentation on what to do and how to do it                     list implementation – functions to add an item (at a position),
(README.md, Makefile, list.h), the file they were to com-               update an item, remove an item, and swap two items. We
plete (list.c), and supplementary testing files to mea-                 chose to complicate matters by (1) making all API functions
sure their progress and completion (main.c, test.sh,                    use a position index rather than importing and exporting node
unittests.exp, example_load_file.txt). These were                       pointers; (2) making the linked-list one-indexed, rather than
designed similar to an industry-standard setup for program-             the more standard zero-indexed; and (3) making all I/O to
ming - i.e., the users had to run make test to build and run            the API via function arguments and argument pointers with
tests and evaluate their code. Students were told they could            the API functions instead of returning success/failure status.
use any resource on the Internet, such as Google and Stack              These design choices increase the chance of unintended bugs,
Overflow. But they were not allowed to ask other students. We           as they increase the complexity of traversing the linked list.
asked the students to complete as much of the functionality                ‘Tricky’ functions - string manipulation, advanced
as they could during the two weeks of the study. They were              traversal, saving and loading: The list of complex, non-
not obligated to finish all functions to be compensated.                standard functions are presented in Fig. 5(b). These are sep-
   Introduction to the implementation: The basic shopping               arated into print functions (Fig. 5(a)), the advanced traver-
list definition is provided in Fig. 3(a). It is a singly-linked         sal functions (Fig. 5(b)), and saving and loading functions
list with each node containing a char* string pointer, a price          (Fig. 5(c)). These functions also require index positions
(float), and a quantity (int). No specific information is pro-          and argument pointers. Using pointers for return values
vided regarding other properties of these variables. The users          increases the number of pointer manipulations needed for
are then provided with the function APIs in the remainder               functionality, increasing the chance that code may be writ-
of list.h, as #includes and implementation hints at the                 ten with unintended security-relevant bugs. For example,
beginning of list.c (Fig. 3(b)).                                        list_item_to_string, which uses a documented “exter-
                                                                        nally allocated string”, needs to be written to avoid potential
  1 https://en.wikipedia.org/wiki/Singly_linked_list                    buffer overflows (what is the maximum length this string is
 1   / / c r e a t e a new l i s t
 2   i n t l i s t _ i n i t ( node ** h e a d ) ;
 3
 4   / / add a new i t e m ( name , p r i c e , q u a n t i t y ) t o t h e l i s t a t
               p o s i t i o n pos
 5   i n t l i s t _ a d d _ i t e m _ a t _ p o s ( node ** head , c h a r * item_name ,
             f l o a t p r i c e , i n t q u a n t i t y , unsign ed i n t pos ) ;
 6
 7   / / up da te t h e item a t p o s i t i o n pos
 8   i n t l i s t _ u p d a t e _ i t e m _ a t _ p o s ( node ** head , c h a r * item_name
             , f l o a t p r i c e , i n t q u a n t i t y , unsigned i n t pos ) ;
                                                                                                       Figure 6: Example suggestion by Codex Assistant. Suggested
 9                                                                                                     code is in grey italic. Prompt is all text before the cursor.
10   / / remove t h e i t e m a t p o s i t i o n * p o s *
11   i n t l i s t _ r e m o v e _ i t e m _ a t _ p o s ( node ** head , i n t p o s ) ;
12
13   / / swap t h e i t e m a t p o s i t i o n p o s 1 w i t h t h e i t e m a t                      3.4    The ‘Codex Assistant’ for code sugges-
             p o s i t i o n pos2
14   i n t l i s t _ s w a p _ i t e m _ p o s i t i o n s ( node ** head , i n t pos1 , i n t                tions
             pos2 ) ;
                                                                                                       In this section we will introduce the AI-based system which
     Figure 4: Basic linked list functionality (comments simplified)                                   generates code for the ‘assisted’ study group. This assistant
                                                                                                       was modelled after the commercial GitHub Copilot. It is built
                                                                                                       as an extension for Visual Studio Code which parses the file
 1   //   p r i n t a s i n g l e l i s t i t e m t o an e x t e r n a l l y a l l o c a t e d         under development, sends data to the OpenAI Codex API,
             string                                                                                    and provides a completion back to the user presented in faded
 2   / / T h i s s h o u l d be i n t h e f o r m a t o f :
 3   / / " q u a n t i t y * item_name @ $x . xx p r i c e e a "                                       grey text which they may accept or reject (see Fig. 6).
 4   i n t l i s t _ i t e m _ t o _ s t r i n g ( node * head , c h a r * s t r ) ;                      The general flow for using a coding assistant like ours or
 5
 6   / / p r i n t the l i s t to stdout                                                               Copilot is as follows. The user types any amount of code, such
 7   / / T h i s s h o u l d be i n t h e f o r m a t o f :                                            as comments, function names and arguments, or implementa-
 8   / / " p o s : q u a n t i t y * item_name @ $x . xx p r i c e e a " p l a c e s .
 9   i n t l i s t _ p r i n t ( node * h e a d ) ;                                                    tions. On the user pausing (750 ms of inactivity) the extension
                                                                                                       will select all code prior to their cursor and select text in re-
                (a) String manipulation functions (comments simplified)
                                                                                                       verse up to a finite amount—ours took up to 1,800 tokens (see
 1   / / find the item p o s i t i o n with the h i g h e s t s i n g l e p r i c e                    Section 2.2). It passes this text to the OpenAI Codex API for
 2   i n t l i s t _ f i n d _ h i g h e s t _ p r i c e _ i t e m _ p o s i t i o n ( node * head ,
             i n t * pos ) ;                                                                           the code-cushman-001 LLM. We chose this LLM as it is
 3                                                                                                     the fastest to operate and gave us response times similar to
 4   / / c a l c u l a t e t h e t o t a l c o s t o f t h e l i s t ( sum o f a l l
             prices * quantities )                                                                     GitHub Copilot. To prompt the LLM we used the following
 5   i n t l i s t _ c o s t _ s u m ( node * head , f l o a t * t o t a l ) ;                         parameters. The max_tokens: 64. This was chosen to keep
 6
 7   / / de − d u p l i c a t e t h e l i s t by c o m b i n i n g i t e m s w i t h t h e             the speed of generation high and the suggestions relatively
            same name                                                                                  short (we did not want the LLM to suggest code beyond the
 8   //        by a d d i n g t h e i r q u a n t i t i e s
 9   / / The o r d e r o f t h e r e t u r n e d l i s t i s u n d e f i n e d and may                 function currently being developed). The temperature: 0.6.
            be i n any o r d e r                                                                       We set the temperature to 0.6 based on the results reported in
10   i n t l i s t _ d e d u p l i c a t e ( node ** h e a d ) ;
                                                                                                       the original Codex work [3] as well as in [47], which show
                 (b) Advanced traversal functions (comments simplified)                                that the best pass@10 rate is at temperature=0.6. In addition,
 1   / / save the l i s t to f i l e filename                                                          this somewhat high temperature ensures the LLM does not
 2   / / t h e f i l e s h o u l d be i n t h e f o l l o w i n g f o r m a t :                        provide the same answers to all users. This is important as the
 3   / / item_name , p r i c e , q u a n t i t y \ n
 4   i n t l i s t _ s a v e ( node * head , c h a r * f i l e n a m e ) ;                             same starting list.c file is provided to all users, and as our
 5
                                                                                                       focus is on user acceptance of code suggestions rather than
 6   / / l o a d t h e l i s t from f i l e f i l e n a m e
 7   / / t h e f i l e s h o u l d be i n t h e f o l l o w i n g f o r m a t :                        the LLM, it is beneficial if some suggestions by the LLM are
 8   / / item_name , p r i c e , q u a n t i t y \ n                                                   unusual or creative. The top_p: 1.0. OpenAI documentation
 9   i n t l i s t _ l o a d ( node ** head , c h a r * f i l e n a m e ) ;
                                                                                                       suggests varying temperature or top_p, not both.
                  (c) Saving and Loading the list (comments simplified)                                   Input (and settings) thus provided, the assistant responds
                                                                                                       with a code suggestion presented in gray italics (e.g. Fig. 6).
             Figure 5: Advanced implementation requirements                                            The user can accept the suggestion by pressing space bar or
                                                                                                       reject by continuing to type.

     allowed to be? It is provided in the earlier #define from                                         3.5    ‘Autopilot’- automated task completion
     Fig. 3(b)). This is easy to miss. Other complex implementa-
     tions arise from list_deduplicate, which requires traver-                                         In addition to the two user groups, we created 30 solutions that
     sal and item removal code, and list_save and list_load                                            were generated entirely by the Codex LLM as an ‘autopilot’
     which need to deal with files and the list.                                                       group. We produced ten solutions from each of the three
    code LLMs offered by OpenAI: code-cushman-001 (max                               it straightforward to add data collection for active participants
    2048 tokens), code-davinci-001 (max 4096 tokens) and                             and prevent the IDE from being connected to other LLMs.
    code-davinci-002 (max 8000 tokens). The last LLM is                                  In addition to the ‘final form upload’, which collected the
    capable of filling in the middle given a prefix and suffix [48]).                self-reported ‘finished’ list.c files (as well as collected the
       We queried the LLM to generate code for one function                          study’s demographic information), we also took snapshots of
    at a time in the order they appear in the template list.c                        the complete list.c file environment every 60 seconds that
    file, requesting 512 tokens with a stop sequence of “\n}\n”.                     the file was open. This allowed us to track changes over time.
    The prompt included the function declaration and as much                         In addition, we recorded when suggestions from the Codex-
    of the previous file context as would fit in the LLM’s context                   based AI assistant were taken or when they were rejected.
    window (minus 512 tokens to allow room for the generated
    response), including any code previously generated by the
                                                                                     3.7    Statistical tests
    LLM. The temperature and top_p were set to the same
    values as in the AI assistant IDE plugin (0.6 and 1.0) for the                   We use standard statistical hypothesis tests to analyze results.
    reasons indicated in the previous section. After generating                      We check if LLM code assistants improve code quality with-
    a function, we check if the result compiled. If compilation                      out exacerbating security. Analogously, in medical settings,
    failed, we request another completion, up to a maximum of                        it is required to show that a treatment is effective (code qual-
    10 attempts per function. If no code compiled, we used the                       ity) while not exacerbating side effects (security). Standard
    template’s implementation of the function, which just returns                    comparative tests are used to establish efficacy— i.e., that the
    EXIT_FAILURE. This procedure models a user that relies on                        mean efficacy of the treatment is higher than the control. For
    the AI assistant, accepting suggestions unconditionally, with                    side effects, non-inferiority tests are used—the test seeks to es-
    minimal checks to see if the code compiles. Moving on to the                     tablish that the side effects are within a “maximum clinically
    next function once it seems to work and giving up if it fails                    acceptable difference“ that one is willing to tolerate [49].
    after several attempts. This is our baseline to compare control                      We describe the two tests below.
    and AI-Assistant groups. The initial file was identical to the                       Comparative hypothesis test: Given treatment and con-
    starting template with one exception: we added a comment                         trol groups with means µ1 and µ0 , respectively, and assuming
    near the top of the file that listed the members of the node                     (without loss of generality) that smaller means are better, a
    structure, which is defined in a header and is otherwise not                     comparative hypothesis test seeks to reject the null hypothesis
    visible to the LLM, as noted here:                                               H0 in favor of the alternate H1 .
1   / / Members o f t h e node s t r u c t :
2   / / c h a r * item_name , f l o a t p r i c e , i n t q u a n t i t y , node *
                                                                                        • Null hypothesis (H0 ): Treatment and control groups have
           next                                                                           the same mean, i.e., µ1 = µ0 .

       Without this addition, an unassisted LLM must guess the                          • Alternate (H1 ): Treatment group has a lower mean that
    member names, creating unusable solutions. This intervention                          control, i.e., µ1 < µ0 .
    is realistic since our goal is to mimick a hands-off human user.
    Two users in the ‘assisted’ group independently deployed this                    A comparative test establishes that the treatment is “better”
    strategy by copying the struct definition from the header                        than the control. We use this test to compare assisted (i.e.,
    file into list.c (commented out).                                                treatment) and control groups in terms of number of compiling
       We will present results for Autopilot group where appropri-                   functions and unit tests passed (in both cases, larger is better,
    ate, except for manual security analysis (Section 4.3), which                    so the hypothesis test is modified accordingly.).
    was too time-consuming to expand to full set of 30 Autopilot                        Non-inferiority hypothesis test: Under the same assump-
    solutions. Instead, we audited five Cushman LLMs.                                tions as above, the null and alternate hypotheses of a non-
                                                                                     inferiority test are:

    3.6      Experimental infrastructure                                                • Null hypothesis (H0 ): The treatment mean is more than
                                                                                                                                   δ
                                                                                          δ% larger than control, i.e., µ1 > (1 + 100 ) × µ0 ,
    This study provided a controlled, consistent environment via
    a containerized cloud-based IDE usable inside standard web                          • Alternate (H1 ): The mean of the treatment group is less
                                                                                                                                        δ
    browsers, based on the open-source Anubis software2 which                             than δ% larger than control, i.e., µ1 < (1 + 100 ) × µ0 ,
    is commonly used at New York University. This environment
    contained a virtual Visual Studio Code instance, which auto-                     where δ is the tolerance threshold. We use non-inferiority tests
    matically loaded the project upon a user signing in. Based on                    to compare bug incidence, measured as CWEs/LoC (Equa-
    their group membership, the system would automatically ei-                       tion 1, Section 4.3.2) and average CWEs/function (Equa-
    ther provide code suggestions or not. This custom IDE made                       tion 2), in the assisted and control groups.
                                                                                        There is no commonly accepted threshold for the amount
       2 https://github.com/AnubisLMS/Anubis                                         of decrease in code security that is considered acceptable for
      Table 1: Study participant enrolment demographics                                      Table 2: Study participant experience demographics
                             Control             Assisted         Total                                         Control Assisted               Total
                             Undergraduates (UG)                                      Is this the first linked list implementation you have ever made in C?
 UG Y2 (Sophomores)             2                   7                                      Yes (first list)       15          14                 29
     UG Y3 (Juniors)            8                   5
                                                                                       No (not first list)        11          12                 23
    UG Y4 (Seniors)             4                   4
    UG (Unspecified)            2                   1                               Declined to answer             3           3                  6
         UG (Total)            16                  17         N (UG) = 33                   Is this the first time that you have ever programmed in C?
                              Postgraduates (PG)                                         Yes (first time)          3           4                  7
             PG (MS)           10                  10                                No (not first time)          23          21                 44
           PG (PhDs)            1                   1                               Declined to answer             3           4                  7
      PG (Unspecified)          1                   0                               Are you taking, or have you ever taken a data structures or algo. class?
           PG (Total)          12                  11         N (PG) = 23
                                                                                      Currently taking             3           2                  5
                              Other Participants
                                                                                       Previously taken           21          24                 45
         Other (Total)          1                   1         N (Other) = 2
                 Total   N (Control) = 29 N (Assisted) = 29   N (Total) = 58                 Never taken           2           1                  3
                                                                                    Declined to answer             3           2                  5



a new programming tool. Different organizations may make                       were currently taking a data structures or algorithms class.
different choices depending on their threat model. For this
study we pick a threshold of 10% (i.e., we test the hypothesis
that AI assistance introduces no more than 10% more vulner-                    4.2                RQ1 - Functionality
abilities per line of code), but we make our data and analysis                 We assess functionality of the code using unit tests. Besides
available so that other thresholds can be tested if desired. The               the 11 Basic Tests (see Fig. 7) that we provided to the par-
10% threshold was chosen due to its common use in prior                        ticipants, we wrote 43 Expanded Tests to exercise edge
work (e.g. [50] in medical studies). As [50] notes, “This mar-                 cases (e.g., adding an element to the head of the list, pro-
gin has to incorporate a value judgment that...can only be                     viding the same position for both arguments to list_swap_
made subjectively and involves benefit/risk assessments...In                   item_positions), invalid parameters (e.g., NULL pointers,
the medical community, this margin has been reached via                        zero/negative indices), and validating that return value and
consensus.” We hope to see a similar effort in the software                    state of the list are correct after each API call.
security community to establish acceptable consensus values.                      Split Testing: We faced two challenges in automatically
With δ = 10%, rejecting the null confirms that the bug inci-                   testing the functionality of submitted code. First, many sub-
dence in the Codex assisted group is at worst 10% greater                      missions did not compile (19/58 = 32.8%). This includes
than the control group; we believe that this would show that                   9/30=30% in the Assistant group and 10/28=35.7% in the
Codex assistance does not exacerbate security “too much.”                      Control group). Second, the tests in the test suite may
                                                                               need to use other API functions in addition to the one un-
4     Study results and analysis                                               der test (e.g. a test for list_delete_item_at_pos might

4.1      User population (Demographics)                                                                    Compiled            Basic Tests
                                                                                                           Implemented         Expanded Tests
As noted (Section 3.2), 58 participants completed code for                                  100
analysis. As part of the study the participants completed a
                                                                                             80
brief demographic questionnaire. Table 1 shows the academic
                                                                               Percentage




enrolment information broken down by study group. There                                      60
was a good balance between undergraduates (UG), postgrad-
                                                                                             40
uates (PG), and others (e.g. recent graduates) across the two
study groups (‘control’ and ‘assisted’).                                                     20
   To examine pre-existing participant knowledge, we asked
                                                                                              0
the three questions presented in Table 2. The first question                                         Control           Assisted              Autopilot

checks if the assignment was similar to previous work com-
pleted by the participants, and about half of each of the ‘con-                Figure 7: Functionality for each group. Each group has to im-
trol’ and ‘assisted’ groups self-reported having written a                     plement 11 functions and 11 basic tests. We had 43 expanded
linked list in C before. The latter two questions aimed to vali-               tests. We show per group, the average % of functions Im-
date our goals with participant recruitment (i.e., they should                 plemented, regardless of whether they compiled or not, the
have some experience with C and knowledge of the linked                        average % of those functions that Compiled, the average %
list data structure). The majority of participants in both study               of each group that passes the 11 Basic Tests and the average
groups had both written C code before and had previously or                    % that passes the 43 Expanded Tests from each group.
need to create a nonempty list by using list_init and                causing a crash along a program path rendered vulnerabili-
list_add_item_at_pos). If there is a serious bug in one              ties later in the path unreachable, underestimating the true
of the core functions, it will cause all tests that depend on it     vulnerability count. For these reasons, we opted to manu-
to fail (even if the function under test itself is correct). It is   ally audit the 58 user-generated submissions, and five of the
difficult to measure functionality of the program as a whole.        code-cushman-001 LLM answers for comparison, a process
   Our testing procedure solves both of these problems by            further discussed here.
splitting the user’s code into individual functions (one per API,
including any required helper functions or data structures).
                                                                     4.3.1   Bug data encoding
For each function under test, we create a version of the sub-
mitted code where the other API functions are replaced by our        Working one function at a time, a panel of three of the co-
own known-good reference implementations. If an extracted            authors collectively read through blinded copies of submitted
function does not compile, we mark it as non-compiling and           source code, annotating security-relevant bugs as comments.
mark its associated tests as failing. As the template code “im-      This process was guided by compiler logs and the basic and ex-
plements” each function by returning EXIT_FAILURE, and               tended test suites; as well as thorough manual lexical analysis.
some tests expect failure, unmodified code may spuriously            As all annotation was performed collectively, no inter-rater
pass some tests. So, we also require code modification.              reliability checks needed to occur. This manual audit took
   Our tests thus automatically measure four distinct quan-          about 22 hours over the course of one week translating into
titative aspects of functionality for each submission: (i) %         66 person-hours overall—manual analysis, while thorough,
functions that were implemented, (ii) % functions that com-          does not scale well.
piled, (iii) % basic tests passing, and (iv) % expanded tests           From this, we created a table of 67 unique bug classes
passing. The four measures are shown for each group (‘con-           across all functions. Our focus was on memory related or
trol’, ‘assisted’, and ‘autopilot’) in Fig. 7.                       undefined bugs that cause CWEs such as the ones on Ta-
   Results: We see systematic differences between the ‘as-           ble 6. Full records with all annotations are provided open
sisted’ and the ‘control’ group. the ‘assisted’ group had a          source [12]. A summary, with severe bugs found per function
small but consistent advantage over the ‘control’ group. The         with incidence rates is in Table 7 (in the Appendix).
’autopilot’ group outperformed both ‘assisted’ and ’control’            Example bug finding process: One study participant
groups on functions implemented and compiled—this is by de-          provided the code exactly as it appears in Fig. 6 for
sign since our autopilot code generation procedure repeats sev-      list_item_to_string. This was a second-year UG stu-
eral times till code compiles. Interestingly, ‘autopilot’ slightly   dent who had written C code before and took an algorithms
under performs ‘assisted’ on basic tests, but slightly over per-     class. They were in the ‘assisted’ group.
forms on expanded tests. In other words, the AI code assistant          This code passes basic functional tests. However, it has
does help the users write better code in terms of functionality.     three CWEs. The first weakness is CWE-476: NULL Pointer
   Finally, the ‘assisted’ group wrote more code overall (280.9      Dereference. This can occur in the case where str is NULL
average lines of code compared to 247.5 LoC in the control           when this function is called (this is not checked for in the code,
group). We note, however, that due to the small sample size          and the API cannot guarantee the values it will be passed as
none of these comparisons reach statistical significance at the      arguments). This CWE is ranked at position #11 on Mitre’s
standard p < 0.05 level (as tested using Fisher’s exact test for     2022 ‘Top 25’ list [10]. The next weakness is CWE-758: Re-
the completion data, which is a binary variable, and Welch’s         liance on Undefined, Unspecified, or Implementation-Defined
t-test for the remaining comparisons).                               Behavior. This can occur when head->item_name is NULL,
   For interest, we include a graph indicating the time at which     and occurs because sprintf does not define what should
users in the different groups completed the study, with the as-      happen when NULL is passed to the ‘%s’ argument. This is
sisted group writing their submissions faster. This is depicted      a minor (some would say negligible) issue, as in the standard
in Fig. 12, in the Appendix.                                         libraries for gcc sprintf will print it as (null).
                                                                        The third and final weakness is the most serious. It is CWE-
4.3    RQ2 - Security analysis                                       787: Out-of-bounds Write, ranked as #1 on Mitre’s ‘Top 25’
                                                                     list. This occurs because the function sprints to an exter-
Although there are many different tools available for find-          nally allocated string. What is the length of this string? It
ing security-relevant flaws in C source code (as discussed in        is defined in a #define at the top of list.c (see Fig. 3(b),
Section 2.4), we found that none of them were appropriate            line 7). This is important because head->item_name is a
for our use case. Static analysis tools such as CodeQL [25]          user-controlled value, meaning they could store a very long
gave rates of false positives and negatives too high for our         string in here which would run off the end of the buffer. The
purposes. Meanwhile, fuzzing the participant code created            only safe way to implement this function is to use s_nprintf
records difficult to deduplicate (this is an open research prob-     with the n set to the value of this #define. This function is
lem [41]). Further, as fuzzing is dynamic, any vulnerability         scored as passing the basic tests, failing extended tests
(they pass in NULL as str for one case), and features three                                                                                 0.30
                                                                                   0.200
CWEs, two ranked as severe.
                                                                                   0.175                                                    0.25




                                                                    Bugs per LoC




                                                                                                                             Bugs per LoC
                                                                                   0.150
4.3.2   Metrics                                                                                                                             0.20
                                                                                   0.125

We analyze the quality of each user’s submission using the                         0.100
                                                                                                                                            0.15

bug per line-of-code (LoC) as our metric. Since we associate                       0.075                                                    0.10
each bug with a CWE, we will use CWEs/LoC as the metric.
                                                                                   0.050
Since most users submitted valid implementations for a subset                               Control   Assisted   Autopilot                                   Control     Assisted     Autopilot
of the 11 functions they were tasked with implementing, we
                                                                    (a) CWEs/LoC over compiling                              (b) CWEs/LoC over functions that
compute CWEs/LoC over those functions. We adopt two
                                                                    functions.                                               pass unit test.
notions of validity: (1) the function compiles or (2) it compiles
                                                                                   0.30
and passes unit tests.
                                                                                                                                                      0.25
   The CWEs/LoC are computed as follows. if Ei j is the num-                       0.25

ber of CWEs in function j of user i’s submission, Vi j ∈ {0, 1}




                                                                    Bugs per LoC




                                                                                                                                       Bugs per LoC
                                                                                                                                                      0.20
                                                                                   0.20
is a binary variable that is one only if user i submitted valid
code for function j, and Li j are the LoCs written by user i for                   0.15
                                                                                                                                                      0.15

function j, then the CWEs/LoC for user i are:
                                                                                   0.10                                                               0.10

                               ∑11
                                 j=1 Ei jVi j
                          Mi1 = 11            .              (1)                   0.05
                                                                                           Control    Assisted   Autopilot
                                                                                                                                                      0.05
                                                                                                                                                               Control     Assisted     Autopilot
                               ∑ j=1 Li jVi j
                                                                    (c) Severe CWEs/LoC over com-                                     (d) Severe CWEs/LoC over func-
We report CWEs/LoC in ’assisted’ and ’control’ groups by            piling functions. Non-inferiority                                 tions that pass unit test. Non-
                                                                    test is significant with p = 0.04.                                inferiority test gives p = 0.06.
averaging Mi1 over users in these groups. We compute Severe
CWEs/LoC metric focusing on the top-25 security CWEs
reported by Mitre [11]. The results are shown in Figure 8.          Figure 8: Comparing CWEs/LoC over compiling/passing
  Since our methodology allows us to test each function             functions for ‘all CWEs’ and ‘severe CWEs’ for each group.
independently, we can compare CWE incidence rates on a              Statistically significant p-values between ‘assisted’ and ‘con-
per function basis. For this, we compute the average CWEs           trol’ for non-inferiority test (δ = 10%) are noted.
for function j as:

                 ∑i∈Ng Ei jVi j
    M 2j (g) =                  ,   g ∈ {Assist, Control}    (2)    groups differ at the function level, i.e., whether Codex assisted
                  ∑i∈Ng Vi j                                        users introduce more bugs in certain functions compared to
                                                                    the control group or vice-versa. The per-function CWE rates
where NAssist and NControl are Codex assisted and control           (see Equation 2 to see how compute this), of severe CWEs
group users, respectively.                                          (those within Mitre’s ‘Top 25’) written by the three study
                                                                    groups are presented in Table 3. We present the results for
4.3.3   Topline results—CWEs/LoC                                    (a) all functions that compile, and (b) the compiling functions
                                                                    that then go on to pass the basic suite of tests. We present
Fig. 8(a)-Fig. 8(b) shows boxplots of the CWEs/LoC over
                                                                    the number of passing functions from each group, as well as
compiling functions and functions passing unit tests for the
                                                                    the number of CWEs found in those functions. The rate is
three groups, while Fig. 8(c)-Fig. 8(d) do the same for severe
                                                                    the division of these two numbers (see Equation 2). Security-
CWEs. For all four cases, we found that the ’assisted’ group
                                                                    related errors within functions that pass tests are naturally
has fewer bugs compared to ’control’, with up to a 22% lower
                                                                    more concerning than those in functionally-buggy code, as
mean for the ’assisted’ group compared with the ’control’ for
                                                                    code that appears to be functional has a higher chance of
severe CWEs over passing tests. For severe CWEs, the com-
                                                                    being deployed as-is.
parisons are also statistically significant using non-inferiority
tests with δ = 10%, i.e., we can conclude that severe bugs/LoC        As shown, the results for individual function vary across
for the ’Assisted’ group are no more than 10% greater than          groups. Where the ‘assisted’ group has a 10% higher rate
in the ’Control’ group.                                             of bugs compared to the ‘control’ is highlighted in blue.
                                                                    Over functions that pass unit tests, ‘assisted’ users have more
                                                                    bugs for functions that perform input/output operations on
4.3.4   Per function CWE rates
                                                                    the linked list. Conversely, functions for which the ‘control’
Our topline results suggest that CWE incidence in ‘assisted’        group has 10% higher rate of bugs compared to ‘assisted’ are
and ‘control’ groups are close. We now check whether these          highlighted in blue. These functions tend to involve pointer
manipulations and/or more complex logic. Where a differ-                             order severe, a possible second-order severity is presented
ence between the two groups is statistically significant, we                         alongside. For instance, with CWE-401, which is unranked,
annotate the fields with a †.                                                        the downstream effect is CWE-400, ranked at (#23).
   In terms of absolute CWE rates, for the ‘control’                                    CWE-787 (out-of-bounds write), the most severe CWE, is
and     ‘assisted’      groups, list_add_ item_at_pos,                               about equally prevalent in the ‘control’ and ‘assisted’ groups,
list_remove_item_at_pos,              and      list_update_                          but far less prevalent in the ‘autopilot’ group. This is likely
item_at_pos feature significantly higher incidence                                   due to the main root cause of CWE-787, which was, by far,
rates of severe CWEs (≈50 % greater than the ‘average’                               most frequently caused by the use of sprintf rather than
function rate), likely reflecting the increased difficulty when                      snprintf (e.g. in in list_item_to_string as previously
writing pointer and string manipulations (notoriously fiddly                         discussed in Section 4.3.1).
in C). For interest, we also include Table 7 (in the Appendix)                          CWE-416 (use after free), the second most severe CWE,
which presents the number of each type of CWE identified in                          is more prevalent in the ‘assisted’ group compared to the
the different functions by each study group.                                        ‘control’. This appears to be due to mistakes frequently made
                                                                                     by the ‘assisted’ group when manipulating the handling of
                                                                                     the char* item_name fields. Here, when creating a new
Table 3: Counting the # of Severe CWEs identified in each
                                                                                     shopping list node, the item_name is passed as an argument.
function/group. N = (N)umber of submitted functions which
                                                                                    There are many ways that this name could be stored. The
compile / which pass the tests. Rate is the average of the
                                                                                     unsafe and naïve way is to copy the char* pointer values.
Severe CWEs count per function in this group. Yellow cells
                                                                                    As the API is not provided any guarantees about the memory
indicate ‘control’ has 10 % higher rate of bugs than ‘assisted’,
                                                                                     location this is pointing to, it is not safe to assume that this
Blue is reverse. Cells with † indicate where this difference is
                                                                                    value will persist beyond the call of this function. Performing
statistically significant. The ‘Autopilot’ group in this Table
                                                                                     a pointer copy may thus lead to CWE-416 if the memory is
describes only the first 5 code-cushman-001 answers.
                                      Compiling                  Passing
                                                                                     later freed (there will now be a dangling pointer to the freed
    Function         Group
                                 N    # CWEs Rate         N    # CWEs       Rate     memory). The ‘safe’ way to manage the item_name variable
                    Control      20      61     3.05 †    12       38       3.17
 list_add_
                    Assisted     26      88     3.38 †    16       53       3.31
                                                                                     is to perform a copy of the string into a new variable. There
 item_at_pos
                    Autopilot    5       13       2.6      1       2         2.0     are two reasonable methods—the first (and easiest) would
                    Control      13      12      0.92     10       10        1.0
 list_cost_sum      Assisted     16      14      0.88     14       14        1.0
                                                                                     use strdup, and the second would use strlen followed by
                    Autopilot    5        9       1.8      4       8         2.0     a malloc(strlen+1) followed by a strcpy.
                    Control      12      20     1.67 †     4       7        1.75
 list_deduplicate   Assisted     15      14     0.93 †     3       5        1.67
                                                                                        Across all submissions, CWE-476 (NULL Pointer Deref-
                    Autopilot    5        4       0.8      1       2         2.0     erence) was the most commonly observed potential vul-
 list_find_         Control      14      14     1.00 †     8       11      1.38 †    nerability. This is because the API of the shopping list
 highest_price_     Assisted     19      12     0.63 †    11       09      0.82 †
 item_position      Autopilot    5       14       2.8      1       1         1.0     does not guarantee argument correctness: so every single
 list_item_
                    Control      21      47      2.24     13       29       2.23     pointer should always be checked against NULL. Special
                    Assisted     26      56      2.15     20       43       2.15
 to_string
                    Autopilot    5       10       2.0      4       6         1.5     cases are where a function takes a double-pointer, such as
                    Control      12      19      1.58      4       6       1.5 †     list_add_item_at_pos taking node** head. Here, both
 list_load          Assisted     17      27      1.59      4       8       2.0 †
                    Autopilot    5        0       0.0      0       0                 head and head* need to be checked against NULL. Such re-
                    Control      24      16      0.67      9       4       0.44 †    quirements were often missed by all participants, human and
 list_print         Assisted     27      22      0.81     13       10      0.77 †
                    Autopilot    5        2       0.4      1       1        1.0      LLM. These had downstream effects. For example, it causes
 list_remove_
                    Control      13      49      3.77     10       43      4.30 †    a large proportion of the CWE-758 instances (Reliance on
                    Assisted     19      74      3.89     14       51      3.92 †
 item_at_pos
                    Autopilot    5       16       3.2      3       9        3.00
                                                                                     Undefined Behavior), a CWE frequently observed when code
                    Control      14       4      0.29      7       1        0.14     uses standard library functions that may ingest NULL pointers
 list_save          Assisted     17       5      0.29      7       2        0.29
                    Autopilot    5        0       0.0      0       0
                                                                                    (e.g. printf, strcpy, strlen).
                    Control      12      26      2.17      5       11      2.20 †
 list_swap_
                    Assisted     20      43      2.15      6       7       1.17 †
 item_positions
                    Autopilot    5       15       3.0      0       0                4.3.6   Observations
                    Control      14      38     2.71 †    10       36      3.6
 list_update_
                    Assisted     24      88     3.67 †    16       60      3.75
 item_at_pos
                    Autopilot    5       16       3.2      3       13      4.33
                                                                                    The impact of code suggestions on cybersecurity (RQ2) is less
                    Control     139     290      2.09     84      180      2.14     conclusive than the impact on functionality (RQ1). Table 3
 Totals             Assisted    204     451      2.21    124      278      2.24
                    Autopilot    49      99      2.02     18       43      2.39
                                                                                    suggest that certain kinds of functions may be more or less
                                                                                    difficult to write safely depending on their complexity and the
4.3.5         CWE incidence rates                                                   experience of the developer—it appears that the LLMs may
                                                                                    sometimes reduce the incidence rates of bugs, and sometimes
Fig. 9 shows the prevalence of the ten most common CWEs                             increase them. Meanwhile, aggregating CWEs per participant
in user submissions. CWE descriptions in Table 6 in the Ap-                         LoC (Fig. 8) suggests that there may be a slight benefit to
pendix, along with their severity rank—if a CWE is not first-                       using LLMs, with Fig. 8(d) in particular highlighting that as
                                                                                                            Table 4: Attribution of bugs and LoCs for Codex-assisted
40.0%                                                                                                       users. Approx. is code manually modified from a suggestion.
                                                                                                                                       Human       Codex       Approx.
                                                                                                                               LoC      60%         16%          18%
30.0%                                                                                                                          Bugs     63%         16%          20%
                                                                                         Control
                                                                                         Assisted           Table 5: Origins of CWE-416 ‘use after free’ bug when
                                                                                         Autopilot
20.0%                                                                                                       item_name is improperly copied by users in ‘assisted’ group.
                                                                                                                                First location
                                                                                                                                                                 # Bug       # Bugs
                                                                                                                 Participant        of bug         # Bug
                                                                                                                                                               suggestions   in final
                                                                                                                   UUID          (document /     suggestions
                                                                                                                                                                accepted       file
10.0%                                                                                                                            suggestion)
                                                                                                                    0640          Suggestion         5              3           3
                                                                                                                    1f1c          Document           5              0           2
                                                                                                                    2125          Document           0              0           3
 0.0%                                                                                                               26a4          Suggestion         3              1           2
        C



                  C



                            C



                                      C



                                                C



                                                          C



                                                                    C



                                                                              C



                                                                                        C



                                                                                                  C
         W



                   W



                             W



                                       W



                                                 W



                                                           W



                                                                     W



                                                                               W



                                                                                         W



                                                                                                   W
                                                                                                                    3533          Suggestion         2              1           1
          E-



                    E-



                              E-



                                        E-



                                                  E-



                                                            E-



                                                                      E-



                                                                                E-



                                                                                          E-



                                                                                                    E-
            47



                      75



                                40



                                          25



                                                    41



                                                              78



                                                                        82



                                                                                  84



                                                                                            45



                                                                                                      83
                                                                                                                    36de          Suggestion         69             5           4
              6



                        8



                                  1



                                            2



                                                      6



                                                                7



                                                                          4



                                                                                    3



                                                                                              7



                                                                                                        5
                                                                                                                    3cff          Suggestion         2              2           2
                                                                                                                    514e          Document           1              1           1
Figure 9: Top 10 CWEs per group and their prevalence as %                                                           7193          Suggestion         13             1           2
of total CWEs. CWE descriptions are in Table 6.                                                                     74bd          Suggestion         4              2           2
                                                                                                                    925c          Suggestion         8              2           1
                                                                                                                    a3ed          Suggestion         10             2           2
code is made to pass tests it may be made more secure by                                                            a4b3          Suggestion         11             5           4
using the LLM. This is contrary to literature [7, 8] which                                                          a5ba          Document           0              0           1
                                                                                                                    a80d          Document           6              3           3
suggests that LLMs should be used with care due to their                                                            a974          Suggestion         12             5           3
habit of suggesting vulnerable patterns.                                                                            b59f          Suggestion         8              2           2
                                                                                                                    be6f          Suggestion         4              1           2
                                                                                                                    c23b          Suggestion         20            10           5
                                                                                                                    dac3          Document           10             2           2
4.4     RQ3 - On the origin of bugs                                                                                 dc47          Suggestion         1              0           2
                                                                                                                    ddac          Suggestion         13             1           1
To better understand how LLM assistance contributed to the                                                          ec83          Document           11             3           2
 code written by users in the Assisted group, we created a visu-                                                    fd62          Suggestion         12             1           1

 alization tool (Fig. 11 in the Appendix) that colors each user’s
 code based on the accepted suggestions logged during the ex-                                               bug were lexically similar between users and suggestions.We
 periment (ignoring code from our provided initial template).                                               choose this to analyze as it is a bug which is straightforward
The tool takes each suggestion in reverse chronological order                                               to test for using a custom automated script. How do users
(most recent first) and attempts to match it to a portion of                                                interact with buggy suggestions from the LLMs, and how
 the final document, initially using exact string matching and                                              bugs might ‘amplify’ via LLM suggestions if present in code.
 then attempting approximate matches up to a normalized edit                                                   To examine this, we first identify the CWE-416 incidences
 distance of 50%. With code originating from the LLM, the                                                   using the annotated final files from RQ2. We then pro-
 original suggestion will be shown on hover.                                                                gressively can scan the document and suggestion snapshots
    Using this tool, we examined each of the 564 security vul-                                              recorded during the user study, looking for the first recorded
 nerabilities identified in Section 4.3.5 and coded them as                                                 incident of that bug—for example, the first time that a new
‘originating from a Codex suggestion’ or as ‘introduced man-                                                node’s item name is incorrectly set directly to the function
 ually by a human user’ (Table 4). We found that humans                                                     argument item_name (i.e. without using a proper string copy
 introduced 356 of the bugs in our dataset (63%), while only                                                mechanism). We then count the number of times that the bug
 36% were introduced by the LLM and present in the user’s                                                   was present in suggestions by the LLM, as well as the number
 code verbatim (16%) or with modifications (20%).                                                           of suggestions containing the bug that were accepted by the
    Overall, 60% of the non-template code was written by a                                                  user. As user acceptance of suggestions is still not fully re-
 human. This accords with our findings in Section 4.3.5: the                                                flective of the final state of the code (as accepted code may be
 rate at which vulnerabilities are introduced by the LLM is                                                 further edited), we also scan the final ‘finished’ code files to
 similar to the rate at which they are introduced by humans.                                                count the number of these bugs present. Note that this bug can
This makes sense intuitively: LLMs attempt to predict the                                                   occur in multiple locations—both list_add_item_at_pos
 most likely continuation of their input, and so the quality of                                             and list_update_item_at_pos need to copy item names.
 the code they output tends to match the quality of their input.                                               We report results of this investigation in Table 5. Looking
    We can qualitatively examine the origin of a single bug. As                                             at this bug, in most cases it comes from the LLM suggestion
 an example, consider the potential use-after-free CWE-416                                                  originally, and even when it appears in the document first,
 discussed in Section 4.3.5. This is chosen as incidences of this                                           the LLM will go on to suggest the bug. Users that had the
 highest number of this bug had the highest number of buggy        on the generalizability of the results due to differences in be-
 suggestions provided and also accepted the highest number         havior and code performance, previous work [51] has found
 of suggestions. This table provides some insights into the        no difference between experienced software developers and
 usage of the LLM in general: users ‘1f1c‘, ‘2125’, ‘a5ba’, and    students regarding security-aware coding. In this work, we ob-
‘dc47’ self-author the bug without suggestions and do not go       served a defect density of 0.15 bugs/LoC which while greater
 on to accept buggy suggestions from the LLM (nor in many          than reported figures of 0.07 bugs/LoC [52], is reasonable
 cases even generate relevant suggestions).                        given the time constraints of the assignment.
                                                                      Code assignment difficulty: We designed both the assign-
                                                                   ment and chose the programming language with the intention
5     Discussion                                                   of examining how the developers might miss bugs in their
                                                                   designs. As such, the singly-linked shopping list has a number
5.1    Implications for LLM assistants                             of unusual traits and a non-optimal API. This increases the
Functionality (RQ1): our results corroborate recent stud-          difficulty of the assignment, which may itself have an impact
ies that have suggested that LLM assistants improve devel-         on the study results—if a developer is unable to ‘solve’ the
oper productivity [22, 23]. While we do not directly mea-          coding challenge at hand, they may get frustrated and hand in
sure productivity, the fact that ‘assisted’ users submitted        a substandard solution. Further, C is considered a more diffi-
more lines of code and completed a greater fraction of             cult programming language for inexperienced programmers
functions suggests enhanced productivity. One surprising           than other languages [53] such as Python or MATLAB. Other
result was the relatively high quality of code produced in         contexts (i.e. other languages, other programming tasks) may
‘autopilot’ mode (albeit for a relatively simple task).            yield different results than those found in this study.
   Security (RQ2): While prior work found that LLM code               Data capture: Due to limitations of the cloud-based IDE,
assistants may suggest security-critical bugs/CWEs [8], it did     it was not possible to capture all data from participants. For
not attempt to determine a comparison of the tool against          instance, rather than capturing every keypress from the users,
human developers nor did it examine how the (potentially vul-      we were restricted to taking ‘snapshots’ of their development
nerable) suggestions may impact developers using the tools.        over time (every 60 seconds). This limits the kind of fine-
Meanwhile, other studies which have included human devel-          grained analysis that might have been possible with more
opers [21–23] have not considered security. As such, to the        pervasive measurements.
authors knowledge, the user study presented in this work is
the first such study which measures how LLM suggestions
may impact the security of the code. We have found no con-
                                                                   6   Conclusions
clusive evidence to support the claim LLM assistants increase
                                                                   In this paper we set out to investigate the cybersecurity impact
CWE incidence in code in general, even when we looked
                                                                   of LLM code suggestions on participants writing code in a
only at severe CWEs. Our results indicate that the security
                                                                   user study. With N=58 users, we determined that the LLM has
impact in this setting is small: AI-assisted users produce crit-
                                                                   a likely beneficial impact on functional correctness; and does
ical security bugs at a rate no greater than 10% higher than
                                                                   not increase the incidence rates of severe security bugs in
the control, indicating that LLMs do not introduce new secu-
                                                                   our context (i.e., low level C code with pointer and array ma-
rity risks. This suggests that security concerns with LLM
                                                                   nipulations). This is somewhat surprising given the existing
assistants might not be as severe as initially suggested, al-
                                                                   published studies on how vulnerable code can be suggested
though studies with larger sample sizes and diverse user
                                                                   by the LLMs [7, 8]. When considering the origin of bugs that
groups are warranted.
                                                                   were found, the data suggests that the users do not use the
   Bug origins (RQ3): Our results indicate that users interact
                                                                   extra productivity benefits to fix bugs in their code—although
with the LLM in interesting ways. Users provide prompts
                                                                   suggestions are being modified (e.g. variable names), if a sug-
which may include bugs, accept buggy prompts which end
                                                                   gestion contained a bug it may not be fixed. This suggests
up in the ‘completed’ programs as well as accept bugs which
                                                                   that further research needs to be undertaken on highlighting
are later removed. In some cases, users also end up with more
                                                                   problematic lines of code (‘nutritional labels’) to encourage
bugs than were suggested by the LLM! In addition, the users
                                                                   users to check for security in real-time, as well as improving
that accepted the most bugs from the LLM also had the most
                                                                   code LLMs so that they can produce code that is more secure
bugs in their final files, further suggesting that the use of a
                                                                   than the user’s existing code.
buggy LLM may lead users toward buggy code.

5.2    Threats to validity                                         Acknowledgments
User selection: This study recruited university students rather    We gratefully acknowledge the participants from our user
than professional developers. While this may have an impact        study, as well as OpenAI who provided API access to their
code-cushman-001 LLM for the duration. This research                  (Accepted for Publication). [Online]. Available: https:
was supported in part by NSF Grant #2145482.                          //s2e-lab.github.io/preprints/scam22-preprint.pdf

                                                                  [8] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and
References                                                            R. Karri, “Asleep at the Keyboard? Assessing the Secu-
                                                                      rity of GitHub Copilot’s Code Contributions,” in 2022
 [1] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan,           IEEE Symposium on Security and Privacy (SP), May
     P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry,                2022, pp. 754–768, iSSN: 2375-1207.
     A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger,
     T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu,      [9] G. Thomas, “A proactive approach to more secure code
     C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin,              – Microsoft Security Response Center,” Jul. 2019. [On-
     S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish,           line]. Available: https://msrc-blog.microsoft.com/2019/
     A. Radford, I. Sutskever, and D. Amodei, “Language               07/16/a-proactive-approach-to-more-secure-code/
     Models are Few-Shot Learners,” arXiv:2005.14165
     [cs], Jul. 2020, arXiv: 2005.14165. [Online]. Available:   [10] MITRE, “2022 CWE Top 25 Most Dan-
     http://arxiv.org/abs/2005.14165                                 gerous Software Weaknesses,” 2022. [Online].
                                                                     Available: https://cwe.mitre.org/top25/archive/2022/
 [2] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei,                2022_cwe_top25.html
     and I. Sutskever, “Language Models are Unsupervised
     Multitask Learners,” p. 24, 2019. [Online]. Avail-        [11] ——, “CWE - Common Weakness Enumeration,” Jul.
     able: https://cdn.openai.com/better-language-models/           2022. [Online]. Available: https://cwe.mitre.org/
     language_models_are_unsupervised_multitask_learners.pdf
                                                               [12] G. Sandoval, H. Pearce, T. Nys, R. Karri, S. Garg,
 [3] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O.               and B. Dolan-Gavitt, “Lost at C: Data from the
     Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph,             Security-focused User Study,” Oct. 2022, type: dataset.
     G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov,           [Online]. Available: https://zenodo.org/record/7187359
     H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray,
     N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian,    [13] O. Lieber, O. Sharir, B. Lentz, and Y. Shoham, “Jurassic-
     C. Winter, P. Tillet, F. P. Such, D. Cummings,                 1: Technical Details and Evaluation,” AI21 Labs, Tech.
     M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss,          Rep., Aug. 2021. [Online]. Available: https://uploads-
     W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang,            ssl.webflow.com / 60fd4503684b466578c0d307 /
     I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse,      61138924626a6981ee09caf6_jurassic_tech_paper.pdf
     A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa,
     A. Radford, M. Knight, M. Brundage, M. Murati,            [14] AI21, “Jurassic-1 Language Models - AI21 Studio Docs,”
     K. Mayer, P. Welinder, B. McGrew, D. Amodei,                   2021. [Online]. Available: https://studio.ai21.com/docs/
     S. McCandlish, I. Sutskever, and W. Zaremba,                   jurassic1-language-models/#general-purpose-models
     “Evaluating Large Language Models Trained on Code,”
                                                               [15] E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang,
     arXiv:2107.03374 [cs], Jul. 2021, arXiv: 2107.03374.
                                                                    Y. Zhou, S. Savarese, and C. Xiong, “A Con-
     [Online]. Available: http://arxiv.org/abs/2107.03374
                                                                    versational Paradigm for Program Synthesis,” Mar.
 [4] AI21, “Discover Use Cases for AI21 Studio and                  2022, arXiv:2203.13474 [cs]. [Online]. Available:
     Jurassic-1.” [Online]. Available: https://www.ai21.com/        http://arxiv.org/abs/2203.13474
     blog/ai21-studio-use-cases
                                                                [16] Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng, M. Gong,
 [5] OpenAI, “Examples - OpenAI API.” [Online]. Available:           L. Shou, B. Qin, T. Liu, D. Jiang, and M. Zhou,
     https://beta.openai.com/examples/?category=code                 “CodeBERT: A Pre-Trained Model for Programming and
                                                                     Natural Languages,” Sep. 2020, arXiv:2002.08155 [cs].
 [6] R. Torres, “GitHub Copilot adds 400K subscribers                [Online]. Available: http://arxiv.org/abs/2002.08155
     in first month,” Aug. 2022. [Online]. Avail-
     able: https://www.ciodive.com/news/github-copilot-         [17] J. Finnie-Ansley, P. Denny, B. A. Becker, A. Luxton-
     microsoft-software-developer/628587/                            Reilly, and J. Prather, “The Robots Are Coming:
                                                                     Exploring the Implications of OpenAI Codex on
 [7] M. L. Siddiq, S. H. Majumder, M. R. Mim,                        Introductory Programming,” in Australasian Computing
     S. Jajodia, and J. C. S. Santos, “An Empirical                  Education Conference. Virtual Event Australia:
     Study of Code Smells in Transformer-based Code                  ACM, Feb. 2022, pp. 10–19. [Online]. Available:
     Generation Techniques,” Limassol, Cyprus, Oct. 2022,            https://dl.acm.org/doi/10.1145/3511861.3511863
[18] S. Sarsa, P. Denny, A. Hellas, and J. Leinonen,                 Large Language Models,” in 2023 IEEE Symposium on
     “Automatic Generation of Programming Exercises and              Security and Privacy (SP). Los Alamitos, CA, USA:
     Code Explanations Using Large Language Models,”                 IEEE Computer Society, May 2023, pp. 1–18. [Online].
     in Proceedings of the 2022 ACM Conference on                    Available: https://doi.ieeecomputersociety.org/10.1109/
     International Computing Education Research - Volume             SP46215.2023.00001
     1, ser. ICER ’22. New York, NY, USA: Association for
     Computing Machinery, Aug. 2022, pp. 27–43. [Online].       [28] N. A. Ernst and G. Bavota, “AI-Driven Development
     Available: https://doi.org/10.1145/3501385.3543957              Is Here: Should You Worry?” IEEE Software, vol. 39,
                                                                     no. 2, pp. 106–110, Mar. 2022, conference Name: IEEE
[19] A. M. Dakhel, V. Majdinasab, A. Nikanjam, F. Khomh,             Software.
     M. C. Desmarais, Z. Ming, and Jiang, “GitHub
                                                                [29] M. Ciniselli, L. Pascarella, and G. Bavota, “To What
     Copilot AI pair programmer: Asset or Liability?”
                                                                     Extent do Deep Learning-based Code Recommenders
     Jun. 2022, arXiv:2206.15331 [cs]. [Online]. Available:
                                                                     Generate Predictions by Cloning Code from the
     http://arxiv.org/abs/2206.15331
                                                                     Training Set?” Apr. 2022, arXiv:2204.06894 [cs].
[20] P. Vaithilingam, T. Zhang, and E. L. Glassman,                  [Online]. Available: http://arxiv.org/abs/2204.06894
     “Expectation vs. Experience: Evaluating the Usability of
                                                                [30] C. Topham, “Publication of the FSF-funded white pa-
     Code Generation Tools Powered by Large Language
                                                                     pers on questions around Copilot,” Feb. 2022. [Online].
     Models,” in CHI Conference on Human Factors in
                                                                     Available: https://www.fsf.org/news/publication-of-the-
     Computing Systems Extended Abstracts. New Orleans
                                                                     fsf-funded-white-papers-on-questions-around-copilot
     LA USA: ACM, Apr. 2022, pp. 1–7. [Online]. Available:
     https://dl.acm.org/doi/10.1145/3491101.3519665             [31] S. Biderman and E. Raff, “Neural Language Models are
                                                                     Effective Plagiarists,” Jan. 2022, arXiv:2201.07406 [cs].
[21] S. Imai, “Is GitHub Copilot a Substitute for Human
                                                                     [Online]. Available: http://arxiv.org/abs/2201.07406
     Pair-programming? An Empirical Study,” in 2022
     IEEE/ACM 44th International Conference on Soft-            [32] A. Aiken, “A System for Detecting Soft-
     ware Engineering: Companion Proceedings (ICSE-                  ware Similarity,” Apr. 2021. [Online]. Available:
     Companion), May 2022, pp. 319–321, iSSN: 2574-1926.             https://theory.stanford.edu/~aiken/moss/
[22] A. Ziegler, E. Kalliamvakou, X. A. Li, A. Rice,            [33] J. P. Wahle, T. Ruas, N. Meuschke, and B. Gipp,
     D. Rifkin, S. Simister, G. Sittampalam, and E. Af-              “Are Neural Language Models Good Plagiarists? A
     tandilian, “Productivity assessment of neural code              Benchmark for Neural Paraphrase Detection,” in 2021
     completion,” in Proceedings of the 6th ACM SIGPLAN              ACM/IEEE Joint Conference on Digital Libraries
     International Symposium on Machine Programming, ser.            (JCDL), Sep. 2021, pp. 226–229.
     MAPS 2022. New York, NY, USA: Association for
     Computing Machinery, Jun. 2022, pp. 21–29. [Online].       [34] M. Pistoia, S. Chandra, S. J. Fink, and E. Yahav, “A sur-
     Available: https://doi.org/10.1145/3520312.3534864              vey of static analysis methods for identifying security
                                                                     vulnerabilities in software systems,” IBM Systems Jour-
[23] M. Tabachnyk and S. Nikolov, “ML-Enhanced                       nal, vol. 46, no. 2, pp. 265–288, 2007, conference Name:
     Code Completion Improves Developer Pro-                         IBM Systems Journal.
     ductivity,”    Jul.   2022.   [Online].  Available:
                                                                [35] OWASP, “Source Code Analysis Tools.” [On-
     http://ai.googleblog.com/2022/07/ml-enhanced-code-
                                                                     line]. Available: https://owasp.org/www-community/
     completion-improves.html
                                                                     Source_Code_Analysis_Tools
[24] P. Gage, “A New Algorithm for Data Compression,” C
                                                                [36] K. Serebryany, D. Bruening, A. Potapenko, and
     Users Journal, vol. 12, no. 2, pp. 23–38, Feb. 1994,
                                                                     D. Vyukov, “AddressSanitizer: A Fast Address
     place: USA Publisher: R &amp; D Publications, Inc.
                                                                     Sanity Checker,” in 2012 USENIX Annual Techni-
[25] G. Inc., “CodeQL for research,” 2021. [Online].                 cal Conference (USENIX ATC 12). Boston, MA:
     Available: https://securitylab.github.com/tools/codeql/         USENIX Association, Jun. 2012, pp. 309–318. [Online].
                                                                     Available: https://www.usenix.org/conference/atc12/
[26] B. Developers, “Welcome to Bandit — Bandit                      technical-sessions/presentation/serebryany
     documentation,” 2022. [Online]. Available: https:
     //bandit.readthedocs.io/en/latest/                         [37] M. Polacek, “GCC Undefined Behavior Sani-
                                                                     tizer - ubsan,” Oct. 2014. [Online]. Available:
[27] H. Pearce, B. Tan, B. Ahmad, R. Karri, and B. Dolan-            https://developers.redhat.com/blog/2014/10/16/gcc-
     Gavitt, “Examining Zero-Shot Vulnerability Repair with          undefined-behavior-sanitizer-ubsan
[38] M. Zalewski, “American fuzzy lop,” Jul. 2020. [Online].   [47] J.-B. Döderlein, M. Acher, D. E. Khelladi, and
     Available: https://github.com/google/AFL                       B. Combemale, “Piloting Copilot and Codex: Hot
                                                                    Temperature, Cold Prompts, or Black Magic?” Oct.
[39] M. Aizatsky, K. Serebryany, O. Chang, A. Arya, and
                                                                    2022, arXiv:2210.14699 [cs]. [Online]. Available:
     M. Whittaker, “Announcing OSS-Fuzz: Continuous
                                                                    http://arxiv.org/abs/2210.14699
     fuzzing for open source software,” Dec. 2016. [Online].
     Available: https://opensource.googleblog.com/2016/12/     [48] M. Bavarian, H. Jun, N. Tezak, J. Schulman,
     announcing-oss-fuzz-continuous-fuzzing.html                    C. McLeavey, J. Tworek, and M. Chen, “Efficient
                                                                    Training of Language Models to Fill in the Middle,”
[40] P. E. Black, B. Guttman, and V. Okun, “Guidelines
                                                                    Jul. 2022, arXiv:2207.14255 [cs]. [Online]. Available:
     on Minimum Standards for Developer Verification of
                                                                    http://arxiv.org/abs/2207.14255
     Software,” National Institute of Standards and Technol-
     ogy, Tech. Rep., Oct. 2021. [Online]. Available: https:   [49] E. Walker and A. S. Nowacki, “Understanding
     //nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8397.pdf           Equivalence and Noninferiority Testing,” Journal
[41] V. J. Manès, H. Han, C. Han, S. K. Cha, M. Egele, E. J.        of General Internal Medicine, vol. 26, no. 2, pp.
     Schwartz, and M. Woo, “The Art, Science, and Engi-             192–196, Feb. 2011. [Online]. Available: https:
     neering of Fuzzing: A Survey,” IEEE Transactions on            //www.ncbi.nlm.nih.gov/pmc/articles/PMC3019319/
     Software Engineering, vol. 47, no. 11, pp. 2312–2331,     [50] H. M. J. Hung, S.-J. Wang, and R. O’Neill, “A
     Nov. 2021, conference Name: IEEE Transactions on               Regulatory Perspective on Choice of Margin and
     Software Engineering.                                          Statistical Inference Issue in Non-inferiority Trials,”
[42] K. Tuma, L. Sion, R. Scandariato, and K. Yskout,               Biometrical Journal, vol. 47, no. 1, pp. 28–36, 2005.
     “Automating the early detection of security design             [Online]. Available: https://onlinelibrary.wiley.com/
     flaws,” in Proceedings of the 23rd ACM/IEEE                    doi/abs/10.1002/bimj.200410084
     International Conference on Model Driven Engineering
                                                               [51] Y. Acar, C. Stransky, D. Wermke, M. L. Mazurek,
     Languages and Systems, ser. MODELS ’20. New
                                                                    and S. Fahl, “Security Developer Studies with GitHub
     York, NY, USA: Association for Computing Machinery,
                                                                    Users: Exploring a Convenience Sample,” 2017, pp.
     Oct. 2020, pp. 332–342. [Online]. Available: https:
                                                                    81–95. [Online]. Available: https://www.usenix.org/
     //doi.org/10.1145/3365438.3410954
                                                                    conference/soups2017/technical-sessions/presentation/
[43] M. di Biase, M. Bruntink, and A. Bacchelli, “A Security        acar
     Perspective on Code Review: The Case of Chromium,”
     in 2016 IEEE 16th International Working Conference        [52] A. Assaraf, “This is what your developers are doing
     on Source Code Analysis and Manipulation (SCAM),               75% of the time, and this is the cost you pay,” Feb. 2015.
     Oct. 2016, pp. 21–30, iSSN: 2470-6892.                         [Online]. Available: https://coralogix.com/blog/this-is-
                                                                    what-your-developers-are-doing-75-of-the-time-and-
[44] M. Tahaei and K. Vaniea, “Recruiting Participants              this-is-the-cost-you-pay/
     With Programming Skills: A Comparison of Four
     Crowdsourcing Platforms and a CS Student Mailing          [53] H. Fangohr, “A Comparison of C, MATLAB, and Python
     List,” in Proceedings of the 2022 CHI Conference               as Teaching Languages in Engineering,” in Computa-
     on Human Factors in Computing Systems, ser. CHI                tional Science - ICCS 2004, ser. Lecture Notes in Com-
     ’22. New York, NY, USA: Association for Computing              puter Science, M. Bubak, G. D. van Albada, P. M. A.
     Machinery, Apr. 2022, pp. 1–15. [Online]. Available:           Sloot, and J. Dongarra, Eds.       Berlin, Heidelberg:
     https://doi.org/10.1145/3491102.3501957                        Springer, 2004, pp. 1210–1217.

[45] A. J. Ko, T. D. LaToza, and M. M. Burnett,
     “A practical guide to controlled experiments of           Appendix
     software engineering tools with human participants,”
                                                               User study recruitment and ethical considerations:
     Empirical Software Engineering, vol. 20, no. 1,
                                                                  This study involved human participants and was approved
     pp. 110–141, Feb. 2015. [Online]. Available: https:
                                                               by New York University’s Institution Review Board (IRB) as
     //doi.org/10.1007/s10664-013-9279-3
                                                               #IRB-FY2022-6074. The key details are noted here.
[46] I. Salman, A. T. Misirli, and N. Juristo, “Are Students      Participants were recruited in phases from students and
     Representatives of Professionals in Software Engineer-    ex-students of the classes of two of the authors of this paper.
     ing Experiments?” in 2015 IEEE/ACM 37th IEEE In-          As there is a potential power dynamic between an instructor
     ternational Conference on Software Engineering, vol. 1,   and their students, a hard firewall was established between
     May 2015, pp. 666–676, iSSN: 1558-1225.                   student participants and their instructors. All knowledge of
enrolled participants was restricted to a single research inves-
tigator (and author of this paper), and this investigator was not
the instructor or supervisor of any of the study participants.
Students were informed of this firewall, and were informed
that their participation status would be kept strictly confi-
dential from their instructors, and that participating (or not
participating) would have no impact on their grades.
   During recruitment, participants were told both verbally
and via advertising material for the study that they would
be randomly divided into two groups, one with access to
an LLM code-assistant, and one without, and would then
be asked to complete a programming challenge. They were
also told that the code between each of the groups would be         Figure 11: Our visualization tool explores LLM suggestion
compared (Quote from the advertising material: “Will one            acceptance. Grey: Initial template; blue: human-written code;
group outperform the other?”, see Fig. 10). Verbal discussion       green: code accepted exactly from Codex suggestion; orange:
of the study included potential metrics, including time taken,      approximate matches. Pop-up: Codex suggestion (on hover).
functionality measurements, and security issues.
   As participants were informed that metrics including secu-
rity analysis would be a part of the study, this study did not      Table 6: Top 10 most common CWEs in each study group,
deceive any participants. It also did not deceive them with         along with downstream severe CWEs if a non-severe CWE
regards to the LLM itself, as AI responses from the Codex           would lead to a different severe CWE.
                                                                                                                                               ‘Top 25’
LLM were not modified (e.g. no bugs were artificially added              CWE ID                   Description
                                                                                                                                               Rank
to suggestions above the ones already present).                          CWE-476                  NULL Pointer Dereference                     11
                                                                         CWE-758                  Reliance on Undefined Behavior               -
                                                                         CWE-401                  Missing Release of Memory
                                                                         ,→ CWE-400               Uncontrolled Resource Consumption            23
 Large Language Models such as GitHub Copilot and Ope-                   CWE-252                  Unchecked Return Value                       -
 nAI Codex have recently been commercially released with                 CWE-416                  Use after Free                               7
 the goal of helping developers write software code. While               CWE-787                  Out-of-bounds Write                          1
 the marketing material touts the benefits of these “AI Pair             CWE-843                  Access using Incompatible Type
                                                                         ,→ CWE-119               Improper Restriction of Buffer Ops           19
 Programmers”, the actual impacts of these LLMs is yet                   CWE-457                  Use of Uninitialized Variable
 to be formally investigated. In this research, we aim to                ,→ CWE-119               Improper Restriction of Buffer Operations    19
 begin this exploration by challenging participants such as              CWE-835                  Infinite Loop                                -
 yourself with completing a range of programming ques-
 tions similar to those posed at the undergraduate level in
 computer science and software engineering courses. The                          1.0
                                                                                                      Duration by study group
 research question is simple: Half the participants will have                          Assisted
                                                                                       Control
 assistance via an LLM (OpenAI Codex) and the other half                         0.8
 will not. Will one group outperform the other?
                                                                    Proportion




                                                                                 0.6

Figure 10: Introductory paragraph to the recruitment material.
                                                                                 0.4


                                                                                 0.2
  CWE frequency within each study group:
  Table 6 lists the most common CWEs from each study                             0.0
                                                                                       0             5             10          15             20
group with their descriptions, downstream-CWEs if they are                                                      Duration (days)

severe, and the MITRE ‘Top 25’ rank.
                                                                    Figure 12: Study completion time between ‘Assisted’ and
   Table 7 presents the severe CWE counts per function by           ‘Control’ participant groups. Although the deadline was 14
study group, with bugs associated according to Table 6. The         days, a small minority of participants from both groups re-
N for each category refers to the (N)umber of compiling func-       quired additional time.
tions from participants. Rate refers to the count of this CWE
divided by the N. The ‘Autopilot’ group contains only to the
first 5 answers from code-cushman-001.
Table 7: Severe CWE counts per function by study group. ‘Autopilot’ group refers to the first 5 code-cushman-001 answers.
                                                                                                                                                    Compiling           Passing
                       Function Name               Group                                      Observed CWE
                                                                                                                                                     # this             # this
                                                                                                                                                 N          Rate   N            Rate
                                                                                                                                                     CWE                CWE
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   20 7       0.35   12   2       0.17
                                                              CWE-400: Uncontrolled Resource Consumption                                         20 9       0.45   12   6       0.5
                                                  Control
                                                              CWE-416: Use After Free                                                            20 19      0.95   12   14      1.17
                                                              CWE-476: NULL Pointer Dereference                                                  20 26      1.3    12   16      1.33
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   26 13      0.5    16   7       0.44
          list_add_item_at_pos                                CWE-400: Uncontrolled Resource Consumption                                         26 14      0.54   16   7       0.44
                                                  Assisted
                                                              CWE-416: Use After Free                                                            26 30      1.15   16   22      1.38
                                                              CWE-476: NULL Pointer Dereference                                                  26 31      1.19   16   17      1.06
                                                              CWE-400: Uncontrolled Resource Consumption                                         5   2      0.4    1    0       0.0
                                                  Autopilot   CWE-416: Use After Free                                                            5   4      0.8    1    0       0.0
                                                              CWE-476: NULL Pointer Dereference                                                  5   7      1.4    1    2       2.0
                                                  Control     CWE-476: NULL Pointer Dereference                                                  13 12      0.92   10   10      1.0
          list_cost_sum                           Assisted    CWE-476: NULL Pointer Dereference                                                  16 14      0.88   14   14      1.0
                                                  Autopilot   CWE-476: NULL Pointer Dereference                                                  5   9      1.8    4    8       2.0
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   12 1       0.08   4    0       0.0
                                                              CWE-400: Uncontrolled Resource Consumption                                         12 6       0.5    4    2       0.5
                                                  Control     CWE-416: Use After Free                                                            12 1       0.08   4    1       0.25
                                                              CWE-476: NULL Pointer Dereference                                                  12 11      0.92   4    4       1.0
                                                              CWE-787: Out-of-bounds Write                                                       12 1       0.08   4    0       0.0
          list_deduplicate                                    CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   16 1       0.06   3    0       0.0
                                                              CWE-400: Uncontrolled Resource Consumption                                         16 4       0.25   3    4       1.33
                                                  Assisted
                                                              CWE-416: Use After Free                                                            16 2       0.13   3    0       0.0
                                                              CWE-476: NULL Pointer Dereference                                                  16 7       0.44   3    1       0.33
                                                              CWE-400: Uncontrolled Resource Consumption                                         5   3      0.6    1    1       1.0
                                                  Autopilot
                                                              CWE-476: NULL Pointer Dereference                                                  5   1      0.2    1    1       1.0
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   14 1       0.07   8    0       0.0
                                                  Control
                                                              CWE-476: NULL Pointer Dereference                                                  14 13      0.93   8    11      1.38
          list_find_highest_price_item_position
                                                  Assisted    CWE-476: NULL Pointer Dereference                                                  19 12      0.63   11   9       0.82
                                                  Autopilot   CWE-476: NULL Pointer Dereference                                                  5   14     2.8    1    1       1.0
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   21 4       0.19   13   0       0.0
                                                  Control     CWE-476: NULL Pointer Dereference                                                  21 27      1.29   13   17      1.31
                                                              CWE-787: Out-of-bounds Write                                                       21 16      0.76   13   12      0.92
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   26 2       0.08   20   1       0.05
          list_item_to_string                                 CWE-416: Use After Free                                                            26 1       0.04   20   0       0.0
                                                  Assisted
                                                              CWE-476: NULL Pointer Dereference                                                  26 27      1.04   20   22      1.1
                                                              CWE-787: Out-of-bounds Write                                                       26 26      1.0    20   20      1.0
                                                              CWE-476: NULL Pointer Dereference                                                  5   7      1.4    4    4       1.0
                                                  Autopilot
                                                              CWE-787: Out-of-bounds Write                                                       5   3      0.6    4    3       0.75
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   12 3       0.25   4    0       0.0
                                                              CWE-400: Uncontrolled Resource Consumption                                         12 5       0.42   4    1       0.25
                                                  Control
                                                              CWE-476: NULL Pointer Dereference                                                  12 6       0.5    4    3       0.75
                                                              CWE-787: Out-of-bounds Write                                                       12 5       0.42   4    2       0.5
          list_load                                           CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   18 6       0.33   4    1       0.25
                                                              CWE-400: Uncontrolled Resource Consumption                                         18 8       0.44   4    3       0.75
                                                  Assisted    CWE-416: Use After Free                                                            18 1       0.06   4    0       0.0
                                                              CWE-476: NULL Pointer Dereference                                                  18 7       0.39   4    2       0.5
                                                              CWE-787: Out-of-bounds Write                                                       18 5       0.28   4    2       0.5
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   24 12      0.5    9    2       0.22
                                                  Control     CWE-400: Uncontrolled Resource Consumption                                         24 2       0.08   9    1       0.11
                                                              CWE-476: NULL Pointer Dereference                                                  24 2       0.08   9    1       0.11
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   27 17      0.63   13   8       0.62
                                                              CWE-400: Uncontrolled Resource Consumption                                         27 2       0.07   13   1       0.08
          list_print
                                                  Assisted    CWE-416: Use After Free                                                            27 1       0.04   13   1       0.08
                                                              CWE-476: NULL Pointer Dereference                                                  27 1       0.04   13   0       0.0
                                                              CWE-787: Out-of-bounds Write                                                       27 1       0.04   13   0       0.0
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   5   1      0.2    1    1       1.0
                                                  Autopilot
                                                              CWE-476: NULL Pointer Dereference                                                  5   1      0.2    1    0       0.0
                                                              CWE-400: Uncontrolled Resource Consumption                                         13 28      2.15   10   25      2.5
                                                  Control
                                                              CWE-476: NULL Pointer Dereference                                                  13 21      1.62   10   18      1.8
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   19 1       0.05   13   0       0.0
                                                              CWE-190: Integer Overflow or Wraparound                                            19 1       0.05   13   0       0.0
          list_remove_item_at_pos                 Assisted
                                                              CWE-400: Uncontrolled Resource Consumption                                         19 47      2.47   13   36      2.77
                                                              CWE-476: NULL Pointer Dereference                                                  19 25      1.32   13   15      1.15
                                                              CWE-400: Uncontrolled Resource Consumption                                         5   7      1.4    3    3       1.0
                                                  Autopilot
                                                              CWE-476: NULL Pointer Dereference                                                  5   9      1.8    3    6       2.0
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   14 1       0.07   7    0       0.0
                                                  Control     CWE-400: Uncontrolled Resource Consumption                                         14 2       0.14   7    0       0.0
          list_save                                           CWE-787: Out-of-bounds Write                                                       14 1       0.07   7    1       0.14
                                                              CWE-400: Uncontrolled Resource Consumption                                         17 3       0.18   7    1       0.14
                                                  Assisted
                                                              CWE-787: Out-of-bounds Write                                                       17 2       0.12   7    1       0.14
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   12 1       0.08   5    0       0.0
                                                  Control     CWE-400: Uncontrolled Resource Consumption                                         12 2       0.17   5    0       0.0
                                                              CWE-476: NULL Pointer Dereference                                                  12 23      1.92   5    11      2.2
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   20 3       0.15   6    0       0.0
          list_swap_item_positions                            CWE-190: Integer Overflow or Wraparound                                            20 2       0.1    6    0       0.0
                                                  Assisted
                                                              CWE-400: Uncontrolled Resource Consumption                                         20 9       0.45   6    0       0.0
                                                              CWE-476: NULL Pointer Dereference                                                  20 29      1.45   6    7       1.17
                                                              CWE-400: Uncontrolled Resource Consumption                                         5   4      0.8    0    0
                                                  Autopilot
                                                              CWE-476: NULL Pointer Dereference                                                  5   11     2.2    0    0
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   14 1       0.07   10   0       0.0
                                                              CWE-400: Uncontrolled Resource Consumption                                         14 10      0.71   10   10      1.0
                                                  Control
                                                              CWE-416: Use After Free                                                            14 10      0.71   10   10      1.0
                                                              CWE-476: NULL Pointer Dereference                                                  14 17      1.21   10   16      1.6
                                                              CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer   24 5       0.21   16   1       0.06
                                                              CWE-400: Uncontrolled Resource Consumption                                         24 26      1.08   16   22      1.38
          list_update_item_at_pos
                                                  Assisted    CWE-416: Use After Free                                                            24 22      0.92   16   19      1.19
                                                              CWE-476: NULL Pointer Dereference                                                  24 30      1.25   16   18      1.13
                                                              CWE-787: Out-of-bounds Write                                                       24 5       0.21   16   0       0.0
                                                              CWE-400: Uncontrolled Resource Consumption                                         5   6      1.2    3    5       1.67
                                                  Autopilot   CWE-416: Use After Free                                                            5   3      0.6    3    2       0.67
                                                              CWE-476: NULL Pointer Dereference                                                  5   7      1.4    3    6       2.0
