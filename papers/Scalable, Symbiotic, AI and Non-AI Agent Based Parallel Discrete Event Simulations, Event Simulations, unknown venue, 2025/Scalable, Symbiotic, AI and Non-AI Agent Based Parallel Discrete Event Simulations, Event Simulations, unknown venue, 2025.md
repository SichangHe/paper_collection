                                         Scalable, Symbiotic, AI and Non-AI Agent Based Parallel Discrete
                                                                 Event Simulations
                                                          Atanu Barai                                Stephan Eidenbenz                            Nandakishore Santhi
                                               Los Alamos National Laboratory                  Los Alamos National Laboratory                 Los Alamos National Laboratory
                                                    Los Alamos, NM, USA                             Los Alamos, NM, USA                            Los Alamos, NM, USA
                                                      abarai@lanl.gov                                eidenben@lanl.gov                               nsanthi@lanl.gov

                                         Abstract                                                                       The growing complexity of pressing problems in science and other
                                         To fully leverage the potential of artificial intelligence (AI) systems    domains demands solutions that not only leverage the strengths of
                                         in a trustworthy manner, it is often desirable to couple multiple          multiple AI systems but also of non-AI systems, all coupled together.
                                         AI and non-AI systems together seamlessly for constraining and             While AI agents excel in tasks such as repetitive data processing, pat-
arXiv:2505.23846v1 [cs.CL] 28 May 2025




                                         ensuring correctness of the output. This paper introduces a novel          tern recognition, content generation, and adaptive decision making,
                                         parallel discrete event simulation (PDES) based symbiotic methodol-        non-AI agents such as human experts, and rule-based determinis-
                                         ogy to combine multiple AI and non-AI agents in a causal, rule-based       tic/Monte Carlo systems, often possess domain-specific knowledge,
                                         way. Our approach tightly integrates the concept of passage of time,       practical constraints, and ethical/societal considerations that the AI
                                         with each agent considered as an entity in the PDES framework and          systems can’t yet fully encapsulate. Thus their collaboration can
                                         responding to prior requests from other agents. Such a coupling            lead to more versatile, resilient, and context-aware systems capable
                                         mechanism enables the agents to work in a co-operative environ-            of addressing a broad spectrum of challenges by pooling knowledge,
                                         ment towards a common goal while many tasks run in parallel                sharing information, and coordinating actions that would be be-
                                         throughout the simulation. It further enables setting up boundaries        yond the reach of any individual agent. Thus, these types of systems
                                         to the outputs of the AI agents by applying necessary dynamic con-         promise enhanced problem solving capabilities and greater adaptabil-
                                         straints using non-AI agents while allowing for scalability through        ity to complex environments including autonomous transportation,
                                         deployment of hundreds of such agents in a larger compute clus-            drug discovery, education etc.
                                         ter. Distributing smaller AI agents can potentially enable extremely           However, developing a robust coupling methodology to enable
                                         scalable simulations in the future, while also circumventing local         multi-agent AI systems is challenging due to several factors. Issues
                                         memory bottlenecks for model parameter storage.                            such as communication methodologies, timing/coordination among
                                            Within a parallel discrete event simulation involving both AI and       the agents, conflict resolution, handling biases, security consider-
                                         non-AI agents, we break down the problem at hand into structured           ations, and most importantly extreme scalability to handle a very
                                         steps, when necessary, providing a set of multiple choices to the AI       large number of agents must be addressed to ensure an effective
                                         agents, and then progressively solve these steps towards a final goal.     collaboration strategy.
                                         At each step, the non-AI agents act as unbiased auditors, examining            This paper introduces a robust parallel discrete event simulation
                                         and verifying each action by the AI agents so that certain rules of        (PDES) based methodology to couple AI and non-AI agents in a
                                         engagement are followed. We evaluate our approach by solving four          rule-based way into cohesive multi-agent systems. Using PDES for
                                         problems from four different domains and comparing the results with        coupling inherently addresses many of the problems mentioned
                                         those from AI models alone. Our results show that by adopting the          previously. This strategy is capable of solving a problem by breaking
                                         coupling methodology, we can achieve greater accuracy in solving           it into many smaller, more manageable steps, involving both AI and
                                         problems from various domains where the AI models struggle to              non-AI agents to solve each stage in a causal event-driven manner.
                                         solve the problems solely by themselves. Results show that overall         We use the open-source Simian [56] PDES engine to couple the
                                         accuracy of our approach is 68% where as the accuracy of vanilla           agents. Simian is simple and easy to use, yet powerful enough to
                                         models is less than 23%.                                                   support the deployment of thousands of such agents through a user-
                                                                                                                    transparent parallelization mechanism which effectively uses the
                                         Keywords                                                                   message passing interface (MPI) library. Each simulation agent is
                                                                                                                    implemented as an entity object of the Simian engine and is assigned
                                         AI, PDES, AI/non-AI Coupling, Automated Reasoning, Symbiotic
                                                                                                                    to one of the MPI ranks for parallel processing. The entities serve
                                         Simulations
                                                                                                                    requests through a reqService process which schedules a future event
                                                                                                                    at the corresponding entity to be processed by a user-defined event
                                         1   Introduction                                                           handler.
                                         Artificial intelligence (AI) is revolutionizing countless industries and       The ability to couple and deploy hundreds of AI and non-AI agents
                                         enabling new discoveries in every field including science, energy,         also addresses another contemporary challenge faced by the AI com-
                                         economics, and security thus transforming how we innovate. AI              munity. Today’s AI models utilize the extremely parallel computing
                                         systems, when specifically trained on various topics, are capable          power of graphics processing units (GPUs). With the introduction
                                         of tasks once thought to be possible only by humans. However, a            and rapid adoption of large language models (LLMs) [12, 70] such as
                                         majority of AI models today run in isolation, unable to fully harness      Llama3 [25] and GPT4 [50], computing requirements and demand
                                         the potential of collective knowledge and parallel synergy, thus           for powerful GPUs have skyrocketed [63], since these models are
                                         hindering further innovation by achieving shared objectives.               trained on large amounts of web data. Running local inference on
ArXiv Preprint, 2025, USA                                                                      Atanu Barai, Stephan Eidenbenz, and Nandakishore Santhi


these models can be costly and out of reach for a vast majority of        of integrating AI and non-AI entities [1, 39, 62] including multi-agent
researchers due to the requirement for very large compute and mem-        deep-reinforcement learning [36].
ory throughputs. By using our PDES based methodology, we are                  Baratta et al. [3] showed how AI-based robots can collaborate with
able to deploy thousands of smaller AI agents coupled with many           human agents in industrial settings through continuous learning of
non-AI agents to work together to solve a particular problem.             human behavior. Ming et al. [48] explored a framework for bridging
   To demonstrate our approach more thoroughly, we solve four             AI based adaptive algorithms with deterministic non-AI control
common problems from geometry, combinatorics, arithmetics and,            software within the context of autonomous vehicles.
graph-theory by coupling small language model (SLM) based AI                  In terms of language models, the coupling approaches vary de-
agent with non-AI agents, where a small AI agent by itself is unable      pending on model architecture and the underlying learning settings.
to solve these problems correctly. We consider models with 16B            Shen et al. [59] proposed a model collaboration approach where
parameters or less as SLM, while anything larger is considered an         off-the-shelf models learn to choose among themselves which one
LLM. This is based on current technology considerations, where            will handle what portion of all the input tokens. Tokens are gener-
16B or lower models can be accommodated on low to medium scale            ated by a model and then the model-choice decision is represented
consumer-grade GPUs from major vendors, albeit by employing               as a latent variable. In another approach named Mixture of Ex-
suitable parameter quantization strategies. The general symbiotic         perts [21, 40, 58, 74, 81] all experts are trained simultaneously on the
approach to solving the problems is the following:                        same/similar data. These experts are sub-networks of the mixture
    (1) We break down the problem into multiple smaller steps,            that can’t be used standalone where the feed-forward layers in a
    (2) SLM agents are asked in parallel to solve a step,                 transformer is decomposed into modules called experts. Similarly
    (3) Constraints in the solution space are applied by providing        Proxy Tuning [44] and PATHGOOSE [49] also require same/similar
        SLM agents with some pre-defined options to choose from,          training datasets and/or fine-tuning methods for all experts to bring
    (4) Non-SLM agents collate and then inspect SLM responses and         out the best performance.
        provide feedback in the form of further prompts to the SLM            Researchers also proposed various prompt-based methods to en-
        agents,                                                           hance an LLM’s reasoning ability. These methods focus on tuning the
    (5) The whole process runs under the umbrella of a parallel dis-      instructions detailing context, inputs, or examples. Approaches in
        crete event simulation.                                           this area include few-shot prompting [14] where in-context learning
                                                                          is enabled by providing demonstrations in the prompt. In chain-
    These problems sometimes can be solved by a large language            of-thought [42, 71] paradigm, one activates intermediate reasoning
model (LLM) acting on its own. But most large models require GPU          steps for providing a response which promotes a more complex
acceleration with very large local memory to run which is in turn         reasoning capability. Meta prompting [77] tries to improve language
very expensive and often scarce. In contrast, in our approach, we         model performance by focusing on format and syntax of the prob-
use SLMs that require far less powerful GPUs with low local mem-          lem at hand, and responses are crafted over specific content details.
ory requirements, and can even be accelerated on GPUs/custom-             Syntax is used as a guiding template for the expected response
accelerators/NPUs integrated on the CPU-fabric. On the other hand,        or solution. Other methods that aim at improving inference per-
our method can optionally couple together multiple SLMs to get            formance include problem decomposition or chaining [35, 41, 80],
more accurate responses [59]. Our approach also has a simple ver-         abstraction [78], planning and programming [16, 24, 79] or self-
ification step built in as the non-AI agent checks individual SLM         verification [33]. Similarly, tree-search approaches like Monte-Carlo
answers, thus making the entire system much more trustworthy              Tree Search also break the task into smaller sub-tasks and improve
than a pure SLM/LLM approach.                                             the performance by sampling simpler, individual, and intermediate
    The rest of the paper is organized as follows: Section 2 summarizes   reasoning steps [52, 75, 76] but employs a structured way in doing
the relevant related works and sets this work apart from those.           so. In reflection [60, 68], further improvement in next response is
Section 3 covers the necessary background concepts used in this           achieved by reinforcing language agents through linguistic feed-
paper. Section 4 provides an overview of our coupling methodology         back. The linguistic feedback which is essentially a reward score for
and shows how one can solve some common problems encountered              previous response, also referred to as self-reflection is provided as
in different domains by incorporating both AI and non-AI agents           context to a language model for improving further responses.
through PDES. Section 5 goes over some experimental results. It               In terms of using LLMx in simulation, Diamantopoulos et al. [23]
compares the outcome of our coupled AI system with a traditional          proposed using LLM in blockchain simulation where they proposed
stand-alone AI system. Finally, Section 6 concludes the paper.            using LLMs for dynamic simulation scenario generation and mali-
                                                                          cious code modeling. Liu et al. [45] proposed using LLMs in trans-
2    Related Works                                                        portation simulation. They proposed leveraging LLMs to represent
Coupling several models trained on varied topics into multi-agent         individual units in the transportation system such as a traveler or
systems has been an active field of research to improve the overall       driver. Giabbanelli [34] and Wu et al. [73] also proposed smart agent
quality of AI model responses. The interplay of multiple agents           based modeling and simulation methodologies where the LLMs are
require seamless integration of heterogenous agents bringing unique       leveraged in agent-based modeling.
challenges regarding communication, coordination and interaction-             In our work, we aim to couple off-the-shelf models in a rule-
rules. Wooldridge discussed various aspects of multi-agent systems        based way to work collaboratively towards common solution by
including architectures and applications [72]. Researchers have also      breaking down a problem into simpler sub-tasks. It also inherently
extensively studied those challenges, opportunities and limitations       enables deployment of hundreds of agents through MPI support.
Scalable, Symbiotic, AI and Non-AI Agent Based Parallel Discrete Event Simulations                                                     ArXiv Preprint, 2025, USA


Decomposing the problem also enables exploring new PDES-based                        language recognition and translation [38, 43] but still had problems
algorithms to solve a particular problem using less powerful AI                      like vanishing gradient [9] and inability to capture very long-range
models.                                                                              relationships among the words. Researchers adopted long short-
                                                                                     term memory (LSTM) [37] and gated recurrent units (GRUs) [17] to
3     Background                                                                     extend RNN based models to address these issues but they were still
In this section we discuss some concepts used in the paper.                          limited in handling very large sequences of data.
                                                                                        The introduction of the self-attention based transformer architec-
                                                                                     ture [67] for language models revolutionized this field by enabling
3.1     Parallel Discrete Event Simulation
                                                                                     training on very large web-scale unstructured data in parallel and
Parallel discrete event simulation (PDES) refers to the execution of a               capturing long-rage relationships in the text. Built on transformer
single discrete event simulation program on multiple processors [28]                 architectures, large language models like BERT [22] and GPT [54]
so that the simulation runs more efficiently in parallel than tradi-                 set new standards for solving a wide range of NLP tasks. These mod-
tional sequential simulation. In a discrete event simulation (DES),                  els learn broad language representations and can be fine-tuned for
a simulated system is decomposed into smaller independent sub-                       specific tasks with smaller, labeled datasets. Because these models
systems, and it is assumed that changes in system state occur at                     are capable of in-context learning, they can generate coherent and
discrete points of simulated time. In a popular implementation style,                contextually relevant responses making them suitable for interactive
each subsystem would then maintain its own event list with times-                    applications in diverse scenarios [14].are symbiotically edusing the
tamps, containing the events that are scheduled to occur within that                 Simian PDES semantics at runtime
subsystem in the future.
   The occurrence of events (execution of subsystems) triggers a set                                                Simian Entity
of events which may include performing calculations, updating state
variables of the simulation and generating new events. This causes
                                                                                                     AI Agents                        Non-AI Agent
the simulation to advance. The simulation runs until all events are
processed. In sequential DES, timestamps denote when the event will
                                                                                                   Sub-task 1                          Sub-task 1
occur changing the system. The main loop of the simulation engine
                                                                                                                       Simian
repeatedly processes the event with smallest timestamp and removes                                                      PDES
the event from event list [28]. But if an event with larger timestamp                                                  Engine
(Et-large ) is executed before a smaller one (Et-small ), (Et-large ) might
                                                                                                   Sub-task n                          Sub-task n
change a state variable used by (Et-small ) thus making a future event
affecting past event. This error is called causality error.
   PDES tries to execute the events in parallel avoiding causality
error (in conservative scheme) or detecting causality error for later                                        Interact with the PDES engine to
recovery (in optimistic scheme) [26, 28, 66]. This parallel execution                                        schedule tasks using reqService method
along with clever problem decomposition enables PDES to run very
large-scale simulations on large supercomputers [4, 8, 29, 51, 55].
                                                                                     Figure 1: AI / non-AI agents are coupled using the Simian
                                                                                     PDES semantics at runtime.
3.2     Language Models
Language models are a class of generative AI systems designed to
understand, synthesize, and manipulate human language [15]. They
are built using techniques from natural language processing (NLP), a
                                                                                     4     Methodology
subset of machine learning models and trained on text data to learn                  This section lays out in detail various steps of our proposed approach
the statistical relationship between words or phrases [18, 22, 30, 43].              to couple multiple AI and non-AI agents in a rule-based way. We first
These models are capable of predicting and generating new text                       explain the coupling technique in subsection 4.1 followed by how
sequences based on given input text prompts – although they face                     we formulate a problem into the framework of parallel discrete event
many challenges such as difficulty in understanding complex lan-                     simulations after applying constraints in subsection 4.2. Finally, we
guage, unseen words, structured applications such as mathematics,                    show several case studies from four different domains to demonstrate
logic, reasoning etc.                                                                the effectiveness of the coupling technique in subsection 4.3.
   Early language models such as n-gram [13] (e.g. bigram, trigram)
were based on simple statistical modeling techniques in predicting                   4.1    Coupling Technique
the probabilities of next word based on preceding words. Although                    We use the open-source Simian [56] PDES engine designed for large-
these models were capable of question answering, text analysis,                      scale computing environments to couple multiple AI and non-AI
summarizing and information retrieval [6, 10, 20, 46], these models                  agents. We use the Python implementation of Simian for rapid proto-
were limited in understanding context from large text.                               typing of our proposed coupling methodology because it works very
   Later, with the rise of deep learning and GPGPUs, researchers                     well with mainstream LLM libraries such as TensorFlow, PyTorch,
proposed recurrent neural network (RNN) based language models                        llama.cpp, and Transformers. Simian uses entities as objects that con-
that were capable of capturing temporal relationship among the                       tain event handling functions and these entities are automatically
words in a sentence [47]. These models were good in tasks like                       distributed among the various MPI ranks for parallel processing.
     ArXiv Preprint, 2025, USA                                                                         Atanu Barai, Stephan Eidenbenz, and Nandakishore Santhi


 1   # Gathering simulation involving Small Language Model
 2   agent_speed = [10 , 15 , 20 , 25 , 30]
 3   init_pos = [[0 , 108] , [0 , 462] , [335 , 571] , [543 , 285] , [335 , 0]]
 4   startTime , endTime , minDelay , useMPI , mpiLib , simProgress = 0 , 100000 , 0.0001 , True , " / path / to / libmpich " , 1
 5   simianEngine = Simian ( " Gathering_Agents_Dynamic_Gathering_Positions " , startTime , endTime , minDelay , useMPI , mpiLib )
 6   msg_prompt = [ {" role " : " system " , " content " : " You are an AI agent moving in a two - dimensional Euclidean space ."},
 7       {" role ": " user " , " content " : " " } ,]
 8
 9   class SLMAgent ( simianEngine . Entity ) :
10       def __init__ ( self , baseInfo , * args ) :
11           super ( SLMAgent , self ) . __init__ ( baseInfo )
12           self . position = init_pos [ self . num ]
13           self . max_speed = agent_speed [ self . num ]
14           self . slm = Llama ( model_path = " Qwen2 .5 -7 B - Instruct -1 M - f16 . gguf " , n_gpu_layers = -1 , n_ctx =20000 , chat_format =" qwen ")
15       def choose_next_step ( self , optimal , * args ) :
16           msg_prompt [1][ " content " ] = f " You are located at position ({ self . position [0]} , { self . position [1]}) . Your goal is
17                 to go to position ({ optimal [0]} , { optimal [1]}) . You can move maximum { self . max_speed } units in each step .
18                 What should be your position in the next step ? Verify that the distance between your new position and old
19                 position didn 't exceed { self . max_speed } units . Strictly follow the following format to provide your answer
20                 in integer coordinates in the last line of your response . New_Position :(.. , ..) . "
21           response = self . llm . create_chat_completion ( messages = msg_prompt , temperature =0.1)
22           lines = response [ " choices " ][0][ ' message '][ ' content ']. split ( " \ n " )
23           for line in reversed ( lines ) :
24                 if line . find ( " New_Position : " ) != -1:
25                       new_position = re . findall ( r ' \(.*?\) ', line ) [ -1]
26                       break
27           self . position [0] = int ( eval ( re . findall ( r '\ d +\.\ d +|\ d + ', new_position . split ( " , " ) [0]) [ -1]) ) # Parse new pos_x
28           self . position [0] = int ( eval ( re . findall ( r '\ d +\.\ d +|\ d + ', new_position . split ( " , " ) [1]) [ -1]) ) # Parse new pos_y
29           reached_optimal = True if math . dist ( new_position , optimal ) < self . max_speed else False
30           # Schedule update_non_slm_copy_of_agent_pos on " Non - AI - Agent " entity .
31           self . reqService ( simProgress , " update_non_slm_copy_of_agent_pos " , ( self . num , self . position , reached_optimal ) ,
32           " Non -AI - Agent " , 0)
33
34   class NonAIAgent ( simianEngine . Entity ) :
35        def __init__ ( self , baseInfo , * args ) :
36            super ( NonAIAgent , self ) . __init__ ( baseInfo )
37            self . optimal_pos , self . reached_optimal = None , [ False ] * agentCount
38            self . agent_positions = [([ None ] * 2) for _ in range ( agentCount ) ] ,
39        def update_non_slm_copy_of_agent_pos ( self , data , * args ) : # data = ( agent_num , new_pos , reached_optimal ?)
40            slm_agent_num , self . reached_optimals [ slm_agent_num ] = data [0] , data [2]
41            self . agent_positions [ slm_agent_num ][0] = data [1][0] # agent [ num ][0] , x coordinater
42            self . agent_positions [ slm_agent_num ][1] = data [1][1] # agent [ num ][1] , y coordinate
43            # After updating all agent locations ( should happen in same virtual time ) , schedule next event
44            if slm_agent_num == 0: # Only one agent needs to request this
45                 self . reqService ( simProgress , " calculate_optimal_gathering_position " , self . agent_positions , " Non - AI - Agent " ,0)
46        def calculate_optimal_gathering_position ( self , positions_lst , * args ) :
47            if all ( self . reached_optimals ) : # Checks if all agents reached optimal position
48                 for i in range ( agentCount ) :
49                      self . reqService ( simProgress , " dump_stats " , None , " SLM - Agent " , i )
50            else : # Calculates geometric median
51                 self . reached_optimals
52                 self . optimal_position = CACL_GEOMETRIC_MEDIAN ()
53                 for i in range ( agentCount ) :
54                      self . reqService ( sim_progress , " choose_next_step " , self . optimal_position , " SLM - Agent " , i )
55        ............
56   simianEngine . addEntity ( " Non - AI - Agent " , NonAIAgent , 0)
57   for i in range ( agentCount ) :
58        simianEngine . addEntity ( " SLM - Agent " , SLMAgent , i )
59   # Schedule first event at virtual time 0
60   simianEngine . schedService (0 , " calculate_optimal_gathering_position " , init_pos [: agentCount ] , " Non - AI - Agent " , 0)
61
62   simianEngine . run ()
63   simianEngine . exit ()


     Figure 2: Code snippet from our simulator to solve the gathering problem involving multiple AI agent entities and a non-AI
     agent entity. Here the non-AI agent mainly performs structured mathematical side-calculations that SLMs are not so good at
     natively.
Scalable, Symbiotic, AI and Non-AI Agent Based Parallel Discrete Event Simulations                                                     ArXiv Preprint, 2025, USA


As shown in Figure 1, each AI and non-AI agent is implemented                        On the other hand, complex mathematical sub-tasks that SLMs often
as an entity of the Simian engine enabling them to inherently run                    fail to provide correct to, can be handled by the non-AI entities. Each
in parallel. The entity class has several methods like attachService,                sub-task is designated as an event of the PDES simulation. Each event
reqService, createProcess, startProcess to handle the events and pro-                is associated with a Simian entity. When an event is requested, it is
cesses. In our work we use the reqService method to schedule future                  added to the corresponding entity’s event list along with timestamp
events at the corresponding entity which effectively inserts new                     information. When the simulation runs with MPI enabled, these
events into that entity’s event list at the appropriate time slots.                  entities can opportunistically run methods in parallel and execute
    Figure 2 shows an example of how AI/SLM and non-AI agents                        independent events with the current timestamps in their event lists.
are defined as Simian entities. We present the gathering problem                        In many scenarios, it is advantageous to considerably constrain an
in geometry domain where multiple AI-based agents each with it’s                     SLM’s solution space – this helps reduce its tendency to hallucinate
own maximum speed try to gather. In the example, a Simian PDES                       or wander-off into irrelevant contexts. As mentioned, one effective
engine is initiated in line 5. Two classes SLMAgent and NonAIA-                      strategy we adopted was to provide the SLM with a set of multiple
gent are defined in lines 9 and 35 where both inherit the PDES                       choices to choose from. Furthermore, the many non-AI agents in
engine’s Entity class. One instance of NonAIAgent class and multiple                 the simulation are always cross-checking the SLMs’ outputs, and
instances of SLMAgent class are added to the PDES engine as entities                 working to further dynamically constrain the various AI agent’s
using the addEntity function while also assigning specific names                     solution search-space.
and numbers to those entities for identification. In lines 58 to 60                     As an example in Figure 5, the task of multiplication is broken
these entities are added. In line 62, the first event of the simulation              down into the simpler sub-tasks of long multiplication – single digit
(calculate_optimal_gathering_position) is scheduled at virtual time 0                multiplication and left-shifts. When a language model is asked to
on the non-AI entity which calculates the geometric median of given                  multiply large numbers by itself, it often cannot perform the task
coordinates. Further events are generated and registered to the corre-               correctly, except when the numbers are relatively small [57, 61]. This
sponding entities using the reqService method in lines 31, 46, 50, and               behavior is more noticeable for SLMs where the number of parame-
55. The simulation starts with simianEngine.run () at line 64 where                  ters is relatively smaller. But we were able to successfully complete
it starts executing the registered events based on their virtual times-              the task by breaking down the problem into simpler sub-tasks and
tamp. In line 6 and 16 we define the system and user prompts that                    involving both SLM and non-AI agents. We perform partial multi-
are passed to language model inference API create_chat_completion                    plication with all digits of the multiplier in parallel using multiple
(line 21) along with other parameters such as sampling temperature,                  SLMs deployed as individual entities on multiple nodes. These sub-
where the temperature defines the randomness of the output of                        tasks or events are added to corresponding entities to be executed
language models. Higher temperature results in more random and                       in chronological (causal) order.
diverse outputs. The language model in the SLMAgent is initiated
in line 14 where we pass the model path, number of model layers                      4.3    Case Studies
to be offloaded to any available GPU, context size during model                      In this subsection we elaborate how we solve four algorithmic prob-
inference, and chat format. The response from the language model is                  lems from different application domains to demonstrate our cou-
parsed and necessary information in extracted which is later passed                  pling methodology. We solve gathering problem from geometry,
to further events when registering them using reqService method.                     sorting problem from combinatorics, multiplication problem from
Simulation ends when no further events are available in the event                    arithmetic, and breadth-first traversal problem from graph theory.
queue for processing.                                                                Even though the chosen problems are relatively simple, and several
    Incorporating probabilistic AI models such as the language mod-                  solution strategies are already available to humans, these are still
els inherently adds the non-deterministic characteristics in the sim-                substantially challenging to solve for most SLMs and even for the
ulation. Thus, the simulation scenarios with non-deterministic or                    prominent mammoth language models. Hence any improvement in
somewhat random agent decision requirement, can benefit from the                     the state-of-the-art in enabling algorithmic reasoning tasks using
AI/non-AI coupling the most.                                                         language models can be considered significant. In many ways, one
                                                                                     may argue that the chosen problems are representative of some of
                                                                                     the harder problems for the current generation of language models
4.2     Problem Formulation                                                          to solve on their own, and hence serve as representative tough-case
To solve a problem using SLM involving PDES, we (re)formulate it                     scenarios. Next we describe our approach in each case in more detail.
into a multi-step task by breaking the problem into simpler sub-tasks
that can have one of a finite number of possible solutions identifiable              4.3.1 Geometry. We define the problem as n number of autonomous
by an AI-agent. This way, the AI-agent is constrained to a certain                   AI agents on a 2D space (Euclidean plane) trying to gather starting
finite solution space, thereby boosting chances of success in each                   from their initial positions. Each agent has its own maximum speed,
sub-task. When we use more sophisticated models like Qwen [53], for                  thus limiting the number of units it can move in any direction in a
simpler tasks the model is often able to provide correct response. In                given time-step. The optimal gathering position (geometric median)
that case we don’t constrain the model response by providing it with                 is calculated and updated by non-AI agent at each time-step. Step
relevant choices to choose from. We use non-AI agents in tandem                      by step, our simulation method is as below:
with SLMs to solve each sub-task as one of those finite possible                         (a) to start the simulation, the initial positions of the agents are
choices. When an SLM is asked to solve any sub-task, the non-AI                              assigned from preset positions so that the same simulation
agents may be used to verify and correct the responses of an SLM.                            can be performed with varying SLM sampling parameters.
ArXiv Preprint, 2025, USA                                                                          Atanu Barai, Stephan Eidenbenz, and Nandakishore Santhi


   (b) the non-AI agent is scheduled to calculate the geometric me-              Non-AI                      Init Unsorted
       dian as optimal gathering position.                                                                     array and
                                                                                 AI                         Empty Array to
   (c) the SLMs belonging to each agent are asked to choose the new                                          be populated
       position it should move to in next step following maximum
       speed guideline.
   (d) the non-AI agent verifies whether the new position provided
                                                                                                               Select the
       by the SLM follows maximum speed guideline. If not, it sets                                         Smallest Element
       the correct coordinates.                                                                             from Unsorted
                                                                                                                 Array
   (e) the new positions of the agents are passed to the non-AI agent
       to further adjust the optimal gathering position.
                                                                                          Verify
   All of these subtasks are repeated until the agents gather together.                                                              Verify
We deploy n SLMAgent Simian entities (Figure 2, line 9) as n gath-
ering agents. These entities run in parallel by deploying multiple
instances of SLMs on different MPI ranks. The steps are illustrated in            Pops the
Figure 3 where multiple instances of SLM-based agents run parallelly                                                                       Pushes to
                                                                               element from
                                                                                                                 Verify                   the Sorted
to determine new agent position.                                                 Unsorted
                                                                                                                                             Array
                                                                                   Array
4.3.2 Combinatorics. When an SLM is asked to sort an array with
broad ranges of numbers, the response is often incorrect. In fact out
                                                                           Figure 4: Simulation process for sorting array using SLM.
of 10 times the 8-bit quantized Meta-Llama-3.1-8B-Instruct model
was asked to sort a 10-element array, it was able to provide correct
answer 6 time. As a workaround, we break down the problem into            fix the erroneous response. One PDES entity is defined as an SLM-
the following sub-tasks and simulator events mimicking selection          based agent, and another as a non-AI agent. These entities execute
sort algorithm to improve accuracy.                                       their corresponding events in parallel which changes the simulation
    (a) Non-AI agent initializes the unsorted array and an empty          state and adds newly timestamped event requests to that entity’s
        array to hold the sorted array.                                   event list. Figure 4 shows a high-level picture of how the problem is
   (b) SLM based agent is asked to select the smallest element from       formulated as a parallel discrete event simulation.
        the unsorted array.
    (c) SLM agent removes the element from the unsorted array.            4.3.3 Arithmetic. In tandem with LLMs’ overall poor performance
   (d) The removed item is appended to the sorted array which is          when solving most structured mathematical problems, SLMs cannot
        initially empty.                                                  even multiply large numbers correctly [57, 61]. We break down the
   Sub-tasks b, c and, d are repeated until the unsorted array is         task into the simpler steps of long multiplication. Figure 5 shows
empty. A non-AI agent is deployed after each of these LLM-based           our formulation of the problem using a PDES enabled simulation.
sub-tasks’ output to verify those responses and in case of wrong             (a) Define an event/sub-task to get the multiplier digits and their
response, it can send feedback to the SLM agent asking for it to                 positions starting from rightmost.
                                                                             (b) Ask the SLM to provide the product of the multiplicand and
                                                                                 each digit of multiplier.
      Non-AI                                                                 (c) Multiply the partial multiplication result with 10𝑝𝑜𝑠𝑖𝑡𝑖𝑜𝑛 using
                                 Init                                            SLM (i.e., left-shifts).
      AI                        Agent
                                                                             (d) The partials results from each SLM are finally added using a
                               Location
                                                                                 non-AI agent.
                                                                             Here also, SLM responses in steps b and c are verified and if not
                                                                          correct, the SLM is given yet another chance to correct itself. If there
                                                                          are i number of digits in the multiplier then i number of SLM based
                              Calc Optimal                                entities may be deployed to perform steps b and c in parallel for each
                               Gathering                                  digit. In our experiments, we deployed just one non-LLM agent to
                                Position                                  handle PDES events that perform steps a, d along with intermediate
                                                                          result verifications.
                Choosenew
               Choose   new                                               4.3.4 Graph theory. We perform the breadth first traversal of a
             Choose
            Choose    new
                     new
           Choose position
                   new                                  Verify &
                 position
               position
              position                                                    graph as follows:
             position
                maintaining
               maintaining                               Update
              maintaining
            maintaining                                                      (a) initialize the graphs using a non-AI agent. We use the random
                    speed
           maintaining
                  speed                                  Agent
                speed
               speed                                                             graph generator [7] (fast_gnp_random_graph) to randomly
              speed                                     Location
                                                                                 generate 10 graphs each with 10 nodes. We use ‘incident’
                                                                                 encoding (using a graph’s incidence matrix as opposed to its
Figure 3: Simulation process of multiple agents trying to                        adjacency matrix) to represent the graphs as text since this
gather in a 2D space involving SLM.                                              encoding has been show to outperform other schemes [27].
Scalable, Symbiotic, AI and Non-AI Agent Based Parallel Discrete Event Simulations                                                  ArXiv Preprint, 2025, USA



       Non-AI                          Init                                          diverse than the relatively simple, yet representative case-studies
                                    Multiplier,                                      presented in this paper. The authors of this paper intend to open-
       AI                                                                            source the entire PDES-AI simulator framework code for research
                                   Multiplicand,
                                    Result = 0                                       purposes.

                                                                                     5     Experiments and Results
                                  Get each digit                                     In this section we discuss the experimental setup and results in
                                 and its position                                    detail.
                                  number from
                                       right                                         5.1    Hardware Setup
       Multiplican                                                                   We use a cluster of six x86 computer nodes connected in a single
      Multiplicand
            dx                                                                       network to run the MPI enabled parallel discrete event simulations.
      Multiplicand                                               Add to
            x
           digit                                                                     Each node has an Nvidia Volta GPU [65] from the Volta series archi-
           x                                                     Result
          digit                                                                      tecture [19] attached to it. Table 1 shows the configuration of each
         digit
                                                                                     node.
                                   Multiply
                                    Multiply
                                 Partial Result
                                     Multiply                                        Table 1: CPU, GPU and Memory Configuration of a compute
                                  Partial
                                  by 10   Result
                                         position
                                       Partial                                       node.
                                   byResult
                                      10position
                                               by
                                      10position                                                                                               GPU
                                                                                                 CPU                RAM          GPU
                                                                                                                                              Memory
Figure 5: Simulation process for long multiplication involving                           Intel(R) Xeon(R) CPU
SLM.                                                                                                               125GB     Tesla_V100S        32GB
                                                                                         E5-2660 v3 @ 2.60GHz

   (b) also initialize an empty queue and an empty list of visited
                                                                                        To demonstrate the scaling gain from deploying the models in
       nodes.
                                                                                     multiple ranks for parallel execution, we use a different hardware
   (c) beginning from the start node, for each of its adjacent nodes,
                                                                                     setup. This is due to the fact that when we offload the models to the
       the SLM is asked to check if it is in the Visited list. If not, it is
                                                                                     attached GPUs listed in Table 1 to accelerate token generation, GPU
       pushed to the back of the queue data-structure.
                                                                                     memory runs out and thus multiple MPI ranks can’t be assigned to
   (d) next, the queue head is popped and its adjacent nodes are
                                                                                     single node to show strong scaling. Due to this we run the models
       also pushed to the queue depending on the responses from
                                                                                     on a cluster of 6 AMD EPYC_7402 @2.8GHz CPUs each with 503GB
       the SLM.
                                                                                     of memory attached. This larger memory size allows us to assign
                                                                                     multiple MPI ranks on a single node avoiding overflow. We take
               Non-AI            Init Graph,                                         the geometry problem to show simulation scaling with MPI rank in-
                                   Empty                                             crease. We assign 18 CPU threads for the SLM inference within each
               AI
                                 Queue, List                                         MPI rank. Thus each MPI rank deploys 18 threads to run inference
                                  of Visited                                         in CPUs.

                                                                                     5.2    SLM Models
                               Is the Adjacent
                                 Node in the                                         We use instruct versions of three state-of-the-art open-weight mod-
                                 Visited List?                                       els – Qwen [53], Llama3 [25] and Mistral-Nemo [64] – which have
                                                                                     been fine tuned for a question-answer scenario. We use the smaller
                Push to                                   Pop                        versions of these models in our experiment since the larger mod-
                  the                                    Queue                       els of 70B+ parameters require a large amount of local video-ram
                Queue                                    Head                        memory and more powerful GPUs to accelerate that are stipulated
                                                                                     to be unavailable. For Qwen and Llama3, we use a 7 and 8 billion
                                                                                     parameter versions respectively and for Mistral-Nemo, the available
Figure 6: Simulation process for breadth-first traversal involv-
                                                                                     models had a 12B parameter size. The FP32 versions of these models
ing SLM.
                                                                                     are still large enough to not fit in our GPUs, since we used GPU
                                                                                     configurations with 32GB VRAM memories. As a workaround, for
                                                                                     Qwen we used 16 bits and, for Llama3 and Mistral-Nemo we used the
4.4     Open Source Generic PDES-AI Framework                                        8-bit quantized versions of these models in GPT-Generated Unified
Our Simian PDES based AI/non-AI hybrid agent simulator has been                      Format (GGUF) [31] available on Huggingface repositories [5, 53].
designed in a generic manner with a view to enable its use in complex,               Table 2 shows the details of these models. Using such quantized,
real-world reasoning problems of broader research interest, more                     smaller models further enabled running the initial experiments on
ArXiv Preprint, 2025, USA                                                                                Atanu Barai, Stephan Eidenbenz, and Nandakishore Santhi


an Apple M3 MacBook with Metal Shading Language (MSL) accel-                                                    Agent 1                                                Agent 1

eration and 64GB total RAM. [2]. We use Qwen in the geometry               500
                                                                                                                Agent 2
                                                                                                                Agent 3
                                                                                                                Agent 4            500
                                                                                                                                                                       Agent 2
                                                                                                                                                                       Agent 3
                                                                                                                                                                       Agent 4
                                                                                                                Agent 5                                                Agent 5
problem, since it can provide new positions of the agents quite ac-        400
                                                                                                                Geometric Median
                                                                                                                                   400
                                                                                                                                                                       Geometric Median



curately compared to other two models. For the other problems we           300                                                     300

experiment with LLama3 and Mistral-Nemo.                                   200                                                     200


                                                                           100                                                     100


Table 2: CPU, GPU and Memory Configuration of a compute                     0                                                       0
                                                                                 0     100   200   300    400         500                0     100   200   300   400         500
node.
                                                                                     (a) Temperature 0.1                                     (f) Temperature 0.1
                                            Original    Quantized
                             Parameter                                                                          Agent 1                                                Agent 1
             Name                            Model       Model                                                  Agent 2                                                Agent 2

                                Size
                                                                                                                Agent 3                                                Agent 3
                                                                           500                                  Agent 4            500                                 Agent 4

                                              Size        Size
                                                                                                                Agent 5                                                Agent 5
                                                                                                                Geometric Median                                       Geometric Median
                                                                           400                                                     400



    Qwen2.5-7B-Instruct-                                                   300                                                     300

                                 7B         30.5GB       15.2 GB
       1M-f16.gguf                                                         200                                                     200


                                                                           100                                                     100

      Meta-Llama-3.1-8B-
                                 8B         32.10GB      8.54 GB            0                                                       0

      Instruct-Q8_0.gguf                                                         0     100   200   300    400         500                0     100   200   300   400         500




                                                                                     (b) Temperature 0.2                                     (g) Temperature 0.2
   Mistral-Nemo-Instruct-        12B        49.00GB      13.02GB
      2407-Q8_0.gguf
                                                                                                                Agent 1                                                Agent 1
                                                                           600                                  Agent 2                                                Agent 2
                                                                                                                Agent 3                                                Agent 3
                                                                                                                Agent 4            500                                 Agent 4
                                                                           500                                  Agent 5                                                Agent 5
                                                                                                                Geometric Median                                       Geometric Median
                                                                                                                                   400
                                                                           400

   To run inference on these models we used llama-cpp-python[11],          300
                                                                                                                                   300


which is a python binding of the llama-cpp [32] implementation.            200
                                                                                                                                   200


Llama-cpp-python is an open-source, lightweight, cross-platform            100                                                     100


supported, community driven C++ accelerated LLM inference li-               0
                                                                                 0     100   200   300    400         500
                                                                                                                                    0
                                                                                                                                         0     100   200   300   400         500

brary. It supports quantization and is especially optimized to run
efficiently on devices with limited resources. Thus it enables running               (c) Temperature 0.3                                     (h) Temperature 0.3
the models locally even on CPUs without GPU acceleration ensuring
on-device privacy where user data never leaves the user premises.                                               Agent 1
                                                                                                                Agent 2
                                                                                                                Agent 3
                                                                                                                                                                       Agent 1
                                                                                                                                                                       Agent 2
                                                                                                                                                                       Agent 3

When running the SLM inference using llama-cpp-python, we keep
                                                                           500                                  Agent 4            500                                 Agent 4
                                                                                                                Agent 5                                                Agent 5
                                                                                                                Geometric Median                                       Geometric Median

the default parameters such as top_p = 0.95 (sample from tokens
                                                                           400                                                     400



with 95% probability), top_k = 40 (sample from top 40 tokens) except
                                                                           300                                                     300



for the gathering problem where we vary modeltemperature.
                                                                           200                                                     200



   Line 10 in Figure 2 shows how a model object is initialized using
                                                                           100                                                     100



llama-cpp-python. The path to the model location and preferred
                                                                            0                                                       0
                                                                                 0     100   200   300    400         500                0     100   200   300   400         500


context size is provided to the object-constructor along with the
preferred chat format for the model. Llama-cpp-python supports                       (d) Temperature 0.4                                     (i) Temperature 0.4
llama-3 and mistral-instruct formats which are required to run the
                                                                                                                Agent 1                                                Agent 1
models in table 2. Line 21 shows an example how a response can             500
                                                                                                                Agent 2
                                                                                                                Agent 3
                                                                                                                Agent 4            500
                                                                                                                                                                       Agent 2
                                                                                                                                                                       Agent 3
                                                                                                                                                                       Agent 4

be generated from a language model. In our experimental setup, we
                                                                                                                Agent 5                                                Agent 5
                                                                                                                Geometric Median                                       Geometric Median
                                                                           400                                                     400

use 8192 as our standard context window size, use GPU acceleration         300                                                     300

whenever available and further limit the maximum number of tokens          200                                                     200

generated by the SLM to 512, leaving other parameters to their             100                                                     100

defaults.                                                                   0                                                       0
                                                                                 0     100   200   300    400         500                0     100   200   300   400         500



5.3     Result Verification
                                                                                     (e) Temperature 0.5                                     (j) Temperature 0.5
To compare the result of our approach against the response solely
from the SLM (without PDES based coupling, to serve as the base-         Figure 7: Comparing the paths the SLM-based agents take
case scenario for comparison), we ask the SLM to solve the same          when the SLM is asked to choose paths varying SLM sampling
problem using zero-shot prompting [69]. Here the SLMs are also           temperatures. The figures in the left column (a-e) show the
given a second chance to correct their responses. To serve as a          path the SLM-based agents take when the non-AI agent / simu-
benchmark to compare our coupling methodology against vanilla            lation entity doesn’t verify and correct the SLM response. The
stand-alone language-models, we randomly generated ten problems          images in right column (f-j) shows the path the same agents
for the combinatorics, arithmetic, and graph domains mentioned in        take with same SLM temperature settings, but response veri-
subsection 4.3 to be solved. As an example, we used the following        fied and corrected by the non-AI agent.
Scalable, Symbiotic, AI and Non-AI Agent Based Parallel Discrete Event Simulations                                                                         ArXiv Preprint, 2025, USA



                         Accuracy comparison in solving different problems                              are listed on Figure 2’s line 3. The maximum distance each agent can
                                                                                                        travel is also listed in line 2 of the same figure. The left column of the
 12
                                                                                                        figure shows the path the agents take when trying to gather. We vary
 10                                                                                                     the sampling temperature of the LLM agents to obtain different paths
     8                                                                                                  the agents take to gather. Without verification of SLM response,
     6                                                                                                  we notice that sometimes the agents take big jumps exceeding the
     4
                                                                                                        predefined maximum distance it can travel in each step. On the other
                                                                                                        hand, the figures in the right column show that when these jumps are
     2
                                                                                                        detected by the non-AI agent, it can ask the SLM to provide correct
     0
                                                                                                        new position or even it can itself correct the error; thus avoiding
                         llama3       mistral-nemo   llama3    mistral-nemo   llama3     mistral-nemo
                                                                                                        the jumps. Overall smoothness and quality of the agent trajectories
                                  Sorting               Multiplication                 BFS
                                                                                                        is observed to be better with the symbiotic coupling strategy, with
                                                      PDES    Zero-Shot
                                                                                                        differences being more noticeable at lower temperatures.
                                                                                                           Figure 8 compares the accuracy of our approach against zero-shot
Figure 8: Comparison of results among PDES-based approach                                               prompting in solving the problems except the geometry(gathering
and vanilla SLM with Zero-Shot prompt.                                                                  problem). For the array sorting problem we observe that the LLM
                                                                                                        makes mistake in the smallest number selection stage. We see the
                                                                                                        largest gain in accuracy for the multiplication task. We also observe
                                        Simulation Time Scaling with Ranks                              that llama-3.1 models performs better that mistral-nemo in sorting
                   325                                                                                  and bfs. In case of multiplication, the accuracy depends on the capa-
                   300                                                                                  bility to do single-digit multiplication of the multiplicand. Since the
 Time in minutes




                   275                                                                                  parameter size of mistral-nemo is larger than llama3, this behavior
                                                                                                        is expected. Overall, when llama-3.1 SLM is used, PDES based so-
                   250
                                                                                                        lution has overall accuracy of 77% where the accuracy of zero-shot
                   225                                                                                  prompt is 26%. On the other hand, for mistral-nemo, the accuracy of
                   200                                                                                  PDES based and zero-shot prompt based solution is 60% and, 20%
                   175                                                                                  respectively.
                            1                 2        3            4         5              6             Figure 9 shows that with the increase of simulation ranks, the
                                                        No. of Ranks
                                                                                                        simulation time decreases while Figure 10 shows that the average
                                                                                                        number of tokens generated by the language models per minute also
Figure 9: Simulation time as number of MPI ranks in the PDES                                            increase with the increase of MPI ranks for the gathering simulation.
model is varied.                                                                                        The incremental improvements are more when the number of MPI
                                            Tokens/Minutes Scaling with Ranks                           ranks are low, since more agent entities need to be assigned on
                                                                                                        the same MPI rank (or compute node). In the geometric simulation
                   700
                                                                                                        scenario which is shown in the plot, there were 6 agents in total: 5
                   650                                                                                  SLM AI agents, and 1 non-AI rule enforcing agent. In all our four
 Tokens/minute




                   600                                                                                  scenario based experiments, strong scaling in simulation time and
                   550                                                                                  tokens/minute has been observed up to as many ranks as there
                   500                                                                                  are instantiated agents, since the AI agents in particular are almost
                   450                                                                                  always compute/memory-resource bound.
                   400
                            1                 2        3            4         5              6
                                                        No. of Ranks                                    6    Conclusion
                                                                                                        This paper presents a PDES based novel methodology to couple
                                                                                                        multiple AI and non-AI agents in a rule-based way to work towards
                     Figure 10: Tokens/sec with scaling of MPI ranks
                                                                                                        a common goal. With the support of MPI, careful problem decom-
user and system prompts to get the responses from SLMs for the                                          position, and multiple-choice constraints, the AI and non-AI agents
sorting problem.                                                                                        run in parallel to solve each sub-task of a more complex parent-
System Prompt : You a r e an AI a g e n t who can                                                       task. We demonstrated how four problems from diverse domains
       s o r t an a r r a y .                                                                           may be efficiently solved by our structured, parallel discrete event
                                                                                                        simulation strategy involving multiple AI and non-AI agents. More-
U s e r Prompt : S o r t t h e a r r a y [ 4 7 5 6 2 3 , 5 7 7 9 6 3 ,
                                                                                                        over, the intermediate results are cross-checked using non-AI agents
       156161 , 563672 , 7440 , 844580 , 365172 ,
                                                                                                        (potentially involving even more complex sub-simulations), pro-
       730079 , 984081 , 120146].                                                                       moting verifiability of AI model responses and thereby ensuring
   For the Geometry problem, Figure 7 shows the path of the agents                                      trustworthiness of AI agent simulations. Results show that our ap-
in various conditions. We choose the starting positions of the agents                                   proach achieves a much better accuracy while enabling collaborative
as the vertices of a pentagon for better visualization. These vertices                                  problem solving, among multiple AI and non-AI agents, which is
ArXiv Preprint, 2025, USA                                                                                               Atanu Barai, Stephan Eidenbenz, and Nandakishore Santhi


essentially the first step towards automated harnessing of domain ex-                        [19] NVIDIA Corporation. June 2017. Volta Tesla V100 GPU Architecture Whitepa-
pertise from different fields. Furthermore, we intend to open-source                              per. http://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-
                                                                                                  whitepaper.pdf
release the PDES-AI agent simulator codebase for research purposes.                          [20] Bruce Croft and John Lafferty. 2003. Language modeling for information retrieval.
                                                                                                  Vol. 13. Springer Science & Business Media.
                                                                                             [21] Damai Dai, Chengqi Deng, Chenggang Zhao, R. X. Xu, Huazuo Gao, Deli Chen,
                                                                                                  Jiashi Li, Wangding Zeng, Xingkai Yu, Y. Wu, Zhenda Xie, Y. K. Li, Panpan Huang,
References                                                                                        Fuli Luo, Chong Ruan, Zhifang Sui, and Wenfeng Liang. 2024. DeepSeekMoE:
 [1] Eduardo Alonso, Mark D’Inverno, Daniel Kudenko, Michael Luck, and Jason Noble.               Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models.
     2001. Learning in multi-agent systems. The Knowledge Engineering Review 16, 3                arXiv:2401.06066 [cs.CL] https://arxiv.org/abs/2401.06066
     (2001), 277–284. doi:10.1017/S0269888901000170                                          [22] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT:
 [2] Apple. July 2024. Metal Overview. https://developer.apple.com/metal/                         Pre-training of Deep Bidirectional Transformers for Language Understanding.
 [3] Alessio Baratta, Antonio Cimino, Maria Grazia Gnoni, and Francesco Longo. 2023.              arXiv:1810.04805 [cs.CL] https://arxiv.org/abs/1810.04805
     Human Robot Collaboration in Industry 4.0: a literature review. Procedia Computer       [23] Georgios Diamatopoulos, Georgios Theodoropoulos, Nikos Tziritas, and Rami
     Science 217 (2023), 1887–1895. doi:10.1016/j.procs.2022.12.389 4th International             Bahsoon. 2024. Towards LLM Augmented Discrete Event Simulation of Blockchain
     Conference on Industry 4.0 and Smart Manufacturing.                                          Systems. In Proceedings of the 38th ACM SIGSIM Conference on Principles of Ad-
 [4] Peter D. Barnes, Christopher D. Carothers, David R. Jefferson, and Justin M. LaPre.          vanced Discrete Simulation (Atlanta, GA, USA) (SIGSIM-PADS ’24). Association for
     2013. Warp speed: executing time warp on 1,966,080 cores. In Proceedings of the 1st          Computing Machinery, New York, NY, USA, 75–76. doi:10.1145/3615979.3662156
     ACM SIGSIM Conference on Principles of Advanced Discrete Simulation (Montr©al,          [24] Ruomeng Ding, Chaoyun Zhang, Lu Wang, Yong Xu, Minghua Ma, Wei Zhang, Si
     Québec, Canada) (SIGSIM PADS ’13). Association for Computing Machinery, New                  Qin, Saravan Rajmohan, Qingwei Lin, and Dongmei Zhang. 2024. Everything of
     York, NY, USA, 327–336. doi:10.1145/2486092.2486134                                          Thoughts: Defying the Law of Penrose Triangle for Thought Generation. In ACL
 [5] A Bartowski. Septerber 2024. Mistral-Nemo-Instruct-2407-GGUF - Hugging Face.                 (Findings). 1638–1662. https://doi.org/10.18653/v1/2024.findings-acl.95
     https://huggingface.co/bartowski/Mistral-Nemo-Instruct-2407-GGUF                        [25] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
 [6] Regina Barzilay and Lillian Lee. 2004. Catching the Drift: Probabilistic Con-                Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, and Angela Fan
     tent Models, with Applications to Generation and Summarization. In Proceed-                  et. al. 2024. The Llama 3 Herd of Models. arXiv:2407.21783 [cs.AI] https://arxiv.
     ings of the Human Language Technology Conference of the North American Chap-                 org/abs/2407.21783
     ter of the Association for Computational Linguistics: HLT-NAACL 2004. Asso-             [26] Ali Eker, Yehia Arafa, Abdel-Hameed A. Badawy, Nandakishore Santhi, Stephan
     ciation for Computational Linguistics, Boston, Massachusetts, USA, 113–120.                  Eidenbenz, and Dmitry Ponomarev. 2021. Load-Aware Dynamic Time Syn-
     https://aclanthology.org/N04-1015                                                            chronization in Parallel Discrete Event Simulation. In Proceedings of the 2021
 [7] Vladimir Batagelj and Ulrik Brandes. 2005. Efficient generation of large random              ACM SIGSIM Conference on Principles of Advanced Discrete Simulation (SIGSIM-
     networks. Phys. Rev. E 71 (Mar 2005), 036113. Issue 3. doi:10.1103/PhysRevE.71.              PADS ’21). Association for Computing Machinery, New York, NY, USA, 95–105.
     036113                                                                                       doi:10.1145/3437959.3459249
 [8] David W. Bauer Jr., Christopher D. Carothers, and Akintayo Holder. 2009. Scalable       [27] Bahare Fatemi, Jonathan Halcrow, and Bryan Perozzi. 2024. Talk like a Graph: En-
     Time Warp on Blue Gene Supercomputers. In 2009 ACM/IEEE/SCS 23rd Workshop on                 coding Graphs for Large Language Models. In The Twelfth International Conference
     Principles of Advanced and Distributed Simulation. 35–44. doi:10.1109/PADS.2009.21           on Learning Representations. https://openreview.net/forum?id=IuXR1CCrSi
 [9] Y. Bengio, P. Simard, and P. Frasconi. 1994. Learning long-term dependencies            [28] Richard M. Fujimoto. 1990. Parallel discrete event simulation. Commun. ACM 33,
     with gradient descent is difficult. IEEE Transactions on Neural Networks 5, 2 (1994),        10 (Oct. 1990), 30–53. doi:10.1145/84537.84545
     157–166. doi:10.1109/72.279181                                                          [29] Richard M. Fujimoto, K. Perumalla, A. Park, H. Wu, M.H. Ammar, and G.F. Riley.
[10] Adam Berger and John Lafferty. 2001. Statistical machine learning for information            2003. Large-scale network simulation: how big? how fast?. In 11th IEEE/ACM In-
     retrieval. Ph. D. Dissertation. Carnegie Mellon University, USA. AAI3168516.                 ternational Symposium on Modeling, Analysis and Simulation of Computer Telecom-
[11] Andrei Betlen. October 2024. Python bindings for llama.cpp. https://github.com/              munications Systems, 2003. MASCOTS 2003. 116–123. doi:10.1109/MASCOT.2003.
     abetlen/llama-cpp-python                                                                     1240649
[12] Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora,                [30] Jianfeng Gao and Chin-Yew Lin. 2004. Introduction to the special issue on statistical
     Sydney von Arx, and Michael S. Bernstein et. al. 2021. On the Opportunities and              language modeling. ACM Transactions on Asian Language Information Processing
     Risks of Foundation Models. ArXiv (2021). https://crfm.stanford.edu/assets/report.           3, 2 (June 2004), 87–93. doi:10.1145/1034780.1034781
     pdf                                                                                     [31] Georgi Gerganov. Septerber 2024. GGUF. https://github.com/ggerganov/ggml/
[13] Peter F. Brown, Peter V. deSouza, Robert L. Mercer, Vincent J. Della Pietra, and             blob/master/docs/gguf.md
     Jenifer C. Lai. 1992. Class-based n-gram models of natural language. Comput.            [32] Georgi Gerganov. Septerber 2024. LLM inference in C/C++. https://github.com/
     Linguist. 18, 4 (Dec. 1992), 467–479.                                                        ggerganov/llama.cpp
[14] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Pra-             [33] Zelalem Gero, Chandan Singh, Hao Cheng, Tristan Naumann, Michel Galley,
     fulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,              Jianfeng Gao, and Hoifung Poon. 2023. Self-Verification Improves Few-Shot
     Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon                  Clinical Information Extraction. arXiv:2306.00024 [cs.CL] https://arxiv.org/abs/
     Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse,               2306.00024
     Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark,         [34] Philippe J. Giabbanelli. 2023. GPT-Based Models Meet Simulation: How to Effi-
     Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario                  ciently use Large-Scale Pre-Trained Language Models Across Simulation Tasks. In
     Amodei. 2020. Language Models are Few-Shot Learners. In Advances in Neural                   Proceedings of the Winter Simulation Conference (San Antonio, Texas, USA) (WSC
     Information Processing Systems, H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan,          ’23). IEEE Press, 2920–2931.
     and H. Lin (Eds.), Vol. 33. Curran Associates, Inc., 1877–1901.                         [35] Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang,
[15] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao                    and Zhiting Hu. 2023. Reasoning with Language Model is Planning with World
     Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, Wei Ye, Yue Zhang, Yi Chang,                  Model. arXiv:2305.14992 [cs.CL] https://arxiv.org/abs/2305.14992
     Philip S. Yu, Qiang Yang, and Xing Xie. 2024. A Survey on Evaluation of Large           [36] Pablo Hernandez-Leal, Bilal Kartal, and Matthew E Taylor. 2019. A survey and
     Language Models. ACM Trans. Intell. Syst. Technol. 15, 3, Article 39 (March 2024),           critique of multiagent deep reinforcement learning. Autonomous Agents and
     45 pages. doi:10.1145/3641289                                                                Multi-Agent Systems 33, 6 (2019), 750–797.
[16] Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen. 2023. Program of             [37] Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long Short-Term Memory. Neural
     Thoughts Prompting: Disentangling Computation from Reasoning for Numerical                   Computation 9, 8 (1997), 1735–1780. doi:10.1162/neco.1997.9.8.1735
     Reasoning Tasks. Transactions on Machine Learning Research (2023). https:               [38] Takaaki Hori, Jaejin Cho, and Shinji Watanabe. 2018. End-to-end Speech Recog-
     //openreview.net/forum?id=YfZ4ZPt8zd                                                         nition With Word-Based Rnn Language Models. In 2018 IEEE Spoken Language
[17] Kyunghyun Cho, Bart van Merriënboer, Dzmitry Bahdanau, and Yoshua Bengio.                    Technology Workshop (SLT). 389–396. doi:10.1109/SLT.2018.8639693
     2014. On the Properties of Neural Machine Translation: Encoder–Decoder Ap-              [39] Anthony Hunter, Simon Parsons, and Michael Wooldridge. 2014. Measuring
     proaches. In Proceedings of SSST-8, Eighth Workshop on Syntax, Semantics and                 inconsistency in multi-agent systems. KI-Künstliche Intelligenz 28 (2014), 169–
     Structure in Statistical Translation, Dekai Wu, Marine Carpuat, Xavier Carreras,             178.
     and Eva Maria Vecchi (Eds.). Association for Computational Linguistics, Doha,           [40] Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche
     Qatar, 103–111. doi:10.3115/v1/W14-4012                                                      Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou
[18] Alexis Conneau, Douwe Kiela, Holger Schwenk, Loïc Barrault, and Antoine Bordes.              Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample,
     2017. Supervised Learning of Universal Sentence Representations from Natural                 Lélio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep
     Language Inference Data. In Proceedings of the 2017 Conference on Empirical Meth-            Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Théophile Gervet,
     ods in Natural Language Processing. Association for Computational Linguistics,               Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2024.
     Copenhagen, Denmark, 670–680. doi:10.18653/v1/D17-1070                                       Mixtral of Experts. arXiv:2401.04088 [cs.LG] https://arxiv.org/abs/2401.04088
Scalable, Symbiotic, AI and Non-AI Agent Based Parallel Discrete Event Simulations                                                                     ArXiv Preprint, 2025, USA


[41] Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter        [62] Peter Stone and Manuela Veloso. 2000. Multiagent systems: A survey from a
     Clark, and Ashish Sabharwal. 2023. Decomposed Prompting: A Modular Approach               machine learning perspective. Autonomous Robots 8 (2000), 345–383.
     for Solving Complex Tasks. arXiv:2210.02406 [cs.CL] https://arxiv.org/abs/2210.      [63] Foteini Strati, Paul Elvinger, Tolga Kerimoglu, and Ana Klimovic. 2024. ML Train-
     02406                                                                                     ing with Cloud GPU Shortages: Is Cross-Region the Answer?. In Proceedings of
[42] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke                 the 4th Workshop on Machine Learning and Systems (Athens, Greece) (EuroML-
     Iwasawa. 2024. Large language models are zero-shot reasoners. In Proceedings of           Sys ’24). Association for Computing Machinery, New York, NY, USA, 107–116.
     the 36th International Conference on Neural Information Processing Systems (New           doi:10.1145/3642970.3655843
     Orleans, LA, USA) (NIPS ’22). Curran Associates Inc., Red Hook, NY, USA, Article     [64] Mistral AI team. July 2024. Mistral Nemo. https://mistral.ai/news/mistral-nemo/
     1613, 15 pages.                                                                      [65] TechPowerUp. June 2017. NVIDIA Tesla V100 Specs. https://www.techpowerup.
[43] Stefan Kombrink, Tomas Mikolov, Martin Karafiát, and Lukás Burget. 2011. Re-              com/gpu-specs/tesla-v100-pcie-16-gb.c2957
     current Neural Network Based Language Modeling in Meeting Recognition.. In           [66] Sunil Thulasidasan, Lukas Kroc, and Stephan Eidenbenz. 2014. Developing parallel,
     Interspeech, Vol. 11. 2877–2880.                                                          discrete event simulations in Python - first results and user experiences with the
[44] Alisa Liu, Xiaochuang Han, Yizhong Wang, Yulia Tsvetkov, Yejin Choi, and Noah A.          SimX library. In 2014 4th International Conference On Simulation And Modeling
     Smith. 2024. Tuning Language Models by Proxy. arXiv:2401.08565 [cs.CL] https:             Methodologies, Technologies And Applications (SIMULTECH). 188–194. doi:10.5220/
     //arxiv.org/abs/2401.08565                                                                0005042701880194
[45] Tianming Liu, Jirong Yang, and Yafeng Yin. 2024. Toward LLM-Agent-Based Model-       [67] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N
     ing of Transportation Systems: A Conceptual Framework. arXiv:2412.06681 [cs.AI]           Gomez, Lukasz Kaiser, and Illia Polosukhin. 2017. Attention is All you Need. In
     https://arxiv.org/abs/2412.06681                                                          Advances in Neural Information Processing Systems, I. Guyon, U. Von Luxburg,
[46] Xiaoyong Liu and W Bruce Croft. 2005. Statistical language modeling for informa-          S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett (Eds.), Vol. 30.
     tion retrieval. Annu. Rev. Inf. Sci. Technol. 39, 1 (2005), 1–31.                         Curran Associates, Inc.
[47] Tomas Mikolov, Martin Karafiát, Lukas Burget, Jan Cernockỳ, and Sanjeev Khu-        [68] Yu Wang, Zhiwei Liu, Jianguo Zhang, Weiran Yao, Shelby Heinecke, and Philip S.
     danpur. 2010. Recurrent neural network based language model.. In Interspeech,             Yu. 2023. DRDT: Dynamic Reflection with Divergent Thinking for LLM-based
     Vol. 2. Makuhari, 1045–1048.                                                              Sequential Recommendation. arXiv:2312.11336 [cs.IR] https://arxiv.org/abs/2312.
[48] Guo Ming. 2023. Exploration of the intelligent control system of autonomous               11336
     vehicles based on edge computing. PLoS One 18, 2 (2023), e0281294.                   [69] Jason Wei, Maarten Bosma, Vincent Zhao, Kelvin Guu, Adams Wei Yu, Brian
[49] Mohammed Muqeeth, Haokun Liu, Yufan Liu, and Colin Raffel. 2024. Learn-                   Lester, Nan Du, Andrew M. Dai, and Quoc V Le. 2022. Finetuned Language Models
     ing to Route Among Specialized Experts for Zero-Shot Generalization.                      are Zero-Shot Learners. In International Conference on Learning Representations.
     arXiv:2402.05859 [cs.LG] https://arxiv.org/abs/2402.05859                                 https://openreview.net/forum?id=gEZrGCozdqR
[50] OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya,        [70] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud,
     Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, and Sam Altman et.             Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tat-
     al. 2024. GPT-4 Technical Report. arXiv:2303.08774 [cs.CL] https://arxiv.org/abs/         sunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus. 2022.
     2303.08774                                                                                Emergent Abilities of Large Language Models. Transactions on Machine Learning
[51] Kalyan S. Perumalla. 2007. Scaling time warp-based discrete event execution to            Research (2022). https://openreview.net/forum?id=yzkSU5zdwD Survey Certifi-
     104 processors on a Blue Gene supercomputer. In Proceedings of the 4th Interna-           cation.
     tional Conference on Computing Frontiers (Ischia, Italy) (CF ’07). Association for   [71] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei
     Computing Machinery, New York, NY, USA, 69–76. doi:10.1145/1242531.1242543                Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2024. Chain-of-thought prompting
[52] Zhenting Qi, Mingyuan Ma, Jiahang Xu, Li Lyna Zhang, Fan Yang, and Mao                    elicits reasoning in large language models. In Proceedings of the 36th International
     Yang. 2024. Mutual Reasoning Makes Smaller LLMs Stronger Problem-Solvers.                 Conference on Neural Information Processing Systems (New Orleans, LA, USA) (NIPS
     arXiv:2408.06195 [cs.CL] https://arxiv.org/abs/2408.06195                                 ’22). Curran Associates Inc., Red Hook, NY, USA, Article 1800, 14 pages.
[53] Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen          [72] Michael Wooldridge. 2009. An introduction to multiagent systems. John wiley &
     Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang,               sons.
     Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang          [73] Zengqing Wu, Run Peng, Xu Han, Shuyuan Zheng, Yixin Zhang, and Chuan Xiao.
     Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue,             2023. Smart Agent-Based Modeling: On the Use of Large Language Models in
     Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia,              Computer Simulations. arXiv:2311.06330 [cs.AI] https://arxiv.org/abs/2311.06330
     Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan,              [74] Fuzhao Xue, Zian Zheng, Yao Fu, Jinjie Ni, Zangwei Zheng, Wangchunshu Zhou,
     Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. 2025. Qwen2.5 Technical               and Yang You. 2024. OpenMoE: An Early Effort on Open Mixture-of-Experts
     Report. arXiv:2412.15115 [cs.CL] https://arxiv.org/abs/2412.15115                         Language Models. arXiv:2402.01739 [cs.CL] https://arxiv.org/abs/2402.01739
[54] Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. 2018. Improv-    [75] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao,
     ing language understanding by generative pre-training. https://cdn.openai.com/            and Karthik Narasimhan. 2023. Tree of Thoughts: Deliberate Problem Solving with
     research-covers/language-unsupervised/language_understanding_paper.pdf                    Large Language Models. arXiv:2305.10601 [cs.CL] https://arxiv.org/abs/2305.10601
[55] Rong Rong, Jiang Hao, and Jason Liu. 2014. Performance Study of a Minimalistic       [76] Di Zhang, Xiaoshui Huang, Dongzhan Zhou, Yuqiang Li, and Wanli Ouyang. 2024.
     Simulator on XSEDE Massively Parallel Systems. In Proceedings of the 2014 Annual          Accessing GPT-4 level Mathematical Olympiad Solutions via Monte Carlo Tree Self-
     Conference on Extreme Science and Engineering Discovery Environment (Atlanta,             refine with LLaMa-3 8B. arXiv:2406.07394 [cs.AI] https://arxiv.org/abs/2406.07394
     GA, USA) (XSEDE ’14). Association for Computing Machinery, New York, NY,             [77] Yifan Zhang, Yang Yuan, and Andrew Chi-Chih Yao. 2024. Meta Prompting for AI
     USA, Article 15, 8 pages. doi:10.1145/2616498.2616512                                     Systems. arXiv:2311.11482 [cs.AI] https://arxiv.org/abs/2311.11482
[56] Nandakishore Santhi, Stephan Eidenbenz, and Jason Liu. 2015. The Simian concept:     [78] Huaixiu Steven Zheng, Swaroop Mishra, Xinyun Chen, Heng-Tze Cheng, Ed H.
     Parallel Discrete Event Simulation with interpreted languages and just-in-time            Chi, Quoc V Le, and Denny Zhou. 2024. Take a Step Back: Evoking Reasoning via
     compilation. In 2015 Winter Simulation Conference (WSC). 3013–3024. doi:10.1109/          Abstraction in Large Language Models. In The Twelfth International Conference on
     WSC.2015.7408405                                                                          Learning Representations. https://openreview.net/forum?id=3bq3jsvcQ1
[57] Ankit Satpute, Noah Gießing, André Greiner-Petter, Moritz Schubotz, Olaf Teschke,    [79] Aojun Zhou, Ke Wang, Zimu Lu, Weikang Shi, Sichun Luo, Zipeng Qin, Shaoqing
     Akiko Aizawa, and Bela Gipp. 2024. Can LLMs Master Math? Investigating Large              Lu, Anya Jia, Linqi Song, Mingjie Zhan, and Hongsheng Li. 2024. Solving Chal-
     Language Models on Math Stack Exchange. In Proceedings of the 47th Interna-               lenging Math Word Problems Using GPT-4 Code Interpreter with Code-based
     tional ACM SIGIR Conference on Research and Development in Information Retrieval          Self-Verification. In The Twelfth International Conference on Learning Representa-
     (Washington DC, USA) (SIGIR ’24). Association for Computing Machinery, New                tions. https://openreview.net/forum?id=c8McWs4Av0
     York, NY, USA, 2316–2320. doi:10.1145/3626772.3657945                                [80] Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang,
[58] Noam Shazeer, *Azalia Mirhoseini, *Krzysztof Maziarz, Andy Davis, Quoc Le,                Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc V Le, and Ed H. Chi. 2023.
     Geoffrey Hinton, and Jeff Dean. 2017. Outrageously Large Neural Networks: The             Least-to-Most Prompting Enables Complex Reasoning in Large Language Models.
     Sparsely-Gated Mixture-of-Experts Layer. In International Conference on Learning          In The Eleventh International Conference on Learning Representations. https://
     Representations. https://openreview.net/forum?id=B1ckMDqlg                                openreview.net/forum?id=WZH7099tgfM
[59] Shannon Zejiang Shen, Hunter Lang, Bailin Wang, Yoon Kim, and David Son-             [81] Yanqi Zhou, Tao Lei, Hanxiao Liu, Nan Du, Yanping Huang, Vincent Zhao, An-
     tag. 2024. Learning to Decode Collaboratively with Multiple Language Models.              drew M Dai, Quoc V Le, James Laudon, et al. 2022. Mixture-of-experts with expert
     arXiv:2403.03870 [cs.CL] https://arxiv.org/abs/2403.03870                                 choice routing. Advances in Neural Information Processing Systems 35 (2022),
[60] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik                     7103–7114.
     Narasimhan, and Shunyu Yao. 2023. Reflexion: Language Agents with Verbal Re-
     inforcement Learning. arXiv:2303.11366 [cs.AI] https://arxiv.org/abs/2303.11366
[61] Viraj Singh. July 16, 2024. Why LLMs Are Bad at Math — and How They Can Be
     Better. https://www.reachcapital.com/2024/07/16/why-llms-are-bad-at-math-
     and-how-they-can-be-better/
