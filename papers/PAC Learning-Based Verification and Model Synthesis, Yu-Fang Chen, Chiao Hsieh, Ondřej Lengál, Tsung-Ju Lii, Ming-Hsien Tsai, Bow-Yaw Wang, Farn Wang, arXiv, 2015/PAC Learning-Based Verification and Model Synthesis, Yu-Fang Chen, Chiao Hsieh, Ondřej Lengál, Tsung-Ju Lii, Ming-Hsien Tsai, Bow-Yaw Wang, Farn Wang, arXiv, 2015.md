                                             PAC Learning-Based Verification and Model Synthesis

                                                     Yu-Fang Chen                                Chiao Hsieh                           Ondřej Lengál
                                                     Academia Sinica                           Academia Sinica                        Academia Sinica
                                                                                          National Taiwan University            Brno University of Technology
                                                       Tsung-Ju Lii                           Ming-Hsien Tsai                         Bow-Yaw Wang
                                                     Academia Sinica                            Academia Sinica                        Academia Sinica
                                                National Taiwan University
                                                                                                  Farn Wang
arXiv:1511.00754v1 [cs.SE] 3 Nov 2015




                                                                                          National Taiwan University

                                        ABSTRACT                                                          that this work reduces the dichotomy between formal and
                                        We introduce a novel technique for verification and model         practical software engineering techniques.
                                        synthesis of sequential programs. Our technique is based             In our technical setting, we assume programs are an-
                                        on learning a regular model of the set of feasible paths in       notated with program assertions. A program assertion is
                                        a program, and testing whether this model contains an in-         a Boolean expression intended to be true every time it is
                                        correct behavior. Exact learning algorithms require check-        encountered during program execution. Given a program
                                        ing equivalence between the model and the program, which          with assertions, our task is to check whether all assertions
                                        is a difficult problem, in general undecidable. Our learning      evaluate to true on all possible executions. In principle, the
                                        procedure is therefore based on the framework of probably         problem can be solved by examining all program executions.
                                        approximately correct (PAC) learning, which uses sampling         It is, however, prohibitive to inspect all executions exhaus-
                                        instead and provides correctness guarantees expressed using       tively since there may be infinitely many of them. One way
                                        the terms error probability and confidence. Besides the ver-      to simplify the analysis is to group the set of program exe-
                                        ification result, our procedure also outputs the model with       cutions to paths of a control flow graph.
                                        the said correctness guarantees. Obtained preliminary ex-            A control flow graph (CFG) is derived from the syntactic
                                        periments show encouraging results, in some cases even out-       structure of a program source code. Each execution of a pro-
                                        performing mature software verifiers.                             gram corresponds to a path in its control flow graph. One
                                                                                                          can therefore measure the completeness of software testing
                                        1.   INTRODUCTION                                                 on CFGs. Line coverage, for instance, gives the ratio of ex-
                                           Formal verification of software aims to prove software         plored edges in the CFG of the tested program, while branch
                                        properties through rigorous mathematical reasoning. Con-          coverage is the ratio of explored branches of this CFG. Note
                                        sider, for example, the C statement assert(x > 0) spec-           that such syntactic measures of code coverage approximate
                                        ifying that the value of the variable x must be positive.         program executions only very roughly. Executions that dif-
                                        If the assertion is formally verified, it cannot be violated      fer in the number of iterations in a simple program loop have
                                        in any possible execution during runtime. Formal verifica-        the same line and branch coverages, although their compu-
                                        tion techniques are, however, often computationally expen-        tation may be drastically different. A full syntactic code
                                        sive. Although sophisticated heuristics have been developed       coverage does not necessarily mean all executions have been
                                        to improve scalability of the techniques, formally verifying      explored by software testing.
                                        real-world software is still considered to be impractical.           Observe that program executions traversing the same path
                                           A common technique to ensure quality in industry is soft-      in a CFG perform the same sequence of operations (although
                                        ware testing. Errors in software can be detected by explor-       maybe with different values). Consider a path corresponding
                                        ing different software behaviors via injecting various testing    to a program execution in a CFG. Such a path can be char-
                                        vectors. Testing cannot, however, guarantee software is free      acterized by the sequence of decisions that the execution
                                        from errors. Consider again the assertion assert(x > 0).          took when traversing conditional statements in the CFG.
                                        Unless all system behaviors are explored by testing vectors,      We call a sequence of such decisions a decision vector. A de-
                                        it is unsound to conclude that the value of x is always posi-     cision vector is feasible if it represents one or more (possibly
                                        tive. Various techniques have been proposed to improve its        infinitely many) program executions, and infeasible if it rep-
                                        coverage, but it is an inherent feature of software testing       resents a sequence of branching choices than can never occur
                                        that it cannot establish program properties conclusively.         in an execution of the program. To check whether all asser-
                                           In this paper, we propose a novel learning-based approach      tions evaluate to true on all executions, it suffices to examine
                                        that aims to balance scalability and coverage of existing soft-   all feasible decision vectors and check they do not represent
                                        ware engineering techniques. In order to be scalable, as for      any assertion-violating program execution. Although feasi-
                                        software testing, our new technique explores only a subset of     bility of a decision vector can be determined by using an off-
                                        all program behaviors. Moreover, we apply machine learn-          the-shelf Satisfiability Modulo Theories (SMT) solver, the
                                        ing to generalize observed program behaviors for better se-       set of feasible decision vectors is in general difficult to com-
                                        mantic coverage. Our technique allows software engineers          pute exactly. Therefore, we apply algorithmic learning, in
                                        to combine scalable testing with high-coverage formal anal-       particular the framework of probably approximately correct
                                        yses and improve the quality assurance process. We hope           learning, to construct a regular approximation of this set.
   Within the framework of probably approximately correct          quantified guarantee accompanied by a faithful approximate
(PAC) learning with queries, learning algorithms query             model for several examples that are challenging for program
about target concepts to construct hypotheses. The con-            verifiers and concolic testers. This approximate model can
structed hypotheses are then validated by sampling. If a hy-       later be reused, e.g., for verifying the same program with
pothesis is invalidated by witnessing a counterexample,            a different set of program assertions.
learning algorithms refine the invalidated hypothesis by the          Our contributions are summarized in the following:
witness and more queries. If, on the other hand, a hypothe-            • We show the PAC learning algorithm can be applied
sis conforms to all samples, PAC learning algorithms return               to synthesize a faithful approximate model of the set
the inferred hypothesis with statistical guarantees. In our               of feasible decision vectors of a program. Such a model
approach, we adopt a PAC learning algorithm with queries                  can be useful in many different aspect of program veri-
to infer a regular language approximation to the set of fea-              fication (cf. Section 12 for details). We believe it is not
sible decision vectors of a program.                                      hard to adopt our approach to handle different type of
   To grasp the statistical guarantees provided by PAC learn-             systems (e.g., black box systems) and to obtain ap-
ing, consider the task of checking defects in a large shipment            proximate models on a different level of abstraction
using uniform sampling. Because of the size of the shipment,              (e.g., on a function call graph).
it is impractical to check every item. We instead want to              • We develop a verification procedure based on the ap-
know, with a given confidence δ, if the defect probability is            proximate model obtained from PAC learning. The
at most ǫ. This can be done by selecting r (to be deter-                 procedure integrates the advantages of both testing
mined later) randomly chosen items. If all chosen items are              and verification. It uses testing techniques to col-
good, the method reports that the defect probability is at               lect samples and catch bugs. The PAC learning al-
most ǫ. We argue the simple method can err with proba-                   gorithm generalizes the samples to obtain an approxi-
bility at most 1 − δ. Suppose r randomly chosen items are                mate model that can then be analyzed by verification
tested without any defect, but the defect probability is, in             techniques for statistical guarantees.
fact, more than ǫ. Under this thesis, the probability that r
random items are all good is lower than (1 − ǫ)r . That is,        2. PRELIMINARIES
the method is incorrect with probability lower than (1 − ǫ)r .
Take r such that (1−ǫ)r < 1−δ. The simple method reports              Let X be the set of program variables and F the set of
incorrect results with probability at most 1 − δ; we equiva-       function and predicate symbols. We use X ′ for the set {x′ |
lently say the result of the method is PAC (ǫ, δ)-correct.         x ∈ X }. The set T [X , F] of transition formulae consists
   Using a similar argument, it can be shown that our PAC          of well-formed first-order logic formulae over X , X ′ , and F.
learning algorithm returns a regular set approximating the         For a transition formula f ∈ T [X , F] and n ∈ N, we use
set of feasible decision vectors of the program with the error     f hni to denote the formula obtained from f by replacing
probability ǫ and confidence δ of our choice. If the inferred      all free variables x ∈ X and x′ ∈ X ′ with xhni and xhn+1i
set contains no decision vector representing an assertion-         respectively.
violating program execution, our technique concludes the              We represent a program with a single procedure using
verification with statistical guarantees about correctness.        a control flow graph. (Section 9 extends the notion to pro-
   Our learning-based approach finds a balance between for-        grams with multiple procedures and procedure calls.) A con-
mal analysis and testing. Rather than exploring program            trol flow graph (CFG) is a graph G = (V, E, vi , vr , Ve , XFP )
behaviors exhaustively, our technique infers an approxima-         where V = Vb ∪Vs is a finite set of nodes consisting of disjoint
tion of the set of feasible decision vectors by queries and        sets of branching nodes Vb and sequential nodes Vs , vi ∈ V
sampling. Although the set of feasible decision vectors is         is the initial node, vr ∈ Vs is the return node, Ve ⊆ V is the
in general not computable, PAC learning with queries may           set of error nodes, XFP ⊆ X is the set of formal parameters,
still return a regular set approximation of it with a quantified   and E is a finite set of edges such that E ⊆ V × T [X , F] × V
guarantee. Such an approximate model with statistical guar-        and the following conditions hold:
antees can be useful for program verification. With an ap-             • for any branching node vb ∈ Vb , there are exactly
proximate model that is PAC (ǫ, δ)-correct and proved to be               two nodes v0′ , v1′ ∈ V with (vb , f0 , v0′ ), (vb , f1 , v1′ ) ∈ E,
free from assertion violation, one can conclude that the pro-             where f0 , f1 ∈ T [X , F] are transition formulae;
gram is also PAC (ǫ, δ)-correct. The statistical guarantees            • for any non-return sequential node vs ∈ Vs \{vr }, there
are different from syntactic code coverages in software test-            is exactly one node v ′ ∈ V with (vs , f, v ′ ) ∈ E; and
ing. Recall that our application of PAC learning works over            • for the return node vr ∈ Vs , there is no v ′ ∈ V such
decision vectors. Decision vectors in turn represent program             that (vr , f, v ′ ) ∈ E for any f ∈ T [X , F].
executions. When our technique does not find any assertion
                                                                   We say v ′ is a successor of v if (v, f, v ′ ) ∈ E. Assume,
violation, the statistical guarantees give software engineers
                                                                   moreover, that the two successors v0′ and v1′ of the branch-
a semantic coverage about program executions. Along with
                                                                   ing node v are ordered. Intuitively, the ‘1’ corresponds to
conventional syntactic coverages, such information may help
                                                                   the if branch and the ‘0’ corresponds to the else branch.
software engineers estimate the quality of software.
                                                                   We call v0′ and v1′ the 0-successor and 1-successor of v re-
   We implement a prototype, named Pac-Man (PAC
                                                                   spectively. Similarly, f0 and f1 are called the 0-transition
learning-based Model synthesizer and ANalyzer), of our pro-
                                                                   and 1-transition formulae of v. Note that the definition of
cedure based on program verifiers CPAchecker, CBMC,
                                                                   a CFG allows us to describe nondeterministic choice, which
and the concolic tester Crest. We evaluate the proto-
                                                                   is commonly used to model the environment. To be more
type on the benchmarks from the recursive category of SV-
                                                                   specific, a nondeterministic choice from a branching node v
COMP 2015 [1]. The results are encouraging—we can find
                                                                   can be represented by defining     V both the 0-transition and
all errors that can be found by Crest. We also provide
                                                                   1-transition formulae of v as x∈X x = x′ .
   A path in the CFG G is a sequence π                                       =                                   The system is PAC (ǫ, δ)-correct
hv0 , f1 , v1 , f2 , v2 , . . . , fm , vm i such that v0 = vi and                  Found a feasible error decision vector
(vj , fj+1 , vj+1 ) ∈ E for every 0 ≤ j < m. The path π is
                                                                                                   Mechanical Teacher
feasible if the path formula m                    hki
                                         V
                                           k=1 fk     is satisfiable. It is an
error path if vj ∈ Ve for some 0 ≤ j ≤ m. The task of our                                Resolving Mem-             Resolving Equiv-
                                                                                         bership Queries           alence Queries by
analysis is to check whether G contains a feasible error path.                             (Section 6)            Sampling (Section 5)
   A sequence w = a1 a2 · · · an with aj ∈ {0, 1} for 1 ≤ j ≤ n
is called a word over {0, 1}. The length of w is |w| = n.
                                                                                    Mem(w)           yes/no      Equ(C)          counterexample
The word of length 0 is the empty word λ. We also use w[j]
to denote the j-th symbol aj . If u, w are words over {0, 1},
u · w denotes the concatenation of u and w. A language L                                  PAC Automata Learning Algorithm
over {0, 1} is a set of words over {0, 1}.                                                          (Section 4)
   We introduce the function decision that maps a path π
of G to a sequence of decisions made in the branching                                Figure 1: Components of our verification procedure
nodes traversed by π. Formally, decision is a function from
paths to words over {0, 1} defined recursively as follows:                       whether there is a feasible error path in G. More concretely,
decision(hv0 , f1 , v1 , f2 , v2 , . . . , fm , vm i) = decision(hv0 , f1 i) ·   consider the set Π of feasible paths in G and the set B of
decision(hv1 , f2 , v2 , . . . , fm , vm i) such that                            error paths in G. We call the languages decision(Π) and
  decision(hvi) = λ                                                              decision(B) over the alphabet {0, 1} as feasible decision vec-
                                                                                 tors and error decision vectors respectively. The program is
                      λ          if v ∈ Vs ,
                    
                                                                                correct if the intersection decision(Π) ∩ decision(B) is empty,
                     0          if v ∈ Vb and
                    
                    
                                                                                 i.e., if G contains no feasible error path.
decision(hv, f i) =              f is the 0-transition formula of v,
                                                                                    Representation of the language decision(Π) of all feasible
                     1          if v ∈ Vb and
                    
                    
                                                                                 decision vectors in G is not so easy. In general, this lan-
                    
                                 f is the 1-transition formula of v.
                                                                                 guage may not be regular or even computable. In our pro-
For a path π, decision(π) is the decision vector of π. We lift                   cedure, we construct a candidate finite automaton C that
decision to a set of paths Π and define decision vectors of Π                    approximates decision(Π), the set of feasible decision vec-
as decision(Π) = {decision(π) | π ∈ Π}.                                          tors of G. We infer C using a probably approximately correct
   A finite automaton (with λ-moves) A is a tuple A =                            (PAC) online automata learning algorithm [2]. The use of
(Σ, Q, qi , ∆, F ) consisting of a finite alphabet Σ, a finite                   PAC learning provides us with statistical guarantees about
set of states Q, an initial state qi ∈ Q, a transition rela-                     the correctness of C—we can claim that C is PAC (ǫ, δ)-
tion ∆ ⊆ Q × (Σ ∪ {λ}) × Q, and a set of accepting states                        correct, i.e., with confidence δ, the deviation of L(C) from
F ⊆ Q. A transition (q, λ, q ′ ) ∈ ∆ is called a λ-transition.                   decision(Π) is less than ǫ (we give a proper explanation of
A word w over Σ is accepted by A if there are states                             the terms in Section 4).
q0 , . . . , qm ∈ Q and symbols (or λ’s) a1 , . . . , am ∈ (Σ ∪ {λ}),               On the other hand, it is straightforward to convert G to
such that w = a1 · · · am , for every 0 ≤ j < m there is                         a finite automaton B accepting the set of all error decision
a transition (qj , aj+1 , qj+1 ) ∈ ∆, and further q0 = qi and                    vectors decision(B). Intuitively, states of B correspond to
qm ∈ F . The language of A is defined as L(A) = {w |                             nodes of G, the initial state of B corresponds to the initial
w is accepted by A}. A language R is regular if R = L(A)                         node of G, and accepting states of B correspond to G’s error
for some finite automaton A. The finite automaton A is de-                       nodes. An edge from a sequential node is translated to a
terministic if its transition relation is a function from Q × Σ                  λ-transition. For a branching node, the edges to its 0- and
to Q. For any finite automaton A, there exists a determin-                       1-successors are translated to transitions over symbols 0 and
istic finite automaton (DFA) B such that L(A) = L(B).                            1 respectively (cf. Section 7).
   A pushdown automaton (PDA) is a tuple P =                                        A high-level overview or our learning procedure is given
(Σ, Q, Γ, qi , ∆, F ) where Σ is a finite input alphabet, Q is                   in Figure 1 (the procedure is similar in structure to the one
a finite set of states, Γ is a finite stack alphabet, qi ∈ Q                     of [2]). It consists of two main components: The learning
is the initial state, F ⊆ Q is the set of final states, and                      algorithm asks the teacher two kinds of questions: mem-
∆ ⊆ Q × (Σ ∪ {λ}) × (Γ ∪ {λ}) × (Γ ∪ {λ}) × Q is a transi-                       bership (“Is a given decision vector feasible?”) and equiv-
tion relation. We use (q, [a; b/c], q ′ ) to denote the transition               alence (“Is a given candidate finite automaton PAC (ǫ, δ)-
(q, a, b, c, q ′ ), and we sometimes simplify (q, [a; λ/λ], q ′ ) to             correct?”) queries. The teacher resolves the queries, at the
(q, a, q ′ ). We define a configuration of P as a pair (q, γ) ∈                  same time observing whether some of the tested decision vec-
Q×Γ∗ . A word w over Σ is accepted by P if there exists a se-                    tors corresponds to a feasible error path. By posing these
quence of configurations (q0 , γ0 ), . . . , (qm , γm ) ∈ Q × Γ∗ and             queries, either the learning algorithm iteratively constructs
a sequence of symbols (or λ’s) a1 , . . . , am ∈ (Σ ∪ {λ}), such                 a PAC (ǫ, δ)-correct approximation of decision(Π) or our pro-
that w = a1 · · · am , q0 = qi , γ0 = ǫ, qm ∈ F , and for every                  cedure finds a feasible error decision vector.
0 ≤ j < m it holds that there are some bj , bj+1 ∈ (Γ ∪ {λ})                        As with other online learning-based techniques, we need
and γj′ , γj+1′
                   ∈ Γ∗ such that γj = bj γj′ , γj+1 = bj+1 γj+1
                                                             ′
                                                                 , and           to devise a mechanical teacher that answers queries from
there is (qj , [aj+1 ; bj /bj+1 ], qj+1 ) ∈ ∆. The language of P is              the learning algorithm. Checking membership queries (i.e.,
defined as L(P ) = {w | w is accepted by P }.                                    membership in the set decision(Π) of feasible decision vec-
                                                                                 tors) is relatively easy—for example, given a decision vec-
3.    OVERVIEW                                                                   tor d, we obtain its corresponding path π by unfolding the
  In this section, we give an overview of our verification pro-                  CFG G according to d, and use an off-the-shelf solver to
cedure. Let G be a CFG of a program. Our goal is to check                        decide whether π is feasible or not (cf. Section 6).
   When the automata learning algorithm infers a candidate        We modified the used learning algorithm in a similar way.
finite automaton C, we need to check whether L(C) ap-             To be more specific, when the classical learning algorithm
proximates decision(Π), i.e., whether C is PAC (ǫ, δ)-correct.    poses an equivalence query Equ(C), we first check whether
Since we cannot compare decision(Π) with L(C) directly, we        there exists a decision vector c such that c ∈ L(C) ∩ L(B)
employ the sampling-based approximate equivalence tech-           and then test if c ∈ decision(Π).
nique of PAC learning. While generally unsound, the tech-           1. In case that the two tests identified a decision vector
nique still provides statistical guarantee about the correct-          c such that c ∈ L(C) ∩ L(B) and c 6∈ decision(Π),
ness of the inferred model (details are given in Section 5).           then c is in the difference of L(C) and decision(Π) and
                                                                       hence a valid counterexample for the classical learning
4.    PAC AUTOMATA LEARNING                                            algorithm to refine the next conjecture automaton C.
   Here we explain the PAC automata learning algorithm
that we use to find an approximation to decision(Π). Clas-          2. In case that the two tests identified a decision vector
sical PAC automata learning algorithm cannot be used di-               c such that c ∈ L(C) ∩ L(B) and c ∈ decision(Π), then
rectly for the purpose of program verification. It has to              c is a feasible error decision vector and we report c to
be modified to handle the case when the program contains               the user.
an error. The classical PAC automata learning algorithm             3. In case that L(C) ∩ L(B) = ∅, the modified learning
was obtained from modifying the requirement of the exact               algorithm poses an equivalence query Equ(C) to the
automata learning algorithm [3]. Our modification follows              teacher.
the same route. In this section, we first describe the classi-
cal “exact” automata learning algorithm of regular languages        Given a teacher answers membership and equivalence
and then describe how to modify it for verification. Then we      queries about decision(Π), the modified automata learning
explain how to relax the requirement of an exact automata         algorithm has the following properties.
learning algorithm to infer an approximation to decision(Π).        Lemma 1. Assume decision(Π) is a regular set. The
                                                                  modified automata learning algorithm eventually finds a
4.1 Exact Learning of Regular Languages                           counterexample c ∈ L(B) ∩ decision(Π) when L(B) ∩
  Suppose R is a target regular language such that its de-        decision(Π) 6= ∅. It eventually finds a finite automaton rec-
scription is not directly accessible. Automaton learning al-      ognizing decision(Π) when L(B) ∩ decision(Π) = ∅.
gorithms [2, 18, 14, 5] infer automatically a finite automa-
ton AR recognizing R. The setting of an online learning              Observe that when the program does not contain any er-
algorithm assumes a teacher who has access to R and can           ror, the behavior of the modified learning algorithm is identi-
answer the following two types of queries:                        cal to the classical one and hence is still an exact automata
                                                                  learning algorithm. Next we explain how to relax the re-
     • Membership query Mem(w): is the word w a member            quirements of the exact automata learning algorithm to ob-
       of R, i.e., w ∈ R?                                         tain a PAC automata learning algorithm that is suitable for
                                                                  program verification.
     • Equivalence query Equ(C): is the language of the finite
       automaton C equal to R, i.e., L(C) = R? If not, what       4.3 Probably Approximately Correct Learning
       is a counterexample to this equality (a word in the           The techniques for learning automata we just discussed in
       symmetric difference of L(C) and R)?                       the previous section assume a teacher who has the ability to
                                                                  answer equivalence queries. Such an assumption is, however,
The learning algorithm will then construct a finite automa-       invalid in our procedure. Checking decision(Π) = L(C) can
ton AR such that L(AR ) = R by interacting with the               be undecidable. Angluin showed in [3] that if we substitute
teacher. Such an algorithm works iteratively: In each it-         equivalence queries with sampling, we can still make statis-
eration, it performs membership queries to get information        tical claims about the difference of the inferred set and the
about R from the teacher. Using the results of the queries,       target set.
it proceeds by constructing a candidate automaton C and,             Assume that we are given a probability distribution D
finally, makes an equivalence query Equ(C). If L(C) = R,          over the elements of a universe U, and a hypothesis in the
the algorithm terminates with C as the resulting finite au-       form
tomaton AR . Otherwise, the teacher returns a word w dis-
tinguishing L(C) from the target language R. The learning                            Prob w∈U |D [¬ϕ(w)] ≤ ǫ.
algorithm uses w to modify the conjecture for the next it-        In the hypothesis, the term Prob w∈U |D [¬ϕ(w)] denotes the
eration. The mentioned learning algorithms are guaranteed         probability that the formula ϕ(w) is invalid for w chosen
to find a finite automaton AR recognizing R using a number        randomly from U according to the distribution D. We call ǫ
of queries polynomial to the number of states of the mini-        the error parameter and use the term confidence to denote
mal DFA recognizing R. In the rest of the paper, we denote        the least probability that the hypothesis is correct. We say
“online automata learning” simply as “automata learning”.         that ϕ(w) is PAC (ǫ, δ)-valid if Prob w∈U |D [¬ϕ(w)] ≤ ǫ with
                                                                  confidence δ.
4.2 Learning for Program Verification                               In the setting of automata learning, the considered uni-
   Under the context of program verification, it may be the       verse is Σ∗ and the target regular language is R ⊆ Σ∗ .
case that decision(Π) ∩ L(B) 6= ∅; in such a case, our pro-       The task of an equivalence query Equ(C) is changed from
cedure should return a feasible error path in the program.        checking exact equivalence, which we can express as check-
This is very similar to the setting of learning-based verifica-   ing that ∀w ∈ Σ∗ : w ∈      / R ⊖ L(C) (we use ⊖ to de-
tion [11, 9], where the learning algorithm is modified to re-     note the symmetric difference operator), to checking ap-
turn a counterexample in case the system contains an error.       proximate equivalence, i.e., checking whether the formula
ϕ(w) = w ∈  / R ⊖ L(C) is PAC (ǫ, δ)-valid. In other words,       a concolic tester [12, 19, 7], which is an efficient means for
we check whether Prob w∈Σ∗ |D [w ∈ R ⊖ L(C)] ≤ ǫ with con-        exploring decision vectors corresponding to rare paths.
fidence δ. For a fixed R and a candidate C, we say that C           We describe the technique and prove its properties in the
is PAC (ǫ, δ)-correct if w ∈
                           / R ⊖ L(C) is PAC (ǫ, δ)-valid.        rest of this section.
   The teacher checks the PAC (ǫ, δ)-correctness of C by pick-
ing r samples according to D and testing if all of them are       5.1 Concolic Testing
not in R ⊖ L(C). For the i-th equivalence query of the learn-        Concolic testing is a testing approach that explores paths
ing algorithm, the number of samples qi needed to establish       in the CFG of a program while searching for bugs. The
that C is PAC (ǫ, δ)-correct is given by Angluin in [2] as        algorithm begins with a decision vector generated by ran-
                                                              domly picked input values. Then, it finds the next decision
                        1      1
                qi =       ln      + i ln 2   .            (1)    vector by flipping some decision made in the chosen path
                        ǫ     1−δ                                 and obtains new input values that lead the program execu-
Since the inferred set C is guaranteed to be PAC (ǫ, δ)-          tion according to the new path. This mechanism gives rare
correct, this approach is termed probably approximately cor-      paths a much greater chance to be explored. The selection of
rect (PAC) learning [21].                                         which decision should be flipped depends on the used search
                                                                  strategy of the tester.
5.     RESOLVING EQUIVALENCE QUERIES                                 In our procedure, we use the concept of a batched sample.
       BY SAMPLING                                                A batched sample is defined as a set of decision vectors of the
                                                                  size k (where k is a given parameter) obtained from a con-
  The current section discusses how to design a mechanism
                                                                  colic tester by exploring k paths using its search strategy.
that the teacher can use for equivalence queries to provide
                                                                  We denote Dk the distribution over elements of (Σ∗ )k ob-
the PAC (ǫ, δ)-correctness guarantee, as defined in Section 4.
                                                                  tained in this way. Our procedure restarts the concolic tester
Given a probability distribution D over the set of feasible
                                                                  after taking every batched sample. The previous point gives
decision vectors decision(Π), we can use D to give a formal
                                                                  us the guarantee that the probability of taking each batched
definition of the quality of a candidate automaton C. In
                                                                  sample remains the same during the execution our procedure
particular, we use as a measure the probability with which
                                                                  (we assume that the concolic tester does not keep state in-
a decision vector chosen randomly from decision(Π) (accord-
                                                                  formation between its restarts), and that the distribution
ing to the distribution D) is contained in C.
                                                                  is IID and, therefore, meets condition 2 defined above. The
  A sampling mechanism offering such a distribution must
                                                                  principal functioning of concolic testers guarantees that con-
satisfy the following conditions:
                                                                  dition 1 is also met.
     1. Only decision vectors in decision(Π) are sampled.
                                                                  5.2 Generalized Stochastic Equivalence
     2. The samples are independent and identically dis-             In this section, we show that our sampling mechanism
        tributed (IID), i.e., the distribution is fixed and the   using batched samples has the property required for the
        probability of sampling a particular element does not     PAC (ǫ, δ)-correctness guarantee of the learning algorithm
        depend on the previously picked samples.                  given in Section 4.3.
                                                                     Recall that for the set of feasible decision vectors of a pro-
In this paragraph, we introduce the random input sampling         gram decision(Π) and a candidate automaton C inferred by
mechanism. We treat all nondeterministic choices and for-         the learning algorithm using some distribution D over Σ∗ ,
mal parameters of the program as input variables and as-          if the teacher gives the answer yes for the equivalence query
sume that all input variables are over finite domains. Each       Equ(C), it guarantees with confidence δ that
set of initial values of input variables yields a path in the
CFG of the program. Based on this observation, random in-                  Prob w∈Σ∗ |D [w ∈ decision(Π) ⊖ L(C)] ≤ ǫ.          (2)
put sampling works by (1) picking uniformly at random a set
of initial values for input variables of the program and then     Since our sampling technique uses batched samples from the
(2) obtaining the corresponding decision vector by traversing     universe Uk = (Σ∗ )k w.r.t. the distribution Dk instead of el-
the CFG of the program using the picked values. The sam-          ements of Σ∗ and distribution D, we need to change the
pling mechanism forms a distribution such that the proba-         provided guarantee in our modification of the learning algo-
bility of a decision vector d being chosen is proportional to     rithm. If our algorithm answers yes, it guarantees that
the number of program paths corresponding to d.                      Prob S∈Uk |D [∃w ∈ S : w ∈ decision(Π) ⊖ L(C)] ≤ ǫ        (3)
   The issue of random input sampling is that it suffers                         k

from the well-known fact that coverage of input values is         with confidence δ (we hereafter use the term PAC (ǫ, δ)-
not a good approximation of program path coverage. De-            correct to denote this form of guarantee).
pending on the sizes of input domains of program vari-               When a teacher receives an equivalence query Equ(C),
ables, some paths might have only a negligible probabil-          it uses a concolic tester to obtain qi (given in (1)) batch
ity of being selected—for instance, given two 64-bit integers     samples. For each batch sample S, the teacher checks if
x and y, the probability of taking the true branch in the test    there exists a decision vector w ∈ S such that w ∈   / L(C)
x == 0 && y == 0 is equal to 2−128 . The situation gets even      (by definition w ∈ decision(Π)). The teacher answers yes if
worse for input variables over unbounded domains. Even            there is no such w. Otherwise, the teacher checks if w is
with an extremely high coverage rate of input variables’ val-     an error decision vector and either reports w as a feasible
ues, many paths may still not be explored, while other are        error decision vector or returns w to the learning algorithm
explored repeatedly. In order to get a sampling mechanism         to refine the next conjecture.
with a better distribution over program paths, we developed          The following lemma shows that if we use the number qi
a technique that randomly explores program’s paths using          batched samples for testing the equivalence, we obtain the
modified PAC (ǫ, δ)-correctness guarantee from (3).                        Informally, B contains a state for every node and a transi-
                                                                           tion for every edge of G. It reads a symbol in each state cor-
   Lemma 2. Let ǫ and δ be the error and confidence param-                 responding to a branching node and performs λ-transitions
eters, and R be the target language. If no decision vector                 for states corresponding to sequential nodes. For every error
w∈ / L(C) is found in the qi batched samples, then it holds                node, B reads all remaining symbols and accepts the input
that C is PAC (ǫ, δ)-correct.                                              word. It is straightforward to see that B accepts exactly the
                                                                           set of decision vectors corresponding to error paths in G.
Based on the fact that L(C) ∩ L(B) = ∅ (the property of the
modified learning algorithm in Section 4.2) and the lemma                    Lemma 3. Let G = (V, E, vi , vr , Ve , XFP ) be a CFG and
above, we obtain the following corollary.                                  B the set of error paths in G. Let B be the error trace
                                                                           automaton for G. It holds that L(B) = decision(B).
  Corollary 1. Let ǫ and δ be the error and confidence
parameters, and R be the target language. If no decision                     In Section 9, we describe an extension of our procedure
vector w ∈ / L(C) is found in qi batched samples, then it                  to programs with procedure calls. Because representing the
holds that the program is PAC (ǫ, δ)-correct.                              set of error decision vectors using a finite automaton is in
                                                                           this setting imprecise, the section also discusses an extension
                                                                           that represents the set of error paths in a program with
6.     RESOLVING MEMBERSHIP QUERIES                                        procedure calls using pushdown automata.
  In this section, we describe how a membership query
Mem(d) in the algorithm in Figure 1 is discharged by the                   8. THE MAIN PROCEDURE
teacher. Let Π be the set of feasible paths of a CFG G.                       We summarize our procedure in this section. Let G be
When the learning algorithm asks a membership query                        the CFG of the verified program, k be the size of a batched
Mem(d), the teacher needs to check whether the decision                    sample, ǫ be the error parameter, and δ be the confidence
vector d is in the set of feasible decision vectors decision(Π).           parameter. The goal of our procedure is to either find a fea-
To answer the query, the teacher first constructs a path                   sible error decision vector of G or show that G is PAC (ǫ, δ)-
π = hv0 , f1 , v1 , f2 , v2 , . . . , vm−1 , fm , vm i in G such that      correct. In the latter case, we also accompany our answer
     • there are exactly |d| occurrences of branching nodes in             with a PAC (ǫ, δ)-correct regular representation of the set of
       the prefix hv0 , f1 , v1 , f2 , v2 , . . . , vm−1 i of π,           feasible decision vectors of G. Let Π be the set of feasible
                                                                           paths of G, Dk be the distribution defined by our sampling
     • if vk is the j-th branching node in π, it holds that
                                                                           mechanism (cf. Section 5), and L(B) be the set of error de-
       decision(vk , fk+1 ) = d[j], and
                                                                           cision vectors of G (cf. Section 7).
    • vm−1 is a branching node.                                               A detailed flow chart of our procedure can be found in
Recall that π is a feasible path if and only if ϕ = m
                                                   V        hji            Figure 2. First, the bottom part of the figure describes our
                                                     j=1 fj
is satisfiable. Therefore, the teacher can simply construct                learning algorithm. We extend the online automata learning
the formula ϕ from the path π and check its satisfiability                 algorithm with two additional tests for verification, as de-
using an off-the-shelf constraint solver.                                  scribed in Section 4.2. In particular, when the automata
   Alternatively, the teacher can check feasibility by trans-              learning algorithm outputs a candidate C, before sending
lating the path into a sequence of program statements (with                teacher the equivalence query Equ(C), we first test whether
conditions removed and substituted by assertions on the val-               L(C) contains a feasible error decision vector c. In case it
ues of the conditions) and asking a symbolic executor or soft-             does, we report c as an error. Otherwise, in the case c is
ware model checker whether the final line of the constructed               both in L(C) and L(B) but is not feasible, we return c to
program is reachable. The alternative option is easier to im-              the learning algorithm to further refine the conjecture.
plement but usually suffers from some performance penalty.                    The top part of the figure describes our design of a me-
                                                                           chanical teacher. The task of the teacher is to answer queries
7.     ERROR DECISION VECTORS                                              from the learning algorithm. Membership queries of the
  Let B be the set of error paths in a CFG. In this section,               form Mem(w) can be answered by constructing the path
we show how we construct a finite automaton accepting the                  corresponding to the decision vector w and the associated
set of all error decision vectors decision(B) of the given CFG.            path formula, which is then solved using a constraint solver
This automaton will later be intersected with the automaton                (cf. Section 6). Equivalence queries, on the other hand, are
representing the set of feasible paths to determine whether                discharged using a concolic tester by checking whether there
the CFG contains a feasible error path.                                    is a decision vector s in the set of batched samples S such
                                                                           that it does not belong to the language of C (cf. Section 5).
   Definition 1. Let G = (Vb ∪ Vs , E, vi , vr , Ve , XFP ) be             If no such a decision vector exists, we conclude that the
a CFG. We define the error trace automaton for G as the                    program is PAC (ǫ, δ)-correct. Otherwise, we test whether
finite automaton B = ({0, 1}, Vb ∪ Vs , vi , ∆E , Ve ) where ∆E            s ∈ L(B); if this holds, we report that we have found a feasi-
is defined as follows:                                                     ble error decision vector. In the case s ∈
                                                                                                                    / L(B), it holds that
                                                                           s is a feasible decision vector in decision(Π) but not in the
     • (v, 0, v0′ ) ∈ ∆E if v ∈ Vb \ Ve , (v, f0 , v0′ ) ∈ E, and v0′ is   language of the current conjecture L(C). If this happens,
       the 0-successor of v;                                               we return s to the automata learning algorithm to refine
     • (v, 1, v1′ ) ∈ ∆E if v ∈ Vb \ Ve , (v, f1 , v1′ ) ∈ E, and v1′ is   the conjecture and continue with the next iteration of the
       the 1-successor of v;                                               learning loop.
     • (v, λ, v ′ ) ∈ ∆E if v ∈ Vs \ Ve and (v, f, v ′ ) ∈ E; and             In general, our procedure is not guaranteed to terminate.
                                                                           When the procedure terminates and reports an error (either
     • (v, 0, v), (v, 1, v) ∈ ∆E if v ∈ Ve .                               by the teacher or the learning algorithm), a feasible error
                s is a feasible error decision vector                                               The system is PAC (ǫ, δ)-correct
                                                     yes         Mechanical Teacher       no
           Build and check                                                                                                 Sample a set
           the path formula                        s ∈ L(B)?                        ∃s ∈ S.s 6∈ L(C)?                      S of decision
                                                                        yes                                     S
            of w (Section 6)                                                                                            vectors (Section 5)
                                                            no

  Mem(w)          yes/no       s is a counterexample
                                                                                                                         Equ(C)
                                                       no
 start    Build/Refine Model      Equ(C)                                yes                                    yes     c is a feasible error
                                               ∃c.c ∈ L(C)∩L(B)?                     c ∈ decision(Π)?
         (Learning Algorithm)                                                                                          decision vector
                                                                                               no
         c is a counterexample
                                 PAC Automata Learning Algorithm (Section 4)

                                     Figure 2: A detailed flow chart of our verification procedure
decision vector is found and the program is reported to be                    where V, vi , vr , Ve , and XFP are defined in the same way
incorrect. If the teacher approves an approximate finite au-                  as for a CFG, and E ⊆ (V × T [X , F] × V ) ∪ (V × (P ×
tomaton C, our procedure reports that C is an approximate                     T [X , F] × T [X , F]) × V ) is an extended set of edges that
model of decision(Π) w.r.t. the PAC (ǫ, δ)-correctness guar-                  apart from local CFG edges (v, f, v ′ ) for f ∈ T [X , F] also
antee, which, in turn, implies that the program is PAC (ǫ, δ)-                contains procedure call edges e = (v, (p, gin , gout ), v ′ ) for
correct. From Lemma 2, we have the following theorem                          (p, gin , gout ) ∈ P × T [X , F] × T [X , F] and sequential nodes
                                                                              v. The gin and gout components of e correspond to for-
   Theorem 1. Let ǫ and δ be the error and confidence pa-                     mulae for passing actual values to formal parameters of p
rameters respectively and Π be the set of feasible paths of                   (formula gin ) and passing the return value of p back to the
a given CFG G. If our procedure terminates with an approx-                    caller procedure (formula gout ).
imate finite automaton C, the program is PAC (ǫ, δ)-correct.                     In this extension, we define a program as a set of CFGCs
Moreover, we obtain the following corollary.                                  prog = {G1 , . . . , Gn } together with a (bijective) mapping
                                                                              cfgc prog : P → prog that assigns procedure names to CFGCs.
   Corollary 2. Suppose our procedure reports a program                       We abuse notation and use prog to denote cfgc prog , i.e.,
P is PAC (ǫ, δ)-correct. If we run the concolic tester with                   prog (p) denotes the CFGC of a procedure p in a program
the same search strategy and batch size used in our procedure                 prog . We assume that all CFGCs in prog have pairwise
on P , with confidence δ, the concolic tester will find an error              disjoint sets of nodes, and further assume an entry point
with a probability less than ǫ.                                               main ∈ P.
  Thanks to the properties of the modified automata learn-                       In this paragraph, we give an informal description of how
ing algorithm, when decision(Π) is a regular set, our al-                     we extend the definition of a path from a program consisting
gorithm is guaranteed to terminate and either (1) return                      of single CFG to a program consisting of a set of CFGCs and
a counterexample c ∈ L(B) ∩ decision(Π) or (2) find an ap-                    a dedicated entry point. Given a procedure call edge e in
proximate model of decision(Π) that is disjoint with L(B).                    a CFGC G, we call the inlining of e in G the CFGC G′
                                                                              obtained from G by substituting e with the CFGC of the
9.   HANDLING PROCEDURE CALLS                                                 called procedure. We use Jprog K to denote the set of CFGs
                                                                              obtained from prog (main) by performing all possible (even
   In this section, we extend our formalism of CFGs to han-                   recursively called) sequences of inlinings, and removing any
dle programs with multiple procedures. We use a PDA to                        left procedure call edges from the output CFGCs. A path
represent error decision vectors in this setting. The issue of                in prog is then a sequence π = hv0 , f1 , v1 , f2 , v2 , . . . , fm , vm i
using finite automata to represent error decision vectors in                  such that there exists a CFG G′ ∈ Jprog K for which it holds
the said setting is that when returning from a procedure call,                that π ∈ G′ .
a finite automaton cannot remember an unbounded num-
ber of return points (in the case of recursive procedures).
Therefore, an overapproximation, such as a nondeterminis-                     9.2 Encoding Error Decision Vectors with
tic jump to any possible return point, needs to be used. The                      Pushdown Automata
said overapproximation is, however, too imprecise and yields                     In this section, we describe how we construct the PDA
numerous spurious errors. In contrast, PDAs can represent                     encoding the set of error traces in the considered extension.
the set of error decision vectors precisely.                                  The general idea is the same as the one for the use of finite
   On the other hand, we still use a finite automaton to repre-               automata (described in Section 7). The main difference is
sent the approximation of the set of feasible decision vectors                that we add jumps between CFGCs (corresponding to pro-
decision(Π). As a consequence, except that we need to use                     cedure call edges), which use the stack to remember which
PDA operations instead of FA operations and handle proce-                     state the PDA should return to after the procedure call ter-
dure calls in the membership queries, all other components                    minates.
remain unchanged for the setting of multiple procedures.                         In the following, given a CFGC G = (V, E, vi , vr , Ve , XFP ),
                                                                              we use V (G), E(G), . . . , XFP (G) to denote the correspond-
9.1 Extending CFGs with Procedure Calls                                       ing components of G, and, moreover, we use Vs (G) and
  Assume the set of procedure names P. A CFG with calls                       Vb (G) to denote the set of sequential and branching nodes
(CFGC) is defined as a graph G = (V, E, vi , vr , Ve , XFP )                  of G respectively. Consider a program prog = {G1 , . . . , Gn }.
We construct the error path automaton as the PDA BP =                            Recall that our modified learning algorithm (described in
({0, 1}, Q, Q, qi , ∆, F ) in the following way:                              Section 4.2) first checks whether the intersection of the lan-
                                                                              guage of the conjecture L(C) and the bad language L(BP )
   • Q = V (G1 ) ∪ · · · ∪ V (Gn ),
                                                                              is empty. Checking emptiness of a PDA is, however, more
   • qi = vi (Gk ) such that prog (main) = Gk ,                               difficult than that of a finite automaton. To speed up
                                                                              the procedure, we build a finite automaton BO that over-
   • F = Ve (G1 ) ∪ · · · ∪ Ve (Gn ),
                                                                              approximates the error language and always first checks
   • ∆ = ∆1 ∪ · · · ∪∆n where every ∆j is defined as follows:                 whether L(C) ∩ L(BO ) = ∅, which is an emptiness test for
                                                                              finite automata. We check L(C) ∩ L(BP ) = ∅ only for the
        – (v, 0, v0′ ) ∈ ∆j if v ∈ Vb (Gj ) \ Ve (Gj ), (v, f0 , v0′ ) ∈      cases that the previous test fails.
          E(Gj ), and v0′ is the 0-successor of v;
        – (v, 1, v1′ ) ∈ ∆j if v ∈ Vb (Gj ) \ Ve (Gj ), (v, f1 , v1′ ) ∈      Counterexample from the Learning Algorithm.
          E(Gj ), and v1′ is the 1-successor of v;                               When an equivalence query returns a counterexample c,
        – (v, λ, v ′ ) ∈ ∆j if v ∈ Vs (Gj ) \ Ve (Gj ) and                    automata learning algorithms usually do not guarantee that
          (v, f, v ′ ) ∈ E(Gj );                                              c is not a valid counterexample in the next conjecture au-
        – (v, 0, v), (v, 1, v) ∈ ∆j if v ∈ Ve (Gj ); and                      tomaton. In our preliminary experiments, we found out that
        – (v, [λ; λ/v ′ ], vi (Gk )), (vr (Gk ), [λ; v ′ /λ], v ′ ) ∈ ∆j if   it happens very often that the mechanical teacher returns
          v ∈ Vs (Gj ) \ Ve (Gj ), (v, (p, gin , gout ), v ′ ) ∈ E(Gj ),      the same counterexample in several consecutive iterations.
          and Gk = prog (p).                                                  Therefore, we decided to check whether c is still a valid
                                                                              counterexample (by a membership query) for the learning
   Lemma 4. Let prog be a program, B the set of error paths                   algorithm before proceeding to the emptiness test. In the
of prog , and BP be the error path PDA for prog . Then it                     case c is valid, it will be immediately returned to the learn-
holds that L(BP ) = decision(B).                                              ing algorithm to refine the conjecture.

                                                                              Handling Membership Queries.
10. IMPLEMENTATION                                                              The main bottleneck of our approach is the time spent
   We created a prototype tool Pac-Man that implements                        for membership queries. In our implementation, the soft-
the verification procedure described in this paper. The tool                  ware model checker CPAchecker is used to check whether
uses several third-party libraries and tools. First, it uses                  a path is feasible. For each membership query, if we invoke
CIL (C Intermediate Language) [17] to convert the verified                    CPAchecker with a system call, a Java virtual machine
C program to a set of CFGCs, from which we construct                          will be created and the components of CPAchecker need
the error trace pushdown automaton BP . Further, we use                       to be loaded, which is very time consuming. To make mem-
the libAMoRE++ library [16, 6] to perform operations of                       bership queries more efficient, we modified CPAchecker to
automata, such as testing their membership and emptiness,                     run in a server mode so that it can check more than a single
or computing their intersection.                                              path without being re-invoked.
   For learning automata, we use the implementation of vari-
ous learning algorithms within the libalf library [6]. Mem-
bership queries are discharged using a concolic tester, men-                  11. EXPERIMENTS
tioned as an alternative option in Section 6. Given a decision                   This section presents our experimental results to justify
vector, our tool uses the CFG of the program to generate                      the claims made in this paper. We evaluated the perfor-
a path corresponding to the decision vector. The path is                      mance of our prototype using the recursive category of SV-
passed in the form of a sequence of program statements to                     COMP 2015 [1] as the benchmark. The recursive category
the software model checker CPAchecker [4], which checks                       consists of 24 non-trivial examples such as Ackermann, Mc-
its feasibility. It is possible to switch the model checker with              Carthy 91, and Euclidean algorithms. Among eight par-
other checkers, such as CBMC [10].                                            ticipating tools, only two can solve 20 or more examples
   To deal with equivalence queries, we modified the concolic                 correctly. Among the 24 examples, 8 of them contain an
tester Crest [7] to generate a batch of k decision vectors, as                error. We performed our experiments with the error param-
described in Section 5. As Crest may fail to generate the                     eter ǫ = 0.1, confidence δ = 0.9, and size of batched samples
decision vector of a program execution when the execution                     k = 10. We ran our prototype on each example three times
terminates abnormally, we modified Crest to take a finite                     in all experiments. The provided statistical data were calcu-
prefix of the execution in this case. One issue of Crest                      lated based on the average of the three runs unless explicitly
that we encountered is that when it processes a condition                     stated otherwise. We set the timeout to 900 s to match the
composed using Boolean connectives, it expands the condi-                     rules of SV-COMP 2015.
tion into a cascade of if statements corresponding to the
Boolean expression, making the program longer and harder                      11.1 Comparison of Learning Algorithms
to learn. We addressed this by modifying Crest so that                          We evaluated our approach with different automata learn-
it can process conditions with Boolean connectives inside                     ing algorithms implemented within the libalf library.
without expanding them, and in this way we increased the                      There are five active online automata learning algorithms
performance and precision of the analysis.                                    implemented in libalf: Angluin’s L∗ [2], L∗ -columns,
   We also implemented the following three optimizations to                   Kearns/Vazirani (KV) [14], Rivest/Schapire (RS) [18], and
improve the performance of the prototype.                                     NL∗ [5]. Among the search strategies provided by Crest,
                                                                              we chose the random branch strategy. The experimental
Intersection with Bad Automaton.                                              results are in Table 1.
        Table 1: Comparison of learning algorithms               Table 3: Evaluation of Crest with and without restart. For
                                    Algorithms                   each example, the number of batches and the number of it-
                      KV     L∗      L∗ -col. RS      N L∗       erations used to find bugs are obtained respectively from
  Verified            15     9.67    10       11.33   8.33       the worst run in scenario (1) and from the best run in sce-
  Bug found           6      6.33    6        6.33    6          nario (2).
   by Bad             4      4.67    4        3       4.33
   by Crest           2      1.67    2        3.33    1.67                                                Settings
  False positives     0      0       1        0.33    1            Examples                    Batch Size 10 Never Restart
  False negatives     2      1.67    1.33     1.67    1            Ackermann02                 batch 3         iteration 14
  Timeouts            1      6.33    5.67     4.33    7.67         Addition02                  batch 1         iteration 2
  # of Mem queries    2896   8898    10071    15377   14463        Addition03                  Timeout         Timeout
  # of Equ queries    548    78      77       367     67           BallRajamani-SPIN2000       batch 1         iteration 1
  Total time [s]      2406   6668    6565     5786    7972         EvenOdd03                   batch 1         iteration 2
  Mem queries time    30 %   59 %    58 %     63 %    70 %         Fibonacci04                 batch 4         iteration 2
    Table 2: Comparison of search strategies of Crest              Fibonacci05                 Timeout         Timeout
                                                                   McCarthy91                  batch 1         iteration 2
                                    Search Strategy
                                    RBS CDS
                                                                 Table 4: Comparison of Crest search strategies in terms of
        Verified                    15     15
                                                                 the quality of the learned automata. The total number of
        Bug found                   6      6
                                                                 tested batches is 1500.
        False positives             0      0
        False negatives             2      2                                                       Equ query strategy
        Timeouts                    1      1                                                       RBS      CDS
        # of Mem queries            2896 2362                           Evaluation     Accepted    1487     1473
        # of Equ queries            548    463                          (RBS)          Ratio       99.13 % 98.2 %
        Total time [s]              2406 2013
                                                                        Evaluation     Accepted    1489     1500
        Time for one sample [s]     0.75   0.82
                                                                        (CDS)          Ratio       99.27 % 100 %
   The results show that KV is the algorithm with the best
performance—it solved 21 out of the 24 examples. Our tech-       Crest with two different scenarios: (1) restart after each 10
nique solves more than any participant in the recursive cat-     decision vectors and (2) never restart. We performed the ex-
egory of SV-COMP 2015 but the winner. The main reason            periment on the 8 buggy examples in the recursive category
for the performance difference is that KV uses a tree-based      and calculated in how many examples Crest found a bug
data structure to store query results. Compared to other         for within the timeout period. In Table 3, we chose RBS as
learning algorithms that use table-based structures, KV re-      the search strategy. We also tried the experiments with the
quires much less number of membership queries to maintain        CFG strategy and got a similar result. We list the worst
the consistency of the tree-based structure. For all learn-      result for scenario (1) and the best result for scenario (2)
ing algorithms except RS, the number of error paths found        that we received in our three runs. We found out that the
by the emptiness test of the intersection of the conjecture      worst runs in scenario (1) can still find with a little overhead
and the bad automaton is more than that found by Crest.          all bugs found by the best runs in scenario (2).
In our experiments, the time spent for membership queries
is usually the performance bottleneck. Table 1 shows that        11.4 Evaluating Quality of Learned Automata
membership queries took 30 % of the total execution time            Besides the performance in terms of the running time, we
for KV and at least 58 % for other algorithms.                   also compared the quality of the learned automata produced
                                                                 by our prototype using the two strategies for the 15 success-
11.2 Comparison of Search Strategies                             fully verified bug-free examples. To evaluate the quality of
   We also evaluated the performance of our algorithm            the learned automata, for each example, we ran Crest with
against different Crest search strategies. According to [7],     the given search strategy to get 100 batched samples and
the most efficient ones are random branch strategy (RBS          tested how many of the them are all accepted by the learned
for short) and control-flow directed strategy (CDS for short).   automaton. The average values of the runs are shown in
Therefore, we tested the performance of our prototype using      Table 4 where evaluation strategies are strategies used to
these two strategies. We selected KV as the learning algo-       generate the testing batched samples. The table shows that
rithm in this experiment. The results are shown in Table 2.      the quality of the automata learned with the two strategies
   Table 2 shows that although the average time for taking       is almost the same. Also, observe that the guarantee of our
one sample with CDS is more than with RBS, the total time        procedure is that the sample coverage is higher than 90 %.
is less. The main reason is that CDS explores untouched          Our experimental results show that the quality of the au-
branching points more aggressively than RBS but requires         tomata produced by our procedure matches the theoretical
more overhead. Our experiments conform the results in [7].       expectations.
                                                                    Finally, we tested how many words generated by Crest
11.3 Evaluation of CREST with Restarts                           are not covered in the automata learned with the KV algo-
  To justify our modification to the PAC (ǫ, δ)-correctness      rithm and RBS. Again, we ran Crest with RBS in two
guarantee given in Section 5.2, we show in the experiment        scenarios: (1) restart after each 10 decision vectors and
below that running Crest in batches does not decrease its        (2) never restart. For each learned automaton (there were
bug-hunting capabilities. We compared the performance of         15) and each scenario, we generated 1000 decision vectors
and checked how many of them are accepted by the automa-             Applying PAC learning to testing has been considered be-
ton. In total, for scenario (1), we observed 1487 accepted        fore [22, 13]. The work in [13] considers a program that
batches of size 10 (for the total of 15 000 tested vectors),      manipulates graphs and check if the output graph of the
yielding the correctness 99.13 %. For scenario (2), we ob-        program has properties such as being bipartite, k-colorable,
served 14 977 accepted vectors, for the correctness 99.86 %.      etc. Our work considers assertion checking, which is more
We notice that no matter which strategy we use, the learned       general than the specialized properties. The work [22] con-
automaton accepts over 99 % of the decision vectors pro-          siders more theoretical aspects of the problem. The author
duced by Crest.                                                   estimates the maximal number of queries required to infer
                                                                  a model of a black box machine. The context is quite differ-
                                                                  ent, e.g., the work does not discuss how to sample according
12. DISCUSSION                                                    to some distribution efficiently to produce the desired guar-
   There are several advantages of having a program model         antee (bounded path coverage) as we do in this paper.
with statistical guarantees. For instance, the model can be          The L∗ algorithm has been used to infer the model of error
reused for verifying a different set of properties of the pro-    traces of a program. In [8], instead of decision vectors, the
gram. Assume that the new property to be verified is de-          authors try to learn the sequences of function calls leading
scribed as an error path automaton B ′ and C is the learned       to an error. Their teacher is implemented using a bounded
automaton. If L(B ′ ) ∩ L(C) = ∅, we verified the program         model checker and hence can only guarantee correctness up
with the new property and the same PAC (ǫ, δ)-correctness         to a given bound. The authors do not make use of the PAC
guarantee. For the case that there exists a decision vector       learning technique as we did in this work.
w ∈ L(B ′ ) ∩ L(C), we test whether w is feasible and either         Both our approach and statistical model checking [20, 15,
report that w is a feasible error decision vector w.r.t. B ′ or   23] provide statistical guarantees. As mentioned in the in-
continue the learning algorithm with w as a counterexample        troduction, statistical model checking assumes a given model
for refining the next conjecture.                                 while our technique generates models of programs with sta-
   In this paper we focus on checking validity of program         tistical guarantee. Those models can be analyzed using var-
assertions. The verification step is handled by making an         ious techniques and reused for verifying different properties.
intersection of the conjecture automaton C and the error
path automaton B and testing its emptiness. This proce-
dure can be generalized to more sophisticated safety prop-        APPENDIX
erties by replacing the tests L(C) ∩ L(B) = ∅ and s ∈ L(B)        A. AN INLINING IN A CFGC
with other tests. For example, we can check the property
“the program contains at most 10 consecutive 1-decisions on           Consider a procedure call edge e = (v, (p, gin , gout ), v ′ ) of
any path” with a statistical guarantee of the correctness of      Gj = (Vj , Ej , vij , vrj , Vej , XFP j ) for 1 ≤ j ≤ n. Further
the received answer. By extending the alphabet {0, 1} with        assume that prog (p) = Gk = (Vk , Ek , vik , vrk , Vek , XFP k )
program labels, one can also check temporal properties re-        for 1 ≤ k ≤ n. The inlining of e in prog is the pro-
lated to those labels, e.g., “label A should be reached within    gram prog # = {G1 , . . . , Gj−1 , G#             j , Gj+1 , . . . , Gn } such that

10 decisions after label B is reached.”                           G#                      #         #                     #
                                                                     j = (Vj ∪ Vk , E , vij , vrj , Vej ∪ Vek , XFP j ) where Vk is
                                                                                                                                                      #

                                                                                                                 #
   One possible extension of our work is to learn sequences of    a set of fresh nodes (i.e., Vk is disjoint from the set of
feasible function calls instead of decision vectors. This might   nodes of any CFGC in prog ) and Vek                      #
                                                                                                                               ⊆ Vk# . Moreover,
lead to a more compact model in contrast to the current ap-                                                     #
                                                                  there exist bijections σ : Vk → Vk and σe : Vek                             #
                                                                                                                                                  → Vek
proach. However, in this case the alphabet of the model to                                                                          #
                                                                  such that σe ⊆ σ. The set of edges E is defined as
be learned will be all function names in the program, which
                                                                  E # = (Ej \ {e}) ∪ Ek# ∪ {(v, gin , vik               #      #
                                                                                                                          ), (vrk  , gout , v ′ )} where
is usually much larger than 2, the size of the alphabet in our       #             #         #′             #          #′
work. Moreover, in this setting, it is much harder to answer      Ek = {(vk , f, vk ) | (σ(vk ), f, σ(vk )) ∈ Ek }.
membership queries; a program path composed of function               Let inln(prog) be the smallest (potentially infinite) set
calls might perform a complex traversal through loops and         that contains prog and is closed w.r.t. inlinings in main, i.e.,
branches in between the calls, making the problem of check-       if inln(prog) contains a program prog # with a procedure call
ing feasibility of a program path already undecidable.            edge e in the CFGC prog # (main), it also contains the inlin-
   One benefit of our approach is that, in principle, it can be   ing of e in prog # . We abuse notation and use σ uniformly to
extended to black box system verification and model syn-          denote for all programs prog # ∈ inln(prog) the mapping of
thesis. By observing the behavior of the environment, we          the nodes of the CFGCs in prog # to their original nodes in
may find some pattern (e.g., some statistical distribution)       prog (for nodes V of prog , we assume that σ|V = id, i.e., that
of the inputs and then, based on that, design a sampling          the restriction of σ to V is the identity relation). We denote
mechanism. Under the assumption that the behavior of the          as Jprog K the set of CFGs (without procedure call edges)
environment remains unchanged, we can verify or synthesize        obtained by starting from the set inln(prog), collecting the
the model of the system w.r.t. the given sample distribution.     CFGCs of main functions of all inlinings of prog into the
                                                                  set M = {prog # (main) | prog # ∈ inln(prog)}, and, finally,
                                                                  transforming the CFGCs of M into CFGs of Jprog K by sub-
13. RELATED WORKS                                                 stituting each procedure call edge (v # , (p# , gin                   #       #
                                                                                                                                           , gout  ), v #′ )
                                                                                              #          #′
   Exact automata learning algorithm was first proposed by        with the edge (v , ff, v ).
Angluin [2] and later improved by many people [2, 18, 14, 5].         We extend the definition of a path as follows: A path in
The concept of probably approximately correct (PAC) learn-        prog is a sequence π = hv0 , f1 , v1 , f2 , v2 , . . . , fm , vm i such
ing was first proposed by Valiant in his seminal work [21].       that there exists a CFG G′ ∈ Jprog K and a CFG path π ′ =
The idea of turning an exact learning algorithm to a PAC          hv0′ , f1 , v1′ , f2 , v2′ , . . . , fm , vm
                                                                                                             ′
                                                                                                               i in G′ such that ∀0 ≤ j ≤ m :
                                                                                ′
learning algorithm can be found in Section 1.2 of [3].            vj = σ(vj ).
14. REFERENCES                                                  [19] Koushik Sen, Darko Marinov, and Gul Agha. CUTE:
 [1] Software verification competition 2015,                         a concolic unit testing engine for C. In Proc. of
     http://sv-comp.sosy-lab.org/2015/.                              FSE’05, pages 263–272, 2005.
 [2] Dana Angluin. Learning regular sets from queries and       [20] Koushik Sen, Mahesh Viswanathan, and Gul Agha.
     counterexamples. Information and Computation,                   Statistical model checking of black-box probabilistic
     75(2):87–106, 1987.                                             systems. In Proc. of CAV’04, volume 3114 of LNCS,
 [3] Dana Angluin. Queries and concept learning. Machine             pages 202–215. Springer, 2004.
     Learning, 2(4):319–342, 1987.                              [21] Leslie G. Valiant. A theory of the learnable.
 [4] Dirk Beyer and M. Erkan Keremoglu. CPAchecker: A                Communications of the ACM, 27(11):1134–1142, 1984.
     tool for configurable software verification. In Proc. of   [22] Neil Walkinshaw. Assessing test adequacy for
     CAV’11, pages 184–190. Springer, 2011.                          black-box systems without specifications. In Proc. of
 [5] Benedikt Bollig, Peter Habermehl, Carsten Kern, and             ICTSS’11, volume 7019 of LNCS, pages 209–224.
     Martin Leucker. Angluin-style learning of NFA. In               Springer, 2011.
     Proc. of IJCAI’09, pages 1004–1009. IJCAI, 2009.           [23] Paolo Zuliani, André Platzer, and Edmund M. Clarke.
 [6] Benedikt Bollig, Joost-Pieter Katoen, Carsten Kern,             Bayesian statistical model checking with application
     Martin Leucker, Daniel Neider, and David R. Piegdon.            to Stateflow/Simulink verification. Formal Methods in
     libalf: The automata learning framework. In Proc. of            System Design, 43(2):338–367, 2013.
     CAV’10, volume 6174 of LNCS, pages 360–364.
     Springer, 2010.
 [7] Jacob Burnim and Koushik Sen. Heuristics for
     scalable dynamic test generation. In Proc. of ASE’08,
     pages 443–446. IEEE Computer Society, 2008.
 [8] Martin Chapman, Hana Chockler, Pascal Kesseli,
     Daniel Kroening, Ofer Strichman, and Michael
     Tautschnig. Learning the language of error. In Proc. of
     ATVA’15, LNCS. Springer, 2015. To appear.
 [9] Yu-Fang Chen, Azadeh Farzan, Edmund M. Clarke,
     Yih-Kuen Tsay, and Bow-Yaw Wang. Learning
     minimal separating DFA’s for compositional
     verification. In Proc. of TACAS’09, pages 31–45, 2009.
[10] Edmund Clarke, Daniel Kroening, and Flavio Lerda.
     A tool for checking ANSI-C programs. In Proc. of
     TACAS’04, volume 2988 of LNCS, pages 168–176.
     Springer, 2004.
[11] Jamieson M. Cobleigh, Dimitra Giannakopoulou, and
     Corina S. Pasareanu. Learning assumptions for
     compositional verification. In Proc. of TACAS’03,
     pages 331–346, 2003.
[12] Patrice Godefroid, Nils Klarlund, and Koushik Sen.
     DART: directed automated random testing. In Proc.
     of PLDI’05, pages 213–223, 2005.
[13] Oded Goldreich, Shari Goldwasser, and Dana Ron.
     Property testing and its connection to learning and
     approximation. Journal of ACM, 45(4):653–750, July
     1998.
[14] Michael J. Kearns and Umesh Virkumar Vazirani. An
     introduction to computational learning theory. MIT
     Press, 1994.
[15] Axel Legay, Benoı̂t Delahaye, and Saddek Bensalem.
     Statistical model checking: An overview. In Proc. of
     RV’10, volume 6418 of LNCS, pages 122–135.
     Springer, 2010.
[16] Oliver Matz, Axel Miller, Andreas Potthoff, Wolfgang
     Thomas, and Erich Valkema. Report on the program
     amore. 1995.
[17] George C. Necula, Scott McPeak, Shree Prakash
     Rahul, and Westley Weimer. CIL: Intermediate
     language and tools for analysis and transformation of
     C programs. In Proc. of CC’02, pages 213–228, 2002.
[18] Ronald L. Rivest and Robert E. Schapire. Inference of
     finite automata using homing sequences. Information
     and Computation, 103(2):299–347, 1993.
