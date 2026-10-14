                                            PaMpeR: Proof Method Recommendation System
                                                          for Isabelle/HOL
                                                                        Yutaka Nagashima                                                    Yilun He
                                                CIIRC, Czech Technical University in Prague, Czech Republic                    School of Information Technologies
                                               Department of Computer Science, University of Innsbruck, Austria               University of Sydney, Sydney, Australia
                                                             Email: yutaka.nagashima@uibk.ac.at                                Email: yihe8397@uni.sydney.edu.au



                                            Abstract—Deciding which sub-tool to use for a given proof state        it is possible to advise which proof methods are
arXiv:1806.07239v1 [cs.LO] 19 Jun 2018




                                         requires expertise specific to each ITP. To mitigate this problem,        useful to a given proof state, based only on the meta-
                                         we present PaMpeR, a proof method recommendation system for               information about the state and information in the
                                         Isabelle/HOL. Given a proof state, PaMpeR recommends proof
                                         methods to discharge the proof goal and provides qualitative              standard library. Furthermore, we can extract advice
                                         explanations as to why it suggests these methods. PaMpeR                  by applying machine learning algorithms to existing
                                         generates these recommendations based on existing hand-written            large proof corpora.
                                         proof corpora, thus transferring experienced users’ expertise to
                                                                                                              The paper is organized as follows: Section II explains the
                                         new users. Our evaluation shows that PaMpeR correctly predicts
                                         experienced users’ proof methods invocation especially when it       basics of Isabelle/HOL and provides the overview of PaMpeR.
                                         comes to special purpose proof methods.                              Section III expounds how PaMpeR transforms the complex
                                                                                                              data structures representing proof states to simple data struc-
                                                                 I. I NTRODUCTION
                                                                                                              tures that are easier to handle for machine learning algo-
                                            Do you know when to use the proof method called                   rithms. Section IV shows how our machine learning algorithm
                                         intro_classes in Isabelle? What about uint_arith?                    constructs regression trees from these simple data structures.
                                         Can you tell when fastforce tends to be more powerful                Section V demonstrates how users can elicit recommendations
                                         than auto? If you are an Isabelle expert, your answer is             from PaMpeR. Section VI presents our extensive evaluation
                                         “Sure.” But if you are new to Isabelle, your answer might            of PaMpeR to assess the accuracy of PaMpeR’s recommen-
                                         be “No. Do I have to know these Isabelle specific details?”          dations. Section VII discusses the strengths and limitations of
                                            Interactive theorem provers (ITPs) are forming the basis          the current implementation and the design of a proof search
                                         of reliable software engineering. Klein et al. proved the cor-       tool based on PaMpeR. Section VIII compares our work with
                                         rectness of the seL4 micro-kernel in Isabelle/HOL [2]. Leroy         other attempts of applying machine learning and data mining
                                         developed a certifying C compiler, CompCert, using Coq [3].          to interactive theorem proving.
                                         Kumar et al. built a verified compiler for a functional pro-
                                         gramming language, CakeML, in HOL4 [4]. In mathematics,                    II. BACKGROUND AND OVERVIEW OF P A M P E R
                                         mathematicians are replacing their pen-and-paper proofs with
                                                                                                              A. Background
                                         mechanised proofs to avoid human-errors in their proofs: Hales
                                         et al. mechanically proved the Kepler conjecture using HOL-             Isabelle/HOL is an interactive theorem prover, mostly writ-
                                         light and Isabelle/HOL [5], whereas Gonthier et al. finished         ten in Standard ML. The consistency of Isabelle/HOL is
                                         the formal proofs of the four colour theorem in Coq [6]. In          carefully protected by isolating its logical kernel using the
                                         theoretical computer science, Thiemann et al. formalized term        module system of Standard ML. Isabelle/Isar [19] (Isar for
                                         rewriting system using Isabelle/HOL [7], and Paulson proved          short) is a proof language used in Isabelle/HOL. Isar provides
                                         Gödel’s incompleteness theorems using Nominal Isabelle [8].         a human-friendly interface to specify and discharge proof
                                            To facilitate efficient proof developments in such large scale    goals. Isabelle users discharge proof goals by applying proof
                                         verification projects, modern ITPs are equipped with many            methods, which are the Isar syntactic layer of LCF-style
                                         sub-tools, such as proof methods and tactics. For example,           tactics.
                                         Isabelle/HOL comes with 159 proof methods defined in its                Each proof goal in Isabelle/HOL is stored within a proof
                                         standard library. These sub-tools provide useful automation          state, which also contains locally bound theorems for proof
                                         for interactive theorem proving; however, it still requires          methods (chained facts) and the background proof context of
                                         ITP specific expertise to pick up the right proof method to          the proof goal, which includes local assumptions, auxiliary
                                         discharge a given proof goal.                                        definitions, and lemmas proved prior to the the current step.
                                            This paper presents our novel approach to proof method            Proof methods are in general sensitive not only to proof goals
                                         recommendation and its implementation, PaMpeR. The imple-            but also to their chained facts and background proof contexts:
                                         mentation is available at GitHub [21]. Our research hypothesis       they behave differently based on information stored in proof
                                         is that:                                                             state. Therefore, when users decide which proof method to
apply to a proof goal, they often have to take other information   to conclude a proof attempt.
in the proof state into consideration.                                Isabelle provides a plethora of proof methods, which serves
   Isabelle comes with many Isar keywords to define new            as ammunitions when used by experienced Isabelle users;
types and constants, such as datatype, codatatype,                 However, new Isabelle users sometimes spend hours or days
primrec, primcorec, inductive, and definition.                     trying to prove goals using proof methods sub-optimal to their
For example, the fun command is used for general recursive         problems without knowing Isabelle has already specialized
definitions.                                                       methods that are optimized for their goals.
   These keywords not only let users define new types or
constants, but they also automatically derive auxiliary lemmas     B. Overview of PaMpeR
relevant to the defined objects behind the user-interface and         Figure 1 illustrates the overview of PaMpeR. The system
register them in the background proof context where each           consists of two phases: the upper half of the figure shows
keyword is used. For example, Nipkow et al. defined a              PaMpeR’s preparation phase, and the lower half shows its
function, sep, using the fun keyword in an old Isabelle            recommendation phase.
tutorial [1] as follows:
                                                                      In the preparation phase, PaMpeR’s feature extractor con-
fun sep::"’a => ’a list => ’a list" where                          verts the proof states in existing proof corpora such as the
"sep a [ ]      = [ ]" |                                           Archive of Formal Proofs (AFP) [15] into a database. This
"sep a [x]      = [x]" |                                           database describes which proof methods have been applied
"sep a (x#y#zs) = x # a # sep a (y#zs)"                            to what kind of proof state, while abstracting proof states as
                                                                   arrays of boolean values. This abstraction is a many-to-one
   Intuitively, this function inserts the first argument between
                                                                   mapping: it may map multiple distinct proof states into to the
any two elements in the second argument. Following this def-
                                                                   same array of boolean values. Therefore, each array represents
inition, Isabelle automatically derives the following auxiliary
                                                                   a group of proof states sharing certain properties.
lemma, sep.induct, and registers it in the background
                                                                      PaMpeR first preprocesses this database and generates a
proof context as well as other four automatically derived
                                                                   database for each proof method. Then, PaMpeR applies a
lemmas:
                                                                   regression algorithm to each database and creates a regression
sep.induct: (!!a. ?P a [])                                         tree for each proof method. This regression algorithm attempts
  ==> (!!a x. ?P a [x])                                            to discover combinations of features useful to recommend
  ==> (!!a x y zs. ?P a (y # zs)                                   which proof method to apply. Each tree corresponds to a
  ==> ?P a (x # y # zs))                                           certain proof method, and each node in a tree corresponds
  ==> ?P ?a0.0 ?a1.0                                               to a group of proof states, and the value tagged to each leaf
                                                                   node shows how likely it is that the method represented by
where variables prefixed with ? are schematic variables, !!
                                                                   the tree is applied to these proof states according to the proof
is the meta-logic universal quantifier, ==> is the meta-logic
                                                                   corpora used as training sample.
implication. Isabelle also attaches unique names to these
                                                                      For the recommendation phase, PaMpeR offers three
automatically derived lemmas following certain naming con-
                                                                   commands,        which_method,           why_method,         and
ventions hard-coded in Isabelle’s source code. In this example,
                                                                   rank_method. The which_method command first
the full name of this lemma is fun0.sep.induct, which
                                                                   abstracts the state into a vector of boolean values using
is a concatenation of the theory name (fun0), the delimiter
                                                                   PaMpeR’s feature extractor. Then, PaMpeR looks up
(.), the name of the constant defined (sep), followed by a
                                                                   the regression trees and presents its recommendations in
hard-coded postfix (.induct), which represents the kind of
                                                                   Isabelle/jEdit’s output panel. If you wonder why PaMpeR
this derived lemma.
                                                                   recommends certain methods, for example auto, to your
   When users want to prove conjectures about sep, they can
                                                                   proof state, type why_method auto. Then, PaMpeR
specify their conjectures using Isar keywords such as lemma
                                                                   tells you why it recommended auto to the proof state
and theorem. The Isar commands, apply and by, allow
                                                                   in jEdit’s output panel. If you are curious how PaMpeR
users to apply proof methods to these proof goals. In the
                                                                   ranks a certain method, let us say intro_classes, type
above example, Nipkow et al. proved the following lemma
                                                                   rank_method intro_classes. This command shows
about map and sep using the automatically derived auxiliary
                                                                   intro_classes’s rank given by PaMpeR in comparison
lemma, sep.induct, as an argument to the proof method
                                                                   to other proof methods. In the following, we describe these
induct_tac as following:
                                                                   steps in detail.
lemma
"map f (sep x xs) = sep (f x) (map f xs)"                                  III. P ROCESSING L ARGE P ROOF C ORPORA
 apply(induct_tac x xs rule: sep.induct)
                                                                      The key component of PaMpeR is its feature extractor:
 apply simp_all done
                                                                   the extractor converts proof goals, chained facts, and proof
where simp_all is a proof method that executes simplifica-         contexts into arrays of boolean values by applying assertions
tion to all sub-goals and done is another Isar command used        to them.
                                                        full feature extractor             database
                 preparation phase
                           large proof corpora




                                                                                                 preprocess




                                                                                                 decision tree construction




                 recommendation phase                 fast feature extractor         feature vector


                                proof
                           ? state
                                                                                                                lookup
                                proof
                               engineer                                     proof method
                                                                          recommendation




                                                 Fig. 1: Proof attempt with PaMpeR.


A. Representing a Proof State as an Array of Boolean Values                We wrote some assertions to reflect our own expertise
   Currently we employ 108 assertions manually written in               in Isabelle/HOL. One example is the assertion that checks
Isabelle’s implementation language, Standard ML, based on               if the proof goal or chained facts involve the constant,
our expertise in Isabelle/HOL. Table I shows selected as-               Filter.eventually, defined in Isabelle’s standard li-
sertions we used in PaMpeR. Most of these assertions fall               brary. We developed such an assertion because we knew that
into two categories: assertions about proof goals themselves,           the proof method called eventually_elim can handle
and assertions about the relation between proof goals and               many proof goals involving this constant. But in some cases
information stored in the corresponding proof context.                  we were not sure which assertion can be useful to decide which
                                                                        method to use. For example, we have assertions to check if
   Note that PaMpeR’s assertions do not directly rely on any
                                                                        a proof goal has constants defined in Set.thy, Int.thy,
user-defined constants because PaMpeR’s developers cannot
                                                                        or List.thy as these theory files define commonly used
access concrete definitions of user-defined constants when
                                                                        concepts in theorem proving. But their effects to proof method
developing PaMpeR. For example, we can check if the first
                                                                        selection were unclear until we conducted an extensive eval-
proof goal has a constant defined in the Set.thy file in
                                                                        uation described in Section VI.
Isabelle/HOL, but we cannot check if that sub-goal has a
constant defined in the proof script that some user developed              More importantly, we did not know numerical estimates on
after we released PaMpeR.                                               which assertion is more useful than others when developing
   However, by investigating how Isabelle/HOL works, we                 these assertions. For instance, we guessed that the assertion
implemented assertions that can check the meta-information of           to check the use of the constant Filter.eventually to
proof goal even without knowing their concrete specifications           be useful to recommend the use of the eventually_elim
when developing PaMpeR. For example, the lemma presented                method, but we did not have means of comparing the accuracy
in Section II-A has a function, sep, which was defined                  of this guess with other hints prior to this project. To obtain
with the fun keyword. PaMpeR’s feature extractor checks                 numerical assessments for proof method prediction, we applied
if the underlying proof context contains a lemma of name                the multi-output regression algorithm described in Section IV.
sep.elims. If the context has such a lemma, PaMpeR infers                  The evaluation in Section VI corroborates that it is possible
that a user defined sep using either the fun keyword or                 to derive meaningful advice about proof methods. This implies
the function keyword, rather than other keywords such as                that some parts of the expertise necessary to select appropriate
primcorec or definition.                                                proof methods are based on the meta-information about proof
  •   Assertions about proof goals themselves.
        – constants defined in Isabelle’s standard library
           ∗ check if the first goal has the BNF_Def.rel_fun constant or the Fun.map_fun constant.
           ∗ check if the first goal has Orderings.ord_class.less_eq, Orderings.ord_class.less, or Groups.plus_class.plus.
           ∗ check if the fist goal and its chained facts have Filter.eventually
        – constants defined in Isabelle’s standard library at certain locations in the first proof goal
           ∗ check if the outermost constant of the first goal is the meta-logic universal quantifier
           ∗ check if the first goal has the HOL existential quantifier but not as the outermost constant
        – terms of certain types defined in Isabelle’s standard library
           ∗ check if the first goal has a term of type Word.word
           ∗ check if the first goal has a schematic variable
        – existence of constants defined in certain theory files
           ∗ check if the first goal has a constant defined in the Nat theory
           ∗ check if the first goal has a constant defined in the Real theory
           ∗ check if the first goal has a constant defined in the Set theory
  •   Assertions about the relation between proof goals and proof contexts.
        – types defined with a certain Isar keyword
           ∗ check if the goal has a term of a type defined with the datatype keyword
           ∗ check if the goal has a term of a type defined with the codatatype keyword
           ∗ check if the goal has a term of a type defined with the record keyword
        – constants defined with a certain Isar keyword
           ∗ check if the goal has a constant defined with the lift_definition keyword
           ∗ check if the goal has a constant defined with the primcorec keyword
           ∗ check if the goal has a constant defined with the inductive keyword or inductive_set keyword.

                                                  TABLE I: Selected Assertions.


states or the information available within Isabelle’s standard      users choose to use the off-the-shelf default learning results,
library, and our assertion-based feature extractor preserves        they can use PaMpeR without ever modifying Isabelle’s source
some essence of proof states while converting them into             code. In that case, they only have to include the theory file
simpler format.                                                     PaMpeR/PaMpeR.thy into their own theory file using the
                                                                    Isar keyword import just as a normal theory file to use
B. Database Extraction from Large Proof Corpora                     PaMpeR.
   The first step of the preparation phase is to build a database      Note that logging mechanism ignores the apply commands
from existing proof corpora. We modified the proof method           that contain composite proof methods to avoid data pollution.
application commands, apply and by, in Isabelle and im-             When multiple proof methods are combined within a single
plemented a logging mechanism to build the database. The            command, the naive logging approach would record proof
modified apply and by take the following steps to generate          steps that are backtracked to produce the final result.
the database:                                                          One exemplary data point in an extracted database would
   1) apply assertions to the current proof state,                  look as the following:
   2) represent the proof state as an array of boolean values,      induct, [1,0,0,1,0,0,0,0,1,0,0,1,0,...]
   3) record which method is used to that array,
   4) apply the method as the standard apply or by com-             where induct is the name of method applied to this proof
       mand, accordingly.                                           state and the nth element in the list shows the result of the
This step requires a slight modification to the Isabelle source     nth assertion of the feature extractor when applied to the proof
code to allow us to overwrite the definition of these command.      state.
This way, we build its database by running the target proof            The default database construction from Isabelle standard
scripts.                                                            library and the AFP took about 6021 hours 43 minutes of CPU
   The current version of PaMpeR available at our website           time, producing a database consisting of 425334 unique data
[21] is based on the database extracted from Isabelle’s standard    points. We used three multi-core server machines1 to reduce
library and the AFP, but the database extraction mechanism is       the clock time necessary to obtain this dataset. Unfortunately,
not specific to this library. In case users prefer to optimise      this database is heavily imbalanced: some proof methods are
PaMpeR’s recommendation for their own proof scripts, they           used far more often than others. We discuss how this imbal-
can take the same approach following the instructions at            ance influenced the quality of PaMpeR’s recommendation in
our website [21], even though this process tends to require         Section VI.
significant computational resources.
                                                                       1 One of them has 2 Intel(R) Xeon(R) CPUs E5-2698 v3 @ 2.30GHz
   This overwriting of apply and by is the only modification
                                                                    with 16 cores for each and with hyperthreading, the other two have 2
we made to Isabelle’s source code, and we did so only to build      Intel(R) Xeon(R) CPUs E5-2690 v4 @ 2.60GHz with 14 cores for each with
the database for our machine learning algorithm. As long as         hyperthreading.
           IV. M ACHINE L EARNING DATABASES                            For this reason, this preprocessing may misjudge some
                                                                    methods to be inappropriate to a proof state represented by
   In this section, we explain the multi-output regression tree
                                                                    a feature vector in some cases. Unfortunately, exploring all
construction algorithm we implemented in Standard ML for
                                                                    the possible combinations of proof methods for each case is
PaMpeR. We chose a multi-output algorithm because there
                                                                    computational infeasible: some proof methods work well only
are in general multiple valid proof methods for each proof
                                                                    when they are followed by other proof methods or they are
goal, and we chose a regression algorithm rather than classifi-
                                                                    applied with certain arguments, and the combination of these
cation algorithm because we would like to provide numerical
                                                                    proof methods and arguments explodes quickly.
estimates about how likely each method would be useful to
                                                                       On the other hand, we can reasonably expect that the proof
a given proof goal. We chose a regression tree construction
                                                                    method appearing in our training sample is the right choice to
algorithm [22] because this simple algorithm allows us to pro-
                                                                    the proof state represented by the feature vector, since Isabelle
duce qualitative explanations as to why PaMpeR recommends
                                                                    mechanically checks the proof scripts. Furthermore, we built
certain methods and it works well for small datasets for rarely
                                                                    the default recommendation using Isabelle’s standard library,
used methods as shown in Section VI; However, it might be
                                                                    which was developed by experienced Isabelle developers, and
possible that more advanced machine learning algorithms can
                                                                    the AFP, which accepts new proofs only after peer reviews by
result in more accurate recommendations. The comparisons
                                                                    Isabelle experts. This allowed us to avoid low quality proof
of various machine learning algorithms remain as our future
                                                                    scripts that Isabelle can merely process but are inappropriate.
work.
                                                                    Therefore, we consider the approximation PaMpeR’s prepro-
                                                                    cessor makes to be a realistic point of compromise and show
A. Preprocess the Database
                                                                    the effectiveness of this approach in Section VI.
   We first preprocess the database generated in Section III-B.
This process produces a separate database for each proof            B. Regression Tree Construction
method from the raw database, which describes the use of
                                                                       After preprocessing, we apply our regression tree con-
all proof methods appearing in the target proof corpora.
                                                                    struction algorithm to each created database separately. We
   Among the class of problem transformation methods for
                                                                    implemented our tree construction algorithm from scratch in
multi-output regression problems, this straightforward ap-
                                                                    Standard ML for better flexibility and tool integration.
proach is called single-target method: it first transforms a sin-
                                                                       In general, the goal of the regression tree construction is
gle multi-output problem into several single-target problems,
                                                                    to partition the feature space described in each database into
then applies a regression algorithm to each of them separately,
                                                                    partitions of sub-spaces that lead to the minimal Residual Sum
then combines the results of each regression algorithm to build
                                                                    of Squares (RSS) 2 while avoiding over-fitting. Intuitively, RSS
a single predictor for the original multi-output problem.
                                                                    denotes the discrepancy between the data and estimation based
   For example, if our preprocessor finds the example
                                                                    on a model. The RSS in our problem is defined as follows:
line discussed in Section III-B, it considers that an ideal
user represented by the proof corpora decided to use the                                     J X
                                                                                             X
induct method but not other methods, such as auto                                  RSS =                         d R )2
                                                                                                       (usedi − used               (1)
                                                                                                                     j
or coinduction, and produces the following line in the                                       j=1i∈Rj
database for induct:
                                                                    where Rj stands for the jth sub-space, to which certain data
used, [1,0,0,1,0,0,0,0,1,0,0,1,0,...]                               points (represented as lines in database) belong. The value of
And the preprocessor adds the following line in the databases       usedi is 1.0 if the data point represented by the subscript i
for other proof methods appearing in the proof corpora:             says the method was applied to the feature vector, and it is 0.0
                                                                    if the data point represented by the subscript i says otherwise.
not, [1,0,0,1,0,0,0,0,1,0,0,1,0,...]                                used
                                                                     d R is the average value of used among the data points
                                                                           j
                                                                    pertaining to the sub-space Rj .
   Note that the resulting databases do not always represent
                                                                       Computing the RSS for every possible partition of the
a provably correct choice of proof methods but conservative
                                                                    database under consideration is computational infeasible.
estimates. In principle, there could be multiple equally valid
                                                                    Therefore, PaMpeR’s tree construction takes a top-down,
proof methods for a single proof state, but existing proof
                                                                    greedy approach, called recursive binary splitting [10].
corpora describe only one way of attacking it. For example,
Nipkow et al. applied the induct_tac method to the lemma               In recursive binary splitting, we start constructing the re-
in Section II-A, but we can prove this lemma with another           gression tree from the root node, which corresponds to the
method for mathematical induction (induction) as follows:           entire dataset for a given method. First, we select a feature
                                                                    in such a way we can achieve the greatest reduction in RSS
lemma                                                               at this particular step. We find such feature by computing the
 "map f (sep x xs) = sep (f x) (map f xs)"                          reduction of the RSS by each feature by one level. For each
 apply(induction x xs rule: sep.induct)
 apply simp_all done                                                  2 RSS is also known as the sum of squared residuals (SSR).
feature, we split the database into two sub-spaces, Rused (j)      assertions are not useful, by checking which features are used
and Rnot (j) as follows:                                           to branch each regression tree.
                                                                      The build_fast_feature_extractor command in
            Rused (j) = {used|usedj = 1.0} and
                                                             (2)   PaMpeR/PaMpeR.thy constructs a faster feature extractor
            Rnot (j) = {used|usedj = 0.0}                          from the regression trees built in the preparation phase and the
where j stands for the number representing each feature. Then,     full feature extractor to reduce the waiting time of PaMpeR’s
for each feature represented by j, we compute the following        users. It builds the faster feature extractor by removing asser-
value:                                                             tions that do not result in a branch in the regression trees.

                X                                                  B. The which_method command.
                             (usedi − used
                                       dR
                                           used (j)
                                                    )2 +
                                                                      When users invoke the which_method command,
           i:xi ∈Rused (j)
               X                                             (3)   PaMpeR applies the faster feature extractor to convert the
                                  d R (j) )2
                        (usedi − used                              ongoing proof state into a feature vector, which consists
                                      not
           i:xi ∈Rnot (j)                                          of those features that are deemed to be important to make
 and choose the feature j that minimizes this value.               a recommendation. The speed of this faster feature vector
   Second, we repeat this partition procedure to each emerging     depends on both the regression trees and what each proof state
sub-node of the regression tree under construction until the       contains. As a rule of thumb, if the proof goal has less terms,
depth of tree hits our pre-defined upper limit.                    it tends to spend less time.
   After reaching the maximum depth, we compute the average           Then, PaMpeR looks up the corresponding node in each
value of used(j) in the corresponding sub-space R for each         regression tree and decides the expectation that the method is
leaf node. We consider this value as the expectation that the      the right choice for the proof state represented by the feature
method is useful to proof states abstracted to the combination     vector. PaMpeR computes this value for each proof method
of feature values to that leaf node.                               it encountered in the training proof corpora, by looking up a
   PaMpeR records these regression trees in a text file,           node in each regression tree. Finally, PaMpeR compares these
regression_trees.txt, so that users can avoid the                  expectations and shows the 15 most promising proof methods
computationally intensive data extraction and regression tree      with their expectations in Isabelle/jEdit’s output panel. In the
construction processes unless they want to optimize the learn-     on-going example from Section II-A, a user can know which
ing results based on their own proof corpora.                      method to use by typing the which_method command as
   Note that if we add more assertions to our feature extractor    follows:
in future, the complexity of this algorithm increases linearly     lemma
with the number of assertions given a fixed depth of regression     "map f (sep x xs) = sep (f x) (map f xs)"
tree, since the partition only takes the best step at each level    which_method
instead of exploring all the combinations of partitions.
                                                                   Then, PaMpeR shows the following message in the output
               V. R ECOMMENDATION P HASE                           panel for the top 15 methods 3 :
   Once finishing building regression trees for each proof
                                                                   Promising methods for this proof goal are:
method appeared in the given proof corpora, one can
                                                                     simp with expectation of 0.4119
extract recommendations from PaMpeR. When imported
                                                                     auto with expectation of 0.1593
to users’ theory file, PaMpeR automatically reads these
                                                                     rule with expectation of 0.0874
trees using the read_regression_trees command in
                                                                     induction with expectation of 0.06137
PaMpeR/PaMpeR.thy.
                                                                     metis with expectation of 0.05260 ...
   PaMpeR provides three new commands to provide two
kinds of information: the which_method command tells               Attentive readers might have noticed that PaMpeR’s recom-
which proof methods are likely to be useful for a given            mendations are not identical to the model answer provided
proof state; the why_method command takes a name of                by Nipkow et al. This, however, does not immediately mean
proof method and tells why PaMpeR would recommend the              PaMpeR’s recommendation is not valuable: in fact, PaMpeR
proof method for the proof state; and the rank_method              recommended the induction method at the fourth place out
command shows the rank of a given method to the proof state        of 239 proof methods, and induction is also a valid method
in comparison to other proof methods. In the following, we         for this proof goal as discussed in Section IV-A.
explain how these two commands produce recommendations
from the regression trees produced in the preparation phase.       C. The why_method command.
                                                                     Our rather straightforward machine learning algorithm
A. Faster Feature Extractor
                                                                   makes PaMpeR’s recommendation explainable. If you
  Before applying the machine learning algorithm, we were          wonder why PaMpeR recommends a certain method,
not sure which assertion produces valuable features, but after
applying the machine learning algorithm, we can judge which          3 Note that we truncated the message due to the space restriction here.
for example case_tac, to your proof goal, type                    evaluation dataset. Third, we built regression trees from the
why_method case_tac in the proof script. PaMpeR                   remaining 90%. There is no overlap between the evaluation
first checks features used to evaluate the expectation for the    dataset and training dataset. Then, we applied regression trees
method and their feature values. Second, PaMpeR shows             to each each data point in the evaluation dataset and counted
qualitative explanations tagged to both these features and        how often PaMpeR’s recommendation coincides with the
their values in jEdit’s output. If you wonder why PaMpeR          proof methods chosen by human proof authors.
recommended induction in the above example, type the                 Since there are often multiple equally valid proof methods
following:                                                        for each proof state, it is only reasonable to expect that
                                                                  which_method should be able to recommend the proof
lemma
                                                                  method used in the evaluation dataset as one of the most im-
 "map f (sep x xs) = sep (f x) (map f xs)"
                                                                  portant methods for each proof method invocation. Therefore,
 why_method induction
                                                                  for each proof method, we measured how often each proof
Then, you will see this message in jEdit’s output panel:          method used in the evaluation dataset appears among the top
                                                                  n methods in PaMpeR’s recommendations.
Because it is not true that the context
                                                                     Table II shows the results for the 15 proof methods that are
has locally defined assumptions.
                                                                  most frequently used in the training data in the descending
Because the underlying proof context has
                                                                  order.
a recursive simplification rule related to
                                                                     For example, the top row for simp should be interpreted
a constant appearing in the first subgoal.
                                                                  as following: The simp method was used 102441 times in
The first reason corresponds to the first branching at the root   the training data. This amounts to 26.8% of all proof method
node in the regression tree for the induction method, and         invocations in the training data that are recorded by PaMpeR.
the second reason corresponds to the second branching in the      In the evaluation dataset, simp was used 11385 times, which
tree. In this case, PaMpeR found that the proof goal involves     amounts to 26.8% of proof method invocations in the evalu-
the constant, sep, and the underlying proof context contains      ation dataset that are recorded by PaMpeR. For 58% out of
a simplification rule, sep.simps(3), which involves a             11385 simp invocations in the evaluation dataset, PaMpeR
recursive call of sep as following:                               predicted that simp is the most promising method for the
                                                                  corresponding proof states. For 98% out of 11385 simp
sep.simp(3):
                                                                  invocations in the evaluation dataset, PaMpeR recommended
  sep ?a (?x # ?y # ?zs)
                                                                  that simp is either the most promising method or the second
= ?x # ?a # sep ?a (?y # ?zs)
                                                                  most promising method for the corresponding proof states.
D. The rank_method command.                                          Note that the numbers presented in this table are not the suc-
   Sometimes users already have a guess as to which proof         cess rates of PaMpeR’s recommendation but its conservative
method would be useful to their proof state, but they want        estimates. Assume PaMpeR recommends simp as the most
to know how PaMpeR ranks the proof method in mind.                promising method and auto as the second most promising
Continuing with the above example, if you want to know how        method to a proof goal, say pg, in the evaluation dataset, but
PaMpeR ranks conduction for this proof state, type the            the human proof author of pg chose to apply auto to this
following:                                                        proof goal. This does not immediately mean that PaMpeR
                                                                  failed to recommend auto in the first place, because both
lemma                                                             simp and auto might be equally suitable for pg. Therefore,
"map f (sep x xs) = sep (f x) (map f xs)"                         the 58% for simp mentioned above should be interpreted
 rank_method coinduction                                          as follows: PaMpeR’s recommendation coincides with the
Then, PaMpeR warns you:                                           choice of experienced Isabelle user for 58% of times where
                                                                  human engineers applied simp when PaMpeR is allowed to
coinduction 123 out of 239                                        recommend only one proof method, but the real success rate of
indicating that PaMpeR does not consider coinduction              PaMpeR’s recommendation can be higher than 58% for these
to be the right choice for this proof goal, before you waste      cases. To avoid the confusion with success rate, we introduce
your time on emerging sub-goals appearing after applying          the term, coincidence rate, for this measure. Table III, IV and,
coinduction.                                                      V in Appendix provide the complete list of the evaluation
                                                                  results.
                      VI. E VALUATION                                The overall results of this evaluation are as follows:
  We conducted a cross-validation to assess the accuracy of       PaMpeR learnt 239 proof methods from Isabelle’s standard
PaMpeR’s which_method command. For this evaluation,               library and the AFP: 160 of them are defined within Isabelle’s
we used Isabelle’s standard library and the AFP as follows:       standard library, and the others are user-defined proof methods,
First, we extracted a database from these proof corpora. This     which are specified in the AFP entries.
database consists of 425334 data points. Second, we randomly         Out of the 239 proof methods PaMpeR learnt from the
chose 10% of data points in this database to create the           training dataset, 171 proof methods appeared in the evaluation
                         TABLE II: Evaluation of PaMpeR on 15 most frequently used proof methods.

              proof method training   % evaluation   %   1   2   3   4      5   6    7   8     9    10    11    12    13    14    15
              simp      102441 26.8         11385 26.8 58 98 99 99 100 100 100 100           100   100   100   100   100   100   100
              auto       85097 22.2          9527 22.4 60 94 98 99 100 100 100 100           100   100   100   100   100   100   100
              rule       38856 10.2          4150 9.8 3 15 86 99 100 100 100 100             100   100   100   100   100   100   100
              blast      23814 6.2           2590 6.1 0 26 26 35 84 95 99 100                100   100   100   100   100   100   100
              metis      19771 5.2           2149 5.1 0 0 13 72 84 89 93 96                   98    99   100   100   100   100   100
              fastforce   9477 2.5           1093 2.6 0 0 0 0        5 54 70 81               89    93    96    96    97    98    98
              force       6232 1.6            708 1.7 0 0 0 0        1   9 22 32              40    51    66    77    84    89    94
              clarsimp    5984 1.6            628 1.5 0 12 14 14 20 29 39 49                  54    57    62    64    66    67    73
              cases       5842 1.5            689 1.6 0 0 1 16 16 20 34 54                    70    80    86    91    93    95    96
              erule       5732 1.5            707 1.7 0 0 15 38 44 53 64 70                   76    82    85    87    91    92    93
              subst       5655 1.5            619 1.5 0 0 19 19 19 20 22 28                   45    58    69    77    82    86    90
              rule_tac    5342 1.4            631 1.5 0 14 32 34 44 45 46 47                  50    51    52    52    53    57    63
              intro       4988 1.3            619 1.5 0 0 5 18 24 39 46 47                    48    48    49    57    69    77    84
              simp_all    4982 1.3            568 1.3 0 0 0 1        3   6 15 21              26    33    45    60    70    78    83
              induct      4884 1.3            568 1.3 0 0 0 1 27 45 49 50                     50    51    56    62    71    77    79



dataset. Out of these 171 proof methods within the evaluation            that is suitable for the proof goal at hand, whereas PaMpeR’s
dataset, 133 methods are defined in Isabelle’s standard library,         recommendations tend to differ from human engineers’ choice
and 38 methods were defined by the AFP authors.                          when there are multiple equally valid proof methods for the
   The distribution of proof method usage is heavily imbal-              same goal. For example, PaMpeR’s coincidence rates are
anced. The three most frequently used proof methods (simp,               low for less commonly used general-purpose methods, such
auto, and rule) account for 59.1% of all data points in                  as safe, clarimp, best, bestsimp because multiple
the training dataset, and the ten most frequently used methods           general purpose proof methods can often handle the same
account for 79.2% in the training dataset. Similarly in the              proof goal equally well.
evaluation dataset, the top three methods account for 58.9%,                A careful observation at the raw evaluation results pro-
and the top ten methods for 79.1%.                                       vided in the Appendix reveal that PaMpeR provides valu-
   Fig. 2 illustrates this imbalance, in which the horizontal axis       able recommendations when proof states are best handled by
represents the rank of method usage for a proof method and the           special purpose proof methods, such as unfold_locales,
vertical axis stands for the number of methods invocations for           transfer, eventually_elim, standard, and so on.
that proof method. For instance, the square located at the top-             PaMpeR’s regression tree construction does not severely
left corner denotes that the most frequently used proof method           suffer from the imbalance among proof method invoca-
in the training dataset (simp) is used 102441 times. And the             tion, even though class imbalances often cause problems in
circle located at (6, 1093) denotes that the sixth most fre-             other domains such as fraud detection and medical diagnosis
quently used method in the evaluation dataset (fastforce)                [20]. The complete evaluation results in Appendix show that
is used 1093 times in the evaluation dataset. With the use of            PaMpeR achieved 50% of coincidence rate for 34 proof
logarithmic scale on the vertical axis, this figure presents the         methods that appear less than 0.1% of times in the training
serious imbalance of proof method invocations occurring in               dataset.
Isabelle’s standard library and the AFP.                                    The reason the imbalance did not cause serious problems
   Fig. 3 summarises the overall performance of PaMpeR. In               to PaMpeR is that some of these rarely used methods are
this figure the horizontal axis represents the number of proof           specialised proof methods, for which we can write assertions
methods PaMpeR is allowed to recommend (15 by default),                  that can abstract the essence of the problem very well. Another
whereas the vertical axis represents the number of proof                 reason is the fact that commonly used proof methods tend
methods, for which PaMpeR achieves certain coincidence                   to hold up each other’s share, since they address similar
rates.                                                                   problems, lowering expectations for commonly used general
   For example, the square at (3, 23) means that PaMpeR can              purpose methods where both specialised methods and general
achieve 50% of coincidence rate for 23 methods if PaMpeR                 purpose methods can discharge proof goals.
is allowed to recommend three most promising methods.                       On the other hand, PaMpeR did not produce valuable
Similarly, PaMpeR achieves 50% of coincidence rate for 58                recommendations to some special purpose proof methods, such
methods when recommending 10 methods and for 72 methods                  as normalization and vector, for which we did not
when recommending 15 methods.                                            manage to develop assertions that capture the properties shared
   The number of methods PaMpeR achieved the four coinci-                by the proof goals that these methods can handle well. Writing
dent rates (25%, 50%, 75%, and 90%), reached a plateau when              suitable assertions for these remain as our future work.
PaMpeR is allowed to recommend about 60 proof methods.                      Some of the proof methods appearing in our evaluation
   Overall, PaMpeR’s recommendations tend to coincide with               dataset are clearly outside the scope of PaMpeR. For example,
human engineers’ choice when Isabelle has only one method                tactic, cartouche, ml_tactic, rotate_tac do not
                                         Fig.2: Method usage in large proof corpora.                                                       Fig. 3: Coincidence rate for PaMpeR.
                               100,000




                                                                                       Methods above four coincidence rates.
                                                                in training dataset                                            160
Number of method invocation.



                                                               in evaluation dataset                                           140
                                10,000
                                                                                                                               120
                                 1,000                                                                                         100
                                                                                                                                80
                                  100
                                                                                                                                60                                more than 25%
                                                                                                                                40                                more than 50%
                                   10
                                                                                                                                                                  more than 75%
                                                                                                                                20                                more than 90%
                                    1                                                                                            1
                                          20 40 60 80 100 120 140 160                                                                1    20 40 60 80 100 120 140 160
                                          Nth most commonly used proof method.                                                           Number of methods PaMpeR recommends.


                                                                                          Choosing the right methods was a difficult task for new
have much semantic meaning: tactic is simply an interface                              ITP users especially when they should choose special-purpose
between Isabelle’s source code language, Standard ML, and                              proof methods, since new users tend not to know even the
Isabelle’s proof language, Isar, whereas rotate_tac simply                             existence of those rarely used proof methods. Some proof
rotates the order of premises when a proof goal has multiple                           methods are strongly related to certain definitional mecha-
premises. Another good example of proof methods outside                                nisms in Isabelle. Therefore, when Isabelle experts use such
the scope of PaMpeR is the my_simp method. This method                                 definitional mechanisms, they can often guess which proof
was defined in the standard library to test the domain specific                        methods they should use later. But this is not an easy task
language, Eisbach, for writing new proof methods: my_simp                              for new users. And this is becoming truer nowadays, since
is simply a synonym of simp and nobody is expected to use                              large scale theorem proving projects are slowly becoming
my_simp. Predicting such methods is not a very meaningful                              popular and new ITP users often have to take over proof scripts
task for PaMpeR.                                                                       developed by others and they also have to discharge proof
   To our surprise, Table V shows that PaMpeR’s recommen-                              goals specified by others. PaMpeR addressed this problem
dation achieved 50% of coincidence rate for 12 methods out                             by systematically transferring experienced users knowledge to
of 38 user-defined proof methods defined outside Isabelle’s                            less experienced users. We plan to keep improving PaMpeR
standard library appearing in the evaluation dataset when                              by incorporating other Isabelle users intuitions as assertions.
PaMpeR is allowed to provide 15 most promising proof meth-                                Our manually written feature extractor may seem to be naive
ods, even though PaMpeR’s developers did not know anything                             compared to the recent success in machine learning research:
about these proof methods at the time of development. This                             in some problem domains, such as image recognition and the
suggests that one does not need to know the problem specific                           game of Go, deep neural networks extract features of the
information about proof goals to predict the use of some user-                         subject matters via expensive training. Indeed, others have
defined proof methods. For example, PaMpeR achieves 100%                               applied deep neural networks to theorem proving, but without
of coincidence rate for sepref when allowed to recommend                               much success [12], [13].
only four methods, by checking if the first sub-goal has a                                The two major problems of automatic feature extraction
schematic variable and if the first sub-goal has variables of                          for theorem proving is the lack of enormous database needed
type record.                                                                           to train deep neural networks and the expressive nature of
                                                                                       the underlying language, i.e. logic. The second problem, the
                                    VII. D ISCUSSION AND F UTURE W ORK                 expressive nature of logic, contributes to the first problem:
                                                                                       self-respecting proof engineers tend to replace multiple similar
   Prior to PaMpeR, Isabelle had the print_methods com-                                propositions with one proposition from which one can easily
mand, which merely lists the proof methods defined in the                              conclude similar propositions, aiming at a succinct presenta-
corresponding proof context in alphabetical order ignoring                             tion of the underlying concept.
the properties of the proof goal at hand. Therefore, new                                  What is worse, when working with modern ITPs, it is often
Isabelle/HOL users have to go through various documentations                           not enough to reason about a proof goal, but one also has
and the archive of mailing lists to learn how to prove lemmas                          to take its proof context into consideration. A proof context
in Isabelle/HOL independently.                                                         usually contains numerous auxiliary lemmas and nested defi-
nitions, and each of them is a syntax tree, making the effective   PSL’s automatic removal of backtracked proof steps eliminates
automatic feature extraction harder.                               the data pollution problem discussed in Section III-B. PSL’s
   Furthermore, whenever a proof author defines a new con-         framework to write history-sensitive proof methods allows us
stant or prove a new lemma, Isabelle/HOL changes the under-        to write history-sensitive assertions, so that PaMpeR can take
lying proof context, which affects how one should attack proof     the sequence of proof methods into account.
goals defined within this proof context. And proof authors do
add new definitions because they use ITPs as specification                  VIII. C ONCLUSION AND R ELATED W ORK
tools as well as tools for theorem proving. Some of these             We presented the design and implementation of PaMpeR.
changes are minor modifications to proof states that do not        In the preparation phase, PaMpeR learns which method to use
severely affect how to attack proof goals in the following         from existing proof corpora using regression tree construction
proof scripts, but in general changing proof contexts results      algorithm. In the recommendation phase, PaMpeR recom-
in, sometimes unexpected, problems.                                mends which proof methods to use to a given proof goal and
   For this reason, even though the ITP community has large        explains why it suggests that method. Our evaluation showed
proof corpora, we are essentially dealing with different prob-     that PaMpeR tends to provide valuable recommendations
lems in each line of each proof corpus. For example, even          especially for specialised proof methods, which new Isabelle
the AFP has 396 articles consisting of more than 100,000           users tend not to be aware of. We also identified problems
lemmas, only 4 articles are used by more than 10 articles          that arise when applying machine learning to proof method
in the AFP, indicating that many proof authors work on their       recommendation and proposed our solution to them.
own specifications, creating new problems. This results in an           Related Work: ML4PG [14] extends a proof editor, Proof
important difference that lies between theorem proving in an       General, to collect proof statistics about shapes of goals,
expressive logic and other machine learning domains, such as       sequence of applied tactics, and proof tree structures. It also
image recognition where one can collects numerous instances        clusters the gathered data using machine learning algorithms
of similar objects.                                                in MATLAB and Weka and provides proof hints during proof
   We addressed this problem with human-machine coopera-           developments. Based on learning, ML4PG lists similar proof
tion, the philosophy that underpins ITPs. Even though it is        goals proved so far, from which users can infer how to attack
hard to extract features automatically, experienced ITP users      the proof goal at hand, while PaMpeR directly works on proof
know that they can discharge many proof goals with shallow         methods. Compared to ML4PG, PaMpeR’s feature extractor
reasoning. We encoded experienced Isabelle users’ expertise        is implemented within Isabelle/ML, which made it possible
as assertions to simulate their shallow reasoning. Since these     to investigate not only proof goals themselves but also their
assertions are carefully hand-written in Isabelle/ML, they can     surrounding proof context.
extract features of proof states (including proof goal, chained       Gauthier et al. developed TacticToe for HOL4. It selects
facts, and its context) despite the above mentioned problems.      proved lemmas similar to the current proof goal using premise
   Currently PaMpeR recommends only which methods to use           selection and applies tactics used to these similar goals to
and shows why it suggests that method. This is enough for          discharge the current proof goal. Compared to TacticToe, the
many special purpose methods which do not take parameters.         abstraction via assertions allows PaMpeR to provide valuable
For other methods, such as induct, it is often indispensable       recommendations even when similar goals do not exist in the
to pass the correct parameters to guide methods. If you prefer     problem domain.
to know which arguments to pass to the proof method PaMpeR            Several people applied machine learning techniques to im-
recommends, we would invite you to use PSL [11], the proof         prove the so-called Hammer-style tools. For Isabelle/HOL,
strategy language for Isabelle/HOL, which attempts to find the     both MePo [17] and MaSh [18] decreased the quantity of facts
right combination of arguments through an iterative deepening      passed to the automatic provers while increasing their quality
depth first search based on rough ideas about which method         to improve Sledgehammers performance. Their approaches
to use. If you want to have those rough ideas, use PaMpeR.         attempt to choose facts that are likely to be useful to the given
   Moreover, none of PaMpeR’s assertions takes the sequence        proof goal, while PaMpeR suggests proof methods that are
of proof method applications into account: even though they        likely to be useful to the goal.
can check the information contained in the background proof           MePo judges the relevance of facts by checking the oc-
context, the parse-then-consume style of Isabelle/Isar makes       currence of symbols appearing in proof goals and available
it difficult for PaMpeR to trace which methods have been           facts, while MaSh computes the relevance using sparse naive
applied to reach the current proof state.                          Bayes and k Nearest Neighbours. They detect similarities
   We envision a more powerful proof automation tool backed        between proof goals and available facts by checking mostly
by PaMpeR and PSL. We use PaMpeR’s recommendation                  formalization-specific information and only two piece of meta
to navigate the search of PSL, changing PSL’s evaluation           information, while PaMpeR discards most of problem specific
strategy from the IDDFS to the best-first search. PSL pro-         information and focus on meta information of proof goals: the
vides a mechanism to generate variants of proof methods            choice of relevant fact is a problem specific question, while the
with different combinations of parameters to find the right        choice of proof method largely depends on which Isabelle’s
combination of parameters for a given goal through a search.       subsystem is used to specify a proof goal.
   The original version of MaSh was using machine learning                                      R EFERENCES
libraries in Python, and Blanchette et al. ported them from
Python to Standard ML for better efficiency and reliability.       [1] Tobias Nipkow and Lawrence C. Paulson and Markus Wenzel, Is-
Similarly, an early version of PaMpeR was also using a Python          abelle/HOL - A proof assistant for Higher-Order Logic, Lecture Notes in
                                                                       Computer Science, vol. 2283, Springer, 2002, 3-540-43376-7
library [9] until we implemented the regression tree construc-     [2] Gerwin Klein and June Andronick and Kevin Elphinstone and Gernot
tion algorithm in Standard ML for better tool integration and          Heiser and David Cock and Philip Derrin and Dhammika Elkaduwe and
flexibility. Both MaSh and PaMpeR record learning results in           Kai Engelhardt and Rafal Kolanski and Michael Norrish and Thomas
                                                                       Sewell and Harvey Tuch and Simon Winwood, seL4: formal verification
persistent states outside the main memory, so that users can           of an operating-system kernel, Commun. ACM, vol. 53-6, pp. 107-115,
preserve the learning results even after shutting down Isabelle.       2010
   Blanchette et al. analysed the AFP, looking at sizes and        [3] Xavier Leroy, Formal verification of a realistic compiler, Commun. ACM,
dependencies for theory files [23]. Matichuk et al. investigated       vol. 52-7, pp. 107-115, 2009
                                                                   [4] Ramana Kumar and Magnus O. Myreen and Michael Norrish and Scott
the seL4 proofs and two articles in the AFP to find the                Owens, CakeML: a verified implementation of ML, The 41st Annual
relationship between the size of statement and the size of proof       ACM SIGPLAN-SIGACT Symposium on Principles of Programming
[24]. None of them analysed the occurrence of proof methods            Languages, POPL ’14, San Diego, CA, USA, January 20-21, 2014, pp.
                                                                       179-192
in their target proof corpora nor developed a recommendation       [5] Thomas C. Hales and Mark Adams and Gertrud Bauer and Dat Tat Dang
system based on their results. Moreover, PaMpeR’s database             and John Harrison and Truong Le Hoang and Cezary Kaliszyk and Victor
construction is more active compared to their work: it applies         Magron and Sean McLaughlin and Thang Tat Nguyen and Truong Quang
                                                                       Nguyen and Tobias Nipkow and Steven Obua and Joseph Pleso and
108 hand-written assertions to analyse the properties of not           Jason M. Rute and Alexey Solovyev and An Hoai Thi Ta and Trung
only each proof goal but also the relationship between each            Nam Tran and Diep Thi Trieu and Josef Urban and Ky Khac Vu and
goal and its background context and chained facts.                     Roland Zumkeller, A formal proof of the Kepler conjecture, CoRR, vol.
                                                                       abs/1501.02155, 2015, arXiv
                                                                   [6] Georges Gonthier, The four colour theorem: engineering of a formal
                                                                       proof, Computer Mathematics, 8th Asian Symposium, ASCM 2007,
                                                                       Singapore, December 15-17, 2007. Revised and Invited Papers, pp. 333
                                                                   [7] Ren Thiemann and Christian Sternagel Certification of termination proofs
                                                                       using CeTA In Proceedings of the 22nd International Conference on
                                                                       Theorem Proving in Higher Order Logics (TPHOLs ’09), Lecture Notes
                                                                       in Computer Science 5674, pp. 452468, 2009, Springer-Verlag
                                                                   [8] Lawrence C. Paulson, A mechanised proof of gödel’s incompleteness
                                                                       theorems using Nominal Isabelle, J. Autom. Reasoning, vol. 55-1, pp.
                                                                       1-37, 2015, https://doi.org/10.1007/s10817-015-9322-8
                                                                   [9] Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B.,
                                                                       Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V. Van-
                                                                       derPlas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., Duch-
                                                                       esnay, E. Scikit-learn: Machine Learning in Python, Journal of Machine
                                                                       Learning Research, volume 12, 2011
                                                                   [10] James, G., Witten, D., Hastie, T., Tibshirani R. An Introduction to
                                                                       Statistical Learning with Applications in R
                                                                   [11] Yutaka Nagashima and Ramana Kumar, A proof strategy language and
                                                                       proof script generation for Isabelle/HOL, Automated Deduction - CADE
                                                                       26 - 26th International Conference on Automated Deduction, Gothenburg,
                                                                       Sweden, August 6-11, 2017, Proceedings, pp. 528–545
                                                                   [12] Geoffrey Irving and Christian Szegedy and Alexander A. Alemi
                                                                       and Niklas Eén and François Chollet and Josef Urban, Deep-
                                                                       Math - deep sequence models for premise selection, Advances
                                                                       in Neural Information Processing Systems 29: Annual Conference
                                                                       on Neural Information Processing Systems 2016, December 5-10,
                                                                       2016, Barcelona, Spain, pp. 2235–2243, http://papers.nips.cc/paper/
                                                                       6280-deepmath-deep-sequence-models-for-premise-selection
                                                                   [13] Sarah M. Loos and Geoffrey Irving and Christian Szegedy and Cezary
                                                                       Kaliszyk, Deep network guided proof search, LPAR-21, 21st Interna-
                                                                       tional Conference on Logic for Programming, Artificial Intelligence
                                                                       and Reasoning, Maun, Botswana, May 7-12, 2017, pp. 85-105, http:
                                                                       //www.easychair.org/publications/paper/340345
                                                                   [14] Ekaterina Komendantskaya and Jónathan Heras and Gudmund Grov,
                                                                       Machine learning in proof general: interfacing interfaces, Proceedings
                                                                       10th International Workshop On User Interfaces for Theorem Provers,
                                                                       UITP 2012, Bremen, Germany, July 11th, 2012. pp. 15-41
                                                                   [15] Gerwin Klein, Tobias Nipkow, Larry Paulson, Rene Thiemann, Archive
                                                                       of Formal Proofs, https://www.isa-afp.org/
                                                                   [16] Thibault Gauthier and Cezary Kaliszyk and Josef Urban, TacticToe:
                                                                       learning to reason with HOL4 tactics, LPAR-21, 21st International Con-
                                                                       ference on Logic for Programming, Artificial Intelligence and Reasoning,
                                                                       Maun, Botswana, May 7-12, 2017, pp. 125-143
                                                                   [17] Jia Meng and Lawrence C. Paulson, Lightweight relevance filtering for
                                                                       machine-generated resolution problems, J. Applied Logic, vol. 7-1, pp.
                                                                       41-57 2009
[18] Jasmin Christian Blanchette and David Greenaway and Cezary Kaliszyk                                       A PPENDIX
    and Daniel Kühlwein and Josef Urban, A learning-based fact selector for
    Isabelle/HOL, J. Autom. Reasoning, vol. 57-3, pp. 219-244 2016                      Table III shows the results for proof methods that are defined
[19] Markus Wenzel, Isar - a generic interpretative approach to readable             in the standard library and are frequently used in the training
    formal proof documents, Theorem Proving in Higher Order Logics, 12th             data in the descending order. Table IV shows the results for
    International Conference, TPHOLs’99, Nice, France, September, 1999,
    Proceedings, pp. 167–184                                                         proof methods that are defined in the standard library and are
[20] Haibo He and Edwardo A. Garcia, Learning from imbalanced data, IEEE             less frequently used in the training data in the descending
    Trans. Knowl. Data Eng., vol. 21. pp. 1263-1284. 2009,                           order. Table V shows the results for proof methods that are
[21] https://github.com/data61/PSL/releases/tag/v0.1.1 To use PaMpeR, one
    first needs to install Isabelle/HOL, which is distributed at https://isabelle.   locally defined in the AFP entries by Isabelle users.
    in.tum.de/. PGT/Example.thy provides the example presented in this                  For example, the top row for simp in Table III should
    paper.                                                                           be interpreted as following: The simp method was used
[22] Breiman, Leo; Friedman, J. H.; Olshen, R. A.; Stone, C. J., 1984, Clas-
    sification and regression trees. Monterey, CA: Wadsworth & Brooks/Cole           102441 times in the training data. This amounts to 26.8%
    Advanced Books & Software.                                                       of all proof method invocations in the training data that
[23] Jasmin Christian Blanchette and Maximilian P. L. Haslbeck and Daniel            are recorded by PaMpeR. In the evaluation dataset, simp
    Matichuk and Tobias Nipkow, Mining the Archive of Formal Proofs,
    Intelligent Computer Mathematics - International Conference, CICM                was used 11385 times, which amounts to 26.8% of proof
    2015, Washington, DC, USA, July 13-17, 2015, Proceedings, pp. 3 -17              method invocations in the evaluation dataset that are recorded
[24] Daniel Matichuk and Toby C. Murray and June Andronick and D. Ross               by PaMpeR. For 58% out of 11385 simp invocations in
    Jeffery and Gerwin Klein and Mark Staples, Empirical study towards a
    leading indicator for cost of formal software verification, 37th IEEE/ACM        the evaluation dataset, PaMpeR predicted that simp is the
    International Conference on Software Engineering, ICSE 2015, Florence,           most promising method for the corresponding proof states.
    Italy, May 16-24, 2015, Volume 1, pp. 722-732                                    For 98% out of 11385 simp invocations in the evaluation
                                                                                     dataset, PaMpeR recommended that simp is either the most
                                                                                     promising method or the second most promising method for
                                                                                     the corresponding proof states.
                                                                                        Note that the numbers presented in this table are not the suc-
                                                                                     cess rates of PaMpeR’s recommendation but its conservative
                                                                                     estimates. Assume PaMpeR recommends simp as the most
                                                                                     promising method and auto as the second most promising
                                                                                     method to a proof goal, say pg, in the evaluation dataset, but
                                                                                     the human proof author of pg chose to apply auto to this
                                                                                     proof goal. This does not immediately mean that PaMpeR
                                                                                     failed to recommend auto in the first place, because both
                                                                                     simp and auto might be equally suitable for pg. Therefore,
                                                                                     the 58% for simp mentioned above should be interpreted
                                                                                     as follows: PaMpeR’s recommendation coincides with the
                                                                                     choice of experienced Isabelle user for 58% of times where
                                                                                     human engineers applied simp when PaMpeR is allowed to
                                                                                     recommend only one proof method, but the real success rate of
                                                                                     PaMpeR’s recommendation can be higher than 58% for these
                                                                                     cases. In Section VI, we introduced the term, coincidence rate,
                                                                                     for this measure to avoid the confusion with success rate.
                                                                                        The last figure in the Appendix is a screenshot of Is-
                                                                                     abelle/HOL with PaMpeR, which shows the seamless in-
                                                                                     tegration of PaMpeR to Isabelle’s default proof editor, Is-
                                                                                     abelle/jEdit.
               TABLE III: Evaluation of PaMpeR on proof methods defined in the standard library 1.

proof method           training    % evaluation    %    1    2    3   4   5    6   7   8     9    10    11    12    13    14    15
simp                   102441 26.8       11385 26.8 58      98   99   99 100 100 100 100   100   100   100   100   100   100   100
auto                    85097 22.2        9527 22.4 60      94   98   99 100 100 100 100   100   100   100   100   100   100   100
rule                    38856 10.2        4150 9.8 3        15   86   99 100 100 100 100   100   100   100   100   100   100   100
blast                   23814 6.2         2590 6.1 0        26   26   35 84 95 99 100      100   100   100   100   100   100   100
metis                   19771 5.2         2149 5.1 0         0   13   72 84 89 93 96        98    99   100   100   100   100   100
fastforce                9477 2.5         1093 2.6 0         0    0    0   5 54 70 81       89    93    96    96    97    98    98
force                    6232 1.6          708 1.7 0         0    0    0   1   9 22 32      40    51    66    77    84    89    94
clarsimp                 5984 1.6          628 1.5 0        12   14   14 20 29 39 49        54    57    62    64    66    67    73
cases                    5842 1.5          689 1.6 0         0    1   16 16 20 34 54        70    80    86    91    93    95    96
erule                    5732 1.5          707 1.7 0         0   15   38 44 53 64 70        76    82    85    87    91    92    93
subst                    5655 1.5          619 1.5 0         0   19   19 19 20 22 28        45    58    69    77    82    86    90
rule_tac                 5342 1.4          631 1.5 0        14   32   34 44 45 46 47        50    51    52    52    53    57    63
intro                    4988 1.3          619 1.5 0         0    5   18 24 39 46 47        48    48    49    57    69    77    84
simp_all                 4982 1.3          568 1.3 0         0    0    1   3   6 15 21      26    33    45    60    70    78    83
induct                   4884 1.3          568 1.3 0         0    0    1 27 45 49 50        50    51    56    62    71    77    79
case_tac                 3347     0.9      362    0.9    0   0   0   0 10 24 35 43 49 54                58    62    66    70    77
fast                     3078     0.8      364    0.9    0   0   0   0   0   0   0   7 22 45            57    62    64    67    70
drule                    3020     0.8      343    0.8    0   0   0   0   7 19 24 25 29 35               45    55    68    79    90
subgoal_tac              2981     0.8      332    0.8    0   0   0   0   2 11 28 44 61 70               73    76    78    79    82
fact                     2861     0.7      356    0.8    0   0 30 30 30 30 33 35 39 50                  60    68    75    80    81
unfold                   2856     0.7      293    0.7    0   0   0   0   0 12 30 45 52 58               60    61    61    61    61
-                        2653     0.7      279    0.7    0   0   0   0   0   2 15 32 36 37              38    42    51    66    80
drule_tac                2620     0.7      299    0.7    0   7 23 38 38 38 38 39 40 41                  43    48    52    64    71
assumption               1855     0.5      184    0.4    0   0 39 45 48 48 49 50 50 50                  50    52    52    55    61
induction                1839     0.5      185    0.4    0   0   0 37 40 40 40 40 40 40                 40    40    40    41    45
transfer                 1661     0.4      186    0.4    0   0 51 51 51 51 51 51 51 51                  52    53    56    59    60
frule                    1592     0.4      166    0.4    0   0   0   0   1   5 16 29 39 42              42    42    42    42    43
erule_tac                1491     0.4      193    0.5    0   0   0   1   5 17 32 46 52 58               62    63    63    63    63
clarify                  1353     0.4      153    0.4    0   0   0   0   2   9 18 31 33 33              38    39    40    44    48
meson                    1275     0.3      139    0.3    2   2   2   2   2   2   2   2   2   2           2     2     3     8     9
rename_tac               1251     0.3      133    0.3    0   0   0   0   0   2   5 13 23 30             42    53    62    68    72
unfold_locales           1127     0.3       97    0.2    0   8 50 50 50 50 50 50 50 50                  50    50    50    50    50
cut_tac                  1003     0.3      102    0.2    0   0   0   0   0   0   0   0   0   5           8    17    26    28    36
arith                     998     0.3      127    0.3    0   0   0   0   0   0 18 27 42 48              50    51    53    53    54
safe                      982     0.3      100    0.2    0   0   0   0   0   0   0   3   6   7           7     7    11    13    14
frule_tac                 735     0.2       71    0.2    0   0   0   0   1   3   3   3   3   3           3     3     3     3     3
elim                      681     0.2       71    0.2    0   0   0   0   0   0   0   0   0   0           0     0     0     0     0
induct_tac                622     0.2       76    0.2    0   0   0 14 14 14 14 14 14 14                 14    14    14    14    14
eval                      621     0.2       65    0.2    0   0   0   8 48 62 65 65 65 65                65    65    65    65    65
iprover                   587     0.2       65    0.2    0   0   0   0   0 11 11 11 11 11               11    15    20    28    31
linarith                  550     0.1       57    0.1    0   0   4   4   4   9   9   9 10 10            10    10    10    10    10
standard                  534     0.1       59    0.1   56 56 56 56 56 56 59 66 70 70                   71    71    71    71    71
presburger                529     0.1       55    0.1    0   0   0   0   0   6 11 20 20 20              20    20    20    20    20
thin_tac                  492     0.1       50    0.1    0   0   0   0   0   0   0   0   0   0           0     0     2    12    24
insert                    475     0.1       37    0.1    0   0   0   0   0   0   0   0   0   0           0     0     0     0     0
tactic                    461     0.1       57    0.1    0   0 16 16 16 16 16 16 16 16                  16    16    16    16    16
nominal_induct            361     0.1       48    0.1    0   0   0 19 23 23 23 23 23 23                 23    23    25    29    54
rotate_tac                288     0.1       30    0.1    0   0   0   0   0   0   0   3   3   3           3    17    17    17    17
perm_simp                 282     0.1       32    0.1    0   0   0   0   0   0   3 12 12 16             19    19    47    47    56
eventually_elim           263     0.1       28    0.1    0   0 86 86 86 86 86 100 100 100              100   100   100   100   100
transfer_prover           257     0.1       26    0.1   50 50 50 73 77 77 77 77 77 77                   77    77    77    77    77
generate_fresh            235     0.1       22    0.1    0   0   0   0   0   0   0   0 18 27            36    41    41    41    41
contradiction             235     0.1       18    0.0    0   0   0   0   0   0   0   0   0   0          78    78    78    78    78
vcg                       206     0.1       26    0.1   88 92 92 92 92 92 92 92 92 92                   92    92    92    92    92
smt                       194     0.1       20    0.0    0   0   0   0   0   0   0   0   0   0           0     0     0     0     5
intro_classes             193     0.1       14    0.0    0 100 100 100 100 100 100 100 100 100         100   100   100   100   100
fold                      162     0.0       15    0.0    0   0   0   7   7   7   7   7   7   7           7     7     7     7     7
rewrite                   158     0.0       17    0.0    0   0   6   6   6   6   6   6   6   6           6     6     6     6     6
fresh_fun_simp            152     0.0       15    0.0    0   0   0   0   0 40 47 47 73 73               73    73    73    73    73
measurable                126     0.0       16    0.0    0   0   0   0   0   0   0 62 75 94            100   100   100   100   100
pat_completeness          120     0.0       12    0.0   92 92 92 92 92 92 92 92 92 100                 100   100   100   100   100
ind_cases                 118     0.0       13    0.0    0   0   0   0   0   0   0   0   0   0           0     0     0     0     0
field                     112     0.0       14    0.0    0   0 36 36 36 36 36 36 36 36                  36    36    36    36    43
sos                       103     0.0       14    0.0   50 50 50 50 50 50 50 50 50 50                   50    50    50    50    50
relation                  102     0.0       12    0.0   92 92 92 92 92 92 92 92 92 92                   92    92    92    92    92
               TABLE IV: Evaluation of PaMpeR on proof methods defined in the standard library 2.

proof method              training    % evaluation   %    1   2   3   4    5    6     7     8     9    10    11    12    13    14    15
descending                     94    0.0       18    0.0   0   0   0   0   0     0     6    33    61    61    61    61    61    61    61
normalization                  91    0.0       12    0.0 25 25 25 25 25         25    25    25    25    25    25    25    25    25    25
fixrec_simp                    90    0.0        9    0.0   0 89 89 89 89        89    89    89    89    89    89    89    89    89    89
coinduct                       90    0.0        6    0.0   0   0   0   0   0     0     0     0     0     0    67    67    83    83    83
lexicographic_order            89    0.0       12    0.0 67 67 67 92 92         92    92    92    92    92    92    92    92    92    92
argo                           78    0.0       16    0.0   0   0   0   0   0     0     0     0     0     6     6     6    12    12    12
ring                           73    0.0        7    0.0   0   0   0 43 43      43    43    43    43    43    43    43    43    43    43
atomize_elim                   67    0.0        4    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
coinduction                    66    0.0       12    0.0   0   0   0 25 33      33    33    33    33    33    33    33    33    33    33
best                           64    0.0        4    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
this                           63    0.0       10    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
hypsubst_thin                  58    0.0        6    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
spy_analz                      55    0.0        6    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
pair                           49    0.0        7    0.0 14 14 14 14 14         14    14    14    14    14    57    57    57    71    71
ferrack                        45    0.0        2    0.0   0   0   0   0   0     0    50   100   100   100   100   100   100   100   100
disjE_tac                      44    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
algebra                        44    0.0        6    0.0   0   0   0   0   0     0     0     0     0     0     0    17    17    17    17
vcg_simp                       43    0.0        6    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
split                          43    0.0        7    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
interfree_aux                  39    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
hypsubst                       37    0.0        7    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
sat                            36    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
cooper                         35    0.0        4    0.0   0   0   0 75 75      75    75    75    75    75    75    75    75    75    75
countable_datatype             32    0.0        1    0.0 100 100 100 100 100   100   100   100   100   100   100   100   100   100   100
simplesubst                    29    0.0        4    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0    25    25
vector                         23    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
valid_certificate_tac          23    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
metis_exhaust                  23    0.0        4    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
Seq_case_simp                  23    0.0        3    0.0   0   0   0   0   0     0    67    67   100   100   100   100   100   100   100
oghoare                        22    0.0        5    0.0 100 100 100 100 100   100   100   100   100   100   100   100   100   100   100
lifting                        22    0.0        6    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
uint_arith                     21    0.0        4    0.0   0   0   0   0   0   100   100   100   100   100   100   100   100   100   100
atomize                        21    0.0        4    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
fresh_guess                    19    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
unat_arith                     18    0.0        4    0.0   0   0   0   0   0     0     0    25    75    75    75    75    75    75    75
hoare                          17    0.0        2    0.0 50 50 50 50 50         50    50    50    50    50    50    50   100   100   100
approximation                  17    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
annhoare                       16    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
reify                          15    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
record_auto                    15    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
moura                          15    0.0        4    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
intro_locales                  15    0.0        2    0.0   0   0   0   0   0     0    50    50    50    50    50    50    50    50    50
bestsimp                       15    0.0        3    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
induction_schema               14    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
pair_induct                    13    0.0        2    0.0   0   0 100 100 100   100   100   100   100   100   100   100   100   100   100
finite_guess                    9    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
merge_box                       8    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
transfer_step                   7    0.0        2    0.0   0 50 100 100 100    100   100   100   100   100   100   100   100   100   100
size_change                     7    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
ns_induct                       6    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
reflection                      5    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
enabled                         5    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
ml_tactic                       4    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
mkex_induct                     4    0.0        1    0.0 100 100 100 100 100   100   100   100   100   100   100   100   100   100   100
merge_temp_box                  4    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
cartouche                       3    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
analz_mono_contra               3    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
rename_client_map               2    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
possibility                     2    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
defined                         2    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
corec_unique                    2    0.0        3    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
basic_possibility               2    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
sc_analz_freshK                 1    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
invariant                       1    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
disentangle                     1    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
coherent                        1    0.0        2    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
my_simp                         0    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
dlo                             0    0.0        1    0.0   0   0   0   0   0     0     0     0     0     0     0     0     0     0     0
                  TABLE V: Evaluation of PaMpeR on proof methods defined by users.

proof method             training    % evaluation    % 1     2   3   4   5   6   7   8     9    10    11    12    13    14    15
refine_vcg                   193    0.1       31    0.1   0 0   0 36 36 36 36 36          36    36    36    36    36    36    36
inv_cterms                   173    0.0       17    0.0   0 0   0   0   0 24 71 71       100   100   100   100   100   100   100
autoref_monadic              167    0.0       12    0.0   0 0 58 58 58 58 58 58           58    58    58    67    75    75    75
autoref                      113    0.0       17    0.0   0 0   0   0   0 12 35 59       100   100   100   100   100   100   100
sep_auto                     108    0.0        6    0.0   0 0   0 67 83 83 100 100       100   100   100   100   100   100   100
sepref                        86    0.0       12    0.0   0 0   0 100 100 100 100 100    100   100   100   100   100   100   100
hoare_rule                    80    0.0        7    0.0   0 14 14 14 14 14 14 14          14    14    14    14    14    14    14
refine_rcg                    77    0.0       10    0.0   0 0   0   0   0   0   0   0      0     0    10    30    50    50    50
solves                        73    0.0        8    0.0   0 0   0   0   0   0   0   0      0     0     0    38    38    38    38
prec                          70    0.0        7    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
vcg_step                      66    0.0        5    0.0   0 0   0   0 40 80 80 80         80    80    80    80    80    80    80
vc_solve                      58    0.0        5    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
code_simp                     42    0.0        2    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
refine_dref_type              41    0.0        1    0.0   0 0   0   0   0   0   0   0      0   100   100   100   100   100   100
vcg_jackhammer                40    0.0        3    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
refine_transfer               35    0.0        5    0.0   0 0   0   0   0   0   0   0      0    20    20    40    40    40    40
parametricity                 35    0.0        3    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
sepref_to_hoare               33    0.0        6    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
separata                      31    0.0        5    0.0   0 0   0 60 60 60 60 60          60    60    60    60    60    60    60
vcg_ni                        29    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
sepref_dbg_trans_step         21    0.0        4    0.0   0 0   0   0   0   0 50 75       75    75    75    75    75    75    75
clarsimp_all                  19    0.0        2    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
vcg_nihe                      18    0.0        4    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
tagged_solver                 11    0.0        2    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
rprems                        10    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
akra_bazzi_termination        10    0.0        2    0.0   0 0 100 100 100 100 100 100    100   100   100   100   100   100   100
kat_hom                        8    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
applicative_nf                 8    0.0        3    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
wellformed                     6    0.0        2    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
seq_stop_inv_method            5    0.0        1    0.0   0 0   0   0   0   0 100 100    100   100   100   100   100   100   100
fo_rule                        5    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
dlo_reify                      5    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
refine_mono                    4    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
sepref_dbg_opt_init            3    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
sepref_dbg_cons_init           3    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
sep_subst                      3    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
vcg_jackhammer_ff              2    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
sep_select                     2    0.0        1    0.0   0 0   0   0   0   0   0   0      0     0     0     0     0     0     0
Screenshot of Isabelle/HOL with PaMpeR.
