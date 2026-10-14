                                               Formally Specifying the High-Level Behavior of LLM-Based Agents

                                               Maxwell Crouse, Ibrahim Abdelaziz, Ramon Astudillo, Kinjal Basu, Soham Dan,
                                             Sadhana Kumaravel, Achille Fokoue, Pavan Kapanipathi, Salim Roukos, Luis Lastras
                                                  { maxwell.crouse, ibrahim.abdelaziz1, ramon.astudillo }@ibm.com
                                                      { kinjal.basu, soham.dan, sadhana.kumaravel1 }@ibm.com
                                                        { achille, kapanipa, roukos, lastrasl }@us.ibm.com
                                                                              IBM Research


                                                                Abstract                             API call (Schick et al., 2023; Qin et al., 2023; Tang
                                                                                                     et al., 2023), which can supply new context to the
                                              Autonomous, goal-driven agents powered by
                                                                                                     agent. Importantly, while the order of steps to take
                                              LLMs have recently emerged as promising
                                              tools for solving challenging problems with-           is dictated by a high-level, prespecified behavior
arXiv:2310.08535v3 [cs.AI] 24 Jan 2024




                                              out the need for task-specific finetuned models        implemented by the user, the underlying LLM is
                                              that can be expensive to procure. Currently, the       still allowed significant flexibility in what it may
                                              design and implementation of such agents is            produce. At each individual step, the outputs are
                                              ad hoc, as the wide variety of tasks that LLM-         entirely determined by the LLM, thus allowing the
                                              based agents may be applied to naturally means         agent to leverage the strong generative capabili-
                                              there can be no one-size-fits-all approach to
                                                                                                     ties of LLMs while ensuring there are guardrails
                                              agent design. In this work we aim to alleviate
                                              the difficulty of designing and implementing           to prevent aberrant behavior. Figure 1 provides an
                                              new agents by proposing a minimalistic gen-            example of text produced by the popular ReACT
                                              eration framework that simplifies the process          (Yao et al., 2022) framework, where an agent ex-
                                              of building agents. The framework we intro-            ecutes a loop that goes between generative steps
                                              duce allows the user to define desired agent           (i.e., Thought, Action, Action Input) and tool
                                              behaviors in a high-level, declarative specifi-        execution steps (i.e., Observation).
                                              cation that is then used to construct a decod-            Though LLM-based agents show much promise,
                                              ing monitor which guarantees the LLM will
                                                                                                     there still remain challenges involved with their
                                              produce an output exhibiting the desired be-
                                              havior. Our declarative approach, in which the         practical application. As each agent has its own
                                              behavior is described without concern for how          strengths and weaknesses, it can be necessary to try
                                              it should be implemented or enforced, enables          a variety of different agents when approaching a
                                              rapid design, implementation, and experimen-           problem. This can be a steep barrier to entry, as the
                                              tation with different LLM-based agents. We             lack of a standard framework for defining agents
                                              demonstrate how the proposed framework can             means that the end user must reimplement in code
                                              be used to implement recent LLM-based agents
                                                                                                     the exact behavior they wish for an agent to exhibit.
                                              (e.g., ReACT), and show how the flexibility of
                                              our approach can be leveraged to define a new          In addition, the use of explicit code to implement
                                              agent with more complex behavior, the Plan-            agents has lead to their execution being largely
                                              Act-Summarize-Solve (PASS) agent. Lastly, we           rigid, i.e., they are hard coded to follow a fixed
                                              demonstrate that our method outperforms other          path of behavior; which takes away flexibility from
                                              agents on multiple popular reasoning-centric           the LLM in deciding how best to solve a problem.
                                              question-answering benchmarks.                            To address the aforementioned challenges, we
                                                                                                     propose a declarative framework to formally spec-
                                         1     Introduction
                                                                                                     ify the high-level behavior of an LLM-based agent.
                                         Many recent works (e.g., (Brohan et al., 2023; Shen         Our framework takes in an agent behavior speci-
                                         et al., 2023; Yao et al., 2022; Shinn et al., 2023))        fied as a finite-state machine, which it then uses to
                                         have explored the use of large language models              define a decoding monitor that ensures the LLM-
                                         (LLMs) to drive the decision-making of intelligent,         based agent executes steps in a way that conforms
                                         autonomous agents. Given a problem to solve,                to the user’s expectation. Importantly, the decoding
                                         these LLM-based agents break the problem down               monitor operates in a post hoc fashion, intervening
                                         into a sequence of steps, where each step involves          only to correct generated text when it observes a
                                         either generating text or executing a tool, e.g., an        deviation from the desired behavior. This makes it

                                                                                                 1
    [Question] Musician and satirist Allie
                                                           tion of entire chunks of text at the client side, thus
    Goertz   wrote    a   song   about   the   “The
                                                           reducing communication overhead.
    Simpsons” character Milhouse, who Matt                    We demonstrate how a number of popular agents
    Groening named after who?                              can be straightforwardly implemented in our frame-
    [Thought] The question simplifies to “The              work (e.g., ReACT (Yao et al., 2022), ReWOO (Xu
    Simpsons” character Milhouse is named                  et al., 2023b), Reflexion (Shinn et al., 2023)). In
    after who. I only need to search ...                   addition, we introduce the Plan-Act-Summarize-
    [Action] Search                                        Solve (PASS) agent. The PASS agent leverages the
    [Action Input] Milhouse                                flexibility enabled by our framework and operates
    [Observation]     Milhouse    Mussolini    Van         by dynamically adjusting the number of actions
    Houten is a recurring character in ...                 it executes in parallel. It thus differs from prior
    [Thought] The paragraph does not tell who              agents that operate entirely sequentially (e.g., (Yao
    Milhouse is named after, maybe I can look              et al., 2022)) or in parallel (e.g., (Xu et al., 2023b)).
    up “named after”.                                         In summary, our contributions in this work are as
    [Action] Lookup                                        follows: (a) we introduce a declarative framework
    [Action Input] named after                             for defining LLM-based agents that ensures confor-
    [Observation] (Result 1 / 1) Milhouse was              mance to desired behaviors with a decoding monti-
    named after U.S. president Richard Nixon,              tor, (b) we demonstrate how to implement a number
    whose middle name was Milhous.                         of well-known agents with our framework, and (c)
    [Final Thought] Milhouse was named after               we introduce PASS, a new agent architecture that
    U.S. president Richard Nixon,          so the          leverages the declarative nature of our framework
    answer is Richard Nixon.                               and yields improved performance as compared to
    [Answer] Richard Nixon                                 other agents across three standard datasets (Hot-
                                                           pot QA (Yang et al., 2018), TriviaQA (Joshi et al.,
                                                           2017), and GSM8K (Cobbe et al., 2021)).
Figure 1: Text output by ReACT agent that
alternates between generative states (Thought,             2     Agent Specification Framework
Action, Action Input) and tool execution states
(Observation)                                              In this section, we introduce our framework for de-
                                                           signing and implementing autonomous agents that
                                                           can interact with the environment to solve problems
applicable to models only accessible through APIs.         expressed in natural language. Our framework is
   The ability to leverage the highest performing          intended to be lightweight (i.e., add as little addi-
LLMs (which are often closed source) is a key              tional overhead to LLM operation as is possible)
component of our approach. Following in-context            and declarative (i.e., the user specifies the desired
learning (Brown et al., 2020) and instruction-tuning       high-level behavior in terms of constraints without
(Wei et al., 2021; Ouyang et al., 2022), LLMs have         concern for how they should be implemented or
shown generalization to a large number of tasks            enforced). To begin, we provide a more formal def-
without any parameter tuning. In addition, it is           inition of agents and how they are specified in our
clear that large model size and the use of special-        framework. Then, we describe how the framework
ized hardware (e.g., GPUs) are fundamental fac-            is used to control what an agent can generate.
tors in performance. For these reasons, centralized
                                                           2.1    Specifying Agent Behavior
systems that serve large numbers of requests re-
motely through an API are increasingly central to          We model agents as generic finite-state machines,
how LLMs are utilized. In this context, custom             where a finite-state machine is considered a tuple
applications of token-level constrained decoding           ⟨DS , δ, s0 , send ⟩ consisting of a non-empty set of
(Wuebker et al., 2016; Hokamp and Liu, 2017)               states DS , a state transition function δ : DS → DS ,
that directly modify the output softmax of a model         an initial state s0 ∈ DS , and a final state send ∈ DS .
would have high communication overhead. The                To define an agent and its underlying state machine,
decoding monitor proposed here circumvents this            the user provides a specification consisting of 1) a
by optimistically assuming most generated tokens           list of states and their properties and 2) a desired
will be correct and rejects or prefixes the genera-        behavior in the form of a logical formula. At each

                                                       2
                                                                           (define react-agent
                                                                              (:states
                                                                                (Ques (:text "[Question]"))
                                                                                (Tht (:text "[Thought]"))
                                                                                (Act (:text "[Action]"))
                                                                                (Act-Inp (:text "[Action Input]"))
                                                                                (Obs (:text "[Observation]")
                                                                                      (:flags :env-input))
                                                                                (Final-Tht (:text "[Final Thought]"))
                                                                                (Ans (:text "[Answer]")))


Figure 2: State diagram of ReACT agent architecture                           (:behavior
                                                                                (next
                                                                                   Ques
time step, the agent will receive a string from either                             (until
an LLM or the environment1 , with the source of                                      (next Tht Act Act-Inp Obs)
the string determined by the state the agent is in.                                  Final-Tht)
   Figure 3 shows an example of a specification                                    Ans)))
provided in the format of a Lisp-style s-expression.
In the specification, the :states list contains all
                                                                       Figure 3: Specification for ReACT agent (see Figure 2)
possible states for the agent. Each state within the
list must specify a prompt string (e.g., “[Thought]”
for the Tht state), which will serve as both an initial                of states produced by our agent, with si being the
prompt for when the agent is in that state and as                      state of our agent at time i. We write that S satisfies
a signal to detect when a state transition occurs.                     (|=) the behavior if the following holds
When the environment is the intended provider of a
string for a particular state, the special :env-input                      S |= a
flag is used (e.g., shown in the Obs state).                                   iff S = ⟨a⟩ ∧ a ∈ :states
   The behavior of an agent is provided in the                             S |= (or a b c . . . )
:behavior list as a logical formula, where each for-                           iff S |= a ∨ S |= b ∨ . . . ∨ S |= c ∨ . . .
mula is constructed from states connected together
                                                                           S |= (next a b c . . . )
with the logical operators or, next or until. We
enforce that the top-level formula in :behavior                                iff ∃i > 0. S[0 . . . i] |= a
begins with next. From the formula, a finite-state                             and S[i . . .] |= (next b c . . . )
machine (FSM) is constructed that will be used to                          S |= (until a b)
validate the behavior of the agent.
                                                                               iff ∃j ≥ 0. S[j . . .] |= b
   The operators are taken from linear-temporal
logic (LTL) (Pnueli, 1977), which is commonly                                  and S[i . . .] |= a, for all 0 ≤ i < j
used for runtime verification systems. We note                         where S[i . . . j] = ⟨si , . . . , sj−1 ⟩ and S[i . . .] =
however, that any method for constructing an FSM                       ⟨si , . . .⟩ are slicing operations that return subse-
would suffice. We next give an overview of how our                     quences of observations following time step i.
approach evaluates formulas, with a more detailed                         Informally, the above rules operate as one might
background of LTL provided in Appendix A.1.                            expect. (next a b c . . . ) specifies that a must
   In this work, the formula is evaluated over a                       hold, then b, then c, etc. Similarly, (until a b)
finite sequence of states, where each state is taken                   specifies that a must hold (and may loop indef-
from the list of states provided in :states. In the                    initely) until b holds. Lastly, (or a b c . . . )
following, the letters after the logical operator (e.g.,               requires that any of a, b, c, etc. hold. Despite the
a, b, and c) will denote arguments, i.e., formulas or                  simplicity of the above representation, we find it
states, and let S = ⟨s0 , s1 , . . .⟩ denote the sequence              to be sufficient to represent a range of agents. We
   1
     Here we refer to the “environment” as any provider of             refer back to Figures 2 and 3 for ReACT, with ex-
text that is not the LLM (e.g., external tools, API calls, etc.)       amples of other agents provided in Appendix A.1.

                                                                   3
                                                             3). When text is produced by the environment, it is
                                                             treated in the same way as if it were produced by
                                                             the LLM. In both cases, the chunk of text is then
                                                             passed to decoding monitor for validation.

                                                             2.2.2    Validation
                                                             Text received from generation is first parsed and
                                                             separated into a sequence of states paired with
                                                             their corresponding content, i.e., S = ⟨⟨si , ti ⟩ , . . .⟩,
                                                             with separation dividing the text by occurrences of
                                                             the prompts associated with any of the agent’s spec-
                                                             ification’s states (regardless of whether the state re-
                                                             flects a valid transition). Splitting on prompt strings
                                                             thus serves as the state transition function δ, where
                                                             one must be sure that the prompts for each state are
                                                             not otherwise commonly occurring strings.
                                                                With S in hand, the decoding monitor (con-
                                                             structed from the specification’s behavior) walks
                                                             through each pair ⟨si , ti ⟩ to both update its current
                                                             state as well as validate the correctness of state
            Figure 4: Agent generation loop                  transitions. When it detects a state transition error,
                                                             i.e., when si does not follow from si−1 according
                                                             to the specification’s behavior or si is not given,
2.2     Constraining Agent Behavior                          the text following the invalid state or state content
Agents in our framework begin generation like any            is discarded, and the remaining subsequence of S
other prompting approach. First, the agent is pro-           is passed to the correction module.
vided with the input prompt, which consists of in-
structions, (optionally) a number of examples, and           2.2.3    Correction
the prompt text t0 associated with the initial state         The correction module will be passed the sequence
s0 (e.g., “[Question]” for the agent of Figure 3).           S = ⟨⟨si , ti ⟩ , . . .⟩ from before that has been trun-
At this point, the agent is considered to be in state        cated to remove all text beyond the first violation
s0 and must transition between states according to           of the specification. It takes the truncated text and
the behavior prescribed by its logical formula. For          applies a correction, then returns the new string to
the remainder of generation, the agent operates in a         the LLM to resume generation. The difficulty with
loop that alternates between generation, validation,         this step is to apply a correction that meaningfully
and correction, until the the agent reaches the final        changes what the LLM generates next while also
state send , at which point a termination signal halts       not imposing a hard constraint on the LLM.
generation. Figure 4 provides a diagram illustrating            To correct a state transition error (e.g., the LLM
our system’s process, which we next describe.                produced “[Thought]” instead of “[Action]”), the
                                                             correction module employs valid state prefixing.
2.2.1    Generation                                          Taking the last observed state in S as the last cor-
Depending on the current state of the agent, text            rect state, we define the set of next valid states to
will be produced by either the underlying LLM of             be the states that can be transitioned to according
the agent or by the environment (e.g., the result of         to the agent’s behavior. Valid state prefixing takes
an API call). When text must be produced by the              the longest common prefix of the prompt texts for
LLM, the agent’s LLM is prompted with all his-               each state within the set of next valid states and
torical context concatenated with all text produced          appends that prefix to the string to be returned to
thus far. It then generates text until either a stop         the LLM. For instance, for “[Action]” and “[Ac-
sequence is output or a pre-specified chunk size             tion Input]”, the longest common prefix would be
is reached. In this work, stop sequences are the             “[Action”, while for “[Action]” and “[Thought]”, it
prompt texts for any state that must be produced by          would be “[”. Once the longest common prefix is
the environment (e.g., “[Observation]” in Figure             determined, the correction module returns the trun-

                                                         4
    (define pass-agent
       (:states
         (Ques (:text "[Question]"))
         (Plan (:text "[Thought]"))
         (Act (:text "[Action]"))
         (Act-Inp (:text "[Action Input]"))
         (Sum (:text "[Summary]")
                 (:flags :env-input))
         (Final-Tht (:text "[Final Thought]"))
         (Ans (:text "[Answer]")))


       (:behavior                                                  Figure 6: State diagram of PASS agent architecture
         (next
            Ques
            (until                                               those actions are summarized by an LLM before
              (next                                              being returned to the agent (i.e., Summarize in Fig-
                 Plan                                            ure 6). This loop continues until the agent believes
                 (until                                          it can solve the problem, at which point it exits
                    (next Act Act-Inp)                           the planning loop and writes its final solution (i.e.,
                    Sum))                                        Final Thought and Answer in Figure 6).
              Final-Tht)                                            The summarization step takes as input the orig-
            Ans)))                                               inal question, the subgoal to be solved, and the
                                                                 result of each action that was executed (in a list
                                                                 format). It then uses the same LLM that powers the
Figure 5: Specification for PASS agent that that itera-
                                                                 agent to produce a summary of the action results
tively aggregates sets of actions, executes them in paral-
lel, and then summarizes their output                            with respect to the question and subgoal. Once
                                                                 the summary has been generated, the summariza-
                                                                 tion step must decide whether it is best to return
cated original text (i.e., all text occurring before the         the generated summary or the raw action results to
detected error) concatenated with this prefix.                   the agent. Letting x be the LLM context thus far,
                                                                 s be the summarization, and o be the original ac-
3   The PASS Agent Architecture                                  tion results concatenated into a list, then the output
                                                                 returned to the PASS agent is
In addition to implementing several existing agents
(see Appendix A.3), we also introduce a new                                 |y|
agent, referred to as the Plan-Act-Summarize-
                                                                            X                                      (5 + |y|)α
                                                                 arg max          log p(yi |x, y1 , . . . , yi−1 )
Solve (PASS) agent. PASS is a hybrid between the                  y∈{s,o}                                            (5 + 1)α
                                                                             i
entirely sequential ReACT (Yao et al., 2022) and
the entirely parallel ReWOO (Xu et al., 2023b) that              where p(y|x) is computed by the same LLM pow-
is designed to address both of their deficiencies. In            ering the agent and the score is length-normalized
Figures 5 and 6, we provide both the specification               (Wu et al., 2016; Murray and Chiang, 2018).
and finite-state diagram for the PASS agent.                        In this work, the summarization step is intended
   At a high level, PASS operates in a loop that                 to serve two purposes. First, when the summa-
alternates between action execution and summa-                   rization is returned, it can consolidate a poten-
rization. Each iteration of the main loop begins                 tially large amount of information into a concise
with a planning step (i.e., Plan in Figure 6), where             summary which (ideally) excludes extraneous de-
the LLM writes out the series of actions it believes             tails that are unhelpful with respect to the origi-
must be executed (i.e., Action and Action Input                  nal prompt. Second, the summarization step pro-
in Figure 6). Then, the LLM aggregates a set of                  vides the agent with action results that are most in
independent actions that can be executed simulta-                line with the distribution of the underlying model
neously in service of the previously written plan.               (whether that be the raw action results or the sum-
The set of actions is executed, and the results of               marization). That is, rather than the agent’s LLM

                                                             5
    Statements: Arthur’s Magazine (1844-1846)
                                                             framework, see Section 3). In addition, following
    was an American periodical published in
                                                             (Yao et al., 2022), we tested the complimentarity
    Philadelphia in the 19th century.
                                                             of agent and non-agent-based approaches. For this,
    First for Women is a woman’s magazine
                                                             questions were first attempted by the non-agent ap-
    published by Bauer Media Group in the
                                                             proaches (i.e., Direct / CoT). Then, if no answer
    USA.[1] The magazine was started in 1989.
                                                             was repeated after k = 5 self-consistency attempts,
    Context: Which magazine was started first
                                                             the agent-based approach was used to produce an
    Arthur’s Magazine or First for Women?
                                                             answer. In the tables, these results will be indicated
    Goal: I need to search Arthur’s Magazine
                                                             with [Non-Agent] → [Agent].
    and First for Women, and find which was                     We evaluated these approaches on three standard
    started first.                                           datasets: 1) GSM8K (Cobbe et al., 2021), a math-
    Summary:    Arthur’s Magazine started in                 ematical reasoning dataset that tests the ability of
    1844 and First for Women started in 1989                 a system to solve grade school math word prob-
                                                             lems, 2) HotpotQA (Yang et al., 2018), a multi-hop
                                                             question-answering dataset that requires reason-
Figure 7: Example of inputs (i.e., Statements,               ing over passages from Wikipedia, and 3) Trivi-
Context, and Goal) and output (i.e., Summary) for the        aQA (Joshi et al., 2017), a challenging, question-
summarization step. The summarization LLM was                answering dataset with compositional questions.
called for the actions Search[Arthur’s Magazine]
and Search[First for Women]                                     Where possible, we follow the methodology of
                                                             prior agent-based works in terms of datasets and
                                                             hyperparameters (see also, Appendix A.2), with
incorporating text from arbitrary sources into its           prompts taken from (Xu et al., 2023b). Like (Yao
generation process, it instead incorporates text pro-        et al., 2022; Xu et al., 2023b), we do not use the
duced by an identical LLM (assuming the summa-               annotated Wikipedia passages for HotpotQA or
rization model is the same as the agent’s LLM). In           TriviaQA and instead have the agent choose what
Figure 7, we provide an example of the summariza-            terms to search in Wikipedia. To mitigate the
tion LLM’s input and output.                                 cost involved with running large models across a
   The aggregation of a set of actions to take differ-       large number of experiments, we follow (Xu et al.,
entiates PASS from ReACT, which executes actions             2023b; Shinn et al., 2023; Liu et al., 2023; Yao
one by one in sequence. Thus, it can be considered           et al., 2022) for the larger datasets and select a ran-
the extension of ReACT to partially ordered ac-              dom subset of questions from their development
tion spaces. The advantage of this approach is that,         set for evaluation. For HotpotQA and TriviaQA we
like ReWOO, it reduces costly action execution               select a random subset of 1000 questions from the
steps that require the agent to suspend the LLM.             development set for evaluation, while for GSM8K
Unlike ReWOO, however, which cannot leverage                 we keep the full test set for evaluation.
the result of an action to influence how it gener-              In all experiments, we used Llama-2-70b (Tou-
ates subsequent actions (as ReWOO writes out all             vron et al., 2023) as the LLM powering our agents.
actions prior to execution), our approach can incor-         All systems had access to the same tools: 1)
porate feedback from executed actions in its gen-            Calculator for GSM8K, which executes an in-
eration process. This can be advantageous when               put formula and returns a number, 2) Search for
incorrect action calls are possible (e.g., executing a       HotpotQA and TriviaQA, which returns the first
Wikipedia search with the wrong article title).              sentences of the Wikipedia page for the entity if
                                                             it exists, or returns the most similar entities with
4   Experiments                                              Wikipedia pages, 3) Lookup for HotpotQA and
                                                             TriviaQA, which returns the next sentence contain-
To demonstrate our framework, we implemented                 ing the input string in the last page searched for.
five prompting approaches: 1) Self-consistency
alone (Direct), i.e., where the model immediately            5   Results
responds with an answer (Wang et al., 2022),
2) Chain-of-Thought with self-consistency (CoT)              In Table 1 we provide the results for all three
(Wei et al., 2022), 3) ReACT (Yao et al., 2022),             datasets. We again note that all agents were im-
4) ReWOO (Xu et al., 2023b), and 5) PASS (our                plemented and evaluated in our framework. While

                                                         6
  Method               HotpotQA   GSM8K     TriviaQA
                                                                  [Question] Who was born first,           Yanka
  Direct                 29.3       15.8      74.4                Dyagileva or Alexander Bashlachev?
  CoT (Wei et al.)       35.0       64.6      69.4
                                                                  [Thought] I need to search Yanka Dyagileva
  ReACT (Yao et al.)     28.7       53.8      44.1                and     Alexander   Bashlachev,   find   their
  ReWOO (Xu et al.)      27.0       51.9      52.4
  PASS (ours)            34.7       53.2      57.8                birth years, then find which was born
  Direct → ReACT         33.1       33.3      75.3                first.
  Direct → ReWOO         31.3       32.6      75.4                [Action] Search
  Direct → PASS          33.3       33.1      75.9                [Action Input] Yanka Dyagileva
  CoT → ReACT            37.8       65.3      71.4
  CoT → ReWOO            37.0       65.6      71.6                [Action] Search
  CoT → PASS             38.5       64.7      72.6                [Action Input] Alexander Bashlachev
                                                                  [Summary] Yanka Dyagileva was born in 1966
Table 1: Exact-match accuracy (%) results for alterna-            while Alexander Bashlachev was born in
tive prompting types across datasets. The best results            1960.
in all three groups (agent-based, non-agent-based, and
                                                                  [Final Thought] 1960 (Alexander
hybrid) are bolded
                                                                  Bashlachev) < 1966 (Yanka Dyagileva), so
                                                                  Alexander Bashlachev was born first.
  Agent                HotpotQA   GSM8K     TriviaQA
                                                                  [Answer] Alexander Bashlachev
  ReACT (Yao et al.)     28.7       53.8      44.1
  ReWOO (Xu et al.)      27.0       51.9      52.4
  PASS                   34.7       53.2      57.8            Figure 8: Example of text output by PASS agent for a
   - No Summarizer       25.7       53.8      45.2            question from the HotpotQA dataset

Table 2: Exact-match accuracy (%) ablation results for
PASS architecture with / without the summarization step

                                                              and TriviaQA while underperforming as compared
a perfect comparison to prior work is difficult to            to ReACT for GSM8K. We provide an example
achieve, as each of (Yao et al., 2022; Xu et al.,             of PASS output in Figure 8 for the HotpotQA
2023b; Shinn et al., 2023; Liu et al., 2023) evaluate         dataset. We suspected the summarization step
on different subsets of each dataset and use differ-          to have played a key role in the performance of
ent underlying models (e.g., GPT-3.5 (Brown et al.,           PASS. Thus, we ran an ablation experiment with the
2020), PaLM (Chowdhery et al., 2022)), our results            PASS agent where the summarization model was
are consistent in terms of trends with the findings           removed. In this setting, the results of all actions
of (Xu et al., 2023b; Yao et al., 2022). In (Xu et al.,       were instead put into a numbered list and returned
2023b), ReWOO was demonstrated to outperform                  to the agent unmodified.
ReACT on TriviaQA (51.8% versus 47.4% in their
work) and underperform on HotpotQA (30.4% ver-                   Table 2 shows the results of the ablation exper-
sus 32.2%). Lastly, like (Yao et al., 2022) and               iment. In the table, we see that, for HotpotQA
(Xu et al., 2023b), we observed chain-of-thought              and TriviaQA, the use of summarization boosted
(Wei et al., 2022) and direct response to be more             performance. This could be due to the search and
effective than agent-based works.                             lookup tools often returning very information dense
   In addition to individual methods, Table 1 also            results (i.e., raw Wikipedia text) that contain ex-
shows how well the agent approaches compli-                   traneous information. In contrast, for GSM8K the
mented the non-agent-based approaches. As shown               summarization LLM negatively impacted results.
in the table, hybrid systems (i.e., non-agent systems         In GSM8K, the only tool available was a calcula-
that used agents as a fallback prediction) resulted           tor that returned numeric values. We believe that,
in the top performances across all datasets, with the         because there was little to summarize, the LLM
best results being produced by non-agent methods              could not provide enough value to offset any er-
combined with our PASS agent. This suggests there             rors it would make from introduced hallucinations.
to be complimentary between these two distinct                These results suggest that summarization can be a
response paradigms.                                           very valuable addition to a tool-augmented agent,
   Among the agent-based systems, we see that                 however, it should only be applied when the raw
our PASS agent performed the best on HotpotQA                 results of tool calls are likely to derail the agent.

                                                          7
6     Related Work                                         A key point of differentiation with their approach
                                                           is that it utilized eager enforcement of constraints
6.1    LLM-Based Agents                                    (e.g., when used to implement the ReACT agent,
Various LLM-based agents targeting different tasks         their approach halted decoding at each individual
have been proposed. Among them, WebAgent (Gur              state). While this allowed them to capture a much
et al., 2023) demonstrates language-based agents           larger range of constraints and behaviors, it also
capable of executing tasks on websites by adher-           leads to costly reprompting (see (Xu et al., 2023b)).
ing to natural language commands. Relatedly, the
Generative Agents (Park et al., 2023) work aims            6.2    Constrained Decoding
to simulate believable human behavior, and Say-            Conceptually related to our work are constrained
Can (Ahn et al., 2022) illustrates the capability to       generation methods that modify the standard beam
use LLMs in embodied agents. These agents are              search decoding procedure at inference time, to
intended for a particular purpose, and thus are less       incorporate constraints in the output (Wiseman and
related to this work than those that can be tailored       Rush, 2016; Wuebker et al., 2016; Anderson et al.,
to solve a wider range of tasks, e.g., ReACT (Yao          2017a; Lu et al., 2022; Hokamp and Liu, 2017; Post
et al., 2022), Reflexion (Shinn et al., 2023), Re-         and Vilar, 2018). While these works focus one level
WOO (Xu et al., 2023b).                                    lower than our work in that they go directly into the
   Several open-source projects have also centered         decoder to modify its outputs, such methods could
on agent creation, e.g., AutoGPT (Gravitas, 2023)          be used to implement controls within our approach
and BabyAGI (Nakajima, 2023). These works have             if we were to instead rely on locally hosted models.
focused on constructing self-sufficient agents that           Of particular note, (Anderson et al., 2017b) pro-
fulfil user requests, which differs from our frame-        poses a constrained beam search algorithm that
work wherein the user defines task-specific individ-       keeps track of constraints via a finite-state machine,
ual agents for their specific purposes.                    and demonstrates its benefits on several image cap-
   There have been several multi-agent orchestra-          tioning tasks. The NEUROLOGIC DECODING line
tion frameworks that have been recently introduced,        of work (Lu et al., 2021, 2022) enforces the sat-
e.g., BOLAA (Liu et al., 2023), MetaGPT (Hong              isfaction of lexical constraints (specified as any
et al., 2023), Gentopia (Xu et al., 2023a), and Au-        predicate logic formula having word inclusion and
toGen (Wu et al., 2023). These frameworks focus            exclusion constraints) via adding a penalty term for
primarily on the related problem of orchestrating          constraint violation in the beam search decoding
multiple, simple LLM-based agents to achieve com-          algorithm. (Bastan et al., 2023) builds on top of
plex goals, where the individual agents themselves         NEUROLOGIC DECODING by incorporating struc-
are generally no more complex than ReACT or Re-            tural constraints that capture dependency parsing
WOO. This differs from our focus of designing,             information. Lastly, both the FUDGE (Yang and
implementing, and validating complex individual            Klein, 2021) and NADO (Meng et al., 2022) works
agents (however, we suspect our work would syn-            propose the use of auxillary models that have been
ergize well with such approaches).                         trained to recognize constraint-satisfying outputs
   Most conceptually similar to our approach are           as a means of controlling a base model (e.g., pre-
the works of (Harrison, 2022) and (Beurer-Kellner          trained LLM) for generation.
et al., 2023). LangChain (Harrison, 2022) is a pop-
ular framework for designing LLM-based applica-            7     Conclusion
tions that has some support for implementing LLM-
based agents. However, their approach does not             In this work, we introduced a high-level, declar-
guarantee conformance to the user’s desired behav-         ative framework for defining LLM-based agents.
ior, relying almost entirely on prompting to encour-       We implemented a number of well-known agent
age models to follow the expected behavior. The            types with our framework, and went further to in-
work of (Beurer-Kellner et al., 2023) introduced           troduce PASS, a new agent architecture that takes
a scripting language for LLMs based on prompt-             advantage of the declarative nature of our frame-
ing. Their approach did not focus exclusively on           work. Lastly, we compared its performance to other
LLM-based agents, instead more broadly consider-           agents across three standard datasets and found it to
ing the problem of interleaving LLM outputs into           be strong-performing with complimentary abilities
complex, programmatically defined text templates.          to non-agent-based prompting approaches.

                                                       8
References                                                      Significant Gravitas. 2023. Autogpt. https://agpt.
                                                                  co.
Michael Ahn, Anthony Brohan, Noah Brown, Yevgen
  Chebotar, Omar Cortes, Byron David, Chelsea Finn,             Izzeddin Gur, Hiroki Furuta, Austin Huang, Mustafa
  Chuyuan Fu, Keerthana Gopalakrishnan, Karol Haus-                Safdari, Yutaka Matsuo, Douglas Eck, and Aleksan-
  man, et al. 2022. Do as i can, not as i say: Ground-             dra Faust. 2023. A real-world webagent with plan-
  ing language in robotic affordances. arXiv preprint              ning, long context understanding, and program syn-
  arXiv:2204.01691.                                                thesis. arXiv preprint arXiv:2307.12856.

Peter Anderson, Basura Fernando, Mark Johnson, and              Chase Harrison. 2022. Langchain. https://github.
  Stephen Gould. 2017a. Guided open vocabulary im-                com/langchain-ai/langchain.
  age captioning with constrained beam search. In
                                                                Chris Hokamp and Qun Liu. 2017. Lexically con-
  Proceedings of the 2017 Conference on Empirical
                                                                  strained decoding for sequence generation using grid
  Methods in Natural Language Processing, pages 936–
                                                                  beam search. In Proceedings of the 55th Annual
  945, Copenhagen, Denmark. Association for Compu-
                                                                  Meeting of the Association for Computational Lin-
  tational Linguistics.
                                                                  guistics (Volume 1: Long Papers), pages 1535–1546.
Peter Anderson, Basura Fernando, Mark Johnson, and              Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng
  Stephen Gould. 2017b. Guided open vocabulary im-                 Cheng, Ceyao Zhang, Zili Wang, Steven Ka Shing
  age captioning with constrained beam search. In                  Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, et al.
  Proceedings of the 2017 Conference on Empirical                  2023. Metagpt: Meta programming for multi-
  Methods in Natural Language Processing, pages 936–               agent collaborative framework. arXiv preprint
  945.                                                             arXiv:2308.00352.
Christel Baier and Joost-Pieter Katoen. 2008. Principles        Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke
  of model checking. MIT press.                                  Zettlemoyer. 2017. TriviaQA: A large scale distantly
                                                                 supervised challenge dataset for reading comprehen-
Mohaddeseh Bastan, Mihai Surdeanu, and Niranjan Bal-             sion. In Proceedings of the 55th Annual Meeting of
 asubramanian. 2023. Neurostructural decoding: Neu-              the Association for Computational Linguistics (Vol-
 ral text generation with structural constraints. In             ume 1: Long Papers), pages 1601–1611, Vancouver,
 Proceedings of the 61st Annual Meeting of the As-               Canada. Association for Computational Linguistics.
 sociation for Computational Linguistics (Volume 1:
 Long Papers), pages 9496–9510.                                 Zhiwei Liu, Weiran Yao, Jianguo Zhang, Le Xue,
                                                                  Shelby Heinecke, Rithesh Murthy, Yihao Feng,
Luca Beurer-Kellner, Marc Fischer, and Martin Vechev.             Zeyuan Chen, Juan Carlos Niebles, Devansh Arpit,
  2023. Prompting is programming: A query language                et al. 2023. Bolaa: Benchmarking and orchestrating
  for large language models. Proceedings of the ACM               llm-augmented autonomous agents. arXiv preprint
  on Programming Languages, 7(PLDI):1946–1969.                    arXiv:2308.05960.

Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol            Ximing Lu, Sean Welleck, Peter West, Liwei Jiang,
  Hausman, Alexander Herzog, Daniel Ho, Julian                    Jungo Kasai, Daniel Khashabi, Ronan Le Bras, Lian-
  Ibarz, Alex Irpan, Eric Jang, Ryan Julian, et al. 2023.         hui Qin, Youngjae Yu, Rowan Zellers, et al. 2022.
  Do as i can, not as i say: Grounding language in                Neurologic a* esque decoding: Constrained text gen-
  robotic affordances. In Conference on Robot Learn-              eration with lookahead heuristics. In Proceedings of
  ing, pages 287–318. PMLR.                                       the 2022 Conference of the North American Chap-
                                                                  ter of the Association for Computational Linguistics:
Tom Brown, Benjamin Mann, Nick Ryder, Melanie                     Human Language Technologies, pages 780–799.
  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind            Ximing Lu, Peter West, Rowan Zellers, Ronan Le Bras,
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda                Chandra Bhagavatula, and Yejin Choi. 2021. Neuro-
  Askell, et al. 2020. Language models are few-shot               logic decoding:(un) supervised neural text generation
  learners. Advances in neural information processing             with predicate logic constraints. In Proceedings of
  systems, 33:1877–1901.                                          the 2021 Conference of the North American Chap-
                                                                  ter of the Association for Computational Linguistics:
Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
                                                                  Human Language Technologies, pages 4288–4299.
  Maarten Bosma, Gaurav Mishra, Adam Roberts,
  Paul Barham, Hyung Won Chung, Charles Sutton,                 Tao Meng, Sidi Lu, Nanyun Peng, and Kai-Wei Chang.
  Sebastian Gehrmann, et al. 2022. Palm: Scaling                  2022. Controllable text generation with neurally-
  language modeling with pathways. arXiv preprint                 decomposed oracle. Advances in Neural Information
  arXiv:2204.02311.                                               Processing Systems, 35:28125–28139.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,                 Kenton Murray and David Chiang. 2018. Correcting
  Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias                  length bias in neural machine translation. In Proceed-
  Plappert, Jerry Tworek, Jacob Hilton, Reiichiro                 ings of the Third Conference on Machine Translation:
  Nakano, et al. 2021. Training verifiers to solve math           Research Papers, pages 212–223, Brussels, Belgium.
  word problems. arXiv preprint arXiv:2110.14168.                 Association for Computational Linguistics.


                                                            9
Y Nakajima. 2023. Task-driven autonomous agent                 Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le,
  utilizing gpt-4, pinecone, and langchain for di-               Ed H Chi, Sharan Narang, Aakanksha Chowdhery,
  verse applications.    See https://yoheinakajima.              and Denny Zhou. 2022. Self-consistency improves
  com/task-driven-autonomous-agent-utilizing-gpt-4-              chain of thought reasoning in language models. In
  pinecone-and-langchain-for-diverse-applications                The Eleventh International Conference on Learning
  (accessed 18 April 2023).                                      Representations.

Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,              Jason Wei, Maarten Bosma, Vincent Zhao, Kelvin Guu,
  Carroll Wainwright, Pamela Mishkin, Chong Zhang,                Adams Wei Yu, Brian Lester, Nan Du, Andrew M
  Sandhini Agarwal, Katarina Slama, Alex Ray, et al.              Dai, and Quoc V Le. 2021. Finetuned language mod-
  2022. Training language models to follow instruc-               els are zero-shot learners. In International Confer-
  tions with human feedback. Advances in Neural                   ence on Learning Representations.
  Information Processing Systems, 35:27730–27744.              Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
                                                                  Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
Joon Sung Park, Joseph C O’Brien, Carrie J Cai, Mered-
                                                                  et al. 2022. Chain-of-thought prompting elicits rea-
  ith Ringel Morris, Percy Liang, and Michael S
                                                                  soning in large language models. Advances in Neural
  Bernstein. 2023. Generative agents: Interactive
                                                                  Information Processing Systems, 35:24824–24837.
  simulacra of human behavior. arXiv preprint
  arXiv:2304.03442.                                            Sam Wiseman and Alexander M. Rush. 2016. Sequence-
                                                                 to-sequence learning as beam-search optimization.
Amir Pnueli. 1977. The temporal logic of programs. In            In Proceedings of the 2016 Conference on Empiri-
 18th Annual Symposium on Foundations of Computer                cal Methods in Natural Language Processing, pages
 Science (sfcs 1977), pages 46–57. ieee.                         1296–1306, Austin, Texas. Association for Computa-
                                                                 tional Linguistics.
Matt Post and David Vilar. 2018. Fast lexically con-
 strained decoding with dynamic beam allocation for            Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu,
 neural machine translation. In Proceedings of the               Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang,
 2018 Conference of the North American Chapter of                Xiaoyun Zhang, and Chi Wang. 2023. Auto-
 the Association for Computational Linguistics: Hu-              gen: Enabling next-gen llm applications via multi-
 man Language Technologies, Volume 1 (Long Pa-                   agent conversation framework. arXiv preprint
 pers), pages 1314–1324.                                         arXiv:2308.08155.

Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan            Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le,
  Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang,              Mohammad Norouzi, Wolfgang Macherey, Maxim
  Bill Qian, et al. 2023. Toolllm: Facilitating large            Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al.
  language models to master 16000+ real-world apis.              2016. Google’s neural machine translation system:
  arXiv preprint arXiv:2307.16789.                               Bridging the gap between human and machine trans-
                                                                 lation. arXiv preprint arXiv:1609.08144.
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta
  Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola             Joern Wuebker, Spence Green, John DeNero, Saša
  Cancedda, and Thomas Scialom. 2023. Toolformer:                Hasan, and Minh-Thang Luong. 2016. Models and
  Language models can teach themselves to use tools.             inference for prefix-constrained machine translation.
  arXiv preprint arXiv:2302.04761.                               In Proceedings of the 54th Annual Meeting of the
                                                                 Association for Computational Linguistics (Volume
Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li,               1: Long Papers), pages 66–75, Berlin, Germany. As-
  Weiming Lu, and Yueting Zhuang. 2023. Hugging-                 sociation for Computational Linguistics.
  gpt: Solving ai tasks with chatgpt and its friends in        Binfeng Xu, Xukun Liu, Hua Shen, Zeyu Han, Yuhan
  huggingface. arXiv preprint arXiv:2303.17580.                  Li, Murong Yue, Zhiyuan Peng, Yuchen Liu, Ziyu
                                                                 Yao, and Dongkuan Xu. 2023a. Gentopia.AI: A col-
Noah Shinn, Beck Labash, and Ashwin Gopinath.
                                                                 laborative platform for tool-augmented LLMs. In
  2023. Reflexion: an autonomous agent with dy-
                                                                 Proceedings of the 2023 Conference on Empirical
  namic memory and self-reflection. arXiv preprint
                                                                 Methods in Natural Language Processing: System
  arXiv:2303.11366.
                                                                 Demonstrations, pages 237–245, Singapore. Associa-
Qiaoyu Tang, Ziliang Deng, Hongyu Lin, Xianpei Han,              tion for Computational Linguistics.
  Qiao Liang, and Le Sun. 2023. Toolalpaca: Gener-             Binfeng Xu, Zhiyuan Peng, Bowen Lei, Subhabrata
  alized tool learning for language models with 3000             Mukherjee, Yuchen Liu, and Dongkuan Xu. 2023b.
  simulated cases. arXiv preprint arXiv:2306.05301.              Rewoo: Decoupling reasoning from observations for
                                                                 efficient augmented language models. arXiv preprint
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-               arXiv:2305.18323.
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti           Kevin Yang and Dan Klein. 2021. Fudge: Controlled
  Bhosale, et al. 2023. Llama 2: Open founda-                    text generation with future discriminators. In Pro-
  tion and fine-tuned chat models. arXiv preprint                ceedings of the 2021 Conference of the North Amer-
  arXiv:2307.09288.                                              ican Chapter of the Association for Computational


                                                          10
  Linguistics: Human Language Technologies, pages            A     Appendix
  3511–3535.
                                                             A.1    Linear Temporal Logic
Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio,
  William Cohen, Ruslan Salakhutdinov, and Christo-          Here we provide a light overview of linear tem-
  pher D Manning. 2018. Hotpotqa: A dataset for              poral logic (LTL), which is used in our agent
  diverse, explainable multi-hop question answering.         specification framework. LTL is a modal tempo-
  In Proceedings of the 2018 Conference on Empiri-           ral logic originally introduced for formal verifica-
  cal Methods in Natural Language Processing, pages
  2369–2380.                                                 tion (Pnueli, 1977) that extends propositional logic
                                                             with the temporal operators ⃝ (next) and U (until).
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak             The two operators have intuitive definitions, with
  Shafran, Karthik R Narasimhan, and Yuan Cao. 2022.
  React: Synergizing reasoning and acting in language        ⃝ (next) being a unary operator that (informally)
  models. In The Eleventh International Conference           means a formula φ must hold in the next time step,
  on Learning Representations.                               and U (until) being a binary operator that speci-
                                                             fies a formula φi must be true until φj becomes
                                                             true. LTL formulas are defined over a set of atomic
                                                             propositions P with their syntax given by

                                                             φ ::= true       p   ¬φ     φ1 ∧φ2      ⃝φ       φ1 Uφ2

                                                             where p ∈ P. An LTL formula is evaluated over
                                                             an infinite sequence of observations, where each
                                                             observation is a truth assignment over symbols in P.
                                                             Letting φ be a LTL formula and σ be the sequence
                                                             of observations σ = ⟨σ1 , σ2 , . . .⟩, where each σi
                                                             can be considered the subset of P that is true at
                                                             time i, then we write σ |= φ (satisfies) when

                                                             σ     |=     true
                                                             σ     |=     p            iff p ∈ σ0
                                                             σ     |=     ¬φ           iff σ ̸|= φ
                                                             σ     |=     φ1 ∧ φ2      iff σ |= φ1 and σ |= φ2
                                                             σ     |=     ⃝φ           iff σ[1 . . .] |= φ
                                                             σ     |=     φ1 U φ2      iff ∃j ≥ 0. σ[j . . .] |= φ2
                                                                                       and σ[i . . .] |= φ1
                                                                                       for all 0 ≤ i < j

                                                             where σ[i . . .] = ⟨σi , . . .⟩ is the remaining se-
                                                             quence of observations following time step i. From
                                                             the operators listed above, we can define additional
                                                             propositional logic operators ∨ (disjunction), and
                                                             → (implication) as well as temporal operators ♢
                                                             (eventually) and □ (always)

                                                                        φ1 ∨ φ2     :=      ¬(¬φ1 ∧ ¬φ2 )
                                                                        φ1 → φ2     :=      ¬φ1 ∨ φ2
                                                                        ♢φ          :=      true U φ
                                                                        □φ          :=      ¬ ♢ ¬φ

                                                             In this work, we treat next as an n-ary operator,
                                                             which can be considered simply a chained sequence
                                                             of next operators, i.e., ⃝(φ1 , φ2 , φ3 , . . .) with the

                                                        11
                                                                  (define react-agent
                                                                    (:states
                                                                      (Ques (:text "[Question]"))
                                                                      (Tht (:text "[Thought]"))
                                                                      (Act (:text "[Action]"))
                                                                      (Act-Inp (:text "[Action Input]"))
                                                                      (Obs (:text "[Observation]")
                                                                            (:flags :env-input))
                                                                      (Final-Tht (:text "[Final Thought]"))
                                                                      (Ans (:text "[Answer]")))


                                                                    (:behavior
                                                                      (next
                                                                         Ques
                                                                         (until
                                                                           (next Tht Act Act-Inp Obs)
Figure 9: Examples of truth assignments over time with
                                                                           Final-Tht)
various LTL operators
                                                                         Ans)))


straightforward informal interpretation of “φ1 then
φ2 then φ3 ”, etc.. In Figure 9, we provide a graphi-         Figure 10: Specification for ReACT agent (Yao et al.,
                                                              2022)
cal depiction of the truth assignments over time for
the above temporal operators.
   In this work, we found that only allowing for-
mulas to be those containing atomic propositions
p, as well as operators →, ⃝, □, and U (i.e., we
do not allow formulas to include ¬, ∧, etc.) was
sufficient to represent the range of existing agent               (define rewoo-agent
architectures. We leave extending the set of opera-                 (:states
tors (e.g., to include ♢, ∧, etc.) to future work. For                (Ques (:text "[Question]"))
more details regarding LTL and its numerous ap-                       (Plan (:text "[Plan]"))
plications, we direct the interested reader to (Baier                 (Act-Lbl (:text "[Action Label]"))
and Katoen, 2008).                                                    (Act (:text "[Action]"))
                                                                      (Act-Inp (:text "[Action Input]"))
A.2   Hyperparameters and Hardware
                                                                      (Solver (:text "[Answer]")
There were not many hyperparameters to our ap-                                  (:flags :env-input)))
proach beyond those listed in the experiments sec-
tion, as our LLMs were only used for inference.                     (:behavior
The decoding strategy for our LLMs was set to                         (next
greedy in all cases except for approaches which                          Ques
used self-consistency (i.e., Direct, CoT). For self-                     (until
consistency, the temperature for sampling was set                          (next Plan Act-Lbl Act Act-Inp)
to 0.7 (as in (Yao et al., 2022)) and k = 5 samples                        Solver))))
were drawn.

A.3   Agent Definitions                                       Figure 11: Specification for ReWOO agent (Xu et al.,
                                                              2023b)




                                                         12
   (define reflexion-agent
     (:states
       (Ques (:text "[Question]"))
       (Tht (:text "[Thought]"))
       (Act (:text "[Action]"))
       (Act-Inp (:text "[Action Input]"))
       (Obs (:text "[Observation]")
               (:flags :env-input))
       (Final-Tht (:text "[Final Thought]"))
       (Prop-Ans (:text "[Proposed Answer]"))
       (Eval (:text "[Evaluation]")
               (:flags :env-input))
       (Ref (:text "[Reflection]"))
       (Ans (:text "[Answer]")))


     (:behavior
       (next
         Ques
         (until
                                                               (define direct-agent
            (next
                                                                  (:states
               (until
                                                                    (Ques (:text "[Question]"))
                  (next Tht Act Act-Inp Obs)
                                                                    (Ans (:text "[Answer]")))
                  Final-Tht)
               Prop-Ans
                                                                  (:behavior
               Eval
                                                                    (next Ques Ans)))
               Ref)
            Ans))))
                                                           Figure 14: Specification for direct response agent (i.e.,
                                                           outputs only answer)
Figure 12: Specification for Reflexion agent (Shinn
et al., 2023)




    (define cot-agent
      (:states
        (Ques (:text "[Question]"))
        (Tht (:text "[Thought]"))
        (Ans (:text "[Answer]")))


      (:behavior
        (next Ques Tht Ans)))



Figure 13: Specification for Chain-of-thought agent
(Wei et al., 2022)




                                                      13
