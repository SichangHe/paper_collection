                                                        Algorithms and Complexity of Difference Logic∗
                                          Konrad K. Dabrowski†                   Peter Jonsson‡            Sebastian Ordyniak§                 George Osipov¶
                                                                                           February 6, 2024
arXiv:2402.03273v1 [cs.DS] 5 Feb 2024




                                                                                                 Abstract
                                                  Difference Logic (DL) is a fragment of linear arithmetics where atoms are constraints x + k ≤
                                              y for variables x, y (ranging over Q or Z) and integer k. We study the complexity of deciding
                                              the truth of existential DL sentences. This problem appears in many contexts: examples include
                                              verification, bioinformatics, telecommunications, and spatio-temporal reasoning in AI. We begin by
                                              considering sentences in CNF with rational-valued variables. We restrict the allowed clauses via two
                                              natural parameters: arity and coefficient bounds. The problem is NP-hard for most choices of these
                                              parameters. As a response to this, we refine our understanding by analyzing the time complexity and
                                              the parameterized complexity (with respect to well-studied parameters such as primal and incidence
                                              treewidth). We obtain a comprehensive picture of the complexity landscape in both cases. Finally,
                                              we generalize our results to integer domains and sentences that are not in CNF.


                                        Keywords: Diﬀerence Logic, Algorithms and Complexity, Fine-grained Complexity, Parameterized
                                        Complexity, Treewidth.




                                           ∗ This article improves and extends results from two conference papers [25, 26]. For the purpose of open access, the authors

                                        have applied a Creative Commons Attribution (CC BY) licence to any Author Accepted Manuscript version arising.
                                           † School of Computing, Newcastle University, UK, konrad.dabrowski@newcastle.ac.uk
                                           ‡ Department of Computer and Information Science, Linköping University, Sweden, peter.jonsson@liu.se
                                           § School of Computing, University of Leeds, UK, sordyniak@gmail.com
                                          ¶ Department of Computer and Information Science, Linköping University, Sweden, george.osipov@pm.me




                                                                                                      1
Contents
1 Introduction                                                                                               3
  1.1 Background . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     3
  1.2 Time Complexity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      5
  1.3 Parameterized Complexity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       7
  1.4 Outline . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    9

2 Preliminaries                                                                                               9
  2.1 Diﬀerence Logic . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    10
  2.2 Constraint Satisfaction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    10
  2.3 Sidon Sets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   12

3 Upper Bounds on Time Complexity                                                                            12
  3.1 Upper Bound for CSP(D) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         12
  3.2 Upper Bound for CSP(D2,k ) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         14
      3.2.1 Certiﬁcates . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      15
      3.2.2 Instances with Bounded Span . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          15
      3.2.3 Divide-and-Conquer Strategy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          16

4 Lower Bounds on Time Complexity                                                                            20

5 Parameterized Upper Bounds                                                                                 24
  5.1 Treewidth . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    24
  5.2 XP Algorithm for CSP(D∞,k ) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        26

6 Parameterized Lower Bounds                                                                                 30
  6.1 pNP-hardness for CSP(D2,∞ ) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        30
  6.2 W[1]-hardness for Multi-Dimensional Partitioned Subset Sum . . . . . . . . . . . .                     31
  6.3 W[1]-hardness for CSP(D2,1 ) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       32

7 Generalizations                                                                                            39
  7.1 General Formulas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     39
  7.2 Integer Domains . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      40

8 Conclusion and Future Work                                                                                 41




                                                       2
1     Introduction
We have divided this introductory section into four parts. In the ﬁrst one (Section 1.1), we present diﬀer-
ence logic (DL) and some of its applications, and we describe our approach for studying the complexity
of DL. In short, the satisﬁability problem for DL is almost always NP-hard and a more ﬁne-grained anal-
ysis becomes necessary; we will thus study the time complexity of DL together with its parameterized
complexity under natural structural parameters. Our time complexity results are discussed in Section 1.2
while our parameterized results are discussed in Section 1.3. Finally, an outline of the article is given in
Section 1.4.

1.1    Background
Difference Logic is a fragment of linear arithmetics where atoms are constraints of the form x + k ≤ y for
variables x, y (with some numeric domain such as Q or Z) and some integer k. The satisfiability problem
for DL is the computational problem of deciding the truth of sentences

                                                ∃x1 , . . . , xn .φ

where φ is a quantiﬁer-free formula over variable set {x1 , . . . , xn }. The satisﬁablity problem for conjunc-
tions of diﬀerence atoms is solvable in polynomial time (by, for instance, the Floyd-Warshall algorithm),
while adding various logical features often leads to computational hardness. We note, for instance, that the
satisﬁability problem is NP-hard (since the satisﬁability problem for propositional logic is NP-hard [22])
and that the problem of deciding the truth of an arbitrary formula is PSPACE-hard (since deciding the
truth of quantiﬁed propositional formulas is PSPACE-hard [76]). These complexity results hold both for
rational and integer variable domains. DL is a well-studied formalism due to its many applications: the
archetypal example is from veriﬁcation where timed automata have natural connections with DL [3, 58].
Other important applications include the channel assignment problem (which is a central problem in
telecommunications [5, 54]), unit interval problems (with applications in bioinformatics and graph the-
ory [39, 65]), and problems in connection with answer set programming [55, 60]—all of these can be
viewed as restricted variants of DL. Applications like these and the relative simplicity of DL have made it
into one of the most ubiquitous theories in the context of satisfiability modulo theories (SMT) [7, 20, 61].
DL is also interesting from a complexity-theoretic point of view. One example is the max-atom problem
(see the paper by Bezem et al. [9] or Section 6 in [15]) that can be viewed as a severely restricted version
of DL. This problem is polynomial-time equivalent to problems such as mean pay-oﬀ games, scheduling
under and-or precedence constraints, and ﬁnding solutions to certain classes of equations. The max-atom
problem is intriguing since it is known to be in NP ∩ coNP but no polynomial-time algorithm has yet
been identiﬁed.
    DL is of major importance in AI but the connections are in general not clearly spelled out in the liter-
ature. Spatial-temporal reasoning is a fundamental task in AI and one of the most inﬂuential formalisms
is the simple temporal problem (STP) that was ﬁrst proposed in an AI context by Dechter et al. [28]. It
is a constraint satisfaction problem (CSP) over a constraint language with relations

                                        {(x, y) ∈ Q2 : x − y ∈ [l, u]}

where ℓ, u ∈ Q ∪ {−∞, +∞} and [ℓ, u] denotes a closed interval. We refer to constraints using such
relations as simple constraints. The close relationship to DL is obvious. The STP formalism is often
generalized so that the intervals may be half-closed, open, or a single point. Dechter et al. [28, Sec.
7] point out that this generalization apparently do not have any adverse eﬀects and, in particular, the
resulting CSP is still solvable in polynomial time. Even though STPs have proven to be immensely useful
in AI, their expressive power is limited. Thus, a common way of obtaining increased expressibility is
to introduce disjunctions in various ways [6, 28, 63, 75]. From the DL perspective, this is equivalent to
considering DL formulas on conjunctive normal form and restricting the set of allowed clauses in various
ways. The resulting formalisms are highly relevant in an AI context. Well-known examples can be found
in automated planning [38, 79] and multi-agent systems [10, 18]. Stergiou & Koubarakis [75, Sec. 7],


                                                        3
Tsamardinos & Pollack [78] and Peintner et al. [66] discuss various other applications, and Zavatteri et
al. [82] have recently presented a large-scale evaluation of software for solving DTPs.
    We traditionally view a computational problem as intractable if it is NP-hard. NP-hardness rules out
polynomial-time algorithms (assuming P 6= NP), but it does not say anything about the time complexity
of the best possible algorithm. Recent advances in complexity theory allow us to prove conditional lower
bounds via restricted reductions from complexity-theoretic conjectures that are stronger than the P 6=
NP conjecture. This methodology has enabled proving close-to-optimal bounds on time complexity for a
multitude of problems assuming suitable conjectures, cf. the textbook by Gaspers [37]. The goal of this
article is to analyze the satisﬁability problem for DL following this methodology. Our time complexity
results reveal that many severely restricted variants of DL cannot be solved in a reasonable amount of
time under the Exponential-Time Hypothesis (ETH). This computational hardness makes it worthwhile
to use parameterized complexity for analyzing DL with restricted interactions between variables and
constraints.
    We need some deﬁnitions and notation to facilitate the discussion of the problems that we will study.
In the sequel, we restrict ourselves to the satisﬁability problem for DL over rational numbers where
the input is in CNF, and we study various ways of restricting the allowed clauses. We will return to DL
without these restrictions in Section 7. The restriction to CNF formulas allows us to view the satisﬁability
problem for DL as a constraint satisfaction problem where the constraint language correspond to the
allowed clauses. Our clause restrictions will be based on two parameters: arity and coefficient bounds.
The arity bounds the number of distinct variables that may appear in a clause. It is closely connected to
the length of a clause, i.e. the maximum number of literals, since if a clause has length k, then its arity
is at most 2k. The coeﬃcient bound simply equals the maximum over the absolute values of constants
appearing in clauses.
    We continue by introducing the maximally expressive constraint language D. We consider intervals
over Q with endpoints in Z ∪ {−∞, +∞}. The intervals may be open, closed, half-closed, or a single
point. Let I denote the set of these intervals and let D contain all relations
                                                            Wm
                                  {(x1 , . . . , xt ) ∈ Qt : ℓ=1 xiℓ − xjℓ ∈ Iℓ }
for arbitrary t, m ≥ 1 where iℓ , jℓ ∈ {1, . . . , t} and Iℓ ∈ I for all 1 ≤ ℓ ≤ m. We remark that one may
equally well use the reals instead of the rationals as the underlying domain. The CSP for D is known
as the disjunctive temporal problem (DTP) in the AI literature. It is easy to verify that CSP(D) is in
NP since the STP is solvable in polynomial time. Given a relation R ∈ D, let K(R) denote the set of
numerical bounds appearing in R, e.g. for
                        R = {(x, y, z) ∈ Q3 : (−∞ < x − y ≤ 3) ∨ (0 ≤ x − z < 6)}

S have K(R) = {3, 0, 6}. If X is a set of relations, then the deﬁnition of K extends naturally: K(X) =
we
  R∈X K(R). Let A ⊆ D and deﬁne num(A) = max{|a| : a ∈ K(A)}, i.e. num(A) is the least upper
bound on absolute values of all numerical bounds appearing in the relations of A. We let Da,k (where
a, k ∈ N ∪ {∞}) denote the class of relations of arity at most a and with num(Da,k ) ≤ k.
    We illustrate the basic deﬁnitions with an example: consider Allen’s interval algebra [2] restricted so
that the intervals are only allowed to have unit length. This formalism (which is referred to as the unit
Allen algebra) has, for example, applications in bioinformatics and graph theory [39, 65]. Given a closed
interval I, we let I − and I + denote the left and the right endpoint, respectively. We let Aua denote a
binary structure based on the following relations:
                    I{p}J       I precedes J       I+ < J−
                    I{m}J       I meets J          I+ = J−
                    I{o}J       I overlaps J       I − < J − and J − < I + and I + < J +
                    I{e}J       I equals J         I − = J − and I + = J +
Note that relations p, m, o admit converses p−1 , m−1 , o−1 while the relation e is symmetric. We let the
structure Aua contain every disjunction of the basicW relations. Formally, let U denote the set of all unit in-
tervals on the real line. Aua contains {(I, J) ∈ U2 : r∈S I{r}J} for every S ⊆ {p, m, o, e, o−1 , m−1 , p−1 }.

                                                      4
                                      k=0           1≤k<∞           k unbounded
                           a=2         ∈P          NP-complete      NP-complete
                           a≥3     NP-complete     NP-complete      NP-complete

                  Table 1: Summary of computational complexity landscape for CSP(Da,k ).


Observe that every basic relation in the unit Allen algebra can be expressed as a simple relation in D2,1
over the left endpoints of the intervals, i.e.

                                  I{p}J     ⇐⇒      I − − J − ∈ (−∞, −1),
                                 I{m}J      ⇐⇒      I − − J − ∈ {−1},
                                  I{o}J     ⇐⇒      I − − J − ∈ (−1, 0),
                                  I{e}J     ⇐⇒      I − − J − ∈ {0},

and similarly for the converse relations. Moreover, every simple relation in D2,1 can be expressed as a
basic relation of the unit Allen algebra since the correspondence is one to one. This reasoning naturally
extends to taking disjunctions of simple/basic relations. Thus, CSP(Aua ) and CSP(D2,1 ) are the same
computational problem, and any upper/lower bound that applies to one of the problems also applied to
the other.
    Let us now summarize the computational complexity of CSP(Da,k ). The polynomial-time solvability
of CSP(D2,0 ) follows from the fact that the relations in D2,0 equal the point algebra [80]. It is well known
that CSP(Dk,0 ) for k ≥ 3 is NP-hard (this follows, for instance, from an easy reduction from the Be-
tweenness problem [36]). Finally, CSP(D2,1 ) (and thus CSP(Aua )) are NP-hard via a straightforward
reduction from 3-Colourability; NP-hardness for CSP(D2,k ), k > 1, is a direct consequence. These
results are presented in Table 1—we immediately see that there is an conspicuous lack of polynomial-time
solvable cases. In the rest of this article, we will reﬁne our understanding of the complexity of CSP(Da,k )
by ﬁrst analyzing its time complexity and continue with its parameterized complexity. We discuss these
results in Sections 1.2 and 1.3, respectively.

1.2    Time Complexity
We prove the following results concerning the time complexity of DTPs. Our lower bounds are based on
the Exponential Time Hypothesis (ETH) by Impagliazzo et al. [46], i.e. the 3-Satisfiability problem
cannot be solved in 2o(n) time, where n is the number of variables. We let D≤
                                                                            a,k denote the subset of Da,k
where the relations are deﬁned by only using closed intervals.
  1. CSP(D) is solvable in 2O(n(log n+log k)) time (Corollary 7).
  2. CSP(D2,k ) is solvable in 2O(n log log n) time (Theorem 13).

  3. CSP(D4,0 ) and CSP(D≤
                         3,1 ) are not solvable in 2
                                                     o(n log n)
                                                                time (Theorems 15 and 16).

  4. CSP(D≤
          2,∞ ) is not solvable in 2
                                     o(n(log n+log k))
                                                       time (Theorem 17).

  5. For every c > 1, there exist k ≥ 0 and A ⊆ D≤                                           n
                                                 2,k such that CSP(A) cannot be solved in O(c ) time
     (Theorem 19).
   We additionally use a result by Eriksson and Lagerkvist [31, Section 3].
Theorem 1 ([31]). CSP(D3,0 ) is solvable in 2O(n) but not in 2o(n) time (if the ETH is true).
    The results are summarized in Table 2 and we see that the upper and lower bounds are reasonably
close. The lower bounds hold for constraint languages that do not use strict inequalities except for
CSP(Da,0 ), a ≥ 2; an instance of CSP(D≤  a,0 ) is always satisﬁable by assigning each variable value 0.



                                                     5
The results concerning CSP(D2,k ) indicates that there is no uniform single-exponential algorithm for
CSP(D2,k ). The result does not, however, rule out the possibility that CSP(D2,k ) can be solved in 2ck ·n
time, where c1 , c2 , . . . is an increasing sequence. All results in Table 2 remain intact if we restrict the
variables to take integer values only (see Section 7.2). We remark that our main goal is in delineating
single-exponential vs super-exponential running times, for which the ETH is a reasonable starting point.
To obtain more ﬁne-grained lower bounds, e.g. rule out concrete constants in the bases of exponential
functions, one typically needs to rely on stronger hypotheses like the strong ETH [19].
    Our algorithm for CSP(D) is based on proving a small solution property: every satisﬁable instance
of CSP(D) has a solution that assigns suﬃciently small values to the variables. The small solution
property is not very common in inﬁnite-domain CSPs but it is, for instance, known to hold for the
max-atom problem [9] and the CSP problem for unit two variables per inequality relations [72]. Our
proof utilizes certain ordering properties inherent in D together with a method for handling the integer
and fractional part of the variables independently; this approach is distinctly diﬀerent compared to the
proof techniques used in [9] and [72]. With the aid of this result, we can enumerate a suitable collection
of assignments and check whether at least one of them satisﬁes all constraints in the instance. The
small solution property will be important once again when we consider the parameterized setting (see
Section 1.3). Our algorithm for CSP(D2,k ) is based on a non-trivial divide-and-conquer approach. The
relations in D2,k exhibit even stronger ordering properties than the relations in D and this allows us to
show that any solution for an instance I of CSP(D2,k ) suggests a natural split of the whole instance
into either two or three subinstances sharing only a small number of variables. Hence, our algorithm
enumerates all possible decompositions into two or three subinstances with small variable overlap and
recurses on those for every possible assignment of the shared variables. An immediate consequence of this
algorithm is the following result (since CSP(Aua ) and CSP(D2,1 ) are the same computational problem).
Proposition 2. CSP(Aua ) is solvable in 2O(n log log n) time.

    Our lower bounds are based on a mixture of related ideas. We exploit the lower bound on the (k × k)-
Independent Set problem by Lokshtanov, Marx and Saurabh [56], and the lower bound by Traxler [77].
The latter result concerns binary CSPs over ﬁnite domains, where the complexity is measured with
respect to the number of variables. Intuitively, Traxler shows that, under the ETH, the complexity of
binary CSPs grows together with the domain size. We illustrate the main technical idea by an example.
Suppose an instance of a CSP over the domain {1, 2, 3} has two variables v1 , v2 and two unary constraints:
v1 ∈ {1, 2} and v2 ∈ {2, 3}. One can reduce it to a CSP over the domain {1, 2, 3}2 with a single constraint
v ∈ {1, 2} × {2, 3}, where {1, 2} × {2, 3} = {(1, 2), (1, 3), (2, 2), (2, 3)}. Here variable v encodes the pair of
variables (v1 , v2 ). Applying the same idea, one can reduce any instance of binary CSP over domain d with
n variables to a binary CSP over domain dr with roughly n/r variables, for any constant r. Thus, with
increased domain size, the number of variables required to encode the same set of constraints decreases.
Lokshtanov et al. push this idea to the limit, where the domain size and the number of variables are
roughly equal. A helpful technical tool that we use in adapting these results to CSP(Da,k ) are Sidon
sets. A set S of natural numbers is called a Sidon set if all pairwise sums of its elements are distinct, i.e.
the equation a + b = c + d with a, b, c, d ∈ S is only solvable when {a, b} = {c, d}. Sidon sets are also
used in our lower bound proofs in the parameterized case.
    We conclude this section with a few words about related problems from the literature. The CSP(D)
problem can be expressed in the existential theory of the reals (∃R). An ∃R-formula is a Boolean
combination of atomic predicates of the form p(x1 , . . . , xn ) ⊙ 0, where p is a real polynomial and
⊙ ∈ {<, ≤, =, ≥, >, 6=}. Renegar’s algorithm [68] decides the satisﬁability problem for ∃R-formulas
in L log L log log L · (md)O(n) time where L is the number of bits needed to represent the coeﬃcients in
the polynomials, m is the number of polynomials in the sentence, d is maximum among total degrees of
the polynomials, and n is the number of variables. Observe that instances of CSP(D) can be written as
∃R-formulas by replacing atomic formulas of the form x− y ≤ a with p(x, y) ≤ 0 where p(x, y) = x− y − a.
An instance    I of CSP(D) with n variables and k = num(I) can have O(n2 k) atomic formulas: there
      n
       
are 2 pairs of variables and O(k) possible bounds can be expressed on their diﬀerence. We are allowed
to use disjunctions, which can be applied to an arbitrary subset of the O(n2 k) atomic formulas. Thus,


                                                        6
                      Upper bounds            k=0         1≤k<∞             k unbounded
                          a=2                  ∈P        2O(n log log n)   2O(n(log n+log k))

                          a=3                 2O(n)       2O(n log n)      2O(n(log n+log k))
                          a≥4              2O(n log n)    2O(n log n)      2O(n(log n+log k))
                      Lower bounds           k=0          1≤k<∞              k unbounded
                          a=2                  −              (∗)          2o(n(log n+log k))
                          a=3                2o(n)         2o(n log n)     2o(n(log n+log k))
                          a≥4              2o(n log n)     2o(n log n)     2o(n(log n+log k))

Table 2: Summary of time complexity landscape for CSP(Da,k ). (∗) means that for every c > 1, there exists
k ≥ 0 and A ⊆ D2,k such that CSP(A) cannot be solved in O(cn ) time.

                                          2                                                            3
cast as a ∃R-formula, I has m ≤ 2O(n k) polynomials of degree d = 1. This leads to a 2O(n k) -time
                                                  3
algorithm for CSP(D) and, consequently, 2O(n ) time for CSP(D∞,k ). For binary constraint languages,
Renegar’s algorithm yields better results with 2O(n(log n+log k)) time for CSP(D2,∞ ) and 2O(n log n) time
for CSP(D2,k ) because only O(n2 k) disjunctive formulas are available. In fact, the running time for
CSP(D2,∞ ) obtained this way matches our result. However, we claim that our algorithm represents a
very simple and natural approach to solving this problem. While asymptotically the result are the same,
Renegar’s algorithm solves a much more general problem, and the hidden constants in its running time
are astronomical (see e.g. the practical evaluation in [44]).
    Let us turn our attention to lower bounds. Socała [74] shows that the channel assignment problem
cannot be solved in 2o(n log n) time under the ETH. This problem can be viewed as CSP(Aca ) where Aca
contains the relation {(x, y) ∈ N2 : |x − y| ≥ a} for every a ∈ N. This result implies that CSP(D≤         2,∞ )
is not solvable in 2o(n log n) time but it does not directly imply our stronger 2o(n(log n+log k)) lower bound
for integer solutions (that is derived by combining Theorem 17 and Lemma 37). Unit two variables per
inequality (UTVPI) relations are deﬁned as {(x, y) ∈ Z2 : ax + by ≥ c} where a, b ∈ {−1, 0, 1} and c ∈ Z.
This is a well-studied and interesting generalization of CSP(D≤   2,∞ ) over the integers; Schutt and Stuckey
write the following [71, p. 514].
          Unit two-variable-per-inequality (UTVPI) constraints form one of the largest class of in-
      teger constraints which are polynomial time solvable (unless P = NP). There is considerable
      interest in their use for constraint solving, abstract interpretation, spatial databases, and
      theorem proving.
Seshia et al. [72] have presented an algorithm for checking the satisﬁability of ﬁrst-order formulas without
universal quantiﬁcation over UTVPI constraints. This algorithm runs in 2O(n(log n+log k)) time (where, as
usual, n is the number of variables and k is the coeﬃcient bound). Our lower bound result for CSP(D≤    2,∞ )
over the integers shows that this algorithm is essentially optimal with respect to running time.

1.3    Parameterized Complexity
We have seen that CSP(D) (and many severely restricted variants) cannot be solved in single-exponential
time under the Exponential-Time Hypothesis (ETH). This motivates the search for eﬃciently solvable
subproblems. To this end, we use the framework of parameterized complexity [29, 32, 59], where the run-
time of an algorithm is studied with respect to a parameter p ∈ N and the input size n. The idea is that
the parameter describes the structure of the instance in a computationally meaningful way. Here, the
most favorable complexity class is FPT (fixed-parameter tractable), which contains all problems that can
be decided in f (p) · nO(1) time, where f is a computable function. The next best option is the complexity
class XP, which contains all problems decidable in nf (p) time, i.e. the problems solvable in polynomial
time when the parameter p is bounded. Clearly, FPT ⊆ XP and this inclusion is strict (see e.g. [32, Cor.
2.26]). It is signiﬁcantly better if a problem is in FPT than in XP since the order of the polynomial factor
in the former case does not depend on the parameter p. Finally, the class pNP contains all problems that


                                                         7
can be decided in f (p) · nO(1) time by a non-deterministic algorithm for some computable function f . It
is known that a problem is pNP-hard (under fpt-reductions; see Sec 6) if it is NP-hard for some constant
value of the parameter. Problems that are pNP-hard are considered to be signiﬁcantly harder than those
in XP since a problem that is pNP-hard cannot be in XP unless P = NP.
    A prominent method for identifying tractable fragments of CSPs is to restrict variable-constraint
interactions (see, for instance, the survey by Carbonnel and Cooper [21, Sec. 5]); these are referred to
as structural restrictions and are commonly studied via the primal and incidence graphs associated with
instances of the CSP. The primal graph has the variables as its vertices with any two joined by an edge
if they occur together in a constraint. The incidence graph is the bipartite graph with two disjoint sets
of vertices corresponding to the variables and the constraints, respectively. A constraint vertex and a
variable vertex are joined by an edge if the variable occurs in the scope of the constraint. The treewidth
of such graphs has been used extensively. It is, for example, known that the ﬁnite-domain CSP is in FPT
with the parameter w + d if w is the primal treewidth and d is the domain size [41], while this is not true
(under standard complexity assumptions) if w is the incidence treewidth [70].
    We now describe our parameterized results. It is known that the primal treewidth is bounded from
below by the incidence treewidth [52] for arbitrary CSP instances. Thus, we present algorithms for
CSP(Da,k ) parameterized by incidence treewidth and lower bounds with respect to primal treewidth.
We exhibit an XP algorithm for CSP(D∞,k ) when k ∈ N. This is a bottom-up dynamic programming
algorithm along a nice tree-decomposition of the incidence graph that exploits the fact that CSP(D)
has the small solution property. The algorithm runs in time (nk)O(w) where w is the treewidth of the
incidence graph. One may note that CSP(D) is in XP whenever the numeric values occurring in the
instance are bounded by a polynomial in the number of variables.
    We complement this algorithmic result by proving that CSP(D2,k ) for 1 ≤ k < ∞ is W[1]-hard when
parameterized by primal treewidth and thus not in FPT under standard complexity-theoretic assumptions.
This shows that signiﬁcantly faster algorithms for CSP(Da,k ) with k < ∞ are unlikely. This W[1]-
hardness result carries over to CSP(D≤  a,k ) when k ≥ 1 almost without extra eﬀort; note that the condition
                               ≤
on k is required since CSP(Da,0 ) is trivially in P. The reduction is from a novel multi-dimensional variant
of the well-known Subset Sum problem, which we show to be W[1]-hard. Many important problems from
the AI literature such as Allen’s Algebra and RCC8 are in FPT [27] so even CSP(D2,1 ) is a substantially
harder problem. We ﬁnally show that CSP(D2,∞ ) is pNP-hard, i.e. the problem becomes much harder
when the numeric values are unbounded. If a language L is in NP, then all parameterized languages
L′ ⊆ L × N are members of pNP so CSP(D2,∞ ) is a pNP-complete problem. We summarize our results
in Table 3. All results for k ≥ 1 can be found in this article, while the result for k = 0 was proven
by Dabrowski et al. [27]. We note that the results still hold if we restrict ourselves to integer variable
domains (see Corollary 34 and Section 7.2). The results outlined above immediately implies the following
since CSP(Aua ) and CSP(D2,1 ) are the same computational problem.
Proposition 3. CSP(Aua ) with parameter treewidth of incidence graph is in XP and it is W[1]-hard
with parameter treewidth of primal graph.

    We conclude this section by discussing some related algorithms from the literature. Bodirsky &
Dalmau [13] and Huang et al. [45] proved that CSP(A) is in XP (with treewidth of the primal graph
as parameter) for ω-categorical A and binary constraint languages A that have the atomic network
amalgamation property (aNAP), respectively. Huang et al. write that their algorithm is ﬁxed-parameter
tractable, but this is due to non-standard terminology; according to their Theorem 6, the algorithm
                   2              2
runs in O(w3 n · ew log n ) = nO(w ) time. These two general results apply to many interesting problems:
ω-categoricity is a fundamental property in the study of inﬁnite-domain CSPs and many AI-relevant
CSPs have this property (cf. the book by Bodirsky [12]). Similarly, the aNAP and other amalgamation
properties are highly important in this context, too. However, these properties do not hold for the
constraint language D or even the fragment D2,1 , as we will show next.
    The theorem by Engeler, Ryll-Nardzewski, and Svenonius (see e.g. [43, Theorem 6.3.1]) implies that
if A is an ω-categorical constraint language, then for all n > 1, there are ﬁnitely many nonequivalent
formulas over A with n free variables. This is not true for D2,1 : consider the inﬁnite sequence of formulas


                                                     8
                            Upper bounds           k=0          1≤k<∞           k unbounded
                               a=2                  ∈P           ∈ XP              ∈ pNP
                               a≥3                 ∈ FPT         ∈ XP              ∈ pNP

                             Lower bounds          k=0       1≤k<∞             k unbounded
                                 a=2                −        W[1]-hard           pNP-hard
                                 a≥3                −        W[1]-hard           pNP-hard

                    Table 3: Summary of parameterized complexity landscape for CSP(Da,k )


φ2 (x, y), φ3 (x, y), . . . deﬁned as follows:
                                                                              k−1
                                                                              ^
                           φk (x, y) ≡ ∃z1 , . . . , zk . x = z1 ∧ y = zk ∧         zi+1 − zi = 1
                                                                              i=1

and note that φk (x, y) holds if and only if y = x + k − 1. If a structure A containing binary relations
has aNAP, then for any pair of complete atomic instances (V1 , C1 ) and (V2 , C2 ) of CSP(A) that have
the same constraints over the variables in V1 ∩ V2 , their union (V1 ∪ V2 , C1 ∪ C2 ) is satisﬁable. An
instance of CSP(A) is complete if there is one constraint for every pair of variables, and it is atomic if
no constraints involve disjunctions. Consider the instances

                           I1 = ({x, a, y}, {a − x = 1, y − a = 1, y − x ∈ (1, ∞)}),
                           I2 = ({x, b, y}, {b − x = 1, y − b ∈ (0, 1), y − x ∈ (1, ∞)}).

I1 and I2 are complete, satisﬁable, atomic instances of CSP(D2,1 ), and they agree on their intersection.
However, their union is not satisﬁable, since I1 implies that y − x = 2, while I2 implies that y − x ∈ (1, 2).
    Dabrowski et al. [27] have presented a ﬁxed-parameter tractable algorithm for constraint languages
having the patchwork property [57]; this is yet another amalgamation property. The applicability of this
algorithm can naturally be ruled out with the aid of the hardness results presented in Section 6. It is
also straightforward to verify directly that the problems we study do not have the patchwork property:
in fact, the example above for ruling out that D2,1 has aNAP also shows that D2,1 does not have the
patchwork property.

1.4     Outline
This article is based on two conference papers [25, 26]. The major diﬀerences are that (1) this article gen-
eralizes our earlier results on various temporal formalisms to diﬀerence logic, (2) it gives a comprehensive
picture of the time complexity landscape, (3) the proofs are both uniﬁed and signiﬁcantly simpliﬁed by
the addition of multi-purpose results such as Theorem 6, and (4) the results are extended to both general
formulas and variables with integer domains. The article has the following structure. We present the
necessary preliminaries in Section 2. The upper and lower bounds on time complexity are collected in
Sections 3 and 4, respectively, while the parameterized upper and lower bounds are collected in Sections 5
and 6, respectively. We look at two generalizations of our results in Section 7: formulas that are not in
conjunctive normal form are considered in Section 7.1 and problems where variables have integer domains
in Section 7.2. We conclude the article in Section 8 with a discussion of our results.


2     Preliminaries
In this section we provide some prerequisites. We present the basic language of diﬀerence logic in Sec-
tion 2.1 and give a compact overview of the constraint satisfaction problem in Section 2.2. Finally,
Section 2.3 contains a primer on Sidon sets that we use as a tool for proving our lower bound results.


                                                            9
2.1     Difference Logic
We begin with some basic logical terminology. A (relational) signature τ is a set of symbols, each with
an associated natural number called their arity. A (relational) τ -structure A consists of a set D (the
domain), together with relations RA ⊆ Dk for each k-ary symbol R ∈ τ . To avoid overly complex
notation, we sometimes do not distinguish between the symbol R for a relation and the relation RA
itself. We also allow ourselves to view relational structures as sets and, for instance, write expressions
like R ∈ A. Let A be a τ -structure over a domain D. We say that A has arity a if every relation in A
has arity at most a.
     Let A be a τ -structure. First-order formulas φ over A (or, for short, A-formulas) are deﬁned using the
logical symbols of universal and existential quantiﬁcation, disjunction, conjunction, negation, equality,
bracketing, variable symbols, the relation symbols from τ , and the symbol ⊥ for the truth-value false.
First-order formulas over A can be used to deﬁne relations: for a formula φ(x1 , . . . , xk ) with free variables
x1 , . . . , xk , the corresponding relation R is the set of all k-tuples (t1 , . . . , tk ) ∈ Dk such that φ(t1 , . . . , tk )
is true in A. In this case we say that R is first-order definable in A. Our deﬁnitions of relations are
always parameter-free, i.e. we do not allow the use of domain elements within them.
     Certain types of ﬁrst-order formulas are particularly interesting for our purposes. Let φ denote a
ﬁrst-order formula.

    • φ is a sentence if it has no free variables.
    • φ is in conjunctive normal form (CNF), if it is a a conjunction of disjunctions of literals, i.e., atomic
      formulas or their negations. A disjunction of literals is called a clause.
    • φ is quantifier-free if it does not contain existential and/or universal quantiﬁers.
    • φ is existential if φ = ∃x1 , . . . , xn .ψ where ψ is quantiﬁer-free.

We let S denote the relational structure representing the atomic DL formulas, i.e. the inﬁnite set of
relations
                                   {(x, y) ∈ Q2 : ℓ ⊙1 x − y ⊙2 u}
for any ℓ ∈ Z ∪ {−∞}, u ∈ Z ∪ {∞} and ⊙1 , ⊙2 ∈ {<, ≤}. We will sometimes consider a restricted set
S≤ where ⊙1 = ⊙2 = ≤. The satisﬁability problem for DL is the following problem.

  DL-Sat
   Input:         An existential ﬁrst-order sentence φ over S.
   Question:      Is φ true?

    Note that we make (without loss of generality) the sensible assumption that the bounding values are
integers (see e.g. the article by Tsamardinos & Pollack [78]): real values cannot in general be written down
with a ﬁnite number of bits, and rational numbers can be scaled in a suitable way. We use the rationals
as the value domain (also without loss of generality): if there is a solution to an instance of CSP(D)
over the reals, then there is also a solution over the rationals. While this is not of major importance in
this article, the diﬀerences between R and Q sometimes causes confusion and/or technical problems. We
refer the reader to the literature for a more thorough discussion of representational issues [14, 50].

2.2     Constraint Satisfaction
We continue by deﬁning the constraint satisfaction problem (CSP). Let A denote a relational τ -structure
deﬁned on a set D of values. The constraint satisfaction problem over A (CSP(A)) is deﬁned as follows:




                                                              10
  CSP(A)
   Input:        A tuple (V, C), where V is a set of variables and C is a set of constraints
                 of the form R(v1 , . . . , va ), where a is the arity of R, v1 , . . . , va ∈ V , and
                 R ∈ A.
   Question:     Is there a function f : V → D such that (f (v1 ), . . . , f (va )) ∈ R for
                 every R(v1 , . . . , va ) ∈ C?

    Observe that we do not require A to have ﬁnite signature or D to be a ﬁnite set. The structure
A is sometimes referred to as a constraint language, while the function f is a satisfying assignment or
simply a solution. If c = R(x1 , . . . , xa ) is a constraint, then the set {x1 , . . . , xa } is the scope of c. We
denote this set by scope(c). A basic example of a CSP is the STP problem: it is easy to verify that it
equals CSP(S). Another example is the max-atoms problem: it is conveniently deﬁned as a CSP with
the inﬁnite constraint language Amax containing the relations Ra = {(x, y, z) ∈ Q3 : max(x, y) + d ≥ z}
for every d ≥ 0. We note that Rd is quantiﬁer-free deﬁnable in S since

                                 max(x, y) + d ≥ z ⇔ (x + d ≥ z) ∨ (y + d ≥ z).

   One may view CSP(A) with A ⊆ D as a restricted DL-Sat problem. An A-sentence is primitive
positive if it is of the form

                                                 ∃x1 , . . . , xn .ψ1 ∧ . . . ψl
where ψ1 , . . . , ψl are atomic formulas over A, i.e. formulas (1) R(y1 , . . . , ya ) with R ∈ A, (2) yi = yj , or
(3) ⊥. Thus, CSP(A) can be viewed as DL-Sat restricted to primitive positive A-formulas whenever
the equality relation is in A. This assumption is harmless for the CSP problem: adding equality to the
constraint language does not aﬀect the complexity of the CSP up to log-space reductions (cf. Lemma
1.2.6 in [12]). This connection between CSP and DL-Sat will be exploited in Section 7.
WmTo simplify the presentation, we sometimes use an alternative notation for a disjunctive constraint
   ℓ=1 xiℓ − xjℓ ∈ Iℓ and write it as a set of simple constraints {xiℓ − xjℓ ∈ Iℓ : ℓ ∈ {1, . . . , m}}. Then, an
assignment satisﬁes the disjunctive constraint whenever it satisﬁes at least one simple constraint in the
corresponding set. This way of viewing disjunctions simpliﬁes, for instance, the treatment of certiﬁcates
in Section 3.2.1.
     When considering CSPs with inﬁnite constraint languages, it is important to specify how the relation
symbols are represented in the input instances. In our case, it would (for instance) be suﬃcient to
represent the relation symbol for a relation R by a quantiﬁer-free CNF deﬁnition of R using atomic
formulas of the form x − y ⊙ c with ⊙ ∈ {<, ≤}, and coeﬃcients c ∈ Z represented in binary. Such a
representation has certain pleasant features: one may, for instance, check in polynomial time whether a
given rational tuple (where the numerator and denominator are viewed as integers represented in binary)
is a member of R or not. Note that there are no representational issues like these when considering ﬁnite
constraint languages.
     For an instance I of CSP(A), we write kIk for the number of bits required to represent I. We
primarily measure time complexity in terms of n (the number of variables). Historically, this has been
the most common way of measuring time complexity: for instance, the vast majority of work concerning
ﬁnite-domain CSPs concentrates on the number of variables. One reason for this is that an instance may
be much larger than the number of variables. Consider an instance of the propositional SAT problem,
i.e. a propositional logical formula in CNF. Such a formula may contain up to 22n distinct clauses if
repeated literals are disallowed, so measuring in terms of the instance size may give far too optimistic
ﬁgures. It is thus more informative to know that SAT can be solved in O∗ (2n ) time1 instead of knowing
that it is solvable in O∗ (2kIk ) time.
     The various constraint languages that we will consider were deﬁned in Section 1. We note that
disjunctive temporal relations are sometimes deﬁned in a more general way which allows for unary atomic
relations x ∈ I (as opposed to binary atomic relations x − y ∈ I). The standard trick for handling unary
  1 The O ∗ (·) notation hides polynomial factors.




                                                              11
relations is to introduce a zero variable (see [6]). Solutions to CSP(D) have the following property: if
ϕ : V → Q satisﬁes an instance (V, C), then so does ϕ′ (v) = ϕ(v)+c where c ∈ Q is an arbitrary constant.
Thus, we can pick an arbitrary variable in V and assume that its value is zero: such a variable is called a
zero variable. We can now easily express unary constraints, e.g. the constraint x − z ∈ (0, 2] is equivalent
to x ∈ (0, 2] if z is the zero variable. Adding a single zero variable does not aﬀect the time complexity
with more than a multiplicative factor.

2.3    Sidon Sets
Our lower bound results presented in Sections 4 and 6 use Sidon sets [73]. The study of Sidon sets is
an important topic in additive number theory and elsewhere; see e.g. the survey by O’Bryant [62] or
the book by Halberstam and Roth [42]. The terminology used in the literature may appear confusing:
they are known under several names such as Golomb rulers, Sidon sequences, and B2 -sets, and the term
Sidon set has diﬀerent meanings in number theory and functional analysis. A Sidon set S is a set of
integers such that the sum of any pair of its elements is unique, i.e. if a + b = c + d for a, b, c, d ∈ S,
then {a, b} = {c, d}. It is easier to work with diﬀerences in our proofs so we use the following equivalent
condition: for all a, b, c, d ∈ S such that a 6= b and c 6= d, a − b = c − d holds if and only if a = c and
b = d. This indicates one way of using Sidon sets: they allow us (under certain conditions) to rewrite a
disjunction x 6= a ∨ y 6= b (where x, y are variables and a, b integers) as a diﬀerence x − y 6= c for some
integer c.
    The order of a Sidon set is the number of elements in it and the length is the diﬀerence between its
maximal and minimal elements. For example, {0, 1, 4, 6} is a Sidon set of order 4 with length 6. We will
use a particular way of constructing Sidon sets with length quadratic in their order.
Proposition 4 ([30]). Let p ≥ n be an odd prime. Then

                            Sn = pa + (a2 mod p) : a ∈ {0, . . . , n − 1}
                                  


is a Sidon set.
    We sometimes need to ensure that the length of a Sidon set is bounded by a polynomial in its order
k. Indeed, Proposition 4 shows that there is a Sidon set containing k positive integers and whose largest
element is at most 2p2 , where p is the smallest prime number larger than or equal to k. This set can
clearly be constructed in polynomial time. Together with Bertrand’s postulate (see e.g. Chapter 2 in the
book by Aigner and Ziegler [1]) which states that for every natural number n there is a prime number
between n and 2n, we see that a Sidon set of order k and length 8k 2 can be generated in polynomial
time.


3     Upper Bounds on Time Complexity
This section contains two main results: a 2O(n(log n+log k)) time algorithm for CSP(D) (Section 3.1) and
a 2O(n log log n) time algorithm for CSP(D2,k ) when k < ∞ is ﬁxed (Section 3.2). These results together
with the lower bound results that are proved in Section 4 are summarized in Table 2.

3.1    Upper Bound for CSP(D)
We will prove a small solution property for CSP(D). Small solution properties are results that state
that a solvable instance of CSP(A) has a solution that assign ‘small’ values to the variables. Exactly
what is meant by ‘small’ varies in diﬀerent contexts. A concrete example is provided by Bezem et al. [9]
for the max-atoms problem that we encountered in Section 1.1: every satisﬁable instance (V, C) of the
max-atoms problem has a solution f : V → {0, . . . , p} where
                                                    X
                                         p=                  |d|.
                                              max(x,y)+d≥z∈C


                                                    12
    Another example (from Section 1.2) is UTVPI relations. These are deﬁned as {(x, y) ∈ Z2 : ax + by ≥
c} where a, b ∈ {−1, 0, 1} and c ∈ Z. Seshia et al. [72] prove that every satisﬁable instance (V, C) of the
CSP over UTVPI relations has a solution in the interval {−|V | · k, . . . , |V | · k} where k = num(C).This
result implies that every satisﬁable instance (V, C) of CSP(D≤ ) has a solution {−|V | · k, . . . , |V | · k}
but it does not give a bound for CSP(D)—note, for instance, that CSP(D) is not guaranteed to have
integer solutions, e.g. {x − y ∈ (0, 1)}. Bezem et al.’s proof has a graph-theoretical ﬂavor while Sesha et
al.’s proof is based on a polyhedral approach. None of these methods appear to be directly applicable
to CSP(D): Bezem et al.’s proof use intrinsic properties of the max-atom problem while Sesha et al.’s
approach is built around the fact that solutions must assign integers to the variables. Our proof strategy
has more of an order-theoretic ﬂavor. Deﬁne the set
                               n     q                                                     o
                  CD (n, k) = z + : z, q ∈ N, 0 ≤ z ≤ (n − 1)(k + 1), and 0 ≤ q < n
                                     n
for n, k ∈ N. This set will serve as a ruler, and we will show that any satisfying assignment to an instance
of CSP(D) with n variables and numerical bound k can be transformed into one that only chooses values
from the ruler. To achieve this we will split the assignment of each variable into the integral part and
the fractional part and show how to independently transform these parts. Our starting point is the
following lemma which provides suﬃcient conditions for two assignments to satisfy the same set of simple
constraints. This lemma will also be useful when proving the forthcoming Lemma 10.
    We let ⌊x⌋ denote the floor function (i.e. ⌊x⌋ is the largest integer less than or equal to the real number
x) and we let frac(x) denote the fractional part of the non-negative real number x (i.e. frac(x) = x − ⌊x⌋).
To simplify the proof, we note that it is suﬃcient to concentrate on unit constraints, which are deﬁned
as follows. Let T ⊆ D2,k be the constraint language with relations

                                    {(x, y) ∈ Q2 : x − y ∈ {i}},
                                    {(x, y) ∈ Q2 : x − y ∈ (i, i + 1)}, and
                                    {(x, y) ∈ Q2 : x − y ∈ (i, ∞)}

for all i ∈ Z. We refer to the relations in T as unit relations. Consider constraint x − y ∈ (−1, 0] ∪ [1, ∞).
An equivalent constraint can be enforced by a disjunction of unit constraints x − y ∈ (−1, 0) ∨ x − y ∈
{0} ∨ x − y ∈ {1} ∨ x − y ∈ (1, ∞). In a similar manner, we can rewrite every disjunctive temporal
constraint as a disjunction of unit constraints. We are now ready to prove the main technical lemma.
Lemma 5. Let k be an integer and let φ1 : V → Q and φ2 : V → Q be two assignments of the variables
in V that satisfy the following two conditions:
  1. For every x, y ∈ V , it holds that φ1 (x) − φ1 (y) and φ2 (x) − φ2 (y) have the same integer part up to
     k + 1, i.e. min{⌊φ1 (x) − φ1 (y)⌋, k + 1} = min{⌊φ2 (x) − φ2 (y)⌋, k + 1}.
  2. For every x, y ∈ V , it holds that frac(φ1 (x)) ⊙ frac(φ1 (y)) if and only if frac(φ2 (x)) ⊙ frac(φ2 (y))
     for every ⊙ ∈ {<, =, >}.
Then, φ1 and φ2 satisfy the same simple constraints over V with relations in D2,k .
Proof. To show the lemma, it is suﬃcient to show that φ1 and φ2 satisfy the same unit constraints.
Suppose that φ1 and φ2 satisfy conditions 1 and 2. We need to show that φ1 satisﬁes any of the unit
constraints on two variables x and y if and only if so does φ2 . We distinguish the following cases according
to the three types of unit constraints given above.
   • If φ1 (x) − φ1 (y) ∈ {i} for some i ≤ k, then ⌊φ1 (x) − φ1 (y)⌋ = i and frac(φ1 (x)) = frac(φ1 (y)).
     Therefore, ⌊φ2 (x)−φ2 (y)⌋ = i and frac(φ2 (x)) = frac(φ2 (y)), which implies that φ2 (x)−φ2 (y) ∈ {i}.
   • If φ1 (x) − φ1 (y) ∈ (i, i + 1) for some i < k, then ⌊φ1 (x) − φ1 (y)⌋ = i and frac(φ1 (x)) > frac(φ1 (y)).
     Therefore, ⌊φ2 (x) − φ2 (y)⌋ = i and frac(φ2 (x)) > frac(φ2 (y)), which implies that φ2 (x) − φ2 (y) ∈
     (i, i + 1).


                                                      13
   • If φ1 (x) − φ1 (y) ∈ (i, ∞) for some i ≤ k, then either ⌊φ1 (x) − φ1 (y)⌋ = i and frac(φ1 (x)) >
     frac(φ1 (y)) or ⌊φ1 (x) − φ1 (y)⌋ > i. In the former case, we have that ⌊φ2 (x) − φ2 (y)⌋ = i and
     frac(φ2 (x)) > frac(φ2 (y)) and therefore φ2 (x) − φ2 (y) ∈ (i, ∞). In the latter case, we have that
     ⌊φ2 (x) − φ2 (y)⌋ > i and therefore φ2 (x) − φ2 (y) ∈ (i, ∞).
This completes the proof.
   Lemma 5 enables us to give a clear-cut proof of the small solution property.
Theorem 6. Every satisfiable instance I = (V, C) of CSP(D) has a solution f : V → CD (|V |, num(C)).
Proof. Let I = (V, C) be a satisﬁable instance of CSP(D) with solution g : V → Q. Let n = |V |,
k = num(C), our strategy is to take the assignment g and construct a new assignment f : V → CD (n, k)
that satisﬁes the same simple constraints as g over V with relations in D2,k .
    Index the variables {v1 , . . . , vn } so that g(vi ) ≤ g(vi+1 ) for all 1 ≤ i < n. Then, split the values
g(vi ) into integral and fractional parts, i.e. deﬁne zi = ⌊g(vi )⌋ and qi = frac(g(vi )) for all i. Note that
0 ≤ qi < 1 and the integers z1 , . . . , zn are in non-decreasing order.
    We recursively deﬁne the assignment f (vi ) = ci + di for all i, where ci is the integral part and di is
the fractional part of f (vi ). Set c1 = 0 and let ci+1 = ci + min{zi+1 − zi , k + 1} for all 1 ≤ i < n. Note
that c1 , . . . , cn are sorted in non-decreasing order. Furthermore, let σ : {q1 , . . . , qn } → {0, . . . , n − 1} be
an injective function such that σ(qi ) ⊙ σ(qj ) ⇐⇒ qi ⊙ qj for all i, j and ⊙ ∈ {<, =, >}. One may view
                                                                                                    i)
σ as an order-preserving ‘scaling’ of the fractional parts into the integers. Let di = σ(q        n    for all i. Note
that cn ≤ (n − 1)(k + 1) and 0 ≤ σ(qi ) ≤ n − 1, so f maps the variables in V into the set CD (n, k), as
desired. Moreover, since f and g satisfy the conditions on φ1 and φ2 given in the statement of Lemma 5,
we obtain that f and g satisfy the same simple constraints over V with relations in D2,k . Therefore, f
also satisﬁes I, as required.
    Theorem 6 gives us straightforward upper bounds on the time complexity of CSP(D) and many of
its subclasses.
Corollary 7. Every instance I = (V, C) of CSP(D) can be solved in 2O(n(log n+log k)) time where n = |V |
and k = num(C). In particular, every instance of CSP(D∞,k ) can be solved in 2O(n log n) time.
Proof. Enumerate all assignments f : V → CD(n, k) and check if they satisfy I. Theorem 6 implies that
I is satisﬁable if and only if at least one such assignment is satisfying. This takes O∗ (|CD(n, k)|n ) time
in total. The set CD(n, k) contains O(n2 k) elements so
                 O∗ (|CD(n, k)|n ) = O∗ ((n2 k)n ) = 2O(n log n) · 2O(n log k) = 2O(n(log n+log k)) .



3.2     Upper Bound for CSP(D2,k )
In this section we prove that CSP(D2,k ) can be solved in 2O(n log log n) time. Our algorithm for CSP(D2,k )
is based on a divide-and-conquer approach, i.e., we split the instance into smaller parts and solve them
recursively. To achieve the splitting, we ﬁrst show that any solution for an instance I of CSP(D2,k )
suggests a natural split of the whole instance into either two or three almost independent subinstances;
here, almost independent refers to the instances sharing only a small set of variables. This will be
exploited by the algorithm to enumerate all possible decompositions into two or three subinstances and
recurse on those for every possible assignment of the shared variables. We also need a subroutine that
allows us to ﬁnd all solutions with small domain values. This is used to solve the middle instance in the
case that the instance decomposes into three subinstances.
    Before we begin, we describe some polynomial time preprocessing steps for CSP(D2 ). Suppose there
are two constraints for a pair of variables x − y:
                                           x − y ∈ I1 ∨ · · · ∨ x − y ∈ Ip ,
                                           x − y ∈ J1 ∨ · · · ∨ x − y ∈ J q ,



                                                          14
where I1 , . . . , Ip and J1 , . . . , Jq are intervals. For both constraints to hold, there must exist 1 ≤ i ≤ p
and 1 ≤ j ≤ q such that x − y ∈ Ii ∩ Jj . Thus, we can replace these two constraints with
                                            p _
                                            _ q
                                                      x − y ∈ Ii ∩ Jj .
                                            i=1 j=1

Applying this procedure exhaustively, we obtain an instance with at most one constraint for every pair
of variables. In the rest of the section we assume that all instances I = (V, C) are preprocessed, and we
write σC (x, y) to denote the constraint in C over variables x and y; if there are no constraints over x and
y, we let σC (x, y) be the set of all possible simple constraints over x and y.
    The rest of this section is divided into three parts (Sections 3.2.1–3.2.3): the ﬁrst two sections introduce
certain subroutines that are needed in the algorithm, and the algorithm itself is presented and proven
correct in the third section.

3.2.1   Certificates
We begin by presenting an alternative method for enumerating compact representations of solutions to
CSP(D) instances in terms of certiﬁcates. The main advantage of certiﬁcates compared to representing
solutions by assignments is that certiﬁcates allow us to express the partial solution in terms of constraints.
In particular, it allows us to ﬁx the behavior of certain variables by simply adding additional constraints
to the instance.
    Let I = (V, C) be an instance of CSP(D). Deﬁne U(C) to be the set of simple temporal constraints
appearing as disjuncts in C. For example, if C = {(x − y ≤ 0) ∨ (x − y ≥ 1), x − z ≥ 1}, then
U(C) = {x − y ≤ 0, x − y ≥ 1, x − z ≥ 1}. Let ϕ : V → R be an assignment to I. We identify ϕ with
the subset of constraints F ⊆ U(C) satisﬁed by ϕ. This allows us to deﬁne an equivalence relation ∼ on
the assignments where ϕ1 ∼ ϕ2 holds if and only if F1 = F2 . This way, F represents the entire class of
assignments equivalent to ϕ. We say that F is a certificate of the satisﬁability of I. An assignment ϕ
is satisfying if the certiﬁcate F contains at least one simple constraint from every c ∈ C. Note that if
ϕ1 ∼ ϕ2 and ϕ1 is a satisfying assignment, then so is ϕ2 . While there may be inﬁnitely many satisfying
assignments to I, the number of certiﬁcates is ﬁnite since there are at most as many certiﬁcates as there
are subsets of U(C).
Theorem 8. The list of certificates to an instance I = (V, C) of CSP(D) can be computed in 2O(n(log n+log k))
time, where n = |V | and k = num(C).
Proof. By deﬁnition, every certiﬁcate I ′ = (V ′ , C ′ ) for I is a satisﬁable instance of CSP(S) with n
variables and num(C ′ ) ≤ k. Theorem 6 implies that each I ′ admits a satisfying assignment in CD(n, k).
Thus, we can enumerate assignments f : V (I) → CD(n, k), check whether it satisﬁes I, and if so,
collect the simple constraints in U(C) satisﬁed by f and output them as a certiﬁcate. This requires
|CD(n, k)|n ≤ (n2 k)n = 2O(n(log n+log k)) time.
  The algorithm underlying the previous theorem will be used as a subroutine in our algorithm for
CSP(D2,k ). We will refer to it as ListCert in what follows.

3.2.2   Instances with Bounded Span
We continue by examining a restricted version of CSP(D2 ) (denoted w-CSP(D2 )) where solutions can
only take values in the interval [0, w); we say that such a solution has span w. We show that this problem
can be solved in O∗ (wn ) time.

Lemma 9. w-CSP(D2 ) can be solved in O∗ (wn ) time.
Proof. Let I = (V, C) be an instance of w-CSP(D2 ) and assume ϕ : V → [0, w) is a satisfying assignment.
Without loss of generality, assume that all constraints in C are represented as disjunctions of unit con-
straints. We split ϕ into integral and fractional parts: ϕ(x) = ϕi (x)+ ϕf (x), where ϕi (x) ∈ {0, . . . , w − 1}


                                                         15
and 0 ≤ ϕf (x) < 1. Suppose we ﬁx ϕi and want to check whether any ϕf extends ϕi to a satisfying
assignment. For every pair of distinct variables x and y we have ϕi (x) − ϕi (y) = c for some integer c.
There are only six nontrivial unit constraints that agree with this assignment, each of them expressible
as a linear inequality or disequality:

               x − y ∈ (c − 1, c)                           −→                 ϕf (x) < ϕf (y)
               x − y ∈ {c}                                  −→                 ϕf (x) = ϕf (y)
               x − y ∈ (c, c + 1)                           −→                 ϕf (x) > ϕf (y)
               x − y ∈ (c − 1, c]                           −→                 ϕf (x) ≤ ϕf (y),
               x − y ∈ [c, c + 1)                           −→                 ϕf (x) ≥ ϕf (y),
               x − y ∈ (c − 1, c) ∪ (c, c + 1)              −→                 ϕf (x) 6= ϕf (y).

These constraints together with the domain restriction 0 ≤ ϕf (v) < 1 for each v yield a system of linear
inequalities and disequalities that has a solution if and only if there is a fractional assignment ϕf that
extends ϕi to a satisfying assignment. Feasibility of a system of linear inequalities and disequalities can
be decided in polynomial time [47, 53]. There are wn possible functions ϕi : V → {0, . . . , w − 1} and
checking whether an integer assignment ϕi can be extended to a satisfying assignment requires polynomial
time. Hence, the total running time of this algorithm is O∗ (wn ).
   We refer to the algorithm underlying the previous lemma as SolveBounded.

3.2.3   Divide-and-Conquer Strategy
Our algorithm for CSP(D2,k ) is based on a divide-and-conquer approach: we split the instances into
smaller parts and solve them recursively. To achieve the splitting, we ﬁrst show that any satisfying
assignment for an instance of CSP(D2,k ) provides a natural split of the instance into either two or
three subinstances. These subinstances are almost independent in the sense that they only share a small
number of variables. By enumerating suitable values for the shared variables, we can thus solve the original
instance recursively. To show that every satisfying assignment allows one of the two splits, consider a
satisfying assignment ϕ of an instance I = (V, C) of CSP(D2,k ). We can assume that the minimal value
assigned by ϕ is zero by translational invariance and we additionally assume that ϕ : V → [0, kw) for some
w ∈ N. Next, we divide the domain of ϕ into intervals [ki − k, ki) of span k for every i ∈ {1, . . . , w}. This
implies a partition of the variables in V into disjoint (possible empty) subsets {Vi : i ∈ {0, . . . , w + 1}}
deﬁned as follows:
                                       Vi = {v ∈ V : ϕ(v) ∈ [ki − k, ki)}
for all i ∈ {1, . . . , w}, and V0 = Vw+1 = ∅. Also, deﬁne the sets Li = i−1
                                                                            S                  Sw+1
                                                                              j=0 Vj and Ri =     j=i+1 Vj for
all i. We start by showing that we can split the instance at any Vi to obtain two subinstances that are
independent up to their overlap at Vi . That is, let I[U ] = (U, C[U ]) be the subinstance of I induced by
the variables in U , where C[U ] is the subset of C containing only the constraints with all variables in
U . Then, the following lemma provides necessary and suﬃcient conditions that allows us to transform
solutions for the subinstances I[Li ∪ Vi ] and I[Vi ∪ Ri ] into a solution for the whole instance; informally
the lemma allows us to split the instance at any Vi .
Lemma 10. Let I = (V, C) be an instance of CSP(D2,k ), where V is equal to the disjoint union of
the sets X, Y , and Z. Assume ϕ1 and ϕ2 are satisfying assignments to the subinstances I[X ∪ Y ] and
I[Y ∪ Z], respectively. If the following conditions hold, then I is satisfiable:
  1. For every pair of variables x ∈ X and z ∈ Z, the constraint σC (x, z) is empty or it implies z −x > k.
  2. Assignments ϕ1 and ϕ2 satisfy the same unit constraints over every pair of variables in Y .
  3. There is T1 ∈ Q such that ϕ1 (x) < T1 ≤ ϕ1 (y) < T1 + k for all x ∈ X and y ∈ Y .
  4. There is T2 ∈ Q such that T2 ≤ ϕ2 (y) < T2 + k ≤ ϕ2 (z) for all y ∈ Y and z ∈ Z.

                                                      16
Proof. First note that the ordering of the variables in Y with respect to ϕ1 and ϕ2 is the same since,
otherwise, there are two variables y and y ′ that do not satisfy the same simple constraints under ϕ1 and ϕ2
and this contradicts condition 2. Rename the variables in Y so that y1 , . . . , y|Y | is in non-decreasing order
with respect to ϕ1 and ϕ2 . It is convenient to assume, without loss of generality, that ϕ1 (y1 ) = ϕ2 (y1 ) = 0
– we can arrive at such assignments by subtracting ϕi (y1 ) from ϕi (y) for every y ∈ Y and i ∈ {1, 2}.
We show next that ⌊ϕ1 (y)⌋ = ⌊ϕ2 (y)⌋ for every y ∈ Y . This clearly holds for y1 so we arbitrarily pick
another variable y ∈ Y . Now, it holds that ϕi (y) − ϕi (y1 ) = ϕi (y) for every i ∈ {1, 2}. We distinguish
the following cases:
   • ϕ1 (y) − ϕ1 (y1 ) = i for some i ∈ {0, . . . , k},
   • ϕ1 (y) − ϕ1 (y1 ) ∈ (i, i + 1) for some i ∈ {0, . . . , k − 1}, or
   • ϕ1 (y) − ϕ1 (y1 ) ∈ (k, ∞).
Note that the third case cannot occur because of conditions 3 or 4. Moreover, in the ﬁrst case we obtain
from condition 2 that ϕ2 (y) − ϕ2 (y1 ) = i, which implies that ϕ1 (y) = ϕ2 (y) = i. Finally, in the second
case, we obtain from condition 2 that ϕ2 (y) − ϕ2 (y1 ) ∈ (i, i + 1), which implies that ⌊ϕ1 (y)⌋ = ⌊ϕ2 (y)⌋.
    Now we show that frac(ϕ1 (y))⊙ frac(ϕ1 (y ′ )) if and only if frac(ϕ2 (y))⊙ frac(ϕ2 (y ′ )) for every y, y ′ ∈ Y
and ⊙ ∈ {<, =, >}. We distinguish the following cases. If frac(ϕi (y)) = frac(ϕi (y ′ )) for some i ∈ {1, 2},
then ϕi (y)−ϕi (y ′ ) is an integer and conditions 3 and 4 imply that ϕi (y)−ϕi (y ′ ) ∈ {−k, . . . , k}. Therefore,
we obtain from condition 2 that ϕ1 (y) − ϕ1 (y ′ ) = ϕ2 (y) − ϕ2 (y ′ ) so ϕ2 (y) − ϕ2 (y ′ ) is an integer and
frac(ϕ2 (y)) = frac(ϕ2 (y ′ )), as required. Otherwise, suppose without loss of generality that frac(ϕ1 (y)) <
frac(ϕ1 (y ′ )) and ⌊ϕ1 (y)⌋ ≤ ⌊ϕ1 (y ′ )⌋. Then, using condition 3, we obtain that ϕ1 (y ′ ) − ϕ1 (y) ∈ (i, i + 1)
for some i ∈ {0, . . . , k − 1}. By condition 2, it follows that ϕ2 (y ′ ) − ϕ2 (y) ∈ (i, i + 1), too. Since the
integer parts of y and y ′ are the same for both ϕ1 and ϕ2 , we see that frac(ϕ2 (y)) < frac(ϕ2 (y ′ )), as
required.
    We are now ready to deﬁne a common assignment ϕ for I as follows. We keep the integer part of
every variable in X ∪ Y ∪ Z the same as before, i.e.:
   • for every x ∈ X, we set the integer part of ϕ(x) equal to the integer part of ϕ1 (x),
   • for every z ∈ Z, we set the integer part of ϕ(z) equal to the integer part of ϕ2 (z), and
   • for every y ∈ Y , we set the integer part of ϕ(y) equal to the integer part of ϕ1 (y) and ϕ2 (y); using
     the property that the integer parts of ϕ1 (y) and ϕ2 (y) are equal.
To deﬁne the fractional part of ϕ(v) for every v ∈ X ∪ Y ∪ Z, let ρ1 (ρ2 ) be the ordered partition2
of the variables in X ∪ Y (Y ∪ Z) ordered by non-decreasing fractional part with respect to ϕ1 (ϕ2 ).
Then, ρ1 and ρ2 are equal if restricted to the variables in Y and therefore we can combine them into
an ordered partition ρ of the variables in X ∪ Y ∪ Z. Moreover, from ρ we can obtain a function
σ : X ∪ Y ∪ Z → {0, . . . , |X ∪ Y ∪ Z| − 1} such that for every ⊙ ∈ {<, =, >} it holds that:
   • σ(u) ⊙ σ(v) if and only if frac(ϕ1 (u)) ⊙ frac(ϕ1 (v)) for every u, v ∈ X ∪ Y and
   • σ(u) ⊙ σ(v) if and only if frac(ϕ2 (u)) ⊙ frac(ϕ2 (v)) for every u, v ∈ Y ∪ Z.
We now obtain the fractional part of ϕ(v) by setting ϕ(v) = σ(v)/n, which implies that ϕ satisﬁes:
   • ϕ(u) ⊙ ϕ(v) if and only if frac(ϕ1 (u)) ⊙ frac(ϕ1 (v)) for every u, v ∈ X ∪ Y and
   • ϕ(u) ⊙ ϕ(v) if and only if frac(ϕ2 (u)) ⊙ frac(ϕ2 (v)) for every u, v ∈ Y ∪ Z.
It now follows from Lemma 5 (applied to ϕ and ϕ1 as well as ϕ and ϕ2 ) that ϕ satisﬁes I[X ∪ Y ] and
I[Y ∪ Z]. Moreover, because of condition 3 and 4, it holds that ϕ(z) − ϕ(x) > k for every x ∈ X and
z ∈ Z, which together with condition 1 implies that ϕ also satisﬁes I[X ∪ Z]. Therefore, ϕ satisﬁes I, as
required.
  2 An ordered partition of a finite set S is a sequence of non-empty disjoint subsets (S
                                                                                                                         Sℓ
                                                                                            1 , . . . , Sℓ ) such that    i=1 Si = S.



                                                            17
    The above lemma shows that the instance can be split at any Vi into two subinstances I[Li ∪ Vi ] and
I[Vi ∪ Ri ] that are independent once we ﬁx a certiﬁcate for the instance I[Vi ]. This also means that a
split at Vi will only be useful if the number of possible certiﬁcates of I[Vi ], or equivalently the number of
variables in Vi , is not too large. That is, if Vi contains at most n/ log n variables, then we say it is sparse
and, otherwise, we say that it is dense. The choice of n/ log n as the threshold value is justiﬁed by the
following proposition:
Proposition 11. The number of certificates for any instance I = (V, C) of CSP(D) with at most
N ≤ n/ log(n) variables can be computed in time 2O(n) .
Proof. This follows immediately from Theorem 8 after observing that 2O(N (log N +log k)) = 2O(n) , where
k = num(C) is constant.

    The next lemma is crucial for our algorithm since it allows us to show that any solution naturally
splits the instance into either two or three almost independent subinstances; we will later see how the
subinstances are obtained from the partitions identiﬁed by the lemma. Informally, case 1 in the lemma
corresponds to a three-split and gives rise to the two instances I[Li ∪ Vi ] and I[Vi ∪ Ri ] and case 2 in the
lemma corresponds to a ﬁve-split and gives rise to the three instances I[Li ∪Vi ], I[Vi ∪Vi+1 ∪· · ·∪Vj−1 ∪Vj ]
(where i ≤ j), and I[Vj ∪ Rj ].
Lemma 12. Let I = (V, C) be an instance of CSP(D2,k ), let ϕ : V → [0, kw) be an assignment of
I = (V, C), and let Vi , Li , and Ri be defined as above with respect to ϕ. If |V | ≥ 8, then one of the
following holds:
  1. There is an index 0 ≤ i ≤ w + 1 such that Vi is sparse, |Li | ≥ n/3 and |Ri | ≥ n/3.
  2. There are indices 0 ≤ i < j ≤ w + 1 such that Vi and Vj are sparse, Vs is dense for all i < s < j,
     |Li | < n/3 and |Rj | < n/3.
Proof. If Vi is sparse, then |Li |+|Ri | = |V |−|Vi | ≥ n−n/ log n. Since log n ≥ 3, we have |Li |+|Ri | ≥ 2n/3.
Thus, for every sparse Vi either |Li | ≥ n/3 or |Ri | ≥ n/3.
   Let i be the maximal index such that Vi is sparse and |Ri | ≥ n/3. Similarly, let j be the minimal index
such that Vj is sparse and |Lj | ≥ n/3. Such indices always exist since V0 and Vw+1 are sparse. If i ≥ j,
then both Vi and Vj meet the conditions of Case 1. Otherwise, all Vs for i < s < j are dense. If neither
Vi nor Vj fulﬁlls the conditions of Case 1, then |Li | < n/3 and |Rj | < n/3, and we are in Case 2.
   We are now ready to prove that the algorithm is correct and analyze its running time.
Theorem 13. Algorithm 1 solves instances of CSP(D2,k ) in 2O(n log log n) time.
Proof. Consider an arbitrary instance I = (V, C) of CSP(D2,k ). We prove the claim by induction based
on |V |. If the instance has fewer than 8 variables, the claim follows by Corollary 7. Assume henceforth
that |V | ≥ 8.
    First, we prove that if the algorithm accepts an instance, then it is satisﬁable. Suppose the procedure
ThreeSplit accepts I. We show that instance I is satisﬁable since all four conditions of Lemma 10 are
fulﬁlled. First, note that subinstances I1 and I2 in lines 15 and 16 have at most 2n/3 + 1 < n variables.
Hence, they admit satisfying assignments by the inductive hypothesis. Condition 1 is ensured by the
check on line 11. Condition 2 is ensured since both subinstances I1 and I2 satisfy all constraints in FY ′ .
Conditions 3 and 4 are ensured by the introduction of ymin and the constraints involving it.
    Suppose instead that the procedure FiveSplit accepts I. First, note that subinstances I1 and I3 in
lines 32 and 34 have at most n/3 + 1 < n variables. Hence, they admit satisfying assignments by the
inductive hypothesis. Subinstance I2 is satisﬁable by Lemma 9. Observe that Lemma 10 applies to the
subinstance induced by S3 ∪S4 ∪S5 . We see that Condition 1 is ensured by the check on line 25, Condition 2
is ensured since both subinstances I2 and I3 satisfy all constraints in FS4′ , and Conditions 3 and 4 are
ensured by the introduction of smin4   and the constraints involving it. Let X = S3 ∪ S4 ∪ S5 and consider
the subinstance induced by S1 ∪ S2 ∪ X. Lemma 10 is applicable and we see that Condition 1 is ensured


                                                      18
Algorithm 1
 1: procedure Solve(I = (V, C))
 2:   if ∅ ∈ C then reject
 3:   if |V | < 8 then
 4:      accept if ListCert(I) 6= ∅ else reject
 5:   if ThreeSplit(I) then accept
 6:   if FiveSplit(I) then accept
 7:   reject

 8: procedure ThreeSplit(I = (V, C))
 9:   for each 3-partition (X, Y, Z) of V do
10:     if |X|, |Z| ≥ |V3 | and |Y | ≤ log|V|V| | and
11:        z − x > k ∈ σC (x, z) for x ∈ X, z ∈ Z then
           // introduce a fresh variable ymin
12:        Y ′ ← Y ∪ {ymin}
13:        IY ′ ← (Y ′ , CY ∪ {0 ≤ y − ymin < k}y∈Y )
14:        for FY ′ ∈ ListCert(IY ′ ) do
15:           I1 ← (X ∪ Y ′ , CX∪Y ∪ FY ′ ∪ {ymin − x > 0}x∈X )
16:           I2 ← (Y ′ ∪ Z, CY ∪Z ∪ FY ′ ∪ {z − ymin > k}z∈Z )
17:           if Solve(I1 ) and Solve(I2 ) then
18:              accept
19:   reject

20: procedure FiveSplit(I = (V, C))
21:   for each 5-partition (S1 , S2 , S3 , S4 , S5 ) of V do
22:     X ← S3 ∪ S4 ∪ S5
23:     if |S1 |, |S5 | < |V3 | and |S2 |, |S4 | ≤ log|V|V| | and
24:        (x − s1 > k) ∈ σC (s1 , x) for s1 ∈ S1 , x ∈ X and
25:        (s5 − s3 > k) ∈ σC (s3 , s5 ) for s3 ∈ S3 , s5 ∈ S5 then
           // introduce fresh variables smin    2   and smin  4
26:        S2′ = S2 ∪ {smin 2   }
27:        S4′ = S4 ∪ {smin 4 }
28:        IS2′ ← (S2′ , CS2 ∪ {0 ≤ s2 − smin   2   < k}s2 ∈S2 )
                        ′                       min
29:        IS4 ← (S4 , CS4 ∪ {0 ≤ s4 − s4 < k}s4 ∈S4 )
              ′

30:        for FS2′ ∈ ListCert(IS2′ ) and
31:             FS4′ ∈ ListCert(IS4′ ) do
32:           I1 ← (S1 ∪ S2′ , CS1 ∪S2 ∪ FS2′ ∪ {smin    2    − s1 > 0}s1 ∈S1 )
33:           I2 ← (S2′ ∪ S3 ∪ S4′ , CS2 ∪S3 ∪S4 ∪ FS2′ ∪ {s3 − smin   2   > k}s3 ∈S3 ∪
                                 min
                      FS4 ∪ {s4 − s3 > 0}s3 ∈S3 )
                          ′

34:           I3 ← (S4′ ∪ S5 , CS4 ∪S5 ∪ FS4′ ∪ {s5 − smin      4  > k}s5 ∈S5 )
35:           w ← k(log |V | + 2)
36:           if Solve(I1 ) and Solve(I3 ) and
37:              SolveBounded(w, I2 ) then
38:              accept
39:   reject


by the check on line 24, Condition 2 is ensured since both subinstances I1 and I2 satisfy all constraints
in FS2′ , and Conditions 3 and 4 are ensured by the introduction of smin
                                                                     2   and the constraints involving it.
Hence, we have showed that I is satisﬁable.


                                                           19
   We proceed by proving the other direction: if I is satisﬁable with satisfying assignment ϕ, then the
algorithm accepts it. Lemma 12 implies that ϕ splits the instance as in Case 1 or 2.
Case 1. We show that ThreeSplit accepts I. The procedure enumerates every 3-partition of the
variables, so at some step of the algorithm X = Li , Y = Vi and Z = Ri , where (Li , Vi , Ri ) is the split
under the assignment ϕ according to Lemma 12 Case 1. We set ϕ(ymin ) = ki − k and observe that
ϕ satisﬁes instances in Lines 13, 15 and 16. Note that the procedure Solve accepts I1 and I2 by the
inductive hypothesis.
Case 2. We show that FiveSplit accepts I. The procedure enumerates every 5-partition of the variables,
so at some step of the algorithm S1 = Li , S2 = Vi , S3 = Ri ∩Lj , S4 = Vj and S5 = Rj , where (Li , Vi , Ri ∩
Lj , Vj , Rj ) is the split under the assignment ϕ according to Lemma 12 Case 2. We set ϕ(smin 2 ) = ki − k
and ϕ(smin 4   ) =  kj −  k  and observe that ϕ satisﬁes the instances in Lines 28, 29, 32, 33 and 34. Note
that the procedure Solve accepts I1 and I3 by the inductive hypothesis. By Lemma 12, all subsets in
Ri ∩ Lj are dense. Since each of them contains at least n/log n variables, there may be at most log n
such subsets. Taking Vi and Vj into account, we conclude that ϕ satisﬁes instance I2 with span at most
k(log n + 2). This completes the correctness proof.

Time complexity. Let T (n) be the running time of Algorithm 1 on an instance of CSP(D2,k ) with n
variables. We claim that T (n) ≤ cn (log n + 2)n = 2O(n log log n) for some constant c. If n < 8, then T (n)
is constant. Otherwise, T (n) = T1 (n) + T2 (n) + poly(n), where T1 and T2 are the running times of the
procedures ThreeSplit and FiveSplit, respectively. Note that T1 (n) < T2 (n) for all n, so we can focus
our attention on the running time of FiveSplit.
    The running time T2 (n) is bounded from above by 5n · 22n · (2T ( n3 + 1) + (k(log n + 2))n ) · poly(n),
where 5n is an upper bound on the number of 5-partitions of V , 22n comes from the upper bound on the
running time of the calls to ListCert in lines 30 and 31, 2T ( n3 + 1) is an upper bound on the running
time of the recursive calls in line 36, and (k(log n+ 2))n comes from the running time of the bounded-span
algorithm SolveBounded in line 37 (see Lemma 9). Observe that for suﬃciently large values of n we
                                 εn
have (log n + 2)n > α log (εn) for arbitrary α ≥ 0 and 0 ≤ ε < 1. Hence, (k(log n + 2))n asymptotically
dominates 2T ( n3 + 1) by our initial hypothesis. Finally, observe that

                                   T (n) < 2 · (40k)n · (log n + 2)n · poly(n).

Setting c = 81k completes the proof.


4      Lower Bounds on Time Complexity
This section contains our time complexity lower bound results for various subclasses of CSP(D). The
full picture of upper and lower bounds on time complexity is summarized in Table 2. The majority of
our lower-bound results are based on reductions from the n × n Independent Set problem.

    n × n Independent Set
     Input:      A graph G = (V, E) with vertex set V = {(i, j) : 1 ≤ i ≤ n, 1 ≤ j ≤ n}.
     Question:   Is there an independent set in G with one vertex from each row, i.e.,
                 subset of vertices {(1, j1 ), . . . , (n, jn )} where no pair of vertices is con-
                 nected by an edge?

     Lokshtanov et al. [56] have proved the following result.
Theorem 14. n × n Independent Set cannot be solved in 2o(n log n) time unless the ETH fails.
    We begin by proving lower bounds for CSP(Da,0 ) when a ≥ 4. Note that CSP(D≤
                                                                               a,0 ) is trivially in P
for every a ≥ 0 so this result cannot be extended to CSP(D≤
                                                          a,0 ).

Theorem 15. CSP(D4,0 ) cannot be solved in 2o(n log n) time unless the ETH fails.

                                                         20
Proof. We reduce from n × n Independent Set. Given an instance G of this problem, do the following.

   1. Introduce n column variables c1 , . . . , cn and the constraints ci < ci−1 for all i ∈ {2, . . . , n}.
   2. Introduce n row variables r1 , . . . , rn . To ensure that each ri is equal to one of the column variables,
      add the following constraints: c1 ≤ ri , ri ≤ cn and (ri ≤ cj−1 ) ∨ (ri ≥ cj ) for all j ∈ {2, . . . , n}.
   3. No pair of vertices (i, j) and (k, ℓ) adjacent in G can be simultaneously included in the independent
      set. To ensure this property, we add the following constraint:

                                           (ri < cj ) ∨ (ri > cj ) ∨ (rk < cℓ ) ∨ (rk > cℓ ).

    The resulting set of constraints only use relations in CSP(D4,0 ). The correctness of the reduction
is easy to verify: If G has an independent set I, than setting ri = cj for all (i, j) ∈ I satisﬁes all
constraints of the instance above, and vice versa. The reduction requires polynomial time and introduces
2n variables. Thus, if CSP(D4,0 ) admits a 2o(n log n) algorithm, then so does n × n Independent Set
and this contradicts the ETH by Theorem 14.
    A slightly weaker bound can be inferred from Theorem 11 in [48]: if the randomized ETH holds, then
there is no randomized algorithm for CSP(D4,0 ) that runs in O(cn ) time for any c ≥ 0. We continue by
studying CSP(D≤   3,1 ). We use Sidon sets in the proof so the reader may want to skip back to Section 2.3
for a reminder.
Theorem 16. CSP(D≤
                 3,1 ) is not solvable in 2
                                            o(n log n)
                                                       time if the ETH holds.
Proof. The proof is by a reduction from n × n Independent Set. Assume G = (V, E) to be an arbitrary
instance of this problem with r rows. We use the results from Section 2.3 and construct (in polynomial
time) a Sidon set S = {a0 , . . . , ar } where 0 = a0 < a2 < · · · < ar and ar ≤ 8r2 . We present the rest of
the reduction in three steps.

   1. Introduce ar fresh variables y0 , . . . , yar and use the relation y = x+1 for enforcing yi = i, 0 ≤ i ≤ ar .
   2. Introduce one variable xr for each row r. We ﬁrst ensure that the range of each variable is in
      {0, . . . , yar } by adding the constraint

                                               xr ≤ ai − 1 ∨ xr = ai ∨ xr ≥ ai + 1

      for each 1 ≤ i ≤ ar together with the constraints x ≥ 0 and x ≤ yar . Next, we restrict the range to
      be in S by adding the constraint
                                            x ≤ ys − 1 ∨ x ≥ ys + 1
      for each s ∈ {0, . . . , ar } \ S.
   3. Let R(x, y, z) denote the relation x − y 6= z, i.e. R(x, y, z) ≡ (x − y < z) ∨ (y − x < z). For every
      edge ((c, c′ ), (d, d′ )) ∈ E, compute e = ac′ − ad′ and add the constraint R(xc , xd , ye ).

The resulting set of constraints only use relations in CSP(D≤      3,1 ) This reduction can be performed in
polynomial time. Steps 1. and 2. take polynomial time since ar ≤ 8r2 ≤ 8||G||2 and step 3. can
obviously performed in polynomial time in the size p    of E. Let (V ′ , C ′ ) denote the resulting instance of
                               ′    2
CSP(D3,1 ). We see that |V | ≤ 8r + r ≤ 8|V | + ⌈ |V |⌉ ≤ 9|V |. Thus, if (V ′ , C ′ ) is satisﬁable if and
only if G is a yes-instance, then CSP(D3,1 ) is not solvable in 2o(n log n) time by Theorem 14. We conclude
the proof by proving this equivalence.
Forward direction. Assume f is a solution to (V ′ , C ′ ). We claim that for every 1 ≤ c 6= d ≤ r, it holds
that ((c, f (c)), (d, f (d))) is not in E and G is a yes-instance. Assume to the contrary that c, d can be
chosen such that ((c, f (c)), (d, f (d))) ∈ E. This edge implies that there is a constraint R(xc , xd , ye ) ∈ C ′
where e = af (c) − af (d) . Hence,


                                                               21
                                             f (xc ) − f (xd ) 6= f (ye ) ⇒
                                            ac′ − ad′ 6= af (c) − af (d) ⇒
                                                ac′ − ad′ 6= ac′ − ad′
   and we have reached a contradiction.
Backward direction. Assume X = {v1 , . . . , vr } ⊆ V is an independent set and vi occurs in position
(i, i′ ), 1 ≤ i, i′ ≤ r. Deﬁne the assignment f such that f (xi ) = ai′ , 1 ≤ i ≤ r, and f (yi ) = i, 0 ≤ i ≤ ar .
This assignment satisﬁes all constraints introduced in step 2.
     Arbitrarily choose an edge ((c, c∗ ), (d, d∗ )) ∈ E. It gives rise to the constraint R(xc , xd , ye ) where
e = (ac∗ − ad∗ ). We know that ((c, c′ ), (d, d′ )) is a non-edge in E since (c, c′ ) = vc , (d, d′ ) = vd , and vc , vd
are in the independent set X. The constraint R(xc , xd , ye ) is equivalent to xc − xd 6= ye . We apply the
assignment f to it:

                                          f (xc ) − f (xd ) 6= f (yac∗ −ad∗ ) ⇒
                                                ac′ − ad′ 6= ac∗ − ad∗
    We know that ((c, c′ ), (d, d′ )) is a non-edge in E while ((c, c∗ ), (d, d∗ )) is an edge in E. Hence, ac′ 6= ac∗
or ad′ 6= ad∗ . Recall that for all w1 , . . . , w4 ∈ S such that w1 6= w2 and w3 6= w4 , w1 − w2 = w3 − w4
if and only if w1 = w3 and w2 = w4 . Thus, if ac′ 6= ad′ and ac∗ 6= ad∗ , then the disequality holds. If
ac′ = ad′ , then ac∗ 6= ad∗ (since ((c, c′ ), (d, d′ )) 6∈ E and ((c, c∗ ), (d, d∗ )) ∈ E) and we conclude that the
disequality holds. The case when ac∗ = ad∗ is symmetric.
   Our ﬁnal lower bound based on a reduction from n × n Independent Set concerns the problem
CSP(D6 2 ). Since there is no upper bound on the coeﬃcients in this case, the lower bound is parameterized
both by the number of variables and the maximum over the coeﬃcients.
Theorem 17. CSP(D6
                 2 ) is not solvable in 2
                                          o(n(log n+log k))
                                                            time if the ETH holds.
Proof. The proof is by reduction from n × n Independent Set. Given an instance G of this problem,
we introduce a zero variable z and two variables xr , x′r for each row r. We add the following constraints:
      Wn
  1. i=1 xr − z = i for every row r,
      Wn                         Wn
  2. i=1 x′r − xr = ni − i and i=1 x′r − z = ni for every row r,
   3. x′a − xb ∈ (−∞, ni − j − 1] ∨ x′a − xb ∈ [ni − j + 1, ∞) for every edge {(a, i), (b, j)} in G.
Constraints of the ﬁrst type restrict the domain of xr to {1, . . . , n}. Constraints of the second type
ensure that x′r = nxr . Constraints of the third type ensure are equivalent to x′a − xb 6= ni − j, which
forbids setting xa = i and xb = j. Furthermore, function f : {1, . . . , n} × {1, . . . , n} → {0, . . . , n2 − 1}
deﬁned as f (i, j) = ni − j is bijective, so x′a − xb 6= ni − j is satisﬁed by every other choice of values, i.e.
whenever xa 6= i or xb 6= j. Thus, the resulting instance of CSP(D6       2 ) has a solution if and only if G has
an independent set with one variable per row. The total number of variables in the resulting instance is
2n + 1 and the absolute values of the integers appearing in the constraints do not exceed n2 . Thus, an
algorithm solving CSP(D6   2 ) in 2
                                    o(n(log n+log k))
                                                      time can be used for solving n × n Independent Set in
                                                                2
                                         2o(n(log (2n+1)+log n )) = 2o(n log n)

time and this contradicts the ETH by Theorem 14.




                                                           22
    Our ﬁnal lower bound for CSP(D2,k ) relies on a modiﬁcation of a result by Traxler [77]. Let d-CSP be
the constraint satisfaction problem with domain D = {1, . . . , d} and binary relations Ra,b = (x 6= a ∨ y 6= b)
for all a, b ∈ D. Note that this relation is akin to the binary relation in our reductions from (n × n) Inde-
pendent Set that is used to forbid choosing an edge. We cannot use the same reduction here because
the numerical bound k is ﬁxed. Indeed, a 2o(n log n) lower bound for this problem stands in contradiction
with Theorem 13 or the ETH. For our reductions, we consider a modiﬁed version of d-CSP denoted by
d-CSPχ . It allows binary relations
                                  χ                        V
                               Ra,b  = (x 6= a ∨ y 6= b) ∧ c∈D (x 6= c ∨ y 6= c)
for all a, b ∈ D. For convenience, we consider the constraints that rule out (c, c) tuples (i.e. the right-
hand side constraints in the deﬁnition above) separately, and assume the following rule: if an instance
of d-CSPχ includes a constraint (x 6= a ∨ y 6= b), then it implicitly includes the required constraints
(x 6= c ∨ y 6= c) for all c ∈ D. Additionally, we allow unary relations x 6= a for all a ∈ D.
Lemma 18. For any r ∈ N and any instance of d-CSPχ with n variables, there exists an equivalent
instance of dr -CSPχ with ⌈n/r⌉ variables.
Proof. Let I = (V, C) be an instance of d-CSPχ with |V | = n. Augment V with at most r − 1 extra
variables so that its new size n′ becomes a multiple of r. Partition V into ℓ = n′ /r = ⌈n/r⌉ disjoint
subsets V1 , . . . , Vℓ of equal size and index the elements of each subset arbitrarily.
     The set of tuples Dr represents all assignments to the variables in a subset Vi . For convenience, we
use the tuples directly as the domain of dr -CSPχ . Deﬁne an instance I ′ = (V ′ , C ′ ) of dr -CSP as follows.
For each subset Vi in the partition introduce a variable zi to V ′ . Note that |V ′ | = ℓ.
     First, consider a unary constraint x 6= a in C. Assume x ∈ Vi and ix is the index of x in Vi . Add
constraints zi 6= t to C ′ for all t ∈ Dr such that tix = a. Now consider a binary constraint (x 6= a)∨(y 6= b)
in C. Assume x ∈ Vi , y ∈ Vj and ix , jy are the indices of x, y in the respective subsets. If i 6= j, then add
constraints (zi 6= s ∨ zj 6= t) for all tuples s, t ∈ Dr such that six = a and tjy = b. If i = j (index of y is
iy ), add unary constraints zi 6= t for all t such that tix = a and tiy = b.
     Observe that the required constraints (x 6= c ∨ y 6= c) for all c ∈ D are converted into (zi 6= s ∨ zj 6= t)
for every pair of tuples s, t ∈ Dr that coincide in at least one position. Clearly, this includes the case
when s and t are equal. Hence, I ′ is an instance of dr -CSPχ . Proving the equivalence of I and I ′ is
analogous to the proof of Lemma 1 in [77].
   We are now ready to prove the lower bound.
Theorem 19. If we assume that the ETH holds, then for arbitrary m > 0 there is an integer k such that
any algorithm solving CSP(D≤                        ∗  n
                           2,k ) requires at least O (m ) time.

Proof. We start by proving that the time complexity of d-CSPχ increases with d assuming the ETH. Let
                     cd = inf{c ∈ R : there is a 2cn -time algorithm solving d-CSPχ }.

We show that limd→∞ cd = ∞. The 3-Colourability problem cannot be solved in subexponential time
assuming the ETH [46]. 3-CSPχ is a generalization of 3-Colourability so c3 > 0. By Lemma 18, for
any r ∈ N we have c3r ≥ c3 · r. Observe that limr→∞ c3 · r = ∞, so limd→∞ cd = ∞.
   Next, we show that for any instance of d-CSPχ with n variables there is an equivalent instance of
CSP(D≤                                           2                                    χ
        2,k ) with n + 1 variables and k ∈ O(d ). Let I be an instance of d-CSP with n variables.
                          ′
Construct an instance I of CSP(D2,k ) as follows. Choose k so that {−k, . . . , k} contains a Sidon set of
order d as a subset. One can choose such a k to be in O(d2 ) by Section 2.3. Denote the corresponding
Sidon set by Gd . Associate each integer in {1, . . . , d} with a unique element of Gd via the bijection
ρ : {1, . . . , d} → Gd . Introduce zero variable z to express unary relations. For each variable x in
I introduce a new variable vx . WDeﬁne Ex = {ρ(c) : (x 6= c) ∈ C}. Restrict the domain of vx to
Dx = Gd \ Ex by the constraint i∈Dx vx − z ∈ {i}. Any constraint (x 6= a ∨ y 6= b) can be expressed by
enforcing vx − vy 6= δ where δ = ρ(a) − ρ(b). This is done by adding the constraint

                                vx − vy ∈ (−∞, δ − 1] ∨ vx − vy ∈ [δ + 1, ∞).

                                                       23
                       a
                                                                           c, d, f
                             c      d
                   b                                             b, c, f              d, f, g

                                                       a, b, c             b, e, f     g, h
                       e     f      g      h

                Figure 1: A graph (left) and an optimal tree decomposition of the graph (right).


By the properties of Sidon sets, this constraint is satisﬁed if and only if x 6= ρ(a) or y 6= ρ(b).
   The reduction introduces only one extra variable and the lower bound on d-CSPχ carries over to
CSP(D≤ 2,k ).



5     Parameterized Upper Bounds
The results in Section 4 imply that most subproblems of CSP(D) cannot be solved in subexponential time
under the ETH. This is a strong motivation for analyzing the problems from a parameterized perspective.
A highly successful approach for identifying tractable fragments of CSPs is to restrict variable-constraint
interactions via the underlying primal and incidence graphs. The primal graph has the variables as its
vertices with any two joined by an edge if they occur together in a constraint. The incidence graph is
the bipartite graph with two disjoint sets of vertices corresponding to the variables and the constraints,
respectively, and a constraint vertex and a variable vertex are joined by an edge if the variable occurs
in the scope of the constraint. The treewidth of such graphs has been used extensively and it has been
successfully employed for many application areas. In particular, it has been used for problems such as
SAT, CSP, and ILP [11, 13, 34, 40, 41, 45, 70]. Formal deﬁnitions and some auxiliary results are collected
in Section 5.1.
    The results in this section (together with the lower bound results that will be proved in Section 6) are
summarized in Table 3. The main result is an XP algorithm for CSP(D∞,k ), k < ∞, where the parameter
is the treewidth of the incidence graph. This algorithm is presented in Section 5.2. The treewidth of the
incidence graph cannot be larger than the treewidth of the primal graph plus one so tractability results
are more general if they hold for incidence treewidth and hardness results are more general if they hold
for primal treewidth.

5.1     Treewidth
Treewidth is based on tree decompositions [8, 69]: a tree decomposition (T, χ) of an undirected graph
G = (V, E) consists of a rooted tree T and a mapping χ from nodes V (T ) of the tree to subsets of V .
The subsets χ(t) are called bags. Tt denotes the sub-tree
                                                    S         rooted at t, while χ(Tt ) denotes the set of all
vertices occurring in the bags of Tt , i.e. χ(Tt ) = s∈V (Tt ) χ(s). A tree decomposition has the following
properties:
    1. for every {u, v} ∈ E, there is a node t ∈ V (T ) such that u, v ∈ χ(t), and
    2. for every v ∈ V , the set of bags of T containing v forms a non-empty sub-tree of T .
    An example is given in Figure 1. The width of a tree decomposition T is max{|χ(t)| − 1 : t ∈ T }.
The treewidth of a graph G, denoted by tw(G), is the minimum width of a tree decomposition of G. It
is NP-complete to determine if a graph has treewidth at most w [4] but when w is ﬁxed, the graphs
with treewidth w can be recognized and corresponding tree decompositions can be constructed in linear
time [16].



                                                      24
                                                                        ∅

                                                                        a

                              a
                                                                 a                 a


                             a, c                               a, b         a          a
                  a, b                 a, d

                                                                 b          a, c       a, d
                   b, e
                                                                b, e         c          d

                                                                 e           ∅          ∅


                                                                 ∅


          Figure 2: A tree decomposition (left) and a corresponding nice tree decomposition (right).


    We simplify the presentation by using restricted tree decompositions. A tree decomposition is nice if
(1) χ(r) = ∅ for the root r and |χ(l)| = 1 and for all leaf nodes l in T , and (2) every non-leaf node in T
is of one of the following types:
   • An introduce node: a node t with exactly one child t0 such that χ(t) = χ(t0 ) ∪ {v} for some v ∈ V .
   • A forget node: a node t with exactly one child t0 such that χ(t) = χ(t0 ) \ {v} for some v ∈ V .
   • A join node: a node t with exactly two children t1 and t2 such that χ(t) = χ(t1 ) = χ(t2 ).
    Nice tree decompositions are illustrated in Figure 2. Note that nice tree decompositions are merely a
structured type of tree decomposition and their only purpose is to simplify the presentation of dynamic
programming algorithms. It is NP-complete to determine if a graph has treewidth at most w [4], but
when w is ﬁxed, then graphs with treewidth w can be recognized and corresponding tree decompositions
can be constructed in linear time.
Proposition 20 (Bodlaender & Kloks [17]; Kloks [51]). Let G = (V, E) be a graph. For fixed w, if G
has treewidth at most w, then a nice tree decomposition of width at most w with O(|V |) nodes can be
computed in linear time.
    Let I = (V, C) be an instance of CSP(A). The primal graph of I, denote by P (I), is the graph with
vertices V having an edge between two variables if both appear together in the scope of one constraint.
The incidence graph of I, denote by I(I), is the bipartite graph with V on one side and C on the
other side having an edge between a variable and a constraint if the variable appears in the scope of the
constraint. It is well known that the treewidth of the incidence graph is at most equal to the treewidth of
the primal graph plus one [52] and that the incidence treewidth can be arbitrary smaller than the primal
treewidth. This means that tractability results are more general if they hold for incidence treewidth and
hardness results are more general if they hold for primal treewidth.
    We continue with a few observations concerning treewidth. We discussed in Section 2.2 that zero
variables can be used for simulating unary constraints, and that they do not aﬀect the time complexity
with more than a multiplicative factor. We have a similar situation in the parameterized setting: adding a

                                                     25
zero variable can increase the treewidth of the incidence graph by at most 1 so algorithmic results (such as
the forthcoming Theorem 22) are still valid for this extended formalism. We will use a related observation
when we argue about the treewidth of the graphs obtained in our hardness result (Theorem 33).
Proposition 21 (Bodlaender [16]). Let G be a graph and B ⊆ V (G). Then the treewidth of G is at most
|B| + tw(G − B).

5.2    XP Algorithm for CSP(D∞,k )
We are now ready to present our dynamic programming algorithm for CSP(D∞,k ).
Theorem 22. CSP(D∞,k ) can be solved in (nk)O(w) time, where w is the treewidth of the incidence
graph and n is the number of variables.
    Note that the bound implies that CSP(D) is in XP whenever the numeric values are bounded by a
polynomial in the input size. Proposition 20 implies that the computation of a nice tree decomposition
of the incidence graph does not incur an additional run-time overhead. We may thus assume that a nice
tree decomposition is provided in the input, and it is hence suﬃcient to show the following.
Theorem 23. CSP(D∞,k ) can be solved in time (nk)O(w) provided that a nice tree decomposition of the
incidence graph of width at most w is given as part of the input.
    Let I = (V, C) be an instance of CSP(D∞,k ) with n variables and assume (T, χ) is a nice tree
decomposition of the incidence graph of I of width w. Bags of this decomposition contain vertices
corresponding to both variables and constraints. To distinguish between them, we use varχ (t) to denote
all variables in the bag χ(t) and conχ (t) to denote all constraints in χ(t). These deﬁnitions naturally
extend to the subsets of V (T ). Note that by Theorem 6, we may assume that every solution for I maps
the variables into the set CD = CD(n, k).
    Intuitively, the algorithm behind Theorem 22 works as follows. It uses bottom-up dynamic pro-
gramming on the nodes of T starting from the leaves and ﬁnishing at the root. It computes a compact
representation, represented by a set of valid records, of all solutions to I restricted to the variables and
constraints in χ(Tt ) for every node t ∈ V (T ).
    A record for t ∈ V (T ) is a pair (α, β) where
   • α : varχ (t) → CD is an assignment of values in CD to the variables in varχ (t), and
   • β : conχ (t) → DB , where DB = {S, U }∪{ (v, d) | v ∈ V and d ∈ CD } such that for every constraint
     c ∈ conχ (t) either:
        – β(c) = S signaling that the constraint c is already satisﬁed,
        – β(c) = U signaling that the constraint c is not yet satisﬁed,
        – β(c) = (v, d), where v ∈ scope(c) ∩ (varχ (Tt ) \ varχ (t)) and d ∈ CD , signaling that c is not yet
          satisﬁed, but satisfying c can use the assumption that v is set to d. This also means that c
          will be satisﬁed by satisfying a simple constraint on v and some variable in V \ varχ (Tt ).
Note that there are at most |CD | possible choices for every variable in varχ (t) and at most |V ||CD | + 2
possible choices for every constraint in conχ (t). Therefore, the total number of valid records for t is at
most (|V ||CD | + 2)w+1 .
   For X ∈ {S, U }, deﬁne the inverse β −1 (X) as {c ∈ conχ (t) | β(c) = X} and let

                                  β −1 (F ) = conχ (t) \ (β −1 (S) ∪ β −1 (U )),

i.e. β(c) = (v, d) for some v ∈ V and d ∈ CD for all c ∈ β −1 (F ).
     The semantic of a record is deﬁned as follows. We say that a record (α, β) is valid for t if there is an
assignment τ : varχ (Tt ) → CD such that:

(R1) τ does not satisfy any constraint in Y = conχ (t)\β −1 (S) and satisﬁes all constraints in conχ (Tt )\Y ,

                                                       26
(R2) τ (v) = α(v) for every v ∈ varχ (t), and
(R3) τ (v) = d holds for every constraint c ∈ conχ (t) with β(c) = (v, d).

    Let R(t) be the set of all valid records for t. Note that I has a solution if and only if R(r) 6= ∅ for
the root r of T since the records in R(r) represent solutions for the whole instance. Moreover, once we
have computed the set of records for all nodes, a straightforward application of standard techniques [29]
can be used to obtain a solution for I using a second top-to-bottom run through the tree-decomposition.
    Next, we will show that R(t) can be computed via a dynamic programming algorithm on (T, χ) in
a bottom-up manner. The algorithm starts by computing the set of all valid records for the leaves of
T and then proceeds by computing the set of all valid records for the other three types of nodes of a
nice tree-decomposition (always selecting nodes all of whose children have already been processed). The
following lemmas show how this is achieved for the diﬀerent types of nodes of (T, χ).
Lemma 24 (variable leaf node). Let t ∈ V (T ) be a leaf node with χ(t) = {v} for some variable v ∈ V .
Then, R(t) can be computed in O(|CD |) time.
Proof. R(t) consists of all records (α, ∅) for every assignment α : {v} → CD , so R(t) can be computed
by enumerating all assignments α : {v} → CD for v in O(|CD |) time. Correctness follows immediately
from the deﬁnition of valid records.
Lemma 25 (constraint leaf node). Let t ∈ V (T ) be a leaf node with χ(t) = {c} for some constraint
c ∈ C. Then, R(t) can be computed in O(1) time.
Proof. R(t) consists of the record (∅, β), where β : {c} → DB is deﬁned by setting β(c) = U . Thus,
R(t) can be computed in constant time and correctness follows immediately from the deﬁnition of valid
records.
Lemma 26 (variable introduce node). Let t ∈ V (T ) be an introduce node with child t0 such that
χ(t) \ χ(t0 ) = {v} for some variable v ∈ V . Then, R(t) can be computed in O(|R(t0 )| · |CD | · |I|) time.
Proof. Informally, the set R(t) is obtained from R(t0 ) by extending every record R0 = (α0 , β0 ) in R(t0 )
with an assignment αv : {v} → CD for the variable v and then updating the record (i.e. updating β0 )
if αv causes additional constraints to be satisﬁed. More formally, for every (α0 , β0 ) ∈ R(t0 ) and every
assignment αv : {v} → CD, the set R(t) contains the record (α, β), where:
   • α(u) = α0 (u) for all u ∈ χ(t0 ) and α(v) = αv (v),
   • β(c) = S for every constraint c ∈ β0−1 (S) ∪ U ′ ∪ F ′ , where:
        – U ′ is the set of all constraints c ∈ β0−1 (U ) that are satisﬁed by the (partial) assignment α and
        – F ′ is the set of all constraints c ∈ β0−1 (F ) that are satisﬁed by setting v to αv (v) and u to d,
          where (u, d) = β0 (c).
   • β(c) = β0 (c) for every other constraint c, i.e. every constraint c ∈ conχ (t) \ (β0−1 (S) ∪ U ′ ∪ F ′ ).
    Towards showing correctness of the deﬁnition for R(t), we ﬁrst show that every valid record R = (α, β)
for t is added to R(t). Because R is valid, there is an assignment τ : varχ (Tt ) → CD satisfying (R1)–
(R3). Let α0 be the restriction of α to varχ (t0 ) and let τ0 be the restriction of τ to varχ (Tt0 ). Let
Z be the set of all constraints in conχ (t) = conχ (t0 ) that are satisﬁed by τ but not satisﬁed by τ0 .
Moreover, let X ⊆ Z contain the constraints that are satisﬁed by α and set Y = Z \ X. Then, for every
constraint c ∈ Y , there is (at least one) variable, denoted by y(c), in varχ (Tt ) \ varχ (t) such that the
partial assignment setting y(c) to τ (y(c)) and setting v to α(v) satisﬁes c. This implies that the record
R0 = (α0 , β0 ) deﬁned by setting β0 (c) = β(c) for every c ∈ conχ (t0 ) \ (X ∪ Y ), β0 (c) = U for every c ∈ X,
and β0 (c) = (y(c), τ (y(c))) for every c ∈ Y is contained in R(t0 ). Finally, U ′ = X and F ′ = Y holds for
the record R0 , so R is added to R(t).



                                                       27
    It remains to show that if a record R = (α, β) is added to R(t), then R is valid for t. Suppose that
R is obtained from the record R0 = (α0 , β0 ) ∈ R(t0 ). There is an assignment τ0 : varχ (Tt0 ) → CD
satisfying (R1)–(R3) since R0 is valid for t0 . Now it is straightforward to verify that the extension τ of
τ0 obtained by setting τ (v) = α(v) witnesses that R is a valid record.
    Finally, the run-time of the procedure follows because there are |R(t0 )| · |CD | pairs of records in
R(t0 ) and assignments αv for v. Computing the record for one such combination requires evaluating the
constraints in conχ (t) for partial assignments and thus takes O(|I|) time.
Lemma 27 (constraint introduce node). Let t ∈ V (T ) be an introduce node with child t0 such that
χ(t) \ χ(t0 ) = {c} for some constraint c ∈ C. Then, R(t) can be computed in O(|R(t0 )||I|) time.
Proof. Informally, the set R(t) is obtained from R(t0 ) by checking, for every record (α0 , β0 ) ∈ R(t0 ),
whether α0 satisﬁes the constraint c and if so, extending β0 by setting c to being satisﬁed, and if not,
extending β0 by setting c to being unsatisﬁed. More formally, for every record (α0 , β0 ) ∈ R(t0 ):
   • if the constraint c is satisﬁed by the partial assignment α0 , then R(t) contains the record (α0 , β),
     where β is the extension of β0 that sets c to S.
   • otherwise, i.e. if α0 does not satisfy c, then R(t) contains the record (α0 , β), where β is the extension
     of β0 that sets c to U .
Towards showing correctness of the deﬁnition for R(t), we ﬁrst show that every valid record R = (α, β)
for t is added to R(t). Because R is valid, there is an assignment τ : varχ (Tt ) → CD satisfying (R1)–(R3).
Because (T, χ) is a tree decomposition, it follows that the scope of c does not contain any variable from
varχ (Tt ) \ varχ (t); otherwise the edge between c and the variable in varχ (Tt ) \ varχ (t) in the incidence
graph is not contained in any bag of T . Therefore, β(c) ∈ {S, U } so if β(c) = S, then c is already satisﬁed
by the partial assignment α. It follows that τ witnesses that the record (α, β0 ), where β0 is the restriction
of β to conχ (t′ ), is in R(t0 ) and R is added to R(t).
    It remains to show that if a record R = (α, β) is added to R(t), then R is valid for t. Assume that R is
obtained from the record R0 = (α, β0 ) ∈ R(t0 ). We know that R0 is valid for t0 so there is an assignment
τ0 : varχ (Tt0 ) → CD satisfying (R1)–(R3). Because (T, χ) is a tree decomposition, it follows that the
scope of c does not contain any variable from varχ (Tt ) \ varχ (t). Hence, β(c) ∈ {S, U } so if β(c) = S,
then c is already satisﬁed by the partial assignment α. Therefore, τ witnesses that R is valid.
    Finally, the run-time follows because we have to consider every record (α0 , β0 ) in R(t0 ) and we can
check in O(|I|) time whether α satisﬁes c or not.
Lemma 28 (variable forget node). Let t ∈ V (T ) be a forget node with child t0 such that χ(t0 ) \ χ(t) =
{v} for some variable v ∈ V . Then, R(t) can be computed in O(|R(t0 )|2w w) time.
Proof. Informally, R(t) is obtained from R(t0 ) by restricting α0 of every record (α0 , β0 ) ∈ R(t0 ) to
varχ (t), but allowing the assignment that sets v to α0 (v) to satisfy any set of yet unsatisﬁed constraints
in β0−1 (U ) that have v in their scope. More formally, for every record (α0 , β0 ) ∈ R(t0 ) and every subset
U ′ of β0−1 (U ) ∩ { c ∈ C | v ∈ scope(c) }, the set R(t) contains the record (α, β), where α is the restriction
of α0 to varχ (t) and β is deﬁned by setting β(c) = β0 (c) for every c ∈ conχ (t) \ U ′ and β(c) = (v, α0 (v))
for every c ∈ U ′ .
    Towards showing the correctness of the deﬁnition for R(t), we ﬁrst show that every valid record
R = (α, β) for t is added to R(t). Because R is valid, there is an assignment τ : varχ (Tt ) → CD satisfying
(R1)–(R3). Let X be the set of all constraints c in conχ (t) such that β(c) = (v, d). We know that τ
satisﬁes (R3) so d = τ (v) for all constraints in X. Then, τ witnesses validity of the record R0 = (α0 , β0 ),
where α0 is the extension of α setting v to τ (v) and β0 is obtained from β by setting β0 (c) = U for every
c ∈ X. Now, the record R0 together with the set U ′ = X shows that R is added to R(t).
    It remains to show that if a record R = (α, β) is added to R(t), then R is valid for t. Assume that R is
obtained from the record R0 = (α0 , β0 ) ∈ R(t0 ). Then, because R0 is valid for t0 , there is an assignment
τ0 : varχ (Tt0 ) → CD satisfying (R1)–(R3). Moreover, the assignment τ0 witnesses the validity of R.
Finally, the run-time follows because there are at most |R(t0 )|2w pairs of a record in R(t0 ) and a subset
U ′ and the time required to compute a record for such a pair is at most O(w).

                                                      28
Lemma 29 (constraint forget node). Let t ∈ V (T ) be a forget node with child t0 such that χ(t0 )\χ(t) =
{c} for some constraint c ∈ C. Then, R(t) can be computed in O(|R(t0 )||χ(t)|) time.
Proof. Informally, R(t) is obtained from R(t0 ) by taking all records (α0 , β0 ) in R(t0 ) that satisfy c and
restricting β0 to conχ (t). More formally, for every record (α0 , β0 ) ∈ R(t0 ) such that β0 (c) = S, R(t)
contains the record (α0 , β), where β is the restriction of β0 to conχ (t).
    Towards showing the correctness of the deﬁnition for R(t), we ﬁrst show that every valid record
R = (α, β) for t is added to R(t). Because R is valid, there is an assignment τ : varχ (Tt ) → CD satisfying
(R1)–(R3). Because τ satisﬁes (R1), it also satisﬁes the constraint c. Therefore the record R0 = (α, β0 ),
where β0 is the extension of β to c by setting β0 (c) = S, is valid and hence R0 ∈ R(t0 ). Therefore, R is
added to R(t).
    It remains to show that if a record R = (α, β) is added to R(t), then R is valid for t. Assume that R is
obtained from the record R0 = (α0 , β0 ) ∈ R(t0 ). Then, because R0 is valid for t0 , there is an assignment
τ0 : varχ (Tt0 ) → CD satisfying (R1)–(R3). Moreover, from the deﬁnition of R(t), we obtain that τ0
satisﬁes c so τ0 witnesses that R is valid.
    Finally, the run-time estimate is correct because it takes O(|χ(t)|) time to check whether β0 (c) = S
and to compute the restriction of β to conχ (t) for a record (α0 , β0 ) in R(t0 ).
Lemma 30 (join node). Let t ∈ V (T ) be a join node with children t1 and t2 , where χ(t) = χ(t1 ) = χ(t2 ).
Then, R(t) can be computed in O(|R(t1 )||R(t2 )||I|) time.
Proof. Informally, R(t) is obtained from R(t1 ) and R(t2 ) by combining all pairs of records (αi , βi ) in
R(ti ) that agree on the assignments αi to a new record and updating the set of satisﬁed constraints. More
formally, we say that two records (α1 , β1 ) ∈ R(t1 ) and (α2 , β2 ) ∈ R(t2 ) are compatible if α1 = α2 and for
every constraint c ∈ conχ (t) such that for i ∈ {1, 2}, βi (c) = (vi , di ), and the partial assignment setting
vi to di satisﬁes c. Then, for every pair of compatible records (α1 , β1 ) ∈ R(t1 ) and (α2 , β2 ) ∈ R(t2 ), the
set R(t) contains the record (α, β), where:
   • α = α1 = α2 and
   • β(c) = S if either:
        – β1 (c) = S or β2 (c) = S or
        – β1 (c) = (v1 , d1 ) and β2 (c) = (v2 , d2 ) and the (partial) assignment setting v1 to d1 and v2 to d2
          satisﬁes c.
   • β(c) = U if β1 (c) = U and β2 (c) = U ,
   • β(c) = (v, d) if either:
        – β1 (c) = (v, d) and β2 (c) = U or
        – β1 (c) = U and β2 (c) = (v, d)
    We will now show the correctness of the deﬁnition of R(t). We ﬁrst show that every valid record R =
(α, β) for t is added to R(t). Because R is valid, there is an assignment τ : varχ (Tt ) → CD satisfying (R1)–
(R3). Let τi be the restriction of τ to varχ (Tti ). Note ﬁrst that every constraint c ∈ conχ (Tt ) \ conχ (t),
is either satisﬁed by τ1 or by τ2 . This is because (T, χ) is a tree decomposition so scope(c) ⊆ varχ (Tti )
for some i ∈ {1, 2}. Moreover, every constraint c ∈ conχ (t) that is satisﬁed by τ is either (1) already
satisﬁed by τi (for some i ∈ {1, 2}) or (2) it is satisﬁed by a simple constraint involving two variables
vi ∈ varχ (Ti ) \ varχ (t) assigned according to τ . We set βi (c) = S if c is satisﬁed by τi . Otherwise, we
set βi (c) = U if β(c) = U or β(c) = S, and τ3−i satisﬁes c. Finally, we set βi (c) = (vi , τ (vi )) if either
β(c) = (vi , τ (vi )) and vi ∈ varχ (Tti ) \ varχ (t), or β(c) = S but neither τ1 nor τ2 satisfy c and setting vi
to di satisﬁes c. Then, the records Ri = (α, βi ) are valid for ti as witnessed by τi , so (α, βi ) ∈ R(ti ).
Moreover, R1 and R2 are compatible and R is the result of combining R1 and R2 , showing that R is
added to R(t).


                                                       29
    It remains to show that if a record R = (α, β) is added to R(t), then R is valid for t. Assume that
R is obtained from two compatible records Ri = (α, βi ) ∈ R(ti ). Then, because Ri is valid for ti , there
is an assignment τi : varχ (Tti ) → CD satisfying (R1)–(R3). It is now straightforward to verify that the
assignment τ obtained by combining τ1 and τ2 witnesses that R is valid for t.
    Finally, the run-time follows because there are at most |R(t1 )||R(t2 )| compatible pairs of records and
for every such pair it takes time at most O(|I|) to compute the combined record for R(t).
    We can now conclude the results in this section.
Proof of Theorem 22. The algorithm computes the set of all valid records R(t) for every node t of T using
a bottom-up dynamic programming algorithm starting in the leaves of T . It then solves I by checking
whether R(r) 6= ∅. The correctness of the algorithm follows from Lemmas 24–30. The run-time of the
algorithm is at most the number of nodes of T , which can be assumed to be bounded from above by
O(|I|) (Proposition 20), times the maximum time required to compute R(t) for any of the node types
of a nice tree-decomposition, which is obtained for join nodes with a run-time of O(|R(t1 )||R(t2 )||I|). It
follows that
                                O((|V ||CD | + 2)2(w+1) (|I|)2 ) ∈ (nk)O(w)
is the total run-time because |R(t)| ≤ (|V ||CD | + 2)w+1 .


6     Parameterized Lower Bounds
This section contains two main results: we show that CSP(D2,∞ ) is pNP-hard (Section 6.1) and that
CSP(D2,1 ) is W[1]-hard (Section 6.3) when parameterized by primal treewidth. These results indicate
that there is no fpt algorithm for CSP(D2,k ), k ∈ {1, 2, . . . } ∪ {∞}, under standard complexity-theoretic
assumptions. The pNP-hardness result is proved by a direct reduction from Subset Sum while the
W[1]-hardness result is based on a reduction from a variant of the Subset Sum problem that we call
Multi-Dimensional Partitioned Subset Sum. W[1]-hardness for the latter problem is proved in
Section 6.2. The full picture of parameterized upper and lower bounds is summarized in Table 3.
    To present our results, we need some additional technical machinery. A parameterized problem is,
formally speaking, a subset of Σ∗ × N where Σ is the input alphabet. Reductions between parameterized
problems need to take the parameter into account. To this end, we will use parameterized reductions (or
fpt-reductions). Let L1 and L2 denote parameterized problems with L1 ⊆ Σ∗1 × N and L2 ⊆ Σ∗2 × N. A
parameterized reduction from L1 to L2 is a mapping P : Σ∗1 × N → Σ∗2 × N such that
 (1) (x, k) ∈ L1 if and only if P ((x, k)) ∈ L2 ,
 (2) the mapping can be computed by an fpt-algorithm with respect to the parameter k, and
 (3) there is a computable function g : N → N such that for all (x, k) ∈ L1 if (x′ , k ′ ) = P ((x, k)), then
     k ′ ≤ g(k).
The class W[1] contains all problems that are fpt-reducible to Independent Set parameterized by the
size of the solution, i.e. the number of vertices in the maximum independent set. Showing W[1]-hardness
(by an fpt-reduction) for a problem rules out the existence of a ﬁxed-parameter algorithm under the
standard assumption FPT 6= W[1]. The class pNP contains all parameterized problems that can be solved
by a nondeterministic algorithm in time f (k) · ||x||O(1) for some computable function f . It is known that
FPT = pNP if and only if P = NP. A problem is pNP-hard if it is NP-hard for a constant value of the
parameter.

6.1    pNP-hardness for CSP(D2,∞ )
We show that if there is no upper bound on the size of the numbers used in the constraints, then
CSP(D2,∞ ) is NP-hard, even for instances whose primal graph has constant treewidth. In other words,
we prove that CSP(D2,∞ ) is pNP-hard. This result is based on the NP-hard problem Subset Sum [36].


                                                     30
 Subset Sum
  Input:    A set of integers S and an integer N P
                                                 .
  Question: Is there a set S ′ ⊆ S such that N = s∈S ′ s?

Theorem 31. CSP(D2,∞ ) is NP-hard, even for instances whose primal graph has treewidth at most 2.
Proof. We present a polynomial-time reduction from the Subset Sum problem to CSP(D2,∞ ). Let
(S, N ) be an instance of Subset Sum with S = {s1 , . . . , sn }. We construct an equivalent instance I
of CSP(D2,∞ ) as follows. Introduce n + 1 variables x0 , . . . , xn . For every i with 1 ≤ i ≤ n, introduce
the constraint xi − xi−1 = 0 ∨ xi − xi−1 = si . Finally, add the constraint xn − x0 = N . Note that the
primal graph of I is a cycle, so its treewidth is at most 2. Given a solution to I, selecting those si for
which xi − xi−1 = si yields a subset of S that sums up to N . In the opposite direction, a solution to I
can be constructed from the subset S ′ ⊆ S that sums up to N by setting xi − xi−1 = si if si ∈ S ′ and
xi − xi−1 = 0 otherwise.

6.2    W[1]-hardness for Multi-Dimensional Partitioned Subset Sum
Our parameterized hardness result for CSP(D2,k ) is based on a variant of Subset Sum; we note here that
similar but slightly diﬀerent variants of Subset Sum have beenconsidered before [33, 35]. Let k denote
a natural number and let v̄ denote a vector of dimension K = k2 . We sometimes refer to the coordinates
of v̄ by a pair (a, b) of natural numbers with 1 ≤ a < b ≤ k; here, we implicitly use an arbitrary bijection
between the K pairs (a, b) satisfying the inequality and the K coordinates of the vector v̄. We say that
v̄ is uniform if every non-zero coordinate of v̄ has the same value s(v̄). Finally, for an integer N , we let
N̄ denote the K-dimensional vector that is equal to N at every coordinate.

 Multi-dimensional Partitioned Subset Sum (MPSS)
   Input:       Integers k and N , and sets V1 , . . . , Vk and E1 , . . . , EK of uniform K-
                dimensional vectors over the natural numbers such that:
                   • Every vector v̄ ∈ Vi is non-zero at all coordinates (a, b) such that
                      a = i or b = i and zero elsewhere.
                    • Every vector v̄ ∈ Er is non-zero only at the coordinate r.

   Param.:      k
   Question:    Are
                 Pk there  v̄ 1 , P
                                  . . . , v̄ k and ē1 , . . . , ēK with v̄ i ∈ Vi and ēr ∈ Er such that
                ( i=1 v̄ ) + ( K
                        i                      r
                                      r=1 ē ) = N̄ ?

Theorem 32. MPSS is strongly W[1]-hard (i.e. it is W[1]-hard even if all numbers are encoded in
unary).
Proof. We prove the lemma by a parameterized reduction from Multicoloured Clique, which is well
known to be W[1]-complete [67]. Given an integer k and a k-partite graph G with partition U1 , . . . , Uk ,
the Multicoloured Clique problem asks whether G contains a k-clique (note that since the sets Ui
are independent, any k-clique must contain exactly one vertex from each set Ui ). We let W(i,j) denote
the set of all edges in G with one endpoint in Ui and the other endpoint in Uj , for every i and j with
1 ≤ i < j ≤ k. To show the lemma, we construct an instance

                                         I = (k, N, (Vi )1≤i≤k , (Er )1≤r≤K ),

of MPSS in polynomial time where all integers in I are bounded by a polynomial in |V (G)| and K = k2 .
                                                                                                        

Our construction yields an instance I such that G contains a k-clique if and only if I has a solution.
    We will employ Sidon sets from Section 2.3 in the reduction. Namely, we need a Sidon set containing
|V (G)| natural numbers, i.e. one number for each vertex of G. Since the numbers in the Sidon set will be
used as numbers in I, we need to ensure that the largest of these numbers is bounded by a polynomial


                                                             31
                                                                   V1                     V                              EK
b11       b14 = b21       b24 = b31   bK
                                       1       bK
                                                4         g0V1    g|V1|
                                                                        = g1V2    V
                                                                                 g0 k
                                                                                                         E1
                                                                                         g|Vkk | = g0E1 g|E 1|
                                                                                                                 g0EK   g|E K|




      N               N                    N        M            < TV1                  < TVk    < TE1              < TEK
                      Buckets                       Gap               Garbage for Vi                  Garbage for Er

FigureP3: The board consisting of the bucket part and the garbage part defined in the proof of Theorem 33. Here,
TA = ā∈A s(ā) for A ∈ {V1 , . . . , Vk , E1 , . . . , EK }.


in |V (G)|. We know from Section 2.3 that such a set (where the bound on the largest element is 8|V |2 )
can be computed in polynomial time. In the following, we will assume that we are given such a Sidon
sequence S and we let S(i) denote the i-th element of S for 1 ≤ i ≤ |V (G)|. Let max(S) and max2 (S)
denote the largest element of S and the maximum sum of any two distinct elements in S, respectively.
We will furthermore assume that the vertices of G are identiﬁed with the numbers from 1 to |V (G)| and
therefore S(v) is properly deﬁned for every v ∈ V (G).
    We are now ready to construct the instance I. We set N = max2 (S)+1 and proceed to the construction
of the sets V1 , . . . , Vk and the sets E1 , . . . , EK . For every i with 1 ≤ i ≤ k and every u ∈ Ui , the set Vi
contains the vector ū with s(ū) = S(u) being non-zero at all coordinates (a, b) such that either a = i or
b = i. Moreover, for every 1 ≤ r ≤ K and every e = (u, v) ∈ Wr , the set Er contains the vector ē with
s(ē) = (max2 (S) + 1) − (S(u) + S(v)), and the non-zero value appearing only at coordinate r.
    This completes the construction of I. It is clear that I can be constructed in polynomial time and
that every integer in I is at most max2 (S) + 1 so I is polynomially bounded in |V (G)|. Intuitively,
the construction relies on the fact that since the sum of each pair of vertices is unique, we can uniquely
associate each pair with an edge between these vertices, whose value will then be the global upper bound
of max2 (S) + 1 minus the unique sum.
    It remains to show that G contains a k-clique if and only if I has a solution.
Forward direction. Let C be a k-clique in G with vertices u1 , . . . , uk such that ui ∈ Ui for every i
with 1 ≤ i ≤ k. Choose the vector ūi from Vi , 1 ≤ i ≤ k, and the vector ē(i,j) from E(i,j) , where ē(i,j) is
the edge with endpoints ui and uj for every i and j with 1 ≤ i < j ≤ k. We claim that this choice is a
                                             Pk         PK
solution for I. Let t̄ be the vector ( i=1 ūi ) + ( i=1 ēi ). For every coordinate (i, j) with 1 ≤ i < j ≤ k,
the vectors ūi , ūj , and ē(i,j) are the only vectors that are non-zero at the coordinate (i, j). Therefore,
t̄[(i, j)] = s(ūi ) + s(ūj ) + s(ē(i,j) ). Moreover, using the identities s(ūi ) = S(ui ), s(ūj ) = S(uj ), and
s(ē(i,j) ) = (max2 (S) + 1) − (S(ui ) + S(uj )), we obtain that

                t̄[(i, j)] = S(ui ) + S(uj ) + (max2 (S) + 1) − (S(ui ) + S(uj )) = max2 (S) + 1 = N,

as required.
Backward direction. Assume ūi ∈ Vi , 1 ≤ i ≤ k together with ēj ∈ Ej , 1 ≤ j ≤ K is a solution for I.
We claim that {u1 , . . . , uk } forms a k-clique in G, i.e. e(i,j) = {ui , uj } is an edge of G for every i and j
with 1 ≤ i < j ≤ k. Note that the only vectors in the solution for I that have a non-zero contribution
towards the (i, j)-th coordinate of the sum vector are the vectors ūi , ūj , and ēi,j . Since s(ūi ) = S(ui ),
ūj = S(uj ), and N = max2 (S) + 1, we see that s(ē(i,j) ) = (max2 (S) + 1) − (S(ui ) + S(uj )). Moreover, S
is a Sidon sequence so the sum (S(ui ) + S(uj )) is unique. It follows that e(i,j) = {ui , uj } as required.


6.3       W[1]-hardness for CSP(D2,1 )
We provide a parameterized reduction from MPSS, which together with Theorem 32 establishes the result.
To simplify the reduction, we provide it in two stages. First we show how to construct an equivalent
instance I ′′ of CSP(D2 ) and then we show how to obtain the desired instance I ′ of CSP(D2,1 ) from I ′′ .
    Before giving the formal proof in Theorem 33, let us provide an informal overview of the main
ideas behind the proof. Let I = (k, N, (Vi )1≤i≤k , (Er )1≤r≤K ) be an instance of MPSS. We let our
playing board be the real line; please refer to Figure 3 for an illustration. First, for every vector v̄ in

                                                                 32
        Sk                SK
VE = ( i=1 Vi ) ∪ ( i=1 Ei ) and every non-zero coordinate c of v̄, we introduce a segment on the board
represented by two variables x and y at distance exactly s(v̄) from each other. We divide our board into
two main parts: the bucket part and the garbage part. While the bucket part provides placeholders for
the segments of the vectors chosen to be in a solution for I, the garbage part provides placeholders for
all other segments. Crucial for the idea is a gadget that ensures that a segment can only be in one of
two places, i.e. either its place inside the bucket part or its place inside the garbage part. To illustrate
the idea behind this gadget, suppose one wants to ensure that a variable x is either equal to a variable
a or equal to a variable b. This can be achieved by the ternary constraint x = a ∨ x = b. However,
since we are only allowed to use binary constraints, it becomes more complicated. The idea is that we
additionally ensure that the distance between a and b is between M and 2M − 1 for some number M .
Then we can ensure that x is either equal to a or equal to b by using the constraints x = a ∨ x − a ≥ M
and x = b ∨ b − x ≥ M .
    With this in mind, let us provide some details on the bucket part and the garbage part. The main
idea behind the bucket part is that it provides placeholders for the segments representing the non-zero
coordinates of all vectors that are in the solution for I. More speciﬁcally, consider a solution for I
choosing exactly one vector v̄ i from each Vi and exactly one vector ēr from each Er . Then for every
coordinate r = (i, j), the solution contains exactly three vectors that are non-zero at coordinate r, i.e.
the vector v̄ i , the vector v̄ j , and the vector ēr . Thus, the bucket part will provide three placeholders.
This is achieved by introducing four variables br1 , . . . , br4 for every coordinate r with the idea that, the
place between br1 and br2 is a placeholder for the r-th coordinate of v̄ i , the place between br2 and br3 is
a placeholder the r-th coordinate of v̄j , and the place between br3 and br4 is a placeholder for the r-th
coordinate of ēr . Finally, to verify that the sum of all vectors in the solution is equal to N at each
coordinate r, we introduce the constraint br4 − br1 = N .
    The main function of the garbage part is to ensure two things: (1) if a segment representing a non-
zero coordinate of some vector v̄ in VE is chosen to be in the bucket part, then all segments representing
non-zero coordinates of v̄ are chosen to be in the bucket part and (2) the segments of at least one vector
from every set Vi and every set Er are chosen to be in the bucket part. To achieve this, the garbage
part consists of k + K parts, i.e. one part for every set Vi and one part for every set Er . Moreover, the
part for a set A ∈ {V1 , . . . , Vk , E1 , . . . , EK }, has one placeholder for every vector ā ∈ A, which can hold
all segments representing non-zero coordinates of the vector ā. This is achieved by introducing |A| + 1
variables g0A , . . . , g|A|
                         A
                             such that the place between gi−1  A
                                                                   and giA is reserved to hold all segments of the i-th
vector in A. Here, it is important to recall that every non-zero coordinate of every          P vector v̄ in VE has
                                                                                   A
the same value s(v̄). Finally, we ensure (2) by adding the constraint g|A|            − g0A < ā∈A s(ā) = TA , which
ensures that not all vectors of A can ﬁt into the garbage part. We are now ready to provide the formal
proof.
Theorem 33. CSP(D2,1 ) is strongly W[1]-hard parameterized by primal treewidth.
Proof. Let I = (k, N, (Vi )1≤i≤k , (Er )1≤r≤K ) be an arbitrary instance of MPSS. We start by introducing
the board consisting of the bucket part and the garbage part; see Figure 3 for an illustration.


                                                 xVℓ,ci   s(v̄ℓ )    Vi
                                                                    yℓ,c




                             bc1           bc2    bc3      bc4              Vi
                                                                           gℓ−1       gℓVi
                                           N

Figure 4: Possible ways to place the variables xVℓ,ci and yℓ,c
                                                           Vi
                                                               corresponding to the non-zero coordinate c = (i, j) of
the ℓ-th vector v̄ℓ in Vi .



                                                            33
The bucket part. For every coordinate r (of the vectors in I), where 1 ≤ r ≤ K, we introduce 4 bucket
variables br1 , . . . , br4 and ensure that those appear consecutively in any solution by using the constraints
brl+1 − brl ≥ 0 for every l with 1 ≤ l < 4. We introduce a constraint that ensures that the distance
between br1 and br4 is exactly N , i.e. the constraint br4 − br1 = N . Finally, we arrange the bucket variables
for diﬀerent coordinates in the natural order by introducing the constraints br4 = br+1   1    for every r with
1 ≤ r < K.

The garbage part (for the sets Vi ). For every set Vi = {v̄1 , . . . , v̄|Vi | }, we introduce |Vi | + 1 garbage
variables g0Vi , . . . g|V
                        Vi
                          i|
                             and ensure that those appear consecutively in any solution by using the constraints
 Vi
gl+1  − glVi ≥ 0 for every l with 0 ≤ l < |Vi |. We introduce a constraint that ensures that the distance
between g0Vi and g|V  Vi                                                         Vi
                                                                                      − g0Vi < T . Additionally,
                                              P
                        i|
                           is smaller than T = v̄∈Vi s(v̄), i.e. the constraint g|Vi|
we arrange the garbage variables for diﬀerent sets Vi in the natural order by introducing the constraints
 V         Vi
g0 i+1 = g|V i|
                for every i with 1 ≤ i < k.

The garbage part (for the sets Er ). For every set Ei = {v̄1 , . . . , v̄|Ei | }, we introduce |Ei | + 1 garbage
variables g0Ei , . . . g|E
                        Ei
                           i|
                              and ensure that those appear consecutively in any solution by using the constraints
 Ei
gl+1 − glEi ≥ 0 for every l with 0 ≤ l < |Ei |. We introduce a constraint that ensures that the distance
between g0Ei and g|E  Ei                                                         Ei
                                                                                       − g0Ei < T . Additionally,
                                                P
                        i|
                           is smaller than T = v̄∈Ei s(v̄), i.e. the constraint g|E i|
we arrange the garbage variables for diﬀerent sets Ei in the natural order by introducing the constraints
 E        Ei
g0 i+1 = g|E i|
                for every i with 1 ≤ i < K.
    We ensure that the garbage variables of the sets Ei are placed after the garbage variables of the
                                        Vk
sets Vi by adding the constraint g|V      k|
                                             = g0E1 . Finally, to make the later arguments simpler, we make
                                                                                                          |V |
sure that the last bucket variable bK                                                      i
                                    4 has suﬃcient distance to the ﬁrst garbage variable g0 . We let
                                                  |V1 |
M = K · N + v̄∈VE s(v̄) and add the constraint g0 − bK
              P
                                                         4 = M.


The vector variables for the sets Vi . For every set Vi = {v̄1 , . . . , v̄|Vi | }, every ℓ with 1 ≤ ℓ ≤
|Vi |, and every non-zero coordinate c of v̄ℓ , we introduce two variables xVℓ,ci and yℓ,c  Vi
                                                                                                and the constraint
 Vi      Vi                                                   Vi      Vi
yℓ,c −xℓ,c = s(v̄ℓ ) ensuring that the distance between yℓ,c and xℓ,c is exactly s(v̄ℓ ). We associate one bucket
variable, denoted by B(xVℓ,ci ) and B(yℓ,c  Vi
                                               ), respectively, and one garbage variable, denoted by G(xVℓ,ci ) and
      Vi                         Vi         Vi
G(xℓ,c ), respectively, with xℓ,c and yℓ,c as follows. If c = (i, j) (for some j > i), we set B(xVℓ,ci ) = bc1
            Vi
and B(yℓ,c     ) = bc2 . Otherwise, i.e. if c = (j, i) (for some j < i), we set B(xVℓ,ci ) = bc2 and B(yℓ,c Vi
                                                                                                               ) = bc3 .
                           Vi    c              V                                                 V
Moreover, we set G(xℓ,c ) = gℓ−1      and G(yℓ,ci ) = gℓc . We add constraints that ensure that xℓ,ci is either equal
         Vi             Vi
to B(xℓ,c ) or G(xℓ,c ) (see Figure 4). As we will show later this can be guaranteed by the constraints:

   • xVℓ,ci = B(xVℓ,ci ) ∨ xVℓ,ci − B(xVℓ,ci ) ≥ M and

   • xVℓ,ci = G(xVℓ,ci ) ∨ G(xVℓ,ci ) − xVℓ,ci ≥ M .
                                       Vi                        Vi          Vi
Similarly, we add constraints so that yℓ,c is either equal to B(yℓ,c ) or G(yℓ,c ), i.e. we add the constraints:
      Vi       Vi       Vi       Vi
   • yℓ,c = B(yℓ,c ) ∨ yℓ,c − B(yℓ,c ) ≥ M and
      Vi       Vi         Vi       Vi
   • yℓ,c = G(yℓ,c ) ∨ G(yℓ,c ) − yℓ,c ≥ M.
Let XYV denote the set of all vector variables for the sets Vi , i.e. the set

                    { xVℓ,ci , yℓ,c
                                Vi
                                    | 1 ≤ i ≤ k ∧ 1 ≤ ℓ ≤ |Vi | ∧ c is a non-zero coordinate of v̄ℓi }.




                                                            34
The Vector Variables for the sets Ei . For every set Ei = {ē1 , . . . , ē|Ei | } and every ℓ with 1 ≤
ℓ ≤ |Ei |, we introduce two variables xE
                                       ℓ and yℓ
                                         i       Ei
                                                     and the constraint yℓEi − xE
                                                                                ℓ = s(ēℓ ) ensuring that
                                                                                  i

                        Ei      Ei
the distance between yℓ and xℓ is exactly s(ēℓ ). Similarly, to the vector variables for the sets Vi , we
associate a bucket variable and a garbage variable with xE          Ei                          Ei
                                                           ℓ and yℓ , deﬁned by setting: B(xℓ ) = b3 ,
                                                            i                                            i
    Ei      Ei       Ei    i         Ei      Ei                                         Ei
G(xℓ ) = gℓ−1 , B(yℓ ) = b4 , and G(yℓ ) = gℓ . We add constraints that ensure that xℓ is either equal
to B(xE           Ei
       ℓ ) or G(xℓ ). As we will show later, this is guaranteed by the constraints:
         i



    • xE      Ei     Ei     Ei
       ℓ = B(xℓ ) ∨ xℓ − B(xℓ ) ≥ M and
         i



    • xE      Ei       Ei     Ei
       ℓ = G(xℓ ) ∨ G(xℓ ) − xℓ ≥ M .
         i



Finally, we add constraints that imply that yℓEi is either equal to B(yℓEi ) or G(yℓEi ):

    • yℓEi = B(yℓEi ) ∨ yℓEi − B(yℓEi ) ≥ M and

    • yℓEi = G(yℓEi ) ∨ G(yℓEi ) − yℓEi ≥ M .
We will verify that these constraints have the required properties later on. Let XYE denote the set of all
vector variables for the sets Ei , i.e. the set

                                        { xE    Ei
                                           ℓ , yℓ | 1 ≤ i ≤ K ∧ 1 ≤ ℓ ≤ |Vi | }
                                             i




and let XY = XYV ∪ XYE .
     This completes the construction of the instance I ′′ of CSP(D2 ). We ﬁrst show that the primal
treewidth of I ′′ is at most 4K + 3 and consequently bounded by a function of the parameter k only. Let
B = {bil : 1 ≤ i ≤ K ∧ 1 ≤ l ≤ 4} be the set of all 4K bucket variables and let G be the primal graph of
I ′′ after removing the variables in B. It is straightforward to verify that G has treewidth at most 3 and
we obtain, from Proposition 21, that the primal graph of I ′′ has treewidth at most |B| + 3 = 4K + 3.
     We now show the equivalence of the instances I and I ′′ .
Forward direction. Let v̄i11 , . . . , v̄ikk and ē1j1 , . . . , ēK              ℓ             ℓ
                                                                       jK with v̄iℓ ∈ Vℓ and ējℓ ∈ Eℓ be a solution for I.
Informally, the main idea to obtain a solution for I ′′ is to set the variables xViℓℓ,c and yiVℓℓ,c equal to their
respective bucket variables, i.e. the variables B(xViℓℓ,c ) and B(yiVℓℓ,c ), and similarly for the variables xE            jℓ
                                                                                                                             ℓ


and yjEℓℓ . All other variables in XY are then set to be equal to their respective garbage variables. Since
                                                                         Pk          PK ℓ
v̄i11 , . . . , v̄ikk and ē1j1 , . . . , ēK
                                            jK is a solution for I (and
                                                                                ℓ
                                                                          ℓ=1 v̄iℓ +   ℓ=1 ējℓ = N̄ ), this ensures that the
distance between b1 and b4 is exactly N for every coordinate/bucket r and the distance between g0A and
                               r             r
   A
g|A|     is less than the sum of all vectors in the set A ∈ {V1 , . . . , Vk , E1 , . . . , EK }.
    More formally, we set xViℓℓ,c and yiVℓℓ,c equal to B(xViℓℓ,c ) and B(yiVℓℓ,c ), respectively, for every ℓ with
1 ≤ ℓ ≤ k and every non-zero coordinate c of v̄iℓℓ . Similarly, we set xE                         Eℓ
                                                                                  jℓ and yjℓ equal to B(xjℓ ) and
                                                                                     ℓ                              Eℓ

B(yjEℓℓ ), respectively, for every ℓ with 1 ≤ ℓ ≤ K. For every other variable v in XY, we set v equal to
G(v). Finally, we set giVℓℓ−1 equal to giVℓℓ for every ℓ with 1 ≤ ℓ ≤ k and gjEℓℓ−1 equal to gjEℓℓ for every ℓ
with 1 ≤ ℓ ≤ k. Note that because of the distances between the variables in XY, this already ﬁxes the
position (value) of each variable (up to an additive constant). Note also that all constraints are satisﬁed.
In particular, the constraints bc4 − bc1 = N are satisﬁed because kℓ=1 v̄iℓℓ + K                        ℓ
                                                                             P                  P
                                                                                                  ℓ=1 ējℓ = N̄ . Similarly,
                                                                        A      A
                                                                                         P
for every set A ∈ {V1 , . . . , Vk , E1 , . . . , EK } the constraints g|A| − g0 <            v̄∈A s(v̄) are satisﬁed since
                                                                   1           1
g|A| − g0 = ( v̄∈A\C s(v̄)) and A ∩ C 6= ∅, where C = {v̄i1 , . . . , v̄ik , ēj1 , . . . , ēK
 A        A                                                                 k
               P
                                                                                              jK }.

Backward direction. Let α be an arbitrary solution to I ′′ . We start by showing the following claim.
Claim 33.1. For every v ∈ XY either α(v) = α(B(v)) or α(v) = α(G(v)).
Proof of claim: Suppose to the contrary that this is not the case. Because v ∈ XY, v appears in the two
constraints:


                                                             35
   • v = B(v) ∨ v − B(v) ≥ M and
   • v = G(v) ∨ G(v) − v ≥ M .
Thus, α(v)−α(B(v)) ≥ M and α(G(v))−α(v) ≥ M . However, this is only possible if α(G(v))−α(B(v)) ≥
2M , which, as we will show now, is not the case. It follows from the relation between the bucket and
                                                                                          EK
garbage variables and the deﬁnition of B(v) and G(v) that α(B(v)) ≥ b11 and α(G(v)) ≤ g|E  K|
                                                                                              . Hence,
                           EK
α(G(v))−α(B(v)) ≤ α(g|E      K|
                                )−α(b11 ). Because of the constraints on the bucket variables and the garbage
variables, i.e. the constraints:
   • bi4 − bi1 = N for every i with 1 ≤ i ≤ K,
   • bi+1
      1   = bi4 for every i with 1 ≤ i < K,
      A
          − g0A < v̄∈A s(v̄) for every A ∈ {V1 , . . . , Vk , E1 , . . . , EK },
                  P
   • g|A|
       V       Vi
   • g0 i+1 = g|Vi|
                    for every i with 1 ≤ i ≤ k,
       E       Ei
   • g0 i+1 = g|E i|
                     for every i with 1 ≤ i ≤ K,
      Vk
   • g|Vk|
           = g0E1 ,

   • g0V1 − bK
             4 = M.

we obtain that:

                                 α(G(v)) − α(B(v))             EK
                                                          ≤ α(g|E K|
                                                                     ) − α(b11 )
                                                                          X
                                                          < NK + M +            s(v̄)
                                                                                v̄∈S
                                                                        X
                                                          ≤ NK +               s(v̄) + M
                                                                        v̄∈S
                                                          ≤ 2M


We see that α(G(v)) − α(B(v)) < 2M . This contradiction concludes the proof of Claim 33.1.                        ⋄
   We say that a vector v̄ℓi ∈ Vi is in the bucket if α(xVℓ,ci ) = α(B(xVℓ,ci )) and α(yℓ,c
                                                                                         Vi          Vi
                                                                                            ) = α(B(yℓ,c )) for every
                                                                                              V
non-zero coordinate c of v̄ℓi . Moreover, we say that v̄ℓi ∈ Vi is in the garbage if α(xℓ,ci ) = α(G(xVℓ,ci )) and
   Vi           Vi
α(yℓ,c ) = α(G(yℓ,c )) for every non-zero coordinate c of v̄ℓi . Similarly, we say that a vector ēiℓ ∈ Ei is in
the bucket if α(xE               Ei           Ei              Ei                        i
                 ℓ ) = α(B(xℓ )) and α(yℓ ) = α(B(yℓ )) and we say that ēℓ ∈ Ei is in the garbage if
                    i

    Ei          Ei              Ei           Ei
α(xℓ ) = α(G(xℓ )) and α(yℓ ) = α(G(yℓ )).
   Based on Claim 33.1, we will now show that for every set Vi and every set Ei exactly one vector is in
the bucket and all other vectors (of the set) are in the garbage. We start by showing the claim for the
sets Vi .
Claim 33.2. For every Vi there is exactly one vector v̄ℓi ∈ Vi such that v̄ℓi is in the bucket, and all other
vectors in Vi are in the garbage.
Proof of claim: We ﬁrst show that at least one vector v̄ℓi is in the bucket. Suppose to the contrary
that this is not the case. Claim 33.1 implies that for every ℓ there is a non-zero coordinate c of v̄ℓi such
that α(xVℓ,ci ) = α(G(xVℓ,ci )) and, consequently, α(yℓ,c
                                                      Vi           Vi
                                                          ) = α(G(yℓ,c                                 Vi
                                                                       )). Thus, the distance between gℓ−1 and
 Vi                 i                              Vi       Vi          P
gℓ is exactly s(v̄ℓ ) so the distance between g0 and g|Vi | equals v̄∈Vi s(v̄). This violates the constraint
 Vi
      − g0Vi < v̄∈Vi s(v̄) and consequently contradicts our assumption that α is a solution for I ′′ . We
                 P
g|Vi|
conclude that there is at least one vector v̄ℓi in the bucket.


                                                           36
    It remains to show that all other vectors v̄ℓi′ ∈ Vi for ℓ′ 6= ℓ are in the garbage, i.e. α(xVℓ′i,c ) = α(G(xVℓ′i,c ))
and α(yℓV′i,c ) = α(G(yℓV′i,c )) for every ℓ′ 6= ℓ and every non-zero component c of v̄ℓi′ . Suppose this is not
the case and assume that the claim is violated for ℓ′ and c. Then, by Claim 33.1, it follows that
α(xVℓ′i,c ) = α(B(xVℓ′i,c )) (and therefore also α(yℓV′i,c ) = α(B(yℓV′i,c ))). This implies that the distance between
B(xVℓ′i,c ) and B(yℓV′i,c ) is equal to s(v̄ℓi′ ). However, since α(xVℓ,ci ) = α(B(xVℓ,ci )) and α(yℓ,c
                                                                                                    Vi           Vi
                                                                                                        ) = α(B(yℓ,c )), we
                                                  Vi         Vi             Vi           Vi                  i
obtain that the distance between B(xℓ′ ,c ) = B(xℓ,c ) and B(yℓ′ ,c ) = B(yℓ,c ) is equal to s(v̄ℓ ). However,
this is not possible because no two vectors in Vi agree on s(v̄) and hence s(v̄ℓi′ ) 6= s(v̄ℓi ).                        ⋄
     An analogous proof shows the statement of Claim 33.2 for the sets Ei (instead of the sets Vi ).
Claim 33.3. For every Ei there is exactly one vector ēiℓ ∈ Ei such that ēiℓ is in the bucket, and all other
vectors in Ei are in the garbage.
   We continue by showing that the vectors that are in the bucket form a solution for I. Let v̄ i ∈ Vi and
 j
ē ∈ Ej with 1 ≤ i ≤ k and 1 ≤ j ≤ K be the vectors that are in the bucket; these vectors exist due to
Claims 33.2 and 33.3. The constraints bl4 − bl1 = N imply that
                                      k            K
                                              !          !
                                     X             X
                                          v̄ i +      ēi = N̄ .
                                             i=1           i=1

for every 1 ≤ l ≤ K. Hence, the vectors v̄ 1 , . . . , v̄ k and ē1 , . . . , ēK indeed form a solution for I.
    The proof so far shows that I has a solution if and only if I ′′ has a solution. In the ﬁnal part of
the proof, we show how to transform the instance I ′′ into the equivalent instance I ′ of CSP(D2,1 ). To
achieve this we ﬁrst replace every constraint of the form a − b ⊙ n (for variables a and b, natural number
n with n > 1, and ⊙ ∈ {≤, <, =, ≥, >}) by a ‘path’ on n auxiliary variables. More formally, to replace
the constraint C = a − b ⊙ n, we add n auxiliary variables hC                C
                                                                1 , . . . , hn and the constraints h1 − b ⊙ 1,
 C        C                                      C
hi+1 − hi ⊙ 1 for every i with 1 ≤ i ≤ n, and hn = b. This allows us to replace the following constraints
of I ′′ :
     • the constraints bi4 − bi1 = N for every i with 1 ≤ i ≤ K,
                         A
                            − g0A < v̄∈A s(v̄) for every A ∈ {V1 , . . . , Vk , E1 , . . . , EK },
                                    P
     • the constraints g|A|

     • the constraint g0V1 − bK
                              4 = M,

     • the constraints yℓEi − xE       i
                               ℓ = s(ēℓ ), for every i and ℓ with 1 ≤ i ≤ K and 1 ≤ ℓ ≤ |Ei |, and
                                 i



                        Vi
     • the constraints yℓ,c  − xVℓ,ci = s(v̄ℓi ), for every i and ℓ with 1 ≤ i ≤ k, 1 ≤ ℓ ≤ |Ei |, and every non-zero
       component c of v̄ℓi .
Note that this reduction is polynomial since the numbers in the instance I can be assumed to be polyno-
mially bounded in the input size because MPSS is strongly W[1]-hard. Also note that this replacement
does not increase the treewidth of the primal graph by more than 1 since the new primal graph can be
obtained by subdividing edges of the original primal graph and it is well known that subdividing edges
can only increase the treewidth of a graph by at most 1. Let I ′′′ be the instance obtained from I ′′ after
replacing all of the constraints as described above.
    It now only remains to replace the remaining constraints for the variables in XY. Recall that these
constraints are of the form z = B(z) ∨ z − B(z) ≥ M and z = G(z) ∨ G(z) − z ≥ M for some
z ∈ XY. As we saw in Claim 33.1, the eﬀect of these two constraints is that for every variable z ∈ XY
and every solution α for I ′′ , either α(z) = α(B(z)) or α(z) = α(G(z)). To replace these constraints, we
ﬁrst introduce a gadget U (a, b, Z), where a and b are variables and Z is a natural number, which ensures
that either a = b or b − a ≥ Z. The gadget U (a, b, Z) has 2Z + 1 auxiliary variables h0 , . . . , h2Z and the
following constraints:
(C1) h0 = a, hi+1 − hi ∈ [0, 1] for every i with 0 ≤ i < 2Z, and h2Z = b,


                                                            37
(C2) hi+2 − hi = 0 ∨ hi+2 − hi > 1 for every i with 0 ≤ i < 2Z − 1.
Claim 33.4. Consider the instance U (a, b, Z) for variables a and b and natural number Z. Then:
   • every solution β for U (a, b, Z) satisfies either β(a) = β(b) or β(b) − β(a) ∈ (Z, 2Z], and
   • for every number Z ′ ∈ {0} ∪ (Z, 2Z], there is a solution β for U (a, b, Z) such that β(b) − β(a) = Z ′ .
Proof of claim: Let β be a solution for U (a, b, Z). The constraints in (C1) imply that β(b)−β(a) ∈ [0, 2Z].
If β(a) = β(b), then there is nothing to show. Hence, assume that β(a) < β(b). Now, there is an i with
0 ≤ i < 2Z − 1 such that hi+2 − hi > 0. We ﬁrst show that hi+2 − hi > 0 for every i with 0 ≤ i < 2Z − 1.
Suppose that this is not the case and let i be an index such that hi+2 −hi > 0 but either hi+3 −hi+1 = 0 or
hi+1 − hi−1 = 0. In both cases it follows from the constraints in (C2) that hi+2 − hi > 1. Consequently,
the constraints in (C1) imply that hi+1 − hi > 0 and hi+2 − hi+1 > 0. However, this implies that
hi+3 − hi+1 > 0 (since i < 2Z − 2) and hi+1 − hi−1 > 0 (since i > 0) so we obtain a contradiction. Hence,
hi+2 − hi > 0 for every i with 0 ≤ i < 2Z − 1, which together with the constraints in (C2) implies that
hi+2 − hi > 1 for every i with 0 ≤ i < 2Z − 1. Since
                                                      Z
                                                      X
                                   β(b) − β(a)    ≥         β(h2i ) − β(h2i−2 )
                                                      i=1
                                                      Z
                                                      X
                                                  >         1
                                                      i=1
                                                  = Z

it follows that β(b) − β(a) > Z. This completes the proof of the ﬁrst statement of the claim.
    We continue with the second statement of the claim. Arbitrarily choose Z ′ ∈ {0} ∪ (Z, 2Z]. If Z ′ = 0,
then we set
                         β(a) = β(h0 ) = β(h1 ) = · · · = β(h2Z−1 ) = β(h2Z ) = β(b)
and this assignment clearly satisﬁes all constraints in (C1) and (C2). If Z ′ ∈ (Z, 2Z), then we set
β(a) = β(h0 ), β(hi+1 ) − β(hi ) = 0.5 + ǫ for every i with 0 ≤ i < 2Z, and β(h2Z ) = β(b), where
ǫ = (Z ′ − Z)/2Z. It is straightforward to verify that this assignment satisﬁes the constraints in (C1) and
(C2). This completes the proof of Claim 33.4.                                                             ⋄
    We are now ready to show how to replace the constraints z = B(z) ∨ z − B(z) ≥ M and z =
G(z) ∨ G(z) − z ≥ M for every variable z ∈ XY. That is, for z ∈ XY, we replace the constraint z =
B(z)∨z−B(z) ≥ M with the gadget U (z, B(z), M ) and we replace the constraint z = G(z)∨G(z)−z ≥ M
with the gadget U (G(z), z, M ).
    Then, I ′ is obtained from I ′′′ after replacing all the remaining constraints of the variables in XY
as described above. Clearly, I ′ is an instance of CSP(D2,1 ). Furthermore, the treewidth of the primal
graph of I ′ is at most the treewidth of the primal graph of I ′′ plus 2. This is because the treewidth of
the primal graph of I ′′′ is at most the treewidth of I ′′ plus 1 (as we already argued above). Furthermore,
the primal graph for I ′ is obtained from the primal graph of I ′′′ by replacing the edges between x and
B(x) as well as between x and G(x) with the primal graph of the gadget U (a, b, Z) for every x ∈ XY.
The result now follows because the treewidth of the primal graph of U (a, b, Z) is at most 2. Because the
treewidth of the primal graph of I ′′ is at most 4K + 3, we obtain that the treewidth of the primal graph
of I ′ is at most 4K + 5.
   Since all variables in the proof of Theorem 33 are only assigned integers, we can replace every constraint
                                                                          Vi
L < R that uses < in the construction, i.e., the constraints of the form g|Vi|
                                                                               − g0Vi < T and g|E
                                                                                               Ei
                                                                                                  i|
                                                                                                     − g0Ei < T ,
by L ≤ R − 1. Therefore, we obtain the following corollary from Theorem 33.
Corollary 34. CSP(D≤
                   2,1 ) is strongly W[1]-hard parameterized by primal treewidth.




                                                       38
7     Generalizations
The results that we have proved in Sections 3–6 are restricted in two ways: (1) formulas are assumed to
be in conjunctive normal form and (2) the variable domains are assumed to be the set of rationals. We
consider the satisﬁability problem for DL without these restrictions in the following two sections. Thus,
we discuss DL with general formulas (i.e. the DL-Sat problem from Section 2.1) in Section 7.1 and we
discuss DL with integer variable domains in Section 7.2.

7.1    General Formulas
Every DL formula can be converted into a logically equivalent formula that is in CNF by using well-known
laws of logic. We use this fact for proving the following result.
Theorem 35. DL-Sat is solvable in 2O(n(log n+log k)) time where n is the number of variables in the
given formula φ and k = num(φ). DL-Sat is not solvable in 2o(n(log n+log k)) if the ETH holds.
Proof. The lower bound is an immediate consequence of Theorem 17 since every instance of CSP(D6         2 )
can be viewed as a DL formula (as was discussed in Section 2.2). To show the upper bound, we let φ
denote an arbitrary instance of DL-Sat. Assume φ contains n variables and that k = num(I). Every
existential sentence φ admits a logically equivalent existential sentence φ′ such that φ′ is in CNF, φ and
φ′ contains the same number of variables, and k = num(φ′ ). The formula φ′ may be viewed as an instance
I = (V, C) of CSP(D) where |V | = n and num(I) = k. Theorem 6 implies that φ′ is satisﬁable if and
only if it has a solution f : V → CD (n, k). Since φ and φ′ are logically equivalent formulas, the same
holds for φ. The upper bound follows immediately since CD (n, k) contains 2O(n(log n+log k)) elements (as
was proved in Corollary 7).
    The conversion of a DL formula into CNF can obviously lead to an exponential larger formula and
the conversion process may thus take exponential time. Note, however, that we do not need to compute
the CNF formula explicitly in the proof of Theorem 35.
    Theorem 35 is closely connected to Satisfiability Modulo Theories (SMT), i.e. the decision problem
for logical sentences with respect to a given background theory, where logical formulas are expressed in
classical ﬁrst-order logic with equality. Let SMT(T ) be the problem of determining whether a ﬁrst-order
sentence is true with respect to a background theory T , and let SMT∃ (T ) be the subproblem where uni-
versal quantiﬁers are not allowed. If we let Tdiff denote the background theory for diﬀerence constraints,
then DL-Sat and SMT∃ (Tdiff ) are the same computational problems. Jonsson and Lagerkvist [49, The-
orem 9] prove bounds valid for any background theory: SMT∃ (∅) is solvable in 2O(|V | log |V |) time but it
cannot be solved in 2o(|V | log |V |) time unless the ETH is false. Theorem 35 thus implies that SMT∃ (Tdiff )
is only marginally harder than SMT∃ (∅).
    Applying the restricted time complexity results and the parameterized results to DL-Sat directly is,
unfortunately, not possible. The clause arity parameter is obviously not well-deﬁned for an arbitrary
existential formula φ since it is not required to be in CNF. Similarly, the primal and incidence graphs
are not well-deﬁned in this case. Converting the formula into CNF is typically not a viable option since
this process may take exponential time and it may produce a formula that is exponentially larger than
the original formula. A simple (but sometimes suﬃciently powerful) workaround is based on generalizing
the results to more complex subformulas than clauses. We present one possible way of doing this. Recall
from Section 2.2 that we can always view a CSP instance as a primitive positive sentence over some
structure. We have used this perspective throughout the article: we view an existential formula in CNF
as a CSP instance where the structure contains the relations that describe the allowed clauses. Clearly,
we can instead consider relations that describe other subformulas than clauses. This must be done with
care, though. These relations cannot use auxiliary variables in their deﬁnitions since this introduces a
time complexity dependency on the number of subformulas and not only on the number of variables and
the magnitude of the coeﬃcients. Furthermore, the deﬁnitions of the subformulas must (in a certain
sense) be easy to compute. We circumvent this problem by restricting ourselves to a ﬁnite number of
subformula types; this restriction can often be lifted but it needs a careful analysis based on the chosen
relations and the representation of them. We arrive at the following result.

                                                     39
Proposition 36. If A is a finite structure that is quantifier-free definable in S, then the following hold.

  1. CSP(A) is solvable in 2O(n log n) time.
  2. If the relations in A have arity at most 2, then CSP(A) is solvable in 2O(n log log n) time.
  3. If the relations in A have arity at most 3 and num(A) = 0, then CSP(A) is solvable in 2O(n) time.
  4. CSP(A) is in XP when parameterized by the treewidth of the incidence graph.

Proof. The structure A is ﬁnite and every relation in A has a quantiﬁer-free deﬁnition in S. We may
without loss of generality assume that the deﬁning formulas are in CNF. This implies that every relation
can be viewed as a conjunction of relations in Da,k where a, k < ∞. Since A is ﬁnite, we may assume
that we have access to a table containing the deﬁning CNF formulas for each relation in A.
   Let I = (V, C) denote an instance of CSP(A) and arbitrarily choose a constraint R(x1 , . . . , xn ) in C.
The relation R has a deﬁnition
                                                            p
                                                            ^
                                   R(x1 , . . . , xn ) ≡          Ri (xi,1 , . . . , xi,ar(Ri ) )
                                                            i=1

where R1 , . . . , Rp ∈ Da,k and {xi,j : 1 ≤ i ≤ p, 1 ≤ j ≤ max{ar(Rm ) : 1 ≤ m ≤ p}} ⊆ {x1 , . . . , xn }. This
constraint in I can be replaced by p constraints

                              R1 (x1,1 , . . . , x1,ar(R1 ) ), . . . , Rp (xp,1 , . . . , xp,ar(Rp ) )

and this transformation does not aﬀect the solvability of the instance since it preserves the set of solutions.
Let I ′ = (V ′ , C ′ ) denote the instance that results from applying this transformation to each constraint
in C. We note that I ′ can be computed in polynomial time, V ′ = V , num(C) = num(C ′ ), and I ′ has
a solution if and only if I has a solution. Now, item 1 follows from Corollary 7, item 2 follows from
Theorem 13, and item 3 follows from Theorem 1. Finally, we claim that item 4 follows from Theorem 22
together with the observation that tw(I(I ′ )) ≤ q · tw(I(I)), where q is the smallest integer such that any
constraint in I is replaced by at most q constraints in I ′ ; note that q can be considered constant because
A is ﬁnite. The last observation follows because any tree decomposition of I(I) can be transformed into
a tree decomposition of I(I ′ ) by replacing any vertex corresponding to a constraint c in I by the at most
q vertices corresponding to the constraints that replace c in I ′ .

7.2    Integer Domains
We show that the complexity results presented in this article also hold if we restrict DL to integer variable
domains. Henceforth, we let DZa,k denote the set of relations in Da,k restricted to the integers. Let A
and B be two structures. We write CSP(A) ≤0 CSP(B) if there exists a polynomial-time reduction F
from CSP(A) to CSP(B) that introduces no additional variables, i.e. if (V, C) is an instance of CSP(A),
then F ((V, C)) = (V, C ′ ). The existence of such a reduction implies the following.

   1. If CSP(A) is not solvable within a time bound f (|V |), then CSP(B) is not solvable within f (|V |),
      either.
   2. If CSP(B) is solvable within a time bound f (|V |), then CSP(A) is solvable within f (|V |), too.

   We continue by presenting a number of reductions.
Lemma 37. CSP(D≤             Z             ≤
               a,k ) ≤0 CSP(Da,k ) ≤0 CSP(Da,k+1 ).

Proof. We ﬁrst verify that if an instance I of CSP(D≤ ) has a solution, then it has a solution over Z,
too. Let I = (V, C) with C = {c1 , . . . , cp } denote an arbitrary satisﬁable instance of CSP(D≤ ). Since
I is satisﬁable, we can pick one literal li out of the deﬁnition of every constraint c1 , . . . , cp such that
{l1 , . . . , lp } is satisﬁable. This set of constraints admits an integer solution since the literals are of the

                                                                40
form x − y ≤ c and the bound c is an integer: this follows from the original algorithm for solving STPs by
Dechter et al. [28, Section 3] but it is also a consequence of the theory of total unimodularity [64, Section
13.2]. Consequently, I admits an integer solution.
    We begin with the reduction CSP(D≤                              Z
                                                  a,k ) ≤0 CSP(Da,k ). Let R denote a relation in Da,k and let
                                                                                                                ≤

RZ have the same deﬁnition as R but with domain Z instead of Q. Let I = (V, C) denote an arbitrary
instance of CSP(D≤        a,k ) and let IZ = (V, CZ ) where CZ = {RZ (x1 , . . . , xk ) : R(x1 , . . . , xk ) ∈ C}. If I is
not satisﬁable, then IZ is not satisﬁable since Z ⊆ R. If I is satisﬁable, then IZ is satisﬁable as pointed
out earlier.
    We continue with the reduction CSP(DZa,k ) ≤0 CSP(D≤                                                           Z
                                                                      a,k+1 ). Let RZ denote a relation in Da,k . We
deﬁne a relation R over Q as follows: R has the same deﬁnition as RZ but every literal that is a strict
inequality x − y < c is replaced by x − y ≤ c − 1. Observe that RZ ⊆ R and R is a member of D≤                       a,k+1 .
                                                              Z
Let IZ = (V, CZ ) denote an arbitrary instance of Da,k and let I = (V, C) where C = {R(x1 , . . . , xk ) :
RZ (x1 , . . . , xk ) ∈ CZ }. If IZ has a solution fZ , then this solution is a solution to I, too, since RZ ⊆ R for
every RZ ∈ DZa,k . If I is satisﬁable, then it has an integer solution (as discussed earlier) and this solution
witnesses the satisﬁability of IZ .
Lemma 38. CSP(Da,0 ) ≤0 CSP(DZa,0 ) ≤0 CSP(Da,0 )
Proof. We ﬁrst verify that if an instance I of CSP(Da,0 ) has a solution, then it has a solution over Z,
too. Arbitrarily choose a satisﬁable instance I of CSP(Da,0 ). Assume that f : V → Q is a solution
to I. Observe that the function fc (x) = c · f (x) is a solution to I whenever c 6= 0. We assume that
V = {x1 , . . . , xn } and f (xi ) = ai /bi , 1 ≤ i ≤ n, where ai and bi 6= 0 are integers. Let c = b1 · . . . · bn and
note that fc is a function from V to Z. Thus, a satisﬁable instance I of CSP(Da,0 ) always has an integer
solution.
    Let us now consider the reduction CSP(Da,0 ) ≤0 CSP(DZa,0 ). Given a relation R ∈ Da,0 , we let RZ
denote R restricted to the integers. Let IZ denote an arbitrary instance of DZa,0 and let I = (V, C) where
C = {R(x1 , . . . , xk ) : RZ (x1 , . . . , xk ) ∈ CZ }. If IZ has a solution, then I has a solution, too. If I has a
solution, then IZ has a solution as pointed out earlier. The other reduction is analogous.
    These reductions imply that all results in Table 2 hold for DZa,k . Similarly, the results in Table 3 hold
since the reductions do not change the primal and incidence graphs of a given instance. The results for
DL-Sat (Theorem 35) also hold in the integer case. The reductions show that CSP(DZ ) is solvable in
2O(n(log n+log k)) time but not in 2o(n(log n+log k)) (under the ETH). The proof of Theorem 35 shows that
these results immediately carry over to DL-Sat over the integers.


8     Conclusion and Future Work
We have initiated a ﬁne-grained complexity analysis of the satisﬁability problem for DL. We have studied
the time complexity of CSP(Da,k ) and obtained closely matching bounds for almost all choices of a, k ∈
N ∪ {∞}. We have studied the parameterized complexity of CSP(Da,k ) (with parameters primal and
incidence treewidth) and obtained a comprehensive picture for all choices of a and k. We have considered
generalizations where arbitrary formulas are allowed and where variable domains are the integers; many
of our results survive such generalizations.
    A future research direction is to close the gaps between lower bounds and upper bounds for time
complexity. This boils down to a better understanding of the time complexity of CSP(D2,k ). There is a
lack of natural problems that can be solved in 2O(n log log n) time but do not admit a single-exponential-
time algorithm. This may point in the direction that CSP(D2,k ) is solvable in single-exponential time
but it may equally well indicate a need for new lower bound techniques. We remark that the running time
of the bounded-span algorithm (Lemma 9) is the dominant term in the time complexity of our algorithm
for CSP(D2,k ) so improving this part would reduce the overall time complexity.
    Our work on parameterized complexity have focused on the parameters primal and incidence treewidth
One possible way forward is to study other structural parameters. The notion of treewidth captures the
fact that trees are structurally simple, but fails to do this for cliques since the treewidth of an n-clique


                                                            41
is n − 1. An alternative graph decomposition with a corresponding quality measure (known as clique-
width) was introduced and analyzed in a series of articles [23, 24, 81]. This decomposition captures the
structure of both sparse graphs (such as trees) and dense graphs (such as cliques), and it is known to
have algorithmic properties that are similar to those of bounded treewidth graphs. It may thus be highly
relevant in connection with DL.
    Algorithms for deciding the truth of DL formulas containing universal quantiﬁers is a natural step for-
ward. Theorem 6 suggests a straightforward but incorrect approach. Consider a formula Q1 x1 . . . Qn xn .φ
where Qi ∈ {∀, ∃} and φ is quantiﬁer-free. Let D = CD(n, k) be the set of values needed for φ via Lemma
6. If Q1 = ∀, then we assign the values from D to variable x1 and recursively check that all assignments
leads to satisﬁability. If Q1 = ∃, then we check that at least one assignment leads to satisﬁability. How-
ever, such an algorithm does not work as intended: the formula ∀x∃y.y − x ≥ 1 is false when interpreted
over any ﬁnite D ⊆ Q while it is true when interpreted over Q. This implies that another algorithmic
approach is needed for handling quantiﬁed DL formula.


Acknowledgements
The second and the fourth author were supported by the Wallenberg AI, Autonomous Systems and
Software Program (WASP) funded by the Knut and Alice Wallenberg Foundation. In addition, the
second author was partially supported by the Swedish Research Council (VR) under grant 2021-0437.
The third author was supported by the Engineering and Physical Sciences Research Council (EPSRC)
(Project EP/V00252X/1).


References
 [1] Martin Aigner and Günter M. Ziegler. Proofs from THE BOOK. Springer, 6th edition, 2018.
 [2] James F. Allen. Maintaining knowledge about temporal intervals. Communications of the ACM,
     26(11):832–843, 1983.
 [3] Rajeev Alur. Timed automata. In Proc. 11th International Conference on Computer Aided Verifi-
     cation (CAV-1999), pages 8–22, 1999.
 [4] Stefan Arnborg, Derek Corneil, and Andrzej Proskurowski. Complexity of ﬁnding embeddings in a
     k-tree. SIAM Journal on Matrix Analysis and Applications, 8(2):277–284, 1987.
 [5] Goutam K. Audhya, Koushik Sinha, and Sasthi C. Ghosh. A survey on the channel assignment
     problem in wireless networks. Wireless Communications & Mobile Computing, 11(5):583–609, 2011.
 [6] Federico Barber. Reasoning on interval and point-based disjunctive metric constraints in temporal
     contexts. Journal of Artificial Intelligence Research, 12:35–86, 2000.
 [7] Clark W. Barrett, Roberto Sebastiani, Sanjit A. Seshia, and Cesare Tinelli. Satisﬁability modulo
     theories. In Armin Biere, Marijn Heule, Hans van Maaren, and Toby Walsh, editors, Handbook of
     Satisfiability, volume 185 of Frontiers in Artificial Intelligence and Applications, pages 825–885. IOS
     Press, 2009.
 [8] Umberto Bertelé and Franscesco Brioschi. Nonserial Dynamic Programming. Academic Press, 1972.
 [9] Marc Bezem, Robert Nieuwenhuis, and Enric Rodríguez-Carbonell. The max-atom problem and its
     relevance. In Proc. 15th International Conference on Logic for Programming, Artificial Intelligence,
     and Reasoning (LPAR-2008), pages 47–61, 2008.
[10] Nikhil Bhargava and Brian C. Williams. Multiagent disjunctive temporal networks. In Proc. 18th
     International Conference on Autonomous Agents and MultiAgent Systems (AAMAS-2019), pages
     458–466, 2019.

                                                    42
[11] Bernhard Bliem, Michael Morak, Marius Moldovan, and Stefan Woltran. The impact of treewidth on
     grounding and solving of answer set programs. Journal of Artificial Intelligence Research, 67:35–80,
     2020.
[12] Manuel Bodirsky. Complexity of Infinite-Domain Constraint Satisfaction. Cambridge University
     Press, 2021.
[13] Manuel Bodirsky and Víctor Dalmau. Datalog and constraint satisfaction with inﬁnite templates.
     Journal of Computer and System Sciences, 79(1):79–100, 2013.
[14] Manuel Bodirsky and Peter Jonsson. A model-theoretic view on qualitative constraint reasoning.
     Journal of Artificial Intelligence Research, 58:339–385, 2017.
[15] Manuel Bodirsky and Marcello Mamino. Constraint satisfaction problems over numeric domains.
     In The Constraint Satisfaction Problem: Complexity and Approximability, volume 7 of Dagstuhl
     Follow-Ups, pages 79–111. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2017.
[16] Hans L. Bodlaender. A linear-time algorithm for ﬁnding tree-decompositions of small treewidth.
     SIAM Journal on Computing, 25(6):1305–1317, 1996.
[17] Hans L. Bodlaender and Ton Kloks. Eﬃcient and constructive algorithms for the pathwidth and
     treewidth of graphs. Journal of Algorithms, 21(2):358–402, 1996.
[18] James C. Boerkoel and Edmund H. Durfee. Decoupling the multiagent disjunctive temporal problem.
     In Proc. 27th AAAI Conference on Artificial Intelligence (AAAI-2013), 2013.
[19] Chris Calabro, Russell Impagliazzo, and Ramamohan Paturi. The complexity of satisﬁability of
     small depth circuits. In Proc. 4th International Workshop on Parameterized and Exact Computation
     (IWPEC-2009), pages 75–85, 2009.
[20] Lorenzo Candeago, Daniel Larraz, Albert Oliveras, Enric Rodríguez-Carbonell, and Albert Rubio.
     Speeding up the constraint-based method in diﬀerence logic. In Proc. 19th International Conference
     on the Theory and Applications of Satisfiability Testing (SAT-2016), pages 284–301, 2016.
[21] Clément Carbonnel and Martin C. Cooper. Tractability in constraint satisfaction problems: A
     survey. Constraints, 21(2):115–144, 2016.
[22] Stephen A. Cook. The complexity of theorem-proving procedures. In Proc. 3rd Annual ACM
     Symposium on Theory of Computing (STOC-1971), pages 151–158, 1971.
[23] Bruno Courcelle, Joost Engelfriet, and Grzegorz Rozenberg. Handle-rewriting hypergraph grammars.
     Journal of Computer and System Sciences, 46(2):218–270, 1993.
[24] Bruno Courcelle and Stephan Olariu. Upper bounds to the clique width of graphs. Discrete Applied
     Mathematics, 101(1–3):77–114, 2000.
[25] Konrad K. Dabrowski, Peter Jonsson, Sebastian Ordyniak, and George Osipov. Fine-grained com-
     plexity of temporal problems. In Proc. 17th International Conference on Principles of Knowledge
     Representation and Reasoning (KR-2020), pages 284–293, 2020.
[26] Konrad K. Dabrowski, Peter Jonsson, Sebastian Ordyniak, and George Osipov. Disjunctive temporal
     problems under structural restrictions. In Proc. 35th AAAI Conference on Artificial Intelligence
     (AAAI-2021), pages 3724–3732, 2021.
[27] Konrad K. Dabrowski, Peter Jonsson, Sebastian Ordyniak, and George Osipov. Solving inﬁnite-
     domain CSPs using the patchwork property. Artificial Intelligence, 317:103880, 2023.
[28] Rina Dechter, Itay Meiri, and Judea Pearl. Temporal constraint networks. Artificial intelligence,
     49(1-3):61–95, 1991.

                                                   43
[29] Rodney G. Downey and Michael R. Fellows. Fundamentals of Parameterized Complexity. Springer,
     2013.
[30] Paul Erdős and Pál Turán. On a problem of Sidon in additive number theory, and on some related
     problems. Journal of the London Mathematical Society, 1(4):212–215, 1941.
[31] Leif Eriksson and Victor Lagerkvist. Improved algorithms for Allen’s interval algebra: a dynamic pro-
     gramming approach. In Proc. 30th International Joint Conference on Artificial Intelligence (IJCAI-
     2021), pages 1873–1879, 2021.
[32] Jörg Flum and Martin Grohe. Parameterized Complexity Theory. Springer, 2006.
[33] Robert Ganian, Fabian Klute, and Sebastian Ordyniak. On structural parameterizations of the
     bounded-degree vertex deletion problem. Algorithmica, 83(1):297–336, 2021.
[34] Robert Ganian and Sebastian Ordyniak. The complexity landscape of decompositional parameters
     for ILP. Artificial Intelligence, 257:61–71, 2018.
[35] Robert Ganian, Sebastian Ordyniak, and C. S. Rahul. Group activity selection with few agent types.
     Algorithmica, 85(5):1111–1155, 2023.
[36] Michael R. Garey and David S. Johnson. Computers and Intractability: A Guide to the Theory of
     NP-Completeness. W.H. Freeman and Company, 1979.
[37] Serge Gaspers. Exponential Time Algorithms - Structures, Measures, and Bounds. VDM, 2010.
[38] Alfonso Gerevini, Alessandro Saetti, and Ivan Serina. An approach to temporal planning and schedul-
     ing in domains with predictable exogenous events. Journal of Artificial Intelligence Research, 25:187–
     231, 2006.
[39] Martin Charles Golumbic, Haim Kaplan, and Ron Shamir. On the complexity of DNA physical
     mapping. Advances in Applied Mathematics, 15:251–261, 1994.
[40] Georg Gottlob, Reinhard Pichler, and Fang Wei. Bounded treewidth as a key to tractability of
     knowledge representation and reasoning. In Proc. 21st National Conference on Artificial Intelligence
     (AAAI-2006), pages 250–256, 2006.
[41] Georg Gottlob, Francesco Scarcello, and Martha Sideri. Fixed-parameter complexity in AI and
     nonmonotonic reasoning. Artificial Intelligence, 138(1-2):55–86, 2002.
[42] Heini Halberstam and Klaus Roth. Sequences. Springer, 1966.
[43] Wilfrid Hodges. A Shorter Model Theory. Cambridge University Press, New York, NY, USA, 1997.
[44] Hoon Hong. Comparison of several decision algorithms for the existential theory of the reals. Tech-
     nical Report 91-41, RISC Linz, 1991.
[45] Jinbo Huang, Jason Jingshi Li, and Jochen Renz. Decomposition and tractability in qualitative
     spatial and temporal reasoning. Artificial Intelligence, 195:140–164, 2013.
[46] Russell Impagliazzo, Ramamohan Paturi, and Francis Zane. Which problems have strongly expo-
     nential complexity? Journal of Computer and System Sciences, 63(4):512–530, 2001.
[47] Peter Jonsson and Christer Bäckström. A unifying approach to temporal constraint reasoning.
     Artificial Intelligence, 102(1):143–155, 1998.
[48] Peter Jonsson and Victor Lagerkvist. Why are CSPs based on partition schemes computationally
     hard? In Proc. 43rd International Symposium on Mathematical Foundations of Computer Science
     (MFCS-2018), pages 43:1–43:15, 2018.


                                                    44
[49] Peter Jonsson and Victor Lagerkvist. General lower bounds and improved algorithms for inﬁnite-
     domain CSPs. Algorithmica, 85(1):188–215, 2023.
[50] Peter Jonsson and Tomas Lööw. Computational complexity of linear constraints over the integers.
     Artificial Intelligence, 195:44–62, 2013.
[51] Ton Kloks. Treewidth: Computations and Approximations, volume 842 of LNCS. Springer, 1994.
[52] Phokion G. Kolaitis and Moshe Y. Vardi. Conjunctive-query containment and constraint satisfaction.
     Journal of Computer and System Sciences, 61(2):302–332, 2000.
[53] Manolis Koubarakis. Tractable disjunctions of linear constraints: basic results and applications to
     temporal reasoning. Theoretical Computer Science, 266(1-2):311–339, 2001.
[54] Daniel Král’. An exact algorithm for the channel assignment problem. Discrete Applied Mathematics,
     145(2):326–331, 2005.
[55] Yuliya Lierler and Benjamin Susman. On relation between constraint answer set programming and
     satisﬁability modulo theories. Theory and Practice of Logic Programming, 17(4):559–590, 2017.
[56] Daniel Lokshtanov, Dániel Marx, and Saket Saurabh. Slightly superexponential parameterized prob-
     lems. SIAM Journal on Computing, 47(3):675–702, 2018.
[57] Carsten Lutz and Maja Miličić. A tableau algorithm for description logics with concrete domains
     and general tboxes. Journal of Automated Reasoning, 38(1-3):227–259, 2007.
[58] Peter Niebert, Moez Mahfoudh, Eugene Asarin, Marius Bozga, Oded Maler, and Navendu Jain.
     Veriﬁcation of timed automata via satisﬁability checking. In Proc. 7th International Symposium on
     Formal Techniques in Real-Time and Fault-Tolerant Systems (FTRTFT-2002), pages 225–244, 2002.
[59] Rolf Niedermeier. Invitation to Fixed-Parameter Algorithms. Oxford University Press, 2006.
[60] Ilkka Niemelä. Stable models and diﬀerence logic. Annals of Mathematics and Artificial Intelligence,
     53(1-4):313–329, 2008.
[61] Robert Nieuwenhuis, Albert Oliveras, and Cesare Tinelli. Solving SAT and SAT modulo theories:
     From an abstract Davis–Putnam–Logemann–Loveland procedure to DPLL(T ). Journal of the ACM,
     53(6):937–977, 2006.
[62] Kevin O’Bryant. A complete annotated bibliography of work related to Sidon sequences. Electronic
     Journal on Combinatorics, Dynamic Survey(11), 2004.
[63] Angelo Oddi and Amedeo Cesta. Incremental forward checking for the disjunctive temporal problem.
     In Proc. 14th European Conference on Artificial Intelligence (ECAI-2000), pages 108–112, 2000.
[64] Christos H. Papadimitriou and Kenneth Steiglitz. Combinatorial Optimization: Algorithms and
     Complexity. Prentice-Hall, 1982.
[65] Itsik Pe’er and Ron Shamir. Satisﬁability problems on intervals and unit intervals. Theoretical
     Computer Science, 175(2):349–372, 1997.
[66] Bart Peintner, Kristen Brent Venable, and Neil Yorke-Smith. Strong controllability of disjunctive
     temporal problems with uncertainty. In Proc. 13th International Conference on Principles and
     Practice of Constraint Programming (CP-2007), pages 856–863, 2007.
[67] Krzysztof Pietrzak. On the parameterized complexity of the ﬁxed alphabet shortest common super-
     sequence and longest common subsequence problems. Journal of Computer and System Sciences,
     67(4):757–771, 2003.



                                                   45
[68] James Renegar. On the computational complexity and geometry of the ﬁrst-order theory of the
     reals. Part I: Introduction. preliminaries. The geometry of semi-algebraic sets. The decision problem
     for the existential theory of the reals. Journal of Symbolic Computation, 13(3):255–299, 1992.
[69] Neil Robertson and Paul D. Seymour. Graph minors. III. Planar tree-width. Journal of Combina-
     torial Theory, Series B, 36(1):49–64, 1984.
[70] Marko Samer and Stefan Szeider. Constraint satisfaction with bounded treewidth revisited. Journal
     of Computer and System Sciences, 76(2):103–114, 2010.
[71] Andreas Schutt and Peter J. Stuckey. Incremental satisﬁability and implication for UTVPI con-
     straints. INFORMS Journal on Computing, 22(4):514–527, 2010.
[72] Sanjit A. Seshia, K. Subramani, and Randal E. Bryant. On solving boolean combinations of UTVPI
     constraints. Journal on Satisfiability, Boolean Modeling and Computation, 3(1-2):67–90, 2007.
[73] Simon Sidon. Ein Satz über trigonometrische Polynome und seine Anwendung in der Theorie der
     Fourier-Reihen. Mathematische Annalen, 106(1):536–539, 1932.
[74] Arkadiusz Socała. Tight lower bound for the channel assignment problem. ACM Transactions on
     Algorithms, 12(4):48, 2016.
[75] Kostas Stergiou and Manolis Koubarakis. Backtracking algorithms for disjunctions of temporal
     constraints. Artificial Intelligence, 120(1):81–117, 2000.
[76] Larry J. Stockmeyer and Albert R. Meyer. Word problems requiring exponential time: Preliminary
     report. In Proc. 5th Annual ACM Symposium on Theory of Computing (STOC-1973), pages 1–9,
     1973.
[77] Patrick Traxler. The time complexity of constraint satisfaction. In Proc. 3rd International Workshop
     on Parameterized and Exact Computation (IWPEC-2008), pages 190–201. Springer, 2008.
[78] Ioannis Tsamardinos and Martha E. Pollack. Eﬃcient solution techniques for disjunctive temporal
     reasoning problems. Artificial Intelligence, 151(1-2):43–89, 2003.
[79] Kristen Brent Venable and Neil Yorke-Smith. Disjunctive temporal planning with uncertainty. In
     Proc. 19th International Joint Conference on Artificial Intelligence (IJCAI-2005), pages 1721–1722,
     2005.
[80] Marc B. Vilain and Henry A. Kautz. Constraint propagation algorithms for temporal reasoning. In
     Proc. 5th National Conference on Artificial Intelligence (AAAI-1986), pages 377–382, 1986.
[81] Egon Wanke. k-NLC graphs and polynomial algorithms. Discrete Applied Mathematics, 54(2-3):251–
     266, 1994.
[82] Matteo Zavatteri, Alice Raﬀaele, Dario Ostuni, and Romeo Rizzi. An interdisciplinary experimental
     evaluation on the disjunctive temporal problem. Constraints, 28(1):1–12, 2023.




                                                   46
