      Scalable Shape Analysis for Systems Code

      Hongseok Yang1 , Oukseh Lee2 , Josh Berdine3 , Cristiano Calcagno4 ,
             Byron Cook3 , Dino Distefano1 , and Peter O’Hearn1
                             1
                                 Queen Mary, Univ. of London
                                 2
                                  Hanyang University, Korea
                                   3
                                      Microsoft Research
                                     4
                                       Imperial College



       Abstract. Pointer safety faults in device drivers are one of the leading
       causes of crashes in operating systems code. In principle, shape analysis
       tools can be used to prove the absence of this type of error. In practice,
       however, shape analysis is not used due to the unacceptable mixture
       of scalability and precision provided by existing tools. In this paper we
       report on a new join operation    † for the separation domain which aggres-
       sively abstracts information for scalability yet does not lead to false error
       reports. 
                † is a critical piece of a new shape analysis tool that provides an
       acceptable mixture of scalability and precision for industrial application.
       Experiments on whole Windows and Linux device drivers (ﬁrewire, pci-
       driver, cdrom, md, etc.) represent the ﬁrst working application of shape
       analysis to veriﬁcation of whole industrial programs.


1    Introduction
Pointer safety faults in device drivers are one of the leading causes of operating
system crashes. The reasons for this are as follows:
 – The average Windows or Linux computer has numerous (i.e. >15) device
   drivers installed,
 – Most device drivers manage relatively complex combinations of shared
   singly- and doubly-linked lists,
 – Device drivers are required to respect many byzantine invariants while ma-
   nipulating data structures (e.g. pieces of data structures that have been
   paged out can only be referenced at low thread-priority). This results in
   complex and nonuniform calling conventions, unlike typical benchmark code.
   By pointer safety we mean that a program does not dereference null or a
dangling pointer, or produce a memory leak. In principle a shape analysis tool
can be used to prove the absence of pointer safety violations: shape analysis is
a heap-aware program analysis with accurate handling of deep update. Further-
more, device drivers are small (e.g. <15k LOC) and usually do not use trees or
DAGs—thus making device drivers the perfect application for shape analysis.
   So, why aren’t shape analysis tools regularly applied to device drivers? The
reason is that today’s shape analysis tools are either scalable, or precise, but

A. Gupta and S. Malik (Eds.): CAV 2008, LNCS 5123, pp. 385–398, 2008.

c Springer-Verlag Berlin Heidelberg 2008
386     H. Yang et al.


Table 1. Results with the † extension of SpaceInvader on Windows and Linux device
drivers. Experiments were performed on an Intel Core Duo 2.0GHz with 2GB. Each er-
ror found was conﬁrmed manually. Errors in the Windows device driver (t1394Diag.c)
were conﬁrmed by the Windows kernel team. The time and space columns contain the
numbers for the analysis of ﬁxed versions of the drivers (and so report time to ﬁnd
proofs of pointer safety).

Program      LOC Sec       MB Memory leaks Dereference errors False error rate
scull.c      1010    0.36 0.25    1                 0               0%
class.c      1983    8.21 7.62    2                 1               0%
pci-driver.c 2532    0.97 1.72    0                0                0%
ll rw blk.c  5469 887.94 485.87   3                1                0%
cdrom.c      6218 103.26 71.52    0                2                0%
md.c         6635 1585.69 847.63  6                5                0%
t1394Diag.c 10240 135.05 68.81    33               10               0%


not both. Numerous papers have reported on the application of accurate shape
analysis to small examples drawn from real systems code; other papers have
reported on very imprecise analysis on large code bases. The veriﬁcation of whole
industrial programs, however, requires both.
   Towards the elusive goal of ﬁnding a scalable and precise analysis, in this
paper we describe a new join operation,  † , for shape analysis tools based on the
separation domain [4,10,17].  † provides a mixture of scalability and precision
suﬃcient for the problem of proving pointer safety of whole industrial device
drivers. A join operation (in the terminology of abstract interpretation [9]) takes
a disjunction of two abstract states, each of which describes (in our setting) a
set of concrete heaps that may arise during program execution.      † attempts to
construct a common generalization of the states. In case the attempt succeeds (  †
is a partial join operator) the generalization subsequently replaces the original
disjunction, leading to fewer cases to consider during the shape analysis.
   In order to demonstrate the scalability and accuracy of     † , we have imple-
mented it in our shape analysis tool SpaceInvader, together with an abstract
model of the operating system environment that we have developed. Then, we
have applied the resulting tool to numerous Windows and Linux device drivers.


2     Experiments

Before describing the technical details of † , we ﬁrst present the results of an
experimental evaluation that demonstrates its scalability and precision. Table 1
displays the results of experiments with the  † extension of SpaceInvader on
seven device drivers. Each of the drivers manipulates multiple, sometimes nested,
sometimes circular, linked lists. One driver, t1394Diag.c, is the IEEE 1394
(ﬁrewire) driver for the Windows operating system. The drivers pci-driver.c,
ll rw blk.c, cdrom.c and md.c are from an industrial version of Embedded
Linux, given to us by ETRI. The driver class.c is from a standard Linux
                                    Scalable Shape Analysis for Systems Code       387

distribution, and scull.c is a Linux char driver used in the experiments in [7]1
Each of these drivers is analyzed in the context of environment code which non-
deterministically generates input data structures, and calls the driver’s dispatch
routines repeatedly. In essence, each driver is supplied with a particular pre-
condition (expressed as C code, as in [7]) but the model of system calls can be
reused from driver to driver.
    During our experiments SpaceInvader was used in a stop-ﬁrst conﬁguration,
where the analyzer halts if it cannot prove that a dereferencing operator is safe or
if it cannot prove that a cell is reachable. When we encountered bugs we would
ﬁx them, and then run our tool again. The time and space columns in Table
1 report the numbers for the analysis of our bug-ﬁxed versions of the drivers.
Note that, during our experiments, no false errors were found. Also, note that
for the ﬁxed drivers SpaceInvader proved pointer safety. No known tool with
scalability reported to programs up to 10k LOC can match that precision.
Caveats. Device drivers often use circular doubly-linked lists. The ﬁrst caveat is
that, in several cases, we modiﬁed the examples in order to operate over singly-
linked lists, in order to aid our analysis. Pointer safety can often be proved
using singly-linked semantics even though the code is designed to operate over
doubly-linked lists (it is rare for code to actually make use of the back pointers).
Second, there is a signiﬁcant caveat regarding arrays. SpaceInvader currently
presumes memory safety of arrays, by returning a nondeterministic value for any
array dereferencing. The treatment of pointer safety can still be sound under
such an assumption, and in the (slightly modiﬁed) Linux drivers our analyzer
encountered no false alarms. However, the 1394 device driver contains arrays
of pointers, which are beyond what our method can handle: we modiﬁed the
code such that those arrays have size 1 and can be treated as pointer variables.
This, of course, is just one instance of the fact that the problems of analyzing
arrays and pointers are not independent. We regard this issue as an avenue
for interesting future work. Finally, note that SpaceInvader currently only
implements shape analysis for sequential programs, whereas device drivers of
course are multi-threaded. As reported in [12], a sequential shape analysis tool
such as SpaceInvader can be used to ﬁnd and then verify resource invariants
for device drivers, thereby proving pointer safety for the concurrent program.
However, we emphasize that developing a scalable, precise shape analysis for
concurrent programs is an open problem; only very recently, some interesting
ideas such as [5,12,18] have been proposed, which give promising new lines of
attack, but on which further, especially experimental, work is needed.


3     Abstract States and Setting

In this section we describe the abstract states that SpaceInvader analysis
operates over. In the next section we will describe the details of 
                                                                   † . Due to space
1
    This is a modiﬁed version of the Linux scull driver, where arrays are assumed to be
    of size 1.
388      H. Yang et al.

constraints we will assume that the reader is somewhat familiar with the basics
of program analysis and shape analysis.
   SpaceInvader operates over abstract states expressed as separation logic
formulae. Following [4,10,17], we call these abstract states symbolic heaps. The
symbolic heaps q, are deﬁned by the following grammar:

            e ::= x | x | 0                       P ::= · · ·
           Π ::= Π ∧ Π | e=e | e=e | true         Σ ::= Σ ∗ Σ | emp | P | true
            q ::= err | Π ∧ Σ

A symbolic heap q can be err, denoting the error state, or it has the form Π ∧ Σ,
where Π and Σ describe properties of variables and the heap, respectively. The
separating conjunction Σ0 ∗ Σ1 holds for a heap if and only if the heap can be
split into two disjoint parts, one making Σ0 true and the other making Σ1 true.
emp means the empty heap, and true holds for all heaps. The primed variables
x in a symbolic heap are assumed to be (implicitly) existentially quantiﬁed.
   P is a collection of basic predicates. One instantiation is

                    k ::= PE | NE             P ::= (e → e) | ls k e e

Here, e → f means a heap with only one cell e that stores f . The list segment
predicate ls k e0 e1 denotes heaps containing one list segment from e0 to e1 only.
This list segment starts at cell e0 and its last cell stores e1 . The list is possibly
empty if k = PE; otherwise (i.e., k = NE), the list is not empty. The meanings of
the segment predicates can be understood in terms of the deﬁnitions

                   ls PE e f ⇐⇒ (e = f ∧ emp) ∨ (ls NE e f ),
                   ls NE e f ⇐⇒ (e → f ) ∨ (∃y  . e → y  ∗ ls NE y  f ).

These deﬁnitions are not within the shape domain (e.g., the domain does not
have ∨), but are mathematical deﬁnitions in the metalanguage, used to verify
soundness of operations on the predicates. Note that there is no problem with
the recursion in ls NE : the recursive instance is in a positive position, and the
deﬁnition satisﬁes monotonicity properties suﬃcient to ensure a solution.
  A diﬀerent instantiation of P gives us a variation on [3].2

                  k ::= PE | NE            P ::= (e → f : e) | ls k φ e e

Here, the points-to predicate (e → f : e) is for records with ﬁelds f, and φ is a
binary predicate that describes the shape of each node in a list. The deﬁnition
of the nonempty list segment here is

                 ls NE φ e f ⇐⇒ φ(e, f ) ∨ (∃y  . φ(e, y  ) ∗ ls NE y  f )

and the φ predicate gives us a way to describe composite structures.
2
    This instantiation assumes the change of the language where we have heap cells with
    multiple ﬁelds, instead of unary cells.
                                      Scalable Shape Analysis for Systems Code        389

  For example, if f is a ﬁeld, let φf be the predicate where φf (x, y) is x → f : y.
Then using φf as φ, the formula ls NE φ e f describes lists linked by the f ﬁeld.
The formula

                  (x → f : y  , g : z  ) ∗ ls PE φf y  x ∗ ls PE φg z  x

describes two circular linked lists sharing a common header, where one list uses f
for linking and the other uses g. Finally, if φ itself describes lists, as when φ(x, y)
is the predicate ∃x . (x → g : x , f : y) ∗ ls PE φg x 0, then ls NE φ e f describes a
nonempty linked list where each node points to a possibly empty sublist, and
where the sublists are disjoint. Combinations of these kinds of structures, nested
lists and multiple lists with a common header node, are common in device drivers.
    The experiments in this paper are done using this second instantiation of P. It
is similar to the domain from [3], but uses predicates for both possibly empty and
necessarily nonempty list segments. The reader might have noticed that having
ls PE does not give us any extra expressive power: its meaning can be represented
using two abstract states, one a emp and the other a ls NE. However, having ls PE
impacts performance, as it represents disjunctive information, succinctly.
    SpaceInvader implements a context sensitive, ﬂow sensitive analysis, us-
ing a variant of the RHS interprocedural dataﬂow analysis algorithm [22,11]. It
employs join to make procedure summaries smaller. Following [21,23], SpaceIn-
vader also passes only the reachable portion of the heap to a procedure and
aggressively discards intermediate states. The mixture of these optimizations—
join, locality, discarding states—is key; turning oﬀ any one of the optimizations
results in the analysis using more than the 2GB RAM on at least one of the
examples, causing disk thrashing, and then leading to timeout (which we set at
90min). Thus we do not claim that        † alone is the root cause for the performance
found in Table 1, but it is a critical ingredient (c.f., §4.3).


4    A Join for Symbolic Heaps

We now discuss    † . We begin with an intuitive explanation. Later, in §4.1, we
provide a formal deﬁnition.
  In the framework of abstract interpretation [9], a join operator takes two sym-
bolic states in a program analysis and attempts to ﬁnd a common generalization.
To see the issue, consider the program

 x=0;    while (NONDET) { d=malloc(sizeof(Node)); d->next=x; x=d; }

which nondeterministically generates acyclic linked lists. When we run our ba-
sic analysis algorithm, without    † , it returns three symbolic heaps at the end:
(ls NE x 0) ∨ (x → 0) ∨ (x = 0 ∧ emp). (Here, for simplicity in the presentation, we
have elided the φ parameter of the ls predicates.)
    Now, if you look at the ﬁrst two disjuncts there is evident redundancy: If
you know that either x points to 0 or a nonempty linked list, then that is the
same as knowing you have a nonempty linked list. So,         † replaces the ﬁrst two
390     H. Yang et al.


Table 2. Creation routines. Reports the number of states in the postcondition with
join turned on or oﬀ, and the base list predicates chosen to be either nonempty ls only
(NE), or both nonempty and possibly empty ls (PE).

                                            NO JOIN JOIN
                          Program             NE   PE NE PE
                          onelist create.c     3    3 2 1
                          twolist create.c     9    9 4 1
                          firewire create.c 3969 3087 32 1


disjuncts with just the list segment formula, giving us (ls NE x 0) ∨ (x = 0 ∧ emp).
It is possible to take yet a further step, using the notion of a possibly empty list
segment. If you know that either you have a nonempty list, or that x = 0 ∧ emp,
then that is the same as having ls PE x 0, and      † produces this formula from the
previous two. Thus, using       † we have gone from a position where we have three
disjuncts in our postcondition, to where we have only one. The saving that this
possibly gives us is substantial, especially for more complicated programs or
more complicated data structures.
    Table 2 gives an indication. onelist create.c in the table is the C program
above that nondeterministically creates a list and twolist create.c is a simi-
lar C program that creates two disjoint linked lists. firewire create.c is the
environment code we use in the analysis of the 1394 ﬁrewire driver: it creates
ﬁve cyclic linked lists, which share a common header node, with head pointers
in some of the lists, and with nested sublists.
    There are two points to note. The ﬁrst is just the great saving, in number of
states (e.g., from 3087 down to 1). This is particularly important with environ-
ment code, like firewire create.c, which is run as a harness to generate heaps
on which driver routines will subsequently be run. The second is the distinction
between NE and PE. In the table we keep track of two versions of our analysis,
one where ls NE is the only list predicate used by the analysis, and another where
we use both ls NE and ls PE.
    This illustration shows some of the aspects of    † , but not all. In the illustration

† worked perfectly, never losing any information, but this is not always the case.
Part of the intuition is that you generalize points-to facts by list segments when
you can. So, considering y → 0 ∗ (ls NE x 0) ∨ (ls NE y 0) ∗ x → 0,     † will produce
(ls NE y 0) ∗ (ls NE x 0). This formula is less precise than the disjunction, in that it
loses the information that one or the other of the lists pointed to by x and y has
length precisely 1. Fortunately, it is unusual for programs to rely on this sort of
disjunctive information.
    We have tried to keep the intuitive description simple, but the truth is that

† must deal with disequalities, equalities, and generalization of “nothing” by
ls PE in ways that are nontrivial. It also must deal with the existential (primed)
variables specially. In the end, for instance, when       † is given
                 q0 ≡ x=y ∧ (ls NE x 0 ∗ y → 0)     and
                 q1 ≡ x=y ∧ x =y ∧ (x → x ∗ ls NE y x ∗ ls NE x 0),
                                          Scalable Shape Analysis for Systems Code            391

it will produce x=y ∧ ls NE x v  ∗ ls NE y v  ∗ ls PE v  0. Now we turn to the formal
deﬁnition.

4.1       Formal Deﬁnition
In this section, we deﬁne the (partial) binary operator         † on symbolic heaps,
considering only the simple linked lists (the ﬁrst instantiation of P). The    † for
nested lists will be described in the next section.
  † works in two stages. Suppose that it is given symbolic heaps (Π0 ∧ Σ0 ) and
(Π1 ∧ Σ1 ) that do not share any primed variables. In the ﬁrst stage,   † constructs
Σ and a ternary relation  on expressions such that
                                                           
           ∀i ∈ {0, 1}.      {ei =x | (e0 , e1 , x ) ∈  } ∧ Σi =⇒ Σ.          (1)

Intuitively, this condition means that Σ overapproximates both Σ0 and Σ1 ,
and that  provides witnesses of existential (primed) variables of Σ for this
overapproximation. For instance, if Σ0 ≡ (ls NE x 0 ∗ y → 0) and Σ1 ≡ (x → x ∗
ls NE y x ∗ ls NE x 0), then 
                               † returns

               Σ ≡ ls NE x v  ∗ ls NE y v  ∗ ls PE v  0,    ≡ {(0, x , v  )}.          (2)

In this case, the condition (1) is

               0=v  ∧ (ls NE x 0 ∗ y → 0) =⇒ (ls NE x v  ∗ ls NE y v  ∗ ls PE v  0)
   x =v ∧ (x → x ∗ ls NE y x ∗ ls NE x 0) =⇒ (ls NE x v  ∗ ls NE y v  ∗ ls PE v  0).
          


This means that both Σ0 and Σ1 imply Σ when 0 and x are used as witnesses
for the (implicitly) existentially quantiﬁed variable v  of Σ.
   After constructing Σ and  , the      † operator does one syntactic check on  , in
order to decide whether it has lost crucial sharing information of input symbolic
heaps. Only when the check succeeds does           † move on to the second stage. (We
will describe the details of the ﬁrst stage, including the check on  , later.)
   In the second stage, the  † operator computes an overapproximation Π of Π0
and Π1 :
             ⎛                                                                   ⎞
               {e=f | e=f has no primed vars, it occurs in Π0 and Π1 }
  Π =
       def
             ⎝ ∪ {e=f | e=f has no primed vars, it occurs in Π0 and Π1 }⎠ .
                ∪ {x =0 | (e0 , e1 , x ) ∈  and ei =0 occurs in Πi }

This deﬁnition says that  † keeps an equality or disequality in Π if it appears
in both Π0 and Π1 and does not contain any primed variables, or if it is of the
form x =0 and its witness ei for the i-th symbolic heap is guaranteed to be dif-
ferent from 0. Both cases are considered here in order to deal with programming
patterns found in device drivers. For instance, x =0 in the second case should
be included, because some drivers store 0 or 1 to a cell, say, x, depending on
whether a linked list y is empty, and subsequently, they use the contents of cell
x to decide the emptiness of the list y. The computed Π and the result Σ of the
ﬁrst stage become the output of   †.
392       H. Yang et al.

Computation of Σ,  : We now describe the details of the ﬁrst stage of 
                                                                        † . For
this, we need a judgment

                                   Σ0 , Σ1 ,   Σ,  , δ0 , δ1

where δi is a binary relation on expressions in Σi . This judgment signiﬁes that
Σ0 and Σ1 can be joined to give Σ and a ternary relation  for witnesses.
Furthermore, the judgment ensures that  extends the given , and that δi
records (ei , fi ) of all ls k ei fi in Σi that have been generalized to a possibly
empty list during the join; these δi components are used later to decide whether
this join to Σ has lost too much information and should, therefore, be discarded.
For instance, we have

   (ls NE x 0 ∗ y → 0), (x → x ∗ ls NE y x ∗ ls NE x 0), ∅
                      (ls NE x v  ∗ ls NE y v  ∗ ls PE v  0), {(0, x , v  )}, ∅, {(x , 0)}.

which means that Σ0 ≡ (ls NE x 0 ∗ y → 0) and Σ1 ≡ (x → x ∗ ls NE y x ∗ ls NE x 0)
are joined to Σ ≡ (ls NE x v  ∗ ls NE y v  ∗ ls PE v  0). The judgment also says that v 
in Σ corresponds to 0 in Σ0 and x in Σ1 . Note that the δ1 component of the
judgment is {(x , 0)}, and it reﬂects the fact that ls NE x 0 in Σ1 is generalized
to a possibly empty list and results in ls PE v  0 in Σ.
   The derivation rules of the  predicate are given in Figure 1. The ﬁrst two
rules deal with the cases when emp or true appear in both Σ0 and Σ1 . The third
rule has to do with generalizing two lists or abstracting a points-to to a list,
and the last two rules are about generalizing (or synthesizing) possibly empty
lists. Note that when possibly empty lists are introduced by the last two rules,
the appropriate δi component is extended with the information about the ls
predicate of Σi that supports this generalization.
   The ﬁrst stage of † works as follows:
    † searches for Σ,  , δ0 , δ1 for which Σ0 , Σ1 , ∅  Σ,  , δ0 , δ1 can be derived
 1. 
    using the rules in Figure 1. This proof search proceeds by viewing rules
    backward from conclusion to premise. It searches for a rule whose conclusion
    has the left hand side matching with Σ0 , Σ1 ,  and whose side condition is
    satisﬁed with this matching. Once such a rule is found, the search modiﬁes
    Σ0 , Σ1 ,  such that they ﬁt the left hand side of the  judgment in the
    premise. The search continues with this modiﬁed Σ0 , Σ1 , , until it hits the
    base case (i.e., the ﬁrst rule in Figure 1). Figure 2 shows an example proof
    search. If the search fails, the join fails.
    † checks whether for all (e0 , e1 , e), (f0 , f1 , f ) ∈  ∪ {(e, e, e) | e not primed var}
 2. 
    and all i ∈ {0, 1},

                        ei = fi ∧ ei = 0 =⇒ (e1−i , f1−i ) ∈ eq(δ1−i ) ,

      where eq(δi ) is the least equivalence relation containing δi . Intuitively this
      condition amounts to the following: consider Σ0 and Σ1 viewed as graphs
      with edges for → and ls, and then identify vertices according to the returned
      δ’s, then they should be isomorphic via  ∪ {(e, e, e) | e not primed var}.
                                         Scalable Shape Analysis for Systems Code               393



        A(e, f ) ::= (e → f ) | ls k e f       EQ = {(e, e, e) | e is not a primed var}
                    PE  NE = NE  PE = PE  PE = PE             NE  NE = NE

          A(e, f )  A(e, f ) = A(e, f ) (ls k0 e f )  (ls k1 e f ) = (ls (k0  k1 ) e f )
                     (e → f )  (ls k e f ) = (ls k e f )  (e → f ) = ls k e f
                                                    Σ0 , Σ1 ,   Σ ,  , δ0 , δ1
                                   emp                                                         true
 emp, emp,   emp, , ∅, ∅                 true ∗ Σ0 , true ∗ Σ1 ,   true ∗ Σ,  , δ0 , δ1
                    Σ0 , Σ1 , ext(, f0 , f1 , f )  Σ ,  , δ0 , δ1
                                                                                            match
 A0 (e0 , f0 ) ∗ Σ0 , A1 (e1 , f1 ) ∗ Σ1 ,   (A0 (e, f )  A1 (e, f )) ∗ Σ ,  , δ0 , δ1
                                           (when (e0 , e1 , e) ∈ ( ∪ EQ) ∧ comb (f0 , f1 ) = f )
                 Σ0 , Σ1 , ext(, f0 , e1 , f )  Σ ,  , δ0 , δ1
                                                                                 PE-left
       (ls k e0 f0 ) ∗ Σ0 , Σ1 ,   (ls PE e f ) ∗ Σ ,  , δ0 ∪(e0 , f0 ) , δ1
             (when (e0 , e1 , e) ∈ ( ∪ EQ) ∧ e1 ∈ MayAlloc(Σ1 ) ∧ comb (f0 , e1 ) = f )
                 Σ0 , Σ1 , ext(, e0 , f1 , f )  Σ ,  , δ0 , δ1
                                                                                 PE-right
       Σ0 , (ls k e1 f1 ) ∗ Σ1 ,   (ls PE e f ) ∗ Σ ,  , δ0 , δ1 ∪(e1 , f1 )
           (when (e0 , e1 , e) ∈ ( ∪ EQ) ∧ e0 ∈ MayAlloc(Σ0 ) ∧ comb (e0 , f1 ) = f )

Here (a) we write X ∪x instead of X ∪{x}; (b) ext(, e0 , e1 , e) is (∪(e0 , e1 , e))−EQ; (c)
MayAlloc(Σ) is the set of expressions that appear on the left hand side of a points-to
predicate or as a ﬁrst expression argument of ls in Σ; (d) comb is a function deﬁned as:
                   ⎧
                   ⎨e                                if (e0 , e1 , e) ∈  for some e
 comb (e0 , e1 ) = e0                               if e0 =e1 and e0 is not a primed var
                   ⎩ 
                     x for some x ∈ FV(, e0 , e1 ) otherwise


                                      Fig. 1. Rules for 

      Only when the check succeeds does the ﬁrst stage of         † return Σ,  . For
      instance, given Σ0 ≡ (x → y) ∗ ls NE y 0 and Σ1 ≡ ls NE x 0 ∗ (y → 0), the proof
      search in the previous step succeeds with

              Σ ≡ ls NE x y  ∗ ls NE y 0,         ≡ {(y, 0, y  )},      δ0 ≡ δ1 ≡ ∅.

      However, the ﬁnal check on  fails, since y in the Σ0 symbolic heap is related
      to both 0 (by  ) and y (by default) in Σ1 . Thus, the join fails. Note that the
      failure is desired in this case since Σ0 and Σ1 describe heaps with diﬀerent
      shapes.

4.2     Composite Structures
In order to handle composite structures, such as nested lists, we adjust the def-
inition of 
           † in the previous section. Speciﬁcally, we change the rules for the 
relation in Figure 1. Firstly, we modify the third rule, which is used to generalize
394      H. Yang et al.


                                                                emp
                       emp , emp ,   emp ,  , ∅ , ∅
                                                                           PE-right
               emp , (ls NE x 0) ,   ls PE v  0 ,  , ∅ , {(x , 0)}
                                                                                               match
 (y → 0) , (ls NE y x ∗ ls NE x 0) ,   ls NE y v  ∗ ls PE v  0 ,  , ∅ , {(x , 0)}
                                                                                               match
          (ls NE x 0 ∗ y → 0) , (x → x ∗ ls NE y x ∗ ls NE x 0) , ∅
                             ls NE x v  ∗ ls NE y v  ∗ ls PE v  0 ,  , ∅ , {(x , 0)}


                  Fig. 2. Example proof search, where  = {(0, x , v  )}


two ls or points-to predicates, such that it can deal with points-to predicates
with multiple ﬁelds f and a parameterized list-segment predicate. Each of the
new rules, shown in Figure 3, corresponds to one of the four cases of A0  A1
in the third rule of Figure 1. The ﬁrst rule combines two points-to predicates
with multiple ﬁelds, by extending  with the targets of all the ﬁelds. The other
rules generalize two list-segment predicates (the second rule) or a list segment
and its length-one instance (the third and fourth rules), by looking inside the
two available descriptions of list nodes (denoted φ0 and φ1 ), and chooses the
more general one (denoted φ0  φ1 ). In the third rule of Figure 3, the ﬁrst input
symbolic heap is decomposed into φ0 (e0 , f0 )[e/x ] ∗ Σ0 using a frame inference
algorithm [4] to subtract a symbolic heap φ0 (e0 , f0 )[e/x ] such that φ0 can be
-joined with φ1 , leaving Σ0 as a remainder. And similarly in the fourth rule.
Secondly, we change the remaining rules in Figure 1 such that they work with
parameterized list-segment predicates. We simply replace all unparameterized
list-segment predicates ls k e e in the rules by parameterized ones ls k φ e e .
    After these changes,  † works for composite structures. For instance, let
φd (x, y) ≡ (x → d:y), φ(x, y) ≡ ∃x . (x → d:x , f:y) ∗ (ls PE φd x 0), and ψ(x, y) ≡
(x → d:0, f:y). Given two symbolic heaps

      (ls NE φ x y) ∗ (y → d:y  , f:0) ∗ (y  → d:0)    ∨     (ls PE ψ x y) ∗ (ls PE φ y 0),

the † generalizes the list segments from x to y to a possibly empty φ-shaped
list since ψ(x, y)  φ(x, y). Then, it views the two points-to facts on y and y 
as an instantiation φ (x, y)[y  /x ] of φ (x, y) ≡ ∃x . (x → d:x , f:y) ∗ (x → d:0),
combines these facts with the list y since φ (x, y)  φ(x, y), and produces

                                     ls PE φ x y ∗ ls PE φ y 0.

4.3    Incorporating 
                     † into the Analysis
SpaceInvader incorporates    † together with RHS [22], a now-standard inter-
procedural analysis algorithm. RHS associates a set of symbolic heaps with each
program point, which represents the disjunction of those heaps.  † is applied to
reduce the number of disjuncts in those sets.
   Given a set of symbolic heaps at a program point, the analysis takes two
symbolic heaps in the set and applies 
                                      † to them. If the application succeeds, the
                                             Scalable Shape Analysis for Systems Code                395


         ⎧
         ⎨ φ0                     if φ1 (x, y)     φ0 (x, y)        where φ0 (x, y) φ1 (x, y) denotes
φ0  φ1 = φ1                      if φ0 (x, y)     φ1 (x, y)        a call to a sound theorem prover
         ⎩
           undeﬁned               otherwise                         for fresh x, y
                  Σ0 , Σ1 , ext(ext(, f0 , f1 , f ), g0 , g1 , g)  Σ,  , δ0 , δ1
                                                                                              match1
(e0 → f:f0 , g:g0 ) ∗ Σ0 , (e1 → f:f1 , g:g1 ) ∗ Σ1 ,   (e → f:f, g:g) ∗ Σ,  , δ0 , δ1
                   (when (e0 , e1 , e) ∈ ( ∪ EQ) ∧ comb (f0 , f1 )=f ∧ comb (g0 , g1 )=g)
                        Σ0 , Σ1 , ext(, f0 , f1 , f )  Σ,  , δ0 , δ1
                                                                                             match2
ls k0 φ0 e0 f0 ∗ Σ0 , ls k1 φ1 e1 f1 ∗ Σ1 ,   ls (k0 k1 ) (φ0 φ1 ) e f ∗ Σ,  , δ0 , δ1
               (when (e0 , e1 , e) ∈ ( ∪ EQ) ∧ φ0  φ1 is deﬁned ∧ comb (f0 , f1 ) = f )
                        Σ0 , Σ1 , ext(, f0 , f1 , f )  Σ,  , δ0 , δ1
                                                                                                   match3
 φ0 (e0 , f0 )[e/x ] ∗ Σ0 , (ls k φ1 e1 f1 ) ∗ Σ1 ,   (ls k (φ0 φ1 ) e f ) ∗ Σ,  , δ0 , δ1
                  (when (e0 , e1 , e) ∈ ( ∪ EQ) ∧ φ0  φ1 is deﬁned ∧ comb (f0 , f1 ) = f )
                        Σ0 , Σ1 , ext(, f0 , f1 , f )  Σ,  , δ0 , δ1
                                                                                                   match4
 (ls k φ0 e0 f0 ) ∗ Σ0 , φ1 (e1 , f1 )[e/x ] ∗ Σ1 ,   (ls k (φ0 φ1 ) e f ) ∗ Σ,  , δ0 , δ1
                (when (e0 , e1 , e) ∈ ( ∪ EQ) ∧ φ0  φ1 is deﬁned ∧ comb (f0 , f1 ) = f )

Here −[e/x ] in φ(e, f )[e/x ] is the substitution of all the existentially quantiﬁed
primed variables x in φ(e, f ) by e.


                   Fig. 3. Sample rules for . Composite structure case.

result of the join replaces those heaps. Otherwise, those two symbolic heaps are
returned to the set.
   In order to maintain precision in the analysis, we restrict the application of 
                                                                                  †
to only those program points where controlling the number of disjuncts is cru-
cial. They are (a) the beginning of loops, (b) the end of conditional statements
when those statements are not inside loops, (c) the call sites of procedures, and
(d) the exit points of procedures. The ﬁrst case accelerates the analysis of the
usual ﬁxed-point computation for loops, and the second prevents the combina-
torial explosion caused by a sequence of conditional statements; for instance,
the procedure register cdrom in cdrom.c uses 25 conditional statements to
adjust values of a structure for cdrom, which makes the analysis without join
suﬀer from a serious performance problem. The other two cases aim for comput-
ing small procedure summaries; the third reduces the number of input symbolic
heaps to consider for each procedure, and the last reduces the analysis results
of a procedure with respect to each symbolic heap.
   We have measured the eﬀects of      † on the performance of SpaceInvader,
using our seven driver examples. Table 3 reports the results of our measurements.
The third and fourth columns of the table record the time of analyzing the drivers
without using   † : without 
                             † , we cannot analyze our example drivers except the
simplest one, scull.c. The next two columns concern a pivotal design decision
for † , looking at variations on the ls predicate; the ﬁfth column considers the
necessarily non-empty ls predicate only, and the sixth column considers both
396     H. Yang et al.


Table 3. Experimental results on the eﬀects of     † . Timeout (X) set at 90min. Exper-
iments run on Intel Core Duo 2.0GHz with 2GB RAM. The ”Opt. except           † ” column
records the results of the analysis runs without † nor possibly empty ls predicates, but
with two optimizations: discarding the intermediate analysis results and passing only
the reachable portion of the heap to a procedure. The next column contains the analy-
sis time with these two optimizations and  † , but without possibly empty ls predicates.
The last column contains the analysis time with all the optimizations.

                      No Opt. Opt. except † Opt. including †,    Opt. including 
                                                                                  †,
Program      LOC         (sec)         (sec) with NE only (sec) with NE and PE (sec)
scull.c      1010         1.41          1.15               0.59                 0.36
class.c      1983            X             X             48.24                  8.21
pci-driver.c 2532            X             X               2.69                 0.97
ll rw blk.c  5469            X             X                  X               887.94
cdrom.c      6218            X             X            193.01                103.26
md.c         6653            X             X                  X              1585.69
t1394Diag.c 10240            X             X           3415.76                135.05


the necessarily non-empty and possibly empty ls predicates. These experimental
results conﬁrm the beneﬁt of using the ls PE predicate in 
                                                          †.


5     Related Work
Device driver veriﬁcation has attracted considerable interest due to the realiza-
tion that most OS failures arise from bugs in device drivers [8,24,2]. Tools like
Slam [2] and Blast [15] have been eﬀectively applied in veriﬁcation of properties
of real device drivers, especially properties describing the calling conventions of
OS kernel APIs. Unfortunately these tools use coarse models of the heap; Slam,
for example, assumes memory safety. Other tools are known to prove memory
safety, but with the restriction that the input programs do not perform dynamic
memory allocation (e.g. ASTRÉE [6]). Proving full memory safety (which in-
cludes array bounds errors as well as what we have termed pointer safety) of
entire systems programs is thus a more diﬃcult problem than that considered
in this paper, or in work that concentrates on array bounds errors.
   Several papers report on the results of applying shape analysis to the source
code of substantial, real-world systems programs. The analysis in [14] has been
applied to non-trivial code, but the abstract domain there is purposely much less
precise than here, and it could not be used to verify pointer safety of the device
drivers that we consider. [7] includes an analysis of a restricted and modiﬁed
version of the Linux scull driver. Our analysis terminates on the modiﬁed scull
code (which they kindly supplied to us) in 0.36sec, where [7] terminated in
9.71sec when using user-supplied assertions (which we did not use) to help the
analysis along. It is also worth mentioning [13], which uses slicing to remove
heap-irrelevant statements. An earlier version of SpaceInvader [3] analyzed
several procedures from the 1394 driver used in Table 1. It timed out on an 1800
LOC subset of the driver, and this drove us to consider   †.
                                   Scalable Shape Analysis for Systems Code         397

   The very idea of a join operator is of course not novel, and many other joins
have been successfully applied in their application domain. The problem is al-
ways one of balancing precision and speed. The claim that    † does not lose too
much precision is backed up with experimental results.     † is not unrelated to
other join operators that have been proposed in shape analysis [19,1,7]. For in-
stance, Chang et al. deﬁne a partial join operator for separation logic formulas,
and Arnold [1] develops a notion of “loose embedding” in TVLA [16] which is
in an intuitive sense related to our use of predicates for possibly-empty, rather
than only nonempty, lists. However, our   † is diﬀerent in its detailed formula-
tion; unlike Chang et al., we simplify symbolic heaps before applying     † , and
unlike Arnold and Manevich [19,1], our  † keeps the structure of composite data
structures precisely. The latter diﬀerence, in particular, is crucial to verifying
the drivers.
   Marron et al. reports on shape analyses of several Java programs of up to 3705
LOC [20]. They use an aggressive join operator which always merges several
abstract states into one. Such a join operator would lead to many false alarms
when applied to our device drivers (for example, when dealing with exceptional
conditions), and so is too imprecise for our goal of proving pointer safety.

6   Conclusions
This paper has presented the ﬁrst application of shape analysis to a real-world
industrial veriﬁcation problem: proving pointer safety of entire Windows and
Linux device drivers. We have achieved this milestone by enhancing our separa-
tion domain based shape analysis tool with a sophisticated new join operation,

† . This paper has made two contributions:   † , and a demonstration that shape
analysis can be scaled to real-world industrial veriﬁcation problems. The second
contribution is, in a sense, the most important one. We hope, now that we know
that whole device drivers can be accurately handled by today’s shape analysis
tools, that future research papers on the subject will use device drivers and other
substantial systems programs as a part of their experimental evaluations.

Acknowledgments. We would like to thank Viktor Vafeiadis for helpful discus-
sions on the OCaml garbage collector. The London authors acknowledge the
support of the EPSRC. Lee was supported by Brain Korea 21. Distefano was
supported by a Royal Academy of Engineering research fellowship. O’Hearn was
supported by a Royal Society Wolfson Research Merit Award.


References
 1. Arnold, G.: Specialized 3-valued logic shape analysis using structure-based reﬁne-
    ment and loose embedding. In: Yi, K. (ed.) SAS 2006. LNCS, vol. 4134, pp. 204–220.
    Springer, Heidelberg (2006)
 2. Ball, T., Bounimova, E., Cook, B., Levin, V., Lichtenberg, J., McGarvey, C., On-
    drusek, B., Rajamani, S.K., Ustuner, A.: Thorough static analysis of device drivers.
    In: EuroSys (2006)
398     H. Yang et al.

 3. Berdine, J., Calcagno, C., Cook, B., Distefano, D., O’Hearn, P., Wies, T., Yang,
    H.: Shape analysis of composite data structures. In: Damm, W., Hermanns, H.
    (eds.) CAV 2007. LNCS, vol. 4590, pp. 178–192. Springer, Heidelberg (2007)
 4. Berdine, J., Calcagno, C., O’Hearn, P.: Symbolic execution with separation logic.
    In: Yi, K. (ed.) APLAS 2005. LNCS, vol. 3780, pp. 52–68. Springer, Heidelberg
    (2005)
 5. Berdine, J., Lev-Ami, T., Manevich, R., Ramalingam, G., Sagiv, M.: Thread quan-
    tiﬁcation for concurrent shape analysis. In: CAV (2008)
 6. Blanchet, B., Cousot, P., Cousot, R., Feret, J., Mauborgne, L., Miné, A., Monniaux,
    D., Rival, X.: A static analyzer for large safety-critical software. In: PLDI (2003)
 7. Chang, B., Rival, X., Necula, G.: Shape analysis with structural invariant check-
    ers. In: Riis Nielson, H., Filé, G. (eds.) SAS 2007. LNCS, vol. 4634, pp. 384–401.
    Springer, Heidelberg (2007)
 8. Chou, A., Yang, J., Chelf, B., Hallem, S., Engler, D.R.: An empirical study of
    operating system errors. In: SOSP (2001)
 9. Cousot, P., Cousot, R.: Abstract interpretation: A uniﬁed lattice model for static
    analysis of programs by construction or approximation of ﬁxpoints. In: POPL (1977)
10. Distefano, D., O’Hearn, P., Yang, H.: A local shape analysis based on separation
    logic. In: Hermanns, H., Palsberg, J. (eds.) TACAS 2006 and ETAPS 2006. LNCS,
    vol. 3920, pp. 287–302. Springer, Heidelberg (2006)
11. Gotsman, A., Berdine, J., Cook, B.: Interprocedural shape analysis with sepa-
    rated heap abstractions. In: Yi, K. (ed.) SAS 2006. LNCS, vol. 4134, pp. 240–260.
    Springer, Heidelberg (2006)
12. Gotsman, A., Berdine, J., Cook, B., Sagiv, M.: Thread-modular shape analysis. In:
    PLDI (2007)
13. Guo, B., Vachharajani, N., August, D.: Shape analysis with inductive recursion
    synthesis. In: PLDI (2007)
14. Hackett, B., Rugina, R.: Region-based shape analysis with tracked locations. In:
    POPL (2005)
15. Henzinger, T., Jhala, R., Majumdar, R., McMillan, K.: Abstractions from proofs.
    In: POPL (2004)
16. Lev-Ami, T., Sagiv, M.: TVLA: A system for implementing static analyses. In: Pals-
    berg, J. (ed.) SAS 2000. LNCS, vol. 1824, pp. 280–302. Springer, Heidelberg (2000)
17. Magill, S., Nanevski, A., Clarke, E., Lee, P.: Inferring invariants in Separation
    Logic for imperative list-processing programs. In: SPACE (2006)
18. Manevich, R., Lev-Ami, T., Ramalingam, G., Sagiv, M., Berdine, J.: Heap decom-
    position for concurrent shape analysis. In: SAS (2008)
19. Manevich, R., Sagiv, M., Ramalingam, G., Field, J.: Partially disjunctive heap
    abstraction. In: Giacobazzi, R. (ed.) SAS 2004. LNCS, vol. 3148, pp. 265–279.
    Springer, Heidelberg (2004)
20. Marron, M., Hermenegildo, M., Kapur, D., Stefanovic, D.: Eﬃcient context-
    sensitive shape analysis with graph based heap models. In: CC (2008)
21. O’Hearn, P., Reynolds, J., Yang, H.: Local reasoning about programs that alter
    data structures. In: Fribourg, L. (ed.) CSL 2001 and EACSL 2001. LNCS, vol. 2142.
    Springer, Heidelberg (2001)
22. Reps, T., Horwitz, S., Sagiv, M.: Precise interprocedural dataﬂow analysis via
    graph reachability. In: POPL (1995)
23. Rinetzky, N., Bauer, J., Reps, T., Sagiv, M., Wilhelm, R.: A semantics for proce-
    dure local heaps and its abstractions. In: POPL (2005)
24. Swift, M.M., Bershad, B.N., Levy, H.M.: Improving the reliability of commodity
    operating systems. In: SOSP (2003)
