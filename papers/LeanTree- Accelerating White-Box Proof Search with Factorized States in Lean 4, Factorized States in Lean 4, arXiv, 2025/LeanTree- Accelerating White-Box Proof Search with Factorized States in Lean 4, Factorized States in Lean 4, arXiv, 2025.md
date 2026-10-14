                                                              LeanTree: Accelerating White-Box Proof Search with
                                                                         Factorized States in Lean 4


                                                                              Matěj Kripner 1 Michal Šustr 2 Milan Straka 1


                                                                  Abstract                                     and chemistry (Bobbin et al., 2024) to software verifica-
                                                                                                               tion (Avigad et al., 2025), cryptography (Doussot, 2024),
                                              Automated theorem proving (ATP) has been a
                                                                                                               SQL query verification (Chu et al., 2018), and general rea-
                                              classical problem in artificial intelligence since
arXiv:2507.14722v1 [cs.LG] 19 Jul 2025




                                                                                                               soning (Jiang et al., 2024).
                                              its inception, yet it remains challenging due to its
                                              vast state and action space. Large language mod-                 Despite extensive research using logical formalisms, ATP
                                              els (LLMs) have recently emerged as a promis-                    continues to face significant challenges due to the com-
                                              ing heuristic for ATP, but they lack correctness                 binatorial explosion of its underlying state and action
                                              guarantees and thus require interaction with a                   spaces (Harrison, 2009; Baader, 2003; Barrett & Tinelli,
                                              proof verifier. Such interactions typically follow               2018) and the infinite branching factor introduced by exoge-
                                              one of two approaches: black-box interaction,                    nous term creation (Trinh et al., 2024).
                                              which does not utilize intermediate proof states, or
                                                                                                               Recent advances in large language models (LLMs) capable
                                              white-box approaches, which allow for incremen-
                                                                                                               of sophisticated reasoning in human languages (Guo et al.,
                                              tal proof construction and examination of interme-
                                                                                                               2025) have sparked interest in their application to ATP (Ren
                                              diate states. While black-box approaches have
                                                                                                               et al., 2025), serving as a powerful heuristic in navigating
                                              directly benefited from recent LLM advances,
                                                                                                               the proof search. Conversely, ATP and formal verification
                                              white-box methods have comparatively lagged
                                                                                                               present an avenue for improving reliability and interpretabil-
                                              behind. In this paper, we address this gap by intro-
                                                                                                               ity of LLMs (Achim & Tenev, 2023). Open-source tooling
                                              ducing LeanTree, which consists of (i) a tool built
                                                                                                               and datasets are crucial in leveraging this synergy.
                                              in the Lean 4 language that factorizes complex
                                              proof states into simpler, independent branches,                 The existing approaches for ATP can be categorized into
                                              and (ii) a dataset of these factorized intermediate              two distinct methodologies. In white-box generation, the
                                              states. Our white-box tooling offers several ad-                 prover interacts with a formal verifier iteratively, generat-
                                              vantages over black-box approaches: it simplifies                ing individual proof steps conditioned on the internal proof
                                              evaluation, reduces necessary context, generates                 state, interleaving proof search with verification. In contrast,
                                              richer training data, enables parallel search across             black-box provers only use the formal verifier to verify the
                                              multiple states, supports efficient reuse of states,             final proof, generating proof steps with no feedback about
                                              and provides feedback in case of errors. Our pre-                the validity of preceding steps or the current internal proof
                                              liminary results hint that white-box approaches                  state. Thus, in a black-box search, it falls upon the proof
                                              outperform black-box alternatives in some set-                   step generator to deduce the evolving proof state, as this
                                              tings.                                                           is a necessary precondition to determining the validity of a
                                                                                                               subsequent proof step. This coupling of policy model and
                                                                                                               world model increases complexity of proof step generation,
                                         1. Introduction                                                       necessitating the use of more powerful models, while also re-
                                                                                                               quiring the proof generator to be retrained when modifying
                                         Automated theorem proving (ATP) has long been a founda-               the formal verifier in case of upgrades or patches.
                                         tional task in artificial intelligence (Gelernter, 1959), with
                                         applications ranging from the formalization of mathemat-              While black-box whole-proof generation methods directly
                                         ics (van Doorn et al., 2023), physics (Tooby-Smith, 2024)             benefit from recent advances in LLMs (Wang et al., 2025),
                                                                                                               white-box tree-search methods have seen comparatively
                                            1
                                              Charles University, Faculty of Mathematics and Physics           little improvement since their introduction. Notably, the
                                         2
                                          Czech Technical University, Faculty of Electrical Engineering.       hypertree proof search approach introduced by Lample
                                         Correspondence to: Matěj Kripner <kripner@ufal.mff.cuni.cz>.
                                                                                                               et al. (2022) has not been replicated in open source or
                                         The second AI for MATH Workshop at the 42nd International             built upon, except for follow-up work by the same research
                                         Conference on Machine Learning, Vancouver, Canada.

                                                                                                           1
                       LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

group (Gloeckle et al., 2024). We attribute this primarily to          2. Related work
insufficient tooling and the lack of suitable datasets. Specifi-
cally, machine learning-based white-box techniques require             We give a brief overview of Lean, black-box and white-box
nontrivial preprocessing of existing proofs to extract inter-          ATP approaches, and existing datasets and benchmarks.
mediate proof states. Additionally, the size of proof states           Lean 4 (Moura & Ullrich, 2021) is a leading formal lan-
in verification languages like Lean tends to increase as the           guage for theorem proving with applications both in the
proof search progresses, exacerbating the distribution shift           formalization of mathematics (van Doorn et al., 2023) and
for LLMs pretrained on general text corpora. As such, it is            in numerous other domains (Tooby-Smith, 2024; Bobbin
desirable to simplify proof states by factorizing them into            et al., 2024; Doussot, 2024; Jiang et al., 2024). One of
branches that can be solved independently. Although Lam-               the pleasant attributes of Lean is its extensibility, stemming
ple et al. (2022) demonstrated the benefit of this white-box           from the fact that its theorem proving component is written
approach using factorized states, their tooling and dataset            in Lean itself, and the user can modify both its syntax and
remain practically unusable for the ATP community (see                 its semantics. Such an approach is possible because Lean
Section 5).                                                            4 is also a fully-fledged functional programming language.
To address these challenges, we introduce LeanTree, which              This is in contrast to previous versions of Lean, where some
is a) a tool for white-box interaction and data extraction             of the existing Lean interaction tools had to bind directly to
in Lean 4 (Moura & Ullrich, 2021), and b) a dataset of                 the Lean kernel written in C++.
preprocessed proofs from Mathlib (Community, 2020) and                 Black-box ATP. Automated theorem proving can be for-
DeepSeekProver-V1 (Xin et al., 2024a) in a unified format.             mulated as a text-to-text problem so that any existing ap-
Our contributions are as follows:                                      proach based on a large language model (LLM) is directly
                                                                       applicable. This approach to theorem proving was pio-
   • We build on top of Lean REPL (Community, 2025)
                                                                       neered by Baldur (First et al., 2023). Recently, a LLM with
     to enable programmatic proof search over factorized
                                                                       chain-of-thought refined using reinforcement learning was
     proof states, meaning that independent goals can be
                                                                       utilized by DeepSeek-Prover-V2 (Ren et al., 2025), Kimina-
     solved individually (Section 3.2). To enable this, we
                                                                       Prover (Wang et al., 2025), and InternLM-Math (Ying et al.,
     detect dependence between goals caused by metavari-
                                                                       2024b), securing top places on relevant benchmarks.
     able coupling (Section 3.3). Other improvements over
     Lean REPL include better error reporting, richer in-              White-box ATP. In white-box ATP, the prover interacts with
     formation about open goals, and a new incremental                 the verification system iteratively during a proof search,
     strategy for proof verification in Lean REPL using the            generating proof steps conditioned on the internal proof
     Lean’s verification kernel (Appendix B).                          state, with consequences discussed in the introduction
   • We build a data extraction module by integrating Lean             of this paper. In neural theorem proving, this approach
     REPL, PaperProof (Karunus & Kovsharov, 2024), and                 was pioneered by Holophrasm (Whalen, 2016) in Meta-
     a custom algorithm for proof tree building and tactic             math (Megill & Wheeler, 2019), using a UCT-based (Koc-
     simplification (Section 4.1). The extracted dataset also          sis & Szepesvári, 2006) AND-OR tree search with a RNN
     contains information about the current Lean context for           sequence-to-sequence model for tactic enumeration and pay-
     each theorem and the distance to the end of the proof             off prediction. This approach was extended by GPT-f (Polu
     for each step.                                                    & Sutskever, 2020) and Evariste (Lample et al., 2022), with
   • We release the resulting suite of tools and datasets,             the latter additionally targeting Lean 3. ABEL (Gloeckle
     dubbed LeanTree, in a format directly accessible by               et al., 2024) extended Evariste with incremental improve-
     the community12 with a user-friendly Python interface.            ments and Lean 4 compatibility, but did not release their
   • We present a preliminary experiment hinting that sup-             code or dataset.
     plying information about the intermediate proof state
                                                                       Datasets. The standard library of Lean, Mathlib (Commu-
     to a pretrained model during proof search outperforms
                                                                       nity, 2020), offers more than 107k formal definitions and
     black-box generation.
                                                                       220k formal proofs. Together with numerous formaliza-
   • We identify and prevent false-positive errors in proof
                                                                       tion projects created by the community, this offers a sizable
     search that result from the usage of library search tac-
                                                                       human-written dataset for black-box theorem proving.
     tics such as apply? (Appendix A). For example, such
     errors are present in the proofs presented by DeepSeek-           In contrast, white-box ATP approaches require data in a
     Prover-V2 (Ren et al., 2025).                                     more preprocessed format that reveals intermediate proof
   1                                                                   states. First, such a dataset was provided by LeanStep (Han
   https://github.com/Kripner/leantree
   2
   https://huggingface.co/datasets/ufal/                               et al., 2021) in Lean 3 by extracting tactic invocation data
leantree                                                               from Mathlib. LeanDojo (Yang et al., 2023) extends this
                                                                       for Lean 4, additionally containing information about the

                                                                   2
                       LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

premises used in each tactic application, suitable for training       written proofs.
retrieval-augmented approaches. Similar datasets are also
                                                                      Upon entering tactic mode using the by keyword, Lean
offered by Pantograph (Aniva et al., 2024) and lean-training-
                                                                      creates a metavariable with the desired type a - b = a
data (Morrison, 2023). Additionally, Lean-Workbook (Ying
                                                                      and no value assigned yet. Metavariables can be thought
et al., 2024a) and DeepSeek-Prover-V1 (Xin et al., 2024a)
                                                                      of as holes in a proof that have to be filled in before the
provide large collections of automatically formalized proofs
                                                                      proof is considered finished. This gives us an intermediate
of various quality. However, none of these datasets offers
                                                                      state in the proof construction, where the proof term is type-
tactic proofs in a structured, simplified way, which we de-
                                                                      correct but still contains holes to be filled in later. The still
scribe in this paper.
                                                                      unassigned metavariables are called open goals so that each
Benchmarks. ATP benchmarks typically consist of a set                 goal has a target type and a set of available free variables
of formalized theorem statements, optionally accompanied              called hypotheses. Because goals are metavariables, the two
by their informal counterparts in natural language, where             terms are often used interchangeably.
the objective is to generate a valid proof. MiniF2F (Zheng
                                                                      We then proceed by applying a tactic to the list of open goals.
et al., 2021) offers 488 problems drawn from mathematical
                                                                      A tactic is a procedure that assigns values to one or more
olympiad and undergraduate mathematics courses, formal-
                                                                      open goals, with each of the values possibly containing new
ized in parallel in Lean 3, Metamath, Isabelle, and HOL
                                                                      unassigned metavariables. In this way, a tactic invocation
Light. The benchmark was later ported to Lean 4 by Yang
                                                                      transforms the list of open goals into a new list of open
et al. (2023), with some formalization errors corrected by
                                                                      goals. Typically, a tactic only affects the main goal (defined
Wu et al. (2024).
                                                                      to be the first goal), either solving it or reducing it to one
Similarly, ProofNet (Azerbayev et al., 2023a) provides 371            or more simpler sub-goals. The proof is finished once there
problems formalized in Lean 3, together with their natural            are no more open goals, i.e., every metavariable has been
language statement and natural language proof, making it              assigned.
suitable also for evaluating autoformalization approaches.
This benchmark was ported to Lean 4 by Xin et al. (2024b).            3.1. LeanTree interaction module
PutnamBench (Tsoukalas et al., 2024) comprises of 1 099               LeanTree offers a Python interface, where the user can initi-
problems formalized in Lean 4, Isabelle, and Coq. This                ate a proof search either from an individual theorem state-
benchmark is comparatively difficult, with DeepSeek-                  ment or from a Lean file. After applying a Lean tactic to a
Prover-V2 (Ren et al., 2025), the current state-of-the-art,           proof state, LeanTree returns a list of resulting sub-states.
attaining only 7.2 % success rate with pass@1024.3                    This interface is suitable for tree search and backtracking as
Lean Tooling. The comparison of LeanTree with existing                the interaction can be started from any intermediate proof
tools is given in Section 5.                                          state. Additionally, given the high CPU requirements of
                                                                      Lean 4, LeanTree implements a dynamic pool of environ-
                                                                      ments suitable for parallel execution.
3. Lean programmatic interaction
We build on top of Lean REPL (Community, 2025) to enable              3.2. Factorized proof states
incremental proof execution. In this section, we describe             We follow Lample et al. (2022) in factorizing proof states
the LeanTree interaction module.                                      into independent goals, which can be explored and proven
Preliminaries. In Lean, theorem proving consists of pro-              individually. Note that in this section, we disregard metavari-
ducing a term whose type is equal to the theorem type. For            able coupling, which is then addressed in Section 3.3.
example, consider the following theorem:                              The utility of proof state factorization has been identified by
                                                                      Lample et al. (2022), citing the “re-use and parallelization
 theorem sub_zero (a b : N) (h : b = 0)                               in the proof search algorithm” as their primary motivation.
   : a - b = a                                             (1)
                                                                      An example of potential state reuse is shown in Figure 1,
                                                                      where the same node is reached using two different search
Proving Theorem 1 consists of supplying a term of type                paths. To illustrate proof search parallelization, consider the
a - b = a using available free variables a, b of type N               following theorem:
and h of type b = 0. While such a term can be written
down explicitly, it is common to utilize Lean’s tactic mode            theorem mul_eq_zero_iff (n m : N)
                                                                         : n * m = 0 ↔ n = 0 ∨ m = 0                               (2)
to structure the proof in a format more aligned with human-
  3
    https://trishullab.github.io/                                     A possible strategy to prove Theorem 2 is to branch out
PutnamBench/leaderboard.html (retrieved Jun 2025)                     based on the values of n and m. We achieve this by execut-

                                                                  3
                           LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

ing the tactic cases n <;> cases m. Since each of                     cutions, leading to incorrect proofs being accepted in some
the two numbers can be either zero or a successor of another          cases. Our prover managed to exploit these inconsistencies,
number following the Peano axioms, the resulting proof                finding 12 incorrect proofs on MiniF2F that passed veri-
state consists of four goals. For example, one of the states          fication in the REPL. We describe these incorrect proofs
is (n′ + 1) · 0 = 0 ↔ n′ + 1 = 0 ∨ 0 = 0, corresponding               and recent approaches to fix Lean REPL in the appendix.
to the case where n is a successor and m is zero.                     Note that all proofs found by our prover are also indepen-
                                                                      dently verified directly using Lean, which guarantees their
To complete the proof, all four goals must be closed. In
                                                                      correctness.
a non-factorized setting, the proof state consisting of four
goals is assessed by the policy and critic models as a whole.
Since tactics typically affect only the main goal, the last           4. Supervised data extraction
goal can only be worked on once all others have been closed.
                                                                      To enable machine learning-based approaches to imitate
In contrast, factorized states allow the search algorithm to
                                                                      proofs without interfacing with Lean, LeanTree offers a data
focus on the goals individually, in any order the algorithm
                                                                      extraction module to create supervised data from existing
deems fit.
                                                                      Lean proofs. The data extraction module is fully compatible
As a final advantage, simplifying states reduces the difficulty       with the interaction module in the sense that the extracted
of the policy task, deciding which tactic to apply next, and          proof trees can be directly executed and verified.
of the critic task, estimating the value of the current goal.
Note that proof states can grow arbitrarily complex during            4.1. Proof tree building
proof search since each state corresponds to a list of goals.
                                                                      To achieve compatibility with the interaction module, the
AND-OR Search. Search over factorized states naturally                proof states extracted from supervised data must be factor-
leads to an AND-OR tree, where a prover selects a tactic              ized into independent branches as described in Section 3.2.
in an OR node and subsequently has to prove all goals in              This process yields a proof tree where each node contains
an AND node. Figure 1 shows an example where choosing                 a list of goals (typically a singleton list), and each edge
either the rw tactic or the cases tactic in the root leads to         corresponds to a tactic application.
a proof. For a more in-depth introduction to proof search in
Lean, we recommend (Limperg & From, 2023).                            To illustrate some challenges in building a proof tree, con-
                                                                      sider the Lean proof and its corresponding proof tree shown
                                                                      in Figure 2, where we prove n < 2n under the condition
3.3. Metavariable coupling
                                                                      n > 0. For the purposes of this illustration, we do not utilize
Contrary to the simplified view presented in Section 3.2, it          powerful tactics like linarith, which would solve this
is not always possible to fully factorize the proof state into        trivial theorem nearly automatically. Instead, we illustrate
individual goals that can be proven independently. Subse-             branching, metavariable coupling, and the introduction of a
quently, nodes in the proof tree are allowed to contain more          new hypothesis.
than one goal. Specifically, this occurs when two goals share
                                                                      Note that in the original Lean proof in Figure 2, tactics are
the same metavariable. For example, applying the transi-
                                                                      nontrivially structured via branching using cases, focusing
tivity lemma Nat.le trans to the goal 2 ≤ 5 produces
                                                                      a goal via the center-dot operator, and merging multiple
goals 2 ≤ ?m and ?m ≤ 5 sharing a metavariable ?m whose
                                                                      rw commands into one. Additionally, each Lean tactic
value has not yet been decided.4 Subsequently, choosing
                                                                      consumes the set of currently open goals – the unfactorized
a value for ?m in one of the goals affects the provability
                                                                      proof state – and produces a new set of open goals – a new
of the other goal, and therefore the two goals cannot be
                                                                      proof state. In contrast, each edge of the constructed proof
explored independently. For a more in-depth explanation of
                                                                      tree corresponds to a simple tactic applied to a minimal
this phenomenon, we recommend Aniva et al. (2024).
                                                                      list of goals that cannot be split further due to metavariable
LeanTree detects all dependencies between goals caused                coupling.
by metavariables and offers strategies to deal with them
                                                                      To illustrate metavariable coupling, observe that applying
during proof search. By default, goals are factorized to the
                                                                      Nat.le trans yields three goals that are not split due to
maximum extend allowed by metavariable coupling.
                                                                      a shared metavariable ?m. However, once the metavariable
                                                                      is assigned using exact, the remaining two goals are now
3.4. Proof verification                                               independent and can be split.
Originally, the Lean REPL did not utilize Lean verification           Finally, note that in the proof tree, the tactic case succ
kernel to type-check assignments introduced by tactic exe-            n’ and its parent node are synthetic in the sense that they do
   4
       A third goal of type N is created for technical reasons.       not have a counterpart in the original proof. This synthetic


                                                                  4
                       LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

                          OR                 AND                      OR                    AND
                                              rw [h]                 ⊢ a-0=a            rw [Nat.sub_zero]
                       h:b=0
                      ⊢ a-b=a                                        ⊢ a-0=a            rw [Nat.sub_zero]
                                             cases b
                                                                h : b’ + 1 = 0
                                                                ⊢ a - (b’ + 1) = a        contradiction



Figure 1: Example of an AND-OR proof tree for Theorem 1. Nodes connected with a dashed line could potentially be
merged and correspond to transpositions in board games. This is possible thanks to factorization (see Section 3.2).


tactic is necessary to assign the name n’ to the otherwise           In Listing 3, the exact tactic is parametrized by a term
inaccessible variable – denoted n† before the assignment –           which contains a tactic block introduced using the by key-
so that it can be referenced by later tactics.                       word. We break down this complex proof step by masking
                                                                     the nested tactic block and instead spawning a child goal,
Other Lean features not shown in Figure 2 that further com-
                                                                     yielding the following series of simpler proof steps.
plicate proof tree construction include tactic combinators
such as try, iterate, and any goals, where the set of
affected goals is determined in runtime, constructs such as           exact ⟨by sorry, rfl⟩
                                                                      rw [aeval_algHom_apply]
all goals and <;> that go against the tree formulation                rw [hw]                                                   (4)
by operating on multiple goals, or tactics like switch and            rw [map_zero]
rotate left that change the order of open goals.
We implement the transformation illustrated in Figure 2 in           Note that the rfl tactic is not masked since it is used as a
three stages described in the following three subsections.           term instead of as a tactic.
                                                                     Structuring tactics. The cases and induction tactics
4.1.1. S INGLETON TREES                                              introduce syntactic branching by partitioning a proof based
In the first stage of proof tree building, a Lean proof is           on the value of an inductive type. The respective tactic
transformed into a singleton tree, where each node contains          optionally contains a solving branch for each constructor
a single goal, by matching tactic applications with the goals        of such type. For example, the cases tactic in Listing 2
they affect. This is nontrivial, because, in general, a tactic       provides separate proofs for the zero and succ construc-
application transforms a list of open goals into an entirely         tors of variable n. This cases tactic spans 10 lines, which
new list of empty goals without any guarantees about the             is contrary to our effort of breaking down the proof into
transformation.                                                      simple steps. For this reason, we move the individual proof
                                                                     branches from the cases tactic into their separate proof
To build the singleton tree, we integrate Lean REPL with the         steps.
BetterParser module of PaperProof (Karunus & Kovsharov,
2024), which solves the analogous problem for the purposes           However, branches corresponding to parametrized construc-
of visualization.                                                    tors can optionally assign names to some of the constructors’
                                                                     parameters. For example, in Listing 2, the succ constructor
4.1.2. TACTIC SIMPLIFICATION                                         is parametrized by a single natural number which is given
                                                                     the name n’. When the cases tactic is broken down, the
In the second stage, the singleton tree is modified so that          name n’ has to be assigned manually, since Lean disallows
complex tactics are broken down into simpler ones and each           referring to variables with no explicitly assigned name. We
tactic is a valid self-contained proof step. Here we describe        achieve this by adding a synthetic tactic case which has
some of these modifications.                                         no direct tactic counterpart in the original proof. Note that
Nested Tactics. Tactics parametrized by a term can them-             the same effect could be achieved using the rename tactic,
selves contain nested tactic blocks. For example, consider           which is, however, rare in human-written proofs.
the following tactic from the Complex Analysis module in             Merged rw tactics. In Lean, subsequent rw tactics can
Mathlib.                                                             be merged into a single tactic, which is commonplace in
                                                                     human-writen proofs. We partition such composite tactics
 exact ⟨by                                                           back into individual rw tactics. This is also the case for the
  rw [aeval_algHom_apply, hw, map_zero], (3)                         rwa tactic, where we additionally add the assumption
  rfl⟩                                                               tactic to preserve semantics.

                                                                 5
                       LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

                                                                                        ⊢ n > 0 → n < 2 * n
      theorem succ_less_double_succ (n : Nat) :
          n > 0 → n < 2 * n := by
                                                                                               intro h
        intro h
        cases n with                                                                       h : n > 0
        | zero => apply h                                                                  ⊢ n < 2 * n
        | succ n' =>
          apply Nat.le_trans                                                                   cases n
          case m => exact n' + 2
          · rfl
          · rw [two_mul, add_succ]                                               case zero          case succ
                                                                                 h : 0 > 0          h : n✝ + 1 > 0
            have h1 : 1 ≤ n' + 1
                                                                                 ⊢ 0 < 2 * 0        ⊢ n✝ + 1 < 2 * (n✝ + 1)
            · apply Nat.succ_le_succ (Nat.zero_le _)
            · exact add_le_add_left h1 (n' + 1)                                                              case succ n'
                                                                                     apply h

                                                                                                    h : n' + 1 > 0
                                                                                                    ⊢ n' + 1 < 2 * (n' + 1)


                                                                                                          apply Nat.le_trans

                                                                                                         h : n' + 1 > 0
        1. Factorize   proof states using PaperProof.                                                    ⊢ (n' + 1).succ ≤ ?m
        2. Simplify                                                                                      ⊢ ?m ≤ 2 * (n' + 1)
               nested tactics,                                                                           ⊢ ℕ
               structuring tactics,
               composite rw tactics                                                                  case m => exact n' + 2
               ...
        3. Merge metavariable-dependent goals.
                                                                     h : n' + 1 > 0                 h : n' + 1 > 0
                                                                     ⊢ (n' + 1).succ ≤ n' + 2       ⊢ n' + 2 ≤ 2 * (n' + 1)


                                                                               rfl                               ···
                                                                                                         have h1 : 1 ≤ n' + 1



                                                                                       h : n' + 1 > 0
                                                             h : n' + 1 > 0
                                                                                       h1 : 1 ≤ n' + 1
                                                             ⊢ 1 ≤ n' + 1
                                                                                       ⊢ (n' + 1).succ ≤ n' + 1 + (n' + 1)

                                                                     ···                                   ···

Figure 2: Proof tree builder in LeanTrees transforms a Lean proof with complex structure (left) into a proof tree (right) with
simple states (lists of goals that cannot be split further) and transitions (tactics). Synthetic elements in the proof tree are
marked using dashed border.


4.1.3. M ERGING METAVARIABLE - DEPENDENT GOALS                       4.2. LeanTree dataset
To obtain the final proof tree, sibling nodes in a singleton         We release the extracted proof tree data in an unified format
tree are merged if they share a metavariable. This corre-            from two sources: 1) a recent version of Mathlib 4,5 the
sponds to the fact that metavariable-dependent goals cannot          standard library of human-written proofs in Lean, and 2) a
be explored independently.                                           collection of 27.5K proofs autoformalized by DeepSeek-
                                                                     Prover-V1.6 Importantly, each sample in the LeanTree
During this merging process, the entire proof tree is executed
                                                                     dataset corresponds to a Lean file rather than just an in-
in Lean REPL starting from the root state and following
                                                                     dividual theorem. This is necessary to capture the structure
each tree edge, verifying that each proof branch ends in
                                                                     of a real-world Lean project like Mathlib where a proof can
a proven state. In this way, we ensure the correctness of
                                                                     depend on any definition located above it in the source file.
the whole proof tree building process. Proof trees that fail
this verification are not included in the final dataset (cf.         Each file in the LeanTree dataset contains a list of theorems,
Section 4.2).                                                           5
                                                                        leanprover/lean4:v4.19.0, Apache-2.0 license
                                                                        6
                                                                        https://huggingface.co/datasets/
                                                                     deepseek-ai/DeepSeek-Prover-V1, MIT License


                                                                 6
                       LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

and each theorem contains a list of all tactic proofs in its          mented using C++, directly binding to Lean 3 internals, its
proof term. Note that there can be more than one tactic proof         migration to Lean 4 would be difficult. In contrast, the core
for a theorem if its proof contains more than one non-nested          logic of LeanTree is implemented in Lean 4 itself, which
by-blocks. For each tactic proof, LeanTree then contains              is a common Lean 4 paradigm (Moura & Ullrich, 2021).
a proof tree with nodes corresponding to factorized proof             Furthermore, LeanTree builds on top of the semi-official
states and edges corresponding to tactic applications.                Lean REPL project, and it is therefore set to benefit from
                                                                      future improvements by the community.
To demonstrate a possible use case for proof trees, the
dataset also contains the size and depth for each proof tree          LeanDojo (Yang et al., 2023) offers both an interaction
node. These can serve as objectives for a critic model in             module and a supervised data extraction module. The ex-
various proof search algorithm.                                       tracted data also contains information about the premises
                                                                      used in each tactic application, enabling training of retrieval-
Additionally, the LeanTree dataset contains information
                                                                      augmented generation models. The extracted datasets are
about the surrounding context, namely the list of imported
                                                                      available for both Lean 3 and Lean 4.
modules for each Lean file and the list of open namespaces
for each theorem. The correspondence between samples in               However, LeanDojo does not offer proof state factorization,
the dataset and the underlying Lean repository is given by            tactic simplification, or proof tree building. First, this means
character offsets specifying the span of each theorem, proof,         that a tactic can only be applied to a whole proof state
and tactic execution.                                                 consisting of a list of goals, yielding a new set of goals.
                                                                      This prevents parallel search over independent goals.
Overall, LeanTree contains 74 706 factorized tactic proofs
from Mathlib and 26 201 from DeepSeek-Prover-V1. Since                Second, tactics in the LeanDojo dataset are left in the form
Lean was not designed to enable factorized proof tree search          in which they appear in the abstract syntax tree of a Lean
out-of-the-box, there are a large number of small techni-             source code. This includes complex or nested tactics that
cal challenges to overcome during the proof tree building.            span multiple lines. For example, the cases tactic shown
While we are continually working on perfecting this process,          in Figure 2 is left unaltered. The user of the dataset can then
not all tactic proofs can currently be converted. Specifically,       choose to filter out such samples, losing valuable training
23.0% of tactic proofs in Mathlib and 4.7% in DeepSeek-               data, or keep them in the training set, but increase the diffi-
Prover-V1 were not converted. We note that for Mathlib,               culty of the modeling task and reduce the granularity of the
28.6% of the issues stem from the usage of calc and conv              inference-time proof search.
tactics that fundamentally change the structure of a proof.
                                                                      Third, LeanDojo does not contain information about the sub-
                                                                      proof size and sub-proof depth for each node, and provides
5. Comparison to existing tools                                       tactics in an unstructured format that is not conducive to
                                                                      proof tree building.
Several tools have recently emerged both for programmatic
interaction with Lean and machine learning data extraction            Pantograph (Aniva et al., 2024) In contrast to LeanDojo,
from human-written Lean proofs. In this section, we com-              Pantograph’s interaction and data extraction modules offer
pare them to LeanTree. We argue that LeanTree is unique               proof state factorization, meaning that independent goals
in its data extraction capabilities.                                  can be explored independently. Pantograph also provides
                                                                      information about which goals are coupled via a shared
Evariste (Lample et al., 2022) corresponds most closely
                                                                      metavariable.
to LeanTree. Evariste enables factorizing proof state into
individual goals, which can be explored independently. In             However, tactic simplification and proof tree building are
addition, Evariste detects metavariable coupling and does             not supported by the data extraction module, leading to
not split metavariable-dependent goals, similar to LeanTree.          the same drawbacks as described for the case of LeanDojo.
                                                                      Information about sub-proof size and sub-proof depth is
However, the Evariste dataset has not been released and the
                                                                      also not provided.
tool itself is available only in a limited, nonexecutable for-
mat.7 This makes it challenging to build on top of Evariste’s         In addition, the Pantograph API is not well suited for gradu-
contributions.                                                        ally building the current Lean context by interleaving def-
                                                                      initions and theorems that can depend on any previously
Importantly, Evariste was only implemented for Lean 3,
                                                                      declared ones. Instead, theorems are treated as independent
which is now deprecated. Since its core logic is imple-
                                                                      units.
   7
     Specifically, the codebase states: “code does NOT run
out of the box as we removed references to Meta-internal
systems” https://github.com/facebookresearch/
Evariste


                                                                  7
                         LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

                                                                               best-first search
                                                                          25
         Approach                MiniF2F-test                             20




                                                            MiniF2F (%)
         Whole-proof              9.59 % ± 0.71                           15
         Black-box rollout        5.32 % ± 0.37
         White-box rollout       18.36 % ± 0.60                           10 whole-proof generation
         Best-first search∗      26.23 %
                                                                           5
         ∗
             Reported by Azerbayev et al. (2023b).
                                                                           0      Black-box                       White-box
                                                                                   Rollout                         Rollout
Figure 3: Performance on MiniF2F using linear rollouts with Llemma-7B. Error bars show standard deviation over 5 runs.


6. Experiments                                                            7. Conclusion
We investigate the utility of white-box approach in proof                 In this work, we introduced LeanTree, a novel white-box
search using the Llemma-7B model (Azerbayev et al.,                       tool designed to accelerate white-box approaches to auto-
2023b) (MIT license), reporting the success rate on MiniF2F               mated theorem proving in Lean 4 via factorized proof states
test set (Zheng et al., 2021) modified for Lean 4 by Wu et al.            and structured proof trees. Our approach addresses limita-
(2024). For each input theorem, we run N = 10 inde-                       tions of existing black-box methods by leveraging interme-
pendent linear rollouts, starting from an empty proof and                 diate proof states, enabling parallelized and efficient proof
sequentially sampling tactics proposed by the model for a                 search, and providing structured feedback during theorem
maximum of M = 25 steps. The search is successful if the                  proving. LeanTree’s integration with Lean REPL ensures
concatenated tactics from a rollout are a valid proof of the              that it will continue to benefit from patches and fixes by the
input theorem. If no proof is found during the N rollouts,                Lean community.
the search is unsuccessful.
                                                                          Additionally, we released a unified dataset of factorized in-
In Figure 3, we report the results for the black-box and                  termediate proof states derived from Mathlib and DeepSeek-
white-box rollouts averaged over 5 runs with error bars of                Prover-V1. A limitation of LeanTree is that currently not all
one standard deviation. We additionally report the success                tactic proofs can be converted.
rate of black-box whole proof generation, where the model
                                                                          Finally, our preliminary experiments hint that white-box
is prompted to generate the entire proof at once. Lastly, we
                                                                          approaches, facilitated by LeanTree, can outperform black-
include the success rate of proof generation using best-first
                                                                          box methods in automated theorem proving. We hope that
search (Polu & Sutskever, 2020) reported by Azerbayev
                                                                          LeanTree serves as a stepping stone toward more efficient,
et al. (2023b), which performs white-box rollouts in a tree
                                                                          parallelizable, and reliable proof search and encourages
fashion and is therefore a natural upper bound on the white-
                                                                          further research into white-box automated theorem proving.
box rollout performance.
Our results show that in our specific setting, supplying the              Acknowledgements
prover with internal proof states improves proof search per-
formance. Interestingly, black-box linear rollouts achieve                Matěj Kripner was supported by the grant no. 25-18031S
worse performance than black-box whole-proof generation,                  of the Czech Science Foundation (GAČR). This research
indicating that constraining the model to generate only one               was partially supported by SVV project number 260 821.
tactic at a time hurts its performance. However, rollouts                 We acknowledge VSB – Technical University of Ostrava,
with access to the internal state consistently outperform                 IT4Innovations National Supercomputing Center, Czech
both black-box methods.                                                   Republic, for awarding this project access to the LUMI
                                                                          supercomputer, owned by the EuroHPC Joint Undertaking,
We run all our experiments on a single node equipped with 8
                                                                          hosted by CSC (Finland) and the LUMI consortium through
AMD MI210 accelerators and 192 CPU nodes, parallelizing
                                                                          the Ministry of Education, Youth and Sports of the Czech
both model inference and Lean interaction. In total, our ex-
                                                                          Republic through the e-INFRA CZ (grant ID: 90254). The
periments necessitated 59 GPU-hours and 450 CPU-hours.
                                                                          authors thank Martin Suda, Matej Straka, Tomáš Čı́žek,
                                                                          Radovan Haluška, Martin Schmid, and the Lean community
                                                                          for helpful suggestions and corrections.

                                                                    8
                      LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

References                                                         Doussot, G. Cryptography experiments in lean 4: SHA-
                                                                     3 implementation. Cryptology ePrint Archive, Paper
Achim, T. and Tenev, V. Harmonic: Building mathematical
                                                                     2024/1880, 2024. URL https://eprint.iacr.
  superintelligence. https://harmonic.fun/, 2023.
                                                                     org/2024/1880.
  Accessed: 2025-05-14.
                                                                   First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:
Aniva, L., Sun, C., Miranda, B., Barrett, C., and Koyejo,
                                                                     Whole-proof generation and repair with large language
  S. Pantograph: A machine-to-machine interaction in-
                                                                     models. In Proceedings of the 31st ACM Joint European
  terface for advanced theorem proving, high level rea-
                                                                     Software Engineering Conference and Symposium on the
  soning, and data extraction in lean 4. arXiv preprint
                                                                     Foundations of Software Engineering, pp. 1229–1241,
  arXiv:2410.16429, 2024.
                                                                     2023.
Avigad, J., Goldberg, L., Levit, D., Seginer, Y., and Titel-
  man, A. A proof-producing compiler for blockchain appli-         Gelernter, H. L. Realization of a geometry theorem-proving
  cations. J. Autom. Reason., 69(2), April 2025. ISSN 0168-          machine. In Proceedings of the First International Con-
  7433. doi: 10.1007/s10817-025-09723-y. URL https:                  ference on Information Processing (IFIP), pp. 273–281,
  //doi.org/10.1007/s10817-025-09723-y.                             1959.

Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,       Gloeckle, F., Limperg, J., Synnaeve, G., and Hayat, A.
  Radev, D., and Avigad, J. ProofNet: Autoformalizing                ABEL: Sample efficient online reinforcement learning
  and formally proving undergraduate-level mathematics               for neural theorem proving. In The 4th Workshop on
  (2023). URL https://arxiv. org/abs/2302.12433, 2023a.              Mathematical Reasoning and AI at NeurIPS’24, 2024.

Azerbayev, Z., Schoelkopf, H., Paster, K., Santos, M. D.,          Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R.,
  McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and             Zhu, Q., Ma, S., Wang, P., Bi, X., et al. Deepseek-r1: In-
 Welleck, S. Llemma: An open language model for math-                centivizing reasoning capability in llms via reinforcement
  ematics. arXiv preprint arXiv:2310.10631, 2023b.                   learning. arXiv preprint arXiv:2501.12948, 2025.

Baader, F. The description logic handbook: Theory, imple-          Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S. Proof
  mentation and applications. Cambridge university press,            artifact co-training for theorem proving with language
  2003.                                                              models. arXiv preprint arXiv:2102.06203, 2021.

Barrett, C. and Tinelli, C. Satisfiability modulo theories.        Harrison, J. Handbook of practical logic and automated
  Handbook of model checking, pp. 305–343, 2018.                     reasoning. Cambridge University Press, 2009.

Bobbin, M. P., Sharlin, S., Feyzishendi, P., Dang, A. H.,          Jiang, D., Fonseca, M., and Cohen, S. B. Leanreasoner:
  Wraback, C. M., and Josephson, T. R. Formalizing chem-              Boosting complex logical reasoning with lean. North
  ical physics using the lean theorem prover. Digital Dis-            American Chapter of the Association for Computational
  covery, 3(2):264–280, 2024.                                         Linguistics, 2024. doi: 10.48550/arxiv.2403.13312.

Chu, S., Murphy, B., Roesch, J., Cheung, A., and Suciu,            Karunus, E. and Kovsharov, A. Paperproof: A new
  D. Axiomatic foundations and algorithms for deciding               proof interface for lean 4. https://github.com/
  semantic equivalences of sql queries. Proc. VLDB Endow.,           Paper-Proof/paperproof, 2024. URL https:
 11(11):1482–1495, July 2018. ISSN 2150-8097. doi: 10.              //github.com/Paper-Proof/paperproof.
 14778/3236187.3236200. URL https://doi.org/                         Accessed: 2025-04-30.
  10.14778/3236187.3236200.
                                                                   Kocsis, L. and Szepesvári, C. Bandit based monte-carlo
Community, L. Lean 4 repl. https://github.com/                       planning. In European conference on machine learning,
  leanprover-community/repl, 2025. Accessed:                         pp. 282–293. Springer, 2006.
  2025-04-28.
                                                                   Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A.,
Community, M. The lean mathematical library. In Pro-                 Hayat, A., Lavril, T., Ebner, G., and Martinet, X. Hyper-
  ceedings of the 9th ACM SIGPLAN International Con-                 tree proof search for neural theorem proving. Advances in
  ference on Certified Programs and Proofs, CPP 2020,                neural information processing systems, 35:26337–26349,
  pp. 367–381, New York, NY, USA, 2020. Associa-                     2022.
  tion for Computing Machinery. ISBN 9781450370974.
  doi: 10.1145/3372885.3373824. URL https://doi.                   Limperg, J. and From, A. H. Aesop: White-box best-
  org/10.1145/3372885.3373824.                                       first proof search for lean. In Proceedings of the

                                                               9
                      LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

  12th ACM SIGPLAN International Conference on Cer-                    Kimina-prover preview: Towards large formal reason-
  tified Programs and Proofs, CPP 2023, pp. 253–266,                   ing models with reinforcement learning. arXiv preprint
  New York, NY, USA, 2023. Association for Comput-                     arXiv:2504.11354, 2025.
  ing Machinery. ISBN 9798400700262. doi: 10.1145/
  3573105.3575671. URL https://doi.org/10.                           Whalen, D. Holophrasm: a neural automated theo-
  1145/3573105.3575671.                                               rem prover for higher-order logic. arXiv preprint
                                                                      arXiv:1608.02644, 2016.
Megill, N. and Wheeler, D. A. Metamath: a computer
 language for mathematical proofs. Lulu. com, 2019.                  Wu, Z., Huang, S., Zhou, Z., Ying, H., Wang, J., Lin, D., and
                                                                      Chen, K. Internlm2. 5-stepprover: Advancing automated
Morrison, K. lean-training-data: Tools for extracting                 theorem proving via expert iteration on large-scale lean
 training-data from lean libraries. https://github.                   problems. arXiv preprint arXiv:2410.15700, 2024.
 com/kim-em/lean-training-data, 2023. Ac-
                                                                     Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan,
 cessed: 2025-07-01.
                                                                       C., Li, W., and Liang, X. Deepseek-prover: Advancing
Moura, L. d. and Ullrich, S. The Lean 4 theorem prover                 theorem proving in llms through large-scale synthetic
 and programming language. In Automated Deduction–                     data. arXiv preprint arXiv:2405.14333, 2024a.
 CADE 28: 28th International Conference on Automated
                                                                     Xin, H., Ren, Z., Song, J., Shao, Z., Zhao, W., Wang, H., Liu,
 Deduction, Virtual Event, July 12–15, 2021, Proceedings
                                                                       B., Zhang, L., Lu, X., Du, Q., et al. Deepseek-prover-v1.5:
 28, pp. 625–635. Springer, 2021.
                                                                       Harnessing proof assistant feedback for reinforcement
Polu, S. and Sutskever, I. Generative language model-                  learning and monte-carlo tree search. arXiv preprint
  ing for automated theorem proving. arXiv preprint                    arXiv:2408.08152, 2024b.
  arXiv:2009.03393, 2020.                                            Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
Ren, Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W.,              Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
  Zhang, L., Fu, Z., Zhu, Q., Yang, D., et al. Deepseek-               LeanDojo: Theorem proving with retrieval-augmented
  prover-v2: Advancing formal mathematical reasoning via               language models. Advances in Neural Information Pro-
  reinforcement learning for subgoal decomposition. arXiv              cessing Systems, 36:21573–21612, 2023.
  preprint arXiv:2504.21801, 2025.                                   Ying, H., Wu, Z., Geng, Y., Wang, J., Lin, D., and Chen,
                                                                       K. Lean workbook: A large-scale lean problem set for-
Tooby-Smith, J. Formalization of physics index no-
                                                                       malized from natural language math problems. arXiv
  tation in lean 4. ArXiv, abs/2411.07667, 2024.
                                                                       preprint arXiv:2406.03847, 2024a.
  URL https://api.semanticscholar.org/
  CorpusID:273970152.                                                Ying, H., Zhang, S., Li, L., Zhou, Z., Shao, Y., Fei, Z.,
                                                                       Ma, Y., Hong, J., Liu, K., Wang, Z., et al. Internlm-
Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T. Solv-
                                                                       math: Open math large language models toward verifiable
  ing olympiad geometry without human demonstrations.
                                                                       reasoning. arXiv preprint arXiv:2402.06332, 2024b.
  Nature, 625(7995):476–482, 2024.
                                                                     Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jen-
                                                                       benchmark for formal olympiad-level mathematics. arXiv
  nings, M., Thakur, A., and Chaudhuri, S. Putnambench:
                                                                       preprint arXiv:2109.00110, 2021.
  Evaluating neural theorem-provers on the putnam mathe-
  matical competition. arXiv preprint arXiv:2407.11214,
  2024.

van Doorn, F., Massot, P., and Nash, O. Formalis-
  ing the h-principle and sphere eversion. In Proceed-
  ings of the 12th ACM SIGPLAN International Con-
  ference on Certified Programs and Proofs, CPP 2023,
  pp. 121–134, New York, NY, USA, 2023. Associa-
  tion for Computing Machinery. ISBN 9798400700262.
  doi: 10.1145/3573105.3575688. URL https://doi.
  org/10.1145/3573105.3575688.

Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,
 M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.

                                                                10
                       LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

A. False-positives with library search tactics
The apply? tactic8 is intended for searching the Lean library for lemmas applicable in the current context during interactive
proof construction, similar to exact? and rw?. However, the apply? tactic must not be left in a final proof, as it has the
same semantics as the sorry keyword, leaving such a proof incomplete.
For example, the proofs of putnam 2005 a4 and putnam 2007 b4 presented by DeepSeek-Prover-V2 (Ren et al.,
2025) utilize the apply? tactic and are thus incorrect. This highlights the potential of reinforcement learning to exploit
unchecked ambiguities in a proving environment. It also hints as to why a smaller DeepSeek-Prover-V2-7B model beat
DeepSeek-Prover-V2-671B in some contexts related to cardinal numbers, as the former might have learned to exploit the
apply? tactic while the latter did not (cf. Section Skill Discovery by Reinforcement Learning in Ren et al. (2025)).
In LeanTree, we prevent such errors by banning the usage of apply? by default, leaving it as opt-in for users who explicitly
want to integrate it into their proving system.

B. Incremental proof verification
Originally, the Lean REPL did not utilize the Lean verification kernel to type-check assignments introduced by tactic
applications, leading to incorrect proofs being accepted in some cases. Our prover managed to exploit these inconsistencies,
finding 12 incorrect proofs in the MiniF2F validation set that passed verification in the REPL when using the tactic mode.
One of these incorrect proofs is listed below.

theorem mathd_algebra_422 (x : R) (σ : Equiv R R) (h0 : ∀ x, σ.1 x = 5 * x - 12)
    (h1 : σ.1 (x + 1) = σ.2 x) : x = 47 / 24 := by
  rw [h0 ] at h1
  by_contra! h
  apply h.symm
  simpa using h _

Lean correctly rejects the above proof with the error: “don’t know how to synthesize placeholder”. However, when executing
the proof in the tactic mode using the old version of Lean REPL, the proof passes as correct.
In a recent update,9 Lean REPL was extended to type-check the full proof term after each tactic application, mitigating all
false positives in the verification process, at the cost of introducing some drawbacks detailed below. We propose a different
strategy: Instead of verifying the type-correctness of the whole proof term, type-check only the new assignments introduced
by a tactic application.
To illustrate this difference, assume that we are searching for a proof of type T and have already constructed a term t : T
which still contains unassigned metavariables of types G1 , . . . , Gn . Next, assume that we apply a tactic assigning terms
g1 : G1 , . . . , gn : Gn to the metavariables in t. The current strategy of Lean REPL is to type-check the whole assignment
t : T , which contains the new terms g1 , . . . , gn as subterms.
This leads to issues when the proof bifurcates into two branches. For example, consider applying the tactic have k :=
sorry in the REPL’s tactic mode.10 This corresponds to the assignment of the term ((fun k 7→ ? ) sorry) to the
metavariable corresponding to the main goal, where ? is a new unassigned metavariable. Lean REPL then enables solving
the ? and sorry parts independently. However, assignments made in one of these two branches are not propagated to
the other one, meaning that, from the perspective of each branch, the root proof term will always contain at least one hole
introduced by an unassigned metavariable or the sorry keyword. This leads to the kernel always failing during a type
check for the duration of this proof. The end effect is that the current verification strategy leads to false negatives when the
proof being verified contains at least one syntactic branching.
In contrast, the proposed strategy implemented in LeanTree type-checks only the new assignments g1 : G1 , . . . , gn : Gn
introduced by a tactic application. The type correctness of the whole proof term t : T then follows transitively. Most
importantly, this new verification strategy mitigates the false negatives described in the previous paragraph. Additionally,
   8
     https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference/#apply___
   9
     Published on GitHub on Apr 10, 2025.
  10
     This is the standard way to use the have tactic in the REPL – see for example https://github.com/
leanprover-community/repl/blob/master/test/have_by_sorry.in


                                                              11
                      LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

the new strategy also decreases the time complexity of verifying a proof from quadratic to linear since each sub-assignment
is only verified once.
Note that all proofs found by our prover are independently verified directly using Lean, bypassing Lean REPL together with
the new verification algorithm described in this section.

C. Experiments setup
In all experiments, we prompt the Llema-7B model using the following prompt.

   Complete the given Lean 4 code.
   Directly output the completed Lean 4 code without any additional text,
   comments, or reasoning.

When performing linear rollouts, we manually select only the first tactic from the model output.
During generation, we disable sampling of the sorry and admit keywords, together with syntax for comment sections.




                                                            12
                       LeanTree: Accelerating White-Box Proof Search with Factorized States in Lean 4

 D. Dataset schema
 The dataset is distributed in two files corresponding to the two data sources:

     • lean-trees mathlib.jsonl

     • lean-trees deepseek-prover-v1.jsonl

 Both of these files share the following unified schema.

 1   <sample> ::= {
 2     "path": <string>,
 3     "imports": [<string>],
 4     "theorems": [<error> | {
 5        "span": <span>,
 6        "name": <string?>,
 7        "context": [<string>],
 8        "by_blocks": [{
 9           "tree": <error> | {
10             "root": <proof_node>
11           }
12        }]
13     }]
14   }
15
16   <proof_node> ::= {
17     "id": <string>,
18     "proof_size": <int>,
19     "proof_depth": <int>,
20     "tactic": {
21       "tactic_string": <string>,
22       "span": <span>,
23       "children": [<string>],
24       "tactic_depends_on": [<string>]
25     }
26     "state": {
27       "goals": [{
28          "tag": <string?>,
29          "type": <string>,
30          "hypotheses": [{
31             "type": <string>,
32             "user_name": <string>,
33             "value": <string?>
34          }]
35       }]
36     }
37   }
38
39   <span> ::= {
40     "start": <int>,
41     "finish": <int>
42   }
43
44   <error> ::= {
45     "error": <string>
46   }




                                                              13
