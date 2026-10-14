                                                        Less Effort, Shorter Proofs: Reinforcement Learning
                                                             for Security Protocol Analysis in Tamarin
                                                 Matthias Cosler1 , Cas Cremers1 , Bernd Finkbeiner1,2 , Mohamed Ghanem1 , Niklas Medinger1
                                                                       1 CISPA Helmholtz Center for Information Security, Saarbrücken, Germany
                                                                                     2 Technical University of Munich, Munich, Germany

                                                        {matthias.cosler, cremers, finkbeiner, mohamed.ghanem, niklas.medinger}@cispa.de
                                         Abstract                                                                        fail to guide Tamarin towards an automatic proof, users may even
                                         Tools like Tamarin and ProVerif have achieved notable success in                manually construct a proof by exploring the search tree themselves
                                         analyzing and verifying complex real-world protocols such as EMV,               and applying proof steps as they see fit.
arXiv:2605.23643v1 [cs.CR] 22 May 2026




                                         5G, and WPA2, even detecting zero-day exploits. Despite these suc-                  All of these forms of human assistance require expert insight into
                                         cesses, verifying such protocols remains a time-consuming, chal-                the protocol being verified and the internals of the Tamarin prover
                                         lenging task, often requiring significant human effort and expertise.           to understand why an automatic proof fails and how to accomplish
                                            In this paper, we present a reinforcement learning (RL) frame-               it. Acquiring this insight is time-consuming and requires multiple
                                         work inspired by AlphaZero and AlphaProof that implements a                     iterations of trial and error, as users have to repeatedly inspect failed
                                         new style of proof search for Tamarin. We have developed a state-               proof attempts. As a result, verifying large, complex protocols can
                                         less API for Tamarin that acts as a classical RL environment. We                take up to months [7, 8, 12, 14].
                                         guide a Monte Carlo Tree Search (MCTS) by a neural heuristic that                   The human effort still required places symbolic protocol verifi-
                                         learns from completed subproofs. We evaluate our framework on 16                cation well behind the automation level achieved in other domains,
                                         case studies, ranging from classical protocol models to challenging             such as game-playing, e.g., Chess and Go, or, more recently, mathe-
                                         state-of-the-art protocol models from recent publications.                      matical theorem proving. Like symbolic protocol verification, these
                                            Our method finds more proofs automatically than Tamarin’s                    domains are also characterized by large, potentially infinite search
                                         standard search and produces shorter proofs than both the standard              spaces and complex decision making.
                                         and human-engineered heuristics. Our pipeline is applicable out                     In the case of game-playing, Google’s AlphaZero [34] achieved
                                         of the box to assist Tamarin users in active research, reducing                 superhuman performance in Go, Chess, and Shogi by combining
                                         the human effort required. Moreover, our standardized interface                 neural networks that evaluate the game state and predict promising
                                         provides a programmatic way for users to interact with Tamarin.                 moves with a Monte Carlo Tree Search (MCTS) algorithm that
                                         Finally, our work demonstrates the promising potential of adapting              explores the game tree guided by the neural network’s predictions.
                                         RL-based methods to the Tamarin domain.                                         AlphaZero was trained purely through self-play via reinforcement
                                                                                                                         learning, without any human data or domain-specific heuristics.
                                                                                                                             In the case of theorem proving, AlphaProof [20] recently claimed
                                         1    Introduction                                                               silver-medal-level performance at the International Mathematical
                                         Over the last years, symbolic security protocol verification has had            Olympiad (IMO) 2024 by adapting a similar combination of neural
                                         many success stories, as tools like Tamarin [29] and ProVerif [4]               networks and MCTS to the domain of formal mathematics in the
                                         have been used to verify large, complex real-world protocols, like              Lean theorem prover. Following the same principle as AlphaZero,
                                         WPA2 [11], TLS 1.3 [9, 10], 5G [14, 30], EMV [15], Signal [22],                 AlphaProof generates its own training data through proof attempts
                                         Apple’s iMessage [26], SPDM [7, 8], and WireGuard [17], making                  rather than self-play. Additionally, it was pretrained on mathe-
                                         them the de-facto standard verifiers in the field.                              matical text and uses test-time reinforcement learning (TTRL) for
                                            Despite these successes, verifying such large real-world proto-              particularly hard problems. These achievements raise the question
                                         cols remains a time-consuming, challenging task, often requiring                of whether similar machine learning and search techniques can be
                                         significant human expertise and manual effort. This is due to the fact          applied to the domain of symbolic protocol verification, increasing
                                         that the verifiers used often fail to scale to the size and complexity          automation and reducing the human effort required.
                                         of state-of-the-art security protocols, resulting in non-terminating                In this work, we address and positively answer this question by
                                         proof attempts. In this case, the user might have to simplify the               developing a reinforcement learning system that guides the proof
                                         model, potentially decreasing its faithfulness to the real protocol,            search of the Tamarin prover, learning from previous proof attempts
                                         and thus the value of the verification. Alternatively, if the verifier          to select better proof steps and find proofs that previously could
                                         allows it, the user has to manually assist the tool’s proof effort in           not be found without human heuristics.
                                         some way.                                                                           To implement our RL system, we had to overcome multiple chal-
                                            In the case of the Tamarin prover, users can inspect failed proof            lenges: First, Tamarin is primarily an automated model checker.
                                         attempts via its graphical user interface to find out where and why             While it also offers some interactivity via a graphical user inter-
                                         the proof failed. Then they can assist the tool by providing it with a          face, there is no interface to programmatically interact with its
                                         heuristic that selects better proof steps to apply to the proof state, or       proof search, which is required to integrate it into a reinforcement
                                         by specifying intermediate lemmas which reduce the search space                 learning system. Second, each step in Tamarin’s proof search is com-
                                         and need to be independently proven [3]. Should all of these efforts            putationally expensive, as it invokes Tamarin’s constraint-solving
                                                                                                                     1
                                                                                                             Cosler, Cremers, Finkbeiner, Ghanem, Medinger


procedure, thus limiting the search space we can explore. This is           the agent observes the current state 𝑠, selects an action 𝑎, receives
contrary to classical reinforcement learning environments, where            a scalar reward 𝑟 , and the environment transitions to a successor
the environment is typically fast to interact with, allowing for            state 𝑠 ′ . The agent’s objective is to learn a policy, a mapping from
millions of interactions during training. Third, Tamarin is special-        states to distributions over actions, that maximizes the expected cu-
ized for symbolic protocol verification, a domain with far fewer            mulative reward. The value function 𝑉 (𝑠) estimates this reward for
existing formal proofs than first-order mathematics. In contrast,           state 𝑠 under the current policy. We differentiate between the state
related work in theorem proving relies heavily on pretraining on            of the environment and the agent’s observation. While the state cap-
large corpora of existing proofs (in the case of AlphaProof [20],           tures all information that determines the environment’s dynamics,
80 million auto-formalized statements). This makes pretraining at           the observation can be a partial or transformed representation of it.
a comparable scale infeasible, so our agent must learn effectively
                                                                               Monte Carlo Tree Search and AlphaZero. Monte Carlo Tree
from self-generated experience on individual protocols, without
                                                                            Search (MCTS) is a best-first search algorithm that builds a search
access to large-scale training data.
                                                                            tree incrementally through repeated simulations [5]. Each simula-
    Contributions. Our contributions are:                                   tion consists of four phases: selection, where the algorithm traverses
     (1) We extend the Tamarin prover with a reusable API, allow-           the tree from the root, choosing the most promising child at each
         ing users to programmatically interact with it. Using this         node; expansion, where a new node is added; evaluation, where the
         API, Tamarin becomes a stateless REST server queried by            new state’s value is estimated; and backup, where the obtained value
         external clients that store the state of the proof search.         is propagated back up the path to update ancestor statistics. The
         This design allows users to easily implement custom proof          classical UCT algorithm [23] balances exploitation and exploration
         search algorithms, including reinforcement learning-based          by deriving a selection formula from upper confidence bounds for
         ones, without having to modify Tamarin’s source code.              multi-armed bandits. AlphaZero [34] extends MCTS by replacing
     (2) We use this API to implement an RL agent combining a tree          the random rollout with a neural network 𝑓𝜃 that, given a state 𝑠,
         search algorithm inspired by AlphaZero [34] with a neural          outputs a prior distribution p assigning a probability to each action
         model that learns to interpret the proof state and outputs a       and a scalar value estimate 𝑣 ≈ 𝑉 (𝑠). This constitutes an actor-critic
         policy, i.e., which proof method to apply next, and a value,       architecture: The policy head (actor) proposes promising actions,
         estimating the distance to a complete proof from this state.       while the value head (critic) evaluates state quality. For selection,
     (3) We evaluate our RL agent on a set of protocols from the            AlphaZero uses the PUCT rule [34, 35], which replaces the UCT
         Tamarin prover’s GitHub repository and recent publica-             exploration term with one guided by the learned priors and values:
         tions. We show that our agent can learn to prove proper-                                                      √︁
                                                                                                                          𝑁 (𝑠)
                                                                                                     𝑉 (𝑠, 𝑎)
         ties in these protocols that were previously unprovable by                PUCT(𝑠, 𝑎) =               + 𝑐·                · 𝑝 (𝑎 | 𝑠),
                                                                                                     𝑁 (𝑠, 𝑎)        1 + 𝑁 (𝑠, 𝑎)
         Tamarin’s default search strategies without human heuris-                                   | {z }      |            {z           }
         tics, and that it consistently finds shorter proofs than the                                value                      prior
         human heuristics.
                                                                            where 𝑉 (𝑠, 𝑎) is the accumulated value of the child reached via
Our code for the Tamarin API1 and the RL agent2 is open-source              action 𝑎 in state 𝑠, 𝑁 (𝑠, 𝑎) the visit count of action 𝑎, 𝑁 (𝑠) =
and available on GitHub.                                                    Í
                                                                              𝑏 𝑁 (𝑠, 𝑏) the parent’s total visit count, and 𝑝 (𝑎 | 𝑠) the prior
   Outline. This paper is structured as follows: In Section 2 and           probability from the policy network. After each completed game,
Section 3, we provide background on machine learning and the                the MCTS visit counts are normalized into a search policy 𝝅, which
Tamarin prover. We describe our reusable API for Tamarin in Sec-            serves as the training target for the network’s prior p, while the
tion 4 and our reinforcement learning agent that guides Tamarin’s           game outcome serves as the target for the value 𝑣. The network
proof search in Section 5. In Section 6, we present our case studies        is trained to match p → 𝝅 via cross-entropy and 𝑣 to the game
and experimental results. We present related work in Section 7, and         outcome via mean squared error, creating a positive feedback loop
we conclude in Section 8.                                                   between search quality and network accuracy.
                                                                               Transformers. The Transformer [38] is the dominant neural
2    Background on Machine Learning                                         network architecture in modern deep learning. Its core mechanism
Our approach uses reinforcement learning to train a neural net-             is attention: Given a sequence of input elements, each element com-
work that guides a tree search over Tamarin’s proof space. This             putes a learned compatibility score with every other element and
section gives the necessary background on these three components:           aggregates their representations weighted by these scores. This
Reinforcement learning provides the training framework, Monte               allows each element’s representation to be informed by all other
Carlo Tree Search (MCTS) is the search algorithm that explores              elements, with the network learning which relationships are rele-
possible proof steps, and a Transformer network learns which proof          vant. Multi-head attention applies multiple independent attention
steps are promising.                                                        operations in parallel, each capturing different aspects of the input.
                                                                               A Transformer encoder stacks multiple layers of multi-head at-
  Reinforcement Learning. In reinforcement learning [36], an
                                                                            tention and feed-forward networks. The input is first split into
agent interacts with an environment in discrete steps: At each step,
                                                                            tokens and mapped to fixed-size vectors via a learned embedding
1 https://github.com/niklasmedinger/Tamarin-ML-API                          layer. Since attention is permutation-invariant, positional encod-
2 https://github.com/MatCos/TamRL                                           ings are added to provide order information. After processing, the
                                                                        2
Less Effort, Shorter Proofs: Reinforcement Learning
for Security Protocol Analysis in Tamarin


per-token representations can be aggregated to produce fixed-size             encrypted session key k to it:
representations for variable-length inputs, which then serve as the                         [ Fr(k), !Pk($S, pkS) ]
basis for downstream predictions such as the prior distribution and
                                                                                            −[ SessionKey($S, k) ]→
value estimate.
                                                                                            [ Client_1($S, k), Out(aenc(k, pkS)) ]
3    Background on Tamarin                                                    The fact Fr, called fresh, is provided by a built-in rule that models
                                                                              generating a unique, random value k for each execution of the rule.
The Tamarin prover [29] is a state-of-the-art model checker for
                                                                              This fact is commonly used to generate nonces and cryptographic
symbolic security protocol verification. It takes as input a protocol
                                                                              keys in Tamarin models. The fact !Pk is a user-defined fact that is
model, a symbolic model of cryptography, and the desired security
                                                                              used to store the public key of a server and its public identity $S.
properties of the protocol. It then tries to find a proof or counterex-
                                                                              The ! in front of the fact indicates that it is a persistent fact, which,
ample of the properties in the presence of a Dolev-Yao adversary [16]
                                                                              unlike linear facts, is not consumed when the rule is executed. The
that can intercept, modify, construct, and inject messages.
                                                                              Client_1 fact is also user-defined and stores the server’s identity
   Tamarin performs unbounded verification, i.e., there are no bounds
                                                                              as well as the session key for the next step of the client’s protocol
on the number of protocol sessions, the number of messages, the
                                                                              execution. Finally, the Out fact is a built-in fact that models sending
number of agents running the protocol, and, thus, the size of a
                                                                              a message to the adversary-controlled network.
counterexample. As a result, the problem of verifying whether a
property holds is undecidable [18, 37], and Tamarin may fail to                  Semantics & Protocol Properties. The multiset rewriting
terminate — not finding a proof nor a counterexample. In this case,           rules of a Tamarin model induce a labeled transition system, whose
Tamarin’s users can use its graphical user interface (GUI) to man-            state is a multiset of facts and whose transitions are labeled with
ually investigate the failing proof attempt to find out where and             the action facts of the rules. The initial state of the system is the
why Tamarin fails to finish the proof. If they identify a reason for          empty multiset. A rule can be executed if its premises are contained
the failure, they can assist Tamarin by providing a heuristic that            in the current state, and executing it leads to a new state where
selects better proof steps to use during proof search, or by specify-         the linear premises are removed and the conclusions are added. A
ing intermediate lemmas, which need to be independently proven,               sequence of rule executions starting from the initial state is called
acting as invariants and reducing the search space.                           an execution, and the sequence of action facts of the rules in an
                                                                              execution is called the execution’s trace.
   Protocol Specification. Tamarin works in the symbolic model                   Tamarin allows the user to specify the protocol’s desired prop-
of cryptography, where protocol messages are represented as terms,            erties as trace properties in a fragment of first-order logic over the
cryptographic primitives are represented as function symbols, and             traces Tr of a Tamarin model. Trace properties are inductively built
an equational theory 𝐸 defines their semantics.                               from atomic formulas using the usual logical operators as well as
   For instance, the equation adec(aenc(m, pk(sk)), sk) = 𝑚 models            universal and existential quantification over terms and timepoints
the semantics of asymmetric encryption: Decrypting a message                  in the trace. The atomic formulas are ⊤ and ⊥, which, respectively,
𝑚 encrypted with the public key 𝑝𝑘 (𝑠𝑘) using the secret key 𝑠𝑘               always and never hold, action formulas 𝑓 @#i, which hold if the
yields the original message 𝑚. Tamarin comes with built-in support            action fact 𝑓 occurs at timepoint #i in the trace, equality of time-
for many common cryptographic primitives, but it also allows its              points #i = #j, which holds if the timepoints #i and #j are the same,
users to specify their own function symbols and equations, letting            and equality of terms 𝑠 =𝐸 𝑡, which holds if the terms 𝑠 and 𝑡 are
them model a wide range of cryptographic primitives. We refrain               equal modulo the equational theory 𝐸.
from giving a complete introduction to Tamarin’s term algebra and                Tamarin allows for both existential and universal trace proper-
instead refer the reader to [3] for more details.                             ties, i.e., properties that only need to hold for a single trace of the
   To specify the protocol’s semantics, Tamarin uses multiset rewrit-         system or for all traces of the system, respectively. Existential trace
ing rules of the form                                                         properties are usually used by users to test their protocol model by
                                                                              checking that there exists an execution that achieves the protocol’s
                [Premises] −[Actions]→ [Conclusions].                         goal, e.g., setting up a shared session key between two parties. Uni-
                                                                              versal trace properties are used to specify the security properties a
The premises and conclusions of a rule are multisets of facts, which          protocol should achieve, e.g., that the session key cannot be learned
are special or user-defined symbols applied to terms. These facts             by the adversary.
are used by the user to model the different protocol participants                Example 3.2. The following universal trace property is a standard
and their internal state, and by Tamarin, for instance, to model the          formulation of a secrecy property. If a session key k is established
adversary’s knowledge. The premises of a rule specify the facts that          between a server S and a client, formalized by the SessionKey(S, k)
are necessary to execute the rule, while the conclusions specify the          action fact, and the adversary learns k, formalized by the built-in
facts that are produced by this rule. The actions of a rule are used          K(k) action fact, then this leads to a contradiction ⊥:
to label the rule with action facts that can then be used to specify
properties of the protocol’s executions via lemmas.
                                                                                               ∀ 𝑡 ∈ Tr. ∀ S k #i #j.
  Example 3.1. The following rule models the lookup of the public                              SessionKey(S, k) @ #i ∧ K(k) @ #j
key pkS of a server S by a client, which then sends an asymmetrically                          ⇒ ⊥
                                                                          3
                                                                                                                Cosler, Cremers, Finkbeiner, Ghanem, Medinger


4     A Reusable API for Proof Search in Tamarin                                 existential trace property 𝜙
In this section, we describe our first contribution: a reusable API                             ∃ 𝑡 ∈ Tr. ∃ S k #i #j.
for the Tamarin prover that allows users to programmatically in-
                                                                                                SessionKey(S, k) @ #i ∧ K(k) @ #j.
teract with its proof search. While we use this API to implement
a reinforcement learning agent in Section 5, we want to highlight                Then it will simplify the initial constraint system Γ 0 = {𝜙 } by
that it can be used for any proof search algorithm and thus facili-              applying constraint solving rules that instantiate the existentially
tates future research on custom proof search strategies for Tamarin,             quantified variables and split the conjunction, resulting in the fol-
including but not limited to machine learning-based ones.                        lowing constraint system that contains two action formulas:
   We first give an overview of Tamarin’s current proof search and
how users guide it via heuristics, and we then describe our API and                          Γ = { SessionKey(S, k) @ #i, K(k) @ #j }.
how it facilitates a new way of interacting with Tamarin via an                  This constraint system exactly captures all traces where the adver-
external client that stores the state of the proof search and only               sary learns the session key k established with a server S.
queries Tamarin to execute proof steps and validate the final proof.
                                                                                     To search for a solved constraint system, Tamarin has to make
                                                                                 two decisions: First, it has to decide which constraint solving rule
4.1    Tamarin’s Proof Search and Heuristics                                     to apply to the current constraint system. Second, it has to decide
To prove a property 𝜓 , Tamarin proceeds as follows: If 𝜓 is an                  how to explore the resulting tree of child constraint systems. To
existential trace property, Tamarin directly searches for a trace that           solve the first problem, Tamarin uses heuristics, which rank the
satisfies 𝜓 , proving the property if it finds one. If 𝜓 is a universal          rules ⇝0, . . . , ⇝𝑛 applicable to a constraint system Γ. Tamarin
trace property, Tamarin uses the duality of existential and universal            features many inbuilt heuristics that are suited for a large class of
quantifiers: It proves 𝜓 for all traces by showing that there is no              protocols and achieve automatic proofs on them, but users can also
trace satisfying ¬𝜓 . To show this, Tamarin exhaustively searches                provide their own heuristics via different means, as we will see
for a trace that satisfies ¬𝜓 with the intention of not finding one.             shortly.
    This approach allows Tamarin to prove both existential and uni-                  The second problem is more intricate than it first seems: The
versal trace properties by searching for traces that satisfy them                search space might be infinite in depth, as there is no bound on the
or their negation respectively. During this search, Tamarin sym-                 size of the counterexample that Tamarin might find. Thus, the tree
bolically represents the candidate traces by constraint systems. A               search must not get lost in infinite depth branches since this could
constraint system Γ is a set of constraints, which assert, for instance,         cause it to miss a solved constraint system in a different branch.
that a multiset rewriting rule is executed at some timepoint in the              To solve this problem, Tamarin uses iterative deepening depth first
trace, that a logical formula holds, or that the conclusion of a rule            search (IDDFS) by default, but it also supports breadth first search
execution is consumed by the premises of another.                                (BFS). Both search strategies will explore the complete search space
    To search for a trace, Tamarin starts with an initial constraint             up to a certain depth, and only then increase their depth bound,
system Γ 0 = {𝜓 }, which exactly captures the set of traces satisfying           ensuring that no solution is missed.
𝜓 . Then, it recursively applies constraint solving rules (also called               Both of these search strategies are greedy, i.e., they always use
proof methods) of the form Γ ⇝ Γ0 × . . . × Γ𝑛 , which, when applied             the highest ranked constraint solving rule according to a heuristic.
to a constraint system Γ𝑖 , produce new child constraint systems                 This greedy search comes with upsides and downsides: On the one
Γ0𝑖+1 × . . . × Γ𝑛𝑖+1 . Since Tamarin’s constraint solving rules are sound       hand, it can lead to fast proofs if the heuristic is informative. On
                                                                                 the other hand, it will lead to much longer proof times and proof
and complete, the set of traces captured by Γ𝑖 is exactly the union
                                                                                 sizes or even failure if the heuristic is bad.
of the sets of traces captured by Γ0𝑖+1 × . . . × Γ𝑛𝑖+1 . When a rule
                                                                                     Should Tamarin fail to find a proof, users have to manually
application produces more than one child constraint system (𝑛 > 1),
                                                                                 investigate where in the search Tamarin fails and why this is the
it is called a case split. By applying these constraint solving rules
                                                                                 case: Is Tamarin failing to prove a property which actually holds?
recursively, Tamarin creates a tree, refining the initial constraint
                                                                                 Is it failing to find a counterexample? Is a found counterexample
system Γ 0 into more and more concrete child constraint systems.
                                                                                 a true positive, i.e., the property does not hold, or is it due to a
    This continues until Tamarin finds a proof, or proof tree, which
                                                                                 bug in the protocol model or property formulation that needs to
contains a branch with a solved constraint system or only branches
                                                                                 be addressed? To answer these questions, users most commonly
that end in a contradictory constraint system. In the former case,
                                                                                 use Tamarin’s GUI to manually explore the search tree, inspecting
the proof shows that a trace satisfying the initial constraint system
                                                                                 constraint systems and applying constraint solving rules to them.
exists, while in the latter case, the proof shows the absence of such
                                                                                 When inspecting a constraint system, users try to identify whether
a trace. If the property is universal, a solution corresponds to a
                                                                                 the traces represented by this system are ultimately contradictory,
counterexample, and the absence of solutions corresponds to a
                                                                                 i.e., whether the system should lead to contradictory child systems,
proof. If the property is existential, a solution is a proof (witness),
                                                                                 or whether these traces are valid executions of the protocol, i.e.,
and the absence of solutions is a proof that the property does not
                                                                                 whether the system should lead to a solved child system. This
hold.
                                                                                 process takes expert insight into the protocol, as the user needs
                                                                                 to correctly judge the constraint system’s traces, and Tamarin’s
  Example 4.1. When proving the universal property from the                      internals, as the user needs to understand why Tamarin fails to
previous example, Tamarin will first negate it, resulting in the                 automatically prove these systems.
                                                                             4
Less Effort, Shorter Proofs: Reinforcement Learning
for Security Protocol Analysis in Tamarin


     1   tactic : secret_k_gnb                                                  4.2    A Reusable API for the Tamarin Prover
     2   presort : C
     3   prio :
                                                                                In [14], the authors report the proof of the protocol’s properties
     4        regex ".* Secret .*"                                              “require[d] dedicated and involved proof strategies (∼1000 LoC
     5   prio :                                                                 of Python)” and that “[t]he effort of writing such generic proof
     6        regex ".* X # k .*"                                               strategies represents several person-months.” Other Tamarin case
     7        regex ".*# j \. \( Create .*"
                                                                                studies do not specifically report on the time taken for writing
     8        // ...
     9   prio :                                                                 heuristics, but they do report on the overall time taken for the
    10        regex ".* KeyDerived \( .*"                                       proof effort. For instance, the authors of the WPA2 case study [12]
    11        regex ".*! KU \( KDF \(~ K_SEAF .*"                               report 12 person-months of work, [7] reports 6-7 person-months of
    12            & not regex ".*! KU \( .*~ K_SEAF \..*"                       work, and [8] reports 3-4 person-months of work building on the
    13        // ...
    14   deprio :
                                                                                models of [7]. From corresponding with the authors, we know that
    15        regex ".*! KU \( .*~ K_SEAF \..*"                                 a significant portion of the reported time was spent on manually
    16        regex ".* Intermediate .* < ' NH \ ' , NH .*"                     searching for candidate heuristics, making it clear that this is a
                                                                                significant bottleneck for Tamarin verification.
Figure 1: Example Tamarin tactic from the 5G Handover Xn                            The cause of this bottleneck is the lack of search over the applica-
model [30]. Constraint solving rules that match a ranking                       ble constraint solving rules: If Tamarin’s greedy search fails to find
function with higher priority are ranked higher. Rules within                   a proof with the inbuilt heuristics, users have to manually search
the same priority are ranked according to the inbuilt ‘C’                       over the applicable rules to identify promising proof strategies.
heuristic, indicated by presort.                                                    While we could implement a custom proof search over the appli-
                                                                                cable rules by directly modifying Tamarin’s source code, we have
                                                                                higher aspirations: We want to empower Tamarin’s users to imple-
                                                                                ment their own proof search algorithms, rather than being limited
                                                                                to the one we provide.
                                                                                    To this end, we implement a reusable API for Tamarin that allows
    Once the user identifies where and why Tamarin fails to finish a            users to interact with Tamarin’s proof search without modifying
proof, they can try to work towards a successful proof by 1) chang-             its source code, significantly lowering the entry barrier for imple-
ing the model in a way that makes it easier for Tamarin to verify its           menting new proof search algorithms. Our API turns Tamarin into
properties, while keeping the same scope of verification, 2) identify-          a stateless REST server that exposes endpoints for querying the
ing a useful intermediate lemma that can be proven independently                initial constraint system and its applicable rules, for executing proof
and reduces the search space, or 3) discovering a proof strategy,               methods, and for validating the final proof. This way, users can
i.e., a sequence of constraint solving rule applications, that can be           implement their own proof search algorithms by simply implement-
turned into a heuristic for an automatic proof.                                 ing a client that queries Tamarin’s REST API, without having to
    Specifying a heuristic can be done in numerous ways, ranging                interact with the internals of Tamarin or modifying its source code.
from fact-specific annotations in the model that (de)prioritize apply-              As a side effect, this also allows users to implement their proof
ing constraint solving rules to these facts to providing a so-called            search algorithms in any programming language they want instead
oracle, which is an executable script, often written in Python, called          of being constrained to Haskell by Tamarin, and to implement
by Tamarin whenever the constraint solving rules need to be ranked.             heuristics that are more complex than what Tamarin’s tactics allow,
However, tactics [32] have recently become the standard way to                  for instance, by inspecting the current constraint system or the
provide heuristics to Tamarin. Tactics are a small domain-specific              history of applied rules in addition to the applicable rules.
language built into Tamarin that allows users to specify a heuristic                Our API consists of three main endpoints: 1) getInitialSystem,
by ranking constraint solving rules based on which ranking func-                which returns the initial constraint system of the proof search
tion they match. See Figure 1 for an example tactic from the 5G                 and its applicable rules, 2) executeMethod, which takes as input a
Handover XN model from [30]. A tactic has a name and multiple                   constraint system and a constraint solving rule to apply to it, checks
prio or deprio segments, each containing functions that match the               whether the rule is applicable, and then returns the resulting child
applicable constraint solving rules. Rules are then ranked based on             constraint systems and their applicable rules, and 3) checkProof ,
which segment they match, and, should multiple rules match the                  which takes as input a proof, checks whether it is a valid proof of
same segment, based on an optional, inbuilt presort heuristic that              the desired property, and returns a Tamarin spthy file containing
ranks rules within the same segment.                                            the proof as well as metadata about the proof such as the size.
    Most commonly, the ranking functions of tactics are regexes that                Our API can now be used to implement a proof search as follows:
match on the pretty-printed string representation of the constraint             The client starts by querying the getInitialSystem endpoint to get
solving rules, as this gives users most control. One limitation of              the initial constraint system of a proof and its applicable rules. It
tactics is that they are stateless and only have access to the applicable       then selects a rule to apply, for instance, by using a heuristic or by
constraint solving rules of a constraint system and not the system              searching over the applicable rules, and queries the executeMethod
itself, which could be useful for guiding the proof search. As a result,        endpoint to apply this rule and get the resulting child constraint
tactics cannot specify that a rule should be ranked higher if the               systems and their applicable rules. This process is repeated until a
constraint system contains a specific fact or if it has already been
applied multiple times.
                                                                            5
                                                                                                               Cosler, Cremers, Finkbeiner, Ghanem, Medinger


                                                                                 API from Section 4 and collect training examples from successful
                                                                                 subproofs. These examples then update the neural network, which
          Tamarin Server                                 External Client
                                                                                 in turn guides the current and subsequent searches more effectively.
                              getInitialSystem()

                               Γ 0, ⇝00, . . . , ⇝𝑛0                             5.1    Proof Search as Graph Exploration
                                                                                 We adapt MCTS to Tamarin’s proof search by modeling the search
           loop                                                                  space as a graph with two types of nodes: OR nodes represent con-
                           executeMethod (Γ𝑖 , ⇝𝑖𝑘 )
                                                                                 straint systems where the agent must choose which proof method
                  (Γ0𝑖+1, ⇝𝑖+1
                           0 , . . . , ⇝𝑛 ), . . . , (Γ𝑛 , . . .)
                                        𝑖+1            𝑖+1                       to apply next. Any single choice that leads to a proof suffices. AND
                                                                                 nodes arise from case splits when the application of a proof method
                                                                                 produces multiple child constraint systems. Their semantics change
                                                                                 depending on whether there exists a solution to the constraint
                                                  𝑇 ← Construct Proof Tree
                                                                                 system or not: If there is a solution, for instance because a coun-
                                checkProof (𝑇 )                                  terexample to a universal property is found, then the case split
                                                                                 acts as a disjunction, as it suffices to find a solution in any of the
                                     ✓ or X                                      branches. If there is no solution because the constraint system is
                                                                                 ultimately contradictory, then the case split acts as a conjunction,
                                                                                 as all branches must be proven contradictory to show the absence
                                                                                 of a solution. Because it is not known a priori whether a property
                                                                                 has a solution or not, we conservatively treat all case splits as AND
Figure 2: Message sequence chart of an external client in-
                                                                                 nodes. Once a (sub-)proof is found, the search can identify which
teracting with our Tamarin API during proof search. The
                                                                                 branches of the AND nodes are relevant and update their status
client first queries Tamarin for the initial constraint system
                                                                                 accordingly. Figure 3 gives an overview of the search procedure for
Γ 0 and its constraint solving rules. Then it repeatedly queries
                                                                                 a single lemma and Figure 4 illustrates the resulting search graph.
Tamarin to execute a rule ⇝𝑖𝑘 , obtaining the child constraint
                                                                                    The following paragraphs detail each phase.
systems Γ0𝑖+1, . . . , Γ𝑛𝑖+1 and their rules. Internally, the client
constructs a search tree until a counterexample is found or                        Selection. We traverse the graph from the root. At each OR
its absence is confirmed. Finally, the client constructs a proof                 node we select the child that maximizes a PUCT-style score:
tree and queries Tamarin to check whether it is correct.                                   PUCTOR (𝑠, 𝑎) = 𝛾 −1−𝑉 (𝑠,𝑎) + 𝑐 (𝑠) · 𝑝 (𝑎 | 𝑠),
                                                                                                           | {z }         |      {z      }
                                                                                                               value score        prior score
solved constraint system is found or the absence of a counterexam-
                                                                                 where 𝑉 (𝑠, 𝑎) is the aggregated value of the child node reached by
ple is confirmed, at which point the client can construct a proof tree
                                                                                 taking action 𝑎 in state 𝑠, 𝛾 ∈ (0, 1] is a value discount that controls
and query the checkProof endpoint to check whether it is a valid
                                                                                 sensitivity to value differences, 𝑝 (𝑎 | 𝑠) is the prior probability
proof. Figure 2 visualizes this interaction between the client and
                                                                                 assigned by the neural network to action 𝑎 in state 𝑠, and
Tamarin. Notably, the search tree of the proof search is now stored
                                                                                                                                         √︁Í
by the client instead of Tamarin, allowing the client to implement                                                                            𝑏 𝑁 (𝑠, 𝑏)
                                                                                               Í                            
                                                                                                      𝑏 𝑁 (𝑠, 𝑏) + 𝑐 base + 1
any proof search algorithm.                                                          𝑐 (𝑠) = log                                + 𝑐 init ·
                                                                                                              𝑐 base                       𝑁 (𝑠, 𝑎) + 1

5   Reinforcement Learning for Tamarin                                           is the exploration coefficient, with 𝑁 (𝑠, 𝑎) the number of times
                                                                                                                                  Í
                                                                                 action 𝑎 has been selected from state 𝑠 and 𝑏 𝑁 (𝑠, 𝑏) the total
Tamarin’s built-in proof search greedily selects the top-ranked ap-              number of actions taken from 𝑠, summed over all available actions 𝑏.
plicable proof method at each step. This approach is efficient when              For unvisited actions, the value is estimated pessimistically as 𝑉 (𝑠)−
the heuristic is informative, but it often leads to suboptimal and               𝛿, where 𝛿 is a configurable penalty. Following AlphaProof [20], we
non-terminating search when the heuristic is imperfect. In contrast,             replace the linear value term of the AlphaZero PUCT formula with
our approach formulates proof search as a full graph exploration                 an exponential discount to handle the unbounded returns in proof
problem where not only AND nodes (case splits) but also OR nodes                 search and maintain a consistent scale between the value and prior
(choosing which constraint to solve) are part of the search space.               terms. The discount 𝛾 additionally controls sensitivity: 𝛾 close to
The selection of which proof method to apply is guided by a learned              1 compresses differences (prior-dominated), while smaller values
policy and value function, optimized via Monte Carlo Tree Search                 amplify them (value-dominated).
(MCTS), building on the AlphaZero paradigm of combining neural                      At AND nodes, following AlphaProof [20], priors are uniform,
network guidance with tree search [34], recently applied to for-                 and the exploration coefficient is scaled by 𝑐 and to control explo-
mal mathematics by AlphaProof [20]. The reinforcement learning                   ration at AND nodes separately from OR nodes:
framework maps naturally onto Tamarin’s proof search: States cor-
                                                                                                                                              1
respond to constraint systems, actions correspond to the applicable                      PUCTAND (𝑠, 𝑎) = 𝛾 −1−𝑉 (𝑠,𝑎) + 𝑐 and · 𝑐 (𝑠) ·
proof methods at a given proof state, and rewards encode proof                                                                              |𝐴(𝑠)|
progress signals. Our system benefits from a self-improving loop:                Contrary to AlphaProof, we do not invert the value score at AND
Parallel workers run MCTS searches on different lemmas using the                 nodes for two reasons: First, AlphaProof’s prioritization of the
                                                                             6
Less Effort, Shorter Proofs: Reinforcement Learning
for Security Protocol Analysis in Tamarin


1    // Input: 𝑓𝜃 , budget B, top-N expansion, root
                                                                                                                          V=−3.8
2    // Output: proof tree or EXHAUSTED                                                          Client_1(S, k)▶0#i                 !KU(h(k))@#vk
                                                                                                       p=0.65                            p=0.35
3    for step = 1 to B do
4      // Selection: traverse to unexpanded node
5      node ← root; path ← [root]                                                             V=−2.7                                              V=−3.4
6      while node is expanded do                                            !KU(~k)@#vk.1                  !KU(h(~k))@#vk           case Serv_1            case c_h
                                                                               p=0.42                          p=0.58
7        node, m ← argmax PUCT(node, m) over all methods m at node
8        append node to path
                                                                                 V=−3.5                      V=−2.3                  V=−2.4                   V=−1.7
9      // Expansion & Evaluation: evaluate and expand node
                                                                                                case c_h              case Serv_1
10     p, v(node) ← 𝑓𝜃 (node) // prior, value
11     sort applicable methods by p descending                                                                                      Client_1(S, k)▶0#i
                                                                                                                                          p=0.69
12     for each top N applicable method m at node do
                                                                                              V=−1.3                      V=−1.0
13       environment_step(node, m)
14     // Backup: propagate values along path                                   !KU(~k)@#vk.1          !KU(~ltk)@#vk.3

                                                                                                                            ...
15     for each node 𝑛 ′ in path (leaf to root) do                                      p=1                     p=0.74                   OR node (proof method)
16       if 𝑛 ′ is OR then
                                                                                                                                         AND node (case split)
17         V(n') ← visit-weighted mean of v(n') and children values                           V=−0.4
                                                                                                                                     ✓   Contradiction or Solved (resolved)
18       else
19         V(n') ← min over children c: V(c)                                                                                             Selection path

20     // Extract: collect from highest resolved subtree                                                                    ✓            Merged (graph search)

21     if resolved node 𝑛 ′ found on path then
22       walk proof subtree (OR: proven child, AND: all children)
23       collect (state, method, recomputed 𝑣𝑡 ) per OR node               Figure 4: AND/OR search graph for the Tutorial protocol
24     if root is resolved then                                            model, lemma Client Session Key Secrecy after several MCTS
25       tree ← extract proof tree from root                               iterations. OR nodes (circles) represent constraint systems
26       TamarinAPI.checkProof(tree)                                       where the agent selects a proof method; AND nodes (dia-
27       return tree
28   return EXHAUSTED
                                                                           monds) arise from case splits requiring all children to be
29                                                                         resolved. Edges carry the proof method and neural network
30   environment_step(node, m):                                            prior 𝑝. Node values 𝑉 reflect backed-up estimates. The thick
31     C ← TamarinAPI.executeMethod(node, m)                               path shows PUCT selection; the dotted edge illustrates graph-
32     if |C| = 0 then        // contradiction
                                                                           search deduplication.
33       create terminal child: prior 𝑝 (𝑚 | node ) , value 0
34     else if |C| = 1 then   // single successor
35       if C is solved or contradictory then
36         create terminal child: prior 𝑝 (𝑚 | node ) , value 0            all child constraint systems as OR nodes. A proof method that pro-
37       else                                                              duces zero children is contradictory by design, and a single child
38         create OR child from C: prior 𝑝 (𝑚 | node )                     system may be either a terminal state (solved or contradictory)
39     else                   // case split                                or an OR node. Terminal nodes receive a value of 1.0 instead of
40       create AND node with prior 𝑝 (𝑚 | node )
41       add OR children forall 𝑐 ∈ 𝐶 , uniform prior
                                                                           a neural estimate. Proof methods that exceed a per-call timeout
                                                                           are retried with a longer timeout, and, if they still fail, they are
                                                                           excluded from the search.
Figure 3: Main MCTS loop. The four phases (Selection, Ex-
pansion, Backup, and Extraction) are explained in detail in                   Backup. After expansion, values and status flags (contradictory,
Section 5.1.                                                               solved) are propagated back along the traversed path. OR nodes
                                                                           aggregate child values as a weighted running mean:
                                                                                               Í
                                                                                            𝑣 + 𝑎∈visited 𝑁 (𝑠, 𝑎) · (𝑅(𝑠, 𝑎) + 𝑉 (𝑠, 𝑎))
                                                                                   𝑉OR =                     Í                            ,
hardest sub-goal stalls finding subproofs from which we can learn                                        1 + 𝑎 𝑁 (𝑠, 𝑎)
(See Extraction). Second, it hurts existential lemmas, where case          where 𝑣 is the network’s initial value estimate for the node, 𝑁 (𝑠, 𝑎)
splits are disjunctions and it is more efficient to find any single        is the number of times action 𝑎 has been selected from state 𝑠, 𝑅(𝑠, 𝑎)
subproof first.                                                            is the edge reward (Section 5.4), and 𝑉 (𝑠, 𝑎) is the aggregated value
                                                                           of the child reached via action 𝑎. An OR node becomes contradictory
   Expansion & Evaluation. When selection reaches an unex-
                                                                           if any child is contradictory, and it becomes solved if any child is
panded OR node, we first query the neural network to obtain a
                                                                           solved.
prior distribution p and a value estimate 𝑣 for the state. We then
                                                                               AND nodes take the minimum value over visited, non-contradictory
apply the top N applicable proof methods to Tamarin, obtaining
                                                                           children, reflecting that the overall difficulty is determined by the
the child constraint systems for each method. This is different from
                                                                           hardest remaining sub-case. Unvisited children are treated opti-
both AlphaZero, which expands only a single child per node, and
                                                                           mistically (assigned the maximum value 1), so the AND node’s
AlphaProof, which expands all children. We decided on this middle
                                                                           value reflects only the known hardest subgoal. An AND node be-
ground to eagerly detect contradictions and solved states and to
                                                                           comes contradictory only when all its children are contradictory,
generate training data while keeping the compute overhead man-
                                                                           but it becomes solved if any child is solved.
ageable with parallelization. Each proof method application yields
a set of children. More than one child indicates a case split, which         Extraction. We extract training examples from the search when-
we handle by creating an AND node with uniform prior and adding            ever a node becomes resolved (contradictory or solved), rather than
                                                                       7
                                                                                                           Cosler, Cremers, Finkbeiner, Ghanem, Medinger


waiting until the search terminates. Extracting partial subproofs               Value Head. The value head is a separate projection layer
mid-search, rather than waiting for a complete proof, provides train-        𝑉 : S × A → R, where S and A are the state space and ac-
ing signal early and allows the network to improve while the search          tion space, respectively. The 𝑉 layer is equipped with the same
is still running. To avoid contamination of the training data with the       pointer-network architecture as the policy head to produce per-
network’s own value estimates, we recompute the objective value              method scores. The scores are then mean-pooled across all methods
targets 𝑣𝑡 (𝑠) for all OR nodes by backing up values analogously to          in the state to obtain a single scalar value estimate.
the backup phase, but without averaging with the network’s own                  Both heads share the same Transformer encoder, forming an
value estimates. Training examples are tuples (𝑠, 𝑎, 𝑣𝑡 ), where 𝑠 is        actor-critic architecture on shared representations.
the proof state, 𝑎 is the index of the selected action, and 𝑣𝑡 is the
value target.                                                                5.3    Integrating Heuristic Knowledge
    When the root node is finally resolved, the extracted proof tree         To leverage existing domain knowledge, we combine the learned
is validated independently by sending it to Tamarin’s checkProof             prior with a rank-based bias derived from Tamarin’s heuristic or-
endpoint via the API, and the search is finished.                            dering. We exploit this ordering by adding a rank-dependent bias
   Graph Search. Contrary to the standard MCTS formulation and               to the network’s logits before normalization:
AlphaZero [34], we perform a Monte Carlo graph search [13, 43],
                                                                                                                            
                                                                                                                     ℓ −𝜆 ·𝑟
since the same constraint system can be reached via different proof                           pcombined = softmax              ,
                                                                                                                        𝑇
paths; for instance, through different interleavings of the same
                                                                             where ℓ are the raw model logits, 𝑟 = (0, 1, 2, . . .) are the rank
proof methods. While this turns the search tree into a directed
                                                                             positions from the heuristic ordering, 𝜆 controls the heuristic’s
acyclic graph (DAG), graph search does not fundamentally change
                                                                             influence, and 𝑇 is a temperature parameter that flattens the com-
the MCTS algorithm. Its main advantage is efficiency: By merging
                                                                             bined distribution, making it more uniform. Setting 𝜆 = 0 yields a
duplicate states, we significantly reduce the search space by avoid-
                                                                             purely learned prior; increasing 𝜆 interpolates toward the heuristic
ing redundant exploration. We find in our experiments that usually
                                                                             ordering. If the inbuilt heuristic is informative, this bias can help
around 2 − 5% of the nodes in the search are shared, with some
                                                                             the search converge faster by guiding it toward promising proof
protocols up to 25%.
                                                                             methods early on. Vice versa, if the heuristic is misleading, the
                                                                             heuristic can either be switched off manually or the learned prior
5.2    Neural Network Architecture
                                                                             can override it. A human-engineered heuristic can be integrated
The Reinforcement Learning agent relies on a neural network to               in the same way, allowing the framework to benefit from human
guide its search by providing a policy and a value estimate for each         insights along the process.
proof state, taking an observation of the state as input.
   State Encoding. We experimented with different full-state en-             5.4    Reward Shaping
codings, including a Graph Neural Network, but we quickly en-                Each edge in the search graph carries a reward that the agent
countered scalability issues due to the size of the constraint system.       seeks to maximize. Following AlphaProof’s approach of penalizing
As a consequence, we instead abstract from the full state, using the         each proof step, we use a base cost of −1 per step. By encouraging
set of applicable proof methods as the observations. This aligns             shorter proofs, we implicitly encourage termination in general, as
with how Tamarin’s heuristics work.                                          diverging paths or loops accumulate large negative rewards. We
   The observable proof state is encoded by a Transformer-based              augment this base cost with three domain-specific penalty terms,
neural network. Each proof method is represented as a sequence               each normalized to a comparable range, yielding the overall reward:
of its method type and arguments, similar to its representation
                                                                                            𝑅(𝑠, 𝑎) = −(1 + 𝛽 · 𝑏 + 𝛼 · 𝑡 + 𝜏 · ℎ),
in the Web interface, and tokenized using a standard subword
tokenizer [28]. Token sequences are embedded via a learned em-               where 𝑏, 𝑡, and ℎ are the branching, soft-time, and hard-timeout
bedding layer into 𝑑-dimensional vectors 𝒙 𝑡 ∈ R𝑑 , augmented                penalties defined below, and 𝛽, 𝛼, 𝜏 control their respective influ-
with sinusoidal positional encodings, then processed by a standard           ence. Terminal edges (contradictions, solved states) and edges to
Transformer encoder. The resulting token-level representations are           AND nodes carry only the base cost of −1.
mean-pooled over each proof method’s tokens, yielding a single
                                                                                Branching Penalty. The branching penalty 𝑏 penalizes transi-
vector 𝒆𝑖 ∈ R𝑑 per proof method.
                                                                             tions that increase the number of applicable proof methods relative
    Policy Head. For a state 𝑠 consisting of 𝐿 proof methods, the            to the worst-case branching factor on the current path, steering the
policy head scores each of them against the full set, using a pointer        search toward states with fewer applicable methods, which tend to
attention mechanism [39]: Each method’s encoding is projected                be closer to a terminal state.
into a key 𝒌 𝑖 ∈ R𝑑 . A shared query 𝒒 ∈ R𝑑 summarizing the
                                                                                Soft-Time Penalty. The soft-time penalty captures the wall-
entire state is obtained by summing all method encodings (after
                                                                             clock time Δ𝑡 Tamarin takes to expand a node, clipped and nor-
a nonlinear transformation) and applying a linear projection on
                                                                             malized: 𝑠 = min(Δ𝑡, 𝑡 clip )/𝑡 clip . This guides the search away from
the result. The unnormalized score (i.e., logit) for method 𝑖 is ℓ𝑖 =
                                                                             proof methods that are computationally expensive to execute.
𝒘 ⊤ tanh(𝒌 𝑖 + 𝒒) ∈ R, with 𝒘 ∈ R𝑑 . We then apply a log-softmax on
{ℓ𝑖 }𝑖=0
     𝐿−1 to normalize the logits into a prior probability distribution
                                                                                Hard-Timeout Penalty. If a proof method exceeds the per-
𝑝 (· | 𝑠) ∈ R𝐿 over proof methods.                                           call timeout, we retry with a longer sequential timeout to avoid
                                                                         8
Less Effort, Shorter Proofs: Reinforcement Learning
for Security Protocol Analysis in Tamarin


                Worker 1                                                                    Multi-worker Parallelism. Multiple worker processes run
                  Expand
                                                                                         MCTS searches in parallel, while neural network inference and
      Tamarin               MCTS                Collect
       Server
                  Check
                  Proof     Search           (sub-)proofs
                                                                                         gradient updates are centralized in the trainer process on a sin-
                                                              Replay Buffer
                                                                                         gle GPU. Workers send proof states to the trainer via pipes and
                                                                    Sample & Learn       receive policy and value predictions in return, always using the
                Worker n
                  Expand
                                              Inference
                                           prior and values
                                                                                         latest model weights without explicit synchronization. Collected
                                                                 Model
      Tamarin      Check
                             MCTS                                                        training examples flow back through a shared queue into the replay
       Server      Proof     Search                                                      buffer. This architecture allows us to scale the number of workers
                                                                                         independently of the GPU resources.

Figure 5: Training architecture overview. Multiple workers                                  Multi-lemma Training. Workers can operate on different lem-
run MCTS searches in parallel, each communicating with                                   mas or even different protocols while sharing a single neural net-
its own Tamarin server instance. Workers collect training                                work, enabling transfer of learned proof strategies across related
examples from subproofs and send them to a shared replay                                 properties. The trainer dynamically schedules workers across lem-
buffer. The model learns from buffer samples and provides                                mas, starting new searches as previous ones complete or exhaust
inference (prior and value estimates) back to the workers.                               their search budget. The scheduler selects lemmas in a round-robin
                                                                                         fashion until a number of searches or proofs are completed, so
                                                                                         easier lemmas are solved first and contribute more training exam-
                                                                                         ples early on, while harder lemmas receive more attention as the
permanently excluding reachable states. Methods that eventually                          training progresses and the network improves.
succeed under the extended timeout receive a fixed penalty ℎ, dis-
couraging paths that repeatedly trigger expensive Tamarin calls. If                      6   Case Studies and Experimental Results
the extended timeout also fails, the proof method is permanently
                                                                                         To demonstrate the efficacy of our approach, we picked 16 case stud-
excluded.
                                                                                         ies from Tamarin’s main repository and recent publications. These
                                                                                         case studies range from classical protocol models that Tamarin
5.5      Training                                                                        quickly solves by default, over models where some human guid-
Training follows an online self-play loop (Figure 5): Parallel work-                     ance was necessary to guide the proof search, to state-of-the-art
ers run independent MCTS searches, extract training examples                             models from recent publications, where person-months of effort
from successful subproofs (Section 5.1), and feed them into a shared                     went into finding heuristics [7, 8, 12, 14].
replay buffer. The trainer process continuously samples from this                           We find that our approach solves more lemmas automatically
buffer and updates the neural network, whose improved predic-                            than Tamarin’s default heuristics and that it produces shorter proofs
tions immediately guide ongoing and subsequent searches. Unlike                          than both the default heuristics and the original human-written
AlphaProof, which only learns from fully solved problems, our on-                        heuristics. Moreover, we show that our approach generalizes across
line loop generates training signal from partial subproofs, making                       different lemmas within the same protocol, using knowledge gained
training feasible without extensive pretraining.                                         from previous proof attempts to assist in proving future lemmas.
                                                                                            In the following, we first provide an overview of the case studies
   Replay Buffer. Training examples are stored in a FIFO buffer.                         we selected and then describe our experiments and findings.
We sample from the buffer with a probability inversely proportional
to the number of times an example has been drawn, to mitigate                               Case Studies. We group our case studies into three categories:
staleness and improve data efficiency. We sample from this buffer                        The first category consists of classical security protocol models
continuously under two conditions: (1) the least seen example has                        from Tamarin’s main repository [1], which are quickly solved by
been seen fewer than 𝑀 times, and (2) the buffer has been filled to                      Tamarin’s default heuristics and require no human guidance. The
a fraction 𝑓 of its capacity, to ensure a minimum level of diversity                     second category consists of more complex models, such as Wire-
in the training data. Both 𝑀 and 𝑓 are configurable parameters.                          Guard [17], the Signal model from [27], and 5G Handover EPS
                                                                                         N26 [30], for which some human effort was necessary to guide
   Losses. The training objective combines a cross-entropy loss                          the proof search. The third category consists of state-of-the-art
on the policy head (encouraging the network to predict the MCTS-                         models like 5G AKA [14], SPDM [7, 8], and WPA2 [11], where
selected action) with a mean squared error loss on the value head                        person-months of effort went into finding heuristics [7, 8, 12, 14].
(encouraging the network to predict the backed-up value target).
We use the Adam optimizer with gradients clipped at a global norm                           Experimental Setup. Our experiments are structured as fol-
of 1.0.                                                                                  lows: We first establish Tamarin’s baseline performance on our
                                                                                         case studies by removing all human annotations and heuristics
    Search Budget. Each MCTS search is allocated a budget of 𝐵                           that influence the search heuristics, but we keep helper lemmas
node expansions. If the proof is not found within the budget, the                        and the corresponding reuse and hide_lemmas annotations. While
search terminates and a new search begins with an increased budget                       identifying key helping lemmas is also an important aspect of the
𝐵 ′ = ⌊𝐵 · 𝜙⌋, where 𝜙 > 1 is a configurable growth factor. This                         proof effort, we consider it complementary to our work and only
allows the system to attempt quick proofs first and progressively                        focus on the proof search. We then run Tamarin on these models
invest more computation in harder lemmas.                                                using its default search strategy (IDDFS) with the default heuristic
                                                                                     9
                                                                                                                               Cosler, Cremers, Finkbeiner, Ghanem, Medinger


s and the heuristic c with a timeout of two hours, respectively four                             Table 1: Overview of how many lemmas our RL system (best
hours for especially large protocols (SPDM and WPA2). We also                                    single configuration), and Tamarin’s c and s heuristics, solve
chose to include the c heuristic in our baseline performance because                             in each case study. The Total column shows the number of
it ranks applicable proof methods based on how long they were ap-                                total lemmas in this category, with the original heuristics in
plicable to the constraint system and, as a result, never indefinitely                           parentheses when fewer than the total. See the paragraph
delays applying one, making it the best attempt at searching over                                Less Effort in Section 6 for a discussion of this table.
the applicable proof methods that Tamarin currently has.
    We also run Tamarin on the original, unaltered case studies in an                                 Protocol                    Type      Total      c     s    RL
attempt to reproduce the results reported in the respective papers
                                                                                                                          Classical Models
on our Tamarin version. These runs reflect the original performance
of Tamarin on these case studies, usually with significant human                                                                    ∀         2        2     2     2
                                                                                                      FOO Eligibility
engineering effort required to create effective heuristics. For the                                                                 ∃         1        1     1     1
classical models, the original performance is often achieved without                                  KAS2 eCK                      ∀         1        1     1     1
human heuristics, as they were not necessary to solve all lemmas
in the case study. For some case studies, we fail to reproduce the                                    NAXOS eCK                     ∀         1        0     1     1
reported results from the original papers (See Section B in the                                       NAXOS eCK PFS                 ∀         1        1     1     1
Appendix for details).
                                                                                                                                    ∀         3        3     3     3
    We then train and evaluate our approach as described in Sec-                                      Tutorial
                                                                                                                                    ∃         1        1     1     1
tion 5.5. We experiment with multiple configurations, varying key
hyperparameters such as the heuristic influence 𝜆, exploration coef-                                  UM PFS                        ∀         2        2     2     2
ficients, and search budget 𝐵. We report the details in Table 3 in the                                                              ∀       3 (0)      0     0     1
Appendix. We report the results of the best single configuration.                                     YubiKey
                                                                                                                                    ∃         1        1     1     1
    We use an Intel(R) Xeon(R) CPU E5-4650L 2.60GHz machine
with 1TB of RAM and 8 cores per Tamarin call for the Tamarin                                          YubiKey HSM                   ∀         4        4     4     4
baseline experiments. For our reinforcement learning setting, we                                                          Complex Models
use one NVIDIA A100 GPU with 40GB of memory, up to 64 cores
                                                                                                                                    ∀         7        2     2     7
AMD Rome 7742, 2.25 GHz, and 250GB of RAM. While we have not                                          5G Handover EPS N26
                                                                                                                                    ∃         1        1     1     1
systematically evaluated on consumer-grade CPU-only hardware,
running without a GPU is generally possible. We recommend at                                          PKCS11 AEAD                   ∀         4        3     4     4
least 60 GB of memory. Due to reduced worker parallelization and                                                                    ∀       4 (1)      1     1     4
slower training, longer run times are to be expected.                                                 Signal
                                                                                                                                    ∃       1 (0)      1     0     1
    Less Effort. In Table 1 we summarize the number of lemmas                                                                       ∀         6        4     6     6
                                                                                                      Wireguard
solved by each approach. The Total column shows the total number                                                                    ∃         2        1     2     2
of lemmas in each case study, split into universal and existential lem-                                               State-of-the-Art Models
mas. Our approach consistently matches or outperforms Tamarin’s
baseline heuristics, with the advantage becoming more pronounced                                                                    ∀       9 (8)      5     6     9
                                                                                                      5G AKA
on the complex and state-of-the-art models. On the classical models,                                                                ∃         4        3     3     4
we match the baseline and solve one additional lemma on YubiKey3 .                                                                  ∀        13        3     3     8
    On the complex models, the gap widens substantially: Our ap-                                      5G Handover XN
                                                                                                                                    ∃        7         0     0     1
proach solves all lemmas on 5G Handover and Signal, whereas the
                                                                                                                                    ∀        31       24    28    30
baselines solve only a fraction, that is 3 out of 8 on 5G Handover,                                   SPDM
                                                                                                                                    ∃      18 (17)    14    15     7
and on Signal 1 out of 5 even with the original heuristic, while 2
out of 5 with the c heuristic. On WireGuard and PKCS11, we match                                                                    ∀       73        41    32    71
                                                                                                      WPA2
the baseline with all lemmas solved.                                                                                                ∃      12 (2)     2     2      2
    On the state-of-the-art models, we continue to outperform the
baseline significantly, solving 73 of 85 WPA2 lemmas (baseline: 43)
and 9 of 20 5G Handover XN lemmas (baseline: 3). On the 5G AKA
model, we solve all 13 lemmas, whereas the baseline solves only                                  configuration also solves one additional WPA2 lemma, bringing
9, and the original heuristics 12. On WPA2 we solve an additional                                the union to 74.
30 lemmas compared to the best baseline heuristic and almost                                        On the SPDM model, we do not fully match the baseline heuris-
match the original heuristics (us 73 vs. original 75), without needing                           tics, solving 37 out of 49 lemmas vs. 43. We attribute this to the size
any person-months of manual effort to design heuristics. On top                                  and complexity of the model: Single Tamarin calls can take up to
of the results in Table 1 (best single configuration), a second RL                               10 minutes (timeout), and sequential backup calls can add up to 90
                                                                                                 minutes per node expansion. This severely limits exploration, and a
3 This is not the YubiKey model verified in the SmartVerif paper [47] (see Section 7), as        greedy selection strategy, as the baseline heuristics employ, can per-
their version appears to be a SAPIC+ [6] model that was translated to Tamarin.                   form better in such a setting. In addition, the SPDM model contains
                                                                                            10
Less Effort, Shorter Proofs: Reinforcement Learning
for Security Protocol Analysis in Tamarin


a large number of existential lemmas, which we find particularly                show the average proof size for those lemmas that were solved
difficult for our approach, as described in the Limitations.                    by both our RL approach and either respective baseline heuristics,
   In summary, our approach matches or significantly outperforms                whereas the columns Orig. ∩ RL show the averages for those lem-
the default heuristics across all models except the SPDM model,                 mas that were solved by both our RL approach and Tamarin with
proving statements that previously required human guidance. Our                 the original heuristic. Note that for some easier models, the original
approach nearly matches the original, human-engineered heuristics               heuristics and the baseline heuristics are identical.
on the most complex models, without any manual engineering                         Compared to the baseline heuristics, we find shorter or equal
effort for heuristics. Moreover, our approach outperformed the                  sized proofs across all models. In some cases, the difference is sub-
original heuristics on several models where the originally reported             stantial, with a factor of over 18 for YubiKey HSM and up to 500
performance was no longer reproducible with the current Tamarin                 for the 5G Handover model. Such differences make shorter proofs
version, highlighting the brittleness of changes in Tamarin versions            not only a theoretical advantage but a practical necessity, as proofs
and the advantage of our approach being more robust to such                     of sizes in the thousands are impossible to interpret.
changes. While our approach does not yet fully automate proof                      Our approach also often finds shorter proofs than the human-
search for the most complex models, it substantially reduces the                written original heuristics. Most notably, we produce shorter proofs
human effort required.                                                          on 5G Handover EPS N26 (factor 3.5), 5G Handover XN (factor 2.1),
                                                                                and WPA2 and SPDM (factor 1.5–1.6). Thus, our proofs distill the
Table 2: Average proof size for the lemmas solved by both the                   key proof steps, making them easier to understand than the proofs
respective baseline and our approach (RL). Best configuration                   produced by the baseline and original heuristics.
per lemma. See the paragraph Shorter Proofs in Section 6 for
                                                                                   Execution Time. Since our approach interleaves training and
a detailed explanation and discussion of this table.
                                                                                search, the proof times include both neural network updates and
                                                                                proof search via Tamarin. On the classical models, all lemmas are
                                         c/s ∩ RL          Orig. ∩ RL           solved within a couple of minutes, and on the complex models, it
      Protocol                          c/s           RL   Orig.   RL           takes between a few minutes (5G Handover EPS N26, WireGuard)
                                                                                and about two hours (Signal). Notably, on 5G Handover EPS N26,
                             Classical Models                                   our approach solves more lemmas faster than both of Tamarin’s
      FOO Eligibility                   21.0      20.3      21.0    20.3        built-in heuristics: 3 minutes vs. 45 minutes (c) and 49 minutes (s).
      KAS2 eCK                          12.0      11.0      16.0    11.0        On the state-of-the-art models, our search requires between 4.5 and
      NAXOS eCK                        134.0     117.0     134.0   117.0        20 hours. While this is a significant computational cost, it remains
      NAXOS eCK PFS                     13.0       8.0      13.0     8.0        well within a practical time frame and automates a significant part
      Tutorial                           9.0       8.2       9.0     8.2        of the person-months of manual heuristic engineering that were
      UM PFS                             8.0       8.0       8.0     8.0        necessary to solve a similar number of lemmas in these models. A
      YubiKey                           12.0      12.0      12.0    12.0        full timing comparison is provided in Section A.
      YubiKey HSM                      378.8      20.8     570.0    20.8
                                                                                    Limitations & Future Work. When conducting our experi-
                             Complex Models                                     ments, we observed that our approach underperforms on existential
      5G Handover EPS N26            9531.7       17.3      85.8    24.4        lemmas. We believe that this is due to two factors: First, solutions
      PKCS11 AEAD                     471.8      245.2     471.8   245.2        to existential lemmas are usually much deeper in the search tree
      Signal                           18.0       15.5      20.0    20.0        than proofs for universal lemmas. As the search space grows expo-
      Wireguard                        77.4       49.1      47.8    49.1        nentially with the depth of the tree, search-based methods struggle
                                                                                to find deep solutions and thus to solve existential lemmas. Con-
                        State-of-the-Art Models                                 sequently, search-based methods must be particularly well guided
      5G AKA                         1679.0      148.8      73.3   118.6        to find such deep solutions, which brings us to the second factor:
      5G Handover XN                   26.3       20.7     102.8    48.3        Our models learn from completed (sub-)proofs. A subproof through
      SPDM                             94.9       64.6     106.1    70.8        finding a solved constraint system immediately finishes the proof
      WPA2                            903.7       34.8      81.9    52.0        on these lemmas, hence we cannot learn from this data within the
                                                                                same search. Subproofs through contradictory constraint systems,
                                                                                on the other hand, occur rarely in existential lemmas, as the prop-
   Shorter Proofs. While proof size is not the primary optimiza-                erty is meant to be satisfied, and thus the search generates relatively
tion objective when verifying security protocols, shorter proofs are            little training data for our model. In turn, the search on existential
generally preferable as they are easier to understand and easier to             lemmas is less informed, adding to the difficulty of finding solutions
maintain. Similarly, counterexamples are easier to interpret when               for them. We consider specialized solutions for existential lemmas
they are smaller, making it easier to identify and fix bugs in both the         an interesting target for future work. Possible approaches are a
model and the real-world protocol. Our approach finds significantly             different backup logic or a different paradigm for selecting training
shorter proofs than the baseline heuristics and often shorter proofs            data, as well as a specialized reward signal for existential lemmas.
than the original, human-engineered heuristics. The columns in                      Another challenge we encountered is the amount of time it takes
Table 2 show the average proof size for the lemmas solved by the                to execute proof steps with Tamarin. For instance, for the SPDM
respective approach. For a fair comparison, the columns c/s ∩ RL                model and 5G Handover XN model, we observed that a single node
                                                                           11
                                                                                                                     Cosler, Cremers, Finkbeiner, Ghanem, Medinger


expansion can take up to 90 minutes, with an average of 30 min-                    In our approach, we extend Tamarin with a reusable REST API
utes. This significantly limits the search space we can explore and             instead of integrating the search directly into Tamarin. We learn
thus the performance of our approach. This drawback affects any                 the encoding of a proof state through a transformer over tokenized
approach that searches through the proof methods. Directing the                 proof methods, and our approach uses MCTS to proactively guide
search better would address this, e.g., through machine learning                the search through learned and backed-up signals rather than rely-
models with stronger initial knowledge from pretraining. In this                ing on a fixed loop-detection heuristic.
work, we have not yet established whether transfer learning across                 Although the SmartVerif paper [47] states that its artifacts are
protocols, which is the basis for pretraining, is effective. In contrast        available, this no longer seems to be the case4 . Without access
to related work in mathematical theorem proving, where the under-               to SmartVerif’s implementation and protocol formalizations, it is
lying deductive system is fixed and thus pretraining is possible, in            impossible to evaluate our approach on its models, or vice versa.
Tamarin, each protocol model defines its own semantics and should               Nevertheless, we chose several of our classical protocols in Section 6
be viewed as its own deductive system. Thus, it is an open question             inspired by SmartVerif’s evaluation.
whether transfer learning across protocols is effective.
                                                                                8     Conclusion
7    Related Work                                                               In this work, we have extended the Tamarin prover with an API
                                                                                for proof search and used it to implement a new, reinforcement
   Reinforcement Learning for Theorem Proving. In recent                        learning-guided proof search in the style of AlphaZero [33]. In
years, there has been increasing interest in using machine learn-               contrast to Tamarin’s current greedy search guided by internal or
ing for mathematical reasoning and interactive theorem proving.                 human-written heuristics, our approach performs a graph search
Approaches range from generating whole proofs [21, 40, 48] to                   over the applicable constraint solving rules and learns a policy and
iteratively selecting single proof steps [2, 19, 20, 25, 31]; our work          value function to guide this search. We have evaluated our approach
falls in the latter category. Much of this line of work traces back to          on 16 case studies, and we have found that it outperforms Tamarin’s
the AlphaGo lineage [33–35], which combines learned policy and                  heuristics in terms of the number of lemmas solved and the size
value functions with MCTS. Notable examples include HTPS [25],                  of the proofs found. In particular, our approach performs well on
ABEL [19], DeepSeek-Prover-V1.5 [44], and AlphaProof [20], adapt-               the most complex, state-of-the-art models, often achieving similar
ing the AlphaZero framework to theorem proving by using an                      performance to human-written heuristics. Thus, our work reduces
MCTS to search over applicable proof steps or tactics. Similar to               the amount of human effort required to find proofs in Tamarin
our work, the proof search is structured as an AND/OR tree: Proof               and opens up new avenues for future research on proof search in
states where tactics are generated and selected are OR-nodes, while             Tamarin.
case splits are AND-nodes. The policy and value networks are
trained on data generated by the MCTS itself, following the same                References
self-play reinforcement learning paradigm as AlphaZero. Different                [1] 2026. The Tamarin prover github repository. https://github.com/tamarin-
from our work, HTPS [25] and ABEL [19] extract training data                         prover/tamarin-prover
only after a proof search ends, while AlphaProof [20] additionally               [2] Kshitij Bansal, Sarah Loos, Markus Rabe, Christian Szegedy, and Stewart Wilcox.
                                                                                     2019. HOList: An environment for machine learning of higher order logic
requires the root to be fully solved. We extract training samples                    theorem proving. In Proceedings of the 36th International Conference on Machine
from sub-proofs mid-search to benefit from those learning signals                    Learning. PMLR, 454–463. https://proceedings.mlr.press/v97/bansal19a.html
as soon as possible. Since these systems target interactive theorem              [3] David Basin, Cas Cremers, Jannik Dreier, and Ralf Sasse. 2025. Modeling and
                                                                                     analyzing security protocols with Tamarin: a comprehensive guide. Springer
provers such as Lean, they rely on pretraining their neural networks                 Nature.
on large corpora of existing proofs, mathematical text, and code.                [4] Bruno Blanchet. 2001. An efficient cryptographic protocol verifier based on
                                                                                     Prolog rules. In 14th IEEE computer security foundations workshop (CSFW-14).
For instance, AlphaProof additionally uses a Gemini-based LLM to                     IEEE Computer Society, Cape Breton, Nova Scotia, Canada, 82–96.
autoformalize approximately one million natural-language prob-                   [5] Cameron B Browne, Edward Powley, Daniel Whitehouse, Simon M Lucas, Peter I
lems into roughly 80 million formal Lean statements as additional                    Cowling, Philipp Rohlfshagen, Stephen Tavener, Diego Perez, Spyridon Samoth-
                                                                                     rakis, and Simon Colton. 2012. A survey of monte carlo tree search methods.
training data. Our approach does not use pretraining and instead                     IEEE Transactions on Computational Intelligence and AI in games 4, 1 (2012), 1–43.
trains from scratch on individual protocols.                                     [6] Vincent Cheval, Charlie Jacomme, Steve Kremer, and Robert Künnemann. 2022.
                                                                                     { SAPIC+ } : protocol verifiers of the world, unite!. In 31st USENIX Security Sym-
                                                                                     posium (USENIX Security 22). 3935–3952.
   Machine Learning for Security Protocol Verification. The                      [7] Cremers, Cas and Dax, Alexander and Naska, Aurora. 2023. Formal analysis of
most closely related work is SmartVerif [47], which integrates a                     SPDM: Security protocol and data model version 1.2. In Usenix 2023.
                                                                                 [8] Cremers, Cas and Dax, Alexander and Naska, Aurora. 2025. Breaking and
Deep Q-Network (DQN) into a modified version of Tamarin to                           provably restoring authentication: A formal analysis of SPDM 1.2 including
select which leaf node to expand in the proof search tree. Each node                 cross-protocol attacks. In Proceedings of the 2025 ACM SIGSAC conference on
                                                                                     computer and communications security. 1424–1438.
is represented by a low-dimensional feature vector derived from                  [9] Cremers, Cas and Horvat, Marko and Hoyland, Jonathan and Scott, Sam and
the applied constraint reduction rule and the current step depth,                    van der Merwe, Thyla. 2017. A comprehensive symbolic analysis of TLS 1.3. In
although the paper does not specify how this vector is constructed.                  Proceedings of the 2017 ACM SIGSAC conference on computer and communications
                                                                                     security (Ccs ’17). Association for Computing Machinery, New York, NY, USA,
SmartVerif’s DQN greedily selects the highest-Q-value child at each                  1773–1788. doi:10.1145/3133956.3134063
step without any lookahead search, and it learns exclusively from
                                                                                4 They are not accessible at the dropbox URL from the paper or through the authors’
a loop-detection heuristic based on Levenshtein distance between
                                                                                webpages. The v6 release of the corresponding ArXiv paper [45] contains a link to a
the string representation of the proof methods, assigning a uniform             github repo [42], but this repository no longer exists. The latest v7 arXiv version [46]
negative reward to paths identified as looping.                                 and journal version [41] do not provide any artifact links.
                                                                           12
Less Effort, Shorter Proofs: Reinforcement Learning
for Security Protocol Analysis in Tamarin


[10] Cremers, Cas and Horvat, Marko and Scott, Sam and van der Merwe, Thyla. 2016.            [30] Aleksi Peltonen, Ralf Sasse, and David Basin. 2021. A comprehensive formal
     Automated analysis and verification of TLS 1.3: 0-RTT, resumption and delayed                 analysis of 5G handover. In Proceedings of the 14th ACM conference on security and
     authentication. In 2016 IEEE symposium on security and privacy (SP). 470–485.                 privacy in wireless and mobile networks (WiSec ’21). Association for Computing
     doi:10.1109/SP.2016.35                                                                        Machinery, New York, NY, USA, 1–12. doi:10.1145/3448300.3467823
[11] Cremers, Cas and Kiesl, Benjamin and Medinger, Niklas. 2020. A formal analysis           [31] Stanislas Polu and Ilya Sutskever. 2020. Generative language modeling for
     of IEEE 802.11’s WPA2: countering the kracks caused by cracking the counters.                 automated theorem proving. arXiv:2009.03393 [cs] doi:10.48550/arXiv.2009.03393
     In Proceedings of the 29th USENIX conference on security symposium (SEC’20).             [32] Maiwenn Racouchot. 2024. Formal analysis of security protocols : real-world
     USENIX Association, USA, Article 1.                                                           case-studies and automated proof strategies. Ph. D. Dissertation. doi:10.70675/
[12] Cremers, Cas and Kiesl, Benjamin and Medinger, Niklas. 2020. Presentation                     a4b61c5dz65f8z4921z920fz51e1a9860549
     of a formal analysis of IEEE 802.11’s WPA2: Countering the kracks caused by              [33] David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew
     cracking the counters. https://www.usenix.org/conference/usenixsecurity20/                    Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Grae-
     presentation/cremers                                                                          pel, Timothy Lillicrap, Karen Simonyan, and Demis Hassabis. 2017. Mastering
[13] Johannes Czech, Patrick Korus, and Kristian Kersting. 2020. Monte-carlo graph                 chess and shogi by self-play with a general reinforcement learning algorithm.
     search for AlphaZero. arXiv:2012.11045 [cs] doi:10.48550/arXiv.2012.11045                     arXiv:1712.01815 [cs] doi:10.48550/arXiv.1712.01815
[14] David A. Basin and Jannik Dreier and Lucca Hirschi and Sasa Radomirovic and              [34] David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew
     Ralf Sasse and Vincent Stettler. 2018. Formal analysis of 5G authentication. CoRR             Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Grae-
     abs/1806.10360 (2018). arXiv:1806.10360 http://arxiv.org/abs/1806.10360                       pel, Timothy Lillicrap, Karen Simonyan, and Demis Hassabis. 2018. A general
[15] David A. Basin and Ralf Sasse and Jorge Toro-Pozo. 2020. The EMV standard:                    reinforcement learning algorithm that masters chess, shogi, and go through
     Break, fix, verify. CoRR abs/2006.08249 (2020). arXiv:2006.08249 https://arxiv.               self-play. Science 362, 6419 (Dec. 2018), 1140–1144. doi:10.1126/science.aar6404
     org/abs/2006.08249                                                                       [35] David Silver, Julian Schrittwieser, Karen Simonyan, Ioannis Antonoglou, Aja
[16] Danny Dolev and Andrew Yao. 1983. On the security of public key protocols.                    Huang, Arthur Guez, Thomas Hubert, Lucas Baker, Matthew Lai, Adrian Bolton,
     IEEE Transactions on information theory 29, 2 (1983), 198–208.                                Yutian Chen, Timothy Lillicrap, Fan Hui, Laurent Sifre, George van den Driessche,
[17] Jason A Donenfeld and Kevin Milner. 2017. Formal verification of the WireGuard                Thore Graepel, and Demis Hassabis. 2017. Mastering the game of go without hu-
     protocol. Technical Report, Tech. Rep. (2017).                                                man knowledge. Nature 550, 7676 (Oct. 2017), 354–359. doi:10.1038/nature24270
[18] Nancy Durgin, Patrick Lincoln, John Mitchell, and Andre Scedrov. 2004. Multiset          [36] Richard S. Sutton and Andrew G. Barto. 2020. Reinforcement learning, second
     rewriting and the complexity of bounded security protocols. Journal of Computer               edition: An introduction. Bradford Books, Cambridge, Massachusetts London,
     Security 12, 2 (2004), 247–311.                                                               England.
[19] Fabian Gloeckle, Jannis Limperg, Gabriel Synnaeve, and Amaury Hayat. 2024.               [37] Ferucio Laurentiu Tiplea, Constantin Enea, and Catalin V Bîrjoveanu. 2005.
     ABEL: Sample efficient online reinforcement learning for neural theorem proving.              Decidability and complexity results for security protocols. VISSAS 1 (2005),
     In The 4th Workshop on Mathematical Reasoning and AI at NeurIPS’24. https:                    185–211.
     //openreview.net/forum?id=kk3mSjVCUO                                                     [38] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
[20] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z. Horváth, Goran Žužić,                  Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is
     Eric Wieser, Aja Huang, Julian Schrittwieser, Yannick Schroecker, Hussain Ma-                 All you Need. In Advances in Neural Information Processing Systems, Vol. 30.
     soom, Ottavia Bertolli, Tom Zahavy, Amol Mandhane, Jessica Yung, Iuliya Be-                   Curran Associates, Inc.        https://proceedings.neurips.cc/paper/2017/hash/
     loshapka, Borja Ibarz, Vivek Veeriah, Lei Yu, Oliver Nash, Paul Lezeau, Salva-                3f5ee243547dee91fbd053c1c4a845aa-Abstract.html
     tore Mercuri, Calle Sönne, Bhavik Mehta, Alex Davies, Daniel Zheng, Fabian               [39] Oriol Vinyals, Meire Fortunato, and Navdeep Jaitly. 2015. Pointer Networks.
     Pedregosa, Yin Li, Ingrid von Glehn, Mark Rowland, Samuel Albanie, Ameya Vel-                 In Advances in Neural Information Processing Systems, Vol. 28. Curran As-
     ingker, Simon Schmitt, Edward Lockhart, Edward Hughes, Henryk Michalewski,                    sociates, Inc.     https://proceedings.neurips.cc/paper_files/paper/2015/hash/
     Nicolas Sonnerat, Demis Hassabis, Pushmeet Kohli, and David Silver. 2026.                     29921001f2f04bd3baee84a12e98098f-Abstract.html
     Olympiad-level formal mathematical reasoning with reinforcement learning.                [40] Haiming Wang, Huajian Xin, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing
     Nature 651, 8106 (March 2026), 607–613. doi:10.1038/s41586-025-09833-y                        Cao, Yinya Huang, Jing Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, Heng
[21] Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng                 Liao, and Xiaodan Liang. 2023. LEGO-Prover: Neural Theorem Proving with
     Liu, Wenda Li, Mateja Jamnik, Guillaume Lample, and Yuhuai Wu. 2022. Draft,                   Growing Libraries. arXiv:2310.00656 [cs.AI] https://arxiv.org/abs/2310.00656
     sketch, and prove: Guiding formal theorem provers with informal proofs. In               [41] Wansen Wang, Wenchao Huang, Zhaoyi Meng, Yan Xiong, and Cheng Su. 2024.
     The Eleventh International Conference on Learning Representations. https://                   Advancing the Automation Capability of Verifying Security Protocols . IEEE
     openreview.net/forum?id=SMa9EAovKMC                                                           Transactions on Dependable and Secure Computing 21, 06 (Nov. 2024), 5059–5070.
[22] Nadim Kobeissi, Karthikeyan Bhargavan, and Bruno Blanchet. 2017. Automated                    doi:10.1109/TDSC.2024.3368131
     verification for secure messaging protocols and their implementations: A sym-            [42] Wang, Wansen and Huang, Wenchao and Meng, Zhaoyi and Xiong, Yan and Su,
     bolic and computational approach. In 2017 IEEE European symposium on security                 Cheng. 2019. GitHub repository of “Verifying Security Protocols using Dynamic
     and privacy (EuroS&P). IEEE, 435–450.                                                         Strategies”. https://github.com/SmartVerif/SmartVerif
[23] Levente Kocsis and Csaba Szepesvári. 2006. Bandit based monte-carlo planning.            [43] David J. Wu. 2019. Monte-carlo graph search from first principles. KataGo
     In Machine Learning: ECML 2006, Johannes Fürnkranz, Tobias Scheffer, and Myra                 Documentation, GitHub. https://github.com/lightvector/KataGo/blob/master/
     Spiliopoulou (Eds.). Springer, Berlin, Heidelberg, 282–293. doi:10.1007/11871842_             docs/GraphSearch.md
     29                                                                                       [44] Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng
[24] Robert Künnemann and Graham Steel. 2012. YubiSecure? Formal security analy-                   Wang, Bo Liu, Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu,
     sis results for the YubiKey and YubiHSM. In International workshop on security                Dejian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and Chong Ruan. 2024. DeepSeek-
     and trust management. Springer, 257–272.                                                      prover-V1.5: Harnessing proof assistant feedback for reinforcement learning and
[25] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien                              monte-carlo tree search. arXiv:2408.08152 [cs] doi:10.48550/arXiv.2408.08152
     Rodriguez, Amaury Hayat, Thibaut Lavril, Gabriel Ebner, and Xavier                       [45] Yan Xiong, Cheng Su, Wenchao Huang, Fuyou Miao, Wansen Wang, and
     Martinet. 2022.        HyperTree proof search for neural theorem proving.                     Hengyi Ouyang. 2019. Verifying Security Protocols using Dynamic Strategies.
     In Advances in Neural Information Processing Systems, Vol. 35. 26337–                         arXiv:1807.00669 [cs.CR] https://arxiv.org/abs/1807.00669v6
     26349.              https://proceedings.neurips.cc/paper_files/paper/2022/hash/          [46] Yan Xiong, Cheng Su, Wenchao Huang, Fuyou Miao, Wansen Wang, and
     a8901c5e85fb8e1823bbf0f755053672-Abstract-Conference.html                                     Hengyi Ouyang. 2019. Verifying Security Protocols using Dynamic Strategies.
[26] Felix Linker, Ralf Sasse, and David Basin. 2025. A formal analysis of Apple’s                 arXiv:1807.00669 [cs.CR] https://arxiv.org/abs/1807.00669v7
     iMessage PQ3 protocol. In 34th USENIX security symposium (USENIX security 25).           [47] Yan Xiong, Cheng Su, Wenchao Huang, Fuyou Miao, Wansen Wang, and Hengyi
     5015–5034.                                                                                    Ouyang. 2020. SmartVerif: Push the limit of automation capability of verify-
[27] Felix Linker, Christoph Sprenger, Cas Cremers, and David Basin. 2025. Looping                 ing security protocols by dynamic strategies. In 29th USENIX Security Sym-
     for good: Cyclic proofs for security protocols. In Proceedings of the 2025 ACM                posium (USENIX Security 20). 253–270. https://www.usenix.org/conference/
     SIGSAC conference on computer and communications security. 2759–2773.                         usenixsecurity20/presentation/xiong
[28] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer            [48] Xueliang Zhao, Wenda Li, and Lingpeng Kong. 2023. Decomposing the
     Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. RoBERTa: A                    Enigma: Subgoal-based Demonstration Learning for Formal Theorem Proving.
     robustly optimized BERT pretraining approach. arXiv:1907.11692 [cs] doi:10.                   arXiv:2305.16366 [cs.CL] https://arxiv.org/abs/2305.16366
     48550/arXiv.1907.11692
[29] Simon Meier, Benedikt Schmidt, Cas Cremers, and David A. Basin. 2013. The
     TAMARIN prover for the symbolic analysis of security protocols. In CAV (Lecture
     notes in computer science, Vol. 8044). Springer, 696–701.


                                                                                         13
                                                                                                              Cosler, Cremers, Finkbeiner, Ghanem, Medinger


A    Additional Experimental Data                                              not able to find the proofs automatically because of differences in
   Hyperparameters. Table 3 lists the hyperparameters of the                   Tamarin versions.
best configuration per protocol as reported in Table 1. For WPA2, a               For the Signal model from [27], we only solve 1 out of 5 lemmas
second configuration (†) solves one additional lemma not covered by            with the authors heuristics, while the paper reports that all lemmas
the best configuration, as discussed in Section 6. Full configurations         were solved. [27] extends Tamarin with cyclic induction and uses
for reproducibility are in the artifact.                                       the Signal protocol model to compare Tamarin’s performance under
                                                                               trace induction against their cyclic induction extension. Since we
   Proof Sizes. Table 4 provides the full data on proof sizes for              solve all lemmas using our approach, we are sure that the model
all lemmas solved by each approach, including those solved by                  does not need the cyclic induction extension (our Tamarin version
only one approach. This complements the data in Table 2, which is              does not have the cyclic induction extension). Again, we suspect
restricted to lemmas solved by both approaches.                                our failure to reproduce the original results are due to different
                                                                               Tamarin versions: Both our work and the original work modify
    Times. Table 5 gives a complete picture of the time required to            Tamarin and we forked different releases of the main repository.
solve all the lemmas that were in reach for the respective approach.              For the 5G AKA and the SPDM model, we fail to reproduce the
We chose this per protocol aggregation instead of a per lemma                  proof of a single lemma. We ran these lemmas again with a four hour
listing since our approach trains and searches for proofs for all              timeout instead of two, but we still failed to prove them. Since we
lemmas of a protocol concurrently. For a fair comparison with                  solve the other lemmas for these models, the difference in Tamarin
the baseline, we report the longest time it takes to solve a lemma             versions is less likely to be the cause of this failure, but it still might
across all lemmas solved, assuming maximal parallelization on the              be. Another reason for our failure might be that we are not giving
baseline.                                                                      Tamarin enough computational resources. While our hardware
    Since our approach interleaves training and search, the reported           is powerful, we are proving multiple lemmas concurrently, and
times include both neural network updates and proof search via                 we are not the only ones using the compute infrastructure. As a
Tamarin.                                                                       consequence, there is some non-determinism in the actual available
    On the classical models, all lemmas are solved within a couple             computational resources.
of minutes. On the complex models, the time ranges from a few                     For the WPA2 model, we fail to reproduce the proofs for 10
minutes to about two hours: 5G Handover EPS N26 takes 3 minutes,               existential lemmas. Again, this is likely due to the different Tamarin
WireGuard 5 minutes, PKCS11 AEAD 25 minutes, and Signal about                  versions or insufficient computational resources.
2 hours. Notably, on 5G Handover EPS N26, our approach finishes
faster than both of Tamarin’s built-in heuristics individually: 3
minutes vs. 45 minutes (c) and 49 minutes (s). On WireGuard, the
fastest inbuilt configuration (s) is 23 minutes. Interestingly, c and s
are complementary on WireGuard, such that the aggregate time
of the best per-lemma time from either heuristic is 5 minutes 27
seconds, comparable to our 5 minutes 10 seconds. Our approach
combines the best of both worlds into a single configuration that
solves all lemmas in 5 minutes 10 seconds. On the state-of-the-art
models, training requires between 4.5 hours (5G Handover XN) and
20 hours (5G AKA), with SPDM at about 18 hours and WPA2 at
about 13 hours. While this is a significant computational cost, it
remains well within a practical time frame and automates a signif-
icant part of the person-months of manual heuristic engineering
that were necessary to achieve comparable results on these models.

B    Original Results Reproduction
We fail to prove all lemmas proven in the original models of the
YubiKey, Signal, 5G AKA, SPDM, and WPA2 case studies, even
though we used timeouts of up to four hours per lemma, which is
significantly longer than the timeouts used in the original papers.
We discuss potential reasons for this failure below.
   The YubiKey paper [24] reports that all lemmas were solved, but
this required finding typing invariants via Tamarin’s source lemmas.
However, the models did not contain such lemmas, and Tamarin did
not report any partial deconstructions, which are usually a sign of
such invariants being necessary. Additionally, we tried running the
models using Tamarin’s auto-sources feature, which automatically
adds sources lemmas, but this did not help either. We suspect that
either the original proofs were done manually or that we were
                                                                          14
Less Effort, Shorter Proofs: Reinforcement Learning
for Security Protocol Analysis in Tamarin


Table 3: Hyperparameters of the best configuration per protocol. 𝐵: search budget, 𝐵 inc : budget increase factor, 𝑆: number of
searches per lemma, 𝑁 : expansion breadth, LR: learning rate, 𝜆: heuristic influence, 𝛿: unvisited penalty, Temp: UCB temperature,
𝑐 and /𝑐 base /𝑐 init : UCB exploration constants, 𝑟 time : time penalty. †: both runs solve the same number of lemmas, but each run
solves one additional lemma that the other run does not solve.

Category                Protocol                      Solved      𝐵    𝐵 inc         𝑆   𝑁          LR    𝜆      𝛿     Temp    𝑐 and    𝑐 base       𝑐 init    𝑟 time
                        FOO Eligibility                   3    1000    1.75          5    3     0.001    0.3     8        10   128     3200        0.0001        0.1
                        KAS2 eCK                          1    1000    1.75          5    3     0.001    0.3     8        10   128     3200        0.0001        0.1
                        NAXOS eCK                         1    1000    1.75          5    3     0.001    0.3     8        10   128     3200        0.0001        0.1
                        NAXOS eCK PFS                     1    1000    1.75          5    3     0.001    0.3     8        10   128     3200        0.0001        0.1
Classical Models
                        Tutorial                          4    1000    1.75          5    3     0.001    0.3     8        10   128     3200        0.0001        0.1
                        UM PFS                            2    1000    1.75          5    3     0.001      0     8        10   128     3200        0.0001        0.1
                        YubiKey                           2    1000    1.75          5   50    0.0001    0.3     8        10    64     3200         0.001        0.1
                        YubiKey HSM                       4    1000    1.75          5   50    0.0001    0.3     8        10    64     3200         0.001        0.1
                        5G Handover EPS N26               8     1000   1.75       5       3    0.0001    0.3      8       10    64      3200        0.001        0.1
                        PKCS11 AEAD                       4     1500   1.75      20       3     0.001    0.3      8       10   128      3200       0.0001        0.1
Complex Models
                        Signal                            5    12000    1.5      35       3    0.0001    0.5      8       50    64     50000        0.001        0.3
                        Wireguard                         8     1500    1.5      15       3    0.0001      1   5000      200    64     10000        0.001        0.1
                        5G AKA                           13    5000     1.5      15       3    0.0001    0.2   100        50   128     19652       0.0001        0.3
                        5G Handover XN                    9    5000     1.5      15      20    0.0001      3    50        10   0.01     3200           0.1       0.3
State-of-the-Art
                        SPDM                             37    2000    1.75       5       3    0.0001    0.5     8        10   128      3200        0.001        0.2
Models
                        WPA2†                            73    1000    1.75       5      20    0.0001    0.3     8        10   128      3200       0.0001        0.1
                        WPA2†                            73    1500    1.75       5       3    0.0001      0     8        10      8      100             1       0.1

Table 4: Average proof size for the lemmas solved by the different approaches, i.e., RL, c, s, and Orig. Intersection columns are
restricted to lemmas solved by both approaches. When c and s are aggregated into a single column, the smallest proof size per
lemma is reported.


                                                                                          Tamarin                        c/s ∩ RL                Orig. ∩ RL
Category                       Protocol                           RL             c              s        Orig.         c/s        RL        Orig.             RL
                               FOO Eligibility                    20.3          102.3           21.0      21.0          21.0     20.3        21.0              20.3
                               KAS2 eCK                           11.0           12.0           16.0      16.0          12.0     11.0        16.0              11.0
                               NAXOS eCK                         117.0           N/A           134.0     134.0         134.0    117.0       134.0             117.0
                               NAXOS eCK PFS                       8.0           13.0           13.0      13.0          13.0      8.0        13.0               8.0
Classical Models
                               Tutorial                            8.2           13.2            9.0       9.0           9.0      8.2         9.0               8.2
                               UM PFS                              8.0            8.0            8.0       8.0           8.0      8.0         8.0               8.0
                               YubiKey                            29.0           12.0           12.0      12.0          12.0     12.0        12.0              12.0
                               YubiKey HSM                        20.8          414.8          570.0     570.0         378.8     20.8       570.0              20.8
                               5G Handover EPS N26                24.4         9532.7         9932.3      85.8        9531.7     17.3        85.8              24.4
                               PKCS11 AEAD                       245.2          736.0          471.8     471.8         471.8    245.2       471.8             245.2
Complex Models
                               Signal                            306.0           18.5           20.0      20.0          18.0     15.5        20.0              20.0
                               Wireguard                          49.1         3816.2           92.0      47.8          77.4     49.1        47.8              49.1
                               5G AKA                            194.0           27.4         1708.1      73.3        1679.0    148.8        73.3             118.6
State-of-the-Art               5G Handover XN                     48.3          286.7           69.7     822.8          26.3     20.7       102.8              48.3
Models                         SPDM                               70.8          270.9           85.9     104.8          94.9     64.6       106.1              70.8
                               WPA2                               52.0         1418.0          102.6      88.9         903.7     34.8        81.9              52.0


                                                                                15
                                                                                                  Cosler, Cremers, Finkbeiner, Ghanem, Medinger


Table 5: Wall-clock time to solve all lemmas of a protocol, assuming as much parallelization across lemmas as each approach
allows. RL times include both training and proof search. Intersection columns pick the shortest time per lemma. Times are
rounded to integer seconds (≥10s) or nearest minute (≥1h).

                                                                    Tamarin                      c/s ∩ RL                 Orig. ∩ RL
Category           Protocol                 RL         c               s        Orig.      c/s              RL          Orig.          RL
                   FOO Eligibility            31s      4.9s             1.3s      1.3s       1.3s           31s            1.3s          31s
                   KAS2 eCK                   32s      5.9s             3.8s      3.8s       3.8s           32s            3.8s          32s
                   NAXOS eCK               3m 11s      N/A              5.3s      5.3s       5.3s        3m 11s            5.3s       3m 11s
                   NAXOS eCK PFS              22s   57m 22s             5.0s      5.0s       5.0s           22s            5.0s          22s
Classical Models
                   Tutorial                   18s      0.5s             0.4s      0.4s       0.4s           18s            0.4s          18s
                   UM PFS                     18s      3.9s             0.8s      0.8s       0.8s           18s            0.8s          18s
                   YubiKey                 2m 23s      4.0s             2.5s      2.5s       2.5s           31s            2.5s          31s
                   YubiKey HSM                49s       48s             34s       34s        26s            49s            34s           49s
                   5G Handover EPS N26     3m 25s    45m 6s         49m 29s       37s     45m 6s           48s            37s        3m 25s
                   PKCS11 AEAD            25m 17s        41s            23s       23s         23s       25m 17s           23s       25m 17s
Complex Models
                   Signal                  1h 50m    1h 40m          1m 12s       48s     1h 40m        3m 22s            48s        1m 16s
                   Wireguard               5m 10s    1h 50m         22m 37s    1m 14s     5m 27s        5m 10s         1m 14s        5m 10s
                   5G AKA                19h 48m    29m 27s         11m 32s        17m   11m 32s        2h 27m          17m         19h 48m
State-of-the-Art   5G Handover XN         4h 36m      1m 8s              42s    1h 28m        39s       1m 59s        3m 22s         4h 36m
Models             SPDM                  17h 48m     3h 42m           3h 6m    49m 21s   21m 23s       17h 48m       17m 49s        17h 48m
                   WPA2                  12h 55m      1h 8m         12m 23s     5m 58s     1h 8m        1h 52m        5m 58s        12h 55m




                                                               16
