                                             CoProver: A Recommender System for Proof
                                                           Construction

                                        Eric Yeh? , Briland Hitaj, Sam Owre, Maena Quemener, and Natarajan Shankar

                                                        SRI International, Menlo Park, CA 94025, USA
                                        {eric.yeh,briland.hitaj,sam.owre,maena.quemener,natarajan.shankar}@sri.com
arXiv:2304.10486v1 [cs.LO] 1 Mar 2023




                                                Abstract. Interactive Theorem Provers (ITPs) are an indispensable
                                                tool in the arsenal of formal method experts as a platform for construc-
                                                tion and (formal) verification of proofs. The complexity of the proofs in
                                                conjunction with the level of expertise typically required for the process
                                                to succeed can often hinder the adoption of ITPs. A recent strain of
                                                work has investigated methods to incorporate machine learning models
                                                trained on ITP user activity traces as a viable path towards full automa-
                                                tion. While a valuable line of investigation, many problems still require
                                                human supervision to be completed fully, thus applying learning methods
                                                to assist the user with useful recommendations can prove more fruitful.
                                                Following the vein of user assistance, we introduce CoProver, a proof rec-
                                                ommender system based on transformers, capable of learning from past
                                                actions during proof construction, all while exploring knowledge stored in
                                                the ITP concerning previous proofs. CoProver employs a neurally learnt
                                                sequence-based encoding of sequents, capturing long distance relation-
                                                ships between terms and hidden cues therein. We couple CoProver with
                                                the Prototype Verification System (PVS) and evaluate its performance
                                                on two key areas, namely: (1) Next Proof Action Recommendation, and
                                                (2) Relevant Lemma Retrieval given a library of theories. We evaluate
                                                CoProver on a series of well-established metrics originating from the rec-
                                                ommender system and information retrieval communities, respectively.
                                                We show that CoProver successfully outperforms prior state of the art
                                                applied to recommendation in the domain. We conclude by discussing
                                                future directions viable for CoProver (and similar approaches) such as
                                                argument prediction, proof summarization, and more.




                                        1     Introduction


                                        Interactive theorem proving (ITP) is a well-entrenched technology for formalizing
                                        proofs in mathematics, computing, and several other domains. While ITP tools
                                        ?
                                            This research was, in part, developed with funding from the Defense Advanced Re-
                                            search Projects Agency (DARPA). The views and conclusions contained in this doc-
                                            ument are those of the authors and should not be interpreted as representing the
                                            official policies, either expressed or implied, of the U.S. Government or DARPA.
2     Yeh et al.

provide powerful automation and customization, the task of manually guiding
the theorem prover toward QED is still an onerous one. For inexperienced users,
this challenge translates to crafting mathematically elegant formalizations, iden-
tifying suitable proof commands, and diagnosing the root cause of failed proof
attempts. Whereas for the expert users, the challenge consists in navigating a
large body of formalized content to ferret out the useful definitions and the right
lemmas. Both novice and expert users can benefit from recommendations in the
form of proof commands and lemma retrieval that can guide proof construction.

The goal of the present project is to scale up proof technology by introducing
CoProver as a proof recommender system that discerns suitable cues from the
libraries, the proof context, and the proof goal to offer recommendations for
ITP users. Building on the proof technology and proof corpora of the Proto-
type Verification System (PVS) a state-of-the-art proof assistant [34], we focus
on recommendations for two key tasks in ITP: Suggesting PVS commands and
lemmas. The first is to recommend the likely command an expert user would take
given the current proof state. As the number of possible commands can number
over 100, recommending steps an expert may take would be beneficial, particu-
larly for novices. The second is to identify lemmas for inclusion from a library
of lemmas that may help with forward progress on a proof. Currently, only lem-
mas from user-imported theories are considered and selection of a lemma relies
on user familiarity with candidate theories and their lemmas. For the problems
PVS is commonly employed on, there are usually several hundred theories with
thousands of possible lemmas combined to consider. At this scale, even expert
users with decades of experience may not be aware of all possible lemmas (or
even their names) that may be relevant for their proof. A mechanism that can
automatically identify relevant lemmas at scale would be desirable.

In order to develop these two capabilities, we leverage the expert proof traces for
NASA’s PVS Library 1 (PVSLib), a large collection of highly polished formal
developments centered on safety-critical applications, and the PVS Prelude, a
collection of theories built into PVS. We aim to capture the expertise and in-
tuition of the developers by training systems to emulate user decisions on these
completed proofs.

Key to our approach is the use of recent machine learning techniques that can
capture sequential information across a greater window than previously possible.
Indeed, we show how application of these methods over a simple sequence-based
encoding of formulas can better capture relationships between proof states with
commands and libraries than prior sequence encoding techniques.

We start with an overview in Section 2 of the CoProver system, describing the
core recommendation tasks. We describe each approach and contrast it against
prior literature. Section 3 contains implementation details of how sequents and
1
    https://shemesh.larc.nasa.gov/fm/pvs/PVS-library/


    Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                     CoProver        3

states are featurized into a common representation used to provide inputs for the
command prediction and lemma retrieval capabilities. Sections 4 and 5 provide
specific details of how these are implemented, along with experiments detailing
their effectiveness described in Section 6. Section 7 describes deployments of this
capability on PVS, initial user evaluations of these capabilities, and Section 9
concludes with a discussion of future directions.



2     CoProver Overview


            [-1] exists x : ...                                     Command
            [-2] x > x - 5                                          Prediction
                                          Featurization
            {1} forall x: exists y: ...
                                                                 Lemma Retrieval
                  Sequent

Fig. 1: The CoProver system. A sequent is featurized, and this is representation
is used to provide command recommendations and retrieve relevant lemmas.


Figure 1 illustrates the CoProver system. The Featurization step converts the
structured logical formula of the sequent and other information constituting the
proof state, such as previous commands, into a token sequence that can be later
ingested by the transformer model. This sequence is provided to the Command
Prediction and Lemma Retrieval modules. Command Prediction identifies the
next likely command an expert user would take in successful proofs, given similar
states. When a lemma is to be imported, Lemma Retrieval examines the state
and suggests the most relevant ones from a given library, based off of a history
of human-selected lemmas that have progressed their proofs.

Both Command Prediction and Lemma Retrieval use RoBERTa[28] to encode
the proof state sequence tokens. RoBERTa is a Transformers-based neural lan-
guage model [42], which can learn long-range sequences of terms useful for per-
forming a downstream task. Unlike n-grams or other Markov window methods,
Transformers employ a self-attention mechanism that lets tokens employ a wider
range of neighboring tokens to generate a representation suitable for a down-
stream task. The token-level representations are real-valued vectors that can be
tailored to perform for a variety of tasks, and have been used to give state-of-
the-art performance across multiple tasks such as large language modeling, text
classification, and visual understanding. In our case, the RoBERTa-based encod-
ing of the proof state is used as input to a multinomial classifier for predicting
the next command an expert user would take. Backpropagated error from the
classifier is used to adjust, or to fine-tune these representations make them more
suitable for the classification task.


    Distribution Statement A – Approved for Public Release, Distribution Unlimited
4     Yeh et al.

Lemma retrieval is the task of identifying which lemmas from an existing library
of theories may be relevant to include to help with performing forward progress
on a proof. This task is made challenging by the fact that a potentially useful
lemma may exist in a theory that the user is not aware of or might not recall
the name of, and therefore would not import into the proof. This use case has
strong connections to the document-retrieval problem in information retrieval
(IR) [31], where the goal is to identify which documents in a collection are most
relevant to a search query. A particular challenge is the fact that IR models
rely on overlap and term rarity heuristics for relevance. While the assumptions
that motivate these heuristics work for natural documents and queries, whether
they hold for theorem proving is in question. To account for this, CoProver uses
a training set of lemma import decisions by users to fine-tune the RoBERTa-
derived proof state representations to learn combinations of proof state and
lemma symbols that prove useful for identifying relevant lemmas from a given
database of lemmas.



3     Data Generation


3.1    Datasets


For both command prediction and lemma retrieval, we used proof sequences
from the PVSLib library, a large set of formal developments containing theorems
proofs for a variety of mathematical and engineering areas. In total PVSLib
contains 184, 335 proof steps. We note that these are completed and polished
proofs so that backtracked sequences of steps are pared and only the successful
sequence of proof commands and imported lemmas are retained.



3.2    Featurization


In order to convert the logical formulas into a representation amenable to ma-
chine learning, we convert the structured representation into a token sequence.
While the original PVS is a well-structured formal language, featurization is still
required for several reasons. First, our models used RoBERTa to encode PVS
proof states and lemmas. As Transformer models have fixed width input, a more
parsimonious encoding that strips away boilerplate while retaining the original
semantics will allow longer formulas to work without truncating them. Many
formulas use names for variables and constants that are specific to that proof or
theory, and having the model learn these names would reduce the generalization
ability of the model.


    Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                         CoProver         5

Given this, all symbol names for functions and operators are copied over as-
is. Constant and variable names are replaced by a generic placeholder. Integer
values are retained. Syntactic constructs such as parentheses are excluded and
not included in the featurized form, as the ordering of the above can roughly
capture the syntactic arrangement of the original form.

An example of the input and output of this process is given in Figure 2. Here,
symbols such as the forall quantifier and implication operator are preserved,
while the variables f, high, and low are replaced with their type, nat repre-
senting the natural numbers.



FORALL (F: nat, high:nat, low:nat):
    (bool_à (reals_>= high low) (equalities_= …   FORALL NAT NAT NAT bool_à reals_> NAT NAT…



                     PVS                                      Featurized

Fig. 2: Featurization converts formulas in PVS (left) into a more machine learning
friendly token stream (right).




Following previous work in Transformer-based encodings, we use special tokens
<ant>, <cons>, and <hid> to mark regions of tokens corresponding to for-
mulas in the sequent’s antecedent
                    CMD1          and consequent.
                          <ANT><CONS>FORALL       The
                                              NAT …    last corresponds to hid-
                                                    <HID>…
den formulas, a feature of PVS that allows the user to reserve certain formulas
from being operated on by commands.

For command prediction, we prefix all token streams with a cmd1 special to-
ken. This acts as a bias term for this task and can be used to condition the
Transformer model for multi-task learning. The lefthand side of Figure 3 gives
an example of a featurized sequent with no antecedents and one consequent.

Our current setup makes the Markov assumption, that only the current state is
sufficient for making our predictions. At least anecdotally knowing which com-
mands were performed can inform what steps are taken next, so incorporating
previous commands can capture some non-Markovian information. This is done
by adding the previous three commands issued by the user to the state repre-
sentation after the cmd1 token.

For the lemma retrieval experiments, we modified the above procedure to allow
constant and variables to be replaced with their type name. This was done to
allow matching by type, as arguments for imported lemmas also need to match by
type. Higher-order and custom types are currently represented by a placeholders.
Accounting for matches on higher-order types and on advanced type operations
such as predicate-based approaches is reserved for future work.


  Distribution Statement A – Approved for Public Release, Distribution Unlimited
6       Yeh et al.

We use the Byte Pair Encoding (BPE) [40,10] from the Huggingface Trans-
formers Library [45] to train a token vocabulary customized for the featurized
formulas (sequents and lemmas). BPE encodes words as a sequences of byte pairs
instead of singular tokens. This reduces the size of the vocabulary required, as
rare words can be encoded using byte pairs and do not need to be memorized,
while common words can be encoded in their entirety to improve efficiency. This
also introduces a tolerance for new terms, which can be assembled from suitable
byte pair sequences.

As with many other Transformers based encoders, RoBERTa is first trained
in a self-supervised fashion. Given unlabeled data, one can generate labeled
versions through operations where the ground truth can be determined. Masked
language modeling is one such task, where a supervised prediction problem can
be constructed by masking the identity of the word, and then asking the model
to predict that word [7]. By conducting this type of self-supervised training on a
large corpus, the resulting representations can capture distributional information
about the domain that can make training downstream components easier.

For our experiments, the language model was trained for 1, 100, 000 steps over
our dataset, using the default set of self-supervised language tasks used to train
RoBERTa.



4       Command Prediction


                                                                              skolem


|----
    FORALL (F: nat, high:nat, low:nat):
        (bool_à (reals_>= high low)
        (equalities_= …


CMD1 <ANT><CONS>FORALL NAT NAT NAT        CMD1   <ANT>   <CONS>   …   NAT
bool_à … <HID>…<S>



Fig. 3: The process for featurizing a sequent and then using repeated self-
attention to create representations capturing information for predicting the next
command.


The goal of the command prediction task is to identify the next command an
expert user may likely take given the current step in the proof. To make this pre-
diction, we use the T5 sequence to sequence training framework [36] implemented
in Huggingface [45]. Here, the RoBERTa encoding of the featurized proof state
is used as input to output the command the expert user took given the proof
state. Figure 3 illustrates how a command prediction is made. First the sequent is


    Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                     CoProver        7

featurized into a token sequence, which are converted into classification-suitable
representations via repeated applications of self-attention. These are then inte-
grated by the classifier, which writes out the next likely command. As with most
classifiers, the top-N most confident hypotheses can be emitted, allowing for a
window of predictions to be generated.



5     Lemma Retrieval



                           forall int … ⊢…




                                               RoBERTa



                                                         Pooling
                                                          Avg
                               Sequent

                                                                    0..1
             BEGIN elt: U players_set: TYPE+
                                               RoBERTa



                                                         Pooling
            = non_empty_finite_set[U] …




                                                           Avg
                                Lemma

Fig. 4: Siamese architecture used to determine whether a lemma is relevant to a
given sequent.


As previously mentioned, we treat lemma retrieval as an information retrieval
problem, where the proof state acts as the query against a library of avail-
able lemmas. Given we have a large corpus of user-performed lemma imports in
the PVSLib proof traces, we can use it to train a neural information retrieval
approach [32], which learns a relevance ranking function from these examples.
CoProver takes this approach as the assumptions used to determine relevance
between queries and natural language may not apply to matching proof states
with lemmas. A supervised neural architecture can learn the best combination
of features for assessing relevance of a lemma to a sequent. Figure 4 illustrates
how the sequent and lemma are encoded and compared to assess relevance. The
architecture follows a Siamese Network [5], implemented in the SBERT [37]
framework. Given two inputs, Siamese networks encode them into a common
representation which is scored typically by comparing the input representations
with a tensor operation such as cosine similarity or dot-product. Supervised
training causes the architecture to learn feature combinations and weightings
that are useful for computing the score. When a fast operation such as cosine
similarity is used to compute the score, comparisons can be extremely efficient
as the bulk of the representations can be pre-computed. This approach has been
used to learn ranking functions for tasks with a large amount of data, such as
using clickthrough data to rank queries and documents [16]. In CoProver, the
token sequences for the logical formulas representing the lemma and sequent are
passed to the RoBERTa encoder to construct token-level representations. These


    Distribution Statement A – Approved for Public Release, Distribution Unlimited
8     Yeh et al.

representations are averaged to give a single vector characterizing the content
of the lemma or the sequent. Finally, the relevance of the lemma and sequent
vectors is scored using cosine similarity, with 0 indicating no relevance and 1
indicating maximal relevance.



6     Experiments and Results

We detail the experimental setup and results for the Command Prediction and
Lemma Retrieval tasks.



6.1    Command Prediction


From the full PVSLib library of proofs, we subsampled 20, 000 proof steps to
create a tractable training set 2 . From these we randomly sampled 90% of these
pairs for the training data, and used the remaining 10% as a held out test-set.

For CoProver, we trained on this data for 10 epochs on four NVIDIA GeForce
RTX 3090 cards using distributed data parallel training (DDP) [26] implemented
using PyTorch Lightning 3 . As each card in DDP contains its own model, we
selected the one with the best validation set error. As baselines for comparison,
we follow prior literature on tactic prediction [11] and used classifiers trained over
term-frequency inverse document frequency (TF-IDF) [30,21] weighted feature
counts of symbols observed in the sequent. TF-IDF incorporates frequency of
occurrence of a term and its distinguishability against the backdrop of the entire
collection. Here, the sequents are represented as a vector, with each dimension
corresponding to a symbol in the vocabulary and weighted by TF-IDF. In order
to make a fair comparison, these were derived from the same featurized token
stream used by CoProver. To strengthen this type of approach, we experimented
with multiple classifiers for the baseline: Linear support vector classifier (Linear
SVC), support vector machines using a radial basis kernel (RBF) and one using
a polynomial kernel (Poly), and a k-nearest neighbor classifier (k-NN). We used
the Scikit-Learn4 implementations with default parameters unless specified. For
the k-nearest neighbor classifier, we used a distance weighted variant with n = 5
following prior literature [11].

Table 1 shows the test command predication accuracy for each of the methods
with the sequent and command history, and without the command history. We
2
  Initial experiments with larger samples showed no difference in performance with a
  system trained with the smaller set
3
  https://www.pytorchlightning.ai/
4
  https://scikit-learn.org/


    Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                   CoProver        9


Table 1: Command prediction test accuracies by method, with and without com-
mand history information.
  Method     Acc. cmdhist + sequent Acc., sequent only Acc., cmdhist only
Linear SVC        0.30 ± 1.1 × 10−2      0.20 ± 9.1 × 10−3    0.30 ± 1.1 × 10−2
SVM (RBF)         0.29 ± 1.0 × 10−2      0.22 ± 9.5 × 10−3    0.30 ± 1.0 × 10−2
SVM (Poly)        0.20 ± 8.9 × 10−3      0.20 ± 8.9 × 10−3    0.22 ± 1.0 × 10−2
   k-NN           0.28 ± 1.0 × 10−2      0.19 ± 8.6 × 10−3    0.27 ± 9.6 × 10−3
 CoProver        0.48 ± 7.3 × 10−3       0.28 ± 9.8 × 10−3    0.21 ± 9.3 × 10−3



find that the CoProver predictions are more accurate than the baselines when the
full sequent and command histories are used. Of note is the fact that most of the
accuracies for the baseline methods is from the command history itself, whereas
CoProver is able to integrate the sequent and command history together to
achieve a significantly higher value than the next-best baseline, k-NN. Variances
for each method were estimated using bootstrap resampling [8] and significance
was determined using a two-sample t-test with α = 0.001.



Table 2: Command prediction accuracy for baseline methods using features that
incorporate more structural information (left to right).
                            Method     n=1 n=2 n=3
                           Linear SVC 0.30 0.37 0.30
                           SVM (RBF) 0.29 0.32 0.33
                           SVM (Poly) 0.20 0.18 0.19
                              k-NN    0.28 0.30 0.32



In order to determine the significance of structural information for this task,
we experimented with TF-IDF sequent featurizations of increasing maximum
n-gram degree. Here, a n-gram featurization consists of all symbol sequences of
length n. At n = 1, only single symbols are used and thus no structural informa-
tion is encoded. In contrast, n = 3 uses all observed combinations of up to three
symbols in sequence and contains considerably more of the sequent structure.
Table 2 shows the accuracies for each classification method by the maximum
n-gram degree. With the exception of the SVM using the polynomial kernel
(SVM Poly), every method benefits from increasing structural information. We
suspect that model’s poorer performance may be due to the greater number of
hyperparameters given the polynomial kernel, which greatly increases the risk
of overfitting on sparse data [14].

Recommender systems often present the top N -most relevant predictions for the
user, instead of presenting just the top recommendation. In many domains users


  Distribution Statement A – Approved for Public Release, Distribution Unlimited
10    Yeh et al.

                                             Command Prediction, Accuracy at N
                  0.8
                        cmdhist
                        sequent
                  0.7   cmdhistory+sequent
                        baseline
                  0.6
       Accuracy   0.5

                  0.4

                  0.3

                  0.2


                               2                  4               6              8   10
                                                          Top-N
Fig. 5: Command prediction test accuracies by method, with and without com-
mand history information.


can easily scan a set of candidates and choose the best one. Alternately, in other
cases the context provided by multiple candidates can provide useful informa-
tion as well. To assess how well CoProver can perform in this regime, we assess
the top-N test set accuracy, where matches are made if the correct prediction
is within the top N predictions. Figure 5 shows the accuracy of the CoProver
system at different sizes of N using just the command history (cmdhist), se-
quent (sequent) and both (cmdhist+sequent) for N ranging from 1 to 10. For
comparison, we also include the baseline guess, where the top-N most frequent
commands in the training set are used as the candidate window. We find that
the combination of sequent and command history information gives consistently
higher accuracy than using either alone, while all methods outperform the base-
line. Observe that the accurate command is present in the top-7 response over
70% of the time.



6.2   Lemma Retrieval


For lemma retrieval, we winnowed the PVSLib proof steps to lemma commands
that imported a lemma into the proof. We restricted our analysis to explicit
imports: While there are several other commands that also import lemmas, they
do so as an implicit part of their operation and may have additional side effects.
From these 20, 221 steps, we randomly selected 12, 132 of them for training
lemma retrieval models, with 8, 089 for testing. These proofs reference libraries
in both PVSLib and PVS Prelude, giving a total of 9, 468 possible candidate
lemmas.

This model is trained on lemma commands in the training set of proof sequences
in the PVSLib. For each lemma invocation, we record the sequent at that point


  Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                  CoProver      11

in the proof and the name of the referenced lemma. PVSLib has 20, 221 lemma
pairs in the proofs for PVSLib. These consist of the sequent state when the
import lemma command was issued by the user and the name of the lemma. We
randomly split them into 12, 132 train and 8, 089 test pairs. This is against a
combined library of PVS and PVSLib theories, with a total of 747 theories and
9468 available lemmas.

For training the Siamese network, the observed sequents and lemmas in the
training invocations have a score of 1. An equal number of sequent and lemma
pairs were sampled, with their score set to 0, following the rationale that a
randomly selected lemma would very likely not be relevant for progressing for a
given sequent.

We evaluated the resulting network on the test pairs. We measured how well each
method performed using mean reciprocal rank (MRR), an evaluation measure
commonly used in information retrieval to assess how highly compared methods
can rank relevant documents from a corpus [31]. MRR is computed from the
rank position of the ground truth lemma in the relevance-ordered scores given
the sequent. For a given test pair consisting of a sequent s, selected lemma lgt
and library of lemmas L with lgt ∈ L, we use the Siamese network to score how
relevant lemma l ∈ L is to the sequent, frel (s, l). We derive a rank ordering over
all lemmas L,


                                             N
                                         1 X 1
                                M RR =
                                         N i ri


Where ri is the rank of the ground truth lemma for the ith lemma pair. Thus
higher MRR values indicate the scoring method does a better job of assigning
higher relevance to ground truth documents.


                                 Method MRR
                                Baseline 0.0015
                                 Count 0.0030
                                TF-IDF 0.043
                                CoProver 0.51


We find that the CoProver approach to outperform the other methods for iden-
tifying relevant lemmas with their sequents, including the TF-IDF bag-of-words
representation used by previous work. A MRR of 0.51 corresponds to an average
mean rank of 1.98, which corresponds to the relevant lemma appearing around
position 2 in a score-based rank ordering of all lemmas.


  Distribution Statement A – Approved for Public Release, Distribution Unlimited
12      Yeh et al.

7      Deployments


CoProver is currently available as a web-application backed services for PVS. We
took the command prediction and lemma retrieval models and wrapped these
up as web services in the Flask5 framework. To request a command prediction
or a relevant lemma, the calling component converts the current sequent into a
JSON formatted message. Hypotheses are returned as JSON objects, which are
presented in PVS directly.

We are preparing this recommender-augmented version of PVS for a large user
study to assess how useful these capabilities are to end users. However, internal
developers have found the capability to generally give good suggestions, when
presenting the top 5 commands.

The code and the data used for this work are open-sourced and will be available
at https://github.com/coproof.



8      Related Work


In the last decade, there has been a significant amount of activity in apply-
ing machine learning to automated deduction. The progress is summarized in
an invited talk by Markus Rabe (Google Research) at the 2021 CADE con-
ference [35]. Prior work on using machine learning in theorem proving can be
classified in terms of the predictive goal of machine learning as


1. Learning search heuristics (E-prover [38], SAT/SMT solvers [3]): The sys-
   tems ENIGMA [18], MaLeCoP [41] and FEMaLeCoP [22] augment a tableau-
   based prover LeanCoP [33] with a naïve Bayes classifier for clause selection.
   Graph neural nets have been used to predict the clauses that are in the
   unsatisfiable core set of clauses from a clause set [39] and to guide SMT
   solvers [1].
2. Premise selection from a library of facts (DeepMath [17], CoqHammer, HOLy-
   Hammer, HOList [2], Thor [19]): Several proof assistants invoke hammers
   (theorem provers and SAT/SMT solvers) on each subgoal together with a
   set of background lemmas (the premises). These hammers can fail if there
   are too many premises. Machine learning has been used to identify the most
   promising premises to pick from the background library [24]. As with tac-
   tic selection below, a range of learning techniques have been employed for
   premise selection, including sequence, tree, and graph representations [43].
5
     https://flask.palletsprojects.com/


    Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                  CoProver     13

3. Step or tactic selection (GPT-f, Holophrasm [44], CoqGym [47], HOL4RL [46],
   HOList [29], GamePad [15], Tactic-Toe [11], proof synthesis [9,20,25]): In-
   teractive proof assistants build proof trees by applying tactics to goals to
   generate zero or more subgoals. The SEPIA system [13] predicts tactics for
   the Coq proof assistant based purely on analyzing proofs. GPT-f uses the
   GPT-3 transformer model to train on Goal/Proof pairs from the Metamath
   corpus (augmented with synthesized proofs) to predict the proof given the
   goal. This is used to construct a proof tree by applying the proof steps sug-
   gested by the model to the open subgoals in the tree. The system was able
   to find shorter proofs for 23 theorems in the Metamath corpus. CoqGym [47]
   uses a much larger training corpus spanning 71,000 proofs from various Coq
   libraries. TacticToe [12] is trained on proofs from HOL4 libraries and com-
   bines tactic prediction using k-nearest neighbors with A* search, and in
   some cases yields better (more perspicuous and maintainable) proofs than
   the alternatives using Hammers. IsarStep [27] uses a transformer encoding
   to identify intermediate formulas in a declarative Isar proof. ML4PG [23]
   extracts useful statistical patterns from higher-order logic proofs using un-
   supervised learning techniques like K-Means clustering.



Learning to predict the next command from user activity traces has been ex-
amined in works such as TacticToe [11]. However, the focus of this work was
on the ability of the system to fully automate the proof, and performance was
measured in terms of the lift in number of proofs that can be completed with-
out human assistance. To our knowledge, prior work has not examined how well
these systems can predict the next step a user would take to make progress.

In addition, previous work has also featurized sequents using a “bag-of-words”
approach, where the proof state is characterized as a histogram of the tokens
observed in the sequent. While pairs of histograms of pairs of adjacent tokens
can retain some sequentiality, this approach can ablate longer-range structural
information that may be valuable for tasks such as prediction. In contrast, Co-
Prover leverages neural language modeling technology that can learn sequential
combinations of tokens over longer ranges.

Treating lemma retrieval as an information retrieval problem has been done
in prior work [4,11]. As with most IR methods, these works use a weighted
histogram of terms observed in the sequent (query) and lemma (document) to
characterize them. While this “bag-of-words” approach removes sequentiality and
thus structural information, it turns out the overlap in vocabulary use between
a query and candidate document can act as a good approximator for search
relevance. Terms are relevance weighted using term-frequency inverse document
frequency (TF-IDF) [30,21], which incorporates frequency of occurrence of a
term and its distinguishability against the backdrop of the entire collection. The
similarity comparison is usually performed using a fast computational method,

  Distribution Statement A – Approved for Public Release, Distribution Unlimited
14      Yeh et al.

such as strict dot products or cosine similarity, so a query can be tractably
performed against a large collection of candidate documents.

However, bag-of-words modeling and the TF-IDF weighting scheme are assump-
tions targeting how relevance appears for natural language queries and docu-
ments. Logical formula observed in lemmas and sequents may not exhibit the
same behavior, particularly for determining if a lemma is relevant to moving
proof progress in a sequent. Indeed, neural information retrieval has focused on
using supervised queries and document pairs to learn relevance functions that
may not be captured by assumptions taken in standard IR modeling.



9     Conclusions


In this work, we have demonstrated how a simple featurization of proof state can
be used to perform two recommendation tasks, predicting next commands and
retrieving relevant lemmas. For command prediction, CoProver’s approach has
been shown to outperform prior methods, giving significantly higher accuracies.
In the context of recommendation systems, showing the top 3 − 5 commands
is a reasonable amount, with these windows capturing 50% − 70% of the origi-
nal prediction correctly on the validation set. As with systems trained on user
interaction traces, there will are often many cases where the system can learn
a solution that the original user did not consider. As one internal user com-
mented, the application of an automated hammer (the grind command) in a
convergence proof was unexpected, but lead to completion of the proof. Simi-
larly, using a neural learning approach with CoProver’s featurization can give
significantly better performance on lemma retrieval, in comparison with retrieval
using IR-derived baselines.

In spite of these results, we note that the neural learning mechanism are not
necessarily learning deep reasoning structures, and may more likely be learning
complex structural cues. Indeed, an analysis of large language models found
them to be impressive memorization machines that are incapable of performing
arithmetic [6]. A cursory examination of the attention heads in the command
prediction task revealed the model’s attention weightings did not consistently
align with experienced users’ intuitions about what should govern the direction
of the proof.

Future directions of proof command recommendation include identification of
arguments used for these commands. These primarily consist of the formula
to use, but in some cases more complex arguments are needed. Of particular
interest is pairing this capability with explanation mechanisms. Perhaps the
simplest explanation capability is to run the top-N commands in the background
and displaying the results provides a look ahead capability that allows users to

    Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                  CoProver     15

see the envelope of outcomes. When paired with heuristics that measure proof
completion, this may be beneficial for developing an intuitive understanding.

To the best of our knowledge, we are the first work to assess and evaluate lemma
retrieval as an information retrieval problem. Previous work on lemma retrieval
focused on whether or not a selected lemma can progress a proof towards com-
pletion in an automated solver. While this does cover situations where multiple
lemmas may be relevant to automatic proof completion, for the type of prob-
lems addressed by interactive theorem provers, automatic completion may not
be feasible. However, importing a lemma can help progress the proof and thus
can be considered relevant, similar to how retrieving the right document can
help a querying user perform a task.

To that end, we have demonstrated how a neurally trained architecture can
determine which lemma a human user would have selected for making progress on
a proof given the sequent. This approach can provide a better relevance ranking
for lemmas, as opposed to the representation and scoring methods discussed in
previous work.

Note that from our data setup, only the lemmas selected by the user are con-
sidered to be relevant for the given sequent. This disregards the possibility that
another lemma may be just as useful for the proof as well. However, this is a
well known issue in natural language information retrieval corpora, and measures
such as MRR are used to compare system performance as opposed to acting as
a standalone performance measure.

Possible future work in this area can focus on analyzing relevant structural el-
ements that trigger a match between a sequent and a lemma. While the final
comparison is performed using a cosine similarity computation, the nature of the
highest scoring feature matches can be hard to discern. In particular, it is pos-
sible that the formula for the lemma and sequent may not have much apparent
overlap, but relevant token sequences may map to the same feature.

For future work, we are examining the application of CoProver’s Transformer
based sequent representation towards tasks such as nominating witnesses, proof
repair, and developing a measure for proof progress.




Acknowledgements This material is based upon work supported by the De-
fense Advanced Research Projects Agency (DARPA) under Contract No. HR00112290064
and by the National Institute of Aeronautics. Any opinions, findings, and conclu-
sions or recommendations expressed in this material are those of the author(s)
and do not necessarily reflect the views of the United States Government or
DARPA.

  Distribution Statement A – Approved for Public Release, Distribution Unlimited
16    Yeh et al.

References

 1. Balunovic, M., Bielik, P., Vechev, M.T.: Learning to solve SMT formulas. In:
    NeurIPS. pp. 10338–10349 (2018)
 2. Bansal, K., Loos, S., Rabe, M., Szegedy, C., Wilcox, S.: Holist: An environment
    for machine learning of higher order logic theorem proving. In: International Con-
    ference on Machine Learning. pp. 454–463. PMLR (2019)
 3. Biere, A., Heule, M., van Maaren, H., Walsh, T. (eds.): Handbook of Satisfiability.
    IOS Press (2009)
 4. Blanchette, J.C., Greenaway, D., Kaliszyk, C., Kühlwein, D., Urban, J.: A learning-
    based fact selector for isabelle/hol. Journal of Automated Reasoning 57, 219–244
    (2016)
 5. Bromley, J., Guyon, I., LeCun, Y., Säckinger, E., Shah, R.: Signature verifica-
    tion using a "siamese" time delay neural network. Advances in neural information
    processing systems 6 (1993)
 6. Brown, T.B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Nee-
    lakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A.,
    Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D.M., Wu, J., Win-
    ter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark,
    J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., Amodei, D.: Language
    models are few-shot learners. CoRR abs/2005.14165 (2020), https://arxiv.
    org/abs/2005.14165
 7. Devlin, J., Chang, M.W., Lee, K., Toutanova, K.: BERT: Pre-training of deep
    bidirectional transformers for language understanding. In: Proceedings of the 2019
    Conference of the North American Chapter of the Association for Computational
    Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers).
    pp. 4171–4186. Association for Computational Linguistics, Minneapolis, Minnesota
    (Jun 2019). https://doi.org/10.18653/v1/N19-1423, https://aclanthology.org/
    N19-1423
 8. Efron, B., Tibshirani, R.J.: An Introduction to the Bootstrap. No. 57 in Mono-
    graphs on Statistics and Applied Probability, Chapman & Hall/CRC, Boca Raton,
    Florida, USA (1993)
 9. First, E., Brun, Y., Guha, A.: Tactok: semantics-aware proof synthesis. Proceedings
    of the ACM on Programming Languages 4(OOPSLA), 1–31 (2020)
10. Gage, P.: A new algorithm for data compression. C Users J. 12(2), 23–38 (feb
    1994)
11. Gauthier, T., Kaliszyk, C., Urban, J., Kumar, R., Norrish, M.: Learning to prove
    with tactics. arXiv preprint arXiv:1804.00596 (2018)
12. Gauthier, T., Kaliszyk, C., Urban, J., Kumar, R., Norrish, M.: Tactictoe: Learning
    to prove with tactics. Journal of Automated Reasoning 65(2), 257–286 (2021)
13. Gransden, T., Walkinshaw, N., Raman, R.: Sepia: search for proofs using inferred
    automata. In: International Conference on Automated Deduction. pp. 246–255.
    Springer (2015)
14. Hsu, C.W., Chang, C.C., Lin, C.J.: A practical guide to support vector classifi-
    cation. Tech. rep., Department of Computer Science, National Taiwan University
    (2003), http://www.csie.ntu.edu.tw/~cjlin/papers.html
15. Huang, D., Dhariwal, P., Song, D., Sutskever, I.: Gamepad: A learning environment
    for theorem proving. arXiv preprint arXiv:1806.00608 (2018)


  Distribution Statement A – Approved for Public Release, Distribution Unlimited
                                                                      CoProver       17

16. Huang, P.S., He, X., Gao, J., Deng, L., Acero, A., Heck, L.: Learning deep
    structured semantic models for web search using clickthrough data. In: Pro-
    ceedings of the 22nd ACM International Conference on Information and Knowl-
    edge Management. p. 2333–2338. CIKM ’13, Association for Computing Ma-
    chinery, New York, NY, USA (2013). https://doi.org/10.1145/2505515.2505665,
    https://doi.org/10.1145/2505515.2505665
17. Irving, G., Szegedy, C., Alemi, A.A., Eén, N., Chollet, F., Urban, J.: Deepmath-
    deep sequence models for premise selection. Advances in Neural Information Pro-
    cessing Systems 29, 2235–2243 (2016)
18. Jakubův, J., Urban, J.: Enigma: efficient learning-based inference guiding machine.
    In: Intelligent Computer Mathematics: 10th International Conference, CICM 2017,
    Edinburgh, UK, July 17-21, 2017, Proceedings 10. pp. 292–302. Springer (2017)
19. Jiang, A.Q., Li, W., Tworkowski, S., Czechowski, K., Odrzygóźdź, T., Miłoś, P.,
    Wu, Y., Jamnik, M.: Thor: Wielding hammers to integrate language models and
    automated theorem provers (2022). https://doi.org/10.48550/ARXIV.2205.10893,
    https://arxiv.org/abs/2205.10893
20. Jiang, A.Q., Welleck, S., Zhou, J.P., Li, W., Liu, J., Jamnik, M., Lacroix, T.,
    Wu, Y., Lample, G.: Draft, sketch, and prove: Guiding formal theorem provers
    with informal proofs (2022). https://doi.org/10.48550/ARXIV.2210.12283, https:
    //arxiv.org/abs/2210.12283
21. Jones, K.S.: A statistical interpretation of term specificity and its application in
    retrieval. Journal of Documentation 28, 11–21 (1972)
22. Kaliszyk, C., Urban, J.: Femalecop: Fairly efficient machine learning connection
    prover. In: Logic for Programming, Artificial Intelligence, and Reasoning. pp. 88–
    96. Springer (2015)
23. Komendantskaya, E., Heras, J., Grov, G.: Machine learning in proof general: In-
    terfacing interfaces. arXiv preprint arXiv:1212.3618 (2012)
24. Kühlwein, D., Blanchette, J.C., Kaliszyk, C., Urban, J.: Mash: machine learning
    for sledgehammer. In: International Conference on Interactive Theorem Proving.
    pp. 35–50. Springer (2013)
25. Lample, G., Lachaux, M.A., Lavril, T., Martinet, X., Hayat, A., Ebner, G.,
    Rodriguez, A., Lacroix, T.: Hypertree proof search for neural theorem proving
    (2022). https://doi.org/10.48550/ARXIV.2205.11491, https://arxiv.org/abs/
    2205.11491
26. Li, S., Zhao, Y., Varma, R., Salpekar, O., Noordhuis, P., Li, T., Paszke, A.,
    Smith, J., Vaughan, B., Damania, P., Chintala, S.: PyTorch Distributed: Expe-
    riences on accelerating data parallel training. CoRR abs/2006.15704 (2020),
    https://arxiv.org/abs/2006.15704
27. Li, W., Yu, L., Wu, Y., Paulson, L.C.: Isarstep: a benchmark for high-level math-
    ematical reasoning. arXiv preprint arXiv:2006.09265 (2020)
28. Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis,
    M., Zettlemoyer, L., Stoyanov, V.: RoBERTa: A robustly optimized BERT pre-
    training approach (2019). https://doi.org/10.48550/ARXIV.1907.11692, https:
    //arxiv.org/abs/1907.11692
29. Loos, S., Irving, G., Szegedy, C., Kaliszyk, C.: Deep network guided proof search.
    arXiv preprint arXiv:1701.06972 (2017)
30. Luhn, H.P.: A statistical approach to mechanized encoding and searching of literary
    information. IBM Journal of Research and Development 1(4), 309–317 (1957).
    https://doi.org/10.1147/rd.14.0309


  Distribution Statement A – Approved for Public Release, Distribution Unlimited
18    Yeh et al.

31. Manning, C.D., Raghavan, P., Schütze, H.: Introduction to Information Retrieval.
    Cambridge University Press, Cambridge, UK (2008), http://nlp.stanford.edu/
    IR-book/information-retrieval-book.html
32. Mitra, B., Craswell, N.: (2018)
33. Otten, J., Bibel, W.: leancop: lean connection-based theorem proving. Journal of
    Symbolic Computation 36(1-2), 139–161 (2003)
34. Owre, S., Rushby, J.M., Shankar, N.: PVS: A prototype verification system. In:
    International Conference on Automated Deduction. pp. 748–752. Springer (1992)
35. Rabe, M.N., Szegedy, C.: Towards the automatic mathematician. In: International
    Conference on Automated Deduction. pp. 25–37. Springer, Cham (2021)
36. Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li,
    W., Liu, P.J.: Exploring the limits of transfer learning with a unified text-to-text
    transformer. CoRR abs/1910.10683 (2019), http://arxiv.org/abs/1910.10683
37. Reimers, N., Gurevych, I.: Sentence-BERT: Sentence embeddings using Siamese
    BERT-Networks. CoRR abs/1908.10084 (2019), http://arxiv.org/abs/1908.
    10084
38. Schulz, S.: E – A Brainiac Theorem Prover. Journal of AI Communications 15(2/3),
    111–126 (2002)
39. Selsam, D., Bjørner, N.: Guiding high-performance sat solvers with unsat-core pre-
    dictions. In: International Conference on Theory and Applications of Satisfiability
    Testing. pp. 336–353. Springer (2019)
40. Sennrich, R., Haddow, B., Birch, A.: Neural machine translation of rare words
    with subword units. In: Proceedings of the 54th Annual Meeting of the As-
    sociation for Computational Linguistics (Volume 1: Long Papers). pp. 1715–
    1725. Association for Computational Linguistics, Berlin, Germany (Aug 2016).
    https://doi.org/10.18653/v1/P16-1162, https://aclanthology.org/P16-1162
41. Urban, J., Vyskočil, J., Štěpánek, P.: Malecop machine learning connection prover.
    In: International Conference on Automated Reasoning with Analytic Tableaux and
    Related Methods. pp. 263–277. Springer (2011)
42. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser,
    Ł., Polosukhin, I.: Attention is all you need. Advances in neural information pro-
    cessing systems 30 (2017)
43. Wang, M., Tang, Y., Wang, J., Deng, J.: Premise selection for theorem proving by
    deep graph embedding. arXiv preprint arXiv:1709.09994 (2017)
44. Whalen, D.: Holophrasm: a neural automated theorem prover for higher-order
    logic. arXiv preprint arXiv:1608.02644 (2016)
45. Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., Cistac, P.,
    Rault, T., Louf, R., Funtowicz, M., Davison, J., Shleifer, S., von Platen, P., Ma, C.,
    Jernite, Y., Plu, J., Xu, C., Scao, T.L., Gugger, S., Drame, M., Lhoest, Q., Rush,
    A.M.: Transformers: State-of-the-art natural language processing. In: Proceedings
    of the 2020 Conference on Empirical Methods in Natural Language Processing: Sys-
    tem Demonstrations. pp. 38–45. Association for Computational Linguistics, Online
    (Oct 2020), https://www.aclweb.org/anthology/2020.emnlp-demos.6
46. Wu, M., Norrish, M., Walder, C., Dezfouli, A.: Tacticzero: Learning to
    prove theorems from scratch with deep reinforcement learning. arXiv preprint
    arXiv:2102.09756 (2021)
47. Yang, K., Deng, J.: Learning to prove theorems via interacting with proof assis-
    tants. In: International Conference on Machine Learning. pp. 6984–6994. PMLR
    (2019)



  Distribution Statement A – Approved for Public Release, Distribution Unlimited
