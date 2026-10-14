                                                       Planning in the LLM Era: Building for Reliability and Efficiency

                                                                   Michael Katz, Harsha Kokel, Kavitha Srinivas, Shirin Sohrabi
                                                                                                        IBM Research




                                                                     Abstract
arXiv:2605.21902v1 [cs.AI] 21 May 2026




                                           Growing attention to intelligent agents has put a spotlight on
                                           one of their central capabilities: planning. Early attempts to
                                           leverage large language models (LLMs) for planning relied on
                                           single-shot plan generation, followed by hybrid approaches
                                           that coupled LLMs with limited external search. These meth-
                                           ods, unsound and incomplete by their very nature, often re-
                                           quire substantial resources without yielding better solutions on
                                           unseen problems. As the limitations of LLMs become clearer,
                                           recent work has shifted toward using them at solution con-
                                           struction time – generating symbolic solvers for a family of
                                           problems that can be verified and then used efficiently at in-
                                           ference time. This trend reflects the growing need for agents
                                           that are both reliable and resource-efficient. It also offers a
                                           path towards generating maintainable planners with minimal            Figure 1: An overview of the planner generation methods
                                           dependence on language models at inference time. In this pa-
                                           per, we argue that this shift reflects a broader realignment of
                                           the planning field in the LLM era. We examine three major
                                           categories of planner-generation methods, discuss their current      Seipp 2025a). Hybrid methods that incorporated restricted
                                           limitations, and outline research steps towards a more reliable      forms of backtracking or external search into LLM-based
                                           and efficient LLM-based generation of planners.                      exploration (Yao et al. 2023; Besta et al. 2024; Sel et al.
                                                                                                                2023) are unsound and incomplete, and often require dra-
                                                                 Introduction                                   matically more LLM calls without delivering reliably better
                                                                                                                performance (Katz et al. 2024). Further, all that hard work is
                                         Planning is one of the defining capabilities of intelligent            wasted – each problem is solved separately and no computa-
                                         agents, enabling them to reason about actions, anticipate their        tion is reused for the next problem in the same dataset.
                                         consequences, and synthesize solutions that achieve com-
                                         plex goals. This recognition has recently brought renewed                 These realizations, coupled with increased awareness of
                                         attention to planning within the broader surge of interest in          the environmental and monetary costs of LLM inference gave
                                         language-driven agents. Early attempts to use large language           rise to the emergence of a promising paradigm: instead of
                                         models (LLMs) for planning treated each task independently             relying on LLMs at inference time, use them at construction
                                         by prompting the model to generate entire plans in a single            time. In this view, LLMs are not planners themselves but
                                         step (Silver et al. 2022; Valmeekam et al. 2023a,b; Kambham-           generators of domain-specific planners that can be validated,
                                         pati et al. 2024). These approaches achieved limited success           maintained, and run efficiently without repeated model calls.
                                         on simple problems but quickly revealed fundamental lim-               This shift is visible across multiple lines of work. In this
                                         itations: the inability to reconsider earlier decisions, poor          position paper, we discuss three directions outlined in Figure
                                         long-horizon reasoning, and difficulty generalizing to unseen          1. Search-based planner generation (NL2Search) uses LLMs
                                         instances. More recent evaluations of frontier models reflect          to generate code for search components, i.e., successor gen-
                                         the rapid and multifaceted nature of progress in LLM-based             erator and goal test (Katz et al. 2024; Cao et al. 2024), as
                                         planning, showing that systems such as GPT-5 can approach              well as heuristic functions (Tuisov, Vernik, and Shleyfman
                                         the coverage of a strong planner like LAMA on existing do-             2025; Corrêa, Pereira, and Seipp 2025b). Planning via plan-
                                         mains, while still degrading under obfuscation and requiring           ning models generation (NL2PDDL) focuses on translating
                                         vastly greater computational resources (Corrêa, Pereira, and          natural language task description into formal planning lan-
                                                                                                                guage that can be consumed by off-the-shelf planners (Guan
                                         Copyright © 2026, Association for the Advancement of Artificial        et al. 2023; Oswald et al. 2024; Gestrin, Kuhlmann, and
                                         Intelligence (www.aaai.org). All rights reserved.                      Seipp 2024; Huang, Lipovetzky, and Cohn 2025; Tantakoun,
Muise, and Zhu 2025). Policy code generation (NL2Policy)           The Next Steps
leverages LLMs to synthesize domain-specific strategies and        While progress on generating search-based planner com-
executable policies that generalize across problem instances       ponents is encouraging, these methods are not yet ready
(Silver et al. 2024; Hodel 2024; Stein et al. 2025). We discuss    for realistic settings. The foundation laid by ToS and Au-
the current state of these directions and the next steps that      toToS demonstrates that code for search components can
must be addressed to operationalize these ideas in trustworthy     be synthesized and iteratively refined, but several aspects
and effective language-driven agents.                              of these approaches remain in their simplest form. One ma-
                                                                   jor example is the state representation. In ToS, the state
        Generating Search Based Planners                           representation was hand-crafted and somewhat similar to a
An emerging trend in solving planning tasks with language          multi-valued encoding (Bäckström and Nebel 1995), while
models focused on simply asking the model to produce a             in heuristic-generation work it was propositional and derived
plan by providing a few examples (Silver et al. 2022). These       from a formal task specification. This raises the question of
models were able to find plans only in the simplest cases,         whether certain representations work better for generating
when the solutions were very similar in structure to the exam-     search components. More importantly, it raises the question
ple plans. Any need to generate something novel or unseen          of where state features should come from in the first place.
resulted in failure (Valmeekam et al. 2023b). This quickly         Prior work assumes that state features are known, and relax-
reinforced a familiar insight from classical planning: gen-        ing this assumption is a critical step toward adapting to new
erating a plan often requires search. Hence, an alternative        domains, such as webpage navigation in WebArena (Zhou
line of work shifted toward integrating search, the ability        et al. 2024) and API calling in AppWorld (Trivedi et al. 2024).
to backtrack and consider many possibilities before finding        One might expect that language models could automatically
a valid one. As language models excel at text-based input,         infer such state features, but current models struggle with
the focus was on planning problems expressed in natural            this task (Vafa et al. 2024). Nonetheless, prior work on learn-
language. A variety of approaches were proposed, exploit-          ing state representations from images (Asai and Fukunaga
ing search methods for the heavy lifting of exploring the          2018), text (Lindsay et al. 2017; Sohrabi et al. 2018), and
problem’s state space, while the language model was used to        reinforcement learning (Konidaris, Kaelbling, and Lozano-
define the search space, with the required search components       Perez 2018; Echchahed and Castro 2025) offers potential
successor function succ and goal test is goal implemented          clues for addressing this challenge. A central question here
as calls to the model (Hao et al. 2023; Shinn et al. 2023; Yao     is how to determine the right level of abstraction for both
et al. 2023; Besta et al. 2024; Sel et al. 2023).                  the actions and the state representation.
    All these attempts have the same common pitfall, their            Other limitations arise when dealing with partial informa-
search components implementation calls a language model,           tion. Generating successors might require interaction with
which takes significant time and is impractical in planning,       the environment, like in the aforementioned AppWorld. Such
where problems have combinatorially large state spaces and         cases might be handled either via planning and execution
it is imperative to have an efficient implementation of these      loop or via knowledge compilation (Palacios and Geffner
search components. The aforementioned literature made a            2009). Regardless, it can be challenging to determine the
different choice, instead heavily restricting the search algo-     initial state, goal formulation, or even whether additional
rithms, bounding their exploration depth, width, frontier size,    information-gathering actions are required.
etc. Consequently, the algorithms lost their soundness and            Another limitation of the implementation strategy used in
completeness properties (Katz et al. 2024), without gaining        AutoToS is its linear nature, where each single alternative
in precision (Katz, Kokel, and Sreedharan 2025). A more            suggested by the language model is accepted without compar-
promising alternative has been to use LLMs only at construc-       ison. In more complex domains, generating and evaluating
tion time to generate code (e.g., Python code) that imple-         multiple candidate components should be a global search
ments search components, avoiding LLM calls during search          process with the ability to backtrack on earlier decisions.
or inference time. Such implementations can then be tested
and reflected upon, improving gradually with case-specific
feedback, like in the case of (Automated) Thought of Search                  Planning via PDDL Generation
(ToS/AutoToS) (Katz et al. 2024; Cao et al. 2024).                 PDDL (McDermott et al. 1998) has long served as de-facto
    That initial work on using the language models to ob-          the standard formalism for expressing planning tasks, provid-
tain code for the succ and is goal search components has           ing the input for a wide range of planners. However, repre-
paved the way for the next step, obtaining code for a domain-      senting a planning task in PDDL is one of the few remaining
specific heuristic h (Corrêa, Pereira, and Seipp 2025b; Tuisov,   challenges that require manual human labor. Recent research
Vernik, and Shleyfman 2025). That was a major step, allow-         has turned to language models for help with closing this gap
ing to move away from a blind exploration into the realm of        by translating natural language task descriptions into formal
an informed search, making the generated solvers substan-          PDDL specifications. The developed approaches, that we
tially more efficient. Both of these investigations focus on       collectively refer to as NL2PDDL, aim to make planning
deterministic tasks expressed in PDDL, one for purely propo-       more accessible, while reducing the burden of manual knowl-
sitional and the other for numeric planning. In both cases, it     edge engineering and enabling the use of existing planners in
should be rather straightforward to move away from PDDL            settings where formal domain specifications in PDDL were
to tasks that are specified purely in natural language.            not yet readily available. The plan generation therefore can
be done with existing domain-independent planners, exploit-        concrete Venmo payment action is applicable may require ob-
ing decades of research and engineering efforts in making          serving the response of an API call, which cannot be known
efficient planners.                                                a priori. Another limitation is that some applications require
   Among the first is the work of Guan et al. (2023), which        object creation (Corrêa et al. 2024), conditional plans and
explores using pre-trained LLMs to construct PDDL (domain          loops, some of which might need to be handled outside of
and problem). The approach takes as input the detailed nat-        the planning problem, for example in AppWorld, sending
ural language description of the task, in-context examples,        Venmo payments to “all” friends, formulating an appropriate
description of the domain, any physical constraints, and a         goal state requires quantifying over an unknown number of
dynamically updated list of predicates that is initially empty.    objects, a well-known limitation of classical PDDL. Further-
The LLM then incrementally proposes action argument lists,         more, it is not clear how to integrate the procedural glue
preconditions, and effects, together with any newly intro-         code that is required between APIs, or actions in this case,
duced predicates and their natural language descriptions, and      at certain abstraction levels, such as dealing with multi-page
refines them through validator feedback and human guidance.        API responses, transforming returned data formats, or chain-
To reduce the reliance on human experts for the in-the-loop        ing heterogeneous tool outputs. All of these fall outside the
feedback, Huang, Lipovetzky, and Cohn (2025) propose a             capabilities of current NL2PDDL pipelines.
fully automated method. They would first generate a diverse           Beyond addressing these modeling limitations, there is
library of candidate action schemas to capture multiple in-        also substantial room for improving the feedback used during
terpretations of natural language task description, then apply     PDDL construction. Existing approaches typically explore
semantic filtering using sentence encoders to automatically        modifications to PDDL models in a greedy, linear fashion,
validate, filter, and rank the generated action schemas. Their     evaluating each proposed model in isolation rather than with
experiments show that this approach can produce sound plans        respect to the model it aims to refine. This prevents systems
and better accommodate natural language ambiguity without          from determining whether a newly proposed model repre-
human feedback. These approaches laid the foundation for           sents a true improvement. While some work begins to move
the technical construction of the feedback flows. The work         beyond single-path refinement (Huang, Lipovetzky, and Cohn
of Oswald et al. (2024) focused on evaluation of constructed       2025), a more systematic model-space search—such as the
models, going beyond the semantic filtering and addressing         one explored in (Caglar et al. 2024) is still largely missing.
syntactic validity, semantic correctness, and usability of the        There is also considerable room to improve how semantic
generated results by existing planners. It did so by focusing      errors are detected and corrected. Recent work on knowledge
on the operational semantics instead of action schema simi-        engineering in the LLM era (Vallati et al. 2025) emphasizes
larity, comparing models in terms of similarity of the solution    that knowledge engineering is not solely about drafting ac-
spaces they implicitly encode. Another approach by Gestrin,        tion schemas but involves iterative refinement, validation,
Kuhlmann, and Seipp (2024) aims for robustness from mini-          maintenance, and ensuring that models accurately reflect
mal textual specifications (rather than assuming rich textual      operational semantics. Hybrid workflows, in which LLMs
specifications). Their framework, NL2Plan, incrementally           assist human designers and are complemented by princi-
extracts necessary information to build the PDDL planning          pled model-validation and repair techniques, may therefore
task in a particular order, similar to how students are taught     offer a more robust foundation. Most NL2PDDL systems
to model in PDDL.                                                  rely on VAL for syntactic validation, but deeper semantic
   To learn more about the plethora of available techniques        inconsistencies—incorrect invariants, missing preconditions,
that use language models to help construct planning mod-           unintended side effects—are rarely addressed. Incorporat-
els, one can look at the survey by Tantakoun, Muise, and           ing richer feedback mechanisms, including domain-analysis
Zhu (2025). They also introduce Language-to-Plan (L2P),            tools, invariants, or landmarks, could substantially strengthen
an open-source Python library that re-implements several           model quality. Moreover, current pipelines accept a single
NL2PDDL approaches. L2P is designed to streamline reuse            LLM suggestion at each refinement step; exploring multi-
and enable systematic, reproducible experimental results           ple candidate models or applying meta-reasoning over the
across a variety of NL2PDDL approaches.                            refinement trajectory could prevent error accumulation and
                                                                   improve convergence.
The Next Steps
Since this method deals with generating models in a restric-             Planning via Policy Code Generation
tive form, all the shortcomings of the search-based methods        Generalized planning deals with finding policies that can effi-
described in the previous section persist here as well. Choos-     ciently solve the entire family of planning problems (Jiménez,
ing the right level of abstraction for both actions and pred-      Segovia-Aguas, and Jonsson 2019). The conceptual idea of
icates/numeric fluents as well as how to deal with features        exploring the use of LLMs for generating a generalized policy
outside of the classical fragment (full observability, determin-   in the form of code (Silver et al. 2024) is naturally appealing,
istic action dynamics, and offline access to task structure)       as the generated code can be validated, adapted, and when
are arguably the biggest open questions. The interplay be-         deemed working, deployed. In this original two-phase formu-
tween planning and execution often provides information            lation, a language model is asked to summarize and describe
beyond the common knowledge - strong suit of language              in natural language both the problem and a strategy to solve
models - that might be exploited via means of transformation.      the problem. Then, a language model is asked to implement
To give an example, in AppWorld, determining whether a             the strategy in code. The generated code can be tested with
a held out set of instances to produce a feedback in case of                  Cross-Category Observations
an error. A key limitation of such an approach is the inherent
assumption that the produced natural language strategy is          We have discussed each of the categories in isolation. Here,
correct; indeed, while the method works remarkably well            we propose a cross-category view.
on some domains, there are domains where the produced                 Policy-code generation appears to get us closer to realis-
strategy is incorrect (Hodel 2024). To mitigate this limitation,   tic agentic environments, with many of the limitations ob-
the follow up work proposed generating the strategy in the         served in other approaches being easier to tackle within this
form of pseudo-code (Stein et al. 2025). The pseudo-code can       paradigm. Unlike NL2Search or NL2PDDL, policy-code gen-
then be verified with held out instances, asking the language      eration can directly express procedural glue code, interleave
model to emulate an execution of the pseudo-code on these          sensing with acting (addressing partial observability more
inputs. In this way, mistakes can be detected and corrected        naturally), and incorporate reusable components that arise
prior to the generation of the generalized plan, substantially     frequently in real applications. Such components natively cap-
improving the reliability across diverse IPC domains.              ture the hierarchical nature of some applications. In domains
   Approaches that leverage LLMs’ programming abilities to         like AppWorld, for example, one can imagine writing poli-
generate a policy are also emerging in related areas of task       cies that capture sub-tasks, such as sending Venmo payments
and motion planning (Singh et al. 2023; Sun et al. 2023; Liang     to friends, co-workers, or roommates. It is also possible to
et al. 2023) as well as web interaction domains (Song et al.       define macro-actions or reusable code fragments that support
2025). Code-As-Policies (Liang et al. 2023) define a hierar-       multiple tasks, including authentication, retrieval, filtering,
chical code generation approach with LLMs such that new            or error handling.
functions are defined recursively to create complex policies          It is also worth noting that these methods can be used to
for robot. Policies ProgPrompt (Wang et al. 2024) proposes to      improve each other. As a simple example, one can imagine
prompt the language model to implement a python function as        NL2Search first used to obtain the search components, pass-
a policy for a new task, given a policy as in-context example.     ing these generated components code as an additional input
CodeActAgent (Wang et al. 2024) proposes to reduce LLM             to NL2PDDL. More complex iterations are also possible
calls by prompting LLM to provide executable python code           and sometimes are unavoidable. In domains where search
that can iterate over multiple actions in a single generation.     is needed and pure policy-code generation is not possible, a
AdaPlanner (Sun et al. 2023) proposed adaptive closed-loop         mix of approaches might work best. Higher-level actions/sub-
planning with LLMs through code-prompting for AlfWorld,            tasks might be realized via policy-code, while the search-
with a refinement flow that is triggered when the generated        requiring planning can be done via one of the other two
program fails. In web-interaction domain CoAct (Song et al.        methods. This kind of integration of the discussed methods
2025) proposes to query LLM for actions as well as CodeAc-         seems to be most promising for handling realistic scenarios.
tions, to improve efficiency.                                         To sum up, while the progress to date in LLM-driven
                                                                   policy synthesis is promising, opportunities remain for the
The Next Steps                                                     planning community to shape how planning concepts, policy
                                                                   generation, procedural knowledge, and hierarchical structure,
While the concept of two-phase iterative generation of code        can make meaningful impact in real-world agentic systems.
policies using language models was established by the origi-
nal work (Silver et al. 2024), the adaptation of the first phase
to take a form that can be evaluated is significant (Stein                                Conclusions
et al. 2025). Coming up with the strategy and implementing         In this position paper, we examined three major categories
the strategy are the two conceptual steps that need to be per-     of planner-generation methods: search-based planner genera-
formed, but the actual realization can differ. The current work    tion (NL2Search), planning via PDDL or model generation
validates the two steps separately, moving to the next once        (NL2PDDL), and planning via policy or solver code gener-
the first one was deemed valid. One can however imagine            ation (NL2Policy). The methods focus on using LLMs at
that during the second step, an evidence is obtained that the      construction time, to generate the search components, the
strategy/pseudo-code obtained in the first step is incorrect,      planning models, or policy that can be validated and used
resulting in revisiting the first step.                            efficiently at inference time. We examined each direction,
   Similarly to the case of AutoToS, a limitation of the current   highlighting the progress made to date while outlining the
approach is its linear nature, where alternatives are weighted     challenges, and the future steps needed to make these ap-
against each other and local decisions are made. This local        proaches usable in real-world applications. Although each
search through the space of alternative changes proposed by        line of work currently has limitations and/or makes simplify-
the language model is an improvement over the paradigm             ing assumptions, these challenges also reveal opportunities
adopted by AutoToS, but here as well, the better choice would      for future research and can help motivate research to address
be a global, systematic search procedure.                          the identified gaps. Ultimately, the opportunity ahead is to
   A major limitation is the restriction to PDDL in the in-        both advance planning research along these directions and
put. While extending to natural language specified inputs          to have a critical view and/or framework for assessing their
would bring forward the many of the issues pointed out in          impact in the LLM era, ensuring the planning contributions
the previous sections, it might be unavoidable in real-world       meaningfully influence the efficiency, reliability, and capabil-
applications.                                                      ities of agentic systems in the years to come.
                        References                                Huang, S.; Lipovetzky, N.; and Cohn, T. 2025. Planning in
Asai, M.; and Fukunaga, A. 2018. Classical Planning in Deep       the Dark: LLM-Symbolic Planning Pipeline Without Experts.
Latent Space: Bridging the Subsymbolic-Symbolic Boundary.         In Walsh, T.; Shah, J.; and Kolter, Z., eds., Proceedings of
In Proceedings of the Thirty-Second AAAI Conference on            the Thirty-Nineth AAAI Conference on Artificial Intelligence
Artificial Intelligence (AAAI 2018), 6094–6101. AAAI Press.       (AAAI 2025), 26542–26550. AAAI Press.
Bäckström, C.; and Nebel, B. 1995. Complexity Results for       Jiménez, S.; Segovia-Aguas, J.; and Jonsson, A. 2019. A Re-
SAS+ Planning. Computational Intelligence, 11(4): 625–            view of Generalized Planning. The Knowledge Engineering
655.                                                              Review, 34: e5.
Besta, M.; Blach, N.; Kubicek, A.; Gerstenberger, R.;             Kambhampati, S.; Valmeekam, K.; Guan, L.; Verma, M.;
Podstawski, M.; Gianinazzi, L.; Gajda, J.; Lehmann, T.;           Stechly, K.; Bhambri, S.; Saldyt, L. P.; and Murthy, A. B.
Niewiadomski, H.; Nyczyk, P.; and Hoefler, T. 2024. Graph         2024. Position: LLMs Can’t Plan, But Can Help Planning
of Thoughts: Solving Elaborate Problems with Large Lan-           in LLM-Modulo Frameworks. In Proceedings of the 41st
guage Models. In Dy, J.; and Natarajan, S., eds., Proceedings     International Conference on Machine Learning (ICML 2024).
of the Thirty-Eighth AAAI Conference on Artificial Intelli-       JMLR.org.
gence (AAAI 2024), 17682–17690. AAAI Press.                       Katz, M.; Kokel, H.; and Sreedharan, S. 2025. Seemingly
Caglar, T.; Belhaj, S.; Chakraborti, T.; Katz, M.; and Sreedha-   Simple Planning Problems are Computationally Challenging:
ran, S. 2024. Can LLMs Fix Issues with Reasoning Models?          The Countdown Game. arXiv:2508.02900 [cs.AI].
Towards More Likely Models for AI Planning. In Dy, J.; and
                                                                  Katz, M.; Kokel, H.; Srinivas, K.; and Sohrabi, S. 2024.
Natarajan, S., eds., Proceedings of the Thirty-Eighth AAAI
                                                                  Thought of Search: Planning with Language Models Through
Conference on Artificial Intelligence (AAAI 2024), 20061–
                                                                  The Lens of Efficiency. In Proceedings of the Thirty-Seventh
20069. AAAI Press.
                                                                  Annual Conference on Neural Information Processing Sys-
Cao, D.; Katz, M.; Kokel, H.; Srinivas, K.; and Sohrabi, S.       tems (NeurIPS 2024).
2024. Automating Thought of Search: A Journey Towards
Soundness and Completeness. In NeurIPS 2024 Workshop              Konidaris, G.; Kaelbling, L. P.; and Lozano-Perez, T. 2018.
on Open-World Agents.                                             From skills to symbols: Learning symbolic representations
                                                                  for abstract high-level planning. Journal of Artificial Intelli-
Corrêa, A. B.; Giacomo, G. D.; Helmert, M.; and Rubin, S.        gence Research, 61: 215–289.
2024. Planning with Object Creation. In Bernardini, S.; and
Muise, C., eds., Proceedings of the Thirty-Fourth Interna-        Liang, J.; Huang, W.; Xia, F.; Xu, P.; Hausman, K.; Ichter, B.;
tional Conference on Automated Planning and Scheduling            Florence, P.; and Zeng, A. 2023. Code as Policies: Language
(ICAPS 2024), 104–113. AAAI Press.                                Model Programs for Embodied Control. In 2023 IEEE In-
                                                                  ternational Conference on Robotics and Automation (ICRA),
Corrêa, A. B.; Pereira, A. G.; and Seipp, J. 2025a. The 2025
                                                                  9493–9500.
Planning Performance of Frontier Large Language Models.
arXiv:2511.09378.                                                 Lindsay, A.; Read, J.; Ferreira, J. F.; Hayton, T.; Porteous,
Corrêa, A. B.; Pereira, A. G.; and Seipp, J. 2025b. Classi-      J.; and Gregory, P. 2017. Framer: Planning Models from
cal Planning with LLM-Generated Heuristics: Challenging           Natural Language Action Descriptions. In Barbulescu, L.;
the State of the Art with Python Code. In Proceedings of          Frank, J.; Mausam; and Smith, S. F., eds., Proceedings of
the Thirty-Eight Annual Conference on Neural Information          the Twenty-Seventh International Conference on Automated
Processing Systems (NeurIPS 2025).                                Planning and Scheduling (ICAPS 2017), 434–442. AAAI
                                                                  Press.
Echchahed, A.; and Castro, P. S. 2025. A Survey of State
Representation Learning for Deep Reinforcement Learning.          McDermott, D.; Ghallab, M.; Howe, A.; Knoblock, C.; Ram,
Trans. Mach. Learn. Res., 2025.                                   A.; Veloso, M.; Weld, D.; and Wilkins, D. 1998. PDDL – The
Gestrin, E.; Kuhlmann, M.; and Seipp, J. 2024. NL2Plan: Ro-       Planning Domain Definition Language – Version 1.2. Techni-
bust LLM-Driven Planning from Minimal Text Descriptions.          cal Report CVC TR-98-003/DCS TR-1165, Yale Center for
arXiv:2405.04215.                                                 Computational Vision and Control, Yale University.
Guan, L.; Valmeekam, K.; Sreedharan, S.; and Kambham-             Oswald, J.; Srinivas, K.; Kokel, H.; Lee, J.; Katz, M.; and
pati, S. 2023. Leveraging pre-trained large language models       Sohrabi, S. 2024. Large Language Models as Planning Do-
to construct and utilize world models for model-based task        main Generators. In Bernardini, S.; and Muise, C., eds., Pro-
planning. In Proceedings of the Thirty-Seventh Annual Con-        ceedings of the Thirty-Fourth International Conference on
ference on Neural Information Processing Systems (NeurIPS         Automated Planning and Scheduling (ICAPS 2024). AAAI
2023), 79081–79094.                                               Press.
Hao, S.; Gu, Y.; Ma, H.; Hong, J.; Wang, Z.; Wang, D.;            Palacios, H.; and Geffner, H. 2009. Compiling Uncer-
and Hu, Z. 2023. Reasoning with Language Model is Plan-           tainty Away in Conformant Planning Problems with Bounded
ning with World Model. In Proceedings of the 2023 Confer-         Width. Journal of Artificial Intelligence Research, 35: 623–
ence on Empirical Methods in Natural Language Processing          675.
(EMNLP 2023).                                                     Sel, B.; Al-Tawaha, A.; Khattar, V.; Wang, L.; Jia, R.; and Jin,
Hodel, N. 2024. Exploring the use of LLMs in generalized          M. 2023. Algorithm of Thoughts: Enhancing Exploration of
planning. Bachelor’s thesis, Saarland University.                 Ideas in Large Language Models. CoRR, abs/2308.10379.
Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and        Vafa, K.; Chen, J. Y.; Rambachan, A.; Kleinberg, J.; and
Yao, S. 2023. Reflexion: language agents with verbal rein-       Mullainathan, S. 2024. Evaluating the World Model Implicit
forcement learning. In Proceedings of the Thirty-Seventh         in a Generative Model. arXiv:2406.03689.
Annual Conference on Neural Information Processing Sys-          Vallati, M.; Barták, R.; Chrpa, L.; McCluskey, T. L.; and Pet-
tems (NeurIPS 2023).                                             rick, R. P. A. 2025. Knowledge Engineering for Planning and
Silver, T.; Dan, S.; Srinivas, K.; Tenenbaum, J.; Pack Kael-     Scheduling in the LLM Era. In Harabor, D.; and Ramirez,
bling, L.; and Katz, M. 2024. Generalized Planning in            M., eds., Proceedings of the thirty-fifth International Confer-
PDDL Domains with Pretrained Large Language Models.              ence on Automated Planning and Scheduling (ICAPS 2025),
In Dy, J.; and Natarajan, S., eds., Proceedings of the Thirty-   391–395. AAAI Press.
Eighth AAAI Conference on Artificial Intelligence (AAAI          Valmeekam, K.; Marquez, M.; Olmo, A.; Sreedharan, S.;
2024). AAAI Press.                                               and Kambhampati, S. 2023a. PlanBench: An Extensible
Silver, T.; Hariprasad, V.; Shuttleworth, R. S.; Kumar, N.;      Benchmark for Evaluating Large Language Models on Plan-
Lozano-Pérez, T.; and Kaelbling, L. P. 2022. PDDL Planning      ning and Reasoning about Change. In Proceedings of the
with Pretrained Large Language Models. In NeurIPS 2022           Thirty-Seventh Annual Conference on Neural Information
Workshop on Foundation Models for Decision Making.               Processing Systems (NeurIPS 2023), 38975–38987.
                                                                 Valmeekam, K.; Marquez, M.; Sreedharan, S.; and Kambham-
Singh, I.; Blukis, V.; Mousavian, A.; Goyal, A.; Xu, D.; Trem-   pati, S. 2023b. On the Planning Abilities of Large Language
blay, J.; Fox, D.; Thomason, J.; and Garg, A. 2023. Prog-        Models - A Critical Investigation. In Proceedings of the
Prompt: Generating Situated Robot Task Plans using Large         Thirty-Seventh Annual Conference on Neural Information
Language Models. In 2023 IEEE International Conference           Processing Systems (NeurIPS 2023).
on Robotics and Automation (ICRA), 11523–11530.
                                                                 Wang, X.; Chen, Y.; Yuan, L.; Zhang, Y.; Li, Y.; Peng, H.;
Sohrabi, S.; Riabov, A. V.; Katz, M.; and Udrea, O. 2018. An     and Ji, H. 2024. Executable Code Actions Elicit Better LLM
AI Planning Solution to Scenario Generation for Enterprise       Agents. In Proceedings of the 41st International Conference
Risk Management. In Proceedings of the Thirty-Second AAAI        on Machine Learning (ICML 2024). OpenReview.net.
Conference on Artificial Intelligence (AAAI 2018), 160–167.      Yao, S.; Yu, D.; Zhao, J.; Shafran, I.; Griffiths, T.; Cao, Y.; and
AAAI Press.                                                      Narasimhan, K. 2023. Tree of thoughts: Deliberate problem
Song, L.; Dai, Y.; Prabhu, V.; Zhang, J.; Shi, T.; Li, L.; Li,   solving with large language models. In Proceedings of the
J.; Savarese, S.; Chen, Z.; Zhao, J.; et al. 2025. Coact-1:      Thirty-Seventh Annual Conference on Neural Information
Computer-using agents with coding as actions. arXiv preprint     Processing Systems (NeurIPS 2023).
arXiv:2508.03923.                                                Zhou, S.; Xu, F. F.; Zhu, H.; Zhou, X.; Lo, R.; Sridhar, A.;
Stein, K.; Hodel, N.; Fišer, D.; Hoffmann, J.; Katz, M.;        Cheng, X.; Ou, T.; Bisk, Y.; Fried, D.; Alon, U.; and Neu-
and Koller, A. 2025. Improved Generalized Planning               big, G. 2024. WebArena: A Realistic Web Environment for
with LLMs through Strategy Refinement and Reflection.            Building Autonomous Agents. In Proceedings of the Twelfth
arXiv:2508.13876.                                                International Conference on Learning Representations (ICLR
                                                                 2024). OpenReview.net.
Sun, H.; Zhuang, Y.; Kong, L.; Dai, B.; and Zhang, C. 2023.
AdaPlanner: Adaptive Planning from Feedback with Lan-
guage Models. In Oh, A.; Naumann, T.; Globerson, A.;
Saenko, K.; Hardt, M.; and Levine, S., eds., Advances in
Neural Information Processing Systems, volume 36, 58202–
58245. Curran Associates, Inc.
Tantakoun, M.; Muise, C.; and Zhu, X. 2025. LLMs as Plan-
ning Formalizers: A Survey for Leveraging Large Language
Models to Construct Automated Planning Models. In Che,
W.; Nabende, J.; Shutova, E.; and Pilehvar, M. T., eds., Find-
ings of the Association for Computational Linguistics: ACL
2025. Association for Computational Linguistics.
Trivedi, H.; Khot, T.; Hartmann, M.; Manku, R.; Dong, V.;
Li, E.; Gupta, S.; Sabharwal, A.; and Balasubramanian, N.
2024. AppWorld: A Controllable World of Apps and People
for Benchmarking Interactive Coding Agents. In Ku, L.;
Martins, A.; and Srikumar, V., eds., Findings of the Associa-
tion for Computational Linguistics: ACL 2024, 16022–16076.
Association for Computational Linguistics.
Tuisov, A.; Vernik, Y.; and Shleyfman, A. 2025. LLM-
Generated Heuristics for AI Planning: Do We Even Need
Domain-Independence Anymore? arXiv:2501.18784.
