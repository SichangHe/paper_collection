                                                          Learning an Effective Premise Retrieval Model for Efficient
                                                                        Mathematical Formalization


                                                                    Yicheng Tao * 1 2 Haotian Liu * 1 Shanwen Wang 2 Hongteng Xu 1 3 4


                                                                   Abstract                                                                         User Interface

                                               Formalized mathematics has recently garnered
arXiv:2501.13959v3 [cs.CL] 16 Jul 2025




                                               significant attention for its ability to assist mathe-
                                               maticians across various fields. Premise retrieval,
                                               as a common step in mathematical formalization,
                                               has been a challenge, particularly for inexperi-
                                               enced users. Existing retrieval methods that fa-                              Proof State (Query)
                                                                                                                              Provided by Lean              Select Useful Premise
                                               cilitate natural language queries require a cer-                                                             for Lean Programming
                                               tain level of mathematical expertise from users,
                                               while approaches based on formal languages (e.g.,
                                               Lean) typically struggle with the scarcity of train-
                                               ing data, hindering the training of effective and                           Proposed Premise
                                               generalizable retrieval models. In this work, we                             Retrieval Model
                                               introduce a novel method that leverages data ex-
                                               tracted from Mathlib to train a lightweight and ef-
                                                                                                                                                                     :
                                               fective premise retrieval model. In particular, the                                                                   :

                                               proposed model embeds queries (i.e., proof state
                                               provided by Lean) and premises in a latent space,                             Premise Database
                                                                                                                           Extracted from Mathlib       Top-K Retrieved Premises
                                               featuring a tokenizer specifically trained on for-
                                               mal corpora. The model is learned in a contrastive
                                                                                                                   Figure 1. A schematic diagram illustrating user interactions with
                                               learning framework, in which a fine-grained simi-                   an ITP (e.g., Lean) given our premise retrieval model.
                                               larity calculation method and a re-ranking mod-
                                               ule are applied to enhance the retrieval perfor-
                                               mance. Experimental results demonstrate that
                                               our model outperforms existing baselines, achiev-                   1. Introduction
                                               ing higher accuracy while maintaining a lower
                                                                                                                   Formalized mathematics has recently attracted significant
                                               computational load. We have released an open-
                                                                                                                   attention. It helps verify existing mathematical results, iden-
                                               source search engine based on our retrieval model
                                                                                                                   tify errors in the literature, and has the potential to accelerate
                                               at https://premise-search.com/. The
                                                                                                                   the peer-review process for mathematical papers. This pro-
                                               source code and the trained model can be found
                                                                                                                   cess involves proving natural language theorems within a
                                               at https://github.com/ruc-ai4math/
                                                                                                                   strict formal logical framework. Interactive theorem provers
                                               Premise-Retrieval.
                                                                                                                   (ITPs), or proof assistants, are commonly used for this pur-
                                                                                                                   pose. In recent years, mathematicians have actively partici-
                                           *
                                             Equal contribution 1 Gaoling School of Artificial Intelligence,       pated in developing large formalized theorem libraries using
                                         Renmin University of China 2 School of Mathematics, Renmin Uni-           ITPs such as Lean (De Moura et al., 2015), Coq (Barras
                                         versity of China 3 Beijing Key Laboratory of Research on Large            et al., 1997), and Isabelle (Nipkow et al., 2002).
                                         Models and Intelligent Governance 4 Engineering Research Center
                                         of Next-Generation Intelligent Search and Recommendation, MOE.            However, the process of mathematics formalization often
                                         Correspondence to: Shanwen Wang <s wang@ruc.edu.cn>,                      demands extensive experience with formalization and a high
                                         Hongteng Xu <hongtengxu@ruc.edu.cn>.                                      level of mathematical expertise. Therefore, there has been
                                         The second AI for MATH Workshop at the 42 nd International                a sustained demand for automated auxiliary tools in the
                                         Conference on Machine Learning, Vancouver, Canada. Copyright              formalization field, such as premise retrievers. As illus-
                                         2025 by the author(s).                                                    trated in Figure 1, premise retrieval aims to retrieve useful

                                                                                                               1
                   Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

premises based on the current proof state provided by the for-         of our retrieval model in facilitating the proof process.
malization platform. An effective premise retrieval system
                                                                       Our contributions can be summarized as follows:
can help mathematicians quickly identify relevant theorems,
thereby accelerating the proof process. For example, Lean-
Dojo (Yang et al., 2024) shows that a retrieval-augmented              • We train an effective retrieval model for formalized the-
generator achieves a higher proof pass rate compared to a                orems, with a new tokenizer for formal language, which
standalone generator without premise selection.                          achieves notable results at low computational costs and
                                                                         capable of running on a personal computer.
The early premise retrieval methods leverage internal APIs
of ITPs to identify applicable theorems through pattern-               • We evaluate various retrieval models in a retrieval-
matching algorithms. These methods, however, rely on                     augmented theorem proving pipeline, demonstrating the
strict matching criteria and may miss relevant theorems. Re-             advantages of the proposed retrieval model in assisting
cently, learning-based methods (Yang et al., 2024; Mikuła                proof generators.
et al., 2023) have been proposed to encode formalized theo-
                                                                       • Based on our model, we have deployed a search engine
rems in a latent space and retrieve them by computing their
                                                                         featuring a real-time updating database, available free of
embedding similarities. The learning-based methods can
                                                                         charge to provers, and provide a toolkit to facilitate local
be further categorized based on the query language: natu-
                                                                         model deployment for users.
ral language queries or formal proof state queries. Natural
language-based retrieval (Gao et al., 2024) requires users
to have a sufficient mathematical understanding of the cur-            2. Preliminaries and Related Work
rent proof state, posing a significant challenge for beginners.
                                                                       2.1. Preliminaries in Formalization and Lean
In contrast, formal language-based retrieval is more user-
friendly, but it often relies on fine-tuning pre-trained natural       As a proof assistant, Lean provides a user interface for con-
language models (Yang et al., 2024) because of the scarcity            structing formal proofs. The formalization process typically
of formal proof data. As a result, the fundamental differ-             begins by translating a mathematical statement into Lean.
ences between formal and natural languages introduce a                 Lean then analyzes the statement and presents the user with
semantic gap, leading to suboptimal performance.                       a proof state, which consists of a collection of hypothe-
                                                                       ses and the proposition to be proved. The user provides
The above challenges motivate us to design and learn a
                                                                       commands to modify the proof state until no goals remain.
more effective premise retrieval system that directly lever-
                                                                       In this context, the set of hypotheses is referred to as the
ages the formal proof state to retrieve premises, improving
                                                                       context, and the proposition is called the goal.
accuracy and usability for formalized mathematics. Specif-
ically, our premise retrieval model consists of a context-             While there are various styles of proofwriting, machine
free retrieval (CFR) module and a context-aware re-ranking             learning researchers commonly adopt the tactic-state trans-
(CAR) module, each of which takes BERT (Devlin et al.,                 formation as an abstraction of the process. A tactic is a
2019) as its backbone. The CFR module derives embed-                   piece of program that modifies the current proof state. Ex-
dings for premises and proof states (i.e., queries) and re-            perienced Lean users can develop custom tactics through
trieves relevant premises based on their similarity to the             meta-programming, utilizing Lean’s native automation tools.
input proof states. The CAR module is employed to re-                  Pre-defined tactics, such as simp, linarith, and so on,
order the retrieved premises, and accordingly, improves                have significantly enhanced the efficiency of formalization.1
the top-k recall of the retrieval results. Unlike approaches
                                                                       We present a formal specification of the theorem-proving
that merely fine-tune pre-trained language models, we first
                                                                       process in Lean. Starting with an initial proof state S0 =
pre-train a BERT model from scratch based on existing
                                                                       {Γ0 , G0 }, where Γ0 represents the initial context and G0
formalized corpora, in which a new tokenizer is learned
                                                                       the initial goal, the prover must provide a sequence of tac-
for formal language. Based on the pre-trained BERT, we
                                                                       tics {ti }ni=1 to construct the proof. This sequence can be
further learn the CFR and CAR modules separately via con-
                                                                       visualized as a linked chain of transformations, i.e.,
trastive learning (Chen et al., 2020; He et al., 2020). Experi-
ments show that the retrieval results of our model surpass                             1 t   2    t3       tn       t
                                                                                   S0 −→ S1 −→ S2 −→ · · · −→ Sn .                    (1)
state-of-the-art models in performance while still maintain-
ing computational efficiency. Furthermore, to evaluate the             The proof is complete when Gn = “No Goals”. Note that
practicality of our premise retrieval model, we integrate it           tactics are naturally various. As shown in Figure 2, some
with an independently trained tactic generator, creating a
                                                                           1
retrieval-augmented automated theorem prover. We then                        The simp tactic uses lemmas and hypotheses to simplify the
assess this system using the test dataset and MiniF2F bench-           main goal target or non-dependent hypotheses. The linarith
                                                                       tactic attempts to find a contradiction between hypotheses that are
mark (Zheng et al., 2022), demonstrating the effectiveness             linear (in)equalities.

                                                                   2
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

         Proof State S0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Tactics Relying    Proof State S1
                    <latexit sha1_base64="TzgexU0eciHJdjC5SK5xmbO90Q8=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseiF4+VWltoQ9lsJ+3SzSbsboQS+hO8eFDEq7/Im//GbZuDtj4YeLw3w8y8IBFcG9f9dgpr6xubW8Xt0s7u3v5B+fDoUcepYthisYhVJ6AaBZfYMtwI7CQKaRQIbAfj25nffkKleSwfzCRBP6JDyUPOqLFSs9l3++WKW3XnIKvEy0kFcjT65a/eIGZphNIwQbXuem5i/Iwqw5nAaamXakwoG9Mhdi2VNELtZ/NTp+TMKgMSxsqWNGSu/p7IaKT1JApsZ0TNSC97M/E/r5ua8NrPuExSg5ItFoWpICYms7/JgCtkRkwsoUxxeythI6ooMzadkg3BW355lTxeVL1atXZ/Wanf5HEU4QRO4Rw8uII63EEDWsBgCM/wCm+OcF6cd+dj0Vpw8plj+APn8wfVUY2F</latexit>                                      <latexit sha1_base64="R08Wl6200PgZ9IdGJB20xT7J+58=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseiF4+VWltoQ9lsJ+3SzSbsboQS+hO8eFDEq7/Im//GbZuDtj4YeLw3w8y8IBFcG9f9dgpr6xubW8Xt0s7u3v5B+fDoUcepYthisYhVJ6AaBZfYMtwI7CQKaRQIbAfj25nffkKleSwfzCRBP6JDyUPOqLFSs9n3+uWKW3XnIKvEy0kFcjT65a/eIGZphNIwQbXuem5i/Iwqw5nAaamXakwoG9Mhdi2VNELtZ/NTp+TMKgMSxsqWNGSu/p7IaKT1JApsZ0TNSC97M/E/r5ua8NrPuExSg5ItFoWpICYms7/JgCtkRkwsoUxxeythI6ooMzadkg3BW355lTxeVL1atXZ/Wanf5HEU4QRO4Rw8uII63EEDWsBgCM/wCm+OcF6cd+dj0Vpw8plj+APn8wfW1Y2G</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        on Premise
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     employs pattern matching to identify theorems applicable
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     to the current proof state. This approach, however, en-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     forces strict matching criteria, which often leads to failures
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Case 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     in retrieving relevant theorems. In addition, applications
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     like Moogle3 and leansearch (Gao et al., 2024) have been
         Proof State S0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Tactics Working
                    <latexit sha1_base64="TzgexU0eciHJdjC5SK5xmbO90Q8=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseiF4+VWltoQ9lsJ+3SzSbsboQS+hO8eFDEq7/Im//GbZuDtj4YeLw3w8y8IBFcG9f9dgpr6xubW8Xt0s7u3v5B+fDoUcepYthisYhVJ6AaBZfYMtwI7CQKaRQIbAfj25nffkKleSwfzCRBP6JDyUPOqLFSs9l3++WKW3XnIKvEy0kFcjT65a/eIGZphNIwQbXuem5i/Iwqw5nAaamXakwoG9Mhdi2VNELtZ/NTp+TMKgMSxsqWNGSu/p7IaKT1JApsZ0TNSC97M/E/r5ua8NrPuExSg5ItFoWpICYms7/JgCtkRkwsoUxxeythI6ooMzadkg3BW355lTxeVL1atXZ/Wanf5HEU4QRO4Rw8uII63EEDWsBgCM/wCm+OcF6cd+dj0Vpw8plj+APn8wfVUY2F</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      without Premise
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     developed to enable searches based on natural language de-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Proof State S1
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    <latexit sha1_base64="R08Wl6200PgZ9IdGJB20xT7J+58=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseiF4+VWltoQ9lsJ+3SzSbsboQS+hO8eFDEq7/Im//GbZuDtj4YeLw3w8y8IBFcG9f9dgpr6xubW8Xt0s7u3v5B+fDoUcepYthisYhVJ6AaBZfYMtwI7CQKaRQIbAfj25nffkKleSwfzCRBP6JDyUPOqLFSs9n3+uWKW3XnIKvEy0kFcjT65a/eIGZphNIwQbXuem5i/Iwqw5nAaamXakwoG9Mhdi2VNELtZ/NTp+TMKgMSxsqWNGSu/p7IaKT1JApsZ0TNSC97M/E/r5ua8NrPuExSg5ItFoWpICYms7/JgCtkRkwsoUxxeythI6ooMzadkg3BW355lTxeVL1atXZ/Wanf5HEU4QRO4Rw8uII63EEDWsBgCM/wCm+OcF6cd+dj0Vpw8plj+APn8wfW1Y2G</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     scriptions of the target query. However, they place a higher
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          No Goal
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     demand on the precision of natural language formulations
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     for both the query and the formal theorems. In contrast,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Case 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     premise selection based on purely current formal proof state
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     is a more straightforward approach. LeanDojo (Yang et al.,
Figure 2. Examples of the theorem-proving process in Lean.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           2024) employs a learning-based retrieval model that encodes
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     the proof state and theorems independently, subsequently
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     calculating their similarity to perform the retrieval task.
require additional premises to take effect, while others op-
erate independently. Furthermore, the behavior of certain                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            3. Proposed Method
tactics may vary depending on the presence of premises.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     As shown in Figure 3, our work includes three stages: 1)
2.2. Related Work                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Extract data from the formal mathematics library to con-
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     struct the theorem corpus. 2) The context-free retrieval
Learning-based Retrieval Models In the field of infor-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               stage involves encoding the premises and proof states us-
mation retrieval, traditional methods like BM25 (Harman,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             ing a learning-based proof state encoder and calculating
1995; Robertson et al., 2009) and TF-IDF (Salton & Buck-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             semantic similarities. 3) In the context-aware re-ranking
ley, 1988) rely on term information and document statistics                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          stage, the retrieved premises are concatenated with the query
to match queries with relevant documents. With the ad-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               and evaluated using a cross-encoder for classification and
vancement of deep learning, researchers have developed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               re-ranking.
learning-based retrieval models, often referred to as dense
retrieval models (Karpukhin et al., 2020; Qu et al., 2021).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          3.1. Data Preparation
These models typically fall into two categories.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Let M = {pi }N i=1 denote the library to be searched, where
The first approach (Karpukhin et al., 2020; Qu et al., 2021)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         each pi represents a theorem within the library. Since theo-
encodes queries and documents into embeddings separately.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            rems are functions that accept hypotheses as input and yield
Their similarity is then computed in the embedding space,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            proofs of specified propositions, pi can be represented as
and the top-ranked documents are retrieved as the final re-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          {Γpi , Gpi }, where Γpi = [v1 , . . . , vn ]pi is the argument
sults. A key advantage of this method is that document em-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           list of the theorem and Gpi is the output of the theorem.
beddings can be precomputed, allowing the system to embed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            This representation is isomorphic to a proof state. Given
only the query during retrieval and improving computational                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          the current proof state s, the parameterized retrieval model
efficiency significantly. However, this approach lacks direct                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Φ(s; M, Θ) assigns a score to each premise and returns the
interaction between queries and documents, which may limit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           top-k results. Note that a proof state may contain several
its retrieval performance. The second approach (Qiao et al.,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |s|
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     cases, denoted as s = {si }i=1 , where si = {Γis , Gis }.
2019; Nogueira & Cho, 2019) concatenates the query and
document as a single input to the encoder model, which then                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          From human-written proofs, we extract tactic steps T =
outputs a relevance score between them. This method can                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              {ti }Ti=1 . Each tactic step contains the proof state before
capture richer interactions between queries and documents,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           and after executing the tactic, as well as the premises used
leading to improved performance. However, it incurs higher                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           in the tactic, denoted as ti = (sbefore
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          i      , {pij }nj=1
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           i
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              , safter
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 i     ),
computational costs since the concatenation must be per-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             where pij ∈ M. We collect state-premise pairs from these
formed for each query-document pair. Recently, researchers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           tactics to form our training dataset. We consider the state
have increasingly embraced the paradigm of fine-tuning pre-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          before/after a tactic both relevant to the premises used in
trained models for various retrieval tasks (Ma et al., 2024;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         this step since the state before should satisfy the hypotheses
Wang et al., 2024; Li et al., 2024), leading to substantial                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          of the premises, while the state after will contain patterns
improvements in performance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         in the goal of the premises. Thus, we form our dataset as
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |D|
Premise Selection in Lean Premises are theorems or hy-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               D = {(si , Pi )}i=1 , where si are distinct proof states and
potheses that can be used in a tactic. Lean’s internal API2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          Pi is the set of relevant premises of si .
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        3
   2
       Loogle: https://loogle.lean-lang.org/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Moogle: https://www.moogle.ai/


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 3
                       Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

  Formal Theorem Corpus                          Context-Free Retrieval                                         Context-Aware Re-rank
  theorem mul_two (n : ℕ) : n * 2 = n + n             { pi }iN1                                                   Premise Ranked List
                                                                                        query
  theorem gcd_dvd_left (m n : ℕ) : m.gcd n ∣ m                                                                      theorem Nat.add_comm
                                                        Context𝜞𝚪𝚪
                                                       Context
                                                       Context
                                                                          Goal𝑮𝐆𝐆
                                                                         Goal
                                                                         Goal               Proof State 𝒔           theorem Int.add_comm
                                                                                                                    theorem Nat.sub_add_comm
    ···




                                      ···
            149549 premises
                                                                                                                    ······

  theorem add_comm (n m : ℕ) : n + m = m + n
                                                                         BERT                          𝒇 ⋅; 𝜽
                                                                                                                                     Choose Top 𝒌𝟐
                                                   𝒇 𝚪; 𝜽           𝒇 𝑮; 𝜽            𝒇 𝒔; 𝜽
                       Data Extraction                                                                            E[CLS]     MLP        Softmax      Pr (s, p)
                       Stepwise Proofs
                       Tactic-Premise Pairs                                                                                         BERT
                       Theorem Declarations                        𝒇(𝒔; 𝜽) 𝟏      𝒇 𝚪; 𝜽        𝒇 𝑮; 𝜽
                                                    𝑠𝑖𝑚 𝒔, 𝒑 =              ·                +
                                                                    𝒇(𝒔; 𝜽) 𝟐      𝒇 𝚪; 𝜽        𝒇 𝑮; 𝜽           [CLS]      query     [SEP]      premise
   Mathlib
                                                                                   Maximum Similarity                Choose Top 𝒌𝟏


Figure 3. The overview of the retrieval framework. We extract 149,549 premises from Mathlib as our formal theorem corpus. In the
context-free retrieval stage, all the premises are encoded by averaging the embeddings of context and goal. The top-k1 premises retrieved
in this stage will be re-ranked in a context-aware manner.


3.2. Model Architecture                                                          The retrieval model measures the relevance between a proof
                                                                                 state s and a premise p by computing the similarity of their
Our premise retrieval model consists of two components:
                                                                                 embeddings. The conventional similarity can be defined as
a context-free retrieval (CFR) module and a context-aware
re-ranking (CAR) module. In detail, the CFR module re-                                                           f (s; θ)   f (p; θ)
trieves a large set of relevant theorems for a given proof                                       sim(s, p) =              ·           .                     (2)
                                                                                                                ∥f (s; θ)∥ ∥f (p; θ)∥
state. Subsequently, the CAR module refines the ranking
of the top-k theorems retrieved by the CFR module, further                       However, considering that some states may only correlate
improving the accuracy of the retrieval process.                                 with either the arguments or the goal, we encode the premise
Context-Free Retrieval In the context-free retrieval stage,                      arguments and goal separately, which can be denoted as
we adopt a dense retrieval method (Karpukhin et al., 2020).                      f (Γp , θ) and f (Gp , θ). Accordingly, we design a fine-
This approach maps both the proof state and the theorem                          grained similarity between the given state s and premise p
into a shared latent space, enabling retrieval through the                       — sim(s; p) is formulated as
computation of their cosine similarity. We design the model                                                                         
                                                                                          f (s; θ)    1    f (Γp ; θ)     f (Gp ; θ)
based on the BERT encoder architecture. For a given input                                           ·                  +               . (3)
                                                                                         ∥f (s; θ)∥ 2 ∥f (Γp ; θ)∥ ∥f (Gp ; θ)∥
text, we process it through the model and apply average                                  | {z } |                     {z             }
pooling over the last hidden states to derive its latent repre-                        state embedding              premise embedding
sentation, denoted as f (·; θ).
                                                                                 This similarity is designed based on the principle that the
We preprocess the context and goal for each state and                            context of the proof state should first meet the preconditions
premise to eliminate the effect of the theorem name and                          of the available premises and, afterward, determine whether
achieve a unified format. We prepend a special token                             the conclusions drawn from these premises fulfill the current
<VAR> to each element of the context Γ and <GOAL> to the                         requirements. Compared to the conventional similarity, this
goal G, then concatenate them to form a new string. Here is                      fine-grained design aims to explicitly measure the similarity
an example:                                                                      from both perspectives, capturing premises that can be ap-
                                                                                 plied in the current context, along with premises that can be
                                                                                 a solution to the current goal.
    Raw theorem:
                                                                                 Context-Aware Re-ranking While facilitating the retrieval
    theorem Nat.add_comm (n m : Nat) :                                           model and vector store enables fast and efficient queries,
        n + m = m + n
                                                                                 the lack of interaction between the state and premise may
    After process:                                                               lead to lower accuracy. To address the limitations of this
                                                                                 context-free approach, we adopt a context-aware method to
    <VAR> n m : Nat <GOAL> n + m = m + n
                                                                                 re-ranking the results from first stage. Specifically, we de-
                                                                                 sign the re-ranking model based on BERT architecture that

                                                                             4
                      Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

follows the sequence-pair classification of (Nogueira & Cho,              which the choice of negatives is crucial. We sample hard
2019). The state and premise will be concatenated together                negatives from the top-k1 premises selected by the retrieval
by [SEP] as the re-ranking module’s input sequence.                       model and they will be used in the re-ranking model train-
                                                                          ing process. During testing, we also use the retrieval model
The module obtains the embeddings of the input. Passing the
                                                                          to retrieve the top-k1 premises and re-ranking them by the
[CLS] embedding through an affine projection followed
                                                                          re-ranking model. The loss function used for training the
by a sigmoid layer, we obtain the relevant probability of the
                                                                          re-ranking model is the cross-entropy loss, and the optimiza-
state and premise, i.e.,
                                                                          tion objective is formulated as
              P r(s, p) = σ(W · h[CLS] + b),                    (4)                       |D| |Pi |
                                                                                          X   X               P r(si , pij )
                                                                                    min               − log P                 ′
                                                                                                                                 ,   (6)
where h[CLS] is the embedding of the [CLS] token, W is                                    i=1 j=1           p′ ∈P ′ P r(si , p )
                                                                                                                 ij
the weight matrix, b is the bias term, and σ represents the
                                                                                  ′
sigmoid activation function. For top-k retrieval, we first use            where Pij  contains one positive pij and some hard negatives.
the retrieval model to find k1 candidates. The re-ranking                 P r(s, p) is the relevant probability obtained via Eq. (4).
model serves as a filter and returns top-k as the final result.           Training Tactic Generator After training the retrieval
Note that, existing re-ranking methods (Qiao et al., 2019;                model, we integrate it with the generator for testing. The
Nogueira & Cho, 2019) improve retrieval performance by                    generator is trained in an independent paradigm for a fair
concatenating the query and each passage and passing them                 comparison between retrievers. Most prior work on genera-
through their re-ranking models. This strategy has a high                 tors (Welleck & Saha, 2023; Song et al., 2023; Yang et al.,
computational cost during inference due to the combining                  2024) utilizes state-tactic pairs to fine-tune a pre-trained
process of state and premise. As a trade-off, we apply a                  model for tactic generation. Leandojo (Yang et al., 2024)
re-ranking model to refine the ranking of premises retrieved              incorporates premise retrieval by leveraging the retrieval
by the retrieval model.                                                   model to extract relevant premises based on the state from
                                                                          the training dataset. The premises are then concatenated
3.3. Learning Algorithm                                                   with the state to form premise-augmented state-tactic pairs
                                                                          used for fine-tuning. However, this approach results in a
Based on the Masked Language Modeling (MLM) (Taylor,                      high degree of coupling between the retrieval model and the
1953; Devlin et al., 2019) method, we pre-train the CFR and               generator, as prior knowledge of the retrieval result distribu-
CAR modules on the formalized corpus we collected. Their                  tion is incorporated during training.
tokenizers are the same and trained on formalized language
corpus using WordPiece (Song et al., 2021) algorithm. Then,               To ensure a fair experimental setup, we aim to decouple the
we use the state-premises pairs to fine-tune the pre-trained              generator from the retrieval model and train the generator
modules separately by contrastive learning.                               independently. As a substitution of the retrieval model, we
                                                                          randomly select the positive and negative premises from
Contrastive Learning of CFR Module For (si , Pi ) ∈ D,                    the library and prepend them to the state, thereby creating
we use pij ∈ Pi along with negatives sampled from M                       premise-augmented state-tactic pairs. For each tactic, we
                    ′
to construct a set Pij , which contains one positive pij and              add up to ten premises. The number of positive premises
   ′
|Pij |−1 negatives. The optimization objective of contrastive             selected is randomly determined, ranging from one to the
learning is formulated as                                                 lesser of the total available positive premises or ten. The
         |D| |Pi |
                                                                          remaining premises are negative. Half of these negatives
         X   X                   exp(sim(si , pij )/τ )                   are selected from the same module as the positive samples,
   min               − log P                          ′
                                                            ,   (5)
                               p′ ∈P ′ exp(sim(si , p )/τ )
                                                                          while the remaining are chosen from other modules. Follow-
         i=1 j=1                    ij
                                                                          ing (Yang et al., 2024), we use these pairs to fine-tune the
where τ refers to the temperature. We use the Homoge-                     ByT5 (Xue et al., 2022) model for tactic generation. The
neous In-Batch Negative Sampling, which calls for many                    loss function we use is typically cross-entropy loss.
negative samples to guarantee the embedding’s discrimina-
tivenss (Izacard et al., 2022; Wang et al., 2022; Qu et al.,              4. Experiments
2021). In our work, this is implemented by the usage of
in-batch negatives — for each query, the negatives are ran-               4.1. Experiment Setup
domly sampled from the corpus, excluding the other positive
                                                                          Implementation Details Our retrieval and re-ranking mod-
premises of the query. Given a batch of B samples, it results
           ′                                                              els are based on the BERT architecture, which consists of
in B × |Pij  | − 1 negative samples.
                                                                          6 layers, each with 12 attention heads. It features a hidden
Contrastive Learning of CAR module The CAR module                         size of 768 and an intermediate size of 3,072, complemented
is learned in the same contrastive learning framework, in                 by a vocabulary size of 30,522. For the retrieval model, the

                                                                      5
                    Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

maximum position embeddings are configured at 512. The
                                                                                 Table 1. Relevance criteria for the retrieval results.
maximum length for states is set at 512 and for premises’
arguments and goals set at 256 respectively. The batch size                Rating Score Description
                    ′
is set at 32, and |Pij | mentioned in 3.3 is set at 2. In contrast,        Match       1   Match to one of the premises used in the tactic.
the re-ranking model has its maximum position embeddings                                   Within the same module with any of the
set at 1,024. We set the batch size at 2, gradient accumula-              Relevant 0.3
                                                                                           premises used in the tactic.
                          ′
tion steps at 8, and |Pij   | at 8. We construct the pre-training         Irrelevant   0   Situations other than the two mentioned above.
corpus by concatenating states from the training set and all
premises’ argument lists and goals from the corpus. The
results of our method presented in Table 2 are obtained by                                                                                |P |
first training the retrieval model and selecting the top-100              strategies. Here, we represent a proof as P = {ti }i=1 ,
results as hard negative candidates. We then train the re-                which is a sequence of tactics, and apply Proof Length and
ranking model and use it to reorder the top-20 results from               Premise Frequency to characterize the proof, i.e.,
the retrieval stage. The experiments are conducted on 8                      ProofLength = |P |,
RTX 4080 servers.
                                                                                            1 X|P |
Baselines As mentioned above, ReProver (Yang et al.,                         PremiseFreq =           PremiseNum(ti ),
                                                                                           |P |  i=1
2024) is a model specifically trained on the Lean dataset,
using formal states and premises. Therefore, it serves as                 where PremiseNum(ti ) denotes the number of external
our primary baseline. Moreover, we retrain the model using                premise in a tactic. Proof Length reflects the complexity of
our dataset and following the setting in (Yang et al., 2024).             the proof, while the Premise Frequency indicates the degree
In addition to ReProver, we compare against several other                 of reliance on external theorems during the proof process.
commonly used retrieval models that have demonstrated                     Then, we apply the following four data split strategies to
strong performance in their specific domains.                             obtain four datasets:

• UniXcoder-base (Guo et al., 2022): It is one of the state-              • Random (RD): Randomly split the dataset.
  of-the-art code embedding models to transform code snip-
  pets into hidden vectors. It leverages multimodal data,                 • Reference Isolated (RI): Premises in the validation and
  such as code comments and abstract syntax trees (ASTs),                   test sets will not appear in the training set.
  to pre-train code representations.
                                                                          • Proof Length (PL): Sample proofs for the validation and
• E5-large-v2 (Wang et al., 2022): It is trained in a con-                  test sets weighted by Proof Length.
  trastive manner using weak supervision signals derived
  from a curated, large-scale text-pair dataset (referred to as           • Premise Frequency (PF): Sample proofs for the valida-
  CCPairs) and demonstrates strong performance on several                   tion and test sets weighted by Premise Frequency.
  English retrieval tasks.
                                                                          Each dataset contains 65,567 theorems for training, while
• BGE-m3 (Chen et al., 2024): It is distinguished for its ver-            the validation and test sets each contain 2,000 theorems.
  satility and excels in multiple functionalities, multilingual
  capabilities, and fine granularity retrieval tasks.                     4.2. Main Results
We fine-tune the three aforementioned baselines using our                 After training different models on the training dataset and
dataset. Following the parameters provided in (Chen et al.,               evaluating them on the corresponding test sets, we obtain
2024), we set the learning rate to 1e-5 and use a linear                  the results presented in Table 2. From this table, we can
scheduler. Due to server constraints, the batch sizes for the             observe that our method demonstrates exceptional perfor-
three models are set to 16, 8, and 6, respectively.                       mance, outperforming other baseline models. Specifically,
                                                                          UniXcoder-base (Guo et al., 2022), E5-large-v2 (Izacard
Metrics To evaluate the performance of various retrieval
                                                                          et al., 2022), and BGE-m3 (Chen et al., 2024) exhibit gen-
models, we utilize four widely adopted metrics: Precision,
                                                                          erally poor performance, which can be attributed to the
Recall, F1-Score, and nDCG. Since the nDCG considers
                                                                          substantial discrepancy between the pre-training corpora
the retrieved results’ relevance and position, it allows for
                                                                          used by these models (based on natural language data) and
multiple relevance levels. Following the setup in (Gao et al.,
                                                                          the Lean language. Although these models are fine-tuned,
2024), we define the relevance criteria in Table 1, which
                                                                          they cannot fully capture the core aspects of the Lean lan-
provides the relevance scores for calculating nDCG.
                                                                          guage due to Lean’s unique syntax and semantic features
Data Split To evaluate the performance of the model across                and thus suffer suboptimal performance. In contrast, the
different feature datasets, we employ four distinct data split            ReProver (Yang et al., 2024) model performs relatively well,

                                                                      6
                    Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization


                     Table 2. Premise selection results of our method and other baselines on different data splits.
                                   Recall                     Precision                 F1-score                      nDCG
 Split       Method
                            R@1 R@5 R@10 P@1 P@5 P@10 F@1 F@5 F@10                                           n@1       n@5      n@10
         UniXcoder-base 4.23 19.47 27.01               6.68     6.90    5.04     5.18 10.19        8.50     0.2283    0.3455    0.3958
         E5-large-v2        4.42 18.99 27.29           6.90     6.75    5.09     5.39     9.96     8.58     0.2313    0.3458    0.3952
  RD     BGE-m3             4.00 18.56 25.29           6.40     6.51    4.64     4.92     9.64     7.84     0.2374    0.3481    0.3930
         ReProver          11.79 28.78 36.69 19.80 10.90                7.23    14.78 15.81 12.08 0.3351              0.4072    0.4617
         Ours              15.17 38.20 46.53 26.80 14.87                9.30    19.38 21.41 15.51 0.3731              0.4698    0.5163
         UniXcoder-base 4.54 17.55 24.16               6.68     6.18    4.54     5.41     9.15     7.64     0.2303    0.3258    0.3768
         E5-large-v2        4.80 18.21 24.73           7.42     6.55    4.69     5.83     9.64     7.88     0.2356    0.3407    0.3878
  RI     BGE-m3             4.52 17.69 23.76           7.05     6.19    4.45     5.51     9.17     7.49     0.2306    0.3312    0.3788
         ReProver           5.05 14.26 19.48           9.30     5.77    4.10     6.54     8.22     6.77     0.2442    0.3059    0.3563
         Ours               7.79 23.38 30.91 14.76 9.30                 6.38    10.20 13.31 10.58 0.2731              0.3736    0.4322
         UniXcoder-base 3.94 15.45 22.72               6.70     5.66    4.32     4.96     8.29     7.25     0.1958    0.2804    0.3272
         E5-large-v2        3.66 14.65 21.65           6.25     5.47    4.23     4.61     7.96     7.08     0.1849    0.2735    0.3229
  PL     BGE-m3             3.99 14.65 20.53           7.06     5.41    3.92     5.10     7.90     6.59     0.1974    0.2781    0.3218
         ReProver          11.16 26.83 33.96 19.64 10.31                6.83    14.23 14.90 11.38 0.3059              0.3699    0.4232
         Ours              14.39 34.99 41.61 25.18 13.80                8.45    18.31 19.80 14.04 0.3479              0.4319    0.4781
         UniXcoder-base 2.69 15.03 21.91               5.19     6.92    5.43     3.54     9.48     8.70     0.2251    0.3426    0.3973
         E5-large-v2        3.08 14.44 22.11           5.84     6.70    5.39     4.04     9.16     8.67     0.2300    0.3464    0.4023
  PF     BGE-m3             2.59 13.85 20.05           5.42     6.27    4.86     3.51     8.63     7.83     0.2320    0.3404    0.3910
         ReProver           8.29 22.74 30.21 18.99 11.83                8.30    11.54 15.57 13.02 0.3257              0.3966    0.4544
         Ours              11.44 31.02 38.88 26.38 15.96 10.52 15.96 21.08 16.56 0.3764                               0.4693    0.5238


Table 3. Ablation studies on pre-training, tokenizer, and similarity calculation on Random split dataset for the CFR module. Here P means
the model is pre-trained or not, T means the model uses a new tokenizer or not, S means similarity calculation.
        Method                    Recall                     Precision                  F1-score                      nDCG
   P     T      S       R@1 R@5 R@10                  P@1 P@5 P@10 F@1 F@5 F@10                                n@1     n@5      n@10
   × × Eq. (3)           4.63     20.09     29.05      8.35    7.45      5.62     5.96 10.87        9.42      0.2443 0.3503 0.4030
   × ✓ Eq. (3)           4.93     20.49     30.33      8.04    7.50      5.79     6.11 10.98        9.72      0.2368 0.3493 0.4034
   ✓ × Eq. (3)           6.31     23.81     34.21     10.34 8.77         6.59     7.84 12.82 11.05 0.2484 0.3655 0.4240
   ✓ ✓ Eq. (2)           5.65     25.87     36.78      9.36    9.55      7.12     7.05 13.95 11.92 0.2382 0.3662 0.4238
   ✓ ✓ Eq. (3)           5.94     25.81     37.70      9.80    9.53      7.24     7.40 13.92 12.15 0.2422 0.3674 0.4293


likely due to its specifically designed parameter-tuning strat-        4.3. Ablation Studies
egy. Furthermore, ReProver utilizes ByT5 (Xue et al., 2022),
                                                                       Impacts of Pre-Training, Tokenizer, and Similarity Cal-
a byte-level tokenizer, which may allow the model to bet-
                                                                       culation We evaluate the impacts of pre-training the model,
ter handle the special symbols and structures in the Lean
                                                                       training the specific tokenizer for Lean, and the proposed
language. Our method, on the other hand, improves perfor-
                                                                       similarity calculation in Table 3, respectively. To ensure a
mance by retraining the tokenizer on the Lean corpus and
                                                                       fair comparison, we filter out the impact of the re-ranking
pre-training the retrieval model, allowing it to better adapt
                                                                       module and only compare the results provided by the re-
to the syntax and semantic features of Lean.
                                                                       trieval module. This table shows a performance improve-
For different data splitting strategies, we observe that ran-          ment when the model is pre-trained on the Lean corpus
dom data splitting is relatively easy. However, when the the-          compared to not performing pre-training. This indicates that
orems in the test set involve longer proofs or require a larger        the pre-training process helps the model acquire semantic
number of premises, the performance of the model tends to              information about Lean in advance. The experiment also
be lower. The reference isolated method, where the premises            shows that if we only pre-train the model without training
in the test set have not appeared during training, is the most         a new tokenizer, the performance when k = 1 is slightly
challenging. It requires the model to exhibit strong gener-            better but degrades a lot when k = 5 or 10. In addition, we
alization ability. Nevertheless, under each of these split-            evaluate the impacts of different similarity calculation meth-
ting strategies, our model consistently outperforms other              ods on the retrieval results. The results in Table 3 emphasize
baseline methods, which indicates that our model exhibits              the benefits of assessing similarity in a fine-grained manner.
superior adaptability.
                                                                       The Effect of Re-ranking We validate the effectiveness
                                                                       of using the proposed re-ranking module. As shown in

                                                                   7
                         Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization



                                                                                                                       16 Model Performance Comparison
                   2 X U V         2 X U V  Z  R  U H U D Q N         5 H 3 U R Y H U

                    RD                                                 RI
        50                                        50                                                                   14                                    Ours
                                                                                                                                                           w/ re-rank
        40                                        40                                                                                                        134.3M
                                                                                                                       12
 Recall@k




                                         Recall@k
        30                                        30                                                                                               ReProver
                                                                                                                       10




                                                                                                         Recall@1(%)
                                                                                                                                                   217.66M
        20                                        20
                                                                                                                             Ours
        10                                        10                                                                    8 w/o re-rank E5-large-v2
                                                                                                                            66.95M
                                                                                                                                          335.14M
         01   5     10       15     20             01              5   10         15       20                           6
                       k                                               k
                     PL                                                PF                                               4
        50                                        50                                                                       UniXcoder-base
                                                                                                                        2 125.93M          BGE-m3
        40                                        40                                                                                      567.75M
                                                                                                                        0 0 50 100 150 200 250 300 350
 Recall@k




                                         Recall@k




        30                                        30
                                                                                                                                            GFLOPs
        20                                        20
        10                                        10                                                Figure 5. The performance and efficiency comparison on Random
         01                                        01                                               split datasets. The size of each point reflects the parameter size of
              5     10       15     20                             5   10         15       20
                       k                                               k                            each model.


Figure 4. The Recall@k of our method with or without re-ranking                                     performance even improves when k = 1. These results
on each split, compared with ReProver.                                                              demonstrate that our retrieval model is robust to variations
                                                                                                    in the order of query states and the potential absence of
                                                                                                    certain local hypotheses.
Figure 4, when only the CFR module is used, our model
outperforms the ReProver only for larger values of k in Re-                                         Impact of Reduced Training Data The sparsity of data is
call@k (e.g., k ≥ 10). Applying the CAR module improves                                             an inherent challenge in formalization tasks. We test the sen-
the recall of our model when k < 10, so that our model can                                          sitivity of our retrieval model to the amount of training data.
consistently outperform ReProver and users are likely to find                                       The tests are conducted on the Random split dataset. The
useful premises in a relatively short list. Figure 5 presents                                       results in Figures 6 show that the model trained on the full
a comparison for our model and other baselines in terms                                             dataset outperforms the model trained on only 25% of the
of model size and inference GFLOPs. Without re-ranking,                                             data by approximately 25% in terms of k = 5, 10. The con-
our model achieves the lowest GFLOPs and it outperforms                                             sistent performance improvement suggests that there is still
in Recall@1 most of the baselines except ReProver. When                                             potential for further enhancement by increasing the amount
re-ranking the top-5 retrieval results by our CAR module,                                           of training data. When k = 1, the performance seems to
our model outperforms all the baselines and its GFLOPs                                              reach a bottleneck as the data size increases. Therefore,
and model size are comparable to those of ReProver.                                                 it may be necessary to incorporate re-ranking or explore
                                                                                                    alternative methods to further improve performance.
4.4. Robustness Experiments
                                                                                                    4.5. Theorem Proving Experiments
Effect of Data Perturbation Considering the generally
high quality of proofs in Mathlib, models trained on this                                           As mentioned in Section 3.3, we fine-tune ByT5 (Xue et al.,
dataset may be sensitive to the common issues of redundant                                          2022) and obtain a tactic generator. Facilitating the genera-
variables, missing conditions, and disordered sequences in                                          tor, we conduct theorem-proving experiments with retrieval.
the context of proof states, resulting in poor generalization                                       The results in Figure 7 show that assisted by our model, the
ability. We evaluate our retrieval model’s robustness to                                            generator averagely performs better than ReProver (Yang
low-quality inputs by perturbing the query states in the test                                       et al., 2024). Additionally, we evaluate our method on the
set. Specifically, we applied two perturbation strategies to                                        Minif2f benchmark (Zheng et al., 2022) using the model
a subset of the test data: shuffling the context or randomly                                        trained on the random split dataset. Our approach achieves
removing 20% of the context from states with a context                                              a pass@1 rate of 30.74%, while ReProver reached 28.28%,
length of 15 or more. As shown in Figure 6, all the metrics                                         indicating that our method is more effective. This means
exhibit a moderate decline as the perturbation ratio increases,                                     that retrieval-augmented language models are effective: For
with a maximum drop of approximately 6% when k = 5, 10                                              tasks such as formal theorem proving, which relies on exter-
compared to the unperturbed case. Especially, the model’s                                           nal theorem libraries, an effective retrieval model is expected

                                                                                                8
                                            Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

                     1.20                 Recall                                     1.4               Recall                                                       Ours   ReProver        Ours Avg   ReProver Avg
                                   R@1                                                          R@1                                                         0.350




                                                                                                                                Proved Theorem Percentage
                     1.15          R@5                                               1.3        R@5
                     1.10          R@10                                                         R@10                                                        0.325
  Normalized Value




                                                                  Normalized Value
                     1.05                                                            1.2                                                                    0.300
                     1.00                                                            1.1                                                                    0.275
                     0.95                                                            1.0                                                                    0.250
                     0.90                                                                                                                                   0.225
                     0.85                                                            0.9
                                                                                                                                                            0.200
                     0.80 0.00     0.25    0.50    0.75    1.00                      0.8 0.25     0.50      0.75   1.00                                     0.175
                                 Perturbation Proportion                                    Training Data Proportion
                                       Precision                                                   Precision                                                0.150
                     1.20                                                            1.4                                                                            RD         RI                PL       PF
                     1.15
                                   P@1                                                          P@1                                                                                 Data Split
                                   P@5                                               1.3        P@5
                     1.10          P@10                                                         P@10
  Normalized Value




                                                                  Normalized Value


                     1.05                                                            1.2                                                        Figure 7. Retrieval-augmented theorem proving results.
                     1.00                                                            1.1
                     0.95                                                            1.0
                     0.90
                     0.85                                                            0.9                                      researchers in the community.
                     0.80 0.00     0.25    0.50    0.75    1.00                      0.8 0.25     0.50      0.75   1.00
                                 Perturbation Proportion                                    Training Data Proportion          Although our method has yielded promising results, there
                                                                                                                              is still room for optimization in the retriever’s backbone
Figure 6. The variation of the normalized values of the model’s                                                               model. For the Lean premise retrieval task, the data cor-
metrics under different data perturbations and different training                                                             pus contains valuable semantic information, such as the
data proportion. In data perturbation experiments, the metric with                                                            hierarchy of Lean’s type system, that has yet to be fully
no perturbation v0 is adopted as baseline. The normalized value                                                               explored. Moreover, the results of theorem proving experi-
v ∗ = v/v0 . In data proportion experiments, the metric with 25%                                                              ments need further clarification with stronger provers, such
training data is adopted as baseline.                                                                                         as DeepSeek-Prover-V2 (Ren et al., 2025), to demonstrate
                                                                                                                              the effects of premise selection for automated theorem prov-
                                                                                                                              ing. In the future, we will focus on leveraging this untapped
to enhance generation performance.
                                                                                                                              semantic information more effectively and developing better
On test sets with high premise frequency but relatively short                                                                 models.
proof, our model performs better than ReProver, demonstrat-
ing the advantages of a more powerful retriever. In contrast,                                                                 Acknowledgements
on test sets with long proof but low premise frequency, our
model performs almost on par with ReProver. However, on                                                                       Yicheng Tao and Shanwen Wang are supported by Na-
the RD test sets, our model performs slightly worse than                                                                      tional Key Technologies R&D Program of China, Grant
ReProver, despite the improvement in retrieval accuracy.                                                                      No. 2024YFA1014001. Haotian Liu and Hongteng Xu are
We attribute this outcome to several factors. First, incor-                                                                   supported by Beijing Natural Science Foundation (Grant
porating retrieved premises into the prompt increases the                                                                     No. L233008), the fund for building world-class univer-
length of the context that the model must process compared                                                                    sities of Renmin University of China, and the funds from
to providing only the proof state. This imposes certain re-                                                                   Beijing Key Laboratory of Research on Large Models and
quirements on the model’s parameter size and architecture,                                                                    Intelligent Governance, and Engineering Research Center
as smaller models may struggle to accurately identify useful                                                                  of Next-Generation Intelligent Search and Recommenda-
information within longer contexts. We will explore this                                                                      tion, Ministry of Education. We thank Beijing International
issue in our future work.                                                                                                     Center for Mathematical Research(BICMR) at Peking Uni-
                                                                                                                              versity and Institute for Mathematical Sciences(IMS) at
5. Conclusion                                                                                                                 National University of Singapore for organizing Lean work-
                                                                                                                              shops, which provides great opportunities for learning and
In this paper, we propose an innovative method that lever-                                                                    communication.
ages data extracted from Mathlib4 to train a retrieval model
specifically designed for Lean premise retrieval. Experi-                                                                     Impact Statement
ments show that our method outperforms previous models
and demonstrates the potential of domain-specific smaller                                                                     The formalization community has been exploring the poten-
models in data-sparse tasks, such as formal premise retrieval.                                                                tial of AI tools as assistants. In this work we develop an
We have developed a search engine for premise retrieval                                                                       intelligent search engine for formal theorems based on proof
based on our model. We hope that our work can help ac-                                                                        states, aiming to accelerating the process of mathematical
celerate mathematical formalization and contributes to the                                                                    formalization.

                                                                                                                          9
                  Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

References                                                           (Volume 1: Long Papers), pp. 7212–7225, Dublin, Ire-
                                                                     land, May 2022. Association for Computational Linguis-
Barras, B., Boutin, S., Cornes, C., Courant, J., Filliatre,
                                                                     tics. doi: 10.18653/v1/2022.acl-long.499. URL https:
  J.-C., Gimenez, E., Herbelin, H., Huet, G., Munoz, C.,
                                                                     //aclanthology.org/2022.acl-long.499/.
  Murthy, C., et al. The Coq proof assistant reference
  manual: Version 6.1. PhD thesis, Inria, 1997.                    Harman, D. K. Overview of the third text retrieval confer-
                                                                     ence (TREC-3). Number 500. DIANE Publishing, 1995.
Chen, J., Xiao, S., Zhang, P., Luo, K., Lian, D.,
  and Liu, Z. M3-embedding: Multi-linguality, multi-               He, K., Fan, H., Wu, Y., Xie, S., and Girshick, R. Mo-
  functionality, multi-granularity text embeddings through           mentum contrast for unsupervised visual representation
  self-knowledge distillation. In Ku, L.-W., Martins, A.,            learning. In Proceedings of the IEEE/CVF conference on
  and Srikumar, V. (eds.), Findings of the Association               computer vision and pattern recognition, pp. 9729–9738,
  for Computational Linguistics: ACL 2024, pp. 2318–                 2020.
  2335, Bangkok, Thailand, August 2024. Association
                                                                   Izacard, G., Caron, M., Hosseini, L., Riedel, S., Bojanowski,
  for Computational Linguistics. doi: 10.18653/v1/2024.
                                                                      P., Joulin, A., and Grave, E. Unsupervised dense in-
  findings-acl.137. URL https://aclanthology.
                                                                      formation retrieval with contrastive learning. Transac-
  org/2024.findings-acl.137/.
                                                                      tions on Machine Learning Research, 2022. ISSN 2835-
Chen, T., Kornblith, S., Norouzi, M., and Hinton, G. A                8856. URL https://openreview.net/forum?
  simple framework for contrastive learning of visual rep-            id=jKN1pXi7b0.
  resentations. In International conference on machine             Karpukhin, V., Oguz, B., Min, S., Lewis, P., Wu, L.,
  learning, pp. 1597–1607. PMLR, 2020.                               Edunov, S., Chen, D., and Yih, W.-t. Dense passage
                                                                     retrieval for open-domain question answering. In Web-
De Moura, L., Kong, S., Avigad, J., Van Doorn, F., and von
                                                                     ber, B., Cohn, T., He, Y., and Liu, Y. (eds.), Proceed-
  Raumer, J. The lean theorem prover (system description).
                                                                     ings of the 2020 Conference on Empirical Methods
  In Automated Deduction-CADE-25: 25th International
                                                                     in Natural Language Processing (EMNLP), pp. 6769–
  Conference on Automated Deduction, Berlin, Germany,
                                                                     6781, Online, November 2020. Association for Computa-
  August 1-7, 2015, Proceedings 25, pp. 378–388. Springer,
                                                                     tional Linguistics. doi: 10.18653/v1/2020.emnlp-main.
  2015.
                                                                     550. URL https://aclanthology.org/2020.
Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. BERT:           emnlp-main.550/.
  Pre-training of deep bidirectional transformers for lan-         Li, C., Liu, Z., Xiao, S., Shao, Y., and Lian, D. Llama2vec:
  guage understanding. In Burstein, J., Doran, C., and               Unsupervised adaptation of large language models for
  Solorio, T. (eds.), Proceedings of the 2019 Conference of          dense retrieval. In Proceedings of the 62nd Annual Meet-
  the North American Chapter of the Association for Com-             ing of the Association for Computational Linguistics (Vol-
  putational Linguistics: Human Language Technologies,               ume 1: Long Papers), pp. 3490–3500, 2024.
  Volume 1 (Long and Short Papers), pp. 4171–4186, Min-
  neapolis, Minnesota, June 2019. Association for Compu-           Ma, X., Wang, L., Yang, N., Wei, F., and Lin, J. Fine-tuning
  tational Linguistics. doi: 10.18653/v1/N19-1423. URL              llama for multi-stage text retrieval. In Proceedings of the
  https://aclanthology.org/N19-1423/.                               47th International ACM SIGIR Conference on Research
                                                                    and Development in Information Retrieval, pp. 2421–
Gao, G., Ju, H., Jiang, J., Qin, Z., and Dong, B.                   2425, 2024.
  A semantic search engine for mathlib4.         In Al-
  Onaizan, Y., Bansal, M., and Chen, Y.-N. (eds.), Find-           Mikuła, M., Antoniak, S., Tworkowski, S., Piotrowski,
  ings of the Association for Computational Linguis-                B., Jiang, A., Zhou, J. P., Szegedy, C., Kuciński, Ł.,
  tics: EMNLP 2024, pp. 8001–8013, Miami, Florida,                  Miłoś, P., and Wu, Y. Magnushammer: A transformer-
  USA, November 2024. Association for Computational                 based approach to premise selection. In The 3rd Work-
  Linguistics. doi: 10.18653/v1/2024.findings-emnlp.                shop on Mathematical Reasoning and AI at NeurIPS’23,
  470. URL https://aclanthology.org/2024.                           2023. URL https://openreview.net/forum?
  findings-emnlp.470.                                               id=WgaVCqZeIU.
                                                                   Nipkow, T., Wenzel, M., and Paulson, L. C. Isabelle/HOL:
Guo, D., Lu, S., Duan, N., Wang, Y., Zhou, M., and Yin,              a proof assistant for higher-order logic. Springer, 2002.
 J. UniXcoder: Unified cross-modal pre-training for code
  representation. In Muresan, S., Nakov, P., and Villavi-          Nogueira, R. and Cho, K. Passage re-ranking with bert.
  cencio, A. (eds.), Proceedings of the 60th Annual Meet-           CoRR, abs/1901.04085, 2019. URL http://arxiv.
  ing of the Association for Computational Linguistics               org/abs/1901.04085.

                                                              10
                  Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

Qiao, Y., Xiong, C., Liu, Z., and Liu, Z. Understand-                the Association for Computational Linguistics (Volume
  ing the behaviors of bert in ranking. arXiv preprint               1: Long Papers), pp. 11897–11916, Bangkok, Thailand,
  arXiv:1904.07531, 2019.                                            August 2024. Association for Computational Linguis-
                                                                     tics. doi: 10.18653/v1/2024.acl-long.642. URL https:
Qu, Y., Ding, Y., Liu, J., Liu, K., Ren, R., Zhao, W. X.,            //aclanthology.org/2024.acl-long.642/.
  Dong, D., Wu, H., and Wang, H. RocketQA: An opti-
  mized training approach to dense passage retrieval for           Welleck, S. and Saha, R. llmstep: LLM proofstep sugges-
  open-domain question answering. In Toutanova, K.,                 tions in lean. In The 3rd Workshop on Mathematical
  Rumshisky, A., Zettlemoyer, L., Hakkani-Tur, D., Belt-            Reasoning and AI at NeurIPS’23, 2023. URL https:
  agy, I., Bethard, S., Cotterell, R., Chakraborty, T., and         //openreview.net/forum?id=ODOJuAM4Qj.
  Zhou, Y. (eds.), Proceedings of the 2021 Conference
  of the North American Chapter of the Association for             Xue, L., Barua, A., Constant, N., Al-Rfou, R., Narang, S.,
 Computational Linguistics: Human Language Technolo-                 Kale, M., Roberts, A., and Raffel, C. Byt5: Towards
  gies, pp. 5835–5847, Online, June 2021. Association                a token-free future with pre-trained byte-to-byte mod-
  for Computational Linguistics. doi: 10.18653/v1/2021.              els. Transactions of the Association for Computational
  naacl-main.466. URL https://aclanthology.                         Linguistics, 10:291–306, 2022.
  org/2021.naacl-main.466/.                                        Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao,             Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
  W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., Wu, Z. F.,               Leandojo: Theorem proving with retrieval-augmented
  Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D.,              language models. Advances in Neural Information Pro-
  and Ruan, C. Deepseek-prover-v2: Advancing formal                  cessing Systems, 36, 2024.
  mathematical reasoning via reinforcement learning for            Zheng, K., Han, J. M., and Polu, S. minif2f: a cross-system
  subgoal decomposition, 2025. URL https://arxiv.                    benchmark for formal olympiad-level mathematics. In
  org/abs/2504.21801.                                                International Conference on Learning Representations,
                                                                     2022. URL https://openreview.net/forum?
Robertson, S., Zaragoza, H., et al. The probabilistic rele-
                                                                     id=9ZPegFuFTFv.
  vance framework: Bm25 and beyond. Foundations and
  Trends® in Information Retrieval, 3(4):333–389, 2009.

Salton, G. and Buckley, C. Term-weighting approaches
  in automatic text retrieval. Information processing &
  management, 24(5):513–523, 1988.

Song, P., Yang, K., and Anandkumar, A. Towards large
  language models as copilots for theorem proving in lean.
  In The 3rd Workshop on Mathematical Reasoning and AI
  at NeurIPS’23, 2023. URL https://openreview.
  net/forum?id=C9X5sXa2k1.

Song, X., Salcianu, A., Song, Y., Dopson, D., and Zhou, D.
  Fast wordpiece tokenization. In EMNLP (1), pp. 2089–
  2103, 2021. URL https://aclanthology.org/
  2021.emnlp-main.160.

Taylor, W. L. “cloze procedure”: A new tool for measuring
  readability. Journalism quarterly, 30(4):415–433, 1953.

Wang, L., Yang, N., Huang, X., Jiao, B., Yang, L.,
 Jiang, D., Majumder, R., and Wei, F. Text embeddings
 by weakly-supervised contrastive pre-training. arXiv
 preprint arXiv:2212.03533, 2022.

Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R.,
 and Wei, F. Improving text embeddings with large lan-
 guage models. In Ku, L.-W., Martins, A., and Srikumar,
 V. (eds.), Proceedings of the 62nd Annual Meeting of

                                                              11
                                    Learning an Effective Premise Retrieval Model for Efficient Mathematical Formalization

A. Data Extraction
Several tools have been developed to extract data from a Lean project. To meet our requirements, we utilize the script from
LeanDojo and incorporate additional features. We applied this pipeline to Mathlib4 . The extracted information covers all
the premises and proofs in this project, along with metadata such as file dependencies. For each premise, we extract its
argument list and output. The proofs are lists of tactics, with the state before/after the tactics and premises used in each step.
Figure 8 illustrates the statistics related to context length and the number of premises in the dataset. The context length
represents the length of Γ, while the premise number indicates how many premises are utilized in a specific tactic. It is
important to note that tactics that do not have any premises are excluded from these statistics.


                                  Contexts Length Distribution                                                       Premise Number Distribution
                      0.06                                       Mean: 11.96                              0.20                           Mean: 3.39
                                                                 Std: 8.17                                                               Std: 2.95
                      0.05
Probability Density




                                                                                    Probability Density
                                                                                                          0.15
                      0.04
                      0.03                                                                                0.10
                      0.02
                                                                                                          0.05
                      0.01
                      0.00                                                                                0.00
                              0          20           40          60           80                                0         10       20         30
                                                   Length                                                                       Number
                             Figure 8. The probability density distribution of context lengths and premise numbers in the extracted dataset.




           4
               We used tag v4.10.0 of mathlib4. https://github.com/leanprover-community/mathlib4/tree/v4.10.0

                                                                                    12
