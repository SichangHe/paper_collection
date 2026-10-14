          A More Pragmatic CDCL for IsaSAT
          and Targetting LLVM (Short Paper)

                 Mathias Fleury1,2,3(B)        and Peter Lammich4,5
                        1
                       University Freiburg, Freiburg, Germany
                           fleury@cs.uni-freiburg.de
             2
               Max-Planck-Institut für Informatik, Saarbrücken, Germany
                  3
                    Johannes Kepler University Linz, Linz, Austria
                    4
                      University of Manchester, Manchester, UK
                    5
                      University of Twente, Twente, Netherlands
                               p.lammich@utwente.nl

       Abstract. IsaSAT is the most advanced veriﬁed SAT solver, but it did
       not yet feature inprocessing (to simplify and strengthen clauses). In order
       to improve performance, we enriched the base calculus to not only do
       CDCL but also inprocess clauses. We also replaced the target of our code
       synthesis by Isabelle/LLVM. With these improvements, we can solve 4
       times more SAT Competition 2022 problems than the original IsaSAT
       version, and 4.5 times more problems than any other veriﬁed SAT solver
       we are aware of. Additionally, our changes signiﬁcantly reduce the trusted
       code base of our veriﬁcation.


1    Introduction
SAT solving is a very important tool that has been extensively used in various
applications like mathematics or cryptography. To ensure the correctness of the
answer provided by a SAT solver, there are two approaches: either producing a
certiﬁcate that can be checked independently or verifying a SAT solver. The ﬁrst
approach has been extensively studied and works very well in practice [19,26,28]
– only checked proofs are counted in the SAT Competition [2].
    The second approach, i.e., verifying a whole SAT solver is orders of mag-
nitudes more complex than checking a certiﬁcate. To this end, the goal of the
IsaFoL (Isabelle Formalization of Logic) [3] eﬀort is to develop methodology and
libraries for formalizing modern research in automated reasoning. In this con-
text, we have veriﬁed a CDCL calculus (conﬂict-driven clause learning) and a
two-watched literals data structure (Sect. 2). To show that they are useful, we
have developed the veriﬁed SAT solver IsaSAT [8], which we later optimized [12].
To our surprise, it won the EDA Challenge 2021 defeating all the non-veriﬁed
solvers, but, as expected, it ﬁnished last at the SAT Competition 2022 [2]. How-
ever, the former used a much shorter timeout (200 s, not announced before the
competition) whereas the latter uses 5000 s.
    In this paper, we present our new developments in IsaSAT, which make
our solver arguably the most advanced formally veriﬁed SAT solver to date:
inprocessing and verifying fast LLVM code [20] rather than slow functional code.
c The Author(s) 2023
B. Pientka and C. Tinelli (Eds.): CADE 2023, LNAI 14132, pp. 207–219, 2023.
https://doi.org/10.1007/978-3-031-38499-8_12
208     M. Fleury and P. Lammich

    Inprocessing is a critical feature of modern SAT solvers (e.g., every winner of
the SAT Competition since 2013 includes it). In order to use it in our formally
veriﬁed solver, we had to extend our veriﬁed CDCL calculus: Our new PCDCL
calculus includes features to encompass various inprocessing techniques, even if
we have not yet implemented every possible technique (Sect. 3).
    We generate IsaSAT by exporting a model in the interactive theorem prover
Isabelle [22] to executable code. Earlier we used Isabelle’s default code gen-
erator to export to Standard ML (SML). However, the performance was not
suﬃcient – especially memory consumption was very high. Thus, we switched to
Isabelle/LLVM [18], which generates LLVM intermediate representation (LLVM
IR). Apart from allowing faster imperative code, it also reduced the trusted
code base (Sect. 4), replacing the rather niche MLton [27] compiler by only the
backend of the widely used LLVM.
    Porting our entire development to Isabelle/LLVM required some changes
and some cleanup. Moreover, when we implemented and veriﬁed inprocessing,
we realized that some design decisions need to be improved. In Sect. 5, we report
on our experiences and lessons learned while porting and extending IsaSAT.
    Finally, we have benchmarked IsaSAT on the problems from the SAT Compe-
tition 2022. We show that just porting IsaSAT from SML to Isabelle/LLVM sig-
niﬁcantly improved the performance, and the new inprocessing techniques com-
bined with heuristic improvements give us another signiﬁcant increase, demon-
strating the usefulness of our PCDCL calculus (Sect. 6).
    This presentation is an extended version of our (non-peer-reviewed) system
description from the EDA Challenge 2021 [13] and the SAT Competition 2022 [6].
Compared to that version, we have provided much more details on PCDCL, our
experience porting the development to LLVM, and performance tests.


2     Preliminaries
CDCL. CDCL is a procedure that builds a partial assignment called a trail
either by guessing (called deciding) or propagating information. If the partial
assignment is a model, the algorithm stops. If there is a conﬂict between the
partial assignment and a clause, the partial assignment is repaired and a new
clause is learned. For more details (beyond the scope of this paper), we refer the
reader to the Handbook of Satisfiability [7].
    We use a transition system for our formalization of CDCL [8]. Its state con-
sists of the trail M , the (multi)sets of initial and learned clauses (N and U ),
and the conﬂict clause to analyze (or None if there is none). We show one rule,
decide, that adds L to the current assignment M :
    inductive decide :: st ⇒ st ⇒ bool where
      undefined lit M L =
                         ⇒ |L| ∈ |N | =
                                       ⇒
      decide (M, N, U, None) (L · M, N, U, None)
If no conﬂict has been found so far (None), we add the new literal L at the begin-
ning of the trail M . We prove that our set of rules is terminating and correct [8].
  A More Pragmatic CDCL for IsaSAT and Targetting LLVM (Short Paper)            209

Code Synthesis. To generate the IsaSAT code, we start from the abstract rules
like decide and gradually reﬁne it to some deterministic functions using the
Reﬁnement Framework [16]. Then, we rely on Sepref [17] to synthesize code: It
takes an (Isabelle) function and synthesizes a new version, replacing functional
data structures (like lists) by imperative data structures (like arrays). There
are two versions of the tool. The older version, which we used before [8,12],
uses Imperative HOL [9] and Isabelle’s standard (trusted) code generator [14]
to export code into various functional languages. We used Standard ML (SML)
with the compiler MLton [27], because it oﬀers (by far) the best performance
for our use case. The new Sepref is part of the Isabelle/LLVM library (devel-
oped by the second author) and generates LLVM IR from a model of LLVM IR
inside the theorem prover. The code generator interprets a shallow embedding
of Isabelle/LLVM as equivalent to similar looking LLVM code. This reduces the
trusted code base in two ways: ﬁrst, the trusted pretty printer is simpler, and,
second, instead of the rather niche full compiler MLton, we use only the backend
of the widely used LLVM [20].
    The biggest diﬀerence is that Imperative HOL allows arbitrary large arrays
and integers, whereas Isabelle/LLVM is more realistic, requiring integers (in
particular array oﬀsets, see Sect. 5.1) to have a ﬁxed bit-width.
Related Work. Our goal is to produce a fully veriﬁed SAT solver, without any
runtime checks, that both terminates and returns a correct model while using
eﬃcient data structures. No other solver achieves all three goals. The SAT solver
TrueSAT from Andrici and Ciobaca [1] relies on the original DPLL and uses
less eﬃcient data structures (including counters instead of watch lists), but it
terminates. Historically, this would roughly correspond to SAT solver from the
early 90s. However, it only uses stateless heuristics, and it is not clear if the
approach can be extended to CDCL (where the solver learns and keeps new
clauses) or to stateful heuristics (like VSIDS [21]). The solvers versat [23] and
Creusat [25] go into a similar direction with CDCL instead of DPLL, but prove
a weaker correctness property: they only show that an UNSAT result is correct,
while a SAT result requires an additional check. Also, termination is not proved.
Only proving this partial property makes many proofs considerably easier, in
particular adding restarts. Oe et al’s solver versat [23] was the ﬁrst partially
veriﬁed solver that could run benchmarks from the SAT Competition. More
recently, Skotåm [25] has veriﬁed in his Master’s thesis the SAT solver CreuSAT
using the Creusot framework (relying on Why3 internally). While CreuSAT is
much faster than versat in our tests, its correctness relies on (trusted) SMT
solvers, and the proofs are not checked by a small kernel like our Isabelle code.
However, the veriﬁcation also takes much less time (a few minutes compared to
several hours).
    Modern SAT solvers use inprocessing to make the subsequent CDCL run
heuristically faster [15]. In particular, clauses are strengthened and global trans-
formation (e.g., to remove variables) are applied. Two techniques (that we do
not support), variable elimination and addition, slowly change the models of the
formula by changing the set of variable. The SAT solver then reconstructs a
210     M. Fleury and P. Lammich

model of the original formula at the end. Fazekas et al. [11] made it compati-
ble with incremental SAT solving. All others inprocessing technique ﬁt into our
extended CDCL described in the next section.


3     Pragmatic CDCL for Inprocessing
SAT solvers nowadays apply a combination of CDCL (most of the time) and
inprocessing (sometimes). Therefore, we extended our calculus similarly. At the
core, we have our terminating CDCL. We also allow for formula transformation
and restarts. We call the combination pragmatic CDCL or PCDCL.
Splitting the Clause Set. Inprocessing makes it possible to strengthen and
simplify clauses. However, we want models from the ﬁnal set of clauses to remain
models from the initial set of clauses. Deleting clauses is not possible: if we start
with the clauses A∨C and B ∨¬B, removing the tautology means that the model
A of A ∨ C is not a model of the initial clause set anymore. Hence we want to
keep the literal B without considering the tautology for propagation/conﬂict.
    To solve the issue we split our set of clauses into two parts: clauses that
are useful for propagation and clauses that can be ignored but are kept for
their literals. Thus we keep the set of all literals A constant. For our proof of
reﬁnement to the original CDCL, we have to make sure that the new behavior is
also possible in the original calculus – in particular we do not miss propagations
or conﬂicts. In the case of tautologies, this is simple (they are never used). If
we consider subsumption, like A ∨ B subsumes A ∨ B ∨ C, whenever the latter
propagates, then the former is a conﬂict. Therefore, the behavior is compatible.
    While the idea of splitting our clauses seems surprising, the additional clause
sets are only required for the connection to our CDCL transition system, and
we entirely remove them when generating the code. Moreover, the reﬁnement
is easier as we do not have to update our heuristics to remove literals (and
potentially shorten arrays). Finally, this is similar to the behavior of SAT solvers
like Kissat [4]: while the clauses are removed, all literals of the problem are set.
    In our original reﬁnement, we have split the clauses to distinguish between
clauses of length 1 (where we cannot distinguish two distinct literals and thus
they cannot ﬁt into our two-watched literals data structures) and longer clauses,
but the aim was only distinguishing on the length.
    One important point to notice is that the role of our clause sets changes. In
our original CDCL, N was the (immutable) set of initial clauses and U contains
the redundant clauses that can be removed at any point: N ensures that we do
gain new models during our transformations. Now, the set changes: strengthening
an irredundant clause from N also shortens the clause that is in there. Therefore,
a naive version could remove literals.
    Overall we have 4 sets of clauses: the irredundant clauses N and the redun-
dant U clauses, and each one is divided into the active clauses (Na and Ua ) and
the inactive (discarded) clauses (Nd and Ud ). For example, tautologies or sub-
sumed clauses are discarded, but remain in N , so literals are never removed. In
our development there are actually three sets (containing a literal set at level 0
  A More Pragmatic CDCL for IsaSAT and Targetting LLVM (Short Paper)             211

or tautologies, subsumed clauses, and false clauses) to reduce the number of case
distinction in some proofs. We never demote irredundant clauses to redundant
ones, but we can promote them.
Inprocessing Rules. Our aim when picking the rule is to be general (like
we can learn any useful clause) and then we specialize rules to speciﬁc tech-
niques. We will show this with the example of subsumption-resolution [7]. When
doing subsumption-resolution, we resolve two clauses together if the conclusion
is shorter. Then we can remove either one or both of the antecedents. For exam-
ple, resolving A ∨ B ∨ C with A ∨ ¬C produces the clause A ∨ B with subsumes
the former clause. If the latter clause was A ∨ B ∨ ¬C, the resolved clauses would
actually subsume both clauses.
    One of the most important inprocessing rule learns any possible clause. To
simplify the presentation, we will only give the rules operating on the learned
clauses, but similar rules exists for the initial set of clauses.

   inductive cdcl learn clause :: prag st ⇒ prag st ⇒ bool where
     |C| ⊆ |N + Nd | =⇒ count decided M = 0 =  ⇒
     N ∧ Nd  C =  ⇒ ¬tautology C =⇒ distinct C =
                                                   ⇒
     cdcl learn clause (M, N, U, None, Nd , Ud )
                     (M, N, U ∧ C, None, Nd , Ud )

The side conditions not only include that the clause is entailed and duplicate-
free, but also the clause is not a tautology and we do not break CDCL invariants
(count decided M = 0). Then we can deactivate subsumed clauses:

   inductive cdcl subsumed :: prag st ⇒ prag st ⇒ bool where
     C ⊆ D = ⇒ count decided M = 0 =⇒
     cdcl subsumed (M, N, U ∧ C ∧ D, None, Nd , Ud )
                   (M, N, U ∧ C, None, Nd , D ∧ Ud )

We combine these rules to express subsumption-resolution: We ﬁrst learn the
clause obtained by resolution. Then we can remove the antecedents. If either
antecedent is in N , we also have promoted the conclusion from N to U . The
advantage of our approach is that we can express other inprocessing techniques
without adding new rules, only by specializing them.
    Overall we have 9 rules with some overlap with CDCL (propagation and
conﬂict), but mostly simpliﬁcation of clauses (removing true clauses and false
literals from clauses) and pure literal deletion: When a literal always appears
positively (or always negatively), we can set this literal to be true unconditionally
(later removing all clauses containing it): every model after adding the clause is
also a model of the original set of clauses but not the opposite. This is the ﬁrst
transformation that does not preserve models in IsaSAT or any other veriﬁed
SAT solvers.
Refinement of Subsumption-Resolution. While the deﬁnition of subsump-
tion resolution is very simple, the reﬁnement to code was challenging.
212     M. Fleury and P. Lammich

    We veriﬁed forward subsumption [7] following CaDiCaL [5] (unbounded how-
ever, so all clauses selected heuristically are checked). We sort clauses by size
and check if the current candidate is subsumed by one of the smaller clauses.
Because we use two-watched literals, we need to distinguish between the binary
clauses (than can produce new units) and the other clauses. At the end, we
implemented two forward subsumption passes: one for binary clauses only and
the other for larger clauses.
    To subsume the candidates, we build occurrence lists and populate them with
binary clauses, whereas Kissat [5] reuses watch lists. Moreover, for eﬃciency,
we need a new marking data structure for eﬃcient detection of subsuming-
resolution.


4     Correctness of the Code and Completeness

Our speciﬁcation model if satisfiable takes the multiset of clauses and returns
a model (if there is one) or None if the clauses are unsatisﬁable. Our imple-
mentation IsaSATSML opts takes an array containing the clauses and returns an
optional array containing the assignment, assuming that the clauses do not con-
tain duplicated literals or the empty clause (precondition proper lits no dups ⊥).
The additional argument opts activates and deactivates certain techniques for
solving. The following theorem states that our implementation reﬁnes the spec-
iﬁcation:

Theorem 1 (SML End-to-End Correctness). The following refinement
relation holds:

             (IsaSATSML opts, model if satisfiable)
           ∈ [proper lits no dups ⊥] clauses assn → option model assn

    The LLVM version is nearly the same. It can handle duplicated literals and
the empty clause. Moreover, the new speciﬁcation model if satisfiable bounded
allows for an unknown result if arrays would grow larger than the size permitted
by the ﬁxed bit-width. While this limit does not exist in Imperative HOL, it
exists in practice as no machine supports arrays that large. Therefore, we tech-
nically weakened our theorem, but did not change practical guarantees on the
generated code. For IsaSATSML we start [12] with 64-bit unsigned integers and
only switch to GMP integers if the arrays grow too large.

Theorem 2 (LLVM End-to-End Correctness). The following refinement
relation holds:

           (IsaSATLLVM opts, RETURN ◦ model if satisfiable bounded)
         ∈ [proper lits] clauses assn → option model assn

  Moreover, the change from SML to LLVM reduces the trusted code base:
The Isabelle/LLVM model is closer to the actual LLVM, such that the trusted
    A More Pragmatic CDCL for IsaSAT and Targetting LLVM (Short Paper)          213

pretty-printer is simpler. LLVM is also more low-level, such that fewer parts of
the compiler have to be trusted. Finally, the LLVM compiler is more widely used
and tested than the rather niche MLton compiler we used before.


5     Experience Porting the Development to LLVM
We report on the challenges we faced when updating the huge IsaSAT formaliza-
tion (Sect. 5.1). Moreover, we report on the unveriﬁed parts of IsaSAT (Sect. 5.2),
and ﬁnally compile some lessons learned (Sect. 5.3).


5.1    Required Changes

Before porting the development to LLVM, we removed our only remaining source
of unbounded integers: the clause indices during the garbage collection. As
garbage collection does not happen very often, we did not expect this to make
a diﬀerence. Surprisingly, it turns out to have a performance impact.
    Isabelle/LLVM is an entire tool set, including a fork of the original Sepref
tool. While related to the original Sepref tool, there are diﬀerent libraries, and
the development of the two versions has diverged.
    Initially, we tried to support both versions of Sepref. We ended up with two
sets of ﬁles for code synthesis, and duplication of some libraries (to provide
constants deﬁned in Isabelle/LLVM but not in SeprefSML ). This signiﬁcantly
complicated our reﬁnement approach, although we made it conceptually cleaner
during the porting. Then, we realized that IsaSATLLVM was much faster than
IsaSATSML (we observed a factor 2 on our test ﬁles), and decided to discontinue
the SML backend.
    With this, also some workarounds for SML speciﬁc performance issues (like
the tuple uint32 * bool * uint64 being much less eﬃcient than combining
the uint32 and the Boolean into a single 64-bit number) became obsolete.
Compilation. We have experimented with compilation ﬂags before to improve
performance. We know from the SML code that we need to increase the level of
inlining, because many small functions make the veriﬁcation easier. The same
applies for LLVM and the easiest solution is to use link-time optimization that
increases the inlining level as a side eﬀect. However, this makes proﬁling impos-
sible – exactly like the SML code. So there is no regression here.
Tuples. In 2021, we observed a major performance regression of the synthe-
sis, caused by a new feature in SeprefLLVM : pointer-equality tracking caused
quadratic behaviour for case-splits of tuples. As our solver state is a large tuple,
synthesis became impossible (several dozen minutes for simple functions).
    To avoid the issue, we decided to work around on the abstract level, using
getter and setter functions for the state’s components, rather than case splitting.
Now, every function on the state would ﬁrst get the required components, update
them, and then put them back. For example:
214    M. Fleury and P. Lammich

   definition rescore conflict :: clause index ⇒ isasat ⇒ isasat where
     rescore conflict C S = do{
        let (M, S) = extract trail S;
        ... (*reads the trail M and can change it*) ...
        let S = update trail M S;
        RETURN S
     }

This makes synthesis much faster. However, the ownership model of Sepref does
not allow aliasing, nor do our reﬁnement relations allow leaving a ’gap’ in the
state where we moved out an element. As an easy work-around, we resorted to
placing dummy-values, like empty lists, in the state, hoping that LLVM would
optimize away the allocations and deallocations for these values. However, this
did not happen: In the hot-spot of the SAT solver, the propagation loop, the
dummy value for the trail was recreated and freed each time. Thus, we locally
resorted to unfolding our code to make sure that we need only one free in the
inner propagation loop. We leave a more principled solution of this problem
(possibly changing Sepref) to future work.
    We even attempted to go one step further (as the state-of-the-art SAT solver
Kissat [4] does) and simply passing a pointer to the state structure as argument.
Once we had already changed our reﬁnement with accessors, we simply had
to change them to work on a pointer. However, we never managed to make
the synthesized code eﬃcient. We observed a factor of 10 slower code. Hand-
optimizing the accessors (basically making sure that LLVM understands that
we care only about one component) reduced this to factor 2 slower. Once we
realized that the LLVM optimizer was replacing the pointer by the structure
passed directly as argument, we gave up on that approach.


5.2   Unverified Parts

In the generated SAT solver, there are some parts that we cannot verify. First,
the parser is not veriﬁed, because the ﬁle system has no model in Isabelle (unlike
CakeML, where conditions apply however). To this end, we link the veriﬁed code
with an unveriﬁed C program, which provides the parser and command line
interface.
    Second, Isabelle/LLVM does not support any output (like statistics, or the
DRAT proofs [28] required for the SAT Competition). For the SML version, we
could use a feature of Isabelle’s code generator to (axiomatically) implement
a function by some external function (e.g. a function that does nothing in the
model, by a printing function). As Isabelle/LLVM does not yet have such a
feature, we resorted to post-processing the generated code (i.e., a function that
does nothing in the model, is replaced by a printing function or even a function
storing some literals for DRAT proofs). Note that this post-processing is not
required for IsaSAT to work (but it won’t print DRAT proofs).
  A More Pragmatic CDCL for IsaSAT and Targetting LLVM (Short Paper)            215

5.3   Lessons Learned

Lesson 1: Embrace Duplication. We have already highlighted the importance
of the set of all possible literals A, in particular to establish a bound on the
size of various arrays. At ﬁrst, we tried to avoid duplicating this set across the
diﬀerent components on the speciﬁcation side. This, however, resulted in a closer
coupling of the various reﬁnement proofs, impeding modularity: data structures
that, conceptually, are just a small part of the whole state, have to be formalized
on the whole state, just to have the set A available. We solved this problem by
duplicating the set A on the abstract level for all new data structures. Note that
this duplication is removed in a later reﬁnement stage.
Lesson 2: The Limits are Isabelle Files. Checking our Isabelle ﬁles takes
nearly two hours. This can be explained by three factors: 1. the heuristic and
code synthesis amounts to 91 000 loc, making it a very large formalization; 2. the
synthesis is single-threaded (for technical reasons); 3. Sepref encourages a style
that is not very parallel: every reﬁnement starts with a call to a tactic refine vcg
that generates the goals (meaning that all successive tactics have to wait). To
improve performance we have attempted [12] to generate more standard proofs
in Isar (by generating the text corresponding to the theorems to prove), but it
is not clear that this style is faster as huge number of variables are generated
(this style is required for more complicated proofs, however).
     In order to improve Isabelle’s performance and speed-up the testing of new
heuristics in IsaSATLLVM , we have split the ﬁles into three parts: the shared def-
initions of the functions to reﬁne, the (single-threaded) synthesis, and the cor-
rectness proof of the reﬁnement. Even with these optimizations, proof checking
still takes 2 h. There is also no clear improvement path. The old SML version has
a similar problem, but it is overall faster because it has fewer features, making
it less critical.
Lesson 3: Performance Bugs exist. In order to improve performance, we
need to measure and observe performance. To solve that problem, IsaSAT prints
statistics and produces some timing information. The statistics during the run
made identifying scheduling bugs for the diﬀerent techniques possible – we acci-
dentally ran some techniques way too often or barely ever. Especially because
we increase the interval between two inprocessing rounds geometrically, a simple
statistics at the end of the run is not suﬃcient. One interesting performance
bug we found was that we accidentally inverted reducing clauses (marking them
as removed) and garbage collection (physically removing them). Therefore, we
would nearly always physically delete clauses. We never saw this issue, because
we also printed the statistics inverted. To help debugging performance, we pro-
duce some timing information by measuring time in the C program:

c propagate                : 83.48% (581.66 s)
c reduce                   : 0.12% (0.82 s)
c subsumption              : 0.06% (0.39 s)
c pure_lits                : 0.05% (0.33 s)
216    M. Fleury and P. Lammich




                  Fig. 1. CDF of the performance of SAT solvers


c binary_simp              : 0.02% (0.15 s)
c GC                       : 0.16% (1.10 s)
This helps to identify bottlenecks but also outliers where one technique is par-
ticularly slow and requires some limits or a change in the scheduling to avoid
slowing down the solver too much. This makes it possible to identify errors like
allocations in loops. The overall timing matches what we expect from other
SAT solvers (although usually they spend more time on inprocessing and less on
propagation).


6     Performance
In order to study the performance we have run 3 diﬀerent IsaSAT versions:
the original SML solver (using MLton with the LLVM backend), the ﬁrst port
of the IsaSAT solver, and the current version with inprocessing and various
other improvements on heuristics that do not require any change on our PCDCL
calculus, notably rephasing and target phases [10] (but no local search) and the
alternation between aggressive restarts (heuristically seems better for UNSAT)
and few restarts (seems better for SAT) following the ideas of Chanseok Oh [24].
    We run all the benchmarks from the SAT Competition 2022 on an Intel Xeon
E5-2620 v4 CPU at 2.10 GHz (with turbo-mode disabled) with a memory limit
of 7 GB and a timeout of 5000 s. For comparison, we have included versat [23]
and CreuSAT [25]. For completeness, we have included Kissat [6] (more precisely
the bulky version submitted for the anniversary track).
    The results are given in Fig. 1 as a CDF (the higher the curve, the more solved
problems). The ﬁrst surprise is that CreuSAT performs similarly to IsaSATSML
(37 vs 40 solved problems), worse than expected given the results reported in the
    A More Pragmatic CDCL for IsaSAT and Targetting LLVM (Short Paper)               217

Master’s thesis [25] that tested on the 2015 benchmarks. We suspect that is due
to the garbage collection and the fact that problems from the SAT Competition
have become harder.
    There is a clear improvement when going from the SML version to the LLVM
version (98 solved), while the latest version solves 166. The SML version produces
335 out-of-memory errors (OOMs), the base LLVM version is more memory
eﬃcient (23 OOMs) like the latest IsaSAT version (19 OOMs) or CaDiCaL that
has the same memory layout (17 OOMs). However, there is still a large gap to
reach the performance level of Kissat and its inprocessing techniques.


7     Conclusion
We have reported on updating our veriﬁed SAT solver IsaSAT to a more powerful
base calculus (our pragmatic CDCL) which can express inprocessing, and to the
more eﬃcient Isabelle/LLVM backend. We have also compiled important lessons
learned from proof-engineering and maintaining large formalizations like IsaSAT
(∼200 kloc of proofs).
    Our changes made IsaSAT solve 4 times more problems (166/40), making it
the most eﬃcient veriﬁed SAT solver. At the same time, our veriﬁcation is more
complete than the next fastest veriﬁed solvers.
    Most techniques (including the two most important, viviﬁcation and probing)
either ﬁt into our new PCDCL base calculus or do not require any change (like
random walk [10] that is conjectured to be the reason for the major performance
improvement in 2020). One major technique that we cannot currently express is
variable elimination, because models are changed and need to be ﬁxed. We leave
the required extensions to our PCDCL for future work.

Acknowledgments. The work presented here was done over several years and several
work places. The ﬁrst author was supported for some time by Austrian Science Fund
(FWF), NFN S11408-N23 (RiSE), and the LIT AI Lab funded by the State of Upper
Austria. We thank the anonymous reviewers for their detailed comments.


References
 1. Andrici, C.C., Ciobâcă, S.: A veriﬁed implementation of the DPLL algorithm in
    Dafny. Mathematics 10(13), 1–26 (2022). https://ideas.repec.org/a/gam/jmathe/
    v10y2022i13p2264-d850381.html
 2. Balyo, T., Heule, M., Iser, M., Järvisalo, M., Suda, M. (eds.): Proceedings of SAT
    Competition 2022: Solver and Benchmark Descriptions. Department of Computer
    Science Series of Publications B, Department of Computer Science, University of
    Helsinki, Finland (2022)
 3. Becker, H., et al.: IsaFoL: Isabelle formalization of logic. https://bitbucket.org/
    isafol/isafol/
 4. Biere, A., Fazekas, K., Fleury, M., Heisinger, M.: CaDiCaL, Kissat, Paracooba,
    Plingeling and Treengeling entering the SAT Competition 2020. In: Balyo, T.,
    Froleyks, N., Heule, M., Iser, M., Järvisalo, M., Suda, M. (eds.) Proceedings of SAT
218     M. Fleury and P. Lammich

    Competition 2020 - Solver and Benchmark Descriptions. Department of Computer
    Science Report Series B, vol. B-2020-1, pp. 51–53. University of Helsinki (2020)
 5. Biere, A., Fazekas, K., Fleury, M., Heisinger, M.: CaDiCaL, Kissat, Paracooba,
    Plingeling and Treengeling entering the SAT Competition 2021. In: Proceedings of
    the SAT Competition 2021 - Solver and Benchmark Descriptions (2021). submitted
 6. Biere, A., Fleury, M.: Gimsatul, IsaSAT and Kissat entering the SAT Competition
    2022. In: Balyo, T., Heule, M., Iser, M., Järvisalo, M., Suda, M. (eds.) Proceedings
    of the SAT Competition 2022 - Solver and Benchmark Descriptions. Department
    of Computer Science Series of Publications B, vol. B-2022-1, pp. 10–11. University
    of Helsinki (2022)
 7. Biere, A., Järvisalo, M., Kiesl, B.: Preprocessing in SAT solving. In: Biere, A.,
    Heule, M., van Maaren, H., Walsh, T. (eds.) Handbook of Satisﬁability, Frontiers
    in Artiﬁcial Intelligence and Applications. 2nd edn, vol. 336, pp. 391–435. IOS
    Press (2021). https://doi.org/10.3233/FAIA200992
 8. Blanchette, J.C., Fleury, M., Lammich, P., Weidenbach, C.: A veriﬁed SAT solver
    framework with learn, forget, restart, and incrementality. J. Autom. Reason. 61(1–
    4), 333–365 (2018). https://doi.org/10.1007/s10817-018-9455-7
 9. Bulwahn, L., Krauss, A., Haftmann, F., Erkök, L., Matthews, J.: Imperative func-
    tional programming with Isabelle/HOL. In: Mohamed, O.A., Muñoz, C., Tahar, S.
    (eds.) TPHOLs 2008. LNCS, vol. 5170, pp. 134–149. Springer, Heidelberg (2008).
    https://doi.org/10.1007/978-3-540-71067-7 14
10. Cai, S., Zhang, X., Fleury, M., Biere, A.: Better decision heuristics in CDCL
    through local search and target phases. J. Artif. Intell. Res. 74, 1515–1563 (2022).
    https://doi.org/10.1613/jair.1.13666
11. Fazekas, K., Biere, A., Scholl, C.: Incremental inprocessing in SAT solving. In:
    Janota, M., Lynce, I. (eds.) SAT 2019. LNCS, vol. 11628, pp. 136–154. Springer,
    Cham (2019). https://doi.org/10.1007/978-3-030-24258-9 9
12. Fleury, M.: Optimizing a Veriﬁed SAT Solver. In: Badger, J.M., Rozier, K.Y. (eds.)
    NFM 2019. LNCS, vol. 11460, pp. 148–165. Springer, Cham (2019). https://doi.
    org/10.1007/978-3-030-20652-9 10
13. Fleury, M.: IsaSAT and Kissat entering the EDA Challenge 2021 (2021). https://
    www.eda-ai.org/results/, system description accepted at the EDA Challenge 2021.
    https://m-ﬂeury.github.io/ox-hugo/Fleury-EDA-Challenge-2021.pdf
14. Haftmann, F., Nipkow, T.: Code generation via higher-order rewrite systems. In:
    Blume, M., Kobayashi, N., Vidal, G. (eds.) FLOPS 2010. LNCS, vol. 6009, pp.
    103–117. Springer, Heidelberg (2010). https://doi.org/10.1007/978-3-642-12251-
    49
15. Järvisalo, M., Heule, M.J.H., Biere, A.: Inprocessing rules. In: Gramlich, B., Miller,
    D., Sattler, U. (eds.) IJCAR 2012. LNCS (LNAI), vol. 7364, pp. 355–370. Springer,
    Heidelberg (2012). https://doi.org/10.1007/978-3-642-31365-3 28
16. Lammich, P.: Automatic data reﬁnement. In: Blazy, S., Paulin-Mohring, C.,
    Pichardie, D. (eds.) ITP 2013. LNCS, vol. 7998, pp. 84–99. Springer, Heidelberg
    (2013). https://doi.org/10.1007/978-3-642-39634-2 9
17. Lammich, P.: Reﬁnement to imperative HOL. J. Autom. Reason. 62(4), 481–503
    (2017). https://doi.org/10.1007/s10817-017-9437-1
18. Lammich, P.: Generating veriﬁed LLVM from Isabelle/HOL. In: Harrison, J.,
    O’Leary, J., Tolmach, A. (eds.) 10th International Conference on Interactive The-
    orem Proving, ITP 2019, 9–12, September 2019, Portland, OR, USA. LIPIcs, vol.
    141, pp. 22:1–22:19. Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2019).
    https://doi.org/10.4230/LIPIcs.ITP.2019.22
  A More Pragmatic CDCL for IsaSAT and Targetting LLVM (Short Paper)                219

19. Lammich, P.: Eﬃcient veriﬁed (UN)SAT certiﬁcate checking. J. Autom. Reason.
    64(3), 513–532 (2019). https://doi.org/10.1007/s10817-019-09525-z
20. Lattner, C., Adve, V.: LLVM: a compilation framework for lifelong program analy-
    sis & transformation. In: International Symposium on Code Generation and Opti-
    mization, 2004. CGO 2004, pp. 75–88. IEEE (2004). https://doi.org/10.1109/cgo.
    2004.1281665
21. Moskewicz, M.W., Madigan, C.F., Zhao, Y., Zhang, L., Malik, S.: Chaﬀ: Engi-
    neering an eﬃcient SAT solver. In: Proceedings of the 38th Design Automation
    Conference, DAC 2001, Las Vegas, NV, USA, 18–22 June 2001, pp. 530–535. ACM
    (2001). https://doi.org/10.1145/378239.379017
22. Nipkow, T., Wenzel, M., Paulson, L.C. (eds.): Isabelle/HOL: A Proof Assistant
    for Higher-Order Logic. LNCS, vol. 2283. Springer, Heidelberg (2002). https://
    doi.org/10.1007/3-540-45949-9
23. Oe, D., Stump, A., Oliver, C., Clancy, K.: versat: a veriﬁed modern SAT solver. In:
    Kuncak, V., Rybalchenko, A. (eds.) VMCAI 2012. LNCS, vol. 7148, pp. 363–378.
    Springer, Heidelberg (2012). https://doi.org/10.1007/978-3-642-27940-9 24
24. Oh, C.: Between SAT and UNSAT: the fundamental diﬀerence in CDCL SAT. In:
    Heule, M., Weaver, S. (eds.) SAT 2015. LNCS, vol. 9340, pp. 307–323. Springer,
    Cham (2015). https://doi.org/10.1007/978-3-319-24318-4 23
25. Skotåm, S.H.: CreuSAT - using rust and Creusot to create the world’s fastest
    deductively veriﬁed SAT solver. Master’s thesis, University of Oslo (2022). https://
    www.duo.uio.no/handle/10852/96757
26. Tan, Y.K., Heule, M.J.H., Myreen, M.O.: cake lpr: veriﬁed propagation redun-
    dancy checking in CakeML. In: TACAS 2021. LNCS, vol. 12652, pp. 223–241.
    Springer, Cham (2021). https://doi.org/10.1007/978-3-030-72013-1 12
27. Weeks, S.: Whole-program compilation in MLton. In: Proceedings of the ACM
    Workshop on ML, 2006, Portland, Oregon, USA, 16 September 2006, p. 1. ACM
    Press (2006). https://doi.org/10.1145/1159876.1159877
28. Wetzler, N., Heule, M.J.H., Hunt, W.A.: DRAT-trim: eﬃcient checking and trim-
    ming using expressive clausal proofs. In: Sinz, C., Egly, U. (eds.) SAT 2014. LNCS,
    vol. 8561, pp. 422–429. Springer, Cham (2014). https://doi.org/10.1007/978-3-319-
    09284-3 31




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
