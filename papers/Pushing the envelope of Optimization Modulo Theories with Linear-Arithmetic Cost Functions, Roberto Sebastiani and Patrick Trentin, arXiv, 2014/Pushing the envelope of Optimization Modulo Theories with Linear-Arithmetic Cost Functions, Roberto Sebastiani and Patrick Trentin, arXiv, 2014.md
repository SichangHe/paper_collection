                                        Pushing the Envelope of Optimization Modulo Theories
                                              with Linear-Arithmetic Cost Functions ?

                                                                   Roberto Sebastiani and Patrick Trentin

                                                                        DISI, University of Trento, Italy
arXiv:1410.5568v2 [cs.LO] 16 Jan 2015




                                                                                 NOTE
                                                 This is an extended version of a paper published at TACAS 2015 [24].
                                                               Latest update: Friday 10th September, 2021


                                                Abstract. In the last decade we have witnessed an impressive progress in the
                                                expressiveness and efficiency of Satisfiability Modulo Theories (SMT) solving
                                                techniques. This has brought previously-intractable problems at the reach of state-
                                                of-the-art SMT solvers, in particular in the domain of SW and HW verifica-
                                                tion. Many SMT-encodable problems of interest, however, require also the ca-
                                                pability of finding models that are optimal wrt. some cost functions. In previous
                                                work, namely Optimization Modulo Theory with Linear Rational Cost Functions
                                                – OMT(LRA ∪ T ), we have leveraged SMT solving to handle the minimization
                                                of cost functions on linear arithmetic over the rationals, by means of a combina-
                                                tion of SMT and LP minimization techniques.
                                                In this paper we push the envelope of our OMT approach along three directions:
                                                first, we extend it to work with linear arithmetic on the mixed integer/rational
                                                domain, by means of a combination of SMT, LP and ILP minimization tech-
                                                niques; second, we develop a multi-objective version of OMT, so that to handle
                                                many cost functions simultaneously or lexicographically; third, we develop an
                                                incremental version of OMT, so that to exploit the incrementality of some OMT-
                                                encodable problems. An empirical evaluation performed on OMT-encoded veri-
                                                fication problems demonstrates the usefulness and efficiency of these extensions.


                                        1     Introduction

                                        In many contexts including automated reasoning (AR) and formal verification (FV)
                                        important decision problems are effectively encoded into and solved as Satisfiability
                                        Modulo Theories (SMT) problems. In the last decade efficient SMT solvers have been
                                        developed, that combine the power of modern conflict-driven clause-learning (CDCL)
                                        SAT solvers [18] with the expressiveness of dedicated decision procedures (T -solvers)
                                        for several first-order theories of practical interest like, e.g., those of linear arithmetic
                                        over the rationals (LRA) or the integers (LIA) or their combination (LRIA), those of
                                        non-linear arithmetic over the reals (N LRA) or the integers (N LIA), of arrays (AR),
                                        of bit-vectors (BV), and their combinations. (See [20, 21, 3] for an overview.) This has
                                        ?
                                            This work is supported by Semiconductor Research Corporation (SRC) under GRC Research
                                            Project 2012-TJ-2266 WOLF. We thank Alberto Griggio for support with M ATH SAT5 code.
brought previously-intractable problems at the reach of state-of-the-art SMT solvers, in
particular in the domain of software (SW) and hardware (HW) verification.
    Many SMT-encodable problems of interest, however, may require also the capabil-
ity of finding models that are optimal wrt. some cost function over arithmetical vari-
ables. (See e.g. [23, 16, 22] for a rich list of such applications.) For instance, in SMT-
based model checking with timed or hybrid systems (e.g. [2, 1]) you may want to find
executions which optimize the value of some parameter (e.g., a clock timeout value, or
the total elapsed time) while fulfilling/violating some property (e.g., find the minimum
time interval for a rail-crossing causing a safety violation).
    Surprisingly, only few works extending SMT to deal with optimization problems
have been presented in the literature [19, 8, 23, 11, 17, 9, 22, 16, 15, 5] –most of which
handle problems which are different to that addressed in this paper [19, 8, 11, 17, 9], see
related work below.
    Sebastiani and Tomasi [23, 22] presented two procedures for adding to SMT(LRA∪
T ) the functionality of finding models minimizing some LRA cost variable –T be-
ing some (possibly empty) stably-infinite theory s.t. T and LRA are signature-disjoint.
This problem is referred to as Optimization Modulo Theories with linear cost func-
tions on the rationals, OMT(LRA ∪ T ). (If T is the empty theory, then we refer to
it as OMT(LRA).) 1 These procedures combine standard SMT and LP minimization
techniques: the first, called offline, is much simpler to implement, since it uses an incre-
mental SMT solver as a black-box, whilst the second, called inline, embeds the search
for optimum within the CDCL loop schema, and as such it is more sophisticate and effi-
cient, but it requires modifying the code of the SMT solver. In [23, 22] these procedures
have been implemented on top of the M ATH SAT5 SMT solver [10] into a tool called
O PTI M ATH SAT, and an extensive empirical evaluation is presented.
    Li et al. [16] extended the OMT(LRA) problem by considering contemporarily
many cost functions for the input formula ϕ, namely {cost1 , ..., costk }, so that the
problem consists in enumerating k independent models for ϕ, each minimizing one
specific costi . 2 (Intuitively, enumerating such models is in general more efficient than
solving one optimization problem at the time, because it allows for sharing the SMT
search steps among different cost objectives.) In [16] they presented a novel offline
algorithm for OMT(LRA), and implemented it into the tool S YMBA. Unlike with the
procedures in [23, 22], the algorithm described in [16] does not use a LP minimiza-
tion procedure: rather, a sequence of blackbox calls to an underlying SMT solver (Z3)
allows for finding progressively-better solutions along some objective direction, either
forcing discrete jumps to some bounds induced by the inequalities in the problem, or
proving such objective is unbounded. S YMBA is used as backend engine of the SW
model checker UFO. 3 An empirical evaluation on problems derived from SW verifica-
tion shows the usefulness of this multiple-cost approach.
 1
   Importantly, both MaxSMT ([19, 8, 9]) and SMT with pseudo-Boolean constraints and costs
   [8] are straightforwardly encoded into OMT [23, 22].
 2
   More precisely, in [16] the set of objectives k1 , k2 , ... must be maximized, but the problem can
   be converted into a minimization problem by setting costi = −ki . As in [16], we remark also
   that this is not Pareto-optimality, where a single model optimizing all objectives is searched.
 3
   https://bitbucket.org/arieg/ufo/


                                                 2
    Larraz et al. [15] present incomplete SMT(N LIA) and MaxSMT(N LIA) proce-
dures, which use an OMT(LIA) tool as an internal component. The latter procedure,
called BCLT, is described neither in [15] nor in any previous publication; however, it
has been kindly made available to us by their authors upon request, together with a link
to the master student’s thesis describing it. 4
    Finally, we have been informed by a reviewer of an invited presentation given by
Bjørner and Phan two months after the submission of this paper [5], describing general
algorithms for optimization in SMT, including MaxSMT, incremental, multi-objective
and lexicographic OMT, Pareto-optimality, which are implemented into the tool νZ on
top of Z3. Remarkably, [5] presents specialized procedures for MaxSMT, and enriches
the offline OMT schema of [23, 22] with specialized algorithms for unbound-solution
detection and for bound-tightening.
    We are not aware of any other OMT tool currently available.
    We remark a few facts about the OMT tools in [23, 22, 16, 15]. First, none of them
has an incremental interface, allowing for pushing and popping subformulas (including
definitions of novel cost functions) so that to reuse previous search from one call to
the other; in a FV context this limitation is relevant, because often SMT backends are
called incrementally (e.g., in the previously-mentioned example of SMT-based bounded
model checking of timed&hybrid systems). Second, none of the above tools supports
mixed integer/real optimization, OMT(LRIA). Third, none of the above tools supports
both multi-objective optimization and integer optimization. Finally, neither S YMBA nor
BCLT currently handle combined theories.
    In this paper we push the envelope of the OMT(LRA ∪ T ) approach of [23, 22]
along three directions: (i) we extend it to work also with linear arithmetic on the mixed
integer/rational domain, OMT(LRIA ∪ T ), by means of a combination of SMT, LP
and ILP minimization techniques; (ii) we develop a multi-objective version of OMT,
so that to handle many cost functions simultaneously or lexicographically; (iii) we de-
velop an incremental version of OMT, so that to exploit the incrementality of some
OMT-encodable problems. We have implement these novel functionalities in O PTI -
M ATH SAT. An empirical evaluation performed on OMT-encoded formal verification
problems demonstrates the usefulness and efficiency of these extensions.

Content. The paper is organized as follows: in §2 we provide the necessary background
knowledge on SMT and OMT; in §3 we introduce and discuss the above-mentioned
novel extensions of OMT; in §4 we perform an empirical evaluation of such procedures.


Other Related Work The idea of optimization in SMT was first introduced by Nieuwen-
huis & Oliveras [19], who presented an abstract logical framework of “SMT with
progressively stronger theories” (e.g., where the theory is progressively strengthened
by every new approximation of the minimum cost), and present implementations for
MaxSMT based on this framework. Cimatti et al. [8] introduced the notion of “The-
ory of Costs” C to handle PB cost functions and constraints by an ad-hoc and inde-
pendent “C-solver” in the standard lazy SMT schema, and implemented a variant of
 4
     http://upcommons.upc.edu/pfc/handle/2099.1/14204?locale=en.


                                           3
MathSAT tool able to handle SMT with PB constraints and to minimize PB cost func-
tions. Cimatti et al. [9] presented a “modular” approach for MaxSMT, combining a
lazy SMT solver with a MaxSAT solver, which can be used as blackboxes. We recall
that SMT with PB functions and MaxSMT can be encoded into each other, and that
both are strictly less general than the OMT(LRA ∪ T ) problems (see [23, 22]).
     Two other forms of optimization in SMT, which are quite different from the one
presented in our work, have been proposed in the literature. Dillig et al. [11] addressed
the problem of finding partial models for quantified first-order formulas modulo the-
ories, which minimize the number of free variables which are assigned a value from
                                                                       def
the domain.Quoting an example from [11], given the formula ϕ = (x + y + w >
0) ∨ (x + y + z + w < 5), the partial assignment {z = 0} satisfies ϕ because every to-
tal assignment extending it satisfies ϕ and is minimum because there is no assignment
satisfying ϕ which assigns less then one variable. They proposed a general proce-
dure addressing the problem for every theory T admitting quantifier elimination, and
implemented a version for LIA and EU F into the M ISTRAL tool. Manolios and Pa-
pavasileiou [17] proposed the “ILP Modulo Theories” framework as an alternative to
SAT Modulo Theories, which allows for combining Integer Linear Programming with
decision procedures for signature-disjoint stably-infinite theories T ; they presented a
general algorithm by integrating the Branch&Cut ILP method with T -specific decision
procedures, and implemented it into the I NEZ tool. Notice that the approach of [17]
cannot combine ILP with LRA, since LIA and LRA are not signature-disjoint. (See
Definition 2 in [17].) Also, the objective function is defined on the Integer domain. We
understand that neither of the above-mentioned works can handle the problem addressed
in this paper, and vice versa. (See [22] for a discussion on this topic.)


2     Background
In this section we provide the necessary background on SMT and OMT.

2.1   Satisfiability Modulo Theories
We assume a basic background knowledge on first-order logic and on CDCL SAT solv-
ing [18]. We consider some first-order theory T , and we restrict our interest to ground
formulas/literals/atoms in the language of T (T -formulas/literals/atoms hereafter).
    A theory solver for T , T -solver, is a procedure able to decide the T -satisfiability of
a conjunction/set µ of T -literals. If µ is T -unsatisfiable, then T -solver returns UNSAT
and a set/conjunction η of T -literals in µ which was found T -unsatisfiable; η is called
a T -conflict set, and ¬η a T -conflict clause. If µ is T -satisfiable, then T -solver returns
SAT ; it may also be able to return some unassigned T -literal l 6∈ µ from a set of all
available T -literals,Ws.t. {l1 , ..., ln } |=T l, where {l1 , ..., ln } ⊆ µ. We call this process
                       n
T -deduction and ( i=1 ¬li ∨ l) a T -deduction clause. Notice that T -conflict and T -
deduction clauses are valid in T . We call them T -lemmas.
    Given a T -formula ϕ, the formula ϕp obtained by rewriting each T -atom in ϕ into a
fresh atomic proposition is the Boolean abstraction of ϕ, and ϕ is the refinement of ϕp .
Notationally, we indicate by ϕp and µp the Boolean abstraction of ϕ and µ, and by ϕ

                                                4
and µ the refinements of ϕp and µp respectively. With a little abuse of notation, we say
that µp is T -(un)satisfiable iff µ is T -(un)satisfiable. We say that the truth assignment
µ propositionally satisfies the formula ϕ, written µ |=p ϕ, if µp |= ϕp .
    In a lazy SMT(T ) solver, the Boolean abstraction ϕp of the input formula ϕ is given
as input to a CDCL SAT solver, and whenever a satisfying assignment µp is found s.t.
µp |= ϕp , the corresponding set of T -literals µ is fed to the T -solver; if µ is found
T -consistent, then ϕ is T -consistent; otherwise, T -solver returns a T -conflict set η
causing the inconsistency, so that the clause ¬η p is used to drive the backjumping and
learning mechanism of the SAT solver. The process proceeds until either a T -consistent
assignment µ is found (ϕ is T -satisfiable), or no more assignments are available (ϕ is
T -unsatisfiable).
    Important optimizations are early pruning and T -propagation. The T -solver is in-
voked also when an assignment µ is still under construction: if it is T -unsatisfiable, then
the procedure backtracks, without exploring the (possibly many) extensions of µ; if it
is T -satisfiable, and if the T -solver is able to perform a T -deduction
                                                                 Wn         {l1 , ..., ln } |=T l,
then l can be unit-propagated, and the T -deduction clause ( i=1 ¬li ∨ l) can be used
in backjumping and learning. To this extent, in order to maximize the efficiency, most
T -solvers are incremental and backtrackable, that is, they are called via a push&pop
interface, maintaining and reusing the status of the search from one call and the other.
    Another optimization is pure-literal filtering: if some LRA-atoms occur only pos-
itively [resp. negatively] in the original formula (learned clauses are ignored), then we
can safely drop every negative [resp. positive] occurrence of them from the assignment
µ to be checked by the T -solver [21]. Intuitively, since such occurrences play no role in
satisfying the formula, the resulting partial assignment µp 0 still satisfies ϕp . The benefits
of this action are twofold: (i) it reduces the workload for the T -solver by feeding to it
smaller sets; (ii) it increases the chance of finding a T -consistent satisfying assignment
by removing “useless” T -literals which may cause the T -inconsistency of µ.
    The above schema is a coarse abstraction of the procedures underlying most state-
of-the-art SMT tools. The interested reader is pointed to, e.g., [20, 21, 3] for details.

2.2   Optimization Modulo Theories
We recall the basic ideas about OMT(LRA ∪ T ) and about the inline procedure in
[23, 22]. In what follows, T is some stably-infinite theory with equality s.t. LRA and
T are signature-disjoint. (T can be a combination of theories.) We call an Optimiza-
tion Modulo LRA ∪ T problem, OMT(LRA ∪ T ), a pair hϕ, costi such that ϕ is an
SMT(LRA ∪ T ) formula and cost is an LRA variable occurring in ϕ, representing
the cost to be minimized. The problem consists in finding a LRA-model M for ϕ (if
any) whose value of cost is minimum. We call an Optimization Modulo LRA problem
(OMT(LRA)) an OMT(LRA ∪ T ) problem where T is empty. If ϕ is in the form
ϕ0 ∧ (cost < c) [resp. ϕ0 ∧ ¬(cost < c)] for some value c ∈ Q, then we call c an upper
bound [resp. lower bound] for cost. If ub [resp. lb ] is the minimum upper bound [resp.
the maximum lower bound] for ϕ, we also call the interval [lb, ub[ the range of cost.
Remark 1. [23, 22] explain a general technique to pass from OMT(LRA) to OMT(LRA∪
T ) by exploiting the Delayed Theory Combination technique [6] implemented in M ATH -
SAT5. It is easy to see that this holds also for LIA and LRIA. Therefore, for the sake

                                                5
of brevity and readability, hereafter we consider the case where T is the empty theory
(OMT(LRA), OMT(LIA) or OMT(LRIA)), referring the reader to [23, 22] for a
detailed explanation about how to handle the general case.
     In the inline OMT(LRA) schema, the procedure takes as input a pair hϕ, costi, plus
optionally values for lb and ub (which are implicitly considered to be −∞ and +∞ if
                                                                                 def
not present), and returns the model M of minimum cost and its cost u = M(cost);
it returns the value ub and an empty model if ϕ is LRA-inconsistent. Notice that by
providing a lower bound lb [resp. an upper bound ub ] the user implicitly assumes the
responsibility of asserting there is no model whose cost is lower than lb [there is a model
whose cost is ub ]. The standard CDCL-based schema of the SMT solver is modified
as follows.
Initialization. the variables l, u (defining the current range) are initialized to lb and ub
respectively, the variable pivot (defining the pivot in binary search) is not initialized,
the LRA-atom PIV is initialized to > and the output model M is initialized to be an
empty model.
Range Updating & Pivoting. Every time the search of the CDCL SAT solver gets
back to decision level 0, the range [l, u[ is updated s.t. u [resp. l ] is assigned the lowest
[resp. highest] value ui [resp. li ] such that the atom (cost < ui ) [resp. ¬(cost < li )] is
currently assigned at level 0. Then the heuristic function BinSearchMode() is invoked,
which decides whether to run the current step in binary- or in linear-search mode: in
the first case (which can occur only if l > −∞ and u < ∞) a value pivot ∈ ]l, u[ is
                                                                             def
computed (e.g. pivot = (l + u)/2), and the (possibly new) atom PIV = (cost < pivot)
is decided to be true (level 1) by the SAT solver. This temporarily restricts the cost range
to [l, pivot[. Then the CDCL solver proceeds its search, as in §2.1.
Decreasing the Upper Bound. When an assignment µ is generated s.t. µp |= ϕp and
which is found LRA-consistent by LRA-Solver, µ is also fed to LRA-Minimize, re-
                                                                      def
turning the minimum cost min of µ; then the unit clause Cµ = (cost < min) is learned
and fed to the backjumping mechanism, which forces the SAT solver to backjump to
level 0, then unit-propagating (cost < min). This restricts the cost range to [l, min[.
LRA-Minimize is embedded within LRA-Solver –it is a simple extension of the LP
algorithm in [12]– so that it is called incrementally after it, without restarting its search
from scratch. Notice that the clauses Cµ ensure progress in the minimization every time
that a new LRA-consistent assignment is generated.
Termination. The procedure terminates when the embedded SMT-solving algorithm
reveals an inconsistency, returning the current values of u and M.
     As a result of these modifications, we also have the following typical scenario (see
Figure 1).
Increasing the Lower Bound. In binary-search mode, when a conflict occurs and the
conflict analysis of the SAT solver produces a conflict clause in the form ¬PIV ∨ ¬η 0
s.t. all literals in η 0 are assigned true at level 0 (i.e., ϕ ∧ PIV is LRA-inconsistent), then
the SAT solver backtracks to level 0, unit-propagating ¬PIV. This case permanently
restricts the cost range to [pivot, u[.
     Notice that, to guarantee termination, binary-search steps must be interleaved with
linear-search ones infinitely often. We refer the reader to [23, 22] for details and for a
description of further improvements to the basic inline procedure.

                                              6
                                                          ϕ
                                    (cost < pivot0)




                conflict                                   lb0         pivot0               ub0

                                                      µ |= ϕ


                                                          ϕ
                                    (cost < pivot0)
                                                          ϕ ∧ ¬(cost < pivot0)




                conflict                                   lb0         pivot0               ub0

                                                      µ |= ϕ


                                                          ϕ
                                    (cost < pivot0)
                                                          ϕ ∧ ¬(cost < pivot0)
                                    (cost < pivot1)



                               ϕ ∧ ¬(cost < pivot0) ∧ ¬ηi ∧ (cost < mi) ∧ (cost < pivot1)




                conflict                                   lb0         pivot0        pivot1 ub0

                         ηi ⊆ µi                      µ |= ϕ                    mi
                      mi = mincost(µi)


Fig. 1. One piece of possible execution of an inline procedure. (i) Pivoting on (cost < pivot0 ).
(ii) Increasing the lower bound to pivot0 . (iii) Decreasing the upper bound to mincost (µi ).




                                                      7
3      Pushing the envelope of OMT

3.1     From OMT(LRA) to OMT(LRIA)

We start from the observation that the only LRA-specific components of the inline
OMT(LRA) schema of §2.2 are the T -solving and minimizing procedures. Thus, under
the assumption of having an efficient LRIA-Solver already implemented inside the
embedded SMT solver –like we have in M ATH SAT5 [14]– the schema in §2.2 can be
adapted to LRIA by invoking an LRIA-specific minimizing procedure each time a
truth-assignment µ s.t. µp |= ϕp is generated.

Remark 2. Notice that in principle in LIA the minimization step is not strictly nec-
essary if the input problem is lower bounded. In fact, to find the optimum cost value
it would be sufficient to iteratively enumerate and remove each solution found by the
standard implementation of the LIA-Solver, because each step guarantees an improve-
ment of at least 1. Minimizing the cost value at each iteration of the SMT engine,
however, allows for speeding up the optimization search by preventing the current truth
assignment µ from being generated more than once. In addition, the availability of a
specialized LIA-Minimize procedure is essential to recognize unbounded problems.

    The problem of implementing an efficient OMT(LRIA) tool reduces thus to that
of implementing an efficient minimizer in LRIA, namely LRIA-Minimize, which
exploits and cooperates in synergy with the other components of the SMT solver. In
particular, it is advisable that LRIA-Minimize is embedded into the LRIA-Solver, so
that it is called incrementally after the latter has checked the LRIA-consistency of the
current assignment µ. (Notice that, e.g., embedding into LRIA-Minimize a MILP tool
from the shelf would not match these requirements.) To this extent, we have investigated
both theoretically and empirically three different schemas of Branch&Bound LRIA-
Minimize procedure, which we call basic, advanced and truncated.
    The first step performed by LRIA-Minimize is to check whether cost is lower
bounded. Since a feasible MILP problem is unbounded if and only if its corresponding
continuous relaxation is unbounded [7],5 we run LRA-Minimize on the relaxation of
µ. If the relaxed problem if unbounded, then LIA-Minimize returns −∞; otherwise,
LRA-Minimize returns the minimum value of cost in the relaxed problem, which we
set as the current lower bound lb for cost in the original problem. We also initialize the
upper bound ub for cost to the value M(cost), where M is the model returned by the
most recent call to the LRIA-Solver on µ.
    Then we explore the solution space by means of an LP-based Branch&Bound pro-
cedure that reduces the original MILP problem to a sequence of smaller sub-problems,
which are solved separately.
Basic Branch&Bound. We describe first a naive version of the Branch&Bound min-
imization procedure. (Since it is very inefficient, we present it only as a baseline for
 5
     As in [7], by “continuous relaxation” –henceforth simply “relaxation”– we mean that the inte-
     grality constraints on the integer variables are relaxed, so that they can take fractional values.


                                                   8
the other approaches.) We first invoke LRA-Minimize on the relaxation of the cur-
rent LRIA problem. If the relaxation is found LRA-unsatisfiable, then also the orig-
inal problem is LRIA-unsatisfiable, and the procedure backtracks. Otherwise, LRA-
Minimize returns a minimum-cost model M of cost min. If such solution is LRIA-
compliant, then we can return M and min, setting ub = min. (By “LRIA-compliant
solution” here we mean that the integer variables are all given integer values, whilst
rational variables can be given fractional values.)
    Otherwise, we select an integer variable xj which is given a fractional value x∗j in
M as branching variable, and split the current problem into a pair of complementary
sub-problems, by augmenting them respectively with the linear cuts (xj ≤ bx∗j c) and
(xj ≥ dx∗j e). Then, we separately explore each of these two sub-problems in a recursive
fashion, and we return the best of the two minimum values of cost which is found in
the two branches, with the relative model.
    In order to make this exploration more efficient, as the recursive Branch&Bound
search proceeds, we keep updating the upper bound ub to the current best value of cost
corresponding to an LRIA-compliant solution. Then, we can prune all sub-problems
in which the LRA optimum cost value is greater or equal than ub, as they cannot
contain any better solution.
Advanced Branch&Bound. Unlike the basic scheme, the advanced Branch&Bound
is built on top of the LRIA-Solver of M ATH SAT5 and takes advantage of all the ad-
vanced features for performance optimization that are already implemented there [14].
In particular, we re-use its very-efficient internal Branch&Bound procedure for LRIA-
solving, which exploits historical information to drive the search and achieves higher
pruning by back-jumping within the Branch&Bound search tree, driven by the analysis
of unsatisfiable cores. (We refer the reader to [14] for details.)
    We adapt the LRIA-solving algorithm of [14] to minimization as follows. As be-
fore, the minimization algorithm starts by setting ub = M(cost), M being the model
for µ which was returned by the most recent call to the LRIA-Solver. Then the linear
cut (cost < ub) is pushed on top of the constraint stack of the LRIA-Solver, which
forces the search to look for a better LRIA-compliant solution than the current one.
    Then, we use the internal Branch&Bound component of the LRIA-Solver to seek
for a new LRIA-compliant solution. The first key modification is that we invoke
LRA-Minimize on each node of Branch&Bound search tree to ensure that x∗LP is opti-
mal in the LRA domain. The second modification is that, every time a new solution is
found –whose cost ub improves the previous upper bound by construction– we empty
the stack of LRIA-Solver, push there a new cut in the form (cost < ub) and restart
the search. Since the problem is known to be bounded, there are only a finite number of
LRIA-compliant solutions possible that can be removed from the search space. There-
fore, the set of constraints is guaranteed to eventually become unsatisfiable, and at that
point ub is returned as optimum cost value in µ to the SMT solver, which learns the
                 def
unit clause Cµ = (cost < ub).
Truncated Branch&Bound. We have empirically observed that in most cases the
above scheme is effective enough that a single loop of advanced Branch&Bound is
sufficient to find the optimal solution for the current truth assignment µ. However, the
advanced Branch&Bound procedure still performs an additional loop iteration to prove


                                            9
 that such solution is indeed optimal, which causes additional unnecessary overhead. An-
 other drawback of advanced B&B is that for degenerate problems the Branch&Bound
 technique is very inefficient. In such cases, it is more convenient to interrupt the B&B
                                                                              def
 search and simply return ub to the SMT solver, s.t. the unit clause Cµ = (cost < ub)
 is learned; in fact, in this way we can easily re-use the entire stack of LRIA-Solver
 routines in M ATH SAT5 to find an improved solution more efficiently.
      Therefore, we have implemented a “sub-optimum” variant of LRIA-Minimize in
 which the inner LRIA-Solver minimization procedure stops as soon as either it finds
 its first solution or it reaches a certain limit on the number of branching steps. The draw-
 back of this variant is that, in some cases, it analyzes a truth assignment µ (augmented
 with the extra constraint (cost < ub)) more than once.

 3.2   Multiple-objective OMT
 We generalize the OMT(LRIA) problem to multiple cost functions as follows. (As
 with plain OMT(LRIA), the extension to OMT(LRIA ∪ T ) follows the technique
                                                                                         def
 described in [23, 22].) A multiple-cost OMT(LRIA) problem is a pair hϕ, Ci s.t C =
 {cost1 , ..., costk } is a set of LRIA-variables occurring in ϕ, and consists in finding a
 set of LRIA-models {M1 , ..., Mk } s.t. each Mi makes costi minimum. We extend
 the OMT(LRA) [OMT(LRIA) ] procedures of §2.2 and §3.1 to handle multiple-cost
 problems. The procedure works in linear-search mode only.
 Remark 3. Since the linear-search versions of the procedures in §2.2 and §3.1 differ
 only for the fact that they invoke LRA-Minimize and LRIA-Minimize respectively,
 here we do not distinguish between them. We only implicitly make the assumption
 that the LRIA-Minimize does not work in truncated mode, so that it is guaranteed to
 find a minimum in one run. Such assumption is not strictly necessary, but it makes the
 explanation easier.
      It takes as input a pair hϕ, Ci and returns a list of minimum-cost models {M1 , ..., Mk },
 plus the corresponding list of minimum values {u1 , ..., uk }. (If ϕ is LRIA-inconsistent,
 it returns ui = +∞ for every i.)
 Initialization. First, we set ui = +∞ for every i, and we set C ∗ = C, s.t. C ∗ is the list
 of currently-active cost functions.
 Decreasing the Upper Bound. When an assignment µ is generated s.t. µp |= ϕp and
 which is found LRIA-consistent by LRIA-Solver, µ is also fed to LRIA-Minimize.
 For each costi ∈ C ∗ :
  (i) LRIA-Minimize finds an LRIA-model M for µ of minimum cost mini ;
 (ii) if mini is −∞, then there is no more reason to investigate costi , so that we set
      ui = −∞ and Mi = M, and costi is dropped from C ∗ ;
(iii) if mini < ui , then we set ui = mini and Mi = M.
 As with the single-cost versions of §2.2, LRIA-Minimize is embedded within LRIA-
 Solver, so that it is called incrementally after it, without restarting its search from
 scratch. After that, the clause
                                    def
                                         _
                                 Cµ =        (costi < ui )                            (1)
                                       costi ∈C ∗


                                              10
            cost1                                  def
                                                ϕ = (1 ≤ y) ∧ (y ≤ 3)
                 µ1              µ2               ∧ (((1 ≤ x) ∧ (x ≤ 3)) ∨ (x ≥ 4))
3
                                                  ∧ (cost1 = −y) ∧ (cost2 = −x − y)
                            cost2
                                                    def
                                                µ1 = {(1 ≤ y), (y ≤ 3), (1 ≤ x), (x ≤ 3),
1                                                      (cost1 = −y), (cost2 = −x − y)}
                                                   def
                                                µ2 = {(cost1 = −y), (cost2 = −x − y),
 0    1         3     4                                (1 ≤ y), (y ≤ 3), (x ≥ 4),
                                                       (cost2 < −6)}

Fig. 2. In one possible execution over the LRA-formula ϕ, the CDCL-based SMT engine finds
the truth assignment µ1 first, which is found LRA-consistent by the LRA-solver. (For the sake
of readability, we’ve removed from the µi ’s the redundant literals like “¬(x ≥ 4)” from µ1 .)
Then the minimizer finds the minima min1 = −3, min2 = −6, the upper bounds are updated to
these values, and the clause (cost1 < −3) ∨ (cost2 < −6) is learned. The next LRA-consistent
assignment found is necessarily µ2 , from which the minimizer finds the minima min1 = −3,
min2 = −∞. Hence cost2 is dropped from C ∗ , and the unit clause (cost1 < −3) is learned,
making ϕ LRA-inconsistent, so that no more assignment is found and the procedure terminates.
In a luckier execution µ2 \ {(cost2 < −6)} is found first, thus the minimizer finds directly the
minima min1 = −3, min2 = −∞ s.t. (cost1 < −3) is learned, and the procedure terminates
without generating µ1 .


is learned, and the CDCL-based SMT solving process proceeds its search. Notice that,
since by construction µ ∧ Cµ |=LRIA ⊥, a theory-driven backjumping step [3] will
occur as soon as µ is extended to assign to true some literal of Cµ .
Termination. The procedure terminates either when C ∗ is empty or when ϕ is found
LRIA-inconsistent. (The former case is a subcase of the latter, because it would cause
the generation of an empty clause Cµ (1).)
     The clauses Cµ (1) ensure a progress in the minimization of one or more of the
costi ’s every time that a new LRIA-consistent assignment is generated. We notice
that, by construction, Cµ is such that µ ∧ Cµ |=LRIA ⊥, so that each µ satisfying
the original version of ϕ can be investigated by the minimizer only once. Since we
have only a finite number of such candidate assignments for ϕ, this guarantees the
termination of the procedure. The correctness and completeness is guaranteed by these
of LRIA-Minimize, which returns the minimum values for each such assignment.
     To illustrate the behaviour of our procedure, and to allow for a direct comparison
wrt. the procedure described in [16], in Figure 2 we present its execution on the toy ex-
ample LRA-problem in [16]. Notice that, unlike the algorithm in [16], our procedure is
driven by the Boolean search: each time a novel assignment is generated, it eagerly pro-
duces the maximum progress for as many costi ’s as possible. The algorithm described
in [16], instead, does not use a LP minimization procedure: rather, a sequence of black-
box calls to an underlying SMT solver (Z3) allows for finding progressively-better so-
lutions along some objective direction, either forcing discrete jumps to some bounds
induced by the inequalities in the problem, or proving such objective is unbounded.
    The procedure is improved in various ways. First, we notice that the clause Cµ
is strictly stronger than the clause Cµ0 which was generated with the previous truth


                                              11
assignment µ0 , so that Cµ0 can be safely dropped, keeping only one of such clauses
at a time. This is as if we had only one such clause whose literals are progressively
strengthened. Second, before step (i), the constraint (costi < ui ) can be temporarily
pushed into µ: if LRIA-Minimize returns UNSAT, then there is no chance to improve
the current value of ui , so that the above constraint can be popped from µ and step (ii)
and (iii) can be skipped for the current costi . Third, in case the condition in step (iii)
holds, it is possible to learn also the LRIA-valid clause (costi < ui ) → (costi < u0i )
s.t. u0i is the previous value of ui . This allows for “activating” all previously-learned
clauses in the form ¬(costi < u0i ) ∨ C as soon as (costi < ui ) is assigned to true.

Lexicographic combination. As in [5], we easily extend our inline procedure to deal
with the lexicographic combination of multiple costs {cost1 , ..., costk }. This works as
follows. We start by looking for a minimum for cost1 : as soon as a minimum u1 with
its model M1 is found, if u1 = −∞ then we stop, otherwise we substitute inside ϕ the
                                                        def
unit clause (cost1 < u1 ) with (cost1 = u1 ), we set u2 = M1 (cost2 ), and we look for
the minimum of cost2 in the resulting formula. This is repeated until all costi ’s have
been considered.

3.3     Incremental OMT
Many modern SMT solvers, including M ATH SAT5, provide a stack-based incremental
interface (see e.g. [13]), by which it is possible to push/pop sub-formulas φi into a
                       def
stack of formulas Φ = {φ1 , ..., φk }, and then to check incrementally the satisfiability of
Vk
   i=1 φi . The interface maintains the status of the search from one call to the other, in
particular it records the learned clauses (plus other information). Consequently, when
invoked on Φ, the solver can reuse a clause C which was learned during a previous call
on some Φ0 if C was derived only from clauses which are still in Φ. 6 In particular, if
Φ0 ⊆ Φ, then the solver can reuse all clauses learned while solving Φ0 .
     In particular, in M ATH SAT5 incrementality is achieved by first rewriting Φ into
{A1 → φ1 , ..., Ak → φk }, each Ai being a fresh Boolean variable, and then by running
the SMT solver under the assumption of the variables {A1 , ..., Ak }, in such a way that
every learned clause which is derived from some φi is in the form ¬Ai ∨ C [13]. Thus
it is possible to safely keep the learned clause from one call to the other because, if φi
is popped from Φ, then Ai is no more assumed, so that the clause ¬Ai ∨ C is inactive.
(Such clauses can be garbage-collected from time to time to reduce the overhead.)
     Since none of the OMT tools in [23, 22, 16, 15] provides an incremental interface,
nor such paper explains how to achieve it, here we address explicitly the problem of
making OMT incremental.
     We start noticing that if (i) the OMT tool is based on the schema in §2.1 or on
its LRIA and multiple-cost extensions of §3.1 and §3.2, and (ii) the embedded SMT
solver has an incremental interface, like that of M ATH SAT5, then an OMT tool can be
easily made incremental by exploiting the incremental interface of its SMT solver.
     In fact, in our OMT schema all learned clauses are either T -lemmas or they are
derived from T -lemmas and some of the subformulas φi ’s, with the exception of the
 6
     Provided C was not discharged in the meantime.


                                              12
             def                                    def                                  def
clauses
W        Cµ = (cost < min) (§2.2) [resp. Cµ = (cost < min) (§3.1) and Cµ =
  costi ∈C ∗ (costi < ui ) (§3.2),] which are “artificially” introduced to ensure progress
in the minimization steps. (This holds also for the unit clauses (PIV) which are learned
in an improved version, see [23, 22].) Thus, in order to handle incrementality, it suffices
to drop only these clauses from one OMT call to the other, while preserving all the
others, as with incremental SMT.
    In a more elegant variant of this technique, which we have used in our implemen-
tation, at each incremental call to OMT (namely the k-th call) a fresh Boolean vari-
able A(k) is assumed. Whenever a new minimum min is found, the augmented clause
     def                                                      def
Cµ∗ = ¬A(k) ∨ (cost < min) is learned instead of Cµ = (cost < min). In the sub-
sequent calls to OMT, A(k) is no more assumed, so that the augmented clauses Cµ∗ ’s
which have been learned during the k-th call are no more active.
    Notice that in this process reusing the clauses that are learned by the underlying
SMT-solving steps is not the only benefit. In fact also the learned clauses in the form
                                                                      def
¬(cost < min) ∨ C which may be produced after learning Cµ = (cost < min) are
preserved to the next OMT calls. (Same discourse holds for the Cµ ’s of §3.1 and §3.2.)
In the subsequent calls such clauses are initially inactive, but they can be activated as
soon as the current minimum, namely min0 , becomes smaller or equal than min and the
novel clause (cost < min0 ) is learned, so that (cost < min) can be T -propagated or
(¬(cost < min0 ) ∨ (cost < min)) can be T -learned. This allows for reusing lots of
previous search.


4     Experimental Evaluation

We have extended O PTI M ATH SAT [23, 22] by implementing the advanced and trun-
cated B&B OMT(LRIA ∪ T ) procedures described in §3.1. On top of that, we have
implemented our techniques for multi-objective OMT (§3.2) —including the lexico-
graphic combination— and incremental OMT (§3.3). Then, we have investigated em-
pirically the efficiency of our new procedures by conducing two different experimental
evaluations, respectively on OMT(LRIA) (§4.1) and on multi-objective and incremen-
tal OMT(LRA) (§4.2). All tests in this section were executed on two identical 8-core
2.20Ghz Xeon machines with 64 GB of RAM and running Linux with 3.8-0-29 kernel,
with an enforced timeout of 1200 seconds.
    For every problem in this evaluation, the correctness of the minimum costs found
by O PTI M ATH SAT and its competitor tools, namely “min”, have been cross-checked
with the SMT solver Z3, by checking both the inconsistency of ϕ ∧ (cost < min) and
the consistency of ϕ ∧ (cost = min). In all tests, when terminating, all tools returned
the correct results. To make the experiments reproducible, the full-size plots, a Linux
binary of O PTI M ATH SAT, the input OMT problems, and the results are available. 7
 7
     http://disi.unitn.it/˜trentin/resources/tacas15.tar.gz;          BCLT
     is available at http://www.lsi.upc.edu/˜oliveras/bclt.gz; S YMBA is
     available at https://bitbucket.org/arieg/symba/src; νZ is available at
     http://rise4fun.com/z3opt.


                                            13
                                                                       Tool:          #inst. #solved #timeout time
                                                                       BCLT             544      500       44 93040
                                                                       νZ               544      544        0 36089
                                                                       OptiM.-adv-lin   544      544        0 91032
                                                                       OptiM.-adv-bin   544      544        0 99214
                                                                       OptiM.-adv-ada 544        544        0 88750
                                                                       OptiM.-trn-lin   544      544        0 91735
                                                                       OptiM.-trn-bin   544      544        0 99556
                                                                       OptiM.-trn-ada   544      544        0 88730
                                 104                                                                                 104

                                 103                                                                                 103
      optimathsat-trn-ada (s.)




                                                                                          optimathsat-trn-ada (s.)
                                 102                                                                                 102

                                 101                                                                                 101

                                 100                                                                                 100

                                 10-1                                                                                10-1

                                 10-2                                                                                10-2

                                      -3
                                 10                                                                                  10-3 -3
                                      10-3   10-2   10-1   100   101    102   103   104                                10      10-2   10-1   100   101   102   103   104
                                                           bclt (s.)                                                                         muz3 (s.)

Fig. 3. A table comparing the performances of BCLT, νZ and different configurations of O PTI -
M ATH SAT on Bounded Model Checking problems. Scatterplots: pairwise comparisons between
O PTI M ATH SAT-trn-ada and BCLT (left) and νZ (right).


4.1                      Evaluation of OMT(LRIA) procedures

Here we consider three different configurations of O PTI M ATH SAT based on the search
schemas (linear vs. binary vs. adaptive, denoted respectively by “- LIN ”, “- BIN ” and “-
ADA”) presented in §2.2; the adaptive strategy dynamically switches the search schemas
between linear and binary search, based on the heuristic described in [22]. We run
O PTI M ATH SAT both with the advanced and truncated branch&bound minimization
procedures for LRIA presented in §3.1, denoted respectively by “- ADV ” and “- TRN ”.
    In order to have a comparison of O PTI M ATH SAT with both νZ and BCLT, in this
experimental evaluation we restricted our focus on OMT(LIA) only. Here we do not
consider S YMBA, since it does not support OMT(LIA). We used as benchmarks a set
of 544 problems derived from SMT-based Bounded Model Checking and K-Induction
on parametric problems, generated via the SAL model checker. 8
    The results of this evaluation are shown in Figure 3. By looking at the table, we
observe that the best O PTI M ATH SAT configuration on these benchmarks is - TRN - ADA,
which uses the truncated branch&bound approach within the LIA-Minimize procedure
with adaptive search scheme. We notice that the differences in performances among the
various configurations of O PTI M ATH SAT are small on these specific benchmarks.
    Comparing the O PTI M ATH SAT versions against BCLT and νZ, we notice that O P -
TI M ATH SATand νZ solve all input formulas regardless of their configuration, νZ hav-
ing better time performances, whilst BCLT timeouts on 44 problems.
 8
     http://sal.csl.sri.com/.


                                                                                                        14
4.2    Evaluation of Incremental and Multiple-objective OMT

As mentioned in Section §1, so far BCLT does not feature multi-objective OMT, and
neither S YMBA nor BCLT implement incremental OMT. Thus, in order to test the ef-
ficiency of our multiple-objective OMT approach, we compared three versions of O P -
TI M ATH SAT against the corresponding versions of νZ and the two best-performing
versions of S YMBA presented in [16], namely S YMBA(100) and S YMBA(40)+OPT- Z 3.
     So far S YMBA handles only OMT(LRA), without combinations with other theo-
ries. Moreover, it currently does not support strict inequalities inside the input formulas.
Therefore for both comparisons we used as benchmarks the multiple-objective prob-
lems which were proposed in [16] to evaluate S YMBA, which were generated from a
set of C programs used in the 2013 SW Verification Competition. 9 Also, S YMBA com-
putes both the minimum and the maximum value for each cost variable, and there is no
way of restricting its focus only on one direction. Consequently, in our tests we have
forced also O PTI M ATH SATand νZ to both minimize and maximize each objective.
(More specifically, they had to minimize both costi and −costi , for each costi .)
     We tested three different configurations of νZ and O PTI M ATH SAT:

 – SINGLEOBJECTIVE: each tool is run singularly on the single-objective problems
   hϕ, costi i and hϕ, −costi i for each costi , and the cumulative time is taken;
 – INCREMENTAL: as above, using the incremental version of each tool, each time
   popping the definition of the previous cost and pushing the new S   one;
 – MULTIOBJECTIVE: each tool is run in multi-objective mode with i {costi , −costi }.

    Figure 4 provides the cumulative plots and the global data of the performance of all
procedures under test, whilst Figure 5 reports pairwise comparisons.
    We first compare the different versions of O PTI M ATH SAT (see Figure 4 and the first
row of Figure 5). By looking at Figure 4 and at the top-left plot in Figure 5, we observe a
uniform and relevant speedup when passing from non-incremental to incremental OMT.
This is explained by the possibility of reusing learned clauses from one call to the other,
saving thus lots of search, as explained in §3.3.
    By looking at Figure 4 and at the top-center plot in Figure 5, we observe a uniform
and drastic speedup in performance –about one order of magnitude– when passing from
single-objective to multiple-objective OMT. We also notice (top-right plot in Figure 5)
that this performance is significantly better than that obtained with incremental OMT.
Analogous considerations hold for νZ.
    We see two main motivations for this improvement in performance with our multiple-
objective OMT technique: first, every time a novel truth assignment is generated, the
value of many cost functions can be updated, sharing thus lots of Boolean and LRA
search; second, the process of certifying that there is no better solution, which typically
requires a significant part of the overall OMT search [22], here is executed only once.
    In the second row of Figure 5 we compare the performances of O PTI M ATH SAT-
MULTI - OBJECTIVE against the two versions of S YMBA and νZ- MULTI - OBJECTIVE .
We observe that multi-objective O PTI M ATH SAT performs much better than the default
 9
     https://bitbucket.org/liyi0630/symba-bench.


                                            15
                                                 Tools Performances
                              105

                              104

                              103
             Cum. time (s.)
                              102
                                                                   optimathsat-sequential
                              101                                  symba(100)
                                                                   vZ-singleobjective
                              100                                  vZ-incremental
                                                                   optimathsat-incremental
                                                                   vZ-multiobjective
                              10-1                                 symba(40)+opti(z3)
                                                                   optimathsat-multiobjective
                              10-2 0     200       400       600         800      1000      1200
                                                         No. solved
                               Tool:                       #inst. #solved #timeout time
                               S YMBA(100)                 1103 1091         12    10917
                               S YMBA(40)+OPT- Z 3         1103 1103          0    1128
                               νZ-multiobjective           1103 1090         13    1761
                               νZ-incremental              1103 1100          3    8683
                               νZ-singleobjective          1103 1101          2    10002
                               optimathsat-multiobjective 1103 1103           0     901
                               optimathsat-incremental     1103 1103          0    3477
                               optimathsat-singleobjective 1103 1103          0    16161

Fig. 4. Comparison of different versions of O PTI M ATH SAT and S YMBA on the SW verification
problems in [16]. (Notice the logarithmic scale of the vertical axis in the cumulative plots.)


configuration of S YMBA, and significantly better than both S YMBA(40)+OPT- Z 3 and
νZ- MULTI - OBJECTIVE.
    We have also wondered how much the relative performances of O PTI M ATH SAT,
S YMBA and νZ depend on the relative efficiency of their underlying SMT solvers:
M ATH SAT5 for O PTI M ATH SAT and Z3 for S YMBA and νZ. Thus we have run both
M ATH SAT5 and Z3 on the set of problems ϕ ∧ (cost < min) derived from the orig-
inal benchmarks, and used their timings to divide the respective O PTI M ATH SAT and
S YMBA/νZ execution time values.10 These “normalized” results, which are shown in
the bottom row of Figure 5, seem to suggest that the better performances of O PTI -
M ATH SAT are not due to better performances of the underlying SMT solver.




10
     That is, each value represents the time taken by each OMT tool on hϕ, costi i divided by the
     time taken by its underlying SMT solver to solve ϕ ∧ (cost < min).


                                                          16
                                               103                                                                                                               103




                                                                                                                      optimathsat-multiobjective (s.)




                                                                                                                                                                                                                           optimathsat-multiobjective (s.)
                                                                                                                                                                                                                                                                      102


    optimathsat-incremental (s.)
                                               102                                                                                                               102

                                                                                                                                                                                                                                                                      101
                                               101                                                                                                               101


                                                                                                                                                                                                                                                                      100
                                               100                                                                                                               100


                                               10-1                                                                                                              10-1                                                                                                 10-1
                                                      10-1          100        101            102            103                                                          10-1        100         101      102       103                                                      10-1             100               101         102
                                                                optimathsat-sequential (s.)                                                                                       optimathsat-sequential (s.)                                                                        optimathsat-incremental (s.)

                                               103                                                                                                                                                                                                                    103
    optimathsat-multiobjective (s.)




                                                                                                                      optimathsat-multiobjective (s.)




                                                                                                                                                                                                                           optimathsat-multiobjective (s.)
                                               102                                                                                                                                                                                                                    102
                                                                                                                                                                 101


                                               101                                                                                                                                                                                                                    101

                                                                                                                                                                 100
                                               100                                                                                                                                                                                                                    100


                                               10-1                                                                                                              10-1                                                                                                 10-1
                                                           -1                       1
                                                      10            10   0
                                                                               10             10   2
                                                                                                             10   3
                                                                                                                                                                           10-1             100          101                                                                 10-1            100           101         102           103
                                                                         symba(100) (s.)                                                                                           symba(40)+opti(z3) (s.)                                                                              vZ-multiobjective (s.)
    optimathsat-multiobjective (unsat norm.)




                                                                                                                      optimathsat-multiobjective (unsat norm.)




                                                                                                                                                                                                                           optimathsat-multiobjective (unsat norm.)
                                                                                                                                                                                                                                                                      104
                                               103
                                                                                                                                                                      2
                                                                                                                                                                 10
                                                                                                                                                                                                                                                                      103
                                               102

                                                                                                                                                                 101                                                                                                  102
                                               101
                                                                                                                                                                                                                                                                      101
                                                                                                                                                                 100
                                               100
                                                                                                                                                                                                                                                                      100

                                               10-1                                                                                                              10-1                                                                                                 10-1
                                                      10-1         100       101        102            103                                                                10-1        100          101         102                                                           10-1      100           101     102       103         104
                                                                symba(100) (unsat norm.)                                                                                  symba(40)+opti(z3) (unsat norm.)                                                                      vZ-multiobjective (unsat norm.)



Fig. 5. First row: pairwise comparisons between different versions of O PTI M ATH SAT. Sec-
ond row: pairwise comparisons between O PTI M ATH SAT- MULTIOBJECTIVE, the two versions
of S YMBA and νZ- MULTIOBJECTIVE. Third row: “normalized” version of the plots in the sec-
ond row.



References

 1. G. Audemard, M. Bozzano, A. Cimatti, and R. Sebastiani. Verifying Industrial Hybrid Sys-
    tems with MathSAT. In Proc. BMC 2004, volume 119 of ENTCS. Elsevier, 2005.
 2. G. Audemard, A. Cimatti, A. Korniłowicz, and R. Sebastiani. SAT-Based Bounded Model
    Checking for Timed Systems. In Proc. FORTE’02., volume 2529 of LNCS. Springer, 2002.
 3. C. Barrett, R. Sebastiani, S. A. Seshia, and C. Tinelli. Satisfiability Modulo Theories, chap-
    ter 26, pages 825–885. In Biere et al. [4], February 2009.
 4. A. Biere, M. J. H. Heule, H. van Maaren, and T. Walsh, editors. Handbook of Satisfiability.
    IOS Press, February 2009.


                                                                                                                                                                                     17
 5. N. Bjorner and A.-D. Phan. νZ - Maximal Satisfaction with Z3. In Proc SCSS. Invited
    presentation., Gammart, Tunisia, December 2014. EasyChair Proceedings in Computing
    (EPiC). http://www.easychair.org/publications/?page=862275542.
 6. M. Bozzano, R. Bruttomesso, A. Cimatti, T. A. Junttila, S. Ranise, P. van Rossum, and R. Se-
    bastiani. Efficient Theory Combination via Boolean Search. Information and Computation,
    204(10):1493–1525, 2006.
 7. R. H. Byrd, A. J. Goldman, and M. Heller. Technical Note– Recognizing Unbounded Integer
    Programs. Operations Research, 35(1), 1987.
 8. A. Cimatti, A. Franzén, A. Griggio, R. Sebastiani, and C. Stenico. Satisfiability modulo
    the theory of costs: Foundations and applications. In TACAS, volume 6015 of LNCS, pages
    99–113. Springer, 2010.
 9. A. Cimatti, A. Griggio, B. J. Schaafsma, and R. Sebastiani. A Modular Approach to MaxSAT
    Modulo Theories. In SAT, volume 7962 of LNCS, July 2013.
10. A. Cimatti, A. Griggio, B. J. Schaafsma, and R. Sebastiani. The MathSAT 5 SMT Solver.
    volume 7795 of LNCS. Springer, 2013.
11. I. Dillig, T. Dillig, K. L. McMillan, and A. Aiken. Minimum Satisfying Assignments for
    SMT. In CAV, pages 394–409, 2012.
12. B. Dutertre and L. de Moura. A Fast Linear-Arithmetic Solver for DPLL(T). In CAV, volume
    4144 of LNCS, 2006.
13. N. Eén and N. Sörensson. An extensible SAT-solver. In Theory and Applications of Satisfi-
    ability Testing (SAT 2003), volume 2919 of LNCS, pages 502–518. Springer, 2004.
14. A. Griggio. A Practical Approach to Satisfiability Modulo Linear Integer Arithmetic. Jour-
    nal on Satisfiability, Boolean Modeling and Computation - JSAT, 8:1–27, 2012.
15. D. Larraz, A. Oliveras, E. Rodrı́guez-Carbonell, and A. Rubio. Minimal-Model-Guided
    Approaches to Solving Polynomial Constraints and Extensions. In SAT, 2014.
16. Y. Li, A. Albarghouthi, Z. Kincad, A. Gurfinkel, and M. Chechik. Symbolic Optimization
    with SMT Solvers. In POPL. ACM Press., 2014.
17. P. Manolios and V. Papavasileiou. Ilp modulo theories. In CAV, pages 662–677, 2013.
18. J. P. Marques-Silva, I. Lynce, and S. Malik. Conflict-Driven Clause Learning SAT Solvers,
    chapter 4, pages 131–153. In Biere et al. [4], February 2009.
19. R. Nieuwenhuis and A. Oliveras. On SAT Modulo Theories and Optimization Problems. In
    SAT, volume 4121 of LNCS. Springer, 2006.
20. R. Nieuwenhuis, A. Oliveras, and C. Tinelli. Solving SAT and SAT Modulo Theories: from
    an Abstract Davis-Putnam-Logemann-Loveland Procedure to DPLL(T). Journal of the ACM,
    53(6):937–977, November 2006.
21. R. Sebastiani. Lazy Satisfiability Modulo Theories. Journal on Satisfiability, Boolean Mod-
    eling and Computation, JSAT, 3(3-4):141–224, 2007.
22. R. Sebastiani and S. Tomasi. Optimization Modulo Theories with Linear Rational Costs.
    To appear on ACM Transactions on Computational Logics, TOCL. Available at http:
    //optimathsat.disi.unitn.it/pages/publications.html.
23. R. Sebastiani and S. Tomasi. Optimization in SMT with LA(Q) Cost Functions. In IJCAR,
    volume 7364 of LNAI, pages 484–498. Springer, July 2012.
24. R. Sebastiani and P. Trentin. Pushing the envelope of optimization modulo theories with
    linear-arithmetic cost functions. In Proc. TACAS, LNCS. Springer, 2015.




                                              18
