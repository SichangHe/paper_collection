                                           AI Chains: Transparent and Controllable Human-AI Interaction
                                                   by Chaining Large Language Model Prompts
                                                          Tongshuang Wu∗                                                 Michael Terry                                   Carrie J. Cai
                                                  wtshuang@cs.washington.edu                                      michaelterry@google.com                              cjcai@google.com
                                                    University of Washington                                          Google Research                                   Google Research
                                                              USA                                                           USA                                              USA
                                         ABSTRACT                                                                                    1   INTRODUCTION
                                         Although large language models (LLMs) have demonstrated im-                                 Large language models (LLMs) have introduced new possibilities for
                                         pressive potential on simple tasks, their breadth of scope, lack of                         human-AI collaboration [10]. Pretrained on billions of inputs from
arXiv:2110.01691v3 [cs.HC] 17 Mar 2022




                                         transparency, and insufficient controllability can make them less ef-                       the Internet [29], generative models like GPT-3 can now perform a
                                         fective when assisting humans on more complex tasks. In response,                           wide variety of tasks [10], ranging from translation [12], to question
                                         we introduce the concept of Chaining LLM steps together, where the                          answering [47], and even advanced story writing [60]. These suc-
                                         output of one step becomes the input for the next, thus aggregating                         cesses are enabled by their ability to adapt to desired tasks purely
                                         the gains per step. We first define a set of LLM primitive operations                       using prompts, or natural language descriptions of the tasks [55].
                                         useful for Chain construction, then present an interactive system                           For example, one could adapt an LLM to act as a translation engine,
                                         where users can modify these Chains, along with their intermedi-                            simply by providing a few examples of the desired inputs and out-
                                         ate results, in a modular way. In a 20-person user study, we found                          puts: “English: How are you? French: Comment allez-vous? English:
                                         that Chaining not only improved the quality of task outcomes, but                           Hello! French:” Based on this prompt, the model is likely to follow
                                         also significantly enhanced system transparency, controllability,                           the pattern to output the correct French translation: “Bonjour!”
                                         and sense of collaboration. Additionally, we saw that users devel-                             The relative ease of natural-language-based prompt program-
                                         oped new ways of interacting with LLMs through Chains: they                                 ming suggests that LLMs may be useful assistants for real-world
                                         leveraged sub-tasks to calibrate model expectations, compared and                           tasks, with users customizing the models to their own needs. In
                                         contrasted alternative strategies by observing parallel downstream                          this light, recent work in Natural Language Processing (NLP) has
                                         effects, and debugged unexpected model outputs by “unit-testing”                            begun to examine the algorithmic capabilities of LLMs, mostly on
                                         sub-components of a Chain. In two case studies, we further explore                          synthesized tasks [26, 55, 66]. However, many real-world tasks can
                                         how LLM Chains may be used in future applications.                                          be quite complex (e.g., outlining long essays, debugging software
                                                                                                                                     code), and may present challenges for current LLMs to solve from
                                         CCS CONCEPTS                                                                                a single model run. For example, as LLMs learn the forms of lan-
                                                                                                                                     guage [7], they produce lower quality outputs when solving tasks
                                         • Human-centered computing → Empirical studies in HCI;
                                                                                                                                     that require multi-step reasoning [11, 61, 67]. Likewise, they may
                                         Interactive systems and tools; • Computing methodologies →
                                                                                                                                     fail to capture the subtleties of many tasks that involve multiple
                                         Machine learning.
                                                                                                                                     objectives simultaneously (e.g., identifying and fixing multiple bugs
                                                                                                                                     in a code snippet). Figure 1 shows a task involving multiple con-
                                         KEYWORDS                                                                                    current objectives: (1) to rewrite peer feedback to be more friendly,
                                         Human-AI Interaction, Large Language Models, Natural Language                               and (2) to rewrite it with additional concrete suggestions, and (3)
                                         Processing                                                                                  to ensure that each noted sub-problem (e.g., too many words on
                                                                                                                                     slides, presentation meaders, does not engage with audience) is
                                         ACM Reference Format:
                                                                                                                                     addressed. While an LLM can both generate suggestions [1] and
                                         Tongshuang Wu, Michael Terry, and Carrie J. Cai. 2022. AI Chains: Trans-
                                                                                                                                     adjust the tone in isolation (e.g., in [3]), it lacks the capability to
                                         parent and Controllable Human-AI Interaction by Chaining Large Language
                                         Model Prompts. In CHI Conference on Human Factors in Computing Systems                      perform both tasks together well in an end-to-end manner. As a
                                         (CHI ’22), April 29-May 5, 2022, New Orleans, LA, USA. ACM, New York, NY,                   result, it produces a mediocre paragraph that only meets a few
                                         USA, 22 pages. https://doi.org/10.1145/3491102.3517582                                      requirements (see output of Figure 1A).
                                                                                                                                        Besides being inherently limited for complex problems, LLMs
                                                                                                                                     are also difficult to interact and collaborate with, as they can be
                                         ∗ The work was done when the author was an intern at Google Inc.
                                                                                                                                     opaque and hard to debug. Since LLMs can take in any natural
                                                                                                                                     language prompts, end users may struggle to determine how to
                                                                                                                                     change their prompts to remedy unexpected model outputs. They
                                         Permission to make digital or hard copies of part or all of this work for personal or       may also have difficulties developing accurate mental models of an
                                         classroom use is granted without fee provided that copies are not made or distributed
                                         for profit or commercial advantage and that copies bear this notice and the full citation   LLM’s capabilities and limitations. There are no obvious edits on
                                         on the first page. Copyrights for third-party components of this work must be honored.      the prompt that can, for instance, encourage the model to add more
                                         For all other uses, contact the owner/author(s).
                                                                                                                                     suggestions regarding “too much text on slides” in Figure 1A.
                                         CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA
                                         © 2022 Copyright held by the owner/author(s).                                                  In this work, we introduce the notion of Chaining multiple LLM
                                         ACM ISBN 978-1-4503-9157-3/22/04.                                                           prompts together, to help users accomplish complex tasks with
                                         https://doi.org/10.1145/3491102.3517582
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                           Tongshuang Wu, Michael Terry, and Carrie J. Cai


      Original feedback
      Alex could improve his presentation skills. He has too much text on his slides. His presentation meanders                           Data layer
      from topic to topic without a clear structure. He also does not engage with his audience when he presents.


                           A NO-CHAINING                  Split points      b1                                 B CHAINING
                                                                                             Suggestions for improvement                LLM operation
             Direct rewriting                                                      b2
                                                       Alex’s problems                       More images on the slides




                                                                                  Ideation
  Given the following feedback,                        Too much text...
  rewrite it into a friendly paragraph                                                       Sectionalize the talk
  with concrete suggestions for each                   No clear structure                                                                 LLM step
  of Alex’s presentation problems                                                            Ask the audience questions
                                                       Does not engage...
  Original feedback:                                                                         Use humor
  [Original feedback text — see above
  More friendly feedback:
  [Model output — see below]

                                                       Compose points       b3

    Friendly paragraph                                Friendly paragraph
     Alex, you have too many words on                 Alex, your presentation was interesting! However, I noticed that
     your slides. You should use                      you have a lot of information on your slides. It might be
     images and bullet points to help
     get your message across. You
                                                      helpful to vary pictures with text so that it is easier to
                                                      follow. Also, you might consider the flow of your theme. If it
                                                                                                                           B
     should have a clear structure                    were me, I would have divided it into three sections and then
     for the presentation. You should                 used your conclusion at the end. You may also want to add some
     also engage with your audience.                  humor, and ask more questions to engage the audience.



Figure 1: A walkthrough example illustrating the differences between no-Chaining (A) and Chaining (B), using the example
task of writing a peer review to be more constructive. With a single call to the model in (A), even though the prompt (italicized)
clearly describes the task, the •generated paragraph remains mostly impersonal and does not provide concrete suggestions for
all 3 of Alex’s presentation problems. In (B), we instead use an LLM Chain with three steps, each for a distinct sub-task: (b1)
A Split points step that extracts each individual presentation •problem from the •original feedback, (b2) An Ideation step that
brainstorms •suggestions per problem, and (b3) A Compose points step that synthesizes all the problems and suggestions into
a final •friendly paragraph. The result is noticeably improved.

LLMs in a way that is more transparent and debuggable. Chaining                  default prompting and data structures. They help inform what types
takes advantage of LLMs’ unique ability to handle a variety of                   of sub-tasks could be used within a Chain, as well as how those
independent tasks. In a Chain, a problem is broken down into a                   steps can feed into each other.
number of smaller sub-tasks, each mapped to a distinct step with
                       
              .
   ]

                                                                                     To evaluate the impact of Chaining on both task performance
a corresponding natural language prompt; results of one or more                  and user experience, we conducted a within-subject user study, in
previous steps are aggregated in the next step’s input prompt. Thus,             which 20 participants completed tasks using both Chaining and a
Chaining enables users to run the same model on multiple sub-tasks,              standard (non-Chaining) interface, with the same underlying LLM
thereby granting each sub-task a higher likelihood of success (as                powering all the steps in the Chaining interface, as well as the
opposed to solving the entire task in one go). In Figure 1B, while               non-Chaining one. Our results show that Chaining significantly im-
the underlying LLM remains the same, by splitting (i.e.,, extracting)            proved key dimensions of the human-AI experience: transparency,
presentation problems (𝑏 1 ) and ideating suggestions per problem                controllability, collaboration, and mental support. In addition, par-
(𝑏 2 ), the final composed paragraph (𝑏 3 ) is more comprehensive in             ticipants also achieved higher-quality outcomes ∼82% of the time
addressing all problems, and has a more constructive tone.                       using Chaining. We also saw participants leveraging Chaining for
    In addition to potentially improving outcomes, Chaining opens                purposes beyond immediate task accomplishment — they calibrated
up new channels for fine-grained human feedback and control. For                 their expectations of the model using the smaller scope of sub-tasks,
example, thanks to the separate Ideation step in Figure 1𝑏 2 , Chain-            explored alternative prompting strategies by comparing parallel
ing allows users to customize which suggestions to include in the                downstream effects, and debugged unexpected model output by
final paragraph, an operation that is unavailable without Chaining               isolating and “unit-testing” different parts of a Chain. Critically,
(Figure 1A). We develop an interactive interface to expose these                 these improvements were achieved without changing the model
additional “knobs” to end users. The interface visualizes the Chain              itself. These findings suggest that one way to improve the explain-
structure, and allows users to customize a Chain at various levels:              ability and debuggability of an otherwise opaque, black-box LLM
they can iterate on the local prompts in each step, edit interme-                is to have it do less: breaking a problem up into smaller problems,
diate data between steps, or modify the entire Chain. To inform                  having the model solve each (smaller) problem separately, showing
the design of this tool, we surveyed 73 existing LLM use cases and               the intermediate results, and allowing users to edit those results.
summarized them into a set of LLM primitive operations, each with
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                               CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA


    The ability to chain LLM calls using a set of Chaining building             Despite their versatility, LLMs require careful prompt design.
blocks, within an interactive interface, collectively represents a          Various studies therefore focus on prompt engineering [9, 43, 45]. As
novel method and system for prototyping new AI-powered tasks                manual prompting can be sub-optimal, some work automatically
and features using LLMs. We conclude the paper with case studies            mines more effective prompts. However, the mined prompts tend
illustrating how Chaining can support more diverse applications             to be less human-readable [58] and therefore less compatible with
in the future, as well as insights into challenges and opportunities        human-AI interaction. Conversely, strategies like progressive gen-
that arose from our experiments. In summary, we contribute:                 eration (i.e., multi-round text expansion) [61] and meta-prompting
• We introduce the notion of LLM Chaining. Through a series                 (i.e., asking the model to elaborate on the problem) [9, 55] attempt
    of chained model calls, each targeting a small and well-scoped          to seed LLMs to generate more effective prompts before solving
    sub-task, we adapt a single LLM to contribute to multiple sub-          the task. In essence, these approaches also adopt the spirit of multi-
    components of a task.                                                   step problem solving, but focus on expanding the context without
• We design and implement building blocks for constructing and              human intervention. Our work defines Chaining more comprehen-
    interacting with LLM Chains. These include a set of primitive           sively, with primitive operations that illustrate LLM capabilities,
    LLM operations representing functions well-scoped for a single          LLM steps that can add or remove information along the Chain,
    model run, and an interactive interface that displays the intra-        and editable intermediate data points.
    and inter-step structures of a Chain. Users can run Chains step-
    by-step, and customize them at various granularities (editing           2.2     Human-AI Collaboration
    intermediate model outputs, rewiring steps, etc.).                      Human-AI interaction has been explored in domains such as clas-
• We report results from a 20-person evaluation that shows Chain-           sification [6, 59], drawing [24, 52], translation [28], creative writ-
    ing can increase system transparency, controllability, and task         ing [23, 27], and design ideation [36]. Prior work has noted core
    outcomes. Importantly, these gains are achieved without any             challenges of the interaction, such as a lack of transparency, con-
    changes to the underlying model. Combined with the case stud-           trollability, and user agency [5, 13, 31]. Through Chaining, we aim
    ies, we demonstrate the potential of improving explainability           to address these user-centered concerns.
    and debuggability of LLMs through task decomposition and                    In a collaboration, AI can play various roles, such as casual cre-
    finer-grained application of LLM models.                                ators that encourage exploration [24] or assistants that compensate
    Taken together, our findings inform the design and research             for human weaknesses [39, 70]. For example, Gero et al. [27] showed
of future human-LLM collaborative systems, an area of critical              that generators could serve as cognitive offloading tools so that
importance in years to come.                                                humans could focus their attention where it is needed most, a core
                                                                            motivation that we also share. Cai et al. [16] investigated how a
2 BACKGROUND AND RELATED WORK                                               medical AI can assist with doctors’ decision-making process during
                                                                            prostate cancer diagnosis, by helping them compare and contrast
2.1 Large Language Models                                                   similar images. Most of these studies, however, use task-specific
A generative language model is primarily designed to continue its           models, and therefore limit observations to human interaction with
input with plausible output (e.g., given a prompt “I went to the”,          AI that primarily serves one function, or in one domain (e.g., writ-
it might auto-complete with “coffee shop”). However, when pre-              ing, medicine, music, etc.). DuetDraw [52] may be an exception to
trained on billions of samples from the Internet, recent transformer-       this, as it uses several models, each of which supports a different
based LLMs [64] like GPT-3 [12] and Jurassic-1 [40] encode enough           co-drawing functionality. Rather than training multiple models for
information to support additional in-context learning: they can be          different tasks, or using a single model for a single type of task, our
easily customized at run time (without any re-training needed)              work explores how a single large language model (with inherently
to handle new tasks beyond text continuation. To invoke the de-             customizable capabilities) can support humans in a variety of sub-
sired functionality, users write natural language instructions, or          tasks. Finally, the closest work to ours might be online interfaces
prompts [9, 43, 45], that are appropriate for the task. The most            for users to interactively create prompts1 , or interfaces enabling
common patterns for prompting are either zero-shot or few-shot              users to perform natural language programming of code using a
prompts. Zero-shot prompts directly describe what ought to happen           large language model [32]. These systems used prompt engineer-
in a task. For example, we can enact English-to-French translation          ing to create a set of programming-related functionality for users.
with a prompt such as “Translate the sentence “Do you like the              While this prior work focused on single prompts, our work looks
weather?” to French:”. In contrast, few-shot prompts show the LLM           at how Chaining multiple prompts can address a much wider range
what pattern to follow by feeding it examples of desired inputs and         of human tasks, and evaluate its effects on user experience.
outputs: “[English] Hello! [French] Bonjour! [English] Do you like
the weather? [French]”. Given either of these prompts, the LLM may          2.3     Workflows in Crowdsourcing
respond with the French translation “Vous aimez le temps?” [33].
                                                                            Though less prevalent in human-AI collaboration, the concept of
Importantly, such task customization happens on the fly and, as
                                                                            Chaining is inspired by concepts of “pipelining” and “microtasking,”
a result, a single LLM can be flexibly adapted to a wide variety of
                                                                            which have long been used in crowdsourcing [15, 62]. In crowd-
use cases like code generation, question answering, creative writ-
                                                                            sourcing, requesters break down complex tasks into pieces that
ing, etc. [12, 60]. This flexible adaptation, together with the text-in,
                                                                            can be performed independently, then combined [22, 34, 38, 54].
text-out structure, creates an intuitive natural language interface
between humans and the model.                                               1 https://gpt3demo.com/apps/openai-gpt-3-playground
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                  Tongshuang Wu, Michael Terry, and Carrie J. Cai


Previous research shows that decomposed tasks allow the comple-          may help overcome those challenges by scoping the inputs/outputs
tion process to become more structured [21] and more resilient to        to be more amenable to what an LLM can handle.
interruptions [20], something we also witness in our user study.
The goal of crowd workflows is typically to address and safeguard        3.1    LLM Challenges & Primitive Operations
against the limitations of a typical worker. For example, Bernstein et   Existing literature exposes three main challenges that LLMs face:
al. [8] ensured text editing quality through a Find-Fix-Verify work-
flow, which modulates the scope of sub-tasks to reduce variance of         C.1 LLMs lack multi-step reasoning capabilities. Because
crowdworker effort. Meanwhile, Context Trees [65] hierarchically               LLMs are designed to grasp the form of language, rather
summarize and trim the otherwise overwhelming global contexts,                 than the meaning [7], they can struggle on tasks like se-
making them compact enough for a single worker to digest.                      quential arithmetic problems, multi-hop question answering,
    Our Chaining approach also aims to address pitfalls of a single            recognizing and comparing sentences, or those that require
LLM pass, but the pitfalls are somewhat distinct. While crowdsourc-            branching logic [9, 11, 26, 66, 67].
ing focuses more on cognitive load and task duration — factors             C.2 LLMs suffer from exposure bias [53, 61]. Because LLMs
that can affect the performance of human workers [37] — for LLMs               generate text sequentially in an autoregressive manner (the
with intensive computing power, their limitations err towards a                tokens generated by the models are themselves used to
lack of reasoning abilities, high variance of prompt effectiveness,            predict the next word), errors or imperfections from pre-
and exposure bias. A thorough analysis of these AI issues is needed            vious runs can accumulate. Thus, LLMs are less likely to
for constructing and chaining LLM steps, which we illustrate in                perform well when generating long bodies of text. Exposure
Section 3.1, and address through the design of primitive operations            bias can also cause LLMs to produce redundant content, in
in Table 2. Through user studies (Section 5) and case studies (Sec-            some severe cases repeating the same phrase over and over
tion 6), we demonstrate that Chaining can effectively address these            again [30, 68]. As a result, they struggle to generate text with
issues. Finally, our work also shares challenges found in crowd-               diverse themes or arguments (e.g., suggestions for all three
sourcing workflows, such as handling cascading errors that affect              problems in the peer review example in Figure 1).
later stages [35], staged crash-and-rerun [42], all of which we take       C.3 LLMs are sensitive to input prompts. They tend to favor
into consideration in the design of the Chaining structure. Beyond             certain prompt formats, paraphrases [45, 51], or even certain
this, we advance the field by examining how core features of Chain-            information in the input. For example, prompts that are
ing (e.g., cascading effects, parallel paths) are used not only to             unnatural relative to the typical text distribution tend to be
accomplish tasks, but also to aid in increasing the transparency and           less efficient [11], while nouns and verbs are more important
debuggability of AI.                                                           than adjectives and function words [51].
                                                                             These challenges tend to stem from tasks being too broad. Yet,
                                                                         as discussed above, LLMs may be able to perform certain tasks well
                                                                         if they are highly targeted, with narrower contexts. Hence, with
3    CHAINING LLMS                                                       these challenges in mind, we reviewed 73 existing demos based
Despite the impressive capabilities of LLMs, there may be contexts       on an extensive search of official LLM websites, social media, and
in which LLM performance would suffer, such as if the data is for-       published case studies (these are enumerated in Table 2, Appen-
matted sub-optimally, if there is extraneous data in the input, if the   dix A) to identify promising LLM capabilities that may help scope
task inherently demands solving multiple sub-parts, or if the user is    the inputs/outputs, culminating in a set of primitive operations.
asking the model to perform several tasks at once. Meanwhile, LLMs       Note that the operations we identified may not be exhaustive, but
may perform highly targeted tasks well. By narrowing the scope           rather represent an interesting range for study, with a variety of
and context of an LLM operation, for example, LLMs may them-             operations addressing each LLM challenge. Pilot studies — as well
selves be useful for addressing some of their own challenges (e.g.,      as use cases we present later — suggested these were a reason-
removing extraneous data, splitting problems into sub-parts, etc.).      able set to pursue. Full details of our methodology can be found in
Thus, we hypothesize that decomposing a problem into smaller,            Appendix A.
highly targeted tasks is likely to increase model performance on             Table 1 shows how the derived operations fall into three cat-
those sub-tasks, and by extension, the overarching task.                 egories and can address the aforementioned challenges. First, as
   We define Chaining as the process of breaking up complex tasks        LLMs may have difficulty applying common sense reasoning or
into smaller steps, where each step can be completed by an in-           complex inference to nuanced problems (C.1), the Classification
dependent run of an LLM, and where the output of one or more             operation can act as a validation check or triage, before more
steps is used as input for the next. To identify tasks that are most     steps are carried out (Table 1a). For example, a chatbot may need to
likely to benefit from Chaining, we first surveyed existing language     first classify the type of question a user is asking before providing
modeling literature, and summarized common challenges LLMs               adequate responses. Second, to alleviate exposure bias (C.2, the
face. As described in Section 3.1, these challenges are caused by        inability to generate long and diverse text), some operations can be
the underlying modeling structure shared by the mainstream LLMs,         used to query small chunks of new content (Table 1b), so as to
including but not limited to GPT-3, Jurassic-1, and the internal LLM     gradually build up the generation diversity and length. Three ways
used in Section 5 and 6. Then, to identify promising sub-tasks that      to get new content include querying facts, generating hallucinations,
could be used as building blocks, we surveyed existing online demos      and ideating lists of items. For example, in the peer review rewrit-
of LLMs, and curated a list of primitive LLM operations, which           ing scenario (Figure 1B), the separate Ideation step per problem
   Transparent
Transparent andand Controllable
                Controllable    Human-AI
                             Human-AI    Interaction
                                      Interaction  byby ChainingLLM
                                                      Chaining   LLMPrompts
                                                                     Prompts                                                        CHI ’22, April 29-May
                                                                                                                                    CHI            29-May 5,
                                                                                                                                                          5, 2022,
                                                                                                                                                             2022, New
                                                                                                                                                                   NewOrleans,
                                                                                                                                                                       Orleans,LA,
                                                                                                                                                                                LA,USA
                                                                                                                                                                                    USA


      (a) Validate and categorize the input                                                          (c) Re-organize the input
     Def. Classification: Assign the input to categories. Most useful for                            Def. Info. Extraction: Extract information from the context.
             branching logic and validation.                                                         Ex.   Given the text, extract airport codes per city.
      Ex.    Classify if the question is answerable.                                                       text: I want to fly from Los Angeles to Miami.
             question: What is the square root of banana?                                                  airport codes: LAX, MIA
             is answerable (Yes/No): No                                                              Def. Rewriting: 1-1 mapping that changes the input to more machine-
                                                                                                           readable formats (e.g., JSON to natural language).
                                                                                                     Ex.   Rewrite the first-person text into third-person.
      (b) Gather additional information from the LLM                                                       first-person text: I decided to make a movie
                                                                                                           third-person text: He decided to make a movie.
     Def. Factual Query: Ask the model for a fact.
                                                                                                     Def. Split Points: 1-N mapping that is particularly useful for splitting
      Ex.    Given the US state, find the population.
             US state: Washington                                                                          contexts.
             Population: 7.6 million                                                                 Ex.   Split the feedback paragraph into a list of Alex’s
     Def. Generation: Ask the model to do some creative “hallucination”                                    presentation problems.
                                                                                                           Feedback: Alex could improve his presentation skills. He has
             on the input.                                                                                 too much text on his slides. His presentation meanders from
      Ex.    Given the topic, create a two-sentence horror story.                                          topic to topic without a clear structure. He also does not
             topic: Breakfast                                                                              engage with his audience when he presents.
             two-sentence                horror                story:                                      Alex’s problems: 1) Too much text
             He always stops crying when I pour the milk                                                   2) No clear structure
             on his cereal. I just have to remember not                                                    3) Does not engage with audience
             to let him see his face on the carton.                                                  Def. Compose Points: N-1 mapping, the reverse operation of decompo-
     Def. Ideation: Ask the model for a list of ideas or examples.                                         sition; merge multiple results back together.
      Ex.    Given Alex’s presentation problem, the following is a                                   Ex.   Write one friendly paragraph to cover all the problems and
             list of suggestions.                                                                          suggestions for improvement.
             Alex’s problem: Too much text                                                                 Alex’s problems: 1) Too much text; 2) No...
             Suggestions for improvements:                                                                 Suggestions: 1) More images on the slides;...
             1) Use more graphics                                                                          Review: Your presentation was interesting!
             2) Use bullet points                                                                          However, I noticed that you have a lot of...

Table 1: We curate eight primitive operations that may be adequately handled by a single LLM run. Grouped according to their
  Table 1: We curate eight primitive operations that may be adequately handled by a single LLM run. Grouped according to their
intended objectives, these operations can help address the LLM challenges detailed in Section 3.1. Along with the definitions,
  intended objectives, these operations can help address the LLM challenges detailed in Section 3.1. Along with the definitions,
we provide examples of prompts that enact these operations, with the underlined text being the LLM output given the preced-
  we provide examples of prompts that enact these operations, with the underlined text being the LLM output given the preced-
ing prompt. The examples for Ideation, Split and Compose points are replicas of steps in Figure 1. The full implementations
  ing prompt. The examples for Ideation, Split and Compose points are replicas of steps in Figure 1. The full implementations
(with the parameters in Figure 6) are in Appendix D.
  (with the parameters in Figure 6) are in Appendix D.

prevents
   prevents  suggestions
                 suggestions    forfor
                                     oneone  criticism
                                                criticismfrom frombeing
                                                                      beinginfluenced
                                                                                 influencedby   by    output
                                                                                                       3.2 data    (which weOperations
                                                                                                              Designing            call data layers). forForLLM
                                                                                                                                                              example,      the Split point
                                                                                                                                                                      Chaining
thethe
     other
        other two criticisms. Finally, because LLMs may strugglewith
             two    criticisms.     Finally,     because      LLMs    may      struggle      with     operation in Figure 1 takes in the initial feedback for Alex as input,
                                                                                                       An LLM Chain consists of multiple steps. Each step is defined by
certain
   certaininput
              input prompt
                       prompt   types,
                                   types, reorganizing
                                              reorganizingthe             promptcould
                                                                   theprompt            couldbe be    and produces a list of presentation problems (“too much text”, “no
                                                                                                       an LLM operation, which takes in input data and produces output
helpful  when      itsits
                       original   form     is is
                                               convoluted.        Rewritingand
                                                  convoluted.Rewriting            andCompose          clear structure”,    etc.)   as output.
   helpful   when         original    form                                              Compose        data (which   we call   data    layers). LLM     Chains the
                                                                                                                                                  For example,     are Split
                                                                                                                                                                         constructed
                                                                                                                                                                               point oper- by
points  transform
   points   transform    input
                            inputintointomoremore  parsable
                                                      parsableforms,
                                                                  forms,Information
                                                                              InformationEx-   Ex-    connecting    these   steps     through     shared   data   layers.    In  the    same
                                                                                                       ation in Figure 1 takes in the •initial feedback for Alex as input,
   traction elicits concise information (C.3), and Split pointssplits
traction  elicits    concise    information         (C.3),   and  Split   points      splitstext
                                                                                              text    example   above,a the
                                                                                                       and produces       list Ideation     operationproblems
                                                                                                                                of •presentation        comes after       themuch
                                                                                                                                                                      (“too    Split points
                                                                                                                                                                                      text”,
into  smaller
   into  smaller  andandmore
                           more manageable
                                   manageable       units
                                                       units(C.1)—all
                                                               (C.1)—allare   aresummarized
                                                                                   summarized         operation, taking a (previously generated) problem as input and
in in
   Table    1c.1c.
                 AsAs  wewe will  seeseeinin a case                                                    “no clear structure”, etc.) as output. LLM Chains are constructed
       Table                   will              a casestudy
                                                           study(Section
                                                                   (Section6.1),  6.1),translat-
                                                                                         translat-    producing
inging
     JSON-formatted          specifications        totonatural                                         by connecting suggestions
                                                                                                                        these steps   forthrough   shared as
                                                                                                                                           improvements     dataoutput.
                                                                                                                                                                   layers. In the same
        JSON-formatted          specifications            naturallanguage
                                                                    languagedescriptions
                                                                                   descriptions          Each step   of an   LLM     (an operation
helps  LLMs      parse    thethe
                               embedded          information.                                          example   above,   the   Ideation     operationand   its data
                                                                                                                                                        comes    afterlayers)
                                                                                                                                                                         the Splitis accom-
                                                                                                                                                                                     points
   helps   LLMs      parse        embedded          information.                                      plished  through
   Chaining                                                                                            operation,  takinga anatural
                                                                                                                               (previouslylanguage    prompt.
                                                                                                                                                generated)         While as
                                                                                                                                                             •problem        prompts
                                                                                                                                                                                input and are
       Chaining and its operations alsohave
                  and   its  operations        also      havesome
                                                                someparallels
                                                                        parallelstotocrowd-crowd-     task-dependent,     they can for  have    some task-agnostic        properties. For
sourcing     workflows.       However,         whereas                                                 producing •suggestions                improvements       as output.
   sourcing      workflows.      However,         whereassub-tasks
                                                               sub-tasksinincrowdsourc-
                                                                                   crowdsourc-        example,   the of
                                                                                                                      prompt      for(an
                                                                                                                                       theoperation
inging
     areare
          assumed
              assumed   to tobebefeasible
                                    feasible   forfora ahuman
                                                          humanworkerworker(reviewed
                                                                                  (reviewedinin           Each step      an LLM                        and itsoperation
                                                                                                                                             Classification     data layers) would     likely
                                                                                                                                                                                 is accom-
                                                                                                      contain  the  verb   “classify”,      regardless  of  what
                                                                                                       plished through a natural language prompt. While prompts are  is being    classified.
Section
   Section 2.3),  LLMs
               2.3),  LLMs  areare
                                 more
                                    more  restricted
                                              restrictedinintermstermsofoftasks tasksthey
                                                                                        theycan
                                                                                              can     These  keywords they help canset an    LLM   operation’s     scope     and expecta-
perform
   perform  reliably,
                reliably,andandthus
                                  thus thetheprimitive
                                                 primitiveoperations
                                                               operationspresented
                                                                                 presentedare  are     task-dependent,                  have    some  task-agnostic      properties.     For
                                                                                                      tions [53].the
                                                                                                       example,   Weprompt
                                                                                                                       aim to for abstract     these task-agnostic
                                                                                                                                       the Classification    operation    properties
                                                                                                                                                                            would likely into
more
   morescoped
          scoped  and   granular.
                      and   granular. ForForexample,
                                                example,   Kittur
                                                             Kitturetetal.al.[37]’s
                                                                               [35]’sPartition-
                                                                                        Partition-    default
   Map-Reduce
Map-Reduce             workflow
                   workflow       usesuses    Splitand
                                          Split       andCompose
                                                            ComposePoints           operations
                                                                          Pointsoperations             containparameters      for each operation
                                                                                                                the verb “classify”,        regardless(Figure
                                                                                                                                                        of what2A),      so as to
                                                                                                                                                                    is being        provide
                                                                                                                                                                                classified.
                                                                                                      consistent  starting    points    for   interacting  with    LLM
                                                                                                       These keywords help set an LLM operation’s scope and expecta-       Chains     across
(in(in Figure
    Figure    1B),1B),
                     butbut   does
                           does   not not   indicatespecifically
                                        indicate         specificallyhow  howtototransform
                                                                                     transform
                                                                                                      use
thethe  text
     text      (Ideation),
           (Ideation),        though
                           though     it it
                                         alsoalso    targetscollaborative
                                                  targets      collaborativewriting.writing.           tions [51]. We aim to abstract these task-agnostic propertiesshow
                                                                                                           cases. Using    the   Ideation      operation  as   an  example,       we    into
                                                                                                      how   we parameters
                                                                                                       default  design these  forparameters
                                                                                                                                    each operationto satisfy
                                                                                                                                                       (Figurethe   following
                                                                                                                                                                 2A),   so as to three
                                                                                                                                                                                   provide re-
                                                                                                      quirements    for chaining,
                                                                                                       consistent starting     pointsand       how they help
                                                                                                                                         for interacting   withto LLM build   the Ideation
                                                                                                                                                                           Chains    across
3.2         Designing Operations for LLM Chaining                                                     prompt   shown
                                                                                                       use cases.  Usingin the
                                                                                                                            Table    1 and Figure
                                                                                                                                  Ideation            2B. as an example, we show
                                                                                                                                               operation
                                                                                                         Operations need to invoke the desired functionalities, through
An LLM Chain consists of multiple steps. Each step is defined                                         prompt design. To date, the most common patterns for prompting
by an LLM operation, which takes in input data and produces
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                                   Tongshuang Wu, Michael Terry, and Carrie J. Cai


                                                                                                                                                Filled




                                                                     PROMPT
                     Alex’s problem                                                 Given Alex’s problem, the following is a list
                                                      Pre x-1
                                                                                    of suggestions for improvements.                            description
                    Too much text
                                                      Input string
                                                                                    Alex’s problem: Mumbles when presenting                     Few-shot
                                                                                    Suggestions for improvements:                               examples
                         Ideation t=0.7
                                                                                    1) Enunciate each syllable
                 Given [prefix-1], the following Description                        2) Speak more slowly
      TEMPLATE
       PROMPT




                 is a list of [prefix-2].                                           ###
                 [few-shot examples]                                                Alex’s problem: No eye contact
                 [prefix-1]: (string)            Pre xes &                          Suggestions for improvements:
                 [prefix-2]: 1) (list)       A Data types                           1) Look at the middle row of the audience
                                                                                    2) Practice to look at yourself in the mirror




                                                                     MODEL OUTPUT
                                                                                    ###
                    Suggestions for improvements      Pre x-2                       Alex’s problem: Too much text                               Pre x &
                    Use more graphics                 Output list                   Suggestions for improvements:                               Input
                                                      (Parsed)                      1) Use more graphics
                    Use bullet points
                                                                                    2) Use bullet points                       B

Figure 2: An example of how to create an LLM step using a prompt template (A), using the Ideation step of the peer review
writing scenario (from Figure 1) as an example. For the peer review scenario, the Ideation operation takes in a problem (e.g.,
too much text) as input, and produces suggestions for improvement as output, but the prompt template allows the Ideation
operation to take in any custom inputs and outputs. The template includes placeholders for the input (prefix-1), output (prefix-
2), and (optional) few-shot examples. (B) shows the actual prompt after filling in the placeholders in the prompt template.

how we design these parameters to satisfy the following three re-                       allows us to build LLM steps simply by filling in the placeholders
quirements for chaining, and how they help to build the Ideation                        with definitions on data layers, as demonstrated in Figure 2. In
prompt shown in Table 1 and Figure 2B.                                                  particular, we include key verbs and nouns [51] in the template,
   Operations need to invoke the desired functionalities,                               to best reflect the operation objective (e.g.,“a list of” for Ideation,
through prompt design. To date, the most common patterns for                            “classify” for Classification). The template also accepts optional few-
prompting are either zero-shot or few-shot prompts, depending on                        shot examples. We can build the few-shot prompt in Figure 2B if
how many demonstrating examples are provided in the prompt [12].                        we provide those pairs of problems and suggestions, or default to
Zero-shot prompts directly describe what ought to happen in a task:                     just the zero-shot version in Table 1 when examples are not read-
e.g., we can enact Ideation with a task description prompt “Given                       ily available. Though we provide this as one example of a prompt
Alex’s presentation problem, the following is a list of suggestions.”                   template, we do not claim it to be exhaustive as there may be other
In contrast, few-shot prompts show the LLM what pattern to follow                       equally effective ones.
by feeding it examples of the desired input and output data: “Prob-                        Operations should handle parsing of the expected input/
lem: mumbles when presenting, Suggestion: enunciate each syllable,
          fi                                                                            output data types. Different data layers may take on different
Problem: too much text, Suggestion:” (full prompt in Figure 2B).                        data types. For example, the Split step (Figure 1𝑏 1 ) produces a list of
Given these prompts, the LLM might produce a reasonable sug-                            problems, but only a single problem is the input to each subsequent
gestion, e.g.,“use more graphics on the slides.” Zero-shot prompts                      Ideation step (𝑏 2 ). To handle different formats in different steps,
can also be easily transformed into few-shot prompts, by append-                        in each operation’s definition, we define the required data types
ing examples to the initial zero-shot task description. In either                       per operation (e.g. “list” in Figure 2 for Ideation), along with the
case, prompts commonly include meaningful names as prefixes                             corresponding parsing necessary to produce the expected data type
(“Problem:” and “Suggestion:”) to demarcate structure, which helps                      (e.g., split each row of the numbered list into an item).
re-emphasize the desired intent [64]. Following this convention,                           Empirically, we find these defaults to work reasonably well across
we build our prompts to include task descriptions followed by pre-                      domains (see later sections 5 and 6). Still, we note that our defaults
fixes. Aside from the prompt itself, we also associate with each LLM                    here are just one example of possible operation implementations;
operation a default temperature setting: a model parameter that                         in our review of existing demos, there appeared to be many diverse
influences the randomness of the LLM generation. For instance,                          prompting strategies even for the same task. We hope the prompt
creative operations like Ideation benefit from a higher temperature                     templates provided here may serve as a starting point for Chain de-
(𝑡=0.7) than more factual or deterministic tasks like Classification                    signers or users to modify. In the next section, we demonstrate how
(𝑡=0.0) [2].                                                                            these designs serve as the underlying data structure for interactive
   Operations should be able to take custom data layers as                              Chain execution by end-users.
inputs and outputs. Though our walkthrough example takes in
“Alex’s presentation problem” and generates “Suggestions”, in the-
ory an operation should be able to handle any custom data layers.                       4    INTERACTIVE USER INTERFACE
We thus create prompt templates to support a wide range of sce-
narios, with placeholders for input and output data. The template                       We designed an interface that helps users execute and customize
                                                                                        LLM Chains interactively.
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                           CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA



                  A                                               B                                                   C




                                                                                  b1

      a1


                                                                                  b2



                                                                                                           c1

                                                                                  b3
             a2




                                                        b4
                                                                                                                                   c2




Figure 3: An overview of the interface, reflecting the peer review rewriting example in Figure 1. It consists of (A) a Chain view
that depicts the high level Chaining structure, and (B/C) a Step view that allows for refining and executing each LLM step. The
interface facilitates tracking the progress of the LLM Chain. For example, when moving from step 2: Ideation (B) to step 3:
Compose Points (C), the previously generated presentation problems and suggestions become inputs for the final paragraph.
A demonstration is available at https://youtu.be/QFS-1EWlvMM.

4.1     Design Rationales                                                         task description or intermediate model output) and globally
Over the course of several weeks, we designed and iterated on                     (e.g., changing how the steps are connected). Because global
the prototype with feedback from four pilot users (software engi-                 changes have more impactful consequences (they may over-
neers and designers who have experience designing LLM prompts),                   write the underlying Chain structure), we designed the UI
producing three design rationales for the final interface.                        to require a switch to editing mode for this type of changes.
                                                                              R.3 The structured controls should still reflect the natural
  R.1 Visually reflect the underlying Chaining structure. In
                                                                                  language interaction supported by LLMs. In an early
      early prototypes, we explained the Chain structure using a
                                                                                  prototype, we formatted the data as structured tables with
      static slide deck that highlighted the data produced at each
                                                                                  each data layer being a column, but received feedback from
      step (e.g., problems, suggestions for improvement, and final
                                                                                  two users that making text edits in cells felt unnatural as
      paragraph in Figure 1). In reaction, users expressed a desire
                                                                                  they lost the sense of interacting with the model through
      to understand the operations taken at each step to arrive
                                                                                  natural language. To retain a natural interaction experience,
      at these data layers (split points, ideation, compose points),
                                                                                  we keep these structures as in-line text fields.
      and wanted to visually track progress through the Chain. To
      achieve this, we designed the interface to reflect not only
      the data layers, but also the LLM details within each step.           4.2   Interface Design and Implementation
  R.2 Provide controls at different granularities. Pilot users              We design the interface in Figure 3 following these design ratio-
      favored flexible controls. We observed users frequently mak-          nales above, which consists of two primary views: the Chain view
      ing local fixes on intermediate data points that flow between         (Figure 3A), and the Step view (Figure 3B/C).
      LLM steps, and therefore designed the UI to allow in-place               The Chain view (Figure 3A) depicts the high level Chaining
      editing, without explicitly requiring a switch to editing mode.       structure through a flow chart. It contains three primary visual
      Some users also voiced an interest in iterating on alterna-           cues that closely reflect the underlying design (R.1) described in
      tive Chaining structures (“Can I change this step with...”).          Section 3.2. First, we use grey glyphs to represent LLM operations,
      We therefore conclude that the interface should support               with shapes indicating 1-1 (rectangle, for operations like Rewrit-
      modification of LLM Chains both locally (e.g., changing one           ing in Table 1), 1-N (trapezoid, e.g., Ideation operation), and N-1
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                             Tongshuang Wu, Michael Terry, and Carrie J. Cai


data mappings (inverted trapezoid, e.g., Compose points operation).           the Chain view, or through text fields in the Step view. Finally,
Clicking on these glyphs allows users to choose which step to zoom            users can more aggressively modify the Chaining structure itself
into (highlighted in pink), and the Step view would change in re-             by adding, removing and rewiring operations or data layers in the
sponse. Then, we use rectangles with colored stripes to represent             Chain view through intuitive visual programming (R.3). The change
data layers. Users can preview their data entries through white               would then cause the entire Chain to re-render, with the defaults
rows (e.g., Figure 3𝑎 1 and 𝑎 2 ), which are updated after each LLM           (e.g., temperature, instructions) refreshed.
execution, and thus track Chain execution progress. Finally, we
link these elements with dotted-line arrows to highlight which data           5     USER STUDY
output serves as the input to which step, and use the number of               To understand how Chaining affects the user experience of accom-
arrows going out of an operation to re-emphasize the data map-                plishing tasks with LLMs, we conducted a within-subject user study
pings (e.g., multiple •problems coming out from Split points, which           comparing Chaining with a state-of-the-art baseline interface, on
is approximated with three lines, and a single •paragraph out of              two user tasks.
Compose points).
   On the right, the Step view (Figure 3B) allows users to explore            5.1     Study Design
each LLM step by interacting with inputs, outputs, and the un-                Underlying LLM. All of our experiments (including our baseline
derlying prompt structure. It is divided into an instruction block            interface introduced below) and each step of the Chaining interface
and several running blocks to handle parallel paths. Each of these            rely on exactly the same underlying LLM: LaMDA [63]2 , a 137
parallel paths translates to a different LLM invocation; they share           billion parameter, general-purpose language model. This model
some common parts in their prompt strings, while having other                 is roughly equivalent to the GPT-3 model in terms of size and
parts being distinct from each other. We use the running blocks               capability: it is trained with more than 1.5T words of text data,
to hold the unique parts, and the instruction block to hold the               in an auto-regressive manner using a decoder-only Transformer
shared sub-string is pre-pended to all running blocks, such that              structure which is useful for text generation. It has comparable per-
they are combined to form the full prompt. For example, Figure 3𝑏 2           formances with GPT-3 on a variety of tasks, and behaves similarly
is the final prompt for the step that generations suggestions for             in its ability to follow prompts. Note that we only use this model
the problem “too much text.” It starts with the content from the              to represent the recent class of LLMs; essentially, the chaining in-
instruction block (𝑏 1 ), and merges the text in the running block            terface is model agnostic, and is compatible with any LLM that has
thereafter, ignoring the other parallel running blocks.                       in-context learning capability.
   Every running block visually resembles a textarea with a num-                 Systems. We compared Chaining with Sandbox, an interface
ber of editable text fields. It shows the prefix fields before colons         that looks aesthetically similar to the Chaining interface, but with-
(e.g.,•Short suggestions for improvement, 𝑐 1 ) in the same color             out the Chaining functionality. We based the Sandbox interaction
as the data layer rectangles, which helps users distinguish between           on GPT-3 playground,3 the standard online interface for LLMs. It
data layers. It also includes text fields (𝑏 4 , 𝑐 2 ) for the model output   presents a single textbox with a run button, which allows the user to
for that step. The number of text fields (e.g., 1 vs. N) are consistent       enter the text prompt, run the model on that prompt, and then view
with the data types defined for the primitive operation for that step.        the model result in the same textbox, with the ability to edit that
   This view also handles the per-step execution. Users can click             result and then continue to iterate. Like the Chaining interface,
the small “run” button to execute each running block individually.            the Sandbox also allows users to adjust the temperature setting
Alternatively, users can use the Play button on the top to run all            through a knob.
the parallel blocks at once and compare their results. To improve                Tasks. We conducted the study using two tasks: peer review
natural language interaction transparency (R.3), running a block              writing, and personalized flashcard creation, as they reflect different
also triggers a preview of the final prompt text (𝑏 2 ). The output is        types of challenges (as explained below), and are both commonly
then parsed and added to the corresponding field (𝑏 4 , 𝑐 2 ) for users       used in user-centered task scenarios [14, 17, 25]. In the peer review
to further iterate on.                                                        writing task (“Review,” our walk-through scenario), the user is
   Interactions and controls. Notably, there are three levels of              given a paragraph (the same as in Figure 1) outlining three different
control available with this interface (R.2), from local customization         problems in an imaginary person’s presentation style, and their
of prompts to global modification of the LLM Chain structure, each            task is to write a friendly paragraph with 1-3 suggestions for each
with clear cues on its impact. First, users can customize the prompt          problem. In flashcard creation (“Flashcard”), participants were
for a particular step, e.g., by changing its task descriptions. Since         asked to create at least ten English-French sentence pairs they
the customization only applies to the current step, all other views           could use while traveling in Paris, and to make them as diverse as
remain unchanged. Second, users can customize the model output                possible while being personalized to their own travel goals.
for that step by adding, deleting, or editing content (e.g., editing             Though both tasks are possible when using an LLM without
“read outlines” to emphasize main points in 𝑏 4 ), or rename data layers      any LLM Chains, they present different types of challenges which
(e.g., rephrasing “Alex’s presentation problems” as “Criticisms of            could potentially be improved through Chaining. The Review task
Alex” in 𝑎 1 ). These changes impact both the current step in focus as        implicitly involves multi-step reasoning (Challenge C.1 in Section 3):
well as other steps involving the shared data layers (e.g., Compose           to create a thorough and constructive review, one needs to identify
Points takes in both the “problems” and the “suggestion” layer),
and thus they can be changed either in the colored rectangles in              2 We used a non-dialog version of the model.
                                                                              3 https://gpt3demo.com/apps/openai-gpt-3-playground
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                                         CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA


                                        Types of interactions




                             Ideation
                                         Small talk                     B           Examples in English               C           Examples in French
                                         Transportation                             Do you like the weather?                      Vous aimez le temps?




                                                                                                                     Rewriting
                                                                       Ideation
                                         Accommodation
   City to visit
                                                                                    Where's the bus station?                      Où est la gare routière?
    Paris                     A                                                     How do I go to the Louvre?                    Comment aller au Louvre?

                                                                                    I will check out at noon.                     je partirai à midi.


Figure 4: The LLM Chain for flashcard creation, with: (A) An Ideation step that brainstorms the •types of interactions that we
might encounter when •visiting a given city (Paris), (B) Another Ideation step that creates a list of •English examples for each
•interaction type, and (C) A Rewriting step that translates each •English example into •French.

each problem, provide suggestions per problem, and compose all                             Collected data. We collected and analyzed three sets of data.
the suggestions into one paragraph. The Flashcard task, on the                          First, to assess participants’ self-perceived experience, we used
other hand, exposes the challenge of having sufficient diversity in                     a standard seven-point Likert Scale [41] to collect all ratings from
light of LLM exposure bias (C.2). In the Chaining condition, we                         the exit survey, with one being “Strongly disagree” and seven being
built a default Chain for each task. The Chain for Review in Figure 1                   “Strongly agree” with the statement in question (e.g., for system
reflects the three aforementioned steps (as explained before); the                      Transparency: “The system is transparent about how it arrives at its
Chain for Flashcard (see Figure 4) sources additional content from                      final result”). Detailed survey questions are listed in Appendix B.1.
the LLM like •types of interactions in a trip, which can help the                          We also observed and recorded their entire task completion ses-
user diversify the flashcards.                                                          sions, and later transcribed their comments and experience for
   Study procedure. Before the study, participants completed a 30-                      qualitative analysis. Second, to quantify their interaction mecha-
minute tutorial that summarized the concept of LLMs and demon-                          nisms and behaviors, we logged their interactions with the two
strated how both Sandbox and Chaining work.4 They were told                             interfaces. We were particularly interested in how participants re-
upfront that both systems rely on the same underlying LLM. Then,                        acted and iterated on model outputs, so we sorted their interactions
in an hour-long study, participants performed a randomly selected                       with text fields by: (1) whether participants mainly relied on run-
task (Flashcard or Review), once with each interface (Sandbox and                       ning the model again to get a different result (Consecutive run),
Chaining), whose orders were counterbalanced. We first briefed                          or if they also edited the prompt in between (Edited); and (2) when
participants on the task, and then asked them to accomplish it with                     they edited the prompt, how dependent it was on the existing model
LLM’s help in each interface until they were satisfied with the final                   generation: whether they closely CURATED and refined the model
results, or until they reached 25 minutes. Since LLM Chains came                        outputs, loosely interacted around them by CREATING completely
with automatically generated prompts (by filling in the templates),                     new content, or tried again by UNDOING the outputs. The detailed
we similarly offered several default prompts for Sandbox that we                        categorization criteria is in Appendix B.2. Third, to assess the task
knew to work reasonably, so that both interfaces had a fair starting                    outcome, we logged the final reviews and flashcards participants
point for prompt engineering (detailed in Appendix B). We encour-                       created. Blinded to the condition, two non-participants performed
aged participants to think aloud and describe their actions as they                     anonymous, paired comparisons on results from each participant in
completed the task.                                                                     Sandbox and Chaining, choosing the result that satisfied the task
   In the Chaining condition, participants were asked to first stick                    goals the best.
to the default Chain so that we could make consistent observa-                             Participants. We recruited 20 participants using email lists that
tions across participants in terms of how they use Chains. In the                       reach a wide range of practitioners (e.g., UX designers, linguists,
process, they could modify any other aspect (e.g., the prompt, the                      data analysts) at a large software company. Eight participants were
intermediate model outputs, etc.) At the end, we gave participants                      26-35 years old, eight aged 36-45, two aged 46-55, one 56-65, and
the option to modify the default Chain, so that we could observe                        one 18–26. As there is an initial learning curve associated with LLM
how they would expect the LLM to assist them beyond the de-                             capability, we required that participants had at least seen an LLM
fault design. Finally, participants completed an exit survey and a                      example before. Among those we recruited, half of the participants
semi-structured interview. They rated their experience using each                       had no prompting experience but had seen online demos powered
interface along various dimensions. These dimensions were cho-                          by LLM models, whereas the other half had some basic experience
sen to reflect the effectiveness of the human-AI collaboration (e.g.,                   using default text prompts. Further, as the goal of Chaining is to
support for their thought process, quality of the final result), and                    use LLMs to assist with human tasks, we sought to recruit poten-
core user-centered challenges in human-AI systems [5, 13, 31] (e.g.,                    tial users of ML/LLM who would benefit from interacting with the
transparency, controllability, and sense of collaboration). They                        models, rather than ML model experts or creators. Thus, our partic-
also verbally compared their impressions of the two interfaces, and                     ipants included technically knowledgeable but non-ML software
envisioned possible use cases for them.                                                 engineers, linguists, UX designers, and data analysts who worked
                                                                                        in a wide range of domains (e.g., health, privacy, cloud storage, etc.).
4 We took inspiration from the OpenAI: https://beta.openai.com/docs/introduction/
prompt-design-101; the task used for tutorial is in Appendix B.3.
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                                 Tongshuang Wu, Michael Terry, and Carrie J. Cai


Each participant spent approximately 90 minutes total in our study,                    5.3    Qualitative results: Chaining as Guardrails
and received a $40 gift certificate for their time.                                           and Operation Manuals
                                                                                       Through analyses of the transcribed think-aloud comments and
5.2     Quantitative Results: Increased                                                semi-structured interviews, we further unpack the reasons behind
        Transparency & Control, and                                                    the quantitative differences. Since we asked participants to explain
        Higher-quality Task Outcome                                                    their Likert Scale ratings, their interview responses naturally map to
All the participants were able to complete the tasks in both systems                   dimensions in Figure 5 like transparency, collaboration, etc. One au-
within the given time: they spent 12.4±4.0 minutes in Sandbox, and                     thor further sorted their think-aloud comments into the categories.
14.6 ± 5.4 in Chaining. Student’s t-test did not show any significant                  Three researchers then conducted thematic analysis, examining
difference between their completion time (𝑡 = −.1.1, 𝑝 = .278). In                     relationships between categories and iteratively converging on a
analyzing subjective ratings from participants, the logged click-                      set of higher-level themes. In general, Chaining helped support
streams, as well as the final generated results, we found:                             human-LLM interaction by serving as (1) a guardrail that helped
   First, Chaining led to improved user experience in human-AI in-                     users stay on track towards the task goal (Section 5.3.2 and 5.3.5);
teractions. We performed the non-parametric Wilcoxon signed-rank                       and (2) an “operation manual” that implicitly explained how to
test to compare users’ nominal Likert Scale ratings and, as shown                      use LLMs for less obvious objectives, and that provided channels
in Figure 5, participants felt that Chaining helped them think                         for users to intervene (Section 5.3.1, 5.3.3 and 5.3.4). In the follow-
through the task better (Chaining 6.0 ± 1.4 vs. Sandbox 3.6 ± 1.3,                     ing sections, we present key themes on how Chaining improved
𝑧 = 0, 𝑝 < .001), and gave them more control (6.2±0.9 vs. 4.5±1.3,                     the human-AI experience, as well as some additional challenges
𝑧 = 3.0, 𝑝 < .001). They also rated Chaining as being more collab-                     brought on by Chaining.
orative (5.7 ± 1.3 vs. = 4.6 ± 1.6 , 𝑧 = 25, 𝑝 = .04) and transparent                  5.3.1 Chaining helped users more fully capitalize on the model’s
(5.4 ± 1.3 vs. 3.8 ± 1.8, 𝑧 = 9.0, 𝑝 = .002).                                          latent capabilities.
   Second, Chaining shifted the types of edits participants made                       In Sandbox, participants tended to use the LLM for a single purpose,
while interacting with the LLM. In Chaining, participants were                         under-utilizing the model’s full potential in supporting various
more likely to make manual interventions, whereas in Sandbox,                          kinds of tasks. Four out of ten people in the Flashcard task only
they often re-ran the model (without changing the prompt) — akin                       used the model as a translator in Sandbox, even though they were
to “rolling the dice again" in an attempt to get better output. As                     provided with default prompts that demonstrated how to generate
shown in Figure 6A, this tendency to perform consecutive runs                          English sentences using the model. In the Review task, even though
without altering anything from the previous run occurred 51% of                        nearly everyone (nine out of ten) used a two-step process of gen-
the time on average in Sandbox and 36% in Chaining. Student’s                          erating suggestions prior to merging them into the full paragraph
t-test shows the difference is significant: 𝑡 = 3.5, 𝑝 = .001.5                        (see the two-step prompt template in Appendix B.5), three people
   The manual edits made were also finer-grained in Chaining                           only relied on the LLM to generate suggestions, and then manually
than in Sandbox (Figure 6B). In Sandbox, people largely focused on                     merged them into the paragraph themselves, without LLM input.
either completely UNDO output and rerunning the model (45% of the                          There may be two reasons for these behaviors. First, Sandbox
time on average), or manually CREATING their own content as input                      naturally affords single-operation interactions. Given this, it is not
to the model (14%). They only CURATED or modified existing text                        surprising that users would gravitate toward using the model only
41% of the time. On the other hand, in Chaining people performed                       for a part of the task that seemed most likely to yield promising
CURATION 77% of the time, only doing UNDO and CREATE 18% and                           results given the status-quo applications of machine learning (e.g.,
5% of the time, respectively. The shift to CURATION is significant,                    translation), overlooking others that may seem less likely to suc-
according to Student’s t-test (𝑡 = −6.75, 𝑝 < .001).                                   ceed (e.g., merging text into a paragraph). Indeed, some participants
   As a result, Chaining led to higher-quality generations that met                    were unaware of less obvious sub-tasks (P4: “this is just a simple
the task goal. The two independent raters consistently preferred                       translation task” in Flashcard). Second, the friction of juggling mul-
Chaining results 85% and 80% of the time, respectively. The results                    tiple sub-tasks in Sandbox deterred some users from doing so. Even
also matched participants’ own judgements in Figure 5 (see Match                       participants who became aware of the Chaining structure (from
goal) — they preferred their own final results from Chaining (6.0 ±                    getting the Chaining condition first in their study condition or-
0.9) to the Sandbox results (5.0 ± 1.1, Wilcoxon signed-rank test,                     der) struggled to replicate it using a single prompt. For example,
𝑧 = 11.0, 𝑝=.002).                                                                     P2 attempted to tackle both sub-tasks (generating diverse English
   Aside from using Chaining, many participants were also able to                      sentences, and translating to French) simultaneously with a single
iterate on and customize the underlying Chaining structure. While                      prompt instruction: “Given the previous English sentence, translate
five of them preferred the default Chains provided and didn’t want                     it to French. Generate further English sentences relevant to travel
to change them, the remaining 15 people were able to identify parts                    in Paris.” However, because the instruction was too nuanced for
they found lacking and suggested at least one change. 11 of them                       the model to follow, they eventually resorted to manually creating
successfully implemented and executed one of their own solutions.                      their own English sentences.
                                                                                           Ultimately, this inability to fully utilize the model led to lower
5 The clickstreams fall into the continuous range of 0%–100%, and follows a normal
                                                                                       quality final results in Sandbox. For example, the flashcards had less
distribution according to a D’Agostino-Pearson Test (e.g., 𝑝 = 0.58 for the ratio of   topical diversity (P4: “I had limited diversity myself”) because the
consecutive runs).                                                                     Ideation step in Figure 4A was rarely ever leveraged. As a byproduct
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                            CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA




Figure 5: Participants’ ratings in the form of seven-point Likert scale questions (details in Appendix B.1), with 95% confidence
intervals. Using Chaining, participants felt they produced results that better matched the task goals, and that the system helped
them think through the task. They also found Chaining more transparent, controllable, and collaborative.

               A                                                                        B




Figure 6: Distribution (based on the logged interactions) of how participants interacted with the prompts and model outputs,
with and without chaining. (A) They made more edits in Chaining (compared to just repeatedly running the model), and (B)
They tended to curate model outputs, rather than either deleting (undoing) them entirely or manually creating new content.

of the inadequate support, participants also found collaboration in         noticed that the desired model randomness should vary per sub-
Sandbox to be shallow (P5: “I’m doing all the specific work [creating       task, and tuned the temperature settings accordingly: they increased
English sentences] and it’s just doing its one thing [translation]”).       the temperatures in Ideation steps to broaden the diversity and
In contrast, Chaining allowed users to leverage the model in mul-           creativity of model responses (Figure 4A and B), and lowered it for
tiple ways. Seven participants particularly liked that they could           Rewriting to increase the chances of getting correct model output
accomplish multiple goals through the Chain, i.e., acquiring model-         (Figure 4C). However, none of them did so in the Sandbox condition
powered diversity in the Ideation step, while maintaining transla-          (e.g., P5: “I realized my temperature was always high in sandbox. I
tion correctness in the Rewriting step. This additional support may         should have had it low at translation, and high when I ask the model
have contributed to participants shifting from creation (manually           for English sentences.” ) Many Review participants also liked iterating
creating text from scratch) to curation (modifying model outputs)           on each of the presentation problems individually (e.g.,“To much
as shown in Quantitative Results (Figure 6B). Quoting P5, “I didn’t         text on slides” vs. “No clear structure”) without affecting the others.
need to give it as much, but it was giving me a lot.”                          This well-scoped impact of interventions may explain why par-
   LLMs’ diverse primitive operations and capabilities also led             ticipants felt more motivated and comfortable making manual edits
participants to consider other ways the model might be help-                in Chaining (Figure 6A). Nine people felt more compelled to enact
ful. For example, when asked to modify the Chaining structure               controls on sub-tasks, knowing that they did not have to worry
itself, P1 in Flashcard swapped the Ideation step (which gener-             about unintended effects on other parts.
ated •types of interactions) with a Generation step to produce                 Four of them further noted that this clean separation would
•a journal of my one day trip, so the model could “think about              be tedious (if not impossible) in Sandbox, hence the differences
what conversations can happen across my day trip” and provide “less         in the perceived controllability in Figure 5. For example, P13 in
generic context suggestions.” The operations became inspirational           Review attempted to replicate the exact same Chain in Sandbox.
here. P12 and P20 in Review both added a Classification step to             They manually divided the original paragraph into three problems,
determine if the paragraph is in the right voice or if a suggestion         then asked the model for suggestions for each, and to compose the
is actionable, only once they realized the classification operation         final paragraph. However, rather than storing suggestions exter-
existed.                                                                    nally and starting fresh for each problem, they simply stacked them
                                                                            together in a single prompt: “Original paragraph:...; Problem: too
                                                                            much text; Suggestions: 1)...; Problem: Split...” The resulting long
                                                                            and intertwined text became overwhelming: “I was very nervous to
5.3.2 The ability to isolate interventions and save progress enhanced       edit anything, because I didn’t know how that was going to impact
controllability of LLM.                                                     the end task goals.”
Because each step of a Chain involves a separate run of the model,             Beyond staged interventions, staged outputs also provided par-
Chaining allowed users to control certain aspects of each sub-task          ticipants with the opportunity to evaluate and improve individual
independent of others. Four Flashcard participants in Chaining
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                          Tongshuang Wu, Michael Terry, and Carrie J. Cai


components irrespective of previous failure [50]. Three partici-               deficiencies, and possible remediation. P9 found it easier to debug
pants praised the ability to “freeze” their preferred intermediate             by modifying the inputs and outputs for each step of the Chain,
data points: “I reached some point of some progress in the middle              rather than merely re-running the model in Sandbox repeatedly,
of the Chain and if this works, then it’s fixed when I play with the           in the hopes of more promising model results (“I had to constantly
next step. It doesn’t get lost — unlike the sandbox, where whenever I          delete and rerun things.”). This may explain why the frequency of
change something somewhere the result will be completely different”            UNDO actions was reduced in Chaining (Figure 6B).
(P10). Their observations are also in line with the crash-and-rerun               Accordingly, three interesting debugging mechanisms emerged:
capability of crowdsourcing [42], where local reruns are desirable             First, the isolated steps in Chaining acted as AI “unit tests" that
without affecting previous stages.                                             enabled users to pinpoint a seemingly global error to its local cause.
                                                                               For example, participants in Flashcard frequently removed topics
5.3.3 Surfacing the Chaining structure increased transparency.                 irrelevant to traveling (e.g., education), so that sub-optimal solu-
Chaining enriched system transparency, which helped participants               tions would not be fed into subsequent steps. Second, the ability
better calibrate their expectations of the model. As each step of the          to create parallel paths and alternate step orders (elaborated in
Chain had a specific role (Ideation, Rewriting, etc.), they helped nar-        Section 5.3.3) enabled comparative debugging. Revisiting the case
row the scope of the model’s intended functionality, making it easier          mentioned above, observing a higher-quality path (e.g., using a
for participants to understand what to expect from a model that                simple keyword in the prompt like “accommodation”) helped par-
might otherwise seem all-encompassing. Nine participants noted                 ticipants infer how to improve prompts in other parts of the Chain
this benefit of calibrated expectations. For example, P6 commented             (e.g., changing “topics related to public transportation” to “public
that “Chaining helped you speak the language. It lift[ed] up the hood          transportation.”)
and showed you the steps and what’s happening at different phrases,”              Finally, the ability to propagate a change throughout the
and P15 stated that “having default settings like your templates gave          entire Chain gave users immediate feedback on whether a fix
me an idea of how it works.” As elaborated in Section 5.3.2, having            was successful, thereby shortening feedback and iteration cy-
isolated steps, each with a reduced scope, also enabled users to bet-          cles. For example, P3 renamed •types of interactions with
ter anticipate the potential impact of their inputs, further increasing        •places where conversation might occur, so as to “have flash-
system transparency.                                                           cards grouped by happening at the airport, restaurant, while walking
   More globally, Chaining enabled users to develop a more accu-               around streets.” They were impressed by the changes propagating to
rate mental model of the LLM’s capabilities, by allowing them to               the final results: “you can just change a step without affecting other
tinker with sub-components in a modular and comparative manner.                steps but then your final results are reshaped based on that. I didn’t
Users could, for example, compare parallel paths to deduce how                 think that was going to work that simply.” This combined ability to
the model would respond to alternative inputs. In the Flashcard                both isolate and propagate interventions was key to increasing AI
task, P8 noticed during the Ideation step that the model generated             debuggability.
more useful English sentences when the •types of interactions
was “accommodation,” compared to “topics related to public trans-              5.3.5 Scoped objectives in sub-tasks served as guardrails against
portation.” This hinted at the model’s better performance when                 LLM-inspired tangents.
presented with a useful keyword. Modifying the order of LLM steps              One challenge that hindered participants’ performance on the tasks
also enabled users to learn aspects of the model’s strengths and               was LLMs’ randomness and creative surprises. The model would of-
weaknesses. When customizing the Chaining structure, five par-                 ten produce outputs that were compelling in their own right, which
ticipants tried adding another Rewriting step either after the final           in turn would derail people from the intended task. For example, P5
paragraph (at the end of the Chain), or on the individual presenta-            in Flashcard was intrigued by an LLM-generated English sentence,
tion problems (early in the Chain). Though initially unaware that              “That man is suspicious to me,” and started tricking the model into
LLMs can suffer from exposure bias (see C.2), participants quickly             writing a story — “I want to know what happened to the suspicious
discovered through this comparison that the model could more                   man!” Five out of twenty people wandered from their task goal
effectively modify sentences than paragraphs. This comparison was              in Sandbox and began exploring tangents or attempting to “break”
rare in Sandbox, as it was not obvious to participants that they               the model. They had to be reminded several times to get back on
could keep the LLM functionality but shorten the input.                        track. Participants later recalled their habit of drifting: “I tried a lot
                                                                               of cool things, but it’s not the task I want to complete” (P17).
5.3.4 Surfacing the Chaining structure increased debuggability.                   Interestingly, we found Chaining acted as a safeguard against
The increased transparency in Chaining also gave users better de-              model-inspired tangents, not only because each step of the Chain
bugging mechanisms. When the model output was inconsistent                     defined a clear goal, but also because the interconnected data layers
with user intent, participants were at a loss for what to try next             motivated participants to deliberately steer outputs of each step
in Sandbox. Because users could conceivably type and modify any                away from cascading errors (e.g., incorrect problem extraction in
natural language prompt in the text box, the scope for “debugging”             the first step of Figure 1𝑏 1 could lead to a poor final paragraph). In
was too expansive. P9 remarked that “too much freedom can be a                 the Ideation steps, participants would even manually move model
curse,” while P7 felt like “sitting down in front of the controls of an air-   output around to make sure they fit the topic (P7: “this isn’t really
plane, all the knobs are there but I don’t know what to do with them.”         about asking for directions, I should put it in accommodation.”) Ul-
Instead, Chaining exposed intermediate knobs that helped partic-               timately, participants treated the entire task more carefully (see
ipants draw a more direct connection between observed model                    Figure 5, think through) — “if I was trying to do it with speed, I might
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                            CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA


find the sandbox easier; but if I want to do it with precision, I prefer    fixes. However, in a single run of an LLM, this reasoning can be
the Chaining structure.” (P13).                                             challenging, as LLMs have trouble parsing visualization specs in
                                                                            JSON formats (see LLM Challenge C.3 in Section 3.1).
5.3.6 Additional challenges.
                                                                               We thus created a Chain (see Figure 7) that (A) rewrites the JSON
Chaining brought many benefits to human-AI collaboration, but
                                                                            format in natural language, (B) classifies and validates the descrip-
it also presented several challenges. Nine participants noted that
                                                                            tions, and (C) rewrites the spec. To explore how the Chain performs
although they found the Chains to be transparent, rich, and educa-
                                                                            in practice, we took examples from VizLinter [19], used five pairs
tional, they were also more complex, with steeper learning curves.
                                                                            of erroneous and fixed specs as few-shot prompt examples, and
Moreover, while Chaining enabled participants to zoom into sub-
                                                                            tested the Chain on another five cases. One author with sufficient
tasks in modular ways, it also occasionally made the larger picture
                                                                            visualization knowledge determined that the Chain correctly re-
more difficult to recall: Four participants had questions about “how
                                                                            vealed the violated constraints for all the test cases, and provided
my particular change to this data entry will affect the final result”
                                                                            useful fixes for two of them. We also tried running a single pass
in Chaining (P2), and commented that the end-to-end aspect of
                                                                            of the LLM for comparison on the same examples, using multiple
Sandbox enabled them to see the direct effects of their actions.
                                                                            prompt designs. We observed that output from the single-passes
These challenges may have been a side-effect of participants using
                                                                            tended to be consistently worse, with at most one correct reasoning.
pre-defined Chains, which may not necessarily reflect their own
                                                                            This is possibly due to parsing difficulty (see LLM Challenge C.3),
intuition of how they would have decomposed the task [18, 71].
                                                                            as well as the inability to disentangle the sub-tasks of validation
Most people had a much more fluent experience with the Chains
                                                                            and rewriting (C.1). In contrast, each Chain step was highly scoped,
they modified — “I liked creating my framework.” (P13). Though
                                                                            increasing the chance that the intermediate data would be correct.
beyond the scope of this paper, this raises the question of how to
support users in not just using Chains, but also authoring their own
Chains, to improve user agency and intuitiveness of Chaining [69].          6.2    Case 2: Assisted Text Entry
    Moreover, while Chaining provided better guardrails for staying         We further demonstrate how Chaining could enable the branching
on task, it may come at the expense of a decreased ability to explore       logic in assisted text entry. This is based on a real industry use case
freely; three participants mentioned they would prefer Sandbox for          that aims to speed up gaze input by requiring fewer character in-
“trying out random things and see if the model can cope” (P3), and “I       puts [4, 46, 56]. Ideally, a user (e.g., person using Alternative and
feel more at liberty to play with language outside the the Chain” (P6).     Augmentative Communication technology) would express a full
They suggested they would prefer a combination of both systems:             sentence through short abbreviations that an LLM would automati-
“when there’s more ambiguity I prefer the sandbox to explore first,         cally expand. However, there are too many possible expansions to
but once I have a clear goal, I would use the Chaining to steer myself      disambiguate, e.g.,“LTSGCHKITOT” could mean “Let’s go check it
towards a fixed number of function blocks.” (P13)                           out ,” “Let’s get coffee and have a chat ,” “Let’s get some chicken
    Inspired by these concerns, we envision future research to focus        in the old town,” etc. Thus, the end user often needs to resolve the
on relaxing certain structural constraints and providing guidance           ambiguity or adjust the input.
on LLM Chain creation and refinement, which we detail later in                 With Chaining, we enable interactive disambiguation through
Discussion (Section 7).                                                     gradual expansion and if-else logic. As shown in Figure 8, if the
                                                                            user input is a shorthand (e.g.,“LTSG”), the LLM should expand it to
6     CASE STUDIES                                                          possible matching phrases (“Let’s go”, “Let’s get”), which the user
Beyond the user study tasks, LLM Chaining has the potential to              can select from. However, if the input is already a phrase, the LLM
enable a wide range of complex applications. We illustrate how              should instead auto-complete it (“Let’s go” may trigger “check it
Chaining could support more diverse applications through two case           out.”) If the desired option does not appear, the user can also insert
studies in the domains of software development and accessibility,           additional short-hands for the model to expand again, e.g.,“Let’s go
using the same model in our user study.                                     CHKITOT”, which would exclude expansions starting with “Let’s
                                                                            get.” The switch between shorthand expansion and auto-completion
6.1     Case 1: Visualization code debugging                                enables better prediction on the full text, which would be nontrivial
                                                                            for a single prompt, given the different natures of the two branches.
In this case study on visualization code debugging, we uncover how
                                                                            This case also provides a glimpse into how LLM Chains can help
intermediate data points in a Chain can become useful, especially
                                                                            prototype applications with complex logic but simple interactions
when the end goal of the task is unclear. Unlike typical code syn-
                                                                            (elaborated in the next section).
tax errors, when a visualization violates design constraints [48],
there are usually multiple valid solutions that cannot be objectively
ranked. For example, the •original visualization (using VegaLite            7     DISCUSSION & FUTURE DIRECTIONS
specifications [57]) in Figure 7 has a single violation, i.e., circle       Our work is a first step towards improving human-LLM interaction
size is continuous and thus should not be used to represent the             through Chaining. We found that it not only raises the ceiling of
discrete (nominal) field “Origin.” However, there may be multiple           what LLMs can meaningfully support, but also boosts transparency,
ways to resolve the issue [19], such as using color instead of size         controllability and debuggability — key concerns when interacting
(𝑑 1 ), removing size information altogether (𝑑 2 ), or changing the        with generative AI [5, 10]. Interestingly, we achieved this purely
data encoded to a continuous “Acceleration” field (𝑑 3 ). Thus, LLMs        by reshaping the interaction mechanism, without any need to re-
should reason about the violated constraints for users to adjust the        train the model. This suggests that LLMs to date may already have
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                                                                                                                                                                        Tongshuang Wu, Michael Terry, and Carrie J. Cai


         VegaLite Spec                                                                          Fixed VegaLite Spec
           "size": {                                                                                         "size→color": {                                                                           "size":                                              "size": {
             "field": "Origin",                                                                                "field": "Origin",                                                                        field: "Origin"                                      "field": “Origin→Acceleration",
       8/28/2021
             "type": "nominal"                                                                 Chart "type":
                                                                                              8/28/2021                "nominal"                                                                         type: "nominal
                                                                                                                                                                                                                   Chart                                    8/28/2021
                                                                                                                                                                                                                                                              "type": "nominal→quantitative"                                          Chart
           }                                                                                                 }                                                                                         }                                                    }
                                  Origin                                                                                 Origin                                                                                                                                                         Acceleration
                                                                                                                                                                                        8/28/2021                                                                                           5        10
                                                                                                                                                                                                                                                                                                          Chart 15         20
                                      Europe           Japan         USA                                                      Europe    Japan     USA

                                                                                                                    50                                                                                        50                                                                   50
                             50

                                                                                    C
                                                                                                                    40                                                                                        40                                                                   40
                             40




                                                                                                                                                                                           Miles_per_Gallon
                                                                                                 Miles_per_Gallon




                                                                                                                                                                                                                                                                Miles_per_Gallon
          Miles_per_Gallon




                                                                                  Rewriting
                                                                                                                    30                                                                                        30                                                                   30
                             30


                                                                                                                    20                                                                                        20                                                                   20
                             20


                                                                                                                    10                                                                                        10                                                                   10
                             10


                                                                                                                     0                                                                                         0                                                                    0
                              0
                                                                                                                         0        50    100     150     200                                                        0         50       100      150   200                                0       50         100       150        200
                                  0        50          100     150     200
                                                AHorsepower                                                 d1                         Horsepower
                                                                                                                                                                                            d2                                      Horsepower
                                                                                                                                                                                                                                                            d3                                            Horsepower




                                                                                                                                                                        classi cation
                                  A                                                                                                                     B
                                           Rewriting




                                                                Visualization description                                                                                                                                Validation result and suggested x
                                                                A) [encoding: size] has [data type: nominal                                                                                                              [encoding: size] conflicts with [data type: nominal].
                                                                B) ...                                                                                                                                                   Change [encoding: size] to [encoding: color].



Figure 7: An example for Chaining-based VegaLite bug fixing (simplified; the full Chain is in Appendix C). (A) We first rewrite
the •JSON format specs into •natural language descriptions to make it more parsable, then (B) classify the descriptions to
•validate design constraints and suggest fixes , and (C) finally rewrite the •final spec based on the suggested fix. While the
LLM generates the fix in 𝑑 1 , users may also choose 𝑑 2 and 𝑑 3 , both of which can fix the •validated issue just as effectively.

                                                                                                                                                                                                                                  Generation
                                                                                                                                                        classi cation
                                                                                                                     Rewriting




                                                                                                                                   Shorthand                                             Phrase


                             fi   {
                   "
,
                  fi          ]
                                   





Figure 8: An example of Chaining-based assisted text entry (the full Chain is in Appendix C). To produce better full sentences,
we classify the input text to switch between expanding shorthands (through Rewrite) and auto-completing phrases (through
Generation). By wrapping the complex Chaining logic in a simple text field, we provide intuitive interactions for end users.
       about:blank                                                                            about:blank                                                                                                              1/1                                   about:blank                                             1/1

the potential to support human-AI collaborations on many com-                                                                                                                      be     combined. In particular, model units could be used not only
plex tasks, if their latent potential can be better realized through                                                                                                               to accomplish sub-tasks, but also to more thoroughly aid in the
                                                                                                                                                                                    about:blank                                                                                                                                               1/1



thoughtful interaction design. Below, we discuss the implications                                                                                                                  task decomposition design and debugging process. To overcome
of our studies, as well as future research directions.                                                                                                                             users’ own systematic omissions [70], an upstream unit could be
                                                                                                                                                                                   designed to help users create sub-tasks to begin with, similar to
   Chaining as a new paradigm of control on multiple model units.
                                                                                                                                                                                   metaprompting [55]. Or, model units could serve as checkpoints
Contrary to recent work in human-AI interaction, which primar-
                                                                                                                                                                                   along the Chain to ensure data correctness (similar to assertions
ily examined how to increase AI controllability through exposing
                                                                                                                                                                                   in code). Moreover, while the Chains in this paper consisted of
knobs within a model [44, 49], our work opens up the possibility of
                                                                                                                                                                                   only LLM steps, alternative designs may also interleave LLM steps
steering AI using the model itself as units to control. In other words,
                                                                                                                                                                                   with human-computation steps, depending on which roles each
beyond controlling properties within a single model unit, users
                                                                                                                                                                                   collaborator could best fill.
may be able to achieve new kinds of control through manipulat-
ing how multiple model runs interact with one another, including:                                                                                                                     Chaining for rapid prototyping of integrated applications. Chain-
how modifications to upstream model units cascade, how to isolate                                                                                                                  ing also opens up new possibilities for designing AI-infused appli-
changes between model units, and how to improve user inputs by                                                                                                                     cations. With LLMs’ easy adaptation to natural language prompts,
comparing the effectiveness of parallel model runs. As language                                                                                                                    users could conceivably already prototype custom ML functionality
models grow in size and capability, they may ironically allow users                                                                                                                with lower effort, as they bypass the otherwise necessary but expen-
to treat them as smaller entities of abstraction — serving as building                                                                                                             sive process of collecting data and designing models upfront [10].
blocks towards larger human goals.                                                                                                                                                 Chaining further accelerates this design process. Taking advantage
   We envision the HCI community innovating more types of build-                                                                                                                   of interactions between multiple LLM steps, developers could build
ing blocks that a model can provide, as well as the ways they can                                                                                                                  multiple Chains to envision possible flows of how an application
                                           fi
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                                  CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA


may be used, and then perform A/B testing on those Chains. For              to maximize its utility [35]. For example, users could be provided
example, in the case of assisted text entry (Section 6.2), developers       strategic guidance on iterative Chain improvements, such as using
could quickly prototype what might happen if end users were al-             paired comparisons and version control of Chain edits to help users
lowed to provide more context: e.g., if the user is “having a meeting       decide whether to keep or further decompose an existing step.
in 5 minutes,” then “Let’s go” is more likely than “Let’s get” for the
abbreviation “LTSG.” They could test this interaction by adding an          8    CONCLUSION
additional layer of input to the shorthand expansion step.                  In this work, we introduce the notion of “Chaining” multiple LLM
   One might argue that, because each run of an LLM involves                steps together, such that the output of one step is the input to the
some computational overhead, chaining may introduce additional              next. We present an interactive system where users can modify
costs that need to be weighed against their benefits. However, as           these Chains, along with their intermediate results, in a modular
indicated above, a key benefit of chaining is that it could flexibly        way. We find that Chaining not only enhanced the quality of the
power a wide range of prototypes and applications, without the              task outcome, but also improved user satisfaction, with an increased
need to train or build bespoke, single-purpose AIs. Thus, we believe        sense of control and collaboration, a greater perception of trans-
the saved efforts outweigh the cost.                                        parency of the LLM system, and more support of the user’s thought
   Balancing between structured scaffolding and free exploration.           processes. Furthermore, we envision with case studies that LLM
While Chaining provided guardrails and scaffolding for helping              Chaining may be advantageous for complex AI-infusion applica-
users accomplish the task at hand, it also limited their ability to ex-     tions and in cases where intermediate reasoning is more important
plore freely. Yet, experimenting, tinkering, and interacting are key        than the final output. We encourage future work to explore how
to users forming mental models for AI [49]. One way to balance be-          LLMs can serve other kinds of building blocks, how Chains can be
tween structure and exploration is to loosen structural constraints         used in rapid prototyping, and strategies that can help users build
within steps. For example, it may be useful to permit users to cus-         and iterate on Chains.
tomize prompts within each step in a Sandbox-like environment,
and to define their own input and output parsers. In other words,           ACKNOWLEDGMENTS
rather than providing a full implementation of steps, a Chain could         We gratefully thank Shanqing Cai, David Dohan, Aaron Donsbach,
define the API with input-output types, and ask users to fill in the        Noah Fiedel, Anna Huang, Ellen Jiang, Ajit Narayanan, Kristen
implementations for each step. Or, a small Sandbox could be pro-            Olson, Meredith Ringel Morris, Adam Pearce, Jascha Sohl-dickstein,
vided along-side the Chaining interface, for users to occasionally          Edwin Toh, Subhashini Venugopalan, and Google PAIR team for
use when they need to experiment with a new approach.                       their helpful comments. We also appreciate the valuable input from
   Meanwhile, though our studies mostly explored how humans                 our study participants.
use pre-defined LLM Chains, a natural follow-up question becomes
whether end users can effectively author their own LLM Chains.              REFERENCES
Indeed, one potential downside of Chaining is that it may decrease           [1] [n. d.]. GPT-3 is an idea machine. https://interconnected.org/home/2020/09/04/
                                                                                 idea_machine. Accessed: 2021-08-23.
transparency if the pre-built Chain does not match the way a user            [2] [n. d.]. Prompt design 101. https://beta.openai.com/docs/introduction/prompt-
would naturally break down the task (mentioned in Section 5.3.6).                design-101. Accessed: 2021-08-07.
                                                                             [3] [n. d.]. A Recipe For Arbitrary Text Style Transfer With Large Language Models.
We believe our operations can serve as a starting point for future               https://www.gwern.net/GPT-3. Accessed: 2021-08-01.
work on authoring. With the templates, users could instantiate an            [4] Jiban Adhikary, Jamie Berger, and Keith Vertanen. 2021. Accelerating Text Com-
LLM step by defining the data layers and selecting the operations.               munication via Abbreviated Sentence Input. In Proceedings of the Joint Conference
                                                                                 of the 59th Annual Meeting of the Association for Computational Linguistics and
In our study, most participants were able to spot deficiencies and               the 11th International Joint Conf erence on Natural Language Processing.
refine the default Chains accordingly. Thus, we envision that a set          [5] Saleema Amershi, Daniel S. Weld, Mihaela Vorvoreanu, Adam Fourney, Besmira
of generic default Chains could help onboard end users to the idea               Nushi, Penny Collisson, Jina Suh, Shamsi T. Iqbal, Paul N. Bennett, Kori Inkpen,
                                                                                 Jaime Teevan, Ruth Kikin-Gil, and Eric Horvitz. 2019. Guidelines for Human-
of LLM Chaining, and inspire them to author more tailored Chains.                AI Interaction. In Proceedings of the 2019 CHI Conference on Human Factors in
We leave end user authoring of Chains to future work.                            Computing Systems, CHI 2019, Glasgow, Scotland, UK, May 04-09, 2019, Stephen A.
                                                                                 Brewster, Geraldine Fitzpatrick, Anna L. Cox, and Vassilis Kostakos (Eds.). ACM,
   Enhancing LLM Chain design and refinement. Our work centered                  3. https://doi.org/10.1145/3290605.3300233
                                                                             [6] Gagan Bansal, Tongshuang Wu, Joyce Zhou, Raymond Fok, Besmira Nushi, Ece
mostly on moderately complex tasks that can be naturally broken                  Kamar, Marco Tulio Ribeiro, and Daniel Weld. 2021. Does the whole exceed
down. However, decomposition might be less straightforward in                    its parts? the effect of ai explanations on complementary team performance. In
some cases [34]. Tasks with more complex interdependence may                     Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems.
                                                                                 1–16.
lose coherence and quality if they are split into independent sub-           [7] Emily M. Bender and Alexander Koller. 2020. Climbing towards NLU: On Mean-
parts. For example, in the Review task (Figure 1), we treated the                ing, Form, and Understanding in the Age of Data. In Proceedings of the 58th
different problems independently. However, if the problems are                   Annual Meeting of the Association for Computational Linguistics. Association for
                                                                                 Computational Linguistics, Online, 5185–5198.
interrelated, keeping them together would promote more effective             [8] Michael S Bernstein, Greg Little, Robert C Miller, Björn Hartmann, Mark S
suggestions (e.g., not engaging and speaks too quietly). Moreover,               Ackerman, David R Karger, David Crowell, and Katrina Panovich. 2010. Soylent:
                                                                                 a word processor with a crowd inside. In Proceedings of the 23nd annual ACM
while users had the option of excluding specific data layers along               symposium on User interface software and technology. 313–322.
the way (e.g., the original review in Figure 1 is not fed into the           [9] Gregor Betz, Kyle Richardson, and Christian Voigt. 2021. Thinking Aloud: Dy-
final step), the information loss may also lead to task distortion               namic Context Generation Improves Zero-Shot Reasoning Performance of GPT-2.
                                                                                 arXiv preprint arXiv:2103.13033 (2021).
or compression [55]. In light of these issues, future work could            [10] Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora,
investigate how to assist users in crafting the steps of a Chain                 Sydney von Arx, Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                                               Tongshuang Wu, Michael Terry, and Carrie J. Cai


     Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon,                   conference on human factors in computing systems. 3169–3178.
     Niladri Chatterji, Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora Dem-             [26] Luciano Floridi and Massimo Chiriatti. 2020. GPT-3: Its nature, scope, limits, and
     szky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John                       consequences. Minds and Machines 30, 4 (2020), 681–694.
     Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren              [27] Katy Ilonka Gero and Lydia B. Chilton. 2019. Metaphoria: An Algorithmic
     Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha, Tatsunori                    Companion for Metaphor Creation. In Proceedings of the 2019 CHI Conference
     Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu,                  on Human Factors in Computing Systems, CHI 2019, Glasgow, Scotland, UK, May
     Jing Huang, Thomas Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth             04-09, 2019, Stephen A. Brewster, Geraldine Fitzpatrick, Anna L. Cox, and Vassilis
     Karamcheti, Geoff Keeling, Fereshte Khani, Omar Khattab, Pang Wei Kohd, Mark                  Kostakos (Eds.). ACM, 296. https://doi.org/10.1145/3290605.3300526
     Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal Ladhak, Mina              [28] Spence Green, Jason Chuang, Jeffrey Heer, and Christopher D Manning. 2014.
     Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li, Xuechen Li, Tengyu              Predictive translation memory: A mixed-initiative system for human language
     Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani, Eric Mitchell, Zanele               translation. In Proceedings of the 27th annual ACM symposium on User interface
     Munyikwa, Suraj Nair, Avanika Narayan, Deepak Narayanan, Ben Newman,                          software and technology. 177–187.
     Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan, Julian Nyarko, Giray Ogut,            [29] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn
     Laurel Orr, Isabel Papadimitriou, Joon Sung Park, Chris Piech, Eva Portelance,                Song, and Jacob Steinhardt. 2020. Measuring massive multitask language under-
     Christopher Potts, Aditi Raghunathan, Rob Reich, Hongyu Ren, Frieda Rong,                     standing. arXiv preprint arXiv:2009.03300 (2020).
     Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher Ré, Dorsa Sadigh, Shiori              [30] Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. 2020. The
     Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, Alex Tamkin, Ro-                    Curious Case of Neural Text Degeneration. In 8th International Conference on
     han Taori, Armin W. Thomas, Florian Tramèr, Rose E. Wang, William Wang,                       Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020.
     Bohan Wu, Jiajun Wu, Yuhuai Wu, Sang Michael Xie, Michihiro Yasunaga, Ji-                     OpenReview.net. https://openreview.net/forum?id=rygGQyrFvH
     axuan You, Matei Zaharia, Michael Zhang, Tianyi Zhang, Xikun Zhang, Yuhui                [31] Cheng-Zhi Anna Huang, Hendrik Vincent Koops, Ed Newton-Rex, Monica Din-
     Zhang, Lucia Zheng, Kaitlyn Zhou, and Percy Liang. 2021. On the Opportunities                 culescu, and Carrie J Cai. 2020. AI song contest: Human-AI co-creation in
     and Risks of Foundation Models. arXiv:2108.07258 [cs.LG]                                      songwriting. arXiv preprint arXiv:2010.05388 (2020).
[11] Gwern Branwen. 2020. GPT-3 creative fiction. (2020).                                     [32] Ellen Jiang, Edwin Toh, Alejandra Molina, Aaron Donsbach, Carrie J Cai, and
[12] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan,                       Michael Terry. 2021. Genline and genform: Two tools for interacting with gener-
     Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda                    ative language models in a code editor. In Adjunct Publication of the 34rd Annual
     Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan,                 ACM Symposium on User Interface Software and Technology.
     Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter,               [33] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu.
     Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin               2016. Exploring the limits of language modeling. arXiv preprint arXiv:1602.02410
     Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya                     (2016).
     Sutskever, and Dario Amodei. 2020. Language Models are Few-Shot Learners.                [34] Joy Kim, Sarah Sterman, Allegra Argent Beal Cohen, and Michael S Bernstein.
     In Advances in Neural Information Processing Systems 33: Annual Conference on                 2017. Mechanical novel: Crowdsourcing complex work through reflection and re-
     Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020,                vision. In Proceedings of the 2017 acm conference on computer supported cooperative
     virtual, Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina                   work and social computing. 233–245.
     Balcan, and Hsuan-Tien Lin (Eds.). https://proceedings.neurips.cc/paper/2020/            [35] Aniket Kittur, Boris Smus, Susheel Khamkar, and Robert E Kraut. 2011. Crowd-
     hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html                                           forge: Crowdsourcing complex work. In Proceedings of the 24th annual ACM
[13] Daniel Buschek, Lukas Mecke, Florian Lehmann, and Hai Dang. 2021. Nine                        symposium on User interface software and technology. 43–52.
     Potential Pitfalls when Designing Human-AI Co-Creative Systems. arXiv preprint           [36] Janin Koch, Andrés Lucero, Lena Hegemann, and Antti Oulasvirta. 2019. May
     arXiv:2104.00358 (2021).                                                                      AI?: Design Ideation with Cooperative Contextual Bandits. In Proceedings of the
[14] Carrie J Cai, Philip J Guo, James Glass, and Robert C Miller. 2014. Wait-learning:            2019 CHI Conference on Human Factors in Computing Systems, CHI 2019, Glasgow,
     leveraging conversational dead time for second language education. In CHI’14                  Scotland, UK, May 04-09, 2019, Stephen A. Brewster, Geraldine Fitzpatrick, Anna L.
     Extended Abstracts on Human Factors in Computing Systems. 2239–2244.                          Cox, and Vassilis Kostakos (Eds.). ACM, 633. https://doi.org/10.1145/3290605.
[15] Carrie J Cai, Shamsi T Iqbal, and Jaime Teevan. 2016. Chain reactions: The impact             3300863
     of order on microtask chains. In Proceedings of the 2016 CHI Conference on Human         [37] Anand Pramod Kulkarni, Matthew Can, and Bjoern Hartmann. 2011. Turkomatic:
     Factors in Computing Systems. 3143–3154.                                                      automatic, recursive task and workflow design for mechanical turk. In Workshops
[16] Carrie J Cai, Emily Reif, Narayan Hegde, Jason Hipp, Been Kim, Daniel Smilkov,                at the Twenty-Fifth AAAI Conference on Artificial Intelligence.
     Martin Wattenberg, Fernanda Viegas, Greg S Corrado, Martin C Stumpe, et al.              [38] Edith Law and Haoqi Zhang. 2011. Towards Large-Scale Collaborative Planning:
     2019. Human-centered tools for coping with imperfect algorithms during medical                Answering High-Level Search Queries Using Human Computation. In Proceedings
     decision-making. In Proceedings of the 2019 CHI Conference on Human Factors in                of the Twenty-Fifth AAAI Conference on Artificial Intelligence, AAAI 2011, San
     Computing Systems. 1–14.                                                                      Francisco, California, USA, August 7-11, 2011, Wolfram Burgard and Dan Roth
[17] Julia Cambre, Scott Klemmer, and Chinmay Kulkarni. 2018. Juxtapeer: Compara-                  (Eds.). AAAI Press. http://www.aaai.org/ocs/index.php/AAAI/AAAI11/paper/
     tive peer review yields higher quality feedback and promotes deeper reflection.               view/3675
     In Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems.         [39] Ariel Levy, Monica Agrawal, Arvind Satyanarayan, and David Sontag. 2021.
     1–13.                                                                                         Assessing the Impact of Automated Suggestions on Decision Making: Domain
[18] John M Carroll and Judith Reitman Olson. 1988. Mental models in human-                        Experts Mediate Model Errors but Take Less Initiative. In Proceedings of the 2021
     computer interaction. Handbook of human-computer interaction (1988), 45–65.                   CHI Conference on Human Factors in Computing Systems. 1–13.
[19] Qing Chen, Fuling Sun, Xinyue Xu, Jiazhe Wang, and Nan Cao. 2021. VizLinter:             [40] Opher Lieber, Or Sharir, Barak Lenz, and Yoav Shoham. 2021. Jurassic-1: Technical
     A Linter and Fixer Framework for Data Visualization. IEEE transactions on                     Details And Evaluation. Technical Report. AI21 Labs.
     visualization and computer graphics (2021).                                              [41] Rensis Likert. 1932. A technique for the measurement of attitudes. Archives of
[20] Justin Cheng, Jaime Teevan, Shamsi T. Iqbal, and Michael S. Bernstein. 2015. Break            psychology (1932).
     It Down: A Comparison of Macro- and Microtasks. In Proceedings of the 33rd               [42] Greg Little, Lydia B Chilton, Max Goldman, and Robert C Miller. 2010. Turkit:
     Annual ACM Conference on Human Factors in Computing Systems, CHI 2015, Seoul,                 human computation algorithms on mechanical turk. In Proceedings of the 23nd
     Republic of Korea, April 18-23, 2015, Bo Begole, Jinwoo Kim, Kori Inkpen, and                 annual ACM symposium on User interface software and technology. 57–66.
     Woontack Woo (Eds.). ACM, 4061–4064. https://doi.org/10.1145/2702123.2702146             [43] Jiachang Liu, Dinghan Shen, Yizhe Zhang, Bill Dolan, Lawrence Carin, and
[21] Lydia B Chilton, James A Landay, and Daniel S Weld. 2016. Humortools: A                       Weizhu Chen. 2021. What Makes Good In-Context Examples for GPT-3? arXiv
     microtask workflow for writing news satire. El Paso, Texas: ACM (2016).                       preprint arXiv:2101.06804 (2021).
[22] Lydia B. Chilton, Greg Little, Darren Edge, Daniel S. Weld, and James A. Landay.         [44] Ryan Louie, Andy Coenen, Cheng Zhi Huang, Michael Terry, and Carrie J. Cai.
     2013. Cascade: crowdsourcing taxonomy creation. In 2013 ACM SIGCHI Confer-                    2020. Novice-AI Music Co-Creation via AI-Steering Tools for Deep Generative
     ence on Human Factors in Computing Systems, CHI ’13, Paris, France, April 27 -                Models. In CHI ’20: CHI Conference on Human Factors in Computing Systems,
     May 2, 2013, Wendy E. Mackay, Stephen A. Brewster, and Susanne Bødker (Eds.).                 Honolulu, HI, USA, April 25-30, 2020, Regina Bernhaupt, Florian ’Floyd’ Mueller,
     ACM, 1999–2008. https://doi.org/10.1145/2470654.2466265                                       David Verweij, Josh Andres, Joanna McGrenere, Andy Cockburn, Ignacio Avellino,
[23] Elizabeth Clark, Anne Spencer Ross, Chenhao Tan, Yangfeng Ji, and Noah A                      Alix Goguey, Pernille Bjøn, Shengdong Zhao, Briane Paul Samson, and Rafal
     Smith. 2018. Creative writing with a machine in the loop: Case studies on slogans             Kocielnik (Eds.). ACM, 1–13. https://doi.org/10.1145/3313831.3376739
     and stories. In 23rd International Conference on Intelligent User Interfaces. 329–340.   [45] Yao Lu, Max Bartolo, Alastair Moore, Sebastian Riedel, and Pontus Stenetorp.
[24] Nicholas Davis, Chih-PIn Hsiao, Kunwar Yashraj Singh, Lisa Li, and Brian                      2021. Fantastically Ordered Prompts and Where to Find Them: Overcoming
     Magerko. 2016. Empirically studying participatory sense-making in abstract                    Few-Shot Prompt Order Sensitivity. arXiv preprint arXiv:2104.08786 (2021).
     drawing with a co-creative cognitive agent. In Proceedings of the 21st International     [46] Päivi Majaranta and Kari-Jouko Räihä. 2007. Text entry by gaze: Utilizing eye-
     Conference on Intelligent User Interfaces. 196–207.                                           tracking. Text entry systems: Mobility, accessibility, universality (2007), 175–187.
[25] Darren Edge, Elly Searle, Kevin Chiu, Jing Zhao, and James A Landay. 2011.
     MicroMandarin: mobile language learning in context. In Proceedings of the SIGCHI
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                                                CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA


[47] Swaroop Mishra, Daniel Khashabi, Chitta Baral, and Hannaneh Hajishirzi. 2021.       [60] Ben Swanson, Kory Mathewson, Ben Pietrzak, Sherol Chen, and Monica Di-
     Cross-Task Generalization via Natural Language Crowdsourcing Instructions.               nalescu. 2021. Story Centaur: Large Language Model Few Shot Learning as
     arXiv preprint arXiv:2104.08773 (2021).                                                  a Creative Writing Tool. In Proceedings of the 16th Conference of the Euro-
[48] Dominik Moritz, Chenglong Wang, Greg L Nelson, Halden Lin, Adam M Smith,                 pean Chapter of the Association for Computational Linguistics: System Demon-
     Bill Howe, and Jeffrey Heer. 2018. Formalizing visualization design knowledge            strations. Association for Computational Linguistics, Online, 244–256. https:
     as constraints: Actionable and extensible models in draco. IEEE transactions on          //www.aclweb.org/anthology/2021.eacl-demos.29
     visualization and computer graphics 25, 1 (2018), 438–448.                          [61] Bowen Tan, Zichao Yang, Maruan Al-Shedivat, Eric Xing, and Zhiting Hu. 2021.
[49] Hegde Narayan, Jason D Hipp, Yun Liu, Michael Emmert-Buck, Emily Reif, Daniel            Progressive Generation of Long Text with Pretrained Language Models. In Pro-
     Smilkov, Michael Terry, Carrie J Cai, Mahul B Amin, Craig H Mermel, et al. 2019.         ceedings of the 2021 Conference of the North American Chapter of the Association for
     Similar image search for histopathology: SMILY. NPJ Digital Medicine 2, 1 (2019).        Computational Linguistics: Human Language Technologies. Association for Com-
[50] Besmira Nushi, Ece Kamar, Eric Horvitz, and Donald Kossmann. 2017. On                    putational Linguistics, Online, 4313–4324. https://www.aclweb.org/anthology/
     Human Intellect and Machine Failures: Troubleshooting Integrative Machine                2021.naacl-main.341
     Learning Systems. In Proceedings of the Thirty-First AAAI Conference on Ar-         [62] Jaime Teevan, Shamsi T Iqbal, Carrie J Cai, Jeffrey P Bigham, Michael S Bernstein,
     tificial Intelligence, February 4-9, 2017, San Francisco, California, USA, Satin-        and Elizabeth M Gerber. 2016. Productivity decomposed: Getting big things
     der P. Singh and Shaul Markovitch (Eds.). AAAI Press, 1017–1025. http:                   done with little microtasks. In Proceedings of the 2016 CHI Conference Extended
     //aaai.org/ocs/index.php/AAAI/AAAI17/paper/view/15032                                    Abstracts on Human Factors in Computing Systems. 3500–3507.
[51] Joe O’Connor and Jacob Andreas. 2021. What Context Features Can Transformer         [63] Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam Shazeer, Apoorv Kul-
     Language Models Use? arXiv preprint arXiv:2106.08367 (2021).                             shreshtha, Heng-Tze Cheng, Alicia Jin, Taylor Bos, Leslie Baker, Yu Du, et al. 2022.
[52] Changhoon Oh, Jungwoo Song, Jinhan Choi, Seonghyeon Kim, Sungwoo Lee, and                LaMDA: Language Models for Dialog Applications. ArXiv preprint abs/2201.08239
     Bongwon Suh. 2018. I Lead, You Help but Only with Enough Details: Understand-            (2022). https://arxiv.org/abs/2201.08239
     ing User Experience of Co-Creation with Artificial Intelligence. In Proceedings     [64] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
     of the 2018 CHI Conference on Human Factors in Computing Systems, CHI 2018,              Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. 2017. Attention is All you
     Montreal, QC, Canada, April 21-26, 2018, Regan L. Mandryk, Mark Hancock, Mark            Need. In Advances in Neural Information Processing Systems 30: Annual Conference
     Perry, and Anna L. Cox (Eds.). ACM, 649. https://doi.org/10.1145/3173574.3174223         on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach,
[53] Marc’Aurelio Ranzato, Sumit Chopra, Michael Auli, and Wojciech Zaremba. 2016.            CA, USA, Isabelle Guyon, Ulrike von Luxburg, Samy Bengio, Hanna M. Wallach,
     Sequence Level Training with Recurrent Neural Networks. In 4th International             Rob Fergus, S. V. N. Vishwanathan, and Roman Garnett (Eds.). 5998–6008.
     Conference on Learning Representations, ICLR 2016, San Juan, Puerto Rico, May       [65] Vasilis Verroios and Michael S Bernstein. 2014. Context trees: Crowdsourcing
     2-4, 2016, Conference Track Proceedings, Yoshua Bengio and Yann LeCun (Eds.).            global understanding from local views. In Second AAAI Conference on Human
     http://arxiv.org/abs/1511.06732                                                          Computation and Crowdsourcing.
[54] Daniela Retelny, Michael S Bernstein, and Melissa A Valentine. 2017. No workflow    [66] Cunxiang Wang, Boyuan Zheng, Yuchen Niu, and Yue Zhang. 2021. Exploring
     can ever be enough: How crowdsourcing workflows constrain complex work.                  Generalization Ability of Pretrained Language Models on Arithmetic and Logical
     Proceedings of the ACM on Human-Computer Interaction 1, CSCW (2017), 1–23.               Reasoning. arXiv preprint arXiv:2108.06743 (2021).
[55] Laria Reynolds and Kyle McDonell. 2021. Prompt programming for large language       [67] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le,
     models: Beyond the few-shot paradigm. In Extended Abstracts of the 2021 CHI              and Denny Zhou. 2022. Chain of Thought Prompting Elicits Reasoning in Large
     Conference on Human Factors in Computing Systems. 1–7.                                   Language Models. arXiv preprint arXiv:2201.11903 (2022).
[56] Daniel Rough, Keith Vertanen, and Per Ola Kristensson. 2014. An evaluation          [68] Sean Welleck, Ilia Kulikov, Jaedeok Kim, Richard Yuanzhe Pang, and Kyunghyun
     of Dasher with a high-performance language model as a gaze communication                 Cho. 2020. Consistency of a Recurrent Language Model With Respect to Incom-
     method. In Proceedings of the 2014 International Working Conference on Advanced          plete Decoding. In Proceedings of the 2020 Conference on Empirical Methods in
     Visual Interfaces. 169–176.                                                              Natural Language Processing (EMNLP). Association for Computational Linguistics,
[57] Arvind Satyanarayan, Dominik Moritz, Kanit Wongsuphasawat, and Jeffrey Heer.             Online, 5553–5568. https://doi.org/10.18653/v1/2020.emnlp-main.448
     2016. Vega-lite: A grammar of interactive graphics. IEEE transactions on visual-    [69] Tongshuang Wu, Ellen Jiang, Aaron Donsbach, Jeff Gray, Alejandra Molina,
     ization and computer graphics 23, 1 (2016), 341–350.                                     Michael Terry, and Carrie J Cai. 2022. PromptChainer: Chaining Large Language
[58] Taylor Shin, Yasaman Razeghi, Robert L. Logan IV, Eric Wallace, and Sameer               Model Prompts through Visual Programming. Association for Computing Machin-
     Singh. 2020. AutoPrompt: Eliciting Knowledge from Language Models with Auto-             ery, New York, NY, USA. https://doi.org/10.1145/3491101.3519729
     matically Generated Prompts. In Proceedings of the 2020 Conference on Empirical     [70] Tongshuang Wu, Marco Tulio Ribeiro, Jeffrey Heer, and Daniel Weld. 2021.
     Methods in Natural Language Processing (EMNLP). Association for Computational            Polyjuice: Generating Counterfactuals for Explaining, Evaluating, and Improving
     Linguistics, Online, 4222–4235. https://doi.org/10.18653/v1/2020.emnlp-main.346          Models. In Proceedings of the 59th Annual Meeting of the Association for Computa-
[59] Alison Smith-Renner, Ron Fan, Melissa Birchfield, Tongshuang Wu, Jordan Boyd-            tional Linguistics and the 11th International Joint Conference on Natural Language
     Graber, Daniel S. Weld, and Leah Findlater. 2020. No Explainability without              Processing (Volume 1: Long Papers). Association for Computational Linguistics,
     Accountability: An Empirical Study of Explanations and Feedback in Interactive           Online, 6707–6723. https://doi.org/10.18653/v1/2021.acl-long.523
     ML. Association for Computing Machinery, New York, NY, USA, 1–13. https:            [71] Bingjun Xie, Jia Zhou, and Huilin Wang. 2017. How influential are mental models
     //doi.org/10.1145/3313831.3376624                                                        on interaction performance? exploring the gap between users’ and designers’
                                                                                              mental models through a new quantitative method. Advances in Human-Computer
                                                                                              Interaction 2017 (2017).
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                                    Tongshuang Wu, Michael Terry, and Carrie J. Cai


A     IDENTIFYING
CHI ’22,                        LLM
         April 29-May 5, 2022, New      PRIMITIVE
                                   Orleans, LA, USA OPERATIONS                                                         Tongshuang Wu, Michael Terry, and Carrie J. Cai



         Primitive       Online demos

Info, extraction (9)     plan extraction [55], arithmetic reasoning [70], Keyword-extract, airport-code-extract, contact-info, color scale extractor, read code
                         and answer questions, Summarize restaurant reviews (AI21), table question answering (AI21)
  Classification (6)     hate speech detection [24], tweet-classifier, esrb rating, Automatically generating Request for Admissions, evaluate quiz answers,
                         Classify news topics (AI21)
       Rewrite (26)      program synthesis [6], Wordtune, generate database specific SQL code, parse-understructed-text, text to command, English to French,
                         movie to emoji, tl;dr, sql-request, js-multi-line-to-one-line, js2python, html generation, description to app design description to todo
                         list, Summarize-for-2nd-grade, Grammar-correction, third-person converter, rewrite as an attorney, Simplifying legal language, more
                         polite, summarize famous people thoughts, speak in some personality, rewrite helper, mood color, De-jargonizer (AI21), Convert text
                         to table (AI21)
     Split points (1)    turn-by-turn directions
   Composition (4)       Notes to summary review creator Description to ads Writing full emails from key points
 Factual query (11)      add info to table, table computation, company to categories, factual answer, js-chatbot, ai-chatbot-tutor, sarcastic chatbot, imdb movie
                         link, guess movie, Explain a word (AI21), Sports trivia (AI21)
     Generation (8)      drafting email responses [66], Keyword 2 name, Generate poetry, spreadsheet generator, topic to horror story, Predict the outcome
                         (AI21), project description generator (AI21), generate catchy headline (AI21),
        Ideation (8)     scifi-booklist, essay outline, create study notes, interview questions, content creation for marketing, topic to quiz questions, VR fitness
                         idea illustrator, blog post ideation (AI21)
Table 2: A survey of 73 online demos that inspired the design of our operation, mostly from published manuscripts, the OpenAI
Table 2: A survey of 73 online demos that inspired the design of our operation, mostly from published manuscripts, the OpenAI
official GPT-3 example page, the AI21 tutorial, and the demo collection repository. All the links are last accessed in 2021/08.
official GPT-3 example page, the AI21 tutorial, and the demo collection repository. All the links are last accessed in 2021/08.

   We reviewed 73 existing demos to identify promising LLM capabilities that may help overcome the challenges above by scoping the
A IDENTIFYING
inputs/outputs      to be moreLLM     PRIMITIVE
                                amenable    to what an LLM  OPERATIONS
                                                                 can handle.
WeFirst,  we collected
     reviewed              demos
                  73 existing      fromtoLLM
                                demos            official
                                           identify        websitesLLM
                                                       promising     (e.g., capabilities
                                                                             GPT-3 and Jurassic),
                                                                                           that maysocial     media, andthe
                                                                                                       help overcome       published    caseabove
                                                                                                                               challenges    studiesbyby  searching
                                                                                                                                                        scoping   the
for keywords including
inputs/outputs      to be more“GPT-3,” “language
                                amenable    to whatmodel,”
                                                       an LLM“prompt,”
                                                                 can handle. etc. After removing some demos that were highly open-ended rather than
targeted  (e.g.,collected
   First, we      generic demos
                           chatbots), weLLM
                                   from   iteratively
                                                 officialsorted  the (e.g.,
                                                           websites  demos    into eight
                                                                            GPT-3          LLM primitive
                                                                                     and Jurassic),   social operations,
                                                                                                             media, andas     shown incase
                                                                                                                           published     Table  1. Forby
                                                                                                                                             studies   example,
                                                                                                                                                          searchingwe
distinguished
for keywords between
                  includingoperations  that had different
                              “GPT-3,” “language      model,”expected
                                                                “prompt,” data
                                                                             etc.mappings    (one-to-many
                                                                                  After removing             v.s. many-to-one),
                                                                                                      some demos                   and different
                                                                                                                    that were highly              application
                                                                                                                                          open-ended    rather types
                                                                                                                                                                than
(deterministic     v.s. creative).
targeted (e.g., generic            We we
                           chatbots), then   grouped sorted
                                          iteratively     the primitives
                                                                 the demos  into
                                                                              intothree
                                                                                    eighthigh
                                                                                           LLMlevel   groupsoperations,
                                                                                                 primitive     based on which
                                                                                                                          as shown LLMin challenge
                                                                                                                                         Table 1. Forthey  may help
                                                                                                                                                       example,   we
address.  The groups
distinguished    betweenalso   appear to
                            operations thatbehadconsistent
                                                    differentwith  categories
                                                               expected           presented(one-to-many
                                                                          data mappings        on the GPT-3v.s.tutorial page,6 which
                                                                                                                  many-to-one),           highlighted
                                                                                                                                   and different        typicaltypes
                                                                                                                                                  application    NLP
tasks like Classification,
(deterministic     v.s. creative).       (i.e.,
                                   We then
                              Generation         gather additional
                                             grouped                  information
                                                         the primitives     into threein Table  1b), Transformation
                                                                                         high level   groups based on (i.e., re-organization).
                                                                                                                          which   LLM challenge Finally,
                                                                                                                                                     theywe
                                                                                                                                                          mayfurther
                                                                                                                                                                help
refined
address.the
          Theprimitive     categories
                 groups also   appearand
                                       to benames     basedwith
                                                consistent    on feedback
                                                                   categories from   three pilot
                                                                                 presented        users
                                                                                               on the    (one tutorial
                                                                                                       GPT-3    LLM expert
                                                                                                                        page,and6 which
                                                                                                                                    two UX   engineerstypical
                                                                                                                                         highlighted      with basic
                                                                                                                                                                NLP
knowledge    of LLM prompting).
tasks like Classification,    Generation (i.e., gather additional information in Table 1b), Transformation (i.e., re-organization). Finally, we further
refined the primitive categories and names based on feedback from three pilot users (one LLM expert and two UX engineers with basic
B     ADDITIONAL
knowledge    of LLM prompting).DETAILS FOR USER STUDY
B.1 Questions in the Exit Survey
B ADDITIONAL DETAILS FOR USER STUDY
After completing the given task in both conditions, participants self-rated their experience on the following dimensions, in the form of
B.1 Questions
seven-point  Likert scalein[43].
                             theEach Exitquestion
                                            Survey was asked twice, once on Sandbox and once on Chaining. They described their reasoning along
with
Afterthe ratings. the given task in both conditions, participants self-rated their experience on the following dimensions, in the form of
      completing
seven-point
    • MatchLikert
               goal: scale  [41]. Each
                     I’m satisfied       question
                                      with         was
                                            my final        askedfrom
                                                        results    twice,  once on Sandbox and
                                                                         [ Sandbox/Chaining         oncemet
                                                                                                 ]; they  on Chaining.      They described their reasoning along
                                                                                                               the task goal.
with•the ratings.
       Think  through: The [ Sandbox/Chaining ] system helped me think through what kinds of outputs I would want to complete the task
     • goal,
       Matchand   how
               goal: I’mtosatisfied
                            complete    themy
                                      with   task.
                                                final results from [ Sandbox/Chaining ]; they met the task goal.
    • Transparent:
       Think through: The   [ Sandbox/Chaining
                          The   [ Sandbox/Chaining   ] system
                                                           ] systemis transparent   aboutthrough
                                                                       helped me think    how it arrives   at its of
                                                                                                    what kinds    final  result;I Iwould
                                                                                                                     outputs        could want
                                                                                                                                          roughly  track its progress.
                                                                                                                                               to complete   the task
       goal, and howI felt
    • Controllable:           I had control
                         to complete          creating with the [ Sandbox/Chaining ] system. I can steer the system towards the task goal.
                                        the task.
       Transparent: The
    • Collaborative:    In [ Sandbox/Chaining ],          I felt I was
                                                     ] system           collaborating
                                                                   is transparent      with
                                                                                    about howtheit system  to its
                                                                                                   arrives at  come
                                                                                                                  finalupresult;
                                                                                                                           with Ithe  outputs.
                                                                                                                                    could roughly track its progress.
   Additionally,      I felt I had
                 participants
     • Controllable:                 control
                                   also       creating
                                        answered   the with      the [ two
                                                           following                          ] system. I can steer the system towards the task goal.
                                                                             free form questions:
                                                                        Sandbox/Chaining
       Collaborative:
    •• Difference: What In [were    the differences, ],if Iany,
                              Sandbox/Chaining              felt between
                                                                 I was collaborating   withof
                                                                            the experience   the   system to the
                                                                                                completing    come    upusing
                                                                                                                   task    with the   outputs.
                                                                                                                                  Sandbox   and Chaining?
    Additionally,
      • Vision: If youparticipants
                           were usingalsolanguage
                                          answeredmodels
                                                       the following
                                                              in your two free
                                                                      work,  in form
                                                                                 whatquestions:
                                                                                      situations would you prefer to use Sandbox? Chaining? Can you
      • think     of 1-3What
          Difference:    concrete
                               wereexamples?
                                      the differences, if any, between the experience of completing the task using Sandbox and Chaining?
      • Vision: If you were using language models in your work, in what situations would you prefer to use Sandbox? Chaining? Can you
6 https://beta.openai.com/docs/guides/completion/introduction
          think of 1-3 concrete examples?
6 https://beta.openai.com/docs/guides/completion/introduction
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                           CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA



                                                Unique trait
                                                                                          Metaphor on the concept




                                    Ideation
                                                Wisdom of the crowd           B
                                                                                          People work together like bees to create
                                                Asynchronous                              something greater than the individuals.




                                                                             Generation
                                                Workers are unreliable
          Concept                                                                         A group of people who submit their
                                                                                          answers to a question at different times.
          Crowdsourcing              A
                                                                                          A group of blindfolded people trying to
                                                                                          solve a puzzle.
                                Intermediate data layers


Figure 9: The pipeline for acronym expansion. The steps include: (A) An ideator that brainstorms various •unique traits for
•the concept (crowdsourcing). (B) For each trait, a generator creates a related •metaphor.



B.2     Clickstream Categorization
we log the text status before and after each round of model run. Through sequence match, we recover what’s generated by the model after
each run, and how the participants edit the text in between of two runs. We split the logs into: (1) RUN the model, (2) UNDO the model, where
people removed the generations from the previous run, making the resulting text more similar to prior to the previous run, (3) FORMAT,
where people only add or remove line split or formatting-related stopwords, (4) CREATE-CONTENT, where people only insert meaningful
spans to the text, (5) CURATE-CONTENT, where people make all the other kinds of refinements on the existing text — in Chaining, this is
a merge of changing the instruction, prefix, and the data entries. We also logged (6) CHANGE-TEMPERATURE to denote when people make
non-text based change on the model input, i.e., temperature.
   On top of the logs, we define consecutive runs (in Figure 6A) as those in which users did not change anything after the previous run (or
only add formatting through line changes or adding stopwords, i.e., RUN+FORMAT). Otherwise, the logs are counted as humans making edits.

B.3     Case 0: Metaphor Creation (Used in tutorial)
  Description. Create metaphors for the concept of crowdsourcing, so that we can explain the different aspects of crowdsourcing in a poetic
way. The pipeline is as in Figure 9.
  A metaphor may look like:
             In crowdsourcing, people are like bees; they work together to make honey.
   With the concept being “crowdsourcing”, the simile being “bees”, and the similar aspect being “work together.”

   Default baseline commands.
   (1) In the form of question answering,
       Question: What is a good metaphor for crowdsourcing?
       Answer: a swarm of bees.
   (2) In the form of command instruction,
       Write a metaphor for the concept of crowdsourcing.
       Concept: crowdsourcing
       Metaphor: Crowdsourcing is like a game of chess. A crowdsourcer’s skills, as in a chess player’s skills, are combined with
       another person’s skills to make something new.
   (3) List enumeration
       The following is a list of metaphors on crowdsourcing.
       1. Crowdsourcing is like a beehive – Many people (bees) contribute to a larger cause.
   (4) Few-shot example,
       Concept: gratitude
       Metaphor: gratitude is like a stream in that it’s a force that can carry you along.
       ###
       Concept: loss
       Metaphor: loss is like a wing in that it’s something you never wanted to lose, and it can take you away.
       ###
       Concept: crowdsourcing
       Metaphor:crowdsourcing is like a team sport in that it brings people to achieve one goal.
CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA                                                       Tongshuang Wu, Michael Terry, and Carrie J. Cai


B.4     Case 1: Flashcard Creation
   Description. Suppose you will be traveling to Paris next week, and you would like to create flashcards to learn about some basic French
so you can have basic conversations with local people whenever you are in a non-English speaking region. Your goal is to create flashcards
that are both diverse and personalized to your travel desires.
   A flashcard may look like:
             English: Where is a good restaurant?; French: Où est un bon restaurant?

   Default baseline commands. we offer three versions:
   (1) In the form of question answering,
        Question: What are some English and French sentence pairs useful for traveling to Paris?
        Answers:
        English: Where is a good restaurant?
        French: Où est un bon restaurant?
   (2) In the form of list enumeration,
        The following are English and French sentence pairs useful for traveling to Paris.
        1. Que fais-tu ici? / What are you doing here?
   (3) Few-shot example,
        English: I do not speak French.
        French: Je ne parle pas français.
        ###
        English: Where is a good restaurant?
        French: Où est un bon restaurant?
        ###
        English: Where’s the bus station?
        French: Où est la gare routière?


B.5     Case 2: Peer Review Paragraph Rewriting
  Description. The following is a peer review paragraph on Alex’s presentation. Please rewrite it to be more friendly and constructive.
The paragraph should include 1-3 concrete and actionable suggestions for each of Alex’s presentation problems.Original feedback:
             Alex could improve his presentation skills. He has too much text on his slides. His presentation meanders from topic to topic without
             a clear structure. He also does not engage with his audience when he presents.
   An example output from the language model:
             Alex, you have a lot of good ideas in your presentations. However, your slides are too cluttered with text. I would recommend that
             you use more graphics, pictures, and white space. Your slides should be simple enough that you could read your presentation off of
             the slides. This will allow you to engage the audience and not have to read from your notes. Also, you need to have a clear structure
             to your presentation. Lastly, you need to practice speaking. This will familiarize you with the material and reduce the likelihood of
             you meandering.

   Default baseline commands. we offer two versions:
   (1) End-to-end version,
        Given the feedback, rewrite it into a friendly paragraph with concrete suggestions on each of Alex’s presentation problems.
        Feedback: Alex could improve his presentation skills. He has too much text on his slides. His presentation meanders from
        topic to topic without a clear structure. He also does not engage with his audience when he presents.
        Friendly paragraph: [LLM generation]
   (2) Two-step version, where we query LLM for improvement suggestions first, and then ask it to integrate the problem and the suggestion.
        Alex could improve his presentation skills. He has too much text on his slides. His presentation meanders from topic to
        topic without a clear structure. He also does not engage with his audience when he presents.
        Give Alex some suggestions on his presentation:
        1. [LLM generation]
        Write one friendly paragraph that covers all the presentation problems and suggestions:[LLM generation]
Transparent and Controllable Human-AI Interaction by Chaining LLM Prompts                                                                                                                                   CHI ’22, April 29-May 5, 2022, New Orleans, LA, USA


C           FULL LLM CHAINS FOR CASE STUDIES

        VegaLite Spec                                                                                                                                                      Fixed VegaLite Spec
                                                     6/3/2021                                                                                                Chart                                             6/3/2021                                                         Chart
        "mark": “point"                                                                                                                                                    "mark": “point"
        "encoding":                 50
                                                                                                                            Origin                           D             "encoding":                                                                               Origin
                                                                                                                                                                                                      40                                                               Europe
         "x": {                                                                                                                  Europe                                     "x": {




                                                                                                                                                                                                                  Mean of Miles_per_Gallon
                                                                                                                                 Japan                                                                                                                                 Japan
           "field": "Horsepower",   40                                                                                                                                        "field": "Horsepower",




                                                                                                                                                       Rewriting
                                                                                                                                                                                                                                                                       USA
           "type": "quantitative"                                                                                                USA                                          "type": "quantitative" 30
                                                        Miles_per_Gallon
         },                         30                                                                                                                                      },
         “size": {                                                                                                                                                          “size→color": {
                                                                                                                                                                                                      20
           "field": "Origin",       20                                                                                                                                        "field": "Origin",
           "type": "nominal"                                                                                                                                                  "type": "nominal"
         }                          10                                                                                                                                      }                         10
         "y": {                                                                                                                                                             "y": {
           "type": "quantitative", 0                                                                                                                                          "type": "quantitative", 0
           "aggregate": "mn"           0                                                   50    100    150    200                                                            "aggregate":"mn→mean"      0                                   50    100   150   200
           "field": "Miles_per_Gallon"                                                          Horsepower                                                                    "field": "Miles_per_Gallon"                                         Horsepower


        }                                                                                                                                                                  }




                           A                                                                                                                                                     C
                                                 Visualization description                                                                                                                      Validation result and suggested x




                                                                                                                                                                               classi cation
                                                                                                                                                                                                Invalid.
                         Rewriting




                                                 A) [mark type: point] has [x: quantitative],
                                                                                                                                                                                                On [encoding: size], [encoding: size]
                                                    [y: quantitative], [size: nominal]
                                                                                                                                                                                                conflicts with [data type: nominal]. Change
                                                 B) [encoding: x] has [data type: quantitative
                                                                                                                                                                                                [encoding: size] to [encoding: color]
                                                 C) [encoding: y] has [data type: quantitative,
                                                                                                                                                                                                On [encoding: y], [aggregate: mn] is not
                                                    aggregate: mn
                                                                                                                                                                                                parsable. Change [aggregate: mn] to
                                                 D) [encoding: size] has [data type: nominal]
                                                                                                                                                                                                [aggregate: mean].

                                                                                                                                                B
        All visualization constraints
                                                                                                                                                                        Relevant visualization constraints
                                                                                                                                                   Extract
                                                                                                                                              Rewriting




        1) [mark type: line] is invalid, if it does not
           have both [x] and [y]                                                                                                                                         1) [encoding: size] is invalid, when having [data
        2) [scale type: log] is invalid, if it does not                                                                                                                     type: quantitative]
                                                                                                                                                                         2) [aggregate] has to be count, mean, max, min,
                                                                                                                                             Info.




           have [data type: quantitative]
        3) [aggregate] has to be count, mean, max, min,                                                                                                                     sum, stdev
           sum, stdev
        4) ...
                                                                                                                                                                                                                                                     Intermediate data layers



Figure 10: The LLM Chain for visualization bug fixing (in VegaLite). The stages include: (A) A Rewrite step that transforms the
•json format VegaLite spec into •natural language description, so to eliminate noise from data. (B) An Information Extraction
step that locate •related visualization rules. (C) A Classification step that verifies the description as either •valid or invalid
(with concrete errors and fixes). (D) A Rewriting step that generates •the fixed VegaLite spec based on the •validity reasons.
}
,
        fi    
 .
 {
]
          ,
.
 .
,
         fi .
                      .
       .
      ]



                                                     about:blank                                                                                                                                                    1/1
                                                                                                                                                                                                               about:blank



                                                                                                                                                                     Intermediate data layers
                                                                           classi cation




                                                                                                                                                                                               Generation
                                                                                                                     Rewriting




       Shorthand sentence                                                                       Shorthand                                 Expanded sentence                                                     Full sentence w/ suggestion
       LTSGCHKITOT                                                                                                                        Let’s go CHKITOT                                                       Let’s go check it out tomorrow




                                                                             A                                         B                                                                         C



                                                                                                              Phrase Let’s go check it out


Figure 11: The LLM Chain for assisted text entry. The stages include: (A) A Classification steps that detects whether a
•given sentence •contains a shorthand or not. (B) If there exists certain shorthand, a Rewriting step expands it, so we arrive
at the •expanded sentence which can become the context for additional shorthand inputs. For “LTSG”, it can be “Let’s go” or
“Let’s get”, which relies on human selection. (C) Otherwise, a Generation step autocompletes •the sentence.
CHI
 CHI’22,
      ’22,April
           April29-May
                 29-May5,5,2022,
                            2022,New
                                  NewOrleans,
                                      Orleans,LA,
                                               LA,USA
                                                   USA                                                         Tongshuang
                                                                                                                TongshuangWu,
                                                                                                                           Wu,Michael
                                                                                                                               MichaelTerry, and
                                                                                                                                        Terry,   Carrie
                                                                                                                                               and      J. J.
                                                                                                                                                   Carrie  CaiCai


DD THE
    THEFULL
        FULLIMPLEMENTATION
             IMPLEMENTATIONOF
                            OFPRIMITIVE
                               PRIMITIVEOPERATIONS
                                         OPERATIONS

  Prompt template                                             Example                                                                                     T
  Classification: Assign the input based on limited categories. Most useful for branching logics and validation.
 Instruct Classify if [detail-1] [detail-2].                  Classify if the question is answerable.                                                      0
   Input [prefix-1]: (str)                                    question: What is the square root of banana
  output [prefix-2]: (str)                                    is answerable (Yes/No): No
                   (a) Primitive for examining the given input, to judge its value (potentially with reasoning), and what to do next.

  Information Extraction: Gather some information from the context.
 Instruct Given [detail-1], extract [detail-2].               Given text, extract airport codes for the cities.                                           0.2
   Input [prefix-1]: (string)                                 text: I want to fly from Los Angeles to Miami.
  output [prefix-2]: (string)                                 airport codes: LAX, MIA
  Rewriting: 1-1 mapping that changes the input to more machine-readable formats (e.g. json to natural language).
 Instruct Rewrite [detail-1] into [detail-2].                 Rewrite the first-person text into third-person text.                                       0.3
   Input [prefix-1]: (string)                                 first-person text: I decide to make a movie
  output [prefix-2]: (string)                                 third-person text: He decides to make a movie.
  Split Points: 1-N mapping that is particularly useful for splitting contexts.
 Instruct Split [detail-1] into                a    list   of Split the descriptions on the direction into a list of turn-by-turn directions. 0.3
          [detail-2].
   Input [prefix-1]: (string)                                 Direction description: Go south on 95 until you hit Sunrise Blvd, then take it
                                                              east to US-1 and head south.
  output [prefix-2]: 1.(list of strings)                      turn-by-turn directions: 1. Drive south on 95.
                                                              2. Turn left onto Sunrise Blvd.
                                                              3. Turn left onto US-1 SE.
  Compose Points: N-1 mapping, the reverse operation of decomposition; merge multiple results back.
 Instruct Write one [detail-1] to cover all the Write one review to cover all the restaurant name and notes.                                              0.5
          [detail-2].
   Input [prefix-1]: (list of strings)          Restaurant name: The Blue Wharf
                                                Short notes: 1. Lobster great; 2.noisy; 3.service polite
  output [prefix-2]: (string)                   Review: The place is great if you like lobster. The noise level
                                                is a little high, but the service is polite.
                 (b) Primitives for reorganizing the given input, and re-format it by parsing and expressing them in different ways.

  Factual Query: Ask the model for a fact.
 Instruct Given [detail-1], find [detail-2].                  Given the US state, find the population.                                                    0.3
   Input [prefix-1]: (string)                                 US state: Washington
  output [prefix-2]: (string)                                 Population: 7.6 million
  Generation: Ask the model to do some creative “hallucination” on the input.
 Instruct Given [detail-1], create [detail-2].                Given the topic, create a two-sentence horror story.                                        0.7
   Input [prefix-1]: (string)                                 topic: Breakfast
  output [prefix-2]: (string)                                 two-sentence horror story: He always stops crying when I pour
                                                              the milk on his cereal. I just have to remember not to let him
                                                              see his face on the carton.
  Ideation: Ask the model for a list of ideas or examples.
 Instruct Given [detail-1], the following is a list Given the interviewee, the following is a list of interview questions.                                0.7
          of [detail-2].
   Input [prefix-1]: (string)                       Interviewee: A science fiction author
  output [prefix-2]: 1.(list of strings)            Interview questions: 1. What’s your favorite sci-fi book?
                                                    2. Who inspired you to start writing books?
                    (c) Primitives for gathering additional clues from LLMs, when the desired output is too longer or too diverse.

Table
 Table3:3:We
          Wedesign
              designaalist
                       listofofprimitive
                                primitivebuilding
                                          buildingblocks,
                                                   blocks,each
                                                           eachwith
                                                                withdefault
                                                                     defaultprompting
                                                                              promptingtemplates
                                                                                        templatesand
                                                                                                  andtemperatures,
                                                                                                      temperatures,and
                                                                                                                    andgroup
                                                                                                                        group
them
 thembybytheir
           theirintended
                 intendedobjectives.
                           objectives.Examples
                                       Examplesare
                                                 aretaken
                                                     takenfrom
                                                           fromhttps://beta.openai.com/examples.
                                                                https://beta.openai.com/examples.
