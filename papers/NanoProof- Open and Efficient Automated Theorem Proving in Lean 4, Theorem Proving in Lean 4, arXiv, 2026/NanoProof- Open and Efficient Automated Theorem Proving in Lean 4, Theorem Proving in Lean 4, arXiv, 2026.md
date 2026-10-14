                                                        NanoProof: Open and Efficient Automated
                                                              Theorem Proving in Lean 4
                                                                                            Matěj Kripner∗        Milan Straka
                                                      Institute of Formal and Applied Linguistics, Faculty of Mathematics and Physics, Charles University
                                                                                           Prague, Czech Republic

                                        Abstract                                                                    On an implementation level, ATP systems can be divided
                                        We introduce NanoProof, to our knowledge the first factor-               along several axes. First, in an execution-guided proof search,
                                        ized execution-guided theorem prover in Lean 4 whose train-              a prover interleaves proof search with verification, leverag-
                                        ing data, extraction tooling, training pipeline, and weights             ing feedback from the formal verifier after each proof step
                                        are all released, making it end-to-end reproducible using                and generating steps conditioned on the true internal proof
arXiv:2610.11605v1 [cs.LG] 8 Oct 2026




                                        open-source resources. To this end, we build and release a               state. For example, in Lean 4, an execution-guided prover ob-
                                        dataset of structured proof trees, as well as a tool for pro-            serves the list of currently open goals and is informed on any
                                        grammatic interaction and data extraction within the Lean 4              proof steps that resulted in an error. In contrast, execution-
                                        formal verifier. To support sustainable research, we focus on            agnostic provers only use the formal verifier to verify the
                                        compute efficiency to facilitate accessible training and eval-           final proof, generating proof steps with no feedback about
                                        uation. NanoProof achieves 50.8% pass@16 on MiniF2F-Test,                the validity of preceding steps or the current internal proof
                                        exceeding the two closest systems of its class, HyperTree                state. Thus, in execution-agnostic search, it falls upon the
                                        Proof Search and ABEL, at roughly 90× and 7× less compute,               proof step generator to deduce the evolving proof state, as
                                        and using more than four orders of magnitude less compute                this is a necessary precondition to determine the validity of
                                        than AlphaProof. Stronger open-weight provers exist, but                 subsequent proof steps. This coupling of a policy model and
                                        they are fine-tuned from large pretrained language models                a world model increases the complexity of proof generation.
                                        and release neither training data nor pipeline; NanoProof                   Second, in a factorized proof search, the prover is allowed
                                        shows that the factorized execution-guided class of provers              to split proof states into separate branches that can be ex-
                                        can be rebuilt from scratch with modest resources.                       plored independently. An illustrative example is mathemat-
                                                                                                                 ical induction, where factorized search considers the base
                                                                                                                 case and the inductive case independently, enabling paral-
                                        1    Introduction                                                        lelization and dynamic allocation of search budget between
                                        In automated theorem proving (ATP), the task at hand con-                the two branches. The utility of node re-use and paralleliza-
                                        sists of generating a valid proof to a mathematical statement.           tion enabled by factorization has been verified by Lample
                                        We focus our attention on formal ATP, where both the state-              et al. [22] and Hubert et al. [14] and we do not reiterate it
                                        ment and the proof are expressed in a formal language such               in this work. In contrast, in a linear proof search, the proof
                                        as Lean 4 [29]. In this setting, the correctness of a generated          state consists of all the context necessary to complete the
                                        proof can be verified automatically, providing clear feedback            proof.
                                        to an ATP system, which can be used for training using                      Finally, in an any-time proof search, the prover perfor-
                                        reinforcement learning (RL).                                             mance grows when time or compute budget is increased,
                                           Formal methods have found applications in the formal-                 while a one-shot prover can only be scaled by running multi-
                                        ization of mathematics [36], physics [34], and chemistry [3],            ple instances in parallel, without the possibility of utilizing
                                        as well as software verification [2], cryptography [8], and              results across searches.
                                        general reasoning [16]. With the current and anticipated                    Proof search can be treated as a generic text-to-text
                                        rise of AI-generated code, proofs, and other artifacts, we               language modeling problem of generating a proof given a
                                        expect human verification to become the bottleneck to in-                statement, resulting in a linear one-shot execution-agnostic
                                        novation, making formal methods essential for their ability              method. Such methods have directly benefited from the
                                        to automatically filter out incorrect solutions. For example,            recent rapid rise in capabilities of large language models
                                        mathematicians already benefit from expediting the review                (LLMs). In contrast, factorized any-time execution-guided
                                        process in frontier research by submitting a formalization               provers require careful pre-processing of training data
                                        of their results [12]. Similarly, formal verification enables            and tight integration with the verification framework. The
                                        massively collaborative mathematical projects without the                existing systems of this class, HyperTree Proof Search [22],
                                        need for extensive human moderation [4].                                 ABEL [11], and AlphaProof [14], released neither their
                                                                                                                 data nor runnable code. Open execution-guided provers
                                                                                                                 such as InternLM2.5-StepProver [40], BFS-Prover [43], and
                                        ∗ Corresponding author: kripner@ufal.mff.cuni.cz.

                                                                                                             1
                                                                                                                     Matěj Kripner and Milan Straka


BFS-Prover-V2 [44] perform linear best-first search over                                run, achieving 50.8% pass@16 on MiniF2F-Test [50] us-
monolithic proof states and release at most model weights.                              ing more than four orders of magnitude less compute
The factorized class has therefore been out of reach for the                            than AlphaProof.
open-source community, both in terms of data availability                             • Search-Level Techniques We describe practical
and compute requirements. We identify this as a major                                   train-time and inference-time techniques, namely
roadblock to advancing Machine Learning-based ATP in the                                proof simplification and augmentation, cycle detec-
age of large models, particularly since recent approaches                               tion, and diverse tactic sampling, and quantify their
like AlphaProof [14] and HyperTree Proof Search [22]                                    effect where our compute budget allowed.
demonstrated the viability of this paradigm.
                                                                                     In Section 3, we present the training pipeline and the
   Since the inception of this work, text-to-text and agen-
                                                                                  search algorithm of NanoProof. In Section 4, we describe the
tic provers built on large language models have become
                                                                                  algorithm for extracting proof trees from human-authored
extremely strong, with Seed-Prover [5] and Goedel-Prover-
                                                                                  Lean projects and the resulting LeanTree dataset, a necessary
V2 [25] saturating MiniF2F. We do not take this as evidence
                                                                                  component for pre-training a factorized execution-guided
that search-based approaches are obsolete. Casting proving
                                                                                  prover. Finally, in Section 5, we present a training run of
as plain text generation means that a frontier LLM can be
                                                                                  NanoProof using openly available datasets and LeanTree.
applied without adaptation, whereas factorized search-based
                                                                                  The necessary background in Lean and proof search is avail-
provers require structured training data, verifier integra-
                                                                                  able in Appendix A.
tion, and search infrastructure before they can run at all,
and until now this machinery existed only inside closed sys-
tems. Whether classical search with small models remains                          2   Related Work
competitive with large generic LLMs at equal compute is                           We give a brief overview of Lean, different ATP approaches,
an open question, and it can only be studied if this class                        and existing formal ATP datasets and benchmarks.
of system exists in an open and reproducible form. More-                             Lean 4 [29] is a leading formal language for theorem
over, the strongest approach may turn out to be a combi-                          proving with applications both in the formalization of math-
nation of the two, LLM reasoning with verifier-grounded                           ematics [36] and in numerous other domains [3, 8, 16, 34].
search, a direction that the heavy use of Lean feedback in                        One of the appealing properties of Lean is its extensibility,
Seed-Prover already explores. Factorized search also offers                       stemming from the fact that its theorem proving component
concrete advantages independent of model size: node re-use                        is written in Lean itself, and the user can modify both its syn-
across branches, independent allocation of search budget to                       tax and its semantics, which we heavily utilize in LeanTree.
subgoals, and distance-to-proof-end labels that directly su-                         Execution-Agnostic ATP. ATP can be formulated as a
pervise the critic. This is why we consider open, reproducible                    text-to-text task so that any existing LLM is directly appli-
tooling for the search-based side worth building.                                 cable. This approach to theorem proving was pioneered by
   In this work, we address this reproducibility barrier by                       Baldur [10]. More recently, LLMs using chain-of-thought
introducing NanoProof, an end-to-end ATP system that lever-                       refined using RL were utilized by DeepSeek-Prover-V2 [32],
ages existing open resources and provides the novel compo-                        Kimina-Prover [38], InternLM-Math [49], Goedel-Prover-
nents necessary to complete the Lean 4 pipeline. Specifically,                    V2 [25], and Seed-Prover [5], among others, securing top
our contributions are as follows.                                                 positions on relevant benchmarks; Goedel-Prover-V2 reports
                                                                                  88.1% on MiniF2F-Test at pass@32 and Seed-Prover 99.6%.
     • Data, Tooling, and Environment We release
                                                                                     Execution-Guided ATP. In execution-guided ATP, a
       LeanTree, a dataset of 92,927 independently verified
                                                                                  prover interacts with the verification system iteratively dur-
       structured proof trees extracted from Mathlib, the
                                                                                  ing the proof search, generating proof steps conditioned on
       extraction tool that produces such trees from any
                                                                                  the internal proof state. In neural theorem proving, this ap-
       Lean 4 project, and a Lean interface with incremental
                                                                                  proach was pioneered by Holophrasm [39] in Metamath [27],
       kernel verification and a distributed environment
                                                                                  using a UCT-based [19] AND-OR tree search with a RNN
       pool for reinforcement learning.
                                                                                  sequence-to-sequence model for tactic enumeration and
     • ATP System We introduce a factorized any-time
                                                                                  payoff prediction. Later extensions include GPT-f [30] and
       execution-guided prover called NanoProof and release
                                                                                  Evariste [22], the latter also targeting Lean 3 in addition to
       all the tooling necessary to reproduce it and build on
                                                                                  Metamath. ABEL [11] extended Evariste with incremental
       top of it.1
                                                                                  improvements and Lean 4 compatibility, but did not release
     • Performance Evaluation We demonstrate the ef-
                                                                                  the code or dataset. AlphaProof [14] then achieved a signifi-
       ficacy of NanoProof through an end-to-end training
                                                                                  cant improvement in performance, unfortunately also with
                                                                                  closed code and data.
1 The Python package and its source code is available at https://github.com          A separate line of open execution-guided provers performs
/kripner/nanoproof.                                                               linear best-first search over monolithic Lean proof states
                                                                              2
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4



                                                                                                RL Loop
       Base Training                 Mid-Training                     Fine-Tuning                            NanoProof
                                                                                                                                   Replay
                                                                                                                                   Buffer


   Nemotron-CC-Math-4+            LEAN-Github (raw)                    LeanTree
         10B tokens                   64M tokens                    287k proof edges
                                                                                                            NuminaMath-LEAN
                                                                                                           97k formal statements
                                                                        Mathlib
                                                                    103k tactic proofs



Figure 1. NanoProof training pipeline. After supervised pretraining, the prover enters into a self-improvement loop where
successfully discovered proofs are used for further training. Mid-training is not included in the final run, as described in
Section 5.

with a policy fine-tuned from a pretrained LLM: InternLM2.5-                    Additionally, Lean-Workbook [48], DeepSeek-Prover-
StepProver [40], BFS-Prover [43] with 72.95% on MiniF2F-                     V1 [42], and NuminaMath-LEAN [38] provide large collec-
Test, BFS-Prover-V2 [44] with 82.4% and 86.1% for its 7B                     tions of automatically formalized proofs of various quality,
and 32B models (95.1% with an additional Gemini 2.5 Pro                      the latter also offering a sizable human-formalized portion.
planner), and MPS-Prover [23] with 75.82%. In the terminol-                     Benchmarks. MiniF2F [50] offers 488 problems drawn
ogy introduced above, these are execution-guided but linear                  from mathematical olympiad and undergraduate mathemat-
provers: none of them factorizes proof states into indepen-                  ics courses, formalized in parallel in Lean 3, Metamath, Is-
dently searchable goals with node re-use and metavariable-                   abelle, and HOL Light. The objective is to generate valid
coupling handling. They release at most weights and infer-                   formal proofs of the statements. The benchmark was later
ence code, and none releases training data or pipeline. Being                ported to Lean 4 by Yang et al. [47], with some formaliza-
fine-tuned from Qwen2.5 [46], their reported budgets ex-                     tion errors corrected by Wu et al. [40]. We use MiniF2F as
clude the pre-training of the base model, on the order of 1012               released by Hubert et al. [14].
TFLOPs, and their undisclosed pre-training corpora cannot
be audited for benchmark contamination. BFS-Prover also
argues that, in its setting of a large pretrained policy and no              3     NanoProof Automated Theorem Prover
learned critic, simple best-first search can outperform MCTS-
style search; whether this carries over to factorized search                 We describe the training and inference mechanism of
with a trained critic is an open question that our release                   NanoProof. Section 3.1 mostly follows Hubert et al. [14],
makes testable.                                                              while the following sections describe our implementation
   Datasets. The standard library of Lean, Mathlib [7], offers               choices and additions; the LeanTree dataset and extraction
more than 124k formal definitions and 255k formal proofs.                    tool that enable the supervised training of such a prover are
Together with numerous formalization projects created by                     described in Section 4.
the community, this offers a sizable human-written dataset
for the supervised training of theorem provers.
   However, execution-guided ATP approaches require addi-                    3.1    Proof Search Algorithm
tional data pre-processing to expose the intermediate proof                  RL Environment. We formulate the proof search process
states. Such a dataset was first provided by LeanStep [13]                   as an RL environment. At episode start, a formal theorem
in Lean 3 by extracting tactic invocation data from Mathlib.                 statement is sampled from a corpus (cf. Section 5). At each
LeanDojo [47] extends this approach to Lean 4, additionally                  step, the prover (agent) observes the current state 𝑠𝑡 consist-
providing information about the premises used in each tactic                 ing of the list of open goals yet to be proven, and generates
application, necessary for training retrieval-augmented ap-                  an action 𝑎𝑡 , i.e., a Lean tactic. The Lean verifier then imple-
proaches. Similar datasets are also offered by Pantograph [1]                ments the transition function from the pair (𝑠𝑡 , 𝑎𝑡 ) to the list
and lean-training-data [28]. However, none of these datasets                 of next states (𝑠𝑡1+1, . . . , 𝑠𝑡𝑛+1 ), potentially empty. Note that
offers tactic proofs in a structured, simplified format, which               this deviates from a simple Markov Decision Process in that
is needed for NanoProof training. Most importantly, they do                  the agent proceeds independently into each next state. Recall
not contain distance-to-proof-end information.                               that for the goals in state 𝑠𝑡 to be proven, it is necessary to
                                                                             prove all goals in states (𝑠𝑡1+1, . . . , 𝑠𝑡𝑛+1 ).
                                                                         3
                                                                                                          Matěj Kripner and Milan Straka


   The episode ends when a valid action has been assigned              3.3   Training Pipeline
to each state, yielding a proof tree. The agent is then as-            As shown in Figure 1, the prover network undergoes
signed a reward 𝑟 = −𝑑, where 𝑑 is the depth of the proof              several supervised training phases before entering a self-
tree. This incentivizes the agent to find short proofs that            improvement loop. This preliminary phase is necessary
maximize branching, utilizing the factorization capability             because the generation of valid and diverse tactics is a
outlined above.                                                        challenging task in itself. The supervised phases use in-
MCTS Search. Our proof search algorithm follows closely                creasingly targeted training data, starting with general
that of AlphaProof, and we leave detailed description to Hu-           math-related text and progressing through Lean source code
bert et al. [14]. The prover consists of an actor predicting           to highly pre-processed human-authored Lean proofs. This
which proof tactic to apply in the current proof state, and a          progression of data quality is mirrored in an increasingly
critic predicting future reward in the current proof branch,           limited quantity.
i.e., the negative depth of the proof sub-tree starting from the          During the self-improvement loop, the prover continu-
current state. The algorithm maintains an AND-OR search                ously samples theorems from an autoformalized corpus and
tree that initially contains only the root node with the theo-         attempts to prove them, storing all successful proofs in a
rem to be proven and is then iteratively expanded by repeat-           replay buffer. Transitions sampled from the replay buffer are
ing three phases: selection, expansion and backpropagation,            then used as further training data for the prover network. In
adapted from AlphaZero [33] and Sampled MuZero [15]. At                addition, a given fraction of supervised fine-tuning data is
node expansion, generated tactics are immediately executed             mixed in with the collected data to increase training stability.
in Lean, and invalid ones are discarded. Compared to sequen-           The system alternates between collecting 𝑛 samples new proof
tial two-player games, the prover agent does not commit to             transitions and performing 𝑛 updates gradient updates.
intermediate actions and only performs a single search for                As shown in Figure 2, the RL loop infrastructure features
each theorem. For this reason, Hubert et al. [14] incorporates         an inference server with simple first-available load balancing,
a progressive sampling mechanism, allowing new tactics to              a distributed trainer and detached Lean servers running on
be sampled for internal nodes.                                         CPU nodes.
Matchmaker. Theorems to be proven are sampled from
a corpus with sampling weights determined by a simple                  3.4   Lean Integration
heuristic matchmaker. After initial trust_count attempts at
each theorem, the matchmaker down-weights theorems that                LeanTree offers a Python interface built on top of Lean
have been proven at least trust_count_proved in a row                  REPL [6]. After initiating a proof search and applying a
and theorems that have never been proved, thus prioritizing            Lean tactic to a given proof state, LeanTree returns a list of
theorems at the edge of the prover’s current ability. Com-             resulting sub-states. The interface is suitable for tree search
pared to Hubert et al. [14], we additionally down-weight               and backtracking as the interaction can be restarted from
theorems for which a single-tactic proof has been found,               any intermediate proof state. Additionally, given the high
since no shorter proof can be discovered.                              CPU requirements of Lean 4, LeanTree implements a dy-
                                                                       namic pool of environments exposed over HTTP endpoint
3.2   Network Architecture                                             for deployment to CPU nodes during distributed training.
                                                                          During our work, we encountered invalid proofs that
The actor and critic are modeled using a single Transformer
                                                                       Lean REPL accepted as valid; the details and a correction
model [37] based on nanochat [17].2 Instead of utilizing ded-
                                                                       are described in Appendix E. Note that all proofs found by
icated actor and critic heads, we adopt the simpler approach
                                                                       NanoProof are independently verified by exporting them as
of shared vocabulary by Polu and Sutskever [30]. Specifi-
                                                                       standalone Lean code.
cally, the model input consists of a tokenized pretty-printed
Lean state followed by a special token indicating whether
what follows is a tactic or a critic value. During inference,          3.5   Proof Simplification and Augmentation
tactics are decoded autoregressively. In contrast, prediction          Proof Simplification. We attempt to simplify the proofs
of the critic value is done with only a single forward pass            produced by the proof search algorithm by pruning redun-
and weighted averaging of the value bins based on predicted            dant tactics. This is done both during experience collection
token probabilities.                                                   to improve the quality of the data saved to the replay buffer
   For tokenization, we use the GPT-2 tokenizer [31]3 ex-              and during final inference to enhance the readability of the
tended with dedicated tokens for symbols that occur at least           generated proofs for humans. In a representative RL run, our
1,000× in Mathlib. The range of allowed critic values is di-           algorithm was able to simplify 59% of proofs longer than one
vided into discrete bins using dedicated tokens [9].                   tactic. An example of a simplified proof recorded during an
                                                                       experience collection phase is shown in Appendix C.
2 https://github.com/karpathy/nanochat, MIT License                       The proof simplification algorithm is outlined in Listing 1.
3 https://huggingface.co/openai-community/gpt2, MIT License            Given a generated proof, the simplification aims to extract
                                                                   4
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4


a minimal sub-proof that still proves the original theorem.               4    Structured Proof Tree Dataset
Starting with a proof tree, we consider each non-leaf edge                To enable supervised pretraining on existing human-written
individually. If contracting an edge leaves the proof valid, the          Lean proofs, factorized execution-guided provers require
edge is removed. For a non-leaf edge 𝑒 = (𝑠𝑡 , 𝑠𝑡 +1 ) with tactic        careful pre-processing of proofs into structured proof trees.
𝑎𝑡 , contraction is implemented by discarding 𝑎𝑡 (together                The challenge is twofold: First, the Lean language under-
with 𝑠𝑡 +1 ), replacing it with any tactic 𝑎𝑡 +1 applied in 𝑠𝑡 +1 .       stands a proof as a linear sequence of tactics, instead of a
    When re-verifying the proof after contraction, it suffices            tree where different branches can be produced independently.
to verify the modified proof sub-tree below 𝑠𝑡 , since other              These tactics can be nested and combined with tactic combi-
branches and tactics on the path to root are not affected. The            nators as well as other syntactic sugar. Second, Lean proofs,
sub-tree is verified by re-executing each tactic application in           as present in human-written repositories, are written in a
it, starting with the application of 𝑎𝑡 +1 . When 𝑎𝑡 produces             compact, refined way to make them easy to read, maintain,
multiple factorized goals, i.e., it has more than one child node,         and build on. However, we seek a different proof style, one
we individually attempt to execute each of the sub-trees, and             that unfolds the proof in a way amenable to search, i.e., in
𝑒 is deemed redundant when at least one execution succeeds.               small incremental steps.
After a node is removed, the whole simplification process is                 To address this challenge, we introduce a proof extrac-
restarted because removing an edge might only be possible                 tion tool and dataset, collectively called LeanTree, whose
after a different edge is removed first.                                  preliminary version was presented in Kripner et al. [21]. In
Proof Augmentation. When sampling a proof from the                        each extracted proof tree, a node carries a single goal,4 and
replay buffer, we apply a random augmentation to each of its              an edge corresponds to a tactic application operating on
proof edges, altering them while preserving their semantics.              that goal. The dataset contains 92,927 extracted proof trees
First, all hypotheses and goals are randomly renamed with                 from a recent version of Mathlib,5 the standard library of
probability 𝑝 rename , applying the rename accordingly also in            human-written proofs in Lean. Details about the structure of
both the tactic and the other hypotheses. Second, the hy-                 the dataset are provided in Appendix H. Importantly, each
potheses in each goal are randomly shuffled with probability              included tree is independently verified by executing it from
𝑝 shuffle .                                                               the root down in topological order. Because of technical
                                                                          challenges outlined in this section, not all tactic proofs can
                                                                          currently be verifiably converted. Specifically, 9.53% of tactic
3.6   Cycle Detection                                                     proofs in Mathlib were not included in LeanTree because
We apply a cycle detection mechanism during node expan-                   the validity of all tactics in the extracted proof trees could
sion. When a tactic application results in a goal 𝐺 that is               not be verified. We are continually working on perfecting
equivalent to a goal 𝐺 ′ already present on the path to root,             this process.
the tactic is discarded. Any final proof containing this tactic              The LeanTree dataset, together with its documentation
could equivalently be found by solving 𝐺 directly instead of              and relevant metadata, is publicly available at https://hugg
descending to 𝐺 ′ . In a representative run, 18% of otherwise             ingface.co/datasets/ufal/leantree. The extraction tool and
valid tactics were rejected due to cycle detection. Note that             the Lean interface are available at https://github.com/kripn
goal equivalence is checked at the syntactic level up to goal             er/leantree.
re-shuffling, goal renaming, and whitespace changes.                      Proof Tree Building. To illustrate the challenges in build-
                                                                          ing a proof tree, Figure 3 shows two example Lean proofs and
                                                                          the resulting trees. For the purposes of illustration, we do not
                                                                          utilize powerful tactics such as linarith, which would solve
3.7   Diverse Tactic Sampling
                                                                          the trivial theorem nearly automatically. Instead, we show-
We observe that the autoregressive tactic sampling often                  case branching, metavariable coupling, and the introduction
produces duplicate tactics, sometimes constraining node ex-               of a new hypothesis.
pansion to just a single action, particularly in the case of                 Other Lean features not shown in Figure 3 that further
short one-token tactics. In a representative run, 32% of nodes            complicate the construction of proof trees include tactic
had their action count reduced due to duplicated sampling.                combinators such as try, iterate, and any_goals, where
We address this by forcing diverse sampling on the first                  the set of affected goals is determined in runtime, constructs
tactic token. Specifically, the first sampling step employs               such as all_goals and <;> that go against tree formulation
the Gumbel-Top-𝑘 trick [20] to cap each possible token to                 due to operating on multiple goals, or tactics such as switch
first_token_cap occurrences. Taking an average over last                  and rotate_left that change the order of open goals.
three saved checkpoints in the same run, this diverse tac-
tic sampling increased performance on MiniF2F-Valid by                    4 Note that, due to metavariable coupling, nodes occasionally contain more
2.0 percentage points under 16 simulations, highlighting its              than one goal, which we detail in Section 4.3.
importance for small compute budgets.                                     5 leanprover/lean4:v4.27.0, Apache-2.0 License

                                                                      5
                                                                                                        Matěj Kripner and Milan Straka



Algorithm 1 Pruning of redundant tactics.                                            DDP                    Replay
  Input: proof tree 𝑃                                                               Trainer                 Buffer
  procedure PruneTactics(𝑃)
                                                                                                         Coordinator
  for any non-leaf 𝑒 = (𝑠𝑡 , 𝑠𝑡 +1 ) with action 𝑎𝑡
    for any 𝑎𝑡 +1 applied in 𝑠𝑡 +1
                                                                                                       Prover Server
       𝑃 ′ ← contract(𝑃, 𝑒, 𝑎𝑡 ← 𝑎𝑡 +1 )                                          Inference
                                                                                    Router                            ...
       if subtree_valid(𝑠𝑡 , 𝑃 ′ )
          return PruneTactics(𝑃 ′ )
                                                                           RL Trainer
       end if
    end for
  end for                                                                     Process Pool               Process Pool

  return 𝑃


                                                                            Lean Server                Lean Server

                                                                           Figure 2. Runtime architecture of RL training.
   We implement the proof extraction in three stages de-               In Listing 1, the exact tactic is parametrized by a term
scribed in the following three subsections. A comparison of          which contains a tactic block introduced using the by key-
LeanTree with existing datasets and tools for training data          word. We break down this complex proof step by masking
extraction in Lean is given in Appendix G.                           the nested tactic block and instead spawning a child goal,
                                                                     yielding the following series of simpler proof steps.
4.1   Singleton Tree Construction
The first stage of proof tree building transforms a Lean proof        exact ⟨by sorry, rfl⟩
into a singleton tree, where each node contains a single goal,        rw [aeval_algHom_apply]
by matching tactic applications with the goals they affect. In                                                                     (2)
                                                                      rw [hw]
general, a tactic application transforms a list of open goals         rw [map_zero]
into an entirely new list of open goals without any addi-
tional guarantees, making this transformation nontrivial.               Note that the rfl tactic is not masked since it is used as a
To build singleton trees, we integrate Lean REPL with an             term instead of a tactic.
augmented version of the BetterParser module of Paper-                  calc Blocks. The calc tactic combines a sequence of
Proof [18],6 which solves an analogous problem, although             relational proofs into a single transitive derivation. We de-
originally developed for visualization purposes.                     compose such a block into one have tactic per step, followed
                                                                     by a final exact tactic that combines the intermediate lem-
4.2   Tactic Simplification
                                                                     mas. An example is shown in Figure 3.
Singleton trees are modified so that complex tactics are bro-           Structuring Tactics. The cases and induction tactics
ken down into simpler ones, and each tactic is a valid self-         introduce syntactic branching by partitioning a proof based
contained proof step. We now describe some of these modi-            on the value of an inductive type. The tactic optionally con-
fications.                                                           tains a solving branch for each of the constructors of such a
   Nested Tactics. Tactics parametrized by a term can them-          type. We move the individual proof branches from the cases
selves contain nested tactic blocks. For example, consider           or induction tactic into their separate proof steps. For ex-
the following tactic from the Complex Analysis module in             ample, consider the cases tactic in Figure 3, which spans
Mathlib.                                                             10 lines and should not be presented to a policy model as a
  exact ⟨by                                                          training sample.
   rw [aeval_algHom_apply, hw, map_zero],                  (1)          Merged rw Tactics. In Lean, subsequent rw tactics can
   rfl⟩                                                              be merged into a single tactic, which is commonplace in
                                                                     human-written proofs. We partition such composite tactics
6 https://github.com/Paper-Proof/paperproof, MIT License             into individual rw tactics.
                                                                 6
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4



      Mathlib
                                                                                    open Nat
      import Mathlib.Algebra.Group.Basic
      import Mathlib.Algebra.Order.Monoid.Unbundled.Basic                           theorem succ_less_double_succ (n : Nat) :
      import Mathlib.Order.Lattice                                                      n > 0 → n < 2 * n := by
                                                                                      intro h
      variable {α : Type*}                                                            cases n with
      variable [PartialOrder α] [AddCommSemigroup α] {a b c d : α}                    | zero => apply h
      variable [AddLeftReflectLE α]                                                   | succ n' =>
                                                                                        apply le_trans
      theorem tsub_eq_tsub_of_add_eq_add (h : a + d = c + b) :                          case m => exact n' + 2
          a - b = c - d := by                                                           · rfl
        calc a - b = a + d - d - b := by rw [add_tsub_cancel_right]                     · rw [two_mul, add_succ]
                 _ = c + b - b - d := by rw [h, tsub_right_comm]                          have h1 : 1 ≤ n' + 1
                 _ = c - d := by rw [add_tsub_cancel_right]                               · apply succ_le_succ (zero_le _)
                                                                                          · exact add_le_add_left h1 (n' + 1)

                                                    Factorize proof states.
                                                    Simplify
                                                         nested tactics,
                                                         structuring tactics,
                                                         calc blocks,

      LeanTree
                                                                                                      ⊢ n > 0 → n < 2 * n
                                                         composite rw tactics,
                                                         ...                                                   ···
                                                    Merge metavariable-dependent goals.
                                                                                                             cases n

                                                                                     h : 0 > 0      h : n✝ + 1 > 0
                                                                                     ⊢ 0 < 2 * 0    ⊢ n✝ + 1 < 2 * (n✝ + 1)
                               h : a + d = c + b
                               ⊢ a - b = c - d
                                                                                                         case succ n'
                                                                                          apply h
                       have h1 : a - b = a + d - d - b
                                                                                                    h : n' + 1 > 0
                                                                                                    ⊢ n' + 1 < 2 * (n' + 1)
                   h h1                 h
                   ⊢ a - b = c - d      ⊢ a - b = a + d - d - b
                                                                                                      apply Nat.le_trans

                                       rw [add_tsub_cancel_right]                                    h : n' + 1 > 0
                                                                                                     ⊢ (n' + 1).succ ≤ ?m
             have h2 : a + d - d - b                                                                 ⊢ ?m ≤ 2 * (n' + 1)
                     = c + b - b - d                                                                 ⊢ ℕ

                                                                                                    case m => exact n' + 2
                   h h1 h2              h h1
                   ⊢ a - b = c - d      ⊢ a - b = a + d - d - b
                                                                                             ···    h : n' + 1 > 0
                         ···            rw [h, tsub_right_comm]
                                                                                                    ⊢ n' + 2 ≤ 2 * (n' + 1)
                                                                                             rfl
             exact Trans.trans h1                                                                              ···
                    (Trans.trans h2 h3)                                                              have h1 : 1 ≤ n' + 1

                                                                                                       ···              ···


Figure 3. LeanTree extracts Lean proofs from a Lean file (top) and transforms them into structured proof trees (bottom).
Synthetic tactics in the proof tree are marked using dashed border.

4.3    Merging Metavariable-Dependent Goals                               tree building process. Proof trees that fail this verification
To obtain the final proof tree, sibling nodes in a singleton              are not included in the final dataset.
tree are merged if they share a metavariable. This corre-                    In Figure 3, observe that applying Nat.le_trans yields
sponds to the fact that metavariable-dependent goals cannot               three goals that are not split due to a shared metavariable
be explored independently.                                                ?m. However, once the metavariable is assigned using exact,
   During this merging process, the entire proof tree is ex-              the remaining two goals are now independent and can be
ecuted starting from the root state and following each tree               split.
edge, verifying that each proof branch ends in a proven state.
In this way, we ensure the correctness of the whole proof
                                                                      7
                                                                                                                                            Matěj Kripner and Milan Straka


                                                                                                     100                                          AlphaProof (TTRL)
                    52                                         51.3%
                                                               (nsim = 256)                                                                 DeepSeek-Prover-V2
                    50                                         49.9%
                                                               (nsim = 128)                          80
                    48
MiniF2F-Valid (%)



                                                                                                                                        BFS-Prover




                                                                                  MiniF2F-Test (%)
                                                               47.0%
                                                               (nsim = 32)
                    46                                                                               60
                    44                                         42.4%
                                                                                                             NanoProof

                    42                                         (nsim = 8)                            40
                                                                                                                        ABEL         HTPS

                    40
                    38                                                                               20
                                                                                                                     ReProver

                    36                                                                                                               Closed-Source
                                                                                                                                     Factorized Any-Time Execution-Guided
                    34
                         0   20   40          60   80       100                                       0
                                                                                                               109         1010        1011      1012          1013
                                       Step                                                                                       Compute (TFLOPs)


 Figure 4. Prover performance throughout RL training.                             Figure 5. FLOPs vs performance comparison. We show
 We show how NanoProof success rate on MiniF2F scales with                        ATP success rate on MiniF2F-Test relative to approximate
 RL training time and number of simulations 𝑛 sim . Averaged                      total compute requirements. FLOPs are converted by us from
 over three independent runs with min/max bands.                                  reported hardware usage, or estimated where it is not dis-
                                                                                  closed (Appendix F).
  5                 Experiments                                                        dataset [38].8 Note that the dataset contains additional 5,529
 We present an end-to-end training run of NanoProof. The                               theorems which are incompatible with Lean v4.27.
 prover policy and critic network is first trained in a super-                            The RL training was run distributed over a node with
 vised fashion before entering into a self-improvement loop as                         eight GPUs and two CPU nodes, with the total hardware
 described in Section 3.3. We describe both of these phases be-                        requirements detailed in Appendix F (excluding preliminary
 low, with key hyperparameters listed in Appendix B. Hyper-                            experiments).
 parameters were chosen manually after several experiments
                                                                                       5.1                 Results
 on MiniF2F-Valid, leaving MiniF2F-Test for final evaluation.
    Supervised Training. First, we base train the network                             Figure 4 shows the progression of NanoProof success rate on
 on the first 10B tokens of the Nemotron-CC-Math-4+                                   MiniF2F during RL training for different numbers of MCTS
 dataset [26],7 containing math and code related text. Then,                          iterations, starting with the checkpoint after supervised train-
 we fine-tune the network on the 287k pre-processed proof                             ing. We perform three independent runs of RL training and
 steps from Mathlib [7] contained in LeanTree, leaving the                            report the mean score with min/max bands. The runs are
 last 10% of files (amounting to 29k proof steps) for validation                      independent in terms of both the theorems sampled by the
 and training on the remaining 258k. Each proof step con-                             matchmaker and the tactics sampled during node expansion.
 sists of a proof state, tactic, and distance to proof end, i.e.,                        After 100 steps of RL training, or 45 hours, NanoProof
 the corresponding sub-proof depth. The data used during                              achieves a mean performance of 51.3% on MiniF2F-Valid
 fine-tuning necessitate careful pre-processing described in                          over 3 runs (min: 51.2%, max: 51.6%) under the budget of 256
 Section 4.                                                                           MCTS iterations. A final checkpoint, selected from the three
    We additionally experimented with inserting a mid-train                           using validation split performance, achieves 50.8% pass@16
 phase between base training and fine-tuning, consisting of                           on MiniF2F-Test under 512 iterations.
 additional training on 64M tokens of Lean code scraped from                             Our MiniF2F-Test score is contextualized in terms of the
 GitHub repositories listed in the LEAN-Github dataset [41].                          total compute budget in Figure 5 relative to selected exist-
 However, we did not observe performance improvements                                 ing provers. Among the systems of the factorized any-time
 and did not include mid-training in the final evaluations.                           execution-guided class, NanoProof reaches a higher MiniF2F-
    Reinforcement Learning Loop. During RL training,                                  Test score than HyperTree Proof Search and ABEL at roughly
 we sample theorems from a corpus of 96,967 autofor-                                  90× and 7× less compute, and it is, to our knowledge, the
 malized statements provided by the NuminaMath-LEAN                                   only member of this class whose data, tooling, pipeline, and
                                                                                      weights are all released. Open-weight linear provers such
                                                                                      as BFS-Prover report higher scores, but they start from a
                                                                                      pretrained base model whose pre-training alone costs about
  7 https://huggingface.co/datasets/nvidia/Nemotron-CC-Math-v1, NVIDIA                 8 https://huggingface.co/datasets/AI-MO/NuminaMath-LEAN, Apache-2.0

  Open Data License                                                                    License
                                                                              8
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4


three orders of magnitude more than our entire pipeline and             Republic through the e-INFRA CZ (grant ID: 90254). This
cannot be reproduced; NanoProof instead reaches its score               work was supported by the Ministry of Education, Youth
training from scratch, within a budget that any research                and Sports of the Czech Republic through the e-INFRA CZ
group can rerun and modify. The comparison is necessar-                 (ID:90254).
ily heterogeneous in Lean versions, pass@𝑘 protocols, and
search budgets, with compute figures converted by us from               References
reported hardware usage, or estimated where it is not dis-               [1] Leni Aniva, Chuyue Sun, Brando Miranda, Clark Barrett, and Sanmi
closed (Appendix F).                                                         Koyejo. 2024. Pantograph: A Machine-to-Machine Interaction Inter-
                                                                             face for Advanced Theorem Proving, High Level Reasoning, and Data
                                                                             Extraction in Lean 4. arXiv preprint arXiv:2410.16429 (2024).
6    Conclusion                                                          [2] Jeremy Avigad, Lior Goldberg, David Levit, Yoav Seginer, and Alon
In this work, we identified and resolved a major roadblock in                Titelman. 2025. A Proof-Producing Compiler for Blockchain Ap-
the open research of a class of automated theorem provers                    plications. J. Autom. Reason. 69, 2 (April 2025), 25 pages. https:
inspired by approaches such as AlphaProof and HyperTree                      //doi.org/10.1007/s10817-025-09723-y
                                                                         [3] Maxwell P Bobbin, Samiha Sharlin, Parivash Feyzishendi, An Hong
Proof Search. Furthermore, NanoProof, our end-to-end ATP                     Dang, Catherine M Wraback, and Tyler R Josephson. 2024. Formalizing
system, reaches a higher MiniF2F-Test score than the previ-                  chemical physics using the Lean theorem prover. Digital Discovery 3,
ous systems of its class at a fraction of their compute, and is              2 (2024), 264–280.
the only one that can be rebuilt from the released artifacts.            [4] Matthew Bolan, Joachim Breitner, Jose Brox, Nicholas Carlini, Mario
Along the way, we showcased a synthesis of available public                  Carneiro, Floris van Doorn, Martin Dvorak, Andrés Goens, Aaron
                                                                             Hill, Harald Husum, Hernán Ibarra Mejia, Zoltan A. Kocsis, Bruno Le
datasets and filled in the missing pieces where necessary,                   Floch, Amir Livne Bar-on, Lorenzo Luccioli, Douglas McNeil, Alex
particularly with the introduction of LeanTree, a dataset of                 Meiburg, Pietro Monticone, Pace P. Nielsen, Emmanuel Osalotioman
structured proof trees extracted from Mathlib, and a tool                    Osazuwa, Giovanni Paolini, Marco Petracci, Bernhard Reinke, David
for efficient distributed interaction with Lean. We release all              Renshaw, Marcus Rossel, Cody Roux, Jérémy Scanvic, Shreyas Srini-
resulting artifacts as open-source.                                          vas, Anand Rao Tadipatri, Terence Tao, Vlad Tsyrklevich, Fernando
                                                                             Vaquerizo-Villar, Daniel Weber, and Fan Zheng. 2025. The Equational
   Limitations. We do not at this time possess enough com-                   Theories Project: Advancing Collaborative Mathematical Research at
puting resources to fully utilize the presented pipeline, lead-              Scale. arXiv:2512.07087 [math.RA] https://arxiv.org/abs/2512.07087
ing to quantitative results that are sub-par compared to Al-             [5] Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng
phaProof and the open-weight provers of Section 2, and to                    Jiang, Allan Jie, Xiaoran Jin, Xing Jin, Chenggang Li, Kaijing Ma,
the absence of proper ablations: only diverse tactic sampling                et al. 2025. Seed-Prover: Deep and Broad Reasoning for Automated
                                                                             Theorem Proving. arXiv preprint arXiv:2507.23726 (2025).
is ablated, while the other search-level techniques are re-              [6] Lean Community. 2025. Lean 4 REPL. https://github.com/leanprover-
ported through descriptive statistics only. We do not claim                  community/repl. Accessed: 2025-04-28.
methodological novelty in the search algorithm, which fol-               [7] Mathlib Community. 2020. The lean mathematical library. In Pro-
lows AlphaProof; our contribution lies in the data, tooling,                 ceedings of the 9th ACM SIGPLAN International Conference on Cer-
and pipeline that make this class of prover reproducible. The                tified Programs and Proofs (New Orleans, LA, USA) (CPP 2020). As-
                                                                             sociation for Computing Machinery, New York, NY, USA, 367–381.
cross-system comparison is heterogeneous in Lean versions,                   https://doi.org/10.1145/3372885.3373824
pass@𝑘 protocols, and search budgets, and the compute                    [8] Gérald Doussot. 2024. Cryptography Experiments In Lean 4: SHA-3
figures are converted from reported hardware usage or es-                    Implementation. Cryptology ePrint Archive, Paper 2024/1880. https:
timated where undisclosed. NanoProof does not reach the                      //eprint.iacr.org/2024/1880
level necessary for IMO or PutnamBench [35] problems, and                [9] Jesse Farebrother, Jordi Orbay, Quan Vuong, Adrien Ali Taïga, Yevgen
                                                                             Chebotar, Ted Xiao, Alex Irpan, Sergey Levine, Pablo Samuel Castro,
only MiniF2F is included in the evaluation. Finally, 9.53% of                Aleksandra Faust, Aviral Kumar, and Rishabh Agarwal. 2024. Stop
Mathlib proofs are not yet available in a structured format                  Regressing: Training Value Functions via Classification for Scalable
in LeanTree.                                                                 Deep RL. arXiv:2403.03950 [cs.LG] https://arxiv.org/abs/2403.03950
                                                                        [10] Emily First, Markus N Rabe, Talia Ringer, and Yuriy Brun. 2023. Bal-
                                                                             dur: Whole-proof generation and repair with large language models.
Acknowledgments                                                              In Proceedings of the 31st ACM Joint European Software Engineering
This project was supported by the Charles University                         Conference and Symposium on the Foundations of Software Engineering.
Grant Agency (GAUK), project no. 458326 and by the grant                     1229–1241.
                                                                        [11] Fabian Gloeckle, Jannis Limperg, Gabriel Synnaeve, and Amaury
no. 25-18031S of the Czech Science Foundation (GAČR). This                   Hayat. 2024. ABEL: Sample efficient online reinforcement learning
research was partially supported by SVV project number                       for neural theorem proving. In The 4th Workshop on Mathematical
260 821. We acknowledge VSB – Technical University of                        Reasoning and AI at NeurIPS’24.
Ostrava, IT4Innovations National Supercomputing Center,                 [12] Thomas Hales. 2024. The Formal Proof of the Kepler Conjecture: a
Czech Republic, for awarding this project access to the LUMI                 critical retrospective. arXiv:2402.08032 [math.MG] https://arxiv.org/
                                                                             abs/2402.08032
supercomputer, owned by the EuroHPC Joint Undertaking,                  [13] Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W Ayers, and
hosted by CSC (Finland) and the LUMI consortium through                      Stanislas Polu. 2021. Proof artifact co-training for theorem proving
the Ministry of Education, Youth and Sports of the Czech                     with language models. arXiv preprint arXiv:2102.06203 (2021).
                                                                    9
                                                                                                                               Matěj Kripner and Milan Straka


[14] Thomas Hubert, Rishi Mehta, Laurent Sartran, Miklós Z Horváth,                        Learners. (2019).
     Goran Žužić, Eric Wieser, Aja Huang, Julian Schrittwieser, Yannick               [32] ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang,
     Schroecker, Hussain Masoom, et al. 2025. Olympiad-level formal                        Wanjia Zhao, Liyue Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, et al. 2025.
     mathematical reasoning with reinforcement learning. Nature (2025),                    DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via
     1–3.                                                                                  Reinforcement Learning for Subgoal Decomposition. arXiv preprint
[15] Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Moham-                       arXiv:2504.21801 (2025).
     madamin Barekatain, Simon Schmitt, and David Silver. 2021. Learning              [33] David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis
     and planning in complex action spaces. In International Conference on                 Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot, Laurent
     Machine Learning. PMLR, 4476–4486.                                                    Sifre, Dharshan Kumaran, Thore Graepel, et al. 2018. A general
[16] Dongwei Jiang, Marcio Fonseca, and Shay B. Cohen. 2024. Lean-                         reinforcement learning algorithm that masters chess, shogi, and Go
     Reasoner: Boosting Complex Logical Reasoning with Lean. North                         through self-play. Science 362, 6419 (2018), 1140–1144.
     American Chapter of the Association for Computational Linguistics                [34] Joseph Tooby-Smith. 2024. Formalization of physics index notation in
     (2024). https://doi.org/10.48550/arxiv.2403.13312                                     Lean 4. ArXiv abs/2411.07667 (2024). https://api.semanticscholar.org/
[17] Andrej Karpathy. 2025. nanochat: The best ChatGPT that $100 can                       CorpusID:273970152
     buy. https://github.com/karpathy/nanochat                                        [35] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle
[18] Evgenia Karunus and Anton Kovsharov. 2024. Paperproof: A new proof                    Ding, Michael Jennings, Amitayush Thakur, and Swarat Chaudhuri.
     interface for Lean 4. https://github.com/Paper-Proof/paperproof                       2024. Putnambench: Evaluating neural theorem-provers on the
     Accessed: 2025-04-30.                                                                 putnam mathematical competition. arXiv preprint arXiv:2407.11214
[19] Levente Kocsis and Csaba Szepesvári. 2006. Bandit based monte-                        (2024).
     carlo planning. In European conference on machine learning. Springer,            [36] Floris van Doorn, Patrick Massot, and Oliver Nash. 2023. Formalising
     282–293.                                                                              the h-Principle and Sphere Eversion. In Proceedings of the 12th ACM
[20] Wouter Kool, Herke Van Hoof, and Max Welling. 2019. Stochastic                        SIGPLAN International Conference on Certified Programs and Proofs
     beams and where to find them: The gumbel-top-k trick for sampling                     (Boston, MA, USA) (CPP 2023). Association for Computing Machinery,
     sequences without replacement. In International conference on machine                 New York, NY, USA, 121–134. https://doi.org/10.1145/3573105.3575
     learning. PMLR, 3499–3508.                                                            688
[21] Matěj Kripner, Michal Šustr, and Milan Straka. 2025. LeanTree: Accel-            [37] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion
     erating White-Box Proof Search with Factorized States in Lean 4. In                   Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017.
     The 2nd AI for Math Workshop at ICML 2025. arXiv:2507.14722.                          Attention is all you need. Advances in neural information processing
[22] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien                      systems 30 (2017).
     Rodriguez, Amaury Hayat, Thibaut Lavril, Gabriel Ebner, and Xavier               [38] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi
     Martinet. 2022. Hypertree proof search for neural theorem proving.                    Liu, Marco Dos Santos, Flood Sung, Marina Vinyes, Zhenzhe Ying,
     Advances in neural information processing systems 35 (2022), 26337–                   Zekai Zhu, et al. 2025. Kimina-Prover Preview: Towards large for-
     26349.                                                                                mal reasoning models with reinforcement learning. arXiv preprint
[23] Zhenwen Liang, Linfeng Song, Yang Li, Tao Yang, Feng Zhang, Haitao                    arXiv:2504.11354 (2025).
     Mi, and Dong Yu. 2025. MPS-Prover: Advancing Stepwise Theorem                    [39] Daniel Whalen. 2016. Holophrasm: a neural automated theorem prover
     Proving by Multi-Perspective Search and Data Curation. In Advances                    for higher-order logic. arXiv preprint arXiv:1608.02644 (2016).
     in Neural Information Processing Systems.                                        [40] Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang,
[24] Jannis Limperg and Asta Halkjær From. 2023. Aesop: White-Box Best-                    Dahua Lin, and Kai Chen. 2024. Internlm2. 5-stepprover: Advancing
     First Proof Search for Lean. In Proceedings of the 12th ACM SIGPLAN                   automated theorem proving via expert iteration on large-scale lean
     International Conference on Certified Programs and Proofs (Boston, MA,                problems. arXiv preprint arXiv:2410.15700 (2024).
     USA) (CPP 2023). Association for Computing Machinery, New York,                  [41] Zijian Wu, Jiayu Wang, Dahua Lin, and Kai Chen. 2024. Lean-github:
     NY, USA, 253–266. https://doi.org/10.1145/3573105.3575671                             Compiling github lean repositories for a versatile lean prover. arXiv
[25] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu                    preprint arXiv:2407.17227 (2024).
     Zhao, Lai Jiang, Yihan Geng, Jiawei Ge, Jingruo Sun, et al. 2025. Goedel-        [42] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo
     Prover-V2: Scaling Formal Theorem Proving with Scaffolded Data                        Liu, Chong Ruan, Wenda Li, and Xiaodan Liang. 2024. Deepseek-
     Synthesis and Self-Correction. arXiv preprint arXiv:2508.03613 (2025).                prover: Advancing theorem proving in llms through large-scale syn-
[26] Rabeeh Karimi Mahabadi, Sanjeev Satheesh, Shrimai Prabhumoye,                         thetic data. arXiv preprint arXiv:2405.14333 (2024).
     Mostofa Patwary, Mohammad Shoeybi, and Bryan Catanzaro. 2025.                    [43] Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao,
     Nemotron-cc-math: A 133 billion-token-scale high quality math pre-                    Yifan Sun, Shen Zheng, and Ming Ding. 2025. BFS-Prover: Scalable
     training dataset. arXiv preprint arXiv:2508.15096 (2025).                             Best-First Tree Search for LLM-based Automatic Theorem Proving. In
[27] Norman Megill and David A Wheeler. 2019. Metamath: a computer                         Proceedings of the 63rd Annual Meeting of the Association for Computa-
     language for mathematical proofs. Lulu. com.                                          tional Linguistics (Volume 1: Long Papers).
[28] Kim Morrison. 2023.        lean-training-data: Tools for extracting              [44] Ran Xin, Zeyu Zheng, Yanchen Nie, Kun Yuan, and Xia Xiao. 2025.
     training-data from Lean libraries. https://github.com/kim-em/lean-                    Scaling up Multi-Turn Off-Policy RL and Multi-Agent Tree Search for
     training-data. Accessed: 2025-07-01.                                                  LLM Step-Provers. arXiv preprint arXiv:2509.06493 (2025).
[29] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 theorem                [45] Linting Xue, Aditya Barua, Noah Constant, Rami Al-Rfou, Sharan
     prover and programming language. In Automated Deduction–CADE 28:                      Narang, Mihir Kale, Adam Roberts, and Colin Raffel. 2022. ByT5:
     28th International Conference on Automated Deduction, Virtual Event,                  Towards a token-free future with pre-trained byte-to-byte models.
     July 12–15, 2021, Proceedings 28. Springer, 625–635.                                  arXiv:2105.13626 [cs.CL] https://arxiv.org/abs/2105.13626
[30] Stanislas Polu and Ilya Sutskever. 2020. Generative language model-              [46] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng,
     ing for automated theorem proving. arXiv preprint arXiv:2009.03393                    Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei,
     (2020).                                                                               et al. 2024. Qwen2.5 Technical Report. arXiv preprint arXiv:2412.15115
[31] Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei, and                     (2024).
     Ilya Sutskever. 2019. Language Models are Unsupervised Multitask

                                                                                 10
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4


[47] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song,
     Shixing Yu, Saad Godil, Ryan J Prenger, and Animashree Anandkumar.
     2023. LeanDojo: Theorem proving with retrieval-augmented language
     models. Advances in Neural Information Processing Systems 36 (2023),
     21573–21612.
[48] Huaiyuan Ying, Zijian Wu, Yihan Geng, Jiayu Wang, Dahua Lin, and
     Kai Chen. 2024. Lean workbook: A large-scale lean problem set
     formalized from natural language math problems. arXiv preprint
     arXiv:2406.03847 (2024).
[49] Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou, Yunfan Shao,
     Zhaoye Fei, Yichuan Ma, Jiawei Hong, Kuikun Liu, Ziyi Wang, et al.
     2024. Internlm-math: Open math large language models toward veri-
     fiable reasoning. arXiv preprint arXiv:2402.06332 (2024).
[50] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. 2021. Minif2f:
     a cross-system benchmark for formal olympiad-level mathematics.
     arXiv preprint arXiv:2109.00110 (2021).




                                                                            11
                                                                                                                   Matěj Kripner and Milan Straka


A    Preliminaries: Lean and Proof Search                                  To complete the proof, all four goals must be closed. In
In Lean, theorem statements correspond to types and proofs              a non-factorized setting, the proof state consisting of four
correspond to values. Theorem proving then amounts to                   goals is assessed by the policy and critic models as a whole.
producing a term whose type is equal to the theorem type.               Since tactics typically affect only the main goal, the last goal
For example, consider the following theorem:                            can only be worked on once all others have been closed.
                                                                        In contrast, factorized states allow the search algorithm to
 theorem sub_zero (a b : N) (h : b = 0)                                 focus on the goals individually, in any order the algorithm
                                                            (3)
   : a - b = a                                                          deems fit.
                                                                           AND-OR Search. The search of factorized states naturally
   Proving Theorem 3 consists in supplying a term of type a -           yields an AND-OR tree, where a prover selects a tactic in an
b = a using the available free variables a, b of type N and h of        OR node and subsequently has to prove all the goals in an
type b = 0. While such a term can be written down explicitly,           AND node. Figure 6 shows an example in which choosing
it is common to utilize Lean’s tactic mode to structure the             either the rw tactic or the cases tactic in the root leads to a
proof in a format more aligned with human-written proofs.               proof. For a more in-depth introduction to proof search in
   Upon entering tactic mode using the by keyword, Lean                 Lean, refer to [24].
creates a metavariable with the desired type a - b = a and              Metavariable Coupling. It is not always possible to fully
no value assigned yet. Metavariables can be thought of as               factorize the proof state into individual goals that can be
holes in a proof that have to be filled in before the proof is          proven independently. For this reason, nodes in the proof
considered finished. This gives us an intermediate state in the         tree are allowed to contain more than one goal. Specifically,
proof construction, where the proof term is type-correct but            this occurs when two goals share the same metavariable –
still contains holes to be filled in later. The still unassigned        for example, applying the transitivity lemma Nat.le_trans
metavariables are called open goals, so each goal has a target          to the goal 2 ≤ 5 produces goals 2 ≤ ?m and ?m ≤ 5 sharing
type and a set of available free variables called hypotheses.           a metavariable ?m whose value has not yet been decided.9
Because goals are metavariables, the two terms are often                Subsequently, choosing a value for ?m in one of the goals
used interchangeably.                                                   affects the provability of the other goal, and therefore the two
   We then proceed by applying a tactic to the list of open             goals cannot be explored independently. For a more in-depth
goals. A tactic is a procedure that assigns values to one or            explanation of this phenomenon, we recommend Aniva et al.
more open goals, with each of the values possibly containing            [1].
new unassigned metavariables. In this way, a tactic invoca-
tion transforms the list of open goals into a new list of open
goals. Typically, a tactic only affects the main goal (defined
to be the first goal), either solving it or reducing it to one          B     Hyperparameter Overview
or more simpler sub-goals. The proof is finished once there             We give an overview of the most notable hyperparameters
are no more open goals, i.e., every metavariable has been               used during training and search in Table 1.
assigned.
Proof State Factorization. We follow Lample et al. [22] in
factorizing proof states into independent goals, which can be
explored and proven individually. Note that we temporarily              C     Proof Simplification
disregard metavariable coupling, which is addressed later in            We provide an example of a proof found during the RL train-
this section.                                                           ing loop in Listing 5 and its simplified version in Listing 6.
   An example of potential state reuse is shown in Figure 6,            The latter was produced by the simplification algorithm de-
where the same node is reached using two different search               scribed in Section 3.5. Only the simplified version is saved
paths.                                                                  to the replay buffer during training.
 theorem mul_eq_zero_iff (n m : N)
                                                            (4)
   : n * m = 0 ↔ n = 0 ∨ m = 0

  A possible strategy to prove Theorem 4 is to branch out
based on the values of 𝑛 and 𝑚. We achieve this by executing
the tactic cases n <;> cases m. Since each of the two
numbers can be either zero or a successor of another number,
the resulting proof state consists of four goals. For example,
one of the states is (𝑛 ′ + 1) · 0 = 0 ↔ 𝑛 ′ + 1 = 0 ∨ 0 = 0,
corresponding to the case where 𝑛 is a successor and 𝑚 is
zero.                                                                   9 A third goal of type N is created for technical reasons.

                                                                   12
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4


                             OR                   AND                      OR                  AND
                                                   rw [h]                 ⊢ a-0=a          rw [Nat.sub_zero]
                         h:b=0
                        ⊢ a-b=a                                           ⊢ a-0=a          rw [Nat.sub_zero]
                                                  cases b
                                                                    h : b’ + 1 = 0
                                                                    ⊢ a - (b’ + 1) = a       contradiction



Figure 6. Example of an AND-OR proof tree for Theorem 3. Nodes connected with a dashed line could potentially be merged
and correspond to transpositions in games. This is possible thanks to factorization.

                                 Table 1. Architectural, optimization and search hyperparameters.

                        Category              Hyperparameter                                     Value
                                       Total Parameters                                            1B
                                       Number of Blocks                                             26
                                       𝑑𝑚𝑜𝑑𝑒𝑙                                                     1664
                                       Attention Heads                                              13
                        Prover Network
                                       Feed Forward Widening Factor                                  4
                                       Vocabulary Size                                           50,441
                                       RoPE Base (𝜃 )                                           100,000
                                       Value Bins                                            {1, 2, . . . , 64}
                                              Sequence Length                                       768
                                              Global Batch Size                                  491,520
                                              AdamW Betas                                       (0.8, 0.95)
                                              AdamW Epsilon                                     1 × 10−10
                        Pre-Training          Muon Momentum                                       √︁0.97
                                              LR (embedding)                              0.3 · 1/ √︁𝑑𝑚𝑜𝑑𝑒𝑙 /768
                                              LR (unembedding)                           0.008 · 1/ 𝑑𝑚𝑜𝑑𝑒𝑙 /768
                                              LR (matrices)                                        0.02
                                              LR Warmdown                                        last 65%
                        Fine-Tuning           Value Weight                                         0.01
                                             Replay Buffer Max. Size                        250k transitions
                                             Supervised Data Fraction                             10%
                                             Transitions per Step (𝑛 samples )                    100
                        RL Training
                                             Examples per Update Step                             256
                                             Updates per Step (𝑛 updates )                         2
                                             𝑛 sim during Experience Collection                    64
                                              Maximum Tactic Length                            24 tokens
                                              Sampled Tactics                                       6
                                              Progressive Sampling 𝐶                               0.1
                                              Progressive Sampling 𝛼                               0.6
                                              UCB value discount 𝛽                                0.98
                        Proof Search
                                              UCB prior temperature 𝜏                             200
                                              UCB exploration constant 𝑐𝑖𝑛𝑖𝑡                     0.001
                                              UCB exploration constant 𝑐𝑏𝑎𝑠𝑒                      200
                                              UCB AND-node prior multiplier 𝑐 𝐴𝑁 𝐷                 64
                                              UCB unvisited children value penalty                 16



                                                                     13
                                                                                                             Matěj Kripner and Milan Straka


                                                                   E     Incremental Proof Verification
                                                                   Originally, the Lean REPL did not utilize the Lean verifica-
 theorem                                                           tion kernel to type-check assignments introduced by tactic
     algebra_2complexrootspoly_xsqp49eqxp7itxpn7i                  applications, leading to incorrect proofs being accepted in
     (x : C) :                                                     some cases. Our prover managed to exploit these inconsis-
     x ^ 2 + 49 = (x + 7 * Complex.I) * (x + -7 *                  tencies, finding 12 incorrect proofs in the MiniF2F validation
      Complex.I) := by                                             set that passed verification in the REPL when using the tactic
   subst_vars                                                      mode. One of these incorrect proofs is listed below.
   rw [← sub_eq_zero]                                                  theorem mathd_algebra_422 (x : R) (𝜎 : Equiv R R)
   rw [← sub_eq_zero]                                                      (h0 : ∀ x, 𝜎.1 x = 5 * x - 12)
   simp                                                                    (h1 : 𝜎.1 (x + 1) = 𝜎.2 x) : x = 47 / 24 := by
   simp only [Real.cos_sq, Real.sin_sq,                                  rw [h0 ] at h1
     mul_comm, neg_mul]                                                  by_contra! h
   rw [sub_eq_add_neg]                                                   apply h.symm
   rw [mul_comm]                                                         simpa using h _
   rw [pow_two]
                                                                       Lean correctly rejects the above proof with the error:
   rw [← sub_eq_zero]
                                                                   “don’t know how to synthesize placeholder”. However, when
   simp only [mul_comm]
                                                                   executing the proof in the tactic mode using the old version
   simp [sub_eq_add_neg]
                                                                   of Lean REPL, the proof passes as correct.
   rw [add_comm]
                                                  (5)                  In a recent update,10 Lean REPL was extended to type-
   rw [← sub_eq_add_neg]
                                                                   check the full proof term after each tactic application, miti-
   rw [mul_comm]
                                                                   gating all false positives in the verification process, at the cost
   rw [mul_add]
                                                                   of introducing some drawbacks detailed below. We propose
   rw [sub_eq_add_neg]
                                                                   a different strategy: Instead of verifying the type-correctness
   simp_all
                                                                   of the whole proof term, type-check only the new assign-
   rw [add_comm]
                                                                   ments introduced by a tactic application.
   rw [← sub_eq_zero]
                                                                       To illustrate this difference, assume that we are searching
   rw [← neg_sub]
                                                                   for a proof of type 𝑇 and have already constructed a term
   rw [add_comm]
                                                                   𝑡 : 𝑇 which still contains unassigned metavariables of types
   rw [← neg_add]
                                                                   𝐺 1, . . . , 𝐺𝑛 . Next, assume that we apply a tactic assigning
   rw [sub_eq_add_neg]
                                                                   terms 𝑔1 : 𝐺 1, . . . , 𝑔𝑛 : 𝐺𝑛 to the metavariables in 𝑡. The
   rw [← sub_self]
                                                                   current strategy of Lean REPL is to type-check the whole
   rw [← neg_neg x]
                                                                   assignment 𝑡 : 𝑇 , which contains the new terms 𝑔1, . . . , 𝑔𝑛 as
   rw [sub_neg_eq_add]
                                                                   subterms.
   rw [neg_mul]
                                                                       This leads to issues when the proof bifurcates into two
   rw [add_comm]
                                                                   branches. For example, consider applying the tactic have k
   ring_nf
                                                                   := sorry in the REPL’s tactic mode.11 This corresponds to
   norm_num
                                                                   the assignment of the term ((fun k ↦→ ?_) sorry) to
                                                                   the metavariable corresponding to the main goal, where ?_
                                                                   is a new unassigned metavariable. Lean REPL then enables
                                                                   solving the ?_ and sorry parts independently. However,
 theorem
                                                                   assignments made in one of these two branches are not prop-
     algebra_2complexrootspoly_xsqp49eqxp7itxpn7i'
                                                                   agated to the other one, meaning that, from the perspective
     (x : C) :
                                                                   of each branch, the root proof term will always contain at
     x ^ 2 + 49 = (x + 7 * Complex.I) * (x + -7 *
                                                   (6)             least one hole introduced by an unassigned metavariable or
      Complex.I) := by
                                                                   the sorry keyword. This leads to the kernel always failing
   rw [← sub_eq_zero]
                                                                   during a type check for the duration of this proof. The end
   ring_nf
                                                                   effect is that the current verification strategy leads to false
   norm_num


D    Structured Proof Tree Extraction                              10 Published on GitHub on Apr 10, 2025.
                                                                   11 This is the standard way to use the have tactic in the REPL – see for
Figures 7 and 8 provide proof trees presented schematically        example https://github.com/leanprover-community/repl/blob/master/tes
in Figure 3.                                                       t/have_by_sorry.in
                                                              14
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4




                                                                                              ⊢ n > 0 → n < 2 * n

                                                                                                     intro h

                                                                                                 h : n > 0
                                                                                                 ⊢ n < 2 * n

                                                                                                     cases n



                                                                                      case zero          case succ
                                                                                      h : 0 > 0          h : n✝ + 1 > 0
                                                                                      ⊢ 0 < 2 * 0        ⊢ n✝ + 1 < 2 * (n✝ + 1)
    theorem succ_less_double_succ (n : Nat) :
        n > 0 → n < 2 * n := by                                                            apply h               case succ n'
      intro h
      cases n with                                                                                       h : n' + 1 > 0
      | zero => apply h                                                                                  ⊢ n' + 1 < 2 * (n' + 1)
      | succ n' =>
        apply Nat.le_trans                                                                                     apply Nat.le_trans
        case m => exact n' + 2
        · rfl                                                                                              h : n' + 1 > 0
        · rw [two_mul, add_succ]                                                                           ⊢ (n' + 1).succ ≤ ?m
                                                                                                           ⊢ ?m ≤ 2 * (n' + 1)
          have h1 : 1 ≤ n' + 1                                                                             ⊢ ℕ
          · apply Nat.succ_le_succ (Nat.zero_le _)
          · exact Nat.add_le_add_left h1 (n' + 1)
                                                                                                          case m => exact n' + 2



                                                                         h : n' + 1 > 0                  h : n' + 1 > 0
                                                                         ⊢ (n' + 1).succ ≤ n' + 2        ⊢ n' + 2 ≤ 2 * (n' + 1)


                                                                                     rfl                              ···
                                                                                                           have h1 : 1 ≤ n' + 1



                                                                    h : n' + 1 > 0          h : n' + 1 > 0
                                                                                            h1 : 1 ≤ n' + 1
                                                                    ⊢ 1 ≤ n' + 1
                                                                                            ⊢ (n' + 1).succ ≤ n' + 1 + (n' + 1)

                                                                             ···                                ···


Figure 7. Example Lean theorem and its corresponding executable proof tree extracted using LeanTree. Some tactics and
hypotheses are omitted.

negatives when the proof being verified contains at least one              Note that all proofs found by our prover are independently
syntactic branching.                                                     verified directly using Lean, bypassing Lean REPL together
   In contrast, the proposed strategy implemented in                     with the new verification algorithm described in this section.
LeanTree type-checks only the new assignments 𝑔1 :
𝐺 1, . . . , 𝑔𝑛 : 𝐺𝑛 introduced by a tactic application. The type
                                                                         F     Compute Estimation Methodology
correctness of the whole proof term 𝑡 : 𝑇 then follows
transitively. Most importantly, this new verification strategy           We estimate compute in FLOPs based on reported hardware
mitigates the false negatives described in the previous                  usage, training time, and the following approximate conver-
paragraph. Additionally, the new strategy also decreases                 sion factors for BF16:
the time complexity of verifying a proof from quadratic to                   • NVIDIA H100 NVL: 1671 TFLOPS

linear since each sub-assignment is only verified once.                      • NVIDIA A100: 312 TFLOPS
                                                                             • NVIDIA L40: 242 TFLOPS
                                                                             • NVIDIA V100: 125 TFLOPS
                                                                    15
                                                                                                               Matěj Kripner and Milan Straka


                                                                                 h : a + d = c + b
                                                                                 ⊢ a - b = c - d

                                                                          have h1 : a - b = a + d - d - b


                                                                            h : a + d = c + b
                                                                                                              h : a + d = c + b
                                                                            h1 : a - b = a + d - d - b
                                                                                                              ⊢ a - b = a + d - d - b
                                                                            ⊢ a - b = c - d
   theorem tsub_eq_tsub_of_add_eq_add (h : a + d = c + b) :
       a - b = c - d := by                                                                                    rw [add_tsub_cancel_right]
     calc a - b = a + d - d - b := by rw [add_tsub_cancel_right]             have h2 : a + d - d - b =
              _ = c + b - b - d := by rw [h, tsub_right_comm]                          c + b - b - d
              _ = c - d := by rw [add_tsub_cancel_right]

                                                                         h : a + d = c + b
                                                                                                              h : a + d = c + b
                                                                         h1 : a - b = a + d - d - b
                                                                                                              h1 : a - b = a + d - d - b
                                                                         h2 : a + d - d - b = c + b - b - d
                                                                                                              ⊢ a - b = a + d - d - b
                                                                         ⊢ a - b = c - d

                                                                                                               rw [h, tsub_right_comm]
                                                                                        ···
                                                                   exact Trans.trans h1 (Trans.trans h2 h3)




Figure 8. Example Lean theorem and its corresponding executable proof tree extracted using LeanTree. Some tactics and
hypotheses are omitted.

    •   Google TPU v6e (used in AlphaProof): 918 TFLOPS                       DeepSeek-Prover-V2 [32]: Because the compute budget
    • AMD Instinct MI250: 383 TFLOPS                                       of DeepSeek-Prover-V2 has not been disclosed, we estimate it
   Note that this form of compute budget estimation only                   as approximately 1013 TFLOPs based on its architecture and
provides rough estimates since the precise hardware charac-                training methodology: it fine-tunes a 671B parameter model
teristics and architectural details are not taken into consid-             using RL over a large formal proof dataset with recursive
eration.                                                                   self-play. The estimate is conservatively aligned with models
                                                                           of similar size and RL complexity.
                                                                              ReProver [47]: The training of retrieval and policy mod-
                                                                           els requires 5 A100-days, corresponding to 1.3 × 108 TFLOPs.
Per-Model Estimation Details                                               Inference then requires 16 V100-days, corresponding to
AlphaProof [14]: Computational budget as reported in-                      1.7 × 108 TFLOPs. However, the training was initialized from
cludes 10 TPUdays for base training, 100,000 TPUdays for                   Google ByT5 Small [45], which required an estimate of 109
the autoformalization process, 80,000 TPUdays for RL train-                TFLOPs. We thus report the total approximate budget as
ing, and 500 TPUdays per problem for TTRL. These 302,010                   1.3 × 109 TFLOPs.
TPUdays (with test set size 244) correspond approximately to                  BFS-Prover [43]: The prover is fine-tuned from Qwen2.5-
2.4 × 1013 TFLOPs. Of this budget, 100,000 TPUdays are spent               Math-7B, and its fine-tuning compute is not fully disclosed.
on autoformalization. NanoProof does not perform autofor-                  We therefore report a lower bound given by the pre-training
malization but consumes the NuminaMath-LEAN corpus,                        cost of the base model alone, estimated as 6𝑁 𝐷 for 𝑁 parame-
whose generation cost is not disclosed and not included in                 ters and 𝐷 training tokens, with 18T tokens for Qwen2.5 [46],
our total. Relative to NanoProof’s 3.8 × 108 TFLOPs, the ra-               giving approximately 7.6 × 1011 TFLOPs.
tio is approximately 63,000× for AlphaProof’s total budget,                   NanoProof: Here we describe one final run of NanoProof.
42,000× when its autoformalization stage is excluded, and                  Supervised training, consisting of base training and fine-
17,000× when counting only its RL stage; we therefore state                tuning, was performed on four A100-SXM4-40GB GPUs for
the difference conservatively as more than four orders of                  a total of 16.3 hours. RL training was performed on four AMD
magnitude.                                                                 Instinct MI250 accelerators (each exposing two GPU devices,
   HyperTree Proof Search (HTPS) [22]: Compute budget                      i.e., the eight GPUs of Section 5) for 45 hours together with
as reported is 1260 A100-days for training with negligible                 two CPU nodes with comparatively negligible TFLOPS. The
inference cost. This approximately corresponds to 3.4 × 1010               final pass@16 performance was evaluated on four AMD
TFLOPs.                                                                    Instinct MI250 GPUs for 11 hours.
   ABEL [11]: Compute budget as reported is 96 A100-days                      This approximately corresponds to 7.3 × 107 TFLOPs for
for training with negligible inference cost. This approxi-                 supervised training, 2.5 × 108 TFLOPs for RL, and 6.1 × 107
mately corresponds to 2.6 × 109 TFLOPs.
                                                                    16
NanoProof: Open and Efficient Automated Theorem Proving in Lean 4


TFLOPs for final evaluation, for a total of 3.8 × 108 TFLOPs.                        Third, LeanDojo does not contain information about the
Note that this total includes the final evaluation (6.1 × 107                     sub-proof size and sub-proof depth for each node, and pro-
TFLOPs, 16%), while the figures for HyperTree Proof Search                        vides tactics in an unstructured format that is not conducive
and ABEL cover training only.                                                     to proof tree building.
                                                                                     Pantograph [1] In contrast to LeanDojo, Pantograph’s
G     LeanTree Comparison to Existing Tools                                       interaction and data extraction modules offer proof state fac-
                                                                                  torization, meaning that independent goals can be explored
Several tools have recently emerged for both programmatic                         independently. Pantograph also provides information about
interaction with Lean and machine learning data extraction                        which goals are coupled via a shared metavariable.
from human-written Lean proofs. In this section, we compare                          However, tactic simplification and proof tree building are
them to LeanTree. We argue that LeanTree brings novel                             not supported by the data extraction module, leading to
unique extraction capabilities.                                                   the same drawbacks as described for the case of LeanDojo.
   Evariste [22] corresponds most closely to LeanTree.                            Information about sub-proof size and sub-proof depth is also
Evariste enables factorizing proof state into individual                          not provided.
goals, which can be explored independently. In addition,                             In addition, the Pantograph API is not well suited for
Evariste detects metavariable coupling and does not split                         gradually building the current Lean context by interleaving
metavariable-dependent goals, similar to LeanTree.                                definitions and theorems that can depend on any previously
   However, the Evariste dataset has not been released and                        declared ones. Instead, theorems are treated as independent
the tool itself is available only in a limited, nonexecutable for-                units.
mat.12 This makes it challenging to build on top of Evariste’s
contributions.                                                                    H    Dataset Schema
   Importantly, Evariste was only implemented for Lean 3,
                                                                                  Each sample in the LeanTree dataset corresponds to a Lean
which is now deprecated. Since its core logic is implemented
                                                                                  file rather than just an individual theorem. This is necessary
using C++, directly binding to Lean 3 internals, its migration
                                                                                  to capture the structure of a real-world Lean project like
to Lean 4 would be difficult. In contrast, the core logic of
                                                                                  Mathlib where a proof can depend on any definition located
LeanTree is implemented in Lean 4 itself, which is a common
                                                                                  above it in the source file.
Lean 4 paradigm [29]. Furthermore, LeanTree builds on top
                                                                                     Each file in the dataset contains a list of theorems, and
of the semi-official Lean REPL project, and it is therefore set
                                                                                  each theorem contains a list of all tactic proofs in its proof
to benefit from future improvements by the community.
                                                                                  term. Note that there can be more than one tactic proof for
   LeanDojo [47] offers both an interaction module and
                                                                                  a theorem if its proof contains more than one non-nested
a supervised data extraction module. The extracted data
                                                                                  by-blocks. For each tactic proof, the dataset then contains
also contains information about the premises used in each
                                                                                  a proof tree with nodes corresponding to factorized proof
tactic application, enabling training of retrieval-augmented
                                                                                  states and edges corresponding to tactic applications. Every
generation models. The extracted datasets are available for
                                                                                  proof node contains also precomputed size and the depth of
both Lean 3 and Lean 4.
                                                                                  its sub-tree.
   However, LeanDojo does not offer proof state factoriza-
                                                                                     Additionally, the LeanTree dataset contains information
tion, tactic simplification, or proof tree building. First, this
                                                                                  about the surrounding context, namely the list of imported
means that a tactic can only be applied to a whole proof state
                                                                                  modules for each Lean file and the list of open namespaces
consisting of a list of goals, yielding a new set of goals. This
                                                                                  for each theorem. The correspondence between samples in
prevents parallel search over independent goals.
                                                                                  the dataset and the underlying Lean repository is given by
   Second, tactics in the LeanDojo dataset are left in the form
                                                                                  character offsets specifying the span of each theorem, proof,
in which they appear in the abstract syntax tree of a Lean
                                                                                  and tactic execution.
source code. This includes complex or nested tactics that
                                                                                     The JSON schema of the dataset is presented in Figure 9.
span multiple lines. For example, the cases tactic shown in
Figure 7 is left unaltered. The user of the dataset can then
choose to filter out such samples, losing valuable training
data, or keep them in the training set, but increase the diffi-
culty of the modeling task and reduce the granularity of the
inference-time proof search.



12 Specifically, the codebase states: “code does NOT run out of the box as

we removed references to Meta-internal systems” https://github.com/faceb
ookresearch/Evariste
                                                                             17
                                                                                                   Matěj Kripner and Milan Straka


 1   < sample > : : = {
 2      " path " : < string >,
 3      " imports " : [ < string >],
 4      " theorems " : [ < theorem >]
 5   }
 6
 7   < theorem > : : = {
 8      " span " : < span ?>,
 9      " name " : < string ?>,
10      " context " : [ < string >],
11      " by_blocks " : [ < by_block >],
12      " error " : < string ?>
13   }
14
15   < by_block > : : = {
16      " span " : < span >,
17      " tree " : {
18         " nodes " : [ < proof_node >],
19         " root_id " : < string ?>,
20         " error " : < string ?>
21      }
22   }
23
24   < proof_node > ::= {
25      " id " : < string >,
26      " state " : {
27         " goals " : [ <goal >]
28      },
29      " tactic " : < edge ?>,
30      " proof_size ": < int ?>,
31      " proof_depth ": < int ?>
32   }
33
34   <edge > : : = {
35     " tactic_string ": < string >,
36     " span " : < span ?>,
37     " parent " : < string >,
38     " children " : [ < string >],
39     " tactic_depends_on ": [ < string >? ]
40   }
41
42   <goal > : : = {
43     " type " : < string >,
44     " hypotheses ": [ < hypothesis >],
45     " tag " : < string >?
46   }
47
48   < hypothesis > ::= {
49      " type " : < string >,
50      " user_name " : < string >,
51      " value " : < string >?
52   }
53
54   <span > : : = {
55     " start " : <int >,
56     " finish " : <int >
57   }


                                      Figure 9. JSON schema of a sample
                                                                  18    in the LeanTree dataset.
