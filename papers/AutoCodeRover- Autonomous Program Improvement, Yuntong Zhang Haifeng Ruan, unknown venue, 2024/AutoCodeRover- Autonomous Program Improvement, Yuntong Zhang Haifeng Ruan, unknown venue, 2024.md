                                                         AutoCodeRover: Autonomous Program Improvement
                                                                          Yuntong Zhang                                                                    Haifeng Ruan
                                                                National University of Singapore                                                  National University of Singapore
                                                                  yuntong@comp.nus.edu.sg                                                             hruan@comp.nus.edu.sg

                                                                               Zhiyu Fan                                                             Abhik Roychoudhury
                                                                National University of Singapore                                                 National University of Singapore
                                                                  zhiyufan@comp.nus.edu.sg                                                           abhik@comp.nus.edu.sg

                                         Abstract                                                                                    CCS Concepts
                                         Researchers have made significant progress in automating the soft-                          • Software and its engineering → Automatic programming;
arXiv:2404.05427v3 [cs.SE] 25 Jul 2024




                                         ware development process in the past decades. Automated tech-                               Maintaining software; Software testing and debugging; • Com-
                                         niques for issue summarization, bug reproduction, fault localiza-                           puting methodologies → Natural language processing.
                                         tion, and program repair have been built to ease the workload of
                                         developers. Recent progress in Large Language Models (LLMs) has                             Keywords
                                         significantly impacted the development process, where developers                            large language model, automatic program repair, autonomous soft-
                                         can use LLM-based programming assistants to achieve automated                               ware engineering, autonomous software improvement
                                         coding. Nevertheless, software engineering involves the process
                                                                                                                                     ACM Reference Format:
                                         of program improvement apart from coding, specifically to enable                            Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury. 2024.
                                         software maintenance (e.g. program repair to fix bugs) and software                         AutoCodeRover: Autonomous Program Improvement. In Proceedings of
                                         evolution (e.g. feature additions). In this paper, we propose an auto-                      the 33rd ACM SIGSOFT International Symposium on Software Testing and
                                         mated approach for solving Github issues to autonomously achieve                            Analysis (ISSTA ’24), September 16–20, 2024, Vienna, Austria. ACM, New
                                         program improvement. In our approach called AutoCodeRover,                                  York, NY, USA, 13 pages. https://doi.org/10.1145/3650212.3680384
                                         LLMs are combined with sophisticated code search capabilities, ul-
                                         timately leading to a program modification or patch. In contrast to                         1   Beyond Automatic Programming
                                         recent LLM agent approaches from AI researchers and practitioners,                          Automating software engineering tasks has long been a vision
                                         our outlook is more software engineering oriented. We work on a                             among software engineering researchers and practitioners. One of
                                         program representation (abstract syntax tree) as opposed to view-                           the key challenges has been the handling of ambiguous natural lan-
                                         ing a software project as a mere collection of files. Our code search                       guage requirements, in the process of automatic programming. In
                                         exploits the program structure in the form of classes/methods to en-                        addition, there has been progress in some other software engineer-
                                         hance LLM’s understanding of the issue’s root cause, and effectively                        ing activities such as automated test generation [5, 7], automated
                                         retrieve a context via iterative search. The use of spectrum-based                          program repair [13], and so on.
                                         fault localization using tests, further sharpens the context, as long                          Recent progress in large language models (LLMs) and the ap-
                                         as a test-suite is available. Experiments on the recently proposed                          pearance of tools like Github Copilot [32] hold significant promise
                                         SWE-bench-lite (300 real-life Github issues) show increased efficacy                        in automatic programming. This progress immediately raises the
                                         in solving Github issues (19% on SWE-bench-lite), which is higher                           question of whether such automatically generated code can be
                                         than the efficacy of the recently reported Swe-agent. Interestingly,                        trusted to be integrated into software projects, and if not, what
                                         our approach resolved 57 GitHub issues in about 4 minutes each                              improvements to the technology are needed. One possibility is to
                                         (pass@1), whereas developers spent more than 2.68 days on av-                               automatically repair generated code to achieve trust. This brings
                                         erage. In addition, AutoCodeRover achieved this efficacy with                               out the importance of automating program repair tasks towards
                                         significantly lower cost (on average, $0.43 USD), compared to other                         achieving the vision of autonomous software engineering.
                                         baselines. We posit that our workflow enables autonomous software                              Given this motivation of automating program repair, and the
                                         engineering, where, in future, auto-generated code from LLMs can                            large number of hours developers often spend manually fixing
                                         be autonomously improved.                                                                   bugs, we looked into the possibility of fully autonomous program
                                                                                                                                     improvement. Specifically, we feel that bug fixing and feature addi-
                                                                                                                                     tion are the two key categories of tasks that a development team
                                                                                                                                     may focus on when maintaining an existing software project. To
                                                                                                                                     achieve this goal, we proposed an approach that augments LLM
                                         Permission to make digital or hard copies of all or part of this work for personal or       with context knowledge from the code repository. We call our tool
                                         classroom use is granted without fee provided that copies are not made or distributed       AutoCodeRover.
                                         for profit or commercial advantage and that copies bear this notice and the full citation
                                         on the first page. Copyrights for third-party components of this work must be honored.         Technically our solution works as follows. Given a real-life
                                         For all other uses, contact the owner/author(s).                                            GitHub issue, LLM first analyzes the attached natural language de-
                                         ISSTA ’24, September 16–20, 2024, Vienna, Austria                                           scription to extract keywords that may represent files/classes/meth-
                                         © 2024 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-0612-7/24/09                                                            ods/code snippets in the codebase. Once these keywords are identi-
                                         https://doi.org/10.1145/3650212.3680384                                                     fied, we employ a stratified strategy for the LLM agent to retrieve
ISSTA ’24, September 16–20, 2024, Vienna, Austria                                     Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury


code context by invoking multiple necessary code search APIs                It is well-known in empirical software engineering research that
at one time with the keyword combinations as arguments (e.g.,               time limits of 30-60 minutes for automated repair are tolerable,
search_method_in_file). These code search APIs are running lo-              based on extensive developer surveys in the field [31]. We thus
cally based on AST analysis and are responsible for retrieving code         report 19% efficacy on SWE-bench lite in solving GitHub issues,
context such as class signatures and method implementation details          within 4 minutes. We can compare this time limit of 4 minutes to
from a particular location in the codebase. By collecting the project       the average time of 2.68 days to fix the GitHub issues manually.
context with code search APIs, LLM refines its understanding of           • One should be able to exploit debugging techniques like test-
the issue based on the currently available context. Note that our           based fault localization to guide the search for code in resolving
code context retrieval will proceed in an iterative fashion. The LLM        GitHub issues. We show that the use of fault localization in
agent directs the navigation and decides which code search APIs             setting the code context leads to an increase in the efficacy of
to use (i.e. where/what to retrieve code) in each iteration based on        AutoCodeRover in solving GitHub issues.
the current available context returned from the previous API calls.       • Finally, it is also useful to examine how many of the solved
AutoCodeRover then enquires whether there is sufficient project             GitHub issues are producing acceptable patches. We study the
context, and subsequently uses the collected context to derive the          patches produced by AutoCodeRover and report that 2/3 of
buggy locations. The patch construction is then handled by another          the autonomously produced patches from AutoCodeRover are
LLM agent which considers the buggy locations as well as all the            correct and acceptable. We note that this aspect has not been
context collected so far for those locations.                               reported by Devin [24] and SWE-agent [47].
   AutoCodeRover also can leverage debugging techniques such
as spectrum-based fault localization (SBFL) [44] to decide more
precise code search APIs for context retrieval if a test suite ac-        2 Relevant Literature
companying the project is available. SBFL primarily considers the
control flow of the passing and failing tests and assigns a suspi-        2.1 Program Repair
ciousness score to the different methods of the program. The LLM          Test-suite based automated program repair (APR) has attracted
agent may prioritize retrieving context from particular methods           significant attention in the last decade [13]. These techniques aim
and classes if the fault localization result is provided, e.g., when      to generate a patch for a buggy program to pass a given test-suite.
a method appears both in the issue description and in the output          APR techniques typically include search-based, semantic-based,
of fault localization. In the last step, AutoCodeRover may per-           and pattern/learning-based APR. Search-based APR techniques like
form patch validation using available tests, to determine whether         GenProg [42] take a buggy program and generate patches using
the patch produced by AutoCodeRover passes the tests in the               predefined code mutation operators, or search for a patch over
given test-suite. Otherwise, AutoCodeRover will rerun the patch           the patch space that passes the given test suite. Semantics-based
generation with a retry limit until a correct patch is found.             APR techniques [28, 30] generate patches by formulating a repair
                                                                          constraint that needs to be satisfied based on a given test suite
   Contributions. Our contribution lies in the effective use of code      specification, and then solving the repair constraint to generate
search to make software engineering processes like program repair         patches. Learning-based APR techniques [26, 38, 48] often train a
autonomous. Instead of viewing the codebase as a collection of files,     deep learning model with large code repositories and are guided by
we posit AutoCodeRover as an approach that gleans specification           a specific representation of code syntax and semantics to predict
from software structure, which is used to guide the patching. The         the next tokens that are most likely to be correct patch. There are
code search in AutoCodeRover is a vehicle for inferring specifi-          also works [23, 29, 39] that tried to leverage GitHub issues and bug
cation from program structure. We demonstrate this capability by          reports to improve APR effectiveness.
autonomously solving GitHub issues. We report favorable experi-               Recent work [10, 15, 46] have shown the use of LLMs for auto-
mental results on the SWE-bench lite dataset [17]. We achieve 19%         mated program repair. This line of work often assumes the buggy
efficacy on the SWE-bench lite with 300 GitHub issues. Overall,           program statements are given (i.e. perfect fault localization assump-
we see the need to endow a software engineering oriented outlook          tion) and focuses on constructing APR-specific prompts that guide
to the recent flurry of activity on LLM agents for software engi-         LLM to generate a patch for the selected buggy program statements
neering, which mostly has only an AI flavor. The angle of software        multiple times until a patch that passes all tests is found. The typical
engineering can be conveyed by the following five dimensions.             work targets repairing functional [10, 35, 41], type [9] bugs, and
• We work on program representations (abstract syntax tree or             even software vulnerabilities [11, 18, 33] in different languages with
  AST) as opposed to viewing a software project as a collection of        open-source/commercialised models (e.g., CodeT5, ChatGPT, GPT-
  files. We posit that working on program representations like AST        4, etc). However, obtaining buggy locations for a large project is an
  will be useful in autonomous software engineering workflows.            essential and challenging task in resolving real-life bug reports.
• To solve GitHub issues, we focus on code search in a way that               APR techniques have been successfully deployed in industries
  resembles the activity of a human software engineer. So we try          for domain-specific bug fixing [4, 27, 43]. However, a long-standing
  to use the program structure - classes, methods, code snippets          challenge for the APR techniques is to resolve general real-life
  - in searching for relevant code context. This leads to a more          software issues from scratch. The above APR techniques rely on
  effective usage of the context provided to LLM.                         a high-quality test suite which is not always available in the real
• We posit that higher efficacy of automated repair is more impor-        world and they do not leverage the valuable natural language spec-
  tant than time efficiency, as long as the time is within a threshold.   ification from the original problem description. To address these
AutoCodeRover: Autonomous Program Improvement                                                                                                                          ISSTA ’24, September 16–20, 2024, Vienna, Austria


             Issue Description                                                                                            Step 2
                                                                                                                                   1. Found 1 class with name ModelChoiceField.
             ModelChoiceField does not provide value of invalid choice when raising Validation Error.
                                                                                                                                      Signature: ... def to_python(): ... def validate(): ...
             Compared with ChoiceField and others, ModelChoiceField does not show the value of the
                                                                                                                                   2. Found 1 class with name ModelMultipleChoiceField.
             invalid choice when raising a validation error. Passing in parameters with the invalid value and
                                                                                                                                      Signature: ... def to_python(): ... def clean(): ...
             modifying the default error message for the code invalid_choice should fix this.
                                                                                                                                   3. Could not find method clean in ModelChoiceField.
             From source code:
                                                                                                                                   4. Found 1 method clean in ModelMultipleChoiceField. Code: ...
             class ModelMultipleChoiceField(ModelChoiceField):
                ... 'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'), ...
             class ModelChoiceField(ChoiceField):                                                                                  - ModelChoiceField class does not have a clean method. It likely uses
                ... 'invalid_choice': _('Select a valid choice. That choice is not one of the available choices.'), ...              another method like validate or to_python to validate inputs.
                                                                                                                                   - ModelMultipleChoiceField class incorporates the invalid value (%(value)s)
                                                                                                                                     into the error message. This is not the case for ModelChoiceField, which is
             Step 1                                                                                                                  likely the root of the issue.
                          Based on the issue, use the APIs below to get more context:
                                                                                                                                   - We might modify the validate or to_python method (since clean is not
                          - search_class(...).
                          - search_method_in_class(...)                                                                              directly overwritten) to customize the error message similarly to how
                                                                                                                                     ModelMultipleChoiceField does.
                          - search_code_in_file(...)
                                                                                                                                   - Next step: examine validate and to_python methods of ModelChoiceField.
                          - ......
                          Select necessary APIs. You can use multiple APIs.
                                                                                                                                   1. search_method_in_class("validate", "ModelChoiceField")
                                                                                                                                   2. search_method_in_class("to_python", "ModelChoiceField")
                          We need to understand how the ModelChoiceField and potentially the
                          ModelMultipleChoiceField classes handle validation and error messages. ...
                          Typically, Django fields use a clean method for validation.
                          1. search_class("ModelChoiceField")
                          2. search_class("ModelMultipleChoiceField")
                          3. search_method_in_class("clean", "ModelChoiceField")                                          Step 3
                                                                                                                                   1. Found 1 method validate in ModelChoiceField. Implementation is: ...
                          4. search_method_in_class("clean", "ModelMultipleChoiceField")
                                                                                                                                   2. Found 1 method to_python in ModelChoiceField. Implementation is:
                                                                                                                                     def to_python(self, value):
                                                                                                                                       ...
             Step 4                                                                                                                    raise ValidationError(self.error_messages['invalid_choice'],
                                                                                                                                             code='invalid_choice')
                          Here are the code in buggy locations:
                            ....
                          Write a patch for the issue, based on the retrieved context.                                             - validate method simply calls the validate method of its parent class.
                                                                                                                                   - to_python method is responsible for converting the input into a Python object.
                                                                                                                                     The ValidationError raised in to_python does not include the invalid value
                          <file>
                                                                                                                                     in the error message (consistent with the issue).
                             django/forms/models.py, Line 1287
                                                                                                                                   - Proposed solution: Adjust the error message to incorporate the value
                          </file>
                                                                                                                                     dynamically, similar to how ModelMultipleChoiceField includes %(value)s
                                                                                                                                     in its error message.
                          <patched>
                             raise ValidationError(self.error_messages['invalid_choice'] %
                                                                                                                                   Buggy location:
                                   {'value':value}, code='invalid_choice')
                                                                                                                                   1. File django/forms/models.py, class ModelChoiceField, method to_python
                          </patched>




                                   Figure 1: Issue description of django-13933 and AutoCodeRover’s workflow on it.


challenges and achieve autonomous software engineering, we focus                                                           engineer that can solve various software engineering tasks, includ-
on resolving GitHub issues from a real-life dataset.                                                                       ing building a project from scratch, bug-fixing/feature-addition for
                                                                                                                           existing projects. However, it is a close-sourced commercial tool,
2.2     LLM Agents for SE and Dataset                                                                                      and its details are not available. Swe-agent [47] is a concurrent
SWE-bench lite [17] is a benchmark that aims to evaluate the capa-                                                         work against AutoCodeRover. It designed an agent-computer in-
bilities of large language models in resolving end-to-end real-life                                                        terface (ACI) that allows LLM agents to execute basic file operations
software engineering tasks. The benchmark consists of 300 real-life                                                        via shell commands to achieve interaction between the LLM en-
software engineering task instances collected from the repositories                                                        gine and a software repository. Compared to Swe-agent, we posit
of 11 popular large Python projects 1 (e.g., django, sympy). Each                                                          AutoCodeRover as an approach that gleans specification from
SWE-bench lite task instance contains a pair of Github issue and                                                           software structure, which is used to guide the patching. Instead of
corresponding pull requests. The GitHub issue either reports a bug                                                         viewing the codebase as a collection of files.
to be fixed or requests to implement new features. The pull request
includes the code changes made by human developers to resolve the
                                                                                                                           3       Motivating Example
issue and test cases that prevent the issue. Unlike traditional code                                                          In this section, we illustrate how our tool AutoCodeRover can
generation tasks in HumanEval [8] and MBPP [25] benchmark,                                                                 collect code context and generate a patch from an issue description
resolving a SWE-bench lite instance is particularly challenging                                                            and the corresponding project code-base. We show an example
because it requires automatically generating code changes that                                                             of a feature addition task. Figure 1 demonstrates the workflow
address the problem in a GitHub issue for a matured large code                                                             of AutoCodeRover on an issue submitted to the Django issue
repository based only on the issue description. More specifically,                                                         tracker2 . This issue is classified as “New feature” in the issue tracker,
the process may involve a series of complex tasks like reasoning                                                           and is included in SWE-bench lite with the id “django-13933”. The
the target bug location across files in the code repository, analyz-                                                       first part of Figure 1 shows the issue description (the code part is
ing the root cause of the issue, proposing bug-fixing strategies,                                                          simplified for brevity). This issue requests adding support to the
and eventually writing a patch that passes all the test cases added                                                        ModelChoiceField class, so that it “shows the value of the invalid
in the pull request. There are a few primary attempts at tackling                                                          choice when raising a validation error”.
tasks in SWE-bench lite. Devin [24] is named the first AI software                                                            With this issue description, AutoCodeRover operates in two
                                                                                                                           stages - context retrieval (Step 1-3 in Figure 1) and patch generation
1 https://www.swebench.com/index.html                                                                                      2 https://code.djangoproject.com/ticket/32347
ISSTA ’24, September 16–20, 2024, Vienna, Austria                                                               Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury




                                                                                                              "Code at buggy
                   "Collect context by                               No
                                              API invocations                                                   location: ...
                    invoking APIs."                                                                         Please write patch."
  Problem                                                                             Yes    Buggy                                                          Can be    Yes
                                                                      sufficient?                                                  Patch generation                         Final patch
 Statement                                                                                  locations                                                      applied?
                                                                                                             "Patch cannot be
                     "Results of the
                                              Context analysis                                              applied to program.
                    invocations: ..."
                                                                                                             Please try again."
                                                                                                                                     No
                                                            Context retrieval stage                                                            Patch generatation stage



                                                      Figure 2: Overall workflow of AutoCodeRover.

""" AutoCodeRover patch . """                                                                      to be the more suitable place to make changes, since to_python
  except ( ValueError , TypeError , self . queryset . model . DoesNotExist ):
-     raise ValidationError ( self . error_messages [ ' invalid_choice '],
                                                                                                   raises the relevent exception and does not include the invalid value.
-          code = ' invalid_choice ')                                                              At this point, the retrieval agent deems the collected code context
+     % Include the invalid value in the error message                                             as sufficient for understanding the issue and drafting the patch. The
+     raise ValidationError (
+          self . error_messages [ ' invalid_choice '] % { ' value ': value },                     identified buggy location, together with the gathered context and
+          code = ' invalid_choice ')                                                              analysis so far, is passed to another patch generation agent. This
""" Developer patch . """
                                                                                                   agent is instructed to write patches following the format described
  except ( ValueError , TypeError , self . queryset . model . DoesNotExist ):
-     raise ValidationError ( self . error_messages [ ' invalid_choice '],                         in Step 4 (see yellow box) of Figure 2. In Step 4, a patch is written to
-          code = ' invalid_choice ')                                                              allow a value to be integrated into the error message, by utilizing
+     raise ValidationError (
+          self . error_messages [ ' invalid_choice '],
                                                                                                   %-formatting in Python. Figure 3 shows the patch generated by
+          code = ' invalid_choice ',                                                              AutoCodeRover and the developer. Although written in a different
+          params ={ ' value ': value } ,)                                                         way compared to the developer patch, this patch achieves similar
                                                                                                   effect and passes the developer provided test-suite for this issue.
Figure 3: AutoCodeRover and developer patch for Django-
13933.                                                                                             4     AI Program Improvement Framework
                                                                                                   In this section, we discuss the design of AutoCodeRover. Au-
(Step 4). First, a context retrieval LLM agent is instructed to collect                            toCodeRover is a system incorporating AI agents for program
the relevant code context related to this issue, from a local copy                                 improvement tasks in large software projects. AutoCodeRover
of the Django project codebase. This retrieval is achieved by in-                                  is designed to work in a realistic software development lifecycle,
ferring relevant names (e.g. ModelChoiceField) and searching for                                   in which users submit issue reports to a software repository de-
them in the Abstract Syntax Tree (AST) of the project. A set of re-                                scribing a bug, and the project maintainers craft a patch to resolve
trieval APIs are provided to the agent. In Step 1, the agent identifies                            the issue. With a submitted issue, AutoCodeRover autonomously
the classes ModelChoiceField and ModelMultipleChoiceField                                          analyzes the submitted issue, retrieves the relevant code context in
might be relevant based on the issue description, and infers that a                                the software project, and generates a patch. This patch can then be
clean method might be also of interest for validation-related issues.                              vetted by human developers. If such a tool can automatically handle
It then invokes the search_class and search_method_in_class                                        a certain percentage of the issues awaiting developers’ attention,
APIs to retrieve more information about them.                                                      manual efforts are reduced.
    In Step 2, API invocations return the signature of the classes and
implementation of the methods found. Results of invocation #3 re-                                  4.1    Overview
veals the absence of method clean in the class ModelChoiceField,                                   We first describe the overall stages AutoCodeRover operates in,
which helps to refine the agent’s understanding from Step 1. The re-                               and will proceed in more details in the rest of this section. The
turned class signature from invocation #1 also reveals two more rele-                              overall workflow of AutoCodeRover is shown in Figure 2. Au-
vant methods to_python and validate, which were not mentioned                                      toCodeRover takes in as input a problem statement 𝑃 of the issue
in the issue description. This suggests the retrieval should be per-                               to be resolved, and a codebase 𝐶 of the corresponding software
formed iteratively in multiple steps, so that results from a previous                              project. This problem statement 𝑃 contains the title and descrip-
search can become arguments of the following search. In this exam-                                 tion of the issue, as shown in Section 3. From a problem statement
ple, the agent then iteratively invokes search_method_in_class                                     written in natural language, AutoCodeRover analyzes the require-
on the two newly revealed methods. Furthermore, by referenc-                                       ment from it and proceeds in two main stages, which are context
ing results from multiple invocations, the agent can infer that                                    retrieval and patch generation.
ModelMultipleChoiceField incorporates the invalid value into                                          In the context retrieval stage, AutoCodeRover employs an LLM
the message with %(value)s, and methods in ModelChoiceField                                        agent to navigate through a potentially large codebase 𝐶 and ex-
can be modified similarly to ModelMultipleChoiceField.                                             tract the relevant code snippets relevant to 𝑃. This navigation is
    In Step 3, the agent receives the implementation of validate and                               facilitated by a set of context retrieval APIs (Section 4.2), which
to_python methods. Among the two methods, it selects to_python                                     enables an LLM to retrieve information about the project (e.g. class
AutoCodeRover: Autonomous Program Improvement                                                                  ISSTA ’24, September 16–20, 2024, Vienna, Austria


                                                    Table 1: List of Context Retrieval APIs.

      API name                               Description                                     Output
      search_class (cls)                     Search for class cls in the codebase.           Signature of the searched class.
      search_class_in_file (cls, f)          Search for class cls in file f.                 Signature of the searched class.
      search_method (m)                      Search for method m in the codebase.            Implementation of the searched method.
      search_method_in_class (m, cls)        Search for method m in class cls.               Implementation of the searched method.
      search_method_in_file (m, f)           Search for method m in file f.                  Implementation of the searched method.
      search_code (c)                        Search for code snippet c in the codebase.      +/- 3 lines of the searched snippet c.
      search_code_in_file (c, f)             Search for code snippet c in file f.            +/- 3 lines of the searched snippet c.


signatures) and actual code snippets (e.g. method implementations).           (Issue sympy-12481)
The context retrieval agent directs this navigation, and decides              Permutation constructor fails with non-disjoint cycles.
which retrieval APIs to use based on the current available context.
                                                                              Calling Permutation([[0,1],[0,1]]) raises a ValueError instead of constructing
In order to make the LLM-directed navigation more “controlled”, we
                                                                              the identity permutation. If the cycles passed in are non-disjoint, they should be
devise a stratified stategy of invoking the retrieval APIs (Section 4.3).     applied in left-to-right order and the resulting permutation should be returned.
This stratified strategy instructs the LLM to only invoke necessary
retrieval APIs based on the available information, and iteratively            This should be easy to compute. I don't see a reason why non-disjoint cycles
                                                                              should be forbidden.
changes the set of retrieval APIs used when more code-related
context are returned from the previous API calls.                             (Issue django-13230)
    Once the context retrieval agent has gathered sufficient context          Add support for item_comments to syndication framework.
about the issue, AutoCodeRover proceeds to the patch generation
                                                                              Add comments argument to feed.add_item() in syndication.views so that
stage (Section 4.5). In this stage, AutoCodeRover employs another             item_comments can be defined directly without having to take the detour via
LLM agent to extract more precise code snippets from the retrieved            item_extra_kwargs.
context, and craft a patch based on the extracted code snippets. This         Additionally, comments is already explicitly mentioned in the feedparser, but
patch generation agent is instructed to craft a patch in a specific           not implemented in the view.

format, and if the produced patch does not follow the format spec-
ification or cannot be applied to the original codebase, the agent
                                                                            Figure 4: Issue description of sympy-12481 and django-13230.
enters a retry-loop which terminates after a pre-configured number
                                                                            “Hints” are highlighted.
of attempts. Finally, AutoCodeRover outputs a patch that attempts
to resolve the original issue.
    We note that the workflow of AutoCodeRover discussed so far
only requires the problem statement 𝑃 and codebase 𝐶 as input,              the project that is relevant to the current issue. Figure 4 illustrates
and do not require any program specifications such as testcases.            two real-world issues submitted to the sympy and django projects,
However, when testcases are available (e.g. provided by develop-            respectively, and the “hints” are highlighted. In sympy-12481, the
ers or generated from another tool), execution-based information            class Permutation is mentioned twice; in django-13230, multiple
and program analysis techniques can be integrated into the Au-              hints are mentioned, such as code snippet feed.add_item(), pack-
toCodeRover framework (Section 4.4). For example, statistical               age path syndication.views, method name item_extra_kwargs
fault localization [44] tool can be used to reveal more relevant            and etc. Based on the type of project and code related hints, we
methods beyond those mentioned in the problem statement. The                design a set of APIs for an LLM agent to retrieve code context from
additionally revealed code context can thereby influence the set of         these hints. The current set of APIs in AutoCodeRover and their
retrieval APIs invoked in the context retrieval stage. Moreover, with       outputs are shown in Table 1. Once invoked by the LLM agent,
testcases available, the patch generation agent can employ an addi-         the retrieval APIs search for classes, methods and code snippets in
tional patch validation step in its retry-loop when crafting a patch.       the code-base, and return the results back to the agent. To avoid
In the remainder of this section, we discuss in greater detail the          forming very lengthy code context that creates distraction during
components of AutoCodeRover and their design considerations.                patch generation, we return only necessary information as API
                                                                            outputs. For example, since the complete definition of a class can
4.2    Context Retrieval APIs                                               be lengthy in large projects, we only return signature of the class as
                                                                            output for search_class and search_class_in_file. Returning
In the context retrieval stage, the basic components are a set of APIs      the signature to shorten cntext, is a better approach than cutting off
which an LLM agent can use to gather relevant code context and              the context at a certain bound. Upon receiving the class signature,
snippets from the codebase. For typical software project issues, we         the agent could then invoke another API to search for the relevant
observe that users often mention some “hints” on which part of the          methods / snippets inside the class.
codebase is relevant. These hints can be the names of the relevant
methods, classes, or files, and sometimes also contain short code              Interfacing with LLM. For the LLM agent to invoke the context
snippets. Although these hints may not directly point to the precise        retrieval APIs, the description and expected output of them are
location for code modification, they often reveal code context in           presented to it as part of prompt. When the agent decides to invoke
ISSTA ’24, September 16–20, 2024, Vienna, Austria                                                      Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury


                             Stratum 1                                             Stratum 2                          Stratum k

                        search_class(classA)
                                                                                                                                              <Project context k>
                                                                               search_class(classB)                                           Context sufficient.
       Problem
      Statement
                      search_method(methodA)
                                                     <Project context 1>
                                                    Context not sufficient.
                                                                                                         ...     search_method_in_class
                                                                                                                    (methodC, classB)         Buggy location is:
                                                                              search_method_in_class
                                                                                                                                              1. ClassA.methodB
                                                                                 (methodB, classA)
                         search_code_in_file                                                                                                  2.ClassB.methodC
                           (code_str, fileA)


                                         Figure 5: Stratified search with retrieval APIs for context gathering.


a set of retrieval APIs, it responds with the list of API call names                      After the API invocations in a stratum are executed, the newly
and the corresponding arguments. These retrieval API requests are                      retrieved code snippets are added to the current context. The LLM
processed locally by parsing a local codebase of the project into                      agent is then prompted to analyze whether the current context is
AST and searching over it. Results of locally executing these APIs                     sufficient for understanding the issue, thereby deciding whether (a)
are returned to the agent, forming the code context.                                   we continue the iterative search process, or (b) we decide on the
                                                                                       buggy locations which will be considered for fixing.

4.3     Stratified Context Search                                                      4.4       Analysis-Augmented Context Retrieval
The set of context retrieval APIs listed in Table 1 serves as build-                   We also investigate how program debugging techniques can aug-
ing blocks for searching relevant code context. With the context                       ment our workflow. Specifically, we integrate the Spectrum-based
retrieval APIs and the LLM-identified keyword “hints” from the                         Fault Localization (SBFL) analysis into AutoCodeRover to study
problem statement, a set of possible API invocations can be derived                    the effect of such a test-based dynamic analysis. We make a test-
by using the identified keywords as API parameters. We discuss                         suite 𝑇 available to AutoCodeRover, in addition to the problem
a few observations on using these API invocations to gather code                       statement 𝑃 and codebase 𝐶.
context, and propose a stratified context retrieval process.
    Our first observation is that the context retrieval should not                         Spectrum-based Fault Localization. The goal of SBFL is to identify
be restricted to a single API invocation. For example, in the issue                    the location of software faults [45]. Given a test-suite 𝑇 containing
django-13230 mentioned in Figure 4, if the retrieval starts from                       both passing and failing tests, SBFL considers control-flow differ-
the invocation search_method("add_item"), the implementation                           ences in the passing and failing test executions, and assigns a suspi-
of method add_item can be considered by the LLM agent as a                             ciousness score to different program locations. This suspiciousness
sufficient context, since it appears to be relevant to the problem                     score can be computed with various metrics such as Tarantula [21]
statement. However, searching from only one method can lead to                         and Ochiai [3]. Program elements (e.g. statements/basic blocks)
incomplete context for the agent to reason about root cause of the                     with the highest suspiciousness scores are identified as likely fault
problem. On the other hand, if all API invocations are executed at                     locations. SBFL can be performed at different granularities of pro-
once, a large code context can be retrieved, especially when the                       gram elements, such as statements or basic blocks. Since the LLM
problem statement mentions many class and method names. This                           can process reasonably long code snippets, we use method-level
large code context can be difficult for an LLM to comprehend, or                       SBFL in AutoCodeRover. Given an test-suite, SBFL can be used to
may even exceed its context window.                                                    directly output a few program locations to be repaired. However, the
    The second observation is that some of the API invocation results                  accuracy of SBFL highly relies on the quality of the test-suite [22]
provide more elements to build new possible API invocations, which                     - since the SBFL results are effectively an abstraction of the dif-
means the process of invoking retrieval APIs should be iterative.                      ferential of control flows between passing tests and failing tests.
For example, the result of a search_class call returns the method                      Therefore, instead of replacing the stratified context retrieval with
signatures within the searched class, and an LLM can iteratively                       SBFL, we use the SBFL identified methods to augment the search
invoke method-related APIs afterwards.                                                 process. Before AutoCodeRover enters the context retrieval stage,
    With these two observations, we propose a stratified search                        we provide the SBFL-identified methods to the LLM agent as “re-
process for invoking context retrieval APIs, as illustrated in Figure 5.               sults from an external analysis tool that identifies suspicous code”.
From a problem statement, stratified search iteratively invokes                        The main role of SBFL-identified methods is to reveal more “hints”
retrieval APIs to gather project code context, and finally outputs a                   on relevant classes and methods beyond those mentioned in the
list of potentially buggy locations to be fixed. In each stratum, we                   problem statement. The LLM agent can then use the context re-
prompt the LLM agent to select a set of necessary API invocations,                     trieval APIs to examine these methods. Since the SBFL-identified
based on the current context. In stratum 1, the current context only                   methods are presented to the agent together with the problem
contains the problem statement; in the following strata, the context                   statements, the agent can then cross-reference between these two
contains both the problem statement and the code searched so far.                      sources of information. For example, if one of the SBFL-identified
By allowing LLM to select more than one API invocations and also                       method names is more closly related to the problem statement, the
instructing it to only select the necessary ones, we make the best                     LLM is more likely to invoke the search_method API on this name.
use of the context, building what we deem an optimal context.                          We will demonstrate this observation in Section 6.2.
AutoCodeRover: Autonomous Program Improvement                                                       ISSTA ’24, September 16–20, 2024, Vienna, Austria


4.5     Patch Generation                                                 refining the issue description, and writing a final patch. For param-
In the patch generation stage, AutoCodeRover employs a patch             eters of GPT-4, we set a low temperature=0.2, max_tokens=1024
generation agent to use the collected code context to write a patch      to produce relatively deterministic results and enable sufficient
for the problem statement. This agent is given the problem state-        reasoning length for AutoCodeRover, and all other parameters
ment, the identified buggy locations/methods, and the history of         remain as per default. AutoCodeRover terminates either a patch
context retrieval, including the invoked APIs, the API results, as       is generated or the context retrieval stage repeats ten times. Exper-
well as the previous analysis on the code context made by the            iment results and artifacts for AutoCodeRover can be found at
context retrieval agent.                                                 https://github.com/nus-apr/auto-code-rover.
   As a first step, the patch generation agent retrieves the precise
code snippets at the buggy locations from the codebase. Based               System Environment. All experiments are conducted on an x86_64
on the precise code snippets and other relevant code context, the        Linux server with Ubuntu 20.04 installed. The correctness of gen-
agent enters a retry-loop of generating patches. If a generated patch    erated patches by AutoCodeRover is evaluated on the official
does not follow the specified patch format or could not be applied       SWE-bench docker environment.
syntactically to the original program, the agent is prompted to retry.
We also employs a linter to indentify Python-specific syntax issues      6 Evaluation
such as indentation errors in this retry-loop. The agent is allowed to
retry up to a pre-configured attempt limits (currently set to three),
                                                                         6.1 RQ1: Overall Effectiveness
after which the best patch so far is returned as output.                 We first measure the overall effectiveness of AutoCodeRover
                                                                         and baselines with the number of resolved task instances in SWE-
5     Experiment Setup                                                   bench. With the goal of understanding to what extent the current
                                                                         AI systems can automatically resolve real-life software issues, the
To evaluate the capabilities of AutoCodeRover in resolving real-
                                                                         only inputs we provided are the natural language issue description
life software issues, we answer the following research questions.
                                                                         and a local code repository checked out at the erroneous version.
RQ1: To what extent can AutoCodeRover automate software                  We repeated the experiment of AutoCodeRover three times to
issues like human developers?                                            avoid randomness and presented the results in pass@1 and pass@3
RQ2: Can existing debugging / analysis techniques assist                 metrics [8], which are denoted as AutoCodeRover @1 and Au-
AutoCodeRover?                                                           toCodeRover @3 respectively. When reporting time and token/-
RQ3: What are the challenges for AutoCodeRover and fully au-             cost for AutoCodeRover @3, we report the time and cost required
tomated program improvement in future?                                   for running each task three times. Since Devin was evaluated on a
                                                                         random 25% subset of SWE-bench [24], we also report results of Au-
  Benchmark. We evaluate AutoCodeRover in recently proposed
                                                                         toCodeRover on this subset (we refer to this as “SWE-bench Devin
benchmarks SWE-bench and SWE-bench lite [17], comprising 2294
                                                                         subset”). Table 2 shows the overall result of AutoCodeRover in
and 300 real-life GitHub issues, respectively. The only input is the
                                                                         SWE-bench lite, full SWE-bench and SWE-bench Devin subset and
natural language description in the original GitHub issue and its
                                                                         Figure 7 shows a visual efficacy summary of AutoCodeRover’s
corresponding buggy codebase. Details of SWE-bench and SWE-
                                                                         comparison with Swe-agent, Devin.
bench lite appear in Section 2.2.

   Baseline and Evaluation Metric. We selected two LLM-based                Results on SWE-bench. The results reported in Table 2 indicate
agent systems Devin [24], Swe-agent [47] as baselines and com-           that in the full SWE-bench, AutoCodeRover @1 resolved 12.42%
pare their performance against AutoCodeRover. We directly com-           task instances with 248 seconds per task, and AutoCodeRover
pare AutoCodeRover with Swe-agent’s original results as it is            @3 resolved 17.96% task instances taking a time of 701 seconds per
publicly available at GitHub3 . In contrast to Swe-agent, we do not      task, which is at par with 12.47% resolved tasks by the concurrent
have access to Devin, so we take the most relevant reported result       work Swe-agent, according to their technical report [47]. We also
from their technical report [40]. To avoid the natural randomness of     performed another round of experiments with AutoCodeRover on
LLM, we repeat our experiments three times. We report the result         SWE-bench lite (300 instances). AutoCodeRover @1 resolved 19%
with the AutoCodeRover @1 and AutoCodeRover @3 anno-                     task instances in taking an average time of 195 seconds, whereas
tations (i.e. pass@1, pass@3 metrics [8] respectively). We use (1)       Swe-agent resolved 18% task instances. Moreover, we also investi-
the percentage of resolved instances, (2) average time cost, and (3)     gated AutoCodeRover @3 in SWE-bench lite, in which the per-
average token cost to evaluate the effectiveness of the tools. These     centage of resolved task instances increased to 26%. The results of
evaluation metrics represent overall effectiveness, time efficiency,     AutoCodeRover @3 in SWE-bench imply that AutoCodeRover
and economic efficacy in resolving real-world GitHub issues.             may be complemented by running multiple times, highlighting
                                                                         the possibility of improving AutoCodeRover with an iterated
   Implementation and Parameters. We use the state-of-the-art Ope-       generate-and-validate process in the future, if any program specifi-
nAI GPT-4 (gpt-4-0125-preview) as foundation inference model             cation is available.
for AutoCodeRover. In AutoCodeRover, the GPT-4 model is
responsible for selecting search APIs to retrieve codebase context,         Comparison with Devin. To compare with Devin, we report Au-
                                                                         toCodeRover’s result on the 570 task instances (random 25% subset
3 https://github.com/princeton-nlp/SWE-agent                             of SWE-bench) Devin [24] was evaluated on. The results of Devin
ISSTA ’24, September 16–20, 2024, Vienna, Austria                                                 Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury


Table 2: Overall Result of AutoCodeRover and baselines on
full SWE-bench, SWE-bench Devin subset, and SWE-bench
lite. "-" indicates data not available.                                                             AutoCodeRover                SWE-agent
                                                                                                       Unique:  Common:          Unique:
                                                                                                         26       31               23
 Tools                         Resolved Tasks Avg Time Avg Tokens
          Reported result on SWE-bench lite (size=300)
 Swe-agent [47]        18.00% (54)    -            245k ($2.51)
 AutoCodeRover @1 19.00% (57)         195          37k ($0.43)
 AutoCodeRover @3 26.00% (78)         520          112k ($1.30)                        Figure 6: Venn diagrams of resolved tasks instances by Au-
 ACR-sbfl              22.00% (66)    250          40k ($0.47)                         toCodeRover and Swe-agent, on SWE-bench lite.
        Reported result on full SWE-bench (size=2294)
 Swe-agent [47]       12.47% (286)    -           240k ($2.46)
 AutoCodeRover @1 12.42% (285)        248         39k ($0.45)
 AutoCodeRover @3 17.96% (422)        701         120k ($1.39)
    Reported result on SWE-bench Devin subset (size=570)
 Swe-agent [47]        13.51% (77)   -           234k ($2.40)
 Devin [24, 40]4       13.86% (79)   > 600       -
 AutoCodeRover @1 12.63% (72)        238         37k ($0.42)
 AutoCodeRover @3 18.77% (107)       692         117k ($1.36)


are taken from their technical report [40]. In this Devin partic-
ular subset, AutoCodeRover successfully resolved 12.63% task
instances on average in pass@1, and 18.77% of the task instances                       Figure 7: Task-resolving success rates (%) and average costs
in pass@3, which is higher than Devin. Besides, the time taken by                      per task in USD of AutoCodeRover and baselines.
AutoCodeRover is much smaller than Devin.
   Detailed Comparison with Swe-agent. In the rest of RQ1, we
compare AutoCodeRover with Swe-agent on SWE-bench lite
using the highlighted AutoCodeRover @1 result. We further an-
alyzed the commonly and uniquely resolved instances between
AutoCodeRover and Swe-agent in Figure 6, and we found that
AutoCodeRover and Swe-agent complement each other in differ-
ent scenarios. AutoCodeRover uniquely resolved 26 task instances,
which benefited from the fine-grained code context search at the
AST level to precisely locate the bug locations (e.g., django-13401
searches three necessary methods at one time). On the other hand,
the main reason that AutoCodeRover failed on the 23 unique in-
stances resolved by Swe-agent is unimplemented search APIs (e.g.,                      Figure 8: The number of resolved tasks and token cost distri-
search_file invoked in django-12286). When such unimplemented                          butions of AutoCodeRover and Swe-agent.
APIs are invoked, AutoCodeRover returns an error message to
the LLM, but the LLM may still fail to invoke valid search APIs in
later attempts. This implies more robust search APIs are desired for                   publicly available. When considering the combined three repeti-
future improvement of AutoCodeRover.                                                   tions, AutoCodeRover takes 520 seconds (~8.67 minutes) per task,
                                                                                       which is below the 30-60 minute time limit deemed acceptable by
   Time / Token Cost. Today, the price of invoking state-of-the-art
                                                                                       developers for automated repair tools [31]. Looking into the 78
LLMs such as GPT-4 and Claude-3-Opus are still very expensive.
                                                                                       issues resolved by AutoCodeRover @3 in SWE-bench lite, it costs
Hence, we are also interested in assessing the feasibility of deploy-
                                                                                       on average ~2.68 days for developers to create pull requests for
ing AutoCodeRover in the real world in terms of time and eco-
                                                                                       66 issues, and the other 12 issues take even longer to be closed
nomic cost. Figure 7 shows the comparison between task-resolving
                                                                                       by developers (ranging from 34 - 4023 days). The short response
success rate and average costs per task for all tools. On average,
                                                                                       time and significantly low success-rate/cost ratio show the poten-
AutoCodeRover takes 195 seconds and 37k tokens (equivalent
                                                                                       tial for AutoCodeRover to act as a first affordable step in future
to 0.43 USD) to resolve one task instance in SWE-bench lite. In
                                                                                       autonomous bug fixing.
comparison, Swe-agent costs 245k tokens (equivalent to 2.51 USD)
per task instance. The cost of Devin is empty because it is not                           Token Distribution of Resolved Tasks. We dived into the details
                                                                                       of token cost distribution among resolved task instances by Au-
4 The reported result of Devin is evaluated on a random 25% subset of full SWE-bench   toCodeRover and Swe-agent in Figure 8. The x-axis represents
AutoCodeRover: Autonomous Program Improvement                                                                      ISSTA ’24, September 16–20, 2024, Vienna, Austria


token cost ranges and the y-axis represents the number of re-                    Saving parent object after setting on child leads to data loss for parents with
solved tasks. Figure 8 shows that regarding the resolved tasks,                  non-numeric primary key.
                                                                                 Given a model with a ForeignKey relation to another model that has a non-auto
AutoCodeRover is even more token-efficient. AutoCodeRover                        CharField as its primary key:
resolved 19 tasks with less than 10k tokens (~0.1 USD) and 31 tasks                class Product(model.Model): ...
                                                                                   class Order(model.Model): ...
between 10k-30k tokens, whereas 66.7% of resolved tasks by Swe-                  If the relation is initialized on the parent with an empty instance ...
agent at least requires more than 100k tokens. This implies the                  Instead of product_id being populated with product.sku, it is set to empty string. ...
strong capability of stratified context retrieval in AutoCodeRover               <Details at https://code.djangoproject.com/ticket/32332>

to fast pinpoint error locations and thus produce final patch.
                                                                                                                (WITHOUT SBFL)
                                                                                        I would use the following APIs:
   Plausible / Correct patches. Overfitting is a well-known challenge             Stratum 1:.search_class(Product), search_class(Order), ...
                                                                                  Stratum 2: search_code_in_file("class Product(models.Model):",
in the Automated Program Repair community [12]. A program                                   "tests/queries/models.py")
patch that passes the given test suite is said to be plausible. How-
ever, a plausible patch is deemed as overfitting if it fails to conform to                                         (WITH SBFL)
the developer’s intent. Otherwise, it is deemed as correct. To further                  An external analysis tool identifies the following code as suspicious:
                                                                                  1. Method convert_uuidfield_value in class DatabaseOperations
understand the patch quality of AutoCodeRover and baselines,                      2. Method _do_update in class Model
we manually verify the correctness of task-resolving (i.e. plausible)             3. Method _prepare_related_fields_for_save in class Model
                                                                                  4. Method _resolve_output_field in class Value
patches in SWE-bench lite. Since three repetitions are performed,                 5. Method resolve_related_fields in class ForeignKey
we consider a task to have a correct patch if any of the three repeti-
tions produced a correct patch. A plausible patch is correct if it is                    I would use the following APIs:
                                                                                  1. search_method_in_class (resolve_related_fields, ForeignKey)
semantically equivalent to the developer patch. In this verification              2. search_method_in_class(_prepare_related_fields_for_save, Model)
process, at least two authors of the paper cross-validated each patch,
and any disagreement was resolved with another author. Overall, on
SWE-bench lite, AutoCodeRover has a correctness rate of 65.4%                Figure 9: Issue description and AutoCodeRover’s context
(51 correct/78 plausible). We observed that the vast majority of             retrieval (w. and w.o. SBFL), on django-13964.
AutoCodeRover’s overfitting patches (all but 2 of the overfitting
patches) modify the same methods as the developer patches, but the
code modifications are wrong. This means that even the overfitting           then use the test-suite for patch validation during the patch gener-
patches from AutoCodeRover are useful to the developer, since                ation retry-loop. We denote this setting as ACR-sbfl in Table 2. The
it helps in localization. The main causes of wrong modifications             patch validation is added as follows: when a patch is generated by
are the limits of the LLM’s capability or insufficient context. Apart        the LLM agent, the test-suite is executed on the patched program;
from these, we noticed two other interesting causes of overfitting.          if the patch fails to pass the complete test-suite, AutoCodeRover
One cause is that the issue creator gives a preliminary patch in the         re-invokes the patch generation agent to write a new patch. This
description. This patch can be different from the final developer            validation loop is configured to run three times.
patch, misleading the LLM. The other interesting cause is that the
                                                                                 Results. Table 2 shows that, with the additional information pro-
issue creator mentioned a case that needs to be handled. The LLM
                                                                             vided by SBFL, the number of resolved tasks increased from 57 to 66
only fixes this mentioned case, but the developer fixed other similar
                                                                             (i.e. 19% to 22% resolved rate on SWE-bench lite). Moreover, when
cases as well. The two causes indicate that the issue description,
                                                                             comparing with task instances resolved in AutoCodeRover on
just like test suites, can be an incomplete specification.
                                                                             SWE-bench lite, ACR-sbfl still uniquely resolves 7 task instances
                                                                             that are not resolved in any of the other runs.
6.2    RQ2: Effect of SBFL                                                      Case study. We present a case study on one of the tasks uniquely
Bug reproduction [6, 20] is a well-studied topic in the software en-         resolved by ACR-sbfl. Figure 9 shows the issue description of django-
gineering community. It aims to automatically construct input tests          139645 and how AutoCodeRover attempts to retrieve code context
to reproduce bugs that are described in bug reports. Subsequently,           with and without SBFL. This issue reported a bug when saving
those bug reproduction tests can be used by program analysis tech-           django models to a database. A simplified version of the issue de-
niques to localize the root cause of bugs and generate patches for           scription is shown in the first part of Figure 9, in which important
APR tools [30].                                                              parts are highlighted. In this issue, some “hints” (highlighted in red)
   In this research question, we investigate whether program anal-           mentioned are actually distracting factors for a context retrieval
ysis techniques with reproducible tests can benefit the workflow             agent. For example, the Product and Order classes describe how
of AutoCodeRover, and we use spectrum-based fault localization               the bug can be reproduced, and are not classes that cause the bug.
(SBFL) as an example. Different from RQ1, here we construct a com-           Retrieving code context from these two classes (as shown in Fig-
mon scenario in program repair that AutoCodeRover has access                 ure 9 part 2 “WITHOUT SBFL”) does not yield useful results for
to the complete test-suite of the target task instance. We use the           forming the context and resolving the issue.
developer-written test cases for each task instance (provided in                On the other hand, the SBFL component can provide extra hints
SWE-bench lite) as the test-suite. To understand the effect of SBFL,         for context retrieval agent (as shown in Figure 9 part 3 “WITH
we additionally provide SBFL results (top-5 suspicious methods) to
AutoCodeRover at the beginning of the context retrieval stage,               5 https://code.djangoproject.com/ticket/32332
ISSTA ’24, September 16–20, 2024, Vienna, Austria                                   Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury


                                                                        mentioned in Section 6.1. The fail-to-resolve cases are included in
                                                                        the remaining four categories. In 29.3% of the tasks, AutoCodeRover
                                                                        correctly decided on all patch locations (at the method-level), but
                                                                        did not produce a correct patch (“Wrong patch”). More fine-grained
                                                                        intra-procedural analysis and specification inference techniques
                                                                        can play a significant role in improving these cases, by providing
                                                                        the patch generation agent with more method-level repair guid-
                                                                        ance. In the other three categories, the fault localization could not
                                                                        pinpoint all the locations to be modified. In 20.0% of the tasks, a
                                                                        patch is generated in the correct file, but at wrong methods / classes
                                                                        in the file (“Wrong location in correct file”). In some of these runs,
                                                                        the developer patch modifies multiple methods, but the generated
                                                                        patch did not modify all of them. In the other categories, a patch
                                                                        could not be generated at the correct file - in 18.0% of the tasks a
   Figure 10: Taxonomy of Challenges in SWE-bench lite.
                                                                        patch is generated in wrong files, and in 6.7% of the tasks there is
                                                                        no applicable patch (“Wrong file” and “No patch”). We manually
                                                                        inspected some tasks in these two categories, and observed that
SBFL”). This is because SBFL considers test execution differences,
                                                                        their issue description mentions few methods / classes / files in
which in this case revealed a few more methods in the codebase that
                                                                        the codebase. Instead, some of them contain short examples to re-
are related to the issue. With these newly revealed hints, the agent
                                                                        produce the issue. For these tasks, one possibility is to generate a
decides to invoke APIs to search for the resolve_related_fields
                                                                        comprehensive test-suite based on the issue description, and then
and _prepare_related_fields_for_save methods (the latter
                                                                        use execution information of the test-suite (e.g. SBFL) to reveal
method is actually where the developer chose to fix this bug6 ).
                                                                        suspicious program locations. On the other hand, some other tasks
Moreover, we observe that the agent does not solely rely on the
                                                                        do not contain reproducible examples and only consist of natural
SBFL results to make API invocations. Instead of searching for
                                                                        language descriptions. For these tasks some human involvement
methods ranked as top-1 in the SBFL results, the agent searched for
                                                                        might be helpful. The developers could focus on these tasks.
the 3rd and 5th ranked methods. These methods are more related
to some other hints mentioned in the issue description (highlighted
in yellow), and the LLM agent is able to exploit this correlation       7   Discussion on Experiments and
between the natural language descriptions and the SBFL analysis             Improvements
results. With the correct context collected, AutoCodeRover is then
                                                                        In this section, we discuss our position on the experiment results
able to draft a patch that resolves this issue. This suggests that an
                                                                        and a few possible directions for future improvements.
execution-based analysis can complement the agent workflow by
revealing information not included in the issue description.
                                                                           Position on Experiment Results. Building autonomous large lan-
                                                                        guage model agent systems for software engineering tasks is one of
6.3     RQ3: Challenges on real-life tasks
                                                                        the fastest-growing research fields now. There were more than 17
In this research question, we analyze the task instances in SWE-        attempts from both academia and industries on SWE-bench since
bench lite that AutoCodeRover failed to resolve (based on the           April 2024. We refer the practitioners to the SWE-bench Leader-
result of ACR-all in Table 2, without applying SBFL) and provide        board [16] (refer Figure 11) which maintains the latest research
a taxonomy of the issue characteristics to highlight the practical      effort of various recent agents. The most recent resolve rate on
challenges in achieving fully automated software improvement.           full SWE-bench leaderboard has reached 19.27% by Factory Code
Our taxonomy consists of challenges in the fault localization stage     Droid as of 12th July 2024. In the meantime, AutoCodeRover is
and patch generation stage. Specifically, for each task, we analyze     also rapidly progressing towards better performance, the most re-
the best run in the three repetitions, and classify each of the 300     cent update of AutoCodeRover (18.83% on SWE-bench on 12th
tasks into one of the following:                                        July 2024) can also be found at [2]. However, despite the satisfying
• Success: The generated patch resolves the issue.                      results of AutoCodeRover, it is useful to interpret the results in
• Wrong patch: The generated patch modifies all methods that are        the right spirit. Apart from showing good efficacy with low cost,
  modified in the developer patch. This means the patch content         AutoCodeRover is significant because of the way it tries to gener-
  is wrong but the patch location(s) are correct.                       ate program modifications. Thus, we highlight the importance of
• Wrong location in correct file: The generated patch that modifies     gleaning program specifications to guide the patching process by
  the correct file but wrong location(s) in the file.                   agents as a general guideline for future research.
• Wrong file: The generated patch modifies the wrong file.
• No patch: No patch is generated from the retrieved context.              Issue Reproducer. In Section 4, we described two scenarios that
    Figure 10 shows the distribution of the 300 tasks in SWE-bench      AutoCodeRover can work on, (1) issue description only, (2) aided
lite. AutoCodeRover resolves 26.0% of the issues (“Success”), as        by SBFL when the test suite is available. Although the second sce-
                                                                        nario is not always practical in real-life software development, the
6 https://github.com/django/django/pull/13964/files                     issue description sometimes contains a concrete reproduction script
AutoCodeRover: Autonomous Program Improvement                                                          ISSTA ’24, September 16–20, 2024, Vienna, Austria


                                                                           threat by manually verifying whether the patches are semantically
                                                                           equivalent to developers’ patches among the authors.

                                                                           9   Perspectives
                                                                           AI-based software engineering is currently a topic of study among
                                                                           researchers, innovators, and entrepreneurs. Part of the trigger for
                                                                           this interest has been provided by efforts like GitHub Copilot [1] in
                                                                           the last few years. These efforts show significant promise in the use
                                                                           of Large Language Models (LLMs) to automatically generate code.
                                                                           At the same time, code generated by LLMs may be incorrect [10] or
                                                                           vulnerable [34]. Thus, we need autonomous processes which allow
                                                                           for code improvements, such as bug fixes and feature additions.
Figure 11: Snapshot of full SWE-bench leaderboard on 12th                      In this paper, we suggest a LLM-based solution AutoCodeRover
July 2024                                                                  for autonomous code improvement. The key distinguishing feature
                                                                           of AutoCodeRover is its conscious attempt to inject a software en-
                                                                           gineering outlook by integrating (a) use of program representations
from the user that reports the bug. In the future, it is possible to de-   such as ASTs instead of files, (b) iterative code search by exploiting
sign an LLM agent specifically to generate a bug reproduction test         program structure and (c) use of test-based fault localization when
based on the GitHub issue description. The bug reproduction test           tests can be constructed. AutoCodeRover shows significant effi-
can then be used to validate the correctness of AutoCodeRover’s            cacy in terms of solving real-life GitHub issues. AutoCodeRover
generated patch and possibly enable a regeneration process if a            shows that relying only on the GitHub issue description to guide
patch fails to pass the reproduction test.                                 code search for patches / modifications can be misleading. From
                                                                           the point of view of program repair, the toughest challenge lies
   Semantic Artifacts. During context retrieval, AutoCodeRover             in inferring the intent of the developer or the specification. The
effectively navigates through the codebase by visiting code entities       outlook of AutoCodeRover is that the developer intent is gleaned
such as classes and methods. The idea of utilizing code-specific           from the project structure for automated program modifications.
structure for context retrieval can be taken further by considering            Today, the code LLMs cannot produce safe and secure code which
artifacts from program semantics. For example, from an initial set         can be trusted enough to be integrated into real software projects.
of methods identified in the issue description, a static call graph        There is thus a need to autonomously improve code (both automat-
analysis [36, 37] can be used to collect additional relevant methods       ically generated and manually written), for which LLMs can play a
when testcases are absent. There are also potential in integrating a       role. Future work needs to focus further on the appropriate points
language server [14] for codebase navigation, so that the context          when tools like AutoCodeRover may converse with the human
retrieval agent can perform more code-specific actions such as             programmer. Developers may need to shift to playing different roles
“jump-to-definition” from a method invocation. Finally, one can use        at the same time in future software industry - vetting different con-
forward data dependence analysis [19] from the methods in the              versations with LLM-based tools like AutoCodeRover to enable
issue description to search for other relevant methods.                    a variety of software engineering activities. This would contrast
                                                                           with today’s software industry where a person has specific roles like
    Human Involvement. Currently, AutoCodeRover left all decision-
                                                                           programmer/tester/architect/requirements-engineer. Thus, apart
making processes to its foundation LLM — e.g. deciding context
                                                                           from full-stack engineers, we may see more full-lifecycle software
retrieving locations and whether to terminate the retrieval stage.
                                                                           engineers in the future, who are comfortable working with the entire
However, leaving it to the LLM may not always be enough. Note that
                                                                           lifecycle of (the components of) a software system. Furthermore,
it is common to have multiple rounds of discussion even between
                                                                           the focus of LLM-oriented workflows is on scale today. This focus
the project maintainers before a pull request is created. Hence, a
                                                                           may shift to the engendering of trust if LLM-oriented autonomous
flexible interface and human involvement criteria between human
                                                                           software engineering becomes commonplace. Future software en-
developers and LLM agents are desired.
                                                                           gineers may focus more on greater trust, instead of larger scale.
8   Threats to Validity                                                    DATA AVAILABILITY
Despite the high efficacy AutoCodeRover achieved in SWE-bench,             We share full public access to (1) AutoCodeRover’s implementa-
we report a few potential threats to our approach and experiments          tion, (2) all patches generated during our experiment and conversa-
and discuss how we addressed them. First, LLM is known for its             tion history with LLM, (3) replication scripts for our experiments at
randomness to generate different results in different runs, which          the following website: https://github.com/nus-apr/auto-code-rover.
may threaten the validity of AutoCodeRover’s performance. We
address this by repeating our main evaluation experiment three             Acknowledgments
times and releasing a replication package for practitioners. Second,
                                                                           We thank the anonymous reviewers for their suggestions. This work
we consider a task instance in SWE-bench as resolved if the gener-
                                                                           was partially supported by a Singapore Ministry of Education (MoE)
ated patch passes all the test cases added in the pull request for the
                                                                           Tier 3 grant "Automated Program Repair", MOE-MOET32021-0001.
issue. However, this patch may be overfitting. We addressed this
ISSTA ’24, September 16–20, 2024, Vienna, Austria                                                        Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury


References                                                                                [22] Fabian Keller, Lars Grunske, Simon Heiden, Antonio Filieri, Andre van Hoorn,
 [1] 2022. GitHub Copilot, your AI pair programmer. https://github.com/features/               and David Lo. 2017. A critical evaluation of spectrum-based fault localization
     copilot/                                                                                  techniques on a large-scale software system. In 2017 IEEE International Conference
 [2] 2024. AutoCodeRover, Autonomous Software Engineering. Retrieved July 10,                  on Software Quality, Reliability and Security (QRS). IEEE, 114–125.
     2024 from https://autocoderover.dev/                                                 [23] Anil Koyuncu, Kui Liu, Tegawendé F Bissyandé, Dongsun Kim, Martin Monper-
 [3] Rui Abreu, Peter Zoeteweij, and Arjan J.C. van Gemund. 2007. On the Accuracy              rus, Jacques Klein, and Yves Le Traon. 2019. iFixR: Bug report driven program
     of Spectrum-based Fault Localization. In Testing: Academic and Industrial Confer-         repair. In Proceedings of the 2019 27th ACM joint meeting on european software
     ence Practice and Research Techniques - MUTATION (TAICPART-MUTATION 2007).                engineering conference and symposium on the foundations of software engineering.
     IEEE, IEEE, 89–98. https://doi.org/10.1109/taic.part.2007.13                              314–325.
 [4] Johannes Bader, Andrew Scott, Michael Pradel, and Satish Chandra. 2019. Getafix:     [24] Cognition Labs. 2024. Devin, AI software engineer. Retrieved April 12, 2024
     Learning to fix bugs automatically. Proceedings of the ACM on Programming Lan-            from https://www.cognition-labs.com/introducing-devin
     guages 3, OOPSLA (2019), 1–27.                                                       [25] Yujia Li, David H. Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser,
 [5] Marcel Böhme, Cristian Cadar, and Abhik Roychoudhury. 2021. Fuzzing: Chal-                Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago,
     lenges and Reflections. IEEE Software 38, 3 (2021).                                       Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin,
 [6] Marcel Böhme, Van-Thuan Pham, Manh-Dung Nguyen, and Abhik Roychoud-                       Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov,
     hury. 2017. Directed greybox fuzzing. In Proceedings of the 2017 ACM SIGSAC               James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli,
     conference on computer and communications security. 2329–2344.                            Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. 2022. Competition-
 [7] Cristian Cadar and Koushik Sen. 2013. Symbolic execution for software testing:            Level Code Generation with AlphaCode. Science abs/2203.07814, 6624 (12 2022),
     three decades later. Commun. ACM 56, 2 (2013).                                            1092–1097. https://doi.org/10.48550/arxiv.2203.07814
 [8] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de                  [26] Thibaud Lutellier, Hung Viet Pham, Lawrence Pang, Yitong Li, Moshi Wei, and
     Oliveira Pinto, Jared Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph,              Lin Tan. 2020. CoCoNuT: combining context-aware neural translation models us-
     Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy               ing ensemble for program repair., In ISSTA ’20: 29th ACM SIGSOFT International
     Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder,               Symposium on Software Testing and Analysis, Virtual Event, USA, July 18-22,
     Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens                  2020, Sarfraz Khurshid and Corina S. Pasareanu (Eds.). International Symposium
     Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert,          on Software Testing and Analysis, 101–114.
     Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss,          [27] Alexandru Marginean, Johannes Bader, Satish Chandra, Mark Harman, Yue Jia,
     Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji,         Ke Mao, Alexander Mols, and Andrew Scott. 2019. Sapfix: Automated end-to-
     Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike,            end repair at scale. In 2019 IEEE/ACM 41st International Conference on Software
     Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight,                 Engineering: Software Engineering in Practice (ICSE-SEIP). IEEE, 269–278.
     Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario          [28] Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. 2016. Angelix: scalable
     Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. Evaluat-              multiline program patch synthesis via symbolic analysis., In Proceedings of the
     ing Large Language Models Trained on Code. arXiv.org abs/2107.03374 (7 2021).             38th International Conference on Software Engineering, ICSE 2016, Austin, TX,
     arXiv:2107.03374 https://arxiv.org/abs/2107.03374                                         USA, May 14-22, 2016, Laura K. Dillon, Willem Visser, and Laurie Williams (Eds.).
 [9] Yiu Wai Chow, Luca Di Grazia, and Michael Pradel. 2024. Pyty: Repairing static            International Conference on Software Engineering, 691–701.
     type errors in python. In Proceedings of the IEEE/ACM 46th International Confer-     [29] Manish Motwani and Yuriy Brun. 2023. Better automatic program repair by using
     ence on Software Engineering. 1–13.                                                       bug reports and tests together. In 2023 IEEE/ACM 45th International Conference
[10] Zhiyu Fan, Xiang Gao, Martin Mirchev, Abhik Roychoudhury, and Shin Hwei                   on Software Engineering (ICSE). IEEE, 1225–1237.
     Tan. 2023. Automated Repair of Programs from Large Language Models.. In              [30] Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and Satish Chan-
     45th IEEE/ACM International Conference on Software Engineering, ICSE 2023, Mel-           dra. 2013. SemFix: program repair via semantic analysis., In 35th International
     bourne, Australia, May 14-20, 2023. IEEE, IEEE, 1469–1481. https://doi.org/10.            Conference on Software Engineering, ICSE ’13, San Francisco, CA, USA, May
     1109/icse48619.2023.00128                                                                 18-26, 2013 (San Francisco, CA, USA), David Notkin, Betty H. C. Cheng, and
[11] Michael Fu, Chakkrit Tantithamthavorn, Trung Le, Van Nguyen, and Dinh Phung.              Klaus Pohl (Eds.). International Conference on Software Engineering, 772–781.
     2022. VulRepair: a T5-based automated software vulnerability repair. In Pro-              https://doi.org/10.1109/icse.2013.6606623
     ceedings of the 30th ACM joint european software engineering conference and          [31] Yannic Noller, Ridwan Shariffdeen, Xiang Gao, and Abhik Roychoudhury. 2022.
     symposium on the foundations of software engineering. 935–947.                            Trust Enhancement Issues in Program Repair. In IEEE/ACM 44th International
[12] Xiang Gao, Sergey Mechtaev, and Abhik Roychoudhury. 2019. Crash-avoiding                  Conference on Software Engineering (ICSE).
     program repair. In Proceedings of the 28th ACM SIGSOFT International Symposium       [32] Brayan Stiven Torrres Ovalle. 2023. GitHub Copilot. https://doi.org/10.26507/
     on Software Testing and Analysis. 8–18.                                                   paper.2300
[13] Claire Le Goues, Michael Pradel, and Abhik Roychoudhury. 2019. Automated             [33] Hammond Pearce, Benjamin Tan, Baleegh Ahmad, Ramesh Karri, and Brendan
     program repair. Commun. ACM 62 (11 2019), 56–65. Issue 12.                                Dolan-Gavitt. 2023. Examining zero-shot vulnerability repair with large language
[14] Nadeeshaan Gunasinghe and Nipuna Marcus. 2021. Language Server Protocol and               models. In 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 2339–2356.
     Implementation. Springer.                                                            [34] H Pearce, B Tan, B Ahmad, R Karri, and B Dolan-Gavitt. 2023. Examining zero-
[15] Nan Jiang, Kevin Liu, Thibaud Lutellier, and Lin Tan. 2023. Impact of Code Lan-           shot vulnerability repair with large language models. In IEEE Symposium on
     guage Models on Automated Program Repair., In 45th IEEE/ACM International                 Security and Privacy (SP).
     Conference on Software Engineering, ICSE 2023, Melbourne, Australia, May             [35] Julian Aron Prenner, Hlib Babii, and Romain Robbes. 2022. Can OpenAI’s codex
     14-20, 2023 (Melbourne, Victoria, Australia). International Conference on Software        fix bugs? an evaluation on QuixBugs. In Proceedings of the Third International
     Engineering, 1430–1442. https://doi.org/10.1109/icse48619.2023.00125                      Workshop on Automated Program Repair. 69–75.
[16] Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press,   [36] Barbara G Ryder. 1979. Constructing the call graph of a program. IEEE Transac-
     and Karthik Narasimhan. 2024. Leaderboard results on SWE-bench. Retrieved                 tions on Software Engineering 3 (1979), 216–226.
     April 8, 2024 from https://www.swebench.com/                                         [37] Vitalis Salis, Thodoris Sotiropoulos, Panos Louridas, Diomidis Spinellis, and Dim-
[17] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press,         itris Mitropoulos. 2021. Pycg: Practical call graph generation in python. In 2021
     and Karthik R Narasimhan. 2024. SWE-bench: Can Language Models Resolve                    IEEE/ACM 43rd International Conference on Software Engineering (ICSE). IEEE,
     Real-world Github Issues?. In The Twelfth International Conference on Learning            1646–1657.
     Representations. https://openreview.net/forum?id=VTF8yNQM66                          [38] Edward K. Smith, Earl T. Barr, Claire Le Goues, and Yuriy Brun. 2015. Is the cure
[18] Matthew Jin, Syed Shahriar, Michele Tufano, Xin Shi, Shuai Lu, Neel Sundaresan,           worse than the disease? overfitting in automated program repair., In Proceed-
     and Alexey Svyatkovskiy. 2023. Inferfix: End-to-end program repair with llms.             ings of the 2015 10th Joint Meeting on Foundations of Software Engineering,
     In Proceedings of the 31st ACM Joint European Software Engineering Conference             ESEC/FSE 2015, Bergamo, Italy, August 30 - September 4, 2015, Elisabetta Di
     and Symposium on the Foundations of Software Engineering. 1646–1656.                      Nitto, Mark Harman, and Patrick Heymans (Eds.). ESEC/SIGSOFT FSE, 532–543.
[19] Wuxia Jin et al. 2024. PyAnalyzer: An Effective and Practical Approach for De-            http://people.cs.umass.edu/%7Ebrun/pubs/pubs/Smith15fse.pdf
     pendency Extraction from Python Code. In International Conference on Software        [39] Shin Hwei Tan, Ziqiang Li, and Lu Yan. 2024. CrossFix: Resolution of GitHub is-
     Engineering (ICSE).                                                                       sues via similar bugs recommendation. Journal of Software: Evolution and Process
[20] Wei Jin and Alessandro Orso. 2012. BugRedux: Reproducing field failures for               36, 4 (2024), e2554.
     in-house debugging. In 2012 34th International Conference on Software Engineering    [40] The Cognition Team. 2024. SWE-bench technical report (Devin). Retrieved April
     (ICSE). 474–484. https://doi.org/10.1109/ICSE.2012.6227168                                12, 2024 from https://www.cognition-labs.com/post/swe-bench-technical-report
[21] James A Jones, Mary Jean Harrold, and John Stasko. 2002. Visualization of test       [41] Weishi Wang, Yue Wang, Shafiq Joty, and Steven CH Hoi. 2023. Rap-gen: Retrieval-
     information to assist fault localization. In Proceedings of the 24th international        augmented patch generation with codet5 for automatic program repair. In Pro-
     conference on Software engineering. 467–477.                                              ceedings of the 31st ACM Joint European Software Engineering Conference and
                                                                                               Symposium on the Foundations of Software Engineering. 146–158.
AutoCodeRover: Autonomous Program Improvement                                                                             ISSTA ’24, September 16–20, 2024, Vienna, Austria


[42] Westley Weimer, ThanhVu Nguyen, Claire Le Goues, and Stephanie Forrest. 2009.       [46] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023. Automated pro-
     Automatically finding patches using genetic programming., In 31st International          gram repair in the era of large pre-trained language models. In 2023 IEEE/ACM
     Conference on Software Engineering, ICSE 2009, May 16-24, 2009, Vancouver,               45th International Conference on Software Engineering (ICSE). IEEE, 1482–1494.
     Canada, Proceedings. 2009 IEEE 31st International Conference on Software Engi-      [47] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao,
     neering, 364–374. https://doi.org/10.1109/icse.2009.5070536                              Karthik Narasimhan, and Ofir Press. 2024. SWE-agent: Agent-Computer In-
[43] David Williams, James Callan, Serkan Kirbas, Sergey Mechtaev, Justyna Petke,             terfaces Enable Automated Software Engineering. arXiv:2405.15793 [cs.SE]
     Thomas Prideaux-Ghee, and Federica Sarro. 2023. User-Centric Deployment of          [48] Qihao Zhu, Zeyu Sun, Yuan-an Xiao, Wenjie Zhang, Kang Yuan, Yingfei Xiong,
     Automated Program Repair at Bloomberg. arXiv preprint arXiv:2311.10516 (2023).           and Lu Zhang. 2021. A syntax-guided edit decoder for neural program repair.,
[44] WE Wong, R Gao, Y Li, R Abreu, and F Wotawa. 2016. A survey on software fault            In ESEC/FSE ’21: 29th ACM Joint European Software Engineering Conference
     localization. IEEE Transactions on Software Engineering (2016), 707–740. Issue 8.        and Symposium on the Foundations of Software Engineering, Athens, Greece,
[45] W Eric Wong, Ruizhi Gao, Yihao Li, Rui Abreu, and Franz Wotawa. 2016. A                  August 23-28, 2021, Diomidis Spinellis, Georgios Gousios, Marsha Chechik, and
     survey on software fault localization. IEEE Transactions on Software Engineering         Massimiliano Di Penta (Eds.). ESEC/SIGSOFT FSE, 341–353. https://arxiv.org/
     42, 8 (2016), 707–740.                                                                   pdf/2106.08253



Received 2024-04-12; accepted 2024-07-03
