                                          Neural Network Verification with Proof Production
                                                                            Omri Isac∗ , Clark Barrett† , Min Zhang‡ and Guy Katz∗
                                                           ∗ The Hebrew University of Jerusalem, † Stanford University, ‡ East China Normal University




                                            Abstract—Deep neural networks (DNNs) are increasingly being        combinations thereof. Notably, many modern approaches [49],
                                         employed in safety-critical systems, and there is an urgent need to   [52], [54], [64] involve a search procedure, in which the
                                         guarantee their correctness. Consequently, the verification com-      verification problem is regarded as a set of constraints. Then,
                                         munity has devised multiple techniques and tools for verifying
                                         DNNs. When DNN verifiers discover an input that triggers an           various input assignments to the DNN are considered in order
                                         error, that is easy to confirm; but when they report that no          to discover a counter-example that satisfies these constraints,
                                                                                                               or to prove that no such counter-example exists.
arXiv:2206.00512v2 [cs.LO] 27 Aug 2022




                                         error exists, there is no way to ensure that the verification
                                         tool itself is not flawed. As multiple errors have already been          Verification tools are known to be as prone to errors as
                                         observed in DNN verification tools, this calls the applicability      any other program [43], [71]. Moreover, the search procedures
                                         of DNN verification into question. In this work, we present a
                                         novel mechanism for enhancing Simplex-based DNN verifiers             applied as part of DNN verification typically involve the
                                         with proof production capabilities: the generation of an easy-to-     repeated manipulation of a large number of floating-point
                                         check witness of unsatisfiability, which attests to the absence of    equations; this can lead to rounding errors and numerical
                                         errors. Our proof production is based on an efficient adaptation      stability issues, which in turn could potentially compromise
                                         of the well-known Farkas’ lemma, combined with mechanisms             the verifier’s soundness [12], [43]. When the verifier discovers
                                         for handling piecewise-linear functions and numerical precision
                                         errors. As a proof of concept, we implemented our technique on        a counter-example, this issue is perhaps less crucial, as the
                                         top of the Marabou DNN verifier. Our evaluation on a safety-          counter-example can be checked by evaluating the DNN; but
                                         critical system for airborne collision avoidance shows that proof     when the verifier determines that no counter-example exists,
                                         production succeeds in almost all cases and requires only minimal     this conclusion is typically not accompanied by a witness of
                                         overhead.                                                             its correctness.
                                                                                                                  In this work, we present a novel proof-production mech-
                                                                I. I NTRODUCTION
                                                                                                               anism for a broad family of search-based DNN verification
                                            Machine learning techniques, and specifically deep neural          algorithms. Whenever the search procedure returns UNSAT
                                         networks (DNNs), have been achieving groundbreaking re-               (indicating that no counter-example exists), our mechanism
                                         sults in solving computationally difficult problems. Nowadays,        produces a proof certificate that can be readily checked using
                                         DNNs are state-of-the-art tools for performing many safety-           simple, external checkers. The proof certificate is produced
                                         critical tasks in the domains of healthcare [29], aviation [44]       using a constructive version of Farkas’ lemma, which guaran-
                                         and autonomous driving [19]. DNN training is performed by             tees the existence of a witness to the unsatisfiability of a set
                                         adjusting the parameters of a DNN to mimic a highly complex           of linear equations — combined with additional constructs
                                         function over a large set of input-output examples (the training      to support the non-linear components of a DNN, i.e., its
                                         set) in an automated way that is mostly opaque to humans.             piecewise-linear activation functions. We show how to instru-
                                            The Achilles heel of DNNs typically lies in generalizing           ment the verification algorithm in order to keep track of its
                                         their predictions from the finite training set to an infinite input   search steps, and use that information to construct the proof
                                         domain. First, DNNs tend to produce unexpected results on             with only a small overhead.
                                         inputs that are considerably different from those in the training        For evaluation purposes, we implemented our proof-
                                         set; and second, the input to the DNN might be perturbed              production technique on top of the Marabou DNN verifier [49].
                                         by sensorial imperfections, or even by a malicious adversary,         We then evaluated our technique on the ACAS Xu set of
                                         again resulting in unexpected and erroneous results. These            benchmarks for airborne collision avoidance [45], [47]. Our
                                         weaknesses have already been observed in many modern                  approach was able to produce proof certificates for the safety
                                         DNNs [37], [63], and have even been demonstrated in the               of various ACAS Xu properties with reasonable overhead
                                         real world [30] — thus hindering the adoption of DNNs in              (5.7% on average). Checking the proof certificates produced
                                         safety-critical settings.                                             by our approach was usually considerably faster than dispatch-
                                            In order to bridge this gap, in recent years, the formal           ing the original verification query.
                                         methods community has started devising techniques for DNN                The main contribution of our paper is in proposing a
                                         verification (e.g., [2], [11], [13], [31], [32], [40], [41], [52],    proof-production mechanism for search-based DNN verifiers,
                                         [57], [60], [61], [65], [67], [72], among many others). Typi-         which can substantially increase their reliability when de-
                                         cally, DNN verification tools seek to prove that outputs from a       termining unsatisfiability. However, it also lays a foundation
                                         given set of inputs are contained within a safe subspace of the       for a conflict-driven clause learning (CDCL) [73] verification
                                         output space, using various methods such as SMT solving [1],          scheme for DNNs, which might significantly improve the
                                         [16], [23], abstract interpretation [32], MILP solving [64], and      performance of search-based procedures (see discussion in
Sec. IX).                                                                               x1
   The rest of this paper is organized as follows. In Sec. II                                1
                                                                                                  ReLU        ReLU
we provide relevant background on DNNs, formal verification,
                                                                                                   v1          v2        y
the Simplex algorithm, and on using Simplex for search-based                                             −2          1
DNN verification. In Sec. III, IV and V, we describe the proof-
                                                                                             −1
production mechanism for Simplex and its extension to DNN                               x2
verification. Next, in Sec. VI, we briefly discuss complexity-
theoretical aspects of the proof production. Sec. VII details our                            Fig. 1: A toy DNN.
implementation of the technique and its evaluation. We then
discuss related work in Sec. VIII and conclude with Sec. IX.
                                                                      DNN Verification and Proofs. Given a DNN N : Rm → Rk
                       II. BACKGROUND
                                                                      and a property P : Rm+k → {T, F}, the DNN verification
Deep Neural Networks. Deep neural networks (DNNs) [36]                problem is to decide whether there exist x ∈ Rm and y ∈ Rk
are directed graphs, whose nodes (neurons) are organized into         such that (N (x) = y)∧P (x, y) holds. If such x and y exist, we
layers. Nodes in the first layer, called the input layer, are         say that the verification query hN , P i is satisfiable (SAT); and
assigned values based on the input to the DNN; and then               otherwise, we say that it is unsatisfiable (UNSAT). For exam-
the values of nodes in each of the subsequent layers are              ple, given the toy DNN from Fig. 1, we can define a property
computed as functions of the values assigned to neurons in            P : P (x, y) ⇔ (x ∈ [2, 3] × [−1, 1]) ∧ (y ∈ [0.25, 0.5]). Here,
the preceding layer. More specifically, each node value is            P expresses the existence of an input x ∈ [2, 3] × [−1, 1] that
computed by first applying an affine transformation to the            produces an output y ∈ [0.25, 0.5]. Later on, we will prove
values from the preceding layer and then applying a non-linear        that no such x exists, i.e., the verification query hN , P i is
activation function to the result. The final (output) layer, which    UNSAT.
corresponds to the output of the network, is computed without            Typically, P represents the negation of a desired property,
applying an activation function.                                      and so an input x which satisfies the query is a counter-
   One of the most common activation functions is the rectified       example — whereas the query’s unsatisfiability indicates that
linear unit (ReLU), which is defined as:                              the property holds. In this work, we follow mainstream DNN
                                    (                                 verification research [52], [67] and focus on properties P that
                                      b b>0                           are a conjunction of linear lower- and upper-bound constraints
             f (b) = ReLU(b) =
                                      0 otherwise.                    on the neurons of x and y. It has been shown that even
When b > 0, we say that the ReLU is in the active phase;              for such simple properties, and for DNNs that use only the
otherwise, we say it is in the inactive phase. For simplicity,        ReLU activation function, the verification problem is NP-
we restrict our attention here to ReLUs, although our approach        complete [47].
could be applied to other piecewise-linear functions (such as            A proof is a mathematical object that certifies a mathemat-
max pooling, absolute value, sign, etc.). Non piecewise-linear        ical statement. In case a DNN verification query is SAT, the
functions, such as as sigmoid or tanh, are left for future work.      input x for which P holds constitutes a proof of the query’s
  Formally, a DNN N : Rm → Rk , is a sequence of n layers             satisfiability. Our goal here is to generate proofs also for the
L0 , ..., Ln−1 where each layer Li consists of si ∈ N nodes,          UNSAT case, which, to the best of our knowledge, is a feature
denoted vi1 , ..., visi . The assignment for the j th node in the     that no DNN verifier currently supports [12].
1 ≤ i < n − 1 layer is computed as                                    Verifying DNNs via Linear Programming. Linear Program-
                               si−1                                   ming (LP) [22] is the problem of optimizing a linear function
                                                       !
                j
                               X                     j
                                              l
              vi = ReLU             wi,j,l · vi−1 + pi                over a given convex polytope. An LP instance over variables
                                                                                             |
                                  l=1                                 V = [x1 , . . . , xn ] ∈ Rn contains an objective function c · V
and neurons in the output layer are computed as:                      to be maximized, subject to the constraints A · V = b for
                       sn−2                                           some A ∈ Mm×n (R), b ∈ Rm , and l ≤ V ≤ u for some
                                                                      l, u ∈ (R ∪ {±∞})n . Throughout the paper, we use l(xi ) and
               j
                           X
              vn−1 =                         l
                                 wn−1,j,l · vn−2 + pjn−1
                           l=1                                        u(xi ), to refer to the lower and upper bounds (respectively)
                                                                      of xi . LP solving can also be used to check the satisfiability
where wi,j,l and     pji are (respectively) the predetermined
                                                                      of constraints of the form (A · V = b) ∧ (l ≤ V ≤ u).
weights and biases of N . We set s0 = m and treat v01 , ..., v0m
                                                                         The Simplex algorithm [22] is a widely used technique
as the input of N .
                                                                      for solving LP instances. It begins by creating a tableau,
   A simple DNN with four layers appears in Fig. 1. For
                                                                      which is equivalent to the original set of equations AV = b.
simplicity, the pji parameters are all set to zero and are ignored.
                                                                      Next, Simplex selects a certain subset of the variables, B ⊆
For input h1, 2i, the node in the second layer evaluates to
                                                                      {x1 , . . . , xn }, to act as the basic variables; and the tableau
ReLU(1 · 1 + 2 · (−1)) = ReLU(−1) = 0; the node in the
                                                                      is considered as representing each basic variable xi ∈ B as
third layer evaluates to ReLU(0 · (−2)) = 0; and the node in                                                                  P
                                                                      a linear combination of non-basic variables, xi =          cj · xj .
the fourth (output) layer evaluates to 0 · 1 = 0.                                                                             j ∈B
                                                                                                                                /
We use Ai,j to denote the coefficient of a variable xj in the                                             Query ϕ
tableau row that corresponds to basic variable xi . Apart from                          Linear                        Piecewise-Linear
the tableau, Simplex also maintains a variable assignment that                     e 1 : b1 = x 1 − x 2
satisfies the equations of A, but which may temporarily violate                      e2 : b2 = −2f1                    f1 = ReLU(b1 )
                                                                                        e3 : y = f2                    f2 = ReLU(b2 )
the bound constraints l ≤ V ≤ u. The assignment for a
variable xi is denoted α(xi ).
                                                                                                   
                                                                                 2            x1         3
                                                                              −1   x2   1 
   After initialization, Simplex begins searching for an as-                        
                                                                              0  ≤  f1  ≤ 0.5
                                                                                                      
signment that simultaneously satisfies both the tableau and                                        
                                                                              0.25   f2 , y  0.5
bound constraints. This is done by manipulating the set B,                    −0.5          b1 , b2     0.5
each time swapping a basic and a non-basic variable. This
alters the equations of A by adding multiples of equations          Fig. 2: An example of a DNN verification query ϕ, comprised
to other equations, and allows the algorithm to explore new         of an LP instance and piecewise-linear constraints.
assignments. The algorithm can terminate with a SAT answer
when a satisfying assignment is discovered or an UNSAT
answer when: (i) a variable has contradicting bounds, i.e.,         assignment also satisfies the ReLU constraints. If it does,
l(xi ) > u(xi ); or (ii) one of the tableau equations xi =          then the whole query is SAT. Otherwise, case splitting is
 P
    cj · xj implies that xi can never satisfy its bounds. The       applied in order to split the query into two different sub-
j ∈B
  /
Simplex algorithm is sound, and is also complete if certain         queries, according to the two phases of the ReLU function.1
heuristics are used for selecting the manipulations of B [22].      Specifically, in one of the sub-queries, the LP query is adjusted
A detailed calculus for the version of Simplex that we use          to enforce the ReLU to be in the active phase: the equation
appears in Appendix A.                                              f = b is added, along with the bound b ≥ 0. In the other sub-
   LP solving is particularly useful in the context of DNN          query, the inactive phase is enforced: b ≤ 0, 0 ≤ f ≤ 0. This
verification, and is used by almost all modern tools (either na-    effectively reduces the ReLU constraint into linear constraints
tively [47], or by invoking external solvers such as GLPK [53]      in each sub-query. This process is then repeated for each of
or Gurobi [39]). More specifically, a DNN verification query        the two sub-queries.
can be regarded as an LP instance with bounded variables               Case-splitting turns the verification procedure into a search
that represents the property P and the affine transformations       tree [47], with nodes corresponding to the splits that were ap-
within N , combined with a set of piecewise-linear constraints      plied. The tree is constructed iteratively, with Simplex invoked
that represent the activation functions. We demonstrate this        on every node to try and derive UNSAT or find a true satisfying
with an example, and then explain how this formulation can          assignment. If Simplex is able to deduce that all leaves in
be solved.                                                          the search tree are UNSAT, then so is the original query.
                                                                    Otherwise, it will eventually find a satisfying assignment that
   Recall the toy DNN from Fig. 1, and property P that is
                                                                    also satisfies the original query. This process is sound, and
used for checking whether there exists an input x in the range
                                                                    will always terminate if appropriate splitting strategies are
[2, 3] × [−1, 1] for which N produces an output y in the range
                                                                    used [22], [47]. Unfortunately, the size of the search tree
[0.25, 0.5]. We use b1 , f1 to denote the input and output to
                                                                    can be exponential in the number of ReLU constraints; and
node v1 ; b2 , f2 for the input and output of v2 ; x1 and x2 to
                                                                    so in order to keep the search tree small, case splitting is
denote the network’s inputs, and y to denote the network’s
                                                                    applied as little as possible, according to various heuristics that
output. The linear constraints of the network yield the linear
                                                                    change from tool to tool [54], [61], [67]. In order to reduce
equations b1 = x1 − x2 , b2 = −2f1 , and y = f2 (which
                                                                    the number of splits even further, verification algorithms apply
we name e1 , e2 , and e3 , respectively). The restrictions on the
                                                                    clever deduction techniques for discovering tighter variable
network’s input and output are translated to lower and upper
                                                                    bounds, which may in turn rule out some of the splits a-priori.
bounds: 2 ≤ x1 ≤ 3, −1 ≤ x2 ≤ 1, 0.25 ≤ y ≤ 0.5. The third
                                                                    We also discuss this kind of deduction, which we refer to as
equation implies that 0.25 ≤ f2 ≤ 0.5, which in turn implies
                                                                    dynamic bound tightening, in the following sections.
that b2 ≤ 0.5. Assume we also restrict: −0.5 ≤ b2 , −0.5 ≤
b1 ≤ 0.5, 0 ≤ f1 ≤ 0.5, . Together, these constraints give rise                   III. P ROOF P RODUCTION OVERVIEW
to the linear program that appears in Fig. 2. The remaining
ReLU constraints, i.e. fi = ReLU(bi ) for i ∈ {1, 2}, exist            A Simplex-based verification process of a DNN is tree-
alongside the LP instance. Together, query ϕ is equivalent to       shaped, and so we propose to generate a proof tree to match
the DNN verification problem that we are trying to solve.           it. Within the proof tree, internal nodes will correspond to
   Using this formulation, the verification problem can be          case splits, whereas each leaf node will contain a proof of
solved using Simplex, enhanced with a case-splitting approach       unsatisfiability based on all splits performed on the path
for handling the ReLU constraints [17], [47]. Intuitively, we       between itself and the root. Thus, a proof tree constitutes a
first invoke the LP solver on the LP portion of the query; and        1 The approach is easily generalizable to any piecewise-linear constraint, by
if it returns UNSAT, the whole query is UNSAT. Otherwise,           splitting the query according to the different linear pieces of the activation
if it finds a satisfying assignment, we check whether this          function.
valid proof of unsatisfiability if each of its leaves contains                             IV. S IMPLEX WITH P ROOFS
a proof that demonstrates that all splits so far lead to a
contradiction. The proof tree might also include proofs for             A. Producing proofs for LP
lemmas, which are valid statements for the node in which they             We now describe our approach for creating proof trees,
reside and its descendants (lemmas are needed for supporting            beginning with leaf nodes. We start with the following lemma:
bound tightening, as we discuss later).
                                                                        Lemma 1. If Simplex returns UNSAT, then there exists a
   As a simple, intuitive example, we depict in Fig. 3 a proof
                                                                        variable with contradicting bounds; that is, there exists a
of unsatisfiability for the query ϕ from Fig. 2. The root of
                                                                        variable xi ∈ V with lower and upper bounds l(xi ) and u(xi ),
the proof tree represents the initial verification query, which
                                                                        for which Simplex has discovered that l(xi ) > u(xi ).
is comprised of LP constraints and ReLU constraints. The
fact that this node is not a leaf indicates that the Simplex-              This lemma justifies our choice of using contradicting
based verifier was unable to conclude UNSAT in this state,              bounds as proofs of unsatisfiability in the leaves of the proof
and needed to perform a case split on the ReLU node v1 . The            tree. The lemma follows directly from the derivation rules
left child of the root corresponds to the case where ReLU v1 is         of Simplex. Specifically, there are only two ways to reach
inactive: the LP is augmented with additional constraints that          UNSAT: when the input problem already contains inconsistent
represent the case split, i.e., f1 = 0 and b1 ≤ 0. This new fact        bounds l(xi ) > u(xi ), or when Simplex finds a tableau row
may now be used by the Simplex procedure, which is indeed
                                                                               P
                                                                        xi =      cj · xj that gives rise to such inconsistent bounds.
able to obtain an UNSAT   result. The|node then contains a proof            j ∈B
                                                                                /
of this unsatisfiability: −1 0 0 . This vector instructs the            The complete proof appears in Appendix B.
checker how to construct a linear combination of the current               We demonstrate this with an example, based on the query ϕ
tableau’s rows, in a way that leads to a bound contradiction,           from Fig. 2. Suppose that, as part of its Simplex-based solution
as we later explain in Sec. V.                                          process, a DNN verifier performs two case splits, fixing the
                                                                        two ReLUs to their active states: f1 = b1 ∧ b1 ≥ 0 and f2 =
                             ϕ                                          b2 ∧b2 ≥ 0. This gives rise to the following (slightly simplified)
               v1 inactive         v1 active                            system of equations:
   ϕ ∧ (f1 = 0) ∧ (b1 ≤ 0)       ϕ ∧ (f1 = b1 ) ∧ (b1 ≥ 0)                b1 = x 1 − x 2    b2 = −2f1     y = f2   f 1 = b1   f 2 = b2
                  |
         −1 0 0
                     v2 inactive                     v2 active          Which corresponds to the tableau and variables
                                                                                                                               |
                                                                                                                               x1
       ϕ ∧ (f1 = b1 ) ∧ (b1 ≥ 0)            ϕ ∧ (f1 = b1 ) ∧ (b1 ≥ 0)      
                                                                            1        −1     −1    0    0    0      0
                                                                                                                      
                                                                                                                              x2 
        ∧(f2 = 0) ∧ (b2 ≤ 0)                 ∧(f2 = b2 ) ∧ (b2 ≥ 0)                                                            
                                                                           0         0      0   −1   −2     0      0         b1 
                                                                  |                                                         
                  f2                                                                                               −1
                                             
                                              −2 1 0 −2 0                  0
                                                                         A=          0      0   0    0     1                  b2 
                                                                                                                           V =    
                                                                                                                      
                                                                           0         0      1   0    −1     0      0         f1 
                  Fig. 3: A proof tree example.                             0         0      0   1    0     −1      0
                                                                                                                               
                                                                                                                               f2 
                                                                                                                                y
   In the right child of the root, which represents v1 ’s active
phase, the constraints f1 = b1 and b1 ≥ 0 are added by the              such that AV = 0, with the corresponding bound vectors:
split. This node is not a leaf, because the verifier performed a                                                       |
second case split, this time on v2 . The left child represents                   l = 2 −1 0        0     0    0.25 0.25
                                                                                                                     |
v2 ’s inactive phase, and has the corresponding constraints
                                                                                    
                                                                                u = 3 1 0.5 0.5 0.5 0.5 0.5
f2 = 0 and b2 ≤ 0. This child is a leaf, and is marked
with f2 , indicating that f2 is a variable whose bounds led                Then, the Simplex solver iteratively alters the set of basic
to a contradiction. Specifically, f2 ≥ 0.25 from ϕ and f2 = 0           variables, which corresponds to multiplying various equations
from the case split are contradictory.                                  by scalars and summing them to obtain new equations. At
   The last node (the rightmost leaf) represents v2 ’s active           some point,the equation b2 = −2x | 1 + 2x2 is obtained (by
phase, and has the constraints f2 = b2 and b2 ≥ 0. Here,                computing −2 1 0 −2 0 · A · V ), with a current
the node indicates that a contradiction   can be reached from
                                                             |         assignment of α(V )| = 2 1 1 −2 1 −2 −2 .
the current tableau, using the vector −2 1 0 −2 0 .                        At this point, the Simplex solver halts with an UNSAT
In Sec. IV, we explain how this process works.                          notice. The reason is that b2 is currently assigned the value
   Because each leaf of the proof tree contains a proof of              −2, which is below its lower bound of 0, and so its value
unsatisfiability, the tree itself proves that the original query        needs to be increased. However, the equation, combined with
is UNSAT. Note that many other proof trees may exist for                the fact that x1 is pressed against its lower bound, while x2 is
the same query. In the following sections, we explain how to            pressed against its upper bound, indicates that there is no slack
instrument a Simplex-based verifier in order to extract such            remaining in order to increase the value of b2 (this corresponds
proof trees from the solver execution.                                  to the Failure1 rule in the Simplex calculus in Appendix A).
The key point is that the same equation could be used in              B. Supporting dynamic bound tightening
deducing a tighter bound for b2 :
                                                                         So far, we have only considered Simplex executions that do
        b2 ≤ −2l(x1 ) + 2u(x2 ) = −2 · 2 + 2 · 1 = −2                 not perform any bound tightening steps; i.e., derive UNSAT
and a contradiction could then be obtained based on the               by finding a contradiction to the original bounds. However, in
contradictory facts 0 = l(b2 ) ≤ b2 ≤ −2. In other words,             practice, modern DNN solvers perform a great deal of dynamic
and as we formally prove in Appendix B, any UNSAT answer              bound tightening, and so this needs to be reflected in the proof.
returned by Simplex can be regarded as a case of conflicting             We use the term ground bounds to refer to variable bounds
lower and upper bounds.                                               that are part of the LP being solved, whether they were
   Given Lemma 1, our goal is to instrument the Simplex               introduced by the original input, or by successive case splits,
procedure so that whenever it returns UNSAT, we are able to           as we will explain in Sec. V. This is opposed to dynamic
produce a proof which indicates that l(xi ) > u(xi ) for some         bounds, which are bounds introduced on the fly, via bound
variable xi . To this end, we introduce the following adaptation      tightening. The ground bounds, denoted l, u ∈ Rn , are used
of Farkas’ Lemma [66] to the Simplex setting, which states            in explaining dynamic bounds, denoted l0 , u0 ∈ Rn , via Farkas
that a linear-sized proof of this fact exists.                        vectors.
                                                                         For simplicity, we consider here a simple and popular
Lemma 2. Given the constraints A · V = 0 and l ≤ V ≤ u,               version of bound tightening, called interval propagation [25],
where A ∈ Mm×n (R) and l, V, u ∈ Rn , exactly one of these                                             P
                                                                      [47]. Given an equation xi =        cj · xj and current bounds
two options holds:                                                                                       j ∈B
                                                                                                           /
  1) The SAT case: ∃V ∈ Rn such that A · V = 0 and l ≤                l0 (x) and u0 (x) for each of the variables (whether these are the
     V ≤ u.                                                           ground bounds or dynamically tightened bounds themselves),
  2) The UNSAT case: ∃w ∈ Rm such that for all l ≤ V ≤ u,             a new upper bound for xi can be derived:
     w| · A · V < 0, whereas 0 · w = 0. Thus, w is a proof of                            X                       X
     the constraints’ unsatisfiability.                                   u0 (xi ) :=           cj · u0 (xj ) +         cj · l0 (xj ) (1)
Moreover, these vectors can be constructed during the run of                        xj ∈B,
                                                                                       / cj >0                  xj ∈B,
                                                                                                                   / cj <0
the Simplex algorithm.
                                                                      (provided that the new bound is tighter, i.e., smaller, than the
   This Lemma is actually a corollary of Theorem 3, which             current upper bound for xi ). A symmetrical version exists for
we introduce later. For a complete proof, see Appendix D.             discovering lower bounds.
   In our previous, UNSAT | example, one possible vector is            A naive approach for handling bound tightening is to store,
w = −2 1 0 −2 0 . Indeed, w · A · V = 0 gives us                      each time a new bound is discovered, a separate proof that
the equation −2x1 + 2x2 − b2 = 0. Given the lower and upper           justifies it; for example, a Farkas vector for deriving the
bounds for the participating variables, the largest value that        equation that was used in the bound tightening. However,
the left-hand side of the equation can obtain is:                     a Simplex execution can include many thousands of bound
  −2l(x1 ) + 2u(x2 ) − l(b2 ) = −2 · 2 + 2 · 1 − 0 = −2 < 0           tightenings — and so doing this would strain resources. Even
                                                                      worse, many of the intermediate bound tightenings might not
Therefore, no variable assignment within the stated bounds can
                                                                      even participate in deriving the final contradiction, and so
satisfy the equation, indicating that the constraints are UNSAT.
                                                                      storing them would be a waste.
   Given Lemma 2, all that remains is to instrument the
                                                                         In order to circumvent this issue, we propose a scheme in
Simplex solver in order to produce the proof vector w on
                                                                      which we store, for each variable in the query, a single column
the fly, whenever a contradiction is detected. In case a trivial
                                                                      vector that justifies its current lower bound, and another for its
contradiction l(xi ) > u(xi ) is given as part of the input
                                                                      current upper bound. Whenever a tighter bound is dynamically
query for some variable xi , we simply return “xi ” as the
                                                                      discovered, the corresponding vector is updated; and even if
proof (we later discuss also how to handle this case in the
                                                                      other, previously discovered dynamic bounds were used in the
presence of dynamic bound tightenings). Otherwise, a non-
                                                                      derivation, the vector that we store indicates how the same
trivial contradiction is detected as a result of an equation
              P                                                       bound can be derived using the ground bounds. Thus, the proof
e ≡ xi =          cj · xj , which contradicts one of the input
             j ∈B
               /
                                                                      of the tightened bounds remains compact, regardless of the
bounds of xi . In this case, no assignment can satisfy the            number of derived bounds; specifically, it requires only O(n ·
                                                                      m) space overall. Formally, we have the following result:
                    P
equivalent equation    cj · xj − xi = 0. Since the Simplex
                      j ∈B
                        /
algorithm applies only linear operations to the input tableau,        Theorem 3. Let A · V = 0 such that l ≤ V ≤ u be an LP
e is given by a linear combination of the original tableau rows.      instance, where A ∈ Mm×n (R) and l, V, u ∈ Rn .
Let coef (e) denote the Farkas vector of the equation e, i.e., the       Let u0 , l0 ∈ Rn represent dynamically tightened bounds of
column vector such that coef (e)| · A = e, and which proves           V . Then ∀i ∈ [n] ∃fu (xi ), fl (xi ) ∈ Rm such that fu (xi )| · A
unsatisfiability in this case. Our framework simply keeps track,      and fl (xi )| ·A can be used to efficiently compute u0 (xi ), l0 (xi )
for each row of the tableau, of its coefficient vector; and if that   from l and u. Moreover, vectors fu (xi ) and fl (xi ) can be
row leads to a contradiction, the vector is returned.                 constructed during the run of the Simplex algorithm.
    When a Simplex procedure with bound tightening reaches                                       V. DNN V ERIFICATION WITH P ROOFS
an UNSAT answer, it has discovered a variable xi with                                 A. Producing a proof-tree
l0 (xi ) > u0 (xi ). The theorem guarantees that in this case we
                                                                                         We now discuss how to leverage the results of Sec. IV
have two column vectors, fu (xi ) and fl (xi ), which explain
                                                                                      in order to produce the entire proof tree for an UNSAT
how u0 (xi ) and l0 (xi ) were discovered. We refer to these
                                                                                      DNN verification query. Recall that the main challenge lies in
vectors as the Farkas vectors of the upper and lower bounds of
                                                                                      accounting for the piecewise-linear constraints, which affect
xi , respectively. Because u0 (xi )−l0 (xi ) is negative, the column
                                                                                      the solving process by introducing case-splits.
vector w = fu (xi ) − fl (xi ) creates a tableau row which is
                                                                                         Each case split performed by the solver introduces a branch-
always negative, making w ∈ Rm a proof of unsatisfiability.
                                                                                      ing in the proof tree — with a new child node for each of the
The formal, constructive proof of the theorem appears in
                                                                                      linear phases of the constraint being split on — and introduces
Appendix C.
                                                                                      new equations and bounds. In the case of ReLU, one child
    In order to maintain fu (xi ) and fl (xi ) during the execution
                                                                                      node represents the active branch, through the equation f = b
of Simplex, whenever a tigher upper bound is tightened using
                                                                                      and bound b ≥ 0; and another represents the inactive branch,
Eq. 1, we update the matching Farkas vector:
                                                                                      with b ≤ 0 and 0 ≤ f ≤ 0. These new bounds become
                X                              X                                      the ground bounds for this node: their Farkas vectors are
fu (xi ) :=                cj · fu (xj ) +                cj · fl (xj ) + coef (e),   reset to zero, and all subsequent Farkas vectors refer to these
              j6=i,cj >0                     j6=i,cj <0                               new bounds (as opposed to the ground bounds of the parent
                                                                                      node). A new node inherits any previously-discovered dynamic
where e is the linear equation used for tightening, and coef (e)
                                                                                      bounds, as well as the Farkas vectors that explain them, from
is the column vector such that coef (e)| · A = e. The lower
                                                                                      its parent; these vectors remain valid, as ground bounds only
bound case is symmetrical. To demonstrate the procedure,
                                                                                      become tighter as a result of splitting (see Appendix F).
consider again the verification query from Fig. 2. Assume
                                                                                         For example, let us return to the query from Fig. 2 and the
the phases of v1 , v2 have both been set to active, and that
                                                                                      proof tree from Fig. 3. Initially, the solver decides to split on
consequently two new equations have been added: e4 : f1 =
                                                                                      v1 . This adds two new children to the proof tree. In the first
b1 , e5 : f2 = b2 . In this example, we have five linear
                                                                                      child, representing the inactive case, we update the ground
equations, so we initialize a zero vector of size five for each of
                                                                                      bounds u(b1 ) := 0, u(f1 ) := 0, and reset the corresponding
the variable bounds. Now, suppose Simplex tightens the lower
                                                                                      Farkas vectors fu (b1 ) and fu (f1 ) to 0. Now, Simplex can
bound of b1 using the first equation e1 :
                                                                                      tighten the lower bound of b1 using the first equation e1 :
                l0 (b1 ) := l(x1 ) − u(x2 ) = 2 − 1 = 1                                              l0 (b1 ) := l(x1 ) − u(x2 ) = 2 − 1 = 1
                                                                                                                                         |
and thus we update                                                                    resulting in the the updated fl (b1 ) = 1 0 0 , as shown in
                                                                                      Sec. IV, where we use vectors of size three since in this search
      fl (b1 ) := fl (x) − fu (y) + coef (e1 )                                        state we have three equations. Observe this bound contradicts
                                  |                                      |        the upper ground bound of b1 , represented by the zero vector.
               = 0 0 0 0 0 + 0 0                               0    0   0
                                  |                                                 We can then use the vector
               + 1 0 0 0 0                                                                                                       |          |
                 
               = 1 0 0 0 0
                                   |                                                       fu (b1 ) − fl (b1 ) = 0 − 1 0 0 = −1 0 0
                                                                                      as a proof for contradiction. Indeed, the matrix A0 , which is
since all fl and fu vectors have been initialized to 0 and                          obtained using the first three rows and columns of A as defined
                                  |
coef (e) = 1 0 0 0 0 — which indicates that e1 is                                     in Sec. III, corresponds to
simply the first row of the tableau.                                                                              the tableau
                                                                                                                             | before adding any new
                                                                                      equations. Observe that −1 0 0 · A0 · V = 0 gives the
   We can now tighten bounds again, using the fourth row                              equation −x1 +x2 +b1 = 0. Given the current ground bounds,
f1 = b1 , and get l0 (f1 ) := l0 (b1 ) = 1. We update fl (f1 ):                       the largest value of the left-hand side is:
      fl (f1 ) := fl (b1 ) + coef (e4 )                                                       −l(x1 ) + u(x2 ) + u(b1 ) = −2 + 1 + 0 = −1
                                    |                                    |
               = 1 0 0 0 0 + 0                             0    0   1   0             which is negative, meaning that no variable assignment within
                                    |
               = 1 0 0 1 0                                                            these bounds can satisfy the equation. This indicates that the
                                                                                      proof node representing v1 ’s inactive phase is UNSAT.
To see that the Farkas vector can indeed explain the dy-                                 In the second child, representing v1 ’s active case, we update
namically
          tightened
                 | bound, observe that the combination                               the ground bound l(b1 ) := 0 and the Farkas vector fl (b1 ) := 0.
 1 0 0 1 0 of tableau rows gives the equation f1 =                                    We also add the equation e4 : f1 = b1 . Next, the solver
x1 − x2 . We can then tighten the lower bound of f1 , using the                       performs another split on v2 , adding two new children to the
ground bounds: l0 (f1 ) := l(x1 ) − u(x2 ) = 2 − 1 = 1. This                          tree. In the first one (representing the inactive case) we update
bound matches the one that we had discovered dynamically,                             the ground bounds u(b2 ) := 0, u(f2 ) := 0, and reset the
though we derived it using ground bounds only.                                        corresponding Farkas vectors fu (b2 ) and fu (f2 ) to 0. In this
node, we have a contradiction already in the ground bounds,             VI. P ROOF C HECKING AND N UMERICAL S TABILITY
since u(f2 ) := 0 but l(f2 ) := 0.25. The contradiction in this        Checking the validity of a proof tree is straightforward.
case is comprised of a symbol for f2 .                              First, the checker must read the initial query and confirm that
   We are left with proving UNSAT for the last child, repre-        it is consistent with the LP and piecewise-linear constraints
senting the case where both ReLU nodes v1 , v2 are active.          stored at the root of the tree. Next, the checker begins a
For this node of the proof tree, we update the ground bound         depth-first traversal of the proof tree. Whenever it reaches
l(b2 ) := 0 and Farkas vector fl (b2 ) := 0, and add the equation   a new inner node, it must confirm that that node’s children
e5 : f2 = b2 . Recall that previously, we learned the tighter       correspond to the linear phases of a piecewise-linear constraint
bound l0 (f1 ) = 1. With the same   procedure as described
                                                     |        in   present in the query. Further, the checker must maintain a
Sec. IV, we can update fl (f1 ) = 1 0 0 1 0 . Now, we               list of current equations and lower and upper bounds, and
can use e2 : b2 = −2f1 to tighten u0 (b2 ) := −2l0 (f1 ) = −2,      whenever a new node is visited — update these lists (i.e., add
and consequently update the Farkas vector:                          equations and tighten bounds as needed), to reflect the LP
                                                                    stored in that node. Additionally, the checker must confirm
   fu (b2 ) = −2 · fl (f1 ) + coef (e2 )
                                      |              |          the validity of lemmas that appear in the node — specifically,
            = −2 · 1 0 0 1 0 + 0 1 0 0 0                            to confirm that they adhere to one of the permitted derivation
                                    |
            = −2 1 0 −2 0                                           rules. Finally, when a leaf node is visited, the checker must
                                                           |       confirm that the Farkas vector stored therein does indeed lead
The bound u0 (b2 ) = −2, explained by −2 1 0 −2 0
                                          
                                                                    to a contradiction when applied to the current LP — by
contradicts the ground bound l(b2 ) = 0 explained by the zero       ensuring that the linear combinationP   of rows created by the
vector. Therefore, we get the vector                                Farkas vector leads to a matrix row       cj · xj = 0, such that
                           |                        |           for any assignment of the variables, the left-hand side will
     −2 1 0 −2 0 − 0 = −2 1 0 −2 0                                  have a negative value.
as the proof of contraction for this node.                             The process of checking a proof certificate is thus much
                                                                    simpler than verifying a DNN using modern approaches,
B. Bound tightenings from piecewise-linear constraints              as it consists primarily of traversing a tree and computing
                                                                    linear combinations of the tableau’s columns. Furthermore, the
   Modern solvers often use sophisticated methods [25], [49],       proof checking process does not require using division for its
[61] to tighten variable bounds using the piecewise-linear          arithmetic computations, thus making the checking program
constraints. For example, if f = ReLU(b), then in particular        more stable arithmetically [43]. Consequently, we propose
b ≤ f , and so u(b) ≤ u(f ). Thus, if initially u(b) = u(f ) = 7    to treat the checker as a trusted code-base, as is commonly
and it is later discovered that u0 (f ) = 5, we can deduce          done [15], [48].
that also u0 (b) = 5. We show here how such tightening
can be supported by our proof framework, focusing on some           Complexity and Proof Size. Proving that a DNN verifi-
ReLU tightening rules as specified in Appendix E. Supporting        cation query is SAT (by providing a satisfying assignment)
additional rules should be similar.                                 is significantly easier than discovering an UNSAT witness
   We distinguish between two kinds of ReLU bound tight-            using our technique. Indeed, this is not surprising; recall that
enings. The first are tightenings that can be explained via         the DNN verification problem is NP-complete, and that yes-
a Farkas vector; these are handled the same way as bounds           instances of NP problems have polynomial-size witnesses (i.e.,
discovered using interval propagation. The second, more com-        polynomial-size proofs). Discovering a way to similarly pro-
plex tightenings are those that cannot be explained using an        duce polynomial proofs for no-instances of DNN verification
equation (and thus a Farkas vector). Instead, we treat these        is equivalent to proving that NP = coNP, which is a major
bound tightenings as lemmas, which are added to the proof           open problem [8] and might, of course, be impossible.
node along with their respective proofs; and the bounds that        Numerical Stability. Recall that enhancing DNN verifiers
they tighten are introduced as ground bounds, to be used in         with proof production is needed in part because they might
constructing future Farkas vectors. The proof for a lemma           produce incorrect UNSAT results due to numerical instability.
consists of Farkas vectors explaining any current bounds that       When this happens, the proof checking will fail when checking
were used in deducing it; as well as an indication of the           a proof leaf, and the user will receive warning. There are,
tightening rule that was used. The list of allowed tightening       however, cases where the query is UNSAT, but only the proof
rules must be agreed upon beforehand and provided to the            produced by the verifier is flawed. To recover from these cases
checker; in Appendix E, we present the tightening rules for         and correct the proof, we propose to use an external SMT
ReLUs that we currently support.                                    solver to re-solve the query stored in the leaf in question.
   For example, if f = ReLU(b) and u0 (f ) = 5 causes a                SMT solvers typically use sound arithmetic (as opposed to
bound tightening u0 (b) = 5, then this new bound u0 (b) = 5         DNN verifiers), and so their conclusions are generally more
is stored as a lemma. Its proof consists of the Farkas vector       reliable. Further, if a proof-producing SMT solver is used,
fu (f ) which explains why u0 (f ) = 5, and an indication of the    the proof that it produces could be plugged into the larger
deduction rule that was used (in this case, u0 (b) ≤ u0 (f )).      proof tree, instead of the incorrect proof previously discovered.
Although using SMT solvers to directly verify DNNs has been           of 45 networks and 4 properties to test on each, producing a
shown to be highly ineffective [47], [58], in our evaluation          total of 180 verification queries. Marabou returned an UNSAT
we observed that leaves typically represented problems that           result on 113 of these queries, and so we focus on them. In the
were significantly simpler than the original query, and could         future, we intend to evaluate our proof-production mechanism
be solved efficiently by the SMT solver.                              on other benchmarks as well.
                                                                         We set out to evaluate our proof production mechanism
         VII. I MPLEMENTATION AND E VALUATION                         along 3 axes: (i) correctness: how often was the checker able
                                                                      to verify the proof artifact, and how often did Marabou (prob-
Implementation. For evaluation purposes, we instrumented
                                                                      ably due to numerical instability issues) produce incorrect
the Marabou DNN verifier [49], [68] with proof production
                                                                      proofs?; (ii) overhead: by how much did Marabou’s runtime
capabilities. Marabou is a state-of-the-art DNN verifier, which
                                                                      increase due to the added overhead of proof production?; and
uses a native Simplex solver, and combines it with other
                                                                      (iii) checking time: how long did it take to check the produced
modern techniques — such as abstraction and abstract inter-
                                                                      proofs? Below we address each of these questions.
pretation [26], [27], [56], [61], [67], [70], advanced splitting
                                                                         Correctness. Over 1.46 million proof-tree leaves were cre-
heuristics [69], DNN optimization [62], and support for varied
                                                                      ated and checked as part of our experiments. Of these,
activation functions [6]. Additionally, Marabou has been ap-
                                                                      proof checking failed for only 77 leaves, meaning that the
plied to a variety of verification-based tasks, such as verifying
                                                                      Farkas vector written in the proof-tree leaf did not allow
recurrent networks [42] and DRL-based systems [3], [5], [28],
                                                                      the proof checker to deduce a contradiction. Out of the 113
[50], network repair [34], [59], network simplification [33],
                                                                      queries checked, 97 had all their proof-tree leaves checked
[51], and ensemble selection [4].
                                                                      successfully. As for the rest, typically only a tiny number
   As part of our enhancements to Marabou’s Simplex core,
                                                                      of leaves would fail per query, but we did identify a single
we added a mechanism that stores, for each variable, the
                                                                      query where a significant number of proofs failed to check
current Farkas vectors that explain its bounds. These vectors
                                                                      (see Fig. 4). We speculate that this query had some intrinsic
are updated with each Simplex iteration in which the tableau
                                                                      numerical issues encoded into it (e.g., equations with very
is altered. Additionally, we instrumented some of Marabou’s
                                                                      small coefficients [20]).
Simplex bound propagation mechanisms — specifically, those
that perform interval-based bound tightening on individual
                                                                                                   120
rows [25], to record for each tighter bound the Farkas vector
that justifies it. Thus, whenever the Simplex core declares                                        100   97
                                                                               Number of queries




UNSAT as a result of conflicting bounds, the proof infrastruc-
                                                                                                    80
ture is able to collect all relevant components for creating the
certificate for that particular leaf in the proof tree. Due to time                                 60
restrictions, we were not able to instrument all of Marabou’s
                                                                                                    40
many bound propagation components; this is ongoing work,
and our experiments described below were run with yet-                                              20           9
unsupported components turned off. The only exception is                                                                  5        1        1
                                                                                                     0
Marabou’s preprocessing component, which is not supported,                                               0      1         2        3        55
but is run before proof production starts.                                                               Number of leaves with incorrect proof
   In order to keep track of Marabou’s tree-like search, we
instrumented Marabou’s SmtCore class, which is in charge of
                                                                      Fig. 4: Number of queries per number of leaves with incorrect
case splitting and backtracking [49]. Whenever a case-split
                                                                      proofs.
was performed, the corresponding equations and bounds were
added to the proof tree as ground truths; and whenever a
                                                                         Next, when we encoded each of the 77 leaves as a query
previous split was popped, our data structures would backtrack
                                                                      to the cvc5 SMT solver [14], it was able to show that all
as well, returning to the previous ground bounds.
                                                                      queries were indeed UNSAT, in under 20 seconds per query.
   In addition to the instrumentation of Marabou, we also
                                                                      From this we learn that although some of the proof certificates
wrote a simple proof checker that receives a query and a proof
                                                                      produced by Marabou were incorrect, the ultimate UNSAT
artifact — and then checks, based on this artifact, that the
                                                                      result was correct. Further, it is interesting to note how quickly
query is indeed UNSAT. That checker also interfaces with the
                                                                      each of the queries could be solved. This gives rise to an
cvc5 SMT solver [14] for attempting recovery from numerical
                                                                      interesting verification strategy: use modern DNN verifiers to
instability errors.
                                                                      do the “heavy-lifting”, and then use more precise SMT solvers
Evaluation. We used our proof-producing version of Marabou            specifically on small components of the query that proved
to solve queries on the ACAS-Xu family of benchmarks for              difficult to solve accurately.
airborne collision avoidance [44]. We argue that the safety-             Overhead and Checking Time. In Fig. 5, we compare the
critical nature of this system makes it a prime candidate for         running time of vanilla Marabou, the overhead incurred by
proof production. Our set of benchmarks was thus comprised            our proof-production extension to Marabou, and the checking
                   160000                                                                     100%

                   140000

                   120000                                                                      75%

                   100000
      Time (sec)




                   80000                                                                       50%

                   60000

                   40000                                                                       25%

                   20000

                       0                                                                        0%
                            Solving time   Proof production time   Proof checking time                Solving time   Proof production time   Proof checking time




                                  Fig. 5: Proof production and checking time comparison — absolute (left) and relative (right)


time of the resulting proof certificates. We can see that the                            could be used to generate conflict clauses on-the-fly. Intu-
overhead of proof production time is relatively small for all                            itively, conflict clauses guide the verification algorithm to
queries (an average overhead of 5.7%), while the certification                           avoid any future search for a satisfying assignment within
time is non-negligible, but shorter than the time it takes to                            subspaces of the search space already proven to be UNSAT.
solve the queries by a factor of 66.5% on average.                                       Such clauses are a key component in modern SAT and SMT
                                                                                         solvers, and are the main component of CDCL algorithms [73]
                                      VIII. R ELATED W ORK                               — and could significantly curtail the search space traversed by
   The importance of proof production in verifiers has been                              DNN verifiers and improve their scalability.
repeatedly recognized, for example by the SAT, SMT, and
model-checking communities (e.g., [15], [21], [38]). Although                            Acknowledgments. This work was supported by the Is-
the risks posed by numerical imprecision within DNN verifiers                            rael Science Foundation (grant number 683/18), the ISF-
have been raised repeatedly [12], [43], [47], [46], we are                               NSFC joint research program (grant numbers 3420/21 and
unaware of any existing proof-producing DNN verifiers.                                   62161146001), the Binational Science Foundation (grant num-
   Proof production for various Simplex variants has been                                bers 2017662 and 2020250), and the National Science Foun-
studied previously [55]. In [24], Dutertre and de Moura study a                          dation (grant number 1814369).
Simplex variant similar to ours, but without explicit support for
dynamic bound tightening. Techniques for producing Farkas                                                             R EFERENCES
vectors have also been studied [10], but again without support
                                                                                         [1] E. Ábrahám and G. Kremer. SMT Solving for Arithmetic Theories:
for dynamic bound tightening, which is crucial in DNN                                        Theory and Tool Support. In Proc. 19th Int. Symposium on Symbolic
verification. Other uses of Farkas vectors, specifically in the                              and Numeric Algorithms for Scientific Computing (SYNASC), pages 1–8,
context of interpolants, have also been explored [9], [18].                                  2017.
                                                                                         [2] M. Akintunde, A. Kevorchian, A. Lomuscio, and E. Pirovano. Verifica-
   Other frameworks for proof production for machine learning                                tion of RNN-Based Neural Agent-Environment Systems. In Proc. 33rd
have also been proposed [7], [35]; but these frameworks are                                  AAAI Conf. on Artificial Intelligence (AAAI), pages 197–210, 2019.
interactive, unlike the automated mechanism we present here.                             [3] G. Amir, D. Corsi, R. Yerushalmi, L. Marzari, D. Harel, A. Farinelli,
                                                                                             and G. Katz. Verifying Learning-Based Robotic Navigation Systems,
                                                                                             2022. Technical Report. https://arxiv.org/abs/2205.13536.
                       IX. C ONCLUSION AND F UTURE WORK                                  [4] G. Amir, G. Katz, and M. Schapira. Verification-Aided Deep Ensemble
   We presented a novel framework for producing proofs of un-                                Selection. In Proc. 22nd Int. Conf. on Formal Methods in Computer-
                                                                                             Aided Design (FMCAD), 2022.
satisfiability for Simplex-based DNN verifiers. Our framework                            [5] G. Amir, M. Schapira, and G. Katz. Towards Scalable Verification
constructs a proof tree that contains lemma proofs in internal                               of Deep Reinforcement Learning. In Proc. 21st Int. Conf. on Formal
nodes and unsatisfiability proofs in each leaf. The certificates                             Methods in Computer-Aided Design (FMCAD), pages 193–203, 2021.
                                                                                         [6] G. Amir, H. Wu, C. Barrett, and G. Katz. An SMT-Based Approach for
of unsatisfiability that we provide can increase the reliability of                          Verifying Binarized Neural Networks. In Proc. 27th Int. Conf. on Tools
DNN verification, particularly when floating-point arithmetic                                and Algorithms for the Construction and Analysis of Systems (TACAS),
(which is susceptible to numerical instability) is used.                                     pages 203–222, 2021.
   We plan to continue this work along two orthogonal paths:                             [7] C. Anil, G. Zhang, A. Wu, and R. Grosse. Learning to Give Checkable
                                                                                             Answers with Prover-Verifier Games, 2021. Technical Report. https:
(i) extend our mechanism to support additional steps per-                                    //arxiv.org/abs/2108.12099.
formed in modern verifiers, such as preprocessing and addi-                              [8] S. Arora and B. Barak. Computational Complexity: A Modern Approach.
tional abstract interpretation steps [52], [61]; and (ii) use our                            Cambridge University Press, 2009.
                                                                                         [9] S. Asadi, M. Blicha, A. Hyvärinen, G. Fedyukovich, and N. Sharygina.
infrastructure to allow learning succinct conflict clauses [73].                             Farkas-Based Tree Interpolation. In Proc. 27th Int. Static Analysis
During search, the Farkas vectors produced by our approach                                   Symposium (SAS), pages 357–379, 2020.
[10] D. Avis and B. Kaluzny. Solving Inequalities and Proving Farkas’s                Networks with Abstract Interpretation. In Proc. 39th IEEE Symposium
     Lemma Made Easy. The American Mathematical Monthly, 111(2):152–                  on Security and Privacy (S&P), pages 3–18, 2018.
     157, 2004.                                                                  [33] S. Gokulanathan, A. Feldsher, A. Malca, C. Barrett, and G. Katz.
[11] G. Avni, R. Bloem, K. Chatterjee, T. Henzinger, B. Konighofer, and               Simplifying Neural Networks using Formal Verification. In Proc. 12th
     S. Pranger. Run-Time Optimization for Learned Controllers through                NASA Formal Methods Symposium (NFM), pages 85–93, 2020.
     Quantitative Games. In Proc. 31st Int. Conf. on Computer Aided              [34] B. Goldberger, Y. Adi, J. Keshet, and G. Katz. Minimal Modifications
     Verification (CAV), pages 630–649, 2019.                                         of Deep Neural Networks using Verification. In Proc. 23rd Int. Conf. on
[12] S. Bak, C. Liu, and T. Johnson. The Second International Verification            Logic for Programming, Artificial Intelligence and Reasoning (LPAR),
     of Neural Networks Competition (VNN-COMP 2021): Summary and                      pages 260–278, 2020.
     Results, 2021. Technical Report. http://arxiv.org/abs/2109.00498.           [35] S. Goldwasser, G. Rothblum, J. Shafer, and A. Yehudayoff. Interactive
[13] T. Baluta, S. Shen, S. Shinde, K. Meel, and P. Saxena. Quantitative              Proofs for Verifying Machine Learning. In Proc. 12th Innovations in
     Verification of Neural Networks And its Security Applications. In Proc.          Theoretical Computer Science Conf. (ITCS), 2021.
     ACM SIGSAC Conf. on Computer and Communications Security (CCS),             [36] I. Goodfellow, Y. Bengio, and A. Courville. Deep Learning. MIT Press,
     pages 1249–1264, 2019.                                                           2016.
[14] H. Barbosa, C. Barrett, M. Brain, G. Kremer, H. Lachnitt, M. Mann,          [37] I. Goodfellow, J. Shlens, and C. Szegedy. Explaining and Harnessing
     A. Mohamed, M. Mohamed, A. Niemetz, A. Nötzli, A. Ozdemir,                      Adversarial Examples, 2014. Technical Report. http://arxiv.org/abs/1412.
     M. Preiner, A. Reynolds, Y. Sheng, C. Tinelli, and Y. Zohar. cvc5: A             6572.
     Versatile and Industrial-Strength SMT Solver. In Proc. 28th Int. Conf.      [38] A. Griggio, M. Roveri, and S. Tonetta. Certifying Proofs for SAT-Based
     on Tools and Algorithms for the Construction and Analysis of Systems             Model Checking. Formal Methods in System Design, 57(2):178–210,
     (TACAS), pages 415–442, 2022.                                                    2021.
[15] C. Barrett, L. de Moura, and P. Fontaine. Proofs in Satisfiability Modulo   [39] The Gurobi Optimizer. https://www.gurobi.com/.
     Theories. All about Proofs, Proofs for All, 55(1):23–44, 2015.              [40] P. Henriksen and A. Lomuscio. Efficient Neural Network Verification via
[16] C. Barrett and C. Tinelli. Satisfiability Modulo Theories. In Handbook           Adaptive Refinement and Adversarial Search. In Proc. 24th European
     of Model Checking, pages 305–343. Springer, 2018.                                Conf. on Artificial Intelligence (ECAI), pages 2513–2520, 2020.
[17] O. Bastani, Y. Ioannou, L. Lampropoulos, D. Vytiniotis, A. Nori, and        [41] X. Huang, M. Kwiatkowska, S. Wang, and M. Wu. Safety Verification
     A. Criminisi. Measuring Neural Net Robustness with Constraints. In               of Deep Neural Networks. In Proc. 29th Int. Conf. on Computer Aided
     Proc. 30th Conf. on Neural Information Processing Systems (NIPS),                Verification (CAV), pages 3–29, 2017.
     2016.                                                                       [42] Y. Jacoby, C. Barrett, and G. Katz. Verifying Recurrent Neural Networks
[18] M. Blicha, A. Hyvärinen, J. Kofron̆, and N. Sharygina. Decomposing              using Invariant Inference. In Proc. 18th Int. Symposium on Automated
     Farkas Interpolants. In Proc. 25th Int. Conf. on Tools and Algorithms for        Technology for Verification and Analysis (ATVA), pages 57–74, 2020.
     the Construction and Analysis of Systems (TACAS), pages 3–20, 2019.         [43] K. Jia and M. Rinard. Exploiting Verified Neural Networks via Floating
[19] M. Bojarski, D. Del Testa, D. Dworakowski, B. Firner, B. Flepp,                  Point Numerical Error. In Proc. 28th Int. Static Analysis Symposium
     P. Goyal, L. Jackel, M. Monfort, U. Muller, J. Zhang, X. Zhang, J. Zhao,         (SAS), pages 191–205, 2021.
     and K. Zieba. End to End Learning for Self-Driving Cars, 2016.              [44] K. Julian, M. Kochenderfer, and M. Owen. Deep Neural Network
     Technical Report. http://arxiv.org/abs/1604.07316.                               Compression for Aircraft Collision Avoidance Systems. Journal of
[20] V. Chvátal. Linear Programming. W. H. Freeman and Company, 1983.                Guidance, Control, and Dynamics, 42(3):598–608, 2019.
                                                                                 [45] K. Julian, J. Lopez, J. Brush, M. Owen, and M. Kochenderfer. Policy
[21] S. Conchon, A. Mebsout, and F. Zaı̈di. Certificates for Parameterized
                                                                                      Compression for Aircraft Collision Avoidance Systems. In Proc. 35th
     Model Checking. In Proc. 20th Int. Symposium on Formal Methods
                                                                                      Digital Avionics Systems Conf. (DASC), pages 1–10, 2016.
     (FM), pages 126–142, 2015.
                                                                                 [46] G. Katz, C. Barrett, D. Dill, K. Julian, and M. Kochenderfer. Reluplex:
[22] G. Dantzig. Linear Programming and Extensions. Princeton University
                                                                                      An Efficient SMT Solver for Verifying Deep Neural Networks. In Proc.
     Press, 1963.
                                                                                      29th Int. Conf. on Computer Aided Verification (CAV), pages 97–117,
[23] L. de Moura and N. Bjørner. Satisfiability Modulo Theories: Introduction         2017.
     and Applications. Communications of the ACM, 54(9):69–77, 2011.             [47] G. Katz, C. Barrett, D. Dill, K. Julian, and M. Kochenderfer. Reluplex: a
[24] B. Dutertre and L. de Moura. A Fast Linear-Arithmetic Solver for                 Calculus for Reasoning about Deep Neural Networks. Formal Methods
     DPLL(T). In Proc. 18th Int. Conf. on Computer Aided Verification                 in System Design (FMSD), 2021.
     (CAV), pages 81–94, 2006.                                                   [48] G. Katz, C. Barrett, C. Tinelli, A. Reynolds, and L. Hadarean. Lazy
[25] R. Ehlers. Formal Verification of Piece-Wise Linear Feed-Forward                 Proofs for DPLL(T)-Based SMT Solvers. In Proc. 16th Int. Conf. on
     Neural Networks. In Proc. 15th Int. Symp. on Automated Technology                Formal Methods in Computer-Aided Design (FMCAD), pages 93–100,
     for Verification and Analysis (ATVA), pages 269–286, 2017.                       2016.
[26] Y. Elboher, E. Cohen, and G. Katz. Neural Network Verification using        [49] G. Katz, D. Huang, D. Ibeling, K. Julian, C. Lazarus, R. Lim, P. Shah,
     Residual Reasoning. In Proc. 20th Int. Conf. on Software Engineering             S. Thakoor, H. Wu, A. Zeljić, D. Dill, M. Kochenderfer, and C. Barrett.
     and Formal Methods (SEFM), 2022.                                                 The Marabou Framework for Verification and Analysis of Deep Neural
[27] Y. Elboher, J. Gottschlich, and G. Katz. An Abstraction-Based Frame-             Networks. In Proc. 31st Int. Conf. on Computer Aided Verification
     work for Neural Network Verification. In Proc. 32nd Int. Conf. on                (CAV), pages 443–452, 2019.
     Computer Aided Verification (CAV), pages 43–65, 2020.                       [50] Y. Kazak, C. Barrett, G. Katz, and M. Schapira. Verifying Deep-RL-
[28] T. Eliyahu, Y. Kazak, G. Katz, and M. Schapira. Verifying Learning-              Driven Systems. In Proc. 1st ACM SIGCOMM Workshop on Network
     Augmented Systems. In Proc. Conf. of the ACM Special Interest Group              Meets AI & ML (NetAI), pages 83–89, 2019.
     on Data Communication on the Applications, Technologies, Architec-          [51] O. Lahav and G. Katz. Pruning and Slicing Neural Networks using
     tures, and Protocols for Computer Communication (SIGCOMM), pages                 Formal Verification. In Proc. 21st Int. Conf. on Formal Methods in
     305–318, 2021.                                                                   Computer-Aided Design (FMCAD), pages 183–192, 2021.
[29] A. Esteva, A. Robicquet, B. Ramsundar, V. Kuleshov, M. DePristo,            [52] Z. Lyu, C.-Y. Ko, Z. Kong, N. Wong, D. Lin, and L. Daniel. Fastened
     K. Chou, C. Cui, G. Corrado, S. Thrun, and J. Dean. A Guide to                   Crown: Tightened Neural Network Robustness Certificates. In Proc.
     Deep Learning in Healthcare. Nature medicine, 25(1):24–29, 2019.                 34th AAAI Conf. on Artificial Intelligence (AAAI), pages 5037–5044,
[30] K. Eykholt, I. Evtimov, E. Fernandes, B. Li, A. Rahmati, C. Xiao,                2020.
     A. Prakash, T. Kohno, and D. Song. Robust Physical-World Attacks on         [53] A. Makhorin. GLPK (GNU Linear Programming Kit). https://www.gnu.
     Deep Learning Visual Classification. In Proc. IEEE Conf. on Computer             org/s/glpk/glpk.html.
     Vision and Pattern Recognition (CVPR), pages 1625–1634, 2018.               [54] M. Müller, G. Makarchuk, G. Singh, M. Püschel, and M. Vechev.
[31] D. Fremont, J. Chiu, D. Margineantu, D. Osipychev, and S. Seshia.                PRIMA: General and Precise Neural Network Certification via Scalable
     Formal Analysis and Redesign of a Neural Network-Based Aircraft                  Convex Hull Approximations. In Proc. 49th ACM SIGPLAN Symposium
     Taxiing System with VERIFAI. In Proc. 32nd Int. Conf. on Computer                on Principles of Programming Languages (POPL), 2022.
     Aided Verification (CAV), pages 122–134, 2020.                              [55] G. Necula. Compiling with Proofs. Carnegie Mellon University, 1998.
[32] T. Gehr, M. Mirman, D. Drachsler-Cohen, E. Tsankov, S. Chaudhuri,           [56] M. Ostrovsky, C. Barrett, and G. Katz. An Abstraction-Refinement
     and M. Vechev. AI2: Safety and Robustness Certification of Neural                Approach to Verifying Convolutional Neural Networks. In Proc. 20th.
     Int. Symposium on Automated Technology for Verification and Analysis
     (ATVA), 2022.
                                                                               Appendix
[57] L. Pulina and A. Tacchella. An Abstraction-Refinement Approach to
     Verification of Artificial Neural Networks. In Proc. 22nd Int. Conf. on
     Computer Aided Verification (CAV), pages 243–257, 2010.
[58] L. Pulina and A. Tacchella. Challenging SMT Solvers to Verify Neural                      A. T HE S IMPLEX C ALCULUS
     Networks. AI Communications, 25(2):117–135, 2012.
[59] I. Refaeli and G. Katz. Minimal Multi-Layer Modifications of Deep
     Neural Networks. In Proc. 5th Workshop on Formal Methods for ML-
     Enabled Autonomous Systems (FoMLAS), 2022.                                   There exist numerous flavors and implementations of the
[60] S. Sankaranarayanan, S. Dutta, and S. Mover. Reaching Out Towards         Simplex algorithm for solving LP instances [22]. To make our
     Fully Verified Autonomous Systems. In Proc. 13th Int. Conf. on
     Reachability Problems (RP), pages 22–32, 2019.                            proof-production scheme compatible with many of them, we
[61] G. Singh, T. Gehr, M. Püschel, and M. Vechev. An Abstract Domain for     used it to extend the following, abstract version of Simplex,
     Certifying Neural Networks. In Proc. 46th ACM SIGPLAN Symposium           where the algorithm is given as a set of derivation rules. This
     on Principles of Programming Languages (POPL), pages 1–30, 2019.
[62] C. Strong, H. Wu, A. Zeljić, K. Julian, G. Katz, C. Barrett, and         formulation, which appears below, is borrowed from Katz et
     M. Kochenderfer. Global Optimization of Objective Functions Repre-        al. [47] (see therein for additional details).
     sented by ReLU Networks. Journal of Machine Learning, pages 1–28,
     2021.                                                                        Let X denote a set of variables: X = {x1 , . . . , xn }. We
[63] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfel-     define a simplex configuration to be either one of the dis-
     low, and R. Fergus. Intriguing Properties of Neural Networks, 2013.       tinguished symbols {SAT, UNSAT}, or a tuple hB, A, l, u, αi.
     Technical Report. http://arxiv.org/abs/1312.6199.
[64] V. Tjeng, K. Xiao, and R. Tedrake. Evaluating Robustness of Neural        The tuple is comprised of the following components:
     Networks with Mixed Integer Programming, 2017. Technical Report.
     http://arxiv.org/abs/1711.07356.                                            • B ⊆ X is the set of basic variables.
[65] H.-D. Tran, S. Bak, W. Xiang, and T. Johnson. Verification of Deep          • A, also called Pthe tableau, contains for each xi ∈ B an
     Convolutional Neural Networks Using ImageStars. In Proc. 32nd Int.
     Conf. on Computer Aided Verification (CAV), pages 18–42, 2020.                equation xi = xj ∈B  / cj x j .
[66] R. Vanderbei. Linear Programming: Foundations and Extensions.               • l and u are mappings, which assign to each variable x ∈
     Springer, Berlin, 1996.                                                       X a lower and an upper bound, respectively.
[67] S. Wang, K. Pei, J. Whitehouse, J. Yang, and S. Jana. Formal Security
     Analysis of Neural Networks using Symbolic Intervals. In Proc. 27th         • α, called the assignment, is a mapping from each variable
     USENIX Security Symposium, pages 1599–1614, 2018.                             x ∈ X to a real value assigned to it
[68] H. Wu, A. Ozdemir, A. Zeljić, A. Irfan, K. Julian, D. Gopinath,
     S. Fouladi, G. Katz, C. Păsăreanu, and C. Barrett. Parallelization      When beginning a Simplex execution, the initial configuration
     Techniques for Verifying Neural Networks. In Proc. 20th Int. Conf. on
     Formal Methods in Computer-Aided Design (FMCAD), pages 128–137,           (including the initial tableau A0 ) is created
                                                                                                                           P to match the input
     2020.                                                                     LP instance. Specifically, each equation xi ∈X ci xi = d that
[69] H. Wu, A. Zeljić, K. Katz, and C. Barrett. Efficient Neural Network      appears in thePinput is assigned a fresh basic variable b, and the
     Analysis with Sum-of-Infeasibilities. In Proc. 28th Int. Conf. on Tools
     and Algorithms for the Construction and Analysis of Systems (TACAS),      equation b = xi ∈X ci xi is added to the tableau. Additionally,
     pages 143–163, 2022.                                                      d is set as both the lower and upper bound for b. The initial
[70] T. Zelazny, H. Wu, C. Barrett, and G. Katz. On Reducing Over-             assignment is 0 for each of the variables, thus ensuring that
     Approximation Errors for Neural Network Verification. In Proc. 22nd
     Int. Conf. on Formal Methods in Computer-Aided Design (FMCAD),            all tableau equations hold (though this assignment may violate
     2022.                                                                     variable bounds).
[71] C. Zhang, T. Su, Y. Yan, F. Zhang, G. Pu, and Z. Su. Finding
     and Understanding Bugs in Software Model Checkers. In Proc. 27th             It is often convenient to regard the tableau A as a matrix,
     ACM Joint Meeting on European Software Engineering Conference and         where each row expresses a basic variables (a variable in B) as
     Symposium on the Foundations of Software Engineering (ESEC/FSE),          a linear combination of non-basic variables (those in X \ B).
     pages 673–773, 2019.
[72] H. Zhang, M. Shinn, A. Gupta, A. Gurfinkel, N. Le, and N. Narodytska.        Then, the rows of A correspond to the basic variables, and
     Verification of Recurrent Neural Networks for Cognitive Tasks via         its columns to the non-basic variables. For xi ∈ B and xj ∈  /B
     Reachability Analysis. In Proc. 24th European Conf. on Artificial
     Intelligence (ECAI), pages 1690–1697, 2020.                               we usePAi,j to denote the coefficient cj of xj in the equation
[73] L. Zhang, C. Madigan, M. Moskewicz, and S. Malik. Efficient Conflict      xi = xj ∈B / cj xj . The tableau is changed via pivoting: the
     Driven Learning in a Boolean Satisfiability Solver. In Proc. IEEE/ACM     switching of one basic variable xi (the leaving variable) with
     Int. Conf. on Computer Aided Design (ICCAD), pages 279–285, 2001.
                                                                               one non-basic variable xj (the entering variable), for which
                                                                               Ai,j 6= 0. When a pivot(A, i, j) operation is performed,
                                                                                                                                  P           it
                                                                               returns a new tableau, where the equation xP   i =       / ck x k
                                                                                                                                     xk ∈B
                                                                                                                                          ck
                                                                               has been replaced by the equation xj = xcji − xk ∈B,k6
                                                                                                                                  /   =j cj xk ,
                                                                               and in which any occurrences xj in each of the other equations
                                                                               has been replaced by the right-hand side of the new equation
                                                                               (and the resulting expressions are normalized to fit the tableau
                                                                               form). The variable assignment, α, can be changed via update
                                                                               operations (which are applied to non-basic variables): for xj ∈/
                                                                               B, an update(α, xj , δ) operation returns an updated assignment
                                                                               α0 , which is identical to α except that α0 (xj ) = α(xj ) + δ;
                                                                               and for every xi ∈ B, we have that α0 (xi ) = α(xi ) + δ · Ai,j .
                                                 xi ∈ B, α(xi ) < l(xi ), xj ∈ slack+ (xi )
                                      Pivot1
                                                 A := pivot(A, i, j), B := B ∪ {xj } \ {xi }

                                                 xi ∈ B, α(xi ) > u(xi ), xj ∈ slack− (xi )
                                      Pivot2
                                                 A := pivot(A, i, j), B := B ∪ {xj } \ {xi }

                                  xj ∈
                                     / B, α(xj ) < l(xj ) ∨ α(xj ) > u(xj ), l(xj ) ≤ α(xj ) + δ ≤ u(xj )
                       Update
                                                          α := update(α, xj , δ)

                            xi ∈ B, (α(xi ) < l(xi ) ∧ slack+ (xi ) = ∅) ∨ (α(xi ) > u(xi ) ∧ slack− (xi ) = ∅)
                 Failure1
                                                                 UNSAT

                                                                l(xi ) > u(xi )
                                                     Failure2
                                                                   UNSAT

                                                      ∀xi ∈ X . l(xi ) ≤ α(xi ) ≤ u(xi )
                                           Success
                                                                     SAT
                                    Fig. 6: Derivation rules for the abstract simplex algorithm.


To simplify later presentation we also denote:                          Suppose a Simplex run ended in the distinguished state
                                                                     UNSAT. There are precisely two deduction rules that result
       slack+ (xi ) =                                                in a transition to this state. The first, Failure2 , can only be
                 {xj ∈
                     / B | (Ai,j > 0 ∧ α(xj ) < u(xj ))∨             triggered if there is an explicit bound contradiction for one of
                 (Ai,j < 0 ∧ α(xj ) > l(xj ))}                       the variable, thus proving the lemma. The second, Failure1 ,
             −                                                       can only be triggered if there exists a basic variable xi , whose
       slack (xi ) =                                                                        P
                                                                     tableau row is xi =       cj · xj , with either
                 {xj ∈
                     / B | (Ai,j < 0 ∧ α(xj ) < u(xj ))∨                                    j ∈B
                                                                                              /

                 (Ai,j > 0 ∧ α(xj ) > l(xj ))}                                        α(xi ) < l(xi ) ∧ slack + (xi ) = ∅
   Fig. 6 depicts the rules of the Simplex calculus, in guarded      or
assignment form. We say that a rule applies to a configuration                      α(xi ) > u(xi ) ∧ slack − (xi ) = ∅
S if all of its premises hold in S. A rule’s conclusion describes
how each component of S is (possibly) changed. We say that              If the first condition holds, then variable xi ’s assignment
S derives S 0 if S 0 is the result of applying a rule to S. A        is below its lower bound, and for all j 6= i, if Ai,j < 0
derivation is a sequence of configurations Si , where each Si        (equivalently, cj < 0), then xj is pressed against its lower
derives Si+1 .                                                       bound; and if Ai,j > 0 (equivalently, cj > 0), then xj is
   The Simplex calculus is known to be sound [66] (i.e., if a        pressed against its upper bound. Therefore, the right-hand side
                                                                                              P
derivation ends in SAT or UNSAT, then the original problem           of the equation xi =       cj · xj is pressed against its upper
is satisfiable or unsatisfiable, respectively) and complete (there                            j ∈B
                                                                                                /
always exists a derivation ending in either SAT or UNSAT from        bound. Since the upper bound of the left-hand side, xi , cannot
any starting configuration). Termination can be guaranteed if        be greater than the upper bound of the right-hand side, we
certain strategies are used in applying the transition rules — in    conclude that:
particular in picking the leaving and entering variables when
                                                                                      X                     X
                                                                           u(xi ) ≤         cj · u(xj ) +         cj · l(xj )
multiple options exist [66].                                                          j ∈B,c
                                                                                        /   j >0                   j ∈B,c
                                                                                                                     /   j <0
                                                                                         X                            X
                     B. P ROOF OF LEMMA 1                                         =                cj · α(xj ) +                cj · α(xj )
                                                                                      j ∈B,c
                                                                                        /   j >0                   j ∈B,c
                                                                                                                     /   j <0
   Recall the following lemma, which was introduced in Sec-                       = α(xi ) < l(xi )
tion IV:
                                                                     where the second transition is correct because the variables
Lemma 1. If Simplex returns UNSAT, then there exists a
                                                                     are pressed against their bounds, as we described.
variable with contradicting bounds; that is, there exists a
                                                                        The proof for the second case is symmetrical. In either case,
variable xi ∈ V with lower and upper bounds l(xi ) and u(xi ),
                                                                     we get that if the Failure2 rule is applicable, then Simplex
for which Simplex has discovered that l(xi ) > u(xi ).
                                                                     has discovered a variable with contradicting lower and upper
  We now formally prove this lemma.                                  bounds, as needed.
                      C. P ROOF OF THEOREM 3                                  Upon initialization of the Simplex algorithm, for each vari-
   Before proving the theorem, we begin by describing the                  able xi we assign two vectors, fu (xi ), fl (xi ) = 0, to represent
procedure for deducing a bound using a Farkas vector w. We                 that no bound tightening has occurred for xi . Whenever one
assume without loss of generality, that the Tableau is of the              of its bounds is updated, the corresponding vector is updated.
form AV = 0, for V the variables vector. If this is initially              In the case of an upper bound, we set
not so, we add a fresh variable xj to every row j of A, and
set l(xj ) = u(xj ) = −bj .                                                                 X                             X
                                                                           fu (xi ) :=                cj · fu (xj ) +             cj · fl (xj ) + coef (e)
   Given a tableau A ∈ Mm×n , bounds u, l and a column
                                                                                         j6=i,cj >0                     j6=i,cj <0
vector w ∈ Rm , the row vector w| · A · V corresponds to
                                  n
an equation of the form 0 =
                                 P
                                    cj · xj , or equivalently xi =         where coef (e) is a column vector such that coef (e)| · A = e.
                                 j=0                                          The case of xi ’s lower bound is symmetrical. The tightening
P
   cj · xj + (ci + 1) · xi . We seek to use the right-hand of the          is performed according to the equation
j6=i
equation to deduce tighter bounds for its left-hand side.
                                                                                               X                     X
                                                                                  l0 (xi ) :=        cj · l0 (xj ) +    cj · u0 (xj )
  Suppose we are able to learn a tighter upper bound for                                       j6=i,cj >0                    j6=i,cj <0
xi (the lower bound case is symmetrical). In this case, the
new upper bound learned for xi is the upper bound of the                   and the update rule is
expression                                                                              X                                X
                 X                                                          fl (xi ) :=      cj · fl (xj ) +                     cj · fu (xj ) + coef (e)
                     cj · xj + (ci + 1) · xi ,                                           j6=i,cj >0                 j6=i,cj <0
                       j6=i
                                                                              In order to prove the theorem, we need to prove the
which is
    X                             X                                        following invariant: regardless of the bounds dynamically
                cj · u(xj ) +            cj · l(xj ) + (ci + 1) · γ(xi )   tightened so far, the two vectors fu (xi ), fl (xi ) can always
   j6=i,cj >0                   j6=i,cj <0                                 be used to deduce the current tightest bounds u0 (xi ), l0 (xi )
                                                                           from the ground bounds. A key point is that this holds even if
Where γ(xi ) = u(xi ) if ci +1 > 0, or γ(xi ) = l(xi ) otherwise.          u0 (xi ) and l0 (xi ) were discovered by Simplex using previously
  We now use the aforementioned observation in proving                     tightened bounds for other variables.
Theorem 3. Let us recall the theorem itself:                                  We now prove this claim, by induction, for fu (xi ); the proof
Theorem 3. Let A · V = 0 such that l ≤ V ≤ u be an LP                      for fl (xi ) is symmetrical and is omitted.
instance, where A ∈ Mm×n (R) and l, V, u ∈ Rn .
                                                                              Base case: Suppose no tighter upper bound was learned
   Let u0 , l0 ∈ Rn represent dynamically tightened bounds of
                                                                           for the variable xi , so u0 (xi ) equals the ground upper bound
V . Then ∀i ∈ [n] ∃fu (xi ), fl (xi ) ∈ Rm such that fu (xi )| · A
                                                                           u(xi ). In this case, fu (xi ) is initialized to 0, and fu (xi )| · A
and fl (xi )| ·A can be used to efficiently compute u0 (xi ), l0 (xi )
                                                                           produces a zero row vector. Therefore ci = 0, and the upper
from l and u. Moreover, vectors fu (xi ) and fl (xi ) can be
                                                                           bound deduced is
constructed during the run of the Simplex algorithm.
                                                                                                     u0 (xi ) = u(xi ).
   The proof that we provide next is constructive. Observe
variable xi , for which a dynamic bound is currently being                     Suppose that u0 (xi ) is the first bound being updated dy-
discovered. As we observed before, this tightening is being                namically using equation e. In this case, for all j 6= i we have
performed using an equation of the form xi =
                                                        P
                                                            cj · x j ,     fl (xj ) = fu (xj ) = 0, and so we get that fu (xi ) = coef (e).
                                                        j6=i               Consequently,
                                                                                                    fu (xi )| · A = e
                                 P
which is equivalent to 0 =            cj · xj − xi . We define the
                                 j6=i                                                                                  P
                                                                                                                         cj · xj − xi which
                         
vector e = e1 , . . . , en as:                                             which indeed produces the equation 0 =
                                                                                                                                     j6=i
                                                                           was used for the tightening. We then have ci = −1, and the
                            (
                              −1 if k = i
                       ek =                                                deduced bound is
                              cj    otherwise
                                                                                      X                   X
This vector represents the coefficients of the equation that is            u0 (xi ) =       cj · u(xj ) +      cj · l(xj ) + (−1 + 1) · ui .
                                                                                     j6=i,cj >0                  j6=i,cj <0
used for bound tightening using the product e · V .
  Suppose that the bound being tightened is xi ’s upper bound.
In that case, the new bound is given by:                                      Inductive step: In the general case, fu (xi ) is updated using
                    X                    X                                 previously tightened bounds. Consequently, for j 6= i, the
       u0 (xi ) :=       cj · u0 (xj ) +       cj · l0 (xj )               vectors fu (xj ) and fl (xj ) need not be the zero vectors. In
                     j6=i,cj >0                 j6=i,cj <0                 this case we have that:
i.e., the new upper bound of xi is set to match the upper bound
                                                                                            X                       X
                                                                           fu (xi )| ·A =        cj ·fu (xj )| ·A+          cj ·fl (xj )| ·A+e
of the equation on the right-hand side.                                                     j6=i,cj >0                        j6=i,cj <0
   Using the induction hypothesis, we have that each fu (xj )| ·        applied, the tableau is multiplied by elementary matrices. Let
A, fl (xj )| · A P
                 is equal to some vector that represents a row of       e = (c, d) be a tableau row after several pivots have been
the form 0 = bk,j · xk , where the bound of xj is tightened             applied, where d ∈ Rm corresponds to the last m coefficients
                                                                        of e. We then have that d is a row of Ek · ... · E1 · I for
        P
using      bk,j · xk + (bj,j + 1) · xj . It is important to note here
      k6=j                                                              some sequence of elementary matrices, or equivalently,
that it is possible that bj,i 6= 0, and thus the coefficient of xi      d = e|l · Ek · ... · E1 , and similarly c = e|l · Ek · ... · E1 · C.
in fu (xi )| · A might not be −1.                                       We have that d · C = e|l · Ek · ... · E1 · C = c. We conclude
   Based on the above, we get that fu (xi )| · A produces the           that d · A = d · C | d · I = (c, d) = e. 
equation:
                                                                         Hence, an efficient algorithm for extracting coef (e) from e
             X       X                                                  is to extract its last m entries, and transpose that vector.
     =         cj ·  bk,j · xk + bj,j · xj +
          j6=i,cj >0       k6=j
                                                                                          D. P ROOF OF L EMMA 2
             X       X
     =         cj ·  bk,j · xk,j + bj,j · xj +                          Recall Lemma 2, which we introduced in Sec. IV:
          j6=i,cj <0       k6=j
                                                                        Lemma 2. Given the constraints A · V = 0 and l ≤ V ≤ u,
                                                                        where A ∈ Mm×n (R) and l, V, u ∈ Rn , exactly one of these
       X
     =  cj · x j − x i
          j6=i                                                          two options holds:
                                                         
             X               X                                           1) The SAT case: ∃V ∈ Rn such that A · V = 0 and l ≤
      =                cj ·  bk,j · xk + (bj,j + 1) · xj +                V ≤ u.
          j6=i,cj >0        k6=j                                         2) The UNSAT case: ∃w ∈ Rm such that for all l ≤ V ≤ u,
                                                                            w| · A · V < 0, whereas 0 · w = 0. Thus, w is a proof of
                                                 
             X       X
     =         cj ·  bk,j · xk + (bj,j + 1) · xj  − xi                    the constraints’ unsatisfiability.
          j6=i,cj <0       k6=j                                         Moreover, these vectors can be constructed during the run of
  In other words, the tighter bound that is currently being             the Simplex algorithm.
deduced is derived using the sum                                           We now give a formal proof for this Lemma.
                                                  
          X           X                                                    Since the Simplex calculus that we use is sound and
                cj ·  bk,j · xk + (bj,j + 1) · xj +                   complete [47], and since it returns a satisfying assignment V
          j6=i,cj >0        k6=j                                        for a satisfiable query, we only need to focus on the UNSAT
                                                                      query. Specifically, we need to show the existence of a vector
                                                                        w ∈ Rm when the constraints are unsatisfiable.
             X       X
               cj ·  bk,j · xk + (bj,j + 1) · xj ,
          j6=i,cj <0        k6=j                                           Observe a row of the tableau, and its corresponding equation
                                                                              Pn
which, according to the induction hypothesis, has an upper              a =       cj · xj . The upper bound of a that can be derived
                                                                              j=1
bound of                                                                from the equation, denoted u(a), is a linear combination of
            X                     X                                     the bounds of the xj ’s, where we take the upper bounds for
                  cj · u0 (xj ) +    cj · l0 (xj ),
                                                                        variables with a positive coefficient cj , and the lower bounds
              j6=i,cj >0              j6=i,cj <0
                                                                        for negative cj values. More formally,
exactly as desired — thus completing the proof.                                             X                  X
   We end this section with a straightforward algorithm for                        u(a) =        cj · u(xj ) +       cj · l(xj )
extracting coef (e) when given e. We assume, without loss of                                j,cj >0             j,cj <0
generality, that b is the zero vector, and that the m right-most
columns of A form the identity matrix (if this is initially not         The lower bound for a that can be derived from the equation
so, we add a fresh variable xj to every row j of A, and set             is marked l(a), and is defined symmetrically.
l(xj ) = u(xj ) = −bj .)                                                   By Lemma 1, the Simplex algorithm concludes that a query
                                                                        is UNSAT if and only if it discovers a variable xi with
Theorem 4. The coefficients of a tableau row e are equal to
                                                                        inconsistent bounds l0 (xi ) > u0 (xi ) (whether these are ground
its last m entries, where m is the number of tableau rows.
                                                                        bounds, or bounds discovered through an equation). Theorem 3
Formally, consider a tableau of the form A := [C | I] = 0,
                                                                        then states that there exists fu (xi ), fl (xi ) ∈ Rm that witness
where C ∈ Mm×n−m (R) and I is the identity matrix of size
                                                                        these bounds. From the proof of Theorem 3, we know that
m. Let e = (c, d) be a row in the tableau, where d ∈ Rm is
                                                                        fu (xi )| · A = r, and we have proved that u0 (xi ) = u(r + xi ).
the last m entries of e. Then d · A = e
                                                                        Similarly, we have that fl (xi )| ·A = s where l0 (xi ) = l(s+xi ).
  Proof: Upon initialization, I corresponds to the coefficients            Consider the vector w = fu (xi ) − fl (xi ). We know that
of the last m variables. Whenever a pivot operation is                  w| · A = r − s, and therefore:
             u(w| · A) = u(r − s)
                        = u(r + xi − s − xi )
                        ≤ u(r + xi ) − l(s + xi )
                        = u0 (xi ) − l0 (xi ) < 0
This means that for any assignment of V , the value of w| · A
is negative. In other words, we have proved that for all l ≤
V ≤ u, it hods that w| · A · V < 0, as needed.
 E. P ROOF PRODUCTION FOR R E LU BOUND TIGHTENING
                            RULES
   Here, we summarize some bound tightenings that can be
performed as a ReLU constraint f = ReLU (b), and which our
method currently supports. As before, we denote dynamically-
tightened bounds as l0 , u0 , and the ground bounds as l, u.
   As stated before, these tightenings can be introduced as
lemmas, or in some cases be derived as linear tightenings,
if appropriate equations have been added to the tableau (i.e.,
the equation f = b). Recall that:
                                  (
                                    b b>0
               f = ReLU(b) =
                                    0 otherwise.
  Therefore, the following tightenings can be performed (pro-
vided that they lead to tighter bounds than the ones presently
known):
      (i) For a positive l0 (f ), l0 (b) := l0 (f ).
      (ii) For a positive l0 (b), l0 (f ) := l0 (b).
      (iii) For any u0 (f ), u0 (b) := u0 (f ).
      (iv) For non-positive u0 (b), u0 (f ) := 0.
      (v) For a positive u0 (b), u0 (f ) := u0 (b).

     F. A NOTE ON MAINTAINING THE CORRECTNESS OF
                      FARKAS VECTORS
   It may not be immediately clear that updating a ground
bound of a variable x (e.g., as a result of case-splitting)
maintains the correctness of other variables’ Farkas vectors
that depend on the ground bounds of x. Since the Simplex
calculus allows ground bounds to only be tightened (i.e., lower
bounds to be increased, and upper bounds to be decreased),
the dynamically tightened bounds computed using the ground
bounds are tightened as well. This can be observed since a
dynamic upper bound is calculated using ground upper bounds
with positive coefficients, and ground lower bounds with
negative coefficients. Therefore, when ground lower bound
increases or ground upper bound decreases, any dynamic upper
bound computed using them decreases too. Increasing of a
dynamic lower bound follows similarly. We conclude that
using a Farkas vector to prove a bound, might lead to a tighter
bound than expected, but this does not harm soundness.
   For example, consider the case where the Farkas vector of
the upper bound of a variable y creates the row u0 (y) = u(x)−
l(z), and u(x) = 4, l(z) = 1, so u0 (y) = 3. If we tighten
u(x) := 2, then the Farkas vector of the upper bound of y
will prove the bound 1, which is tighter than 3.
