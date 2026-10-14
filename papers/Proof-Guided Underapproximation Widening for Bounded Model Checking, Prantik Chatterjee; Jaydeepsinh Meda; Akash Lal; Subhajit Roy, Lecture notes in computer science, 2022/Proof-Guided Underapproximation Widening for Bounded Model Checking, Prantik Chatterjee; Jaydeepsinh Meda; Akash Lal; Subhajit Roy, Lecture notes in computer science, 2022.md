         Proof-Guided Underapproximation
        Widening for Bounded Model Checking

           Prantik Chatterjee1(B) , Jaydeepsinh Meda2 , Akash Lal3 ,
                             and Subhajit Roy1
               1
                   Indian Institute of Technology Kanpur, Kanpur, India
                    prantik@cse.iitk.ac.in, subhajit@iitk.ac.in
                                2
                                  Oracle, Bengaluru, India
                         3
                           Microsoft Research, Bengaluru, India
                                  akashl@microsoft.com



       Abstract. Bounded Model Checking (BMC) is a popularly used strat-
       egy for program veriﬁcation and it has been explored extensively over
       the past decade. Despite such a long history, BMC still faces scalability
       challenges as programs continue to grow larger and more complex. One
       approach that has proven to be eﬀective in verifying large programs
       is called Counterexample Guided Abstraction Reﬁnement (CEGAR).
       In this work, we propose a complementary approach to CEGAR for
       bounded model checking of sequential programs: in contrast to CEGAR,
       our algorithm gradually widens underapproximations of a program,
       guided by the proofs of unsatisﬁability. We implemented our ideas in
       a tool called Legion. We compare the performance of Legion against
       that of Corral, a state-of-the-art veriﬁer from Microsoft, that utilizes
       the CEGAR strategy. We conduct our experiments on 727 Windows and
       Linux device driver benchmarks. We ﬁnd that Legion is able to solve
       12% more instances than Corral and that Legion exhibits a comple-
       mentary behavior to that of Corral. Motivated by this, we also build
       a portfolio veriﬁer, Legion+ , that attempts to draw the best of Legion
       and Corral. Our portfolio, Legion+ , solves 15% more benchmarks than
       Corral with similar computational resource constraints (i.e. each ver-
       iﬁer in the portfolio is run with a time budget that is half of the time
       budget of Corral). Moreover, it is found to be 2.9× faster than Corral
       on benchmarks that are solved by both Corral and Legion+ .


       Keywords: Veriﬁcation · Bounded model checking ·
       Underapproximation widening


1    Introduction
Bounded Model Checking (BMC) [11,20,26,33] is a popular option for program
veriﬁcation, primarily due to its ability of side-stepping the necessity of synthe-
sizing complex invariants. BMC harnesses the power of modern SMT solvers to
verify a bounded set of behaviors of a program. The user, if interested, may
c The Author(s) 2022
S. Shoham and Y. Vizel (Eds.): CAV 2022, LNCS 13371, pp. 304–324, 2022.
https://doi.org/10.1007/978-3-031-13185-1_15
    Proof-Guided Underapproximation Widening for Bounded Model Checking           305

re-attempt veriﬁcation with larger bounds once the program is proven correct
with small bounds.
    BMC operates by constructing a logical formula that symbolically captures
all states reachable by a program under a user-provided bound. A query, referred
to as the verification condition (VC), is constructed as a conjunction of the
program semantics and the negation of the property, which is also expressed as
a logical formula. If the veriﬁcation condition is satisﬁable, it implies that some
program execution violated the property of interest, thus the program is faulty.
If unsatisﬁable, the program satisﬁes the property, i.e. the program is safe under
the chosen bound.
    However, for large programs, BMC faces scalability challenges as the ver-
iﬁcation condition for the program tends to grow large, posing diﬃculties for
the SMT solver. Prior work has answered this challenge by using the popular
counterexample-guided abstraction refinement (CEGAR) strategy: start oﬀ with
the VC for an abstraction of the program, and incrementally reﬁne the abstrac-
tion until the program is decided as safe or faulty. The Stratified Inlining (SI) [26]
algorithm is an instance of this strategy. SI starts oﬀ with an abstraction of
only the entry procedure of the program, and then incrementally inlines callees,
guided by counterexamples. Not surprisingly, the dynamic inlining strategy of
SI has been found to be signiﬁcantly more scalable than algorithms that stat-
ically inline all procedures [25]. The SI algorithm is used in practice by the
Corral [24] veriﬁer that powers Microsoft’s Static Driver Veriﬁer (SDV) [4].
    In this work, we propose a new algorithm that uses proofs of unsatisﬁabil-
ity to widen underapproximate models of the program en route to veriﬁcation
of sequential programs. Our algorithm starts oﬀ by constructing a partial ver-
iﬁcation condition for only the program entry procedure and blocks all paths
that invoke calls to procedures that have not yet been inlined. This constructs
an underapproximation of the original program (because paths are blocked). A
satisﬁable result on an underapproximation will indicate the presence of a bug.
If the VC is unsatisﬁable, we examine its proof of unsatisfiability in order to
guide the inlining of called procedures. The program can be declared safe when
the proof of unsatisﬁability does not depend on any procedure call that has not
been inlined yet. We implemented our ideas in a tool called Legion.
    Further, we found that our underapproximation widening algorithm and the
abstraction reﬁnement strategy (used by Corral) demonstrate complementary
behaviors—many programs that Corral struggles on, yield to the underapprox-
imation based technique, and vice-versa. This observation motivated us to build
a portfolio veriﬁer, Legion+ , that runs both these techniques in parallel. We
found that the portfolio is more eﬀective than any of the tools alone (with simi-
lar computational resources, i.e. each veriﬁer in the portfolio is run with a time
budget that is half of the time budget of Corral). Both Legion and Legion+
are available open-source at the legion branch of the corral repository1 .
    Our experiments are conducted on 727 Windows and Linux device driver
benchmarks on which Corral struggles, i.e., Corral is unable to solve any of
1
    https://github.com/boogie-org/corral.git (branch: legion).
306    P. Chatterjee et al.

these benchmarks in less than 200 s. We ﬁnd that Legion is able to solve 12%
more instances than Corral with a time budget of 2 h per instance. Further,
the portfolio veriﬁer, Legion+ , given half the time budget of Corral, solves
15% more benchmarks than Corral, and it is found to be 2.9× faster than
Corral on benchmarks that are solved by both Corral and Legion+ .
   The primary contributions of this paper are as follows:

– We design a new algorithm, Underapproximation Widening guided Stratified
  Inlining, that uses proof-based artifacts to widen underapproximate models
  (in contrast to using counterexamples to reﬁne overapproximate models).
– We implemented our ideas in a tool called Legion for bounded program
  veriﬁcation.
– We also design a portfolio veriﬁer, Legion+ , that includes both overapprox-
  imation reﬁnement and underapproximation widening to verify a program in
  an attempt to reap the beneﬁts of both worlds.
– We evaluate both Legion and Legion+ on a set of 727 programs from Win-
  dows Device Drivers [31] from the SDV test-suite and Linux Device Drivers
  from SVCOMP [7] benchmarks.


2     Background

This section presents background material that we use in the rest of the paper.
    A logical formula consists of literals. A literal is either a variable or the
negation of a variable. A logical formula expressed in a Conjunctive Normal
Formal (CNF) is a conjunction of clauses where each clause is a disjunction
of literals. Given a logical formula, a satisfiability solver returns whether the
formula is satisfiable (SAT) or unsatisfiable (UNSAT). If a formula is SAT, the
solver provides a model in the form of a satisfying assignment of the variables. If
a formula is UNSAT, the solver returns an unsatisfiable core (unsat core), which
is a subset of clauses of the input formula whose conjunction is still UNSAT.


2.1   Language Model

We consider a programming language that represents a passified form of Boo-
gie programs [8]. A program consists of multiple procedures (Proc). We assume
an entry-point procedure called main where program execution starts. Each pro-
cedure can have any number of local variable declarations followed by a series
of basic blocks (BasicBlock ). We assume that local variables are initially uncon-
strained. A basic block is labeled by a unique identiﬁer and consists of mul-
tiple statements (Stmt) followed by a single control statement (ControlStmt).
A control statement is either a goto, which takes a sequence of basic block
labels and non-deterministically picks one to jump to, or a return that returns
control back to the caller. Returning from main terminates the program exe-
cution. A statement is either an assume command or a procedure call. The
statement (assume ϕ) allows a feasible execution only if ϕ is satisﬁable.
  Proof-Guided Underapproximation Widening for Bounded Model Checking         307




                           Fig. 1. A passiﬁed program


    We leave the set of variable types (Type) and expressions (Expr ) unspeciﬁed.
In practice, we can use any expression language that can be directly encoded
in SMT. Our implementation uses linear arithmetic, ﬁxed-size bit-vectors, unin-
terpreted functions, and extensional arrays. This combination is suﬃcient to
realistically translate C programs into our language representation [21,24].
    Note that the programs that we consider do not have global variables, return
parameters of procedures, or assignments. These restrictions are without loss of
generality [23]. Conversion of these additional feature into our language repre-
sentation is readily available in tools like Boogie. A passiﬁed program makes it
easy to describe the veriﬁcation-condition generation process.
    Given a program P, we consider the veriﬁcation question of whether there
exists a terminating execution of P. To be precise, we are interested in ﬁnding
out whether there is any execution of main that reaches its return statement.
If no such execution exists, then P is considered veriﬁed, or Safe. Otherwise,
we say that P is Unsafe and return the execution trace with concrete variable
values along the trace. Note that we consider a bounded version of the veriﬁcation
problem, i.e., we require that P does not contain any loops or recursive procedure
calls. All such loops and recursive calls must be unrolled to a pre-determined
308    P. Chatterjee et al.




                    Fig. 2. Call graph of the program in Fig. 1.




                              Fig. 3. Partial VC of main()


depth before proceeding with veriﬁcation, and thus, the veriﬁcation problem now
becomes decidable (if the expression language of the program is decidable) [23].


2.2   VC Generation for a Procedure

Consider a procedure baz that does not contain any procedure calls. This section
outlines one way of verifying baz, i.e., ﬁnding out if it has a terminating exe-
cution. We use a process called Veriﬁcation Condition (VC) generation on baz
to construct a logical formula Φ and feed it to an SMT solver. If Φ is UNSAT,
then the return statement in baz is unreachable and baz is Safe. Otherwise, we
extract the satisﬁable model from the SMT solver, construct the execution trace
and return Unsafe along with the trace. We now outline the VC-generation
process.
    Suppose that baz takes input arguments x. For each basic block j in baz,
we deﬁne a boolean variable blkj that is termed as the control-flow variable.
Let stj denote the conjunction of all assume statements in basic block j. Let
successor(j) denote the targets of the goto statement in j, i.e., all the successor
basic blocks in baz, to which control may jump non-deterministically from j.
Let ij be a unique integer constant representing basic block j. We also deﬁne an
uninterpreted function f low : Z → Z that records the non-deterministic choice
of the successor basic block of j. Given the above, we construct a logical formula
ψj for each basic block j as follows:
  Proof-Guided Underapproximation Widening for Bounded Model Checking          309


                                   
              blkj ⇒ (stj ∧                 (blks ∧ (is == f low(ij ))))
                              s∈successor(j)

If basic block j ends with a return statement instead of a goto, then ψj is:

                                      blkj ⇒ stj

   Assuming the ﬁrst basic block of baz, where procedure execution begin, is
labeled s, the VC of baz is constructed as follows:
                                        
                             blks ∧              ψl
                                       l∈basicblocks(p)

  In Fig. 3, we show the VC of main of the program in Fig. 1 as an example,
where we ignore the procedure calls in main (i.e., treat them as (assume true)).
We term such a VC (of a procedure where its calls are skipped) as the partial
VC (pVC) of the procedure.


2.3   Static Versus Dynamic Inlining
Given a program P with a starting procedure main, one simple way to verify P
would be to construct the VC of main by inlining all the procedure calls and
check the satisﬁability of VC(main) with an SMT solver. However, employing
such a static inlining strategy can cause an exponential blowup in the size of the
VC. Hence, we instead make use of dynamic inlining algorithm, called Stratiﬁed
Inlining (SI) [26], that employs a Counterexample Guided Abstraction Reﬁne-
ment (CEGAR) technique [14] to dynamically inline procedure VCs. It has been
shown that dynamic inlining scales better than static inlining [25]. Dynamic
inlining produces more compact VCs during abstraction reﬁnement which leads
to signiﬁcantly faster program veriﬁcation.


2.4   Verification with Stratified Inlining
The working of SI is shown in Algorithm 1. For the sake of simplicity, let us
assume that each basic block in P may contain only a single procedure call.
Every program point, from which a procedure is called, is termed as a callsite.
For example, main in Fig. 1, has two callsites; foo and bar which are called from
basic blocks L1, L2 and L3 respectively. A static instance of a callsite is denoted
with a pair (l, c) where l denotes the basic block identiﬁer from which a call
to the procedure c is made. A dynamic callsite is deﬁned as a stack of static
callsites which represents the runtime stack during a program’s execution with
main being present at the bottom of the stack. For example, the dynamic callsite
corresponding to the call foo from L1 in main is given by [main, (L1, foo)]. The
call graph of the program in Fig. 1 is shown in Fig. 2.
310    P. Chatterjee et al.


 Algorithm 1: Stratiﬁed Inlining (SI) algorithm.
   Input: program P with starting procedure main
   Input: An SMT solver S
   Output: Safe, or UnSafe(τ )
 1 C ← {[main, s] | s ∈ callsites(main)}
 2 S.Assert(pVC(main, [main]))
 3 while true do
 4    outcome ← OverRefStep(P, C, S)
 5    if outcome == Safe ∨ outcome == UnSafe(τ ) then
 6        return outcome
 7     else
 8         let NoDecision( , C  ) = outcome
 9         C ← C




    The SI algorithm takes as input a program P with a starting procedure main
and an SMT solver S. Initially, we add the dynamic callsites in main to a list C
(Line 1) and then inline main, i.e., assert the pVC of main (Line 2). The callsites
in C are termed as open callsites because they have not yet been inlined. The
above steps construct an abstraction of P. The SI algorithm then iteratively
calls the OverRefStep routine on this abstraction (Line 4) to perform gradual
reﬁnement until we can reach a decision about whether P is Safe or not. Each
invocation of OverRefStep can potentially inline more procedures by asserting
their partial VC to the solver S. Thus, the state of the solver, as well as the set
of open callsites C change across invocations of OverRefStep. We discuss the
Overapproximation Refinement Guided Stratified Inlining (OverRefSI ) strategy
used by the OverRefStep routine in Sect. 2.5.

2.5   Overapproximation Refinement Guided Stratified Inlining
The OverRefStep routine given in Algorithm 2 demonstrates the inner work-
ings of the OverRefSI strategy at each veriﬁcation step. The OverRefSI strat-
egy [26] for verifying a program works by iteratively ﬁring overapproximation
queries and gradually reﬁning the abstraction of P. If the query returns UNSAT,
then we can conclude that P is safe with respect to the given property. Other-
wise, we extract all the open callsites that appear on the counterexample trace
and reﬁne the abstraction of P by inlining these callsites. If the counterexample
trace contains no open callsites, then P is unsafe and we return the verdict
along with the counterexample trace.
    The OverRefStep routine takes as input a program P, a set of open call-
sites C and an SMT solver S. The OverRefStep routine is called iteratively
in order to verify the safety of P. We demonstrate the working of OverRefSI to
verify the pVC of main of Fig. 1 in Table 1. At the beginning, the SI algorithm
asserts the pVC of main to S and adds [main, (L1, foo)] and [main, (L2, bar)] to
the list of open callsites C in step 0.
  Proof-Guided Underapproximation Widening for Bounded Model Checking            311


 Algorithm 2: OverRefStep(P, C, S)
   Input: procedure P, set of callsites C, SMT solver S
   Output: Safe, UnSafe(trace), NoDecision(τ , C)
 1 // Overapproximate check
 2 if S.Check() == UNSAT then
 3     return Safe
 4   else
 5       τ ← opencallsites(S.Model())
 6   if τ == ∅ then
 7       return UnSafe(S.Model())
 8 else
 9     C ← ∅
10     forall c ∈ τ do
11        C  ← Inline(P, c)
12      C ← (C − τ ) ∪ C 
13      return NoDecision(τ , C)




    Next, the SI algorithm calls OverRefStep with P, C and S as arguments.
OverRefStep ﬁres an overapproximation query in Line 2. If the query is unsat-
isﬁable, we return the safe verdict. If the query is satisﬁable, we get the coun-
terexample trace and extract all the open callsites on the trace in τ (Line 5).
If τ is empty, i.e., the counterexample trace contains no open callsites, then
the trace is not spurious and we can return an unsafe verdict with the trace
(Line 7). Otherwise, we inline all the callsites in τ and add all the new callsites
that opened up due to the inlinings in C  (Line 11). Inlining a callsite c consists
of asserting the partial VC of the procedure that was invoked from c.
    Subsequently, the inlined callsites are removed from the list of open callsites C
and new callsites that opened up due to the inlinings are added to C (Line 12).
For example, in step 1 of Table 1, OverRefStep ﬁres an overapproximation
query that returns SAT with a counterexample trace that contains the callsite
of foo, i.e., [main, (L1,foo)]. This callsite is then inlined by asserting the pVC
of foo to the solver. This opens up the callsites of foo1 and foo2. Since we have
not been able to arrive at a decision regarding the safety of P at this step, a
verdict of NoDecision is returned along with the list of inlined callsites τ and
the new list of open callsites C (Line 13).
    Next, the SI algorithm calls OverRefStep again and in step 2, it ﬁres an
overapproximation query again, which returns SAT with the counterexample
trace containing the open callsite of foo1 that we inline by asserting the pVC
of foo1. The veriﬁcation process continues in this way by inlining the open
callsites on the counterexample trace in every step, which gradually reﬁnes the
pVC of main. Finally, in step 7, the overapproximation query returns UNSAT
from which we can conclude that main is safe.
312    P. Chatterjee et al.

            Table 1. Execution of OverRefSI on the program of Fig. 1

             Step             Action                        Open callsites
               0       Assert pVC(main)                    [main, (L1,foo)]
                                                           [main, (L2,bar)]
               1     Overapprox check: SAT
                        Assert pVC(foo)                    [main, (L2,bar)]
                                              [main, (L1, foo), (L6, foo1)]
                                               [main, (L1,foo), (L7, foo2)]
               2     Overapprox check: SAT
                       Assert pVC(foo1)                    [main, (L2,bar)]
                                               [main, (L1,foo), (L7, foo2)]
               3     Overapprox check: SAT
                       Assert pVC(foo2)                    [main, (L2,bar)]
               4     Overapprox check: SAT
                        Assert pVC(bar)       [main, (L2,bar), (L12, bar1)]
                                              [main, (L2,bar), (L13, bar2)]
               5     Overapprox check: SAT
                       Assert pVC(bar1)       [main, (L2,bar), (L13, bar2)]
               6     Overapprox check: SAT
                       Assert pVC(bar2)
               7    Overapprox check: UNSAT
                          Return Safe



3     Overview

3.1   Underapproximation Widening

We propose a novel algorithm, Underapproximation Widening Guided Stratified
Inlining (UnderWidenSI ), that uses proofs of unsatisﬁability to guide stratiﬁed
inlining. UnderWidenSI maintains an underapproximated model of the target
program and widens it until either the program is veriﬁed as safe or a bug is
found.
    We illustrate the UnderWidenSI strategy in Figs. 4a to 4d. Assume that we
are trying to verify whether some required property holds on a program. The
space contained by the yellow ovals show the reachable program states while the
red ovals depict error states on which the required property does not hold. The
objective of a veriﬁcation algorithm is to construct a model of the program that
is precise enough to show that the program can reach an error state or prove
that the error states are unreachable. Figures 4a to 4c show a safe program while
Fig. 4d depicts an unsafe program.
    Consider Fig. 4a: the UnderWidenSI algorithm starts oﬀ with the partial
veriﬁcation condition of the entry procedure and “blocks” executions though all
its open callsites.
    Proof-Guided Underapproximation Widening for Bounded Model Checking             313




                          Fig. 4. How UnderWidenSI works


Definition (Blocked callsites). We use the term, blocking a callsite C, to
imply that all paths that reach C are deemed infeasible. That is, blocking a
callsite has the eﬀect of replacing the callsite by (assume false).
    Essentially, blocking callsites creates underapproximations of the set of feasi-
ble program paths. Such underapproximated VCs can be constructed by assert-
ing additional blocking clauses corresponding to the control-ﬂow variables of the
open callsites. These blocks disallow reachability to certain program states. For
example, in Fig. 4a, we construct an underapproximated model of the program by
blocking the open callsites C1 and C2 . The inner green oval depicts the program
states that are reachable in the underapproximated model, whereas the outer
gray regions demonstrate the states that are unreachable due to the blocks on
C1 and C2 .
    If the veriﬁcation query on this model (conjunction of the underapproximated
model and the negation of the property) returns SAT, it implies that an error
state in indeed reachable. On the other hand, if the query returns UNSAT (as
shown in Fig. 4a), we need to widen the model to procure additional reachable
executions. We guide this widening operation by extracting the reason for this
unsatisﬁability from a minimal unsat core 2 of the query, that returns the set of
block clauses; the callsites corresponding to these blocking clauses constitutes
2
    Although there may exist multiple minimal unsat cores, we found via some prelimi-
    nary experiments that the choice of the unsat core does not have a signiﬁcant impact
    on the overall runtime of our algorithm (on an average).
314     P. Chatterjee et al.




                               Fig. 5. How OverRefSI works


a reason of why the current underapproximate model is not able to reach any
of the error states. Hence, we widen the model by unblocking exactly these
callsites leading to a wider model (see Fig. 4b). The widening by inlining C2
causes a stratiﬁed inlining step, and hence may open up new callsites, say C3
and C4 .
     We proceed in the same manner by blocking these open callsites and repeat
the query. Finally, (in Fig. 4c) we construct an underapproximated model that
still does not intersect with the error states. However, in this case, the unsat core
does not contain any blocked clause, as none of the currently blocked callsites
would have allowed widening in the direction of the error states.
     The unsat core provides a direction for widening towards the error states.
This also allows us to declare that the program is safe without requiring to
widen the model to encompass the set of all reachable program states—if the
veriﬁcation query is UNSAT and the unsat core does not contain any blocked
clause, then this forms a suﬃcient condition to declare the program safe.
     Figure 4d shows how our algorithm proceeds for a faulty program: it incre-
mentally widens the model in the direction of the error states till an error state
R is reached. At this point, the UnderWidenSI algorithm declares the program
as unsafe.
     Let us now contrast the UnderWidenSI strategy with the OverRefSI strategy,
popularly known as counterexample-guided abstraction refinement (CEGAR),
which currently drives the SI algorithm in Corral. OverRefSI starts oﬀ with
an overapproximated model of the program: the pVC of the entry procedure
with all callsites replaced by non-deterministic updates to its set of modi-
ﬁed variables. For example, in Fig. 5a, OverRefSI constructs an abstract pro-
gram/overapproximated model M1 of the program by overapproximating the
open callsites. If the resulting veriﬁcation condition is SAT, it examines the gen-
erated counterexample to check if it spurious. If the counterexample is found to
be a true bug, it declares the program unsafe. If the counterexample is spurious,
the model is reﬁned to eliminate this spurious counterexample. For example, in
Fig. 5a, we ﬁnd that there exists an error state/counterexample P within M1 ,
where the property can be violated. Hence, OverRefSI reﬁnes M1 in Fig. 5a by
    Proof-Guided Underapproximation Widening for Bounded Model Checking       315

inlining the overapproximated callsites through which P is reachable. The reﬁne-
ment is done to rule out P as a counterexample, i.e., P becomes unreachable
after reﬁnement. We observe in Fig. 5a, that after the ﬁrst round of reﬁnement,
P is no longer reachable in the overapproximated M2 , however, we can still ﬁnd
another counterexample Q. Hence, the abstraction M2 is reﬁned again. The pro-
gram is declared safe when the model cannot reach any error state. Note that
the algorithm can prove the safety of the program without requiring to precisely
capture the exact set of reachable program state.
    OverRefSI and UnderWidenSI are complementary: while OverRefSI main-
tains an overapproximated model and reﬁnes the model (shrinking the set of
reachable states), UnderWidenSI maintains an underapproximated model and
widens the model (expanding the set of reachable states) incrementally. In terms
of the algorithmic details, the OverRefSI algorithm in Corral uses the models
(the counterexamples) to drive reﬁnements, whereas our UnderWidenSI algo-
rithm uses the proof (the unsat core) to guide the widenings.


4     Algorithms
4.1    Underapproximation Widening Guided Stratified Inlining
       (UnderWidenSI )

The UnderWidenStep routine in Algorithm 3 demonstrates how the Under-
WidenSI strategy works in each veriﬁcation step. It takes as input a procedure P,
a set of open callsites C and an SMT solver S. The UnderWidenStep routine
is called by the SI algorithm (instead of OverRefStep in Line 4) iteratively in
order to verify the safety of P.
     In the beginning, we construct an underapproximated pVC of the input pro-
cedure P by blocking all calls through the open callsites in C (Line 4). Next, we
ﬁre an underapproximation query (Line 5). If the query returns SAT, then we
return the verdict unsafe with the counterexample trace (Line 6). Otherwise,
we get the minimal unsatisﬁable core uc and extract all the blocked callsites
which appear on uc in μ (Line 8).
     If μ does not contain any blocked callsites, we deduce that P is safe. The
proof of the safety of P is captured by uc. Hence, we return the verdict that P
is safe. Otherwise, each of the callsites in μ are then inlined (Line 15) which
constructs a reﬁnement of P. The inlined callsites are then removed from the
list of open callsites C and new callsites that opened up due to the inlinings are
added to C (Line 16).
     When the algorithm is unable to arrive at a decision regarding the safety
of P, it returns a verdict of NoDecision along with the list of inlined callsites
μ and the new list of open callsites C (Line 13).


Example. We demonstrate the working of UnderWidenSI to verify the pVC
of main of Fig. 1 in Table 2. Initially, we assert the pVC of main and add
[main, (L1, foo)] and [main, (L2, bar)] to the list of open callsites in step 0.
316    P. Chatterjee et al.


 Algorithm 3: UnderWidenStep(P, C, S)
   Input: procedure P, set of callsites C, SMT solver S
   Output: Safe, UnSafe(trace), NoDecision(μ, C)
 1 // Underapproximate check
 2 S.Push()
 3 forall c ∈ C do
 4    S.Assert(¬ControlVariable(c))
 5 if S.Check() == SAT then
 6     return UnSafe(S.Model())
 7 else
 8     μ ← BlockedCallsites(S.UnsatCore())
 9 S.Pop()
10 if μ == ∅ then
11     return Safe
12 else
13     C ← ∅
14     forall c ∈ μ do
15        C  ← Inline(P, c)
16     C ← (C − μ) ∪ C 
17     return NoDecision(μ, C)




Replacing each of the open callsites with (assume false) statement, i.e., blocking
them, constructs an underapproximation of the program. If an SMT solver query
on this underapproximation returns SAT, then the program is surely unsafe as
the satisﬁable model can only represent an execution trace that goes through
inlined callsites. In that case, we can return the verdict unsafe along with an
error trace constructed from the model. On the other hand, if the underapprox-
imation check returns UNSAT, then we cannot return a verdict on the safety of
the program immediately.
    Following this, in step 1 (see Table 2), we push a new frame on the solver
and assert (¬blkL1 ∧ ¬blkL2 ) to block executions through the callsites of foo and
bar respectively to construct the underapproximated pVC of main. We query
the solver with these constraints. Figure 1 shows that if we block executions
through basic blocks L1 and L2, the program cannot terminate, i.e., the return
statement in L3 is not reachable. Hence, the solver returns UNSAT. The reason
for the unsatisﬁability is blocking executions through both L1 and L2.
    To widen the underapproximated model of the program so that we may
reach L3, we need to remove the block on at least one of them and inline the
respective callsite. The unsat core, in this case, contains the callsite of varbar
in basic block L2. Therefore, we pop the earlier solver frame containing blocked
clauses and assert (blkL2 =⇒ pVC(bar)) in the solver. Inlining bar, opens up
the callsites [main, (L2, bar), (L12, bar1)] and [main, (L2, bar), (L13, bar2)].
    Next, in step 2, we again construct the underapproximated pVC of main
by blocking executions through the callsites of foo, bar1 and bar2. The solver
  Proof-Guided Underapproximation Widening for Bounded Model Checking            317

          Table 2. Execution of UnderWidenSI on the program of Fig. 1

             Step            Action                          Open callsites
             0         Assert pVC(main)                     [main, (L1,foo)]
                                                            [main, (L2,bar)]
             1      Underapprox check: UNSAT
                        Assert pVC(bar)                    [main, (L1,foo)],
                                               [main, (L2,bar), (L12, bar1)]
                                               [main, (L2,bar), (L13, bar2)]
             2      Underapprox check: UNSAT
                        Assert pVC(foo)         [main, (L1,foo), (L6, foo1)]
                       Assert pVC(bar1)         [main, (L1,foo), (L7, foo2)]
                       Assert pVC(bar2)
             3      Underapprox check: UNSAT
                       Assert pVC(foo1)
                       Assert pVC(foo2)
             4      Underapprox check: UNSAT
                          Return Safe



query returns UNSAT with uc containing the callsites of foo, bar1 and bar2
which are inlined.
    In step 3, the callsites of foo1 and foo2 are now open. Blocking both of
these callsites and making an underapproximation check returns UNSAT with
uc containing the callsites of foo1 and foo2. These callsites are now inlined.
    In step 4, the underapproximation query returns UNSAT and uc contains
no blocked callsites. This points to the fact that uc contains only inlined call-
sites, i.e., starting from step 0 if we only inline the callsites in uc and leave the
remaining callsites overapproximated, we will still get an UNSAT. Therefore, uc
is the proof of the safety of the program and we return the verdict that the pVC
of main is safe.
    Note that when the underapproximation query returns SAT, then the coun-
terexample trace is constructed on the underapproximated program, i.e., the
trace may contain only blocked and inlined callsites. The underapproximated
program represents a subset of the paths in the original program, therefore, any
counterexample trace present in the underapproximated program is sure to be
present in the original program as well. Therefore, if the underapproximated
program is unsafe, the original program is unsafe as well.
    We have implemented the UnderWidenSI algorithm in Legion. We compare
the performance of the UnderWidenSI algorithm in Legion against that of
Corral which uses OverRefSI .

4.2   Portfolio Technique
The complementary behavior of the OverRefSI and the UnderWidenSI algo-
rithms motivate us to design a portfolio approach for verifying a program. The
318     P. Chatterjee et al.

portfolio strategy incorporates both the OverRefSI algorithm used by Corral
and the UnderWidenSI algorithm implemented in Legion. We refer to the port-
folio veriﬁer as Legion+ . For each program, Legion+ runs both Corral and
Legion in parallel. Legion+ terminates veriﬁcation as soon as one of the algo-
rithms ﬁnishes veriﬁcation and reports the outcome. We discuss the performance
of Legion+ against that of Corral and Legion in Sect. 5.


5     Experimental Results
We have built a tool, Legion, that implements our UnderWidenSI algorithm.
To compare against OverRefSI , we use Corral [26], a state-of-the-art veriﬁer
used at Microsoft [24]. We also build a portfolio solver, Legion+ , that runs both
Corral and Legion in parallel. Whenever one of the tools ﬁnish veriﬁcation,
Legion+ terminates the algorithms and reports the outcome.
    We compare the performance of Corral against Legion and Legion+ on
a suite of Windows and Linux device driver benchmarks. The Windows device
driver benchmarks are obtained by running Static Driver Veriﬁer (SDV) [4] on
real windows device drivers that exercise all features of the C language such as
arrays, heaps, pointers, loops, recursion etc. SDV compiles these drivers into a
suite of BOOGIE [8] programs, each of which is a device driver paired with prop-
erty (compilation is detailed in [24]). Note that, although the suite of Windows
device drivers compiled into BOOGIE programs are available as SDV bench-
marks [31], the actual C programs are internal to Microsoft.
    Along with this, we also use a set of Linux device drivers that are available as
C programs as part of the SVCOMP benchmarks suite [7]. We used SMACK [36]
to compile the Linux device drivers into BOOGIE programs. Overall, we elect
to use a total of 727 hard programs, on which Corral took more than 200 s to
verify or times out, from the SDV and SVCOMP benchmarks to run our experi-
ments. We set the timeout for each veriﬁcation task to 2 h for both Corral and
Legion. For all veriﬁcation tasks, We use an unrolling length of 3 as advised in
the benchmarks [31] and used in other works [11].
    As Legion+ uses twice the computational resources compared to Corral
and Legion, we halve its time budget to 1 h to make a fair comparison. We also
report the performance of Legion+ with a 2 h time budget (it can be seen as
the virtual best of Corral and Legion).
    The experiments were performed on a machine with AMD EPYC 7452 pro-
cessor (48 cores) and 384 GB of RAM. Both Corral and Legion uses Z3 [15]
as the underlying SMT solver. We have used the default setting of a ﬁxed ran-
dom seed for Z3 for all our experiments after verifying the fact that the choice
of random seed does not have any signiﬁcant impact on our results.


5.1   Corral Versus Legion

Figure 6 depicts the number of solved instances within the time budget by Cor-
ral and Legion. In Fig. 6, a point (x, y) denotes the number of instances x,
  Proof-Guided Underapproximation Widening for Bounded Model Checking                                    319


                                                                          262           351       397
                                   2
                                              LEGION
                                              CORRAL

          Time taken (in hours)
                                              LEGION+
                                  1.5


                                                                                            369
                                   1



                                  0.5



                                   0
                                        0    50       100    150    200   250     300    350       400
                                                        Number of solved instances

Fig. 6. Number of instances solved within time (in hours) for Corral vs Legion vs
Legion+ .
                   Table 3. Total time taken by each veriﬁer to solve instances

                                            Veriﬁer     Solved instances Total time taken
                                            Corral            262               109 h
                                            Legion            351               112 h
                                            Legion+           369                71 h



each of which was solved within time y. As we can observe, Corral is able to
solve 262 out of 727 instances (36%) with a time budget of 2 h per instance,
whereas Legion solves 351 instances (48%) with the same time budget. Both of
them fail to solve 330 instances (45%). Out of the 397 instances (55%) that are
solved by either Corral or Legion, 46 instances (12%) are solved exclusively
by Corral, whereas 135 instances (34%) are solved exclusively by Legion.
    The scatter plot of veriﬁcation times across Legion and Corral is shown
in Fig. 7. The spread in the scatter plots demonstrate that these two tools com-
plement each other—the benchmarks on which Corral struggles are sometimes
handled well by Legion, and vice-versa. Picking the best of two veriﬁers solves a
total of 397 out of 727 instances (55%). This motivated the design of Legion+ .

5.2   Performance of Legion+
As Legion+ utilizes parallelism, in order to make a fair comparison we halve
the time budget for Legion+ on each veriﬁcation instance to 1 h. This means
that Legion+ runs both the tools Corral and Legion in parallel but with a
time budget of 1 h each.
    Figure 6 shows that the portfolio veriﬁer Legion+ solves 369 out of 727
instances (51%) with a 1 h time budget, whereas Corral solves only 262
320    P. Chatterjee et al.

                                              7000



          Time Taken By LEGION (in seconds)
                                              6000


                                              5000


                                              4000


                                              3000


                                              2000


                                              1000


                                                0
                                                     0   1000   2000     3000     4000    5000      6000   7000
                                                                Time Taken By CORRAL (in seconds)


          Fig. 7. Scatter plot of veriﬁcation time of Corral vs Legion.


instances (36%) with a total time budget of 2 h. There are only 14 instances
that Corral solves but Legion+ is unable to solve. Similarly, there are only
17 instances that Legion solves but Legion+ is unable to solve.
    With a 2 h timeout, Legion+ solves 397 instances in total (55%). This is
essentially the virtual best of Corral and Legion with a 2 h timeout.
    Figure 8 shows the total time taken (in hours) by Corral, Legion and
Legion+ to verify the instances that were solved by all three of them (total 213
instances). Legion+ is 1.9× faster than Legion and 2.9× faster than Corral.
    Across the benchmarks that each of the tools solve individually, Corral
takes 109 h to solve 262 benchmarks, Legion takes 112 h to solve 351 bench-
marks, whereas Legion+ solves 369 benchmarks within only 71 h (see Table 3).
    Note that the benchmarks used in our study are those on which Corral
took greater than 200 s. On the rest of the benchmarks, clearly Legion+ will
perform at least as well as Corral. We chose to leave them out to ensure that
the experiments run in a reasonable time: there were roughly 14000 of these easy
cases. It allowed us to focus on benchmarks where speedup was important.


6     Related Work
The high-level idea of using proof-guided abstractions has been long known [3,
30]. Proofs of unsatisﬁability have been used to derive abstractions for
unbounded model checking in the context of microprocessor veriﬁcation [30].
Amla et al. have also demonstrated that counterexample based abstraction is
complementary to proof based abstraction and they can be combined in a judi-
cious manner to reap the beneﬁts of both the techniques for hardware veriﬁ-
cation tasks [3]. However, program veriﬁcation has mostly been dominated by
counterexample-guided abstraction reﬁnement (CEGAR) based strategies. Of
  Proof-Guided Underapproximation Widening for Bounded Model Checking               321

                                             100




           Cumulative time taken to verify
                                                   81 hours
                                              80



                                              60
                                                              52 hours


                                              40
                                                                         28 hours

                                              20



                                               0
                                                   CORRAL     LEGION     LEGION+


Fig. 8. Cumulative time taken (in hours) to verify 213 instances that were solved by
all three veriﬁers.


the few proposals that use proof-guided underapproximation widening strategies,
most of them focus on veriﬁcation of multi-threaded programs [18,35]. These
techniques perform underapproximation on the number of thread interleavings
allowed, while eagerly inlining all procedures. One technique [18] constrains the
number of interleavings to certain bounds, while the other [35] uses dynam-
ically inferred invariants for constructing (potential) underapproximations on
interleavings. Note that, these techniques are orthogonal to our approach. Eager
inlining is not feasible for our benchmarks, which is precisely the problem that we
address. Our proposal shows that proof-guided widening strategies can be eﬀec-
tively employed for verifying large sequential programs. Proof of unsatisﬁability
from underapproximated models have also been utilized to narrow down the
search space for overapproximation reﬁnement in order to decide ﬁnite precision
bit vector arithmetic with arbitrary bit vector operations [9]. The underapproxi-
mation is done on the bit vector variables of a propositional logic formula where
some of the bit vector variables are encoded with fewer boolean variables than
their width.
    Other than using proofs to guide widening heuristics, proof artifacts, like
interpolants, have been used to construct annotations [1,2,27–29] that can be
useful in constraining future search. Such techniques are orthogonal to underap-
proximation widening based techniques. However, they can be useful for Legion
and we plan to investigate them in the future.
    Underapproximation widening has also been used in program synthe-
sis [37,39,40]. Instead of unleashing the search for the program on the whole
search space, such techniques search for the desired program in an underap-
proximated search space. While prior approaches [37] used a pre-deﬁned widen-
ing sequence, later approaches [39,40] use proofs of unsatisﬁability to guide
the widening sequence. Similar techniques have also been used in the synthe-
322     P. Chatterjee et al.

sis of boolean functions [16,17]. Manthan [16,17] constructs an initial guess of
the boolean function by sampling the speciﬁcation and constructing a decision-
tree classiﬁer from the resulting data. It, then, uses a proof-guided technique to
“repair” the learnt model into a desired function.
    There have also been applications of the maximal satisﬁable set (MAXSAT)
on an unsatisﬁable formula for program debugging. BugAssist [19] attempts to
infer the set of suspicious locations using a MAXSAT formulation over an failing
program trace and the speciﬁcations. Bavishi et al. [6] extend the formulation
to provide a ranking over the suspicious locations such that the locations higher
up in the rankings are less likely to cause regressions.
    Another line of work is to use fuzzers to sample concrete instances and grad-
ually build approximations of program behavior for the purpose of deductive
veriﬁcation [22] and symbolic execution [34]. However, such approaches use test
instances and do not apply a proof-guided strategy.
    Legion is inspired by many of the above algorithms and, there is potential
of incorporating more of these ideas in Legion in the future.


7     Conclusion

Bounded model checking approaches for program veriﬁcation predominantly
focuses on CEGAR based strategies. In this work, we propose a proof-guided
underapproximation widening strategy which behaves in a complementary man-
ner to the CEGAR technique. The complementary nature allows us to build a
portfolio strategy that takes advantage of both proof-guided underapproxima-
tion widening and CEGAR to deliver a signiﬁcant speed up in veriﬁcation time
over both.
    Our current approach only looks at the predicates corresponding to the call-
sites to ﬁgure out which are most relevant to the proof of unsatisﬁability of the
underapproximated model. In the future, we aim to extract additional informa-
tion from the unsat core which would allow us to explore more involved widen-
ing strategies. Furthermore, combining the underapproximation techniques that
work on the domain of thread interleavings to deal with a large space of sequen-
tial behaviors (via lots of procedures) and concurrent behaviors (via lots of inter-
leavings) would be another interesting direction to explore. We also believe that
underapproximation widening may yield improvement performance on our dis-
tributed bounded model checker, Hydra [11,12]. Another interesting direction
that we want to pursue is on combining bounded model checking algorithms
(both overapproximation reﬁnement and underapproximation widening) with
dynamic analysis [5,13,38] and statistical testing [10,32] based approaches.

Acknowledgements. We wish to express our gratitude towards Microsoft Azure and
Google Cloud Platform for providing us with computational resources for the experi-
ments. We are also indebted to the PRAISE group of CSE department, IIT Kanpur
and the anonymous reviewers for their helpful suggestions.
  Proof-Guided Underapproximation Widening for Bounded Model Checking               323

References
 1. Albarghouthi, A., Li, Y., Gurﬁnkel, A., Chechik, M.: Ufo: a framework for
    abstraction-and interpolation-based software veriﬁcation. In: CAV (2012)
 2. Alt, L., et al.: Hifrog: Smt-based function summarization for software veriﬁcation.
    In: TACAS (2017)
 3. Amla, N., McMillan, K.L.: A hybrid of counterexample-based and proof-based
    abstraction. In: FMCAD (2004)
 4. Ball, T., Cook, B., Levin, V., Rajamani, S.K.: Slam and static driver veriﬁer: Tech-
    nology transfer of formal methods inside microsoft. In: International Conference
    on Integrated Formal Methods (2004)
 5. Ball, T., Larus, J.R.: Eﬃcient path proﬁling. In: Proceedings of the 29th Annual
    ACM/IEEE International Symposium on Microarchitecture (1996)
 6. Bavishi, R., Pandey, A., Roy, S.: To be precise: regression aware debugging. ACM
    SIGPLAN Notices (2016)
 7. Beyer, D.: Automatic veriﬁcation of C and Java programs: SV-COMP 2019. In:
    Tools and Algorithms for the Construction and Analysis of Systems - 25 Years
    of TACAS: TOOLympics, Held as Part of ETAPS 2019, Prague, Czech Republic,
    6–11 April, 2019, Proceedings, Part III (2019)
 8. Boogie: An intermediate veriﬁcation language. https://boogie-docs.readthedocs.
    io/en/latest/. Accessed June 2022
 9. Bryant, R.E., Kroening, D., Ouaknine, J., Seshia, S.A., Strichman, O., Brady, B.:
    Deciding bit-vector arithmetic with abstraction. In: TACAS (2007)
10. Chatterjee, P., Chatterjee, A., Campos, J., Abreu, R., Roy, S.: Diagnosing software
    faults using multiverse analysis. In: IJCAI (2020). https://doi.org/10.24963/ijcai.
    2020/226
11. Chatterjee, P., Roy, S., Diep, B.P., Lal, A.: Distributed bounded model checking.
    In: FMCAD (2020)
12. Chatterjee, P., Roy, S., Diep, B.P., Lal, A.: Distributed bounded model checking.
    Formal Methods in System Design (2022). https://doi.org/10.1007/s10703-021-
    00385-1
13. Chouhan, R., Roy, S., Baswana, S.: Pertinent path proﬁling: tracking interactions
    among relevant statements. In: CGO (2013). https://doi.org/10.1109/CGO.2013.
    6494983
14. Clarke, E., Grumberg, O., Jha, S., Lu, Y., Veith, H.: Counterexample-guided
    abstraction reﬁnement. In: CAV (2000)
15. De Moura, L., Bjørner, N.: Z3: An eﬃcient smt solver. In: TACAS (2008)
16. Golia, P., Roy, S., Meel, K.S.: Manthan: a data-driven approach for boolean func-
    tion synthesis. In: CAV (2020)
17. Golia, P., Roy, S., Slivovsky, F., Meel, K.S.: Engineering an eﬃcient boolean func-
    tional synthesis engine. In: ICCAD (2021)
18. Grumberg, O., Lerda, F., Strichman, O., Theobald, M.: Proof-guided under-
    approximation-widening for multi-process systems. In: POPL (2005)
19. Jose, M., Majumdar, R.: Cause clue clauses: error localization using maximum
    satisﬁability. ACM SIGPLAN Notices (2011)
20. Kroening, D., Tautschnig, M.: Cbmc-c bounded model checker. In: TACAS (2014)
21. Lahiri, S.K., Qadeer, S.: Back to the future: revisiting precise program veriﬁcation
    using smt solvers. In: POPL (2008)
22. Lahiri, S., Roy, S.: Almost correct invariants: synthesizing inductive invariants by
    fuzzing proofs. In: ISSTA (2022)
324     P. Chatterjee et al.

23. Lal, A., Qadeer, S.: Reachability modulo theories. In: Reachability Problems - 7th
    International Workshop, RP (2013)
24. Lal, A., Qadeer, S.: Powering the static driver veriﬁer using Corral. In: FSE (2014)
25. Lal, A., Qadeer, S.: DAG inlining: a decision procedure for reachability-modulo-
    theories in hierarchical programs. ACM SIGPLAN Notices (2015)
26. Lal, A., Qadeer, S., Lahiri, S.K.: A solver for reachability modulo theories. In: CAV
    (2012)
27. McMillan, K.L.: Interpolation and SAT-based model checking. In: CAV (2003)
28. McMillan, K.L.: Lazy abstraction with interpolants. In: CAV (2006)
29. McMillan, K.L.: Lazy annotation revisited. In: CAV (2014)
30. McMillan, K.L., Amla, N.: Automatic abstraction without counterexamples. In:
    TACAS (2003)
31. Microsoft: Static Driver Veriﬁer Benchmarks. https://github.com/boogie-org/
    sdvbench
32. Modi, V., Roy, S., Aggarwal, S.K.: Exploring program phases for statistical bug
    localization. In: PASTE (2013). https://doi.org/10.1145/2462029.2462034
33. Morse, J., Ramalho, M., Cordeiro, L., Nicole, D., Fischer, B.: Esbmc 1.22. In:
    TACAS (2014)
34. Pandey, A., Kotcharlakota, P.R.G., Roy, S.: Deferred concretization in symbolic
    execution via fuzzing. In: ISSTA (2019). https://doi.org/10.1145/3293882.3330554
35. Prabhu, S., Schrammel, P., Srivas, M., Tautschnig, M., Yeolekar, A.: Concurrent
    program veriﬁcation with invariant-guided underapproximation. In: ATVA (2017)
36. Rakamarić, Z., Emmi, M.: SMACK: decoupling source language details from veri-
    ﬁer implementations. In: CAV (2014)
37. Roy, S.: From concrete examples to heap manipulating programs. In: SAS (2013).
    https://doi.org/10.1007/978-3-642-38856-9 9
38. Roy, S., Srikant, Y.N.: Proﬁling k-iteration paths: A generalization of the ball-larus
    proﬁling algorithm. In: CGO (2009). https://doi.org/10.1109/CGO.2009.11
39. Verma, A., Kalita, P.K., Pandey, A., Roy, S.: Interactive debugging of concurrent
    programs under relaxed memory models. In: CGO (2020)
40. Verma, S., Roy, S.: Synergistic debug-repair of heap manipulations. In: ESEC/FSE
    (2017)




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
     The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
