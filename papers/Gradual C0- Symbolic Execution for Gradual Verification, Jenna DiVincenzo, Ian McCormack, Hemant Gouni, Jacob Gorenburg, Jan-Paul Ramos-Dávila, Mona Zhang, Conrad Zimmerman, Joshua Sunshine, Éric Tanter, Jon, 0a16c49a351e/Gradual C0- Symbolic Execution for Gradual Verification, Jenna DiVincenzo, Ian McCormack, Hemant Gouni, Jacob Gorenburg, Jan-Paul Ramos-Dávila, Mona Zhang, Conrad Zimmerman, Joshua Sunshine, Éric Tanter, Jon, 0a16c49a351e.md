                                         Gradual C0: Symbolic Execution for Gradual Verification
                                         JENNA DIVINCENZO, Purdue University, USA
                                         IAN MCCORMACK, Carnegie Mellon University, USA
                                         HEMANT GOUNI, Carnegie Mellon University, USA
arXiv:2210.02428v3 [cs.LO] 19 Jan 2024




                                         JACOB GORENBURG, Haverford College, USA
                                         JAN-PAUL RAMOS-DÁVILA, Cornell University, USA
                                         MONA ZHANG, Columbia University, USA
                                         CONRAD ZIMMERMAN, Brown University, USA
                                         JOSHUA SUNSHINE, Carnegie Mellon University, USA
                                         ÉRIC TANTER, University of Chile, Chile
                                         JONATHAN ALDRICH, Carnegie Mellon University, USA
                                         Current static verification techniques such as separation logic support a wide range of programs. However,
                                         such techniques only support complete and detailed specifications, which places an undue burden on users.
                                         To solve this problem, prior work proposed gradual verification, which handles complete, partial, or missing
                                         specifications by soundly combining static and dynamic checking. Gradual verification has also been extended
                                         to programs that manipulate recursive, mutable data structures on the heap. Unfortunately, this extension
                                         does not reward users with decreased dynamic checking as specifications are refined. In fact, all properties
                                         are checked dynamically regardless of any static guarantees. Additionally, no full-fledged implementation of
                                         gradual verification exists so far, which prevents studying its performance and applicability in practice.
                                            We present Gradual C0, the first practicable gradual verifier for recursive heap data structures, which targets
                                         C0, a safe subset of C designed for education. Static verifiers supporting separation logic or implicit dynamic
                                         frames use symbolic execution for reasoning; so Gradual C0, which extends one such verifier, adopts symbolic
                                         execution at its core instead of the weakest liberal precondition approach used in prior work. Our approach
                                         addresses technical challenges related to symbolic execution with imprecise specifications, heap ownership,
                                         and branching in both program statements and specification formulas. We also deal with challenges related
                                         to minimizing insertion of dynamic checks and extensibility to other programming languages beyond C0.
                                         Finally, we provide the first empirical performance evaluation of a gradual verifier, and found that on average,
                                         Gradual C0 decreases run-time overhead between 11-34% compared to the fully-dynamic approach used in
                                         prior work. Further, the worst-case scenarios for performance are predictable and avoidable. This work paves
                                         the way towards evaluating gradual verification at scale.
                                         CCS Concepts: • Theory of computation → Logic and verification; Automated reasoning; Hoare logic;
                                         Separation logic.

                                         1   INTRODUCTION
                                         Separation logic [Reynolds 2002] supports the modular static verification of heap-manipulating
                                         programs. Its variant Implicit dynamic frames (IDF) [Smans et al. 2009] and extension with recursive
                                         ∗ This material is based upon work supported by a Google PhD Fellowship award and the National Science Foundation under

                                         Grant Nos. CCF-1901033, DGE1745016, and DGE2140739. É. Tanter is partially funded by the ANID FONDECYT Regular
                                         Project 1190058 and the Millennium Science Initiative Program: code ICN17_002. Any opinions, findings, and conclusions
                                         or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the
                                         National Science Foundation, Google, ANID, or the Millennium Science Initiative.

                                         Authors’ addresses: Jenna DiVincenzo, Purdue University, USA, jennad@purdue.edu; Ian McCormack, Carnegie Mellon
                                         University, USA, icmccorm@cs.cmu.edu; Hemant Gouni, Carnegie Mellon University, USA, hsgouni@cs.cmu.edu; Jacob
                                         Gorenburg, Haverford College, USA, jgorenburg@haverford.edu; Jan-Paul Ramos-Dávila, Cornell University, USA, jvr34@
                                         cornell.edu; Mona Zhang, Columbia University, USA, mz2781@columbia.edu; Conrad Zimmerman, Brown University, USA,
                                         conrad_zimmerman@brown.edu; Joshua Sunshine, Carnegie Mellon University, USA, sunshine@cs.cmu.edu; Éric Tanter,
                                         University of Chile, Chile, etanter@dcc.uchile.cl; Jonathan Aldrich, Carnegie Mellon University, USA, jonathan.aldrich@cs.
                                         cmu.edu.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:2                                                                                                            Aldrich

abstract predicates [Parkinson and Bierman 2005; Smans et al. 2009] further support verifying
recursive heap data structures, such as trees, lists, and graphs. While these techniques allow users
to specify and verify more code than ever before, tools implementing them (e.g. Viper [Müller et al.
2016], VeriFast [Jacobs et al. 2011], Chalice [Leino et al. 2009], JStar [Distefano and Parkinson J
2008], and SmallFoot [Berdine et al. 2006]) are still largely unused due to the burden they place on
their users. Such tools poorly support partial specifications, and thus require users to provide a
number of auxiliary specifications (such as folds, unfolds, loop invariants, and inductive lemmas)
in an all or nothing fashion to support inductive proofs of correctness. The tools also require
many of these auxiliary specifications to be written before they can provide feedback on the
correctness of specifications for important functional properties. For example, to prove that a
simple insertion function preserves list acyclicity, static verifers need 1.5 times as many lines of
auxiliary specifications to program code (§2). They also need a significant number of these auxiliary
specifications to uncover problems with specifications of the acyclic property (§2).
   Inspired by gradual typing [Siek and Taha 2006], Bader et al. [2018] proposed gradual verification
to support the incremental specification and verification of software. Users can write imprecise (i.e.
partial) specifications backed by run-time checking where necessary. An imprecise formula can be
fully unknown, written ?, or combine a static part with the unknown, as in ? ∗ 𝑥 .𝑓 == 2. Wise et al.
[2020] extend Bader et al. [2018]’s initial system by designing and formalizing the first gradual
verifier for recursive heap data structures. It supports imprecise specifications with accessibility
predicates from IDF and abstract predicates; and thus, also (in theory) the run-time verification
of these constructs. During static verification, an imprecise specification can be optimistically
strengthened (in non-contradictory ways) by the verifier to support proof goals. Wherever such
strengthenings occur, dynamic checks are inserted to preserve soundness. Gradual verification
smoothly supports the spectrum between static and dynamic verification. This is captured by
properties adapted from gradual typing [Siek et al. 2015], namely the gradual guarantee, stating that
the verifier will not flag static or dynamic errors for specifications that are correct but imprecise,
and the fact that gradual verification conservatively extends static verification, i.e. they coincide on
fully-precise programs.
   While promising, Wise et al. [2020]’s gradual verifier has neither been implemented nor validated
in practice. Furthermore, their design relies on weakest liberal preconditions [Dijkstra 1975] for
static reasoning rather than symbolic execution [King 1976], which is the ideal reasoning technique
for tools based on separation logic or IDF. Indeed, Viper [Müller et al. 2016], VeriFast [Jacobs et al.
2011], JStar [Distefano and Parkinson J 2008], and SmallFoot [Berdine et al. 2006] all support these
permission logics with symbolic execution, not weakest liberal preconditions. Finally, Wise et al.
[2020]’s gradual verifier is not efficient in the sense that it checks all memory safety and functional
properties dynamically regardless of the precision of specifications.
   This paper presents the design, implementation, and validation of Gradual C01 —the first grad-
ual verifier for imperative programs manipulating recursive heap data structures that is based
on symbolic execution. Gradual C0 targets C0, a safe subset of C designed for education, with
appropriate support (and pedagogical material) for dynamic verification. Technically, Gradual C0 is
built on top of the Viper static verification infrastructure [Müller et al. 2016], which facilitates the
development of program verifiers supporting IDF and recursive abstract predicates. Gradual C0’s
back-end leverages this infrastructure to simplify the implementation of gradual verifiers for other
programming languages, and Gradual C0’s front-end demonstrates how this is done for C0. Further,
Gradual C0 minimizes the insertion of dynamic checks using statically available information and
optimizes the checks’ overhead at run time.

1 Gradual C0 is hosted on Github: https://github.com/gradual-verification/gvc0.
Gradual C0                                                                                               1:3


   Overall, we address new technical challenges in gradual verification related to symbolic execution,
extensibility to multiple programming languages, and minimizing run-time checks and their
overhead:
 • Gradual C0’s symbolic execution algorithm is responsible for statically verifying programs
    with imprecise specifications and producing minimized run-time checks. In particular, Gradual
    C0 tracks the branch conditions created by program statements and specifications to produce
    run-time checks for corresponding execution paths. At run time, branch conditions are assigned
    to variables at the branch point that introduced them, which are then used to coordinate the
    successive checks as required. Further, Gradual C0 creates run-time checks by translating
    symbolic expressions into specifications—reversing the symbolic execution process.
 • The run-time checks produced by Gradual C0 contain branch conditions, simple logical expres-
    sions, accessibility predicates, separating conjunctions, and predicates. Each of these constructs
    is specially translated into source code that can be executed at run time for dynamic verification.
    Logical expressions are turned into assertions. Accessibility predicates and separating conjunc-
    tions are checked by tracking and updating a set of owned heap locations. Finally, predicates are
    translated into recursive boolean functions. By encoding run-time checks into C0 source code,
    we avoid complexities from augmenting the C0 compiler to support dynamic verification. We
    also design these encodings to be performance friendly, e.g. owned heap locations are tracked
    in a dynamic hash table.
   Work on gradual typing performance has shown that minimizing the insertion of dynamic checks
does not trivially correlate with overall execution performance; the nature of the inserted checks
(such as higher-order function wrappers) as well as their location in the overall execution flow of a
program can have drastic and hard-to-predict consequences [Campora et al. 2018; Feltey et al. 2018;
Takikawa et al. 2016]. Therefore, our validation of Gradual C0 aims to empirically evaluate the
relationship between minimizing check insertion and observed run-time performance in gradual
verification. We evaluate the performance of Gradual C0 by adapting Takikawa et al. [2016]’s
performance lattice method to gradual verification, exploring the performance characteristics for
partial specifications of four common data structures. This method models the gradual verification
process as a series of steps of partial specifications from an unspecified program (containing all ?s)
to a statically verifiable specification (not containing any ?s) where, at each step, an atomic conjunct
is added to the current, partial specification. Statically, we observe that as more specifications are
added, more verification conditions can be statically discharged. Though imprecision introduces
unavoidable run-time checks, gradual verification decreases run-time overhead by an average
of 11-34% compared to dynamic verification (and thus Wise et al. [2020]’s approach). Sources
of run-time overhead correspond to the predictions made in prior work, and our study shows
that the gradual guarantee holds empirically for our tool across thousands of sampled imprecise
specifications.

2   GRADUAL C0 IMPROVES THE STATIC SPECIFICATION PROCESS
   Static verification tools, like Viper [Müller et al. 2016], VeriFast [Jacobs et al. 2011], Chalice [Leino
et al. 2009], JStar [Distefano and Parkinson J 2008], and SmallFoot [Berdine et al. 2006], require a
number of user-provided auxiliary specifications, such as folds, unfolds, lemmas, and loop invariants,
to prove properties about recursive heap data structures. Worse, they also require users to write
many of these auxiliary specifications before the tools can provide useful feedback on the correctness
of other specifications, including ones containing important functional properties. Therefore, users
are burdened by writing many detailed and extraneous specifications with inadequate static feedback
through the process. In this section, we illustrate this burden with a simple list insertion example
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:4                                                                                                            Aldrich

(inspired by a similar introductory example and discussion from Wise et al. [2020]) and output from
Viper. Then, we show in §3 how Gradual C0 overcomes this burden by smoothly supporting the
spectrum between static and dynamic checking. Users can avoid writing auxiliary specifications
and still get sound verification of their code with increased run-time checking. Users can also
receive run-time feedback on the correctness of their specifications very early in the specification
process, and the resulting error messages closely align with inherent problems in the specifications
or in the program, making debugging them easier.
                                                         Fig. 1 implements a linked list and function
  1  struct Node { int val ; struct Node * next ; }; that inserts a new node at the end of a given
  2  typedef struct Node Node ;
  3                                                  list, called insertLast, in C0 [Arnold 2010]. The
  4  Node * insertLast ( Node * list , int val )     insertLast function traverses the list to its end
  5 {                                                with a while loop starting from the root. That
  6       Node * y = list ;
  7       while (y -> next != NULL )                 is, insertLast implicitly assumes the list is non-
  8           { y = y -> next ; }                    empty (non-null) and acyclic; and that for mul-
  9       y -> next = alloc ( struct Node );         tiple successive calls to insertLast the list re-
10        y -> next -> val = val ;
11        y -> next -> next = NULL ;                 mains acyclic and non-empty after insertion.
12        return list ;                              These facts can be proven explicitly with static
13 }                                                 verification; the complete static specification is
       Fig. 1. Non-empty linked list insertion in C0 given in Fig. 2, highlighted in grey.
                                                         List acyclicity is specified with two predicates
                                                     acyclicSeg and acyclic:

predicate acyclicSeg(Node* s, Node* e) =
      s == e ? true : acc ( s->val) && acc ( s->next) && acyclicSeg(s->next, e)
predicate acyclic(Node* n) = acyclicSeg(Node* n, NULL)

The acyclicSeg predicate uses accessibility predicates and the separating conjunction from IDF.
Ownership is ensured through accessibility predicates such as acc ( s->val); and, acc ( s->val) &&
s->val == 2 states that s->val is uniquely owned and contains the value 2. The separating conjunc-
tion, denoted by &&,2 ensures memory disjointness: acc ( s->next) && acc ( s->next->next) states
that the heap locations s->next and s->next->next are distinct (i.e. 𝑠 ≠ s->next) and are each
owned.
   Thus, the abstract recursive predicate acyclicSeg, which can be thought of as a pure boolean
function, specifies that a list segment is acyclic. That is, acyclicSeg(s, e) denotes that all heap
locations in list s are distinct up to node e by recursively generating accessibility predicates for each
node in s up to e, joined with the separating conjunction. Further, acyclicSeg(n, NULL) denotes
that all heap locations in list n are distinct and so n is acyclic, as specified with acyclic(n).
   Now that we have specified acyclic, we use it in insertLast’s precondition (line 5) and postcon-
dition (lines 6-7) to denote preservation of list acyclicity. We also specify that insertLast preserves
list non-nullness with simple comparison logic (i.e. list != NULL and \result != NULL). Ideally, we
would stop here and static verifiers would be able to prove insertLast’s implementation is correct
with respect to this specification; however, as you can see in Fig. 2 such tools require many more
specifications. In fact, there are 27 lines of auxiliary specifications (comprised of folds, unfolds, loop
invariants, and inductive lemmas); in contrast to 18 lines of wanted specifications (the predicates
and pre- and postconditions) and program code. Furthermore, these auxiliary specifications are
complex, as discussed next.

2 Most IDF papers use ∗ to denote the separating conjuction. We follow Viper and use && instead.
Gradual C0                                                                                                                 1:5


 1    /*@ predicate acyclicSeg(Node* s, Node* e) =
 2             (s == e) ? true : acc(s->val) && acc(s->next) && acyclicSeg(s->next,e); @*/
 3    //@ predicate acyclic(Node* n) = acyclicSeg(n, NULL);

 4    Node * insertLast ( Node * list , int val )                 27             y - > next = alloc ( struct Node );
 5      // @ requires acyclic(list) && list != NULL ;             28             y - > next - > val = val ;
 6        /* @ ensures acyclic(\result) &&                        29             y - > next - > next = NULL ;
 7                                \result != NULL ; @ */          30              //@ fold acyclicSeg(y->next->next, NULL);
 8    {                                                           31              //@ fold acyclicSeg(y->next, NULL);
 9          //@ unfold acyclic(list);                             32              //@ fold acyclicSeg(y, NULL);
10         //@ unfold acyclicSeg(list, NULL);                     33              mergeLemma(list, y, NULL);
11         Node * y = list ;                                      34              //@ fold acyclic(list);
12         //@ fold acyclicSeg(list, y);                          35              return list ;
13         while (y -> next != NULL )                             36   }
14         /* @ loop_invariant acyclicSeg(list, y) &&             37
15                 acc(y->next) && acc(y->val) &&                 38    void mergeLemma (Node* a, Node* b, Node* c)
16                 acyclicSeg(y->next, NULL) ; @ */               39            //@ requires acyclicSeg(a, b) && acyclicSeg(b, c);
17         {                                                      40            //@ ensures acyclicSeg(a, c);
18             Node * tmp = y ;                                   41        {
19             y = y -> next ;
                                                                  42               if (a == b) {
20             //@ unfold acyclicSeg(y, NULL);
                                                                  43               } else {
21              //@ fold acyclicSeg(tmp->next, y);
                                                                  44                    //@ unfold acyclicSeg(a, b);
22              //@ fold acyclicSeg(tmp, y);
                                                                  45                    mergeLemma(a->next, b, c);
23              mergeLemma(list, tmp, y);
                                                                  46                    //@ fold acyclicSeg(a, c);
24         }
                                                                  47               }
25
26                                                                48    }

                                        □      Program code   ■    Static specification

                                   Fig. 2. The static verification of insertLast from Fig. 1

2.1       Auxiliary Specifications
Static verifiers cannot reliably unroll recursive predicates during verification; so, such tools rely
on explicit fold and unfold statements to control the availability of predicate information in the
verifier. This treats predicates iso-recursively; while an equi-recursive interpretation treats predicates
as their complete unrolling [Summers and Drossopoulou 2013]. Consequently, the acyclic and
acyclicSeg predicates are unfolded and folded often in Fig. 2 (lines 9-10, 12, 20-22, 30-32, and
34). Looking closely, we see that acyclic(list), which is assumed true from the precondition, is
unfolded on line 9. This consumes acyclic(list) and produces its body acyclicSeg(list, NULL),
which is subsequently unfolded on line 10. Then, at the fold on line 34, the body of acyclic(list)
is packed up into the predicate itself to prove the list remains acyclic after insertion.
   Additionally, static verifiers cannot tell if or when a loop will end (in our example the verifier
cannot tell when the list being iterated over ends), but must verify all paths through the program.
Therefore, static verifiers reason about loops using specifications called loop invariants, which are
properties that are preserved for each execution of the loop including at entry and exit. Further,
loop invariants must also provide information necessary for proof obligations after the loop, e.g.
that the list in insertLast is acyclic after insertion. In Fig. 2, these constraints result in the loop
invariant on lines 14-16 that segments the list into three disjoint and acyclic parts: from the root up
to the current node y (acyclicSeg(list, y)), the current node y (acc ( y->val) && acc ( y->next)),
and from the node after y to the end (acyclicSeg(y->next, NULL)). Exposing y via its accessibility
predicates provides access to y->next on line 19 in the loop body; and, acyclicSeg(list, y) helps
prove acyclic(list) holds after the loop, as we will see next.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:6                                                                                                            Aldrich

 1   Node * insertLast ( Node * list , int val )                    17           //@ unfold acyclicSeg(y, NULL);
 2     // @ requires acyclic(list) && list != NULL ;                18           //@ fold acyclicSeg(tmp->next, y);
 3       /* @ ensures acyclic(\result) &&                           19           //@ fold acyclicSeg(tmp, y);
 4                                  \result != NULL ; @ */          20           mergeLemma(list, tmp, y);
 5   {                                                              21       }
 6        //@ unfold acyclic(list);                                 22
 7        //@ unfold acyclicSeg(list, NULL);                        23       y - > next = alloc ( struct Node );
 8        Node * y = list ;                                         24       y - > next - > val = val ;
 9        //@ fold acyclicSeg(list, y);                             25       y - > next - > next = NULL ;
10        while (y -> next != NULL )                                26        //@ fold acyclicSeg(y->next->next, NULL);
11        /* @ loop_invariant acyclicSeg(list, y) &&                27       //@ fold acyclicSeg(y->next, NULL);
12                 acc(y->next)      && acc(y->val) &&              28       //@ fold acyclicSeg(y, NULL);
13                 acyclicSeg(y->next, NULL) ; @ */                 29       mergeLemma(list, y, NULL);
14        {                                                         30       //@ fold acyclic(list);
15             Node * tmp = y ;                                     31       return list ;
16             y = y -> next ;                                      32   }

     ■        1𝑠𝑡 increment (least precise)   ■    2𝑛𝑑 increment    ■    3𝑟𝑑 increment               ■   4𝑡ℎ increment
     ■        5𝑡ℎ increment                   ■    6𝑡ℎ increment    ■    7𝑡ℎ increment (full spec)

                                  Fig. 3. The incremental verification of insertLast from Fig. 1


   To prove acyclic(list) holds at the end of insertLast (line 35), it is sufficient to prove instead
that acyclicSeg(list, NULL) holds (line 34). After inserting a new node at the end of the list (lines
27-29), we can build up an inductive proof with folds (lines 30-32) that the list is acyclic from
the insertion point y to the new end, i.e. acyclicSeg(y, NULL) holds. We also have that the list is
acyclic from the root to y (acyclicSeg(list, y)) from to the loop invariant, and so, we are done
after proving transitivity of acyclic list segments, e.g. i.e. acyclicSeg(list, y) and acyclicSeg(y,
NULL) implies acyclicSeg(list, NULL). Sadly, static verifiers cannot automatically discharge such
inductive proofs, and so we specify the proof steps in mergeLemma on lines 38-48. Then, after using
the lemma on line 33, we achieve our proof goal.
   As we can see, not only do users of static verifiers need to write a number of auxiliary spec-
ifications in support of proof goals, the specifications are often more complex compared to the
program code itself even for simple examples like insertLast. Worse even, is that while users are
developing these complex specifications static tools provide limited feedback on their correctness
as demonstrated next (§2.2).

2.2 Lack of Early Specification Feedback
Since static verifiers, like Viper, limit themselves to reasoning about predicates iso-recursively
and rely on loop invariants to prove properties about loops, feedback on the correctness of
specifications early in the specification process is limited. For example, consider that a user
named Daisy incorrectly specifies the body of acyclicSeg (our recursive predicate) as (s == e) ?
acc ( s->val) && acc ( s->next) && acyclicSeg(s->next, e) : true, which swaps the branches of
the ternary in the correct specification from Fig. 2. Let’s see how Daisy comes across this error
while using Viper to incrementally specify insertLast in Fig. 3. Each increment from the first
to the last (seventh) is highlighted in a different color. The first increment, highlighted in green,
specifies the precondition and postcondition of insertLast with acyclic and acyclicSeg (lines 2-4).
Since predicates are black boxes in static verifiers, Viper only tells Daisy that there is insufficient
permission to access y->next in the loop condition on line 10. So, Daisy specifies the required
acc ( y->next) permission (as highlighted in purple for the second increment on line 12) in the loop
invariant, which must frame the loop condition. But, alas Viper cannot prove that acc ( y->next)
Gradual C0                                                                                          1:7


holds on entry to the loop. Without realizing the branches of acyclicSeg are out of order, Daisy
expects acyclicSeg(list, NULL)’s body to provide acc ( y->next) at loop entry as list != NULL and
y == list; and so, she unfolds acyclic(list) and acyclicSeg(list, NULL) on lines 6-7 making
up the third specification increment highlighted in pink. Unfortunately, Viper still reports that
acc ( y->next) does not hold on entry to the loop, which alerts Daisy to the problem with acyclicSeg.
   With Viper, Daisy required three specification increments to detect a bug in the first unfold-
ing of acyclicSeg, and this problem gets worse the deeper the bug is in the recursive predicate.
For example, consider now that acyclicSeg’s body is incorrectly specified as (s == e) ? true :
acc ( s->val) && acc ( s->next) && acyclicSeg(e, s->next), which swaps s->next and e in the
recursive call to acyclicSeg. As a result, acyclicSeg asserts in lock-step that the nodes in lists
s and e are accessible and separated—which is not the intended behavior of acyclicSeg—and
acyclicSeg now always fails when e reaches its end, i.e. is NULL, as it tries to assert acc ( e->val)
and acc ( e->next). It takes until the fourth specification increment highlighted in blue to discover
that acyclicSeg is incorrectly specified using Viper. As before, Daisy is led to specifying the first
three increments by Viper’s error messages that first require acc ( y->next) in the loop invariant
and then require acc ( y->next) to hold on entry to the loop. This time, however, acyclicSeg(list,
NULL)’s body contains acc ( y->next) when list != NULL, so Viper can prove acc ( y->next) holds
on loop entry and instead reports that the loop invariant acc ( y->next) might not be preserved
by the loop body. Daisy recalls the loop iterates over all nodes in the list with the current node
being y, so preserving acc ( y->next) in the loop is the same as showing that Viper has accessibility
predicates for every node in the list. As a result, she specifies the fourth increment (lines 12-13 and
17), which continuously unfolds the acyclicSeg(list, NULL) predicate on every iteration of the
loop and captures the information in its body in the loop invariant. Alas, Viper reports that the
new loop invariant does not hold on entry as it cannot prove acyclicSeg(y->next, NULL) holds
here. Since this information should come from unfolding acyclicSeg(list, NULL) on line 7, Daisy
takes another look at acyclicSeg’s body and discovers her specification error. That is, it takes four
specification increments for Daisy to realize her mistake and the fourth increment required her to
think deeply about her while loop.
   Clearly, static verifiers burden their users, like Daisy, by requiring them to write a number of
complex auxiliary specifications both for proofs and to receive useful feedback on the correctness
of their specifications. Fortunately, as we will show next in §3, Gradual C0 overcomes this burden
by smoothly supporting the spectrum between static and dynamic checking.

3     GRADUAL C0 TO THE RESCUE
In this section, we show how Gradual C0’s ability to smoothly integrate static and dynamic checking
allows users to overcome specification burdens inherent to static verification, e.g. that users have
to write complex auxiliary specifications in support of proofs and to receive useful feedback on the
correctness of their specifications.

3.1    Ignore Auxiliary Specifications with Gradual C0
In §2.1, we saw how static verifiers force users to write complex auxiliary specifications (like
folds and unfolds, loop invariants, and inductive lemmas) in support of proof goals. In contrast,
Gradual C0 allows users to write as many or as few auxiliary specifications as they want, and
instead utilizes dynamic verification to check proof obligations not discharged statically due
to missing specifications. For example, consider Fig. 3, in which our user Daisy incrementally
specifies insertLast for preservation of list acyclicity and non-nullness. With Gradual C0, Daisy
only needs to specify the first increment in green, which contains the pre- and postcondition of
insertLast on lines 2-4. She can completely avoid specifying the auxiliary specifications in the rest
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:8                                                                                                            Aldrich

of the increments by instead specifying ? in the loop invariant on line 10. Then, Gradual C0 uses
the allocation statement on line 23 to statically validate the write accesses of y->next->val and
y->next->next on lines 24-25. It can also prove statically that the list after insertion is non-null. All
other proof obligations, which ensure memory safety of the while loop and the list after insertion
is acyclic, are checked dynamically.
   Run-time checking memory safety of the while loop involves three parts: 1) verifying access to
y->next in the loop condition (line 10), 2) verifying access to y->next in the loop body (line 16), and
3) verifying access to y->next in the alloc statement directly after the loop (line 23). That is, Gradual
C0 asserts ownership of all heap locations in the given list, which are being iterated over by the
loop. Consequently, the larger the list the higher the run-time cost of verification for insertLast.
This cost is unacceptable to Daisy, so she statically specifies memory safety of the while loop in the
first four increments in Fig. 3 (lines 2-4, 6-7, 12-13, and 17). The new loop invariant (lines 12-13)
uses acyclicSeg to expose acc ( y->next) for verifying access to y->next in the loop condition, loop
body, and after the loop. The unfolds on lines 6-7 and 17 are used to prove that the loop invariant is
preserved by the loop given the precondition on line 2. After all this work, Daisy is not interested in
also statically specifying the list after insertion is acyclic, and so, she joins ? with her newly specified
loop invariant. As a result, Gradual C0 now additionally checks memory safety of the while loop
statically reducing run-time cost, and only checks acyclic(\result) from the postcondition of
insertLast (line 3) dynamically (i.e. the list returned after insertion is acyclic). By allowing Gradual
C0 to check acyclic(\result) dynamically, Daisy saved herself a lot of specification effort. She
avoided building up acyclicSeg from the previous end of the list to the new one (increment five in
orange, lines 26-28), specifying a more complex loop invariant (increment six in red, lines 9, 11,
and 18-19), and stating and proving transitivity of acyclic list segments (increment seven in yellow,
lines 20 and 29). Daisy is very happy to make this human-effort vs run-time cost trade-off.

3.2   Gradual C0 Provides Earlier Feedback with Run-Time Checks
As we saw in §2.2, static verifiers struggle to provide early feedback on specification errors in
predicates. Using Viper, it took until the third specification increment in Fig. 3 for Daisy to
discover the simple error in acyclicSeg’s body, (s == e) ? acc ( s->val) && acc ( s->next) &&
acyclicSeg(s->next, e) : true, which swaps the branches of the ternary in the correct specification
from Fig. 2. In contrast, with Gradual C0, Daisy easily discovers this error on the first specifica-
tion increment (in green, lines 2-4), which specifies the pre- and postcondition of insertLast.
She additionally specifies ? on the loop invariant and provides a simple test case that calls
insertLast on a list with one node. Then, Gradual C0 alerts Daisy to the error in acyclicSeg
by reporting at run time that acc ( s->val) from acyclicSeg does not hold at the end of the list
where s == NULL. Clearly, acc ( s->val) will never hold when s == NULL, so Daisy realizes she
swapped the branches in acyclicSeg. Similarly, the second example of an error in acyclicSeg’s
specification, which swaps s->next and e in the recursive call to acyclicSeg ((s == e) ? true :
acc ( s->val) && acc ( s->next) && acyclicSeg(e, s->next)), took four specification increments
in Fig. 3 to be exposed by Viper. Again with Gradual C0, Daisy can detect the error by the first
increment as long as she specifies ? on her loop invariant and supplies a simple test case with a
list containing two elements. In this case, Gradual C0 reports at run time that acc ( s->val) from
acyclicSeg does not hold for s which is NULL. Since acc ( s->val) will never hold when s == NULL,
Daisy takes another look at acyclicSeg’s body and realizes her error. That is, Gradual C0’s dynamic
checking of partial specifications is helpful for detecting errors in recursive predicates much earlier
in the specification process than static verification alone and the errors better capture the inherent
problems in the specifications.
Gradual C0                                                                                             1:9


   To summarize, users of Gradual C0 may write as many or as little auxiliary specifications as they
want and still get sound verification of their code by trading off between human-effort and run-time
cost. Users can also receive feedback on the correctness of their specifications much earlier in the
specification process than if they used static verification alone and the run-time errors reported
often closely match the inherent problems with the specification.

4   GRADUAL C0’S DESIGN AND IMPLEMENTATION
                                                  Gradual C0 is a working gradual verifier for the C0
                                                  programming language [Arnold 2010] that is built
                                                  as extension of the Viper static verifier [Müller et al.
                                                  2016]. Our goals for the design and implementation
                                                  of Gradual C0 are to:
                                                       • be easily extensible to other programming
                                                         languages beyond C0,
                                                       • minimize run-time overhead from verifica-
                                                         tion as much as possible without introduc-
                                                         ing highly complex algorithms, and
        Fig. 4. System design of Gradual C0            • use symbolic execution for static reasoning.
                                                    Consequently, we settled on the design illustrated
in Fig. 4. Gradual C0 is structured in two major sub-systems: 1) the gradual verification pipeline
and 2) the C0 pipeline. Within the gradual verification pipeline, a C0 program is first translated
AST-to-AST into a Gradual Viper program by Gradual C0’s frontend module, GVC0. The GVC0
module implements a simple parser, abstract syntax, and type checker for C0 programs to facilitate
the translation. The Gradual Viper module is the backend of Gradual C0 and implements its own
parser, abstract syntax, and type checker for its own imperative language called the Gradual Viper
language. This language is the Viper language plus imprecise formulas and allows Gradual Viper
to support multiple frontend languages, not just C0. We chose to build a C0 frontend first because
C0 is a pedagogical version of C designed with dynamic verification in mind, and we plan to use it
in the classroom.
   Once the C0 program is translated into a Gradual Viper program, it is optimistically statically
verified by the Gradual Viper module. Gradual Viper extends Viper’s symbolic execution based
verifier to support imprecise formulas and resulting holes in static reasoning as inspired by Wise et al.
[2020] and gradual typing [Herman et al. 2010; Siek and Taha 2006; Siek et al. 2015]. Consequently,
by construction Gradual Viper supports full static verification of programs when specifications
are complete. Differing from Wise et al. [2020]’s work, Gradual Viper also extends the symbolic
execution algorithm to create a description of needed run-time checks in support of static holes.
The run-time checks are minimized with statically available information during reasoning. Finally,
GVC0 takes these run-time checks and encodes them in the original C0 program to produce a
sound, gradually-verified program. The C0 pipeline takes this C0 program and feeds it to the C0
compiler, CC0, which is used to execute the program. Note, the encoding of checks into C0 source
code optimizes for run-time performance and simplifies extending C0 with dynamic verification in
our domain.
   The rest of this section describes the implementation of Gradual Viper and GVC0’s designs in
more detail and illustrates the concepts via example. We also highlight design and implementation
choices influenced by our goals. §4.1 discusses how C0 programs are translated to Gradual Viper
programs, along with modifications made to both C0 and Viper for gradual verification. Then,
§4.2 and §4.3 detail Gradual Viper’s symbolic execution approach and how it produces minimized
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:10                                                                                                           Aldrich

  𝑥 ∈ VAR                                (variables)                  𝑆 ∈ STRUCTNAME                               (struct names)
  𝑣 ∈ VAL                                   (values)                  𝑓 ∈ FIELDNAME                                 (field names)
  𝑒 ∈ EXPR                             (expressions)                  𝑝 ∈ PREDNAME                              (predicate names)
  𝑠 ∈ STMT                              (statements)                  𝑚 ∈ METHODNAME                               (method names)
 𝑜𝑝 ∈ +, -, /, *, ==, !=, <=, >=, <, >   (operators)

                                            Fig. 5. Shared abstract syntax definitions
      P         ::= 𝑠𝑡𝑟𝑢𝑐𝑡 𝑝𝑟𝑒𝑑𝑖𝑐𝑎𝑡𝑒 𝑚𝑒𝑡ℎ𝑜𝑑                               P     ::= field 𝑝𝑟𝑒𝑑𝑖𝑐𝑎𝑡𝑒 𝑚𝑒𝑡ℎ𝑜𝑑
  𝑠𝑡𝑟𝑢𝑐𝑡 ::= struct 𝑆 { 𝑇 𝑓 }                                           field   ::= field 𝑓 : 𝑇
 𝑝𝑟𝑒𝑑𝑖𝑐𝑎𝑡𝑒 ::= //@predicate 𝑝 (𝑇 𝑥 ) = 𝜙e                             predicate ::= predicate 𝑝 (𝑥 : 𝑇 ) { 𝜙e }
  𝑚𝑒𝑡ℎ𝑜𝑑 ::= 𝑇˜ 𝑚 (𝑇 𝑥 ) 𝑐𝑜𝑛𝑡𝑟𝑎𝑐𝑡 { 𝑠 }                               method ::= method 𝑚 (𝑥 : 𝑇 ) returns (𝑦 : 𝑇 )
 𝑐𝑜𝑛𝑡𝑟𝑎𝑐𝑡 ::= //@requires 𝜙;e //@ensures 𝜙; e                                      contract { 𝑠 }
    𝑇      ::= struct 𝑆 | int | bool | char | 𝑇 ∗                     contract ::= requires 𝜙e ensures 𝜙e
    𝑇˜     ::= void | 𝑇                                                  𝑇      ::= Int | Bool | Ref
     𝑠     ::= 𝑠; 𝑠 | 𝑇 𝑥 | 𝑇 𝑥 = 𝑒 | 𝑥 = 𝑒                              𝑠      ::= 𝑠 ; 𝑠 | var 𝑥 : 𝑇 | 𝑥 := 𝑒
              | 𝑙 = 𝑒 | 𝑒 | assert (𝑒 ) | //@assert 𝜙                             | 𝑥 . 𝑓 := 𝑒 | 𝑥 := new (𝑓 )
                 | //@fold 𝑝 (𝑒˜ ) | //@unfold 𝑝 (𝑒˜ )                             | 𝑥 := 𝑚 (𝑒 ) | assert 𝜙
                 | if (𝑒 ) { 𝑠 } else { 𝑠 }                                        | fold acc (𝑝 (𝑒 ) ) | unfold acc (𝑝 (𝑒 ) )
                 | while (𝑒 ) //@loop_invariant 𝜙e { 𝑠 }                           | if (𝑒 ) { 𝑠 } else { 𝑠 }
                | for (𝑠; 𝑒; 𝑠 ) //@loop_invariant 𝜙e { 𝑠 }                        | while (𝑒 ) invariant 𝜙e { 𝑠 }
                                                                          𝑒     ::= 𝑣 | 𝑥 | 𝑜𝑝 (𝑒 ) | 𝑒 . 𝑓
      𝑒         ::= 𝑣 | 𝑥 | 𝑜𝑝 (𝑒 ) | 𝑒 -> 𝑓 | ∗𝑒 | 𝑚 (𝑒 )               𝑥      ::= result | 𝑖𝑑
                 | alloc (𝑇 ) | 𝑒 ? 𝑒 : 𝑒                                 𝑣     ::= 𝑛 | null | true | false
       𝑒˜       ::= 𝑣 | 𝑥 | 𝑜𝑝 (𝑒˜ ) | 𝑒˜ -> 𝑓 | *𝑒˜                     𝜙e     ::= ? && 𝜙 | 𝜃
       𝑙        ::= 𝑥 -> 𝑓 | *𝑥 | 𝑙 -> 𝑓 | *𝑙                            𝜃      ::= self-framed 𝜙
                                                                         𝜙      ::= 𝑒 | acc (𝑝 (𝑒 ) ) | acc (𝑒.𝑓 ) | 𝜙 && 𝜙
      𝑥         ::= \result | 𝑖𝑑
                                                                                   | 𝑒 ? 𝜙 : 𝜙
       𝑣        ::= 𝑛 | 𝑐 | NULL | true | false
      𝜙e        ::= ? && 𝜙 | 𝜃                                                  Fig. 7. Gradual Viper abstract syntax
      𝜃         ::= self-framed 𝜙
      𝜙         ::= 𝑒˜ | 𝑝 (𝑒˜ ) | acc (𝑙 ) | 𝜙 && 𝜙
                   | 𝑒˜ ? 𝜙 : 𝜙

                 Fig. 6. GVC0 abstract syntax
                  Representation differs slightly in GVC0 vs.           Functionality in GVC0 that requires non-
            ■                                                     ■
                  Gradual Viper                                         trivial translation to Gradual Viper

                                Fig. 8. Abstract syntax comparison for GVC0 and Gradual Viper


run-time checks. Finally, §4.4 focuses on how GVC0 turns run-time checks from Gradual Viper
into C0 code for dynamic verification.

4.1    Translating C0 Source Code to Gradual Viper Source Code for Verification
The C0 language, with its minimal set of language features and its existing support for specifications,
serves well as the target language for our implementation. As its name suggests, C0 borrows heavily
from C, but its feature set is reduced to better suit its intended purpose as a tool in computer science
education [Arnold 2010]. It is a memory-safe subset of C that forbids casts, pointer arithmetic, and
pointers to stack-allocated memory. All pointers are created with heap allocation, and de-allocation
is handled by a garbage collector.
   The abstract syntax for C0 programs supported by Gradual C0 is given in Fig. 6, i.e. GVC0’s
abstract syntax. GVC0 programs are made of struct and method declarations that largely follow C
syntax. What differs from both C and C0 is GVC0’s specification language. Methods may specify
constraints on their input and output values as side-effect-free gradual formulas 𝜙,       e usually in
//@requires or //@ensures clauses in the method header. Loops and abstract predicates contain
invariants and bodies respectively that are made of gradual formulas. Such formulas 𝜙e are imprecise
Gradual C0                                                                                      1:11


formulas ? && 𝜙 or complete boolean formulas 𝜙 (Note, in this case, 𝜙 must be self-framed as
defined in IDF). A formula 𝜙 joins boolean values, boolean operators, predicate instances, acces-
sibility predicates, and conditionals via the separating conjunction && . GVC0 programs also
contain //@fold p(𝑒) ˜ and //@unfold p(𝑒)  ˜ statements for predicates and //@assert 𝜙 statements
for convenience.
   To support the gradual verification of many different imperative programming languages, Gradual
Viper verifies programs written in its own custom imperative language, which is designed to ease
the translation from other imperative languages into it. The Gradual Viper language’s abstract
syntax is given in Fig. 7. The GVC0 and Gradual Viper languages are roughly 1-to-1, including their
specification languages, so translation is mostly straightforward, but there are some differences
as highlighted in yellow (trivial) and blue (non-trivial) in Fig. 8. For example, for loops in GVC0
are rewritten as while loops in Gradual Viper, and alloc(struct T) expressions are translated to
new statements containing struct T’s fields. Additionally, GVC0 allows method calls, allocs, and
ternaries in arbitrary expressions, while Gradual Viper only allows such constructs in corresponding
program statements3 . Therefore, GVC0 uses fresh temporary variables to version expressions
containing the aformentioned constructs into program statements in Gradual Viper. The temporary
variables are then used in the original expression in place of the corresponding method call, alloc,
or ternary. Nested field assignments, such as x->y->z = a, are similarly expanded into multiple
program statements using temporary variables. Value type pointers in GVC0 are rewritten as
pointers to single-value structs that can be easily translated into Gradual Viper syntax. Finally,
assert(𝑒) statements are essentially ignored in Gradual Viper; 𝑒 is translated into Gradual Viper
syntax to verify its heap accesses, but 𝑒 is not asserted. Instead, the assert is always kept in the
original C0 program and is checked exclusively at run time. Fig. 9 provides a simple example
program written in both the GVC0 language (Fig. 9a) and Gradual Viper language (Fig. 9b) for
reference.
   Note that GVC0 does not support array and string values since gradually verifying any interesting
properties about such constructs requires non-trivial extensions to current gradual verification
theory. Similarly, the Gradual Viper language, in contrast to the Viper language, does not support
the aforementioned constructs and fractional permissions.

4.2    Gradual Viper: Symbolic Execution for Gradual Verification
In this section, we describe the design and implementation of Gradual Viper’s symbolic execution
based algorithm supporting the static verification of imprecise formulas. Gradual verification of
recursive heap data structures was formalized with weakest liberal preconditions [Wise et al. 2020].
All of the static verifiers supporting separation logic or IDF—such as Viper [Müller et al. 2016],
VeriFast [Jacobs et al. 2011], JStar [Distefano and Parkinson J 2008], and SmallFoot [Berdine et al.
2006]—reason with symbolic execution. Therefore, this work serves as a first guide for building
gradual verifiers from static verifiers using symbolic execution for reasoning. Additionally, unlike
in Wise et al. [2020]’s work, we use our static reasoning algorithm not just for optimistic static
verification but also for soundly reducing the number of run-time checks required during dynamic
verification. That is, during a single execution of Gradual Viper a program is statically verified
and a set of minimized run-time checks is produced for program points where the algorithm is
optimistic during verification due to imprecision.
   Before formalizing Gradual Viper’s implementation in §4.3, we first demonstrate at a high-level
with examples how symbolic execution is used to perform optimistic static verification of programs
containing recursive heap data structures and how minimized run-time checks are produced during
3 Note, ternaries correspond to if statements
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:12                                                                                                           Aldrich

this process. We also point out novel technical challenges faced and solutions developed thanks to
relying on symbolic execution both for static verification and minimizing run-time checks.
4.2.1 Optimistic static verification in Gradual Viper by example. The simple program given
in Fig. 9b implements a withdraw function (method), which subtracts the balance in one bank
account (the subtrahend) from the balance in another account (the minuend) returning the result.4
Any client program of withdraw must ensure the subtrahend’s balance is less than or equal to the
minuend’s balance and that both balances are positive as specified by withdraw’s precondition
(line 11). Then, withdraw will return an account with a positive balance as specified by withdraw’s
postcondition (lines 12-13). Additionally, withdraw’s postcondition ensures the subtrahend’s balance
remains positive as well. Note, the withdraw example is contrived to better illustrate how Gradual
Viper works and its interesting aspects.
   Well-formedness of user written specifications. Gradual Viper begins static verification by first
checking user written specifications, like predicate bodies, preconditions, and postconditions, for
well-formedness. That is, user specifications must be self-framed and cannot contain duplicate
accessibility predicates or predicates joined by the separating conjunction &&. Self-framing from
IDF [Smans et al. 2009] simply means that a formula must contain accessibility predicates for any
heap locations accessed in the formula. In gradual verification [Wise et al. 2020], ? can represent
these accessibility predicates. For example, in the withdraw program geqTo’s body (lines 4-5) is
self-framed, because ? can represent acc ( a1.balance) and acc ( a2.balance) to frame a1.balance
and a2.balance. On the other hand, positive’s body (line 7) is classically self-framed as it explicitly
contains acc ( a.balance) to frame a.balance. All of the user written formulas, which are geqTo’s
body (lines 4-5), positive’s body (line 7), withdraw’s precondition (line 11), and its postcondition
(lines 12-13), are well-formed.
   Next, Gradual Viper optimistically statically verifies each function in the given program, e.g.
the withdraw function in our running example. This involves symbolically executing the function
from top to bottom and tracking information in a symbolic state. Information is gathered from the
execution of both specifications and code, and proof obligations are established by the symbolic
state. If any obligations are established optimistically, corresponding run-time checks are stored
in the symbolic state. Fig. 9c displays the contents of the symbolic state at every program point
(marked by program lines) during the verification of withdraw. In general, a symbolic state can
be thought of as writing an intermediate logical formula in a special form. We will discuss the
contents of a symbolic state in more detail as we work through the withdraw example.
   Producing a precondition. At the start of withdraw (lines 14-15), information in the precondition,
e.g. geqTo(a1,a2), is produced or translated into an empty symbolic state resulting in the first state in
the table in Fig. 9c. As with formulas, symbolic states may be imprecise or not, meaning information
may be missing from the state due to imprecision. In fact, you can think of an imprecise symbolic
state as representing an imprecise intermediate formula. Here, the precondition geqTo(a1,a2) is
precise,5 so the state also remains precise. Had the precondition been imprecise, then the state
would also become imprecise. Local variables are mapped to symbolic values in a symbolic, variable
store. Since a1 and a2 are arguments to withdraw and res the return value, they are all assigned
fresh symbolic values t1, t2, and t3 respectively in the store. Then, permissions like accessibility
4 Note, we refer to the version of the withdraw program written in the Gradual Viper language rather than its Gradual C0

counterpart in Fig. 9a as we will be discussing how Gradual Viper works in this section.
5 Note, precision in a static context as in Gradual Viper means the formula does not contain ? at the top-level. Predicates are

treated as black-boxes, so even if their bodies are imprecise, as with geqTo(a1,a2), a formula containing them, such as
geqTo(a1,a2), can be precise.
Gradual C0                                                                                                                                        1:13


      1       struct Account { int balance ; };                                   1    field balance : Int
      2       typedef struct Account Account ;                                    2
      3       /*@ predicate geqTo(Account* a1, Account* a2) =                     3    predicate geqTo(a1: Ref, a2: Ref)
      4           ? && a1->balance >= a2->balance &&                              4            { ? && a1.balance >= a2.balance &&
      5           a2->balance >= 0; @*/                                           5            a2.balance >= 0 }
      6       /*@ predicate positive(Account* a) =                                6    predicate positive(a: Ref)
    7             acc(a->balance) && a->balance >= 0; @*/         7                            { acc(a.balance) && a.balance >= 0 }
    8                                                             8
    9         Account * withdraw ( Account * a1 , Account * a2 ) 9                     method withdraw ( a1 : Ref , a2 : Ref )
   10           // @ requires geqTo(a1,a2) ;                     10                    returns ( res : Ref )
   11           // @ ensures ? && positive(a2) &&                11                      requires acc(geqTo(a1,a2))
   12                               positive(\result) ;                         12         ensures ? && acc(positive(a2)) &&
   13         {                                                                 13                          acc(positive(res))
   14             //@ unfold geqTo(a1,a2);                                      14     {
   15             if ( a1 == NULL || a2 == NULL ) {                             15         unfold acc(geqTo(a1,a2))
   16               return a1 ;                                                 16         if ( a1 == null || a2 == null ) {
   17             } else {                                                      17           res := a1
   18               int newB = a1 - > balance - a2 - > balance ;                18         } else {
   19               a1 -> balance = newB ;                                      19           var newB : Int = a1 . balance - a2 . balance
   20               //@ fold positive(a1);                                      20           a1 . balance := newB
   21                 //@ fold positive(a2);                                    21           fold acc(positive(a1))
   22                 return a1 ;                                               22                  fold acc(positive(a2))
   23             }                                                             23                  res := a1
   24         }                                                                 24         }
   25                                                                           25     }

  (a) A simple bank withdraw example written in the Grad-                       (b) A simple bank withdraw program written in the
  ual C0 language                                                               Gradual Viper language

                                □    Program code        ■    Static specification         ■        Imprecise specification

 Ln       Impr-        Opt. Heap              Heap                 Var Store                    Path Condition              Run-time Checks
          ecise
 14-      No           ∅                      geqTo(t1,t2)         a1→t1 ; a2→t2 ;              ∅                           ∅
 15                                                                res→t3
 15-      Yes          acc(t1,balance,p1) ;   ∅                    a1→t1 ; a2→t2 ;              t1 != null ; t2 != null ;   ∅
 16                    acc(t2,balance,p2)                          res→t3                       p1 >= p2 ; p2 >= 0
 16-      -            -                      -                    -                            -                           -
 17
 17-      -            -                      -                    -                            -                           -
 18
 18-      Yes          acc(t1,balance,p1) ;   ∅                    a1→t1 ; a2→t2 ;              t1 != null ; t2 != null ;   ∅
 19                    acc(t2,balance,p2)                          res→t3                       p1 >= p2 ; p2 >= 0
 19-      Yes          acc(t1,balance,p1) ;   ∅                    a1→t1 ; a2→t2 ;              t1 != null ; t2 != null     ∅
 20                    acc(t2,balance,p2)                          res→t3 ; newB→t4             ; p1 >= p2 ; p2 >= 0 ;
                                                                                                t4 = p1 - p2
 20-      Yes          ∅                      acc(t1,balance,p3)   a1→t1 ; a2→t2 ;              t1 != null ; t2 != null     ∅
 21                                                                res→t3 ; newB→t4             ; p1 >= p2 ; p2 >= 0 ;
                                                                                                t4 = p1 - p2 ; p3 = t4
 21-      Yes          ∅                      positive(t1)         a1→t1 ; a2→t2 ;              t1 != null ; t2 != null     ∅
 22                                                                res→t3 ; newB→t4             ; p1 >= p2 ; p2 >= 0 ;
                                                                                                t4 = p1 - p2 ; p3 = t4
 22-      Yes          ∅                      positive(t2)         a1→t1 ; a2→t2 ;                                    𝑙𝑏𝑐 , ¬(a1 = null || a2 = null)
                                                                                                t1 != null ; t2 != null
 23                                                                res→t3 ; newB→t4             ; p1 >= p2 ; p2 >= 0 ;−→ 𝑙𝑐1 , acc(a2.balance) ;
                                                                                                t4 = p1 - p2 ; p3 = t4𝑙𝑏𝑐 , ¬(a1 = null || a2 = null)
                                                                                                                      −→ 𝑙𝑐2 , a2.balance >= 0
 23-      Yes        ∅                       positive(t2)             a1→t1 ; a2→t2 ; t1 != null ; t2 != null 𝑙𝑏𝑐 , ¬(a1 = null || a2 = null)
 24                                                                   res→t3 ; newB→t4 ; p1 >= p2 ; p2 >= 0 ; −→ 𝑙𝑐1 , acc(a2.balance) ;
                                                                                            t4 = p1 - p2 ; p3 = t4 ; 𝑙𝑏𝑐 , ¬(a1 = null || a2 = null)
                                                                                            t3 = t1                   −→ 𝑙𝑐2 , a2.balance >= 0
 24       𝑙𝑏𝑐 , ¬(a1 = null || a2 = null) −→ 𝑙𝑐1 , acc(a2.balance) ; 𝑙𝑏𝑐 , ¬(a1 = null || a2 = null) −→ 𝑙𝑐2 , a2.balance >= 0 ;
          𝑙𝑏𝑐 , ¬(a1 = null || a2 = null) −→ 𝑙𝑐3 , acc(positive(res))

(c) Contents of the symbolic state at each program point during Gradual Viper’s static verification of withdraw in Fig. 9b
Fig. 9. A gradually verified, bank withdraw program that is contrived to illustrate how Gradual Viper works
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:14                                                                                                           Aldrich

predicates and predicates can be stored in a symbolic heap (either the optimistic heap or heap)
in terms of the symbolic values. We call symbolic versions of permissions heap chunks. Since
geqTo(a1,a2) is concretely known it is added directly to the heap as the heap chunk geqTo(t1,t2).
An important invariant of the heap is that permissions in it are guaranteed to be separated in
memory, i.e. when they are joined by the separating conjunction they return true. The optimistic
heap contains heap chunks for accessibility predicates that are optimistically assumed during
verification and is introduced in this work to reduce the number of run-time checks produced by
Gradual Viper. We will see how this works as we continue to discuss the withdraw example. For
now, the optimistic heap is empty. Similarly, both the path condition and set of run-time checks
both remain empty. The path condition contains constraints on symbolic values that have been
collected on the current verification path. The precondition geqTo(t1,t2) only contains permission
information, so the path condition is empty. Further, producing a formula into the symbolic state
does not introduce any run-time checks.
   Unfolding a predicate. Next, Gradual Viper executes the unfold statement on line 15 causing the
predicate geqTo(a1,a2) to be consumed and then its body to be produced into the state on lines
15-16. In general, consuming a formula 1) checks whether the formula is established by the symbolic
state, 2) generates minimized run-time checks for the state to establish the formula soundly, and 3)
removes permissions asserted in the formula from the symbolic state. That is, consume is Gradual
Viper’s mechanism for checking proof obligations; and as we will see, is used a few different times
throughout the verification of withdraw. Here, since geqTo(t1,t2) is in the heap, geqTo(a1,a2) is
established by the symbolic state and no run-time checks are required. It is then removed from the
heap as it is “consumed". After consumption, geqTo(a1,a2)’s body (lines 4-5) is produced into the
current state (the one without geqTo(t1,t2)). The body of geqTo is imprecise, so the symbolic state
is made imprecise (as seen in Fig. 9c at lines 15-16). The rest of geqTo’s body is a boolean expression
constraining a1 and a2’s account balances: a1’s balance is greater than or equal to a2’s balance and
a2’s balance is positive. Before adding these constraints to the path condition, Gradual Viper first
looks for heap chunks in the current symbolic state corresponding to accessibility predicates that
frame a1.balance and a2.balance in geqTo’s body. Both the heap and optimistic heap are empty,
but the state is imprecise so the missing heap chunks are optimistically assumed to be in the
state. In fact, it is sound to make this assumption without any run-time checks, because we are
producing (rather than consuming) the predicate body. As a result, fresh symbolic values p1 and p2
for a1.balance and a2.balance respectively are generated and used to record constraints on the
balances in the path condition. Gradual Viper also records that the receivers a1 and a2 are non-null
in the path condition, because Gradual Viper assumed they can be safely de-referenced. Finally,
Gradual Viper adds heap chunks acc ( t1,balance,p1) and acc ( t2,balance,p2) to the optimistic
heap to 1) record the mappings of locations to their values and 2) avoid producing run-time checks
for the accessibility predicates later in the program. These heap chunks are added to the optimistic
heap rather than the heap, because getTo’s body does not specify whether or not a1 (t1) or a2 (t2)
alias. So adding them to the heap would break the heap’s invariant. The optimistic heap, however,
does not maintain any invariants. It is also convenient to store optimistic heap chunks in their own
heap signaling that they are available due to optimism in the verification. The final symbolic state
after consuming geqTo(a1,a2) and producing its body is given in Fig. 9c lines 15-16.
  Branching. After the unfold on line 15, Gradual Viper reaches the start of the if statement on
the following line 16. As is common with static verifiers based on symbolic execution, Gradual
Viper’s execution branches at if statements. Execution also branches at other conditioned points,
such as logical conditionals and loops. Gradual Viper analyzes the then branch (lines 16-18) under
the assumption the condition a1 == null|| a2 == null is true, and the else branch (lines 18-24)
Gradual C0                                                                                          1:15


under the assumption a1 == null || a2 == null is false. These assumptions are added to the path
condition for each execution path respectively. However, in our example the symbolic state going
into the if statement (Fig. 9c lines 15-16) states that both a1 and a2 are non-null. So the then branch
is infeasible, and Gradual Viper prunes this execution path resulting in the blank symbolic states in
Fig. 9c from lines 16-18. Both accounts being non-null means the else branch condition for sure
holds and so execution proceeds down this branch without any changes to the symbolic state. That
is, for withdraw to be statically verified, this one execution path must successfully verify. If Gradual
Viper executed both branches, then determining verification success is a bit more complicated:
 • If the current symbolic state is precise, then both execution paths must successfully verify. This
     is the default functionality in static verifiers.
 • If the current symbolic state is imprecise, then verification succeeds when one or both paths
     successfully verify. When only one path succeeds and the state is imprecise, Gradual Viper
     optimistically assumes the state contains information that forces program execution down the
     success path only at run time. This more permissive static functionality is critical for adhering
     to the gradual guarantee at branch points. To ensure the program will never actually execute the
     failing branch (i.e., to ensure soundness), Gradual Viper adds a run-time check for the success
     path’s condition at the branch point.

   Variable assignment. Let’s look now at how Gradual Viper verifies the else branch (lines 18-24).
At the variable assignment on line 19, Gradual Viper first evaluates the right-hand expression to
the symbolic value p1 - p2. To do this, Gradual Viper first looks for heap chunks for a1.balance
and a2.balance in the current symbolic heaps (Fig. 9c lines 18-19) to both frame the locations and
get their values. Both heap chunks are in the optimistic heap, so no run-time checks are required
for framing and p1 and p2 are used in the evaluation of the right-hand expression. Note, if Gradual
Viper did not add the aforementioned heap chunks to the optimistic heap when producing the body
of geqTo(a1,a2), then Gradual Viper would create run-time checks for them here in the program.
However, these checks would be duplicates, because Gradual Viper also checks that these heap
chunks are available when ensuring the precondition getTo(a1,a2) holds in client contexts at calls
to withdraw. So sound tracking of heap chunks in an optimistic heap has helped us avoid duplicating
run-time checks! Finally, Gradual Viper adds a new mapping to the variable store for newB and its
fresh symbolic value t4; and then, adds the constraint t4 = p1 - p2 to the path condition to record
information from the assignment in the symbolic state (Fig. 9c lines 19-20).

   Field assignment. Next, a1.balance is assigned newB’s value in the field assignment on line 20.
Gradual Viper mimics this behavior symbolically by first pulling newB’s value t4 from the symbolic
state (Fig. 9c lines 19-20). Then, Gradual Viper looks for a1.balance’s heap chunk in the state
for framing, and if there, removes the chunk as a1.balance’s value may change in the write, i.e.
acc ( a1.balance) is consumed. Gradual Viper also asserts that a1 is non-null. The heap chunk for
a1.balance is in the optimistic heap and a1 != NULL is in the path condition, so no run-time checks
are needed here. Then, a1.balance’s heap chunk is removed from the state; and, unfortunately,
this action causes a2.balance’s heap chunk to be removed from the state as well. Gradual Viper
does not know whether or not a1 and a2 alias, because this information does not appear in the
current path condition and the optimistic heap does not maintain the separation invariant. Then,
since the state is imprecise Gradual Viper could assume that a1.balance and a2.balance refer to
the same heap location, i.e. a1 and a2 are aliased. In this case, removing a1.balance’s heap chunk
requires also removing a2.balance’s heap chunk as a2.balance may have also changed with the
write. On the other hand, the case where they do not alias and a2.balance’s heap chunk can stay in
the optimistic heap is also possible from Gradual Viper’s perspective. To simply and soundly cover
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:16                                                                                                           Aldrich

both cases Gradual Viper removes a2.balance’s heap chunk by default when alias information is
unknown. As we will see next, this comes at the cost of additional run-time checks later in the
verification of withdraw. Finally, Gradual Viper produces a new heap chunk for a1.balance into the
state to track its new, fresh symbolic value p3 after the write and updates the path condition with
the assignment information p3 = t4 (Fig. 9c lines 20-21).

   Folding a predicate. After a1.balance is assigned a new balance, Gradual Viper executes the
fold statement on line 21. Folding a predicate is similar to unfolding a predicate except that the
functionality is reversed: positive(a1)’s body is consumed from the current state (Fig. 9c lines 20-21)
and then positive(a1) is produced into the state after consumption (Fig. 9c lines 21-22). The body of
positive(a1) is acc ( a1.balance) && a1.balance >= 0, so acc ( a1.balance) is consumed first then
a1.balance >= 0 second. The heap chunk acc ( t1,balance,p3) corresponding to acc ( a1.balance)
is in the heap and a1 != null holds in the path condition, so no run-time check is required for
consuming acc ( a1.balance). Then, a1.balance’s heap chunk is removed from the heap as seen
in Fig. 9c lines 21-22. Next, the boolean expression a1.balance >= 0 is evaluated to its symbolic
value p3 >= 0. Recall that to do this, Gradual Viper must look up a heap chunk for a1.balance in
the symbolic state to both frame the heap location and get its value. However, Gradual Viper just
removed this heap chunk from the current state due to the left-to-right execution of consume. To
solve this issue, Gradual Viper looks for framing and value information in the state before the fold,
i.e. the state before consumption at lines 20-21 in Fig. 9c. As we know, a1.balance’s heap chunk
is in this state and maps a1.balance to the value p3, so no run-time check is needed for framing.
Then, p3 >= 0 is asserted against the current path condition. Since p1 >= p2 >= 0 and p3 = t4 =
p1 - p2 are in the path condition, p3 is clearly greater than or equal to 0 and is proven directly
by the path condition. That is, no run-time check is needed for p3 >= 0. Finally, positive(a1) is
produced into the current state, which adds positive(t1) to the heap resulting in the final version
of the state in Fig. 9c lines 21-22.
   Next, Gradual Viper executes the second fold statement on line 22 with the aforementioned
state. This fold statement consumes positive(a2)’s body and then produces positive(a2) into the
state. So as before, Gradual Viper first consumes acc ( a2.balance) and then a2.balance >= 0. The
receiver a2 is proved to be non-null by the path condition; however this time, the heap chunk for
acc ( a2.balance) is not in either of the heaps. Fortunately for us, the state is imprecise and can opti-
mistically contain this heap chunk, so a run-time check is produced for acc ( a2.balance) as seen in
the state after folding positive(a2) in Fig. 9c lines 22-23. Since this run-time check occurs down the
else branch of the if statement in withdraw, branch information, e.g. 𝑙𝑏𝑐 , ¬(a1 = null || a2 = null),
is included with the check. The location 𝑙𝑏𝑐 specifies where the branch point originated in the pro-
gram, e.g. line 16, and ¬(a1 = null || a2 = null) is the assumption made at the branch point for
the current execution path. Additionally, 𝑙𝑐1 contains the location where the check itself is required
in the program, e.g. line 22. While it does not happen in the withdraw example, sometimes different
checks are required at the same program point down different execution paths. So, Gradual Viper
attaches branch information for the entire execution path to each run-time check to allow GVC0
(or other frontends) to apply checks only on the execution path they are required. This ensures
soundness and reduces run-time checking. Now, Gradual Viper removes acc ( a2.balance) from the
current state (Fig. 9c lines 21-22), which actually causes positive(t1) to be removed from the heap
as well. Predicates are treated as black boxes in Gradual Viper; so unless told otherwise, Gradual
Viper conservatively assumes acc ( a2.balance) is in positive(t1) and removes positive(t1) from
the heap alongside acc ( a2.balance). The only way Gradual Viper can guarantee acc ( a2.balance)
is not in positive(t1) is if a heap chunk for a2.balance and positive(t1) both exist in the heap,
as the heap maintains the separation invariant. In this case, positive(t1) can remain in the heap
Gradual C0                                                                                         1:17


while only acc ( a2.balance) is removed. Of course, in our example the heap chunk for a2.balance
is definitely not in the heap, so postive(t1) is removed.
   Continuing, Gradual Viper consumes a2.balance >= 0, which first looks for a heap hunk to frame
a2.balance in the state before the consume (Fig. 9c lines 21-22). However, neither of the heaps
contain a heap chunk for a2.balance. As before, Gradual Viper uses imprecision to optimistically
assume the heap chunk is in the state and produces a run-time check for acc ( a2.balance). Since this
run-time check for the same location already exists in the state, the two checks are condensed into
the first one. Then, Gradual Viper returns a fresh symbolic value for a2.balance, say p4, to evaluate
a2.balance >= 0 down to p4 >= 0. Note, Gradual Viper can only return a fresh value here, because
the heaps do not contain a heap chunk recording a2.balance’s value in the state. Unfortunately,
this means Gradual Viper cannot prove a2.balance >= 0 holds as no constraints exist for p4 in the
path condition. But, this also means p4 >= 0 does not contradict existing information in the path
condition. So, imprecision in the state can optimistically represent p4 >= 0 and a run-time check
for a2.balance >= 0 is generated as seen in Fig. 9c lines 22-23. A few things of note here:
 • Run-time checks are originally computed in terms of symbolic values, e.g. p4 >= 0, but are
    ultimately replaced with counterparts written in terms of program variables, e.g. a2.balance >=
    0. This replacement by the translate function in Gradual Viper simplifies the implementation of
    run-time checks for frontends like GVC0, which operate on program variables and concrete
    values not symbolic values. The translate function uses mappings in the symbolic heaps and
    store to reverse the symbolic execution. Special considerations are made for fresh symbolic
    values like p4, aliasing between object values, and different variable contexts.
 • On another note, if consuming acc ( a1.balance) at the field assignment on line 20 did not also
    consume the heap chunk for a2.balance, then the run-time checks for acc ( a2.balance) and
    a2.balance >= 0 would not be necessary. Gradual Viper conservatively assumed a1 and a2 were
    aliased at the consume, so it removed both chunks from the state. However, in practice a1 and
    a2 are likely to be distinct objects; and in fact, folding positive(a1) then positive(a2) is a good
    sign the developer of withdraw expects a1 and a2 to be distinct. In this case, a2.balance’s heap
    chunk does not need to be removed making the aforementioned run-time checks unnecessary.
    Unfortunately, since we designed Gradual Viper to be conservative for simplicity, these run-time
    checks are only eliminated when the developer explicitly specifies that a1 and a2 are not aliased,
    such as in the precondition of withdraw. So, we are trading more optimal run-time checks for
    simplicity in our consume algorithm.
 • While it does not happen here in our withdraw example, there may be times where parts
    of a symbolic, boolean expression are proven statically and the rest optimistically. In this
    case, Gradual Viper re-writes the expression into conjunctive normal form and computes the
    conjuncts in this form that cannot be proven statically by the path condition. These conjuncts
    (after translation) will then be checked at run time. We call this process computing the difference
    between the expression and the path condition, and it results in minimized run-time checks
    given statically available information.
Finally, a heap chunk for positive(a2) (e.g. positive(t2)) is produced into the heap resulting in
the final form of the state in Fig. 9c lines 22-23.

   Return value assignment. Then, Gradual Viper reaches the variable assignment on line 23, which
assigns a1 to res—the return value of withdraw. Gradual Viper first looks up the symbolic value
t1 for a1 and then the symbolic value t3 for res in the variable store. Gradual Viper stores the
information t3 = t1 from the assignment in the path condition resulting in the next symbolic state
in Fig. 9c lines 23-24.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:18                                                                                                           Aldrich

   Consuming a postcondition. Finally, Gradual Viper reaches the end of withdraw down its one and
only execution path on line 24. So the last thing Gradual Viper must do to verify the function, is
to consume the postcondition ? && acc ( positive(a2)) && acc ( positive(res)) (lines 12-13) in the
current symbolic state (Fig. 9c lines 23-24). Gradual Viper begins by first consuming positive(a2)
then positive(res). The heap chunk for positive(a2) is in the heap, so no run-time check is
needed for it. Then positive(t2) is removed from the heap leaving both symbolic heaps empty. As
a result (and because the state is imprecise), consuming positive(res) in the next step results in a
run-time check for the predicate as seen in the final set of run-time checks required for withdraw
given in Fig. 9c line 24. Note, consuming acc ( positive(a2)) && acc ( positive(res)) requires both
consuming the predicates individually (which we’ve done) and ensuring that one predicate does not
access heap locations overlapping with the other (in adherence with the separating conjunction &&).
Unfortunately, the state does not contain enough information to prove this fact statically, e.g. only
the heap chunk for positive(a2) appears in the heap, but the state is imprecise! So when Gradual
Viper optimistically assumes positive(res) holds, it also assumes positive(res) is separated
from positive(a2). Gradual Viper flags positive(res)’s run-time check with this additional check
for GVC0 to handle. Additionally, after consuming the static part of an imprecise formula, e.g.
acc ( positive(a2)) && acc ( positive(res)) in withdraw’s postcondition, Gradual Viper makes the
state imprecise and empties both symbolic heaps. The ? in the imprecise formula can represent any
permission available in the state, so they must be removed by consume.

  Takeaways. To summarize, Gradual Viper statically verifies the withdraw function successfully,
and produces run-time checks for acc ( a2.balance) before line 20, a2.balance >= 0 also before line
20, and positive(res) at the end of withdraw (line 24). The withdraw function will be completely
verified if these checks succeed at run time. During our discussion of the withdraw function, we
highlighted a number of technical challenges addressed and solutions developed related to designing
and implementing Gradual Viper. One of our goals was for Gradual Viper to minimize run-time
checks as much as possible without using highly complex algorithms. For this we introduced the
optimistic heap, which tracks heap chunks that are optimistically assumed during static verification
and can be soundly used to reduce run-time checking in successive program statements from
where they originated. In withdraw, we saw the heap chunks for a1.balance and a2.balance, which
were added to the optimistic heap during the production of geqTo(a1,a2)’s body (line 15), be
used to eliminate duplicate run-time checks at the assignment on line 19. We had to make careful
considerations for the separating conjunction and removal of heap chunks at consumes to ensure
sound tracking of heap chunks in the optimistic heap. We also defined and implemented the
diff function, which utilizes conjunctive normal form to optimize run-time checks for boolean
expressions. Finally, Gradual Viper conservatively removes heap chunks from the symbolic heaps
that may alias with other heap chunks removed at a consume. We saw in withdraw that this comes at
the cost of additional run-time checks: consuming a1.balance’s heap chunk at the field assignment
on line 20 also consumed a2.balance’s heap chunk resulting in run-time checks for acc ( a2.balance)
and a2.balance >= 0 before line 20. That is, we are trading more optimal run-time checks for
simplicity in our consume algorithm.
  Another goal for Gradual Viper, is for it to use symbolic execution for static reasoning. We
accomplished this goal, but not without dealing with some technical challenges. Symbolic execution
based static verifiers generate and discharge proof obligations written in terms of symbolic values,
causing Gradual Viper, which extends this system, to follow suit. As a result, Gradual Viper naturally
generates run-time checks written in terms of symbolic values as well. Unfortunately, dynamic
verifiers only operate on program variables and concrete values not symbolic ones. To bridge this
gap between the static and dynamic systems, we implemented a translate function in Gradual Viper
Gradual C0                                                                                            1:19


that re-writes run-time checks containing symbolic values to ones containing program variables
and concrete values while being careful about aliases. Finally, execution splitting at branch points
led to some trickiness in gradual verification. Different run-time checks may appear at the same
program point along different execution paths, so we augmented Gradual Viper to attach branching
information to run-time checks. We also augmented Gradual Viper to be more optimistic about
verification success when dealing with failing execution paths in the presence of imprecision. This
was done in compliance with the gradual guarantee [Wise et al. 2020].

4.3   Gradual Viper: Implemented Algorithm
In this section, we formalize the symbolic execution algorithm implemented by Gradual Viper. A
high-level description of how it works is given in §4.2. Our algorithm extends Viper’s symbolic
execution algorithm, and so Gradual Viper’s design is heavily influenced by Müller et al. [2016]’s
work. Like Viper, Gradual Viper’s algorithm consists of 4 major functions: eval, produce, consume,
and exec. The functions evaluate expressions, produce (inhale) and consume (exhale) formulas, and
execute program statements respectively. Following Viper’s lead, our 4 functions are defined in
continuation-passing style, where the last argument of each of the aforementioned functions is a
continuation 𝑄. The continuation is a function that represents the remaining symbolic execution
that still needs to be performed. Note that the last continuation returns a boolean (𝜆 _ . success()
or 𝜆 _ . failure()), indicating whether or not symbolic execution was successful.
   The rest of this section is outlined as follows. Run-time checks and the collections that hold
them are described in §4.3.1. We define symbolic states in §4.3.2 and preliminaries in §4.3.3. Finally,
the 4 major functions of our algorithm are given in their own sections: eval §4.3.4, produce §4.3.5,
consume §4.3.6, and exec §4.3.7. Throughout this section, we make clear where Viper has been
extended to support imprecise formulas with yellow highlighting in figures. We also use blue
highlighting to indicate extensions for run-time check generation and collection.

4.3.1 Run-time checks. Run-time checks produced by Gradual Viper are collected in the ℜ set. A
run-time check is a 4-tuple ( bcs𝑐 , origin𝑐 , location𝑐 , 𝜙𝑐 ), where bcs𝑐 is a set of branch conditions,
origin𝑐 and location𝑐 denote where the run-time check is required in the program, and 𝜙𝑐 is what
must be checked. A branch condition in bcs𝑐 is also a tuple of ( origin𝑒 , location𝑒 , 𝑒), where
origin𝑒 and location𝑒 define the program location at which Gradual Viper’s execution branches
on the condition 𝑒. A location is the AST element in the program where the branch or check
occurs, denoted as a formula 𝜙𝑙 . Sometimes, the condition being checked is defined elsewhere in
the program (e.g. in the precondition of a method) but we need to relate it to the method being
verified. The origin is used to do this. It is none when the condition is in the method being verified;
otherwise, it contains a method call, fold, unfold, or special loop statement from the method
being verified that referenced the check specified in the location. An example run-time check is:
({( none, 𝑥 > 2, ¬(𝑥 > 2))}, 𝑧 := 𝑚 (𝑦 ), acc (𝑦.𝑓 ), acc (𝑦.𝑓 )). The check is for accessing 𝑦.𝑓 , and
it is required for 𝑚’s precondition element acc (𝑦.𝑓 ) at the method call statement 𝑧 := 𝑚 (𝑦 ). The
check is only required when ¬(𝑥 > 2), which is evaluated at the program point where the AST
element 𝑥 > 2 exists. Since ¬(𝑥 > 2)’s origin is none, it comes from an if or assert statement.
    Further, R is used to collect run-time checks down a particular execution path in Gradual Viper.
R is a 3-tuple ( bcs𝑝 , origin𝑝 , rcs𝑝 ) where bcs𝑝 is the set of branch conditions collected down
the execution path 𝑝, origin𝑝 is the current origin that is set and reset during execution, and
rcs is the set of run-time checks collected down 𝑝. Two auxiliary functions are used to modify
R: addcheck and addbc. The addcheck function takes an R collection R𝑎𝑟𝑔 , a location 𝜙𝑙 for a
check, and the check itself, and returns a copy of R𝑎𝑟𝑔 with the run-time check added to R𝑎𝑟𝑔 .rcs.
If necessary, addcheck uses R𝑎𝑟𝑔 .origin and substitution to ensure 𝜙𝑙 and the check refer to the
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:20                                                                                                           Aldrich

correct context. For example, let 𝜙𝑙 and check 𝜙𝑐 come from asserting a precondition for 𝑧 := 𝑚 (𝑦 ).
Then, addcheck performs the substitutions: 𝜙𝑙 [𝑡 ↦→ 𝑚𝑎𝑟𝑔 ] (precondition declaration context) and
𝜙𝑐 [𝑡 ↦→ 𝑦] (method call context) where 𝑡 is the symbolic value for 𝑦. The addbc function operates
similarly to addcheck but for branch conditions.
4.3.2 Symbolic State. We use 𝜎 ∈ Σ to denote a symbolic state, which is a 6-tuple
( isImprecise, ℎ ?, ℎ, 𝛾, 𝜋, R) consisting of a boolean isImprecise, a symbolic heap ℎ ? , another
symbolic heap ℎ, a symbolic store 𝛾, a path condition 𝜋, and a collection R (defined in §4.3.1). The
boolean isImprecise records whether or not the state is imprecise, the symbolic store 𝛾 maps local
variables to their symbolic values, and the path condition 𝜋 (defined in §4.3.3) contains constraints
on symbolic values that have been collected on the current verification path.
   A symbolic heap is a multiset of heap chunks for fields or predicates that are currently accessible.
A field chunk 𝑖𝑑 (𝑟 ; 𝛿 ) (representing expression 𝑟 .𝑖𝑑) consists of the field name 𝑖𝑑, the receiver’s
symbolic value 𝑟 , and the field’s symbolic value 𝛿—also referred to as the snapshot of a heap chunk.
For a predicate chunk 𝑖𝑑 (𝑎𝑟𝑔𝑠; 𝛿 ), 𝑖𝑑 is the predicate name, 𝑎𝑟𝑔𝑠 is a list of symbolic values that are
arguments to the predicate, and 𝛿 is the snapshot of the predicate. A predicate’s snapshot represents
the values of the heap locations abstracted over by the predicate. The symbolic, optimistic heap
ℎ ? contains heap chunks that are accessible due to optimism in the symbolic execution, while ℎ
contains heap chunks that are statically accessible. Further, only ℎ maintains the invariant that
its heap chunks are separated in memory, and thus, can be joined successfully by the separating
conjunction. The empty symbolic state is
𝜎0 = ( isImprecise := false, ℎ ? := ∅, ℎ := ∅, 𝛾 := ∅, 𝜋 := ∅, R := (∅, none, ∅)).
4.3.3 Preliminaries. We introduce a few preliminary definitions here that will be helpful later. A
path condition 𝜋 is a stack of tuples (𝑖𝑑, 𝑏𝑐, 𝑝𝑐𝑠). An 𝑖𝑑 is a unique identifier that determines the
constraints on symbolic values that have been collected between two branch points in execution.
The 𝑏𝑐 entry is the symbolic value for the branch condition from the first of two branch points, and
𝑝𝑐𝑠 is the set of constraints that have been collected. Branch points can be from if statements and
logical conditionals in formulas. Functions pc-all, pc-add, and pc-push manipulate path conditions
and are formally defined in Appendix Fig. 21. The pc-all function collects and returns all the
constraints in 𝜋, pc-add adds a new constraint to 𝜋, and pc-push adds a new stack entry to 𝜋.
Similarly, snapshots for heap chunks have their own related functions: unit, pair, first, and second.
The constant unit is the empty snapshot, pair constructs pairs of snapshots, and first and second
deconstruct pairs of snapshots into their sub-parts. Further, fresh is used to create fresh snapshots,
symbolic values, and other identifiers depending on the context. The havoc function similarly
updates a symbolic store by assigning a fresh symbolic value to each variable in a given collection
of variables. Finally, check(𝜋, 𝑡 ) = pc-all(𝜋 ) ⇒ 𝑡 queries the underlying SAT solver to see if the
given constraint 𝑡 is valid in a given path condition 𝜋 (i.e. 𝜋 proves or implies 𝑡).
4.3.4 Symbolic execution of expressions. The symbolic execution of expressions by the eval
function is defined in Fig. 10. Using the current symbolic state, eval evaluates an expression to
a symbolic value 𝑡 and returns 𝑡 and the current state to the continuation 𝑄. Variable values are
looked up in the symbolic store and returned. For 𝑜𝑝 (𝑒), its arguments 𝑒 are each evaluated to
their symbolic values 𝑡. A symbolic value 𝑜𝑝 ′ (𝑡) is then created and returned with the state after
evaluation. Each 𝑜𝑝 has a corresponding symbolic value 𝑜𝑝 ′ of the same arity. For example, 𝑒 1 + 𝑒 2
results in the symbolic value 𝑎𝑑𝑑 (𝑡 1, 𝑡 2 ) where 𝑒 1 and 𝑒 2 evaluate to 𝑡 1 and 𝑡 2 respectively.
   Finally, the most interesting rule is for fields 𝑒.𝑓 . The receiver 𝑒 is first evaluated to 𝑡 resulting in a
new state 𝜎2 . Then, eval looks for a heap chunk for 𝑡 .𝑓 first in the current heap ℎ.6 If a chunk exists,
6 Heap lookup in eval also looks for heap chunks that are aliases (according to the path condition) to the chunk in question.
Gradual C0                                                                                                                         1:21


      eval(𝜎, 𝑡, 𝑄 )          = 𝑄 (𝜎, 𝑡 )
      eval(𝜎, 𝑥, 𝑄 )          = 𝑄 (𝜎, 𝜎 .𝛾 (𝑥 ) )
      eval(𝜎1 , 𝑜𝑝 (𝑒 ), 𝑄 ) = eval(𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . 𝑄 (𝜎2 , 𝑜𝑝 ′ (𝑡 ) ) ) )
      eval(𝜎1 , 𝑒.𝑓 , 𝑄 )     = eval(𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .
                               if (∃ 𝑓 (𝑟 ; 𝛿 ) ∈ 𝜎2 .ℎ . check(𝜎2 .𝜋, 𝑟 = 𝑡 ) ) then
                                  𝑄 (𝜎2 , 𝛿 )
                                else if (∃ 𝑓 (𝑟 ; 𝛿 ) ∈ 𝜎2 .ℎ ? . check(𝜎2 .𝜋, 𝑟 = 𝑡 ) ) then

                                   𝑄 (𝜎2 , 𝛿 )

                                else if (𝜎2 .isImprecise ) then

                                   𝑟𝑒𝑠, _ := assert(𝜎2 .isImprecise, 𝜎2 .𝜋, 𝑡 ≠ null)
                                   𝑒𝑡 := translate (𝜎2 , 𝑡 )

                                   R ′ := addcheck (𝜎2 .R, 𝑒.𝑓 , acc (𝑒𝑡 .𝑓 ) )

                                   𝛿 := fresh

                                   𝑟𝑒𝑠 ∧ 𝑄 (𝜎2 {ℎ ? := 𝜎2 .ℎ ? ∪ 𝑓 (𝑡 ; 𝛿 ), 𝜋 := pc-add(𝜎2 .𝜋, {𝑡 ≠ null } ),   R := R ′ }, 𝛿 )
                               else failure())

                     ■      Handles imprecision        ■       Handles run-time check generation and collection

                                       Fig. 10. Rules for symbolically executing expressions


then the heap read succeeds and 𝜎2 and the chunk’s snapshot 𝛿 is returned to the continuation. If a
chunk does not exist in ℎ, then eval looks for a chunk in the optimistic heap ℎ ? , and if found the
chunk’s snapshot is returned with 𝜎2 . If a heap chunk for 𝑡 .𝑓 is not found in either heap, then the
heap read can still succeed when 𝜎2 is imprecise. As long as 𝑡 ≠ null does not contradict the current
path condition 𝜎2 .𝜋 (the call to assert, Appendix Fig. 28), 𝜎2 ’s imprecision optimistically provides
access to 𝑡 .𝑓 . Therefore, a run-time check for acc (𝑒𝑡 .𝑓 ) is created and added to 𝜎2 ’s set of run-time
checks (highlighted in blue). Note that 𝑒𝑡 .𝑓 is used in the check rather than 𝑡 .𝑓 , because—unlike 𝑡
which is a symbolic value—the expression 𝑒𝑡 can be evaluated at run time. Specifically, translate
(described in Appendix Fig. 25) is called on 𝑡 with the current state 𝜎2 to compute 𝑒𝑡 . Additionally,
the AST element 𝑒.𝑓 is used to denote the check’s location.
   Afterwards, a fresh snapshot 𝛿 is created for 𝑡 .𝑓 ’s value, and a heap chunk 𝑓 (𝑡; 𝛿 ) for 𝑡 .𝑓 and 𝛿
is created and added to 𝜎2 ’s optimistic heap passed to the continuation. Similarly, the constraint
𝑡 ≠ null is added to 𝜎2 ’s path condition. By adding 𝑓 (𝑡; 𝛿 ) to the optimistic heap, the following
accesses of 𝑡 .𝑓 are statically verified by the optimistic heap, which reduces the number of run-time
checks produced. Finally, verification of the heap read for 𝑡 .𝑓 fails when none of the aforementioned
cases are true. Fig. 22 and Fig. 23 in the Appendix define variants of eval, called eval-p and eval-
c, that are used in produce and consume respectively. The eval-p variant does not introduce
run-time checks and eval-c does not extend the optimistic heap and path condition, because the
aforementioned functionalities are not needed in these contexts.

4.3.5 Symbolic production of formulas. Produce (Fig. 11) is responsible for adding information
to the symbolic state, in particular, the path condition and the heap ℎ. Producing an imprecise
formula makes the symbolic state imprecise. The produce rule for an expression 𝑒 evaluates 𝑒
to its symbolic value and produces it into the path condition. The produce rules for accessibility
predicates containing fields and predicates are similar, so we focus on the rule for fields only.
The field 𝑒.𝑓 in acc (𝑒.𝑓 ) first has its receiver 𝑒 evaluated to a symbolic value 𝑡. Then, using the
parameter 𝛿 a fresh heap chunk 𝑓 (𝑡; 𝛿 ) is created and added to the heap before invoking the
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:22                                                                                                           Aldrich

produce(𝜎, ? && 𝜙, 𝛿, 𝑄 )            = produce(𝜎 { isImprecise := true }, 𝜙, second(𝛿 ), 𝑄 )
produce(𝜎1 , 𝑒, 𝛿, 𝑄 )               = eval-p (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . 𝑄 (𝜎2 {𝜋 := pc-add(𝜎2 .𝜋, {𝑡, 𝛿 = 𝑢𝑛𝑖𝑡 } ) } ) ) )
produce(𝜎1 , acc (𝑝 (𝑒 ) ), 𝛿, 𝑄 )   = eval-p (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . 𝑄 (𝜎2 {ℎ := 𝜎2 .ℎ ⊎ 𝑝 (𝑡 ; 𝛿 ) } ) ) )
produce(𝜎1 , acc (𝑒.𝑓 ), 𝛿, 𝑄 )      = eval-p (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .
                                      𝑄 (𝜎2 {ℎ := 𝜎2 .ℎ ⊎ 𝑓 (𝑡 ; 𝛿 ), 𝜋 := pc-add(𝜎2 .𝜋, {𝑡 ≠ null } ) } ) ) )
produce(𝜎1 , 𝜙 1 && 𝜙 2 , 𝛿, 𝑄 )     = produce(𝜎1 , 𝜙 1 , first(𝛿 ), (𝜆 𝜎2 . produce(𝜎2 , 𝜙 2 , second(𝛿 ), 𝑄 ) ) )
produce(𝜎1 , 𝑒 ? 𝜙 1 : 𝜙 2 , 𝛿, 𝑄 ) = eval-p (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .

                                       branch (𝜎2 , 𝑒, 𝑡, (𝜆 𝜎3 . produce(𝜎3 , 𝜙 1 , 𝛿, 𝑄 ) ), (𝜆 𝜎3 . produce(𝜎3 , 𝜙 2 , 𝛿, 𝑄 ) ) ) ) )

                     ■    Handles imprecision        ■     Handles run-time check generation and collection

                                       Fig. 11. Rules for symbolically producing formulas

continuation. Note, the disjoint union ⊎ ensures 𝑓 (𝑡; 𝛿 ) is not already in the heap before 𝑓 (𝑡; 𝛿 ) is
added; otherwise, verification fails. Further, acc (𝑒.𝑓 ) implies 𝑒 ≠ null and so that fact is recorded
in the path condition as 𝑡 ≠ null. When the separating conjunction 𝜙 1 && 𝜙 2 is produced, 𝜙 1 is first
produced into the symbolic state, followed by 𝜙 2 . Finally, to produce a conditional, Gradual Viper
branches on the symbolic value 𝑡 for the condition 𝑒 splitting execution along two different paths.
Along one path 𝜙 1 is produced into the state under the assumption that 𝑡 is true, and along the
other path 𝜙 2 is produced under the ¬𝑡 assumption. Both paths follow the continuation to the end
of its execution, and a branch condition corresponding to the 𝑡 assumption made is added to the
symbolic state. Paths are pruned when they are infeasible (the assumption about 𝑡 would contradict
the current path conditions). Overall verification success is computed from the results of the two
execution paths, and an imprecise state allows this computation to be optimistic when one path
successfully verifies and the other doesn’t. In this case, branch optimistically marks verification a
success when normally it should fail, because the state may optimistically contain information that
prunes the failure case. A run-time check is then added for the success path’s condition to ensure
soundness. This functionality is important for adhering to the gradual guarantee [Wise et al. 2020].
The formal definition of branch is in Fig. 12, and other details for branch and produce are given in
Appendix §A.2. Note, produce only adds run-time checks for branching to the symbolic state.
4.3.6 Symbolic consumption of formulas. The goals of consume are 3-fold: 1) given a symbolic
state 𝜎 and formula 𝜙,  e check whether 𝜙e is established by 𝜎, i.e. 𝜙e𝜎 ⇒
                                                                         f 𝜙e where 𝜙e𝜎 is the formula
which represents the state 𝜎, 2) produce and collect run-time checks that are minimally sufficient
for 𝜎 to establish 𝜙e soundly, and 3) remove accessibility predicates and predicates that are asserted
in 𝜙e from 𝜎. The rules for consume are given in full and described in great detail in Appendix §A.3.
We give select rules in Fig. 13 and an abstract description here.
   The functionality of consume is split across two functions: consume, which is the interface
to consume accepting only a state, formula, and continuation, and consume’, which is a helper
function performing consume’s major functionality. Note, before calling consume’, consume first
adds non-alias information from the heap to the path condition and checks that the heap and path
condition are non-contradictory using consolidate [Schwerhoff 2016].
   Then, the two functions work together to accomplish the aforementioned goals. For the first and
second goals, heap chunks representing accessibility predicates and predicates in 𝜙e are looked up
in the heap ℎ and optimistic heap ℎ ? from 𝜎. When 𝜎 is precise, the heap chunks must be in ℎ or
verification fails. If 𝜎 is imprecise, then the heap chunks are always justified either by the heaps
or imprecision. Run-time checks for heap chunks that are verified by imprecision are collected
in 𝜎.R. The consume’ rule for acc (𝑒.𝑓 ) (and the rule for acc (𝑝 (𝑒)) which is similar) supports this
Gradual C0                                                                                                       1:23


               branch(𝜎, 𝑒, 𝑡, 𝑄 𝑡 , 𝑄 ¬𝑡 ) =

                 (𝜋𝑇 , R𝑇 ) := ( pc-push(𝜎 .𝜋, fresh, 𝑡 ), addbc (𝜎 .R, 𝑒, 𝑒 ) )
                 (𝜋 𝐹 , R 𝐹 ) := ( pc-push(𝜎 .𝜋, fresh, ¬𝑡 ), addbc (𝜎 .R, 𝑒, ¬𝑒 ) )
                    if (𝜎 .isImprecise ) then

                      𝑟𝑒𝑠𝑇 := ( if ¬check(𝜎 .𝜋, ¬𝑡 ) then 𝑄𝑡 (𝜎 {𝜋 := 𝜋𝑇 ,        R := R𝑇 } ) else failure() )

                      𝑟𝑒𝑠 𝐹 := ( if ¬check(𝜎 .𝜋, 𝑡 ) then 𝑄 ¬𝑡 (𝜎 {𝜋 := 𝜋𝐹 ,     R := R 𝐹 } ) else failure() )

                      if ( (𝑟𝑒𝑠𝑇 ∧ ¬𝑟𝑒𝑠 𝐹 ) ∨ (¬𝑟𝑒𝑠𝑇 ∧ 𝑟𝑒𝑠 𝐹 ) ) then

                           R ′ := addcheck (𝜎 .R, 𝑒, ( if (𝑟𝑒𝑠𝑇 ) then 𝑒 else ¬𝑒 ) )

                           ℜ := ℜ ∪ R ′ .rcs.last
                      𝑟𝑒𝑠𝑇 ∨ 𝑟𝑒𝑠 𝐹
                    else
                     ( if ¬check(𝜎 .𝜋, ¬𝑡 ) then 𝑄𝑡 (𝜎 {𝜋 := 𝜋𝑇 ,       R := R𝑇 } ) else success() )      ∧
                     ( if ¬check(𝜎 .𝜋, 𝑡 ) then 𝑄 ¬𝑡 (𝜎 {𝜋 := 𝜋𝐹 ,      R := R 𝐹 } ) else success() )

                ■     Handles imprecision           ■   Handles run-time check generation and collection

                                        Fig. 12. Formally defining the branch function


functionality by calling heap-rem-acc (defined in Appendix Fig. 27) for the look-up, assigning
the boolean results to 𝑏 1 and 𝑏 2 , and then using them in if-then-else and else-if casing. The
blue highlighting in the isImprecise is true case in the aforementioned rule handles the run-time
checks. Clauses in 𝜙e containing logical expressions are first evaluated to a symbolic value 𝑡, which
is then checked against 𝜎’s path condition 𝜋. If 𝜎 is precise, then pc-all(𝜋 ) ⇒Ó𝑡 must hold (i.e. the
constraints in 𝜋 prove 𝑡) or verification fails. In contrast, when 𝜎 is imprecise, pc-all(𝜋 ) ∧ 𝑡 must
hold (i.e. 𝑡 does not contradict constraints in 𝜋) otherwise verification fails. In this case, a run-time
check is added to 𝜎.R for the set of residual symbolic values in 𝑡 that cannot be proved statically
by 𝜋. The consume’ rules for expressions and symbolic values implement this behavior. The call
to assert (defined in Appendix Fig. 28) checks 𝑡 against 𝜋 and returns the result and any residual
symbolic values. Note, assert uses diff from Appendix §A.1 to compute the residuals. The part
highlighted in blue adds the run-time check for the residuals to the state. Finally, fields used in
𝜙e must have corresponding heap chunks in ℎ when 𝜎 and 𝜙e are precise; otherwise when 𝜎 or 𝜙e
are imprecise, field access can be justified by either the heaps or imprecision. A run-time check
containing an accessibility predicate for the field is added to 𝜎.R when imprecision is relied on. This
is all handled by the second argument 𝑓? to consume’ and eval-c called by consume’ on expressions.
   The third goal of consume is to remove heap chunks ℎ𝑐𝑖 representing accessibility predicates
and predicates in 𝜙e from 𝜎, and in particular, from heaps ℎ and ℎ ? . When 𝜎 and 𝜙e are both precise,
the heap chunks in ℎ𝑐𝑖 are each removed from ℎ (ℎ ? is empty here). If 𝜙e is imprecise, then all heap
chunks in both heaps are removed as they may be in ℎ𝑐𝑖 or 𝜙e may represent them with imprecision.
Finally, when 𝜎 is imprecise and 𝜙e is precise, any heap chunks in ℎ or ℎ ? that overlap with or
may potentially overlap with (thanks to 𝜎’s imprecision) heap chunks in ℎ𝑐𝑖 are removed. The
calls to heap-rem-acc (and its counterpart heap-rem-pred) in consume’, the extra heaps tracked
in consume’, and the heap assignments in the continuations from consume come together to
implement heap chunk removal.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:24                                                                                                           Aldrich

           consume(𝜎1 , 𝜃, 𝑄 )             = 𝜎2 := 𝜎1 { ℎ, 𝜋 := consolidate(𝜎1 .ℎ, 𝜎1 .𝜋 ) }

                                            consume’(𝜎2 , 𝜎2 .isImprecise , 𝜎2 .ℎ ? , 𝜎2 .ℎ, 𝜃, (𝜆 𝜎3 , ℎ ?′ , ℎ 1 , 𝛿 1 .

                                                  𝑄 (𝜎3 { ℎ ? := ℎ ?′ , ℎ := ℎ 1 }, 𝛿 1 ) ) )

           consume(𝜎1 , ? && 𝜙, 𝑄 ) = 𝜎2 := 𝜎1 { ℎ, 𝜋 := consolidate(𝜎1 .ℎ, 𝜎1 .𝜋 ) }

                                            consume’(𝜎2 , true , 𝜎2 .ℎ ? , 𝜎2 .ℎ, 𝜙, (𝜆 𝜎3 , ℎ ?′ , ℎ 1 , 𝛿 1 .

                                                  𝑄 (𝜎3 { isImprecise := true, ℎ ? := ∅, ℎ := ∅ }, 𝑝𝑎𝑖𝑟 (𝑢𝑛𝑖𝑡, 𝛿 1 ) ) ) )


   consume’(𝜎,     𝑓? , ℎ ? , ℎ, ( 𝑒 , 𝑡 ), 𝑄 )       = 𝑟𝑒𝑠, 𝑡 := assert(𝜎 .isImprecise, 𝜎 .𝜋, 𝑡 )

                                                         R ′ := addcheck (𝜎 .R, 𝑒, translate (𝜎, 𝑡 ) )

                                                       𝑟𝑒𝑠 ∧ 𝑄 (𝜎 { R := R ′ }, ℎ ? , ℎ, 𝑢𝑛𝑖𝑡 )
   consume’(𝜎1 ,   𝑓? , ℎ ? , ℎ, 𝑒, 𝑄 )               = eval-c (𝜎1 { isImprecise := 𝑓? }, 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                    consume’(𝜎2 { isImprecise := 𝜎1 .isImprecise },             𝑓? , ℎ ? , ℎ, ( 𝑒 , 𝑡 ), 𝑄 ) ) )

   consume’(𝜎1 ,   𝑓? , ℎ ? , ℎ, acc (𝑒.𝑓 ), 𝑄 ) = eval-c (𝜎1 { isImprecise := 𝑓? }, 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                        𝜎3 := 𝜎2 { isImprecise := 𝜎1 .isImprecise }

                                                       𝑟𝑒𝑠, 𝑡 := assert(𝜎3 .isImprecise, 𝜎3 .𝜋, 𝑡 ≠ null)
                                                       𝑟𝑒𝑠 ∧ (

                                                         R ′ := addcheck (𝜎3 .R, acc (𝑒.𝑓 ), translate (𝜎3 , 𝑡 ) )

                                                         (ℎ 1 , 𝛿 1 , 𝑏 1 ) := heap-rem-acc(𝜎3 .isImprecise, ℎ, 𝜎3 .𝜋, 𝑓 (𝑡 ) )

                                                        if (𝜎3 .isImprecise ) then

                                                            (ℎ ?′ , 𝛿 2 , 𝑏 2 ) := heap-rem-acc(𝜎3 .isImprecise, ℎ ? , 𝜎3 .𝜋, 𝑓 (𝑡 ) )

                                                            if (𝑏 1 = 𝑏 2 = false ) then

                                                              R ′′ := addcheck ( R ′ , acc (𝑒.𝑓 ), acc ( translate (𝜎3 , 𝑡 ).𝑓 ) )

                                                            else R ′′ := R ′

                                                            𝑄 (𝜎3 { R := R ′′ }, ℎ ?′ , ℎ 1 , ( if (𝑏 1 ) then 𝛿 1 else 𝛿 2 ) )

                                                        else if (𝑏 1 ) then 𝑄 (𝜎3 { R := R ′ }, 𝜎3 .ℎ ? , ℎ 1 , 𝛿 1 )

                                                        else failure() ) ) )

                    ■     Handles imprecision           ■     Handles run-time check generation and collection

                                    Fig. 13. Select rules for symbolically consuming formulas


4.3.7 Symbolic execution of statements. The exec rules in Gradual Viper, which symbolically
execute program statements, are largely unchanged from Viper. The only differences are 1) the
rules now utilize versions of eval, produce, consume, and branch defined previously in this paper
and 2) the rules track origins where appropriate. To provide an intuition, select rules for exec are
given in Fig. 14; the full set of rules are listed in the Appendix §A.4. The exec function takes a
symbolic state 𝜎, program statement 𝑠𝑡𝑚𝑡, and continuation 𝑄. Then, exec symbolically executes
𝑠𝑡𝑚𝑡 using 𝜎 to produce a potentially modified state 𝜎 ′ , which is passed to the continuation.
   Symbolic execution of field assignments first evaluates the right-hand side expression 𝑒 to the
symbolic value 𝑡. Any field reads in 𝑒 are either directly or optimistically verified using 𝜎1 . Then,
the resulting state 𝜎2 must establish write access to 𝑥 .𝑓 in consume, i.e. 𝜎2 ⇒     f acc (𝑥 .𝑓 ). Calling
consume also removes the field chunk for acc (𝑥 .𝑓 ) from 𝜎2 (if it is in there) resulting in 𝜎3 . Therefore,
Gradual C0                                                                                                              1:25


       exec(𝜎1 , 𝑥 . 𝑓 := 𝑒, 𝑄 ) = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . consume (𝜎2 , acc (𝑥 .𝑓 ), (𝜆 𝜎3 , _ .
                                      produce (𝜎3 , acc (𝑥 .𝑓 ) && 𝑥 .𝑓 = 𝑡, 𝑝𝑎𝑖𝑟 ( fresh, 𝑢𝑛𝑖𝑡 ), 𝑄 ) ) ) ) )

       exec(𝜎1 , 𝑧 := 𝑚 (𝑒 ), 𝑄 ) = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .

                                      R ′ := 𝜎2 .R { origin := (𝜎2 , 𝑧 := 𝑚 (𝑒 ), 𝑡 ) }

                                      consume (𝜎2 { R := R ′ }, 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 [𝑚𝑒𝑡ℎ𝑎𝑟𝑔𝑠 ↦→ 𝑡 ], (𝜆 𝜎3 , 𝛿 .

                                          if ( equi-imp(𝑚𝑒𝑡ℎ𝑝𝑟𝑒 ) ) then

                                            𝜎4 := 𝜎3 { isImprecise := true, ℎ ? := ∅, ℎ := ∅, 𝛾 := havoc(𝜎3 .𝛾, 𝑧 ) }
                                          else 𝜎4 := 𝜎3 {𝛾 := havoc(𝜎3 .𝛾, 𝑧 ) }

                                          produce (𝜎4 , 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 [𝑚𝑒𝑡ℎ𝑎𝑟𝑔𝑠 ↦→ 𝑡 ] [𝑚𝑒𝑡ℎ𝑟𝑒𝑡 ↦→ 𝑧 ], fresh,

                                           (𝜆 𝜎5 . 𝑄 (𝜎5 { R := 𝜎5 .R { origin := none } } ) ) ) ) ) ) )

                   ■    Handles imprecision        ■    Handles run-time check generation and collection

                           Fig. 14. Select rules for symbolically executing program statements

the call to produce can safely add a fresh field chunk for acc (𝑥 .𝑓 ) alongside 𝑥 .𝑓 = 𝑡 to 𝜎3 before it
is passed to the continuation 𝑄. Under the hood, run-time checks are collected and passed to 𝑄.
   The method call rule evaluates the arguments 𝑒 to symbolic values 𝑡, consumes the method
precondition (substituting arguments with 𝑡) while making sure the origin is set properly for check
and branch condition insertion, havocs existing assumptions about the variables being assigned
to, produces knowledge from the postcondition, and finally continues after resetting the origin to
none. An in-depth explanation is in the Appendix, along with the other exec rules and equi-imp
definition.
   Note that while Gradual Viper treats predicates iso-recursively in all other cases, it makes an
exception when consuming preconditions at method calls (and loop invariants before entering
loops), which can be seen in the if-then in the method call rule (Fig. 14). If Gradual Viper determines
the precondition (invariant) is equi-recursively imprecise, then it will conservatively remove all
the heap chunks from both symbolic heaps and make the state imprecise after the consume. This
exception ensures the static verification semantics in Gradual Viper lines up with the equi-recursive,
dynamic verification semantics encoded by GVC0 (describe in §4.4) such that Gradual C0 is sound.
Interestingly, Wise et al. [2020]’s gradual verifier does not need this special case, because it does not
optimize run-time checks with statically available information. Once optimization is introduced,
the semantics across the two systems need to be more tightly integrated to ensure soundness.
Zimmerman et al. [2024] alerted us to this issue and proposed the aforementioned solution.
4.3.8 Valid Gradual Viper programs. Finally, putting everything together, a Gradual Viper program
is checked by examining each of its method and predicate definitions to ensure they are well-formed
(formally defined in Appendix Fig. 31). The formal definitions are given in Fig. 15, and a more
detailed description of the rules is given in the Appendix, §A.5. Intuitively, for each method, we
define symbolic values for the method arguments, and then create an initial symbolic state by
calling the produce function on the method precondition7 . We then call the exec function on the
method body, which symbolically executes the body and ensures that all operations are valid based
on that precondition. Finally, we invoke the consume function on the final symbolic state and the
postcondition, verifying that the former implies the latter. Throughout these operations a set of
run-time checks is built up, which (along with success or failure) is the ultimate result of gradual
verification.
7 Note, produce is part of well-formed.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:26                                                                                                           Aldrich

verify(method 𝑚 (𝑥 : 𝑇 ) returns (𝑦 : 𝑇 ) ) = well-formed (𝜎0 {𝛾 := 𝜎0 .𝛾 [𝑥 ↦→ fresh ] [𝑦 ↦→ fresh ] }, 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 , fresh, (𝜆 𝜎1 .

                                                 well-formed (𝜎1 { isImprecise := false, ℎ ? := ∅ , ℎ := ∅ }, 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 ,
                                                     fresh, (𝜆 _ . success() ) )
                                                 ∧
                                                 exec (𝜎1 , 𝑚𝑒𝑡ℎ𝑏𝑜𝑑 𝑦 , (𝜆 𝜎2 .
                                                     consume (𝜎2 , 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 , (𝜆 𝜎3 , _ .

                                                        ℜ := ℜ ∪ 𝜎3 .R.rcs ; success() ) ) ) ) ) )
verify(predicate 𝑝 (𝑥 : 𝑇 ))                 = well-formed (𝜎0 {𝛾 := 𝜎0 .𝛾 [𝑥 ↦→ fresh ] }, 𝑝𝑟𝑒𝑑𝑏𝑜𝑑 𝑦 , fresh, (𝜆 _ . success() ) )

                   ■    Handles imprecision      ■      Handles run-time check generation and collection

                                   Fig. 15. Rules defining a valid Gradual Viper program


4.4   Dynamic Verification: Encoding Run-time Checks into C0 Source Code
After static verification, Gradual Viper returns a collection of run-time checks ℜ that are required
for soundness to GVC0. Then, GVC0 creates a C0 program from the run-time checks in ℜ and the
original C0 program by encoding the checks in C0 source code. The C0 program is sent to the C0
compiler to be compiled, executed, and thus dynamically verified. We chose to encode the run-time
checks directly in source code to avoid complexities from augmenting the C0 compiler with support
for dynamic verification. Further, since C0 is a simple imperative language, any more expressive
language should be able to encode the checks far more easily. That is, we hope this work serves as
a guide to the developers of Gradual Viper frontends for other languages on how to implement
efficient dynamic verification for gradual verification—especially, when modifying the compiler for
their language is difficult. The rest of this section illustrates GVC0’s encoding of run-time checks
into C0 source code via example. We also highlight design points in the encoding that minimize
run-time overhead of the checks during execution.
   Now, consider the C0 program in Fig. 16 that implements a method for inserting a new node at the
end of a list, called insertLastWrapper. Note, when passed a non-empty list, insertLastWrapper calls
insertLast from Fig. 1 to perform insertion (line 17). Here, insertLast is gradually verified with the
simpler and fully specified (precise) acyclic predicate given on lines 1-4 in Fig. 16. For our purposes,
we only need to know that insertLast’s precondition is ? && acyclic(list) && list != NULL
and its postcondition is acyclic(\result) && \result != NULL. The insertLastWrapper method is
also gradually specified: its precondition is ? (line 7)—requiring unknown information—and its
postcondition is acyclic(\result) (line 8)—ensuring the list after insertion is acyclic. Fig. 16 also
contains run-time checks generated by Gradual Viper for insertLastWrapper, as highlighted in blue.
The first check (lines 15-16) ensures the list l sent to insertLast (line 17) is acyclic, and is only
required when l is non-empty (non-null). The second check (lines 20-21) ensures the list returned
from insertLastWrapper is acyclic, and is only required when insertLastWrapper’s parameter l
is empty (null). These checks are not executable by the C0 compiler; therefore, GVC0 takes the
program and checks in Fig. 16 and returns the executable program in Fig. 17. That is, GVC0 encodes
branch conditions (lines 15 and 20), predicates (lines 16 and 21), accessibility predicates (acc ( l->val)
and acc ( l->next) in acyclic’s body, lines 1-4), and separating conjunctions (also in acyclic’s body)
from Gradual Viper into C0 source code. We discuss the aforementioned encodings in sections
§4.4.1, §4.4.2, and §4.4.3 respectively. While not in the insertLastWrapper example, GVC0 translates
checks of simple logical expressions into C0 assertions: e.g. assert(y >= 0);.

4.4.1 Encoding branch conditions. Run-time checks contain branch conditions that denote
the execution path a check is required on. For example, in Fig. 16 acyclic(\result) should only be
Gradual C0                                                                                                        1:27


 1   /* @ predicate acyclic ( Node * l ) =                1     Node * insertLastWrapper ( Node * l , int val ,
 2          l == NULL ? true :                            2       OwnedFields* _ownedFields )
 3            acc (l -> val ) && acc (l - > next ) &&     3     {
 4            acyclic (l - > next ) ; @ */                4       bool _cond_1 = l == NULL;
 5                                                        5       if ( l == NULL ) {
 6   Node * insertLastWrapper ( Node * l , int val )      6          l = alloc ( struct Node );
 7     // @ requires ?;
                                                          7           l->_id = addStructAcc(_ownedFields, 2);
 8     // @ ensures acyclic (\ result );
                                                          8          l - > val = val ; l - > next = NULL ;
 9   {
                                                          9       } else {
10     if (l == NULL ) {
11        l = alloc ( struct Node );                     10           if (!_cond_1) { acyclic(l, _ownedFields); }
12        l -> val = val ;                               11           OwnedFields* _tempFields =
13        l -> next = NULL ;                             12                initOwnedFields(_ownedFields->instCntr);
14     } else {                                          13           sep_acyclic(l, _tempFields);
15     ({(none, l == NULL, ¬(l == NULL))},               14           l = insertLast (l , val , _ownedFields );
16         (l=insertLast(l,val), acyclic(l), acyclic(l)) 15         }
17         l = insertLast (l , val );                    16         if (_cond_1) { acyclic(l, _ownedFields); }
18       }
                                                         17         OwnedFields* _tempFields1 =
19       return l;
                                                         18              initOwnedFields(_ownedFields->instCntr);
20       ({(none, l == NULL, l == NULL)},
                                                         19         sep_acyclic(l, _tempFields1);
21         (none, acyclic(\result), acyclic(\result))
                                                         20         return l ;
22   }
                                                         21     }
     ■    Run-time checks from Gradual Viper
                                                                          ■   Run-time checks from GVC0
Fig. 16. Original insertLastWrapper program with
                                                              Fig. 17. GVC0 generated insertLastWrapper program
run-time checks from Gradual Viper
                                                              with run-time checks

checked at lines 20-21 when l == NULL, as indicated by the branch condition (none,l == NULL,l ==
NULL). Therefore, GVC0 first encodes the condition l == NULL into C0 code. In general, conditions
are encoded as logical expressions in C0 and assigned to fresh boolean variables at the program
point where they originated—we call this versioning. Then, the boolean variable is used in checks
in place of the condition. For example, the origin and location pair (none,l == NULL) tells GVC0
that l == NULL must be evaluated at the program point in insertLastWrapper containing the l ==
NULL AST element. As a result, in Fig. 17 a boolean variable _cond_1 is introduced on line 4 to hold
the value of l == NULL. The condition variable _cond_1 is then used in the C0 run-time check for
acyclic(\result) later in the program (line 16). To reduce run-time overhead, _cond_1 is also used
in the check for acyclic(l) on line 10, which relies on the same branch point (none,l == NULL).
Further, while not demonstrated here, GVC0 supports short-circuit evaluation of conditions on the
same execution path to reduce run-time overhead. Finally, note, GVC0 carefully places versioning
code after any run-time checks encoded at the program point where the condition originated to
ensure this new assignment code (not verified by Gradual Viper) is framed, i.e. correct.
4.4.2 Encoding predicates. Now that GVC0 has versioned the branch conditions in Fig. 16 into
variables, GVC0 can use the variables to develop C0 run-time checks. The Gradual Viper check
({(none,l == NULL,¬(l == NULL))}, (l=insertLast(l,val),acyclic(l),acyclic(l))) is translated
into if (!_cond_1) {acyclic(l,_ownedFields);} on line 10 in Fig. 17. GVC0 places this C0 check
according to the origin, location pair ((l=insertLast(l, val),acyclic(l)), which points to the
program point just before the call to insertLast on line 14. The branch condition becomes the
if statement with condition !_cond_1 (§4.4.1), and acyclic(l) is turned into the C0 function call
acyclic(l,_ownedFields). The acyclic function implements acyclic’s predicate body as C0 code: it
asserts true for empty lists and recursively verifies accessibility predicates (using _ownedFields) for
nodes in non-empty lists. That is, predicates are encoded and treated equi-recursively by GVC0.
For efficiency, separation of list nodes is encoded separately on lines 11-13. We discuss the dynamic
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:28                                                                                                           Aldrich

verification of accessibility predicates and the separating conjunction in C0 code next (§4.4.3).
Finally, a similar C0 check is created for acyclic(\result) on lines 16-19.
4.4.3 Encoding accessibility predicates and separating conjunctions. GVC0 implements
run-time tracking of owned heap locations in C0 programs to verify accessibility predicates and
uses of the separating conjunction.
   Encoding owned fields in C0 source code. An owned field is a tuple (𝑖𝑑, field) where 𝑖𝑑 is an integer
identifying a struct instance (object in C0) and field is an integer indexing a field in the struct. The
OwnedFields struct, which is implemented as a dynamic hash table to improve check performance,
contains currently owned fields. That is, hashed object identifiers (𝑖𝑑) and then field identifiers
(field) are used to index into OwnedFields where a boolean that determines whether or not the field
is currently owned is stored. Since objects are tracked with integers, all struct definitions in a C0
program are modified to contain an additional _id field.
   Semantics of tracking owned fields (inspired by Wise et al. [2020]). At the entry point to a C0
program (e.g. main), an empty OwnedFields struct called _ownedFields is allocated and initialized.
This is not shown in Fig. 17. Then, when a new struct instance is created—such as allocating a
new node on line 6 in Fig. 17—the _id field is initialized with the value of a global integer instCntr
that uniquely identifies the instance. The call to library function addStructAcc on line 7 performs
this functionality and then increments instCntr. It also adds all fields in the struct instance (e.g.
l->val:(l->_id,0), l->next:(l->_id,1), and l->_id:(l->_id,2)) to _ownedFields and marks them
as owned. The only other times _ownedFields can change are at method/function calls. Methods,
like insertLast and insertLastWrapper, may add or drop owned fields during their executions.
They may also contain run-time checks, such as the one for acyclic(l) on line 10, that need owned
fields for verification. So, GVC0 adds an additional parameter to the their declarations (e.g. line 2,
Fig. 17) to accept, initialize, and then modify _ownedFields in their contexts. A callee’s pre- and
postcondition controls what owned fields are passed to and from the callee via this new parameter.
When a method’s precondition is imprecise8 , then any caller will pass all of its owned fields to the
method, as on line 14 for the call to insertLast. After execution, the callee method returns all of its
owned fields to the caller. When a method’s precondition is precise, then any caller only passes its
owned fields specified by the precondition to the method. If the method’s postcondition is imprecise,
then after execution the callee method returns all of its owned fields as before; otherwise, only the
owned fields specified by the postcondition are returned. Finally, as an optimization, in precisely
specified methods (no external—pre- and postconditions—or internal—loop invariants, unfolds,
folds, etc.—specifications contain imprecision and no run-time checks are required), GVC0 does not
implement any _ownedFields tracking. In this case, GVC0 uses the callee’s pre- and postcondition
to modularly update _ownedFields in the caller.
   Verifying accessibility predicates and separating conjunctions with owned fields. Now, _ownedFields
tracking is used to verify accessibility predicates and uses of the separating conjunction. Run-time
checks for accessibility predicates are turned into assertions that ensure the presence of their heap
location in _ownedFields. For example, acc ( l->val) looks like assertAcc(_ownedFields,l->_id,0);
in C0 code, where 0 is the index for val in the Node struct. The assertAcc library function indexes
into _ownedFields using l->_id and 0 and ensures a boolean entry is in there and is true; otherwise,
assertAcc throws an error. Wherever GVC0 must check separation of heap locations (as indicated
in run-time checks from Gradual Viper via a flag9 ),—such as for the nodes in list l at lines 10-13—it
8 Here, a formula is also imprecise if it contains predicates that expose ? when fully unrolled—an equi-recursive treatment.
9 Note, this flag is not formalized in this paper for simplicity.
Gradual C0                                                                                         1:29


creates (with the library method initOwnedFields) an auxiliary data structure _tempFields of type
OwnedFields. We check that heap cells are disjoint by adding them one at a time to _tempFields and
failing if the cell is already there. GVC0 generates a sep_X method for each predicate X to actually
perform the separation check; and when done, discards _tempFields, as its purpose was only to
check separation. Similar checks are created for the acyclic(\result) check on lines 16-19.

5     EMPIRICAL EVALUATION
The seminal work on gradual typing [Siek and Taha 2006] selectively inserts run-time casts in
support of optimistic static checking: for instance, whenever a function application is deemed
well-typed only because of imprecision—such as passing an argument of the unknown type to
a function that expects an integer—the type-directed cast insertion procedure inserts a run-time
check. But if the application is definitely well-typed, no cast is inserted. This approach ensures that
a fully-precise program does not incur any overhead related to run-time type checking. While it is
tempting to assume that more precision necessarily results in better performance, the reality has
been shown to be more subtle: both the nature of the inserted checks (such as higher-order function
wrappers) as well as when/how often they are executed is of utmost importance [Muehlboeck
and Tate 2017; Takikawa et al. 2016], and anticipating the performance impact of precision is
challenging [Campora et al. 2018].
   The performance of gradual verification has never been studied until now, due to the lack of
a working gradual verifier. Here, we explore the relation between minimizing dynamic check
insertion with statically available information and observed run-time performance in gradual
verification with Gradual C0. Specifically, we explore the performance characteristics of Gradual
C0 for thousands of partial specifications generated from four data structures, as inspired by
Takikawa et al. [2016]’s work in gradual typing. In particular, we observe how adding or removing
individual atomic formulas and ? within a specification impacts the degree of static and dynamic
verification and, as a result, the run-time overhead of the program. Additionally, we compare the
run-time performance of Gradual C0 to a fully dynamic approach, as readily available in C0. The
aforementioned ideas are captured in the following research questions:
RQ1: As specifications are made more precise, can more verification conditions be eliminated
     statically?
RQ2: Does gradual verification result in less run-time overhead than a fully dynamic approach?
RQ3: Are there particular types of specification elements that have significant impact in run-time
     overhead, and can high overhead be avoided?

5.1    Creating Performance Lattices
We define a complete specification as being statically verifiable when all ?s are removed, and then
a partial specification as a subset of formulas from a complete specification that are joined with
?. Like Takikawa et al. [2016], we model the gradual verification process as a series of steps from
an unspecified program to a statically verifiable specification where, at each step, an element is
added to the current, partial specification. An element is an atomic conjunct (excluding boolean
primitives) in any type of method contract, assertion, or loop invariant. We form a lattice of partial
specifications by varying which elements of the complete specification are included. We also
similarly vary the presence of ? in formulas that are complete—contain the same elements as their
counterparts in the statically verifiable specification—and have related fold and unfold statements
in the partial specification. Otherwise, ? is always added to incomplete formulas. This strategy
creates lattices where the bottom entry is an empty specification containing only ?s and the top
entry is a statically verifiable specification. A path through a lattice is the set of specifications
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:30                                                                                                           Aldrich

                                                                            Contents of Complete Spec
  Example              Unverified Complexity    # Specs
                                                           Fold   Unfold      Pre.       Post.    Pred. Body    Loop Inv.
  Binary Search Tree        𝑂 (𝑛 𝑙𝑜𝑔 (𝑛) )        3473      43      23     0/20/21/24   0/22/6/24    6/6/7/4    0/2/4/2
  Linked List                   𝑂 (𝑛)             1745      17      10      8/6/15/5     4/5/6/5     4/3/4/3    4/3/5/2
  Composite                 𝑂 (𝑛 𝑙𝑜𝑔 (𝑛) )        2577      28      15      0/10/2/12   0/11/1/12   32/9/17/3   0/3/2/3
  AVL                       𝑂 (𝑛 𝑙𝑜𝑔 (𝑛) )        3057      25      14       3/4/5/9     3/6/9/9    25/8/21/3   1/1/2/1
Table 1. Description of benchmark examples. For each example, the table shows the complexity of the test program without
verification, the number of sampled partial specifications, and the distribution of specification elements for the complete
specification. Element counts are formatted as “Accessibility Predicate/Predicate Instance/Boolean Expression/Imprecision"

created by appending 𝑛 elements or removing ?s one at a time from the bottom to the top of the
lattice. The large array of partial specifications created in each lattice closely approximates the
positive specifications supported by the gradual guarantee [Wise et al. 2020], which are less precise
variants of successfully verified programs. For reference, we give a more formal statement of the
gradual guarantee:
         Let 𝑝 1 and 𝑝 2 be Gradual C0 programs where 𝑝 1 ⊑ 𝑝 2 (i.e. the formulas in 𝑝 1 are more
         precise than those in 𝑝 2 ). If 𝑝 1 statically verifies, then 𝑝 2 statically verifies. Additionally,
         𝑝 2 must execute at least as far as 𝑝 1 executes at run time.
Now, to illustrate the aforementioned approach, consider the following loop invariant:
              // @ loop_invariant sortedSeg ( list , curr , curr - > val ) && curr - > val <= val ;

The invariant is made of two elements: the sortedSeg predicate instance and the boolean expres-
sion curr->val <= val;. The lattice generated for a program with this invariant has five unique
specifications: four contain a combination of the two elements joined with ?, and the fifth is the
complete invariant above.

5.2    Data Structures
To apply this methodology, we implemented and fully specified four recursive heap data structures
with Gradual C0: binary search tree, sorted linked list, composite tree, and AVL tree. We chose
these data structures because complete static specifications exist for them in prior work and
they are interesting use cases for gradual verification. Linked list is implemented with a while
loop rather than recursion. Binary search tree is a more complex data structure with a more
complex property (BST property) than a linked list and uses recursion. Composite tree implements
a structure where modifications do not have to start at the root, but can be applied directly to any
node in the tree. Its invariant also applies to any node in the tree. Finally, AVL tree implements
the most complex invariant (the balanced property) and data structure with many interdependent
functions and predicates related to tree rotations. Each data structure has a test program that
contains its implementation and a main function that adds elements to the structure based on a
workload parameter 𝜔. We design the test programs to incur as little run-time overhead as possible
outside of structure size and run-time checks. For each example and corresponding test program,
Table 1 displays the distribution of elements in the complete specification, as well as the run-time
complexity of the test program and the number of unique partial specifications generated by our
benchmarking tool.

   Binary Search Tree (BST). The implementation of the binary search tree is typical; each node
contains a value and pointers to left and right nodes. We statically specify memory safety and
preservation of the binary search tree property—that is, any node’s value is greater than any value
in its left subtree and less than any value in its right subtree. The test program creates a root node
with value 𝜔 and sequentially adds and removes a set of 𝜔 values in the range [0, 2𝜔]. Note that
values are removed in the same order they were added.
Gradual C0                                                                                                            1:31


   Linked List. We implement a linked list with insertion similar to the one given in Fig. 1. Insertion
is statically specified for memory safety as well as preservation of list sortedness. Its test program
creates a new list and inserts 𝜔 arbitrary elements.
   Composite. The composite data structure is a binary tree where each node tracks the size of its
subtree—this is verified by its specification along with memory safety. Its test program starts with
a root node and builds a tree of size 𝜔 by randomly descending from the root until a node without
a left or right subtree is reached. A new node is added in the empty position, and then traversal
backtracks to the root.
   AVL Tree. The implementation of AVL tree with insertion is standard except that the height of
the left and right subtrees is stored in each node (instead of the overall height of the tree). This
allows us to easily state the AVL balanced property—for every node in the tree the height difference
between its left and right children is at most 1—without using functions or ghost variables, which
Gradual C0 does not currently support. In addition to specifying the AVL balanced property for
insertion, we also specify memory safety. The AVL test program starts with a root node and builds
a tree of size 𝜔 by inserting randomly valued nodes into the tree using balanced insertion.

5.3    Experimental Setup
With upwards of 100 elements in the specifications for each data structure, it is combinatorially
infeasible to fully explore every partial specification. Therefore, unlike Takikawa et al. [2016],
we proceed by sampling a subset of partial specifications in a lattice, rather than executing them
all. Specifically, we sample 16 unique paths through the lattice from randomized orderings of
specification elements. We chose partial specifications along lattice paths to explore trends in
migration from no specifications to complete specifications, which is how we imagine developers
may use our tool. We also randomly sampled paths, rather than using a another heuristic for
selecting paths, to be prescriptive to users of Gradual C0. We wanted to find and recommend new
specification patterns that users should apply or avoid depending on their performance. Every step
is executed with three workloads chosen arbitrarily to ensure observable differences in timing.
Each timing measurement is the median of 10 iterations. Programs were executed on four physical
Intel Core i5-4250U 1.3GHz Cores with 16 GB of RAM.
   We introduce two baseline verifiers to compare Gradual C0 against. The dynamic verifier trans-
forms every specification into a run-time check and inserts accessibility predicate checks for field
dereferences—thereby emulating a fully dynamic verifier. The framing verifier only performs the
accessibility predicate checks, and therefore represents the minimal dynamic checks that must be
performed in a language that checks ownership.10 We implement the baseline verifiers ourselves
using Wise et al. [2020]’s dynamic semantics, which checks everything at run time, as a guide.
Wise et al. [2020]’s work is the only work that we are aware of that handles run-time checking of
both ownership and recursive predicates.

5.4    Evaluation
Fig. 18 shows how the total number of verification conditions (proof obligations) changes as more
of each benchmark is specified (green curve). The figure also similarly shows the number of
verification conditions that are statically verified as each benchmark is specified (purple curve).
From the green curve, we see that even when there are no specifications, there are verification
conditions, e.g. before a field is accessed, the object reference must be non-null and the field must be
10 These framing checks could fail, for example, if some function lower in the call stack owns data that is accessed by the

currently-executing function.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:32                                                                                                           Aldrich

                                            Mean Verification Conditions




                           Total Verification Conditions       Statically Eliminated Verification Conditions
Fig. 18. For each example, the average quantity of verification conditions and the subset that were eliminated statically at
each level of specification completeness across all paths sampled. Shading indicates the standard deviation.


                                      Mean Execution Time Over All Paths




                             Dynamic Verification          Only Framing Checks       Gradual Verification
Fig. 19. The mean time elapsed at each step over the 16 paths sampled. Shading indicates the confidence interval of the
mean for each verification type.


owned. Some of these verification conditions can be verified statically as illustrated by the purple
curve. As more of a benchmark is specified, there are more verification conditions (green curve); but
also, more of these verification conditions are discharged statically and do not have to be checked
dynamically (purple curve). Towards the right end of the plots, the two curves converge until they
meet when all the verification conditions are discharged statically. As a result, the answer to RQ1
is yes. Note, the number of verification conditions does decrease when enough of the benchmark is
specified. This is due to being able to prune symbolic execution paths with new static information.
   The plots in Fig. 19 display the run-time performance (in red) of dynamically checking the
verification conditions from Fig. 18. The plots also show how the run-time performance of the
dynamic verifier (in green) and framing verifier (in purple) change as more of each benchmark is
specified. The green lines show that as more properties are specified, the cost of run-time verification
increases. With Gradual C0, some of these properties can be checked statically; therefore, the run-
time cost of gradual verification, shown in red, starts equivalent but eventually ends up significantly
lower than the cost of pure run-time verification.
   Notably, the purple lines are significantly lower than the red and greens ones until they exhibit
a dramatic increase starting at around 80% specified all the way to 100%. Eventually (after about
95% specified), the purple lines end above the red ones (but below the green ones) where running
time is orders of magnitude higher than at the start of the incline. The framing verifier (in purple)
only checks that heap accesses are safe—i.e. they are owned and their receivers are non-null.
So unsurprisingly, the dynamic and gradual verifiers, which check more properties like heap
Gradual C0                                                                                                            1:33

                                    % Δ𝑡 , GV vs. DV            % Steps GV < DV for Paths DV < GV
        Example       𝜔                                                                             % Paths GV < DV
                            Mean    St. Dev.   Max     Min      Mean St. Dev.      Max      Min.
                      32    -14.4    29.4     170.0     -88.8   80.6     14.8      95.3    50.8           0.0
             AVL      64    -16.1    50.5     256.3     -96.0   84.3     15.5      98.4    55.5           0.0
                      128   -11.5    74.0     384.7     -98.6   82.2     16.5      99.5    55.0           0.0
                      32    -24.7    35.0     144.5     -93.8   74.2     9.0       89.4    60.8           0.0
             BST      64    -23.9    46.8     301.3     -98.5   74.7     9.3       92.2    59.4           0.0
                      128   -21.7    55.6     436.1     -99.6   74.7     11.9      96.3    51.6           0.0
                      32    -18.0    27.7     138.9     -95.7   78.8     14.8      96.3    34.9           0.0
        Linked List   64    -21.0    48.6     389.0     -99.8   85.2     15.1     100.0    37.6           6.3
                      128   -20.7    59.7     603.3    -100.0   85.8     15.0      99.1    42.2           0.0
                      32    -34.4    40.1     141.7     -99.1   80.3     10.7      94.4    60.9           0.0
        Composite     64    -33.1    50.1     258.6     -99.8   80.0     12.2      96.3    50.9           0.0
                      128   -30.1    63.9     419.0    -100.0   80.4     13.0      96.3    48.4           0.0
Table 2. Summary statistics for the performance of each example over 16 paths at selected workloads (𝜔), comparing
gradual verification (GV) against dynamic verification (DV). The grouped column “% in Δ𝑡 , GV. vs. DV." displays summary
statistics for the percent decrease in time elapsed for each step when using GV versus DV. The column “% Steps GV<DV
for Paths DV<GV" shows the distribution of steps that performed best under GV that were part of paths containing steps
that performed better under DV. The final column shows the percentage of paths in which every step performed better
under GV.

separation, nearly always have significantly higher run-time verification overhead than the framing
verifier. Eventually, Gradual C0 outperforms the framing verifier when enough properties, including
framing, are checked statically.
   The dramatic increase in the framing verifier’s run-time performance is caused by the owned
fields passing strategy employed at method boundaries (described in §4.4.3) to verify memory
safety at run time. To respect precondition abstractions, only owned fields specified by a callee’s
precondition are passed by the caller to the callee when the precondition is precise. Similarly, when
a callee’s postcondition is precise, then only the owned fields specified by the postcondition are
passed back to the caller. Computing owned fields from precise contracts is costly; and even more-so
for contracts containing recursive predicates like in our benchmarks. Further, our benchmarks call
such methods frequently during execution. As a result, execution time increases significantly at
each path step where one of the aforementioned methods gets a precise pre or postcondition from
? removal. This, of course, happens more frequently as more of a benchmark is specified. At 100%
specified every method contract is precise, and so the owned fields passing strategy is used at every
method call and return leading to the highest run-time costs for the framing verifier. In contrast,
Gradual C0 checks fully-specified methods completely statically and does not use the owned field
passing strategy for calls to these methods. As a result, looking at the red lines, Gradual C0 is not
heavily affected by this phenomena—we see slight increases starting at 90% specified but they
are significantly less costly. Additionally, once a critical mass of specifications have been written,
Gradual C0’s run-time verification cost decreases until reaching zero—which is the same as running
the raw C0 version of the benchmark. If the spikes around 90% specified are too costly, production
gradual verifiers can reduce them by employing more optimal permission passing strategies.
   In general, according to the red lines, Gradual C0’s performance increases gradually as more
proof obligations are specified but are not yet statically verified; and thus, must be checked at
run time. When a critical mass of specifications are written that allows more and more of these
proof obligations to be proven statically, run-time performance starts to decrease until reaching
the spikes around 90% specified caused by owned fields passing. After the spikes, performance
decreases to the benchmark’s raw baseline. This trend is consistent with speculations made in Wise
et al. [2020]’s work, and also confirms that increasing precision in gradual verification does not
always correspond with decreased run-time overhead from dynamic verification.
   Table 2 displays summary statistics for Gradual C0’s performance on every sampled partial
specification compared to the dynamic verification baseline. Depending on the workload and
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:34                                                                                                           Aldrich

                                99th Percentile Changes in Run-time Overhead




                      Accessibility Predicate    Predicate Instance    Boolean Expression     ? Removed
Fig. 20. The quantity of specification elements, grouped by type and location, that caused the highest (𝑃 99% ) increases and
decreases in time elapsed out of every path sampled


example, on average Gradual C0 reduces run-time overhead by 11.5-34.4% (Table 2, Column 3)
compared to the dynamic verifier. Note, the speed-ups are consistent as 𝜔 increases: -14.4%, -
24.7%, -18.0%, and -34.4% at the lowest 𝜔 values compared to -11.5%, -21.7%, -20.7%, and -30.1%
at the largest. While Gradual C0 generally improves performance, there are some outliers in the
data (Table 2, Column 5) where Gradual C0 is slower than dynamic verification by 138.9-603.3%.
Fortunately, for lattice paths that produce these poor-performing specifications, gradual verification
still outperforms dynamic verification (on average) for 74.2-85.8% (Table 2, Column 7) of all steps.
Further, these outliers appear under 20% specified where the bookkeeping we insert to track
conditionals, which is unoptimized and could be improved, and measurement error are the cause
of such outcomes.
   Fig. 19 displays the average run-time cost across all paths under each of our benchmarks and
verifiers. In all the plots, for some early parts of the path the cost of Gradual C0 is comparable
to or exceeds the cost of the dynamic verifier, but after 50% completion, static optimization kicks
in and Gradual C0 begins to significantly outperform it. Further, Table 2 shows that on average
Gradual C0 reduces run-time overhead by 11.5-34.4% compared to the dynamic verifier. Therefore,
the answer to RQ2 is yes.
   Fig. 20 captures the impact that different types of specification elements (accessibility predicates,
predicates, and boolean expressions) have on Gradual C0’s run-time performance when specified
in different locations. It also captures the impact removing ? from a formula has on performance.
Elements that when added or ? that when removed from one step in a lattice path to another
increase run-time overhead significantly (in the top 1%) are counted in the left sub-figure, and ones
that decrease run-time overhead significantly (top 1%) are counted in the right sub-figure. The
count for accessibility predicates is colored in green, predicates in purple, boolean expressions in
yellow, and ? removal in red.
   Adding recursive predicates to preconditions, postconditions, and predicate bodies is the most fre-
quent cause (67.6%) of dramatic increases in run-time verification overhead during the specification
process. When these predicates are added to preconditions and postconditions they create additional
proof obligations for them in callers and callees (respectively) that are frequently checked at run
time. Similarly, when they are added to predicate bodies any proof obligations for the enclosing
predicate that are checked at run time become far more expensive. Fortunately, folding or unfolding
a predicate can decrease run-time cost when doing so discharges such proof obligations statically
Gradual C0                                                                                           1:35


(as seen in the right sub-figure). Therefore, users of Gradual C0 may consider specifying proofs of
recursive predicates in frequently-executed code to significantly reduce checking costs.
   Removing ? from preconditions, postconditions, and predicate bodies when the costly owned
fields passing strategy is still required in corresponding methods is the second most frequent
cause (27.9%) of increases in Gradual C0’s run-time overhead. This corresponds with the spikes
at 90% specified in Fig. 19 for Gradual C0: removal of ? in the aforementioned locations leads to
precise pre- and postconditions that trigger the use of this costly strategy. Eventually, a critical
mass of specifications are written so that when ?s are removed further this costly strategy is no
longer necessary (i.e. when callee methods are full statically verified) and so run-time performance
improves dramatically—the downward trends seen prior to full static specification in Fig. 19. This
is reflected in the right sub-figure in Fig. 20, where removing ? from preconditions, postconditions,
and predicate bodies is the most frequent cause (68.2%) of significant decreases in run-time overhead.
This suggests a strategy for avoiding high checking costs: specify frequently-executed code in
critical-mass chunks that are fully statically verifiable, leaving boundaries between statically and
dynamically verified code in places that are executed less frequently.
   Overall, the answer to RQ3 is yes; we have identified some key contributors to run-time overhead,
whose optimization is a promising direction for future work, and we have also identified strategies
for minimizing run time overhead in practice.
   Finally, all of the partial specification evaluated in our study were successfully verified by Gradual
C0. Since they originated from complete and correct specifications on code, we can conclude Gradual
C0 adheres to the gradual guarantee for these partial specifications and likely adheres to the gradual
guarantee for common use cases of Gradual C0.

   Threats to Validity. Our test programs were executed on multiple devices, each with the same CPU
and memory configuration. However, we did not otherwise control for differences in performance
between devices. While the test programs we used are of sufficient complexity to demonstrate
interesting empirical trends, they are not representative of all software. Further, the baseline we
used for dynamic verification is entirely unoptimized as we naively insert a check for each written
element of a specification. Finally, due to computational constraints, only a small subset of over
2100 possible imprecise specifications were sampled, and we did not use a formal criteria to choose
our workload values. As such, while our results reveal interesting trends, including significant
performance improvements by Gradual C0 over dynamic verification, more work is needed to
validate the robustness of those trends.

5.5   Qualitative Experience with AVL Tree
Notably, it was our experience that the incrementality of gradual verification was very helpful for
developing a complete specification of the AVL tree example. In particular, a run-time verification
error from a partial specification helped us realize the contract for the rotateRight helper function
was not general enough. We fully specified rotateRight and proved it correct. However, insert’s pre-
and postconditions were left as ?, and so static verification could not show us that the contract proved
for rotateRight was insufficiently general. Nevertheless, we ran the program; gradual verification
inserted run-time checks, and the precondition for rotateRight failed. This early notification
allowed us to identify the problem with the specification and fix it immediately. Otherwise, we
would have had to get deep into the static verification of insert—a complicated function, 50 lines
long, with lots of tricky logic and invariants—before discovering the error, and a lot of verification
work built on the faulty specification would have had to be redone. Interestingly, it is conventional
wisdom that one of the benefits of static checking is that you get feedback early, when it is easier to
correct mistakes. Here, we encountered a scenario where gradual verification had a similar benefit
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:36                                                                                                           Aldrich

over static verification! We found an error (in a specification) earlier than we would have otherwise,
presumably saving time.

6   RELATED WORK
Much of the closely related work, particularly work on gradual verification [Bader et al. 2018;
Wise et al. 2020; Zimmerman et al. 2024], gradual typing [Herman et al. 2010; Siek and Taha 2006;
Siek et al. 2015; Takikawa et al. 2016], and static verification [Müller et al. 2016; Parkinson and
Bierman 2005; Reynolds 2002; Smans et al. 2009], has been discussed throughout the paper. Note,
this paper and Zimmerman et al. [2024]’s paper have distinct contributions. Our work includes
the original development of symbolic execution based gradual verification and describes the first
implementation of the same, as well as related empirical results. Zimmerman et al. [2024]’s paper
proves that the approach is sound. Now, we discuss additional related work.

   Gradual typing. Additional related work in gradual typing includes richer type systems such
as gradual refinement types [Lehmann and Tanter 2017] and gradual dependent types [Eremondi
et al. 2019; Lennon-Bertrand et al. 2022]. These systems focus on pure functional programming,
while Gradual C0 targets imperative programs. There is an extensive body of work on optimizing
run-time checks in gradual type systems. Muehlboeck and Tate [2017] show that in languages with
nominal type systems, such as Java, gradual typing does not exhibit the usual slowdowns induced by
structural types. Feltey et al. [2018] reduce run-time overhead from redundant contract checking by
contract wrappers. They eliminate unnecessary contract checking by determining—across multiple
contract checking boundaries for some datatype or function call—whether some of the contracts
being checked imply others. While the results in §5 are promising, we may be able to draw from
the extensive body of work in gradual typing to achieve further performance gains.

   Static verification. Work in formal verification contains approaches that try to reduce the spec-
ification burden of users—a goal of Gradual C0. Furia and Meyer [2010] infer loop invariants
with heuristics that weaken postconditions into invariants. When that approach fails, verification
also fails because invariants are missing. Similarly, several tools (Smallfoot [Berdine et al. 2006],
jStar [Distefano and Parkinson J 2008], and Chalice [Leino et al. 2009]) use heuristics to infer
fold and unfold statements for verification. In contrast, Gradual C0 does not fail solely because
invariants, folds, or unfolds are missing; imprecision begets optimism. However, Gradual C0 may
benefit from similar heuristic approaches by leveraging additional static information to further
reduce run-time overhead.
   Abductive reasoning (abductive inference) tries to find an explanatory hypothesis for a desired
outcome [Dillig et al. 2012]. In static verification, the desired outcome is a proof obligation (𝑂),
facts (𝐹 ) are invariants derived from the program and specifications using some analysis, and the
explanatory hypothesis (𝐸) are invariants that do not contradict the derived facts (SAT(𝐹 ∧ 𝐸)) and
are required to discharge the proof obligation (𝐹 ∧𝐸 |= 𝑂). Ideally, 𝐹 should be sufficient to discharge
𝑂, but missing or insufficient specifications often results in 𝐹 being too weak to prove 𝑂 leading
to false positives (alarms) in tools. So, work in applying abductive reasoning to static verification
[Blackshear and Lahiri 2013; Calcagno et al. 2009; Chandra et al. 2009; Das et al. 2015; Dillig et al.
2012] aims to compute 𝐸 in order to prioritize—with minimal human intervention—verification
failures caused by bugs in a program and de-emphasize false positives (alarms) caused by missing or
incomplete specifications. In angelic verification [Blackshear and Lahiri 2013; Das et al. 2015] and
Calcagno et al. [2009]’s work, entire specifications, such as preconditions, postconditions, and loop
invariants are generated as explanatory hypotheses. Dillig et al. [2012] instead compute smaller,
intermediate formulas as explanatory hypotheses.
Gradual C0                                                                                               1:37


   Similar to prior abductive reasoning work [Blackshear and Lahiri 2013; Calcagno et al. 2009; Das
et al. 2015; Dillig et al. 2012], Gradual C0’s static system reasons around missing or incomplete
specifications to compute facts 𝐹 as part of imprecise formulas ? ∧ 𝐹 . At proof obligations, we
approximate the weakest formula that can replace ? in ? ∧ 𝐹 |= 𝑂 and SAT( ? ∧ 𝐹 ) successfully.
So, like Dillig et al. [2012] we compute intermediate explanatory hypotheses rather than whole
specifications like Blackshear and Lahiri [2013], Calcagno et al. [2009], and Das et al. [2015]. But,
rather than relying on users to validate generated hypotheses [Blackshear and Lahiri 2013; Calcagno
et al. 2009; Das et al. 2015; Dillig et al. 2012], we check their correctness at run time. This significantly
simplifies their computation—since they do not need to be human readable and can statically mark
code as unreachable—and allows Gradual C0 to be sound (prior abduction work is not).

   Dynamic verification. Meyer [1988] introduced the Eiffel language, which automatically performs
dynamic verification of pre- and postconditions and class invariants in first order logic. Nguyen
et al. [2008] extended dynamic verification to support separation logic assertions. More recently,
Agten et al. [2015] applied dynamic checking at the boundaries between statically verified and
unverified code to guarantee that no assertion failures or invalid memory accesses occur at run
time in any verified code. Their approach improved on Nguyen et al. [2008]’s approach in terms
of performance by allowing unverified code to read arbitrary memory. Further, unlike Nguyen
et al. [2008], Agten et al. [2015]’s approach only needs access to verified code rather than the
entire codebase. As with Nguyen et al. [2008]’s work, Gradual C0 supports dynamic verification of
ownership and first order logic. Gradual C0 additionally supports run-time checking of recursive
predicates. Similarly to Agten et al. [2015], Gradual C0 applies dynamic checking at the boundaries
between verified and unverified code to protect verified code. However, in Gradual C0 unverified
code must be accessible to the verifier as it is gradually verified as well. Future work in gradual
verification should incorporate insights from Agten et al. [2015]’s work to avoid requiring entire
codebases for verification and to improve verification performance.

   Hybrid verification. Another closely related work is soft contract verification [Nguyen et al. 2014],
which verifies dynamic contracts statically where possible and dynamically where necessary by
utilizing symbolic execution. This hybrid technique does not rely on a notion of precision, which
is central to gradual approaches and their metatheory [Siek et al. 2015]. Nguyen et al. [2014] use
symbolic execution results directly to discharge proof obligations where possible, while Gradual
C0 strengthens symbolic execution results to discharge proof obligations adhering to the theory
of imprecise formulas from Wise et al. [2020]. Further, Nguyen et al. [2014]’s work is targeted at
dynamic functional languages, while our work focuses on imperative languages. We also build in
memory safety as a default, while Nguyen et al. [2014] do not.

7   CONCLUSION
Gradual verification is a promising approach to supporting incrementality and enhance adoptability
of program verification. Users can focus on specifying and verifying the most important properties
and components of their systems and get immediate feedback about the consistency of their
specifications and the correctness of their code. By relying on symbolic execution, Gradual C0
overcomes several limitations of prior work on gradual verification of heap-manipulating programs.
The experimental results show that our approach can reduce overhead significantly compared to
purely dynamic checking and confirms performance trends speculated in prior work. While more
work remains to extend gradual verification (and Gradual C0) to the expressiveness of state-of-the-
art static program verifiers, we believe the symbolic-execution approach to gradual verification
shows promise to make verification more adoptable in software development practice.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:38                                                                                                           Aldrich

REFERENCES
Pieter Agten, Bart Jacobs, and Frank Piessens. 2015. Sound Modular Verification of C Code Executing in an Unverified
    Context. In Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages
    (Mumbai, India) (POPL ’15). Association for Computing Machinery, New York, NY, USA, 581–594. https://doi.org/10.
    1145/2676726.2676972
Rob Arnold. 2010. C0, an imperative programming language for novice computer scientists. Master’s thesis. Department of
    Computer Science, Carnegie Mellon University.
Johannes Bader, Jonathan Aldrich, and Éric Tanter. 2018. Gradual Program Verification. In International Conference on
    Verification, Model Checking, and Abstract Interpretation. Springer, 25–46.
Josh Berdine, Cristiano Calcagno, and Peter W O’hearn. 2006. Smallfoot: Modular automatic assertion checking with
    separation logic. In Formal Methods for Components and Objects: 4th International Symposium, FMCO 2005, Amsterdam,
    The Netherlands, November 1-4, 2005, Revised Lectures 4. Springer, 115–137.
Sam Blackshear and Shuvendu K Lahiri. 2013. Almost-correct specifications: A modular semantic framework for assigning
    confidence to warnings. In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and
    Implementation. 209–218.
Cristiano Calcagno, Dino Distefano, Peter O’Hearn, and Hongseok Yang. 2009. Compositional shape analysis by means of
    bi-abduction. In Proceedings of the 36th annual ACM SIGPLAN-SIGACT symposium on Principles of programming languages.
    289–300.
John Peter Campora, Sheng Chen, and Eric Walkingshaw. 2018. Casts and costs: harmonizing safety and performance in
    gradual typing. PACM on Programming Languages 2, ICFP (Sept. 2018), 98:1–98:30.
Satish Chandra, Stephen J Fink, and Manu Sridharan. 2009. Snugglebug: a powerful approach to weakest preconditions. In
    Proceedings of the 30th ACM SIGPLAN Conference on Programming Language Design and Implementation. 363–374.
Ankush Das, Shuvendu K Lahiri, Akash Lal, and Yi Li. 2015. Angelic verification: Precise verification modulo unknowns. In
    Computer Aided Verification: 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceedings,
    Part I 27. Springer, 324–342.
Edsger W. Dijkstra. 1975. Guarded Commands, Nondeterminacy and Formal Derivation of Programs. Commun. ACM 18, 8
    (August 1975), 453–457.
Isil Dillig, Thomas Dillig, and Alex Aiken. 2012. Automated error diagnosis using abductive inference. ACM SIGPLAN
    Notices 47, 6 (2012), 181–192.
Dino Distefano and Matthew J Parkinson J. 2008. jStar: Towards practical verification for Java. ACM Sigplan Notices 43, 10
    (2008), 213–226.
Joseph Eremondi, Éric Tanter, and Ronald Garcia. 2019. Approximate Normalization for Gradual Dependent Types. Proc.
    ACM Program. Lang. 3, ICFP, Article 88 (jul 2019), 30 pages. https://doi.org/10.1145/3341692
Daniel Feltey, Ben Greenman, Christophe Scholliers, Robert Bruce Findler, and Vincent St-Amour. 2018. Collapsible
    Contracts: Fixing a Pathology of Gradual Typing. Proc. ACM Program. Lang. 2, OOPSLA, Article 133 (oct 2018), 27 pages.
    https://doi.org/10.1145/3276503
Carlo Alberto Furia and Bertrand Meyer. 2010. Inferring loop invariants using postconditions. In Fields of logic and
    computation. Springer, 277–300.
David Herman, Aaron Tomb, and Cormac Flanagan. 2010. Space-efficient gradual typing. 23, 2 (June 2010), 167–189.
Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
    powerful, sound, predictable, fast verifier for C and Java. In NASA Formal Methods Symposium. Springer, 41–55.
James C. King. 1976. Symbolic Execution and Program Testing. Commun. ACM 19, 7 (July 1976), 385–394.
Nico Lehmann and Éric Tanter. 2017. Gradual Refinement Types. SIGPLAN Not. 52, 1 (jan 2017), 775–788. https:
    //doi.org/10.1145/3093333.3009856
K Rustan M Leino, Peter Müller, and Jan Smans. 2009. Verification of concurrent programs with Chalice. In Foundations of
    Security Analysis and Design V. Springer, 195–222.
Meven Lennon-Bertrand, Kenji Maillard, Nicolas Tabareau, and Éric Tanter. 2022. Gradualizing the Calculus of Inductive
    Constructions. ACM Transactions on Programming Languages and Systems 44, 2 (June 2022). https://doi.org/10.1145/
    3495528
Bertrand Meyer. 1988. Eiffel: A language and environment for software engineering. Journal of Systems and Software 8, 3
    (1988), 199–246.
Fabian Muehlboeck and Ross Tate. 2017. Sound Gradual Typing is Nominally Alive and Well. Proc. ACM Program. Lang. 1,
    OOPSLA, Article 56 (oct 2017), 30 pages. https://doi.org/10.1145/3133880
P. Müller, M. Schwerhoff, and A. J. Summers. 2016. Viper: A Verification Infrastructure for Permission-Based Reasoning. In
    Verification, Model Checking, and Abstract Interpretation (VMCAI) (LNCS, Vol. 9583), B. Jobstmann and K. R. M. Leino
    (Eds.). Springer-Verlag, 41–62.
Gradual C0                                                                                                         1:39


Huu Hai Nguyen, Viktor Kuncak, and Wei-Ngan Chin. 2008. Runtime checking for separation logic. In International
   Workshop on Verification, Model Checking, and Abstract Interpretation. Springer, 203–217.
Phúc C. Nguyen, Sam Tobin-Hochstadt, and David Van Horn. 2014. Soft Contract Verification. In Proceedings of the 19th
   ACM SIGPLAN International Conference on Functional Programming (Gothenburg, Sweden) (ICFP ’14). Association for
   Computing Machinery, New York, NY, USA, 139–152. https://doi.org/10.1145/2628136.2628156
Matthew Parkinson and Gavin Bierman. 2005. Separation logic and abstraction. In ACM SIGPLAN Notices, Vol. 40. ACM,
   247–258.
John C Reynolds. 2002. Separation logic: A logic for shared mutable data structures. In Logic in Computer Science, 2002.
   Proceedings. 17th Annual IEEE Symposium on. IEEE, 55–74.
Malte H Schwerhoff. 2016. Advancing automated, permission-based program verification using symbolic execution. Ph. D.
   Dissertation. ETH Zurich.
Jeremy G Siek and Walid Taha. 2006. Gradual typing for functional languages. In Scheme and Functional Programming
   Workshop, Vol. 6. 81–92.
Jeremy G Siek, Michael M Vitousek, Matteo Cimini, and John Tang Boyland. 2015. Refined criteria for gradual typing. In
   LIPIcs-Leibniz International Proceedings in Informatics, Vol. 32. Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik.
Jan Smans, Bart Jacobs, and Frank Piessens. 2009. Implicit dynamic frames: Combining dynamic frames and separation
   logic. In European Conference on Object-Oriented Programming. Springer, 148–172.
Alexander J Summers and Sophia Drossopoulou. 2013. A formal semantics for isorecursive and equirecursive state
   abstractions. In European Conference on Object-Oriented Programming. Springer, 129–153.
Asumu Takikawa, Daniel Feltey, Ben Greenman, Max S. New, Jan Vitek, and Matthias Felleisen. 2016. Is Sound Gradual
   Typing Dead? SIGPLAN Not. 51, 1 (jan 2016), 456–468. https://doi.org/10.1145/2914770.2837630
Jenna Wise, Johannes Bader, Cameron Wong, Jonathan Aldrich, Éric Tanter, and Joshua Sunshine. 2020. Gradual verification
   of recursive heap data structures. Proceedings of the ACM on Programming Languages 4, OOPSLA (2020), 1–28.
Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound Gradual Verification with Symbolic Execution.
   Proceedings of the ACM on Programming Languages 8, POPL (2024), 2547–2576.
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:40                                                                                                           Aldrich

A    APPENDIX

                            pc-add(𝜋, 𝑡 ) = Let (𝑖𝑑, 𝑏𝑐, 𝑝𝑐𝑠 ) :: suffix match 𝜋
                                (𝑖𝑑, 𝑏𝑐, 𝑝𝑐𝑠 ∪ {𝑡 } ) :: suffix
                            pc-push(𝜋, 𝑖𝑑, 𝑏𝑐 ) = (𝑖𝑑, 𝑏𝑐, ∅ ) :: 𝜋
                            pc-all(𝜋 ) = foldl(𝜋, ∅, (𝜆 (𝑖𝑑𝑖 , 𝑏𝑐𝑖 , 𝑝𝑐𝑠𝑖 ), 𝑎𝑙𝑙𝑖 . 𝑎𝑙𝑙𝑖 ∪ {𝑏𝑐𝑖 } ∪ 𝑝𝑐𝑠𝑖 ) )

                                                Fig. 21. Path condition helper functions



        eval-p(𝜎, 𝑡, 𝑄 )          = 𝑄 (𝜎, 𝑡 )
        eval-p(𝜎, 𝑥, 𝑄 )          = 𝑄 (𝜎, 𝜎 .𝛾 (𝑥 ) )
        eval-p(𝜎1 , 𝑜𝑝 (𝑒 ), 𝑄 ) = eval-p(𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . 𝑄 (𝜎2 , 𝑜𝑝 ′ (𝑡 ) ) ) )
        eval-p(𝜎1 , 𝑒.𝑓 , 𝑄 )     = eval-p(𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .
                                    if (∃ 𝑓 (𝑟 ; 𝛿 ) ∈ 𝜎2 .ℎ . check(𝜎2 .𝜋, 𝑟 = 𝑡 ) ) then
                                      𝑄 (𝜎2 , 𝛿 )
                                    else if (∃ 𝑓 (𝑟 ; 𝛿 ) ∈ 𝜎2 .ℎ ? . check(𝜎2 .𝜋, 𝑟 = 𝑡 ) ) then
                                      𝑄 (𝜎2 , 𝛿 )
                                    else if (𝜎2 .isImprecise ) then

                                       if (𝜎2 .R.origin = ( _, unfold acc ( _ ), _ ) ) then

                                         𝑒𝑡 := translate (𝜎2 , 𝑡 )

                                          R ′ := addcheck (𝜎2 .R, 𝑒.𝑓 , acc (𝑒𝑡 .𝑓 ) )
                                       else

                                          R ′ := 𝜎2 .R
                                      𝛿 := fresh
                                      𝑄 (𝜎2 { ℎ ? := 𝜎2 .ℎ ? ∪ 𝑓 (𝑡 ; 𝛿 ), 𝜋 := pc-add(𝜎2 .𝜋, {𝑡 ≠ null } ), R := R ′ }, 𝛿 )
                                    else failure())

Fig. 22. Rules for symbolically executing expressions without introducing run-time checks (except for a special case for
unfold)


In eval-p (Fig. 22), a special case (highlighted in blue) for unfold statements is added that creates
run-time checks for field accesses in the unfolded predicate’s body. This case ensures soundness
when introducing branch condition variables in C0 programs during run-time verification. In our
implementation of Gradual C0, these checks are optimized further as they are only produced for
branch conditions in the predicate body rather than for the whole body.
Gradual C0                                                                                                             1:41


                      eval-c(𝜎, 𝑡, 𝑄 )         = 𝑄 (𝜎, 𝑡 )
                      eval-c(𝜎, 𝑥, 𝑄 )         = 𝑄 (𝜎, 𝜎 .𝛾 (𝑥 ) )
                      eval-c(𝜎1 , 𝑜𝑝 (𝑒 ), 𝑄 ) = eval-c(𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . 𝑄 (𝜎2 , 𝑜𝑝 ′ (𝑡 ) ) ) )
                      eval-c(𝜎1 , 𝑒.𝑓 , 𝑄 )    = eval-c(𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .
                                                 if (∃ 𝑓 (𝑟 ; 𝛿 ) ∈ 𝜎2 .ℎ . check(𝜎2 .𝜋, 𝑟 = 𝑡 ) ) then
                                                   𝑄 (𝜎2 , 𝛿 )
                                                 else if (∃ 𝑓 (𝑟 ; 𝛿 ) ∈ 𝜎2 .ℎ ? . check(𝜎2 .𝜋, 𝑟 = 𝑡 ) ) then
                                                   𝑄 (𝜎2 , 𝛿 )
                                                 else if (𝜎2 .isImprecise ) then
                                                   𝑟𝑒𝑠, _ := assert(𝜎2 .isImprecise, 𝜎2 .𝜋, 𝑡 ≠ null)
                                                   𝑒𝑡 := translate (𝜎2 , 𝑡 )
                                                    R ′ := addcheck (𝜎2 .R, 𝑒.𝑓 , acc (𝑒𝑡 .𝑓 ) )
                                                   𝑟𝑒𝑠 ∧ 𝑄 (𝜎2 { R := R ′ }, fresh )
                                                 else failure())

      Fig. 23. Rules for symbolically executing expressions without modifying the optimistic heap and path condition



A.1      Diff and Translate


Algorithm 1 Generating minimal checks

 1: function Diff(𝜙)
 2:    𝑐𝑜𝑛 𝑗𝑢𝑛𝑐𝑡𝑠 ← 𝐶𝑁 𝐹 (𝜙)
 3:    𝜙′ ← ∅
 4:    for 𝑐 ← 𝑐𝑜𝑛 𝑗𝑢𝑛𝑐𝑡𝑠 do
 5:       if !𝑐ℎ𝑒𝑐𝑘 (𝑐) then
 6:          𝜙′ ← 𝜙′ + 𝑐
 7:       end if
 8:    end for
 9:    return 𝜙 ′
10: end function


                          Fig. 24. Algorithm for computing the diff between two symbolic values


   The diff (Fig. 24) function finds a minimal run-time check from an optimistically asserted
formula containing statically known information. It accomplishes this by first performing a standard
transformation to conjunctive normal form (CNF) on the optimistically asserted formula, to extract
the maximal number of top level conjuncts. It then attempts to call check() on each conjunct; it
accumulates each conjunct for which the call does not succeed. The set of conjuncts which could
not be statically discharged are returned as the final check.
   The translate (Fig. 25) function lifts symbolic values to concrete values. Most symbolic values
are directly translated to their concrete counterparts via recursive descent; the exception is variables,
whose concrete values must be reconstructed by searching the program state known by the verifier.
This is done by retrieving the states of the symbolic store, which contains mappings from concrete
variables to symbolic variables, and the heap, which contains field and predicate permissions. When
translate encounters a symbolic variable, it first retrieves all possible aliasing information from
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:42                                                                                                           Aldrich



Algorithm 2 Variable resolution procedure
 1: function Translate-var(𝑠, 𝑣)
 2:    𝑠𝑡𝑜𝑟𝑒 ← ∅
 3:    if 𝑠.𝑜𝑙𝑑𝑆𝑡𝑜𝑟𝑒 then
 4:        𝑠𝑡𝑜𝑟𝑒 ← 𝑠.𝑜𝑙𝑑𝑆𝑡𝑜𝑟𝑒
 5:    else
 6:        𝑠𝑡𝑜𝑟𝑒 ← 𝑠.𝑠𝑡𝑜𝑟𝑒
 7:    end if
 8:    𝑎𝑙𝑖𝑎𝑠𝐿𝑖𝑠𝑡 ← 𝑎𝑙𝑖𝑎𝑠𝑒𝑠 (𝑣, 𝑠.𝑝𝑎𝑡ℎ𝐶𝑜𝑛𝑑𝑖𝑡𝑖𝑜𝑛𝑠 + +𝑠.ℎ𝑒𝑎𝑝 + +𝑠.𝑜𝑝𝑡𝑖𝑚𝑖𝑠𝑡𝑖𝑐𝐻𝑒𝑎𝑝)
 9:    ℎ𝑒𝑎𝑝 ← 𝑠.ℎ𝑒𝑎𝑝 + +𝑠.𝑜𝑝𝑡𝑖𝑚𝑖𝑠𝑡𝑖𝑐𝐻𝑒𝑎𝑝
10:    𝑜𝑢𝑡𝑝𝑢𝑡𝑠 ← ∅
11:    for 𝑣 ← 𝑎𝑙𝑖𝑎𝑠𝐿𝑖𝑠𝑡 do
12:        if 𝑐 ← 𝑠𝑡𝑜𝑟𝑒.𝑙𝑜𝑜𝑘𝑢𝑝 (𝑣) then
13:            𝑜𝑢𝑡𝑝𝑢𝑡𝑠 ← 𝑜𝑢𝑡𝑝𝑢𝑡𝑠 + 𝑐
14:        else
15:            if ℎ ← ℎ𝑒𝑎𝑝.𝑙𝑜𝑜𝑘𝑢𝑝 (𝑣)&&𝑐 ← 𝑠𝑡𝑜𝑟𝑒.𝑙𝑜𝑜𝑘𝑢𝑝 (ℎ) then
16:               𝑜𝑢𝑡𝑝𝑢𝑡𝑠 ← 𝑜𝑢𝑡𝑝𝑢𝑡𝑠 + 𝑐
17:            end if
18:        end if
19:    end for
20:    return 𝑠𝑒𝑙𝑒𝑐𝑡𝐿𝑜𝑛𝑔𝑒𝑠𝑡 (𝑜𝑢𝑡𝑝𝑢𝑡𝑠)
21: end function


                                 Fig. 25. Translate’s procedure for resolving variables


Gradual Viper’s state. This includes all variables known to be equivalent to the translation target
according to the path condition and the heap. If the translation target or one of its aliases exists
as a value in the symbolic store, then the translator finds a key corresponding to it in the store
and returns it. Note that multiple valid keys may exist for a particular symbolic variable, because
Gradual Viper may have determined that multiple concrete values are equivalent at a particular
program point. If the translation target is a field, then only the top level receiver (the variable on
which fields are being accessed) or one of its aliases will exist in the store. The fields being accessed
are resolved by mapping their corresponding heap entries, or any aliased heap entries, to a value in
the symbolic store, and resolving the store entry as described. In particular contexts, translate
may be asked to translate a precondition for a method call, or a predicate body for an (un)fold
statement. In these cases, an old store attached to the current symbolic state as described in 4.3.7
is retrieved, and its symbolic store and heap are used for translation. This causes variables in a
precondition or predicate to be resolved to their concrete values at the call site, or site of unfolding.
This enables run-time checks produced via translate to be straightforwardly emitted to the frontend.
The portion of translate related to translating variables is shown in Fig. 25.

A.2 Symbolic production of formulas
The rules for produce are given in Fig. 11. Essentially, produce takes a formula and snapshot 𝛿
(mirroring the structure of the formula) and adds the information in the formula to the symbolic
state, which is then returned to the continuation 𝑄. An imprecise formula ? &&𝜙 has its static part 𝜙
produced into the current state 𝜎 alongside second(𝛿 ). Note the snapshot 𝛿 for an imprecise formula
Gradual C0                                                                                           1:43


looks like (𝑢𝑛𝑖𝑡, second(𝛿 )) where 𝑢𝑛𝑖𝑡 is the snapshot for ? and second(𝛿 ) is the snapshot for 𝜙.
An imprecise formula also turns 𝜎 imprecise to produce the unknown information represented by ?
into 𝜎. For example, if the state is represented by the formula 𝜃 , then this rule results in ? &&𝜃 && 𝜙.
A symbolic value 𝑡 is produced into the path condition of the current state 𝜎. Also, the snapshot 𝛿
for 𝑡 must be 𝑢𝑛𝑖𝑡, so this fact is also stored in 𝜎’s path condition. Then, 𝜎 is passed to 𝑄.
   The produce rule for expression 𝑒, first evaluates 𝑒 to its symbolic value 𝑡 using eval-p. Then,
𝑡 is produced into the path condition of the current state 𝜎2 using the aforementioned symbolic
value rule. Imprecision in the symbolic state can always provide accessibility predicates for fields
also in the state. Therefore, when fields in 𝑒 are added to an imprecise state, heap chunks for those
fields do not have to already be in the state, e.g. the state ? && true becomes ? && true && 𝑒. This
functionality is permitted by eval-p. Similarly, an imprecise formula always provides accessibility
predicates for fields in its static part, e.g. the state true and produced formula ? && 𝑒 results in
the state ? && true && 𝑒. The goal of produce is not to assert information in the state, but rather
add information to the state. So we reduce run-time overhead by ensuring no run-time checks are
produced by produce even for verifying field accesses.
   The rules for producing field and predicate accessibility predicates into the state 𝜎1 operate in a
very similar manner. Thus, we will focus on the rule for fields only. The field 𝑒.𝑓 in acc (𝑒.𝑓 ) first
has its receiver 𝑒 evaluated to 𝑡 by eval-pc, resulting in 𝜎2 . Then, using the parameter 𝛿 a fresh heap
chunk 𝑓 (𝑡; 𝛿 ) is created and added to 𝜎2 ’s heap ℎ, which represents acc (𝑒.𝑓 ) in the state. Note, the
disjoint union ⊎ ensures 𝑓 (𝑡; 𝛿 ) is not already in the heap before adding 𝑓 (𝑡; 𝛿 ) in there. If the
chunk is in the heap, then verification will fail. Further, acc (𝑒.𝑓 ) implies 𝑒 ≠ null and so that fact
is recorded in 𝜎2 ’s path condition as 𝑡 ≠ null.
   When the separating conjunction 𝜙 1 && 𝜙 2 is produced, 𝜙 1 is first produced and then afterwards
𝜙 2 is produced into the resulting symbolic state. Note that the snapshot 𝛿 is split between the two
formulas using first(𝛿 ) and second(𝛿 ). Finally, to produce a conditional, Gradual Viper branches
on the symbolic value 𝑡 for the condition 𝑒 splitting execution along two different paths. Along
one path only the true branch 𝜙 1 is produced into the state, and along the other path only the false
branch 𝜙 2 is produced. Both paths follow the continuation to the end of its execution. More details
about branching are provided next, as we describe Gradual Viper’s branch function.
   The branch function in Fig. 12 is used to split the symbolic execution into two paths in a
number of places in our algorithm: during the production or consumption of logical conditionals
and during the execution of if statements. One path (𝑄𝑡 ) is taken under the assumption that the
parameter 𝑡 is true, and the other (𝑄 ¬𝑡 ) is taken under the assumption that 𝑡 is false. For each path,
a branch condition corresponding to the assumption made is added to 𝜎.R, as highlighted in blue.
Additionally, paths may be pruned using check when Gradual Viper knows for certain a path is
infeasible (the assumption about 𝑡 would contradict the current path conditions). Now, normally,
if either of the two paths fail verification, then branch marks verification as failed (∧ the results).
This is still true when 𝜎 (the current state) is precise. However, when 𝜎 is imprecise, branch can be
more permissive as highlighted in yellow. If verification fails on one of two paths only (one success,
one failure), then branch returns success (∨ the results). In this case, a run-time check (highlighted
in blue) is added to ℜ to force run-time execution down the success path only. Of course, two
failures result in failure and two successes result in success (∨ the results). No run-time checks
are produced in these cases, as neither path can be soundly taken or both paths can be soundly
taken at run time respectively. Note that Gradual Viper being flexible in the aforementioned way
is critical to adhering to the gradual guarantee at branch points.

A.3   Symbolic consumption of formulas
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:44                                                                                                           Aldrich

           consume(𝜎1 , 𝜃, 𝑄 )        = 𝜎2 := 𝜎1 { ℎ, 𝜋 := consolidate(𝜎1 .ℎ, 𝜎1 .𝜋 ) }

                                       consume’(𝜎2 , 𝜎2 .isImprecise , 𝜎2 .ℎ ? , 𝜎2 .ℎ, 𝜃, (𝜆 𝜎3 , ℎ ?′ , ℎ 1 , 𝛿 1 .

                                         𝑄 (𝜎3 { ℎ ? := ℎ ?′ , ℎ := ℎ 1 }, 𝛿 1 ) ) )

           consume(𝜎1 , ? && 𝜙, 𝑄 ) = 𝜎2 := 𝜎1 { ℎ, 𝜋 := consolidate(𝜎1 .ℎ, 𝜎1 .𝜋 ) }

                                       consume’(𝜎2 , true , 𝜎2 .ℎ ? , 𝜎2 .ℎ, 𝜙, (𝜆 𝜎3 , ℎ ?′ , ℎ 1 , 𝛿 1 .

                                         𝑄 (𝜎3 { isImprecise := true, ℎ ? := ∅, ℎ := ∅ }, 𝑝𝑎𝑖𝑟 (𝑢𝑛𝑖𝑡, 𝛿 1 ) ) ) )

                  ■   Handles imprecision      ■     Handles run-time check generation and collection

                                 Fig. 26. Rules for symbolically consuming formulas (1/3)


    The goals of consume are 3-fold: 1) given a symbolic state 𝜎 and formula 𝜙e check whether 𝜙e is
established by 𝜎, i.e. 𝜙e𝜎 ⇒
                           f 𝜙e where 𝜙e𝜎 is the formula which represents the state 𝜎, 2) produce and
collect run-time checks that are minimally sufficient for 𝜎 to establish 𝜙e soundly, and 3) remove
accessibility predicates and predicates that are asserted in 𝜙e from 𝜎. Note that ⇒    f is the consistent
implication formally defined by Wise et al. [2020]. The rules for consume are given in Fig. 26.
    The consume function always begins by consolidating information across the given heap 𝜎1 .ℎ and
path condition 𝜎1 .𝜋. The invariant on the heap 𝜎1 .ℎ ensures all heap chunks in 𝜎1 .ℎ are separated in
memory, e.g. 𝑓 (𝑥; 𝛿 1 ) ∈ 𝜎1 .ℎ and 𝑓 (𝑦; 𝛿 2 ) ∈ 𝜎1 .ℎ implies 𝑥 ≠ 𝑦. Similarly, 𝑓 (𝑥; 𝛿 1 ) ∈ 𝜎1 .ℎ implies
𝑥 ≠ null. Therefore, such information is added to the path condition 𝜎1 .𝜋 during consolidation. Fur-
ther, consolidate ensures 𝜎1 .ℎ and 𝜎1 .𝜋 are consistent, i.e. do not contain contradictory information.
We use the definition of consolidate from [Schwerhoff 2016], without repeating it here.
    After consolidation, consume calls a helper function consume’, which performs the major
functionality of consume. Along with the state 𝜎2 from consolidation, consume’ accepts a boolean
flag, optimistic heap 𝜎2 .ℎ ? , regular heap 𝜎2 .ℎ, the formula to be consumed 𝜙,    e and a continuation.
The boolean flag sent to consume’ controls how 𝜎2 provides access to fields in 𝜙.      e When 𝜙e is precise
(is 𝜃 ), then 𝜎2 provides access to fields in 𝜃 through heap chunks or imprecision where applicable.
Therefore, in this case, the boolean flag is set to 𝜎2 .isImprecise. However, when 𝜙e is imprecise
(i.e. ? && 𝜙), then the boolean flag is set to true so access to fields in 𝜙e is always justified: first by
𝜎2 if applicable and second by imprecision in 𝜙.     e Copies of the optimistic heap 𝜎2 .ℎ ? and regular
heap 𝜎2 .ℎ are sent to consume’ where heap chunks from 𝜙e are removed from them. If consume’
succeeds, then when 𝜙e is precise execution continues with the residual heap chunks. When 𝜙e is
imprecise execution continues with empty heaps, because 𝜙e may require and assert any heap chunk
in 𝜎2 . Residual heap chunks are instead represented by imprecision, i.e. execution continues with
an imprecise state. Finally, consume’ also sends snapshots collected for removed heap chunks to
the continuation.
    Rules for consume’ can also be found in Fig. 26. Cases for expressions 𝑒, the separating conjunction
𝜙 1 && 𝜙 2 , and logical conditionals 𝑒 ? 𝜙 1 : 𝜙 2 are straightforward. Expressions are evaluated to
symbolic values that are then consumed with the corresponding rule. In a separating conjunction,
𝜙 1 is consumed first, then afterward 𝜙 2 is consumed. The rule for logical conditionals evaluates the
condition 𝑒 to a symbolic value, and then uses the branch function to consume 𝜙 1 and 𝜙 2 along
different execution paths. The case for acc (𝑝 (𝑒)) is also very similar to the case for acc (𝑒.𝑓 ) that
we discuss later in this section.
    When a symbolic value 𝑡 is consumed, the current state 𝜎 must establish 𝑡, i.e. 𝜎 ⇒      f 𝑡, or verifica-
tion fails. The assert function (defined in Fig. 28) implements this functionality. In particular, assert
returns success() when 𝜋 can statically prove 𝑡 or when 𝜎 is imprecise and 𝑡 does not contradict
Gradual C0                                                                                                                               1:45


  consume’(𝜎,     𝑓? , ℎ ? , ℎ, ( 𝑒 , 𝑡 ), 𝑄 )    = 𝑟𝑒𝑠, 𝑡 := assert(𝜎 .isImprecise, 𝜎 .𝜋, 𝑡 )

                                                    R ′ := addcheck (𝜎 .R, 𝑒, translate (𝜎, 𝑡 ) )

                                                   𝑟𝑒𝑠 ∧ 𝑄 (𝜎 { R := R ′ }, ℎ ? , ℎ, 𝑢𝑛𝑖𝑡 )
  consume’(𝜎1 ,   𝑓? , ℎ ? , ℎ, 𝑒, 𝑄 )            = eval-c (𝜎1 { isImprecise := 𝑓? }, 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                 consume’(𝜎2 { isImprecise := 𝜎1 .isImprecise },           𝑓? , ℎ ? , ℎ, ( 𝑒 , 𝑡 ), 𝑄 ) ) )

  consume’(𝜎1 ,   𝑓? , ℎ ? , ℎ, acc (𝑝 (𝑒 ) ), 𝑄 ) = eval-c (𝜎1 { isImprecise := 𝑓? }, 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                    𝜎3 := 𝜎2 { isImprecise := 𝜎1 .isImprecise }

                                                    (ℎ 1 , 𝛿 1 , 𝑏 1 ) := heap-rem-pred(𝜎3 .isImprecise, ℎ, 𝜎3 .𝜋, 𝑝 (𝑡 ) )

                                                    if (𝜎3 .isImprecise ) then

                                                       (ℎ ?′ , 𝛿 2 , 𝑏 2 ) := heap-rem-pred(𝜎3 .isImprecise, ℎ ? , 𝜎3 .𝜋, 𝑝 (𝑡 ) )

                                                       if (𝑏 1 = 𝑏 2 = false ) then

                                                         R ′ := addcheck (𝜎3 .R, acc (𝑝 (𝑒 ) ), acc (𝑝 (𝑒 ) ) )

                                                       else R ′ := 𝜎3 .R

                                                       𝑄 (𝜎3 { R := R ′ }, ℎ ?′ , ℎ 1 , ( if (𝑏 1 ) then 𝛿 1 else 𝛿 2 ) )

                                                    else if (𝑏 1 ) then 𝑄 (𝜎3 , 𝜎3 .ℎ ? , ℎ 1 , 𝛿 1 )

                                                    else failure() ) )

  consume’(𝜎1 ,   𝑓? , ℎ ? , ℎ, acc (𝑒.𝑓 ), 𝑄 ) = eval-c (𝜎1 { isImprecise := 𝑓? }, 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                    𝜎3 := 𝜎2 { isImprecise := 𝜎1 .isImprecise }

                                                   𝑟𝑒𝑠, 𝑡 := assert(𝜎3 .isImprecise, 𝜎3 .𝜋, 𝑡 ≠ null)
                                                   𝑟𝑒𝑠 ∧ (

                                                    R ′ := addcheck (𝜎3 .R, acc (𝑒.𝑓 ), translate (𝜎3 , 𝑡 ) )

                                                    (ℎ 1 , 𝛿 1 , 𝑏 1 ) := heap-rem-acc(𝜎3 .isImprecise, ℎ, 𝜎3 .𝜋, 𝑓 (𝑡 ) )

                                                    if (𝜎3 .isImprecise ) then

                                                       (ℎ ?′ , 𝛿 2 , 𝑏 2 ) := heap-rem-acc(𝜎3 .isImprecise, ℎ ? , 𝜎3 .𝜋, 𝑓 (𝑡 ) )

                                                       if (𝑏 1 = 𝑏 2 = false ) then

                                                         R ′′ := addcheck ( R ′ , acc (𝑒.𝑓 ), acc ( translate (𝜎3 , 𝑡 ).𝑓 ) )

                                                       else R ′′ := R ′

                                                       𝑄 (𝜎3 { R := R ′′ }, ℎ ?′ , ℎ 1 , ( if (𝑏 1 ) then 𝛿 1 else 𝛿 2 ) )

                                                    else if (𝑏 1 ) then 𝑄 (𝜎3 { R := R ′ }, 𝜎3 .ℎ ? , ℎ 1 , 𝛿 1 )

                                                    else failure() ) ) )

                    ■    Handles imprecision       ■    Handles run-time check generation and collection

                                    Fig. 26. Rules for symbolically consuming formulas (2/3)


constraints in 𝜋—here, 𝑡 is optimistically assumed to be true. Otherwise, assert returns failure().
When assert succeeds, it also returns a set of symbolic values 𝑡 that are residuals of 𝑡 that cannot be
proved statically by 𝜋. If 𝑡 is proven entirely statically, then assert returns true. A run-time check is
created for the residuals 𝑡 and is added to 𝜎 to be passed to the continuation 𝑄. Note that translate
is used to create an expression from 𝑡 that can be evaluated at run time. Further, the location 𝑒 is
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:46                                                                                                           Aldrich

          consume’(𝜎1 ,    𝑓? , ℎ ? , ℎ, 𝜙 1 && 𝜙 2 , 𝑄 )      = consume’(𝜎1 , 𝑓? , ℎ ? , ℎ, 𝜙 1 , (𝜆 𝜎2 , ℎ ?′ , ℎ ′ , 𝛿 1 .

                                                                consume’(𝜎2 ,        𝑓? , ℎ ?′ , ℎ ′ , 𝜙 2 , (𝜆 𝜎3 , ℎ ?′′ , ℎ ′′ , 𝛿 2 .

                                                                   𝑄 (𝜎3 , ℎ ?′′ , ℎ ′′ , 𝑝𝑎𝑖𝑟 (𝛿 1 , 𝛿 2 ) ) ) ) ) )

          consume’(𝜎1 ,    𝑓? , ℎ ? , ℎ, 𝑒 ? 𝜙 1 : 𝜙 2 , 𝑄 ) = eval-c (𝜎1 { isImprecise := 𝑓? }, 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                                 𝜎3 := 𝜎2 { isImprecise := 𝜎1 .isImprecise }
                                                                 branch (𝜎3 , 𝑒, 𝑡,

                                                                   (𝜆 𝜎4 . consume’(𝜎4 , 𝑓? , ℎ ? , ℎ, 𝜙 1 , 𝑄 ) ),

                                                                   (𝜆 𝜎4 . consume’(𝜎4 , 𝑓? , ℎ ? , ℎ, 𝜙 2 , 𝑄 ) ) ) ) )

                   ■      Handles imprecision       ■       Handles run-time check generation and collection

                                   Fig. 26. Rules for symbolically consuming formulas (3/3)

the expression that evaluates to 𝑡 and is passed to consume’ alongside 𝑡. The heaps ℎ ? and ℎ are
passed unmodified to 𝑄 alongside the snapshot 𝑢𝑛𝑖𝑡.
   The consume’ rule for accessibility predicates acc (𝑒.𝑓 ), first evaluates the receiver 𝑒 to 𝑡 using
eval-c, the current state 𝜎1 , and the parameter 𝑓? . The parameter 𝑓? is the boolean flag mentioned
previously. Assigning 𝑓? to 𝜎1 .isImprecise during evaluation allows 𝑓? to control whether or not
imprecision verifies field accesses. This occurs in all of the consume’ rules where expressions
and thus fields are evaluated. After evaluation, the isImprecise field is reset resulting in 𝜎3 , and
assert is used to ensure the receiver 𝑡 is non-null. If 𝑡 ≠ null is optimistically true, a run-time
check for 𝑡 ≠ null at location acc (𝑒.𝑓 ) is created and added to 𝜎3 .R. Next, heap-rem-acc is used to
remove the heap chunks from heap ℎ that overlap with or may potentially overlap with acc (𝑒.𝑓 ) in
memory. The heap-rem-acc function is formally defined alongside a similar function for predicates
(heap-rem-pred) in the Fig. 27. If a field chunk is not statically proven to be disjoint from acc (𝑒.𝑓 ),
then it is removed. Further, since predicates are opaque, Gradual Viper cannot tell whether or
not their predicate bodies overlap with acc (𝑒.𝑓 ). Therefore, predicate chunks are almost always
considered to potentially overlap with acc (𝑒.𝑓 ). The only time this is not the case is if they both
exist in the heap ℎ, which ensures its heap chunks do not overlap in memory. The heap-rem-acc
function also checks that acc (𝑒.𝑓 ) has a corresponding heap chunk in ℎ. If so, its snapshot 𝛿 1 is
returned and 𝑏 1 is assigned true. Otherwise, a fresh snapshot is returned with false. If the current
state 𝜎3 is imprecise, then heap chunks are similarly removed from ℎ ? and acc (𝑒.𝑓 ) is checked for
existence in ℎ ? . If a field chunk for acc (𝑒.𝑓 ) is not found in either heap, then a run-time check
is generated for it and passed to the continuation 𝑄 alongside the two heaps after removal and
acc (𝑒.𝑓 )’s snapshot. Without imprecision, consume’ will fail when a field chunk for acc (𝑒.𝑓 ) is not
found in ℎ.

A.4    Symbolic execution of statements
The exec rules for sequence statements, variable declarations and assignments, allocations, and
if statements are pretty much unchanged from Viper. The only difference is that Gradual Viper’s
versions of eval, produce, branch, and consume (defined previously) are used instead of Viper’s.
Statements in a sequence are executed one after another, and variable declarations introduce a fresh
symbolic value for the variable into the state. Variable assignments evaluate the right-hand side to
a symbolic value and update the variable in the symbolic store with the result. Allocations produce
fresh heap chunks for fields into the state. Finally, if statements have their condition evaluated and
then branch is used to split execution along two paths to symbolically execute the true and false
branches.
Gradual C0                                                                                                                       1:47

                                                                                        Û
    heap-rem-pred(isImprecise, ℎ, 𝜋, 𝑝 (𝑡 ) ) = if ∃ (𝑝 (𝑟 ; 𝛿 ) ∈ ℎ . check(𝜋,             𝑡 = 𝑟 ) ) then
                                                       (ℎ \ {𝑝 (𝑟 ; 𝛿 ) }, 𝛿, true )
                                                  else ( ∅, fresh, false )
    heap-rem-acc(isImprecise, ℎ, 𝜋, 𝑓 (𝑡 ) ) = ℎ ′ := foldl(ℎ, ∅, (𝜆 𝑓𝑠𝑟𝑐 (𝑟 ; 𝛿 ), ℎ𝑑𝑠𝑡 .
                                                       if (¬( |𝑟 | = 1) ∥ ¬(𝑓 = 𝑓𝑠𝑟𝑐 ) ∥ ¬check(isImprecise, 𝜋, 𝑡 = 𝑟 ) ) then
                                                         ℎ𝑑𝑠𝑡 ∪ 𝑓𝑠𝑟𝑐 (𝑟 ; 𝛿 )
                                                       else ℎ𝑑𝑠𝑡 ) )
                                                  if ∃ 𝑓 (𝑟 ; 𝛿 ) ∈ ℎ . check(𝜋, 𝑡 = 𝑟 ) then
                                                       (ℎ ′ , 𝛿, true )
                                                  else
                                                       ℎ ′ := foldl(ℎ ′ , ∅, (𝜆 𝑓𝑠𝑟𝑐 (𝑟 ; 𝛿 ), ℎ𝑑𝑠𝑡 .
                                                            if (𝑓𝑠𝑟𝑐 (𝑟 ; 𝛿 ) is a field chunk ) then
                                                              ℎ𝑑𝑠𝑡 ∪ 𝑓𝑠𝑟𝑐 (𝑟 ; 𝛿 )
                                                            else ℎ𝑑𝑠𝑡 ) )
                                                       (ℎ ′ , fresh, false )

                                          Fig. 27. Heap remove function definitions


        check(𝜋, 𝑡 ) = pc-all(𝜋 ) ⇒ 𝑡
                                         
                                         
                                          true, true                    if check(𝜋, 𝑡 )
                                         
                                         
                                                                                              Û
        check( isImprecise , 𝜋, 𝑡 ) =       true, diff ( pc-all(𝜋 ), 𝑡 )  if ( isImprecise ∧ (   pc-all(𝜋 ) ∧ 𝑡 ) SAT )
                                         
                                         
                                          false, ∅
                                                                        otherwise
                                         
                                         (
                                           success(), 𝑡       if (𝑏 = true ) where 𝑏, 𝑡 := check(isImprecise, 𝜋, 𝑡 )
        assert( isImprecise , 𝜋, 𝑡 ) =
                                          failure(),    ∅      otherwise

                  ■    Handles imprecision        ■      Handles run-time check generation and collection

                                        Fig. 28. Check and assert function definitions

   Symbolic execution of field assignments first evaluates the right-hand side expression 𝑒 to the
symbolic value 𝑡 with the current state 𝜎1 and eval. Any field reads in 𝑒 are either directly or
optimistically verified using 𝜎1 . Then, the resulting state 𝜎2 must establish write access to 𝑥 .𝑓 in
consume, i.e. 𝜎2 ⇒  f acc (𝑥 .𝑓 ). The call to consume also removes the field chunk for acc (𝑥 .𝑓 ) from
𝜎2 (if it is in there) resulting in 𝜎3 . Therefore, the call to produce can safely add a fresh field chunk
for acc (𝑥 .𝑓 ) alongside 𝑥 .𝑓 = 𝑡 to 𝜎3 before it is passed to the continuation 𝑄. Under the hood,
run-time checks are collected where required for soundness and passed to 𝑄.
   The exec rule for method calls similarly uses eval to evaluate the given args 𝑒 to symbolic values
𝑡, asserts the method’s precondition 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 holds in the current state, consumes the heap chunks
in the precondition, and produces the method’s postcondition 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 into the continuation. Run-
time checks are also collected where necessary (under the hood) and passed to the continuation.
Gradual Viper makes an exception when consuming preconditions at method calls (and loop
invariants before entering loops), which can be seen in the if-then in the method call rule. If
Gradual Viper determines the precondition (invariant) is equi-recursively imprecise, then it will
conservatively remove all the heap chunks from both symbolic heaps after the consume. This
exception ensures the static verification semantics in Gradual Viper lines up with the equi-recursive,
dynamic verification semantics encoded by GVC0 in §4.4 such that Gradual C0 is sound. Note that
the origin field of R is set to 𝑧 := 𝑚 (𝑒 ) before consuming 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 and reset to none after producing
𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 . Setting the origin indicates that run-time checks or branch conditions for 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 or
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:48                                                                                                           Aldrich

  exec(𝜎1 , 𝑠 1 ; 𝑠 2 , 𝑄 )                                = exec(𝜎1 , 𝑠 1 , (𝜆 𝜎2 . exec(𝜎2 , 𝑠 2 , 𝑄 ) ) )
  exec(𝜎, var 𝑥 : 𝑇 , 𝑄 )                                  = 𝑄 (𝜎 {𝛾 := havoc(𝜎 .𝛾, 𝑥 ) } )
  exec(𝜎1 , 𝑥 := 𝑒, 𝑄 )                                    = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . 𝑄 (𝜎2 {𝛾 := 𝜎2 .𝛾 [𝑥 ↦→ 𝑡 ] } ) ) )
  exec(𝜎1 , 𝑥 . 𝑓 := 𝑒, 𝑄 )                                = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 . consume (𝜎2 , acc (𝑥 .𝑓 ), (𝜆 𝜎3 , _ .
                                                                produce (𝜎3 , acc (𝑥 .𝑓 ) && 𝑥 .𝑓 = 𝑡, 𝑝𝑎𝑖𝑟 ( fresh, 𝑢𝑛𝑖𝑡 ), 𝑄 ) ) ) ) )

  exec(𝜎, 𝑥 := new (𝑓 ), 𝑄 )                               = produce (𝜎 {𝛾 := havoc(𝜎 .𝛾, 𝑥 ) }, acc (𝑥 .𝑓 ), fresh, 𝑄 )
  exec(𝜎1 , 𝑧 := 𝑚 (𝑒 ), 𝑄 )                               = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                                R ′ := 𝜎2 .R { origin := (𝜎2 , 𝑧 := 𝑚 (𝑒 ), 𝑡 ) }

                                                                consume (𝜎2 { R := R ′ }, 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 [𝑚𝑒𝑡ℎ𝑎𝑟𝑔𝑠 ↦→ 𝑡 ], (𝜆 𝜎3 , 𝛿 .

                                                                  if ( equi-imp(𝑚𝑒𝑡ℎ𝑝𝑟𝑒 ) ) then

                                                                     𝜎4 := 𝜎3 { isImprecise := true, ℎ ? := ∅, ℎ := ∅,

                                                                                  𝛾 := havoc(𝜎3 .𝛾, 𝑧 ) }
                                                                  else 𝜎4 := 𝜎3 {𝛾 := havoc(𝜎3 .𝛾, 𝑧 ) }

                                                                  produce (𝜎4 , 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 [𝑚𝑒𝑡ℎ𝑎𝑟𝑔𝑠 ↦→ 𝑡 ] [𝑚𝑒𝑡ℎ𝑟𝑒𝑡 ↦→ 𝑧 ], fresh,

                                                                    (𝜆 𝜎5 . 𝑄 (𝜎5 { R := 𝜎5 .R { origin := none } } ) ) ) ) ) ) )
  exec(𝜎1 , assert 𝜙, 𝑄 )                                  = consume (𝜎1 , 𝜙, (𝜆 𝜎2 , 𝛿 .
                                                                well-formed (𝜎2 , ? && 𝜙 , 𝛿, (𝜆 𝜎3 .

                                                                 𝑄 (𝜎1 { 𝜋 := 𝜎3 .𝜋 ,     R := 𝜎3 .R } ) ) ) ) )
  exec(𝜎1 , fold acc (𝑝 (𝑒 ) ), 𝑄 )                        = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                                R ′ := 𝜎2 .R { origin := (𝜎2 , fold acc (𝑝 (𝑒 ) ), 𝑡 ) }

                                                                consume (𝜎2 { R := R ′ }, 𝑝𝑟𝑒𝑑𝑏𝑜𝑑 𝑦 [𝑝𝑟𝑒𝑑𝑎𝑟𝑔𝑠 ↦→ 𝑡 ], (𝜆 𝜎3 , 𝛿 .

                                                                  produce (𝜎3 { R := 𝜎3 .R { origin := none } }, acc (𝑝 (𝑡 ) ), 𝛿,
                                                                    𝑄 )) )) ) )
  exec(𝜎1 , unfold acc (𝑝 (𝑒 ) ), 𝑄 )                      = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .

                                                                R ′ := 𝜎2 .R { origin := (𝜎2 , unfold acc (𝑝 (𝑒 ) ), 𝑡 ) }

                                                                consume (𝜎2 { R := R ′ }, acc (𝑝 (𝑡 ) ), (𝜆 𝜎3 , 𝛿 .

                                                                  produce (𝜎3 , 𝑝𝑟𝑒𝑑𝑏𝑜𝑑 𝑦 [𝑝𝑟𝑒𝑑𝑎𝑟𝑔𝑠 ↦→ 𝑡 ], 𝛿, (𝜆 𝜎4 .

                                                                    𝑄 (𝜎4 { R := 𝜎4 .R { origin := none } } ) ) ) ) ) ) ) )
  exec(𝜎1 , if (𝑒 ) { 𝑠𝑡𝑚𝑡 1 } else { 𝑠𝑡𝑚𝑡 2 }, 𝑄 ) = eval (𝜎1 , 𝑒, (𝜆 𝜎2 , 𝑡 .
                                     branch (𝜎2 , 𝑒, 𝑡, (𝜆 𝜎3 . exec(𝜎3 , 𝑠𝑡𝑚𝑡 1 , 𝑄 ) ), (𝜆 𝜎3 . exec(𝜎3 , 𝑠𝑡𝑚𝑡 2 , 𝑄 ) ) ) ) )


                      ■       Handles imprecision     ■    Handles run-time check generation and collection

                                 Fig. 29. Rules for symbolically executing program statements (1/2)



𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 should be attached to the method call statement rather than where they are declared. The
origin arguments 𝜎2 and 𝑡 are used to reverse the substitution [𝑚𝑒𝑡ℎ𝑎𝑟𝑔𝑠 ↦→ 𝑡] in run-time checks
and branch conditions for 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 and 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 . The rule for (un)folding predicates operates the
same as for method calls where 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 is the predicate body (predicate instance) and 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 is
the predicate instance (predicate body). The origin is set to fold acc (𝑝 (𝑒)) and unfold acc (𝑝 (𝑒))
respectively.
Gradual C0                                                                                                               1:49


exec(𝜎1 , while (𝑒 ) invariant 𝜙e { 𝑠𝑡𝑚𝑡 }, 𝑄 ) =         𝛾 2 := havoc(𝜎1 .𝛾, 𝑥 )
                      𝑟𝑒𝑠𝑏𝑜𝑑 𝑦 := well-formed (

                       𝜎1 { isImprecise := false, ℎ ? := ∅ , ℎ := ∅, 𝛾 := 𝛾 2 ,

                            R := 𝜎1 .R { origin := (𝜎1 , while (𝑒 ) invariant 𝜙e { 𝑠𝑡𝑚𝑡 }, beginning ) } },

                        𝜙e && 𝑒 , fresh, (𝜆 𝜎3 { R := 𝜎3 .R { origin := none } } .
                         exec(𝜎3 , 𝑠𝑡𝑚𝑡, (𝜆 𝜎4 .

                              eval ( 𝜎4 { R := 𝜎4 .R { origin := (𝜎4 , while (𝑒 ) invariant 𝜙e { 𝑠𝑡𝑚𝑡 }, end ) } } ,
                                𝑒, (𝜆 𝜎𝑒 , _ .
                                     consume ( 𝜎4 { R := 𝜎4 .R { origin := 𝜎𝑒 .R.origin, rcs := 𝜎𝑒 .R.rcs } } ,

                                        𝜙e , (𝜆 𝜎5 , _ . ℜ := ℜ ∪ 𝜎5 .R.rcs ; success() ) ) ) ) ) ) ) )

                      𝑟𝑒𝑠𝑎𝑓 𝑡𝑒𝑟 := eval ( 𝜎1 { R := 𝜎1 .R { origin := (𝜎1 , while (𝑒 ) invariant 𝜙e { 𝑠𝑡𝑚𝑡 }, before ) } } ,
                       𝑒, (𝜆 𝜎𝑒 , _ . consume (
                            𝜎1 { R := 𝜎1 .R { origin := 𝜎𝑒 .R.origin, rcs := 𝜎𝑒 .R.rcs } } ,

                            𝜙e , (𝜆 𝜎2 , _ .

                              if ( equi-imp(𝜙e) ) then

                                𝜎3 := 𝜎2 { isImprecise := true, ℎ ? := ∅, ℎ := ∅, 𝛾 := 𝛾 2 }
                              else 𝜎3 := 𝜎2 {𝛾 := 𝛾 2 }

                              produce (𝜎3 { 𝜎3 .R { origin := (𝜎3 , while (𝑒 ) invariant 𝜙e { 𝑠𝑡𝑚𝑡 }, after ) } },

                                𝜙e && !𝑒 , fresh, 𝑄 ) ) ) ) )
                      if (𝜎1 .isImprecise) then
                        if (¬𝑟𝑒𝑠𝑏𝑜𝑑 𝑦 ∧ 𝑟𝑒𝑠𝑎𝑓 𝑡𝑒𝑟 ) then

                            R ′ := addcheck (𝜎1 .R, 𝑒, ¬𝑒 )

                            ℜ := ℜ ∪ R ′ .rcs.last
                        (¬𝑟𝑒𝑠𝑏𝑜𝑑 𝑦 ∨ 𝑟𝑒𝑠𝑎𝑓 𝑡𝑒𝑟 ) ∧ (𝑟𝑒𝑠𝑏𝑜𝑑 𝑦 ∨ 𝑟𝑒𝑠𝑎𝑓 𝑡𝑒𝑟 )
                     else
                       𝑟𝑒𝑠𝑏𝑜𝑑 𝑦 ∧ 𝑟𝑒𝑠𝑎𝑓 𝑡𝑒𝑟
             where 𝑥 are variables modified by the loop body

                 ■    Handles imprecision         ■     Handles run-time check generation and collection

                            Fig. 29. Rules for symbolically executing program statements (2/2)



   In contrast, 𝜙 in assert 𝜙 maintains a none origin field, because 𝜙’s use and declaration align
at the same program location assert 𝜙. The assert rule relies on consume to assert 𝜙 holds in
the current state 𝜎1 . If the consume succeeds, the state 𝜎1 is passed to the continuation nearly
unmodified. Path condition constraints from 𝜙 hold in 𝜎1 either directly or optimistically. Therefore,
these constraints are added to 𝜎1 to avoid producing run-time checks for them in later program
statements. Run-time checks from the consume are also passed to the continuation. Note that 𝜙 is
checked for well-formedness here (Fig. 31). A formula is well-formed if it contains ? or accessibility
predicates that verify access to the formula’s fields (self-framing). Additionally, the formula cannot
contain duplicate accessibility predicates or predicate instances. Finally, well-formed adds the
J. DiVincenzo, I. McCormack, H. Gouni, J. Gorenburg, J. Ramos-Dávila, M. Zhang, C. Zimmerman, J. Sunshine, É. Tanter, J.
1:50                                                                                                           Aldrich

                              equi-imp(? && 𝜙 )          = true
                              equi-imp(𝜙 1 && 𝜙 2 )      = equi-imp(𝜙 1 ) ∨ equi-imp(𝜙 2 )
                              equi-imp(𝑒 ? 𝜙 1 : 𝜙 2 ) = equi-imp(𝜙 1 ) ∨ equi-imp(𝜙 2 )
                              equi-imp(acc (𝑝 (𝑒 ) ) )   = if (𝑝 ∈ VisitedPreds ) then
                                                             false
                                                          else
                                                             VisitedPreds := VisitedPreds ∪ 𝑝
                                                             𝑏 := equi-imp(𝑝𝑟𝑒𝑑𝑏𝑜𝑑 𝑦 )
                                                             VisitedPreds := VisitedPreds \ 𝑝
                                                             𝑏
                              equi-imp(_)                = false



            Fig. 30. Boolean function determining if a gradual formula is equi-recursively imprecise or not

formula’s information to the given symbolic state. Here, 𝜙 does not need to be self-framed, and so
it is joined with ? in the call to well-formed. ? verifies access to all of 𝜙’s fields.

                                                                   e 𝛿, (𝜆 𝜎2 .
                                           e 𝛿, 𝑄 ) = produce(𝜎1 , 𝜙,
                          well-formed(𝜎1 , 𝜙,

                                                            produce(𝜎1 { 𝜋 := 𝜎2 .𝜋 }, 𝜙,
                                                                                       e 𝛿, 𝑄 ) ) )

                                    Fig. 31. Well-formed formula function definition


  Finally, while the while loop rule is the largest rule and looks fairly complex, it just combines
ideas from other rules that are discussed in great detail in this section and from the branch rule
described in §A.2.

A.5    Valid program
A Gradual Viper program is valid if all of its method and predicate declarations are verified
successfully as defined in Fig. 15. In particular, a method 𝑚’s declaration is verified first by checking
well-formedness of 𝑚’s precondition 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 and postcondition 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 using the empty state
𝜎0 (well-formedness is described in §A.4). Note, fresh symbolic values are created and added to
𝜎0 for 𝑚’s argument variables 𝑥 and return variables 𝑦. If 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 and 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 are well-formed,
then the body of 𝑚 (𝑚𝑒𝑡ℎ𝑏𝑜𝑑 𝑦 ) is symbolically executed (§A.4) starting with the symbolic state 𝜎1
containing 𝑚𝑒𝑡ℎ𝑝𝑟𝑒 . Recall, well-formed additionally produces the formula that is being checked
into the symbolic state. The symbolic state 𝜎2 is produced after the symbolic execution of 𝑚𝑒𝑡ℎ𝑏𝑜𝑑𝑦 .
Then, 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 is checked for validity against 𝜎2 , i.e. 𝜎2 must establish 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡 (§A.3). If 𝑚𝑒𝑡ℎ𝑝𝑜𝑠𝑡
is established, then verification succeeds; and as a result, the run-time checks collected during
verification are added to ℜ (highlighted in blue). A valid predicate 𝑝 is simply valid if 𝑝’s body
𝑝𝑟𝑒𝑑𝑏𝑜𝑑 𝑦 is well-formed. As before, fresh symbolic values are created for 𝑝’s argument variables 𝑥.
Note, no run-time checks are added to ℜ here, because well-formedness checks do not produce any
run-time checks.
