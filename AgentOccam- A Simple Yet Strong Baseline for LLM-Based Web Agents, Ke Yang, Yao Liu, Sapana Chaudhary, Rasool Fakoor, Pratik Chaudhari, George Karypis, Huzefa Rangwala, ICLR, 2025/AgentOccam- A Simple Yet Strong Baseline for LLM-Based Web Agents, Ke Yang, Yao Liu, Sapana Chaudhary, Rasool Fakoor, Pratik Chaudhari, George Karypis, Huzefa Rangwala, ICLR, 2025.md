# <span id="page-0-1"></span>AGENTOCCAM: A SIMPLE YET STRONG BASELINE FOR LLM-BASED WEB AGENTS

Ke Yang†∗, Yao Liu♢, Sapana Chaudhary♢, Rasool Fakoor♢, Pratik Chaudhari♢, George Karypis♢, Huzefa Rangwala♢

University of Illinois Urbana-Champaign† , Amazon♢

key4@illinois.edu, {yaoliuai,chausapa,fakoor,rhuzefa}@amazon.com

# ABSTRACT

Autonomy via agents based on large language models (LLMs) that can carry out personalized yet standardized tasks presents a significant opportunity to drive human efficiency. There is an emerging need and interest in automating web tasks (e.g., booking a hotel for a given date within a budget). Being a practical use case itself, the web agent also serves as an important proof-of-concept example for various agent grounding scenarios, with its success promising advancements in many future applications. Meanwhile, much prior research focuses on handcrafting their web agent strategies (e.g., agent's prompting templates, reflective workflow, role-play and multi-agent systems, search or sampling methods, etc.) and the corresponding in-context examples. However, these custom strategies often struggle with generalizability across all potential real-world applications. On the other hand, there has been limited study on the misalignment between a web agent's observation and action representation, and the data on which the agent's underlying LLM has been pre-trained. This discrepancy is especially notable when LLMs are primarily trained for language completion rather than tasks involving embodied navigation actions and symbolic web elements. In our study, we enhance an LLM-based web agent by simply refining its observation and action space, aligning these more closely with the LLM's capabilities. This approach enables our base agent to significantly outperform previous methods on a wide variety of web tasks. Specifically, on WebArena, a benchmark featuring general-purpose web interaction tasks, our agent AGENTOCCAM surpasses the previous state-of-the-art and concurrent work by 9.8 (+29.4%) and 5.9 (+15.8%) absolute points respectively, and boosts the success rate by 26.6 points (+161%) over similar plain web agents with its observation and action space alignment. Furthermore, on WebVoyager benchmark comprising tasks defined on real-world websites, AGENTOCCAM exceeds the former best agent by 2.4 points (+4.6%) on tasks with deterministic answers. We achieve this without using in-context examples, new agent roles, online feedback or search strategies. AGENTOCCAM's simple design highlights LLMs' impressive zero-shot performance on web tasks, and underlines the critical role of carefully tuning observation and action spaces for LLM-based agents.[1](#page-0-0)

# 1 INTRODUCTION

AI agents leveraging large language models (LLMs) show great potential in automating repetitive and programmatic tasks and thereby alleviating human workloads [\(Gao et al.,](#page-10-0) [2024;](#page-10-0) [Xi et al.,](#page-11-0) [2023;](#page-11-0) [Yang et al.,](#page-11-1) [2024\)](#page-11-1). LLMs showcase remarkable capabilities in perception, reasoning and planning primarily due to their pre-training and post-learning. However, their effectiveness is significantly constrained when task-specific observation and action representations diverge from the parametric knowledge encoded during their training/learning time. For instance, in web-based tasks, these agents perform notably below human levels [\(Zhou et al.,](#page-12-0) [2023b;](#page-12-0) [Koh et al.,](#page-10-1) [2024a\)](#page-10-1).

To improve web task performance by LLM-based agents, recent work focuses on designing better agent policies with either handcrafted prompting templates [\(Sodhi et al.,](#page-11-2) [2024\)](#page-11-2) or hard-coded auto-

<sup>∗</sup>Work performed while interning at Amazon.

<span id="page-0-0"></span><sup>1</sup>Our code and data are available at [https://github.com/amazon-science/AgentOccam.](https://github.com/amazon-science/AgentOccam)

<span id="page-1-0"></span>![](_page_1_Figure_1.jpeg)

Figure 1: Overview of AGENTOCCAM. Unlike prior research that works intensively on designing compound LLM policies, we enhance the web agent simply by aligning the web interaction action and observation space with the functioning LLM's acquired knowledge and skills during its training.

prompting strategies (Fu et al., 2024; Wang et al., 2024). While those pre-defined strategies can be effective for certain tasks, they struggle to generalize to diverse websites and varying skill requirements. Another emerging trend is to adopt sampling or search algorithms for a dynamic exploration of web navigation actions, which reduces dependence on pre-defined strategies but increases the cost of LLM inferences (Koh et al., 2024b; Zhang et al., 2024; Pan et al., 2024).

In this work, we aim to enhance an LLM-based web agent's proficiency by optimizing the text-based task understanding and reasoning of existing LLMs, rather than refining the agent strategies. Automating web tasks is challenging, as the agent needs to *i*) accurately extract information from web pages with varying formats and encoded scripts, and *ii*) issue appropriate embodied actions, selecting from those defined merely on web (e.g., scrolling, clicking, or hovering over buttons). These web observation and action spaces are less common in both, the pre- and post-training data of LLMs, preventing the LLMs from fully realizing their potential in accomplishing general-purpose web tasks. Therefore, we study how to properly tune the observation and actions for LLM-based web agents, to align them with the functioning LLMs capacities learned during training.

As shown in Figure 1, our method comprises of three components: *i)* We reduce non-essential actions to minimize the agent's embodiment and trivial interaction needs; *ii)* We refine the observation by eliminating redundant and irrelevant web elements, and restructuring web content blocks for more succinct yet as informative representations; *iii)* We introduce two planning actions (branch and prune), which enables the agent to self-organize navigation workflow with a planning tree, and use the same structure to filter the previous traces for history replay. It's noteworthy that those planning commands are in the same position as navigation prompts for the agent. We implement these components by generic rules that applies to all types of markup-language-formatted web pages, without leveraging task-related information on the test benchmark.

By combining the three techniques mentioned above, our proposed agent AGENTOCCAM performs substantially better on web tasks across websites in the WebArena environments (Zhou et al., 2023b). AGENTOCCAM outperforms the previous state-of-the-art approach by 9.8 absolute points ( $\pm$ 29.4%) and surpasses concurrent work by 5.9 absolute points ( $\pm$ 15.8%). Notably, unlike most prior work, we do not use any in-context examples, additional online search or sampling, nor specialized prompting templates or agent roles to play well. In contrast, AGENTOCCAM delivers such strong performance with an unexpectedly simple approach: letting the LLM issue actions within the processed and augmented observation and action spaces. Compared with a similar plain web agent without these proposed observation and action space changes, AGENTOCCAM increases the success rate by 26.6 absolute points ( $\pm$ 161%). Moreover, we prove AGENTOCCAM's web environment generalizability in the real-world web environment. In the WebVoyager definite-answer subset (He et al., 2024), which consists of real-world web tasks with deterministic answers, AGENTOCCAM exceeds the previous best agent on this benchmark by 2.4 points ( $\pm$ 4.6%).

In summary, the primary contribution of this work are as follows. First, we develop a new state-of-the-art agent, AGENTOCCAM, for web tasks. On the WebArena benchmark consisting of 812 tasks across five diverse websites (e.g., shopping, searching on a forum), AGENTOCCAM outperforms previous and concurrent work significantly. Second, we shed light on the strong zero-shot perfor-

| sential Components        | Task-specific<br>Strategies | In-context<br>Examples | Additional<br>Module | Offline Data <sup>2</sup> | Online<br>Search |
|---------------------------|-----------------------------|------------------------|----------------------|---------------------------|------------------|
| toGuide (Fu et al., 2024) | NO                          | YES                    | YES                  | YES                       | NO               |

Table 1: Comparison of essential components for different LLM-based web agents.

<span id="page-2-1"></span>Ess Aut SteP (Sodhi et al., 2024) YES YES YES NO NO AutoRefine (Pan et al., 2024) YES YES YES YES NO LM-Tree Search (Koh et al., 2024b) NO YES YES YES YES **AWM (Wang et al., 2024)** NO YES YES YES NO WebPilot (Zhang et al., 2024) NO YES YES NO YES Agent-E (Abuelsaad et al., 2024) YES NO NO AGENTOCCAM NO NO

mance of LLMs on web tasks with our simple agentic workflow, in sharp contrast to many more complex compound agent policies. Last, our work on aligning the observation and action spaces is orthogonal to agentic strategies and can be combined with future advances in that aspect.

#### RELATED WORK

**LLM-based Web Agent** Advances in large language and multi-modal foundation models have significantly boosted the development of autonomous agents to solve web tasks. Techniques translating LLMs to powerful decision-making agents (Yao et al., 2022b; Shinn et al., 2024) have advanced web agents, inspiring many techniques that design inference time agent strategies. Many prior approaches improve the agent system by designing auxiliary modules with specialized LLMs or roles, aiming to break down complex tasks (Sun et al., 2024; Prasad et al., 2024; Abuelsaad et al., 2024). Other work leverages LLMs to extract common patterns from examples or past experience (Zheng et al., 2023; Fu et al., 2024; Wang et al., 2024). However, this line of work often relies on pre-defined control hierarchy, prompt templates or examples to act accurately in the test environments. For example, SteP (Sodhi et al., 2024) utilizes a stack-based approach for dynamic multi-level control in the web tasks but relies on task-specific atomic policies with environment-related information hardcoded in prompt template. Another line of work focuses on improving web agents' performance by leveraging more online examples from the environments. Many of them (Zhou et al., 2023a; Zhang et al., 2024; Putta et al., 2024) adapt Monte Carlo Tree Search (MCTS) methods, expanding intermediate states (tree nodes) in one task repeatedly by multiple trials over that task. Among them, WebPilot (Zhang et al., 2024) also adds a global optimization layer for high-level planning. Koh et al. (2024b) use a trained value function to guide search and to back-trace on the task execution tree. Auto Eval and Refine (Pan et al., 2024) trains a separate evaluator, and improves the task execution using reflective thinking (Shinn et al., 2024) on past trials in the same task. However, sampling or resetting multiple times in the same task, not only increases the inference cost significantly, but also limits its applicability when failed task is not revocable. As a comparison, we highlight the simplicity of our method and its difference with related agent approaches in Table 1.

Fine-tuned or Trained Models for Web Tasks Fine-tuning language or multimodal models for web tasks is another effective approach to enhance decision-making capabilities on the web tasks (Yin et al., 2024; Hong et al., 2024; Lai et al., 2024; Putta et al., 2024). While fine-tuning promises more adaptivity and broader optimization space, the size of task-specific fine-tuned models are typically not comparable with the most powerful closed-source models. There is also some early research that trains models to follow natural language command on the web before LLMs emerged, using semantic parsing (Artzi & Zettlemoyer, 2013), reinforcement learning (Branavan et al., 2009) and imitation learning (Liu et al., 2018; Humphreys et al., 2022). However, those fine-tuned agents, limited by the base model's capacities or training data volume, often fail to match those constructed with LLMs regarding performance or/and generalizability, and is beyond the scope of this work.

**Simulated Web Agent Environments** Web agent development has been supported by increasingly complex web simulators for training and evaluation. These range from basic platforms like MiniWoB (Shi et al., 2017) and its extension MiniWoB++ (Liu et al., 2018), to more sophisticated

<span id="page-2-0"></span><sup>&</sup>lt;sup>2</sup>The offline data refers to a labeled dataset to instill human knowledge into models.

<sup>&</sup>lt;sup>3</sup>AWM supports two scenarios: in offline scenarios it directly leverage an offline dataset, and in online scenarios it relies on a domain-specific evaluator from Pan et al. (2024) which requires offline data to train.

environments such as WebShop [\(Yao et al.,](#page-11-12) [2022a\)](#page-11-12), WebArena [\(Zhou et al.,](#page-12-0) [2023b\)](#page-12-0), and Visual-WebArena [\(Koh et al.,](#page-10-1) [2024a\)](#page-10-1). These simulators progressively incorporate real-world complexities, from simple form-filling to tasks across multiple full-featured websites. In this work, we focus only on the text modality, and use WebArena to evaluate our method's task success and generalizability as it contains different types of websites and task-intents in a single suite. To further assess AGEN-TOCCAM's generalizabilty, we extend experiments to the real-world web environments, evluated with the tasks and golden answers proposed in WebVoyager [\(He et al.,](#page-10-4) [2024\)](#page-10-4).

# 3 PROBLEM FORMULATION

We formalize the web interaction process by a Partially Observable Markov Decision Process (POMDP, [Littman](#page-10-11) [\(2009\)](#page-10-11); [Spaan](#page-11-13) [\(2012\)](#page-11-13)): ⟨O, S, A, P, R, p0, γ⟩. In POMDPs, an observation o ∈ O consists of information that the agent receives from the web environment, e.g. HTMLs, as well as any instructions and prompts. In this work, we only consider the text modality. A state s ∈ S denotes the whole underlying (unobserved) state of the agent and the environment such that the state transition is Markovian. An action a ∈ A is either a command recognized by the web environment, or any other unrecognized token sequence that will lead to a stay in the current state. P denotes a deterministic state transition function that records the change in the webpage state given the current state and agent action. R is the reward function that decides the success or failure of the agent's sequence of actions. p<sup>0</sup> denotes the initial state distribution which is uniform over tasks tested. The discounting factor γ is typically set to 1 when the reward is only assigned at the end of an agent-web interaction episode.

To solve POMDP, a common goal is to find a decision policy π(at|ht) maximizing the expected cumulative reward, where h<sup>t</sup> denotes the observation history {o0, o1, ..., ot}. In LLM-based web agent design, that is translated to designing a policy π(at|ht) with the help of one or more base LLM policies πLLM and a set of algorithmic modules. In this work, we work on a special class of policies that can be expressed as: π(g(at)|ht) = πLLM(at|f(ht)), where f and g are rule-based functions that process the observation (including action instructions) and actions for the LLM policy. We name it the observation and action space alignment problem. Notice that under such a problem setting, all of our changes apply only to the observations and the actions. We emphasize not all agent strategies in previous approaches can be represented in this way. For example, search-based algorithms require a control program on the top to select actions and trigger back-tracing; methods with evaluators, reflective thinking or memory modules also necessitate a managing center to alternate between the main LLM and these helper segments or other role-playing LLMs. In contrast, we aim to answer the following question in our work: Can we build a strong web agent with the base LLM policy πLLM by optimizing only the observation and action mapping f and g?

# <span id="page-3-1"></span>4 METHOD

Rather than introducing any new modules or hierarchical structures on top of the base LLM, our method focuses on a simple web agent workflow that inputs the web observations to a generalpurpose LLM-API and uses the LLM outputs as actions directly. In this section, we describe the process of aligning web tasks, which necessitates embodiment knowledge, with the predominantly static and text-centric nature of LLM training. Section [4.1](#page-3-0) discusses our strategies (summarized in Figure [2\)](#page-4-0) for refining the action space to be more compact and reducing the need for the agent's embodiment capabilities. Section [4.2](#page-5-0) outlines our methods (summarized in Figure [4\)](#page-5-1) for condensing web content descriptions to be both brief and informative, and identifying key web elements and relevant steps for retention to organize the agent's memory in a pertinent manner.

## <span id="page-3-0"></span>4.1 ACTION SPACE ALIGNMENT

A web agent's action space defines the valid commands it can use to interact with the web environment. The WebArena simulator supports translating three categories of actions into mouse and keyboard operations: basic actions (e.g., click, type), tab operations (e.g., tab focus for managing active tabs), and page operations (e.g., go back for navigation). These actions are detailed in Appendix [A,](#page-13-0) along with a comparison of our changes to the action space.

Based on our observation of common failure modes in web agents, there exist two key challenges to be addressed by editing the action space: *i)* removing irrelevant actions that LLMs struggle to understand and frequently misuse, and *ii)* improving the memorization and planning ability when

<span id="page-4-0"></span>![](_page_4_Figure_1.jpeg)

Figure 2: In aligning the action space with LLM pre-training, we only retain high-utility actions and lessen the demand for advanced embodiment skills (steps 1 and 2). Additionally, we incorporate planning steps, allowing the agent to *autonomously* manage task breakdown and execution (step 3).

the task execution requires navigating multiple potential paths to succeed. We propose that the first can be corrected simply by removing and combining actions. The second issue was often addressed in the previous work using handcrafted rules or strategies, making these approaches hard to generalize. In this work, we tackle the second problem by introducing actions that allow the LLM to autonomously generate plans and manage the task workflow. These proposed solutions are explained in detail below and illustrated in Figure [2.](#page-4-0) The list of all actions in original and reduced action space is shown in Table [3,](#page-8-0) together with the frequency they are taken in different agents.

Simplifying the Action Space. First, we eliminate actions that can be replicated using similar actions or replace multiple actions with one action with the same expressiveness (illustrated in Figure [2](#page-4-0) step 1). Specifically, we remove the noop action, signifying "no operation", as it is shown to be a distraction to the agent in most cases. Similarly, tab operations, which manage the focusing, opening, or closing of tabs are removed because they are only needed in limited cases of multi-site tasks requiring two tabs. Furthermore, we limit page navigation actions like go forward and goto, as their utility is greatly constrained by the agent's poor memory of the relationship between a page's URL and its content. By eliminating these less effective actions, our goal is to minimize distractions and boost the agent's concentration on more meaningful operations. In addition, we introduce the note action, allowing the agent to record key observations for subsequent conclusions, and the stop action, enabling the agent to autonomously conclude the trajectory with answers. We also add a go home command for multi-site tasks, enabling the agent to navigate directly to the homepage where all available sites are listed.

Second, we eliminate actions that heavily require embodiment knowledge and simplify low-level actions into more abstract operations as shown in Figure [2](#page-4-0) step 2. In particular, we reduce commands that LLM-based agents struggle with unless provided with detailed context-specific guidance, like hover or press (the latter is for pressing key combinations, often shortcuts). To properly use these actions requires LLMs to have embodied thinking of the current scenario, especially regarding the mouse position or keyboard operations, which it has not acquired during their training. Additionally, we remove the scroll action, opting instead to load the full page content as the web state. This change is in response to our observation that agents tend to engage in aimless and repetitive scrolling when an essential link is not visible at the top of the page, wasting steps without making progress. Furthermore, we streamline the agent's interaction with drop-down menus; instead of selecting the menu and then an option, a single click command with the ID of the desired option now suffices.

Planning via Generation. Web tasks often require a solution that requires navigating multiple paths, e.g. extracting information from one page and submitting it to another page, like the task of creating a refund request on the Contact Us page for a broken product (task template 154), which requires parsing the order ID and refund amount from the order pages. We introduce two actions, branch and prune, to generate plans in a tree structure and save them for future observations. As Figure [2](#page-4-0) step 3 shows, the LLM-generated plans start with a root node being the objective of the task. The branch action will generate new subplans under the current node, decomposing high-level objectives into smaller, more manageable subgoals. Conversely, the prune action allows the agent

<span id="page-5-2"></span>![](_page_5_Figure_1.jpeg)

Figure 3: The components of our web navigation agent's prompt. It includes a general instruction outlining the task, the desired output and available actions, as well as online task information providing the current goal, the agent's past interactions, and the latest observations. Notably, the sections on previous interactions and current observation use the most tokens, and can be attributed to two main factors: the length of the pages and the extent of history span.

<span id="page-5-1"></span>![](_page_5_Figure_3.jpeg)

Figure 4: To align the web task's observation space with the format that the base model perceives most effectively, we condense a single-page length by removing unnecessary texts that repetitively describe the web page's functionality and layout (step 1), and by identifying page elements relevant to the task for the agent to remember (step 2). Additionally, we optimize the agent workflow memory through a planning tree, viewing each new plan as a separate goal and excluding past steps' information dedicated to previous plans to enhance memory conciseness (step 3).

to give up the current sub-plan, often after repetitive failed attempts, and seek alternatives. Together with the branch and the prune actions, the LLM can edit the planning tree autonomously. Note that these two planning actions are of no difference from the native navigation actions in the web environment (e.g. click, type) and the LLM is free to choose when to take these actions to update the plan. The generated plan provides a context for future action generation and enhances the consistency of actions in one trajectory. This approach leverages the intrinsic planning ability of LLM itself. We argue that this will not compromise the agent's generalization capability as this design relies minimally on task-specific prior knowledge.

#### <span id="page-5-0"></span>4.2 Observation Space Alignment

The observation space of web agents consists of task objectives, instructions, previous interaction, and the current web text descriptions or screenshots (see Figure 3 and Appendix G for our agent). Among them, previous interactions and current web content consume the most number of tokens, which scales with the length of a single page and the length of history. This often results in a long context window, which not only increases the LLM inference cost but also poses challenges for LLM to extract related information accurately. Therefore, our main goal in refining the observation is to address these two aspects. The alignment of observations is outlined in Figure 4.

Simplifying Web Page Observations. The content on web pages is represented in HTML or accessibility tree format in most text-only web agents. These formats are designed towards front-end loading and rendering, containing numerous formatting tokens making them lengthy and repetitive, as illustrated in Figure [4](#page-5-1) Step 1. Our goal is to optimize the representation to make it more readable to LLMs on one single page. Specifically, we merge function-descriptive web elements (e.g., StaticText [761] 'My Account') with interactive elements that share the same label (e.g., link [1312] 'My Account'). We then convert table and list blocks to Markdown, eliminating repetitive structural tokens (e.g., columnheader, gridcell). Consequently, we achieve a more concise representation while keeping the same information.

Replaying Observation History Selectively. Taking observation history as input is important for decision-making agents to act consistently for tasks requiring long horizons, given that the observation state only contains partial information about the environment's state. For web tasks, it is also important to include both observation and action history as some key information may not be displayed on the current page. However, the observation history will also significantly scale up the context length and increase reasoning difficulty as well as inference cost. We address this issue by only selecting the most important and related information on the previous web pages, according to two rules based on the "pivotal" nodes (defined later) and the planning tree. We provide detailed examples of how these two techniques are implemented in Appendix [B.](#page-13-1)

First, we observe that only a small amount of content on a web page is pertinent to a specific task among several steps and is worth replaying in future steps. For example, in tasks requiring the agent to find all reviews within three months, it is unnecessary to keep other reviews or some unrelated links like Contact Us on the page. Thus we employ a simple rule to identify this small amount of content by leveraging the tree structure of web data (e.g. accessibility tree). To do this, we first instruct the agent to pinpoint the crucial web elements denoted as "pivotal" nodes, at the same time when the agent generates an action. The agent is then programmed to include only the pivotal nodes' ancestor nodes (indicating their global hierarchy and position), sibling nodes (providing immediate context), and descendant nodes (offering detailed characteristics) in the future observations as illustrated in Figure [4](#page-5-1) Step 2. This effectively narrows down the volume of data and level of noise passed to the future context of LLM inference.

Second, we observe that not all previous steps' observation needs to be noted during the inference of future steps. Thus we can leverage the planning tree generated by the agent itself to keep the agent's focus sharp. Specifically, when the agent initiates a branch action to develop a new plan, we treat this new plan as a separate goal. Steps taken for earlier plans and their observations will be dismissed in the current plan's observation window, as depicted in Figure [4](#page-5-1) step 3. This allows the agent to focus only on information dedicated to the current plan for a sub-task.

# 5 EXPERIMENTAL RESULTS AND ANALYSIS

Here, we detail experiments on WebArena [\(Zhou et al.,](#page-12-0) [2023b\)](#page-12-0), a web simulator benchmark. Further experiments with WebVoyager [\(He et al.,](#page-10-4) [2024\)](#page-10-4), a web benchmark based on real-world websites, are included in Appendix [C.](#page-16-0) We show AGENTOCCAM's base model generalizability in Appendix [D.](#page-17-0)

Environment. We utilize WebArena, an interactive web simulator, as our benchmark. WebArena consists of fully functional websites from four common domains: e-commerce platforms (OneStop-Shop), social forums for idea and opinion exchange (Reddit), collaborative software development (GitLab), and content management for creation and management of online data (online store management). The platform additionally includes utility tools: a map, a calculator, a scratchpad, and Wikipedia to enable human-like task-solving. The benchmark consists of 812 tasks generated from 241 templates. A template here is a parametric form of a task intent, allowing for multiple instantiations with different keywords. Each task is accompanied by an evaluator that programmatically checks the correctness of the final information with respect to the desired ground truth information[4](#page-6-0) . We use GPT-4-turbo-2024-04-09 [\(Achiam et al.,](#page-10-12) [2023\)](#page-10-12) to build our AGENTOCCAM.

Baselines. We compare AGENTOCCAM with the following prior and concurrent work: 1) WebArena agent: the Chain-of-Thought (CoT) prompted agent included in the WebArena benchmark

<span id="page-6-0"></span><sup>4</sup>We identified and corrected errors in the original evaluators, with details discussed in Appendix [E.](#page-19-0) Our approach outperforms the baseline methods with both the original and the corrected evaluators.

| Agent                | Model       | SR (%) | Shopping | Shopping Admin | GitLab | Map    | Reddit | Multisite |
|----------------------|-------------|--------|----------|----------------|--------|--------|--------|-----------|
|                      |             | (#812) | (#187)   | (#182)         | (#180) | (#109) | (#106) | (#48)     |
| WebArena-replication | GPT-4-Turbo | 16.5   | 16.6     | 15.9           | 10.0   | 22.9   | 21.7   | 16.7      |
| SteP-replication     | GPT-4-Turbo | 33.3   | 33.2     | 32.4           | 26.7   | 35.8   | 52.8   | 12.5      |
| AWM                  | GPT-4       | 35.5   | -        | -              | -      | -      | -      | -         |
| WebPilot             | GPT-4o      | 37.2   | -        | -              | -      | -      | -      | -         |
| AGENTOCCAM           | GPT-4-Turbo | 43.1   | 40.6     | 45.6           | 37.8   | 46.8   | 61.3   | 14.6      |

<span id="page-7-1"></span>Table 2: Comparison of the success rate (SR) of AGENTOCCAM with baseline agents on WebArena.

<span id="page-7-2"></span>![](_page_7_Figure_3.jpeg)

Figure 5: Ablation study of AGENTOCCAM's action and observation space alignment, with details in Table [17.](#page-28-0) We incrementally add refinement components and assess marginal performance gains.

[\(Zhou et al.,](#page-12-0) [2023b\)](#page-12-0). 2) SteP [\(Sodhi et al.,](#page-11-2) [2024\)](#page-11-2): a stack-based approach on top of 14 human-written atomic strategies tailored to solving WebArena. 3) WebPilot [\(Zhang et al.,](#page-12-1) [2024\)](#page-12-1): a multi-agent, multi-level MCTS based agent that reports state-of-the-art overall performance on WebArena. 4) Agent Workflow Memory (AWM) [\(Wang et al.,](#page-11-3) [2024\)](#page-11-3): a method automatically summarizing workflow from past experience. SteP has made its code and interaction trajectories public. Hence, we are able to fully replicate the agents from WebArena and SteP with GPT-4-turbo in the identical web environments as our methods, for a fair comparison.[5](#page-7-0) WebPilot and AWM, being concurrent works with this paper, have not yet provided source code or resulting trajectories, limiting our analysis of these works to just reporting the aggregated performance numbers included in their technical reports. Our analysis focuses on SteP as it was the most performant method prior to this work.

Question 1: How well does AGENTOCCAM perform? As seen from the results in Table [2,](#page-7-1) our agent AGENTOCCAM, which optimizes the action and observation space, now sets a new SOTA on the WebArena benchmark. It increases the overall success rate from 37.2% to 43.1%, a 15.8% relative improvement over best results among previous and concurrent work. We observe that AGENTOCCAM not only accomplishes tasks in the template that is previously unsolvable, like updating personal information on OneStopShop (task template 165), but it also raises the success rate for templates with mixed results previously, such as setting a homepage URL on a GitLab profile (task template 331). This is further illustrated in Figure [6](#page-28-1) in the appendix.

Question 2: How much does each observation and action space change contribute to AGEN-TOCCAM? We evaluate the contribution of each component in AGENTOCCAM described in Section [4](#page-3-1) to its overall success by incrementally integrating them into the vanilla agent (WebArena-Replication) and assessing the marginal performance gain shown in Figure [5.](#page-7-2) The details of each incremental experiment are as follows:

- *i)* Removal of non-essential actions (↓ **Actions**): Narrowing the action space can reduce the level of distraction for LLM policies and significantly improves performance across all tested websites as shown in Figure [5.](#page-7-2) By removing rarely used actions like tab focus,go forward, hover and press, the agent spends fewer steps wandering around and explores more efficiently using actions such as click and type. Table [3](#page-8-0) shows it reduces hundreds of hover and goto actions while significantly increasing the number of click and type.
- *ii)* Disabling scrolling (**Above + X Scrolling**): We observe that LLM policies tend to use scroll up and down often when they do not know what to do (since these actions are revertible). Consequently, it significantly delays the task execution and causes looping in certain tasks. As a

<span id="page-7-0"></span><sup>5</sup> In our experiments, we note that all agents occasionally fail due to errors from the WebArena simulator, such as posting rate limits in Reddit or login expiration. In such cases, we restart the experiments.

<span id="page-8-0"></span>Table 3: Action statistics for the ablation study of AGENTOCCAM's components. Each number in the table represents the frequency of an action across all the tasks within the experiment setting. Actions noop, go forward, tab focus and tab close are not included since they are not used even once in vanilla agent and removed in our method.

| Exp.                     | click | hover | type | press |     | scroll new tab go back |     | goto | note | stop   | go home branch |    | prune |
|--------------------------|-------|-------|------|-------|-----|------------------------|-----|------|------|--------|----------------|----|-------|
| Vanilla                  | 2328  | 126   | 1024 | 7     | 132 | 20                     | 71  | 511  | -    | 6<br>- | -              | -  | -     |
| ↓ Actions                | 7119  | -     | 2531 | -     | 370 | -                      | 52  | -    | 194  | 512    | 36             | -  | -     |
| Above + X Scrolling 7033 |       | -     | 2390 | -     | -   | -                      | 100 | -    | 219  | 536    | 42             | -  | -     |
| Above + Obs Opt.         | 6890  | -     | 2040 | -     | -   | -                      | 56  | -    | 201  | 571    | 23             | -  | -     |
| Above + History          | 4625  | -     | 1286 | -     | -   | -                      | 94  | -    | 112  | 801    | 54             | -  | -     |
| AGENTOCCAM               | 4720  | -     | 1159 | -     | -   | -                      | 339 | -    | 197  | 769    | 42             | 34 | 47    |

<span id="page-8-2"></span>Table 4: Average observation tokens per step across WebArena sites. We use the GPT2 tokenizer from HUGGINGFACE [\(Radford et al.,](#page-11-14) [2019\)](#page-11-14).

| Exp.                | All    | Shopping | Shopping Admin | GitLab | Map    | Reddit | Multisite |
|---------------------|--------|----------|----------------|--------|--------|--------|-----------|
| Vanilla             | 2210.2 | 2272.1   | 2460.2         | 2199.1 | 1883.2 | 2132.4 | 1751.0    |
| ↓ Actions           | 1652.0 | 1644.7   | 2133.1         | 1981.3 | 912.0  | 1081.2 | 1296.8    |
| Above + X Scrolling | 3376.2 | 3148.0   | 5403.7         | 3364.9 | 1378.1 | 2603.6 | 1975.5    |
| Above + Obs Opt.    | 2891.1 | 1722.5   | 4791.7         | 2560.8 | 1476.4 | 3332.3 | 1619.4    |
| Above + History     | 3051.3 | 1802.6   | 5140.2         | 3153.3 | 862.1  | 3156.1 | 2030.3    |
| AGENTOCCAM          | 2930.9 | 1634.2   | 4920.7         | 3126.8 | 1056.0 | 3697.8 | 1282.5    |

result, disabling the scrolling action and passing the entire page to the agent proves advantageous, especially for GitLab and Reddit tasks. However, this strategy increases the number of observation tokens, which will be addressed by subsequent refinements.

- *iii)* Simplifying web page elements (**Above + Obs Opt.**): We remove redundant text and web format as show in Figure [4](#page-5-1) Step 1. This results in fewer tokens in the context window, as outlined in Table [4.](#page-8-2) It helps the agent focus on web elements crucial to task success across all websites and boosts the performance on all task types, except on GitLab, where this sometimes leads the agent to overlook simpler solutions (task id 394).
- *iv)* Selective replay of web elements in one page (**Above + History**): In this experiment, we follow step 2 shown in Figure [4](#page-5-1) to add a subset of elements from previous web pages as history. We observe that it allows the agent to avoid repetitive actions in tasks, significantly decreasing the steps needed for task completion as demonstrated in Table [5.](#page-9-0) However, this addition slightly hurts performance in tasks with dense single-page content or those requiring navigation across multiple pages, as shopping and Reddit tasks success rate drops by 3.2 and 6.0 points, respectively.
- *v)* Planning via generation and selective replay of past pages (AGENTOCCAM; **Above + Planning**): We introduce actions branch and prune to allow the agent to autonomously generate plans and exclude historical steps not in the current sub-plan from the prompt context. This results in performance gains in tasks across nearly all websites, alongside a reduction in the required observation tokens. The actions branch and prune are both primarily used in correcting a failed strategy and trying an alternative path. For example, in the task of identifying the nearest national park to Boston (task id 265), the agent employs a branch action to adopt an alternative search strategy after a failed search attempt. In a GitLab task (task id 563), after multiple failed attempts using the Create project button, the agent opts for a prune action to explore other methods.

Question 3: Could the power of AGENTOCCAM be combined with other agentic strategies? A natural question to ask next is if we can combine these changes with other common agent strategies or prior work, since the changes in observation and action space are orthogonal and complementary to them. We showcase two example studies to answer this question: one with the SteP method [\(Sodhi et al.,](#page-11-2) [2024\)](#page-11-2) and another action selection method with LLM-as-a-judge.

The judge method is motivated by our observation of the high variation in the agent's behavior. In some key steps, the agent has a certain probability of generating the correct action but often fails to do so, making it hard for the agent to recover from later pages. For instance, when tasked with identifying the most suitable subreddit for posting (task template 6100), the AGENTOCCAM agent

<span id="page-8-1"></span><sup>6</sup>We remove stop in the statistics for the vanilla WebArena agent as this action is excluded in their officially defined action space. However, their agent is allowed by code to generate stop to end the trajectory.

Table 5: Average number of steps per task across all WebArena sites.

<span id="page-9-0"></span>

| Exp.                | All  | Shopping | Shopping Admin | GitLab | Map  | Reddit | Multisite |
|---------------------|------|----------|----------------|--------|------|--------|-----------|
| Vanilla             | 6.2  | 6.2      | 6.6            | 5.9    | 5.7  | 7.4    | 4.4       |
| ↓ Actions           | 13.3 | 10.6     | 14.3           | 14.8   | 11.9 | 15.2   | 13.7      |
| Above + X Scrolling | 12.7 | 9.0      | 14.0           | 14.8   | 12.7 | 13.0   | 14.0      |
| Above + Obs Opt.    | 12.0 | 8.5      | 13.2           | 15.4   | 10.2 | 12.1   | 13.2      |
| Above + History     | 8.6  | 5.6      | 9.6            | 10.3   | 8.3  | 7.6    | 12.9      |
| AGENTOCCAM          | 9.0  | 6.7      | 9.2            | 10.8   | 8.5  | 8.6    | 13.4      |

<span id="page-9-1"></span>Table 6: Success rate (SR) of AGENTOCCAM combined with agent strategies on WebArena.

| Agent              | Model       | SR (%) | Shopping | Shopping Admin | GitLab | Map    | Reddit | Multisite |
|--------------------|-------------|--------|----------|----------------|--------|--------|--------|-----------|
|                    |             | (#812) | (#187)   | (#182)         | (#180) | (#109) | (#106) | (#48)     |
| AGENTOCCAM         | GPT-4-Turbo | 43.1   | 40.6     | 45.6           | 37.8   | 46.8   | 61.3   | 14.6      |
| AGENTOCCAM + SteP  | GPT-4-Turbo | 41.1   | 46.5     | 36.3           | 36.7   | 47.7   | 50.9   | 18.8      |
| AGENTOCCAM + Judge | GPT-4-Turbo | 45.7   | 43.3     | 46.2           | 38.9   | 52.3   | 67.0   | 16.7      |

tends to hastily choose less relevant subreddits and gets stuck there. To address this, we direct the AGENTOCCAM to generate all possible suitable actions instead of one action at each step. These action candidates are then evaluated by another LLM (GPT-4-turbo as well) prompted to play the role of a judge and select the best action. The prompts for the judge are included in Appendix [G.](#page-30-0)

Table [6](#page-9-1) shows that a AGENTOCCAM + SteP agent, enhanced with task strategies, outperforms the standalone SteP method but doesn't match AGENTOCCAM's base performance. Additionally, combining AGENTOCCAM with a judge role through an action prediction and selection pipeline rectifies some of the base agent's behavioral misconduct.

By analyzing the trajectories of each method, we observe that task-specific strategies like those introduced in SteP can help when the strategy fits the task requirements. For example, in the task of "Draft an email to the shop owner via their contact us function for a coupon as {reason}" (task template 163), the AGENTOCCAM + SteP and SteP agents excel by prompting the agent explicitly not to click the submit button after drafting, where AGENTOCCAM fails to follow. However, for tasks outside the designed strategies, these hints can mislead the agent, leading to a 2-point drop in the overall success rate of AGENTOCCAM + SteP compared to AGENTOCCAM only. An example is task 639, where the agent, guided by SteP's instruction "Under forums, you will see only a subset of subreddits. To get the full list of subreddits, you need to navigate to the Alphabetical option.", repetitively navigates away from the appropriate subreddit, and generates reasons for its action selection that "Clicking on the 'Alphabetical' link will help us access a more comprehensive Reddit list.", demonstrating how hard-coded strategies can distract the agent and hurt generalizability.

The AGENTOCCAM + Judge agent, combining the AGENTOCCAM's generated action list with the second opinion from an LLM judge increases its overall success rate by 2.6%, by completing tasks where it may well fail due to intermediate decision flaws. For example, in choosing the right subreddit for a post (task template 6100), the base AGENTOCCAM might hastily pick from an initial list, whereas the AGENTOCCAM + Judge agent conducts a thorough search using post keywords or explores the entire forum list before drafting the post. This approach minimizes errors due to rushed decisions, increasing the likelihood of successfully completing task series.

# 6 CONCLUSION

In this paper, we proposed a simple but effective LLM-based web agent AGENTOCCAM that refines its action and observation spaces to be more comprehensible for LLMs primarily trained on static text. Unlike other methods, AGENTOCCAM stands out for its remarkably simple policy workflow, requiring no extra modules, additional LLM calls, or in-context examples. This simplicity does not compromise its performance; AGENTOCCAM surpasses previous and contemporary approaches on WebArena by 9.8 (SteP) and 5.9 (WebPilot) absolute points, respectively. Our results emphasize the importance of maintaining a simple agent architecture for better generalizability, echoing Occam's razor principle. In summary, AGENTOCCAM aims to lay a solid foundation and offer valuable insights for future web agent research and development.

# REFERENCES

- <span id="page-10-5"></span>Tamer Abuelsaad, Deepak Akkil, Prasenjit Dey, Ashish Jagmohan, Aditya Vempaty, and Ravi Kokku. Agent-e: From autonomous web navigation to foundational design principles in agentic systems, 2024. URL <https://arxiv.org/abs/2407.13032>.
- <span id="page-10-12"></span>Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.
- <span id="page-10-8"></span>Yoav Artzi and Luke Zettlemoyer. Weakly supervised learning of semantic parsers for mapping instructions to actions. Transactions of the association for computational linguistics, 1:49–62, 2013.
- <span id="page-10-9"></span>Satchuthananthavale RK Branavan, Harr Chen, Luke Zettlemoyer, and Regina Barzilay. Reinforcement learning for mapping instructions to actions. In Proceedings of the Joint Conference of the 47th Annual Meeting of the ACL and the 4th International Joint Conference on Natural Language Processing of the AFNLP, pp. 82–90, 2009.
- <span id="page-10-2"></span>Yao Fu, Dong-Ki Kim, Jaekyeom Kim, Sungryull Sohn, Lajanugen Logeswaran, Kyunghoon Bae, and Honglak Lee. Autoguide: Automated generation and selection of state-aware guidelines for large language model agents, 2024. URL <https://arxiv.org/abs/2403.08978>.
- <span id="page-10-0"></span>Chen Gao, Xiaochong Lan, Nian Li, Yuan Yuan, Jingtao Ding, Zhilun Zhou, Fengli Xu, and Yong Li. Large language models empowered agent-based modeling and simulation: A survey and perspectives. Humanities and Social Sciences Communications, 11(1):1–24, 2024.
- <span id="page-10-13"></span>Google. Gemini-1.5, 2024. URL [https://blog.google/technology/ai/](https://blog.google/technology/ai/google-gemini-ai/#sundar-note) [google-gemini-ai/#sundar-note](https://blog.google/technology/ai/google-gemini-ai/#sundar-note).
- <span id="page-10-4"></span>Hongliang He, Wenlin Yao, Kaixin Ma, Wenhao Yu, Yong Dai, Hongming Zhang, Zhenzhong Lan, and Dong Yu. Webvoyager: Building an end-to-end web agent with large multimodal models, 2024. URL <https://arxiv.org/abs/2401.13919>.
- <span id="page-10-6"></span>Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxiao Dong, Ming Ding, et al. Cogagent: A visual language model for gui agents. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 14281–14290, 2024.
- <span id="page-10-10"></span>Peter C Humphreys, David Raposo, Tobias Pohlen, Gregory Thornton, Rachita Chhaparia, Alistair Muldal, Josh Abramson, Petko Georgiev, Adam Santoro, and Timothy Lillicrap. A data-driven approach for learning to control computers. In International Conference on Machine Learning, pp. 9466–9482. PMLR, 2022.
- <span id="page-10-1"></span>Jing Yu Koh, Robert Lo, Lawrence Jang, Vikram Duvvur, Ming Lim, Po-Yu Huang, Graham Neubig, Shuyan Zhou, Russ Salakhutdinov, and Daniel Fried. VisualWebArena: Evaluating multimodal agents on realistic visual web tasks. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 881–905, Bangkok, Thailand, August 2024a. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.50. URL [https:](https://aclanthology.org/2024.acl-long.50) [//aclanthology.org/2024.acl-long.50](https://aclanthology.org/2024.acl-long.50).
- <span id="page-10-3"></span>Jing Yu Koh, Stephen McAleer, Daniel Fried, and Ruslan Salakhutdinov. Tree search for language model agents, 2024b. URL <https://arxiv.org/abs/2407.01476>.
- <span id="page-10-7"></span>Hanyu Lai, Xiao Liu, Iat Long Iong, Shuntian Yao, Yuxuan Chen, Pengbo Shen, Hao Yu, Hanchen Zhang, Xiaohan Zhang, Yuxiao Dong, et al. Autowebglm: A large language model-based web navigating agent. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 5295–5306, 2024.
- <span id="page-10-11"></span>Michael L Littman. A tutorial on partially observable markov decision processes. Journal of Mathematical Psychology, 53(3):119–125, 2009.

- <span id="page-11-10"></span>Evan Zheran Liu, Kelvin Guu, Panupong Pasupat, Tianlin Shi, and Percy Liang. Reinforcement learning on web interfaces using workflow-guided exploration. arXiv preprint arXiv:1802.08802, 2018.
- <span id="page-11-4"></span>Jiayi Pan, Yichi Zhang, Nicholas Tomlin, Yifei Zhou, Sergey Levine, and Alane Suhr. Autonomous evaluation and refinement of digital agents. In First Conference on Language Modeling, 2024.
- <span id="page-11-8"></span>Archiki Prasad, Alexander Koller, Mareike Hartmann, Peter Clark, Ashish Sabharwal, Mohit Bansal, and Tushar Khot. ADaPT: As-needed decomposition and planning with language models. In Kevin Duh, Helena Gomez, and Steven Bethard (eds.), Findings of the Association for Computational Linguistics: NAACL 2024, pp. 4226–4252, Mexico City, Mexico, June 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.findings-naacl.264. URL <https://aclanthology.org/2024.findings-naacl.264>.
- <span id="page-11-9"></span>Pranav Putta, Edmund Mills, Naman Garg, Sumeet Motwani, Chelsea Finn, Divyansh Garg, and Rafael Rafailov. Agent q: Advanced reasoning and learning for autonomous ai agents. arXiv preprint arXiv:2408.07199, 2024.
- <span id="page-11-14"></span>Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Language models are unsupervised multitask learners. OpenAI, 2019. URL [https://huggingface.](https://huggingface.co/openai-community/gpt2) [co/openai-community/gpt2](https://huggingface.co/openai-community/gpt2).
- <span id="page-11-11"></span>Tianlin Shi, Andrej Karpathy, Linxi Fan, Jonathan Hernandez, and Percy Liang. World of bits: An open-domain platform for web-based agents. In International Conference on Machine Learning, pp. 3135–3144. PMLR, 2017.
- <span id="page-11-6"></span>Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems, 36, 2024.
- <span id="page-11-2"></span>Paloma Sodhi, SRK Branavan, Yoav Artzi, and Ryan McDonald. Step: Stacked llm policies for web actions. In First Conference on Language Modeling, 2024.
- <span id="page-11-13"></span>Matthijs TJ Spaan. Partially observable markov decision processes. In Reinforcement learning: State-of-the-art, pp. 387–414. Springer, 2012.
- <span id="page-11-7"></span>Haotian Sun, Yuchen Zhuang, Lingkai Kong, Bo Dai, and Chao Zhang. Adaplanner: Adaptive planning from feedback with language models. Advances in Neural Information Processing Systems, 36, 2024.
- <span id="page-11-3"></span>Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. Agent workflow memory, 2024. URL <https://arxiv.org/abs/2409.07429>.
- <span id="page-11-0"></span>Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, et al. The rise and potential of large language model based agents: A survey. arXiv preprint arXiv:2309.07864, 2023.
- <span id="page-11-1"></span>Ke Yang, Jiateng Liu, John Wu, Chaoqi Yang, Yi R Fung, Sha Li, Zixuan Huang, Xu Cao, Xingyao Wang, Yiquan Wang, et al. If llm is the wizard, then code is the wand: A survey on how code empowers large language models to serve as intelligent agents. arXiv preprint arXiv:2401.00812, 2024.
- <span id="page-11-12"></span>Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. Webshop: Towards scalable real-world web interaction with grounded language agents. Advances in Neural Information Processing Systems, 35:20744–20757, 2022a.
- <span id="page-11-5"></span>Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629, 2022b.

- <span id="page-12-4"></span>Da Yin, Faeze Brahman, Abhilasha Ravichander, Khyathi Chandu, Kai-Wei Chang, Yejin Choi, and Bill Yuchen Lin. Agent lumos: Unified and modular training for open-source language agents. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 12380–12403, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/ 2024.acl-long.670. URL <https://aclanthology.org/2024.acl-long.670>.
- <span id="page-12-1"></span>Yao Zhang, Zijian Ma, Yunpu Ma, Zhen Han, Yu Wu, and Volker Tresp. Webpilot: A versatile and autonomous multi-agent system for web task execution with strategic exploration, 2024. URL <https://arxiv.org/abs/2408.15978>.
- <span id="page-12-2"></span>Longtao Zheng, Rundong Wang, Xinrun Wang, and Bo An. Synapse: Trajectory-as-exemplar prompting with memory for computer control. In The Twelfth International Conference on Learning Representations, 2023.
- <span id="page-12-3"></span>Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. Language agent tree search unifies reasoning acting and planning in language models. arXiv preprint arXiv:2310.04406, 2023a.
- <span id="page-12-0"></span>Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, et al. Webarena: A realistic web environment for building autonomous agents. arXiv preprint arXiv:2307.13854, 2023b.

# <span id="page-13-3"></span><span id="page-13-0"></span>A COMPARISON OF THE VANILLA AND THE ALIGNED ACTION SPACE

Table 7: The action space in WebArena.

| Category        | Action Type         | Description             |
|-----------------|---------------------|-------------------------|
|                 | noop                | Do nothing              |
|                 | click(elem)         | Click at an element     |
| Basic Actions   | hover(elem)         | Hover on an element     |
|                 | type(elem, text)    | Type to an element      |
|                 | press(key<br>comb)  | Press a key combination |
|                 | scroll(dir)         | Scroll up and down      |
|                 | tab<br>focus(index) | Focus on the i-th tab   |
| Tab Operations  | new<br>tab          | Open a new tab          |
|                 | tab<br>close        | Close current tab       |
|                 | go<br>back          | Visit the last URL      |
| Page Operations | go<br>forward       | Undo go back            |
|                 | goto(URL)           | Go to URL               |

Table 8: The aligned action space of AGENTOCCAM.

<span id="page-13-4"></span>

| Category            | Action Type          | Description                |
|---------------------|----------------------|----------------------------|
|                     | noop                 | Do nothing                 |
|                     | click [id]           | Click at an element        |
| Basic Actions       | hover                | Hover on an element        |
|                     | type [id] [content]  | Type to an element         |
|                     | press                | Press a key combination    |
|                     | scroll               | Scroll up and down         |
|                     | tab<br>focus         | Focus on the i-th tab      |
| Tab Operations      | new<br>tab           | Open a new tab             |
|                     | tab<br>close         | Close current tab          |
|                     | go<br>back           | Visit the last URL         |
| Page Operations     | go<br>forward        | Undo go back               |
|                     | goto                 | Go to URL                  |
|                     | home7<br>go          | Go to home page            |
| Workflow Management | note [content]       | Take notes                 |
|                     | stop [answer]        | Stop with an answer        |
|                     | branch [id] [intent] | Generate a new plan        |
| Planning Actions    | prune [id] [reason]  | Restore to a previous plan |

We list the action space of WebArena and our aligned action space in Table [7](#page-13-3) and [8,](#page-13-4) respectively. In detail, we remove non-essential and embodiment-understanding-required actions like noop and scroll, and add more actions for internal workflow management or autonomous planning control.

# <span id="page-13-1"></span>B PIVOTAL NODES AND THE PLANNING TREE CLARIFICATIONS

To prevent confusion, we separate the following explanations for the independent techniques of "selectively replaying web elements on a page" and "selectively replaying entire pages."

<span id="page-13-2"></span><sup>7</sup>Valid only in multisite tasks.

# B.1 SELECTIVELY REPLAYING WEB ELEMENTS ON A PAGE WITH PIVOTAL NODES (FIGURE 4 STEP 2)

#### B.1.1 INTUITION AND BACKGROUND

We could view selectively replaying web elements on a page as a focused memory mechanism, where only the information that's relevant to the task would be recorded and replayed as the agent history traces. As all the web pages could be framed into a (DOM) tree structure, any web elements are nodes in this representation. We define pivotal nodes as the web elements, be it interactable or not, that are potentially useful for completing the task. Those pivotal nodes might present information (e.g., customer reviews in a review summary task) or the agent could interact with them to navigate to crucial states (e.g., the search box and the search button in a search task). We obtain these nodes at each step by prompting the agent to generate the page's highlights based on which they issue the action, or any web elements they will attend to if they fail at future steps and restore to the current state. After identifying the pivotal nodes with the agent's efforts, our code supports automatically parsing the web page's DOM tree and retaining nodes that are associated with the pivotal nodes (i.e., pivotal nodes' ancestor, sibling, and descendant nodes, as shown in Figure 4), to get a more succinct but less noisy version of the observation. This version would be used for constructing the agent's focused working history.

#### B.2 PROMPT, PIVOTAL NODE SECTION

```
Generate the response in the following format:
...

OBSERVATION HIGHLIGHT:
List the numerical ids of elements on the current webpage based on which you would issue your action. Also include elements on the current webpage you would attend to if you fail in the future and have to restore to this step. Don't include elements from the previous pages. Select elements at a higher hierarchical level if most their children nodes are considered crucial. Sort by relevance and potential values from high to low, and separate the ids with commas. E.g., '1321, 52, 756, 838'.
```

#### B.3 EXAMPLE TASK OBJECTIVE

What is the email address of the Dean of the School of Engineering at Stanford University?

## B.4 AGENTOCCAM'S WORKFLOW REGARDING THE PIVOTAL NODES

0. The task started at the Google.com, with the observation to be:

```
RootWebArea 'Google'
          link [29] 'About'
link [30] 'Store'
          link [277] 'Gmail'
link [275] 'Search for Images'
          button [282] 'Google apps
          link [152] 'Sign in
          IframePresentational [153]
          search [6]
                     combobox [12] 'Search' [required: False] button [294] 'Search by voice'
                     button [295] 'Search by image
button [272] 'Google Search'
                     button [273] "I'm Feeling Lucky"
          contentinfo
                     link [83] 'Advertising link [84] 'Business'
                     link [85] 'How Search works'
                     link [89] 'Our third decade of climate action: join us'
                     link [93] 'Privacy
link [94] 'Terms'
                     button [100] 'Settings
                                generic [102] 'Settings'
```

1. The agent typed the keyword into the search box and identified element 12 (combobox [12] 'Search' [required: False]) and 272 (button [272] 'Google Search') as the pivotal nodes. The web transit to a Google search page with the searched entries listed. Now, the agent would be prompted

with task history and web observation for issuing the next action, where the task history was constructed based on the pivotal nodes selected by the agent previously, and any pivotal-node-associated nodes. We take the automatically-generated interaction history clip from the prompt at this step:

```
OBSERVATION:
RootWebArea 'Google
        search
                combobox 'Search' [required: False]
                button 'Search by voice
button 'Search by image
                 button 'Google Search'
                 button "I'm Feeling Lucky"
REASON FOR ACTION:
To progress towards finding the email address of the Dean of the School of Engineering at
     Stanford University, the first logical step is to search for relevant information. Using
     the search input box to enter a query such as "Dean of the School of Engineering Stanford
     University email" and then submitting it using the 'Google Search' button is a direct
     approach to gather this information.
ACTION:
type [12] [Dean of the School of Engineering Stanford University email] [1]
</step_0_interaction>
```

2. We can observe that the "pivotal node" technique helps keep a focused memory attention by only retaining the context of crucial information and omitting irrelevant noise. Based on the interaction history summary and current observation, the agent executed the following steps, with the history section constantly updated with the information from the ongoing steps till trajectory ended.

# B.5 SELECTIVELY REPLAYING ENTIRE PAGES WITH THE PLANNING TREE (FIGURE 4 STEP 3)

We will use a planning tree generated by our agent during the development stage as an example for explaining how the planning tree takes shape and helps in selectively replaying past pages.

#### B.5.1 INTUITION AND BACKGROUND

If we make an analogy of the single-thread web task completion to code execution, the agent's issuing sub plans mimic nested function calling, the active plan is like the uppermost function in the execution stack, and pruning the planning tree plays as popping failed functions off the stack. There constantly exists a planning tree and the planning tree operation instructions in the agent's prompt. We enable the agent to organize the planning tree with 'branch' and 'prune' commands, where the 'branch' action creates new subplans, and the 'prune' action restores the task progress to a previous state. It's noteworthy that those planning commands are in the same position as navigation prompts for the agent.

#### B.5.2 PROMPT, PLANNING TREE SECTION

```
If you think you should refine the plan, use the following actions:
branch [parent_plan_id] [new_subplan_intent]: To create a new subplan based on PREVIOUS PLANS.

Ensure the new subplan is connected to the appropriate parent plan by using its ID. E.g., 'branch [12] [Navigate to the "Issue" page to check all the issues.]'
prune [resume_plan_id] [reason]: To return to a previous plan state when the current plan is deemed impractical. Enter the ID of the plan state you want to resume. E.g., 'prune [5] [
The current page lacks items "black speaker," prompting a return to the initial page to restart the item search.]'
Otherwise, use the following actions:
{navigation_specifications}
```

#### B.6 EXAMPLE TASK OBJECTIVE

(WebArena 174) Open my latest updated issue that has keyword "feature" in its title to check if it is closed.

- B.7 AGENTOCCAM 'S WORKFLOW REGARDING THE PLANNING TREE
- 0. At the beginning, we used the task objective as the root plan:

- [0] (Active Plan) Find the solution to "Open my latest updated issue that has keyword "feature " in its title to check if it is closed"
- 1. The agent added a subplan to planning node 0 by issuing branch [0] [Navigate to the Issues page to search for the latest issue with the keyword "feature" in the title.]. Now the planning tree changed into:
- [0] Find the solution to "Open my latest updated issue that has keyword "feature" in its title to check if it is closed"
  - [1] (Active Plan) Navigate to the Issues page to search for the latest issue with the keyword "feature" in the title.
- 2. The agent navigated to the project's issue page.
- 3. The agent decomposed the plan by generating branch actions branch [1] [Search for the latest issue with the keyword "feature" in the title and check if it is closed.] and branch [1] [Open the latest issue with the keyword "feature" in the title.]. It performed navigation steps for each active plan before the next planning command was executed. In this example, after branch [1] [Search for the latest issue with the keyword "feature" in the title and check if it is closed.] was proposed, the active plan turned into "Search for the latest issue with the keyword 'feature' in the title and check if it is closed." The agent then typed the keyword "feature" into the search box and sorted the issues by operating the sort icon before generating the next plan "Open the latest issue with the keyword 'feature' in the title." In other words, all the navigation commands (e.g., search and sort) it issued were intended for the current active plan (e.g., search for the latest issue with the keyword "feature" in the title and check if it is closed). Just like a function call only needs to consider the function's scope, this allows the agent to only attend to the navigation actions dedicated to the active plan and the corresponding web observation as the playing history, which helps selectively replay past pages for the agent. Note that in this case, it assigned the two new sub plans to the same parent plan [1], which automatically shaped the planning tree's structure. Finally, the planning tree reformed into (the content enclosed in "[]" means comments, which is intended for illustration and didn't appear in the agent's prompt):
- [0] Find the solution to "Open my latest updated issue that has keyword "feature" in its title to check if it is closed"
  - [1] Navigate to the Issues page to search for the latest issue with the keyword "feature" in the title. [Plan's action scope: navigate.]
    - [2] Search for the latest issue with the keyword "feature" in the title and check if it is closed [Plan's action scope; search and sort ]
    - check if it is closed. [Plan's action scope: search and sort.]
      [3] (Active Plan) Open the latest issue with the keyword "feature" in the title.
- 4. The agent executed the following steps to complete the task.

#### <span id="page-16-0"></span>C AGENTOCCAM'S GENERALIZABILITY TO REAL-WORLD WEBSITES

<span id="page-16-1"></span>Table 9: Performance comparison between Agent-E success rate (SR) and AgentOccam SR on tasks defined on real-world web environments from WebVoyager (He et al., 2024).

| Website (Task Number)    | Agent-E SR | AgentOccam SR |
|--------------------------|------------|---------------|
| Allrecipes (4)           | 75.00%     | 50.00%        |
| Amazon (1)               | 0.00%      | 0.00%         |
| Apple (7)                | 57.14%     | 28.57%        |
| ArXiv (16)               | 50.00%     | 43.75%        |
| BBC News (2)             | 0.00%      | 0.00%         |
| Booking (2)              | 50.00%     | 100.00%       |
| Cambridge Dictionary (9) | 55.56%     | 88.89%        |
| Coursera (2)             | 50.00%     | 50.00%        |
| ESPN (10)                | 40.00%     | 50.00%        |
| Google Map (9)           | 33.33%     | 44.44%        |
| Google Search (16)       | 62.50%     | 81.25%        |
| Huggingface (17)         | 17.65%     | 29.41%        |
| Wolfram Alpha (34)       | 73.53%     | 61.76%        |
| Overall (129)            | 51.90%     | 54.30%        |

WebVoyager benchmark (He et al., 2024) compiles web tasks based on 15 popular real-world websites. It comprises tasks with two types of user questions: ones with "golden" answers that are

<span id="page-17-2"></span>Table 10: The success rate (SR) of AGENTOCCAM's ablation study with models GPT-4-TURBO and GEMINI-1.5-FLASH on the WebArena's development set.

| Agent               | Model            | SR (%) | Shopping | Shopping Admin | GitLab | Map   | Reddit | Multisite |
|---------------------|------------------|--------|----------|----------------|--------|-------|--------|-----------|
|                     |                  | (#190) | (#48)    | (#41)          | (#41)  | (#29) | (#21)  | (#10)     |
| Vanilla             | GPT-4-Turbo      | 14.2   | 16.7     | 12.2           | 14.6   | 17.2  | 9.5    | 10.0      |
| ↓ Actions           | GPT-4-Turbo      | 25.8   | 22.9     | 24.4           | 34.2   | 31.0  | 19.1   | 10.0      |
| Above + X Scrolling | GPT-4-Turbo      | 30.0   | 29.2     | 29.3           | 36.6   | 24.1  | 38.1   | 10.0      |
| Above + Obs Opt.    | GPT-4-Turbo      | 34.7   | 37.5     | 34.2           | 22.0   | 41.4  | 57.1   | 10.0      |
| Above + History     | GPT-4-Turbo      | 36.8   | 39.6     | 34.2           | 36.6   | 44.8  | 38.1   | 10.0      |
| AGENTOCCAM          | GPT-4-Turbo      | 44.2   | 45.8     | 46.3           | 48.8   | 41.4  | 47.6   | 10.0      |
| Vanilla             | Gemini-1.5-Flash | 11.6   | 20.8     | 4.9            | 9.8    | 17.2  | 4.8    | 0.0       |
| ↓ Actions           | Gemini-1.5-Flash | 23.2   | 29.2     | 22.0           | 29.3   | 13.8  | 19.1   | 10.0      |
| Above + X Scrolling | Gemini-1.5-Flash | 24.2   | 33.3     | 24.4           | 22.0   | 27.6  | 14.3   | 0.0       |
| Above + Obs Opt.    | Gemini-1.5-Flash | 30.0   | 37.5     | 34.2           | 31.7   | 20.7  | 23.8   | 10.0      |
| Above + History     | Gemini-1.5-Flash | 32.1   | 35.4     | 31.7           | 31.7   | 37.9  | 28.6   | 10.0      |
| AGENTOCCAM          | Gemini-1.5-Flash | 33.7   | 37.5     | 34.2           | 36.6   | 37.9  | 28.6   | 0.0       |

definite and time-invariant, and ones with "possible" answers that are either open-ended with multiple potential answers or related to real-time information. We use WebVoyager questions with golden answers to avoid subjective human evaluations. We acknowledge that other WebVoyager tasks might test more web agent skills, but since they are not defined on static web pages, and thus their solutions would change over time, each new web agent's success rate would require human assessment of trajectories. Due to the subjectivity of human annotation (as evidenced by the high variance in our main experiment's human annotations provided alongside the code<sup>8</sup>), these results aren't comparable. We can't expect the same group of human annotators to label all previous agents' trajectories for every new agent, so we regretfully omit other tasks. Additionally, we exclude GitHub tasks, as the site's anti-scraping measures frequently cause page loading timeouts. Additionally, due to these measures, GitHub limits interactable elements, which prevents web page proper functionality, and the IP address hosting the agent is at risk of being banned. In contrast, WebArena's simulated GitLab environment mimics GitHub, enabling us to demonstrate AGENTOCCAM's performance on similar tasks using existing results. In a nutshell, we have 129 tasks from WebVoyager with definite golden answers across 13 real-world web environments, including Allrecipes, Amazon, Apple, ArXiv, BBC News, Booking, Cambridge Dictionary, Coursera, ESPN, Google Map, Google Search, Huggingface, and Wolfram Alpha.

Our baseline on WebVoyager is the concurrent work Agent-E (Abuelsaad et al., 2024), which introduces several architectural improvements like the planner-browser-reflector agent architecture and the browser's document object model selection. It achieves the previous SOTA on the full WebVoyager with the assessments done by humans. As they didn't report agent trajectory logs, we replicate their work on the WebVoyager subset introduced in the above paragraph, evaluated with the same definite-answer-based hard-coded evaluators as ours. We run each task once for both agents.

Based on the results in Table 9, AGENTOCCAM performs better than Agent-E on WebVoyager's definite-answer-subset. Specifically, both agents have their specificities. We find that Agent-E makes an edge on websites like Wolfram Alpha with more delicate plans issued by its "planner," and AGENTOCCAM outperforms it on websites like Google Search and Hugging Face with more accurate task interpretation and information retrieval. The impressive results across 10+ websites and many types of tasks can show AGENTOCCAM's generalizability in the web environment.

#### <span id="page-17-0"></span>D AGENTOCCAM'S GENERALIZABILITY TO BASE MODEL FAMILIES

We conduct the full set of ablation studies on a WebArena development subset with GEMINI-1.5-FLASH (Google, 2024), a model trained with different data from the GPT model family.

Due to the cost constraints, we construct a representative subset from the original 812 tasks in WebArena. Specifically, we sample one task from each task cluster instantiated with the same intent

<span id="page-17-1"></span><sup>&</sup>lt;sup>8</sup>We would like to thank Yuhao Cheng, Tong Li, Yuren Hao, Ye Wu, and Xiaoxuan Wang for helping assess the agent trajectories.

<span id="page-18-1"></span>Table 11: Action statistics for the ablation study of AGENTOCCAM's components with models GPT-4-TURBO and GEMINI-1.5-FLASH on the WebArena's development set.

| Exp.                                      | Model                 |      |    |     |   |     |   | click hover type press scroll new tab go back goto |     | note |     | stop go homebranch prune |    |    |
|-------------------------------------------|-----------------------|------|----|-----|---|-----|---|----------------------------------------------------|-----|------|-----|--------------------------|----|----|
| Vanilla                                   | GPT-4-Turbo           | 473  | 26 | 212 | 1 | 22  | 4 | 9                                                  | 115 | -    | -   | -                        | -  | -  |
| ↓ Actions                                 | GPT-4-Turbo           | 1612 | -  | 515 | - | 107 | - | 16                                                 | -   | 40   | 120 | 5                        | -  | -  |
| Above + X Scrolling                       | GPT-4-Turbo           | 1641 | -  | 491 | - | -   | - | 19                                                 | -   | 60   | 128 | 5                        | -  | -  |
| Above + Obs Opt.                          | GPT-4-Turbo           | 1539 | -  | 437 | - | -   | - | 21                                                 | -   | 82   | 137 | 1                        | -  | -  |
| Above + History                           | GPT-4-Turbo           | 1068 | -  | 287 | - | -   | - | 24                                                 | -   | 23   | 181 | 24                       | -  | -  |
| AGENTOCCAM                                | GPT-4-Turbo           | 1110 | -  | 261 | - | -   | - | 123                                                | 1   | 40   | 183 | 3                        | 9  | 6  |
| Vanilla                                   | Gemini-1.5-Flash      | 103  | 0  | 65  | 0 | 7   | 5 | 0                                                  | 9   | -    | -   | -                        | -  | -  |
| ↓ Actions                                 | Gemini-1.5-Flash 1390 |      | -  | 509 | - | 176 | - | 28                                                 | -   | 31   | 130 | 11                       | -  | -  |
| Above + X Scrolling Gemini-1.5-Flash 1258 |                       |      | -  | 542 | - | -   | - | 23                                                 | -   | 53   | 134 | 22                       | -  | -  |
| Above + Obs Opt.                          | Gemini-1.5-Flash 1322 |      | -  | 377 | - | -   | - | 28                                                 | -   | 29   | 144 | 42                       | -  | -  |
| Above + History                           | Gemini-1.5-Flash      | 776  | -  | 253 | - | -   | - | 50                                                 | -   | 44   | 185 | 15                       | -  | -  |
| AGENTOCCAM                                | Gemini-1.5-Flash      | 942  | -  | 289 | - | -   | - | 67                                                 | -   | 44   | 185 | 34                       | 27 | 75 |

<span id="page-18-2"></span>Table 12: Average observation tokens per step of AGENTOCCAM's components with models GPT-4-TURBO and GEMINI-1.5-FLASH on the WebArena's development set. We use the GPT2 tokenizer from HUGGINGFACE [\(Radford et al.,](#page-11-14) [2019\)](#page-11-14).

| Exp.                | Model            | All    | Shopping | Shopping Admin | GitLab | Map    | Reddit | Multisite |
|---------------------|------------------|--------|----------|----------------|--------|--------|--------|-----------|
| Vanilla             | GPT-4-Turbo      | 2202.5 | 2268.7   | 2421.6         | 2267.3 | 1882.3 | 2119.0 | 1715.8    |
| ↓ Actions           | GPT-4-Turbo      | 1682.1 | 1496.7   | 2186.6         | 2168.3 | 953.3  | 1102.3 | 1261.8    |
| Above + X Scrolling | GPT-4-Turbo      | 3571.2 | 3120.3   | 5175.5         | 4234.9 | 1423.3 | 3079.8 | 1977.9    |
| Above + Obs Opt.    | GPT-4-Turbo      | 2669.8 | 1664.9   | 4274.6         | 2744.3 | 1930.8 | 2664.4 | 1370.6    |
| Above + History     | GPT-4-Turbo      | 3107.0 | 1745.4   | 4988.5         | 3579.2 | 788.0  | 2758.4 | 1856.9    |
| AGENTOCCAM          | GPT-4-Turbo      | 2785.1 | 1500.8   | 5032.8         | 3032.3 | 645.6  | 3476.0 | 1233.9    |
| Vanilla             | Gemini-1.5-Flash | 2303.4 | 2307.0   | 2537.5         | 2707.0 | 1849.7 | 1794.7 | 2037.6    |
| ↓ Actions           | Gemini-1.5-Flash | 1713.9 | 1577.4   | 2112.3         | 2257.1 | 818.5  | 1542.8 | 1177.2    |
| Above + X Scrolling | Gemini-1.5-Flash | 3219.6 | 3110.7   | 5234.0         | 3378.0 | 1040.7 | 3204.9 | 2021.1    |
| Above + Obs Opt.    | Gemini-1.5-Flash | 2814.9 | 1769.8   | 4632.9         | 3410.7 | 858.7  | 3203.5 | 1577.0    |
| Above + History     | Gemini-1.5-Flash | 3283.2 | 1720.7   | 5078.3         | 3657.6 | 734.2  | 5712.5 | 1112.4    |
| AGENTOCCAM          | Gemini-1.5-Flash | 2872.2 | 1639.6   | 4156.3         | 2519.3 | 688.7  | 6241.4 | 1267.7    |

template (e.g., "What is the top-{{n}} best-selling product in {{year}}", where "n" and "{{year}}" would be replaced by instantiation tokens) in WebArena, forming a development set with 190 tasks[9](#page-18-0) . We use Gemini-1.5-flash for all experiments. We run each task once and restart the experiment if the WebArena simulator fails (i.e., login expires, Reddit post limit exceeds, map malfunctioning, etc.). The results and statistics are listed in Table [10,](#page-17-2) [11,](#page-18-1) [12,](#page-18-2) [13,](#page-19-1) with the performance from the GPT-4-turbo counterpart on the same development task set for comparison.

We can observe a similar trend with the Gemini model that each alignment component introduced by our paper contributes to the web agent's overall performance. To be specific, removing non-essential actions (↓ Actions) encourages the agent to explore more actively with commands click and type; disabling scrolling (Above + X Scrolling) proves advantageous in tasks where key information is not presented on the first browser sight; simplifying web page elements (Above + Obs Opt.) reduces the observation token number; selectively replaying web element in one page (Above + History) reduces the steps required to accomplish the task; and planning and selectively replay past pages (AGENTOCCAM) enables the agent to self-organize task workflow and quickly restore to a previous stage after several failed attempts. In conclusion, each alignment component proposed by AGENTOCCAM proves beneficial to the agent system and can be generalized to different base models.

<span id="page-18-0"></span><sup>9</sup>We remove stop in the statistics for the vanilla WebArena agent as this action is excluded in their officially defined action space. However, their agent is allowed by code to generate stop to end the trajectory.

<sup>9</sup>The task ids are: 3, 9, 13, 20, 22, 30, 35, 40, 42, 44, 46, 48, 52, 61, 65, 68, 71, 76, 78, 80, 86, 89, 94, 96, 97, 99, 104, 109, 116, 117, 118, 120, 125, 127, 131, 132, 138, 141, 148, 153, 156, 157, 158, 164, 171, 173, 180, 187, 188, 194, 204, 205, 212, 217, 219, 224, 225, 230, 234, 237, 239, 244, 250, 257, 258, 259, 262, 265, 271, 274, 281, 283, 285, 287, 289, 294, 298, 305, 311, 313, 316, 323, 324, 333, 337, 340, 345, 350, 354, 356, 357, 360, 367, 368, 370, 375, 376, 377, 382, 383, 384, 386, 388, 390, 395, 401, 406, 410, 413, 416, 419, 423, 425, 435, 440, 443, 446, 452, 457, 463, 468, 472, 476, 482, 490, 495, 499, 503, 508, 509, 512, 518, 521, 525, 530, 535, 539, 546, 550, 555, 561, 566, 567, 571, 578, 580, 587, 594, 599, 604, 606, 613, 615, 624, 627, 634, 637, 644, 646, 653, 660, 663, 666, 669, 674, 677, 682, 687, 691, 698, 702, 706, 713, 715, 720, 730, 731, 738, 749, 754, 758, 762, 766, 770, 771, 772, 779, 785, 797, 803.

<span id="page-19-1"></span>Table 13: Average number of steps per task of AGENTOCCAM's components with models GPT-4- TURBO and GEMINI-1.5-FLASH on the WebArena's development set.

| Exp.                | Model            | All | Shopping | Shopping Admin | GitLab | Map | Reddit | Multisite |
|---------------------|------------------|-----|----------|----------------|--------|-----|--------|-----------|
| Vanilla             | GPT-4-Turbo      | 1.3 | 1.5      | 1.3            | 1.1    | 1.4 | 1.3    | 0.9       |
| ↓ Actions           | GPT-4-Turbo      | 3.0 | 2.9      | 3.1            | 3.2    | 3.3 | 2.4    | 2.4       |
| Above + X Scrolling | GPT-4-Turbo      | 2.9 | 2.2      | 3.3            | 3.2    | 3.5 | 2.2    | 2.8       |
| Above + Obs Opt.    | GPT-4-Turbo      | 2.7 | 2.4      | 2.7            | 3.4    | 2.7 | 2.4    | 2.7       |
| Above + History     | GPT-4-Turbo      | 2.0 | 1.3      | 2.4            | 2.4    | 1.8 | 1.4    | 3.2       |
| AGENTOCCAM          | GPT-4-Turbo      | 2.1 | 1.7      | 2.2            | 2.4    | 2.2 | 2.0    | 3.0       |
| Vanilla             | Gemini-1.5-Flash | 0.5 | 0.5      | 0.4            | 0.5    | 0.5 | 0.3    | 0.6       |
| ↓ Actions           | Gemini-1.5-Flash | 2.8 | 3.2      | 2.8            | 2.5    | 2.6 | 2.9    | 2.4       |
| Above + X Scrolling | Gemini-1.5-Flash | 2.5 | 2.4      | 2.2            | 2.4    | 2.7 | 2.7    | 3.3       |
| Above + Obs Opt.    | Gemini-1.5-Flash | 2.4 | 2.5      | 2.3            | 2.8    | 2.4 | 1.9    | 2.2       |
| Above + History     | Gemini-1.5-Flash | 1.6 | 1.6      | 1.7            | 1.7    | 1.4 | 1.5    | 1.7       |
| AGENTOCCAM          | Gemini-1.5-Flash | 2.0 | 1.6      | 2.4            | 2.0    | 2.2 | 1.8    | 2.8       |

# <span id="page-19-0"></span>E EVALUATOR RECTIFICATIONS

## E.1 RECTIFICATION CATEGORIZATION

We only modify the evaluator when it's deemed erroneous due to the wrong task labels or misuse of evaluating functions. When the task definition and corresponding evaluation metric match to some extent but might be misleading to most agents and even to human, we still keep the original ones to ensure the slightest reasonable changes. We emphasize that we re-implement WebArena's base agent SteP's agent with the same web environment and modified evaluators as AGEN-TOCCAM for a fair comparison. For example, we keep the evaluators of shopping tasks defined with template 163, requiring the agent to "Draft an email to the shop owner via their contact us function for a coupon as {reason}", which doesn't explicitly specify whether to submit the drafted email. However, the evaluator is defined to assess the not yet submitted email. All capable LLM-based agents we have tested, which have been aligned to be helpful, will for sure submit the email if not directly prompted to behave in the way the evaluator desires, leading the email field to be blank and thus failing those tasks. Another example of this kind is the Reddit task asking the agent to find the most appropriate subreddit to post (task template 6100), where the assessment of appropriation is very subjective. In all those tasks, we follow the original evaluators, though their evaluation outcomes are arguably questionable.

We categorize our evaluator modifications into two classes, namely label errors and improper evaluation function selection, raise representative examples for each class, and list all the changes made.[10](#page-19-2)

Label errors: We find there exist evaluator definition errors and some typos in the correct answers. In the later cases, the tasks always require exact matching, where any well-aligned LLM-agent would correct those typos in their generation. We thus rectify those errors:

*i)* Evaluator definitions contain errors. For example, in the Reddit task 584, the evaluator would open up the wrong page for the evaluation. Another case in point is the shopping task 261, where the url match evaluator is constrained to identifying one correct url (<server host>:7770/electronics/headphones.html), misjudging the same page (of the identical content) with a different url (<server host>:7770/electronics.html?cat=60). Tasks fall in this category include: 261-264, 351-355, 584, 644, 679, 707-709, 786.

*ii)* The answer contains typos or grammatical errors. For example the is car necessary in NYC in task 601, or the budge in task 603. More tasks of this kind include: task id 240, 298-302, 489, 583, 601, 603, 606, 608, 629, 645-649.

Improper evaluation function selection: Evaluator problems are more obvious in this case with the following types:

<span id="page-19-2"></span><sup>10</sup>As the evaluator is programmed by the WebArena simulator to be revoked only once at the end of each trajectory, our statement of "our approach outperforms the baseline methods with the original evaluators" refers to setting all the rewards of the trajectories with modified evaluators to be 0, which can be verified with the reported trajectory logs.

*i)* Use the exact match function that compares whether the answer given by a human label-er and the answer returned by the agent is identically the same. Errors occur when the agent returns a fullform or a more complete answer, where the evaluators' labels cannot match. For example, in Reddit task 644 that requires the agent to post a meeting notice with the meeting date, where the keyword match for such date is exactly the Dec 15th, where the evaluator would judge other answers like December 15th as incorrect, where we change the keyword matching to one that could match both Dec 15th and December 15th. (In other cases with a single answer, we simply replace exact match with fuzzy match, which for instance in task 254 it could match 4125785000 with the agent's answer The phone number is 4125785000; or replace exact match with must include, which for instance in task 363 it could match 778m with the agent's answer 778 m.) It also demands that the answer should strictly include expressions like virtual meetup, where the agent might add other words in the virtual and meetup. In that sense, we also split the keyword virtual meetup into two separate keywords, i.e., virtual and meetup. Tasks of this kind include: task id 97, 118, 146, 178-182, 254, 293-297, 308-312, 330, 363-367, 415-418, 528-532, 640-649, 653-657.

*ii)* Use the poorly defined fuzzy match function, that would view the answer returned as unqualified for the missing-from-expression answer exploration process, or assess answers with more detailed answers as partially correct (reward=0). We thus shift our prompt for the fuzzy match function from: *'Help a teacher to grade the answer of a student given a question. Keep in mind that the student may use different phrasing or wording to answer the question. The goal is to evaluate whether the answer is semantically equivalent to the reference answer."* to *'Help a teacher to grade the answer of a student given a question. Keep in mind that the student has executed the actions to get the answer. They are allowed to use different phrasing or wording to answer the question. The goal is to evaluate whether the key points in the reference answer are included in the student's answer. We allow answers with additional information that doesn't contradict the reference answer and review them as fully (not partially) correct."*

*iii)* Misuse the fuzzy match function by splitting the keyword list for matching into a list, where each of the keyword and the entire answer, would be evaluated as partially correct (reward=0). In other words, no answer would be assessed as the correct answer (even the gloden-standard answer itself) due to such evaluator function misuse. This could be inferred from the function and the evaluator's definition. Tasks of this type include: task id 16-20, In such tasks, we simply merge the list of keywords into a string, concatenated with "; ". For instance, for task 16, the previous fuzzy match field is ["driving: 2min", "walking: 16min"], and we modify it to ["driving: 2min; walking: 16min"].

## E.2 DETAILS

```
# Task 16
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' d r i v i n g : 2min ' , ' walking : 16min ' ]
[ ' d r i v i n g : 2min ; walking : 16min ' ]
# Task 17
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' d r i v i n g : 13min ' , ' walking : 1h 35min ' ]
[ ' d r i v i n g : 13 min ; walking : 1h 35min ' ]
# Task 18
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' d r i v i n g : 15min ' , ' walking : 1h 47min ' ]
[ ' d r i v i n g : 15 min ; walking : 1h 47min ' ]
# Task 19
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' d r i v i n g : 12min ' , ' walking : 1h 44 min . ' ]
[ ' d r i v i n g : 12 min ; walking : 1h 44 min . ' ]
# Task 20
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' d r i v i n g : 13min ' , ' walking : 1h 45min ' ]
[ ' d r i v i n g : 13 min ; walking : 1h 45min ' ]
# Task 97
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ '914km ' ]
[ '914km |OR| 914 km ' ]
# Task 118
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' jaw bruxism ' , ' mouth guard ']}}]
```

```
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' jaw ' , ' bruxism ' , ' mouth guard ']}}]
# Task 146
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ '16 x24 ' ]
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ '16 x24 ' ]
# Task 178
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
Yes
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' Yes , i t i s c l o s e d ' ]
# Task 179
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
Yes
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' Yes , i t i s c l o s e d ' ]
# Task 180
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
No
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' No , i t i s open ' ]
# Task 181
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
No
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' No , i t i s open ' ]
# Task 182
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
Yes
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ ' Yes , i t i s c l o s e d ' ]
# Task 240
### i n s t a n t i a t i o n d i c t . p r o d u c t c a t e g o r y
c o m p e t i t i v e swimwear
c o m p e t a t i v e swimwear
### i n t e n t
I am doing a market s u r v e y f o r one s t o p market , show me t h e most e x p e n s i v e p r o d u c t from c o m p e t i t i v e swimwear
         c a t e g o r y
I am doing a market s u r v e y f o r one s t o p market , show me t h e most e x p e n s i v e p r o d u c t from c o m p e t a t i v e swimwear
         c a t e g o r y
# Task 254
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
4125785000
### e v a l . r e f e r e n c e a n s w e r s . f u z z y m a t c h
[ '4125785000 ']
# Task 261
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / e l e c t r o n i c s . html ? c a t =60 '}]
# Task 262
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / c l o t h i n g − shoes − j e w e l r y . html ? c a t =145 '}]
# Task 263
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / c l o t h i n g − shoes − j e w e l r y . html ? c a t =143 '}]
# Task 264
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / o f f i c e − p r o d u c t s . html ? c a t =187 '}]
# Task 293
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / convexegg / s u p e r a w e s o m e r o b o t . g i t
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / convexegg / s u p e r a w e s o m e r o b o t . g i t ' ]
# Task 294
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / convexegg / c h a t g p t . g i t
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / convexegg / c h a t g p t . g i t ' ]
# Task 295
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / r o o t / metaseq . g i t
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / r o o t / metaseq . g i t ' ]
# Task 296
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / e r i k l i n d e r n o r e n / PyTorch −GAN. g i t
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
```

```
[ ' g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / e r i k l i n d e r n o r e n / PyTorch −GAN. g i t ' ]
# Task 297
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / y j l o u /2019 − nCov . g i t
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' g i t c l o n e s s h : / / g i t @ m e t i s . l t i . cs . cmu . edu : 2 2 2 2 / y j l o u /2019 − nCov . g i t ' ]
# Task 298
### i n t e n t t e m p l a t e
Show t h e most r e c e n t {{ s t a t u s }} o r d e r
Show t h e most r e c e n t {{ s t a t u s }} o r d e r page
### i n t e n t
Show t h e most r e c e n t completed o r d e r
Show t h e most r e c e n t completed o r d e r page
# Task 299
### i n t e n t t e m p l a t e
Show t h e most r e c e n t {{ s t a t u s }} o r d e r
Show t h e most r e c e n t {{ s t a t u s }} o r d e r page
### i n t e n t
Show t h e most r e c e n t c a n c e l l e d o r d e r
Show t h e most r e c e n t c a n c e l l e d o r d e r page
# Task 300
### i n t e n t t e m p l a t e
Show t h e most r e c e n t {{ s t a t u s }} o r d e r
Show t h e most r e c e n t {{ s t a t u s }} o r d e r page
### i n t e n t
Show t h e most r e c e n t pending o r d e r
Show t h e most r e c e n t pending o r d e r page
# Task 301
### i n t e n t t e m p l a t e
Show t h e most r e c e n t {{ s t a t u s }} o r d e r
Show t h e most r e c e n t {{ s t a t u s }} o r d e r page
### i n t e n t
Show t h e most r e c e n t p r o c e s s i n g o r d e r
Show t h e most r e c e n t p r o c e s s i n g o r d e r page
# Task 302
### i n t e n t t e m p l a t e
Show t h e most r e c e n t {{ s t a t u s }} o r d e r
Show t h e most r e c e n t {{ s t a t u s }} o r d e r page
### i n t e n t
Show t h e most r e c e n t o u t of d e l i v e r y o r d e r
Show t h e most r e c e n t o u t of d e l i v e r y o r d e r page
# Task 308
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
Shawn A l l e n
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' Shawn Allen ' ]
# Task 309
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
Grayson Wright
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' Grayson Wright ' ]
# Task 310
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
tokudu
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' tokudu ' ]
# Task 311
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
E r i k Linder −Nor\' en
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' E r i k Linder −Nor\'en ' ]
# Task 312
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
C h r i s t o p h e r Groskopf
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' C h r i s t o p h e r Groskopf ' ]
# Task 330
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' 8 1 . 3 1 ' ]
[ ' 8 3 . 3 1 ' ]
### e v a l . r e f e r e n c e a n s w e r r a w a n n o t a t i o n
8 1 . 3 1
8 3 . 3 1
# Task 351
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / video −games . html ? c a t =67& p r o d u c t l i s t o r d e r = p r i c e '}]
# Task 352
### e v a l . or
```

```
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / h e a l t h − h o u s e h o l d . html ? c a t =192& p r o d u c t l i s t o r d e r = p r i c e '}]
# Task 353
### i n s t a n t i a t i o n d i c t . p r o d u c t c a t e g o r y
c o m p e t i t i v e swimwear
c o m p e t a t i v e swimwear
### i n t e n t
L i s t p r o d u c t s from c o m p e t i t i v e swimwear c a t e g o r y by a s c e n d i n g p r i c e
L i s t p r o d u c t s from c o m p e t a t i v e swimwear c a t e g o r y by a s c e n d i n g p r i c e
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / c l o t h i n g − shoes − j e w e l r y . html ? c a t =149& p r o d u c t l i s t o r d e r = p r i c e '}]
# Task 354
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / home− k i t c h e n . html ? c a t =154& p r o d u c t l i s t o r d e r = p r i c e&p r o d u c t l i s t d i r =
         desc '}]
# Task 355
### e v a l . or
[{ ' r e f e r e n c e u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 7 0 / home− k i t c h e n . html ? c a t =155& p r o d u c t l i s t d i r =desc '}]
# Task 363
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
748m
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ '778m |OR| 778 m' ]
### e v a l . r e f e r e n c e a n s w e r r a w a n n o t a t i o n
748m
778m
# Task 364
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
1 . 7km
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' 1 . 7 km |OR| 1 . 7 km ' ]
# Task 365
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
2 . 2km
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' 2 . 2 km |OR| 2 . 2 km ' ]
# Task 366
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
1 . 2km
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' 1 . 2 km |OR| 1 . 2 km ' ]
# Task 367
### e v a l . r e f e r e n c e a n s w e r s . e x a c t m a t c h
1 . 4km
1 . 4km |OR| 1 . 4 km
# Task 415
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / b y t e b l a z e / a11y − webring . c l u b / − / m e r g e r e q u e s t s / 4 0 ' , ' l o c a t o r ' : ' document .
          q u e r y S e l e c t o r (\ ' [ i d =" n o t e s − l i s t "\ ') . l a s t E l e m e n t C h i l d . q u e r y S e l e c t o r (\ ' . t i m e l i n e − d i s c u s s i o n −body \ ') .
          o u t e r T e x t ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : ' @davepgreene '}}]
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / b y t e b l a z e / a11y − webring . c l u b / − / m e r g e r e q u e s t s / 4 0 ' , ' l o c a t o r ' : ' document .
          q u e r y S e l e c t o r (\ ' [ i d =" n o t e s − l i s t "\ ') . l a s t E l e m e n t C h i l d . q u e r y S e l e c t o r (\ ' . t i m e l i n e − d i s c u s s i o n −body \ ') .
          o u t e r T e x t ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' @davepgreene ']}}]
# Task 416
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / a 1 1 y p r o j e c t / a 1 1 y p r o j e c t . com / − / m e r g e r e q u e s t s / 1 2 7 0 ' , ' l o c a t o r ' : ' document .
          q u e r y S e l e c t o r (\ ' [ i d =" n o t e s − l i s t "\ ') . l a s t E l e m e n t C h i l d . q u e r y S e l e c t o r (\ ' . t i m e l i n e − d i s c u s s i o n −body \ ') .
          o u t e r T e x t ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : ' Thank you '}}]
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / a 1 1 y p r o j e c t / a 1 1 y p r o j e c t . com / − / m e r g e r e q u e s t s / 1 2 7 0 ' , ' l o c a t o r ' : ' document .
          q u e r y S e l e c t o r (\ ' [ i d =" n o t e s − l i s t "\ ') . l a s t E l e m e n t C h i l d . q u e r y S e l e c t o r (\ ' . t i m e l i n e − d i s c u s s i o n −body \ ') .
          o u t e r T e x t ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Thank you ']}}]
# Task 417
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / a 1 1 y p r o j e c t / a 1 1 y p r o j e c t . com / − / m e r g e r e q u e s t s / 1 4 8 5 ' , ' l o c a t o r ' : ' document .
          q u e r y S e l e c t o r (\ ' [ i d =" n o t e s − l i s t "\ ') . l a s t E l e m e n t C h i l d . q u e r y S e l e c t o r (\ ' . t i m e l i n e − d i s c u s s i o n −body \ ') .
          o u t e r T e x t ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : ' @Roshanjossey '}}]
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / a 1 1 y p r o j e c t / a 1 1 y p r o j e c t . com / − / m e r g e r e q u e s t s / 1 4 8 5 ' , ' l o c a t o r ' : ' document .
          q u e r y S e l e c t o r (\ ' [ i d =" n o t e s − l i s t "\ ') . l a s t E l e m e n t C h i l d . q u e r y S e l e c t o r (\ ' . t i m e l i n e − d i s c u s s i o n −body \ ') .
          o u t e r T e x t ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' @Roshanjossey ']}}]
# Task 418
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / b y t e b l a z e ' , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . cover − s t a t u s ' ) . l a s t C h i l d .
          t e x t C o n t e n t " , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : ' Busy '}}]
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 8 0 2 3 / b y t e b l a z e ' , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . cover − t i t l e ' ) . t e x t C o n t e n t " , '
          r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Busy ']}}]
# Task 489
### i n s t a n t i a t i o n d i c t . h e a d i n g
No p r i v a c y p o l i c y i s needed i s t h i s d y s t o p i a n world
No p r i v a c y p o l i c y i s needed i n t h i s d y s t o p i a n world
### i n t e n t
```

```
Change t h e page t i t l e of " P r i v a c y P o l i c y " page on my s i t e t o "No p r i v a c y p o l i c y i s needed i s t h i s d y s t o p i a n
         world " .
Change t h e page t i t l e of " P r i v a c y P o l i c y " page on my s i t e t o "No p r i v a c y p o l i c y i s needed i n t h i s d y s t o p i a n
         world " .
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 8 0 / admin / cms / page / e d i t / p a g e i d / 4 / ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' i n p u t [
        name=" t i t l e "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : 'No p r i v a c y p o l i c y i s needed i s t h i s
         d y s t o p i a n world '}}]
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 7 7 8 0 / admin / cms / page / e d i t / p a g e i d / 4 / ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' i n p u t [
        name=" t i t l e "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : 'No p r i v a c y p o l i c y i s needed i n t h i s
         d y s t o p i a n world '}}]
# Task 528
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '000000180 ' ,
         '1 2.9 9 ' ]}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '000000180 ' , '12 .99 ']}}]
# Task 529
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '000000148 ' ,
         '169.95 ']}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '000000148 ' , '169.95 ']}}]
# Task 530
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '000000161 ' ,
         '6 8.8 8 ' ]}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '000000161 ' , '68 .88 ']}}]
# Task 531
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '000000180 ' , ' $12
         . 9 9 ' ]}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '000000180 ' , ' $12 . 9 9 ' ]}}]
# Task 532
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '000000180 ' ,
         ' 1 . 6 3 ' ]}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '000000180 ' , ' 1 . 6 3 ' ]}}]
# Task 583
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 9 9 9 9 / f / P l a n t s F o r C a t P a r e n t s / e d i t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " #
         f o r u m d e s c r i p t i o n " ) . value ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Cat p a r e n t s & p l a n l o v e r s ']}} , {' u r l
         ' : ' h t t p : / / l o c a l h o s t : 9 9 9 9 / f / P l a n t s F o r C a t P a r e n t s / e d i t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " #
         f o r u m s i d e b a r " ) . value ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Cat f r i e n d l y ' , ' Local vendors ' , '
         Promotion ' , ' Toxic p l a n t s ! ']}}]
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 9 9 9 9 / f / P l a n t s F o r C a t P a r e n t s / e d i t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " #
         f o r u m d e s c r i p t i o n " ) . value ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Cat p a r e n t s & p l a n t l o v e r s ']}} , {'
         u r l ' : ' h t t p : / / l o c a l h o s t : 9 9 9 9 / f / P l a n t s F o r C a t P a r e n t s / e d i t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " #
         f o r u m s i d e b a r " ) . value ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Cat f r i e n d l y ' , ' Local vendors ' , '
         Promotion ' , ' Toxic p l a n t s ! ']}}]
# Task 584
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 9 9 9 9 / f / Karaoke ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " # f o r u m d e s c r i p t i o n " ) . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' P l a c e f o r Karaoke l o v e r s ']}} , {' u r l ' : ' h t t p : / / l o c a l h o s t : 9 9 9 9 / f /
        Karaoke ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " # f o r u m s i d e b a r " ) . value ' , ' r e q u i r e d c o n t e n t s ' : {'
         m u s t i n c l u d e ' : [ ' d e v i c e s ' , ' s e t u p ']}}]
[{ ' u r l ' : ' h t t p : / / l o c a l h o s t : 9 9 9 9 / f / Karaoke / e d i t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " # f o r u m d e s c r i p t i o n " ) .
         value ' , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' P l a c e f o r Karaoke l o v e r s ']}} , {' u r l ' : ' h t t p : / / l o c a l h o s t
         : 9 9 9 9 / f / Karaoke / e d i t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " # f o r u m s i d e b a r " ) . value ' , ' r e q u i r e d c o n t e n t s ' :
          {' m u s t i n c l u d e ' : [ ' d e v i c e s ' , ' s e t u p ']}}]
# Task 601
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' i s c a r n e c e s s a r y i n NYC']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' i s c a r n e c e s s a r y i n NYC |OR| i s a c a r n e c e s s a r y i n
        NYC']}}]
# Task 603
### i n s t a n t i a t i o n d i c t . q u e s t i o n
s a f e and budge a p a r t m e n t t o l i v e i n nyc
s a f e and b u d g e t a p a r t m e n t t o l i v e i n nyc
### i n t e n t
P o s t my q u e s t i o n , " s a f e and budge a p a r t m e n t t o l i v e i n nyc " , i n a s u b r e d d i t where I 'm l i k e l y t o g e t an answer
P o s t my q u e s t i o n , " s a f e and b u d g e t a p a r t m e n t t o l i v e i n nyc " , i n a s u b r e d d i t where I 'm l i k e l y t o g e t an answer
### e v a l . pr ogr am h tml
```

```
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' s a f e and budge a p a r t m e n t t o l i v e i n nyc ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' s a f e and b u d g e t a p a r t m e n t t o l i v e i n nyc ']}}]
# Task 606
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' i s c a r n e c e s s a r y ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' i s c a r n e c e s s a r y |OR| i s a c a r n e c e s s a r y ']}}]
# Task 608
### i n s t a n t i a t i o n d i c t . q u e s t i o n
s a f e and budge a p a r t m e n t t o l i v e
s a f e and b u d g e t a p a r t m e n t t o l i v e
### i n t e n t
Find a s u b r e d d i t f o c u s e d on t o p i c s r e l a t e d t o c i t y l i v e s i n DMV area , and p o s t my q u e s t i o n , " s a f e and budge
         a p a r t m e n t t o l i v e " t h e r e
Find a s u b r e d d i t f o c u s e d on t o p i c s r e l a t e d t o c i t y l i v e s i n DMV area , and p o s t my q u e s t i o n , " s a f e and b u d g e t
         a p a r t m e n t t o l i v e " t h e r e
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' s a f e and budge a p a r t m e n t t o l i v e ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' s a f e and b u d g e t a p a r t m e n t t o l i v e ']}}]
# Task 629
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' your o p i n i o n ' , ' Fun t h i n g t o do i n P i t t s b u r g h ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' your o p i n i o n ' , ' Fun t h i n g t o do i n P i t t s b u r g h |OR|
         Fun t h i n g s t o do i n P i t t s b u r g h ']}}]
# Task 640
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' book r e a d i n g ' , ' March 15 th ' , ' v i r t u a l meetup ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' book r e a d i n g ' , 'Mar 15 t h |OR| March 15 th ' , ' v i r t u a l
         ' , ' meetup ']}}]
# Task 641
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Harry P o t t e r ' , ' J u l y 8 th ' , ' v i r t u a l meetup ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Harry P o t t e r ' , ' J u l 8 t h |OR| J u l y 8 th ' , ' v i r t u a l ' , '
         meetup ']}}]
# Task 642
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Big l i t t l e l i e s ' , ' Sep 10 th ' , ' v i r t u a l meetup ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Big l i t t l e l i e s ' , ' Sep 10 t h |OR| September 10 th ' , '
         v i r t u a l ' , ' meetup ']}}]
# Task 643
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' r a c i n g c a r s ' , ' Oct 21 s t ' , ' v i r t u a l meetup ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' r a c i n g c a r s ' , ' Oct 21 s t |OR| October 21 s t ' , ' v i r t u a l
         ' , ' meetup ']}}]
# Task 644
### i n s t a n t i a t i o n d i c t . s u b r e d d i t
games
gaming
### i n t e n t
P o s t a n o t i c e on a v i r t u a l meetup f o r T e a r s of Kingdom e n t h u s i a s t s on Dec 15 t h i n t h e games s u b r e d d i t
P o s t a n o t i c e on a v i r t u a l meetup f o r T e a r s of Kingdom e n t h u s i a s t s on Dec 15 t h i n t h e gaming s u b r e d d i t
### e v a l . r e f e r e n c e u r l
h t t p : / / l o c a l h o s t : 9 9 9 9 / f / games
h t t p : / / l o c a l h o s t : 9 9 9 9 / f / gaming
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' T e a r s of Kingdom ' , ' Dec 15 th ' , ' v i r t u a l meetup ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' T e a r s of Kingdom ' , ' Dec 15 t h |OR| December 15 th ' , '
         v i r t u a l ' , ' meetup ']}}]
# Task 645
### i n t e n t t e m p l a t e
P o s t i n {{s u b r e d d i t}} s u b r e d d i t a b o u t what c o u l d machine l e a r n i n g h e l p t h e c o r r e p o n g f i e l d .
P o s t i n {{s u b r e d d i t}} s u b r e d d i t a b o u t what c o u l d machine l e a r n i n g h e l p t h e c o r r e s p o n d i n g f i e l d .
### i n t e n t
P o s t i n books s u b r e d d i t a b o u t what c o u l d machine l e a r n i n g h e l p t h e c o r r e p o n g f i e l d .
P o s t i n books s u b r e d d i t a b o u t what c o u l d machine l e a r n i n g h e l p t h e c o r r e s p o n d i n g f i e l d .
### e v a l . pr ogr am h tml
```

```
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' machine l e a r n i n g ' , ' help ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' machine l e a r n i n g ' , ' h e l p |OR| a s s i s t |OR| b e n e f i t |
        OR| improve |OR| enhance |OR| t r a n s f o r m |OR| r e v o l u t i o n i z e ']}}]
# Task 646
### i n t e n t t e m p l a t e
P o s t i n {{s u b r e d d i t}} s u b r e d d i t a b o u t what c o u l d m i d j o u r n e y h e l p t h e c o r r e p o n g f i e l d .
P o s t i n {{s u b r e d d i t}} s u b r e d d i t a b o u t what c o u l d m i d j o u r n e y h e l p t h e c o r r e s p o n d i n g f i e l d .
### i n t e n t
P o s t i n DIY s u b r e d d i t a b o u t what c o u l d m i d j o u r n e y h e l p t h e c o r r e p o n g f i e l d .
P o s t i n DIY s u b r e d d i t a b o u t what c o u l d m i d j o u r n e y h e l p t h e c o r r e s p o n d i n g f i e l d .
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' midjourney ' , ' help ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' midjourney ' , ' h e l p |OR| a s s i s t |OR| b e n e f i t |OR|
        improve |OR| enhance |OR| t r a n s f o r m |OR| r e v o l u t i o n i z e ']}}]
# Task 647
### i n t e n t t e m p l a t e
P o s t i n {{s u b r e d d i t}} forum a b o u t what c o u l d open − s o u r c e LLMs h e l p t h e c o r r e p o n g f i e l d .
P o s t i n {{s u b r e d d i t}} forum a b o u t what c o u l d open − s o u r c e LLMs h e l p t h e c o r r e s p o n d i n g f i e l d .
### i n t e n t
P o s t i n t e c h n o l o g y forum a b o u t what c o u l d open − s o u r c e LLMs h e l p t h e c o r r e p o n g f i e l d .
P o s t i n t e c h n o l o g y forum a b o u t what c o u l d open − s o u r c e LLMs h e l p t h e c o r r e s p o n d i n g f i e l d .
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' open − s o u r c e LLMs' , ' help ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' open − s o u r c e LLMs' , ' h e l p |OR| a s s i s t |OR| b e n e f i t |
        OR| improve |OR| enhance |OR| t r a n s f o r m |OR| r e v o l u t i o n i z e ']}}]
# Task 648
### i n t e n t t e m p l a t e
P o s t i n {{s u b r e d d i t}} forum a b o u t what c o u l d l a r g e l a n g u a g e models h e l p t h e c o r r e p o n g f i e l d .
P o s t i n {{s u b r e d d i t}} forum a b o u t what c o u l d l a r g e l a n g u a g e models h e l p t h e c o r r e s p o n d i n g f i e l d .
### i n t e n t
P o s t i n d a t a i s b e a u t i f u l forum a b o u t what c o u l d l a r g e l a n g u a g e models h e l p t h e c o r r e p o n g f i e l d .
P o s t i n d a t a i s b e a u t i f u l forum a b o u t what c o u l d l a r g e l a n g u a g e models h e l p t h e c o r r e s p o n d i n g f i e l d .
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' l a r g e l a n g u a g e models ' , ' help ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' l a r g e l a n g u a g e models ' , ' h e l p |OR| a s s i s t |OR|
         b e n e f i t |OR| improve |OR| enhance |OR| t r a n s f o r m |OR| r e v o l u t i o n i z e ']}}]
# Task 649
### i n t e n t t e m p l a t e
P o s t i n {{s u b r e d d i t}} s u b r e d d i t a b o u t what c o u l d d i f f u s i o n model h e l p t h e c o r r e p o n g f i e l d .
P o s t i n {{s u b r e d d i t}} s u b r e d d i t a b o u t what c o u l d d i f f u s i o n model h e l p t h e c o r r e s p o n d i n g f i e l d .
### i n t e n t
P o s t i n h i s t o r y s u b r e d d i t a b o u t what c o u l d d i f f u s i o n model h e l p t h e c o r r e p o n g f i e l d .
P o s t i n h i s t o r y s u b r e d d i t a b o u t what c o u l d d i f f u s i o n model h e l p t h e c o r r e s p o n d i n g f i e l d .
### e v a l . pr ogr am h tml
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' d i f f u s i o n model ' , ' help ']}}]
[{ ' u r l ' : " fu n c : r e d d i t g e t p o s t u r l ( ' l a s t u r l ' ) " , ' l o c a t o r ' : " document . q u e r y S e l e c t o r ( ' . s u b m i s s i o n i n n e r ' ) .
         o u t e r T e x t " , ' r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' d i f f u s i o n model ' , ' h e l p |OR| a s s i s t |OR| b e n e f i t |OR
        | improve |OR| enhance |OR| t r a n s f o r m |OR| r e v o l u t i o n i z e ']}}]
# Task 653
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '000000180 ' , '
        B087QJN9W1 ']}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke a f t e r ' , ' t h r e e days of use ' , '000000180 ' , '
        B087QJN9W1 ']}}]
# Task 654
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '161 ' , 'B09P7BFL4H
        ']}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '161 ' , 'B09P7BFL4H ']}}]
# Task 655
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '180 ' , 'B087QJN9W1
        ']}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '180 ' , 'B087QJN9W1 ']}}]
# Task 656
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' i t broke a f t e r t h r e e days of use ' , '180 ' , 'B0041MSF2S
        ']}}]
```

```
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '180 ' , 'B0041MSF2S ']}}]
# Task 657
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke a f t e r t h r e e days of use ' , '148 ' , 'B003FVW3VA']}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ t i t l e ="What ' s on your mind ?"\ ') . value ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' refund ' , ' broke ' , ' t h r e e days of use ' , '148 ' , 'B003FVW3VA']}}]
# Task 679
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " d i v . a d m i n d a t a − g r i d − f i l t e r s − c u r r e n t " ) . o u t e r T e x t ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Completed ']}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r ( " d i v . a d m i n d a t a − g r i d − f i l t e r s − c u r r e n t " ) . o u t e r T e x t ' , '
         r e q u i r e d c o n t e n t s ' : {' m u s t i n c l u d e ' : [ ' Complete ']}}]
# Task 707
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t f r o m "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' :
         {' e x a c t m a t c h ' : '1/1/2022 '}} , {' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t t o
         "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : '12/31/2022 '}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t f r o m "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' :
         {' e x a c t m a t c h ' : '1/1/22 '}} , {' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t t o
         "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : '12/31/22 '}}]
# Task 708
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t f r o m "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' :
         {' e x a c t m a t c h ' : '1/1/2023 '}} , {' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t t o
         "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : '12/31/2023 '}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t f r o m "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' :
         {' e x a c t m a t c h ' : '1/1/23 '}} , {' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t t o
         "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : '12/31/23 '}}]
# Task 709
### e v a l . pr ogr am h tml
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t f r o m "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' :
         {' e x a c t m a t c h ' : '5/1/2021 '}} , {' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t t o
         "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : '3/31/2022 '}}]
[{ ' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t f r o m "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' :
         {' e x a c t m a t c h ' : '5/1/21 '}} , {' u r l ' : ' l a s t ' , ' l o c a t o r ' : ' document . q u e r y S e l e c t o r (\ ' [ i d =" s a l e s r e p o r t t o
         "\ ') . value ' , ' r e q u i r e d c o n t e n t s ' : {' e x a c t m a t c h ' : ' 3/ 31 /2 2 '}}]
# Task 786
### e v a l . r e f e r e n c e a n s w e r s . m u s t i n c l u d e
[ ' 4 1 2 ' ]
[ ' 4 1 4 ' ]
```

Table 14: Action statistics.

<span id="page-27-0"></span>

| Exp.               | click | hover | type |    | scroll go back | goto | note | stop | go home branch |     | prune |
|--------------------|-------|-------|------|----|----------------|------|------|------|----------------|-----|-------|
| AGENTOCCAM         | 4715  | -     | 1159 | -  | 339            | -    | 197  | 769  | 42             | 34  | 47    |
| AGENTOCCAM + SteP  | 5235  | 198   | 1407 | 11 | 25             | 132  | 124  | 1733 | -              | -   | -     |
| AGENTOCCAM + Judge | 4893  | -     | 1297 | -  | 261            | -    | 127  | 726  | 94             | 220 | 41    |

Table 15: Average number of steps per task across all WebArena sites.

<span id="page-27-1"></span>

| Exp.               | All  | Shopping | Shopping Admin | GitLab | Map  | Reddit | Multisite |
|--------------------|------|----------|----------------|--------|------|--------|-----------|
| AGENTOCCAM         | 9.0  | 6.7      | 9.2            | 10.8   | 8.5  | 8.6    | 13.3      |
| AGENTOCCAM + SteP  | 11.6 | 10.3     | 12.0           | 10.6   | 12.0 | 14.6   | 11.0      |
| AGENTOCCAM + Judge | 9.4  | 6.7      | 10.5           | 10.6   | 9.6  | 8.4    | 13.5      |

Table 16: Average observation tokens per step across WebArena sites.

<span id="page-27-2"></span>

| Exp.               | All    | Shopping | Shopping Admin | GitLab | Map    | Reddit | Multisite |
|--------------------|--------|----------|----------------|--------|--------|--------|-----------|
| AGENTOCCAM         | 2932.1 | 1634.2   | 4920.7         | 3126.8 | 1056.0 | 3697.8 | 1282.9    |
| AGENTOCCAM + SteP  | 2601.1 | 1675.2   | 3833.3         | 2983.8 | 1196.4 | 3071.4 | 1581.9    |
| AGENTOCCAM + Judge | 2646.4 | 1773.8   | 4181.2         | 2848.4 | 729.7  | 3285.4 | 1433.2    |

# F ADDITIONAL EXPERIMENT DETAILS

We include the trial statistics for experiments that combine AGENTOCCAM with other compound agent policies like SteP's strategies and our newly proposed Judge role. Specifically, [14](#page-27-0) shows these well performing agent are equally open to web environment exploration, actively issuing environment-changing actions like click and type. Not surprisingly, the AGENTOCCAM + SteP

<span id="page-28-0"></span>

| Agent               | Model       | SR (%) | Shopping | Shopping Admin | GitLab | Map    | Reddit | Multisite |
|---------------------|-------------|--------|----------|----------------|--------|--------|--------|-----------|
|                     |             | (#812) | (#187)   | (#182)         | (#180) | (#109) | (#106) | (#48)     |
| Vanilla             | GPT-4-Turbo | 16.5   | 16.6     | 15.9           | 10.0   | 22.9   | 21.7   | 16.7      |
| ↓ Actions           | GPT-4-Turbo | 25.9   | 23.5     | 23.6           | 24.4   | 34.9   | 33.0   | 12.5      |
| Above + X Scrolling | GPT-4-Turbo | 31.7   | 26.2     | 25.3           | 35.0   | 33.0   | 52.8   | 14.6      |
| Above + Obs Opt.    | GPT-4-Turbo | 37.1   | 35.8     | 37.4           | 26.7   | 45.0   | 57.5   | 16.7      |
| Above + History     | GPT-4-Turbo | 38.2   | 33.7     | 40.1           | 31.7   | 50.5   | 51.9   | 14.6      |
| AGENTOCCAM          | GPT-4-Turbo | 43.1   | 40.6     | 45.6           | 37.8   | 46.8   | 61.3   | 14.6      |

Table 17: The success rate (SR) of AGENTOCCAM's ablation study on WebArena.

agent frequently issuing un-interactive actions like hover. From Table 15, we can observe that AGENTOCCAM finish the task with the fewest steps, often yielding a task result with 9 steps. Last, from Table 16, those three agents' token consumptions are of comparative orders of magnitude.

<span id="page-28-1"></span>![](_page_28_Figure_4.jpeg)

Figure 6: Success patterns of AGENTOCCAM (leftmost in each sub figure), AGENTOCCAM + SteP, and AGENTOCCAM + Judge (rightmost) across different sites on WebArena. The y-axis represents task ids, with **green** indicating successful trials and **grey** indicating unsuccessful trials. Notably, tasks defined with the same templates are clustered together.

As shown in Figure 6, agents that combing AGENTOCCAM with compound agent policies possess different behavioral success patterns. For AGENTOCCAM + SteP, it benefits in tasks where the agent could easily be guided with detailed instructions, such as shopping tasks, with more success (green) blocks and denser success rate in tasks defined with the identical templates. However, it falls short in tasks that require generalizable skills like shopping admin tasks, and in tasks where task-specific strategies distract, like reddit tasks. On the contrary, AGENTOCCAM + Judge agent shares similar patterns with the AGENTOCCAM agent except that some of the success blocks are denser, thanks to the behavior rectification enabled by the action generation and selection pipeline.

In addition, we add the success rate figures of the ablation studies in Table 17, which has been visually represented in Figure 5. During development, we slightly modifies AGENTOCCAM's prompt such as improving the wording or correcting the typos of the prompts, which don't affect the semantic meanings of the prompts or add any additional information, and are reflected in the reported trajectory logs. As some failed trajectories are induced by the invalid interaction, we improve the interaction scripts, though not perfectly as it would be beyond the scope of this paper, with the following code shifts:

```
# In browser_env.py

def execute_action(
    action: Action,
    page: Page,
    browser_ctx: BrowserContext,
    obseration_processor: ObservationProcessor,
) -> Page:
    match action_type:
    ...
    case ActionTypes.CLICK:
    # check each kind of locator in order
    # TODO(shuyanzh): order is temp now
```

```
i f a c t i o n [ " e l e m e n t i d " ] :
             node = o b s e r a t i o n p r o c e s s o r . g e t n o d e i n f o b y e l e m e n t i d ( i n t ( e l e m e n t i d ) )
             # i f node and node . r o l e ==" menuitem " and node . p a r e n t and node . p a r e n t . r o l e =="combobox " :
             i f node and ( node . r o l e ==" menuitem " or node . r o l e ==" o p t i o n " ) :
                    t r y :
                          page . g e t b y r o l e ( node . r o l e , name=node . name , e x a c t =True ) . c l i c k ( )
                    e x c e p t :
                          t r y :
                                 page . g e t b y r o l e ( node . r o l e , name=node . name ) . c l i c k ( )
                          e x c e p t :
                                 t r y :
                                       page . g e t b y r o l e ( node . p a r e n t . r o l e , name=node . p a r e n t . name , e x a c t =True ) .
                                                 s e l e c t o p t i o n ( node . name )
                                 e x c e p t :
                                       page . g e t b y r o l e ( node . p a r e n t . r o l e , name=node . p a r e n t . name ) . s e l e c t o p t i o n ( node .
                                                 name )
             # e l i f n o t o b s e r a t i o n p r o c e s s o r . e l e m e n t i s v i s i b l e ( page , e l e m e n t i d ) :
             e l s e :
                    t r y :
                          page . g e t b y r o l e ( node . r o l e , name=node . name , e x a c t =True ) . c l i c k ( )
                    e x c e p t E x c e p t i o n as e :
                          t r y :
                                 # p r i n t ( " Cannot c l i c k by e l e m e n t r o l e and e x a c t name . " , e )
                                 page . g e t b y r o l e ( node . r o l e , name=node . name ) . c l i c k ( )
                          e x c e p t E x c e p t i o n as e :
                                 # p r i n t ( " Cannot c l i c k by e l e m e n t r o l e and f u z z y name . " , e )
                                 e l e m e n t i d = a c t i o n [ " e l e m e n t i d " ]
                                 e l e m e n t c e n t e r = o b s e r a t i o n p r o c e s s o r . g e t e l e m e n t c e n t e r ( e l e m e n t i d , page ) # t y p e
                                          : i g n o r e [ a t t r − d e f i n e d ]
                                 e x e c u t e m o u s e c l i c k ( e l e m e n t c e n t e r [ 0 ] , e l e m e n t c e n t e r [ 1 ] , page )
      e l i f a c t i o n [ " e l e m e n t r o l e " ] and a c t i o n [ " element name " ] :
             e l e m e n t r o l e = i n t ( a c t i o n [ " e l e m e n t r o l e " ] )
             element name = a c t i o n [ " element name " ]
             n t h = a c t i o n [ " n t h " ]
             e x e c u t e f o c u s ( e l e m e n t r o l e , element name , nth , page )
             e x e c u t e c l i c k c u r r e n t ( page )
      e l i f a c t i o n [ " pw code " ] :
             p a r s e d c o d e = p a r s e p l a y w r i g h t c o d e ( a c t i o n [ " pw code " ] )
             l o c a t o r c o d e = p a r s e d c o d e [ : − 1 ]
             # [ shuyanzh ] , don ' t s u p p o r t a c t i o n a r g s and kwargs now
             e x e c u t e p l a y w r i g h t c l i c k ( l o c a t o r c o d e = l o c a t o r c o d e , page=page )
      e l s e :
             r a i s e V a l u e E r r o r ( " No p r o p e r l o c a t o r found f o r c l i c k a c t i o n " )
c a s e ActionTypes . TYPE :
      i f a c t i o n [ " e l e m e n t i d " ] :
             i f n o t o b s e r a t i o n p r o c e s s o r . e l e m e n t i s v i s i b l e ( page , e l e m e n t i d ) :
                    p r e s s e n t e r = True i f i d 2 k e y [ a c t i o n [ " t e x t " ] [ − 1 ] ] == "\n " e l s e F a l s e
                   node = o b s e r a t i o n p r o c e s s o r . g e t n o d e i n f o b y e l e m e n t i d ( i n t ( e l e m e n t i d ) )
                    t r y :
                          i f p r e s s e n t e r :
                                 page . g e t b y r o l e ( node . r o l e , name=node . name , e x a c t =True ) . f i l l ( " " . j o i n ( [ i d 2 k e y [ i d x ]
                                            f o r i d x i n a c t i o n [ " t e x t " ] [ : − 1 ] ] ) )
                                 ti me . s l e e p ( 1 )
                                 page . keyboard . p r e s s ( " E n t e r " )
                          e l s e :
                                 page . g e t b y r o l e ( node . r o l e , name=node . name , e x a c t =True ) . f i l l ( " " . j o i n ( [ i d 2 k e y [ i d x ]
                                            f o r i d x i n a c t i o n [ " t e x t " ] ] ) )
                    e x c e p t :
                          i f p r e s s e n t e r :
                                 page . g e t b y r o l e ( node . r o l e , name=node . name ) . f i l l ( " " . j o i n ( [ i d 2 k e y [ i d x ] f o r i d x i n
                                          a c t i o n [ " t e x t " ] [ : − 1 ] ] ) )
                                 ti me . s l e e p ( 1 )
                                 page . keyboard . p r e s s ( " E n t e r " )
                          e l s e :
                                 page . g e t b y r o l e ( node . r o l e , name=node . name ) . f i l l ( " " . j o i n ( [ i d 2 k e y [ i d x ] f o r i d x i n
                                          a c t i o n [ " t e x t " ] ] ) )
             e l s e :
                    e l e m e n t i d = a c t i o n [ " e l e m e n t i d " ]
                    e l e m e n t c e n t e r = o b s e r a t i o n p r o c e s s o r . g e t e l e m e n t c e n t e r ( e l e m e n t i d , page ) # t y p e : i g n o r e
                             [ a t t r − d e f i n e d ]
                    e x e c u t e m o u s e c l i c k ( e l e m e n t c e n t e r [ 0 ] , e l e m e n t c e n t e r [ 1 ] , page )
                   page . keyboard . p r e s s ( " C o n t r o l +A" )
                    f o r i n r a n g e ( 1 ) :
                          # page . keyboard . p r e s s ( " D e l e t e " )
                          page . keyboard . p r e s s ( " Backspace " )
                    e x e c u t e t y p e ( a c t i o n [ " t e x t " ] , page )
      e l i f a c t i o n [ " e l e m e n t r o l e " ] and a c t i o n [ " element name " ] :
             e l e m e n t r o l e = i n t ( a c t i o n [ " e l e m e n t r o l e " ] )
             element name = a c t i o n [ " element name " ]
             n t h = a c t i o n [ " n t h " ]
             e x e c u t e f o c u s ( e l e m e n t r o l e , element name , nth , page )
             e x e c u t e t y p e ( a c t i o n [ " t e x t " ] , page )
      e l i f a c t i o n [ " pw code " ] :
             p a r s e d c o d e = p a r s e p l a y w r i g h t c o d e ( a c t i o n [ " pw code " ] )
             l o c a t o r c o d e = p a r s e d c o d e [ : − 1 ]
             t e x t = p a r s e d c o d e [ − 1 ] [ " arguments " ] [ 0 ]
             # [ shuyanzh ] , don ' t s u p p o r t a c t i o n a r g s and kwargs now
             e x e c u t e p l a y w r i g h t t y p e (
                    t e x t = t e x t , l o c a t o r c o d e = l o c a t o r c o d e , page=page
             )
      e l s e :
```

```
r a i s e N o t I m p l e m e n t e d E r r o r (
      "No p r o p e r l o c a t o r found f o r t y p e a c t i o n "
)
```

# <span id="page-30-0"></span>G AGENT PROMPTS

## G.1 AGENTOCCAM

## The general prompt template:

## • With planning

You a r e an AI a s s i s t a n t p e r f o r m i n g t a s k s on a web browser . You w i l l be p r o v i d e d w ith t a s k o b j e c t i v e , c u r r e n t s t e p , web page o b s e r v a t i o n s , p r e v i o u s p l a n s , and i n t e r a c t i o n h i s t o r y . You need t o i s s u e an a c t i o n f o r t h i s s t e p .

```
G e n e r a t e t h e r e s p o n s e i n t h e f o l l o w i n g f o r m a t :
{ o u t p u t s p e c i f i c a t i o n s }
```

You a r e ONLY a l l o w e d t o use t h e f o l l o w i n g a c t i o n commands . S t r i c t l y a d h e r e s t o t h e g i v e n f o r m a t . Only i s s u e one s i n g l e a c t i o n .

I f you t h i n k you s h o u l d r e f i n e t h e plan , use t h e f o l l o w i n g a c t i o n s :

{ p l a n n i n g a c t i o n s p e c i f i c a t i o n s }

Otherwise , use t h e f o l l o w i n g a c t i o n s : { n a v i g a t i o n a c t i o n s p e c i f i c a t i o n s }

## • Without planning

You a r e an AI a s s i s t a n t p e r f o r m i n g t a s k s on a web browser . You w i l l be p r o v i d e d w ith t a s k o b j e c t i v e , c u r r e n t s t e p , web page o b s e r v a t i o n s , and o t h e r r e l e v a n t i n f o r m a t i o n . You need t o i s s u e an a c t i o n f o r t h i s s t e p .

```
G e n e r a t e t h e r e s p o n s e i n t h e f o l l o w i n g f o r m a t :
{ o u t p u t s p e c i f i c a t i o n s }
```

You a r e ONLY a l l o w e d t o use t h e f o l l o w i n g a c t i o n commands . S t r i c t l y a d h e r e s t o t h e g i v e n f o r m a t . Only i s s u e one s i n g l e a c t i o n .

{ n a v i g a t i o n a c t i o n s p e c i f i c a t i o n s }

## Output specifications:

I n t e r a c t i o n h i s t o r y summary : Emphasize a l l i m p o r t a n t d e t a i l s i n t h e INTERACTION HISTORY s e c t i o n . O b s e r v a t i o n d e s c r i p t i o n : D e s c r i b e i n f o r m a t i o n i n t h e CURRENT OBSERVATION s e c t i o n . Emphasize e l e m e n t s and f e a t u r e s t h a t a r e r e l e v a n t or p o t e n t i a l l y h e l p f u l f o r f u l f i l l i n g t h e o b j e c t i v e i n d e t a i l . Reason : P r o v i d e your r a t i o n a l e f o r p r o p o s i n g t h e s u b s e q u e n t a c t i o n commands h e r e .

A c t i o n : S e l e c t your a c t i o n h e r e . O b s e r v a t i o n H i g h l i g h t : L i s t t h e n u m e r i c a l i d s of e l e m e n t s on t h e c u r r e n t webpage based on which you would i s s u e your a c t i o n . Also i n c l u d e e l e m e n t s on t h e c u r r e n t webpage you would a t t e n d t o i f you f a i l i n t h e f u t u r e and have t o r e s t o r e t o t h i s s t e p . Don ' t i n c l u d e e l e m e n t s from t h e p r e v i o u s pages . S e l e c t e l e m e n t s a t a h i g h e r h i e r a r c h i c a l l e v e l i f most t h e i r c h i l d r e n nodes a r e c o n s i d e r e d c r u c i a l . S o r t by r e l e v a n c e and p o t e n t i a l v a l u e s from hig h t o low , and s e p a r a t e t h e i d s wi th commas . E . g . , '1321 , 52 , 756 , 8 3 8 ' .

## Action space specifications:

## • Planning action specifications

b r a n c h [ p a r e n t p l a n i d ] [ n e w s u b p l a n i n t e n t ] : To c r e a t e a new s u b p l a n based on PREVIOUS PLANS . Ensure t h e new s u b p l a n i s c o n n e c t e d t o t h e a p p r o p r i a t e p a r e n t p l a n by u s i n g i t s ID . E . g . , ' b r a n c h [ 1 2 ] [ N a v i g a t e t o t h e ' I s s u e " page t o check a l l t h e i s s u e s . ] '

prune [ r e s u m e p l a n i d ] [ r e a s o n ] : To r e t u r n t o a p r e v i o u s p l a n s t a t e when t h e c u r r e n t p l a n i s deemed i m p r a c t i c a l . E n t e r t h e ID of t h e p l a n s t a t e you want t o resume . E . g . , ' prune [ 5 ] [ The c u r r e n t page l a c k s i t e m s ' b l a c k s p e a k e r , ' prompting a r e t u r n t o t h e i n i t i a l page t o r e s t a r t t h e it em s e a r c h . ] '

## • Navigation action specifications

c l i c k [ i d ] : To c l i c k on an e l e m e n t wit h i t s n u m e r i c a l ID on t h e webpage . E . g . , ' c l i c k [ 7 ] ' I f c l i c k i n g on a s p e c i f i c e l e m e n t doesn ' t t r i g g e r t h e t r a n s i t i o n t o your d e s i r e d web s t a t e , t h i s i s due t o t h e element ' s l a c k of i n t e r a c t i v i t y or GUI v i s i b i l i t y . In such c a s e s , move on t o i n t e r a c t wi th OTHER s i m i l a r or r e l e v a n t e l e m e n t s INSTEAD .

t y p e [ i d ] [ c o n t e n t ] [ p r e s s e n t e r a f t e r = 0 | 1 ] : To t y p e c o n t e n t i n t o a f i e l d wit h a s p e c i f i c ID . By d e f a u l t , t h e ' Enter ' key i s p r e s s e d a f t e r t y p i n g u n l e s s ' p r e s s e n t e r a f t e r ' i s s e t t o 0 . E . g . , ' t y p e [ 1 5 ] [ C a r n e g i e Mellon U n i v e r s i t y ] [ 1 ] ' I f you can ' t f i n d what you ' r e l o o k i n g f o r on your f i r s t a t t e m p t , c o n s i d e r r e f i n i n g your s e a r c h keywords by b r e a k i n g them down or t r y i n g r e l a t e d t e r m s .

go back : To r e t u r n t o t h e p r e v i o u s l y viewed page .

n o t e [ c o n t e n t ] : To t a k e n o t e of a l l i m p o r t a n t i n f o w. r . t . c o m p l e t i n g t h e t a s k t o e n a b l e r e v i e w i n g i t l a t e r . E . g . , ' n o t e [ Spent \$10 on 4 / 1 / 2 0 2 4 ] '

s t o p [ answer ] : To s t o p i n t e r a c t i o n and r e t u r n r e s p o n s e . P r e s e n t your answer w i t h i n t h e b r a c k e t s . I f t h e t a s k doesn ' t r e q u i r e a t e x t u a l answer or a p p e a r s i n s u r m o u n t a b l e , i n d i c a t e 'N/A' and a d d i t i o n a l r e a s o n s and a l l r e l e v a n t i n f o r m a t i o n you g a t h e r as t h e answer . E . g . , ' s t o p [5 h 47 min ] ' go home : To r e t u r n t o t h e homepage where you can f i n d o t h e r w e b s i t e s .

## Observation space example:

```
RootWebArea [ 1 ] ' Dashboard / Magento Admin '
      l i n k [ 1 7 8 ] ' Magento Admin Panel '
      menubar [ 8 5 ]
                  l i n k [ 8 7 ] 'DASHBOARD'
                  l i n k [ 9 0 ] 'SALES'
                  l i n k [ 9 6 ] 'CATALOG'
                  l i n k [ 1 0 2 ] 'CUSTOMERS'
                  l i n k [ 1 0 8 ] 'MARKETING'
                  l i n k [ 1 1 4 ] 'CONTENT'
                  l i n k [ 1 2 0 ] 'REPORTS'
                  l i n k [ 1 3 8 ] 'STORES'
                  l i n k [ 1 4 4 ] 'SYSTEM'
                  l i n k [ 1 5 0 ] 'FIND PARTNERS & EXTENSIONS'
      h e a d i n g ' Dashboard '
      l i n k [ 2 5 4 ] ' admin '
      l i n k [ 2 5 6 ]
      t e x t b o x [ 8 9 4 ] [ r e q u i r e d : F a l s e ]
     main
                  t e x t ' Scope : '
                  b u t t o n [ 2 6 2 ] ' A l l S t o r e Views '
                  l i n k [ 2 6 5 ] ' What i s t h i s ? '
                  b u t t o n [ 2 4 0 ] ' Reload Data '
                 HeaderAsNonLandmark [ 8 9 8 ] ' Advanced R e p o r t i n g '
                  t e x t " Gain new i n s i g h t s and t a k e command of your b u s i n e s s ' performance , u s i n g our dynamic
                          p r o d u c t , o r d e r , . . .
                  l i n k [ 9 0 2 ] 'Go t o Advanced R e p o r t i n g '
                  t e x t ' C h a r t i s d i s a b l e d . To e n a b l e t h e c h a r t , c l i c k '
                  l i n k [ 9 0 6 ] ' here '
                  t e x t ' Revenue '
                  t e x t ' Tax '
                  t e x t ' Shipping '
                  t e x t ' Q u a n t i t y '
                  t a b l i s t [ 5 7 ]
                              t a b [ 5 9 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . T his t a b c o n t a i n s i n v a l i d d a t a
                                          l i n k [ 6 7 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . Th is t a b c o n t a i n s
                                                  i n v a l i d d a t a . . .
                                                     t e x t ' The i n f o r m a t i o n i n t h i s t a b has been changed . '
                                                     t e x t ' T hi s t a b c o n t a i n s i n v a l i d d a t a . P l e a s e r e s o l v e t h i s b e f o r e
                                                              s a v i n g . '
                                                     t e x t ' Loading . . . '
                              t a b [ 6 1 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . T his t a b c o n t a i n s i n v a l i d d a t a
                                          l i n k [ 6 9 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . Th is t a b c o n t a i n s
                                                  i n v a l i d d a t a . . .
                                                     t e x t ' The i n f o r m a t i o n i n t h i s t a b has been changed . '
                                                     t e x t ' T hi s t a b c o n t a i n s i n v a l i d d a t a . P l e a s e r e s o l v e t h i s b e f o r e
                                                              s a v i n g . '
                                                     t e x t ' Loading . . . '
                              t a b [ 6 3 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . T his t a b c o n t a i n s i n v a l i d d a t a
                                          l i n k [ 7 1 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . Th is t a b c o n t a i n s
                                                  i n v a l i d d a t a . . .
                                                     t e x t ' The i n f o r m a t i o n i n t h i s t a b has been changed . '
                                                     t e x t ' T hi s t a b c o n t a i n s i n v a l i d d a t a . P l e a s e r e s o l v e t h i s b e f o r e
                                                              s a v i n g . '
                                                     t e x t ' Loading . . . '
                              t a b [ 6 5 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . T his t a b c o n t a i n s i n v a l i d d a t a
                                          l i n k [ 7 3 ] ' The i n f o r m a t i o n i n t h i s t a b has been changed . Th is t a b c o n t a i n s
                                                  i n v a l i d d a t a . . .
                                                     t e x t ' The i n f o r m a t i o n i n t h i s t a b has been changed . '
                                                     t e x t ' T hi s t a b c o n t a i n s i n v a l i d d a t a . P l e a s e r e s o l v e t h i s b e f o r e
                                                              s a v i n g . '
                                                     t e x t ' Loading . . . '
                  t a b p a n e l ' The i n f o r m a t i o n i n t h i s t a b has been changed . Th is t a b c o n t a i n s i n v a l i d d a t a . . .
                              t a b l e
                                         row '| P r o d u c t | P r i c e | Q u a n t i t y | '
                                         row '| −−− | −−− | −−− | '
                                         row '| S p r i t e S t a s i s B a l l 65 cm | 2 7 . 0 0 | 6 | '
                                         row '| Quest Lumaflex Band | 1 9 . 0 0 | 6 | '
                                         row '| S p r i t e Yoga S t r a p 6 f o o t | 1 4 . 0 0 | 6 | '
                                         row '| S p r i t e S t a s i s B a l l 55 cm | 2 3 . 0 0 | 5 | '
                                         row '| O v e r n i g h t D u f f l e | 4 5 . 0 0 | 5 | '
                  t e x t ' L i f e t i m e S a l e s '
                  t e x t ' Average Order '
                  t e x t ' L a s t Orders '
                  t a b l e
                             row '| Customer | I t e m s | T o t a l | '
                             row '| −−− | −−− | −−− | '
                             row '| Sarah M i l l e r | 5 | 194.40 | '
                             row '| Grace Nguyen | 4 | 190.00 | '
                             row '| Matt Baker | 3 | 151.40 | '
                             row '| L i l y P o t t e r | 4 | 188.20 | '
                             row '| Ava Brown | 2 | 8 3 . 4 0 | '
                  t e x t ' L a s t S e a r c h Terms '
                  t a b l e
                             row '| S e a r c h Term | R e s u l t s | Uses | '
                             row '| −−− | −−− | −−− | '
                             row '| t a n k s | 23 | 1 | '
```

```
row '| n i k e | 0 | 3 | '
                      row '| J o u s t Bag | 10 | 4 | '
                      row '| h o l l i s t e r | 1 | 19 | '
                      row '| Antonia Racer Tank | 23 | 2 | '
           t e x t ' Top S e a r c h Terms '
           t a b l e
                      row '| S e a r c h Term | R e s u l t s | Uses | '
                      row '| −−− | −−− | −−− | '
                      row '| h o l l i s t e r | 1 | 19 | '
                      row '| J o u s t Bag | 10 | 4 | '
                      row '| Antonia Racer Tank | 23 | 2 | '
                      row '| t a n k s | 23 | 1 | '
                      row '| WP10 | 1 | 1 | '
c o n t e n t i n f o
           l i n k [ 2 4 4 ]
           t e x t ' C o p y r i g h t 2024 Magento Commerce I n c . A l l r i g h t s r e s e r v e d . '
           t e x t ' v e r . 2 . 4 . 6 '
           l i n k [ 2 4 7 ] ' P r i v a c y P o l i c y '
           l i n k [ 2 4 9 ] ' Account A c t i v i t y '
           l i n k [ 2 5 1 ] ' R e p o r t an I s s u e '
```

## G.2 JUDGE USED IN AGENTOCCAM + JUDGE EXPERIMENTS

## The general prompt template:

```
You a r e a s e a s o n e d web n a v i g a t o r . You now a s s e s s t h e v a l u e and r i s k of s e r v e r a l web n a v i g a t i o n a c t i o n s based
        on t h e o b j e c t i v e , t h e p r e v i o u s i n t e r a c t i o n h i s t o r y and t h e web ' s c u r r e n t s t a t e . Then , you s e l e c t t h e
        a c t i o n w ith t h e most v a l u e and l e a s t r i s k w it h which you would e a r n t h e maximum o b j e c t i v e f u l f i l l m e n t
        reward i n t h e f u t u r e .
Adhere t o t h e f o l l o w i n g o u t p u t f o r m a t :
{ o u t p u t s p e c i f i c a t i o n s }
Note t h a t ' branch ' and ' prune ' a r e p l a n n i n g a c t i o n s t h a t w i l l modify t h e PREVIOUS PLAN s e c t i o n and won ' t
         i n t e r a c t w ith t h e web e n v i r o n m e n t .
```

## Output specifications:

```
Pl an p r o g r e s s a s s e s s m e n t : Review c r i t i c a l l y why t h e p l a n s have n o t been f u l f i l l e d or t h e o b j e c t i v e a c h i e v e d .
         J u s t i f y your a s s e s s m e n t wi th d e t a i l e d e v i d e n c e drawn from t h e o b j e c t i v e , o b s e r v a t i o n s , and a c t i o n s t a k e n
         . I t e m i z e t h e a s s e s s m e n t u s i n g t h i s f o r m a t : '− p l a n [{ p l a n i d }]\n\t [{ s t e p i d s t a k e n f o r t h i s m i l e s t o n e }]
          [{ c o n c r e t e p r o o f f r o m o b s e r v a t i o n }] [{ w h y m i l e s t o n e a n o t s u c c e s s f u l }]\n\t [{
         s t e p i d s t a k e n f o r t h i s m i l e s t o n e }] [{ c o n c r e t e p r o o f f r o m o b s e r v a t i o n }] [{ w h y m i l e s t o n e b n o t s u c c e s s f u l
        }]\n\t . . . ' .
A c t i o n a s s e s s m e n t : A s s e s s t h e v a l u e and r i s k of each a c t i o n . C o n s i d e r b ot h t h e b e s t − c a s e and worst − c a s e
        outcomes r e s u l t i n g from i t s i m p l e m e n t a t i o n . I t e m i z e t h e a s s e s s m e n t u s i n g t h i s f o r m a t : '− a c t i o n [
         a c t i o n i d ] : [ a c t i o n value , i n c l u d i n g b u t n o t l i m i t e d t o what outcomes you can e x p e c t by e x e c u t i n g t h e
        a c t i o n , or whether t h e n o t e i s of t h e most c o r r e c t and co m pr e h en s iv e c o n t e n t ] [ a c t i o n r i s k , i n c l u d i n g
        b u t n o t l i m i t e d t o whether t h e n o t e / s t o p c o n t e n t i s c o r r e c t , and whether you can g a t h e r more i n f o r m a t i o n
          by c o n t i n u i n g p l a y i n g r a t h e r t h a n e n d i n g t h e t r i a l ] [{ b e s t c a s e }] [{ w o r s t c a s e }] ' .
A c t i o n s e l e c t i o n : L i s t t h e n u m e r i c a l i d of your s e l e c t e d a c t i o n h e r e . You can o nl y choose one a c t i o n . E . g . ,
         ' 1 ' .
```

# H FUTURE DIRECTION: TRAINING EVOLVING WEB AGENTS

Our current alignment of the action and observation space is designed and deployed based on human heuristics under the assumption that the base models are not trainable. This approach excludes certain useful web actions or web element formatting that could potentially be learned with minimal examples, rather than being mastered through training AGENTOCCAM. For instance, incorporating the scroll action could significantly reduce the observation's volume and better align with the design of real web environments, e.g., many shopping websites are designed to load more products only when a user scrolls down. Considering that the agent can record interaction traces to determine whether to scroll up or down, it is likely that an LLM could learn this action without extensive training. By lifting the restriction on the non-trainability of LLMs, incorporating such design considerations might enhance the performance of web agents and reduce operational costs.

Furthermore, given the evolving nature of web layouts and human needs, developing adaptable agents is essential. Their autonomy is not only reflected by the ability to adapt to ever-so-updating web tasks, but also by the creation of more sophisticated observation and action mappings (functions f and g) as tools to get them more familiar with the web environments regarding perception and action grounding, rather than relying on human heuristics, just as what has been done in this work. Such agents would be able to autonomously refine their skills and improve system performance.