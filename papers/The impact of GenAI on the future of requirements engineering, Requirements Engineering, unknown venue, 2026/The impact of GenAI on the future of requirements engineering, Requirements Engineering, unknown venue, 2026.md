                                                     The Impact of GenAI on the Future of
                                                          Requirements Engineering

                                                              Travis Breaux1* and Anmol Singhal1
                                                1*
                                                 Software and Societal Systems Department, Carnegie Mellon
                                              University, 5000 Forbes Avenue, Pittsburgh, 15213, Pennsylvania,
                                                                       United States.
arXiv:2609.05667v1 [cs.SE] 4 Sep 2026




                                                     *Corresponding author(s). E-mail(s): breaux@cmu.edu;
                                                         Contributing authors: anmolsinghal@cmu.edu;


                                                                                  Abstract
                                             Recent advances in artificial intelligence (AI), particularly large language mod-
                                             els (LLMs), are transforming how we design and build systems by increasing
                                             access to domain knowledge and by providing automation support to software
                                             engineering (SE). As implementation becomes less expensive through generalist
                                             SE agents, engineering effort shifts away from writing correct code and toward
                                             expressing, curating, verifying, and evaluating requirements. In this paper, we
                                             survey the state of the art in AI for requirements engineering (RE) research lead-
                                             ing up to the transformation, before reviewing advances in LLMs. We survey
                                             two subsequent research areas: prompt programming, which treats LLM instruc-
                                             tions as a program in SE vernacular, and generalist SE agents, which combine
                                             multiple LLM advances to yield semi-autonomous processes that complete SE
                                             tasks. Finally, we explore the future of requirements engineering along two axes:
                                             matters changing how we interact with requirements through the SE process,
                                             and matters changing how requirements are experienced by software developers
                                             and stakeholders more broadly, including end-users. This article aims to inform
                                             how RE researchers can navigate this transformation in the selection of future
                                             research priorities.

                                             Keywords: requirements, artificial intelligence, agents, automation




                                        1 Introduction
                                        Requirements have long been a key focus of software engineering (SE). In 1970, Win-
                                        ston Royce argued for iterative system design because the so-called water-fall model
                                        was broken: as he described the problem, the “testing phase” was the first moment in
                                        software construction wherein requirements were experienced as opposed to being ana-
                                        lyzed [151], revealing gaps in analysis that lead to discovering imperfect specifications.
                                        In the late 1980s, Barry Boehm argued for the spiral model to gatekeep develop-
                                        ment using risk analysis, prototyping, simulation, modeling, and benchmarking – all


                                                                                       1
hallmarks of rigorous requirements verification and validation practices [19]. Later in
the early 1990s, a new vision emerged that foresaw the automation of requirements
engineering (RE) tasks through artificial intelligence (AI) built on various forms of
symbolic [148, 150] and statistical reasoning [152]. Yet, with the rapid and widespread
adoption of the Internet in the late 1990s, it was Agile methodology that pushed
back on plan-driven software development, minimizing requirements to user stories
and relying on the expertise of developers to supplant the need for requirements anal-
ysis and documentation in a rapidly growing market of e-commerce and web-based
systems [20].
     The world today is transformed by large language models (LLMs) that underpin
generalist SE agents: while surprisingly unexpected, this future was foretold, but it is
still arriving unevenly. This article aims to answer the question “What is the state of
the art in AI for Requirements Engineering?” at a time when that future is rapidly
evolving. In a 2025 survey of 1,006 executives, 60% responded that, in anticipation
of AI automation, they have made headcount reductions, including 21% who have
made large reductions [38]. Importantly, this evidence is anticipatory: the source itself
argues that layoffs are driven by AI’s perceived potential rather than its demonstrated
performance. Meanwhile, LLM manufacturers, including Anthropic, Google, and Ope-
nAI, are prioritizing SE use cases with new tools to generate code. In one–possibly
outdated–2026 study of 4,867 developers, the code generation assistant GitHub Copi-
lot accounted for a 26% increase in task completion [34]. Some job losses represent
companies shifting their capital from human developers to invest in AI infrastructure
and AI cloud services [134]. Although these economic developments are early indus-
try signals described in trade press and analyst reports, they nevertheless describe a
plausible future direction: a world with fewer software developers orchestrating gener-
alist SE agents [107]. In this world, developers rely more on how well they can express
requirements, curate constraints from a brownfield software development ecosystem,
and evaluate agent-produced artifacts than on their ability to write correct code.
Therefore, in this paper, we argue that as implementation becomes cheaper through
agents, RE shifts to operational specifications, context curation, verification, and eval-
uation. In this regard, we see the pendulum swinging back to plan-driven development,
not because risk is any greater than it was in the 1980s, but because implementa-
tion is becoming far less expensive and automation is reducing the software engineer’s
visibility into code.
     To this end, we address this shifting landscape in three ways: (1) we briefly review
the history of AI in RE, describing where RE researchers have primarily focused and
how AI has supported that focus; (2) we review the state-of-the-art and limitations
in rapidly advancing generative AI, specifically around LLMs, prompt programming,
and generalist SE agents; and finally (3) we forecast how RE practice may change in
an AI-driven setting where requirements increasingly instruct software agents rather
than merely guiding the work of human implementers. This article is cross-cutting by
reviewing how RE researchers have sought to advance the state-of-the-art in AI for RE,
broadly, while situating the future of RE practice in terms of the recent disruptions
caused by GenAI and LLMs, in particular. We believe that RE researchers can build
on this evolving ecosystem, whether they use AI, GenAI or LLMs in any capacity in
their research and methodology.

2 History of AI for Requirements Engineering
Requirements engineering (RE) is a broad field covering diverse concerns across a
variety of systems types [139], including information-processing and cyber-physical


                                            2
Table 1 Working taxonomy of recent AI-supported requirements engineering research.


 RE Tasks                Representative Works
 Elicitation             AI-driven interviews [83, 92], script generation [170], follow-up
                         question recommendations [161], inquiry planning [179], and gen-
                         erated feature ideas [184, 185].
 Extraction              Requirements extraction and classification from authoritative doc-
                         uments [1, 7, 13, 37, 78], app reviews [42, 68, 121, 129, 166], issue
                         trackers [181], and online communities [74, 98].
 Generation              Domain models [22, 154], tests [8], security requirements [93, 99],
                         traces [37, 69], goals [132, 160], user stories [131], formal specifica-
                         tions [122], and requirements from design guidance [40].
 Analysis                Ambiguity detection and resolution [46–48, 70, 85], incomplete-
                         ness and consistency checking [6, 10, 17, 112], requirements change
                         detection [2], violation and incompatibility detection [115], conflict
                         detection [53], hallucination reduction [189], and satisfaction check-
                         ing [155].
 Traceability            Trace recovery [59], requirements-smell analysis [178], trace-
                         link explanations [106], and multi-channel requirements manage-
                         ment [172].
 Pipelines               Operational anomaly detection from extracted requirements [4],
                         privacy-risk assessment from user scenarios [72], requirements per-
                         turbation and feature tracing [67], and test-dataset completeness
                         evaluation from refined specifications [12].



systems. In Table 1, RE tasks are broadly grouped into elicitation, extraction, speci-
fication, analysis, management, validation and verification, whereas AI-supported RE
research has primarily covered elicitation, extraction and analysis. We distinguish
between AI-assisted RE, wherein AI is used to aid a human in the completion of an
RE task, and AI-driven RE, where the task is entirely and wholly completed by AI,
even if the task was initiated by a human.
    To characterize recent AI for RE research, we reviewed papers published since
2020 in prominent SE and RE journals and conference proceedings, including the
IEEE Transactions on Software Engineering, ACM Transactions on Software Engi-
neering Methodology, and the Requirements Engineering Journal, in addition to the
ACM/IEEE International Conference on Software Engineering, ACM Foundations of
Software Engineering, IEEE International Requirements Engineering Conference, and
Automated Software Engineering Conference. This review is not systematic nor is it
comprehensive. We now report our observations recent work in AI for RE.
    Elicitation. Advances in LLMs have led to a surge of recent research in
requirements elicitation. In AI-driven interviews, an evaluation of agents conduct-
ing interviews with virtual agent stakeholders found that AI makes similar mistakes
as human interviewers [92]. To support human interviewers, emerging AI-assistance
aims to score interview script quality [170] and generate interview follow-up questions
from real-time transcript histories [161]. Emerging techniques exist to hierarchically
organize and prune the inquiry space to support prioritizing questions in AI-driven
interviews [83] and to generate requirements from stakeholder conversations with
scores for correctness, completeness and relevance [179]. Analysis comparing app-store
and LLM-generated features finds that LLMs can produce useful sub-feature inspira-
tion for novel app scopes [184]. Finally, generative image models have been used to
assist app users in expressing UI improvement suggestions [185]. Across this work, we


                                               3
observe a shift from passively capturing stakeholder statements toward active engage-
ment via question generation and dialogue management. An open and continuing
challenge is that elicitation quality still depends on surfacing tacit knowledge, that
communication and human behavior underlies the effective exchange of information,
and that dynamic, reactive evaluation settings are difficult to replicate.
    Requirements Extraction and Classification. Research to extract require-
ments from authoritative sources includes extracting requirements and associated
fragments from contracts [78], laws [1], requirements documents [13], specifica-
tions [7, 37], process models [90] and GitHub issues [181], as well as from mobile
app reviews [42, 68, 121, 129, 166], sub-reddits [74, 98], twitter [42] and video-
based social media [163]. Related work includes emotion classification of app reviews
for more enhanced feature planning [126] and user story quality assessment [124].
In addition, classification may include assigning requirements to the right develop-
ment teams [13, 143] and deciding which features to delete [129]. Prior work also
involves training small language models to improve the extraction and classification
of non-functional requirements [114, 147]. In addition, methods to promote fairness-
focused RE by extracting fairness requirements from context have been proposed [55].
Three RE tasks, including classification, defect detection and conflict detection, have
been reformulated as natural language inference tasks — a format popular in nat-
ural language processing for which AI performance has improved considerably [52].
This research shows increasing breadth across artifact types and data sources, while
extracted requirements exist in isolation, at best weakly connected to stakeholder
intent, software project context, and downstream developer decisions.
    Generating Requirements Artifacts. Research has used AI to generate
requirements specifications and other artifacts, including traces, which can then be
used for analysis. In most instances, the generated artifact is the research end and
objective with the downstream task unstudied. This includes generating domain mod-
els from classroom assignments [154] and from user stories [22], generating test cases
from requirements [8], security requirements on demand [93] and from verification
standards [99], trace links from requirements and code [37, 69], context-sensitive user
stories from diverse specifications [131], safety goals from a malfunction catalog and
scenarios [132], goal models from interview transcripts [160], formal specifications from
natural-language requirements [122], and requirements from design guidelines and
designer question-answering [40]. Unlike the extractive research, wherein extracted
artifacts maintain strong lexical and semantic coherence with the source data, gener-
ative research relies on synthesis and translation to yield greater interpretation and
conversion between concepts present in the source data and those emerging in the tar-
get artifacts. For example, while user stories provide evidence of user actions and goals,
scenarios that one could generate from such stories can include additional assumptions
(e.g., about the kinds of data and data inter-dependencies that must exist to support
those actions), which are missing or not explicitly stated in the original stories.
    Disambiguation, Inconsistency and Completeness. Requirements analy-
sis leads to improving requirements and specifications by identifying, removing,
and augmenting defects in the form of ambiguities, inconsistencies and omissions.
Research has used AI to identify ambiguity in feature requests [85], financial speci-
fications [177] and system policies [70], identify missing links in issue trackers [112],
changes in requirements found in laws [2] and to detect requirements violations and
incompatibilities [115]. AI has been used to detect and interpret anaphoric ambi-
guities [46]. To resolve ambiguity, external, supplemental domain knowledge can be
introduced [47, 48]. Neuro-symbolic methods showcase how to combine language mod-
els with SMT-based satisfiability reasoning to detect conflicting requirements [53].


                                            4
Where ambiguity and completeness refer to what is missing, hallucinations in language
model usage refer to what is inaccurate and inconsistent. Use-case, entity-relationship
and create, read, update, and delete (CRUD) models can be used to reduce halluci-
nations in LLM-based requirement auto-completion [189]. More recently, researchers
have started to assess the downstream impact of clarifying ambiguous requirements on
code generation [127, 171]. In addition, research has used AI to translate natural lan-
guage requirements into models for consistency and completeness checking [6, 17], to
check completeness of data processing agreements [10] and to verify whether natural
language specifications satisfy requirements [155].
    Traceability and Requirements Management. A significant body of work
focuses on automatically recovering trace links among requirements, code, documen-
tation and user feedback. This includes using retrieval-augmented generation for
generic traceability link recovery and improves code-related traceability tasks [59].
Requirements smells have a measurable effect on LLM-based traceability decisions,
suggesting that prompt quality and requirements quality can interact in automated
trace recovery [178]. Other work generates and visualizes trace-link explanations to
help non-experts understand why artifacts are related [106]. A requirements ecosystem
study links forum posts, issue tracker entries and FAQs, showing how deep learning
can support requirements management across user-feedback channels [172]. Traceabil-
ity is continuing to provide mechanism for retrieval and explanation across iterative
development of heterogeneous artifacts, while challenges persist in how to establish
and maintain trusted links, particularly as software engineering becomes increasingly
generative.
    Integrated Analysis Pipelines. While most RE research reviewed above has
studied narrowly-scoped RE tasks, a few projects have sought to create pipelines span-
ning multiple RE task categories. For example, aviation requirements were extracted
from forum posts and product documentation and used to detect anomalies in real-
time flight operations [4]. In other work, users author scenarios about their use of
software, which were next analyzed by AI to identify privacy sensitive data types that
users then scored for privacy risk [72]. Existing requirements were perturbed to iden-
tify novel variations, which were then traced to existing features and studied through
software development team reflections [67]. Operational design domain attributes,
such as road and lighting conditions for autonomous vehicle testing, were refined into
specifications by AI, which are then used to evaluate test dataset completeness [12].
Whereas narrowly scoped tasks are amenable to ground-truth evaluation with a sin-
gle dataset, pipeline integration must contend with the reality of cascading errors, in
which imperfect artifacts or data identified by AI are used as input to a downstream
task, which is then evaluated separately.

3 Advances in Language Models
Since the introduction of the third generation Generative Pre-Trained Transformer
(GPT-3), followed by the public inflection point around ChatGPT and GPT-3.5, large
language models (LLMs) have undergone significant advances impacting nearly every
industry in modern civilization. Many LLMs are instruction-tuned and aligned, which
consists of fine-tuning and reinforcement learning to follow human instructions [187]
and maximize helpfulness, honesty and harmlessness [9]. Early work on FLAN-style
instruction tuning found substantial improvements in zero-shot task performance [109].
Few-shot chain-of-thought (CoT) prompting raises awareness that models can improve




                                          5
on reasoning tasks when examples include intermediate reasoning steps [186]; zero-
shot CoT, in which users prompt an LLM to “Let’s think step by step,” was found to
improve performance accuracy on math problem tasks by 30-50% [91].
    Today, frontier language models (Claude, Gemini and GPT) include “native” mul-
timodal models trained on text, images and code, and large reasoning models (LRMs)
trained to generate long chain-of-thought. Although the exact sizes and training costs
of leading closed models are not generally disclosed, frontier models are widely under-
stood to require large-scale training runs involving many GPUs and substantial capital
expenditure. Through model distillation, in which a large model is used to train a
small model, a variety of “small” language models averaging in size from 1B to 12B
parameters exist, which can be further fine-tuned on single-GPU workstations. Finally,
modern models can make use of a mixture of experts (MoE), in which model layers are
partitioned into multiple “experts” and a routing gate selects a subset of experts for
each input [76, 84]. This allows the experts to specialize through training on smaller
parts of a problem, which reduces training and inference costs since only a subset of
the entire network is active at any one time.
    Several observations emerge over the state-of-the-art that affect how recent
advances in AI and LLMs in particular can impact RE research and practice. In
Figure 1, we present a general overview of several significant advances in LLM research
and development that we discuss further in this section. Following the introduction of
GPT-3 in 2020 [23], chain-of-thought (CoT) prompting emerged in early 2022 [186]
and instruction-tuning was introduced with InstructGPT in the same year [133]. Tool-
calling was first observed in the 2021 WebGPT study [128], after which it was later
embedded in LLM APIs in 2023 through GPT-3.5 and GPT-4; today, tool calling is
standard post-training for agent-supporting LLMs. Long CoT, which was inspired by
CoT and introduced through a post-training method called STaR in 2022 [198], first
arrived in production in late 2024 with GPT-o1. The agentic loop, introduced by the
popular ReAct framework [196], appeared in late 2023 [196]. Most recently, “skills”
that describe re-usable plans appeared in mid 2026 alongside Amazon Kiro and GitHub
SpecKit. Taken together, these advances enabled the creation of software engineering
(SE) agents and spec-driven development, which we discuss at the end of this section.


                                                                         “Skills”
                                             ReAct                       Spec-driven Dev
                                                                    Long Chain-of-Thought
                                                Tool calling
                                    Chain-of-Thought (CoT)
            In-context Learning     Instruction-tuning


          2020       2021         2022       2023        2024   2025        2026

Fig. 1 Timeline of significant advances in large language models.




3.1 Pre-training Limitations
The quality and type of pre-training data determines which “skills” can be learned
later [203]. GPT-3 was a notable advance not just because of its size (175B parame-
ters), but because its pre-training data included highly curated prose from web crawl
data, WebText2 pages linked from Reddit posts, and vast quantities of fiction and non-
fiction describing human emotion, motivation, empathy and strategy. This early data


                                                     6
also had its limitations: numerical representations of multiplication and division were
largely absent and there was an absence of code, which corresponded to poor math
performance [23] and the inability to generate executable code [29]. Finally, due to pre-
training cut-off dates – the date after which the LLM parameters are frozen and no
new information is learned – there will always be a need for augmented generation [61],
whether using retrieval-augmented generation [50] or tool calling [137, 142, 195]. In
fact, the under-representation of knowledge in pre-training is directly proportional to
inaccuracy in zero-shot question-answering [118].
    In RE, tacit knowledge, also referred to as the unknown knowns [156], refers to
knowledge that a stakeholder has, but which they withhold from the development
process for reasons including that they do not realize they have it or that they
struggle to articulate it [63]. Requirements elicitation interviews are the predomi-
nant technique for surfacing tacit knowledge [57]. A consequence of tacit knowledge
is under-representation of such knowledge in modern pre-training data: unspoken or
unwritten stakeholder needs are unlikely to be captured in web text, audio or video.
Consequently, because the accuracy of LLM-based question-answering is proportional
to the number of relevant pre-training documents [118], accuracy on tasks concerning
tacit knowledge is likely to be poor. Moreover, long-tail knowledge, which is largely
under-represented [87], leads to increased incidence of hallucination [200], which means
LLMs can generate factual inaccuracies or inconsistencies when LLMs are prompted
on topics covering tacit knowledge. While many measures of language models have
converged on fluency [71], we also know that human trust increases as reading effort
decreases, independent of whether the information is valid [96, 145], which can lead
to over-reliance and misplaced trust in generative AI [65].

3.2 Symbolic and Statistical Reasoning
Language models struggle to emulate logical reasoning [31], which is the foundation
of many RE analysis methods [110]. For example, when LLMs are tested on sym-
metric relations learned during fine-tuning, e.g., testing “B is A” when “A is B” was
learned, LLM performance is no better than random chance [16]. However, trans-
lating natural language problems into logic has since improved by decomposing and
chaining translations of atomic formulae needed to construct complex logic [153], and
then fine-tuning LLMs on synthetic logic samples to improve accuracy by 9-11% on
both logic and code benchmarks [125]. In contrast, chain-of-thought prompting [186]
raises awareness that inference-time compute to generate reasoning trajectories can
increase accuracy in math word problems. This observation led to frontier-scale large
reasoning models (LRMs) that generate long chain-of-thought (LCoT), which is encap-
sulated at inference time and later truncated from the response (e.g., in a generated
<think>< /think> block). While LCoT simulates cognitive behaviors (e.g., verifica-
tion, backtracking and sub-goal setting) in reasoning [60], the improvements gained
by CoT have been limited to logic and algorithmic reasoning tasks, with performance
on classification and question-answering tasks no different from random chance [165].
In LCoT, the cost of increasing inference-time compute is prohibitive, particularly
when LRMs are known for overthinking, which can arrive at and later skip a correct
answer in the reasoning trajectory [201]. Finally, it’s important to note that CoT is
not an explanation, nor is it necessarily faithful to the generated conclusion [173] and
unfaithfulness increases as language models become sufficiently large [15, 94].
    Reasoning by requirements analysts has traditionally been inquiry-focused [140]
to guide requirements elicitation, and model-driven notations and formalisms, includ-
ing use cases, data flow diagrams, state-transition diagrams, goal models and business



                                           7
process models [139]. While research using formal methods have studied the bene-
fits of automation to assist the human analyst [169], and logic is part of a historical
foundation of AI reasoning [62], there remains a gap between the recent advances
in LLM-based reasoning and reasoning used to perform requirements validation and
verification. Neuro-symbolic reasoning is a promising advance that combines the statis-
tical, translation capabilities of LLMs with the formal guarantees of theorem proving
and model checking [51]. This can be used to translate natural language requirements
into formal specifications expressed in logic, called auto-formalization [188], which can
then be checked using model checkers and verifiers [180].

3.3 Context Management
LLMs have evolved to include ever increasing context windows from approximately
2K tokens in GPT-3 to 8K-32K tokens in GPT-4-era models and 128K-1M tokens in
some modern frontier models. Larger contexts enable new tasks that require processing
large documents and code bases without pre-filtering this data. Context augmentation,
which consists of adding relevant data to the context window for task completion,
is a strategy to introduce new information that emerged after the LLM cut-off date
and to reduce hallucinations. This includes both retrieval-augmented generation [61]
and custom retrievers [50] and tool calling [142], in which LLMs generate tool calls to
collect information through APIs [137]. However, large contexts increase inaccuracy
in task performance when the information needed to answer questions becomes “lost
in the middle” [103], including a leading bias in summarization tasks [144]. Attention
loss is particularly a problem in long-horizon tasks (LHTs), which consist of extended
sequences of steps with delayed feedback and frequently combine context augmentation
with reasoning to complete multi-step problem solving.

4 Requirements Re-visited
Large language models (LLMs) have led to two new ways that researchers think about
requirements. In prompt programming, language model “prompts” are viewed as pro-
grams that include “requirements” intended to constrain the model output. In software
engineering (SE), there has been a shift toward deploying a version of a product, how-
ever imperfect, and relying on bug reports and feature requests to allow the product
to better meet stakeholder needs post-deployment. This process shift highlights the
value of LLM-based agents in the resolution of project issues. Finally, to guide SE
agents in general software development tasks, specification (spec)-driven development
has emerged as a means to anchor agents on documented requirements, which serve
as input to the agent. We now discuss these approaches as we re-visit emerging ways
that software engineering engages with requirements.

4.1 Prompt Programming
Prompt programming is a new paradigm that emerges from human computer interac-
tion and treats the LLM input context as a natural language program [58, 149] that
introduces a new class of requirement, defined as “a skeleton instruction that commu-
nicates an essential condition or constraint on desired LLMs output” [117]. In prompt
programming, “requirements engineering” is the practice of iterating over the instruc-
tions to improve the output, for example, by ignoring implicit requirements, such as
“respond in the same language,” that need not be stated, and by making task-relevant
requirements explicit, such as “correct the grammar in this e-mail” [117]. Programmers



                                           8
report frequently having to identify and introduce unknown knowns or tacit knowl-
edge into prompts to correct unintended LLM output [100]. Debugging is an exercise
in revising the prompt program to localize faults [101]. In prompt programming, qual-
ity requirements refer to the prompt output and may be induced by role instructions,
e.g., “software developer who writes clean and simple code” [88]. Where prompt pro-
gramming tasks concern code generation, the conventional definition of requirement
overlaps this new class, e.g., when a prompt instruction defines a requirement for the
behavior of the generated code [100].

4.2 Advances in Agentic AI
Agentic AI integrates recent advances in LLMs and LRMs into a harness that consists
of sensors, actuators and control loops.

4.2.1 Generalist Agents
The thought-action-observe (TAO) loop introduced by ReAct [196] is the foundation
of modern LLM-based agents, in which CoT is generated to plan the next action, after
which the result of the action is observed for feedback. If feedback includes observed
errors, the next thought step can choose an alternative action and re-try [162]. Sensors
and actuators correspond to the inputs and outputs of tool calls, wherein a tool is
an API function, which can further access command-line programs and scripts. Tools
can be selected during decoding [157] from a list of API references [142] or agents
can build their own tools through code generation [191]. Because LLMs are highly
sensitive to context changes [159], small changes to tool descriptions can impact tool
selection reliability [49]. Inspired by robotics, LLM-based agent performance improves
when planned actions are grounded in the world [3, 73], which has been extended to
solving computer tasks, including using command-line and web-based interfaces [89].
Skills compose tools into text-based procedures with “explicit applicability conditions,
execution policies, termination criteria, and reusable interfaces,” [81] which support
agents in solving longer horizon tasks [27].
    Multi-agent systems build on a simple paradigm, which consists of proposers that
generate content, and aggregators that synthesize, summarize, and discriminate signals
from generated content [183]. Agents can assume roles [97], which specialize their
generation and synthesis tasks, particularly during agent debate [26, 44].

4.2.2 Long-Horizon Tasks
Long-horizon tasks (LHTs) can lead to compounding errors as incorrect output from
one step propagates as input to the next step in the sequence. Agent gyms and arenas
have emerged to test an agent’s abilities in LHTs and discover limitations, includ-
ing in web page navigation [95, 204], desktop operating system usage [192], GitHub
issue resolution [82] and programming tasks [79]. Unlike classical benchmarks, gyms
and arenas operate “live” environments consisting of a containerized operating system
configured with running programs. Agents can be assigned a “budget” to limit token
utilization and other sources of under-performance, such as task re-try attempts. Eval-
uation metrics include task completion [105] and tool selection [137, 142] accuracy, and
agent-to-agent matchup performance via win rates and ELO ratings [32, 202]. Because
task trajectories are non-deterministic, pass@k is a popular metric, which estimates
the probability of at least one successful outcome across k attempts [29]. There is an
increasing over-reliance on LLM-as-a-Judge [202] to perform evaluations of two out-
comes, wherein little established ground truth presupposes that LLMs are sound and
reliable verifiers, even if they are flawed generators. This over-reliance is in contrast


                                           9
to recent evaluations that show LLM-as-a-Judge with strong models produce biased
labels [43] and perform slightly better than random guessing [168].

4.2.3 Software Engineering Agents
Software engineering agents tailor the generalist agent paradigm to software engineer-
ing tasks, such as issue resolution and debugging. For example, issue resolving agents
use tools to find and edit relevant files in project repositories before submitting a
pull request containing a code patch that resolves a reported issue [182, 193]. Popu-
lar benchmark are curated from GitHub project repositories to include Python code
bases, issues and pull requests [82, 199] and executable runtime environments [135],
as well as, a pipeline to generate training data for benchmarks [194]. Evidence shows
that hand-crafted AI pipelines for issue resolution can still outperform synthetic data
and Agentic frameworks [190].

4.3 Spec-Driven Development
Spec-Driven Development (SDD) re-frames requirements specifications as operational
inputs to coding-generating agents in contrast to being reference documents only
reviewed by humans developers [138]. In SDD, specifications or “specs” are a version-
controlled, behavior-oriented artifact that describes product scenarios, user stories,
EARS-formatted requirements [119], environmental and development constraints, and
expected outcomes before implementation begins [41]. Specs, which in RE sit at the
intersection of the machine and the environment [75], more broadly cover requirements
artifacts in SDD and are intended to provide the coding agent with the necessary
context to steer implementation. The SDD defines a spectrum in which specs gain
increasing authority over code: in spec-first development, the spec is written before
coding to guide the initial implementation, which may drift away from the spec over
time; in spec-anchored development, the spec is maintained alongside the code and
alignment is enforced through testing; and in spec-as-source development, developers
edit specifications while code is generated from the spec [138].
     Recent tools impose SDD workflows on development, including GitHub
SpecKit [41], Amazon Kiro, BMAD, and OpenSpec 1 . Each workflow defines a spec
format, level of detail, and how specs are integrated into a project. While spec files are
written in natural language, early research argues that LHTs require additional arti-
facts, including scenarios, models, and Gherkin-style specifications to improve SDD
outcomes [54].
     The SDD vision and current tool support have open challenges in software devel-
opment process quality, including a lack of sufficient evaluation frameworks and
benchmarks to verify requirements satisfaction and traceability. LLMs struggle to gen-
erate executable behavioral specifications, especially at repository level, where the
best model in CodeSpecBench solves only 20.2% of tasks [28]. Maintaining spec sat-
isfiability over time is also challenging because, as the software project grows, the
code could drift away from the specs on which the code was initially based. Studies of
repository-level context files show mixed results: while agents.md files, which contain
agent instructions, rules, and context, may reduce median runtime and output token
use while preserving completion behavior [113], when context files contain unneces-
sary requirements they are observed to have the opposite effect, reducing task success
and increasing token use [66]. Similarly, explicit plans can improve issue resolution
by agents, whereas subpar plans and poorly aligned instruction language can degrade

 1
     Amazon Kiro, BMAD and OpenSpec




                                           10
performance [104]. As prior work in prompt engineering has shown, LLMs are sensitive
to input contexts and research is needed as task complexity increases.

5 Future of Requirements
Advances in AI create new opportunities for the future of RE research. In par-
ticular, we focus on two broad dimensions: matters of software process, including
how AI is changing the way that software is constructed; and matters of experienc-
ing requirements, which shifts how we collect, analyze, and realize requirements in
software.

5.1 Matters of Software Process
In the early aughts at the turn of the century, Agile methodology fundamentally
changed how requirements were integrated into software development by reducing
effort invested into requirements planning and emphasizing the need to work with
skilled developers [20]. Arguably, the growing prevalence of frameworks and reusable
code enabled this change by accelerating development when developers accept require-
ments from third-party code. SE agents have the potential to again transform this
integration by shifting attention back to well-defined requirements, because agents
increasingly sit between the developer and the code. While Agile methods depend
heavily on expert developers to function without extensive documentation and plan-
ning [20], SE agents require upfront planning and direction, including instructions
with detailed requirements [138]. In this section, we review the ways that LLMs are
transforming the requirements engineering process.

5.1.1 From Validation to Verification
Recent AI-assisted RE tasks surveyed in Section 2 primarily cover requirements valida-
tion, which concerns whether organizations have the right requirements by acquiring
requirements-related data from novel sources [1, 42, 74, 98, 163] and identifying
requirements defects [6, 17, 70, 85, 112]. Less work covers requirements verification,
which concerns checking whether design specifications and code satisfy require-
ments [4, 155], as well as work to bridge requirements to verification, including test
case generation [8] and trace link discovery [37, 69]. Meanwhile, developers routinely
face challenges using AI-assisted code completion, including difficulty interpreting and
debugging generated code [11, 176], which obfuscates the information needed to per-
form verification. Developers report that requirements are often too abstract to include
in prompts, instead they have to first decompose requirements into programming tasks
manually, which are then further enriched by developers with design decisions and
architectural constraints [174].
    Requirements analysis and implementation planning by future SE agents will
require intentional fine-tuning of LLMs to be proficient, as evidenced by NLP
performance gains realized through instruction-tuning [109]. While zero-shot chain-of-
thought prompting was an emergent LLM property [91], long chain-of-thought, which
underpins LRMs and includes inferential behaviors such as verification and backtrack-
ing [60], was only achieved through reinforcement learning [198]. SE agents introduce
additional abstractions between the developer and code, introducing new questions
about the maintainability and reliability of specs in agentic development. New work is
needed to evaluate SE agents in requirements comprehension and to extend SE agentic
benchmarks to cover requirements task evaluation.



                                          11
    Spec-driven development proposes to create a path from validation to verification
by turning validated requirements into executable or checkable artifacts. If a valid spec
is used to shape and control generated artifacts in downstream tasks, then generated
code, generated tests, and generated documentation must be checked against behavior
intended by the spec. Preliminary research already shows that executable behavioral
specifications encode pre-conditions and post-conditions that can accept valid behav-
ior and reject invalid behavior [28]. Auto-formalization may further increase access
to formal methods by translating natural language mathematics into formal specifi-
cations and proofs [188], while neuro-symbolic methods may allow offloading parts of
verification to theorem provers and model checkers.

5.1.2 Singular to Long-Horizon Tasks
Prior work has largely focused on well-defined, separable, and singular RE tasks, for
example, deciding which software features to delete [129]. However, the efficacy of task
automation is determined by introducing the task output into a downstream task,
such as identifying code-level dependencies on features targeted for removal, accepting
or rejecting the feature removal request based on these dependencies, removing code
associated with accepted feature deletion requests, and updating requirements docu-
mentation to reflect the change. In prior research, the downstream task is frequently
presented as motivation using vague terminology, for example, to support requirements
elicitation and analysis [90], to support maintenance and version tracking [181], or
to support product improvement, customer outreach, and competitive analysis [121].
A consequence of this vagueness is that the downstream task is under-specified and
unclear, in which case the singleton task output may not be fit-for-purpose.
    RE therefore needs long-horizon benchmarks that evaluate requirements utility
beyond singular tasks. SE has SWE-bench-style issue-resolution benchmarks for assess-
ing whether agents can modify real repositories [82]. However, RE does not have a
widely accepted benchmark suite where agents must elicit and analyze real require-
ments, plan an implementation against those requirements, maintain traces, and
test requirements satisfiability. To leverage recent advances in agentic AI, future RE
research should focus on RE-specific arena and gym designs to include: elicitation
tasks, such as detecting tacit knowledge or design trade-offs that require clarification
of stakeholder intent; modeling and analysis tasks to surface implied requirements or
requirements conflicts; and trace preservation tasks to avoid losing requirements and
design intent over multiple cycles of agentic loops and tying implementation back to
stakeholder acceptance tests. With LHT evaluation, arenas and gyms move beyond
testing only whether a requirements artifact is fluent. In practice, we understand that
the best benchmarks are: (1) based on real data, not synthetic data; (2) designed with
a deterministic, measurable objective that is used to show improvement; and (3) so
difficult that baseline attempts achieve roughly 10% accuracy, which is small enough
to leave room for improvement and large enough to show that machine learning is
feasible.
    Advances in LLM-based code generation introduce new opportunities to extend
RE tasks into implementation and testing. In testing, for example, a long-horizon
task consists of identifying requirements, finding relevant code segments distributed
across multiple files that relate to those requirements, writing and executing test
cases, and changing the code to pass those test cases. Code can represent traditional
requirements abstractions, including models [77], which may support translating the
results of model-based analysis into code generation and evaluating the effects of
this translation through novel, long-horizon task benchmarks. Original requirements
analysis techniques that pre-date the latest AI advances, such as model checking [25],


                                           12
model merging [130], and obstacle analysis [5, 175], may be re-imagined as RE tools
for use by SE agents. A challenge, however, is managing cascading error across the
duration of LHTs and supporting tool calls, which requires innovation in evaluation.
    To take advantage of these LHT opportunities, RE researchers must invest in
acquiring more data for LLM training and fine-tuning, particularly in rare and special-
ized domains. Underlying every agent harness used to solve an LHT is an LLM that
has been pre-trained on the domain and the sub-tasks required to fulfill the LHT. The
absence of requirements documentation in public code repositories elevates reverse
engineering research to acquire requirements from code [197]. While some might argue
that the gold standard is industry data in RE, the code generating model Codex was
fine-tuned from a GPT-3 base on public GitHub repositories [29], which are frequently
criticized for being mostly inactive or personal projects [86]. This is because, in addi-
tion to memorization, LLMs learn patterns and clone behavior from data, which can
generalize to solve industrial tasks that fit the same patterns as public, open source
projects. In contrast, recursive training on synthetic data is known to lead to model
collapse [164]. This observation is in contrast to model distillation, which is shown
to yield high performance in small models trained from data generated by larger
models [60].

5.1.3 Innovation in Evaluation
As instruction-tuned LLMs are increasingly used to manipulate and transform the
requirement text, and as requirements are further integrated into downstream tasks,
novel metrics and benchmarking methods are needed to evaluate the effectiveness
of future AI-driven RE. The traditional natural language generation (NLG) metrics
BLEU and ROUGE, for example, have known limitations that reduce their effective-
ness in evaluating generated requirements artifacts. BLEU measures modified n-gram
precision with a brevity penalty [136], and is known to measure improvement with-
out increases in quality assessed by human judges [24, 146]. ROUGE is a family of
recall-oriented overlap metrics [102], and can exhibit measured improvement when
the generated text contains hallucinations [21, 120]. In code generation, BLEU and
ROUGE penalize programs with structural dissimilarity that produce the same, cor-
rect output [29]. LLM-as-a-Judge [202] also does not solve this problem. Agentic
benchmarks are increasingly relying on LLM judges, but recent evaluations show that
LLM judges can produce biased labels [43] and perform only slightly better than
random guessing in certain settings [168].
    Human evaluation is also insufficient when it is dominated by fluency. NLG
researchers documented over 200 metrics used across 478 single-criteria evaluations
in a survey of 165 research papers from 2000-2020 [71]. Among these metrics, flu-
ency (“how grammatical and readable is the text?”) mapped to the largest number
of normalized criteria, which is known to correlate with human trust [96, 145]: as flu-
ency increases in the text, humans are more likely to trust the text, independent of
what the human may need to comprehend from the text. Moreover, human evaluators
applying an evaluation rubric to score factuality tend to employ a fluency heuristic
by rating fluent text as higher quality regardless of factual content [33, 80]. Wherein
LLMs are used to solve increasingly complex, long-horizon tasks, researchers risk sub-
jecting their evaluations of generated artifacts to fluency bias, reducing their ability to
measure the construct of interest. In RE, for example, fluent requirements and fluent
trace explanations may appear plausible to human evaluators, even when they fail to
preserve stakeholder intent or satisfy a specification.
    Due to the dominance of fluency as a mediating factor, requirements evaluation
may need to shift from human assessments of generated requirements quality (e.g.,


                                            13
ambiguity, completeness, consistency) to measuring requirements utility, or how use-
ful and fit-for-purpose generated requirements artifacts are in LHTs. Agent gyms
and arenas introduce LHT evaluation strategies in web page navigation [95, 204],
desktop operating system usage [192], GitHub issue resolution [82] and programming
tasks [79] that measure changes in outcomes. For example, GitHub issue resolution
benchmarks [82] use pass@k [29], which estimates whether at least one of k agent-
generated code samples passes oracle test cases, while the effects of agents browsing the
web and completing web forms are evaluated using content metrics for exact match,
string subset, and fuzzy match [204]. Moving beyond requirements text and quality
metrics requires a deeper understanding of how changes in requirements affect changes
in the state of software development.

5.1.4 Requirements Evolution & Management
Software engineering (SE) agents and Spec-Driven Development (SDD) have the
potential to change requirements management from a repository of stored requirements
into an active process for evolving agent-facing artifacts. When specifications guide
implementation, a change request should first be interpreted as a proposed change to
existing spec files. The scenarios, constraints, plans, tests, and code affected by the
changes can then be updated as downstream artifacts. This is especially important in
brownfield projects, where the agent must preserve existing behavior while adding or
revising functionality [138].
     Requirements management is not only to store specifications, but to keep specs
minimal, current, and performant in SE agent frameworks. Context files (e.g.,
agents.md and spec.md) reduce development time or increase task failure, depending
on how they are written [66, 113], particularly if they contain irrelevant informa-
tion [66]. To address evolution, context files must be versioned and maintained, with
frequent changes by adding or modifying instructions, sections, and testing guid-
ance [123]. To understand and predict the impact of requirements evolution on SDD
workflows, we need new methods for change-impact analysis over spec-related arti-
facts. The goal is to detect conflicts early, propagate accepted changes to the correct
artifacts, and preserve traceability across repeated AI-driven software revisions.
     A key challenge going forward will be context management by ensuring that
SE agents that are refactoring code adhere to previously documented requirements,
assumptions, and constraints. As this documentation grows, new techniques for man-
aging and scoping only relevant context to a given task will be needed to avoid
attention loss. Vanilla retrieval-augmented generation (RAG) methods may be insuf-
ficient during a LHT, instead requiring recursive summarization [180], hierarchical
memory management [167], or graph-based retrieval techniques [116], among others,
adapted to scope and trace requirements to partitions of software project repositories.

5.2 Matters of Experiencing Requirements
Recent advances in AI have the potential to shift how requirements are experienced
by developers and stakeholders, including users. As upfront requirements elicitation,
documentation and analysis have been reduced over time in Agile development, devel-
opers have come to experience stakeholder “needs” through software implementation:
as they author code, they realize needs for process concurrency to improve response
times, or needs to pre-process and stage data to simplify user interfaces and work-
flows [45]. Such needs arise during coding due to under-specified requirements, which
developers have managed to backfill while they face implementation challenges or



                                           14
observe performance deficits during implementation and testing. This experiential pro-
cess illustrates Jackson’s argument S, K ⊨ R, wherein requirements are a by-product
of software and knowledge, regardless of whether the requirements were collected and
documented early in the process.
    We organize this section in three parts: developer experience of requirements dur-
ing implementation will be reduced as they off-load code authorship to AI; with AI,
developers have easier access to preview requirements through behavioral artifacts,
such as prototypes, that have traditionally been too costly to implement; and stake-
holders could have new opportunities to express requirements through more responsive
and adaptive AI-driven means.

5.2.1 Reductions in Authorship Experience
Advances in AI are changing how requirements are experienced by developers: devel-
opers who rely on SE agents to complete SE tasks will defer their experiences
of requirements later into testing, in memory of Royce’s critique of the waterfall
model [151]. The traditional practices of interpreting requirements to plan implemen-
tation, of authoring code to implement the plan, and of writing test cases to verify
that the authored code will satisfy requirements are being delegated to SE agents
(e.g., Claude Code or GitHub Copilot). Historically, as developers author software
components during implementation, they often experience unstated assumptions in
requirements. For example, integrating a component with an audio processing library
can introduce audio sampling and encoding constraints imposed by the library, which
may have been unspecified in the original requirements; or segmenting data process-
ing into asynchronous components can raise unstated performance requirements when
components run at different speeds and slower than anticipated. In Agile software
development, these unknown knowns may be identified and resolved in the code by
the developer, while remaining undocumented. With SE agents, developers will off-
load these experiences to agents, which will cause their comprehension of requirements
to become shallow, less particular and less technical. Developers need greater trans-
parency into requirements-related design choices that arise during implementation so
that those choices may be reviewed, supervised, and documented. Meanwhile, written
requirements and specifications could emerge as a contract between the developer and
agent, if the effects of that documentation leads to guarantees of software behavior in
development and production.

5.2.2 Previewing Behavioral Experiences
An important consequence of LLMs today and going forward is the reduced effort
needed to author benchmarks, prototypes, and simulations in code. Benchmarks pro-
vide a means to evaluate and compare alternative design choices against established
performance measures and to test for performance regression, while prototypes allow
developers to reduce risk by exploring technology integrations. In software engineer-
ing research and practice, SE agents can now be used to generate multiple, divergent
prototypes for far less cost and time, allowing stakeholders to review and select
the best prototype. After learning about the effectiveness of integrations to satisfy
requirements, prototypes can be thrown away, if they represent a path to abandon,
or preserved as part of the system to-be [39]. Simulations are used to test scalabil-
ity and to evaluate the effects of edge cases, particularly in autonomous systems [18].
Combined, these techniques allow developers and other stakeholders to preview, assess
and experience various requirements outcomes faster, even before the requirements are
explored or understood. Advances in LLMs to generate code can be used to expedite


                                          15
development and re-introduce these planning activities originally proposed in plan-
driven development [19]. These techniques may be used to define requirements-based
guardrails around development spaces: the outcome of design variances introduced
by SE agents, for example, may be observed through benchmarks, explored using
prototypes, and assessed at scale using simulations.

5.2.3 Responsive and Adaptive Specification
As Agile methods have minimized costly planning procedures, techniques have
emerged to preserve and simulate access to stakeholder needs, often through stake-
holder surrogacy. This includes the product owner role, which is a member of the
development team who represents stakeholder values and intent [14, 158], and per-
sonas, which are representative “cutouts” used to motivate and guide discussions about
how stakeholders view and experience needs [141]. The extent to which SE agents
become increasingly responsible for larger portions of the software development life
cycle (SDLC), the cost of customization and personalization may be reduced to allow
end-users to more easily communicate their unmet needs directly to designers, SE
agents or both. In RE, traditional ML has been used to mine user needs from app
reviews [35, 111], which capture delayed descriptions of user need, often long after an
unmet need is experienced. In contrast, SE agents create the possibility that users can
identify their unmet needs in the moment of experience, wherein the salience of those
needs is highest and the description of desired outcomes may be more easily demon-
strated and evaluated by those users as SE agents iterate over solutions. This includes
capturing ephemeral requirements that require satisfaction within minutes or hours of
experience [56, 108]. To accommodate real-time refactoring, software must be designed
to support modifiability, evolution, and even self-adaptivity, in which software sensors
dynamically detect the need to undergo design adaptation [30, 36, 64].

6 Conclusion
Requirements engineering (RE) activities have long been considered repetitive and
tedious due to the intensive human effort required to collect, analyze, and synthesize
under-specified and conflicting needs into actionable requirements. In the past five
years, a transformation through generative artificial intelligence (AI) has impacted
nearly every domain in which software is used. Against the backdrop of an outstanding
rate of innovation in software engineering (SE), we observe a shift in the use of AI
from solving singular tasks to longer-horizon tasks, in which SE agents situate code
generation into agentic planning loops using observation, feedback, and verification.
This innovation creates new opportunities for re-introducing historically heavy-weight
RE methods into the software engineering pipeline, while allowing developers to see the
outcome of RE-related changes throughout the pipeline. Future RE tasks must account
for the underlying technology fundamentals and innovation in large language models
and agentic AI. While the future is hard to predict in this rapidly changing moment, we
envision two general ways that requirements stand to change: in how requirements are
integrated into software processes, shifting the focus from validation, which remains
relevant, toward verification, especially as a form of evaluating automation over long
horizon tasks; and in how requirements are experienced, shifting developer attention
away from code authorship and toward evaluating design alternatives and observing
the behavioral effects of selected designs, while increasing stakeholder access to directly
evolve requirements and implementations at their own time of need.




                                            16
References
 [1] Abualhaija, S., Arora, C., Sleimi, A. and Briand, L.C., 2022, August. Automated
     question answering for improved understanding of compliance requirements: A
     multi-document study. In 2022 IEEE 30th international requirements engineering
     conference (RE) (pp. 39-50).

 [2] Abualhaija, S., Ceci, M., Sannier, N., Bianculli, D., Briand, L.C., Zetzsche, D. and
     Bodellini, M., 2024, June. AI-enabled regulatory change analysis of legal require-
     ments. In 2024 IEEE 32nd International Requirements Engineering Conference
     (RE) (pp. 5-17).

 [3] Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., Finn,
     C., Fu, C., Gopalakrishnan, K., Hausman, K. and Herzog, A., 2022. “Do as I
     can, not as I say: Grounding language in robotic affordances.” arXiv preprint
     arXiv:2204.01691.

 [4] Al Islam, M.N., Ma, Y., Alarcon, P., Chawla, N. and Cleland-Huang, J., 2022,
     August. RESAM: Requirements elicitation and specification for deep-learning
     anomaly models with applications to UAV flight controllers. In 2022 IEEE 30th
     international requirements engineering conference (RE) (pp. 153-165).

 [5] Alrajeh, D., Kramer, J., Van Lamsweerde, A., Russo, A. and Uchitel, S., 2012,
     June. “Generating obstacle conditions for requirements completeness.” In 2012
     34th International Conference on Software Engineering (ICSE) (pp. 705-715).
     IEEE.

 [6] Amaral, O., Abualhaija, S. and Briand, L., 2023, September. Ml-based compli-
     ance verification of data processing agreements against gdpr. In 2023 IEEE 31st
     international requirements engineering conference (RE) (pp. 53-64).

 [7] Anish, P.R., Lawhatre, P., Chatterjee, R., Joshi, V. and Ghaisas, S., 2022. “Auto-
     mated Labeling and Classification of Business Rules from Software Requirement
     Specifications.” In 2022 IEEE/ACM 44th International Conference on Software
     Engineering: Software Engineering in Practice (ICSE-SEIP). https://ieeexplore.
     ieee.org/document/9793544.

 [8] Arora, C., Herda, T. and Homm, V., 2024, June. Generating test scenarios from nl
     requirements using retrieval-augmented llms: An industrial study. In 2024 IEEE
     32nd International Requirements Engineering Conference (RE) (pp. 240-251).

 [9] Askell, A., Bai, Y., Chen, A., Drain, D., Ganguli, D., Henighan, T., Jones, A.,
     Joseph, N., Mann, B., DasSarma, N. and Elhage, N., 2021. “A general language
     assistant as a laboratory for alignment.” arXiv preprint arXiv:2112.00861.

[10] Azeem, M.I. and Abualhaija, S., 2024. “A Multi-solution Study on GDPR
     AI-enabled Completeness Checking of DPAs.” Empirical Software Engineering.
     https://doi.org/10.1007/s10664-024-10491-3.

[11] Barke, S., James, M.B. and Polikarpova, N., 2023. “Grounded CoPilot: How pro-
     grammers interact with code-generating models.” Proceedings of the ACM on
     Programming Languages, 7(OOPSLA1), pp.85-111.




                                           17
[12] Barzamini, H., Ramesh, S., Adiththan, A., Peranandam, P. and Rahimi, M., 2025,
     September. Specifying Operational Design Domain in Autonomous Driving for
     Comprehensive Data Evaluation. In 2025 IEEE 33rd International Requirements
     Engineering Conference (RE) (pp. 43-55).

[13] Bashir, S., Abbas, M., Ferrari, A., Saadatmand, M. and Lindberg, P., 2023,
     September. Requirements classification for smart allocation: A case study in
     the railway industry. In 2023 IEEE 31st International Requirements Engineering
     Conference (RE) (pp. 201-211)

[14] Bass, J.M., Beecham, S., Razzak, M.A., Canna, C.N. and Noll, J., 2018, May.
     “An empirical study of the product owner role in scrum.” In Proceedings of the
     40th International Conference on Software Engineering (pp. 123-124).

[15] Bentham, O., Stringham, N. and Marasović, A., 2024, July. “Chain-of-thought
     unfaithfulness as disguised accuracy.” Transactions on Machine Learning
     Research.

[16] Berglund, L., Tong, M., Kaufmann, M., Balesni, M., Stickland, A., Korbak, T.
     and Evans, O., 2024, May. “The Reversal Curse: LLMs trained on ‘A is B’ fail to
     learn ‘B is A’.” In International Conference on Learning Representations (Vol.
     2024, pp. 18623-18642).

[17] Bertram, V., Kausch, H., Kusmenko, E., Nqiri, H., Rumpe, B. and Venhoff,
     C., 2023, September. Leveraging natural language processing for a consistency
     checking toolchain of automotive requirements. In 2023 IEEE 31st International
     Requirements Engineering Conference (RE) (pp. 212-222).

[18] Birchler, C., Khatiri, S., Rani, P., Kehrer, T. and Panichella, S., 2025. A
     roadmap for simulation-based testing of autonomous cyber-physical systems:
     Challenges and future direction. ACM Transactions on Software Engineering and
     Methodology, 34(5), pp.1-9

[19] B. W. Boehm, “A spiral model of software development and enhancement,” ACM
     Software Engineering Notes, 11(4): 14-24, 1988.

[20] B. W. Boehm, Turner. Balancing Agility and Discipline: A Guide for the
     Perplexed, 1st ed., Addison-Wesley, 2004.

[21] Böhm, F., Gao, Y., Meyer, C.M., Shapira, O., Dagan, I. and Gurevych, I., 2019,
     November. “Better rewards yield better summaries: Learning to summarise with-
     out references.” In Proceedings of the 2019 Conference on Empirical Methods
     in Natural Language Processing and the 9th International Joint Conference on
     Natural Language Processing (EMNLP-IJCNLP) (pp. 3110-3120).

[22] Bragilovski, M., Van Can, A.T., Dalpiaz, F. and Sturm, A., 2024, June. Deriv-
     ing domain models from user stories: Human vs. machines. In 2024 IEEE 32nd
     International Requirements Engineering Conference (RE) (pp. 31-42). IEEE.

[23] Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Nee-
     lakantan, A., Shyam, P., Sastry, G., Askell, A. and Agarwal, S., 2020. “Language
     models are few-shot learners.” Advances in neural information processing systems,
     33, pp.1877-1901.


                                         18
[24] Callison-Burch, C., Osborne, M. and Koehn, P., 2006, April. “Re-evaluating the
     role of BLEU in machine translation research.” In 11th conference of the European
     chapter of the Association for Computational Linguistics (pp. 249-256).

[25] Chan, W., Anderson, R.J., Beame, P., Burns, S., Modugno, F., Notkin, D.
     and Reese, J.D., 1998. “Model checking large software specifications.” IEEE
     Transactions on Software Engineering, 24(7), pp.498-520.

[26] Chan, C.M., Chen, W., Su, Y., Yu, J., Xue, W., Zhang, S., Fu, J. and Liu, Z.,
     2024, May. Chateval: Towards better llm-based evaluators through multi-agent
     debate. In International conference on learning representations (Vol. 2024, pp.
     9079-9093).

[27] Chen, S., Gai, J., Zhou, R., Zhang, J., Zhu, T., Li, J., Wang, K., Wang, Z., Chen,
     Z., Kaleb, K. and Miao, N., 2026. “Skillcraft: Can LLM agents learn to use tools
     skillfully?” arXiv preprint arXiv:2603.00718.

[28] Chen, Z., Dai, J., Zhu, B., Wang, J., Wang, H., Xu, X., Yuan, H., Guo, Z. and Wu,
     X.M., 2026. “CodeSpecBench: Benchmarking LLMs for executable behavioral
     specification generation.” arXiv preprint arXiv:2604.12268.

[29] Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H.P.D.O., Kaplan, J., Edwards,
     H., Burda, Y., Joseph, N., Brockman, G. and Ray, A., 2021. “Evaluating large
     language models trained on code.” arXiv preprint arXiv:2107.03374.

[30] Cheng, B. HC., de Lemos, R., Giese, H., Inverardi, P., Magee, J., Andersson, J.,
     Becker, B., Bencomo, N., Brun, Y., Cukic, B., Di Marzo Serugendo, G., Dustdar,
     S., Finkelstein, A., Gacek, C., Geihs, K., Grassi, V., Karsai, G., Kienle, H.M.,
     Kramer, J., Litoiu, M., Malek, S., Mirandola, R., Miller, H.A., Park, S., Shaw, M.,
     Tichy, M., Tivoli, M., Weyns, D., Whittle, J. 2009. “Software engineering for self-
     adaptive systems: A research roadmap” In Software Engineering for Self-adaptive
     Systems, pp. 1-26, Springer, Berlin, Heidelberg

[31] Cheng, F., Li, H., Liu, F., Van Rooij, R., Zhang, K., and Lin, Z. 2025. “Empow-
     ering LLMs with logical reasoning: a comprehensive survey.” In Proceedings of
     the 34th International Joint Conference on Artificial Intelligence. Article 1155,
     10400–10408.

[32] Chiang, W.L., Zheng, L., Sheng, Y., Angelopoulos, A.N., Li, T., Li, D., Zhang,
     H., Zhu, B., Jordan, M., Gonzalez, J.E. and Stoica, I., 2024. Chatbot arena: An
     open platform for evaluating llms by human preference. In Proceedings of the 41st
     International Conference on Machine Learning (ICML), Article No.: 331, Pages
     8359-8388.

[33] Clark, E., August, T., Serrano, S., Haduong, N., Gururangan, S. and Smith, N.A.,
     2021, August. “All that’s ‘human’ is not gold: Evaluating human evaluation of
     generated text.” In Proceedings of the 59th Annual Meeting of the Association
     for Computational Linguistics and the 11th International Joint Conference on
     Natural Language Processing (Volume 1: Long Papers) (pp. 7282-7296).

[34] Cui, K.Z., Demirer, M., Jaffe, S., Musolff, L., Peng, S. and Salz, T., 2026.
     “The effects of generative AI on high-skilled work: Evidence from three field
     experiments with software developers.” Management Science.


                                          19
[35] Dabrowski, J., Letier, E., Perini, A. and Susi, A., 2022. “Analysing app reviews
     for software engineering: a systematic literature review.” Empirical Software
     Engineering, 27(2), p.43.

[36] De Lemos, R., Giese, H., Müller, H.A., Shaw, M., Andersson, J., Litoiu, M.,
     Schmerl, B., Tamura, G., Villegas, N.M., Vogel, T. and Weyns, D., 2013, January.
     “Software engineering for self-adaptive systems: A second research roadmap.”
     In Software Engineering for Self-Adaptive Systems II: International Seminar,
     Dagstuhl Castle, Germany, October 24-29, 2010 Revised Selected and Invited
     Papers (pp. 1-32). Berlin, Heidelberg: Springer Berlin Heidelberg.

[37] Das, S., Deb, N., Cortesi, A. and Chaki, N., 2023, September. Zero-shot learning
     for named entity recognition in software specification documents. In 2023 IEEE
     31st International Requirements Engineering Conference (RE) (pp. 100-110).

[38] Davenport, T.H. and Srinivasan, L., 2026. Companies Are Laying Off Workers
     Because of AI’s Potential—Not Its Performance. Harvard Business Review, 29.

[39] Davis, A.M., 2002. “Operational prototyping: A new development approach.”
     IEEE software, 9(5), pp.70-78.

[40] Dearstyne, K.R., Granadeno, P.T.A., Chambers, T. and Cleland-Huang, J., 2025,
     September. QUESTRL: A Q&A Framework for Designing Trustworthy Rein-
     forcement Learning Systems. In 2025 IEEE 33rd International Requirements
     Engineering Conference (RE) (pp. 80-91).

[41] Delimarsky, D. and Riem, M., 2026. Spec Kit. Version 0.7.3. GitHub. https://
     github.github.io/spec-kit/.

[42] Devine, P., Tizard, J., Wang, H., Koh, Y.S. and Blincoe, K., 2022, August. What’s
     inside a cluster of software user feedback: A study of characterisation methods. In
     2022 IEEE 30th International Requirements Engineering Conference (RE) (pp.
     189-200).

[43] Dorner, F.E., Nastl, V. and Hardt, M., 2025, May. Limits to scalable evaluation at
     the frontier: Llm as judge won’t beat twice the data. In International Conference
     on Learning Representations (Vol. 2025, pp. 26467-26491).

[44] Du, Y., Li, S., Torralba, A., Tenenbaum, J.B. and Mordatch, I., 2024, July.
     Improving factuality and reasoning in language models through multiagent
     debate. In Forty-first international conference on machine learning.

[45] Ernst, N.A. and Murphy, G.C., (2012). “Case studies in just-in-time requirements
     analysis.” In 2012 Second IEEE international workshop on empirical requirements
     engineering (EmpiRE) (pp. 25-32). IEEE.

[46] Ezzini, S., Abualhaija, S., Arora, C. and Sabetzadeh, M., 2022. “Automated han-
     dling of anaphoric ambiguity in requirements: a multi-solution study.” In ICSE
     ’22. https://dl.acm.org/doi/10.1145/3510003.3510157.

[47] Ezzini, S., Abualhaija, S., Arora, C. and Sabetzadeh, M., 2023. “AI-based Ques-
     tion Answering Assistance for Analyzing Natural-language Requirements.” arXiv
     preprint arXiv:2302.04793. http://arxiv.org/abs/2302.04793.



                                          20
[48] Ezzini, S., Abualhaija, S., Arora, C., Sabetzadeh, M. and Briand, L.C., 2021.
     “Using Domain-Specific Corpora for Improved Handling of Ambiguity in Require-
     ments.” In 2021 IEEE/ACM 43rd International Conference on Software Engi-
     neering (ICSE). https://ieeexplore.ieee.org/document/9402055.

[49] Faghih, K., Wang, W., Cheng, Y., Bharti, S., Sriramanan, G., Balasubramanian,
     S., Hosseini, P. and Feizi, S., 2025, November. Tool Preferences in Agentic LLMs
     are Unreliable. In Proceedings of the 2025 Conference on Empirical Methods in
     Natural Language Processing (pp. 20965-20980).

[50] Fan, W., Ding, Y., Ning, L., Wang, S., Li, H., Yin, D., Chua, T.S. and Li,
     Q., 2024, August. “A survey on rag meeting llms: Towards retrieval-augmented
     large language models.” In Proceedings of the 30th ACM SIGKDD conference on
     knowledge discovery and data mining (pp. 6491-6501).

[51] Fang, M., Deng, S., Zhang, Y., Shi, Z., Chen, L., Pechenizkiy, M. and Wang,
     J., 2024, March. “Large language models are neurosymbolic reasoners.” In Pro-
     ceedings of the AAAI Conference on Artificial Intelligence (Vol. 38, No. 16, pp.
     17985-17993).

[52] Fazelnia, M., Koscinski, V., Herzog, S. and Mirakhorli, M., 2024, June. Lessons
     from the use of natural language inference (nli) in requirements engineering tasks.
     In 2024 IEEE 32nd International Requirements Engineering Conference (RE) (pp.
     103-115).

[53] Fazelnia, M., Mirakhorli, M. and Bagheri, H., 2024. “Translation Titans, Reason-
     ing Challenges: Satisfiability-Aided Language Models for Detecting Conflicting
     Requirements.” In ASE ’24. https://dl.acm.org/doi/10.1145/3691620.3695302.

[54] Feng, S., Chen, B., Meyer, B.H. and Mussbacher, G., 2026. “LLM-assisted
     repository-level generation with structured spec-driven engineering.” In Pro-
     ceedings of the 34th ACM Joint European Software Engineering Conference
     and Symposium on the Foundations of Software Engineering Companion (FSE
     Companion ’26).

[55] Ferrara, C., Casillo, F., Gravino, C., De Lucia, A. and Palomba, F., 2024.
     “ReFAIR: Toward a Context-Aware Recommender for Fairness Requirements
     Engineering.” In ICSE ’24. https://dl.acm.org/doi/10.1145/3597503.3639185.

[56] Fickas, S., Beauchamp, T. and Mamy, N.A.R., 2002, September. “Monitoring
     requirements: A case study.” In Proceedings 17th IEEE International Conference
     on Automated Software Engineering, (pp. 299-304). IEEE.

[57] Ferrari, A., Spoletini, P. and Gnesi, S., 2016. Ambiguity and tacit knowledge in
     requirements elicitation interviews. Requirements Engineering, 21(3), pp.333-355.

[58] Fiannaca, A.J., Kulkarni, C., Cai, C.J. and Terry, M., 2023, April. “Programming
     without a programming language: Challenges and opportunities for designing
     developer tools for prompt programming.” In Extended Abstracts of the 2023
     CHI Conference on Human Factors in Computing Systems (pp. 1-7).

[59] Fuch, D., Hey, T., Keim, J., Liu, H., Ewald, N., Thirolf, T. and Kozi-
     olek, A., 2025. “LiSSA: Toward Generic Traceability Link Recovery through


                                          21
    Retrieval-Augmented Generation.” In ICSE ’25. https://dl.acm.org/doi/10.1109/
    ICSE55347.2025.00186.

[60] Gandhi, K., Chakravarthy, A., Singh, A., Lile, N. and Goodman, N.D., 2025.
     “Cognitive behaviors that enable self-improving reasoners, or, four habits of
     highly effective stars.” In Proceedings of the 2nd Conference on Language
     Modeling.

[61] Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, H.
     and Wang, H., 2023. Retrieval-augmented generation for large language models:
     A survey. arXiv preprint arXiv:2312.10997, 2(1), p.32.

[62] Genesereth, M.R. and Nilsson, N.J., 2012. Logical Foundations of Artificial
     Intelligence. Morgan Kaufmann.

[63] Gervasi, V., Gacitua, R., Rouncefield, M., Sawyer, P., Kof, L., Ma, L., Piwek,
     P., De Roeck, A., Willis, A., Yang, H. and Nuseibeh, B., 2013. Unpacking tacit
     knowledge for requirements engineering. In Managing requirements knowledge
     (pp. 23-47). Berlin, Heidelberg: Springer Berlin Heidelberg.

[64] Gheibi, O., Weyns, D. and Quin, F., 2021. “Applying machine learning in
     self-adaptive systems: A systematic literature review.” ACM Transactions on
     Autonomous and Adaptive Systems (TAAS), 15(3), pp.1-37.

[65] Glikson, E. and Woolley, A.W., 2020. “Human trust in artificial intelligence:
     Review of empirical research.” Academy of Management Annals, 14(2), pp.627-
     660.

[66] Gloaguen, T., Mündler, N., Müller, M., Raychev, V. and Vechev, M., 2026. “Eval-
     uating AGENTS.md: Are repository-level context files helpful for coding agents?”
     arXiv preprint arXiv:2602.11988.

[67] Gudaparthi, H., Niu, N., Wang, B., Bhowmik, T., Liu, H., Zhang, J., Savolainen,
     J., Horton, G., Crowe, S., Scherz, T. and Haitz, L., 2023, September. Prompting
     creative requirements via traceable and adversarial examples in deep learning.
     In 2023 IEEE 31st international requirements engineering conference (RE) (pp.
     134-145).

[68] Hadi, M.A. and Fard, F.H., 2023. “Evaluating pre-trained models for user feed-
     back analysis in software engineering: a study on classification of app-reviews.”
     Empirical Software Engineering. https://doi.org/10.1007/s10664-023-10314-x.

[69] Hey, T., Keim, J. and Corallo, S., 2024, June. Requirements classification
     for traceability link recovery. In 2024 IEEE 32nd International Requirements
     Engineering Conference (RE) (pp. 155-167).

[70] Hosseini, M.B., Heaps, J., Slavin, R., Niu, J. and Breaux, T., 2021, September.
     Ambiguity and generality in natural language privacy policies. In 2021 IEEE 29th
     International Requirements Engineering Conference (RE) (pp. 70-81).

[71] Howcroft, D.M., Belz, A., Clinciu, M., Gkatzia, D., Hasan, S.A., Mahamood, S.,
     Mille, S., Van Miltenburg, E., Santhanam, S. and Rieser, V., 2020, December.
     “Twenty years of confusion in human evaluation: NLG needs evaluation sheets



                                         22
    and standardised definitions.” In Proceedings of the 13th international conference
    on natural language generation (pp. 169-182).

[72] Huang, T., Kaulagi, V., Hosseini, M.B. and Breaux, T., 2023, September. Mobile
     application privacy risk assessments from user-authored scenarios. In 2023 IEEE
     31st International Requirements Engineering Conference (RE) (pp. 17-28).

[73] Huang, W., Xia, F., Xiao, T., Chan, H., Liang, J., Florence, P., Zeng, A., Tomp-
     son, J., Mordatch, I., Chebotar, Y. and Sermanet, P., 2022. Inner monologue:
     Embodied reasoning through planning with language models. arXiv preprint
     arXiv:2207.05608.

[74] Iqbal, T., Khan, M., Taveter, K. and Seyff, N., 2021, September. “Mining reddit
     as a new source for software requirements.” In 2021 IEEE 29th international
     requirements engineering conference (RE) (pp. 128-138).

[75] Jackson M. 1995. “The world and the machine”. In Proceedings of the 17th
     international conference on Software engineering (ICSE ’95).

[76] Jacobs, R.A., Jordan, M.I., Nowlan, S.J. and Hinton, G.E., 1991. “Adaptive
     mixtures of local experts.” Neural computation, 3(1), pp.79-87.

[77] Jahan, M., Hassan, M.M., Golpayegani, R., Ranjbaran, G., Roy, C., Roy, B.
     and Schneider, K., 2024, September. “Automated derivation of UML sequence
     diagrams from user stories: Unleashing the power of generative ai vs. a rule-based
     approach.” In Proceedings of the ACM/IEEE 27th International Conference on
     Model Driven Engineering Languages and Systems (pp. 138-148).

[78] Jain, C., Anish, P.R., Singh, A. and Ghaisas, S., 2023, September. A transformer-
     based approach for abstractive summarization of requirements from obligations
     in software engineering contracts. In 2023 IEEE 31st International Requirements
     Engineering Conference (RE) (pp. 169-179).

[79] Jain, N., Gu, A., Li, W.D., Yan, F., Zhang, T., Wang, S., Solar-Lezama, A.,
     Sen, K. and Stoica, I., 2025, May. Livecodebench: Holistic and contamination
     free evaluation of large language models for code. In International Conference on
     Learning Representations (Vol. 2025, pp. 58791-58831).

[80] Jakesch, M., Hancock, J.T. and Naaman, M., 2023. “Human heuristics for AI-
     generated language are flawed.” Proceedings of the National Academy of Sciences,
     120(11), p.e2208839120.

[81] Jiang, Y., Li, D., Deng, H., Ma, B., Wang, X., Wang, Q. and Yu, G.,
     2026. “SoK: Agentic Skills–Beyond Tool Use in LLM Agents.” arXiv preprint
     arXiv:2602.20867.

[82] Jimenez, C.E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O. and Narasimhan,
     K., 2024, May. Swe-bench: Can language models resolve real-world github issues?.
     In International Conference on Learning Representations (Vol. 2024, pp. 54107-
     54157).

[83] Jin, D., Jin, Z., Yang, Y., Li, L., Fang, Z., He, Y. Jing, W., and Chen, X. 2026.
     “From Chat to Interview: Agentic Requirements Elicitation with an Experience



                                          23
    Typology,” In the Proceedings of the 34th IEEEE International Conference on
    Requirements Engineering.

[84] Jordan, M.I. and Jacobs, R.A., 1994. “Hierarchical mixtures of experts and the
     EM algorithm.” Neural computation, 6(2), pp.181-214.

[85] KC, P., Ghandiparsi, R., Herron, T., Heaps, J. and Hosseini, M.B., 2025. Demys-
     tifying feature requests: Leveraging llms to refine feature requests in open-source
     software, In 2024 IEEE 32nd International Requirements Engineering Conference
     (RE).

[86] Kalliamvakou, E., Gousios, G., Blincoe, K., Singer, L., German, D.M. and
     Damian, D., 2016. “An in-depth study of the promises and perils of mining
     GitHub.” Empirical Software Engineering, 21(5), pp.2035-2071.

[87] Kandpal, N., Deng, H., Roberts, A., Wallace, E. and Raffel, C., 2023, July. Large
     language models struggle to learn long-tail knowledge. In International conference
     on machine learning (pp. 15696-15707). PMLR.

[88] Khojah, R., de Oliveira Neto, F.G., Mohamad, M. and Leitner, P., 2025.
     “The impact of prompt programming on function-level code generation.” IEEE
     Transactions on Software Engineering.

[89] Kim, G., Baldi, P. and McAleer, S., 2023. Language models can solve computer
     tasks. Advances in Neural Information Processing Systems, 36, pp.39648-39677.

[90] Klievtsova, N., Mangler, J., Kampik, T. and Rinderle-Ma, S., 2024, June. Utiliz-
     ing process models in the requirements engineering process through model2text
     transformation. In 2024 IEEE 32nd International Requirements Engineering
     Conference (RE) (pp. 205-217).

[91] Kojima, T., Gu, S.S., Reid, M., Matsuo, Y. and Iwasawa, Y., 2022. “Large lan-
     guage models are zero-shot reasoners.” Advances in neural information processing
     systems, 35, pp.22199-22213.

[92] Korn, A., Gorsch, S. and Vogelsang, A., 2025, September. LLMREI: Automating
     requirements elicitation interviews with LLMs. In 2025 IEEE 33rd International
     Requirements Engineering Conference (RE) (pp. 19-30).

[93] Koscinski, V., Hashemi, S. and Mirakhorli, M., 2023. “On-Demand Secu-
     rity Requirements Synthesis with Relational Generative Adversarial Networks.”
     In 2023 IEEE/ACM 45th International Conference on Software Engineering
     (ICSE). https://ieeexplore.ieee.org/document/10172729.

[94] Lanham, T., Chen, A., Radhakrishnan, A., Steiner, B., Denison, C., Her-
     nandez, D., Li, D., Durmus, E., Hubinger, E., Kernion, J. and Lukošiūtė,
     K., 2023. Measuring faithfulness in chain-of-thought reasoning. arXiv preprint
     arXiv:2307.13702.

[95] Le Sellier De Chezelles, T., Gasse, M., Lacoste, A., Drouin, A., Caccia, M.,
     Boisvert, L., Thakkar, M., Marty, T., Assouel, R., Shayegan, S.O. and Jang,
     L.K., 2025. The BrowserGym Ecosystem for Web Agent Research. Transactions
     on Machine Learning Research, 3(3835).



                                          24
[96] Lev-Ari, S. and Keysar, B., 2010. “Why don’t we believe non-native speakers?
     The influence of accent on credibility.” Journal of Experimental Social Psychology,
     46(6), pp.1093-1096.

[97] Li, G., Hammoud, H., Itani, H., Khizbullin, D. and Ghanem, B., 2023. Camel:
     Communicative agents for” mind” exploration of large language model society.
     Advances in neural information processing systems, 36, pp.51991-52008.

[98] Li, Z.S., Sihag, M., Arony, N.N., Junior, J.B., Phan, T., Ernst, N. and Damian,
     D., 2022, August. Narratives: the unforeseen influencer of privacy concerns. In
     2022 IEEE 30th International Requirements Engineering Conference (RE) (pp.
     127-139).

[99] Lian, X., Wang, S., Zou, H., Liu, F., Wu, J. and Zhang, L., 2025. “Incorporat-
     ing Verification Standards for Security Requirements Generation from Functional
     Specifications.” Proceedings of the ACM on Software Engineering. https://dl.
     acm.org/doi/10.1145/3729347.

[100] Liang, J.T., Lin, M., Rao, N. and Myers, B.A., 2025. “Prompts are programs too!
     understanding how developers build software containing prompts.” Proceedings
     of the ACM on Software Engineering, 2(FSE), pp.1591-1614.

[101] Liang, J.T., Yang, C., Sergeyuk, A., Breaux, T.D. and Myers, B.A., 2025.
     “Understanding prompt programming tasks and questions.” arXiv preprint
     arXiv:2507.17264.

[102] Lin, C.Y., 2004, July. “Rouge: A package for automatic evaluation of sum-
     maries.” In Text Summarization Branches Out (pp. 74-81).

[103] Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F. and
     Liang, P., 2024. “Lost in the middle: How language models use long contexts.”
     Transactions of the association for computational linguistics, 12, pp.157-173.

[104] Liu, S., Dehghan, S., Ganhotra, J., Hirzel, M. and Jabbarvand, R., 2026.
     “Evaluating plan compliance in autonomous programming agents.” Preprint.

[105] Liu, X., Yu, H., Zhang, H., Xu, Y., Lei, X., Lai, H., Gu, Y., Ding, H., Men,
     K., Yang, K. and Zhang, S., 2024, May. Agentbench: Evaluating llms as agents.
     In International Conference on Learning Representations (Vol. 2024, pp. 52989-
     53046).

[106] Liu, Y., Lin, J., Anuyah, O., Metoyer, R. and Cleland-Huang, J., 2022. “Gener-
     ating and visualizing trace link explanations.” In ICSE ’22. https://dl.acm.org/
     doi/10.1145/3510003.3510129.

[107] Lo Giudice, D., O’Grady, M., Gardner, C., Cornwall, A., Betz, C. “AI Is
     Evolving The Development Workforce In Dramatic Ways: Predictive, Generative,
     And Agentic AI Will Completely Change The SDLC,” Forrester Trend Report,
     October 29, 2025.

[108] Lopez, T., Petre, M. and Nuseibeh, B., 2012, June. “Getting at ephemeral
     flaws.” In 2012 5th International Workshop on Co-operative and Human Aspects
     of Software Engineering (CHASE) (pp. 90-92). IEEE.



                                          25
[109] Longpre, S., Hou, L., Vu, T., Webson, A., Chung, H.W., Tay, Y., Zhou, D.,
     Le, Q.V., Zoph, B., Wei, J. and Roberts, A., 2023, July. “The flan collection:
     Designing data and methods for effective instruction tuning.” In International
     Conference on Machine Learning (pp. 22631-22648).

[110] Lorch, R., Meng, B., Siu, K., Moitra, A., Durling, M., Paul, S., Varanasi, S.C. and
     McMillan, C., 2024, April. Formal methods in requirements engineering: Survey
     and future directions. In Proceedings of the 2024 IEEE/ACM 12th International
     Conference on Formal Methods in Software Engineering (FormaliSE) (pp. 88-99).

[111] Lu, M. and Liang, P., 2017, June. “Automatic classification of non-functional
     requirements from augmented app user reviews.” In Proceedings of the 21st Inter-
     national Conference on Evaluation and Assessment in Software Engineering (pp.
     344-353).

[112] Lüders, C.M., Pietz, T. and Maalej, W., 2022, August. Automated detection
     of typed links in issue trackers. In 2022 IEEE 30th International Requirements
     Engineering Conference (RE) (pp. 26-38).

[113] Lulla, J.L., Mohsenimofidi, S., Galster, M., Zhang, J.M., Baltes, S. and Treude,
     C., 2026. “On the impact of AGENTS.md files on the efficiency of AI coding
     agents.” In Proceedings of the ICSE Journal Ahead Workshop (JAWs ’26).

[114] Luo, X., Xue, Y., Xing, Z. and Sun, J., 2023. “PRCBERT: Prompt Learning for
     Requirement Classification using BERT-based Pretrained Language Models.” In
     ASE ’22. https://dl.acm.org/doi/10.1145/3551349.3560417.

[115] Luo, Y., Zhang, X.Y., Arcaini, P., Jin, Z., Zhao, H., Zhang, L. and Ishikawa, F.,
     2022, August. Hierarchical assessment of safety requirements for configurations
     of autonomous driving systems. In 2022 IEEE 30th International Requirements
     Engineering Conference (RE) (pp. 88-100).

[116] Luo, L., Zhao, Z., Haffari, G., Phung, D., Gong, C. and Pan, S., 2025, “Gfm-
     rag: Graph foundation model for retrieval augmented generation,” Advances in
     Neural Information Processing Systems (NeurIPS) 38.

[117] Ma, Q., Peng, W., Yang, C., Shen, H., Koedinger, K. and Wu, T., 2025. “What
     should we engineer in prompts? training humans in requirement-driven LLM use.”
     ACM Transactions on Computer-Human Interaction, 32(4), pp.1-27.

[118] Mallen, A., Asai, A., Zhong, V., Das, R., Khashabi, D. and Hajishirzi, H., 2023,
     July. “When not to trust language models: Investigating effectiveness of para-
     metric and non-parametric memories.” In Proceedings of the 61st annual meeting
     of the association for computational linguistics (volume 1: Long papers) (pp.
     9802-9822).

[119] Mavin, A., Wilkinson, P., Harwood, A. and Novak, M., 2009, August. Easy
     approach to requirements syntax (EARS). In 2009 17th IEEE international
     requirements engineering conference (pp. 317-322). IEEE.

[120] Maynez, J., Narayan, S., Bohnet, B. and McDonald, R., 2020, July. “On faith-
     fulness and factuality in abstractive summarization.” In Proceedings of the
     58th Annual Meeting of the Association for Computational Linguistics (pp.


                                           26
    1906-1919).

[121] Mekala, R.R., Irfan, A., Groen, E.C., Porter, A. and Lindvall, M., 2021,
     September. “Classifying user requirements from online feedback in small dataset
     environments using deep learning.” In 2021 IEEE 29th International requirements
     engineering conference (RE) (pp. 139-149)

[122] Mendoza, D., Mavridou, A., Katis, A. and Trippel, C., 2026. “Automating
     Requirements Formalization: Using LLMs and Low-Complexity Distin-
     guishing Traces for Semantic Validation.” Conference abstract page.
     https://conf.researchr.org/details/icse-2026/icse-2026-research-track/287/
     Automating-Requirements-Formalization-Using-LLMs-and-Low-Complexity-Distinguishing-T.

[123] Mohsenimofidi, S., Galster, M., Treude, C. and Baltes, S., 2026. “Context Engi-
     neering for AI Agents in Open-Source Software.” In 23rd International Conference
     on Mining Software Repositories (MSR ’26). https://doi.org/10.1145/3793302.
     3793350.

[124] Molenaar, S. and Dalpiaz, F., 2025, September. The impact of requirements
     artifacts on efficiency in agile development: a case study. In 2025 IEEE 33rd
     International Requirements Engineering Conference (RE) (pp. 68-79).

[125] Morishita, T., Morio, G., Yamaguchi, A. and Sogawa, Y., 2024. Enhancing rea-
     soning capabilities of llms via principled synthetic logic corpus. Advances in
     Neural Information Processing Systems, 37, pp.73572-73604.

[126] Motger, Q., Oriol, M., Tiessler, M., Franch, X. and Marco, J., 2025, September.
     What about emotions? guiding fine-grained emotion extraction from mobile app
     reviews. In 2025 IEEE 33rd International Requirements Engineering Conference
     (RE) (pp. 6-18).

[127] Mu, F., Shi, L., Wang, S., Yu, Z., Zhang, B., Wang, C., Liu, S. and Wang,
     Q., 2024. “ClarifyGPT: A Framework for Enhancing LLM-Based Code Gen-
     eration via Requirements Clarification.” Proceedings of the ACM on Software
     Engineering. https://dl.acm.org/doi/10.1145/3660810.

[128] Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim, C., Hesse, C., Jain,
     S., Kosaraju, V., Saunders, W. and Jiang, X., 2021. “WebGPT: Browser-assisted
     question-answering with human feedback.” arXiv preprint arXiv:2112.09332.

[129] Nayebi, M., Kuznetsov, K., Zeller, A. and Ruhe, G., 2023, September. User
     driven functionality deletion for mobile apps. In 2023 IEEE 31st International
     Requirements Engineering Conference (RE) (pp. 6-16).

[130] Nejati, S., Sabetzadeh, M., Chechik, M., Easterbrook, S. and Zave, P., 2007,
     May. “Matching and merging of statecharts specifications.” In 29th International
     Conference on Software Engineering (ICSE’07) (pp. 54-64). IEEE.

[131] Nistala, P.V., Rajbhoj, A., Kulkarni, V., Soni, S., Nori, K.V. and Reddy, R.,
     2022. “Towards digitalization of requirements: generating context-sensitive user
     stories from diverse specifications.” Automated Software Engineering. https://
     doi.org/10.1007/s10515-022-00324-2.




                                          27
[132] Nouri, A., Cabrero-Daniel, B., Törner, F., Sivencrona, H. and Berger, C.,
     2024, June. Engineering safety requirements for autonomous driving with large
     language models. In 2024 IEEE 32nd International Requirements Engineering
     Conference (RE) (pp. 218-228)

[133] Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang,
     C., Agarwal, S., Slama, K., Ray, A. and Schulman, J., 2022. 11Training lan-
     guage models to follow instructions with human feedback.” Advances in neural
     information processing systems, 35, pp.27730-27744.

[134] Palumbo, A. “Tech Layoffs Are Surpassing 2025 Levels. The Real Reason
     Companies Are Slashing Headcount.” BARRON’s, April 21, 2026.

[135] Pan, J., Wang, X., Neubig, G., Jaitly, N., Ji, H., Suhr, A. and Zhang, Y.,
     2025. “Training software engineering agents and verifiers with SWE-gym.” In
     International Conference on Machine Learning (ICML).

[136] Papineni, K., Roukos, S., Ward, T. and Zhu, W.J., 2002, July. “BLEU: a method
     for automatic evaluation of machine translation.” In Proceedings of the 40th
     annual meeting of the Association for Computational Linguistics (pp. 311-318).

[137] Patil, S.G., Zhang, T., Wang, X. and Gonzalez, J.E., 2024. Gorilla: Large
     language model connected with massive apis. Advances in Neural Information
     Processing Systems, 37, pp.126544-126565.

[138] Piskala, D.B., 2026. “Spec-Driven Development: From Code to Contract in the
     Age of AI Coding Assistants.” arXiv preprint arXiv:2602.00180.

[139] Pohl, K., 1996. Requirements engineering: An overview. Aachen: RWTH,
     Fachgruppe Informatik.

[140] Potts, C., Takahashi, K. and Anton, A.I., 1994. Inquiry-based requirements
     analysis. IEEE software, 11(2), pp.21-32.

[141] Pruitt, J. and Adlin, T., 2010. The Persona Lifecycle: Keeping People in Mind
     throughout Product Design. Elsevier.

[142] Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y., Lin, Y., Cong, X., Tang,
     X., Qian, B. and Zhao, S., 2024, May. Toolllm: Facilitating large language mod-
     els to master 16000+ real-world apis. In International Conference on Learning
     Representations (Vol. 2024, pp. 9695-9717).

[143] Rajbhoj, A., Nistala, P., Pathan, A., Kulkarni, P. and Kulkarni, V., 2023,
     September. RClassify: Combining NLP and ML to Classify Rules from Require-
     ments Specifications Documents. In 2023 IEEE 31st International Requirements
     Engineering Conference (RE) (pp. 180-189).

[144] Ravaut, M., Sun, A., Chen, N. and Joty, S., 2024, August. “On context uti-
     lization in summarization with large language models.” In Proceedings of the
     62nd Annual Meeting of the Association for Computational Linguistics (Volume
     1: Long Papers) (pp. 2764-2781).




                                         28
[145] Reber, R. and Schwarz, N., 1999. “Effects of perceptual fluency on judgments
     of truth.” Consciousness and Cognition, 8(3), pp.338-342.

[146] Reiter, E., 2018. “A structured review of the validity of BLEU.” Computational
     Linguistics, 44(3), pp.393-401.

[147] Rejithkumar, G. and Anish, P.R., 2025. “NICE: Non-Functional Requirements
     Identification, Classification, and Explanation Using Small Language Models.”
     In 2025 IEEE/ACM 47th International Conference on Software Engineer-
     ing: Software Engineering in Practice (ICSE-SEIP). https://ieeexplore.ieee.org/
     document/11121724.

[148] Reubenstein, H. B., Waters, R. C. “The Requirements Apprentice: Auto-
     mated Assistance for Requirements Acquisition,” IEEE Transactions on Software
     Engineering, 17(3): 226-240, 1991.

[149] Reynolds, L. and McDonell, K., 2021, May. “Prompt programming for large
     language models: Beyond the few-shot paradigm.” In Extended Abstracts of the
     2021 CHI Conference on Human Factors in Computing Systems (pp. 1-7).

[150] Rich, C., 1991. “Cake: An implemented hybrid knowledge representation and
     limited reasoning system.” ACM SIGART Bulletin, 2(3), pp.120-127.

[151] Royce, W.W. “Managing the Development of Large Software Systems,” IEEE
     WESCON, 1970 pp. 1-9

[152] Ryan, K., 1993, January. “The role of natural language in requirements engi-
     neering.“ In Proceedings of the IEEE International Symposium on Requirements
     Engineering (pp. 240-242).

[153] Ryu, H., Kim, G., Lee, H.S. and Yang, E., 2025, May. “Divide and translate:
     Compositional first-order logic translation and verification for complex logical
     reasoning.” In International Conference on Learning Representations (Vol. 2025,
     pp. 24935-24964).

[154] Saini, R., Mussbacher, G., Guo, J.L. and Kienzle, J., 2021, September. Auto-
     mated traceability for domain modelling decisions empowered by artificial intel-
     ligence. In 2021 IEEE 29th International Requirements Engineering Conference
     (RE) (pp. 173-184).

[155] Santos, S., Breaux, T., Norton, T., Haghighi, S. and Ghanavati, S., 2024,
     June. Requirements satisfiability with in-context learning. In 2024 IEEE 32nd
     International Requirements Engineering Conference (RE) (pp. 168-179).

[156] Sawyer, P., Gervasi, V. and Nuseibeh, B., 2011, August. “Unknown knowns:
     Tacit knowledge in requirements engineering.” In 2011 IEEE 19th International
     Requirements Engineering Conference (pp. 329-329).

[157] Schick, T., Dwivedi-Yu, J., Dessı̀, R., Raileanu, R., Lomeli, M., Hambro, E.,
     Zettlemoyer, L., Cancedda, N. and Scialom, T., 2023. Toolformer: Language mod-
     els can teach themselves to use tools. Advances in neural information processing
     systems, 36, pp.68539-68551.




                                         29
[158] Schwaber, K. and Beedle, M., 2001. “Agile software development with Scrum.”
     Prentice Hall PTR.

[159] Sclar, M., Choi, Y., Tsvetkov, Y. and Suhr, A., 2024, May. Quantifying Language
     Models’ Sensitivity to Spurious Features in Prompt Design or: How I learned to
     start worrying about prompt formatting. In International Conference on Learning
     Representations (Vol. 2024, pp. 25055-25083).

[160] Sharfuddin, A. and Breaux, T., 2025, September. Generative goal modeling. In
     2025 IEEE 33rd International Requirements Engineering Conference (RE) (pp.
     92-103).

[161] Shen, Y., Singhal, A. and Breaux, T., 2025, September. Requirements elicitation
     follow-up question generation. In 2025 IEEE 33rd International Requirements
     Engineering Conference (RE) (pp. 117-129).

[162] Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K. and Yao, S., 2023. Reflex-
     ion: Language agents with verbal reinforcement learning. Advances in neural
     information processing systems, 36, pp.8634-8652.

[163] Sihag, M., Li, Z.S., Dash, A., Arony, N.N., Devathasan, K., Ernst, N., Albu, A.B.
     and Damian, D., 2023, September. A data-driven approach for finding require-
     ments relevant feedback from tiktok and youtube. In 2023 IEEE 31st International
     Requirements Engineering Conference (RE) (pp. 111-122).

[164] Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R. and Gal,
     Y., 2024. AI models collapse when trained on recursively generated data. Nature,
     631(8022), pp.755-759.

[165] Sprague, Z., Yin, F., Rodriguez, J., Jiang, D., Wadhwa, M., Singhal, P., Zhao,
     X., Ye, X., Mahowald, K. and Durrett, G., 2025, May. “To CoT or not to CoT?
     Chain-of-thought helps mainly on math and symbolic reasoning.” In International
     Conference on Learning Representations (Vol. 2025, pp. 94118-94162).

[166] Stanik, C., Pietz, T. and Maalej, W., 2021, September. Unsupervised topic
     discovery in user comments. In 2021 IEEE 29th International Requirements
     Engineering Conference (RE) (pp. 150-161).

[167] Sun, H., Zeng, S. and Zhang, B., 2026, March. H-mem: Hierarchical memory for
     high-efficiency long-term reasoning in llm agents. In Proceedings of the 19th Con-
     ference of the European Chapter of the Association for Computational Linguistics
     (Volume 1: Long Papers) (pp. 341-350).

[168] Tan, S., Zhuang, S., Montgomery, K., Tang, W., Cuadron, A., Wang, C., Popa,
     R. and Stoica, I., 2025, May. Judgebench: A benchmark for evaluating llm-based
     judges. In International Conference on Learning Representations (Vol. 2025, pp.
     63277-63303).

[169] ter Beek, M.H., Chapman, R., Cleaveland, R., Garavel, H., Gu, R., Ter Horst,
     I., Keiren, J.J., Lecomte, T., Leuschel, M., Rozier, K.Y. and Sampaio, A., 2024.
     “Formal methods in industry.” Formal Aspects of Computing, 37(1), pp.1-38.




                                          30
[170] Tefur, A.E.M., Fotrousi, F., Ferrari, A., Spoletini, P., Maalej, W. 2026. “Debug-
     ging Requirements Interview Scripts: A Framework for Quality Assessment,” In
     the Proceedings of the 34th IEEEE International Conference on Requirements
     Engineering.

[171] Tian, Z. and Chen, J., 2025. “Aligning Requirement for Large Language Model’s
     Code Generation.” arXiv preprint arXiv:2509.01313. http://arxiv.org/abs/2509.
     01313.

[172] Tizard, J., Devine, P., Wang, H. and Blincoe, K., 2023. “A Software Require-
     ments Ecosystem: Linking Forum, Issue Tracker, and FAQs for Requirements
     Management.” IEEE Transactions on Software Engineering. https://ieeexplore.
     ieee.org/document/9940985.

[173] Turpin, M., Michael, J., Perez, E. and Bowman, S., 2023. Language models
     don’t always say what they think: Unfaithful explanations in chain-of-thought
     prompting. Advances in Neural Information Processing Systems, 36, pp.74952-
     74965.

[174] Ullrich, J., Koch, M. and Vogelsang, A., 2025, September. “From requirements to
     code: Understanding developer practices in LLM-assisted software engineering.”
     In 2025 IEEE 33rd International Requirements Engineering Conference (RE)
     (pp. 257-266). IEEE.

[175] Van Lamsweerde, A. and Letier, E., 2000. “Handling obstacles in goal-oriented
     requirements engineering.” IEEE Transactions on Software Engineering, 26(10),
     pp.978-1005.

[176] Vaithilingam, P., Zhang, T. and Glassman, E.L., 2022, April. “Expectation vs.
     experience: Evaluating the usability of code generation tools powered by large
     language models.” In CHI Conference on Human Factors in Computing Systems
     Extended Abstracts (pp. 1-7).

[177] Veizaga, A., Shin, S.Y. and Briand, L.C., 2023. “Automated Smell Detec-
     tion and Recommendation in Natural Language Requirements.” arXiv preprint
     arXiv:2305.07097. http://arxiv.org/abs/2305.07097.

[178] Vogelsang, A., Korn, A., Broccia, G., Ferrari, A., Fischbach, J. and Arora,
     C., 2025. “On the Impact of Requirements Smells in Prompts: The Case of
     Automated Traceability.” In 2025 IEEE/ACM 47th International Conference on
     Software Engineering: New Ideas and Emerging Results (ICSE-NIER). https:
     //dl.acm.org/doi/10.1109/ICSE-NIER66352.2025.00016.

[179] Voria, G., Casillo, F., Gravino, C., Catolino, G. and Palomba, F., 2025.
     “RECOVER: Toward Requirements Generation From Stakeholders’ Conversa-
     tions.” IEEE Transactions on Software Engineering. https://ieeexplore.ieee.org/
     document/11008757/.

[180] Wang, Q., Fu, Y., Cao, Y., Wang, S., Tian, Z. and Ding, L., 2025. “Recur-
     sively summarizing enables long-term dialogue memory in large language models.”
     Neurocomputing, 639, p.130193.




                                          31
[181] Wang, X., Huang, J., Ye, C. and Zhou, H., 2024, June. Globaltagnet: A graph-
     based framework for multi-label classification in github issues. In 2024 IEEE 32nd
     International Requirements Engineering Conference (RE) (pp. 67-78).

[182] Wang, X., Li, B., Song, Y., Xu, F.F., Tang, X., Zhuge, M., Pan, J., Song, Y., Li,
     B., Singh, J. and Tran, H., 2025, May. “OpenHands: An open platform for ai soft-
     ware developers as generalist agents.” In International Conference on Learning
     Representations (Vol. 2025, pp. 65882-65919).

[183] Wang, J., Wang, J., Athiwaratkun, B., Zhang, C. and Zou, J.Y., 2025, May.
     Mixture-of-agents enhances large language model capabilities. In International
     Conference on Learning Representations (Vol. 2025, pp. 33944-33963).

[184] Wei, J., Courbis, A.L., Lambolais, T., Xu, B., Bernard, P.L., Dray, G. and
     Maalej, W., 2024. “Getting Inspiration for Feature Elicitation: App Store- vs.
     LLM-based Approach.” In ASE ’24. https://dl.acm.org/doi/10.1145/3691620.
     3695591.

[185] Wei, J., Ebrahimi Pourasad, A. and Maalej, W., 2026. “LikeThis! Empowering
     App Users to Submit UI Improvement Suggestions Instead of Complaints.” arXiv
     preprint. doi: 10.1145/3744916.3787834. http://arxiv.org/abs/2603.04245.

[186] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V. and
     Zhou, D., 2022. “Chain-of-thought prompting elicits reasoning in large language
     models.” Advances in neural information processing systems, 35, pp.24824-24837.

[187] Wei, J., Bosma, M., Zhao, V.Y., Guu, K., Yu, A.W., Lester, B., Du, N., Dai,
     A.M. and Le, Q.V., 2022. “Finetuned language models are zero-shot learners.” In
     International Conference on Learning Representations.

[188] Wu, Y., Jiang, A.Q., Li, W., Rabe, M., Staats, C., Jamnik, M. and Szegedy,
     C., 2022. “Autoformalization with large language models.” Advances in Neural
     Information Processing Systems, 35, pp.32353-32368.

[189] Wu, Z., Chen, X., Jin, Z., Hu, M. and Jin, D., 2026.
     “Unlocking      the     Silent     Needs:     Business-Logic-Driven     Iterative
     Requirements      Auto-completion.”     Conference    abstract    page.    https:
     //conf.researchr.org/details/icse-2026/icse-2026-research-track/68/
     Unlocking-the-Silent-Needs-Business-Logic-Driven-Iterative-Requirements-Auto-complet.

[190] Xia, C.S., Deng, Y., Dunn, S. and Zhang, L., 2024. “Agentless: Demystifying
     LLM-based software engineering agents.” In Proceedings of the ACM on Software
     Engineering, Volume 2, Issue FSE, Article No.: FSE037, Pages 801 - 824

[191] Xia, C.S., Wang, Z., Yang, Y., Wei, Y. and Zhang, L., 2025. Live-SWE-
     agent: Can Software Engineering Agents Self-Evolve on the Fly?. arXiv preprint
     arXiv:2511.13646.

[192] Xie, T., Zhang, D., Chen, J., Li, X., Zhao, S., Cao, R., Hua, T.J., Cheng, Z.,
     Shin, D., Lei, F. and Liu, Y., 2024. Osworld: Benchmarking multimodal agents for
     open-ended tasks in real computer environments. Advances in Neural Information
     Processing Systems, 37, pp.52040-52094




                                          32
[193] Yang, J., Jimenez, C.E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K. and
     Press, O., 2024. “SWE-agent: Agent-computer interfaces enable automated soft-
     ware engineering.” Advances in Neural Information Processing Systems, 37,
     pp.50528-50652.

[194] Yang, J., Lieret, K., Jimenez, C., Wettig, A., Khandpur, K., Zhang, Y., Hui, B.,
     Press, O., Schmidt, L. and Yang, D., 2026. “SWE-smith: Scaling data for software
     engineering agents.” Advances in Neural Information Processing Systems, 38.

[195] Yao, S., Shinn, N., Razavi, P. and Narasimhan, K., 2025. τ -bench: A Benchmark
     for Tool-Agent-User Interaction in Real-World Domains. International Conference
     on Learning Representations (ICLR).

[196] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. and Cao, Y., 2023.
     “ReAct: Synergizing reasoning and acting in language models.” In International
     Conference on Learning Representations.

[197] Yu, Y., Wang, Y., Mylopoulos, J., Liaskos, S., Lapouchnian, A. and do Prado
     Leite, J.C.S., 2005, August. “Reverse engineering goal models from legacy code.”
     In 13th IEEE International Conference on Requirements Engineering (RE’05)
     (pp. 363-372). IEEE.

[198] Zelikman, E., Wu, Y., Mu, J. and Goodman, N., 2022. “Star: Bootstrapping
     reasoning with reasoning.” Advances in Neural Information Processing Systems,
     35, pp.15476-15488.

[199] Zhang, L., He, S., Zhang, C., Kang, Y., Li, B., Xie, C., Wang, J., Wang, M.,
     Huang, Y., Fu, S. and Nallipogu, E., 2026. “SWE-bench goes live!” Advances in
     Neural Information Processing Systems, 38.

[200] Zhang, S., Gotti, F., Mo, F. and Nie, J.Y., 2025. “Measuring the Impact of
     Lexical Training Data Coverage on Hallucination Detection in Large Language
     Models.” arXiv preprint arXiv:2511.17946.

[201] Zhang, X.F., Mohananey, A., Chronopoulou, A., Papalampidi, P., Gupta, S.,
     Munkhdalai, T., Wang, L. and Upadhyay, S., 2025. “Do LLMs Really Need 10+
     Thoughts for Find the Time 1000 Days Later? Towards Structural Understanding
     of LLM Overthinking.” arXiv preprint arXiv:2510.07880.

[202] Zheng, L., Chiang, W.L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z.,
     Li, Z., Li, D., Xing, E. and Zhang, H., 2023. Judging llm-as-a-judge with mt-
     bench and chatbot arena. Advances in neural information processing systems, 36,
     pp.46595-46623.

[203] Zhou, C., Liu, P., Xu, P., Iyer, S., Sun, J., Mao, Y., Ma, X., Efrat, A., Yu, P., Yu,
     L. and Zhang, S., 2023. “Lima: Less is more for alignment.” Advances in Neural
     Information Processing Systems, 36, pp.55006-55021.

[204] Zhou, S., Xu, F.F., Zhu, H., Zhou, X., Lo, R., Sridhar, A., Cheng, X., Ou, T.,
     Bisk, Y., Fried, D. and Alon, U., 2024, May. Webarena: A realistic web environ-
     ment for building autonomous agents. In International Conference on Learning
     Representations (Vol. 2024, pp. 15585-15606).




                                            33
