                                                      Generating Correctness Proofs with Neural
                                                                      Networks
                                                                Alex Sanchez-Stern                                                   Yousef Alhessi
                                                                     UC San Diego                                                      UC San Diego
                                                                         USA                                                                USA
                                                                  alexss@eng.ucsd.edu                                              yalhessi@eng.ucsd.edu

                                                                    Lawrence Saul                                                     Sorin Lerner
                                                                     UC San Diego                                                      UC San Diego
                                                                         USA                                                                USA
arXiv:1907.07794v4 [cs.PL] 28 May 2020




                                                                    saul@cs.ucsd.edu                                                 lerner@cs.ucsd.edu
                                         Abstract                                                                  ACM Reference Format:
                                         Foundational verification allows programmers to build                     Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin
                                                                                                                   Lerner. 2020. Generating Correctness Proofs with Neural
                                         software which has been empirically shown to have high
                                                                                                                   Networks. In Proceedings of the 4th ACM SIGPLAN Interna-
                                         levels of assurance in a variety of important domains.                    tional Workshop on Machine Learning and Programming Lan-
                                         However, the cost of producing foundationally verified                    guages (MAPL ’20), June 15, 2020, London, UK . ACM, New
                                         software remains prohibitively high for most projects,                    York, NY, USA, 15 pages. https://doi.org/10.1145/3394450.
                                         as it requires significant manual effort by highly trained                3397466
                                         experts. In this paper we present Proverbot9001, a proof
                                         search system using machine learning techniques to pro-
                                         duce proofs of software correctness in interactive the-                   1    Introduction
                                         orem provers. We demonstrate Proverbot9001 on the                         A promising approach to software verification is founda-
                                         proof obligations from a large practical proof project,                   tional verification. In this approach, programmers use
                                         the CompCert verified C compiler, and show that it                        an interactive theorem prover, such as Coq [14] or Is-
                                         can effectively automate what were previously manual                      abelle/HOL [35], to state and prove properties about
                                         proofs, automatically producing proofs for 28% of theo-                   their programs. Foundational verification has shown
                                         rem statements in our test dataset, when combined with                    increasing promise over the past two decades; it has
                                         solver-based tooling. Without any additional solvers, we                  been used to prove properties of programs in a variety of
                                         exhibit a proof completion rate that is a 4X improvement                  settings, including compilers [28], operating systems [23],
                                         over prior state-of-the-art machine learning models for                   database systems [31], file systems [8], distributed sys-
                                         generating proofs in Coq.                                                 tems [39], and cryptographic primitives [3].
                                                                                                                      One of the main benefits of foundational verification is
                                         CCS Concepts: • Computing methodologies →                                 that it provides high levels of assurance. The interactive
                                         Symbolic and algebraic manipulation; Machine                              theorem prover makes sure that proofs of program prop-
                                         learning.                                                                 erties are done in full and complete detail, without any
                                                                                                                   implicit assumptions or forgotten proof obligations. Fur-
                                         Keywords: Machine-learning, Theorem proving                               thermore, once a proof is completed, foundational proof
                                                                                                                   assistants can generate a representation of the proof in
                                                                                                                   a foundational logic; these proofs can be checked with a
                                         Permission to make digital or hard copies of all or part of this          small kernel. In this setting only the kernel needs to be
                                         work for personal or classroom use is granted without fee provided        trusted (as opposed to the entire proof assistant), leading
                                         that copies are not made or distributed for profit or commercial          to a small trusted computing base. As an example of
                                         advantage and that copies bear this notice and the full citation
                                         on the first page. Copyrights for components of this work owned           this high-level of assurance, a study of compilers [41] has
                                         by others than the author(s) must be honored. Abstracting with            shown that CompCert [28], a compiler proved correct
                                         credit is permitted. To copy otherwise, or republish, to post on          in the Coq proof assistant, is significantly more robust
                                         servers or to redistribute to lists, requires prior specific permission   than its non-verified counterparts.
                                         and/or a fee. Request permissions from permissions@acm.org.                  Unfortunately, the benefits of foundational verification
                                         MAPL ’20, June 15, 2020, London, UK
                                                                                                                   come at a great cost. The process of performing proofs in
                                         © 2020 Copyright held by the owner/author(s). Publication rights
                                         licensed to ACM.                                                          a proof assistant is extremely laborious. CompCert [28]
                                         ACM ISBN 978-1-4503-7996-0/20/06. . . $15.00                              took 6 person-years and 100,000 lines of Coq to write
                                         https://doi.org/10.1145/3394450.3397466                                   and verify, and seL4 [23], which is a verified version of
MAPL ’20, June 15, 2020, London, UK                                    Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner


a 10,000 line operating system, took 22 person-years                     in0                                in0    ×
to verify. The sort of manual effort is one of the main                  in1                                in1    ×
                                                                                                                          +     f    out
impediments to the broader adoption of proof assistants.                 in2
                                                                                                   out
   In this paper, we present Proverbot9001, a novel sys-
                                                                         in3                         (a) (b) inn   ×
tem that uses machine learning to help alleviate the
manual effort required to complete proofs in an interac-
tive theorem prover. Proverbot9001 trains on existing                  Figure 1. (a) A feed-forward neural network, where
proofs to learn models. Proverbot9001 then incorporates                each individual gray circle is a perceptron (b) An in-
these learned models in a tree search process to complete              dividual perceptron, which multiplies all the inputs by
proofs. The source of Proverbot9001 is publicly available              weights, sums up the results, and then applies a non-
on GitHub 1 .                                                          linear function 𝑓 .
   The main contribution of this paper is bringing domain
knowledge to the feature engineering, model architecture,
and search procedures of machine-learning based systems                based techniques, where a complex proof is checked by
for interactive theorem proving. In particular, our work               a simple procedure.
distinguishes itself from prior work on machine learning                  While research into solver-backed techniques has pro-
for proofs in three ways:                                              duced fully-automated tools in many domains, these
                                                                       approaches are generally incomplete, failing to prove
    1. A two part tactic-prediction model, in which pre-
                                                                       some desirable propositions. When these procedures fail,
       diction of tactic arguments is primary and informs
                                                                       it is often difficult or impossible for a user to complete
       prediction of tactics themselves.
                                                                       the proof, requiring a deep knowledge of the automation.
    2. An argument prediction architecture which makes
                                                                       In contrast, foundational verification techniques require
       use of recurrent neural networks over sequential
                                                                       a heavy initial proof burden, but scale to any propo-
       representations of terms.
                                                                       sition without requiring a change in proof technique.
    3. Several effective tree pruning techniques inside of
                                                                       However, the proof burden of foundational techniques
       a prediction-guided proof search.
                                                                       can be prohibitive; CompCert, a large and well-known
   We tested Proverbot9001 end-to-end by training on                   foundationally verified compiler, took 6 person-years of
the proofs from 162 files from CompCert, and testing on                work to verify [27], with other large verification projects
the proofs from 13 files2 . When combined with solver-                 sporting similar proof burdens.
based tooling (which alone can only solve 7% of proofs),
Proverbot9001 can automatically produce proofs for 28%                  2.2    Interactive Theorem Provers
of the theorem statements in our test dataset (138/501).
                                                                       Most foundational (and some solver-backed) verification
In our default configuration without external solvers,
                                                                       is done in an interactive theorem prover. Interactive
Proverbot9001 solves (produces a checkable proof for)
                                                                       theorem provers allow the user to define proof goals
19.36% (97/501) of the proofs in our test set, which is
                                                                       alongside data and program definitions, and then prove
a nearly 4X improvement over the previous state of the
                                                                       those goals interactively, by entering commands which
art system that attempts the same task [40]. Our model
                                                                       manipulate the proof context. The name and nature of
is able to reproduce the tactic name from the solution
                                                                       these commands varies by the proof assistant, but in
32% of the time; and when the tactic name is correct,
                                                                       many foundational assistants, these commands are called
our model is able to predict the solution argument 89%
                                                                       “tactics”, and coorespond to primitive proof techniques
of the time. We also show that Proverbot9001 can be
                                                                       like “induction”, as well as search procedures like “omega”
trained on one project and then effectively predict on
                                                                       (which searches for proofs over ring-like structures). Proof
another project.
                                                                       obligations in such proof assistants take the form of a
                                                                       set of hypotheses (in a Curry-Howard compatible proof
2     Background
                                                                       theory, bound variables in a context), and a goal (a
2.1    Foundational Verification                                       target type); proof contexts may consist of multiple
Program verification is a well studied problem in the pro-             proof obligations.
gramming languages community. Most work in this field
falls into one of two categories: solver-backed automated               2.3    Machine Learning and Neural Networks
(or semi-automated) techniques, where a simple proof is                 Machine learning is an area of computer science dating
checked by a complex procedure; and foundational logic                  back to the 1950s. In problems of supervised learning,
1 https://github.com/UCSD-PL/proverbot9001                              the goal is to learn a function from labeled examples
2 This training/test split comes from splitting the dataset 90/10,      of input-output pairs. Models for supervised learning
and then removing from the test set files that don’t contain proofs.    parameterize a function from inputs to outputs and have
Generating Correctness Proofs with Neural Networks                                                 MAPL ’20, June 15, 2020, London, UK


    out              6       1       3       4       2   5                                         Theorem To
          Visually                                                                                   Prove
          Unfold
    G                G       G       G       G       G   G                          Commands                        Proof States
                                                                                                                                      Neural Network
                                                                Coq Interface                       Search
                                                                                                                                      Prediction Model
                                                                                    Proof States                    Predictions
    in               not      (      eq      x       y   )

                                                                                                       Proof
Figure 2. A recurrent neural network. Inputs are in
blue boxes at the bottom, and each iteration produces
an output value, as well as a new state value for the next   Figure 3. The overall architecture of Proverbot9001,
iteration.                                                   built using CoqSerapi, Python, and PyTroch.


                                                                                                       eval_mulhs
a procedure to update the parameters from a data set
of labeled examples. Machine learning has traditionally
                                                                          econstructor                   eauto         unfold binary_constructor_sound
been applied to problems such as handwriting recogni-
tion, natural language processing, and recommendation
                                                              simpl             eauto       try omega                intros          simpl         eauto
systems.
   Neural Networks are a particular class of learned model
where layers of nodes are connected together by a lin-                                         inv H                 inv H0        TrivialExists

ear combination and a non-linear activation function, to
form general function approximators. Neural Networks                     TrivialExists      econstructor             subst

have a variety of structures, some forming a straightfor-
ward “stack” of nodes with some connections removed                         QED

(convolutional), and others, such as those used for natu-
ral language processing, using more complex structures       Figure 4. A graph of a Proverbot9001 search. In green
like loops.                                                  are the tactics that formed part of the discovered solution,
   We will make use of two different kinds of neural net-    as well as the lemma name and the QED. In orange are
works: feed-forward networks and recurrent neural net-       nodes that resulted in a context that is at least as hard
works. Figure 1(a) shows the structure of a feed-forward     as one previously found (see Section 7).
network, where each gray circle is a perceptron, and
Figure 1(b) shows individual structure of a perceptron.
   Figure 2 shows the structure of a recurrent neural net-   Definition binary_constructor_sound
                                                                 (cstr: expr -> expr -> expr)
work (RNN). Inputs are shown in blue, outputs in green
                                                                 (sem: val -> val -> val) : Prop :=
and computational nodes in gray. The computational             forall le a x b y,
nodes are Gated Recurrent Network nodes, GRU for               eval_expr ge sp e m le a x ->
short, a commonly used network component with two              eval_expr ge sp e m le b y ->
inputs and two outputs [10]. The network is recurrent          exists v, eval_expr ge sp e m le (cstr a b) v
                                                                         /\ Val.lessdef (sem x y) v.
because it feeds back into itself, with the state output
from the previous iteration feeding into the state input     Theorem eval_mulhs:
of the next iteration. When we display an RNN receiving        binary_constructor_sound mulhs Val.mulhs.
data, we visually unfold the RNN, as shown on the right      Proof.
side of Figure 2, even though in practice there is still     ...
only one GRU node. The right side of Figure 2 shows             This theorem states that the mulhs expression con-
an example RNN that processes tokens of a Coq goal,          structor is sound with respect to the specification
and produces some output values.                             Val.mulhs.
                                                                At the beginning of the proof of eval_mulhs, Prover-
3    Overview                                                bot9001 predicts three candidate tactics, econstructor,
In this section, we’ll present Proverbot9001’s prediction    eauto, and unfold binary_constructor_sound. Once
and search process with an example from CompCert.            these predictions are made, Proverbot9001 tries running
You can see the top-level structure of Proverbot9001 in      all three, which results in three new states of the proof
Figure 3.                                                    assistant. In each of these three states, Proverbot9001
  Consider the following theorem from the CompCert           again makes predictions for what the most likely tactics
compiler:                                                    are to apply next. These repeated predictions create a
MAPL ’20, June 15, 2020, London, UK                          Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner


            𝒯                Tactics                          under which we want to make a prediction) and returns
            𝒜                Tactic arguments                 a scoring function over 𝜏 . In particular, we have:
            𝒞 =𝒯 ×𝒜          Proof commands
                                                                                    ℛ[𝜏 ] = 𝒮 → 𝒟[𝜏 ]
            ℐ                Identifiers
            𝒬                Propositions                     Our main predictor 𝑃 will be a predictor of the next
            𝒢=𝒬              Goals                            step in the proof, i.e. a predictor for proof commands:
            ℋ=ℐ ×𝒬           Hypotheses                                                𝑃 : ℛ[𝒯 × 𝒜]
            𝒪 = [ℋ] × 𝒢      Obligations
                                                             We divide our main predictor into two predictors, one
            𝒮 = [𝒪 × [𝒞]]    Proof states
                                                             for tactics, and one for arguments:
    Figure 5. Formalism to model a Proof Assistant                                      𝑃tac : ℛ[𝒯 ]
                                                                                 𝑃arg : 𝒯 → ℛ[𝒜]
search tree, which Proverbot9001 explores in a depth          Our main predictor 𝑃 combines 𝑃tac and 𝑃arg as follows:
first way. The proof command predictions that Prover-               𝑃 (𝜎) = 𝜆(𝜏, 𝑎) . 𝑃tac (𝜎)(𝜏 ) ⊗ 𝑃arg (𝜏 )(𝜎)(𝑎)
bot9001 makes are ordered by likelihood, and the search
                                                             where ⊗ is an operator that combines the scores of the
explores more likely branches first.
                                                             tactic and the argument predictors. We now describe
   Figure 4 shows the resulting search tree for
                                                             the three parts of this prediction architecture in turn:
eval_mulhs. The nodes in green are the nodes that pro-
                                                             𝑃tac , 𝑃arg , and ⊗.
duce the final proof. Orange nodes are predictions that
fail to make progress on the proof (see Section 7); these     5.1    Predicting Tactics (𝑃tac )
nodes are not expanded further. All the white nodes to
                                                             To predict tactics, Proverbot9001 uses of a set of manu-
the right of the green path are not explored, because the
                                                             ally engineered features to reflect important aspects of
proof in the green path is found first.
                                                             proof prediction: (1) the head of the goal as an integer
                                                             (2) the name of the previously run tactic as an integer
4    Definitions                                             (3) a hypothesis that is heuristically chosen (based on
In the rest of the paper, we will describe the details       string similarity to goal) as being the most relevant to
of how Proverbot9001 works. We start with a set of           the goal (4) the similarity score of this most relevant
definitions that will be used throughout. In particular,     hypothesis.
Figure 5 shows the formalism we will use to represent the       These features are embedded into a continuous vector
state of an in-progress proof. A tactic 𝜏 ∈ 𝒯 is a tactic    of 128 floats using a standard word embedding, and then
name. An argument 𝑎 ∈ 𝒜 is a tactic argument. For            fed into a fully connected feed-forward neural network
simplicity of the formalism, we assume that all tactics      (3 layers, 128 nodes-wide) with a softmax (normalizing)
take zero or one arguments. We use ℐ for the set of          layer at the end, to compute a probability distribution
Coq identifiers, and 𝒬 for the set of Coq propositions.      over possible tactic names. This architecture is trained
A proof state 𝜎 ∈ 𝒮 is a state of the proof assistant,       on 153402 samples with a stochastic gradient descent
which consists of a list of obligations along with their     optimizer.
proof command history. We use [𝑋] to denote the set             The architecture of this model is shown in Figure 6.
of lists of elements from 𝑋. An obligation is a pair of:     Blue boxes represent input; purple boxes represent inter-
(1) a set of hypotheses (2) a goal to prove. A hypothesis    mediate encoded values; green boxes represent outputs;
is a proposition named by an identifier, and a goal is a     and gray circles represent computations. The NN circle
proposition.                                                 is the feed-forward Neural Network mentioned above.
                                                             The Enc circle is a word embedding module.
5    Predicting a Single Proof Step
We start by explaining how we predict individual steps        5.2    Predicting Tactic Arguments (𝑃arg )
in the proof. Once we have done this, we will explain         Once a tactic is predicted, Proverbot9001 next predicts
how we use these proof command predictions to guide a         arguments. Recall that the argument predictor is a func-
proof search procedure.                                       tion 𝑃arg : ℛ[𝒜]. In contrast to previous work, our ar-
   We define 𝒟[𝜏 ] to be a scoring function over 𝜏 , where    gument model is a prediction architecture in its own
larger scores are preferred over smaller ones:                right.
                                                                 Proverbot9001 currently predicts zero or one tactic
                      𝒟[𝜏 ] = 𝜏 → R
                                                              arguments; However, since the most often-used multi-
We define a 𝜏 -predictor ℛ[𝜏 ] to be a function that takes    argument Coq tactics can be desugared to sequences of
a proof state 𝜎 ∈ 𝒮 (i.e. a state of the proof assistant      single argument tactics (for example “unfold a, b” to
Generating Correctness Proofs with Neural Networks                                                           MAPL ’20, June 15, 2020, London, UK

                            Encode   Vectors of reals
          Previous tactic                                                                                                      Token Output
                                                                                               60    1   3      4    29   5
            “apply”          Enc                         Distribution      Tactic name                                            Scores
                                                         over tactics    predicted by Ptac
          Goal head                                                          “unfold”          G     G   G      G    G    G
            “forall”         Enc                    NN
                                                                                               not   (   eq      x    y    )   Goal
          Hypothesis head
                                                                                    Constant                                   Encoded Goal
             “eq”            Enc
                                                                                        0      G     G   G      G    G    G    8.2 2.1 3.0 9.2




Figure 6. Proverbot9001’s model for predicting tactics.                                                                                          Hypothesis/
                                                                                     NN        G     G   G      G    G    G     G            8     Lemma
Takes as input three features for each data point: the                                                                                           Output Score

previous tactic run, the head token of the goal, and of the                   5.2              y     >   (       x    +    1     )         Hypothesis/
                                                                                                                                           Lemma
                                                                        Hypothesis/Lemma
most relevant hypothesis (see Section 5.1). We restrict                  Similarity Score
the previous tactic feature to the 50 most common tactics,
and head tokens on goal and hypothesis to the 100 most                  Figure 7. The model for scoring possible arguments.
common head tokens.


                                                                           As before, blue boxes are inputs; purple boxes are
“unfold a. unfold b.”), this limitation does not signifi-               encoded values; green diamonds are outputs, in this case
cantly restrict our expressivity in practice.                           scores for each individual possible argument; and gray
   Proverbot9001 makes three kinds of predictions for                   circles are computational nodes. The GRU nodes are
arguments: goal-token arguments, hypothesis arguments,                  Gated Recurrent Units [10]. The NN node is a feed-
lemma arguments:                                                        forward neural network.
   Goal-token arguments are arguments that are a sin-                      For illustration purposes, Figure 7 uses an example
gle token in the goal; for instance, if the goal is                     to provide sample values. Each token in the goal is an
not (eq x y), we might predict unfold not, where not                    input – in Figure 7 the goal is “not (eq x y)”. The tactic
refers to the first token in the goal. In the case of tactics           predicted by 𝑃tac is also an input – in Figure 7 this tactic
like unfold and destruct, the argument is often (though                 is “unfold”. The hypothesis that is heuristically closest
not always) a token in the goal.                                        to the goal (according to our heuristic from Section 5.1)
   Hypothesis arguments are identifiers referring to a hy-              is also an input, one token at a time being fed to a GRU.
pothesis in context. For instance, if we have a hypothesis              In our example, let’s assume this closest hypothesis is
H in context, with type is_path (cons (pair s d) m),                    “y > (x+1)”. The similarity score of this most relevant
we might predict inversion H, where H refers to the                     hypothesis is an additional input – in Figure 7 this score
hypothesis, and inversion breaks it down. In the case                   is 5.2.
of tactics like inversion and destruct, the argument is                    There is an additional RNN (the middle row of GRUs
often a hypothesis identifier.                                          in Figure 7) which encodes the goal as a vector of reals.
   Finally, lemma arguments are identifiers referring to                The initial state of this RNN is set to some arbitrary
a previously defined proof. These can be basic facts in                 constant, in this case 0.
the standard library, like                                                 The initial state of the hypothesis RNN (the third
                                                                        row of GRUs in Figure 7) is computed using a feed-
plus_n_0 : forall n : nat, n = n + 0
                                                                        forward Neural Network (NN). This feed-forward Neural
or a lemma from the current project, such as the                        Network takes as input the tactic predicted by 𝑃tac , the
eval_mulhs described in the overview. In Proverbot9001,                 goal encoded as a vector of reals, and the similarity score
lemmas are considered from a subset of the possible                     of the hypothesis.
lemma arguments available in the global context, in or-                    The architecture in Figure 7 produces one output score
der to make training tractable. Proverbot9001 supports                  for each token in the goal and one output score for the
several different modes for determining this subset; by                 hypothesis. The highest scoring element will be chosen
default we consider lemmas defined previously in the                    as the argument to the tactic. In Figure 7, the highest
current file.                                                           scoring element is the “not” token, resulting in the proof
  The architecture of the scoring functions for these                   command “unfold not”. If the hypothesis score (in our
argument types is shown in Figure 7. One recurrent                      example this score is 8) would have been the highest
neural network (RNN) is used to give scores to each                     score, then the chosen argument would be the identifier
hypothesis and lemma by processing the type of the                      of that hypothesis in the Coq context. For example, if the
term, and outputting a final score. A different RNN is                  identifier was IHn (as is sometimes the case for inductive
then used to process the goal, assigning a score to each                hypotheses), then the resulting proof command would
token in processes.                                                     be “unfold IHn”.
MAPL ’20, June 15, 2020, London, UK                           Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner


5.3   Combining Tactic and Argument Scores                    tactic name (from the actual proof), are passed to a
      (⊗)                                                     module that computes changes to the weights based
The ⊗ operator attempts to provide a balanced combi-          on the NLLLoss criterion. These changes are batched
nation of tactic and argument prediction, taking both         together over several steps of the proof, and then applied
into account even across different tactics. The operator      to update the tactic model. Running over all the training
works as follows. We pick the 𝑛 highest-scoring tactics       data to update the weights is called an epoch, and we
and for each tactic the 𝑚 highest-scoring arguments.          run our training over 20 epochs.
We then score each proof command by multiplying the              Figure 10 shows the training architecture for the argu-
tactic score and the argument score, without any normal-      ment predictor, 𝑃arg (recall that the detailed architecture
ization. Formally, we can implement this approach by          of 𝑃arg is shown in Figure 7). The goal of training is
defining ⊗ to be multiplication, and by not normalizing       to find weights for the GRU components in 𝑃arg . Here
the probabilities produced by 𝑃arg until all possibilities    again, Proverbot9001 processes all the Coq theorems in
are considered together.                                      the training set, and steps through the proof of each of
   Because we don’t normalize the probabilities of tac-       these theorems. Figure 10 shows what happens at each
tics, the potential arguments for a tactic are used in        step in the proof. In particular, at each step in the proof,
determining the eligibility of the tactic itself (as long     the current 𝑃tac predictor is run to produce the top pre-
as that tactic is in the top 𝑛). This forms one of the        dictions for tactic. These predicted tactic, along with the
most important contributions of our work: the argument        correct tactic, are passed to the argument model 𝑃arg .
selection is primary, with the tactic prediction mostly       To make Figure 10 more readable, we do not show the
serving to help prune its search space.                       additional parameters to 𝑃arg that where displayed in
                                                              Figure 8, but these parameters are in fact also passed to
5.4   Putting It All Together                                 𝑃arg during training. Note that it is very important for
                                                              us to inject the tactics predicted by 𝑃tac into the input
The overall architecture that we have described is shown
in Figure 8. The 𝑃tac predictor (whose detailed struc-        of the argument model 𝑃arg , instead of using just the
ture is shown in Figure 6) computes a distribution over       correct tactic name. This allows the scores produced by
tactic using three features as input: the previous tactic,    the argument model to be comparable across different
head constructor of goal, and head constructor of the         predicted tactics. Once the argument model 𝑃arg com-
                                                              putes a score for each possible argument, we combine
hypothesis deemed most relevant. Then, for each of the
                                                              these predictions using ⊗ to get a distribution of scores
top tactic predicted by 𝑃tac , the 𝑃arg predictor (whose
detailed structure is shown in Figure 7) is invoked. In ad-   over tactic/argument pairs. Finally, this distribution,
dition to the tactic name, the 𝑃arg predictor takes several   along with the correct tactic/argument pair is passed to
additional inputs: the goal, the hypotheses in context,       a module that computes changes to the weights based
and the similarity between each of those hypotheses and       on the NLLLoss criterion. In our main CompCert bench-
                                                              mark the 153402 tactic samples from the training set
the goal. The 𝑃arg predictor produces scores for each
                                                              are processed for 20 epochs.
possible argument (in our case one score for each token
in the goal, and one score the single hypothesis). These
scores are combined with ⊗ to produce an overall scoring       6.2    Learning From Higher-Order Proof
of proof commands.                                                    Commands
                                                              Proof assistants generally have higher-order proof com-
6     Training                                                mands, which are tactics that take other proof commands
6.1   Training Architecture                                   as arguments; in Coq, these are called tacticals. One of
Figure 9 shows the training architecture for the tactic       the most common examples is the (;) infix operator
predictor, 𝑃tac (recall that the detailed architecture of     which runs the proof command on the right on every
𝑃tac is shown in Figure 6). The goal of training is to        sub-goal produced by the tactic on the left. Another
find weights for the neural network that is found inside      example is the repeat tactical, which repeats a provided
the gray 𝑃tac circle. Proverbot9001 processes all the Coq     tactic until it fails.
theorems in the training set, and steps through the proof       While higher-order proof commands are extremely
of each of these theorems. Figure 9 shows what happens        important for human proof engineers, they are harder to
at each step in the proof. In particular, at each step in     predict automatically because of their generality. While
the proof, Proverbot9001 computes the three features          some previous work [40] attempts to learn directly on
we are training with, and passes these features to the        data which uses these higher-order proof commands,
current tactic model to get a distribution over tactics.      we instead take the approach of desugaring higher-order
This distribution over tactics, along with the correct        proof commands into first-order ones as much as possible;
Generating Correctness Proofs with Neural Networks                                                                           MAPL ’20, June 15, 2020, London, UK


                                                                                                            Arg
                                                                                                   Arg
                                                                                                           Scores
                                                                                                  Model
  Features                                                                                                   1
                                                                            Top tactics                                                              Top tactic/arg pairs
                                                                                                  Parg       3
   “apply”                                          Distribution              “unfold”                                           Distribution over       “unfold eq”
                                Tactic                                                                       9
 Prev tactic                                        over tactics                                                                 tactic/arg pairs
                                Model
                                                                                                             2

    “forall”                        Ptac                                      “intros”            Parg       5                                           “apply IHn”
                                                                                                             8
 Goal head
                                                                                                             7
                                                                              “apply”
      “eq”                                       Goal, Hypothesis,
                                                                                                  Parg       6                                             “intros”
                                                  Similarity Score
Hypothesis head                             not (eq x y) y > (x+1) 5.2                                       4



       Figure 8. The overall prediction model, combining the tactic prediction and argument prediction models.

 Features                                                                                            desugars the cases that can be sequenced, and the re-
 “apply”
                         Tactic
                                        Distribution                                                 maining commands containing (;) are filtered out of the
 Prev tactic             Model
                                        over tactics
                                                         Evaluate Criterion &                        training set.
                                                          Compute Weight                               In addition to the (;) tactical, there are other tacticals
 “forall”                    Ptac                             Changes                                in common use in Coq. Some can be desugared into
Goal head                                                                  Weight
                                                                          Changes                    simpler forms. For example:
   “eq”                                 Correct tactic
                                          “unfold”
                                                                                                          ∙ “now <tac>” becomes “<tac>;easy”.
Hypothesis head                                                                                           ∙ “rewrite <term> by <tac>”                        becomes
                                                                                                            “rewrite <term> ; [ | <tac>]”
Figure 9. The architecture for training the tactic mod-                                                   ∙ “assert <term> by <tac>”                         becomes
els.                                                                                                        “assert <term> ; [ | <tac>]”
                                                                                                       In other cases, like try <tac> or solve <tac>, the
                                            Arg
                                                                                                     tactical changes the behavior of the proof command in
                                 Arg
                     Top
                                Model      Scores
                                             1
                                                                                                     a way that cannot be desugared; for these we simply
Distribution
over tactics
                   tactics
                  “unfold”
                                 Parg        3
                                                        Distribution over                            treat the prefixed tactic as a separate, learned tactic.
                                             9
 from Ptac
                                             2
                                                         tactic/arg pairs
                                                                                                     For example, we would treat try eauto as a new tactic.
                  “intros”       Parg        5                         Evaluate Criterion &
                                             8                          Compute Weight

                   “apply”
                                             7
                                                                            Changes
                                                                                         Weight
                                                                                                     7     Prediction-Guided Search
                                 Parg        6

                                                                                                     Now that we have explained how we predict a single step
                                                       Correct tactic &                 Changes
                                             4
                                                         argument
                                                                                                     in the proof, we describe how Proverbot9001 uses these
               Correct tactic                3           “unfold eq”
                 “unfold”        Parg        9
                                             7
                                                                                                     predictions in a proof search.
                                                                                                        In general, proof search works by transitioning the
Figure 10. The architecture for training the argument                                                proof assistant into different states by applying proof
models. Note that we inject predicted tactics into the                                               commands, and backtracking when a given part of the
input of the argument model, instead of just using the                                               search space has either been exhausted, or deemed un-
correct tactic, so that argument scores will be compara-                                             viable. Exhaustive proof search in proof assistants is
ble.                                                                                                 untenable because the number of possible proof com-
                                                                                                     mands to apply is large. Instead, we use the predictor
                                                                                                     described above to guide the search. Aside from using
                                                                                                     these predictions, the algorithm is a straightforward
this makes the data more learnable, without restricting                                              depth-limited search, with three subtleties.
the set of expressible proofs.
   For example, instead of trying to learn and predict                                                 First. we stop the search when we find a proof goal
(;) directly, Proverbot9001 has a system which attempts                                              that is at least as hard (by a syntactic definition) as a
to desugar (;) into linear sequences of proof commands.                                              goal earlier in the history. While in general it is hard
This is not always possible (without using explicit sub-                                             to formally define what makes one proof state harder
goal switching commands), due to propagation of exis-                                                than another, there are some obvious cases which we
tential variables across proof branches. Proverbot9001                                               can detect. A proof state with a superset of the original
MAPL ’20, June 15, 2020, London, UK                            Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner


obligations will be harder to prove, and a proof state         (since this second proof would essentially be considered
with the same goal, but fewer assumptions, will be harder      to have a depth of two, not three).
to prove.
   To formalize this intuition, we define a relation ≥          8     Evaluation
between states such that 𝜎1 ≥ 𝜎2 is meant to capture
“Proof state 𝜎1 is at least as hard as proof state 𝜎2 ”. We    This section shows that Proverbot9001 is able to success-
                                                               fully solve many proofs. We also experimentally show
say that 𝜎1 ≥ 𝜎2 if and only if for all obligations 𝑂2 in
                                                               that Proverbot9001 improves significantly on the state-
𝜎2 there exists an obligation 𝑂1 in 𝜎1 such that 𝑂1 ≥𝑜 𝑂2 .
For obligations 𝑂1 and 𝑂2 , we say that 𝑂1 ≥𝑜 𝑂2 if and        of-the-art presented in previous work.
only if each hypothesis in 𝑂1 is also a hypothesis in 𝑂2 ,        First, in Section 8.2, we compare experimentally to
and the goals of 𝑂1 and 𝑂2 are the same.                       previous work, by running both Proverbot9001 and the
   Since ≥ is reflexive, this notion allows us to generalize   CoqGym [40] project on CompCert, in several config-
                                                               urations outlined in the CoqGym paper. Next, in Sec-
all the cases above to a single pruning criteria: “proof
command prediction produces a proof state which is ≥           tion 8.3, we experiment with using the weights learned
than a proof state in the history”.                            from one project to produce proofs in another. Then,
                                                               in Section 8.4, we show the “hardness” of proofs that
   Second. when backtracking, we do not attempt to             Proverbot9001 is generally able to complete, using the
find a different proof for an already proven sub-obligation.   length of the original solution as proxy for proof diffi-
While in general this can lead to missed proofs because of     culty. Finally, in Appendix A.1, we measure the predictor
existential variables (typed holes filled based on context),   subsystem, without proof search. Additional evaluation
this has not been an issue for the kinds of proofs we have     can be found in the appendix.
worked with so far.                                               Experiments were run on two machines. Machine A
                                                               is an Intel i7 machine with 4 cores, a NVIDIA Quadro
  Third. we had to adapt our notion of search “depth”          P4000 8BG 256-bit, and 20 gigabytes of memory. Ma-
to the structure of Coq proofs (in which a tactic can          chine B is Intel Xeon E5-2686 v4 machine with 8 cores,
produce multiple sub-obligations). A naïve tree search         a Nvidia Tesla v100 16GB 4096-bit, and 61 gigabytes of
through the Coq proof space will fail to exploit some of       memory. Experiments were run using GNU Parallel [38].
the structure of sub-proofs in Coq.                               During the development of Proverbot9001, we explored
  Consider for example the following two proofs:               many alternatives, including n-gram/bag-of-words rep-
                                                               resentations of terms, a variety of features, and several
   1. intros. simpl. eauto.                                    core models including k-nearest neighbors, support vec-
   2. induction n. eauto. simpl.                               tor machines, and several neural architectures. While we
At first glance, it seems that both of these proofs have       include here some experiments that explore high-level
a depth of three. This means that a straightforward            design decisions (such as training and testing on the
tree search (which is blind to the structure of subproofs)     same projects vs cross project, working with and with-
                                                               out solver-based tooling, modifying the search depth and
would not find either of these proofs if the depth limit
                                                               width, and running with and without pre-processing),
were set to two.
   However, there is a subtlety in the second proof above      we also note that in the development of a large system
which is important (and yet not visible syntactically). In-    tackling a hard problem, it becomes intractable to eval-
deed, the induction n proof command actually produces          uate against every possible permutation of every design
two obligations (“sub-goals” in the Coq terminology).          decision. In this setting, we are still confident in having
                                                               demonstrated a system that works for the specific prob-
These correspond to the base case and the inductive
                                                               lem of generating correctness proof with performance
case for the induction on n. Then eauto discharges the
first obligation (the base case), and simpl discharges the     that outperforms the state-of-the-art techniques by many
second obligation (the inductive case). So in reality, the     folds.
second proof above really only has a depth of two, not
three.                                                          8.1    Summary of Results
   Taking this sub-proof structure into account is impor-      Proverbot9001, run using CoqHammer [11] and the de-
tant because it allows Proverbot9001 to discover more          fault configuration, is able to produce proofs for 28% of
proofs for a fixed depth. In the example above, if the         the theorem statements in CompCert. This represents
depth were set to two, and we used a naïve search, we          a 2.4X improvement over the previous state-of-the-art.
would not find either of the proofs. However, at the same      Without any external tooling, Proverbot9001 can pro-
depth of two, a search which takes the sub-proof struc-        duce proofs for 19.36%, an almost 4X improvement over
ture into account would be able to find the second proof       previous state-of-the-art prediction-based proofs. Our
Generating Correctness Proofs with Neural Networks                                               MAPL ’20, June 15, 2020, London, UK


core prediction model is able to reproduce the tactic                           160
name from the solution 32% of the time; and when the                            140                                      138 142
tactic name is correct, our model is able to predict the
                                                                                120
solution argument 89% of the time. We also show that




                                                              # proofs solved
                                                                                100               97   100
Proverbot9001 can be trained on one project and then
effectively predict on another project.                                         80
                                                                                60
                                                                                                                    48
8.2   Experimental Comparison to Previous                                       40    37
      Work                                                                                  23
                                                                                20
We tested Proverbot9001 end-to-end by training on the                            0
proofs from 162 files from CompCert, and testing on                                   H     G      P   G+P          GH   PH GH+PH
the proofs from 13 different files. On our default config-                                  P = Proverbot9001
uration, Proverbot9001 solves 19.36% (97/501) of the                                        G = CoqGym
proofs in our test set.                                                                     H = CoqHammer
                                                                                            _H = _ with CoqHammer
   In addition to running Proverbot9001 on CompCert,
we ran the CoqGym [40] tool, which represents the state      Figure 11. A comparison of Proverbot9001 and Co-
of the art in this area, on the same dataset in several      qGym’s abilities to complete proofs. H stands for Co-
configurations.                                              qHammer by itself, as a single invocation; G stands for
   To account for differences in training dataset, we ran    CoqGym by itself; P stands for Proverbot9001 by itself;
CoqGym with their original training schema, and also         G+P stands for the union of proofs done by G or P;
our training schema, and reported the best of the two        GH stands for CoqGym with CoqHammer; PH stands
numbers. CoqGym is intended to be combined with a            for Proverbot9001 with CoqHammer; GH +PH stands for
solver based proof-procedure, CoqHammer [11], which          the union of proofs done by GH or PH .
is run after every proof command invocation. While
our system was not originally designed this way, we
compare both systems using CoqHammer, as well as             20%. Combining Proverbot9001 and CoqGym, each with
both systems without. We also compared our system            CoqHammer, allows us to solve 142/501 proofs, a success
to using CoqHammer on the initial goal directly, which       rate of 28%. It’s important to realize that, whereas the
simultaneously invokes Z3 [13], CVC4 [6], Vampire [26],      prior state of the art was CoqGym with CoqHammer,
and E Prover [36], in addition to attempting to solve the    at 48 proofs, by combining CoqGym and Proverbot9001
goal using a crush-like tactic [9].                          (both with CoqHammer), we can reach a grand total of
   Figure 11 shows the proofs solved by various configu-     142 proofs, which is a 2.96X improvement over the prior
rations. The configurations are described in the caption.    state of art.
For all configurations, we ran Proverbot9001 with a
search depth of 6 and a search width of 3 (see Appen-        8.3                 Cross-Project Predictions
dix A.5). Note that in Figure 11 the bars for H, G, and      To test Proverbot9001’s ability to make use of train-
GH are prior work. The bars P, G+P and GH +PH are            ing across projects, we used the weights learned from
the ones made possible by our work.                          CompCert, and ran Proverbot9001 in its default configu-
   When CoqHammer is not used, Proverbot9001 can             ration on three other Coq projects from the Coq Contrib
complete nearly 4 times the number of proofs that are        collection, concat, float, and zfc.
completed by CoqGym. In fact, even when CoqGym is               concat is a library of constructive category theory
augmented with CoqHammer Proverbot9001 by itself             proofs, which showcases Coq proofs of mathematical
(without CoqHammer) still completes 39 more proofs,          concepts instead of program correctness. The concat
which is a 67% improvement (and corresponds to about         library is made of 514 proofs across 105 files; Prover-
8% of the test set). When enabling CoqHammer in both         bot9001 was able to successfully produce a proof for 91
CoqGym and Proverbot9001, we see that CoqGym solves          (17.7%) of the extracted theorem statements, without
48 proofs whereas Proverbot9001 solves 138 proofs, which     the use of CoqHammer.
is a 2.88X improvement over the state of art.                   float is a formalization of floating point numbers,
   Finally, CoqGym and Proverbot9001 approaches are          made of 742 proofs across 38 files; Proverbot9001 was
complementary; both can complete proofs which the            able to successfully produce a proof for 100 (13.48%)
other cannot. Therefore, one can combine both tools to       proofs.
produce more solutions than either alone. Combining Co-         zfc is a formalization of set theory made of 241 proofs
qGym and Proverbot9001, without CoqHammer, allows            across 78 files; 41 (17.01%) were successfully completed.
us to complete 100/501 proofs, a proof success rate of          The comparable number for CompCert was 19.36%.
MAPL ’20, June 15, 2020, London, UK                           Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner


                                                              to complete the proof. Figure 12 shows proofs of length
                                                              10 or below, and Figure 13 shows all proofs, binned in
                                                              sets of 10.
                                                                There are several observations that can be made. First,
                                                              most original proofs in our test set are less than 20 steps
                                                              long, with a heavy tail of longer proofs. Second, we do
                                                              better on shorter proofs. Indeed, 51% (256/501) of the
                                                              original proofs in our test set are ten proof commands or
                                                              shorter, and of those proofs, we can solve 35% (89/256),
                                                              compared to our overall solve rate of 19.36% (97/501).
Figure 12. A histogram plotting the original proof            Third, we are in some cases able to handle proofs whose
lengths in proof commands vs number of proofs of that         original length is longer than 10. Indeed, 7 of the proofs
length, in three classes, for proofs with length 10 or        we solve (out of 79 solved) had an original length longer
less. From bottom to top: proofs solved, proofs unsolved      than 10. In fact, the longest proof we solve is originally 25
because of depth limit, and proofs where our search           proof commands long; linearized it’s 256 proof commands
space was exhausted without finding a solution.               long. Our solution proof is 267 (linear) proof commands
                                                              long, comparable to the original proof, with frequent
                                                              case splits. The depth limit for individual obligations in
                                                              our search was 6 in all of these runs.


                                                               9     Related Work
                                                               9.1    Program Synthesis
                                                               Program Synthesis is the automatic generation of pro-
                                                               grams from a high-level specification [18]. This specifica-
                                                               tion can come in many forms, the most common being a
                                                               logical formula over inputs and outputs, or a set of input-
Figure 13. A histogram plotting the original proof             output examples. Programs generated can be in a variety
lengths in proof commands vs number of proofs of that          of paradigms and languages, often domain-specific. Our
length, in three classes. From bottom to top: proofs           tool, Proverbot9001, is a program synthesis tool that
solved, proofs unsolved because of depth limit, and proofs     focuses on synthesis of proof command programs.
where our search space was exhausted without finding              Several program synthesis works have used types ex-
a solution. Note that most proofs are between 0 and 10         tensively to guide search. Some work synthesizes pro-
proof commands long, with a long tail of much longer           grams purely from their types [19], while other work
proofs.                                                        uses both a type and a set of examples to synthesize
                                                               programs [15, 33]. In Proverbot9001, the programs be-
                                                               ing synthesized use a term type as their specification,
  These results demonstrate not only that Proverbot9001        however, the proof command program itself isn’t typed
can operate on proof projects in a variety of domains,         using that type, rather it must generate a term of that
but more importantly that it can effectively transfer          type (through search).
training from one project to another. This would allow            Further work in [29] attempts to learn from a set of
programmers to use Proverbot9001 even in the initial de-       patches on GitHub, general rules for inferring patches
velopment of a project, if it had been previously trained      to software. This work does not use traditional machine
on other projects.                                             learning techniques, but nevertheless learns from data,
                                                               albeit in a restricted way.
8.4   Original Proof Length vs Completion Rate
In Figure 12 and Figure 13, we plot a histogram of
the original proof lengths (in proof commands) vs the          9.2    Machine Learning for Code
number of proofs of that length. We break down the             Machine learning for modeling code is a well explored
proofs by (from bottom to top) number we solve, number         area [2], as an alternative to more structured methods
we cannot solve but still have unexplored nodes, and           of modeling code. Several models have been proposed
number run out of unexplored nodes before finding a            for learning code, such as AST-like trees [32], long-term
solution. Note that for the second class (middle bar), it’s    language models [12], and probabilistic grammars [7].
possible that increasing the search depth would allow us       Proverbot9001 does not attempt to be so general, using
Generating Correctness Proofs with Neural Networks                                         MAPL ’20, June 15, 2020, London, UK


a model of programs that is specific to its domain, al-         representations of terms, which is a technique that we
lowing us to capture the unique dependencies of proof           have not yet used, and could adapt if proven successful.
command languages. While the model is simple, it is able           Finally, there is also another approach to proof gen-
to model real proofs better than more general models            eration, which is to generate the term directly using
in similar domains (see Section 8.2). Machine learning          language translation models [37], instead of using tac-
has been used for various tasks such as code and patch          tics; however this technique has only been applied to
generation [2, 7, 12], program classification [32], and         small proofs due to its direct generation of low-level
learning loop invariants [16].                                  proof term syntax.


9.3 Machine Learning for Proofs                                 Acknowledgments
While machine learning has previously been explored for         We would like to thank Joseph Redmon for his invaluable
various aspects of proof writing, we believe there are still    help building the first Proverbot9001 version, Prover-
significant opportunities for improving on the state-of-        bot9000.
the-art, getting closer and closer to making foundational
verification broadly applicable.                                References
   More concretely, work on machine learning for proofs          [1] Alexander A. Alemi, François Chollet, Geoffrey Irving, Chris-
includes: using machine learning to speed up automated               tian Szegedy, and Josef Urban. 2016. DeepMath - Deep Se-
solvers [4], developing data sets [5, 22, 40], doing premise         quence Models for Premise Selection. CoRR abs/1606.04442
selection [1, 30], pattern recognition [25], clustering proof        (2016). arXiv:1606.04442 http://arxiv.org/abs/1606.04442
data [24], learning from synthetic data [21], interactively      [2] Miltiadis Allamanis, Earl T. Barr, Premkumar T. Devanbu,
                                                                     and Charles A. Sutton. 2017. A Survey of Machine Learning
suggesting tactics [20, 24].                                         for Big Code and Naturalness. CoRR abs/1709.06182 (2017).
   Finally, CoqGym attempts to model proofs with a                   arXiv:1709.06182 http://arxiv.org/abs/1709.06182
fully general proof command and term model expressing            [3] Andrew W. Appel. 2015. Verification of a Cryptographic
arbitrary AST’s. We experimentally compare Prover-                   Primitive: SHA-256. ACM Trans. Program. Lang. Syst. 37,
bot9001’s ability to complete proofs to that of CoqGym               2, Article 7 (April 2015), 31 pages. https://doi.org/10.1145/
                                                                     2701415
in detail in Section 8.2 There are also several important        [4] Mislav Balunoviundefined, Pavol Bielik, and Martin Vechev.
conceptual differences. First, the argument model in Co-             2018. Learning to Solve SMT Formulas. In Proceedings of
qGym is not as expressive as the one in Proverbot9001.               the 32nd International Conference on Neural Information
CoqGym’s argument model can predict a hypothesis                     Processing Systems (NIPS’18). Curran Associates Inc., Red
name, a number between 1 and 4 (which many tactics                   Hook, NY, USA, 10338–10349.
                                                                 [5] Kshitij Bansal, Sarah M. Loos, Markus N. Rabe, Chris-
in Coq interpret as referring to binders, for example                tian Szegedy, and Stewart Wilcox. 2019. HOList: An En-
induction 2 performs induction on the second quanti-                 vironment for Machine Learning of Higher-Order Theorem
fied variable), or a random (not predicted using machine             Proving (extended version). CoRR abs/1904.03241 (2019).
learning) quantified variable in the goal. In contrast,              arXiv:1904.03241 http://arxiv.org/abs/1904.03241
                                                                 [6] Clark Barrett, Christopher L. Conway, Morgan Deters, Liana
the argument model in Proverbot9001 can predict any
                                                                     Hadarean, Dejan Jovanović, Tim King, Andrew Reynolds,
token in the goal, which subsumes the numbers and the                and Cesare Tinelli. 2011. CVC4. In Proceedings of the 23rd
quantified variables that CoqGym can predict. Most im-               International Conference on Computer Aided Verification
portantly because Proverbot9001’s model can predict                  (CAV’11). Springer-Verlag, Berlin, Heidelberg, 171–177. http:
symbols in the goal, which allows effective unfolding,               //dl.acm.org/citation.cfm?id=2032305.2032319
for example “unfold eq”. Second, in contrast to Coq-             [7] Pavol Bielik, Veselin Raychev, and Martin Vechev. 2016.
                                                                     PHOG: Probabilistic Model for Code. In Proceedings of The
Gym, Proverbot9001 uses several hand-tuned features                  33rd International Conference on Machine Learning (Proceed-
for predicting proof commands. One key example is the                ings of Machine Learning Research), Maria Florina Balcan
previous tactic, which CoqGym does not even encode                   and Kilian Q. Weinberger (Eds.), Vol. 48. PMLR, New York,
as part of the context. Third, CoqGym’s treatment of                 New York, USA, 2933–2942. http://proceedings.mlr.press/
higher-order proof commands like “;” is not as effective             v48/bielik16.html
                                                                 [8] Haogang Chen, Tej Chajed, Alex Konradi, Stephanie Wang,
as Proverbot9001’s. While neither system can predict                 Atalay İleri, Adam Chlipala, M. Frans Kaashoek, and Nickolai
“;”, Proverbot9001 learns from “;” by linearizing them,              Zeldovich. 2017. Verifying a High-performance Crash-safe File
whereas CoqGym does not.                                             System Using a Tree Specification. In Proceedings of the 26th
   There is also a recent line of work on doing end-to-              Symposium on Operating Systems Principles (SOSP ’17).
end proofs in Isabelle/HOL and HOL4 [5, 17, 34]. This                ACM, New York, NY, USA, 270–286. https://doi.org/10.
                                                                     1145/3132747.3132776
work is hard to experimentally compare to ours, since            [9] Adam Chlipala. 2013. Certified Programming with Dependent
they use different benchmark sets, proof styles, and                 Types: A Pragmatic Introduction to the Coq Proof Assistant.
proof languages. Their most recent work [34] uses graph              The MIT Press.
MAPL ’20, June 15, 2020, London, UK                                  Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner


[10] Kyunghyun Cho, Bart van Merrienboer, Çaglar Gülçehre,                 Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas
     Fethi Bougares, Holger Schwenk, and Yoshua Bengio. 2014.              Sewell, Harvey Tuch, and Simon Winwood. 2009. seL4:
     Learning Phrase Representations using RNN Encoder-                    Formal Verification of an OS Kernel. In Proceedings of the
     Decoder for Statistical Machine Translation.          CoRR            ACM SIGOPS 22Nd Symposium on Operating Systems Prin-
     abs/1406.1078 (2014). arXiv:1406.1078 http://arxiv.org/abs/           ciples (SOSP ’09). ACM, New York, NY, USA, 207–220.
     1406.1078                                                             https://doi.org/10.1145/1629575.1629596
[11] Łukasz Czajka and Cezary Kaliszyk. 2018. Hammer for Coq:         [24] Ekaterina Komendantskaya, Jónathan Heras, and Gudmund
     Automation for Dependent Type Theory. Journal of Au-                  Grov. 2012. Machine Learning in Proof General: Interfacing
     tomated Reasoning 61, 1 (01 Jun 2018), 423–453. https:                Interfaces. Electronic Proceedings in Theoretical Computer
     //doi.org/10.1007/s10817-018-9458-4                                   Science 118 (12 2012). https://doi.org/10.4204/EPTCS.118.2
[12] Hoa Khanh Dam, Truyen Tran, and Trang Pham. 2016. A              [25] Ekaterina Komendantskaya and Kacper Lichota. 2012. Neural
     deep language model for software code. CoRR abs/1608.02715            Networks for Proof-Pattern Recognition, Vol. 7553. 427–434.
     (2016). arXiv:1608.02715 http://arxiv.org/abs/1608.02715              https://doi.org/10.1007/978-3-642-33266-1_53
[13] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Effi-        [26] Laura Kovács and Andrei Voronkov. 2013. First-Order
     cient SMT Solver. In Tools and Algorithms for the Construc-           Theorem Proving and Vampire, Vol. 8044. 1–35.             https:
     tion and Analysis of Systems, C. R. Ramakrishnan and Jakob            //doi.org/10.1007/978-3-642-39799-8_1
     Rehof (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,    [27] Daniel Kästner, Joerg Barrho, Ulrich Wünsche, Marc Schlick-
     337–340.                                                              ling, Bernhard Schommer, Michael Schmidt, Christian Fer-
[14] Jean-Christophe Filliâtre, Hugo Herbelin, Bruno Barras,               dinand, Xavier Leroy, and Sandrine Blazy. 2018. CompCert:
     Bruno Barras, Samuel Boutin, Eduardo Giménez, Samuel                  Practical Experience on Integrating and Qualifying a Formally
     Boutin, Gérard Huet, César Muñoz, Cristina Cornes, Cristina           Verified Optimizing Compiler.
     Cornes, Judicaël Courant, Judicael Courant, Chetan Murthy,       [28] Xavier Leroy. 2009. Formal verification of a realistic compiler.
     Chetan Murthy, Catherine Parent, Catherine Parent, Chris-             Commun. ACM 52, 7 (2009), 107–115. http://xavierleroy.org/
     tine Paulin-mohring, Christine Paulin-mohring, Amokrane               publi/compcert-CACM.pdf
     Saibi, Amokrane Saibi, Benjamin Werner, and Benjamin             [29] Fan Long, Peter Amidon, and Martin Rinard. 2017. Automatic
     Werner. 1997. The Coq Proof Assistant - Reference Manual              inference of code transforms for patch generation. 727–739.
     Version 6.1. Technical Report.                                        https://doi.org/10.1145/3106237.3106253
[15] Jonathan Frankle, Peter-Michael Osera, David Walker, and S       [30] Sarah M. Loos, Geoffrey Irving, Christian Szegedy, and Cezary
     Zdancewic. 2016. Example-directed synthesis: a type-theoretic         Kaliszyk. 2017. Deep Network Guided Proof Search. CoRR
     interpretation. ACM SIGPLAN Notices 51 (01 2016), 802–                abs/1701.06972 (2017). arXiv:1701.06972 http://arxiv.org/
     815. https://doi.org/10.1145/2914770.2837629                          abs/1701.06972
[16] Pranav Garg, Daniel Neider, P. Madhusudan, and Dan Roth.         [31] Gregory Malecha, Greg Morrisett, Avraham Shinnar, and
     2016. Learning Invariants Using Decision Trees and Impli-             Ryan Wisnesky. 2010. Toward a Verified Relational Database
     cation Counterexamples. SIGPLAN Not. 51, 1 (Jan. 2016),               Management System. In Proceedings of the 37th Annual ACM
     499–512. https://doi.org/10.1145/2914770.2837664                      SIGPLAN-SIGACT Symposium on Principles of Program-
[17] Thibault Gauthier, Cezary Kaliszyk, and Josef Urban. 2017.            ming Languages (POPL ’10). ACM, New York, NY, USA,
     TacticToe: Learning to Reason with HOL4 Tactics. In LPAR-             237–248. https://doi.org/10.1145/1706299.1706329
     21. 21st International Conference on Logic for Programming,      [32] Lili Mou, Ge Li, Zhi Jin, Lu Zhang, and Tao Wang. 2014.
     Artificial Intelligence and Reasoning (EPiC Series in Com-            TBCNN: A Tree-Based Convolutional Neural Network for
     puting), Thomas Eiter and David Sands (Eds.), Vol. 46. Easy-          Programming Language Processing. CoRR abs/1409.5718
     Chair, 125–143. https://doi.org/10.29007/ntlb                         (2014). arXiv:1409.5718 http://arxiv.org/abs/1409.5718
[18] Sumit Gulwani. 2010. Dimensions in Program Synthesis. In         [33] Peter-Michael Osera and Steve Zdancewic. 2015. Type-and-
     PPDP ’10 Hagenberg, Austria (ppdp ’10 hagenberg, austria              example-directed Program Synthesis. SIGPLAN Not. 50,
     ed.). https://www.microsoft.com/en-us/research/publication/           6 (June 2015), 619–630. https://doi.org/10.1145/2813885.
     dimensions-program-synthesis/                                         2738007
[19] Tihomir Gvero, Viktor Kuncak, Ivan Kuraj, and Ruzica             [34] Aditya Paliwal, Sarah M. Loos, Markus N. Rabe, Kshitij
     Piskac. 2013. Complete Completion using Types and Weights.            Bansal, and Christian Szegedy. 2019. Graph Representa-
     PLDI 2013 (2013), 12. 27–38. http://infoscience.epfl.ch/              tions for Higher-Order Logic and Theorem Proving. CoRR
     record/188990                                                         abs/1905.10006 (2019). arXiv:1905.10006 http://arxiv.org/
[20] Jónathan Heras and Ekaterina Komendantskaya. 2014.                    abs/1905.10006
     ACL2(ml): Machine-Learning for ACL2. In Proceedings              [35] Lawrence C. Paulson. 1993. Natural Deduction as Higher-
     Twelfth International Workshop on the ACL2 Theorem Prover             Order Resolution. CoRR cs.LO/9301104 (1993). http://arxiv.
     and its Applications, Vienna, Austria, 12-13th July 2014. 61–         org/abs/cs.LO/9301104
     75. https://doi.org/10.4204/EPTCS.152.5                          [36] Stephan Schulz. 2013. System Description: E 1.8. In Proc. of
[21] Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya                  the 19th LPAR, Stellenbosch (LNCS), Ken McMillan, Aart
     Sutskever. 2018. GamePad: A Learning Environment for Theo-            Middeldorp, and Andrei Voronkov (Eds.), Vol. 8312. Springer.
     rem Proving. CoRR abs/1806.00608 (2018). arXiv:1806.00608        [37] Taro Sekiyama, Akifumi Imanishi, and Kohei Suenaga.
     http://arxiv.org/abs/1806.00608                                       2017. Towards Proof Synthesis Guided by Neural Machine
[22] Cezary Kaliszyk, François Chollet, and Christian Szegedy.             Translation for Intuitionistic Propositional Logic. CoRR
     2017. HolStep: A Machine Learning Dataset for Higher-                 abs/1706.06462 (2017). arXiv:1706.06462 http://arxiv.org/
     order Logic Theorem Proving. CoRR abs/1703.00426 (2017).              abs/1706.06462
     arXiv:1703.00426 http://arxiv.org/abs/1703.00426                 [38] O. Tange. 2011. GNU Parallel - The Command-Line Power
[23] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June An-              Tool. ;login: The USENIX Magazine 36, 1 (Feb 2011), 42–47.
     dronick, David Cock, Philip Derrin, Dhammika Elkaduwe,                http://www.gnu.org/s/parallel
Generating Correctness Proofs with Neural Networks                MAPL ’20, June 15, 2020, London, UK


[39] James R. Wilcox, Doug Woos, Pavel Panchekha, Zachary
     Tatlock, Xi Wang, Michael D. Ernst, and Thomas Anderson.
     2015. Verdi: A Framework for Implementing and Formally
     Verifying Distributed Systems. In Proceedings of the 36th
     ACM SIGPLAN Conference on Programming Language De-
     sign and Implementation (PLDI ’15). ACM, New York, NY,
     USA, 357–368. https://doi.org/10.1145/2737924.2737958
[40] Kaiyu Yang and Jia Deng. 2019. Learning to Prove Theorems
     via Interacting with Proof Assistants. CoRR abs/1905.09381
     (2019). arXiv:1905.09381 http://arxiv.org/abs/1905.09381
[41] Xuejun Yang, Yang Chen, Eric Eide, and John Regehr. 2011.
     Finding and Understanding Bugs in C Compilers. PLDI
     (2011).
MAPL ’20, June 15, 2020, London, UK                           Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner


A     Appendix: Additional Evaluation                          A.3    Completion Rate in Proverbot9001’s
We now explore more detailed measurements about proof                 Prediction Domain
production.                                                   Proverbot9001 has a restricted model of proof commands:
                                                              it only captures proof commands with a single argument
                                                              that is a hypothesis identifier or a token in the goal. As re-
A.1    Individual Prediction Accuracy                         sult, it makes sense to consider Proverbot9001 within the
We want to measure the effectiveness of the predictor         context of proofs that were originally solved with these
subsystem that predicts proof command pairs (the 𝑃            types of proof commands. We will call proofs that were
function defined in Section 5). To do this, we broke          originally solved using these types of proof commands
the test dataset down into individual (linearized) proof      proofs that are in Proverbot9001’s prediction domain.
commands, and ran to just before each proof command           There are 79 such proofs in our test dataset (15.77% of
to get its prediction context. Then we fed that context       the proofs in the test dataset), and Proverbot9001 was
into our predictor, and compared the result to the proof      able to solve 48 of them.
command in the original solution. Of all the proof com-           What is interesting is that Proverbot9001 is able to
mands in our test dataset, we are able to predict 28.66%      solve proofs that are not in its prediction domain: these
(3784/13203) accurately. This includes the correct tac-       are proofs that were originally performed with proof
tic and the correct argument. If we only test on the          commands that are not in Proverbot9001’s domain, but
proof commands which are in Proverbot9001’s predic-           Proverbot9001 found another proof of the theorem that is
tion domain, we are able to predict 39.25% (3210/8178)        in its domain. This happened for 49 proofs (out of a total
accurately.                                                   of 97 solved proofs). Sometimes this is because Prover-
   During search, our proof command predictor returns         bot9001 is able to find a simpler proof command which
the top N tactics for various values of N, and all of these   fills the exact role of a more complex one in the original
proof commands are tried. Therefore, we also measured         proof; for instance, destruct (find_symbol ge id) in
how often the proof command in the original proof is in       an original proof is replaced by destruct find_symbol
the top 3 predictions, and the top 5 predictions. For all     in Proverbot9001’s solution. Other times it is because
proof commands in the data set, the tactic in the original    Proverbot9001 finds a proof which takes an entirely differ-
proof is in our top 3 predictions 38.93% of the time,         ent path than the original. In fact, 31 of Proverbot9001’s
and in our top 5 predictions 42.66% of the time. If we        97 found solutions are shorter than the original. It’s
restrict to proof commands in Proverbot9001’s prediction      useful to note that while previous work had a more ex-
domain, those numbers are 52.17% and 60.39%.                  pressive proof command model, in practice it was unable
                                                              to solve as many proofs as Proverbot9001 could in our
                                                              more restricted model.
A.2    Argument Accuracy
                                                                  Together, these numbers indicate that the restricted
Our argument prediction model is crucial to the success       tactic model used by Proverbot9001 does not inhibit its
of our system, and forms one of the main contributions        ability to solve proofs in practice, even when the original
of our work. To measure its efficacy at improving search      proof solution used tactics outside of that model.
is hard, because it’s impossible to separate its success
in progressing a proof from the success of the tactic
predictor. However, we can measure how it contributes          A.4    Data Transformation
to individual prediction accuracy.                             Crucial to Proverbot9001’s performance is its ability to
   On our test dataset, where we can predict the full          learn from data which is not initially in its proof com-
proof command in the original proof correctly 28.66% of        mand model, but can be transformed into data which
the time, we predict the tactic correctly but the argu-        is. This includes desugaring tacticals like now, splitting
ment wrong 32.24% of the time. Put another way, when           up multi-argument tactics like unfold a, b into single
we successfully predict the tactic, we can predict the         argument ones, and rearranging proofs with semicolons
argument successfully with 89% accuracy. If we only test       into linear series of proof commands. To evaluate how
on proof commands within Proverbot9001’s prediction            much this data transformation contributes to the overall
domain, where we correctly predict the entire proof com-       performance of Proverbot9001, we disabled it, and in-
mand 39.25% of the time, we predict the name correctly         stead filtered the proof commands in the dataset which
41.01% of the time; that is, our argument accuracy is          did not fit into our proof command model.
96% when we get the tactic right. It’s important to               With data transformation disabled, and the default
note, however, that many common tactics don’t take             search width (5) and depth (6), the proof completion
any arguments, and thus predicting their arguments is          accuracy of Proverbot9001 is 15.57% (78/501 proofs).
trivial.                                                       Recall that with data transformation enabled as usual,
Generating Correctness Proofs with Neural Networks                                 MAPL ’20, June 15, 2020, London, UK


this accuracy is 19.36%. This shows that the end-to-end       To explore the space of possible depths and widths, we
performance of Proverbot9001 benefits greatly from the     varied the depth and width, on our default configuration
transformation of input data, although it still outper-    without external tooling. With a search width of 1 (no
forms prior work (CoqGym) without it.                      search, just running the first prediction), and a depth
   When we measure the individual prediction accuracy      of 6, we can solve 5.59% (28/501) of proofs in our test
of our model, trained without data transformation, we      dataset. With a search width of 2, and a depth of 6, we’re
see that its performance significantly decreases (16.32%   able to solve 16.17% (81/501) of proofs, as opposed to a
instead of 26.77%), demonstrating that the extra data      width of 3 and depth of 6, where we can solve 19.36% of
produced by preprocessing is crucial to training a good    proofs.
tactic predictor.                                             To explore variations in depth, we set the width at 3,
                                                           and varied depth. With a depth of 2, we were able to
A.5    Search Widths and Depths                            solve 5.19% (26/501) of the proofs in our test set. By
Our search procedure has two main parameters, a search     increasing the depth to 4, we were able to solve 13.97%
width, and a search depth. The search width is how many    (70/501) of the proofs in our test set. At a depth of 6
predictions are explored at each context. The search       (our default), that amount goes up to 19.36% (97/501).
depth is the longest path from the root a single proof
obligation state can have.
