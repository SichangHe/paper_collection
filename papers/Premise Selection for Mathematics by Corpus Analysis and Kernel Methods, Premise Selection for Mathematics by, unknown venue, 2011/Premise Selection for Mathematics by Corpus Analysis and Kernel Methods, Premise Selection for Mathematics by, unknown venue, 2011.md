                                        Noname manuscript No.
                                        (will be inserted by the editor)




                                        Premise Selection for Mathematics by
                                        Corpus Analysis and Kernel Methods

                                        Jesse Alama∗ · Tom Heskes∗∗ · Daniel
                                        Kühlwein∗∗ · Evgeni Tsivtsivadze∗∗ ·
                                        Josef Urban∗∗




                                        the date of receipt and acceptance should be inserted later
arXiv:1108.3446v2 [cs.LG] 12 Apr 2012




                                        Abstract Smart premise selection is essential when using automated reason-
                                        ing as a tool for large-theory formal proof development. A good method for
                                        premise selection in complex mathematical libraries is the application of ma-
                                        chine learning to large corpora of proofs.
                                            This work develops learning-based premise selection in two ways. First,
                                        a newly available minimal dependency analysis of existing high-level formal
                                        mathematical proofs is used to build a large knowledge base of proof depen-
                                        dencies, providing precise data for ATP-based re-verification and for train-
                                        ing premise selection algorithms. Second, a new machine learning algorithm
                                        for premise selection based on kernel methods is proposed and implemented.
                                        To evaluate the impact of both techniques, a benchmark consisting of 2078
                                        large-theory mathematical problems is constructed, extending the older MPTP
                                        Challenge benchmark. The combined effect of the techniques results in a 50%
                                        improvement on the benchmark over the Vampire/SInE state-of-the-art sys-
                                        tem for automated reasoning in large theories.


                                        1 Introduction

                                        In this paper we significantly improve theorem proving in large formal mathe-
                                        matical libraries by using a two-phase approach combining precise proof anal-
                                        ysis with machine learning of premise selection.
                                            The first phase makes the first practical use of the newly available min-
                                        imal dependency analysis of the proofs in the large Mizar Mathematical Li-
                                        ∗  Center for Artificial Intelligence, New University of Lisbon. Funded by the FCT project
                                        “Dialogical Foundations of Semantics” (DiFoS) in the ESF EuroCoRes programme Log-
                                        ICCC (FCT LogICCC/0001/2007). Research for this paper was partially done while a vis-
                                        iting fellow at the Isaac Newton Institute for the Mathematical Sciences in the programme
                                        ‘Semantics & Syntax’.
                                        ∗∗ Intelligent Systems, Institute for Computing and Information Sciences, Radboud Uni-

                                        versity Nijmegen. Funded by the NWO projects “Learning2Reason” and “MathWiki”.
2                                  Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


brary (mml)1 . This analysis allows us to construct precise problems for ATP-
based re-verification of the Mizar proofs. More importantly, the precise depen-
dency data can be used as a large repository of previous problem-solving knowl-
edge from which premise selection can be efficiently automatically learned by
machine learning algorithms.
    In the second phase, a complementary improvement is achieved by using
a new kernel-based machine learning algorithm, which outperforms existing
methods for premise selection. This means that based on the large number
of previously solved mathematical problems, we can more accurately estimate
which premises will be useful for proving a new conjecture.
    Such learned knowledge considerably helps automated proving of new for-
mally expressed mathematical problems by recommending the most relevant
previous theorems and definitions from the very large existing libraries, and
thus shielding the existing ATP methods from considering thousands of irrel-
evant axioms. The better such symbiosis of formal mathematics and learning-
assisted automated reasoning gets, the better for both parties: improved auto-
mated reasoning increases the efficiency of formal mathematicians, and lowers
the cost of producing formal mathematics. This in turn leads to larger corpora
of previously solved nontrivial problems from which the learning-assisted ATP
can extract additional problem-solving knowledge covering larger and larger
parts of mathematics.
    The rest of the paper is organized as follows. Section 2 describes recent
developments in large-theory automated reasoning and motivates our prob-
lem. Section 3 summarizes the recent implementation of precise dependency
analysis over the large mml, and its use for ATP-based cross-verification and
training premise selection. Section 4 describes the general machine learning ap-
proach to premise selection and an efficient kernel-based multi-output ranking
algorithm for premise selection. In Section 5 a new large-theory benchmark of
2078 related mml problems is defined, extending the older and smaller MPTP
Challenge benchmark, and our techniques are evaluated on this benchmark in
Section 6. Section 7 concludes and discusses future work and extensions.


2 Automated Reasoning in Large Theories (ARLT)

In recent years, large formal libraries of re-usable knowledge expressed in rich
formalisms have been built with interactive proof assistants, such as Mizar [11],
Isabelle [17], Coq [6], HOL (light) [13], and others. Formal approaches are also
being used increasingly in non-mathematical fields such as software and hard-
ware verification and common-sense reasoning about real-world knowledge.
Such trends lead to growth of formal knowledge bases in these fields.
    One important development is that a number of these formal knowledge
bases and core logics have been translated to first-order formats suitable for
ATPs [16, 32, 19], and first-order ATP is today routinely used for proof as-
sistance in systems like Isabelle [18, 7], Mizar [35, 34], and HOL [12]. These
    1   http://www.mizar.org
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods                  3


first-order translations give rise to large, semantically rich corpora that present
significant new challenges for the field of automated reasoning. The techniques
developed so far for ATP in large theories can be broadly divided into two cat-
egories:
1. Heuristic symbolic analysis of the formulas appearing in problems, and
2. Analysis of previous proofs.
In the first category, the SInE preprocessor by K. Hoder [14, 33] has so far been
the most successful. SInE is particularly strong in domains with many hierar-
chical definitions such as those in common-sense ontologies. In the second cat-
egory, machine learning of premise selection, as done e.g. by the MaLARea [36]
system, is an effective method in hard mathematical domains, where the knowl-
edge bases contain proportionally many more nontrivial lemmas and theorems
than simple definitions, and previous verified proofs can be used for learning
proof guidance.
    Automated reasoning in large mathematical corpora is an interesting new
field in several respects. Large theories permit data-driven approaches [27]
to constructing ATP algorithms; indeed, the sheer size of such libraries ac-
tually necessitates such methods. It turns out that purely deductive, brute-
force search methods can be improved significantly by heuristic and induc-
tive2 methods, thus allowing experimental research into combinations [36] of
inductive and deductive methods. Large-theory benchmarks like the MPTP
Challenge3 , and its extended version developed here in Section 5, can serve
for rigorous evaluation of such novel Artificial Intelligence (AI) methods over
thousands of real-world mathematical problems.4 Apart from the novel AI as-
pect, and the obvious proof assistance aspect, automated reasoning over large
formal mathematical corpora can also become a new tool in the established
field of reverse mathematics [28]. This line of research has been already started,
for example by Solovay’s analysis [29] of the connection between Tarski’s ax-
iom [30] and the axiom of choice, and by Alama’s analysis of the Euler’s
polyhedron formula [1], both conducted over the mml.


3 Computing Minimal Dependencies in Mizar

In the world of automated theorem proving, proofs contain essentially all logi-
cal steps, even very small ones (such as the steps taken in a resolution proof).
In the world of interactive theorem proving, one of the goals is to allow the
users to express themselves with minimal verbosity. Towards that end, in-
teractive theorem proving (ITP) systems often come with mechanisms for
suppressing some steps of an argument. By design, an ITP can suppress logi-
cal and mathematical steps that might be necessary for a complete analysis of
 2  The word inductive denotes here inductive reasoning, as opposed to deductive reasoning.
 3  http://www.tptp.org/MPTPChallenge
  4 We do not evaluate on the CASC LTB datasets, because they are too small to allow

machine learning techniques. Our goal is to help mathematicians who work with and re-use
large amounts of previously established complex proofs and theorems.
4                                  Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


what a particular proof depends upon. In this section we summarize a recently
developed solution to this problem for the mml. The basis of the solution is
refactoring of the articles of the mml into one-item micro-articles, and comput-
ing their minimal dependencies by a brute-force minimization algorithm. For
a more detailed discussion of Mizar, see [15, 11]; for a more detailed discussion
of refactoring and minimization algorithms, see [4].
    As an example of how inferences in ITP-assisted formal mathematical
proofs can be suppressed, consider a theorem of the form

                                ∀x : τ [ψ (g(x))],

where “x : τ ” means that the variable x has type τ , and g is a unary function
symbol that accepts arguments of type τ 0 . Suppose further that, prior to the
assertion of this theorem, it is proved that τ is a subtype of τ 0 . The well-
formedness of the theorem depends on this subtyping relationship. Moreover,
the proof of the theorem may not mention this fact; the subtyping relationship
between τ and τ 0 may very well not be an outright theorem. In such a situation,
the fact
                               ∀x(x : τ → x : τ 0 )

is suppressed. We can see that by not requiring the author of a formal proof
to supply such subtyping relationships, we permit him to focus more on the
heart of the matter of his proof, rather than repeating the obvious. But if we
are interested in giving a complete answer to the question of what a formalized
proof depends upon, we must expose suppressed facts and inferences. Having
the complete answer is important for a number of applications, see [4] for
examples. The particular importance for the work described here is that when
efficient first-order ATPs are used to assist high-level formal proof assistants
like Mizar, the difference between the implicitly used facts and the explicitly
used facts disappears. The ATPs need to explicitly know all the facts that are
necessary for finding the proofs. (If we were to omit the subtyping axiom, for
example, an ATP might find that the problem is countersatisfiable.)
     The first step in the computation of fine-grained dependencies in Mizar is to
break up each article in the mml into a sequence of Mizar texts, each consisting
of a single top-level item (e.g., theorem, definition). Each of these texts can—
with suitable preprocessing—be regarded as a complete, valid Mizar article in
its own right. The decomposition of a whole article from the mml into such
smaller articles typically requires a number of nontrivial refactoring steps,
comparable, e.g., to automated splitting and re-factoring of large programs
written in programming languages with complicated syntactic mechanisms.
     In Mizar, every article begins with a so-called environment specifying the
background knowledge (theorems, notations, etc.) that is used to verify the
article. The actual Mizar content that is imported, given an environment, is,
in general, a rather conservative overestimate of the items that the article
actually needs. That is why we apply a greedy minimization process to the
environment to compute a minimal set of items that are sufficient to verify
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods                   5


each “micro-article”. This produces a minimal set of dependencies5 for each
Mizar item, both syntactic (e.g., notational macros), and semantic (e.g., the-
orems, typings, etc.). The drawback of this minimization process is that the
greedy approach to minimization6 of certain kinds of dependencies can be time
consuming.7 The advantage is that (unlike in any other proof assistant) the
computed set of dependencies is truly minimal (with respect to the power of the
proof checker), and does not include redundant dependencies which are typi-
cally drawn in by overly powerful proof checking algorithms (like congruence
closure over sets of all available equalities, etc.) when the dependency tracking
is implemented internally inside a proof assistant. The dependency minimiza-
tion is particularly important for the ATP and premise-selection applications
that are explained in this paper: a day more of routine computation of the
minimal dependencies is a very good time investment if it can provide better
guidance for the fast-growing search space explored by ATPs. Another advan-
tage of this approach is that it also provides syntactic dependencies, which are
needed for real-world recompilation of the particular item as written in the
article. This functionality is important for fast fine-grained recompilation in
formal wikis [2], however for semantic applications like ATP we are only con-
sidering the truly semantic dependencies, i.e., those dependencies that result
in a formula when translated by the MPTP system [32] to first-order logic.
    Table 1 provides a summary of the fine-grained dependency data for the
set of 33 Mizar articles coming from the MPTP2078 benchmark developed in
Section 5, and used for the experiments in Section 6. For each theorem in the
sequence of the 33 Mizar articles (ordered from first to last by their order in
the mml) we show how many explicit dependencies are involved (on average)
in their proofs and how many implicit dependencies (on average) it contains.
The table also shows how much of an improvement the exact dependency
calculation is, compared to a simple safe fixed-point MPTP construction of an
over-approximation of what is truly used in the mml proof.



4 Premise Selection in Large Theories by Machine Learning

When reasoning over a large theory (like the mml), thousands of premises are
available. In the presence of such large numbers of premises, the performance
of most ATP systems degrades considerably [33]. Yet typically only a fraction
of the available premises are actually needed to construct a proof. Estimating
which premises are likely to be useful for constructing a proof is our research
problem:

  5 Precisely, the minimality means that removing any dependence will cause the verification

to fail.
  6 The basic greedy minimization proceeds by checking if an article still compiles after

removing increasingly larger parts of the environment.
  7 This can be improved by heuristics for guessing the needed dependencies, analogous to

those used for ATP premise selection.
6                                       Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


Table 1 Effectiveness of fine-grained dependencies on the 33 MPTP2078 articles ordered
from top to bottom by their order in the mml.

    Article    Theorems   Expl. Refs.    Uniq. Expl. Refs.   Fine Deps.    MPTP Deps.

    xboole 0          7             4                  2.7        11.57            12.62
    xboole 1        117          5.34                  2.3        15.27            17.86
    enumset1         87          3.26                  2.7        10.67            10.82
    zfmisc 1        129          4.74                  2.9        16.59            21.08
    subset 1         43          4.62                  2.4        22.30            28.15
    setfam 1         48          6.56                  2.4        25.62            37.93
    relat 1         184          5.66                  2.2        19.97            27.31
    funct 1         107          7.69                  3.4        22.94            42.05
    ordinal1         37          7.81                  3.9           26            61.92
    wellord1         53          11.7                  5.6        30.45             55.5
    relset 1         32          4.71                  2.6           27            55.59
    mcart 1          92          5.71                  2.8        21.25            29.77
    wellord2         24          14.2                  6.9        36.41             75.2
    funct 2         124          4.14                  2.5        30.77            92.45
    finset 1         15          8.66                  3.9        23.93            72.22
    pre topc         36          6.47                  3.2        35.58            53.51
    orders 2         56          10.6                  5.3        46.28            79.77
    lattices         27          5.59                  3.1           43            72.96
    tops 1           71          6.67                  4.2        43.46            66.42
    tops 2           65          7.36                  4.0        37.41            103.4
    compts 1         23          17.7                  8.6        48.86            102.9
    connsp 2         29          9.86                  6.4        39.51             96.5
    filter 1         61          14.6                  5.3        52.27            122.8
    lattice3         55           8.6                  4.2        47.07            92.25
    yellow 0         70          6.75                  3.2        26.55            46.12
    yellow 1         28          9.03                  5.1        53.17            128.3
    waybel 0         76          9.34                  4.1        35.03            82.34
    tmap 1          141          8.78                  4.5        47.04            140.0
    tex 2            74          7.66                  5.0        37.31            155.6
    yellow 6         44          11.2                  6.4        50.31            173.5
    waybel 7         46          13.0                  7.7        57.10            140.3
    waybel 9         41             9                  5.2        51.56            156.5
    yellow19         36          8.44                  5.3        53.02            137.2

Article: Mizar Article relevant to the MPTP2078 benchmark.
Theorems: Total number of theorems in the article.
Expl. Refs.: Average number of (non-unique) explicit references (to theorems, definitional
    theorems, and schemes) per theorem in the article.
Uniq. Expl. Refs.: Average number of unique explicit references per theorem.
Fine Deps.: Average number of all (both explicitly and implicitly) used items (explicitly
    referred to theorems, together with implicitly used items) per theorem as computed by
    dependency analysis.
MPTP Deps.: Average number of items per theorem as approximated by the MPTP fixpoint
    algorithm.
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods                    7


Definition 1 (Premise selection problem)
Given a large number of premises P and a new conjecture c, predict those
premises from P that are likely to be useful for automatically constructing a
proof of c.
    Knowledge of previous proofs and problem-solving techniques is used by
mathematicians to guide their thinking about new problems. The detailed
mml proof analysis described above provides a large computer-understandable
corpus of dependencies of mathematical proofs. In this section we present
the machine learning setting and algorithms that are used to train premise
selection on such corpora. Our goal is to begin emulating the training of human
mathematicians.
    When the translation [32] from Mizar to ATP formats is applied, the Mizar
theorems and their proof dependencies (definitions, other theorems, etc.) trans-
late to first-order formulas, used in the corresponding ATP problems as con-
jectures and their premises (axioms). For further presentation here we identify
each mml formula with its first-order translation.8 We will work in the follow-
ing setting, which is tailored to the mml, but can easily be translated to other
large datasets. Let Γ be the set of first order formulas that appear in the mml.

Definition 2 (Proof matrix) Using the fine-grained Mizar proof analysis -
which says for each pair of formulas p, c ∈ Γ whether p is used in the mml
proof of c - define the function µ : Γ × Γ → {0, 1} by
                                (
                                 1 if p is used to prove c,
                     µ(c, p) :=
                                 0 otherwise.

In other words, µ is the adjacency matrix of the graph of the direct mml
proof dependencies. This proof matrix, together with suitably chosen formula
features, will be used for training machine learning algorithms.
    Note that in the mml, there is always exactly one (typically a textbook)
proof of a particular theorem c, and hence exactly one set of premises
usedP remises(c) := {p | µ(c, p) = 1} used in the proof of c. This corresponds
to the mathematical textbook practice where typically only one proof is given
for a particular theorem. It is however obvious that for example any expansion
of the proof dependencies can lead to an alternative proof.
    In general, given a mathematical theory, there can be a variety of more or
less related alternative proofs of a particular theorem. This variety however
typically is not the explicit textbook data on which mathematicians study.
Such variety is only formed (in different measure) in their minds, after studying
(training on) the textbook proofs, which typically are chosen for some nice
properties (simplicity, beauty, clarity, educational value, etc.). Hence it is also
plausible to use the set of mml proofs for training algorithms that attempt to
emulate human proof learning. Below we will often refer to the set of premises
  8 Mizar is “nearly first-order”, so the correspondence is “nearly” one-to-one, and in par-

ticular it is possible to construct the set of ATP premises from the exact Mizar dependencies
for each Mizar theorem.
8                                    Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


used in the (unique) mml proof of a theorem c as the set of premises of c.
This concept is not to be read as the only set of premises of c, but rather as
the particular set of premises that is used in human training, and therefore is
also likely to be useful in training computers. It would not be difficult to relax
this approach, if the corpora from which we learn contained a number of good
alternative proofs. This is however so far not the case with the current mml,
on which we conduct these experiments.
    Also note that although our training set consists of formal proofs, these
proofs have been authored by humans, and not found fully automatically by
ATPs. But the evaluation conducted here (Section 6) is done by running ATPs
on the recommended premises. It could be the case (depending on the ATP
implementation) that a fully automatically found proof would provide a better
training example than the human proof from the mml. A major obstacle for
such training is however the relative weakness of existing ATPs in finding more
involved proofs of mml theorems (see [33]), and thus their failure to provide
the training examples for a large part of mml. Still, a comparison of the power
of training on mml and ATP proofs could be interesting future work.
Definition 3 (Feature matrix) We characterize mml formulas by the sym-
bols and (sub)terms appearing in them. We use de Bruijn indices for variables,
and term equality is then just string equality. Let T := {t1 , . . . , tm } be a fixed
enumeration of the set of all symbols and (sub)terms that appear in all for-
mulas from Γ . We define Φ : Γ × {1, . . . , m} → {0, 1} by
                                  (
                                   1 if ti appears in c,
                       Φ(c, i) :=
                                   0 otherwise.
This matrix gives rise to the feature function ϕ : Γ → {0, 1}m which for c ∈ Γ
is the vector ϕc with entries in {0, 1} satisfying
                             ϕci = 1 ⇐⇒ Φ(c, i) = 1.
The expressed features of a formula are denoted by the value of the function
e : Γ → P(T ) that maps c to {ti | Φ(c, i) = 1}.
    Note that our choice of feature characterization is quite arbitrary. We could
try to use only symbols, or only (sub)terms, or some totally different features.
The better the features correspond to the concepts that are relevant when
choosing theorems for solving a particular problem, the more successful the
machine learning of premise selection can be. As with the case of using al-
ternative proofs for training, we just note that finding suitable feature char-
acterizations is a very interesting problem in this area, and that our current
choice seems to perform already quite reasonably in the experiments. For the
particular heuristic justification of using formula (sub)terms, see [36].
    The premise selection problem can be treated as a ranking problem, or
as a classification problem. In the ranking approach, we for a given a conjec-
ture c rank the available premises by their predicted usefulness for an auto-
mated proof of c, and use some number n of premises with the highest rank-
ing (denoted here as advisedP remises(c, n)). In the classification approach,
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods                9


we are looking for each premise p ∈ Γ for a real-valued classifier function
Cp (·) : Γ → R which, given a conjecture c, estimates how useful p is for prov-
ing c. In standard classification, a premise p would then be used if Cp (c) is
above certain threshold. A common approach to ranking is to use classification,
and to combine the real-valued classifiers [21]: the premises for a conjecture c
are ranked by the values of Cp (c), and we choose a certain number of the best
ones. This is the approach that we use in this paper.
    Given a training corpus, machine learning algorithms can automatically
learn classifier functions. The main difference between learning algorithms is
the function space in which they search for the classifiers and the measure they
use to evaluate how good a classifier is. In our prior work on the applications of
machine learning techniques to the premise selection problem [36] we used the
SNoW implementation [9] of a multiclass naive Bayes learning method because
of its efficiency. In this work, we experiment with state-of-the-art kernel-based
learning methods for premise selection. We present both methods and show
the benefits of using kernels.




4.1 A Naive Bayes Classifier


Naive Bayes is a statistical learning method based on Bayes’s theorem about
conditional probabilities9 with a strong (read: naive) independence assump-
tions. In the naive Bayes setting, the value Cp (c) of the classifier function of
a premise p at a conjecture c is the probability that µ(c, p) = 1 given the
expressed features e(c).
     To understand the difference between the naive Bayes and the kernel-based
learning algorithm we need to take a closer look at the naive Bayes classifier.
Let θ denote the statement that µ(c, p) = 1 and for each feature ti ∈ T let
t̄i denote that Φ(c, i) = 1. Furthermore, let e(c) = {s1 , . . . , sl } ⊆ T be the
expressed features of c (with corresponding s̄1 , . . . , s̄l ). We have



  9 In its simplest form, Bayes’s theorem asserts for a probability function P and random

variables X and Y that

                                             P (Y |X)P (X)
                                P (X|Y ) =                 ,
                                                 P (Y )


where P (X|Y ) is understood as the conditional probability of X given Y .
10                                             Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban




                                     P (θ | s̄1 , . . . , s̄l )
       P (θ | s̄1 , . . . , s̄l ) ∝ ln                                                      (1)
                                    P (¬θ | s̄1 , . . . , s̄l )
                                      P (s̄1 , . . . , s̄l | θ)P (θ)
                               = ln                                                         (2)
                                    P (s̄1 , . . . , s̄l | ¬θ)P (¬θ)
                                     P (s̄1 , . . . , s̄l | θ)        P (θ)
                               = ln                             + ln                        (3)
                                    P (s̄1 , . . . , s̄l | ¬θ)       P (¬θ)
                                         l
                                         Y P (s̄i | θ)        P (θ)
                               = ln                     + ln         by independence        (4)
                                   i=1
                                       P (s̄i | ¬θ)          P (¬θ)
                                  m                        
                                 X
                                      c        P (t̄i | θ)           P (θ)
                               =     ϕi ln                    + ln                          (5)
                                 i=1
                                              P (t̄ i | ¬θ)         P (¬θ)
                                                     P (θ)
                               = wT ϕc + ln                                                 (6)
                                                    P (¬θ)

     where                                                             
                                                         P (t̄i | θ)
                                         wi := ln                                           (7)
                                                        P (t̄i ) | ¬θ
Line (6) shows that the naive-Bayes classifier is “essentially” (after the mono-
tonic transformation) a linear function of the features of the conjecture. The
feature weights w are here computed using formula (7).


4.2 Kernel-based Learning

We saw that the naive Bayes algorithm gives rise to a linear classifier. This
leads to several questions: ‘Are there better parameters?’ and ‘Can one get
better performance with non-linear functions?’. Kernel-based learning provides
a framework for investigating such questions. In this subsection we give a
simplified, brief description of kernel-based learning that is tailored to our
present problem; for further information, see [5, 25, 27].

4.2.1 Are there better parameters?

To answer this question we must first define what ‘better’ means. Using the
number of problems solved as measure is not feasible because we cannot prac-
tically run an ATP for every possible parameter combination. Instead, we
measure how good a classifier approximates our training data. We would like
to have that
                         ∀x ∈ Γ : Cp (x) = µ(x, p).
However, this will almost never be the case. To compare how well a classifier
approximates the data, we use loss functions and the notion of expected loss
that they provide, which we now define.
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods      11


Definition 4 (Loss function and Expected Loss) A loss function is any
function l : R × R → R+ .
    Given a loss function l we can then define the expected loss E(·) of a
classifier Cp as                 X
                        E(Cp ) =    l(Cp (x), µ(x, p))
                                    x∈Γ

One might add additional properties such as l(x, x) = 0, but this is not nec-
essary. Typical examples of a loss function l(x, y) are the square loss (y − x)2
or the 0-1 loss defined by I(x = y).
    We can compare two different classifiers via their expected loss. If the
expected loss of classifier Cp is less than the expected loss of a classifier Cq
then Cp is the better classifier. It should be noted that a lower expected loss
on a particular training set (like the mml proofs) need not necessarily lead
to more solved problems by an ATP. One could imagine that the training
set contains proofs that are very different from the way a particular ATP
would proceed most easily. Also, what happens if the classifier is not able to
predict all mml premises, but just a large part of them? These are questions
about alternative proofs, and about the robustness of the ATP and prediction
methods. An experimental answer is provided in Section 6.3.

4.2.2 Nonlinear Classifiers

It seems straightforward that more complex functions would lead to a lower
expected loss and are hence desirable. However, parameter optimization be-
comes tedious once we leave the linear case. Kernels provide a way to use the
machinery of linear optimization on non-linear functions.

Definition 5 (Kernel) A kernel is is a function k : Γ × Γ → R satisfying

                              k(x, y) = hφ(x), φ(y)i

where φ : Γ → F is a mapping from Γ to an inner product space F with inner
product h·, ·i. A kernel can be understood as a similarity measure between two
entities.

Example 1 A simple kernel for our setting is the linear kernel:

                              klin (x, y) := hϕx , ϕy i

with h·, ·i being the normal dot product in Rm . Here, ϕf denotes the features
of a formula f (see definition 3), and the inner product space F is Rm . A
nontrivial example is the Gaussian kernel with parameter σ:
                                   hϕx , ϕx i − 2hϕx , ϕy i + hϕy , ϕy i
                                                                        
            kgauss (x, y) := exp −
                                                   σ2
    We can now define our kernel function space in which we will search for
classification functions.
12                                       Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


Definition 6 (Kernel Function Space) Given a kernel k, we define
              (                                             )
                              X
                    Γ
        Fk := f ∈ R | f (x) =   αv k(x, v), αv ∈ R, kf k < ∞ .
                                         v∈Γ

as our kernel function space, where
                     w              w
                     wX             w   X
                          αv k(x, v)w =   αu αv k(u, v)
                     w              w
                     w
                     w              w
                           v∈Γ                    u,v∈Γ

Essentially, every function in Fk compares the input x with formulas in Γ using
the kernel, and the weights α determine how important each comparison is10 .
    The kernel function space Fk naturally depends on the kernel k. It can
be shown that when we use klin , Fklin consists of linear functions of the mml
features T . In contrast, the Gaussian kernel kgauss gives rise to a very nonlinear
kernel function space.

4.2.3 Putting it all together

Having defined loss functions, kernels and kernel function spaces we can now
define how kernel-based learning algorithms learn classifier functions. Given a
kernel k and a loss function l, recall that we measure how good a classifier Cp
is with the expected loss E(Cp ). With all our definitions it seems reasonable
to define Cp as

                                   Cp := arg min E(f )                                (8)
                                               f ∈Fk
However, this is not what a kernel based learning algorithm does. There are
two reasons for this. First, the minimum might not exist. Second, in partic-
ular when using complex kernel functions, such an approach might lead to
overfitting: Cp might perform very well on our training data, but bad on data
that was not seen before. To handle both problems, a regularization param-
eter λ > 0 is introduced to penalize complex functions (assuming that high
complexity implies a high norm). This regularization parameter allows us to
place a bound on possible solution which together with the fact that Fk is a
Hilbert space ensures the existence of Cp . Hence we define
                              Cp = arg min E(f ) + λkf k2                             (9)
                                       f ∈Fk

     Recall from the definition of Fk that Cp has the form
                                       X
                              Cp (x) =    αv k(x, v),                                (10)
                                            v∈Γ

with αv ∈ R. Hence, for any fixed λ, we only need to compute the weights
αv for all v ∈ Γ in order to find Cp . In section 4.3 we show how to solve this
optimization problem in our setting.
10   A more general approach to kernel spaces is available; see [24].
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods                13


4.2.4 Naive Bayes vs Kernel-based Learning

Kernel-based methods typically outperform the naive Bayes algorithm. There
are several reasons for this. Firstly and most importantly, while naive Bayes is
essentially a linear classifier, kernel based methods can learn non-linear depen-
dencies when an appropriate non-linear (e.g. Gaussian) kernel function is used.
This advantage in expressiveness usually leads to significantly better general-
ization11 performance of the algorithm given properly estimated hyperparam-
eters (e.g., the kernel width for Gaussian functions). Secondly, kernel-based
methods are formulated within the regularization framework that provides
mechanism to control the errors on the training set and the complexity (”ex-
pressiveness”) of the prediction function. Such setting prevents overfitting of
the algorithm and leads to notably better results compared to unregularized
methods. Thirdly, some of the kernel-based methods (depending on the loss
function) can use very efficient procedures for hyperparameter estimation (e.g.
fast leave-one-out cross-validation [22]) and therefore result in a close to opti-
mal model for the classification/regression task. For such reasons kernel-based
methods are among the most successful algorithms applied to various problems
from bioinformatics to information retrieval to computer vision [27]. A general
advantage of naive Bayes over kernel-based algorithms is the computational
efficiency, particularly when taking into account the fact that computing the
kernel matrix is generally quadratic in the number of training data points.
However, recent advances in large scale learning have led to extensions of
various kernel-based methods such as SVMs, with sublinear complexity, prov-
ably fast convergence rate, and the generalization performance that cannot be
matched by most of the methods in the field [26].


4.3 MOR Experimental Setup

For our experiments, we will now define a kernel-based multi-output ranking
(MOR) algorithm that is a relatively straightforward extension of our prefer-
ence learning algorithm presented in [31]. MOR is also based on the regularized
least-squares algorithm presented in [22].
    Let Γ = {x1 , . . . , xn }. Then formula (10) becomes
                                           n
                                           X
                                Cp (x) =         αi k(x, xi )
                                           i=1

Using this and the square-loss l(x, y) = (x − y)2 function, solving equation (9)
is equivalent to finding weights αi that minimize
                                               2                       
             X n    Xn                                 n
                                                       X
      min             αj k(xi , xj ) − µ(xi , p) + λ   αi αj k(xi , xj ) (11)
                                                                        
    α1 ,...,αn
                 i=1   j=1                                      i,j=1

 11 Generalization is the ability of a machine learning algorithm to perform accurately on

new, unseen examples after training on a finite data set.
14                                    Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


    Recall that Cp is the classifier for a single premise. Since we eventually
want to rank all premises, we need to train a classifier for each premise. So
we need to find weights αi,p for each premise p. This does seem to complicate
the problem quite a bit. However, we can use the fact that for each premise
p, Cp depends on the values of k(xi , xj ), where 1 ≤ i, j ≤ n, to speed up the
computation. Instead of learning the classifiers Cp for each premise separately,
we learn all the weights αp,i simultaneously.
    To do this, we first need some definitions. Let

                         A = (αi,p )i,p   (1 ≤ i ≤ n, p ∈ Γ ).

A is the matrix where each column contains the parameters of one premise
classifier. Define the kernel matrix K and the label matrix Y as

                     K := (k(xi , xj ))i,j (1 ≤ i, j ≤ n)
                     Y := (µ(xi , p))i,p (1 ≤ i ≤ n, p ∈ Γ ).

We can now rewrite (11) in matrix notation to state the problem for all
premises:
             arg min tr (Y − KA)T (Y − KA) + λAT KA
                                                       
                                                                  (12)
                     A

where tr(A) denotes the trace of the matrix A. Taking the derivative with
respect to A leads to:

                      ∂
                                                        
                     ∂A tr   (Y − KA)T (Y − KA) + λAT KA
                 =             −2K(Y − KA) + 2λKA
                 =            −2KY + (2KK + 2λK)A

To find the minimum, we set the derivative to zero and solve with respect to
A. This leads to:

                              A = (KK + λK)−1 KY                                  (13)
                                              −1
                                 = (K + λI)        Y                              (14)

    In the experiments, we use the Gaussian kernel kgauss we defined in Exam-
ple 1. Ergo, if we fix the regularization parameter λ and the kernel parameter
σ we can find the optimal weights through simple matrix computations. Thus,
to fully determine the classifiers, it remains to find good values for the param-
eters λ and σ. This is done, as is common with such parameter optimization
for kernel methods, by simple (logarithmically scaled) grid search and cross-
validation on the training data using a 70/30 split.
      Premise Selection for Mathematics by Corpus Analysis and Kernel Methods      15


      5 Data: The MPTP2078 Benchmark

      The effects of using the minimized dependency data (both for direct re-proving
      and for training premise selection), and the effect of using our kernel-based
      MOR algorithm are evaluated on a newly created large-theory benchmark12
      of 2078 related mml problems, which extends the older and smaller MPTP
      Challenge benchmark.
          The original MPTP Challenge benchmark was created in 2006, with the
      purpose of supporting the development of ARLT (automated reasoning for
      large theories) techniques. It contains 252 related problems, leading to the
      Mizar proof of one implication of the Bolzano-Weierstrass theorem. The chal-
      lenge has two divisions: chainy (harder) and bushy (easier). The motivation
      behind them is given below when we describe their analogs in the MPTP2078
      benchmark.
          Both the ARLT techniques and the computing power (particularly multi-
      core technology) have developed since 2006. Appropriately, we define a larger
      benchmark with a larger numbers of problems and premises, and making use
      of the more precise dependency knowledge. The larger number of problems
      together with their dependencies more faithfully mirror the setting that math-
      ematicians are facing: typically, they know a number of related theorems and
      their proofs when solving a new problem.
          The new MPTP2078 benchmark is created as follows: The 33 Mizar articles
      from which problems were previously selected for constructing the MPTP
      Challenge are used. We however use a new version of Mizar and mml allowing
      the precise dependency analysis, and use all problems from these articles. This
      yields 2078 problems. As with the MPTP Challenge benchmark, we create two
      groups (divisions) of problems.
Chainy: Versions of the 2078 problems containing all previous mml contents as
        premises. This means that the conjecture is attacked with “all existing
        knowledge”, without any premise selection. This is a common use case for
        proving new conjectures fully automatically, see also Section 6.2. In the
        MPTP Challenge, the name chainy has been introduced for this division,
        because the problems and dependencies are ordered into a chronological
        chain, emulating the growth of the library.
 Bushy: Versions of the 2078 problems with premises pruned using the new fine-
        grained dependency information. This use-case has been introduced in
        proof assistants by Harrison’s MESON TACTIC [12], which takes an explicit
        list of premises from the large library selected by a knowledgeable user,
        and attempts to prove the conjecture just from these premises. We are
        interested in how powerful ATPs can get on mml with such precise advice.
      To evaluate the benefit of having precise minimal dependencies, we addition-
      ally also produce in this work versions of the 2078 problems with premises
      pruned by the old heuristic dependency-pruning method used for construct-
      ing re-proving problems by the MPTP system. The MPTP heuristic proceeds
       12   http://wiki.mizar.org/twiki/bin/view/Mizar/MpTP2078
16                                  Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


by taking all explicit premises contained in the original human-written Mizar
proof. To get all the premises used by Mizar implicitly, the heuristic watches
the problem’s set of symbols, and adds the implicitly used formulas (typi-
cally typing formulas about the problem’s symbols) in a fixpoint manner. The
heuristic attempts hard to guarantee completeness, however, minimality is not
achievable with such simple approach.
    All three datasets contain the same conjectures. They only differ in the
number of redundant axioms. Note that the problems in the second and third
dataset are considerably smaller than the unpruned problems. The average
number of premises is 1976.5 for the unpruned (chainy) problems, 74 for the
heuristically-pruned problems (bushy-old) and 31.5 for the problems pruned
using fine-grained dependencies (bushy). Table 2 summarizes the datasets.


Table 2 Average Number of Premises in the three Datasets

          Dataset      Premises used             Avg. number of premises

          Chainy       All previous                               1976.5
          Bushy-Old    Heuristic dependencies                         74
          Bushy        Minimized dependencies                       31.5




6 Experiments and Results

We use Vampire 0.6 [20] as the ATP system for all experiments conducted here.
Adding other ATP systems is useful (see, e.g., [33] for recent evaluation), and
there are metasystems like MaLARea which attempt to exploit the joint power
of different systems in an organized way. However, the focus of this work is on
premise selection, which has been shown to have similar effect across the main
state-of-the-art ATP systems. Another reason for using the recent Vampire is
that in [33], Vampire with the SInE preprocessor was sufficiently tested and
tuned on the mml data, providing a good baseline for comparing learning-
based premise-selection methods with robust state-of-the-art methods that can
run on any isolated large problem without any learning. All measurements are
done on an Intel Xeon E5520 2.27GHz server with 8GB RAM and 8MB CPU
cache. Each problem is always assigned one CPU.
    In Section 6.1 we evaluate the ATP performance when fine-grained depen-
dencies (bushy problems) are used by comparing it to the ATP performance on
the old MPTP heuristic pruning (bushy-old problems), and to the ATP perfor-
mance on the large (chainy) versions of the MPTP2078 problems. These results
show that there is a lot to gain by constructing good algorithms for premise
selection. In Section 6.2 SNoW’s naive Bayes and the MOR machine learning al-
gorithms are incrementally trained on the fine-grained mml dependency data,
and their precision in predicting the mml premises on new problems are com-
pared. This standard machine-learning comparison is then in Section 6.3 com-
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods                   17


pleted by running Vampire on the premises predicted by the MOR and SNoW
algorithms. This provides information about the overall theorem-proving per-
formance of the whole dependency-minimization/learning/ATP stack. This
performance is compared to the performance of Vampire/SInE.



6.1 Using the Fine-Grained Dependency Analysis for Re-proving

The first experiment evaluates the effect of fine-grained dependencies on re-
proving Mizar theorems automatically. The results of Vampire/SInE run with
10s time limit13 on the datasets defined above are shown in Table 3.


Table 3 Performance of Vampire (10s time limit) on 2078 MPTP2078 benchmark with
different axiom pruning.

            Pruning                   Solved problems     Solved as percentage

            Chainy                                 548                     26.4
            Chainy (Vampire -d1)                   556                     26.8
            Bushy-old                             1023                     49.2
            Bushy                                 1105                     53.2



    Vampire (run in the unmodified automated CASC mode) solves 548 of
the unpruned problems. If we use the -d1 parameter14 , Vampire solves 556
problems. Things change a lot with external premise pruning. Vampire solves
1023 of the 2078 problems when the old MPTP heuristic pruning (bushy-old)
is applied. Using the pruning based on the new fine-grained analysis Vampire
solves 1105 problems, which is an 8% improvement over the heuristic pruning
in the number of problems solved. Since the heuristic pruning becomes more
and more inaccurate as the mml grows (the ratio of MPTP Deps. to Fine Deps.
in Table 1 has a growing trend from top to bottom), we can conjecture that this
improvement will be even more significant when considering the whole mml.
Also note that these numbers point to the significant improvement potential
that can be gained by good premise selection: the performance on the pruned
dataset is doubled in comparison to the unpruned dataset. Again, this ratio
grows as mml grows, and the number of premises approaches 100.000.15
 13 There are several reasons why we use low time limits. First, Vampire performs reasonably

with them in [33]. Second, low time limits are useful when conducting large-scale experiments
and combining different strategies. Third, in typical ITP proof-advice scenarios [34], the
preferable query response time is in (tens of) seconds. Fourth, 10 seconds in 2011 is much
more than it was fifteen years ago, when the CASC competition started.
 14 The -d parameter limits the depth of recursion for the SInE algorithm. In [33] running

Vampire with the -d1 pruning parameter resulted in significant performance improvement
on large Mizar problems.
 15 In the evaluation done in [33] on the whole mml with Vampire/SInE, this ratio is 39%

to 14%.
18                                     Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


6.2 Combining Fine-Grained Dependencies with Learning

For the next experiment, we emulate the growth of the library (limited to the
2078 problems), by considering all previous theorems and definitions when a
new conjecture is attempted. This is a natural “ATP advice over the whole
library” scenario, in which the ATP problems however become very large,
containing thousands of the previously proved formulas. Premise selection can
therefore help significantly.
    We use the fine-grained mml dependencies extracted from previous proofs16
to train the premise-selection algorithms, use their advice on the new prob-
lems, and compare the recall (and also the ATP performance in the next
subsection). For each problem, the learning algorithms are allowed to learn on
the dependencies of all previous problems, which corresponds to the situation
in general mathematics when mathematicians not only know many previous
theorems, but also re-use previous problem solving knowledge. This approach
requires us to do 2078 training steps as the problems and their proofs are
added to the library and the dataset grows. We compare the MOR algorithm
with SNoW’s naive Bayes.
    Figure 1 shows the average recall of SNoW and MOR on this dataset.
The rankings obtained from the algorithms are compared with the actual
premises used in the mml proof, by computing the size (ratio) of the overlap
for the increasing top segments of the ranked predicted premises (the size of
the segment is the x axis in Figure 1). Formally, the recall recall(c, n) for one
conjecture c when n premises are advised is defined as:

                           |usedP remises(c) ∩ advisedP remises(c, n)|
          recall(c, n) =
                                       |usedP remises(c)|

It can be seen that the MOR algorithm performs considerably better than
SNoW. E.g., on average 88% of the used premises are within the 50 high-
est MOR-ranked premises, whereas when we consider the SNoW ranking only
around 80% of the used premises are with the 50 highest ranked premises.
    Note that this kind of comparison is the standard endpoint in machine
learning applications like keyword-based document retrieval, consumer choice
prediction, etc. However, in a semantic domain like ours, we can go further,
and see how this improved prediction performance helps the theorem proving
process. This is also interesting to see, because having for example only 90%
coverage of the original mml premises could be insufficient for constructing an
ATP proof, unless the ATP can invent alternative (sub-)proofs.17 This final
evaluation is done in the next section.
 16 We do not evaluate the performance of learning on the approximate bushy-old depen-

dencies here and in the next subsection. Table 1 and Section 6.1 already sufficiently show
that these data are less precise than the fine-grained mml dependencies.
 17 See [3] for an initial exploration of the phenomenon of alternative ATP proofs for mml

theorems.
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods             19




Fig. 1 Comparison of the SNoW and MOR average recall of premises used in the Mizar
proofs. The x-axis shows the number of premises asked from SNoW and MOR, and the y-axis
shows their relative overlap with the premises used in the original Mizar proof.




6.3 Combining It All: ATP Supported by Learning from Fine Dependencies

In the last experiment, we finally chain the whole ITP/Learning/ATP stack
together, and evaluate how the influence of the improved premise selection
reflects on performance of automated theorem proving on new large-theory
conjectures. Both the naive Bayes (SNoW) and the new MOR learning algo-
rithms are evaluated.
    Figure 2 shows the numbers of problems solved by Vampire using different
numbers of the top premises predicted by SNoW and MOR, and a 5 seconds
time limit. The maximum number of problems solved with MOR is 729 with the
top 60 advised premises. SNoW’s maximum is 652 with the top 70 premises.
The corresponding numbers for a 10 second time limit are 795 solved problems
for MOR-60, and 722 for SNoW-70. Table 4 compares these data with the
overall performance of Vampire with a 10 second time limit run on problems
with pruning done by SInE. The SNoW-60 resp. MOR-70 runs give a 32% resp.
45% improvement over the 548 problems Vampire solves in auto-mode, and a
30% resp. 43% improvement over the 556 problems solved by Vampire using
the -d1 option.
20                                    Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban




Fig. 2 Comparison of the number of solved problems by SNoW and MOR. The x-axis shows
the number of premises given to the Vampire, and the y-axis shows the number of problems
solved within 5 seconds. The number of problems solved by Vampire/SInE in 10 seconds is
given as a baseline.



Table 4 Comparison of Vampire (10s time limit) performance on MPTP2078 with different
premise selections.

             System                 Solved Problems    Gain over Vampire

             Vampire/SInE                        548                 0%
             Vampire/SInE (-d1)                  556                1.5%
             SNoW-70                             722               31.8%
             MOR-60                              795               45.1%




    Table 5 additionally compares the performance of Vampire/SInE with the
performance of SNoW and MOR when computed for each of them as a union
of the two 5s runs with the largest joint coverage. Those are obtained by using
the top 40 advised premises and the top 180 advised premises for SNoW, and
the top 40 and top 100 advised premises for MOR. These SNoW resp. MOR
combined runs give a 44% resp. 50% improvement over the 548 problems
Vampire solves in auto-mode, and a 42% resp. 48% improvement over the 556
problems solved by Vampire using the -d1 option.
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods            21


    Note that Vampire/SInE does strategy scheduling internally, and with dif-
ferent SInE parameters. Thus combining two different premise selection strate-
gies by us is perfectly comparable to the way Vampire’s automated mode is
constructed and used. Also note that combining the two different ways in
which unadvised Vampire/SInE was run is not productive: the union of both
unadvised runs is just 559 problems, which is only 3 more solved problems
(generally in 20s) than with running Vampire/SInE with -d1 for ten seconds.


Table 5 10s performance of the two strategies with the largest joint coverage for SNoW
and MOR.

             System                Solved Problems    Gain over Vampire

             Vampire/SInE                      548                  0%
             Vampire/SInE (-d1)                556                 1.5%
             SNoW-40/180                       788                43.7%
             MOR-40/100                        824                50.4%



    Finally, Figure 3 and Figure 4 compare the cumulative and average per-
formance of the algorithms (combined with ATPs) at different points of the
MPTP2078 benchmark, using the chronological ordering of the MPTP2078
problems. The average available number of premises for the theorems ordered
chronologically grows linearly (the earlier theorems and definitions become eli-
gible premises for the later ones), making the later problems harder on average.
Figure 3 shows the performance computed on initial segments of problems us-
ing step value of 50. The last value (for 2050) corresponds to the performance
of the algorithms on the whole MPTP2078 (0.38 for MOR-60), while for ex-
ample the value for 1000 (0.60 for MOR-60) shows the performance of the
algorithms on the first 1000 MPTP2078 problems. Figure 4 compares the av-
erage performance of the algorithms when the problems are divided into four
successive segments of equal size. Note that even with the precise use of the
mml premises the problems do not have uniform difficulty across the bench-
mark, and on average, even the bushy versions of the later problems get harder.
To visualize this, we also add the values for Vampire-bushy to the comparison.
    Except from small deviations, the ratio of solved problems decreases for all
the algorithms. Vampire/MOR-60 is able to keep up with Vampire-bushy in the
range of the initial 800 problems, and after that the human selection increas-
ingly outperforms all the algorithms. Making this gap as small as possible is
an obvious challenge on the path to strong automated reasoning in general
mathematics.


7 Conclusion and Future Work

The performance of automated theorem proving over real-world mathematics
has been significantly improved by using detailed minimized formally-assisted
22                                    Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


      1
                                                                 "MOR-60"
                                                               "SNoW-70"
     0.9                                                         "SInE-d1"
                                                           "Vampire-bushy"
     0.8

     0.7

     0.6

     0.5

     0.4

     0.3

     0.2
           0            500              1000              1500              2000


Fig. 3 Performance of the algorithms on initial segments of MPTP2078.




Fig. 4 Average performance of the algorithms on four successive equally sized segments of
MPTP2078.
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods           23


analysis of a large corpus of theorems and proofs, and by using improved pre-
diction algorithms. In particular, it was demonstrated that premise selection
based on learning from exact previous proof dependencies improves the ATP
performance in large mathematical theories by about 44% when using off-the-
shelf learning methods like naive Bayes in comparison with state-of-the-art
general premise-selection heuristics like SInE. It was shown that this can be
further improved to about 50% when employing state-of-the-art kernel-based
learning methods.
    Automated reasoning in large mathematical libraries is becoming a com-
plex AI field, allowing interplay of very different AI techniques. Manual tuning
of strategies and heuristics does not scale to large complicated domains, and
data-driven approaches are becoming very useful in handling such domains.
At the same time, existing strong learning methods are typically developed on
imprecise domains, where feedback loops between prediction and automated
verified confirmation as done for example in MaLARea are not possible. The
stronger such AI systems become, the closer we get to formally assisted mathe-
matics, both in its “forward” and “reverse” form. And this is obviously another
positive feedback loop that we explore here: the larger the body of formally
expressed and verified ideas, the smarter the AI systems that learn from them.
    The work started here can be improved in many possible ways. While we
have achieved 50% ATP improvement on large problems by better premise se-
lection resulting in 824 problems proved within 10 seconds, we know (from 6.1)
that with a better premise selection it is possible to prove at least 1105 prob-
lems. Thus, there is still a great opportunity for improved premise selection
algorithms. Our dependency analysis can be finer and faster, and combined
with ATP and machine learning systems, can be the basis for a research tool
for experimental formal (reverse) mathematics. An interesting AI problem that
is becoming more and more relevant as the ATP methods for mathematics are
getting stronger, is translation of the (typically resolution-based) ATP proofs
into human-understandable [10, 23] formats used by mathematicians. We be-
lieve that machine learning from large human-proof corpora like mml is likely
to be useful for this task, in a similar way to how it is useful for finding relevant
premises.
    The MOR algorithm has a number of parameterizations that we have fixed
for the experiments done here. Further experiments with different loss func-
tions could yield better results. One of the most interesting parameterizations
is the right choice of features for the formal mathematical domain. So far, we
have been using only the symbols and terms occurring in formulas as their fea-
ture characterizations, but other features are possible, and very likely used by
mathematicians. In particular, for ad hoc problem collections like the TPTP li-
brary, where symbols are used inconsistently across different problems, formula
features that abstract from particular symbols will likely be needed. Also, the
output of the learning algorithms does not have to be limited to the ranking of
premises. In general, all kinds of relevant problem-solving parameterizations
can be learned, and an attractive candidate for such treatment is the large set
of ATP strategies and options parameterizing the proof search. With such ex-
24                                      Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


periments, a large number of alternative ATP proofs are likely to be obtained,
and an interesting task is to productively learn from such a combination of
alternative (both human and machine) proofs. Premise selection is only one
instance of the ubiquitous proof guidance problem, and recent prototypes like
the MaLeCoP system [37] indicate that guidance obtained by machine learning
can considerably help also inside automated theorem provers.
     Finally, we hope that this work and the performance numbers obtained
will provide a valuable feedback to the CADE competition organizers: Pre-
vious proofs and theory developments in general are an important part of
real-world mathematics and theorem proving. At present, the LTB division of
CASC does not recognize proofs in the way that we are recognizing them here.
Organizing large-theory competitions that separate theorems from their proofs
is like organizing web search competitions that separate web pages from their
link structure [8]. We believe that re-introducing a large-theory competition
that does provide both a large number of theorems and a large number of
proofs will cover this important research direction, and most of all, properly
evaluate techniques that significantly improve the ATP end-user experience.


8 Acknowledgment

We would like to thank the anonymous JAR referees for a number of questions,
comments, and insights that helped to significantly improve the final version
of this paper.


References

 1. Alama, J.: Formal Proofs and Refutations. Ph.D. thesis, Stanford University (2009)
 2. Alama, J., Brink, K., Mamane, L., Urban, J.: Large formal wikis: Issues and solutions.
    In: Davenport, J., Farmer, W., Urban, J., Rabe, F. (eds.) Intelligent Computer Math-
    ematics, Lecture Notes in Computer Science, vol. 6824, pp. 133–148. Springer Berlin /
    Heidelberg (2011)
 3. Alama, J., Kühlwein, D., Urban, J.: Automated and human proofs in general mathe-
    matics: An initial comparison. In: Bjørner, N., Voronkov, A. (eds.) LPAR. Lecture Notes
    in Computer Science, vol. 7180, pp. 37–45. Springer (2012)
 4. Alama, J., Mamane, L., Urban, J.: Dependencies in formal mathematics: Applications
    and extraction for Coq and Mizar (2011), arxiv.org pre-print abs/1109.3687
 5. Aronszajn, N.: Theory of reproducing kernels. Transactions of the American Mathemat-
    ical Society 68 (1950)
 6. Bertot, Y., Castéran, P.: Interactive Theorem Proving and Program Development.
    Coq’Art: The Calculus of Inductive Constructions. Texts in Theoretical Computer Sci-
    ence, Springer Verlag (2004)
 7. Blanchette, J.C., Bulwahn, L., Nipkow, T.: Automatic proof and disproof in Is-
    abelle/HOL. In: Tinelli, C., Sofronie-Stokkermans, V. (eds.) FroCos. Lecture Notes in
    Computer Science, vol. 6989, pp. 12–27. Springer (2011)
 8. Brin, S., Page, L.: The anatomy of a large-scale hypertextual web search engine. Com-
    puter Networks 30(1-7), 107–117 (1998)
 9. Carlson, A., Cumby, C., Rizzolo, N., Rosen, J., Roth, D.: SNoW user manual (1999),
    http://l2r.cs.uiuc.edu/~cogcomp/software/snow-userguide.pdf
10. Davis, M.: Obvious logical inferences. In: Hayes, P.J. (ed.) IJCAI. pp. 530–531. William
    Kaufmann (1981)
Premise Selection for Mathematics by Corpus Analysis and Kernel Methods                        25


11. Grabowski, A., Kornilowicz, A., Naumowicz, A.: Mizar in a nutshell. Journal of For-
    malized Reasoning 3(2), 153–245 (2010)
12. Harrison, J.: Optimizing proof search in model elimination. In: McRobbie, M.A., Slaney,
    J.K. (eds.) CADE. Lecture Notes in Computer Science, vol. 1104, pp. 313–327. Springer
    (1996)
13. Harrison, J., Slind, K., Arthan, R.: HOL. In: Wiedijk, F. (ed.) The Seventeen Provers
    of the World. Lecture Notes in Computer Science, vol. 3600, pp. 11–19. Springer (2006)
14. Hoder, K., Voronkov, A.: Sine qua non for large theory reasoning. In: Bjørner, N.,
    Sofronie-Stokkermans, V. (eds.) Automated Deduction – CADE-23, Lecture Notes in
    Computer Science, vol. 6803, pp. 299–314. Springer Berlin / Heidelberg (2011)
15. Matuszewski, R., Rudnicki, P.: Mizar: the first 30 years. Mechanized Mathematics and
    Its Applications 4, 3–24 (2005)
16. Meng, J., Paulson, L.C.: Translating higher-order clauses to first-order clauses. J. Au-
    tom. Reasoning 40(1), 35–60 (2008)
17. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL - A Proof Assistant for Higher-
    Order Logic, Lecture Notes in Computer Science, vol. 2283. Springer (2002)
18. Paulson, L.C., Susanto, K.W.: Source-level proof reconstruction for interactive theo-
    rem proving. In: Schneider, K., Brandt, J. (eds.) TPHOLs. Lecture Notes in Computer
    Science, vol. 4732, pp. 232–245. Springer (2007)
19. Pease, A., Sutcliffe, G.: First order reasoning on a large ontology. In: Sutcliffe, G., Urban,
    J., Schulz, S. (eds.) ESARLT. CEUR Workshop Proceedings, vol. 257. CEUR-WS.org
    (2007)
20. Riazanov, A., Voronkov, A.: The design and implementation of VAMPIRE. AI Commun.
    15(2-3), 91–110 (2002)
21. Richard, M.D., Lippmann, R.P.: Neural Network Classifiers Estimate Bayesian a pos-
    teriori Probabilities. Neural Computation 3(4), 461–483 (2010)
22. Rifkin, R., Yeo, G., Poggio, T., Rifkin, R., Yeo, G., Poggio, T.: Regularized Least-
    Squares Classification. In: Suykens, J., Horvath, G., Basu, S., Micchelli, C., Vandewalle,
    J. (eds.) Advances in Learning Theory: Methods, Model and Applications NATO Science
    Series III: Computer and Systems Sciences, vol. 190, pp. 131–154. IOS Press (2003)
23. Rudnicki, P.: Obvious inferences. J. Autom. Reasoning 3(4), 383–393 (1987)
24. Schoelkopf, B., Herbrich, R., Williamson, R., Smola, A.J.: A Generalized Represen-
    ter Theorem. In: Helmbold, D., Williamson, R. (eds.) Proceedings of the 14th Annual
    Conference on Computational Learning Theory. pp. 416–426. Berlin, Germany (2001)
25. Scholkopf, B., Smola, A.J.: Learning with Kernels: Support Vector Machines, Regular-
    ization, Optimization, and Beyond. MIT Press, Cambridge, MA, USA (2001)
26. Shalev-Shwartz, S., Singer, Y., Srebro, N., Cotter, A.: Pegasos: primal estimated sub-
    gradient solver for SVM. Math. Program. 127(1), 3–30 (2011)
27. Shawe-Taylor, J., Cristianini, N.: Kernel Methods for Pattern Analysis. Cambridge Uni-
    versity Press, New York, NY, USA (2004)
28. Simpson, S.G.: Subsystems of Second Order Arithmetic. Perspectives in Mathematical
    Logic, Springer, 2 edn. (2009)
29. Solovay, R.: AC and strongly inaccessible cardinals. Available on the Foundations of
    Mathematics archives at http://www.cs.nyu.edu/pipermail/fom/2008-March/012783.
    html (March 29 2008)
30. Tarski, A.: On well-ordered subsets of any set. Fundamenta Mathematicae 32, 176–183
    (1939)
31. Tsivtsivadze, E., Pahikkala, T., Boberg, J., Salakoski, T., Heskes, T.: Co-regularized
    least-squares for label ranking. In: Hüllermeier, E., Fürnkranz, J. (eds.) Chapter in
    Preference Learning Book). pp. 107–123 (2010)
32. Urban, J.: MPTP 0.2: Design, implementation, and initial experiments. J. Autom. Rea-
    soning 37(1-2), 21–43 (2006)
33. Urban, J., Hoder, K., Voronkov, A.: Evaluation of automated theorem proving on the
    Mizar mathematical library. In: Fukuda, K., van der Hoeven, J., Joswig, M., Takayama,
    N. (eds.) ICMS. Lecture Notes in Computer Science, vol. 6327, pp. 155–166. Springer
    (2010)
34. Urban, J., Rudnicki, P., Sutcliffe, G.: ATP and presentation service for Mizar formal-
    izations. CoRR abs/1109.0616 (2011)
26                                      Alama, Heskes, Kühlwein, Tsivtsivadze, and Urban


35. Urban, J., Sutcliffe, G.: Automated reasoning and presentation support for formalizing
    mathematics in Mizar. In: Autexier, S., Calmet, J., Delahaye, D., Ion, P.D.F., Rideau, L.,
    Rioboo, R., Sexton, A.P. (eds.) AISC/MKM/Calculemus. Lecture Notes in Computer
    Science, vol. 6167, pp. 132–146. Springer (2010)
36. Urban, J., Sutcliffe, G., Pudlák, P., Vyskocil, J.: MaLARea SG1–machine learner for au-
    tomated reasoning with semantic guidance. In: Armando, A., Baumgartner, P., Dowek,
    G. (eds.) IJCAR. Lecture Notes in Computer Science, vol. 5195, pp. 441–456. Springer
    (2008)
37. Urban, J., Vyskocil, J., Stepánek, P.: MaLeCoP: Machine learning connection prover.
    In: Brünnler, K., Metcalfe, G. (eds.) TABLEAUX. Lecture Notes in Computer Science,
    vol. 6793, pp. 263–277. Springer (2011)
