                                               Predicting Rankings of Software Verification Competitions∗
                                                                   Mike Czech, Eyke Hüllermeier, Marie-Christine Jakobs, Heike Wehrheim
                                                                                                            Department of Computer Science
                                                                                                                 Paderborn University
                                                                                                                      Germany

                                        ABSTRACT                                                                                    the Competition on Software Verification SV-COMP [1]. Over the
                                        Software verification competitions, such as the annual SV-COMP,                             years, the SV-COMP community has collected a large number of
                                        evaluate software verification tools with respect to their effectivity                      benchmark verification tasks, i.e., software source code together
                                        and efficiency. Typically, the outcome of a competition is a (possi-                        with properties to be proven, and is constantly continuing to do
arXiv:1703.00757v1 [cs.LG] 2 Mar 2017




                                        bly category-specific) ranking of the tools. For many applications,                         so. Verification tasks are bundled in categories, and the outcome
                                        such as building portfolio solvers, it would be desirable to have an                        of SV-COMP are rankings (overall and per category) computed by
                                        idea of the (relative) performance of verification tools on a given                         means of a scoring schema.
                                        verification task beforehand, i.e., prior to actually running all tools                         Rankings of verification tools on verification tasks in software
                                        on the task.                                                                                competitions offer an a-posteriori insight into the particular use-
                                           In this paper, we present a machine learning approach to pre-                            fulness of a tool on a verification task. However, for programmers
                                        dicting rankings of tools on verification tasks. The method builds                          wanting to select a tool for verification of their program, or for
                                        upon so-called label ranking algorithms, which we complement                                building portfolio solvers, a prediction on a likely ranking without
                                        with appropriate kernels providing a similarity measure for verifica-                       actually running (all or some) tools is needed. In this paper, we
                                        tion tasks. Our kernels employ a graph representation for software                          propose such a method.
                                        source code that mixes elements of control flow and program de-                                 Our method for rank prediction builds upon machine learning
                                        pendence graphs with abstract syntax trees. Using data sets from                            techniques, more precisely on so-called label ranking algorithms
                                        SV-COMP, we demonstrate our rank prediction technique to gener-                             [9] using support vector machines [3] as base learners. As training
                                        alize well and achieve a rather high predictive accuracy. In partic-                        data, we take the SV-COMP results of 2015 and the only recently
                                        ular, our method outperforms a recently proposed feature-based                              published results of 2017. The key ingredient of our approach is
                                        approach of Demyanova et al. (when applied to rank predictions).                            the definition of a number of kernels [20], which act as similarity
                                                                                                                                    measures on verification tasks. So far, two other machine learning
                                        CCS CONCEPTS                                                                                methods for selecting tools or algorithms for verification have been
                                                                                                                                    proposed [6, 23], both of them being based on feature vectors: while
                                        •Computing methodologies →Ranking; Support vector machines;
                                                                                                                                    Tulsian et al. [23] only employ structural features of programs (like
                                        Cross-validation; •Software and its engineering →Software ver-
                                                                                                                                    the number of arrays, loops, recursive functions), Demyanova et
                                        ification; Formal software verification;
                                                                                                                                    al. [6] uses a number of data-flow analyses to also determine more
                                                                                                                                    sophisticated features (e.g., certain loop patterns). Thus, both ap-
                                        KEYWORDS
                                                                                                                                    proaches try to explicitly capture aspects of source code that make
                                        Software verification, machine learning, ranking.                                           verification hard (for some or all tools). With our kernels, we take
                                        ACM Reference format:                                                                       a different approach: we supply the learning algorithm with a rep-
                                        Mike Czech, Eyke Hüllermeier, Marie-Christine Jakobs, Heike Wehrheim .                     resentation of source code that enables the learner itself to identify
                                        2017. Predicting Rankings of Software Verification Competitions.                            the distinguishing patterns. We believe that our kernels are thus
                                                                                                                                    more readily usable for other program analysis tasks, for which a
                                        1     INTRODUCTION                                                                          machine learning method might be considered (e.g., program classi-
                                                                                                                                    fication or program analysis). In that case, we could use exactly the
                                        The annual holding of software verification competitions has re-                            same kernel and just exchange the training data. Still, our experi-
                                        cently stimulated the development of verification tools, in partic-                         ments show that the prediction accuracy for rankings of software
                                        ular the tuning of tools towards performance and precision. The                             verification competitions is higher than that of Demyanova et al. [6]
                                        participating candidate tools typically employ a large range of dif-                        (when using their feature vectors for predicting rankings, not just
                                        ferent techniques, from static analysis, abstract interpretation and                        predicting winners)1 .
                                        automata-based techniques to SAT or SMT solving. In the area of                                 More specifically, our kernels are constructed on graph repre-
                                        automatic verification, the most prominent competition today is                             sentations of source code. We have experimented with different
                                        ∗ This work was partially supported by the German Research Foundation (DFG) within          (weighted) combinations of control flow graphs (CFGs), program
                                        the Collaborative Research Centre “On-The-Fly Computing” (SFB 901).                         dependence graphs (PDGs), and abstract syntax trees (ASTs). In
                                                                                                                                    these, concrete inscriptions on nodes (like x:=y+1) are first of all
                                        Permission to make digital or hard copies of part or all of this work for personal or
                                        classroom use is granted without fee provided that copies are not made or distributed
                                                                                                                                    replaced by abstract labels (e.g., Assign). Such labelled graphs are
                                        for profit or commercial advantage and that copies bear this notice and the full citation   used within our specific adaptation of the Weisfeiler-Lehman graph
                                        on the first page. Copyrights for third-party components of this work must be honored.
                                        For all other uses, contact the owner/author(s).                                            1 A comparison with Tulsian et al. [23] is difficult due to non-reproducability of their
                                        © 2017 Copyright held by the owner/author(s).                                               results.
                                                                   Mike Czech, Eyke Hüllermeier, Marie-Christine Jakobs, Heike Wehrheim


kernel framework [21] that compares graphs not only according to          1 int i;                     6 i = 0;
their labels (and how often they occur) but also according to associ-     2 int n;                     7 while (i <= n)
ations between labels (via edges in the graph). This is achieved by       3 int sn;                    8       sn = sn + 2;
iteratively comparing larger and larger subtrees of nodes, where the      4 n = input();               9       i = i + 1;
maximum depth of subtrees to be considered is a parameter to the          5 sn = 0;                    10 assert (sn == n*2 || sn == 0);
framework. The choice of Weisfeiler-Lehman kernels is motivated
by their better scalability compared to other graph kernels, such                          Figure 1: The verification task PSUM
as random walk or shortest path kernels (see [21]). We prove our
kernels to be positive definite, which is the key property for kernels
to be usable for machine learning. The ranking is finally computed        a verification run is a pair (TIME, ANSWER),2 where TIME is the
by a method for rank prediction via pairwise comparison [9], using        time in seconds from the start of the verification run to its end, and
support vector machines as base learners.                                 ANSWER is of the following form:
    We have implemented our technique and carried out experi-                   TRUE when the verification tool has concluded that P satis-
mental (cross-validation) studies using data from SV-COMP 2015                    fies φ,
and 2017. The experiments show that our technique can predict                   FALSE when the verification tool has concluded that P vio-
rankings with a rather high accuracy, using Spearman’s rank corre-                lates φ, and
lation [22] to compare predicted with true rankings. To see how                 UNKNOWN when no conclusive result was achieved.
our technique compares to existing approaches, we have also used
the feature vectors of Demyanova et al. [6] for rank prediction.          In SV-COMP, verification tasks are bundled into categories (e.g.,
It turns out that, for three different data sets (containing general      memory safety, termination, concurrency). Ranking of tools is first
safety, termination and memory safety verification tasks), our tech-      of all being carried out per category (but then extended to meta
nique outperforms the technique of [6] in almost all instantiations       categories). The ranking within a category is done via a scoring
(choosing a depth for subtrees and a combination of CFG, PDG and          schema which gives positive and negative points to outcomes, e.g.,
AST) .                                                                    negative points when the tool incorrectly concluded the property
                                                                          to be valid for the program. When the scores of two tools are the
Summarizing, this paper makes the following contributions:
                                                                          same, the runtimes (of successful runs) determine the ordering. The
      • We propose a technique for the prediction of rankings in          data from SV-COMP available for learning rankings thus consists
        software verification competitions (instead of just predict-      of verification tasks in different categories, outcomes of tools on
        ing winners);                                                     these tasks and scores assigned to these outcomes as well as the
      • we present an expressive representation of source code            final ranking.
        ready for use in other machine learning approaches to                The purpose of the machine learning algorithm is to learn from
        program analysis;                                                 these observations how tools will perform on specific verification
      • we experimentally demonstrate our technique—despite be-           tasks. Our machine learning technique is based on kernel methods
        ing more general and more widely applicable—to compare            (see e.g. [20]). In general, a kernel can be interpreted as a similarity
        favorably with existing approaches on the specific task of        measure on data instances (in our case verification tasks), with
        predicting rankings of software verification tools.               the idea that similar results (in our case rankings) are produced
All data of 2015 and software is available at https://github.com/         for similar instances. While kernel-based learning algorithms are
zenscr/PyPRSVT.                                                           completely generic, the kernel function itself is application-specific
                                                                          and, to achieve strong performance, needs to be designed in an
2   REPRESENTING VERIFICATION TASKS                                       appropriate way. In other words, a key question is how to define
Our objective is to predict rankings of software verification compe-      kernels suitable for the application at hand.
titions via machine learning. To this end, the learning algorithm            The simplest way of defining a kernel is via the inner product
has to be supplied with training data, which, in our case, is readily     of feature vectors, i.e., vectorial representations of data objects. In
available from the SV-COMP website. We start with explaining              the two approaches existing so far [6, 23], corresponding features
what kind of data our rank prediction technique is supplied with,         of programs, such as the number of loops, conditionals, pointer
and how this data is represented.                                         variables, or arrays in a program, are defined in an explicit way.
    The purpose of SV-COMP is to compare verification tools with          Obviously, this approach requires sufficient domain knowledge
respect to their effectiveness and efficiency. To this end, the tools     to identify those features that are important for the prediction
are supplied with verification tasks.                                     problem at hand. Our approach essentially differs in that features
                                                                          are specified in a more indirect way, namely by systematically
   Definition 2.1. A verification task (P, φ) consists of a program P     extracting (a typically large number of) generic features from a
(for SV-COMP written in C) and a property (also called specification)     suitable representation of the verification task. Selecting the useful
φ (typically written as assertion into the program).                      features and combining them appropriately is then basically left to
                                                                          the learner.
Figure 1 shows our running example PSUM of a verification task
(computing n times 2 via addition). In a verification run, a ver-         2 In addition, witnesses are part of the outcomes. Witnesses have only been part of the
ification tool is run on a verification task in order to determine        scoring scheme of 2017, and are thus for reasons of harmonisation of 2015 and 2017
whether the program fulfills the specification. The outcome of such       not considered here.
Predicting Rankings of Software Verification Competitions

                            Loop                       loop                                                If                                 conditional
                            Decl                       variable declaration                              Assign                               variable assignment
                            Incr                       variable increment                                Assert                               assertion
                             Ref                       variable reference                          Int Literal Small                          integer literal in [0,10]
                        Function Call                  function call                              Int Literal Medium                          integer literal in [10,100]
                       Function Return                 function return                             Int Literal Large                          integer literal > 100
                                                   Table 1: Some node identifiers and their meaning



                                          Int                                             Int                                               Int




                                         Decl                                         Decl                                               Decl




                                        Assign                                       Assign                                             Assign



                               Ref               Int_Literal_Small             Ref              input()
                                                                                                                                  Ref              Int_Literal_Small



                                                        Ref           Ref
                                                                                                                                Ref               Int_Literal_Small
                                                              <=

                                                                                                                        Ref             +

                                                               Loop

                                                                                                                       Assign

                              Incr

                                                                      Assert

                              Ref                                                                                                                 Control-Flow
                                                                          ||                         Ref                                          Data Dependence
                                           Ref           Ref
                                                                                     ==
                                                                                                                                                  Control Dependence
                           Int_Literal_Small       *                 ==                            Int_Literal_Small                              Syntactic Dependence




                                           Figure 2: Graph representation of PSUM eliding labelling ν


   But how to represent the verification tasks in a proper way?                                             1     int i = 0;                                           1   int i = 0;
The first idea is to use the source code itself (i.e., strings). How-                                       2     int n = abs(input());                                2   int n = abs(input());
ever, the source code of two programs might look very different                                             3     while (i < n)                                        3   while (i < n)
although the underlying program is actually the same (different                                             4            i++;                                          4          i++;
variable names, while instead of for loops, etc.). What we need is                                          5     assert (i == n);                                     5   assert (i != n);
a representation that abstracts from issues like variable names but
still represents the structure of programs, in particular dependen-                                             Figure 3: Two programs indistinguishable by our kernel
cies between elements of the program. These considerations (and
some experiments comparing different representations) have led to
a graph representation of programs combining concepts of three
existing program representations:
                                                                                                                         depends on an input variable (as is the case in program
                                                                                                                         PSUM ).
     Control flow graphs: CFGs record the control flow in pro-                                                         Abstract syntax trees: ASTs reflect the syntactical struc-
        grams and thus the overall structure with loops, condi-                                                          ture of programs according to a given grammar and can
        tionals etc.; these are needed, for example, to see loops in                                                     for instance help to reveal the complexity of expressions.
        programs.
     Program dependence graphs: PDGs [10] represent depen-                                                  Unlike CFGs and PDGs but (partly) alike ASTs, we abstract from
        dencies between elements in programs. We distinguish                                                concrete names occuring in programs. Nodes in the graph will
        control and data dependencies. This information is im-                                              thus not be labelled with statements or variables as occuring in the
        portant, for example, to detect whether a loop boundary                                             program, but with abstract identifiers. We let Lab be the set of all
                                                                                       Mike Czech, Eyke Hüllermeier, Marie-Christine Jakobs, Heike Wehrheim


such labels. Table 1 lists some identifiers and their meaning. The                            3.1    Label Ranking
following definition formalizes this graph representation.3                                   Consider a finite set of K alternatives identified by class labels
                                                                                              Y = {y1 , . . . , yK }; in our case, the alternatives correspond to the
   Definition 2.2. Let P be a verification task. The graph representa-                        verification tools to be compared. We are interested in total order
tion of P is a graph G = (N , E, s, t, ρ, τ , η) with                                         relations  on Y, that is, complete, transitive, and antisymmetric
       • N a set of nodes (basically, we build an AST for every                               relations, where yi  y j indicates that yi precedes y j in the order.
         statement in P, and use the nodes of these ASTs),                                    Formally, a total order  can be identified with a permutation
       • E a set of edges, with s : E → N denoting the start and                              π of the set [K] = {1, . . . , K }, such that π (i) is the position of
         t : E → N the end node of an edge,                                                   yi in the order. We denote the class of permutations of [K] (the
       • ρ : N → Lab a labelling function for nodes,                                          symmetric group of order K) by SK . By abuse of terminology,
       • τ : E → {CD, DD, SD, CF } a labelling function for edges                             though justified in light of the above one-to-one correspondence,
         reflecting the type of dependence: CD (control dependency)                           we refer to elements π ∈ SK as both permutations and rankings.
         and DD (data dependency) origin in PDGs, SD (syntactical                                In the setting of label ranking (see e.g. [25]), preferences on Y
         dependence) is the “consists-of” relationship of ASTs and                            are “contextualized” by instances x ∈ X, where X is an underlying
         CF (control flow) the usual control flow in programs,                                instance space; in our case, instances are programs to be verified.
       • ν : E → {T , F } a function labelling control dependence                             Thus, each instance x is associated with a ranking x of the label
         edges according to the valuation of the conditional they                             set Y or, equivalently, a permutation πx ∈ SK . More specifically,
         arise from. All other edges are labelled true.                                       since label rankings do not necessarily depend on instances in a
                                                                                              deterministic way, each instance x is associated with a probability
We let GV denote the set of all verification task graphs.                                     distribution P(· | x) on SK . Thus, for each π ∈ SK , P(π | x) denotes
                                                                                              the probability to observe the ranking π in the context specified by
Figure 2 depicts the graph representation of the verification task
                                                                                              x.
PSUM . The rectangle nodes represent the statements in the program
                                                                                                 The goal in label ranking is to learn a “label ranker”, that is, a
and act as root nodes of small ASTs. For instance, the rectangle
                                                                                              model
labelled Assert at the bottom, middle represents the assertion in
line 10. The gray ovals represent the AST parts below the root                                                               M : X → SK
nodes. We define the depth of nodes n, d(n), as the distance of a                             that predicts a ranking π̂ for each instance x given as an input. More
node to its root node. As an example, the depth of the Assert-node                            specifically, seeking a model with optimal prediction performance,
itself is 0, the depth of both ==-nodes is 2.                                                 the goal is to find a risk (expected loss) minimizer
    This graph representation allows us to see the key structural                                                            ∫
properties of a verification task, e.g., that the loop (condition) in                                        M ∗ ∈ argmin            D(M(x), π ) d P ,
                                                                                                                     M ∈M     X×SK
our example program depends on an assignment where the right-
hand-side is an input (which makes verification more complicated).                            where M is the underlying model class, P is the joint measure
With respect to semantical properties, our graph representation (as                           P(x, π ) = P(x)P(π | x) on X × SK and D is a loss function on SK .
well as all feature-based approaches relying on static analyses of                            A common example of such a loss is D(π , π̂ ) = 1 − S(π , π̂ ), where
programs) is less adequate. To see this, consider the two programs                            S(π , π̂ ) is the Spearman rank correlation [22]:
in Figure 3. They only differ in the assertion at line 5, which from                                                           ÍK
                                                                                                                              6 i=1 (π (i) − π̂ (i))2
its syntax is the same on both sides: a simple boolean expression on                                         S(π , π̂ ) = 1 −                         ∈ [−1, 1]
two variables of exactly the same type and dependencies. However,                                                                K(K 2 − 1)
verification of the left program is difficult for verification tools                          As training data D, a label ranker uses a set of instances x n (n ∈ [N ]),
which cannot generate loop invariants. Verification of the program                            together with information about the associated rankings πn .
on the right, however, is easy as it is incorrect (which can e.g. be
detected by a bounded unrolling of the loop). Here, we clearly see                            3.2    Ranking by Pairwise Comparison
the limits of any learning approach based on structural properties                            Ranking by pairwise comparison (RPC) is a meta-learning technique
of programs.                                                                                  that reduces a label ranking task to a set of binary classification
                                                                                              problems [12]. More specifically, the idea is to train a separate
3     PREDICTING RANKINGS                                                                     model (base learner) Mi, j for each pair of labels (yi , y j ) ∈ Y,
This section starts with a short description of the necessary back-                           1 ≤ i < j ≤ K; thus, a total number of K(K − 1)/2 models is needed
ground in machine learning. More specifically, we explain the prob-                           (see Figure 4 for an illustration).
lem of label ranking as well as the method of ranking by pairwise                                 For training, the original data D is first turned into binary classi-
comparison for solving this problem. In the second part, we recall                            fication data sets Di, j , 1 ≤ i < j ≤ K. To this end, each preference
binary classification with support vector machines and introduce                              information of the form yi x y j (extracted from full or partial
our kernel functions on verification tasks.                                                   information about a ranking πx ) is turned into a positive (classifica-
                                                                                              tion) example (x, 1) for the learner Mi, j ; likewise, each preference
                                                                                              y j x yi is turned into a negative example (x, 0). Thus, Mi, j
3 Actually, it only partly does, because a full formalization would require definitions of    trained on Di, j is intended to learn the mapping that outputs 1 if
CFGs, PDGs and ASTs which – due to lack of space – cannot all be given here.                  yi x y j and 0 if y j x yi . This mapping can be realized by any
Predicting Rankings of Software Verification Competitions


        T R A I N 	                                        P R E D I C T 	     training example (x i , yi ) ∈ Rm × {−1, +1} is given by yi (w >x i +b);
                                                                                 thus, a positive margin indicates that x i is on the right side of
                                                                                 the decision boundary, and hence classified correctly, whereas a
                                                                                 negative margin corresponds to a mistake on the training data.
                                                                                      The “soft margin” version allows for adding a slack variable
                                                               RANKING	  
                                                                                 ξ i ≥ 0 and defines the margin as yi (w >x i +b) + ξ i for each example
                                                                                 x i ; this is necessary in the case of data that is not linearly separable.
                                                                                 Obviously, the values of the slack variables should be kept small, i.e.,
    DECOM-­‐	                                          BINARY	                 the problem comes down to finding a reasonable balance between
   POSITION	                                           PREDICTION	  
                                                                                 a large (soft) margin and a small amount of slack. This problem
                                                                                 can be formalized in terms of a constrained quadratic optimization
                                                                                 problem:
                                                                                                                                       N
                                                                                                                      (                      )
                                                                                                     ∗ ∗                1            Õ
Figure 4: Illustration of the RPC approach (for K = 4). At                                         (w , b ) = argmin      kw k + C
                                                                                                                               2
                                                                                                                                          ξi
training time (left), the original data D is split into K(K −1)/2                                              w,b, ξ   2             i=1
smaller data sets, one for each pair of labels, and a binary
                                                                                 subject to the constraints
classifier is trained on each of these data sets. If a prediction
for a new instance is sought (right), this instance is submit-                                     yi (w >x i + b) ≥ 1 − ξ i ,          ξi ≥ 0 ,        (1)
ted to each of the binary models, and the pairwise prefer-
ences obtained as predictions are combined into a complete                       where C is a parameter that controls the penalization of errors on
ranking π via a ranking procedure P.                                             the training data (indicated by a non-zero ξ i ). Instead of solving
                                                                                 this problem directly, it is often more convenient to solve its dual.
                                                                                    At prediction time, a new instance x 0 ∈ Rm is classified posi-
binary classifier. Instead of a {0, 1}-valued classifier, one can of             tive or negative depending on whether it lies above or below the
course also employ a scoring classifier. For example, the output of a            hyperplane (w ∗ , b ∗ ). Instead of only returning a binary decision,
probabilistic classifier would be a number in the unit interval [0, 1]           the distance from the hyperplane is often reported as kind of mea-
that can be interpreted as a probability of the preference yi x y j .           sure of certainty (with the idea that the closer an instance to the
In our approach, we use support vector machines as base learners                 decision boundary, the less certain the prediction). As a disadvan-
[19, 24] .                                                                       tage of this measure, note that the distance is not normalized and
   At classification time, a query x 0 ∈ X is submitted to the com-              therefore difficult to interpret and compare. So-called Platt scal-
plete ensemble of binary learners. Thus, a collection of predicted               ing is a post-processing step, in which distances are mapped to
pairwise preference degrees Mi, j (x), 1 ≤ i, j ≤ K, is obtained. The            [0, 1] via a logistic transformation; thus, each instance is assigned a
problem, then, is to turn these pairwise preferences into a ranking              (pseudo-)probability of belonging to the positive class [14].
of the label set Y. To this end, different ranking procedures can                   In the dual formulation of the above optimization problem, train-
be used. The simplest approach is to extend the (weighted) voting                ing instances x i , x j never occur in isolation but always in the form
procedure that is often applied in pairwise classification [7]: For              of inner products hx i , x j i. This allows for the “kernelization” of
each label yi , a score                                                          SVMs, simply be replacing such inner products by values k(x i , x j )
                                                                                 of a so-called kernel function k(·).
                                Õ
                        Si =          Mi, j (x 0 )
                              1≤j,i ≤K
                                                                                    Definition 3.1. A function k : X × X → R is a positive semi-
is derived (where Mi, j (x 0 ) = 1 − M j,i (x 0 ) for i > j), and then the       definite kernel iff k is symmetric, i.e., k(x, x 0 ) = k(x 0, x), and
labels are sorted according to these scores. Despite its simplicity,
this ranking procedure has several appealing properties. Apart from                                      N Õ
                                                                                                         Õ N
its computational efficiency, it turned out to be relatively robust                                                c i c j k(x i , x j ) ≥ 0
in practice and, moreover, it possesses some provable optimality                                         i=1 j=1
properties in the case where Spearman’s rank correlation is used
                                                                                 for arbitrary N , arbitrary instances x 1 , . . . , x N ∈ X and arbitrary
as an underlying accuracy measure [11].
                                                                                 c 1 , . . . , c N ∈ R.
3.3       Support Vector Machines                                                   If k(·) is a proper kernel function, one can guarantee the ex-
As already said, support vector machines (SVMs) are used as base                 istence of an induced feature space F (which is a Hilbert space)
learners in RPC. SVMs are so-called “large margin” classifiers [19].             and a feature map ϕ : X → F such that hϕ(x), ϕ(x 0 )i = k(x i , x j ).
They separate positive from negative training instances in Rm by                 Thus, the computation of inner products in the (typically very high-
means of a linear hyperplane that maximizes the minimum distance                 dimensional) space F can be replaced by the evaluations of the
of any of the training instances from the hyperplane (decision                   kernel, which in turn allows a linear model to be fit in F without
boundary). Formally, a hyperplane {x | w >x + b = 0} in Rm is                    ever accessing that space or computing the image ϕ(x i ) of a training
characterized by the normal vector w ∈ Rm and the bias term                      instance x i —this is called the “kernel trick”. The learning algorithm
b ∈ R. Then, encoding the two classes by ±1, the margin of a                     only requires access to the Gram matrix, i.e., the value of the kernel
                                                                          Mike Czech, Eyke Hüllermeier, Marie-Christine Jakobs, Heike Wehrheim

Algorithm 1 relabel (Graph relabelling)                                          exhausted. This bound is used to regulate the depth of subtrees
Input:                                                                           considered. Note that this is a test only, not a proof of isomorphism.
    G = (N , E, s, t, ρ, τ , ν ) graph                                               For making this Weisfeiler-Lehman test act as a kernel for verifi-
    z : Σ∗ → Σ injective compression function                                    cation tasks, we made three adaptations to the graph relabelling,
    η : N → 2E neighbour function                                                giving rise to Algorithm 1:
    m iteration bound                                                                  (1) extension to directed multigraphs,
Output:                                                                                (2) customization to specific neighbours of nodes, and
    relabelled graph G                                                                 (3) integration of edge labels.
 1: for i = 1 to m do                                                            In Algorithm 1, we use the notation h. . . | . . .i for list comprehen-
 2:     for n ∈ N do                                                             sions, defining a sequence of values. Moreover, z is the compression
            Auд(n) := z ρ(s(e)) ⊕ τ (e) ⊕ ν (e) | e ∈ η(n)
                                               
 3:                                                                              function compressing sequences of labels into new labels (which
 4:         Auд(n) := sort(Auд(n))                                               thus needs to be injective). In our case, we use numbers as labels,
 5:         str (n) := concat(Auд(n))                                            i.e., Σ = N with the usual ordering ≤. To this end, we first map all
 6:         str (n) := ρ(n) ⊕ str (n)                                            node identifiers and edge labels to N. Every newly arising sequence
 7:         ρ(n) := z(str (n))                                                   then simply gets a new number assigned. The neighbour function η
 8: return G                                                                     is used to customize kernels by selectively choosing the neighbours
                                                                                 to be considered during augmentation. Thereby, we can specialize
                                                                                 our kernels to just control flow or just data dependence edges, for
for each pair of training instances:                                             example. The functions sort and concat sort sequences of labels (in
                k(x 1 , x 1 )   k(x 1 , x 2 )   ...    k(x 1 , x N )             ascending order) and concatenate sequences, respectively.
              © k(x , x )       k(x 2 , x 2 )   ...    k(x 2 , x N ) ª®              This lets us finally define our kernels for verification tasks.
                    2 1
         G = ­­
              ­
                     ..              ..         ..           ..       ®
                                                                                    Definition 3.2. Let G i = (Ni , Ei , si , ti , ρ i , τi , νi ), i = 1, 2 be graph
                      .               .            .          .
                                                                      ®
                                                                                 representations of verification tasks, z : Σ∗ → Σ a compression
              ­                                                       ®
              « k(x N , x 1 )   k(x N , x 2 )   ...    k(x N , x N ) ¬
                                                                                 function, m ∈ N an iteration bound, d ∈ N a depth for subtrees and
Note that the instance space X, on which the kernel is defined, is               ηi : Ni → 2Ei neighbour functions. The verification graph kernel
not necessarily an Euclidean space. Instead, X can be any space                   (d,m)
                                                                                 kη1,η2,z : GV × GV → R is defined as
or set of objects. In particular, this allows SVMs to be trained on
                                                                                                                 m
structured (non-vectorial) objects. In general, a kernel function can                                                     relabel(G 1 , z, η 1 , m),
                                                                                                                                                            
                                                                                                                   kd
                                                                                           (d,m)
                                                                                                                 Õ
                                                                                         kη1,η2,z (G 1 , G 2 ) =
be interpreted as a kind of similarity measure on X, i.e., the more                                                       relabel(G 2 , z, η 2 , m)
                                                                                                                     i=1
similar instances x i , x j , the larger k(x i , x j ). Next, we address the
question of how to define appropriate kernel functions on verifica-               with
                                                                                  k d (G, G 0 )                          kδd (n, n 0 ) and
                                                                                                         Õ Õ
tion tasks.                                                                                          =
                                                                                                         n ∈N n 0 ∈N 0
3.4    Graph Kernels for Verification Tasks                                                              
                                                                                                             δ (ρ 1 (n), ρ 2 (n 0 ))   if d(n) ≤ d ∧ d(n 0 ) ≤ d
                                                                                     kδd (n, n 0 )   =                                                           ,
Verification tasks are represented by specific graphs, whence our                                            0                         else
kernel needs to operate on graphs. A number of graph kernels                     where δ is a Dirac kernel defined as δ (u, w) = 1 if u equals w and 0
already exist, for instance based on comparisons of shortest paths               otherwise.
or random walks of graphs. However, most of these graph kernels
do not scale well to large graphs [21]. As our graphs are representa-            Intuitively, the kernels count the number of equally labelled nodes
tions of programs with several thousands lines of code, and hence                in all iterations, where the iteration bound steers to what extent
very large, we have chosen to proceed from our own kernel devel-                 subtrees of root ASTs nodes are considered, the neighbour function
opment based on Weisfeiler-Lehman subtree kernels [21], which are                controls what edges are taken into account, and the depth d fixes
known to scale better.                                                           whether a node is considered at all. For the latter, remember that
   Weisfeiler-Lehman kernels are extensions of the Weisfeiler-Lehman             the depth of a node is its distance to its top-level AST node. By
test of isomorphism between two discretely labelled, undirected                  incorporating the depth, we have the option to consider or ignore
graphs [26]. This test basically compares graphs according to their              details of expressions.
node labels. For taking edges into account, node labels are extended             We can show the following result (for the proof, we refer to [5]):
with information about neighbouring nodes in three steps:                                                                  (d,m)
                                                                                     Theorem 3.3. The kernel kη1,η2,z is positive semi-definite.
      Augmentation: Concatenate label of node n with labels of
          its neighbours,                                                           Our kernels can now be used in a support vector machine within
      Sorting: Sort this sequence according to predefined order on               the ranking by pairwise composition approach outlined above.
          labels,
      Compression: Compress thus obtained sequences into new                     4      IMPLEMENTATION AND EXPERIMENTAL
          labels.                                                                       EVALUATION
These steps are repeated until the node label sets of the two graphs             In our experiments, we studied the performance of our method
differ or until a predefined bound on the number of iterations is                for rank prediction in the SV-COMP 2015 and 2017. To this end,
Predicting Rankings of Software Verification Competitions

Table 2: SV-COMP 2015 – Prediction accuracy (mean and standard deviation) in terms of the Spearman rank correlation (higher
is better, minimum is −1, maximum is +1).

                                            Kernel / Data Set           SAFETY        TERMINATION         MEMSAFETY
                                                  k CF (CFG)          .616 ± .002       .709 ± .008        .774 ± .003
                                     k DD (data dependency)           .615 ± .004       .680 ± .009        .761 ± .003
                                  k CD (control dependency)           .607 ± .005       .674 ± .008        .767 ± .005
                                              k CD,DD (PDG)           .611 ± .005       .692 ± .006        .771 ± .009
                                    k CF,CD,DD (PDG + CFG)            .614 ± .004       .692 ± .002        .784 ± .003
                                      weighted combination            .615 ± .002       .711 ± .007        .769 ± .004
                                              features of [6]         .576 ± .006       .609 ± .011        .692 ± .006
                                            default predictor         .560 ± .003       .332 ± .008        .604 ± .002

Table 3: SV-COMP 2017 – Prediction accuracy (mean and standard deviation) in terms of the Spearman rank correlation (higher
is better, minimum is −1, maximum is +1).

                                            Kernel / Data Set           SAFETY        TERMINATION         MEMSAFETY
                                                  k CF (CFG)          .635 ± .003       .657 ± .007        .755 ± .004
                                     k DD (data dependency)           .618 ± .003       .635 ± .006        .754 ± .007
                                  k CD (control dependency)           .627 ± .002       .637 ± .006        .756 ± .005
                                              k CD,DD (PDG)            .630± .005       .644 ± .003        .757 ± .007
                                    k CF,CD,DD (PDG + CFG)            .632 ± .004       .658 ± .009        .756 ± .003
                                      weighted combination            .634 ± .003       .664 ± .010        .756 ± .003
                                              features of [6]         .560 ± .004       .560 ± .006        .717 ± .001
                                            default predictor         .452 ± .003       .339 ± .004        .668 ± .001


we compared six variants of our kernel with respect to prediction                   In addition, we constructed a default predictor for comparison: the
accuracy, each of which focuses on different aspects of a program.                  default predictor takes all rankings of the data set used for learning,
Such kind of customization of kernels becomes possible thanks to                    determines the ranking which minimizes the distance (wrt. Spear-
the two neighbouring functions η 1 and η 2 . In our case, neighbours                man rank correlation) to these rankings and always predicts this
are chosen according to the type of edge connecting them. We                        default ranking without any learning.
define η ` , ` ∈ {CD, DD, SD, CF } to be η ` (n) = {e | τ (e) = ` ∧ s(e) =             We constructed the following data sets for our experiments:
n}, and let η L (n) = ` ∈L η ` (n) for a node n. For our kernels, we
                      Ð
                                                                                    SAFETY, TERMINATION, and MEMSAFETY. Each data set consists
always use the same neighbouring function on both graphs. Hence,                    of several verification tasks taken from the SV-COMP 2015 and 2017
we will just use the edge labels employed in neighbouring functions                 benchmark sets. To provide a comprehensive analysis under vary-
as indizes for kernels.                                                             ing conditions, each data set represents a different property type
   Our experiments include kernels                                                  (safety, termination, and memory safety). In case of SV-COMP 2015,
           (d,m)
      • k {CF } (control-flow),                                                     SAFETY is a data set of 483 verification tasks originating from the
                                                                                    SV-COMP categories Loops, BitVectors, Floats, Simple, ControlFlow-
           (d,m)
      • k {C D } (control dependencies),                                            Integer, and HeapManipulation. For 2017, our SAFETY set consists
           (d,m)
      • k {DD } (data dependencies),                                                of 637 verification tasks out of the categories ReachSafety-Bitvectors,
                                                                                    ReachSafety-ControlFlow, ReachSafety-Heap, ReachSafety-Floats and
           (d,m)
      • k {CD,DD } (control and data dependencies), and                             ReachSafety-Loops. The set of considered tools in SAFETY consists
           (d,m)
      • k {CF,CD,DD } (control-flow, data- and control-                             of the tools, which participated in all these categories (6 tools for
                                                                                    2015 and 11 tools for 2017). TERMINATION is a data set of verifica-
         dependencies).
                                                                                    tion tasks taken from the category Termination, 393 tasks in 2015
In addition, we included an equally weighted linear combination                     and 507 for 2017. In this data set, we consider tools that participated
 (d,m)
klin of some of our kernels, which is defined as                                    in this category and successfully proved or disproved termination
        (d,m)                                                                       on at least one verification task (5 tools both for 2015 and 2017).
       kl in   (G 1 , G 2 ) =
                                                                                    MEMSAFETY is the data set of verification tasks consisting of tasks
       1 k (d,m) (G , G ) + 1 k (d,m) (G , G ) + 1 k (d,m) (G , G )
       3 {CF }       1 2      3 {CD } 1 2        3 {DD } 1 2                        from the category MemorySafety, 205 for 2015 and 181 for 2017.
(one can easily check that this is again a valid kernel, see e.g. [5]).             Again, we considered only tools that report at least one correct
To get an insight on how the prediction accuracy performs com-                      outcome (9 tools in 2015 and 11 tools in 2017).
pared to state-of-the-art approaches, we also included the accuracy                    For the computation of our verification graphs, we used the
achieved by using the feature vectors from Demyanova et al. [6].                    configurable software analysis framework CPAChecker [2]: To
                                                                   Mike Czech, Eyke Hüllermeier, Marie-Christine Jakobs, Heike Wehrheim


obtain control-flow and AST information, we used the integrated           this paper, we have proposed a method for predicting rankings of
C parser. In case of data dependencies, we utilized the integrated        verification tools on given programs. Our rank prediction tech-
reaching definition analysis as is described in [10]. For the sake        nique builds on existing methods for label ranking via pairwise
of simplicity, we ignored complex dependencies introduced by              comparison. To this end, we have developed an expressive repre-
pointers. Also according to [10], we computed control dependencies.       sentation of source code, capturing various forms of dependencies
Eventually, we built another extension of the CPAChecker that             between program elements. Instead of explicitly extracting features
combines all the collected information into one graph using the           of programs tailored towards verification, we have constructed a
JGraphT library4 . To solve our label ranking problem, we integrated      kernel that compares programs according to their elements and the
the RPC approach and our kernel framework into the scikit-learn           connections between them. Due to its generic nature, we specu-
library5 . There, we also employed the implementation of support          late that this kernel will also be useful for other sorts of learning
vector machines (with Platt scaling) offered by scikit-learn. Finally,    problems on programs—a conjecture we shall verify in future work.
we integrated the feature vectors of [6] through the tool Verifolio6 .       Our approach can be seen as a tool for algorithm selection, a
All the code and data (of 2015) is available via GitHub7 .                problem that has also been tackled by other authors [6, 23, 27].
   To examine the prediction accuracy for each configuration, we          Other applications of machine learning include the learning of
performed a 10-fold cross-validation. A k-fold cross-validation is a      programs from examples ([13, 15]) and the prediction of properties
commonly used technique for model assessment. First, the data is          of programs (e.g., types for program variables [16] or malware in
divided into k subsets of equal size. Then, one subset is used as test    Android apps [17]). Just like our approach, the latter also uses
set, whereas the learning algorithm trains a model on the remaining       Weisfeiler-Lehman subtree kernels (on CFGs only). A machine
k − 1 subsets. This procedure is repeated exactly k times, each time      learning approach to software verification itself has recently been
using one of the folds for testing, and the overall performance is        proposed in [4]. However, to the best of our knowledge, the use of
obtained as the average of the k test performances thus produced.         machine learning for predicting rankings of tools (algorithms) has
After each step of the cross-validation, we compared the actual           never been tried so far.
true rankings on the test sets to the corresponding predicted rank-          For future work, we are planning to generalize our methodology
ings (with RPC and SVMs) using the Spearman rank correlation.             by exploiting properties (features) of verification tools, which are
The overall accuracy is then the average over all the accuracies          only identified by their name so far. Recently, a generalization of
encountered in each step.                                                 label ranking called dyad ranking has been proposed, in which not
   In Table 2 (SV-COMP 2015) and Table 3 (SV-COMP 2017), we               only the instances but also the alternatives to be ranked can be
report the average prediction accuracies (and standard deviations)        described in terms of properties [18]. As an important advantage
in terms of the Spearman rank correlation; note that an average           of this approach, note that it in principle allows for ranking alter-
accuracy of 0 would be obtained by guessing rankings at random,           natives with very few or even no training information so far. This
while +1 stands for predictions that perfectly coincide with the true     becomes possible by generalizing via the feature descriptions (al-
ranking (and −1 for completely reversing that ranking). As can be         ternatives with similar properties are expected to perform similarly
seen, our approach shows a rather strong predictive performance.          and hence to occupy similar ranks). In our case, this would mean,
Depending on the verification task, different kernels achieve the         for example, that predictions can be made for a new verification tool
best results, though the differences in performance are statistically     that has never been tried so far—provided, of course, meaningful
non-significant. More importantly, our approach significantly out-        descriptions of such tools are available. Developing corresponding
performs the one of [6] as well as the default predictor on all tasks.    representations is one of the challenges we will address next.
This applies to the data of 2015 as well as 2017.
   Table 4 (SV-COMP 2015) and Table 5 (SV-COMP 2017) show
the average training and testing times during the 10-fold cross           REFERENCES
validation (using the precomputed Gram matrix), i.e., the time in          [1] Dirk Beyer. 2015. Software Verification and Verifiable Witnesses - (Re-
seconds for the training with 9 folds of the input data and the time           port on SV-COMP 2015). In TACAS 2015 (LNCS), Christel Baier and Cesare
                                                                               Tinelli (Eds.), Vol. 9035. Springer, 401–416. DOI:http://dx.doi.org/10.1007/
for computing the rankings (testing) for the remaining fold. As                978-3-662-46681-0-31
expected, training a model is more time-consuming than using it            [2] Dirk Beyer and M. Erkan Keremoglu. 2011. CPAchecker: A Tool for Configurable
for prediction. Moreover, like for accuracy, there are no signifi-             Software Verification. In Computer Aided Verification ,CAV (Lecture Notes in
                                                                               Computer Science), Ganesh Gopalakrishnan and Shaz Qadeer (Eds.), Vol. 6806.
cant differences between the kernels. Interestingly, the kernels are           Springer, 184–190. DOI:http://dx.doi.org/10.1007/978-3-642-22110-1 16
sometimes even faster than the simple feature representation of            [3] Bernhard E. Boser, Isabelle Guyon, and Vladimir Vapnik. 1992. A Training
                                                                               Algorithm for Optimal Margin Classifiers. In ACM Conference on Computational
[6].                                                                           Learning Theory, COLT, David Haussler (Ed.). ACM, 144–152. DOI:http://dx.doi.
                                                                               org/10.1145/130385.130401
5     CONCLUSION                                                           [4] Yu-Fang Chen, Chiao Hsieh, Ondrej Lengál, Tsung-Ju Lii, Ming-Hsien Tsai, Bow-
                                                                               Yaw Wang, and Farn Wang. 2016. PAC learning-based verification and model
In the recent years, machine learning has attracted increasing at-             synthesis. In International Conference on Software Engineering, ICSE, Laura K.
tention in software engineering and related fields, where it has               Dillon, Willem Visser, and Laurie Williams (Eds.). ACM, 714–724. DOI:http:
                                                                               //dx.doi.org/10.1145/2884781.2884860
been used, for example, in program construction and analysis. In           [5] Mike Czech. 2016. Predicting Rankings of Software Verification Tools using Kernels
                                                                               for Structured Data. Master’s thesis. Paderborn University.
4 http://jgrapht.org
                                                                           [6] Yulia Demyanova, Thomas Pani, Helmut Veith, and Florian Zuleger. 2015. Em-
5 http://scikit-learn.org
                                                                               pirical Software Metrics for Benchmarking of Verification Tools. In CAV 2015
6 http://forsyte.at/software/verifolio/
                                                                               (LNCS), Daniel Kroening and Corina S. Pasareanu (Eds.), Vol. 9206. Springer,
7 https://github.com/zenscr/PyPRSVT                                            561–579. DOI:http://dx.doi.org/10.1007/978-3-319-21690-4 39
Predicting Rankings of Software Verification Competitions

                    Table 4: SV-COMP 2015 – Time (in seconds) for training and testing (mean ± standard deviation)

                                                            Kernel / Data Set     SAFETY         TERMINATION             MEMSAFETY
                                                                  k CF (CFG)     367 ± .634        147 ± 1.10             128 ± .728
                                                     k DD (data dependency)      461 ± 13.8        172 ± 4.74             137 ± 1.81
                                                  k CD (control dependency)

                                       training
                                                                                 393 ± 2.14        160 ± 2.32             129 ± 6.35
                                                              k CD,DD (PDG)      359 ± 1.53        131 ± .627             126 ± .445
                                                    k CF,CD,DD (PDG + CFG)       318 ± 5.06        125 ± 1.54             125 ± 2.72
                                                      weighted combination       349 ± 9.13        127 ± 1.17             120 ± .200
                                                              features of [6]    266 ± 3.55        138 ± .282             150 ± .410
                                                                  k CF (CFG)      .021 ± .0         .011 ± .0              .035 ± .0
                                                     k DD (data dependency)       .020 ± .0         .011 ± .0              .034 ± .0
                                                  k CD (control dependency)       .021 ± .0         .011 ± .0              .034 ± .0
                                       testing




                                                              k CD,DD (PDG)       .020 ± .0         .012 ± .0              .034 ± .0
                                                    k CF,CD,DD (PDG + CFG)       .022 ± .005        .013 ± .0              .036 ± .0
                                                      weighted combination        .019 ± .0         .011 ± .0              .033 ± .0
                                                              features of [6]     .026 ± .0         .013 ± .0              .019 ± .0

                    Table 5: SV-COMP 2017 – Time (in seconds) for training and testing (mean ± standard deviation)

                                                            Kernel / Data Set      SAFETY        TERMINATION             MEMSAFETY
                                                                  k CF (CFG)     5584 ± 762         470 ± 3.92            237 ± 1.68
                                                     k DD (data dependency)      7229 ± 731         529 ± 8.11            260 ± 1.23
                                                  k CD (control dependency)
                                      training




                                                                                 4301 ± 207         510 ± 7.48            243 ± 15.2
                                                              k CD,DD (PDG)      5533 ± 490         440 ± 10.1             231 ± 2.0
                                                    k CF,CD,DD (PDG + CFG)       3774 ± 276        394 ± 10.4             231 ± 1.23
                                                      weighted combination       3809 ± 99.4        413 ± 5.40            235 ± 1.29
                                                              features of [6]    4914 ± 273         711 ± 21.0            331 ± 5.25
                                                                  k CF (CFG)     .347 ± .048       .044 ± .002              .104 ± .0
                                                     k DD (data dependency)      .341 ± .020       .043 ± .002            .106 ± .003
                                                  k CD (control dependency)      .290 ± .018       .038 ± .002             .116 ± .02
                                      testing




                                                              k CD,DD (PDG)      .424 ± .018       .039 ± .002            .104 ± .001
                                                    k CF,CD,DD (PDG + CFG)       .286 ± .007       .046 ± .003            .104 ± .008
                                                      weighted combination       .294 ± .022       .048 ± .005            .112 ± .011
                                                              features of [6]    .534 ± .026       .077 ± .003              .042 ± .0


 [7] J. Fürnkranz. 2002. Round Robin Classification. Journal of Machine Learning                Languages, POPL, Sriram K. Rajamani and David Walker (Eds.). ACM, 111–124.
     Research 2 (2002), 721–747.                                                                 DOI:http://dx.doi.org/10.1145/2676726.2677009
 [8] Johannes Fürnkranz and Eyke Hüllermeier (Eds.). 2010. Preference Learning.         [17]   Justin Sahs and Latifur Khan. 2012. A Machine Learning Approach to Android
     Springer. DOI:http://dx.doi.org/10.1007/978-3-642-14125-6                                   Malware Detection. In European Intelligence and Security Informatics Conference,
 [9] Johannes Fürnkranz and Eyke Hüllermeier. 2010. Preference Learning and                    EISIC, Nasrullah Memon and Daniel Zeng (Eds.). IEEE Computer Society, 141–147.
     Ranking by Pairwise Comparison. See [8], 65–82. DOI:http://dx.doi.org/10.1007/              DOI:http://dx.doi.org/10.1109/EISIC.2012.34
     978-3-642-14125-6-4                                                                  [18]   D. Schäfer and E. Hüllermeier. 2015. Dyad Ranking using a Bilinear Plackett-
[10] Susan Horwitz and Thomas W. Reps. 1992. The Use of Program Dependence                       Luce Model. In Proceedings ECML/PKDD–2015, European Conference on Machine
     Graphs in Software Engineering. In International Conference on Software Engi-               Learning and Knowledge Discovery in Databases. Porto, Portugal.
     neering, ICSE, Tony Montgomery, Lori A. Clarke, and Carlo Ghezzi (Eds.). ACM         [19]   B. Schölkopf and AJ. Smola. 2001. Learning with Kernels: Support Vector Machines,
     Press, 392–411. DOI:http://dx.doi.org/10.1145/143062.143156                                 Regularization, Optimization, and Beyond. MIT Press.
[11] E. Hüllermeier and J. Fürnkranz. 2010. On predictive accuracy and risk mini-       [20]   John Shawe-Taylor and Nello Cristianini. 2004. Kernel Methods for Pattern
     mization in pairwise label ranking. J. Comput. System Sci. 76, 1 (2010), 49–62.             Analysis. Cambridge University Press.
[12] E. Hüllermeier, J. Fürnkranz, W. Cheng, and K. Brinker. 2008. Label Ranking by     [21]   Nino Shervashidze, Pascal Schweitzer, Erik Jan van Leeuwen, Kurt Mehlhorn,
     Learning Pairwise Preferences. Artificial Intelligence 172 (2008), 1897–1917.               and Karsten M. Borgwardt. 2011. Weisfeiler-Lehman Graph Kernels. Journal of
[13] Tessa Lau. 2001. Programming by Demonstration: a Machine Learning Approach.                 Machine Learning Research 12 (2011), 2539–2561. http://dl.acm.org/citation.cfm?
     Ph.D. Dissertation. University of Washington.                                               id=2078187
[14] John Platt. 1999. Probabilistic outputs for support vector machines and compar-      [22]   Charles Spearman. 1904. The proof and measurement of association between
     isons to regularized likelihood methods. In Advances in Large Margin Classifiers.           two things. American Journal of Psychology 15 (1904), 72–101.
     MIT Press, 6–74.                                                                     [23]   Varun Tulsian, Aditya Kanade, Rahul Kumar, Akash Lal, and Aditya V. Nori.
[15] Veselin Raychev, Pavol Bielik, Martin T. Vechev, and Andreas Krause. 2016.                  2014. MUX: algorithm selection for software model checkers. In Conference on
     Learning programs from noisy data. In Symposium on Principles of Programming                Mining Software Repositories, MSR, Premkumar T. Devanbu, Sung Kim, and Martin
     Languages, POPL, Rastislav Bodı́k and Rupak Majumdar (Eds.). ACM, 761–774.                  Pinzger (Eds.). ACM, 132–141. DOI:http://dx.doi.org/10.1145/2597073.2597080
     DOI:http://dx.doi.org/10.1145/2837614.2837671                                        [24]   V.N. Vapnik. 1998. Statistical Learning Theory. John Wiley & Sons.
[16] Veselin Raychev, Martin T. Vechev, and Andreas Krause. 2015. Predicting Pro-         [25]   Shankar Vembu and Thomas Gärtner. 2010. Label Ranking Algorithms: A Survey.
     gram Properties from ”Big Code”. In Symposium on Principles of Programming                  See [8], 45–64. DOI:http://dx.doi.org/10.1007/978-3-642-14125-6 3
                                                                               Mike Czech, Eyke Hüllermeier, Marie-Christine Jakobs, Heike Wehrheim


[26] Boris Weisfeiler and A.A. Lehman. 1968. A reduction of a graph to a canonical
     form and an algebra arising during this reduction. Nauchno Technicheskaya
     Informatsia 2, 9 (1968), 12–19.
[27] Lin Xu, Frank Hutter, Holger H. Hoos, and Kevin Leyton-Brown. 2011. SATzilla:
     Portfolio-based Algorithm Selection for SAT. CoRR abs/1111.2249 (2011). http:
     //arxiv.org/abs/1111.2249
