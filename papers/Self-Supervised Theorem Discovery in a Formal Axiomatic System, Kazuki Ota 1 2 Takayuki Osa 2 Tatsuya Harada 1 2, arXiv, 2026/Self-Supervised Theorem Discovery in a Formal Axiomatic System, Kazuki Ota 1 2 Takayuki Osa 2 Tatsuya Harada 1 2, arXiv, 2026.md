                                                   Self-Supervised Theorem Discovery in a Formal Axiomatic System


                                                                            Kazuki Ota 1 2 Takayuki Osa 2 Tatsuya Harada 1 2


                                                                  Abstract                                     els (LLMs) such as GPT and Gemini have shown steady
                                                                                                               gains on mathematical benchmarks (OpenAI, 2024b; 2025;
                                              Recent artificial intelligence (AI) systems have                 Gemini Team, 2025). A recent Gemini model was also
                                              shown remarkable progress in mathematical rea-                   reported to achieve gold-medal standard performance at
                                              soning. Many existing approaches, including
arXiv:2606.28747v1 [cs.AI] 27 Jun 2026




                                                                                                               the International Mathematical Olympiad 2025 (Luong &
                                              large language models (LLMs), draw on human                      Lockhart, 2025), highlighting advances in LLM-based math-
                                              prior knowledge in the form of mathematical text,                ematical reasoning.
                                              code, or theorem libraries. Although these ap-
                                              proaches are highly effective in practice, it re-                Although LLMs can perform mathematical reasoning in
                                              mains an open question whether an agent can                      natural language, their outputs can be difficult to verify be-
                                              autonomously discover useful theorems without                    cause they may contain plausible but incorrect statements
                                              such human priors. We study this question in a                   caused by hallucination (Farquhar et al., 2024; Kalai et al.,
                                              formal axiomatic system by developing an agent                   2025). This has motivated work on theorem proving with
                                              that starts from axioms and inference rules alone                formal languages and proof assistants as a path toward rig-
                                              and gradually grows a library of useful theorems.                orous mathematical reasoning. Recent work includes aut-
                                              Concretely, we propose a self-supervised theorem-                oformalization and proof sketching methods that connect
                                              discovery algorithm that alternates between proof                natural-language mathematics to formal proofs (Wu et al.,
                                              search and useful-theorem extraction, building a                 2022; Jiang et al., 2023), methods for generating proofs
                                              theorem library whose entries are reused as lem-                 in proof assistants such as Lean (Han et al., 2022; Polu
                                              mas for subsequent proof search. Experiments                     et al., 2023; Yang et al., 2023; Xin et al., 2024; Zimmer
                                              show that the agent discovers tens of thousands                  et al., 2025; Hubert et al., 2026), and methods that com-
                                              of theorems and finds proofs for human-written                   bine language-model generation with symbolic reasoning
                                              benchmark problems, suggesting that its discov-                  or learned libraries (Trinh et al., 2024; Wang et al., 2024;
                                              eries include theorems meaningful from a hu-                     Dong & Ma, 2025). This line of work highlights the value
                                              man mathematical perspective. Furthermore, the                   of combining formally verifiable reasoning substrates with
                                              discovered theorems improve LLM proof perfor-                    the search capabilities of machine learning models.
                                              mance when provided as prompt lemmas, indicat-                   At the same time, many current methods start from math-
                                              ing that they can serve as external knowledge for                ematical knowledge constructed by humans. For example,
                                              LLM reasoning. Our results provide evidence that                 mathematical language models may use natural-language
                                              useful theorems can emerge from proof search                     mathematical knowledge through pretraining on mathemat-
                                              without relying on human-provided theorem li-                    ical text and code (Azerbayev et al., 2024), and methods
                                              braries. More broadly, they suggest a path toward                that connect natural language to formal proofs often start
                                              self-evolving AI systems for mathematics whose                   from human-written problem statements or informal proofs
                                              discoveries remain formally verifiable.                          (Wu et al., 2022; Jiang et al., 2023). In addition, meth-
                                                                                                               ods for proof generation and retrieval-augmented theorem
                                                                                                               proving often use existing formal libraries and the theo-
                                         1. Introduction                                                       rems and proofs contained in them (Han et al., 2022; Polu
                                                                                                               et al., 2023; Yang et al., 2023). Even methods based on
                                         Artificial intelligence (AI) systems are rapidly improving
                                                                                                               large-scale synthetic data often construct training data from
                                         their mathematical reasoning abilities. Large language mod-
                                                                                                               natural-language mathematical problems (Xin et al., 2024).
                                            1
                                              The University of Tokyo, Japan 2 RIKEN AIP, Japan. Corre-        Such knowledge is highly useful in practice, but it makes it
                                         spondence to: Kazuki Ota <ota@mi.t.u-tokyo.ac.jp>.                    difficult to isolate the question of how much mathematical
                                                                                                               structure an agent can discover from formal rules alone.
                                         The 3 rd AI for Math Workshop at the 43rd International Confer-
                                         ence on Machine Learning (ICML), Seoul, South Korea, 2026.            A related line reduces reliance on human-provided proofs or
                                         Copyright 2026 by the author(s).

                                                                                                           1
                              Self-Supervised Theorem Discovery in a Formal Axiomatic System

existing data by learning from axioms and formal rules (Wu           useful theorems can emerge from proof search based only
et al., 2021; Laurent & Platzer, 2022; Poesia et al., 2024).         on axioms and inference rules, and that they can serve not
These studies show that agents can self-improve in axioma-           only as internal lemmas for the agent but also as knowledge
tized domains and discover theorems or proofs. Kasriel et al.        that assists external reasoning systems.
(2025) is especially close, as it discovers theorems from ax-
                                                                     Our contributions can be summarized as follows:
ioms, reuses them for further search, and evaluates external
usefulness by asking an LLM judge whether they appear use-             1. We formulate propositional theorem proving as a
ful. However, it remains open whether such theorems can                   stack-machine decision process based directly on the
improve an external reasoning agent’s proof performance                   axioms and the inference rule of a Hilbert axiom sys-
when supplied as lemmas. We address this question and                     tem.
show that the theorems discovered by our approach improve              2. We propose a self-supervised theorem-discovery algo-
both the agent’s own proof search and LLM proof search.                   rithm that grows a theorem library from the primitive
In this study, we ask whether an agent can autonomously                   rules of a Hilbert axiom system and then reuses ex-
discover useful theorems without relying on human prior                   tracted theorems as lemmas for further proof search.
knowledge. To isolate this question, we require the agent              3. Our experiments show that our agent discovers tens
to start only from the primitive rules of a formal axiomatic              of thousands of theorems and finds proofs for human-
system, without using an existing theorem library, a proof                written benchmark problems.
corpus, natural-language priors, or an externally provided             4. Finally, we show that the extracted theorems also
training problem set. Human-written problems are used only                improve LLM proof performance when provided as
for evaluation, not for training the agent or constructing the            prompt lemmas, serving as external knowledge for
theorem library.                                                          LLM reasoning.

We instantiate this formal-system setting in a Hilbert axiom
system for propositional logic. This setting is deliberately         2. Preliminaries
minimal: it has only a few primitive rules, but proof search         This section defines the logical setting used throughout the
is still nontrivial and every discovered theorem remains for-        paper. It provides the basis for the stack-machine decision
mally checkable. Specifically, we formulate Hilbert-system           process introduced in Section 3.
proof search as a stack-machine decision process, where the
state is the current proof stack and the actions push Hilbert        Notation for Propositional Formulas. To keep syntax
axioms onto the stack or apply Modus Ponens. Because for-            simple, this paper builds formulas only from implication →
mulas obtained during search can be regarded as theorems,            and falsity ⊥. Standard presentations often use primitive
proof search itself generates theorem candidates.                    connectives such as negation ¬, conjunction ∧, disjunction
On top of this stack-machine formulation, we propose a               ∨, implication →, and biconditional ↔. For expressive
self-supervised theorem-discovery algorithm that grows a             power in classical propositional logic, these connectives
theorem library from the agent’s own proof search. The               need not all be primitive, since implication and falsity form
agent reuses theorems reached during search as future proof          a basis for the usual connectives (Post, 1921). Concretely,
goals and learns a goal-conditioned policy from the action           define ¬A := A → ⊥, A ∨ B := (A → ⊥) → B, and
sequences that reach them. The supervision comes from                A ∧ B := (A → (B → ⊥)) → ⊥. Define A ↔ B as
the agent’s own successful proof prefixes: whenever search           (A → B) ∧ (B → A), expanded using conjunction. Thus,
reaches a theorem, the corresponding action sequence be-             unless otherwise stated, every formula uses only → and ⊥,
comes a training signal for proving that theorem again. It           and other connectives are syntactic sugar expanded by the
then extracts useful theorems from the discovered set and            translations above.
adds them as theorem actions that can be used as lemmas
in later generations of proof search. In this way, the agent         Rules of the Hilbert System. A Hilbert system is an
learns not only to discover theorems, but also to use them to        axiomatic proof system in which theorems are derived from
prove new theorems.                                                  axioms using inference rules (Hilbert & Ackermann, 1950;
                                                                     Mendelson, 2015). The system used in this paper, shown
Experiments show that the proposed method discovers theo-            in Figure 1, consists of three axioms, Ax1, Ax2, Ax3, and
rems that are useful both for the agent’s own proof search           one inference rule, Modus Ponens. The symbols A, B, C in
and for proof search by external LLMs. Specifically, the             the axioms stand for arbitrary formulas. A proof repeatedly
agent discovers tens of thousands of theorems and finds              introduces axioms and applies Modus Ponens, which derives
proofs for human-written benchmark problems. Moreover,               Y from previously obtained formulas X and X → Y . When
the extracted theorems improve LLM proof performance                 the final formula matches the target, it has been derived as a
when provided as prompt lemmas. These results show that              theorem. The bottom panel of Figure 1 shows a proof tree

                                                                 2
                               Self-Supervised Theorem Discovery in a Formal Axiomatic System


     Ax1: A → (B → A)
                                                                         Modus Ponens (MP)                 X         X→Y
     Ax2: (A → (B → C)) → ((A → B) → (A → C))
                                                                                                                 Y
     Ax3: ( ¬A → ¬B) → (B → A)

                                                  Ax1                                    Ax2
                      Ax1             MP       A → (B → A)                (A → (B → C)) → ((A → B) → (A → C))
       MP       A → (B → A)                                  (A → B) → (A → A)
                                             A→A

Figure 1. Hilbert system and proof tree for A → A. Top: the three axioms and Modus Ponens. The axioms respectively mean weakening,
distribution of implication, and contraposition. Bottom: a proof tree deriving A → A from two Ax1 instances, one Ax2 instance, and two
Modus Ponens steps.


for the theorem A → A. It uses two instances of Ax1, one              Formally, for a target formula g, we define the
instance of Ax2, and two applications of Modus Ponens. In             stack-machine decision process as a deterministic,
this way, a Hilbert system proves theorems by combining               goal-conditioned decision process given by the tuple
axioms and inference rules.                                           (S, A, s0 , P ), where S is the set of finite stacks of for-
                                                                      mulas, A = {Ax1, Ax2, Ax3, MP} is the action space, and
Soundness and Completeness. This Hilbert system is                    the initial state s0 is the empty stack. The transition rule
known to be sound and complete for classical propositional            P is deterministic. Each axiom action pushes the corre-
logic (Church, 1996). Soundness means that every formula              sponding Hilbert axiom schema onto the stack. For the
derived in this system is valid under the standard semantics          MP action, we use Hindley–Milner unification over formula
of classical propositional logic. Completeness gives the              metavariables (Hindley, 1969; Milner, 1978; Damas & Mil-
converse guarantee, namely every formula valid in classical           ner, 1982). If the top formula can be unified with an impli-
propositional logic can be derived in this Hilbert system.            cation X → Y and the formula immediately below it can
These properties justify viewing the Hilbert system as one            be unified with X, then the MP action is legal and, when
of the standard axiomatic systems for classical propositional         applied, pops both formulas and pushes the resulting con-
logic.                                                                sequent Y . The process succeeds for goal g when the stack
                                                                      consists of the single formula g. We do not specify a scalar
Difficulty of Finding Proofs. While soundness and com-                reward function in this formulation, because the learning
pleteness guarantee correctness and existence of proofs, they         signals in our method are constructed from self-discovered
do not imply that proofs are easy to find. Indeed, deciding           theorems rather than externally defined rewards.
propositional validity is a coNP-complete problem (Cook,
                                                                      Figure 2 illustrates this view by showing the proof tree for
1971). Moreover, from the perspective of proof complexity,
                                                                      A → A as a stack-machine execution. In this example,
valid formulas need not have short proofs in a given proof
                                                                      two Ax1 actions, one Ax2 action, and two Modus Ponens
system, and proof length can vary substantially across proof
                                                                      actions produce the theorem A → A on the stack. Following
systems (Cook & Reckhow, 1979). Therefore, efficiently
                                                                      this stack-machine decision process, Hilbert-style theorem
finding proofs in the Hilbert system is a nontrivial problem.
                                                                      proving can be treated as a sequential decision problem in
                                                                      which the agent chooses which axiom to introduce and when
3. Stack-Machine Formulation of Theorem                               to apply Modus Ponens.
   Proving
We formulate proof construction in the Hilbert system as              4. Self-Supervised Theorem Discovery
an action sequence executed by a stack machine. A Hilbert             In this section, we describe how the proposed algorithm
proof is usually represented as a proof tree built from ax-           operates on the stack-machine decision process formulated
ioms and Modus Ponens. For a learning algorithm, however,             in Section 3 and how it reuses discovered theorems in subse-
it is more natural to represent proof construction as a se-           quent proof search. The central idea is to construct learning
quential decision process. We therefore flatten proof trees           signals from the agent’s own search trajectories, rather than
into sequences of stack operations.

                                                                  3
                               Self-Supervised Theorem Discovery in a Formal Axiomatic System




Figure 2. Stack-machine execution for the proof tree of A → A. The proof tree in Figure 1 is converted into a linear action sequence:
axiom instances at the leaves are executed as push actions Ax1, Ax2, and Ax3, and internal Modus Ponens nodes are executed as MP
actions. Each MP action pops an implication and its antecedent from the stack and pushes the corresponding consequent. This example
shows that the five-action sequence Ax1, Ax1, Ax2, MP, MP is a proof of A → A.


relying on external proof data or human-provided lemmas.              Algorithm 1 Policy Learning in a Fixed Action Space
Specifically, the policy is learned from self-discovered the-          1: Input: action space A.
orems through goal-conditioned supervised learning. In                 2: Initialize a new policy πθ (A|S, g) for A.
addition, the algorithm extracts theorems that are difficult to        3: Bootstrap the goal buffer G with random rollouts.
reprove and highly general, and adds them as new actions               4: for each iteration do
so that they can be reused as lemmas in subsequent search.             5:    Initialize current training set Dtrain ← ∅.
We describe these components in the following subsections.             6:    for each episode do
                                                                       7:       Sample a goal formula g uniformly from G.
4.1. Learning a Goal-Conditioned Policy from                           8:       Roll out πθ (·|S, g) for T steps.
     Self-Discovered Theorems                                          9:       for each reached theorem ft at time t do
The proposed method learns a goal-conditioned policy                  10:          Add ft to G.
πθ (A|S, g), where S is the current proof stack, g is the             11:          Add proof-prefix examples for ft to Dtrain .
target theorem, and A is a stack-machine action. Here, A              12:       end for
either introduces Ax1, Ax2, or Ax3, or applies MP. The                13:    end for
policy therefore predicts which action should be taken next           14:    Update πθ by cross-entropy on Dtrain .
                                                                      15: end for
to prove the goal formula g from the current stack S.
                                                                      16: Return: goal buffer G.
During search, any state whose stack contains a single for-
mula yields a reached theorem. If the state St contains only
one formula ft at time t, we call St a single-formula stack
and treat ft as a theorem reached in that episode, regardless         current policy update. When ft is reached at time t, the
of whether it matches the original goal formula g. Thus,              prefix up to t is treated as a proof of ft , and for each 0 ≤
even a failed attempt can provide a learning signal when a            t′ < t we add (St′ , At′ , ft ) to Dtrain . The policy πθ (A|S, g)
single-formula stack appears.                                         is then updated by cross-entropy on Dtrain , increasing the
                                                                      likelihood of πθ (At′ |St′ , ft ).
Figure 3 illustrates this construction. The marked states S1 ,
S3 , and S7 contain f1 , f3 , and f7 , and the corresponding          Algorithm 1 summarizes this procedure for a fixed action
action prefixes are proofs of those formulas. These reached           space. It makes explicit that each reached theorem is in-
theorems are then used in two ways, as future goals and as            serted into two objects with different roles. The training set
supervised training data.                                             Dtrain stores proof-labeled examples for the current policy
                                                                      update and is reset at each iteration. In contrast, the goal
We maintain a goal buffer G containing theorems discovered            buffer G is maintained across iterations, so the agent gradu-
during search. Training begins by bootstrapping G with                ally expands the set of goals available for later search. This
random rollouts. Whenever search produces new reached                 separation keeps policy updates local to the current iteration
theorems, they are added to G, and later iterations sample            while preserving discovered theorems as persistent future
a goal formula g uniformly from G before rolling out the              goals.
current policy πθ (·|S, g).
                                                                      Our method shares with Hindsight Experience Replay
Reached theorems also define supervised targets for the               (HER) and goal-conditioned supervised learning (GCSL)

                                                                  4
                                Self-Supervised Theorem Discovery in a Formal Axiomatic System




Figure 3. An example proof-search episode used to generate goals and training data. Marked states are single-formula stacks, and the
corresponding formulas f1 , f3 , and f7 are added to the goal buffer G. For each reached
                                                                                      theorem, we use all preceding state-action prefixes
as training examples: Dtrain ← Dtrain ∪ ∪t∈{1,3,7} {(St′ , At′ , ft ) | 0 ≤ t′ < t} .


the idea of reusing what was actually reached in past tra-              theorem available as a lemma can compress a difficult partial
jectories as new goals (Andrychowicz et al., 2017; Ghosh                proof into a single lemma call. To estimate reprovability, we
et al., 2021). The difference is that the relabeled goals are           use the Bayesian posterior mean p̂g = (mg + 1)/(ng + 2),
not environment states, but proved theorems obtained as                 which corresponds to a Beta(1, 1) prior, rather than the raw
single-formula stacks in the Hilbert system. Thus, formu-               empirical success rate. This smoothing prevents the ranking
las encountered during exploration can be reused as valid               from over-prioritizing theorems that fail after only a few
theorem-proving targets in subsequent search.                           samples and helps identify theorems with persistently low
                                                                        reprovability.
4.2. Extracting Useful Theorems                                         Finally, generality filtering and reprovability ranking are
We extract useful theorems from the discovered theorem                  combined to select useful theorems from G. The method first
set using two criteria, generality and reprovability. The               keeps only the theorems that are not specializations of other
goal buffer G constructed in the previous section serves as             candidates, thereby removing redundant specializations. It
the candidate set. Generality removes overly specialized                then sorts the remaining candidates so that lower values of
theorems, while reprovability prioritizes theorems that have            the reprovability posterior mean p̂g receive higher priority.
already been discovered but cannot be reliably reproved by              Finally, a fixed number of the highest-priority theorems are
the current policy. Adding such theorems as lemmas can                  selected from this ranking and regarded as useful theorems.
expand the set of theorems reached in subsequent proof
search.                                                                 4.3. Reusing Useful Theorems
The first criterion uses the generality order induced by sub-           The proposed method reuses extracted theorems by adding
stituting formulas for variables to remove overly specialized           them to the action space of the stack-machine decision
theorems. For example, the theorem A → A is more general                process. The original action space consists of four ac-
than the theorem (A → B) → (A → B), because substi-                     tions: pushing an instance of Ax1, Ax2, or Ax3 onto
tuting the formula A → B for A in the former yields the                 the stack, and applying the inference rule MP. For each
latter, whereas no variable substitution in the latter yields           extracted theorem, we add one library action, denoted by
the former. We keep only the theorems that are not special-             Thm1, Thm2, . . . , ThmN. When one of these theorem actions
izations of other candidates. Formally, we define a partial             is selected, the corresponding theorem is pushed onto the
order so that more general theorems are smaller, and retain             stack instead of an axiom. The resulting stack-machine deci-
the minimal elements under this order. This filtering re-               sion process allows the agent to reuse theorems discovered
moves redundant specialized theorems while retaining more               in earlier generations as lemmas in later proof search.
general candidates.
                                                                        Algorithm 2 summarizes how the action space is expanded
The second criterion ranks the remaining candidates by                  across generations. The algorithm alternates between policy
estimating how reliably the current policy can reprove them.            learning under a fixed action space and action-space expan-
For each candidate theorem g ∈ G, we record the number                  sion using extracted theorems. In each generation, we train
ng of times g was sampled as a proof goal and the number                a new policy network for the current action space, because
mg of those episodes in which g was proved. A theorem                   adding library actions changes the action space of the stack-
with low reprovability has already been discovered, but the             machine decision process. During policy learning, reached
current policy cannot reliably prove it again. Making such a            theorems accumulate in the goal buffer G through multiple

                                                                    5
                                Self-Supervised Theorem Discovery in a Formal Axiomatic System




Figure 4. Number of discovered theorems in the Hilbert axiom            Figure 5. Proof success rates on human-written benchmark prob-
system. The count increases over generations, indicating that the       lems. Our agent finds Hilbert-system proofs for 30% of them,
agent can grow a theorem library within the Hilbert axiom system.       while GPT baselines indicate the difficulty of the task.


iterations of proof search and supervised updates. At the               settings, so the reported success rates reflect single-shot
end of the generation, useful theorems are extracted from G,            proof generation rather than best-of-k sampling. A prob-
and the corresponding library actions are added to the action           lem is counted as solved only when the generated action
space A. This process turns theorems discovered in one gen-             sequence is accepted by a stack-machine proof checker im-
eration into reusable action primitives for later generations.          plementing Ax1–Ax3, theorem actions, and Modus Ponens
By repeating this process, the agent gradually expands its              with the same unification rule as in Section 3. In the lemma-
action space and grows a library of useful theorems.                    augmented setting, each theorem action pushes the corre-
                                                                        sponding theorem from the extracted library onto the stack.
Algorithm 2 Multi-Generation Library Expansion                          Since each extracted theorem is stored with its primitive
                                                                        axiom/MP proof trajectory, lemma-augmented proofs can in
 1: Initialize action space A ← {Ax1, Ax2, Ax3, MP}.
                                                                        principle be expanded into axiom-only Hilbert proofs.
 2: for each generation do
 3:    Give A to Algorithm 1 and obtain theorem buffer G.
                                                                        5.2. Quantitative Evaluation of Theorem Discovery
 4:    Extract useful theorems {Thm1, . . . , ThmN} from G.
 5:    Expand A ← A ∪ {Thm1, . . . , ThmN}.                             We first evaluate whether the proposed method can grow the
 6: end for                                                             goal buffer G starting only from the axioms and inference
                                                                        rule of the Hilbert axiom system defined in Section 2.
                                                                        Figure 4 shows that the number of discovered theorems
5. Experiments                                                          increases over generations. This result demonstrates that our
5.1. Experimental Setup                                                 approach accumulates found theorems and reuses them to
                                                                        derive further theorems within the formal axiomatic system.
We run theorem discovery and library construction in the
                                                                        We next evaluate coverage on the human-written bench-
Hilbert axiom system shown in Figure 1. The initial action
                                                                        mark problems. Discovering many theorems alone does not
space consists of Ax1, Ax2, Ax3, and MP. Thus, before
                                                                        guarantee that they are meaningful from a human perspec-
any library theorem is extracted, the agent can only push
                                                                        tive. This benchmark consists of classical-logic problems.
instances of the three axioms onto the stack or apply Modus
                                                                        As shown in Figure 5, the discovered theorem set covers
Ponens. We repeat proof search and library extraction over
                                                                        30% of these benchmark problems. This result suggests
six generations. The numbers of extracted theorems added
                                                                        that the agent does not merely generate many theorems, but
to the library are 20, 10, 5, 2, 1, 0 from Generation 1 to Gen-
                                                                        also discovers theorems that are meaningful from a human
eration 6, which yields a final library of 38 theorem actions.
                                                                        perspective.
For benchmark evaluation, we use the 30 human-written
                                                                        We further evaluate the difficulty of solving these bench-
propositional-logic problems derived from Kleene’s text-
                                                                        mark problems in the Hilbert system using LLM baselines.
book (Kleene, 1952) and curated by Poesia et al. (2024).
                                                                        Figure 5 shows the fraction of benchmark problems for
This benchmark provides a human-written test set that is
                                                                        which each GPT baseline (OpenAI, 2023; 2024a; 2025)
independent of our theorem-discovery process. Each LLM
                                                                        finds a Hilbert-system proof path. For GPT-5, low, medium,
baseline is evaluated once per problem with fixed decoding

                                                                    6
                               Self-Supervised Theorem Discovery in a Formal Axiomatic System

Table 1. Qualitative examples in which GPT-5-high failed without prompt lemmas but succeeded when supplied with extracted theorem
actions. The last column lists the theorem actions used in each successful proof.

                    Example Goal formula                                          Used theorem actions
                        1       A → (¬A → B)                                      Thm1, Thm2
                        2       (A → B) → ((B → C) → (A → C))                     Thm3, Thm5
                        3       ¬((A → B) → ¬(B → A)) → (B → A)                   Thm1, Thm2, Thm3, Thm4

Table 2. Extracted theorem actions appearing in the successful qualitative proofs in Table 1. Each action label denotes a discovered
theorem supplied to GPT-5-high as a prompt lemma.

              Action    Theorem formula
              Thm1      ¬A → (A → B)
              Thm2      (A → (B → C)) → (D → ((A → B) → (A → C)))
              Thm3      (A → B) → ((C → A) → (C → B))
              Thm4      (¬A → ¬(B → (C → B))) → A
              Thm5      ((A → (B → C)) → (((A → B) → (A → C)) → D)) → ((A → (B → C)) → D)


and high denote the reasoning effort used at inference time.
Even GPT-5-high, the strongest GPT baseline in our eval-
uation, reaches only about 23% accuracy, which indicates
that constructing Hilbert-system proofs for these benchmark
theorems is nontrivial. Here, we do not aim to claim that
the proposed method generally outperforms state-of-the-art
LLMs. Rather, these results show that the benchmark prob-
lems are difficult to solve in the Hilbert system and indicate
that our approach can discover nontrivial proofs.

5.3. Quantitative Evaluation of Extracted Theorems
We evaluate whether the extracted theorems also function
as external knowledge for LLM proof search. Specifically,
we provide the extracted theorems as prompt lemmas and               Figure 6. Effect of extracted theorems as prompt lemmas for LLM
                                                                     proof search. Providing extracted theorems improves proof success
compare the proof success rate of GPT baselines on human-            rates for GPT-4o and GPT-5 variants.
written benchmark problems. This evaluation tests whether
theorems obtained by our proof-search agent can transfer to
LLMs, which rely on a different reasoning architecture.              theorem actions that appear in these successful proofs.
Figure 6 compares the proof success rate with and without            The first example is especially informative because the two
the extracted theorems provided as prompt lemmas. For                lemmas used in the proof have different roles. With the
GPT-4o and the GPT-5 variants, proof success rates improve           extracted theorems provided as prompt lemmas, GPT-5-
when the extracted theorems are provided as prompt lemmas.           high constructed the following Hilbert-system proof action
This result shows that the extracted theorems can help LLMs          sequence:
find proofs in the Hilbert system. Overall, these results show
that theorems extracted through our approach function as                           Ax1, Thm1, Thm2, MP, Ax2, MP, MP.
transferable knowledge for LLM-based theorem proving.
                                                                     In this proof, Thm1 corresponds to the principle of explo-
5.4. Qualitative Analysis of Extracted Theorems                      sion, deriving an arbitrary B from ¬A and A. Thus, the
                                                                     usefulness of Thm1 is easy to interpret from a human per-
Finally, we examine concrete examples of how extracted
                                                                     spective. In contrast, Thm2 does not appear among the
theorems assist LLM proof construction. Table 1 summa-
                                                                     human-written benchmark problems and was discovered by
rizes three goals for which GPT-5-high failed to find a proof
                                                                     our approach. Although its usefulness is not obvious at first
without prompt lemmas but succeeded when the extracted
                                                                     glance, Thm2 lifts an implication under an additional con-
theorem library was supplied. Table 2 lists the extracted
                                                                     text and contributes to proving the first goal in Table 1 when

                                                                 7
                             Self-Supervised Theorem Discovery in a Formal Axiomatic System

combined with Thm1. This contrast shows that usefulness             Lemma discovery and library learning. Lemma discov-
is not always apparent from human inspection alone.                 ery and library learning are important directions for accel-
                                                                    erating proof search (Yang et al., 2023; Wang et al., 2024).
These examples show that extracted theorems do not merely
                                                                    In contrast to methods that rely on existing formal libraries,
improve aggregate evaluation metrics, but also play con-
                                                                    human-provided lemmas, or LLM-based proving pipelines,
crete roles in individual proof constructions. In particular,
                                                                    our agent discovers useful theorems through proof search
not only human-interpretable theorems such as Thm1 and
                                                                    using only the axioms and inference rule.
Thm3, but also theorems whose usefulness is not obvious
at first glance, such as Thm2, Thm4, and Thm5, function as
effective supporting knowledge when an LLM constructs               Curry–Howard motivation. Our stack-machine view
Hilbert-system proofs. More broadly, this suggests that the-        is also motivated by the Curry–Howard correspondence,
orem discovery without human prior knowledge may allow              which relates propositions to types and proofs to programs
AI systems to surface useful lemmas that humans did not             (Howard, 1980; Sørensen & Urzyczyn, 2006). There, impli-
explicitly provide.                                                 cation resembles a function type and MP resembles function
                                                                    application. This is not central to our claims, but explains
                                                                    why Hilbert proofs can be flattened into action sequences
6. Related Work                                                     that push axioms or lemmas and compose them on a stack.
Learning-guided formal theorem proving. Prior work                  Our MP implementation follows this intuition by unifying
on learning-guided formal theorem proving has studied               an implication antecedent with another stack formula, as
reinforcement-learning proof search, tactic prediction, proof       in Hindley–Milner type inference (Hindley, 1969; Milner,
generation, and LLM-based proving in Lean (Kaliszyk et al.,         1978; Damas & Milner, 1982).
2018; Han et al., 2022; Polu et al., 2023; Yang et al., 2023;
Xin et al., 2024; Zimmer et al., 2025; Hubert et al., 2026).        7. Conclusions
These methods build strong provers using existing formal
libraries or proof data. In contrast, we ask how far theorem        We studied whether useful theorems can be discovered
discovery and reuse can go using only the three axioms and          within a formal axiomatic system using only its primitive
one inference rule of a Hilbert axiom system.                       rules. We formulated Hilbert-system propositional theorem
                                                                    proving as a stack-machine decision process and proposed
                                                                    a learning algorithm that grows a theorem library through
                                                                    proof search. The algorithm treats reached theorems as fu-
Self-play and intrinsic theorem discovery. Another line
                                                                    ture proof goals and extracts useful theorems for reuse as
reduces dependence on human proof examples by learning
                                                                    lemmas. Experiments show that the agent discovers many
proof-search or conjecturing through self-play or intrinsic
                                                                    theorems over multiple generations in the Hilbert axiom sys-
motivation (Wu et al., 2021; Lample et al., 2022; Poesia
                                                                    tem and finds proofs for a meaningful fraction of the human-
et al., 2024; Laurent & Platzer, 2022; Dong & Ma, 2025;
                                                                    written benchmark problems. We also demonstrate that the
Zhao et al., 2025). Kasriel et al. (2025) is especially close
                                                                    extracted theorems improve LLM proof performance when
because it discovers useful theorems from axioms, reuses
                                                                    provided as prompt lemmas.
them for further search, and evaluates external usefulness
by asking an LLM judge whether they appear useful. Com-             A limitation of this study is that our experiments are con-
plementing this direction, we ask whether self-supervised           ducted in a single axiom system. However, the proposed
theorem-discovery methods can find theorems that not only           framework is not specific to this axiom system and should
appear useful, but also actually improve LLM-based proof            be applicable to multiple axiom systems; evaluating this
search when supplied as lemmas.                                     broader applicability is a natural next step. Furthermore,
                                                                    it also remains an important direction for future work to
                                                                    test whether the same approach can scale to richer formal
                                                                    systems with broader applications, such as first-order logic,
Goal-conditioned and hindsight learning. Our learn-
                                                                    set theory, and more general mathematical domains.
ing rule relates to Hindsight Experience Replay and goal-
conditioned supervised learning, which reuse reached states         While we have focused on Hilbert-style propositional theo-
as goals (Andrychowicz et al., 2017; Ghosh et al., 2021).           rem proving, our experiments provide evidence that useful
In our setting, the reached objects are theorems, not envi-         theorems can emerge from proof search without relying
ronment states, and some are reused as both training goals          on human-provided theorem libraries. More broadly, these
and action primitives in subsequent stack-machine decision          findings suggest a path toward self-evolving AI systems
processes. Thus, a proof prefix reaching a formula becomes          for mathematics: systems that autonomously expand their
hindsight supervision for proving it. This connects goal            formal knowledge through proof search while keeping each
relabeling with theorem-proving library learning.                   discovery formally verifiable.

                                                                8
                             Self-Supervised Theorem Discovery in a Formal Axiomatic System

Acknowledgements                                                    next generation agentic capabilities.     arXiv preprint
                                                                    arXiv:2507.06261, 2025.
This work was partially supported by JST Moonshot R&D
Grant Number JPMJPS2011, CREST Grant Number JP-                   Ghosh, D., Gupta, A., Reddy, A., Fu, J., Devin, C., Ey-
MJCR2015 and Basic Research Grant (Super AI) of Insti-              senbach, B., and Levine, S. Learning to reach goals via
tute for AI and Beyond of the University of Tokyo. Kazuki           iterated supervised learning. In International Conference
Ota was supported by JST SPRING, Grant Number JP-                   on Learning Representations, 2021.
MJSP2108. Takayuki Osa was supported by JSPS KAK-
ENHI Grant Number JP25K03176.                                     Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S.
                                                                    Proof artifact co-training for theorem proving with lan-
References                                                          guage models. In International Conference on Learning
                                                                    Representations, 2022.
Andrychowicz, M., Wolski, F., Ray, A., Schneider, J., Fong,
  R., Welinder, P., McGrew, B., Tobin, J., Abbeel, P., and        Hilbert, D. and Ackermann, W. Principles of Mathematical
  Zaremba, W. Hindsight experience replay. In Advances              Logic. Chelsea Publishing Company, New York, 1950.
  in Neural Information Processing Systems, volume 30,              Translated by Lewis M. Hammond, George G. Leckie,
  pp. 5048–5058, 2017.                                              and F. Steinhardt.
Azerbayev, Z., Schoelkopf, H., Paster, K., Dos Santos, M.,
                                                                  Hindley, R. The principal type-scheme of an object in combi-
  McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and
                                                                    natory logic. Transactions of the American Mathematical
 Welleck, S. Llemma: An open language model for math-
                                                                    Society, 146:29–60, 1969.
  ematics. In International Conference on Learning Repre-
  sentations, 2024.                                               Howard, W. A. The formulae-as-types notion of construc-
Church, A. Introduction to Mathematical Logic. Princeton            tion. In Seldin, J. P. and Hindley, J. R. (eds.), To H. B.
  University Press, Princeton, NJ, 1996. Reprint of the            Curry: Essays on Combinatory Logic, Lambda Calculus
  revised 1956 edition. See Propositions 235 and 239, pp.           and Formalism, pp. 479–490. Academic Press, New York,
  127–128.                                                         1980.

Cook, S. A. The complexity of theorem-proving procedures.         Hubert, T., Mehta, R., Sartran, L., Horvath, M. Z., Zuzic,
  In Proceedings of the Third Annual ACM Symposium                  G., Wieser, E., Huang, A., Schrittwieser, J., Schroecker,
  on Theory of Computing, pp. 151–158. Association for             Y., Masoom, H., Bertolli, O., Zahavy, T., Mandhane, A.,
  Computing Machinery, 1971.                                       Yung, J., Beloshapka, I., Ibarz, B., Veeriah, V., Yu, L.,
                                                                    Nash, O., Lezeau, P., Mercuri, S., Sonne, C., Mehta, B.,
Cook, S. A. and Reckhow, R. A. The relative efficiency of           Davies, A., Zheng, D., Pedregosa, F., Li, Y., von Glehn,
  propositional proof systems. Journal of Symbolic Logic,           I., Rowland, M., Albanie, S., Velingker, A., Schmitt, S.,
  44(1):36–50, 1979.                                                Lockhart, E., Hughes, E., Michalewski, H., Sonnerat,
                                                                    N., Hassabis, D., Kohli, P., and Silver, D. Olympiad-
Damas, L. and Milner, R. Principal type-schemes for                 level formal mathematical reasoning with reinforcement
  functional programs. In Proceedings of the 9th ACM                learning. Nature, 651(8106):607–613, 2026. doi: 10.103
  SIGPLAN-SIGACT Symposium on Principles of Program-                8/s41586-025-09833-y.
  ming Languages, pp. 207–212. Association for Comput-
  ing Machinery, 1982.                                            Jiang, A. Q., Welleck, S., Zhou, J. P., Lacroix, T., Liu,
Dong, K. and Ma, T. STP: Self-play LLM theorem provers               J., Li, W., Jamnik, M., Lample, G., and Wu, Y. Draft,
 with iterative conjecturing and proving. In Proceedings             sketch, and prove: Guiding formal theorem provers with
  of the 42nd International Conference on Machine Learn-             informal proofs. In International Conference on Learning
  ing, volume 267 of Proceedings of Machine Learning                 Representations, 2023.
  Research, pp. 14114–14136. PMLR, 2025.
                                                                  Kalai, A. T., Nachum, O., Vempala, S. S., and Zhang,
Farquhar, S., Kossen, J., Kuhn, L., and Gal, Y. Detecting           E. Why language models hallucinate. arXiv preprint
  hallucinations in large language models using semantic            arXiv:2509.04664, 2025.
  entropy. Nature, 630:625–630, 2024. doi: 10.1038/s415
  86-024-07421-0.                                                 Kaliszyk, C., Urban, J., Michalewski, H., and Olšák, M.
                                                                    Reinforcement learning of theorem proving. In Advances
Gemini Team. Gemini 2.5: Pushing the frontier with                  in Neural Information Processing Systems, volume 31,
  advanced reasoning, multimodality, long context, and              2018.

                                                              9
                              Self-Supervised Theorem Discovery in a Formal Axiomatic System

Kasriel, T., Lu, T., Ding, Q., He, J., and Song, D. Usefulness-        Polu, S., Han, J. M., Zheng, K., Baksys, M., Babuschkin, I.,
  driven learning of formal mathematics. In The 5th Work-                and Sutskever, I. Formal mathematics statement curricu-
  shop on Mathematical Reasoning and AI (MATH-AI) at                     lum learning. In International Conference on Learning
  NeurIPS, 2025.                                                         Representations, 2023.
Kleene, S. C. Introduction to Metamathematics. Van Nos-                Post, E. L. Introduction to a general theory of elementary
  trand, 1952.                                                           propositions. American Journal of Mathematics, 43(3):
                                                                         163–185, 1921.
Lample, G., Lachaux, M.-A., Lavril, T., Martinet, X., Hayat,
  A., Ebner, G., Rodriguez, A., and Lacroix, T. HyperTree              Sørensen, M. H. and Urzyczyn, P. Lectures on the Curry–
  proof search for neural theorem proving. In Advances                   Howard Isomorphism, volume 149 of Studies in Logic
  in Neural Information Processing Systems, volume 35,                   and the Foundations of Mathematics. Elsevier, 2006.
  2022.                                                                  ISBN 9780444520777.
Laurent, J. and Platzer, A. Learning to find proofs and                Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T. Solv-
  theorems by learning to refine search strategies: The                  ing olympiad geometry without human demonstrations.
  case of loop invariant synthesis. In Advances in Neural                Nature, 625:476–482, 2024. doi: 10.1038/s41586-023-0
  Information Processing Systems, volume 35, pp. 4843–                   6747-5.
  4856, 2022.
                                                                       Wang, H., Xin, H., Zheng, C., Liu, Z., Cao, Q., Huang,
Luong, T. and Lockhart, E. Advanced version of Gemini                   Y., Xiong, J., Shi, H., Xie, E., Yin, J., Li, Z., and Liang,
  with Deep Think officially achieves gold-medal standard               X. LEGO-Prover: Neural theorem proving with grow-
  at the International Mathematical Olympiad. Google                    ing libraries. In International Conference on Learning
  DeepMind blog, 2025. URL: https://deepmind.g                          Representations, 2024.
  oogle/blog/advanced-version-of-gemin
  i-with-deep-think-officially-achieve                                 Wu, M., Norrish, M., Walder, C., and Dezfouli, A. Tac-
  s-gold-medal-standard-at-the-interna                                  ticZero: Learning to prove theorems from scratch with
  tional-mathematical-olympiad/. Accessed:                              deep reinforcement learning. In Advances in Neural In-
  May 25, 2026.                                                         formation Processing Systems, volume 34, 2021.
Mendelson, E. Introduction to Mathematical Logic.                      Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
 CRC Press, Boca Raton, 6 edition, 2015. ISBN                           nik, M., and Szegedy, C. Autoformalization with large
 9781482237726.                                                         language models. In Advances in Neural Information
                                                                        Processing Systems, volume 35, 2022.
Milner, R. A theory of type polymorphism in programming.
 Journal of Computer and System Sciences, 17(3):348–                   Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan,
 375, 1978.                                                              C., Li, W., and Liang, X. DeepSeek-Prover: Advancing
OpenAI. Introducing APIs for GPT-3.5 Turbo and Whisper,                  theorem proving in LLMs through large-scale synthetic
  2023. OpenAI blog. URL: https://openai.com                             data. arXiv preprint arXiv:2405.14333, 2024.
 /index/introducing-chatgpt-and-whisp                                  Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  er-apis/. Accessed: May 25, 2026.                                      P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
OpenAI. GPT-4o system card, 2024a. URL: https://                         LeanDojo: Theorem proving with retrieval-augmented
  openai.com/index/gpt-4o-system-card/.                                  language models. In Advances in Neural Information
 Accessed: May 25, 2026.                                                 Processing Systems, volume 36, 2023.

OpenAI. OpenAI o1 system card, 2024b. URL: https:                      Zhao, A., Wu, Y., Yue, Y., Wu, T., Xu, Q., Yue, Y., Lin,
 //openai.com/index/openai-o1-system-c                                   M., Wang, S., Wu, Q., Zheng, Z., and Huang, G. Abso-
  ard/. Accessed: May 25, 2026.                                          lute zero: Reinforced self-play reasoning with zero data.
                                                                         In Advances in Neural Information Processing Systems,
OpenAI. GPT-5 system card, 2025. URL: https://                           volume 38, 2025.
  openai.com/index/gpt-5-system-card/.
 Accessed: May 25, 2026.                                               Zimmer, M., Ji, X., Tutunov, R., Bordg, A., Wang, J., and
                                                                         Bou Ammar, H. Bourbaki: Self-generated and goal-
Poesia, G., Broman, D., Haber, N., and Goodman, N. D.                    conditioned MDPs for theorem proving. arXiv preprint
  Learning formal mathematics from intrinsic motivation.                 arXiv:2507.02726, 2025.
  In Advances in Neural Information Processing Systems,
  volume 37, 2024.

                                                                  10
                              Self-Supervised Theorem Discovery in a Formal Axiomatic System

A. Experimental Details
In this section, we explain implementation details for theorem-discovery training and library construction. Each generation
uses 25 training iterations. In each iteration, the agent generates 8192 episodes, and each episode has a maximum length of
7 steps. Therefore, each generation uses 25 × 8192 × 7 simulator evaluations. Episodes are processed in batches of 2048
episodes.
The policy is parameterized by a Transformer network. The model uses embedding dimension 128, four Transformer blocks,
four attention heads, feed-forward dimension 512, dropout rate 0.1, and learned positional encodings. The policy is trained
with cross-entropy loss under a legal-action mask. We use Adam with learning rate 0.001, batch size 512, and one training
epoch per iteration.
The policy observation is a fixed-length sequence of 1024 integer tokens. It consists of the sampled goal formula followed by
the current proof stack, separated by a special field-separator token, and padded to a fixed length. Each formula is tokenized
at the symbol level in reverse Polish notation, with tokens for implication, falsity, variables, and formula separators. Thus, a
training example for πθ (A|S, g) presents the goal formula g and the current stack S to the Transformer.
Across generations, the action space consists of the three axiom actions, the MP action, and the library theorem actions
available at that generation. The legal-action mask is computed from the current stack, the remaining horizon, and the
current action space. It is used to mask illegal actions during sampling and in the cross-entropy loss. When new theorems
are extracted and added to the library, the action space changes accordingly. We therefore initialize and train a new policy
network for the updated action space at each generation.

B. Prompts for LLM Evaluation
We show the prompt template used for LLM evaluation. In the prompt, the axioms corresponding to Ax1, Ax2, and Ax3 in
the main text are denoted by ‘A01’, ‘A02’, and ‘A03’, respectively, and Modus Ponens is denoted by ‘MP’. When discovered
theorems are provided as lemmas, they are listed as ‘L01’, ‘L02’, and so on. For the baseline without lemmas, this lemma
list is empty, and the LLM is asked to construct a proof using only ‘A01’, ‘A02’, ‘A03’, and ‘MP’. The final answer is
requested as an RPN sequence in which actions are separated by spaces.
# Rules
Prove the given proposition in the Hilbert system (with axioms A01, A02, A03 and the
inference rule Modus Ponens).

## Axioms:
A01: A -> (B -> A)
A02: (A -> (B -> C)) -> ((A -> B) -> (A -> C))
A03: (!A -> !B) -> (B -> A)

## Inference Rule (MP):
In the stack, the top element is regarded as X->Y, and the one below it as X. Unify the
antecedents of X and X->Y as in Hindley-Milner type inference, and as a result derive the
consequent Y, which is then pushed onto the stack. For example, if the top of the stack is
 (A->(B->C))->((A->B)->(A->C)) and the next one is A->(B->A), then A->(B->C) and A->(B->A)
 are unified with A=C, yielding the result (A->B)->(A->A).

## Lemmas:
You can use the following lemmas if you need.
L01: (A -> B) -> ((C -> A) -> (C -> B))
L02: (A -> (B -> C)) -> (B -> (A -> C))

# Output Format
The proof must ultimately be represented as a combinator expression in Reverse Polish
Notation (RPN). In RPN, A01, A02, A03 each push an instance of the corresponding axiom
onto the stack, L01, L02, ... do the same for lemmas, and MP represents Modus Ponens
according to the above rule. You may include explanations, but enclose the final proof
expression between <final_answer> and </final_answer>.

# Example Problem
Target proposition: A -> A
Reference proof steps:

                                                              11
                     Self-Supervised Theorem Discovery in a Formal Axiomatic System

1. A -> (B -> A) (Axiom A01)
2. A -> (B -> A) (Axiom A01)
3. (A -> (B -> C)) -> ((A -> B) -> (A -> C)) (Axiom A02)
4. (A -> B) -> (A -> A) (Apply MP to 3 and 2)
5. A -> A (Apply MP to 4 and 1)
In this case, the combinator expression in RPN is A01 A01 A02 MP MP. Final output example
is the following:
<final_answer>A01 A01 A02 MP MP</final_answer>

# Problem
Prove the following proposition:
(A -> B) -> ((B -> C) -> (A -> C))




                                                  12
