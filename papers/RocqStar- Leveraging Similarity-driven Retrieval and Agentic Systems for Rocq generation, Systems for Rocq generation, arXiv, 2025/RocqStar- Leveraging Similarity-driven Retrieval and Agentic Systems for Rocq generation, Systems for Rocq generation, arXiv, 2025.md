                                             RocqStar: Leveraging Similarity-driven Retrieval and Agentic
                                                            Systems for Rocq generation
                                                Andrei Kozyrev                  ∗           Nikita Khramov                   ∗       Gleb Solovev                    Anton Podkopaev
                                                   JetBrains Research                          JetBrains Research                    JetBrains Research                JetBrains Research
                                                        Germany                                     Germany                               Germany                        the Netherlands
                                                                                                                                                                      Constructor University
                                                                                                                                                                        Bremen, Germany

                                         ABSTRACT                                                                                 there exist several ITPs, such as Rocq (formerly Coq) [1], Lean [6],
                                         Interactive Theorem Proving was repeatedly shown to be fruitful                          Agda [14], Isabelle [20], and others. Rocq is a mature ITP, which has
                                                                                                                                  experienced more than 30 years of continuous development and
arXiv:2505.22846v3 [cs.LG] 26 Jan 2026




                                         when combined with Generative Artificial Intelligence. This paper
                                         assesses multiple approaches to Rocq generation and illuminates                          improvement. Rocq has an extensive track record of high-impact
                                         potential avenues for improvement. We identify retrieval-based                           projects. For example, Rocq was used to verify the correctness of
                                         premise selection as a central component of effective Rocq proof                         the CompCert C compiler [16], the only C compiler, in which an
                                         generation and propose a novel approach based on a self-attentive                        extensive study found no bugs [35].
                                         embedder model. The evaluation of the designed approach shows                               Verifying software has always been a rigorous process requiring
                                         up to 28% relative increase of the generator’s performance. We                           significant time and human effort. To mitigate this, a number of
                                         tackle the problem of writing Rocq proofs using a multi-stage agen-                      approaches have been developed to automate theorem proving in
                                         tic system, tailored for formal verification, and demonstrate its                        Rocq. These approaches build upon the underlying interactive proof
                                         high effectiveness. We conduct an ablation study and demonstrate                         paradigm of Rocq, where proofs are constructed incrementally us-
                                         that incorporating multi-agent debate during the planning stage                          ing so-called tactics. Tactics serve as elementary building blocks
                                         increases the proof success rate by 20% overall and nearly doubles                       that allow the user to manipulate the proof state — a data structure
                                         it for complex theorems, while the reflection mechanism further                          containing the current goal and its context. Each applied tactic
                                         enhances stability and consistency.                                                      transforms the proof state, reducing the original task into simpler
                                                                                                                                  subgoals that can be solved recursively. Most solutions implement
                                         KEYWORDS                                                                                 tactic-prediction approaches and employ beam search or a similar
                                                                                                                                  algorithm to navigate the search space. Tactician [3] is a kNN-based
                                         Rocq, Coq, theorem proving, proof assistant, premise selection,
                                                                                                                                  approach, which does similarity-based retrieval of tactics used in
                                         agentic system, multi-agentic debate
                                                                                                                                  similar states. CoqGym [33] and Proverbot9001 [26] use Recurrent
                                         ACM Reference Format:                                                                    Neural Networks (RNNs), Graph2Tac [25] proposed a novel graph-
                                         Andrei Kozyrev , Nikita Khramov , Gleb Solovev , and Anton Podkopaev                     based neural tactic prediction. Thakur et al. [27] and Kozyrev et al.
                                           . 2026. RocqStar: Leveraging Similarity-driven Retrieval and Agentic Sys-
                                                                                                                                  [15] instead build generation pipelines around general-purpose,
                                         tems for Rocq generation. In Proc. of the 25th International Conference on
                                                                                                                                  cloud-hosted LLMs, so that no heavy computations occur on the
                                         Autonomous Agents and Multiagent Systems (AAMAS 2026), Paphos, Cyprus,
                                         May 25 – 29, 2026, IFAAMAS, 12 pages.                                                    user’s machine. CoqPilot [15], along with that, contributes a bench-
                                                                                                                                  marking framework and allows seamless integration of standalone
                                         1     INTRODUCTION                                                                       tools into the workflow of Rocq’s user.
                                                                                                                                     Many approaches call attention to the importance of premise
                                         In recent years, the advent of Generative Artificial Intelligence (AI)                   selection, i.e., retrieving useful context information to advance gen-
                                         has accelerated the process of developing new software. However,                         eration. Yang et al. [34] introduced LeanDojo, a retrieval-augmented
                                         there are studies [22] showing that users who use AI assistants                          prover in Lean that significantly improves over non-retrieval base-
                                         tend to introduce more bugs and vulnerabilities into their code,                         lines. Thompson et al. [28] present the Rango tool and report state-
                                         compared to those who write code on their own. Formal software                           of-the-art performance on the CoqStoq benchmark, automatically
                                         verification could help mitigate the issue of bugs and security flaws,                   synthesizing complete proofs for 32% of the theorems. The work
                                         as it ensures that the software operates correctly and reliably in                       highlights how strongly the well-formed context contributes to
                                         compliance with the given specification. Under the assumption                            the success of Rango. Moreover, they show that proof retrieval is
                                         of a well-formed specification, formal verification provides strong                      the most performant mechanism for premise selection. The proof
                                         guaranties and an acceptance criterion for the generated code. Inter-                    retriever selects relevant previously completed proofs from the
                                         active Theorem Prover (ITP) is a software tool that assists the user                     current project and provides them as references to the model. Ac-
                                         with the development of formal specifications and proofs. To date,                       cording to the evaluation, Rango proved 47% more theorems than
                                         ∗ Authors contributed equally to this work.                                              the variant without a proof retriever. However, their retrieval mech-
                                                                                                                                  anism assumes that two textually similar statements have proofs
                                         Proc. of the 25th International Conference on Autonomous Agents and Multiagent Systems   relevant to each other. In this work, we demonstrate that this as-
                                         (AAMAS 2026), C. Amato, L. Dennis, V. Mascardi, J. Thangarajah (eds.), May 25 – 29,
                                         2026, Paphos, Cyprus. © 2026 International Foundation for Autonomous Agents and          sumption oversimplifies the relationship between statements and
                                         Multiagent Systems (www.ifaamas.org). This work is licenced under the Creative
                                         Commons Attribution 4.0 International (CC-BY 4.0) licence.
proofs and introduce a novel embedding model for Rocq state-            agentic-system. Our approach follows a structured process consist-
ments. It is trained to predict the similarity between their proofs     ing of planning, execution, and reflection. An ablation study shows
and achieves up to a 28% relative improvement on the evaluation         that while naive planning has limited impact, effective planning
set.                                                                    based on the Multi-Agent Debate (MAD) framework plays a crucial
   Another promising direction in generative theorem proving that       role. Specifically, it yields a 20% relative improvement in the overall
we have identified is Agentic Systems. Research by Kozyrev et al.       proof success rate and nearly doubles the success rate on complex
[15] shows that current Rocq generation methods mostly strug-           theorems with longer reference proofs (33% vs. 17%). Additionally,
gle with complex reasoning tasks. Approaches that perform proof         we demonstrate the benefits of the reflection mechanism, which
search on top of a tactic generator slow down dramatically as theo-     improves the overall proof success rate from 48% to 66% and more
rem complexity grows, since searching for longer proofs becomes         than quadruples success on complex theorems; see § 4.3 for details.
exponentially harder due to the explosion of the underlying search      The evaluation results show that the RocqStar system solves up to
space [30]. Other neural methods, which apply LLMs, suffer from         60% of the theorems from the CoqPilot dataset. It is implemented
the same problem due to the inability of the model to handle com-       using Koog1 , an open-source JetBrains framework that offers a type-
plex reasoning tasks [12]. Agentic systems are known to address         safe Kotlin DSL for building AI agents with structured workflows
these problems; however, to our knowledge, there were close to no       and tool interaction. The source code of the agent is available at
attempts to build an autonomous agentic system for an ITP. We           https://github.com/JetBrains-Research/rocqstar-agentic-system.
build an extensive Model Context Protocol (MCP) server for Rocq            The remainder of the paper is organized as follows. § 2 describes
and implement an autonomous Agentic System over it, utilizing           our Similarity-Driven Retrieval mechanism. § 3 introduces the agen-
various problem-specific solutions, such as multi-agent debate. We      tic system. § 4 presents an evaluation of the retrieval component
conduct an evaluation and show that our agentic system strongly         (§ 4.1), the agent (§ 4.2), and an ablation study of the agentic system
outperforms all other previously benchmarked solutions in the           (§ 4.3). We describe the related work in § 5 and conclude in § 6.
CoqPilot’s work, raising the ratio of successfully proven theorems
from 51% to 60%.                                                        2    SIMILARITY-DRIVEN RETRIEVAL
                                                                        A known problem in Retrieval Augmented Generation (RAG), ap-
                                                                        plied to the domain of Interactive Theorem Proving (ITP), is premise
                                                                        selection [10, 29]. Premise selection is the task of retrieving rele-
1.1    Contributions
                                                                        vant facts from a given knowledge base to provide the model with
The main contributions of this paper are the following.                 the necessary context to advance the proof. However, Huang et al.
    RocqStar proof retriever We propose a novel approach for            [9] and Xu et al. [31] highlight that this context must be carefully
premise selection in Rocq. Rocq suffers from the data-scarcity prob-    curated, as the inclusion of irrelevant information degrades model
lem that is common to most ITPs. Aggregating the largest pub-           performance.
licly available repositories, one could expect to collect roughly 300       We distinguish two ways of doing premise selection in Rocq.
million tokens of Rocq, and about the same for Lean. In contrast,       Hint selection — given a context 𝐶 and a tactic with an unknown
open-source Python corpora easily exceed 100 billion tokens. To         positional argument, e.g. apply _, the task is to yield potential
tackle this issue we contribute a convenient standalone tool BigRocq    candidates for the argument. Proof selection, in turn, given theo-
to extract additional data from Rocq code, utilizing the nature of      rem statement 𝑆, focuses on choosing other statements with their
Rocq’s system and the intermediate states of the proof. BigRocq         respective proofs, so that their presence in the context of the gen-
bridges the gap between Automated Generation and Rocq’s ecosys-         eration request would help the model with the generation of the
tem. Using BigRocq, we mine a dataset of 76,524 statements with         proof for statement 𝑆. Since the approach of applying general pur-
corresponding proofs from 4 big projects and train a self-attentive     pose models to proof generation is relatively new, most of the
embedder model, which learns to predict how close the proofs of         works [2, 13, 28, 34] on premise selection in Rocq and other ITPs fo-
given statements will be. In addition, we provide a pipeline to re-     cused on hint selection. However, Thompson et al. [28] and Kozyrev
produce such embeddings for an arbitrary project, which offers          et al. [15] show that even a baseline proof selection significantly
even better results. We integrate the solution as a new retrieval       boosts the model’s capabilities and is stronger than hint selection.
approach for selecting context theorems in CoqPilot and evaluate        The baseline proof selection presented in both works [15, 28], given
it using CoqPilot’s benchmarking infrastructure. Compared to the        the target statement 𝑠 ∗ and a database of already proven theorems
baseline text similarity-based ranker, we show an improvement of        [𝑠 0, 𝑝 0 ] , . . . , [𝑠𝑛 , 𝑝𝑛 ] (where 𝑠𝑖 denotes a theorem statement and 𝑝𝑖
28% on the evaluation set. The BigRocq tool, the training dataset,      its respective proof), chooses theorems, statements of which have
and the code for training the embedder model are available at           the maximum similarity to the target one. Similarity is defined by
https://github.com/JetBrains-Research/rocqstar-rag. The embedder        the BM-25 information retrieval technique [24] or the Jaccard simi-
model’s checkpoint is available at https://huggingface.co/JetBrains-    larity index. That results in packing the generator’s context with
Research/rocq-language-theorem-embeddings.                              theorems, based on how similar their statements are syntactically.
    RocqStar agentic system Addressing the lack of research on              We propose a retrieval mechanism that improves the perfor-
applying agentic systems to ITPs, we build an autonomous sys-           mance of the generator compared to the described baseline. During
tem for generating Rocq proofs. A custom MCP server built on            the generation of the target proof for the statement 𝑆 we generally
top of coq-lsp [7] handles the interaction with Rocq; its source
code is available at https://github.com/JetBrains-Research/rocqstar-    1 Koog https://docs.koog.ai
                                                                                                               Lemma s1 (n : nat) : n = 0 \/ n <> 0.
                       Theorem test :                                                                          Proof.
                           forall n : nat,                                              left; auto.                destruct n.
                             n = 0 \/ n <> 0.
                                                                                       𝑠2           []             - left; auto.
                                                                   destruct n.
                       Proof.                                                                                      - right; auto.
                                                               intros n.                                       Qed.
                           intros n.                      𝑠0               𝑠1
                           destruct n.
                                                                   destruct n.                                 Lemma s2 : 0 = 0 \/ 0 <> 0.
                           - left; auto.                                                right; auto.
                           - right; auto.                                              𝑠3           []         Proof. left; auto. Qed.

                       Qed.                                                                                    Lemma s3 (n : nat) : S n = 0 \/ S n <> 0.
                                                                                                               Proof. right; auto. Qed.



                                                Figure 1: Processing theorems into trees; 𝑠𝑖 denotes a state


assume that the model benefits more from seeing similar proofs to                            utilize Rocq system’s functionality, preprocess theorems, and trans-
the one that it needs to generate, rather than from seeing similar                           form sequential proof structures into trees. Fig. 1 illustrates this
statements with proofs dissimilar from the target one. Evaluation of                         transformation process. Since every node in such a tree is a valid
our retriever in § 4.1 supports this supposition. One might assume                           state, we can automatically construct a proof for it by recursively
that if statements 𝑠 ∗ and 𝑠𝑖 are similar, their respective proofs 𝑝 ∗                       following its subtree edges. Extracting all intermediate statements
and 𝑝𝑖 are similar as well:                                                                  together with their proofs allows us to expand any given Rocq
                similarity(𝑠 ∗, 𝑠𝑖 ) =⇒ similarity(𝑝 ∗, 𝑝𝑖 )                     (1)         theorem dataset by a factor roughly proportional to the average
                                                                                             proof length. In practice, the observed expansion is also affected by
However, we show that this implication often does not hold. The                              limitations of our extraction procedure. In our case, this resulted
heuristic of retrieving similar statements produces decent baseline                          in an approximately fourfold increase in dataset size. The dataset
results, but fails in complex cases, leaving room for improvement.                           format and further details are provided in Appendix A.
We design our retrieval method to guide context selection based                                 We call the proposed tool BigRocq and make it publicly avail-
on the similarity of the proofs and show its practicality.                                   able as a standalone component of our system. The idea of min-
   Let us define the proof similarity 𝐷 𝐿 as the Levenshtein edit                            ing additional training data from the intermediate states of the
distance computed over lists of tactics. Insertions and deletions of                         ITP is not new; Kogkalidis et al. [13] conducted analogous re-
tactics have a unit cost, as in the standard Levenshtein formulation.                        search for the Agda [14] language. Similar research for Rocq also
The substitution cost between two tactics is proportional to the                             takes place [25, 33]; however, some of those works are highly de-
Levenshtein distance between their string representations. The                               pendent on the deprecated ways of communication with Rocq’s
resulting distance is normalized by the maximum proof length.                                compiler [33] and do not support up-to-date versions of Rocq. In
                                                             Lev(𝑝𝑖 , 𝑝 𝑗 )                contrast, others implement similar ideas as a part of the training
   𝑝𝑖 = 𝑡𝑎𝑐𝑖 0 , . . . , 𝑡𝑎𝑐𝑖𝑚 , 𝑙𝑖 = |𝑠𝑖 |, 𝐷 𝐿 (𝑝𝑖 , 𝑝 𝑗 ) =                               pipeline and do not allow for seamless reuse. Using BigRocq, we
                                                               max(𝑙𝑖 , 𝑙 𝑗 )
                                                                                             mine a total of 76,524 statements, collected from 344 files from 4 big
We conduct the following experiment to examine whether the
                                                                                             Rocq projects. These projects are CompCert, IMM, Promising2Imm,
relation in Equation (1) holds in practice. Considering 1,855,701
                                                                                             and XMM. CompCert contributes large and heterogeneous proofs,
pairs of theorems from the IMM project2 , corresponding to all
                                                                                             while the remaining projects focus on weak-memory reasoning,
unordered pairs among 1,927 theorems, we compute correlations
                                                                                             which exhibits diverse proof styles across multiple abstraction lev-
between statement similarities and respective proof similarities. In
                                                                                             els. To avoid data leakage, we exclude theorems belonging to the
summary, BM25-based statement similarity shows a weak negative
                                                                                             evaluation datasets from training and only mine subgoals when
relationship with the Levenshtein-based proof distance (Pearson
                                                                                             augmenting a project.
𝑟 = –0.154, Spearman 𝜌 = –0.171). The code to reproduce these
experiments could be found in the RocqStar-retriever repository3 .
   To assess the issue of ineffective proof selection, we try to find                         2.2        Modeling
a function 𝑓 (𝑠𝑖 , 𝑠 𝑗 ) that correlates with the defined proof distance                      In our work, we formulate the problem as a self-supervised con-
stronger than statement similarity does. In this work, we introduce                           trastive representation learning task and train a self-attentive em-
a neural method that learns vector embeddings for Rocq theorem                                bedder model [19]. Given a dataset T = (𝑠𝑖 , 𝑝𝑖 ), where 𝑠𝑖 is a Rocq
statements, training them so that the distance between any two                                statement, 𝑝𝑖 is its corresponding proof, and S denotes the set of
vectors mirrors the similarity between the respective theorem’s                               all statements appearing in T , together with a similarity function
proofs.                                                                                       𝑓 (proof 𝑖 , proof 𝑗 ) defined between two proofs, we aim to learn a
                                                                                              function
2.1     Dataset mining
                                                                                                                          𝑟 : S × S → R,
Along with other ITPs, Rocq struggles with data scarcity. To ad-
dress this issue, we mine additional data from the Rocq code. We                             which takes two statements 𝑠𝑖 , 𝑠 𝑗 ∈ S as inputs and outputs a
2 IMM https://github.com/weakmemory/imm                                                      score approximating the similarity of their respective proofs 𝑝𝑖 , 𝑝 𝑗 .
3 RocqStar retriever: https://github.com/JetBrains-Research/rocqstar-rag/tree/main/          In other words, 𝑟 (𝑠𝑖 , 𝑠 𝑗 ) ≈ 𝑓 (𝑝𝑖 , 𝑝 𝑗 ). This formulation allows the
experiments                                                                                  ranker 𝑟 to assign scores to candidate statements relative to a target
statement, thereby guiding retrieval towards those whose proofs                  ensuring that informative gradients are maintained. In particular,
are most likely to be useful.                                                    given a statement 𝑠, during dataset preprocessing we compute
   In § 4, we evaluate the performance of the proposed model in                  distances to other samples. We then mark a pair as positive if the
the following task. Given a target statement 𝑠 ∗ and a set of proven             distance between their proofs is less than a threshold 𝜏𝑝𝑜𝑠 , and mark
theorems T , we aim to select 𝑘 premises from T to be used as                    it as negative if it is greater than 𝜏𝑛𝑒𝑔 . Given the hyperparameter
context for generating a proof of 𝑠 ∗ . We take the 𝑘 most relevant              𝑘 neg and sets of positive and negative pairs 𝑃𝑠+ and 𝑃𝑠− , we compute
theorems, according to the ranker 𝑟 .                                            a per-statement loss term L𝑠 as follows:
                                                                                                                                      
                      Top𝑘 (𝑟, 𝑠 ∗ ) = arg top𝑘 𝑟 (𝑠𝑖 , 𝑠 ∗ )                                                     exp cos(𝑧𝑠 , 𝑧𝑝 )/𝑇
                                          (𝑠𝑖 ,𝑝𝑖 ) ∈ T                                L𝑠 = − log
                                                                                                                          𝑘 neg
                                                                                                                        ∑︁
We say that statement 𝑠 ∗ is solved with the use of the ranker 𝑟 if
                                                                                                                                                      
                                                                                                    exp cos(𝑧𝑠 , 𝑧𝑝 )/𝑇 +       exp cos(𝑧𝑠 , 𝑧𝑛 𝑗 )/𝑇
the generator 𝑔 produces a valid proof for 𝑠 ∗ given the premises                                                        𝑗=1
selected by 𝑟 .                                                                  where cos is a cosine similarity between ℓ2 -normalized embeddings
                         (
                                                                                 of statements, and 𝑝 ∈ 𝑃𝑠+ , 𝑛 𝑗 ∈ 𝑃𝑠− . On average, we observed
                                                   
                           1, 𝑔 Top𝑘 (𝑟, 𝑠 ∗ ), 𝑠 ∗ is a valid proof,
      Solve(𝑠 ∗, 𝑟, 𝑔) =                                                         smoother convergence for higher values of 𝑘 neg , which is consis-
                           0, otherwise.
                                                                                 tent with findings by Chen et al. [5]. However, due to hardware
Finally, the quality of the ranker is estimated by the number of theo-           limitations, we selected 𝑘 neg = 100 as a practical trade-off between
rems in the evaluation set that can be solved using 𝑟 in combination             convergence stability and computational cost.
with a given generator 𝑔.                                                           Despite the adjustment of proof_distance(·), during training
   One of the difficulties we encountered during training is a U-                we experienced the problem of the model converging too quickly
shaped distribution of proof distances over randomly sampled the-                on “easy” negatives—pairs, whose proofs (and typically their state-
orem pairs. Specifically, when plotting the frequency of theorem                 ments) are already far apart in the raw distance space. To keep in-
pairs against their proof distance, most pairs cluster either at very            formative gradients flowing, we add hard negative pairs; with some
small distances, corresponding to short, highly similar proofs, or               probability we treat a pair of statements as negative if 𝜏hardneg ⩽
at very large distances, corresponding to largely unrelated proofs.              sim(proof𝑎 , proof𝑏 ) ⩽ 𝜏neg . Introduction of negative samples helped
As a result, pairs with intermediate distances are underrepresented,             to stabilize the training process; we have observed a less steep
creating a gap that hinders effective training. To mitigate this, we             training curve and better generalization overall. Other training
define a modified proof distance that combines the previously intro-             hyperparameters are listed in Appendix B.
duced in § 2 distance measures with an additional similarity term
and injected noise for robustness:                                               3   AGENTIC SYSTEM
   proof_distance(𝑝𝑖 , 𝑝 𝑗 ) = 𝛼 𝐷 𝐿 (𝑝𝑖 , 𝑝 𝑗 ) + (1 − 𝛼) 𝐷 𝐽 (𝑝𝑖 , 𝑝 𝑗 ) + 𝛾   Agent-based approaches are broadly used in code generation and
                                          |𝑝𝑖 ∩ 𝑝 𝑗 |                            repair tasks [4, 32, 36]. Despite a large number of autonomous
                  𝐷 𝐽 (𝑝𝑖 , 𝑝 𝑗 ) = 1 −                                          and semi-autonomous coding agents, they are not widely used in
                                          |𝑝𝑖 ∪ 𝑝 𝑗 |
                                                                                 formal proofs generation and are not tailored to the Rocq specifics.
The coefficient 𝛼 = 0.7 was chosen heuristically based on the
                                                                                 To address this, we have implemented a RocqStar agentic system.
distribution plot and yielded the best performance in experiments.
                                                                                    To allow interaction between the agent and Rocq’s system, we
The noise 𝛾 is taken from U (−1𝑒 − 3, +1𝑒 − 3).
                                                                                 develop a REST API server that provides a set of tools that are
   As we have already explained in § 2, statement similarity is a poor
                                                                                 useful during the execution. We apply our domain knowledge and
choice of 𝑟 , as it shows a low correlation with the target function
                                                                                 construct these tools to bring an agent-driven proving process
proof_distance. However, it still provides a strong baseline: in prac-
                                                                                 as close as possible to a human-driven one. Examples of allowed
tice, similar theorems occasionally have similar proofs. Accordingly,
                                                                                 function calls include checking validity of proofs, retrieving the
our approach builds upon statement encoders, fine-tuning them
                                                                                 valid prefix of given proof, gathering additional information about
to better align with the underlying proof structure. We fine-tune
                                                                                 available entities in the context, and interacting with the context
Microsoft’s 108-million-parameter encoder CodeBert [8], originally
                                                                                 via performing commands like Print ?a to identify the type of an
pretrained on a combined corpus of programming and natural lan-
                                                                                 argument or Search ?exp to search for defined terms by a pattern.
guage texts. We also experimented with gte-modernbert-base4
                                                                                 Toolset is described in detail in Appendix C. Interaction with Rocq’s
as the base model, but it did not yield notable improvements. As
                                                                                 system is carried out through its language server, coq-lsp [7]. To
shown in § 4.1, the encoder without post-training performs on par
                                                                                 conform with a commonly used Model Context Protocol (MCP) and
with the Jaccard-similarity baseline, indicating that the unadapted
                                                                                 allow seamless agent interaction with the environment through
model relies primarily on surface-level syntactic similarity rather
                                                                                 tools, we implement an MCP server that wraps the REST API server.
than proof-related semantics. Our goal, therefore, is to adapt the
                                                                                 Among the provided tools, the most important is the proof-checking
encoder to capture this deeper semantic relation.
                                                                                 tool. It not only verifies whether a proof is valid but, in case of an
   To achieve this, we train the model using the InfoNCE [21] loss.
                                                                                 error, returns detailed diagnostic information: the error message,
In our setting, the distribution of proof distances is imbalanced
                                                                                 its exact location, the valid prefix preceding the error, and the
even after normalization. InfoNCE naturally handles this case by
                                                                                 remaining goals after that prefix. This functionality allows the
contrasting a limited number of positives against a set of negatives,
                                                                                 agent to maintain awareness of the current proof state and leverage
4 gte-modernbert-base: https://huggingface.co/Alibaba-NLP/gte-modernbert-base    partial proof progress.
                  1                                      2
                      Target theorem
                                                                                           Planning Stage
                      b : bool
                                                                                                  Initial plan                                               Plan scoring
                      negb (negb b) = b.




                                                                                                                                                       ans
                                                                                                                                                                  LLM




                                                                                                                                                   k pl
                                                                                                  Args against
                      Premises                                    Pro LLM                                              Con LLM                               Plan 1: 0.95
                                                                                                    Args pro                                                      ...
                      Theorem plusn0: n : nat,                                                          m rounds                                             Plan k: 0.36
                          (n + 1) =? 0 = false.
                                                                                                                                            an




                                                        Emb
                      Proof. ... Qed.                                                                                                  pl
                                                                                                                                   g




                                                                   Av
                                                                                                                                 in




                                                         edd
                                                                                                                             n




                                                                    ai
                                                                                                                         Win




                                                                        la
                                                             er




                                                                         bl
                      Theorem add_comm: b c,




                                                                             e
                                                                                                  Judge LLM




                                                                              to
                          andb b c = andb c b.                                                                                              plan




                                                                                 ol
                                                                                                                                  Upd




                                                                                   s
                      Proof. ... Qed.
                                                                                                                                                              Critic LLM
                                    ..
                                     .                    3
                                                                                                                                                                   if fails
                      Theorem plus0: n : nat,                                                                                                                       often
                                                    Embedder                           analyzed
                          0 + n = n.
                      Proof. ... Qed.                                                                                                 Executor LLM




                                                  Figure 2: Agentic pipeline with RocqStar retriever


3.1    Agent Logic                                                                                  the current plan along with similar proofs and their analysis. The
The input to the agent is presented as a target theorem without a                                   replanner is a separate language model that revises the plan based
proof and a file where it was declared, see box 1 of Fig. 2. Agent’s                                on the critic’s feedback and the retrieved examples. The whole
pipeline is logically split into two main stages: planning and execu-                               message history is sent back to the executor agent. During the
tion. In the planning phase, multiple language models rigorously                                    execution of each plan, 𝑛 tool calls are allowed. If valid proof is not
work out the strategy for the further implementation. During exe-                                   found after 𝑛 tool calls, we denote the plan as failed. In this case, we
cution agents follow the plan aiming to generate the correct proof.                                 ask a plan failure summarizer LLM to generate a short explanation
   Planning Stage We employ the idea of multi-agent debates [18]                                    of why the strategy execution failed and what happened during
to generate a strategy for proving the given theorem. Specifically,                                 it. Then this summarized explanation is sent to the new execution
two LLMs engage in a discussion: one proposes and defends an                                        stage with the next selected plan. This procedure is repeated until
initial plan (pro LLM), while the other critiques it (con LLM); see                                 the correct proof is found or there are no more strategies to execute.
box 2 in Fig. 2. After several debate rounds, the entire message                                    For clarity, Figure Fig. 2 presents a simplified view of the system
history is passed to a judge LLM, which determines the winner and                                   and does not explicitly depict all auxiliary LLM components used
produces the final plan. By repeating this procedure, we generate                                   in the pipeline.
𝑘 candidate strategies. These are then evaluated by a plan scoring
LLM that assigns each a numerical score (the higher, the better).                                   4       EVALUATION
Finally, the top-𝑙 plans are selected and forwarded to the Execution
                                                                                                    To evaluate our approach, partially and as a whole, we use the
Stage; see box 3 of Fig. 2.
                                                                                                    CoqPilot benchmarking framework. We required a dataset with a
   Execution Stage For each of the selected plans, we run an
                                                                                                    large number of human-written theorems and proofs. To compare
executor agent that follows it step by step, invoking tools from
                                                                                                    our solution to existing ones, we decided to re-use the dataset by
the provided tool set — proof checker, context–inspection queries,
                                                                                                    Kozyrev et al. [15]. It is limited to 300 theorems from the IMM
search commands, and others, as atomic actions. Through these
                                                                                                    project [23], which was suitable for us in terms of computational
tool calls, the agent interacts with the environment via the MCP
                                                                                                    and financial costs. The theorems are partitioned into three groups,
server. In addition to this iterative execution, we employ a reflection
                                                                                                    corresponding to the difficulty level. The length (in tactics) of the
mechanism that monitors the progress of the proof and adjusts
                                                                                                    human-written reference proof of the theorem estimates its diffi-
the strategy when necessary. We track how many consecutive
                                                                                                    culty. The sizes of each group are chosen with respect to the initial
erroneous proof attempts occur, and once this number exceeds a
                                                                                                    distribution of proof lengths in the project. Final group sizes and
predefined threshold (set to five during evaluation), a critic model
                                                                                                    length ranges of each group could be found in Table 2. The dataset
is called to assess the current proof state and identify deviations
                                                                                                    is further restricted to theorems whose human-written reference
from the intended strategy. After that, we retrieve theorems along
                                                                                                    proofs contain no more than 20 tactics, following the original setup
with their proofs, whose top-level goals are similar to the currently
                                                                                                    of the CoqPilot benchmark. From now on, we will refer to the de-
remaining goal, according to the cosine similarity between their
                                                                                                    scribed dataset as the IMM-300 dataset. For smaller ablation studies
RocqStar-ranker embeddings. We prompt the LLM to explain which
                                                                                                    we additionally prepared IMM-50, a 50-theorem subset of IMM, con-
tactic sequences could be helpful to finish our proof. We gather
                                                                                                    structed with the same procedure. No theorems from the dataset
the generated criticism and send it to the replanner LLM to refine
                                                                                                    were present in the training set of the RocqStar ranker embedding
  Group                               ⩽4                                          5−8                                        9 − 20
  Ranker            Jaccard       ModernBert RocqStar               Jaccard      ModernBert RocqStar          Jaccard      ModernBert RocqStar
  GPT-4o           48% ± 5%        44% ± 4%        51% ± 5%        18% ± 4%      21% ± 5%      25% ± 3%       11% ± 4%       8% ± 4%       14% ± 5%
  Claude 3.5       58% ± 5%        57% ± 3%        61% ± 4%        28% ± 5%      30% ± 3%      36% ± 5%       16% ± 5%      16% ± 5%       21% ± 5%

                              Table 1: Model performance under different ablations across all evaluation sets



   Reference proof length            ⩽4         5–8       9–20       Total
   Group size                        131         98         71        300
                                                                                    Reference proof length         ⩽4         5–8      9–20      Total
   OpenAI GPT-4o                     50%        26%        15%        34%           Group size                      22         16        12        50
   OpenAI o1                         66%        31%         8%        41%
                                                                                    Full Agent                     91%       56%        33%       66%
   Deepseek R1                       58%        29%        11%        37%
                                                                                    Agent w/o MAD                  86%       44%        17%       56%
   Claude 3.5 Sonnet                 73%        41%        27%        51%
                                                                                    Agent w/o Planning             86%       50%        17%       58%
   LleMMa 7B                         24%        11%         1%        15%
                                                                                    Agent w/o Rocq★ retr.          86%       50%        33%       62%
   Tactician (synth)                 45%        23%        10%        29%           Agent w/o Reflection           73%       44%         8%       48%
   Rango                             38%        18%         8%        25%           Claude 3.5 Sonnet              86%       37%         8%       52%
   RocqStar Agent                   76%        56%         38%        60%                Table 3: Ablation study of Multi-Agent Debate
  Table 2: Different Rocq generation methods via CoqPilot



model. Moreover, the training set only contained partial theorem                     As can be seen from Table 1, our RocqStar ranker consistently
goals, i.e., intermediate proof goals arising during proof execution,             outperforms both the Jaccard baseline and the untrained Modern-
rather than the original top-level theorem statements. The split                  Bert encoder, demonstrating reliable gains across all evaluation
of both datasets into groups, details, and limitations are described              groups. Most of the performance increase could be seen in the sec-
in Appendix D. Computational and financial resources used for                     ond group; we interpret these results as follows. For short theorems
experiments are described in Appendix E.                                          in the first group, the assumption that similar statements imply
                                                                                  similar proofs often holds; therefore, all rankers perform compara-
4.1     Retrieval Mechanism                                                       bly. For complex theorems from the third group, it rarely happens
                                                                                  that two theorems have significantly similar proofs, resulting in
We integrate our retrieval mechanism as a ranker into CoqPilot                    less advancement space for the model.
and evaluate it on the IMM-300 dataset with different models under
the hood. To assess its performance, we compare our approach
against two baselines: (i) an untrained embedder model (we use                    4.2    Agentic System
gte-modernbert-base, with codebert-base yielding comparable                       We evaluate our agentic system on the IMM-300 dataset with the
results), and (ii) a lexical similarity baseline based on the Jaccard             goal of solving as many theorems as possible. We use the strongest
index. In the latter, given a target theorem statement 𝑠 ∗ and a set              available Rocq proof–generating models, as measured by pass@12
of proven theorems [𝑠 0, 𝑝 0 ] , . . . , [𝑠𝑛 , 𝑝𝑛 ], it ranks the theorems in     on the CoqPilot benchmark. In addition, following the common
descending order of 𝐽 (𝑠 ∗, 𝑠𝑖 ), where 𝐽 (𝑠 ∗, 𝑠𝑖 ) is the Jaccard-similarity    principle of using a critic stronger than the executor [37], we em-
index. The statement is split into tokens by whitespaces, commas,                 ploy a more capable model for the planning and evaluation stages.
etc. Jaccard-similarity index is semantically almost the same as                  Specifically, for all parts of the planning stage, we use the Claude 3.5
the BM-25 metric and produces the same numerical results. For                     Sonnet model and perform two rounds of debate between actors.
each theorem in the dataset, we take theorems within the same                     Four plans are generated, and two are chosen for further execu-
file, sort them using the ranker (Jaccard, ModernBert, or RocqStar,               tion. During execution, 20 tool calls are allowed from the MCP
respectively), take the 𝑘 most relevant ones (𝑘 is equal to 7 in                  server. Additionally, after five proof-checking calls, the critic model
our experiments) and send a request to the model to generate the                  (Claude 3.7 Sonnet) is invoked and analyzes whether a deviation
completion. The chosen theorems are being sent as a few-shot                      from the initial plan has occurred. We use Claude 3.5 Sonnet for
prompt. Generation for each theorem is requested 12 times. If the                 the execution and re-planning, and Google Gemini Flash 2.0 for
Rocq’s system accepts any of the proofs, the theorem is considered                other tasks, due to the necessity of a big context. Results of the
solved. The target metric in our evaluation is the ratio of solved                evaluation are shown in Table 2.
theorems. The evaluation results are presented in Table 1. The                       As shown in Table 2, our agentic system outperforms other
reported values denote mean success rates, and the ± intervals                    benchmarked models inside the CoqPilot framework. The strongest
correspond to the standard deviation across three independent                     model so far was Claude 3.5 Sonnet, which achieves 51% accuracy
runs.                                                                             on the dataset, given 12 retries for each theorem. RocqStar agent
achieves 60%, showing vigorous improvement. In terms of financial        tactic, retrieving relevant lemmas or definitions to use in the next
costs, we estimate a run of an agent on one theorem at 1.3 US dollars,   step. The problem of retrieving existing proofs that can help ad-
compared to 0.25 US dollars for 12 requests to the pure Claude 3.5       vance generation is barely explored in the literature. CoqPilot [15]
Sonnet in CoqPilot. Along with five language models invocated            and Rango [28] address this problem by augmenting the generator’s
through the CoqPilot framework, we have compared our solution            context with previously proven theorems whose statements are
to other Rocq generation approaches, such as Tactician and Rango.        similar to the target theorem being proved. Our work proposes a
On our IMM-300 dataset both solutions showed a result comparable         novel premise selection method and demonstrates improvements
to CoqPilot with OpenAI GPT-4o as the generator model.                   over the baselines used in prior work [15, 28].
                                                                            In our multi-agentic system, we distribute responsibility across
4.3    Ablation study                                                    multiple agents, each responsible for a simpler subtask within the
                                                                         overall proof generation process. This decomposition, which sepa-
We conduct an ablation study to analyze the contribution of individ-
                                                                         rates high-level reasoning, planning, and execution, is a common
ual components of the agentic pipeline to the overall success rate.
                                                                         design pattern in agentic systems. For example, Li et al. [17] pro-
In particular, we investigate the effects of removing (1) the Multi-
                                                                         pose a task force split into Thinker, Solver, Critic, and Debug agents,
Agent Debate (MAD) layer responsible for iterative plan refinement,
                                                                         while Liang et al. [18] introduce a multi-agent debate framework
(2) the Planning stage entirely, (3) the RocqStar retrieval module,
                                                                         that encourages divergent reasoning in complex tasks. We show
and (4) the Reflection mechanism responsible for forced retrieval,
                                                                         that explicitly separating planning from execution is essential for
criticism, and replanning. All experiments are performed on the
                                                                         the formal verification pipeline. Theorem-proving demands a clear
IMM-50 dataset, with all other system components kept unchanged.
                                                                         and high-level picture of the proof before executing any code. Run-
The results are summarized in Table 3.
                                                                         ning a multi-agent debate at the planning stage ensures rigorous
   Planning Considering that software-verification tasks cannot
                                                                         evaluation of different approaches before interacting with Rocq’s
be solved ad hoc, without explicit planning, we measure how remov-
                                                                         system. We produce several plans for further execution. In a man-
ing the MAD layer and reverting to single-pass planning affects the
                                                                         ner similar to Islam et al. [11], we assign scores to plans and run
proportion of successfully proved theorems. We run two versions
                                                                         them in the order of score decrease. To our knowledge, there have
of the agent: one generates plans via MAD, and the other produces
                                                                         been no substantial attempts to build fully agentic systems for ITPs.
a single plan in one LLM call without further refinement. Addition-
                                                                         The closest related effort is the early proof-of-concept by Yang et al.
ally, we include a configuration with the Planning stage entirely
                                                                         [34], which explores the use of agents for proof generation in Lean.
disabled, where the executor immediately attempts to construct a
                                                                         While this work illustrates the potential of agent-based approaches
proof without any plan. This comparison shows that an agent with-
                                                                         in this domain, it relies on minimal tooling and does not form a fully
out planning performs nearly identically, or slightly worse, than
                                                                         agentic system with autonomous planning and iterative execution.
one guided by a poor single-pass plan, suggesting that a suboptimal
                                                                            As a user interface, we utilize CoqPilot to integrate into the com-
plan does not provide advantage. In contrast, multi-step planning
                                                                         mon Rocq’s programmer pipeline. CoqPilot is a VSCode5 plugin,
via MAD yields a consistent improvement across all groups, con-
                                                                         facilitating access to Rocq generation methods for end-users. Cur-
firming the importance of structured plan refinement. An example
                                                                         rently, the RocqStar retrieval component is available in CoqPilot as
of how MAD repairs a previously unsuccessful plan is presented in
                                                                         a premise-ranking module. Integration of the full RocqStar agentic
Appendix F.
                                                                         system as a proof generator is ongoing.
   RocqStar retrieval To further assess the contribution of re-
trieval to the agentic pipeline, we evaluate the agent with its re-
                                                                         6    CONCLUSION
trieval component replaced by a Jaccard-based baseline. This sub-
stitution results in a small but consistent decrease in performance,     We have presented a method to enhance retrieval-augmented gen-
indicating that the proposed retrieval mechanism provides a mean-        eration in Rocq via leveraging neural premise selection using a
ingful, though moderate, improvement in the agentic setting. While       self-attentive embedder model. We evaluated our proposed solution
the agentic architecture mitigates some of the limitations of weaker     on a dataset of 300 Rocq theorems with two different generator
premise selection, effective retrieval remains an important compo-       models under the hood and showed a noticeable improvement of up
nent that contributes to more stable and reliable proof generation.      to 28% relative to the baseline. Our result suggests that proof-aware
   Reflection Finally, we disable the reflection mechanism that          premise selection considerably improves generation quality, par-
triggers forced retrieval and replanning after failed attempts. With-    ticularly for medium-difficulty theorems, where the gap between
out reflection, the agent loses its ability to recover from early mis-   statement similarity and proof similarity becomes more significant.
takes, leading to a noticeable degradation of performance, especially       Our work pioneers the use of Agentic Systems applied to For-
on longer and more complex proofs. The result shows that reflection      mal Verification. We have implemented an advanced pipeline that
complements planning by enabling recovery from failed reasoning          includes rigorous planning via multi-agent debate, domain-specific
trajectories.                                                            tooling, and an adaptive executor–critic loop that iteratively refines
                                                                         proofs based on partial progress. We conclude that our RocqStar
                                                                         agent shows promising results, surpassing strong baselines and
5     RELATED WORK
                                                                         highlighting the applicability of agentic systems in the domain of
Many Rocq generation methods improve generation using Retrieval          theorem proving. The ablation study further demonstrates that both
Augmentation. Most of those works solve the hint selection prob-
lem [2, 28], described in § 2. Those approaches build proofs tactic by   5 VSCode: https://code.visualstudio.com
multi-agent planning and reflection are key to maintaining stable                           [17] Jierui Li, Hung Le, Yingbo Zhou, Caiming Xiong, Silvio Savarese, and Doyen
reasoning and achieving consistent improvements in the proof’s                                   Sahoo. 2024. Codetree: Agent-guided tree search for code generation with large
                                                                                                 language models. arXiv preprint arXiv:2411.04329 (2024).
success rate.                                                                               [18] Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang, Yan Wang, Rui Wang,
                                                                                                 Yujiu Yang, Shuming Shi, and Zhaopeng Tu. 2023. Encouraging divergent
                                                                                                 thinking in large language models through multi-agent debate. arXiv preprint
ACKNOWLEDGMENTS                                                                                  arXiv:2305.19118 (2023).
                                                                                            [19] Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang,
We thank Ekaterina Verbitskaia, Ivan Kabashnyi, Maksim Rozen-                                    Bowen Zhou, and Yoshua Bengio. 2017. A structured self-attentive sentence
berg, and Pavel Guliaev for their valuable comments on this work.                                embedding. arXiv preprint arXiv:1703.03130 (2017).
                                                                                            [20] Tobias Nipkow, Markus Wenzel, and Lawrence C Paulson. 2002. Isabelle/HOL:
We also thank the Dynamic Program Analysis Research team at                                      a proof assistant for higher-order logic. Springer. https://doi.org/10.1007/3-540-
JetBrains (Nikita Dukin, Saga Rut Sunnevudóttir, and Egor Klimov)                                45949-9_5
for their help in building tool execution distributions described                           [21] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning
                                                                                                 with contrastive predictive coding. arXiv preprint arXiv:1807.03748 (2018).
in Appendix G. Finally, we thank the Koog team at JetBrains for                             [22] Neil Perry, Megha Srivastava, Deepak Kumar, and Dan Boneh. 2022. Do users
developing Koog, an open-source framework for building AI agents                                 write more insecure code with ai assistants?(2022). arXiv preprint arXiv:2211.03622
with an idiomatic, type-safe Kotlin DSL.                                                         (2022).
                                                                                            [23] Anton Podkopaev, Ori Lahav, and Viktor Vafeiadis. 2019. Bridging the gap be-
                                                                                                 tween programming languages and hardware weak memory models. Proceedings
                                                                                                 of the ACM on Programming Languages 3, POPL (2019), 1–31.
REFERENCES                                                                                  [24] Stephen Robertson, Hugo Zaragoza, et al. 2009. The probabilistic relevance
 [1] Yves Bertot and Pierre Castéran. 2013. Interactive theorem proving and program              framework: BM25 and beyond. Foundations and Trends® in Information Retrieval
     development: Coq’Art: the calculus of inductive constructions. Springer Science &           3, 4 (2009), 333–389.
     Business Media. https://doi.org/10.1007/978-3-662-07964-5                              [25] Jason Rute, Miroslav Olšák, Lasse Blaauwbroek, Fidel Ivan Schaposnik Mas-
 [2] Lasse Blaauwbroek, Josef Urban, and Herman Geuvers. 2020. Tactic learning                   solo, Jelle Piepenbrock, and Vasily Pestun. 2024. Graph2Tac: Learning Hierar-
     and proving for the Coq proof assistant. arXiv preprint arXiv:2003.09140 (2020).            chical Representations of Math Concepts in Theorem proving. arXiv preprint
     https://doi.org/10.29007/wg1q                                                               arXiv:2401.02949 (2024). https://doi.org/10.48550/arXiv.2401.02949
 [3] Lasse Blaauwbroek, Josef Urban, and Herman Geuvers. 2020. The tactician: A             [26] Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner. 2020. Gen-
     seamless, interactive tactic learner and prover for coq. In International Conference        erating correctness proofs with neural networks. In Proceedings of the 4th ACM
     on Intelligent Computer Mathematics. Springer, 271–277. https://doi.org/10.1007/            SIGPLAN International Workshop on Machine Learning and Programming Lan-
     978-3-030-53518-6_17                                                                        guages. 1–10. https://doi.org/10.1145/3394450.3397466
 [4] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. 2024. RepairAgent:              [27] Amitayush Thakur, Yeming Wen, and Swarat Chaudhuri. 2023. A language-agent
     An Autonomous, LLM-Based Agent for Program Repair. arXiv:2403.17134 [cs.SE]                 approach to formal theorem-proving. arXiv preprint arXiv:2310.04353 (2023).
     https://arxiv.org/abs/2403.17134                                                            https://doi.org/10.48550/arXiv.2310.04353
 [5] Changyou Chen, Jianyi Zhang, Yi Xu, Liqun Chen, Jiali Duan, Yiran Chen, Son            [28] Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin Fisher, Alex Sanchez-
     Tran, Belinda Zeng, and Trishul Chilimbi. 2022. Why do we need large batch-                 Stern, Yuriy Brun, João F Ferreira, Sorin Lerner, and Emily First. 2024. Rango:
     sizes in contrastive learning? a gradient-bias perspective. Advances in Neural              Adaptive Retrieval-Augmented Proving for Automated Software Verification.
     Information Processing Systems 35 (2022), 33860–33875.                                      arXiv preprint arXiv:2412.14063 (2024).
 [6] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob             [29] Josef Urban. 2004. MPTP–motivation, implementation, first experiments. Journal
     von Raumer. 2015. The Lean theorem prover (system description). In Automated                of Automated Reasoning 33 (2004), 319–339.
     Deduction-CADE-25: 25th International Conference on Automated Deduction, Berlin,       [30] Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Zheng Yuan, Wenwei
     Germany, August 1-7, 2015, Proceedings 25. Springer, 378–388. https://doi.org/10.           Zhang, Dahua Lin, and Kai Chen. 2025. InternLM2.5-StepProver: Advancing
     1007/978-3-319-21401-6_26                                                                   Automated Theorem Proving via Critic-Guided Search. arXiv:2410.15700 [cs.AI]
 [7] Emilio Jesús Gallego Arias et al. 2022. Visual Studio Code Extension and Language           https://arxiv.org/abs/2410.15700
     Server Protocol for Coq. https://github.com/ejgallego/coq-lsp                          [31] Xiaohan Xu, Chongyang Tao, Tao Shen, Can Xu, Hongbo Xu, Guodong Long,
 [8] Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xiaocheng Feng, Ming                          Jian guang Lou, and Shuai Ma. 2024. Re-Reading Improves Reasoning in Large
     Gong, Linjun Shou, Bing Qin, Ting Liu, Daxin Jiang, and Ming Zhou. 2020.                    Language Models. arXiv:2309.06275 [cs.CL] https://arxiv.org/abs/2309.06275
     CodeBERT: A Pre-Trained Model for Programming and Natural Languages.                   [32] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao,
     arXiv:2002.08155 [cs.CL]                                                                    Karthik Narasimhan, and Ofir Press. 2024. SWE-agent: Agent-Computer In-
 [9] Yue Huang, Yanbo Wang, Zixiang Xu, Chujie Gao, Siyuan Wu, Jiayi Ye, Xiuying                 terfaces Enable Automated Software Engineering. arXiv:2405.15793 [cs.SE]
     Chen, Pin-Yu Chen, and Xiangliang Zhang. 2025. Breaking Focus: Contextual                   https://arxiv.org/abs/2405.15793
     Distraction Curse in Large Language Models. ArXiv abs/2502.01609 (2025). https:        [33] Kaiyu Yang and Jia Deng. 2019. Learning to prove theorems via interacting
     //api.semanticscholar.org/CorpusID:276107466                                                with proof assistants. In International Conference on Machine Learning. PMLR,
[10] Geoffrey Irving, Christian Szegedy, Alexander A Alemi, Niklas Eén, François                 6984–6994. https://doi.org/10.48550/arXiv.1905.09381
     Chollet, and Josef Urban. 2016. Deepmath-deep sequence models for premise              [34] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing
     selection. Advances in neural information processing systems 29 (2016).                     Yu, Saad Godil, Ryan J Prenger, and Animashree Anandkumar. 2023. Leandojo:
[11] Md Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. 2024. Map-                     Theorem proving with retrieval-augmented language models. Advances in Neural
     coder: Multi-agent code generation for competitive problem solving. arXiv                   Information Processing Systems 36 (2023), 21573–21612.
     preprint arXiv:2405.11403 (2024).                                                      [35] Xuejun Yang, Yang Chen, Eric Eide, and John Regehr. 2011. Finding and un-
[12] Bowen Jiang, Yangxinyu Xie, Zhuoqun Hao, Xiaomeng Wang, Tanwi Mallick,                      derstanding bugs in C compilers. In Proceedings of the 32nd ACM SIGPLAN
     Weijie J Su, Camillo J Taylor, and Dan Roth. 2024. A peek into token bias: Large            conference on Programming language design and implementation. 283–294. https:
     language models are not yet genuine reasoners. arXiv preprint arXiv:2406.11050              //doi.org/10.1145/1993498.1993532
     (2024).                                                                                [36] Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury. 2024. Au-
[13] Konstantinos Kogkalidis, Orestis Melkonian, and Jean-Philippe Bernardy. 2024.               toCodeRover: Autonomous Program Improvement. arXiv:2404.05427 [cs.SE]
     Learning structure-aware representations of dependent types. Advances in Neural             https://arxiv.org/abs/2404.05427
     Information Processing Systems 37 (2024), 65095–65118.                                 [37] Yefan Zhou, Austin Xu, Yilun Zhou, Janvijay Singh, Jiang Gui, and Shafiq Joty.
[14] Wen Kokke, Jeremy G. Siek, and Philip Wadler. 2020. Programming language                    2025. Variation in Verification: Understanding Verification Dynamics in Large
     foundations in Agda. Science of Computer Programming 194 (2020), 102440.                    Language Models. arXiv:2509.17995 [cs.CL] https://arxiv.org/abs/2509.17995
     https://doi.org/10.1016/j.scico.2020.102440
[15] Andrei Kozyrev, Gleb Solovev, Nikita Khramov, and Anton Podkopaev. 2024.
     CoqPilot, a plugin for LLM-based generation of proofs. In Proceedings of the 39th
     IEEE/ACM International Conference on Automated Software Engineering (Sacra-
     mento, CA, USA) (ASE ’24). Association for Computing Machinery, New York,
     NY, USA, 2382–2385. https://doi.org/10.1145/3691620.3695357
[16] Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister,
     and Christian Ferdinand. 2016. CompCert-a formally verified optimizing compiler.
     In ERTS 2016: Embedded Real Time Software and Systems, 8th European Congress.
                                                                                              (a) Optimization hyperparameters
A    ENCODER TRAINING DATASET
One of the limitations of our BigRocq tool is that it cannot pro-                     Parameter             Value
cess theorems that contain so-called goal selectors. The following                    algorithm             AdamW (0.9, 0.99, e−2)
example illustrates how they work.                                                    schedule              linear warmup (10)
 Theorem test2nat1 : forall n : nat, n = 0 \/ n <> 0.                                 lr                    4e−6
 Proof.
     destruct n.                                                                      batch size (stmts)    16
     - left; auto.                                                                    dropout               0.1
     - right; auto.
 Qed.
                                                                                          (b) Model&Dataset hyperparameters
This example could be rewritten with the use of goal selectors to
the following proof:                                                                 Parameter                          Value
 Theorem test2nat1 : forall n : nat, n = 0 \/ n <> 0.                                embedding dim                      768
 Proof.                                                                              max sequence length                128
     intros n.
     destruct n.                                                                     (positive, negative) threshold     (0.3, 0.65)
     all: try (left; auto) || (right; auto).
 Qed.
                                                                                     threshold hard neg.                0.45
                                                                                     hard negatives prob.               30%
Due to the limited information we get from the Coq-LSP, our heuris-
tic algorithm of transforming the proof into a tree breaks down.
We cannot augment such theorems. The authors of CoqGym [33]                  Table 4: Hyperparameters of the embedder training
also explicitly state that they do not handle theorems with goal
selectors. They state that in their dataset, goal selectors occur in     theorem’s context into it, type-check the context using Coq-LSP,
less than 1% data. The situation has changed since the work was          and then start executing commands and continuously checking
published; the feature is now used more often but is still relatively    generated proofs in the context of this session.
rare. Goal selectors are an issue to be solved, and we are working on
                                                                             • list_coq_files: Returns a list of all Coq files in the project.
a solution by extracting some additional information from Rocq’s
                                                                             • get_theorem_names: Retrieves theorem names available in
system through Coq-LSP.
                                                                                the file, including the target theorem.
   The dataset is stored as a collection of JSON files and, due to
                                                                             • get_theorem_names_excl: Retrieves the available theorem
its relatively small size, is stored within the repository, in the
                                                                                names from a file with the target theorem excluded from the
sub-directory with the model training code: https://github.com/
                                                                                list.
JetBrains-Research/rocqstar-rag/tree/main/proof-embeddings/data.
                                                                             • get_current_target_state: Returns the proof stage for
   Dataset is split into training, validation, and test sets with pro-
                                                                                the target theorem in the current session.
portions of 70%, 20%, and 10% respectively. Theorems from the
                                                                             • get_theorem_with_proof: Given the theorem’s name, re-
same file do not appear in different sets. Parameters of building
                                                                                turns the theorem with its proof.
the dataset are listed in Table 3b. Pair of statements is considered
                                                                             • check_proof: Validates a proof (or a part of a proof) in the
as negative, if the proof_distance between them is greater than
                                                                                context of a session and returns either of the following:
0.65, and positive if it is less than 0.3. If the distance is in range
                                                                               (i) That there are no more goals to prove
[0.45, 0.65], with probability of 30% it is also considered to be a
                                                                              (ii) Provided proof produces no errors, but the goal is not fully
negative pair (see hard negatives in § 2.2).
                                                                                   solved. Returns: updated goal state
                                                                             (iii) The current goal is solved, but there are more goals at other
B    ENCODER DETAILS                                                               depth levels. Returns: first unsolved goal at the closest
The hyperparameters used for training the embedder model are                       depth level
listed in Table 4. We have used microsoft/codebert-base as the               (iv) Provided proof produces errors. Returns: error message
base model and trained our embedder for 22000 steps with a batch             • get_similar_proofs: Given theorem goal/statement as a
size 16, since we use many negative samples in the loss. We applied             string, it uses RocqStar ranker to retrieve theorems that are
a dropout of 0.1 on the last layer of the model; the embedding                  similar to the input statement and returns 15 most similar
dimension is 768, and the maximum sequence length is 128. We use                ones.
AdamW optimizer with a linear warmup schedule for 10% of the                 • about_term: Uses About Rocq’s Command in the current
training steps.                                                                 session. Accepts the term name as an argument. Outputs the
                                                                                term’s definition and a short description from the Coq-LSP.
C    AGENT TOOLSET                                                           • search_pattern: Uses Rocq’s Search ?exp to search for a
Below are the tools that the agent uses to interact with Rocq’s                 pattern in the current session’s file. An example of a valid
system. The session is a utility abstraction, mainly handled by our             command: Search (?a + ?b = ?b + ?a). It could be useful
middleware server under the MCP. It manages sessions and creates                for finding lemmas that could be used in the proof.
a new one when the agent starts proving a new theorem. Sessions              • print_term: Prints a term in the current session file. Uses
are introduced to speed up type-checking and reduce overhead.                   Rocq’s Print command. Accepts the term name as an argu-
When the session is started, we create a file, copy all required                ment. Outputs the term’s definition.
      • check_term: Checks a term in the current session’s file.                Lemma ext_sb_trans : transitive            Lemma ext_sb_irr : irreflexive
                                                                                exts_sb.                                   exts_sb.
        Uses Rocq’s Check command. Similarly to print_term or                   Proof using.                               Proof using.
                                                                                  unfold ext_sb; red; ins.                   unfold ext_sb; red; ins.
        about_term, but outputs only the type of the term. In the                 destruct x,y,z; ins; desf;                 destruct x; ins; desf; splits;
        case of a theorem, it outputs its statement.                            splits; eauto.                             firstorder.
                                                                                  by rewrite H2.                             lia.
                                                                                Qed.                                       Qed.
D     IMM EVALUATION DATASET
The collected IMM-300 dataset from the CoqPilot [15] work includes
                                                                                Figure 3: Theorems with dissimilar statements and similar
only theorems with proofs of length no more than 20. For that
                                                                                proofs
reason the bucket with the most difficult theorems is labeled 9—20
tactics. This decision has been made, reflecting CoqPilot’s original
focus on subgoals and shorter lemmas. Theorems of length no more
than 20 tactics account for 83% of all proofs in the IMM project.                  If we measure the distance between theorems from Figure 3
                                                                                using the conventional Jaccard distance, which is used by default
As we take the same dataset, it possesses the same limitations.
                                                                                in CoqPilot, we get 0.67:
Therefore, we have not evaluated our solution on theorems, for
which the reference proof contains more than 20 tactics. However,                                           | { transitive, ext_sb } ∩ { irreflexive, ext_sb } |
                                                                                 Jaccard_dist(𝑡 1, 𝑡 2) = 1 −
                                                                                                            | { transitive, ext_sb } ∪ { irreflexive, ext_sb } |
such theorems are quite rare.                                                                               1
   The exact list of theorems used in each group could be found in                                     = 1 − = 0.67
                                                                                                            3
the repository of the CoqPilot project: https://github.com/JetBrains-
                                                                                 Jaccard ranker focuses only on statement similarity, which in this
Research/coqpilot/blob/main/etc/docs/benchmark/.
                                                                                case is relatively small, the only similar parts are highlighted with
   A common problem with testing pipelines that include general-
                                                                                red. Jaccard would probably not select theorem ext_sb_irr as a
purpose LLM providers, such as OpenAI, is data contamination.
                                                                                premise for theorem ext_sb_trans; however, they have similar
We are aware, that the model could have possibly seen the human-
                                                                                proofs and one could help the model to generate the proof for
written proofs, as the IMM project has been publicly available
                                                                                the other. Similar parts of the proofs are highlighted with yel-
since a while. However, firstly, the model is provided with neither
                                                                                low. If we measure the distance between these theorems using the
the theorem name for which it is generating the proof, nor the
                                                                                proof_similarity metric we define, we get 0.32, and our trained
proof goal exactly as it appeared in the original file. As we treat
                                                                                model yields 0.28. When using our ranker, it is probable that one
them as proof states, rather than theorems, an LLM receives it in
                                                                                theorem would be selected as a premise for the other.
an equivalent, but slightly modified way. Secondly, as many of
our experiments have shown, various quality of premise selection                                                proof_sim(𝑡1, 𝑡2) = 0.32
drasticly changes the behavior of the model. That hints that the
                                                                                                       embedder_pred(𝑡1, 𝑡2) = 0.28
model is not able to memorize all theorems and proofs. Lastly, data
contamination issue was one of the things we had in mind, while
developing BigRocq. One could pass a Rocq project into BigRocq as
                                                                                E    EXPERIMENTS COMPUTE RESOURCES
input, and for each theorem retrieve the sub-state, that is achieved            Our experiments in the evaluation part mainly use cloud LLM
after 𝑘 steps. On an example of 𝑘 = 2, the following theorem:                   providers and therefore require minimum compute, but compre-
                                                                                hensive financial resources.
 Lemma eq_trans (A : Type) : forall (x y z : A), x = y -> y = z -> x = z.
 Proof.                                                                            Embedder training During our final training run of the em-
     intros x y z Hxy Hyz.                                                      bedding model for RocqStar ranker, the model consumed roughly
     rewrite Hxy. (* State: (A : Type) (x y z: A) (Hxy: x = y) (Hyz: y = z) :
            y = z *)                                                            43 GB of GPU-process memory and only about 6% of the host’s
     rewrite Hyz.
     reflexivity.
                                                                                RAM. Over 31 hours on a single NVIDIA H200 accelerator (with 16
 Qed.                                                                           CPU cores and 200 GB of system memory), disk usage grew steadily
                                                                                from 28 GB to 76 GB as checkpoints and logs accumulated. GPU
Could be automatically tranformed into the following one:
                                                                                utilization stabilized above 90% shortly after the warmup phase
 Lemma eq_trans_modified (A : Type) (x y z: A) (Hxy: x = y) (Hyz: y = z) : y    and remained near saturation for the remainder of training. To sum
        = z.
 Proof.                                                                         up, our setup runs comfortably on a single GPU node with modest
     rewrite Hyz.
     reflexivity.
                                                                                additional CPU and memory overhead.
 Qed.                                                                              Embedder model evaluation Experiments were conducted
                                                                                on a single MacBook Pro with an M1 chip. The only computation-
The higher 𝑘 is chosen, the smaller would be the chances of data                ally expensive part of the experiments (for the local machine) is
leakage, as the produced sub-state gets further and further from                launching multiple Coq-LSP servers at once (CoqPilot benchmark
the original theorem.                                                           does that to optimize the time of the experiments and accelerate
                                                                                type-checking). As we use a middleware service over LLM APIs, our
D.1     Visualizing RocqStar vs. Baseline Premise                               financial estimations might not be accurate. However, we roughly
        Selection                                                               estimate 12 generation attempts per theorem with seven contextual
Here we try to illustrate the difference between different rankers              theorems at 12 cents per theorem for Claude 3.5 and 7 cents for
and show an example of a theorem from IMM project, where our                    GPT-4o. Running the experiment on 300 theorems and repeating it
ranker outperforms the baseline. Figure 3 presents such an example.             three times amounts to a total of 171 US Dollars. Performing the
same experiment for three different retrieval engines brings the        The proposed proof strategy is quite vague, too wordy, and impre-
overall cost to approximately 513 US Dollars.                        cise. With this plan, the executor agent started by fetching similar
   Agent evaluation In the case of the agent evaluation, we ran      theorems and then got stuck in a cycle of ad-hoc attempts to check
the experiment only once and did not provide the confidence inter-   incorrect proofs. In contrast, the winning plan was precise, concise
vals due to financial limitations. We ran our agent on the IMM-300   and clear. It had a top-level structure of the proof incorporated into
dataset, and afterward, we compared five versions of the agent on    the plan and made a winning solution to use the search command,
the IMM-50 dataset in our § 4.3. That results in 550 attempts to     which helped to finish the proof:
prove different theorems. We estimate a single attempt at 1.3 US      Proof.
dollars. Therefore, we estimate the cost of the evaluation of the         unfold IPROP.
                                                                          rewrite sub_W. rewrite sub_is_ta_propagate_to_G.
agent to be 715 US dollars.                                               done.
                                                                      Qed.

F    PLAN REFINEMENT VIA MULTI-AGENT
                                                                       Below, as a comparisson, is the plan, yielded by the multi-agent
     DEBATE                                                          debate:
We compare two proof plans: one generated by a single model call
and one produced via multi-agent debate. The target theorem is
sub_IPROP from src/imm/SubExecution.v, which states:                     The winning proof plan follows these steps:
                                                                           (1) Initial Analysis:
 Lemma sub_IPROP : subseteq (IPROP G') (IPROP G).
                                                                               • Use rewrite /IPROP /subseteq to fully
    The following plan was produced by a single planning call:                   understand the expanded goal
                                                                               • Check G and G’ relationship via about_term
                                                                                 and search_pattern
    Let me outline a proof strategy for showing that                           • Look for helper lemmas about IPROP
    IPROP G’ is a subset of IPROP G.                                             transformations
    First, I want to understand the context better.                        (2) Proof Structure:
    The lemma involves two grammars G and G’, and we                            Proof.
    need to show that the improper symbols of G’ are                            rewrite /IPROP /subseteq.
    contained within the improper symbols of G. Let                             (* See expanded goal structure *)
    me check the definitions and related theorems.                              intros x Hx.
    print_term: "IPROP"                                                         (* Analyze Hx’s type carefully *)
    Understanding the definition of IPROP will help                             (* Use discovered helper lemmas *)
    us formulate the proof. This looks like a lemma                       (3) Reasoning Steps:
    about grammar properties, where we need to show                           • Work with explicit set inclusion based on
    that if a symbol is improper in G’, it must also                            subseteq definition
    be improper in G.                                                         • Use any discovered lemmas about G/G’
    My proposed strategy:                                                       relationship
      (1) Use the definition of subset (⊆) to unfold                          • Preserve flexibility to adapt based on
          the goal.                                                             actual definitions
      (2) For any symbol X in IPROP G’, show it’s also
          in IPROP G.                                                    B’s plan wins because it:
      (3) This will likely require using the                                 • Prioritizes understanding definitions be
          definitions of improper symbols and their                            fore tactical decisions
          relationship between grammars G and G’.                            • Makes systematic use of available tools
    I expect we’ll need to:                                                  • Avoids    assumptions   about   existential
                                                                               structure
        • Start with intros X H to get a symbol X and
                                                                             • Maintains flexibility while having concrete
          hypothesis that it’s in IPROP G’.
                                                                               next steps
        • Use the definition of improper symbols to
          understand why X is improper in G’.
        • Show that these same conditions must hold in
                                                                     G    AGENT EXECUTION PATTERNS
          G.
                                                                     We analyze the agent’s behavior to identify patterns that distinguish
    Before proceeding with the actual proof steps, I’d
                                                                     successful and failed proof attempts. Specifically, we selected the
    like to see if there are any similar theorems or
                                                                     theorem no_sb_cr_to_init from group B of the IMM-50 dataset,
    relevant properties about IPROP that might help
                                                                     which the agent sometimes proved and sometimes failed to prove.
    us.
                                                                     We collected traces from ten successful and seventeen failing exe-
    search_pattern: "IPROP"                                          cutions and plotted the distributions of tool calls averaged over all
                                                                     runs in each scenario (Fig. 4).
                                                                                                    Although the experiment was relatively small, it already pro-
   0.25
                                                              searchPattern
                                                              checkTerm
                                                                                                 vides several observations about the agent’s behavior. We have
                                                              checkProof



    0.2
                                                              getCurrentTargetTheoremState
                                                                                                 not yet identified clear action points that could directly improve
                                                                                                 the agent, but we plan to conduct a larger-scale study and dedi-
   0.15

                                                                                                 cate more effort to analyzing execution trajectories in the future.
    0.1
                                                                                                 Notably, only a subset of available tools is actively used during
   0.05                                                                                          proof attempts, especially in successful runs, indicating that the
         0
                                                                                                 agent has not yet learned to leverage the full range of available
                                                                                                 functionality, although this behavior partly reflects the specifics
                                                                                                 of the analyzed theorem. In failing runs, we observe a more uni-
                                                                                                 form distribution of tool calls (particularly aboutTerm, printTerm,
                 0   5          10        15        20
                                                                                                 and searchPattern), without a pronounced early activity peak.
                                                                                                 This behavior suggests that the agent tends to wander through the
                                                                                                 search space without a clear strategy. Combined with the findings
                         Average successful run                                                  from § 4.3, which highlight the importance of effective planning,
                                                                                                 this supports the view that a well-defined plan, one that explicitly
                                                                  printTerm
                                                                  getCurrentTargetTheoremState
                                                                                                 incorporates context exploration and the retrieval of relevant in-
                                                                                                 formation before trying to build the proof, is essential for stable
                                                                  aboutTerm
                                                                  checkProof
   0.2
                                                                  searchPattern
                                                                  checkTerm




  0.15
                                                                                                 performance. We consider introducing a dedicated, more manual
   0.1
                                                                                                 phase for contextual exploration in future iterations of the agent.
  0.05




    0




             0       5           10            15        20




                          Average failing run

Figure 4: Distributions of successful and failing runs for the
no_sb_cr_to_init theorem
