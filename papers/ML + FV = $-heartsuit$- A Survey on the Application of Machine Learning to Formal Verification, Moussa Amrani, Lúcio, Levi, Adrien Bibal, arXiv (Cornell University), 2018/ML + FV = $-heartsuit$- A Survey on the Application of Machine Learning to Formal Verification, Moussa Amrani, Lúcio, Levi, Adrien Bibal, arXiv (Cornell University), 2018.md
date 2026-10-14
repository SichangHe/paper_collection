                                                                    ML + FV = ♥?
                                              A Survey on the Application of Machine Learning to Formal
                                                                     Verification
                                                       Moussa Amrani                                     Levi Lúcio                                Adrien Bibal
                                              University of Namur, Faculty of                          fortiss GmbH                      University of Namur, Faculty of
                                             Computer Science, PReCiSE / NaDI                        Guerickestraße 25                  Computer Science, PReCiSE / NaDI
                                                  Rue Grangagnage, 21                            München, Germany 80805                     Rue Grangagnage, 21
                                                  Namur, Belgium 5000                                lucio@fortiss.org                       Namur, Belgium 5000
                                               Moussa.Amrani@unamur.be                                                                     Adrien.Bibal@unamur.be
arXiv:1806.03600v2 [cs.SE] 12 Jun 2018




                                         ABSTRACT                                                                Fv are necessarily disparate, Fv newcomers and practitioners have
                                         Formal Verification (Fv) and Machine Learning (Ml) can seem in-         currently no pointers to introduce them to the topic.
                                         compatible due to their opposite mathematical foundations and              This paper is an attempt to provide a comprehensive survey of
                                         their use in real-life problems: Fv mostly relies on discrete mathe-    the various ways Ml contributes to enhance Fv tools’ efficiency.
                                         matics and aims at ensuring correctness; Ml often relies on proba-      To achieve this goal, we propose to catalog the challenges Fv faces
                                         bilistic models and consists of learning patterns from training data.   that may be handled through Ml techniques, called themes, and
                                         In this paper, we postulate that they are complementary in practice,    characterize each theme with a corresponding Ml task, i.e. Ml
                                         and explore how Ml helps Fv in its classical approaches: static         problem categories (such as classification, regression, clustering,
                                         analysis, model-checking, theorem-proving, and Sat solving. We          etc.), pointing for each theme to the relevant literature. To the best
                                         draw a landscape of the current practice and catalog some of the        of our knowledge, no contributions in the literature currently exist
                                         most prominent uses of Ml inside Fv tools, thus offering a new          that spans all the spectrum of the main Fv approaches (namely,
                                         perspective on Fv techniques that can help researchers and practi-      Model-Checking, Theorem-Proving, Static Analysis, and to a certain
                                         tioners to better locate the possible synergies. We discuss lessons     extend, Sat-solving). By covering various approaches, we aim at
                                         learned from our work, point to possible improvements and offer         extracting valuable, transversal lessons about general trends of Ml
                                         visions for the future of the domain in the light of the science of     usage within Fv, as well as provide a high-level snapshot of the
                                         software and systems modeling.                                          current practice in each Fv approach.
                                                                                                                    The main contributions of this paper are the following:
                                         CCS CONCEPTS
                                                                                                                       • We provide a catalog of themes for each Fv approach, pre-
                                         •General and reference → Validation; Verification; •Computing                   sented in a systematic way: each theme details the cor-
                                         methodologies → Machine learning;                                               responding Ml task, and provides a commented list of
                                                                                                                         relevant contributions. An overview is available in Table 2.
                                         KEYWORDS                                                                      • We analyze the literature to extract general observations
                                         Formal Verification, Machine Learning                                           on the use of Ml inside Fv tools, and to identify some
                                                                                                                         trends and lessons, with an insight on what the future may
                                                                                                                         be.
                                                                                                                       • We build a comprehensive and searchable repository of
                                         1   INTRODUCTION                                                                contributions found in the literature that can help the Fv
                                         Formal Verification (Fv) aims at guaranteeing correctness properties            community build a multi-level understanding of Ml usage
                                         of software and hardware systems. In that sense, a system is safe               in Fv tools. The repository is sorted according to various
                                         with respect to the checked properties. Machine Learning (Ml)                   criteria (publication date, themes, and Ml tasks).
                                         aims at learning patterns from training data for various purposes;
                                         the derived model generalizes from the data it was trained on. Both        This paper is organized as follows. Section 3 describes the paper
                                         Fv and Ml are grounded on solid mathematical foundations: the           selection protocol, formulates research questions and discusses
                                         former uses mostly discrete mathematics, fixpoints and abstractions     threats to validity. Section 4 analyses in detail the contributions we
                                         to specify (concrete/abstract) semantics, properties of interest and    retrieved. Section 5 discusses how our findings answer the research
                                         the checking process itself; the latter uses in general continuous      questions before concluding in Section 7.
                                         mathematics and/or probability theory to infer models. While they
                                         seem at first sight not suitable for each other, their relative and
                                         apparent opposition provides, just like in real life, the spark for     2     BACKGROUND
                                         a strong love story. This paper focuses on one part of the love         This section provides a high-level introduction to both Formal Veri-
                                         story: what Ml brings to Fv to make it flourish, become more            fication (Fv) and Machine Learning (Ml), as the key actors in our
                                         efficient and accurate, and face real-life challenges? While we are     survey. For further details, reference pointers are provided in each
                                         aware that the topic is broad and the ways in which Ml can help         section.
2.1    Formal Verification (FV)                                                   In supervised learning, the target is known a priori and the
In its most classical form, Fv attempts to answer the following               learner minimizes some type of distance between the target and
question: does a behavioral model, which reflects the evolution               its prediction. On the contrary, in unsupervised learning, no target
of the various variables of a system, satisfy a specification of a            is given a priori: the Ml algorithm tries to find recurring patterns
program, which consists in properties of interest characterizing              inside the data and the final quality judgment is ultimately human.
error/undesired states.                                                       The well-known clustering Ml task consists for instance in grouping
    Computing the system’s so-called concrete semantics explicitly            elements in the dataset, but whether finding three clusters is better
is in the general case impossible, since it is infinite even for very         than finding five depends on the domain problem and cannot be
simple programs. Rather, Fv proceeds by abstraction, or overap-               answered fully automatically outside the context of the algorithm’s
proximation [28]: demonstrating that an abstraction never reaches             use. Another task of this kind, the item set finding task, consists in
forbidden values proves the fact that the actual executions are cor-          finding items that may often co-occur together (e.g., buying butter
rect. However, false alarms (or false positives) may arise, i.e. errors       and jam may often occur together with buying bread).
due to an abstraction that is too coarse and that does not corre-                 Finally, the third considered category is reinforcement learning,
spond to any actual system execution. Aside from extracting the               which “is learning what to do — how to map situations to actions
behavioral model itself, one of the main difficulties in Fv is building       — so as to maximize a numerical reward signal. The learner is not
abstractions that are sufficiently precise to avoid false alarms, but         told which actions to take, as in many forms of machine learning,
sufficiently simple to be automatically computed. This abstraction            but instead must discover which actions yield the most reward by
can take on many forms, leading to a variety of Fv approaches.                trying them” [92]. For instance, an AI agent taking the role of a
In this paper we will concentrate on Static Analysis (Sa), Model              human player in a computer game can learn how to complete a
Checking (Mc) and Theorem Proving (Tp). We also consider Sat                  level by finding the action patterns leading to a minimization of
solving (Sat): many Fv problems can be reduced to the satisfaction            penalties. These penalties may be provided every time the agent
of Sat formulæ [77].                                                          dies while trying to complete a given level of the game.
                                                                                  Once an Ml task is determined, and features of the instances
                                                                              under study are identified, an Ml specialist should select the type
2.2    Machine Learning (ML)                                                  of Ml model that would approximate the patterns to be found
Humans learn from experience. Car drivers learn by following                  in the data. Examples of such Ml models are decision trees, or
instructions from driving school monitors, parents or friends, but            the well-known neural networks [67]. Choosing an appropriate
also by identifying good behaviors in other drivers. Players learn            model requires expertise and fine-tuning (in particular, tuning of
chess or basket-ball by studying “good” and “bad” games, practic-             the so-called hyper-parameters). As a consequence, failing to obtain
ing the fundamental moves again and again, and by identifying                 meaningful results for a given Ml task may mean that the model is
best practices that ensure victory. Humans seem also naturally                inappropriate, or badly parameterized. We consider that specific
designed to extract patterns and features in what surrounds them.             considerations on Ml models are beyond the scope of this paper.
For instance, medical doctors provide diagnostics based on many
anatomic and physiological variables such as body temperature or
blood pressure – formally called features in Ml– available in patient         3    SEARCH PROTOCOL
data, trying to minimize death risk. Ml can be seen as a systematic
way of solving a problem by optimizing some objective function                   For realizing this survey, we used a methodology inspired by
using training data [67].                                                     Kitchenham [52]. Our protocol relies on two observations. First,
   In this paper, we only consider three task categories in Ml: super-        the authors involved in this work have different, complementary
vised and unsupervised learning, as well as reinforcement learning.           backgrounds (the two first authors work on Software Engineering
Other categories (like semi-supervised learning), as well as many             and Fv, while the latter is specialized in Ml). Second, no authors had
other Ml tasks in supervised/unsupervised learning exist, but the             prior knowledge of what could exist in the literature: we were quite
ones presented here cover all the themes we encountered while                 certain to retrieve only a few papers, partly due to the opposition
analyzing contributions of Ml in Fv approaches.                               mentioned in Section 1. Therefore, we adapted the general method-
   In supervised learning, a learning algorithm (learner) builds a            ology of Kitchenham in two ways: we only relied on electronic
predictive model during a training phase, based on features found             search queries to collect papers (as we were not sure which aca-
in the training data, by optimizing a defined objective function. The         demic venues were suitable to such publications, although the study
learned model is then used in a subsequent phase as a predictor               direction we focus on highly suggested to look into Fv venues);
for new, previously unseen data. Tasks can be further classified              and we conducted a pre-study to determine which information is
into problems according to the nature of the predicted variable               relevant to build our survey. More concretely, we followed three
(also called target): categorical or continuous. For instance, in the         steps:
medical domain, determining whether an Mri evidences a cancer
is a classification task, because the answer is categorical (a boolean              • First, we queried several search engines to crawl the largest
yes/no answer, but more elaborate classes may be possible); whereas                   possible set of relevant publications.
determining which quantity of insulin should be injected into a pa-                 • Second, we conducted a pre-study on a set of random pa-
tient’s blood stream is a regression task, since the predicted variable               pers to determine classification categories for analyzing
is continuous.                                                                        the literature.
                                                                          2
                                              FV                                                                                                ML
                                                                                                  machine learning ∨ supervised learning ∨ unsupervised learning ∨ semi-supervised learning ∨
                                                                                                  clustering ∨ regularization ∨ overfitting ∨ underfitting ∨ feature selection ∨ dimensionality
                                                                                                  reduction ∨ cross-validation ∨ backpropagation ∨ artificial neural networks ∨ deep learning ∨
                                                                                                  support vector machines ∨ kernel methods ∨ decision tree ∨ decision trees ∨ rule learning ∨
                                                                                                  fuzzy learning ∨ meta-parameter tuning ∨ hyper-parameter tuning ∨ ensemble learning ∨
  Formal Method ∨ Formal Methods ∨ Formal Analysis ∨ Formal Verification ∨ Model Checking ∨       ensemble methods ∨ random forest ∨ probabilistic learning ∨ bayesian induction ∨ bayesian
  SAT Solver ∨ SMT Solver ∨ Theorem Proving ∨ Static Analysis ∨ Abstract Interpretation           probability ∨ reinforcement learning ∨ regression ∨ feature extraction ∨ gradient descent ∨ cost
                                                                                                  function ∨ data mining ∨ data science ∨ natural language processing ∨ active learning ∨ transfer
                                                                                                  learning ∨ matrix factorization ∨ manifold learning ∨ multidimensional scaling ∨ preference
                                                                                                  learning ∨ ranking learning ∨ similarity learning ∨ distance learning ∨ statistical learning ∨
                                                                                                  density estimation ∨ text mining ∨ time series analysis ∨ predictive model ∨ learning bias ∨
                                                                                                  maximum likelihood ∨ k-nearest neighbors ∨ k-means

Table 1: Query String used for Search Engines. We queried the most popular and well-known academic publishers that offer
keyword-based search engines (Elsevier ScienceDirect; Springer Link; Ieee XPlore and Acm Digital Libraries; Semantic Scholar,
Scopus, Mendeley and Google Scholar) with the conjunction of strings appearing in Fv and Ml columns.



       • Third, all authors reviewed the papers and filled a shared                                        (2) identifying the corresponding Ml task;
         document with the relevant information extracted from                                             (3) providing Ml features to characterize the learning instances;
         the papers.                                                                                       (4) figuring out which Ml model (type) would perform ade-
The rest of this section explains each step in detail, and finishes                                            quately.
by formulating our Research Questions in Section 3.4. Table 2                                       Whether extracting Ml model types (Step 4 of the pipeline) from
summaries our findings.                                                                             the papers we reviewed has any relevance for readers is debatable:
                                                                                                    the list we propose is informative, since it only reflects the model
3.1      Search Strategy                                                                            types authors have selected, but may in some cases be disputed by
Having no assumption on how to locate relevant papers, we simply                                    Ml experts to be the optimal solution (if such an optimal solution
opted for a large list of terms on both sides: we used general-                                     ever exists). Nevertheless, we included this information to reflect
purpose terms for Fv and Ml, strings corresponding to techniques                                    the literature, such that readers can grasp what experimentations
and algorithms, as well as small variations of those terms (e.g., plu-                              have been conducted to date for a particular theme/approach.
ral and hyphened forms, “-ing” forms of verbs, etc.). The search                                        We then performed a first round of reading in order to roughly
was conducted between the 10th and the 30th September 2017. We                                      classify each paper into Fv approaches, and to discard papers that
queried the main well-known electronic repositories (Elsevier Sci-                                  were clearly out of scope – papers that solely focus on one topic
enceDirect, SpringerLink, Ieee XPlore Digital Library, Acm Digital                                  (either Fv or Ml), or papers that leverage dynamic techniques (i.e.
Library, Semantic Scholar, Scopus and Google Scholar), where we                                     that require to actually execute the system). This step resulted in a
manually processed the result pages and selected the relevant pub-                                  categorized repository and a shared spreadsheet for cross-checking
lications. We discarded some contributions clearly out of scope                                     papers that have unclear contributions. When the Fv contribution
based on their abstract and a quick scan of the content. We stopped                                 was not clear (i.e., whether it does not fit into an Fv approach),
collecting papers after 10 pages of results for each search engine, be-                             we ensured that a cross-check by an author with the appropriate
cause at that point, most results simply correspond to disjunctions                                 background was made; when the Ml contribution was doubtful
of all strings, which becomes highly irrelevant. Our search string                                  (i.e. whether it is really an Ml technique), the author with Ml
is formed as a conjunction of the disjunction of the expressions                                    background checked the paper. This resulted in discarding 96 pa-
in each column of Table 1. Finally, at a later stage, we performed                                  pers, thus retaining 168 papers for analysis: 53 papers define actual
a lightweight snowballing from the set of papers we collected, in                                   themes whereas the rest define auxiliary resources. In particular, we
order to retrieve papers that may have been missed by our search                                    list in Table 3 papers that provide reference contributions regarding
keywords. This resulted in 264 papers collected in a shared online                                  the definition of Ml features.
repository.
                                                                                                    3.3       Literature Analysis
3.2      Pre-Study & Paper Filtering
                                                                                                    Once the papers were sorted, the authors with a background in
The next step aimed at discarding clearly irrelevant papers, and                                    Fv were assigned two Fv approaches to review: they extracted the
performing a pre-study to extract analysis categories. Each author                                  theme, identified the corresponding Ml task, and retrieved features
selected about 20 papers and proposed classification criteria that                                  from each paper. The last author cross-checked the most key papers
were collegially discussed. We ultimately retained the elements                                     in each approach to allow a comparison from both perspectives,
that constitute a classical Ml pipeline:                                                            thus reducing misleading readings about the theme or the task.
      (1) identifying the theme, i.e. the Fv problem at hand;                                       At later stages when the list of themes became stable, we made
                                                                                              3
vocabulary used throughout the approaches homogenous. When                         In order to guide the reader, Table 2 gathers the highlights of our
possible we factored out the common features for the approaches                findings in a comprehensive way: for each theme identified within
(mostly done for Sat and Tp).                                                  each approach, we gather all the selected contributions from the
                                                                               literature, the Ml tasks used in that theme and provide hints on the
3.4    Research Questions                                                      Ml model types that these contributions used.
This survey aims at answering the following Research Questions
(Rq):                                                                          4.1    SAT / SMT Solving (SAT)
RQ1: How is Ml used inside Fv tools? This Rq will be answered in
                                                                               The Sat problem is a decision problem: given a boolean propo-
two ways: first, by precisely locating where and how Ml is used
                                                                               sitional formula, find one (or several) valuation(s) for which the
inside Fv tools; and second, by providing a higher-level overview
                                                                               formula evaluates to true. When such a valuation exists, the for-
that spans over all Fv approaches.
                                                                               mula is said to be satisfiable (and unsatisfiable otherwise). Usually, a
RQ2: Is using Ml inside Fv tools beneficial? This Rq is necessary to
                                                                               formula is processed starting from a canonical representation such
assess the benefits of Ml in Fv. We answer this Rq qualitatively,
                                                                               as the Conjunctive Normal Form (Cnf), where formulas consist
based on the assessments made by the authors of the papers we
                                                                               of disjunctions of clauses, which are themselves conjunctions of
surveyed.
                                                                               literals defined as variables or their negation. Theories may enrich
RQ3: What Ml task(s) is (are) used for which purpose in Fv? This Rq
                                                                               propositional boolean formulæ to represent e.g. first-order logic,
is intended to associate an Ml task to an Fv theme, as described in
                                                                               numbers or richer data structures such as arrays or lists, resulting
Background Section 2.2, and helps bridging both worlds by relating
                                                                               in the Satisfiability Modulo Theory (Smt) decision problem. Some
activities in Fv tools to a meaningful category for Ml experts.
                                                                               Fv approaches may be reduced to a Sat problems (e.g., Mc [4] and
RQ4: Which model types are used to perform the Ml tasks? This
                                                                               Tp [14]; for Fv see [77]), making Sat research relevant for Fv.
Rq is intended to collect from the reviewed papers the Ml model
                                                                                   No algorithm can solve all Sat instances efficiently, which results
types the various authors have used to enhance Fv tools. Although
                                                                               in a plethora of solving algorithms. Most of the existing algorithms
indicative and by no means complete or definitive, it provides an
                                                                               are variations of the Davis–Putnam-Logemann–Loveland (Dpll)
interesting panorama of the current practice.
                                                                               algorithm. In practice, tools need to carefully choose the adequate
RQ5: How are Ml features extracted/selected to guide Ml tasks? This
                                                                               variation for a given (set of) instance(s) to solve them efficiently,
Rq is intended to locate the Ml instances’ characteristics as used in
                                                                               generally by reducing the overall runtime. In a simplified way,
the literature, and to eventually list the most common ones.
                                                                               the Dpll algorithm proceeds as follows: first, chooses a branching
                                                                               literal and assign it a truth value; then, propagates this assignment
4     CONTRIBUTIONS                                                            to other clauses, resulting in unit clauses, i.e. clauses in which
This section catalogs some of the ways Ml complements Fv ap-                   only one literal remains unassigned, making its assignment obvi-
proaches. We aimed at representativity, i.e. we tried to maximally             ous; and finally, propagates those choices appropriately until full
cover the Ml/Fv complementarities (called themes from now on) to               assignment, or detection of conflict. When facing a conflict the
propose an overview of the panorama of techniques and current                  algorithm backtracks to the previous branching literal to try the
practices in this field. To the best of our knowledge, this is the first       opposite assignment. These steps apply recursively until success
study that spans over the main Fv approaches to provide insights               or unsatisfiability. The Conflict-Driven Clause Learning (Cdcl)
on how Ml participates in Fv tools.                                            improves the general Dpll algorithm by analyzing the cause of the
   We organize this section by Fv approaches in a self-contained               conflicts and backtracking to the appropriate level instead of simply
way such that each may be read independently. We start with                    the previous choice, thus improving the overall runtime.
Sat-Smt Solving, then Theorem Proving (Tp), which corresponds                      Historically, the Sat community already identified a number
to a progression in the expressiveness of the underlying logics                of (Sat) instances features that characterize the hardness of satis-
(propositional/boolean, then First-Order and Higher-Order). After              fying an instance. We detail here the most important ones, and
we introduce and Model Checking (Mc), given the particularity that             mention in the themes the contributions’ features that differ from
temporal logic deals with time, and end with Static Analysis (Sa).             them. SATzilla [100, Fig. 2] integrates a large number of these well-
   Each approach follows the same outline. First, we briefly recall            recognized features (around 150): instance size metrics; Variable
how the Fv approach works. Second, we explain the sources of                   Incidence / Clause-Variable Incidence Graphs (Vig/Civg) metrics,
complexity (typically, NP-completeness) and which countermea-                  balance of positive/negative literals in clause and variable occur-
sures (e.g. heuristics) have been historically designed to partially           rences, binary/ternary and Horn clause fractions, number of unit
overcome them. When necessary, we introduce a brief explanation                propagation, search space size and other local search probing char-
of the main algorithm supporting the approach in order to fix the              acteristics. The contributions not explicitly dealing with feature
terminology and to situate how each theme finds its place in Fv.               improvements basically reuse different subsets of these features
Third, we introduce for each theme where the Fv/Ml complemen-                  (see e.g., [44, 97] among many others). For 3-Cnf Sat instances, the
tarity exists, ground it in terms of Ml task(s), and finally provide           authors of SATzilla [98] managed to reduce to five the list of the
examples from the literature. When possible, we indicate the Ml                most prominent features, without significant loss of performance.
features associated with the theme: when they are common, they                 Ansótegui and his co-authors [6] defined new interesting features,
are factored out into the section’s headers; otherwise, they appear            targeting industrial Sat instances: the scale-free structure assumes
in each particular theme.                                                      that the ratio of variable occurrences and total number of variables
                                                                           4
follows a power-law distribution; the community structure mea-               are seen as the possible actions to reinforce. Rewards are defined
sures the modularity of graphs, i.e. how high is a node connected            differently depending on the particular contributions.
to its direct neighbors; and the self-similar structure measures the            Haim & Walsh [39] proposed to select a strategy from a portfolio
fractal effect of Cig and Cvig, i.e. how it changes when a group of          of 9 that were proven to perform well on at least one dataset. The
nodes is replaced by a single one. They show that relying on those           training is based on a subset of features taken from [100]; the pre-
features is computationally affordable, and predicts the instance            diction is realized dynamically, while solving the instance. Horvitz,
satisfiability in a way that is comparable to taking all features that       Kautz, Ruan and their colleagues adopted a more contextualized
SATzilla uses.                                                               approach, in the context of dependent runs [50, 81]: they used
                                                                             predictors (called observators) on some instances of a set to help
    4.1.1 Predicting Runtime. Predicting the runtime of an instance
                                                                             determine how to perform restarts for the other instances of the
(or a subformula) is helpful in many regards: choosing an appropri-
                                                                             set. Observators are generally classifiers trained on a few instances
ate solver depending on the runtime; interrupting a computation to
                                                                             that predict whether (future) instances would be satisfiable or not,
switch to another algorithm when the current one takes too long; se-
                                                                             or whether their runtime takes a short/long time.
lecting an appropriate restart strategy when encountering conflicts;
                                                                                Nejati et al. [74] targeted cryptographic instances, whose run-
selecting a variable to branch on depending on the runtime that
                                                                             time is usually much longer than other instance types, making
will likely result; etc. Runtime is a real, continuous value, making
                                                                             restart strategies a core component. Solving an instance requires,
this prediction, strictly speaking, a regression Ml task. However, the
                                                                             during the solving itself, to change / switch strategies, among the
literature often considers runtime classes (e.g. long/short runtime
                                                                             ones that are known to be the most effective in the literature: uni-
of a specific algorithm, i.e. observing whether the runtime crosses
                                                                             form, linear, luby and geometric [13]). Reinforcement Learning is
a predefined threshold, considering a time budget for solving an
                                                                             performed through the following steps. First, a strategy is chosen,
instance set). This results in practice in a classification Ml task.
                                                                             and the general algorithm proceeds with the solving until the strat-
    Horvitz, Ruan et al. [44] estimated the runtime of the Quasi-
                                                                             egy imposes a restart. At this point, the strategy is rewarded based
group Completion Problem (Qcp, closely related to Sat) by defining
                                                                             on the average Literals Block Distance (Lbd) of the learned clauses
a set of features that accurately estimates the resolution progress
                                                                             generated since the strategy was selected. Finally, this results in
by reflecting the instance patterns (instance size) and dynamic in-
                                                                             choosing/favoring strategies that produce small Lbds for the future
formation about the solver’s state (number of backtracks, search
                                                                             solving steps. Gaglio and Schmidhuber [35] considered the problem
tree depth). Samulowitz and Memisevic [85] targeted Quantified
                                                                             of using the best restart strategies for a set of instances to minimize
Boolean Formulæ and proposed various features: the Vsids (Vari-
                                                                             the global runtime. They choose between two strategies (Luby’s
able State Independent Decaying Sum) score, the number of con-
                                                                             universal and uniform). After one step of solving an instance, they
flicts and the fraction of already solved clauses, the weighted sum
                                                                             reward the strategy that results in a runtime that stays close to
between forced literals and Vsids scores.
                                                                             the runtime of the previous instances. This results in favoring the
   4.1.2 Restarting Computations. When encountering a conflict               strategy that provide a global runtime for the set that is the closest
during resolution, the analysis of the literals that led to assignment       to the runtime of most of the instances in the set.
inconsistencies allows to efficiently backtrack to an appropriate
level, avoiding traps that would likely result from a backtrack at              4.1.3 Selecting the Branching Variable. Choosing the most ap-
another level. A theoretical instance-specific optimal restart strat-        propriate branching variable is crucial for improving solvers’ run-
egy exists, but requires the knowledge of the instance’s runtime             times, because it ultimately minimizes backtracking (which can be
distribution (rarely known and difficult to compute) [66]. Those             seen as a step back towards a solution, since it implies unassigning
strategies are split into two categories: universal strategies are de-       some of the already selected variables). This can be seen as a rein-
fined independently of the instance; and dynamic strategies adapt to         forcement learning problem: along a Sat instance solving, choose
the search length, i.e. the number of already assigned literals. Since       the next variable to branch on, such that the reward attached to the
no strategy outperforms all others on all datasets [45], adapting the        variable choice, called score, maximizes the progress for solving the
strategy to a dataset is often better, and constantly reevaluating the       instance. Note that this task is non-stationary from the Sat solving
portfolio of restart strategies is desirable to keep improving Sat           viewpoint: after each choice, a variable cannot be selected anymore
solvers performances [13].                                                   unless a conflict occurs.
   For solving as many instances as possible within a given time                Liang et al [60, 61] explored two different reward computations
budget, selecting the best restart strategy on an instance basis (ac-        based on different branching heuristics: in [60], they used a conflict-
cording to its features) represents a classification Ml task: from a         history-based heuristic for variable selection; while in [61], they
set of predefined strategies, determine which one would be the best          used another heuristic called learning rate branching. Both re-
to optimally (i.e. by minimizing the expected runtime) solve the in-         warded the generation of learned clauses locally, at each step of
stance at hand. For very hard instances (typically, industrial/crafted       the solving. Later on, Liang et al. [62] rewarded selections that
instances representing cryptographic or planning problems [6]),              maximize global branching learning rates, i.e. rates for the whole
or for solving several instance sets while minimizing the overall            solving. Fröhlich et al. [33] penalize the candidate variables choices
runtime, switching between strategies during the solving is often            that minimizes the number of unstatisfied clauses. Lagoudakis and
more efficient, when some strategies are known in advance to be              Littman [58] penalize branching rules (chosen among seven known
the most powerful for the given instances (sets). This can be seen as        as the best working) whose solving time is too long.
a reinforcement learning problem, in which restart strategy choices
                                                                         5
   4.1.4 Determining Best Solving Algorithm. The Sat community               neither underconstrained (i.e. exhibiting many possible solutions),
identified families of instances that may be better solved with spe-         nor overconstrained (i.e. exhibiting many contradictions). Devlin
cific algorithms, enhancing specific criteria (mostly, solving run-          and O’Sullivan [29], and later on Xu, Hoos and Leyton-Brown
time). In a pure form, this is a classification Ml problem: from a set       [99] studied several classifiers for predicting the (non-)satisfiability
of instances, determine which solving algorithm(s) would be the              of general Sat as well as 3-Cnf instances, based on the classical
most efficient according to a given criterion. However, this could           features used in SATzilla. Xu, Hoos and Leyton-Brown tried to
be seen as a regression Ml problem, when the goal is to predict an           minimize the number of necessary features to build good classi-
algorithm continuous probability of success. Both Ml tasks are               fiers, and managed to reduce to two features while staying robust
achieved offline, i.e. before running the solving algorithms. Note           comparing to classifiers with more features.
that pre-solving is mainstream, i.e. trying some predetermined,
quicker algorithms that may solve some of the instances, leaving
the portfolio selection to focus on difficult instances.                     4.2    Theorem Proving (TP)
   SATzilla [100] is one of the best portfolio solvers [59]: it relies       When the semantics of a software or of a system is expressed as
on a large variety of specialized Sat algorithms that are chosen             mathematical theories, verification conditions for those systems
according to the specificities of the instance at hand, based on             can be formulated as mathematical properties of those theories.
115 features (cf. feature discussion in Section’s header). It allows         In Fv, Theorem Provers (Tp) are then employed, in a more or less
to switch to another algorithm (“next best match”) when the one              automated fashion, to prove or disprove such properties.
attributed initially takes too long. AutoFolio [63] selects algorithms          Mathematical theories are composed of mathematical facts, which
based on features similar to the ones in SATzilla.                           are assumed to be true. Tp is used to infer new facts about the theory,
                                                                             using the inference rules associated to the logic of choice. In this
   4.1.5 Configuring Sat Solvers’ Parameters. Instead of setting
                                                                             sense, a mathematical statement (known as conjecture) becomes
default values for the multiple parameters of the various Sat algo-
                                                                             a theorem if it logically follows from the theory. More precisely,
rithms constituting a portfolio, many Sat solving tools choose to
                                                                             Tp operates as follows: 1) it receives as input a set of facts from a
expose those parameters to the end-users, passing them the burden
                                                                             mathematical theory which are assumed to be true and a conjecture;
of configuration. The end-user faces a highly difficult task: which
                                                                             2) it performs a number of inferences on those facts using the set
parameter settings of the algorithm(s) perform best on a set of
                                                                             of rules that describe the semantics of the logic being used; and 3)
instances, minimizing a cost function (typically in Sat, runtime).
                                                                             outputs a proof for the conjecture or a trace thereof, if one exists,
Several approaches already exist based on heuristics, but the do-
                                                                             in which case the conjecture becomes a theorem and can be added
main recently gained attention with Ml. This particular domain
                                                                             as a new fact to the theory.
has its own competitive event: the Configurable Sat Solver Chal-
                                                                                First-Order Logic (Fol), one of the most popular logics in Tp, is
lenge. Finding the optimal values of a Sat solver’s parameters is
                                                                             semi-decidable. The bulk of the work of applying Ml techniques to
a regression or a classification task whether if a continuous or a
                                                                             TP has thus targeted Fol. Ml techniques assist or replace existing
categorical value is predicted.
                                                                             expert knowledge-based heuristics in order to better navigate the
   Hutter, Hoos and Leyton-Brown [46] defined Smac (Sequential
                                                                             border between decidability and non-decidability and more effi-
Model-based Algorithm Configuration), a technique and tool that
                                                                             ciently lead theorem proofs to completion. Because they present
generalizes the classical optimization algorithm by using training,
                                                                             a high level of automation, provers for Fol are called automated
based mostly on SATzilla’s features. AutoFolio [63] parametrizes
                                                                             theorem provers (Atps).
ClasspFolio 2 (the default version of SATzilla’11), resulting in a
                                                                                Higher-order logic (Hol) adds to Fol the quantification of predi-
highly parametrized algorithm framework.
                                                                             cate and function symbols. Such expressiveness is convenient to
   4.1.6 Learning Satisfiability. Tackling the whole Sat problem             express verification problems that would otherwise be too difficult
through Ml seems difficult, but has been partially attempted. Over-          or impossible to express in lower-order logics. However, Hol is
all this corresponds to a classification problem (although many              undecidable and presents fewer opportunities for automation than
other Ml tasks are performed in between to serve the main goal):             Fol, which means parts of the proofs need to be guided by humans.
determine whether a Sat instance is satisfiable or not.                      For this reason, in the context of Hol, provers are called interactive
   A partial prediction on a subformula may guide a solver for other         theorem provers (Itps).
tasks (e.g., restarting efficiently, or evaluating the potential of a           Decidability and efficiency issues in Atps/Itps mean that de-
variable selection, among others). For example, Wu [97] predicted            cisions are delegated onto humans at many points of the proof.
3-Cnf instance satisfiability with seven features from SATzilla and          Such decisions involve for instance: choosing facts (also known as
other classical ones. They reuse the partial prediction to determine         premises [57]) from the theory relevant to the proof at hand; pick-
which value is preferable for a branching literal. Although the tech-        ing sets of proof engine parameters (also known as heuristics [19])
nique is applied to subformulæ, nothing prevents the technique               such as for instance sets of inference rules used [56]. It is in sup-
from being used on a larger scale (although optimizations are nat-           porting or replacing the human in these decisions that Ml comes
urally expected). One would expect that a Sat problem becomes                to the aid of theorem proving.
harder when the number of clauses increases. In fact, the most diffi-           Features used to characterize facts or conjectures about theories
cult instances are those whose ratio of clauses over variables is near       are majoritarily the symbols found in those mathematical state-
the so-called phase transition (particularly for 3-Cnf instances): the       ments [69], for example literals or predicate names. Metrics such as
number of clauses and variables is at equilibrium, making instances          the number of clauses, literals or subterms, or yet specific metrics
                                                                         6
about the translations of logical formulas into normal forms have                    Bridge [19], a reference for this theme, evaluates more than
also been used [56]. Other authors have attempted to use types [47],             fifty features and concludes that only combinations of very few
or meta-information about the theory name and its presence in                    features (up to two) are required to build classifiers that vastly
various mathematical databases [55]. Recently, Kaliszyk and his co-              outperform random proof engine parameter selection. With his
authors have proposed features that capture semantic relationships               colleagues [20] Bridge later confirms that their system yields the
between mathematical statements [49].                                            same performance as E’s internal proof engine parameter selection
                                                                                 mechanism, without requiring the introduction of any human-
   4.2.1 Selecting Facts. Which subset of facts to take from a large             expert knowledge. Additionally, the system is also able to decline
theory in order to complete a given proof as efficiently as possible             some proofs in case no proof engine parameters can lead to the
(or at all) is one of the most prominent applications of Ml to Tp [57].          completion of the conjecture’s proof in an acceptable amount of
Fact selection is a classification task: either a fact is relevant for the       time (or at all). The authors report that declining proofs greatly
current proof or not, potentially with a probability reflecting a level          improves performance, while only moderately reducing the amount
of certainty.                                                                    of provable theorems.
   Fuchs [34] uses data from previous proofs to train a model for
computing the usefulness of the available facts for the next proof                  4.2.4 Guiding Interactive Proofs. Due to the undecidability of
step. Alama [1] preanalyzes a large mathematical repository of                   Hol, there is no systematic way of finding proofs for conjectures
formalized theories in order to calculate dependencies between                   in such logics. Itps such as Coq [68], Isabelle [15] or Mizar [38]
parts of those theories that can then be used at proof time. Kaliszyk            are used to assist the mathematician in proof finding, while Proof
et al. [16, 47] use classification models to rank facts in Hol theories          General [8] provides a high-level user-friendly interface to those
according to their assumed relevance for the proof of the conjecture.            Itps. Itp environments can act as recommender systems to suggest
They then reduce the best ranked of those facts to simpler problems              for example promising facts to be used in the proof. Because this
that can be handled by fast Fol Atps to help in parts of the proof               theme touches many parts of proofs, both classification and clus-
of the original conjecture. Again Kaliszyk, together with his co-                tering Ml techniques can be used. Clustering becomes particularly
authors, provide in [48] a compelling account of how MaLARea                     useful here as it can inform the user of potential next steps through
performs Ml-based fact selection for the equational reasoning Atp                statistical analysis on similar proofs – it however cannot lead to
E [86] beating the competition in large-theory contests. Alemi et al.            automatic decision making such as when supervised approaches
report in [2] the first application of deep learning to fact selection           are used.
for large theories, concluding that neural networks do help in large-               Urban [93] describes a set of proof aids in Emacs for Mizar,
scale automated reasoning without requiring hand-crafted features.               explaining how Ml classification algorithms are used to suggest
They mention nonetheless that hybrid premise-selection solutions                 facts to a mathematician for the continuation of the proofs. Mercer
where hand-crafted solutions are used together with their solution               et al. [31] propose a system and a user interface for recommending
may yield even superior results. Loos and her colleagues confirm                 the next proof step, based on Duncan’s work [30] on modeling
this thesis in [64] and conclude that fact selection mixing neural               proofs with Variable Length Markov models. Komendantskaya and
networks and other methods is particularly useful for hard theorems              Heras interface Proof General with back-ends running clustering
that require complex reasoning.                                                  algorithms [53] to gather statistics on data from previous proofs.

   4.2.2 Configuring Proof Engine Parameters. Proving a particular                  4.2.5 Learning Theorem Proving. Rocktäschel and Riedel at-
conjecture is typically achieved more or less efficiently (or at all) by         tempted to learn the backward chaining algorithm for Fol [80].
providing the prover with a set of parameters. It is well established            Starting from a set of neural networks that modularly perform
in the Tp community that certain parameters configurations are                   generic Tp-related tasks (such as for example unification), the au-
better suited for the proof of certain classes of conjectures [19].              thors propose an algorithm that is able to assemble those modules
Constructing such parameters automatically for specific conjectures              in order to deduce new theorems from a given knowledge base. This
is assisted by an Ml regression task: Ml helps in predicting proof               contribution has the particularity that, due to the fact that modules
runtime when heuristics are evaluated on specific conjectures.                   are used, the proof is in itself interpretable – more specifically how
   Kühlwein and Urban investigate in [56] a method to automat-                  those modules are used during the proof provides a proof trace. As
ically tune parameters of Atps in order to optimize proof times .                the output of the neural network is a proof score that describes
Their method starts from a set of random or predefined heuristics                the confidence in the derived facts, we technically classify it as a
and the Ml algorithm learns to predict how fast these heuristics                 regression task.
perform on classes of existing problems. The technique then iter-
atively improves the parameters of successful heuristics by using
                                                                                 4.3    Model-Checking (MC)
the prediction learner.                                                          Model-Checking (Mc) [24, 78] consists of abstracting the concrete
                                                                                 system’s execution into a finite-state automaton (that can be ex-
   4.2.3 Selecting Pre-Defined Proof Engine Parameters. Some the-                tracted automatically from the program, and whose execution may
orem provers select proof engine parameters that were manually                   be infinite); and the properties of interest are expressed in temporal
or automatically generated (cf. Configuring Proof Engine Param-                  logics. The model-checking procedure explores exhaustively the
eters theme). This is a classification Ml task: given a conjecture,              (abstract) state space, and either validates the properties, or returns
provide the heuristic that will most likely produce a proof for it in            a counterexample (that may be a false alarm). In practice, exhaustive
an efficient manner.                                                             exploration is difficult: many techniques were crafted to reduce the
                                                                             7   state space (symmetry, slicing, partial evaluation, to cite only a few),
or enhance its exploration (through path exploration heuristics).             recurring paths or rules leading to such errors is related to the Ml
They nowadays equip most tools. We did not find Ml contributions              task of frequent item set finding.
that work at the Mc algorithm level like for others Fv approaches;               Pira, Rafe and Nikanjam [76] characterized frequent patterns as
rather, we found contributions that help detecting counterexamples            sequence of rewriting rules in Groove, a graph-based model trans-
faster, or reducing false positives (using the well-known Cegar               formation tool, using a variation of the APriori algorithm. Those
approach). Note that we did not include contributions for Assume-             patterns are discovered on smaller systems with similar architec-
Guarantee Reasoning [3, 10, 21, 27, 36, 72, 75, 91] based on the              tural design, then used to guide Mc on larger systems.
L∗ algorithm [5, 79]: it is difficult to conclude without deepening
the subject whether L∗ is an Ml algorithm, and which Ml task it               4.4    Static Analysis (SA)
corresponds to.                                                               Static Analysis (Sa) designates a large panel of techniques aimed
                                                                              at computing any information about a program, generally directly
   4.3.1 Finding a Counterexample. Model-Checkers should be ori-              on its Abstract Syntax Tree Ast. The underlying abstractions rely
ented towards error detection [26]: they should favor the discovery           on predefined approximations (possibly parameterized by users’
of errors rather than focusing on guaranteeing correctness. As                inputs): this results in a fixed set of properties of interest, e.g.
a consequence, optimizing counterexample finding is crucial. A                extracting Android apps’ permissions from .apk files, which may
possible approach is to explicitly guide the state space exploration          be parameterized to find only device-specific ones. In most cases,
towards paths that may favor such counterexamples, based on the               the analysis does not carry in itself its own final usage: for instance,
property of interest at hand. This may be achieved through rein-              permissions, in themselves, do not give any information about an
forcement learning: a reward favors positive paths for invalidating           app being a malware. Most of the contributions in Sa leverage Ml
the property; while a punishment discourages negative paths vali-             to bridge this gap, by trying to find links, or reccurent patterns,
dating it. Note that the qualificatives positive/negative correspond          in the retrieved information, e.g. malwares are apps that present
to the error detection goal instead of the traditional Mc goal.               significant discrepancies between exhibited permissions and actual
   Araragi and Mo Cho [7] targeted the production of counterexam-             executed code.
ples for liveness properties that represent responses, i.e. a (premise)
event is expected before a (response) event should eventually occur.              4.4.1 Identifying Actionable Alerts. Sa tools often issue large
The authors kept track of the premise occurrence at the state space           amounts of alarms that warn about code style violations, trivial de-
level, and rewarded explorations that stayed on paths between                 fects with no impact on functionalities, false positives and, of course,
premise and response as long as possible. This would lead to cyclic,          real bugs. Too many warnings hamper developers’ productivity by
or very long (or infinite) paths that would invalidate the property.          forcing them to review alarms, diverting their attention from issues
Behjati, Sirjani and Ahmadabadi [11] studied Ltl properties on                that matter (cf. surveys on alarms handling [43, 71]). Reducing
Büchi automata with on-the-fly Mc: the reinforcement learning                and classifying those alarms based on previous iterations/similarity
agent is punished when following non-accepting cycles, and re-                significantly enhances the experience of using Sa tools. This is a
warded when finding unfair accepting cycles, until a fair one is              classification Ml task: from a set of flagged alarms, which ones are
found, leading to the property’s invalidation.                                actionable, i.e. require a specific bugfix from a developer.
                                                                                  Heckman & Williams [42] postulated that characterizing whether
    4.3.2 Refining Abstraction based on Counterexamples (CEGAR).              an alarm is actionable highly depends on each project and devel-
A spurious counterexample (false alarm) happens when the last                 opers involved. They reduced the unactionable alarm number by
state of a path in the concrete system mixes both deadend states,             first gathering alarms and their features, then by selecting the most
i.e. states with no concrete transition to the failure state; with            relevant ones for training a classifier for future projects. They
bad states, i.e. states using (system) variables useful to prove the          used as features the usual metrics (LoC, etc.) with code change
property, that are not taken into account, and abstracted together            history, and alarm types (null pointers, etc.) with alarm severity
with deadends. To eliminate such a counterexample, some variables             delivered by Sa tools. Hanam et al. [40] proposed to classify alarms
need to be identified and become visible, i.e. separated properly             as actionable or not by identifying recurrent patterns based on
within the abstraction. This is known as the separation problem in            characteristics related to code statements: invocation and creation
Cegar Mc, which is a classification Ml task: given a (sub)set of              sites, field access, binary operations, catch statements as well as
system variables from the failure state, determine whether they               other various structural features like method signatures and class
should be classified as deadend or bad. This information then allows          names. They showed that patterns effectively exist and help dis-
for an abstraction refinement that, even if not optimal, makes it             cover more errors than classical Sa tools reports. Kremeneck et al.
possible to discharge the counterexample. Note that for realistic             [54] correlated alarm reports with their code localization to classify
systems, enumerating all the variables is impossible: a preselection          alarms raised at later stages of code integration. Ruthruff et al. [83]
is generally operated beforehand.                                             identified the legitimate alarms that are more likely to be acted on
    Clarke, Gupta and their colleagues [23, 25] implemented this              by developers, based on Ml features similar to [40, 42]. They also
technique for model-checking hardware circuits, training a learner            managed to reduce the number of metrics necessary for performing
on samples automatically extracted from the concrete system.                  the classification, while preserving a correct classification ratio.
                                                                                 4.4.2 Predicting Bugs from Previous Code Versions. Instead of
   4.3.3 Extracting Most Common Error Patterns. Concurrency er-               running Sa tools during the development phase, an interesting
rors often result from the same error types [65, 82]. Finding the             line of research consists of predicting, at code submission into a
                                                                          8   repository, whether a code change likely contains bugs, based on
the analysis of previously submitted changes in a project. This                 also Sat/Smt-Solving) at different levels, using different techniques
presents several benefits: the change is still fresh in mind, and               and for different purposes.
several actions may be taken (from code review, testing, to Fv                     How can Fv and Ml experts collaborate to leverage Ml’s current
techniques), targeting the recent change. This is a classification Ml           practices in order to enhance and improve current Fv tools? We
task: predict whether a code change is likely to contain bugs, based            follow the classical Ml pipeline: (i) identifying the Fv problem at
on the analysis of previous code version(s).                                    hand; (ii) identifying the corresponding Ml task; (iii) providing Ml
   Kim and his colleagues [51, 88] as well as Hata et al. [41] intro-           features to characterize the learning instances; (iv) figuring out
duced change classification by analyzing the change history, based              which Ml model (type) would perform adequately.
on log messages keywords and correlations to bug fix requests.                     The remainder of this section discusses each of these points, gives
Their predictors rely on various features: change metadata on the               general perspectives on what seems promising for the future, and
versioning system, complexity metrics and various Sa information                provide answers to the research questions formulated in Section 3.4.
to locate code change and analyze their impact. Kim and his col-
leagues also investigated in [51] the possibility of reducing the large             FV Problems ( RQ1: How is Ml used inside Fv tools?) Fv experts
amount of features extracted from change history.                               first identify what they expect to improve, compute, or which kind
                                                                                of pattern they seek in their data. This is one of the topics covered
    4.4.3 Classifying Android Apps as Malware. With hundreds of
                                                                                by this paper: each of the themes indicates precisely to which extent
new apps and countless updates, detecting malware in Android
                                                                                Ml is used in the overall Fv approach: some contributions/tools
apps has become crucial to ensure end-users’ security. Most con-
                                                                                invoke Ml at various steps, or even handle the approach altogether.
tributions mixing Ml with Sa rely on misuse detection that flags
                                                                                We noticed several patterns according to Ml categories. Supervised
an app when permissions mismatch the actual app functionalities
                                                                                techniques are often associated with two kinds of usage observed
(cf. [73] for an overview of static and dynamic malware detection).
                                                                                in Sat and Tp: external guidance, which stands for Ml models
This qualifies as a classification Ml task: given an Android app,
                                                                                that choose an appropriate heuristic, strategy or algorithm (e.g.,
together with a set of characteristic features that are extracted stat-
                                                                                portfolio solving in Sat and proof engine parameter selection in
ically, determine whether the app contains a malware. The listed
                                                                                Tp); and internal guidance, which represents situations where Ml
contributions differ in features and training data sizes for training:
                                                                                models play the role of heuristics/strategies, by selecting the next
we comment on features and refer to each paper for other details.
                                                                                following step in a more global algorithm (e.g., fact selection in
    Aung & Zaw [9] used five characteristic permissions (internet
                                                                                Tp or restart selection in Sat). Other uses do not fit these cate-
access, configuration files change, send/write Sms and phone calls)
                                                                                gories. For instance, the interpretative gap filling in Sa is performed
extracted directly from the distribution files (.apk) of known mal-
                                                                                through Ml models by finding links or recurrent patterns in the
ware and goodware from classical Android Markets. Sahs & Khan
                                                                                collected information (e.g. the link between permissions and the
[84] used a combination of permissions, categorized as built-in (like
                                                                                malware/goodware classes).
accessing Internet) and non-standard (like accessing the camera
                                                                                    Unsupervised techniques do not prescribe an “ideal” answer, but
or the localization), paired with Control Flow Graphs to analyze
                                                                                rather try to identify general patterns. The resulting tasks (mostly
the app’s code. Yerima and his colleagues [102, 104] (cf. [103] for
                                                                                clustering) seem more adequate for Tp, the only Fv approach fa-
details) extracted a set of complementary features, characterized
                                                                                voring interactivity. However, it is not excluded that unsupervised
by specific keywords: a total of 125 permissions extracted from the
                                                                                techniques may bring new insights into other Fv approaches, even
manifest; features related to Linux commands hidden in compiled
                                                                                those that already are fully automated.
or library code, used for escalating privileges or launching scripts
and malicious binaries; and standard Android Api calls extracted
                                                                                   ML Tasks ( RQ3: What Ml task(s) is (are) used for which purpose
from the app’s Dalvik code, to detect required interactions with the
                                                                                in Fv?) Once the Fv problem is identified, Fv specialists associate
various devices (e.g., Sim, location or network accesses, device or
                                                                                an Ml task to guide Ml experts towards the right set of techniques
user ids, or method invocation and class loading, boot process, etc.)
                                                                                and models. When Ml contributes to a small portion of the Fv
or to enrich apps with various functionalities (e.g. contact, Sms or
                                                                                process we have often observed classification tasks, i.e. selecting
Url lists already accessed).
                                                                                a candidate artifact among several available ones. In Tp and Sat,
   4.4.4 Learning SA. Tackling the Sa problem itself, directly from             selecting heuristics according to some criteria (potential for proof
the source program is a classification Ml task: providing the Ast,              completion; solving runtime) among those already programmed
does the (fixed, predefined) property hold or not.                              by experts, relieves Fv users from the burden of having to main-
   Several authors attempted this [22, 70, 101] for various analyses,           tain explicit knowledge of those heuristics. Such approaches have
but all noticed that, for the approach to scale, sufficient training data       improved tools significantly, as witnessed by Tool Contests in Sat
for each property needs to be available (positive as well as negative           and Tp. In Mc and Sat, reinforcement learning is used as a way to
training, i.e. verifying and falsifying the property at hand).                  “guide” the tool towards a counterexample and the most promising
                                                                                branching variable. The final Ml task may differ according to the
5   DISCUSSION                                                                  experts’ viewpoint, but is ultimately guided by Fv experts’ needs:
Is there a love story between Fv and Ml? In this paper, we sur-                 for example, a regression task such as predicting Sat solvers’ pa-
veyed one direction of this relationship: how Ml contributes to                 rameters values, or runtimes in Tp, may very well be turned into a
enhance Fv activities. Without being exhaustive, we have shown                  classification task by imposing runtime thresholds.
throughout Section 4 that Ml enhances all the spectrum of Fv ap-
proaches (Static Analysis, Model-Checking, Theorem-Proving, but             9
            Themes                                               Contributions                                             ML Task                          Ml Model Types gathered from Contributions
            Predicting Runtime                                   [85](+) [44](-)                                           Classification (or Regression)   Logistic Regression ; Decision Trees
                                                                 [39](o) [50, 81](+)                                       Classification                   Logistic Regression ; Decision Trees
            Restarting Computations
                                                                 [74](+) [35](o)                                           Reinforcement                    Multi-Armed Bandit
  Sat-Smt




            Selecting Branching Variable                         [60, 61](+) [62](+) [33] [58](+)                          Reinforcement                    Multi-Armed Bandit ; Temporal Difference
            Determining Best-Solving Algorithm                   [100](+) [63](+)                                          Classification                   Logistic Regression
            Configuring Solvers’ Parameters                      [46](+) [63](+)                                           Regression                       Support Vector Machines ; Random Forest Regression
                                                                                                                                                            Logistic Regression ; Decision Trees ; Random Forests
            Learning Satisfiability                              [97](+) [99](+) [29](+) [87]                              Classification
                                                                                                                                                            k-Nearest Neighbors ; Naı̈ve Bayes ; Neural Network
            Selecting Premises                                   [2](+) [64](+) [34](+) [1](+) [47](+) [16](+) [48](+)     Classification                   Kernel-based models ; Naı̈ve Bayes ; k-Nearest Neighbors
            Configuring Proof Engine’s Parameters                [56](+)                                                   Regression                       Kernel-based models
            Selecting Predefined Proof Engine Parameters         [19](+) [20](+)                                           Classification                   Gaussian Process Classifiers; Kernel-based models
  Tp




            Guiding Interactive Proofs                           [93](◦) [31](◦) [53](◦)                                   Classification / Clustering      Naı̈ve Bayes ; Variable Length Markov Models / k-Means
            Learning Theorem-Proving                             [80](-)                                                   Regression                       Neural Networks
            Finding Counterexamples                              [7](+) [11](+)                                            Reinforcement                    Q-Learning
            Refining Abstractions                                [23, 25](+)                                               Classification                   Decision Trees
  Mc




            Extracting Most Common Error Patterns                [76](o)                                                   Frequent Item Set                A-Priori
                                                                                                                                                            Decision Trees ; Bayesian models ;
            Identifying Actionable Alerts                        [42](◦) [40](+) [54](+) [83](+)                           Classification
                                                                                                                                                            Logistic Regression ; Rule-Based
            Predicting Bugs from Previous Code Versions          [51](◦) [88](+) [41](+)                                   Classification                   Support Vector Machines ; Bayesian models
  Sa




                                                                                                                                                            Decision Trees ; Random Forests ;
            Classifying Android Apps as Malware                  [9](◦) [84](◦) [102](+) [104](-)                          Classification/Clustering
                                                                                                                                                            Support Vector Machines ; Bayesian models / k-Means
            Learning Sa                                          [22](-) [70](+) [101](◦)                                  Classification                   Neural Networks
                           Legend: (+) improves the state of the art; (-) comparable to or worse than state of the art; (◦) no information on how the approach relates to the state of the art
                                      Table 2: Contributions and Ml tasks related to each theme within each Fv approach.



                                                  Reference Papers                                                       a consequence of Wolpert and McReady’s No Free Lunch Theorem
                                                                                                                         [96]). However, we believe that identifying precisely the answers to
                                                     [98, 100] [6]
                                                                                                                         the previous steps should provide Ml practitioners with sufficient
                           Sat-Smt

                               Tp               [69] [47, 49] [55] [56]                                                  information such that they can exercise their expertise.
                              Mc                          [23]
                                                                                                                        RQ2: Is using Ml inside Fv tools beneficial? Table 2 presents a
                                            [40, 42] [88] [41] [9] [84] [104]
                               Sa
                                                                                                                     summary of our findings: for each theme inside each Fv approach,
                Table 3: Main papers defining Ml features.                                                           we list the contributions we reviewed and indicate whether the
                                                                                                                     results of each contribution has improved the existing state-of-the-
                                                                                                                     art, and points to the models commonly used by all contributions
                                                                                                                     in a theme. From a statistical viewpoint, contributions that claim
   ML Features ( RQ5: How are Ml features extracted/selected to                                                      to have brought improvements largely outnumber the ones with
guide Ml tasks?) The choice of features is critical for the learning                                                 similar or lower quality than state-of-the art.
process. We noticed two main categories of such choices in Fv:
features are either based on the raw input used for the Fv approach                                                      Towards end-to-end Fv. All in all, we observed a pyramidal use
(e.g., Ast and manifests in Sa; Cnfs in Sat and Tp); or based on                                                     of Ml models. On one end of the spectrum, Ml models are used
measures computed on those raw inputs (e.g. Call Graphs for Sa,                                                      in a very narrow fashion inside Fv tools for solving very specific
ratios and clause numbers for Sat). Those features were identified                                                   problems inside tools. For instance, in Sat or Tp, the structure of
experimentally while tuning heuristics and/or trying to improve                                                      the current resolution algorithms can be preserved while delegat-
existing algorithms, and often predate the introduction of Ml. Iden-                                                 ing onto Ml models the optimization of specific choices that are
tifying the appropriate features is the task of Fv experts, but using                                                traditionally handled by heuristics (like restarts or fact selections).
Ml may help enhancing them or filtering out superfluous ones.                                                        On the other end of the spectrum, we noticed several attempts to
Table 3 lists the main contributions in each Fv approaches.                                                          handle an Fv approach globally: for instance, predicting satisfia-
                                                                                                                     bility of a formula [97, 99], building a proof [80] or learning static
   ML Models ( RQ4: Which Ml model type are used to perform the                                                      analysis directly [22, 70, 101]. Between these two ends, a range
Ml tasks?) The selection of an Ml model to perform a specific Ml                                                     exists determined by how much Fv expert knowledge is considered
task is the final step. This is extremely delicate, and essentially a                                                while solving the Fv problem. Ml typically aims at finding objective
problem for Ml experts. We noticed in the surveyed contributions                                                     generalizations; however, if injecting domain knowledge (e.g. on
that the use of specific models by Fv experts is not always clearly                                                  how current Fv algorithms are designed) significantly improves
motivated. In fact, the literature suggests that the Ml model is                                                     performances, it becomes meaningful to integrate it to relieve the
often selected among the set of those available in the Ml tool(s)                                                    Ml algorithms from struggling to learn specific aspects while al-
the authors are familiar with (e.g. the Weka Workbench [32]). This                                                   lowing them to focus on more global aspects of the problem. Our
is not incompatible with common practice: Ml experts often use                                                       survey points to that fact that the use of Ml for specific Fv tasks is
a trial-and-error approach to determine which model performs                                                         over-represented, at the expense of more recent holistic strategies.
best for a given task. Having bad performance with a specific Ml                                                         Such holistic strategies have already radically changed fields
model does not always imply that the model is not suited for the Ml                                                  such as image and natural language processing, especially after
task, but rather it is not optimally parameterized. It is sometimes                                                  the introduction of Deep Learning [37]. It became clear from our
impossible to figure out in advance which model will work best (as                                                   literature study that Fv tools that introduced Ml in their workings
                                                                                                               10
started to deliver impressive performances in international con-              problem that was previously manually handled, or not handled at
tests (e.g. [20, 64] in Tp; [63, 100] in Sat). However, using more            all; in others, this simply means no comparison is provided by the
powerful Ml models directly hampers the interpretability of their             authors.
results [12]. This is problematic for Fv, since its techniques are                Finally, the Ml model types presented in Table 2 have been
often used to ensure the correctness of safety-critical software for          gathered for informational purposes and not in an exhaustive way.
which human-understandable justifications need to be provided.                In this sense, the association between themes and Ml models does
We strongly call for a more systematic review of the domain in                not imply an exclusive relation of appropriateness between them.
order to precisely identify future directions in this research domain.
We believe machine learned Fv is potentially achievable when suf-
                                                                              7      CONCLUSION
ficient amounts of data will be collected, just like image analysis
for medical diagnostic [94], board game playing [89, 90] or even              In this paper, we have explored how Ml contributes to enhance Fv
self-driving cars [17, 18]. While a decade ago progress in such do-           tools efficiency. We covered four classical approaches, namely Sat,
mains seemed extremely difficult, it has now become reachable for             Theorem-Proving (Tp), Model-Checking (Mc), and Static Analysis
(state-of-the-art) Ml. Rather than following designs and abstrac-             (Sa), for which we catalog a list of themes, i.e. precise points where
tions created by humans, Ml may indeed find fresh new ways of                 an Fv problem is translated into an Ml task to be handled by an
handling Fv problems, opening the potential to entirely reshaping             Ml model type. Although preliminary, our survey shows not only
the Fv domain.                                                                that Ml may keep on contributing to the Fv field in both short and
                                                                              medium terms. It also shows that integrating Ml methods inside
                                                                              Fv tools is largely beneficial, as demonstrated in Sat and Tp tools
6   THREATS TO VALIDITY                                                       that regularly achieve new scales of efficiency. However it is still
Although we designed our search protocol in a very inclusive way,             essential to tackle challenges that were until recently thought as
as witnessed by the number of papers finally discarded manually,              unreachable (e.g. attacking realistic cryptography protocols like
we may have missed some relevant contributions. First, we relied              Rsa).
exclusively on repository search, whereas crossing searches with                 By studying the intricate relation between Fv and Ml over a
top-venues both in Fv and Ml may have brought new interesting                 large spectrum of approaches, we were able to frame the way Fv
contributions. Second, we stopped searching online repository after           and Ml experts collaborate in a classical Ml pipeline: identifying
10 result pages Third, we performed the search in September 2017,             the Fv problem (corresponding to our themes); determining the
before many important Fv, as well as Ml, venues take place. To                corresponding Ml task; providing Ml features; and figuring out
mitigate these points, we have conducted a backward snowballing               which Ml model type is the most adequate for the task. We also
on the main papers in each approach (typically, the most cited ones)          captured general trends, the most challenging being learning Fv
in January 2018, and looked at the program of some of the relevant            approaches on their own, as witnessed by many attempts in e.g.
top venues. In future revisions of our survey, we will integrate              Sat, Tp and Sa.
forward snowballing, as recommended by Wohlin [95], by looking                   The reverse direction of the love story has been left untouched,
a posteriori at top-venues in recent months.                                  despite a recent growing interest: how can Fv may help Ml. Veri-
    Furthermore, our survey is likely to have missed gaps in the              fying Ml tasks results has nowadays become a stepping stone in
literature, meaning that additional themes and/or better relations            the adoption of thrilling new technologies: for example, correctly
between themes, tasks and Ml models may surface in future work.               identifying road signs directly influences the behavior of self-driven
In fact, as research progresses in this area and Ml becomes more              cars, which in turns guarantees the safety of passengers. One of the
widely adopted, we expect to find new themes that are for the                 main reasons that make such verification hard is that the implicit
moment not explored by the community: this survey may well be                 models (e.g. neural networks, one of the currently most promising
seen as a current snapshot of the available contributions in the              learning technologies) are difficult to grasp and understand for
domain, rather than a definitive survey that closes the matter.               humans. Properly stating what kind of properties one expects from
    In Table 2, the information regarding state-of-the-art improve-           such implicit models is even more difficult. Building appropriate ab-
ments (noted as +/o/-) has been collected from each contribution              stractions of such models, that often integrate probabilistic and/or
relying solely on the article’s text. We have taken into account the          continuous computations is a key challenge. Therefore, specifying
comparisons with other tools operated by the authors, or analyzed             what models to accept appears to be difficult.
explicit statements from them on how their method/tool compare
to others. We have been particularly attentive to available data on           REFERENCES
relevance (precision and recall) and performance (speed). These                   [1] J. Alama, D. Kühlwein, E. Tsivtsivadze, J. Urban, and T. Heskes. Premise selection
comparisons found in the literature form a heterogeneous set: some                    for mathematics by corpus analysis and kernel methods. CoRR, 2011.
                                                                                  [2] A. A. Alemi, F. Chollet, G. Irving, C. Szegedy, and J. Urban. DeepMath — Deep
authors compare their work with solutions where no Ml is used,                        Sequence Models for Premise Selection. CoRR, 2016.
whereas others provide comparisons with Ml-based tools; datasets                  [3] R. Alur, P. Madhusudan, and W. Nam. Symbolic compositional verification by
                                                                                      learning assumptions. In Computer Aided Verification, pages 548–562, 2005.
which are used as the basis for learning are often small and have                 [4] N. Amla, X. Du, A. Kuehlmann, R. P. Kurshan, and K. L. McMillan. An Analysis
not been made available online, meaning reproducibility of the                        of SAT-Based Model Checking Techniques in an Industrial Environment. In Ad-
presented results is, in general, not possible. In some articles, no                  vanced Research Working Conference on Correct Hardware Design and Verification
                                                                                      Methods, 2005.
comparison with the state of the art is provided by the authors:                  [5] D. Angluin. Learning regular sets from queries and counterexamples. Informa-
in some instances, this means that the Ml technique addresses a                       tion and Computation, 75(2):87–106, 1987.
                                                                         11
 [6] C. Ansótegui, M. L. Bonet, J. Giráldez-Cru, and J. Levy. Structure features for              Testing, pages 312–325, 2009.
     sat instances classification. Journal of Applied Logic, 2016.                             [40] Q. Hanam, L. Tan, R. Holmes, and P. Lam. Finding patterns in static analysis
 [7] T. Araragi and S. Mo Cho. Checking liveness properties of concurrent systems                   alerts: Improving actionable alert ranking. In Mining Software Repositories,
     by reinforcement learning. In Model-Checking and Artificial Intelligent, 2006.                 pages 152–161, 2014.
 [8] D. Aspinall. Proof General: A Generic Tool for Proof Development. In TACAS,               [41] H. Hata, O. Mizuno, and T. Kikuno. An extension of fault-prone filtering using
     pages 38–43, Berlin, Heidelberg, 2000. Springer Berlin Heidelberg.                             precise training and a dynamic threshold. In Mining Software Repositories, pages
 [9] Z. Aung and W. Zaw. Permission-based android malware detection. International                  89–98, 2008.
     Journal of Scientific & Technology Research, 2(3):228–234, 2013.                          [42] S. Heckman and L. Williams. A model building process for identifying actionable
[10] H. Barringer, D. Giannakoupolou, and C. Pasareanu. Proof rules for automated                   static analysis alerts. In ICST, pages 161–170, 2009.
     compositional verification through learning. In Workshop on Specification And             [43] S. Heckman and L. Williams. A systematic literature review of actionable alert
     Verification of Component-Bases Systems, pages 14–21, 2003.                                    identification techniques for automated static code analysis. Information and
[11] R. Behjati, M. Sirjani, and M. N. Ahmadabadi. Bounded rational search for                      Software Technology, 53:363–387, 2011.
     on-the-fly model-checking of LTL properties. In FSE, 2009.                                [44] E. Horvitz, Y. Ruan, C. Gomes, H. Kautz, B. Selman, and M. Chickering. A
[12] A. Bibal and B. Frénay. Interpretability of machine learning models and repre-                bayesian approach to tackling hard computational problems. In Conference on
     sentations: an introduction. In Proc. ESANN, pages 77–82, 2016.                                Uncertainty and Artificial Intelligence, pages 235–244, 2001.
[13] A. Biere and A. Fröhlich. Evaluating CDCL Restart Schemes. In Pragmatics of              [45] J. Huang. The effect of restarts on the efficiency of clause learning. In Interna-
     SAT, 2015.                                                                                     tional Joint Conference on Artifical intelligence, pages 2318–2323, 2007.
[14] A. Biere, M. Heule, H. van Maaren, and T. Walsh, editors. Handbook of Satisfia-           [46] F. Hutter, Y. Hamadi, H. H. Hoos, and K. Leyton-Brown. Performance prediction
     bility, volume 185. IOS Press, 2009.                                                           and automated tuning of randomized and parametric algorithms. In Conference
[15] J. C. Blanchette, L. Bulwahn, and T. Nipkow. Automatic proof and disproof                      on Principles and Practice of Constraint Programming, 2006.
     in isabelle/hol. In International Symposium on Frontiers of Combining Systems,            [47] C. Kaliszyk and J. Urban. Learning-assisted automated reasoning with flyspeck.
     pages 12–27, 2011.                                                                             Journal of Automated Reasoning, 53(2):173–213, Aug 2014.
[16] J. C. Blanchette, D. Greenaway, C. Kaliszyk, D. Kühlwein, and J. Urban. A                [48] C. Kaliszyk, J. Urban, and J. Vyskocil. Machine learner for automated reasoning
     Learning-Based Fact Selector for Isabelle/HOL. Journal of Automated Reasoning,                 0.4 and 0.5. CoRR, abs/1402.2359, 2014.
     57(3):219–244, Oct 2016.                                                                  [49] C. Kaliszyk, J. Urban, and J. Vyskočil. Efficient semantic features for auto-
[17] D. Bojarski, Mariusz anf Del Testa, D. Dworakowski, B. Firner, B. Flepp, P. Goyal,             mated reasoning over large theories. In International Conference on Artificial
     L. D. Jackel, M. Monfort, U. Muller, J. Zhang, X. Zhang, J. Zhao, and K. Zieba.                Intelligence, pages 3084–3090, 2015.
     End to end learning for self-driving cars. Available at arXiv:1604.07316, 2016.           [50] H. Kautz, E. Horvitz, Y. Ruan, B. Selman, and C. Gomes. Dynamic randomized
[18] M. Bojarski, P. Yeres, A. Choromanaska, K. Choromanski, B. Firner, L. D. Jackel,               restarts: Optimal restart policies with observation. In American Association for
     and U. Muller. Explaining how a deep neural network trained with end-to-end                    Artificial Intelligence, 2002.
     learning steers a car. Available at arXiv:1704.07911, 2017.                               [51] S. Kim, E. J. J. Whitehead, and Y. Zhang. Classifying software changes: Clean
[19] J. Bridge. Machine Learning and Automated Theorem Proving. PhD thesis,                         or buggy? IEEE Transactions on Software Engineering, 34(2):181–196, 2008.
     University of Cambridge, 2010.                                                            [52] B. Kitchenham. Guidelines for performing Systematic Literature Reviews in
[20] J. Bridge, S. Holden, and L. Paulson. Machine Learning for First-Order Theorem                 Software Engineering. Technical report, University of Durheim and Keele
     Proving – Learning to Select a Good Heuristic. Journal of Automated Reasoning,                 University, 2007.
     53(2):141–172, Aug 2014.                                                                  [53] E. Komendantskaya, J. Heras, and G. Grov. Machine learning in proof general:
[21] S. Chaki, E. Clarke, N. Sinha, and P. Thati. Automated assume-guarantee                        Interfacing interfaces. In International Workshop On User Interfaces for Theorem
     reasoning for simulation conformance. In CAV, pages 534–547, 2005.                             Provers, pages 15–41, 2012.
[22] T. Chappelly, C. Cifuentes, P. Krishnan, and S. Gevay. Machine learning for find-         [54] T. Kremenek, K. Ashcraft, J. Yang, and D. Engler. Correlation exploitation in
     ing bugs: An initial report. In IEEE Workshop on Machine Learning Techniques                   error ranking. In Foundations of Software Engineering, 2004.
     for Software Quality Evaluation, 2017.                                                    [55] D. Kühlwein, J. C. Blanchette, C. Kaliszyk, and J. Urban. MaSh: Machine
[23] E. Clarke, A. Gupta, and O. Strichman. SAT-Based Counterexample Guided Ab-                     Learning for Sledgehammer. In Proceedings of the 4th International Conference
     straction Refinement. IEEE Transactions on Computer-Aided Design of Integrated                 on Interactive Theorem Proving, ITP’13, pages 35–50, Berlin, Heidelberg, 2013.
     Circuits and Systems, 23(7):1113–1123, 2004.                                                   Springer-Verlag.
[24] E. M. Clarke, E. A. Emerson, and A. P. Sistla. Automatic verification of finite-          [56] D. Kühlwein and J. Urban. Males: A framework for automatic tuning of auto-
     state concurrent systems using temporal logic specifications. ACM Transactions                 mated theorem provers. Journal of Automated Reasoning, 55(2):91–116, 2015.
     on Programming Languages and Systems, 8(2):244–263, 1986.                                 [57] D. Kühlwein, T. van Laarhoven, E. Tsivtsivadze, J. Urban, and T. Heskes.
[25] E. M. Clarke, A. Gupta, J. Kukula, and O. Strichman. SAT-Based Abstraction-                    Overview and evaluation of premise selection techniques for large theory
     Refinement Using ILP and Machine Learning Techniques. In Computer Aided                        mathematics. In International Joint Conference on Automated Reasoning, pages
     Verification, pages 265–279, 2002.                                                             378–392, 2012.
[26] E. M. Clarke and J. M. e. Wing. Formal methods: State of the art and future               [58] M. G. Lagoudakis and M. L. Littman. Learning to select branching rules in
     directions. ACM Computing Surveys, 28(4):626–643, 1996.                                        the dpll procedure for satisfiability. Electronic Notes in Discrete Mathematics,
[27] J. M. Cobleigh, D. Giannakopoulou, and C. S. Pasareanu. Learning assumptions                   9:344–359, 2001.
     for compositional verification. In TACAS, pages 331–346, 2003.                            [59] K. Leyton-Brown, E. Nudelman, G. Andrew, J. McFadden, and Y. Shoham. A
[28] P. Cousot and R. Cousot. A Gentle Introduction to Formal Verification of                       portfolio approach to algorithm selection. In IJCAI, pages 1542–1563, 2003.
     Computer Systems by Abstract Interpretation. In Logics and Languages for                  [60] J. H. Liang, V. Ganesh, P. Poupart, and K. Czarnecki. Exponential recency
     Reliability and Security, pages 1–29. IOS Press, 2010.                                         weighted average branching heuristic for SAT solvers. In ICAI, 2016.
[29] D. Devlin and B. O’Sullivan. Satisfiability as a classification problem. In Irish         [61] J. H. Liang, V. Ganesh, P. Poupart, and K. Czarnecki. Learning rate based
     Conference on Artificial Intelligence and Cognitive Science, 2008.                             branching heuristic for SAT solvers. In International Conference on Theory and
[30] H. Duncan, A. Bundy, J. Levine, A. Storkey, and M. Pollet. The use of data-mining              Applications of Satisfiability Testing, pages 123–140, 2016.
     for the automatic formation of tactics. In Proceedings of Computer-Supported              [62] J. H. Liang, H. Govind, P. Poupart, K. Czarnecki, and V. Ganesh. An empirical
     Mathematical Theory Development, 2004.                                                         study of branching heuristics through the lens of global learning rate. In Theory
[31] A. Elizabeth, M. Alan, B. H. Duncan, and D. Aspinall. PG Tips: A Recommender                   and Applications of Satisfiability Testing (SAT), 2017.
     System for an Interactive Theorem Prover, 2006.                                           [63] M. Lindauer, H. H. Hoos, F. Hutter, and T. Schaub. Autofolio: An automatically
[32] E. Frank, M. A. Hall, and I. H. Witten. The WEKA Workbench. Morgan Kaufmann,                   configured algorithm selector. JAIR, 53(1):745–778, 2015.
     2016.                                                                                     [64] S. M. Loos, G. Irving, C. Szegedy, and C. Kaliszyk. Deep network guided proof
[33] A. Frohlich, A. Biere, C. Wintersteiger, and Y. A. . Hamadi. Stochastic local                  search. CoRR, abs/1701.06972, 2017.
     searchf or satisfiability modulo theories. In AAAI, pages 1136–1143, 2015.                [65] S. Lu, S. Park, E. Seo, and Y. Zhou. Learning from mistakes: A comprehensive
[34] M. Fuchs. A Feature-based Learning Method for Theorem Proving. American                        study on real world concurrency bug characteristics. In Architectural Support
     Association for Artificial Intelligence, 1998.                                                 for Programming Languages and Operating Systems, pages 329–339, 2008.
[35] M. Gagliolo and J. Schmidhuber. Learning restart strategies. In International             [66] M. Luby, A. Sinclair, and D. Zuckerman. Optimal speedup of las vegas algorithms.
     Joint Conference on Artifical intelligence, 2007.                                              In Israeli Symposium on the Theory and Computing Systems, 1993.
[36] M. Gheorghiu, D. Giannakopoulou, and C. S. Pasareanu. Refining interface                  [67] T. M. Mitchell. Machine Learning. McGraw-Hill, 1997.
     alphabets for compositional verification. In TACAS, pages 292–307, 2007.                  [68] mboxThe Coq development team. The Coq proof assistant reference manual.
[37] I. Goodfellow, Y. Bengio, and A. Courville. Deep Learning. MIT Press, 2016.                    LogiCal Project, 2009.
[38] A. Grabowski, A. Kornilowicz, and A. Naumowicz. Mizar in a nutshell. Journal              [69] J. Meng and L. C. Paulson. Lightweight relevance filtering for machine-
     of Formalized Reasoning, 3(2):153–245, 2010.                                                   generated resolution problems. Journal of Applied Logic, 7(1):41 – 57, 2009.
[39] S. Haim and T. Walsh. Restart strategy selection using machine learning tech-
     niques. In International Conference on Theory and Applications of Satisfiability
                                                                                          12
[70] L. Mou, G. Li, L. Zhang, T. Wang, and Z. Jin. Convolutional Neural Networks                [88] S. Shivaji, J. Whitehead, R. Akella, and S. Kim. Reducing features to improve
     over Tree Structures for Programming Language Processing. In Conference on                      code change based bug prediction. IEEE Transactions on Software Engineering,
     Artificial Intelligence, pages 1287–1293, 2016.                                                 39(4):552–569, 2013.
[71] T. Muske and A. Serebrenik. Survey of approaches for handling static analysis              [89] D. Silver, A. Huang, C. J. Maddison, A. Guez, and L. e. a. Sifre. Mastering the
     alarms. In Source Code Analysis and Manipulation, 2016.                                         game of go with deep neural networks and tree search. Nature, 529(7587):484–
[72] W. Nam and R. Alur. Learning-based symbolic assume-guarantee reasoning                          489, 2016.
     with automatic decomposition. In ATVA, pages 170–185, 2006.                                [90] D. Silver, T. Hubert, J. Schrittwieser, I. Antonoglou, and M. e. a. Lai. Mastering
[73] H. V. Nath and B. M. Mehtre. Static malware analysis using machine learning                     chess and shogi by self-play with a general reinforcement learning algorithm.
     methods. In International Conference on Security in Computer Networks and                       arXiv:1712.01815, 2017.
     Distributed Systems, pages 440–450, 2014.                                                  [91] N. Sinha and E. M. Clarke. Sat-based compositional verification using lazy
[74] S. Nejati, J. H. Liang, V. Ganesh, C. H. Gebotys, and K. Czarnecki. Adaptive                    learning. In Conference on Computer Aided Verification, pages 39–54, 2007.
     restart and cegar-based solver for inverting cryptographic hash functions. In              [92] R. S. Sutton and A. G. Barto. Reinforcement learning: An introduction. MIT Press,
     Verified Software: Theories, Tools, and Experiments, pages 120–131, 2017.                       1998.
[75] C. S. Pasareanu, D. Giannakopoulou, M. Gheorghiu Bobaru, J. M. Cobleigh,                   [93] J. Urban. MizarMode – An Integrated Proof Assistance Tool for the Mizar way
     and H. Barringer. Learning to divide-and-conquer: Applying the l ∗ algorithm                    of Formalizing Mathematics. Journal of Applied Logic, 4(4):414 – 427, 2006.
     to automate assume-guarantee reasoning. Formal Methods in System Design,                   [94] D. S. Wei Ting, C. Y.-L. Cheung, and G. Lim. Development and validation of a
     32(3):175–205, 2008.                                                                            deep learning system for diabetic retinopathy and related eye diseases using
[76] E. Pira, V. Rafe, and A. Nikanjam. Emcdm: Efficient model checking by data min-                 retinal images from multiethnic populations with diabetes. Journal of American
     ing for verification of complex software systems specified through architectural                Medical Association, 318(22):2211–2223, 2017.
     styles. Applied Soft Computing, 49:1185–1201, 2016.                                        [95] C. Wohlin. Guidelines for snowballing in systematic literature studies and a
[77] M. R. Prasad, A. Biere, and A. Gupta. A Survey of Recent Advances in SAT-Based                  replication in software engineering. In Proceedings of the 18th International
     Formal Verification. STTT Journal, 7(2):156–173, 2005.                                          Conference on Evaluation and Assessment in Software Engineering (EASE), pages
[78] J.-P. Queille and J. Sifakis. Specification and Verification of Concurrent Systems              38:1–38:10, 2014.
     in CESAR. In International Symposium on Programming, pages 337–351, 1982.                  [96] D. Wolpert and W. MacReady. No free lunch theorems for optimization. IEEE
[79] R. L. Rivest and R. E. Schapire. Inference of finite automata using homing                      Transactions on Evolutionary Computation, 1(1):67–82, 1997.
     sequences. Information and Computation, 103(2):299–347, 1993.                              [97] H. Wu. Improving SAT solving with machine learning. In ACM SIGCSE Technical
[80] T. Rocktäschel and S. Riedel. End-to-end differentiable proving. Neural Infor-                 Symposium on Computer Science Education, pages 787–788, 2017.
     mation Processing Systems, 2017.                                                           [98] L. Xu, H. H. Hoos, and K. Leyton-Brown. Hierarchical hardness models for SAT.
[81] Y. Ruan, E. Horvitz, and H. Kautz. Restart policies with dependence among runs:                 In Conference on Principles and Practice of Constraint Programming, 2007.
     A dynamic programming approach. In Conference on Principles and Practice of                [99] L. Xu, H. H. Hoos, and K. Leyton-Brown. Predicting satisfiability at the phase
     Constraint Programming, pages 573–586, 2002.                                                    transition. In ICAI, pages 584–590, 2012.
[82] N. Rungta and E. G. Mercer. Hardness for explicit state software model checking           [100] L. Xu, F. Hutter, H. H. Hoos, and K. Leyton-Brown. Satzilla: Portfolio-based
     benchmarks. In Software Engineering and Formal Methods, pages 247–256, 2007.                    algorithm selection for sat. JAIR, 32:565–606, 2008.
[83] J. Ruthruff, J. Penix, J. D. Morgenthaler, S. Elbaum, and G. Rothermel. Predicting        [101] F. Yamaguchi, M. Lottmann, and K. Rieck. Generalized Vulnerability Extrapo-
     accurate and actionablestatic analysis warnings: An experimental approach. In                   lation using Abstract Syntax Trees. In Annual Computer Security Applications
     International Conference on Software Engineering, pages 341–350, 2008.                          Conference, pages 359–368, 2012.
[84] J. Sahs and L. Khan. A machine learning approach to android malware detection.            [102] S. Y. Yerima, S. Sezer, and I. Muttik. Analysis of bayesian classification-based
     In Intelligence and Security Informatics Conference, pages 141–147, 2012.                       approaches for android malware detection. IET Information Security, 8(1):25–36,
[85] H. Samulowitz and R. Memisevic. Learning to solve qantified boolean formulas.                   2014.
     In ICAI, pages 255–260, 2007.                                                             [103] S. Y. Yerima, S. Sezer, and I. Muttik. Android malware detection using parallel
[86] S. Schulz. E – A Brainiac Theorem Prover. Journal of AI Communications,                         machine learning classifiers. In Next Generation Mobile Apps, Services and
     15(2/3):111–126, 2002.                                                                          Technologies, 2014.
[87] D. Selsam, M. Lamm, B. Bunz, P. Liang, L. de Moura, and D. Dill. Learning a sat           [104] S. Y. Yerima, S. Sezer, and I. Muttik. Android malware detection: An eigenspace
     solver from single-bit supervision. Technical report, Stanford University, 2018.                analysis approach. In Science and Information Conference, pages 1236–1242,
                                                                                                     2015.




                                                                                          13
