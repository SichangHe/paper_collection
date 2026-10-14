                                                 Solving non-linear Horn clauses using a linear solver

                                                                                         Bishoksan Kafle
                                                                                     Roskilde University, Denmark
                                                                                            kafle@ruc.dk


                                               Developing an efficient non-linear Horn clause solver is a challenging task since the solver has to
                                               reason about the tree structures rather than the linear ones as in a linear solver. In this paper we pro-
arXiv:1511.06668v1 [cs.LO] 20 Nov 2015




                                               pose an incremental approach to solving a set of non-linear Horn clauses using a linear Horn clause
                                               solver. We achieve this by interleaving a program transformation and a linear solver. The program
                                               transformation is based on the notion of tree dimension, which we apply to trees corresponding to
                                               Horn clause derivations. The dimension of a tree is a measure of its non-linearity – for example a
                                               linear tree (whose nodes have at most one child) has dimension zero while a complete binary tree has
                                               dimension equal to its height.
                                                    A given set of Horn clauses P can be transformed into a new set of clauses P≤k (whose derivation
                                               trees are the subset of P’s derivation trees with dimension at most k). We start by generating P≤k
                                               with k = 0, which is linear by definition, then pass it to a linear solver. If P≤k has a solution M, and
                                               is a solution to P then P has a solution M. If M is not a solution of P, we plugged M to P≤k+1 which
                                               again becomes linear and pass it to the solver and continue successively for increasing value of k
                                               until we find a solution to P or resources are exhausted. Experiment on some Horn clause verification
                                               benchmarks indicates that this is a promising approach for solving a set of non-linear Horn clauses
                                               using a linear solver. It indicates that many times a solution obtained for some under-approximation
                                               P≤k of P becomes a solution for P for a fairly small value of k.


                                         1    Introduction
                                         In this paper we propose an incremental approach to solving a set of non-linear Horn clauses using a
                                         linear Horn clause solver. The idea is similar in spirit to the bounded model checking with the following
                                         difference. On one hand, the under-approximation we generate is of bounded dimension (see definition
                                         4), which is not finitely nor precisely solvable. On the other hand, each such under-approximation is
                                         linear and the solver has to deal with only linear clauses each time. This is achieved by interleaving a
                                         program transformation and a linear solver. The program transformation is based on the notion of tree
                                         dimension, which we apply to trees corresponding to Horn clause derivations. The dimension of a tree
                                         is a measure of its non-linearity – for example a linear tree (whose nodes have at most one child) has
                                         dimension zero while a complete binary tree has dimension equal to its height.
                                             We say a set of Horn clause P (including integrity constraints) is solvable iff it has a model. Integrity
                                         constraints are special kind of Horn clauses with false head where false is always interpreted as false.
                                         A given set of Horn clauses P can be transformed into a new set of clauses P≤k (whose derivation trees
                                         are the subset of P’s derivation trees with dimension at most k). The predicates of P≤k are subset of
                                         predicates of P indexed from 0 to k. We start by generating P≤k with k = 0, which is linear by definition,
                                         then pass it to a linear solver. If P≤k has a solution M where M is a set of constrained fact of the form
                                         pindex (X) ← C (X) for each predicate pindex of P≤k . Let M 0 is M after removing index of predicates from
                                         each constraint fact in M. If M 0 is a solution to P then P has a solution M 0 . If M 0 is not a solution of P,
                                         we plugged M to P≤k+1 which again becomes linear and pass it to the solver and continue successively
                                         for increasing value of k until we find a solution to P or resources are exhausted.


                                         To appear in EPTCS.
2                                                        Solving non-linear Horn clauses using a linear solver

                       c1. fib(A, B):- A>=0, A=<1, B=A.
                       c2. fib(A, B) :- A > 1, A2 = A - 2, fib(A2, B2),
                                  A1 = A - 1, fib(A1, B1), B = B1 + B2.
                       c3. false:- A>5, fib(A,B), B<A.

                       Figure 1: Example CHCs Fib: it defines a Fibonacci function.

    Experiment on some Horn clause verification benchmarks indicates that this is a promising approach
for solving a set of non-linear Horn clauses. The program transformation allows one to use a linear solver
and solution from a previous iteration can be reused in the latter one. Many times a solution obtained for
some under-approximation P≤k becomes inductive, that is, a solution for P.
    To motivate readers, we present an example set of constrained Horn clauses (CHCs) P in Figure 1
which defines the Fibonacci function. This is an interesting problem whose dimension depends on the
input number and its computations are trees rather than linear sequences. The main contributions of this
paper are the following.
    1. We give an iterative algorithm for solving a set of non-linear Horn clauses using a linear solver
       (Section 3);
    2. We demonstrate the feasibility of our approach in practice applying it to non-linear Horn clause
       verification problems (Section 4);


2    Preliminaries
A constrained Horn clause is a first order formula of the form p(X) ← C , p1 (X1 ), . . . , pk (Xk ) (k ≥ 0)
(using Constraint Logic Programming (CLP) syntax), where C is a conjunction of constraints with re-
spect to some background theory, Xi , X are (possibly empty) vectors of distinct variables, p1 , . . . , pk , p
are predicate symbols, p(X) is the head of the clause and C , p1 (X1 ), . . . , pk (Xk ) is the body. A clause is
called non-linear if it contains more than one atom in the body (k > 1), otherwise it is called linear. A
set of Horn clauses P is called linear if P only contains linear clauses, otherwise it is called non-linear.
A set of Horn clauses is sometimes called a program.
Definition 1 (Solution of Horn clauses) Let P be a set of Horn claues and M a set of constrained fact
of the form p(X) ← C (X), where p(X) is a predicate in P and C (X) is an interpretation of p(X) under
some constraint theory. Then M is called a solution (model) of P if it satisfies each clause in P.
Definition 2 (Inductive solution of Horn clauses) Let Pu be an under-approximation of a set of Horn
clauses P. If a solution M of Pu is also a solution of P, then M is called an inductive solution of P. In
other words, a solution of a particular case (that is an under-approximation) of P becomes a solution of
P.
    A labeled tree c(t1 , . . . ,tk ) is a tree with its nodes labeled, where c is a node label and t1 , . . . ,tk are
labeled trees rooted at the children of the node and leaf nodes are denoted by c.
Definition 3 (Tree dimension (adapted from [4])) Given a labeled tree t = c(t1 , . . . ,tk ), the tree dimen-
sion of t represented as dim(t) is defined as follows:
                                    
                                    0
                                                               if k = 0
                    dim(t) = maxi∈[1..k] dim(ti )               if there is a unique maximum
                                    
                                       maxi∈[1..k] dim(ti ) + 1 otherwise
                                    
Kafle                                                                                                                  3


Figure 2 (a) shows a derivation tree t for Fibonacci number 3 and Figure 2 (b) shows its tree dimension.
It can be seen that dim(t) = 1. This number is a measure of its non-linearity, the smaller the number
the closer the tree is to a list. Since it is not a perfect binary tree, the height of t (3) is greater than its
dimension.




                    Figure 2: (a) derivation tree of Fibonacci 3 and (b) its tree dimension.

    To make the paper self contained, we describe our program transformation approach. Given a set of
CHCs P and k ∈ N, we split each predicate H occurring in P into the predicates H ≤d and H =d where
d ∈ {0, 1, . . . , k}. Here H ≤d and H =d generate trees of dimension at most d and exactly d respectively.

Definition 4 ( At-most-k-dimension program P≤k ) It consists of the following clauses (adapted from
[11, 10]):

   1. Linear clauses:
        If H ← C ∈ P , then H =0 ← C ∈ P≤k .
        If H ← C , B1 ∈ P then H =d ← C , B=d
                                           1 ∈P
                                                ≤k for 0 ≤ d ≤ k.


   2. Non-linear clauses:
        If H ← C , B1 , B2 , . . . , Br ∈ P with r > 1:
           • For 1 ≤ d ≤ k, and 1 ≤ j ≤ r:
                                     ≤d−1
             Set Z j = B=d
                        j and Zi = Bi      for 1 ≤ i ≤ r ∧ i 6= j. Then: H =d ← C , Z1 , . . . , Zr ∈ P≤k .
           • For 1 ≤ d ≤ k, and J ⊆ {1, . . . , r} with |J| = 2:
             Set Zi = B=d−1
                        i   if i ∈ J and Zi = B≤d−2i     if i ∈ {1, . . . , r} \ J. If all Zi are defined, i.e., d ≥ 2 if
             r > 2, then: H ← C , Z1 , . . . , Zr ∈ P≤k .
                           =d


   3. ε-clauses:
        H ≤d ← H =e ∈ P≤k for 0 ≤ d ≤ k , and every 0 ≤ e ≤ d.

    The at-most-0-dimension program of Fib in Figure 1 is depicted in Figure 3. In textual form we
represent a predicate p≤k by p[k] and a predicate p=k by p(k). Since some programs have derivation
trees of unbounded dimension, trying to verify a property for its increasing dimension separately is not a
practical strategy. It only becomes a viable approach if a solution of p≤k for some k ≥ 0 is inductive for
P (definition 2).
4                                                     Solving non-linear Horn clauses using a linear solver

                                   %linear clauses
                                   1. fib(0)(A,A) :- A>=0, A=<1.
                                   2. false(0) :- A>5, B<A, fib(0)(A,B).
                                   %epsilon-clauses
                                   3. false[0] :- false(0).
                                   4. fib[0](A,B) :- fib(0)(A,B).

                          Figure 3: Fib≤0 : at-most-0-dimension program of Fib.

3    Solving non-linear set of Horn clauses
A procedure for solving a set of non-linear Horn clauses using a linear solver is presented in Algorithm
1. The main procedure SOLVE(P) takes a set of non-linear Horn clause as input and outputs a solution
if they are solvable, unknown otherwise. A solution to a set of Horn clause P is an interpretation for
the predicates in P that satisfies each clauses in P. The procedure makes use of several sub-procedures
which will be descirbed next.
     KDIM(P,k) produces an at most k dimesional program P≤k (ref. definition 4). By defintion, P≤k is
linear for k = 0. For our example program presented in 1, the at-most-0-dimension program is shown
in Figure 3 and is linear since there is at most one non-constraint atom in the body of each clauses.
SOLVE LINEAR(P) is an oracle (a linear Horn clause solver) that returns a solution if P is solvable,
otherwise unsolvable. The oracle is sound, that is, if SOLVE LINEAR(P) returns a solution S then P is
solvable and S is a solution of P, if it returns unsolvable then P is unsolvable. In this paper, we make
use of a solver, which is based on abstract interpretation [1] over the domain of convex polyhedra [2].
The solver produces an over-approximation of minimal model of P as a set of constraints facts for each
predictes in P. In essence, any Horn clause solver can be used. This approximation is regarded as
a solution of the claues if there is no constrained fact for false in it. Using this solver, the following
solution is obtained for the program in Figure 3.
fib(0)(A,B) :- [-A>= -1,A>=0,B=1].
fib[0](A,B) :- [-A>= -1,A>=0,B=1].
    INDUCTIVE(M, P) checks if a given solution M is a solution of P. The predicates of P≤k are subset
of predicates of P indexed from 0 to k. If P≤k has a solution M where M is a set of constrained fact of the
form pindex (X) ← C (X) for each predicate pindex of P≤k . Let M 0 is M after removing index of predicates
from each constraint fact in M. If M 0 is a solution to P then P has a solution M 0 . If this is the case, then
INDUCTIVE(M, P) returns “yes” otherwise “no”. Given the above solution for at-most-0-dimension
program, we check if the following (M 0 )
fib(A,B) :- [-A>= -1,A>=0,B=1].
fib(A,B) :- [-A>= -1,A>=0,B=1].
is a solution to the program in Figure 1. We can see that it is not the case, since the clause c2 is not
satisfied under this solution. It should be noted that after removing the index from M to map the solution
to the original program, the resulting solution may be in disjunctive form, which allows a non-disjuntive
solver to produce a disjunctive solution. Thanks are due to our program transformation.
     The sub-procedure LINEARIZE(P, M) generates a linear set of clauses from P and a set of solution
M. Given M as a set of constrained facts of the form p(X) ← C , the procedure involves in replacing
every predicate p(X) in P with C . This produces a linear set of clauses under the following condition,
which is captured by the following lemma 1.
Kafle                                                                                                     5


Lemma 1 (Linearisation) If S is a solution computed for a at-most-k-dimension program (k ≥ 0) and
P is a at-most-(k+1)-dimension program, then the procedure LINEARIZE(P, S) returns a set of linear
clauses.
     An excerpt from a 1-dimension program of our program in Figure 1 is shown below.
false(1) :- A>5, B<A, fib(1)(A,B).
fib(1)(A,B) :- A>1, C=A-2, E=A-1, B=F+D,                        fib(1)(C,D),          fib[0](E,F).
    After plugging in the solution obtained for at-most-0-dimension program, we obtain the following
set of clauses (after constraints simplification), which are now linear since the body atom fib[0](E,F)
in the second clause is replaced by its solution.
false(1) :- A>5, B<A, fib(1)(A,B).
fib(1)(A,B) :- -A>= -2, A>1, A-C=2, B-D=1, fib(1)(C,D).
    Continuing to run our algorithm, the following solution obtained for a 2-dimension program becomes
an inductive solution for the program in Figure 1 and the algorithm terminates.

fib(0)(A,B) :- [-A>= -1,A>=0,B=1].
fib[0](A,B) :- [-A>= -1,A>=0,B=1].
fib(1)(A,B) :- [A>=2,A+ -B=0].
fib[1](A,B) :- [A+ -B>= -1,B>=1,-A+B>=0].
fib(2)(A,B) :- [A>=4,-2*A+B>= -3].
fib[2](A,B) :- [A>=0,B>=1,-A+B>=0].

    The soundness of the algorithm 1 is captured by the following 1 proposition.
Proposition 1 (Soundness of algorithm 1 ) If Algorithm 1 returns a solution S for a set of clauses P
then P is solved and S is in fact a solution of P.


4     Experimental results
We implemented our algorithm in the tool called LHornSolver, which is freely available at https:
//github.com/bishoksan/LHornSolver. Then we carried out an experiment on a set of 9 non-linear
CHC verification problems taken from the repository1 of software verification benchmarks. Our aim in
the current paper is not to make a systematic comparison with other verification techniques; these are
exploratory experiments whether using a linear solver for non-linear problem solving is practical if at all.
The results are summarized in Table 1.
    In the table Program represents a program, Result- represents a verification result using our ap-
proach, Time- is a time to solve the program and k represents a value for which a solution of a at-most-k-
dimension program (under-approximation) of a set of clauses P becomes inductive for P.
    Our current approach solves 9 out of 9 problems with an average time of 2000 milliseconds. These
examples were also run on QARMC [6] which solves all the problems ( and much faster).
    In most of these problems, a solution of an under approximation (at-most-k-dimension program) be-
comes a solution for the original one when k = 1. This shows that a solution for an under-approximation
(k-dimension program) becomes inductive for a fairly small value of k, and demostrates the feasibility of
solving a set of non-linear Horn clauses using a linear solver.
    1 https://svn.sosy-lab.org/software/sv-benchmarks/trunk/clauses/LIA/Eldarica/RECUR/
6                                                   Solving non-linear Horn clauses using a linear solver


    Algorithm 1: Algorithm for solving a set of Horn clauses
    1 Procedure SOLVE (P)
   Input: Set of CHCs P
   Output: (solved, solution), unknown
 2 initialization: k ← 0
 3 P0 ← KDIM(P, k) (Definition 4)
 4 while true do
 5      (rk , Sk ) ← SOLVE LINEAR(P0 )
 6      if rk 6= solved then
 7            return unknown
 8      end
 9      b ← INDUCTIVE(Sk , P)
10      if b = yes then
11            return (solved, Sk )
12      end
13      Pk+1 ← KDIM(P, k + 1) (Definition 4)
14      PLk+1 ← LINEARIZE(Pk+1 , Sk )
15      k ← k + 1 ; P0 ← PLk+1
16 end




5     Related Work

There exists several Horn clause solvers [7, 5, 12, 8, 9] which handle non-linear clauses. However some
tools, for example [3], tackle non-linear clauses by linearising them first and using a linear solver. The
generality of the tool such as [3] depends on the class of clauses that are linearisable and it is still not
clear which classes of clauses are linearisable and under which conditions. But our approach handles any
non-linear clauses and solves them using a linear solver. To the best our knowledge, this is something
new.



6     Conclusion and future work

We presented an incremental approach to solving a set of non-linear Horn clauses using a linear Horn
clause solver. We presented an algorithm based on this idea which yielded preliminary results on set of
non-linear Horn clause verification benchmarks, showing that the approach is feasible.



Acknowledgement

The research leading to these results has received funding from the EU 7th Framework 318337, ENTRA-
Whole-Systems Energy Transparency. The author would like to thank John P. Gallagher and Pierre Ganty
for several discussions, suggestions and comments on the earlier version of this paper.
Kafle                                                                                                             7


                  Table 1: Experimental results on non-linear CHC verification problems
                                 Program          Result Time(ms) k
                                 addition         safe     4000        1
                                 bfprt            safe     2000        2
                                 binarysearch     safe     2000        1
                                 countZero        safe     2000        1
                                 identity         safe     2000        1
                                 merge            safe     2000        1
                                 palindrome       safe     1000        1
                                 fib              safe     2000        2
                                 revlen           safe     1000        1
                                 avg. time(ms)             2000


References
 [1] P. Cousot and R. Cousot. Abstract interpretation: A unified lattice model for static analysis of programs by
     construction or approximation of fixpoints. In R. M. Graham, M. A. Harrison, and R. Sethi, editors, POPL,
     pages 238–252. ACM, 1977.
 [2] P. Cousot and N. Halbwachs. Automatic discovery of linear restraints among variables of a program. In
     Proceedings of the 5th Annual ACM Symposium on Principles of Programming Languages, pages 84–96,
     1978.
 [3] E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. Verimap: A tool for verifying programs through
     transformations. In E. Ábrahám and K. Havelund, editors, TACAS, volume 8413 of LNCS, pages 568–574.
     Springer, 2014.
 [4] J. Esparza, S. Kiefer, and M. Luttenberger. On fixed point equations over commutative semirings. In STACS
     2007, 24th Annual Symposium on Theoretical Aspects of Computer Science, Proceedings, volume 4393 of
     LNCS, pages 296–307. Springer, 2007.
 [5] S. Grebenshchikov, A. Gupta, N. P. Lopes, C. Popeea, and A. Rybalchenko. Hsf(c): A software verifier based
     on Horn clauses - (competition contribution). In C. Flanagan and B. König, editors, TACAS, volume 7214 of
     LNCS, pages 549–551. Springer, 2012.
 [6] S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko. Synthesizing software verifiers from proof
     rules. In J. Vitek, H. Lin, and F. Tip, editors, ACM SIGPLAN Conference on Programming Language Design
     and Implementation, PLDI ’12, Beijing, China - June 11 - 16, 2012, pages 405–416. ACM, 2012.
 [7] A. Gurfinkel, T. Kahsai, and J. A. Navas. Seahorn: A framework for verifying C programs (competition
     contribution). In C. Baier and C. Tinelli, editors, Tools and Algorithms for the Construction and Analysis of
     Systems - 21st International Conference, TACAS 2015, Held as Part of the European Joint Conferences on
     Theory and Practice of Software, ETAPS 2015, London, UK, April 11-18, 2015. Proceedings, volume 9035
     of Lecture Notes in Computer Science, pages 447–450. Springer, 2015.
 [8] K. S. Henriksen, G. Banda, and J. P. Gallagher. Experiments with a convex polyhedral analysis tool for logic
     programs. In Workshop on Logic Programming Environments, Porto, 2007, 2007.
 [9] B. Kafle and J. P. Gallagher. Tree automata-based refinement with application to horn clause verification.
     In D. D’Souza, A. Lal, and K. G. Larsen, editors, Verification, Model Checking, and Abstract Interpretation
     - 16th International Conference, VMCAI 2015, Mumbai, India, January 12-14, 2015. Proceedings, volume
     8931 of Lecture Notes in Computer Science, pages 209–226. Springer, 2015.
[10] B. Kafle, J. P. Gallagher, and P. Ganty. Decomposition by tree dimension in horn clause verification. In press,
     2015.
8                                                      Solving non-linear Horn clauses using a linear solver


[11] M. Luttenberger. An extension of parikh’s theorem beyond idempotence. CoRR, abs/1112.2864, 2011.
[12] P. Rümmer, H. Hojjat, and V. Kuncak. Disjunctive interpolants for Horn-clause verification. In N. Sharygina
     and H. Veith, editors, CAV, volume 8044 of Lecture Notes in Computer Science, pages 347–363. Springer,
     2013.
