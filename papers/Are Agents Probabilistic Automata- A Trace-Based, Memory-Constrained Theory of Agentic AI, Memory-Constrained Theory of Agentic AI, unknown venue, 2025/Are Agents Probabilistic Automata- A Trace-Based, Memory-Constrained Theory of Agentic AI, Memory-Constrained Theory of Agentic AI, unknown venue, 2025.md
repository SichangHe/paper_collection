                                                         Are Agents Probabilistic Automata? A Trace-Based,
                                                             Memory-Constrained Theory of Agentic AI
                                                                    Roham Koohestani†‡ , Ziyou Li‡ Anton Podkopaev†§ , Maliheh Izadi‡
                                                                 † JetBrains Research, Amsterdam, the Netherlands      ‡ Delft University of Technology, Delft, the Netherlands
                                                                                                 § Constructor University, Bremen, Germany


                                         Abstract                                                                          the closed loop induces a probability distribution over traces; af-
                                         This paper studies standard controller architectures for agentic AI               ter abstraction, this yields a finite probabilistic transition model (a
                                         and derives automata-theoretic models of their interaction behavior               Markov chain or MDP) for bounded-memory controllers and push-
                                         via trace semantics and abstraction. We model an agent implemen-                  down/recursive probabilistic models for stack-scoped controllers.
                                         tation as a finite control program augmented with explicit memory                    Goal and Contribution: This work bridges agent engineering
arXiv:2510.23487v2 [cs.AI] 30 Jan 2026




                                         primitives (bounded buffers, a call stack, or read/write external                 practice and automata-theoretic reasoning by focusing on architec-
                                         memory) and a stochastic policy component (e.g., an LLM) that                     tural constraints that are auditable at the framework level. Our con-
                                         selects among architecturally permitted actions. Instead of equat-                tributions are: (1) A trace-centric classification: we define agent
                                         ing the concrete agent with a deterministic acceptor, we treat the                classes in terms of enforced persistent memory operations (finite-
                                         agent-environment closed loop as inducing a probability distribu-                 state, stack-scoped, or unbounded read/write memory) and based
                                         tion over finite interaction traces. Given an abstraction function                on the produced traces of the agents. (2) A right-sizing guideline:
                                         𝛼 from concrete configurations to a finite abstract state space, we               we provide a decision procedure at the architecture level for select-
                                         obtain a probabilistic trace language and an abstract probabilistic               ing the weakest controller class consistent with task requirements.
                                         transition model 𝑀𝛼 suitable for probabilistic model checking.                    (3) Research Roadmap: We outline a series of research paths to
                                            Imposing explicit, framework-auditable restrictions on memory                  explore which focus on formal verification and testing, as well as
                                         access and control flow, we prove that the support of the resulting               practical engineering issues related to right-sizing.
                                         trace language is regular for bounded-memory controllers, context-                   In the following section, we provide the necessary background
                                         free for strict call-return controllers, and recursively enumerable for           (section 2) and define our framework (section 3). Sections 4–6 estab-
                                         controllers equipped with unbounded read/write memory. These                      lish the correspondence between architectural memory constraints
                                         correspondences allow the reuse of existing verification methods                  and their respective automata classes. We extend these results to
                                         for finite-state and pushdown systems, and they delineate precisely               multi-agent systems in section 7. Finally, we operationalize this
                                         when undecidability barriers arise. The probabilistic semantics leads             theory into a right-sizing procedure (section 8) and a case study
                                         to quantitative analyses such as: what is the probability of entering             (section 9), concluding with a discussion in section 10.
                                         an unsafe abstract region, and how can we bound this probability
                                         in the presence of environment nondeterminism.                                    2    Background and Related Work
                                         ACM Reference Format:                                                             Agentic AI Architectures. Modern agentic AI systems are com-
                                          Roham Koohestani†‡ , Ziyou Li‡ Anton Podkopaev†§ , Maliheh Izadi‡ . .            posed of several key components that work in a continuous opera-
                                         Are Agents Probabilistic Automata? A Trace-Based, Memory-Constrained              tional loop. This loop, often a variant of the Sense-Plan-Act cycle,1
                                         Theory of Agentic AI. In Proceedings of . ACM, New York, NY, USA, 10 pages.       dictates how the agent interacts with its environment. Perception:
                                                                                                                           The agent takes in information from its environment, which could
                                         1    Introduction                                                                 be user input, sensor data, or the state of a software system. Rea-
                                         The rapid evolution of artificial intelligence has transitioned from re-          soning (LLM): Large Language Models (LLM) are often used as the
                                         active single-turn systems to proactive autonomous entities known                 brain of the agent. These are tasked with processing the perceived
                                         as agentic AI. These systems are designed to perceive their envi-                 information, maintaining a model of the world, and deciding on the
                                         ronment, formulate plans, and execute multi-step tasks using tools                next course of action. Action Layer: The agent executes actions
                                         to achieve goals with minimal human intervention [11]. Although                   through a set of available tools or APIs, which can modify the envi-
                                         often described in terms of cognitive capabilities like reasoning and             ronment or its internal state. Memory: This is the component that
                                         planning, many agent frameworks implement a control loop that                     stores information about past states, actions, and observations. The
                                         can be described as a labeled transition system once the environ-                 structure and capacity of this memory are central to our thesis.
                                         ment and tool interfaces are made explicit [23].                                     Operational loop variants like ReAct (Reason+Act) [26], State-
                                            This paper presents a framework that classifies agents by the per-             Flow [23], and SMOT (Step-wise Memory-augmented Task-oriented)
                                         sistent memory interfaces they enforce and by the resulting interac-              [14] all represent different strategies for managing this cycle, but
                                         tion traces. The classification has a qualitative layer and a quantita-           fundamentally operate as state-transition systems.
                                         tive layer. Qualitatively, under checkable architectural constraints,                Our classification targets the controller and its persistent mem-
                                         the support of the induced trace language is regular (bounded per-                ory interface. We assume tools are invoked through a finite action
                                         sistent memory), context-free (stack-scoped call-return), or recur-               alphabet Γ and that tool outputs are returned as perceptions via
                                         sively enumerable (unbounded read/write memory). Quantitatively,                  Σ after tokenization. While practical tool interfaces often accept
                                         ,                                                                                 1 E.g., https://motion.cs.illinois.edu/RoboticSystems/AnatomyOfARobot.html
,                                                                                      Roham Koohestani†‡ , Ziyou Li‡ Anton Podkopaev†§ , Maliheh Izadi‡


arguments from infinite domains (e.g., arbitrary text strings or real        Recursive and Pushdown Models. Hierarchical controllers
numbers), we assume for this structural classification that such          with call-return structure are naturally modeled by pushdown sys-
arguments are either discretized via an abstraction layer (e.g., treat-   tems. When probabilistic choices are present, one obtains proba-
ing all invalid inputs as a single symbol) or generated by the model      bilistic pushdown models, which can also be presented as recursive
(and are therefore finite. Unless stated otherwise, we treat tools and    stochastic transition systems. A representative formalization is via
the environment as nondeterministic but computable processes;             recursive Markov chains, where each procedure is a component
the classification does not claim to bound the computational power        with entry and exit nodes and control can invoke components re-
of external oracles, only the controller’s ability to store and reuse     cursively [9]. These models provide the standard bridge between (i)
information across steps.                                                 context-free control structure and (ii) quantitative reachability anal-
    Trace Semantics and Trace Languages. A standard way to                ysis. They are therefore the appropriate background for modeling
model interactive systems is as labeled transition systems, where         the quantitative behavior of stack-scoped agent controllers.
executions induce traces, that is, finite or infinite sequences of           Abstraction and Refinement. Direct verification of realis-
observable events [2]. Trace semantics is used as a linear-time ab-       tic controllers is limited by state explosion and by the need to
straction of behavior and supports property classes such as safety        model tools and environments at an appropriate level of detail.
(prefix-closed) and reachability. In controller-style agent architec-     Abstraction addresses this by mapping concrete configurations to
tures, an interaction trace can be taken as a sequence of (perception,    a finite abstract state space, and then verifying properties on the
action) pairs, or as a sequence of pre/post tool-invocation snap-         induced abstract model. For nondeterministic or probabilistic sys-
shots paired with tool calls, depending on the chosen observation         tems, abstraction must account for both sources of uncertainty,
interface. This paper uses traces as the semantic object for two rea-     and coarse abstractions can introduce spurious behaviors that do
sons. First, traces provide a uniform interface across heterogeneous      not correspond to any concrete execution. Counterexample-guided
agent frameworks whose internal control graphs and tool APIs dif-         abstraction refinement (CEGAR) is a standard methodology that
fer. Second, traces align with verification workflows that interpret a    iteratively refines abstractions using counterexamples produced
controller plus environment as generating a set (or distribution) of      by verification [3]. In probabilistic settings, counterexamples may
observable executions, and then check reachability-style properties       need to represent sets of traces or scheduler choices, and refinement
over those executions.                                                    may separate abstract states to eliminate spurious high-probability
    Probabilistic Transition Models for Stochastic Controllers.           paths [5].
When a controller’s policy is stochastic (for example, due to sam-           Formal Methods in AI Systems. The application of formal
pling in an LLM) and tools exhibit randomness or uncertainty, the         methods to AI is not new. Classical multi-agent systems have
closed-loop system induces a probability distribution over traces. A      been analyzed using model-checking tools like AJPF [7] and MC-
common modeling boundary separates (i) purely probabilistic evolu-        MAS [19]. In the context of LLMs, techniques such as grammar-
tion, represented by Markov chains, and (ii) mixed nondeterministic       constrained decoding [16], Linear Temporal Logic (LTL) moni-
and probabilistic evolution, represented by Markov decision pro-          tors [4], and frameworks like Formal-LLM [13] have been used
cesses (MDPs). MDPs model nondeterministic choices resolved by            to enforce certain properties on the output. However, a significant
a scheduler (or adversary) and probabilistic choices resolved by          gap remains: there is no unifying, memory-based classification that
transition probabilities [2, 17]. Another closely related formalism is    links the architectural patterns of modern agentic AI to the funda-
the probabilistic automaton model that combines nondeterminism            mental decidability and complexity results from automata theory.
with probabilistic transitions. In verification, this is often treated    This paper aims to fill that gap.
as an MDP-style transition system in which each state enables a
set of probability distributions over successors [20].                    3     A Formal Theory for Agentic AI
    These models match agent settings where tool outcomes are not         To develop a formal theory for agents, we must first define the
fully specified or where abstraction introduces uncertainty, while        standard automata for establishing equivalence. We subsequently
still supporting quantitative questions such as maximum probability       present our claims for equivalence.
of reaching an unsafe region.
    Probabilistic Model Checking. Probabilistic model checking
                                                                          3.1     Standard Automata Definitions
analyzes quantitative properties of Markov chains and MDPs, in-
cluding probabilities of reachability, expected accumulated costs,        The definitions that follow are standard in the theory of computa-
and temporal-logic specifications such as PCTL and related logics.        tion and are consistent with the established literature.
Algorithms for reachability in Markov chains reduce to solving                Finite Automaton (FA). is a 5-tuple 𝑀 = (𝑄, Σ𝑖𝑛 , 𝛿, 𝑞 0, 𝐹 ) where:
linear equations; for MDPs they reduce to fixed-point character-
izations that compute extrema over all schedulers [2]. Modern                   • 𝑄 is a finite set of states.
probabilistic model checkers implement these analyses and expose                • Σ𝑖𝑛 is a finite set of input symbols, called the alphabet.
multiple interpretations of nondeterminism (for example, worst-                 • 𝛿 : 𝑄 × Σ𝑖𝑛 → 𝑄 is the transition function.
case and best-case reachability). This paper’s abstraction-based                • 𝑞 0 ∈ 𝑄 is the start state.
modeling step is intended to produce precisely the kind of finite               • 𝐹 ⊆ 𝑄 is the set of accept states.
probabilistic model that these tools consume [6].                            A note on perceptions and finiteness. We model a controller
                                                                          step as consuming a single perception symbol 𝑎 ∈ Σ𝑖𝑛 produced
                                                                          by a tokenizer 𝜏 applied to raw observations. This abstracts away
Are Agents Probabilistic Automata? A Trace-Based, Memory-Constrained Theory of Agentic AI                                                                       ,


variable-length raw observations by treating tokenization and ob-                        Definition 3.3 (State abstraction and abstract traces).
servation packaging as part of the environment. The controller is                     Let 𝛼 : 𝐶 → 𝑆b be an abstraction map into a finite set 𝑆b of abstract
finite-state only when (i) the controller state set is finite and (ii)                states. While a concrete run 𝜌 = 𝑐 0𝑎 0𝑢 0𝑐 1 · · · produces a trace 𝜋 (𝜌) ∈
any persistent memory accessible across steps is constant-bounded                     (Σ × Γ) ∗ , the abstraction allows us to view this run as a path through
and encoded into the finite control. If the architecture exposes a                                                    𝑎 0 /𝑢 0
                                                                                      abstract states : 𝜌b = 𝛼 (𝑐 0 ) −−−−→ 𝛼 (𝑐 1 ) . . . . We can say that the
persistent store whose size can grow with execution, the controller
                                                                                      abstraction induces a probabilistic transition model over 𝑆b (which we
is not finite-state regardless of tokenization.
                                                                                      define formally in Theorem 3.4). The abstract trace semantics is the
   It is well-established that for every NFA, an equivalent DFA
                                                                                      distribution over (Σ × Γ) ∗ induced by this abstract model. Note that
can be constructed using the subset construction method; thus,
                                                                                      unlike the state sequence, the trace retains the perceptions 𝑎𝑖 , as these
DFAs and NFAs recognize the same class of languages, being the
                                                                                      form the input alphabet of the corresponding automaton.
regular languages. We define the extended transition where for
𝑀 = (𝑄, Σ𝑖𝑛 , 𝛿, 𝑞 0, 𝐹 ), define 𝛿ˆ : 𝑄 × Σ𝑖𝑛
                                            ∗ → 𝑄 is given by 𝛿ˆ(𝑞, 𝜖) = 𝑞

and 𝛿ˆ(𝑞, 𝑥𝑎) = 𝛿 (𝛿ˆ(𝑞, 𝑥), 𝑎) for 𝑥 ∈ Σ𝑖𝑛 ∗ ,𝑎 ∈ Σ .
                                                    𝑖𝑛
                                                                                          Definition 3.4 (Abstract probabilistic model induced by
                                                                                      𝛼). An abstract probabilistic model for (𝐴, 𝛼) is a finite transition
    Pushdown Automaton (PDA). is a 6-tuple 𝑃 = (𝑄, Σ𝑖𝑛 , Γ, 𝛿, 𝑞 0, 𝐹 ):              model 𝑀𝛼 over abstract states 𝑆b that induces a distribution over ab-
      • 𝑄, Σ𝑖𝑛 , 𝑞 0 ∈ 𝑄, 𝐹 ⊆ 𝑄 defined similarly to FAs.                             stract traces consistent with Pr𝐴,𝛼 Tr
                                                                                                                             . When the environment is fully
      • Γ is a finite stack alphabet.                                                 probabilistic, 𝑀𝛼 can be taken as a labeled Markov chain. When the
      • 𝛿 : 𝑄 × Σ𝑖𝑛,𝜖 × Γ𝜖 → P (𝑄 × Γ𝜖∗ ) is the transition function,                 environment includes nondeterministic choices (for example, unmod-
         where Σ𝑖𝑛,𝜖 = Σ𝑖𝑛 ∪ {𝜖} and Γ𝜖 = Γ ∪ {𝜖}.                                    eled tool variability), 𝑀𝛼 is taken as an MDP, or more generally as a
PDAs recognize the class of context-free languages [21]. In terms                     probabilistic automaton in the sense of nondeterministic choice over
of acceptance and configurations, we use acceptance by final state.                   probability distributions. Probabilistic model checking queries are
A configuration is (𝑞, 𝑤, 𝛼) ∈ 𝑄 × Σ∗ × Γ ∗ . We write (𝑞, 𝑎𝑤, 𝛾𝛼) ⊢                  evaluated on 𝑀𝛼 under the chosen interpretation of nondeterminism
(𝑞 ′, 𝑤, 𝛼 ′ ) if (𝑞 ′, 𝛼 ′ ) ∈ 𝛿 (𝑞, 𝑎, 𝛾) (with 𝜖-moves when 𝑎 = 𝜖 or 𝛾 = 𝜖).       (e.g., worst case, best case, or strategy-restricted).
   Turing Machine. A standard, single-tape TM is a 7-tuple 𝑀 =                           In the sections that follow, we establish correspondence by relat-
(𝑄, Σ𝑖𝑛 , Γ, 𝛿, 𝑞 0, 𝑞 accept, 𝑞 reject ) where:                                      ing each controller class to a standard machine model at the level
     • 𝑄, Σ𝑖𝑛 , 𝑞 0 ∈ 𝑄 defined similarly to FAs.                                     of support languages of traces (via trace-preserving encodings) and
     • Γ is the tape alphabet, where Σ𝑖𝑛 ⊆ Γ and ⊔ ∈ Γ.                               by showing how each class induces a suitable abstract probabilistic
     • 𝛿 : 𝑄 × Γ → 𝑄 × Γ × {𝐿, 𝑅} is the transition function.                         model 𝑀𝛼 for quantitative verification.
     • 𝑞 accept ∈ 𝑄 is the accept state.
     • 𝑞 reject ∈ 𝑄 is the reject state, where 𝑞 accept ≠ 𝑞 reject .                  4     Regular Agents induce Finite-State
TMs recognize the class of recursively enumerable languages.                                Probabilistic Models
   To prove correspondence, the agent architectures described in                      A Regular Agent is a controller architecture whose persistent
the paper must be abstracted into a formal model. Notably, we                         memory is constant-bounded and encoded into a finite set of con-
use acceptor models only to characterize the support language of                      trol states. The policy component (e.g., an LLM) may be stochastic,
feasible traces under architectural constraints. Probabilities enter                  and the environment (including tools) may be probabilistic or may
through the induced trace distribution and the abstract model 𝑀𝛼 ,                    contain nondeterminism. As a result, the closed loop induces a prob-
not through probabilistic acceptance semantics of automata.                           ability distribution over finite interaction traces (Definition 3.2).
                                                                                         This section establishes two correspondences: (i) the support of
3.2     Agentic Trace Definitions                                                     the induced trace distribution is regular, and (ii) the quantitative be-
    Definition 3.1 (Concrete runs and trace projection). Let a                        havior is representable by a finite Markov chain or MDP (depending
controller 𝐴 interact with an environment in discrete steps. Let 𝐶 be the             on how tool/environment uncertainty is modeled).
set of concrete configurations (state, memory contents, and any fixed
bookkeeping). A run is a (finite) sequence 𝜌 = 𝑐 0𝑎 0𝑢 0𝑐 1𝑎 1𝑢 1 · · · 𝑐𝑛            4.1    Architecture constraint
where each 𝑐𝑖 ∈ 𝐶, each 𝑎𝑖 ∈ Σ is the packaged perception produced                       Definition 4.1 (Regular Agent (architecture)). A Regular
by the environment, and each 𝑢𝑖 ∈ Γ is an action. We write 𝜋 (𝜌) =                    Agent architecture consists of: (i) a finite set 𝑆 of control states, (ii) a
(𝑎 0, 𝑢 0 ) (𝑎 1, 𝑢 1 ) · · · (𝑎𝑛−1, 𝑢𝑛−1 ) ∈ (Σ × Γ) ∗ .                             finite perception alphabet Σ and a finite action alphabet Γ, and (iii) an
                                                                                      enforcement mechanism which ensures that all persistent information
                                                                                      that can influence future control decisions is encoded in 𝑆. At each
   Definition 3.2 (Probabilistic trace semantics). Assume the                         step, given a perception 𝑎 ∈ Σ and state 𝑠 ∈ 𝑆, the architecture enables
closed loop of controller, environment, and policy induces a probability              a finite set of transitions of the form (𝑠, 𝑎) ↦→ (𝑠 ′, 𝑢), where 𝑠 ′ ∈ 𝑆
measure Pr𝐴 over finite runs (equivalently, over finite trace prefixes).              and 𝑢 ∈ Γ. A policy selects among enabled transitions stochastically.
The probabilistic trace semantics of 𝐴 is the pushforward distribution
over traces: Pr𝐴Tr (𝑡) = Pr𝐴 ({𝜌 ∈ Runs(𝐴) | 𝜋 (𝜌) = 𝑡 }) , 𝑡 ∈ (Σ × Γ) ∗ .              Exactness of abstraction. The correspondence statements are
The pair (Tr(𝐴), Pr𝐴Tr ) is a probabilistic trace language. Its support               phrased using a finite abstraction 𝛼 : 𝐶 → 𝑆b (Definition 3.3), where
supp(Pr𝐴Tr ) is the set of traces with nonzero probability.                           𝐶 are concrete configurations. For Regular Agents, we require 𝛼 to
                                                                                      preserve the control-relevant distinctions.
,                                                                                             Roham Koohestani†‡ , Ziyou Li‡ Anton Podkopaev†§ , Maliheh Izadi‡


   Definition 4.2 (Exact abstraction for Regular control).                          Theorem 4.6 (Finite probabilistic representation). Under
Let 𝐴 be a Regular Agent architecture. An abstraction 𝛼 : 𝐶 → 𝑆b                 a fixed environment interpretation, the model 𝑀𝛼 in Definition 4.5
                                                                                                                                   Tr
is exact for control if for all concrete configurations 𝑐, 𝑐 ′ ∈ 𝐶 with          induces the same abstract trace distribution as Pr𝐴,𝛼 (Definition 3.3
𝛼 (𝑐) = 𝛼 (𝑐 ′ ) and for all perceptions 𝑎 ∈ Σ, the sets of architec-            and Definition 3.2), under the standard semantics of Markov chains
turally enabled abstract transitions coincide: {(𝛼 (𝑐 1 ), 𝑢) | 𝑐 −−−→
                                                                         𝑎/𝑢     (probabilistic) or MDPs (nondeterminism resolved by a scheduler).
                          𝑎/𝑢                   𝑎/𝑢
𝑐 1 } = {(𝛼 (𝑐 1′ ), 𝑢) | 𝑐 ′ −−−→ 𝑐 1′ }, where 𝑐 −−−→ 𝑐 1 denotes a one-step      Proof sketch. In each abstract state b       𝑠 and perception 𝑎, the
interaction that consumes perception 𝑎 and emits action 𝑢 (with the                                                    𝑠 ′, 𝑢) successors. The policy and
                                                                                 architecture enables a finite set of (b
environment/tool effects included in the successor configuration).               environment interpretation determine either a single probability
                                                                                 distribution or a set of them over these successors. Because 𝑆b is
4.2          Regular support via an explicit NFA                                 finite, this yields a finite MC/MDP whose stepwise trace generation
We first build an automaton that generates exactly the feasible                  matches the pushforward semantics of Definition 3.2 on abstract
interaction traces of the abstracted system.                                     traces.                                                                □
    Definition 4.3 (Support NFA for Regular Agents). Fix a                                                                               b ⊆ 𝑆,
                                                                                    Quantitative verification queries. For an unsafe set 𝐵   b one
Regular Agent 𝐴 and an abstraction 𝛼 with finite codomain 𝑆.         b Define
                                                                                 evaluates reachability probabilities such as Pr𝑀𝛼 (♢𝐵) or
                                                                                                                                     b
                         𝑠 0, Σ × Γ, →, 𝑆), where all states are accepting,
              reg
an NFA 𝐺𝐴,𝛼 = (𝑆,b     b                b
                                                                                 sup𝜎 Pr𝜎𝑀𝛼 (♢𝐵),
                                                                                              b depending on whether nondeterminism is absent
𝑠 0 = 𝛼 (𝑐 0 ) for the initial configuration 𝑐 0 , and the transition relation
b                                                                                or interpreted via schedulers 𝜎.
    (𝑎,𝑢 )
        𝑠 ′ holds iff there exists a concrete step from some configuration
𝑠 −−−−→ b
b
𝑐 with 𝛼 (𝑐) = b  𝑠 that consumes perception 𝑎, emits action 𝑢, and              5     Context-Free Agents induce Probabilistic
reaches some 𝑐 ′ with 𝛼 (𝑐 ′ ) = b 𝑠′.                                                 Pushdown Models
   The NFA reads symbols in Σ × Γ and accepts every finite trace                 A Context-Free Agent augments finite control with an unbounded
that is feasible under the architecture (and under the chosen inter-             stack and enforces a stack-scoped persistence discipline sufficient to
pretation of environment feasibility as existential).                            model hierarchical control. As before, we separate: (i) a qualitative
                                                                                 correspondence stating that the support trace language is context-
    Theorem 4.4 (Regular support). Let 𝐴 be a Regular Agent and
                                                                                 free, and (ii) a quantitative correspondence stating that the abstract
let 𝛼 be an abstraction with finite codomain 𝑆b that is exact for control
                                                            Tr                   closed loop is representable by a probabilistic pushdown model (or
(Definition 4.2). Then the trace support language supp(Pr𝐴,𝛼    ) ⊆ (Σ ×
                                                                                 a pushdown MDP).
Γ) ∗ is regular. In particular, supp(Pr𝐴,𝛼
                                        Tr         reg
                                           ) = 𝐿(𝐺𝐴,𝛼 ) for the NFA in
Definition 4.3.                                                                  5.1     Architecture constraint
   Proof sketch. Because 𝑆b is finite and Σ × Γ is finite, 𝐺𝐴,𝛼 is a
                                                              reg
                                                                                    Definition 5.1 (Context-Free Agent (architecture)). A
finite automaton. Exactness ensures that abstract states characterize            Context-Free Agent architecture consists of: (i) a finite set 𝑆 of control
precisely the enabled abstract moves, so every feasible abstract trace           states, (ii) a finite stack alphabet 𝑍 , (iii) finite alphabets Σ (percep-
corresponds to a path in the NFA and conversely every NFA path                   tions) and Γ (actions), and (iv) an enforcement mechanism restricting
corresponds to some feasible abstract execution. Regularity follows              persistent memory to a single stack with LIFO access across steps. At
because the accepted language of a finite automaton is regular. □                each step, given control state 𝑠 ∈ 𝑆, perception 𝑎 ∈ Σ, and top-of-stack
   It must be noted that we assume that the policy assigns nonzero               symbol 𝑧 ∈ 𝑍𝜖 , the architecture enables transitions that emit an ac-
probability to each architecturally enabled transition. Equivalently             tion 𝑢 ∈ Γ, update the control state to 𝑠 ′ ∈ 𝑆, and update the stack
we could restrict the transition relation in the support generator to            by replacing 𝑧 with a word 𝛽 ∈ 𝑍 ∗ (push, pop, or no-op). Formally,
those with nonzero probability under the closed-loop semantics.                  enabled moves are of the shape: (𝑠, 𝑧, 𝑎) ↦→ (𝑠 ′, 𝛽, 𝑢). A policy selects
                                                                                 among enabled moves, possibly stochastically.
4.3          Finite probabilistic model for quantitative
             queries                                                                 If a strict call-return discipline is desired, one may further par-
                                                                                 tition actions Γ = Γcall ⊎ Γret ⊎ Γint and enforce that calls push a
We now describe the induced quantitative model used for proba-                   designated return symbol and returns pop it. The correspondence
bilistic model checking. This depends on how tool/environment                    below holds already for general stack updates, and therefore also
uncertainty is represented.                                                      for call-return as a special case.
   Definition 4.5 (Finite-state probabilistic closed-loop model).
Fix 𝐴 and 𝛼 as above and fix an environment interpretation: either (i)           5.2     Context-free support via an explicit PDA
fully probabilistic outcomes or (ii) outcomes containing nondetermin-               Definition 5.2 (Support PDA for Context-Free Agents).
ism. The induced abstract closed-loop model is 𝑀𝛼 = (𝑆,b     b 𝑠 0, Σ, Γ, T ),   Fix a Context-Free Agent 𝐴 and an abstraction 𝛼 : 𝐶 → 𝑆b with
where T (b𝑠 , 𝑎) is:                                                             finite 𝑆b that preserves the finite control and any finite stack in-
     • a single probability distribution over (b𝑠 ′, 𝑢) ∈ 𝑆b× Γ in the fully     formation required to determine enabled transitions. Define a PDA
       probabilistic case, yielding a labeled Markov chain; or                   𝐺𝐴,𝛼      b Σ × Γ, 𝑍, 𝛿𝐺 , b
                                                                                   cfa = (𝑆,                         b where b
                                                                                                                𝑠 0, 𝑆),       𝑠 0 = 𝛼 (𝑐 0 ) and 𝛿𝐺 simulates
     • a finite set of distributions over 𝑆b× Γ in the presence of nonde-        one abstract controller step while reading one symbol (𝑎, 𝑢) ∈ Σ × Γ.
       terminism, yielding an MDP.                                               Concretely, 𝛿𝐺 (b                        𝑠 ′, 𝛽) whenever the architecture
                                                                                                 𝑠 , (𝑎, 𝑢), 𝑧) contains (b
Are Agents Probabilistic Automata? A Trace-Based, Memory-Constrained Theory of Agentic AI                                                                         ,


permits, from some concrete configuration 𝑐 with 𝛼 (𝑐) = b
                                                         𝑠 and stack-                 6.1     Architecture constraint
top 𝑧, consuming perception 𝑎, emitting action 𝑢, moving to some 𝑐 ′                     Definition 6.1 (TC Agent (architecture)). A TC Agent archi-
with 𝛼 (𝑐 ′ ) = b
                𝑠 ′ and replacing 𝑧 by 𝛽.                                             tecture consists of: (i) a finite control state set 𝑆, (ii) finite alphabets Σ
   Theorem 5.3 (Context-free support). Let 𝐴 be a Context-                            (perceptions) and Γ (actions), and (iii) an unbounded persistent store
Free Agent and let 𝛼 be a finite abstraction as in Definition 5.2.                    with a finite memory alphabet Γmem and operations that allow reading
              Tr
Then supp(Pr𝐴,𝛼  ) ⊆ (Σ × Γ) ∗ is context-free, and in particular                     and writing at arbitrary addresses across steps (not restricted to a stack
       Tr                                                                             discipline). The controller can iterate without a global, structurally
supp(Pr𝐴,𝛼 ) = 𝐿(𝐺𝐴,𝛼
                   cfa ).
                                                                                      enforced bound on the number of steps.
   Proof sketch. The PDA 𝐺𝐴,𝛼   cfa reads interaction symbols (𝑎, 𝑢)

and simulates the stack update discipline of the architecture. Thus it                6.2     Recursively enumerable support for
accepts exactly the feasible abstract interaction traces. Because the                         interaction traces
accepted language of a PDA is context-free, the support language
                                                                                         Theorem 6.2 (Recursively enumerable trace support). Let
is context-free.                                                    □
                                                                                      𝐴 be a TC Agent architecture in the unbounded model (Definition 6.1).
                                                                                      Then the set of feasible finite interaction traces Tr(𝐴) ⊆ (Σ × Γ) ∗ is
5.3     Probabilistic pushdown model for                                              recursively enumerable. Conversely, for any recursively enumerable
        quantitative queries                                                          language 𝐿 ⊆ (Σ × Γ) ∗ , there exists a TC Agent architecture 𝐴𝐿 such
   Definition 5.4 (Probabilistic pushdown closed-loop model).                         that Tr(𝐴𝐿 ) = 𝐿.
Fix 𝐴, 𝛼, and an environment interpretation as in the Regular case.
The induced abstract model 𝑀𝛼 is a probabilistic pushdown model: a                       Proof sketch. For the forward direction, simulate the controller
pushdown transition system over control states 𝑆b and stack alphabet                  and store operations by a Turing machine that enumerates all finite
𝑍 whose step relation, conditioned on a perception 𝑎 ∈ Σ, either (i)                  execution prefixes and prints the corresponding interaction traces
                                                           𝑠 ′, 𝛽, 𝑢) or (ii)
assigns a probability distribution over successor triples (b                          when they occur; this is a semi-decision procedure for membership
enables a set of such distributions in the presence of nondeterminism.                in Tr(𝐴), hence Tr(𝐴) is recursively enumerable. For the converse
In case (ii), the model is a pushdown MDP.                                            direction, given an r.e. language 𝐿 ⊆ (Σ × Γ) ∗ recognized by a
                                                                                      Turing machine 𝑀, construct a TC Agent that simulates 𝑀 on its
   Theorem 5.5 (Probabilistic pushdown representation). Un-                           unbounded store and emits exactly the symbols of a trace when
der a fixed environment interpretation, the model in Definition 5.4                   𝑀 reaches the corresponding configuration; feasibility of traces
                                                  Tr
induces the same abstract trace distribution as Pr𝐴,𝛼 , under the stan-               coincides with acceptance by 𝑀.                                  □
dard semantics of probabilistic pushdown systems and pushdown
MDPs.                                                                                 6.3     Quantitative modeling and undecidability
   Proof sketch. The architecture exposes finitely many control                       The probabilistic trace semantics (Definition 3.2) extends to TC
states and a stack with finite alphabet. Each enabled step induces                    Agents by placing a probability measure on runs via the policy and
either a probability distribution over finitely many successor con-                   environment. However, in the unbounded model, many verification
trol/stack/action updates or a set of such distributions under non-                   questions inherit the standard undecidability barriers of universal
determinism. This yields a probabilistic pushdown system (or push-                    computation. In practice, analysis proceeds by (i) bounding execu-
down MDP) whose one-step trace generation matches the pushfor-                        tions (step limits, timeouts, token budgets, or storage quotas), or
ward semantics of Definition 3.2.                                □                    (ii) constructing a finite abstraction 𝛼 and analyzing the induced
                                                                                      model 𝑀𝛼 (Definition 3.4).
   Quantitative verification queries. For an unsafe region 𝐵 b ⊆ 𝑆b                       When explicit bounds are imposed, the induced execution space
(or an unsafe set of control-stack configurations), one can ask for                   becomes finite-state (or at least finitely representable), yielding
extrema of reachability probability, analogously to the finite-state                  a model that can be checked with bounded reachability or finite-
case, but now over pushdown models.                                                   horizon variants of probabilistic model checking.

6     TC Agents induce Recursively Enumerable                                         7     Extension to Multi-Agent Systems
      Trace Support                                                                   The correspondence extends to multi-agent systems under stan-
A TC Agent (Turing-complete agent) is a controller architecture                       dard composition semantics. Let A1, . . . , A𝑛 be controllers with
with finite control and access to an unbounded, arbitrarily read-                     local control states 𝑆 1, . . . , 𝑆𝑛 . A common execution semantics is
able and writable persistent store across steps. Examples include                     interleaving: at each global step a scheduler selects one agent to act,
an unbounded scratchpad, unrestricted file I/O used as persistent                     that agent consumes a perception symbol and emits an action, and
memory, or any external store that can grow without bound and                         the global state updates accordingly.
can be accessed non-LIFO (random access) across execution.                                Products of bounded-memory agents remain bounded-
   This section states the correspondence in the same trace-centric                   memory If every A𝑖 is Regular (i.e., has finite control and per-
form as before: the set of feasible finite interaction traces is re-                  sistently stored memory bounded by a constant), then their com-
cursively enumerable in the unbounded model, and verification in                      position yields a system with a finite global control-state space:
general inherits undecidability barriers unless one bounds execu-                     𝑆 global = 𝑆 1 × · · · × 𝑆𝑛 , possibly extended with finite scheduler book-
tions or abstracts to a finite model.                                                 keeping. Hence, under interleaving semantics, the composed system
,                                                                                              Roham Koohestani†‡ , Ziyou Li‡ Anton Podkopaev†§ , Maliheh Izadi‡


still belongs to the Regular class, although the state space may grow        8.2       Illustrative mapping of patterns under
multiplicatively. An analogous result holds for Context-Free agents                    explicit constraints
under standard pushdown product constructions, provided each
                                                                             Table 1 gives an illustrative mapping from common agent patterns
agent uses its own stack and the scheduler is finite-state.
                                                                             to classes, but only under explicit architectural constraints. The
    Shared unbounded memory yields TC behavior The compu-
                                                                             purpose of the table is to emphasize that “framework” alone is
tational class changes when agents share an unbounded, arbitrarily
                                                                             not the classifier; the classifier is the configuration of memory and
readable/writable persistent store. Even if each individual agent
                                                                             control enforced by the framework.
has finite control, the composition of finite control with a shared
unbounded store can simulate a Turing machine; The global finite             Table 1: Illustrative mapping from patterns to classes under
control implements the machine’s finite control, and the shared              explicit constraints
store implements the tape (or random-access memory). Under a
serialized scheduler (or atomic read/write operations), this simula-           Pattern / Framework           Constraint knob               Class
tion is straightforward. Therefore, a multi-agent system of Regular                                          (enforced)
controllers with shared unbounded read/write memory is TC in the               Rule-based workflows          Finite control graph; no      Regular
                                                                               (IFTTTa , n8nb )              persistent store beyond
unbounded model.                                                                                             constant parameters.
    Probabilistic traces under interleaving Under stochastic poli-
                                                                               Hierarchical task             Stack-scoped task             Context-Free
cies and uncertain tools, the multi-agent closed loop induces a prob-          delegation                    frames; returns restore
ability distribution over global interleaving traces. These traces can         (manager–worker)              caller context; no
be defined as sequences in (Σ × Γ × {1, . . . , 𝑛}) ∗ that also record the                                   general read/write store.

acting agent at each step. All trace-based constructions above lift            Graph-based controllers       If persistent store is        Regular or Context-Free
                                                                               (e.g., LangGraphc )           bounded and cycles are
by including the scheduler choices either as part of nondetermin-                                            bounded (or absent),
ism (adversarial scheduling) or as part of probabilistic evolution                                           controller is finite-state;
(randomized scheduling), depending on modeling intent.                                                       if stack-scoped frames
                                                                                                             only, controller is
                                                                                                             pushdown.
                                                                               ReAct-style loops [26]        If scratchpad and             Regular (bounded) or TC
8     Right-Sizing Agents                                                                                    history are bounded and       (unbounded)
                                                                                                             not reread beyond a
This section instantiates the architectural correspondences of Sec-                                          fixed window,
tions 4 through 6 as a right-sizing guideline. We propose that given                                         finite-state abstraction
                                                                                                             may apply; if the agent
a task specification and a candidate framework, select the weakest                                           can accumulate and
controller class whose enforced memory interface and control disci-                                          arbitrarily reread an
pline can realize the required interaction behavior. Right-sizing is                                         unbounded store, TC.
stated at the architecture level rather than at the level of an indi-          Auto-GPT-style                Unbounded file or             TC
vidual policy, since the policy may be stochastic and is treated as            agents [24]                   database artifacts with
                                                                                                             arbitrary reread and
selecting among architecturally enabled transitions.                                                         iteration without
                                                                                                             structural bound.
                                                                             a https://ifttt.com/
                                                                             b https://n8n.io/
8.1     Decision procedure at the architecture level                         c https://www.langchain.com/langgraph

Right-sizing depends on (i) whether persistent information can
grow with execution, and (ii) how that information can be accessed
across steps. Concretely, for a controller architecture:                     9      Case Study: A Booking Controller
                                                                             This section illustrates right-sizing by instantiating a flight book-
      • Bounded persistent memory: all information that can                  ing task under three controller architectures that share the same
        influence future control is constant-bounded and encoded             external interface but differ in their persistent memory constraints.
        into finite control (section 4).                                        Task. The user requests: “book a flight to London for under $500.”
      • Stack-scoped persistent memory: the only unbounded                   Perceptions are tokenized symbols in Σ (user messages and tool
        persistence is a LIFO stack, optionally with a call-return           outputs) and actions are tool invocations in Γ, such as search_-
        discipline (section 5).                                              flights, check_calendar, and book. Each execution induces an
      • Unbounded read/write persistent memory: the controller               interaction trace in (Σ × Γ) ∗ (Definition 3.1). All three controllers
        can grow a store without bound and later access it in a non-         invoke the same tools, but the architecture restricts what infor-
        stack manner (random access or general key-value retrieval),         mation can persist across steps and how it can be accessed. For
        yielding the unbounded model (section 6).                            analysis, each design yields an induced abstract model 𝑀𝛼 (Defini-
                                                                             tion 3.4) under a chosen environment interpretation (probabilistic
   Figure 1 summarizes these checks. The key point is that the               vs nondeterministic tool outcomes).
classification is determined by enforced interfaces. The same soft-          9.1       Regular design
ware framework may realize different classes depending on how it             Architecture. The controller has a finite set of states encoding
constrains memory, iteration, and tool access.                               a bounded set of slots, for example: Get_Destination, Get_Date,
Are Agents Probabilistic Automata? A Trace-Based, Memory-Constrained Theory of Agentic AI                                                                    ,




                                                                                             If unbounded persistence
                 Task and inter-                   Does the controller                                                             Requires TC
                                                                                                 is needed, is access
                face specification                  require persistent          Yes                                       No       (unbounded
                                                                                                restricted to a LIFO
                   (perceptions                  information whose size                                                             read/write)
                                                                                                stack (call-return or
                   Σ, actions Γ)                can grow with execution?                                                            (section 6)
                                                                                                stack updates only)?




                                                         No
                                                                                                     Yes
                                                      Use Regular
                                                                                                Use Context-Free
                                                      (finite-state)
                                                                                                   (pushdown)
                                                       (section 4)
                                                                                                    (section 5)


Figure 1: Architecture-level decision procedure for right-sizing. The checks are phrased in terms of enforced persistent memory
interfaces and access discipline, rather than policy behavior.


Get_Budget, Confirm, Book. Each slot ranges over a finite domain                      interaction traces is recursively enumerable (Theorem 6.2). This ar-
(or is discretized), so all persistent information is encoded into finite             chitecture can realize traces that correspond to open-ended research
control. Behavioral envelope. The feasible trace support is regu-                     and refinement loops whose length and stored information grow
lar (Theorem 4.4). This controller can realize traces that alternate                  without bound. Verification implication. Quantitative analysis
between requesting missing slot values and invoking tools once all                    can still be performed on bounded executions or on finite abstrac-
slots are filled. It does not realize traces that require unbounded                   tions 𝛼, but general unbounded verification inherits the standard
accumulation of information or hierarchical subtask nesting with                      undecidability barriers of universal computation (section 6).
arbitrary depth. Verification implication. Under a finite abstrac-                    9.4    Summary of the right-sizing trade-off
tion 𝛼, the induced model 𝑀𝛼 is a finite MC/MDP (Theorem 4.6),
which allows for probabilistic reachability checks (e.g., bounding                    All three controllers share the same external tool interface, but
the probability of calling book without user confirmation) rather                     their memory interfaces determine which interaction traces are
than implying that the system is safe by construction.                                feasible and which verification techniques apply. For booking-style
                                                                                      tasks that do not require open-ended information accumulation,
9.2     Context-Free design                                                           Regular or Context-Free designs can realize the relevant trace set
                                                                                      while yielding finite or pushdown probabilistic models amenable
Architecture. The controller maintains a stack of task frames,
                                                                                      to quantitative model checking. TC designs are appropriate only
with a designated top-level frame Plan_Trip. When the user re-
                                                                                      when the specification explicitly requires unbounded read/write
quests “check my calendar before booking,” the controller pushes
                                                                                      persistence or unbounded iteration.
a subtask frame Check_Calendar, executes it, and returns to its
caller. It can then push Search_Flights and later Book_Flight.                        10 Discussion
The only unbounded persistence is the LIFO stack; there is no gen-                    10.1 Why Memory-Based Constraints
eral read/write store. Behavioral envelope. The feasible trace
support is context-free (Theorem 5.3). The stack discipline enables                   Several taxonomies classify autonomy at the behavioral level, in-
hierarchical plans with unbounded nesting depth across execu-                         cluding graded autonomy levels in automotive settings (e.g., levels
tions, while constraining how information persists and is revisited.                  of driving automation) [18]. Behavioral taxonomies are descriptive
Verification implication. The induced model is a probabilistic                        and do not, by themselves, yield a checkable transition model for
pushdown system or pushdown MDP (Theorem 5.5), which sup-                             verification. In contrast, the memory interface exposed by a con-
ports quantitative reachability queries over call-return behavior.                    troller architecture is a structural constraint in that it specifies what
Termination is not implied by pushdown structure; it is a property                    information can persist across steps and how that information can
that can be analyzed under additional assumptions (for example,                       be accessed. Once these constraints are explicit, the controller can
bounded retry policies, ranking arguments, or explicit step limits)                   be placed in a machine class whose induced trace semantics ad-
or as a bounded-execution query on a finite abstraction.                              mits established analysis techniques, including probabilistic model
                                                                                      checking on a finite abstract model 𝑀𝛼 (Definitions 3.3 through
9.3     TC design                                                                     3.4). The result is not that safety holds by construction, but that
                                                                                      the controller class determines which verification questions can be
Architecture. The controller can create and accumulate persis-
                                                                                      posed algorithmically and which questions inherit undecidability.
tent artifacts (files, notes, database entries) without bound and can
reread them arbitrarily across steps. It can iterate without a struc-
turally enforced bound on the number of tool invocations (e.g.,                       10.2     Implications for Engineering Practice
repeated google_search followed by note-taking and refinement).                       The classification supports engineering decisions that depend on
Behavioral envelope. In the unbounded model, the set of feasible                      the interaction envelope and on the available assurance techniques.
,                                                                                    Roham Koohestani†‡ , Ziyou Li‡ Anton Podkopaev†§ , Maliheh Izadi‡


   When the controller admits a finite or pushdown abstraction,          design, the behavior can be encoded into finite control. If the archi-
safety and reachability claims can be reduced to explicit queries        tecture supports unbounded accumulation and arbitrary reread of
on 𝑀𝛼 , including quantitative reachability under probabilistic and      persistent artifacts, then the unbounded model applies.
nondeterministic tool outcomes. This supports structured assurance
arguments that reference an explicit control model, an abstraction       10.4    Limitations and Threats to Validity
map 𝛼, and an interpretation of nondeterminism.
                                                                         This framework relies on assumptions that may not hold in all
   Additionally, bounding the controller’s persistent memory in-
                                                                         deployed systems. LLM context as implicit memory. The policy
terface restricts the set of feasible traces and can reduce the space
                                                                         component relies on the prompt context, which serves as a bounded
of possible behaviors. In deployed systems, additional execution
                                                                         memory whose capacity is determined by the context window and
bounds (step limits, token budgets, retry limits) can be represented
                                                                         by how prompts are constructed in the architecture. The finite-
directly in 𝑀𝛼 and analyzed as reachability or expected-cost queries.
                                                                         state and pushdown mappings require that all control-relevant
These bounds also make it possible to compare architectures using
                                                                         information provided to the policy respect this intended memory
quantitative measures that align with operational constraints.
                                                                         interface, and that information outside this interface cannot affect
   Finally, even when the policy component is not interpretable,
                                                                         control decisions.
architecture-level constraints can be enforced at the tool and mem-
                                                                            Abstraction fidelity. Claims about 𝑀𝛼 depend on whether 𝛼
ory interfaces (for example, disallowing external writes, restricting
                                                                         preserves the control-relevant distinctions needed for the property
reads to a stack frame, or mediating tool calls through an explicit
                                                                         of interest. If the abstraction omits variables that influence enabled
controller). This yields a separation between policy selection and
                                                                         actions or tool arguments, the induced model may be unsound
allowable actions that is compatible with the trace-based semantics.
                                                                         for verification. Furthermore, while practical tools accept infinite
                                                                         domains (e.g., strings), we assume arguments are discretized via ab-
10.3    Implications of Correspondence                                   straction or bounded by model generation limits to maintain a finite
                                                                         alphabet Γ. Additionally, this framework classifies the controller’s
10.3.1 Decidability boundaries for verification queries. The corre-      persistent memory constraints, not the computational power of
spondence results connect controller architectures to known ma-          external tools. Finally, Even when verification is decidable, the in-
chine classes and therefore to known algorithmic boundaries.             duced model can be large. Practical analysis requires abstraction,
   For Regular Agents, properties such as reachability and safety on     compositional reasoning, and symbolic techniques.
the induced finite model 𝑀𝛼 are decidable, and quantitative variants        Environment and tool modeling. Tools and environments
are addressed by probabilistic model checking of Markov chains           may be nondeterministic, stochastic, or non-stationary. Probabil-
and MDPs over a finite state space. As for Context-Free Agents           ity estimates may change over time, and modeling uncertainty as
with a call-return discipline, qualitative and quantitative reachabil-   nondeterminism can be conservative. The interpretation of non-
ity questions can be phrased on a pushdown model (or pushdown            determinism (worst case, best case, or strategy-restricted) affects
MDP) induced by the abstraction. Other properties, such as lan-          reported quantitative guarantees.
guage equivalence, are undecidable for general PDAs and remain              Multi-agent semantics. For multi-agent settings, the relation-
challenging even under determinism. Finally, For TC Agents in the        ship between interleavings, shared memory, and atomicity assump-
unbounded model, reachability questions inherit undecidability via       tions affects the induced trace model and may require a more de-
standard reductions from universal computation. In this setting,         tailed operational semantics than considered in this paper.
analysis proceeds through bounded executions, finite abstractions
𝛼, or additional restrictions that recover decidable subclasses.
                                                                         11     Conclusion and Outlook
                                                                         This paper presented a memory-interface-based framework that
10.3.2 Probabilistic trace abstractions and refinement. The seman-
                                                                         relates controller architectures for agentic systems to standard
tics assigns a distribution over traces (Definition 3.2), and verifi-
                                                                         machine models via probabilistic trace semantics and finite ab-
cation targets an induced abstract probabilistic model 𝑀𝛼 (Defini-
                                                                         straction. Under checkable constraints on persistent memory ac-
tions 3.3–3.4). Coarse abstractions can admit abstract traces that
                                                                         cess and control discipline, the support of the induced trace lan-
do not correspond to any concrete execution, or can introduce spu-
                                                                         guage aligns with regular, context-free, and recursively enumerable
rious high-probability paths under an MDP interpretation. Refine-
                                                                         classes for bounded memory, stack-scoped memory, and unbounded
ment can be driven by counterexamples returned by probabilistic
                                                                         read/write persistence, respectively. The framework motivates a
model checking, by separating abstract states that conflate control-
                                                                         right-sizing guideline in which the weakest controller class is se-
relevant distinctions. This yields a trace-oriented refinement loop
                                                                         lected that can realize the required interaction traces, and analyze
that is compatible with CEGAR-style workflows for nondetermin-
                                                                         the induced abstract model 𝑀𝛼 using probabilistic model checking
istic and probabilistic systems.
                                                                         when a finite abstraction is available.
                                                                            Two directions follow from this formulation. First, minimal-class
10.3.3 Planning structure and controller class. Hierarchical plan-       synthesis: given a task specification and an interface model, syn-
ning can be represented in multiple ways depending on what the           thesize a controller that enforces the weakest sufficient memory
architecture enforces. If the architecture enforces call-return struc-   interface and emit conformance evidence that the implementation
ture with stack-scoped persistence, then a pushdown model is ap-         respects the interface. Second, hybrid architectures with runtime
propriate. If plan depth and stored information are bounded by           enforcement: mediate tool access through finite-state or pushdown
Are Agents Probabilistic Automata? A Trace-Based, Memory-Constrained Theory of Agentic AI                                                                                 ,


cores while permitting higher-power components behind moni-                           References
tored interfaces, and analyze the resulting system under bounded                       [1] W. R. Ashby, J. T. Culbertson, M. D. Davis, S. C. Kleene, K. De Leeuw, D. M.
executions and abstraction.                                                                Mac Kay, J. Mc Carthy, M. L. Minsky, E. F. Moore, C. E. Shannon, N. Shapiro,
                                                                                           A. M. Uttley, and J. Von Neumann. 1956. Automata Studies. (AM-34). Princeton
   A shared suite of reference tasks and conformance tests for mem-                        University Press. https://www.jstor.org/stable/j.ctt1bgzb3s
ory interfaces would enable empirical evaluation of right-sizing                       [2] Christel Baier and Joost-Pieter Katoen. 2008. Principles of Model Checking. MIT
                                                                                           Press.
decisions and support comparisons across frameworks under ex-                          [3] Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. 2000.
plicit constraints.                                                                        Counterexample-guided abstraction refinement. In International Conference on
                                                                                           Computer Aided Verification. Springer, 154–169.
                                                                                       [4] Itay Cohen and Doron Peled. 2024. End-to-End AI Generated Runtime Verification
                                                                                           from Natural Language Specification. doi:10.1007/978-3-031-73741-1_23
                                                                                       [5] Christian Dehnert, Daniel Gebler, Michele Volpato, and David N Jansen. 2012.
                                                                                           On abstraction of probabilistic systems. International autumn school on rigorous
                                                                                           dependability analysis using model checking techniques for stochastic systems
                                                                                           (2012), 87–116.
                                                                                       [6] Christian Dehnert, Sebastian Junges, Joost-Pieter Katoen, and Matthias Volk.
                                                                                           2017. A storm is coming: A modern probabilistic model checker. In International
                                                                                           Conference on Computer Aided Verification. Springer, 592–600.
                                                                                       [7] Louise A. Dennis. 2018. The MCAPL Framework including the Agent Infrastruc-
                                                                                           ture Layer an Agent Java Pathfinder. (2018). https://joss.theoj.org/papers/10.211
                                                                                           05/joss.00617
                                                                                       [8] Louise A. Dennis, Michael Fisher, Matthew P. Webster, and Rafael H. Bordini. 2012.
                                                                                           Model checking agent programming languages. Automated Software Engineering
                                                                                           19, 1 (March 2012), 5–63. doi:10.1007/s10515-011-0088-x Company: Springer
                                                                                           Distributor: Springer Institution: Springer Label: Springer Publisher: Springer
                                                                                           US.
                                                                                       [9] Kousha Etessami and Mihalis Yannakakis. 2005. Recursive Markov chains, sto-
                                                                                           chastic grammars, and monotone systems of nonlinear equations. In Annual
                                                                                           Symposium on Theoretical Aspects of Computer Science. Springer, 340–352.
                                                                                      [10] Patrice Godefroid. 1996. Partial-Order Methods for the Verification of Concurrent
                                                                                           Systems: An Approach to the State-Explosion Problem. Springer.
                                                                                      [11] Junda He, Christoph Treude, and David Lo. 2025. LLM-Based Multi-Agent
                                                                                           Systems for Software Engineering: Literature Review, Vision, and the Road
                                                                                           Ahead. ACM Trans. Softw. Eng. Methodol. 34, 5 (May 2025), 124:1–124:30.
                                                                                           doi:10.1145/3712003
                                                                                      [12] Junda He, Christoph Treude, and David Lo. 2025. LLM-Based Multi-Agent Sys-
                                                                                           tems for Software Engineering: Literature Review, Vision, and the Road Ahead.
                                                                                           ACM Transactions on Software Engineering and Methodology 34, 5 (June 2025),
                                                                                           1–30. doi:10.1145/3712003
                                                                                      [13] Zelong Li, Wenyue Hua, Hao Wang, He Zhu, and Yongfeng Zhang. 2024. Formal-
                                                                                           LLM: Integrating Formal Language and Natural Language for Controllable LLM-
                                                                                           based Agents. doi:10.48550/arXiv.2402.00798 arXiv:2402.00798 [cs].
                                                                                      [14] Jia Liu and Jie Shuai. 2023. SMoT: Think in State Machine. doi:10.48550/arXiv.2
                                                                                           312.17445 arXiv:2312.17445 [cs] version: 1.
                                                                                      [15] Salvador Lucas. 2021. The origins of the halting problem. Journal of Logical and
                                                                                           Algebraic Methods in Programming 121 (June 2021), 100687. doi:10.1016/j.jlamp.
                                                                                           2021.100687
                                                                                      [16] Kanghee Park, Jiayu Wang, Taylor Berg-Kirkpatrick, Nadia Polikarpova, and Loris
                                                                                           D’Antoni. 2024. Grammar-Aligned Decoding. doi:10.48550/arXiv.2405.21047
                                                                                           arXiv:2405.21047 [cs].
                                                                                      [17] Martin L. Puterman. 1994. Markov Decision Processes: Discrete Stochastic Dynamic
                                                                                           Programming. Wiley.
                                                                                      [18] SAE International. 2021. Taxonomy and Definitions for Terms Related to Driving
                                                                                           Automation Systems for On-Road Motor Vehicles. Surface Vehicle Recommended
                                                                                           Practice, J3016_202104. https://www.sae.org/standards/j3016_202104-taxonomy-
                                                                                           definitions-terms-related-driving-automation-systems-road-motor-vehicles
                                                                                           [Online; accessed 26-December-2025].
                                                                                      [19] SAIL. 2006. MCMAS. SAIL (2006). https://sail.doc.ic.ac.uk/software/mcmas/ See
                                                                                           "https://sail.doc.ic.ac.uk/software/mcmas/".
                                                                                      [20] Roberto Segala and Nancy Lynch. 1995. Probabilistic simulations for probabilistic
                                                                                           processes. Nordic Journal of Computing 2, 2 (1995), 250–273.
                                                                                      [21] Michael Sipser. 2012. Introduction to the Theory of Computation. Cengage Learning.
                                                                                           Google-Books-ID: 4J1ZMAEACAAJ.
                                                                                      [22] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li
                                                                                           Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah,
                                                                                           Ryen W. White, Doug Burger, and Chi Wang. 2023. AutoGen: Enabling Next-Gen
                                                                                           LLM Applications via Multi-Agent Conversation. doi:10.48550/arXiv.2308.08155
                                                                                           arXiv:2308.08155 [cs].
                                                                                      [23] Yiran Wu, Tianwei Yue, Shaokun Zhang, Chi Wang, and Qingyun Wu. 2024.
                                                                                           StateFlow: Enhancing LLM Task-Solving through State-Driven Workflows. doi:10
                                                                                           .48550/arXiv.2403.11322 arXiv:2403.11322 [cs].
                                                                                      [24] Hui Yang, Sifu Yue, and Yunzhong He. 2023. Auto-GPT for Online Decision
                                                                                           Making: Benchmarks and Additional Opinions. doi:10.48550/arXiv.2306.02224
                                                                                           arXiv:2306.02224 [cs].
                                                                                      [25] Hui Yang, Sifu Yue, and Yunzhong He. 2023. Auto-GPT for Online Decision
                                                                                           Making: Benchmarks and Additional Opinions. doi:10.48550/arXiv.2306.02224
,                                                                                             Roham Koohestani†‡ , Ziyou Li‡ Anton Podkopaev†§ , Maliheh Izadi‡


     arXiv:2306.02224 [cs].                                                          Models. doi:10.48550/arXiv.2210.03629 arXiv:2210.03629 [cs].
[26] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
     and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language
