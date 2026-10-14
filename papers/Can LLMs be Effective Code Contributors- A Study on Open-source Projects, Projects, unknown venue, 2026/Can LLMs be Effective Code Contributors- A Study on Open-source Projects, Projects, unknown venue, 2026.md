                                             Can LLMs be Effective Code Contributors? A Study on Open-source
                                                                        Projects
                                                               Chun Jie Chong, Muyeed Ahmed, Zhihao (Zephyr) Yao, Iulian Neamtiu
                                                                               New Jersey Institute of Technology
                                                                                   {cc255, ma234, zhihao.yao, ineamtiu}@njit.edu


                                         Abstract                                                                 commits “in the wild” and LLMs could overfit to perform well
                                                                                                                  on benchmarks alone. These benchmarks also fail to capture
arXiv:2604.23340v1 [cs.SE] 25 Apr 2026




                                         LLM-generated code is widely used, and the share of commit-              the whole scope of real-world software evolution, e.g., code
                                         ted code produced by LLMs is expected to increase. However,              integration and testing (unit or whole-system).
                                         we are not at a point where LLMs can be effective contributors               We believe that an effective LLM must provide a fully
                                         to production code. We present an approach that exposes                  automated solution that, given a sizable code base and a prompt,
                                         the shortcomings of LLM generation on such projects, and                 generates a high-quality, usable commit (patch) that satisfies
                                         proposes recommendations; the targets of our study are sizable           the prompt specification and can be directly incorporated into
                                         open-source projects, e.g., FFmpeg and wolfSSL. First, we                the base. Towards that goal, several issues must be addressed:
                                         developed a framework that uses verification and validation              (1) how to assess whether LLMs are suitable at generating
                                         to evaluate a given LLM’s suitability to fix or add features             commit-ready code, and (2) when LLMs fail, how do they fail,
                                         to an existing project. Second, we apply the framework to                and what can we do about it.
                                         212 commits (bug fixes and small feature improvements) in
                                                                                                                      To tackle these issues and help make LLMs more effective at
                                         eight popular open-source projects and three LLMs: GPT-4o,
                                                                                                                  contributing to sizable code bases, we developed an automated
                                         Ministral3, and Qwen3-Coder. The success rate varied from
                                                                                                                  framework that evaluates LLMs’ ability to fix bugs and imple-
                                         0% to 60% depending on the project. The LLMs failed in a
                                                                                                                  ment new features via static analysis and test suites. Further
                                         variety of ways, from generating syntactically incorrect code,
                                                                                                                  comparisons between human-written and LLM-generated code
                                         to producing code that fails basic (static) verification, or val-
                                                                                                                  allow us to identify LLM-generated code issues that escape
                                         idation via the project’s test suite. In particular, the LLMs
                                                                                                                  the purview of automated verification&validation. Our auto-
                                         struggle with generating new code, handling contexts (function
                                                                                                                  mated framework uses programming tasks (commits) from
                                         or file) outside a certain size range, and in many cases their
                                                                                                                  open-source repositories, which are more representative than
                                         success is due to parroting code changes they have been trained
                                                                                                                  generic benchmarks. For our study, we focus on 212 actual
                                         on.
                                                                                                                  commits (187 bug fixes and 25 feature enhancements) in 8
                                                                                                                  open-source projects: Bison, Collections-C, FFmpeg, jansson,
                                         1     Introduction                                                       libhl, packcc, Vsftpd, and wolfSSL. We focus on C code as
                                                                                                                  it is widely spread in system programming and open-source
                                         Thanks to Large Language Models (LLMs) advancements,                     projects.
                                         AI-assisted programming is increasingly adopted in software                  Section 2 presents several motivational examples – four
                                         development [1]. AI code editors such as GitHub Copilot [2]              actual tasks from commits – along with the issues in the
                                         (powered by LLMs including OpenAI’s GPT [3]), Visual Stu-                LLM-generated code. Section 3 describes our approach: the
                                         dio IntelliCode [4], or Cursor [5], help programmers with code           framework, the projects and commits used for evaluation,
                                         suggestions, explanations and implementation. Accelerating               and the verification&validation processes. Section 4 presents
                                         software development is one of the reported benefits, e.g., a            our study results along several Research Questions (RQs)
                                         study found that 88% of developers reported an increase in               designed to check LLMs’ ability to generate effective code
                                         productivity when using Copilot [6].                                     contributions, i.e., Can LLMs generate code that compiles,
                                            However, LLM use comes with trade-offs. Studies have                  passes static analysis, and passes testing? When it fails, why
                                         shown that LLMs misuse APIs [7], create irrelevant and com-              and how does it fail? Which factors affect success rate?
                                         plicated conditional logic [7], lack defensive programming [8],              We applied our framework to three LLMs: GPT-4o,
                                         introduce security issues [8], and hallucinate [9]. Iterative            Ministral3-14B, and Qwen3-Coder-30B. We now summarize
                                         prompting might fix some of these issues, but the results from it-       some of our findings. Though the 212 commits were small,
                                         erative prompting are not consistent and not guaranteed [8, 10].         typically 4–15 LOC, the LLM-generated code fails to compile
                                         While benchmarks have been introduced to evaluate LLM-                   in 2–32 cases (depending on the LLM). Even when the code
                                         generated code [11–13] they might not be representative of               compiles, the verification stage found 9–18 null pointer deref-
                                             Accepted to EASE 2026.                                               erences, and 9–72 unsafe casts. Among those 98–143 commits


                                                                                                              1
                               Bug                                          to check whether an LLM can complete a straightforward task,
1   const size_t c = deque -> capacity - 1;                                 as the fix is suggested in the prompt and requires changing
2   const size_t l = deque ->last & c;                                      a single line of code. The second and third commits involve
3   const size_t f = deque -> first & c;
4   const size_t p = (deque -> first + index ) & c;                         fixing use-after-free and null pointer dereference errors, which
5   void * removed = deque -> buffer [index ];                              are among the 2024 CWE Top 25 Most Dangerous Software
6
                Should be replaced by p                                     Weaknesses list [14]. LLMs’ ability to solve these tasks is crit-
7   if (out)                                                                ical, as these vulnerabilities are common in software projects.
8       *out = removed ;
                                                                            The last commit is a feature enhancement that requires under-
                            Human fix                                       standing of the data structure used; this task examines LLM’s
1   const size_t c = deque -> capacity - 1;                                 understanding of the context. For these tasks, we use the
2   const size_t l = deque ->last & c;                                      commit message as part of the prompt to the LLM and attach
3   const size_t f = deque -> first & c;                                    the affected file as contextual reference. The prompt we used
4   const size_t p = (deque -> first + index ) & c;
5   void * removed = deque -> buffer [p];                                   for fixing a bug was “Modify the function in the provided C
6                                                                           file such that it fixes the following issue: <commit message>
7   if (out)                                                                in <function name>”; for implementing a new feature, we
8       *out = removed ;
                                                                            used “Implement a function in the provided C file: <function
                            GPT-4o fix                                      name> such that it <commit message>”.
1
      Removed 3 variables: c, l and f
2
3   size_t p = (deque ->head + index ) % deque ->
                                                                            2.1    Fixing an Incorrect Index Bug
        capacity ;
4
                                                                            This commit, from Collections-C [15], fixes a function that
                           Modified the calculation of p                    returns an element at the wrong index.1 Figure 1 shows the
5   if (out) {
6       *out = deque -> buffer [p];                                         bug, the human fix, and the GPT-4o-generated fix. The bug
7   }                                                                       is shown on line 6; the human fix correctly changed deque
                                                                            ->buffer[index] to deque->buffer[p]. The commit message
                                                                            is: “The deque_remove_at function was returning an incorrect
Figure 1: Human vs. GPT-4o fixes for an incorrect index bug.                element in certain situations. The correct element is the one
                                                                            at index p”. However, GPT-4o fails to fix the bug; on the
                                                                            right we highlight the three issues with the GPT-4o-generated
on which we could run a test suite, the LLMs had a passing                  code. First, the calculation of p is modified, which leads
rate of 71.8–86.7%. The main causes for validation failure                  to accessing the element at the wrong index again. Second,
included partial fixes, empty generated patches, fixing the                 GPT-4o removes certain variables that are irrelevant to the fix.
wrong thing, or deleting unrelated code. We found that context              Third, GPT-4o uses an undeclared variable, deque->head, which
size (subject file or target function) influences the success rate,         causes a compilation error, despite the fact that the entire file
e.g., a lower rate for larger contexts. In Section 5 we provide             (prior to the commit) was provided as context, including the
recommendations on how to increase effectiveness and safety                 declaration of the deque struct.
when using LLM generation.
   Open Science policy. Our artifact is available at                        2.2    Fixing a Use-after-free Error
https://github.com/LLM-Test-Framework/LLM-Tes
t-Framework.                                                                This commit, from jansson [16] involves fixing a potential
                                                                            use-after-free error when generating an error message.2 The
                                                                            code, shown in Figure 2, has a path on which a pointer key is
2     Motivational Examples                                                 used as an argument to set_error after it has been freed via
                                                                            jsonp_free(key). The fix involves moving the call to set_error
The fundamental question we ask is “Why can’t LLMs be                       before invoking the jsonp_free function on it, as shown in the
effective contributors on sizable projects”; once we know how               human code (center-left). The commit message used for the
they fail in our setting – a variety of tasks from a variety of files       prompt was: “Fix a use after free”. However, all three LLMs
in a variety of projects – we can generalize to larger contexts,            fail to identify this problematic issue. In the GPT-4o-generated
and proceed to address or mitigate some of the issues. We mo-               code, the variable key is still being used after it has been freed.
tivate our approach by showing the generated code if we asked               Furthermore, GPT-4o attempts to fix the use-after-free error
LLMs to produce the code required for typical maintenance                   by decrementing the reference count of value at line 3, which
and evolution needs. The four tasks are actual commits (bug                 reflects a misuse of the function, since value is not an allocated
fixes and feature enhancements) from our examined projects;                 object in this context and does not have a reference count.
the LLMs were given the affected file as context and the actual             Ministral3 replaces the line goto error with return null and a
commit message as prompt. Due to space constraints, we show                 call to decrement the reference count of object at line 3, which
the code output from all three LLMs for only two tasks, and                    1 https://github.com/srdja/Collections-C/commit/5ba7eed

one LLM for the other two tasks. The first commit allows us                    2 https://github.com/akheron/jansson/commit/11813f4




                                                                        2
                                                                 Bug
1   if(ours)
2       jsonp_free (key);
                               Using key after it has been freed
3   set_error (s, "<internal >", " Unable to add key \"%s\"", key);
4   goto error ;

                          Human fix                                                              GPT-4o fix
1   set_error (s, "<internal >", " Unable to add key                     1   if (ours)
         \"%s\"", key);                                                  2       jsonp_free (key);        Invalid, value does not have
2                                                                        3   json_decref ( value );       ref count
3   if(ours)              Call set_error before freeing key              4   set_error (s, "<internal >", " Unable to add key
4       jsonp_free (key);                                                        \"%s\"", key);
5   goto error ;                                                         5   goto error ;           Did not fix the use-after-free error
                        Ministral3 fix                                                        Qwen3-Coder fix
1   if (ours)                                                            1   if (ours)
2       jsonp_free (key);                                                2       jsonp_free (key);             No changes applied
3   json_decref ( object );                                              3
4   set_error (s, "<internal >", " Unable to add key                     4   set_error (s, "<internal >", " Unable to add key
         \"%s\"", key);                                                          \"%s\"", key);
5   return null;         Did not fix the use-after-free error            5   goto error ;



                                  Figure 2: LLM-generated code for fixing a use-after-free bug.


does not change the program as the error label performs the              difference is that the human implementation deviates from
same operations; this change does not fix the use-after-free             the function description by returning -1 instead of 0, whereas
error. Qwen3-Coder makes no changes, and hence does not                  all three LLMs follow the prompt and return 0. The second
fix the error.                                                           difference is that GPT-4o’s and Ministral3’s solutions use an
                                                                         undeclared function, hashtable_size, whereas Qwen3-Coder’s
2.3    Fixing a Null Pointer Dereference                                 solution uses an undeclared struct member. The function
                                                                         and struct are not implemented by the LLMs, but rather the
This commit, from Collections-C [15], fixes a potential null             LLMs assume that they exist in the codebase. These cause
dereference (which could lead to undefined behavior such as              compilation errors, as expected.
a segmentation fault).3 The buggy code, shown in Figure 3
(top), invokes strcmp (table->key_cmp uses strcmp under the
hood) on replace->key, which could be NULL. The human fix                3     Approach
consisted of adding a NULL check on replace->key to prevent
the null pointer dereference. The commit message used for                Figure 5 shows an overview of our approach: a general frame-
the prompt was: “Fixes a bug that would be triggered by add,             work, that evaluates a given LLM on a given repository, with a
get and remove hashtable operations when a key whose hash                given prompt, and an evaluation that applies this framework
value would resolve to table index 0 was used while NULL key             to existing commits from our examined projects.
was already present in the table”. Figure 3 demonstrates one                Framework. The framework is designed to verify and
of the three functions that GPT-4o was asked to fix. GPT-4o              validate LLM-generated code, which can be obtained either (1)
did not make any changes to the three functions, even though             by providing a custom prompt or (2) from a commit in a GitHub
it confidently stated that the generated code has fixed the issue.       repository. The framework takes a source file and a prompt
                                                                         as input which are passed to an LLM to generate a candidate
2.4 Implementing a Function for Size Retrieval                           solution. This solution is integrated in the original source code
                                                                         and then verified with the Clang static analyzer [17] (e.g., for
This commit, from jansson [16] implements a new function                 safety issues), followed by validation via the project’s test suite
that returns the hash table size in a struct called json_object_t        (if available).
.4 Figure 4 shows the function, which first checks whether                  Evaluation. We applied our framework to the actual commits
the parameter is an object, then casts it to json_object_t if the        from our examined projects. We automated prompt generation
check passes, and returns object->hashtable.size. The commit             by leveraging the actual commit message and the function name
message only mentions the name of the added function. There-             affected by the commit. Specifically, given a repository and a
fore, for prompt construction, we use the function description,          commit that describes a bug fix or new function implementation,
stated in the human commit: “Returns the number of elements              we extract the relevant function (e.g., foo(), bar()) from the
in *object*, or 0 if *object* is not a JSON object”. The first           commit diff and construct a prompt using one of two templates
    3 https://github.com/srdja/Collections-C/commit/2843fe2              shown in Section 2, depending on the nature of the change.
    4 https://github.com/akheron/jansson/commit/1e00cd5                  We also identify the changed file (e.g., file.c) and retrieve


                                                                     3
                                                                Bug
1   while ( replace ) {
2       if (table -> key_cmp (replace ->key , key) == 0) {
3            replace -> value = val;
4            return CC_OK ;
5       }                           Could be NULL
6   }

                          Human fix                                                             GPT-4o fix
1   while ( replace ) {                                                 1       while ( replace ) {
2       void *rk = replace ->key;                                       2
3                                                                       3
                                                                                                 No changes applied
4
                     NULL check added                                   4          if (table -> key_cmp (replace ->key , key) == 0)
5        if (rk && table -> key_cmp (rk , key) == 0) {                                  {
6            replace -> value = val;                                    5              replace -> value = val;
7            return CC_OK ;                                             6              return CC_OK ;
8        }                                                              7          }
9   }                                                                   8   }



                          Figure 3: GPT-4o-generated code for fixing a null pointer dereference error.


its previous version from the commit’s parent, which we then            LLM performance on realistic setups, and projects likely to
attach as input to the LLM. The generated function, either              come with tests [21]. We chose projects where context size
a replacement (foo’()) or a new implementation (bar()) is               range (max/min) was at least 7x, to cover a wide range of file
inserted into file.c. Essentially this yields a code base               context sizes. Finally, we only considered projects above a
where the only difference is the LLM-generated patch instead            certain popularity, measured by the number of stars (>300)
of the original human patch; we run verification and validation         and forks (>30), which indicates a diverse contributor list.
on this code base.                                                         We examined eight open-source projects that met these
   No loop. We deliberately eschewed iterative prompting, i.e.,         criteria: six hosted on GitHub, and two hosted elsewhere.
we did not re-prompt in case the LLM-generated code was                 Table 1 shows projects’ characteristics. The GitHub projects
unsatisfactory. We made this choice for two reasons. First,             were: (1) Collections-C [15] – a data structure library; (2)
LLMs should save developers time, not trade development                 packcc [22] – a parser generator; (3) libhl [23] – a thread-safe
time for iterative prompting time. Second, recent research has          data structure library; (4) jansson [16] – a library to process
shown that iterative prompting might degrade the quality of             JSON data; (5) FFmpeg [24] – a framework for processing
the output or even introduce bugs in bug-free code [8].                 audio and video; (6) wolfSSL [25] – a lightweight SSL/TLS
                                                                        library. We also included two open-source projects, the Bison
                                                                        parser generator [26] and the Vsftpd FTP server [27]; while
3.1     LLMs Used for Evaluation                                        not hosted on GitHub, their release histories are available,
For our study, we used three LLMs: one in the cloud and                 as changelog entries, similar to GitHub commit messages.
two local LLMs. First, we used OpenAI’s GPT-4o, due to its              Moreover, Bison and Vsftpd are the default FTP server and
API availability and widespread adoption. Second, we used               parser, respectively, in popular Linux distributions (Debian/Red
Ministral3 with 14 billion parameters and Qwen3-Coder with              Hat and derivatives), which confirms their popularity. All
30 billion parameters as local LLMs. As smaller LLMs are                projects were written mainly in C.
closing the gap with larger LLMs, we wanted to see how well
these smaller LLMs perform as compared to larger LLMs such
                                                                        3.3       Commit Selection Process
as GPT-4o. In addition, local LLMs are more suitable for
the development process, as they incur no token or API fees,            We selected 212 commits, all targeting the C code in the
work offline, and ensure data privacy. Using a different LLM            projects: for GitHub projects we used actual commits, while
involves simply changing the API endpoint.                              for Bison and Vsftpd, we selected the tasks from changelog
                                                                        entries (for uniformity, we refer to these entries as commits as
                                                                        well). The number of commits, and their kind, for each project,
3.2     Projects Used for Evaluation
                                                                        are shown in the last two columns of Table 1. The commits
To bolster external validity [18], i.e., choose representative          were selected based on the following criteria.
GitHub projects, we proceeded in line with previous re-                    Single file and single function change. This criterion keeps
search [19, 20]. Specifically, we selected projects based               the tasks simpler for LLMs. The rationale behind it is that
on four criteria: project size, context size, context size range,       LLMs are known to struggle on complex tasks, e.g., LLMs are
and popularity. We defined a minimum project size, 1500                 more likely to solve tasks that only take humans 11 minutes or
LOC, and a median file size of at least 400 LOC to evaluate             less [28].


                                                                    4
                                      Human                                                                             GPT-4o
1     unsigned int json_object_size ( const json_t *         1                                 unsigned int json_object_size ( const json_t *json )
          json)                                              2                                 {
2     {                               Implementation differs 3                                     if (! json_is_object (json))
3         json_object_t * object ;    from the specification 4                                         return 0;
4         if (! json_is_object (json))                       5
5               return -1;                                   6                                     json_object_t * object = json_to_object (json);
6
                                              Returns -1 instead of 0                  7
7           object = json_to_object (json);                                            8
                                                                                                                            hashtable_size() is undeclared
8           return object -> hashtable .size;                                          9           return hashtable_size (& object -> hashtable );
9     }                                                                               10       }

                                  Ministral3                                                                         Qwen3-Coder
1     unsigned int json_object_size ( const json_t *                                   1       unsigned int json_object_size ( const json_t *json )
          json)                                                                        2       {
2     {                                                                                3           if (! json_is_object (json))
3         if (! json_is_object (json))                                                 4               return 0;
4               return 0;                                                              5
                                                                                                                                  hashtable.entries is
5         json_object_t * object =     hashtable_size() is                             6           const json_object_t * object =
6               json_to_object (json); undeclared                                      7
                                                                                                                            undeclared
                                                                                                       json_to_object (json);
7                                                                                      8
8           return hashtable_size (& object -> hashtable )                             9
                ;                                                                     10           return object -> hashtable . entries ;
9     }                                                                               11       }



                                      Figure 4: LLM-generated code for implementing a size retrieval function.

                                              Table 1: Summary of project, commit, and context properties.

    Name                  Stars       Forks        Commit Timespan                Project Size                 Context (File) Size            #Commits
                                                        (MM/YY)                      (LOC)                          (LOC)                      Feature Bug
                                                    Start       End               Start         End         Min Median            Max    Enhancements Fixes
    Collections-C       2,900        330           09/14      05/25              2,006        6,746           81       493         942               3   17
    packcc                371         33           07/20      05/24              3,833        5,443        3,833     4,465       5,442               0    5
    libhl                 442        119           10/13      06/14              1,750        5,849          103       557         741               1   19
    jansson             3,200        833           09/09      02/15              1,882        4,142           32       667         779              11    9
    FFmpeg             51,200     12,800           01/12      06/25            473,858 1,340,782              65     1,066     10,319                2   73
    wolfSSL             2,500        876           12/23      12/24          1,345,510 1,495,448             253   23,923 125,527                    0   22
    Vsftpd                 n/a        n/a          08/09      08/21             15,302       16,415           37       656       2,554               4   22
    Bison                  n/a        n/a          08/18      09/21             19,681       25,480           98       430         824               4   20


           Framework                                                                           could be used. This prompting technique is recommended by
      Bug Fixing Prompt
                                                                      Pass                     GitHub [31] and has been shown to improve LLMs’ ability to
     New Function Prompt                              Verification:
                                         file.c          Static
                                                                                               perform complex tasks. However, due to the nature of feature
                                                                      Fail                     enhancement commits – requiring the implementation of a
                                       # Bug fix        Analyzer       Syntax Error
 Github             file.c        L    foo’(){…}        (Clang)        Unsafe Cast             new function – their size is slightly higher than for bug fixes.
Repository        foo(){…}        L                                    Memory Error
                                       # New Func                      …
                                  M                                                              Well-formed commit messages and changelog entries. A
                                       bar(){…}
                                                                      Pass                     well-formed commit message contains two main parts: (a)
           Evaluation                                  Validation:
     Bug Fixing Commit                                  Test Suite                             what has changed, and (b) the rationale for the change [32, 33].
                                                                      Fail
      New Function Commit
                                                                                               A study shows that typically 56% of open-source projects’
                                                                                               commits contain the “why” and “what” [34].
                 Figure 5: Overview of our approach.                                              Bug fix variety. The commits were selected to cover: (1)
                                                                                               functional, project-specific issues, and (2) a range of common
                                                                                               errors such as null pointer or indexing errors. We believe
                                                                                               LLMs should be capable of fixing both common C issues and
   Manageable commit size. The selected commits’ median
                                                                                               project-specific bugs.
sizes were 4 LOC for bug fixes and 15 LOC for feature
enhancement (Table 2). When a solution exceeds 12 LOC,                                           Feature enhancements. These involved implementing short,
60% of LLM-generated code tends to be irrelevant to the                                        simple, new functions (human equivalent: ≈15 LOC) that
actual fix [29]; in such cases chain-of-thought prompting [30]                                 might call existing functions from the provided context file.


                                                                                           5
        Table 2: LOC changes in the selected commits.                   Table 3: Categories of issues from static analysis. H: human;
                                                                        G: GPT-4o, M: Ministral3, Q: Qwen3-Coder (LLMs).
      Commit                Min    Max     Median     Mean
      Bug Fix                1      48       4        6.61                       Category                      #Issues in Code
      Feature Enhancement    6      66      15        19.96                                               H        G     M     Q
                                                                                 Null Dereference         23     18     16     9
                                                                                 Undeclared Identifier     0      31    50    20
   Project lifespan. We looked for projects with a long lifespan,                Unsafe Cast              34     64     72     9
to ensure the availability of sufficient commits with a long                     Double Free               0      1      0     2
development history, and capture a wide range of growth                          Use After Free            0      1      1     1
phases in the projects’ evolution. While project lifespan is                     Syntax/Semantic           0      40    45     1
omitted from Table 1 for space reasons, our examined projects’                   Uninitialized Variable    4      4     0      0
                                                                                 Empty/Partial             0      0      7    44
lifespans were at least 5 years (in some cases exceeding 10
                                                                                Total                     61     159   195    97
years).
   Commit dates span pre- and post-cutoff dates. We per-
formed a focused study (GPT-4o only) on the effect of LLM’s
knowledge cut-off date. The first period was before GPT-4o’s            4    Findings
cutoff date (May 2024). Since these pre-cutoff commits are
likely to be in the training data, we expect GPT-4o to do well          We now discuss the findings of our evaluation, structured
and cite sources. The second period comes after the training            around four research questions. Note that due to computational
cutoff date, which evaluates GPT-4o’s performance on unseen             limitations, we were unable to generate code for 14 out of 22
data. Ministral3 and Qwen3-Coder do not specify knowledge               commits from wolfSSL using Qwen3-Coder when the context
cutoff dates; the models themselves were released in December           file size exceeded 13,000 LOC. Since the context file was
2025 and July 2025, respectively.                                       included as part of the prompt for local LLMs, a large context
                                                                        file substantially increases the token count, which requires
                                                                        more memory to process the prompt. We used a MacBook Pro
3.4     Static Analysis                                                 with 36GB RAM for local LLM code generation.

For verification we use the Clang static analyzer [17], to keep
the process scalable for the project size and number of commits
                                                                        4.1 RQ1: Can LLMs Generate Syntactically
we cover. Clang offers a set of default checkers that checks
for issues, such as division by zero, dereference of NULL                   Correct Code?
pointers, and use of uninitialized variables. We also enable
                                                                        Failure to compile is one of the prominent issues observed
experimental checkers in Clang to check for a wider range of
                                                                        in LLM-generated code. This is due to the frequent use of
issues, such as out-of-bounds access in string functions and
                                                                        undeclared identifiers, such as functions, variables, and struct
invalid casting between pointers.
                                                                         members. Undeclared identifiers account for 31 (19.5%),
                                                                        50 (25.6%), and 20 (20.6%) issues for GPT-4o, Ministral3,
                                                                        and Qwen3-Coder respectively, as shown in Table 3. For
3.5     Test Suites
                                                                        instance, Figure 4 illustrates the LLMs’ assumptions that
For validation, we use the projects’ test suites. Test suites           hashtable_size and hashtable.entries exist in the codebase,
are run to achieve the following two objectives: (1) unit               despite their absences in the provided context files. Another
testing, ensuring the LLM-generated code fixes the bug and              noticeable category is syntax and semantic errors; we observed
implements the intended functionality; and (2) regression               40 (25.2%), 45 (23.1%), and 1 (1%) such cases across the
testing, making sure the LLM-generated code does not break              three LLMs. For example, the use of case statement outside
existing functionality.                                                 switch statement, missing curly braces, and treating a variable
                                                                        of type uint8_t as a struct, are grouped as syntax and semantic
                                                                        issues. These issues cause compilation errors, as expected
3.6     Manual Inspection                                               (the human-written code does not have such issues, because
                                                                        it would not be accepted as a commit). Though such issues
We also manually inspected the LLM-generated code to con-               are exposed at compile time, fixing them will require a time-
firm it implements the intended feature or fix. This was                consuming human intervention, which undermines the goal
necessary as we observed that LLM-generated code could                  of accelerating software development using LLMs. Note
pass all the tests even though the correct fix or feature was           that Qwen3-Coder has an ostensibly lower rate for syntax
not implemented, specifically in commits that did not add test          and semantic errors because it generated empty or partial
cases checking the fix or feature. The generated commits were           code for 44 commits, whereas Ministral3 has 7 such cases;
evaluated independently by two PhD students. We confirmed a             uncompilable code vacuously leads to fewer issues during
100% inter-rater agreement rate between the patch assessments.          static analysis.


                                                                    6
            Table 4: Verification (static analysis) results.                            to undefined behavior.
                                                                                           Uninitialized Variables. Variables that are declared but
 Projects                #Issues in Code               #Empty/Partial Code              not assigned to (prior to use) have undefined behavior, with
                    H        G     M     Q              G      M        Q
                                                                                        various manifestations across compilers or machines, e.g., as
 packcc              0       0         1     0         0          0         0           program crashes.
 jansson             0        1       17     5         0          0         0
 Collections-C       0        8        0     3         0          3         3
 libhl               3        4       22     5         0          0         7
 FFmpeg             56      128       99    20         0          0         26          4.3 RQ3: Validation: Why is Code Incorrect
 wolfSSL             0        5       20     0         0          2         7
 Bison               1       12       18    10         0          0         1
                                                                                            Even though It Passes Verification?
 Vsftpd              1        1       11    10         0          2         0
Total               61      159      188    53         0          7         44          In addition to the static analysis-based verification, we also
                                                                                        performed validation: we ran the projects’ test suites, and
                                                                                        followed that with a manual inspection.
Table 5: Test suites results on LLM-generated code. # Tests
means the total number of tests available.                                                 Test Suites. We first ran the test suites on the human-written
                                                                                        code for the selected commits; this code passed all test cases,
 Projects                Pass              Fail         Compile error      #Tests       as expected. Next, we replaced the human-written commit
                   G      M     Q     G     M     Q     G M       Q                     with the LLM-generated commit, and re-ran the test suite. We
 packcc             2      1     3    1     2      0     2    2        2     5          applied this procedure to all projects except Vsftpd, which
 jansson           15     12    15    4     4      4     1    4        1     20         lacks a test suite. For libhl, we were only able to run 19 test
 Collections-C     16     15    13    2     2      1     2    3        6     20
 libhl             13     10    10    6     7      2     0    2        7     19
                                                                                        suites out of 20 commits, as one of the libhl versions does not
 FFmpeg            56     34    27    0     6      3     0   16       26     56         contain a test suite. Note that we were also unable to run test
 wolfSSL           17      7     2    0     0      0     0   10       15     17         suites on LLM-generated code that caused compilation errors,
 Bison             5       5     7    6    12     11     9    3        2     20
                                                                                        such as those resulting from the use of undeclared identifiers
Total             124     84    77   19    33     21    14   40       59    157
                                                                                        (Section 4.1). Therefore, the total number of test suites does
                                                                                        not correspond to the total number of selected commits. In all,
                                                                                        for 7 projects, we have a total of 157 test suites available, and
4.2 RQ2: Why Does Code Fail Static Verifica-                                            we run 98, 117, and 143 test suites (across 98–143 commits)
    tion?                                                                               on Qwen3-Coder, Ministral3, and GPT-4o, respectively.
We performed static analysis on both human-written and LLM-                                Table 5 shows test suite run results. GPT-4o-generated code
generated code for the selected commits. Table 4 shows that                             has the highest number of passing test suites (124), followed
GPT-4o-generated code has a total of 159 issues (160% more                              by Ministral3 (84), and Qwen3-Coder (77). For failing test
than human-written code), whereas Ministral3-generated code                             suites, Ministral3 has the highest number (33), followed by
has a total of 188 issues (208% more). Qwen3-Coder has                                  Qwen3-Coder (21), and GPT-4o (19). The reasons for failing
a total of 53 issues (13.1% less than human-written code);                              test suites include not passing all the test cases and causing
however, 44 of its commits are either empty or contain only                             the test suite to deadlock and hang. We observed that a high
partial code. The numerous issues found in LLM-generated                                test suite passing rate does not guarantee code correctness.
code are presented in Table 3 and discussed next.                                       Fixes or new features often do not come with new associated
   NULL Pointer Dereferences. Null pointer dereferences                                 test cases in the commits. Therefore, LLMs’ failure in fixing
are severe issues that can cause denial of service, which is                            bugs or implementing new features may go unnoticed as the
especially a concern if the error happens in low-level systems                          relevant test cases are missing from the test suites. Note that
software. For instance, as shown in Figure 3, GPT-4o’s failure                          for Qwen3-Coder, there are 59 commits (37.6%) that cannot
to fix the issue could lead to a program crash (segmentation                            be compiled or used to run the test suites, while there are 40
fault).                                                                                 (25.5%) such commits for Ministral3 and 14 commits (8.9%)
   Unsafe Casts. This category has the highest proportion for                           for GPT-4o.
both GPT-4o (40.3%) and Ministral3 (36.9%), and accounts                                   Manual Inspection. We manually inspected all 212 com-
for 9.3% for Qwen3-Coder. Unsafe casts introduce a range of                             mits by comparing LLM-generated with human-written code
potential vulnerabilities: data loss, crashes and invalid reads or                      and tracing the LLM-generated code with inputs that trigger
writes to unintended memory regions. For instance, the LLM-                             the bugs (for bug-fixing commits) and inputs that served as
generated code *dst++ = replacements[i], which attempts to                              use cases (for feature enhancement commits). Table 6 shows
assign a char * (replacements[i]) to a char (dst) causes an                             the results. We group incorrect LLM-generated code into 5
unsafe, pointer-to-character cast.                                                      categories (category Uncompilable Code due to Undeclared
   Free-Related Vulnerabilities. We observed two classes                                Identifiers was discussed in Section 4.1).
of free-related vulnerabilities: double free and use-after-free.                           Partial Fix. In such cases, the fix requires addressing an
Double free occurs when an allocated region is freed twice,                             issue in, say, 𝑁 locations in the given function, but the LLM
while use-after-free involves accessing a variable after its                            addressed fewer than 𝑁. For instance, a commit from libhl [23]
memory has been deallocated. Both vulnerabilities can lead                              fixes a memory leak by releasing references of next and prev


                                                                                    7
Table 6: Manual inspection results for LLM-generated patches. ‘Success Rate’=fraction of patches judged correct by the
inspection.

                                                           packcc jansson              Collec.-C libhl              FFmpeg          wolfSSL             Bison            Vsftpd
                                                          G M Q G M Q                  G M Q G M Q                 G M Q            G M Q          G     M Q         G     M Q
 Correct




             Identical to Human Solution                  0    0    0   3   2     5    6    8    9   6    4    4   3     1      5   1     0    0   0     0      0    1     2     3
             Different from Human, Appears Correct        2    0    2   9   4     3    6    2    1   5    2    3   7     3      4   2     0    0   10    4      7    8     2     2
             Partial Fix                                  0    0    0   0    0     0   0    0    0   1    2    1   12     4  7      0     0    0   1      1      1   0  0        0
 Incorrect




             LLM Did Nothing (Empty Patch)                0    0    0   1    0     1   1    5    5   0    1    9    8    12 21      2     6    7   1      0      1   2  2        3
             Wrong Solution, Failed to Fix or Implement   2    5    3   5   10    10   4    5    1   7    8    3   25    48 35      16    2    1   6     15     12   11 12       11
             Deleted Code Unrelated to the Task           1    0    0   1    0     0   0    0    1   1    2    0    2     3  3      0     0    0   1      0      1   3  1        0
             Uncompilable Code (Undeclared Identifiers)   0    0    0   1    4     1   3    0    3   0    1    0   18     4  0      1     1    0   5      4      2   1  7        7

      Success Rate (GPT-4o)                                   40%           60%            60%           55%            13.3%            15%            41.8%            34.6%
      Success Rate (Ministral3)                               0%            30%            50%           30%            5.3%             0%             16.7%            15.4%
      Success Rate (Qwen3-Coder)                              40%           40%            50%           35%             12%              0%            29.2%            19.2%



 5 . The bug is shown on lines 2 and 8 in Figure 6 (top). The                               buggy code prior to the fix – in the generated code, which left
 human fix involves releasing references of next and prev on                                the bugs unfixed. This also confirms LLMs’ vulnerability to
 lines 2 and 8, respectively. The commit message is as follows:                             data poisoning (generation of harmful code due to malicious
“fixed a memory leak triggered by a fault path. the node was                                data injected purposely into training data). For Ministral3
 overretained”. However, GPT-4o only released the reference                                 and Qwen3-Coder, the generated code does not contain any
 on line 2, i.e., a partial fix.                                                            citations as they are local LLMs.
    LLM Did Nothing (Empty Patch). In such cases, the LLM                                      Different from Human, Appears Correct. Here the LLM
 did not make any changes to the given code, though it was                                  generates the correct code for the intended fix or feature,
 asked to, in the prompt. Figure 3 illustrates this troublesome                             though it differs from the human solution. For instance, when
 behavior: GPT-4o outputs code identical to the code prior to                               checking for integer overflow prior to calling jsonp_malloc(
 the commit, even though GPT-4o is confident in the response                                len + 1), GPT-4o’s code uses if (len + 1 == 0) whereas the
 that it fixed the bug.                                                                     human code uses the more robust version if (len == (size_t)
    Wrong Solution, Failed to Fix or Implement. In such cases,                              - 1).
 the LLM attempted to fix a bug or implement a new feature, but                                Success Rate. The last three rows of Table 6 show the
 the solution is incorrect; for example, GPT-4o and Ministral3                              overall success rates for each project and LLM. The lowest
 failed to address an issue in a single location within the function                        success rate, 0%, is observed for packcc using Ministral3,
 (Figure 2). This differs from a partial fix, where the LLM                                 and wolfSSL using Ministral3 and Qwen3-Coder. Overall,
 performed one or more fixes, but more changes are needed to                                FFmpeg and wolfSSL have relatively low success rates as these
 fully resolve the issue.                                                                   projects have large code bases and large contexts (Table 1)
    Deleted Code that was Unrelated to the Task. We also                                    where LLMs struggle to understand and produce a suitable, or
 observed that the LLM can delete code unrelated to the task,                               even compilable, patch, as discussed next.
 which in turn breaks existing functionality. For example, a
 commit from packcc [22] adds a feature to support escaped
 backslash.6 The commit message used is “Support escaped
                                                                                            4.4 RQ4: What Determines the Success and
 backslash for both string matching and character class match-                                  Failure of LLM Code Generation?
 ing”. However, GPT-4o deleted 3 switch cases – u, \n, and \r –                             We now discuss key factors contributing to LLM success or
 which were unrelated to the task, as shown in Figure 7. This                               failure.
 caused the test suites to fail, as expected.                                                  Context File Size and Function Size. As context file size
    We now discuss the two categories where the LLM-generated                               and function size increase, the success rate first goes up and
 code was correct (top rows of Table 6).                                                    then drops, as shown in Figures 8 and 9. We believe the initial
    Identical to Human Solution. For some commits, the LLM                                  increase happens because very small files and functions may
 generates an exact replica of human-written code. While                                    not give the LLM enough information to understand the task.
 such behavior can be harmless when the reproduced code is                                  With more context, the LLM gets traction – it can see more of
 correct, we observed that 5 out of 16 citations from GPT-4o                                the relevant behavior and dependencies. After a certain point,
 across 212 commits cite the wrong resources7 – using the                                   however, the file or function becomes too large for the LLM
             5 https://github.com/xant/libhl/commit/af96d58                                 to understand reliably. The LLM then has more code to track,
             6 https://github.com/arithy/packcc/commit/5211290                              the relevant changes become harder to isolate, and the success
    7 For the commit shown in Figure 3, the LLM cited 2 GitHub repositories                 rate drops.
 that use versions of Collections-C prior to the fix, alongside the generated
 code. These citations were provided as a file that contains code snippets with             to the LLM generating an empty patch, as the cited versions do not contain
 embedded URLs to their respective GitHub repositories. Anecdotally, this led               any fixes.


                                                                                       8
                                                                           Bug
1        if (! prev) {
2
3             destroy_entry ( entry );
4             return -1;
5        }                           Should release reference here
6        while (1) {
7            if ( ATOMIC_READ (prev ->next) != ATOMIC_READ (next ->node)) {
8
9                   prev = help_insert (prev , next);
10                  continue ;                                            Should release reference here
11            }

                                 Human fix                                                               GPT-4o fix
     1    if (! prev) {                                                           1   if (! prev) {
     2        release_ref (next ->refcnt , ATOMIC_READ (                          2       release_ref (next ->refcnt , ATOMIC_READ (
                   next ->node));                                                              next ->node));
     3        destroy_entry ( entry );                                            3       destroy_entry ( entry );
     4        return -1;                                                          4       return -1;
     5    }                    Reference released                                 5   }                    Reference released
     6    while (1) {                                                             6   while (1) {
     7        if ( ATOMIC_READ (prev ->next) !=                                   7       if ( ATOMIC_READ (prev ->next) !=
                   ATOMIC_READ (next ->node)) {                                                ATOMIC_READ (next ->node)) {
     8             release_ref (prev ->refcnt , ATOMIC_READ                       8
                        (prev ->node));                                           9             prev = help_insert (prev , next);
     9             prev = help_insert (prev , next);                                            continue ;
 10                continue ;
                                                                                 10                             Missing reference release
                                                                                 11        }
 11           }



                                                       Figure 6: GPT-4o fixed a bug partially.

                                 Human fix                                                               GPT-4o fix
     1     case ’r’: str[j++] = ’\x0d ’; break ;                             1    case   ’r’: str[j++] = ’\x0d ’; break ;
     2     case ’t’: str[j++] = ’\x09 ’; break ;                             2    case   ’t’: str[j++] = ’\x09 ’; break ;
     3     case ’v’: str[j++] = ’\x0b ’; break ;                             3    case   ’v’: str[j++] = ’\x0b ’; break ;
     4     case ’x’:                                                         4    case   ’x’: Impl. details omitted
     5     case ’u’:                                                         5
     6     case ’\n’:                                                        6
     7     case ’\r’:
                         Impl. details omitted                               7
                                                                                      Removed 3 switch cases: ’u’ , ’\n’ , and ’\r’
     8     default : str[j++] = ’\\ ’; str[j++] = str[i];                    8    default : str[j++] = ’\\ ’; str[j++] = str[i];



                                       Figure 7: GPT-4o deleted functional code unrelated to the task.


         Table 7: Statistical analysis: file size and function size.             for its success. Across all models, 𝑝-values for file sizes
                                                                                 range from 0.0003 to 0.0053, with failures often involving files
                         File Size (LoC)       Function Size (LoC)               several times larger than successes, e.g., Ministral3’s mean
     Model               Mean                    Mean                            failure at 4339.6 LoC vs. 690.1 LoC for success. For function
                     Success Failure 𝑝-value Success Failure 𝑝-value
                                                                                 size, 𝑝-values are significant (0.0001, 0.018) for GPT-4o as
     GPT-4o      1316.6       4972.4 0.0053     50.4     105.7   0.0001          wel as Ministral 3, and indicative for Qwen3-Coder (0.0575).
     Ministral3   690.9       4339.6 0.0003     56.5      94.2   0.0180
                                                                                 Therefore, the statistical results confirm that LLM’s success is
     Qwen3-Coder 551.3        8049.4 0.0005    101.8     151.2   0.0575
                                                                                 heavily dependent on code size.

                                                                                    Pre- and Post-Knowledge Cutoff Dates. We performed a
   We used Welch’s t-test [35] to validate these observed                        focused study on GPT-4o, which has a significantly larger
thresholds, by determining if the mean LoC differs significantly                 parameter size than Ministral3 and Qwen3-Coder. We found
between successful and failed generations. As shown in Table 7,                  that GPT-4o struggles to generate correct solutions for commits
the results confirm that both file size and function size influence              dated after GPT-4o’s knowledge cutoff date (May 2024). We
success. GPT-4o exhibited its strongest statistical separation at                performed a focused analysis of FFmpeg, which has sufficient
the function level (𝑝 = 0.0001): the mean successful function                    post-cutoff commit activity, and show the results in Table 8. For
was 50.4 LoC compared to 105.7 LoC for failed functions,                         commits that precede the knowledge cutoff date the success rate
showing that larger function sizes pose significant challenge                    was 13.6–17.4% depending on file size, whereas for commits


                                                                            9
                    60                                                ChatGPT            Table 8: FFmpeg: success rate before and after the cutoff date.
 Success Rate (%)
                                                                      Ministral3
                    40                                                Qwen3-Coder                                              Success Rate
                                                                                                                          LOC<Median LOC>Median
                    20                                                                                                        17.4%           13.6%




                                                                                                 Cutoff Date
                                                                                                 Knowledge
                                                                                                               Before
                                                                                                                           (4 out of 23)   (3 out of 22)
                     0
                                                                                                                              14.3%            6.3%
                             [27 ]

                             [48 9]

                             [60 2]

                            [74 4]

                           [10 66]

                           [23 335]

                                          ]

                                          ]
                                        6




                         [76 7695

                                       27
                                                                                                               After
                                    -27

                                      7

                                      0

                                      7
                                  7-4

                                  0-6

                                  3-7

                                     0




                                    55
                                                                                                                           (2 out of 14)   (1 out of 16)



                                 5-1

                                  -2
                                [32




                                  -
                               -12
                              67

                              36
                            96
                                             Context File Size                                     Table 9: Success rate in different commits.
                         Figure 8: Success rate across file sizes (LOC).
                                                                                                                        Feature Enhancement     Bug Fix
                                                                                                Correct                          13                56
                    60                                                ChatGPT                   Wrong                            12               131
                                                                      Ministral3
 Success Rate (%)




                                                                      Qwen3-Coder               Success Rate                    52%              29.9%
                    40

                    20                                                                      Stricter assessment on unfamiliar-task commits. The
                                                                                         LLM struggles to generate correct code for commits that occur
                    0                                                                    after the LLM’s knowledge cutoff date (Table 8). This suggests
                                                                                         that for unfamiliar or uncommon software engineering tasks,
                             ]

                                   ]

                                         ]

                                                 ]

                                                        ]

                                                                 1]

                                                                       [19 1]
                                                                                ]
                            14

                                  -25

                                        -43

                                              -55

                                                      -90




                                                                              16
                                                              -13

                                                                              9
                          [5-




                                                                    2-1

                                                                          2-8
                                 [15

                                       [26

                                             [44

                                                   [56




                                                                                         LLM-generated code should be subject to more rigorous human
                                                          [91

                                                                 [13




                                              Function Size                              review and testing.
                                                                                            Bug-fixing commits require stronger scrutiny. Bug-fixing
                    Figure 9: Success rate across function size (LOC).                   commits are more challenging for LLMs, as they require not
                                                                                         only locating and fixing the bug, but also understanding both
                                                                                         the context file and function. Due to their lower success rate
that come after the knowledge cutoff date, the success rate
                                                                                         (Table 9) we recommend stronger scrutiny of LLM-generated
dropped to 6.3–14.3%. This finding is concerning, because
                                                                                         bug-fixing commits.
LLMs will always operate de novo when writing a patch: they
could not have been trained on the very patch being written.                                LLM selection for appropriate tasks. We found that
                                                                                         the larger model, GPT-4o, generally performs better than
   Nature of the Commit. For our second focused study, the
                                                                                         smaller local LLMs, specifically in handling larger context
LLM, GPT-4o, achieves a lower success rate (29.9%) for bug-
                                                                                         (file/function size). Smaller context and function sizes are
fixing than feature-enhancements commits (Table 9). Although
                                                                                         often assumed to be beneficial to smaller local LLMs, but in
bug-fixing commits are smaller (median LOC=4), GPT-4o
                                                                                         practice they do not reliably lead to correct code generation.
achieves a higher success rate (52%) on feature-enhancement
                                                                                         The local LLMs perform well on routine and popular tasks,
commits (median LOC=15). We believe that locating and
                                                                                         such as implementing data structures and algorithms, as shown
fixing a bug is harder for an LLM than implementing a new
                                                                                         in Table 6; as projects become more specialized, such as in
function because fixing bugs requires understanding the func-
                                                                                         packcc and jansson, they under-perform. Therefore, we suggest
tion, in addition to the context file. This aligns with our finding
                                                                                         a larger model such as GPT-4o for patch generation, Qwen3-
that success rate decreases with larger functions.
                                                                                         Coder (30B parameters in our setting) for exploratory or
                                                                                         assistive coding, and Ministral3 (14B parameters) for resource-
                                                                                         constrained settings.
5                   Discussion
Based on our findings, we provide several recommendations
and discuss the limitations of our study.
                                                                                         5.2    Limitations
                                                                                         Generalizability. Our study is focused on a single language,
5.1                  Recommendations                                                     C. This work could be extended to other languages to check
                                                                                         for systematic, cross-language issues arising in LLM-based
Maintain a smaller context file size and function size. We                               code generation. Our study examines commits affecting a
observed that context file size and function size influence the                          single file and a single function. The study could be extended
LLMs’ ability to generate correct code for commits. Keeping                              to a broader setting, commits affecting multiple files and
the context file under 603 LOC (albeit not too small) and                                functions. However, given the already-low success rate in the
function under 56 LOC increases the likelihood of correct                                single file/function setting, we do not expect the success rate
code generation, as shown in Figures 8 and 9.                                            to improve when the setting is broader.


                                                                                    10
   Commit size. The selected commits are limited to 66 LOC                code-generation prompts does not imply robustness, as LLMs
(Table 2) and contain changes to only a single file and a single          frequently fail on closely related prompt instances that differ
function. We did not evaluate LLMs’ capability in commits                 only in prompt-level constants.
that involve changing multiple functions and files. However,                 Prompting with Better Context and Feedback Loop.
our findings reveal that, even in our simplified setting, LLMs’           LLM coding task benchmarks often fall short because they
ability to generate correct code deteriorates as the context (file        do not include the full or correct context (code base). Hu-
or function) size increases.                                              manEvo [53] includes surrounding code and dependencies
   Availability of commit messages as tasks (prompts). Our                to more accurately assess generated code’s quality. Zhang
study relied on the availability of commit messages as task               et al. [54] enhance LLMs’ ability to modify code snippets
goals, i.e., prompts. When developing de novo, for bug fixes              by providing richer context and breaking down the tasks. To
the prompts can come from bug summaries, after locating/re-               address the drawbacks of single-pass code generation, feedback
producing bugs; for feature improvements, the prompts can                 loops have been introduced [8, 55, 56] to perform a cycle of
come from feature requests.                                               testing and analysis on LLM generated code. Our framework
   Well-formed commit messages. Our study used well-                      also considers contextual references, but we do not perform a
formed commit messages (Section 3.3). Commits without                     feedback loop because we evaluate the LLM system as-is.
well-formed messages (e.g., attaching a link to an issue rather
than providing a detailed message, or lacking a rationale
behind the change) drive the LLM to generate incorrect code.              7    Conclusions
In such cases, the problem is the commit message, not the
                                                                          Given the rise of LLM-generated code, we study three LLMs’
LLM; interestingly, LLMs can help automate the generation
                                                                          viability for evolving real, open-source projects, by analyzing
of high-quality commit messages [36–38].
                                                                          actual commits and combining verification&validation with
                                                                          manual inspection. LLMs are usable for small files and
                                                                          functions, feature improvements, and tasks similar to prior
6    Related Work                                                         (seen) ones. In contrast, LLMs struggle with larger contexts,
                                                                          bug-fixing tasks, and new problems, often producing patches
LLM Coding Evaluation. While Chong et al. [8] studied the                 that fail silently. We outline recommendations to alleviate
security of LLM-generated code, we study LLMs’ capabilities               these issues. Our framework and findings can advance research
at fixing bugs and implementing new features. They analyzed               in both enhancing LLMs’ code generation capabilities, and
early changes in Bison and Vsftpd’s history; our examined                 verification&validation approaches for LLM-generated code.
changes are more recent, and do not overlap with the changes
and period they studied. ObfusEval [39] uses obfuscated code
to test LLMs’ capability on unseen tasks; it revealed that the            Acknowledgments
average pass rate of test suites for LLM-generated code can
decrease by 15.3% to 62.5%, in line with our findings that the            We thank the reviewers for their valuable feedback. This
LLM struggles to generate code for commits made after its                 material is based upon work supported by the National Science
knowledge cutoff date. Sagodi et al. [40] studied automated               Foundation under Grant No. CCF-2106710 and an internal
Java vulnerability repair using manually engineered prompts.              NJIT GHRI grant.
Other studies examined LLM-generated code’s correctness and
structural quality [41–44], robustness [45], and performance
regressions [7]. Wang et al. [29] categorized common types                References
of LLM code generation errors using a benchmark dataset.
                                                                           [1] Survey reveals AI’s impact on the developer experience. https:
Huang et al. [46] introduced ReinFix, an LLM-based program                     //github.blog/news-insights/research/survey-r
repair framework that guides patch generation using local and                  eveals-ais-impact-on-the-developer -experience,
external code bases. FIXCHECK [47] assesses patch correct-                     2024.
ness using LLM-assisted test generation, while METAL [48]                  [2] GitHub Copilot - Your AI pair programmer. https://github
evaluates consistency of LLM outputs via metamorphic testing.                  .com/features/copilot, 2024.
Orthogonal to these efforts, we evaluate LLMs’ capability in               [3] GitHub Copilot Enterprise on GPT-4o. https://github.b
actual, essential software engineering tasks, rather than generic              log/changelog/2024-07-05-github-copilot-enter
code generation.                                                               prise-on-gpt-4o, 2024.
   LLM Hallucinations and Non-Determinism. LLMs can                        [4] IntelliCode. https://visualstudio.microsoft.com/s
                                                                               ervices/intellicode/, 2025.
hallucinate, e.g., by generating syntactically correct but se-
                                                                           [5] Cursor: The ai code editor. https://cursor.com/, 2025.
mantically flawed code [9, 49]. MARIN [50] aims to prevent                     Accessed: 2025-10-15.
LLMs from using non-existent APIs and misusing existing                    [6] Research: quantifying GitHub Copilot’s impact on developer
ones. Our Section 4.1 confirms such hallucinations. Addition-                  productivity and happiness. https://github.blog/2022
ally, the non-deterministic nature of LLMs means that the same                 -09-07-research-quantifying-github-copilots-i
prompts can yield different results, causing reproducibility                   mpact-on-developer-productivity-and-happiness,
issues [51]. Turbulence [52] shows that success on isolated                    2022.


                                                                     11
 [7] S. Li, Y. Cheng, J. Chen, J. Xuan, S. He, and W. Shang.                     [27] vsftpd. https://security.appspot.com/vsftpd.html,
     Assessing the performance of ai-generated code: A case study                     2025.
     on github copilot. In 2024 IEEE 35th ISSRE, pages 216–227,                  [28] A. K. Zhang, N. Perry, R. Dulepet, E. Jones, J. W. Lin, J. Ji,
     2024.                                                                            C. Menders, G. Hussein, S. Liu, D. Jasper, et al. Cybench: A
 [8] C. J. Chong, Z. Yao, and I. Neamtiu. Artificial-intelligence                     framework for evaluating cybersecurity capabilities and risk of
     generated code considered harmful: A road map for secure and                     language models. arXiv preprint arXiv:2408.08926, 2024.
     high-quality code generation. arXiv preprint arXiv:2409.19182,              [29] Z. Wang, Z. Zhou, D. Song, Y. Huang, S. Chen, L. Ma, and
     2024.                                                                            T. Zhang. Towards understanding the characteristics of code
 [9] F. Liu, Y. Liu, L. Shi, H. Huang, R. Wang, Z. Yang, L. Zhang,                    generation errors made by large language models. In 2025
     Z Li, and Y. Ma. Exploring and evaluating hallucinations in                      IEEE/ACM 47th ICSE, pages 2587–2599. IEEE Computer
     llm-powered code generation. arXiv preprint arXiv:2404.00971,                    Society, 2025.
     2024.                                                                       [30] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia,
[10] S. Shukla, H. Joshi, and R. Syed. Security degradation in                        E. H. Chi, Q. V. Le, and D. Zhou. Chain-of-thought prompting
     iterative ai code generation – a systematic analysis of the paradox.             elicits reasoning in large language models. In Proceedings
     arXiv preprint arXiv:2506.11022, 2025.                                           of the 36th International Conference on Neural Information
[11] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto,                          Processing Systems, NIPS ’22. Curran Associates Inc., 2022.
     J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,                         ISBN 9781713871088.
     et al. Evaluating large language models trained on code. arXiv              [31] Prompt engineering for Copilot Chat. https://docs.githu
     preprint arXiv:2107.03374, 2021.                                                 b.com/en/copilot/concepts/prompt-engineering-f
[12] T. Liu, C. Xu, and J. McAuley. Repobench: Benchmarking                           or-copilot-chat, 2025.
     repository-level code auto-completion systems. arXiv preprint               [32] A. Mockus and L. G. Votta. Identifying reasons for software
     arXiv:2306.03091, 2023.                                                          changes using historic databases. In Proceedings 2000 Interna-
[13] H. Yu, B. Shen, D. Ran, J. Zhang, Q. Zhang, Y. Ma, G. Liang,                     tional Conference on Software Maintenance, pages 120–130,
     Y. Li, Q. Wang, and T. Xie. Codereval: A benchmark of                            2000.
     pragmatic code generation with generative pre-trained models.               [33] R.P.L. Buse and W. R. Weimer. Automatically documenting
     In Proceedings of the IEEE/ACM 46th ICSE. Association for                        program changes. In Proceedings of the 25th IEEE/ACM
     Computing Machinery, 2024. ISBN 9798400702174.                                   International Conference on Automated Software Engineering,
[14] 2024 CWE Top 25 Most Dangerous Software Weaknesses.                              page 33–42. Association for Computing Machinery, 2010. ISBN
     https://cwe.mitre.org/top25/archive/2024/2024_                                   9781450301169.
     cwe_top25.html, 2024.                                                       [34] Y. Tian, Y. Zhang, K. Stol, L. Jiang, and H. Liu. What makes a
[15] Collections-C. https://github.com/srdja/Collectio                                good commit message? In 2022 IEEE/ACM 44th ICSE, pages
     ns-C, 2025.                                                                      2389–2401, 2022.
                                                                                 [35] Bernard L Welch. The generalization of ‘student’s’problem
[16] jansson. https://github.com/akheron/jansson, 2025.
                                                                                      when several different population varlances are involved.
[17] Clang: a C Language Family Frontend for LLVM. http:
                                                                                      Biometrika, 34(1-2):28–35, 1947.
     //clang.llvm.org/.
                                                                                 [36] H. Wang, X. Xia, D. Lo, Q. He, X. Wang, and J. Grundy. Context-
[18] Steve Easterbrook, Janice Singer, Margaret-Anne Storey, and
                                                                                      aware retrieval-based deep commit message generation. ACM
     Daniela Damian. Selecting Empirical Methods for Software En-
                                                                                      Trans. Softw. Eng. Methodol., 30(4), 2021. ISSN 1049-331X.
     gineering Research, pages 285–311. Springer London, London,
                                                                                 [37] S. Liu, C. Gao, S. Chen, L. Y. Nie, and Y. Liu. Atom: Commit
     2008. ISBN 978-1-84800-044-5. doi: 10.1007/978-1-84800-0
                                                                                      message generation based on abstract syntax tree and hybrid
     44-5_11. URL https://doi.org/10.1007/978-1-84800
                                                                                      ranking. volume 48, pages 1800–1817, 2022.
     -044-5_11.
                                                                                 [38] Y. Wu, Y. Wang, Y. Li, W. Tao, S. Yu, H. Yang, W. Jiang, and
[19] Israel Herraiz, Daniel Rodriguez, Gregorio Robles, and Jesus M.
                                                                                      J. Li. An empirical study on commit message generation using
     Gonzalez-Barahona. The evolution of the laws of software
                                                                                      llms via in-context learning. In 2025 IEEE/ACM 47th ICSE,
     evolution: A discussion based on a systematic literature review.
                                                                                      pages 553–565. IEEE Computer Society, 2025.
     ACM Comput. Surv., 46(2), December 2013. ISSN 0360-0300.
                                                                                 [39] Y. Zhang, Y. Xie, S. Li, K. Liu, C. Wang, Z. Jia, X. Huang,
     doi: 10.1145/2543581.2543595. URL https://doi.org/10
                                                                                      J. Song, C. Luo, Z. Zheng, R. Xu, S. Liu, Y.and Zheng, and
     .1145/2543581.2543595.
                                                                                      X. Liao. Unseen horizons: Unveiling the real capability of llm
[20] Iulian Neamtiu, Guowu Xie, and Jianbo Chen. Towards a better                     code generation beyond the familiar. In 2025 IEEE/ACM 47th
     understanding of software evolution: an empirical study on                       ICSE, page 604–615. IEEE Computer Society, 2025.
     open-source software. J. Softw. Evol. Process, 25(3):193–218,               [40] Zoltán Ságodi, Gábor Antal, Bence Bogenfürst, Martin Isztin,
     March 2013. ISSN 2047-7473. doi: 10.1002/smr.564. URL                            Péter Hegedűs, and Rudolf Ferenc. Reality check: Assessing gpt-
     https://doi.org/10.1002/smr.564.                                                 4 in fixing real-world software vulnerabilities. In Proceedings of
[21] P. S. Kochhar, T. F. Bissyandé, D. Lo, and L. Jiang. An empirical                the 28th International Conference on Evaluation and Assessment
     study of adoption of software testing in open source projects. In                in Software Engineering, pages 252–261, 2024.
     Proc. 13th International Conference on Quality Software, pages              [41] J. Liu, C. S. Xia, Y. Wang, and L. Zhang. Is your code
     103–112. IEEE, 2013.                                                             generated by ChatGPT really correct? rigorous evaluation of
[22] packcc. https://github.com/arithy/packcc, 2025.                                  large language models for code generation. In Proc. NIPS, 2023.
[23] libhl. https://github.com/xant/libhl, 2025.                                 [42] Antonio Della Porta, Stefano Lambiase, and Fabio Palomba. Do
[24] FFmpeg. https://github.com/FFmpeg/FFmpeg, 2025.                                  prompt patterns affect code quality? a first empirical assessment
[25] wolfSSL. https://github.com/wolfSSL/wolfssl, 2025.                               of chatgpt-generated code. arXiv preprint arXiv:2504.13656,
[26] Bison. https://www.gnu.org/software/bison/, 2025.                                2025.


                                                                            12
[43] Victor Alves, Carla Bezerra, Ivan Machado, Larissa Rocha,                multi-agent llm applications through continuous human-llm co-
     Tássio Virgínio, and Publio Silva. Quality assessment of                 programming. In 2025 IEEE/ACM 4th International Conference
     python tests generated by large language models. arXiv preprint          on AI Engineering – Software Engineering for AI (CAIN), pages
     arXiv:2506.14297, 2025.                                                  42–47. IEEE Computer Society, 2025.
[44] Tristan Coignion, Clément Quinton, and Romain Rouvoy. A
     performance study of llm-generated code on leetcode. In
     Proceedings of the 28th international conference on evaluation
     and assessment in software engineering, pages 79–89, 2024.
[45] L. Zhong and Z. Wang. Can llm replace stack overflow? a
     study on robustness and reliability of large language model code
     generation. In Proceedings of the AAAI conference on artificial
     intelligence, volume 38, pages 21841–21849, 2024.
[46] Jiayi Zhang, Kai Huang, Jian Zhang, Yang Liu, and Chunyang
     Chen. Repair ingredients are all you need: Improving large
     language model-based program repair via repair ingredients
     search. arXiv preprint arXiv:2506.23100, 2025.
[47] Facundo Molina, Juan Manuel Copia, and Alessandra Gorla.
     Improving patch correctness analysis via random testing and
     large language models. In 2024 IEEE Conference on Software
     Testing, Verification and Validation (ICST), pages 317–328.
     IEEE, 2024.
[48] Sangwon Hyun, Mingyu Guo, and M Ali Babar. Metal: meta-
     morphic testing framework for analyzing large-language model
     qualities. In 2024 IEEE Conference on Software Testing, Verifi-
     cation and Validation (ICST), pages 117–128. IEEE, 2024.
[49] Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma, W. Zhong, J. Chen,
     M. Mao, and Z. Zheng. Llm hallucinations in practical code
     generation: Phenomena, mechanism, and mitigation. Proceed-
     ings of the ACM on Software Engineering, 2(ISSTA):481–503,
     2025.
[50] Y. Chen, M. Chen, C. Gao, Z. Jiang, Z. Li, and Y. Ma. Towards
     mitigating api hallucination in code generated by llms with hier-
     archical dependency aware. In Proceedings of the 33rd ACM
     International Conference on the Foundations of Software Engi-
     neering, page 468–479. Association for Computing Machinery,
     2025.
[51] S Ouyang, J. M. Zhang, M. Harman, and M. Wang. An empirical
     study of the non-determinism of chatgpt in code generation.
     ACM Trans. Softw. Eng. Methodol., 34(2), 2025. ISSN 1049-
     331X.
[52] Shahin Honarvar, Mark van der Wilk, and Alastair F Don-
     aldson. Turbulence: Systematically and automatically testing
     instruction-tuned large language models for code. In 2025 IEEE
     Conference on Software Testing, Verification and Validation
     (ICST), pages 80–91. IEEE, 2025.
[53] D. Zheng, Y. Wang, E. Shi, R. Zhang, Y. Ma, H. Zhang, and
     Z. Zheng. Humanevo: An evolution-aware benchmark for more
     realistic evaluation of repository-level code generation. In 2025
     IEEE/ACM 47th ICSE, pages 764–764. IEEE Computer Society,
     2025.
[54] T. Zhang, Y. Yu, X. Mao, S. Wang, K. Yang, Y. Lu, Z. Zhang,
     and Y. Zhao. Instruct or interact? exploring and eliciting
     llms’ capability in code snippet adaptation through prompt
     engineering. In 2025 IEEE/ACM 47th ICSE, page 566–577.
     IEEE Computer Society, 2025.
[55] Z. Tian, J. Chen, and X. Zhang. Fixing large language models’
     specification misunderstanding for better code generation. In
     2025 IEEE/ACM 47th ICSE, pages 1514–1526. IEEE Computer
     Society, 2025.
[56] H. Song, A. Goknil, X. Jiang, E. Melum, H. Joe, C. Gazzotti,
     V. Frascolla, A. N. Videsjorden, and P. Nguyen. Developing


                                                                         13
