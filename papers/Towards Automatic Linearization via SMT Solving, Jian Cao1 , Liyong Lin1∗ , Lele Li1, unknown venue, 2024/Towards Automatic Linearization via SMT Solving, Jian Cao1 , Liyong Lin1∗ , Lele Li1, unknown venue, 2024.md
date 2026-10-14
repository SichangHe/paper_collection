                                                                   Towards Automatic Linearization via SMT Solving

                                                                                  Jian Cao1 , Liyong Lin1∗ , Lele Li1
                                                                              1
                                                                                Contemporary Amperex Technology Limited
                                                                                          llin5@e.ntu.edu.sg
arXiv:2408.13487v1 [cs.LO] 24 Aug 2024




                                                                   Abstract                                  It is relatively difficult to ensure a), since one needs to ensure
                                                                                                             the raw optimization model is semantically an abstraction of
                                                Mathematical optimization is ubiquitous in modern            the problem to be solved and the solution of the model can be
                                                applications. However, in practice, we often need            faithfully executed, discarding irrelevant details. It is tedious,
                                                to use nonlinear optimization models, for which the          but still technically possible, to ensure c)1 . Both a) and c) are
                                                existing optimization tools such as Cplex or Gurobi          not the focus of this work, however. Usually, b) is performed
                                                may not be directly applicable and an (error-prone)          by experienced optimization engineer by manual transforma-
                                                manual transformation often has to be done. Thus,            tion, using tactics that are mastered by either learning or trial-
                                                to address this issue, in this paper we investigate          and-error experiments. However, such a manual transforma-
                                                the problem of automatically verifying and synthe-           tion is not always reliable, since errors could be introduced in
                                                sizing reductions, the solution of which may allow           the transformation process that there is no guarantee of model
                                                an automatic linearization of nonlinear models. We           equivalence or correctness, and a rigorous proof is often lack-
                                                show that the synthesis of reductions can be formu-          ing. This work’s main focus is to address b).
                                                lated as an ∃∗ ∀∗ synthesis problem, which can be                More abstractly, we are interested in the following techni-
                                                solved by an SMT solver via the counter-example              cal problems in the long run.
                                                guided inductive synthesis approach (CEGIS).
                                                                                                              1) Verification: Given an (optimization) model Σ from a
                                                                                                                 class C and another model Σ′ from a class S, how shall
                                         1 Introduction                                                          one automatically (dis)-prove their equivalence?
                                         Mathematical optimization is among the most important tech-          2) Exact Synthesis: Given a model Σ from a class C, how
                                         nological backbones of many modern applications in finance,             to synthesize an equivalent model Σ′ in a different class
                                         engineering, supply chain management and so on. Being able              S or prove that there is no such equivalent model?
                                         to correctly formulate an optimization model for a given ap-
                                         plication is crucial in practice, an art that might require sub-     2) Approximate Synthesis: Given a model Σ from a class
                                         stantial training to master for most beginners, and it can be an        C, how shall one synthesize a “close” model Σ′ in a dif-
                                         error-prone process even for well-trained engineers. In prac-           ferent class S?
                                         tice, however, the most intuitive optimization models for the       For example, class C can represent the class of nonlinear pro-
                                         applications, such as scheduling and production planning, of-       gramming models, while class S could represent the class of
                                         ten involve logical or nonlinear operations, and these are of-      linear programming models. We remark that, of course, more
                                         ten the models that are derived in the first step by optimization   delicate distinctions between classes can also be made by al-
                                         engineers. After this nonlinear optimization model is derived,      lowing different sets of nonlinear functions to extend the base
                                         then the engineers may proceed to transform or relax it into a      optimization classes. For example, the class of mixed integer
                                         linear formulation, if possible.                                    linear programming (MILP) models, when it is extended with
                                            In the above-mentioned process, to ensure a correct math-        the max function, can be shown to be expressively equivalent
                                         ematical optimization model is (correctly) solved, we need to       to itself.
                                         ensure three aspects:                                                  The two classes C and S need not be different, however. In
                                          a) The “raw“ optimization model, i.e., the nonlinear opti-         principle, the above formulation of the problem permits one
                                             mization model before the transformation is carried out,        to derive an efficient model from a less efficient one, despite
                                             correctly captures the user’s intent and models the prob-       both being in effectively the same class of models. As a well
                                             lem to be solved.                                               known example, one can make an MILP model more efficient
                                                                                                             by using a good formulation [1] or by adding cuts [2]. For the
                                          b) The transformed model is equivalent to the raw model.
                                                                                                                1
                                          c) The solver is correct in solving the transformed model.              There are generally two approaches, either by proving the solver
                                                                                                             itself to be correct in solving every instance or providing a certificate
                                            ∗
                                                Contact Author                                               for any given instance solved by the solver.
problem of approximate synthesis, one is often interested in           cation and a substantial reduction of verification complexity.
finding approximation Σ′ in a more efficient class of models           The technique of automaticaly computing a reduction can be
that offers a good bound for a given model Σ.                          used to obtain a compact MILP model encoding of neural net-
    Σ′ can be viewed as a (candidate) reduction of Σ. Thus, the        works with layers that use piecewise-linear functions such as
above three problems could be viewed as the verification and           ReLU or max-pooling [16]. This MILP encoding can then be
synthesis of reductions between (the decision versions of) the         used for downstream neural network verification tasks [16].
two classes of optimization problems (equipped with appro-
priate signatures), similar in spirit to [3]. Without restriction,     2 Verification and Synthesis of Reductions
it is clear that all the above three problems are undecidable in       In this section, we first provide a motivating example to illus-
general.                                                               trate the idea behind the verification and synthesis approach.
    In this paper, we will mainly look at the problems of verifi-
cation and exact synthesis. In practice, there are often bounds        2.1   Motivating Examples
on the variables that appear in the optimization model. Thus,          Nonlinear Constraints:
instead of solving the unbounded verification/synthesis prob-             For the nonlinear constraint c = max{a, b}, the following
lem, we focus on a bounded approach [4, 5]. In addition, for           linearization
bounded synthesis, we shall also parameterize the complexity
of candidate reductions by restricting2 the numbers of auxil-
                                                                                         
                                                                                          c≥a
iary variables and linear inequalities, enabling an incremental                          
                                                                                         
                                                                                         c ≥ b
                                                                                         
search [6, 7] of bounded reductions. As we shall see later, the
                                                                                         
method is quite effective for a class of nonlinear models that                             c ≤ a + (1 − u1 )M                   (1)
are essentially piece-wise linear3 , where automated reasoning                             c ≤ b  + (1 −  u   )M
                                                                                         
                                                                                         
                                                                                         
                                                                                                           2
tools such as SMT solvers [8,9] can be used for automated re-
                                                                                         
                                                                                           u1 + u2 ≥ 1
                                                                                         
duction verification/synthesis.
    The main contributions of this work are listed as follows:         is well known, where u1 , u2 ∈ {0, 1} are two newly intro-
                                                                       duced Boolean variables, and M is a large constant.
   • An approach is given to reduce the problem of bounded                Suppose the nonlinear constraint c = max{a, b} appears
     verification into solving SMT formulas. We remark that,           in an optimization model, then it can be replaced by the above
     in principle, the approach can produce a counter exam-            linearization reduction. In practice, however, to safely use the
     ple to witness non-equivalence of models.                         above linearization reduction, we have to show its correct-
   • We show that the counter-example guided inductive syn-            ness, which amounts to establishing the following.
     thesis (CEGIS) approach could be adopted to synthesize            Proposition 1 Let M > |a| + |b| + |c| + 1. Then, for any
     an optimal reduction (at least in principle), under a natu-       a, b, c ∈ R, c = max{a, b} iff
     ral measure (i.e., the numbers of auxiliary variables and                                     
     linear inequalities).                                                                         
                                                                                                    c≥a
                                                                                                   c ≥ b
                                                                                                   
                                                                                                   
   Related Works: The problems of verifying and synthe-                                            
sizing reductions have been studied in different contexts. [10]                  ∃u1 , u2 ∈ {0, 1}, c ≤ a + (1 − u1 )M              (2)
proposes an approach to allow users to interactively verify the                                      c ≤ b + (1 − u2 )M
                                                                                                   
                                                                                                   
                                                                                                   
                                                                                                   
correctness of reductions from disciplined convex programs                                         
                                                                                                   
                                                                                                     u1 + u2 ≥ 1
(DCP) to conic programs by using Lean, an interactive theo-
rem prover [11]. The earliest work that we know of in synthe-          Proof: Suppose c = max{a, b}, then it is clear that c ≥ a
sizing reductions, which are captured by “gadgets”, between            and c ≥ b. Also, c ≤ a or c ≤ b holds by the definition of
decision problems can be found in [12], by using linear pro-           max. Suppose c ≤ a, then we can set u1 = 1 and u2 = 0,
gramming techniques. In [6, 7], based on descriptive com-              and it holds that c ≤ a + (1 − u1 )M , c ≤ b + (1 − u2 )M and
plexity theory, quantifier free projections (a rather weak class       u1 + u2 ≥ 1. On the other hand, suppose c ≤ b, then we can
of reductions) between complexity classes are automatically            set u1 = 0 and u2 = 1 and it holds that c ≤ a + (1 − u1 )M ,
synthesized via SAT solvers. A reduction in [6, 7] is captured         c ≤ b + (1 − u2 )M and u1 + u2 ≥ 1.
by a Boolean query, which is parameterized by the size of                 Suppose there exists some u1 , u2 ∈ {0, 1} such that c ≥ a,
the structure that the reduction is supposed to be effective,          c ≥ b, c ≤ a + (1 − u1 )M , c ≤ b + (1 − u2 )M and u1 + u2 ≥
as well as another two parameters that characterize the com-           1. Any such a choice of u1 , u2 must satisfy the requirement
plexity of the reduction. The counter-example guided induc-            that u1 = 1 or u2 = 1. Without loss of generality, suppose
tive synthesis (CEGIS) approach is used to address the ∃∗ ∀∗           u1 = 1. Then, by c ≤ a + (1 − u1 )M we have c ≤ a. Then,
synthesis problem. Later, the work has also been extended to           we have a = c ≥ b and thus c = max{a, b}.
accommodate machine learning techniques [13]. In a differ-                Nonlinear Objectives:
ent context, [3, 14, 15] work on the problem of automatically             Consider the following nonlinear program, where the fea-
verifying and synthesizing reductions for a particular class of        sible region D is assumed to be linear.
verification problems, which allows automatic parallel verifi-
   2                                                                                   min                 max{a, b}               (3)
       The details will be explained later.
   3
       For example, the nonlinear function max is piece-wise linear.                   s.t.                (a, b) ∈ D              (4)
   It is straightforward to see that the above program is equiv-         If no such an X exists, then we can set l := l + 1, k := k + 1
alent to the following, where z is a newly introduced auxiliary          and repeat solving Formula 1 for the updated l and k; else, let
variable.                                                                X be obtained, then we know that X is a candidate reduction
                                                                         that works for S ⊆ D1 ×D2 ×. . .×Dm ; however, we are still
                                                                         not yet certain X is a reduction, as it is not fully verified on
                  min                 z                            (5)
                                                                         D1 × D2 × . . . × Dm . Indeed, we need to solve the problem
                  s.t.                (a, b) ∈ D                   (6)   of finding a counter example for X, i.e., solving Formula 2.
                                      z = max{a, b}                (7)      Formula 2: Reduction Refutation
  Thus, without loss of generality, in the rest of this work we                           ∃y ∈ D1 × D2 × . . . × Dm ,
                                                                                 V                   Wl                   T
shall only consider nonlinear constraints.                                         u∈{0,1}k ((Φ(y) ∧ ( i=1 X[i :][y, u, 1] >
                                                                                                                T
                                                                                       0)) ∨ (¬Φ(y) ∧ X[y, u, 1] ≤ 0))
2.2      Methodology
In this section, we show how a predicate may be linearized4 .            If no such a y exists, then X is verified to be a reduction, since
   Given a predicate Φ(y1 , y2 , . . . , ym ), where yi ∈ Di ⊆ R         no counter-example could be found; else, let y be obtained,
for each i ∈ [1, m], we introduce a tuple of boolean variables           then we know that y is a counter example that works for X
(u1 , u2 , . . . , uk ) ∈ {0, 1}k . Let y = (y1 , y2 , . . . , ym ).     (that is, X is refuted by y) and it is clear that y ∈
                                                                                                                             / S. We then
                                                                         can set S := S ∪ {y} and repeat solving Formula 1 for the
Definition 1 The predicate Φ(y) is (l, k)-linearizable iff               updated S to find a new candidate reduction X.
          ∈ Rl×(m+k+1) , ∀y ∈ D1 × D2 × . . . × Dm ,
        ∃XW                                                              Remark 4 With a minor modification, the above incremental
                                       T
           u∈{0,1}k (Φ(y) ⇐⇒ X[y, u, 1] ≤ 0),                            approach is able to find an optimal reduction in principle, if
where 0 is a tuple of 0’s of size l.                                     such a reduction indeed exists.
Remark 1 Intuitively, we look for a valuation of X such that,
the region defined by the set of linear inequalities, after being        3 Conclusions
projected to y, spans the universe D1 ×D2 ×. . .×Dm . Thus,              We have presented an approach to verify and synthesize re-
u1 , u2 , . . . , uk act as auxiliary Boolean variables.                 ductions by using SMT solvers. As a work-in-progress, there
Remark 2 Since the valuation of X uniquely determines the                is an obvious weakness of our approach, that is, the scalability
set of linear inequalities, including its dimensions, hereafter          to large instances (including unbounded synthesis) is limited.
we directly refer to a valuation of X as a reduction of Φ(y).            As the expressive power of MILP models can be restrictive,
                                                                         a viable path is to use our approach for approximate synthe-
Definition 2 The predicate Φ(y) is said to be linearizable iff           sis, where much larger class of nonlinear models can be dealt
it is (l, k)-linearizable for some l ≥ 1, k ≥ 0.                         with. These issues will be studied in future works.
Remark 3 In the above discussion, we only refer to a pred-
icate; however, the definition of linearization and the related          Acknowledgement
verification and synthesis results, to be further discussed, can
be straightforwardly extended to a set of predicates.                    This work is financially supported by National Key R&D Pro-
                                                                         gram of China (Grant 2022YFB4702400).
We do not distinguish between a variable and its valuation in
the rest of this work. In fact, only variables will be quantified.
From Remark 2, a counter example to a candidate reduction
                                                                         References
X ∈ Rl×(m+k+1) is a valuation y ∈ D1 × D2 × . . . × Dm                   [1] J. Hooker, “Formulating good MILP models”, Wiley
such that                                                                    Encyclopedia of Operations Research and Management
         V                       Wl                  T                       Science, 2011.
           u∈{0,1}k ((Φ(y) ∧ ( i=1 X[i :][y, u, 1] >
                                                                         [2] Y. Tang, S. Agrawal, Y. Faenza, “Reinforcement learn-
               0)) ∨ (¬Φ(y) ∧ X[y, u, 1]T ≤ 0))
                                                                             ing for integer programming: learning to cut”, Proceed-
holds. It is clear that the problem of finding counter examples              ings of the 37th International Conference on Machine
for a candidate reduction X ∈ Rl×(m+k+1) can be delegated                    Learning, 119:9367-9376, 2020.
to a SMT solver. In the rest of this section, we shall explain
                                                                         [3] L. Lin, T. Masopust, W. M. Wonham and R. Su, ”Auto-
how the counter-example guided inductive synthesis (CEGIS)
                                                                             matic generation of optimal reductions of distributions,”
approach can be used to synthesize reductions.
                                                                             IEEE Transactions on Automatic Control, vol. 64, no. 3,
   The idea of the CEGIS approach for synthesizing an (l, k)-
                                                                             pp. 896-911, 2019.
linearization is explained as follows. A set S = {y1 , . . . , yn }
of valuations is initialized and a candidate reduction X is syn-         [4] Y. He, P. Zhao, X. Wang, Y. Wang, “VeriEQL: bounded
thesized to work for S by solving Formula 1.                                 equivalence verification for complex SQL queries with
   Formula 1: Reduction Finding                                              integrity constraints”, Proceedings of the ACM on Pro-
      ∃X ∈ Rl×(m+k+1) , y∈S u∈{0,1}k (Φ(y) ⇐⇒
                             V      W                                        gramming Languages 8: 1071 - 1099, 2024.
                         X[y, u, 1]T ≤ 0)                                [5] B. Finkbeiner, S. Schewe, “Bounded synthesis”, In-
                                                                             ternational Journal on Software Tools for Technology
   4
       In this work, reduction is synonymous with linearization.             Transfer, 15, 519–539, 2013.
[6] M. Crouch, N. Immerman, J. Eliot B. Moss, “Finding
     reduction automatically”, Fields of Logic and Compu-
     tation, pp. 181-200, 2010.
[7] C. Jordan, Ł. Kaiser. “Experiments with reduction find-
     ing”, International Conference on Theory and Applica-
     tions of Satisfiability Testing, pp. 192-207, 2013.
[8] L. de Moura, N. Bjørner, “Z3: An efficient SMT
     solver”, International Conference on Tools and Algo-
     rithms for the Construction and Analysis of Systems,
     2008.
[9] H. Barbosa et al., “cvc5: A versatile and industrial-
     strength SMT solver”, International Conference on
     Tools and Algorithms for the Construction and Analysis
     of Systems, 2022.
[10] A. Bentkamp, R. Fernández Mir, J. Avigad, “Verified re-
     ductions for optimization”, International Conference on
     Tools and Algorithms for the Construction and Analysis
     of Systems , 74-92, 2023.
[11] L.d. Moura, S. Ullrich, “The Lean 4 theorem prover
     and programming language”, In: Automated Deduc-
     tion–CADE 28, 2021.
[12] L. Trevisan, G.B. Sorkin, M. Sudan, D.P. Williamson,
     “Gadgets, approximation, and linear programming”,
     Proceedings of 37th Conference on Foundations of
     Computer Science, pp. 617-626, 1996.
[13] C. Jordan, L. Kaiser, “Machine learning with guarantees
     using descriptive complexity and SMT solvers”, CoRR
     abs/1609.02664, 2016.
[14] L. Lin, S. Ware, R. Su, W. M. Wonham, “Reduction
     of distributions and its applications”, American Control
     Conference, pp. 3848-3853, 2017.
[15] L. Lin, T. Masopust, W. M. Wonham, R. Su, “Automatic
     generation of optimal reductions of distributions”, IEEE
     Trans. of Automatic Control, 62(11): 5755-5768, 2017.
[16] V. Tjeng, K. Y. Xiao, R. Tedrake, “Evaluating robust-
     ness of neural networks with mixed integer program-
     ming.” International Conference on Learning Represen-
     tations, 2017.
