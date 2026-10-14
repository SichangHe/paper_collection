                                                    A Neuro-Symbolic Approach to Strategy
                                                        Synthesis for Strategic Logics

                                             Marco Aruta1 , Vadim Malvone2 , Aniello Murano1 , Domenico Parente3 , and
                                                                         Luca Rizzuti3
                                                                1
                                                                University of Naples Federico II, Naples, Italy
                                                2
                                                    LTCI, Télécom Paris, Institut Polytechnique de Paris, Palaiseau, France
arXiv:2606.17962v1 [cs.MA] 16 Jun 2026




                                                             3
                                                               Università degli Studi di Salerno, Salerno, Italy



                                                    Abstract. Reasoning about what agents can achieve through strategic
                                                    interaction is a core challenge in Multi-Agent Systems (MAS). Logics
                                                    for strategic ability, such as ATL, provide rigorous methods, but their
                                                    adoption is often hindered by the computational cost of strategy syn-
                                                    thesis. We introduce a neuro-symbolic framework that integrates large
                                                    language models (LLMs) into the model-checking pipeline for MAS. The
                                                    LLM acts as a strategy-generation oracle, proposing candidate strategies
                                                    that are then formally validated by a standard MAS model checker. This
                                                    generate-and-certify architecture uses LLM guidance to navigate large
                                                    combinatorial strategy spaces while preserving formal soundness: gener-
                                                    ated strategies are accepted only when certified by the verifier. We in-
                                                    stantiate the framework for bounded strategic reasoning in NatATL and
                                                    introduce the first NatATL strategy-synthesis dataset, consisting of 4,211
                                                    instances. Experiments with an open-weight Qwen3-32B model show
                                                    that our certified pipeline achieves 92% accuracy on strategy-synthesis
                                                    outcomes.


                                         1     Introduction
                                         Strategic reasoning in Multi-Agent Systems (MAS) is a central topic in Ar-
                                         tificial Intelligence, with applications ranging from autonomous systems and
                                         robotics to security, economics, and distributed control [46, 48]. Temporal log-
                                         ics for strategies, such as Alternating-time Temporal Logic (ATL) and related
                                         formalisms, provide a rigorous framework to reason about the abilities of agents
                                         and coalitions to enforce temporal objectives under strategic interaction [3, 1,
                                         20, 43]. Among these, Natural Alternating-time Temporal Logic (NatATL) was
                                         introduced to capture natural strategic ability [35], where agents are constrained
                                         to strategies that are cognitively simple, interpretable, and aligned with bounded
                                         rationality assumptions. Real-world agents operate under computational and
                                         cognitive limits: strategies with unbounded memory, although theoretically ex-
                                         pressive, are often impossible to implement in practice. NatATL formalizes this
                                         insight by restricting attention to strategies that can realistically be executed
                                         by boundedly rational agents, thereby bridging the gap between formal strategic
                                         reasoning and implementable strategic behavior.
2         M. Aruta et al.

    Despite its conceptual relevance, NatATL faces two major obstacles that
limit its practical adoption. First, existing model-checking procedures rely on
explicit enumeration of admissible natural strategies, leading to an exponential
blow-up in the strategy space. Approaches based on exhaustive generation [37]
become quickly infeasible even for small models or coalitions. The practical bot-
tleneck is therefore not only checking a fixed candidate strategy, but discovering
a promising bounded natural strategy in a vast combinatorial space. Second,
unlike mainstream learning-based or planning-based approaches, NatATL lacks
structured, labelled datasets that could support data-driven methods for strategy
synthesis or approximation. This absence of benchmarks further hinders the ex-
ploration of alternative computational paradigms beyond brute-force reasoning.
Recent advances in Large Language Models (LLMs) offer a promising direction
to address these challenges. LLMs have shown strong capabilities in synthesizing
structured symbolic artifacts from high-level specifications, implicitly navigating
large combinatorial spaces while favoring concise and human-aligned represen-
tations [9, 44, 47]. However, LLM-only synthesis remains unreliable in the sense
required by formal verification: outputs can be subtly incorrect, semantically
inconsistent with the underlying model, or brittle under adversarial counter-
strategies. In safety-critical and formally verified settings, this lack of intrinsic
reliability is unacceptable: what is needed is not merely a plausible strategy, but
a certified one.

Our Contributions. We propose a neuro-symbolic framework for certified strat-
egy synthesis in NatATL. The main contributions of this paper are as follows:

    – LLM-guided certified strategy synthesis. We introduce a generate-and-
      certify framework in which an LLM acts as a strategy-generation oracle for
      NatATL. The LLM proposes candidate natural strategies directly from the
      multi-agent model and the NatATL specification, while a standard NatATL
      model checker formally validates each candidate. Thus, the framework ex-
      ploits LLM guidance to navigate large combinatorial strategy spaces while
      preserving soundness: only verifier-certified strategies are accepted.
    – The first NatATL strategy-synthesis dataset. We construct the first la-
      belled dataset for NatATL strategy synthesis, consisting of 4,211 instances of
      concurrent multi-agent models, NatATL specifications, and expert-validated
      natural strategies. The dataset is built through a human-in-the-loop valida-
      tion process and is designed to support reproducible evaluation of strategy-
      generation oracles and future learning-based approaches.
    – An open-weight and reproducible implementation. We instantiate
      the framework using an open-weight Qwen3-32B model integrated with the
      VITAMIN NatATL verifier [25]. The resulting pipeline supports end-to-end
      strategy generation, syntactic validation, formal certification, and verifier-
      guided refinement, providing a reproducible neuro-symbolic toolchain for
      NatATL reasoning.
    – Empirical evidence of effectiveness and scalability. We evaluate the
      framework on the proposed benchmark and show that the certified pipeline
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics         3

    achieves 92% accuracy on strategy-synthesis outcomes. The experiments also
    show that our approach mitigates the explicit natural-strategy enumeration
    bottleneck, scaling to configurations with up to 50 states, coalitions of 11
    agents, and complexity bounds up to k = 100, while accepting only formally
    certified positive results.

Related Works. Logics for strategic reasoning in Multi-Agent Systems have been
extensively studied as a formal foundation for analyzing the abilities of agents
and coalitions under strategic interaction [28, 29]. Alternating-time Temporal
Logic (ATL) [3] and its numerous extensions ([27, 22, 31, 2, 32, 15, 24, 16, 17, 34])
constitute a well-established framework, with model-checking techniques that
have been refined to address issues such as imperfect information, memory
bounds, and resource constraints [43, 21, 30, 19, 26, 42, 36]. A long line of work
has investigated the trade-off between expressiveness and computational com-
plexity by restricting strategies, for instance to memoryless, bounded-memory, or
resource-aware variants [14, 23, 13, 4, 11]. In this landscape, Natural Alternating-
time Temporal Logic (NatATL) was introduced to capture natural strategic abil-
ity, enforcing strategies that are cognitively simple and human-interpretable [35,
36]. Subsequent developments explored natural strategies in applied domains
and enriched settings, including auctions, voting protocols, and quantitative or
fuzzy extensions [33, 10, 12, 6]. Despite these advances, existing NatATL verifica-
tion procedures fundamentally rely on explicit enumeration of admissible natural
strategies, which leads to severe scalability limitations as the complexity bound
or coalition size increases [37]. In parallel, several approaches have proposed
symbolic, abstraction-based, or reduction techniques to mitigate state-space ex-
plosion in strategic logics [18, 38], yet they do not address the combinatorial
blow-up inherent in natural strategy generation. More recently, large language
models (LLMs) have demonstrated strong capabilities in synthesizing symbolic
artifacts such as programs, logical rules, and proofs from high-level specifica-
tions [9, 39, 44, 47]. Related work has explored the use of LLMs for formal rea-
soning tasks, including mathematical problem solving, program synthesis, and
neural theorem proving [49, 40, 41]. However, these approaches typically lack for-
mal semantic guarantees and are not grounded in logics of strategic ability. In
parallel, LLMs have been employed in agent-based and planning-oriented set-
tings [50, 45], but without a formal treatment of strategic interaction, bounded
rationality, or temporal objectives. To the best our knowledge, no prior work
integrates LLM-guided strategy synthesis with sound NatATL model checking,
nor provides datasets to support such neuro-symbolic approaches. Our work
combines LLM-based natural strategy synthesis with formal verification and in-
troduces the first expert-validated dataset for NatATL.

Outline. Section 2 introduces the necessary preliminaries on natural strategies
and NatATL verification. Section 3 presents the dataset. Section 4 describes the
proposed LLM-guided verification framework. Section 5 reports the experimental
evaluation. Section 6 concludes the paper.
4       M. Aruta et al.

2    Preliminaries

We briefly recall the main notions underlying Natural Alternating-time Temporal
Logic (NatATL) and its model-checking problem. We assume familiarity with
standard concepts from temporal logic and multi-agent systems, and focus on
the aspects that are essential for our framework.

Concurrent Game Structures. A Concurrent Game Structure (CGS) is the stan-
dard semantic model for logics of strategic ability. Formally, a CGS is a tuple
G = (Ag, Ap, {Acta }a∈Ag , St, s0 , d, δ, ℓ), where Ag is a finite set of agents, Ap a
finite set of atomic propositions, Acta the finite set of actions available to agent
a, St a finite set of states with initial state s0 , d(a, s) ⊆ Acta the non-empty
set of actions available to agent a at state s, δ the transition function mapping
states and joint actions to successor states, and ℓ : St → 2Ap a labeling function.
A joint action is a tuple selecting one action per agent, and the evolution of the
system is determined by the collective choices of all agents.

Natural Strategies. Unlike classical ATL, which allows arbitrary (possibly highly
complex) strategies, NatATL restricts attention to natural strategies, intended to
model human-like, interpretable decision rules. A natural memoryless strategy
for an agent a is given by a finite, ordered list of guarded actions

                           sa = ⟨(φ1 , α1 ), . . . , (φn , αn )⟩,

where each guard φi is a propositional formula over Ap, and αi is an action
available to agent a in every state satisfying φi . The last rule is required to have
guard ⊤, ensuring that the strategy is total. At a given state, the agent executes
the action associated with the first guard that holds. A collective natural strategy
for a coalition A ⊆ Ag is a tuple of individual strategies, one for each agent in
A. The outcome of such a strategy from a state s is defined as the set of all
paths that are compatible with the prescribed actions of the coalition, while the
agents outside the coalition are unrestricted.

Strategy Complexity. The defining feature of NatATL is that natural strategies
are subject to a syntactic complexity bound. Complexity is measured as the size
of the propositional guards (e.g., the number of symbols or atomic propositions
occurring in them). A collective strategy is admissible if the sum of the complexi-
ties of its component strategies does not exceed a given bound k. This formalizes
bounded rationality by limiting the descriptive effort required to specify a strat-
egy.

Model Checking Problem. Given a formula of the form ⟨⟨A⟩⟩≤k ψ, the NatATL
model-checking problem asks whether there exists a collective natural strategy
sA for the coalition A such that compl(sA ) ≤ k and every path induced by
sA satisfies the temporal objective ψ. Existing procedures follow this seman-
tics directly: they search over admissible bounded natural strategies and check,
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics            5

                     Setting         MC bound Search bottleneck
                     Mem., fixed k       in P           Nnr (k)
                     Mem., var. k ∆P  2 -complete     exp. in k
                     Recall, fixed k    in ∆P2    NnR (k) + unfold.
                     Recall, var. k  in PSPACE exp. in k + unfold.
Table 1. NatATL model-checking bounds and natural-strategy generation bottlenecks.
                                    2
Here Nnr (k) = O((|P rop| + |Bool|)k |Act|k ) for memoryless strategies, while NnR (k) =
                              2
O((|P rop| + |Bool| + |Con|)k |Act|k ) for recall-based strategies.




for each candidate, whether the induced outcomes satisfy the temporal objec-
tive [35]. Thus, the key scalability barrier is the explicit construction of the
candidate strategy space.
    This bottleneck comes from the representation of natural strategies. In the
memoryless case, a natural strategy is an ordered list of guarded actions, where
each guard is a Boolean condition over atomic propositions. Therefore, the veri-
fier must consider possible guards, possible actions, possible rule orderings, and
possible ways of distributing the global complexity budget across the agents in
the coalition. For strategies of complexity at most k, the number of memoryless
candidates is bounded by
                                                   2
                                                           
                     Nnr (k) = O (|P rop| + |Bool|)k |Act|k .

This term is already exponential in the bound k. Consequently, even when model
checking is polynomial in the model size for fixed k, the hidden constant contains
the bounded-strategy enumeration factor.
   The situation becomes more demanding for natural strategies with recall. In
that setting, guards are regular expressions over Boolean propositional formulas.
The corresponding candidate space is bounded by
                                                      2
                                                              
                NnR (k) = O (|P rop| + |Bool| + |Con|)k |Act|k ,

where Con denotes the regular-expression constructors. Moreover, checking a
fixed recall-based strategy requires reasoning over a bounded unfolding induced
by the strategy and the automata associated with its guards. Table 1 summarizes
the relevant NatATL settings.
    From an algorithmic perspective, the table shows that the practical bot-
tleneck of NatATL model checking is the search for a bounded natural strategy
witness. Once a memoryless candidate strategy is fixed, the model can be pruned
according to the actions prescribed by the strategy and the temporal objective
can be checked on the resulting structure. The expensive step is finding the
candidate in the first place. This is precisely the step that dominates existing
explicit-generation procedures as the complexity bound, the number of actions,
or the coalition size increases.
6       M. Aruta et al.

3     Dataset
The lack of structured benchmarks for NatATL limits the systematic evaluation
of data-driven and neuro-symbolic approaches to natural strategy synthesis. Ex-
isting NatATL verification procedures are primarily designed around exhaustive
generation and checking of bounded natural strategies [37, 8]. While this yields a
sound verification procedure, it does not provide a shared collection of NatATL
instances on which alternative strategy-generation mechanisms can be evaluated
in a reproducible way.
    To address this gap, we introduce a NatATL benchmark dataset consisting
of 4211 concurrent multi-agent models paired with NatATL specifications. Each
instance describes a finite concurrent game structure, a strategic coalition, a
complexity bound, and a NatATL objective to be checked. The dataset is de-
signed as an evaluation benchmark for strategy-synthesis oracles: given a model
and a formula, an external synthesizer, such as an LLM, proposes a natural strat-
egy, which is then certified or rejected by the NatATL verifier. The instances are
intentionally compact enough to be serialized and processed by an LLM within
its context window, while stressing the main sources of combinatorial blow-up in
NatATL verification: coalition size, branching over joint actions, and the com-
plexity bound on natural strategies. This reflects the observation, discussed in
the preliminaries, that the main scalability barrier is not only the number of
states, but the explosion of admissible guarded strategies as the coalition and
the bound grow [7, 37].

3.1   Generation Pipeline
The dataset was constructed through a multi-stage process combining use-case
ideation, expert modeling, automatic consistency checking, controlled augmen-
tation, and verifier-guided coverage analysis. Figure 1 summarizes the overall
pipeline.
    The first stage focused on identifying application domains and interaction
patterns suitable for natural strategic reasoning. A closed-source LLM (i.e.,
Gemini 3.1 Pro) was used only as a high-level ideation aid to suggest candi-
date use cases, including access control, robotics, logistics, traffic management,
medical operations, industrial control, and cyber-physical monitoring. These sug-
gestions were not used directly as formal data. Instead, five domain experts in
strategic logics, multi-agent systems, and formal verification manually filtered
the proposed scenarios, discarding cases that were not naturally expressible as
concurrent game structures or did not involve meaningful strategic interaction.
Starting from the filtered use cases, the experts manually constructed an initial
seed set of NatATL instances. Each instance was encoded as a finite concurrent
game structure with explicit states, agents, available actions, transitions, initial
state, atomic proposition labeling, coalition, and NatATL formula. During this
phase, the experts aimed to cover different strategic patterns, including safety
objectives, reachability objectives, coordinated multi-agent control, adversarial
disruption, and cases where the coalition is intentionally unable to enforce the
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics       7

                                     Use-case
                                     Ideation

                                 Expert Modeling
                                  and Validation

                                   Controlled
                                  Augmentation

                                 Verifier-guided
                                Coverage Analysis


                                  Final Dataset


               Fig. 1. Pipeline for NatATL benchmark construction.


objective under the specified complexity bound. This design choice was essential
to avoid a benchmark biased toward trivially satisfiable formulas.
    All seed instances underwent structural validation before augmentation. We
checked both automatically and through experts human-in-the-loop inspection
that every transition specifies the required joint-action information, that each
action appearing in a transition belongs to the corresponding agent’s declared
action set, that all states referenced by transitions and labelings are declared,
that the initial state belongs to the state space, that all agents appearing in the
coalition are declared in the model, and that all atomic propositions occurring
in the NatATL formula occur in the model labeling. We also normalized Boolean
connectives and state identifiers to ensure compatibility with the NatATL parser
and the VITAMIN bridge.

3.2   Controlled Augmentation
The validated seed set was expanded through controlled augmentation. This
stage was designed to increase structural and lexical diversity while preserving
formal well-formedness. We used three families of augmentation operators.
    The first family consists of semantics-preserving renamings. These transfor-
mations systematically rename states, agents, actions, and atomic propositions
while updating all dependent fields consistently. For example, when an agent is
renamed, the transformation updates the agent list, the action dictionary, the
coalition, the NatATL formula, and all auxiliary fields used internally during
validation. Similarly, action renaming propagates to both the declared action
sets and the joint actions occurring in the transition relation. These transforma-
tions prevent the benchmark from overfitting to a small vocabulary of recurring
names.
    The second family consists of formula-level transformations. These include
increasing the complexity bound, decreasing it without going below the admissi-
8      M. Aruta et al.

ble minimum bound, changing Boolean structure in controlled ways, modifying
local negations, and altering coalition membership when the resulting formula
remains syntactically valid. Unlike pure renaming, these transformations are not
intended to preserve satisfiability in general. Their purpose is to generate harder
negative or borderline instances by changing the strategic requirements imposed
on the coalition. In particular, decreasing the bound can turn a previously feasi-
ble natural strategy into an infeasible one, while increasing the bound preserves
feasibility whenever a strategy was already available under the smaller bound.
All generated formulas are re-parsed after augmentation to ensure NatATL well-
formedness.
    The third family consists of model-level transformations. These include chang-
ing selected state labelings, redirecting or removing individual transitions, adding
admissible transitions, introducing trap states, and adding a controlled disturb-
ing agent whose actions may interfere with coalition progress. These operators
are used conservatively and only when the resulting model remains structurally
valid. The goal is not to add arbitrary noise, but to generate plausible vari-
ants in which strategic success or failure depends on adversarial choices, missing
progress transitions, or additional environmental interference.
    All augmented instances were subjected to the same structural checks as
the seed instances. In addition, formulas with invalid complexity bounds were
rejected or corrected according to the NatATL encoding used by our verifier.
In particular, for non-empty coalitions we require the bound to be at least one,
since a natural strategy contains at least one guarded rule, whereas the zero
bound is only meaningful for degenerate encodings such as the empty-coalition
universal-path case, which is not relevant to our synthesis objective.

Verifier-guided coverage analysis. After the first augmentation stage, we used
the NatATL verification pipeline to inspect the semantic coverage of the gener-
ated instances, to avoid the dataset being dominated by a single outcome class.
This is important because, for instance, an overwhelmingly negative benchmark
would make it difficult to assess whether a synthesis oracle can both refrain from
proposing impossible strategies and generate certifiable winning strategies when
such strategies exist. Accordingly, we used verifier outcomes to identify under-
represented satisfiable and borderline regions of the instance space, and then
applied an additional conservative augmentation round to improve coverage of
these regions. This second augmentation round used only transformations that
preserve, or monotonically relax, the underlying winning pattern. In particular,
we allowed agent renaming, action renaming, reordering of transitions, reordering
of declared actions, and increases of the complexity bound. We avoided transfor-
mations that may change satisfiability, such as changing the labeling, redirecting
transitions, decreasing the bound, modifying the temporal objective, changing
the coalition size, or adding new adversarial dynamics. This conservative policy
preserves the strategic structure of the source instances while increasing lexical
and syntactic diversity. The final dataset contains 4211 NatATL instances. To
prevent inflated evaluation due to near-duplicate augmented variants, all exper-
imental splits are performed at the level of augmentation families rather than
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics          9

individual JSON objects. Thus, instances derived from the same seed are as-
signed to the same split. This avoids parent-child leakage between development
and evaluation data and ensures that reported results measure generalization to
unseen strategic structures rather than memorization of renamed variants.

Data format and schema. Each dataset element is represented as a JSON object.
The released benchmark focuses on the fields required by the strategy synthesis
and verification pipeline. The main field is input, which contains the concurrent
game structure and the NatATL specification: states, agents, actions, transitions,
initial_state, labeling, coalition, formula_natatl. The field states lists the finite
state space; agents lists the agents of the model; actions maps each agent to
its admissible actions; transitions encodes the transition relation through source
states, joint actions, and target states; initial_state specifies the state from which
verification starts; labeling maps states to atomic propositions; coalition identifies
the strategic coalition; and formula_natatl stores the bounded NatATL objec-
tive. Additional metadata track identifiers, parent-child relations introduced by
augmentation, augmentation type, and a natural language note describing the
strategic objective.

4    LLM-Guided NatATL Verification Framework
Figure 2 summarizes the end-to-end workflow of our tool, which integrates an
open-weight LLM, Qwen3-32B, with the VITAMIN NatATL verifier in a verifier-
in-the-loop synthesis setting. Each input instance consists of a concurrent game
structure, a labeling function, a NatATL specification, a strategic coalition, and
a complexity bound. The pipeline first converts this information into a struc-
tured prompt that exposes the relevant model components and specifies the
required strategy format. The LLM then generates a candidate memoryless nat-
ural strategy. In our setting, a candidate strategy is represented as an ordered
list of guarded actions for each agent in the coalition, together with a default rule
ensuring totality. Before invoking the verifier, the generated output is parsed and
checked against the expected schema. Outputs that are not valid JSON, refer
to unknown agents, states, propositions, or actions, omit required default rules,
or violate the declared strategy format are rejected before semantic verification.
If the candidate passes these preliminary checks, it is submitted to VITAMIN.
The verifier checks whether the strategy is well formed, respects the NatATL
complexity bound, prescribes only admissible actions, and satisfies the target
objective under the NatATL semantics. When the strategy is winning, VITA-
MIN returns a certified positive result together with the synthesized strategy as
a witness. When the strategy is rejected, the verifier returns diagnostic infor-
mation, which can be translated into feedback for a bounded refinement round.
The loop terminates when a strategy is certified, when the LLM fails to produce
a valid candidate, or when the retry budget is exhausted.

Prompt Design. The prompt was designed to make the LLM produce explicit
memoryless natural strategies in a format that can be parsed and checked au-
10      M. Aruta et al.


                                   Input




                                                             Verifier feedback
                                Qwen3-32B
                            Strategy Synthesizer


                              VITAMIN Verifier
                          (NatATL Model Checking)


                            Certified Result
                    (sat/unsat + strategy or witness)

Fig. 2. End-to-end tool pipeline. Given a NatATL instance, Qwen3-32B synthesizes
candidate natural strategies, which are formally verified by the VITAMIN model
checker. Unsatisfied candidates trigger an iterative verifier-guided refinement loop,
while successful ones yield certified verification results.


tomatically. Each prompt contains the concurrent game structure, the coalition,
the complexity bound, and the NatATL objective. The required output is a
JSON object encoding, for each coalition agent, an ordered list of guarded ac-
tions together with a default rule. We initially evaluated both fine-tuning and
one-shot prompting strategies using Qwen2.5-32B-4bit. In preliminary exper-
iments, Qwen2.5 often failed to produce stable JSON outputs conforming to
the required schema, independently of whether fine-tuning was used. We there-
fore switched to Qwen3-32B-4bit, whose reasoning mode produced substantially
more stable structured outputs. Based on this behavior, we adopted a one-shot
prompting strategy rather than a fine-tuning pipeline. Prompt development was
performed on a development subset of 200 instances. At each iteration, we an-
alyzed representative failures, including invalid JSON, incorrect interpretation
of NatATL objectives, missing default rules, complexity-bound violations, and
strategies rejected by the verifier. The prompt was then refined to make the
output schema more explicit and to clarify the semantics of guarded natural
strategies. The refinement process stabilized after approximately six iterations.
Finally, we introduced a compact markdown representation of the input model,
derived from the original JSON encoding. This representation reduces prompt
length and makes states, labels, actions, and transitions easier to inspect. In our
development experiments, this conversion improved accuracy by approximately
3 percentage points, likely by reducing attention dilution caused by long JSON
encodings of multi-agent systems.

Implementation Details. The pipeline is entirely implemented in Python and
integrates Qwen3-32B with the VITAMIN model checker. All inference experi-
ments were run on a Linux machine with 12 CPU cores, 64 GB of RAM, and
an NVIDIA Quadro RTX A5000 GPU. We used the 4-bit quantized model
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics        11

unsloth/Qwen3-32B-bnb-4bit with reasoning mode enabled. VITAMIN is used
as the verification backend for NatATL [25]. This choice is motivated by its open-
source implementation and by its modular architecture, which allows direct inte-
gration with Python and explicit inspection of strategy-evaluation components.
In our pipeline, VITAMIN is responsible for checking whether a candidate strat-
egy is syntactically valid, respects the NatATL complexity bound, prescribes
only admissible actions, and satisfies the target formula on the given model.
Before invoking the verifier, each LLM output is parsed and checked against
the strategy schema. Invalid outputs are classified as parsing or schema failures.
These include malformed JSON, unknown agents, unknown actions, malformed
guards, missing default rules, and outputs that cannot be mapped to the coali-
tion specified in the input formula. When allowed by the retry budget, such
failures are converted into feedback for a subsequent LLM attempt. The same
feedback mechanism is used when VITAMIN rejects a syntactically valid but
losing strategy. In that case, the verifier diagnosis is translated into a natural-
language message describing why the candidate failed, for example because a
prescribed action is not admissible, a guard does not cover the required cases,
or the induced outcomes violate the temporal objective. This feedback is then
appended to the next query in the refinement loop.



Outcome Classification. To evaluate the LLM-guided synthesis pipeline, we in-
terpret each run as a strategy-synthesis outcome. The LLM may either output
a candidate strategy or fail to produce a valid one. If a candidate is produced,
NatATL verification is used to decide whether the strategy is a certified winning
strategy. In addition, we use an ATL pre-filter as a feasibility signal. The ATL
pre-filter is not a replacement for NatATL verification. ATL checks whether a
winning strategy exists in the unconstrained ATL sense. Since NatATL restricts
admissible strategies to bounded natural strategies, a negative ATL result rules
out NatATL satisfiability, whereas a positive ATL result only indicates that a
winning strategy may exist before imposing the NatATL natural-strategy bound.
Thus, ATL is used only to distinguish cases where failure is expected from cases
where the LLM may have failed to find a strategy even though the unconstrained
strategic objective is feasible. Algorithm 1 reports the resulting verification loop.
The procedure first queries the LLM for a candidate strategy. If no valid strat-
egy is produced, the ATL pre-filter is used to distinguish true negatives from
false negatives. If a candidate strategy is produced, the NatATL verifier checks
it. Accepted candidates are classified as true positives. Rejected candidates are
classified as false positives, and if the ATL check indicates that a winning strat-
egy exists in the unconstrained sense, the verifier feedback is used to trigger a
bounded retry. This classification protocol is used only for empirical evaluation.
The soundness guarantee of the framework concerns accepted positive answers: a
strategy is returned as successful only if it has been certified by the NatATL ver-
ifier. All other labels describe failure modes of the LLM-guided synthesis process
under the chosen retry and token budgets.
12      M. Aruta et al.

Algorithm 1 LLM-based Strategy Synthesis and Verification for NatATL
Require: MAS M , NatATL formula φ, LLM Q
Ensure: Prediction P ∈ {TP, TN, FP, FN}, candidate strategy S
 1: resp ← Q.ask(M, φ)
 2: feedback ← ⊥
 3: if resp does not contain a valid candidate strategy then
 4:     (atl , _, _) ← verify(M, ⊥)
 5:     if ¬atl then
 6:         return (TN, ⊥)
 7:     else
 8:         feedback ← “A strategy may exist; generate a valid JSON strategy.”
 9:         resp ← Q.retry(feedback )
10:     end if
11: end if
12: if resp contains a valid candidate strategy then
13:     (atl , nat, S) ← verify(M, resp)
14:     if nat then
15:          return (TP, S)
16:     else if ¬atl then
17:          return (FP, S)
18:     else
19:          feedback ← verifier diagnostic for S
20:          resp ← Q.retry(feedback )
21:          if resp contains a valid candidate strategy then
22:              (_, nat, S) ← verify(M, resp)
23:              if nat then
24:                  return (TP, S)
25:              else
26:                  return (FP, S)
27:              end if
28:          else
29:              return (FN, ⊥)
30:          end if
31:     end if
32: end if
33: return (FN, ⊥)



5    Experiments

To avoid unnecessary exhaustive exploration of the NatATL strategy space, our
pipeline integrates an ATL pre-filtering phase before invoking full NatATL veri-
fication [8]. The rationale is that NatATL strategy synthesis is computationally
expensive and becomes pointless when no winning strategy exists. While ATL
does not synthesize strategies, it can efficiently determine whether a solution
does not exist for the given model and objective. Leveraging ATL as a prelim-
inary feasibility oracle therefore allows us to prune worst-case instances early,
preventing the LLM from wasting computation on strategies that are guaranteed
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics        13

                      LLM      NatATL       ATL        Label
                    false        *       false       TN
                    false        *       true        FN
                    true      false      false    FP–halt
                    true      false      true    FP–retry
                    true       true        *         TP
       Table 2. Outcome matrix for the LLM-driven strategy synthesis tool.



to fail under the fixed bound. Moreover, ATL checking is already embedded in
real time within VITAMIN, and thus introduces negligible computation time
overhead compared to NatATL verification. This makes the pre-filter not only
a scalability optimization, but also a key component for improving training re-
liability: it provides structured signals that help distinguish genuine negative
cases from bound-related failures. Table 2 reports the possible outcomes of our
pipeline. If the LLM does not output any strategy, the model-checking step is
not applicable ("*") and we use the ATL checker to distinguish: (i) TN when
ATL=false (no winning strategy exists), and (ii) FN when ATL=true (a win-
ning strategy exists but the LLM failed to produce one; an exhaustive NatATL
search may be required). If the LLM outputs a strategy but the NatATL model
checker rejects it (NatATL=false), we classify the candidate as a false positive
and use the ATL checker to decide whether to halt (FP-halt, ATL=false) or
to run an additional refinement round (FP-retry, ATL=true). Finally, if the
NatATL model checker validates the strategy (NatATL=true), the outcome is a
TP and the ATL checker is unnecessary ("*").

Results. After the strategy synthesis, we interpreted the results as a classification
problem by labeling each sample as True Positive, True Negative, False Positive
and False Negative, based on the analysis pipeline as reported in the Outcome
interpretation paragraph. From the confusion matrix (Figure 3) we see that the
LLM synthesis is very good, 41 instances over 1411 are marked as false positive
and 72 as false negative, this means that LLM with thinking modalities could
cope with MAS of small to medium complexities under NatATL formula con-
straints with excellent accuracy of 92%. The time distribution that the pipeline
required for each sample is plotted in Figure 4, it best fits a Gamma distribution
of parameters shape = 1.53, loc = 32.23, scale = 101.72. By inferencing with
at least two LLM iterations, we explicitly let the model to better handle the
true-false-true outcome in table 2 (LLM outputs a candidate, NatATL model
checking fails, while the ATL checker indicates that a winning strategy exists).
This case is hard to improve with a single LLM iteration, because without a
second iteration the system cannot provide actionable feedback of the form: "a
strategy does not exist for the given bound k, but it may exist for larger bounds".
Such feedback helps the LLM interpret the instance correctly without forcing it
to always output a strategy, i.e., without implicitly encouraging it to ignore the
resource bound when assessing feasibility. We, finally, need to mention the fact
14      M. Aruta et al.

that not all samples are decidable under our framework because of the inherent
limitation of our experimental setup, we had to put a cap on the maximum token
number of 8192, this makes that not all samples become decidable in the sec-
ond query (or even in the first) to LLM giving a truncated output. Those cases
are marked as ParsingError and do not contribute to the performance metrics.
Those ParsingError account for 51 samples and are not included into the final
dataset samples.




                             Fig. 3. Confusion Matrix.


    Table 3 highlights the radically different scalability behavior of current vali-
dated tools at the nowadays state of art ([37]) and our approach when the size
of the model, the coalition, and the complexity bound grow. NatSTV exhibits a
clear exponential blow-up already at very small scales. While verification remains
fast for models with up to 6 states, performance rapidly deteriorates as soon as
the number of states and coalition agents increases. In particular, moving from
8 to 12 states causes an increase of more than one order of magnitude in run-
time, ultimately leading to a timeout at 14 states. This confirms that NatSTV
suffers heavily from the symbolic encoding of strategy choices combined with
bounded complexity, which quickly saturates the underlying verification engine.
In contrast, our tool maintains stable and predictable performance even under
significantly larger configurations. Although the absolute runtime is higher for
very small instances (due to explicit strategy reasoning rather than symbolic
shortcuts), the growth remains smooth and controlled as both the coalition size
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics     15




                       Fig. 4. Time distribution in seconds.


            Tool      #States |C| kmax Verification time (s)
            NatSTV             6    2      6                    ≈ 0.8
            NatSTV             8    2      8                   ≈ 12.4
            NatSTV           10     3      8                   ≈ 95.7
            NatSTV           12     3    10                  ≈ 312.5
            NatSTV           14     3    10                  timeout
            Our Tool           6    2      3                    ≈ 70
            Our Tool         10     2      5                    ≈ 80
            Our Tool         20     5    10                    ≈ 120
            Our Tool         50 11      100                    ≈ 200
             Table 3. Scalability comparison between existing tools.




and kmax increase. Notably, our approach successfully handles models with up
to 50 states, coalitions of size 11, and bounds as high as k = 100, remaining well
within practical verification time. This demonstrates that the bottleneck affect-
ing NatSTV and the other proposed tools in literature is effectively mitigated
in our framework, which scales with the structure of the strategy space rather
than collapsing under symbolic explosion.




Reproducibility. We provide the source code and data used for the reproducibility
of the experiments, you can download them at: [5].
16     M. Aruta et al.

6    Conclusions
We introduced a neuro-symbolic framework for certified strategy synthesis in
NatATL, where LLMs act as strategy-generation oracles that propose natural
strategies directly from a multi-agent model and a NatATL specification. Rather
than replacing formal verification, the LLM is embedded in a generate-and-
certify pipeline: candidate strategies are accepted only when formally validated
by the NatATL model checker. This design preserves soundness while avoiding,
in successful cases, the exhaustive enumeration of bounded natural strategies. We
focused on NatATL because its bounded-rationality assumptions naturally cap-
ture the implementability constraints of real-world agents. Natural strategies are
required to be simple, interpretable, and bounded in syntactic complexity, mak-
ing them well aligned with practical strategic reasoning. This perspective also
provides a natural interface with LLM-based synthesis, where token budgets and
context-window limitations impose their own form of bounded reasoning. To sup-
port systematic evaluation, we introduced the first NatATL strategy-synthesis
dataset, consisting of 4,211 instances of multi-agent games, NatATL specifica-
tions, and expert-validated natural strategies. The dataset provides a reusable
benchmark for evaluating strategy-generation oracles and for developing future
learning-based approaches to natural strategic reasoning. Our experiments show
that an open-weight Qwen3-32B model, coupled with formal certification, can
effectively synthesize natural strategies for small- to medium-sized multi-agent
systems. On the evaluated benchmark split, the proposed pipeline achieves 92%
accuracy on strategy-synthesis outcomes, while every accepted positive result
is backed by verifier certification. The results also show a favorable scalabil-
ity profile compared with exhaustive natural-strategy verification, with our tool
handling configurations up to 50 states, coalitions of 11 agents, and complexity
bounds up to k = 100. At the same time, our study highlights practical limita-
tions of LLM-guided verification. The maximum context length constrains the
size of the serialized multi-agent models that can be processed by the LLM, and
GPU memory limits the scale of inference for larger instances. These limitations
suggest several directions for future work, including more compact model encod-
ings, verifier-guided prompt compression, fine-tuning or distillation for NatATL-
specific synthesis, and broader comparisons across open-weight and proprietary
LLMs. Overall, our results indicate that LLM-guided synthesis combined with
formal certification is a promising direction for scaling natural strategic reason-
ing without sacrificing correctness guarantees.

Future Works. This seminal study represents a springboard for various directions
to explore in the future. The first task we have identified is the creation of a
dataset and a format to standardize a benchmark for further studies on MAS
synthesis. This would allow us to measure the progress of the field, making
scientific works comparable. Furthermore, reasoning methods have recently been
introduced in small-scale LLM programs; we expect exponential improvements
over time, so a standardized benchmark could highlight these improvements.
Another promising direction is fine-tuning through distillation of largest LLM
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics      17

in which a basic LLM is fine-tuned specifically for model synthesis. Finally, a
specific study to test the strategic capabilities of different LLM models, both
open source and proprietary, would be interesting, in order to create a line of
research to improve the strategic capabilities of future LLMs.

References
 1. Ågotnes, T.: Action and knowledge in alternating-time temporal logic. Synthese
    149(2), 375–407 (2006)
 2. Alechina, N., Logan, B., Nga, N.H., Rakib, A.: Resource-bounded alternating-time
    temporal logic. In: AAMAS 2010. p. 481–488. IFAAMAS (2010)
 3. Alur, R., Henzinger, T.A., Kupferman, O.: Alternating-time temporal logic. Jour-
    nal of the ACM (JACM) 49(5), 672–713 (2002)
 4. Aminof, B., Giacomo, G.D., Lomuscio, A., Murano, A., Rubin, S.: Synthesizing
    best-effort strategies under multiple environment specifications. In: KR 2021. pp.
    42–51 (2021)
 5. Anonymous: Source code for reproducibilty. https://figshare.com/s/6234b3d6607b22f2fce5
    (1 2026)
 6. Aruta, M., Improta, F., Malvone, V., Murano, A.: When natural strategies
    meet fuzziness and resource-bounded actions (extended version). arXiv preprint
    arXiv:2512.20457 (2025)
 7. Aruta, M., Malvone, V., Murano, A.: A model checker for natural strategic ability.
    arXiv preprint arXiv:2410.14374 (2024)
 8. Aruta, M., Malvone, V., Murano, A.: S4h: A tool for synthesizing human-like
    strategies (2025)
 9. Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E.,
    Cai, C., Terry, M., Le, Q., et al.: Program synthesis with large language models.
    arXiv preprint arXiv:2108.07732 (2021)
10. Belardinelli, F., Jamroga, W., Malvone, V., Mittelmann, M., Murano, A., Perrussel,
    L.: Reasoning about human-friendly strategies in repeated keyword auctions. arXiv
    preprint arXiv:2201.09616 (2022)
11. Belardinelli, F., Jamroga, W., Mittelmann, M., Murano, A.: Verification of stochas-
    tic multi-agent systems with forgetful strategies. In: AAMAS 2024. pp. 160–169.
    IFAAMAS/ ACM (2024)
12. Berthon, R., Katoen, J.P., Mittelmann, M., Murano, A.: Natural strategic ability
    in stochastic multi-agent systems. In: AAAI 2024. vol. 38, pp. 17308–17316 (2024)
13. Berthon, R., Maubert, B., Murano, A.: Decidability results for ATL* with imper-
    fect information and perfect recall. In: AAMAS 2017. pp. 1250–1258. ACM (2017)
14. Bulling, N., Dix, J., Jamroga, W.: Model checking logics of strategic ability: Com-
    plexity. In: Specification and Verification of Multi-Agent Systems, pp. 125–159.
    Springer (2010)
15. Bulling, N., Goranko, V.: Combining quantitative and qualitative reasoning in con-
    current multi-player games. Autonomous Agents and Multi-Agent Systems 36(1),
    2 (2022)
16. Catta, D., Ferrando, A., Malvone, V.: Resource action-based bounded ATL: A new
    logic for MAS to express a cost over the actions. In: PRIMA 2024. pp. 206–223.
    LNCS 15395, Springer (2024)
17. Catta, D., Leneutre, J., Malvone, V., Murano, A.: Obstruction alternating-time
    temporal logic: A strategic logic to reason about dynamic models. In: AAMAS
    2024. pp. 271–280 (2024)
18      M. Aruta et al.

18. Cermák, P., Lomuscio, A., Mogavero, F., Murano, A.: MCMAS-SLK: A model
    checker for the verification of strategy logic specifications. In: CAV 2014. pp. 525–
    532. LNCS 8559, Springer (2014)
19. Cermák, P., Lomuscio, A., Murano, A.: Verifying and synthesising multi-agent
    systems against one-goal strategy logic specifications. In: AAAI 2015. pp. 2038–
    2044. AAAI Press (2015)
20. Chatterjee, K., Henzinger, T.A., Piterman, N.: Strategy logic. Information and
    Computation 208(6), 677–693 (2010)
21. Chen, T., Forejt, V., Kwiatkowska, M.Z., Parker, D., Simaitis, A.: Prism-games:
    A model checker for stochastic multi-player games. In: TACAS 2013. pp. 185–191.
    LNCS 7795, Springer (2013)
22. Chen, T., Lu, J.: Probabilistic alternating-time temporal logic and model checking
    algorithm. In: FSKD 2007. pp. 35–39. IEEE Computer Society (2007)
23. Dima, C., Tiplea, F.L.: Model-checking atl under imperfect information and perfect
    recall semantics is undecidable. arXiv preprint arXiv:1102.4225 (2011)
24. Ferrando, A., Luongo, G., Malvone, V., Murano, A.: Theory and practice of quan-
    titative ATL. In: PRIMA 2024. pp. 231–247. LNCS 15395, Springer (2024)
25. Ferrando, A., Malvone, V.: VITAMIN: verification of A multi agent system. In:
    AAMAS 2025. pp. 3023–3025. IFAAMAS (2025)
26. Gutierrez, J., Najib, M., Perelli, G., Wooldridge, M.J.: EVE: A tool for temporal
    equilibrium analysis. In: ATVA 2018. pp. 551–557. LNCS 11138, Springer (2018)
27. Henzinger, T.A., Prabhu, V.S.: Timed alternating-time temporal logic. In: FOR-
    MATS 2006. pp. 1–17. LNCS 4202, Springer (2006)
28. van der Hoek, W., Wooldridge, M.: On the logic of cooperation and propositional
    control. Artificial intelligence 164(1-2), 81–119 (2005)
29. Van der Hoek, W., Wooldridge, M.: Multi-agent systems. Foundations of Artificial
    Intelligence 3, 887–928 (2008)
30. Huang, X., van der Meyden, R.: Symbolic model checking epistemic strategy logic.
    In: AAAI 2014. pp. 1426–1432. AAAI Press (2014)
31. Jamroga, W.: A temporal logic for stochastic multi-agent systems. In: PRIMA
    2008. pp. 239–250. LNCS 5357, Springer (2008)
32. Jamroga, W., Konikowska, B., Kurpiewski, D., Penczek, W.: Multi-valued verifi-
    cation of strategic ability. Fundam. Informaticae 175(1-4), 207–251 (2020)
33. Jamroga, W., Kurpiewski, D., Malvone, V.: Natural strategic abilities in voting
    protocols. In: STAST 2020. pp. 45–62. LNCS 12812, Springer (2020)
34. Jamroga, W., Kwiatkowska, M., Penczek, W., Petrucci, L., Sidoruk, T.: Proba-
    bilistic timed ATL. In: AAMAS 2025. pp. 1051–1059. IFAAMAS / ACM (2025)
35. Jamroga, W., Malvone, V., Murano, A.: Natural strategic ability. Ar-
    tif. Intell. 277 (2019). https://doi.org/10.1016/J.ARTINT.2019.103170,
    https://doi.org/10.1016/j.artint.2019.103170
36. Jamroga, W., Malvone, V., Murano, A.: Natural strategic ability under imperfect
    information. In: AAMAS 2019. pp. 962–970. IFAAMAS (2019)
37. Kaminski, M., Kurpiewski, D., Jamroga, W.: Natstv: Towards verification of nat-
    ural strategic ability. In: IJCAI 2025. pp. 16–22 (2025)
38. Kurpiewski, D., Pazderski, W., Jamroga, W., Kim, Y.: Stv+reductions: Towards
    practical verification of strategic ability using model reductions. In: AAMAS 2021.
    pp. 1770–1772. ACM (2021)
39. Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J., Leblond, R., Eccles,
    T., Keeling, J., Gimeno, F., Dal Lago, A., et al.: Competition-level code generation
    with alphacode. Science 378(6624), 1092–1097 (2022)
      A Neuro-Symbolic Approach to Strategy Synthesis for Strategic Logics            19

40. Li, Z., Zhou, Z., Yao, Y., Zhang, X., Li, Y.F., Cao, C., Yang, F., Ma, X.: Neuro-
    symbolic data generation for math reasoning. Advances in Neural Information Pro-
    cessing Systems 37, 23488–23515 (2024)
41. Liu, H., Fu, Z., Ding, M., Ning, R., Zhang, C., Liu, X., Zhang, Y.: Logical reasoning
    in large language models: A survey. arXiv preprint arXiv:2502.09100 (2025)
42. Lomuscio, A., Qu, H., Raimondi, F.: MCMAS: an open-source model checker for
    the verification of multi-agent systems. Int. J. Softw. Tools Technol. Transf. 19(1),
    9–30 (2017)
43. Mogavero, F., Murano, A., Perelli, G., Vardi, M.Y.: Reasoning about strategies: On
    the model-checking problem. ACM Trans. Comput. Log. 15(4), 34:1–34:47 (2014)
44. Pan, L., Albalak, A., Wang, X., Wang, W.: Logic-lm: Empowering large language
    models with symbolic solvers for faithful logical reasoning. In: EMNLP 2023. pp.
    3806–3824 (2023)
45. Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., Yao, S.: Reflexion: Lan-
    guage agents with verbal reinforcement learning. Advances in Neural Information
    Processing Systems 36, 8634–8652 (2023)
46. Shoham, Y., Leyton-Brown, K.: Multiagent systems: Algorithmic, game-theoretic,
    and logical foundations. Cambridge University Press (2008)
47. Tantakoun, M., Muise, C., Zhu, X.: Llms as planning formalizers: A survey for
    leveraging large language models to construct automated planning models. In:
    ACL 2025. pp. 25167–25188 (2025)
48. Wooldridge, M.: An introduction to multiagent systems. John wiley & sons (2009)
49. Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q.V., Zhou, D., Chen, X.: Large language
    models as optimizers. In: ICLR 2024. OpenReview.net (2024)
50. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K.R., Cao, Y.: React:
    Synergizing reasoning and acting in language models. In: ICLR 2023. OpenRe-
    view.net (2023)
