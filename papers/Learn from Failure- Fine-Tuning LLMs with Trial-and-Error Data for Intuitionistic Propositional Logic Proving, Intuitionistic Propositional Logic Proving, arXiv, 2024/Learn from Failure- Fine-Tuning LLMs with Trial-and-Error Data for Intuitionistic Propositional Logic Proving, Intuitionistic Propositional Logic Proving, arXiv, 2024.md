                                             Learn from Failure: Fine-Tuning LLMs with Trial-and-Error Data for
                                                          Intuitionistic Propositional Logic Proving

                                                     Chenyang An1 * , Zhibo Chen2 * , Qihao Ye1 , Emily First1 , Letian Peng1
                                                         Jiayun Zhang1 , Zihan Wang1† , Sorin Lerner1† , Jingbo Shang1†
                                                         University of California, San Diego1 Carnegie Mellon University2
                                                 {c5an, q8ye, emfirst, lepeng, jiz069, ziw224, lerner, jshang}@ucsd.edu
                                                                              zhiboc@andrew.cmu.edu


                                                                    Abstract                                                                              Conventional Method
                                                                                                                                                                             0        tactic 2: 0.3
                                                                                                                                                                                      tactic 3: 0.1
                                                                                                             k   state k after Lean call     tactic
                                                 Recent advances in Automated Theorem Prov-                  ?   state waiting for Lean call                            1         ?
                                                                                                                                                                                      unchanged
                                                 ing have shown the effectiveness of leveraging
                                                                                                                                                                   …
                                                 a (large) language model that generates tactics             tactic 1: 0.6
                                                                                                                                  0
                                                                                                                                                      0
                                                                                                                                                                tactic 2 is then selected.
arXiv:2404.07382v3 [cs.AI] 29 Jul 2024




                                                                                                             tactic 2: 0.3
                                                 (i.e. proof steps) to search through proof states.          tactic 3: 0.1                    1           TrialMaster                 tactic 2: 0.2
                                                                                                                             ?                                               0
                                                 The current model, while trained solely on suc-                                          …
                                                                                                                                                                                      tactic 3: 0.8
                                                                                                                                                                        1         ?      updated
                                                 cessful proof paths, faces a discrepancy at the            LLM generates tactics;
                                                                                                            tactic 1 is selected first.   backtrack                 …
                                                 inference stage, as it must sample and try vari-
                                                                                                                                                             LLM generates tactics with all
                                                 ous tactics at each proof state until finding suc-                                                       history paths including backtracking.
                                                                                                                                                                 tactic 3 is then selected.
                                                 cess, unlike its training which does not incorpo-
                                                 rate learning from failed attempts. Intuitively, a         Figure 1: A simple example for how learning trial-and-
                                                 tactic that leads to a failed search path would in-        error data impacts inference distribution. See Figure 4
                                                 dicate that similar tactics should receive less at-        for a concrete case.
                                                 tention during the following trials. In this paper,
                                                 we demonstrate the benefit of training models
                                                 that additionally learn from failed search paths.          step, or tactics. The neural models utilize different
                                                 Facing the lack of such trial-and-error data in            architectures like LSTMs (Sekiyama et al., 2017),
                                                 existing open-source theorem-proving datasets,             CNNs (Irving et al., 2016), DNNs (Sekiyama and
                                                 we curate a dataset on intuitionistic proposi-             Suenaga, 2018), GNNs (Bansal et al., 2019; Wang
                                                 tional logic theorems and formalize it in Lean,
                                                                                                            et al., 2017) and RNNs (Wang and Deng, 2020),
                                                 such that we can reliably check the correct-
                                                 ness of proofs. We compare our model trained               though most recent work has begun to explore the
                                                 on relatively short trial-and-error information            use of transformer-based large language models
                                                 (T RIAL M ASTER) with models trained only on               (LLMs) due to their emerging reasoning abilities.
                                                 the correct paths and discover that the former                An interactive proof assistant, such as
                                                 solves more unseen theorems with lower trial               Lean (de Moura et al., 2015), Coq (Barras
                                                 searches.                                                  et al., 1997) or Isabelle (Nipkow et al., 2002),
                                                                                                            evaluates the model’s predicted candidate proof
                                         1       Introduction
                                                                                                            steps, returning either new proof states or errors.
                                         Automated Theorem Proving is a challenging task                    Neural theorem provers iterate on this procedure,
                                         that has recently gained popularity in the machine-                performing proof search, e.g., a depth-first search
                                         learning community. Researchers build neural the-                  (DFS), to traverse the space of possible proofs.
                                         orem provers to synthesize formal proofs of mathe-                 An example of a DFS proof search is illustrated
                                         matical theorems (Yang et al., 2023; Welleck et al.,               in Figure 2a, where the prover progressively
                                         2021; Lample et al., 2022; Mikuła et al., 2023;                    generates new tactics if the attempted tactics result
                                         Wang et al., 2023; Bansal et al., 2019; Davies                     in incorrect proofs.
                                         et al., 2021; Wu et al., 2021; Rabe et al., 2020;                     Such provers are usually trained on a dataset con-
                                         Kusumoto et al., 2018; Bansal et al., 2019; Irving                 taining only the correct proof paths. This, however,
                                         et al., 2016). Typically, a neural theorem prover,                 presents a limitation: during inference, the prover
                                         given a partial proof and the current proof state,                 does not have the ability to leverage the already
                                         uses a neural model to predict the next likely proof               failed paths it explored. Such failure information,
                                             *    The first two authors contributed equally to this work.   intuitively, is beneficial, as it could suggest the
                                             †
                                                  Corresponding authors.                                    model to generate tactics similar to the failed ones
sparingly. At the very least, the failure informa-                intro h1 #this is step 1
tion should help the model easily avoid generating                apply or.inr #this is step 2
                                                                  no solution, backtrack to step 1
already failed tactics. See Figure 1.                             apply or.inl
   In this paper, we wish to empirically verify this              exact h1
intuition. To conduct the experiment, we would
                                                             Note that "no solution, backtrack to step 1" is
compare the conventional model trained on correct
                                                         not a tactic in Lean. It simply tells the system to
proof paths, and T RIAL M ASTER, the model trained
                                                         backtrack to step 2 and start reasoning from there.
on the whole proof tree, containing both correct
                                                             Specifically, our PropL dataset is created through
paths and incorrect paths. See Figure 2b. As such,
                                                         a two-stage process that first involves generating
T RIAL M ASTER can make predictions based on the
                                                         a comprehensive set of propositional logic theo-
failure information during inference time.
                                                         rems by uniformly sampling from all possible theo-
   Since current open-source Automated Theorem
                                                         rems, utilizing a bijection between natural numbers
Proving datasets do not contain complete proof
                                                         and propositions to ensure representativeness. Fol-
trees, we create such a dataset, PropL, written in
                                                         lowing theorem generation, proofs are constructed
Lean. We focus on theorems of intuitionistic propo-
                                                         using a focusing method with polarization, in-
sitional logic. A propositional logic formula in in-
                                                         corporating a detailed trial-and-error search pro-
tuitionistic propositional logic A is true if and only
                                                         cess that includes both successful and backtracked
if ⊢ A has a derivation according to the rules of the
                                                         steps, thereby capturing the complexity and nu-
intuitionistic propositional logic. These rules are
                                                         ances of theorem proving in intuitionistic proposi-
listed in Figure 6 in Appendix A with explanations.
                                                         tional logic. Thus, our dataset is complete, scalable,
This is to be distinguished from the classical logic,
                                                         and representative. The proofs in our dataset are
where a theorem of classical propositional logic
                                                         combined with trial-and-error information, which
admits a proof if and only if under all truth value
                                                         is generated by the Focused Proof Search (FPS)
assignments to all propositions that appear in the
                                                         algorithm (McLaughlin and Pfenning, 2009; Liang
theorem, the theorem statement is evaluated to be
                                                         and Miller, 2009; Pfenning, 2017).
true.
                                                             We verify the effectiveness of incorporating the
   We give two elementary examples of theorems of
                                                         failed trials during training and inference by exper-
intuitionistic propositional logic with proofs. We
                                                         iments on PropL, observing that T RIAL M ASTER
then give an example of a theorem whose proof
                                                         achieves a higher proof search success rate and
contains a backtracking step. The first theorem
                                                         lower search cost over conventional model trained
admits a proof, where as the second doesn’t.
                                                         on correct proof paths. Our experiments further
     theorem_1 thm : p1 → p1 ∨ p2 := by                  indicate that our model can perform backtracking
         intro h1
         apply or.inl                                    without help from an external system.
         exact h1                                            Our main contributions are as follows:
                                                         • We establish, PropL, a complete, scalable, and
   The first theorem states that p1 implies p1 ∨ p2,
                                                            representative benchmark for intuitionistic propo-
where ∨ stands for "or". To show this, we assume
                                                            sitional logic theorems formalized in Lean.
p1 and prove either p1 or p2. We prove p1 in this
                                                            PropL includes proofs with trial-and-error infor-
case. The last three lines are tactics (proof steps)
                                                            mation, generated by the FPS algorithm.
in Lean used to prove this fact.
                                                         • We demonstrate that for intuitionistic proposi-
   Our second example looks like the following.
                                                            tional logic theorem proving, incorporating trial-
     theorem_2 thm : p1 → p1 ∧ p2 := by                     and-error information into training and proving
   The second theorem states that p1 implies p1             outperforms a conventional model that is trained
and p2. There is no proof to this theorem. When             on correct proofs only.
we assume p1, we cannot show both p1 and p2.
   Proofs might include backtracking instructions.       2   Related Work
Here is another possible proof for theorem 1. After      Automated Theorem Proving. Automated The-
step 2, there is no possible proof step that can lead    orem Proving has evolved significantly since its
to final solution. Therefore we backtrack to step 1      inception, focusing mainly on developing com-
and try a different proof step.                          puter programs that can autonomously prove math-
     theorem_1 thm : p1 → p1 ∨ p2 := by                  ematical theorems. Early ATP systems (mechan-
                                                                                                                                                        LLM Fine-Tuning
LLM Fine-Tuning          DFS Inference
                                                                                                                                                                                                                    predicted proof        compute          state 0; tactic 1; state        ground truth
      theorem                k    state k by calling Lean                        tactic generated by LLM                                                                           theorem                           (e.g., state 0;         loss           1; tactic 2; state 2;                            0
   (i.e., state 0)           ?    waiting to call Lean                           backtrack to the last valid parent state                                                                            LLM                                                    backtrack to state 0;
                                                                                                                                                                                (i.e., state 0)                       tactic 1; …;                                                                   1               3
                                                                                                                                                                                                                        state 4)                            tactic 3; state 3; tactic
                                          0                        0                                 0                       0                 0                                                                                                                                             2               4
                                                                                                                                                                                                                                                            4; state 4.
         LLM                      1           ?            1            ?                    1           ?           1            6       1         6

                             2        ?                2       ?                         2       ?               2       5            2       5 7
                                                                                                                                                                                  k    state k     tactic       backtrack          0                        0                     0                              0
  predicted proof                                  3       ?                         3       4               3       4            3       4
(e.g., state 0; tactic                                                                                                                                                                                      0                  1                        1                     1       3                  1               3
   1; …; state 7)                                                                                                                                                                                     1                    2                     2                                               2               4




                                                                                                                                                        TrialMaster Inference
                                                                       state 0; tactic 1;                                                                                          0                                                                                      2
                                 state 0; tactic 1;
             compute             state 1; tactic 2;                    state 1; tactic 2;                            state 0; tactic 6;
               loss                   state 2                               state 2                                       state 6                                                                                                                           state 0; …; state
                                                                                                                                                                                                          state 0; tactic 1;       state 0; tactic 1;        2; backtrack to              state 0; …;
                                                                                     no LLM                                                                                             state 0
      state 0;                                                                                                                                                                                                 state 1             tactic 2; state 2             state 0                     state 3
 tactic 6; state 6;                       LLM                               LLM execution                                        LLM
                                                                                     at this step
 tactic 7; state 7.                                                                                                                                                                      LLM                     LLM                     LLM                     LLM                        LLM
                                 tactic 3, tactic 4                tactic 3, tactic 4                                        tactic 7
             0
                                                                                                                                                                                        tactic 1                tactic 2               “backtrack               tactic 3                   tactic 4
         1       6                        Lean                              Lean                                             Lean                                                                                                      to state 0”
                                                                                                                                                                                         Lean                    Lean                                            Lean                       Lean
     2       7
                                 state 3: “error”                      state 4: “error”                          state 7: “complete”
   proof tree of a                                                                                                                                                                                                                                              state 3               state 4: “complete”
  training sample        …                step 3                                                             …           last step                                                      state 1                 state 2
                                                                            step 4

             (a) Conventional system with depth-first search                                                                                                                                 (b) Our training and inference methodology

Figure 2: Method comparison. (a) A conventional system: The tactic generator (i.e., LLM) is fine-tuned on correct
proof paths only. During inference, the trained tactic generator produces Nsampled (e.g., 2 in the example) tactics at a
time. If Lean decides that the current tactic is wrong, the system backtracks to the last valid state and tries other
candidate tactics. (b) Our methodology: The tactic generator is fine-tuned on proofs with trial-and-error. During
inference, we take the first tactic it generates and feed that into Lean for state checking at each step.


ical theorem proving) were based on first-order                                                                                                         Theorist (Crevier, 1993; McCorduck, 2004; Rus-
logic (Clocksin and Mellish, 2003; Chang and Lee,                                                                                                       sell and Norvig, 2010) and Gilmore’s program
2014), where the resolution method (Robinson,                                                                                                           (Davis, 2001; Gilmore, 1960). These systems
1965) played a crucial role. Recent progress in                                                                                                         laid the groundwork for the resolution of propo-
Automated Theorem Proving has been marked by                                                                                                            sitional logic problems, showcasing the ability of
the integration of machine learning (Bansal et al.,                                                                                                     automated systems to handle logical reasoning
2019; Davies et al., 2021; Wagner, 2021), espe-                                                                                                         tasks. Recent advancements in Automated The-
cially LLMs (Yang et al., 2023; Polu and Sutskever,                                                                                                     orem Proving have revisited propositional logic
2020; Han et al., 2021; Welleck et al., 2021; Jiang                                                                                                     problems, integrating modern computational tech-
et al., 2022), and heuristic methods (Holden and                                                                                                        niques. Sekiyama et al. (Sekiyama and Sue-
Korovin, 2021), aimed at amplifying the efficiency                                                                                                      naga, 2018) have employed Deep Neural Net-
and capacity of Automated Theorem Proving sys-                                                                                                          works (DNNs) as a statistical approach to gener-
tems. Within the domain of LLMs, formal math-                                                                                                           ate proofs for these theorems, while Kusumoto et
ematical languages like Metamath (Megill and                                                                                                            al. (Kusumoto et al., 2018) have explored graph
Wheeler, 2019), Lean (de Moura et al., 2015), Is-                                                                                                       representations coupled with reinforcement learn-
abelle (Nipkow et al., 2002), and Coq (Barras et al.,                                                                                                   ing to find proofs. Furthermore, sequence-to-
1997), serve as a bridge, enabling the precise ex-                                                                                                      sequence neural networks have been applied for
pression and verification of mathematical theorems                                                                                                      deriving proof terms in intuitionistic propositional
and concepts through a computer-verifiable for-                                                                                                         logic (Sekiyama et al., 2017). This area of research
mat, thereby mitigating hallucination risks (Nawaz                                                                                                      is particularly intriguing due to the simplicity and
et al., 2019). COPRA incorporates backtracking                                                                                                          importance of propositional logic in mathematics,
information into a prompt and sends the prompt                                                                                                          and there is a growing interest in evaluating the
to GPT-4 without fine-tuning it to perform proof                                                                                                        capability of LLMs in tackling this specific mathe-
search (Thakur et al., 2023). Baldur fine-tunes                                                                                                         matical domain.
LLMs with proofs and error information given by                                                                                                         Trial-and-Error.           The Chain-of-Thought
the proof assistant (First et al., 2023). In contrast,                                                                                                  (CoT) (Wei et al., 2022; Wang et al., 2022; Zhou
our work focuses on fine-tuning LLMs with the                                                                                                           et al., 2022; Fu et al., 2022; Chu et al., 2023; Yu
complete past proof history without using the error                                                                                                     et al., 2023) approach demonstrates that LLMs
message from the proof assistant.                                                                                                                       can be guided to perform step-by-step reasoning
Propositional Logic Problem. Early implemen-                                                                                                            by incorporating intermediate reasoning steps in
tations of ATP systems demonstrated the poten-                                                                                                          their prompts. This concept is expanded in later
tial for computers to automate logical deduc-                                                                                                           research, such as the Tree of Thoughts (ToT) (Yao
tions, with notable examples including the Logic                                                                                                        et al., 2023), which organizes reasoning into a tree
structure, and the Graph of Thoughts (GoT) (Besta               ((#! ∨ #" ) → &) → ((#! → &) ∧ (#" → &))
et al., 2023), which adopts a graph format for
thought structuring. Trial-and-error complements
                                                                                          tree representation
structured reasoning by allowing the model to                                        →             of theorem
empirically test hypotheses generated, thereby
                                                                           →                      ∧
refining its reasoning process based on feedback
from interactions or emulations. The Boosting of                      ∨          &        →                →
Thoughts (BoT) (Chen et al., 2024) prompting
framework iteratively explores and evaluates                     #!       #"         #!       &       #"       &
multiple trees of thoughts to gain trial-and-error
reasoning experiences, using error analysis from                      encoding                    decoding
the LLMs to revise the prompt. Lyra introduces                                 ID: 760387005
correction mechanisms to improve the performance
of the tactic generator (Zheng et al., 2023).           Figure 3: An illustration of the bijection between a
                                                        proposition and a natural number, where gray nodes
                                                        are leaf nodes. ID is computed using Algorithm 1 with
3     PropL: A New Dataset for Intuitionistic
                                                        n = 6 and p = 2 in this case.
      Propositional Logic Theorems in Lean
Our aim is to experimentally validate that trial-       Theorem Generation. Consider the set of proposi-
and-error information can enhance models’ abil-         tions A with at most p atomic propositions. A can
ity to do backtracking and tactic generation for        be inductively generated by the following gram-
theorem-proving tasks. Given that existing open-        mar:
source theorem proving datasets lack information
on trial-and-error processes, we have developed          A, B ::= Pi | T | F | A ∧ B | A ∨ B | A → B,
PropL, which is based on theorems of intuitionistic
propositional logic. This dataset uniquely includes     where Pi is the i-th atomic proposition with 1 ≤
proofs that encapsulate the complete search pro-        i ≤ p, T stands for True, and F stands for False.
cess, incorporating the trial-and-error data gener-     We note that an atomic proposition is just a state-
ated by the FPS algorithm. Our dataset has two          ment like "Today is sunny". The concrete meaning
other benefits. It is formalized in Lean, so that       of the statement is irrelevant with respect to the
the validity of the theorems and proofs are guaran-     theorem proving task in this paper. A connective
teed. The tactics generated by the model trained        ∧, ∨, → is called an internal node of the proposi-
on PropL can also be directly sent to Lean to be        tion. We assign the following lexicographic order
checked. PropL is also representative of all the        to propositions:
intuitionistic propositional logic theorems, since by     1. Number of internal nodes (increasing order)
uniformly sampling integers, we can use a bijec-          2. Number of internal nodes of the left child (de-
tion between natural numbers and propositions to              creasing order)
uniformly sample propositions. This bijection is          3. Top level connective, T < F < P1 < · · · <
explained in the Theorem Generation section.                  Pp < ∧ < ∨ <→
                                                          4. The (recursive order (2 - 5)) of the left child
3.1    Data Generation of PropL                           5. The (recursive order (2 - 5)) of the right child
PropL comprises theorems uniformly sampled              For a fixed upper bound p for the number of atomic
from the entire set of propositional logic theorems.    propositions, we establish a bijection between the
It includes various proof types for each theorem.       natural numbers and the set of propositional logic
We only report proof types that are used in this        formulas. The counting can be made efficient using
paper. For additional information about the dataset,    the Catalan Numbers (Atkinson and Sack, 1992).
please refer to the GitHub repository and Hugging-      Figure 3 gives an example of mapping between
face.                                                   propositions and natural numbers. Details about
   The construction of PropL involves two primary       the encoding and decoding algorithms are provided
stages: the generation of propositional logic theo-     in Appendix B.
rems and the generation of proofs for these theo-       Proof Generation. Given a randomly sampled the-
rems from an existing algorithm.                        orem, the proof of the theorem is constructed using
                                                                 Without Backtracking               With Backtracking
the focusing method with polarization (McLaugh-
                                                                       Initial State                      Initial State
lin and Pfenning, 2009; Liang and Miller, 2009;                         ⊢ p2 → p 3 ∨ p2                   ⊢ p2 → p3 ∨ p2
Pfenning, 2017). Proof search is divided into two                    Intro: h1                         Intro h1
stages: inversion and chaining. The inversion phase                       State 1          backtrack         State 1
                                                                                                          h1 : p2 ⊢ p3 ∨ p2
                                                                       h1 : p2 ⊢ p3 ∨ p2
mechanically breaks down negative connectives




                                                       Tactics
                                                                  Apply Or.inr                    Apply Or.inl
(e.g. implications) in the goal and positive con-                                                           State 2
                                                                          State 2
nectives (e.g. disjunctions) in the premises. After                       h1 : p2 ⊢ p2                     h1 : p2 ⊢ p3       Apply Or.inr

inversion, chaining will pick an implication in the                  Exact h1
                                                                                                             State 3
premise or show one of the disjuncts in the conclu-                       State 3                           h1 : p2 ⊢ p2
                                                                          Complete
                                                                                                       Exact h1
sion, with backtracking. The proof search proce-
                                                                                                             State 4
dure terminates when the same atomic proposition                                                             Complete
appears in both the premise and the conclusion. An
example of proofs with trial-and-error information     Figure 4: Two proofs for one propositional logic theo-
(backtracking) and with trial-and-error information    rem with tactics and states in Lean.
removed are shown in Figure 4.
   Once proofs are generated, we use them to fine-     in general.
tune models and start the proof search on the test        We first apply our deterministic algorithms to
set.                                                   generate the proofs of the 200,000 theorems, and
   The polarization of the connectives affects the     then remove the trial-and-error information of those
behavior of the inversion and the search procedure.    proofs. We get a word-length distribution of those
We choose to uniformly polarize conjunctions that      proofs without trial-and-error information. Next, to
occur negatively (e.g. on the right-hand side of       ensure the diversity of the trial-and-error informa-
an arrow) as negative and polarize conjunctions        tion, we randomly select propositions to focus on
that occur positively (e.g. on the left-hand side      during the chaining phase of the proof search, and
of an arrow) as positive. Atomic propositions are      then generate 10 different proofs with backtrack-
assigned polarities based on the connective that       ing. By using the average length of the 10 different
they first appear under.                               proofs, we have another word length distribution
   To improve the runtime of the search procedure,     of proofs with trial-and-error information.
we make an additional assumption that once an             We then split the 200,000 theorems into training
implication is picked, the implication cannot be       and test sets based on both of the word length distri-
used to show its premise. In theory, this introduces   butions mentioned above. The word lengths of the
incompleteness into the search procedure, but it       proofs of the training data theorems fall within the
only affects 1 theorem out of around 1000 provable     lower 0.66 quantile of the two distributions of the
theorems randomly sampled.                             word length of all the proofs of the 200,000 theo-
3.2   Construction of Training and Test Sets           rems (109,887 in total). The word lengths of the in-
                                                       distribution test set also fall in that category (1000
In this section, we explain how we construct the       in total). The word lengths of the proofs among
datasets for training and evaluation. We want to       the out-of-distribution test theorems are above 0.8
avoid training and testing on similar data. In order   quantile (1000 total) of the two distributions of
to test the model performance on harder out-of-        the word lengths of all the proofs of the 200,000
distribution (OOD) tasks, we need to ensure that       theorems. We note that the baseline model and
the lengths of the proofs in the training data are     T RIAL M ASTER are trained on proofs of the same
shorter than the lengths of the proofs in the test     set of theorems.
data.
   Given PropL, we fix the number of internal          4          Methodology
nodes in the theorem statement to be 16 (explained
in the dataset generation section). We then uni-       4.1          LLM Fine-Tuning
formly randomly sample 200,000 theorems from           We utilize the training set formed in PropL for train-
PropL, which can be achieved by using the integer-     ing both T RIAL M ASTER and the tactic generator
theorem bijection as explained before. Our method      in the DFS system. The numbers of theorems used
ensures that the theorems we study in this paper are   in the training and test datasets are presented in
representative of the propositional logic theorems     Table 1.
Table 1: The scale of training and test split in our PropL   is repeated until Lean identifies that the proof is
dataset.                                                     complete or any Lean error occurs. We also note
                                                             that T RIAL M ASTER only outputs one tactic at each
      Subset                  Number of theorems             state using greedy search.
      Training set                   109,887                 Inference method of the DFS system. There are
      In-dist. test set               1,000                  two hyperparameters in the DFS system: tempera-
      Out-of-dist. test set           1,000                  ture t and the number of sampled tactics Nsampled .
                                                             The temperature t decides the diversity of the
                                                             model outputs. As t increases, the outputs of the
LLM fine-tuning with trial-and-error. In our                 model become more varied. The second parameter
approach, we randomly select two out of the short-           determines how many tactics the tactic generator
est five among the ten proofs with trial-and-error           of the DFS system produces for a new proof state.
information for each theorem in the training set                During inference, the LLM in the DFS system
and utilize them to train T RIAL M ASTER. Refer to           produces Nsampled of candidate tactics at each new
Figure 2b for a description of this training process.        state. For each proof state, the DFS only makes
LLM fine-tuning in a DFS system. For the tactic              one inference. If any two of the generated tactics
generator of the DFS system, we employ the deter-            for the same state are the same, we remove one
ministic FPS algorithm to generate the proofs of             of them to ensure efficiency. We also remove the
the theorems in the training set. The trial-and-error        tactic suggestions that fail to follow the grammar of
information is removed from the proofs. The LLM              Lean. The system follows the depth-first order to
is then fine-tuned on the proofs without trial-and-          keep trying untried tactics. If the system exhausts
error information as the conventional methods do.            all the tactics for a given state but has not found a
Figure 2a illustrates the training process of the DFS        valid one, the system returns to the parent state and
system.                                                      then keeps trying untried tactics for the parent state.
                                                             The overview is presented in the Figure 2a.
4.2     Inference
                                                                To fully exploit the ability of the DFS system, we
Inference method of model trained with trial-                varied the parameters of it, such as temperature and
and-error. T RIAL M ASTER conducts inference on              the number of sampled tactics. We count how many
itself without any help from a backtracking system           times Lean has been called to check tactics for both
like DFS or BFS. It outputs two kinds of tactics:            the DFS system and T RIAL M ASTER during the
tactics in Lean and backtrack instructions. An ex-           inference stage.
ample of a backtrack instruction would be like “no
solution, return to state 2 [that leads to state 4]”,        Why do we choose DFS over BFS? While the
where state 4 is the current state. When T RIAL -            breadth-first-search (BFS) system is also popular
M ASTER is doing a proof search on the test set, it          for building neural provers in Automated Theorem
is prompted with all history paths, including previ-         Proving, we have opted for DFS as our baseline
ous tactics, states, the backtracking it made before,        over BFS in the context of propositional logic the-
and the failed search path. It then outputs the en-          orem proving. This is due to the finite number
tire proof path after. Nonetheless, we only utilize          (around 20) of tactics available at any step for the
the first tactic in the output and employ Lean as            search process of intuitionistic propositional logic
a calculator to determine the next state, thereby            theorems, making DFS more efficient than BFS
ensuring the correctness of the state following the          without compromising the success rate.
tactic. If the tactic outputted by T RIAL M ASTER
is a backtrack instruction, it is then prompted with         5     Evaluation
all the proof search history including the backtrack
                                                             5.1    Experimental Setup
instruction and the state that the backtrack instruc-
tion says to return to. If that tactic is not a back-        Base LLM. We used Llama-2-7b-hf (Touvron
track instruction, the tactic and the current state          et al., 2023) as the backbone LLM for tactic gener-
will be fed into Lean for producing the state after.         ation. Models are trained on two A100 GPUs for
T RIAL M ASTER is then prompted with the entire              a single epoch with batch size set to 4. Hugging-
proof tree including the state that Lean calculated,         face (Wolf et al., 2019) is used for fine-tuning the
and it should output a tactic again. This process            models, and VLLM (Kwon et al., 2023) is used for
inference of the models for efficiency. The learning     Table 2: Performance on in-distribution task. Both
rate of all training processes is set to be 2 × 10−5 .   methods perform well for propositional logic.

Hyperparameters.          In the experiment, we                          Model                 Success Rate
vary temperature t from {0.3, 0.7, 1.2, 1.5, 2.0}                    T RIAL M ASTER               100%
and number of sampled tactics Nsampled from
                                                                               Nsampled = 2       99.5%
{2, 5, 10, 15, 20}. We notice that in all experiments                          Nsampled = 5       99.9%
                                                                     t = 1.2
for temperature t less than 1.5, there were only very                          Nsampled = 10      99.6%
                                                               DFS
few (less than 15) theorems that were still under                              Nsampled = 2       75.9%
search when the total steps for that search attempt                  t = 2.0   Nsampled = 5       97.3%
                                                                               Nsampled = 10      99.0%
reached 65. For t higher than 1.5, NLean starts
to increase dramatically. At temperature 2 with
Nsampled =20, NLean climbs up to 32,171 when the         5.3   Results and Analysis
number of total steps reaches 65. Therefore, in our
experiment, we set 65 as the search step limit to        T RIAL M ASTER outperforms conventional DFS
control time complexity.                                 system. We begin by evaluating the methods of
                                                         the in-distribution test set. Table 2 illustrates that
                                                         both our method and the DFS system perform ex-
5.2   Evaluation Metrics                                 ceptionally well, achieving a success rate of nearly
                                                         100% in most configurations. This suggests that
Proof search success rate. We use proof search           Llama-7b effectively masters in-distribution intu-
success rate as our primary metric, which repre-         itionistic propositional logic theorems. Then, we
sents the ratio of successful searches by the model.     compare the performance of the methods on the
A search attempt for a theorem is marked as suc-         out-of-distribution task. The results are presented
cessful if Lean outputs state “no goal, the proof        in Figure 5. Our method with trial-and-error signif-
is complete”, implying the theorem is effectively        icantly outperforms the DFS system across various
proved after applying a tactic produced by the           hyperparameter configurations. Additionally, we
model. For T RIAL M ASTER, a search attempt ends         observe that feeding more proofs without trial-and-
and fails immediately after one of the following         error for LLM fine-tuning does not further improve
conditions: 1) the word length of the proof tree         the performance.
with trial-and-error exceeds 1500 (for the sake of       Impact of hyperparameters in the DFS system.
context length of the model), or 2) the tactic pro-      As shown in Figure 5, on the OOD task, although
duced by the model at any step induces a Lean            the success rate of the DFS system gets higher
error. For the conventional DFS system, a search         when we increase the temperature t or the number
attempt fails when one of the following conditions       of sampled tactics Nsampled , the search cost (re-
happens: 1) the word length of the proof tree with-      flected by NLean ) also goes up. Specifically, when
out trial-and-error exceeds 1500, or 2) all tactics      we increase Nsampled , the DFS system explores a
generated for the initial states have been explored      larger pool of candidate tactics during the search,
and failed, or 3) the total search steps exceed 65       leading to a higher number of Lean calls. In con-
(see Section 5.1 for the choice of this value). We       trast, our method does a greedy search to generate
note that the 1500-word limit is stricter for our        only one tactic for each new state. Likewise, as
method since it produces entire proof paths includ-      t increases, the tactic generator of the DFS sys-
ing trial-and-error and thus would be easier to hit      tem tends to produce more diverse tactics at each
the limit.                                               proof state, improving the system’s performance
Search cost. We define a metric to assess the            but leading to higher search costs.
search cost—the total number of Lean calls for tac-      T RIAL M ASTER achieves high success rates at
tic checking during proof search for the entire test     lower search cost. For a direct comparison of
set, denoted as NLean . Given the same proof search      search costs, we plot the NLean values of our
success rate, a lower NLean indicates a more effi-       method alongside those of the top three DFS sys-
cient system for proof search. Note that backtrack-      tems with the highest success rates among all the
ing instructions from our method do not require          hyperparameters we experimented with, i.e., t=1.5,
applying Lean to check the state and, consequently       Nsampled =20 (87.2%), t=1.5, Nsampled = 10 (86.1%),
do not add search cost.                                  and t=1.8, Nsampled =10 (88.4%). This comparison
                1                                                                       1

                     17993                               31101                                17993
               0.9                                                                     0.9                                     17432
Success Rate




                                                                        Success Rate
                                                    19034                                                              17047
                                       16844                                                                  16844
                                                                                                  15462
               0.8           14515                                                     0.8

                       12749                                                                   13167
               0.7                                                                     0.7
                                                     TrialMaster                                                            TrialMaster
                                                     DFS                                                                    DFS
               0.6                                                                     0.6
                       0       0.5       1         1.5           2                            0           5      10      15        20
                                     Temperature                                                       # of Sampled Tactic

                             (a) Temperature t                                               (b) Sampled Tactics Nsampled                          (c) Search Cost

Figure 5: Experiment results on OOD task. (a) We fix Nsampled = 10 to see the impact of temperature on the DFS
system. (b) We fix t = 1.2 to see the impact of the number of sampled tactics. The number of Lean calls is noted
beside the marker. (c) Comparison of NLean among our method and top 3 DFS systems with the highest success rate.
In summary, training with trial-and-error achieves a higher success rate with a relatively lower search cost compared
to the DFS systems.


Table 3: Ablation study: Comparison of T RIAL M AS -                                                                  failed search paths (we don’t compute the loss for
TER and model trained without trial-and-error informa-
                                                                                                                      the failed search paths during the training stage in
tion on OOD task
                                                                                                                      this case). The proof success rate in this case is
                                                                                                                      75.6%, which is lower than T RIAL M ASTER’s proof
                      Model                                          Success rate
                                                                                                                      success rate of 88.7%. The NLean for the model
                      T RIAL M ASTER                                   88.7%                                          is 13,600, which is lower than that of T RIAL M AS -
                      Model - proof w/o t.a.e.                         59.3 %                                         TER . This is expected since the model does not
                                                                                                                      learn to predict failed search paths. Our explana-
                                                                                                                      tion for why T RIAL M ASTER has a higher proof
is illustrated in Figure 5c. Notably, we observe                                                                      search success rate than the model trained in the
that the DFS systems that closely approach our                                                                        previously mentioned experiment is that the failed
model’s performance exhibit significantly higher                                                                      search paths also contribute to improving the proof
search costs. With t=1.8, Nsampled =10, NLean of                                                                      search success rate of the model. T RIAL M ASTER
the DFS system, which has 0.3% lower success                                                                          strategically tried some potentially failed search
rate than our method, has reached 31,101, which is                                                                    paths to gain a more comprehensive view of the
72% higher than that of our method with trial-and-                                                                    problem, which then led to the correct search paths.
error. The high search cost makes the DFS system
with high temperatures unfavorable. These results
demonstrate that training with trial-and-error pro-
duces higher-quality tactics, achieving a higher suc-                                                                 5.4      Ablation Study
cess rate with relatively lower search cost.
Model learns backtracking capability from trial-                                                                      To evaluate the effectiveness of training with trial-
and-error data. In the experiments, we find out                                                                       and-error, we craft an ablated version of our
that our T RIAL M ASTER successfully acquires the                                                                     method where the LLM is fined-tuned with data of
backtracking capability from proofs with trial-and-                                                                   the correct path only and do inference in the same
error information. This is evidenced by the fact                                                                      way as our method (i.e., producing one tactic at a
that during T RIAL M ASTER’s proof search for the-                                                                    time and applying Lean for state checking). We
orems in the test set, all backtracking instructions                                                                  denote the ablated version as Model - proof w/o
produced by the LLM adhere to the correct format                                                                      t.a.e.. For both methods, we mark the search at-
and point to existing state numbers.                                                                                  tempt as failed if the tactic induces a Lean error, or
Including failed search paths helps T RIAL M AS -                                                                     the search exceeds the 1500-word limit. The result
TER to learn. The following experiment shows                                                                          is shown in the Table 3. The difference between the
that adding failed search paths to the training data                                                                  success rates of the two models is 29.4%, which is
for T RIAL M ASTER results in an overall gain. In                                                                     significant. This clearly shows that failed search
this experiment, the model is only trained to learn                                                                   states and trial-and-error information tremendously
the correct search paths and the backtracking in-                                                                     enhance the model’s capability to solve theorem-
structions. The model is not trained to learn the                                                                     proving tasks.
Table 4: Comparison of models trained on different          A natural extension of our research involves in-
lengths of proofs with trial-and-error on OOD task.       vestigating whether trial-and-error information is
                                                          beneficial for more general mathematical theorem-
      Model                           Success rate        proving settings. Exploring this avenue could pro-
      Model - short proof w/ t.a.e.     88.7%             vide valuable insights into the effectiveness of our
      Model - long proof w/ t.a.e.      72.4 %            approach across broader mathematical domains.

                                                          Limitations
5.5      Exploratory Study: Effect of Training
                                                          One limitation of our study is that some proof at-
         Proof Length on Model Performance
                                                          tempts are forced to stop due to the prompt exceed-
Since the FPS algorithm of PropL dataset can gen-         ing the context length of 1500 tokens. This con-
erate multiple proofs with variable length, we con-       straint may potentially influence our results by trun-
duct an exploratory study to assess the impact of         cating the available information during the proof
proof length on model performance. We fine-tune           search process.
two models using proofs with different lengths of            Furthermore, our method was not evaluated on
trial-and-error information. For the first model,         general mathematical theorems. This limitation
which is our T RIAL M ASTER, the training data is         arises from both the scarcity of proofs containing
derived by randomly selecting two out of the short-       trial-and-error information in current math libraries
est four proofs from the ten available proofs for         and the intrinsic challenges associated with produc-
each theorem in PropL. We denote it as Model -            ing proofs, whether with or without backtracking,
short proof w/ t.a.e. In contrast, the training data      for general mathematical theorems in a formalized
of the second model is formed by randomly se-             setting.
lecting two proofs from the ten available for each           Automated theorem proving with LLMs is an
theorem, irrespective of their lengths. We denote         emerging area in machine learning. There is still
it as Model - long proof w/ t.a.e. For both mod-          a lack of baselines on LLMs to compare with our
els, we use greedy search to let them generate one        method. We establish a fundamental baseline, but
tactic for each state. We evaluate the models on          we still need accumulative work to provide meth-
our 1000 OOD test set. The results are shown in           ods for comparison.
the Table 4. A higher success rate is observed in
the model trained with shorter proofs. This can           Ethical Consideration
be attributed to the fact that as the proof with trial-
and-error information becomes longer, there is too        Our work learns large language models to automat-
much trial-and-error information that may detri-          ically prove propositional logic theorems, which
mentally affect the model’s performance, as too           generally does not raise ethical concerns.
many failed search paths may lower the quality of
the training data.                                        Acknowledgments
                                                          This work is supported by the National Science
6       Conclusion and Future Work
                                                          Foundation under grants CCF-1955457 and CCF-
In this paper, we study Automated Theorem Prov-           2220892. This work is also sponsored in part by
ing in formalized environments. We create a com-          NSF CAREER Award 2239440, NSF Proto-OKN
plete, scalable, and representative dataset of in-        Award 2333790, as well as generous gifts from
tuitionistic propositional logic theorems in Lean.        Google, Adobe, and Teradata.
We demonstrate that leveraging information from
failed search states and backtracking not only
teaches models how to backtrack effectively, but          References
also helps in developing better tactics than those        Michael D Atkinson and J-R Sack. 1992. Generating bi-
generated by models trained without access to               nary trees at random. Information Processing Letters,
backtracking insights. We release our datasets on           41(1):21–23.
GitHub and Huggingface.1                                  available at https://huggingface.co/KomeijiForce/
                                                          llama-2-7b-propositional-logic-prover.        Gener-
    1
    PropL dataset is available at https://huggingface.    ation codes for theorems and proofs are available at
co/datasets/KomeijiForce/PropL. Model weights are         https://github.com/ucsd-atp/PropL.
Kshitij Bansal, Christian Szegedy, Markus N Rabe,         Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark,
  Sarah M Loos, and Viktor Toman. 2019. Learning            and Tushar Khot. 2022. Complexity-based prompt-
  to reason in large theories without imitation. arXiv      ing for multi-step reasoning.    arXiv preprint
  preprint arXiv:1905.10501.                                arXiv:2210.00720.

Bruno Barras, Samuel Boutin, Cristina Cornes, Ju-         P. C. Gilmore. 1960. A proof method for quantification
  dicaël Courant, Jean-Christophe Filliatre, Eduardo         theory: Its justification and realization. IBM Journal
  Gimenez, Hugo Herbelin, Gerard Huet, Cesar Munoz,          of Research and Development, 4(1):28–35.
  Chetan Murthy, et al. 1997. The Coq proof assistant
  reference manual: Version 6.1. Ph.D. thesis, Inria.     Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W
                                                             Ayers, and Stanislas Polu. 2021. Proof artifact co-
Maciej Besta, Nils Blach, Ales Kubicek, Robert Ger-          training for theorem proving with language models.
 stenberger, Lukas Gianinazzi, Joanna Gajda, Tomasz          arXiv preprint arXiv:2102.06203.
 Lehmann, Michal Podstawski, Hubert Niewiadomski,         Edvard K Holden and Konstantin Korovin. 2021. Het-
 Piotr Nyczyk, et al. 2023. Graph of thoughts: Solv-        erogeneous heuristic optimisation and scheduling for
 ing elaborate problems with large language models.         first-order theorem proving. In International Con-
 arXiv preprint arXiv:2308.09687.                           ference on Intelligent Computer Mathematics, pages
                                                            107–123. Springer.
Chin-Liang Chang and Richard Char-Tung Lee. 2014.
  Symbolic logic and mechanical theorem proving.          Geoffrey Irving, Christian Szegedy, Alexander A Alemi,
  Academic press.                                           Niklas Eén, François Chollet, and Josef Urban. 2016.
                                                            Deepmath-deep sequence models for premise selec-
Sijia Chen, Baochun Li, and Di Niu. 2024. Boosting          tion. Advances in neural information processing
   of thoughts: Trial-and-error problem solving with        systems, 29.
   large language models. In The Twelfth International
   Conference on Learning Representations.                Albert Q Jiang, Sean Welleck, Jin Peng Zhou,
                                                            Wenda Li, Jiacheng Liu, Mateja Jamnik, Timo-
Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang         thée Lacroix, Yuhuai Wu, and Guillaume Lample.
  Yu, Tao He, Haotian Wang, Weihua Peng, Ming Liu,          2022. Draft, sketch, and prove: Guiding formal the-
  Bing Qin, and Ting Liu. 2023. A survey of chain of        orem provers with informal proofs. arXiv preprint
  thought reasoning: Advances, frontiers and future.        arXiv:2210.12283.
  arXiv preprint arXiv:2309.15402.
                                                          Mitsuru Kusumoto, Keisuke Yahata, and Masahiro
William F Clocksin and Christopher S Mellish. 2003.         Sakai. 2018. Automated theorem proving in intu-
 Programming in PROLOG. Springer Science & Busi-            itionistic propositional logic by deep reinforcement
  ness Media.                                               learning. arXiv preprint arXiv:1811.00796.

Daniel Crevier. 1993. AI: the tumultuous history of the   Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
  search for artificial intelligence. Basic Books, Inc.    Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gon-
                                                           zalez, Hao Zhang, and Ion Stoica. 2023. Efficient
Alex Davies, Petar Veličković, Lars Buesing, Sam         memory management for large language model serv-
  Blackwell, Daniel Zheng, Nenad Tomašev, Richard          ing with pagedattention. In Proceedings of the 29th
  Tanburn, Peter Battaglia, Charles Blundell, András       Symposium on Operating Systems Principles, pages
  Juhász, et al. 2021. Advancing mathematics by guid-      611–626.
  ing human intuition with AI. Nature, 600(7887):70–
                                                          Guillaume Lample, Timothee Lacroix, Marie-Anne
  74.
                                                            Lachaux, Aurelien Rodriguez, Amaury Hayat,
Martin Davis. 2001. The early history of automated          Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.
 deduction. Handbook of automated reasoning, 1:3–           2022. Hypertree proof search for neural theorem
 15.                                                        proving. Advances in Neural Information Processing
                                                            Systems, 35:26337–26349.
Leonardo de Moura, Soonho Kong, Jeremy Avigad,            Chuck C. Liang and Dale Miller. 2009. Focusing and
  Floris Van Doorn, and Jakob von Raumer. 2015. The         polarization in linear, intuitionistic, and classical log-
  lean theorem prover (system description). In Auto-        ics. Theor. Comput. Sci., 410(46):4747–4768.
  mated Deduction-CADE-25: 25th International Con-
  ference on Automated Deduction, Berlin, Germany,        Pamela McCorduck. 2004. Machines Who Think (2Nd
  August 1-7, 2015, Proceedings 25, pages 378–388.          Ed.). A. K. Peters.
  Springer.
                                                          Sean McLaughlin and Frank Pfenning. 2009. Efficient
Emily First, Markus Rabe, Talia Ringer, and Yuriy Brun.     intuitionistic theorem proving with the polarized in-
  2023. Baldur: Whole-proof generation and repair           verse method. In Automated Deduction - CADE-22,
  with large language models. In Proceedings of the         22nd International Conference on Automated Deduc-
  31st ACM Joint European Software Engineering Con-         tion, Montreal, Canada, August 2-7, 2009. Proceed-
  ference and Symposium on the Foundations of Soft-         ings, volume 5663 of Lecture Notes in Computer
  ware Engineering, pages 1229–1241.                        Science, pages 230–244. Springer.
Norman Megill and David A Wheeler. 2019. Metamath:           Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen,
  a computer language for mathematical proofs. Lulu.           Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun
  com.                                                         Li, Lin Li, et al. 2023. Dt-solver: Automated theo-
                                                               rem proving with dynamic-tree sampling guided by
Maciej Mikuła, Szymon Antoniak, Szymon                         proof-level value function. In Proceedings of the
 Tworkowski, Albert Qiaochu Jiang, Jin Peng                    61st Annual Meeting of the Association for Compu-
 Zhou, Christian Szegedy, Łukasz Kuciński, Piotr              tational Linguistics (Volume 1: Long Papers), pages
 Miłoś, and Yuhuai Wu. 2023. Magnushammer: A                  12632–12646.
 transformer-based approach to premise selection.
 arXiv preprint arXiv:2303.04488.                            Mingzhe Wang and Jia Deng. 2020. Learning to prove
                                                               theorems by learning to generate theorems. Advances
M Saqib Nawaz, Moin Malik, Yi Li, Meng Sun, and                in Neural Information Processing Systems, 33:18146–
  M Lali. 2019. A survey on theorem provers in formal         18157.
  methods. arXiv preprint arXiv:1912.03028.
                                                             Mingzhe Wang, Yihe Tang, Jian Wang, and Jia Deng.
Tobias Nipkow, Markus Wenzel, and Lawrence C Paul-             2017. Premise selection for theorem proving by deep
  son. 2002. Isabelle/HOL: a proof assistant for               graph embedding. Advances in neural information
  higher-order logic. Springer.                                processing systems, 30.

Frank Pfenning. 2017. Lecture notes on focusing.             Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,
                                                               Ed Chi, Sharan Narang, Aakanksha Chowdhery, and
Stanislas Polu and Ilya Sutskever. 2020. Generative            Denny Zhou. 2022. Self-consistency improves chain
   language modeling for automated theorem proving.            of thought reasoning in language models. arXiv
   arXiv preprint arXiv:2009.03393.                            preprint arXiv:2203.11171.

Markus N Rabe, Dennis Lee, Kshitij Bansal, and Chris-        Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
 tian Szegedy. 2020. Mathematical reasoning via                 Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
 self-supervised skip-tree training. arXiv preprint             et al. 2022. Chain-of-thought prompting elicits rea-
 arXiv:2006.04757.                                              soning in large language models. Advances in Neural
                                                                Information Processing Systems, 35:24824–24837.
John Alan Robinson. 1965. A machine-oriented logic
  based on the resolution principle. Journal of the          Sean Welleck, Jiacheng Liu, Ronan Le Bras, Hannaneh
  ACM (JACM), 12(1):23–41.                                     Hajishirzi, Yejin Choi, and Kyunghyun Cho. 2021.
                                                               Naturalproofs: Mathematical theorem proving in nat-
Stuart J Russell and Peter Norvig. 2010. Artificial intel-     ural language. arXiv preprint arXiv:2104.01112.
   ligence a modern approach. London.
                                                             Thomas Wolf, Lysandre Debut, Victor Sanh, Julien
Taro Sekiyama, Akifumi Imanishi, and Kohei Suenaga.            Chaumond, Clement Delangue, Anthony Moi, Pier-
  2017. Towards proof synthesis guided by neural               ric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz,
  machine translation for intuitionistic propositional         et al. 2019. Huggingface’s transformers: State-of-
  logic. corr abs/1706.06462 (2017). arXiv preprint            the-art natural language processing. arXiv preprint
  arXiv:1706.06462.                                            arXiv:1910.03771.

Taro Sekiyama and Kohei Suenaga. 2018. Automated             Minchao Wu, Michael Norrish, Christian Walder, and
  proof synthesis for propositional logic with deep neu-       Amir Dezfouli. 2021. Tacticzero: Learning to prove
  ral networks. arXiv preprint arXiv:1805.11799.               theorems from scratch with deep reinforcement learn-
                                                               ing. Advances in Neural Information Processing
Richard P Stanley. 2015. Catalan numbers. Cambridge            Systems, 34:9330–9342.
  University Press.
                                                             Kaiyu Yang, Aidan M Swope, Alex Gu, Rahul Chala-
Amitayush Thakur, Yeming Wen, and Swarat Chaud-                mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
 huri. 2023. A language-agent approach to formal               Prenger, and Anima Anandkumar. 2023. LeanDojo:
 theorem-proving. arXiv preprint arXiv:2310.04353.             Theorem Proving with Retrieval-Augmented Lan-
                                                               guage Models. arXiv preprint arXiv:2306.15626.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay             Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti           Thomas L Griffiths, Yuan Cao, and Karthik
  Bhosale, et al. 2023. Llama 2: Open founda-                  Narasimhan. 2023. Tree of thoughts: Deliberate
  tion and fine-tuned chat models. arXiv preprint              problem solving with large language models. arXiv
  arXiv:2307.09288.                                            preprint arXiv:2305.10601.

Adam Zsolt Wagner. 2021. Constructions in com-               Fei Yu, Hongbo Zhang, and Benyou Wang. 2023. Na-
  binatorics via neural networks. arXiv preprint               ture language reasoning, a survey. arXiv preprint
  arXiv:2104.14516.                                            arXiv:2303.14725.
Chuanyang Zheng, Haiming Wang, Enze Xie, Zhengy-
  ing Liu, Jiankai Sun, Huajian Xin, Jianhao Shen,
  Zhenguo Li, and Yu Li. 2023. Lyra: Orchestrating
  dual correction in automated theorem proving. arXiv
  preprint arXiv:2309.15806.
Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,
  Nathan Scales, Xuezhi Wang, Dale Schuurmans,
  Claire Cui, Olivier Bousquet, Quoc Le, et al. 2022.
  Least-to-most prompting enables complex reason-
  ing in large language models. arXiv preprint
  arXiv:2205.10625.
                                                        one-to-one mapping between propositions and nat-
               (Assumption)                 (T-I)       ural numbers. This bijection allows us to simply
    Γ, A ⊢ A                          Γ⊢T
                                                        sample from the natural numbers to ensure the
    Γ⊢F                  Γ⊢A          Γ⊢B               dataset exhibits uniformity.
           (F-E)                            (∧-I)
    Γ⊢A                     Γ⊢A∧B
                                                        Algorithm 1 Encoding
    Γ⊢A∧B                     Γ⊢A∧B                     Require: A tree T representing a proposition,
               (∧-E1)                     (∧-E2)            with n indicating the number of internal nodes
      Γ⊢A                       Γ⊢B
                                                            and p representing the number of atomic propo-
      Γ⊢A                       Γ⊢B                         sitions
                (∨-I1)                    (∨-I2)        Ensure: Output a natural number
    Γ⊢A∨B                     Γ⊢A∨B
                                                         1: return 3n (p + 2)n+1 × S HAPE N UMBER (T )
                                                            + A SSIGNMENT N UMBER(T )
    Γ⊢A∨B          Γ, A ⊢ C       Γ, B ⊢ C
                                             (∨-E)       2: function S HAPE N UMBER(T )
                    Γ⊢C                                  3:      if T is a single node then return 0
                                                         4:      end if
                   Γ, A ⊢ B                              5:      Tl , Tr ← left and right sub-trees of T
                              (→-I)
                Γ⊢A→B                                    6:      nl , nr ← number of internal nodes in
                                                            Tl , Tr       ▷PTotal nr + nl + 1 internal nodes
          Γ⊢A→B               Γ⊢A                        7:      return ni=1   l
                                                                                  Ci−1 Cnl +nr +1−i + Cnr ×
                                    (→-E)
                   Γ⊢B                                      S HAPE N UMBER(Tl ) + S HAPE N UMBER(Tr )
                                                         8: end function
                                                         9: function A SSIGNMENT N UMBER(T )
Figure 6: Natural Deduction Rules for Intuitionistic
                                                        10:      N ← N ODE N UMBER(root node of T )
Propositional Logic
                                                        11:      if T is a single node then return N
                                                        12:      end if
A    Inference Rules for Intuitionistic                 13:      Tl , Tr ← left and right sub-trees of T
     Propositional Logic                                14:      nr ← number of internal nodes in Tr
                                                        15:      Ar ← 3nr (p + 2)nr +1          ▷ Compute all
Figure 6 shows the inference rules for intuitionistic       possible assignments in the right sub-tree
propositional logic. Rules relate sequents of the       16:      return 3Ar × A SSIGNMENT N UMBER(Tl )
form Γ ⊢ A, where Γ is an unordered list of as-             + Ar × N + A SSIGNMENT N UMBER(Tr )
sumptions. A derivation is constructed from the         17: end function
axiom (Assumption) using the derivation rules until     18: function N ODE N UMBER(N )
Γ is empty.                                             19:      switch N
   For example, the (→-I) rule says that from a         20:          case ∧ or T : return 0
derivation of Γ ⊢ B under the assumption of Γ, A,       21:          case ∨ or F : return 1
we can get a derivation of Γ ⊢ A → B. The (→-E)         22:          case →: return 2
rule says that from a derivation of Γ ⊢ A → B and       23:          case Pi : return i + 1       ▷1≤i≤p
a derivation of Γ ⊢ A we can derive Γ ⊢ B.              24: end function
   Here are an example derivation.
   p1 → p1 ∨ p2.
                                                        B.1   Catalan Number
                        (Assumption)
                p1 ⊢ p1
                          (∨-I1)                        The Catalan number Cn is applicable for counting
             p1 ⊢ p1 ∨ p2
                            (→-I)                       full binary trees that consist of n + 1 leaf nodes,
            ⊢ p1 → p1 ∨ p2                              corresponding to exactly n internal nodes (Stanley,
                                                        2015). Additionally, it can be calculated through
B    Uniformly Distributed Data
                                                        recursion as shown:
     Explanation
                                                                              n
In this section, we discuss the uniform character-
                                                                              X
                                                                       Cn =         Ci−1 Cn−i .
istics of our dataset, particularly emphasizing the                           i=1
The first Catalan numbers for n = 0, 1, 2, 3, 4 are        for internal nodes include conjunction (∧), disjunc-
1, 1, 2, 5, 14.                                            tion (∨), and implication (→); whereas for leaf
A concise interpretation of this recursion is as fol-      nodes, the choices encompass true (T ), false (F ),
lows: it involves counting the number of internal          and a set of propositions P1 , . . . , Pp .
nodes in the left sub-tree, amounting to i − 1, and           This counting facilitates an efficient ranking of
then in the right sub-tree, amounting to n − i, for        all full binary trees with n internal nodes. This
each of the n scenarios in computing Cn .                  ranking process inherently establishes a bijection
                                                           with the set of natural numbers, allowing for a clear
Algorithm 2 Decoding                                       correspondence between each full binary tree and
Require: A natural number ID, with n indicating            a unique natural number. Consequently, this sets
    the number of internal nodes and p represent-          the stage for a detailed examination of two criti-
    ing the number of atomic propositions                  cal processes: encoding (see Algorithm 1), which
Ensure: Output a proposition tree                          involves mapping a proposition tree to a natural
 1: quotient, remainder ← D IV M OD (ID, 3n (p +           number, and decoding (see Algorithm 2), which
    2)n+1 )                                                entails mapping a natural number back to a corre-
 2: S ← T REE S HAPE(quotient, n)                          sponding proposition tree.
 3: A ← T REE A SSIGNMENT(S, remainder)                       Having established the bijection between full
 4: return a tree with shape S and assignment A            binary trees and natural numbers, it becomes appar-
 5: function T REE S HAPE(N , n)                           ent that uniformly sampling from the set of natural
 6:      if n is 0 then return a single node               numbers will, in turn, result in a uniform sampling
 7:      end if                                            of full binary trees.
         nl ← max({k| ki=1 Ci−1 Cn−i ≤ N } ∪
                           P
 8:                                                           The inclusion of the parameter n in Algorithm 1
    {0})                                                   is not critical for the functionality of the algorithm
 9:      nr ← n − nl − 1 P                                 as n can be counted from T ; however, it is retained
10:      remaining ← N − ni=1     l
                                     Ci−1 Cn−i             to denote that the most basic encoding and decod-
11:      Nl , Nr ← D IV M OD(remaining, Cnr )              ing approaches are designed for a fixed number
12:      return a tree with left and right sub-trees       of internal nodes n. For example, ID 0 denotes
    shaped by T REE S HAPE(Nl , nl ) and T REE -           different propositions depending on the specified
    S HAPE(Nr , nr ), respectively                         value of n. As a result, the decoding algorithm, as
13: end function                                           outlined in Algorithm 2, is specifically intended for
14: function T REE A SSIGNMENT(S, N )                      uniformly generating proposition trees with a fixed
15:      Perform an inorder traversal of the tree          n. To achieve a uniformly distributed proposition
    with shape S. For each leaf node, interpret            tree from a set of trees with various n, one might
    it as a digit in base p + 2, and for each internal     simply merge the rankings of fully binary trees
    node, interpret it as a digit in base 3. Compute       with different n, a task which can be performed
    the assignment that gives N by utilizing the           with relative ease. This approach of merging can
    N ODE N UMBER function introduced in Algo-             be similarly applied to trees with varying p as well.
    rithm 1                                                   Given the uncertainty surrounding the proof
16: end function                                           lengths when generating propositions, our ap-
                                                           proach involves uniform sampling for proposition
                                                           selection. This selection is later refined by exclud-
B.2   Bijection between Propositions and
                                                           ing propositions according to their proof lengths as
      Natural Numbers
                                                           computed by the proof generation algorithm.
As depicted in Figure 3, every proposition cor-
responds to a unique tree representation. Conse-           C    Examples
quently, it only requires the identification of a bijec-
                                                           In Figure 7, we show an example Lean proof for
tion between full binary trees and natural numbers.
                                                           a theorem in Figure 3. Lines preceded by ’–’ are
   For every full binary tree possessing n internal
                                                           comments solely for explanatory purposes.
nodes and p atomic propositions, there exist
  3#internal node (p + 2)#leaf node = 3n (p + 2)n+1
distinct cases. Observe that the choices available
variable (p1 p2 p3 p4 p5 : Prop)
theorem : (((p1 ∨ p2) → False) → ((p1 → False) ∧ (p2 → False))) := by
  -- Implications on the right can always be decomposed.
  -- Introduce an assumption h1 that says ((p1 ∨ p2) → False)
  intro h1
  -- Now we want to show ((p1 → False) ∧ (p2 → False))
  -- Conjunctions on the right can always be decomposed.
  -- We then need to show (p1 → False) and (p2 → False) separately.
  apply And.intro
  -- We are showing (p1 → False).
  -- Implications on the right can always be decomposed.
  -- We introduce assumption h2 for p1. And we try to show False.
  intro h2
  -- We want to use the implication h1. So we show its premise.
  have h3 : (p1 ∨ p2) := by
    -- Show the left disjunct. (The right adjunct leads to an TAE)
    apply Or.inl
    -- One of the premise coincides with the conclusion.
    exact h2
  -- We have shown the premise of h1 (p1 ∨ p2),
  -- we can now drive its conclusion (False), denoted by h4.
  let h4 := h1 h3
  -- False on the left can always be used.
  apply False.elim h4
  -- We have shown (p1 → False) and now we show (p2 → False).
  -- Implications on the right can always be decomposed.
  -- We introduce assumption h2 for p2. And we try to show False.
  intro h5
  -- We want to use the implication h1. So we show its premise.
  have h6 : (p1 ∨ p2) := by
    -- Show the right disjunct. (The left adjunct leads to an TAE)
    apply Or.inr
    -- One of the premise coincides with the conclusion.
    exact h5
  -- We have shown the premise of h1 (p1 ∨ p2),
  -- we can now drive its conclusion (False), denoted by h7.
  let h7 := h1 h6
  -- False on the left can always be used.
  apply False.elim h7


         Figure 7: An example of an intuitionistic propositional logic theorem with its proof in Lean
