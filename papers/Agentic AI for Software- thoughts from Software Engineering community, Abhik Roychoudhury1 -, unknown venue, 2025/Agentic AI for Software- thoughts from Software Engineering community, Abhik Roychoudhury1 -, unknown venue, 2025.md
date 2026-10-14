                                               Agentic AI for Software: thoughts from Software Engineering community

                                                                                                  Abhik Roychoudhury1 *
                                                                                             1
                                                                                                 National University of Singapore
                                                                                                     abhik@nus.edu.sg




                                                                     Abstract                                                       Historical Retrospective
arXiv:2508.17343v4 [cs.SE] 22 Sep 2025




                                           AI agents have recently shown significant promise in soft-              Since the 1970’s when programming in modern existing pro-
                                           ware engineering. Much public attention has been transfixed             gramming languages firmly took root - the focus has been
                                           on the topic of code generation from Large Language Mod-                on programming in the large. The start of this period can be
                                           els (LLMs) via a prompt. However, software engineering is               traced back to around fifty years ago - when the first Hello
                                           much more than programming, and AI agents go far beyond                 World program was written by Brian Kerninghan in 1972-3
                                           instructions given by a prompt.                                         in the B programming language, which is the predecessor of
                                           At the code level, common software tasks include code gen-              C. Since the writing of the first ”Hello World” program and
                                           eration, testing, and program repair. Design level software             the initial seminal innovations, there have been only two re-
                                           tasks may include architecture exploration, requirements un-            ally major shifts in the software industry affecting both the
                                           derstanding, and requirements enforcement at the code level.            technology as well as the business of software.
                                           Each of these software tasks involves micro-decisions which
                                           can be taken autonomously by an AI agent, aided by pro-                    The first shift came 25 years after the ”Hello World” pro-
                                           gram analysis tools. This creates the vision of an AI software          gram, in the late nineties. Subsequent to the birth of the in-
                                           engineer, where the AI agent can be seen as a member of a               ternet - the software delivery model as a service took root.
                                           development team.                                                       This led to many Software-as-a-Service (SaaS) offerings in
                                           Conceptually, the key to successfully developing trustworthy            vertical domains such as customer relationship management
                                           agentic AI-based software workflows will be to resolve the              (SalesForce being an example company in the domain). The
                                           core difficulty in software engineering - the deciphering and           movement from in-house software development to cloud-
                                           clarification of developer intent. Specification inference, or          based hosting of software also led to movement of storage
                                           deciphering the intent, thus lies at the heart of many software         or documents to the cloud - allowing for conveniences such
                                           tasks, including software maintenance and program repair. A             as collaboratively working on documents.
                                           successful deployment of agentic technology into software                  In 2025, we are now at the second major shift which af-
                                           engineering would involve making conceptual progress in
                                                                                                                   fects both the software technology and business- the arrival
                                           such intent inference via agents. We discuss, to some length,
                                           the AutoCodeRover agent which embodies such intent infer-               of agentic AI. With the use of agentic AI in software - the
                                           ence. The agent has been integrated into the SonarQube static           change is beyond the hosting of the software - instead, the
                                           analysis tool.                                                          engineering of the software itself is automated to a large
                                                                                                                   degree. Since there is greater automation - this eases the
                                           Trusting the AI agent becomes a key aspect, as software en-
                                           gineering becomes more automated. Higher automation also                writing of code fragments capturing different functionality.
                                           leads to higher volume of code being automatically gener-               However, the correctness of the code and the overall trust in
                                           ated, and then integrated into code-bases. Thus to deal with            the agent output becomes a key concern that needs address-
                                           this explosion, an emerging direction is AI-based verification          ing. Thus, perhaps for the first time since the writing of the
                                           and validation (V & V) of AI generated code. We posit that              ”Hello World” program - we face the central issue of pro-
                                           agentic software workflows in future will include such AI-              gramming with trust, instead of programming in the large.
                                           based V&V.                                                                 Figure 1 shows the timeline of some key developments
                                                                                                                   in the software industry in the past fifty years- highlighting
                                         Code — N.A.                                                               the two major developments: SaaS and agentic AI. It also
                                         Datasets — SWE-bench                                                      shows the contrast between ”programming in the large” and
                                                                                                                   ”programming with trust”.
                                         Extended version — N.A.
                                                                                                                      In the rest of the article we will navigate this tension be-
                                                                                                                   tween scale and trust, and also transcend the issues in pro-
                                            * Full-time involvement as Professor at NUS, while being Se-           gramming to the core concerns in software engineering. We
                                         nior Advisor at SonarSource SA.                                           will also discuss how this tension betwen scale and trust is
                                         Copyright ©2025, All rights reserved.                                     evolving as agentic AI solutions for software develop.
                                                   Five decades since “Hello World”




                    Figure 1: Arrival of Agentic AI in Software - more than fifty years after ”Hello World”.


             Resolving Software Issues
GitHub Co-pilot (Friedman 2022) is an early approach to
AI-based automation in software engineering. It attempts to
provide code completions to complete code while the human
programmer is typing in an Integrated Development Envi-
ronment. Instead of a human programmer going to an online
community such as Stackoverflow to get help in program-
ming, it brings the knowledge from such online communities
to the programmer as part of the development environment.                                                AGENT
AI agents for coding go beyond the Co-pilot approach since
the agents can exercise autonomy to make decisions and act                     Figure 2: Role of analysis in issue resolution.
somewhat like a (human) software engineer.
    A broad structure of Large Language Model (LLM)
agents for software has emerged in the past 1-2 years. An             gested. Availability of open datasets containing open chal-
agent is autonomous and makes (informed) decisions on its             lenges have spurred the growth of agents targeting auto-
own. It may be informed by invoking various external tools.           mated issue resolution in software. A schematic of an LLM
In the case of LLM agents for software - the most effective           agent for conducting software issue resolution is shown in
solution is found if the agents work on program represen-             Figure 2. This schematic is given at a high level showing
tations. By making the agents interpret program representa-           how an agent can invoke program analysis tools to work on
tions and make micro-decisions about software related tasks,          program representations. At a more detailed level, an agent
we can have the agent conduct program analysis to make de-            will use its autonomy to analyze different parts of the code-
cisions. The program analysis can either be invoked as an             base on-the-fly in order to accomplish a software task.
external tool, or it can be embedded in the agent’s actions as           Since the SWE-bench dataset suggested the resolution of
it interprets and navigates the program representation.               software issues as a challenge, several AI-based agent ap-
    One of the key pivots in the growth of LLM agents for             proaches have emerged. Devin (Wu 2024) from Cognition
software has been the interest around automated issue res-            Labs was one of the first approaches. It suggests the use
olution. A software issue is an unit of work that a (human)           of external tools to aid the agent, thereby suggesting a first
software engineer often needs to deal with. Such an issue             step towards AI software engineer. Devin invokes external
is a report given to the software engineer - requesting some          tools such as a shell where any command can be input.
improvement of the software project. The improvement can              Thus, the agent can autonomously work like a software engi-
focus on a bug fix, a feature addition or even a desired              neer - inspecting files in the project and focusing on certain
efficiency improvement in a core library of the software              parts of the program to resolve software issues. The SWE
project. In recent times, open datasets of software issues            agent (Yang et al. 2024) provides an agentic approach that
such as SWE-bench (Jimenez et al. 2024) have been sug-                is thematically similar to Devin. It suggests the setting up of
                                Figure 3: Issue Resolution by Intent Inference in AutoCodeRover.


agent-computer interfaces for the agent to interact with ex-       Coming back: Learning from those lessons Resolving
ternal tools. Openhands (Wang et al. 2025) is an open-source       software issues includes the problem of automated program
approach towards AI agents for code. Like a human devel-           repair, but is a more general problem. Instead of given tests,
oper it can invoke a shell, web-browser or consult Stackover-      the desired behavior is given as a natural language issue. Un-
flow to modify code.                                               derstanding the intended behavior of a software project and
                                                                   how it deviates from the intended behavior can help us re-
                                                                   solve the software issue. In an agentic AI approach to build-
             Intent Inference from Code                            ing an AI software engineer - it is thus not sufficient to in-
All of the aforementioned approaches - Devin, SWE-agent            voke external tools such as a shell or web-browser. Instead
and OpenHands - attempt to create an agentic software engi-        of the agent working on code as text, it needs to work on pro-
neer by endowing it with the tool capabilities of the human        gram representations and needs to employ program analysis
software engineer. However, the human software engineer            for intent inference.
is also capable of understanding and reasoning about pro-          AutoCodeRover and followup AutoCodeRover (Zhang
gram code semantics during the software engineering pro-           et al. 2024) gives a different agentic AI approach by in-
cess. The process of fixing bugs or adding features in a com-      volving program analysis. Given a software issue, its core
plex code-base usually is not as simple as invoking a shell        intuition is to extract specifications (of intended behavior)
or a web-browser or looking up Stackoverflow. The human            from the program structure. This is achieved via code search.
software engineer usually conducts an implicit intent infer-       Starting from the code elements (classes, methods, APIs)
ence - about what is the intended behavior of the software -       mentioned in the issue - it progressively searches other
and whether the current code-base is satisfying the intended       code elements to perform fault localization - finding where
behavior. This understanding of the intended behavior (and         the code changes are needed. This is then followed by a
any deviation from it by the current code-base) allows the         patch generation stage which considers the knowledge/spec-
human software engineer to make code changes, thereby re-          ifications gained from fault localization. A follow-up work
solving software issues.                                           SpecRover (Ruan, Zhang, and Roychoudhury 2025) makes
                                                                   the implicit intent inference in AutoCodeRover more ex-
Digression: Lessons from Program Repair Before the                 plicit by inferring the intended behavior of each of the func-
arrival of AI agents, the software engineering community           tions (or units off code) identified by fault localization. Fig-
has studied the problem of automated program repair (Le            ure 3 shows a simple example of issue resolution via intent
Goues, Pradel, and Roychoudhury 2019). In the problem of           inference. The issue being resolved is shown at the top. The
automated program repair, the correctness criterion is given       code-search starts from the ModelChoiceField class
as a set of tests. The goal of automated program repair is to      which is mentioned in the natural language issue. It then
automatically modify a given buggy program, so that it can         progresses by looking up the signature of this class - and
pass the given set of tests. However, this risks the generated     then further looking into the implementation of the meth-
patch from overfitting the given test data, it can only pass the   dods. The AutoCodeRover agent thus iteratively refines its
given tests, but mostly fail tests outside the test-suite. Try-    lower-level understanding of the intended program behavior
ing to generalize the given tests to infer intended behavior       from the program structure such as classes / methods.
is found to be a solution to combat the overfitting problem.
This lesson forms the heart of semantic program repair ap-         Use-cases and explainability What is the benefit of the
proaches, which use symbolic program analysis (specifically        agent working on program representations? The main bene-
symbolic execution) for intent inference.                          fit is the inference of intended program behavior by the agent
                                                                     Last but not the least, agentic AI can be put to use for for-
                                                                  mal verification of code (Cadar and Roychoudhury 2025).
                                                                  Just like agents like AutoCodeRover can interpret program
                                                                  representations and analyze them, we can devise AI agents
                                                                  which can interpret formal proof representations, analyze
                                                                  them, and communicate with a theorem prover via an iter-
                                                                  ative refinement loop to ”improve” the proof. This will also
                                                                  contrast with approaches like Alphaproof1 which help prove
                                                                  general mathematical theorems. Instead, a program verifi-
   Figure 4: Agentic AI for Policy Enforcement in Code.           cation agent can again leverage the program structure like
                                                                  classes / methods to structure the proof and its intermediate
                                                                  lemmas. This remains an attractive future direction.
which can be used to provide explanations of the agent’s ac-
tions. It enhances trust in the coding agent, and allows one                               References
to employ agents in more critical scenarios (that demand
greater trust) than vibe-coding. We can also observe this         Cadar, C.; and Roychoudhury, A. 2025. AI for Program Ver-
from the current real-life usage of AutoCodeRover, which          ification. In AI4X conference. https://openreview.net/pdf?
has now been integrated into the widely used SonarQube            id=5t9HFssPla.
tool (Gaudin and Mallet 2010). SonarQube is used by enter-        Friedman, N. 2022. Introducing GitHub Copilot - your AI
prises for code quality and security - it provides inspection     pair programmer. The GitHub Blog.
of bugs, code smells and vulnerabilities. Such bug reports        Gaudin, O.; and Mallet, F. 2010. Sonar. Methods and
generated by SonarQube can be treated as issues which are         tools, 18(1): 40—46. https://www.methodsandtools.com/
then automatically fixed by AutoCodeRover. This shows the         PDF/mt201001.pdf.
promise of agentic AI in providing support for critical code.     Guo, J.; Wang, C.; Xu, X.; Su, Z.; and Zhang, X. 2025. Re-
                                                                  poAudit: An Autonomous LLM-Agent for Repository-Level
             Verification and Validation                          Code Auditing. In Forty-Second International Conference
Issue resolution forms the core of program improvement and        on Machine Learning (ICML).
maintenance of a software project. While issue resolution         Jimenez, C. E.; et al. 2024. SWE-bench: Can Language
and prompt based code generation have captured significant        Models Resolve Real-World GitHub Issues? In Inter-
attention - the opportunities of using agentic AI for code are    national Conference on Learning Representations (ICLR).
by no means restricted to these areas. With the growth of         https://www.swebench.com/.
automation in software development, there will arguably be        Le Goues, C.; Pradel, M.; and Roychoudhury, A. 2019. Au-
an explosion of AI-generated code. This will exacerbate the       tomated Program Repair. Communications of the ACM, 62.
issue of verification and validation (V & V) of the generated
                                                                  Pearce, H.; et al. 2025. Asleep at the keyboard? assessing
code. Furthermore, as the generated code gets integrated to
                                                                  the security of github copilot’s code contributions. Commu-
code-bases, the interplay of legacy human written code and
                                                                  nications of the ACM, 68(2).
the generated code - will lead to subtle errors and vulner-
abilities. Even if the agentic AI that produces code (frag-       Ruan, H.; Zhang, Y.; and Roychoudhury, A. 2025.
ments) is trustworthy - the integration of AI generated code      SpecRover: Code Intent Extraction via LLMs. In 47th In-
can create new trust issues in software projects further down     ternational Conference on Software Engineering (ICSE).
the line. There is a long history of prominent vulnerabilities    Wang, X.; et al. 2025. OpenHands: An Open Platform for
caused by (human written) software. The latest prominent          AI Software Developers as Generalist Agents. In The Thir-
example is perhaps CrowdStrike outage in 2024, where the          teenth International Conference on Learning Representa-
security system itself had a bug that caused worldwide out-       tions.
ages. At the same time, AI generated code from prompts            Wu, S. 2024. Introducing Devin, the first AI software en-
have been reported to have many vulnerabilities (see e.g.,        gineer. Cognition Labs blogpost. https://www.cognition.ai/
(Pearce et al. 2025)). There may be a lingering ”trust deficit”   blog/introducing-devin.
in AI generated code.                                             Yang, J.; et al. 2024. SWE-agent: Agent-computer Interfaces
   Looking forward, one prominent direction thus could be         Enable Automated Software Engineering. Thirty-Eighth An-
to put agentic AI itself to use in combating the trust deficit    nual Conference on Neural Information Processing Systems
from AI generated code ! Thus, given a key critical high          (NeurIPS).
level natural language requirement - agentic AI may help
clarify the requirement by understanding its intent, as well      Zhang, Y.; Ruan, H.; Fan, Z.; and Roychoudhury, A. 2024.
as understanding how it is implemented at a low level in the      AutoCodeRover: Autonomous Program Improvement. In
code-base. This may lead to capabilities of security audits       ACM International Symposium on Software Testing and
which have been recently studied (Guo et al. 2025). In fact, it   Analysis (ISSTA).
can go beyond audits by flagging violations of the policy and
fixing these violations via code changes albeit by an issue          1
                                                                       https://deepmind.google/discover/blog/ai-solves-imo-
resolution agent in the back-end.                                 problems-at-silver-medal-level/
