                                              Machine-Learned Premise Selection for Lean⋆

                                                 Bartosz Piotrowski1 , Ramon Fernández Mir2 , and Edward Ayers3
                                                         1
                                                             University of Warsaw and Czech Technical University
                                                                        bartoszpiotrowski@post.pl
                                                                          2
                                                                            University of Edinburgh
                                                                        3
                                                                           Carnegie Mellon University
arXiv:2304.00994v2 [cs.AI] 14 Jun 2023




                                                 Abstract. We introduce a machine-learning-based tool for the Lean
                                                 proof assistant that suggests relevant premises for theorems being proved
                                                 by a user. The design principles for the tool are (1) tight integration with
                                                 the proof assistant, (2) ease of use and installation, (3) a lightweight and
                                                 fast approach. For this purpose, we designed a custom version of the ran-
                                                 dom forest model, trained in an online fashion. It is implemented directly
                                                 in Lean, which was possible thanks to the rich and efficient metaprogram-
                                                 ming features of Lean 4. The random forest is trained on data extracted
                                                 from mathlib – Lean’s mathematics library. We experiment with various
                                                 options for producing training features and labels. The advice from a
                                                 trained model is accessible to the user via the suggest_premises tactic
                                                 which can be called in an editor while constructing a proof interactively.

                                                 Keywords: Lean theorem prover · proof assistants · premise selection ·
                                                 machine learning



                                         1     Introduction

                                         Formalizing mathematics in proof assistants is an ambitious and hard under-
                                         taking. One of the major challenges in constructing formal proofs of theorems
                                         depending on multiple other results is the prerequisite of having a good familiar-
                                         ity with the structure and contents of the library. Tools for helping users search
                                         through formal libraries are currently limited.
                                             In the case of the Lean proof assistant [11], users may look for relevant lemmas
                                         in its formal library, mathlib [5], either by (1) using general textual search tools
                                         and keywords, (2) browsing the related source files manually, (3) using mathlib’s
                                         suggest or library_search tactics.
                                             Approaches (1) and (2) are often slow and tedious. The limitation of approach
                                         (3) is the fact that suggest or library_search propose lemmas that strictly match
                                         the goal at the current proof state. This is often very useful, but it also means
                                         that these tactics often fail to direct the user to relevant lemmas that do not
                                         ⋆
                                             The results were supported by the Hoskinson Center for Formal Mathematics (BP,
                                             RFM, EA), the Kościuszko Foundation (BP), and the Principal’s Career Develop-
                                             ment Scholarship of the University of Edinburgh (RFM).
2       Piotrowski, Fernández Mir, Ayers

match the current goal exactly. They may also suggest too many trivial lemmas
if the goal is simple.
    The aim of this project is to make progress towards improving the situation
of a Lean user looking for relevant lemmas while building proofs. We develop a
new tool that efficiently computes a ranking of potentially useful lemmas selected
by a machine learning (ML) model trained on data extracted from mathlib. This
ranking can be accessed and used interactively via the suggest_premises tactic.
    The project described here belongs to the already quite broad body of work
dealing with the problem of fact selection for theorem proving [9,1,13,7]. This
problem, commonly referred to as the premise selection problem, is a crucial
when performing automated reasoning in large formal libraries, both in the con-
text of automated (ATP) and interactive (ITP) theorem proving, regardless of
the underlying logical calculus. Most of the existing work on premise selection fo-
cuses on the ATP context. Our main contribution is the development of a premise
selection tool that is practically usable in a proof assistant, tightly integrated
with it, lightweight, extendable, and equipped with a convenient interface.


2     Dataset Collection

A crucial requirement of a useful ML model is a high-quality dataset of training
examples. It should represent the learning task well and be suitable for the ML
architecture being applied.
    In this work, we use simple ML architectures that cannot process raw theorem
statements and require featurization as a preprocessing step. The features need
to be meaningful yet simple so that the model can use them appropriately. Our
approach is described in Section 2.1. The notion of relevant premise may be
understood differently depending on the context. In Section 2.2, we describe the
different specifications of this notion that we used in our experiments.
    The tool developed in this work is implemented and meant to be used in
Lean 4 together with mathlib 4. However, since, at the time of writing, Lean 4’s
version of the library is still being ported from Lean 3, we use mathlib3port4 as
our main data source.


2.1    Features

The features, similar to those used in [8,13], consist of the symbols used in the
theorem statement with different degrees of structure. In particular, three types
of features are used: names, bigrams and trigrams. As an illustration, take this
theorem about groups with zero:
theorem div_ne_zero (ha : a ̸= 0) (hb : b ̸= 0) : a / b ̸= 0 := . . .

   The most basic form of featurization is the bag-of-words model, where we
simply collect all the names (and numerical constants) involved in the theorem.
4
    https://github.com/leanprover-community/mathlib3port (commit f4e5dfe)
                                 Machine-Learned Premise Selection for Lean           3

Following this definition naively, we would obtain ̸=, 0 and /. The reality is a bit
more complicated as there are names in the expression that are hidden by the
notation, e.g. OfNat.ofNat.
    Some of the names in div_ne_zero are listed below. The ones starting with T
appear in the conclusion, while the ones starting with H appear in the hypotheses.
H:OfNat.ofNat H:MonoidWithZero.toZero H:0 H:Ne T:HDiv.hDiv T:0 T:Ne . . .
    It would be desirable, however, to keep track of which symbols appear next
to each other in the syntactic trees of the theorem hypotheses and its statement.
Thus, we extract bigrams that are formed by the head symbol and each of its
arguments (separated by / below).
H:Ne/OfNat.ofNat H:OfNat.ofNat/0 T:OfNat.ofNat/0 T:Ne/OfNat.ofNat . . .
   Similarly, we also consider trigrams, taking all paths of length 3 from the
syntactic tree of the expression.
H:Ne/OfNat.ofNat/0 H:Ne/OfNat.ofNat/Zero.toOfNat0 . . .


2.2   Relevant Premises
To obtain the list of all the premises used in the proof term it suffices to tra-
verse the Lean expression and keep track of all the constants whose type is a
proposition. For instance, the raw list of premises that appear in the proof of
div_ne_zero is:
GroupWithZero.noZeroDivisors mul_ne_zero inv_ne_zero Eq.refl
    div_eq_mul_inv
   For more complicated examples, this approach results in a large number of
premises including lemmas used implicitly by tactics (for instance, those picked
by the ‘simplify’ tactic simp), or simple facts that a user would rarely write
explicitly. Three different filters are applied to mitigate this issue: all, source,
and math. They are described below and their overall effect is shown in Table 1.

 1. The all filter preserves almost all premises from the original, raw list, remov-
    ing those that were generated automatically by Lean. They contain a leading
    underscore in their names, e.g., RingTheory.MatrixAlgebra._auxLemma.1. In
    our example, there are no such premises. Examples from this filter are not
    appropriate for training an ML advisor for interactive use as the suggestions


Table 1. Filters’ statistics. An example is a theorem with a non-empty list of premises.

                                              all source math
                     Total premises      96 915 28 784 67 462
                     Total examples      41 755 20 571 40 187
                     Premises per example 3.12 2.35 2.09
4       Piotrowski, Fernández Mir, Ayers

    would contain many lemmas used implicitly by tactics. Yet, such an advisor
    could be used for automated ITP approaches such as hammers [3].
 2. The source filter leaves only those premises that appear in the proof’s source
    code. The idea is to model the explicit usage of premises by a user. Following
    our example, we would take the following proof as a string and list only the
    three premises appearing there:
     by rw [div_eq_mul_inv]; exact mul_ne_zero ha (inv_ne_zero hb)
 3. The math filter preserves only lemmas that are clearly of mathematical na-
    ture, discarding basic, technical ones. The names of all theorems and defini-
    tions from mathlib are extracted and used as a white list. In particular, this
    means that many basic lemmas from Lean’s core library (e.g. Eq.refl from
    our example) are filtered out.

    In addition to our base datasets containing one data point per theorem, we
also created a dataset (labeled as intermediate) representing intermediate proof
states. To this end, we used LeanInk,5 a helper tool for Alectryon [14] – a toolkit
that aids exploration of tactical proof scripts without running the proof assistant.
Given a Lean file, LeanInk generates all the states that a user might be able to see
in the infoview (a panel in Lean that displays goal states and other information
about the prover’s state) by clicking on the file. The file is split into fragments,
each containing a string of Lean code, represented by a list of tokens, together
with the proof states before and after. In this way, the file can be loaded statically
simulating the effect of running Lean. Furthermore, it can be configured to keep
track of typing information, which is key to detecting which tokens are premises.
We modified LeanInk so that every fragment that appears inside a proof is treated
as its own theorem by our extractor. We gather all the premises found in the list
of tokens and featurize the hypotheses and goals in the “before” proof state.
    This dataset consists of 91 292 examples and 143 165 premises, which gives
an average of around 1.57 premises per example. It represents more fine-grained
use of the premises, which is not exactly corresponding to our main objective of
providing rankings of premises on the level of theorem statements. We treat it
as an auxiliary dataset potentially useful for augmenting our base data sets.


3     Machine Learning Models
The task modelled here with ML is predicting a ranking of likely useful premises
(lemmas and theorems) conditioned by the features of the statement of a theorem
being proved by a user. The nature of this problem is different than common
applications of classical ML: both the number of features and labels (premises) to
predict is large, and the training examples are sparse in the feature space. Thus,
we could not directly rely on traditional implementations of ML algorithms, and
using custom-built versions was necessary. As one of our design requirements was
tight integration with the proof assistant, we implemented the ML algorithms
5
    https://github.com/leanprover/LeanInk
                                  Machine-Learned Premise Selection for Lean             5

directly in Lean 4, without needing to call external tools. This also served as a
test for the maturity and efficiency of Lean 4 as a programming language.
    In Sections 3.1 and 3.2 we describe two machine learning algorithms imple-
mented in this work: k-nearest neighbours (k-NN) and random forest.


3.1   k -Nearest Neighbours

This is a classical and conceptually simple ML algorithm [6], which has already
been used multiple times for premise selection [2,9,10]. It belongs to the lazy
learning category, meaning that it does not result in a prediction model trained
beforehand on the dataset, but rather the dataset is an input to the algorithm
while producing the predictions.
    Given an unlabeled example, k-NN produces a prediction by extracting the
labels of the k most similar examples in the dataset and returning an averaged
(or most frequent) label. In our case, the labels are lists of premises. We com-
pose multiple labels into a ranking of premises according to the frequency of
appearance in the concatenated labels.
    The similarity measure in the feature space calculates how many features
are shared between the two data points, but additionally puts more weight on
those features that are rarer in the whole training dataset D. The formula for
the similarity of the two examples x1 and x2 associated with sets of features f1
and f2 , respectively, is given below.
                                P                                                      2
                                 f ∈f1 ∩f2 t(f )
                                                                               
                                                                                  |D|
 M (x1 , x2 ) = P               P               P                , t(f ) = log            ,
                  f ∈f1 t(f ) +  f ∈f2 t(f ) −   f ∈f1 ∩f2 t(f )                 |Df |

where Df are those training examples that contain the feature f .
    The advantages of k-NN are its simplicity and the lack of training. A disad-
vantage, however, is the need to traverse the whole training dataset in order to
produce a single prediction (a ranking). This may be slow, and thus not optimal
for interactive usage in proof assistants.


3.2   Random Forest

As an alternative to k-NN, we use random forest [4] – an ML algorithm from the
eager learning category, with a separate training phase resulting in a prediction
model consisting of a collection of decision trees. The leaves of the trees contain
labels, and their nodes contain decision rules based on the features. In our case,
the labels are sets of premises, and the rules are simple tests that check if a given
feature appears in an example.
    When predicting, unlabeled examples are passed down the trees to the leaves,
the reached labels are recorded, and the final prediction is averaged across the
trees via voting. The trees are trained in such a way as to avoid correlations
between them, and the averaged prediction from them is of better quality than
the prediction from a single tree.
6           Piotrowski, Fernández Mir, Ayers

    Our version of random forest, adapted to deal with sparse binary features and
a large number of labels, is similar to the one used in [16]. It is trained in an online
manner, i.e., it is updated sequentially with single training examples – not with
the entire training dataset at once, as is typically done. The rationale for this is
to make it easy to update the model with data coming from new theorems proved
by a user. This allows the model to immediately provide suggestions taking into
account these recently added theorems.6


                                                      Fig. 1. A schematic example of a deci-
                                                      sion tree from a trained random forest.
    Input                    Tree                     Lowercase letters (a, b, c, ...) designate
 b, c, e, h                   a                       features of theorem statements, whereas
                                                      uppercase letters (P, Q, R, ...) designate
                       e            P, Q              names of premises. The input (a featur-
                                                      ized theorem statement) is being passed
                                                      down the tree (along the green arrows)
               R, S           c                       so that each node tests for a presence of
                                            Output    a single feature, and passes the input ex-
                      R, X        R, T, U   R, T, U   ample to the left (or right) sub-tree in the
                                                      negative (or positive) case. The output is
                                                      a set of premises in the reached leaf.



    Algorithm 1 provides a sketch of how a training example updates a tree – for
all the details see the actual implementation in our public GitHub repository.7
A crucial part of the algorithm is the MakeSplitRule function creating node
splitting rules. Searching for the rules resulting in optimal splits would be costly,
thus this function relies on heuristics.
    Figure 1 schematically depicts how a simple decision tree from a trained
random forest predicts a set of premises for an input example.


4     Evaluation Setup and Results

To assess the performance of the ML algorithms, the data points extracted from
mathlib were split into training and testing sets. The testing examples come from
the modules that are not dependencies of any other modules (there are 592 of
them). This simulates a realistic scenario in which a user utilizing the suggestion
tool develops a new mathlib module. The rest of the modules (2436) served as
the source of training examples.
    Two measures of the quality of the rankings produced by ML are defined:
Cover and Cover+ . Assuming a theorem T depends on the set of premises P of
size n, and R is the ranking of premises predicted by the ML advisor for T , these
6
    This mode, however, has not yet been tested in the current stage of this work.
7
    https://github.com/BartoszPiotrowski/lean-premise-selection
                                 Machine-Learned Premise Selection for Lean           7

Algorithm 1 Updating a tree with a training example in a random forest.
 1: function AddExampleToTree(T , e) ▷ T – tree to update, e – training example
 2:    match T with
 3:       Node(R, Tl , Tr ):        ▷ R – binary rule, Tl , Tr – left and right subtrees
 4:          match R(e) with              ▷ passing example e down the tree to a leaf
 5:              Left: return Node(R, AddExampleToTree(Tl , e), Tr )
 6:              Right: return Node(R, Tl , AddExampleToTree(Tr , e))
 7:       Leaf(E):                                   ▷ E – examples stored in the leaf
 8:          E ← Append(E, e)
 9:          if SplitCondition(E) then             ▷ testing if the leaf should be split
10:              R ← MakeSplitRule(E) ▷ making semi-optimized new split rule
11:              E l , E r ← Split(R, E)           ▷ splitting examples into two parts
12:              return Node(R, Leaf(El ), Leaf(Er )) ▷ new subtree growing the tree
13:          else
14:              return Leaf(E)         ▷ the original leaf augmented with example e



measures are defined as follows:
                      P ∩ R[:n]                             P ∩ R[:n + 10]
       Cover(T ) =              ,           Cover+ (T ) =                  ,
                          n                                       n
where R[:k] is a set of k initial premises from ranking R. Both Cover and
Cover+ return values in [0, 1]. Cover gives the score of 1 only for a “perfect”
prediction where the premises actually used in the proof form an initial segment
of the ranking. Cover+ may also give a perfect score to less precise predictions.
The rationale for Cover+ is that the user in practice may look through 10 or
more suggested premises. This is often more than the n premises actually used
in the proof, so we consider initial segments of length n + 10 in Cover+ .
     Both k-NN and random forest are evaluated on data subject to all three
premise filters described in Section 2.2. For each of these variants of data, three
combinations of features are tested: (1) names only, (2) names and bigrams, (3)
names, bigrams, and trigrams. The hyper-parameters for the ML algorithms
were selected by an experiment on a smaller dataset. For k-NN, the number
of neighbours was fixed to 100. For random forest, the number of trees was
set to 300, each example was used for training a particular decision tree with
probability equal to 0.3, and the training algorithm passed through the whole
training data 3 times.
     Table 2 shows the results of the experiment. In terms of the Cover metric,
random forest performed better than k-NN for all data configurations. However,
for Cover+ metric, k-NN surpassed random forest for the math filter.
     It turned out that the union of names and bigrams constitutes the best
features for all the filters and both ML algorithms. It likely means that the more
complex trigrams did not help the algorithms to generalize well but rather
caused over-fitting on the training set.
     The results for the all filter appear to be much higher than for the other two
filters. However, this is because applying all results in many simple examples
8          Piotrowski, Fernández Mir, Ayers

Table 2. Average performance of random forest and k-NN on testing data, for three
premises filters and three kinds of features. The type of features is indicated by a one-
letter abbreviation: n = names, b = bigrams, t = trigrams. For each configuration,
Cover and Cover+ measures are reported (the latter in brackets). In each row, the best
Cover result is bolded.

                                     machine learning model
                          random forest                     k-nearest neighbours

    premises        n         n+b         n+b+t         n          n+b       n+b+t

    all        0.56 (0.67) 0.57 (0.67) 0.47 (0.58) 0.51 (0.65) 0.52 (0.66) 0.51 (0.62)
    source     0.28 (0.36) 0.29 (0.36) 0.28 (0.36) 0.25 (0.35) 0.25 (0.36) 0.26 (0.35)
    math       0.25 (0.32) 0.26 (0.33) 0.16 (0.24) 0.22 (0.34) 0.23 (0.34) 0.16 (0.26)



containing just a few common, basic premises (e.g., just a single rfl lemma).
They increase the average score.
    Overall, random forest with names + bigrams (n+b) features gives the best
results. An additional practical advantage of this model over k-NN is the speed
of outputting predictions. For instance, for the source filter and n+b features,
the average times of predicting a ranking of premises per theorem were 0.28 s
and 5.65 s for random forest and k-NN, respectively.
    Additionally, we evaluated the ML models on the intermediate dataset,
using n+b features. The random forest achieved Cover = 0.09 and Cover+ = 0.24,
whereas k-NN resulted in Cover = 0.08 and Cover+ = 0.21 on the testing part of
the data. Then, we used the intermediate dataset in an attempt to improve the
testing results on the base dataset with the source filter (as intermediate only
contains premises visible in the source files). We used the intermediate data as
a pre-training dataset, first training a random forest on it, and later on the base
data. We also used intermediate to augment the base data, mixing the two
together. However, neither in the pre-training, nor in the augmentation mode
statistically significant improvements in the testing performance were achieved.
It is possible that the prediction quality from the practical perspective actually
improved, being more proof-state-dependent and not only theorem-dependent,
but it did not manifest in our theorem-dependent evaluation.
    The evaluation may be reproduced by following the instructions in the linked
source code.8


5     Interactive Tool
The ML predictor is wrapped in an interactive tactic suggest_premises that
users can type into their proof script. It will invoke the predictor and produce a
8
    https://github.com/BartoszPiotrowski/lean-premise-selection#
    reproducing-evaluation
                                 Machine-Learned Premise Selection for Lean          9

list of suggestions. This list is displayed in the infoview. The display makes use
of the new remote-procedure-call (RPC) feature in Lean 4 [12], to then asyn-
chronously run various tactics for each suggestion. Given a suggested premise p,
the system will attempt to run tactics apply p, rw [p] and simp only [p], and
return the first successful tactic application that advances the state. This will
then be displayed to the user as shown in Figure 2. She can select the resulting
tactic to insert into the proof script. By using an asynchronous approach, we
can display results rapidly without waiting for a slow tactic search to complete.




Fig. 2. The interactive tool in Visual Studio Code. The left pane shows the source file
with the cursor over a suggest_premises tactic. The right pane shows the goal state
at the cursor position and, below, the suggested lemmas to solve the goal. Suggestions
annotated with a checkbox advance the goal state, suggestions annotated with confetti
close the current goal. Clicking on a suggested tactic (e.g. apply mul_left_eq_self)
automatically appends to the proof script on the left.




6    Future Work
There are several important directions in which the current work may be de-
veloped. The results may be improved by augmenting the dataset with, for in-
stance, synthetic theorems, as well as developing better features, utilizing the
well-defined structure of Lean expressions.
    Applying modern neural architectures in place of the simpler ML algorithms
used here is a promising path [15]. It would depart from our philosophy of a
lightweight, self-contained approach as the suggestions would come from an ex-
ternal tool, possibly placed on a remote server. However, given the strength of the
current neural networks, we could hope for higher-quality predictions. Moreover,
neural models do not require hand-engineered features.
    Finally, premise selection is an important component of ITP hammer systems
[3]. The presented tool may be readily used for a hammer in Lean, which has
not yet been developed.
10      Piotrowski, Fernández Mir, Ayers

References
 1. Alama, J., Heskes, T., Kühlwein, D., Tsivtsivadze, E., Urban, J.: Premise selec-
    tion for mathematics by corpus analysis and kernel methods. J. Autom. Reason.
    52(2), 191–213 (2014). https://doi.org/10.1007/s10817-013-9286-5, https:
    //doi.org/10.1007/s10817-013-9286-5
 2. Blanchette, J.C., Greenaway, D., Kaliszyk, C., Kühlwein, D., Urban, J.: A
    learning-based fact selector for Isabelle/HOL. J. Autom. Reason. 57(3), 219–
    244 (2016). https://doi.org/10.1007/s10817-016-9362-8, https://doi.org/
    10.1007/s10817-016-9362-8
 3. Blanchette, J.C., Kaliszyk, C., Paulson, L.C., Urban, J.: Hammering towards
    QED. J. Formaliz. Reason. 9(1), 101–148 (2016). https://doi.org/10.6092/
    issn.1972-5787/4593, https://doi.org/10.6092/issn.1972-5787/4593
 4. Breiman, L.: Random forests. Mach. Learn. 45(1), 5–32 (2001)
 5. mathlib Community, T.: The Lean mathematical library. In: Proceedings of the
    9th ACM SIGPLAN International Conference on Certified Programs and Proofs.
    p. 367–381. CPP 2020, Association for Computing Machinery, New York, NY,
    USA (2020). https://doi.org/10.1145/3372885.3373824, https://doi.org/10.
    1145/3372885.3373824
 6. Hastie, T., Tibshirani, R., Friedman, J.H.: The Elements of Statistical Learning:
    Data Mining, Inference, and Prediction, 2nd Edition. Springer Series in Statistics,
    Springer (2009). https://doi.org/10.1007/978-0-387-84858-7, https://doi.
    org/10.1007/978-0-387-84858-7
 7. Irving, G., Szegedy, C., Alemi, A.A., Eén, N., Chollet, F., Urban, J.:
    Deepmath – deep sequence models for premise selection. In: Lee, D.D.,
    Sugiyama, M., von Luxburg, U., Guyon, I., Garnett, R. (eds.) Advances
    in Neural Information Processing Systems 29: Annual Conference on Neu-
    ral Information Processing Systems 2016, December 5-10, 2016, Barcelona,
    Spain. pp. 2235–2243 (2016), https://proceedings.neurips.cc/paper/2016/
    hash/f197002b9a0853eca5e046d9ca4663d5-Abstract.html
 8. Jakubuv, J., Urban, J.: ENIGMA: Efficient learning-based inference guiding ma-
    chine. In: Geuvers, H., England, M., Hasan, O., Rabe, F., Teschke, O. (eds.) In-
    telligent Computer Mathematics – 10th International Conference, CICM 2017,
    Edinburgh, UK, July 17-21, 2017, Proceedings. Lecture Notes in Computer
    Science, vol. 10383, pp. 292–302. Springer (2017). https://doi.org/10.1007/
    978-3-319-62075-6_20, https://doi.org/10.1007/978-3-319-62075-6_20
 9. Kaliszyk, C., Urban, J.: Learning-assisted automated reasoning with Fly-
    speck. J. Autom. Reason. 53(2), 173–213 (2014). https://doi.org/10.1007/
    s10817-014-9303-3, https://doi.org/10.1007/s10817-014-9303-3
10. Kaliszyk, C., Urban, J.: Mizar 40 for mizar 40. J. Autom. Reason. 55(3), 245–
    256 (2015). https://doi.org/10.1007/s10817-015-9330-8, https://doi.org/
    10.1007/s10817-015-9330-8
11. de Moura, L., Ullrich, S.: The Lean 4 theorem prover and programming lan-
    guage. In: Platzer, A., Sutcliffe, G. (eds.) Automated Deduction - CADE 28 -
    28th International Conference on Automated Deduction, Virtual Event, July 12-
    15, 2021, Proceedings. Lecture Notes in Computer Science, vol. 12699, pp. 625–
    635. Springer (2021). https://doi.org/10.1007/978-3-030-79876-5_37, https:
    //doi.org/10.1007/978-3-030-79876-5_37
12. Nawrocki, W., Ayers, E.W., Ebner, G.: An extensible user interface for Lean 4.
    In: 14th International Conference on Interactive Theorem Proving, ITP 2023, July
                                Machine-Learned Premise Selection for Lean        11

    31–August 4, 2023, Białystok, Poland. Schloss Dagstuhl - Leibniz-Zentrum für
    Informatik (2023)
13. Piotrowski, B., Urban, J.: ATPboost: Learning premise selection in binary set-
    ting with ATP feedback. In: Galmiche, D., Schulz, S., Sebastiani, R. (eds.) Au-
    tomated Reasoning - 9th International Joint Conference, IJCAR 2018, Held as
    Part of the Federated Logic Conference, FloC 2018, Oxford, UK, July 14-17,
    2018, Proceedings. Lecture Notes in Computer Science, vol. 10900, pp. 566–
    574. Springer (2018). https://doi.org/10.1007/978-3-319-94205-6_37, https:
    //doi.org/10.1007/978-3-319-94205-6_37
14. Pit-Claudel, C.: Untangling mechanized proofs. In: Proceedings of the 13th
    ACM SIGPLAN International Conference on Software Language Engineering. p.
    155–174. SLE 2020, Association for Computing Machinery, New York, NY, USA
    (2020). https://doi.org/10.1145/3426425.3426940, https://pit-claudel.fr/
    clement/papers/alectryon-SLE20.pdf
15. Tworkowski, S., Mikula, M., Odrzygóźdź, T., Czechowski, K., Antoniak, S., Jiang,
    A.Q., Szegedy, C., Łukasz Kuciński, Miłoś, P., Wu, Y.: Formal premise selection
    with language models. In: The 7th Conference on Artificial Intelligence and Theo-
    rem Proving, AITP 2022, September 4-9, 2022, Aussois and online, France (2022),
    http://aitp-conference.org/2022/abstract/AITP_2022_paper_32.pdf
16. Zhang, L., Blaauwbroek, L., Piotrowski, B., Cerný, P., Kaliszyk, C., Urban,
    J.: Online machine learning techniques for Coq: A comparison. In: Kamared-
    dine, F., Coen, C.S. (eds.) Intelligent Computer Mathematics - 14th Interna-
    tional Conference, CICM 2021, Timisoara, Romania, July 26-31, 2021, Pro-
    ceedings. Lecture Notes in Computer Science, vol. 12833, pp. 67–83. Springer
    (2021). https://doi.org/10.1007/978-3-030-81097-9_5, https://doi.org/10.
    1007/978-3-030-81097-9_5
