    Regression Veriﬁcation - A Practical Way to
                 Verify Programs

                          Ofer Strichman and Benny Godlin

                             Technion, Haifa, Israel
              ofers@ie.technion.ac.il, bgodlin@cs.technion.ac.il




1    Introduction

When considering the program veriﬁcation challenge [8] one should not forget a
lesson learned in the testing community: when it comes to industrial size pro-
grams, it is not realistic to expect programmers to formally specify their program
beyond simple assertions. It is well known that large parts of real code cannot be
described naturally with high level invariants or temporal properties, and fur-
ther that it is often the case that the process of describing what a code segment
should do is as diﬃcult and at least as complicated as the coding itself. Indeed,
high-level temporal property-based testing, although by now supported by com-
mercial tools such as Temporal-Rover[4], is in very limited use. The industry
typically attempts to circumvent this problem with Regression Testing, which
is probably the most popular testing method for general computer programs. It
is based on the idea of reasoning by induction: check an initial version of the
software when it is still very simple, and then check that a newer version of the
software produces the same output as the earlier one, given the same inputs. If
this process results with a counterexample, the user is asked to check whether
it is an error or a legitimate change. In the latter case the testing database is
updated with the new ‘correct’ output value. Regression Testing does not re-
quire a formal speciﬁcation of the investigated system nor a deep understanding
of the code, which makes it highly suitable for accompanying the development
process, especially if it involves more than one programmer. We propose to learn
from this experience and develop techniques for Regression Veriﬁcation. The
underlying proof engine is still a certifying compiler as envisioned by the grand
challenge, so this proposal should be thought of as another application of this
technology that makes the veriﬁcation picture more complete.
   While formally proving equivalence between two programs is generally un-
decidable, if one is willing to sacriﬁce completeness this becomes not only a
decidable problem, but also one that can be built on top of existing tools. With-
out completeness, the equivalence problem can be reduced to one of proving an
assertion on a merged program (see next section), for which functional veriﬁca-
tion techniques can be used. Thus, Regression veriﬁcation should be thought of
as an additional layer, or dimension, to be dealt with as part of the veriﬁcation
challenge.

B. Meyer and J. Woodcock (Eds.): Veriﬁed Software, LNCS 4171, pp. 496–501, 2008.

c IFIP International Federation for Information Processing 2008
               Regression Veriﬁcation - A Practical Way to Verify Programs      497

When can Regression-veriﬁcation be useful? A natural question to ask
is whether proving equivalence is relevant in the context of a real software de-
velopment process, as in such a process the program is expected to produce a
diﬀerent output after every revision. While this is in general true, consider the
following scenarios, all of which are targeted by our approach:

 – Checking side-eﬀects of new code. Suppose, for example, that from version
   1.0 to version 1.1 a new ﬂag was added, that changes the result of the com-
   putation. It is desirable to prove that as long as this ﬂag is turned oﬀ, the
   previous functionality is maintained. The RV tool we propose will allow the
   user to express a condition (the inactivation of the ﬂag in this case) under
   which the two programs are expected to produce equal outputs.
 – Checking performance optimizations. After adding an optimization of the
   code for performance purposes, it is desirable to verify that the two versions
   of the code still produce the same output.
 – Manual Re-factoring (a popular set of techniques for rewriting existing code
   for various purposes). To quote Martin Fowler [6,5], the founder of this ﬁeld,
   ‘Refactoring is a disciplined technique for restructuring an existing body of
   code, altering its internal structure without changing its external behavior. Its
   heart is a series of small behavior preserving transformations. Each transfor-
   mation (called a ’refactoring’) does little, but a sequence of transformations
   can produce a signiﬁcant restructuring. Since each refactoring is small, it’s
   less likely to go wrong. The system is also kept fully working after each small
   refactoring, reducing the chances that a system can get seriously broken dur-
   ing the restructuring.’ Equivalence proof, before and after refactoring, seems
   valuable in this case.

This list demonstrates, but does not exhaust, the scenarios in which such a tool
can be used.
                                                                                
                                                                                
   At the Technion we are currently developing a method for formally verifying
the equivalence of two closely related C programs, under certain restrictions
inherited from the functional veriﬁcation tool we use. One of the main challenges
is to ﬁnd ways to beneﬁt from the similarity of the two programs, in order to
scale-up the veriﬁcation system beyond what is currently possible for verifying
a single program. In particular, we are trying to make the complexity depend
only on the diﬀerences between the two programs (including the propagation of
these changes to other parts of the program), rather than on their original sizes.
We dedicate the next section for giving a brief description of this project, after
which we will summarize what we believe are the main challenges in making
veriﬁcation by regression widely used.


2   Proving Equivalence of Two C Programs
In the rest of this note we concentrate on C programs. Automated (incomplete)
veriﬁcation tools that work directly on widely used programming languages such
498     O. Strichman and B. Godlin

as C were ﬁrst made available only a few years ago. We are aware of three
categories of such tools: 1) Predicate-abstraction-based tools such as blast [7],
slam [2] and magic [3], 2) Symbolic search of a bounded model of the program,
as in saturn [14] and cbmc [10], and 3) Explicit state tools such as SPIN
(in combination with feaver [9]) and CMC [11]. Each of the tools in these
three categories is a candidate for serving as an infrastructure for Regression
Veriﬁcation, although adapting each one of them for this task presents a research
challenge by its own right.
   Our prototype implementation uses cbmc as the underlying decision proce-
dure, since it is one of the two tools (together with CMC) that supports full C
and C++. In the rest of this note we exclusively focus on this category.


2.1   The cbmc Tool

cbmc [10], developed by D. Kroening, is a Bounded Model Checking tool for
full ANSI-C and C++ programs. For each loop i in the given program, the
user is required to specify a bound ki on the number of iterations. This enables
cbmc to symbolically characterize the full set of possible executions restricted
by these bounds, with a propositional formula f . The existence of a solution to
f ∧ ¬a, where a is a user deﬁned assertion, implies that there is a path in the
program that violates a. Otherwise, it is still possible that the given bounds are
not suﬃciently high. cbmc allows the user to check whether the bounds are high
‘enough’ by generating special unwinding assertions for each loop. An unwinding
assertion for a loop i, given ki , is satisﬁed iﬀ the condition of this loop cannot
be true after iterating ki times. Thus, cbmc can be thought of as a complete
tool as long as all the loops are terminating.


2.2   A Regression Veriﬁcation Tool for C Programs

We started building a Regression Veriﬁcation tool that generates a combined C
program that is unrolled and checked by cbmc. Our program performs several
simpliﬁcations and abstractions using Uninterpreted Functions as we explain in
Section 2.3. The user is involved in two phases:

 – The user needs to supply a list of pairs

               label#1, expression#1, label#2, expression#2 . . .

   representing his/her speciﬁcation that expression#1 in the location speciﬁed
   by label#1 in the ﬁrst program, should always be equal to expression#2
   in location label#2 in the second program. In other words, the sequence of
   values of these two expressions in these locations should be equal regardless
   of the inputs. A special case of this option is specifying that the outputs of
   the program are equal.
 – When a counterexample is found, the user needs to conﬁrm whether it rep-
   resents an error or a legitimate change resulting from further development of
                   Regression Veriﬁcation - A Practical Way to Verify Programs       499

      the investigated program. The problem is that there can be an exponential
      number of examples due to a single change, so approving them one by one
      is not a desirable option. We plan to give the user the option of describ-
      ing symbolically the allowed changes between the two programs, and also of
      determining dynamically the subset of outputs to concentrate on.


2.3     Optimizations with Uninterpreted Functions

Veriﬁcation can be made simpler by using automated abstraction and decompo-
sition. In the context of proving equivalence, Uninterpreted Functions has proven
to be a highly eﬀective tool (see, for example, the case of Translation Validation
[13,12]).
    In the following description we use unprimed and primed variables to distin-
guish between variables that belong to the old (unprimed) and new (primed)
versions of the code. Consider, for example, a function intf (x1 . . . xn ) that is
syntactically equivalent to its counterpart intf (x1 . . . xn ) in the new code, and
assume that they do not call other functions. We would like in this case to hide
the content of f and f  while assuring that if the input to both functions is
the same, then so is their output and side eﬀects. Assume that f is reading the
values of the global variables in a set Gr and writes to a set of global variables
Gw (Gr and Gw are not necessarily disjoint)1 . We observe that if f and f  are
called with the same arguments, and all variables in Gr have the same values as
their counterparts in Gr when f and f  are called, then the return value of f and
f  is the same, as well as the values in Gw and Gw . Based on this observation,
we represent the functions f and f  with two new variables of type int, say fv
and fv , and add the following constraint:


            
            n
        (       xi = xi ∧ ∀gr ∈ Gr .gr = gr ) → (fv = fv ∧ ∀gw ∈ Gw .gw = gw
                                                                              
                                                                                )    (1)
         i=1

This type of (conservative) abstraction can be seen as a simple extension of a
method suggested by Ackermann [1], who considered the case in which there
are no side eﬀects. There are various complications when using this kind of
simpliﬁcation, some of which are:

 – Recursive and mutually recursive functions require proofs by induction.
 – A change in a function renders all its ancestors in the call-graph unsuitable
   for replacement with Uninterpreted Functions. We attempt to minimize this
   eﬀect in two ways. First, we attempt to prove that although the two func-
   tions are syntactically diﬀerent, they are still semantically the same. Second,
   we consider Uninterpreted Scopes, which are more ﬁne-grained than Unin-
   terpreted Functions, and hence less sensitive to the propagation of changes.
1
    We consider here local variables declared as static as a special case of global vari-
    ables.
500      O. Strichman and B. Godlin

 – Function arguments and global variables can be pointers, which makes Equa-
   tion (1) unusable (obviously the two pointers represent diﬀerent memory ad-
   dresses). We are currently investigating various syntactic analysis methods
   in order to be able to check, at least in some cases, whether two pointers
   point to two isomorphic objects.


2.4    Summary

Compared with existing C veriﬁcation tools, all of which are property based,
Regression Veriﬁcation has two things to oﬀer. First, code that cannot be easily
checked against a formal speciﬁcation can still be checked throughout the devel-
opment process by examining its evolving eﬀect on the output (or, in fact, on
internal variables as well, which helps pin-pointing the cause for the diﬀerence).
Second, comparing two similar systems is in most cases computationally easier
than property-based veriﬁcation2 . The reason for this is that there are various
optimizations and decomposition opportunities that are only relevant when com-
paring two closely related systems. We described one such optimization based
on Uninterpreted Functions in section 2.3.


3     The Road Ahead

Veriﬁcation by regression poses numerous technical challenges, some of which
are:

 – Adapting other existing techniques for formally verifying a single program to
   proving equivalence, most notably predicate abstraction. Our current choice
   of the C language and the tool cbmc as a starting point is largely due to
   the maturity of the tool rather than some deep theoretical reason.
 – Achieving scalability and automation beyond what is possible in functional
   veriﬁcation. Abstracting portions of the program with uninterpreted func-
   tions, as explained above, is one possible technique that is challenging by
   itself in the presence of dynamic data structures, aliasing, arrays and so
   forth. Various Static Analysis techniques (like Pointer Analysis and Shape
   Analysis) seem relevant to this question.
 – Identifying (either manually or automatically) what variables (outputs or
   others) and in which locations should be equal in order to increase the con-
   ﬁdence in the correctness of the changes.
 – Identifying the connection between functional properties and equivalence
   properties: assuming that a certain early version of the program satisﬁes
   some invariants or other high level property, which variables should be fol-
   lowed through the evolvement of the program to guarantee that this property
   still holds ? under which conditions this is decidable?
2
    The same observation is well known in the hardware domain, where equivalence
    checking of circuits is considered computationally easier in practice than model-
    checking.
               Regression Veriﬁcation - A Practical Way to Verify Programs         501

 – Finding the ideal gap between two versions of the same program, for making
   Regression Veriﬁcation most eﬀective. There is an apparent tradeoﬀ between
   larger gaps, which reduce the overhead of proving equivalence, and the ef-
   fectiveness of comparing the two versions of the code.


References
 1. Ackermann, W.: Solvable cases of the Decision Problem. In: Studies in Logic and
    the Foundations of Mathematics, North-Holland, Amsterdam (1954)
 2. Ball, T., Rajamani, S.: Automatically validating temporal safety properties of in-
    terfaces. In: Dwyer, M.B. (ed.) SPIN 2001. LNCS, vol. 2057, Springer, Heidelberg
    (2001)
 3. Chaki, S., Clarke, E., Groce, A., Jha, S., Veith, H.: veriﬁcation of software com-
    ponents in C. In: International Conference on Software Engineering (ICSE) (2003)
    (to appear)
 4. Drusinsky, D.: The Temporal Rover and the ATG Rover. In: Havelund, K., Penix,
    J., Visser, W. (eds.) SPIN 2000. LNCS, vol. 1885, Springer, Heidelberg (2000)
 5. Fowler, M.: http://www.refactoring.com
 6. Fowler, M.: Refactoring: Improving the Design of Existing Code. Addison-Wesley,
    Reading (1999)
 7. Henzinger, T.A., Jhala, R., Majumdar, R., Sutre, G.: Lazy abstraction. In: Sym-
    posium on Principles of Programming Languages, pp. 58–70 (2002) (BLAST)
 8. Hoare, T.: The verifying compiler: A grand challenge for computing research. J.
    ACM 50(1), 63–69 (2003)
 9. Holzmann, G., Smith, M.: An automated veriﬁcation method for distributed sys-
    tems software based on model extraction. IEEE Trans. on Software Engineer-
    ing 28(4), 364–377 (2002)
10. Kroening, D., Clarke, E., Yorav, K.: Behavioral consistency of C and Verilog pro-
    grams using bounded model checking. In: Proceedings of DAC 2003, pp. 368–371.
    ACM Press, New York (2003)
11. Musuvathi, M., Park, D.Y., Chou, A., Engler, D.R., Dill, D.L.: Cmc: A pragmatic
    approach to model checking real code. OSDI 2002 (2002)
12. Pnueli, A., Rodeh, Y., Strichman, O., Siegel, M.: The small model property: How
    small can it be? Information and computation 178(1), 279–293 (2002)
13. Pnueli, A., Siegel, M., Singerman, E.: Translation validation. In: Steﬀen, B. (ed.)
    ETAPS 1998 and TACAS 1998. LNCS, vol. 1384, Springer, Heidelberg (1998)
14. Xie, Y., Aiken, A.: Scalable error detection using boolean satisfability. In: POPL
    2005: Proceedings of the 32nd ACM SIGPLAN-SIGACT sysposium on Principles
    of programming languages, ACM Press, New York (2005)
